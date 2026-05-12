# HANDOFF: Install the NotebookLM skill on this PC

You (Claude Code) are being asked to replicate Mads's NotebookLM skill setup from his other PC onto this one. Everything you need is in this directory. **Read the whole document before you start — don't skip ahead.**

## What you're installing

A local Claude Code skill (`notebooklm`) that lets Claude consult Mads's NotebookLM notebooks per DTU course (DSP, Linear Control, Digital Systems Design, Integrated Analog Electronics 2, Internet of Things). It auto-triggers whenever DTU coursework is mentioned. Backed by a CLI wrapper (`nlm.bat`) that talks to NotebookLM via `notebooklm-py`.

After install, future Claude sessions on this PC will discover the skill from `~/.claude/skills/notebooklm/` and propose using it for course-specific technical questions.

## Assumptions

- Windows PC, same layout as Mads's main PC:
  - Miniconda Python at `%USERPROFILE%\miniconda3\python.exe` (Python 3.9+)
  - User's Google account has access to the same NotebookLM notebooks as the source PC (UUIDs are account-bound, not machine-bound — the alias map in `skill-files/data/library.json` will work as-is)
- Mads has NotebookLM Pro (300 sources/notebook).

If miniconda is **elsewhere**: edit `$PYTHON` on line 5 of `INSTALL.ps1` to the actual path before running. Ask Mads if you're unsure.

## Steps to execute

### 1. Pre-flight (run all checks in parallel)

```bash
ls "$USERPROFILE/miniconda3/python.exe"         # must exist
ls "$USERPROFILE/.claude/skills/notebooklm/"    # should NOT exist yet
```

If the skill dir already exists: **stop and ask Mads** before overwriting. The library.json might have his customizations.

### 2. Run the installer

The DTU repo lives at `C:\Users\Mads2\DTU` on this user's machines.

```powershell
cd C:\Users\Mads2\DTU\notebooklm-skill
.\INSTALL.ps1
```

The script handles: file copy → `pip install notebooklm-py[browser]` → `playwright install chromium` → login prompt → verification → scheduled task.

**Critical**: don't try to run `playwright install chromium` yourself via the Bash tool first. On Mads's main PC, when I (Claude) downloaded Chromium from a sandboxed Bash subprocess, the `chrome.exe` ended up tagged with an `S-1-15-3-*` AppContainer SID and refused to launch — even though file perms looked fine. Always let the user's interactive PowerShell run the playwright install. The INSTALL.ps1 script does this correctly.

### 3. Interactive login step (you cannot do this — Mads must)

When the installer reaches the login step, it will print instructions and pause for ENTER. **Tell Mads**:

> "A Chromium window is about to open. Sign in with the Google account that owns your NotebookLM notebooks (the same account as on your other PC). Wait until you see the NotebookLM homepage. Then come back to PowerShell and press ENTER."

Wait for him to confirm he's done before continuing.

### 4. Verify the install

After INSTALL.ps1 exits cleanly, run these from Bash or PowerShell:

```bash
"$USERPROFILE/.claude/skills/notebooklm/scripts/nlm.bat" list
"$USERPROFILE/.claude/skills/notebooklm/scripts/nlm.bat" library-list
"$USERPROFILE/.claude/skills/notebooklm/scripts/nlm.bat" ask "What is aliasing?" --notebook-id dsp
```

**Pass criteria:**
- `list` shows the 5 DTU notebooks (DTU 34315, DTU 34655, DTU 62711, DTU 62743, and Linear Control Design 1)
- `library-list` shows 5 aliases: `iot`, `iae2`, `lcd1`, `dsd`, `dsp`
- `ask` returns a grounded answer from the DSP notebook with citations like `[1-3]`

If `list` shows 0 notebooks → wrong Google account during login. Run `nlm.bat login` again.

### 5. Persist memory for future sessions

Copy these files from this directory **OR** equivalent on Mads's other PC into the user's Claude memory dir on this PC:

```
%USERPROFILE%\.claude\projects\C--Users-Mads2\memory\notebooklm_skill.md
```

The pointer line in `MEMORY.md`:

```
- [NotebookLM skill](notebooklm_skill.md) — installed at `~/.claude/skills/notebooklm/`, invoke via `nlm.bat`, auto-refresh scheduled, uses conda Python not Store Python
```

If you can't access the source memory file from the other PC, recreate it from the comprehensive context in `skill-files/SKILL.md` and `README-TRANSFER.md`.

### 6. Tell Mads to restart Claude Code

The `notebooklm` skill is discovered at session start. Tell him:

> "Restart Claude Code (or start a new session). The skill will appear in the available-skills list as `notebooklm`. Test with: 'What does my DSP course say about FIR vs IIR filters?' — Claude should auto-invoke the skill, pick the `dsp` alias, and reply with citations."

## Key facts you need to know

- **The CLI is patched 3 times** from upstream (see `skill-files/SKILL.md` + `skill-files/reference.md`). All patches are baked into `scripts/nlm.py` already.
- **Alias resolution** — `nlm.bat ask --notebook-id dsp` works because `data/library.json` maps `dsp` → the real UUID. If you ever see a "Not found" error, FIRST run `nlm.bat library-list` to verify the alias is registered, BEFORE assuming auth has expired.
- **Auth diagnosis** — if `ask` fails for any reason, run `nlm.bat auth-status` first. It will say `Auth looks fresh` (then the problem is elsewhere — likely wrong alias/UUID) or `NOT AUTHENTICATED` (run `nlm.bat login`).
- **PPTX is supported** by NotebookLM despite the upstream docs not listing it.
- **Auto-refresh scheduled task** runs every 3 days at 05:30 to keep cookies warm. INSTALL.ps1 creates it.

## Common failures and fixes

| Symptom | Cause | Fix |
|---|---|---|
| `Miniconda Python not found` | Conda installed elsewhere | Edit `$PYTHON` at top of `INSTALL.ps1`, re-run |
| `Executable doesn't exist at chrome.exe` | Chromium downloaded from sandboxed shell | `& "$env:USERPROFILE\miniconda3\python.exe" -m playwright install --force chromium` from PowerShell directly |
| `RPC GET_NOTEBOOK ... Not found` | Alias didn't resolve OR wrong notebook UUID | Run `nlm.bat library-list`; verify; run `nlm.bat list` to confirm UUIDs match |
| `Authentication expired` after long inactivity | Cookies aged past auto-refresh window | `nlm.bat login` — 30 sec browser flow |
| Source caps at 50 | Free tier somehow | Confirm Pro tier with Mads; Pro = 300/notebook |

## What NOT to do

- Don't `pip install notebooklm-py` against a Windows Store Python. It's installed against miniconda 3.13. The wrapper `.bat` files hardcode miniconda's path via `%USERPROFILE%`.
- Don't try to copy `~/.notebooklm/profiles/default/storage_state.json` from the other PC. Auth must be done freshly per machine — both for security and because the persistent browser profile (which makes auto-refresh work) is gigabytes and machine-specific.
- Don't try to upload course material to NotebookLM on this PC from scratch — the source notebooks already exist under Mads's Google account, and `library.json` already points to their UUIDs. This is purely a *client-side install*.
- Don't proactively run upload scripts (`upload_dtu.py`, `upload_dsp.py` from the source PC). They're not in this bundle for a reason — they're historical and not needed for the second PC.

## Done state

You can consider the install complete when:
1. `INSTALL.ps1` exited 0
2. `nlm.bat list` shows the DTU notebooks
3. `nlm.bat ask "..." --notebook-id dsp` returns a cited answer
4. Scheduled task `NotebookLM Cookie Refresh` shows up in `schtasks /Query`
5. You've told Mads to restart Claude Code to pick up the new skill

Tell him the new aliases (`iot`, `iae2`, `lcd1`, `dsd`, `dsp`) and that the skill will fire automatically on DTU coursework questions in his next session.
