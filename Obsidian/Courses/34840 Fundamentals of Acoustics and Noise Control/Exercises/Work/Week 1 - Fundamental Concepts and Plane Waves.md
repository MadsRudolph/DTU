---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: exercise
date: 2026-09-01
week: 36
status: prepared
tags: [Acoustics, exercise, MATLAB]
---
# Week 1 — Fundamental Concepts and Plane Waves

> [!info] Materials
> **Lecture:** [[Lecture 1 - Introduction and Plane Waves]]
> **Problem sheet:** [[34840-Problems 1.pdf|Original Week 1 problems]]
> **MATLAB:** [Open Week1_Fundamentals_PlaneWaves.m](../../../../../5.%20Semester/Acoustics%20and%20Noise%20Control/Matlab/Week1_Fundamentals_PlaneWaves.m)
> Run the setup first, then use **Run Section** for each problem. Fill the `NaN` placeholders with your expressions. Tables and plots activate once the required variables are filled in. Your calculations are deliberately left for you to solve.

> [!note] Constants and conventions
> Air at 20°C and 101.3 kPa: $c=343$ m/s, $\rho_0=1.204$ kg/m³, $\rho_0c\approx413$ Pa·s/m, $\gamma=1.401$. These match the supplied solutions to their stated precision. Temperature conversion uses 273.15 rather than the rounded 273 in the solutions.
> All amplitudes are **peak**, with the $e^{j\omega t}$ convention. Use `1i`, `abs`, `angle`, and elementwise operations for vectors.

## 1. Harmonic plane wave

> [!question] Problem 1
> A plane wave has pressure amplitude **1 Pa** and frequency **1 kHz**, at normal ambient conditions (**20°C, 101.3 kPa**).
> **1.1:** Calculate wavelength and wavenumber.
> **1.2:** Calculate particle velocity amplitude and particle displacement amplitude.

> [!todo] Preparation and working
> - Connect $f$, $\omega$, $\lambda$ and $k$ using sound speed.
> - Use the travelling-plane-wave impedance to obtain particle velocity.
> - Integrate velocity in harmonic form to obtain displacement; retain the complex phase until taking the amplitude.
> - Report wavelength in cm, velocity in mm/s, and displacement in µm.
>
> $\lambda=$ ⬜ · $k=$ ⬜ · $|U|=$ ⬜ · $|\Xi|=$ ⬜
> **Pressure/velocity/displacement phase relationships:** ⬜

## 2. Two coherent loudspeakers

> [!question] Problem 2
> Two identical loudspeakers each produce **0.5 Pa** pressure amplitude separately at the same observation point. They receive the same pure tone, are equally distant from the observation point, and there are no reflecting surfaces. Find total pressure amplitude for:
> **2.1:** in phase; **2.2:** 90° lag in one channel; **2.3:** 180° lag; **2.4:** 179° lag.

> [!todo] Preparation and working
> Choose the first loudspeaker as the phase reference. Represent the second using a negative phase angle for the lag, add the two complex pressures, then take `abs`.
> Use the four-panel MATLAB phasor plot to explain cancellation. A tiny floating-point residual at 180° represents numerical round-off.
>
> | Part | Lag | Complex sum [Pa] | Amplitude [Pa] |
> |---|---|---|---|
> | 2.1 | 0° | ⬜ | ⬜ |
> | 2.2 | 90° | ⬜ | ⬜ |
> | 2.3 | 180° | ⬜ | ⬜ |
> | 2.4 | 179° | ⬜ | ⬜ |
>
> **Why does a 1° departure from antiphase leave a residual?** ⬜
> **Why should we add phasors rather than powers here?** ⬜

## 3. Adiabatic cavity compression

> [!question] Problem 3
> A hearing-aid loudspeaker causes a harmonic fractional volume variation of amplitude **0.002%** in the cavity between the hearing aid and eardrum.
> **3.1:** Assuming adiabatic compression, find the sound pressure amplitude.

> [!todo] Preparation and working
> - Convert the percentage into a dimensionless fractional volume amplitude.
> - Start from $p/p_0=-\gamma\Delta V/V_0$.
> - Distinguish the signed pressure change from its nonnegative amplitude.
>
> Fractional volume amplitude: ⬜ · pressure amplitude: ⬜ Pa
> **Why does compression increase pressure?** ⬜

## 4. Temperature and organ-pipe tuning

> [!question] Problem 4
> A church's temperature varies between **15°C in winter** and **32°C in summer**.
> **4.1:** Calculate $c_{summer}/c_{winter}$.
> An open organ pipe's fundamental occurs when its length equals half a wavelength. It is tuned to **110 Hz in summer**.
> **4.2:** Calculate its fundamental frequency in winter.

> [!todo] Preparation and working
> - Convert both temperatures to kelvin before taking a ratio.
> - Use $c=\sqrt{\gamma R_sT}$; common gas constants cancel in the ratio.
> - Assume fixed pipe length. Use $f_0=c/(2L)$ and cancel the length to obtain winter tuning.
> - Predict the direction of the frequency shift before evaluating it.
>
> $T_w=$ ⬜ K · $T_s=$ ⬜ K · $c_s/c_w=$ ⬜
> $f_w=$ ⬜ Hz · **physical explanation:** ⬜

---

> [!check]- Supplied answers and solutions — open after attempting
> - **1.1:** 34.3 cm; 18.3 rad/m.
> - **1.2:** 2.42 mm/s; 0.385 µm.
> - **2.1–2.4:** 1 Pa; 0.71 Pa; 0 Pa; 8.7 mPa.
> - **3.1:** 2.84 Pa.
> - **4.1:** 1.029. **4.2:** 106.9 Hz, approximately a quarter-tone drop.
> These are the answers printed on the problem sheet. [[34840_Solutions1.pdf|Open the supplied worked solutions]] for the derivations and phasor diagrams.
> In MATLAB, set `show_reference_answers = true` and run the final section to display the same reference values.

> [!todo] Completion checklist
> - [ ] Problem 1: wave quantities, velocity and displacement with units.
> - [ ] Problem 2: all four phase lags and an explanation of cancellation.
> - [ ] Problem 3: correct percentage conversion and compression relation.
> - [ ] Problem 4: kelvin temperatures and correct tuning direction.
> - [ ] Compare against the supplied solutions and record remaining questions.
