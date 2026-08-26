---
tags: [34722, lcd, exam, cheatsheet, formulas]
course: 34722 Linear Control Design 1
purpose: One-page formula reference for the multiple-choice exam (2-June-2026)
---
# Exam Formula Cheat-Sheet — 2nd-order metrics, margins & controllers

> Distilled from the previous student's `EXAM/Helpers/*.m`. **Two of those scripts have typos** (`bandwidth_second_order.m`, `crossover_frequency2bandwidth.m` use `4*zeta`/`4*zeta^2` where it must be `4*zeta^4`) — the **corrected** forms are below. The overshoot/damping/phase-margin helpers are correct.

## 1. Standard 2nd-order system
$$G(s)=\frac{\omega_n^2}{s^2+2\zeta\omega_n s+\omega_n^2}\qquad \text{poles } s=-\zeta\omega_n\pm j\omega_n\sqrt{1-\zeta^2}$$
- Damped frequency: $\omega_d=\omega_n\sqrt{1-\zeta^2}$

## 2. Overshoot ↔ damping (memorize)
$$M_p=e^{-\pi\zeta/\sqrt{1-\zeta^2}}\quad(0<\zeta<1),\qquad \%OS=100\,M_p$$
$$\zeta=\frac{\ln(1/M_p)}{\sqrt{\pi^2+\ln^2(1/M_p)}}$$
Quick values: $\zeta=0.5\Rightarrow M_p\approx16\%$, $\;\zeta=0.7\Rightarrow\approx5\%$, $\;\zeta=0.6\Rightarrow\approx9.5\%$.

## 3. Phase margin ↔ damping
$$\gamma_M=\arctan\!\frac{2\zeta}{\sqrt{\sqrt{1+4\zeta^4}-2\zeta^2}}\ \text{[rad → deg]}$$
**Rule of thumb (MC favourite):** $\boxed{\;\gamma_M[\deg]\approx 100\,\zeta\;}$ for $\zeta\lesssim0.6$ → e.g. $PM=45^\circ\Rightarrow\zeta\approx0.45$.

## 4. Key frequencies (2nd-order)
- Gain crossover (open-loop): $\;\omega_c=\omega_n\sqrt{\sqrt{1+4\zeta^4}-2\zeta^2}$
- Closed-loop bandwidth **(corrected):** $\;\omega_{BW}=\omega_n\sqrt{(1-2\zeta^2)+\sqrt{4\zeta^4-4\zeta^2+2}}$
- Resonant peak (only if $\zeta<0.707$): $\;\omega_r=\omega_n\sqrt{1-2\zeta^2}$, $\;M_r=\dfrac{1}{2\zeta\sqrt{1-\zeta^2}}$
- Useful ratio: $\omega_{BW}\approx(1.0\text{–}1.5)\,\omega_n$ and $\omega_c<\omega_{BW}$.

## 5. Time-domain (step response)
- Peak time: $t_p=\dfrac{\pi}{\omega_d}=\dfrac{\pi}{\omega_n\sqrt{1-\zeta^2}}$
- Settling time: $t_s\approx\dfrac{4}{\zeta\omega_n}$ (2%), $\;\dfrac{3}{\zeta\omega_n}$ (5%)
- Rise time (10–90%): $t_r\approx\dfrac{1.8}{\omega_n}$

## 6. Stability margins (general, min-phase)
- Gain margin: $GM=\dfrac{1}{|G(j\omega_{pc})|}$ at the phase-crossover ($\angle G=-180^\circ$). In dB: $GM_{dB}=-20\log_{10}|G(j\omega_{pc})|$.
- Phase margin: $\gamma_M=180^\circ+\angle G(j\omega_{gc})$ at the gain-crossover ($|G|=1$).
- **Stable** if $GM>1$ (>0 dB) **and** $\gamma_M>0$. Nyquist: stable iff encirclements of $-1$ satisfy $N=-P$ (P = open-loop RHP poles).

## 7. Steady-state error (unity feedback)
| System type | step $\tfrac{1}{1+K_p}$ | ramp $\tfrac{1}{K_v}$ | parabola $\tfrac{1}{K_a}$ |
|---|---|---|---|
| 0 | $\frac{1}{1+K_p}$ | ∞ | ∞ |
| 1 | 0 | $\frac{1}{K_v}$ | ∞ |
| 2 | 0 | 0 | $\frac{1}{K_a}$ |

$K_p=\lim_{s\to0}G$, $\;K_v=\lim_{s\to0}sG$, $\;K_a=\lim_{s\to0}s^2G$. Type = # of integrators (poles at origin).

## 8. Controllers
- **PI:** $C(s)=K_p\!\left(1+\frac{1}{T_i s}\right)=\frac{K_p(T_i s+1)}{T_i s}$ — adds a pole at origin (+1 type → kills step error) and a zero at $-1/T_i$. Slows response / can cut PM.
- **Lead:** $C(s)=K_c\,\frac{s+z}{s+p}$, $z<p$ — adds phase to **boost PM** (speed/damping). Max boost $\phi_{max}=\arcsin\!\frac{\alpha-1}{\alpha+1}$ with $\alpha=p/z$, at $\omega_{max}=\sqrt{zp}$.
- **Lag / PI** → steady-state accuracy; **Lead** → transient/margin. **PI-Lead** = both.

## 9. Transform theorems
- Final value: $\lim_{t\to\infty}y(t)=\lim_{s\to0}sY(s)$ (if stable).
- Initial value: $\lim_{t\to0^+}y(t)=\lim_{s\to\infty}sY(s)$.

---
**MATLAB checks:** `EXAM/Helpers/overshoot2damping.m`, `damp2phase_margin.m`, `crossover_second_order.m` (all correct). For bandwidth use the corrected §4 formula, not the helper.
