"""
Configuration for Google Drive sync.

Setup instructions:
1. Create a Google Drive folder for your vault assets
2. Set folder sharing to "Anyone with the link can view"
3. Copy the folder ID from the URL (the part after /folders/)
4. Paste it below as DRIVE_FOLDER_ID
"""

# Google Drive folder ID (from URL: drive.google.com/drive/folders/THIS_PART)
DRIVE_FOLDER_ID = "1s3--pi4tpEAhW9sO9cfLh8orU0mCgiK-"

# File extensions to sync (matches your previous LFS config)
LARGE_FILE_EXTENSIONS = {
    ".pdf",
    ".pptx",
    ".ppt",
    ".zip",
    ".iso",
    ".7z",
    ".mov",
    ".mp4",
}

# Minimum file size to consider "large" (in bytes) - optional filter
# Set to 0 to sync all files matching extensions above
MIN_FILE_SIZE_BYTES = 0

# Manifest file location (relative to repo root)
MANIFEST_FILE = "Obsidian/scripts/drive-sync/manifest.json"
