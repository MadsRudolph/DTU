---
course: "34840"
type: exercise
date: 2026-09-29
week: 40
lecture: 5
tags: [Acoustics, exercises, radiation, monopole, dipole, sound-power]
---
# Week 5 — Radiation: Monopoles, Dipoles and Pistons

Source: [[34840_Problems5.pdf|Week 5 sheet]] · official solutions [[34840_Solutions week 5.pdf|Solutions week 5]]. Theory: [[Lecture 5 - Radiation Monopoles Dipoles and Pistons]]. [Interactive problems and benches](https://study.madsrudolph.dev/34840/#l5).

Every answer below was checked against the official solutions; they agree to within rounding. Constants as in the official solutions: $\rho=1.2\ \mathrm{kg/m^3}$, $c=344\ \mathrm{m/s}$, so $\rho c=412.8\ \mathrm{Pa\,s/m}$. Using 343 or 413 changes nothing at the quoted precision, except MC2, which moves by 0.2 Pa. References: $p_0=20\,\mu$Pa, $I_0=10^{-12}$ W/m², $W_0=10^{-12}$ W.

## Answers at a glance

| Problem | Result | Official |
|---|---|---|
| 1 | $L_I=85.9$ dB, $W=4.85$ mW, $L_W=96.9$ dB | 85.9 dB, 96.9 dB ✔ |
| 2 | $L_p=82.6$ dB at 3 m, $72.2$ dB (72.155) at 10 m | 82.6 dB, 72.1 dB ✔ (rounding) |
| 3 | $W=37.3$ mW, $L_W=105.7$ dB | 37.3 mW, 105.7 dB ✔ |
| 4 | $W=74.7$ mW (74.67) | 74.6 mW ✔ (rounding) |
| 5 | $W\approx5.56$ mW (small-$kh$ formula); exact 5.33 mW | 5.6 mW ✔ |
| A.1 | $p_{\rm rms}=0.0843$ Pa (72.5 dB) | 0.0843 Pa ✔ |
| A.2 | $p_{\rm rms}=6.33$ Pa, amplitude $8.95$ Pa | 8.94 Pa ✔ (rounding) |
| MC 1 | **a)** 100 dB SPL | a ✔ |
| MC 2 | **c)** 62.8 Pa (62.7–62.9 depending on $c$) | c ✔ |

## Problem 1 — Intensity level and power level from one SPL reading

**Given:** omnidirectional source, $L_p=86$ dB at $r=1$ m, anechoic room (free field). No frequency given.

> [!hint] Start here
> For a monopole the near-field velocity term is 90° out of phase with pressure, so the active intensity is $p_{\rm rms}^2/\rho c$ at **any** distance. The frequency is not needed. Then spread over a sphere.

$$p_{\rm rms}=p_0\,10^{86/20}=0.3991\ \mathrm{Pa}$$
$$I_r=\frac{p_{\rm rms}^2}{\rho c}=\frac{0.3991^2}{412.8}=3.858\times10^{-4}\ \mathrm{W/m^2}$$
$$L_I=10\log_{10}\frac{3.858\times10^{-4}}{10^{-12}}=\boxed{85.86\ \mathrm{dB}\approx85.9\ \mathrm{dB}}$$
$$W=4\pi r^2 I_r=4\pi(1)^2(3.858\times10^{-4})=4.848\ \mathrm{mW}$$
$$L_W=10\log_{10}\frac{4.848\times10^{-3}}{10^{-12}}=\boxed{96.86\ \mathrm{dB}\approx96.9\ \mathrm{dB}}$$

Two shortcuts worth remembering:
- $L_I=L_p-10\log_{10}(\rho c/400)=86-0.14$ dB.
- $L_W=L_I+10\log_{10}(4\pi r^2)=L_I+11$ dB at 1 m.

**Official:** 85.9 dB, 96.9 dB, via the same route (0.4 Pa, 0.39 mW/m², 4.9 mW). ✔

## Problem 2 — SPL from a 20 mW monopole at 3 m and 10 m

**Given:** small omnidirectional source, 250 Hz, $W=20$ mW, free field.

> [!hint] Start here
> Reverse Problem 1: $W=4\pi r^2p_{\rm rms}^2/\rho c$. Solve for $p_{\rm rms}^2$; the 250 Hz is only needed later in Problems 3–5.

$$p_{\rm rms}^2=\frac{W\rho c}{4\pi r^2}$$
$$r=3\text{ m}:\quad p_{\rm rms}^2=\frac{0.02\cdot412.8}{4\pi\cdot9}=0.0730\ \mathrm{Pa^2}\ (0.270\ \mathrm{Pa}),\qquad L_p=10\log_{10}\frac{0.0730}{(20\times10^{-6})^2}=\boxed{82.6\ \mathrm{dB}}$$
$$r=10\text{ m}:\quad p_{\rm rms}^2=0.00657\ \mathrm{Pa^2}\ (0.0811\ \mathrm{Pa}),\qquad L_p=\boxed{72.15\ \mathrm{dB}}$$

Check: $20\log_{10}(10/3)=10.46$ dB, and $82.61-10.46=72.15$. ✔

**Official:** 82.6 dB and **72.1 dB**. The exact value is 72.155 dB, which rounds to 72.2. The sheet truncates; this is not a physics difference.

## Problem 3 — The same source 10 cm from a large rigid screen

**Given:** source from Problem 2 ($W_{\rm free}=20$ mW, 250 Hz), wall distance $h=0.10$ m. Assume the source keeps the same volume velocity $Q$ (a "velocity source").

> [!hint] Start here
> Replace the wall with an in-phase image source $2h$ behind it. The image's pressure works on the real source and changes its radiation load. Use the half-space power formula from slide 30.

$$k=\frac{2\pi\cdot250}{344}=4.566\ \mathrm{rad/m},\qquad kh=0.4566,\qquad 2kh=0.9133$$
$$\frac{\sin 2kh}{2kh}=\frac{0.7915}{0.9133}=0.8667$$
$$W_{\rm wall}=W_{\rm free}\left(1+\frac{\sin2kh}{2kh}\right)=20\times1.8667=\boxed{37.3\ \mathrm{mW}}$$
$$L_W=10\log_{10}\frac{0.03733}{10^{-12}}=\boxed{105.7\ \mathrm{dB}}$$

The wall is only $\lambda/14$ away ($\lambda=1.376$ m), so the power is almost doubled (the limit is ×2, +3 dB).

**Official:** 37.3 mW, 105.7 dB. ✔

## Problem 4 — Two identical sources 20 cm apart, in phase

**Given:** two Problem-2 sources, free field, separation $d=0.20$ m, same signal.

> [!hint] Start here
> This is the Problem-3 geometry ($2h=0.2$ m) with the image made real. Each source sees the same extra load as in Problem 3, and now **both** radiate.

$$W_{\rm total}=2\,W_{\rm free}\left(1+\frac{\sin kd}{kd}\right)=2\times37.33=\boxed{74.7\ \mathrm{mW}}$$
In the limit $kd\to0$ this becomes $4\times20=80$ mW: the pair is one source with $2Q$, and power $\propto|Q|^2$.

**Official:** 74.6 mW, written as $2\times37.3$. My unrounded value is 74.67 mW. Same result.

## Problem 5 — The same two sources in antiphase

**Given:** as Problem 4, driven 180° out of phase. This is a dipole with half-spacing $h=0.10$ m.

> [!hint] Start here
> The dipole power formula needs $|Q|$, so first recover $|Q|$ of one source from its 20 mW free-field power. Then use $P\approx\rho c h^2k^4|Q|^2/(6\pi)$.

$$P_{\rm mono}=\frac{\rho ck^2|Q|^2}{8\pi}\ \Rightarrow\ |Q|=\sqrt{\frac{8\pi(0.02)}{412.8\,(4.566)^2}}=7.64\times10^{-3}\ \mathrm{m^3/s}\ (\text{peak})$$
$$P_{\rm dipole}\approx\frac{\rho c\,h^2k^4|Q|^2}{6\pi}=\frac{412.8\,(0.1)^2(4.566)^4(7.64\times10^{-3})^2}{6\pi}=\boxed{5.56\ \mathrm{mW}}$$
The same thing as a ratio: $P_{\rm dipole}=\tfrac86(kh)^2P_{\rm mono}=\tfrac86(0.2085)(20)=5.56$ mW.

**Exact check** (no $\sin x\approx x$), integrating $\sin^2(kh\cos\theta)$ over the sphere:
$$P_{\rm dipole}=2P_{\rm mono}\left(1-\frac{\sin2kh}{2kh}\right)=40(1-0.8667)=5.33\ \mathrm{mW}.$$
The approximation is 4.3 % high, which matches the official remark ("about 5 %").

**Why the power drops:** at 250 Hz the sources are only 0.15 λ apart. Each source's pressure at the other is nearly equal and opposite, so the pressure on each surface is mostly out of phase with its velocity and the radiation resistance collapses. Far away, the two contributions almost cancel except for the small path difference $2h\cos\theta$. Compared with one source alone the power falls by a factor of 3.6; compared with the in-phase pair, by 13.4 (11.3 dB).

**Official:** 5.6 mW, with $|Q|=0.0076$ m³/s. ✔

## Exam Problem A — Three sirens

**Given:** three sirens of equal power at 3, 4 and 20 km, each at frequencies the others do not emit. All three together: 74.5 dB at the observation point. Free field.

> [!hint] Start here
> Different frequencies make the sources incoherent, so add **mean-square** pressures. In the far field of a monopole $p\propto1/r$, so express the 4 km and 20 km pressures in terms of the 3 km one.

### A.1 Pressure from the 3 km siren

$$p_{4\rm km}=\tfrac34p_{3\rm km},\qquad p_{20\rm km}=\tfrac{3}{20}p_{3\rm km}$$
$$p_{\rm tot}^2=p_{3\rm km}^2\left(1+\tfrac{9}{16}+\tfrac{9}{400}\right)=1.585\,p_{3\rm km}^2\ \Rightarrow\ p_{\rm tot}=1.259\,p_{3\rm km}$$
$$p_{\rm tot}=20\times10^{-6}\cdot10^{74.5/20}=0.1062\ \mathrm{Pa}$$
$$p_{3\rm km}=\frac{0.1062}{1.259}=\boxed{0.0843\ \mathrm{Pa\ rms}\ (72.5\ \mathrm{dB})}$$
The others contribute 70.0 dB (4 km) and 56.0 dB (20 km). The 20 km siren is practically irrelevant.

### A.2 Pressure 40 m from one siren

$$p_{40\rm m,rms}=p_{3\rm km}\frac{3000}{40}=75\times0.0843=6.33\ \mathrm{Pa}\ (110.0\ \mathrm{dB})$$
$$|\hat p_{40\rm m}|=\sqrt2\times6.33=\boxed{8.95\ \mathrm{Pa}}$$

**Official:** 0.0843 Pa (72.5 dB) and 8.94 Pa. ✔ The official "magnitude" is the **amplitude** (peak), $\sqrt2\times$ RMS. 8.94 against 8.95 is only rounding of the intermediate 0.0843. If a question asks for "sound pressure" with no qualifier, give both to be safe. This assumes free-field spreading to 40 m. At that distance a real siren is not yet a point source, and over 3 km air absorption is not negligible, but the problem says free field.

## Multiple choice 1 — Sources A and B in antiphase

**Given:** A gives a single 1000 Hz tone at 100 dB. B gives 1000 Hz and 1500 Hz tones of equal amplitude, 103 dB total. The microphone is equidistant from all sources. A and B are then run 180° out of phase.

> [!hint] Start here
> Split B's level into its two tones (incoherent sum). Then add coherently, tone by tone.

Two equal incoherent tones add 3 dB, so each B tone is $103-10\log_{10}2=100.0$ dB.
- 1000 Hz: A (100 dB) and B (100 dB) have equal amplitude, are in antiphase and are equidistant, so they **cancel completely**.
- 1500 Hz: only B, 100 dB.

**Answer a) 100 dB SPL.** ✔ (The distractor 107 dB would be the in-phase case, $+6$ dB at 1000 Hz on top of the 1500 Hz tone. $-\infty$ forgets the 1500 Hz tone.)

## Multiple choice 2 — Baffled loudspeaker, then a tube in front

**Given:** $a=5.9$ cm, infinite baffle, $p_{\rm rms}=0.1$ Pa at 1 m, 50 Hz. Then an infinite rigid tube of the same cross section is fitted. Find $p_{\rm rms}$ at 1 m inside the tube.

> [!hint] Start here
> $ka=0.054\ll1$, so the baffled piston is a monopole on a rigid plane: $p=\rho\omega Q/(2\pi r)$. Get $Q$ from this. In the tube the same $Q$ drives a plane wave into the impedance $\rho c/S$, and a plane wave does not decay along a lossless tube.

$$Q_{\rm rms}=\frac{2\pi r\,p_{\rm rms}}{\rho\omega}=\frac{2\pi(1)(0.1)}{1.2\cdot2\pi\cdot50}=1.667\times10^{-3}\ \mathrm{m^3/s}$$
$$p_{\rm tube}=\frac{\rho c}{\pi a^2}Q_{\rm rms}=\frac{412.8}{\pi(0.059)^2}\,1.667\times10^{-3}=\boxed{62.9\ \mathrm{Pa}}$$
In closed form, $p_{\rm tube}/p_{\rm baffle}=2r/(ka^2)=629$: a 56 dB gain. With $c=343$ the result is 62.7 Pa.

**Answer c) 62.8 Pa.** ✔ The tube helps because the radiation resistance rises from $\rho ck^2/(2\pi)$, which is tiny at $ka=0.054$, to the full $\rho c/S$: the cone now pushes against a perfectly matched resistive load. This assumes the cone's volume velocity is the same in both cases, i.e. the driver is a velocity source whose own mechanical impedance dominates the load.

> [!note] Typos in the official MC2 solution
> As printed, $p_{1\rm m,rms}=\rho\omega Q_{\rm rms}/(2\pi)$ drops the $1/r$ (harmless, since $r=1$ m), and $p_{\rm tube}=Z_aQ_{\rm rms}=\rho c/(\pi a^2)$ drops the factor $Q_{\rm rms}$ at the end. The method and the 62.8 Pa answer are correct.

## MATLAB learning document

Open [the MATLAB script](../../../../../5.%20Semester/Acoustics%20and%20Noise%20Control/Matlab/Week5_Radiation.m) under `5. Semester/Acoustics and Noise Control/Matlab/`. Each formula is written first as an equation, then calculated in one plain MATLAB line, with the official answer in a comment beside it. It covers every problem, the slide-37 source comparison and two piston extras. It was run headless in MATLAB R2026a and all printed values match this note.
