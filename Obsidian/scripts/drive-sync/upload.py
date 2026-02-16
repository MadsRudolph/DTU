#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upload large files to Google Drive and update the manifest.

Usage:
    python upload.py                  # Scan and prompt to upload new files
    python upload.py --scan           # Just scan, don't upload
    python upload.py --sync           # Upload all new files without prompting
    python upload.py --list           # List all files in manifest
    python upload.py --remove PATH    # Remove a file from manifest
    python upload.py --pull           # Find files on Drive not in manifest

Requirements:
    rclone (installed and configured with 'gdrive' remote)
"""

import json
import os
import subprocess
import sys
import unicodedata
from pathlib import Path

from config import LARGE_FILE_EXTENSIONS, MIN_FILE_SIZE_BYTES, DRIVE_FOLDER_ID

# rclone path
RCLONE = r"C:\Users\Mads2\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.73.0-windows-amd64\rclone.exe"


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
        return {"version": 1, "files": [], "drive_folder_id": DRIVE_FOLDER_ID}

    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(repo_root: Path, manifest: dict):
    """Save the manifest file."""
    manifest_path = repo_root / "Obsidian" / "scripts" / "drive-sync" / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def get_manifest_paths(manifest: dict) -> set:
    """Get all paths currently in the manifest (normalized for comparison)."""
    paths = set()
    for entry in manifest.get("files", []):
        path = entry["path"]
        paths.add(path)
        # Also add the mojibake form (UTF-8 bytes read as Latin-1) so files
        # on disk with garbled Danish chars (LÃ¸sning) match manifest (Løsning)
        try:
            paths.add(path.encode('utf-8').decode('latin-1'))
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass
        # And NFC/NFD forms
        paths.add(unicodedata.normalize("NFC", path))
        paths.add(unicodedata.normalize("NFD", path))
    return paths


def find_large_files(repo_root: Path, manifest_paths: set) -> list:
    """Find large files not in the manifest."""
    large_files = []

    for root, dirs, files in os.walk(repo_root):
        if ".git" in dirs:
            dirs.remove(".git")
        if ".venv" in dirs:
            dirs.remove(".venv")

        for filename in files:
            filepath = Path(root) / filename
            ext = filepath.suffix.lower()

            if ext not in LARGE_FILE_EXTENSIONS:
                continue

            rel_path = filepath.relative_to(repo_root).as_posix()

            if rel_path in manifest_paths:
                continue

            size = filepath.stat().st_size
            if size < MIN_FILE_SIZE_BYTES:
                continue

            large_files.append({
                "path": rel_path,
                "size": size,
                "size_mb": round(size / (1024 * 1024), 2)
            })

    return sorted(large_files, key=lambda x: x["path"])


def upload_file_to_drive(repo_root: Path, rel_path: str) -> bool:
    """Upload a single file to Google Drive using rclone."""
    local_path = repo_root / rel_path
    remote_dir = str(Path(rel_path).parent)

    cmd = [
        RCLONE, "copy",
        str(local_path),
        f"gdrive:/{remote_dir}/",
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return False

    # Set "Anyone with the link" sharing so gdown can download on other machines
    link_cmd = [
        RCLONE, "link",
        f"gdrive:{rel_path}",
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
    ]
    subprocess.run(link_cmd, capture_output=True, text=True)

    return True


def normalize_path_key(path: str) -> str:
    """Normalize a path for comparison, handling Danish characters (ø, æ, å)."""
    # Try NFC first, then NFD, use the one that gives a "cleaner" result
    nfc = unicodedata.normalize("NFC", path.lower())
    nfd = unicodedata.normalize("NFD", path.lower())

    # Use NFC as the canonical form (precomposed characters)
    return nfc


def get_drive_file_ids(repo_root: Path) -> dict:
    """Get all file IDs from Google Drive."""
    cmd = [
        RCLONE, "lsjson", "gdrive:/",
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
        "-R"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {}

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}

    drive_map = {}
    for item in data:
        if not item.get("IsDir", False):
            path = item["Path"]
            # Store under both NFC and NFD normalized keys for robust matching
            nfc_key = unicodedata.normalize("NFC", path.lower())
            nfd_key = unicodedata.normalize("NFD", path.lower())

            entry = {
                "driveId": item["ID"],
                "size": item["Size"],
                "original_path": path
            }
            drive_map[nfc_key] = entry
            if nfd_key != nfc_key:
                drive_map[nfd_key] = entry

    return drive_map


def rebuild_manifest(repo_root: Path) -> int:
    """Rebuild manifest from local files and Drive IDs."""
    print("Refreshing manifest from Google Drive...")
    drive_map = get_drive_file_ids(repo_root)

    extensions = LARGE_FILE_EXTENSIONS
    new_files = []
    seen_normalized = set()

    for root, dirs, files in os.walk(repo_root):
        if ".git" in dirs:
            dirs.remove(".git")
        if ".venv" in dirs:
            dirs.remove(".venv")

        for filename in files:
            ext = Path(filename).suffix.lower()
            if ext not in extensions:
                continue

            filepath = Path(root) / filename
            rel_path = filepath.relative_to(repo_root).as_posix()

            # Deduplicate: skip mojibake variants of already-seen paths
            nfc_key = unicodedata.normalize("NFC", rel_path.lower())
            if nfc_key in seen_normalized:
                continue
            seen_normalized.add(nfc_key)

            # Also mark the mojibake-decoded form as seen
            try:
                decoded = rel_path.encode('latin-1').decode('utf-8')
                seen_normalized.add(unicodedata.normalize("NFC", decoded.lower()))
            except (UnicodeDecodeError, UnicodeEncodeError):
                pass

            nfd_key = unicodedata.normalize("NFD", rel_path.lower())
            drive_entry = drive_map.get(nfc_key) or drive_map.get(nfd_key)

            if drive_entry:
                new_files.append({
                    "path": rel_path,
                    "driveId": drive_entry["driveId"],
                    "size": filepath.stat().st_size
                })

    manifest = {
        "version": 1,
        "description": "Large files stored in Google Drive. Run download.py to fetch them.",
        "drive_folder_id": DRIVE_FOLDER_ID,
        "files": sorted(new_files, key=lambda x: x["path"])
    }

    save_manifest(repo_root, manifest)
    return len(new_files)


def sync_files(repo_root: Path, manifest: dict, prompt: bool = True) -> int:
    """Upload new files to Drive and update manifest."""
    manifest_paths = get_manifest_paths(manifest)
    large_files = find_large_files(repo_root, manifest_paths)

    if not large_files:
        print("All large files are already in the manifest!")
        return 0

    total_size = sum(f["size"] for f in large_files)
    print(f"Found {len(large_files)} new files ({total_size / (1024*1024):.2f} MB):\n")

    for f in large_files:
        print(f"  {f['size_mb']:>8.2f} MB  {f['path']}")

    if prompt:
        print()
        response = input("Upload these files to Google Drive? [Y/n]: ").strip().lower()
        if response and response != 'y':
            print("Cancelled.")
            return 0

    print("\nUploading...")
    uploaded = 0

    for f in large_files:
        print(f"  {f['path']}...", end=" ", flush=True)
        if upload_file_to_drive(repo_root, f["path"]):
            print("OK")
            uploaded += 1
        else:
            print("FAILED")

    if uploaded > 0:
        count = rebuild_manifest(repo_root)
        print(f"\nDone. Manifest now has {count} files.")

    return uploaded


def remove_file(repo_root: Path, manifest: dict, rel_path: str):
    """Remove a file from the manifest."""
    files = manifest.get("files", [])
    original_count = len(files)

    manifest["files"] = [f for f in files if f["path"] != rel_path]

    if len(manifest["files"]) == original_count:
        print(f"File not found in manifest: {rel_path}")
        return

    save_manifest(repo_root, manifest)
    print(f"Removed from manifest: {rel_path}")


def list_files(manifest: dict):
    """List all files in manifest."""
    files = manifest.get("files", [])
    if not files:
        print("Manifest is empty")
    else:
        print(f"Files in manifest ({len(files)}):\n")
        for f in files:
            size_str = f"{f.get('size', 0) / (1024*1024):.2f} MB" if f.get('size') else "unknown"
            print(f"  {size_str:>10}  {f['path']}")


def pull_from_drive(repo_root: Path, manifest: dict) -> int:
    """Find files on Drive not in manifest and add them."""
    print("Checking Google Drive for new files...")
    drive_map = get_drive_file_ids(repo_root)

    # Build set of manifest paths (both normalizations)
    manifest_paths = set()
    for entry in manifest.get("files", []):
        path = entry["path"]
        manifest_paths.add(unicodedata.normalize("NFC", path.lower()))
        manifest_paths.add(unicodedata.normalize("NFD", path.lower()))

    # Find files on Drive not in manifest
    new_files = []
    seen_paths = set()

    for norm_key, entry in drive_map.items():
        if norm_key in manifest_paths:
            continue
        if norm_key in seen_paths:
            continue

        original_path = entry.get("original_path", "")

        # Skip .venv and other unwanted paths
        if ".venv" in original_path or "__pycache__" in original_path:
            continue

        # Check extension
        ext = Path(original_path).suffix.lower()
        if ext not in LARGE_FILE_EXTENSIONS:
            continue

        # Add BOTH NFC and NFD normalized keys to seen_paths to avoid duplicates
        nfc_key = unicodedata.normalize("NFC", original_path.lower())
        nfd_key = unicodedata.normalize("NFD", original_path.lower())
        seen_paths.add(nfc_key)
        seen_paths.add(nfd_key)

        new_files.append({
            "path": original_path,
            "driveId": entry["driveId"],
            "size": entry["size"]
        })

    if not new_files:
        print("No new files on Drive.")
        return 0

    print(f"Found {len(new_files)} files on Drive not in manifest:\n")
    for f in new_files:
        size_mb = f["size"] / (1024 * 1024)
        print(f"  {size_mb:>8.2f} MB  {f['path']}")

    print()
    response = input("Add these to manifest? [Y/n]: ").strip().lower()
    if response and response != 'y':
        print("Cancelled.")
        return 0

    # Add to manifest
    manifest["files"].extend(new_files)
    manifest["files"] = sorted(manifest["files"], key=lambda x: x["path"])
    save_manifest(repo_root, manifest)

    print(f"\nAdded {len(new_files)} files to manifest.")
    print("Run 'python download.py' to download them.")
    return len(new_files)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Upload large files to Google Drive")
    parser.add_argument("--scan", action="store_true", help="Scan for new files (don't upload)")
    parser.add_argument("--sync", action="store_true", help="Upload all new files without prompting")
    parser.add_argument("--list", action="store_true", help="List all files in manifest")
    parser.add_argument("--remove", metavar="PATH", help="Remove a file from manifest")
    parser.add_argument("--refresh", action="store_true", help="Refresh manifest from Drive")
    parser.add_argument("--pull", action="store_true", help="Find files on Drive not in manifest")
    args = parser.parse_args()

    repo_root = get_repo_root()
    manifest = load_manifest(repo_root)

    if args.scan:
        # Just show what needs uploading
        manifest_paths = get_manifest_paths(manifest)
        large_files = find_large_files(repo_root, manifest_paths)

        if not large_files:
            print("All large files are already in the manifest!")
        else:
            total_size = sum(f["size"] for f in large_files)
            print(f"Found {len(large_files)} new files ({total_size / (1024*1024):.2f} MB):\n")
            for f in large_files:
                print(f"  {f['size_mb']:>8.2f} MB  {f['path']}")
            print(f"\nRun without --scan to upload, or use --sync to upload without prompting.")

    elif args.sync:
        sync_files(repo_root, manifest, prompt=False)

    elif args.list:
        list_files(manifest)

    elif args.remove:
        remove_file(repo_root, manifest, args.remove)

    elif args.refresh:
        count = rebuild_manifest(repo_root)
        print(f"Manifest refreshed: {count} files")

    elif args.pull:
        pull_from_drive(repo_root, manifest)

    else:
        # Default: scan and prompt to upload
        sync_files(repo_root, manifest, prompt=True)


if __name__ == "__main__":
    main()
