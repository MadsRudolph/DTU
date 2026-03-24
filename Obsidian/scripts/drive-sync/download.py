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
import unicodedata
from pathlib import Path

from config import DRIVE_FOLDER_ID

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


def download_rclone(rel_path: str, dest_path: Path) -> bool:
    """Download a file using rclone (authenticated)."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        RCLONE, "copyto",
        f"gdrive:{rel_path}",
        str(dest_path),
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0 and dest_path.exists()


def download_gdown(drive_id: str, dest_path: Path) -> bool:
    """Download a file using gdown (requires public sharing)."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"https://drive.google.com/uc?id={drive_id}"
    output = gdown.download(url, str(dest_path), quiet=True)
    return output is not None


def download_file(rel_path: str, drive_id: str, dest_path: Path, expected_size: int = None) -> bool:
    """Download a file, trying rclone first, then gdown."""
    try:
        print(f"  Downloading: {dest_path.name}...", end=" ", flush=True)

        ok = False
        if RCLONE:
            ok = download_rclone(rel_path, dest_path)

        if not ok and HAS_GDOWN:
            ok = download_gdown(drive_id, dest_path)

        if not ok:
            print("FAILED")
            return False

        # Verify size if provided
        if expected_size and dest_path.exists():
            actual_size = dest_path.stat().st_size
            if actual_size != expected_size:
                print(f"WARNING (size mismatch: expected {expected_size}, got {actual_size})")
                return True

        print("OK")
        return True

    except Exception as e:
        print(f"FAILED ({e})")
        return False


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

    downloaded = 0
    skipped = 0
    failed = 0

    for entry in files:
        rel_path = entry["path"]
        drive_id = entry["driveId"]
        expected_size = entry.get("size")

        # Try both Unicode normalization forms (handles ø, æ, å etc. across platforms)
        dest_path_nfc = repo_root / unicodedata.normalize("NFC", rel_path)
        dest_path_nfd = repo_root / unicodedata.normalize("NFD", rel_path)

        # Use whichever path exists, prefer NFC
        if dest_path_nfc.exists():
            dest_path = dest_path_nfc
        elif dest_path_nfd.exists():
            dest_path = dest_path_nfd
        else:
            dest_path = dest_path_nfc  # Default for download

        # Check if file already exists
        if dest_path.exists() and not args.force:
            if args.verify and expected_size:
                actual_size = dest_path.stat().st_size
                if actual_size != expected_size:
                    print(f"  Size mismatch: {rel_path} (expected {expected_size}, got {actual_size})")
                    failed += 1
                else:
                    skipped += 1
            else:
                skipped += 1
            continue

        if args.dry_run:
            print(f"  Would download: {rel_path}")
            continue

        if download_file(rel_path, drive_id, dest_path, expected_size):
            downloaded += 1
        else:
            failed += 1

    print()
    print(f"Summary: {downloaded} downloaded, {skipped} skipped, {failed} failed")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
