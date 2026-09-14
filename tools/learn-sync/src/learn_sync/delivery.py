"""Get the run's output onto GitHub.

Notes, announcements, deadlines and the state file travel in git from here.
The binaries do not: they are gitignored, and a Syncthing agent on this
container replicates them to the two PCs and the always-on node directly.

That used to be a Google Drive round trip -- upload here, rebuild a manifest,
commit the manifest, have the PCs read it back and pull each file by ID. Drive
is now only an offsite backup, written by the server, and nothing in the
delivery path depends on it.

The invariant this module exists to protect: no partial state is ever committed.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

_COLLISION = "untracked working tree files would be overwritten"


def _collided_paths(message: str) -> list[str]:
    """The paths git lists when untracked files block a merge.

    git prints them one per line, tab-indented, between the `error:` line and
    "Please move or remove them". Keying on the tab is what keeps the fetch
    summary ("db6684a..edf4129  main -> origin/main") out of the result.
    """
    if _COLLISION not in message:
        return []
    paths, listing = [], False
    for line in message.splitlines():
        if _COLLISION in line:
            listing = True
            continue
        if not listing:
            continue
        if not line.startswith("\t"):
            break
        paths.append(line.strip())
    return paths


class DeliveryFailed(RuntimeError):
    """Something went wrong between the working tree and origin."""


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
    def __init__(self, repo: Path) -> None:
        self.repo = Path(repo)

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

        --autostash does NOT cover untracked files, though, and that gap wedged
        the service for five days in September 2026: a run downloaded two photos,
        failed before committing them, and the same two photos then arrived in
        somebody else's commit. From then on every pull aborted with "untracked
        working tree files would be overwritten", identically, every three hours.
        Nothing upstream of here can clear that -- so clear it here.
        """
        try:
            self._git("pull", "--rebase", "--autostash")
            return
        except DeliveryFailed as failure:
            blocked = _collided_paths(str(failure))
            if not blocked:
                raise
            self._clear_collisions(blocked)

        self._git("pull", "--rebase", "--autostash")

    def _clear_collisions(self, paths) -> None:
        """Get untracked files out of the way of an incoming commit.

        Identical content is simply dropped -- that is the common case, because
        the file we downloaded and the file being pulled came from the same place
        upstream. Anything that genuinely differs is kept under a `.local` name
        rather than deleted; a wedged sync is worth fixing automatically, losing
        a file nobody has a second copy of is not.
        """
        for rel in paths:
            target = self.repo / rel
            if not target.exists():
                continue
            if self._matches_upstream(rel):
                target.unlink()
                continue
            spare = target.with_name(target.name + ".local")
            count = 2
            while spare.exists():
                spare = target.with_name(f"{target.name}.local{count}")
                count += 1
            target.rename(spare)

    def _matches_upstream(self, rel: str) -> bool:
        """True when the working-tree file is byte-identical to the incoming one.

        Compares git's own blob hashes, so it costs nothing and cannot be fooled
        by a differing mtime. The failed pull already fetched, so `@{u}` is the
        commit we are about to land on.
        """
        local = self._git("hash-object", "--", str(self.repo / rel), check=False)
        upstream = self._git("rev-parse", f"@{{u}}:{rel}", check=False)
        return bool(local) and local == upstream

    def publish(self, report, paths) -> bool:
        """Commit the given paths and push. Returns whether it committed.

        `paths` are the tracked files this run touched -- notes, the state
        file, plus any tool files a rule routed outside the vault (see
        cmd_sync). Vault binaries are gitignored and reach the other machines
        through Syncthing; nothing outside `paths` is ever staged.
        """
        paths = [str(p) for p in paths]

        if not self._pending(paths):
            return False

        # git add aborts on a pathspec that matches nothing, and a note named in
        # `paths` can be absent on a first run, so stage only what is really there.
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
