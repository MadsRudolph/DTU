---
tags: [34870, lab-d, lab-e, quiz]
---
# Lab D/E quiz: Q10 and Q11, model answers to read, then write your own

Q1–9 are already ticked, and Q5 has its text and two figures. These are the two written questions that waited for Lab E. Numbers are from our own data (`Lab E/matlab/plot_labE.m`, Lab D `plot_labD.m`). Figures are in `Lab DE - Quiz figures/` (also in `Labs/Lab E/quiz/`, which is gitignored). Theory and every number: [[Lab E - Runthrough]]. **Due Mon 26 Oct, individual.**

## Q10: Lab E (20 points)

**Figure 1:** `quiz_Q10_fig1_baffles.png`, the 3″ driver in the small box, on the circular screen and on the IEC screen, at 0° and 30°.

![[quiz_Q10_fig1_baffles.png]]

**Figure 2:** `quiz_Q10_fig2_system.png`, System D's three units at 0° and 30°, and the phase at 0° after compensation.

![[quiz_Q10_fig2_system.png]]

**Baffle shape.** The same 3″ driver was measured at 2.44 m on three mountings.
- **On a finite baffle, every edge point re-radiates an inverted copy of the wave.** Where that copy arrives half a wavelength behind the direct wave it adds (a peak), and where it arrives a whole wavelength behind it cancels (a dip).
- **On the circular screen** (a = 0.30 m, driver centred), every edge point is equally far away, so all the copies arrive together. The path difference is Δ = a + √(a² + r²) − r = 0.318 m. That puts dips at c/Δ = 1078 Hz and 2156 Hz; we measured **1059 Hz (−7.6 dB) and 2115 Hz**. The ripple is 17 dB peak to peak between 300 Hz and 5 kHz.
- **On the IEC screen** the driver is off-centre, so the edges are 0.20–0.44 m away. The copies arrive spread out in time and mostly cancel each other: 10 dB peak to peak, with no deep dips.
- **In the small box** the front is so small that the driver radiates into full space at low frequency. The box sits **5.7 dB below** the screens at 250–600 Hz and level with them above 3 kHz: the baffle step from 4π to 2π radiation.
- **At 30°** the circle's edge points are no longer equidistant from the microphone, so the ripple smears out.
- **diffrac.m** (Terai) with a 30 mm piston reproduces the circle-minus-IEC difference to 1.4 dB RMS (maximum 3.5 dB) from 300 Hz to 5 kHz. In that difference the driver's own response cancels out, so what is left is the baffles alone. A point source keeps rippling at full strength to 20 kHz; the real piston does not, because it sends less sound along the baffle once ka > 1.
- **The IEC off-axis curves divided by the 0° curve** follow a 30 mm piston's 2J₁(x)/x. At 60° we measured −3 dB at 3.45 kHz and the null at 7.96 kHz, against 3.40 and 8.06 kHz for the piston. At 15–30° the nulls come early above 10 kHz, because the cone no longer moves as a rigid piston.

**The three units of System D** (vent plugged, all three in one run, so the relative phase is valid).
- **Woofer:** the most sensitive at low frequency, 7.7 dB re 1 Pa/V at 150–600 Hz, about 5 dB above the midrange. It goes to about 3 kHz on axis, but at 30° it is **15.6 dB down** at 3–8 kHz. A 21 cm piston has ka = 1 at 520 Hz, so it beams early.
- **Midrange** (the DALI Spektor 2's 5¼″ driver, a ≈ 5.25 cm): the flattest of the three, ±2 dB from 120 Hz to 4 kHz. It reaches 12 kHz on axis, but loses 7.5 dB at 30° in the 3–8 kHz band, a little less than a rigid 5.25 cm piston (−10.3 dB): the cone breaks up and its effective area shrinks.
- **Tweeter** (Spektor 2, 25 mm soft dome, ka = 1 at 4.4 kHz): about **9 dB louder** than the midrange in its band (12.4 dB at 1–3 kHz) and almost no beaming (−0.7 dB at 30°). It falls off below 1 kHz, where its resonance (1.45 kHz from Lab D) sets the second-order roll-off.
- **Crossovers:** the curves cross near 950 Hz, but that would drive the tweeter at its resonance. A mid/tweeter crossover around 2.5–3 kHz with about 9 dB of attenuation on the tweeter fits better. DALI's own crossover for the Spektor 2 is at **2,600 Hz**, which agrees. The woofer has to hand over to the midrange well below 1.5 kHz, where it starts to beam.

**Phase.**
- Each measured phase holds the unit's own phase, the flight time and a random sound-card delay. The last two are common to all three units in one run.
- With one compensation distance for all three units, **d = −1.15 m** (negative because the card delay was shorter than the flight time), the phases become readable.
- Read directly as angle(H_a/H_b), where every common delay cancels:
  - woofer − midrange: −12° at 300 Hz, −58° at 2 kHz. The units are nearly in phase, with the woofer's acoustic centre slightly further back.
  - tweeter − midrange: **+163° at 300 Hz**, falling to +76° at 3 kHz. The tweeter is close to inverted below its resonance.
- The crossover must sum the units with these phases. The polarity of the tweeter and the filter orders are chosen against this curve, not assumed.

## Q11: Lab D ↔ Lab E (20 points)

- **The two labs measure the same three units from two sides.** Lab D measures the **electrical** side (input impedance, the load the amplifier and the crossover see). Lab E measures the **acoustic** side (pressure per volt, magnitude and phase, in free field).
- **What Lab D gives the project:**
  - The woofer's T-S behaviour and box tuning: f_S = 22.7 Hz in free air, f_C = 42.0 Hz in the 88 L closed box, and f_B = 23.4 / 22.8 / 21.5 Hz for the 160 / 200 / 240 mm vents.
  - The **complex impedances** of the midrange (R_E = 4.6 Ω, resonance 90 Hz in its box) and the tweeter (R_E = 3.4 Ω, resonance 1.45 kHz). A passive crossover is designed against the real impedance, not a resistor. A filter calculated for a nominal 4 Ω sees an impedance that rises with the voice-coil inductance, so its corner moves.
- **What Lab E gives the project:**
  - The acoustic response that the crossover has to shape: the levels (the tweeter needs about 9 dB of attenuation), the usable band of each unit, the directivity (the woofer beams above about 1.5 kHz, the midrange above about 4 kHz), and the relative phase between the units at the listening position.
- **Why both are needed:**
  - Lab D says how the units load the filter, and Lab E says what the filter's output must look like acoustically. The final response is the voltage transfer of the crossover (which depends on the Lab D impedances) times the Lab E pressure-per-volt of each unit, summed with their phases.
- **The low end comes from Lab D, because Lab E cannot measure it.**
  - The anechoic chamber is not anechoic at low frequency and the vent was plugged in Lab E. So the vented-box tuning from Lab D (f_B, the near-field cone and vent responses) completes the woofer response below about 100 Hz.
  - Lab E's curve is valid above that.
- **The link between the two.** The tweeter's falling response below 1 kHz in Lab E sits where its impedance peak at 1.45 kHz is in Lab D, and the woofer's low-end roll-off in both labs follows from the same T-S parameters.
