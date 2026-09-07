---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: exercise
date: 2026-09-08
week: 37
status: prepared
tags: [Acoustics, exercise, MATLAB]
---
# Week 2 — Reflection and Spherical Waves

> [!info] Materials
> **Lecture:** [[Lecture 2 - Plane Waves Reflection and Spherical Waves]]
> **Questions and supplied answers:** [[34840_Problems2.pdf|Original Week 2 sheet]]
> **MATLAB starter:** [Open Week2_Reflection_SphericalWaves.m](../../../../../5.%20Semester/Acoustics%20and%20Noise%20Control/Matlab/Week2_Reflection_SphericalWaves.m)
> Stored in `5. Semester/Acoustics and Noise Control/Matlab/`. Open in MATLAB, run setup, then solve one `%%` section at a time. Replace `NaN` placeholders with your own expressions. Plotting and result tables activate when the required values are filled in.

> [!note] Assumptions and conventions
> Use $c_{air}=343$ m/s, $\rho_{air}=1.204$ kg/m³, $c_{water}=1480$ m/s and $\rho_{water}=1000$ kg/m³. The sheet supplies the water and helium sound speeds, but not densities; these are stated working assumptions. Small rounding differences from the printed answers are expected.
> Use peak phasors with $e^{j\omega t}$, SI units, `1i` for the imaginary unit, and `.*`, `./`, `.^` for elementwise vector calculations.

## 1. Standing-wave tube

> [!question] Problem 1
> A tube is driven at **1 kHz** and rigidly terminated at the other end. At which distances from the rigid termination does pressure become very small?

> [!todo] Preparation and working
> - Start with the rigid-wall boundary condition and write the pressure envelope.
> - Set that envelope to zero; express all node distances using an integer index.
> - Calculate the first three distances in metres, then centimetres.
> - Use the MATLAB plot to check the predicted nodes.
>
> $\lambda=$ ⬜ · node condition: ⬜ · $d_n=$ ⬜
> **Result and interpretation:** ⬜

## 2. Instrument filled with helium

> [!question] Problem 2
> How does replacing air with helium change a trumpet's **lowest resonance frequency**, assuming $c_{He}=1000$ m/s?

> [!todo] Preparation and working
> The geometry stays fixed. Write the resonance frequency in terms of sound speed and the geometry-dependent wavelength, then form $f_{He}/f_{air}$ so the wavelength cancels. An absolute frequency is not required and no instrument length is provided.
>
> Frequency ratio: ⬜ · explanation: ⬜

## 3. Air–water reflection and transmission

> [!question] Problem 3
> **3.1:** Find the pressure reflection coefficient for a plane wave incident normally from air onto water.
> **3.2:** Repeat for incidence from water onto air.
> **3.3:** Find the pressure attenuation factor $P_i/P_t$ in both directions. Use $c_{water}=1480$ m/s.

> [!todo] Preparation and working
> 1. Calculate both characteristic impedances, $Z=\rho c$.
> 2. Label the incident medium as 1 and the transmitted medium as 2.
> 3. Apply $P_i+P_r=P_t$ and $(P_i-P_r)/Z_1=P_t/Z_2$.
> 4. Find $R=P_r/P_i$ and $T_p=P_t/P_i$; invert $T_p$ for the requested attenuation factor.
> 5. Swap media for the reverse direction. Explain the sign of each reflection.
>
> | Direction | $R$ | $P_t/P_i$ | Requested $P_i/P_t$ |
> |---|---|---|---|
> | Air → water | ⬜ | ⬜ | ⬜ |
> | Water → air | ⬜ | ⬜ | ⬜ |
>
> **Why transmitted pressure can increase without an increase in transmitted power:** ⬜

## 4. Spherical wave near a small source

> [!question] Problem 4
> A small omnidirectional source emits at **250 Hz**, with pressure amplitude **0.5 Pa at 1 m**, in a free field.
> **4.1:** Find pressure amplitude at **10 cm**.
> **4.2:** Find particle velocity amplitude there.
> **4.3:** Find the phase angle of the complex ratio of pressure to particle velocity there.

> [!todo] Preparation and working
> - Convert 10 cm to metres; calculate $k$ and the dimensionless $kr$.
> - Use $1/r$ pressure spreading. For complex pressure, include phase relative to the 1 m reference.
> - Use the full spherical-wave velocity relation from the lecture note, including $1/(jkr)$.
> - Calculate the complex impedance first, then `angle(P/U)`; convert radians to degrees.
> - Compare velocity with the plane-wave approximation and explain any difference.
>
> $kr=$ ⬜ · $|P|=$ ⬜ Pa · $|U_r|=$ ⬜ mm/s
> $Z_s=$ ⬜ Pa·s/m · $\arg Z_s=$ ⬜ rad = ⬜ °
> **Which quantity leads, with the stated phasor convention?** ⬜

## 5. Verify the wave equation

> [!question] Problem 5
> Show that $\hat p=Ae^{j(\omega t-kx)}$ solves
> $$\frac{\partial^2p}{\partial x^2}=\frac{1}{c^2}\frac{\partial^2p}{\partial t^2}.$$

> [!todo] Derivation space
> $$\frac{\partial\hat p}{\partial x}=\boxed{\phantom{xxxxxxxx}},\qquad \frac{\partial^2\hat p}{\partial x^2}=\boxed{\phantom{xxxxxxxx}}$$
> $$\frac{\partial\hat p}{\partial t}=\boxed{\phantom{xxxxxxxx}},\qquad \frac{\partial^2\hat p}{\partial t^2}=\boxed{\phantom{xxxxxxxx}}$$
> Substitute, cancel the common exponential, and state the required relationship between $k$, $\omega$ and $c$: ⬜
> MATLAB provides an optional numerical residual check, using your analytic derivatives. The written derivation establishes the result for all $x,t$.

---

> [!check]- Supplied answers — open after attempting
> These are transcribed from the original sheet, not completed working.
> - **1:** 8.6 cm; 25.7 cm; 42.9 cm; …
> - **2:** frequency increases by a factor of 2.91.
> - **3.1:** 0.99944. **3.2:** −0.99944.
> - **3.3:** air → water: 0.5; water → air: 1793.
> - **4.1:** 5 Pa. **4.2:** 29 mm/s. **4.3:** +1.14 rad = +65.4°.
> - **5:** no printed answer; show the differentiation.

> [!todo] Completion checklist
> - [ ] Solve problems 1–2 and explain the physical results.
> - [ ] Solve all three parts of problem 3, keeping incident/transmitted media explicit.
> - [ ] Solve all three parts of problem 4 with the spherical near-field term.
> - [ ] Write the proof for problem 5.
> - [ ] Compare with the supplied answers and record questions for class.
