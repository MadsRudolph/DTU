#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List (and optionally remove) files on Drive that the manifest no longer references.

Renaming or moving a folder rewrites the manifest paths but leaves the old copies
sitting on Drive forever. Archiving the 4th semester in e17681f moved 548 paths
under Obsidian/Archive/, and the pre-move copies are still up there.

Safe by default: prints what it would remove and exits. `--apply` moves them to the
Google Drive trash (recoverable for 30 days), never a permanent delete.

Usage:
    python prune-drive-orphans.py            # report only
    python prune-drive-orphans.py --apply    # move orphans to Drive trash
"""

import os
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONUTF8", "1")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import subprocess  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import DRIVE_FOLDER_ID  # noqa: E402
from upload import RCLONE, _canon, get_drive_file_ids, get_manifest_paths, get_repo_root, load_manifest  # noqa: E402


def main() -> int:
    apply = "--apply" in sys.argv

    if not RCLONE:
        print("Error: rclone not found.")
        return 1

    repo_root = get_repo_root()
    manifest_paths = get_manifest_paths(load_manifest(repo_root))

    print("Listing Drive...")
    drive_map = get_drive_file_ids(repo_root)
    print(f"  {len(drive_map)} files on Drive, {len(manifest_paths)} in manifest\n")

    orphans = {k: v for k, v in drive_map.items() if k not in manifest_paths}
    if not orphans:
        print("No orphans: every file on Drive is referenced by the manifest.")
        return 0

    total = sum(e["size"] for e in orphans.values())
    print(f"{len(orphans)} orphaned file(s), {total / (1024*1024):.1f} MB\n")

    by_area = Counter(
        "/".join(e["original_path"].split("/")[:3]) for e in orphans.values()
    )
    for area, count in by_area.most_common():
        print(f"  {count:>4}  {area}")

    if not apply:
        print("\n(report only -- pass --apply to move these to the Drive trash)")
        return 0

    # One rclone invocation for the whole batch, not one per file. Per-file calls
    # each pay a fresh OAuth handshake and Google throttles the burst -- a single
    # delete was taking well over a minute under backoff.
    listing = Path(__file__).resolve().parent / ".prune-list.txt"
    listing.write_text(
        "\n".join(e["original_path"] for e in orphans.values()) + "\n",
        encoding="utf-8",
    )

    print("\nMoving to Drive trash...")
    try:
        result = subprocess.run(
            [RCLONE, "delete", "gdrive:",
             "--files-from", str(listing),
             "--drive-root-folder-id", DRIVE_FOLDER_ID,
             # Explicit, not relying on the backend default: these go to the
             # Google Drive trash and stay recoverable for 30 days. This tool
             # must never hard-delete.
             "--drive-use-trash=true",
             # Stay under Drive's per-second quota instead of being throttled.
             "--tpslimit", "8",
             "--checkers", "4",
             "--stats", "10s",
             "--stats-one-line",
             "-v"],
            text=True,
            encoding="utf-8",
        )
    finally:
        listing.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"\nrclone exited {result.returncode} -- re-run to retry what is left.")
        return 1

    print(f"\nDone. {len(orphans)} file(s) moved to the Drive trash.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
