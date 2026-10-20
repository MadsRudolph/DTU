/* Self-checks per lecture. c = index of the correct answer. */
"use strict";
window.QUIZZES = {
  "1": [
    { q: "In a plane wave of 1 Pa amplitude, how fast does the air itself move?", a: ["343 m/s — with the wave", "About 2.4 mm/s, back and forth", "It does not move at all; only pressure changes", "It depends on the frequency"], c: 1, why: "<span class='m'>U = P/\\rho c = 1/413</span> m/s. The pattern travels at c; the particles only oscillate about their rest position, independent of frequency (the displacement does depend on frequency, <span class='m'>\\Xi = U/j\\omega</span>)." },
    { q: "Why does the derivation of the wave equation use γ (adiabatic) rather than the isothermal gas law?", a: ["Because sound only exists in hot gases", "Because compressions in sound are far too fast for heat to flow, so pressure rises more than isothermally", "Because γ makes the algebra simpler", "It does not; γ is a unit conversion"], c: 1, why: "In one period there is no time for heat exchange between compressed and rarefied regions, so <span class='m'>p = -\\gamma p_0\\,\\Delta V/V</span> and <span class='m'>c^2 = \\gamma p_0/\\rho_0</span>. The isothermal value would give 290 m/s instead of 343." },
    { q: "Two equal coherent sources with a 180° lag cancel; with 179° the sum is…", a: ["Also zero — a degree does not matter", "About 1.7 % of one source (8.7 mPa for 0.5 Pa each)", "Half of one source", "Twice one source"], c: 1, why: "<span class='m'>|1 + e^{-j179^\\circ}| = 2|\\cos 89.5^\\circ| = 0.0175</span>. Cancellation is exact only for exact antiphase and equal amplitudes — the reason noise cancelling is hard above a few hundred hertz." },
    { q: "The temperature of a hall rises from 15 to 32 °C. The speed of sound…", a: ["rises by 32/15 ≈ 2.1×", "rises by √(305/288) ≈ 1.029×", "falls, because warm air is thinner", "is unchanged; c depends only on pressure"], c: 1, why: "<span class='m'>c = \\sqrt{\\gamma R_s T}</span> with T in kelvin. Density and pressure both change with temperature, but their ratio only through T — and c does not depend on the static pressure at all." },
  ],
  "2": [
    { q: "At a rigid wall a sound wave has…", a: ["a pressure node and a velocity antinode", "a pressure antinode and a velocity node", "nodes of both", "antinodes of both"], c: 1, why: "The air cannot move into the wall, so U = 0 there; the incident and reflected pressures add (R = +1) to 2P_i. The first pressure node is λ/4 in front of the wall." },
    { q: "Why does the reflected wave carry a minus sign in the velocity but not in the pressure?", a: ["A convention with no physical meaning", "Velocity is a vector: the reflected wave's motion points the other way; pressure is a scalar", "Because reflection inverts pressure", "Because the reflected wave loses energy"], c: 1, why: "<span class='m'>U_x = (P_i e^{-jkx} - P_r e^{jkx})/\\rho c</span>. Each travelling wave has <span class='m'>U = \\pm P/\\rho c</span> according to its direction; at a rigid wall the two velocities cancel while the two pressures add." },
    { q: "Sound goes from air into water (R = 0.9994). The pressure in the water is…", a: ["0.06 % of the incident pressure", "about half of it", "about twice the incident pressure, though only 0.1 % of the power gets in", "equal to it"], c: 2, why: "<span class='m'>T_p = 1 + R \\approx 2</span>: pressure is continuous and the incident and reflected waves add at the interface. Power is another matter: <span class='m'>\\tau = 4Z_1Z_2/(Z_1+Z_2)^2 = 0.11\\,\\%</span>." },
    { q: "Close to a small source (kr ≪ 1) the particle velocity is…", a: ["equal to P/ρc, as in a plane wave", "larger than P/ρc and roughly 90° out of phase with the pressure", "zero", "smaller than P/ρc"], c: 1, why: "<span class='m'>U_r = (P/\\rho c)(1 + 1/jkr)</span>: the near-field term dominates for small kr, giving a large quadrature (reactive) velocity that carries no net power. At 250 Hz and 10 cm it is 2.4× the plane-wave value and 65° behind." },
    { q: "A closed–open tube of length L has resonances at…", a: ["nc/2L, all harmonics", "(2n−1)c/4L, odd harmonics only", "nc/L", "c/L only"], c: 1, why: "The closed end is a velocity node, the open end a pressure node: a quarter wavelength (plus whole half wavelengths) must fit. That is why a closed organ pipe sounds an octave below an open one of the same length and has a hollow, odd-harmonic timbre." },
  ],
  "3": [
    { q: "Two independent machines each give 75 dB at a point. Together they give…", a: ["150 dB", "81 dB", "78 dB", "75 dB"], c: 2, why: "Uncorrelated sources add their mean-square pressures: <span class='m'>10\\log(2) = 3</span> dB more. Only coherent sources (same tone, fixed phase) can reach +6 dB or cancel." },
    { q: "L_eq of a source that is on at 85 dB half the time and a 70 dB background otherwise is closest to…", a: ["77.5 dB, the average of the two", "82 dB", "85 dB", "70 dB"], c: 1, why: "<span class='m'>L_{eq} = 10\\log\\overline{p^2/p_{ref}^2}</span>: average the squared pressure, not the decibels. Half the time at <span class='m'>10^{8.5}</span> plus <span class='m'>10^{7}</span> gives <span class='m'>10\\log(0.5\\cdot 3.16\\times10^8 + 10^7) \\approx 82.3</span> dB." },
    { q: "A signal with period 1.3 ms has harmonics at 769 Hz, 1538, 2308, 3077 … The 2 kHz octave band (1414–2828 Hz) contains…", a: ["one component", "two components → the band level is the component level + 3 dB", "three components", "none"], c: 1, why: "1538 and 2308 Hz fall inside; components at different frequencies are uncorrelated, so two equal ones give +10 log 2 = 3 dB. The 4 kHz band gets four (+6 dB)." },
    { q: "White noise analysed in 1/3-octave bands shows a level that…", a: ["is flat", "rises 1 dB per band", "falls 3 dB per band", "rises 3 dB per band"], c: 1, why: "White noise has constant power per hertz, and each 1/3-octave band is <span class='m'>2^{1/3}</span> wider than the previous: <span class='m'>10\\log 2^{1/3} = 1</span> dB. Pink noise (constant power per octave) is flat in constant-percentage bands, which is why it sounds balanced." },
    { q: "A 100 Hz tone measures 70 dB unweighted. A-weighted it reads about…", a: ["70 dB(A)", "51 dB(A)", "89 dB(A)", "66 dB(A)"], c: 1, why: "The A-weighting response at 100 Hz is −19.1 dB (table 1.3.2): the meter mimics the ear's low-level insensitivity to bass. C-weighting would take off only 0.3 dB." },
  ],
};

QUIZZES["4"] = [
  {
    "q": "A piston converts mechanical to acoustic impedance by…",
    "a": [
      "dividing by S",
      "dividing by S²",
      "multiplying by S",
      "multiplying by S²"
    ],
    "c": 1,
    "why": "F = PS and Q = Sv, so Zm = F/v = S²P/Q = S²Za."
  },
  {
    "q": "Double the bottle volume while keeping the neck unchanged. Its resonance…",
    "a": [
      "doubles",
      "halves",
      "falls by a factor √2",
      "stays the same"
    ],
    "c": 2,
    "why": "Cavity stiffness is proportional to 1/V and f₀ is proportional to √K, hence f₀ ∝ 1/√V."
  },
  {
    "q": "Pressure and velocity are 90° apart. Mean intensity is…",
    "a": [
      "maximum",
      "zero",
      "negative",
      "equal to pressure squared divided by ρc"
    ],
    "c": 1,
    "why": "The average product is prms urms cos φ. At quadrature, stored energy returns each cycle."
  },
  {
    "q": "Air-to-water transmitted pressure nearly doubles. Transmitted intensity…",
    "a": [
      "quadruples",
      "doubles",
      "is only about 0.11% of incident intensity",
      "is unchanged"
    ],
    "c": 2,
    "why": "Intensity is pressure squared divided by characteristic impedance. Water has about 3584 times the impedance of air."
  },
  {
    "q": "90 dB incident SPL and 70 dB reflected SPL give absorption…",
    "a": [
      "0.1",
      "0.9",
      "0.99",
      "0.01"
    ],
    "c": 2,
    "why": "The reflected power fraction is 10^((70−90)/10) = 0.01, so α = 1 − 0.01."
  }
];

QUIZZES["5"] = [
  {
    "q": "A small monopole is moved right up against a large rigid wall (kh ≪ 1), keeping its volume velocity. Far-field SPL and sound power level change by…",
    "a": ["+3 dB and +3 dB", "+6 dB and +3 dB", "+6 dB and +6 dB", "+3 dB and 0 dB"],
    "c": 1,
    "why": "The in-phase image doubles the pressure (+6 dB) but only into a half space: 4× the intensity over half the area is 2× the power (+3 dB). The source really emits more power, because the image's pressure pushes on it in phase with its velocity."
  },
  {
    "q": "Two identical closed-box speakers side by side, same low-frequency signal. Compared with one box, the total power is…",
    "a": ["×2 (+3 dB)", "×4 (+6 dB)", "unchanged", "×8 (+9 dB)"],
    "c": 1,
    "why": "Close together they act as one source with 2Q, and power ∝ |Q|². Each box radiates twice its solo power because it also works against its neighbour's pressure. A wall gives only ×2, since the image does not radiate power of its own."
  },
  {
    "q": "At constant volume velocity, going down one octave changes a dipole's power by…",
    "a": ["−3 dB", "−6 dB", "−12 dB", "0 dB"],
    "c": 2,
    "why": "Dipole power ∝ h²k⁴|Q|², so halving f divides it by 16 (−12 dB). A monopole at constant Q loses 6 dB (∝ k²). That is why a bare driver without a box loses its bass."
  },
  {
    "q": "Why does the directivity factor of a small baffled piston tend to 2 rather than 1?",
    "a": ["The piston beams forward at low frequency", "All its power goes into a half space, so the on-axis intensity is twice that of an omnidirectional source of the same power", "The baffle doubles the volume velocity", "R₁ tends to 2 at low ka"],
    "c": 1,
    "why": "Q(f) compares the on-axis intensity with that of an omnidirectional source of equal power. Half the solid angle means double the intensity: Q = 2, DI = 3 dB. At high ka it grows as (ka)²."
  },
  {
    "q": "A baffled piston's first directivity null appears once…",
    "a": ["ka > 1", "ka > 1.62", "ka > 3.83", "ka > 2π"],
    "c": 2,
    "why": "The far-field directivity is 2J₁(ka sin θ)/(ka sin θ), whose first zero is at 3.83. Since sin θ ≤ 1, the null exists only for ka > 3.83. 1.62 is the −3 dB point; 2π is the condition for the first on-axis near-field minimum."
  }
];

QUIZZES["6"] = [
  {
    "q": "A microphone sits exactly in the centre of a rectangular room. Which mode can it not hear?",
    "a": ["(2,0,0)", "(1,0,0)", "(0,0,2)", "(2,2,0)"],
    "c": 1,
    "why": "At the centre each factor is cos(nπ/2), which is zero for odd n: (1,0,0) has a nodal plane through the middle. Only modes with all indices even have a maximum there. A corner hears every mode."
  },
  {
    "q": "The modal density of a room at high frequency grows as…",
    "a": ["V·f", "V·f²", "f³ only, independent of V", "S·f"],
    "c": 1,
    "why": "dN/df ≈ 4πVf²/c³. That is why the modes merge above the Schroeder frequency, f_S ≈ 2000√(T/V), and statistics take over."
  },
  {
    "q": "In a diffuse field with mean-square pressure p², the power hitting 1 m² of wall is…",
    "a": ["p²/ρc", "p²/2ρc", "p²/4ρc", "4p²/ρc"],
    "c": 2,
    "why": "Half of the waves travel away from the wall, and the rest arrive obliquely with an average cos θ of ½. Together: a quarter of the normal-incidence plane-wave value."
  },
  {
    "q": "A reverberant room: halve the absorption area A. The reverberant level and T change by…",
    "a": ["+3 dB, T doubles", "+6 dB, T doubles", "+3 dB, T unchanged", "0 dB, T doubles"],
    "c": 0,
    "why": "p² = 4Pρc/A doubles (+3 dB), and T = 0.16V/A doubles. The direct field near the source does not change at all."
  },
  {
    "q": "A source is on for 5 minutes in every 15. Its L_eq relative to its level while on is…",
    "a": ["−10 dB", "−4.8 dB", "−3 dB", "the same; dB do not average"],
    "c": 1,
    "why": "Average the mean-square pressure: one third of the time gives 10 log(1/3) = −4.8 dB. That is Problem 3.1: 95.8 → 91.0 dB."
  }
];

QUIZZES["7"] = [
  {
    "q": "A 50 mm porous layer mounted directly on a concrete wall absorbs well from about…",
    "a": ["430 Hz", "860 Hz", "1.7 kHz", "3.4 kHz"],
    "c": 2,
    "why": "The layer needs to reach the first velocity maximum, λ/4 out from the wall: f ≈ c/4d = 344/0.2 = 1.7 kHz. Moving it 5 cm out on an air gap halves that, at no cost in material."
  },
  {
    "q": "You double the cavity depth behind a limp panel absorber. Its peak frequency…",
    "a": ["halves", "falls by √2", "doubles", "stays the same"],
    "c": 1,
    "why": "The cavity stiffness per area is ρc²/L, so f_r ∝ 1/√(mL). Doubling L divides f_r by √2."
  },
  {
    "q": "Z_n = 500 + j1000 N·s/m³. Someone puts r = 500, x = 1000 straight into the random-incidence formula and gets 0.0032. The right value is about…",
    "a": ["0.0032 — the formula is fine", "0.45", "0.53", "0.95"],
    "c": 2,
    "why": "The Paris formula takes the normalised impedance ζ = Z/ρc = 1.21 + j2.42, giving α_r ≈ 0.53. 0.45 is the normal-incidence value."
  },
  {
    "q": "A standing-wave tube shows P_max/P_min = 3. The normal-incidence absorption coefficient is…",
    "a": ["0.33", "0.50", "0.75", "0.89"],
    "c": 2,
    "why": "|R| = (n−1)/(n+1) = 0.5, so α₀ = 1 − 0.25 = 0.75. n is a pressure ratio; if it were given in dB you would first convert with 10^(L/20)."
  },
  {
    "q": "A 10 m² sample measures α_s = 1.1 at 315 Hz in a reverberation room. Most likely…",
    "a": ["the measurement is wrong", "edge diffraction: the sample absorbs more than its geometric area", "the room is not diffuse enough, so α should be capped at 1", "the sample transmits sound"],
    "c": 1,
    "why": "Diffraction at the sample edges draws in energy from around it, most at low frequency where the sample is not large compared with λ. Absorber spread in patches beats the same amount in one block."
  }
];
