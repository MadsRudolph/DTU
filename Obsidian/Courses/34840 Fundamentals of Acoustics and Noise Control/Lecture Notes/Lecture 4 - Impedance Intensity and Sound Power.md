---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: lecture-note
date: 2026-09-22
week: 39
lecture: 4
topic: "Impedance, sound intensity and sound power"
lecturer: Finn Agerkvist
tags: [Acoustics, lecture-note, impedance, intensity, absorption]
---
# Lecture 4 — Impedance, Intensity and Sound Power

> [!abstract] The idea
> Impedance tells us how pressure drives motion. Only the part of that motion in phase with pressure transports energy on average.

**Tuesday 22 September 2026 · Finn Agerkvist.** Sources: [[34840_Lecture4_2026.pdf|Lecture 4 slides (36 pages)]] · [[34840_Lecture4_2026.pptx|PowerPoint]] · [[Fundamentals_of_acoustics_2022.pdf|course text, sections on impedance and sound energy]]. Practice: [[Week 4 - Impedance Intensity and Sound Power|fully worked Week 4 problems]]. Interactive version: [Sound Bench, Lecture 4](https://study.madsrudolph.dev/34840/#l4).

## 1. Three impedances, three different velocities

We use peak phasors and the time convention $e^{j\omega t}$. Thus differentiation becomes $j\omega$ and integration becomes $1/(j\omega)$. Physical pressure is $p(t)=\Re\{Pe^{j\omega t}\}$; for a sinusoid $p_{\rm rms}=|P|/\sqrt2$.

| Quantity | Definition | Units | What it describes |
|---|---|---|---|
| Specific/wave impedance | $z=P/U$ | Pa·s/m | Pressure versus local particle velocity |
| Mechanical impedance | $Z_m=F/v$ | N·s/m | Force versus mechanical velocity |
| Acoustic impedance | $Z_a=P_{\rm av}/Q$ | Pa·s/m³ = N·s/m⁵ | Average pressure versus volume velocity through a surface |

The characteristic impedance of air is $z_0=\rho c\approx413\ \mathrm{Pa\,s/m}$. A **single progressive plane wave**, with velocity measured along propagation, has $P/U=z_0$. A standing wave or a spherical near field generally does not.

For uniform pressure and normal velocity over area $S$,
$$Q=SU,\qquad F=PS,\qquad Z_a=\frac{z}{S}=\frac{Z_m}{S^2}.$$
The area gets squared in the mechanical-to-acoustic transformation because both force and velocity change coordinates. For a nonuniform field use $Q=\int_S\mathbf U\cdot\mathbf n\,dS$ and $P_{\rm av}=S^{-1}\int_S P\,dS$; the simple lumped power relation needs suitable uniform port variables.

## 2. Mass, spring and resonance (slides 5–6)

For mass $M$, $F=M\,dv/dt$, so $Z_{m,M}=j\omega M$. For spring stiffness $K$, $F=Kx$ and $v=j\omega x$, so $Z_{m,K}=K/(j\omega)$. If the same moving mass sees both forces,
$$Z_m=R_m+j\left(\omega M-\frac K\omega\right).$$
At $\omega_0=\sqrt{K/M}$ the reactive terms cancel. The ideal lossless impedance is zero; with damping it is $R_m$, so the velocity for a fixed applied force reaches a finite maximum. Below resonance the system is spring dominated (negative imaginary impedance); above it, mass dominated (positive imaginary impedance).

## 3. A closed tube becomes an air spring (slides 9–11)

Place the rigid termination at $x=0$, the inlet at $x=-l$, and take positive velocity towards the termination. Incident and reflected pressure phasors give
$$P=2P_i\cos(kx),\qquad Q=-j\frac{2SP_i}{\rho c}\sin(kx).$$
At the rigid end $Q=0$, hence the termination impedance is infinite. At the inlet,
$$Z_{a,\rm in}=-j\frac{\rho c}{S}\cot(kl).$$
The input impedance vanishes when $kl=(2n+1)\pi/2$, giving the closed–open tube resonances $f_n=(2n+1)c/(4l)$, $n=0,1,\ldots$. Zeros of impedance are maxima of volume-velocity response for fixed inlet pressure.

When $kl\ll1$, $\cot(kl)\approx1/(kl)$. Since $V=Sl$,
$$Z_{a,V}\approx\frac{\rho c^2}{j\omega V}=\frac{K_a}{j\omega}=\frac{1}{j\omega C_a},\qquad K_a=\frac{\rho c^2}{V},\quad C_a=\frac{V}{\rho c^2}.$$
A smaller sealed volume is a stiffer air spring. This lumped approximation needs dimensions small compared with wavelength and essentially uniform cavity pressure.

## 4. Helmholtz resonator (slides 13–16)

```mermaid
flowchart LR
    P["Driving pressure"] --> N["Neck air plug: acoustic mass ρ l_eff / S"]
    N --> V["Cavity: acoustic compliance V / ρc²"]
    V --> R["Mass and spring exchange stored energy"]
```

The neck contains mechanical air mass $\rho Sl_{\rm eff}$. Transforming through area $S$ gives
$$M_a=\frac{\rho l_{\rm eff}}S,\qquad Z_{a,\rm neck}=j\omega M_a.$$
The neck and cavity carry the same volume velocity, so their impedances add:
$$Z_a=R_a+j\omega M_a+\frac{K_a}{j\omega},\qquad
f_0=\frac{1}{2\pi}\sqrt{\frac{K_a}{M_a}}=\frac{c}{2\pi}\sqrt{\frac{S}{Vl_{\rm eff}}}.$$
Use the **effective** length supplied: it already accounts for moving air at the ends. Do not add another end correction.

**Slide 14 answer: graph C.** The impedance magnitude falls as $1/f$ below resonance, has a minimum at resonance, then rises as $f$. The peak-shaped graph B would describe an admittance-like response, not this series impedance.

> [!warning] Slide 16 has inconsistent volume data
> The heading says 300 ml, but the substitution uses 330 ml. For diameter 15 mm and effective length 40 mm, **330 ml gives 199.7 Hz**, matching the slide. **300 ml gives 209.5 Hz**. Week 4 Problem 1 is a different bottle (400 ml, 20 mm, 21 mm) and gives **333.8 Hz**.

## 5. Stored energy and transported energy (slides 17–25)

The instantaneous potential and kinetic energy densities are
$$w_p=\frac{p^2}{2\rho c^2},\qquad w_k=\frac{\rho|\mathbf u|^2}{2}.$$
For peak harmonic phasors,
$$\overline w_p=\frac{|P|^2}{4\rho c^2},\qquad
\overline w_k=\frac{\rho|\mathbf U|^2}{4}.$$
Units are J/m³. In one travelling plane wave these contributions are equal. A standing wave can store substantial energy while transporting none on average.

Instantaneous intensity is $\mathbf i(t)=p(t)\mathbf u(t)$, with units W/m². Time averaging gives
$$\boxed{\mathbf I=\frac12\Re\{P\mathbf U^*\}}.$$
For collinear scalar amplitudes separated by phase $\phi$,
$$I=\frac12|P||U|\cos\phi=p_{\rm rms}u_{\rm rms}\cos\phi.$$
Pressure and velocity in phase give maximum energy flow. A 45° phase difference gives 0.707 times that value. Quadrature gives zero average flow: energy returns each cycle. The imaginary part of $P U^*/2$ describes reactive exchange, not average transmitted power.

For a single plane wave,
$$I=\frac{|P|^2}{2\rho c}=\frac{p_{\rm rms}^2}{\rho c}.$$
For an outgoing spherical wave,
$$P=\frac{A}{r}e^{-jkr},\qquad U_r=\frac{P}{\rho c}\left(1+\frac{1}{jkr}\right),$$
$$I_r=\frac12\Re\{PU_r^*\}=\frac{|P|^2}{2\rho c}=\frac{|A|^2}{2\rho c r^2}.$$
The extra near-field velocity is in quadrature, so it does not increase active intensity. This is why $|P||U|/2$ alone overestimates the flow near the source.

## 6. Sound power and level (slides 26–31)

Integrate the outward normal component of intensity:
$$W=\int_S\mathbf I\cdot\mathbf n\,dS.$$
For a uniform plane wave crossing a perpendicular area, $W=IS$. For an omnidirectional outgoing wave in free space, $W=4\pi r^2I_r$, independent of $r$ in a lossless medium. Do not use $4\pi r^2$ for a tube or a source radiating only into a hemisphere.

At a uniform acoustic port,
$$W=\frac12\Re\{PQ^*\}=\frac12|Q|^2\Re\{Z_a\}.$$
Only resistance consumes average power; a pure mass or compliance stores and returns energy.

$$L_p=20\log_{10}\frac{p_{\rm rms}}{20\,\mu\mathrm{Pa}},\quad
L_I=10\log_{10}\frac{I}{10^{-12}\,\mathrm{W/m^2}},\quad
L_W=10\log_{10}\frac{W}{10^{-12}\,\mathrm W}.$$
In air a travelling plane wave gives $L_I\approx L_p-0.14$ dB with $\rho c=413$. The familiar equality is an approximation. Pressure level alone cannot determine net intensity in a general standing field. $L_W$ describes total emitted power, while $L_p$ depends on measurement position and environment.

## 7. Absorption from a standing wave (slides 32–34)

Let $R=P_r/P_i$. The reflected wave transports energy in the opposite direction:
$$I_{\rm net}=\frac{|P_i|^2-|P_r|^2}{2\rho c}=I_i(1-|R|^2).$$
For a terminating sample with no transmitted outgoing power, $\alpha=1-|R|^2$. If the interface transmits sound, $1-|R|^2$ includes transmission and is not all dissipated as heat.

The measured pressure extrema satisfy
$$p_{\max}=p_i+p_r,\quad p_{\min}=p_i-p_r,\quad
s=\frac{p_{\max}}{p_{\min}}=10^{(L_{\max}-L_{\min})/20},$$
$$|R|=\frac{s-1}{s+1},\qquad \boxed{\alpha=1-\left(\frac{s-1}{s+1}\right)^2=\frac{4s}{(s+1)^2}}.$$
The same equations hold using RMS amplitudes throughout. A useful shortcut for absorbed power is
$$\boxed{W_{\rm abs}=\frac{S\,p_{\max,\rm rms}p_{\min,\rm rms}}{\rho c}}.$$
Proof: $p_i=(p_{\max}+p_{\min})/2$ and $p_r=(p_{\max}-p_{\min})/2$, hence $p_i^2-p_r^2=p_{\max}p_{\min}$.

> [!warning] Slide 33 wording
> Net intensity equals the **absorbed** intensity at the termination, not the incident intensity unless $\alpha=1$. The reflected contribution must be subtracted.

## 8. Checklist before calculating

- Identify whether the velocity is $U$ (m/s), $v$ (m/s) or $Q$ (m³/s).
- Convert litres to m³, millimetres to metres, and diameter to radius before calculating area.
- A sinusoid's peak-to-peak displacement must be halved, then divided by $\sqrt2$ to obtain RMS.
- Use RMS pressure for SPL. Use the factor $1/2$ with peak phasors for intensity and power.
- At an air–water interface, include the impedance ratio when converting pressure transmission to intensity transmission.
- In a standing field, recover incident and reflected amplitudes; local $p_{\rm rms}^2/(\rho c)$ is not the net intensity.

## 9. Quick self-check

1. Why does $Z_m$ divide by $S^2$ when converted to $Z_a$?
2. Why can a loud closed-tube standing wave carry zero net power?
3. Does doubling bottle volume raise or lower $f_0$? By what factor?
4. Why can pressure double at the water surface while almost all incident energy reflects?
5. Which quantities do the extrema determine? ($|R|$, $\alpha$ and net power; reflection phase additionally needs extrema positions.)
