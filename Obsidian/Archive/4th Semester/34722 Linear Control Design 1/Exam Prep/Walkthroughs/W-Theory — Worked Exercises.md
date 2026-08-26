---
tags: [34722, lcd, exam, theory, worked]
course: 34722 Linear Control Design 1
exam_set: Theoretical Exercises (Papageorgiou) — 10 exercises
questions: 10
purpose: Step-by-step worked walkthrough of the 10 LCD1 Theoretical Exercises — built together in MATLAB, one at a time. The learning-oriented companion to the terse proofs in P7.
---
# W-Theory — Worked Exercises

> [!info] Exam Resources
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Terse proofs reference:** [[P7 — Theory Exercises (Worked Proofs & Derivations)]]
> - **Source PDF:** [[LCD1 Theory Exercises.pdf]] (Past Exams folder) + official Solutions manual
> - **Solve script:** `EXAM/Scripts/solved/solve_Theory.m` · **Practice yourself:** `EXAM/Scripts/practice/practice_Theory.m`
> - Run headless: `matlab -batch "solve_Theory"`

This is the *how we solved it* log — the narrative companion to [[P7 — Theory Exercises (Worked Proofs & Derivations)]] (which holds the compact derivations). Q1–Q3 and Q10 are **proofs**; Q4–Q9 are **exam-style numerics** (Q4, Q5, Q6, Q9 appeared on real exams).

| # | What it asks | Type |
|---|---|---|
| Q1 | Lead `C_D`: prove max-phase frequency & angle | proof |
| Q2 | 1st-order LPF metrics (`ω_c`, `ω_BW`, `t_r`, `t_s`) | proof |
| Q3 | P-Lag phase at `ω_c = N_i/τ_i` | proof |
| Q4 | Poles of `y⁗+9y‴+20ÿ=71u` | numeric |
| Q5 | `ess` with `K_P` in the feedback branch | numeric |
| Q6 | Nested loop — find `K₂` | numeric |
| Q7 | DC gain of telescoping cascade + unity fb | numeric |
| Q8 | Pick the feed-forward `F_d` | concept |
| Q9 | Two nested P-controllers — find `K_P` | numeric |
| Q10 | P-Lag cuts `ess` by `β`; `β→∞ ⇒ PI ⇒ ess→0` | proof |

---

<!-- Sections are added here one at a time as we solve each exercise together. -->
