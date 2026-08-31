"""Entry points: sync, auth, discover.

The orchestration lives here; every decision it makes is delegated to a module
that is tested on its own.
"""

from __future__ import annotations

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

from .auth import AuthFailed, ensure_authenticated, open_session
from .collectors.calendar import parse_ics
from .collectors.content import parse_toc
from .collectors.courses import parse_courses
from .delivery import Delivery, DriveSyncFailed
from .filing import load_rules
from .notes import inject_block, render_announcements, render_deadlines, render_index
from .notify import DiscordNotifier
from .session import Session
from .state import State
from .sync import Sync

log = logging.getLogger("learn_sync")

HERE = Path(__file__).resolve().parent.parent.parent
DEADLINE_MARKER = "learn-sync:deadlines"
UPLOAD_SCRIPT = "Obsidian/scripts/drive-sync/upload.py"


class Config:
    def __init__(self) -> None:
        self.repo_root = Path(os.environ.get("LEARN_REPO", HERE.parent.parent)).resolve()
        self.tool_dir = self.repo_root / "tools" / "learn-sync"
        self.storage_state = Path(
            os.environ.get("LEARN_STORAGE_STATE", self.tool_dir / "storageState.json")
        )
        self.rules_path = self.tool_dir / "rules.yaml"
        self.state_path = self.tool_dir / "state.json"
        self.username = os.environ.get("LEARN_USER", "")
        self.password = os.environ.get("LEARN_PASS", "")
        self.webhook = os.environ.get("DISCORD_WEBHOOK_URL", "")
        self.calendar_feed = os.environ.get("LEARN_CALENDAR_FEED", "")


def _drive_sync(repo_root: Path):
    def run() -> None:
        script = repo_root / UPLOAD_SCRIPT
        if not script.exists():
            log.warning("drive-sync script missing at %s, skipping upload", script)
            return
        result = subprocess.run(
            [sys.executable, str(script), "--sync"],
            cwd=repo_root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise DriveSyncFailed(result.stderr.strip() or "upload.py failed")

    return run


def _write_note(path: Path, content: str, touched: list[str], repo_root: Path) -> None:
    """Write a note only when it actually changed, so unchanged runs make no commit."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")
    touched.append(str(path.relative_to(repo_root)).replace("\\", "/"))


def cmd_sync(args) -> int:
    from playwright.sync_api import sync_playwright

    config = Config()
    notifier = DiscordNotifier(config.webhook)
    rules = load_rules(config.rules_path.read_text(encoding="utf-8"))
    state = State.load(config.state_path)
    delivery = Delivery(config.repo_root, drive_sync=_drive_sync(config.repo_root))

    if not args.dry_run:
        delivery.pull()

    with sync_playwright() as playwright:
        browser, context = open_session(playwright, config.storage_state)
        try:
            ensure_authenticated(context, config.storage_state, config.username,
                                 config.password)
        except AuthFailed as failure:
            notifier.alert(
                "DTU Learn: re-auth needed",
                f"{failure.landing.value} at {failure.url} ({failure.title})\n\n"
                f"Run `learn-sync auth` to sign in again.",
            )
            log.error("authentication failed: %s", failure)
            browser.close()
            return 2

        session = Session(context)
        syncer = Sync(rules, state, config.repo_root, session.download, args.dry_run)
        touched: list[str] = []

        dashboard = session.get_text("/d2l/home")
        courses = parse_courses(dashboard)
        log.info("syncing %d courses", len(courses))

        for course in courses:
            toc = session.get_json(f"/d2l/le/content/{course.org_unit_id}/fullTOC")
            if not toc:
                syncer.report.warnings.append(
                    f"no content tree returned for {course.code}"
                )
                continue

            topics = parse_toc(toc, course)
            syncer.process(course, topics)

            if args.dry_run:
                continue

            entries = [
                (t.module_path, t.title, syncer.state.vault_path_for(t.topic_id))
                for t in topics
                if syncer.state.vault_path_for(t.topic_id)
            ]
            if entries:
                folder = rules.vault_folder(course)
                index = config.repo_root / "Obsidian/Courses" / folder / "_Learn/INDEX.md"
                _write_note(index, render_index(folder, entries), touched,
                            config.repo_root)

        if config.calendar_feed:
            events = parse_ics(session.get_text(config.calendar_feed))
            syncer.report.events = events
            if events and not args.dry_run:
                home = config.repo_root / "Obsidian/Home.md"
                if home.exists():
                    _write_note(
                        home,
                        inject_block(home.read_text(encoding="utf-8"), DEADLINE_MARKER,
                                     render_deadlines(events)),
                        touched,
                        config.repo_root,
                    )

        browser.close()

    if args.dry_run:
        for code, path in syncer.report.files_added:
            print(f"  {code}  {path}")
        for warning in syncer.report.warnings:
            print(f"  ! {warning}")
        print(f"\n{len(syncer.report.files_added)} file(s) would be written")
        return 0

    state.save(config.state_path)
    touched.append(str(config.state_path.relative_to(config.repo_root)).replace("\\", "/"))

    try:
        committed = delivery.publish(syncer.report, touched)
    except DriveSyncFailed as failure:
        notifier.alert("DTU Learn sync: Drive upload failed", str(failure))
        log.error("drive-sync failed: %s", failure)
        return 3

    log.info("committed=%s files=%d", committed, len(syncer.report.files_added))
    notifier.report(syncer.report)
    return 0


def cmd_auth(args) -> int:
    """Open a real browser so a human can sign in, then save the session."""
    from playwright.sync_api import sync_playwright

    config = Config()
    with sync_playwright() as playwright:
        browser, context = open_session(playwright, config.storage_state, headless=False)
        page = context.new_page()
        page.goto("https://learn.inside.dtu.dk/d2l/home")
        print("Sign in in the browser window, then press Enter here.")
        input()
        context.storage_state(path=str(config.storage_state))
        browser.close()

    print(f"Session saved to {config.storage_state}")
    return 0


def cmd_discover(args) -> int:
    from playwright.sync_api import sync_playwright

    from . import discover

    config = Config()
    out_dir = config.tool_dir / "fixtures" / "discovery"

    with sync_playwright() as playwright:
        browser, context = open_session(playwright, config.storage_state)
        try:
            ensure_authenticated(context, config.storage_state, config.username,
                                 config.password)
        except AuthFailed as failure:
            print(f"Not signed in ({failure.landing.value}). Run `learn-sync auth` first.")
            browser.close()
            return 2

        summary = discover.run(Session(context), out_dir)
        browser.close()

    print(f"\nCourses found: {len(summary['courses'])}")
    for course in summary["courses"]:
        print(f"  {course['code']}  {course['name']}  (ou {course['org_unit_id']})")
    print(f"\nWorking endpoints: {summary['working_endpoints']}")
    print(f"Dumps written to {out_dir}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="learn-sync")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sync = sub.add_parser("sync", help="fetch new material and publish it")
    p_sync.add_argument("--dry-run", action="store_true",
                        help="show what would happen, write nothing")
    p_sync.set_defaults(func=cmd_sync)

    sub.add_parser("auth", help="sign in interactively and save the session").set_defaults(
        func=cmd_auth
    )
    sub.add_parser("discover", help="probe the instance and dump payloads").set_defaults(
        func=cmd_discover
    )

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
    )
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
