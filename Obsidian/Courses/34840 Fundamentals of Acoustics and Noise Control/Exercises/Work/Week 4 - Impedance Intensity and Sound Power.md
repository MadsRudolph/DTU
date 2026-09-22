---
course: "34840"
type: exercise
date: 2026-09-22
week: 39
lecture: 4
tags: [Acoustics, exercises, impedance, intensity, absorption]
---
# Week 4 — Impedance, Intensity and Sound Power

Source: [[34840 - Problems 4.pdf|Week 4 sheet, both pages]]. Theory: [[Lecture 4 - Impedance Intensity and Sound Power]]. [Interactive problems and benches](https://study.madsrudolph.dev/34840/#l4).

These are derived solutions checked against the answers printed on the sheet; no separate Week 4 solution file was present. Use $c=343\ \mathrm{m/s}$, $\rho=1.2\ \mathrm{kg/m^3}$ for lumped components, and the course's rounded $\rho c=413\ \mathrm{Pa\,s/m}$ for travelling-wave calculations. This small rounding difference does not affect the quoted answers. Reference pressure $p_0=20\,\mu\mathrm{Pa}$; reference power $W_0=10^{-12}\ \mathrm W$.

## Answers at a glance

| Problem | Result |
|---|---|
| 1 | $f_0=333.8\ \mathrm{Hz}\approx334\ \mathrm{Hz}$ |
| 2 | $W=1.535\ \mathrm{mW}\approx1.54\ \mathrm{mW}$ |
| 3.1 and 3.2 | $I_t/I_i=0.001116$; attenuation $29.5\ \mathrm{dB}\approx30\ \mathrm{dB}$ both ways |
| 4.1 | $\alpha=0.686\approx0.69$ |
| 4.2 | $W_{\rm abs}=0.863\ \mu\mathrm W\approx0.87\ \mu\mathrm W$, $L_W=59.36\ \mathrm{dB}$ |
| 5.1 | $Z_{a,\rm cone}=j\omega(64.0)$, $Z_{a,V}=8.824\times10^6/(j\omega)$ in N·s/m⁵; $f_0=59.1\ \mathrm{Hz}$ |
| 5.2 | Internal $L_p=140.85\ \mathrm{dB}\approx140.9\ \mathrm{dB}$ |
| A.1 | Net intensity $1.273\times10^{-4}\ \mathrm{W/m^2}$ |
| A.2 | Maximum SPL $97.0\ \mathrm{dB}$ |
| MC 1, 2, 3 | **c, c, d** |

## Problem 1 — Bottle resonance

**Given:** $V=400\ \mathrm{ml}=4.00\times10^{-4}\ \mathrm{m^3}$, neck diameter $d=20\ \mathrm{mm}=0.020\ \mathrm m$, effective neck length $l_{\rm eff}=0.021\ \mathrm m$.

> [!hint] Start here
> The neck is an acoustic mass and the enclosed air is a compliance. Find the neck area, then set their reactances equal.

$$S=\pi(d/2)^2=\pi(0.010)^2=3.1416\times10^{-4}\ \mathrm{m^2}.$$
$$M_a=\frac{\rho l_{\rm eff}}S=80.21\ \mathrm{kg/m^4},\qquad
K_a=\frac{\rho c^2}V=3.5295\times10^8\ \mathrm{N/m^5}.$$
$$f_0=\frac1{2\pi}\sqrt{\frac{K_a}{M_a}}
=\frac{343}{2\pi}\sqrt{\frac{3.1416\times10^{-4}}{(4.00\times10^{-4})(0.021)}}
=\boxed{333.8\ \mathrm{Hz}}.$$
A bigger cavity lowers the resonance; a bigger neck area raises it. The wavelength is approximately 1.03 m, much longer than the neck. The given length is already effective, so no extra end correction is needed.

## Problem 2 — Power carried by a plane wave

**Given:** $L_p=82\ \mathrm{dB}$ and perpendicular area $S=10\ \mathrm{m^2}$.

> [!hint] Start here
> Convert SPL to RMS pressure, then use the progressive-plane-wave intensity and multiply by area.

$$p_{\rm rms}=p_0\,10^{L_p/20}=20\times10^{-6}\,10^{82/20}=0.25179\ \mathrm{Pa}.$$
$$I=\frac{p_{\rm rms}^2}{\rho c}=\frac{0.25179^2}{413}=1.5350\times10^{-4}\ \mathrm{W/m^2}.$$
$$W=IS=\boxed{1.535\ \mathrm{mW}\approx1.54\ \mathrm{mW}}.$$
No extra factor $1/2$: the pressure is already RMS. The area must be normal to propagation, as stated.

## Problem 3 — Intensity transmission between water and air

**Given/recall from Week 2:** $z_a=413\ \mathrm{Pa\,s/m}$, $z_w=1000\times1480=1.48\times10^6\ \mathrm{Pa\,s/m}$. Lossless media, plane wave, normal incidence.

> [!hint] Start here
> $I=p_{\rm rms}^2/z$. The pressures on opposite sides have different pressure-to-velocity ratios, so squaring the pressure transmission coefficient is not enough.

Pressure continuity and normal-velocity continuity give
$$P_i+P_r=P_t,\qquad\frac{P_i-P_r}{z_1}=\frac{P_t}{z_2},$$
$$R=\frac{z_2-z_1}{z_2+z_1},\qquad T_p=\frac{P_t}{P_i}=\frac{2z_2}{z_1+z_2}.$$
Thus
$$\tau=\frac{I_t}{I_i}=|T_p|^2\frac{z_1}{z_2}=\frac{4z_1z_2}{(z_1+z_2)^2}.$$

### 3.1 Water to air

$$T_{p,w\to a}=\frac{826}{1480413}=0.00055795,$$
$$\tau=(0.00055795)^2\frac{1.48\times10^6}{413}=0.0011156.$$
Define positive attenuation as incident over transmitted intensity:
$$A_I=10\log_{10}\frac{I_i}{I_t}=-10\log_{10}\tau=\boxed{29.525\ \mathrm{dB}\approx30\ \mathrm{dB}}.$$
If reporting transmitted minus incident intensity level instead, the result is **−29.525 dB**.

### 3.2 Air to water

$$T_{p,a\to w}=\frac{2(1.48\times10^6)}{1480413}=1.999442,$$
$$\tau=(1.999442)^2\frac{413}{1.48\times10^6}=0.0011156,$$
$$\boxed{A_I=29.525\ \mathrm{dB}\approx30\ \mathrm{dB}}.$$
The expression is symmetric in $z_1,z_2$: intensity transmission is the same in either direction. Only **0.1116%** of the incident power crosses the interface.

**Compare Week 2:** the pressure attenuation $20\log_{10}|P_i/P_t|$ is about **65.1 dB** water-to-air but **−6.02 dB** air-to-water. The latter means transmitted pressure nearly doubles. This does not mean energy doubles: water's very large impedance makes the transmitted particle velocity tiny. The missing transmitted energy is reflected, not absorbed by this ideal interface.

## Problem 4 — Standing-wave tube

**Given:** tube length 1 m, area $S=0.01\ \mathrm{m^2}$, $f=1\ \mathrm{kHz}$, $L_{\max}=85\ \mathrm{dB}$, $L_{\min}=74\ \mathrm{dB}$. Assume a lossless plane-wave tube and an absorbing termination with no transmitted power.

> [!hint] Start here
> The difference of levels gives a pressure ratio. From the extrema recover incident and reflected pressures, then subtract their powers.

### 4.1 Absorption coefficient

$$s=10^{(85-74)/20}=3.54813,$$
$$|R|=\frac{s-1}{s+1}=0.56026,$$
$$\boxed{\alpha=1-|R|^2=0.68611\approx0.69}.$$
Using $10^{11/10}$ would give an intensity ratio where a pressure ratio is required.

### 4.2 Absorbed power and power level

$$p_{\max,\rm rms}=20\times10^{-6}10^{85/20}=0.355656\ \mathrm{Pa},$$
$$p_{\min,\rm rms}=20\times10^{-6}10^{74/20}=0.100237\ \mathrm{Pa}.$$
$$p_{i,\rm rms}=\frac{p_{\max}+p_{\min}}2=0.227947\ \mathrm{Pa},\qquad
p_{r,\rm rms}=\frac{p_{\max}-p_{\min}}2=0.127709\ \mathrm{Pa}.$$
$$W_i=\frac{S p_i^2}{413}=1.2581\ \mu\mathrm W,\qquad W_r=\frac{S p_r^2}{413}=0.39491\ \mu\mathrm W.$$
$$W_{\rm abs}=W_i-W_r=\alpha W_i=\frac{S p_{\max}p_{\min}}{413}
=\boxed{0.8632\ \mu\mathrm W}.$$
$$L_W=10\log_{10}\frac{0.8632\times10^{-6}}{10^{-12}}=\boxed{59.36\ \mathrm{dB}\approx59.4\ \mathrm{dB}}.$$
The sheet's $0.87\ \mu\mathrm W$ differs only by rounding/constants. Tube length and frequency are not needed once both extrema are known; they determine their spacing. Here $\lambda=0.343$ m, with adjacent maximum/minimum separated by $\lambda/4=0.08575$ m.

## Problem 5 — Loudspeaker cone and sealed cabinet

**Given:** cone diameter $d=0.150\ \mathrm m$, moving mass $M=0.020\ \mathrm{kg}$, cabinet volume $V=0.016\ \mathrm{m^3}$. Ignore suspension stiffness and external radiation impedance. Treat the cone as a rigid piston and the cavity as a uniform adiabatic compliance.

> [!hint] Start here
> Convert the cone's mechanical mass to the acoustic side using $S^2$. For internal pressure, cone displacement changes the volume by $Sx$.

### 5.1 Acoustic impedances and natural frequency

$$S=\pi(0.075)^2=0.0176715\ \mathrm{m^2},\qquad M_a=\frac M{S^2}=64.04499\ \mathrm{kg/m^4}.$$
$$\boxed{Z_{a,\rm cone}=j\omega\frac M{S^2}=j\omega(64.045)\ \mathrm{N\,s/m^5}}.$$
$$K_a=\frac{\rho c^2}V=\frac{1.2(343)^2}{0.016}=8.823675\times10^6\ \mathrm{N/m^5},$$
$$\boxed{Z_{a,V}=\frac{K_a}{j\omega}=\frac{8.823675\times10^6}{j\omega}\ \mathrm{N\,s/m^5}}.$$
$$f_0=\frac1{2\pi}\sqrt{\frac{K_a}{M_a}}=\boxed{59.07\ \mathrm{Hz}\approx59\ \mathrm{Hz}}.$$
Mechanical cross-check: $K_m=S^2K_a\approx2755.5\ \mathrm{N/m}$, so $f_0=\sqrt{K_m/M}/(2\pi)$ gives the same result.

### 5.2 Internal SPL at the displacement limit

The specified **4 mm peak-to-peak** means $x_{\rm pk}=2\ \mathrm{mm}=0.002\ \mathrm m$.
$$|\Delta V|_{\rm pk}=Sx_{\rm pk}=3.53429\times10^{-5}\ \mathrm{m^3}.$$
Adiabatic compression gives $p=-\rho c^2\Delta V/V$, so its amplitude is
$$p_{\rm pk}=\frac{\rho c^2Sx_{\rm pk}}V=311.85\ \mathrm{Pa},\qquad
p_{\rm rms}=\frac{311.85}{\sqrt2}=220.51\ \mathrm{Pa}.$$
$$L_p=20\log_{10}\frac{220.51}{20\times10^{-6}}=\boxed{140.85\ \mathrm{dB}\approx140.9\ \mathrm{dB}}.$$
This is the **pressure inside the cabinet**, not the free-field SPL outside. For a prescribed displacement, this ideal cavity-pressure amplitude does not depend on frequency within the lumped approximation. Using 4 mm as peak adds an erroneous 6.02 dB; forgetting peak-to-RMS adds another 3.01 dB.

## Exam Problem A — Tube with 10% absorption

**Given:** circular diameter $d=0.10$ m, absorbed power $W_{\rm abs}=1\ \mu\mathrm W$, absorption coefficient $\alpha=0.10$.

### A.1 Intensity in the tube

$$S=\pi(0.05)^2=0.00785398\ \mathrm{m^2}.$$
In a lossless tube the net intensity equals the flux into the sample:
$$\boxed{I_{\rm net}=\frac{W_{\rm abs}}S=1.27324\times10^{-4}\ \mathrm{W/m^2}}.$$
For clarity, the incident and reflected components are different:
$$W_i=W_{\rm abs}/\alpha=10\ \mu\mathrm W,\quad W_r=9\ \mu\mathrm W,$$
$$I_i=1.27324\times10^{-3}\ \mathrm{W/m^2},\quad I_r=-1.14592\times10^{-3}\ \mathrm{W/m^2}.$$
Their signed sum gives the boxed answer. The phrase “intensity in the tube” refers to this net quantity; all three are shown to remove ambiguity.

### A.2 Maximum SPL

$$|R|=\sqrt{1-\alpha}=\sqrt{0.9}=0.948683,$$
$$p_{i,\rm rms}=\sqrt{\rho c I_i}=0.725155\ \mathrm{Pa},$$
$$p_{\max,\rm rms}=p_{i,\rm rms}(1+|R|)=1.41310\ \mathrm{Pa},$$
$$\boxed{L_{p,\max}=20\log_{10}\frac{1.41310}{20\times10^{-6}}=96.98\ \mathrm{dB}\approx97.0\ \mathrm{dB}}.$$
A strong standing-wave maximum can coexist with small net intensity because most incident power returns towards the source.

## Multiple choice 1 — Group third-octaves into octaves

**Given:** only 100, 160, 250, 400, 630 and 1000 Hz third-octave bands contain energy, at 56, 58, 60, 62, 64 and 66 dB respectively. Missing bands contribute zero mean-square energy (not 0 dB).

Add the band energies using $L=10\log_{10}\sum 10^{L_i/10}$:

| Octave centre | Contributing third-octave centres | Calculation | Result |
|---|---|---|---|
| 125 Hz | 100, 160 Hz (125 Hz empty) | $10\log_{10}(10^{5.6}+10^{5.8})$ | 60.12 dB |
| 250 Hz | 250 Hz (200, 315 Hz empty) | $60$ | 60 dB |
| 500 Hz | 400, 630 Hz (500 Hz empty) | $10\log_{10}(10^{6.2}+10^{6.4})$ | 66.12 dB |
| 1000 Hz | 1000 Hz (800, 1250 Hz empty) | $66$ | 66 dB |

Rounded tuple $(60,60,66,66)$: **answer c**.

## Multiple choice 2 — Distance from free-field SPL

**Given:** $L_p(1\ \mathrm m)=64$ dB; other readings 70, 61 and 44 dB. Assume spherical spreading from the same source, with no reflections or appreciable atmospheric attenuation.
$$L_p(r)=64-20\log_{10}\frac r{1\ \mathrm m},\qquad r=(1\ \mathrm m)10^{(64-L_p)/20}.$$
The distances are $10^{-6/20}=0.501$ m, $10^{3/20}=1.413$ m and $10^{20/20}=10$ m. **Answer c: 0.5 m, 1.4 m, 10 m.**

## Multiple choice 3 — Absorption from incident/reflected levels

**Given:** incident plane-wave SPL 90 dB, reflected SPL 70 dB in the same medium.
$$\frac{I_r}{I_i}=10^{(70-90)/10}=0.01,\qquad
|R|=10^{(70-90)/20}=0.1.$$
$$\boxed{\alpha=1-|R|^2=1-0.01=0.99}.$$
**Answer d.** Subtracting the pressure ratio instead would produce the distractor 0.9.

## MATLAB learning document

Open [the MATLAB Live Script](../../../../../5.%20Semester/Acoustics%20and%20Noise%20Control/Matlab/Week4_Impedance_Intensity_Power.mlx) under `5. Semester/Acoustics and Noise Control/Matlab/`: short explanations, equations, calculations and two plots, covering every question. The `.m` is the editable text source, and the `.html` is a readable export. Run from the top once, then use **Run Section** to explore one question at a time.

## Reproduce the numbers

Run `python3 '5. Semester/Acoustics and Noise Control/Week4/check_week4.py'` from the repository root. The script checks the printed answers within their rounding precision and exports a JSON summary used to verify the interactive bench calculations.
