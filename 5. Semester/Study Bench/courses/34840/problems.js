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
