---
tags: [34722, lcd, exam, hub, MOC]
course: 34722 Linear Control Design 1
purpose: Single entry point for the 34722 multiple-choice exam — fast index from "what is the question asking" to the pattern that cracks it
exam: Multiple-choice, Tue 2-June-2026
---
# 00 LCD1 — Exam Hub

**Exam:** 34722 Linear Control Design 1 · ⚠️ **ORAL RE-EXAM: Mon 25 August 2026, 15 minutes, NO aids** — questions in the style of the written exam, solved and explained at the board. (Ordinary MCQ attempt Tue 2-June-2026 scored 3/20 — see [[W-F26 — Worked Exam (MCQ)]].)
The question PATTERNS below are unchanged — but prep is now derive/sketch/explain from memory, with the solver as sparring partner (its Oral Trainer mode), never as the answer machine.

> [!important] ▶️ Active plan
> **[[RE-EXAM — August 2026 Study Plan]]** — 12-day oral-format plan (blank-sheet derivations, sketch drills, explain-aloud sessions, mock orals). Start there.

> [!info] Quick Links
> - Formula reference (don't duplicate, link): [[Exam Formula Cheat-Sheet]]

---
## 🔎 Fast index — "the question shows me…" → go to

| The question gives you… | Pattern | Note |
|---|---|---|
| A block diagram / state-space / ODE / RLC → find `G(s)` or poles | block reduction, `C(sI−A)⁻¹B+D`, linearization | [[P1 — Transfer Functions, Block Reduction & Modelling]] |
| A **Bode plot** → identify poles/zeros or pick `G(s)`; DC gain; bandwidth | asymptote rules, RHP-zero trap, BW read-off | [[P2 — Frequency Response & Bode Read-Off]] |
| "For which `K` is the closed loop stable?" / GM / PM / Nyquist | stable-vs-**unstable**-plant inversion, `Z=N+P`, Routh | [[P3 — Stability, Margins & Nyquist]] |
| Overshoot, ζ, settling/rise/peak time, step-response shape | `Mp↔ζ`, find-K-for-spec, `ωn=2π/T′` | [[P4 — Second-Order Specs (Time & Frequency)]] |
| Steady-state error, system type, find `KP` from `ess`, disturbance | type table, `KP=(1/ess−1)/G(0)`, `Ged=−Gyd` | [[P5 — Steady-State Error & System Type]] |
| "Design a P / Lead / PI-Lead / prefilter / feedforward" | **phase-budget equation**, `τ_d=1/(ωc√α)`, prefilter, `F=D/G₁` | [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]] |
| A proof / derivation, or the theory-exercise numerics | the 10 worked theory exercises | [[P7 — Theory Exercises (Worked Proofs & Derivations)]] |

---

> [!tip] 🎯 High-Value Patterns
> Drill these first — they carry the Q11–Q19 block on every recent exam:
> 1. **PI-Lead phase budget:** $-180^\circ + \gamma_M = \phi_G + \phi_{Lead} + \phi_{PI}$ $\to$ solve for **$\alpha$**, **$N_i$**, or **$K_P$**. ([[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]])
> 2. **Stable-K range inversion:** Stable plant $\Rightarrow 0 < K < GM$; **unstable plant (RHP pole) $\Rightarrow K > 1/|x_{crossing}|$** for the CCW encirclement. ([[P3 — Stability, Margins & Nyquist]])

---
## 🧮 Verified solve-scripts (Danish-commented, MATLAB R2025a)

Each reproduces the **official facit** of a past exam. Path: `4. Semester/Linear Control Design/EXAM/Scripts/solved/`. Run headless: `matlab -batch "solve_S20"`.

| Exam | Script | Notes |
|---|---|---|
| S20 (11 Q) | `solve_S20.m` | Q1 linearization, Q5 `Mp→ζ`, Q9 P-design, Q10–Q11 Lead |
| S21 (10 Q) | `solve_S21.m` | Q4 stable-K, Q6 P-for-PM, Q9 find-K-for-overshoot |
| F22 (20 Q) | `solve_F22.m` | ⚠️ Q19 uses **α=0.01** (problem misprints 0.001) → facit 3.4154 |
| ReExam F22 (10 Q) | `solve_ReExam_F22.m` | ⚠️ Q4 build char-poly by hand (minreal lies); Q8 shape-based |
| REExam F21 (20 Q) | `solve_REExam_F21.m` | ⚠️ Q17 reads **φ_G=−151.064°** (not −15) → Ni=1.57 |
| Theory Exercises (10 Q) | `solve_Theory.m` | Verifies Q1–Q3/Q10 proofs numerically + Q4–Q9 numerics ({0,0,−4,−5}, 0.2, 79.17, 0.8, 4) |

---
## 📝 Practice loop — solve a paper, then check yourself

Three artifacts per exam set. Skeleton has the givens pre-loaded and `NaN; % TODO` blanks; fill them, run, then run the `solved/` script to compare. The **Worked Exam** note has every question's approach + embedded MATLAB graph + facit + planted trap.

| Exam | Practice skeleton | Worked-exam note |
|---|---|---|
| F22 (20 Q) | `practice/practice_F22.m` | [[W-F22 — Worked Exam]] |
| ReExam F22 (10 Q) | `practice/practice_ReExam_F22.m` | [[W-ReExam F22 — Worked Exam]] |
| Theory Exercises (10 Q) | `practice/practice_Theory.m` | [[P7 — Theory Exercises (Worked Proofs & Derivations)]] |
| **F26 (sat exam, 20 Q)** | — | [[W-F26 — Worked Exam (MCQ)]] — my attempt (3/20), all 20 worked + traps |
| **F26 — solve in the app** | — | [[W-F26 — Solve It With The LCD1 Solver]] — click-by-click for every question |

---

> [!warning] ⚠️ The planted traps (lose-a-point-if-you-blink)
> - **Degrees vs radians** — `arcsin/arctan` give radians; the phase budget is in degrees.
> - **dB vs linear** — always `10^{dB/20}` before plugging in (`KP`, `Mp`, `G(0)`).
> - **Unstable plant** flips the stable-`K` interval to `K > K_min`.
> - **RHP zero**: magnitude rises `+20 dB/dec` but phase *drops* `−90°`.
> - **`Mp` is relative to the final value**: `Mp=(peak−yss)/yss`.
> - **`Ged=−Gyd`** $\to$ static disturbance error is the *negative* of the read-off.
> - **F22 Q19 α typo** (0.001 vs 0.01) and **REExam Q17 φ_G misread** (−151 vs −15) — both documented in [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]] §Traps.

---

> [!todo] ✅ Readiness checklist
> - [ ] Can I read poles/zeros off a Bode plot and spot a **RHP zero** by the phase? ([[P2 — Frequency Response & Bode Read-Off]])
> - [ ] Can I state the stable-`K` interval for **both** a stable and an unstable plant? ([[P3 — Stability, Margins & Nyquist]])
> - [ ] Can I invert overshoot↔ζ and recall `ζ=0.5→16%, 0.7→5%, √2/2→4.3%`? ([[P4 — Second-Order Specs (Time & Frequency)]])
> - [ ] Can I find `KP` from a required `ess`, converting `G(0)` dB→linear? ([[P5 — Steady-State Error & System Type]])
> - [ ] Can I run the **phase-budget equation** three ways (α, Ni, KP)? ([[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]])
> - [ ] Do I know the prefilter `τ_f=(1/ωp)√(Mp²−1)` and the **proper, fast** feedforward `F_d`? ([[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]], [[P7 — Theory Exercises (Worked Proofs & Derivations)]])
> - [ ] Have I re-run all four solve-scripts and matched the facit?
> - [ ] Every conversion **dB→linear / deg↔rad** done before the formula, not after?
