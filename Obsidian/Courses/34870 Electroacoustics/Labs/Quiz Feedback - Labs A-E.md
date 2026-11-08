---
tags: [34870, quiz, feedback, oral-exam]
---
# Quiz feedback: Labs A, B/C, D/E

Everything the teachers wrote back on the three lab quizzes (DTU Learn → Quizzes → *View Feedback*, read 8-Nov-2026), sorted by what we lost points on, plus what it means for the oral exam on 9–10 Dec. The quizzes are 30 % of the grade, so these are also the examiners' own words on what they look for.

| Quiz | Submitted | Score | Where the points went |
|---|---|---|---|
| Lab A: Analogy circuits in LTspice | 20-Sep | **89 %** | phase missing, unit prefixes, plotted transfer functions instead of the requested variable, "resonance" used loosely |
| Lab B/C: Microphones | 5-Oct | **98 %** | Q10: the LTspice match was "too good" (the alignment hid the model's bias) |
| Lab D/E: Loudspeakers | 26-Oct | **98 %** | Q5: impedance peak height not explained with R_E + (Bl)²/R_MS, near-field curves summed although they are not phase-coherent |
| Project part 1/2 | 8-Nov | – | submitted, no feedback yet: add it here when it arrives |
| Project part 2/2 | due 30-Nov | – | not started |

Related: [[Lab A - Runthrough]] · [[Lab BC - Quiz model answers]] · [[Lab DE - Quiz model answers]] · the class-wide slides `34870_LabAfeedback (2).pdf` (the newer version; the first one is the 21-Sep draft).

---

## 1. The recurring lessons (read this before every written answer and before the oral)

```mermaid
flowchart LR
    A[Plot] --> B{What was asked?}
    B -->|network variable| C[Plot that variable,<br/>not a ratio to the source]
    C --> D[Magnitude AND phase]
    D --> E[Units: 'Force / N' or 'Force (N)',<br/>never brackets, never el. units on mech./ac. elements]
    E --> F[Quantify: f, level, slope, phase]
    F --> G[Explain WHY with physics,<br/>not only describe]
```

1. **Always magnitude *and* phase.** A complex variable needs both. Phase was the most common comment in Lab A (Q3, Q20, overall). It is also the precise way to find a resonance: read the phase zero crossing, or better a Nyquist plot, not the visual peak.
2. **Plot exactly what was asked.** "Velocity" means u in m/s for the given source, not u/u_source or u/V. Transfer functions were marked down in Lab A Q12, Q20 and Q23 ("no transfer functions in this exercise"). LTspice node names don't know which analogy you used.
3. **"Resonance" is a property of the system's impedance, not of a peak in a velocity or pressure curve.**
   - Impedance **minimum** (dip) means easy to move: **resonance**.
   - Impedance **maximum** (peak) means hard to move: **anti-resonance**.
   - A peak in u or p can be the *result* of a resonance, but also of something else, e.g. Z = R(ω) + jωL. Check the impedance seen by the source.
4. **Unit prefixes belong to the unit and are raised to the power with it.** 1 mm² = 10⁻⁶ m², so "112.5 p m⁵/N" reads as 10⁻⁶⁰ and is wrong. "kkg" and "Mg" don't exist (10³ kg = 1 t). A space between prefix and unit doesn't help ("m s" = metre·second). **Use powers of ten for acoustic and mechanical elements:** 1.125·10⁻¹⁰ m⁵/N, 2.348·10³ kg/m⁴. LTspice's "k", "n" and "p" are not SI notation.
5. **No electrical units on mechanical or acoustic elements** in circuit figures. The mass is in kg (mechanical) or kg/m⁴ (acoustic), not H. This was marked down in Lab A Q18 and Q22.
6. **Units are not written in [square brackets]:** "Force / N" or "Force (N)". dB always needs a reference ("dB re 1 Pa", "dB re 1 m/s") unless it is a ratio.
7. **Use physical words precisely.** "Absorber" and "damped" were questioned twice (Q4, Q23). If you use "absorber", explain the mechanism: which part moves, which stands still, and the relative phase.
8. **Don't tune the model so far to the data that its limitations disappear** (Lab C Q10). A remaining bias is a result: show it and explain it.
9. **Know which data are phase-coherent.** Separate runs with the sound card's random delay can't be summed as complex numbers (Lab D Q5). We said exactly that for Lab E's single runs but then did it ourselves in Lab D.
10. **Quantify, then explain.** "Very good" comments came where every claim had a number *and* a physical reason (Lab A Q15, Q27; Lab B/C Q11; Lab D/E Q10).

---

## 2. Lab A: Analogy circuits in LTspice (89/100)

**Overall comment (verbatim):**
> A very good attempt, passing the quiz (89/100). In general, a very good level of understanding the basics and many concepts is apparent. Some discussions and explanations can be improved especially by considering phase. Some rushing mistakes. Double-check that you plot what was actually requested (no transfer functions in this exercise). Very good figures, easily readable and mostly well labelled (no [brackets] for units). If circuit figures include units, make sure they are correct (not el. units for mech./ac. elements). Understand how unit prefixes (m, k, G) work and that they go together with a unit (and that SI unit kg is special). I.e. 1 mm^2 = 10^-6 m^2.

### Where points were lost

| Q | Score | What we wrote | Feedback | What to do / the right physics |
|---|---|---|---|---|
| 3: velocities, stiff vs soft link | 2.5/4 | Magnitude plot. Stiff link: one resonance at 51.4 Hz. Soft link: "absorber dip" in u_vc at 1.29 kHz, second resonance at 1.78 kHz, "mechanical crossover" | Phase missing. No [brackets]. Careful calling peaks and dips in velocity plots (anti-)resonances: only the impedance shows that directly, or drive with a *velocity source*. More physics: how do the masses move relative to each other at the dip? | At the dip, the outer cone on the soft link is a tuned mass-spring. Its mobility 1/(jωM_o) + jωC_link → 0 at f = 1/(2π√(M_o·C_link)), so the branch presents an *infinite* impedance to the coil node. The coil is blocked (u_vc ≈ 0) while the outer cone swings in anti-phase and its spring force cancels the drive. That is the anti-resonance, and the phase plot shows the 180° flip. |
| 4: mechanical input impedance | 4.5/5 | Z_M = F/u_vc. Stiff: one minimum. Soft: minimum at 51.4 Hz, maximum 334 Ns/m at 1.29 kHz, minimum at 1.78 kHz, then the 6 g mass line | Correct curves. Units not in brackets. The "absorber" statement needs clarifying | Same explanation as Q3. Name it *anti-resonance* and explain why. |
| 6: number of (anti-)resonances in Z_M, soft link | **0/1** | ticked **2** | (hint only: use peaks, dips and phase shifts) | Our own Q4 text lists **three**: resonance 51 Hz, anti-resonance 1.29 kHz, resonance 1.79 kHz. Count the anti-resonance too. The stiff case has 1 (correct). *Rushing mistake.* |
| 10: silencer element values | 3/4 | "2.348 k kg/m⁴", "112.5 p m⁵/N" | Wrong use of prefixes. pm⁵ means 10⁻⁶⁰. No "kkg", no "Mg" | Values were right, the notation wrong. Write M_A = 2.348·10³ kg/m⁴ and C_A = 1.125·10⁻¹⁰ m⁵/N (chambers: 1.125, 7.200, 3.037·10⁻¹⁰ m⁵/N; tubes 2.348, 7.512, 9.390, 3.756·10³ kg/m⁴). |
| 12: U_out, pressure vs volume-velocity source | 3/4 | Plotted U_out/U_in ("transfer function"). Called the peaks resonances | Volume velocity was requested, not relative to the source. Peaks in velocity aren't automatically resonances: check the system impedance. What about the overall amplitude difference (hidden by the normalisation)? | Plot U_out in m³/s for the given source amplitude. Identify resonances from Z_in. Comment on the absolute level difference between the two sources. |
| 14: pressure at the opening + Z_rad | 3.5/4 | "311.0 f m⁵/N", [brackets] | 1 fm⁵ = 10⁻⁷⁵ m⁵. Use powers of ten | C_A = 3.110·10⁻¹³ m⁵/N. |
| 18: radiation impedances of the dual diaphragm | 5.5/8 | Four baffled-piston networks (correct), drawn as **one series network per diaphragm** (2M, 2R, C/2). Circuit labelled with electrical units. "3.551 n m⁵/N" | Electrical units on mechanical/acoustic elements! Combining front and back in series is allowed, but then **you can't read the front and back pressures separately**: the p_i, p_o in the figure are a sum or difference, not the front pressure. nm⁵ = 10⁻⁴⁵ | Keep the front and back radiation impedances as separate branches so the front pressure is a node voltage. Use kg/m⁴, Pa·s/m³, m⁵/N with powers of ten. |
| 20: front pressure of each diaphragm | 4/6 | Plotted V(p)/2 per 1 N (a transfer function), magnitude only. Good level and slope numbers | Phase missing. Pressure was requested, not a transfer function. The result is right but doesn't match the p_i/p_o drawn in the circuit. **No phase discussion: how do the two diaphragms radiate relative to each other at the second resonance, and what does that do to the combined output?** **The high-frequency roll-off is the key benefit of this design** | At the 2nd resonance the two masses move *against* each other on the link spring (anti-phase), so their contributions partly cancel in the summed output. Lead with the design benefit: above it the heavy outer cone decouples, so only the 6 g inner cone radiates → extended treble. |
| 22: electrodynamic circuit | 3.5/4 | Figure only | Electrical units on mechanical elements | As above. |
| 23: velocities of the two masses | 4/4 | | Velocity, not transfer function. No brackets. Careful with "absorber" and "damped" | Full marks, but same three habits. |
| 25: table of (anti-)resonances | 3.5/4 | Listed 5 rows, including "electrical resonance (shallow min.)" at 127 Hz and 1.40 kHz. Mechanical anti-resonance 6.88 kNs/m at 158.5 Hz | **The electrical system has no resonance** (where is the dip with a phase jump?). Mechanical impedance at #3 is wrong, probably the frequency resolution is too low. Frequencies are slightly off, especially #4: use phase or Nyquist | Only rows 1, 3, 4 are real (4.90 Hz res., 158.5 Hz anti-res., 733 Hz res.). A shallow dip without a phase zero crossing isn't a resonance. Refine the sweep around peaks (`.ac dec` with many points per decade, or a narrow linear sweep) before reading off the peak value. |

### Full marks, but the hint is worth keeping

- **Q1 / Q9: analogy tables.** IA: force = across/potential (voltage), velocity = through/kinetic (current), mass = differential element (L), compliance = integral element (C), damper = real (R). MA swaps them: force = through, velocity = across, mass = integral element (C, grounded!), compliance = differential element (L). Acoustic (impedance analogy): p = across, U = through, M_A = L, C_A = C (grounded), losses = R.
- **Q2: "Remember that masses need to be grounded in MA."** **Q11: "Volume compliances need to be grounded."** In both cases one terminal of the element is the inertial reference or the ambient pressure.
- **Q7 / Q8:** use the phase shift to find resonance frequencies, and Nyquist is even better. Don't mistake the anti-resonance for the second resonance.
- **Q13: radiation impedance** goes **in series** after the last pipe. The pipe's element value is **reduced by the radiation mass**, because the given "effective length" already includes the end correction. Output pressure is taken **between the last pipe and Z_rad**.
- **Q15 ("Very good"):** 10 m pressure ratio ρ/(4πr·M_A) → −81.8 dB, frequency independent. The lumped model only holds while l < λ/10, which the 100 mm pipe meets only below about 344 Hz.
- **Q16 / Q21: controlled sources** (check on the oral by asking what each network variable maps to):

| Equation | IA | MA |
|---|---|---|
| U = S·u (acoustic ↔ mech.) | CCCS (u is a current) | VCCS (u is a voltage) |
| f = S·p | VCVS | VCCS |
| Z_m = S²·Z_a | impedance conversion | impedance conversion |
| f = Bl·i (Lorentz) | CCVS | CCCS |
| v = Bl·u (Faraday) | CCVS | VCVS |

- **Q17:** four radiation impedances: two diaphragms, two sides each.
- **Q19:** adding Z_rad leaves the stiff/soft coupling effect the same, moves the (anti-)resonances **down** (the added mass), and **raises** Z_M at the first resonance (added radiation resistance).
- **Q26 / Q27 ("Very good about inversion. Exact about anti-resonance."):** Z_E = R_E + jωL_e + (Bl)²/Z_M.
  - A mechanical resonance (Z_M minimum) means large velocity and large back-EMF, so little current flows and Z_E peaks: an **electrical anti-resonance**, and it needs **low** current/power.
  - A mechanical anti-resonance means the coil is blocked and there is no back-EMF. (Bl)²/Z_M ≈ 0.33 mΩ disappears next to R_c, so it **does not appear** in Z_E.

---

## 3. Lab B/C: Microphones (98/100)

No overall comment. All multiple-choice questions got full marks (answers in [[Lab BC - Quiz model answers]]).

| Q | Score | Feedback (verbatim, shortened) | Lesson |
|---|---|---|---|
| 5: Lab B results | 20/20 | "The figures are very detailed and explanatory. You review almost all aspects of the exercise. **You could have used the averaged simulation in BEM to prove your point with the datasheets.**" | We argued that a real diaphragm averages the pressure over its area, which is why the handbook peak sits higher in frequency than the scaled 0° point value. The BEM package can average over the face, so use that averaged curve as the evidence. Good oral material. |
| 10: Lab C results | **18/20** | (1) "It is not surprising that the calibrators have the systematic drop at 250 Hz. **These are field instruments, not meant for calibration (despite the name), but for field verification.** The actuator calibration should use a **pistonphone**, a lab instrument with much lower uncertainty." (2) "**Your match with the simulation is surprisingly good.** Usually the result shows a bias for one of the microphones for the reasons mentioned in the exercise text. If you corrected this, you miss an effect that reveals the limitations of the model." | (1) Know the hierarchy: primary reciprocity calibration (lab standard mics) → pistonphone (lab reference) → sound calibrator (field check). (2) We aligned both LTspice curves at 1 kHz, which hid the 1.4 dB offset of the 4133. The model has *one* diaphragm data set for two different microphones. That bias is the point: show the absolute curves and explain it. |
| 11: Lab B ↔ Lab C | 20/20 | "Precise and detailed explanation. Very good." | Free-field mic (4133, over-damped, Q ≈ 0.34) cancels its own body's pressure build-up. Pressure mic (4134, Q ≈ 0.84) is flat in pressure and belongs in couplers, walls, or at grazing incidence. Keep this answer for the oral. |

---

## 4. Lab D/E: Loudspeakers (98/100)

No overall comment. All multiple-choice questions got full marks (answers in [[Lab DE - Quiz model answers]]).

| Q | Score | Feedback (verbatim) | Lesson |
|---|---|---|---|
| 5: Lab D results | **18/20** | "**The maximum impedance at f0 is Re + (Bl)²/Rms.** It is higher for drivers with higher DC resistance, larger Bl or smaller suspension resistance. See slide 11, lecture 7. Otherwise good analysis and nice commented figures. **Note that the near-field measurements are not coherent in phase the way we measure. Summing in the far field may not be correct.**" | We described the three peak heights (woofer 117 Ω, mid 19 Ω, tweeter 6.7 Ω) and called the tweeter "heavily damped" without the formula. Explain differences with \|Z\|_max = R_E + (Bl)²/R_MS. Cone and vent were measured in separate runs, each with its own sound-card delay, so the complex cone + vent sum (and the "180° apart" claim) isn't trustworthy. Only a simultaneous two-channel measurement, or a magnitude-only argument, holds. |
| 10: Lab E results | 20/20 | "Very detailed and insightful description and excellent commented figures. Good job." | The model answer for diffraction, baffle step and directivity. |
| 11: Lab D ↔ Lab E | 20/20 | "Nice overview." | Lab D = electrical side and low end (T-S, box, vent, near field), Lab E = acoustic side (level, band, directivity, relative phase). The crossover sits near 2.6 kHz, not at the 950 Hz crossing, because of the tweeter's 1.45 kHz resonance. |

Multiple-choice facts worth having ready: f_b is the **minimum between the two impedance peaks**. V_AS comes from **baffle + closed-box impedances** (or a known added mass). In the near field the **cone has a minimum and the vent a maximum at f_b**. The near-field method is used because the chamber fails at low frequency and near-field pressure converts to far field with a factor. Baffle: off-centre driver and rounded edges are good. Lab B ↔ E: a body alters the field once its size is comparable to λ, and source and receiver are reciprocal. Directivity grows with frequency. Fix the mic position because of directivity and of relative phase near the crossover.

---

## 5. Oral exam drill: questions the feedback tells us to expect

Answer each out loud, in 30–60 s, *with a sketch and the phase*:

1. What is a resonance and what is an anti-resonance? How do you find them precisely (phase zero crossing, Nyquist), and why isn't every peak in a velocity plot one?
2. Dual-diaphragm speaker with a soft link: how many resonances and anti-resonances, how do the two masses move at each one (in phase or anti-phase), and why does the design extend the treble?
3. Why does a mechanical resonance show up as a *peak* in Z_E, and why does the mechanical anti-resonance vanish? Write Z_E = R_E + jωL_e + (Bl)²/Z_M.
4. What sets the height of the impedance peak at f_s? R_E + (Bl)²/R_MS, so compare woofer, midrange and tweeter.
5. Radiation impedance: why four in Lab A part 3, and why does adding it lower the resonances? Effective length and end correction: why is the last pipe's mass reduced?
6. Where do you read f_b in a vented box, both in the impedance and in the near field? Why can't separately measured near-field curves be summed?
7. Calibration chain: reciprocity → pistonphone → sound calibrator. What are the calibrator and the actuator each good for?
8. Free-field vs pressure microphone: how does Lab B's scattering decide which one is "right"? Why does the diaphragm average the pressure?
9. Why does the LTspice condenser model fit one microphone worse than the other? (one diaphragm data set, one lumped backplate element)
10. Baffle diffraction: why does a centred circular baffle give the worst ripple, and what is the baffle step?
11. Units drill: write 15.71 cm³ as an acoustic compliance in m⁵/N, and a 25 mm tube of radius *a* as an acoustic mass in kg/m⁴, with powers of ten and no prefixes.
