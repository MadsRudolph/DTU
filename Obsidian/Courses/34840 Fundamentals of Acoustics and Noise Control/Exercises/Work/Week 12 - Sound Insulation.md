---
course: "34840"
type: exercise
date: 2026-11-24
week: 48
lecture: 12
tags: [Acoustics, exercises, sound-insulation, mass-law, critical-frequency, double-wall, multi-element, old-exams]
---
# Week 12 — Sound Insulation

Source: the official sheet is [[34840_Problems 11_2026.pdf|Problems 11 (2026), "Problems on Sound Insulation", 3 problems]] with [[34840_Solutions 11_2026.pdf|Solutions 11 (2026)]] (handwritten 31200 solution for 1–2, typed for 3). It carries the number 11 but Learn files it under module 12, and it is about this lecture. Extra practice after it: the deck's own worked examples ([[34840_sound_insulation_2026.pdf|slides]]) and every sound insulation question from the old exams ([[34840_Exam_2022_part2_MPC.pdf|2022]], [[34840_exam_2023_part2_questions_answers.pdf|2023]], [[34840_Exam_2024_part2_questions_w_answers.pdf|2024]] part 2, official solutions [[34840_Exam_2022_part2_solution.pdf|2022]], [[34840_exam_2023_part2_solution.pdf|2023]], [[34840_Exam_2024_part2_solution.pdf|2024]]), plus a few I built from the course text (marked "own"). Theory: [[Lecture 12 - Sound Insulation]]. MATLAB: `5. Semester/Acoustics and Noise Control/Matlab/Week12_Sound_Insulation.m` (runs headless, reproduces every number below).

> [!success] Checked against the official solutions (26-Nov)
> Sheet problems 1–3 agree with `34840_Solutions 11_2026.pdf`. One small difference: problem 3's answer line on the sheet prints **28.4 dB**, the typed solution computes **28.5 dB**, and the exact value is 28.54 dB, so 28.5 is right (28.4 is used in the solution's chart check only). All six old-exam questions agree with their official solutions. The deck examples are chart readings, so the exact formula lands a few tenths off (flagged in the table).

Constants: $\rho=1.2\ \mathrm{kg/m^3}$, $c=343$ m/s, $\rho c=411.6$ Pa·s/m (the 2024 solution uses these; the sheet solution uses $A=55.3V/cT$ with $c=343$ or $0.16V/T$).

## Answers at a glance

| # | Problem | My result | Official |
|---|---|---|---|
| **S1.1** | Radio next door: A-weighted level in the bedroom | **33.7 dB(A)** (bands 32.7 / 37.7 / 32.5 / 26.5 / 20.7 / 9.8 dB) | 33.7 ≈ 34 dB ✔ |
| **S2.1** | Show $L_2=L_1-R-10\log(8\pi r^2/S)$ | diffuse $P_1=p_1^2S/4\rho c$, half-space point source $Q=2$ | ✔ |
| **S2.2** | Factory windows: required $R$ | windows give 41.0 dB, background 38.7, allowed 34.2 → need 6.8 dB; ceiling gives 2.8 → **$R=21.0$ dB** | 21 dB ✔ |
| **S3** | Window in a 45 dB wall, total 40 dB | **28.5 dB** | solution 28.5 ✔, sheet prints 28.4 |
| | *Extra practice below (E = extra)* | | |
| E1 | Mass law, 55 kg/m² at 100 Hz / 1 kHz | 32.5 / 52.5 dB; constant −42.35 dB | slide 27 plot ≈ 33; slide 23 rounds to −43 |
| E2 | Random and field incidence, $R_0=52.5$ | 41.6 / 47.5 dB | 2023 Q10: field = 5 dB lower ✔ |
| E3 | 2023 Q8: $L_2$ in the receiver room | **37.9 dB** | 37.9 dB ✔ |
| E4 | Slide 18: wall with a door | **35.4 dB** | 35 dB (chart) ✔ |
| E5 | Slide 19: crack in a wall | **39.6 dB** | 40 dB (chart) ✔ |
| E6 | 2022 Q8: minimum $R$ of the window | **40.5 dB** | 40.5 dB (D) ✔ |
| E7 | 2024 Q8: $f_c$ change, concrete 10 → 15 cm | 189.0 → 126.0 Hz, **−63.0 Hz** | −63 Hz ✔ |
| E8 | 2022 Q9: stacking two plates, $f_c=3000$ Hz | **3000 Hz** | 3000 Hz (C) ✔ |
| E9 | 10 cm concrete wall at 500 Hz, all models | $R_0$ 58.9, resonant 44.1, upper limit 74.5 dB | (own) |
| E10 | Slide 26: thick-wall upper limits | 67.7 / 79.8 / 93.7 dB | 68 / 80 / 94 dB ✔ (my $\rho_M$, $c_L$) |
| E11 | 2024 Q11: double gypsum wall at 600 Hz | $f_d$ 546 Hz, $R_1$ 32.08 dB, **+32.1 dB** | 32.1 dB ✔ |
| E12 | $R_w$ of the 10 cm concrete model | **48 dB** (deviations 31.0 dB) | (own) |
| E13 | Impact $L_n$ and flanking $R'$ | 67.1 dB; 52.5 dB | (own) |

**Disagreements:** sheet problem 3: the sheet prints 28.4 dB, the solution and the exact value give 28.5 dB. None with the official exam answers. Small ones with the deck: slides 18 and 19 read a chart (35 and 40 dB; exact 35.4 and 39.6). Slide 23's "−43" is −42.35 exactly. The 2024 solution writes the surface mass as "15.6 kg/m³" (should be kg/m²) and cites "slide 55" of an older deck; in the 2026 deck that is slide 57. The 2022 solution cites "slides 46–47"; in 2026 it is slides 50–51.

---

## Sheet problem 1 — Radio music through a party wall

**Given:** partition wall 15 m², bedroom 50 m³. Octave bands:

| f (Hz) | 125 | 250 | 500 | 1000 | 2000 | 4000 |
|---|---|---|---|---|---|---|
| $R'$ (dB) | 40 | 42 | 49 | 55 | 61 | 67 |
| $L_1$ (dB) | 70 | 77 | 78 | 78 | 79 | 75 |
| $T_2$ (s) | 1.0 | 1.0 | 1.2 | 1.2 | 1.0 | 0.8 |

**1.1** Average A-weighted level in the neighbour's bedroom.

> [!hint] Start here
> Two-room formula per band, solved for $L_2$, with $A_2=0.16V/T_2$. Then A-weight each band and add on an energy basis.

$$L_2=L_1-R'+10\log_{10}\frac{S\,T_2}{0.16\,V}$$

| f (Hz) | 125 | 250 | 500 | 1000 | 2000 | 4000 |
|---|---|---|---|---|---|---|
| $10\log(ST_2/0.16V)$ | 2.7 | 2.7 | 3.5 | 3.5 | 2.7 | 1.8 |
| $L_2$ (dB) | 32.7 | 37.7 | 32.5 | 26.5 | 20.7 | 9.8 |
| $K_A$ (dB) | −16.1 | −8.6 | −3.2 | 0 | +1.2 | +1.0 |
| $L_2+K_A$ | 16.6 | 29.1 | 29.3 | 26.5 | 21.9 | 10.8 |

$$L_A=10\log_{10}\sum_i10^{0.1(L_{2,i}+K_i)}=\boxed{33.7\ \mathrm{dB(A)}}\approx34\ \mathrm{dB}$$

Official: 33.7 ≈ **34 dB** ✔. The 250 and 500 Hz bands dominate: the wall is weakest relative to the music there, and the A-weighting has already cut the 125 Hz band. Here $10\log(S/A_2)$ is **positive** (the bedroom has only 6.7–10 m² of absorption, less than the 15 m² wall), so the bedroom is louder than $L_1-R'$. $R'$ has a prime: measured in the building, flanking included.

## Sheet problem 2 — Noise from factory windows

### 2.1 Show the guideline formula $L_2=L_1-R-10\log(8\pi r^2/S)$

Inside, a diffuse field with pressure $p_1$ puts this power onto the windows ([[Lecture 12 - Sound Insulation|Lecture 12 §3]]):
$$P_1=\frac{p_1^2S}{4\rho c}.$$
The windows pass $P_2=P_1/10^{R/10}$. Outside, treat them as a point source on a large rigid surface (the façade), radiating into a half-space, directivity factor $Q=2$:
$$p_2^2=\frac{Q\,P_2\,\rho c}{4\pi r^2}=\frac{P_2\,\rho c}{2\pi r^2}.$$
So
$$R=10\log\frac{P_1}{P_2}=10\log\Big(\frac{p_1^2}{p_2^2}\cdot\frac{Q\,S}{16\pi r^2}\Big)=L_1-L_2+10\log\frac{S}{8\pi r^2}\ \Rightarrow\ L_2=L_1-R-10\log\frac{8\pi r^2}{S}\ \checkmark$$
($Q$ here is the directivity factor, not a volume velocity.)

### 2.2 Which $R$ do the new windows need?

**Given:** hall 16 × 16 × 14 m, $T=2.5$ s, $L_1=89$ dB(A); windows 32 m², $R=17$ dB; observation point at 40 m measures 43 dB(A), limit 40 dB(A). Window and other paths are uncorrelated. Proposed: ceiling absorption from $\alpha=0.05$ to 0.85, plus better windows.

> [!hint] Start here
> Four steps: (1) how much comes from the windows now; (2) subtract it from 43 dB to find the background; (3) how much may the windows give so the sum is 40 dB; (4) the ceiling gives part of the reduction, the windows the rest.

1. Windows now: $L_2=89-17-10\log\frac{8\pi\cdot40^2}{32}=72-31.0=41.0$ dB.
2. Background: $L_b=10\log(10^{4.3}-10^{4.10})=38.7$ dB.
3. Allowed from the windows: $L_{2,\rm new}=10\log(10^{4.0}-10^{3.87})=34.2$ dB, so the window path must drop by $\Delta L=41.0-34.2=6.8$ dB.
4. Ceiling: $A_1=\frac{55.3\cdot3584}{343\cdot2.5}=231$ m². The new ceiling **replaces** α = 0.05 by 0.85 on 256 m²: $A_2=231+256\,(0.85-0.05)=436$ m². Lower reverberant level inside: $10\log(436/231)=2.8$ dB.

$$R_{\rm new}=17+(6.8-2.8)=\boxed{21\ \mathrm{dB}}$$

Official: **21 dB** ✔. Two traps: adding $256\cdot0.85$ instead of the **change** in absorption, and forgetting that the 38.7 dB background stays: without it you would think 41 → 40 dB needs only 1 dB.

## Sheet problem 3 — A window cut into a wall

**Given:** wall 20 m² with $R=45$ dB. A 1 m² window is made in it, and the total measures 40 dB. Find the window's $R$.

> [!hint] Start here
> The wall part is now 19 m². $S\tau_{\rm res}=S_1\tau_1+S_2\tau_2$, solve for $\tau_2$.

$$\tau_2=\frac{20\cdot10^{-4}-19\cdot10^{-4.5}}{1}=2.00\times10^{-3}-0.60\times10^{-3}=1.40\times10^{-3}$$
$$R_2=-10\log_{10}(1.40\times10^{-3})=\boxed{28.5\ \mathrm{dB}}$$

Typed solution: **28.5 dB** ✔; the sheet's answer line says 28.4 (a rounding difference). Check with the chart (course text Fig. 5.1.2): $R_1-R_2=16.6$ dB and 5 % area give $R_{\rm res}\approx R_2+12=40.4$ dB. Same pattern as extra 6 below (2022 Q8), from the other direction.

---

## Extra practice: deck examples and old exam questions

## Extra 1 — The mass law and its shortcut (slides 23, 27)

**Given:** a limp wall of 55 kg/m² (slide 27's example). Find $R_0$ at 100 Hz and 1 kHz, and check the "−43 dB" shortcut.

> [!hint] Start here
> Normal incidence, mass only: $R_0=20\log(\omega m/2\rho c)$. The 1 is negligible once $\omega m\gg2\rho c$.

$$R_0(100)=20\log_{10}\frac{2\pi\cdot100\cdot55}{2\cdot411.6}=\boxed{32.5\ \mathrm{dB}},\qquad R_0(1000)=\boxed{52.5\ \mathrm{dB}}$$

Ten times the frequency, +20 dB: 6 dB per octave. The slide 27 plot starts its mass-law line at about 33 dB at 100 Hz ✔.

Shortcut: $20\log\frac{2\pi fm}{2\rho c}=20\log(fm)+20\log\frac{\pi}{\rho c}=20\log(fm)-42.35$. The slide's −43 is a rounded, slightly conservative version.

## Extra 2 — Random and field incidence (slides 40–41), 2023 exam Q10

**Given:** $R_0=52.5$ dB from extra 1. Find the random- and field-incidence values. And 2023 Q10: *"In a diffuse sound field the sound transmission loss is approximately … than that of normal incidence."*

$$R_{\rm random}=R_0-10\log(0.23R_0)=52.5-10.8=\boxed{41.6\ \mathrm{dB}},\qquad R_{\rm field}=R_0-5=\boxed{47.5\ \mathrm{dB}}$$

2023 Q10: **5 dB lower** (field incidence, eq. 5.2.18). The "15 dB lower" option is a distractor; the theoretical random-incidence value is about 10 dB lower, but finite walls measure close to −5.

## Extra 3 — Level in the receiver room, 2023 exam part 2 Q8

**Given:** 80 dB in the source room (1 kHz third-octave), wall 4 m × 3 m with $R=40$ dB, receiver room 60 m³ with $T=0.5$ s. Find $L_2$.

> [!hint] Start here
> Rearrange $R=L_1-L_2+10\log(S/A_2)$. $S$ is the **wall**, 12 m². $A_2$ from Sabine.

$$A_2=\frac{55.3V}{cT}=\frac{55.3\cdot60}{343\cdot0.5}=19.35\ \mathrm{m^2}\quad(0.161V/T\text{ gives }19.32)$$
$$L_2=L_1-R+10\log_{10}\frac{S}{A_2}=80-40+10\log_{10}\frac{12}{19.35}=80-40-2.07=\boxed{37.9\ \mathrm{dB}}$$

Official: **37.9 dB** ✔. Sign check: the receiver room has more absorption (19 m²) than the wall has area (12 m²), so it ends up a little quieter than $L_1-R$.

## Extra 4 — Wall with a door (slide 18)

**Given:** wall $S_1=18$ m², $R_1=44$ dB; door $S_2=2$ m², $R_2=26$ dB. Find $R_{\rm res}$.

> [!hint] Start here
> Power adds, so area-weight the $\tau$'s, not the dB.

$$\tau_1=10^{-4.4}=3.98\times10^{-5},\qquad\tau_2=10^{-2.6}=2.51\times10^{-3}$$
$$\tau_{\rm res}=\frac{18\cdot3.98\times10^{-5}+2\cdot2.51\times10^{-3}}{20}=\frac{0.72\times10^{-3}+5.02\times10^{-3}}{20}=2.87\times10^{-4}$$
$$R_{\rm res}=-10\log_{10}\tau_{\rm res}=\boxed{35.4\ \mathrm{dB}}$$

The slide reads the chart ($R_1-R_2=18$ dB, $S_2/S=10$ %) as $R_2+9=35$ dB ✔. The door, 10 % of the area, lets through 87 % of the power. Area-averaging the dB (wrong) would give 42.2 dB.

## Extra 5 — A crack in the wall (slide 19)

**Given:** wall 10 m², 50 dB; a crack 3 m × 1/3 mm, assume $\tau=1$ in the crack. Find $R_{\rm res}$.

$$S_{\rm ap}=3\cdot\tfrac13\times10^{-3}=10^{-3}\ \mathrm{m^2},\qquad\frac{S_{\rm ap}}S=10^{-4}$$
$$R_{\rm res}=-10\log_{10}\Big(\frac{(10-0.001)\cdot10^{-5}+0.001\cdot1}{10}\Big)=-10\log_{10}(1.1\times10^{-4})=\boxed{39.6\ \mathrm{dB}}$$

Slide: **40 dB** ✔. The crack alone caps the wall at $-10\log(10^{-4})=40$ dB; even an infinitely good wall cannot beat it. That is why door seals matter more than door mass.

## Extra 6 — Minimum $R$ of a window, 2022 exam part 2 Q8

**Given:** total wall 25 m² must reach $R=50$ dB in one band. The wall construction alone is 55 dB. A 2 m² window goes in. Minimum $R$ of the window?

> [!hint] Start here
> Same formula as extra 4, solved for the unknown element. The wall part is now 25 − 2 = 23 m².

$$S\,10^{-0.1R_{\rm res}}=S_{\rm wall}10^{-0.1R_{\rm wall}}+S_{\rm win}10^{-0.1R_{\rm win}}$$
$$R_{\rm win}=-10\log_{10}\Big(\frac{25\cdot10^{-5}-23\cdot10^{-5.5}}{2}\Big)=-10\log_{10}\Big(\frac{2.5\times10^{-4}-0.73\times10^{-4}}{2}\Big)=\boxed{40.5\ \mathrm{dB}}$$

Official: **D) 40.5 dB** ✔. Note it is **not** "50 dB" (option B): the window may be 10 dB worse than the target because it is small, but the wall already eats 29 % of the allowed $\tau$.

## Extra 7 — Critical frequency of a thicker concrete wall, 2024 exam part 2 Q8

**Given:** concrete, $E=2.6\times10^{10}$ Pa, $\rho_M=2.3\times10^3$ kg/m³, $\nu=0.2$, $\eta=0.02$. Thickness 10 → 15 cm. Change in $f_c$?

> [!hint] Start here
> $f_c=\frac{c^2}{2\pi}\sqrt{m/B}$ with $m=\rho_Mh$ and $B=Eh^3/12(1-\nu^2)$. One $h$ is left: $f_c\propto1/h$. The loss factor is a distractor.

$$f_c=\frac{c^2}{2\pi h}\sqrt{\frac{12\rho_M(1-\nu^2)}{E}}=\frac{343^2}{2\pi h}\sqrt{\frac{12\cdot2300\cdot0.96}{2.6\times10^{10}}}=\frac{18.90}{h}\ \mathrm{Hz\,m}$$
$$f_c(0.10)=189.0\ \mathrm{Hz},\qquad f_c(0.15)=126.0\ \mathrm{Hz},\qquad\Delta f_c=\boxed{-63.0\ \mathrm{Hz}}$$

Official: **−63 Hz** ✔. Direction check: thicker → stiffer grows as $h^3$, mass only as $h$ → bending waves faster → they match air at a lower frequency.

## Extra 8 — Stacking plates, 2022 exam part 2 Q9

**Given:** a thin plate with $f_c=3000$ Hz. Two such plates are stacked on top of each other. New $f_c$?

> [!hint] Start here
> Loose layers bend independently: their stiffnesses add, $B\to2B$. Masses add, $m\to2m$.

$$f_c'=\frac{c^2}{2\pi}\sqrt{\frac{2m}{2B}}=f_c=\boxed{3000\ \mathrm{Hz}}$$

Official: **C) 3000 Hz** ✔ (slides 50–51 in the 2026 deck). The trap is **B) 1500 Hz**: that is one plate of **double thickness**, bonded through, where $B\to8B$ and $m\to2m$, so $f_c$ halves. Slide 51 shows both: four stacked 12.5 mm boards keep the dip at about 2.5 kHz ($R_w$ 39 dB); one 50 mm board moves it to about 600 Hz ($R_w$ 32 dB).

## Extra 9 — The 10 cm concrete wall at 500 Hz, four models (own, slide 46)

**Given:** the wall from extra 7, $h=10$ cm: $m=230$ kg/m², $f_c=189$ Hz, $\eta=0.02$. Find $R$ at 500 Hz by the mass law, the general model and the upper limit.

$$R_0(500)=20\log\frac{2\pi\cdot500\cdot230}{823.2}=58.9\ \mathrm{dB}$$
500 Hz is **above** $f_c$, so the resonant formula applies:
$$R=R_0+10\log_{10}\frac{2\eta f}{\pi f_c}=58.9+10\log_{10}\frac{2\cdot0.02\cdot500}{\pi\cdot189}=58.9-14.7=\boxed{44.1\ \mathrm{dB}}$$
Upper limit with $c_L=\sqrt{E/\rho_M}=3362$ m/s:
$$R_{\max}=20\log\frac{2300\cdot3362}{823.2}-5=\boxed{74.5\ \mathrm{dB}}$$

At $f_c$ itself the resonant model sits $10\log(2\eta/\pi)=-19.0$ dB under $R_0$. Field mass law at 500 Hz would say 53.9 dB, so ignoring coincidence overestimates this wall by 10 dB. Plot: [[Lecture 12 - Sound Insulation|Lecture 12 §10]].

## Extra 10 — Upper limits of thick walls (slide 26)

$$R_{N,\max}=20\log_{10}\frac{\rho_Mc_L}{2\rho c}$$

The slide gives only the results. With typical values (my choice):

| Material | $\rho_M$ (kg/m³) | $c_L$ (m/s) | $R_{N,\max}$ | Slide |
|---|---|---|---|---|
| Wood | 500 | 4000 | 67.7 dB | 68 |
| Concrete | 2300 | 3500 | 79.8 dB | 80 |
| Steel | 7800 | 5100 | 93.7 dB | 94 |

The upper limit is the wall's own characteristic impedance against the air's. No single homogeneous wall gets past it, whatever its thickness.

## Extra 11 — Double gypsum wall, 2024 exam part 2 Q11

**Given:** two gypsum boards, 13 mm, 1200 kg/m³. Field mass law for each board. Above $f_d=c/2\pi d$ with $d=10$ cm. At 600 Hz, how much better is the insulation with the boards 10 cm apart than mounted close together?

> [!hint] Start here
> Check $f>f_d$ first. Apart: $R=R_1+R_2+6$. Together: one leaf of the total mass.

$$m=1200\cdot0.013=15.6\ \mathrm{kg/m^2},\qquad f_d=\frac{343}{2\pi\cdot0.1}=546\ \mathrm{Hz}<600\ \text{✔}$$
$$R_1=R_2=20\log_{10}\frac{2\pi\cdot600\cdot15.6}{2\cdot411.6}-5=37.08-5=32.08\ \mathrm{dB}$$
$$R_{\rm apart}=R_1+R_2+6=70.16\ \mathrm{dB},\qquad R_{\rm together}=20\log_{10}\frac{2\pi\cdot600\cdot31.2}{823.2}-5=38.10\ \mathrm{dB}$$
$$\Delta R=70.16-38.10=\boxed{32.1\ \mathrm{dB}}$$

Official: **32.1 dB** ✔. Option **38.1 dB** is the trap: that is $R_{\rm together}$ itself. Mass–air–mass resonance for interest: $f_0=\frac{343}{2\pi}\sqrt{\frac{1.2}{0.1}\cdot\frac{2}{15.6}}=67.7$ Hz, well below 600 Hz.

One subtlety: the official route applies the −5 dB field correction to each board (so −10 in total for the double wall) but only once to the single leaf. If you use normal incidence everywhere you get 37.1 dB, which is not an option. Follow the question: "field mass law for each individual board".

## Extra 12 — Single-number rating $R_w$ of the concrete wall (own, slide 13)

**Given:** the model from extra 9 in the 16 third-octave bands, 100–3150 Hz:

| f (Hz) | 100 | 125 | 160 | 200 | 250 | 315 | 400 | 500 | 630 | 800 | 1k | 1.25k | 1.6k | 2k | 2.5k | 3.15k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $R$ (dB) | 37.0 | 36.8 | 33.0 | 32.2 | 35.1 | 38.1 | 41.2 | 44.1 | 47.2 | 50.3 | 53.2 | 56.1 | 59.3 | 62.2 | 65.1 | 68.1 |
| Ref. at 48 | 29 | 32 | 35 | 38 | 41 | 44 | 47 | 48 | 49 | 50 | 51 | 52 | 52 | 52 | 52 | 52 |

> [!hint] Start here
> Reference curve in its 52 position: 33 36 39 42 45 48 51 **52** 53 54 55 56 56 56 56 56. Shift it, add up the shortfalls where $R$ is below it, stop at the highest position with a sum ≤ 32 dB.

At position 48 the unfavourable deviations are 160 Hz: 2.0, 200: 5.8, 250: 5.9, 315: 5.9, 400: 5.8, 500: 3.9, 630: 1.8 → **31.0 dB** ≤ 32. At 49 every one of those grows by 1 and the 800 Hz band joins: 38.8 dB > 32. So
$$R_w=\boxed{48\ \mathrm{dB}}$$
(the reference value at 500 Hz). The wall's coincidence region around 200–400 Hz is what limits it; its high frequencies are far above the curve and earn nothing.

## Extra 13 — Impact sound and flanking (own, course text §5.4 and §5.6)

**13a.** A tapping machine upstairs gives $L_2=65$ dB in a 50 m³ room with $T=0.5$ s. Find $L_n$.
$$A_2=\frac{0.161\cdot50}{0.5}=16.1\ \mathrm{m^2},\qquad L_n=L_2+10\log\frac{A_2}{10}=65+2.07=\boxed{67.1\ \mathrm{dB}}$$
The room has more than 10 m² absorption, so the normalised level is higher than measured.

**13b.** A partition with $R=55$ dB, plus four flanking paths at $R_F=62$ dB each. Find $R'$.
$$R'=-10\log\big(10^{-5.5}+4\cdot10^{-6.2}\big)=-10\log(3.16\times10^{-6}+2.52\times10^{-6})=\boxed{52.5\ \mathrm{dB}}$$
Four paths that are each 7 dB better than the wall still cost 2.5 dB. Building requirements are on $R'_w$, with flanking.

## Takeaways

1. **Everything combines through $\tau$**: doors, windows, cracks, flanking. The weakest element wins.
2. **Mass law**: $R_0=20\log(\omega m/2\rho c)$, +6 dB per doubling of $f$ or $m$; between rooms subtract 5 dB.
3. **$f_c=\frac{c^2}{2\pi}\sqrt{m/B}\propto1/h$**: thicker plates have lower $f_c$; stacked loose layers keep it.
4. **Double wall**: $f_0$ (mass–air–mass) and $f_d=c/2\pi d$; above $f_d$, $R=R_1+R_2+6$ dB, far more than one leaf of the same mass.
5. **Two-room formula**: $L_2=L_1-R+10\log(S/A_2)$, with $S$ the wall and $A_2$ the receiving room.
