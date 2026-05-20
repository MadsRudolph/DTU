# CLAUDE.md — repo handoff

Auto-loaded by Claude Code, travels with `git pull`. Records **where to pick up** so a fresh session on any PC continues seamlessly.

---

## ACTIVE WORK: 62743 DSP Re-exam — **EXAM-READY** (exam Wed 20 May 2026, code E2-B, 4 h, all aids, no internet)

### ▶️ FIRST ACTION ON A FRESH PC (do this, in order)

1. `git pull` in `C:\Users\Mads2\DTU` (you just did — that's how you got this).
2. **Open the Obsidian hub:** `Obsidian/Courses/62743 Digital Signal Processing (Reexam)/62743 Digital Signal Processing (Reexam).md`. It now has, at the top, an **EXAM-DAY CHECKLIST** callout + a **problem → which-exam-set chart**. The hub is the single entry point — everything navigates from there.
3. **Open the exam skeleton:** `3.semester/DSP/EXAMS/F26.m` (has the same checklist at the top + the 3-question scaffold to fill in).
4. Follow the hub checklist (open old solutions as reference tabs, run the toolbox test, attack order Q3→Q2→Q1, `pretty F26.m` at the end).

There is **nothing left to build.** If the user is still prepping, help them practice (hints-first). If it's exam time, the assets below are everything they need.

### ✅ ASSET VERIFICATION (confirm these exist after pull)

| Asset | Path | State |
|---|---|---|
| Exam-day skeleton | `3.semester/DSP/EXAMS/F26.m` | ✅ checklist header + 3Q scaffold + appendix |
| Full reference solution | `3.semester/DSP/EXAMS/E25_new.m` | ✅ P1 (MATLAB-solved), P2, P3 all complete + verified |
| Previous solutions | `3.semester/DSP/EXAMS/{F24,F25_new,F23,F20,E19,E20,E22,F21}.m` | ✅ open as reference tabs |
| Q1 fallback cookbook | `Obsidian/.../Notes/Reference/Q1 via MATLAB cookbook.md` | ✅ every Q1 type → MATLAB + Danish Svar + panic protocol; slide-verified |
| Flows | `Notes/Flows/{LTI z-transform, Filter analysis and FFT, FIR window design} flow.md` | ✅ |
| Walkthroughs | `Notes/Walkthroughs/{E25,F24,F25,F23,F20} exam walkthrough.md` | ✅ worked twins for the chart |
| Cheat sheet | `Notes/Reference/DSP MATLAB helpers cheat sheet.md` | ✅ |
| Helpers | `3.semester/DSP/Helpers/` (FIR_fourier, FIR_window, MK_values, …) | ✅ `addpath` in F26.m |
| Publisher | `3.semester/DSP/pretty.bat` (+ `publish_pretty.py`) | ✅ `pretty F26.m` → styled PDF |

If any are missing after `git pull`: the commit didn't reach this PC — re-pull / check the branch.

### 📌 Exam format (confirmed from the E25 PDFs)

3 questions, weighted **~40 / 30 / 30** (E25 consolidated from the old 4×25%):
- **Q1 ≈ 40 %** — LTI / Z-transform: poles-zeros, H(z), ROC, stability, inverse-Z, **min-phase/all-pass**. *Weak area but biggest block.* → `Q1 via MATLAB cookbook`.
- **Q2 ≈ 30 %** — filter realisation (block diagram → H(z)) + sampling + FFT + filtering. *Strong.*
- **Q3 ≈ 30 %** — FIR design (Fourier + window). *Strong, formulaic.*

Attack order **Q3 → Q2 → Q1** (banks the strong ~60 % first). Time budget: Q3 60 min · Q2 70 min · Q1 80 min · 30 min review+publish.

### 🚩 The traps that matter (verified vs official solutions / NotebookLM)

- **Q1 "uden brug af MATLAB/Maple":** some Q1 sub-parts forbid MATLAB for Z-transform — a residuez-only answer there scores **0**. Write the analytic *setup* by hand (table pair, PFD ansatz, cover-up) even if unfinished. The cookbook's top danger box covers this.
- **`zplane(z,p)` needs COLUMN vectors** (row vectors are misread as `(b,a)` coefficients). Use `zplane(z(:),p(:))` or `zplane(b,a)`.
- **Diff-eq → `a` sign:** move all y-terms left; `y[n]=0.5y[n-1]+x[n]` ⇒ `a=[1 -0.5]`.
- **Zeros/poles at z=0:** `tf2zpk(b,a)` catches them; `roots(b)` on a z⁻¹ vector misses them.
- **FIR window method:** `FIR_fourier` returns the *ideal/rectangular* response only — for any non-rect window you MUST `.* FIR_window(...)`. (This dumped E25 3-5.)
- **Min-phase/all-pass:** zero z0 outside → reflect to `1/conj(z0)`; `Hap=G(1−z0 z⁻¹)/(1−(1/conj(z0))z⁻¹)`, G from `Hap(1)=1`; `Hmin=H/Hap`; `freqz(Hap)` flat. (Slide-verified.)
- **E25 P2 DF-II trap:** feedback taps after the 2nd & 4th delays → `A2=[1,0,0.4860,0,0.0177]`, not `[1,0.486,0.0177]`.

### Workflow conventions (the user corrected me on these — follow them)

- **Hints-first.** "let's do QX" → small hint, STOP, wait. Full walkthrough only on explicit "walk me through it / do it for me".
- **Verify against truth source.** Official `*student solutions*.pdf` = absolute truth (supersedes notebooklm for E25). NotebookLM: `C:\Users\Mads2\.claude\skills\notebooklm\scripts\nlm.bat ask "..." --notebook-id dsp` (re-`login` if `auth-status` says NOT AUTHENTICATED; it intermittently read-times-out — retry).
- **MATLAB comments in Danish**, real `øæå`. Answers as bare `%%` then `% *Svar N-M:* …` (renders as prose outside the code box). A computed value that *is* the answer → no semicolon. Never a static sentence in `fprintf`.
- **Obsidian notes use `[[wikilinks]]`**, not bare paths.
- After completing a question: log it into the relevant `… exam walkthrough.md`.
- DTU notation: `Ω`=analog rad/s, `ω`=digital rad/sample, `f`=normalized `F/Fs`. `freqs`→rad/s; `bilinear`/`freqz`→Hz.
- **Commits:** NEVER add `Co-Authored-By: Claude` or any AI mention (see memory).

### Known repo issue

Broken nested git repo at `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/Report` makes repo-wide `git add -A` abort. **Stage DSP work by explicit path.** Do not fix the broken submodule without explicit go-ahead (destructive).
