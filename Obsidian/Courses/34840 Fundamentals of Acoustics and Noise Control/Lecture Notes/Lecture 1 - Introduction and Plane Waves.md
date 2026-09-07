---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: lecture-note
date: 2026-09-01
week: 36
lecture: 1
topic: "Introduction, fundamental concepts and plane waves"
lecturer: FA
tags: [Acoustics, lecture-note, plane-waves, wave-equation, phasors]
---
# Lecture 1 — Introduction and Plane Waves

> [!info] Lecture Info
> **Date:** Tuesday 1 September 2026, 08:00–12:00 · building 358, room 063 · **Finn Agerkvist**
> **Main slides:** [[34840_Lecture1_2026_v1.pdf|PDF]] · [[34840_Lecture1_2026_v1.pptx|Open PowerPoint]]
> **Wave-equation supplement:** [[34840_Lecture1_waveequation_26.pdf|PDF derivation]] · [[34840_Lecture1_waveequation_26.pptx|Open PowerPoint derivation]]
> **Reading:** [[Fundamentals_of_acoustics_2022.pdf|Course text]], printed pp. 1–8.
> **Problems:** [[Week 1 - Fundamental Concepts and Plane Waves|Week 1 preparation + MATLAB]]
> **Next:** [[Lecture 2 - Plane Waves Reflection and Spherical Waves|Lecture 2]] · **Course:** [[34840 Fundamentals of Acoustics and Noise Control]]

> [!abstract] Where this lecture sits
> The starting point is a small pressure disturbance in a fluid. Newton's second law, conservation of mass and an adiabatic pressure–density relation connect that disturbance to particle motion and give the wave equation. Complex notation then makes harmonic waves and interference straightforward to calculate.
> Prepared from both supplied slide decks and the course material; the working spaces are for your additions.

---

## 1. Course introduction and applications (slides 1–16)

The course connects sound propagation to measurement, radiation, room acoustics, hearing and noise control. The introductory examples include source identification, microphone arrays, hearing aids, sound perception and room acoustics. See the [[34840 Fundamentals of Acoustics and Noise Control|course home]] for the full lecture plan.

> [!note] Preparation
> Complex numbers and harmonic signal analysis are prerequisites. The course provides [[1-Basics on complex numbers.pdf|complex-number theory]], [[2-Exercises on complex numbers.pdf|practice problems]] and [[3-Solutions to Exercises on complex numbers.pdf|solutions]], alongside Signals & Systems material in `Literature/00 - Prerequisites/`.

> [!warning] Conflicting assignment dates in the supplied material
> Main slide 4 says the individual problem set is uploaded **30 September**, due **13 October**. The existing course plan/home records **28 September / 9 October**. These sources disagree; confirm the current dates on DTU Learn before relying on either. This note does not resolve that discrepancy.

## 2. Sound pressure and particle motion (slides 17–20)

> [!abstract] Definitions
> Write total pressure as $p_{tot}=p_0+p$, where $p_0$ is ambient static pressure and $p$ is the small acoustic fluctuation.
>
> | Quantity | Symbol | Unit | Meaning |
> |---|---|---|---|
> | Static pressure | $p_0$ | Pa | Equilibrium pressure, about 101.3 kPa here |
> | Sound pressure | $p$ | Pa | Time-varying departure from equilibrium |
> | Equilibrium density | $\rho_0$ | kg/m³ | About 1.204 for the exercise assumptions |
> | Particle velocity | $u$ | m/s | Local oscillatory motion of the fluid |
> | Particle displacement | $\xi$ | m | Motion about the equilibrium position |
> | Sound speed | $c$ | m/s | Propagation speed, about 343 in air at 20°C |

> [!important] Particle velocity is not sound speed
> In a longitudinal plane wave, fluid particles oscillate along the propagation axis. The disturbance travels through the medium at $c$; particles do not travel with it at that speed.
> Linear acoustics assumes small perturbations, including $|p|\ll p_0$ and $|u|\ll c$.

## 3. Travelling and harmonic waves (slides 21–25)

A one-dimensional travelling field can be written
$$p(x,t)=f_+(t-x/c)+f_-(t+x/c).$$
The first term travels towards $+x$, the second towards $-x$. To check direction, hold the function's argument constant and follow its position as time increases.

> [!success] Single harmonic wave travelling towards $+x$
> $$p(x,t)=\hat p\cos(\omega t-kx+\varphi),$$
> $$\omega=2\pi f,\qquad \lambda=\frac{c}{f},\qquad k=\frac{2\pi}{\lambda}=\frac{\omega}{c}.$$
> $\hat p$ here is a real peak amplitude, in Pa; $\varphi$ is the phase. Wavenumber is in rad/m and wavelength in m.
> At a fixed position the period is $1/f$; at a fixed instant the spatial period is $\lambda$.

> [!todo] Check your intuition
> - How does wavelength change when frequency doubles? ⬜
> - Why does replacing $-kx$ with $+kx$ reverse propagation? ⬜

## 4. Deriving the 1D wave equation (slide 26 + supplement 1–7)

Use a uniform, stationary equilibrium fluid and small, lossless perturbations. Write density as $\rho=\rho_0+\rho'$. Products of perturbations are neglected.

### Step 1 — Newton's second law / Euler's equation

For a thin fluid slice of area $S$ and length $dx$, the net pressure force is approximately $-S(\partial p/\partial x)dx$, and mass is $\rho_0Sdx$. Therefore
$$\boxed{\rho_0\frac{\partial u}{\partial t}=-\frac{\partial p}{\partial x}}.$$

### Step 2 — conservation of mass

If more fluid leaves a fixed slice than enters, its density falls:
$$\boxed{\frac{\partial\rho'}{\partial t}=-\rho_0\frac{\partial u}{\partial x}}.$$

### Step 3 — pressure–density relation

For small **adiabatic** changes of an ideal gas,
$$\frac{p}{p_0}=\gamma\frac{\rho'}{\rho_0}=-\gamma\frac{\Delta V}{V_0},\qquad \gamma\approx1.4.$$
Consequently,
$$\boxed{p=c^2\rho',\qquad c^2=\frac{\gamma p_0}{\rho_0}}.$$

> [!note] Why adiabatic matters
> Adiabatic means no heat exchange during compression/expansion. The supplement first shows the isothermal relation without $\gamma$, then the adiabatic acoustic model. Compression ($\Delta V<0$) raises pressure ($p>0$).

### Step 4 — combine the three relations

Differentiate continuity with respect to time and Euler's equation with respect to position:
$$\frac{\partial^2\rho'}{\partial t^2}=-\rho_0\frac{\partial^2u}{\partial x\partial t}=\frac{\partial^2p}{\partial x^2}.$$
Substitute $\rho'=p/c^2$:

> [!success] One-dimensional wave equation
> $$\boxed{\frac{\partial^2p}{\partial x^2}=\frac{1}{c^2}\frac{\partial^2p}{\partial t^2}}.$$
> The equation links spatial curvature to temporal acceleration of pressure; $c$ determines propagation speed.

## 5. Complex notation and superposition (slides 29–32)

> [!note] Phasor convention
> From here use capital letters for complex peak phasors:
> $$p(x,t)=\Re\{P(x)e^{j\omega t}\},\qquad P(x)=Ae^{-jkx},\qquad A=|A|e^{j\varphi}.$$
> A phasor contains amplitude and phase, with the common time factor suppressed. In MATLAB use `1i`, `abs`, `angle` and `exp`. Convert degrees to radians before using a complex exponential.

For harmonic steady state,
$$\frac{\partial}{\partial t}\longleftrightarrow j\omega,\qquad \int dt\longleftrightarrow\frac{1}{j\omega}.$$

> [!example] Adding two equal-frequency waves
> Add the **complex pressures first**, then take the magnitude:
> $$P_{tot}=P_1+P_2.$$
> For equal peak amplitudes $a$ and a phase lag $\theta$ in the second channel,
> $$P_{tot}=a(1+e^{-j\theta}),\qquad |P_{tot}|=2a\left|\cos\frac{\theta}{2}\right|.$$
> The main slides illustrate $1-j=\sqrt2e^{-j\pi/4}$: amplitude $\sqrt2$, phase $-\pi/4$.

> [!important] Coherent addition
> The Week 1 loudspeakers are driven with the same pure tone, with equal path lengths to the observation point. Their relative phase matters. Adding magnitudes or adding uncorrelated powers would not describe this setup.

## 6. Plane-wave velocity and displacement (slides 27–28, 33–34)

With $P=Ae^{-jkx}$, Euler's equation gives
$$j\omega\rho_0U_x=-\frac{dP}{dx}=jkP.$$

> [!success] Pressure and velocity in a forward plane wave
> $$U_x=\frac{P}{\rho_0c},\qquad Z_0=\rho_0c\approx413\ \mathrm{Pa\,s/m}.$$
> Pressure and velocity are in phase. This ratio is the **characteristic impedance of the medium**. For a backward travelling wave the velocity component along $+x$ has the opposite sign.

Since $u=\partial\xi/\partial t$,
$$\Xi=\frac{U_x}{j\omega},\qquad |\Xi|=\frac{|U_x|}{\omega}=\frac{|P|}{\omega\rho_0c}.$$

> [!note] Phase and amplitude
> Displacement lags velocity by 90° with the $e^{j\omega t}$ convention. At fixed pressure amplitude, displacement increases as frequency decreases. All exercise amplitudes are peak values; do not insert an RMS factor of $\sqrt2$.

## 7. Sound speed, temperature and cavity compression (slide 35)

For an ideal gas, $p_0=\rho_0R_sT$, with specific gas constant $R_s\approx287$ J/(kg·K) for air. Thus
$$\boxed{c=\sqrt{\gamma R_sT}}.$$

> [!important] Use absolute temperature
> $$T[\mathrm K]=T[{}^\circ\mathrm C]+273.15,\qquad \frac{c_2}{c_1}=\sqrt{\frac{T_2}{T_1}}.$$
> For fixed ideal pipe geometry, resonance frequencies scale with $c$. An open pipe's fundamental has $L=\lambda/2$, so $f_0=c/(2L)$.

> [!success] Small adiabatic cavity compression
> $$p=-\gamma p_0\frac{\Delta V}{V_0},\qquad |p|=\gamma p_0\left|\frac{\Delta V}{V_0}\right|.$$
> A fractional volume variation supplied in percent must be divided by 100 before substitution. The signed relation describes compression/expansion; the amplitude is nonnegative.

## 8. Three dimensions and frequency domain (slides 36–38)

The same physical relations become
$$\rho_0\frac{\partial\mathbf u}{\partial t}=-\nabla p,\qquad \frac{\partial\rho'}{\partial t}=-\rho_0\nabla\cdot\mathbf u.$$
Combining with $p=c^2\rho'$ gives
$$\nabla^2p=\frac{1}{c^2}\frac{\partial^2p}{\partial t^2}.$$
For a single frequency, the time derivative contributes $-\omega^2$:
$$\boxed{\nabla^2P+k^2P=0}.$$
This is the **Helmholtz equation**. In 1D it reduces to $d^2P/dx^2+k^2P=0$.

## 9. Propagation demonstrations (slides 39–42)

The closing demonstrations discuss echoes, lightning, moving sources and the Doppler effect. A moving source changes the spacing of arriving wavefronts, giving a higher observed frequency on approach and a lower one on recession for a stationary listener in a stationary medium. Use the original PowerPoint for any dynamic demonstrations.

> [!todo] Observation notes
> - Example demonstrating finite propagation speed: ⬜
> - Explain the approaching/receding frequency shift using wavefront spacing: ⬜

## 10. Problem preparation

> [!todo] Work through [[Week 1 - Fundamental Concepts and Plane Waves]]
> 1. Wavelength, wavenumber, particle velocity and displacement.
> 2. Coherent addition of two loudspeakers at four phase differences.
> 3. Pressure caused by adiabatic compression of an ear-canal cavity.
> 4. Temperature dependence of sound speed and organ-pipe tuning.

## Summary — what to walk away with

> [!success] Key takeaways
> - Sound is a small pressure disturbance linked to local particle motion.
> - $\lambda=c/f$ and $k=\omega/c$ connect temporal and spatial oscillation.
> - Euler + continuity + adiabatic compression give the wave equation.
> - Add complex amplitudes before taking magnitudes.
> - For a forward plane wave, $U=P/(\rho_0c)$ and $\Xi=U/(j\omega)$.
> - For ideal air, $c\propto\sqrt T$ with temperature in kelvin.

> [!tip] Looking ahead
> [[Lecture 2 - Plane Waves Reflection and Spherical Waves|Lecture 2]] combines forward and backward waves into standing waves, then examines how spherical spreading changes the pressure–velocity relation.
