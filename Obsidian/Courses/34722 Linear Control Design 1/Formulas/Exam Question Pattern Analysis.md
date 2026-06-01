# 34722 LCD1 — Exam Question Pattern Analysis

> Built by reading every past exam in `…/Exercises/Solutions/Past Exams/` (E15, S20, E20, ReExam F21, S21, E21, F22, ReExam F22, E22, E23, E25 + E25 Test) and tagging the topic of every question. Use it to prioritise drilling for the **multiple-choice exam, Tue 2 June 2026.**

---

## 0. The format changed — know which era you're practising

| Era | Exams | Style |
|---|---|---|
| **Old** | E15, S20, E20, ReExam F21 | Longer, partly **computational/derivation** (linearize ODE, invert Laplace, derive y(t)) |
| **Recent (your format)** | E21, E22, E23, E25, E25 Test | **Pure multiple-choice**, nearly identical skeleton year to year |

➡️ **E21 → E25 are your highest-fidelity practice.** Older sets are still good for the underlying topics, but the question *style* has settled.

DTU naming: **E** = December (efterår), **S/F** = May/June (forår).

---

## 1. The recurring exam skeleton (E21–E25 are near carbon copies)

Tick each block as you practise it on each exam:

- [ ] **1. Modelling** — state-space / coupled ODEs → transfer function G(s); sometimes linearization of a nonlinear ODE
- [ ] **2. System type & order** — count integrators / poles at origin → type 0/1/2 and order
- [ ] **3. Block-diagram reduction** — open-loop *and* closed-loop TF; static loop gain K₀
- [ ] **4. Controller-type ID** — classify a given C(s) as P / PI / PD / P-lead / PI-lead
- [ ] **5. Bode read-off** — poles & zeros from asymptotes; type/order; static gain; **gain & phase margins**; **crossover ω_c and π-frequency ω_π**
- [ ] **6. Steady-state error** — e_ss to a **step at the reference** *and* to a **step at the disturbance** (sometimes a ramp)
- [ ] **7. Controller design** — **P-controller for target phase margin (almost always 60°)** → then **Lead/P-lead** → then **PI / PI-lead**
- [ ] **8. Concept** — bandwidth vs phase-margin tradeoff; non-minimum-phase / RHP-zero implications

---

## 2. Topic frequency across all 11 exam sets

### Backbone — appears on essentially every exam (drill hardest)
| Topic | Coverage |
|---|---|
| **Bode plot read-off** (poles/zeros, type/order, DC gain) | all 11 |
| **Block-diagram reduction** → open/closed-loop TF | all 11 |
| **P-controller design for target phase margin** | ~9 — target is **60° far more often than not** (E23, E25, E25-Test, S20 = 60°; F22 = 40°) |
| **Gain margin & phase margin read-off** | ~9 |

### Very common — expect 1–2 questions
- **Crossover ω_c & π-frequency ω_π** from Bode — recent staple (E21, E22, E23, E25)
- **System type & order** classification — heavy in recent exams
- **Steady-state error** — step-at-reference *and* step-at-disturbance both appear; ramp in E22 & ReF22
- **Second-order specs**: overshoot ↔ ζ, ω_n, settling time — E15, S20, E20, ReF21, S21, F22, ReF22, E22
- **Lead / P-lead design** (often α = 0.1) — S20, E23, E25, E25-Test, E15
- **TF from state-space / linearization** — S20, E20, E22, E23, E25, ReF22

### Rotating — know them, lower priority
- **PI / PI-lead design** — S20, ReF21, E21, E25 (often multi-part when present)
- **Nyquist stability** (encirclements, gain for marginal stability) — S20, ReF21, S21; faded in newest MC exams
- **Controller-type identification** — ReF21, E21, E23, E25
- **Bandwidth** & bandwidth-vs-phase-margin tradeoff — E15, S20, E25-Test
- **Sensitivity / disturbance-rejection function** — S20, ReF21
- **Non-minimum-phase / RHP zero** — ReF21, E25-Test

### One-offs — seen once, don't over-invest
- Inverse Laplace / partial fractions → y(t) — only E20 (and ReF22 once)
- Pre-filter / notch filter design — only ReExam F21 (Q18)
- Linearization *error* magnitude — only ReExam F22 (Q1)
- Mass-spring / RLC → TF modelling — S21, F22, ReF22

---

## 3. Recurring numeric motifs (build muscle memory)
- **Phase-margin target = 60°** for the P-controller design question (60° default; 40° is the F22 variant).
- **Lead compensator α = 0.1** (S20 Q10–11, standard lead-design setup).
- Disturbance is almost always a **unit step at the plant input** → asks for e_ss.
- "No zeros given" Bode → match to step response (S21 Q10, E25-Test Q9).

---

## 4. Study priority
1. **Drill the 8-block skeleton on E21, E22, E23, E25** — closest to the real thing. Time yourself.
2. **Four backbone topics** (Bode read-off, block-diagram reduction, P-controller → 60° PM, gain/phase margins) = most points, every year → make automatic.
3. **Cheat-sheet must have clean recipes** for: ω_c/ω_π read-off, e_ss for step-at-r vs step-at-d, overshoot↔ζ, lead/PI design steps.
   - ⚠️ Previous-student `bandwidth_second_order.m` has the `4·ζ⁴` typo — cheat-sheet §4 is the corrected version.
4. Skim the one-offs (pre-filter, inverse-Laplace, linearization-error) once so they don't surprise you.
