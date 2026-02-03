# Google Drive Sync for Large Files

Large files (PDFs, slides, videos) are stored in Google Drive instead of Git to keep the repo lightweight. This system automatically syncs them while preserving Obsidian cross-links.

## After Cloning

```bash
pip install -r Obsidian/scripts/drive-sync/requirements.txt
PYTHONUTF8=1 python Obsidian/scripts/drive-sync/download.py
```

This downloads ~336 files (~1GB) from Google Drive.

## Adding New Files

When you add a new PDF, slide, or other large file:

```bash
python Obsidian/scripts/drive-sync/upload.py
```

That's it. The script will:
1. Find new large files not yet in Drive
2. Show them and ask for confirmation
3. Upload to Google Drive using rclone
4. Update the manifest automatically

### Upload Options

```bash
python upload.py           # Scan and prompt to upload
python upload.py --scan    # Just scan, don't upload
python upload.py --sync    # Upload without prompting
python upload.py --list    # List all files in manifest
python upload.py --refresh # Rebuild manifest from Drive
```

## Download Options

```bash
python download.py           # Download missing files
python download.py --verify  # Verify existing files match expected size
python download.py --force   # Re-download all files
python download.py --dry-run # Show what would be downloaded
```

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
3. `download.py` uses gdown to fetch files by ID
4. `.gitignore` excludes large files from git

## Requirements

- Python 3.8+
- rclone (configured with `gdrive` remote)
- gdown (`pip install gdown`)

## Troubleshooting

**Windows UTF-8 issues with Danish characters:**
```bash
PYTHONUTF8=1 python download.py
```

**Manifest out of sync:**
```bash
python upload.py --refresh
```
