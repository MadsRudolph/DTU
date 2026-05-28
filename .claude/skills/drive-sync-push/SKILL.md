---
name: drive-sync-push
description: Use BEFORE any git push or "commit and push" in the DTU coursework repo (C:\Users\Mads2\DTU) or any repo that contains Obsidian/scripts/drive-sync/upload.py. Large binaries (*.pdf, *.pptx, *.ppt, *.zip, video) are gitignored and stored in Google Drive via the drive-sync script — a plain git push does NOT carry them to other PCs. This skill uploads new large files to Drive and commits the manifest alongside the push. Triggers on "push", "commit and push", "git push", "sync and push", "commit-push-pr".
---

# Drive-sync before pushing

Large binaries in this repo (`*.pdf`, `*.pptx`, `*.ppt`, `*.docx`, `*.zip`, `*.7z`, video, audio)
are **gitignored** and live in **Google Drive**, tracked by
`Obsidian/scripts/drive-sync/manifest.json`. A plain `git push` does **not** carry them — other
PCs fetch them with `download.py`. So whenever the user asks to push, first make sure new large
files are on Drive and the (updated) manifest goes out with the commit.

## When this applies
Any "push" / "commit and push" / "git push" request, **only** if the repo root contains
`Obsidian/scripts/drive-sync/upload.py`. If it doesn't, this skill is irrelevant — just push normally.

## Steps
1. **Scan** for unsynced large files (read-only):
   ```
   python Obsidian/scripts/drive-sync/upload.py --scan
   ```
2. **If it reports new files**, show the user the list briefly, then upload them:
   ```
   python Obsidian/scripts/drive-sync/upload.py --sync
   ```
   This copies them to Google Drive and rebuilds `manifest.json`. Tell the user what was uploaded
   (count + total MB).
   - If the list is large/unexpected (e.g. dozens of files from old semesters), pause and confirm
     scope with the user before `--sync` — the manifest matching is normalization-robust as of the
     2026 fix, so a big list usually means genuinely-new files, but confirm if in doubt.
3. **Stage the manifest** so it travels with the commit:
   ```
   git add -- "Obsidian/scripts/drive-sync/manifest.json"
   ```
4. **Then do the user's commit + push** normally:
   - Stage the user's files **by explicit path** — never `git add -A` (this repo has a broken
     nested git repo under `Obsidian/Courses/34722 .../regbot/Report` that aborts repo-wide adds).
   - Commit message reads like the developer wrote it — **no AI attribution** (no `Co-Authored-By`).
   - `git push`.
5. **If `--scan` reports nothing**, there's nothing to sync — just commit + push.

## Notes
- Requires `rclone` configured with the `gdrive` remote (present on Mads's PCs).
- Path matching is NFC/NFD- and mojibake-robust (Danish `æ/ø/å`) as of the 2026 fix in `upload.py`,
  so `--scan` counts are trustworthy — no more files perpetually showing as "missing".
- `.git/`, `.venv/`, and `.claude/` are excluded from sync (the last avoids uploading throwaway
  git worktrees).
- To fetch large files on a fresh PC: `python Obsidian/scripts/drive-sync/download.py`.
