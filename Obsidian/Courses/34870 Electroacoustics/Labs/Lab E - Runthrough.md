---
course: "34870"
course-name: "Electroacoustics"
type: lab-note
date: 2026-10-20
lab: E
topic: "Lab E — measured: baffle diffraction, piston directivity, System D in the anechoic chamber"
tags: [Electroacoustics, lab-note, loudspeakers, diffraction, baffle, directivity, crossover]
---

# Lab E: what we measured, and what it means

> [!info] The day
> **Tue 20 Oct 2026, 08:30**, large anechoic chamber (rooms 028/025, building 354). **Group 10:** Louis Andrianne, Sophie Kimura, Mads. **System D**, UMIK **708-0332**, sound card.
> **Preparation:** [[Lab E - Preparation]] · **Quiz (D + E):** [[Lab DE - Quiz model answers]], due **Mon 26 Oct** · **Interactive:** [The Analogy Bench, Lab E](https://study.madsrudolph.dev/34870/#labE)
> **Files:** labs repo `Lab E/data/labE_<tag>.mat` (shared); `Lab E/matlab/plot_labE.m` → `Lab E/figures/` (local only, as for Lab D: the group does its own analysis).

## What is in the data

| Tag | What | Settings |
|---|---|---|
| `box_0`, `box_30` | 3″ driver in its small box | 24/oct, Nav 16 |
| `circle_0`, `circle_30` | circular screen, a = **0.30 m**, driver centred | same |
| `iec_0/15/30/60` | IEC screen **0.51 × 0.71 m**, driver 0.205 m from the left, 0.44 m from the bottom | same |
| `system_0`, `system_30` | System D, vent plugged, woofer → midrange → tweeter in **one** run | 48/oct, Nav 64, Nmeas 3 |
| `system_30_bad` | a rejected 30° run (up to 31 dB off): ignore it | |

- **Microphone:** 2.44 m from the speaker in both parts, 1.15 m above the platform in part 2. T = 20 °C, so c = 343.2 m/s.
- **System layout:** mid/tweeter box at `xrel_mid = 0.12, yrel_mid = 0.29` on the woofer box. Dust cover **off**.
- **Not measured:** `system_60`, and the midrange and tweeter diameters. The 3″ driver's diameter is the rule of thumb (a = 3 cm).
- **Above 18.4 kHz** the UMIK channel jumps by about 20 dB in every run, so every plot stops at 18 kHz.

---

## Part 1: one driver, three mountings

![[labE_mountings.png]]

**The small box** is the odd one out. From 250 to 600 Hz it sits **5.7 dB below** the two screens, and above 3 kHz it is level with them (−0.3 dB). That is the **baffle step**: the box's front is so small that at low frequency the driver radiates into full space (4π). A big screen gives it half space (2π) and twice the pressure. It is also the smoothest curve (6 dB peak to peak, 300 Hz – 5 kHz), because its edges are close and the ripple sits higher up and smaller.

**The circular screen** has the worst ripple: **17 dB peak to peak**. With the driver in the centre, every edge point is the same distance away, so all the inverted edge waves arrive together.

$$\Delta = a + \sqrt{a^2 + r^2} - r = 0.30 + \sqrt{0.30^2 + 2.44^2} - 2.44 = 0.318\ \text{m}$$

| | Formula | Measured (circle, 0°) |
|---|---|---|
| first peak, Δ = λ/2 | 539 Hz | broad, 400–600 Hz (the driver's own response sits on top) |
| first dip, Δ = λ | **1078 Hz** | **1059 Hz, −7.6 dB** |
| second peak, Δ = 3λ/2 | 1617 Hz | 1679 Hz |
| second dip, Δ = 2λ | 2156 Hz | 2115 Hz |

**The IEC screen** (driver off-centre) has the edges spread between 0.20 and 0.44 m from the driver, so the edge waves arrive at different times and largely cancel each other out: 10 dB peak to peak, with no deep dips.

**At 30°** the circle's edge points are no longer equidistant from the microphone, and the ripple smears out (bottom panel). The three mountings then lie within a few dB of each other above 1 kHz.

### diffrac.m against the measurement

![[labE_circle_diffrac.png]]

- The measured curve contains the driver's own response (its roll-off below ~200 Hz and its peak near 11 kHz), and `diffrac` does not. So the top two panels are shifted to the model's level over 300 Hz – 5 kHz.
- **The point source** keeps rippling at full strength up to 20 kHz. **The 30 mm piston** damps the high-frequency ripple, because a piston sends less sound sideways along the baffle once ka > 1. The measurement follows the piston.
- **The bottom panel is the cleanest test:** circle minus IEC, measured and modelled. The driver is the same in both, so it **drops out completely**, and only the two baffles are left. The dips at 1029 and 2115 Hz and the ripples up to 5 kHz are on top of `diffrac` within about 1 dB.

### IEC screen: directivity

![[labE_iec_directivity.png]]

Dividing each off-axis curve by the 0° curve removes the baffle and the driver, and leaves the beaming.

| Angle | Piston a = 30 mm: −3 dB / null | Measured: −3 dB / null |
|---|---|---|
| 30° | 5.9 kHz / 14.0 kHz | 5.2 kHz / 10.9 kHz (−17 dB) |
| 60° | 3.4 kHz / 8.1 kHz | **3.45 kHz / 7.96 kHz (−38 dB)** |

- At **60°** the rigid piston is spot on.
- At 15° and 30° the measured nulls come earlier than the piston's: the 30° null implies a ≈ 38 mm, and the 15° dip at 13 kHz has no piston null at all. Up there the 3″ cone no longer moves as one piece (break-up), and the bump in the driver's own response near 11 kHz is part of that.
- The +3 dB around 1.1 kHz in all three ratios is the IEC screen's own on-axis dip, which the off-axis curves don't share.

---

## Part 2: System D

![[labE_system.png]]

**Levels** (0°, dB re 1 Pa/V at 2.44 m):

| Unit | 150–600 Hz | 1–3 kHz | 3–8 kHz | 30° minus 0°, 3–8 kHz |
|---|---|---|---|---|
| woofer (Scan-Speak 26W/8534G00) | **7.7** | 4.7 | 6.7 | **−15.6 dB** |
| midrange (DALI) | 2.8 | 3.3 | 0.2 | −7.5 dB |
| tweeter (DALI) | −19.8 | **12.4** | 11.1 | −0.7 dB |

- **The woofer** is the most sensitive unit at low frequency, about 5 dB above the midrange. It runs out to 3 kHz on axis with break-up peaks at 2.5–3 kHz, but **off axis it is gone above 3 kHz** (−15.6 dB at 30°). A 21 cm piston has ka = 1 at 520 Hz and reaches −3 dB at 30° near 1.7 kHz. It must hand over well below that.
- **The midrange** is the DALI bookshelf's own bass/mid driver. It is flat from 120 Hz to about 4 kHz (±2 dB) and keeps going to 12 kHz on axis. At 30° it loses 7.5 dB in the 3–8 kHz band.
- **The tweeter** is about **9 dB louder** than the midrange in its band and barely beams at all (−0.7 dB at 30°). It is 6 dB down from its band level at 1.04 kHz, just under its resonance (the Lab D impedance peaks at **1.45 kHz**, only 6.7 Ω, so it is well damped). It crosses the woofer and the midrange near **930–960 Hz**, but crossing that low would drive the tweeter at its resonance. A crossover around 2.5–3 kHz keeps it a good octave clear, and that is still below where the midrange starts to beam.
- **Below 100 Hz** the tweeter curve is only noise, and the woofer's low end is the chamber, not the woofer: the vent was plugged and the room isn't anechoic that low.

**Phase.** One compensation distance for all three units, found as the d that makes the three phases smoothest, comes out at **d = −1.15 m**. It is negative because the sound card's random delay in this run was shorter than the flight time: d is "flight time plus card delay", and the card delay can have either sign relative to the start. The relative phase doesn't even need d: within one run, `angle(H_a./H_b)` cancels every common delay.

| f | woofer − midrange | tweeter − midrange |
|---|---|---|
| 300 Hz | −12° | +163° |
| 1 kHz | −36° | +162° |
| 2 kHz | −58° | +97° |
| 3 kHz | −54° | +76° |

- **Woofer and midrange are close to in phase** at the low end and drift apart slowly. The woofer's acoustic centre sits a little further back.
- **The tweeter is nearly inverted** relative to the midrange below 1 kHz (a second-order high-pass gives +180° well below its resonance) and comes round to +76° at 3 kHz. So the crossover's own phase shifts and the drivers' polarity have to be chosen against this curve, not assumed.

---

## Differences and why (for the quiz)

| Observation | Cause |
|---|---|
| box 5.7 dB below the screens at 250–600 Hz | baffle step: full-space radiation from a small front |
| circle dips at 1.06 and 2.1 kHz | edge waves Δ = λ and 2λ behind the direct wave, all in step |
| IEC curve smooth, circle not | edge distances spread (0.20–0.44 m) vs all equal (0.30 m) |
| circle at 30° smoother than at 0° | edge points no longer equidistant from the mic |
| piston fits at 60°, not at 15–30° above 10 kHz | cone break-up: not a rigid piston up there |
| woofer −15.6 dB at 30° above 3 kHz | a 21 cm piston beams (ka ≈ 6 at 3 kHz) |
| tweeter ~9 dB hotter than the midrange | higher sensitivity: the crossover needs an L-pad / attenuation |
| d = −1.15 m, not +2.44 m | the sound card's random delay is part of the "distance" |

## Open points

- [ ] The midrange and tweeter diameters were not measured. Read them off the DALI box or the Spektor 2 spec before the project.
- [ ] `system_60` is missing. 0° and 30° are enough for the quiz and the crossover; mention it if the 60° directivity is asked for.
