---
tags: [34722, lcd, exam, pattern]
course: 34722 Linear Control Design 1
pattern: P6
purpose: The design recipes — P, Lead, PI-Lead phase-budget, prefilter, feedforward — plus the exam's favourite arithmetic traps
---
# P6 — Controller Design (P, Lead, PI-Lead, Feedforward)

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Seen in:** **S20** Q9–Q11, **F22** Q13, Q17–Q19, **REExam F21** Q15, Q17–Q18, Q20.

The highest-value pattern: the Q11–Q19 block on every recent exam is mostly controller design. Learn the **phase-budget equation** and follow the **degrees-vs-radians / dB-vs-linear** discipline to clear these questions easily.

---
## Proportional (P) Controller

Pick the crossover frequency $\omega_c$ where the plant phase yields the target phase margin:
$$\angle G(j\omega_c) = -180^\circ + \gamma_M$$
The required proportional gain is then:
$$K_P = \frac{1}{|G(j\omega_c)|} \;\Rightarrow\; K_{P,dB} = -|G(j\omega_c)|_{dB}$$

> [!example]- P-Design Case (S20 Q9)
> Target phase margin $\gamma_M = 60^\circ \to \angle G(j\omega_c) = -120^\circ$. This occurs at $\omega_c \approx 25\text{ rad/s}$ where $|G| \approx -23\text{ dB} \to K_P = 10^{-(-23)/20} \approx 0.06$.

---
## Lead Controller

$$C_d(s) = \frac{\tau_d s + 1}{\alpha \tau_d s + 1} \qquad (\text{with } \alpha < 1)$$

*   Place the center frequency exactly at the new crossover frequency:
    $$\tau_d = \frac{1}{\omega_c\sqrt{\alpha}}$$
*   **Zero** is placed at: $\omega_z = \frac{1}{\tau_d}$
*   **Pole** is placed at: $\omega_p = \frac{1}{\alpha \tau_d}$
*   **Maximum Phase Lead** added at center frequency:
    $$\phi_{max} = \arcsin\left(\frac{1-\alpha}{1+\alpha}\right)$$
*   **Magnitude Gain** added at center frequency:
    $$|C_d(j\omega_c)| = \frac{1}{\sqrt{\alpha}}$$

> [!example]- Lead Design Cases
> *   **S20 Q10:** $\omega_c = 10\text{ rad/s}$, $\alpha = 0.1 \to \tau_d = \frac{1}{10\sqrt{0.1}} \approx 0.316\text{ s} \to \omega_z = 3.2\text{ rad/s}$.
> *   **S20 Q11 (P-Lead):** $\alpha = 0.1 \to |C_d(j\omega_c)| = 10\text{ dB}$. Plant has $|G(j\omega_c)| = -14\text{ dB}$. Combined loop gain at crossover $|G C_d| = -14\text{ dB} + 10\text{ dB} = -4\text{ dB}$. Setting magnitude to $0\text{ dB}$ requires $K_P = +4\text{ dB} = 1.5$.
> *   **F22 Q13:** $|C_d(10j)| = 1 \to \omega_c = 10\text{ rad/s}$. Using $\alpha = \left(\frac{1}{\omega_c \tau_d}\right)^2 \to$ maximum lead gain is $M_D = \frac{1}{\sqrt{\alpha}} = 11\text{ dB}$.

---
## PI-Lead — The Phase-Budget Equation

$$C(s) = K_P \cdot \frac{\tau_i s + 1}{\tau_i s} \cdot \frac{\tau_d s + 1}{\alpha \tau_d s + 1} = \text{PI} \times \text{Lead}$$

> [!important] The Phase-Budget Equation
> At the target crossover frequency $\omega_c$, the combined phase contributions must sum to the required phase margin:
> $$\boxed{-180^\circ + \gamma_M = \phi_G + \phi_{Lead} + \phi_{PI}}$$
> Where:
> *   $\phi_{PI} = -\arctan(1/N_i)$ (the PI **lags** the phase, where $N_i = \omega_c \tau_i$, typically chosen as $N_i = 3 \text{ to } 5$).
> *   $\phi_{Lead} = \arcsin\left(\frac{1-\alpha}{1+\alpha}\right)$ (the Lead **leads** the phase).
> *   $\phi_G$ = phase of the plant at crossover frequency $\omega_c$, read directly off the Bode plot.

> [!note] The Three Ways the Exam Solves This:
> 1.  **Solve for $\alpha$** (given $\omega_c, \gamma_M, N_i$):
>     $$\phi_{Lead} = -180^\circ + \gamma_M - \phi_G - \phi_{PI} \;\Rightarrow\; \alpha = \frac{1 - \sin(\phi_{Lead})}{1 + \sin(\phi_{Lead})}$$
>     *(F22 Q17 $\to \alpha = 0.5$; REExam Q15 $\to M_D = 3.3$)*
> 2.  **Solve for $N_i = \omega_c \tau_i$**:
>     $$\arctan(1/N_i) = 180^\circ - \gamma_M + \phi_G + \phi_{Lead}$$
>     *(REExam Q17 $\to N_i = 1.57$)*
> 3.  **Solve for $K_P$** (find $\omega_c$ where $\phi_G$ matches, construct $\tau_i$ and $\tau_d$, and solve):
>     $$K_P = \frac{1}{|G(j\omega_c) C_{PI}(j\omega_c) C_d(j\omega_c)|}$$
>     *(F22 Q19 $\to K_P = 3.4154$)*

> [!example]- Worked PI-Lead (REExam Q17)
> Given plant phase $\phi_G = -151.064^\circ$ at $\omega_c = 25.04$, target $\gamma_M = 75^\circ$, and $\alpha = 0.01$:
> *   $\phi_{Lead} = \arcsin(0.99 / 1.01) = 78.58^\circ$
> *   $\arctan(1/N_i) = 180^\circ - 75^\circ - 151.064^\circ + 78.58^\circ = 32.516^\circ$
> *   $N_i = \frac{1}{\tan(32.516^\circ)} = 1.57$

---
## Prefilter (Resonant Peak Flattening)

To flatten a closed-loop resonant peak $M_p$ occurring at frequency $\omega_p$ using a first-order prefilter $G_f(s) = \frac{1}{\tau_f s + 1}$, we require the filtered magnitude at peak to equal unity:
$$\tau_f = \frac{1}{\omega_p}\sqrt{M_p^2 - 1}$$

> [!important] Metric Constraint
> The peak $M_p$ must be in **linear** units ($M_p = 10^{\text{dB}/20}$) before evaluating the formula.

> [!example]- Prefilter Case (REExam Q18)
> Given peak frequency $\omega_p = 0.7707\text{ rad/s}$ and magnitude peak $M_p = 11.0827\text{ dB} = 3.582$:
> $$\tau_f = \frac{1}{0.7707}\sqrt{3.582^2 - 1} = 4.46\text{ s}$$
> 
> *(Distractor options use raw dB value 14.32, forget the square root 2.1, or use $1/\omega_p = 0.224$)*

---
## Feedforward Disturbance Rejection

To reject a disturbance $D(s)$ entering the system after a series of $n$ first-order lags $G_1(s) = \prod_{k=1}^n \frac{1}{\tau_k s + 1}$, the ideal feedforward controller is $F_d(s) = \frac{D(s)}{G_1(s)}$.

Since this ideal controller has more zeros than poles, it is **improper**. We make it realizable by appending an $(n-2)$-order low-pass filter with time constants **faster** than the plant:

$$\boxed{F_d(s) = \frac{D(s)}{G_1(s)(\tau_f s + 1)^{n-2}}, \qquad \tau_f \le \frac{\min(\tau_k)}{5}} \quad \text{— option (d)}$$

---

> [!warning] ⚠️ The Traps (Deliberately Planted!)
> 1.  **Degrees vs. Radians:** Standard inverse trigs (`asin`, `atan`) yield radians. The Phase-Budget equation is resolved in **degrees**. Mixing them leads to distractor choices.
> 2.  **Linear vs. dB Scales:** Forgetting to convert $K_P$ or $M_p$ out of decibels ($10^{\text{dB}/20}$).
> 3.  **F22 Q19 alpha typo:** The paper prints $\alpha = 0.001$, but the official solution was calculated using **$\alpha = 0.01$**. If you use $0.001$, you get $K_P \approx 1.2$ — use **$0.01$** to get the correct option $K_P = 3.4154$.
> 4.  **PI Lag Sign:** The PI term *subtracts* phase ($\phi_{PI} = -\arctan(1/N_i)$). Adding it instead is a trap.
> 5.  **Bode Reading Precision:** Read values carefully (e.g. REExam Q17: plant phase is $-151.064^\circ$, not $-15^\circ$).
