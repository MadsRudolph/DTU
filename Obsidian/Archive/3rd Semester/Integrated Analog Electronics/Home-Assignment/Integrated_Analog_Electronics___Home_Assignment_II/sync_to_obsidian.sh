#!/bin/bash
# Auto-sync PDF to Obsidian vault after LaTeX compilation

SOURCE="main.pdf"
DEST="C:/Users/Mads2/DTU/Obsidian/Courses/Integrated Analog Electronics/Exercises/Home Assignments/2/Home_Assignment_II_Submission.pdf"

if [ -f "$SOURCE" ]; then
    cp "$SOURCE" "$DEST"
    echo "[$(date '+%H:%M:%S')] PDF synced to Obsidian"
else
    echo "[$(date '+%H:%M:%S')] ERROR: $SOURCE not found"
    exit 1
fi
