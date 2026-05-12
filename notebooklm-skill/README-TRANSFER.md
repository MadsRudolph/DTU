# NotebookLM skill — second PC install

## What's in this bundle

```
notebooklm-transfer/
├── INSTALL.ps1          ← run this in PowerShell on the new PC
├── README-TRANSFER.md   ← this file
└── skill-files/         ← gets copied to ~/.claude/skills/notebooklm/
    ├── SKILL.md         ← DTU-focused skill (with custom patches)
    ├── reference.md     ← upstream full reference
    ├── README.md        ← upstream readme
    ├── data/
    │   └── library.json ← course alias map (iot, iae2, lcd1, dsd, dsp → UUIDs)
    └── scripts/
        ├── nlm.py       ← CLI (patched 3x: subprocess.exe, profile paths, alias resolution)
        ├── nlm.bat      ← portable wrapper (uses %USERPROFILE%)
        ├── refresh_auth.py
        └── refresh.bat
```

## Prerequisites on the new PC

- Windows
- Miniconda Python 3.9+ at `%USERPROFILE%\miniconda3\python.exe` (the script will tell you if it's somewhere else)
- A Google account with access to the same NotebookLM library (same account as the source PC — UUIDs match per account, not per machine)

## Install steps

1. Copy this whole `notebooklm-transfer\` folder to the new PC (USB / cloud drive / however).
2. Open PowerShell, navigate to the folder, and run:

   ```powershell
   .\INSTALL.ps1
   ```

   If PowerShell complains about execution policy:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\INSTALL.ps1
   ```

3. The script will:
   - Verify your Python
   - Copy skill files to `%USERPROFILE%\.claude\skills\notebooklm\`
   - `pip install notebooklm-py[browser]`
   - `playwright install chromium` (~330 MB — do this from PowerShell, not WSL/bash, or chromium gets sandboxed and won't launch)
   - Prompt you to do a one-time Google login (browser opens, sign in, press ENTER)
   - Verify with `nlm.bat list`
   - Create the Windows scheduled task `NotebookLM Cookie Refresh` (every 3 days, 05:30)

4. In your **next Claude Code session** on the new PC, the `notebooklm` skill auto-discovers from the skills dir. Test with something like:

   > *"What does my DSP course say about FIR vs IIR filters?"*

   Claude should invoke the skill, pick the `dsp` alias, and reply with citations.

## Verify it worked

```powershell
& "$env:USERPROFILE\.claude\skills\notebooklm\scripts\nlm.bat" list
& "$env:USERPROFILE\.claude\skills\notebooklm\scripts\nlm.bat" library-list
& "$env:USERPROFILE\.claude\skills\notebooklm\scripts\nlm.bat" ask "What is aliasing?" --notebook-id dsp
```

You should see all your notebooks, the alias map, and a grounded DSP answer.

## If something breaks

- **`Authentication expired`-style errors** → run `nlm.bat login` again (browser opens, ~30s)
- **chromium fails to launch** → `& "$env:USERPROFILE\miniconda3\python.exe" -m playwright install --force chromium` (from PowerShell, not bash)
- **Alias not resolving** → check `data/library.json` exists at `~/.claude/skills/notebooklm/data/library.json` with the iot/iae2/lcd1/dsd/dsp slugs

## Memory transfer (optional but recommended)

The Claude Code memory file documenting this skill is at:

```
%USERPROFILE%\.claude\projects\C--Users-Mads2\memory\notebooklm_skill.md
```

Copy it to the same path on the new PC so future Claude sessions remember the patches, alias map, and auth quirks. Also add a pointer line to `MEMORY.md` matching the source PC.
