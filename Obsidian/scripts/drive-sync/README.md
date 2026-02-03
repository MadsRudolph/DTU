# Google Drive Sync for Large Files

This system keeps large files (PDFs, slides, videos) out of Git while preserving cross-links in Obsidian.

## Quick Start (After Cloning)

```bash
# Install dependencies
pip install -r Obsidian/scripts/drive-sync/requirements.txt

# Download all large files
python Obsidian/scripts/drive-sync/download.py
```

## How It Works

1. Large files are stored in a public Google Drive folder
2. `manifest.json` tracks file paths and their Drive IDs
3. `download.py` fetches missing files and places them in the correct locations
4. Git ignores these files via `.gitignore`

## Adding New Large Files

When you add new PDFs, slides, or other large files:

```bash
# 1. See what files need to be uploaded
python Obsidian/scripts/drive-sync/upload.py --scan

# 2. Upload files to Google Drive manually (drag & drop)

# 3. Get the file ID from the share link
#    Example: https://drive.google.com/file/d/ABC123xyz/view
#    File ID: ABC123xyz

# 4. Register in manifest
python Obsidian/scripts/drive-sync/upload.py --add "path/to/file.pdf" "ABC123xyz"

# Or use interactive mode for multiple files:
python Obsidian/scripts/drive-sync/upload.py --interactive
```

## Commands Reference

```bash
# Download missing files
python download.py

# Download and verify sizes
python download.py --verify

# Force re-download all
python download.py --force

# See what would be downloaded
python download.py --dry-run

# Scan for untracked large files
python upload.py --scan

# List files in manifest
python upload.py --list

# Add file to manifest
python upload.py --add "path/to/file.pdf" "DRIVE_ID"

# Remove file from manifest
python upload.py --remove "path/to/file.pdf"

# Interactive bulk add
python upload.py --interactive
```

## Configuration

Edit `config.py` to change:
- `DRIVE_FOLDER_ID` - Your Google Drive folder ID
- `LARGE_FILE_EXTENSIONS` - Which file types to track
- `MIN_FILE_SIZE_BYTES` - Minimum size threshold

## Manifest Format

```json
{
  "version": 1,
  "files": [
    {
      "path": "Obsidian/Courses/34315 IoT/Literature/paper.pdf",
      "driveId": "1abc123...",
      "size": 1234567
    }
  ]
}
```
