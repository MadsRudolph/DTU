---
tags: [34722, lcd, exam, pattern]
course: 34722 Linear Control Design 1
pattern: P2
purpose: "Bode plot → identify G(s)" and read-off questions, with the slope/phase rules
---
# P2 — Frequency Response & Bode Read-Off

> [!info] Quick Links
> - Back to [[00 LCD1 — Exam Hub]] · Formulas: [[Exam Formula Cheat-Sheet]]
> - **Seen in:** **S20** Q6–Q7, **S21** Q3, Q5, **F22** Q4–Q5, Q7, **REExam F21** Q3, Q5.

The single most common MC type: a Bode plot is shown, identify the poles/zeros or pick the matching `G(s)`. Pure read-off — learn the asymptote rules cold.

---
## The rules (memorise)

| Feature | Magnitude | Phase |
|---|---|---|
| **DC gain** | flat low-freq level (dB) $\to |G(0)| = 10^{\text{dB}/20}$ | starts at $0^\circ$ (type 0) |
| **Real pole** at $-p$ | slope **$-20\text{ dB/dec}$** from $\omega = p$ | **$-90^\circ$** (kink at $p$) |
| **Real zero** at $-z$ | slope **$+20\text{ dB/dec}$** | **$+90^\circ$** |
| **Integrator** $1/s$ | $-20\text{ dB/dec}$ everywhere | $-90^\circ$ flat |
| **Complex poles** $\zeta < 0.707$ | **resonant peak** at $\omega_r$ | $-180^\circ$ total, sharp drop |
| **RHP zero** $+z$ | **$+20\text{ dB/dec}$** (up!) | **$-90^\circ$** (down!) $\to$ *the trap* |
| **RHP pole** $+p$ | $-20\text{ dB/dec}$ | **$+90^\circ$** (phase rises) |

> [!tip] Counting Trick
> *   Final magnitude asymptotic slope = $-20 \cdot (\#poles - \#zeros)\text{ dB/dec}$
> *   Final phase asymptotic level = $-90^\circ \cdot (\#poles - \#zeros)$ 
> *(Note: RHP factors will flip the phase contribution sign but keep the magnitude slope intact!)*

---
## Worked identifications

> [!example]- Worked Identifications
> *   **S20 Q6:** Amplitude rises then falls, phase bumps up then decays to $-90^\circ$. A zero must occur lowest ($\sim 10 \to s = -10$), followed by a pole ($\sim 50 \to s = -50$). To end at $-90^\circ$ phase, there must be a second pole ($\sim 1000 \to s = -1000$). **Poles at $-50, -1000$; zero at $-10$.**
> *   **S21 Q5:** DC at $40\text{ dB} \to |G(0)| = 100$. A slope of $-40\text{ dB/dec}$ starts from $\omega = 1$ (two real LHP poles). At $\omega = 10$, the slope steepens to $-60\text{ dB/dec}$ but **phase rises by $+90^\circ$** $\to$ that third pole must be **RHP** ($+10$):
>     $$G(s) = \frac{100}{(1+s)^2(1-0.1s)}$$
>     *(Matches option: "negative and positive real poles, no zeros")*
> *   **REExam Q5:** DC at $60\text{ dB}$, phase climbs from $-180^\circ \to$ one **positive pole** (RHP) + one negative zero:
>     $$G(s) = \frac{100(s+10)}{s-1}$$
> *   **F22 Q4:** One RHP zero ($+20\text{ dB/dec}$ magnitude but $-90^\circ$ phase drop) + two poles on the imaginary axis.
> *   **S21 Q3** (Pole-zero map $\to$ Bode match): Real zero at $-2.5$, complex conjugate poles at $-1.5 \pm j\beta$. Match the curve with the gentle $-90^\circ$ fall.

---
## DC gain in dB (quick ones)

> [!example]- DC Gain Calculation (F22 Q7)
> Given $G(s) = \frac{12}{(s+2)(s+3)}$:
> $$G(0) = \frac{12}{2 \cdot 3} = 2 \;\Rightarrow\; 20\log_{10}(2) = 6\text{ dB}$$
> 
> *Solve scripts:* `solve_F22.m` Q7, `solve_S20.m` Q5.

---
## Bandwidth read-off (closed loop)

**Bandwidth ($\omega_{BW}$) is the frequency where magnitude $|G(j\omega)|$ drops by $-3\text{ dB}$ below its low-frequency (DC) level.**

> [!important] Peaking Bandwidth Shortcut
> If the closed-loop magnitude curve starts with a resonant peak (starts above DC level), the bandwidth is simply read at the **first $0\text{ dB}$ crossing** (as it drops $3\text{ dB}$ below the peak/DC).
> *   **S20 Q7:** Starts at $+3\text{ dB}$, crosses $0\text{ dB}$ at $\sim 22\text{ rad/s} \to$ **BW = 22 rad/s**.

> [!note] Rule of Thumb
> $\omega_{BW} \approx (1.0 \text{ to } 1.5) \cdot \omega_n$ and $\omega_c < \omega_{BW}$. The exact second-order bandwidth formula is located in [[Exam Formula Cheat-Sheet]] §4.

---

> [!warning] ⚠️ Traps
> - **RHP Zero:** Magnitude climbs like a normal zero ($+20\text{ dB/dec}$) but phase *drops* by $-90^\circ$ — a favorite DTU distractor (F22 Q4).
> - **Linear vs. dB:** Accidentally reading the DC level value directly as linear gain instead of converting from decibels ($10^{\text{dB}/20}$).
> - **Real vs. Complex Poles:** A **resonant peak** implies complex poles ($\zeta < 0.707$). The absence of a peak indicates well-damped or real poles.
