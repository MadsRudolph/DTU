/* The Sound Bench — problem sheets with solutions. Weeks 1–2 follow the official
   solution sets; week 3 has the sheet's printed answers with the working. */
"use strict";

window.PROBLEMS = {
  "1": [
    { id: "1.1–1.2", title: "A 1 Pa, 1 kHz plane wave", tag: "34.3 cm · 18.3 rad/m · 2.42 mm/s · 0.385 µm",
      given: `A harmonic plane wave with sound pressure amplitude 1 Pa and frequency 1 kHz at normal ambient conditions (20 °C, 101.3 kPa). 1.1 Wavelength and wavenumber. 1.2 Particle velocity amplitude and particle displacement amplitude.`,
      hint: `<span class="m">\\lambda = c/f</span>, <span class="m">k = 2\\pi/\\lambda</span>; then <span class="m">U = P/\\rho c</span> and integrate once for the displacement: <span class="m">\\Xi = U/j\\omega</span>.`,
      sol: `<div class="M">\\lambda = \\frac{c}{f} = \\frac{343}{1000} = 0.343\\ \\text{m} = 34.3\\ \\text{cm}, \\qquad k = \\frac{2\\pi f}{c} = \\frac{2\\pi}{\\lambda} = 18.3\\ \\text{rad/m}</div>
<div class="M">U = \\frac{|P|}{\\rho c} = \\frac{1}{413} = 2.42\\ \\text{mm/s}, \\qquad \\Xi = \\int U e^{j(\\omega t - kx)}dt = \\frac{U}{j\\omega} \\;\\Rightarrow\\; |\\Xi| = \\frac{U}{2\\pi f} = 0.385\\ \\mu\\text{m}</div>
<p>The displacement is inversely proportional to frequency — which is why the cone of a subwoofer visibly moves while a tweeter's does not.</p>`, bench: "#bench-wave", benchLabel: "the plane-wave bench starts on exactly this wave" },
    { id: "2.1–2.4", title: "Two identical loudspeakers, one tone, four phase lags", tag: "1 Pa · 0.71 Pa · 0 Pa · 8.7 mPa",
      given: `Each speaker alone gives 0.5 Pa at the listening point; same tone, same distance, no reflections. Total amplitude when driven in phase; with a 90° lag in one channel; 180°; 179°.`,
      hint: `Take speaker 1 as the phase reference: <span class="m">P_1 = 0.5</span>, <span class="m">P_2 = 0.5\\,e^{-j\\theta}</span>. Add, then take the magnitude.`,
      sol: `<div class="M">P_{tot} = p_i\\left(1 + e^{j\\varphi}\\right), \\qquad |P_{tot}| = p_i\\sqrt{(1+\\cos\\varphi)^2 + \\sin^2\\varphi} = 2p_i\\left|\\cos\\tfrac{\\varphi}{2}\\right|</div>
<div class="table-wrap"><table><tr><th>lag</th><th>1 + e^{jφ}</th><th>|P_tot|</th></tr><tr><td>0°</td><td>2</td><td>1 Pa</td></tr><tr><td>90°</td><td>1 + j</td><td>√2 · 0.5 = 0.71 Pa</td></tr><tr><td>180°</td><td>0</td><td>0 Pa — destructive interference</td></tr><tr><td>179°</td><td>0.0002 + j0.0175</td><td>8.7 mPa</td></tr></table></div>
<p>One degree short of antiphase leaves 1.7 % of one source: cancellation is only perfect when amplitudes and phases match exactly. The phasor diagrams in the solution set show the two arrows and their sum for each case.</p>`, bench: "#bench-phasors", benchLabel: "phasor bench: chips for 0°, 90°, 179°, 180°" },
    { id: "3.1", title: "Hearing-aid speaker in the ear canal", tag: "2.84 Pa",
      given: `The loudspeaker of a hearing aid makes the fractional volume of the ear-canal cavity vary harmonically with amplitude ΔV/V = 0.002 %. Assuming adiabatic compression, what is the sound pressure amplitude?`,
      hint: `<span class="m">p/p_0 = -\\gamma\\,\\Delta V/V</span>. Convert the percentage first.`,
      sol: `<div class="M">|p| = \\gamma p_0 \\left|\\frac{\\Delta V}{V}\\right| = 1.401 \\times 101.3\\times10^{3} \\times \\frac{0.002}{100} = 2.84\\ \\text{Pa}</div>
<p>The relative pressure change is γ times larger than the relative volume change and of opposite sign: squeezing the cavity raises the pressure. 2.84 Pa peak is about 100 dB — a hearing aid does not need to move much air in a sealed canal.</p>`, bench: null },
    { id: "4.1–4.2", title: "Church organ, summer and winter", tag: "×1.029 · 106.9 Hz (a quarter tone flat)",
      given: `The church is 15 °C in winter and 32 °C in summer. 4.1 Ratio of the speed of sound in summer to winter. 4.2 An open pipe's fundamental has L = λ/2; it is tuned to 110 Hz in summer. Its frequency in winter?`,
      hint: `<span class="m">c \\propto \\sqrt{T}</span> with T in kelvin; the pipe length does not change, so <span class="m">f_0 = c/2L \\propto c</span>.`,
      sol: `<div class="M">\\frac{c_s}{c_w} = \\sqrt{\\frac{T_s}{T_w}} = \\sqrt{\\frac{273 + 32}{273 + 15}} = 1.029, \\qquad f_w = f_s\\,\\frac{c_w}{c_s} = \\frac{110}{1.029} = 106.9\\ \\text{Hz}</div>
<p>A factor 1.029 is <span class="m">2^{1/24}</span>, since <span class="m">\\log_2 1.029 \\approx 1/24</span>: one twenty-fourth of an octave, half a semitone — the organ drops a quarter tone in winter.</p>`, bench: "#bench-speed", benchLabel: "speed-of-sound bench: slide the temperature" },
  ],
  "2": [
    { id: "1", title: "Standing-wave tube, rigid end, 1 kHz", tag: "minima at 8.6, 25.7, 42.9 cm …",
      given: `A tube is driven at 1 kHz by a loudspeaker at one end and terminated rigidly at the other. At which distances from the rigid end is the pressure very small?`,
      hint: `The wall is a pressure antinode. The first node is a quarter wavelength away.`,
      sol: `<p>The incident wave must travel half a wavelength before it is back at the same point, so at a quarter wavelength from the wall incident and reflected waves are in antiphase with equal amplitude and cancel: destructive interference.</p>
<div class="M">\\lambda = \\frac{343}{1000} = 34.3\\ \\text{cm} \\;\\Rightarrow\\; d = \\frac{\\lambda}{4}, \\frac{3\\lambda}{4}, \\frac{5\\lambda}{4}, \\ldots = 8.6,\\ 25.7,\\ 42.9\\ \\text{cm}, \\ldots</div>`, bench: "#bench-standing", benchLabel: "standing-wave bench: rigid wall preset, read the minima" },
    { id: "2", title: "Trumpet filled with helium", tag: "fundamental ×2.91 (an octave and a fifth)",
      given: `A trumpet player fills the instrument with helium (c = 1000 m/s). What happens to the lowest resonance frequency?`,
      hint: `Every resonance is proportional to c at fixed geometry: the wavelength cancels in the ratio.`,
      sol: `<div class="M">\\frac{f_{He}}{f_{air}} = \\frac{c_{He}}{c_{air}} = \\frac{1000}{343} = 2.91, \\qquad n = 12\\log_2(2.91) = 12\\,\\frac{\\log_{10} 2.91}{\\log_{10} 2} \\approx 18.5\\ \\text{semitones}</div>
<p>Twelve semitones are an octave, seven a fifth: the trumpet plays about an octave and a fifth higher. No instrument length is needed — the sheet gives none.</p>`, bench: "#bench-tubemodes", benchLabel: "tube bench: switch the gas to helium" },
    { id: "3.1–3.3", title: "Air–water and water–air", tag: "R = 0.99944 · −0.99944 · attenuation 0.5 and 1793",
      given: `Plane wave at normal incidence. 3.1 Reflection coefficient from air onto water (c_water = 1480 m/s). 3.2 From water onto air. 3.3 The attenuation factor P_i/P_t in both directions.`,
      hint: `<span class="m">Z_{air} = 413</span>, <span class="m">Z_{water} = 1000 \\times 1480 = 1.48\\times10^6</span> Pa·s/m. Two continuity conditions at the interface.`,
      sol: `<div class="M">R_{air \\to water} = \\frac{Z_w - Z_a}{Z_w + Z_a} = 0.99944, \\qquad R_{water \\to air} = \\frac{Z_a - Z_w}{Z_a + Z_w} = -0.99944</div>
<p>Almost total reflection either way, with opposite polarity. For the transmitted pressure combine <span class="m">P_i + P_r = P_t</span> and <span class="m">(P_i - P_r)/Z_1 = P_t/Z_2</span>:</p>
<div class="M">\\frac{P_i}{P_t} = \\frac{Z_1 + Z_2}{2Z_2} \\;\\Rightarrow\\; \\text{air} \\to \\text{water}: \\frac{Z_a + Z_w}{2Z_w} \\approx \\frac12 \\ (\\text{amplification, } -6\\ \\text{dB}); \\qquad \\text{water} \\to \\text{air}: \\frac{Z_w + Z_a}{2Z_a} = 1793\\ (65\\ \\text{dB})</div>
<p>An attenuation factor of 0.5 means the pressure in the water is <em>twice</em> the incident pressure in air. The power transmitted is <span class="m">\\tau = 4Z_1Z_2/(Z_1+Z_2)^2 = 0.11\\,\\%</span> in both directions. With ρ_water = 998.2 the official set gets 1789; with the rounded 3600:1 impedance ratio, 1820.</p>`, bench: "#bench-interface", benchLabel: "interface bench: air → water, then swap" },
    { id: "4.1–4.3", title: "Small source at 250 Hz, 10 cm away", tag: "5 Pa · 29 mm/s · 1.14 rad = 65.4°",
      given: `An omnidirectional source at 250 Hz gives 0.5 Pa at 1 m in a free field. 4.1 Pressure amplitude at 10 cm. 4.2 Particle velocity amplitude there. 4.3 Phase angle of p/u there.`,
      hint: `<span class="m">P = A e^{-jkr}/r</span> with A fixed by the 1 m value. For the velocity keep the <span class="m">1/(jkr)</span> term.`,
      sol: `<div class="M">A = 0.5\\ \\text{Pa·m} \\;\\Rightarrow\\; |P(0.1)| = \\frac{0.5}{0.1} = 5\\ \\text{Pa}, \\qquad kr = \\frac{2\\pi\\cdot 250}{343}\\cdot 0.1 = 0.458</div>
<div class="M">|U_r| = \\frac{|P|}{\\rho c}\\left|1 + \\frac{1}{jkr}\\right| = \\frac{5}{413}\\sqrt{1 + \\frac{1}{(kr)^2}} = 29\\ \\text{mm/s} \\quad (\\text{plane-wave guess: } 12\\ \\text{mm/s})</div>
<div class="M">\\arg\\frac{P}{U_r} = -\\arg\\left(1 + \\frac{1}{jkr}\\right) = \\arctan\\frac{1}{kr} = \\arctan\\frac{343}{2\\pi\\cdot 250\\cdot 0.1} = 1.14\\ \\text{rad} = 65.4^\\circ</div>
<p>Pressure leads the outward velocity by 65°: at kr = 0.46 the field is mostly reactive, and the velocity is 2.4× what the plane-wave relation would give.</p>`, bench: "#bench-spherical", benchLabel: "spherical bench starts on this problem" },
    { id: "5", title: "Verify the plane wave in the wave equation", tag: "both sides give −k²·p; k = ω/c",
      given: `Show that <span class="m">\\hat p = A e^{j(\\omega t - kx)}</span> solves <span class="m">\\partial^2 p/\\partial x^2 = c^{-2}\\,\\partial^2 p/\\partial t^2</span>.`,
      hint: `Each derivative pulls down a factor: <span class="m">-jk</span> for x, <span class="m">j\\omega</span> for t.`,
      sol: `<div class="M">\\frac{\\partial^2 \\hat p}{\\partial x^2} = (-jk)^2 A e^{j(\\omega t - kx)} = -k^2\\hat p, \\qquad \\frac{1}{c^2}\\frac{\\partial^2 \\hat p}{\\partial t^2} = \\frac{(j\\omega)^2}{c^2}\\hat p = -\\frac{\\omega^2}{c^2}\\hat p</div>
<p>Equal for all x and t exactly when <span class="m">k = \\omega/c</span> — the dispersion relation of sound: no dispersion, every frequency travels at the same speed.</p>`, bench: null },
  ],
  "3": [
    { id: "1.1", title: "A 0.02 Pa tone, then a second tone 100 Hz higher", tag: "57 dB · 60 dB",
      given: `A pure tone has amplitude 0.02 Pa. 1.1 Its sound pressure level. 1.2 A second tone of the same amplitude, 100 Hz higher, is added: the level with both present.`,
      hint: `Peak → rms is ÷√2. Different frequencies are uncorrelated: add mean squares.`,
      sol: `<div class="M">p_{rms} = \\frac{0.02}{\\sqrt2} = 14.1\\ \\text{mPa}, \\qquad L_p = 20\\log\\frac{0.01414}{2\\times10^{-5}} = 57.0\\ \\text{dB}</div>
<div class="M">L_{tot} = 10\\log\\left(10^{5.7} + 10^{5.7}\\right) = 57 + 3 = 60\\ \\text{dB}</div>
<p>Two tones of different frequency never stay in phase, so their cross term averages out: the mean squares add, +3 dB. Had it been the <em>same</em> frequency, the answer would depend on the phase (54 to 63 dB).</p>`, bench: "#bench-levels", benchLabel: "levels bench: two equal sources, uncorrelated" },
    { id: "1.2", title: "Two loudspeakers at 90 dB each", tag: "96 dB · 90 dB · 93 dB",
      given: `Each speaker alone gives 90 dB at the listening point. Level when driven in phase with the same tone; with a 120° lag in one channel; with two different tones of the same level.`,
      hint: `Same tone → phasors: <span class="m">|1 + e^{-j\\theta}| = 2|\\cos(\\theta/2)|</span>. Different tones → squares.`,
      sol: `<div class="M">\\text{in phase: } 20\\log 2 = +6 \\Rightarrow 96\\ \\text{dB}; \\qquad 120^\\circ: 2\\cos 60^\\circ = 1 \\Rightarrow 90\\ \\text{dB}; \\qquad \\text{different tones: } 10\\log 2 = +3 \\Rightarrow 93\\ \\text{dB}</div>
<p>At 120° the two phasors and their sum form an equilateral triangle: the total has exactly the amplitude of one source.</p>`, bench: "#bench-levels", benchLabel: "levels bench: coherent mode, θ = 120°" },
    { id: "3", title: "Engine harmonics in octave bands", tag: "1 kHz band 60 dB · 2 kHz 63 dB · 4 kHz 66 dB",
      given: `A rotating engine gives a periodic signal with period 1.3 ms. The fundamental and the first six overtones all have level 60 dB; higher harmonics are negligible. Find the total level in each standard octave band that contains at least one component.`,
      hint: `<span class="m">f_0 = 1/T</span>; octave edges are <span class="m">f_c/\\sqrt2</span> and <span class="m">f_c\\sqrt2</span>; n equal lines in a band → +10 log n.`,
      sol: `<div class="M">f_0 = \\frac{1}{1.3\\ \\text{ms}} = 769\\ \\text{Hz}: \\quad 769,\\ 1538,\\ 2308,\\ 3077,\\ 3846,\\ 4615,\\ 5385\\ \\text{Hz}</div>
<div class="table-wrap"><table><tr><th>octave band</th><th>edges</th><th>components</th><th>level</th></tr><tr><td>1 kHz</td><td>707–1414 Hz</td><td>769</td><td>60 dB</td></tr><tr><td>2 kHz</td><td>1414–2828 Hz</td><td>1538, 2308</td><td>60 + 10 log 2 = 63 dB</td></tr><tr><td>4 kHz</td><td>2828–5657 Hz</td><td>3077, 3846, 4615, 5385</td><td>60 + 10 log 4 = 66 dB</td></tr></table></div>
<p>Components at different frequencies are uncorrelated, so the band level is the mean-square sum. The total over all bands is 60 + 10 log 7 = 68.5 dB.</p>`, bench: "#bench-octave", benchLabel: "octave bench starts on T = 1.3 ms, 7 harmonics" },
    { id: "4", title: "Bandwidth of a 1/12-octave filter at 1 kHz", tag: "57.8 Hz",
      given: `Some analyses use 1/12-octave bands. Bandwidth of such a filter centred at 1 kHz?`,
      hint: `<span class="m">f_u/f_l = 2^{1/12}</span> with <span class="m">f_c = \\sqrt{f_l f_u}</span>, so the edges are <span class="m">f_c\\,2^{\\pm 1/24}</span>.`,
      sol: `<div class="M">BW = f_c\\left(2^{1/24} - 2^{-1/24}\\right) = 1000\\,(1.0293 - 0.9715) = 57.8\\ \\text{Hz}</div>
<p>About 5.8 % of the centre frequency — half a semitone wide. For comparison a 1/3-octave at 1 kHz is 232 Hz, an octave 707 Hz.</p>`, bench: "#bench-octave", benchLabel: "octave bench: the 1/n chips at the bottom" },
    { id: "5", title: "Machine B behind machine A", tag: "78.3 dB",
      given: `Machine A alone: 75 dB. A and B together: 80 dB. Level of B alone (uncorrelated sources)?`,
      hint: `Subtract mean squares, not decibels.`,
      sol: `<div class="M">L_B = 10\\log\\left(10^{8.0} - 10^{7.5}\\right) = 10\\log\\left(10^8\\,(1 - 10^{-0.5})\\right) = 80 + 10\\log 0.684 = 78.3\\ \\text{dB}</div>
<p>The same arithmetic corrects any measurement for a steady background: reliable only when the background is ≥ 3 dB below the total, and hardly needed once it is 10 dB below.</p>`, bench: "#bench-levels", benchLabel: "levels bench: background correction, 80 and 75" },
    { id: "6 · Matlab", title: "Build a sound level meter in Matlab", tag: "74 dB · 76.5 dB · 85.0 / 82 dB · 69.9 dB(A) · 74.4 / 82.0 / 85.8 dB",
      given: `A: L_eq of a whole file and of an interval. B: exponential averaging with τ = 125 ms and 1 s. C: A-weighting with Afilter_44k1. D: 1/n-octave band levels with n_octave and the total from the bands. E (Windows): live recording. Check values are in the guide.`,
      hint: `<span class="m">p_{rms} = \\sqrt{\\text{mean}(p^2)}</span> over the samples; <span class="m">L = 20\\log(p_{rms}/20\\,\\mu\\text{Pa})</span>. For B use the one-pole recursion rather than a convolution.`,
      sol: `<p><b>A1.</b> <span class="mono">Leq = 20*log10(sqrt(mean(sig.^2))/20e-6)</span>. Checks: 440HzSine.wav → 74 dB, ToneComplex.wav → 76.5 dB. <b>A2.</b> Index the interval by samples, <span class="mono">n = round(t*fs)</span>: NonstationaryNoise.wav gives 85.0 dB over 3–9 s and 82 dB overall.</p>
<p><b>B1.</b> <span class="mono">alpha = exp(-1/(tau*fs)); y(1) = sig(1)^2; y(n) = alpha*y(n-1) + (1-alpha)*sig(n)^2; L = 10*log10(y/20e-6^2)</span> — an IIR filter with B = [1−α], A = [1 −α]; <span class="mono">filter()</span> does it in one line. Fast follows the on/off source, Slow smooths it, and the L_eq of the whole file (82.1 dB, 74.4 dB(A)) is the horizontal line.</p>
<p><b>C1.</b> Filter first, then the same rms code: <span class="mono">sig_A = Afilter_44k1(sig)</span>; the 440 Hz sine drops from 74 to 69.9 dB(A) (the A-curve is −4.1 dB at 440 Hz).</p>
<p><b>D1–D3.</b> For each centre frequency <span class="mono">[B,A] = n_octave(fc,n,fs); band = filter(B,A,sig)</span>, then rms per band. Summing the band mean squares (Parseval) must give back the broadband level: 74.4, 82.0 and 85.8 dB for the three 30 s parts of DeepestBluesareBlack.wav. Plot the 1/3-octave levels and compare with the slides.</p>
<p><b>E.</b> Needs the Data Acquisition Toolbox and the Windows sound-card support package; levels are uncalibrated, so judge the spectral balance, not the absolute number.</p>`, bench: "#bench-timeweight", benchLabel: "time-weighting bench shows what B1 should look like" },
  ],
};

window.PROBLEMS["4"] = [
  {
    "id": "1",
    "title": "Problem 1 — Bottle resonance",
    "tag": "334 Hz",
    "given": "<p><b>Given:</b> <span class=\"m\">V=400\\ \\mathrm{ml}=4.00\\times10^{-4}\\ \\mathrm{m^3}</span>, neck diameter <span class=\"m\">d=20\\ \\mathrm{mm}=0.020\\ \\mathrm m</span>, effective neck length <span class=\"m\">l_{\\rm eff}=0.021\\ \\mathrm m</span>.</p>",
    "hint": "<p>The neck is an acoustic mass and the enclosed air is a compliance. Find the neck area, then set their reactances equal.</p>",
    "sol": "<div class=\"M\">S=\\pi(d/2)^2=\\pi(0.010)^2=3.1416\\times10^{-4}\\ \\mathrm{m^2}.</div>\n<div class=\"M\">M_a=\\frac{\\rho l_{\\rm eff}}S=80.21\\ \\mathrm{kg/m^4},\\qquad\nK_a=\\frac{\\rho c^2}V=3.5295\\times10^8\\ \\mathrm{N/m^5}.</div>\n<div class=\"M\">f_0=\\frac1{2\\pi}\\sqrt{\\frac{K_a}{M_a}}\n=\\frac{343}{2\\pi}\\sqrt{\\frac{3.1416\\times10^{-4}}{(4.00\\times10^{-4})(0.021)}}\n=\\boxed{333.8\\ \\mathrm{Hz}}.</div>\nA bigger cavity lowers the resonance; a bigger neck area raises it. The wavelength is approximately 1.03 m, much longer than the neck. The given length is already effective, so no extra end correction is needed.",
    "bench": "#bench-helmholtz",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "2",
    "title": "Problem 2 — Power carried by a plane wave",
    "tag": "1.54 mW",
    "given": "<p><b>Given:</b> <span class=\"m\">L_p=82\\ \\mathrm{dB}</span> and perpendicular area <span class=\"m\">S=10\\ \\mathrm{m^2}</span>.</p>",
    "hint": "<p>Convert SPL to RMS pressure, then use the progressive-plane-wave intensity and multiply by area.</p>",
    "sol": "<div class=\"M\">p_{\\rm rms}=p_0\\,10^{L_p/20}=20\\times10^{-6}\\,10^{82/20}=0.25179\\ \\mathrm{Pa}.</div>\n<div class=\"M\">I=\\frac{p_{\\rm rms}^2}{\\rho c}=\\frac{0.25179^2}{413}=1.5350\\times10^{-4}\\ \\mathrm{W/m^2}.</div>\n<div class=\"M\">W=IS=\\boxed{1.535\\ \\mathrm{mW}\\approx1.54\\ \\mathrm{mW}}.</div>\nNo extra factor <span class=\"m\">1/2</span>: the pressure is already RMS. The area must be normal to propagation, as stated.",
    "bench": "#bench-power4",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "3.1–3.2",
    "title": "Problem 3 — Intensity transmission between water and air",
    "tag": "29.5 dB each way",
    "given": "<p><b>Given/recall from Week 2:</b> <span class=\"m\">z_a=413\\ \\mathrm{Pa\\,s/m}</span>, <span class=\"m\">z_w=1000\\times1480=1.48\\times10^6\\ \\mathrm{Pa\\,s/m}</span>. Lossless media, plane wave, normal incidence.</p>",
    "hint": "<p><span class=\"m\">I=p_{\\rm rms}^2/z</span>. The pressures on opposite sides have different pressure-to-velocity ratios, so squaring the pressure transmission coefficient is not enough.</p>",
    "sol": "<p>Pressure continuity and normal-velocity continuity give <div class=\"M\">P_i+P_r=P_t,\\qquad\\frac{P_i-P_r}{z_1}=\\frac{P_t}{z_2},</div> <div class=\"M\">R=\\frac{z_2-z_1}{z_2+z_1},\\qquad T_p=\\frac{P_t}{P_i}=\\frac{2z_2}{z_1+z_2}.</div> Thus <div class=\"M\">\\tau=\\frac{I_t}{I_i}=|T_p|^2\\frac{z_1}{z_2}=\\frac{4z_1z_2}{(z_1+z_2)^2}.</div></p><h4>3.1 Water to air</h4><div class=\"M\">T_{p,w\\to a}=\\frac{826}{1480413}=0.00055795,</div>\n<div class=\"M\">\\tau=(0.00055795)^2\\frac{1.48\\times10^6}{413}=0.0011156.</div>\nDefine positive attenuation as incident over transmitted intensity:\n<div class=\"M\">A_I=10\\log_{10}\\frac{I_i}{I_t}=-10\\log_{10}\\tau=\\boxed{29.525\\ \\mathrm{dB}\\approx30\\ \\mathrm{dB}}.</div>\nIf reporting transmitted minus incident intensity level instead, the result is <b>−29.525 dB</b>.<h4>3.2 Air to water</h4><div class=\"M\">T_{p,a\\to w}=\\frac{2(1.48\\times10^6)}{1480413}=1.999442,</div>\n<div class=\"M\">\\tau=(1.999442)^2\\frac{413}{1.48\\times10^6}=0.0011156,</div>\n<div class=\"M\">\\boxed{A_I=29.525\\ \\mathrm{dB}\\approx30\\ \\mathrm{dB}}.</div>\nThe expression is symmetric in <span class=\"m\">z_1,z_2</span>: intensity transmission is the same in either direction. Only <b>0.1116%</b> of the incident power crosses the interface.<p><b>Compare Week 2:</b> the pressure attenuation <span class=\"m\">20\\log_{10}|P_i/P_t|</span> is about <b>65.1 dB</b> water-to-air but <b>−6.02 dB</b> air-to-water. The latter means transmitted pressure nearly doubles. This does not mean energy doubles: water's very large impedance makes the transmitted particle velocity tiny. The missing transmitted energy is reflected, not absorbed by this ideal interface.</p>",
    "bench": "#bench-transmission4",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "4.1–4.2",
    "title": "Problem 4 — Standing-wave tube",
    "tag": "0.686 · 0.863 µW · 59.36 dB",
    "given": "<p><b>Given:</b> tube length 1 m, area <span class=\"m\">S=0.01\\ \\mathrm{m^2}</span>, <span class=\"m\">f=1\\ \\mathrm{kHz}</span>, <span class=\"m\">L_{\\max}=85\\ \\mathrm{dB}</span>, <span class=\"m\">L_{\\min}=74\\ \\mathrm{dB}</span>. Assume a lossless plane-wave tube and an absorbing termination with no transmitted power.</p>",
    "hint": "<p>The difference of levels gives a pressure ratio. From the extrema recover incident and reflected pressures, then subtract their powers.</p>",
    "sol": "<h4>4.1 Absorption coefficient</h4><div class=\"M\">s=10^{(85-74)/20}=3.54813,</div>\n<div class=\"M\">|R|=\\frac{s-1}{s+1}=0.56026,</div>\n<div class=\"M\">\\boxed{\\alpha=1-|R|^2=0.68611\\approx0.69}.</div>\nUsing <span class=\"m\">10^{11/10}</span> would give an intensity ratio where a pressure ratio is required.<h4>4.2 Absorbed power and power level</h4><div class=\"M\">p_{\\max,\\rm rms}=20\\times10^{-6}10^{85/20}=0.355656\\ \\mathrm{Pa},</div>\n<div class=\"M\">p_{\\min,\\rm rms}=20\\times10^{-6}10^{74/20}=0.100237\\ \\mathrm{Pa}.</div>\n<div class=\"M\">p_{i,\\rm rms}=\\frac{p_{\\max}+p_{\\min}}2=0.227947\\ \\mathrm{Pa},\\qquad\np_{r,\\rm rms}=\\frac{p_{\\max}-p_{\\min}}2=0.127709\\ \\mathrm{Pa}.</div>\n<div class=\"M\">W_i=\\frac{S p_i^2}{413}=1.2581\\ \\mu\\mathrm W,\\qquad W_r=\\frac{S p_r^2}{413}=0.39491\\ \\mu\\mathrm W.</div>\n<div class=\"M\">W_{\\rm abs}=W_i-W_r=\\alpha W_i=\\frac{S p_{\\max}p_{\\min}}{413}\n=\\boxed{0.8632\\ \\mu\\mathrm W}.</div>\n<div class=\"M\">L_W=10\\log_{10}\\frac{0.8632\\times10^{-6}}{10^{-12}}=\\boxed{59.36\\ \\mathrm{dB}\\approx59.4\\ \\mathrm{dB}}.</div>\nThe sheet's <span class=\"m\">0.87\\ \\mu\\mathrm W</span> differs only by rounding/constants. Tube length and frequency are not needed once both extrema are known; they determine their spacing. Here <span class=\"m\">\\lambda=0.343</span> m, with adjacent maximum/minimum separated by <span class=\"m\">\\lambda/4=0.08575</span> m.",
    "bench": "#bench-absorption4",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "5.1–5.2",
    "title": "Problem 5 — Loudspeaker cone and sealed cabinet",
    "tag": "59.1 Hz · 140.85 dB",
    "given": "<p><b>Given:</b> cone diameter <span class=\"m\">d=0.150\\ \\mathrm m</span>, moving mass <span class=\"m\">M=0.020\\ \\mathrm{kg}</span>, cabinet volume <span class=\"m\">V=0.016\\ \\mathrm{m^3}</span>. Ignore suspension stiffness and external radiation impedance. Treat the cone as a rigid piston and the cavity as a uniform adiabatic compliance.</p>",
    "hint": "<p>Convert the cone's mechanical mass to the acoustic side using <span class=\"m\">S^2</span>. For internal pressure, cone displacement changes the volume by <span class=\"m\">Sx</span>.</p>",
    "sol": "<h4>5.1 Acoustic impedances and natural frequency</h4><div class=\"M\">S=\\pi(0.075)^2=0.0176715\\ \\mathrm{m^2},\\qquad M_a=\\frac M{S^2}=64.04499\\ \\mathrm{kg/m^4}.</div>\n<div class=\"M\">\\boxed{Z_{a,\\rm cone}=j\\omega\\frac M{S^2}=j\\omega(64.045)\\ \\mathrm{N\\,s/m^5}}.</div>\n<div class=\"M\">K_a=\\frac{\\rho c^2}V=\\frac{1.2(343)^2}{0.016}=8.823675\\times10^6\\ \\mathrm{N/m^5},</div>\n<div class=\"M\">\\boxed{Z_{a,V}=\\frac{K_a}{j\\omega}=\\frac{8.823675\\times10^6}{j\\omega}\\ \\mathrm{N\\,s/m^5}}.</div>\n<div class=\"M\">f_0=\\frac1{2\\pi}\\sqrt{\\frac{K_a}{M_a}}=\\boxed{59.07\\ \\mathrm{Hz}\\approx59\\ \\mathrm{Hz}}.</div>\nMechanical cross-check: <span class=\"m\">K_m=S^2K_a\\approx2755.5\\ \\mathrm{N/m}</span>, so <span class=\"m\">f_0=\\sqrt{K_m/M}/(2\\pi)</span> gives the same result.<h4>5.2 Internal SPL at the displacement limit</h4><p>The specified <b>4 mm peak-to-peak</b> means <span class=\"m\">x_{\\rm pk}=2\\ \\mathrm{mm}=0.002\\ \\mathrm m</span>. <div class=\"M\">|\\Delta V|_{\\rm pk}=Sx_{\\rm pk}=3.53429\\times10^{-5}\\ \\mathrm{m^3}.</div> Adiabatic compression gives <span class=\"m\">p=-\\rho c^2\\Delta V/V</span>, so its amplitude is <div class=\"M\">p_{\\rm pk}=\\frac{\\rho c^2Sx_{\\rm pk}}V=311.85\\ \\mathrm{Pa},\\qquad p_{\\rm rms}=\\frac{311.85}{\\sqrt2}=220.51\\ \\mathrm{Pa}.</div> <div class=\"M\">L_p=20\\log_{10}\\frac{220.51}{20\\times10^{-6}}=\\boxed{140.85\\ \\mathrm{dB}\\approx140.9\\ \\mathrm{dB}}.</div> This is the <b>pressure inside the cabinet</b>, not the free-field SPL outside. For a prescribed displacement, this ideal cavity-pressure amplitude does not depend on frequency within the lumped approximation. Using 4 mm as peak adds an erroneous 6.02 dB; forgetting peak-to-RMS adds another 3.01 dB.</p>",
    "bench": "#bench-cabinet4",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "A.1–A.2",
    "title": "Exam Problem A — Tube with 10% absorption",
    "tag": "0.127 mW/m² · 97.0 dB",
    "given": "<p><b>Given:</b> circular diameter <span class=\"m\">d=0.10</span> m, absorbed power <span class=\"m\">W_{\\rm abs}=1\\ \\mu\\mathrm W</span>, absorption coefficient <span class=\"m\">\\alpha=0.10</span>.</p>",
    "hint": "Identify incident and reflected energy, or convert the decibel levels to linear quantities first.",
    "sol": "<h4>A.1 Intensity in the tube</h4><div class=\"M\">S=\\pi(0.05)^2=0.00785398\\ \\mathrm{m^2}.</div>\nIn a lossless tube the net intensity equals the flux into the sample:\n<div class=\"M\">\\boxed{I_{\\rm net}=\\frac{W_{\\rm abs}}S=1.27324\\times10^{-4}\\ \\mathrm{W/m^2}}.</div>\nFor clarity, the incident and reflected components are different:\n<div class=\"M\">W_i=W_{\\rm abs}/\\alpha=10\\ \\mu\\mathrm W,\\quad W_r=9\\ \\mu\\mathrm W,</div>\n<div class=\"M\">I_i=1.27324\\times10^{-3}\\ \\mathrm{W/m^2},\\quad I_r=-1.14592\\times10^{-3}\\ \\mathrm{W/m^2}.</div>\nTheir signed sum gives the boxed answer. The phrase “intensity in the tube” refers to this net quantity; all three are shown to remove ambiguity.<h4>A.2 Maximum SPL</h4><div class=\"M\">|R|=\\sqrt{1-\\alpha}=\\sqrt{0.9}=0.948683,</div>\n<div class=\"M\">p_{i,\\rm rms}=\\sqrt{\\rho c I_i}=0.725155\\ \\mathrm{Pa},</div>\n<div class=\"M\">p_{\\max,\\rm rms}=p_{i,\\rm rms}(1+|R|)=1.41310\\ \\mathrm{Pa},</div>\n<div class=\"M\">\\boxed{L_{p,\\max}=20\\log_{10}\\frac{1.41310}{20\\times10^{-6}}=96.98\\ \\mathrm{dB}\\approx97.0\\ \\mathrm{dB}}.</div>\nA strong standing-wave maximum can coexist with small net intensity because most incident power returns towards the source.",
    "bench": "#bench-absorption4",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "MC 1",
    "title": "Multiple choice 1 — Group third-octaves into octaves",
    "tag": "c · 60, 60, 66, 66 dB",
    "given": "<p><b>Given:</b> only 100, 160, 250, 400, 630 and 1000 Hz third-octave bands contain energy, at 56, 58, 60, 62, 64 and 66 dB respectively. Missing bands contribute zero mean-square energy (not 0 dB).</p>",
    "hint": "Identify incident and reflected energy, or convert the decibel levels to linear quantities first.",
    "sol": "<p>Add the band energies using <span class=\"m\">L=10\\log_{10}\\sum 10^{L_i/10}</span>:</p><div class=\"table-wrap\"><table>\n<tr><td>Octave centre</td><td>Contributing third-octave centres</td><td>Calculation</td><td>Result</td></tr>\n<tr><td>125 Hz</td><td>100, 160 Hz (125 Hz empty)</td><td><span class=\"m\">10\\log_{10}(10^{5.6}+10^{5.8})</span></td><td>60.12 dB</td></tr>\n<tr><td>250 Hz</td><td>250 Hz (200, 315 Hz empty)</td><td><span class=\"m\">60</span></td><td>60 dB</td></tr>\n<tr><td>500 Hz</td><td>400, 630 Hz (500 Hz empty)</td><td><span class=\"m\">10\\log_{10}(10^{6.2}+10^{6.4})</span></td><td>66.12 dB</td></tr>\n<tr><td>1000 Hz</td><td>1000 Hz (800, 1250 Hz empty)</td><td><span class=\"m\">66</span></td><td>66 dB</td></tr>\n</table></div><p>Rounded tuple <span class=\"m\">(60,60,66,66)</span>: <b>answer c</b>.</p>",
    "bench": "#bench-octave",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "MC 2",
    "title": "Multiple choice 2 — Distance from free-field SPL",
    "tag": "c · 0.5, 1.4, 10 m",
    "given": "<p><b>Given:</b> <span class=\"m\">L_p(1\\ \\mathrm m)=64</span> dB; other readings 70, 61 and 44 dB. Assume spherical spreading from the same source, with no reflections or appreciable atmospheric attenuation. <div class=\"M\">L_p(r)=64-20\\log_{10}\\frac r{1\\ \\mathrm m},\\qquad r=(1\\ \\mathrm m)10^{(64-L_p)/20}.</div> The distances are <span class=\"m\">10^{-6/20}=0.501</span> m, <span class=\"m\">10^{3/20}=1.413</span> m and <span class=\"m\">10^{20/20}=10</span> m. <b>Answer c: 0.5 m, 1.4 m, 10 m.</b></p>",
    "hint": "Identify incident and reflected energy, or convert the decibel levels to linear quantities first.",
    "sol": "",
    "bench": "#bench-spherical",
    "benchLabel": "explore the relevant relationships"
  },
  {
    "id": "MC 3",
    "title": "Multiple choice 3 — Absorption from incident/reflected levels",
    "tag": "d · 0.99",
    "given": "<p><b>Given:</b> incident plane-wave SPL 90 dB, reflected SPL 70 dB in the same medium. <div class=\"M\">\\frac{I_r}{I_i}=10^{(70-90)/10}=0.01,\\qquad <div class=\"table-wrap\"><table> <tr><td>R</td><td>=10^{(70-90)/20}=0.1.</div></td></tr> </table></div> <div class=\"M\">\\boxed{\\alpha=1-|R|^2=1-0.01=0.99}.</div> <b>Answer d.</b> Subtracting the pressure ratio instead would produce the distractor 0.9.</p>",
    "hint": "Identify incident and reflected energy, or convert the decibel levels to linear quantities first.",
    "sol": "",
    "bench": "#bench-absorption4",
    "benchLabel": "explore the relevant relationships"
  }
];

/* Week 5: official solutions use ρ = 1.2 kg/m³, c = 344 m/s (ρc = 412.8). */
const R5 = String.raw;
window.PROBLEMS["5"] = [
  {
    id: "1", title: "Problem 1 — Intensity level and power level from one SPL reading", tag: "85.9 dB · 96.9 dB",
    given: R5`<p>An omnidirectional source produces <span class="m">L_p=86</span> dB at <span class="m">r=1</span> m in an anechoic room. Find the sound intensity level there and the sound power level of the source.</p>`,
    hint: R5`<p>For a monopole the near-field velocity term is 90° out of phase with the pressure, so the active intensity is <span class="m">p_{\rm rms}^2/\rho c</span> at <b>any</b> distance. No frequency is needed. Then spread over a sphere.</p>`,
    sol: R5`<div class="M">p_{\rm rms}=20\times10^{-6}\cdot10^{86/20}=0.3991\ \mathrm{Pa}</div>
<div class="M">I_r=\frac{p_{\rm rms}^2}{\rho c}=\frac{0.3991^2}{412.8}=3.858\times10^{-4}\ \mathrm{W/m^2},\qquad L_I=10\log_{10}\frac{3.858\times10^{-4}}{10^{-12}}=\boxed{85.9\ \mathrm{dB}}</div>
<div class="M">W=4\pi r^2I_r=4.848\ \mathrm{mW},\qquad L_W=10\log_{10}\frac{4.848\times10^{-3}}{10^{-12}}=\boxed{96.9\ \mathrm{dB}}</div>
<p>Shortcuts: <span class="m">L_I=L_p-10\log_{10}(\rho c/400)=86-0.14</span> dB, and <span class="m">L_W=L_I+10\log_{10}(4\pi r^2)=L_I+11</span> dB at 1 m.</p>`,
    bench: "#bench-monopole5", benchLabel: "press the Problem 1 chip"
  },
  {
    id: "2", title: "Problem 2 — SPL from a 20 mW source at 3 m and 10 m", tag: "82.6 dB · 72.1 dB",
    given: R5`<p>A small omnidirectional source driven at 250 Hz emits <span class="m">W=20</span> mW. Find the free-field SPL at 3 m and at 10 m.</p>`,
    hint: R5`<p>Problem 1 backwards: <span class="m">W=4\pi r^2p_{\rm rms}^2/\rho c</span>. The 250 Hz is only needed in Problems 3–5.</p>`,
    sol: R5`<div class="M">p_{\rm rms}^2=\frac{W\rho c}{4\pi r^2}</div>
<div class="M">r=3\ \mathrm m:\ p_{\rm rms}^2=\frac{0.02\cdot412.8}{4\pi\cdot9}=0.0730\ \mathrm{Pa^2}\ (0.270\ \mathrm{Pa}),\qquad L_p=\boxed{82.6\ \mathrm{dB}}</div>
<div class="M">r=10\ \mathrm m:\ p_{\rm rms}^2=0.00657\ \mathrm{Pa^2}\ (0.0811\ \mathrm{Pa}),\qquad L_p=\boxed{72.15\ \mathrm{dB}}</div>
<p>Check: <span class="m">20\log_{10}(10/3)=10.46</span> dB. The sheet prints 72.1; the unrounded value 72.155 would round to 72.2. Truncation, not physics.</p>`,
    bench: "#bench-monopole5", benchLabel: "start values"
  },
  {
    id: "3", title: "Problem 3 — The same source 10 cm from a large rigid screen", tag: "37.3 mW · 105.7 dB",
    given: R5`<p>A very large rigid screen is placed 10 cm from the Problem 2 source (20 mW free field, 250 Hz). Find the power and sound power level it now emits.</p>`,
    hint: R5`<p>Replace the screen with an in-phase image source <span class="m">2h</span> behind it, and assume the source keeps the same volume velocity <span class="m">Q</span>. Use the half-space power formula from slide 30.</p>`,
    sol: R5`<div class="M">k=\frac{2\pi\cdot250}{344}=4.566\ \mathrm{rad/m},\qquad kh=0.4566,\qquad \frac{\sin2kh}{2kh}=\frac{0.7915}{0.9133}=0.8667</div>
<div class="M">W_{\rm wall}=W_{\rm free}\left(1+\frac{\sin2kh}{2kh}\right)=20\times1.8667=\boxed{37.3\ \mathrm{mW}},\qquad L_W=\boxed{105.7\ \mathrm{dB}}</div>
<p>The wall is only <span class="m">\lambda/14</span> away (<span class="m">\lambda=1.376</span> m), so the power is almost doubled; the limit is ×2, +3 dB. The image's pressure arrives at the real source in phase with its velocity and adds radiation resistance.</p>`,
    bench: "#bench-wall5", benchLabel: "start values, rigid-wall curve"
  },
  {
    id: "4", title: "Problem 4 — Two identical sources 20 cm apart, in phase", tag: "74.6 mW",
    given: R5`<p>Two sources identical to the Problem 2 source are placed 20 cm apart in free field and driven with the same signal. Find the total power.</p>`,
    hint: R5`<p>This is the Problem 3 geometry (<span class="m">2h=0.2</span> m) with the image made real. Each source sees the same extra load, and now both radiate.</p>`,
    sol: R5`<div class="M">W_{\rm total}=2W_{\rm free}\left(1+\frac{\sin kd}{kd}\right)=2\times37.33=\boxed{74.7\ \mathrm{mW}}</div>
<p>The sheet writes <span class="m">2\times37.3=74.6</span> mW; same result. In the limit <span class="m">kd\to0</span> the pair is one source with <span class="m">2Q</span>, and since power <span class="m">\propto|Q|^2</span> the total becomes <span class="m">4\times20=80</span> mW (+6 dB).</p>`,
    bench: "#bench-wall5", benchLabel: "in-phase twin curve"
  },
  {
    id: "5", title: "Problem 5 — The same two sources in antiphase", tag: "5.6 mW",
    given: R5`<p>The two sources of Problem 4 are driven in antiphase. Find the total radiated power and explain the change.</p>`,
    hint: R5`<p>A dipole with half-spacing <span class="m">h=0.10</span> m. The dipole formula needs <span class="m">|Q|</span>: recover it from the 20 mW free-field power first.</p>`,
    sol: R5`<div class="M">P_{\rm mono}=\frac{\rho ck^2|Q|^2}{8\pi}\Rightarrow|Q|=\sqrt{\frac{8\pi(0.02)}{412.8(4.566)^2}}=7.64\times10^{-3}\ \mathrm{m^3/s}\ \text{(peak)}</div>
<div class="M">P_{\rm dipole}\approx\frac{\rho c\,h^2k^4|Q|^2}{6\pi}=\tfrac86(kh)^2P_{\rm mono}=\tfrac86(0.2085)(20)=\boxed{5.6\ \mathrm{mW}}</div>
<p>Exact (no <span class="m">\sin x\approx x</span>): <span class="m">2P_{\rm mono}(1-\sin2kh/2kh)=40(1-0.8667)=5.33</span> mW; the approximation is 4 % high (the official remark says "about 5 %").</p>
<p><b>Why:</b> at 250 Hz the sources are only 0.15 λ apart. Each one's pressure at the other is nearly equal and opposite, so the pressure on each surface is mostly out of phase with its velocity and the radiation resistance collapses. In the far field the two contributions nearly cancel except for the path difference <span class="m">2h\cos\theta</span>. Versus the in-phase pair: a factor 13.4 (11.3 dB) less.</p>`,
    bench: "#bench-wall5", benchLabel: "antiphase curves, exact and approximate"
  },
  {
    id: "A", title: "Exam problem A — Three sirens", tag: "0.0843 Pa · 8.94 Pa",
    given: R5`<p>Three sirens of equal power at 3, 4 and 20 km from an observation point, each at frequencies the others do not emit. All three on: 74.5 dB. Free field.<br>A.1 Find the sound pressure from the 3 km siren alone. A.2 Find the magnitude of the sound pressure 40 m from one siren.</p>`,
    hint: R5`<p>Different frequencies are incoherent: add mean-square pressures. In the far field <span class="m">p\propto1/r</span>, so write the 4 km and 20 km pressures in terms of the 3 km one.</p>`,
    sol: R5`<h4>A.1</h4><div class="M">p_{\rm tot}^2=p_3^2\left(1+\tfrac9{16}+\tfrac9{400}\right)=1.585\,p_3^2,\qquad p_{\rm tot}=20\,\mu\mathrm{Pa}\cdot10^{74.5/20}=0.1062\ \mathrm{Pa}</div>
<div class="M">p_3=\frac{0.1062}{1.259}=\boxed{0.0843\ \mathrm{Pa\ rms}}\ (72.5\ \mathrm{dB})</div>
<p>The others contribute 70.0 dB (4 km) and 56.0 dB (20 km): the 20 km siren hardly matters.</p>
<h4>A.2</h4><div class="M">p_{40,\rm rms}=0.0843\cdot\frac{3000}{40}=6.33\ \mathrm{Pa}\ (110\ \mathrm{dB}),\qquad|\hat p|=\sqrt2\cdot6.33=\boxed{8.94\ \mathrm{Pa}}</div>
<p>The official "magnitude" is the <b>amplitude</b> (peak). If a question just says "sound pressure", give both.</p>`,
    bench: "#bench-monopole5", benchLabel: "the 1/r law"
  },
  {
    id: "MC 1", title: "Multiple choice 1 — Sources A and B in antiphase", tag: "a · 100 dB",
    given: R5`<p>A: one 1000 Hz tone, 100 dB. B: 1000 Hz and 1500 Hz tones of equal amplitude, 103 dB total. The microphone is equidistant. Level with A and B on, 180° out of phase? a) 100 dB, b) 107 dB, c) 110 dB, d) −∞.</p>`,
    hint: R5`<p>Split B's 103 dB into two equal incoherent tones first. Then add coherently, tone by tone.</p>`,
    sol: R5`<p>Two equal incoherent tones add 3 dB, so each B tone is <span class="m">103-10\log_{10}2=100.0</span> dB.</p>
<ul><li>1000 Hz: A and B both 100 dB, equal amplitude, antiphase, equidistant: they <b>cancel completely</b>.</li><li>1500 Hz: only B, 100 dB.</li></ul>
<p><b>Answer a) 100 dB.</b> 107 dB would be the in-phase case (+6 dB at 1 kHz on top of the 1.5 kHz tone); −∞ forgets the 1500 Hz tone.</p>`,
    bench: "#bench-levels", benchLabel: "coherent vs incoherent sums (lecture 3)"
  },
  {
    id: "MC 2", title: "Multiple choice 2 — Baffled loudspeaker, then a tube in front", tag: "c · 62.8 Pa",
    given: R5`<p>A loudspeaker of radius 5.9 cm in an infinite baffle gives 0.1 Pa rms at 1 m at 50 Hz. An infinite rigid tube with the diaphragm's cross section is fitted in front. RMS pressure 1 m into the tube? a) 0.1 Pa, b) 6.28 Pa, c) 62.8 Pa, d) 413 Pa.</p>`,
    hint: R5`<p><span class="m">ka=0.054\ll1</span>: the baffled piston is a monopole on a rigid plane, <span class="m">p=\rho\omega Q/(2\pi r)</span>. Get <span class="m">Q</span>, then drive a plane wave into <span class="m">\rho c/S</span>; it does not decay along a lossless tube.</p>`,
    sol: R5`<div class="M">Q_{\rm rms}=\frac{2\pi r\,p_{\rm rms}}{\rho\omega}=\frac{2\pi(1)(0.1)}{1.2\cdot2\pi\cdot50}=1.667\times10^{-3}\ \mathrm{m^3/s}</div>
<div class="M">p_{\rm tube}=\frac{\rho c}{\pi a^2}Q_{\rm rms}=\frac{412.8}{\pi(0.059)^2}\,1.667\times10^{-3}=62.9\ \mathrm{Pa}\ \Rightarrow\ \boxed{c)\ 62.8\ \mathrm{Pa}}</div>
<p>62.7–62.9 Pa depending on the value of c. In closed form <span class="m">p_{\rm tube}/p_{\rm baffle}=2r/(ka^2)=629</span>, a 56 dB gain: the radiation resistance rises from the tiny <span class="m">\rho ck^2/2\pi</span> to the matched <span class="m">\rho c/S</span>. This assumes the cone is a velocity source (same <span class="m">Q</span> in both cases). The printed solution drops a <span class="m">1/r</span> and a factor <span class="m">Q_{\rm rms}</span> in its formulas; the answer is right.</p>`,
    bench: "#bench-piston5", benchLabel: "start values, the MC 2 readout"
  }
];

/* Week 6: official Solution 6, c = 343, ρ = 1.2, RMS pressures. */
window.PROBLEMS["6"] = [
  {
    id: "1.1", title: "Problem 1.1 — Natural frequencies below 80 Hz in a 5 × 4 × 3 m room", tag: "34.3 … 79.3 Hz (8 modes)",
    given: R5`<p>A rectangular room measures 5 × 4 × 3 m at 20 °C. Calculate all the natural frequencies below 80 Hz.</p>`,
    hint: R5`<p>Pull out the axial building blocks <span class="m">c/2l</span>: <span class="m">f=\sqrt{(n_xf_x)^2+(n_yf_y)^2+(n_zf_z)^2}</span>. Then try small index combinations in order.</p>`,
    sol: R5`<div class="M">f_x=\frac{343}{10}=34.30,\quad f_y=\frac{343}{8}=42.88,\quad f_z=\frac{343}{6}=57.17\ \mathrm{Hz}</div>
<div class="table-wrap"><table><tr><th>Mode</th><th>Type</th><th>f (Hz)</th></tr><tr><td>(1,0,0)</td><td>axial</td><td>34.3</td></tr><tr><td>(0,1,0)</td><td>axial</td><td>42.9</td></tr><tr><td>(1,1,0)</td><td>tangential</td><td>54.9</td></tr><tr><td>(0,0,1)</td><td>axial</td><td>57.2</td></tr><tr><td>(1,0,1)</td><td>tangential</td><td>66.7</td></tr><tr><td>(2,0,0)</td><td>axial</td><td>68.6</td></tr><tr><td>(0,1,1)</td><td>tangential</td><td>71.5</td></tr><tr><td>(1,1,1)</td><td>oblique</td><td>79.3</td></tr></table></div>
<p>Next up are (2,1,0) at 80.9 Hz and (0,2,0) at 85.8 Hz. Check: <span class="m">N(80)=3.2+4.0+1.4=8.6</span> against 8 counted. <b>Note:</b> Solution 6 prints 34.4 Hz for (1,0,0). That would need c = 344, which would also move the other modes, and the solution does not show that, so it is a rounding slip. The sheet's 34.3 Hz is right.</p>`,
    bench: "#bench-roommodes6", benchLabel: "start values"
  },
  {
    id: "1.2", title: "Problem 1.2 — Which modes have a pressure maximum at the centre?", tag: "only (2,0,0)",
    given: R5`<p>Of the modes in 1.1, which have a pressure maximum at the centre of the room?</p>`,
    hint: R5`<p>At the centre each factor is <span class="m">\cos(n\pi/2)</span>. When is that ±1, and when 0?</p>`,
    sol: R5`<p><span class="m">\cos(n\pi/2)=0</span> for odd <span class="m">n</span>, which puts a nodal plane through the centre. It is ±1 for even <span class="m">n</span>, including 0. So a mode has a maximum at the centre only if <b>all three indices are even</b>. In the list only <b>(2,0,0)</b> qualifies. A microphone in the middle of the room is deaf to (1,0,0) (slide 19).</p>`,
    bench: "#bench-roommodes6", benchLabel: "● marks in the mode list"
  },
  {
    id: "1.3", title: "Problem 1.3 — Modes in the 50 Hz third-octave band", tag: "only (1,1,0)",
    given: R5`<p>Which of all the modes have natural frequencies in the one-third octave band centred on 50 Hz?</p>`,
    hint: R5`<p>The exact band edges are <span class="m">f_c\,2^{\mp1/6}</span>.</p>`,
    sol: R5`<div class="M">f_l=\frac{50}{2^{1/6}}=44.5\ \mathrm{Hz},\qquad f_u=50\cdot2^{1/6}=56.1\ \mathrm{Hz}</div>
<p>42.9 Hz falls just below the band and 57.2 Hz just above, so only <b>(1,1,0) at 54.9 Hz</b> is inside. The count formula predicts 1.5 modes in the band, but at this frequency the discrete count is what matters: one mode per band is why small rooms boom on particular notes.</p>`,
    bench: "#bench-roommodes6", benchLabel: "the 50 Hz band"
  },
  {
    id: "2.1", title: "Problem 2.1 — Degenerate modes in a 3 m cube", tag: "57 · 81 · 114 · 128 Hz",
    given: R5`<p>Modes with the same natural frequency are called degenerate. Find the four lowest natural frequencies with degenerate, coincident modes in a 3 × 3 × 3 m room.</p>`,
    hint: R5`<p>With equal sides <span class="m">f=\frac c{2l}\sqrt{n_x^2+n_y^2+n_z^2}</span>, so only the sum of squares matters and every permutation coincides.</p>`,
    sol: R5`<div class="M">\frac{c}{2l}=\frac{343}{6}=57.17\ \mathrm{Hz}</div>
<div class="table-wrap"><table><tr><th><span class="m">\sum n^2</span></th><th>Modes</th><th>f (Hz)</th></tr><tr><td>1</td><td>(1,0,0) ×3 permutations</td><td><b>57.2</b></td></tr><tr><td>2</td><td>(1,1,0) ×3</td><td><b>80.8</b></td></tr><tr><td>3</td><td>(1,1,1) — only one, not degenerate</td><td>99.0</td></tr><tr><td>4</td><td>(2,0,0) ×3</td><td><b>114.3</b></td></tr><tr><td>5</td><td>(2,1,0) ×6</td><td><b>127.8</b></td></tr></table></div>
<p>Below 130 Hz the cube has only 5 distinct frequencies carrying 16 modes: a few huge peaks with wide gaps between them. Hence the design rule against simple dimension ratios.</p>`,
    bench: "#bench-roommodes6", benchLabel: "the 3 m cube chip"
  },
  {
    id: "3.1", title: "Problem 3.1 — L_eq of an intermittent 10 mW source", tag: "91 dB",
    given: R5`<p>A small omnidirectional source emits 10 mW in the 500 Hz octave band, on for 5 minutes and off for 10. Room: 210 m³, T = 3.1 s in that band. Find the equivalent SPL where the reverberant field dominates. The integration time is a multiple of 15 minutes.</p>`,
    hint: R5`<p>Get A from Sabine, then <span class="m">p^2=4P\rho c/A</span>. Average <span class="m">p^2</span> over time, not the dB value.</p>`,
    sol: R5`<div class="M">A=\frac{55.3\cdot210}{343\cdot3.1}=10.92\ \mathrm{m^2},\qquad p_{\rm on}^2=\frac{4(0.010)(411.6)}{10.92}=1.508\ \mathrm{Pa^2}\ (1.23\ \mathrm{Pa},\ 95.8\ \mathrm{dB})</div>
<div class="M">L_{\rm eq}=10\log_{10}\frac{p_{\rm on}^2/3}{p_0^2}=95.8-4.8=\boxed{91\ \mathrm{dB}}</div>
<p>Build-up and decay take a fraction of a second against 5 minutes on. The reverberation distance is 0.47 m and the Schroeder frequency about 240 Hz, so the diffuse-field formula holds.</p>`,
    bench: "#bench-roomlevel6", benchLabel: "start values"
  },
  {
    id: "3.2", title: "Problem 3.2 — Adding a steady second source", tag: "93 dB",
    given: R5`<p>A second omnidirectional source, which gives 70 dB at 4 m in free space (500 Hz octave), runs continuously in the same room. The sources are uncorrelated. Find the total equivalent SPL in the reverberant field.</p>`,
    hint: R5`<p>Free-field monopole: <span class="m">P=4\pi r^2p^2/\rho c</span>. Then reverberant <span class="m">p_2^2</span>, and add mean squares.</p>`,
    sol: R5`<div class="M">P_2=\frac{(20\times10^{-6}\cdot10^{70/20})^2}{411.6}\,4\pi(4)^2=1.95\ \mathrm{mW}\approx2\ \mathrm{mW}</div>
<div class="M">p_2^2=\frac{4P_2\rho c}{A}=0.295\ \mathrm{Pa^2}\ (0.54\ \mathrm{Pa},\ 88.7\ \mathrm{dB})</div>
<div class="M">L_{\rm eq}=10\log_{10}\frac{1.23^2/3+0.54^2}{(20\times10^{-6})^2}=\boxed{93\ \mathrm{dB}}\quad(91.0\oplus88.7)</div>
<p>Solution 6 writes "sound pressure" for <span class="m">P_a</span>; it means sound power. The <span class="m">(1-\bar\alpha)</span> factor is about −0.2 dB here and is ignored.</p>`,
    bench: "#bench-roomlevel6", benchLabel: "start values"
  }
];

/* Week 7: no official solutions yet — derived, checked against the answers printed on the sheet. ρ = 1.2, c = 344. */
const DER7 = `<p class="small"><i>Derived; official solutions not out yet. The result matches the answer printed on the sheet.</i></p>`;
window.PROBLEMS["7"] = [
  {
    id: "1.1", title: "Problem 1.1 — Absorption coefficient from a reverberation-chamber test", tag: "α = 0.45",
    given: R5`<p>A 10 m² sample is tested in a 200 m³ reverberation chamber: <span class="m">T=5.2</span> s empty, 3.0 s with the sample. Find the absorption coefficient at 500 Hz. The field is ideally diffuse; neglect the absorption of the covered surface.</p>`,
    hint: R5`<p>Work in absorption areas <span class="m">A=0.16V/T</span>. The sample's absorption is the <b>difference</b> between the two.</p>`,
    sol: DER7 + R5`<div class="M">A_{\rm empty}=\frac{0.16\cdot200}{5.2}=6.154\ \mathrm{m^2},\qquad A_{\rm sample}=\frac{0.16\cdot200}{3.0}=10.667\ \mathrm{m^2}</div>
<div class="M">\alpha=\frac{A_{\rm sample}-A_{\rm empty}}{S}=\frac{32}{10}(0.3333-0.1923)=\boxed{0.451}</div>
<p>The <span class="m">+\alpha_{\rm wall}</span> term of ISO 354 is dropped, as the sheet allows (a concrete chamber would add about 0.01–0.02).</p>`,
    bench: "#bench-reverb7", benchLabel: "start values"
  },
  {
    id: "1.2", title: "Problem 1.2 — Area needed in the lecture hall", tag: "62 m²",
    given: R5`<p>A furnished, empty lecture hall of 300 m³ has <span class="m">T_{500}=3.1</span> s. The target is 0.8 s with 40 students present, each adding 0.42 m² at 500 Hz. How much of the Problem 1.1 material is needed?</p>`,
    hint: R5`<p>Absorption the room has now, absorption the target needs, subtract the students, divide the rest by α. Round <b>up</b>.</p>`,
    sol: DER7 + R5`<div class="M">A_{\rm now}=\frac{0.16\cdot300}{3.1}=15.48\ \mathrm{m^2},\quad A_{\rm target}=\frac{0.16\cdot300}{0.8}=60.0\ \mathrm{m^2},\quad A_{\rm students}=40\cdot0.42=16.8\ \mathrm{m^2}</div>
<div class="M">A_{\rm material}=60.0-15.48-16.8=27.72\ \mathrm{m^2},\qquad S=\frac{27.72}{0.451}=61.4\ \mathrm{m^2}\Rightarrow\boxed{62\ \mathrm{m^2}}</div>
<p>Check: <span class="m">T=48/(15.48+16.8+62\cdot0.451)=0.797</span> s. Strictly the covered surfaces' own absorption (about 1 m²) is lost, which would push the area to about 64 m²; the sheet says to ignore it.</p>`,
    bench: "#bench-reverb7", benchLabel: "start values, the T-versus-area curve"
  },
  {
    id: "2.1", title: "Problem 2.1 — Plywood membrane absorber", tag: "77 Hz",
    given: R5`<p>A large plywood panel, 20 mm thick, density 600 kg/m³, is mounted 50 mm from a hard wall with the cavity closed at the sides. At what frequency is its absorption maximum? Neglect panel stiffness.</p>`,
    hint: R5`<p>Limp-membrane mass–spring formula, with mass <b>per unit area</b> <span class="m">m=\rho_ph</span>.</p>`,
    sol: DER7 + R5`<div class="M">m=600\cdot0.020=12\ \mathrm{kg/m^2}</div>
<div class="M">f_r=\frac1{2\pi}\sqrt{\frac{\rho c^2}{mL}}=\frac1{2\pi}\sqrt{\frac{1.42\times10^5}{12\cdot0.05}}=\boxed{77\ \mathrm{Hz}}</div>
<p>77.4 Hz with <span class="m">c=344</span>, 76.9 Hz with the slide's <span class="m">1.4\times10^5</span>, and the rule of thumb <span class="m">60/\sqrt{mL}</span> gives 77.5 Hz.</p>`,
    bench: "#bench-panel7", benchLabel: "start values, membrane curve"
  },
  {
    id: "2.2", title: "Problem 2.2 — The same panel, perforated", tag: "432 Hz",
    given: R5`<p>10 mm holes are drilled in the Problem 2.1 panel on a square pattern with 30 mm between hole centres. Find the resonance frequency of the perforated-panel absorber.</p>`,
    hint: R5`<p>Each hole owns a 30×30 mm patch: <span class="m">P=\pi d^2/4a^2</span>. The neck is the panel thickness, plus the end correction <span class="m">0.8d</span>. The panel's weight no longer matters.</p>`,
    sol: DER7 + R5`<div class="M">P=\frac{\pi\cdot0.010^2/4}{0.030^2}=0.0873,\qquad l+\delta=0.020+0.8\cdot0.010=0.028\ \mathrm m</div>
<div class="M">f_0=\frac{c}{2\pi}\sqrt{\frac{P}{L(l+\delta)}}=\frac{344}{2\pi}\sqrt{\frac{0.0873}{0.05\cdot0.028}}=54.75\cdot7.895=\boxed{432\ \mathrm{Hz}}</div>
<p>Same spring, lighter mass: <span class="m">\rho(l+\delta)/P=0.385</span> kg/m² against the panel's 12, about 31 times lighter, and <span class="m">77\sqrt{31}\approx432</span>. Slide 28 is exactly this calculation.</p>`,
    bench: "#bench-panel7", benchLabel: "start values, perforated curve"
  }
];

function renderProblems() {
  for (const [lec, list] of Object.entries(window.PROBLEMS || {})) {
    const root = document.getElementById(`problems-${lec}`);
    if (!root) continue;
    root.classList.add("problems");
    root.append(h("h3", {}, h("span", { class: "eyebrow" }, `Problems · week ${lec}`), "Problems and solutions"));
    root.append(h("p", { class: "small" }, "Open a problem, try it, then open the hint before the solution. Answers are checked against the sheet where provided; exam examples include derived answers."));
    for (const p of list) {
      const body = h("div", { class: "pbody" });
      body.append(h("div", { class: "pgiven", html: p.given }));
      if (p.hint) body.append(h("details", { class: "phint" }, h("summary", {}, "Hint"), h("div", { html: p.hint })));
      body.append(h("details", { class: "psol" }, h("summary", {}, "Solution"), h("div", { html: p.sol })));
      if (p.bench) body.append(h("a", { class: "pbench", href: p.bench }, `Try it on the bench → ${p.benchLabel || ""}`));
      root.append(h("details", { class: "prob" }, h("summary", {}, h("span", { class: "pid" }, p.id), h("span", { class: "pt" }, p.title), h("span", { class: "pans" }, p.tag)), body));
    }
    renderMath(root);
  }
}
document.addEventListener("DOMContentLoaded", renderProblems);
