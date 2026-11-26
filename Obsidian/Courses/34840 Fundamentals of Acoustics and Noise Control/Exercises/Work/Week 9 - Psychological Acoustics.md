---
course: "34840"
type: exercise
date: 2026-11-03
week: 45
lecture: 9
tags: [Acoustics, exercises, psychoacoustics, ERB, power-spectrum-model, masking, loudness-summation, combination-tones, hearing-loss]
---
# Week 9 — Psychological Acoustics

Source: [[34840_Psychological_Acoustics_Exercise_2026.pdf|Psychological Acoustics exercise, 3 November 2026 (3 problems)]]. Official solutions: [[34840_Psychological_Acoustics_Solutions_2026.doc|Psychological Acoustics solutions (Word .doc)]]. Theory: [[Lecture 9 - Hearing - Frequency Selectivity and Masking]]. MATLAB: `5. Semester/Acoustics and Noise Control/Matlab/Week9_Psychological_Acoustics.m`. [Interactive problems and benches](https://study.madsrudolph.dev/34840/#l9).

> [!note] Checked against the official solutions
> Every number below was computed in `Week9_Psychological_Acoustics.m` (headless run, 26-Nov-2026) and agrees with the official solutions to the printed digit. One unit slip in the official text is flagged in Problem 3.3. Written after the lecture from the deck, the course text and the solutions; I did not attend the lecture.

Tools for the whole sheet:
$$\mathrm{ERB}=24.7\,(4.37F+1)\ \text{Hz}\ (F\text{ in kHz}),\qquad P_s=k\int W(f)N(f)\,df\ \xrightarrow{\text{rectangular }W}\ P_s=k\,N_0\,\Delta f_{\rm in\ filter}$$
$$L_s=N_{0,\rm dB}+10\log_{10}k+10\log_{10}\Delta f_{\rm in\ filter},\qquad P_0=10^{-12}\ \mathrm{W/m^2},\quad k=0.3\ (10\log_{10}0.3=-5.23\ \mathrm{dB})$$

## Answers at a glance

| Question | My result | Official solution |
|---|---|---|
| 1.1 | ERB = 35.5 / 132.6 / 1104.1 Hz | 35.5 / 132.6 / 1104.1 Hz ✔ |
| 1.2 | $L_s$ = 50.3 / 56.0 / 65.2 dB; easiest at 0.1 kHz | 50.3 / 56.0 / 65.2 dB, 0.1 kHz ✔ |
| 1.3 | 47.8 dB at all three frequencies | 47.8 dB, frequency independent ✔ |
| 2.1 | $f_c$ = 100 Hz: the **50 Hz** band is louder (ERB 35.5 Hz) | 50 Hz band louder ✔ |
| 2.2 | $f_c$ = 1 kHz: equally loud (ERB 132.6 Hz) | same loudness ✔ |
| 3.1 | Nonlinearity of the basilar-membrane (cochlear) response | ✔ |
| 3.2 | 900 / 800 / 700 Hz at 37.5 / 25.0 / 12.5 dB SPL | ✔ |
| 3.3 | $N_0$ = 21.9 dB/Hz = $1.54\times10^{-10}$ W/(m²·Hz); checks: 37.1 dB at 800 Hz, 36.7 dB at 700 Hz | 21.9 dB/Hz ✔, but printed as "153.9 **mW**/Hz" ✘ (should be pW); 36.7 dB at 700 Hz ✔ |
| 3.4 | Combination tones get weaker: the impaired cochlea is more linear (OHC loss, less compression) | ✔ |

> [!warning] One disagreement: the unit in 3.3
> The official solution writes the noise density as **153.9 mW/Hz**. The number is right but the prefix is not: $10^{-12}\cdot10^{2.187}=1.539\times10^{-10}$ W/(m²·Hz) = **153.9 pW/(m²·Hz)**. 153.9 mW/Hz would be 111.9 dB/Hz. The dB answer (21.9 dB/Hz) is correct.

## Problem 1 — ERB and masked thresholds

### 1.1 ERB at 0.1, 1 and 10 kHz

> [!hint] Start here
> Glasberg and Moore's formula, with **F in kHz**.

$$\mathrm{ERB}(0.1)=24.7(0.437+1)=\boxed{35.5\ \mathrm{Hz}},\quad \mathrm{ERB}(1)=24.7\cdot5.37=\boxed{132.6\ \mathrm{Hz}},\quad \mathrm{ERB}(10)=24.7\cdot44.7=\boxed{1104.1\ \mathrm{Hz}}$$

Relative to the centre frequency: 35 %, 13 %, 11 %. The filters get wider in hertz but narrower relative to $f_c$.

### 1.2 Thresholds in broadband noise, 40 dB/Hz, $k=0.3$

> [!hint] Start here
> Broadband noise fills the whole filter, so the noise power in the filter is $N_0\cdot\mathrm{ERB}$. Convert $N_0$ to linear, or work in dB throughout; both are fine since nothing gets added.

$$N_0=P_0\,10^{40/10}=10^{-8}\ \mathrm{W/(m^2\,Hz)},\qquad P_s=k\,N_0\,\mathrm{ERB},\qquad L_s=10\log_{10}\frac{P_s}{P_0}$$

| $f$ | ERB (Hz) | $10\log_{10}\mathrm{ERB}$ | $L_s=40-5.23+10\log_{10}\mathrm{ERB}$ |
|---|---|---|---|
| 0.1 kHz | 35.5 | 15.50 | **50.3 dB** |
| 1 kHz | 132.6 | 21.23 | **56.0 dB** |
| 10 kHz | 1104.1 | 30.43 | **65.2 dB** |

**Easiest to detect at 0.1 kHz:** the narrowest filter lets the least noise through, so the tone needs the least power. (This is page 30's quiz: in white noise the masked threshold rises with frequency, following $10\log_{10}\mathrm{ERB}$. The absolute threshold is far below 50 dB everywhere here, so it plays no role.)

### 1.3 Same, but the noise is only 20 Hz wide

20 Hz is narrower than the ERB at all three frequencies (35.5, 132.6, 1104 Hz), so the filter sees all 20 Hz of the noise and no more:
$$L_s=40-5.23+10\log_{10}20=\boxed{47.8\ \mathrm{dB}}\quad\text{at 0.1, 1 and 10 kHz.}$$

![[Courses/34840 Fundamentals of Acoustics and Noise Control/Images/Lecture9/band_widening.png]]
*Fletcher's band-widening experiment in the power spectrum model: below the ERB every curve is the same line (+3 dB per doubling, 47.8 dB at 20 Hz); above it the threshold stops at $N_0+10\log_{10}(k\,\mathrm{ERB})$.*

## Problem 2 — Loudness of two noise bands with the same intensity

> [!hint] Start here
> Compare each bandwidth with the ERB at $f_c$. Loudness of a fixed power **sums across filters**: power spread over several filters sounds louder than the same power inside one.

**2.1, $f_c=100$ Hz:** ERB = 35.5 Hz. The 20 Hz noise fits inside one filter. The 50 Hz noise is wider than the filter and spreads into neighbouring filters. Loudness summation across filters → **the 50 Hz noise is louder.**

**2.2, $f_c=1$ kHz:** ERB = 132.6 Hz. Both noises (20 and 50 Hz) lie inside one filter. Same power in the same filter → **equally loud.**

Why this works: the auditory system compresses within each channel (Lecture 9 §10), so loudness grows slowly with the power in one filter. Splitting the same power across two filters gives two channels, each compressed less, and their loudness adds. Inside one filter, the bandwidth is invisible: only the total power counts. This is the loudness version of Fletcher's experiment: classic loudness-vs-bandwidth curves are flat up to the critical bandwidth and rise beyond it.

## Problem 3 — Combination tones

### 3.1 What makes combination tones?

A **nonlinearity**: the compressive, active response of the **basilar membrane** (outer hair cells). A linear system cannot create frequencies that are not in its input; the nonlinear BM creates distortion products at $f_2-f_1$ and $f_1-n(f_2-f_1)$, and these are heard as extra tones (page 39's demo). They are made in the cochlea, not in the air: they appear even when the two tones come from separate loudspeakers.

### 3.2 Frequencies and levels, $f_1=1$ kHz, $f_2=1.1$ kHz, $L_1=L_2=50$ dB SPL

> [!hint] Start here
> $f_2-f_1=0.1$ kHz. The three closest of the form $f_1-n(f_2-f_1)$ are $n=1,2,3$. Then the given rule, with $f$ in kHz.

$$f_{CT}=f_1-n(f_2-f_1)=0.9,\ 0.8,\ 0.7\ \mathrm{kHz},\qquad L_{CT}=L_1+125(f_{CT}-1)$$

| $n$ | Name | $f_{CT}$ | $L_{CT}$ |
|---|---|---|---|
| 1 | $2f_1-f_2$ (cubic difference tone) | **900 Hz** | $50-12.5=$ **37.5 dB SPL** |
| 2 | $3f_1-2f_2$ | **800 Hz** | $50-25=$ **25.0 dB SPL** |
| 3 | $4f_1-3f_2$ | **700 Hz** | $50-37.5=$ **12.5 dB SPL** |

The simple difference tone $f_2-f_1=100$ Hz is far away in frequency; the question asks for the three closest to $f_1$.

### 3.3 Noise density that just masks all three

> [!hint] Start here
> Each combination tone is detected in the filter centred on it. Find the one that needs the most noise. Rectangular filters: do the neighbours share a filter?

ERB at the strongest tone: $\mathrm{ERB}(0.9)=24.7(4.37\cdot0.9+1)=121.8$ Hz, i.e. 839–961 Hz. The 800 and 700 Hz tones are outside it, so with no interaction each tone is treated alone. The 900 Hz tone is the loudest, so it sets the requirement:
$$P_s=P_0\,10^{37.5/10}=5.62\times10^{-9}\ \mathrm{W/m^2},\qquad N_0=\frac{P_s}{k\,\mathrm{ERB}}=\frac{5.62\times10^{-9}}{0.3\cdot121.8}=\boxed{1.54\times10^{-10}\ \mathrm{W/(m^2\,Hz)}}$$
$$N_{0,\rm dB}=37.5-10\log_{10}(0.3\cdot121.8)=37.5-15.63=\boxed{21.9\ \mathrm{dB/Hz}}$$

**Check the weaker tones** (the same noise in their own filters):

| Tone | ERB | Masked threshold $21.87+10\log_{10}(0.3\,\mathrm{ERB})$ | Tone level | Masked? |
|---|---|---|---|---|
| 800 Hz | 111.0 Hz | 37.1 dB | 25.0 dB | yes, by 12 dB |
| 700 Hz | 100.3 Hz | 36.7 dB | 12.5 dB | yes, by 24 dB (official: 36.7 ✔) |

The official solution only checks 700 Hz; 800 Hz is the closer call, and it passes too. The thresholds barely change (the ERB changes by 20 % over 700–900 Hz, i.e. under 1 dB), while the tones drop 12.5 dB per step, so the strongest tone always decides.

![[Courses/34840 Fundamentals of Acoustics and Noise Control/Images/Lecture9/combination_tones.png]]
*The three combination tones, their rectangular ERBs (shaded) and the masked threshold produced by 21.9 dB/Hz noise. Only the 900 Hz tone reaches the line.*

Unit note: see the warning above. The official "153.9 mW/Hz" should read **153.9 pW/(m²·Hz)**.

### 3.4 Combination tones in sensorineural hearing loss

They get **weaker** (or vanish). The combination tones come from the cochlear nonlinearity, which is the OHC active mechanism (compression near CF). Damaged OHCs → less gain, less compression → a **more linear** cochlea, and a linear system makes no distortion products. Same physics as the broader filters and the loudness recruitment in Lecture 9 §10.

## Takeaways

1. **ERB = 24.7(4.37F + 1), F in kHz**: 35.5 / 132.6 / 1104 Hz at 0.1 / 1 / 10 kHz.
2. **Power spectrum model in one line:** $L_s=N_{0,\rm dB}+10\log_{10}k+10\log_{10}\min(\Delta f_{\rm noise},{\rm ERB})$.
3. **Noise narrower than the filter:** threshold independent of frequency. Wider: only the ERB's worth counts.
4. **Loudness sums across filters**, not within one.
5. **Combination tones = cochlear nonlinearity**; hearing loss linearises the cochlea and weakens them.
