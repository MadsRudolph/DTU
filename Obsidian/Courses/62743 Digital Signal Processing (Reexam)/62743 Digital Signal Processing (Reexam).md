---
course: "62743"
course-name: "Digital Signal Processing (Reexam)"
type: home
cssclass: course-home
tags: [DSP, reexam, home]
aliases:
  - DSP Reexam
  - 62743 Reexam
---
# 62743 Digital Signal Processing (Reexam)

> [!info] Course Information
> **Course:** 62743 Digital Signal Processing
> **Status:** Re-exam preparation (failed E25)
> **Original exam:** December 11, 2025 (written, all aid, no internet)
> **Re-exam:** May 20, 2026 (exam code E2-B, written, all aid, no internet)
> **ECTS:** 5
> **Textbook:** Champagne & Labeau -- *Discrete Time Signal Processing*

> [!tip] Quick Links
> - [DTU Course Page](https://kurser.dtu.dk/course/62743)
> - [[DTU Study Path#Big-picture structure|Study path context]]
> - [[EXAM PREP|Original Exam Prep Master Note]]

> [!warning] Key Locations
> **Obsidian notes (archive):** `Archive/3rd Semester/DSP/`
> **MATLAB exercises & exams:** `C:\Users\Mads2\DTU\3.semester\DSP\`
> **Formula sheets:** `Archive/3rd Semester/DSP/Formulas/`
> **Past exams (11 sets):** `Archive/3rd Semester/DSP/Exercises/Exams/`

---

## Strategy

> [!abstract] Approach
> You already have **comprehensive materials** from E25: DSP Bible, 25+ formula sheets, 11 past exams, MATLAB helpers, and a Python toolbox. The goal is not to re-learn from scratch but to **close the gaps** that cost you the exam.
>
> **Identified weaknesses (from EXAM PREP.md):**
> - Partial fractions algebra under time pressure
> - Fast DTFT evaluation using properties
> - BLT pre-warping small details
> - ROC classification for mixed/tricky cases
> - FIR linear-phase indexing (off-by-one)
> - Time management during the exam
>
> **Strengths to maintain:**
> - MATLAB workflow
> - DFT/FFT understanding
> - Detailed notes and strong structure

---

## Preparation Plan (Feb 19 -- May 20, 2026)

**13 weeks** until the re-exam. The plan is split into **3 phases** designed to fit alongside your 30 ECTS semester. Expect ~3-4 hours/week on DSP, ramping up in the final weeks.

> [!warning] Deadlines
> **Re-exam: May 20, 2026** -- you have exactly 13 weeks. No slack for procrastination.
> **Registration:** April 1 -- April 15, 2026 (don't forget to sign up!)
> **Withdrawal deadline:** May 1, 2026

---

### Phase 1: Foundation Refresh (Weeks 8-12, Feb 19 -- Mar 22)

> [!goal] Goal: Rebuild core intuition, 1 topic per week (~3 hrs/week)

| Week | Date | Topic | Material | Done |
|------|------|-------|----------|------|
| 8 | Feb 19 | DT signals, convolution, LTI properties | Formulas Week 1-4, Slides Uge 01-04 | - [ ] |
| 9 | Feb 26 | DTFT & frequency response | Formulas Week 1-4, DSP Bible sec. DTFT | - [ ] |
| 10 | Mar 5 | Z-transform, ROC, inverse z | Formulas Week 5-7, DSP Bible sec. Z-transform | - [ ] |
| 11 | Mar 12 | H(z), poles/zeros, stability, min-phase | Formulas Week 5-7, Uge 4 Tirsdag exercises | - [ ] |
| 12 | Mar 19 | DFT/IDFT, circular conv, sampling, multirate | Formulas Week 5-7 + 12-13, Uge 12 exercises | - [ ] |

> [!tip] Phase 1 Method
> For each topic:
> 1. Read the formula sheet (~20 min)
> 2. Re-read the DSP Bible section (~30 min)
> 3. Do 2-3 exercises from that week's Ugeseddel on paper (~1-2 hr)
> 4. Check against solutions

---

### Phase 2: Filter Design Deep Dive (Weeks 13-17, Mar 23 -- Apr 26)

> [!goal] Goal: Master the exam-critical filter design topics (~4 hrs/week)

| Week | Date | Topic | Material | Done |
|------|------|-------|----------|------|
| 13 | Mar 23 | IIR filter structures (Direct Form I/II, cascaded) | Formulas Week 8-11, Slides Filter structures | - [ ] |
| 14 | Mar 30 | IIR design via BLT: LP (Butterworth) | Uge 10 Tirsdag.mlx, DSP Bible sec. IIR | - [ ] |
| 15 | Apr 6 | IIR design via BLT: HP/BP (Chebyshev) | Uge 10 Torsdag.mlx, E23 Problem 2 | - [ ] |
| 16 | Apr 13 | FIR design: Fourier method + windowing | Uge 11 Tirsdag/Torsdag.mlx, E23 Problem 4 | - [ ] |
| 17 | Apr 20 | Multirate + under-sampling | Uge 12 Tirsdag/Torsdag.mlx | - [ ] |

> [!tip] Phase 2 Method
> For each topic:
> 1. Re-run the MATLAB live script, understand every line (~1 hr)
> 2. Redo the exercise on paper without looking at the solution (~1 hr)
> 3. Solve 1 related exam sub-problem (~30 min)
> 4. Update your cheat sheet with any new insights

---

### Phase 3: Exam Drilling (Weeks 18-20, Apr 27 -- May 20)

> [!goal] Goal: Exam-speed practice and gap-closing (ramp up to ~6-8 hrs/week)

| Week | Date | Activity | Done |
|------|------|----------|------|
| 18 | Apr 27 | Solve E23 full exam (timed, 4 hrs) + error analysis | - [ ] |
| 19 | May 4 | Solve F24 full exam (timed, 4 hrs) + error analysis | - [ ] |
| 20 | May 11 | Solve F25 full exam (timed, 4 hrs) + weak-spot drilling | - [ ] |
| -- | May 18-19 | Final review: condense cheat sheets, redo worst sub-problems | - [ ] |
| -- | **May 20** | **EXAM DAY** | - [ ] |

> [!tip] Phase 3 Method
> For each practice exam:
> 1. Sit it fully timed (4 hrs, no internet, all other aid OK)
> 2. Grade yourself against solutions
> 3. Log errors in the mistake journal below (type, cause, fix)
> 4. Immediately redo any sub-problem you scored < 50% on
> 5. Update cheat sheet with new traps/tricks
>
> If time allows, squeeze in E24 or E19-E22 as bonus exams on weekends.

---

## Exam Day Checklist

- [ ] Printed/prepared cheat sheets (formula sheet + tricks & mistakes)
- [ ] MATLAB ready with all toolboxes (Communications, DSP System, Signal Processing, Symbolic Math)
- [ ] Helper scripts loaded: `DSP_sketch_generic_spectrum_template.m`, `plot_spectrum.m`, `zpgui.m`
- [ ] Past exam `.mlx` templates open for reference patterns
- [ ] Time plan: ~25% of time per problem, 10 min buffer for review

---

## Critical Topics Heatmap

| Topic | Priority | Exam Frequency | Confidence |
|-------|----------|----------------|------------|
| IIR via BLT (prewarp + design) | **Critical** | Every exam | To rebuild |
| FIR design (windowing/Fourier) | **Critical** | Every exam | To rebuild |
| Z-transform + ROC | **Critical** | Every exam | Medium |
| H(z) + stability + min-phase | **Critical** | Every exam | Medium |
| LTI + convolution | **Critical** | Every exam | Good |
| DFT/IDFT | **Critical** | Every exam | Good |
| FFT scaling + freq axis | **High** | Most exams | Good |
| Sampling/aliasing | **High** | Most exams | Medium |
| Allpass/min-phase decomposition | **High** | Often | Medium |
| Multirate (decim/interp) | **Medium** | Sometimes | To rebuild |

---

## Key Archive Resources

### Formula Sheets
- [[DSP Bible]] -- comprehensive reference (168+ sections)
- [[Formulas Week 1-4]] -- signals, LTI, DTFT, z-transform
- [[Formulas Week 5-7]] -- higher-order systems, DFT, sampling
- [[Formulas Week 8-11]] -- filter structures, IIR/FIR design
- [[Formulas Week 12-13]] -- multirate, under-sampling
- [[Exam Quick Reference OPTIMIZED]] -- condensed cheat sheet

### Past Exams (in `Archive/3rd Semester/DSP/Exercises/Exams/`)
| Exam | Set | Solution | MATLAB |
|------|-----|----------|--------|
| E19 | PDF | PDF | -- |
| E20 | PDF | PDF | -- |
| E21 | PDF | PDF | -- |
| E22 | PDF | PDF | -- |
| E23 | PDF | PDF + MD | E23.mlx |
| E24 | PDF | PDF | E24.mlx |
| E25 | PDF | PDF + MD | E25.mlx |
| F20 | PDF | PDF | -- |
| F21 | PDF | PDF | -- |
| F23 | PDF | PDF | -- |
| F24 | PDF | PDF + MD | -- |
| F25 | PDF | PDF + MD | F25.mlx |

### MATLAB Scripts (`C:\Users\Mads2\DTU\3.semester\DSP\`)
- `UGE10/Tirsdag.mlx` -- IIR LP BLT pipeline
- `UGE10/Torsdag.mlx` -- IIR HP/BP BLT pipeline
- `UGE11/Tirsdag.mlx` -- FIR LP/BP Fourier transform design
- `UGE11/Torsdag.mlx` -- Windowed FIR + frequency-sampling FIR
- `UGE12/Tirsdag.mlx` -- Multirate decimation/interpolation
- `UGE12/Torsdag.mlx` -- Under-sampling of AM bandpass signal

### Python Toolbox (`C:\Users\Mads2\DTU\3.semester\DSP\Assistant\`)
- `dsp_calc.py` -- 24 calculation functions
- `dsp_assistant.py` -- interactive problem solver
- `dsp_viz.py` -- visualization tools

---

## Mistake Journal

> [!failure] Log errors from practice exams here
> Format: `[Exam] [Problem] [Error type] [What went wrong] [Fix]`
>
> *(Fill this in during Phase 3)*

---

## Weekly Log

> [!note] Track your weekly progress here
> Format: `[Date] [Topic] [Time spent] [Confidence after: Low/Med/High]`
>
> *(Start logging from Week 8)*
