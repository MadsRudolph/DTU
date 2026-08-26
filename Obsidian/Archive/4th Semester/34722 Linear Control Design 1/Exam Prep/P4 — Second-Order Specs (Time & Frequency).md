---
tags: [34722, lcd, exam, pattern]
course: 34722 Linear Control Design 1
pattern: P4
purpose: Overshoot↔ζ, step-response identification, finding K for a transient spec, ωn from a damped period
---
# P4 — Second-Order Specs (Time & Frequency)

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Seen in:** **S20** Q4–Q5, Q8, **S21** Q9–Q10, **F22** Q10, **REExam F21** Q7–Q8, Q10.

Standard form of a second-order system:
$$G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$
Poles are located at: $s = -\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2} = -\sigma \pm j\omega_d$

---
## Overshoot ↔ Damping Ratio ($\zeta$)

The peak fractional overshoot $M_p$ and percentage overshoot $\%OS$ are given by:
$$M_p = e^{-\frac{\pi\zeta}{\sqrt{1-\zeta^2}}}, \qquad \%OS = 100 \cdot M_p$$

Inverting this formula yields the required damping ratio for a target overshoot:
$$\zeta = \frac{\ln(1/M_p)}{\sqrt{\pi^2 + \ln^2(1/M_p)}}$$

> [!tip] 💡 Damping Ratio Pegs (Memorise!)
> - $\zeta = 0.5 \quad\to\quad M_p \approx 16.3\%$ (or $\sim 16\%$)
> - $\zeta = 0.6 \quad\to\quad M_p \approx 9.5\%$
> - $\zeta = 0.7 \quad\to\quad M_p \approx 4.6\%$ (or $\sim 5\%$)
> - $\zeta = \frac{\sqrt{2}}{2} \approx 0.707 \quad\to\quad M_p \approx 4.3\%$

> [!example]- Overshoot Worked Cases
> *   **F22 Q10:** $L(s) = \frac{K}{s(s+\sqrt{2K})}$. The closed loop matches the standard form with $\omega_n = \sqrt{K}$ and $2\zeta\omega_n = \sqrt{2K} \to \zeta = \frac{\sqrt{2}}{2}$. Damping ratio peg is $\zeta = 0.707 \to$ **$M_p = 4.3\%$**.
> *   **S20 Q5:** Step peak $y_{peak} = 2.9$, DC gain $y_{ss} = 2$.
>     $$M_p = \frac{2.9 - 2}{2} = 0.45 \;\Rightarrow\; \zeta \approx 0.2$$

---
## Find $K$ for a Transient Specification

Build the closed-loop transfer function, identify $\omega_n$ and $\zeta$ in terms of $K$, and solve for the limit.

> [!example]- Solving for Gain (S21 Q9)
> Forward path $G(s) = \frac{K}{s(s+5)}$. Closed loop has $\omega_n = \sqrt{K}$ and $2\zeta\omega_n = 5 \to \zeta = \frac{2.5}{\sqrt{K}}$. 
> For an overshoot specification of $M_p \le 12\% \to \zeta \ge 0.559$:
> $$\frac{2.5}{\sqrt{K}} \ge 0.559 \;\Rightarrow\; \sqrt{K} \le 4.47 \;\Rightarrow\; K \le 19.97 \;\Rightarrow\; \mathbf{0 \le K \le 20}$$
> 
> *Solve scripts:* `solve_S21.m` Q9, `solve_S20.m` Q5, `solve_F22.m` Q10.

---
## Step-Response Identification

Use the initial and final value theorems to quickly eliminate options:
*   **Initial-Value Theorem:** $y(0^+) = \lim_{s \to \infty} s Y(s) = \lim_{s \to \infty} G(s)$ (for a unit step input $U(s) = 1/s$).
*   **Final-Value Theorem:** $y(\infty) = \lim_{s \to 0} s Y(s) = \lim_{s \to 0} G(s)$ (provided the system is stable).

> [!important] Qualitative Time-Domain Shapes
> - **Initial Jump:** A non-zero initial output value $y(0^+) \ne 0$ occurs if and only if the numerator and denominator share the same degree. This requires an $s$-term in the numerator: $G(s) = \frac{b_1 s + b_0}{s + a_0}$. (S20 Q4: jumps to $0.4$, settles at $0.8$).
> - **DC Tracking:** A final value $y(\infty) \ne 1$ implies the DC gain is not unity. S21 Q10: DC gain is $20\text{ dB} = 10 \to$ unit step response ends at $10$.

> [!example]- PFD Time-Domain Solutions
> *   **REExam Q7:** $Y(s) = \frac{10}{(s+1)(s+3)}$. Residues are $5$ and $-5 \to y(t) = 5e^{-t} - 5e^{-3t}$.
> *   **REExam Q8:** $Y(s) = \frac{4(s+50)}{s(s^2+30s+200)} \to y(t) = 1 + 0.6e^{-20t} - 1.6e^{-10t}$ (final value $y(\infty) = 1$).

---
## $\omega_n$ from a Damped Ring Period

If the step response displays a fast oscillation on top of a slower rise, measure the **damped ring period $T'$** (peak-to-peak time of the fast ring) to calculate the damped frequency $\omega_d = \frac{2\pi}{T'}$. Since $\omega_d \approx \omega_n$ for low damping:
$$\omega_n \approx \frac{2\pi}{T'}$$
> [!example]- Ringing Case (S20 Q8)
> Damped period measured as $T' = 1.2\text{ ms} \to \omega_n \approx \frac{2\pi}{1.2 \cdot 10^{-3}} \approx 5236\text{ rad/s}$.
> Pick the Bode plot containing a resonant peak near $5236\text{ rad/s}$.

---
## Time-Domain Parameter Summary

*   **Peak Time:** $t_p = \frac{\pi}{\omega_n\sqrt{1-\zeta^2}} = \frac{\pi}{\omega_d}$
*   **Settling Time (2% band):** $t_s \approx \frac{4}{\zeta\omega_n} = \frac{4}{\sigma}$
*   **Settling Time (5% band):** $t_s \approx \frac{3}{\zeta\omega_n}$
*   **Rise Time (approximate):** $t_r \approx \frac{1.8}{\omega_n}$
*   **Resonant Frequency (exists only if $\zeta < 0.707$):** $\omega_r = \omega_n\sqrt{1-2\zeta^2}$
*   **Resonant Peak:** $M_r = \frac{1}{2\zeta\sqrt{1-\zeta^2}}$

---

> [!warning] ⚠️ Traps
> - **Overshoot Reference:** Overshoot is relative to the final value, not the origin:
>   $$M_p = \frac{y_{peak} - y_{ss}}{y_{ss}}$$
>   Forgetting to subtract/divide by $y_{ss}$ is a common trap (S20 Q5).
> - **Damping Limits:** The overshoot equation only holds for underdamped systems ($0 < \zeta < 1$). If $\zeta \ge 1$, the response is overdamped and exhibits **no overshoot**.
> - **Frequency Swap:** Do not confuse the undamped natural frequency $\omega_n$ with the actual visible ringing frequency $\omega_d = \omega_n\sqrt{1-\zeta^2}$.
