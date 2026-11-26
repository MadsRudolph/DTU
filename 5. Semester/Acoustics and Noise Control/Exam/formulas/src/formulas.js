// 34840 formula sheets: one topic per page, every formula solvable for any one of its quantities.
// Each formula: name, tex (shown), txt (plain form, used for the worked line; tokens = variable keys),
// vars (keys in this topic), f(v) = residual (zero when the formula holds), optional note.
// Constants available in every formula: c, rho, p0, I0, W0, g.
// Variable spec: [TeX symbol, unit, description, domain]; domain defaults to 'pos'.
//   pos  > 0 (log grid)     db   decibels (−500…500)    any  either sign
//   unit 0…1                sym  −1…1                   ge1  ≥ 1
//   deg90 0…90°             int  integer, never solved for

(function (root) {
  'use strict';
  const L10 = Math.log10, PI = Math.PI, sq = Math.sqrt;

  // IEC 61672 analytic A- and C-weighting (dB)
  function aWeight(f) {
    const f2 = f * f;
    const ra = (12194 ** 2 * f2 * f2) / ((f2 + 20.6 ** 2) * sq((f2 + 107.7 ** 2) * (f2 + 737.9 ** 2)) * (f2 + 12194 ** 2));
    return 20 * L10(ra) + 2.0;
  }
  function cWeight(f) {
    const f2 = f * f;
    const rc = (12194 ** 2 * f2) / ((f2 + 20.6 ** 2) * (f2 + 12194 ** 2));
    return 20 * L10(rc) + 0.06;
  }

  const CONSTANTS = {
    c: { sym: 'c', unit: 'm/s', name: 'speed of sound', value: 343, editable: true },
    rho: { sym: '\\rho', unit: 'kg/m³', name: 'density of air', value: 1.2, editable: true },
    p0: { sym: 'p_0', unit: 'Pa', name: 'reference pressure', value: 20e-6 },
    I0: { sym: 'I_0', unit: 'W/m²', name: 'reference intensity', value: 1e-12 },
    W0: { sym: 'W_0', unit: 'W', name: 'reference power', value: 1e-12 },
    g: { sym: 'g', unit: 'm/s²', name: 'gravity', value: 9.81 },
  };

  const TOPICS = [
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 1', 'Lecture Notes/Lecture 1 - Introduction and Plane Waves.md'], ['Lecture 3', 'Lecture Notes/Lecture 3 - Decibels Frequency Analysis and Measurements.md'], ['Lecture 4', 'Lecture Notes/Lecture 4 - Impedance Intensity and Sound Power.md'], ['Week 1 worked', 'Exercises/Work/Week 1 - Fundamental Concepts and Plane Waves.md'], ['Week 3 worked', 'Exercises/Work/Week 3 - Decibels Frequency Analysis and Measurements.md'], ['Week 4 worked', 'Exercises/Work/Week 4 - Impedance Intensity and Sound Power.md']],
      id: 'levels', title: 'Levels and waves',
      blurb: 'Pressure, intensity and power, and their decibel levels.',
      vars: {
        f: ['f', 'Hz', 'frequency'], w: ['\\omega', 'rad/s', 'angular frequency'],
        lam: ['\\lambda', 'm', 'wavelength'], k: ['k', 'rad/m', 'wavenumber'],
        pk: ['\\hat p', 'Pa', 'peak pressure'], p: ['p_{\\rm rms}', 'Pa', 'rms pressure'],
        Lp: ['L_p', 'dB', 'sound pressure level', 'db'],
        I: ['I', 'W/m²', 'intensity'], LI: ['L_I', 'dB', 'intensity level', 'db'],
        u: ['u_{\\rm rms}', 'm/s', 'particle velocity'],
        W: ['W', 'W', 'sound power'], S: ['S', 'm²', 'area'], LW: ['L_W', 'dB', 'sound power level', 'db'],
      },
      formulas: [
        { name: 'Angular frequency', tex: '\\omega = 2\\pi f', txt: 'w = 2*pi*f', vars: ['w', 'f'], f: v => v.w - 2 * PI * v.f },
        { name: 'Wavelength', tex: '\\lambda = \\dfrac{c}{f}', txt: 'lam = c/f', vars: ['lam', 'f'], f: v => v.lam - v.c / v.f },
        { name: 'Wavenumber', tex: 'k = \\dfrac{\\omega}{c}', txt: 'k = w/c', vars: ['k', 'w'], f: v => v.k - v.w / v.c },
        { name: 'Peak and rms', tex: 'p_{\\rm rms} = \\dfrac{\\hat p}{\\sqrt 2}', txt: 'p = pk/sqrt(2)', vars: ['p', 'pk'], f: v => v.p - v.pk / Math.SQRT2, note: 'Pure tone only. A complex amplitude in the exam text is a peak value.' },
        { name: 'Sound pressure level', tex: 'L_p = 20\\log_{10}\\dfrac{p_{\\rm rms}}{p_0}', txt: 'Lp = 20*log10(p/p0)', vars: ['Lp', 'p'], f: v => v.Lp - 20 * L10(v.p / v.p0) },
        { name: 'Intensity of a plane wave', tex: 'I = \\dfrac{p_{\\rm rms}^2}{\\rho c}', txt: 'I = p^2/(rho*c)', vars: ['I', 'p'], f: v => v.I - v.p * v.p / (v.rho * v.c), note: 'Also holds for a spherical wave in the far field (kr ≫ 1).' },
        { name: 'Intensity level', tex: 'L_I = 10\\log_{10}\\dfrac{I}{I_0}', txt: 'LI = 10*log10(I/I0)', vars: ['LI', 'I'], f: v => v.LI - 10 * L10(v.I / v.I0) },
        { name: 'Particle velocity', tex: 'u_{\\rm rms} = \\dfrac{p_{\\rm rms}}{\\rho c}', txt: 'u = p/(rho*c)', vars: ['u', 'p'], f: v => v.u - v.p / (v.rho * v.c), note: 'Plane wave.' },
        { name: 'Power through an area', tex: 'W = I\\,S', txt: 'W = I*S', vars: ['W', 'I', 'S'], f: v => v.W - v.I * v.S, note: 'Uniform intensity over S.' },
        { name: 'Sound power level', tex: 'L_W = 10\\log_{10}\\dfrac{W}{W_0}', txt: 'LW = 10*log10(W/W0)', vars: ['LW', 'W'], f: v => v.LW - 10 * L10(v.W / v.W0) },
      ],
      widgets: ['combine'],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 1', 'Lecture Notes/Lecture 1 - Introduction and Plane Waves.md'], ['Lecture 2', 'Lecture Notes/Lecture 2 - Plane Waves Reflection and Spherical Waves.md'], ['Lecture 4', 'Lecture Notes/Lecture 4 - Impedance Intensity and Sound Power.md'], ['Week 1 worked', 'Exercises/Work/Week 1 - Fundamental Concepts and Plane Waves.md'], ['Week 2 worked', 'Exercises/Work/Week 2 - Reflection and Spherical Waves.md'], ['Week 4 worked', 'Exercises/Work/Week 4 - Impedance Intensity and Sound Power.md']],
      id: 'plane', title: 'Plane waves and tubes',
      blurb: 'Reflection at a surface, standing waves, transmission between media, tube resonances.',
      vars: {
        Z: ['Z', 'Pa·s/m', 'surface impedance p/u at the surface (real)'], R: ['R', '', 'pressure reflection coefficient p_r/p_i', 'sym'],
        al: ['\\alpha', '', 'absorption coefficient', 'unit'],
        Lmax: ['L_{\\max}', 'dB', 'level at a maximum', 'db'], Lmin: ['L_{\\min}', 'dB', 'level at a minimum', 'db'],
        dL: ['\\Delta L', 'dB', 'max − min', 'db'], s: ['s', '', 'standing wave ratio', 'ge1'],
        Z1: ['Z_1', 'Pa·s/m', 'impedance, medium 1'], Z2: ['Z_2', 'Pa·s/m', 'impedance, medium 2'],
        tau: ['\\tau', '', 'power transmission coefficient', 'unit'], TL: ['\\Delta L_\\tau', 'dB', 'transmission loss', 'db'],
        n: ['n', '', 'mode number', 'int'], Lt: ['L', 'm', 'tube length'],
        fn: ['f_n', 'Hz', 'resonance, both ends alike'], fq: ['f_n', 'Hz', 'resonance, one end open'],
        f: ['f', 'Hz', 'frequency'], dmin: ['d_{\\min}', 'm', 'first minimum from the wall'],
        k: ['k', 'rad/m', 'wavenumber'], d: ['d', 'm', 'distance in front of the surface'],
        pin: ['|p_i|', 'Pa', 'incident amplitude'], pd: ['|p(d)|', 'Pa', 'total amplitude at d'],
      },
      formulas: [
        { name: 'Reflection coefficient', tex: 'R = \\dfrac{Z - \\rho c}{Z + \\rho c}', txt: 'R = (Z - rho*c)/(Z + rho*c)', vars: ['R', 'Z'], f: v => v.R - (v.Z - v.rho * v.c) / (v.Z + v.rho * v.c), note: 'Normal incidence, real impedance. Soft surface (Z < ρc) gives R < 0.' },
        { name: 'Absorption coefficient', tex: '\\alpha = 1 - R^2', txt: 'al = 1 - R^2', vars: ['al', 'R'], f: v => v.al - (1 - v.R * v.R), prefer: () => 1, note: 'Two signs of R give the same α. The page takes R > 0 (hard, pressure maximum at the surface); type a negative R for a soft surface.' },
        { name: 'Wavenumber', tex: 'k = \\dfrac{2\\pi f}{c}', txt: 'k = 2*pi*f/c', vars: ['k', 'f'], f: v => v.k - 2 * PI * v.f / v.c },
        { name: 'Pressure in front of a reflecting surface', tex: '|p(d)| = |p_i|\\sqrt{1 + R^2 + 2R\\cos(2kd)}', txt: 'pd = pin*sqrt(1 + R^2 + 2*R*cos(2*k*d))', vars: ['pd', 'pin', 'R', 'k', 'd'], f: v => v.pd - v.pin * sq(1 + v.R * v.R + 2 * v.R * Math.cos(2 * v.k * v.d)), note: 'Incident plus reflected plane wave, real R, normal incidence. From p(x) = p_i(e^{−jkx} + R e^{jkx}) at x = −d. For a complex amplitude like 0.4 + j0.4, use its magnitude: abs(0.4+0.4j). Peak in, peak out.' },
        { name: 'Level difference in the standing wave', tex: '\\Delta L = L_{\\max} - L_{\\min}', txt: 'dL = Lmax - Lmin', vars: ['dL', 'Lmax', 'Lmin'], f: v => v.dL - (v.Lmax - v.Lmin) },
        { name: 'Standing wave ratio', tex: 's = 10^{\\Delta L/20}', txt: 's = 10^(dL/20)', vars: ['s', 'dL'], f: v => v.s - 10 ** (v.dL / 20) },
        { name: 'Absorption from the standing wave ratio', tex: '\\alpha = \\dfrac{4s}{(s+1)^2}', txt: 'al = 4*s/(s + 1)^2', vars: ['al', 's'], f: v => v.al - 4 * v.s / (v.s + 1) ** 2 },
        { name: 'Transmission between two media', tex: '\\tau = \\dfrac{4Z_1Z_2}{(Z_1+Z_2)^2}', txt: 'tau = 4*Z1*Z2/(Z1 + Z2)^2', vars: ['tau', 'Z1', 'Z2'], f: v => v.tau - 4 * v.Z1 * v.Z2 / (v.Z1 + v.Z2) ** 2, note: 'Air ρc ≈ 412, water ≈ 1.48·10⁶ Pa·s/m.' },
        { name: 'Transmission loss', tex: '\\Delta L_\\tau = -10\\log_{10}\\tau', txt: 'TL = -10*log10(tau)', vars: ['TL', 'tau'], f: v => v.TL + 10 * L10(v.tau) },
        { name: 'Tube with both ends closed (or both open)', tex: 'f_n = \\dfrac{n\\,c}{2L}', txt: 'fn = n*c/(2*Lt)', vars: ['fn', 'n', 'Lt'], f: v => v.fn - v.n * v.c / (2 * v.Lt) },
        { name: 'Tube with one end open', tex: 'f_n = \\dfrac{(2n-1)\\,c}{4L}', txt: 'fq = (2*n - 1)*c/(4*Lt)', vars: ['fq', 'n', 'Lt'], f: v => v.fq - (2 * v.n - 1) * v.c / (4 * v.Lt) },
        { name: 'First pressure minimum in front of a hard wall', tex: 'd_{\\min} = \\dfrac{\\lambda}{4} = \\dfrac{c}{4f}', txt: 'dmin = c/(4*f)', vars: ['dmin', 'f'], f: v => v.dmin - v.c / (4 * v.f) },
      ],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 2', 'Lecture Notes/Lecture 2 - Plane Waves Reflection and Spherical Waves.md'], ['Lecture 5', 'Lecture Notes/Lecture 5 - Radiation Monopoles Dipoles and Pistons.md'], ['Week 2 worked', 'Exercises/Work/Week 2 - Reflection and Spherical Waves.md'], ['Week 5 worked', 'Exercises/Work/Week 5 - Radiation Monopoles Dipoles and Pistons.md']],
      id: 'sources', title: 'Point sources',
      blurb: 'The monopole, its near field, directivity and distance.',
      vars: {
        f: ['f', 'Hz', 'frequency'], k: ['k', 'rad/m', 'wavenumber'], r: ['r', 'm', 'distance'],
        kr: ['kr', '', 'Helmholtz number'], phi: ['\\varphi', '°', 'phase of p ahead of u', 'deg90'],
        zr: ['|Z_s|/\\rho c', '', 'specific impedance, normalised', 'unit'],
        Qv: ['Q_{\\rm rms}', 'm³/s', 'volume velocity'], p: ['p_{\\rm rms}', 'Pa', 'rms pressure'],
        Lp: ['L_p', 'dB', 'sound pressure level', 'db'], W: ['W', 'W', 'sound power'], LW: ['L_W', 'dB', 'sound power level', 'db'],
        Q: ['Q', '', 'directivity factor'], I: ['I', 'W/m²', 'intensity'], DI: ['DI', 'dB', 'directivity index', 'db'],
        L1: ['L_1', 'dB', 'level at r₁', 'db'], L2: ['L_2', 'dB', 'level at r₂', 'db'], r1: ['r_1', 'm', 'distance 1'], r2: ['r_2', 'm', 'distance 2'],
      },
      formulas: [
        { name: 'Wavenumber', tex: 'k = \\dfrac{2\\pi f}{c}', txt: 'k = 2*pi*f/c', vars: ['k', 'f'], f: v => v.k - 2 * PI * v.f / v.c },
        { name: 'Helmholtz number', tex: 'kr', txt: 'kr = k*r', vars: ['kr', 'k', 'r'], f: v => v.kr - v.k * v.r, note: 'kr ≪ 1 near field, kr ≫ 1 far field.' },
        { name: 'Phase between pressure and particle velocity', tex: '\\varphi = \\arctan\\dfrac{1}{kr}', txt: 'phi = atan(1/kr)', matlab: 'phi = atand(1./kr)', vars: ['phi', 'kr'], f: v => v.phi - Math.atan(1 / v.kr) * 180 / PI, note: 'Not arctan(kr): that is the classic trap.' },
        { name: 'Specific impedance magnitude', tex: '\\dfrac{|Z_s|}{\\rho c} = \\dfrac{kr}{\\sqrt{1+(kr)^2}}', txt: 'zr = kr/sqrt(1 + kr^2)', vars: ['zr', 'kr'], f: v => v.zr - v.kr / sq(1 + v.kr * v.kr) },
        { name: 'Pressure of a monopole', tex: 'p_{\\rm rms} = \\dfrac{\\rho c k\\,Q_{\\rm rms}}{4\\pi r}', txt: 'p = rho*c*k*Qv/(4*pi*r)', vars: ['p', 'k', 'Qv', 'r'], f: v => v.p - v.rho * v.c * v.k * v.Qv / (4 * PI * v.r), note: 'Free field. Use peak Q for peak p.' },
        { name: 'Power of a monopole', tex: 'W = \\dfrac{\\rho c k^2 Q_{\\rm rms}^2}{4\\pi}', txt: 'W = rho*c*k^2*Qv^2/(4*pi)', vars: ['W', 'k', 'Qv'], f: v => v.W - v.rho * v.c * v.k * v.k * v.Qv * v.Qv / (4 * PI), note: 'With a peak Q it is 8π in the denominator.' },
        { name: 'Intensity at distance r', tex: 'I = \\dfrac{Q\\,W}{4\\pi r^2}', txt: 'I = Q*W/(4*pi*r^2)', vars: ['I', 'Q', 'W', 'r'], f: v => v.I - v.Q * v.W / (4 * PI * v.r * v.r), note: 'Q = 1 free field, 2 on a floor, 4 at an edge, 8 in a corner.' },
        { name: 'Level from power', tex: 'L_p = L_W + 10\\log_{10}\\dfrac{Q}{4\\pi r^2} + 10\\log_{10}\\dfrac{\\rho c\\,W_0}{p_0^2}', txt: 'Lp = LW + 10*log10(Q/(4*pi*r^2)) + 10*log10(rho*c*W0/p0^2)', vars: ['Lp', 'LW', 'Q', 'r'], f: v => v.Lp - (v.LW + 10 * L10(v.Q / (4 * PI * v.r * v.r)) + 10 * L10(v.rho * v.c * v.W0 / (v.p0 * v.p0))), note: 'The last term is +0.1 dB; most solutions drop it.' },
        { name: 'Sound pressure level', tex: 'L_p = 20\\log_{10}\\dfrac{p_{\\rm rms}}{p_0}', txt: 'Lp = 20*log10(p/p0)', vars: ['Lp', 'p'], f: v => v.Lp - 20 * L10(v.p / v.p0) },
        { name: 'Sound power level', tex: 'L_W = 10\\log_{10}\\dfrac{W}{W_0}', txt: 'LW = 10*log10(W/W0)', vars: ['LW', 'W'], f: v => v.LW - 10 * L10(v.W / v.W0) },
        { name: 'Directivity index', tex: 'DI = 10\\log_{10} Q', txt: 'DI = 10*log10(Q)', vars: ['DI', 'Q'], f: v => v.DI - 10 * L10(v.Q) },
        { name: 'Distance law', tex: 'L_2 = L_1 - 20\\log_{10}\\dfrac{r_2}{r_1}', txt: 'L2 = L1 - 20*log10(r2/r1)', vars: ['L2', 'L1', 'r2', 'r1'], f: v => v.L2 - (v.L1 - 20 * L10(v.r2 / v.r1)), note: 'Point source, free field: −6 dB per doubling. A line source loses 10 log instead (−3 dB).' },
      ],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 3', 'Lecture Notes/Lecture 3 - Decibels Frequency Analysis and Measurements.md'], ['Lecture 5', 'Lecture Notes/Lecture 5 - Radiation Monopoles Dipoles and Pistons.md'], ['Week 5 worked', 'Exercises/Work/Week 5 - Radiation Monopoles Dipoles and Pistons.md']],
      id: 'interference', title: 'Two sources',
      blurb: 'Adding two tones, path differences, the dipole and a source above a floor.',
      vars: {
        f: ['f', 'Hz', 'frequency'], k: ['k', 'rad/m', 'wavenumber'],
        dr: ['\\Delta r', 'm', 'path difference'], dphi: ['\\Delta\\varphi', '°', 'phase difference', 'any'],
        L1: ['L_1', 'dB', 'level of source 1 alone', 'db'], L2: ['L_2', 'dB', 'level of source 2 alone', 'db'],
        a: ['a', '', 'amplitude ratio p₂/p₁'],
        Lc: ['L_{\\rm coh}', 'dB', 'total, same frequency', 'db'], Li: ['L_{\\rm inc}', 'dB', 'total, different frequencies', 'db'],
        d: ['d', 'm', 'spacing'], Wd: ['\\Delta L_W', 'dB', 'dipole vs one monopole', 'db'],
        h: ['h', 'm', 'height above the floor'], Wh: ['\\Delta L_W', 'dB', 'source over floor vs free field', 'db'],
      },
      formulas: [
        { name: 'Wavenumber', tex: 'k = \\dfrac{2\\pi f}{c}', txt: 'k = 2*pi*f/c', vars: ['k', 'f'], f: v => v.k - 2 * PI * v.f / v.c },
        { name: 'Phase from path difference', tex: '\\Delta\\varphi = k\\,\\Delta r', txt: 'dphi = k*dr*180/pi', vars: ['dphi', 'k', 'dr'], f: v => v.dphi - v.k * v.dr * 180 / PI, note: 'In degrees. Add the sources’ own phase difference if they are not in phase.' },
        { name: 'Amplitude ratio', tex: 'a = 10^{(L_2-L_1)/20}', txt: 'a = 10^((L2 - L1)/20)', vars: ['a', 'L2', 'L1'], f: v => v.a - 10 ** ((v.L2 - v.L1) / 20) },
        { name: 'Coherent sum (same frequency)', tex: 'L_{\\rm coh} = L_1 + 10\\log_{10}\\left(1 + a^2 + 2a\\cos\\Delta\\varphi\\right)', txt: 'Lc = L1 + 10*log10(1 + a^2 + 2*a*cos(dphi))', matlab: 'Lc = L1 + 10*log10(1 + a.^2 + 2*a.*cosd(dphi))', vars: ['Lc', 'L1', 'a', 'dphi'], f: v => v.Lc - (v.L1 + 10 * L10(1 + v.a * v.a + 2 * v.a * Math.cos(v.dphi * PI / 180))), note: 'Equal sources: +6 dB in phase, total cancellation at 180°.' },
        { name: 'Incoherent sum (different frequencies, noise)', tex: 'L_{\\rm inc} = L_1 + 10\\log_{10}(1 + a^2)', txt: 'Li = L1 + 10*log10(1 + a^2)', vars: ['Li', 'L1', 'a'], f: v => v.Li - (v.L1 + 10 * L10(1 + v.a * v.a)), note: 'Two equal sources: +3 dB.' },
        { name: 'Dipole power', tex: '\\Delta L_W = 10\\log_{10}\\left[2\\left(1 - \\dfrac{\\sin kd}{kd}\\right)\\right] \\approx 10\\log_{10}\\dfrac{(kd)^2}{3}', txt: 'Wd = 10*log10(2*(1 - sin(k*d)/(k*d)))', vars: ['Wd', 'k', 'd'], f: v => v.Wd - 10 * L10(2 * (1 - Math.sin(v.k * v.d) / (v.k * v.d))), note: 'Two antiphase monopoles, relative to one of them alone. Very inefficient at low frequency (kd ≪ 1).' },
        { name: 'Monopole above a hard floor', tex: '\\Delta L_W = 10\\log_{10}\\left(1 + \\dfrac{\\sin 2kh}{2kh}\\right)', txt: 'Wh = 10*log10(1 + sin(2*k*h)/(2*k*h))', vars: ['Wh', 'k', 'h'], f: v => v.Wh - 10 * L10(1 + Math.sin(2 * v.k * v.h) / (2 * v.k * v.h)), note: 'Relative to the same source in free field: +3 dB when kh ≪ 1 (Q = 2).' },
      ],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 6', 'Lecture Notes/Lecture 6 - Room Modes and the Diffuse Sound Field.md'], ['Week 6 worked', 'Exercises/Work/Week 6 - Room Modes and the Diffuse Sound Field.md']],
      id: 'modes', title: 'Room modes',
      blurb: 'Standing waves in a rectangular room, mode count and the Schroeder frequency.',
      vars: {
        Lx: ['L_x', 'm', 'length'], Ly: ['L_y', 'm', 'width'], Lz: ['L_z', 'm', 'height'],
        nx: ['n_x', '', 'mode number x', 'int'], ny: ['n_y', '', 'mode number y', 'int'], nz: ['n_z', '', 'mode number z', 'int'],
        fm: ['f_{n_x n_y n_z}', 'Hz', 'mode frequency'], V: ['V', 'm³', 'volume'],
        f: ['f', 'Hz', 'frequency'], N: ['N', '', 'number of modes below f'],
        T: ['T', 's', 'reverberation time'], fS: ['f_S', 'Hz', 'Schroeder frequency'],
      },
      formulas: [
        { name: 'Mode frequency', tex: 'f = \\dfrac{c}{2}\\sqrt{\\left(\\dfrac{n_x}{L_x}\\right)^2 + \\left(\\dfrac{n_y}{L_y}\\right)^2 + \\left(\\dfrac{n_z}{L_z}\\right)^2}', txt: 'fm = c/2*sqrt((nx/Lx)^2 + (ny/Ly)^2 + (nz/Lz)^2)', vars: ['fm', 'nx', 'ny', 'nz', 'Lx', 'Ly', 'Lz'], f: v => v.fm - v.c / 2 * sq((v.nx / v.Lx) ** 2 + (v.ny / v.Ly) ** 2 + (v.nz / v.Lz) ** 2), note: 'Every mode has a pressure maximum in all corners. The centre is a maximum only when all n are even.' },
        { name: 'Volume', tex: 'V = L_x L_y L_z', txt: 'V = Lx*Ly*Lz', vars: ['V', 'Lx', 'Ly', 'Lz'], f: v => v.V - v.Lx * v.Ly * v.Lz },
        { name: 'Number of modes below f', tex: 'N \\approx \\dfrac{4\\pi V}{3}\\left(\\dfrac{f}{c}\\right)^3', txt: 'N = 4*pi*V/3*(f/c)^3', vars: ['N', 'V', 'f'], f: v => v.N - 4 * PI * v.V / 3 * (v.f / v.c) ** 3, note: 'Leading term only; it underestimates at low frequency.' },
        { name: 'Schroeder frequency', tex: 'f_S \\approx 2000\\sqrt{\\dfrac{T}{V}}', txt: 'fS = 2000*sqrt(T/V)', vars: ['fS', 'T', 'V'], f: v => v.fS - 2000 * sq(v.T / v.V), note: 'Above f_S the modes overlap and the field is diffuse.' },
      ],
      widgets: ['modes'],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 6', 'Lecture Notes/Lecture 6 - Room Modes and the Diffuse Sound Field.md'], ['Lecture 7', 'Lecture Notes/Lecture 7 - Sound Absorption and Room Acoustic Design.md'], ['Week 6 worked', 'Exercises/Work/Week 6 - Room Modes and the Diffuse Sound Field.md'], ['Week 7 worked', 'Exercises/Work/Week 7 - Sound Absorbers.md']],
      id: 'reverb', title: 'Reverberation and the diffuse field',
      blurb: 'Absorption area, reverberation time, and the level in a room.',
      vars: {
        Lx: ['L_x', 'm', 'length'], Ly: ['L_y', 'm', 'width'], Lz: ['L_z', 'm', 'height'],
        V: ['V', 'm³', 'volume'], S: ['S', 'm²', 'total surface'], al: ['\\bar\\alpha', '', 'mean absorption coefficient', 'unit'],
        A: ['A', 'm²', 'absorption area'], T: ['T', 's', 'reverberation time (Sabine)'], TE: ['T_E', 's', 'reverberation time (Eyring)'],
        LW: ['L_W', 'dB', 'sound power level', 'db'], Lp: ['L_p', 'dB', 'level at r', 'db'], Lr: ['L_{\\rm rev}', 'dB', 'reverberant level', 'db'],
        Q: ['Q', '', 'directivity factor'], r: ['r', 'm', 'distance'], rc: ['r_c', 'm', 'reverberation distance'],
        mfp: ['\\bar\\ell', 'm', 'mean free path'],
        Ss: ['S_s', 'm²', 'sample area'], T1: ['T_1', 's', 'empty room'], T2: ['T_2', 's', 'with sample'], als: ['\\alpha_s', '', 'sample absorption coefficient'],
      },
      formulas: [
        { name: 'Volume', tex: 'V = L_x L_y L_z', txt: 'V = Lx*Ly*Lz', vars: ['V', 'Lx', 'Ly', 'Lz'], f: v => v.V - v.Lx * v.Ly * v.Lz },
        { name: 'Surface', tex: 'S = 2(L_xL_y + L_xL_z + L_yL_z)', txt: 'S = 2*(Lx*Ly + Lx*Lz + Ly*Lz)', vars: ['S', 'Lx', 'Ly', 'Lz'], f: v => v.S - 2 * (v.Lx * v.Ly + v.Lx * v.Lz + v.Ly * v.Lz) },
        { name: 'Absorption area', tex: 'A = S\\,\\bar\\alpha = \\textstyle\\sum S_i\\alpha_i', txt: 'A = S*al', vars: ['A', 'S', 'al'], f: v => v.A - v.S * v.al, note: 'Mixed surfaces: type the sum straight into A, e.g. 40*0.1 + 118*0.3.' },
        { name: 'Sabine', tex: 'T = \\dfrac{55.3\\,V}{c\\,A} \\approx \\dfrac{0.161\\,V}{A}', txt: 'T = 55.3*V/(c*A)', vars: ['T', 'V', 'A'], f: v => v.T - 55.3 * v.V / (v.c * v.A), note: 'Fine when ᾱ is below about 0.3.' },
        { name: 'Eyring', tex: 'T_E = \\dfrac{55.3\\,V}{-c\\,S\\ln(1-\\bar\\alpha)}', txt: 'TE = 55.3*V/(-c*S*ln(1 - al))', vars: ['TE', 'V', 'S', 'al'], f: v => v.TE - 55.3 * v.V / (-v.c * v.S * Math.log(1 - v.al)), note: 'Use for a well-damped room (large ᾱ). Always shorter than Sabine.' },
        { name: 'Level at a distance in a room', tex: 'L_p = L_W + 10\\log_{10}\\left(\\dfrac{Q}{4\\pi r^2} + \\dfrac{4}{A}\\right)', txt: 'Lp = LW + 10*log10(Q/(4*pi*r^2) + 4/A)', vars: ['Lp', 'LW', 'Q', 'r', 'A'], f: v => v.Lp - (v.LW + 10 * L10(v.Q / (4 * PI * v.r * v.r) + 4 / v.A)) },
        { name: 'Reverberant field only', tex: 'L_{\\rm rev} = L_W + 10\\log_{10}\\dfrac{4}{A}', txt: 'Lr = LW + 10*log10(4/A)', vars: ['Lr', 'LW', 'A'], f: v => v.Lr - (v.LW + 10 * L10(4 / v.A)), note: 'Also the way to get L_W from a reverberation-room measurement.' },
        { name: 'Reverberation distance', tex: 'r_c = \\sqrt{\\dfrac{Q\\,A}{16\\pi}}', txt: 'rc = sqrt(Q*A/(16*pi))', vars: ['rc', 'Q', 'A'], f: v => v.rc - sq(v.Q * v.A / (16 * PI)), note: 'Direct and reverberant fields are equal here.' },
        { name: 'Mean free path', tex: '\\bar\\ell = \\dfrac{4V}{S}', txt: 'mfp = 4*V/S', vars: ['mfp', 'V', 'S'], f: v => v.mfp - 4 * v.V / v.S },
        { name: 'Absorption of a sample (ISO 354)', tex: '\\alpha_s = \\dfrac{55.3\\,V}{c\\,S_s}\\left(\\dfrac{1}{T_2} - \\dfrac{1}{T_1}\\right)', txt: 'als = 55.3*V/(c*Ss)*(1/T2 - 1/T1)', vars: ['als', 'V', 'Ss', 'T2', 'T1'], f: v => v.als - 55.3 * v.V / (v.c * v.Ss) * (1 / v.T2 - 1 / v.T1) },
      ],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 7', 'Lecture Notes/Lecture 7 - Sound Absorption and Room Acoustic Design.md'], ['Week 7 worked', 'Exercises/Work/Week 7 - Sound Absorbers.md']],
      id: 'absorbers', title: 'Absorbers',
      blurb: 'Panel, Helmholtz, perforated and porous absorbers.',
      vars: {
        m: ['m', 'kg/m²', 'panel mass per area'], Lc: ['L', 'm', 'air gap behind'],
        fp: ['f_r', 'Hz', 'panel resonance'], fr: ['f_r', 'Hz', 'panel resonance (rule of thumb)'],
        Dn: ['d', 'm', 'neck diameter'], sN: ['s', 'm²', 'neck area'], lneck: ['l', 'm', 'neck length'],
        leff: ['l_{\\rm eff}', 'm', 'effective neck length'], Vc: ['V', 'm³', 'cavity volume'], fH: ['f_0', 'Hz', 'Helmholtz resonance'],
        dh: ['d_h', 'm', 'hole diameter'], ah: ['a', 'm', 'hole spacing'], P: ['P', '', 'perforation ratio', 'unit'],
        t: ['t', 'm', 'plate thickness'], fperf: ['f_0', 'Hz', 'perforated panel resonance'],
        Dp: ['D', 'm', 'porous layer thickness'], fq: ['f_{\\lambda/4}', 'Hz', 'quarter-wave frequency'],
      },
      formulas: [
        { name: 'Panel (membrane) absorber', tex: 'f_r = \\dfrac{1}{2\\pi}\\sqrt{\\dfrac{\\rho c^2}{m\\,L}}', txt: 'fp = 1/(2*pi)*sqrt(rho*c^2/(m*Lc))', vars: ['fp', 'm', 'Lc'], f: v => v.fp - sq(v.rho * v.c * v.c / (v.m * v.Lc)) / (2 * PI) },
        { name: 'Panel absorber, rule of thumb', tex: 'f_r \\approx \\dfrac{60}{\\sqrt{m\\,L}}', txt: 'fr = 60/sqrt(m*Lc)', vars: ['fr', 'm', 'Lc'], f: v => v.fr - 60 / sq(v.m * v.Lc) },
        { name: 'Neck area', tex: 's = \\dfrac{\\pi d^2}{4}', txt: 'sN = pi*Dn^2/4', vars: ['sN', 'Dn'], f: v => v.sN - PI * v.Dn * v.Dn / 4 },
        { name: 'End correction', tex: 'l_{\\rm eff} = l + 0.8\\,d', txt: 'leff = lneck + 0.8*Dn', vars: ['leff', 'lneck', 'Dn'], f: v => v.leff - (v.lneck + 0.8 * v.Dn), note: 'Flanged at both ends. If the exam gives its own correction, type l_eff directly.' },
        { name: 'Helmholtz resonator', tex: 'f_0 = \\dfrac{c}{2\\pi}\\sqrt{\\dfrac{s}{V\\,l_{\\rm eff}}}', txt: 'fH = c/(2*pi)*sqrt(sN/(Vc*leff))', vars: ['fH', 'sN', 'Vc', 'leff'], f: v => v.fH - v.c / (2 * PI) * sq(v.sN / (v.Vc * v.leff)) },
        { name: 'Perforation ratio', tex: 'P = \\dfrac{\\pi d_h^2}{4a^2}', txt: 'P = pi*dh^2/(4*ah^2)', vars: ['P', 'dh', 'ah'], f: v => v.P - PI * v.dh * v.dh / (4 * v.ah * v.ah), note: 'Holes on a square grid with spacing a.' },
        { name: 'Perforated panel', tex: 'f_0 = \\dfrac{c}{2\\pi}\\sqrt{\\dfrac{P}{L\\,(t + 0.8\\,d_h)}}', txt: 'fperf = c/(2*pi)*sqrt(P/(Lc*(t + 0.8*dh)))', vars: ['fperf', 'P', 'Lc', 't', 'dh'], f: v => v.fperf - v.c / (2 * PI) * sq(v.P / (v.Lc * (v.t + 0.8 * v.dh))) },
        { name: 'Porous layer on a hard wall', tex: 'f_{\\lambda/4} = \\dfrac{c}{4D}', txt: 'fq = c/(4*Dp)', vars: ['fq', 'Dp'], f: v => v.fq - v.c / (4 * v.Dp), note: 'Absorbs well from here up: the layer reaches the velocity maximum λ/4 from the wall.' },
      ],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 3', 'Lecture Notes/Lecture 3 - Decibels Frequency Analysis and Measurements.md'], ['Week 3 worked', 'Exercises/Work/Week 3 - Decibels Frequency Analysis and Measurements.md']],
      id: 'bands', title: 'Frequency bands and weighting',
      blurb: 'Octave and third-octave bands, A- and C-weighting.',
      vars: {
        fc: ['f_c', 'Hz', 'centre frequency'], b: ['b', '', '1 = octave, 3 = third octave', 'int'],
        fl: ['f_l', 'Hz', 'lower edge'], fu: ['f_u', 'Hz', 'upper edge'], B: ['B', 'Hz', 'bandwidth'],
        Aw: ['A(f_c)', 'dB', 'A-weighting', 'db'], Cw: ['C(f_c)', 'dB', 'C-weighting', 'db'],
        Lb: ['L', 'dB', 'band level', 'db'], La: ['L_A', 'dB', 'A-weighted band level', 'db'],
      },
      formulas: [
        { name: 'Lower band edge', tex: 'f_l = f_c\\,2^{-1/(2b)}', txt: 'fl = fc*2^(-1/(2*b))', vars: ['fl', 'fc', 'b'], f: v => v.fl - v.fc * 2 ** (-1 / (2 * v.b)) },
        { name: 'Upper band edge', tex: 'f_u = f_c\\,2^{1/(2b)}', txt: 'fu = fc*2^(1/(2*b))', vars: ['fu', 'fc', 'b'], f: v => v.fu - v.fc * 2 ** (1 / (2 * v.b)) },
        { name: 'Bandwidth', tex: 'B = f_u - f_l', txt: 'B = fu - fl', vars: ['B', 'fu', 'fl'], f: v => v.B - (v.fu - v.fl), note: 'Octave ≈ 0.71 f_c, third octave ≈ 0.23 f_c.' },
        { name: 'A-weighting', tex: 'A(f) \\;\\text{(IEC 61672)}', txt: 'Aw = A(fc)', matlab: 'Aw = 20*log10(12194^2*fc.^4./((fc.^2 + 20.6^2).*sqrt((fc.^2 + 107.7^2).*(fc.^2 + 737.9^2)).*(fc.^2 + 12194^2))) + 2.00', vars: ['Aw', 'fc'], f: v => v.Aw - aWeight(v.fc), note: 'The exam’s table rounds to 0.1 dB; the band table below uses the table values.' },
        { name: 'C-weighting', tex: 'C(f) \\;\\text{(IEC 61672)}', txt: 'Cw = C(fc)', matlab: 'Cw = 20*log10(12194^2*fc.^2./((fc.^2 + 20.6^2).*(fc.^2 + 12194^2))) + 0.06', vars: ['Cw', 'fc'], f: v => v.Cw - cWeight(v.fc) },
        { name: 'A-weighted band level', tex: 'L_A = L + A(f_c)', txt: 'La = Lb + Aw', vars: ['La', 'Lb', 'Aw'], f: v => v.La - (v.Lb + v.Aw) },
      ],
      widgets: ['bandtable'],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 9', 'Lecture Notes/Lecture 9 - Hearing - Frequency Selectivity and Masking.md'], ['Lecture 10', 'Lecture Notes/Lecture 10 - Physiological Acoustics.md'], ['Week 9 worked', 'Exercises/Work/Week 9 - Psychological Acoustics.md'], ['Week 10 worked', 'Exercises/Work/Week 10 - Physiological Acoustics.md']],
      id: 'hearing', title: 'Hearing',
      blurb: 'Auditory filters, masking, loudness, the cochlear map and evoked responses.',
      vars: {
        f: ['f', 'Hz', 'frequency'], ERB: ['\\mathrm{ERB}', 'Hz', 'equivalent rectangular bandwidth'], CB: ['\\mathrm{CB}', 'Hz', 'critical band (Zwicker)'],
        N0: ['N_0', 'dB/Hz', 'noise spectrum level', 'db'], kdet: ['k', '', 'detection ratio (linear)'], Ls: ['L_s', 'dB', 'masked threshold', 'db'],
        f1: ['f_1', 'Hz', 'lower tone'], f2: ['f_2', 'Hz', 'upper tone'], fct: ['f_{\\rm CT}', 'Hz', 'combination tone'],
        LN: ['L_N', 'phon', 'loudness level', 'db'], Ns: ['N', 'sone', 'loudness'],
        x: ['x', 'mm', 'distance from the base'], Fg: ['F', 'Hz', 'characteristic frequency'],
        cBM: ['c_{\\rm BM}', 'm/s', 'travelling-wave speed'], t: ['t', 'ms', 'OAE round-trip latency'],
        EP: ['EP', 'µV', 'evoked response amplitude'], Nn: ['N_1', 'µV', 'noise in one sweep'], SNR1: ['\\mathrm{SNR}_1', 'dB', 'one sweep', 'db'],
        nav: ['n', '', 'number of sweeps averaged'], SNRn: ['\\mathrm{SNR}_n', 'dB', 'after n sweeps', 'db'],
      },
      formulas: [
        { name: 'Equivalent rectangular bandwidth', tex: '\\mathrm{ERB} = 24.7\\left(4.37\\,\\dfrac{f}{1000} + 1\\right)', txt: 'ERB = 24.7*(4.37*f/1000 + 1)', vars: ['ERB', 'f'], f: v => v.ERB - 24.7 * (4.37 * v.f / 1000 + 1), note: 'Two tones closer than one ERB share a filter and beat.' },
        { name: 'Critical band (Zwicker)', tex: '\\mathrm{CB} = 25 + 75\\left(1 + 1.4\\left(\\dfrac{f}{1000}\\right)^2\\right)^{0.69}', txt: 'CB = 25 + 75*(1 + 1.4*(f/1000)^2)^0.69', vars: ['CB', 'f'], f: v => v.CB - (25 + 75 * (1 + 1.4 * (v.f / 1000) ** 2) ** 0.69) },
        { name: 'Masked threshold of a tone in noise', tex: 'L_s = N_0 + 10\\log_{10}k + 10\\log_{10}\\mathrm{ERB}', txt: 'Ls = N0 + 10*log10(kdet) + 10*log10(ERB)', vars: ['Ls', 'N0', 'kdet', 'ERB'], f: v => v.Ls - (v.N0 + 10 * L10(v.kdet) + 10 * L10(v.ERB)), note: 'If the noise band is narrower than the ERB, type its bandwidth into ERB instead.' },
        { name: 'Strongest combination tone', tex: 'f_{\\rm CT} = 2f_1 - f_2', txt: 'fct = 2*f1 - f2', vars: ['fct', 'f1', 'f2'], f: v => v.fct - (2 * v.f1 - v.f2), note: 'f₁ < f₂, so it lies below the lower tone.' },
        { name: 'Loudness in sone', tex: 'N = 2^{(L_N - 40)/10}', txt: 'Ns = 2^((LN - 40)/10)', vars: ['Ns', 'LN'], f: v => v.Ns - 2 ** ((v.LN - 40) / 10), note: '+10 phon doubles the loudness.' },
        { name: 'Greenwood map', tex: 'F = 20682\\cdot 10^{-0.061765\\,x} - 140.6', txt: 'Fg = 20682*10^(-0.061765*x) - 140.6', vars: ['Fg', 'x'], f: v => v.Fg - (20682 * 10 ** (-0.061765 * v.x) - 140.6), note: 'x in mm from the base (high frequencies at the base). Human cochlea ≈ 34 mm.' },
        { name: 'OAE place from latency', tex: 'x = c_{\\rm BM}\\,\\dfrac{t}{2}', txt: 'x = cBM*t/2', vars: ['x', 'cBM', 't'], f: v => v.x - v.cBM * v.t / 2, note: 'm/s × ms gives mm. Half the round trip.' },
        { name: 'SNR of one sweep', tex: '\\mathrm{SNR}_1 = 20\\log_{10}\\dfrac{EP}{N_1}', txt: 'SNR1 = 20*log10(EP/Nn)', vars: ['SNR1', 'EP', 'Nn'], f: v => v.SNR1 - 20 * L10(v.EP / v.Nn) },
        { name: 'Averaging gain', tex: '\\mathrm{SNR}_n = \\mathrm{SNR}_1 + 10\\log_{10} n', txt: 'SNRn = SNR1 + 10*log10(nav)', vars: ['SNRn', 'SNR1', 'nav'], f: v => v.SNRn - (v.SNR1 + 10 * L10(v.nav)), note: 'Noise amplitude falls as √n: +3 dB per doubling.' },
      ],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 11', 'Lecture Notes/Lecture 11 - Structure-borne Sound and Vibration Isolation.md'], ['Week 11 worked', 'Exercises/Work/Week 11 - Structure-borne Sound and Vibration Isolation.md']],
      id: 'vibration', title: 'Vibration isolation',
      blurb: 'A machine on springs: resonance, transmissibility and isolation.',
      vars: {
        m: ['m', 'kg', 'mass'], s: ['s', 'N/m', 'spring stiffness'], dl: ['\\xi_0', 'm', 'static deflection'],
        f0: ['f_0', 'Hz', 'mounted resonance'], fv: ['f', 'Hz', 'forcing frequency'], r: ['r', '', 'frequency ratio f/f₀'],
        zeta: ['\\zeta', '', 'damping ratio'], T: ['T', '', 'force transmissibility'], TdB: ['20\\log_{10}T', 'dB', 'transmissibility in dB', 'db'],
        F: ['F', 'N', 'force amplitude'], xi: ['\\xi', 'm', 'displacement amplitude'],
      },
      formulas: [
        { name: 'Stiffness from static deflection', tex: 's = \\dfrac{m g}{\\xi_0}', txt: 's = m*g/dl', vars: ['s', 'm', 'dl'], f: v => v.s - v.m * v.g / v.dl },
        { name: 'Resonance', tex: 'f_0 = \\dfrac{1}{2\\pi}\\sqrt{\\dfrac{s}{m}}', txt: 'f0 = 1/(2*pi)*sqrt(s/m)', vars: ['f0', 's', 'm'], f: v => v.f0 - sq(v.s / v.m) / (2 * PI), note: 'From the deflection alone: f₀ = √(g/ξ₀)/2π ≈ 0.5/√ξ₀.' },
        { name: 'Frequency ratio', tex: 'r = \\dfrac{f}{f_0}', txt: 'r = fv/f0', vars: ['r', 'fv', 'f0'], f: v => v.r - v.fv / v.f0, note: 'Isolation only above r = √2.' },
        { name: 'Transmissibility', tex: 'T = \\sqrt{\\dfrac{1 + (2\\zeta r)^2}{(1 - r^2)^2 + (2\\zeta r)^2}}', txt: 'T = sqrt((1 + (2*zeta*r)^2)/((1 - r^2)^2 + (2*zeta*r)^2))', vars: ['T', 'zeta', 'r'], f: v => v.T - sq((1 + (2 * v.zeta * v.r) ** 2) / ((1 - v.r * v.r) ** 2 + (2 * v.zeta * v.r) ** 2)), note: 'No damping: type ζ = 0, then T = 1/|1 − r²|.' },
        { name: 'Transmissibility in dB', tex: '20\\log_{10}T', txt: 'TdB = 20*log10(T)', vars: ['TdB', 'T'], f: v => v.TdB - 20 * L10(v.T), note: 'Negative means isolation.' },
        { name: 'Forced displacement (no damping)', tex: '\\xi = \\dfrac{F}{s\\,|1 - r^2|}', txt: 'xi = F/(s*abs(1 - r^2))', vars: ['xi', 'F', 's', 'r'], f: v => v.xi - v.F / (v.s * Math.abs(1 - v.r * v.r)) },
      ],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 12', 'Lecture Notes/Lecture 12 - Sound Insulation.md'], ['Week 12 worked', 'Exercises/Work/Week 12 - Sound Insulation.md']],
      id: 'insulation', title: 'Sound insulation',
      blurb: 'Mass law, coincidence, double walls and the level in the receiving room.',
      vars: {
        f: ['f', 'Hz', 'frequency'], m: ['m', 'kg/m²', 'mass per area'],
        R0: ['R_0', 'dB', 'mass law, normal incidence', 'db'], Rf: ['R_{\\rm field}', 'dB', 'mass law, field incidence', 'db'],
        rhoM: ['\\rho_M', 'kg/m³', 'density of the panel'], h: ['h', 'm', 'thickness'],
        E: ['E', 'Pa', 'Young’s modulus'], nu: ['\\nu', '', 'Poisson’s ratio', 'unit'], Bp: ['B', 'N·m', 'bending stiffness'],
        fc: ['f_c', 'Hz', 'critical frequency'], eta: ['\\eta', '', 'loss factor'], Rc: ['R', 'dB', 'above f_c', 'db'],
        m1: ['m_1', 'kg/m²', 'leaf 1'], m2: ['m_2', 'kg/m²', 'leaf 2'], d: ['d', 'm', 'cavity depth'], f0: ['f_0', 'Hz', 'mass–air–mass resonance'],
        R: ['R', 'dB', 'the wall’s reduction index', 'db'], L1: ['L_1', 'dB', 'source room', 'db'], L2: ['L_2', 'dB', 'receiving room', 'db'],
        S: ['S', 'm²', 'wall area'], A2: ['A_2', 'm²', 'absorption, receiving room'], V2: ['V_2', 'm³', 'volume, receiving room'], T2: ['T_2', 's', 'reverberation, receiving room'],
      },
      formulas: [
        { name: 'Mass law, normal incidence', tex: 'R_0 = 20\\log_{10}\\dfrac{\\omega m}{2\\rho c}', txt: 'R0 = 20*log10(2*pi*f*m/(2*rho*c))', vars: ['R0', 'f', 'm'], f: v => v.R0 - 20 * L10(2 * PI * v.f * v.m / (2 * v.rho * v.c)), note: '+6 dB per doubling of mass or frequency.' },
        { name: 'Mass law, field incidence', tex: 'R_{\\rm field} \\approx R_0 - 5\\ \\text{dB}', txt: 'Rf = R0 - 5', vars: ['Rf', 'R0'], f: v => v.Rf - (v.R0 - 5) },
        { name: 'Mass per area', tex: 'm = \\rho_M h', txt: 'm = rhoM*h', vars: ['m', 'rhoM', 'h'], f: v => v.m - v.rhoM * v.h },
        { name: 'Bending stiffness', tex: 'B = \\dfrac{E h^3}{12(1-\\nu^2)}', txt: 'Bp = E*h^3/(12*(1 - nu^2))', vars: ['Bp', 'E', 'h', 'nu'], f: v => v.Bp - v.E * v.h ** 3 / (12 * (1 - v.nu * v.nu)) },
        { name: 'Critical frequency', tex: 'f_c = \\dfrac{c^2}{2\\pi}\\sqrt{\\dfrac{m}{B}}', txt: 'fc = c^2/(2*pi)*sqrt(m/Bp)', vars: ['fc', 'm', 'Bp'], f: v => v.fc - v.c * v.c / (2 * PI) * sq(v.m / v.Bp), note: 'f_c ∝ 1/h: a thicker panel dips lower.' },
        { name: 'Above the critical frequency', tex: 'R = R_0 + 10\\log_{10}\\dfrac{2\\eta f}{\\pi f_c}', txt: 'Rc = R0 + 10*log10(2*eta*f/(pi*fc))', vars: ['Rc', 'R0', 'eta', 'f', 'fc'], f: v => v.Rc - (v.R0 + 10 * L10(2 * v.eta * v.f / (PI * v.fc))) },
        { name: 'Double wall resonance', tex: 'f_0 = \\dfrac{c}{2\\pi}\\sqrt{\\dfrac{\\rho}{d}\\left(\\dfrac{1}{m_1} + \\dfrac{1}{m_2}\\right)}', txt: 'f0 = c/(2*pi)*sqrt(rho/d*(1/m1 + 1/m2))', vars: ['f0', 'd', 'm1', 'm2'], f: v => v.f0 - v.c / (2 * PI) * sq(v.rho / v.d * (1 / v.m1 + 1 / v.m2)), note: 'Below f₀ the wall acts as one mass m₁ + m₂; above it R climbs 18 dB/octave.' },
        { name: 'Level in the receiving room', tex: 'L_2 = L_1 - R + 10\\log_{10}\\dfrac{S}{A_2}', txt: 'L2 = L1 - R + 10*log10(S/A2)', vars: ['L2', 'L1', 'R', 'S', 'A2'], f: v => v.L2 - (v.L1 - v.R + 10 * L10(v.S / v.A2)), note: 'R is whatever reduction index you have: measured, from the mass law above, or composite.' },
        { name: 'Absorption of the receiving room', tex: 'A_2 = \\dfrac{55.3\\,V_2}{c\\,T_2}', txt: 'A2 = 55.3*V2/(c*T2)', vars: ['A2', 'V2', 'T2'], f: v => v.A2 - 55.3 * v.V2 / (v.c * v.T2) },
      ],
      widgets: ['composite'],
    },
    // ------------------------------------------------------------------
    {
      notes: [['Lecture 8', 'Lecture Notes/Lecture 8 - Loudspeakers.md'], ['Week 8 worked', 'Exercises/Work/Week 8 - Loudspeakers.md']],
      id: 'speaker', title: 'Loudspeakers',
      blurb: 'The driver as a mass on a spring, the closed box, and the radiated level.',
      vars: {
        a: ['a', 'm', 'piston radius'], Sd: ['S', 'm²', 'piston area'], K: ['K', 'N/m', 'suspension stiffness'], M: ['M', 'kg', 'moving mass'],
        Rt: ['R_t', 'N·s/m', 'total mechanical resistance'], fs: ['f_s', 'Hz', 'resonance in free air'], Qt: ['Q_t', '', 'total Q'],
        Vb: ['V_b', 'm³', 'box volume'], Kb: ['K_b', 'N/m', 'stiffness of the box air'], fcb: ['f_c', 'Hz', 'resonance in the box'],
        Bl: ['Bl', 'T·m', 'force factor'], Re: ['R_e', 'Ω', 'voice coil resistance'], eg: ['e_{\\rm rms}', 'V', 'drive voltage'],
        Om: ['\\Omega', 'sr', 'solid angle (4π free, 2π baffle)'], r: ['r', 'm', 'distance'], p: ['p_{\\rm rms}', 'Pa', 'pressure, above f_s'],
        f: ['f', 'Hz', 'frequency'], ka: ['ka', '', 'size vs wavelength'], th: ['\\theta_1', '°', 'first null off axis', 'deg90'],
      },
      formulas: [
        { name: 'Piston area', tex: 'S = \\pi a^2', txt: 'Sd = pi*a^2', vars: ['Sd', 'a'], f: v => v.Sd - PI * v.a * v.a },
        { name: 'Resonance in free air', tex: 'f_s = \\dfrac{1}{2\\pi}\\sqrt{\\dfrac{K}{M}}', txt: 'fs = 1/(2*pi)*sqrt(K/M)', vars: ['fs', 'K', 'M'], f: v => v.fs - sq(v.K / v.M) / (2 * PI) },
        { name: 'Total Q', tex: 'Q_t = \\dfrac{\\sqrt{K M}}{R_t}', txt: 'Qt = sqrt(K*M)/Rt', vars: ['Qt', 'K', 'M', 'Rt'], f: v => v.Qt - sq(v.K * v.M) / v.Rt, note: 'R_t includes the electrical damping (Bl)²/R_e.' },
        { name: 'Stiffness of the box air', tex: 'K_b = \\dfrac{\\rho c^2 S^2}{V_b}', txt: 'Kb = rho*c^2*Sd^2/Vb', vars: ['Kb', 'Sd', 'Vb'], f: v => v.Kb - v.rho * v.c * v.c * v.Sd * v.Sd / v.Vb },
        { name: 'Resonance in a closed box', tex: 'f_c = \\dfrac{1}{2\\pi}\\sqrt{\\dfrac{K + K_b}{M}}', txt: 'fcb = 1/(2*pi)*sqrt((K + Kb)/M)', vars: ['fcb', 'K', 'Kb', 'M'], f: v => v.fcb - sq((v.K + v.Kb) / v.M) / (2 * PI) },
        { name: 'Pressure in the mass-controlled range', tex: 'p_{\\rm rms} = \\dfrac{\\rho\\,S\\,Bl\\,e_{\\rm rms}}{\\Omega\\,r\\,R_e M}', txt: 'p = rho*Sd*Bl*eg/(Om*r*Re*M)', vars: ['p', 'Sd', 'Bl', 'eg', 'Om', 'r', 'Re', 'M'], f: v => v.p - v.rho * v.Sd * v.Bl * v.eg / (v.Om * v.r * v.Re * v.M), note: 'Flat response above f_s while ka < 1. Type 4*pi or 2*pi for Ω.' },
        { name: 'Size against wavelength', tex: 'ka = \\dfrac{2\\pi f a}{c}', txt: 'ka = 2*pi*f*a/c', vars: ['ka', 'f', 'a'], f: v => v.ka - 2 * PI * v.f * v.a / v.c, note: 'Omnidirectional below ka ≈ 1, beaming above.' },
        { name: 'First null of a baffled piston', tex: '\\sin\\theta_1 = \\dfrac{3.83}{ka}', txt: 'th = asin(3.83/ka)', matlab: 'th = asind(3.83./ka)', vars: ['th', 'ka'], f: v => Math.sin(v.th * PI / 180) - 3.83 / v.ka, note: 'Only exists when ka > 3.83.' },
      ],
    },
  ];

  const COURSE_DIR = '/home/mads/DTU/Obsidian/Courses/34840 Fundamentals of Acoustics and Noise Control/';
  const EXAM_NOTES = [['Cheat sheet', 'Exam Prep/Cheat Sheet - 34840.md'], ['Old exams worked', 'Exam Prep/Old Exams 2022-2024 - Worked.md'], ['Exam-day checklist', 'Exam Prep/Exam Day Checklist - 34840.md']];
  const api = { TOPICS, CONSTANTS, aWeight, cWeight, COURSE_DIR, EXAM_NOTES };
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.FORMULAS = api;
})(typeof self !== 'undefined' ? self : this);
