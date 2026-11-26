# 34840 Offline Exam App

A self-contained, 100% offline exam companion for **34840 Fundamentals of Acoustics and Noise Control** (written exam Fri 11 Dec 2026, 4 hours, all aids allowed, no internet).

## How to Open on Exam Day (100% Offline)

Double-click [`exam-app.html`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/exam-app.html) in your file manager, or open it from a terminal:

```bash
chromium "/home/mads/DTU/5. Semester/Acoustics and Noise Control/Exam/app/exam-app.html"
```

Everything (all 15 problem solvers `T01`–`T15`, Quick Tools, KaTeX math renderer + all 12 WOFF2 math fonts, searchable Cheat Sheet, Worked 2022–2024 Part 1 solutions, all 45 Multiple-Choice questions from 2022–2024, and the Part 1 Hand-in PDF Builder + Checklist) is bundled inside [`exam-app.html`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/exam-app.html). It makes **zero** network requests and works directly from `file://` with Wi-Fi turned off. See [`DECISION.md`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/DECISION.md) for the trade-offs between a desktop/server app and a single offline HTML file.

## Quick Workflow During the Exam

1. **Find the right solver**: Press `/` (or `Ctrl+K`) and type keywords from the exam question (e.g. `"reverberation"`, `"A-weighted"`, `"two sources"`, `"tunnel"`, `"Helmholtz"`, `"deflection"`, `"double wall"`). Press `Enter` to jump straight to the matching solver or preset.
2. **Check constants**: The top bar defaults to the exam standard $\rho = 1.2\text{ kg/m}^3$ and $c = 343\text{ m/s}$ ($\rho c = 411.6\text{ Pa}\cdot\text{s/m}$). Edit them if a problem specifies different values (e.g. $c = 344\text{ m/s}$ or Venus).
3. **Enter the given numbers**: Type the problem's numbers into the solver form. Watch the **inline decision banners** ($2\pi$ vs $4\pi$, peak vs RMS, coherent vs incoherent, Sabine vs Eyring, $\sqrt{2}f_0$, $f_c$).
4. **Copy or export Part 1 working**: Click **Copy Worked Solution** to copy the step-by-step formula $\to$ substituted numbers $\to$ result with units into your Part 1 document, or click **+ Add to Part 1 Hand-in Builder** to collect your answers and print/save them as one PDF.

## How to Run the Automated Tests (No Network)

```bash
cd "/home/mads/DTU/5. Semester/Acoustics and Noise Control/Exam/app"
node test.js
```

`test.js` runs:
- All **116 numerical checks** from `../toolkit/run_all_checks.m` against [`src/physics.js`](file:///home/mads/DTU/5.%20Semester/Acoustics%20and%20Noise%20Control/Exam/app/src/physics.js) with identical tolerances (`116/116` pass).
- Extra exam checks (2022 P2 octave bands, Week 12 S1.1 party wall A-weighted level).
- Integrity checks for all 15 solver templates, 45 multiple-choice questions (2022–2024), and base64-inlined KaTeX assets.
- A headless Chromium `file://` check inside an isolated Linux network namespace (`unshare -rn`, networking disabled) confirming live DOM computation and KaTeX rendering.

## How to Rebuild `exam-app.html`

If you edit any file in `src/`:

```bash
cd "/home/mads/DTU/5. Semester/Acoustics and Noise Control/Exam/app"
node build.js
node test.js
```

No `npm install` or internet connection is required—`build.js` uses only built-in Node (`fs`, `path`) and the local `vendor/katex/` directory.
