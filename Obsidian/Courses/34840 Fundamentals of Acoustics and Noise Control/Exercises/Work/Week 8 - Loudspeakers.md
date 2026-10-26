---
course: "34840"
type: exercise
date: 2026-10-27
week: 44
lecture: 8
tags: [Acoustics, exercises, loudspeaker, monopole, baffle, sound-power, headphones]
---
# Week 8 — Loudspeakers

Source: [[34840_Problems_8.pdf|Week 8 sheet (4 problems)]]. Official solutions: **not published yet**. Theory: [[Lecture 8 - Loudspeakers]]. MATLAB: `5. Semester/Acoustics and Noise Control/Matlab/Week8_Loudspeakers.m`. [Interactive problems and benches](https://study.madsrudolph.dev/34840/#l8).

> [!warning] Derived, not yet checked against official solutions
> Every answer below is my own derivation, checked in Python and in `Week8_Loudspeakers.m`. All of them reproduce the answers printed on the sheet. The only gap is 0.02 dB in Problem 4.

Constants: the printed answers come out with $\rho=1.2\ \mathrm{kg/m^3}$ and $c=343$ m/s, so $\rho c=411.6$ Pa·s/m. $p_{\rm ref}=20\ \mu$Pa, $I_0=W_0=10^{-12}$.

## Answers at a glance

| Question | Result | Printed on the sheet |
|---|---|---|
| 1 | $L_p=73.47$ dB, $L_I=73.34$ dB at 0.75 m; $W=1.527\times10^{-4}$ W, $L_W=81.84$ dB | 73.46 · 73.34 · 0.000153 W · 81.83 ✔ |
| 2 | 85.96 dB SPL, 85.83 dB at 1 m; $W=2.41$ mW, $L_W=93.82$ dB | 85.96 · 85.83 · 0.0024 W · 93.82 ✔ |
| 3.1 | $Q=1.344\times10^{-3}$ / $0.448\times10^{-3}$ m³/s; 81.65 dB at both | ✔ |
| 3.2 | 67.49 dB at 30 Hz, 80.96 dB at 300 Hz | ✔ |
| 4 | 8.53 dB SPL | 8.55 (0.02 dB off: the value of c) |

## Problem 1 — Small Bluetooth speaker in free space

**Given:** largest dimension < 6 cm, free space, $f<100$ Hz, sound pressure **amplitude** 0.1 Pa at 1 m. Find $L_p$ and $L_I$ at 0.75 m, the power and $L_W$.

> [!hint] Start here
> Is it a monopole? $ka$ at 100 Hz with $a=3$ cm is $0.055\ll1$, and it sits in free space, not in a baffle. So spherical spreading, $4\pi r^2$. Amplitude → rms first.

$$p_{\rm rms}(1\,\mathrm m)=\frac{0.1}{\sqrt2}=0.0707\ \mathrm{Pa},\qquad p_{\rm rms}(0.75)=\frac{0.0707}{0.75}=0.0943\ \mathrm{Pa}$$
$$L_p=20\log_{10}\frac{0.0943}{20\times10^{-6}}=\boxed{73.47\ \mathrm{dB}}$$

Far field? $kr=2\pi\cdot100\cdot0.75/343=1.4$ at 100 Hz, so not deep in the far field at the lowest frequencies. For a monopole, though, the active intensity is $p_{\rm rms}^2/\rho c$ at **any** distance (the near-field velocity is in quadrature and carries no power; [[Lecture 5 - Radiation Monopoles Dipoles and Pistons|Lecture 5]]):
$$I=\frac{p_{\rm rms}^2}{\rho c}=\frac{0.0943^2}{411.6}=2.16\times10^{-5}\ \mathrm{W/m^2},\qquad L_I=\boxed{73.34\ \mathrm{dB}}$$
$$W=4\pi r^2I=4\pi\cdot1^2\cdot\frac{0.0707^2}{411.6}=\boxed{1.527\times10^{-4}\ \mathrm W},\qquad L_W=\boxed{81.84\ \mathrm{dB}}$$

Check: at 1 m, $L_W=L_I+10\log_{10}4\pi=73.34+2.5+11.0$ ✔. The sheet's 81.83 is rounding.

## Problem 2 — Speaker in an infinite baffle

**Given:** $a=5$ cm in an infinite baffle, 50 Hz, 78 dB SPL at 2.5 m. Find $L_p$ and $L_I$ at 1 m, the power and $L_W$.

> [!hint] Start here
> $ka=0.046$: a monopole on a rigid plane. Still $1/r$, but the power goes through a **hemisphere**, $2\pi r^2$.

$$L_p(1\,\mathrm m)=78+20\log_{10}2.5=\boxed{85.96\ \mathrm{dB}}$$
$$p_{\rm rms}(1)=0.397\ \mathrm{Pa},\qquad I=\frac{0.397^2}{411.6}=3.83\times10^{-4},\qquad L_I=\boxed{85.83\ \mathrm{dB}}$$
$$W=2\pi r^2I=2\pi\cdot3.83\times10^{-4}=\boxed{2.41\times10^{-3}\ \mathrm W},\qquad L_W=\boxed{93.82\ \mathrm{dB}}$$

With $4\pi$ by mistake you would get 4.8 mW and 96.8 dB: 3 dB too much.

## Problem 3 — Loudspeaker in an infinite baffle

**Given:** $Bl=8$ Tm, $R_e=5\ \Omega$, $a=6$ cm, $M=20$ g, $e_g=2.8$ V **rms**, piston below 1 kHz, $r=2$ m.

$$S=\pi a^2=0.01131\ \mathrm{m^2},\qquad S\,Bl\,e_g=0.2533$$

> [!hint] Start here
> Chain: $i=e/R_e$ → $F=Bl\,i$ → $U=F/Z_M$ → $Q=SU$ → $p=\rho\omega Q/(2\pi r)$. In 3.1, $Z_M=j\omega M$ only.

### 3.1 Suspension ignored (mass controlled)

$$|Q|=\frac{S\,Bl\,e_g}{\omega R_eM}:\quad Q_{300}=\frac{0.2533}{1885\cdot5\cdot0.02}=\boxed{1.344\times10^{-3}\ \mathrm{m^3/s}},\qquad Q_{900}=\boxed{0.448\times10^{-3}\ \mathrm{m^3/s}}$$
$$p=\frac{\rho\omega Q}{2\pi r}=\frac{\rho\,S\,Bl\,e_g}{2\pi rR_eM}=\frac{1.2\cdot0.2533}{2\pi\cdot2\cdot5\cdot0.02}=0.2419\ \mathrm{Pa}\Rightarrow\boxed{81.65\ \mathrm{dB}}\ \text{at both}$$

The frequency drops out: a third of the volume velocity at three times the frequency. That is the flat, mass-controlled band. (Cone velocity 0.119 m/s, excursion 0.063 mm rms at 300 Hz.)

### 3.2 With $K=2000$ N/m and $R_t=18$ Ns/m

$$|Z_M|=\sqrt{R_t^2+(\omega M-K/\omega)^2},\qquad |p|=\frac{\rho\omega}{2\pi r}\,\frac{S\,Bl\,e_g}{R_e|Z_M|}$$

| | 30 Hz | 300 Hz |
|---|---|---|
| $\omega M$ | 3.77 | 37.70 |
| $K/\omega$ | 10.61 | 1.06 |
| $\omega M-K/\omega$ | −6.84 (spring wins) | +36.64 (mass wins) |
| $\lvert Z_M\rvert$ (Ns/m) | 19.26 | 40.82 |
| $\lvert Q\rvert$ (m³/s) | $2.63\times10^{-3}$ | $1.24\times10^{-3}$ |
| $p_{\rm rms}$ (Pa) | 0.0474 | 0.2234 |
| **$L_p$** | **67.49 dB** | **80.96 dB** |

Reading it:
- $f_s=\frac1{2\pi}\sqrt{K/M}=50.3$ Hz; $Q_t=\sqrt{KM}/R_t=0.35$, heavily damped. $(Bl)^2/R_e=12.8$ of the 18 Ns/m is electrical damping.
- At 300 Hz, 0.7 dB below 3.1: the 3.1 model is a good approximation at 6× $f_s$.
- At 30 Hz, 14 dB below the flat level: below resonance, falling towards 12 dB/octave. Excursion 1.23 mm rms, 20× more than at 300 Hz.

## Problem 4 — Headphone on and off the head

**Given:** 100 Hz, uniform 100 dB in 50 cm³ (cup + ear canal), perfect seal, no sound from the back of the cup, driver Ø40 mm. Find $L_p$ at 0.5 m in free space with the headphone off the head.

> [!hint] Start here
> On the head the load is a pure compliance, $p=Q/(j\omega C_A)$ with $C_A=V/\rho c^2$. That gives the driver's $Q$. Assume the driver keeps the same $Q$ off the head (volume-velocity source) and radiates it as a small monopole: $ka=0.037$.

$$C_A=\frac{V}{\rho c^2}=\frac{50\times10^{-6}}{1.2\cdot343^2}=3.54\times10^{-10}\ \mathrm{m^5/N}$$
$$p_{\rm in}=2\ \mathrm{Pa}\ (100\ \mathrm{dB}),\qquad|Q|=\omega C_A\,p_{\rm in}=628.3\cdot3.54\times10^{-10}\cdot2=4.45\times10^{-7}\ \mathrm{m^3/s}$$
$$p_{\rm free}=\frac{\rho\omega Q}{4\pi r}=\frac{1.2\cdot628.3\cdot4.45\times10^{-7}}{4\pi\cdot0.5}=5.34\times10^{-5}\ \mathrm{Pa}\Rightarrow\boxed{8.53\ \mathrm{dB\ SPL}}$$

In one line, with $\rho$ cancelling:
$$\frac{p_{\rm free}}{p_{\rm in}}=\frac{\omega^2V}{4\pi rc^2}=\frac{k^2V}{4\pi r}\ \Rightarrow\ -91.47\ \mathrm{dB}.$$

The sheet prints 8.55: that needs $c\approx342.6$ m/s, so it is rounding. With $c=344$ it is 8.48. The 40 mm diameter is only there to check that the driver is small ($ka=0.037$). Off the head, the cavity's stiffness no longer multiplies the pressure: 100 dB becomes 8.5 dB. That is why a closed headphone hardly leaks, and why the seal matters so much.

## Takeaways

1. **$4\pi$ or $2\pi$:** free space → sphere; infinite baffle → hemisphere (and $2\pi r$ in the pressure formula).
2. **Mass-controlled driver = flat response** with level $\rho S\,Bl\,e/(2\pi rR_eM)$.
3. **Add the spring and damper** and you get the 2nd-order high-pass: −14 dB at 30 Hz with $f_s=50$ Hz.
4. **A cavity turns $Q$ into pressure through its stiffness**: $p=Q/j\omega C_A$, huge compared with the free-field radiation of the same $Q$.
