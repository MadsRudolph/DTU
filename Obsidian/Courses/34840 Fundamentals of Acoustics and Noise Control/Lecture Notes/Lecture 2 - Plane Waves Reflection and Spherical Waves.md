---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: lecture-note
date: 2026-09-08
week: 37
lecture: 2
topic: "Plane waves, reflection and spherical waves"
lecturer: FA
tags: [Acoustics, lecture-note, standing-waves, reflection, spherical-waves]
---
# Lecture 2 — Plane Waves, Reflection and Spherical Waves

> [!info] Lecture Info
> **Date:** Tuesday 8 September 2026, 08:00–12:00 · building 358, room 063 · **Finn Agerkvist**
> **Slides:** [[34840_Lecture2_2026.pdf|PDF slides]] · [[34840_Lecture2_2026.pptx|Open original PowerPoint]]
> **Reading:** [[Fundamentals_of_acoustics_2022.pdf|Course text]], printed pp. 8–15 (§1.2; plane-wave recap pp. 6–7).
> **Problems:** [[Week 2 - Reflection and Spherical Waves|Week 2 preparation]] · [[34840_Problems2.pdf|Original problem sheet]]
> **Previous:** [[Lecture 1 - Introduction and Plane Waves|Lecture 1]] · **Course:** [[34840 Fundamentals of Acoustics and Noise Control]]

> [!abstract] Where this lecture sits
> Lecture 1 introduced sound pressure, particle velocity and the wave equation. Here we combine travelling waves to explain reflection, standing waves and tube resonances, then move from plane waves to an outgoing spherical wave. The important change is that **pressure divided by particle velocity depends on the sound field**, even in the same medium.
> Prepared from the lecture slides and course text; the working spaces are for additions during class.

---

## 1. Recap — plane waves and notation (slides 3–5)

> [!note] Convention and units
> Use $p(x,t)=\Re\{P(x)e^{j\omega t}\}$ and $u_x(x,t)=\Re\{U_x(x)e^{j\omega t}\}$. Capital letters here are **complex peak phasors**, not RMS values; $U_x$ denotes particle velocity, not volume velocity.
>
> | Quantity | Symbol / relation | Unit |
> |---|---|---|
> | Acoustic pressure | $P$ | Pa |
> | Particle velocity | $U_x$ or $U_r$ | m/s |
> | Angular frequency | $\omega=2\pi f$ | rad/s |
> | Wavenumber | $k=\omega/c=2\pi/\lambda$ | rad/m |
> | Wavelength | $\lambda=c/f$ | m |
> | Characteristic impedance | $Z_0=\rho c\approx413$ in air | Pa·s/m |

The lossless linear wave equation and its single-frequency form are
$$\frac{\partial^2p}{\partial x^2}=\frac{1}{c^2}\frac{\partial^2p}{\partial t^2},\qquad \frac{d^2P}{dx^2}+k^2P=0.$$
Euler's equation gives
$$j\omega\rho U_x=-\frac{dP}{dx}.$$

> [!success] Travelling-wave pair
> $$P=P_i e^{-jkx}+P_r e^{jkx},\qquad U_x=\frac{P_i e^{-jkx}-P_r e^{jkx}}{\rho c}.$$
> The reflected wave has a **minus sign in velocity** because velocity has a direction. For a single wave travelling along $+x$, $P/U_x=\rho c$; for a single wave along $-x$, $P/U_x=-\rho c$.

## 2. Rigid and pressure-release reflection (slides 6–9)

Take the boundary at $x=0$, with the incident wave travelling towards $+x$ in the region $x\le0$. Define the pressure reflection coefficient at the boundary as $R=P_r/P_i$.

> [!example] Rigid termination: $U_x(0)=0$
> The boundary requires $P_i=P_r$, hence $R=+1$:
> $$P(x)=2P_i\cos(kx),\qquad U_x(x)=-j\frac{2P_i}{\rho c}\sin(kx).$$
> The wall is a **pressure antinode** and a **velocity node**. Pressure nodes lie at distances
> $$d_n=\frac{(2n+1)\lambda}{4},\quad n=0,1,2,\ldots$$
> from the wall. Adjacent pressure nodes are separated by $\lambda/2$.

> [!example] Pressure-release termination: $P(0)=0$
> $P_r=-P_i$, hence $R=-1$:
> $$P(x)=-2jP_i\sin(kx),\qquad U_x(x)=\frac{2P_i}{\rho c}\cos(kx).$$
> Pressure has a node at the end, and velocity an antinode. An ideal open tube end is approximated this way.

> [!important] Two different phase relationships
> In a perfect standing wave, pressure and velocity are in temporal quadrature wherever both are nonzero. Their spatial node patterns are displaced by $\lambda/4$. At a node, the zero-amplitude quantity has no defined phase.

## 3. Tube resonances and instruments (slides 10–19)

Resonance requires a round trip with a phase that reinforces the existing field. The two end conditions determine the allowed wavelengths.

> [!abstract] Ideal uniform tubes of length $L$
> | Ends | Boundary conditions | Resonance frequencies |
> |---|---|---|
> | Open–open | pressure nodes at both ends | $f_n=nc/(2L)$, $n=1,2,\ldots$ |
> | Closed–closed | velocity nodes at both ends | $f_n=nc/(2L)$, $n=1,2,\ldots$ |
> | Closed–open | velocity node / pressure node | $f_n=(2n-1)c/(4L)$, $n=1,2,\ldots$ |
>
> At fixed geometry, each resonance frequency scales with $c$. These are ideal tube models; actual instrument geometry and end corrections affect the spectrum.

> [!note] Build-up at resonance
> Slides 16–17 compare repeated reflections at $f_0$ and $1.1f_0$. In-phase arrivals reinforce; detuned arrivals rotate in phase and partly cancel. Losses limit the build-up. Keep the PowerPoint available for the dynamic illustrations, which a static PDF cannot reproduce.

> [!todo] During class
> - Sketch the first two pressure modes for open–open and closed–open tubes.
> - Explain the odd-harmonic sequence for the ideal closed–open tube: ⬜
> - What changes when the speed of sound changes but the tube length stays fixed? ⬜

## 4. Partial reflection and standing wave ratio (slides 20–24)

For a passive termination in the incident lossless medium, $R$ can be complex, with $|R|\le1$:
$$P(x)=P_i\left(e^{-jkx}+R e^{jkx}\right).$$

> [!success] Envelope and standing wave ratio
> $$|P|_{\max}=|P_i|(1+|R|),\qquad |P|_{\min}=|P_i|(1-|R|),$$
> $$s=\frac{|P|_{\max}}{|P|_{\min}}=\frac{1+|R|}{1-|R|},\qquad |R|=\frac{s-1}{s+1}.$$
> $R=0$: no standing-wave modulation. $|R|=1$: perfect nodes and $s\to\infty$. The phase of $R$ shifts the pattern; the standing wave ratio alone does not recover that phase.

### Transmission between two fluids at normal incidence

Let $Z_1=\rho_1c_1$ and $Z_2=\rho_2c_2$, with incidence from medium 1. Pressure and normal velocity are continuous:
$$P_i+P_r=P_t,\qquad \frac{P_i-P_r}{Z_1}=\frac{P_t}{Z_2}.$$

> [!success] Reflection and transmission
> $$R_{12}=\frac{Z_2-Z_1}{Z_2+Z_1},\qquad T_{p,12}=\frac{P_t}{P_i}=1+R_{12}=\frac{2Z_2}{Z_1+Z_2}.$$
> The problem sheet defines the pressure attenuation factor as the **inverse**:
> $$\frac{P_i}{P_t}=\frac{1}{T_{p,12}}.$$
> Reversing the incident side swaps indices: $R_{21}=-R_{12}$.

> [!important] Pressure amplification does not mean power amplification
> A transmitted pressure approaching $2P_i$ is possible when $Z_2\gg Z_1$. For real, lossless impedances the transmitted intensity fraction is
> $$\tau=\frac{Z_1}{Z_2}|T_p|^2=\frac{4Z_1Z_2}{(Z_1+Z_2)^2},\qquad |R|^2+\tau=1.$$
> Air–water is a large impedance mismatch, so almost all incident power is reflected in either direction.

## 5. Spherical waves — why pressure falls as $1/r$ (slides 26–30)

For spherical symmetry there is no angular dependence:
$$\frac{\partial^2p}{\partial r^2}+\frac{2}{r}\frac{\partial p}{\partial r}=\frac{1}{c^2}\frac{\partial^2p}{\partial t^2}.$$
Multiplying by $r$ turns this into a one-dimensional wave equation for $rp$:
$$\frac{\partial^2(rp)}{\partial r^2}=\frac{1}{c^2}\frac{\partial^2(rp)}{\partial t^2}.$$
Thus the harmonic solution contains outgoing and incoming waves,
$$P(r)=\frac{Ae^{-jkr}+Be^{jkr}}{r}.$$

> [!success] Free field, outgoing wave only
> $$P(r)=\frac{Ae^{-jkr}}{r},\qquad P(r)=P(r_0)\frac{r_0}{r}e^{-jk(r-r_0)}.$$
> $$|P(r)|=|P(r_0)|\frac{r_0}{r}.$$
> Distance causes both phase delay and geometric spreading. This idealization applies outside the small source; the singularity at $r=0$ is not a physical source model.

## 6. Spherical particle velocity and impedance (slides 31–33)

Differentiate the outgoing pressure using Euler's equation:
$$\frac{dP}{dr}=\left(-jk-\frac1r\right)P,\qquad U_r=-\frac{1}{j\omega\rho}\frac{dP}{dr}.$$

> [!success] The near-field term matters
> $$U_r=\frac{P}{\rho c}\left(1+\frac{1}{jkr}\right),\qquad Z_s=\frac{P}{U_r}=\frac{\rho c}{1+1/(jkr)}.$$
> $$|U_r|=\frac{|P|}{\rho c}\sqrt{1+\frac{1}{(kr)^2}},\qquad \arg Z_s=\tan^{-1}\left(\frac{1}{kr}\right).$$
> With the $e^{j\omega t}$ convention, pressure **leads outward particle velocity** by this positive angle.

> [!note] Near field versus far field
> - $kr\gg1$: $U_r\approx P/(\rho c)$ and $Z_s\approx\rho c$; pressure and velocity are nearly in phase.
> - Small $kr$: the extra quadrature velocity is important; using the plane-wave relation underestimates velocity amplitude.
> - The correction relative to the plane-wave velocity term is $1/(kr)$, so the useful threshold depends on the accuracy needed.

> [!tip] Connection to Electroacoustics
> Here $P/U_r$ is **specific acoustic impedance**, in Pa·s/m. The lumped acoustic circuits in [[Lecture 3 - Analogies - Acoustic Systems]] use pressure divided by **volume velocity**, in Pa·s/m³. For uniform flow through area $S$, volume velocity is $S U_r$ and the corresponding lumped impedance is $(P/U_r)/S$.

## 7. Problem session — 10:30–12:00 (slide 35)

> [!todo] Work through [[Week 2 - Reflection and Spherical Waves]]
> 1. Locate pressure nodes in a rigidly terminated tube.
> 2. Predict the change in an instrument's fundamental frequency.
> 3. Calculate reflection and pressure transmission in both directions across air–water.
> 4. Calculate spherical pressure, velocity and impedance phase near the source.
> 5. Verify a plane wave in the wave equation by differentiation.

## Summary — what to walk away with

> [!success] Key takeaways
> - Add pressure phasors, and retain the directional minus sign in reflected velocity.
> - Rigid end: $R=+1$, pressure antinode. Pressure-release end: $R=-1$, pressure node.
> - Tube boundary conditions set the resonance sequence; frequencies scale with sound speed.
> - Impedance mismatch causes reflection; pressure transmission and power transmission are different quantities.
> - Outgoing spherical pressure scales as $1/r$; near-field particle velocity also contains a $1/r^2$ term.

> [!todo] Notes and questions from class
> - ⬜
