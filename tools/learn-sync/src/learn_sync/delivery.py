"""Get the run's output onto GitHub and into Google Drive.

Order matters: binaries go to Drive first, because the manifest that drive-sync
rebuilds is what actually travels in git. Committing before the upload would
publish a manifest describing files nobody else can fetch.

The invariant this module exists to protect: no partial state is ever committed.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

MANIFEST = "Obsidian/scripts/drive-sync/manifest.json"


class DeliveryFailed(RuntimeError):
    """Something went wrong between the working tree and origin."""


class DriveSyncFailed(DeliveryFailed):
    """The Drive upload failed, so the manifest cannot be trusted."""


def _join(names) -> str:
    """Human list: 'a', 'a and b', 'a, b and c'."""
    names = list(names)
    if len(names) <= 1:
        return "".join(names)
    return f"{', '.join(names[:-1])} and {names[-1]}"


def commit_message(report) -> str:
    """Build a message that reads like a developer wrote it.

    Repo convention forbids any mention of Claude, AI or automation, so this
    describes the content and nothing else.
    """
    subjects = []
    if report.files_added:
        subjects.append("material")
    if report.announcements:
        subjects.append("announcements")
    if report.events:
        subjects.append("deadlines")

    codes: list[str] = []
    for code, _ in report.files_added:
        if code not in codes:
            codes.append(code)
    for item in (*report.announcements, *report.events):
        if item.course_code not in codes:
            codes.append(item.course_code)

    # A run can change nothing but the state file; it still commits, and
    # "Update  for " is not a commit message.
    if not subjects or not codes:
        return "Update sync state"

    verb = "Add" if (report.files_added or report.announcements) else "Update"
    return f"{verb} {_join(subjects)} for {_join(codes)}"


class Delivery:
    def __init__(self, repo: Path, drive_sync) -> None:
        self.repo = Path(repo)
        self._drive_sync = drive_sync

    def _git(self, *args: str, check: bool = True) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            capture_output=True,
            text=True,
        )
        if check and result.returncode != 0:
            raise DeliveryFailed(f"git {' '.join(args)} failed: {result.stderr.strip()}")
        return result.stdout.strip()

    def pull(self) -> None:
        """Start the run from remote HEAD.

        --autostash because a run that died after writing notes but before
        committing leaves the tree dirty, and a plain rebase refuses to start on
        a dirty tree -- which would wedge every subsequent run, not just that one.
        """
        self._git("pull", "--rebase", "--autostash")

    def publish(self, report, paths) -> bool:
        """Upload binaries, commit the given paths, push. Returns whether it committed.

        `paths` are the tracked text files this run touched -- notes, the state
        file, the manifest. Binaries are gitignored and travel via Drive, and
        nothing outside `paths` is ever staged.
        """
        # The upload comes first, before any "did anything change" check. State can
        # record a topic as synced while Drive never received it -- an aborted run
        # leaves exactly that -- and the run that has to repair it is precisely the
        # one where nothing else changed. upload.py --sync is idempotent: with
        # nothing new it lists Drive and exits.
        paths = [str(p) for p in paths] + [MANIFEST]
        self._drive_sync()

        if not self._pending(paths):
            return False

        # git add aborts on a pathspec that matches nothing, and the manifest may
        # legitimately be absent on a first run, so stage only what is really there.
        present = [p for p in paths if (self.repo / p).exists()]
        if not present:
            return False

        self._git("add", "--", *present)
        if not self._git("diff", "--cached", "--name-only"):
            return False

        self._git("commit", "-m", commit_message(report))
        self._push()
        return True

    def _pending(self, paths) -> bool:
        """True when any of `paths` differs from HEAD."""
        existing = [p for p in paths if (self.repo / p).exists()]
        if not existing:
            return False
        return bool(self._git("status", "--porcelain", "--", *existing))

    def _push(self) -> None:
        result = subprocess.run(
            ["git", "push"], cwd=self.repo, capture_output=True, text=True
        )
        if result.returncode == 0:
            return

        # Someone else pushed between our pull and our commit. Rebase once.
        self._git("pull", "--rebase")
        retry = subprocess.run(
            ["git", "push"], cwd=self.repo, capture_output=True, text=True
        )
        if retry.returncode != 0:
            raise DeliveryFailed(
                f"push rejected twice, commit left local: {retry.stderr.strip()}"
            )
