"""One-off reconnaissance against a live DTU Learn session.

Everything downstream of the collectors is already pinned down by tests. What
cannot be known without logging in is which Brightspace endpoints this DTU
instance actually serves, and what their payloads look like.

`learn-sync discover` logs in once, tries each candidate endpoint, and writes
whatever comes back into fixtures/discovery/. Those dumps become the test
fixtures the collectors are then built against -- so no collector is ever
trusted on a guess about the payload shape.

Nothing is downloaded, filed, committed or pushed by this command.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .collectors.courses import parse_courses

log = logging.getLogger(__name__)

# Candidate table-of-contents endpoints, most specific first.
TOC_CANDIDATES = [
    "/d2l/api/le/1.67/{ou}/content/toc",
    "/d2l/api/le/1.50/{ou}/content/toc",
    "/d2l/le/content/{ou}/fullTOC",
]

NEWS_CANDIDATES = [
    "/d2l/lms/news/main.d2l?ou={ou}",
    "/d2l/le/news/{ou}/mainpage",
]

CALENDAR_CANDIDATES = [
    "/d2l/le/calendar/{ou}/feed/list",
    "/d2l/le/calendar/{ou}/mainView",
]


def _write(directory: Path, name: str, payload) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    if isinstance(payload, (dict, list)):
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        path.write_text(str(payload), encoding="utf-8")
    return path


def run(session, out_dir: Path) -> dict:
    """Probe the instance and dump everything useful. Returns a short summary."""
    out_dir = Path(out_dir)
    summary: dict = {"courses": [], "working_endpoints": {}, "dumped": []}

    dashboard = session.get_text("/d2l/home")
    summary["dumped"].append(str(_write(out_dir, "dashboard.html", dashboard)))

    courses = parse_courses(dashboard)
    summary["courses"] = [
        {"code": c.code, "name": c.name, "org_unit_id": c.org_unit_id} for c in courses
    ]
    log.info("found %d courses: %s", len(courses), [c.code for c in courses])

    if not courses:
        log.warning(
            "no courses parsed from the dashboard -- inspect dashboard.html; "
            "the My Courses widget may load over XHR"
        )
        return summary

    probe = courses[0]
    log.info("probing endpoints against %s (org unit %s)", probe.code, probe.org_unit_id)

    for label, candidates in (
        ("toc", TOC_CANDIDATES),
        ("news", NEWS_CANDIDATES),
        ("calendar", CALENDAR_CANDIDATES),
    ):
        for template in candidates:
            path = template.format(ou=probe.org_unit_id)
            payload = session.get_json(path)
            kind = "json"

            if payload is None:
                payload = session.get_text(path)
                kind = "html"
                if not payload or "Sign In" in payload[:2000]:
                    continue

            suffix = "json" if kind == "json" else "html"
            written = _write(out_dir, f"{label}.{suffix}", payload)
            summary["working_endpoints"][label] = {"path": template, "type": kind}
            summary["dumped"].append(str(written))
            log.info("%s: %s served %s", label, path, kind)
            break
        else:
            log.warning("%s: none of the candidate endpoints responded usefully", label)

    _write(out_dir, "summary.json", summary)
    return summary
