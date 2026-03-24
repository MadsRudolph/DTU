#!/usr/bin/env python3
"""
Migration helper: Move from Git LFS to Google Drive.

This script guides you through the migration process.
Run it step by step to migrate your large files.

Usage:
    python migrate-from-lfs.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from config import LARGE_FILE_EXTENSIONS


def get_repo_root() -> Path:
    """Find the repository root."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find repository root")


def run_command(cmd: list, capture=True) -> tuple:
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(cmd, capture_output=capture, text=True, cwd=get_repo_root())
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)


def check_lfs_installed() -> bool:
    """Check if Git LFS is installed."""
    success, _ = run_command(["git", "lfs", "version"])
    return success


def list_lfs_files() -> list:
    """List all files tracked by LFS."""
    success, output = run_command(["git", "lfs", "ls-files", "-n"])
    if not success:
        return []
    return [line.strip() for line in output.strip().split("\n") if line.strip()]


def get_lfs_file_sizes(repo_root: Path, files: list) -> list:
    """Get sizes of LFS files."""
    result = []
    for f in files:
        filepath = repo_root / f
        if filepath.exists():
            size = filepath.stat().st_size
            result.append({
                "path": f,
                "size": size,
                "size_mb": round(size / (1024 * 1024), 2)
            })
        else:
            result.append({"path": f, "size": 0, "size_mb": 0})
    return result


def print_step(num: int, title: str):
    """Print a step header."""
    print(f"\n{'='*60}")
    print(f"STEP {num}: {title}")
    print('='*60)


def main():
    repo_root = get_repo_root()

    print("=" * 60)
    print("MIGRATION: Git LFS -> Google Drive")
    print("=" * 60)

    # Check LFS
    if not check_lfs_installed():
        print("Git LFS is not installed. Nothing to migrate.")
        return

    # List LFS files
    lfs_files = list_lfs_files()
    if not lfs_files:
        print("No files are currently tracked by Git LFS.")
        return

    files_with_sizes = get_lfs_file_sizes(repo_root, lfs_files)
    total_size = sum(f["size"] for f in files_with_sizes)

    print(f"\nFound {len(lfs_files)} files tracked by Git LFS:")
    print(f"Total size: {total_size / (1024*1024):.2f} MB\n")

    for f in files_with_sizes[:20]:  # Show first 20
        print(f"  {f['size_mb']:>8.2f} MB  {f['path']}")
    if len(files_with_sizes) > 20:
        print(f"  ... and {len(files_with_sizes) - 20} more files")

    # Step 1
    print_step(1, "Create Google Drive Folder")
    print("""
    1. Go to Google Drive (drive.google.com)
    2. Create a new folder: "DTU-Vault-Assets"
    3. Right-click the folder > Share > General access > "Anyone with the link"
    4. Copy the folder link

    The folder ID is in the URL after /folders/
    Example: https://drive.google.com/drive/folders/ABC123xyz
    Folder ID: ABC123xyz
    """)

    folder_id = input("Enter your Drive folder ID (or 'skip' to continue later): ").strip()
    if folder_id and folder_id.lower() != 'skip':
        # Update config
        config_path = repo_root / "Obsidian" / "scripts" / "drive-sync" / "config.py"
        config_content = config_path.read_text()
        config_content = config_content.replace(
            'DRIVE_FOLDER_ID = ""',
            f'DRIVE_FOLDER_ID = "{folder_id}"'
        )
        config_path.write_text(config_content)
        print(f"Updated config.py with folder ID: {folder_id}")

    # Step 2
    print_step(2, "Upload Files to Google Drive")
    print("""
    Upload all your large files to the Google Drive folder.

    Options:
    a) Drag and drop files in browser (easiest for small number of files)
    b) Use Google Drive desktop app to sync a local folder
    c) Use rclone for command-line uploads

    Tip: You can maintain the folder structure in Drive for organization,
    but the manifest tracks files by Drive ID, so flat structure works too.
    """)

    input("Press Enter when you've uploaded the files...")

    # Step 3
    print_step(3, "Register Files in Manifest")
    print("""
    Now you need to register each file in the manifest with its Drive ID.

    For each file:
    1. Find it in Google Drive
    2. Right-click > Get link > Copy link
    3. Extract the file ID from the URL

    Run this command for interactive registration:

        python Obsidian/scripts/drive-sync/upload.py --interactive

    Or add files one by one:

        python Obsidian/scripts/drive-sync/upload.py --add "path/to/file.pdf" "DRIVE_ID"
    """)

    input("Press Enter when you've added files to the manifest...")

    # Step 4
    print_step(4, "Remove Git LFS Tracking")
    print("""
    Now we'll remove LFS tracking. This will:
    - Update .gitattributes to remove LFS filters
    - The files will become regular Git-ignored files

    Commands to run:
    """)

    # Generate untrack commands
    extensions = set()
    for f in lfs_files:
        ext = Path(f).suffix.lower()
        if ext:
            extensions.add(ext)

    print("    # Remove LFS tracking for each extension:")
    for ext in sorted(extensions):
        print(f"    git lfs untrack '*{ext}'")

    print("\n    # Verify .gitattributes is clean:")
    print("    cat .gitattributes")

    proceed = input("\nRun these commands automatically? (yes/no): ").strip().lower()
    if proceed == 'yes':
        for ext in sorted(extensions):
            success, output = run_command(["git", "lfs", "untrack", f"*{ext}"])
            if success:
                print(f"  Untracked: *{ext}")
            else:
                print(f"  Failed to untrack *{ext}: {output}")

    # Step 5
    print_step(5, "Commit Changes")
    print("""
    The large files are now:
    - Ignored by .gitignore (won't be tracked)
    - Tracked in manifest.json (for Drive sync)
    - Removed from LFS tracking

    Commit your changes:

        git add .gitignore .gitattributes Obsidian/scripts/drive-sync/
        git commit -m "Migrate large files from LFS to Google Drive sync"

    Note: The large files will remain in your git history.
    To fully remove them and shrink the repo, you'd need to rewrite history
    using git-filter-repo or BFG Repo Cleaner (advanced, optional).
    """)

    # Step 6
    print_step(6, "Test the Setup")
    print("""
    To test that everything works:

    1. Clone the repo to a new location:
       git clone <your-repo> test-clone

    2. Run the download script:
       cd test-clone
       pip install -r Obsidian/scripts/drive-sync/requirements.txt
       python Obsidian/scripts/drive-sync/download.py

    3. Verify files are downloaded correctly
    """)

    print("\n" + "=" * 60)
    print("Migration guide complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
