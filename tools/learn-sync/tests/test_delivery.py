import subprocess

import pytest

from learn_sync.delivery import (
    Delivery,
    DeliveryFailed,
    _collided_paths,
    commit_message,
)
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
    delivery = Delivery(repo)
    (repo / "note.md").write_text("hello\n", encoding="utf-8")

    committed = delivery.publish(report(files=[("34870", "a.pdf")]), ["note.md"])

    assert committed is True
    assert git(repo, "log", "-1", "--pretty=%s") == "Add material for 34870"
    assert git(repo, "status", "--porcelain") == ""
    # The commit reached origin, not just the local branch.
    assert git(repo, "rev-parse", "HEAD") == git(repo, "rev-parse", "origin/main")


def test_publish_makes_no_commit_when_nothing_changed(repo):
    delivery = Delivery(repo)
    before = git(repo, "rev-parse", "HEAD")

    committed = delivery.publish(report(files=[("34870", "a.pdf")]), ["seed.md"])

    assert committed is False
    assert git(repo, "rev-parse", "HEAD") == before


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

    delivery = Delivery(repo)
    (repo / "note.md").write_text("hello\n", encoding="utf-8")

    assert delivery.publish(report(files=[("34870", "a.pdf")]), ["note.md"]) is True
    assert (repo / "theirs.md").exists()
    assert git(repo, "rev-parse", "HEAD") == git(repo, "rev-parse", "origin/main")


def test_publish_does_not_stage_unrelated_dirty_files(repo):
    """Only the paths we were handed may enter the commit."""
    delivery = Delivery(repo)
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


def test_pull_survives_a_dirty_tree_left_by_an_aborted_run(repo, tmp_path):
    """A run that dies after writing notes but before committing leaves the tree
    dirty. Without autostash the next pull aborts, and every run after it too."""
    other = tmp_path / "other2"
    subprocess.run(["git", "clone", str(tmp_path / "origin.git"), str(other)],
                   check=True, capture_output=True)
    git(other, "config", "user.email", "other@example.com")
    git(other, "config", "user.name", "Other")
    (other / "remote.md").write_text("remote work\n", encoding="utf-8")
    git(other, "add", "remote.md")
    git(other, "commit", "-m", "remote work")
    git(other, "push")

    # Our tree still has an uncommitted change to a tracked file.
    (repo / "seed.md").write_text("half-finished work\n", encoding="utf-8")

    Delivery(repo).pull()

    assert (repo / "remote.md").exists(), "remote commit was not pulled"
    assert (repo / "seed.md").read_text(encoding="utf-8") == "half-finished work\n"


# --- untracked collisions -----------------------------------------------------


def _push_file_from_elsewhere(tmp_path, name, body, clone="collide"):
    """Land `name` in origin from another clone, the way a second machine would."""
    other = tmp_path / clone
    subprocess.run(["git", "clone", str(tmp_path / "origin.git"), str(other)],
                   check=True, capture_output=True)
    git(other, "config", "user.email", "other@example.com")
    git(other, "config", "user.name", "Other")
    target = other / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    git(other, "add", name)
    git(other, "commit", "-m", f"add {name}")
    git(other, "push")


def test_collided_paths_reads_the_file_list_git_prints():
    message = (
        "git pull --rebase --autostash failed: From github.com:MadsRudolph/DTU\n"
        "   db6684a..edf4129  main       -> origin/main\n"
        "error: The following untracked working tree files would be "
        "overwritten by merge:\n"
        "\tObsidian/Courses/62755 Power Electronics/_Learn/a.jpg\n"
        "\tObsidian/Courses/62755 Power Electronics/_Learn/b.jpg\n"
        "Please move or remove them before you merge.\n"
        "Aborting"
    )

    assert _collided_paths(message) == [
        "Obsidian/Courses/62755 Power Electronics/_Learn/a.jpg",
        "Obsidian/Courses/62755 Power Electronics/_Learn/b.jpg",
    ]


def test_collided_paths_ignores_an_unrelated_failure():
    assert _collided_paths("git push failed: rejected, non-fast-forward") == []


def test_pull_drops_an_untracked_file_identical_to_the_incoming_one(repo, tmp_path):
    """The September 2026 wedge, reproduced.

    A run downloaded a photo and died before committing it; the same photo then
    arrived in someone else's commit. Identical bytes on both sides, so the local
    copy is redundant and the pull must simply proceed.
    """
    _push_file_from_elsewhere(tmp_path, "photo.jpg", "same bytes\n")
    (repo / "photo.jpg").write_text("same bytes\n", encoding="utf-8")

    Delivery(repo).pull()

    assert (repo / "photo.jpg").read_text(encoding="utf-8") == "same bytes\n"
    assert not list(repo.glob("photo.jpg.local*")), "identical file should be dropped"
    assert git(repo, "status", "--porcelain").strip() == ""


def test_pull_keeps_an_untracked_file_that_differs(repo, tmp_path):
    """Unwedging must never cost a file that exists nowhere else."""
    _push_file_from_elsewhere(tmp_path, "notes.pdf", "theirs\n")
    (repo / "notes.pdf").write_text("mine\n", encoding="utf-8")

    Delivery(repo).pull()

    assert (repo / "notes.pdf").read_text(encoding="utf-8") == "theirs\n"
    assert (repo / "notes.pdf.local").read_text(encoding="utf-8") == "mine\n"


def test_pull_clears_a_collision_in_a_subdirectory(repo, tmp_path):
    """Real collisions arrive at vault paths with spaces in them."""
    name = "Obsidian/Courses/62755 Power Electronics/_Learn/photo.jpg"
    _push_file_from_elsewhere(tmp_path, name, "same\n")
    local = repo / name
    local.parent.mkdir(parents=True, exist_ok=True)
    local.write_text("same\n", encoding="utf-8")

    Delivery(repo).pull()

    assert local.read_text(encoding="utf-8") == "same\n"
    assert git(repo, "status", "--porcelain").strip() == ""


def test_pull_still_raises_when_it_cannot_help(repo):
    """A failure that is not a collision must surface, not be swallowed."""
    git(repo, "remote", "set-url", "origin", str(repo / "does-not-exist.git"))

    with pytest.raises(DeliveryFailed):
        Delivery(repo).pull()
