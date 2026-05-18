# CLAUDE.md — repo handoff

This file is auto-loaded by Claude Code and travels with `git pull`. It records **where to pick up** the active work so a fresh session on any PC can continue seamlessly.

---

## ACTIVE WORK: 62743 DSP Re-exam prep

**Goal:** Prepare for the DTU 62743 Digital Signal Processing re-exam (exam Wed 20 May 2026, code E2-B, 4 h, all aids, no internet).

### 📌 Exam format — CONFIRMED from the PDFs (read 2026-05-18)

The re-exam mirrors the **E25 (Dec 2025)** sitting it re-examines: **3 questions, weighted ~40 / 30 / 30** (not the old 4×25%).
- **Q1 ≈ 40 %** — LTI / Z-transform by hand: poles-zeros, H(z), ROC, stability, inverse-Z (partial fractions), **min-phase/all-pass**. *User's weak area, but the single biggest block.*
- **Q2 ≈ 30 %** — filter realisation (block diagram → H(z)) + sampling + FFT + filtering. *Strong.*
- **Q3 ≈ 30 %** — FIR design (Fourier + window method). *Strong, formulaic.*

Evidence: re-exam (F) is a parallel form of the ordinary (E) it follows — same 6-archetype pool, same difficulty, renumbered. E23(4Q)→F24(4Q), E24(4Q)→F25(4Q) tracked; E25 consolidated to 3Q. Full analysis + table in the Obsidian hub (see below).

### ▶️ PICK UP HERE (next action)

**Practice E25 — full re-solve.** Working file `3.semester/DSP/EXAMS/E25_new.m` is now fully formatted (3 problems, all sub-cells, `Svar` answer blocks pre-placed, dividers cleaned). The user fills code in the work areas + replaces each `% *Svar N-M:* TODO`, then runs `pretty E25_new.m`. Truth source: `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/Solutions/62743 E25 Exam student solutions.pdf` + notebooklm.
🚩 **Key trap (likely cause of the fail):** P2's DF-II feedback taps sit after the **2nd and 4th** delays → `A2 = [1, 0, 0.4860, 0, 0.0177]` (denominator `1+0.486z⁻²+0.0177z⁻⁴`), NOT `[1,0.486,0.0177]`. Skeleton already corrected; the vault `E25 Exam.md` writeup has this WRONG — trust the official PDF.

Hints-first: give a small hint, let the user attempt, walk through only on request.

### Strategy (UPDATED — supersedes the old "filters alone = pass")

Filter-first still holds as **ordering** (do Q3 then Q2 ≈ 60 %, the strong areas, first), but it is **no longer sufficient to pass alone** — Q1 is 40 %. Q1's early sub-parts (pole-zero plot via `zplane`, write H(z), ROC, stability) are MATLAB-assistable, ~half of Q1's marks, pure recipe — **never leave them blank**. **Min-phase/all-pass is recurring (E24 Q3, E25 Q1) — drill it, do not defer it.** Time budget (4 h): Q3 ≈ 60 min · Q2 ≈ 70 min · Q1 ≈ 80 min · 30 min review+publish.

### Publishing workflow (NEW — built 2026-05-18)

Exam submission = "kommenteret kode"; examiners run the `.m`. Tooling in `3.semester/DSP/`:
- **`pretty <exam>.m`** (`pretty.bat` → `publish_pretty.py`, deps: miniconda `beautifulsoup4`+`pygments`, Edge for PDF). Runs MATLAB `publish` (forces white figures via the settings *light* theme), then re-renders → clean single-file HTML + A4 PDF in `EXAMS/html/<stem>_pretty.pdf`: syntax highlighting, collapsed RCOND warnings, stripped scaffolding, green ✓ **Svar** callouts. Flags: `--no-matlab`, `--open`, `--name/--studentid` (default Mads Rudolph / s246132). Auto-falls-back to a timestamped PDF if the target is open in a viewer.
- **Result-presentation convention** (apply to every exam `.m`):
  - Conclusions / "FIR vs IIR fordi…" → a **bare `%%`** then `% *Svar N-M:* …` → renders as prose **outside** the code box, works in raw MATLAB too.
  - A computed value that *is* the answer → **no semicolon** (`poler = roots(a)`) or value-bearing `fprintf('%.2f dB', x)`.
  - Never a static sentence in `fprintf('...')` (duplicates code + echoed output).
- `F25_new.m` refactored to this convention; `E25_new.m` formatted with it; **`F26.m`** = blank exam-day skeleton (3-question, copy & fill on the day).

### Status

| File | State |
|---|---|
| `EXAMS/F24.m` | ✅ Q2/Q4 complete + walkthrough |
| `EXAMS/F25_new.m` | ✅ Q2/Q4 complete; **refactored to Svar convention** |
| `EXAMS/F23.m` | scaffolded only; deferred |
| `EXAMS/E25_new.m` | **active** — fully formatted skeleton, Svar blocks ready, P2 DF-II trap fixed; **practice next** |
| `EXAMS/F26.m` | ✅ blank reexam skeleton (3-question, exam-day template) |

### Obsidian assets (the in-exam navigator)

`Obsidian/Courses/62743 Digital Signal Processing (Reexam)/`:
- **`62743 Digital Signal Processing (Reexam).md`** — rebuilt as an **in-exam triage hub**: "what kind of problem is this?" → wikilink to a flow. Has the Re-exam-vs-ordinary analysis + 3-question strategy + Publishing section.
- `Notes/LTI z-transform flow.md` (Q1), **`Notes/FIR window design flow.md`** (Q3, new), **`Notes/Filter analysis and FFT flow.md`** (Q2, new), `Notes/F24|F25|F23 exam walkthrough.md`, `Notes/DSP MATLAB helpers cheat sheet.md`.
- Exam + solution PDFs: `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/` (gitignored — must exist locally / via Drive sync). E25 set: `Archive/3rd Semester/DSP/62743 E25 Exam v3.pdf`.

### Workflow conventions (the user corrected me on these — follow them)

- **Hints-first.** "let's do QX" → small hint, STOP, wait. Full walkthrough only on explicit "walk me through it / do it for me".
- **Verify against truth source.** `*student solutions*.pdf` = absolute truth. `notebooklm` skill: `C:\Users\Mads2\.claude\skills\notebooklm\scripts\nlm.bat ask "..." --notebook-id dsp` (re-`login` if auth expired — it was back up 2026-05-18).
- **MATLAB comments in Danish**, real `øæå` (never `oe/ae/aa`). Answers as `Svar` blocks (see Publishing).
- **Obsidian notes use `[[wikilinks]]`**, not bare paths.
- After completing a question: log it into the relevant `... exam walkthrough.md`, then continue.
- DTU notation: `Ω` = analog rad/s, `ω` = digital rad/sample, `f` = normalized `F/Fs`. `Ω = 2πF`, `ω = ΩT = 2πf`. `freqs`→rad/s; `bilinear`/`freqz`→Hz.

### Key reusable patterns (verified 2026-05-18 vs NotebookLM + E25 answers)

- **FIR window design (Q3):** `Fc=(Fpass+Fstop)/2`, `wc=2πFc/Fs`, `ΔF=|Fstop−Fpass|/Fs`. Window from stopband As, `Ntaps`:
  Rect 21 dB `0.9/ΔF` · Hanning 44 dB `3.1/ΔF` · Hamming 53 dB `3.3/ΔF` · Blackman 74 dB `5.5/ΔF` (round up to odd; `M=Ntaps−1`, `K=M/2`). MATLAB `sinc` has π baked in.
- **Min-phase / all-pass (recurring Q1):** zero outside at `z0` → in `Hmp` replace `(1−z0 z⁻¹)` with `(1−(1/conj(z0))z⁻¹)`; `Hap = G·(1−z0 z⁻¹)/(1−(1/conj(z0))z⁻¹)`, fix `G` from `Hap(1)=1`, `Hmp` carries `1/G`; `freqz(Hap)` → flat magnitude.
- **IIR via BLT pipeline:** spec → prewarp `Ω=(2/Ts)tan(πf)` → order `n=ceil(log10((10^(0.1·As)-1)/ε²)/(2log10(νs)))` → prototype (appendix) → `lp2xx` → `bilinear` → `freqz` dB. LP `νs=Ωs/Ωp`; **HP inverted `νs=Ωp/Ωs`**; BP/BS double order.
- **Classmate helpers** `3.semester/DSP/Helpers/`: `n_value` (⚠️ Chebyshev n=4 entry buggy), `time_vec`, `frequency_vec`, `FIR_fourier`, `FIR_window`, `MK_values`.

### Known repo issue

A broken nested git repo at `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/Report` makes repo-wide `git add -A` abort. **Stage DSP work by explicit path.** Do **not** fix the broken submodule without the user's explicit go-ahead (destructive).
