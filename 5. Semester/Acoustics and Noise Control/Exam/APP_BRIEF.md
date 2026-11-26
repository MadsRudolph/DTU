# Brief: a streamlined exam app for 34840 (Fundamentals of Acoustics and Noise Control)

## Why
Mads has the written exam **Fri 11 Dec 2026, 4 h, all aids allowed, NO INTERNET**. Part 1 = 2–3 calculation problems (handed in as one PDF), part 2 = 15 multiple-choice questions. The MATLAB toolkit and notes already exist, but going through 15 MATLAB templates during an exam is too slow and clumsy. He wants **one app** that makes the exam fast: pick the problem type, type the given numbers, get every step and the answer, copy it into the hand-in.

## Hard constraints
- **Must work 100 % offline** on exam day: open by double-clicking a local file (or one local command). No CDN, no web fonts from the internet, no npm install on exam day. Bundle everything (e.g. KaTeX) into the build output. Test it with the network off (e.g. load from `file://`).
- Lives in `/home/mads/DTU/5. Semester/Acoustics and Noise Control/Exam/app/` (source + build). Produce a single self-contained `exam-app.html` (everything inlined) as the main deliverable.
- Plain, conversational English in the UI. No AI attribution anywhere. Do **not** commit or push (the parent session does that). Do not touch `5. Semester/Study Bench/` or the existing toolkit/notes files (read them only).
- Do not start other agents.

## Sources of truth (read these first)
- MATLAB toolkit (verified physics, 116/116 checks pass): `../toolkit/T01_…m` … `T15_…m`, `../toolkit/README.md` (which template for which question type), `../toolkit/run_all_checks.m` (the expected values for every pre-filled example).
- Cheat sheet: `/home/mads/DTU/Obsidian/Courses/34840 Fundamentals of Acoustics and Noise Control/Exam Prep/Cheat Sheet - 34840.md`
- Worked old exams + topic frequency: `…/Exam Prep/Old Exams 2022-2024 - Worked.md`
- Exam-day checklist: `…/Exam Prep/Exam Day Checklist - 34840.md`
- Lecture/week notes: `…/Lecture Notes/Lecture 1..12 - *.md`, `…/Exercises/Work/Week 1..12 - *.md`
- Constants used by the exam paper: c = 343 m/s, ρ = 1.2 kg/m³ (check the cheat sheet for the decision table).

## What the app should do (streamlined first, complete second)
1. **Problem solvers** — one per toolkit template (plane-wave reflection, tube driven at the end, levels/adding/Leq, octave bands + A-weighting, intensity/power/SWR, monopole near field/power, two sources/wall/dipole, loudspeaker, room modes, reverberation/diffuse field, absorbers, ERB/masking, Greenwood/ABR, vibration isolation, sound insulation). Each: a short form with the givens (units shown, sensible defaults = the toolkit's pre-filled real exam problem), live results, and a **step-by-step worked solution** (formula → numbers substituted → result with units) that can be copied as plain text or exported, ready for the part-1 PDF. Flag the classic decision points inline (2π vs 4π, rms vs amplitude, coherent vs incoherent, Sabine vs Eyring, below/above √2·f0, below/above f_c …).
2. **"Which solver?" finder** — a search box / keyword matcher: type words from the question ("reverberation time", "transmission loss", "A-weighted", "two loudspeakers") → jump to the right solver and the relevant cheat-sheet section.
3. **Quick tools**: dB add/subtract/average (coherent & incoherent), Pa↔dB, W/m²↔dB, W↔dB, octave/third-octave band lookup with A/C-weighting, λ/k/ka from f and size, unit converter.
4. **Cheat sheet**, searchable, formulas rendered (KaTeX bundled).
5. **Multiple-choice drill**: all part-2 questions from 2022–2024 with answers and one-line reasons (from the worked old-exams note), plus a "by topic" filter.
6. A **final-check list** panel (the exam-day checklist: time plan, units, rounding, PDF export).

Keep the UI calm and fast: keyboard-friendly, large readable numbers, light and dark theme, works on a laptop screen; minimal clicks from "read question" to "answer + working".

## Verification (required)
- Write automated tests (Node, no network) that run every solver with the toolkit's pre-filled inputs and assert the same values `run_all_checks.m` asserts (same tolerances). All must pass. Report the pass count.
- Open the built `exam-app.html` from `file://` with networking unavailable and confirm it renders and computes (headless browser if available, otherwise a JS DOM test; say which).
- Write a short `README.md` in `app/`: how to open it on exam day, how to rebuild, how to run the tests.

## Report
When done or stuck, report with `hc send t10 "<summary: files, test pass count, offline check result, anything not verified>"`. Put a longer report in `app/REPORT.md` and send its path.
