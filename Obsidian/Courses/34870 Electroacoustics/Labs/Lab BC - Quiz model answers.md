---
tags: [34870, lab-b, lab-c, quiz]
---
# Lab B/C quiz: model answers to read, then write your own

Numbers are from our own data (`Lab B/matlab/process_labB.m`, `Lab C/matlab/run_all.m`). Figures in `Lab BC - Quiz figures/` (upload one per written question). Theory: [[Lab B - Runthrough]], [[Lab C - Preparation]].

## Multiple choice

| Q | Tick | One-line reason |
|---|---|---|
| 1 | nearly no reflections from the walls; well isolated from the exterior | It only works above the ~125 Hz cut-off, and reverberant is the opposite of what you want. |
| 2 | loudspeaker and microphone responses eliminated; only the effect of the mock-up remains | Everything common to both measurements cancels in the ratio. |
| 3 | scattering on a mic body, scaled down in frequency; the field the mock-up mic would measure, normalised by the field without it | Both describe the free-field correction. |
| 4 | ratio of mock-up and real microphone dimensions; frequency axis multiplied by the scale factor | Constant ka means f·D is constant: f_mic = f_mock · D_mock/D_mic (×19.7 for ½″). |
| 6 | well-defined, controllable gain; polarisation voltage and preamp supply | It doesn't equalise the mic or process data. |
| 7 | radiation impedance more similar to that without actuator | Without the holes, a trapped air film would load the diaphragm. |
| 8 | sensitivity at one frequency; used to adjust (scale) the actuator response | The actuator gives the shape, the calibrator the level. |
| 9 | all elements contribute to the uncertainty; a measurement can never be repeated exactly | The spread is uncertainty, not faulty calibrators. There is no "true value" to reach. |

## Q5: Lab B

![[quiz_Q5_labB.png]]

We measured the pressure on the face of a 25 cm cylinder mock-up relative to the free field (same position, mock-up removed), at 0° to 90° in 15° steps, and compared it with BEM.

**Up to about 200 Hz** the body is small compared with the wavelength (ka ≪ 1). The correction is 0 dB at all angles.

**Between 200 Hz and 2 kHz** the pressure on the face builds up as ka approaches 1.
- At 0° it passes +6 dB (pressure doubling, as at a rigid wall).
- It peaks at **+8.6 dB at 1155 Hz**; the BEM gives +9.9 dB at 1345 Hz. The extra rise above +6 dB comes from diffraction around the edge of the face.
- The effect drops with angle: +5 dB at 60° and within +2 dB at 90°, where the face is side-on to the wave.
- Measurement and BEM agree within about 1 dB at all angles in this range.

**Above 2 kHz** the curves split. The UMIK tip was 2–3 cm in front of the face, not on it, and at 3.9 kHz that gap is a quarter wavelength. This gives the −18 dB notch at 0°. The BEM evaluated 3 cm in front of the face reproduces the whole measured 0° curve within 1.5 dB, so the difference is the probe position, not the model.

**Scaled to real microphones**, multiply the frequency by D_mock/D_mic.
- For a 1″ mic (×10.5) the peak lands at about 12 kHz and +8.6 dB. That matches the handbook's curve for a 1″ mic without grid.
- For ½″ (×19.7) it lands at about 23 kHz.

## Q10: Lab C

![[quiz_Q10_labC.png]]

We calibrated two ½″ condenser microphones in two steps.
1. **Level:** three GRAS 42AG calibrators give the sensitivity at a single frequency.
2. **Shape:** an electrostatic actuator measures the pressure response from 20 Hz to 42 kHz. That is the upper limit set by the 96 kHz card; lines above 48 kHz are aliased.

Both were corrected for the DAQ and Nexus chain with H_21,ref. Its phase is a 3.2 µs channel delay, which would otherwise shift the −90° point by several kHz.

**Where this sits in the calibration chain.** It is a secondary calibration: our reference is the calibrator. The calibrator itself is traceable to a primary reciprocity calibration of a laboratory standard microphone, which only needs electrical and physical quantities. The actuator gives the pressure response. For field measurements that has to be combined with the free-field (or diffuse-field) correction of the microphone body: the result of Lab B.

**Results (1 kHz, mean of 3 calibrators):**
- Mic 1 = **4134 (pressure field)**: **10.98 mV/Pa** (−39.2 dB re 1 V/Pa), **f_s = 20.2 kHz, Q = 0.84**
- Mic 2 = **4133 (free field)**: **13.03 mV/Pa** (−37.7 dB re 1 V/Pa), **f_s = 22.9 kHz, Q = 0.34**

f_s is where the phase crosses −90°, and Q is |H(f_s)| relative to the flat level.

**Repeatability, reproducibility, uncertainty.** The three calibrators agree within 0.2 %, which shows the repeatability. The 250 Hz results are 4 % (0.35 dB) lower for both microphones, which is a systematic effect of the method, not of the microphones. The expanded uncertainty is about 2.8 % (k = 2), dominated by the calibrator tolerance.

**LTspice.** The model takes the brief's diaphragm data and gets the backplate mass and resistance from f_s and Q:
- 4134: M_AS = 420 kg/m⁴, R_AS = 1.3·10⁸ Pa·s/m³
- 4133: M_AS = 231 kg/m⁴, R_AS = 2.8·10⁸ Pa·s/m³

The model level (11.14 mV/Pa) is the same for both mics because the brief gives one set of diaphragm data. That is 0.1 dB below the 4134 and 1.4 dB below the 4133, as the brief's appendix warns. Aligned at 1 kHz, the shape matches both mics within ±0.5 dB up to 20 kHz, and the phase within 5°. Above resonance the 4133 departs by up to 1.6 dB and 19°: one lumped backplate R and M can't follow the frequency-dependent air-film damping of a heavily damped free-field capsule. The same thing shows as a 9 % difference between its −90° reading (22.9 kHz) and a whole-curve fit (21.1 kHz).

## Q11: Lab B ↔ Lab C

![[quiz_Q11_labB_labC.png]]

Lab B shows what a microphone body does to the sound field. Facing the source, the pressure on the diaphragm rises with frequency, reaching about +8 to 9 dB when the diameter is comparable to the wavelength. For a ½″ microphone that is roughly 10–30 kHz. A microphone in a free field therefore does not measure the undisturbed pressure; it measures that pressure times the Lab B correction.

The two Lab C microphones deal with this in opposite ways.
- **4133 (free-field type):** deliberately over-damped (Q = 0.34). Its pressure response in the actuator already falls by 3.6 dB at 10 kHz and 8.3 dB at 19 kHz. Adding our Lab B 0° correction scaled to ½″ (+3.9 dB at 10 kHz, +7.7 dB at 19 kHz), its free-field response comes out flat within about ±0.7 dB up to 20 kHz. The damping is chosen to cancel the pressure build-up caused by its own body.
- **4134 (pressure type):** flat in pressure (Q = 0.84) up to about 15 kHz. In a free field at 0° it would therefore read up to about +7 dB too high around 15–20 kHz. It is meant for places where the microphone is part of the boundary and measures the pressure that is there: couplers, walls, small cavities. It can also be used at grazing (90°) incidence in a free field, where Lab B shows the correction is small (under 2 dB).

The actuator measurement alone can't tell which microphone is "better": it only shows the pressure response. Whether a response is right depends on the sound field it is used in. That is what Lab B measures.
