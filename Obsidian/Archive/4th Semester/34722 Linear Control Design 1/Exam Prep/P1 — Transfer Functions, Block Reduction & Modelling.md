---
tags: [34722, lcd, exam, pattern]
course: 34722 Linear Control Design 1
pattern: P1
purpose: Recurring "find the transfer function / model the system" MC questions and how to crack them fast
---
# P1 — Transfer Functions, Block Reduction & Modelling

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Seen in:** **S20** Q1–Q4, **S21** Q1–Q2, Q7–Q8, **F22** Q1–Q2, Q8–Q9, **REExam F21** Q1, Q6, Q9.

This pattern is "given a description of a physical system or a block diagram, pick the right `G(s)`." Almost always solvable by structure, no heavy algebra.

---
## 1a. Block diagram → `Y/U`

The only three rules you need:
- **Series** blocks multiply: `A · B`
- **Parallel** branches add: `A + B`
- **Feedback** loop collapses to:
  $$\frac{\text{Forward}}{1 + \text{Loop Gain}} \text{ (negative feedback)} \qquad \text{or} \qquad \frac{\text{Forward}}{1 - \text{Loop Gain}} \text{ (positive feedback)}$$

Work **inside-out**: collapse the innermost loop first, then the next.

> [!important] Watch the take-off / summing points
> If a feedback is tapped *after* a block $E$, moving the take-off in front of $E$ means **dividing** that branch by $E$ (this is exactly the trick in F22 Q1: $H_1/E$).

| Exam | Answer | Shape to recognise |
|---|---|---|
| S21 Q1 | `(ABCD+ECD)/(1+BCF)` | two forward paths share one feedback `BCF` |
| S20 Q3 | `((1+A)s+AB)/(s+B)` | branch `A` parallel with loop `1/(s+B)` → `A + s/(s+B)` |
| F22 Q1 | `ABE²(C+D)/(…)` | `C,D` parallel; nested fb loops `H1,H2` |
| REExam Q9 | `K·G1·G2·(1/s)/(1+…)` | integrator `1/s` in the forward path |

> [!tip] MC Shortcut
> Check the **denominator** first — count which gains appear in the closed-loop denominator. Wrong options usually have a loop term in the numerator or miss one of the loops entirely.

---
## 1b. State-space → `G(s)`

Use the standard formula $G(s) = C(sI - A)^{-1}B + D$.

> [!example]- Decoupled System Shortcut (REExam Q6)
> For a **diagonal matrix $A$** (decoupled states), each state behaves as its own independent first-order system — simply sum their individual transfer functions:
> *   $A = \text{diag}(-1, -1)$, $B = [1; 9]$, $C = [1, 1]$:
>     $$G(s) = \frac{1}{s+1} + \frac{9}{s+1} = \frac{10}{s+1}$$

> [!note] 2x2 State-Space Systems
> For a 2×2 matrix $A$, the denominator of $G(s)$ is always the characteristic polynomial:
> $$\text{det}(sI - A) = s^2 - \text{trace}(A)s + \text{det}(A)$$
> Stability is achieved when all eigenvalues reside in the LHP. F22 Q9 uses **Routh-Hurwitz** on $s^2 + (1+w)s + (w-2) \to$ stable for $w > 2$.

---
## 1c. ODE → poles / TF

Take the Laplace transform with **zero initial conditions** (linear systems don't require linearization):

> [!example]- ODE to Transfer Function (S21 Q8 / F22 Q8)
> *   $\ddot{y} + 2\dot{y} + y = u \to G(s) = \frac{1}{s^2+2s+1} \to$ double pole at $s = -1$.
> *   $5\ddot{y} + \dot{y} + 0.5y = 3u \to G(s) = \frac{3}{5s^2+s+0.5} \to$ poles at $-0.1 \pm 0.3j$.

---
## 1d. Linearisation / first-principles modelling

1.  Find the **operating point** (set all derivatives = 0, then solve for steady-state values).
2.  **Linearize** the nonlinear term: replace $f(x)$ with the Taylor expansion: $f(x) \approx f(x_0) + f'(x_0)\Delta x$. The derivative $f'(x_0)$ becomes a constant coefficient.
3.  Take the Laplace transform, and normalize the denominator so the constant term or highest power coefficient matches standard form.

> [!example]- Linearization Worked Cases
> *   **S20 Q1** (skateboard motor): Steady state $I_0 K_t = B\omega_0$, where $\omega_0 = \dot{x}_0 \frac{G}{r} \to B = \frac{I_0 K_t}{\dot{x}_0 G / r} = 0.0016$.
> *   **S20 Q2** (steam engine): $J\dot{\omega} + B\omega = a K \sqrt{P - H\omega}$. Linearizing the $\sqrt{P - H\omega}$ term introduces an extra damping factor:
>     $$B_{extra} = \frac{0.5 \cdot K \cdot a_0 \cdot H}{\sqrt{P - H\omega_0}} \to G(s) \approx \frac{109}{s+0.65}$$
> *   **REExam Q1** (DC motor with square-root friction $B\sqrt{\omega}$):
>     $$\frac{d}{d\omega}[B\sqrt{\omega}] = \frac{0.5 B}{\sqrt{\omega_0}}$$
> 
> *Solve script:* `EXAM/Scripts/solved/solve_S20.m` (Q1, Q2)

---
## 1e. Mechanical (masses + springs)

Write **one equation of motion per mass** ($m\ddot{x} + k\Delta x = F$), take the Laplace transform, and solve the algebraic equations to eliminate intermediate coordinates.

> [!example]- Two-Mass System (S21 Q7)
> Two masses, spring $k$, force applied on $m_1$, output position $x_2$:
> $$\frac{X_2}{F} = \frac{k}{(m_2 s^2 + k)(m_1 s^2 + k) - k^2}$$
> With $m_1=m_2=1$ and $k=1 \to G(s) = \frac{1}{s^2(s^2+2)}$. The double pole at the origin ($s^2$) represents the rigid-body mode, which is always present when no element grounds the masses.

---
## 1f. RLC → block diagram

Treat the circuit components in the $s$-domain. Treat current as $I = (V_i - V_0) \frac{1}{R+sL}$, then output voltage as $V_0 = I \frac{1}{sC}$. This maps to a forward path of $\frac{1}{R+sL}$ followed by $\frac{1}{sC}$ under negative unity feedback (S21 Q2, F22 Q2).

*   Capacitor Impedance: $Z_C = \frac{1}{sC}$
*   Inductor Impedance: $Z_L = sL$

---

> [!warning] ⚠️ Traps
> - **Series vs. Parallel:** Mixing them up in block diagram numerators.
> - **Moved Take-Off:** Forgetting to divide a moved take-off branch by the intervening block.
> - **Already Linear:** Wasting time trying to linearize an ODE that is already linear (a classic S21 Q8 distractor).
> - **Metric Prefix Trap:** Reading microfarads ($\mu\text{F}$) as farads ($\text{F}$) (e.g. F22 Q2: "160F" is actually $160\ \mu\text{F} \to \tau=RC=8\text{ ms}$, not $16\text{ ms}$).
