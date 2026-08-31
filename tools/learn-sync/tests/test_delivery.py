import subprocess

import pytest

from learn_sync.delivery import Delivery, DriveSyncFailed, commit_message
from learn_sync.models import Announcement, Event, RunReport
from datetime import datetime


# --- commit message -----------------------------------------------------------


def report(files=(), announcements=(), events=()) -> RunReport:
    return RunReport(
        files_added=list(files),
        announcements=list(announcements),
        events=list(events),
    )


def announcement(code="34870") -> Announcement:
    return Announcement("1", code, datetime(2026, 9, 1), "t", "b")


def event(code="34870") -> Event:
    return Event("1", code, "Lab A", datetime(2026, 9, 12))


def test_commit_message_names_material_and_course():
    msg = commit_message(report(files=[("34870", "a.pdf")]))

    assert msg == "Add material for 34870"


def test_commit_message_joins_several_courses():
    msg = commit_message(
        report(files=[("34870", "a.pdf"), ("62755", "b.pdf"), ("34840", "c.pdf")])
    )

    assert msg == "Add material for 34870, 62755 and 34840"


def test_commit_message_combines_subjects():
    msg = commit_message(
        report(files=[("34870", "a.pdf")], announcements=[announcement("62755")])
    )

    assert msg == "Add material and announcements for 34870 and 62755"


def test_commit_message_for_deadlines_only_uses_update():
    msg = commit_message(report(events=[event()]))

    assert msg == "Update deadlines for 34870"


@pytest.mark.parametrize("banned", ["Claude", "AI", "Co-Authored-By", "🤖", "automat"])
def test_commit_message_never_mentions_automation(banned):
    """Repo convention: commit messages read like a developer wrote them."""
    msg = commit_message(
        report(
            files=[("34870", "a.pdf")],
            announcements=[announcement()],
            events=[event()],
        )
    )

    assert banned.lower() not in msg.lower()


# --- git integration ----------------------------------------------------------


def git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture
def repo(tmp_path):
    """A working clone with a bare origin, so push is exercised for real."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "--bare", "-b", "main", str(origin)], check=True,
                   capture_output=True)

    work = tmp_path / "work"
    subprocess.run(["git", "clone", str(origin), str(work)], check=True, capture_output=True)
    git(work, "config", "user.email", "test@example.com")
    git(work, "config", "user.name", "Test")

    (work / "seed.md").write_text("seed\n", encoding="utf-8")
    git(work, "add", "seed.md")
    git(work, "commit", "-m", "seed")
    git(work, "push", "-u", "origin", "main")
    return work


def test_publish_commits_and_pushes_changed_files(repo):
    delivery = Delivery(repo, drive_sync=lambda: None)
    (repo / "note.md").write_text("hello\n", encoding="utf-8")

    committed = delivery.publish(report(files=[("34870", "a.pdf")]), ["note.md"])

    assert committed is True
    assert git(repo, "log", "-1", "--pretty=%s") == "Add material for 34870"
    assert git(repo, "status", "--porcelain") == ""
    # The commit reached origin, not just the local branch.
    assert git(repo, "rev-parse", "HEAD") == git(repo, "rev-parse", "origin/main")


def test_publish_makes_no_commit_when_nothing_changed(repo):
    delivery = Delivery(repo, drive_sync=lambda: None)
    before = git(repo, "rev-parse", "HEAD")

    committed = delivery.publish(report(files=[("34870", "a.pdf")]), ["seed.md"])

    assert committed is False
    assert git(repo, "rev-parse", "HEAD") == before


def test_drive_sync_runs_before_the_commit(repo):
    calls = []

    def drive_sync():
        # If the commit had already happened, status would be clean here.
        calls.append(git(repo, "status", "--porcelain"))

    delivery = Delivery(repo, drive_sync=drive_sync)
    (repo / "note.md").write_text("hello\n", encoding="utf-8")

    delivery.publish(report(files=[("34870", "a.pdf")]), ["note.md"])

    assert len(calls) == 1
    assert "note.md" in calls[0]


def test_drive_sync_runs_even_when_this_run_downloaded_nothing(repo):
    """Self-healing: state can say "synced" while Drive never got the file.

    Gating the upload on what this run touched made such a gap permanent --
    thirty PDFs once sat on disk, recorded in state, absent from Drive, and no
    future run could notice. upload.py --sync is idempotent, so just run it.
    """
    calls = []
    delivery = Delivery(repo, drive_sync=lambda: calls.append(1))
    (repo / "note.md").write_text("hello\n", encoding="utf-8")

    delivery.publish(report(announcements=[announcement()]), ["note.md"])

    assert calls == [1]


def test_drive_sync_failure_aborts_before_committing(repo):
    def boom():
        raise DriveSyncFailed("rclone exploded")

    delivery = Delivery(repo, drive_sync=boom)
    (repo / "note.md").write_text("hello\n", encoding="utf-8")
    before = git(repo, "rev-parse", "HEAD")

    with pytest.raises(DriveSyncFailed):
        delivery.publish(report(files=[("34870", "a.pdf")]), ["note.md"])

    assert git(repo, "rev-parse", "HEAD") == before
    # The working tree is left dirty on purpose, so the failure is inspectable.
    assert "note.md" in git(repo, "status", "--porcelain")


def test_publish_rebases_onto_remote_work_pushed_meanwhile(repo, tmp_path):
    """Another machine committed since our last pull; we must not clobber it."""
    other = tmp_path / "other"
    subprocess.run(["git", "clone", str(tmp_path / "origin.git"), str(other)],
                   check=True, capture_output=True)
    git(other, "config", "user.email", "other@example.com")
    git(other, "config", "user.name", "Other")
    (other / "theirs.md").write_text("theirs\n", encoding="utf-8")
    git(other, "add", "theirs.md")
    git(other, "commit", "-m", "their work")
    git(other, "push")

    delivery = Delivery(repo, drive_sync=lambda: None)
    (repo / "note.md").write_text("hello\n", encoding="utf-8")

    assert delivery.publish(report(files=[("34870", "a.pdf")]), ["note.md"]) is True
    assert (repo / "theirs.md").exists()
    assert git(repo, "rev-parse", "HEAD") == git(repo, "rev-parse", "origin/main")


def test_publish_does_not_stage_unrelated_dirty_files(repo):
    """Only the paths we were handed may enter the commit."""
    delivery = Delivery(repo, drive_sync=lambda: None)
    (repo / "note.md").write_text("hello\n", encoding="utf-8")
    (repo / "unrelated.md").write_text("do not commit me\n", encoding="utf-8")

    delivery.publish(report(files=[("34870", "a.pdf")]), ["note.md"])

    assert "unrelated.md" in git(repo, "status", "--porcelain")
    assert "unrelated.md" not in git(repo, "show", "--name-only", "--pretty=", "HEAD")


def test_commit_message_for_an_empty_report_is_still_readable():
    """State-only runs still commit; the message must not read 'Update  for'."""
    msg = commit_message(report())

    assert msg == "Update sync state"
    assert "  " not in msg
    assert not msg.endswith("for")


def test_drive_sync_runs_when_files_were_only_adopted(repo):
    """Adopted files are on disk but may never have reached Drive."""
    calls = []
    delivery = Delivery(repo, drive_sync=lambda: calls.append(1))
    (repo / "note.md").write_text("hello\n", encoding="utf-8")
    r = report()
    r.files_adopted = [("34870", "a.pdf")]

    delivery.publish(r, ["note.md"])

    assert calls == [1]
