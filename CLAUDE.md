# CLAUDE.md — repo handoff

This file is auto-loaded by Claude Code and travels with `git pull`. It records **where to pick up** the active work so a fresh session on any PC can continue seamlessly.

---

## ACTIVE WORK: 62743 DSP Re-exam prep

**Goal:** Prepare for the DTU 62743 Digital Signal Processing re-exam (exam Wed 20 May 2026). Work through past exams, filter questions first.

### ▶️ PICK UP HERE (next action)

**F25 Question 4** — digital LP filter realization + application. Working file: `3.semester/DSP/EXAMS/F25_new.m` (section `%% Problem 4`).
Q4 sub-parts: 4-1 (read H(z) off the Direct-Form block diagram, FIR vs IIR), 4-2 (magnitude dB plot, read 3 dB point), 4-3 (poles/zeros + stability), 4-4 (sample xa(t), aliasing check), 4-5 (filter with `filter()`, compare before/after).

Give a small hint and let the user attempt first (see Workflow below).

### Strategy

**Filter-first.** Prioritize MATLAB filter-design questions (`butter`/`lp2lp`/`lp2hp`/`lp2bs`/`bilinear`/`freqz`/`fir`/`filter`). Defer pure-math questions (Z-transform algebra, ROC, DTFT-by-hand, min-phase decomposition). Getting the filter questions right is the pass criterion.

### Status

| Exam | Filter questions | State |
|---|---|---|
| **F24** | Q2 (AA Butterworth LP), Q4 (IIR bandstop BLT) | ✅ complete + walkthrough; Q1/Q3 deferred math |
| **F25** | Q2 (IIR highpass BLT), Q4 (filter realization + apply) | Q2 ✅ done & verified; **Q4 = next** |
| **F23** | Q2 (spectrum + given H(z)), Q4 (FIR HP Fourier + Blackman) | scaffolded only, not started |

Walkthrough notes (Obsidian): `Obsidian/Courses/62743 Digital Signal Processing (Reexam)/Notes/` — `F24/F25/F23 exam walkthrough.md`, `DSP MATLAB helpers cheat sheet.md`.
Exam + solution PDFs: `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/` (gitignored — must exist locally / via Drive sync).

### Workflow conventions (the user corrected me on these — follow them)

- **Hints-first.** When the user says "let's do QX" / "on to QX", give a *small* starting hint then STOP and wait for their attempt. Only give the full step-by-step walkthrough when they explicitly say "walk me through it" / "I don't understand" / "do it for me".
- **Verify against truth source.** The `*student solutions*.pdf` files are absolute truth. Use the `notebooklm` skill (`C:\Users\Mads2\.claude\skills\notebooklm\scripts\nlm.bat ask "..." --notebook-id dsp`) to ground slide citations; re-`login` if auth expired.
- **MATLAB comments in Danish**, real `øæå` (never `oe/ae/aa`). Exam requires "kommenteret kode".
- **Obsidian notes use `[[wikilinks]]`** for vault file references, not bare paths.
- After completing a question: log it into the relevant `... exam walkthrough.md`, then continue.
- DTU notation: `Ω` = analog rad/s, `ω` = digital rad/sample, `f` = normalized `F/Fs`. Conversions: `Ω = 2πF`, `ω = ΩT = 2πf`. `freqs`→rad/s; `bilinear`/`freqz`→Hz.

### Key reusable patterns (already in the walkthroughs)

- **IIR via BLT pipeline:** spec → prewarp `Ω=(2/Ts)tan(πf)` → order `n=ceil(log10((10^(0.1·As)-1)/ε²)/(2log10(νs)))` → prototype (appendix) → `lp2xx` → `bilinear` → `freqz` dB. LP order ratio `νs=Ωs/Ωp`; **HP is inverted: `νs=Ωp/Ωs`**; BP/BS double the order, LP/HP don't.
- **Classmate helpers** in `3.semester/DSP/Helpers/`: `n_value` (order+prototype in one call — ⚠️ Chebyshev n=4 entry is buggy), `time_vec`, `frequency_vec`, `FIR_fourier`, `FIR_window`, `MK_values`.

### Known repo issue

A broken nested git repo at `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/Report` makes repo-wide `git add -A` abort. Stage DSP work by explicit path. Do **not** attempt to fix the broken submodule without the user's explicit go-ahead (destructive).
