---
course: "34840"
type: exercise
date: 2026-10-06
week: 41
lecture: 6
tags: [Acoustics, exercises, room-acoustics, room-modes, reverberation-time, diffuse-field]
---
# Week 6 — Room Modes and the Diffuse Sound Field

Source: [[34840_Problems_roomacoustics6.pdf|Week 6 sheet]] · official solutions [[Solution 6.pdf|Solution 6]]. Theory: [[Lecture 6 - Room Modes and the Diffuse Sound Field]]. [Interactive problems and benches](https://study.madsrudolph.dev/34840/#l6).

Every answer below was checked against the official solutions and the answers printed on the sheet. Constants: $c=343\ \mathrm{m/s}$ (20 °C, as the sheet says; $331.3\sqrt{293.15/273.15}=343.2$), $\rho=1.2\ \mathrm{kg/m^3}$, so $\rho c=411.6\ \mathrm{Pa\,s/m}$. All pressures are RMS. $p_0=20\,\mu$Pa.

## Answers at a glance

| Problem | Result | Official |
|---|---|---|
| 1.1 | 34.3, 42.9, 54.9, 57.2, 66.7, 68.6, 71.5, 79.3 Hz | sheet: same ✔; Solution 6 prints **34.4** for (1,0,0), a slip (see below) |
| 1.2 | Only (2,0,0) | (2,0,0) ✔ |
| 1.3 | Band 44.5–56.1 Hz: only (1,1,0) at 54.9 Hz | (1,1,0) ✔ |
| 2.1 | 57.2 Hz (×3), 80.8 Hz (×3), 114.3 Hz (×3), 127.8 Hz (×6) | 57, 81, 114, 128 Hz ✔ |
| 3.1 | $A=10.9$ m², $L_p=95.8$ dB while on, $L_{\rm eq}=91.0$ dB | 91 dB ✔ |
| 3.2 | Source 2: $P=1.95$ mW, reverberant 88.7 dB; total $L_{\rm eq}=93.0$ dB | 93 dB ✔ |

## Problem 1 — Modes of a 5 × 4 × 3 m room

**Given:** $l_x=5$ m, $l_y=4$ m, $l_z=3$ m, rigid walls, 20 °C.

> [!hint] Start here
> Write the eigenfrequency formula with the three "axial building blocks" $c/2l$ pulled out: $f=\sqrt{(n_xf_x)^2+(n_yf_y)^2+(n_zf_z)^2}$. Then try small index combinations in order.

### 1.1 All natural frequencies below 80 Hz

$$f_{n_x,n_y,n_z}=\sqrt{\left(n_x\frac{c}{2l_x}\right)^2+\left(n_y\frac{c}{2l_y}\right)^2+\left(n_z\frac{c}{2l_z}\right)^2}$$
The building blocks:
$$f_x=\frac{343}{10}=34.30\ \mathrm{Hz},\qquad f_y=\frac{343}{8}=42.88\ \mathrm{Hz},\qquad f_z=\frac{343}{6}=57.17\ \mathrm{Hz}.$$
Combine them:

| Mode | Type | Calculation | $f$ (Hz) |
|---|---|---|---|
| (1,0,0) | axial | $34.30$ | **34.3** |
| (0,1,0) | axial | $42.88$ | **42.9** |
| (1,1,0) | tangential | $\sqrt{34.30^2+42.88^2}$ | **54.9** |
| (0,0,1) | axial | $57.17$ | **57.2** |
| (1,0,1) | tangential | $\sqrt{34.30^2+57.17^2}$ | **66.7** |
| (2,0,0) | axial | $2\times34.30$ | **68.6** |
| (0,1,1) | tangential | $\sqrt{42.88^2+57.17^2}$ | **71.5** |
| (1,1,1) | oblique | $\sqrt{34.30^2+42.88^2+57.17^2}$ | **79.3** |

The next ones are (2,1,0) at 80.9 Hz and (0,2,0) at 85.8 Hz, both just above the limit.
$$\boxed{34.3,\ 42.9,\ 54.9,\ 57.2,\ 66.7,\ 68.6,\ 71.5,\ 79.3\ \mathrm{Hz}}$$
Sanity check with the mode-count formula (Lecture 6 §5): $V=60$, $S=94$, $L=48$ gives $N(80)=3.2+4.0+1.4=8.6$, against 8 counted. ✔

**Official:** the sheet gives exactly these eight values. Solution 6 prints **34.4 Hz** for (1,0,0) but the same seven others. 34.4 Hz would need $c=344$, and then (0,1,0) would be 43.0, (1,1,0) 55.1 and (1,1,1) 79.5 Hz, which the solution does not show. So 34.4 is a rounding slip in the solution, not a different assumption. 34.3 Hz is right at 20 °C.

### 1.2 Which of these have a pressure maximum at the centre?

At the centre $x=l_x/2$, so each factor is $\cos(n\pi/2)$:
- $n$ odd: $\cos(\pi/2)=0$, a **nodal plane** through the centre.
- $n$ even (including 0): $\cos(n\pi/2)=\pm1$, a maximum.

A mode has a pressure maximum at the centre only if **all three indices are even**. In the list, only (2,0,0) qualifies (0 counts as even).
$$\boxed{\text{only }(2,0,0)}$$
**Official:** (2,0,0). ✔ This is slide 19's question 1: a microphone in the middle of the room is deaf to (1,0,0).

### 1.3 Modes in the 50 Hz third-octave band

$$f_l=\frac{50}{2^{1/6}}=44.5\ \mathrm{Hz},\qquad f_u=50\cdot2^{1/6}=56.1\ \mathrm{Hz}.$$
From the table: 42.9 Hz is just below, 57.2 Hz just above, and only 54.9 Hz falls inside.
$$\boxed{\text{only }(1,1,0)\text{ at }54.9\ \mathrm{Hz}}$$
The mode-count formula predicts $N(56.1)-N(44.5)=1.5$ modes: close, but at this low frequency the real answer is the discrete count. One mode per third-octave band is why small rooms sound "boomy" at specific notes.

**Official:** band 44.5–56.1 Hz, only (1,1,0). ✔

## Problem 2 — Degenerate modes in a 3 m cube

**Given:** $l_x=l_y=l_z=3$ m.

> [!hint] Start here
> With equal sides, $f=\dfrac{c}{2l}\sqrt{n_x^2+n_y^2+n_z^2}$. The frequency only depends on $n_x^2+n_y^2+n_z^2$, so every **permutation** of the indices gives the same frequency. List the possible sums of three squares in increasing order and count the permutations.

$$\frac{c}{2l}=\frac{343}{6}=57.17\ \mathrm{Hz}$$

| $n_x^2+n_y^2+n_z^2$ | Modes | Number | $f$ (Hz) | Degenerate? |
|---|---|---|---|---|
| 1 | (1,0,0), (0,1,0), (0,0,1) | 3 | $57.17\sqrt1=$ **57.2** | yes |
| 2 | (1,1,0), (1,0,1), (0,1,1) | 3 | $57.17\sqrt2=$ **80.8** | yes |
| 3 | (1,1,1) | 1 | $57.17\sqrt3=99.0$ | **no**, only one mode |
| 4 | (2,0,0), (0,2,0), (0,0,2) | 3 | $57.17\sqrt4=$ **114.3** | yes |
| 5 | (2,1,0), (2,0,1), (1,2,0), (1,0,2), (0,1,2), (0,2,1) | 6 | $57.17\sqrt5=$ **127.8** | yes |

$$\boxed{57\ \mathrm{Hz},\ 81\ \mathrm{Hz},\ 114\ \mathrm{Hz},\ 128\ \mathrm{Hz}}$$
The trap is (1,1,1) at 99 Hz: it is the third-lowest frequency, but nothing coincides with it, so it does not count. The next degenerate group would be (2,1,1) etc. at $57.17\sqrt6=140$ Hz.

Why this matters: the cube has only 5 distinct frequencies below 130 Hz, carrying 16 modes. The transfer function has a few huge peaks with wide gaps between them, the opposite of what a listening room or a measurement room needs. Hence the design rule of non-simple dimension ratios.

**Official:** 57, 81, 114, 128 Hz with the same mode lists. ✔

## Problem 3 — Intermittent and steady sources in a reverberant room

**Given:** source 1: $P_1=10$ mW in the 500 Hz octave band, on 5 min, off 10 min. Room $V=210$ m³, $T=3.1$ s in that band. Later, source 2: continuous, $L_p=70$ dB at 4 m in free field (500 Hz octave). The two are uncorrelated.

> [!hint] Start here
> "Where the reverberant field dominates" is the cue for $p^2=4P\rho c/A$. You are given $T$ instead of $A$, so get $A$ from Sabine first. For the equivalent level, average $p^2$ over time (on 1/3 of the time), not the dB value.

### 3.1 Equivalent level from source 1

**Absorption area from Sabine:**
$$A=\frac{55.3\,V}{cT}=\frac{55.3\cdot210}{343\cdot3.1}=10.92\ \mathrm{m^2}$$
**Reverberant pressure while the source is on:**
$$p_{\rm on}^2=\frac{4P_1\rho c}{A}=\frac{4(0.010)(411.6)}{10.92}=1.508\ \mathrm{Pa^2}\quad(p_{\rm on}=1.228\ \mathrm{Pa})$$
$$L_{p,\rm on}=10\log_{10}\frac{1.508}{(20\times10^{-6})^2}=95.8\ \mathrm{dB}$$
**Time average.** The cycle is 15 min with 5 min on, and the averaging time is a whole number of cycles, so the mean-square pressure is 1/3 of the on-value:
$$L_{\rm eq}=10\log_{10}\frac{p_{\rm on}^2/3}{p_0^2}=95.8-10\log_{10}3=95.8-4.8=\boxed{91.0\ \mathrm{dB}}$$
The build-up and decay take only a fraction of a second ($T=3.1$ s against 5 min on), so treating the level as a square wave is fine. The reverberation distance is $\sqrt{A/16\pi}=0.47$ m: practically every position in the room is in the reverberant field, so the answer holds almost everywhere. The Schroeder frequency $2000\sqrt{3.1/210}\approx240$ Hz is well below 500 Hz, so the diffuse-field formula is justified.

Shortcut with the dB form: $L_W=10\log(0.01/10^{-12})=100$ dB, $L_p\approx L_W+10\log(4/A)=100-4.36=95.6$ dB, plus the neglected constant $10\log(\rho c\,P_{\rm ref}/p_0^2)=0.12$ dB (0.14 dB in the text, which uses $\rho=1.204$) = 95.8 dB.

**Official:** $p_{\rm rms}=1.23$ Pa, mean square ÷3, ≈ 91 dB. ✔

### 3.2 Both sources

**Power of source 2 from its free-field level** (monopole, $I=p^2/\rho c$ at any distance, Lecture 5):
$$p_{\rm ff}^2=(20\times10^{-6}\cdot10^{70/20})^2=4.0\times10^{-3}\ \mathrm{Pa^2}\quad(0.0632\ \mathrm{Pa})$$
$$P_2=\frac{p_{\rm ff}^2}{\rho c}4\pi r^2=\frac{4.0\times10^{-3}}{411.6}\,4\pi(4)^2=1.954\times10^{-3}\ \mathrm W\approx2\ \mathrm{mW}$$
**Its reverberant pressure in the room:**
$$p_2^2=\frac{4P_2\rho c}{A}=\frac{4(1.954\times10^{-3})(411.6)}{10.92}=0.2946\ \mathrm{Pa^2}\quad(p_2=0.543\ \mathrm{Pa},\ 88.7\ \mathrm{dB})$$
Neat check: $\rho c$ cancels, $p_2^2=p_{\rm ff}^2\cdot16\pi r^2/A$, so $L_2=70+10\log(16\pi\cdot16/10.92)=70+18.7=88.7$ dB.

**Uncorrelated, so add mean squares** (source 1 time-averaged, source 2 continuous):
$$L_{\rm eq}=10\log_{10}\frac{p_{\rm on}^2/3+p_2^2}{p_0^2}=10\log_{10}\frac{0.5027+0.2946}{4\times10^{-10}}=\boxed{93.0\ \mathrm{dB}}$$
In dB terms: $91.0\oplus88.7=93.0$ dB.

**Official:** $P=2$ mW, $p=0.54$ Pa, $10\log\big((1.23^2/3+0.54^2)/(20\times10^{-6})^2\big)=93$ dB. ✔

> [!note] Wording slip in Solution 6
> 3-2 says "Sound pressure of the source: $P_a=\dots=2$ mW". It means sound **power**. The formula and number are right.

> [!note] Why no $(1-\bar\alpha)$?
> The full formula has $p_{\rm rev}^2=4P\rho c(1-\bar\alpha)/A$. We do not know $S$ here, so $\bar\alpha$ is unknown; but a 210 m³ room has $S\approx210$ m², giving $\bar\alpha\approx0.05$ and a correction of only −0.2 dB. The official solution ignores it too.

## MATLAB learning document

Open [the MATLAB script](../../../../../5.%20Semester/Acoustics%20and%20Noise%20Control/Matlab/Week6_Room_Acoustics.m) under `5. Semester/Acoustics and Noise Control/Matlab/`. Each formula is written first as an equation, then calculated in one plain MATLAB line, with the official answer in a comment beside it. It covers every problem plus the lecture's Sabine/Eyring example, the mode count and the reverberation distance.
