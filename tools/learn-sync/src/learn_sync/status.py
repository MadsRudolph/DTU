"""A small JSON status file for the Glance dashboard.

The sync is a one-shot container: it has no HTTP surface, so a dashboard has
nothing to poll and no way to tell a healthy run from one that has been failing
silently for a week. Each run writes this; a static file server on the container
exposes it at http://<container>:8099/status.json.

Written even when the run fails -- a stale `last_run` or `needs_reauth: true` is
exactly what the dashboard needs to show.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

STATUS_DIR = Path("/srv/learn-sync/status")


def render_status(
    report,
    state,
    ok: bool,
    courses: int,
    when: datetime,
    needs_reauth: bool = False,
) -> dict:
    """Everything the dashboard needs, in one flat object."""
    return {
        "ok": ok,
        "needs_reauth": needs_reauth,
        "last_run": when.replace(microsecond=0).isoformat(),
        "courses": courses,
        "files_tracked": len(state.known_vault_paths()),
        "files_added": len(report.files_added),
        "announcements": len(report.announcements),
        "deadlines": len(report.events),
        "warnings": list(report.warnings),
    }


def write_status(path: Path, status: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
