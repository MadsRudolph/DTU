#!/usr/bin/env python3
"""
Upload large files to Google Drive and update the manifest.

This script helps you:
1. Find large files not yet in the manifest
2. Upload them to Google Drive (opens browser for manual upload)
3. Register the Drive file ID in the manifest

Usage:
    python upload.py --scan              # Find large files not in manifest
    python upload.py --add PATH DRIVE_ID # Add a file to manifest after uploading
    python upload.py --remove PATH       # Remove a file from manifest

Note: Due to Google Drive API complexity, actual uploading is done manually.
This script helps manage the manifest and guides you through the process.

Requirements:
    pip install requests
"""

import argparse
import json
import os
import sys
from pathlib import Path

from config import LARGE_FILE_EXTENSIONS, MIN_FILE_SIZE_BYTES


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
        return {"version": 1, "files": []}

    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(repo_root: Path, manifest: dict):
    """Save the manifest file."""
    manifest_path = repo_root / "Obsidian" / "scripts" / "drive-sync" / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Manifest saved to {manifest_path}")


def get_manifest_paths(manifest: dict) -> set:
    """Get all paths currently in the manifest."""
    return {entry["path"] for entry in manifest.get("files", [])}


def find_large_files(repo_root: Path, manifest_paths: set) -> list:
    """Find large files not in the manifest."""
    large_files = []

    for root, dirs, files in os.walk(repo_root):
        # Skip .git directory
        if ".git" in dirs:
            dirs.remove(".git")

        for filename in files:
            filepath = Path(root) / filename
            ext = filepath.suffix.lower()

            if ext not in LARGE_FILE_EXTENSIONS:
                continue

            # Get relative path
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


def scan_files(repo_root: Path, manifest: dict):
    """Scan for large files not in manifest."""
    manifest_paths = get_manifest_paths(manifest)
    large_files = find_large_files(repo_root, manifest_paths)

    if not large_files:
        print("All large files are already in the manifest!")
        return

    print(f"Found {len(large_files)} large files not in manifest:\n")

    total_size = 0
    for f in large_files:
        print(f"  {f['size_mb']:>8.2f} MB  {f['path']}")
        total_size += f['size']

    print(f"\n  Total: {total_size / (1024*1024):.2f} MB")
    print("\nTo add a file to the manifest:")
    print("  1. Upload the file to your Google Drive folder")
    print("  2. Right-click > Get link > Copy link")
    print("  3. Extract the file ID from the URL")
    print('  4. Run: python upload.py --add "PATH" "DRIVE_FILE_ID"')
    print("\nExample Drive URL: https://drive.google.com/file/d/ABC123xyz/view")
    print("The file ID is: ABC123xyz")


def add_file(repo_root: Path, manifest: dict, rel_path: str, drive_id: str):
    """Add a file to the manifest."""
    filepath = repo_root / rel_path

    if not filepath.exists():
        print(f"Warning: File does not exist locally: {rel_path}")
        print("Adding to manifest anyway (file may have been deleted after upload)")

    # Check if already in manifest
    for entry in manifest.get("files", []):
        if entry["path"] == rel_path:
            print(f"Updating existing entry for: {rel_path}")
            entry["driveId"] = drive_id
            if filepath.exists():
                entry["size"] = filepath.stat().st_size
            save_manifest(repo_root, manifest)
            return

    # Add new entry
    entry = {
        "path": rel_path,
        "driveId": drive_id,
    }
    if filepath.exists():
        entry["size"] = filepath.stat().st_size

    manifest.setdefault("files", []).append(entry)
    manifest["files"].sort(key=lambda x: x["path"])

    save_manifest(repo_root, manifest)
    print(f"Added to manifest: {rel_path}")


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


def bulk_add_interactive(repo_root: Path, manifest: dict):
    """Interactive mode to add multiple files."""
    manifest_paths = get_manifest_paths(manifest)
    large_files = find_large_files(repo_root, manifest_paths)

    if not large_files:
        print("No untracked large files found!")
        return

    print(f"Found {len(large_files)} files to add.\n")
    print("For each file, enter the Google Drive file ID (or 'skip' to skip, 'quit' to stop):\n")

    for f in large_files:
        print(f"\nFile: {f['path']}")
        print(f"Size: {f['size_mb']:.2f} MB")

        drive_id = input("Drive ID: ").strip()

        if drive_id.lower() == 'quit':
            break
        if drive_id.lower() == 'skip' or not drive_id:
            print("Skipped")
            continue

        # Handle if user pasted a full URL
        if "drive.google.com" in drive_id:
            # Extract ID from URL
            import re
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', drive_id)
            if match:
                drive_id = match.group(1)
                print(f"Extracted ID: {drive_id}")

        add_file(repo_root, manifest, f['path'], drive_id)


def main():
    parser = argparse.ArgumentParser(description="Manage large files for Google Drive sync")
    parser.add_argument("--scan", action="store_true", help="Find large files not in manifest")
    parser.add_argument("--add", nargs=2, metavar=("PATH", "DRIVE_ID"), help="Add a file to manifest")
    parser.add_argument("--remove", metavar="PATH", help="Remove a file from manifest")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive bulk add mode")
    parser.add_argument("--list", action="store_true", help="List all files in manifest")
    args = parser.parse_args()

    repo_root = get_repo_root()
    manifest = load_manifest(repo_root)

    if args.scan:
        scan_files(repo_root, manifest)
    elif args.add:
        add_file(repo_root, manifest, args.add[0], args.add[1])
    elif args.remove:
        remove_file(repo_root, manifest, args.remove)
    elif args.interactive:
        bulk_add_interactive(repo_root, manifest)
    elif args.list:
        files = manifest.get("files", [])
        if not files:
            print("Manifest is empty")
        else:
            print(f"Files in manifest ({len(files)}):\n")
            for f in files:
                size_str = f"{f.get('size', 0) / (1024*1024):.2f} MB" if f.get('size') else "unknown"
                print(f"  {size_str:>10}  {f['path']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
