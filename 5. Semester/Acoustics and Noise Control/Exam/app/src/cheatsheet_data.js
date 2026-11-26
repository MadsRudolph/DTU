// 34840 Exam App — Searchable Cheat Sheet, Worked Old-Exam Part 1 Problems & Exam-Day Checklist

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.CHEATSHEET_DATA = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  const sections = [
    {
      id: 'cs-0',
      title: '0. Constants & Phasor Conventions',
      solver: 'T01',
      keywords: 'constants rho c air water impedance reference pressure intensity power phasor peak rms amplitude',
      items: [
        { label: 'Air (every exam 2022–2024)', formula: '\\rho = 1.2\\,\\mathrm{kg/m^3},\\quad c = 343\\,\\mathrm{m/s},\\quad \\rho c = 411.6\\,\\mathrm{Pa\\cdot s/m},\\quad \\rho c^2 = 1.412\\times 10^5\\,\\mathrm{Pa}', note: 'Weeks 5 & 7 used c = 344 m/s (shifts 3rd digit only). Always use the cover-page values!' },
        { label: 'Water', formula: '\\rho = 1000\\,\\mathrm{kg/m^3},\\quad c = 1480\\,\\mathrm{m/s} \\implies \\rho c = 1.48\\times 10^6\\,\\mathrm{Pa\\cdot s/m}', note: 'Air ↔ water power transmission τ ≈ 1.1×10⁻³ (−29.5 dB both ways); pressure doubles into water (T_p ≈ 2).' },
        { label: 'Reference values', formula: 'p_{\\mathrm{ref}} = 20\\,\\mu\\mathrm{Pa}\\;(\\text{air}),\\quad I_{\\mathrm{ref}} = 10^{-12}\\,\\mathrm{W/m^2},\\quad W_{\\mathrm{ref}} = 10^{-12}\\,\\mathrm{W},\\quad g = 9.81\\,\\mathrm{m/s^2}', note: '1 Pa rms = 94.0 dB SPL. In a plane wave, L_I = L_p − 0.14 dB.' },
        { label: 'Temperature speed of sound', formula: 'c(T) = \sqrt{\\gamma R_s T} \\approx 20.05\\sqrt{T_{\\mathrm{K}}}\\quad (\\gamma = 1.4,\\; R_s = 287\\,\\mathrm{J/(kg\\cdot K)})', note: 'For fixed geometry (tubes, rooms), resonance frequencies scale as f ∝ c ∝ √T_K.' },
        { label: 'Phasor convention', formula: 'p(t) = \\mathrm{Re}\\{P e^{j\\omega t}\\},\\quad p_{\\mathrm{rms}} = \\frac{|P|}{\\sqrt{2}},\\quad \\frac{\\partial}{\\partial t} \\to j\\omega,\\quad \\int dt \\to \\frac{1}{j\\omega}', note: 'Capital letters P, U, Q are PEAK amplitudes. Room acoustics (L6, L12) uses RMS throughout.' }
      ]
    },
    {
      id: 'cs-05',
      title: '0.5 Decision Table (Read the Question for These First)',
      solver: 'T03',
      keywords: 'decision table coherent incoherent amplitude rms 20log 10log 2pi 4pi baffle wall near field Sabine Eyring isolation coincidence double wall',
      items: [
        { label: 'Same frequency AND fixed phase?', formula: 'P_{\\mathrm{tot}} = \\sum P_i,\\quad p_{\\mathrm{rms}} = \\frac{|P_{\\mathrm{tot}}|}{\\sqrt{2}}', note: 'Coherent: add complex amplitudes first (e.g. 1200 Hz in 2022 P2; 1002 Hz in 2023 P2). Equal levels: −∞ to +6 dB.' },
        { label: 'Different frequencies / independent sources?', formula: 'p_{\\mathrm{rms}}^2 = \\sum p_{\\mathrm{rms},i}^2 = \\sum \\frac{|P_i|^2}{2},\\quad L_{\\mathrm{tot}} = 10\\log_{10}\\sum 10^{L_i/10}', note: 'Incoherent: add squared RMS pressures. Two close tones averaged over ≥ 1 beat period 1/Δf also add incoherently (2022 MC2).' },
        { label: 'Amplitude or RMS?', formula: 'p_{\\mathrm{rms}} = \\frac{\\hat{p}}{\\sqrt{2}} \\implies L_p = 20\\log_{10}\\frac{\\hat{p}}{\\sqrt{2}\\,p_{\\mathrm{ref}}}', note: '"Pressure/velocity amplitude" = peak → divide by √2. Voltages on sheets ("4 V rms") are RMS → multiply by √2 for peak phasors.' },
        { label: 'Free field (4π) vs Baffle / Rigid plane (2π)', formula: '|p| = \\frac{\\rho\\omega |Q|}{\\Omega r},\\quad W = \\Omega r^2 I = \\frac{\\rho c k^2 |Q|^2}{2\\Omega}\\quad (\\Omega = 4\\pi \\text{ or } 2\\pi)', note: 'Small box in free air: Ω = 4π. Infinite baffle / on rigid ground: Ω = 2π (+6 dB pressure, +3 dB power for same Q).' },
        { label: 'Sabine vs Eyring', formula: 'T_{\\mathrm{Sabine}} = \\frac{55.3\\,V}{c\\,A} \\approx \\frac{0.16\\,V}{A},\\qquad T_{\\mathrm{Eyring}} = \\frac{0.16\\,V}{-S\\ln(1-\\bar{\\alpha})}', note: 'Use Sabine for ᾱ < 0.3 (standard exam choice); Eyring for ᾱ > 0.3. Eyring is always shorter.' },
        { label: 'Below / above √2·f₀ (Vibration isolation)', formula: 'f_0 = \\frac{1}{2\\pi}\\sqrt{\\frac{g}{\\xi_0}} \\approx \\frac{0.5}{\\sqrt{\\xi_0}},\\qquad f_{\\mathrm{iso}} = \\sqrt{2}\\,f_0', note: 'Below √2·f₀: T > 1 (amplifies!). At √2·f₀: T = 1 (0 dB). Isolation ONLY above √2·f₀.' }
      ]
    },
    {
      id: 'cs-1',
      title: '1. Plane Waves, Reflection & Tubes (L1–L2) → T01, T02',
      solver: 'T01',
      keywords: 'plane wave wavenumber wavelength reflection coefficient surface impedance standing wave ratio SWR nodes two media air water driven tube tunnel resonances',
      items: [
        { label: 'Plane wave & Euler', formula: 'k = \\frac{\\omega}{c} = \\frac{2\\pi}{\\lambda},\\quad j\\omega\\rho U = -\\frac{dP}{dx},\\quad U_{\\mathrm{fwd}} = \\frac{P}{\\rho c},\\quad U_{\\mathrm{bwd}} = -\\frac{P}{\\rho c}', note: 'Displacement Ξ = U/(jω), |Ξ| = |P|/(ωρc). Adiabatic cavity: p = −γ p₀ ΔV/V.' },
        { label: 'Incident + reflected wave (surface at x = 0)', formula: 'P(x) = P_i e^{-jkx} + R P_i e^{+jkx},\\qquad U(x) = \\frac{P_i e^{-jkx} - R P_i e^{+jkx}}{\\rho c}', note: 'Point at distance d in front of surface is x = −d. Note the MINUS sign on the reflected wave in U(x)!' },
        { label: 'Reflection coefficient & absorption', formula: 'R = \\frac{Z - \\rho c}{Z + \\rho c},\\qquad \\alpha = 1 - |R|^2 \\implies |R| = \\sqrt{1 - \\alpha}', note: 'Rigid wall / water from air: R = +1 (p max at wall, u = 0). Soft / bubbles in water / open end: R = −1 (p = 0 at boundary).' },
        { label: 'Standing-wave pattern & net intensity', formula: '|p|_{\\max} = |P_i|(1+|R|),\\quad |p|_{\\min} = |P_i|(1-|R|),\\quad s = \\frac{1+|R|}{1-|R|},\\quad I = \\frac{|P_i|^2(1-|R|^2)}{2\\rho c}', note: 'For R = +1: P(x) = 2P_i cos(kx), pressure nodes at d = (2n+1)λ/4 from wall, spaced every λ/2.' },
        { label: 'Two media (normal incidence)', formula: 'R_{12} = \\frac{Z_2 - Z_1}{Z_2 + Z_1},\\quad T_p = \\frac{2Z_2}{Z_1 + Z_2},\\quad \\tau = \\frac{4Z_1 Z_2}{(Z_1 + Z_2)^2} = 1 - R_{12}^2', note: 'Air ↔ water: −10 log₁₀ τ = 29.5 dB loss both ways.' },
        { label: 'Tube resonances & driven tunnel (2023 P1)', formula: 'f_{n,\\text{open-open/closed-closed}} = \\frac{nc}{2L},\\quad f_{n,\\text{closed-open}} = \\frac{(2n-1)c}{4L},\\quad A = \\frac{\\rho c U_0}{e^{jkL} - R e^{-jkL}}', note: 'Driven at x = −L with velocity U₀: with absorber (R=0), |p| = ρcU₀ everywhere; with water/rigid (R=1), p(x) = 2A cos(kx).' }
      ]
    },
    {
      id: 'cs-2',
      title: '2. Levels, Adding, L_eq, Octave Bands & A-Weighting (L3) → T03, T04',
      solver: 'T04',
      keywords: 'SPL decibels adding coherent incoherent background noise Leq LAE SEL octave third-octave band edges A-weighting C-weighting table',
      items: [
        { label: 'SPL & coherent phase sum', formula: 'L_p = 20\\log_{10}\\frac{p_{\\mathrm{rms}}}{20\\,\\mu\\mathrm{Pa}},\\qquad \\Delta L_{\\text{2 equal tones}} = 10\\log_{10}(2 + 2\\cos\\phi)', note: 'φ = 0°: +6.0 dB · φ = 90°: +3.0 dB · φ = 120°: 0 dB · φ = 180°: −∞ dB.' },
        { label: 'Uncorrelated sum & background subtraction', formula: 'L_{\\mathrm{tot}} = 10\\log_{10}\\sum_i 10^{L_i/10},\\qquad L_{\\mathrm{src}} = 10\\log_{10}\\left(10^{L_{\\mathrm{tot}}/10} - 10^{L_{\\mathrm{bg}}/10}\\right)', note: 'N equal uncorrelated sources: +10 log₁₀ N. Two equal: +3.0 dB.' },
        { label: 'Equivalent level L_eq,T & SEL (L_AE)', formula: 'L_{\\mathrm{eq},T} = 10\\log_{10}\\sum_i \\frac{t_i}{T}10^{L_i/10} = L_{\\mathrm{on}} + 10\\log_{10}\\frac{t_{\\mathrm{on}}}{T},\\qquad L_{\\mathrm{eq},T} = L_{AE} + 10\\log_{10}n - 10\\log_{10}T_{\\mathrm{sec}}', note: 'Duty cycle d = 1/4 → −6.0 dB; d = 1/3 → −4.8 dB; d = 4/24 = 1/6 → −7.78 dB.' },
        { label: 'Octave (n=1) & third-octave (n=3) band edges', formula: 'f_l = f_c\\,2^{-1/(2n)},\\qquad f_u = f_c\\,2^{+1/(2n)}\\qquad (\\text{Octave: } f_c/\\sqrt{2}\\text{ to } f_c\\sqrt{2})', note: 'Octave edges: 125 Hz [88.4–176.8] · 250 Hz [176.8–353.6] · 500 Hz [353.6–707.1] · 1 kHz [707.1–1414.2] · 2 kHz [1414.2–2828.4] · 4 kHz [2828.4–5656.9]. Empty band = −∞ dB!' },
        { label: 'A-weighting K_A (dB, Table 1.3.2)', formula: 'p_{A,\\mathrm{rms}} = p_{\\mathrm{rms}}\\cdot 10^{K_A/20},\\qquad L_A = 10\\log_{10}\\sum_i 10^{(L_i + K_{A,i})/10}', note: 'Octaves: 63 (−26.2) · 125 (−16.1) · 250 (−8.6) · 500 (−3.2) · 1k (0) · 2k (+1.2) · 4k (+1.0) · 8k (−1.1). Third-octaves: 400 Hz (−4.8 dB), 630 Hz (−1.9 dB).' }
      ]
    },
    {
      id: 'cs-3',
      title: '3. Impedance, Intensity & Sound Power (L4) → T05',
      solver: 'T05',
      keywords: 'specific acoustic mechanical impedance cavity compliance Helmholtz intensity sound power standing wave tube SWR absorbed power',
      items: [
        { label: 'Three impedances (Q = SU, F = PS)', formula: 'z = \\frac{P}{U}\\;[\\mathrm{Pa\\cdot s/m}],\\quad Z_a = \\frac{P}{Q} = \\frac{z}{S}\\;[\\mathrm{Pa\\cdot s/m^3}],\\quad Z_m = \\frac{F}{v} = S\\,z = S^2 Z_a\\;[\\mathrm{N\\cdot s/m}]', note: 'Small cavity compliance: C_a = V/(ρc²), Z_a = 1/(jωC_a). Closed tube: Z_in = −j(ρc/S)cot(kL).' },
        { label: 'Active intensity & sound power', formula: 'I = \\frac{1}{2}\\mathrm{Re}\\{P\\,U^*\\} = p_{\\mathrm{rms}}u_{\\mathrm{rms}}\\cos\\phi,\\qquad W = \\int \\mathbf{I}\\cdot d\\mathbf{S}', note: 'Plane wave: I = p²_rms/(ρc), W = I·S. Free sphere: W = 4πr²I. Baffle hemisphere: W = 2πr²I. Port: W = ½|Q|² Re{Z_a}.' },
        { label: 'Standing-wave tube absorption & power', formula: 's = 10^{(L_{\\max}-L_{\\min})/20},\\quad \\alpha = \\frac{4s}{(s+1)^2},\\quad W_{\\mathrm{abs}} = \\frac{S\\,p_{\\max,\\mathrm{rms}}p_{\\min,\\mathrm{rms}}}{\\rho c}', note: 'p_i,rms = (p_max,rms + p_min,rms)/2, p_r,rms = (p_max,rms − p_min,rms)/2. s = 3 → α = 0.75; s = 2 → α = 0.89.' }
      ]
    },
    {
      id: 'cs-4',
      title: '4. Radiation: Monopole, Wall, Dipole & Piston (L5) → T06, T07',
      solver: 'T06',
      keywords: 'monopole near field phase volume velocity Q two sources cancellation rigid wall image source dipole baffled piston directivity',
      items: [
        { label: 'Monopole pressure, velocity & phase', formula: 'P(r) = \\frac{j\\omega\\rho Q}{4\\pi r}e^{-jkr},\\qquad U_r(r) = \\frac{P(r)}{\\rho c}\\left(1 + \\frac{1}{jkr}\\right),\\qquad \\phi_{p-u} = \\arctan\\left(\\frac{1}{kr}\\right)', note: 'p ∝ 1/r always; u decays faster (1/r²) for kr < 1. At kr = 1 → 45°; kr = 1.73 → 30° (2024 MC1).' },
        { label: 'Monopole radiated power', formula: 'W_{\\mathrm{free}} = \\frac{\\rho c k^2 |Q|^2}{8\\pi}\\;(\\text{peak } Q),\\qquad W_{\\mathrm{baffle}} = \\frac{\\rho c k^2 |Q|^2}{4\\pi}', note: 'General: W = ρck²|Q|²/(2Ω) with Ω = 4π (free) or 2π (baffle).' },
        { label: 'Two sources on a line (x = 0 and x = D)', formula: 'p = p_1 + p_2,\\qquad u_x = u_1 - u_2 = \\frac{p_1}{\\rho c}\\left(1+\\frac{1}{jkr_1}\\right) - \\frac{p_2}{\\rho c}\\left(1+\\frac{1}{jkr_2}\\right)', note: 'Cancellation between in-phase sources: Δx = 2(x_c − D/2) = (2n+1)λ/2 → f_n = (2n+1)f₀, |Q₁|/|Q₂| = x_c/(D − x_c) (2022 P3).' },
        { label: 'Monopole at distance h from a rigid wall (2023 P3)', formula: 'W_{\\mathrm{wall}} = \\frac{\\rho c k^2 |Q|^2}{8\\pi}\\left(1 + \\frac{\\sin 2kh}{2kh}\\right),\\qquad I_{\\mathrm{line}} \\approx \\frac{|p_1|^2 - |p_{\\mathrm{im}}|^2}{2\\rho c}', note: 'Image source at 2h in phase. kh ≪ 1: W × 2 (+3 dB). At the wall (r = h), |p₁| = |p_im| and I = 0.' },
        { label: 'Dipole (two antiphase sources 2h apart)', formula: 'W_{\\mathrm{dip}} = \\frac{\\rho c k^2 |Q|^2}{4\\pi}\\left(1 - \\frac{\\sin 2kh}{2kh}\\right) \\approx \\frac{\\rho c h^2 k^4 |Q|^2}{6\\pi} \\propto f^4', note: 'Very inefficient at low frequencies (kh ≪ 1) because the antiphase halves cancel.' }
      ]
    },
    {
      id: 'cs-5',
      title: '5. Room Modes & Diffuse Sound Field (L6) → T09, T10',
      solver: 'T09',
      keywords: 'room modes axial tangential oblique Schroeder frequency diffuse field Sabine Eyring reverberation time critical radius ISO 354',
      items: [
        { label: 'Rectangular room eigenfrequencies', formula: 'f_{n_x,n_y,n_z} = \\frac{c}{2}\\sqrt{\\left(\\frac{n_x}{l_x}\\right)^2 + \\left(\\frac{n_y}{l_y}\\right)^2 + \\left(\\frac{n_z}{l_z}\\right)^2}', note: '1 non-zero index = axial, 2 = tangential, 3 = oblique. Odd index → node in room centre (only all-even modes heard at centre; all modes max in corners).' },
        { label: 'Mode count & Schroeder frequency', formula: 'N(f) \\approx \\frac{4\\pi V}{3}\\left(\\frac{f}{c}\\right)^3 + \\frac{\\pi S}{4}\\left(\\frac{f}{c}\\right)^2 + \\frac{L}{8}\\frac{f}{c},\\qquad f_S \\approx 2000\\sqrt{\\frac{T}{V}}', note: 'L = 4(l_x + l_y + l_z) is sum of all 12 room edges; S = 2(l_x l_y + l_x l_z + l_y l_z).' },
        { label: 'Sabine, Eyring & ISO 354', formula: 'A = \\sum S_i\\alpha_i + 4mV,\\quad T_{\\mathrm{Sabine}} = \\frac{55.3\\,V}{c\\,A} \\approx \\frac{0.16\\,V}{A},\\quad \\alpha_{\\mathrm{ISO\\,354}} = \\frac{0.16\\,V}{S_{\\mathrm{sample}}}\\left(\\frac{1}{T_2} - \\frac{1}{T_1}\\right)', note: 'Diffuse wall incident intensity: I_inc = p²_rms/(4ρc). Steady-state reverberant pressure: p²_rms = 4Wρc/A.' },
        { label: 'Direct + reverberant level & critical distance', formula: 'L_p = L_W + 10\\log_{10}\\left(\\frac{Q}{4\\pi r^2} + \\frac{4}{A}\\right),\\qquad r_{\\mathrm{rev}} = \\sqrt{\\frac{Q\\,A}{16\\pi}} \\approx 0.14\\sqrt{Q\\,A}', note: 'Sound power in reverb room: L_W = L̄_p + 10 log₁₀ V − 10 log₁₀ T − 14 dB.' }
      ]
    },
    {
      id: 'cs-6',
      title: '6. Sound Absorbers (L7) → T11',
      solver: 'T11',
      keywords: 'porous absorber quarter wavelength membrane panel absorber Helmholtz resonator perforated panel random incidence Paris formula',
      items: [
        { label: 'Porous absorber (thickness/backing distance d)', formula: 'f_{\\lambda/4} = \\frac{c}{4d}\\;(\\text{first peak}),\\qquad f_{\\lambda/2} = \\frac{c}{2d}\\;(\\text{dip})', note: 'Effective at mid/high frequencies where particle velocity is large (distance d from rigid backing ≥ λ/4; λ/8 in diffuse field).' },
        { label: 'Membrane (panel) absorber', formula: 'f_r = \\frac{1}{2\\pi}\\sqrt{\\frac{\\rho c^2}{m\\,L}} \\approx \\frac{60}{\\sqrt{m\\,L}},\\qquad L = \\frac{\\rho c^2}{m(2\\pi f_r)^2}', note: 'm = surface mass in kg/m² (= density × thickness), L = air cavity depth in m.' },
        { label: 'Helmholtz & perforated panel absorbers', formula: 'f_{\\mathrm{Helm}} = \\frac{c}{2\\pi}\\sqrt{\\frac{s}{V(l+\\delta)}},\\qquad f_{\\mathrm{perf}} = \\frac{c}{2\\pi}\\sqrt{\\frac{P}{L(l+\\delta)}}\\quad\\left(s = \\frac{\\pi d^2}{4},\\; P = \\frac{\\pi d^2}{4a^2},\\; \\delta \\approx 0.8d\\right)', note: 'P is the open area FRACTION (not %). L is cavity depth, l is neck/panel thickness.' },
        { label: 'Absorption from surface impedance Z (normal, oblique, Paris)', formula: '\\zeta = \\frac{Z}{\\rho c} = r + jx,\\qquad \\alpha_n = \\frac{4r}{(r+1)^2 + x^2},\\qquad \\alpha_r = \\int_0^{\\pi/2}\\alpha(\\theta)\\sin 2\\theta\\,d\\theta', note: 'Normalise Z by ρc FIRST! Reflected level: L_refl = L_inc + 10 log₁₀(1 − α).' }
      ]
    },
    {
      id: 'cs-7',
      title: '7. Loudspeakers (L8) → T08',
      solver: 'T08',
      keywords: 'loudspeaker driver mechanical impedance resonance volume velocity mass controlled excursion closed box headphone cavity',
      items: [
        { label: 'Driver mechanics & volume velocity', formula: 'F = Bl\\frac{\\hat{e}}{R_e},\\quad Z_M = R_t + j\\left(\\omega M - \\frac{K}{\\omega}\\right),\\quad Q = S\\,U = \\frac{S\\,Bl\\,\\hat{e}}{R_e Z_M}\\quad (S = \\pi a^2,\\; \\hat{e} = \\sqrt{2}\\,e_{\\mathrm{rms}})', note: 'f_s = (1/2π)√(K/M), Q_t = √(KM)/R_t. R_t already includes electrical damping (Bl)²/R_e.' },
        { label: 'Far-field pressure, power & mass-controlled flat region', formula: '|p(r)| = \\frac{\\rho\\omega |Q|}{\\Omega r},\\quad W = \\Omega r^2 \\frac{|p|^2}{2\\rho c},\\quad |p|_{\\mathrm{mass\\,ctrl}}(f \\gg f_s) = \\frac{\\rho\\,S\\,Bl\\,\\hat{e}}{\\Omega r R_e M}', note: 'Ω = 2π (infinite baffle) or 4π (box in free space). Excursion |x| = |U|/ω ∝ 1/f² above f_s.' },
        { label: 'Closed box & sealed headphone cavity', formula: 'K_{\\mathrm{box}} = \\frac{\\rho c^2 S^2}{V_{\\mathrm{box}}},\\quad f_c = \\frac{1}{2\\pi}\\sqrt{\\frac{K+K_{\\mathrm{box}}}{M}},\\quad C_A = \\frac{V_{\\mathrm{cav}}}{\\rho c^2},\\quad |p_{\\mathrm{cav}}| = \\frac{|Q|}{\\omega C_A}', note: 'In a small cavity (headphone on ear), pressure follows cone DISPLACEMENT (flat below f_s); off the ear in free field it follows ACCELERATION.' }
      ]
    },
    {
      id: 'cs-8',
      title: '8. Hearing: Selectivity, Masking & Psychoacoustics (L9) → T12',
      solver: 'T12',
      keywords: 'ERB critical band power spectrum masking combination tones cubic difference tone beating sone phon upward spread loudness recruitment OHC IHC',
      items: [
        { label: 'ERB & Power-Spectrum Model of masking', formula: '\\mathrm{ERB} = 24.7(4.37F + 1)\\,\\mathrm{Hz}\\;(F\\text{ in kHz!}),\\qquad L_s = N_{0,\\mathrm{dB}} + 10\\log_{10}k + 10\\log_{10}\\min(\\Delta f_{\\mathrm{noise}},\\,\\mathrm{ERB})', note: 'At 0.1 / 0.5 / 1 / 2 / 4 / 10 kHz: ERB = 35.5 / 78.7 / 132.6 / 240.6 / 456.5 / 1104.1 Hz.' },
        { label: 'Combination tones, beating & sone/phon', formula: 'f_{\\mathrm{CT},n} = f_1 - n(f_2 - f_1)\\;(f_1 < f_2),\\quad f_{\\mathrm{CDT}} = 2f_1 - f_2,\\qquad N = 2^{(L_N - 40)/10}\\,\\mathrm{sone}', note: 'Two tones with |f₂ − f₁| < ERB fall in ONE filter and beat at |f₂ − f₁|; if |f₂ − f₁| > ERB they resolve into TWO separate filters.' },
        { label: 'High-yield Hearing MC facts', formula: '\\text{Base} = \\text{High } f\\;(\\text{stiff, narrow}),\\qquad \\text{Apex} = \\text{Low } f\\;(\\text{flexible, wide})', note: 'OHC = active amplifier & compressor (more gain for soft sounds, sharp tuning); IHC = sensory transducer to auditory nerve. Masking spreads UPWARD (towards higher frequencies). Filters broaden at high SPL and in SNHL (OHC damage → loss of sensitivity + loss of compression = loudness recruitment).' }
      ]
    },
    {
      id: 'cs-9',
      title: '9. Physiological Acoustics: Greenwood, OAE & ABR (L10) → T13',
      solver: 'T13',
      keywords: 'Greenwood map cochlea OAE latency roundtrip ABR averaging SNR artifact rejection middle ear canal',
      items: [
        { label: 'Greenwood map & OAE roundtrip latency', formula: 'F_c(x) = A\\cdot 10^{-Gx} - B,\\quad x = -\\frac{1}{G}\\log_{10}\\frac{F_c+B}{A},\\quad x_{\\mathrm{OAE}} = c_{\\mathrm{BM}}\\frac{t_{\\mathrm{rt}}}{2}', note: 'A = 20682, G = 61.765 m⁻¹, B = 140.6, x in METRES from the base (0 to 0.034 m → 20541 Hz to 23.7 Hz). Always halve OAE roundtrip time!' },
        { label: 'ABR signal averaging & artifact rejection', formula: '\\mathrm{SNR}_1 = 20\\log_{10}\\frac{\\mathrm{EP}}{N_1},\\quad \\mathrm{SNR}_n = \\mathrm{SNR}_1 + 10\\log_{10}n,\\quad N_{\\mathrm{eff}} = \\sqrt{(1-p)N_1^2 + p N_{\\mathrm{bad}}^2}', note: '+3.01 dB per doubling of sweeps. With rejection of fraction p bad sweeps: n_presented = n_clean / (1 − p).' },
        { label: 'Outer & middle ear numbers', formula: 'f_{\\mathrm{canal}} = \\frac{c}{4L} \\approx 3.4\\,\\mathrm{kHz}\\;(25\\,\\mathrm{mm}),\\qquad \\Delta L_{\\mathrm{ME}} \\approx 20\\log_{10}(14 \\times 1.3) \\approx 25\\,\\mathrm{dB}', note: 'Middle ear impedance matching overcomes most of the 29.5 dB air→fluid reflection loss.' }
      ]
    },
    {
      id: 'cs-10',
      title: '10. Vibration Isolation & Mobility (L11) → T14',
      solver: 'T14',
      keywords: 'vibration isolation static deflection resonance transmissibility damping mobility blocked force rigid floor accelerometer',
      items: [
        { label: 'Static deflection & natural frequency', formula: 's = \\frac{mg}{\\xi_0},\\qquad f_0 = \\frac{1}{2\\pi}\\sqrt{\\frac{s}{m}} = \\frac{1}{2\\pi}\\sqrt{\\frac{g}{\\xi_0}} \\approx \\frac{0.5}{\\sqrt{\\xi_0}}\\quad (\\xi_0\\text{ in metres!})', note: 'ξ₀ = 1 cm (0.01 m) → f₀ = 4.985 Hz (isolation starts at √2·f₀ = 7.05 Hz). ξ₀ = 1.5 cm (0.015 m) → f₀ = 4.07 Hz.' },
        { label: 'Transmissibility T & forced response', formula: 'T = \\sqrt{\\frac{1 + (2\\zeta\\Omega)^2}{(1-\\Omega^2)^2 + (2\\zeta\\Omega)^2}}\\quad (\\Omega = f/f_0),\\qquad |\\xi| = \\frac{F}{s|1-\\Omega^2|},\\quad |F_{\\mathrm{floor}}| = s|\\xi|', note: 'Below f₀: stiffness controlled. At f₀: damping controlled. Above f₀: mass controlled. Isolation (T < 1) ONLY for f > √2·f₀!' },
        { label: 'Mobility & blocked force', formula: 'F = \\frac{v_{\\mathrm{free}}}{Y_S + Y_R},\\qquad Y_{\\mathrm{mass}} = \\frac{1}{j\\omega m},\\quad Y_{\\mathrm{spring}} = \\frac{j\\omega}{s},\\quad Y_{\\mathrm{rigid}} = 0', note: 'For a mass source on a rigid floor (Y_R = 0): F = jωm·v_free (2023 MC11: j·3.14 N). Piezo accelerometer outputs CHARGE ∝ acceleration (2024 MC9).' }
      ]
    },
    {
      id: 'cs-11',
      title: '11. Sound Insulation (L12) → T15',
      solver: 'T15',
      keywords: 'sound insulation transmission loss mass law field incidence two rooms composite wall door window crack critical frequency coincidence double wall flanking impact',
      items: [
        { label: 'Mass law & two-room formula', formula: 'R_0 = 20\\log_{10}\\frac{\\omega m}{2\\rho c} \\approx 20\\log_{10}(fm) - 42.4,\\quad R_{\\mathrm{field}} = R_0 - 5\\,\\mathrm{dB},\\quad L_2 = L_1 - R + 10\\log_{10}\\frac{S}{A_2}', note: 'm = ρ_M h in kg/m² (+6 dB per doubling of f or m). S = partition wall area, A₂ = 0.16V₂/T₂ in receiver room.' },
        { label: 'Composite wall (door, window, crack)', formula: 'R_{\\mathrm{res}} = -10\\log_{10}\\left(\\frac{\\sum S_i 10^{-R_i/10}}{S_{\\mathrm{tot}}}\\right),\\qquad R_{\\mathrm{win}} = -10\\log_{10}\\left(\\frac{S_{\\mathrm{tot}}10^{-R_{\\mathrm{res}}/10} - S_{\\mathrm{wall}}10^{-R_{\\mathrm{wall}}/10}}{S_{\\mathrm{win}}}\\right)', note: 'Remember S_wall = S_tot − S_win! A crack has τ = 1 (R = 0 dB).' },
        { label: 'Critical (coincidence) frequency f_c', formula: 'B = \\frac{Eh^3}{12(1-\\nu^2)},\\quad m = \\rho_M h,\\quad f_c = \\frac{c^2}{2\\pi}\\sqrt{\\frac{m}{B}} \\propto \\frac{1}{h}', note: 'Thicker wall → LOWER f_c (10→15 cm concrete: 189→126 Hz, Δf_c = −63 Hz). Loose stacked plates: B and m both ×N → f_c UNCHANGED (2022 MC9).' },
        { label: 'Double wall (leaves m₁, m₂ separated by d)', formula: 'f_0 = \\frac{c}{2\\pi}\\sqrt{\\frac{\\rho}{d}\\left(\\frac{1}{m_1}+\\frac{1}{m_2}\\right)},\\quad f_d = \\frac{c}{2\\pi d},\\quad R(f > f_d) = R_1 + R_2 + 6\\,\\mathrm{dB}', note: 'For f₀ < f < f_d: R = R₁ + R₂ + 20 log₁₀(2kd). Below f₀: behaves like single wall of m₁ + m₂.' }
      ]
    }
  ];

  const workedPart1 = [
    {
      year: 2024,
      problem: '2024 P1 — Plane wave on a porous absorber + A-weighting',
      solver: 'T01',
      summary: '400 Hz (α = 0.9999, p_i = 0.9 Pa) and 630 Hz (α = 0.19, p_i = 0.4 + j0.4 Pa), R > 0. Find |p| at d = 0.6 m in front, and A-weighted SPL in the 500 Hz octave band.',
      steps: [
        'R_400 = √(1 − 0.9999) = 0.01;  R_630 = √(1 − 0.19) = 0.90.',
        'At x = −0.6 m: |p_400| = |0.9(e^{j·7.326·0.6} + 0.01 e^{−j·7.326·0.6})| = 0.89 Pa.',
        'At x = −0.6 m: |p_630| = |(0.4 + j0.4)(e^{j·11.54·0.6} + 0.9 e^{−j·11.54·0.6})| = 0.86 Pa.',
        'Both 400 and 630 Hz lie in the 500 Hz octave band (354–707 Hz). Apply K_A to each tone first: K_A(400) = −4.8 dB → p_A,rms = (0.89/√2)·10^{−4.8/20} = 0.363 Pa; K_A(630) = −1.9 dB → p_A,rms = (0.86/√2)·10^{−1.9/20} = 0.490 Pa.',
        'L_A = 20 log₁₀(√(0.363² + 0.490²) / 20 µPa) = 89.7 dB(A).'
      ]
    },
    {
      year: 2024,
      problem: '2024 P2 — Single monopole, then antiphase dipole on a line',
      solver: 'T06',
      summary: 'Q = 10⁻⁵ m³/s at 500 Hz (k = 9.16 rad/m). Q2.1: |p| and |u| at r = 0.1, 0.2, 0.3 m. Q2.2: Add second source at D = 0.4 m in antiphase; find p_rms, u_rms, I_x.',
      steps: [
        'Q2.1 (Single monopole): |p(r)| = ωρQ/(4πr) = 30.0 / 15.0 / 10.0 mPa at 0.1 / 0.2 / 0.3 m.',
        'Near-field velocity: |u(r)| = (|p|/ρc)√(1 + 1/(kr)²) = 108 / 41.5 / 25.9 µm/s (kr = 0.92, 1.83, 2.75).',
        'Q2.2 (Antiphase source at x = 0.4 m): p(x) = p₁(x) + p₂(x) with Q₂ = −Q₁; u_x(x) = u₁(x) − u₂(x) (two minus signs cancel so velocity terms add!).',
        'At x = 0.1 m: p_rms = 24.0 mPa, u_rms = 82.2 µm/s, I_x = +459.3 nW/m².',
        'At x = 0.2 m (midpoint): p_rms = 0 Pa, u_rms = 58.7 µm/s, I_x = 0 W/m².',
        'At x = 0.3 m: p_rms = 24.0 mPa, u_rms = 82.2 µm/s, I_x = −459.3 nW/m².'
      ]
    },
    {
      year: 2023,
      problem: '2023 P1 — Vibrating end wall in a 20 m tunnel (absorber vs water)',
      solver: 'T02',
      summary: 'f = 240 Hz (k = 4.396 rad/m), U₀ = 1 mm/s peak, L = 20 m, field point 8 m from wall (x = −12 m). Q1.1: α = 1 absorber. Q1.2: Water-soaked (R ≈ 1).',
      steps: [
        'Q1.1 (Absorber, R = 0): Pure progressive plane wave. |p| = ρc·U₀ = 411.6 × 10⁻³ = 0.4116 Pa → p_rms = 0.291 Pa → SPL = 83.3 dB (official rounds 0.412/√2 to 0.286 Pa → 83.1 dB).',
        'Q1.2 (Water termination, Z_w = 1.48×10⁶ ≫ ρc → R = 0.9994 ≈ +1): Standing wave with p(x) = 2A cos(kx), u(x) = (−2jA/ρc)sin(kx).',
        'Match u(−20) = U₀ → A = ρcU₀ / (2j sin(20k)) = −j 5.62 Pa (note sin(20k) = 0.037 is right next to a closed-closed tunnel resonance!).',
        'At x = −12 m: |p(−12)| = |2A cos(12k)| = 8.94 Pa peak → SPL = 110.0 dB (official: 109.9 dB).'
      ]
    },
    {
      year: 2023,
      problem: '2023 P2 — Two cello strings in octave bands + 1% detuning',
      solver: 'T04',
      summary: 'String 1: 334 (0.1), 668 (j0.001), 1002 (0.04) Pa. String 2: 501 (0.2), 1002 (0.05), 1503 (j0.02) Pa. Octave bands 125–2000 Hz.',
      steps: [
        'Q2.1: Merge the two 1002 Hz components coherently: P(1002) = 0.04 + 0.05 = 0.09 Pa peak → p_rms = 0.0636 Pa.',
        '125 Hz [88–177]: empty → 0 Pa, −∞ dB.',
        '250 Hz [177–354]: 334 Hz (0.1 Pa) → p_rms = 0.0707 Pa → 71.0 dB (official 70.9 dB).',
        '500 Hz [354–707]: 501 Hz (0.2) + 668 Hz (j0.001) → p_rms = √(0.2² + 0.001²)/√2 = 0.1414 Pa → 77.0 dB.',
        '1000 Hz [707–1414]: merged 1002 Hz (0.09 Pa) → p_rms = 0.0636 Pa → 70.1 dB.',
        '2000 Hz [1414–2828]: 1503 Hz (j0.02) → p_rms = 0.0141 Pa → 57.0 dB.',
        'Q2.2 (1% detuned): All components stay in their bands, but 992 Hz and 1002 Hz are now different frequencies → add as squares in 1 kHz band: p_rms = √(0.04² + 0.05²)/√2 = 0.0453 Pa → 67.1 dB (−3.0 dB).'
      ]
    },
    {
      year: 2023,
      problem: '2023 P3 — Monopole 2 m from a rigid wall (power & line intensity)',
      solver: 'T07',
      summary: 'h = 2 m. Q3.1: Power at 20 Hz (Q=3e-3), 200 Hz (Q=4e-4), 2 kHz (Q=5e-5). Q3.2: Intensity at 200 Hz at 0, 0.5, 1 m from wall.',
      steps: [
        'Q3.1: Image source at 2h = 4 m in phase: W = (ρck²|Q|² / 8π)·(1 + sin(2kh)/(2kh)).',
        'Gives W = 33.2 µW (20 Hz), 37.3 µW (200 Hz), 55.3 µW (2 kHz) with ρ = 1.2 (official prints 32.7 / 36.6 / 54.4 µW using ρ ≈ 1.18).',
        'Q3.2: At d_wall = 0, 0.5, 1.0 m (r₁ = 2, 1.5, 1.0 m; r₂ = 2, 2.5, 3.0 m): |p₁| = 0.024, 0.032, 0.048 Pa; |p₂| = 0.024, 0.0192, 0.016 Pa.',
        'Official plane-wave counter-propagating formula I ≈ (|p₁|² − |p₂|²)/(2ρc) gives 0 / 0.80 / 2.49 µW/m² (official ρ=1.18: 0 / 0.78 / 2.45 µW/m²; exact with near-field cross terms: 0 / 0.69 / 2.78 µW/m²).'
      ]
    },
    {
      year: 2022,
      problem: '2022 P1 — Loudspeaker in an infinite baffle',
      solver: 'T08',
      summary: 'R_e = 5 Ω, Bl = 2 Tm, M = 10 g, K = 1500 N/m, R_t = 2.5 Ns/m, a = 6 cm, infinite baffle (2π), 4 V rms at 200 Hz, r = 5 m.',
      steps: [
        'S = π(0.06)² = 0.01131 m², ω = 2π(200) = 1256.6 rad/s, ka = 0.22 < 1 (monopole in half-space Ω = 2π).',
        'Z_M = 2.5 + j(12.57 − 1.19) = 2.5 + j11.37 Ns/m (|Z_M| = 11.64 Ns/m).',
        '|Q| = S·Bl·(√2 e_rms) / (R_e |Z_M|) = 0.01131 × 2 × 5.657 / (5 × 11.64) = 2.20×10⁻³ m³/s (peak).',
        '|p(5 m)| = ρω|Q| / (2πr) = 1.2 × 1256.6 × 0.00220 / (2π × 5) = 0.1055 Pa peak (71.4 dB SPL).',
        'W = 2πr² |p|² / (2ρc) = 2π(25)(0.1055²) / 823.2 = 2.12 mW.'
      ]
    },
    {
      year: 2022,
      problem: '2022 P2 — Two sources in octave bands (250, 500, 1000, 2000 Hz)',
      solver: 'T04',
      summary: 'Source 1: 400 (0.1), 800 (0.02), 1200 (0.01) Pa. Source 2: 600 (j0.05), 900 (j0.03), 1200 (j0.01), 1500 (j0.006) Pa.',
      steps: [
        'At 1200 Hz both sources are active → add complex amplitudes first: |0.01 + j0.01| = 0.01414 Pa peak → p_rms(1200) = 0.010 Pa.',
        '250 Hz [177–354]: no tones → 0 Pa, −∞ dB.',
        '500 Hz [354–707]: 400 (0.1) & 600 (j0.05) → p_rms = √((0.1² + 0.05²)/2) = 0.0791 Pa → 71.9 dB.',
        '1000 Hz [707–1414]: 800 (0.02), 900 (j0.03) & merged 1200 → p_rms = √(0.02²/2 + 0.03²/2 + 0.01²) = 0.0274 Pa → 62.73 dB.',
        '2000 Hz [1414–2828]: 1500 (j0.006) → p_rms = 0.006/√2 = 0.00424 Pa → 46.53 dB.'
      ]
    },
    {
      year: 2022,
      problem: '2022 P3 — Two in-phase monopoles 4 m apart (cancellation & midpoint I)',
      solver: 'T07',
      summary: 'D = 4 m, lowest cancellation frequency at x_c is f₀ = 500 Hz. Midpoint SPL = 80 dB.',
      steps: [
        'Q3.1: Complete cancellation requires equal pressure amplitudes (|p₁| = |p₂|) and 180° phase difference.',
        'Q3.2: Path difference Δx = (2n+1)λ/2 → cancellation frequencies are odd multiples of 500 Hz: 1500, 2500, 3500 Hz…',
        'Q3.3: Δx = 2(x_c − 2) = c/(2f₀) = 0.343 m → x_c = 2 + 0.1715 = 2.172 m. Equal amplitude at x_c requires |Q₁|/|Q₂| = x_c/(4 − x_c) = 2.1715/1.8285 = 1.188 (+1.5 dB).',
        'Q3.4: At midpoint (x = 2 m), both waves arrive in phase: p_rms,tot = 0.2 Pa = p₁ + p₂ with p₁ = 1.188 p₂ → p₂ = 0.0914 Pa, p₁ = 0.1086 Pa. Counter-propagating intensity: I_x = (p₁² − p₂²)/(ρc) = 8.33 µW/m² towards source 2.'
      ]
    }
  ];

  const checklist = {
    timePlan: [
      { time: '09:00–09:10 (10 m)', phase: 'Read & Tag', detail: 'Read both parts. Write the solver code (T01–T15) next to each question. Verify cover-page constants (ρ = 1.2 kg/m³, c = 343 m/s).' },
      { time: '09:10–10:20 (70 m)', phase: 'Part 2 — 15 MC (60%)', detail: 'First pass (~4–5 min each). Do the 4 Hearing questions in 3 min using Cheat Sheet §8–9. Use T01–T15 for the calculation MCs. Flag anything > 6 min.' },
      { time: '10:20–12:05 (105 m)', phase: 'Part 1 — Problems (40%)', detail: '~35 min per problem. For each: (1) state field type (plane, standing, spherical 2π/4π), (2) plug givens into solver, (3) copy step-by-step formula → substituted numbers → result WITH UNITS + one physical sentence.' },
      { time: '12:05–12:25 (20 m)', phase: 'Flagged MC & Sanity Check', detail: 'Finish any flagged MC questions. Check peak vs RMS (√2), 2π vs 4π, and coherent vs incoherent on every problem.' },
      { time: '12:25–12:40 (15 m)', phase: 'Build & Verify PDF', detail: 'Export Part 1 hand-in to ONE combined PDF. Open the PDF, check page order, units, and readability, then upload to Digital Exam.' },
      { time: '12:40–13:00 (20 m)', phase: 'Safety Buffer', detail: 'Do not start new rewrites after 12:45. Double-check all 15 MC answers are saved.' }
    ],
    items: [
      { id: 'chk-1', cat: 'Before Exam Day', text: 'Test exam-app.html offline (Wi-Fi OFF, open via file://) and verify all solvers & KaTeX math render cleanly.' },
      { id: 'chk-2', cat: 'Before Exam Day', text: 'Test MATLAB offline with Wi-Fi OFF (`run_all_checks` → 116/116 pass) or confirm offline license / Octave backup.' },
      { id: 'chk-3', cat: 'Before Exam Day', text: 'Confirm offline PDF export route (Print to PDF from this app’s Hand-in Builder, Obsidian Export to PDF, or LibreOffice Writer).' },
      { id: 'chk-4', cat: 'Before Exam Day', text: 'Print paper backups: Cheat Sheet PDF (2 pages A4) and Worked Old Exams 2022–2024.' },
      { id: 'chk-5', cat: 'Part 1 Hand-in Quality', text: 'Checked PEAK vs RMS on every given pressure, velocity, and voltage (divide peak by √2 for SPL; multiply RMS voltage by √2 for peak phasors).' },
      { id: 'chk-6', cat: 'Part 1 Hand-in Quality', text: 'Checked 2π (baffle / rigid ground) vs 4π (free space) on every radiation / loudspeaker problem.' },
      { id: 'chk-7', cat: 'Part 1 Hand-in Quality', text: 'Checked SAME frequency (complex sum first!) vs DIFFERENT frequencies (sum of squared RMS pressures) on every multi-tone / octave-band problem.' },
      { id: 'chk-8', cat: 'Part 1 Hand-in Quality', text: 'Written explicit UNITS (Pa, m/s, m³/s, W/m², W, dB re 20 µPa, dB(A), Hz, s) on every final number.' },
      { id: 'chk-9', cat: 'Part 1 Hand-in Quality', text: 'Included a 1-sentence physical description where asked (e.g., "Progressive plane wave with constant amplitude" vs "Standing wave near resonance").' },
      { id: 'chk-10', cat: 'Final Submission', text: 'All 15 Multiple-Choice answers selected in Part 2 and single Part 1 PDF verified & uploaded.' }
    ]
  };

  return { sections, workedPart1, checklist };
});
