---
course: "34840"
type: exercise
date: 2026-10-20
week: 43
lecture: 7
tags: [Acoustics, exercises, absorption, reverberation-room, membrane-absorber, perforated-panel]
---
# Week 7 — Sound Absorbers

Source: [[34840_Problems_soundabsorbers7.pdf|Week 7 sheet ("Room acoustic problems", 2 problems)]]. Official solutions: **not published yet** (they usually appear a week later). Theory: [[Lecture 7 - Sound Absorption and Room Acoustic Design]]. [Interactive problems and benches](https://study.madsrudolph.dev/34840/#l7).

> [!warning] Derived, not yet checked against official solutions
> Every answer below is my own derivation, checked numerically in Python and in `Week7_Sound_Absorbers.m`. The sheet prints a final answer for each question, and every result matches those printed answers. The worked routes have not yet been compared with an official solution document.

Constants: $\rho=1.2\ \mathrm{kg/m^3}$, $c=344\ \mathrm{m/s}$, so $\rho c^2=1.42\times10^5$ Pa (the slides round to $1.4\times10^5$). Sabine: $T=0.16V/A$.

## Answers at a glance

| Question | Result | Printed on the sheet |
|---|---|---|
| 1.1 | $\alpha_{500}=0.451$ | 0.45 ✔ |
| 1.2 | $S=61.4\ \mathrm{m^2}$, so **62 m²** | 62 m² ✔ |
| 2.1 | $f_r=77.4$ Hz (76.9 Hz with the slide's $1.4\times10^5$) | 77 Hz ✔ |
| 2.2 | $P=8.73\,\%$, $f_0=432$ Hz | 432 Hz ✔ (also slide 28) |
| Slide 5 | Reflected 67.0 / 60.0 / 50.0 dB | Not printed |
| Slide 25 | DR Studio 1 resonators ≈ 98 Hz and 64 Hz | Hidden on the slide |
| Slide 36 | $\alpha_n=0.451$, $\alpha_r=0.53$ | 0.4511, 0.53 ✔ |

## Problem 1 — Absorbing a lecture hall, with the material tested in a reverberation room

**Given:**
- Lecture hall: $V=300$ m³, furnished and empty, $T_{500}=3.1$ s now. Target **0.8 s with 40 students** present, each adding $A_{\rm student}=0.42$ m² at 500 Hz.
- Test: 10 m² sample in a 200 m³ reverberation chamber. $T_{\rm empty}=5.2$ s, $T_{\rm sample}=3.0$ s.
- Both rooms ideally diffuse. Neglect the absorption of the wall/ceiling surfaces that get covered.

> [!hint] Start here
> Work in absorption areas $A=0.16V/T$ (m²), never in reverberation times directly: absorption areas add, reverberation times don't. In the chamber, the sample's absorption is the **difference** between the two $A$ values.

### 1.1 Absorption coefficient of the material

The sample adds absorption area $\Delta A=S\alpha$ (ISO 354, slide 40):
$$A_{\rm empty}=\frac{0.16\cdot200}{5.2}=6.154\ \mathrm{m^2},\qquad A_{\rm sample}=\frac{0.16\cdot200}{3.0}=10.667\ \mathrm{m^2}$$
$$\alpha=\frac{A_{\rm sample}-A_{\rm empty}}{S}=\frac{0.16V}{S}\left(\frac1{T_2}-\frac1{T_1}\right)=\frac{32}{10}(0.3333-0.1923)=\boxed{0.451}$$

The $+\alpha_{\rm wall}$ term of the full formula is dropped: the chamber's surface area is not given, and the sheet says to ignore it. (A concrete chamber has $\alpha_{\rm wall}\approx0.01$–0.02, which would add that much.)

### 1.2 Area needed in the lecture hall

$$A_{\rm now}=\frac{0.16\cdot300}{3.1}=15.48\ \mathrm{m^2}\qquad\text{(room + furniture, no people)}$$
$$A_{\rm target}=\frac{0.16\cdot300}{0.8}=60.0\ \mathrm{m^2}$$
$$A_{\rm students}=40\cdot0.42=16.8\ \mathrm{m^2}$$
$$A_{\rm material}=60.0-15.48-16.8=27.72\ \mathrm{m^2}$$
$$S=\frac{27.72}{0.451}=61.4\ \mathrm{m^2}\ \Rightarrow\ \boxed{62\ \mathrm{m^2}}$$

Round **up**, otherwise the target is missed by a hair. With the rounded $\alpha=0.45$ the quotient is 61.6, which also gives 62.

**Check:** $T=48/(15.48+16.8+62\cdot0.451)=0.797$ s ✔.

**What was neglected:** the covered surfaces used to contribute about $62\cdot0.02\approx1$ m², which strictly should be subtracted (it is replaced by the new material). That would raise the area by about 4 % (to about 64 m²). The sheet tells you to ignore it.

## Problem 2 — Plywood panel absorber, then perforated

**Given:** plywood $h=20$ mm, $\rho_p=600$ kg/m³, $L=50$ mm in front of a hard wall, cavity closed at the sides.

> [!hint] Start here
> 2.1 is the limp membrane formula. It needs the mass **per unit area** $m=\rho_ph$, not the density. 2.2 turns the same panel into a perforated-panel resonator: now the mass is the air in the holes, so the panel's own weight drops out.

### 2.1 Membrane resonance

$$m=\rho_p h=600\cdot0.020=12\ \mathrm{kg/m^2}$$
$$f_r=\frac1{2\pi}\sqrt{\frac{\rho c^2}{mL}}=\frac1{2\pi}\sqrt{\frac{1.42\times10^5}{12\cdot0.05}}=\frac{486.5}{2\pi}=\boxed{77\ \mathrm{Hz}}$$
(77.4 Hz with $c=344$; 76.9 Hz with the slide's $1.4\times10^5$; the rule of thumb $60/\sqrt{mL}=77.5$ Hz.)

Stiffness is neglected, as the sheet says: the panel is "large", so its bending modes are far below this, and eq. 4.5's stiffness term is small.

### 2.2 Perforated panel resonance

10 mm holes on a 30 mm square grid. Each hole owns a 30×30 mm patch of panel:
$$P=\frac{\pi d^2/4}{a^2}=\frac{\pi\cdot0.010^2/4}{0.030^2}=\frac{7.854\times10^{-5}}{9\times10^{-4}}=0.0873\ (8.7\,\%)$$
Neck length = panel thickness $l=20$ mm. End correction $\delta=0.8d=8$ mm, so $l+\delta=28$ mm.
$$f_0=\frac c{2\pi}\sqrt{\frac{P}{L(l+\delta)}}=\frac{344}{2\pi}\sqrt{\frac{0.0873}{0.05\cdot0.028}}=54.75\cdot\sqrt{62.33}=54.75\cdot7.895=\boxed{432\ \mathrm{Hz}}$$
(431 Hz with $c=343$.) Slide 28 is exactly this calculation.

**Why the frequency jumps from 77 to 432 Hz:** the spring (the 50 mm cavity) is the same. The mass changes. A per-unit-area equivalent mass for the holes is $\rho(l+\delta)/P=1.2\cdot0.028/0.0873=0.385$ kg/m², about 31 times lighter than the 12 kg/m² panel. $\sqrt{31}\approx5.6$, and $77\times5.6=432$ ✔. That is a neat check that the two formulas are the same mass–spring physics.

## Extra: in-lecture examples

### Slide 5 — Reflected SPL

Incident 70 dB, $\alpha=0.5,\ 0.9,\ 0.99$, angle-independent:
$$L_{\rm refl}=70+10\log_{10}(1-\alpha)=\boxed{67.0,\ 60.0,\ 50.0\ \mathrm{dB}}$$

### Slide 25 — Helmholtz resonators in the ceiling of DR Studio 1 (answer hidden on the slide)

Neck Ø65 mm, length 100 mm (my reading of the drawing): $s=\pi\cdot0.065^2/4=3.318\times10^{-3}$ m², $l+\delta=0.100+0.052=0.152$ m.

| Box $a\times b\times c$ (mm) | $V$ | $f_0=\dfrac c{2\pi}\sqrt{\dfrac{s}{V(l+\delta)}}$ |
|---|---|---|
| 150×150×300 | 6.75 L | **98 Hz** |
| 200×200×400 | 16.0 L | **64 Hz** |

Unchecked: the slide's own answer is hidden behind a green box. If the lecturer used no end correction, the values would be 121 and 79 Hz (my calculation).

### Slide 36 — α from a surface impedance $Z_n=500+j1000$ N·s/m³

$$R=\frac{Z_n-414}{Z_n+414}=0.5877+0.4511j,\qquad \alpha_n=1-|R|^2=\boxed{0.451}$$
$$\zeta=\frac{Z_n}{414}=1.208+2.415j\ \Rightarrow\ \alpha_r=\boxed{0.53}\ \text{(Paris formula, slide 35 (c))}$$
Without normalising: 0.0032. Numerically integrating $\int_0^{\pi/2}\alpha(\theta)\sin2\theta\,d\theta$ gives the same 0.531.
