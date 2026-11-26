// 34840 Exam App — Verified Physics Engine (T01..T15 + Quick Tools)
// Matches every formula and pre-filled check in ../toolkit/T01..T15.m and run_all_checks.m (116/116 checks)

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.AcousticsPhysics = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  // --- Complex number helpers ---
  function cplx(re, im) {
    if (typeof re === 'object' && re !== null && 're' in re) return { re: Number(re.re) || 0, im: Number(re.im) || 0 };
    return { re: Number(re) || 0, im: Number(im) || 0 };
  }
  function cAdd(a, b) { a = cplx(a); b = cplx(b); return { re: a.re + b.re, im: a.im + b.im }; }
  function cSub(a, b) { a = cplx(a); b = cplx(b); return { re: a.re - b.re, im: a.im - b.im }; }
  function cMul(a, b) {
    a = cplx(a); b = cplx(b);
    return { re: a.re * b.re - a.im * b.im, im: a.re * b.im + a.im * b.re };
  }
  function cDiv(a, b) {
    a = cplx(a); b = cplx(b);
    const den = b.re * b.re + b.im * b.im;
    return { re: (a.re * b.re + a.im * b.im) / den, im: (a.im * b.re - a.re * b.im) / den };
  }
  function cAbs(a) { a = cplx(a); return Math.hypot(a.re, a.im); }
  function cConj(a) { a = cplx(a); return { re: a.re, im: -a.im }; }
  function cExpJ(theta) { return { re: Math.cos(theta), im: Math.sin(theta) }; }
  function cArgDeg(a) { a = cplx(a); return Math.atan2(a.im, a.re) * 180 / Math.PI; }

  function parseComplexToken(str) {
    if (typeof str === 'number') return { re: str, im: 0 };
    if (typeof str === 'object' && str !== null && 're' in str) return cplx(str.re, str.im);
    let s = String(str).trim().replace(/\s+/g, '');
    if (!s) return { re: 0, im: 0 };
    // Support polar form: r<deg or r∠deg
    if (s.includes('<') || s.includes('∠')) {
      const parts = s.split(/[<∠]/);
      const r = parseFloat(parts[0]) || 0;
      const deg = parseFloat(parts[1]) || 0;
      const rad = deg * Math.PI / 180;
      return { re: r * Math.cos(rad), im: r * Math.sin(rad) };
    }
    if (!/[ijIJ]/.test(s)) {
      return { re: parseFloat(s) || 0, im: 0 };
    }
    // Normalize i/j at start or after +/- (e.g., "j0.05", "+j0.4", "-j", "0.4+0.4j", "0.4+j0.4")
    s = s.replace(/[iI]/g, 'j');
    // Match real and imag tokens
    // Convert "j0.05" -> "0.05j", "+j0.4" -> "+0.4j", "-j0.4" -> "-0.4j"
    s = s.replace(/([+-]|^)j([0-9.]+(?:e[+-]?[0-9]+)?)/gi, '$1$2j');
    s = s.replace(/([+-]|^)j$/gi, '$11j');
    // Split into signed terms (not splitting inside scientific notation e+ / e-)
    const terms = s.match(/[+-]?(?:[0-9.]+(?:e[+-]?[0-9]+)?)?j?/gi) || [];
    let re = 0, im = 0;
    for (const t of terms) {
      if (!t) continue;
      if (t.endsWith('j') || t.endsWith('J')) {
        const numStr = t.slice(0, -1);
        const v = (numStr === '' || numStr === '+') ? 1 : (numStr === '-' ? -1 : parseFloat(numStr));
        im += (isNaN(v) ? 0 : v);
      } else {
        const v = parseFloat(t);
        re += (isNaN(v) ? 0 : v);
      }
    }
    return { re, im };
  }

  function parseNumberList(val) {
    if (Array.isArray(val)) return val.map(Number);
    if (typeof val === 'number') return [val];
    return String(val)
      .trim()
      .split(/[\s,;]+/)
      .filter(Boolean)
      .map(s => {
        if (s.toLowerCase() === 'inf' || s.toLowerCase() === 'infinity') return Infinity;
        return Number(s);
      });
  }

  function parseComplexList(val) {
    if (Array.isArray(val)) return val.map(parseComplexToken);
    if (typeof val === 'number') return [{ re: val, im: 0 }];
    // Split by comma or semicolon, or whitespace when not joining a complex number's +/-
    const raw = String(val).trim().replace(/\s*([+-])\s*([0-9.jJiI])/g, '$1$2');
    return raw.split(/[\s,;]+/).filter(Boolean).map(parseComplexToken);
  }

  function fmtNum(x, digits = 4) {
    if (x === undefined || x === null) return '—';
    if (typeof x === 'object' && 're' in x) return fmtComplex(x, digits);
    if (Array.isArray(x)) return x.map(v => fmtNum(v, digits)).join(', ');
    if (x === -Infinity) return '-∞';
    if (x === Infinity) return '∞';
    if (Number.isNaN(x)) return 'NaN';
    const ax = Math.abs(x);
    if (ax === 0) return '0';
    if (ax >= 1e5 || (ax > 0 && ax < 1e-3)) {
      return x.toExponential(Math.max(1, digits - 1));
    }
    return Number(x.toPrecision(digits)).toString();
  }

  function fmtFixed(x, dec = 2) {
    if (x === -Infinity) return '-∞';
    if (x === Infinity) return '∞';
    if (Number.isNaN(x)) return 'NaN';
    return Number(x).toFixed(dec);
  }

  function fmtComplex(c, digits = 3) {
    c = cplx(c);
    if (Math.abs(c.im) < 1e-12) return fmtNum(c.re, digits);
    if (Math.abs(c.re) < 1e-12) return `${fmtNum(c.im, digits)}j`;
    const sign = c.im >= 0 ? '+' : '-';
    return `${fmtNum(c.re, digits)} ${sign} j${fmtNum(Math.abs(c.im), digits)}`;
  }

  // Bessel function of the first kind J_1(x)
  function besselJ1(x) {
    const ax = Math.abs(x);
    if (ax === 0) return 0;
    if (ax < 8.0) {
      const y = x * x;
      const ans1 = x * (72362614232.0 + y * (-7895059235.0 + y * (242396853.1
        + y * (-2972611.439 + y * (15704.48260 + y * (-30.16036606))))));
      const ans2 = 144725228442.0 + y * (2300535178.0 + y * (18583304.74
        + y * (99447.43394 + y * (376.9991397 + y * 1.0))));
      return ans1 / ans2;
    } else {
      const z = 8.0 / ax;
      const y = z * z;
      const xx = ax - 2.356194491;
      const ans1 = 1.0 + y * (0.183105e-2 + y * (-0.3516396496e-4
        + y * (0.2457520174e-5 + y * (-0.240337019e-6))));
      const ans2 = 0.04687499995 + y * (-0.2002690873e-3
        + y * (0.8449199096e-5 + y * (-0.88228987e-6 + y * 0.105787412e-6)));
      const ans = Math.sqrt(0.636619772 / ax) * (Math.cos(xx) * ans1 - z * Math.sin(xx) * ans2);
      return x < 0.0 ? -ans : ans;
    }
  }

  // Standard third-octave nominal table (course text Table 1.3.2)
  const FA_TABLE = [
    20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000,
    1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000
  ];
  const KA_TABLE = [
    -50.5, -44.7, -39.4, -34.6, -30.2, -26.2, -22.5, -19.1, -16.1, -13.4, -10.9, -8.6,
    -6.6, -4.8, -3.2, -1.9, -0.8, 0.0, 0.6, 1.0, 1.2, 1.3, 1.2, 1.0, 0.5, -0.1, -1.1, -2.5, -4.3, -6.6, -9.3
  ];
  const KC_TABLE = [
    -6.2, -4.4, -3.0, -2.0, -1.3, -0.8, -0.5, -0.3, -0.2, -0.1, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.1, -0.2, -0.3, -0.5, -0.8, -1.3, -2.0, -3.0, -4.4, -6.2, -8.5, -11.2
  ];
  const OCTAVE_CENTRES = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000];

  function interpLogTable(f, fTable, kTable) {
    const lf = Math.log10(f);
    const lTab = fTable.map(Math.log10);
    if (lf <= lTab[0]) return kTable[0];
    if (lf >= lTab[lTab.length - 1]) return kTable[kTable.length - 1];
    for (let i = 0; i < lTab.length - 1; i++) {
      if (lf >= lTab[i] && lf <= lTab[i + 1]) {
        const t = (lf - lTab[i]) / (lTab[i + 1] - lTab[i]);
        return kTable[i] + t * (kTable[i + 1] - kTable[i]);
      }
    }
    return 0;
  }

  function interpAWeight(f) { return interpLogTable(f, FA_TABLE, KA_TABLE); }
  function interpCWeight(f) { return interpLogTable(f, FA_TABLE, KC_TABLE); }

  function analyticAWeight(f) {
    const w = 2 * Math.PI * f;
    // H_A(jw) = 7.4e9 * (jw)^4 / ((jw+129.4)^2 (jw+676.7) (jw+4636) (jw+76655)^2)
    const num = 7.4e9 * Math.pow(w, 4);
    const den = (w * w + 129.4 * 129.4) * Math.hypot(w, 676.7) * Math.hypot(w, 4636) * (w * w + 76655 * 76655);
    return 20 * Math.log10(num / den);
  }

  // Default constants
  const DEFAULT_CONSTANTS = {
    rho: 1.2,
    c: 343,
    p_ref: 20e-6,
    I_ref: 1e-12,
    W_ref: 1e-12,
    g: 9.81
  };

  function getConsts(inp = {}) {
    const rho = inp.rho !== undefined ? Number(inp.rho) : DEFAULT_CONSTANTS.rho;
    const c = inp.c !== undefined ? Number(inp.c) : DEFAULT_CONSTANTS.c;
    const p_ref = inp.p_ref !== undefined ? Number(inp.p_ref) : DEFAULT_CONSTANTS.p_ref;
    const I_ref = inp.I_ref !== undefined ? Number(inp.I_ref) : DEFAULT_CONSTANTS.I_ref;
    const W_ref = inp.W_ref !== undefined ? Number(inp.W_ref) : DEFAULT_CONSTANTS.W_ref;
    const g = inp.g !== undefined ? Number(inp.g) : DEFAULT_CONSTANTS.g;
    return { rho, c, rho_c: rho * c, rho_c2: rho * c * c, p_ref, I_ref, W_ref, g };
  }

  // =========================================================================
  // T01: Plane wave reflection & two-media transmission
  // =========================================================================
  function solveT01(raw = {}) {
    const C = getConsts(raw);
    const f = parseNumberList(raw.f !== undefined ? raw.f : [400, 630]);
    const p_i = parseComplexList(raw.p_i !== undefined ? raw.p_i : ['0.9', '0.4+0.4j']);
    const inputIsRms = Boolean(raw.inputIsRms);
    const p_i_peak = p_i.map(v => inputIsRms ? cMul(v, Math.SQRT2) : v);

    const mode = raw.mode || 'alpha'; // 'alpha' | 'Z' | 'R'
    const alpha = parseNumberList(raw.alpha !== undefined ? raw.alpha : [0.9999, 0.19]);
    const R_sign = raw.R_sign !== undefined ? Number(raw.R_sign) : 1;
    const Z_list = parseComplexList(raw.Z !== undefined ? raw.Z : ['500+1000j']);
    const R_given = parseComplexList(raw.R_direct !== undefined ? raw.R_direct : ['0.01', '0.9']);
    const d = raw.d !== undefined ? Number(raw.d) : 0.6;
    const z1 = raw.z1 !== undefined ? Number(raw.z1) : C.rho_c;
    const z2 = raw.z2 !== undefined ? Number(raw.z2) : 1000 * 1480;
    const rho_planet = raw.rho_planet !== undefined ? Number(raw.rho_planet) : 100;
    const c_planet = raw.c_planet !== undefined ? Number(raw.c_planet) : 500;

    const N = Math.max(f.length, p_i_peak.length);
    const R_c = [];
    const R = [];
    const alpha_out = [];
    for (let i = 0; i < N; i++) {
      if (mode === 'Z') {
        const z = Z_list[i % Z_list.length];
        const rc = cDiv(cSub(z, C.rho_c), cAdd(z, C.rho_c));
        R_c.push(rc);
        R.push(rc.re);
        alpha_out.push(1 - Math.pow(cAbs(rc), 2));
      } else if (mode === 'R') {
        const rc = R_given[i % R_given.length];
        R_c.push(rc);
        R.push(rc.re);
        alpha_out.push(1 - Math.pow(cAbs(rc), 2));
      } else {
        const a = alpha[i % alpha.length];
        const rVal = R_sign * Math.sqrt(Math.max(0, 1 - a));
        R_c.push({ re: rVal, im: 0 });
        R.push(rVal);
        alpha_out.push(a);
      }
    }

    const k = f.map(fi => 2 * Math.PI * fi / C.c);
    const x = -d;
    const p = [];
    const p_amp = [];
    const p_rms = [];
    const Lp = [];
    const u = [];
    const u_amp = [];
    const I = [];
    const I_check = [];
    const p_max = [];
    const p_min = [];
    const SWR = [];
    const lambda = [];
    const d_first_min = [];

    for (let i = 0; i < N; i++) {
      const ki = k[i % k.length];
      const pi = p_i_peak[i % p_i_peak.length];
      const ri = R_c[i];
      const fwd = cMul(pi, cExpJ(-ki * x));
      const bwd = cMul(cMul(ri, pi), cExpJ(ki * x));
      const pTot = cAdd(fwd, bwd);
      const uTot = cDiv(cSub(fwd, bwd), C.rho_c);
      const pAmp = cAbs(pTot);
      const pRms = pAmp / Math.SQRT2;
      p.push(pTot);
      p_amp.push(pAmp);
      p_rms.push(pRms);
      Lp.push(20 * Math.log10(pRms / C.p_ref));
      u.push(uTot);
      u_amp.push(cAbs(uTot));
      I.push(0.5 * cMul(pTot, cConj(uTot)).re);
      I_check.push(Math.pow(cAbs(pi), 2) * (1 - Math.pow(cAbs(ri), 2)) / (2 * C.rho_c));
      const rMag = cAbs(ri);
      const pMax = cAbs(pi) * (1 + rMag);
      const pMin = cAbs(pi) * (1 - rMag);
      p_max.push(pMax);
      p_min.push(pMin);
      SWR.push(pMin > 0 ? pMax / pMin : Infinity);
      const lam = C.c / f[i % f.length];
      lambda.push(lam);
      d_first_min.push(lam / 4);
    }

    // Two media transmission
    const R12 = (z2 - z1) / (z2 + z1);
    const Tp = 2 * z2 / (z1 + z2);
    const tau = 4 * z1 * z2 / Math.pow(z1 + z2, 2);
    const atten_dB = -10 * Math.log10(tau);
    const pi_over_pt_dB = 20 * Math.log10(1 / Tp);
    const Z_ideal_venus = rho_planet * c_planet;

    const warnings = [
      inputIsRms
        ? 'Input treated as RMS pressure (converted to peak ×√2 for phasor formulas).'
        : 'Input treated as PEAK complex amplitude (exam convention: divide |p| by √2 before SPL).',
      R_sign < 0
        ? 'Soft boundary (R < 0): pressure minimum at x = 0 (like air bubbles in water or open tube end).'
        : 'Positive reflection (R > 0): pressure maximum at x = 0 (hard surface / water from air).'
    ];

    const steps = [
      {
        title: 'Step 1 — Characteristic impedance & reflection coefficient',
        latex: mode === 'Z'
          ? '\\rho c = \\rho \\cdot c, \\qquad R = \\frac{Z - \\rho c}{Z + \\rho c}'
          : '\\rho c = \\rho \\cdot c, \\qquad \\alpha = 1 - |R|^2 \\implies R = \\pm\\sqrt{1 - \\alpha}',
        sub: `ρc = ${C.rho} × ${C.c} = ${fmtNum(C.rho_c)} Pa·s/m;  α = [${alpha_out.map(v => fmtNum(v)).join(', ')}]`,
        result: `R = [${R_c.map(v => fmtComplex(v, 4)).join(', ')}]`,
        plain: `R = sqrt(1 - alpha) = [${R_c.map(v => fmtComplex(v, 4)).join(', ')}]`
      },
      {
        title: 'Step 2 — Wavenumber k and evaluation coordinate x = -d',
        latex: 'k = \\frac{2\\pi f}{c}, \\qquad x = -d',
        sub: `f = [${f.join(', ')}] Hz, c = ${C.c} m/s, d = ${d} m`,
        result: `k = [${k.map(v => fmtNum(v, 4)).join(', ')}] rad/m,  x = ${x} m`,
        plain: `k = 2*pi*f/c = [${k.map(v => fmtNum(v, 4)).join(', ')}] rad/m, x = -${d} m`
      },
      {
        title: 'Step 3 — Total complex pressure & amplitude at distance d',
        latex: 'p(x) = p_i e^{-jkx} + R\\,p_i e^{+jkx}, \\qquad p_{\\mathrm{rms}} = \\frac{|p|}{\\sqrt{2}}, \\qquad L_p = 20\\log_{10}\\frac{p_{\\mathrm{rms}}}{20\\,\\mu\\mathrm{Pa}}',
        sub: f.map((fi, idx) => `${fi} Hz: p(${x}) = (${fmtComplex(p_i_peak[idx % p_i_peak.length])})·(e^{j·${fmtNum(k[idx] * d, 4)}} + ${fmtComplex(R_c[idx])}·e^{-j·${fmtNum(k[idx] * d, 4)}})`).join(' | '),
        result: f.map((fi, idx) => `${fi} Hz: |p| = ${fmtFixed(p_amp[idx], 3)} Pa (p_rms = ${fmtFixed(p_rms[idx], 3)} Pa, L_p = ${fmtFixed(Lp[idx], 1)} dB)`).join('  ;  '),
        plain: f.map((fi, idx) => `At ${fi} Hz (d = ${d} m): |p| = ${fmtFixed(p_amp[idx], 2)} Pa (p_rms = ${fmtFixed(p_rms[idx], 3)} Pa, SPL = ${fmtFixed(Lp[idx], 1)} dB)`).join('\n')
      },
      {
        title: 'Step 4 — Particle velocity u(x) and net active intensity I',
        latex: 'u(x) = \\frac{p_i e^{-jkx} - R\\,p_i e^{+jkx}}{\\rho c}, \\qquad I = \\frac{1}{2}\\mathrm{Re}\\{p\\,u^*\\} = \\frac{|p_i|^2(1-|R|^2)}{2\\rho c}',
        sub: `Note the minus sign on the reflected wave in u(x).`,
        result: f.map((fi, idx) => `${fi} Hz: |u| = ${fmtNum(u_amp[idx], 3)} m/s,  I = ${fmtNum(I[idx], 3)} W/m²`).join('  ;  '),
        plain: f.map((fi, idx) => `At ${fi} Hz: |u| = ${fmtNum(u_amp[idx], 3)} m/s, Net intensity I = ${fmtNum(I[idx], 3)} W/m^2`).join('\n')
      },
      {
        title: 'Step 5 — Two-media transmission (z₁ → z₂) & ideal impedance match',
        latex: 'R_{12} = \\frac{z_2 - z_1}{z_2 + z_1}, \\quad T_p = \\frac{2z_2}{z_1 + z_2}, \\quad \\tau = \\frac{4z_1 z_2}{(z_1 + z_2)^2}, \\quad \\Delta L_W = -10\\log_{10}\\tau',
        sub: `z₁ = ${fmtNum(z1)} Pa·s/m, z₂ = ${fmtNum(z2)} Pa·s/m`,
        result: `R₁₂ = ${fmtNum(R12, 4)}, T_p = ${fmtNum(Tp, 4)}, τ = ${fmtNum(tau, 3)}, Power loss = ${fmtFixed(atten_dB, 1)} dB (Ideal Z = ρc = ${fmtNum(Z_ideal_venus)} Pa·s/m)`,
        plain: `Transmission loss: tau = 4*z1*z2/(z1+z2)^2 = ${fmtNum(tau, 3)} -> -10*log10(tau) = ${fmtFixed(atten_dB, 1)} dB`
      }
    ];

    const highlights = f.map((fi, idx) => ({
      label: `|p| at ${fi} Hz (d=${d}m)`,
      value: fmtFixed(p_amp[idx], 2),
      unit: 'Pa (peak)',
      sub: `p_rms = ${fmtFixed(p_rms[idx], 3)} Pa · ${fmtFixed(Lp[idx], 1)} dB SPL`
    }));
    highlights.push({
      label: 'Two-Media Loss (-10 log τ)',
      value: fmtFixed(atten_dB, 1),
      unit: 'dB',
      sub: `T_p = ${fmtFixed(Tp, 3)} · R₁₂ = ${fmtFixed(R12, 4)}`
    });

    return {
      vars: {
        rho_c: C.rho_c, R, p, p_amp, p_rms, Lp, u, u_amp, I, I_check,
        p_max, p_min, SWR, lambda, d_first_min, R12, Tp, tau, atten_dB, pi_over_pt_dB, Z_ideal_venus
      },
      highlights,
      steps,
      warnings
    };
  }

  // =========================================================================
  // T02: Tube / tunnel driven by a vibrating end wall
  // =========================================================================
  function solveT02(raw = {}) {
    const C = getConsts(raw);
    const f = raw.f !== undefined ? Number(raw.f) : 240;
    const U0 = raw.U0 !== undefined ? Number(raw.U0) : 1e-3;
    const L = raw.L !== undefined ? Number(raw.L) : 20;
    const x_from_wall = raw.x_from_wall !== undefined ? Number(raw.x_from_wall) : 8;
    const Z_end = raw.Z_end !== undefined ? Number(raw.Z_end) : 1000 * 1480;
    const L_tube = raw.L_tube !== undefined ? Number(raw.L_tube) : 0.025;
    const f_node = raw.f_node !== undefined ? Number(raw.f_node) : 1000;
    const T_celsius = raw.T_celsius !== undefined ? Number(raw.T_celsius) : 20;

    const k = 2 * Math.PI * f / C.c;
    const x = -L + x_from_wall;

    // Case A: Perfect absorber (R = 0)
    const p_A = C.rho_c * U0;
    const p_A_rms = p_A / Math.SQRT2;
    const Lp_A = 20 * Math.log10(p_A_rms / C.p_ref);

    // Case B: General termination Z_end
    const R = (Z_end - C.rho_c) / (Z_end + C.rho_c);
    const denom = cSub(cExpJ(k * L), cMul(R, cExpJ(-k * L)));
    const A = cDiv(C.rho_c * U0, denom);
    const p_B = cMul(A, cAdd(cExpJ(-k * x), cMul(R, cExpJ(k * x))));
    const Lp_B = 20 * Math.log10(cAbs(p_B) / Math.SQRT2 / C.p_ref);

    // Case B with R = 1 exact (rigid/water shortcut)
    const denomR1 = cSub(cExpJ(k * L), cExpJ(-k * L)); // 2j sin(kL)
    const A_R1 = cDiv(C.rho_c * U0, denomR1);
    const p_R1 = cMul(A_R1, 2 * Math.cos(k * x));
    const Lp_R1 = 20 * Math.log10(cAbs(p_R1) / Math.SQRT2 / C.p_ref);
    const sin_kL = Math.sin(k * L);
    const f_nearest_res = Math.round(f / (C.c / (2 * L))) * (C.c / (2 * L));

    // Ideal tube resonances
    const n = [1, 2, 3, 4];
    const f_open_open = n.map(ni => ni * C.c / (2 * L_tube));
    const f_closed_open = n.map(ni => (2 * ni - 1) * C.c / (4 * L_tube));
    const lambda = C.c / f_node;
    const d_nodes = [0, 1, 2, 3].map(ni => (2 * ni + 1) * lambda / 4);
    const c_at_T = 20.05 * Math.sqrt(273.15 + T_celsius);

    const warnings = [];
    if (Math.abs(sin_kL) < 0.1) {
      warnings.push(`RESONANCE WARNING: sin(kL) = ${fmtNum(sin_kL, 3)} is very close to 0 (nearest closed-closed resonance is ${fmtFixed(f_nearest_res, 2)} Hz). Standing-wave SPL is extremely sensitive to c! Note this in your Part 1 answer.`);
    }
    warnings.push('Case A (R = 0): Pure progressive plane wave; |p| = ρc·U₀ is constant everywhere along the tunnel.');
    warnings.push('Case B (R ≈ +1): Standing wave; p = 2A cos(kx) with pressure maximum at x = 0 (termination) and nodes every λ/2.');

    const steps = [
      {
        title: 'Step 1 — Wavenumber k and coordinate x (termination at x = 0, wall at x = -L)',
        latex: 'k = \\frac{2\\pi f}{c}, \\qquad x = -L + x_{\\mathrm{wall}}',
        sub: `f = ${f} Hz, c = ${C.c} m/s, L = ${L} m, x_wall = ${x_from_wall} m`,
        result: `k = ${fmtNum(k, 4)} rad/m,  x = ${x} m`,
        plain: `k = 2*pi*${f}/${C.c} = ${fmtNum(k, 4)} rad/m; termination at x = 0, field point at x = -${L} + ${x_from_wall} = ${x} m`
      },
      {
        title: 'Step 2 — Case A: Perfect absorber at far end (α = 1 → R = 0)',
        latex: '|p| = \\rho c\\,U_0, \\qquad p_{\\mathrm{rms}} = \\frac{|p|}{\\sqrt{2}}, \\qquad L_p = 20\\log_{10}\\frac{p_{\\mathrm{rms}}}{20\\,\\mu\\mathrm{Pa}}',
        sub: `|p| = ${fmtNum(C.rho_c)} × ${U0} = ${fmtNum(p_A, 4)} Pa (p_rms = ${fmtNum(p_A_rms, 4)} Pa)`,
        result: `L_p (absorber) = ${fmtFixed(Lp_A, 1)} dB (official rounds 0.412/√2 to 0.286 Pa → 83.1 dB; exact is 83.3 dB)`,
        plain: `Case A (absorber, R=0): progressive plane wave, |p| = rho*c*U0 = ${fmtNum(p_A, 3)} Pa -> p_rms = ${fmtNum(p_A_rms, 3)} Pa -> SPL = ${fmtFixed(Lp_A, 1)} dB`
      },
      {
        title: 'Step 3 — Case B: Reflective / water termination (R ≈ +1)',
        latex: 'R = \\frac{Z_{\\mathrm{end}}-\\rho c}{Z_{\\mathrm{end}}+\\rho c}\\approx 1, \\quad A = \\frac{\\rho c\\,U_0}{e^{jkL}-R e^{-jkL}} = \\frac{\\rho c\\,U_0}{2j\\sin(kL)}, \\quad p(x) = 2A\\cos(kx)',
        sub: `R = ${fmtNum(R, 5)}, sin(kL) = ${fmtNum(sin_kL, 4)} → A_R1 = ${fmtComplex(A_R1, 3)} Pa`,
        result: `|p(${x} m)| = ${fmtFixed(cAbs(p_R1), 2)} Pa → L_p (R=1) = ${fmtFixed(Lp_R1, 1)} dB (with exact R=${fmtNum(R, 4)}: ${fmtFixed(Lp_B, 1)} dB)`,
        plain: `Case B (water/rigid, R≈1): standing wave, A = rho*c*U0/(2j*sin(kL)) = ${fmtComplex(A_R1, 3)} Pa, |p(${x} m)| = |2*A*cos(k*${x})| = ${fmtFixed(cAbs(p_R1), 2)} Pa -> SPL = ${fmtFixed(Lp_R1, 1)} dB`
      },
      {
        title: 'Step 4 — Ideal tube resonances & pressure node distances',
        latex: 'f_{n,\\text{open-open/closed-closed}} = \\frac{nc}{2L_{\\mathrm{tube}}}, \\qquad f_{n,\\text{closed-open}} = \\frac{(2n-1)c}{4L_{\\mathrm{tube}}}, \\qquad d_{\\mathrm{node}} = (2n+1)\\frac{\\lambda}{4}',
        sub: `L_tube = ${L_tube} m, node query at f = ${f_node} Hz (λ = ${fmtNum(lambda, 3)} m)`,
        result: `Closed-open f₁ = ${fmtNum(f_closed_open[0], 4)} Hz; Open-open f₁ = ${fmtNum(f_open_open[0], 4)} Hz; Nodes from rigid wall: [${d_nodes.map(v => fmtNum(v, 3)).join(', ')}] m`,
        plain: `Tube resonances (L=${L_tube} m): closed-open f1 = ${fmtNum(f_closed_open[0], 4)} Hz, open-open f1 = ${fmtNum(f_open_open[0], 4)} Hz`
      }
    ];

    return {
      vars: {
        rho_c: C.rho_c, k, p_A, Lp_A, R, A, p_B, Lp_B, A_R1, p_R1, Lp_R1,
        sin_kL, f_nearest_res, f_open_open, f_closed_open, d_nodes, c_at_T
      },
      highlights: [
        { label: 'Case A: Absorber (R=0)', value: fmtFixed(Lp_A, 1), unit: 'dB SPL', sub: `|p| = ${fmtNum(p_A, 3)} Pa · p_rms = ${fmtNum(p_A_rms, 3)} Pa` },
        { label: 'Case B: Rigid/Water (R=1)', value: fmtFixed(Lp_R1, 1), unit: 'dB SPL', sub: `|p| = ${fmtFixed(cAbs(p_R1), 2)} Pa · exact R gives ${fmtFixed(Lp_B, 1)} dB` },
        { label: 'Closed-Open Tube f₁', value: fmtNum(f_closed_open[0], 4), unit: 'Hz', sub: `L_tube = ${L_tube} m (c / 4L)` }
      ],
      steps,
      warnings
    };
  }

  // =========================================================================
  // T03: Levels, adding sources, background noise, Leq
  // =========================================================================
  function solveT03(raw = {}) {
    const C = getConsts(raw);
    // A: Amplitude to SPL
    const p_hat = raw.p_hat !== undefined ? Number(raw.p_hat) : 0.02;
    const p_rms = p_hat / Math.SQRT2;
    const Lp_A = 20 * Math.log10(p_rms / C.p_ref);

    // B: Two tones at different frequencies (or beat period average)
    const p1_hat = raw.p1_hat !== undefined ? Number(raw.p1_hat) : 0.18;
    const p2_hat = raw.p2_hat !== undefined ? Number(raw.p2_hat) : 0.14;
    const f1_B = raw.f1_B !== undefined ? Number(raw.f1_B) : 440.00;
    const f2_B = raw.f2_B !== undefined ? Number(raw.f2_B) : 440.10;
    const beat_period = Math.abs(f2_B - f1_B) > 0 ? 1 / Math.abs(f2_B - f1_B) : Infinity;
    const p_rms_B = Math.sqrt(p1_hat * p1_hat / 2 + p2_hat * p2_hat / 2);
    const Lp_B = 20 * Math.log10(p_rms_B / C.p_ref);

    // C: Two tones at SAME frequency (coherent)
    const L_one = raw.L_one !== undefined ? Number(raw.L_one) : 90;
    const phi = raw.phi !== undefined ? Number(raw.phi) : 120;
    const gain_C = cAbs(cAdd(1, cExpJ(-phi * Math.PI / 180)));
    const L_C = L_one + 20 * Math.log10(gain_C);

    // D: Uncorrelated sources list
    const L_list = parseNumberList(raw.L_list !== undefined ? raw.L_list : [10, 10]);
    const L_D = 10 * Math.log10(L_list.reduce((acc, Li) => acc + Math.pow(10, Li / 10), 0));

    // E: Background noise subtraction
    const L_tot = raw.L_tot !== undefined ? Number(raw.L_tot) : 80;
    const L_bg = raw.L_bg !== undefined ? Number(raw.L_bg) : 75;
    const diff_E = Math.pow(10, L_tot / 10) - Math.pow(10, L_bg / 10);
    const L_E = diff_E > 0 ? 10 * Math.log10(diff_E) : -Infinity;

    // F: Equivalent level of on/off source
    const p_on = raw.p_on !== undefined ? Number(raw.p_on) : 0.1;
    const t_on = raw.t_on !== undefined ? Number(raw.t_on) : 4;
    const T = raw.T !== undefined ? Number(raw.T) : 24;
    const Leq_F = 10 * Math.log10((t_on / T) * (p_on * p_on) / (C.p_ref * C.p_ref));

    const p_on2 = raw.p_on2 !== undefined ? Number(raw.p_on2) : 0.05;
    const duty = raw.duty !== undefined ? Number(raw.duty) : 15 / 60;
    const Leq_F2 = 10 * Math.log10(duty * (p_on2 * p_on2) / (C.p_ref * C.p_ref));

    // G: Several levels L_i for durations t_i
    const L_i = parseNumberList(raw.L_i !== undefined ? raw.L_i : [84, 95, 71]);
    const t_i = parseNumberList(raw.t_i !== undefined ? raw.t_i : [15, 5, 20]);
    const T_sum = t_i.reduce((a, b) => a + b, 0);
    let eSumG = 0;
    for (let i = 0; i < L_i.length; i++) {
      const ti = t_i[i % t_i.length];
      eSumG += (ti / T_sum) * Math.pow(10, L_i[i] / 10);
    }
    const Leq_G = 10 * Math.log10(eSumG);

    // H: Sound exposure level L_AE of n events
    const L_AE = raw.L_AE !== undefined ? Number(raw.L_AE) : 90;
    const n_ev = raw.n_ev !== undefined ? Number(raw.n_ev) : 100;
    const T_s = raw.T_s !== undefined ? Number(raw.T_s) : 8 * 3600;
    const Leq_H = L_AE + 10 * Math.log10(n_ev) - 10 * Math.log10(T_s);

    const steps = [
      {
        title: 'Block A — Peak amplitude to RMS and SPL (Week 3 P1.1)',
        latex: 'p_{\\mathrm{rms}} = \\frac{\\hat{p}}{\\sqrt{2}}, \\qquad L_p = 20\\log_{10}\\frac{p_{\\mathrm{rms}}}{p_{\\mathrm{ref}}}',
        sub: `p̂ = ${p_hat} Pa → p_rms = ${fmtNum(p_rms, 4)} Pa`,
        result: `L_p = ${fmtFixed(Lp_A, 1)} dB`,
        plain: `p_rms = ${p_hat}/sqrt(2) = ${fmtNum(p_rms, 4)} Pa -> L_p = 20*log10(${fmtNum(p_rms, 4)}/20e-6) = ${fmtFixed(Lp_A, 1)} dB`
      },
      {
        title: 'Block B — Two tones at different frequencies / beat average (2022 MC2)',
        latex: 'p_{\\mathrm{rms}} = \\sqrt{\\frac{\\hat{p}_1^2}{2} + \\frac{\\hat{p}_2^2}{2}}, \\qquad T_{\\mathrm{beat}} = \\frac{1}{|f_2 - f_1|}',
        sub: `p̂₁ = ${p1_hat} Pa, p̂₂ = ${p2_hat} Pa (T_beat = ${fmtNum(beat_period, 3)} s)`,
        result: `p_rms = ${fmtFixed(p_rms_B, 3)} Pa (${fmtFixed(Lp_B, 1)} dB)`,
        plain: `Incoherent / beat-averaged rms pressure: p_rms = sqrt((${p1_hat}^2 + ${p2_hat}^2)/2) = ${fmtFixed(p_rms_B, 3)} Pa`
      },
      {
        title: 'Block C — Two coherent equal tones with phase difference φ (Week 3 P2.2)',
        latex: 'L = L_1 + 20\\log_{10}|1 + e^{-j\\phi}| = L_1 + 10\\log_{10}(2 + 2\\cos\\phi)',
        sub: `L₁ = ${L_one} dB, φ = ${phi}° → gain = ${fmtNum(gain_C, 4)}`,
        result: `L_total = ${fmtFixed(L_C, 2)} dB`,
        plain: `Coherent sum (phi = ${phi} deg): L = ${L_one} + 10*log10(2 + 2*cos(${phi} deg)) = ${fmtFixed(L_C, 2)} dB`
      },
      {
        title: 'Block D & E — Uncorrelated dB addition & background subtraction',
        latex: 'L_{\\mathrm{sum}} = 10\\log_{10}\\sum_i 10^{L_i/10}, \\qquad L_{\\mathrm{src}} = 10\\log_{10}\\left(10^{L_{\\mathrm{tot}}/10} - 10^{L_{\\mathrm{bg}}/10}\\right)',
        sub: `Sum of [${L_list.join(', ')}] dB;  Background: L_tot = ${L_tot} dB, L_bg = ${L_bg} dB`,
        result: `L_sum = ${fmtFixed(L_D, 1)} dB  |  L_src (corrected) = ${fmtFixed(L_E, 1)} dB`,
        plain: `Uncorrelated sum: L = 10*log10(sum(10^(L_i/10))) = ${fmtFixed(L_D, 1)} dB; Background corrected: L_src = ${fmtFixed(L_E, 1)} dB`
      },
      {
        title: 'Block F, G, H — Equivalent continuous sound level L_eq,T',
        latex: 'L_{\\mathrm{eq},T} = 10\\log_{10}\\left(\\frac{t_{\\mathrm{on}}}{T}\\frac{p_{\\mathrm{on,rms}}^2}{p_{\\mathrm{ref}}^2}\\right) = 10\\log_{10}\\sum_i \\frac{t_i}{T}10^{L_i/10}',
        sub: `F1: ${p_on} Pa for ${t_on}/${T} h; F2: ${p_on2} Pa for duty ${fmtNum(duty, 3)}; G: L=[${L_i.join(',')}], t=[${t_i.join(',')}]`,
        result: `Leq_F (24h) = ${fmtFixed(Leq_F, 1)} dB · Leq_F2 (duty) = ${fmtFixed(Leq_F2, 1)} dB · Leq_G = ${fmtFixed(Leq_G, 1)} dB · Leq_H (SEL) = ${fmtFixed(Leq_H, 1)} dB`,
        plain: `Leq (on/off): ${fmtFixed(Leq_F, 1)} dB; Leq (duty ${fmtNum(duty, 3)}): ${fmtFixed(Leq_F2, 1)} dB; Leq (multi-interval): ${fmtFixed(Leq_G, 1)} dB`
      }
    ];

    return {
      vars: {
        p_rms, Lp_A, beat_period, p_rms_B, Lp_B, gain_C, L_C, L_D, L_E, Leq_F, Leq_F2, Leq_G, Leq_H
      },
      highlights: [
        { label: 'A: SPL from Amplitude', value: fmtFixed(Lp_A, 1), unit: 'dB', sub: `p̂ = ${p_hat} Pa → p_rms = ${fmtNum(p_rms, 3)} Pa` },
        { label: 'B: Two Tones p_rms', value: fmtFixed(p_rms_B, 3), unit: 'Pa', sub: `${fmtFixed(Lp_B, 1)} dB (incoherent / beat avg)` },
        { label: 'D: Uncorrelated Sum', value: fmtFixed(L_D, 1), unit: 'dB', sub: `Inputs: [${L_list.join(', ')}] dB` },
        { label: 'E: Bg-Corrected L_src', value: fmtFixed(L_E, 1), unit: 'dB', sub: `L_tot=${L_tot} dB, L_bg=${L_bg} dB` },
        { label: 'F: On/Off L_eq,T', value: fmtFixed(Leq_F, 1), unit: 'dB', sub: `F2 (duty): ${fmtFixed(Leq_F2, 1)} dB · G: ${fmtFixed(Leq_G, 1)} dB` }
      ],
      steps,
      warnings: [
        'TRAP: Check whether the given pressure is AMPLITUDE (divide by √2) or already RMS (like 2022 MC3 and 2024 MC2).',
        'TRAP: Two tones separated by Δf = 0.1 Hz averaged over 10 s = 1/Δf complete a full beat cycle → cross term averages to zero (add as incoherent mean squares).'
      ]
    };
  }

  // =========================================================================
  // T04: Spectral components into octave / third-octave bands & A-weighting
  // =========================================================================
  function solveT04(raw = {}) {
    const C = getConsts(raw);
    const f = parseNumberList(raw.f !== undefined ? raw.f : [334, 668, 1002, 501, 1002, 1503]);
    const P = parseComplexList(raw.P !== undefined ? raw.P : ['0.1', '0.001j', '0.04', '0.2', '0.05', '0.02j']);
    const fc = parseNumberList(raw.fc !== undefined ? raw.fc : [125, 250, 500, 1000, 2000]);
    const n_oct = raw.n_oct !== undefined ? Number(raw.n_oct) : 1; // 1 = octave, 3 = third-octave
    const detuneCount = raw.detuneCount !== undefined ? Number(raw.detuneCount) : 3;
    const detuneFactor = raw.detuneFactor !== undefined ? Number(raw.detuneFactor) : 0.99;

    // Step 1: Merge components at exact same frequency (coherent complex sum)
    const freqMap = new Map();
    for (let i = 0; i < f.length; i++) {
      const fi = f[i];
      const pi = P[i % P.length];
      if (freqMap.has(fi)) {
        freqMap.set(fi, cAdd(freqMap.get(fi), pi));
      } else {
        freqMap.set(fi, cplx(pi));
      }
    }
    const f_u = Array.from(freqMap.keys()).sort((a, b) => a - b);
    const P_u = f_u.map(fi => freqMap.get(fi));

    // Step 2: Band edges
    const factor = Math.pow(2, 1 / (2 * n_oct));
    const edges = fc.map(fci => [fci / factor, fci * factor]);

    // Step 3 & 4: Assign merged frequencies to bands and sum |P|^2 / 2
    const p2_band = [];
    const p_rms_band = [];
    const Lp_band = [];
    const bandComponents = [];

    for (let b = 0; b < fc.length; b++) {
      const [fl, fu] = edges[b];
      let sumP2 = 0;
      const comps = [];
      for (let j = 0; j < f_u.length; j++) {
        if (f_u[j] >= fl && f_u[j] < fu) {
          const amp = cAbs(P_u[j]);
          sumP2 += (amp * amp) / 2;
          comps.push(`${f_u[j]} Hz (|P|=${fmtNum(amp, 3)} Pa)`);
        }
      }
      p2_band.push(sumP2);
      p_rms_band.push(Math.sqrt(sumP2));
      Lp_band.push(sumP2 > 0 ? 10 * Math.log10(sumP2 / (C.p_ref * C.p_ref)) : -Infinity);
      bandComponents.push(comps);
    }
    const totalP2 = p2_band.reduce((a, b) => a + b, 0);
    const Lp_total = totalP2 > 0 ? 10 * Math.log10(totalP2 / (C.p_ref * C.p_ref)) : -Infinity;

    // Step 5: Detuned version (first detuneCount components shifted by detuneFactor)
    const f_detuned = f.map((fi, idx) => idx < detuneCount ? fi * detuneFactor : fi);
    const Lp_band_detuned = fc.map((fci, b) => {
      const [fl, fu] = edges[b];
      let sumP2 = 0;
      for (let i = 0; i < f_detuned.length; i++) {
        if (f_detuned[i] >= fl && f_detuned[i] < fu) {
          const amp = cAbs(P[i % P.length]);
          sumP2 += (amp * amp) / 2;
        }
      }
      return sumP2 > 0 ? 10 * Math.log10(sumP2 / (C.p_ref * C.p_ref)) : -Infinity;
    });

    // Block B: A-weighted level of tones (2024 P1.2)
    const f_B = parseNumberList(raw.f_B !== undefined ? raw.f_B : [400, 630]);
    const p_B = parseNumberList(raw.p_B !== undefined ? raw.p_B : [0.89, 0.86]);
    const K_B = f_B.map(interpAWeight);
    const pA_rms = p_B.map((pb, idx) => (pb / Math.SQRT2) * Math.pow(10, K_B[idx] / 20));
    const LA_B = 10 * Math.log10(pA_rms.reduce((acc, v) => acc + v * v, 0) / (C.p_ref * C.p_ref));

    // Block C: A-weighted total from band levels (slides 34-35)
    const fc_C = parseNumberList(raw.fc_C !== undefined ? raw.fc_C : [125, 250, 500, 1000]);
    const L_C = parseNumberList(raw.L_C !== undefined ? raw.L_C : [70, 75, 80, 42]);
    const K_C = fc_C.map(interpAWeight);
    const LZ_C = 10 * Math.log10(L_C.reduce((acc, Li) => acc + Math.pow(10, Li / 10), 0));
    const LA_C = 10 * Math.log10(L_C.reduce((acc, Li, idx) => acc + Math.pow(10, (Li + K_C[idx]) / 10), 0));

    // Block D & E: Third octaves into octave; harmonic series
    const L_thirds = parseNumberList(raw.L_thirds !== undefined ? raw.L_thirds : [55, 55, 55]);
    const L_oct = 10 * Math.log10(L_thirds.reduce((acc, Li) => acc + Math.pow(10, Li / 10), 0));
    const f0 = raw.f0 !== undefined ? Number(raw.f0) : 769;
    const fc_harm = raw.fc_harm !== undefined ? Number(raw.fc_harm) : 4000;
    let n_in_4k = 0;
    for (let n = 1; n <= 30; n++) {
      const fn = n * f0;
      if (fn >= fc_harm / Math.SQRT2 && fn < fc_harm * Math.SQRT2) n_in_4k++;
    }

    const steps = [
      {
        title: 'Step 1 — Merge identical frequencies as complex numbers (coherent sum)',
        latex: 'P(f) = \\sum_{f_i = f} P_i',
        sub: f_u.map((fu, idx) => `${fu} Hz: P = ${fmtComplex(P_u[idx], 3)} Pa (|P| = ${fmtNum(cAbs(P_u[idx]), 3)} Pa)`).join(' · '),
        result: `${f_u.length} distinct frequencies from ${f.length} input components`,
        plain: 'Merged components: ' + f_u.map((fu, idx) => `${fu} Hz -> |P| = ${fmtNum(cAbs(P_u[idx]), 3)} Pa`).join(', ')
      },
      {
        title: `Step 2 & 3 — Band edges (1/${n_oct} octave: f_c · 2^{±1/${2 * n_oct}}) & band SPLs`,
        latex: 'f_l = f_c 2^{-1/(2n)}, \\quad f_u = f_c 2^{+1/(2n)}, \\quad p_{\\mathrm{rms,band}}^2 = \\sum_{f \\in [f_l, f_u)} \\frac{|P(f)|^2}{2}, \\quad L_{p,\\mathrm{band}} = 10\\log_{10}\\frac{p_{\\mathrm{rms,band}}^2}{p_{\\mathrm{ref}}^2}',
        sub: fc.map((fci, b) => `${fci} Hz [${fmtFixed(edges[b][0], 1)}–${fmtFixed(edges[b][1], 1)} Hz]: ${bandComponents[b].length ? bandComponents[b].join(' + ') : 'empty'}`).join(' | '),
        result: fc.map((fci, b) => `${fci} Hz: ${Lp_band[b] === -Infinity ? '-∞ dB' : fmtFixed(Lp_band[b], 1) + ' dB (' + fmtFixed(p_rms_band[b], 4) + ' Pa)'}`).join('  ;  '),
        plain: fc.map((fci, b) => `Band ${fci} Hz [${fmtFixed(edges[b][0], 1)}-${fmtFixed(edges[b][1], 1)} Hz]: p_rms = ${fmtFixed(p_rms_band[b], 4)} Pa, SPL = ${Lp_band[b] === -Infinity ? '-Inf' : fmtFixed(Lp_band[b], 1)} dB (detuned: ${Lp_band_detuned[b] === -Infinity ? '-Inf' : fmtFixed(Lp_band_detuned[b], 1)} dB)`).join('\n')
      },
      {
        title: 'Block B — A-weighting of individual tones before adding (2024 P1.2)',
        latex: 'p_{A,\\mathrm{rms},i} = \\frac{|p_i|}{\\sqrt{2}}10^{K_A(f_i)/20}, \\qquad L_A = 10\\log_{10}\\frac{\\sum_i p_{A,\\mathrm{rms},i}^2}{p_{\\mathrm{ref}}^2}',
        sub: f_B.map((fb, idx) => `${fb} Hz: |p|=${p_B[idx]} Pa, K_A=${fmtFixed(K_B[idx], 1)} dB → p_A,rms=${fmtFixed(pA_rms[idx], 3)} Pa`).join(' ; '),
        result: `L_A = ${fmtFixed(LA_B, 1)} dB(A)`,
        plain: `A-weighted tones: ${f_B.map((fb, idx) => `${fb} Hz (K_A=${fmtFixed(K_B[idx], 1)} dB) -> p_A,rms = ${fmtFixed(pA_rms[idx], 3)} Pa`).join(', ')} -> L_A = ${fmtFixed(LA_B, 1)} dB(A)`
      },
      {
        title: 'Block C — Overall unweighted (L_Z) and A-weighted (L_A) level from band levels',
        latex: 'L_Z = 10\\log_{10}\\sum_i 10^{L_i/10}, \\qquad L_A = 10\\log_{10}\\sum_i 10^{(L_i + K_{A,i})/10}',
        sub: fc_C.map((fcc, idx) => `${fcc} Hz: L=${L_C[idx]} dB (K_A=${fmtFixed(K_C[idx], 1)} dB)`).join(', '),
        result: `L_Z = ${fmtFixed(LZ_C, 1)} dB  |  L_A = ${fmtFixed(LA_C, 1)} dB(A)`,
        plain: `Band totals: L_Z = ${fmtFixed(LZ_C, 1)} dB, L_A = ${fmtFixed(LA_C, 1)} dB(A)`
      }
    ];

    const highlights = fc.map((fci, b) => ({
      label: `${fci} Hz Band SPL`,
      value: Lp_band[b] === -Infinity ? '-∞' : fmtFixed(Lp_band[b], 1),
      unit: 'dB',
      sub: `p_rms = ${fmtFixed(p_rms_band[b], 4)} Pa · Detuned: ${Lp_band_detuned[b] === -Infinity ? '-∞' : fmtFixed(Lp_band_detuned[b], 1)} dB`
    }));
    highlights.push({
      label: 'Block B: Tone List L_A',
      value: fmtFixed(LA_B, 1),
      unit: 'dB(A)',
      sub: `Block C Band L_A: ${fmtFixed(LA_C, 1)} dB(A) (L_Z: ${fmtFixed(LZ_C, 1)} dB)`
    });

    return {
      vars: {
        f_u, P_u, edges, p2_band, p_rms_band, Lp_band, Lp_total,
        Lp_band_detuned, K_B, pA_rms, LA_B, K_C, LZ_C, LA_C, L_oct, n_in_4k
      },
      highlights,
      steps,
      warnings: [
        'DECISION: Merge identical frequencies as complex numbers FIRST (e.g. 1002 Hz in 2023 P2, 1200 Hz in 2022 P2). If detuned by 1%, they are different frequencies and add as mean squares!',
        'TRAP: An empty octave band has 0 Pa rms = -∞ dB (write -∞ dB explicitly, never 0 dB!).',
        'TRAP: When A-weighting tones inside a single octave band (2024 P1.2), apply each tone’s own K_A(f) before summing mean squares.'
      ]
    };
  }

  // =========================================================================
  // T05: Intensity, sound power, standing-wave ratio (SWR)
  // =========================================================================
  function solveT05(raw = {}) {
    const C = getConsts(raw);
    const P_A = parseComplexToken(raw.P_A !== undefined ? raw.P_A : '0.02+0.0275j');
    const U_A_raw = parseComplexToken(raw.U_A !== undefined ? raw.U_A : '107.4e-6-44.6e-6j');
    const PUconj = cMul(P_A, cConj(U_A_raw));
    const I_A = 0.5 * PUconj.re;
    const Q_reactive = 0.5 * PUconj.im;
    const phase_deg = cArgDeg(cDiv(P_A, U_A_raw));

    // B: Plane travelling wave SPL -> I -> W
    const Lp_B = raw.Lp_B !== undefined ? Number(raw.Lp_B) : 82;
    const S_B = raw.S_B !== undefined ? Number(raw.S_B) : 10;
    const p_rms_B = C.p_ref * Math.pow(10, Lp_B / 20);
    const I_B = (p_rms_B * p_rms_B) / C.rho_c;
    const W_B = I_B * S_B;
    const LI_B = 10 * Math.log10(I_B / C.I_ref);
    const LW_B = 10 * Math.log10(W_B / C.W_ref);

    // C & D: Standing-wave tube Lmax and Lmin
    const Lmax = raw.Lmax !== undefined ? Number(raw.Lmax) : 85;
    const Lmin = raw.Lmin !== undefined ? Number(raw.Lmin) : 74;
    const S_tube = raw.S_tube !== undefined ? Number(raw.S_tube) : 0.01;
    const s = raw.s_direct !== undefined && raw.s_direct !== '' ? Number(raw.s_direct) : Math.pow(10, (Lmax - Lmin) / 20);
    const R_mag = (s - 1) / (s + 1);
    const alpha = 1 - R_mag * R_mag;

    const p_max = C.p_ref * Math.pow(10, Lmax / 20);
    const p_min = C.p_ref * Math.pow(10, Lmin / 20);
    const p_inc = (p_max + p_min) / 2;
    const p_refl = (p_max - p_min) / 2;
    const W_inc = S_tube * p_inc * p_inc / C.rho_c;
    const W_abs = S_tube * p_max * p_min / C.rho_c;
    const LW_abs = 10 * Math.log10(W_abs / C.W_ref);

    // E & F: Energy densities & acoustic port power
    const w_p = Math.pow(cAbs(P_A), 2) / (4 * C.rho * C.c * C.c);
    const w_k = C.rho * Math.pow(cAbs(U_A_raw), 2) / 4;
    const Q_F = parseComplexToken(raw.Q_F !== undefined ? raw.Q_F : '1e-4');
    const Za_F = parseComplexToken(raw.Za_F !== undefined ? raw.Za_F : '4e5+2e5j');
    const W_F = 0.5 * Math.pow(cAbs(Q_F), 2) * Za_F.re;

    const steps = [
      {
        title: 'Block A — Active intensity from complex pressure P and velocity U',
        latex: 'I = \\frac{1}{2}\\mathrm{Re}\\{P\\,U^*\\} = p_{\\mathrm{rms}}u_{\\mathrm{rms}}\\cos\\phi',
        sub: `P = ${fmtComplex(P_A, 3)} Pa, U = ${fmtComplex(U_A_raw, 3)} m/s (phase φ = ${fmtFixed(phase_deg, 1)}°)`,
        result: `I = ${fmtNum(I_A, 4)} W/m² (${fmtNum(I_A * 1e9, 4)} nW/m²)`
      },
      {
        title: 'Block B — Plane wave SPL to intensity and power through area S (Week 4 P2)',
        latex: 'p_{\\mathrm{rms}} = p_{\\mathrm{ref}}10^{L_p/20}, \\qquad I = \\frac{p_{\\mathrm{rms}}^2}{\\rho c}, \\qquad W = I\\,S',
        sub: `L_p = ${Lp_B} dB → p_rms = ${fmtNum(p_rms_B, 3)} Pa; S = ${S_B} m²`,
        result: `I = ${fmtNum(I_B, 3)} W/m²,  W = ${fmtNum(W_B, 3)} W (${fmtFixed(W_B * 1e3, 2)} mW, L_W = ${fmtFixed(LW_B, 1)} dB)`
      },
      {
        title: 'Block C & D — Standing-wave tube: SWR, α, and absorbed power (Week 4 P4)',
        latex: 's = 10^{(L_{\\max}-L_{\\min})/20}, \\quad |R| = \\frac{s-1}{s+1}, \\quad \\alpha = 1 - |R|^2 = \\frac{4s}{(s+1)^2}, \\quad W_{\\mathrm{abs}} = \\frac{S\\,p_{\\max,\\mathrm{rms}}p_{\\min,\\mathrm{rms}}}{\\rho c}',
        sub: `L_max = ${Lmax} dB (p_max = ${fmtNum(p_max, 3)} Pa), L_min = ${Lmin} dB (p_min = ${fmtNum(p_min, 3)} Pa), S = ${S_tube} m²`,
        result: `s = ${fmtNum(s, 3)}, |R| = ${fmtNum(R_mag, 3)}, α = ${fmtFixed(alpha, 2)}, W_abs = ${fmtNum(W_abs, 3)} W (L_W,abs = ${fmtFixed(LW_abs, 1)} dB)`
      }
    ];

    return {
      vars: {
        rho_c: C.rho_c, I_A, phase_deg, Q_reactive, p_rms_B, I_B, W_B, LI_B, LW_B,
        s, R_mag, alpha, p_max, p_min, p_inc, p_refl, W_inc, W_abs, LW_abs, w_p, w_k, W_F
      },
      highlights: [
        { label: 'A: Complex Intensity I', value: fmtNum(I_A, 4), unit: 'W/m²', sub: `${fmtFixed(I_A * 1e9, 1)} nW/m² · φ = ${fmtFixed(phase_deg, 1)}°` },
        { label: 'B: Plane Wave Power W', value: fmtNum(W_B, 3), unit: 'W', sub: `I = ${fmtNum(I_B, 3)} W/m² · L_W = ${fmtFixed(LW_B, 1)} dB` },
        { label: 'C: Tube Absorption α', value: fmtFixed(alpha, 3), unit: '', sub: `SWR s = ${fmtFixed(s, 2)} · |R| = ${fmtFixed(R_mag, 3)}` },
        { label: 'D: Absorbed Power W_abs', value: fmtNum(W_abs, 3), unit: 'W', sub: `L_W,abs = ${fmtFixed(LW_abs, 1)} dB` }
      ],
      steps,
      warnings: [
        'DECISION: With peak complex amplitudes P and U, always include the factor 1/2 in I = ½ Re{P U*}. With RMS amplitudes p_rms and u_rms, there is no 1/2.'
      ]
    };
  }

  // =========================================================================
  // T06: One monopole: pressure, near-field velocity, phase, power
  // =========================================================================
  function solveT06(raw = {}) {
    const C = getConsts(raw);
    const Q = raw.Q !== undefined ? Number(raw.Q) : 1e-5;
    const f = raw.f !== undefined ? Number(raw.f) : 500;
    const r = parseNumberList(raw.r !== undefined ? raw.r : [0.1, 0.2, 0.3]);
    const Omega = raw.Omega !== undefined ? Number(raw.Omega) : 4 * Math.PI;

    const w = 2 * Math.PI * f;
    const k = w / C.c;
    const kr = r.map(ri => k * ri);

    const P = r.map((ri, idx) => cMul({ re: 0, im: w * C.rho * Q / (Omega * ri) }, cExpJ(-kr[idx])));
    const p_amp = P.map(cAbs);
    const p_rms = p_amp.map(pa => pa / Math.SQRT2);
    const Lp = p_rms.map(pr => 20 * Math.log10(pr / C.p_ref));

    const U = P.map((Pi, idx) => cMul(cDiv(Pi, C.rho_c), { re: 1, im: -1 / kr[idx] }));
    const u_amp = U.map(cAbs);
    const phase_deg = kr.map(kri => Math.atan(1 / kri) * 180 / Math.PI);
    const Zs = kr.map(kri => cDiv(C.rho_c, { re: 1, im: -1 / kri }));
    const I = P.map((Pi, idx) => 0.5 * cMul(Pi, cConj(U[idx])).re);
    const I_check = p_amp.map(pa => (pa * pa) / (2 * C.rho_c));

    const W_free = C.rho_c * k * k * Q * Q / (8 * Math.PI);
    const W_from_I = Omega * r[0] * r[0] * I[0];
    const LW = 10 * Math.log10(W_from_I / C.W_ref);
    const Lp_from_LW = r.map(ri => LW - 10 * Math.log10(Omega * ri * ri) + 10 * Math.log10(C.rho_c * C.W_ref / (C.p_ref * C.p_ref)));

    // 2024 MC1 phase check
    const f_MC = raw.f_MC !== undefined ? Number(raw.f_MC) : 189;
    const r_MC = raw.r_MC !== undefined ? Number(raw.r_MC) : 0.5;
    const kr_MC = (2 * Math.PI * f_MC / C.c) * r_MC;
    const phase_MC = Math.atan(1 / kr_MC) * 180 / Math.PI;

    // Block E: Week 8 P1 (given p_hat at r1 -> Lp at r2 and L_W)
    const p1_hat_E = raw.p1_hat_E !== undefined ? Number(raw.p1_hat_E) : 0.1;
    const r1_E = raw.r1_E !== undefined ? Number(raw.r1_E) : 1.0;
    const r2_E = raw.r2_E !== undefined ? Number(raw.r2_E) : 0.75;
    const p1_rms = p1_hat_E / Math.SQRT2;
    const p2_rms = p1_rms * (r1_E / r2_E);
    const Lp_075 = 20 * Math.log10(p2_rms / C.p_ref);
    const LI_075 = 10 * Math.log10((p2_rms * p2_rms / C.rho_c) / C.I_ref);
    const LW_E = 10 * Math.log10((4 * Math.PI * r1_E * r1_E * p1_rms * p1_rms / C.rho_c) / C.W_ref);

    // Block F: Pulsating sphere
    const a_s = raw.a_s !== undefined ? Number(raw.a_s) : 0.05;
    const U_a = raw.U_a !== undefined ? Number(raw.U_a) : 0.01;
    const Q_s = 4 * Math.PI * a_s * a_s * U_a;
    const Zar = cMul(C.rho_c / (4 * Math.PI * a_s * a_s), cDiv({ re: 0, im: k * a_s }, { re: 1, im: k * a_s }));
    const W_sphere = 0.5 * Q_s * Q_s * Zar.re;

    const steps = [
      {
        title: 'Step 1 — Wavenumber k and dimensionless distance kr',
        latex: '\\omega = 2\\pi f, \\qquad k = \\frac{\\omega}{c}, \\qquad kr',
        sub: `f = ${f} Hz → ω = ${fmtNum(w, 4)} rad/s, k = ${fmtNum(k, 4)} rad/m`,
        result: `kr = [${kr.map(v => fmtFixed(v, 2)).join(', ')}] at r = [${r.join(', ')}] m`
      },
      {
        title: `Step 2 — Pressure amplitude |p(r)| (Ω = ${Math.abs(Omega - 2 * Math.PI) < 0.01 ? '2π baffle/plane' : '4π free space'})`,
        latex: 'P(r) = \\frac{j\\omega\\rho Q}{\\Omega r}e^{-jkr}, \\qquad |p(r)| = \\frac{\\omega\\rho |Q|}{\\Omega r}',
        sub: `Q = ${fmtNum(Q)} m³/s, ρ = ${C.rho} kg/m³`,
        result: r.map((ri, idx) => `r=${ri}m: |p| = ${fmtNum(p_amp[idx], 3)} Pa (${fmtFixed(p_amp[idx] * 1e3, 1)} mPa, ${fmtFixed(Lp[idx], 1)} dB)`).join('  ;  ')
      },
      {
        title: 'Step 3 & 4 — Near-field particle velocity |u(r)| and p–u phase angle',
        latex: 'U_r(r) = \\frac{P(r)}{\\rho c}\\left(1 + \\frac{1}{jkr}\\right), \\qquad |u(r)| = \\frac{|p(r)|}{\\rho c}\\sqrt{1 + \\frac{1}{(kr)^2}}, \\qquad \\phi_{p-u} = \\arctan\\left(\\frac{1}{kr}\\right)',
        sub: `At f_MC=${f_MC} Hz, r_MC=${r_MC} m: kr=${fmtFixed(kr_MC, 2)} → φ = ${fmtFixed(phase_MC, 1)}°`,
        result: r.map((ri, idx) => `r=${ri}m: |u| = ${fmtFixed(u_amp[idx] * 1e6, 1)} µm/s (φ = ${fmtFixed(phase_deg[idx], 1)}°)`).join('  ;  ')
      },
      {
        title: 'Step 5 & 6 — Active intensity I(r), radiated power W, and Block E (distance law)',
        latex: 'I(r) = \\frac{|p(r)|^2}{2\\rho c} = \\frac{p_{\\mathrm{rms}}^2}{\\rho c}, \\qquad W = \\Omega r^2 I(r) = \\frac{\\rho c k^2 |Q|^2}{2\\Omega}',
        sub: `Block E (${p1_hat_E} Pa peak at ${r1_E} m → ${r2_E} m): L_p(${r2_E}m) = ${fmtFixed(Lp_075, 2)} dB, L_W = ${fmtFixed(LW_E, 2)} dB`,
        result: `W = ${fmtNum(W_from_I, 4)} W (L_W = ${fmtFixed(LW, 1)} dB) · I = [${I.map(v => fmtNum(v, 3)).join(', ')}] W/m²`
      }
    ];

    const highlights = r.map((ri, idx) => ({
      label: `r = ${ri} m (kr = ${fmtFixed(kr[idx], 2)})`,
      value: `${fmtFixed(p_amp[idx] * 1e3, 1)} mPa`,
      unit: `|u| = ${fmtFixed(u_amp[idx] * 1e6, 1)} µm/s`,
      sub: `L_p = ${fmtFixed(Lp[idx], 1)} dB · Phase φ = ${fmtFixed(phase_deg[idx], 1)}°`
    }));
    highlights.push({
      label: 'MC Phase / Block E',
      value: `${fmtFixed(phase_MC, 1)}°`,
      unit: `at ${f_MC}Hz, ${r_MC}m`,
      sub: `Block E: L_p(${r2_E}m) = ${fmtFixed(Lp_075, 2)} dB · L_W = ${fmtFixed(LW_E, 2)} dB`
    });

    return {
      vars: {
        rho_c: C.rho_c, w, k, kr, P, p_amp, p_rms, Lp, U, u_amp, phase_deg, Zs,
        I, I_check, W_free, W_from_I, LW, Lp_from_LW, phase_MC, Lp_075, LI_075, LW_E, Q_s, Zar, W_sphere
      },
      highlights,
      steps,
      warnings: [
        'DECISION: Free field = 4πr (and power over 4πr²). Rigid plane / infinite baffle = 2πr (and power over 2πr²).',
        'TRAP (2024 MC1): Phase between p and u is arctan(1 / kr), NOT arctan(kr)! At kr = 1.73, arctan(1/1.73) = 30° (60° is the trap).'
      ]
    };
  }

  // =========================================================================
  // T07: Two monopoles, line between sources, rigid wall, dipole
  // =========================================================================
  function solveT07(raw = {}) {
    const C = getConsts(raw);

    // Block A: Two sources on x-axis, field points between them (2024 P2.2)
    const f_A = raw.f_A !== undefined ? Number(raw.f_A) : 500;
    const D = raw.D !== undefined ? Number(raw.D) : 0.4;
    const Q1 = parseComplexToken(raw.Q1 !== undefined ? raw.Q1 : 1e-5);
    const Q2 = parseComplexToken(raw.Q2 !== undefined ? raw.Q2 : -1e-5);
    const x = parseNumberList(raw.x !== undefined ? raw.x : [0.1, 0.2, 0.3]);

    const w_A = 2 * Math.PI * f_A;
    const k_A = w_A / C.c;
    const r1 = x.slice();
    const r2 = x.map(xi => D - xi);

    const p1 = r1.map(r1i => cMul(cMul({ re: 0, im: w_A * C.rho / (4 * Math.PI * r1i) }, Q1), cExpJ(-k_A * r1i)));
    const p2 = r2.map(r2i => cMul(cMul({ re: 0, im: w_A * C.rho / (4 * Math.PI * r2i) }, Q2), cExpJ(-k_A * r2i)));
    const p_tot = p1.map((p1i, idx) => cAdd(p1i, p2[idx]));
    const p_rms_A = p_tot.map(pt => cAbs(pt) / Math.SQRT2);

    // Velocity along +x: source 1 pushes +x, source 2 pushes -x -> u_x = u1 - u2
    const u_tot = p1.map((p1i, idx) => {
      const u1 = cMul(cDiv(p1i, C.rho_c), { re: 1, im: -1 / (k_A * r1[idx]) });
      const u2 = cMul(cDiv(p2[idx], C.rho_c), { re: 1, im: -1 / (k_A * r2[idx]) });
      return cSub(u1, u2);
    });
    const u_rms_A = u_tot.map(ut => cAbs(ut) / Math.SQRT2);
    const I_A = p_tot.map((pt, idx) => 0.5 * cMul(pt, cConj(u_tot[idx])).re);

    // Block B: Monopole at distance h from a rigid wall (2023 P3)
    const h = raw.h !== undefined ? Number(raw.h) : 2;
    const f_B = parseNumberList(raw.f_B !== undefined ? raw.f_B : [20, 200, 2000]);
    const Q_B = parseNumberList(raw.Q_B !== undefined ? raw.Q_B : [3e-3, 4e-4, 5e-5]);
    const k_B = f_B.map(fb => 2 * Math.PI * fb / C.c);
    const kh = k_B.map(kb => kb * h);
    const W_free = k_B.map((kb, idx) => C.rho_c * kb * kb * Math.pow(Q_B[idx % Q_B.length], 2) / (8 * Math.PI));
    const W_wall = W_free.map(( wf, idx) => {
      const twoKh = 2 * kh[idx];
      const sinc = twoKh === 0 ? 1 : Math.sin(twoKh) / twoKh;
      return wf * (1 + sinc);
    });
    const gain_dB = W_wall.map((ww, idx) => 10 * Math.log10(ww / W_free[idx]));

    // Intensity on line source -> wall (2023 P3.2)
    const f_B2 = raw.f_B2 !== undefined ? Number(raw.f_B2) : 200;
    const Q_B2 = raw.Q_B2 !== undefined ? Number(raw.Q_B2) : 4e-4;
    const d_from_wall = parseNumberList(raw.d_from_wall !== undefined ? raw.d_from_wall : [0, 0.5, 1]);
    const r_B = d_from_wall.map(dw => h - dw);
    const w_B = 2 * Math.PI * f_B2;
    const k_B2 = w_B / C.c;
    const pr = r_B.map(rb => cMul({ re: 0, im: w_B * C.rho * Q_B2 / (4 * Math.PI * rb) }, cExpJ(-k_B2 * rb)));
    const pim = r_B.map(rb => {
      const rim = 2 * h - rb;
      return cMul({ re: 0, im: w_B * C.rho * Q_B2 / (4 * Math.PI * rim) }, cExpJ(-k_B2 * rim));
    });
    const abs_pr = pr.map(cAbs);
    const abs_pim = pim.map(cAbs);
    const I_B_simple = abs_pr.map((apr, idx) => (apr * apr - abs_pim[idx] * abs_pim[idx]) / (2 * C.rho_c));
    const I_B_exact = pr.map((pri, idx) => {
      const rb = r_B[idx];
      const rim = 2 * h - rb;
      const u1 = cMul(cDiv(pri, C.rho_c), { re: 1, im: -1 / (k_B2 * rb) });
      const u2 = cMul(cDiv(pim[idx], C.rho_c), { re: 1, im: -1 / (k_B2 * rim) });
      const uTot = cSub(u1, u2);
      return 0.5 * cMul(cAdd(pri, pim[idx]), cConj(uTot)).re;
    });

    // Block C: In-phase sources D_C apart — cancellation & midpoint intensity (2022 P3)
    const D_C = raw.D_C !== undefined ? Number(raw.D_C) : 4;
    const f0_C = raw.f0_C !== undefined ? Number(raw.f0_C) : 500;
    const Lp_mid = raw.Lp_mid !== undefined ? Number(raw.Lp_mid) : 80;
    const f_cancel = [0, 1, 2, 3].map(n => (2 * n + 1) * f0_C);
    const dx = C.c / (2 * f0_C);
    const x_c = D_C / 2 + dx / 2;
    const Q1_over_Q2 = x_c / (D_C - x_c);
    const p_rms_mid = C.p_ref * Math.pow(10, Lp_mid / 20);
    const p2_mid = p_rms_mid / (1 + Q1_over_Q2);
    const p1_mid = Q1_over_Q2 * p2_mid;
    const I_C = (p1_mid * p1_mid - p2_mid * p2_mid) / C.rho_c;

    // Block D: Dipole power (two antiphase sources 2h_D apart)
    const f_D = raw.f_D !== undefined ? Number(raw.f_D) : 40;
    const Q_D = raw.Q_D !== undefined ? Number(raw.Q_D) : 0.1;
    const h_D = raw.h_D !== undefined ? Number(raw.h_D) : 0.05;
    const k_D = 2 * Math.PI * f_D / C.c;
    const twoKhD = 2 * k_D * h_D;
    const W_dip = C.rho_c * k_D * k_D * Q_D * Q_D / (4 * Math.PI) * (1 - (twoKhD === 0 ? 1 : Math.sin(twoKhD) / twoKhD));
    const W_dip_small = C.rho_c * h_D * h_D * Math.pow(k_D, 4) * Q_D * Q_D / (6 * Math.PI);
    const W_mono = C.rho_c * k_D * k_D * Q_D * Q_D / (8 * Math.PI);
    const dip_vs_mono_dB = 10 * Math.log10(W_dip / W_mono);

    const steps = [
      {
        title: 'Block A — Two monopoles on the x-axis: p_rms, u_rms, I_x on the line between them (2024 P2.2)',
        latex: 'p = p_1 + p_2, \\qquad u_x = \\frac{p_1}{\\rho c}\\left(1+\\frac{1}{jkr_1}\\right) - \\frac{p_2}{\\rho c}\\left(1+\\frac{1}{jkr_2}\\right), \\qquad I_x = \\frac{1}{2}\\mathrm{Re}\\{p\\,u_x^*\\}',
        sub: `f = ${f_A} Hz, D = ${D} m, Q₁ = ${fmtComplex(Q1)}, Q₂ = ${fmtComplex(Q2)}, x = [${x.join(', ')}] m`,
        result: x.map((xi, idx) => `x=${xi}m: p_rms=${fmtFixed(p_rms_A[idx] * 1e3, 1)} mPa, u_rms=${fmtFixed(u_rms_A[idx] * 1e6, 1)} µm/s, I_x=${fmtFixed(I_A[idx] * 1e9, 1)} nW/m²`).join('  |  ')
      },
      {
        title: 'Block B — Monopole at distance h from a rigid wall: image source power & intensity (2023 P3)',
        latex: 'W_{\\mathrm{wall}} = \\frac{\\rho c k^2 |Q|^2}{8\\pi}\\left(1 + \\frac{\\sin 2kh}{2kh}\\right), \\qquad I_{\\mathrm{line}} \\approx \\frac{|p_1|^2 - |p_{\\mathrm{im}}|^2}{2\\rho c}',
        sub: `h = ${h} m; Power at f = [${f_B.join(', ')}] Hz; Line intensity at ${f_B2} Hz, d_wall = [${d_from_wall.join(', ')}] m`,
        result: `W_wall = [${W_wall.map(w => fmtFixed(w * 1e6, 1) + ' µW').join(', ')}]  |  I_simple = [${I_B_simple.map(i => fmtFixed(i * 1e6, 2) + ' µW/m²').join(', ')}] (exact: [${I_B_exact.map(i => fmtFixed(i * 1e6, 2) + ' µW/m²').join(', ')}])`
      },
      {
        title: 'Block C — In-phase sources D apart: cancellation & midpoint intensity (2022 P3)',
        latex: '\\Delta x = 2(x_c - D/2) = (2n+1)\\frac{\\lambda}{2} \\implies f_n = (2n+1)f_0, \\quad \\frac{|Q_1|}{|Q_2|} = \\frac{x_c}{D - x_c}, \\quad I_{\\mathrm{mid}} = \\frac{p_{1,\\mathrm{rms}}^2 - p_{2,\\mathrm{rms}}^2}{\\rho c}',
        sub: `D = ${D_C} m, f₀ = ${f0_C} Hz, L_p(mid) = ${Lp_mid} dB (p_rms = ${fmtNum(p_rms_mid, 3)} Pa)`,
        result: `f_cancel = [${f_cancel.join(', ')}] Hz · x_c = ${fmtFixed(x_c, 3)} m · |Q₁|/|Q₂| = ${fmtFixed(Q1_over_Q2, 3)} · I_mid = ${fmtFixed(I_C * 1e6, 2)} µW/m²`
      },
      {
        title: 'Block D — Dipole radiated power (two antiphase sources 2h_D apart)',
        latex: 'W_{\\mathrm{dip}} = \\frac{\\rho c k^2 |Q|^2}{4\\pi}\\left(1 - \\frac{\\sin 2kh_D}{2kh_D}\\right) \\approx \\frac{\\rho c h_D^2 k^4 |Q|^2}{6\\pi} \\propto f^4',
        sub: `f = ${f_D} Hz, Q = ${Q_D} m³/s, h_D = ${h_D} m`,
        result: `W_dip = ${fmtNum(W_dip, 3)} W (${fmtFixed(dip_vs_mono_dB, 1)} dB vs single monopole)`
      }
    ];

    return {
      vars: {
        rho_c: C.rho_c, p1, p2, p_tot, p_rms_A, u_tot, u_rms_A, I_A,
        k_B, kh, W_wall, W_free, gain_dB, abs_pr, abs_pim, I_B_simple, I_B_exact,
        f_cancel, dx, x_c, Q1_over_Q2, p_rms_mid, p1_mid, p2_mid, I_C,
        W_dip, W_dip_small, W_mono, dip_vs_mono_dB
      },
      highlights: [
        { label: 'A: Two Sources p_rms', value: p_rms_A.map(v => fmtFixed(v * 1e3, 1)).join(' / '), unit: 'mPa', sub: `u_rms: ${u_rms_A.map(v => fmtFixed(v * 1e6, 1)).join(' / ')} µm/s` },
        { label: 'A: Line Intensity I_x', value: I_A.map(v => fmtFixed(v * 1e9, 1)).join(' / '), unit: 'nW/m²', sub: `at x = [${x.join(', ')}] m` },
        { label: 'B: Wall Power W_wall', value: W_wall.map(v => fmtFixed(v * 1e6, 1)).join(' / '), unit: 'µW', sub: `I_line: ${I_B_simple.map(v => fmtFixed(v * 1e6, 2)).join(' / ')} µW/m²` },
        { label: 'C: Cancel x_c & Q₁/Q₂', value: `${fmtFixed(x_c, 3)} m`, unit: `Q₁/Q₂ = ${fmtFixed(Q1_over_Q2, 3)}`, sub: `I_mid = ${fmtFixed(I_C * 1e6, 2)} µW/m² · Next f = ${f_cancel[1]} Hz` }
      ],
      steps,
      warnings: [
        'DECISION: On the line between two sources, their radial velocities point in OPPOSITE x-directions, so u_x = u₁ - u₂ (minus sign!). If the two sources are in antiphase (Q₂ = -Q₁), the two minuses cancel in u_x, so velocity is non-zero at the midpoint even though p = 0!',
        'NOTE (2023 P3): Official solution uses ρ ≈ 1.18 kg/m³ (giving 32.7/36.6/54.4 µW and 0.78/2.45 µW/m²) and drops near-field cross terms in I. State both in Part 1.'
      ]
    };
  }

  // =========================================================================
  // T08: Loudspeaker driver & sealed headphone cavity
  // =========================================================================
  function solveT08(raw = {}) {
    const C = getConsts(raw);
    const Re = raw.Re !== undefined ? Number(raw.Re) : 5;
    const Bl = raw.Bl !== undefined ? Number(raw.Bl) : 2;
    const M = raw.M !== undefined ? Number(raw.M) : 10e-3;
    const K = raw.K !== undefined ? Number(raw.K) : 1500;
    const Rt = raw.Rt !== undefined ? Number(raw.Rt) : 2.5;
    const a = raw.a !== undefined ? Number(raw.a) : 0.06;
    const e_rms = raw.e_rms !== undefined ? Number(raw.e_rms) : 4;
    const f = raw.f !== undefined ? Number(raw.f) : 200;
    const r = raw.r !== undefined ? Number(raw.r) : 5;
    const Omega = raw.Omega !== undefined ? Number(raw.Omega) : 2 * Math.PI;
    const theta = raw.theta !== undefined ? Number(raw.theta) : 30;
    const V_box = raw.V_box !== undefined ? Number(raw.V_box) : 20e-3;

    const S = Math.PI * a * a;
    const w = 2 * Math.PI * f;
    const k = w / C.c;
    const ka = k * a;
    const e_hat = Math.SQRT2 * e_rms;

    const Z_M = { re: Rt, im: w * M - K / w };
    const f_s = Math.sqrt(K / M) / (2 * Math.PI);
    const Q_t = Math.sqrt(K * M) / Rt;

    const F = Bl * e_hat / Re;
    const U = cDiv(F, Z_M);
    const Q = cMul(S, U);
    const Q_amp = cAbs(Q);

    const p_amp = C.rho * w * Q_amp / (Omega * r);
    const Lp = 20 * Math.log10((p_amp / Math.SQRT2) / C.p_ref);
    const W = Omega * r * r * (p_amp * p_amp) / (2 * C.rho_c);
    const LW = 10 * Math.log10(W / C.W_ref);
    const W_check = C.rho_c * k * k * Q_amp * Q_amp / (2 * Omega);

    const x_amp_mm = (cAbs(U) / w) * 1e3;
    const p_mass_ctrl = C.rho * S * Bl * e_hat / (Omega * r * Re * M);
    const Lp_mass_ctrl = 20 * Math.log10((p_mass_ctrl / Math.SQRT2) / C.p_ref);

    const Z_e = cAdd(Re, cDiv(Bl * Bl, Z_M));
    const Z_e_at_fs = Re + (Bl * Bl) / Rt;
    const R_electrical = (Bl * Bl) / Re;

    // Piston directivity
    const sinTheta = Math.sin(theta * Math.PI / 180);
    const xD = ka * sinTheta;
    const dirRatio = xD === 0 ? 1 : Math.abs(2 * besselJ1(xD) / xD);
    const D_dB = 20 * Math.log10(dirRatio);
    const f_minus3dB = sinTheta > 0 ? 1.62 * C.c / (2 * Math.PI * a * sinTheta) : Infinity;
    const f_first_null = sinTheta > 0 ? 3.83 * C.c / (2 * Math.PI * a * sinTheta) : Infinity;

    // Closed box
    const K_box = C.rho * C.c * C.c * S * S / V_box;
    const f_c_box = Math.sqrt((K + K_box) / M) / (2 * Math.PI);

    // Block F: Week 8 P3 check
    const S_F = Math.PI * 0.06 * 0.06;
    const e_F = 2.8 * Math.SQRT2;
    const w300 = 2 * Math.PI * 300;
    const w30 = 2 * Math.PI * 30;
    const Lp300_massctrl = 20 * Math.log10((C.rho * S_F * 8 * e_F / (2 * Math.PI * 2 * 5 * 0.020)) / Math.SQRT2 / C.p_ref);
    const Z30_abs = Math.hypot(18, w30 * 0.020 - 2000 / w30);
    const Z300_abs = Math.hypot(18, w300 * 0.020 - 2000 / w300);
    const Lp30_full = 20 * Math.log10((C.rho * w30 * S_F * 8 * e_F / (5 * Z30_abs) / (2 * Math.PI * 2)) / Math.SQRT2 / C.p_ref);
    const Lp300_full = 20 * Math.log10((C.rho * w300 * S_F * 8 * e_F / (5 * Z300_abs) / (2 * Math.PI * 2)) / Math.SQRT2 / C.p_ref);

    // Block G: Sealed headphone cavity (Week 8 P4)
    const V_cav = raw.V_cav !== undefined ? Number(raw.V_cav) : 50e-6;
    const L_cav = raw.L_cav !== undefined ? Number(raw.L_cav) : 100;
    const f_G = raw.f_G !== undefined ? Number(raw.f_G) : 100;
    const r_G = raw.r_G !== undefined ? Number(raw.r_G) : 0.5;
    const C_A = V_cav / (C.rho * C.c * C.c);
    const p_cav = C.p_ref * Math.pow(10, L_cav / 20);
    const Q_G = 2 * Math.PI * f_G * C_A * p_cav;
    const Lp_free = 20 * Math.log10((C.rho * 2 * Math.PI * f_G * Q_G / (4 * Math.PI * r_G)) / C.p_ref);

    const steps = [
      {
        title: 'Step 1 & 2 — Piston area S, ka, and mechanical impedance Z_M (2022 P1)',
        latex: 'S = \\pi a^2, \\quad \\hat{e} = \\sqrt{2}\\,e_{\\mathrm{rms}}, \\quad Z_M = R_t + j\\left(\\omega M - \\frac{K}{\\omega}\\right), \\quad f_s = \\frac{1}{2\\pi}\\sqrt{\\frac{K}{M}}',
        sub: `a = ${a} m → S = ${fmtNum(S, 4)} m², ka = ${fmtFixed(ka, 3)} (< 1 → omnidirectional); e_rms = ${e_rms} V → ê = ${fmtNum(e_hat, 4)} V`,
        result: `Z_M = ${fmtComplex(Z_M, 4)} N·s/m (|Z_M| = ${fmtNum(cAbs(Z_M), 4)} N·s/m, f_s = ${fmtFixed(f_s, 1)} Hz, Q_t = ${fmtFixed(Q_t, 2)})`
      },
      {
        title: 'Step 3 — Driving force F, cone velocity U, and volume velocity Q',
        latex: 'F = Bl\\frac{\\hat{e}}{R_e}, \\qquad U = \\frac{F}{Z_M}, \\qquad |Q| = S|U| = \\frac{S\\,Bl\\,\\hat{e}}{R_e|Z_M|}',
        sub: `F = ${Bl} × ${fmtNum(e_hat, 4)} / ${Re} = ${fmtNum(F, 4)} N`,
        result: `|Q| = ${fmtNum(Q_amp, 4)} m³/s (excursion |x| = |U|/ω = ${fmtFixed(x_amp_mm, 3)} mm)`
      },
      {
        title: `Step 4 & 5 — Far-field pressure |p(r)| and radiated acoustic power W (Ω = ${Math.abs(Omega - 2 * Math.PI) < 0.01 ? '2π baffle' : '4π free box'})`,
        latex: '|p(r)| = \\frac{\\rho\\omega |Q|}{\\Omega r}, \\qquad W = \\Omega r^2 \\frac{|p(r)|^2}{2\\rho c}',
        sub: `r = ${r} m, ω = ${fmtNum(w, 4)} rad/s`,
        result: `|p(${r} m)| = ${fmtFixed(p_amp, 3)} Pa (${fmtFixed(Lp, 1)} dB SPL)  |  W = ${fmtFixed(W * 1e3, 2)} mW (L_W = ${fmtFixed(LW, 1)} dB)`
      },
      {
        title: 'Step 7–10 — Mass-controlled limit (f ≫ f_s), closed box f_c, and headphone cavity (Block G)',
        latex: '|p|_{\\mathrm{mass}} = \\frac{\\rho S\\,Bl\\,\\hat{e}}{\\Omega r R_e M}, \\qquad K_{\\mathrm{box}} = \\frac{\\rho c^2 S^2}{V_{\\mathrm{box}}}, \\qquad C_A = \\frac{V_{\\mathrm{cav}}}{\\rho c^2}, \\quad |Q| = \\omega C_A p_{\\mathrm{cav}}',
        sub: `Mass-ctrl: |p|=${fmtFixed(p_mass_ctrl, 3)} Pa (${fmtFixed(Lp_mass_ctrl, 2)} dB); Box f_c=${fmtFixed(f_c_box, 1)} Hz; Headphone off-ear (${r_G}m):`,
        result: `Headphone free-field L_p = ${fmtFixed(Lp_free, 2)} dB (from ${L_cav} dB in ${V_cav * 1e6} cm³ cavity)`
      }
    ];

    return {
      vars: {
        rho_c: C.rho_c, S, w, k, ka, e_hat, Z_M, f_s, Q_t, F, U, Q, Q_amp,
        p_amp, Lp, W, LW, W_check, x_amp_mm, p_mass_ctrl, Z_e, Z_e_at_fs, R_electrical,
        D_dB, f_minus3dB, f_first_null, K_box, f_c_box,
        Lp300_massctrl, Lp30_full, Lp300_full, C_A, p_cav, Q_G, Lp_free
      },
      highlights: [
        { label: 'Volume Velocity |Q|', value: fmtNum(Q_amp, 3), unit: 'm³/s (peak)', sub: `|Z_M| = ${fmtFixed(cAbs(Z_M), 2)} Ns/m · f_s = ${fmtFixed(f_s, 1)} Hz` },
        { label: `Pressure |p(${r}m)|`, value: fmtFixed(p_amp, 3), unit: 'Pa (peak)', sub: `L_p = ${fmtFixed(Lp, 1)} dB · Mass-ctrl: ${fmtFixed(Lp_mass_ctrl, 2)} dB` },
        { label: 'Radiated Power W', value: fmtFixed(W * 1e3, 2), unit: 'mW', sub: `L_W = ${fmtFixed(LW, 1)} dB · ka = ${fmtFixed(ka, 2)}` },
        { label: 'G: Headphone Free-Field', value: fmtFixed(Lp_free, 2), unit: 'dB SPL', sub: `at ${r_G} m (was ${L_cav} dB in ${V_cav * 1e6} cm³ ear)` }
      ],
      steps,
      warnings: [
        'DECISION: Drive voltage on exam sheets is RMS unless "amplitude" is written. Multiply e_rms by √2 to get peak ê when computing peak |Q| and peak |p|.',
        'DECISION: Infinite baffle = 2πr and 2πr². Small closed box in free space = 4πr and 4πr².',
        'NOTE: "Total damping coefficient R_t" already includes electrical damping (Bl)²/R_e. State this assumption in one sentence.'
      ]
    };
  }

  // =========================================================================
  // T09: Room modes of a rectangular room
  // =========================================================================
  function solveT09(raw = {}) {
    const C = getConsts(raw);
    const lx = raw.lx !== undefined ? Number(raw.lx) : 5;
    const ly = raw.ly !== undefined ? Number(raw.ly) : 4;
    const lz = raw.lz !== undefined ? Number(raw.lz) : 3;
    const f_max = raw.f_max !== undefined ? Number(raw.f_max) : 80;
    const n_max = raw.n_max !== undefined ? Number(raw.n_max) : 6;
    const fc_band = raw.fc_band !== undefined ? Number(raw.fc_band) : 50;
    const n_oct_band = raw.n_oct_band !== undefined ? Number(raw.n_oct_band) : 3; // 3 = third-octave
    const T_room = raw.T_room !== undefined ? Number(raw.T_room) : 0.5;

    const modeList = [];
    for (let nx = 0; nx <= n_max; nx++) {
      for (let ny = 0; ny <= n_max; ny++) {
        for (let nz = 0; nz <= n_max; nz++) {
          if (nx === 0 && ny === 0 && nz === 0) continue;
          const f = (C.c / 2) * Math.sqrt(Math.pow(nx / lx, 2) + Math.pow(ny / ly, 2) + Math.pow(nz / lz, 2));
          if (f > 0 && f < f_max) {
            const typeNum = (nx > 0 ? 1 : 0) + (ny > 0 ? 1 : 0) + (nz > 0 ? 1 : 0);
            const typeName = typeNum === 1 ? 'Axial' : (typeNum === 2 ? 'Tangential' : 'Oblique');
            const centreAudible = (nx % 2 === 0) && (ny % 2 === 0) && (nz % 2 === 0);
            modeList.push({ nx, ny, nz, f, fRound: Math.round(f * 10) / 10, typeNum, typeName, centreAudible });
          }
        }
      }
    }
    modeList.sort((a, b) => a.f - b.f);

    const n_modes_below = modeList.length;
    const f_100 = C.c / (2 * lx);
    const f_010 = C.c / (2 * ly);
    const f_001 = C.c / (2 * lz);

    const bandFactor = Math.pow(2, 1 / (2 * n_oct_band));
    const band = [fc_band / bandFactor, fc_band * bandFactor];
    const in_band = modeList.filter(m => m.fRound >= band[0] && m.fRound < band[1]);
    const centre_audible = modeList.filter(m => m.centreAudible);

    const V = lx * ly * lz;
    const S_tot = 2 * (lx * ly + lx * lz + ly * lz);
    const L_edges = 4 * (lx + ly + lz);
    const N_est = (4 * Math.PI * V / 3) * Math.pow(f_max / C.c, 3)
      + (Math.PI * S_tot / 4) * Math.pow(f_max / C.c, 2)
      + (L_edges / 8) * (f_max / C.c);
    const dNdf = 4 * Math.PI * V * f_max * f_max / Math.pow(C.c, 3);
    const f_Schroeder = 2000 * Math.sqrt(T_room / V);

    // Block C: Dimension from two known modes (2022 MC4)
    const f_mode1 = raw.f_mode1 !== undefined ? Number(raw.f_mode1) : 10; // f(0,1,0)
    const f_mode2 = raw.f_mode2 !== undefined ? Number(raw.f_mode2) : 45; // f(0,2,1)
    const ny2_C = raw.ny2_C !== undefined ? Number(raw.ny2_C) : 2;
    const nz2_C = raw.nz2_C !== undefined ? Number(raw.nz2_C) : 1;
    const ly_C = C.c / (2 * f_mode1);
    const lz_C = nz2_C / Math.sqrt(Math.pow(2 * f_mode2 / C.c, 2) - Math.pow(ny2_C / ly_C, 2));

    // Block D: 2023 MC3 (7.2 x 5.4 x 3, 50 Hz 1/3-octave)
    const modes_2023 = [2, 0, 0, (C.c / 2) * (2 / 7.2)];

    const steps = [
      {
        title: `Step 1 & 2 — Natural frequencies below ${f_max} Hz in ${lx} × ${ly} × ${lz} m room`,
        latex: 'f_{n_x,n_y,n_z} = \\frac{c}{2}\\sqrt{\\left(\\frac{n_x}{l_x}\\right)^2 + \\left(\\frac{n_y}{l_y}\\right)^2 + \\left(\\frac{n_z}{l_z}\\right)^2}',
        sub: `Lowest axial modes: f₁₀₀ = ${fmtFixed(f_100, 1)} Hz, f₀₁₀ = ${fmtFixed(f_010, 1)} Hz, f₀₀₁ = ${fmtFixed(f_001, 1)} Hz`,
        result: `${n_modes_below} modes below ${f_max} Hz: ` + modeList.slice(0, 12).map(m => `(${m.nx},${m.ny},${m.nz})=${fmtFixed(m.f, 1)}Hz [${m.typeName[0]}]`).join(', ')
      },
      {
        title: `Step 3 & 4 — Centre-audible modes & modes inside the ${fc_band} Hz (1/${n_oct_band}-octave) band`,
        latex: '\\text{Centre max: all } (n_x,n_y,n_z) \\text{ even}; \\qquad f \\in [f_c 2^{-1/(2n)},\\, f_c 2^{+1/(2n)})',
        sub: `Band [${fmtFixed(band[0], 1)}–${fmtFixed(band[1], 1)} Hz]`,
        result: `In ${fc_band} Hz band: ${in_band.length ? in_band.map(m => `(${m.nx},${m.ny},${m.nz}) at ${fmtFixed(m.f, 1)} Hz`).join(', ') : 'none'}  |  Heard at room centre: ${centre_audible.length ? centre_audible.map(m => `(${m.nx},${m.ny},${m.nz}) at ${fmtFixed(m.f, 1)} Hz`).join(', ') : 'none'}`
      },
      {
        title: 'Step 5 & Block C — Mode count estimate, Schroeder frequency & dimension from modes (2022 MC4)',
        latex: 'N(f) \\approx \\frac{4\\pi V}{3}\\left(\\frac{f}{c}\\right)^3 + \\frac{\\pi S}{4}\\left(\\frac{f}{c}\\right)^2 + \\frac{L}{8}\\frac{f}{c}, \\qquad f_S \\approx 2000\\sqrt{\\frac{T}{V}}, \\qquad \\frac{n_z}{l_z} = \\sqrt{\\left(\\frac{2f}{c}\\right)^2 - \\left(\\frac{n_y}{l_y}\\right)^2}',
        sub: `V = ${V} m³, S = ${S_tot} m², L = ${L_edges} m; Block C: f(0,1,0)=${f_mode1} Hz → l_y=${fmtFixed(ly_C, 2)} m, f(0,${ny2_C},${nz2_C})=${f_mode2} Hz`,
        result: `N_est(${f_max} Hz) = ${fmtFixed(N_est, 1)} · f_Schroeder = ${fmtFixed(f_Schroeder, 0)} Hz · Block C: l_z = ${fmtFixed(lz_C, 2)} m (nearest option: 4 m)`
      }
    ];

    return {
      vars: {
        modeList, n_modes_below, f_100, f_010, f_001, centre_audible, in_band,
        V, S_tot, L_edges, N_est, dNdf, f_Schroeder, ly_C, lz_C, modes_2023
      },
      highlights: [
        { label: `Modes < ${f_max} Hz`, value: String(n_modes_below), unit: 'modes', sub: `f₁₀₀ = ${fmtFixed(f_100, 1)} Hz · N_est = ${fmtFixed(N_est, 1)}` },
        { label: `In ${fc_band} Hz Band`, value: in_band.length ? in_band.map(m => `(${m.nx},${m.ny},${m.nz})`).join(', ') : 'None', unit: in_band.length ? `${fmtFixed(in_band[0].f, 1)} Hz` : '', sub: `Band: ${fmtFixed(band[0], 1)}–${fmtFixed(band[1], 1)} Hz` },
        { label: 'Audible at Centre', value: centre_audible.length ? centre_audible.map(m => `(${m.nx},${m.ny},${m.nz})`).join(', ') : 'None', unit: 'all-even', sub: 'Every mode is maximal in a corner' },
        { label: 'Block C: Height l_z', value: fmtFixed(lz_C, 2), unit: 'm', sub: `from f₀₁₀=${f_mode1} Hz (l_y=${fmtFixed(ly_C, 2)}m), f=${f_mode2} Hz` }
      ],
      steps,
      warnings: [
        'DECISION: Any odd mode index (1, 3, 5…) has cos(nπ/2) = 0 = a pressure NODE at the centre of the room. Only modes with ALL EVEN indices (e.g. (2,0,0)) are heard at the centre! Every mode has an antinode (maximum) in the corners.'
      ]
    };
  }

  // =========================================================================
  // T10: Reverberation time, diffuse-field level, ISO 354
  // =========================================================================
  function solveT10(raw = {}) {
    const C = getConsts(raw);

    // Block A: Room dimensions, Sabine & Eyring (2022 MC5)
    const lx = raw.lx !== undefined ? Number(raw.lx) : 10;
    const ly = raw.ly !== undefined ? Number(raw.ly) : 13;
    const lz = raw.lz !== undefined ? Number(raw.lz) : 8;
    const alpha_ceiling = raw.alpha_ceiling !== undefined ? Number(raw.alpha_ceiling) : 0.8;
    const alpha_rest = raw.alpha_rest !== undefined ? Number(raw.alpha_rest) : 0;

    const V = lx * ly * lz;
    const S_floor = lx * ly;
    const S_walls = 2 * (lx + ly) * lz;
    const S = 2 * S_floor + S_walls;
    const A = S_floor * alpha_ceiling + (S_floor + S_walls) * alpha_rest;
    const alpha_mean = A / S;
    const T_sabine = 55.3 * V / (C.c * A);
    const T_eyring = 55.3 * V / (-C.c * S * Math.log(1 - alpha_mean));
    const T_ceiling_rule = 0.16 * lz / alpha_ceiling;

    // Block B: Unknown alpha of remaining surfaces (2023 MC5 & 2024 MC4)
    const lx_B = raw.lx_B !== undefined ? Number(raw.lx_B) : 6;
    const ly_B = raw.ly_B !== undefined ? Number(raw.ly_B) : 7;
    const lz_B = raw.lz_B !== undefined ? Number(raw.lz_B) : 3;
    const alpha_known_B = raw.alpha_known_B !== undefined ? Number(raw.alpha_known_B) : 0.8;
    const T_meas_B = raw.T_meas_B !== undefined ? Number(raw.T_meas_B) : 0.44;
    const V_B = lx_B * ly_B * lz_B;
    const S_known_B = lx_B * ly_B;
    const S_rest_B = lx_B * ly_B + 2 * (lx_B + ly_B) * lz_B;
    const A_B = 0.16 * V_B / T_meas_B;
    const alpha_walls_B = (A_B - S_known_B * alpha_known_B) / S_rest_B;

    // 2024 MC4 preset check
    const V_B2 = 5 * 8 * 3;
    const S_floor_B2 = 5 * 8;
    const S_rest_B2 = 5 * 8 + 2 * (5 + 8) * 3;
    const A_B2 = 0.16 * V_B2 / 0.4;
    const alpha_needed_B2 = (A_B2 - S_floor_B2 * 0.1) / S_rest_B2;

    // Block C: Steady-state SPL from L_W: direct + reverberant (2023 MC7)
    const LW_C = raw.LW_C !== undefined ? Number(raw.LW_C) : 75;
    const V_C = raw.V_C !== undefined ? Number(raw.V_C) : 200;
    const T_C = raw.T_C !== undefined ? Number(raw.T_C) : 1;
    const Qdir = raw.Qdir !== undefined ? Number(raw.Qdir) : 1;
    const src = parseNumberList(raw.src !== undefined ? raw.src : [1, 1, 1.7]);
    const rec = parseNumberList(raw.rec !== undefined ? raw.rec : [3, 8, 1.2]);
    const r_C = raw.r_C_direct !== undefined && raw.r_C_direct !== ''
      ? Number(raw.r_C_direct)
      : Math.hypot((rec[0] || 0) - (src[0] || 0), (rec[1] || 0) - (src[1] || 0), (rec[2] || 0) - (src[2] || 0));
    const A_C = 0.16 * V_C / T_C;
    const Lp_C = LW_C + 10 * Math.log10(Qdir / (4 * Math.PI * r_C * r_C) + 4 / A_C);
    const Lp_rev_only = LW_C + 10 * Math.log10(4 / A_C);
    const r_rev = Math.sqrt(Qdir * A_C / (16 * Math.PI));

    // Block D: Source power -> room pressure & on/off Leq (Week 6 P3)
    const W_D = raw.W_D !== undefined ? Number(raw.W_D) : 10e-3;
    const V_D = raw.V_D !== undefined ? Number(raw.V_D) : 210;
    const T_D = raw.T_D !== undefined ? Number(raw.T_D) : 3.1;
    const duty_D = raw.duty_D !== undefined ? Number(raw.duty_D) : 5 / 15;
    const A_D = 55.3 * V_D / (C.c * T_D);
    const p2_on = 4 * W_D * C.rho_c / A_D;
    const p_on = Math.sqrt(p2_on);
    const Leq_D = 10 * Math.log10(p2_on * duty_D / (C.p_ref * C.p_ref));
    const W_D2 = Math.pow(C.p_ref * Math.pow(10, 70 / 20), 2) / C.rho_c * 4 * Math.PI * 16;
    const Leq_total_D = 10 * Math.log10((p2_on * duty_D + 4 * W_D2 * C.rho_c / A_D) / (C.p_ref * C.p_ref));

    // Block E: ISO 354 reverberation room (2022 MC7)
    const V_E = raw.V_E !== undefined ? Number(raw.V_E) : 150;
    const S_E = raw.S_E !== undefined ? Number(raw.S_E) : 9;
    const T1 = raw.T1 !== undefined ? Number(raw.T1) : 5;
    const T2 = raw.T2 !== undefined ? Number(raw.T2) : 2;
    const alpha_E = (0.16 * V_E / S_E) * (1 / T2 - 1 / T1);

    // Block F: Design absorber area for target T (Week 7 P1)
    const V_F = 300, T_now = 3.1, T_target = 0.8, A_people = 40 * 0.42;
    const alpha_F = (0.16 * 200 / 10) * (1 / 3.0 - 1 / 5.2);
    const S_needed = (0.16 * V_F / T_target - 0.16 * V_F / T_now - A_people) / alpha_F;

    // Slide 30 check
    const A_s30 = 200 * 0.8 + 500 * 0.1;
    const T_s30_sabine = 55.3 * 1000 / (C.c * A_s30);
    const T_s30_eyring = 55.3 * 1000 / (-C.c * 700 * Math.log(1 - A_s30 / 700));

    const steps = [
      {
        title: 'Block A — Sabine and Eyring reverberation times (2022 MC5)',
        latex: 'A = \\sum_i S_i\\alpha_i, \\quad \\bar{\\alpha} = \\frac{A}{S}, \\quad T_{\\mathrm{Sabine}} = \\frac{55.3\\,V}{c\\,A} \\approx \\frac{0.16\\,V}{A}, \\quad T_{\\mathrm{Eyring}} = \\frac{55.3\\,V}{-c\\,S\\ln(1-\\bar{\\alpha})}',
        sub: `V = ${V} m³, S_floor = ${S_floor} m², S_total = ${S} m², A = ${fmtFixed(A, 2)} m² (ᾱ = ${fmtFixed(alpha_mean, 3)})`,
        result: `T_Sabine = ${fmtFixed(T_sabine, 2)} s  |  T_Eyring = ${fmtFixed(T_eyring, 2)} s`
      },
      {
        title: 'Block B — Unknown α of remaining surfaces for a target/measured T (2023 MC5 & 2024 MC4)',
        latex: 'A = \\frac{0.16\\,V}{T}, \\qquad \\alpha_{\\mathrm{rest}} = \\frac{A - S_{\\mathrm{known}}\\alpha_{\\mathrm{known}}}{S_{\\mathrm{rest}}}',
        sub: `V_B = ${V_B} m³, T = ${T_meas_B} s → A = ${fmtFixed(A_B, 2)} m²; S_known = ${S_known_B} m² (α=${alpha_known_B}), S_rest = ${S_rest_B} m²`,
        result: `α_rest = ${fmtFixed(alpha_walls_B, 3)} (2024 MC4 studio preset: α = ${fmtFixed(alpha_needed_B2, 2)} → option 0.4)`
      },
      {
        title: 'Block C — Steady-state SPL from L_W: direct + reverberant field (2023 MC7)',
        latex: 'L_p = L_W + 10\\log_{10}\\left(\\frac{Q}{4\\pi r^2} + \\frac{4}{A}\\right), \\qquad r_{\\mathrm{rev}} = \\sqrt{\\frac{Q\\,A}{16\\pi}} \\approx 0.14\\sqrt{Q\\,A}',
        sub: `L_W = ${LW_C} dB, V = ${V_C} m³, T = ${T_C} s → A = ${fmtFixed(A_C, 1)} m², r = ${fmtFixed(r_C, 2)} m (r_rev = ${fmtFixed(r_rev, 2)} m)`,
        result: `L_p = ${fmtFixed(Lp_C, 1)} dB (reverberant alone: ${fmtFixed(Lp_rev_only, 1)} dB)`
      },
      {
        title: 'Block D & E — Diffuse pressure from W (Week 6 P3) & ISO 354 absorption (2022 MC7)',
        latex: 'p_{\\mathrm{rms}}^2 = \\frac{4W\\rho c}{A}, \\qquad \\alpha_{\\mathrm{ISO\\,354}} = \\frac{0.16\\,V}{S_{\\mathrm{sample}}}\\left(\\frac{1}{T_2} - \\frac{1}{T_1}\\right)',
        sub: `Block D: W=${W_D * 1e3} mW, A=${fmtFixed(A_D, 2)} m²; Block E: V=${V_E} m³, S=${S_E} m², T₁=${T1} s → T₂=${T2} s`,
        result: `Block D: p_rms = ${fmtFixed(p_on, 2)} Pa, Leq = ${fmtFixed(Leq_D, 1)} dB (2 sources: ${fmtFixed(Leq_total_D, 1)} dB)  |  ISO 354: α = ${fmtFixed(alpha_E, 2)}`
      }
    ];

    return {
      vars: {
        rho_c: C.rho_c, V, S_floor, S_walls, S, A, alpha_mean, T_sabine, T_eyring, T_ceiling_rule,
        A_B, alpha_walls_B, alpha_needed_B2, r_C, A_C, Lp_C, r_rev,
        A_D, p2_on, p_on, Leq_D, W_D2, Leq_total_D, alpha_E, alpha_F, S_needed, T_s30_sabine, T_s30_eyring
      },
      highlights: [
        { label: 'A: Sabine T (Eyring)', value: fmtFixed(T_sabine, 2), unit: `s (${fmtFixed(T_eyring, 2)} s)`, sub: `A = ${fmtFixed(A, 1)} m² · ᾱ = ${fmtFixed(alpha_mean, 2)}` },
        { label: 'B: Unknown Surface α', value: fmtFixed(alpha_walls_B, 2), unit: '', sub: `A = ${fmtFixed(A_B, 1)} m² over S_rest = ${S_rest_B} m²` },
        { label: 'C: Room SPL from L_W', value: fmtFixed(Lp_C, 1), unit: 'dB SPL', sub: `r = ${fmtFixed(r_C, 2)} m · r_rev = ${fmtFixed(r_rev, 2)} m` },
        { label: 'E: ISO 354 Sample α', value: fmtFixed(alpha_E, 2), unit: '', sub: `V=${V_E} m³, S=${S_E} m², T: ${T1}s → ${T2}s` }
      ],
      steps,
      warnings: [
        'DECISION: Use Sabine for ᾱ < 0.3; use Eyring when ᾱ > 0.3 or "high absorption" is specified. Eyring always gives a shorter T.',
        'TRAP (2023 MC5, 2024 MC4): Subtract the known surface absorption S_known·α_known from A, then divide by the REMAINING area S_rest (never the total room area S!).',
        'TRAP (2022 MC7): The absorber thickness (1 cm) in the ISO 354 question is a pure distractor.'
      ]
    };
  }

  // =========================================================================
  // T11: Absorbers: membrane, Helmholtz, perforated panel, porous, Z -> alpha
  // =========================================================================
  function solveT11(raw = {}) {
    const C = getConsts(raw);

    // Block A: Membrane absorber
    const m_panel = raw.m_panel !== undefined ? Number(raw.m_panel) : 600 * 0.020; // 12 kg/m^2
    const L_cav = raw.L_cav !== undefined ? Number(raw.L_cav) : 0.050;
    const f_membrane = (1 / (2 * Math.PI)) * Math.sqrt(C.rho_c2 / (m_panel * L_cav));
    const f_rule = 60 / Math.sqrt(m_panel * L_cav);

    // 2023 MC6 & 2024 MC7 reverse depth
    const m_A2 = raw.m_A2 !== undefined ? Number(raw.m_A2) : 2.1;
    const L_A2 = raw.L_A2 !== undefined ? Number(raw.L_A2) : 0.1;
    const f_A2 = (1 / (2 * Math.PI)) * Math.sqrt(C.rho_c2 / (m_A2 * L_A2));

    const f_A3 = raw.f_A3 !== undefined ? Number(raw.f_A3) : 350;
    const m_A3 = raw.m_A3 !== undefined ? Number(raw.m_A3) : 0.2;
    const L_A3 = C.rho_c2 / (m_A3 * Math.pow(2 * Math.PI * f_A3, 2));

    // Block B: Helmholtz resonator
    const V_B = raw.V_B !== undefined ? Number(raw.V_B) : 400e-6;
    const d_B = raw.d_B !== undefined ? Number(raw.d_B) : 0.020;
    const l_eff_B = raw.l_eff_B !== undefined ? Number(raw.l_eff_B) : 0.021;
    const s_B = Math.PI * d_B * d_B / 4;
    const f_helmholtz = (C.c / (2 * Math.PI)) * Math.sqrt(s_B / (V_B * l_eff_B));

    // 2024 MC6 reverse volume
    const f_B2 = raw.f_B2 !== undefined ? Number(raw.f_B2) : 140;
    const d_B2 = raw.d_B2 !== undefined ? Number(raw.d_B2) : 0.05;
    const l_B2 = raw.l_B2 !== undefined ? Number(raw.l_B2) : 0.02;
    const s_B2 = Math.PI * d_B2 * d_B2 / 4;
    const V_B2 = (s_B2 / l_B2) * Math.pow(C.c / (2 * Math.PI * f_B2), 2);

    // Block C: Perforated panel absorber
    const d_C = raw.d_C !== undefined ? Number(raw.d_C) : 0.010;
    const a_C = raw.a_C !== undefined ? Number(raw.a_C) : 0.030;
    const l_C = raw.l_C !== undefined ? Number(raw.l_C) : 0.020;
    const L_C = raw.L_C !== undefined ? Number(raw.L_C) : 0.050;
    const P_C = Math.PI * d_C * d_C / (4 * a_C * a_C);
    const delta_C = 0.8 * d_C;
    const f_perf = (C.c / (2 * Math.PI)) * Math.sqrt(P_C / (L_C * (l_C + delta_C)));

    // Block D: Porous absorber lambda/4
    const d_D = raw.d_D !== undefined ? Number(raw.d_D) : 0.07;
    const f_quarter = C.c / (4 * d_D);
    const f_half_dip = C.c / (2 * d_D);

    // Block E: alpha from surface impedance Z (normal, oblique, random/Paris)
    const Z = parseComplexToken(raw.Z !== undefined ? raw.Z : '500+1000j');
    const z0 = raw.z0 !== undefined ? Number(raw.z0) : 414;
    const theta = raw.theta !== undefined ? Number(raw.theta) : 45;
    const R_n = cDiv(cSub(Z, z0), cAdd(Z, z0));
    const alpha_n = 1 - Math.pow(cAbs(R_n), 2);
    const cosTh = Math.cos(theta * Math.PI / 180);
    const R_theta = cDiv(cSub(cMul(Z, cosTh), z0), cAdd(cMul(Z, cosTh), z0));
    const alpha_theta = 1 - Math.pow(cAbs(R_theta), 2);

    const zeta = cDiv(Z, z0);
    const r = zeta.re, x = zeta.im;
    let alpha_r;
    if (Math.abs(x) > 1e-9) {
      const r2x2 = r * r + x * x;
      alpha_r = (8 * r / r2x2) * (
        1
        - (r / r2x2) * Math.log((r + 1) * (r + 1) + x * x)
        + ((r * r - x * x) / (x * r2x2)) * Math.atan(x / (r + 1))
      );
    } else {
      // Real impedance closed form
      alpha_r = (8 / r) * (1 + 1 / (1 + r) - (2 / r) * Math.log(1 + r));
    }

    // Block F: 2022 MC6
    const Z_F = [1, 100, 1000, 10000];
    const alpha_F = Z_F.map(zf => 1 - Math.pow((zf - C.rho_c) / (zf + C.rho_c), 2));

    const steps = [
      {
        title: 'Block A — Membrane (panel) absorber resonance & reverse cavity depth (Week 7 P2.1, 2023 MC6, 2024 MC7)',
        latex: 'f_r = \\frac{1}{2\\pi}\\sqrt{\\frac{\\rho c^2}{m\\,L}} \\approx \\frac{60}{\\sqrt{m\\,L}}, \\qquad L = \\frac{\\rho c^2}{m(2\\pi f_r)^2}',
        sub: `A1: m=${m_panel} kg/m², L=${L_cav} m;  A2 (2023 MC6): m=${m_A2} kg/m², L=${L_A2} m;  A3 (2024 MC7): f=${f_A3} Hz, m=${m_A3} kg/m²`,
        result: `f_membrane = ${fmtFixed(f_membrane, 1)} Hz  |  f_A2 = ${fmtFixed(f_A2, 1)} Hz  |  Depth L_A3 = ${fmtFixed(L_A3 * 100, 1)} cm (${fmtFixed(L_A3, 3)} m)`
      },
      {
        title: 'Block B — Helmholtz resonator frequency & reverse cavity volume (Week 4 P1, 2024 MC6)',
        latex: 'f_0 = \\frac{c}{2\\pi}\\sqrt{\\frac{s}{V\\,l_{\\mathrm{eff}}}}, \\qquad s = \\frac{\\pi d^2}{4}, \\qquad V = \\frac{s}{l_{\\mathrm{eff}}}\\left(\\frac{c}{2\\pi f_0}\\right)^2',
        sub: `B1: V=${V_B * 1e6} cm³, d=${d_B * 100} cm, l_eff=${l_eff_B * 100} cm;  B2 (2024 MC6): f₀=${f_B2} Hz, d=${d_B2 * 100} cm, l=${l_B2 * 100} cm`,
        result: `f_Helmholtz = ${fmtFixed(f_helmholtz, 1)} Hz  |  Volume V_B2 = ${fmtFixed(V_B2, 4)} m³ (option 0.015 m³)`
      },
      {
        title: 'Block C & D — Perforated panel (Week 7 P2.2) & porous λ/4 frequency',
        latex: 'f_{\\mathrm{perf}} = \\frac{c}{2\\pi}\\sqrt{\\frac{P}{L(l + 0.8d)}}, \\quad P = \\frac{\\pi d^2}{4a^2}, \\qquad f_{\\lambda/4} = \\frac{c}{4d_{\\mathrm{wall}}}',
        sub: `Perforation P = ${fmtFixed(P_C * 100, 2)}% (fraction ${fmtFixed(P_C, 4)}), L = ${L_C} m, l = ${l_C} m; Porous d = ${d_D} m`,
        result: `f_perf = ${fmtFixed(f_perf, 1)} Hz  |  Porous λ/4 peak = ${fmtFixed(f_quarter, 0)} Hz (λ/2 dip at ${fmtFixed(f_half_dip, 0)} Hz)`
      },
      {
        title: 'Block E & F — Absorption α from surface impedance Z (normal, oblique, Paris random incidence)',
        latex: '\\zeta = \\frac{Z}{\\rho c} = r + jx, \\qquad \\alpha_n = 1 - \\left|\\frac{\\zeta - 1}{\\zeta + 1}\\right|^2, \\qquad \\alpha_r = \\int_0^{\\pi/2}\\alpha(\\theta)\\sin 2\\theta\\,d\\theta',
        sub: `Z = ${fmtComplex(Z)} Pa·s/m, z₀ = ${z0} Pa·s/m → ζ = ${fmtComplex(zeta, 3)}`,
        result: `α_normal = ${fmtFixed(alpha_n, 3)} · α_oblique(${theta}°) = ${fmtFixed(alpha_theta, 3)} · α_random = ${fmtFixed(alpha_r, 3)} · α(Z=1) = ${fmtFixed(alpha_F[0], 4)}`
      }
    ];

    return {
      vars: {
        rho_c: C.rho_c, rho_c2: C.rho_c2, f_membrane, f_rule, f_A2, L_A3,
        s_B, f_helmholtz, s_B2, V_B2, P_C, delta_C, f_perf, f_quarter, f_half_dip,
        R_n, alpha_n, alpha_theta, zeta, alpha_r, alpha_F
      },
      highlights: [
        { label: 'A: Membrane f_r', value: fmtFixed(f_membrane, 1), unit: 'Hz', sub: `2023 MC6: ${fmtFixed(f_A2, 0)} Hz · 2024 MC7 L: ${fmtFixed(L_A3 * 100, 1)} cm` },
        { label: 'B: Helmholtz f₀ / V', value: fmtFixed(f_helmholtz, 0), unit: 'Hz', sub: `2024 MC6 V = ${fmtFixed(V_B2, 4)} m³` },
        { label: 'C: Perforated Panel f₀', value: fmtFixed(f_perf, 1), unit: 'Hz', sub: `P = ${fmtFixed(P_C * 100, 1)}% · Porous λ/4: ${fmtFixed(f_quarter, 0)} Hz` },
        { label: 'E: α_normal / α_random', value: `${fmtFixed(alpha_n, 3)} / ${fmtFixed(alpha_r, 2)}`, unit: '', sub: `Z = ${fmtComplex(Z)} (ζ = ${fmtComplex(zeta, 2)})` }
      ],
      steps,
      warnings: [
        'TRAP: In the Paris random-incidence formula, you MUST normalise Z by ρc first (ζ = Z / ρc = r + jx). Forgetting to divide by ρc gives 0.003 instead of 0.53!',
        'TRAP: Membrane mass m is SURFACE MASS DENSITY in kg/m² (= density × thickness). Helmholtz neck radius is d/2 (don’t plug diameter into πr²!).'
      ]
    };
  }

  // =========================================================================
  // T12: Hearing: ERB, power-spectrum masking, combination tones, loudness
  // =========================================================================
  function solveT12(raw = {}) {
    const F = parseNumberList(raw.F !== undefined ? raw.F : [0.1, 1, 10]); // in kHz!
    const ERB = F.map(Fk => 24.7 * (4.37 * Fk + 1));
    const CB_bark = F.map(Fk => 25 + 75 * Math.pow(1 + 1.4 * Fk * Fk, 0.69));
    const third_oct = F.map(Fk => (Math.pow(2, 1 / 6) - Math.pow(2, -1 / 6)) * Fk * 1000);

    // Block B: Masked threshold of a tone in noise
    const N0_dB = raw.N0_dB !== undefined ? Number(raw.N0_dB) : 40;
    const k = raw.k !== undefined ? Number(raw.k) : 0.3;
    const df_noise = raw.df_noise !== undefined ? Number(raw.df_noise) : Infinity;
    const Ls = ERB.map(erb => N0_dB + 10 * Math.log10(k) + 10 * Math.log10(Math.min(df_noise, erb)));
    const Ls_20Hz = ERB.map(erb => N0_dB + 10 * Math.log10(k) + 10 * Math.log10(Math.min(20, erb)));

    // Block C & D: Combination tones & masking noise density
    const f1 = raw.f1 !== undefined ? Number(raw.f1) : 1.0; // kHz
    const f2 = raw.f2 !== undefined ? Number(raw.f2) : 1.1; // kHz
    const L1 = raw.L1 !== undefined ? Number(raw.L1) : 50;
    const nCT = [1, 2, 3];
    const f_CT = nCT.map(n => f1 - n * (f2 - f1));
    const L_CT = f_CT.map(fct => L1 + 125 * (fct - f1));
    const ERB_09 = 24.7 * (4.37 * f_CT[0] + 1);
    const N0_req_dB = L_CT[0] - 10 * Math.log10(k) - 10 * Math.log10(ERB_09);
    const Ls_at_CT = f_CT.map(fct => N0_req_dB + 10 * Math.log10(k) + 10 * Math.log10(24.7 * (4.37 * fct + 1)));

    // Block E: Two tones in same auditory filter? (2022 MC14 & 2023 MC14)
    const fa = raw.fa !== undefined ? Number(raw.fa) : 850; // Hz
    const fb = raw.fb !== undefined ? Number(raw.fb) : 900; // Hz
    const ERB_mid = 24.7 * (4.37 * ((fa + fb) / 2000) + 1);
    const beat_rate = Math.abs(fb - fa);
    const same_filter = beat_rate < ERB_mid ? 1 : 0;
    const f_CDT_pair = 2 * Math.min(fa, fb) - Math.max(fa, fb);
    const same_filter_2023 = Math.abs(600 - 400) < 24.7 * (4.37 * 0.5 + 1) ? 1 : 0;

    // Block F: Loudness sone from phon
    const L_phon = parseNumberList(raw.L_phon !== undefined ? raw.L_phon : [40, 50, 60]);
    const N_sone = L_phon.map(lp => Math.pow(2, (lp - 40) / 10));

    const steps = [
      {
        title: 'Block A & B — ERB bandwidth and Power-Spectrum Model masked threshold (Week 9 P1)',
        latex: '\\mathrm{ERB}(F) = 24.7(4.37F + 1)\\,\\mathrm{Hz}\\;(F\\text{ in kHz!}), \\qquad L_s = N_{0,\\mathrm{dB}} + 10\\log_{10}k + 10\\log_{10}\\min(\\Delta f_{\\mathrm{noise}},\\,\\mathrm{ERB})',
        sub: `F = [${F.join(', ')}] kHz → ERB = [${ERB.map(v => fmtFixed(v, 1)).join(', ')}] Hz; N₀ = ${N0_dB} dB/Hz, k = ${k} (${ fmtFixed(10 * Math.log10(k), 2)} dB)`,
        result: `Broadband L_s = [${Ls.map(v => fmtFixed(v, 1)).join(', ')}] dB  |  20 Hz narrowband L_s = [${Ls_20Hz.map(v => fmtFixed(v, 1)).join(', ')}] dB`
      },
      {
        title: 'Block C & D — Combination tones f_CT = f₁ - n(f₂ - f₁) and required masking density N₀ (Week 9 P3)',
        latex: 'f_{\\mathrm{CT},n} = f_1 - n(f_2 - f_1), \\qquad N_{0,\\mathrm{req}} = L_{\\mathrm{CT},1} - 10\\log_{10}k - 10\\log_{10}\\mathrm{ERB}(f_{\\mathrm{CT},1})',
        sub: `f₁ = ${f1} kHz, f₂ = ${f2} kHz, L₁ = ${L1} dB → f_CT = [${f_CT.map(v => fmtFixed(v * 1000, 0)).join(', ')}] Hz at L_CT = [${L_CT.map(v => fmtFixed(v, 1)).join(', ')}] dB`,
        result: `Required N₀ = ${fmtFixed(N0_req_dB, 1)} dB/Hz → thresholds at CTs: [${Ls_at_CT.map(v => fmtFixed(v, 1)).join(', ')}] dB`
      },
      {
        title: 'Block E & F — Two tones in one ERB filter? (2022/2023 MC14) & Sone/Phon loudness',
        latex: '|f_b - f_a| < \\mathrm{ERB}(f_{\\mathrm{mid}}) \\implies \\text{1 beating tone at } |f_b - f_a|; \\qquad N = 2^{(L_N - 40)/10}\\,\\mathrm{sone}',
        sub: `f_a = ${fa} Hz, f_b = ${fb} Hz → Δf = ${beat_rate} Hz vs ERB(${(fa + fb) / 2} Hz) = ${fmtFixed(ERB_mid, 1)} Hz (cubic diff tone 2f₁-f₂ = ${f_CDT_pair} Hz)`,
        result: same_filter
          ? `SAME FILTER (Δf = ${beat_rate} Hz < ERB ${fmtFixed(ERB_mid, 1)} Hz) → perceived as ONE tone beating at ${beat_rate} Hz`
          : `SEPARATE FILTERS (Δf = ${beat_rate} Hz > ERB ${fmtFixed(ERB_mid, 1)} Hz) → perceived as TWO distinct tones`
      }
    ];

    return {
      vars: {
        ERB, CB_bark, third_oct, Ls, Ls_20Hz, f_CT, L_CT, ERB_09, N0_req_dB, Ls_at_CT,
        ERB_mid, same_filter, beat_rate, same_filter_2023, N_sone
      },
      highlights: [
        { label: 'A: ERB Bandwidths', value: ERB.map(v => fmtFixed(v, 1)).join(' / '), unit: 'Hz', sub: `at F = [${F.join(', ')}] kHz` },
        { label: 'B: Masked Threshold L_s', value: Ls.map(v => fmtFixed(v, 1)).join(' / '), unit: 'dB', sub: `20 Hz band: ${fmtFixed(Ls_20Hz[0], 1)} dB` },
        { label: 'D: Masking N₀ Needed', value: fmtFixed(N0_req_dB, 1), unit: 'dB/Hz', sub: `700 Hz threshold: ${fmtFixed(Ls_at_CT[2], 1)} dB` },
        { label: `E: ${fa} & ${fb} Hz Filter`, value: same_filter ? '1 Filter (Beats)' : '2 Separate Filters', unit: `Δf=${beat_rate} Hz`, sub: `ERB = ${fmtFixed(ERB_mid, 1)} Hz · 2f₁-f₂ = ${f_CDT_pair} Hz` }
      ],
      steps,
      warnings: [
        'TRAP: F in ERB = 24.7(4.37·F + 1) MUST be in kHz (e.g. 100 Hz = 0.1, 1000 Hz = 1.0)!',
        'TRAP (2022/2023 MC14): The strongest combination tone is 2f₁ - f₂ (with f₁ < f₂), which lies BELOW the lower tone f₁ (800 Hz for 850/900 Hz; 200 Hz for 400/600 Hz — the options 950 Hz and 800 Hz are traps!).'
      ]
    };
  }

  // =========================================================================
  // T13: Physiological acoustics: Greenwood map, OAE latency, ABR averaging
  // =========================================================================
  function solveT13(raw = {}) {
    const A = raw.A !== undefined ? Number(raw.A) : 20682;
    const G = raw.G !== undefined ? Number(raw.G) : 61.765;
    const B = raw.B !== undefined ? Number(raw.B) : 140.6;
    const L_cochlea = raw.L_cochlea !== undefined ? Number(raw.L_cochlea) : 0.034;
    const f_query = raw.f_query !== undefined ? Number(raw.f_query) : 1000;
    const x_query_mm = raw.x_query_mm !== undefined ? Number(raw.x_query_mm) : 20.4;

    const F_base = A * Math.pow(10, -G * 0) - B;
    const F_apex = A * Math.pow(10, -G * L_cochlea) - B;
    const x_of_f_mm = -(1 / G) * Math.log10((f_query + B) / A) * 1000;
    const f_of_x = A * Math.pow(10, -G * (x_query_mm / 1000)) - B;
    const mm_per_octave = (Math.log10(2) / G) * 1000;

    // Block B: OAE roundtrip time -> place -> frequency
    const c_BM = raw.c_BM !== undefined ? Number(raw.c_BM) : 3;
    const t_rt_ms = parseNumberList(raw.t_rt_ms !== undefined ? raw.t_rt_ms : [12, 7, 5]);
    const t_rt = t_rt_ms.map(tms => tms * 1e-3);
    const x_oae = t_rt.map(t => c_BM * t / 2);
    const F_oae = x_oae.map(xo => A * Math.pow(10, -G * xo) - B);

    // Block C: ABR averaging
    const EP = raw.EP !== undefined ? Number(raw.EP) : 0.3e-6;
    const N1 = raw.N1 !== undefined ? Number(raw.N1) : 3e-6;
    const rate = raw.rate !== undefined ? Number(raw.rate) : 20;
    const SNR_target_dB = raw.SNR_target_dB !== undefined ? Number(raw.SNR_target_dB) : 10;
    const frac_bad = raw.frac_bad !== undefined ? Number(raw.frac_bad) : 0.1;
    const N_bad = raw.N_bad !== undefined ? Number(raw.N_bad) : 30e-6;

    const SNR1_dB = 20 * Math.log10(EP / N1);
    const gain_per_doubling = 10 * Math.log10(2);
    const n_needed = Math.pow(10, (SNR_target_dB - SNR1_dB) / 10);
    const t_needed = n_needed / rate;

    const N_eff = Math.sqrt((1 - frac_bad) * N1 * N1 + frac_bad * N_bad * N_bad);
    const n_noRej = Math.pow(N_eff / (EP / Math.pow(10, SNR_target_dB / 20)), 2);
    const t_noRej = n_noRej / rate;
    const n_rej = n_needed / (1 - frac_bad);
    const t_rej = n_rej / rate;

    // Block D: Outer and middle ear
    const f_canal = 340 / (4 * 0.025);
    const ME_gain_dB = 20 * Math.log10(14 * 1.3);
    const tau_aw = 4 * 412 * 1.48e6 / Math.pow(412 + 1.48e6, 2);
    const loss_aw_dB = -10 * Math.log10(tau_aw);

    const steps = [
      {
        title: 'Block A — Greenwood cochlear frequency-position map (Week 10 P1)',
        latex: 'F_c(x) = A\\cdot 10^{-Gx} - B, \\qquad x = -\\frac{1}{G}\\log_{10}\\left(\\frac{F_c + B}{A}\\right)\\quad(x\\text{ in metres from BASE})',
        sub: `A = ${A}, G = ${G} m⁻¹, B = ${B}, L_cochlea = ${L_cochlea * 1000} mm`,
        result: `Base (x=0): ${fmtFixed(F_base, 0)} Hz · Apex (${L_cochlea * 1000} mm): ${fmtFixed(F_apex, 1)} Hz · f=${f_query} Hz is at x=${fmtFixed(x_of_f_mm, 2)} mm (x=${x_query_mm} mm → ${fmtFixed(f_of_x, 0)} Hz)`
      },
      {
        title: 'Block B — OAE roundtrip latency to characteristic place and frequency (Week 10 P3)',
        latex: 'x = c_{\\mathrm{BM}}\\frac{t_{\\mathrm{rt}}}{2}, \\qquad F_{\\mathrm{OAE}} = A\\cdot 10^{-Gx} - B',
        sub: `c_BM = ${c_BM} m/s, t_rt = [${t_rt_ms.join(', ')}] ms → x = [${x_oae.map(v => fmtFixed(v * 1000, 1)).join(', ')}] mm`,
        result: `F_OAE = [${F_oae.map(v => fmtFixed(v, 1) + ' Hz').join(', ')}]`
      },
      {
        title: 'Block C — ABR signal averaging & artifact rejection (Week 10 P2)',
        latex: '\\mathrm{SNR}_1 = 20\\log_{10}\\frac{\\mathrm{EP}}{N_1}, \\quad \\mathrm{SNR}_n = \\mathrm{SNR}_1 + 10\\log_{10}n, \\quad N_{\\mathrm{eff}} = \\sqrt{(1-p)N_1^2 + p N_{\\mathrm{bad}}^2}',
        sub: `EP = ${EP * 1e6} µV, N₁ = ${N1 * 1e6} µV → SNR₁ = ${fmtFixed(SNR1_dB, 1)} dB; Target = ${SNR_target_dB} dB at ${rate} sweeps/s; ${frac_bad * 100}% artifacts at ${N_bad * 1e6} µV`,
        result: `Clean: n = ${fmtFixed(n_needed, 0)} sweeps (${fmtFixed(t_needed, 1)} s) · No rejection: N_eff = ${fmtFixed(N_eff * 1e6, 3)} µV, n = ${fmtFixed(n_noRej, 0)} (${fmtFixed(t_noRej, 0)} s) · With rejection: n_pres = ${fmtFixed(n_rej, 0)} (${fmtFixed(t_rej, 1)} s)`
      }
    ];

    return {
      vars: {
        F_base, F_apex, x_of_f_mm, f_of_x, mm_per_octave, x_oae, F_oae,
        SNR1_dB, gain_per_doubling, n_needed, t_needed, N_eff, n_noRej, t_noRej, n_rej, t_rej,
        f_canal, ME_gain_dB, loss_aw_dB
      },
      highlights: [
        { label: 'A: Base / Apex F_c', value: `${fmtFixed(F_base, 0)} / ${fmtFixed(F_apex, 1)}`, unit: 'Hz', sub: `${f_query} Hz → ${fmtFixed(x_of_f_mm, 1)} mm from base` },
        { label: 'B: OAE Frequencies', value: F_oae.map(v => fmtFixed(v, 1)).join(' / '), unit: 'Hz', sub: `x = ${x_oae.map(v => fmtFixed(v * 1000, 1)).join('/')} mm` },
        { label: 'C: Clean ABR Sweeps', value: fmtFixed(n_needed, 0), unit: `sweeps (${fmtFixed(t_needed, 0)} s)`, sub: `SNR₁ = ${fmtFixed(SNR1_dB, 1)} dB → ${SNR_target_dB} dB` },
        { label: 'C: Artifact Time (NoRej/Rej)', value: `${fmtFixed(t_noRej, 0)} s / ${fmtFixed(t_rej, 1)} s`, unit: '', sub: `N_eff = ${fmtFixed(N_eff * 1e6, 3)} µV` }
      ],
      steps,
      warnings: [
        'TRAP: In Greenwood’s equation, x is measured from the BASE in METRES (so 18 mm = 0.018 m), and OAE latency t_rt is a ROUNDTRIP time (must divide by 2: x = c_BM · t_rt / 2)!',
        'TRAP: Averaging n sweeps improves SNR by 10 log₁₀(n) (+3 dB per doubling), NOT 20 log₁₀(n). And mixed noise averages by POWER (N_eff² = Σ w_i N_i²), not amplitude!'
      ]
    };
  }

  // =========================================================================
  // T14: Vibration isolation: static deflection, transmissibility, mobility
  // =========================================================================
  function solveT14(raw = {}) {
    const C = getConsts(raw);

    // Block A: Static deflection to f0 and transmissibility (2022 MC11, 2024 MC10)
    const m = raw.m !== undefined ? Number(raw.m) : 100;
    const xi0 = raw.xi0 !== undefined ? Number(raw.xi0) : 0.01;
    const f = raw.f !== undefined ? Number(raw.f) : 7;
    const zeta = raw.zeta !== undefined ? Number(raw.zeta) : 0;

    const s = m * C.g / xi0;
    const f0 = Math.sqrt(s / m) / (2 * Math.PI);
    const f0_rule = 0.5 / Math.sqrt(xi0);
    const f_isolation_starts = Math.SQRT2 * f0;
    const Omega = f / f0;
    const T = Math.sqrt((1 + Math.pow(2 * zeta * Omega, 2)) / (Math.pow(1 - Omega * Omega, 2) + Math.pow(2 * zeta * Omega, 2)));
    const T_dB = 20 * Math.log10(T);
    const isolation_dB = -T_dB;

    // Block B: 2023 MC9 (1.5 cm deflection)
    const xi0_B = raw.xi0_B !== undefined ? Number(raw.xi0_B) : 0.015;
    const f0_B = Math.sqrt(C.g / xi0_B) / (2 * Math.PI);

    // Block C: Forced undamped mass-spring (Week 11 P3)
    const s_C = raw.s_C !== undefined ? Number(raw.s_C) : 23.8e3;
    const m_C = raw.m_C !== undefined ? Number(raw.m_C) : 1.5;
    const F_C = raw.F_C !== undefined ? Number(raw.F_C) : 5;
    const w_C = parseNumberList(raw.w_C !== undefined ? raw.w_C : [37.8, 378]);
    const w0_C = Math.sqrt(s_C / m_C);
    const f0_C = w0_C / (2 * Math.PI);
    const xi_C = w_C.map(wc => F_C / (s_C * Math.abs(1 - Math.pow(wc / w0_C, 2))));
    const v_C = w_C.map((wc, idx) => wc * xi_C[idx]);
    const a_C = w_C.map((wc, idx) => wc * wc * xi_C[idx]);
    const Ff_C = xi_C.map(xic => s_C * xic);

    // Block D: Stiffness for target motion ratio (base excitation, Week 11 P4)
    const f_D = raw.f_D !== undefined ? Number(raw.f_D) : 25;
    const w_D = 2 * Math.PI * f_D;
    const m_D = raw.m_D !== undefined ? Number(raw.m_D) : 1.5;
    const ratio_D = raw.ratio_D !== undefined ? Number(raw.ratio_D) : -0.1;
    const s_D = -ratio_D * w_D * w_D * m_D / (1 - ratio_D);
    const f0_D = Math.sqrt(s_D / m_D) / (2 * Math.PI);

    // Block E: Mobility blocked force (2023 MC11)
    const v_free = raw.v_free !== undefined ? Number(raw.v_free) : 0.01;
    const m_src = raw.m_src !== undefined ? Number(raw.m_src) : 0.1;
    const f_E = raw.f_E !== undefined ? Number(raw.f_E) : 500;
    const Y_S = cDiv(1, { re: 0, im: 2 * Math.PI * f_E * m_src });
    const Y_R = parseComplexToken(raw.Y_R !== undefined ? raw.Y_R : 0);
    const F_E = cDiv(v_free, cAdd(Y_S, Y_R));

    const steps = [
      {
        title: 'Block A & B — Static deflection ξ₀ to natural frequency f₀ and transmissibility T (2022 MC11, 2023 MC9, 2024 MC10)',
        latex: 's = \\frac{mg}{\\xi_0}, \\quad f_0 = \\frac{1}{2\\pi}\\sqrt{\\frac{g}{\\xi_0}} \\approx \\frac{0.5}{\\sqrt{\\xi_0}}, \\quad f_{\\mathrm{iso}} = \\sqrt{2}\\,f_0, \\quad T = \\sqrt{\\frac{1+(2\\zeta\\Omega)^2}{(1-\\Omega^2)^2+(2\\zeta\\Omega)^2}}',
        sub: `ξ₀ = ${xi0 * 100} cm (${xi0} m), m = ${m} kg → s = ${fmtNum(s, 4)} N/m, f₀ = ${fmtFixed(f0, 2)} Hz; excitation f = ${f} Hz (Ω = ${fmtFixed(Omega, 3)}, ζ = ${zeta})`,
        result: `f₀ = ${fmtFixed(f0, 2)} Hz · Isolation starts at √2·f₀ = ${fmtFixed(f_isolation_starts, 2)} Hz · At ${f} Hz: T = ${fmtFixed(T, 3)} (20 log T = ${fmtFixed(T_dB, 2)} dB ≈ 0 dB) · Block B (${xi0_B * 100} cm): f₀ = ${fmtFixed(f0_B, 2)} Hz`
      },
      {
        title: 'Block C — Forced undamped mass-spring response & force transmitted to floor (Week 11 P3)',
        latex: '\\omega_0 = \\sqrt{\\frac{s}{m}}, \\qquad |\\xi| = \\frac{F}{s\\,|1 - (\\omega/\\omega_0)^2|}, \\qquad |F_{\\mathrm{floor}}| = s|\\xi|',
        sub: `s = ${s_C} N/m, m = ${m_C} kg → ω₀ = ${fmtFixed(w0_C, 1)} rad/s (f₀ = ${fmtFixed(f0_C, 2)} Hz); F = ${F_C} N at ω = [${w_C.join(', ')}] rad/s`,
        result: w_C.map((wc, idx) => `ω=${wc}: |ξ|=${fmtFixed(xi_C[idx] * 1e3, 3)} mm, |F_floor|=${fmtFixed(Ff_C[idx], 3)} N`).join('  |  ')
      },
      {
        title: 'Block D & E — Stiffness for target motion ratio (Week 11 P4) & Mobility blocked force (2023 MC11)',
        latex: 's = \\frac{-(u/u_f)\\omega^2 m}{1 - u/u_f}, \\qquad F = \\frac{v_{\\mathrm{free}}}{Y_S + Y_R}, \\quad Y_{S,\\mathrm{mass}} = \\frac{1}{j\\omega m_{\\mathrm{src}}}',
        sub: `Block D: f=${f_D} Hz, m=${m_D} kg, u/u_f=${ratio_D};  Block E: v_free=${v_free} m/s, m_src=${m_src} kg, f=${f_E} Hz`,
        result: `Block D: s = ${fmtFixed(s_D, 0)} N/m (f₀ = ${fmtFixed(f0_D, 2)} Hz)  |  Block E: F = ${fmtComplex(F_E, 3)} N`
      }
    ];

    return {
      vars: {
        s, f0, f0_rule, f_isolation_starts, Omega, T, T_dB, isolation_dB,
        f0_B, w0_C, f0_C, xi_C, v_C, a_C, Ff_C, s_D, f0_D, Y_S, Y_R, F_E
      },
      highlights: [
        { label: 'A: f₀ & √2·f₀ Start', value: `${fmtFixed(f0, 2)} Hz`, unit: `iso > ${fmtFixed(f_isolation_starts, 2)} Hz`, sub: `Block B (${xi0_B * 100} cm): f₀ = ${fmtFixed(f0_B, 1)} Hz` },
        { label: `A: 20 log T at ${f} Hz`, value: fmtFixed(T_dB, 2), unit: 'dB', sub: `T = ${fmtFixed(T, 3)} (Isolation = ${fmtFixed(isolation_dB, 2)} dB)` },
        { label: 'C: Forced Response', value: `${fmtFixed(f0_C, 2)} Hz`, unit: `|ξ|=${fmtFixed(xi_C[0] * 1e3, 3)} mm`, sub: `|F_floor| = ${Ff_C.map(v => fmtFixed(v, 3)).join(' / ')} N` },
        { label: 'E: Blocked Force F', value: fmtComplex(F_E, 3), unit: 'N', sub: `Block D: s = ${fmtFixed(s_D, 0)} N/m (f₀=${fmtFixed(f0_D, 2)} Hz)` }
      ],
      steps,
      warnings: [
        'DECISION: Vibration isolation ONLY occurs above √2·f₀! Below √2·f₀, T > 1 (amplification). At f = √2·f₀, T = 1 (0 dB) for any damping.',
        'TRAP: Once static deflection ξ₀ is given, the mass m cancels out of f₀ = (1/2π)√(g/ξ₀) ≈ 0.5/√ξ₀. Remember to convert ξ₀ from cm to metres!',
        'TRAP (Week 11 P4): Above resonance the mass moves in antiphase with the floor, so u/u_f is NEGATIVE (-0.1, not +0.1).'
      ]
    };
  }

  // =========================================================================
  // T15: Sound insulation: mass law, two rooms, composite walls, f_c, double wall
  // =========================================================================
  function solveT15(raw = {}) {
    const C = getConsts(raw);

    // Block A: Mass law
    const m_A = raw.m_A !== undefined ? Number(raw.m_A) : 2300 * 0.10;
    const f_A = raw.f_A !== undefined ? Number(raw.f_A) : 500;
    const R0_A = 20 * Math.log10((2 * Math.PI * f_A * m_A) / (2 * C.rho_c));
    const R_field_A = R0_A - 5;
    const R_random_A = R0_A - 10 * Math.log10(0.23 * R0_A);

    // Block B: Two rooms (2023 MC8)
    const L1_B = raw.L1_B !== undefined ? Number(raw.L1_B) : 80;
    const R_B = raw.R_B !== undefined ? Number(raw.R_B) : 40;
    const S_B = raw.S_B !== undefined ? Number(raw.S_B) : 12;
    const V2 = raw.V2 !== undefined ? Number(raw.V2) : 60;
    const T2 = raw.T2 !== undefined ? Number(raw.T2) : 0.5;
    const A2 = 55.3 * V2 / (C.c * T2);
    const L2_B = L1_B - R_B + 10 * Math.log10(S_B / A2);

    // Block C: Composite wall (door, window, crack)
    const S_i = parseNumberList(raw.S_i !== undefined ? raw.S_i : [18, 2]);
    const R_i = parseNumberList(raw.R_i !== undefined ? raw.R_i : [44, 26]);
    const S_sum = S_i.reduce((a, b) => a + b, 0);
    let tauSum = 0;
    for (let i = 0; i < S_i.length; i++) {
      tauSum += S_i[i] * Math.pow(10, -R_i[i % R_i.length] / 10);
    }
    const R_res = -10 * Math.log10(tauSum / S_sum);
    const R_crack = -10 * Math.log10(((10 - 1e-3) * Math.pow(10, -5) + 1e-3) / 10);

    // Block C2 (Sheet P3) & Block D (2022 MC8): R of one element from target/result
    const S_tot = raw.S_tot !== undefined ? Number(raw.S_tot) : 20;
    const R_res_C2 = raw.R_res_C2 !== undefined ? Number(raw.R_res_C2) : 40;
    const S_win = raw.S_win !== undefined ? Number(raw.S_win) : 1;
    const R_wall = raw.R_wall !== undefined ? Number(raw.R_wall) : 45;
    const R_win_C2 = -10 * Math.log10((S_tot * Math.pow(10, -R_res_C2 / 10) - (S_tot - S_win) * Math.pow(10, -R_wall / 10)) / S_win);

    const S_tot_D = raw.S_tot_D !== undefined ? Number(raw.S_tot_D) : 25;
    const R_target = raw.R_target !== undefined ? Number(raw.R_target) : 50;
    const R_wall_D = raw.R_wall_D !== undefined ? Number(raw.R_wall_D) : 55;
    const S_win_D = raw.S_win_D !== undefined ? Number(raw.S_win_D) : 2;
    const R_win_D = -10 * Math.log10((S_tot_D * Math.pow(10, -R_target / 10) - (S_tot_D - S_win_D) * Math.pow(10, -R_wall_D / 10)) / S_win_D);

    // Block E: Critical frequency f_c (2024 MC8 & 2022 MC9)
    const E = raw.E !== undefined ? Number(raw.E) : 2.6e10;
    const rho_M = raw.rho_M !== undefined ? Number(raw.rho_M) : 2300;
    const nu = raw.nu !== undefined ? Number(raw.nu) : 0.2;
    const h = parseNumberList(raw.h !== undefined ? raw.h : [0.10, 0.15]);
    const eta = raw.eta !== undefined ? Number(raw.eta) : 0.02;
    const B = h.map(hi => E * Math.pow(hi, 3) / (12 * (1 - nu * nu)));
    const m_E = h.map(hi => rho_M * hi);
    const fc = h.map((hi, idx) => (C.c * C.c / (2 * Math.PI)) * Math.sqrt(m_E[idx] / B[idx]));
    const dfc = fc.length >= 2 ? fc[1] - fc[0] : 0;
    const fc_stacked = 3000;
    const fc_double_thick = 1500;
    const R_above_fc = R0_A + 10 * Math.log10((2 * eta * f_A) / (Math.PI * fc[0]));

    // Block F: Double wall (2024 MC11)
    const m1 = raw.m1 !== undefined ? Number(raw.m1) : 1200 * 0.013;
    const m2 = raw.m2 !== undefined ? Number(raw.m2) : m1;
    const d = raw.d !== undefined ? Number(raw.d) : 0.10;
    const f_F = raw.f_F !== undefined ? Number(raw.f_F) : 600;
    const f0_dw = (C.c / (2 * Math.PI)) * Math.sqrt((C.rho / d) * (1 / m1 + 1 / m2));
    const fd_dw = C.c / (2 * Math.PI * d);
    const R1 = 20 * Math.log10((2 * Math.PI * f_F * m1) / (2 * C.rho_c)) - 5;
    const R2 = 20 * Math.log10((2 * Math.PI * f_F * m2) / (2 * C.rho_c)) - 5;
    const R_double = R1 + R2 + 6;
    const R_mid_range = R1 + R2 + 20 * Math.log10(2 * (2 * Math.PI * f_F / C.c) * d);
    const R_together = 20 * Math.log10((2 * Math.PI * f_F * (m1 + m2)) / (2 * C.rho_c)) - 5;
    const gain_double = R_double - R_together;

    // Block G: Flanking and impact sound
    const R_app = -10 * Math.log10(Math.pow(10, -55 / 10) + 4 * Math.pow(10, -62 / 10));
    const Ln = 65 + 10 * Math.log10((0.161 * 50 / 0.5) / 10);

    const steps = [
      {
        title: 'Block A & B — Mass law (normal vs field incidence) & Two-room formula (2023 MC8)',
        latex: 'R_0 = 20\\log_{10}\\frac{\\omega m}{2\\rho c}, \\quad R_{\\mathrm{field}} = R_0 - 5\\,\\mathrm{dB}, \\qquad L_2 = L_1 - R + 10\\log_{10}\\frac{S}{A_2}, \\quad A_2 = \\frac{55.3\\,V_2}{c\\,T_2}',
        sub: `Mass law (m=${m_A} kg/m², f=${f_A} Hz): R₀=${fmtFixed(R0_A, 1)} dB, R_field=${fmtFixed(R_field_A, 1)} dB; Two rooms: L₁=${L1_B} dB, R=${R_B} dB, S=${S_B} m², A₂=${fmtFixed(A2, 2)} m²`,
        result: `Receiver room level L₂ = ${fmtFixed(L2_B, 1)} dB`
      },
      {
        title: 'Block C & D — Composite wall transmission loss & required window R (2022 MC8, Sheet P3)',
        latex: 'R_{\\mathrm{res}} = -10\\log_{10}\\left(\\frac{\\sum_i S_i 10^{-R_i/10}}{\\sum_i S_i}\\right), \\qquad R_{\\mathrm{win}} = -10\\log_{10}\\left(\\frac{S_{\\mathrm{tot}}10^{-R_{\\mathrm{target}}/10} - S_{\\mathrm{wall}}10^{-R_{\\mathrm{wall}}/10}}{S_{\\mathrm{win}}}\\right)',
        sub: `Composite S=[${S_i.join(', ')}] m², R=[${R_i.join(', ')}] dB; Window D (2022 MC8): S_tot=${S_tot_D} m², R_target=${R_target} dB, R_wall=${R_wall_D} dB, S_win=${S_win_D} m²`,
        result: `R_res = ${fmtFixed(R_res, 1)} dB · Crack R = ${fmtFixed(R_crack, 1)} dB · Sheet P3 Window = ${fmtFixed(R_win_C2, 1)} dB · 2022 MC8 Min Window R = ${fmtFixed(R_win_D, 1)} dB`
      },
      {
        title: 'Block E — Critical frequency f_c change with thickness & stacked plates (2024 MC8, 2022 MC9)',
        latex: 'B = \\frac{Eh^3}{12(1-\\nu^2)}, \\quad m = \\rho_M h, \\quad f_c = \\frac{c^2}{2\\pi}\\sqrt{\\frac{m}{B}} \\propto \\frac{1}{h}',
        sub: `E = ${fmtNum(E)} Pa, ρ_M = ${rho_M} kg/m³, ν = ${nu}, h = [${h.join(', ')}] m`,
        result: `f_c = [${fc.map(v => fmtFixed(v, 1) + ' Hz').join(' → ')}] · Change Δf_c = ${fmtFixed(dfc, 1)} Hz · Stacked loose plates keep f_c = ${fc_stacked} Hz`
      },
      {
        title: 'Block F — Double wall resonance f₀, cavity cutoff f_d, and improvement over single leaf (2024 MC11)',
        latex: 'f_0 = \\frac{c}{2\\pi}\\sqrt{\\frac{\\rho}{d}\\left(\\frac{1}{m_1}+\\frac{1}{m_2}\\right)}, \\quad f_d = \\frac{c}{2\\pi d}, \\quad R_{\\mathrm{double}}(f > f_d) = R_1 + R_2 + 6\\,\\mathrm{dB}',
        sub: `m₁=m₂=${fmtFixed(m1, 2)} kg/m², d=${d} m, f=${f_F} Hz → f₀=${fmtFixed(f0_dw, 1)} Hz, f_d=${fmtFixed(fd_dw, 0)} Hz (< ${f_F} Hz), R₁=${fmtFixed(R1, 2)} dB`,
        result: `R_double = ${fmtFixed(R_double, 2)} dB vs R_together = ${fmtFixed(R_together, 2)} dB → Gain ΔR = +${fmtFixed(gain_double, 1)} dB`
      }
    ];

    return {
      vars: {
        rho_c: C.rho_c, R0_A, R_field_A, R_random_A, A2, L2_B,
        R_res, R_crack, R_win_C2, R_win_D, B, m_E, fc, dfc, fc_stacked, fc_double_thick, R_above_fc,
        f0_dw, fd_dw, R1, R2, R_double, R_mid_range, R_together, gain_double, R_app, Ln
      },
      highlights: [
        { label: 'B: Receiver Room L₂', value: fmtFixed(L2_B, 1), unit: 'dB', sub: `A₂ = ${fmtFixed(A2, 1)} m² · R_field = R₀ - 5 dB` },
        { label: 'C/D: Composite & Window', value: `${fmtFixed(R_res, 1)} / ${fmtFixed(R_win_D, 1)}`, unit: 'dB', sub: `Sheet P3 win: ${fmtFixed(R_win_C2, 1)} dB · Crack: ${fmtFixed(R_crack, 1)} dB` },
        { label: 'E: Critical Freq Δf_c', value: fmtFixed(dfc, 1), unit: 'Hz', sub: `${fc.map(v => fmtFixed(v, 0)).join(' → ')} Hz (f_c ∝ 1/h)` },
        { label: 'F: Double Wall Gain', value: `+${fmtFixed(gain_double, 1)}`, unit: 'dB', sub: `f_d = ${fmtFixed(fd_dw, 0)} Hz · R₁ = ${fmtFixed(R1, 2)} dB` }
      ],
      steps,
      warnings: [
        'DECISION: Field incidence transmission loss is R_field = R₀ - 5 dB (2023 MC10).',
        'TRAP (2022 MC9): Stacking two loose/unbonded plates doubles both B and m, so f_c = (c²/2π)√(2m/2B) is UNCHANGED (3000 Hz)! Bonding them into double thickness makes B×8 and halves f_c (1500 Hz is the trap).',
        'TRAP (2024 MC11): In the double-wall question, 38.1 dB is R_together (the trap option); the gain of separating them by 10 cm is R_double - R_together = 70.16 - 38.10 = 32.1 dB.'
      ]
    };
  }

  // Map template names to solver functions
  const SOLVER_MAP = {
    T01_plane_wave_reflection: solveT01,
    T02_tube_driven_end: solveT02,
    T03_levels_adding_Leq: solveT03,
    T04_octave_bands_A_weighting: solveT04,
    T05_intensity_power_SWR: solveT05,
    T06_monopole_nearfield_power: solveT06,
    T07_two_sources_wall_dipole: solveT07,
    T08_loudspeaker: solveT08,
    T09_room_modes: solveT09,
    T10_reverberation_diffuse_field: solveT10,
    T11_absorbers: solveT11,
    T12_hearing_ERB_masking: solveT12,
    T13_physiology_greenwood_ABR: solveT13,
    T14_vibration_isolation: solveT14,
    T15_sound_insulation: solveT15
  };

  function runSolver(idOrScript, inputs = {}) {
    if (SOLVER_MAP[idOrScript]) return SOLVER_MAP[idOrScript](inputs);
    const key = Object.keys(SOLVER_MAP).find(k => k.startsWith(idOrScript));
    if (key) return SOLVER_MAP[key](inputs);
    throw new Error(`Unknown solver: ${idOrScript}`);
  }

  return {
    DEFAULT_CONSTANTS,
    FA_TABLE,
    KA_TABLE,
    KC_TABLE,
    OCTAVE_CENTRES,
    cplx, cAdd, cSub, cMul, cDiv, cAbs, cConj, cExpJ, cArgDeg,
    parseComplexToken, parseComplexList, parseNumberList,
    fmtNum, fmtFixed, fmtComplex,
    besselJ1,
    interpAWeight,
    interpCWeight,
    analyticAWeight,
    solveT01, solveT02, solveT03, solveT04, solveT05,
    solveT06, solveT07, solveT08, solveT09, solveT10,
    solveT11, solveT12, solveT13, solveT14, solveT15,
    runSolver,
    SOLVER_MAP
  };
});
