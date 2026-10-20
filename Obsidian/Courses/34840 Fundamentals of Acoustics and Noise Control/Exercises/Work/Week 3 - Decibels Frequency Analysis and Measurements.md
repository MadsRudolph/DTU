---
course: "34840"
type: exercise
date: 2026-09-15
week: 38
lecture: 3
tags: [Acoustics, exercises, decibels, octave-bands, sound-level-meter]
---
# Week 3 — Decibels, Frequency Analysis and Measurements

Source: [[34840_Problems3.pdf|Week 3 sheet]] · official solutions [[34840_Solutions03.pdf|Solutions 03 (3 pages)]] · Matlab part: [[34840_SoundLevelMeter_Matlab_exercise_guide.pdf|SLM guide]] + [[Matlab_SLM_solution.zip|official SLM solution]]. Theory: [[Lecture 3 - Decibels Frequency Analysis and Measurements]]. [Interactive problems and benches](https://study.madsrudolph.dev/34840/#l3).

Every answer below was derived independently, checked numerically in Python, and compared with the official Solutions 03. **There is no numerical disagreement with the official solutions.** Reference pressure $p_{\rm ref}=20\ \mu\mathrm{Pa}$ throughout.

> [!note] Numbering
> The sheet labels the first two problems "Problem no 1.1" and "Problem no 1.2", each with sub-questions; the official solutions call them Problem 1 and Problem 2. This note follows the solutions: Problem 1 (two tones), Problem 2 (two loudspeakers), then 3–6.

## Answers at a glance

| Problem | Result | Official |
|---|---|---|
| 1.1 | $L_p=56.99\ \mathrm{dB}\approx57\ \mathrm{dB}$ | 57.0 dB |
| 1.2 | $L_p=60.0\ \mathrm{dB}$ (+3 dB) | 60.0 dB |
| 2.1 | In phase: $96.0\ \mathrm{dB}$ (+6.02 dB) | 96 dB |
| 2.2 | 120° phase lag: $90.0\ \mathrm{dB}$ (no change) | 90 dB |
| 2.3 | Different tones: $93.0\ \mathrm{dB}$ (+3.01 dB) | 93 dB |
| 3 | $f_0=769$ Hz; 1 kHz band **60 dB**, 2 kHz band **63 dB**, 4 kHz band **66 dB** (total 68.5 dB) | 60 / 63 / 66 dB |
| 4 | $\Delta f=57.8\ \mathrm{Hz}$ (1/12 octave at 1 kHz) | 57.8 Hz |
| 5 | $L_B=78.3\ \mathrm{dB}$ | 78.3 dB |
| 6 (Matlab) | 440HzSine 74.0 dB / 69.9 dB(A); ToneComplex 76.5 dB; NonStationaryNoise 85.0 dB (3–9 s), 82.0 dB (whole); B1 $L_{\rm eq}=82.1$, $L_{A,\rm eq}=74.4$ dB; DeepestBlues parts 74.4 / 82.0 / 85.8 dB | guide check values, all reproduced |

## Problem 1 — One tone, then a second tone 100 Hz higher

**Given:** pure tone, pressure amplitude (peak) $\hat p=0.02\ \mathrm{Pa}$. Then a second tone of equal amplitude at a frequency 100 Hz higher.

> [!hint] Start here
> SPL needs RMS, not amplitude. For the second part: are the two tones at the same frequency? If not, what happens to the cross term when you square and average?

### 1.1 Sound pressure level

$$p_{\rm rms}=\frac{\hat p}{\sqrt2}=\frac{0.02}{\sqrt2}=0.014142\ \mathrm{Pa},$$
$$L_p=20\log_{10}\frac{0.014142}{20\times10^{-6}}=\boxed{56.99\ \mathrm{dB}\approx57.0\ \mathrm{dB}}.$$
Using the amplitude directly would give 60.0 dB — the classic 3 dB error.

### 1.2 Both tones together

The frequencies differ, so $\overline{p_1p_2}=0$ (averaged over much more than the 10 ms beat period $1/100\ \mathrm{Hz}$). Mean squares add:
$$p^2_{\rm rms,tot}=p^2_{\rm rms,1}+p^2_{\rm rms,2}=2(0.014142)^2=4.0\times10^{-4}\ \mathrm{Pa^2},\qquad p_{\rm rms,tot}=0.0200\ \mathrm{Pa},$$
$$L_p=20\log_{10}\frac{0.0200}{20\times10^{-6}}=\boxed{60.0\ \mathrm{dB}}=57.0+10\log_{10}2.$$
Twice the power, +3 dB. **Official: 57.0 dB and 60.0 dB — agrees.** Funny coincidence: the total RMS (0.0200 Pa) equals the amplitude of one tone.

## Problem 2 — Two identical loudspeakers, same distance

**Given:** each loudspeaker alone gives $L_p=90$ dB at the point, same pure tone, free field, equal distances.

> [!hint] Start here
> Same signal → same frequency → add complex amplitudes. Write the second pressure as $p\,e^{j(\omega t-\varphi)}$ and find $|1+e^{-j\varphi}|$. Part 2.3 is the uncorrelated case.

### 2.1 In phase

$$p_{\rm tot}=2p\ \Rightarrow\ L_p=90+20\log_{10}2=\boxed{96.0\ \mathrm{dB}}.$$

### 2.2 120° phase lag in one channel

$$\frac{|p_{\rm tot}|}{|p|}=\left|1+e^{-j2\pi/3}\right|=\sqrt{\left(1+\cos\tfrac{2\pi}3\right)^2+\sin^2\tfrac{2\pi}3}=\sqrt{2+2\cos\tfrac{2\pi}{3}}=\sqrt{2-1}=1,$$
$$\boxed{L_p=90.0\ \mathrm{dB}}.$$
Geometrically: two unit phasors 120° apart form two sides of an equilateral triangle, so their sum has unit length too. General rule: $\Delta L=10\log_{10}(2+2\cos\varphi)$; 0° → +6, 90° → +3, 120° → 0, 180° → −∞ dB.

### 2.3 Different pure tones

Different frequencies are uncorrelated, so mean squares add:
$$L_p=10\log_{10}\left(10^{9.0}+10^{9.0}\right)=90+10\log_{10}2=\boxed{93.0\ \mathrm{dB}}.$$
**Official: 96, 90, 93 dB — agrees.** The official 2.2 expands $|1+\cos(2\pi/3)+j\sin(2\pi/3)|$ exactly as above (it writes a lag as $e^{+j\varphi}$, but the magnitude is the same for ±120°).

## Problem 3 — Rotating engine in octave bands

**Given:** period $T=1.3$ ms. Fundamental and first six overtones, each 60 dB; higher harmonics ignored.

> [!hint] Start here
> Find $f_0=1/T$. "First six overtones" means harmonics 2–7. Place each in an octave band ($f_c/\sqrt2$ to $f_c\sqrt2$) and add mean squares within each band.

$$f_0=\frac1{1.3\times10^{-3}}=769.2\ \mathrm{Hz},\qquad f_n=nf_0,\ n=1\ldots7.$$

| $n$ | Name | $f_n$ (Hz) | Octave band (limits) |
|---|---|---|---|
| 1 | fundamental | 769 | 1 kHz (707–1414) |
| 2 | 1st overtone | 1538 | 2 kHz (1414–2828) |
| 3 | 2nd overtone | 2308 | 2 kHz |
| 4 | 3rd overtone | 3077 | 4 kHz (2828–5657) |
| 5 | 4th overtone | 3846 | 4 kHz |
| 6 | 5th overtone | 4615 | 4 kHz |
| 7 | 6th overtone | 5385 | 4 kHz |

Harmonics of one engine have different frequencies, so they add as mean squares: $L=60+10\log_{10}N$ for $N$ equal components.

$$\boxed{L_{1\,\rm k}=60.0\ \mathrm{dB},\quad L_{2\,\rm k}=60+10\log2=63.0\ \mathrm{dB},\quad L_{4\,\rm k}=60+10\log4=66.0\ \mathrm{dB}}.$$
All other octave bands (31.5 … 500 Hz, 8 kHz …) are empty. Check by Parseval: total $60+10\log7=68.5$ dB, and $10\log(10^6+10^{6.3}+10^{6.6})=68.5$ dB.

**Official: 1 kHz 60 dB, 2 kHz 63 dB, 4 kHz 66 dB — agrees.** The official table uses the base-2 limits 707–1414–2828–5656 Hz. With the standardised base-10 limits (2818, 5623 Hz) every harmonic stays in the same band; the tightest margin is the 7th harmonic at 5385 Hz, still 238 Hz under 5623 Hz.

## Problem 4 — Bandwidth of a 1/12-octave filter at 1 kHz

> [!hint] Start here
> For a 1/n octave, $f_u/f_l=2^{1/n}$ and $f_c$ is the geometric mean, so $f_{l,u}=f_c\,2^{\mp1/(2n)}$.

$$f_l=1000\cdot2^{-1/24}=971.5\ \mathrm{Hz},\qquad f_u=1000\cdot2^{1/24}=1029.3\ \mathrm{Hz},$$
$$\Delta f=f_c\left(2^{1/24}-2^{-1/24}\right)=\boxed{57.8\ \mathrm{Hz}}.$$
That is 5.78 % of the centre frequency — exactly one equal-tempered semitone wide. **Official: 57.8 Hz — agrees.** (With base-10 band definitions, $10^{\pm0.3/24}$, you would get 57.6 Hz; the sheet means base 2.) The common slip is to use $2^{\pm1/12}$ for the edges, which gives the width of *two* semitones (115.6 Hz).

## Problem 5 — Machine B from the A+B measurement

**Given:** $L_A=75$ dB alone, $L_{A+B}=80$ dB together, uncorrelated.

> [!hint] Start here
> Uncorrelated → mean squares add. So subtract mean squares (this is the background-noise correction with A as "background").

$$p^2_B=p^2_{A+B}-p^2_A\ \Rightarrow\ L_B=10\log_{10}\left(10^{8.0}-10^{7.5}\right)=\boxed{78.3\ \mathrm{dB}}.$$
Correction view: $\Delta L=5$ dB → subtract $-10\log(1-10^{-0.5})=1.65$ dB from 80 dB. Sanity check: $75\oplus78.3=10\log(10^{7.5}+10^{7.83})=80.0$ dB. **Official: 78.3 dB — agrees.** Since $\Delta L=5$ dB > 3 dB, the subtraction is trustworthy (with $\Delta L<3$ dB, small measurement errors explode).

## Problem 6 — Matlab sound-level meter

The task is the separate guide (Tasks A–E); see [[Lecture 3 - Decibels Frequency Analysis and Measurements#11. Matlab sound-level-meter exercise (Problem 6)|lecture note §11]] for what each task builds and how the official solution works. The official solution was run headless in MATLAB R2026a on 20-Oct-2026 (with the three filename case fixes from the lecture note), and B1 was cross-checked in Python:

| Task | Signal | Computed | Guide |
|---|---|---|---|
| A1 | 440HzSine.wav | $p_{\rm rms}=0.1000$ Pa, **73.98 dB** | 74 dB |
| A1 | ToneComplex.wav | **76.51 dB** | 76.5 dB |
| A2 | NonStationaryNoise.wav, 3–9 s | **85.00 dB** | 85.0 dB |
| A2 | NonStationaryNoise.wav, whole | **81.99 dB** | 82 dB |
| B1 | NonStationaryNoise+background.wav, F | $L_{\rm eq}=$ **82.12 dB**, $L_{A,\rm eq}=$ **74.36 dB**; $L_F$ ≈ 66.9 dB before 3 s, ≈ 85.0 dB during | 82.1 / 74.4 dB |
| C1 | 440HzSine.wav, A-weighted | **69.89 dB(A)** | 69.9 dB |
| D3 | DeepestBlues 0–30 / 30–60 / 60–90 s | **74.43 / 82.02 / 85.79 dB** | 74.4 / 82.0 / 85.8 dB |

Reading the numbers: the 440 Hz sine is a 0.1414 Pa amplitude tone (0.1 Pa RMS = 74 dB) and A-weighting at 440 Hz is −4.1 dB → 69.9 dB(A). The 3–9 s burst at 85 dB occupies half of a 12 s file with a near-silent rest, so the whole-file $L_{\rm eq}$ is 85 − 3 = 82 dB. D3 is Parseval: summing the 31 third-octave mean squares reproduces the broadband level.

## MATLAB learning document

Open [the MATLAB script](../../../../../5.%20Semester/Acoustics%20and%20Noise%20Control/Matlab/Week3_Decibels_Levels.m) under `5. Semester/Acoustics and Noise Control/Matlab/`. Each section states the formula first, then one plain MATLAB line per formula, with the official answer in a comment beside the result. It covers Problems 1–5 plus the lecture's worked examples (slide 34 band sum, background correction, duty-cycle $L_{\rm eq}$, A-weighting from the slide formula). Run from the top once, then use **Run Section**.
