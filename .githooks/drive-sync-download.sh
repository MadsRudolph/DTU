#!/bin/sh
#
# Shared body for post-merge / post-rewrite: download new Drive files when
# manifest.json changed between ORIG_HEAD and HEAD.
#
MANIFEST="Obsidian/scripts/drive-sync/manifest.json"

if git diff-tree -r --name-only ORIG_HEAD HEAD 2>/dev/null | grep -qF "$MANIFEST"; then
    echo ""
    echo "=== Drive sync: manifest.json changed, checking for new files... ==="
    echo ""

    if command -v python3 >/dev/null 2>&1; then
        PYTHON=python3
    elif command -v python >/dev/null 2>&1; then
        PYTHON=python
    else
        echo "Warning: Python not found. Run manually:"
        echo "  python Obsidian/scripts/drive-sync/download.py"
        exit 0
    fi

    PYTHONUTF8=1 $PYTHON Obsidian/scripts/drive-sync/download.py

    echo ""
    echo "=== Drive sync complete ==="
    echo ""
fi
