---
tags: [34722, lcd, exam, pattern]
course: 34722 Linear Control Design 1
pattern: P3
purpose: Gain/phase margin, stable-K range, Nyquist criterion, and the stable-vs-unstable plant distinction
---
# P3 — Stability, Margins & Nyquist

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Seen in:** **S20** Q9, **S21** Q4, Q6, **F22** Q9, Q11–Q12, Q14, **REExam F21** Q12, Q14, Q16.

The exam loves "for which `K` is the closed loop stable?" The **whole game** is: *is the open-loop plant already stable, or does it have a RHP pole?* The two cases completely invert the answer.

---
## Margins from a Nyquist / Bode plot

*   **Gain Margin (GM):** $GM = 1 / |G(j\omega_{pc})|$ at the phase-crossover frequency ($\angle G(j\omega_{pc}) = -180^\circ$).
    *   In decibels: $GM_{dB} = -20\log_{10}|G(j\omega_{pc})|$.
*   **Phase Margin ($\gamma_M$):** $\gamma_M = 180^\circ + \angle G(j\omega_{gc})$ at the gain-crossover frequency ($|G(j\omega_{gc})| = 1$).
*   **Nyquist Real Crossing:** If the Nyquist curve crosses the negative real axis at $-x$:
    $$GM = \frac{1}{x}$$
    > [!example]- Margins Example (F22 Q11)
    > Nyquist crosses at $-0.1639 \to GM = \frac{1}{0.1639} = 6.10 \approx 15.71\text{ dB}$.

---
## Stable range of `K` — the two cases

> [!important] Case A — Open-loop plant is STABLE (no RHP poles, $P=0$)
> Closed-loop system is stable for **$0 < K < GM$**. 
> The Bode criterion applies: we need $GM > 1$ (or $GM_{dB} > 0$) and $\gamma_M > 0$.
> *   **S21 Q4:** $L(s) = \frac{K}{(s+1)^3}$. Phase crossover frequency:
>     $$-3\arctan(\omega_{pc}) = -180^\circ \;\Rightarrow\; \omega_{pc} = \tan(60^\circ) = \sqrt{3}$$
>     Magnitude at crossover: $|L(j\sqrt{3})| = \frac{K}{\sqrt{1+3}^3} = \frac{K}{8}$. Setting $|L| = 1 \to K_{max} = 8$. **Stable for $0 < K < 8$.**
> *   **REExam Q14:** $G(s) = \frac{25}{s^3+s^2+10s}$, $GM = 0.398 \to$ stable for **$0 < K_P < 0.398$** (choose $K_P = 0.25$, not $0.5$).

> [!important] Case B — Open-loop plant is UNSTABLE (has RHP poles, $P > 0$)
> The Nyquist criterion requires **$N = -P$** (exactly $P$ counter-clockwise encirclements of the critical point $-1$).
> This requires the controller gain $K$ to be **large enough** to wrap around $-1$:
> $$K > \frac{1}{|x_{crossing}|}$$
> *   **F22 Q12:** Open-loop pole at $+2.5$ ($P=1$), Nyquist crossing at $-0.0222 \to$ stable for $K_P > \frac{1}{0.0222} \approx 45 \to$ **choose $K_P = 50$**.
> *   **REExam Q16:** Crossing at $-0.0247 \to K_{marginal} = 40.5 \to$ stable for $K_P > 40.5 \to$ **choose $K_P = 45$**.

---
## Nyquist criterion in one line

$$Z = N + P$$

Where:
*   $Z$ = number of closed-loop RHP poles (we want $Z = 0$ for stability)
*   $N$ = number of **clockwise** encirclements of $-1$
*   $P$ = number of open-loop RHP poles
*   **Stable Closed Loop** $\Leftrightarrow Z = 0 \Leftrightarrow N = -P$ (i.e. exactly $P$ CCW encirclements)

> [!example]- Nyquist Example (REExam Q12)
> Open-loop plant has $P=1$ RHP pole. The Nyquist plot encircles $-1$ once **counter-clockwise** ($N = -1$).
> $$Z = N + P = -1 + 1 = 0 \;\Rightarrow\; \text{Stable!}$$

---
## P-controller to hit a target PM

To find the gain $K_P$ needed for a target Phase Margin $\gamma_M$:
1.  Find the frequency $\omega$ where the plant phase is exactly $\angle G(j\omega) = -180^\circ + \gamma_M$.
2.  Set $K_P = 1 / |G(j\omega)|$ (which is $K_{P,dB} = -|G(j\omega)|_{dB}$).

> [!example]- P-Design Cases
> *   **S21 Q6:** Target $\gamma_M = 40^\circ \to \angle G = -140^\circ$ occurs at $\omega = 2.28\text{ rad/s}$ where $|G| = -38.9\text{ dB} \to K_P = 10^{38.9/20} = 88$.
> *   **S20 Q9:** Target $\gamma_M = 60^\circ \to \angle G = -120^\circ$ occurs at $\omega \approx 25\text{ rad/s}$ where $|G| \approx -23\text{ dB} \to K_P = 10^{-(-23)/20} \approx 0.06$.
> 
> *Solve scripts:* `solve_S21.m` (Q4, Q6), `solve_F22.m` (Q11, Q12, Q14), `solve_REExam_F21.m` (Q14, Q16).

---
## Routh-Hurwitz Stability Criterion

Build the Routh array from the characteristic equation $1 + L(s) = 0$. The system is stable if and only if all coefficients in the first column are of the same sign.

> [!example]- Routh Example (F22 Q9)
> Char eqn: $s^2 + (1+w)s + (w-2) = 0$. For stability:
> $$1+w > 0 \quad \text{and} \quad w-2 > 0 \;\Rightarrow\; w > 2$$

---

> [!warning] ⚠️ Traps
> - **Reciprocal Trap:** Confusing the Gain Margin ratio ($GM \ge 1$ for stable) with its reciprocal crossing distance ($x$) or its decibel representation.
> - **Plant Stability Check:** Forgetting to check if the plant is open-loop unstable. If it has a RHP pole, the stability range is **$K > K_{min}$**, not $K < K_{max}$!
> - **Crossover Confusion:** Margin definitions are specific: $\gamma_M$ uses $\angle G$ at $|G|=1$; $GM$ uses $|G|$ at $\angle G = -180^\circ$ — do not swap these crossover points.
