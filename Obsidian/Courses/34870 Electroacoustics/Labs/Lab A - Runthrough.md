---
course: "34870"
course-name: "Electroacoustics"
type: lab-note
date: 2026-09-10
lab: A
topic: "Lab A — Analogy circuits (mechanical, acoustic, coupled)"
tags: [Electroacoustics, lab-note, analogies, LTspice, ngspice, KiCad]
---
# Lab A — Analogy Circuits: full runthrough

> [!info] Lab Info
> **Brief:** `Labs/34870 Lab A_2026.pdf` (4 parts + quiz) · **Period:** 8/9 – 20/9 · **Group work** allowed, but every student should attempt every task
> **Quiz:** individual, in DTU Learn, opens Thu 10/9 (previewed in the morning lecture) · ⏰ **deadline Sun 20 Sep 2026, before midnight**
> **Why it matters:** submitting *and passing* all lab + project quizzes is **mandatory to sit the exam**, and together they are **30 % of the grade**. Sign up to an open *34870 Lab Group* in DTU Learn if you are not in one yet (announcement from Frieder, 9/9).
> **Theory:** [[Lecture 2 - Analogies - Mechanical Systems]] (mobility analogy) · [[Lecture 3 - Analogies - Acoustic Systems]] (acoustic elements, radiation impedance §8) · [[Lecture 4 - Analogies - Transducers & Dynamic Microphones]] (coupling with controlled sources)
> **Done here in:** KiCad 10 + ngspice 47 (the physics is tool-agnostic; the quiz wants LTspice screenshots — see the LTspice tips in every part)
> **Full write-up:** `Lab A - Report (KiCad-ngspice).pdf` in this folder (LaTeX source in `5. Semester/Electroacoustics/Labs/Lab A/report/`)

> [!abstract] How this lab is built
> Every part is the same recipe from the lectures: **pick an analogy, map each physical element to R/L/C, hook domains together with controlled sources, run an AC sweep, read velocities/pressures off node voltages and forces/volume velocities off branch currents.**
>
> | Domain | Analogy used | Across = node voltage | Through = branch current | Mass | Compliance | Damping |
> |---|---|---|---|---|---|---|
> | Mechanical | **mobility** | velocity $u$ [m/s] | force $f$ [N] | $C = M_M$ (to ground) | $L = C_M$ | $R = 1/R_M$ |
> | Acoustical | **impedance** | pressure $p$ [Pa] | volume velocity $U$ [m³/s] | $L = M_A$ | $C = C_A$ (to ground!) | $R = R_A$ |
>
> Couplings (Lecture 4A): vibrating area $S$ → $f = S\,p$, $U = S\,u$ (two G sources, gain $S$ each). Coil in a field → $f = Bl\,i$ (G source), $v_\text{emf} = Bl\,u$ (E source). Air everywhere: $\rho = 1.18$ kg/m³, $c = 344$ m/s.
>
> Everything lives in `5. Semester/Electroacoustics/Labs/Lab A/`: `KiCad/<project>/` (schematic, workbook, exported `.cir`), `sim/partN.py` (rebuild → export → ngspice → plots → numbers), `figures/`, `results/partN.md` (all extracted numbers). The plots below are those figures.

---

## Part 1 — Mechanical system: dual-diaphragm loudspeaker

### Model

Two moving masses. The coil + former + inner cone is $M_{mvc}$ (6 g), driven by the force $F$ and hanging on the spider $C_{msp} \| R_{msp}$. The outer cone $M_{md}$ (5 g) hangs on the surround $C_{msr} \| R_{msr}$ and is joined to $M_{mvc}$ through the deliberately soft link $C_{md} \| R_{md}$. Mobility analogy → two velocity nodes `u_vc` and `u_d`; the force is a 1 A current source into `u_vc`.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american,scale=0.85,every node/.style={transform shape}]
\draw (0,0) node[ground]{} to[isource, l=$F$] (0,3) -- (1.5,3) node[circ]{} node[above]{$u_{vc}$};
\draw (1.5,3) to[C, l_=$M_{mvc}$] (1.5,0) node[ground]{};
\draw (3,3) to[L, l_=$C_{msp}$] (3,0) node[ground]{};
\draw (4.5,3) to[R, l_=$1/R_{msp}$] (4.5,0) node[ground]{};
\draw (1.5,3) -- (4.5,3) -- (5.5,3) to[L, l=$C_{md}$] (8,3) -- (9,3) node[circ]{} node[above]{$u_d$};
\draw (5.5,3) -- (5.5,4.3) to[R, l=$1/R_{md}$] (8,4.3) -- (8,3);
\draw (9,3) to[C, l_=$M_{md}$] (9,0) node[ground]{};
\draw (10.5,3) to[L, l_=$C_{msr}$] (10.5,0) node[ground]{};
\draw (12,3) to[R, l_=$1/R_{msr}$] (12,0) node[ground]{};
\draw (9,3) -- (12,3);
\end{circuitikz}
\end{document}
```

| Physical | Value | SPICE | Value | Between |
|---|---|---|---|---|
| $F$ | 1 N | I1, AC 1 | 1 A | gnd → `u_vc` |
| $M_{mvc}$ | 6 g | C1 | 6 mF | `u_vc` – gnd |
| $C_{msp}$ | 1.3 mm/N | L1 | 1.3 mH | `u_vc` – gnd |
| $R_{msp}$ | 0.5 Ns/m | R1 = 1/R | 2 Ω | `u_vc` – gnd |
| $C_{md}$ stiff / soft | 1e‑10 / 3e‑6 m/N | L2 | 100 pH / 3 µH | `u_vc` – `u_d` |
| $R_{md}$ stiff / soft | 5000 / 5 Ns/m | R2 = 1/R | 0.2 mΩ / 0.2 Ω | `u_vc` – `u_d` |
| $M_{md}$ | 5 g | C2 | 5 mF | `u_d` – gnd |
| $C_{msr}$ | 2.7 mm/N | L3 | 2.7 mH | `u_d` – gnd |
| $R_{msr}$ | 0.22 Ns/m | R3 = 1/R | 4.545 Ω | `u_d` – gnd |

Sweep `.ac dec 200 10 10k`. Projects: `KiCad/Part1_DualDiaphragm_Stiff/`, `KiCad/Part1_DualDiaphragm_Soft/`.

> [!note] Hand estimates before pressing Run
> - Suspensions in parallel → stiffnesses add: $1/C_{tot} = 1/1.3 + 1/2.7$ (N/mm) → $C_{tot} = 0.878$ mm/N; $M_{tot} = 11$ g; $R_{tot} = 0.72$ Ns/m.
> - Stiff link: one body, $f_0 = 1/(2\pi\sqrt{M_{tot} C_{tot}}) = \mathbf{51.2\ Hz}$, peak velocity $1/R_{tot} = 1.39$ m/s per N, $Q \approx 4.9$.
> - Soft link: outer cone on the link spring alone $1/(2\pi\sqrt{M_{md} C_{md}}) = 1300$ Hz (the absorber frequency); the two masses bouncing against each other through $C_{md}$ with reduced mass 2.73 g → $\approx 1760$ Hz.

### a) Velocity of the two masses, stiff vs soft link

![[part1a_velocities.png]]
![[part1_velocity_ratio.png]]

> [!success] Answer 1a
> | Case | Feature | Frequency | Value |
> |---|---|---|---|
> | Stiff | single resonance, $u_{vc} = u_d$ | 51.3 Hz | 1.389 m/s per N (= $1/R_{tot}$) |
> | Stiff | $u_d / u_{vc}$ over the whole band | – | 1.000 (0.998 at 10 kHz) |
> | Soft | first resonance, masses in phase | 51.3 Hz | 1.388 (coil), 1.389 (cone) |
> | Soft | dip in $u_{vc}$ (anti-resonance) | 1288 Hz | 0.0030 m/s per N |
> | Soft | max of $u_d$ near the link resonance | 1738 Hz | 0.0493 |
> | Soft | second resonance, masses in anti-phase | 1799 Hz | $u_{vc}$ = 0.0415 |
> | Soft | $u_{vc}/u_d$ at 10 kHz | – | 42 (outer cone 32 dB below the coil) |
>
> **Stiff connection.** $C_{md} = 10^{-10}$ m/N is a rigid rod at every frequency of interest (its own resonance with the 5 g cone would sit at 225 kHz), so the two masses move as one 11 g body on the two suspensions in parallel. One resonance at 51 Hz; below it the compliance controls (velocity rises with frequency, +90°), above it the mass controls (velocity falls 6 dB/octave, −90°). The two velocity curves are identical.
>
> **Soft connection.** Below roughly 300 Hz the link is still stiff compared with the inertia of the masses, so the low resonance is unchanged (51 Hz, same peak). Around 1.3 kHz the outer cone on its soft spring becomes a **tuned absorber**: it resonates against the coil, the reaction force through $C_{md}$ cancels the drive, and the coil velocity dips by about 30 dB (1288 Hz) while the cone is still moving. Just above that (1.7–1.8 kHz) the two masses swing in anti-phase (second resonance, the phase of $u_d$ goes through −180°). Above that the soft link cannot transmit force any more (through a compliance the transmitted velocity falls as $1/\omega^2$): the outer cone rolls off 12 dB/octave faster than the coil, and the coil ends up driving only its own 6 g. **That is the dual-diaphragm trick**: the big cone works up to ~1.5 kHz, then decouples, and the light inner cone alone carries the top octaves without the mass and break-up of the large cone.

### b) Mechanical input impedance seen by the force

![[part1b_impedance.png]]

> [!success] Answer 1b
> $Z_M = F/u_{vc} = 1/V(u_{vc})$ with a 1 A source (mobility analogy → the impedance is the inverse of the node voltage).
>
> | Case | Feature | Frequency | $|Z_M|$ |
> |---|---|---|---|
> | both | compliance line at 10 Hz | 10 Hz | 0.72 − j17.4 Ns/m (≈ $1/\omega C_{tot}$ = 18.1) |
> | both | resonance (minimum) | 51.3 Hz | **0.720 Ns/m = $R_{tot}$**, phase 0° |
> | Stiff | mass line at 10 kHz | 10 kHz | 0.74 + j692 (= $\omega M_{tot}$, 11 g) |
> | Soft | anti-resonance (maximum) | 1288 Hz | **334 Ns/m** |
> | Soft | second resonance (minimum) | 1799 Hz | 24.1 Ns/m |
> | Soft | mass line at 10 kHz | 10 kHz | 5.7 + j372 (= $\omega M_{mvc}$, only 6 g) |
>
> The impedance plot is the mirror image of the coil velocity. Below resonance the suspension dominates: $|Z| \propto 1/f$ at −90° (compliance line). At resonance the two reactances cancel and the floor is the pure damping $R_{tot} = 0.72$ Ns/m at 0°. Above resonance the mass dominates: $|Z| \propto f$ at +90° (mass line). **Stiff:** one 11 g mass line all the way to 10 kHz. **Soft:** the mass line follows 11 g up to ~1 kHz, then the absorber produces a **maximum** (334 Ns/m: the outer cone pumps force back into the coil, the force source "sees a wall"), then a **minimum** at 1.8 kHz (anti-phase resonance), and finally the mass line continues at only 6 g because the outer cone has fallen off. The 5.7 Ns/m real part at 10 kHz is the power still dissipated in $R_{md}$ by the residual relative motion.

> [!tip] Doing Part 1 in LTspice for the quiz
> Same circuit, `I1` with `AC 1`, `.ac dec 200 10 10k`. Plot `V(u_vc)` and `V(u_d)` for a); for b) right-click the plot → *Add Traces* and type `1/V(u_vc)` (this is exactly the waveform-arithmetic hint in the brief). Put both cases in one sweep with `.step param Cmd list 1e-10 3e-6` and `.step param Rmd list 5000 5` (or just two copies of the circuit). Give the element values as text in the schematic.

---

## Part 2 — Acoustic system: car silencer

### Model

Seven elements in a row: narrow tubes 1, 3, 5, 7 (radius 2 mm) and expansion chambers 2, 4, 6. Impedance analogy. Each narrow tube = series acoustic mass $M_A = \rho l/S$ plus the given loss $R_A = 25\cdot10^3$ Pa·s/m³ in series. Each chamber = compliance $C_A = V/(\rho c^2)$ from its node **to ground** (closed volume → always grounded). That makes a ladder low-pass filter with nodes `p_in, p2, p4, p6, p_out`. A 0 V sense source `Vs1 … Vs7` sits in every narrow pipe so the pipe volume velocities are `I(Vs1) … I(Vs7)`.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american,scale=0.75,every node/.style={transform shape}]
\draw (0,0) node[ground]{} to[V, l=$p$ or $U$] (0,2.5)
  to[R, l=$R_{A1}$] (2,2.5) to[L, l=$M_{A1}$] (4,2.5) node[circ]{} node[above]{$p_2$}
  to[R, l=$R_{A3}$] (6,2.5) to[L, l=$M_{A3}$] (8,2.5) node[circ]{} node[above]{$p_4$}
  to[R, l=$R_{A5}$] (10,2.5) to[L, l=$M_{A5}$] (12,2.5) node[circ]{} node[above]{$p_6$}
  to[R, l=$R_{A7}$] (14,2.5) to[L, l=$M_{A7}$] (16,2.5) node[circ]{} node[above]{$p_{out}$};
\draw (4,2.5) to[C, l_=$C_{A2}$] (4,0) node[ground]{};
\draw (8,2.5) to[C, l_=$C_{A4}$] (8,0) node[ground]{};
\draw (12,2.5) to[C, l_=$C_{A6}$] (12,0) node[ground]{};
\draw (16,2.5) to[generic, l_=$Z_{rad}$] (16,0) node[ground]{};
\end{circuitikz}
\end{document}
```

For a)–c) the outlet is an ideal open end ($Z_{rad} = 0$, `p_out` = ground). For d)–e) the tube-end radiation network is inserted.

| Element | $r$ [mm] | $l$ [mm] | $S$ or $V$ | SPICE | Value |
|---|---|---|---|---|---|
| 1 tube | 2 | 25 | 1.257e‑5 m² | L1 + R | 2348 H + 25k Ω |
| 2 chamber | 10 | 50 | 15.7 cm³ | C2 | 1.125e‑10 F |
| 3 tube | 2 | 80 | 1.257e‑5 m² | L3 + R | 7512 H + 25k Ω |
| 4 chamber | 20 | 80 | 100.5 cm³ | C4 | 7.199e‑10 F |
| 5 tube | 2 | 100 | 1.257e‑5 m² | L5 + R | 9390 H + 25k Ω |
| 6 chamber | 15 | 60 | 42.4 cm³ | C6 | 3.037e‑10 F |
| 7 tube | 2 | 40 (38.77 in d/e) | 1.257e‑5 m² | L7 + R | 3756 H (3641) + 25k Ω |
| radiation $M_{A1}$ | – | – | $0.6133\rho/(\pi a)$ | L9 | 115.2 H |
| radiation $C_{A1}$ | – | – | $0.55\pi^2 a^3/(\rho c^2)$ | C9 | 3.11e‑13 F |
| radiation $R_{A1}$ | – | – | $0.5045\rho c/(\pi a^2)$ | R8 | 1.63e7 Ω |
| radiation $R_{A2}$ | – | – | $\rho c/(\pi a^2)$ | R9 | 3.23e7 Ω |

Sweep `.ac dec 200 10 1000`. Projects: `KiCad/Part2a_Silencer_PressureSource/` (V1 = 1 Pa), `KiCad/Part2b_Silencer_VolumeVelocitySource/` (I1 = 1 m³/s), `KiCad/Part2d_Silencer_Radiation/` (I1 + radiation network).

![[sch_Part2b_Silencer_VolumeVelocitySource.png]]

> [!note] Hand estimates: where the resonances should be
> Two-element pairs $f = 1/(2\pi\sqrt{M_A C_A})$ are only a rough guide (this is a 3-degree-of-freedom ladder). The better guess is "a chamber with the two tubes on either side in parallel":
>
> | Pair | $f$ |
> |---|---|
> | $C_{A2}$ with $M_{A1} \| M_{A3}$ | 355 Hz |
> | $C_{A4}$ with $M_{A3} \| M_{A5}$ | 92 Hz |
> | $C_{A6}$ with $M_{A5} \| M_{A7}$ | 176 Hz |
> | all four masses in series (23 006) with all three compliances in parallel (1.136e‑9) | 31 Hz |
>
> The 176 Hz (U-source peak) and 355 Hz (p-source peak) estimates land exactly on the simulation. Total series loss $\sum R_A = 10^5$ Pa·s/m³, total series mass $\sum M_A = 23\,006$ kg/m⁴ — already at 10 Hz $\omega \sum M_A = 1.45\cdot10^6 \gg \sum R_A$, so the masses, not the losses, set the pressure-source floor.

### a) Driven by a pressure source

![[part2a_pressure_source_Uout.png]]
![[part2_input_impedance.png]]

> [!success] Answer 2a
> $|U_{out}/p_{in}|$ from `I(Vs7)` with V1 = 1 Pa:
>
> | Feature | Frequency | Level (dB re 1 m³/(s·Pa)) |
> |---|---|---|
> | 10 Hz | – | −123.0 |
> | dip | 42.2 Hz | −132.0 |
> | **peak** | **76.7 Hz** | **−101.0** |
> | dip | 142.9 Hz | −143.9 |
> | **peak** | **179.9 Hz** | **−112.3** |
> | dip | 309.0 Hz | −170.3 |
> | **peak** | **354.8 Hz** | **−149.6** |
> | 1 kHz | – | −253.9 |
>
> With a pressure source the output is $U_{out} = (p_{in}/Z_{in}) \cdot (U_{out}/U_{in})$, so the low-frequency level is set by the **input impedance of the whole ladder**. Below ~1 Hz that would be the four series losses ($10^5$, −100 dB), but already at 10 Hz the series air masses dominate ($|Z_{in}| \approx 1.5\cdot10^6$ → −123 dB). The three peaks are the **minima of $Z_{in}$** (series resonances): holding the inlet at a fixed pressure means the network's natural frequencies are those of the ladder with a short-circuited ($p = 0$) inlet. The dips are where $U_{out}$ passes through zero between two poles, close to the maxima of $Z_{in}$. Above the last resonance the response falls about 60 dB/decade per chamber section (three L-C low-pass sections, −18 dB/octave each): −150 dB at 355 Hz → −254 dB at 1 kHz. The losses $R_A$ only round the peaks ($\omega M_{A3} = 4.7\cdot10^6 \gg 2.5\cdot10^4$ at 100 Hz, so $Q \approx 100$–200).

### b) Driven by a volume-velocity source, and the difference

![[part2b_volume_velocity_source_Uout.png]]
![[part2ab_source_comparison.png]]

> [!success] Answer 2b
> $|U_{out}/U_{in}|$ from `I(Vs7)` with I1 = 1 m³/s:
>
> | Feature | Frequency | Level (dB) |
> |---|---|---|
> | 10 Hz | – | +0.44 (→ 0 dB as $f \to 0$) |
> | **peak** | **47.3 Hz** | **+25.8** |
> | dip | 112.2 Hz | −5.2 |
> | **peak** | **175.8 Hz** | **+26.6** (shoulder at 190 Hz) |
> | 1 kHz | – | −111.5 |
>
> Transmission loss $TL = -20\log|U_{out}/U_{in}|$: 50 Hz −18 dB (amplification!) · 100 Hz +4.7 dB · 200 Hz −5.5 dB · 300 Hz +41 dB · 500 Hz +74 dB · 1 kHz +112 dB.
>
> **The differences.** An ideal volume-velocity source forces the flow into the inlet whatever pressure that takes. At low frequency the chambers cannot store flow ($1/\omega C_A$ is huge), so everything that goes in comes out: **0 dB transfer**, independent of the series masses and losses. The transfer $U_{out}/U_{in}$ is a property of the network alone; the source only decides *which* natural frequencies get excited. A volume-velocity source is an **open circuit** at the inlet, so its peaks sit at the open-inlet natural frequencies, the **maxima of $Z_{in}$** (47 and 176/190 Hz), exactly where the pressure-source response has its dips; the pressure-source peaks ($Z_{in}$ minima) do not appear at all. At those frequencies the ladder resonates and the silencer *amplifies* the flow by +26 dB. A real engine exhaust sits between the two ideal sources (finite source impedance), which is why silencer design has to know the source impedance. Above 200 Hz the chambers shunt the flow to ground and the following pipe mass blocks it: the same −18 dB/octave per section, 111 dB of transmission loss at 1 kHz (but see the validity warning). Only two clear peaks instead of three because the third open-inlet mode sits at 190 Hz, right beside 176 Hz, and only shows as a shoulder.

### c) Volume velocity in each pipe (U source)

![[part2c_pipe_volume_velocities.png]]

> [!success] Answer 2c
> | Pipe | Level at 1 kHz | Peaks / dips |
> |---|---|---|
> | 1 | 0 dB everywhere | it *is* the source current |
> | 3 | −30.2 dB | +8.7 dB (47 Hz), +19.9 dB (176 Hz), +22.0 dB (191 Hz); dip −22 dB at 51 Hz |
> | 5 | −78.7 dB | +24.9 dB (47 Hz), +18.5 dB (176 Hz), +14.2 dB (188 Hz); dip −39 dB at 150 Hz |
> | 7 | −111.5 dB | +25.8 dB (47 Hz), +26.6 dB (176 Hz) |
>
> `I(Vs1)` equals $U_{in}$ by definition, so pipe 1 is a flat 0 dB line. Each expansion chamber is an acoustic low-pass: chamber 2 shunts part of $U_1$ so $U_3 < U_1$, chamber 4 takes another bite, chamber 6 the last. At 1 kHz the cumulative attenuation is 30 → 79 → 112 dB after one, two and three chambers, i.e. each chamber section contributes 30–40 dB there. The dips in $U_3$ (51 Hz) and $U_5$ (150 Hz) are anti-resonances where the downstream part of the ladder presents a very high impedance, so almost no flow enters that pipe and the chamber before it takes it all. Pipe 7 has no dip because nothing follows it. The resonance peaks appear in every pipe but grow towards the outlet: energy stored in the resonating chambers is released into the pipe after them.

### d) Near-field pressure at the opening (radiation impedance included)

![[sch_Part2d_Silencer_Radiation.png]]
![[part2d_near_field_pressure.png]]

> [!success] Answer 2d
> The exit of pipe 7 is an unflanged tube end → "piston in a long tube" network from Lecture 3 §8b: $Z_{rad} = j\omega M_{A1} \,\|\, [R_{A2} + (R_{A1} \| C_{A1})]$ with the values in the table above, between `p_out` and ground. **Effective-length trap:** Table 2 gives *effective* lengths, which already contain the end-correction mass $0.6133a = 1.23$ mm of the open end, so pipe 7 is shortened to 38.77 mm when the radiation network is present — otherwise that mass is counted twice. (Keeping 40 mm and dropping $M_{A1}$ instead gives the same curves; the radiation load is ≥ 30× smaller than the pipe impedance everywhere in band.)
>
> | $f$ | $|p_{open}|$ for $U_{in} = 1$ m³/s |
> |---|---|
> | 10 Hz | 77.6 dB re 1 Pa (7.6 kPa) |
> | 100 Hz | 92.5 dB |
> | 1 kHz | 5.7 dB |
>
> The radiation impedance of a 2 mm tube end is essentially a **pure mass** in this band: $ka = 0.037$ at 1 kHz, so $Z_{rad} \approx j\omega M_{A1}$ with $M_{A1} = 115$ kg/m⁴ (at 1 kHz $|Z_{rad}| = 7.2\cdot10^5$, real part only 1.5 %). The dashed check curve $\omega M_{A1} |U_{out}|$ lies on top of the simulated $|p_{open}|$. So $p_{open} \approx j\omega M_{A1} U_{out}$: the pressure curve is the $U_{out}$ curve of b) tilted by +6 dB/octave, with the same peaks at 47 and 176 Hz and the same steep fall. The resistive part $R_{A2} = 3.2\cdot10^7$ is only reached far above the band ($ka = 1$ at 27 kHz). Inserting the radiation load changes $U_{out}$ by less than 0.01 dB: the silencer does not "see" the outside air, the ideal open end was a fine approximation.

### e) Pressure at 10 m and model validity

![[part2e_pressure_10m.png]]

> [!success] Answer 2e
> The pipe end radiates into free space as a point source ($4\pi$): $p(r) = j\omega\rho\, U_{out}\, e^{-jkr}/(4\pi r)$, so $|p| = \rho f |U_{out}|/(2r)$. Computed from `I(Vs7)` of the radiation sheet, plotted as SPL re 20 µPa for $U_{in} = 1$ m³/s (a realistic $10^{-3}$ m³/s is 60 dB lower, the shape is the same).
>
> | $f$ | SPL with silencer | Unsilenced ($U_{out} = U_{in}$) |
> |---|---|---|
> | 20 Hz | 97.3 dB | 95.4 dB |
> | 50 Hz | 121.6 dB | 103.4 dB |
> | 100 Hz | 104.7 dB | 109.4 dB |
> | 200 Hz | 120.9 dB | 115.4 dB |
> | 500 Hz | 49.9 dB | 123.4 dB |
> | 1 kHz | 17.9 dB | 129.4 dB |
>
> The far-field pressure of a monopole rises 6 dB/octave for constant $U$ (dashed reference), so the radiated SPL is the transfer of b) plus that tilt. The silencer helps only above about 230 Hz (≈ 75 dB at 500 Hz, 110 dB at 1 kHz) and **hurts by up to 18 dB at its two resonances** (47 and 176 Hz) when driven by an ideal volume-velocity source.

> [!warning] Validity of the silencer model at higher frequencies
> - **Lumped elements need $l < \lambda/10$.** Pipe 5 (100 mm) satisfies this only below **344 Hz**, pipe 3 and chamber 4 (80 mm) below 430 Hz, chamber 6 below 573 Hz, chamber 2 below 688 Hz, pipe 7 below 860 Hz, pipe 1 below 1.4 kHz. Above roughly 350–450 Hz the pipes and chambers must be treated as transmission lines (the ABCD two-port of Lecture 3 §4); the smooth −18 dB/octave-per-section roll-off then turns into a sequence of pass and stop bands (first half-wave resonance of the 100 mm pipe at $c/2l = 1.7$ kHz, of the 80 mm chamber at 2.15 kHz). The grey band in the figure marks this region: the 111 dB transmission loss at 1 kHz is not to be trusted.
> - Plane waves across the chamber radius are fine ($ka = 1$ at 2.7 kHz for the 20 mm chamber), so no transverse modes in band.
> - The point-source assumption for the 2 mm exit is excellent ($ka \ll 1$ to tens of kHz), and $r = 10$ m $\gg \lambda$ ($kr = 1.8$ at 10 Hz, 183 at 1 kHz), so we are in the far field except at the very lowest frequencies.
> - Free-space radiation ignores the car body and the road (a tailpipe under a car sees roughly a half space, +6 dB, plus reflections). $R_A = 25\cdot10^3$ is a crude constant, whereas viscous losses in a 2 mm pipe grow with $\sqrt{f}$. Rigid walls assumed. Hot exhaust gas has a different $\rho$ and $c$ than 20 °C air.

> [!tip] Doing Part 2 in LTspice for the quiz
> `V1 AC 1` for a), `I1 AC 1` for b)–e). Ground every chamber capacitor. Put a 0 V voltage source in series with each narrow pipe and plot `I(Vs7)` etc.; use dB (right-click the axis) with a wide dynamic range (−260 … +30 dB for a), 0 … −120 dB for b). For d) plot `V(p_out)`. For e) add the trace `2*pi*frequency*1.18*I(Vs7)/(4*pi*10)` (that is $|p|$ at 10 m in Pa; divide by 20e-6 and take dB for SPL). LTspice complains about an ideal current source in series with a capacitor at DC only if there is no DC path — the pipes' inductors provide one here, but a 100 MΩ across the source never hurts.

---

## Part 3 — Coupled mechanical–acoustic system

### Model

Part 1 circuit + for **each** diaphragm an acoustic sub-network (impedance analogy) representing the radiation impedance of a baffled piston seen by **both** faces, coupled to the velocity node with two voltage-controlled current sources (Lecture 4A slide 8, mobility form):

- **G_a** injects $U = S\,u$ into the acoustic node `p_i` / `p_o` (control = velocity node, output from ground into the p node). Gain = $S$.
- **G_m** draws the reaction force $f = S\,p$ out of the velocity node (control = p node, output from the u node to ground). Gain = $S$.
- Net effect on the mechanical side: an admittance $S^2 Z_A$ in parallel with the mass (mobility analogy) = the mechanical load $S^2 Z_A$.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american,scale=0.85,every node/.style={transform shape}]
\draw (0,0) node[ground]{} to[isource, l=$F$] (0,3) -- (1.5,3) node[circ]{} node[above]{$u$};
\draw (1.5,3) to[generic, l_=Part 1 net] (1.5,0) node[ground]{};
\draw (1.5,3) -- (4,3) to[cI, l=$G_m{=}S\,p$] (4,0) node[ground]{};
\draw (7,0) node[ground]{} to[cI, l_=$G_a{=}S\,u$] (7,3) -- (9,3) node[circ]{} node[above]{$p$};
\draw (9,3) to[L, l=$2M_{A1}$] (9,0) node[ground]{};
\draw (9,3) -- (11,3) to[R, l=$2R_{A2}$] (11,1.6) -- (11,1.2);
\draw (10.2,1.2) to[R, l_=$2R_{A1}$] (10.2,0) node[ground]{};
\draw (11.8,1.2) to[C, l=$C_{A1}/2$] (11.8,0) node[ground]{};
\draw (10.2,1.2) -- (11.8,1.2);
\end{circuitikz}
\end{document}
```

Radiation network per diaphragm (baffled piston, Lecture 3 §8b), both sides in series = every impedance ×2:

| | inner $S_i$ = 60 cm², $a$ = 43.7 mm | outer $S_o$ = 210 cm², $a$ = 81.8 mm |
|---|---|---|
| $M_{A1} = 8\rho/(3\pi^2 a)$, one side | 7.295 kg/m⁴ | 3.900 kg/m⁴ |
| $R_{A1} = 0.441\rho c/(\pi a^2)$ | 29 835 Pa·s/m³ | 8 524 |
| $R_{A2} = \rho c/(\pi a^2)$ | 67 653 Pa·s/m³ | 19 330 |
| $C_{A1} = 5.94 a^3/(\rho c^2)$ | 3.551e‑9 m⁵/N | 2.325e‑8 |
| SPICE, both sides: L = $2M_{A1}$ | L4 = 14.59 H | L5 = 7.799 H |
| R = $2R_{A2}$ (series from the p node) | R4 = 135.3 kΩ | R6 = 38.66 kΩ |
| R = $2R_{A1}$ (‖ C) | R5 = 59.67 kΩ | R7 = 17.05 kΩ |
| C = $C_{A1}/2$ | C3 = 1.775 nF | C4 = 11.62 nF |
| G gains | $S_i$ = 60e‑4 | $S_o$ = 210e‑4 |
| **added moving mass** $2S^2 M_{A1}$ | **0.525 g** | **3.44 g** |
| **HF radiation resistance** $2S^2 R_{A2}$ | **4.87 Ns/m** | **17.05 Ns/m** |
| $ka = 1$ at $f = c/(2\pi a)$ | **1253 Hz** | **670 Hz** |

Projects: `KiCad/Part3_Coupled_Stiff/`, `KiCad/Part3_Coupled_Soft/`.

> [!note] Sign check (the brief's hint: "pay attention to the signs and polarities of dependent generators")
> A radiation load must *load* the diaphragm, never feed it. Evidence the polarity is right: with air the resonance moves **down** (51.3 → 43.7 Hz; hand: $51.2\sqrt{11/(11+0.525+3.44)} = 43.9$ Hz ✓), the peak velocity **drops** (1.389 → 1.314 m/s per N), and the real part of $Z_M$ at 10 kHz rises from 0.74 to 22.8 Ns/m (= 0.72 + 4.87 + 17.05 = 22.6 ✓). A wrong sign raises the peak or makes the simulation blow up.

### a) Velocities and input impedance with the air load

![[part3a_velocities.png]]
![[part3a_impedance.png]]

> [!success] Answer 3a
> | Case | Feature | Part 1 (no air) | Part 3 (with air) |
> |---|---|---|---|
> | Stiff | resonance | 51.3 Hz, 1.389 m/s per N | **43.7 Hz, 1.314** |
> | Stiff | $|Z_M|$ minimum | 0.720 Ns/m | 0.761 |
> | Stiff | $Z_M$ at 10 kHz | 0.74 + j692 | **22.8 + j693** |
> | Soft | first resonance | 51.3 Hz, 1.388 | 43.7 Hz, 1.314 |
> | Soft | $u_{vc}$ dip / $|Z_M|$ maximum | 1288 Hz, 334 Ns/m | **1023 Hz, 129 Ns/m** |
> | Soft | second resonance ($u_{vc}$ peak, $|Z|$ min) | 1799 Hz, 0.0415, 24.1 Ns/m | **1718 Hz, 0.0264, 37.9 Ns/m** |
> | Soft | $u_d$ maximum | 1738 Hz, 0.0493 | 1549 Hz, 0.0257 |
> | Soft | $Z_M$ at 10 kHz | 5.7 + j372 | 10.6 + j372 |
>
> **Low frequency ($ka \ll 1$):** the radiation impedance is almost a pure mass ($j\omega M_{A1}$ dominates the parallel network). The air adds 0.5 g + 3.4 g of co-moving mass to the 11 g, so the resonance drops to 43.7 Hz for both links. The radiation resistance there is tiny ($\propto (ka)^2$), so the peak height barely changes; the drop from 1.389 to 1.314 is mostly the change of $Q$ from extra mass at fixed $R$.
>
> **Around $ka \approx 1$** (670 Hz outer, 1253 Hz inner) the network turns resistive. For the soft link the absorber frequency of the outer cone drops from 1288 to 1023 Hz (its mass grew from 5 to 8.4 g: $1/(2\pi\sqrt{8.44\,\text{g} \cdot 3\,\text{µm/N}}) = 1000$ Hz) and, more importantly, its 17 Ns/m of radiation resistance **damps the absorber**: the $u_{vc}$ dip is 8 dB shallower and the anti-resonance in $Z_M$ falls from 334 to 129 Ns/m. The second resonance is likewise lower and about 4 dB weaker.
>
> **High frequency ($ka \gg 1$):** the load is a pure resistance $\rho c S^2$ per side. Stiff: 21.9 Ns/m in series with the 11 g mass line, invisible in $|Z|$ (692 Ns/m reactive) but it *is* the whole radiated power. Soft: only the inner cone still moves, so only its 4.87 Ns/m shows up (10.6 = 5.7 + 4.9).
>
> **Effect of the radiation impedance in one sentence:** a frequency-dependent load that is extra mass at low frequency (lowers all resonances) and extra damping at high frequency (flattens the absorber anti-resonance and sets the radiated power); on the outer cone it is about 7× larger than on the inner one.

### b) Sound pressure in front of the diaphragms and the working principle

![[part3b_pressures.png]]
![[part3b_farfield_split.png]]

> [!success] Answer 3b
> Pressure in front of *one* face = `V(p_x)/2` (the p node carries the sum of both faces). Far field on axis at 1 m, half space (infinite baffle): $p = j\omega\rho\,(S_i u_{vc} + S_o u_d)/(2\pi \cdot 1\,\text{m})$, computed from the node voltages.
>
> | Case | Quantity | Value |
> |---|---|---|
> | both | $p_{front}$ inner / outer at the 44 Hz resonance | 15.9 / 29.8 Pa per N |
> | Stiff | $p_{front}$ plateau 100 Hz – 1 kHz, inner / outer | ≈ 3 / 5.6 Pa per N (10 / 15 dB) |
> | Stiff | $p_{front}$ at 10 kHz, both | 0.59 Pa per N |
> | Soft | $p_{front}$ inner: 2nd peak / 10 kHz | 10.0 Pa per N at 1738 Hz / 1.10 |
> | Soft | $p_{front}$ outer: 2nd peak / 10 kHz | 10.9 Pa per N at 1567 Hz / 0.03 |
> | both | far field, peak at 44 Hz | 1.85 Pa per N at 1 m |
> | Stiff | far field 100 Hz – 10 kHz | flat ≈ 0.35–0.46 Pa per N |
> | Soft | far field | 0.35 plateau, **+8 dB hump at 1.6 kHz** (0.87), −18 dB dip at ≈ 3 kHz (0.12), 0.18 at 10 kHz |
>
> **Near field.** Per face $p_{front} = Z_{rad}(f)\,S\,u$. Below $ka = 1$ the load is mass-like, so $p_{front} \approx \omega M_{A1} S u$, and with $u \propto 1/f$ above resonance that is a flat plateau; the outer face sits 5 dB above the inner because $M_{A1} S \propto a$. Above $ka = 1$ the load is the resistance $\rho c/S$, so $p_{front} \approx \rho c\,u$ for either face (same 0.59 Pa/N at 10 kHz in the stiff case) and it falls with the velocity.
>
> **Far field.** With constant force, $\omega\rho S u$ is flat in the mass-controlled region ($\omega \times 1/\omega$): the familiar flat loudspeaker response above resonance. **Stiff:** one 11 g piston, flat to 10 kHz in this lumped model (a real 210 cm² cone would break up; the model has no cone modes). **Soft, the dual-diaphragm principle:** up to ~1 kHz the outer cone supplies 78 % of the volume velocity ($S_o/(S_i + S_o)$). Around 1.6 kHz the link resonance boosts the output (+8 dB hump, the outer cone resonating on $C_{md}$). Above ~2 kHz the outer cone decouples, its velocity falls 12 dB/octave faster and it ends up in anti-phase, so around 3 kHz the two partially cancel (the dip). From ~4 kHz up only the inner cone radiates: −13 dB relative to the low-frequency plateau (= $20\log(60/270)$) but **flat**, extending the bandwidth far beyond where an 11 g, 210 cm² cone would have rolled off or broken up. Design intent: large area for bass efficiency, small light area for treble, and the soft joint is a *mechanical crossover*.

> [!warning] Model validity / assumptions in Part 3
> As the brief instructs: each diaphragm is loaded as an independent baffled piston (no mutual radiation impedance between the two, no dipole cancellation of the inner cone even though it sits in the throat of the outer one), and the total volume velocity is the plain sum $U_i + U_o$. Both overestimate the treble output somewhat. The lumped radiation network is itself a fit valid to $ka$ of a few, i.e. ~2–5 kHz for the outer cone. No cone break-up, no acoustic load on the rear that differs from the front (a real box would change the rear side).

> [!tip] Doing Part 3 in LTspice for the quiz
> Two `G` sources per diaphragm: `G_a` with input `u_vc`/0 and output into `p_i`, value `60e-4`; `G_m` with input `p_i`/0 and output from `u_vc` to 0, value `60e-4` (same for the outer cone with `210e-4`). Watch the output pin order: the G source pushes current from its + output pin *out* through the circuit and back into its − pin, so for the injector the − output pin sits on the p node. Build the two-sided radiation network as L ‖ [R + (R ‖ C)] with the doubled/halved values above. Plot `V(p_i)/2` and `V(p_o)/2` for the front pressures, and the far-field trace `2*pi*frequency*1.18*(60e-4*V(u_vc)+210e-4*V(u_d))/(2*pi*1)` for 1 m in the baffle half-space.

---

## Part 4 — Coupled electrical–mechanical system

### Model

The coil (mass $M_{mc}$, resistance $R_c$, inductance $L_e$) is driven by an ideal 1 V source. Its current makes the Lorentz force $f = Bl\,i$ on the coil; the coil velocity induces the back-EMF $v = Bl\,u_c$ in the loop. The coil is joined to the big mass $M_{m1}$ by $C_{ms} \| R_{ms}$, and $M_{m1}$ to ground by $C_{ms2} \| R_{ms2}$. Mobility analogy on the mechanical side, nodes `u_c` and `u_1`.

```tikz
\usepackage{circuitikz}
\begin{document}
\begin{circuitikz}[american,scale=0.85,every node/.style={transform shape}]
\draw (0,0) node[ground]{} to[V, l=$v$] (0,3) to[R, l=$R_c$, i=$i$] (2.5,3) to[L, l=$L_e$] (4.5,3)
   to[cV, l=$Bl\,u_c$] (4.5,0) node[ground]{};
\draw (7.5,0) node[ground]{} to[cI, l=$Bl\,i$] (7.5,3) -- (9,3) node[circ]{} node[above]{$u_c$};
\draw (9,3) to[C, l_=$M_{mc}$] (9,0) node[ground]{};
\draw (9,3) -- (10,3) to[L, l=$C_{ms}$] (12,3) -- (13,3) node[circ]{} node[above]{$u_1$};
\draw (10,3) -- (10,4.3) to[R, l=$1/R_{ms}$] (12,4.3) -- (12,3);
\draw (13,3) to[C, l_=$M_{m1}$] (13,0) node[ground]{};
\draw (14.5,3) to[L, l_=$C_{ms2}$] (14.5,0) node[ground]{};
\draw (16,3) to[R, l_=$1/R_{ms2}$] (16,0) node[ground]{};
\draw (13,3) -- (16,3);
\end{circuitikz}
\end{document}
```

| Ref | SPICE value | Physical |
|---|---|---|
| V1 | 1 V AC | ideal voltage drive |
| Vs1 | 0 V | current sensor, `I(Vs1)` = $i$ |
| R1 | 0.5 Ω | $R_c$ |
| L1 | 10 µH | $L_e$ |
| E1 | gain 1.5 | back-EMF, $Bl = 1\,\text{T} \cdot 1.5\,\text{m}$ |
| G1 | gain 3 | $f = Bl\,i = (Bl/R_c) \cdot V(R_c)$ (senses the voltage across $R_c$) |
| C1 | 5 mF | $M_{mc}$ = 5 g |
| L2 ‖ R2 | 10 µH ‖ 1 Ω | $C_{ms}$ = 0.01 mm/N, $1/R_{ms}$ |
| C2 ‖ L3 ‖ R3 | 100 mF ‖ 10 mH ‖ 10 Ω | $M_{m1}$ = 100 g, $C_{ms2}$ = 10 mm/N, $1/R_{ms2}$ |

Sweep `.ac dec 200 1 10k`. Project: `KiCad/Part4_Coil_Electromechanical/`. Workbook traces: `V(/u_c)`, `V(/u_1)`, `I(Vs1)`, `1/I(Vs1)` (= $Z_E$), `1.5*I(Vs1)/V(/u_c)` (= $Z_M$).

![[sch_Part4_Coil_Electromechanical.png]]

> [!note] Hand estimates
> - Electrical damping seen by the mechanics: $(Bl)^2/R_c = 4.5$ Ns/m — far larger than $R_{ms} = 1$ and $R_{ms2} = 0.1$.
> - Both masses riding together on $C_{ms2}$ ($C_{ms}$ is 1000× stiffer): $1/(2\pi\sqrt{0.105 \cdot 0.01}) = 4.91$ Hz.
> - Coil bouncing on $C_{ms}$ against $M_{m1}$, reduced mass $\mu = 4.76$ g: $1/(2\pi\sqrt{\mu C_{ms}}) = 729$ Hz (712 Hz with $M_{mc}$ alone).
> - $M_{m1}$ resonating on $C_{ms}$ with the coil held still (anti-resonance seen from the coil): $1/(2\pi\sqrt{0.1 \cdot 10^{-5}}) = 159$ Hz.
> - Electrical corner $R_c/(2\pi L_e) = 7.96$ kHz.

> [!note] Sign check on the back-EMF (from `sim/part4.py`)
> | E1 gain | max $|u_c|$ | at | $|Z_E|$ there |
> |---|---|---|---|
> | **+1.5 as drawn** | **0.652 m/s per V** | 4.9 Hz | 22.6 Ω |
> | 0 (no back-EMF) | 29.5 m/s per V | 4.9 Hz | 0.50 Ω |
> | −1.5 (flipped) | 0.889 m/s per V | 724 Hz (the 4.9 Hz peak vanishes, the 724 Hz one grows: negative damping) | 1.47 Ω |
>
> With the polarity as drawn the electrical damping cuts the 4.9 Hz velocity peak by a factor 45 and the current at resonance drops from 2 A to 44 mA: the back-EMF opposes the drive, which is the physically correct sign. Power check: $v \cdot i = Bl\,u_c\,i$ into E1 equals $f \cdot u_c = Bl\,i\,u_c$ out of G1, so the transducer is lossless as it must be.

### a) Velocities of the coil and of $M_{m1}$

![[part4a_velocities.png]]

> [!success] Answer 4a
> | | $u_c$ (coil) | $u_1$ (mass) |
> |---|---|---|
> | 1 Hz | 0.188 m/s per V | 0.188 |
> | **peak** | **4.90 Hz, 0.652** | **4.90 Hz, 0.652** |
> | dip | **158.5 Hz, 4.3e‑4** | 436.5 Hz, 0.0158 |
> | **peak** | **732.8 Hz, 0.537** | 716 Hz, 0.0272 |
> | 10 kHz | 6.0e‑3 | 1.8e‑6 |
>
> **4.9 Hz, rigid-body mode.** $C_{ms}$ is 1000× stiffer than $C_{ms2}$, so at low frequency coil and mass move as one 105 g lump on the soft suspension: both velocities are equal and in phase. The peak is broad because the electrical damping of 4.5 Ns/m dominates ($Q \approx 0.7$); with the back-EMF removed the same mode is damped only by $R_{ms2}$ and peaks at 29.5 m/s per V. Below the first resonance the motion is compliance-controlled (+90°), between the resonances mass-controlled (−90°).
>
> **158.5 Hz, the coil stops.** Anti-resonance of the mechanical load: $M_{m1}$ on the stiff spring $C_{ms}$ resonates (159 Hz estimate) and presents an almost infinite impedance to the coil, so $u_c$ drops to $4\cdot10^{-4}$ m/s while $u_1$ keeps moving (ratio ~40 right at 158 Hz). A vibration-absorber (tuned-mass-damper) effect; the phase of $u_c$ jumps by 180°.
>
> **733 Hz, coil-on-spring mode.** The 5 g coil bounces on $C_{ms}$ against the heavy, now practically stationary mass (729 Hz reduced-mass estimate). $u_c$ peaks at 0.54 m/s per V; $u_1$ shows only a small hump and then falls at −40 dB/decade because the spring $C_{ms}$ cannot transmit the force to $M_{m1}$ at high frequency (mass isolation). Above 733 Hz $u_c$ falls as $1/(\omega M_{mc})$; above 8 kHz $L_e$ also limits the current. The shallow minimum of $u_1$ at 436 Hz is a zero of the $u_1$ transfer function (spring force against the suspension branch), not a system resonance.

### b) Mechanical input impedance seen by the electromagnetic force

![[part4b_mechanical_impedance.png]]

> [!success] Answer 4b
> $Z_M = f/u_c = Bl \cdot I(Vs1)/V(u_c)$.
>
> | Feature | $f$ | $|Z_M|$ [Ns/m] | Phase |
> |---|---|---|---|
> | 1 Hz | – | 15.2 | −90° (compliance $C_{ms2}$) |
> | **resonance (minimum)** | **4.90 Hz** | **0.10 ≈ $R_{ms2}$** | 0° |
> | **anti-resonance (maximum)** | **158.5 Hz** | **6.9e3** | 0° (flip +90 → −90) |
> | **resonance (minimum)** | **732.8 Hz** | **1.13 ≈ $R_{ms}$** | 0° |
> | 10 kHz | – | 313 ≈ $\omega M_{mc}$ = 314 | +90° (coil mass) |
>
> This is the impedance of the pure mechanical network: the transducer is lossless, so $Z_M$ does **not** contain the electrical damping (the back-EMF acts on the electrical side). Minima are where the force meets almost no impedance, only the dampers: the two resonances, and the damper values can be read straight off the plot (0.1 and 1 Ns/m). The maximum is the anti-resonance where $M_{m1}$ on $C_{ms}$ takes all the force and the coil cannot move. Phase sequence −90° / +90° / −90° / +90°: compliance-like below 4.9 Hz ($C_{ms2}$), mass-like between 4.9 and 158 Hz (the 105 g lump), compliance-like between 158 and 733 Hz ($C_{ms}$, the coil is spring-controlled), mass-like above ($M_{mc}$).

### c) Electrical input impedance of the complete system

![[part4c_electrical_impedance.png]]
![[part4_overview.png]]

> [!success] Answer 4c
> $Z_E = V_1/I(Vs1) = 1/I(Vs1)$.
>
> | Feature | $f$ | $|Z_E|$ |
> |---|---|---|
> | 1 Hz | – | 0.522 Ω |
> | **peak** | **4.90 Hz** | **22.6 Ω** (motional part 22.1 Ω) |
> | broad minimum | ~100–400 Hz | 0.500 Ω = $R_c$ |
> | **peak** | **732.8 Hz** | **2.48 Ω** (motional 1.98 Ω) |
> | dip | 1.4 kHz | 0.5025 Ω |
> | 10 kHz | – | 0.797 Ω ≈ $|R_c + j\omega L_e|$ = 0.803 |
>
> $Z_E = R_c + j\omega L_e + (Bl)^2/Z_M$. The motional term is the **inverse** of the mechanical impedance (Lecture 4 "impedance conversion": $Z_{E,M} = (Bl)^2 Y_M$). So the mechanical **resonances** ($Z_M$ minima) appear as **peaks** in $|Z_E|$: $(Bl)^2/R_{ms2} = 22.5$ Ω at 4.9 Hz and $(Bl)^2/1.13 = 2.0$ Ω at 733 Hz on top of $R_c$. The mechanical **anti-resonance** ($Z_M$ maximum, 158 Hz) is where $Z_E$ is closest to $R_c$ ($(Bl)^2/6.9\cdot10^3 = 0.3$ mΩ): the coil is blocked, there is no back-EMF, and the electrical side sees the blocked-coil impedance. The $Z_E$ peaks are sharp because on the electrical side the mechanical resonance is loaded only by the mechanical dampers ($Q \approx 32$ for the first mode). The phase swings about ±75° around each peak: inductive below a resonance, capacitive above, the classic loudspeaker impedance curve (a motional impedance looks like a parallel RLC on the electrical side). Above ~1.4 kHz the motional term is negligible and $Z_E$ follows $R_c + j\omega L_e$ with the corner at 8 kHz.
>
> **Difference between the impedance plots:** $Z_M$ and $Z_E$ are mirror images on a log scale, every minimum of one is a maximum of the other, scaled by $(Bl)^2 = 2.25$. That is the whole content of "mechanical → electrical impedance is an inversion".

### d) Every resonance and anti-resonance explained

> [!success] Answer 4d
> | $f$ | $u_c$ | $u_1$ | $Z_M$ | $Z_E$ | Physical origin |
> |---|---|---|---|---|---|
> | 4.9 Hz | peak 0.65 | peak 0.65 | min 0.10 (≈ $R_{ms2}$) | peak 22.6 Ω | both masses (105 g) on the soft suspension $C_{ms2}$; rigid-body mode, damped mostly by $(Bl)^2/R_c$ |
> | 158.5 Hz | **dip 4e‑4**, coil stands still | still moving | **max 6.9e3** | ≈ $R_c$ (0.500 Ω) | $M_{m1}$ resonating on the stiff spring $C_{ms}$ absorbs the force: anti-resonance, tuned-mass-damper effect |
> | 436 Hz | – | shallow dip | – | – | zero of the $u_1$ transfer (spring force vs suspension branch), not a system mode |
> | 733 Hz | peak 0.54 | small hump 0.027 | min 1.13 (≈ $R_{ms}$) | peak 2.5 Ω | 5 g coil bouncing on $C_{ms}$ against the nearly stationary $M_{m1}$ (reduced mass 4.76 g → 729 Hz) |
> | 8 kHz | roll-off steepens | – | – | inductive rise | electrical corner $R_c/(2\pi L_e)$: $L_e$ limits the current; no mechanical origin |
>
> Forces vs current (Problem 4.3e in [[Lecture 4 - Analogies - Transducers & Dynamic Microphones]]): the coil force is always $f = Bl\,i$; the force in the spring $C_{ms}$ is $f - j\omega M_{mc} u_c$, which is ≈ $f$ below 158 Hz (the coil mass is negligible) and → 0 above 733 Hz (the coil mass takes the whole force).

> [!warning] Model validity / assumptions in Part 4
> Linear, small-signal: $Bl$ constant (no coil leaving the gap), no eddy-current losses or frequency-dependent $L_e$, no acoustic load on the coil or masses, ideal voltage source with zero output impedance. Peak frequencies are read from a 200-points-per-decade sweep (±0.5 %). The lab allows either analogy; the mobility analogy was used, an impedance-analogy version would use H and F sources instead of E and G and gives identical plots.

> [!tip] Doing Part 4 in LTspice for the quiz
> Electrical loop: `V1 AC 1` → `R1 0.5` → `L1 10u` → `E1` (value `1.5`, input pins on `u_c` and 0) → 0. Add a 0 V source `Vs1` in the loop for the current. Force: `G1` value `3` with input pins across `R1` (+ upstream), output from 0 into `u_c` — or use an `F` source with the current of `Vs1` and gain 1.5, which is what the lecture's table calls the "through ↔ through" element. Plot `V(u_c)`, `V(u_1)`; add traces `1/I(Vs1)` for $Z_E$ and `1.5*I(Vs1)/V(u_c)` for $Z_M$. Check the sign: the 5 Hz peak must be *small* (≈ 0.65 m/s per V); if it is ~30 m/s the back-EMF is the wrong way round.

---

> [!note] KiCad/ngspice gotchas learned in this lab (for next time)
> - **Controlled sources need their Sim fields on the instance.** `GSOURCE`/`ESOURCE` placed by script carry no `Sim.*` properties; write `Sim.Device = SPICE`, `Sim.Params = type=\"G\" model=\"<gain>\"` with the **backslash-escaped quotes**, otherwise the file fails to load.
> - **Current direction:** the export is `G1 N+ N- C+ C- gain`, and the current flows from N+ *through the source* to N−. To inject into a node put N− on the node; to draw from a node put N+ on it.
> - **DC operating point:** an ideal current source into a bare L/C branch has no `.op` solution; a 100 MΩ leak (1 TΩ where a capacitor is loaded below 100 Hz) fixes it without touching the AC result.
> - **Effective length vs radiation mass:** effective lengths already contain the end correction; adding a radiation network with $M_{A1}$ on top double-counts it, so shorten the last pipe by $0.6133a$ (unflanged) or $0.85a$ (flanged).
> - **Currents in AC sweeps:** ngspice does not save inductor currents by default; a 0 V voltage source in series (`Vs…`) gives `I(Vs…)` in KiCad and in batch runs.
> - `.include` in a batch deck chokes on paths with spaces; the run scripts copy the netlist to a temp dir first.
> - Projects: `5. Semester/Electroacoustics/Labs/Lab A/KiCad/{Part1_DualDiaphragm_Stiff, Part1_DualDiaphragm_Soft, Part2a_Silencer_PressureSource, Part2b_Silencer_VolumeVelocitySource, Part2d_Silencer_Radiation, Part3_Coupled_Stiff, Part3_Coupled_Soft, Part4_Coil_Electromechanical}/`. Scripts: `.../sim/part1.py … part4.py` (each rebuilds the schematic, exports, runs, plots). Numbers: `.../results/part1.md … part4.md`. LaTeX: `.../report/LabA_report.tex` → `Lab A - Report (KiCad-ngspice).pdf` here.

## Quiz checklist (20 Sep)

Every plot must have **distinguishable curves, labelled axes with units, the relevant frequency range and the relevant dynamic range**; every circuit must have **readable element names**, and element values listed as text when asked. Concise written answers, limited to the question.

- [ ] Part 1a: $u_{vc}$, $u_d$ vs $f$ (10 Hz – 10 kHz, m/s per N, dB or log), stiff and soft on one plot, with the 51 Hz / 1288 Hz / 1799 Hz features called out.
- [ ] Part 1b: $|Z_M|$ and phase (`1/V(u_vc)`), both cases; name the compliance line, resistive floor 0.72 Ns/m, mass lines 11 g and 6 g, anti-resonance 334 Ns/m.
- [ ] Part 2a/b: $U_{out}$ for p-source (dB, −260 … −90) and U-source (dB, −120 … +30); explain short-circuit vs open-circuit natural frequencies.
- [ ] Part 2c: $I(Vs1), I(Vs3), I(Vs5), I(Vs7)$ on one plot, 10 – 1000 Hz.
- [ ] Part 2d: $p_{out}$ with the radiation network, note $\approx j\omega M_{A1} U_{out}$ and the effective-length choice.
- [ ] Part 2e: SPL at 10 m, plus the $l < \lambda/10$ limit (344 Hz for the 100 mm pipe).
- [ ] Part 3a: overlay Part 1 vs Part 3 velocities and $Z_M$; quote 51.3 → 43.7 Hz, added masses 0.5 g / 3.4 g, radiation resistances 4.9 / 17 Ns/m.
- [ ] Part 3b: $p_{front}$ inner/outer, plus the far-field sum; one paragraph on the mechanical-crossover principle.
- [ ] Part 4a/b/c: $u_c$, $u_1$; $Z_M$; $Z_E$ (1 Hz – 10 kHz); 4d table of 4.9 / 158.5 / 733 Hz / 8 kHz with origins; mention the sign check on the back-EMF.
- [ ] Circuits: one screenshot per part with element names and values, controlled-source gains stated ($S$ in m², $Bl$, $Bl/R_c$).
