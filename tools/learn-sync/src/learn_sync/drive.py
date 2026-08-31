"""Additive Google Drive upload for the files this run downloaded.

Deliberately NOT drive-sync's own `upload.py --sync`. That path calls
`rebuild_manifest()` after a successful upload, which reconstructs the manifest
from whatever binaries are present on local disk. On a full checkout that is the
intended behaviour -- it prunes deleted files. On the container it is
destructive: the clone holds only the binaries learn-sync itself downloaded, so
a rebuild would truncate an 816-entry manifest to ~30 and push the result,
leaving every other machine unable to fetch the rest.

So this uploader only ever appends. It never removes or rewrites an entry, and
it never consults the filesystem for anything except the files it was handed.
"""

from __future__ import annotations

import json
import logging
import subprocess
import unicodedata
from pathlib import Path

from .delivery import DriveSyncFailed

log = logging.getLogger(__name__)

MANIFEST_PATH = "Obsidian/scripts/drive-sync/manifest.json"
REMOTE = "gdrive:"


def _canon(path: str) -> str:
    """Match drive-sync's own canonical key: NFC, lowercased, mojibake repaired."""
    s = path
    if "Ã" in s or "Â" in s:
        try:
            s = s.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return unicodedata.normalize("NFC", s).lower()


def folder_id_from_manifest(repo_root: Path) -> str:
    """The Drive folder the vault lives in, taken from the manifest itself.

    Reading it here rather than importing drive-sync's config.py keeps this
    module standalone inside the container image.
    """
    manifest = json.loads(
        (Path(repo_root) / MANIFEST_PATH).read_text(encoding="utf-8")
    )
    return manifest["drive_folder_id"]


class Rclone:
    """The real rclone CLI. Output is decoded as UTF-8 explicitly -- without that,
    Windows decodes with the locale codepage and every ø/æ/å path silently
    mismatches."""

    def __init__(self, folder_id: str, binary: str = "rclone") -> None:
        self._folder_id = folder_id
        self._binary = binary

    def _run(self, *args: str) -> str:
        result = subprocess.run(
            [self._binary, *args, "--drive-root-folder-id", self._folder_id],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            raise DriveSyncFailed(f"rclone {args[0]} failed: {result.stderr.strip()}")
        return result.stdout

    def copy(self, local: Path, remote_dir: str) -> None:
        self._run("copy", str(local), f"{REMOTE}{remote_dir}")

    def file_ids(self, rel_paths) -> dict[str, str]:
        """Drive ids for a batch, in a single listing.

        One lsjson per file meant 30 uploads took nine minutes: every rclone
        invocation pays the full auth and connection cost. One recursive listing
        covers the whole batch.
        """
        rel_paths = list(rel_paths)
        if not rel_paths:
            return {}

        out = self._run("lsjson", "-R", "--files-only", REMOTE)
        try:
            entries = json.loads(out)
        except json.JSONDecodeError as exc:
            raise DriveSyncFailed(f"could not list Drive: {exc}")

        by_key = {_canon(e["Path"]): e["ID"] for e in entries}
        ids = {}
        for rel in rel_paths:
            drive_id = by_key.get(_canon(rel))
            if drive_id is None:
                raise DriveSyncFailed(f"uploaded {rel} but Drive did not list it")
            ids[rel] = drive_id
        return ids


class DriveUploader:
    def __init__(self, repo_root: Path, rclone) -> None:
        self.repo_root = Path(repo_root)
        self._rclone = rclone
        self._manifest_file = self.repo_root / MANIFEST_PATH

    def upload(self, rel_paths) -> list[str]:
        """Upload any of `rel_paths` Drive does not already have, and record them.

        Returns the paths actually uploaded. Raises DriveSyncFailed on the first
        failure, leaving the manifest untouched so a partial upload is never
        described as complete.
        """
        manifest = json.loads(self._manifest_file.read_text(encoding="utf-8"))
        known = {_canon(e["path"]) for e in manifest.get("files", [])}

        pending = []
        for rel in rel_paths:
            rel = str(rel).replace("\\", "/")
            if _canon(rel) in known:
                continue
            local = self.repo_root / rel
            if not local.exists():
                log.warning("skipping %s: not on disk", rel)
                continue
            pending.append((rel, local))

        if not pending:
            return []

        for rel, local in pending:
            remote_dir = rel.rsplit("/", 1)[0] if "/" in rel else ""
            self._rclone.copy(local, remote_dir)

        # One listing for the whole batch, after every transfer has landed.
        ids = self._rclone.file_ids([rel for rel, _ in pending])
        added = [
            {"path": rel, "driveId": ids[rel], "size": local.stat().st_size}
            for rel, local in pending
        ]

        # Only now, once every transfer succeeded, is the manifest rewritten.
        manifest["files"] = sorted(
            manifest.get("files", []) + added, key=lambda e: e["path"]
        )
        self._manifest_file.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        log.info("uploaded %d file(s) to Drive", len(added))
        return [e["path"] for e in added]
