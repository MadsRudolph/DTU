# 34840 Offline Exam App — Build & Verification Report

## Overview

Built a single-file, 100% offline exam application at [`exam-app.html`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/exam-app.html) (811 KB, zero external dependencies) for **34840 Fundamentals of Acoustics and Noise Control**.

## Files Created in `Exam/app/`

- [`DECISION.md`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/DECISION.md) — Architectural comparison (single self-contained offline HTML vs. local Python/Node server vs. Tauri/Electron/Qt desktop app on Arch Linux/Hyprland) and rationale for choosing the single self-contained offline HTML deliverable.
- [`exam-app.html`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/exam-app.html) — Self-contained single-file deliverable (all HTML, CSS, KaTeX JS/CSS, 12 base64-inlined WOFF2 math fonts, physics engine, 15 solver forms, 45 MC questions, searchable cheat sheet, and Part 1 hand-in builder inlined).
- [`src/physics.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/src/physics.js) — Pure JS physics engine implementing templates `T01` through `T15`, complex arithmetic, Bessel $J_1(x)$, Table 1.3.2 A/C-weighting interpolation, step-by-step worked solution generation, and dynamic sanity warnings.
- [`src/solvers_meta.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/src/solvers_meta.js) — Form schemas, units, presets for past exam & exercise problems, keywords, and inline decision-point banners for `T01`–`T15`.
- [`src/mc_data.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/src/mc_data.js) — All 45 Part-2 multiple-choice questions from 2022, 2023, and 2024 with options A–D, official answers, worked one-line reasons, classic traps, and solver links.
- [`src/cheatsheet_data.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/src/cheatsheet_data.js) — Searchable formula cheat sheet (Sections 0–11), all 8 worked Part-1 problems from 2022–2024, and the exam-day time plan & checklist.
- [`src/ui.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/src/ui.js) & [`src/styles.css`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/src/styles.css) — UI controller (universal `/` and `Ctrl+K` finder, live solver cards, Quick Tools, Cheat Sheet, MC Drill, Hand-in PDF Builder, Light/Dark theme, print stylesheet).
- [`build.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/build.js) — Zero-dependency Node bundler that inlines KaTeX fonts, CSS, and JS modules into `exam-app.html`.
- [`test.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/test.js) — Automated Node + headless Chromium offline test suite.
- [`README.md`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/README.md) — Exam-day usage, rebuild, and testing guide.

## Verification Results

1. **MATLAB Toolkit Parity (`116 / 116` checks passed)**:
   - `node test.js` runs every solver (`T01`–`T15`) with the toolkit's pre-filled inputs and asserts the exact 116 expected values and tolerances from `../toolkit/run_all_checks.m`.
   - All **116 of 116** toolkit checks pass, plus 2 extra exam checks (2022 P2 octave bands `-Inf / 71.9 / 62.73 / 46.53 dB` and Week 12 S1.1 party wall `33.7 dB(A)`).
2. **Offline `file://` Headless Browser Verification**:
   - Verified static HTML contains zero external `http://` or `https://` URLs and all 12 KaTeX `.woff2` fonts are base64-inlined.
   - Executed `unshare -rn chromium --headless --no-sandbox --disable-gpu --dump-dom file:///.../exam-app.html` (inside a network-isolated Linux namespace with no network interfaces).
   - Confirmed `exam-app.html` loads cleanly from `file://`, computes live solver results (`0.89 Pa`, `0.86 Pa`, `29.5 dB`), renders KaTeX `.katex-mathml` formulas, and populates all 15 solvers, 45 MC questions, and the Part 1 Hand-in Builder.
3. **Anything Not Verified**:
   - Everything required by `APP_BRIEF.md` has been verified offline.
