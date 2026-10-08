"""The download-and-file loop.

Holds the rules the vault depends on: nothing is fetched twice, nothing is
silently overwritten, and a failed download leaves no trace in state so the next
run retries it.
"""

from __future__ import annotations

import hashlib
import io
import logging
import zipfile
from pathlib import Path, PurePosixPath

from .filing import Rules, resolve_collision
from .models import Course, RunReport, Topic
from .state import State

log = logging.getLogger(__name__)

ZIP_MAGIC = b"PK\x03\x04"


def unwrap_zip(filename: str, payload: bytes) -> bytes:
    """Return the real file when Brightspace serves it zipped under its own name.

    Seen in October 2026: every 34870 lecture recording arrived as a ZIP holding
    one `Lecture N/<name>.mp4`, saved verbatim as `<name>.mp4`, so no player
    could open it. Only a single member with the same extension is unwrapped;
    anything else (a real .zip, or an archive with several files) is kept as is.
    """
    if filename.lower().endswith(".zip") or not payload.startswith(ZIP_MAGIC):
        return payload
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            members = [m for m in archive.infolist() if not m.is_dir()]
            if len(members) != 1:
                return payload
            if PurePosixPath(members[0].filename).suffix.lower() != PurePosixPath(filename).suffix.lower():
                return payload
            log.info("unwrapped %s from a zip served under its own name", filename)
            return archive.read(members[0])
    except zipfile.BadZipFile:
        return payload


class Sync:
    def __init__(
        self,
        rules: Rules,
        state: State,
        repo_root: Path,
        download,
        dry_run: bool = False,
    ) -> None:
        self.rules = rules
        self.state = state
        self.repo_root = Path(repo_root)
        self._download = download
        self.dry_run = dry_run
        self.report = RunReport()
        # Paths claimed during this run, so two topics cannot collide silently.
        self._claimed: set[PurePosixPath] = {
            PurePosixPath(p) for p in state.known_vault_paths()
        }

    def process(self, course: Course, topics: list[Topic]) -> None:
        """Download and file everything new in one course."""
        if not self.rules.is_known(course.code):
            self.report.warnings.append(
                f"unknown course {course.code} ({course.name}) — "
                f"filed under _Learn/, add rules for it"
            )

        for topic in topics:
            if not self.state.needs_download(topic):
                continue
            self._handle(course, topic)

    def _handle(self, course: Course, topic: Topic) -> None:
        target = self.rules.path_for(topic, course)

        if self.dry_run:
            self.report.files_added.append((course.code, str(target)))
            return

        try:
            payload = self._download(topic.download_url)
        except Exception as exc:
            self.report.warnings.append(
                f"could not download {topic.filename} for {course.code}: {exc}"
            )
            log.warning("download failed for topic %s", topic.topic_id, exc_info=True)
            return

        payload = unwrap_zip(topic.filename, payload)
        digest = hashlib.sha256(payload).hexdigest()

        # Same bytes under a new revision: record the revision, leave the file alone.
        if self.state.content_unchanged(topic, digest):
            existing = self.state.vault_path_for(topic.topic_id) or str(target)
            self.state.record(topic, sha256=digest, vault_path=existing)
            return

        resolved = resolve_collision(target, self._claimed)
        destination = self.repo_root / resolved

        # The vault may already hold this file from a manual download. Adopting it
        # keeps the first run from rewriting material that is already correct, and
        # from reporting thirty "new" files that were there all along.
        if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() == digest:
            self._claimed.add(resolved)
            self.state.record(topic, sha256=digest, vault_path=str(resolved))
            self.report.files_adopted.append((course.code, str(resolved)))
            return

        if resolved != target:
            self.report.warnings.append(
                f"filename collision for {course.code}: {topic.filename} "
                f"saved as {resolved.name}"
            )

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)

        self._claimed.add(resolved)
        self.state.record(topic, sha256=digest, vault_path=str(resolved))
        self.report.files_added.append((course.code, str(resolved)))
