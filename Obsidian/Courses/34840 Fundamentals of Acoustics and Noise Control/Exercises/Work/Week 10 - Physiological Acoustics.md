---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: exercise
date: 2026-11-10
week: 46
lecture: 10
topic: "Physiological acoustics"
lecturer: Torsten Dau
tags: [Acoustics, exercises, physiological-acoustics, greenwood, cochlea, ABR, signal-averaging, artifact-rejection, otoacoustic-emissions]
---
# Week 10 — Physiological Acoustics

Source: [[34840_Physiological_Acoustics_Exercise_2026.pdf|Physiological Acoustics exercise (3 problems)]]. Official solutions: [[34840_Physiological_Acoustics_Solutions_2026.pdf|Physiological Acoustics solutions]]. Theory: [[Lecture 10 - Physiological Acoustics]]. MATLAB: `5. Semester/Acoustics and Noise Control/Matlab/Week10_Physiological_Acoustics.m`.

> [!info] Checked against the official solutions
> Every answer below was derived first and then compared with the official solution sheet and with `Week10_Physiological_Acoustics.m` (headless run, 26-Nov-2026). **All answers agree.** The only difference is rounding: the official 24 Hz is 23.7 Hz. Written after the lecture from the deck and the sheets; there is no recording.

No acoustic constants are needed this week. Everything is the Greenwood map, the $\sqrt n$ averaging law, and a speed.

## Answers at a glance

| Question | My result | Official | |
|---|---|---|---|
| 1, highest | 20 541 Hz at the base ($x=0$) | 20 541 Hz (base) | ✔ |
| 1, lowest | 23.7 Hz at the apex ($x=34$ mm) | 24 Hz (apex) | ✔ |
| 2a | SNR = 0.1 = −20 dB; doubling $n$: +3.01 dB | same | ✔ |
| 2b | $n=1000$ sweeps, 50 s | same | ✔ |
| 2c, all 1000 averaged | $P=98.1\ \mu\mathrm V^2$, $N_{\rm eff}=9.905\ \mu$V, $\bar N=0.3132\ \mu$V, SNR = −0.37 dB | same | ✔ |
| 2c, +10 dB no rejection | 10 900 sweeps, 545 s | same | ✔ |
| 2c, +10 dB with rejection | 1000 clean / 1111 presented, 55.6 s; ratio 9.8 | same | ✔ |
| 3 | 18 / 10.5 / 7.5 mm → 1458.3 / 4505.2 / 6977.4 Hz | same | ✔ |

## Problem 1 — Greenwood: the lowest and highest frequency

**Given:** cochlea as a cascade of low-pass filters, cut-off $F_c=A\cdot10^{-Gx}-B$ with $A=20682$, $G=61.765$, $B=140.6$, $x$ from the base, cochlear length 34 mm. Find the lowest and highest frequency and where they sit.

> [!hint] Start here
> $G=61.765$ only makes sense per **metre** ($61.765\times0.034=2.1$). The highest frequency is where the formula is largest, which is the smallest $x$.

Base, $x=0$:
$$F_{\rm high}=20682\cdot10^{0}-140.6=\boxed{20\,541\ \mathrm{Hz}}\quad\text{(at the base, next to the stapes)}$$

Apex, $x=0.034$ m:
$$10^{-61.765\cdot0.034}=10^{-2.100}=7.943\times10^{-3},\qquad F_{\rm low}=164.3-140.6=\boxed{23.7\ \mathrm{Hz}}\quad\text{(at the apex, by the helicotrema)}$$

That is the textbook 20 Hz–20 kHz. Note the size of the $-B$ term: it is negligible at the base and decides the answer at the apex (without it you'd get 164 Hz).

![[Courses/34840 Fundamentals of Acoustics and Noise Control/Images/Lecture10/greenwood_map.png]]

Why a *cascade of low-pass* filters (the sheet's footnote): sound enters at the base and has to pass every section on its way. Each section passes frequencies below its cut-off and kills those above. A tone travels until it reaches the section whose cut-off equals its frequency and then stops. That is the travelling wave's steep apical cliff from the lecture (pages 17–18) in filter language.

## Problem 2 — Averaging the ABR

**Given:** $S=EP+N$, $EP=0.3\ \mu$V, $N=3\ \mu$V per sweep, 20 sweeps/s, EP identical every sweep, noise independent from sweep to sweep.

> [!hint] Start here
> The sum of $n$ identical EPs is $n\cdot EP$. The sum of $n$ independent noises has **power** $nN^2$, so amplitude $\sqrt n\,N$. Divide both by $n$: the average keeps $EP$ and has noise $N/\sqrt n$.

### 2a. One sweep, and doubling

$$\mathrm{SNR}_1=\frac{EP}{N}=\frac{0.3}{3}=\boxed{0.1},\qquad 20\log_{10}0.1=\boxed{-20\ \mathrm{dB}}$$

After averaging $\mathrm{SNR}_{\rm avg}=\mathrm{SNR}_1\sqrt n$. Doubling $n$:
$$\Delta=20\log_{10}(\mathrm{SNR}_1\sqrt{2n})-20\log_{10}(\mathrm{SNR}_1\sqrt n)=20\log_{10}\sqrt2=10\log_{10}2=\boxed{+3.01\ \mathrm{dB}}$$

### 2b. Sweeps for +10 dB

$$n=\left(\frac{10^{10/20}}{0.1}\right)^2=\left(\frac{3.162}{0.1}\right)^2=\boxed{1000\ \text{sweeps}},\qquad t=\frac{1000}{20}=\boxed{50\ \mathrm s}$$

Quick check in dB: from −20 to +10 is +30 dB $=10\log_{10}n$ → $n=10^3$.

### 2c. Artifacts in 10 % of the sweeps

**Given:** 10 % of sweeps have $N_2=30\ \mu$V (swallowing, movement), 90 % have $N_1=3\ \mu$V.

> [!hint] Start here
> Mean noise **power** per sweep, then pretend every sweep has that power: $N_{\rm eff}=\sqrt P$. After that, the same $N_{\rm eff}/\sqrt n$ law.

$$P=\frac{900\cdot3^2+100\cdot30^2}{1000}=\frac{8100+90\,000}{1000}=\boxed{98.1\ \mu\mathrm V^2},\qquad N_{\rm eff}=\sqrt{98.1}=\boxed{9.905\ \mu\mathrm V}$$

The 100 bad sweeps carry 92 % of the noise power. All 1000 averaged:
$$\bar N=\frac{9.905}{\sqrt{1000}}=\boxed{0.3132\ \mu\mathrm V},\qquad \mathrm{SNR}_{\rm avg}=20\log_{10}\frac{0.3}{0.3132}=\boxed{-0.37\ \mathrm{dB}}$$
instead of +10 dB with clean sweeps. The artifacts cost 10.4 dB.

**+10 dB without rejection.** Target residual noise $N_{\rm target}=0.3/10^{10/20}=0.0949\ \mu$V:
$$n=\frac{P}{N_{\rm target}^2}=\frac{98.1}{0.0949^2}=\boxed{10\,900\ \text{sweeps}},\qquad t=\frac{10\,900}{20}=\boxed{545\ \mathrm s}\ (9\ \text{min})$$

**+10 dB with rejection.** Throw the artifact sweeps away; only clean ones are averaged:
$$n_{\rm clean}=\left(\frac{N_1}{N_{\rm target}}\right)^2=\left(\frac{3}{0.0949}\right)^2=1000,\qquad n_{\rm total}=\frac{1000}{0.9}=\boxed{1111\ \text{sweeps}},\qquad t=\boxed{55.6\ \mathrm s}$$

**Comparison:** $545/55.6=\boxed{9.8}$. Rejecting 10 % of the sweeps makes the recording almost ten times faster. Every clinical ABR system has an artifact-rejection threshold for this reason.

![[Courses/34840 Fundamentals of Acoustics and Noise Control/Images/Lecture10/abr_averaging_snr.png]]

> [!warning] The wrong way that looks right
> Averaging the noise **amplitudes**: $0.9\cdot3+0.1\cdot30=5.7\ \mu$V. That underestimates the noise (the big sweeps count with their square) and would give 3610 sweeps instead of 10 900.

## Problem 3 — Click-evoked OAE: roundtrip → frequency

**Given:** click-evoked emission with three components at 12, 7 and 5 ms; wave speed in the cochlea 3 m/s. Which frequencies?

> [!hint] Start here
> Roundtrip = to the CF place and back, so the place is at speed × **half** the time. Then Greenwood from Problem 1.

$$x=c\cdot\frac{t_{\rm rt}}{2}:\qquad 3\cdot0.006=0.018\ \mathrm m,\quad 3\cdot0.0035=0.0105\ \mathrm m,\quad 3\cdot0.0025=0.0075\ \mathrm m$$

$$F=20682\cdot10^{-61.765x}-140.6$$

| Roundtrip | One way | $x$ | $10^{-Gx}$ | $F$ |
|---|---|---|---|---|
| 12 ms | 6 ms | 18 mm | 0.07730 | **1458.3 Hz** |
| 7 ms | 3.5 ms | 10.5 mm | 0.22463 | **4505.2 Hz** |
| 5 ms | 2.5 ms | 7.5 mm | 0.34416 | **6977.4 Hz** |

The latest component is the lowest frequency: it had the furthest to go. That is cochlear dispersion.

> [!note] What the model leaves out
> It puts all of the delay in the cochlea at a constant 3 m/s. In a real ear the travelling wave slows down as it approaches its CF place (lecture page 17), there is a little ear-canal and middle-ear delay, and the emission is generated over a region rather than at one point. Fine for the exercise; don't quote it as physiology.

## Takeaways

- Greenwood: $x$ in metres from the base. Base = 20.5 kHz, apex = 24 Hz. About 4.9 mm per octave in the high-frequency half.
- Averaging: SNR grows as $\sqrt n$ → $+10\log_{10}n$ dB → +3 dB per doubling, +10 dB per decade.
- Mixed noise: average the **powers**, then take the square root.
- Artifact rejection costs you the rejected sweeps but saves far more than it costs when the artifacts are big.
- OAE latency: halve it, multiply by the speed, look up the frequency.
