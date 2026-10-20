---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: lab-preparation
date: 2026-10-20
tags: [Acoustics, lab, room-modes, reverberation, sound-power]
---
# Lab Exercise — Room Modes, Reverberation Time and Sound Power

> [!abstract] The idea
> A small hard room has a few low modes you can find by ear. Measure how quickly it forgets a sound (T20/T30), and the room becomes a calibrated meter for sound power.

Source: [[34840_Laboratory exercise 2026.pdf|lab guide (7 pages)]]. Theory: [[Lecture 6 - Room Modes and the Diffuse Sound Field]] (modes, Sabine, steady-state level) and [[Lecture 7 - Sound Absorption and Room Acoustic Design]] (absorbers, diffusers). Course text sections 1.3, 1.5, 2.5, 3.1 and 3.2. Read-first primer (for the missed lectures 5–7): [34840 Lab Exercise — Understanding Guide](https://claude.ai/code/artifact/d20e9009-902f-49d2-a238-c0af3ae92c56). Interactive: [Room Lab Explorer](https://claude.ai/artifact/4AmSYVRxKxJN2KccXtqXEq) and [Sound Bench, lab section](https://study.madsrudolph.dev/34840/#lab). MATLAB: `5. Semester/Acoustics and Noise Control/Lab/lab_prep.m` (preparation) and `lab_soundpower.m` (part C processing).

## 0. Logistics

| | |
|---|---|
| **Our slot** | **Wed 28-Oct-2026, 13:00**, with Joan Escandell Martin (s261552) and Louis Andrianne (s253472). The sheet row was still grey (not yet confirmed by the instructor) on 20-Oct. **Report due Wed 11-Nov-2026.** File name: `34840_ex_s246132_s253472_s261552.pdf` |
| Format | Groups of **3**, about 2 hours, one group report |
| Sign-up | The online sheet `34840_LabExercise schedule_2026.xlsx`, linked from the Learn assignment *Labexercise (group handin)*. Choose a slot that is missing students; it turns green when 3 people have signed up. |
| When | Lab slots fall in the weeks of lectures 8–11 (27-Oct to 17-Nov) |
| Where | Meet at the databar in **building 352**, in front of room 005 on the ground floor |
| Instructor | Stefan Graham (stgra@dtu.dk) manages the slots. If you cannot come, tell him and Finn Agerkvist (ftag@dtu.dk). |
| Report | **2 weeks after** your lab day; at most **10 pages**, all names and study numbers on the front page. Submit on Learn as `34840_ex_s111111_s222222_s333333.pdf`. Hand-in and lab together count 10 % of the grade. |
| Bring | (ii) a music track, connected by mini-jack. (iii) A **sound level meter app** on your phone, e.g. Sound Analyzer for Android or Decibel X / NIOSH SLM on iPhone. Install it **before** the lab. |

> [!warning] 34870 clash
> 34870 labs run on Tuesday mornings too. Pick a 34840 slot that avoids the 34870 Lab E follow-ups and the project lab sessions.

## 1. Preparation (i) — the five lowest eigenfrequencies

Room 4.38 × 3.13 × 3.29 m (x = length, y = width, **z = height**). Height > width, so the first z-mode comes **before** the first y-mode.

$$f_{n_x n_y n_z}=\frac c2\sqrt{\left(\frac{n_x}{L_x}\right)^2+\left(\frac{n_y}{L_y}\right)^2+\left(\frac{n_z}{L_z}\right)^2},\qquad c=331.3+0.606\,\vartheta\ \mathrm{m/s}$$

At 20 °C (c = 343.4 m/s):

| # | Mode $(n_x,n_y,n_z)$ | Type | $f$ (Hz) | Pressure minima to find |
|---|---|---|---|---|
| 1 | (1,0,0) | axial | **39.2** | 1 along the length (mid-room); none across the width or up the height |
| 2 | (0,0,1) | axial | **52.2** | 1 halfway up: the floor and ceiling are loud, mid-height is quiet |
| 3 | (0,1,0) | axial | **54.9** | 1 across the width |
| 4 | (1,0,1) | tangential | **65.3** | 1 along the length and 1 up the height |
| 5 | (1,1,0) | tangential | **67.4** | 1 along the length and 1 across the width |
| (6) | (0,1,1) | tangential | 75.7 | spare in case one of the five is hard to find |
| (7) | (2,0,0) | axial | 78.4 | 2 along the length |

- **Temperature:** each kelvin moves every mode by about +0.17 %, i.e. +0.07 Hz at 39 Hz and +0.12 Hz at 67 Hz. Read the room thermometer, or ask, and recompute with that c.
- **Two close pairs:** 52.2/54.9 Hz and 65.3/67.4 Hz are only 2–3 Hz apart. Sweep slowly in steps of about 0.2 Hz around them. The minima pattern tells you which is which: (0,0,1) changes with height, (0,1,0) changes across the width.
- **Schroeder frequency:** V = 45.1 m³. With an empty-room T of a few seconds, $f_S=2000\sqrt{T/V}$ lies at about 400–950 Hz. Below that individual modes dominate, so a 125 Hz octave holds only a handful of modes and the 125 Hz T scatters from position to position.

## 2. Part A — finding the modes (lab day)

**Setup:** generator at 100 mV, loudspeaker gain at 13 o'clock, loudspeaker in the corner near the power sockets.

1. Sweep the generator from 30 Hz up. Mark each frequency where the level peaks, judged by ear in a corner or on the phone app's broadband level.
2. For each peak, walk along the walls with the app and count the minima in x, y and z. The counts give $n_x,n_y,n_z$ directly.
3. Fill in the data sheet (§6).

> [!question] Why corners? (the guide asks you to explain this)
> At a rigid wall, the particle velocity normal to the wall is zero, so for every mode the pressure has a **maximum** there ($\cos(n\pi x/L)=\pm1$ at $x=0$ and $x=L$). A corner is at a pressure maximum in all three directions at once, so **every** mode has a pressure antinode there. A source in a corner excites every mode, because a monopole couples to the pressure, and a microphone or ear in a corner hears every mode. In the middle of the room, every mode with an odd index has a node and disappears.

## 3. Part B — reverberation time (interrupted pink noise)

**Setup:** loudspeaker on the green wall cable at 13 o'clock. GRAS 46AC at 12.5 mV/Pa into the 12AA amplifier at **20 dB**, so the script needs `M = 12.5e-3*10`. **Check this line before the first run.**

**Four room conditions:** empty → 6 absorbers on the wall opposite the door → absorbers + 6 diffusers → diffusers only. In each condition, play the music first and write down what you hear: flutter, boominess, clarity, envelopment.

### Choosing the script's times (empty room, T up to about 10 s)

| Parameter | Meaning | Rule | Empty room | With absorbers |
|---|---|---|---|---|
| `T_build_up` | source on before the cut | ≥ the expected $T_{60}$, so the level is stationary | about 8–10 s | about 2–3 s |
| `T_silence` | decay recording | ≥ $T_{60}$ at the lowest band, or the −35 dB point for T30 is never reached | about 10–12 s | about 3–4 s |
| `T_bgn` | background-noise averaging | long enough for a stable noise floor | 10–16 s | 10 s |
| `Navg` / `Npos` | decays per position / positions | the guide says 5 decays at each of 3 positions | 1 / 1 for the first test | 5 / 3 |

First run a **single position with a single decay** in the empty room and save it. Later, compare it with the 5 × 3 average. The average is much smoother, which is the whole reason for ensemble averaging: a single noise decay fluctuates by several dB.

### T20 versus T30

- **T20** = 3 × the time to fall from −5 to −25 dB. **T30** = 2 × the time from −5 to −35 dB. Both extrapolate to 60 dB.
- They agree if the decay is a single straight line in dB.
- **T30 > T20:** the decay is double-sloped, with a slow tail. In this room that comes from long-lived axial and flutter paths between the two parallel hard surfaces that don't hold the absorbers, especially once all the absorption is on one wall (a non-diffuse field). Diffusers should reduce the difference.
- **T30 cannot be trusted** if the SNR is below about 45 dB (−35 dB plus a 10 dB margin). The −35 dB point then lies in the noise floor, which flattens the tail and makes T30 too long. In that band, use T20; it needs only about 35 dB of SNR.
- **Decide for part C:** use T20 in any band with marginal SNR (typically 125 Hz and 4 kHz), otherwise T30, and state the choice in the report.

> [!question] What does a "healthy" decay look like?
> - **Level:** a clear stationary level before the cut.
> - **Decay:** a decay that is straight in dB over at least 20–30 dB.
> - **Floor:** it ends in a flat noise floor at least 10 dB below the evaluation range.
> - **No glitches:** no clipping, i.e. waveform peaks not flattened at the card's limit. Lower the gain if they are.
> - **No disturbances:** no bumps from someone talking or a door slamming.
> - **Low bands:** at 125 Hz some beating between modes is normal. A strongly curved or wavy decay means a single position is unreliable.

> [!question] Where do diffusers work best?
> With all the absorbers on one wall, sound bouncing between the **side walls** and between **floor and ceiling** never touches them, so those flutter paths decay at the slow empty-room rate. Put the diffusers on those hard parallel pairs, where the mirror paths hit, not next to the absorbers. Their job is to scatter that trapped energy *towards* the absorbing wall. Spread them out, and keep them away from the microphone positions so the mic stays in the far, diffuse field.

### Expected trend

| Condition | Expect | Why |
|---|---|---|
| Empty | longest T, up to about 10 s at low frequency; T30 ≈ T20 | almost no absorption, ᾱ ≈ 0.01 |
| + absorbers on one wall | T drops strongly at mid and high frequencies, much less at 125 Hz; often T30 > T20 | porous absorbers fail below the λ/4 limit; all absorption on one surface gives a non-diffuse field |
| + absorbers + diffusers | T drops further; T20 and T30 closer together | scattering sends the grazing and axial energy into the absorbers |
| Diffusers only | close to empty, slightly shorter | diffusers barely absorb, only the edges and the material |

Sabine sanity check: $A=0.161V/T$, $\bar\alpha=A/S$ with V = 45.1 m³ and S = 76.8 m². T = 10 s gives A = 0.73 m² (ᾱ ≈ 0.01); T = 1 s gives A = 7.3 m². The difference in A between "empty" and "absorbers" divided by the absorber area gives the absorbers' **α in the room**. That is a good discussion point to compare with a data sheet, if one can be found. Measure the absorber panels on the day: you need their area.

## 4. Part C — vacuum-cleaner sound power

Room setup: **diffusers only, no absorbers**. Put the vacuum cleaner mid-room, far from mic positions 1–3. Call `psq = MeasPres(T, fc, fs)` at each of the 3 positions, then average **p² over the positions before** taking the log.

$$L_W=L_p-14\ \mathrm{dB}+10\log_{10}\frac{V}{1\ \mathrm{m^3}}-10\log_{10}\frac{T}{1\ \mathrm s}$$

> [!note] Where the −14 comes from
> Steady state in a diffuse field: $W=\dfrac{\langle p^2\rangle A}{4\rho c}$ and $A=\dfrac{0.161V}{T}$. Then $L_W=L_p+10\log\dfrac{0.161}{4}+10\log V-10\log T+10\log\dfrac{400}{\rho c}$. Here $10\log(0.161/4)=-13.95$ dB, and the last term is ≈ 0 because $\rho c\approx 400$. (Course text §3.2.6.)

Then A-weight each octave and add the bands as powers. The A-weighting values are from table 1.3.2:

| Octave (Hz) | 125 | 250 | 500 | 1k | 2k | 4k |
|---|---|---|---|---|---|---|
| A-weighting (dB) | −16.1 | −8.6 | −3.2 | 0 | +1.2 | +1.0 |

$$L_{WA}=10\log_{10}\sum_i 10^{(L_{W,i}+A_i)/10}$$

A household vacuum cleaner is typically **75–85 dB(A) re 1 pW** (EU label). Something far outside that range means a units or averaging slip. `lab_soundpower.m` does the whole chain from the six `psq` vectors and the T values.

**What to discuss:**
- The 3 positions are few, so the 125 Hz band is unreliable (below $f_S$).
- One source position.
- Diffusers make the field closer to diffuse.
- The near-field / direct-field contribution if a position is too close. Compare with the reverberation distance $r_h=\sqrt{A/16\pi}\approx0.1$ m, so the direct field is negligible beyond about 1 m.

## 5. Report outline (max 10 pages)

1. **Setup:** room, equipment, positions (sketch with mic and source positions), temperature.
2. **A:** table of predicted vs measured modes with $(n_x,n_y,n_z)$. Discuss the deviations: not perfectly rectangular, temperature, doors and windows, coupling to the walls.
3. **B:** T20/T30 per octave and per condition (one plot with four curves). Single vs averaged decay. T20 vs T30 choice. Subjective listening notes per condition. α of the absorbers estimated by Sabine.
4. **C:** $L_p$ per band, $L_W$ and $L_{WA}$ per band, total $L_{WA}$, uncertainty sources.
5. **Conclusion.**

## 6. Lab-day data sheet

Fill in on the day. CSV templates are in `5. Semester/Acoustics and Noise Control/Lab/data/`.

**General:** date ____, temperature ____ °C (→ c = ____ m/s), absorber panel size ____ × ____ m, mic positions marked on the sketch.

**A — modes**

| # | Predicted (Hz) | Measured (Hz) | Minima x / y / z | Identified $(n_x,n_y,n_z)$ |
|---|---|---|---|---|
| 1 | 39.2 | | | |
| 2 | 52.2 | | | |
| 3 | 54.9 | | | |
| 4 | 65.3 | | | |
| 5 | 67.4 | | | |

**B — reverberation time (s)**: save the `T20`, `T30` and `SNR` vectors and the decay figures for every condition. Save the `.mat` workspace too: `save('rt_<condition>.mat')`.

| Condition | | 125 | 250 | 500 | 1k | 2k | 4k |
|---|---|---|---|---|---|---|---|
| Empty, 1 × 1 | T20 / T30 | | | | | | |
| Empty, 5 × 3 | T20 / T30 / SNR | | | | | | |
| Absorbers | T20 / T30 / SNR | | | | | | |
| Abs + diff | T20 / T30 / SNR | | | | | | |
| Diffusers | T20 / T30 / SNR | | | | | | |

**C — vacuum cleaner:** save `psq` for positions 1–3 (`save('psq_vacuum.mat','psq1','psq2','psq3')`) and the background `bgpsq`.

## 7. Self-check before the lab

- [ ] Signed up in the schedule (group of 3); slot is green
- [ ] Sound level meter app installed and tested
- [ ] Music track on the phone + mini-jack
- [ ] Can explain why a corner excites and hears every mode
- [ ] Know the minima pattern of each of the five modes
- [ ] Can say when T30 is invalid (SNR) and why T30 > T20 in a non-diffuse room
- [ ] Know where the −14 dB comes from
- [ ] Bring a USB stick: the decay plots and `.mat` files leave the lab PC with you
