---
tags: [34870, quiz, project, loudspeaker]
---
# Loudspeaker project quiz, part 1/2: what we submitted

Submitted **Sun 8-Nov-2026** on DTU Learn (individual quiz, 10 questions: 8 multiple choice × 2.5 points, Q5 and Q10 × 15 points). No feedback yet; add it to [[Quiz Feedback - Labs A-E]] when it arrives.

Design behind the answers: `5. Semester/Electroacoustics/Labs/Project/Final design/` (report `report/Project_report.tex`, circuits `ltspice/task1/Woofer_Vented_L160.asc` and `ltspice/System_D_course.asc`). Study guide to the two circuits: https://claude.ai/artifact/VUzWqsYsKXDffSh1KDfLps

---

## Task 1: low-frequency design of the woofer box

| Q | Question | What we ticked | Why |
|---|---|---|---|
| 1 | Why fill the woofer box with fibre material? | **damps box resonances** · **effective volume larger than the physical volume** | Project Guide: filling "slightly increase[s] the effective volume of the box and its damping". |
| 2 | Two vents, mark the correct statements | **no radiation impedance at the vent opening needed if its total effective length is used** · **same length: the narrower vent has the larger acoustic mass** | M_A = ρL/S, so a smaller S gives a larger mass. Two vents open = masses in parallel = *less* mass, so "open both for maximum mass" is false. The end corrections in the effective length are the radiation mass. |
| 3 | Tuning of the project box | **the impedance minimum between the peaks marks the box resonance** · **draw and validate the LF analogy in LTspice and use it to tune** | Guide: "you will not be able to achieve any of the standard tunings". The two peaks are coupled-system resonances, not one box peak + one driver peak. |
| 4 | Near-field measurements | **validate the LTspice analogy** · **far field can be obtained from near-field results** | T/S parameters come from the impedance, not the near field (we first had that ticked and changed it). Crossover design uses the anechoic (Lab E) data. Far field from near field: the Lab D brief says the two pressures "can only be added to give the far field pressure after appropriate scaling" (by area), but the Lab D/E feedback reminds us that two **separate runs** are not phase-coherent, so the sum needs one run or the model. The least certain tick. |

### Q5 (15 points): two figures + max half a page

![[Quiz1_Q5_fig1_woofer_circuit.png]]
**Figure 1:** Our LTspice circuit of the woofer box.

![[Quiz1_Q5_fig2_woofer_response.png]]
**Figure 2:** Response from LTspice. Left: far field from the driver, the vent and the total (with the closed box for comparison). Right: the model compared with our Lab D measurements.

> Figure 1 shows our analogy circuit for the woofer in the box. It has three parts: the electrical part (the voice coil), the mechanical part (cone mass, suspension and losses) and the acoustical part (the air in the box, the vent and the air in front of the cone). The parts are connected with controlled sources for Bl and the cone area S_D. We got the driver values by fitting the circuit to our own impedance measurements from Lab D, because our woofer did not quite match the data sheet.
>
> We chose to use one vent with a length of 160 mm and keep the other vent plugged. This gives f_B ≈ 24.6 Hz and moves f_3 from about 37 Hz (closed box) down to about 33 Hz, with a small bump of around 2 dB, which we think is fine. Around f_B the cone hardly moves and the vent does most of the work, which can be seen in Figure 2. We also measured the longer vent lengths (200 and 240 mm), but in the model they did not really give more bass. We did not measure with both vents open, but we tried it in the model with an estimated vent mass, and it only made the bump bigger without more bass. The driver itself was measured without filling (free air and closed box, as the lab brief says), but the vent measurements were done with the filling material in the box, because it is needed to damp the box resonances. So the fitted vent and loss values already include the effect of the filling, and the model describes the box the way we will use it.
>
> To check the model we compared it with the near-field and impedance measurements from Lab D (Figure 2, right). The peaks and the dip at f_B line up well. The near-field level from the model is about 2 dB too high, probably because of the simple formula we use for the near field.

**Facts checked while writing Q5** (worth remembering for the oral):
- Lab D brief 2b1/2b2: free air and closed box **without** filling (so V_AB is the physical volume); the filling was put back before the vented runs (2b4) and the near field. The fitted vent mass and losses therefore describe the *filled* box. The extra losses with a vent open are partly the filling, not only the vent.
- **Both vents open was never measured**: it is a model-only row with an estimated M_AP ≈ 52 kg/m⁴.
- With an empty box, the tube formula puts the 160 mm tuning at 23.3 Hz against the measured impedance dip at 23.4 Hz; the fitted model's dip sits at 24.4 Hz.

---

## Task 2: crossover design

| Q | Question | What we ticked | Why |
|---|---|---|---|
| 6 | Responses of the three units in the LTspice crossover | **carefully measure relative phases between units** · **unwrap and distance-correct the phases** | Guide: "use the same distance for all drivers" (we used d = −1.15 m for all three), so "a different correction per unit" is false. Magnitude alone is not enough. |
| 7 | Input impedance in the crossover simulation | **Zi affects passive crossover filters** · **the woofer box Zi does not need to be included** | Guide 2.2: "There is no need to include Zi, as the unit is excited by the amplifier directly." An ideal amplifier's voltage does not depend on the load, so digital filters are not affected. |
| 8 | What can you test with passive filters in the simulation? | **smooth transition around the crossover** · **interaction between digital and passive filters** · **tolerances of real components** | Guide: "their values have tolerances. Test the effects on the LTspice." The crossover simulation cannot check the Task 1 low end. |
| 9 | Implementation of the crossover simulation | **predicted behaviour as measured in the anechoic chamber** · **effect of components with tolerance** | The TFs are anechoic measurements (Lab E), valid only above ≈ 125 Hz, so the simulation cannot show the woofer box's low end. It does show phase differences between units. |

### Q10 (15 points): two figures + max half a page

![[Quiz1_Q10_fig1_system_circuit.png]]
**Figure 1:** Our LTspice crossover simulation, one row for each unit.

![[Quiz1_Q10_fig2_system_response.png]]
**Figure 2:** Simulated response at the microphone for each unit and for the whole box (sum), with the phase below.

> Figure 1 is our crossover simulation, with one row for each unit. The measured impedances (Lab D) and responses (Lab E) are loaded with .inc files, and we used the same distance correction for all three units so the phase differences between them are kept. At the end the three outputs are added together to get the response of the whole box.
>
> Between the woofer and the midrange we use the digital filter in the MiniDSP: a 4th order Linkwitz-Riley at 325 Hz (two Butterworth biquads after each other). We picked LR4 because the two outputs stay in phase and add up flat. 325 Hz keeps the woofer away from the frequencies where it starts to break up, and the midrange well above its resonance. The woofer was about 4–5 dB louder than the midrange, so we turned it down 4.5 dB.
>
> Between the midrange and the tweeter we use passive 2nd order filters with values from the component list: 0.82 mH and 6.8 µF for the midrange, and 5.6 µF and 0.22 mH for the tweeter. The tweeter was around 10 dB louder, so we added an L-pad (4.7 Ω and 3.3 Ω). The midrange coil ended up bigger than the textbook value because the midrange impedance goes up with frequency.
>
> Figure 2 shows the result. The sum stays within about ±2 dB from 150 Hz to 15 kHz, and all units are connected with normal polarity. Below around 125 Hz the measurements from the anechoic room are not reliable, so the low end is covered by the woofer box design.

**Facts behind Q10:**
- **`.inc` files** paste a measured table into the netlist: `BiZin_*` is a current source I = V·Y(f) (the table holds the admittance 1/Zi), `BvTF_*` a voltage source Pout = V(Vspkr)·TF(f). This is the course's own "Option 1 (default and recommended)" from `Passive_Filters_And_Measurement_Data_in_LTspice.zip`.
- **L-pad:** R3 4.7 Ω in series, R4 3.3 Ω across the tweeter (≈ 4 Ω at 4–5 kHz): 3.3 ‖ 4 ≈ 1.8 Ω, divider 1.8/6.5 ≈ −11 dB. The shunt resistor also holds the load seen by the filter near 6.5–6.9 Ω, hiding the tweeter's 1.45 kHz impedance peak.
- LTspice and the Python design model agree to 0.00 dB; on-axis spread 4.0 dB (1/6 octave, 150 Hz–15 kHz), 6.2 dB at 30°, minimum load on amplifier channel 2 = 4.40 Ω.
