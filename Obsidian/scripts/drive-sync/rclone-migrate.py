#!/usr/bin/env python3
"""
Migrate large files to Google Drive using rclone.

This script:
1. Finds all large files tracked by LFS
2. Uploads them to Google Drive (preserving folder structure)
3. Gets their Drive IDs
4. Updates the manifest
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# rclone path (update if different)
RCLONE = r"C:\Users\Mads2\AppData\Local\Microsoft\WinGet\Packages\Rclone.Rclone_Microsoft.Winget.Source_8wekyb3d8bbwe\rclone-v1.73.0-windows-amd64\rclone.exe"

# Remote name and folder
REMOTE = "gdrive"
DRIVE_FOLDER_ID = "1s3--pi4tpEAhW9sO9cfLh8orU0mCgiK-"

from config import LARGE_FILE_EXTENSIONS


def get_repo_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find repository root")


def run_rclone(args: list, capture=True) -> tuple:
    """Run rclone command."""
    cmd = [RCLONE] + args
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_lfs_files() -> list:
    """Get list of files tracked by LFS."""
    result = subprocess.run(
        ["git", "lfs", "ls-files", "-n"],
        capture_output=True, text=True,
        cwd=get_repo_root()
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]


def find_large_files(repo_root: Path) -> list:
    """Find all large files in repo."""
    large_files = []
    for root, dirs, files in os.walk(repo_root):
        if ".git" in dirs:
            dirs.remove(".git")
        for filename in files:
            filepath = Path(root) / filename
            ext = filepath.suffix.lower()
            if ext in LARGE_FILE_EXTENSIONS:
                rel_path = filepath.relative_to(repo_root).as_posix()
                large_files.append(rel_path)
    return large_files


def upload_file(repo_root: Path, rel_path: str) -> bool:
    """Upload a single file to Google Drive."""
    local_path = repo_root / rel_path
    if not local_path.exists():
        print(f"  SKIP (not found): {rel_path}")
        return False

    # Destination path in Drive (preserve folder structure)
    remote_path = f"{REMOTE}:{{{{1s3--pi4tpEAhW9sO9cfLh8orU0mCgiK-}}}}/{rel_path}"

    # Use copyto to upload to specific path
    success, stdout, stderr = run_rclone([
        "copyto",
        str(local_path),
        f"{REMOTE}:/{rel_path}",
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
        "-v"
    ])

    if success:
        print(f"  OK: {rel_path}")
    else:
        print(f"  FAIL: {rel_path} - {stderr}")

    return success


def get_drive_file_id(rel_path: str) -> str:
    """Get the Drive file ID for a file."""
    success, stdout, stderr = run_rclone([
        "lsjson",
        f"{REMOTE}:/{rel_path}",
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
    ])

    if not success or not stdout.strip():
        return None

    try:
        data = json.loads(stdout)
        if data and len(data) > 0:
            return data[0].get("ID")
    except json.JSONDecodeError:
        pass

    return None


def upload_all_files(repo_root: Path, files: list) -> dict:
    """Upload all files and return mapping of path -> drive_id."""
    print(f"\nUploading {len(files)} files to Google Drive...")
    print(f"Drive folder ID: {DRIVE_FOLDER_ID}\n")

    # Upload all files at once using copy
    success, stdout, stderr = run_rclone([
        "copy",
        str(repo_root),
        f"{REMOTE}:/",
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
        "--include", "*.pdf",
        "--include", "*.pptx",
        "--include", "*.ppt",
        "--include", "*.zip",
        "--include", "*.7z",
        "--include", "*.iso",
        "--include", "*.mov",
        "--include", "*.mp4",
        "-v",
        "--stats", "1s",
        "--stats-one-line",
    ], capture=False)

    return success


def get_all_drive_ids(repo_root: Path) -> dict:
    """Get all file IDs from Drive."""
    print("\nGetting file IDs from Google Drive...")

    success, stdout, stderr = run_rclone([
        "lsjson",
        f"{REMOTE}:/",
        "--drive-root-folder-id", DRIVE_FOLDER_ID,
        "-R",  # Recursive
    ])

    if not success:
        print(f"Error getting file list: {stderr}")
        return {}

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}

    # Build path -> ID mapping
    file_ids = {}
    for item in data:
        if not item.get("IsDir", False):
            path = item.get("Path", "")
            file_id = item.get("ID", "")
            size = item.get("Size", 0)
            if path and file_id:
                file_ids[path] = {"driveId": file_id, "size": size}

    return file_ids


def update_manifest(repo_root: Path, file_ids: dict):
    """Update the manifest with file IDs."""
    manifest_path = repo_root / "Obsidian" / "scripts" / "drive-sync" / "manifest.json"

    manifest = {
        "version": 1,
        "description": "Large files stored in Google Drive. Run download.py to fetch them.",
        "drive_folder_id": DRIVE_FOLDER_ID,
        "files": []
    }

    for path, info in sorted(file_ids.items()):
        manifest["files"].append({
            "path": path,
            "driveId": info["driveId"],
            "size": info["size"]
        })

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nManifest updated with {len(manifest['files'])} files")
    print(f"Saved to: {manifest_path}")


def main():
    repo_root = get_repo_root()

    print("=" * 60)
    print("RCLONE MIGRATION: Upload large files to Google Drive")
    print("=" * 60)

    # Get files to upload
    lfs_files = get_lfs_files()
    print(f"\nFound {len(lfs_files)} files in Git LFS")

    # Step 1: Upload
    print("\n" + "=" * 60)
    print("STEP 1: Uploading files to Google Drive")
    print("=" * 60)

    upload_all_files(repo_root, lfs_files)

    # Step 2: Get IDs
    print("\n" + "=" * 60)
    print("STEP 2: Getting Drive file IDs")
    print("=" * 60)

    file_ids = get_all_drive_ids(repo_root)
    print(f"Found {len(file_ids)} files in Drive")

    # Step 3: Update manifest
    print("\n" + "=" * 60)
    print("STEP 3: Updating manifest")
    print("=" * 60)

    update_manifest(repo_root, file_ids)

    print("\n" + "=" * 60)
    print("Migration complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Verify the manifest: python upload.py --list")
    print("2. Remove LFS tracking: git lfs untrack '*.pdf' etc.")
    print("3. Commit changes: git add -A && git commit -m 'Migrate to Drive sync'")


if __name__ == "__main__":
    main()
