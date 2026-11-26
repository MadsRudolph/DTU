---
course: "34840"
type: exercise
date: 2026-11-17
week: 47
lecture: 11
tags: [Acoustics, exercises, vibration, sdof, natural-frequency, static-deflection, transmissibility, base-excitation]
---
# Week 11 — Structure-borne Sound and Vibration Isolation

Source: [[31200_Problems_8_2022.pdf|vibration problem set (Ohlrich, 4 problems)]]. Official solutions: [[31200_Solutions_8_2022.pdf|answers to exercise problems, chapter 6]]. Theory: [[Lecture 11 - Structure-borne Sound and Vibration Isolation]]. MATLAB: `5. Semester/Acoustics and Noise Control/Matlab/Week11_Vibration_Isolation.m`.

> [!warning] Which sheet belongs to this week
> Learn files the **vibration** set under module 11 (it calls it `31200_Problems_8_2024`; on disk it is `31200_Problems_8_2022.pdf`). The file named `34840_Problems 11_2026.pdf` (and its older copy `34840_Problems 11.pdf`, solutions `_2026` and `_2023`) is the **sound insulation** set: party wall, factory windows, a wall with a window. Learn files that under module 12, so it belongs to Lecture 12 (24-Nov) and is **not** worked here.

> [!success] Checked against the official solutions
> Every answer agrees with `31200_Solutions_8_2022.pdf` to the digits it prints. The official text uses $g=9.81$ in Problem 2 and $9.82$ in Problem 4; I used the same so the numbers match. No disagreements.

## Answers at a glance

| Question | Result | Official |
|---|---|---|
| 1 (a)–(d) | $f_a=f_d=\frac1{2\pi}\sqrt{2s/m}$, $f_b=f_c=\frac1{2\pi}\sqrt{s/2m}$ | same ✔ |
| 2 (a) | 53.05 Hz | 53 Hz ✔ |
| 2 (b) | $\xi_{\rm stat}=0.981$ mm, $f_b=15.24$ Hz | ≈1 mm, 15.2 Hz ✔ |
| 3 (a) | $f_0=20.05$ Hz, $\omega_0=125.96$ rad/s | 20.1 Hz, 126 rad/s ✔ |
| 3 (b) $\omega=37.8$ | $\xi=0.231$ mm, $v=8.73$ mm/s, $a=0.330$ m/s² | 0.231 mm, 8.7 mm/s, 0.33 ✔ |
| 3 (c) $\omega=378$ | $\xi=26.2$ µm, $v=9.92$ mm/s, $a=3.75$ m/s² | 2.62e-5 m, 9.9e-3, 3.75 ✔ |
| 3 (d) | $F_f=5.49$ N (b), 0.625 N (c) | 5.5 N, 0.62 N ✔ |
| 4.1 | $u/u_f=1/(1-\omega^2/\omega_0^2)$ | same ✔ |
| 4.2 | $s=3.36\times10^3$ N/m, $u_0=4.4$ mm, avoid $\omega_0=47.4$ rad/s (7.54 Hz) | 3.37e3, 4.4e-3 m, 47.4 rad/s / 7.54 Hz ✔ |

## Problem 1 — Two springs and two masses: natural frequencies

**Given:** two springs of stiffness $s$, two masses $m$, four arrangements. Find $f_0$ for each.

> [!hint] Start here
> Reduce every sketch to one spring $s_{eq}$ and one mass $m_{eq}$, then $f_0=\frac1{2\pi}\sqrt{s_{eq}/m_{eq}}$. Parallel springs share the deflection (stiffnesses add). Series springs share the force (compliances add).

**(a) Two springs side by side holding one mass.** Same deflection $\xi$ for both, forces add: $F=\xi(s_1+s_2)$, so $s_{eq}=2s$:
$$f_a=\frac1{2\pi}\sqrt{\frac{2s}{m}}$$

**(b) One spring, two masses stacked.** $m_{eq}=2m$:
$$f_b=\frac1{2\pi}\sqrt{\frac{s}{2m}}$$

**(c) Two springs in a chain, one mass at the bottom.** The same force goes through both; the deflections add: $\xi=F(1/s_1+1/s_2)$, so $s_{eq}=s_1s_2/(s_1+s_2)=s/2$:
$$f_c=\frac1{2\pi}\sqrt{\frac{s}{2m}}$$

**(d) Mass between a spring to the ceiling and a spring to the floor.** Move the mass down by $\xi$: the top spring stretches, the bottom one compresses, and **both** push it back. Same deflection, forces add: parallel, $2s$:
$$f_d=\frac1{2\pi}\sqrt{\frac{2s}{m}}$$

(a) and (d) are **twice** the frequency of (b) and (c), an octave apart. (d) is the trap: it *looks* like a series chain.

## Problem 2 — Suspension of a small vibration exciter

**Given:** four leaf springs of $s=0.5$ N/mm $=500$ N/m each, coil + table $m=18$ g. (b) a payload $M=200$ g is fixed to the table.

> [!hint] Start here
> All four springs hold the same table and deflect equally: parallel.

**(a)** $s_{eq}=4s=2000$ N/m.
$$f_a=\frac1{2\pi}\sqrt{\frac{4s}{m}}=\frac1{2\pi}\sqrt{\frac{2000}{0.018}}=\boxed{53.05\ \mathrm{Hz}}$$

**(b)** The payload's weight sinks the table by
$$\xi_{\rm stat}=\frac{Mg}{4s}=\frac{0.2\cdot9.81}{2000}=\boxed{0.981\ \mathrm{mm}}\approx1\ \mathrm{mm}$$
and the new natural frequency uses the total moving mass:
$$f_b=\frac1{2\pi}\sqrt{\frac{4s}{m+M}}=\frac1{2\pi}\sqrt{\frac{2000}{0.218}}=\boxed{15.24\ \mathrm{Hz}}$$

Check with the static-deflection rule: the total deflection under $(m+M)$ is $1.069$ mm, $0.5/\sqrt{0.001069}=15.3$ Hz ✔. The payload is 11× the moving mass, so $f_0$ falls by $\sqrt{12.1}=3.5$. An exciter's own resonance moves a lot with what you bolt onto it.

## Problem 3 — Undamped mass–spring driven by a harmonic force

**Given:** $s=23.8\times10^3$ N/m, $m=1.5$ kg, $|F_0|=5$ N, no damping. (b) $\omega=37.8$ rad/s, (c) $\omega=378$ rad/s, (d) force on the foundation in both cases.

> [!hint] Start here
> $(s-\omega^2m)\,\xi=F$. Velocity and acceleration are $\omega$ and $\omega^2$ times the displacement. Undamped, the force on the floor is the spring force $s\xi$.

**(a)**
$$\omega_0=\sqrt{\frac sm}=\sqrt{\frac{23800}{1.5}}=125.96\ \mathrm{rad/s},\qquad f_0=\boxed{20.05\ \mathrm{Hz}}$$

**(b) $\omega=37.8$ rad/s, $\Omega=0.300$** (below resonance, stiffness controlled):
$$|\xi|=\frac{|F_0|}{s\,|1-\Omega^2|}=\frac{5}{23800\cdot0.910}=\boxed{0.231\times10^{-3}\ \mathrm m}$$
$$|v|=\omega|\xi|=\boxed{8.73\times10^{-3}\ \mathrm{m/s}},\qquad |a|=\omega^2|\xi|=\boxed{0.330\ \mathrm{m/s^2}}$$
Almost the static deflection, $F/s=0.210$ mm, raised 10 % by the approaching resonance.

**(c) $\omega=378$ rad/s, $\Omega=3.00$** (above resonance, mass controlled):
$$|\xi|=\frac{5}{23800\cdot|1-9.006|}=\boxed{2.62\times10^{-5}\ \mathrm m},\quad |v|=\boxed{9.92\times10^{-3}\ \mathrm{m/s}},\quad |a|=\boxed{3.75\ \mathrm{m/s^2}}$$
Check: mass controlled means $|a|\approx F/m=3.33$; the exact value is $3.33\cdot9/8=3.75$ ✔. The displacement is 8.8× smaller than in (b), but the acceleration is 11× larger.

**(d) Force on the foundation**, $|F_f|=s|\xi|$:
$$\text{(b)}\ \ |F_f|=23800\cdot0.231\times10^{-3}=\boxed{5.49\ \mathrm N},\qquad\text{(c)}\ \ |F_f|=23800\cdot2.62\times10^{-5}=\boxed{0.625\ \mathrm N}$$

As a transmissibility, $T=1/|1-\Omega^2|$: **1.10 (+0.8 dB)** at 37.8 rad/s — more force on the floor than you put in — and **0.125 (−18.1 dB)** at 378 rad/s. Same mounting, the only difference is which side of $\sqrt2f_0=28.4$ Hz the excitation sits ($f=6.0$ and $60.2$ Hz).

## Problem 4 — Instrument on a vibrating train floor (base excitation)

**Given:** the floor moves as $u_f(t)=\Re\{u_fe^{j\omega t}\}$; the instrument (mass $m$) sits on a spring $s$. 4.2: wanted $u/u_f=-0.1$ at $\omega=2\pi\cdot25=157.1$ rad/s, $m=1.5$ kg.

> [!hint] Start here
> The spring is compressed by the **difference** $u_f-u$. Newton on the mass, then put in $e^{j\omega t}$.

### 4.1 Equation of motion and the ratio

$$m\ddot u=s(u_f-u)\quad\Longleftrightarrow\quad m\ddot u+su=su_f$$
With $e^{j\omega t}$: $(s-\omega^2m)\,u=s\,u_f$,
$$\boxed{\frac{u}{u_f}=\frac{s}{s-\omega^2m}=\frac{1}{1-(\omega/\omega_0)^2}},\qquad\omega_0=\sqrt{s/m}$$
This is the undamped transmissibility again (deck page 29: motion excitation gives the same curve as force transmission).

### 4.2 Stiffness, static deflection, frequency to avoid

Solve the ratio for $s$:
$$s\Big(1-\frac{u}{u_f}\Big)=-\frac{u}{u_f}\,\omega^2m\ \Rightarrow\ s=\frac{-(u/u_f)\,\omega^2m}{1-u/u_f}=\frac{0.1\cdot157.1^2\cdot1.5}{1.1}=\boxed{3.36\times10^{3}\ \mathrm{N/m}}$$

Why −0.1 and not +0.1: above resonance the mass moves in **antiphase** with the floor, so a small ratio is negative. With +0.1 you would need $1-\Omega^2=10$, so $\Omega^2=-9$: no real solution (the formula would hand you a negative stiffness). The sign is not optional. With −0.1, $1-\Omega^2=-10$, so $\Omega^2=11$ and $\Omega=3.32$.

Static deflection:
$$u_0=\frac{mg}{s}=\frac{1.5\cdot9.82}{3365}=\boxed{4.4\times10^{-3}\ \mathrm m}$$

Avoid the resonance, where $u/u_f\to\infty$:
$$\omega_0=\sqrt{\frac{3365}{1.5}}=\boxed{47.4\ \mathrm{rad/s}},\qquad f_0=\boxed{7.54\ \mathrm{Hz}}$$

Check with the rule of thumb: $0.5/\sqrt{0.0044}=7.56$ Hz ✔. A 4.4 mm sag is right in the course text's practical 4–10 mm window. In practice: if the train also runs at speeds where the motor excites 5–11 Hz, this mounting amplifies the vibration instead.

## Takeaways

1. **Reduce to one $s$ and one $m$.** Parallel springs (same deflection) add; series springs (same force) add compliances; a mass between two springs sees them in parallel.
2. **The static deflection is the natural frequency:** $f_0\approx0.5/\sqrt{\xi_0}$, mass-independent.
3. **Below $\sqrt2f_0$ a spring mount amplifies; above it isolates**, 12 dB/octave undamped. $\Omega=3$ → −18 dB.
4. **Force excitation of a machine and motion excitation of an instrument** give the same ratio, $1/(1-\Omega^2)$ undamped.
5. **Above resonance the ratio is negative** (antiphase); carry the sign when you solve for $s$.
