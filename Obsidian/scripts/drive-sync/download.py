#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download large files from Google Drive based on manifest.

Usage:
    python download.py              # Download all missing files
    python download.py --verify     # Verify existing files match expected size
    python download.py --force      # Re-download all files even if they exist

Requirements:
    rclone (configured with 'gdrive' remote)
    OR pip install gdown requests (fallback, requires public sharing)
"""

# Enable UTF-8 mode on Windows for proper handling of Danish characters (ø, æ, å)
import os
import sys
if sys.platform == "win32":
    os.environ.setdefault("PYTHONUTF8", "1")
    # Reconfigure stdout/stderr for UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import argparse
import json
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path

from config import DRIVE_FOLDER_ID

# Number of concurrent rclone transfers/checkers for the batched download.
# rclone resolves the whole nested Drive path once per process, so a single
# batched `rclone copy --files-from` call is drastically faster than shelling
# out to a fresh rclone process per file (which re-resolves the path each time
# and ends up effectively serial: minutes per file on a large manifest).
RCLONE_TRANSFERS = 8
RCLONE_CHECKERS = 16


# Try to find rclone
def find_rclone() -> str | None:
    """Find rclone executable."""
    # Check PATH first
    rclone = shutil.which("rclone")
    if rclone:
        return rclone

    # Check known install locations on Windows
    known_paths = [
        Path.home() / "AppData/Local/Microsoft/WinGet/Packages",
    ]
    for base in known_paths:
        if base.exists():
            for match in base.rglob("rclone.exe"):
                return str(match)

    return None


RCLONE = find_rclone()

# gdown is optional fallback
try:
    import gdown
    HAS_GDOWN = True
except ImportError:
    HAS_GDOWN = False


def get_repo_root() -> Path:
    """Find the repository root (where .git is)."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find repository root")


def load_manifest(repo_root: Path) -> dict:
    """Load the manifest file."""
    manifest_path = repo_root / "Obsidian" / "scripts" / "drive-sync" / "manifest.json"
    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_dest_path(repo_root: Path, rel_path: str) -> Path:
    """Resolve the local destination path, preferring an already-existing
    NFC/NFD variant (handles ø, æ, å differences across platforms/filesystems)."""
    dest_path_nfc = repo_root / unicodedata.normalize("NFC", rel_path)
    dest_path_nfd = repo_root / unicodedata.normalize("NFD", rel_path)

    if dest_path_nfc.exists():
        return dest_path_nfc
    if dest_path_nfd.exists():
        return dest_path_nfd
    return dest_path_nfc  # Default for download


def download_batch_rclone(entries: list[dict], repo_root: Path) -> None:
    """Download many files in one rclone invocation via --files-from.

    A single process resolves the shared Drive folder tree once and transfers
    files with real concurrency, instead of one rclone process per file.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False, encoding="utf-8"
    ) as f:
        for entry in entries:
            f.write(entry["path"] + "\n")
        file_list_path = f.name

    try:
        cmd = [
            RCLONE, "copy",
            "gdrive:", str(repo_root),
            "--drive-root-folder-id", DRIVE_FOLDER_ID,
            "--files-from", file_list_path,
            "--transfers", str(RCLONE_TRANSFERS),
            "--checkers", str(RCLONE_CHECKERS),
            "--stats", "15s", "--stats-one-line", "-v",
        ]
        subprocess.run(cmd, encoding="utf-8")
    finally:
        os.unlink(file_list_path)


def download_gdown(drive_id: str, dest_path: Path) -> bool:
    """Download a file using gdown (requires public sharing)."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"https://drive.google.com/uc?id={drive_id}"
    output = gdown.download(url, str(dest_path), quiet=True)
    return output is not None


def main():
    parser = argparse.ArgumentParser(description="Download large files from Google Drive")
    parser.add_argument("--verify", action="store_true", help="Verify existing files")
    parser.add_argument("--force", action="store_true", help="Re-download all files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be downloaded")
    args = parser.parse_args()

    if not RCLONE and not HAS_GDOWN:
        print("Error: Neither rclone nor gdown available.")
        print("  Install rclone: winget install Rclone.Rclone")
        print("  Or install gdown: pip install gdown")
        sys.exit(1)

    repo_root = get_repo_root()
    manifest = load_manifest(repo_root)

    files = manifest.get("files", [])
    if not files:
        print("No files in manifest. Nothing to download.")
        return

    backend = "rclone" if RCLONE else "gdown"
    print(f"Found {len(files)} files in manifest (using {backend})")
    print(f"Repository root: {repo_root}")
    print()

    to_download = []
    skipped = 0
    failed = 0

    for entry in files:
        drive_id = entry["driveId"]

        # Skip files pending upload (null driveId)
        if drive_id is None:
            skipped += 1
            continue

        dest_path = resolve_dest_path(repo_root, entry["path"])

        if dest_path.exists() and not args.force:
            expected_size = entry.get("size")
            if args.verify and expected_size:
                actual_size = dest_path.stat().st_size
                if actual_size != expected_size:
                    print(f"  Size mismatch: {entry['path']} (expected {expected_size}, got {actual_size})")
                    failed += 1
                else:
                    skipped += 1
            else:
                skipped += 1
            continue

        to_download.append(entry)

    if args.dry_run:
        for entry in to_download:
            print(f"  Would download: {entry['path']}")
        print()
        print(f"Summary: {len(to_download)} would download, {skipped} skipped, {failed} failed")
        return

    if not to_download:
        print("Nothing to download.")
        print()
        print(f"Summary: 0 downloaded, {skipped} skipped, {failed} failed")
        if failed > 0:
            sys.exit(1)
        return

    print(f"Downloading {len(to_download)} file(s)...")
    print()

    downloaded = 0

    if RCLONE:
        download_batch_rclone(to_download, repo_root)
        print()

        for entry in to_download:
            dest_path = resolve_dest_path(repo_root, entry["path"])
            expected_size = entry.get("size")
            if not dest_path.exists():
                print(f"  FAILED: {entry['path']}")
                failed += 1
                continue
            if expected_size:
                actual_size = dest_path.stat().st_size
                if actual_size != expected_size:
                    print(f"  WARNING (size mismatch): {entry['path']} (expected {expected_size}, got {actual_size})")
            downloaded += 1
    else:
        # gdown fallback: one request per file (no batch API available).
        for entry in to_download:
            rel_path = entry["path"]
            drive_id = entry["driveId"]
            expected_size = entry.get("size")
            dest_path = resolve_dest_path(repo_root, rel_path)
            print(f"  Downloading: {dest_path.name}...", end=" ", flush=True)
            try:
                ok = download_gdown(drive_id, dest_path)
            except Exception as e:
                print(f"FAILED ({e})")
                failed += 1
                continue
            if not ok:
                print("FAILED")
                failed += 1
                continue
            if expected_size and dest_path.exists():
                actual_size = dest_path.stat().st_size
                if actual_size != expected_size:
                    print(f"WARNING (size mismatch: expected {expected_size}, got {actual_size})")
                    downloaded += 1
                    continue
            print("OK")
            downloaded += 1

    print()
    print(f"Summary: {downloaded} downloaded, {skipped} skipped, {failed} failed")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
