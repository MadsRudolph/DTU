"""Reconnaissance against a live DTU Learn session.

Dumps the raw payload of every endpoint the sync depends on, so a shape change
on DTU's side can be diagnosed by diffing rather than guessing. Run it whenever
a collector starts returning nothing.

Nothing is downloaded, filed, committed or pushed by this command.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .collectors.content import TOC_PATH
from .collectors.courses import ENROLMENTS_PATH, parse_enrollments
from .collectors.events import EVENTS_PATH
from .collectors.news import NEWS_PATH

log = logging.getLogger(__name__)


def _write(directory: Path, name: str, payload) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    if isinstance(payload, (dict, list)):
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        path.write_text(str(payload), encoding="utf-8")


def run(session, out_dir: Path, semesters=None) -> dict:
    """Probe every endpoint the sync uses and dump what came back."""
    out_dir = Path(out_dir)
    summary: dict = {"courses": [], "endpoints": {}}

    enrolments = session.get_json(ENROLMENTS_PATH)
    if enrolments is None:
        summary["endpoints"]["enrolments"] = "FAILED — session may be dead"
        return summary

    _write(out_dir, "enrolments.json", enrolments)
    total = len(enrolments.get("Items") or [])
    courses = parse_enrollments(enrolments, semesters=semesters)
    summary["endpoints"]["enrolments"] = f"ok — {total} enrolments, {len(courses)} in scope"
    summary["courses"] = [
        {"code": c.code, "name": c.name, "org_unit_id": c.org_unit_id} for c in courses
    ]

    if not courses:
        log.warning(
            "no courses in scope — check the `semesters` list in rules.yaml "
            "against the Code fields in enrolments.json"
        )
        return summary

    probe = courses[0]
    log.info("probing against %s (org unit %s)", probe.code, probe.org_unit_id)

    now = datetime.now(timezone.utc)
    stamp = "%Y-%m-%dT%H:%M:%S.000Z"

    for label, path in (
        ("toc", TOC_PATH.format(org_unit_id=probe.org_unit_id)),
        ("news", NEWS_PATH.format(org_unit_id=probe.org_unit_id)),
        (
            "events",
            EVENTS_PATH.format(
                org_unit_id=probe.org_unit_id,
                start=(now - timedelta(days=30)).strftime(stamp),
                end=(now + timedelta(days=210)).strftime(stamp),
            ),
        ),
    ):
        payload = session.get_json(path)
        if payload is None:
            summary["endpoints"][label] = "FAILED — no JSON returned"
            log.warning("%s: %s returned no JSON", label, path)
            continue

        _write(out_dir, f"{label}.json", payload)
        if isinstance(payload, list):
            size = f"{len(payload)} items"
        else:
            size = f"keys {list(payload)[:6]}"
        summary["endpoints"][label] = f"ok — {size}"

    _write(out_dir, "summary.json", summary)
    return summary
