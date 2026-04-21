---
course: "62743"
course-name: "Digital Signal Processing (Reexam)"
type: home
tags: [DSP, reexam, home]
aliases:
  - DSP Reexam
---
# 62743 DSP Re-exam -- Hub

> [!info] Exam
> **Date:** Wednesday 20 May 2026 -- code **E2-B**
> **Format:** 4 hours, written, all aid allowed, no internet
> **Room/time:** `eksamensplan.dtu.dk` publishes ~1 week before (Wed 13 May)

---

## How this works

1. Open the next exam in the order below.
2. Open its MATLAB skeleton in `C:\Users\Mads2\DTU\3.semester\DSP\EXAMS\`.
3. Attempt it (talk to me live -- I walk you through anything you're stuck on, especially the DFT / DTFT / z-transform stuff).
4. When done, copy `Exam Evals/_template.md` to `Exam Evals/<exam>.md` and we fill it in together.
5. Tick the box below. Move to the next one.

That's the whole system.

---

## Exam schedule (in order)

Start with the simpler / older exams. Save the well-annotated "golden" ones for later when you know what to look for. E25 last -- the one you failed, fresh attempt after 4 weeks of drilling.

- [ ] **1. F20** -- first one, we go slow and I explain everything. MATLAB: `EXAMS\F20.m`
- [ ] **2. F21** -- MATLAB: `EXAMS\F21.m`
- [ ] **3. F23** -- MATLAB: `EXAMS\F23.m`
- [ ] **4. E19** -- MATLAB: `EXAMS\E19.m`
- [ ] **5. E20** -- MATLAB: `EXAMS\E20.m`
- [ ] **6. E22** -- MATLAB: `EXAMS\E22.m`
- [ ] **7. E23** (golden -- has MATLAB walkthrough + md notes) -- MATLAB: `EXAMS\E23.mlx`, ref [[E23 Exam]]
- [ ] **8. F24** (golden -- has md notes) -- MATLAB: `EXAMS\F24.m`, ref [[F24 Exam]]
- [ ] **9. E24** -- MATLAB: `EXAMS\E24.mlx`
- [ ] **10. F25** (golden) -- MATLAB: `EXAMS\F25.mlx`, ref [[F25 Exam]]
- [ ] **11. E25** (the one you failed -- final attempt) -- MATLAB: `EXAMS\E25.mlx`, refs: [[E25 Exam]], `62743 E25 Exam with student solutions.pdf`

Exam PDFs + solution PDFs: `Obsidian/Archive/3rd Semester/DSP/Exercises/Exams/`

---

## Canonical flow notes (built as we work through exams)

Dedicated deep-dive reference notes for recurring exam patterns. Revisit any of these mid-exam when the pattern comes up.

- [[LTI z-transform flow]] -- diff eq to H(z) to poles/zeros/stability to h[n] to y[n] to energy (every exam has this)
- *(more as we hit new patterns -- FIR design, FFT/DFT, IIR BLT, multirate)*

---

## Good-to-know references

Pull these up when a topic comes up in an exam and we need to fill a gap.

**The master reference:**
- [[EXAM PREP]] -- topic map, heatmap, common error patterns
- [[DSP-Bible]] -- full reference, all topics

**Condensed cheat sheets:**
- [[Exam_Cheat_Sheet_OPTIMIZED]]
- [[Exam_Quick_Reference_OPTIMIZED]]

**Formula sheets by topic:**
- [[Week 1-4]] -- DT signals, LTI, DTFT, z-transform
- [[Week 5-7]] -- DFT, sampling
- [[Week 8-11]] -- filter structures, IIR + FIR design
- [[Week 12-13]] -- multirate, under-sampling

**Topic guides (weak areas per your self-assessment -- DFT side):**
- [[FIR_Windowing_Complete_Guide]]
- [[Multirate Digital Signal Processing]]

**Weekly exercise notes (already worked through once):**
- [[Uge 4 Tirsdag]] -- LTI + H(z)
- [[Uge 10 - Tirsdag]], [[Uge 10 - Torsdag]] -- IIR BLT
- [[Uge 11 - Tirsdag]], [[Uge 11 - Torsdag]] -- FIR design
- [[Uge 12 - Tirsdag]], [[Uge 12 - Torsdag]] -- multirate

---

## Known weak spots (from failed E25)

Not a study list -- just flags so I know what to explain harder when they come up in an exam problem:

1. Partial fractions under time pressure
2. Fast DTFT via properties (not from definition)
3. BLT pre-warping details (Hz vs rad/s)
4. ROC classification
5. FIR linear-phase indexing (K = M/2)
6. Time management

Self-assessed: **filter design OK, DFT / DTFT / z-transform weak.**

---

## MATLAB setup
- R2025a + Signal Processing Toolbox confirmed
- Helpers folder on path: `C:\Users\Mads2\DTU\3.semester\DSP\Helpers\`
- Optional (install via Add-Ons if wanted): DSP System, Communications, Symbolic Math
