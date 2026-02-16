# Google Drive Sync for Large Files

Large files (PDFs, slides, videos) are stored in Google Drive instead of Git to keep the repo lightweight. This system automatically syncs them while preserving Obsidian cross-links.

## After Cloning

```bash
winget install Rclone.Rclone          # If rclone not yet installed
rclone config                         # Set up 'gdrive' remote (one-time)
PYTHONUTF8=1 python Obsidian/scripts/drive-sync/download.py
```

This downloads ~400 files (~1GB) from Google Drive using rclone (authenticated).
Falls back to gdown if rclone is not available (requires public sharing).

## Adding New Files

When you add a new PDF, slide, or other large file:

```bash
python Obsidian/scripts/drive-sync/upload.py
```

The script will:
1. Find new large files not yet in Drive
2. Show them and ask for confirmation
3. Upload to Google Drive using rclone
4. Update the manifest automatically

## Syncing From Another PC

If you uploaded files to Drive from another machine:

```bash
git pull                                # Get latest manifest
python upload.py --pull                 # Find new files on Drive
python download.py                      # Download them
```

## Command Reference

### upload.py

| Command | Description |
|---------|-------------|
| `python upload.py` | Scan and prompt to upload new files |
| `python upload.py --scan` | Just scan, don't upload |
| `python upload.py --sync` | Upload without prompting |
| `python upload.py --pull` | Find files on Drive not in manifest |
| `python upload.py --list` | List all files in manifest |
| `python upload.py --refresh` | Rebuild manifest from Drive |
| `python upload.py --remove PATH` | Remove a file from manifest |

### download.py

| Command | Description |
|---------|-------------|
| `python download.py` | Download missing files |
| `python download.py --verify` | Verify existing files match expected size |
| `python download.py --force` | Re-download all files |
| `python download.py --dry-run` | Show what would be downloaded |

## File Types Tracked

Configured in `config.py`:
- PDFs (`.pdf`)
- Presentations (`.pptx`, `.ppt`)
- Archives (`.zip`, `.7z`, `.iso`)
- Videos (`.mov`, `.mp4`)

## How It Works

```
Local files  ──upload.py──►  Google Drive
                                  │
                                  ▼
manifest.json ◄── tracks file paths + Drive IDs
                                  │
                                  ▼
New clone    ◄──download.py──  Google Drive
```

1. `upload.py` uses rclone to upload files to Drive
2. `manifest.json` maps local paths to Drive file IDs
3. `download.py` uses rclone to download (falls back to gdown)
4. `.gitignore` excludes large files from git

## Requirements

- Python 3.8+
- rclone (configured with `gdrive` remote) - for uploading and downloading
- gdown (`pip install gdown`) - optional fallback for downloading

## Troubleshooting

**Windows UTF-8 issues with Danish characters:**
```bash
PYTHONUTF8=1 python download.py
```

**Manifest out of sync with Drive:**
```bash
python upload.py --refresh
```

**Files uploaded from another PC not showing:**
```bash
python upload.py --pull
```
