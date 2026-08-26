---
tags: [34722, lcd, exam, pattern]
course: 34722 Linear Control Design 1
pattern: P5
purpose: ess by system type, finding KP from a required ess, disturbance sensitivity
---
# P5 — Steady-State Error & System Type

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Seen in:** **F22** Q16, **REExam F21** Q4, Q19. (Underpins conceptual "need a PI term" questions like F22 Q15).

**System Type = number of open-loop poles located at the origin ($s=0$)** in the loop gain $L(s) = C(s)G(s)$. The system type dictates the steady-state tracking capability.

---
## Steady-State Tracking Table (Unity Feedback)

| System Type | Step Input $r(t)=u(t)$ | Ramp Input $r(t)=t$ | Parabolic Input $r(t)=t^2/2$ |
|---|---|---|---|
| **Type 0** | $e_{ss} = \frac{1}{1 + K_p}$ | $e_{ss} = \infty$ | $e_{ss} = \infty$ |
| **Type 1** | $e_{ss} = 0$ | $e_{ss} = \frac{1}{K_v}$ | $e_{ss} = \infty$ |
| **Type 2** | $e_{ss} = 0$ | $e_{ss} = 0$ | $e_{ss} = \frac{1}{K_a}$ |

Where the static error constants are defined as:
*   **Position Constant:** $K_p = \lim_{s \to 0} L(s)$
*   **Velocity Constant:** $K_v = \lim_{s \to 0} s L(s)$
*   **Acceleration Constant:** $K_a = \lim_{s \to 0} s^2 L(s)$

> [!example]- Tracking Example (REExam Q4)
> For a **Type-2** system with input $r(t) = 5 + 2t + \frac{1}{2}t^2$:
> The step ($5$) and ramp ($2t$) inputs are tracked with **zero error**. 
> The parabolic input ($\frac{1}{2}t^2 \to R(s) = 1/s^3$) yields a finite steady-state error of $e_{ss} = 1/K_a$.

> [!note] Conceptual Corollary (Integrator Requirement)
> A **Type-0** plant cannot track a step input with zero error using a finite proportional gain ($K_P$). To achieve zero steady-state step error, you must add a **PI controller** to introduce an integrator at the origin (shifting the loop to Type 1). (This eliminates F22 Q15 option b as a distractor).

---
## Find $K_P$ from a Required Steady-State Error

For a unit step input under unity feedback:
$$e_{ss} = \frac{1}{1 + K_P G(0)} \;\Rightarrow\; K_P = \frac{1/e_{ss} - 1}{G(0)}$$

Read the DC gain $G(0)$ off the Bode plot's low-frequency asymptotic value (remember to convert from decibels to linear first).

> [!example]- Proportional Gain Case (F22 Q16)
> Bode plot shows low-frequency DC magnitude $G(0) = -7.9588\text{ dB} = 0.4$. We want a steady-state step tracking error $e_{ss} = 0.555$:
> $$K_P = \frac{1/0.555 - 1}{0.4} = \frac{1.8018 - 1}{0.4} = 2$$
> 
> *Solve scripts:* `solve_F22.m` Q16, `solve_REExam_F21.m` Q4, Q19.

---
## Disturbance Sensitivity

For the standard feedback loop layout $r \to e \to K_P \to u \to (+ d) \to G(s) \to y$ where the disturbance $d(t)$ enters at the plant input:

*   **Reference-to-Output Transfer Function:**
    $$G_{yr}(s) = \frac{K_P G(s)}{1 + K_P G(s)} \;\Rightarrow\; \text{At DC: } K_P = \frac{G_{yr}(0)}{1 - G_{yr}(0)G(0)}$$
*   **Disturbance-to-Output Transfer Function:**
    $$G_{yd}(s) = \frac{G(s)}{1 + K_P G(s)}$$
*   **Error-to-Disturbance Static Tracking Error:**
    $$e(0) = -G_{yd}(0) \qquad (\text{since } G_{ed}(s) = -G_{yd}(s))$$

> [!example]- Disturbance Case (REExam Q19)
> Given $G(0) = 1$, reference tracking $G_{yr}(0) = -3.52\text{ dB} = 0.6667$, and disturbance sensitivity $G_{yd}(0) = -15.563\text{ dB} = 0.1667$.
> *   $K_P = \frac{0.6667}{1 - 0.6667 \cdot 1} = 2$
> *   Static tracking error to a unit step disturbance: $e(0) = -G_{yd}(0) = -0.1667$

---

> [!warning] ⚠️ Traps
> - **Integrator Definition:** An integrator is a pole **exactly at the origin ($s=0$)**. A real LHP pole (e.g. $s = -5$) is *not* an integrator and does not raise the system type.
> - **Decibel Trap:** Always convert Bode plot values from decibels to linear ($10^{\text{dB}/20}$) before using them in the equations. The raw decibel number is always a distractor option (e.g., F22 Q16 option e: $7.9588$).
> - **Disturbance Error Sign:** Steady-state tracking error to a disturbance is **negative** of the DC sensitivity: $e(0) = -G_{yd}(0)$. The positive value is a classic distractor option.
