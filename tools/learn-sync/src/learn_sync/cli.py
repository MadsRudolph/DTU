"""Entry points: sync, auth, discover.

The orchestration lives here; every decision it makes is delegated to a module
that is tested on its own.
"""

from __future__ import annotations

import argparse
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .auth import AuthFailed, ensure_authenticated, open_session
from .collectors.content import TOC_PATH, parse_toc
from .collectors.courses import ENROLMENTS_PATH, parse_enrollments
from .collectors.events import EVENTS_PATH, parse_events
from .collectors.news import NEWS_PATH, parse_news
from .delivery import Delivery, DeliveryFailed
from .filing import load_rules
from .notes import (
    inject_block,
    render_announcements,
    render_deadlines,
    render_index,
    write_note,
)
from .models import RunReport
from .notify import DiscordNotifier
from .session import Session
from .state import State
from .status import STATUS_DIR, render_status, write_status
from .sync import Sync

log = logging.getLogger("learn_sync")

HERE = Path(__file__).resolve().parent.parent.parent
DEADLINE_MARKER = "learn-sync:deadlines"
COURSES_ROOT = "Obsidian/Courses"

# The calendar API answers 400 without an explicit range.
LOOK_BACK = timedelta(days=30)
LOOK_AHEAD = timedelta(days=210)


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
        self.status_path = Path(
            os.environ.get("LEARN_STATUS", STATUS_DIR / "status.json")
        )


def _write_note(path: Path, content: str, touched: list[str], repo_root: Path) -> None:
    touched.append(write_note(path, content, repo_root))


def _date_range():
    now = datetime.now(timezone.utc)
    stamp = "%Y-%m-%dT%H:%M:%S.000Z"
    return (now - LOOK_BACK).strftime(stamp), (now + LOOK_AHEAD).strftime(stamp)


def _authenticated_context(playwright, config, notifier=None):
    """Open a browser and guarantee a live Learn session, or raise AuthFailed."""
    browser, context = open_session(playwright, config.storage_state)
    try:
        ensure_authenticated(context, config.storage_state, config.username,
                             config.password)
    except AuthFailed:
        browser.close()
        raise
    return browser, context


def cmd_sync(args) -> int:
    from playwright.sync_api import sync_playwright

    config = Config()
    notifier = DiscordNotifier(config.webhook)

    # Pull before anything is read from disk. rules.yaml and state.json are
    # loaded once below and never touched again until this run writes state
    # back out at the end -- pulling after that load would fetch newer
    # content only for it to be silently overwritten by the stale in-memory
    # state a few seconds later (this bit a manual state.json edit made
    # between runs: the very next run's own commit reverted it).
    if not args.dry_run:
        # A pull that cannot be rescued has to be announced. Before this was
        # wrapped, a DeliveryFailed here escaped as a bare traceback: systemd
        # logged a failed unit, Discord heard nothing, the status file kept
        # showing the last good run, and the service sat wedged for five days
        # while looking, from the outside, exactly like a quiet week.
        try:
            Delivery(config.repo_root).pull()
        except DeliveryFailed as failure:
            notifier.alert(
                "DTU Learn sync: the repo is wedged",
                f"{failure}\n\nNo material was fetched. Until the clone at "
                "/srv/learn-sync/repo can pull, every run will fail this way.",
            )
            log.error("pull failed: %s", failure)
            write_status(
                config.status_path,
                render_status(RunReport(), State.load(config.state_path), ok=False,
                              courses=0, when=datetime.now().astimezone()),
            )
            return 3

    rules = load_rules(config.rules_path.read_text(encoding="utf-8"))
    state = State.load(config.state_path)
    delivery = Delivery(config.repo_root)

    touched: list[str] = []

    with sync_playwright() as playwright:
        try:
            browser, context = _authenticated_context(playwright, config)
        except AuthFailed as failure:
            notifier.alert(
                "DTU Learn: re-auth needed",
                f"{failure.landing.value} at {failure.url} ({failure.title})\n\n"
                "Run `learn-sync auth` to sign in again.",
            )
            log.error("authentication failed: %s", failure)
            write_status(
                config.status_path,
                render_status(RunReport(), state, ok=False, courses=0,
                              when=datetime.now().astimezone(), needs_reauth=True),
            )
            return 2

        session = Session(context)
        syncer = Sync(rules, state, config.repo_root, session.download, args.dry_run)

        enrolments = session.get_json(ENROLMENTS_PATH)
        courses = parse_enrollments(enrolments or {}, semesters=rules.semesters)
        log.info("syncing %d courses: %s", len(courses), [c.code for c in courses])

        start, end = _date_range()

        for course in courses:
            toc = session.get_json(TOC_PATH.format(org_unit_id=course.org_unit_id))
            if toc is None:
                syncer.report.warnings.append(
                    f"no content tree returned for {course.code}"
                )
            else:
                topics = parse_toc(toc, course)
                syncer.process(course, topics)

                if not args.dry_run:
                    entries = [
                        (t.module_path, t.title, state.vault_path_for(t.topic_id))
                        for t in topics
                        if state.vault_path_for(t.topic_id)
                    ]
                    if entries:
                        folder = rules.vault_folder(course)
                        _write_note(
                            config.repo_root / COURSES_ROOT / folder / "_Learn/INDEX.md",
                            render_index(folder, entries),
                            touched,
                            config.repo_root,
                        )

            news = parse_news(
                session.get_json(NEWS_PATH.format(org_unit_id=course.org_unit_id)) or [],
                course,
                since=state.newest_announcement(course.code),
            )
            syncer.report.announcements.extend(news)

            if not args.dry_run:
                folder = rules.vault_folder(course)
                path = config.repo_root / COURSES_ROOT / folder / "_Learn/Announcements.md"
                # Re-render whenever the file exists, not only when there is news.
                # An existing note is unchanged by an empty render, but naming it
                # is what gets a file left behind by an aborted run into the commit.
                if news or path.exists():
                    existing = path.read_text(encoding="utf-8") if path.exists() else ""
                    _write_note(path, render_announcements(existing, news), touched,
                                config.repo_root)
                if news:
                    state.set_newest_announcement(
                        course.code, max(n.announcement_id for n in news)
                    )

            events = parse_events(
                session.get_json(
                    EVENTS_PATH.format(
                        org_unit_id=course.org_unit_id, start=start, end=end
                    )
                ) or {},
                course,
            )
            # Only deadlines are surfaced: the weekly timetable is already in
            # Home.md by hand, and the report must describe exactly what gets
            # written or the commit message starts claiming things it did not do.
            syncer.report.events.extend(e for e in events if e.kind == "assignment")

        browser.close()

    if args.dry_run:
        for code, path in syncer.report.files_added:
            print(f"  {code}  {path}")
        for warning in syncer.report.warnings:
            print(f"  ! {warning}")
        print(
            f"\n{len(syncer.report.files_added)} file(s), "
            f"{len(syncer.report.announcements)} announcement(s), "
            f"{len(syncer.report.events)} deadline(s) — nothing written"
        )
        return 0

    home = config.repo_root / "Obsidian/Home.md"
    if syncer.report.events and home.exists():
        _write_note(
            home,
            inject_block(home.read_text(encoding="utf-8"), DEADLINE_MARKER,
                         render_deadlines(syncer.report.events)),
            touched,
            config.repo_root,
        )

    # Files routed outside the vault (tool files under "5. Semester/...") are
    # small, git-native project files, not gitignored binaries bound for Drive
    # -- commit them directly rather than leaving them untracked forever.
    for _code, path in syncer.report.files_added + syncer.report.files_adopted:
        if not (path == COURSES_ROOT or path.startswith(COURSES_ROOT + "/")):
            touched.append(path)

    state.save(config.state_path)
    touched.append(str(config.state_path.relative_to(config.repo_root)).replace("\\", "/"))

    try:
        committed = delivery.publish(syncer.report, touched)
    except DeliveryFailed as failure:
        # Covers a rejected push as well as a failed commit. This used to catch
        # only DriveSyncFailed, so every other delivery problem left the run as a
        # bare traceback with nothing said on Discord -- the same blind spot that
        # hid the wedged pull.
        notifier.alert(
            "DTU Learn sync: could not publish",
            f"{failure}\n\nThe material was downloaded but is still only on the "
            "container. Syncthing has the binaries; the notes are not on GitHub yet.",
        )
        log.error("publish failed: %s", failure)
        write_status(
            config.status_path,
            render_status(syncer.report, state, ok=False, courses=len(courses),
                          when=datetime.now().astimezone()),
        )
        return 3

    log.info("committed=%s files=%d", committed, len(syncer.report.files_added))
    write_status(
        config.status_path,
        render_status(syncer.report, state, ok=True, courses=len(courses),
                      when=datetime.now().astimezone()),
    )
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
    rules = load_rules(config.rules_path.read_text(encoding="utf-8"))
    out_dir = config.tool_dir / "fixtures" / "discovery"

    with sync_playwright() as playwright:
        try:
            browser, context = _authenticated_context(playwright, config)
        except AuthFailed as failure:
            print(f"Not signed in ({failure.landing.value}). Run `learn-sync auth` first.")
            return 2

        summary = discover.run(Session(context), out_dir, semesters=rules.semesters)
        browser.close()

    print(f"\nCourses this semester: {len(summary['courses'])}")
    for course in summary["courses"]:
        print(f"  {course['code']}  {course['name']:<45} ou {course['org_unit_id']}")
    print("\nEndpoints:")
    for label, status in summary["endpoints"].items():
        print(f"  {label:<10} {status}")
    print(f"\nDumps written to {out_dir}")
    return 0


def cmd_test_notify(args) -> int:
    """Prove the configured Discord webhook actually delivers.

    A normal run is silent when nothing is new, so it cannot tell you whether a
    freshly rotated webhook works. This posts one alert unconditionally.
    """
    config = Config()
    if not config.webhook:
        print("DISCORD_WEBHOOK_URL is not set in .env — nothing to test.")
        return 1

    DiscordNotifier(config.webhook).alert(
        "learn-sync", "Webhook test — notifications are working."
    )
    print("Alert sent. Check the Discord channel the webhook belongs to.")
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
    sub.add_parser(
        "test-notify", help="post one Discord alert to prove the webhook works"
    ).set_defaults(func=cmd_test_notify)

    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(message)s",
    )
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
