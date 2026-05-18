# CLAUDE.md — repo handoff

This file is auto-loaded by Claude Code and travels with `git pull`. It records **where to pick up** the active work so a fresh session on any PC can continue seamlessly.

---

## ACTIVE WORK: 62743 DSP Re-exam prep

**Goal:** Prepare for the DTU 62743 Digital Signal Processing re-exam (exam Wed 20 May 2026). Work through past exams, filter questions first.

### ▶️ PICK UP HERE (next action)

**E25 (the failed exam) — full re-solve.** Working file: `3.semester/DSP/EXAMS/E25_new.m` (skeleton built, all 3 problems scaffolded). Official solution PDF (truth source) now at `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/Solutions/62743 E25 Exam student solutions.pdf`.
Filter-first order: **P2** (IIR Direct Form II analysis, 30%) then **P3** (FIR highpass via windowing, 30%) = 60%. P1 is Z-transform math (40%, do last if time).
🚩 **Key trap (likely cause of the fail):** P2's DF-II feedback taps sit after the **2nd and 4th** delays → `A2 = [1, 0, 0.4860, 0, 0.0177]` (denominator `1+0.486z⁻²+0.0177z⁻⁴`), NOT `[1,0.486,0.0177]`. Skeleton already corrected; the vault `E25 Exam.md` writeup has this WRONG — don't trust it, use the official PDF.

Give a small hint and let the user attempt first (see Workflow below).

### Strategy

**Filter-first.** Prioritize MATLAB filter-design questions (`butter`/`lp2lp`/`lp2hp`/`lp2bs`/`bilinear`/`freqz`/`fir`/`filter`). Defer pure-math questions (Z-transform algebra, ROC, DTFT-by-hand, min-phase decomposition). Getting the filter questions right is the pass criterion.

### Status

| Exam | Filter questions | State |
|---|---|---|
| **F24** | Q2 (AA Butterworth LP), Q4 (IIR bandstop BLT) | ✅ complete + walkthrough; Q1/Q3 deferred math |
| **F25** | Q2 (IIR highpass BLT), Q4 (filter realization + apply) | ✅ complete + walkthrough; Q1/Q3-3 deferred math |
| **F23** | Q2 (spectrum + given H(z)), Q4 (FIR HP Fourier + Blackman) | scaffolded only; deferred (pivoted to E25) |
| **E25** | P2 (IIR DF-II analysis), P3 (FIR HP windowing); P1 = Z-math | **active** — skeleton ready + official solution PDF; P2 DF-II trap fixed |

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
