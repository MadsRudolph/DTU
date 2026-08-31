"""learn-sync publishes a small JSON status for the Glance dashboard.

The sync is a one-shot container with no HTTP surface, so a dashboard has
nothing to poll. Each run writes this file; a tiny static server on the
container exposes it.
"""

import json
from datetime import datetime

from learn_sync.models import Announcement, RunReport
from learn_sync.state import State
from learn_sync.status import render_status, write_status


def announcement(code="34870"):
    return Announcement("1", code, datetime(2026, 9, 1), "t", "b")


def test_a_healthy_run_reports_ok():
    s = render_status(RunReport(), State.empty(), ok=True, courses=4,
                      when=datetime(2026, 9, 1, 8, 0))

    assert s["ok"] is True
    assert s["needs_reauth"] is False
    assert s["courses"] == 4
    assert s["last_run"] == "2026-09-01T08:00:00"


def test_counts_come_from_the_run_report():
    report = RunReport(
        files_added=[("34870", "a.pdf"), ("62755", "b.pdf")],
        announcements=[announcement()],
    )

    s = render_status(report, State.empty(), ok=True, courses=4,
                      when=datetime(2026, 9, 1, 8, 0))

    assert s["files_added"] == 2
    assert s["announcements"] == 1


def test_tracked_file_count_comes_from_state():
    state = State.empty()
    for i in range(3):
        topic = type("T", (), {"topic_id": str(i), "revision": "a"})()
        state.record(topic, sha256="x", vault_path=f"Obsidian/{i}.pdf")

    s = render_status(RunReport(), state, ok=True, courses=4,
                      when=datetime(2026, 9, 1, 8, 0))

    assert s["files_tracked"] == 3


def test_a_failed_auth_is_flagged_for_the_dashboard():
    s = render_status(RunReport(), State.empty(), ok=False, courses=0,
                      when=datetime(2026, 9, 1, 8, 0), needs_reauth=True)

    assert s["ok"] is False
    assert s["needs_reauth"] is True


def test_warnings_are_carried_through():
    report = RunReport(warnings=["unknown course 34871"])

    s = render_status(report, State.empty(), ok=True, courses=4,
                      when=datetime(2026, 9, 1, 8, 0))

    assert s["warnings"] == ["unknown course 34871"]


def test_status_is_written_as_json(tmp_path):
    path = tmp_path / "status" / "status.json"

    write_status(path, {"ok": True, "files_tracked": 30})

    assert json.loads(path.read_text(encoding="utf-8"))["files_tracked"] == 30


def test_writing_status_creates_its_directory(tmp_path):
    path = tmp_path / "deep" / "nested" / "status.json"

    write_status(path, {"ok": True})

    assert path.exists()
