/* The Analogy Bench — lecture 11 (radiation, acoustic environment, micro-speakers,
   nonlinear lumped models). Pre-read: written before the lecture from Beranek & Mellow
   13.7 / 8.1–8.3 / 6.18 and p11.py. Physics first (pure functions), then the benches, then the boot. */
"use strict";

/* ===== L11 · physics ===== */
const L11 = { rho: 1.204, c: 343.2 };              // 20 °C, same as p11.py and the project fit
const L11_AW = Math.sqrt(0.0350 / Math.PI);        // System D woofer, S_D = 350 cm² → a = 105.5 mm

/* A · baffled piston */
function l11J1(x) {                                 // Bessel J1 by its integral, midpoint rule (spectrally accurate, any x)
  if (Math.abs(x) < 8) return besselJ1(x);
  const n = 40 + Math.ceil(Math.abs(x)); let s = 0;
  for (let k = 0; k < n; k++) { const t = (k + 0.5) * Math.PI / n; s += Math.cos(t - x * Math.sin(t)); }
  return s / n;
}
function pistonDir(ka, th) {                        // p(θ)/p(0) = 2 J1(v)/v, v = ka sin θ
  const v = ka * Math.sin(th);
  return Math.abs(v) < 1e-9 ? 1 : 2 * l11J1(v) / v;
}
function pistonNumbers(f, a) {
  const c = L11.c, ka = TAU * f / c * a, lam = c / f;
  const f1 = c / (TAU * a);
  let bw = null;                                   // first angle (0.01° grid) below −6 dB, as p11.py
  for (let i = 0; i <= 9000; i++) { const t = i / 100 * Math.PI / 180; if (dB(Math.abs(pistonDir(ka, t))) < -6) { bw = i / 100; break; } }
  const rmax = (a * a - lam * lam / 4) / lam;
  return { ka, f1, fnull: 3.832 * f1, bw, d90: dB(Math.abs(pistonDir(ka, Math.PI / 2))), d30: dB(Math.abs(pistonDir(ka, Math.PI / 6))),
    rR: Math.PI * a * a / lam, rmax, nz: Math.floor(a / lam), MA1: 8 * L11.rho / (3 * Math.PI * Math.PI * a) };
}

/* B · environment */
const L11_SPACES = [["free field", 4 * Math.PI, "4π"], ["one wall / baffle", 2 * Math.PI, "2π"], ["wall + floor", Math.PI, "π"], ["corner", Math.PI / 2, "π/2"]];
const spaceGain = (om) => ({ spl: 20 * Math.log10(4 * Math.PI / om), pow: 10 * Math.log10(4 * Math.PI / om), Q: 4 * Math.PI / om });
const baffleStepF = (W) => L11.c / (Math.PI * W);
function roomNumbers(V, T, Q) { const A = 0.161 * V / T; return { A, rc: Math.sqrt(Q * A / (16 * Math.PI)) }; }

/* C · micro-speaker (illustrative values, Beranek ch. 8) */
const MICRO = { fs: 800, Mms: 0.11e-3, a: 0.0062 };
function microX(f, Lp, r, Sd, om = 2 * Math.PI) {  // peak excursion (m) for Lp dB SPL at r, small source into Ω
  const prms = 20e-6 * Math.pow(10, Lp / 20), w = TAU * f;
  const U = prms * om * r / (L11.rho * w);
  return U / (w * Sd) * Math.SQRT2;
}
function microBox(Sd, Vb) {                         // back volume: acoustic suspension
  const Cms = 1 / ((TAU * MICRO.fs) ** 2 * MICRO.Mms), rc2 = L11.rho * L11.c * L11.c;
  const Vas = Cms * Sd * Sd * rc2;
  return { Vas, alpha: Vas / Vb, fc: MICRO.fs * Math.sqrt(1 + Vas / Vb) };
}
function microHelm(Vf, ah, lh) {                    // front cavity + sound hole, end correction 1.7a (flanged both ends)
  const Mah = L11.rho * (lh + 1.7 * ah) / (Math.PI * ah * ah), Caf = Vf / (L11.rho * L11.c * L11.c);
  return { Mah, Caf, f0: 1 / (TAU * Math.sqrt(Mah * Caf)) };
}

/* D · nonlinear woofer: Scan-Speak 26W/8534G00 (Lab D fit), infinite baffle; shapes assumed (no Klippel data) */
const NL = (() => {
  const RE = 5.7, LE0 = 1.50e-3, BL0 = 8.28, MMD = 36.7e-3, CMS0 = 1.174e-3, RMS = 0.61, SD = 0.0350, XMAX = 6e-3;
  const MA1 = 8 * L11.rho / (3 * Math.PI * Math.PI * L11_AW);
  const MMS = MMD + 2 * SD * SD * MA1, K0 = 1 / CMS0, XOFF = 0.5e-3;
  const B2 = (1 / 0.82 - 1) / XMAX ** 2, K1 = 0.08 / XMAX, K2 = (1 / 0.75 - 1) / XMAX ** 2, L1 = -0.20 / XMAX;
  return { RE, LE0, BL0, MMD, CMS0, RMS, SD, XMAX, MMS, K0, XOFF, B2, K1, K2, L1 };
})();
const nlBl = (x) => NL.BL0 / (1 + NL.B2 * (x - NL.XOFF) ** 2);
const nlK = (x) => NL.K0 * (1 + NL.K1 * x + NL.K2 * x * x);
const nlLe = (x) => NL.LE0 * (1 + NL.L1 * x);
function nlRhs(t, psi, u, x, v, out) {              // state: flux linkage psi = Le(x) i, velocity u, displacement x
  const i = psi / nlLe(x), B = nlBl(x);
  out[0] = v - NL.RE * i - B * u;
  out[1] = (B * i - NL.RMS * u - nlK(x) * x) / NL.MMS;
  out[2] = u;
}
/* classic RK4 at fsamp·sub, keeps every sub-th sample of x and a = du/dt (same as p11.py simulate) */
function nlSimulate(src, fsamp, n, sub = 4) {
  const hh = 1 / (fsamp * sub), X = new Float64Array(n), A = new Float64Array(n);
  let p = 0, u = 0, x = 0, t = 0;
  const k1 = [0, 0, 0], k2 = [0, 0, 0], k3 = [0, 0, 0], k4 = [0, 0, 0];
  for (let k = 0; k < n; k++) {
    for (let s = 0; s < sub; s++) {
      nlRhs(t, p, u, x, src(t), k1);
      nlRhs(t + hh / 2, p + hh / 2 * k1[0], u + hh / 2 * k1[1], x + hh / 2 * k1[2], src(t + hh / 2), k2);
      nlRhs(t + hh / 2, p + hh / 2 * k2[0], u + hh / 2 * k2[1], x + hh / 2 * k2[2], src(t + hh / 2), k3);
      nlRhs(t + hh, p + hh * k3[0], u + hh * k3[1], x + hh * k3[2], src(t + hh), k4);
      p += hh / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
      u += hh / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
      x += hh / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]);
      t += hh;
    }
    nlRhs(t, p, u, x, src(t), k1);
    X[k] = x; A[k] = k1[1];
  }
  return { X, A };
}
function dftBin(sig, i0, i1, bin) {                 // one-sided amplitude of a single DFT bin over sig[i0, i1)
  const N = i1 - i0; let re = 0, im = 0;
  for (let k = 0; k < N; k++) { const ph = TAU * bin * k / N; re += sig[i0 + k] * Math.cos(ph); im -= sig[i0 + k] * Math.sin(ph); }
  return { amp: 2 * Math.hypot(re, im) / N, re: 2 * re / N, im: 2 * im / N };
}
/* one tone: settle 40 periods, analyse 10 (256 samples/period, 4 sub-steps), as tone_run() in p11.py */
function nlTone(f0, V, settle = 40, keep = 10, per = 256) {
  const fsamp = f0 * per, n = (settle + keep) * per;
  const { X, A } = nlSimulate(t => V * Math.sin(TAU * f0 * t), fsamp, n);
  const i0 = settle * per, i1 = n;
  const a = [], xh = [];
  for (let k = 1; k <= 5; k++) { a.push(dftBin(A, i0, i1, k * keep).amp); xh.push(dftBin(X, i0, i1, k * keep)); }
  let mx = -Infinity, mn = Infinity, dc = 0;
  for (let k = i0; k < i1; k++) { mx = Math.max(mx, X[k]); mn = Math.min(mn, X[k]); dc += X[k]; }
  dc /= (i1 - i0);
  const thd = Math.sqrt(a.slice(1).reduce((s, v) => s + v * v, 0)) / a[0];
  return { xpk: (mx - mn) / 2, dc, h: a.map(v => v / a[0]), thd, x: X.slice(i0, i0 + 2 * per), x1: xh[0], fsamp, per };
}
/* two tones: V1 at f1 + V2 at 1 kHz, 1.5 s at 25.6 kHz, last 0.5 s analysed (f1 even → whole periods) */
function nlTwoTone(f1, V1, f2 = 1000, V2 = 2) {
  const fsamp = 25600, n = Math.round(1.5 * fsamp), N = Math.round(0.5 * fsamp), i0 = n - N, df = fsamp / N;
  const { A } = nlSimulate(t => V1 * Math.sin(TAU * f1 * t) + V2 * Math.sin(TAU * f2 * t), fsamp, n);
  const amp = (f) => dftBin(A, i0, n, Math.round(f / df)).amp;
  const a2 = amp(f2);
  const spec = [];
  for (let f = 800; f <= 1200; f += df) spec.push([f, amp(f)]);
  return { im2: (amp(f2 - f1) + amp(f2 + f1)) / a2, im3: (amp(f2 - 2 * f1) + amp(f2 + 2 * f1)) / a2, spec, a2 };
}

/* ===== L11 bench 1 · directivity of a baffled piston ===== */
function benchPiston() {
  const b = bench("bench-piston", "When the piston is not small: 2J₁(ka sin θ)/(ka sin θ)", "lecture 11 · §1 · Beranek 13.7");
  if (!b) return;
  const st = { f: 1500, a: L11_AW };
  const stage = h("div", { style: "display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:14px;align-items:center" });
  const polar = h("div"), cap = h("div", { class: "small" }), side = h("div");
  stage.append(polar, cap); b.plot.append(stage, side);
  const presets = [["System D woofer 105.5 mm", L11_AW], ["5¼″ mid 52.5 mm", 0.0525], ["1″ dome 12.5 mm", 0.0125]];
  const chips = h("div", { class: "chips" });
  for (const [n, v] of presets) chips.append(h("button", { type: "button", class: "chip ac" + (v === st.a ? " on" : ""), onclick: (e) => { st.a = v; sa.set(v * 1000); $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, n));
  b.ctl.append(chips);
  const sf = slider(b.ctl, { label: "frequency <b>f</b>", min: 50, max: 10000, value: st.f, log: true, dom: "ac", fmt: v => hz(v), onchange: v => { st.f = v; upd(); } });
  const sa = slider(b.ctl, { label: "piston radius <b>a</b>", min: 5, max: 200, step: 0.5, value: st.a * 1000, unit: "mm", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.a = v / 1000; $$(".chip", chips).forEach(x => x.classList.remove("on")); upd(); } });
  const ro = readouts(b.ctl, [{ id: "ka", label: "ka", dom: "ac" }, { id: "f1", label: "ka = 1 at", dom: "ac" }, { id: "fn", label: "first null at 90° above" }, { id: "bw", label: "−6 dB beamwidth" }, { id: "d", label: "level at 30° / 90°" }, { id: "rr", label: "Rayleigh distance πa²/λ" }, { id: "ma", label: "air mass per face (M<sub>A1</sub>·S²)", dom: "me" }]);
  const pf = new Plot(side, { h: 260, xmin: 50, xmax: 10000, ymin: -40, ymax: 3, ylabel: "level re on-axis (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const ANG = [[30, DOMC.ac], [60, DOMC.me], [90, DOMC.el]];
  function upd() {
    const n = pistonNumbers(st.f, st.a);
    const toR = (v) => Math.max(0, (dB(Math.abs(v)) + 40) / 40);
    polar.innerHTML = polarSVG([{ fn: t => Math.cos(t) >= -1e-9 ? toR(pistonDir(n.ka, t)) : 0, color: DOMC.ac, fill: 0.14 }], { w: 300 });
    cap.innerHTML = `<p><b>Polar:</b> front half-space at ${hz(st.f)}, 0° = on axis, rings 10 dB apart (outer 0 dB, centre −40 dB). The baffle is the 90°–270° line; nothing goes behind it.</p><p><b>Below:</b> level at 30°, 60° and 90° against frequency for this radius. All three sit on 0 dB until ka ≈ 1, then the 90° curve dives first and reaches its null at ka = 3.83.</p>`;
    const fs = logspace(50, 10000, 400);
    pf.set({ series: ANG.map(([d, col]) => ({ name: `${d}°`, color: col, pts: fs.map(f => [f, Math.max(-60, dB(Math.abs(pistonDir(TAU * f / L11.c * st.a, d * Math.PI / 180))))]) })),
      vlines: [{ x: n.f1, label: "ka = 1", color: DOMC.warn }, { x: n.fnull, label: "null at 90°", color: DOMC.ink3 }, { x: st.f, label: "f", color: DOMC.ink }] });
    const S = Math.PI * st.a * st.a;
    ro({ ka: n.ka.toFixed(2), f1: hz(n.f1), fn: hz(n.fnull), bw: n.bw === null ? "wider than ±90° (no −6 dB point)" : `±${n.bw.toFixed(0)}°`,
      d: `${n.d30.toFixed(1)} / ${n.d90 < -60 ? "null" : n.d90.toFixed(1)} dB`, rr: `${(n.rR * 100).toFixed(1)} cm${n.rmax > 0 ? `, last axial max ${(n.rmax * 100).toFixed(1)} cm` : ", no axial max (λ > 2a)"}`,
      ma: `${(n.MA1 * S * S * 1000).toFixed(2)} g (M_A1 ${n.MA1.toFixed(2)} kg/m⁴)` });
  }
  upd();
  b.note.innerHTML = `<p>Start values: the System D woofer (S<sub>D</sub> 350 cm², a = 105.5 mm) at 1.5 kHz. <b>ka = 1</b> (circumference = wavelength) at <b>517 Hz</b>; below that the pattern is a half-circle. A null at 90° first exists when ka = 3.832, above <b>1983 Hz</b>. The −6 dB beamwidth is ±50° at 1.5 kHz, ±35° at 2 kHz, ±22° at 3 kHz, all as in p11.py. The right plot is the level at 30°, 60° and 90° against frequency: the 30° curve at 3 kHz reads −11.7 dB, the number to hold against Lab E's measured −15.6 dB.</p><p><b>Try:</b> pick the 1″ dome: its ka = 1 sits at 4.4 kHz, which is why a tweeter can take over where the woofer starts to beam. Then drag f to 325 Hz (the project's crossover) with the woofer: ka = 0.63, still omni.</p>`;
}

/* ===== L11 bench 2 · walls, baffle step, room ===== */
function benchSpace() {
  const b = bench("bench-space11", "Where you put it: solid angle, baffle step and the room", "lecture 11 · §2");
  if (!b) return;
  const st = { om: 2 * Math.PI, W: 0.45, V: 100, T: 0.5 };
  const chips = h("div", { class: "chips" });
  for (const [n, om, s] of L11_SPACES) chips.append(h("button", { type: "button", class: "chip ac" + (om === st.om ? " on" : ""), onclick: (e) => { st.om = om; $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, `${n} (${s})`));
  b.ctl.append(chips);
  slider(b.ctl, { label: "box front width <b>W</b>", min: 0.1, max: 1.2, step: 0.01, value: st.W, unit: "m", dom: "me", fmt: v => v.toFixed(2), onchange: v => { st.W = v; upd(); } });
  slider(b.ctl, { label: "room volume <b>V</b>", min: 20, max: 2000, value: st.V, log: true, unit: "m³", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.V = v; upd(); } });
  slider(b.ctl, { label: "reverberation time <b>T₆₀</b>", min: 0.2, max: 3, step: 0.05, value: st.T, unit: "s", dom: "ac", fmt: v => v.toFixed(2), onchange: v => { st.T = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "spl", label: "SPL vs free field", dom: "ac" }, { id: "pow", label: "radiated power vs free field", dom: "ac" }, { id: "fs", label: "baffle step f = c/πW", dom: "me" }, { id: "A", label: "absorption area A = 0.161V/T" }, { id: "rc", label: "critical distance r<sub>c</sub> (Q from Ω)" }]);
  const pb = new Plot(b.plot, { h: 220, xmin: 20, xmax: 5000, ymin: -8, ymax: 2, ylabel: "box on axis re 2π (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const pr = new Plot(b.plot, { h: 220, xmin: 0.1, xmax: 30, ymin: -40, ymax: 10, xlabel: "distance r", xfmt: v => (v < 1 ? (v * 100).toFixed(0) + " cm" : v.toFixed(v < 10 ? 1 : 0) + " m"), ylabel: "L_p − L_W (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const g = spaceGain(st.om), fst = baffleStepF(st.W), rm = roomNumbers(st.V, st.T, g.Q);
    const fs = logspace(20, 5000, 300);
    // first-order shelf: 4π (−6 dB) well below c/πW, 2π (0 dB) well above; the edge-diffraction ripple is left out
    const shelf = (f) => dB(cabs(cdiv(cx(1, 2 * f / fst), cx(2, 2 * f / fst))));
    pb.set({ series: [{ name: "first-order baffle step", color: DOMC.me, pts: fs.map(f => [f, shelf(f)]) }, { name: "4π level", color: DOMC.ink3, thin: true, dash: "4 4", pts: [[20, -6], [5000, -6]] }],
      vlines: [{ x: fst, label: "c/πW", color: DOMC.warn }] });
    const rs = logspace(0.1, 30, 300);
    const lp = (r, Q) => 10 * Math.log10(Q / (4 * Math.PI * r * r) + 4 / rm.A);
    pr.set({ series: [{ name: "direct + reverberant", color: DOMC.ac, width: 2.4, pts: rs.map(r => [r, lp(r, g.Q)]) }, { name: "direct only", color: DOMC.ink3, thin: true, dash: "5 4", pts: rs.map(r => [r, 10 * Math.log10(g.Q / (4 * Math.PI * r * r))]) }, { name: "reverberant 4/A", color: DOMC.ink3, thin: true, dash: "2 3", pts: [[0.1, 10 * Math.log10(4 / rm.A)], [30, 10 * Math.log10(4 / rm.A)]] }],
      vlines: [{ x: rm.rc, label: "r_c", color: DOMC.warn }] });
    ro({ spl: `+${g.spl.toFixed(1)} dB`, pow: `+${g.pow.toFixed(1)} dB`, fs: hz(fst), A: `${rm.A.toFixed(1)} m² sabine`, rc: `${rm.rc.toFixed(2)} m (Q = ${g.Q.toFixed(0)})` });
  }
  upd();
  b.note.innerHTML = `<p>A small source with fixed volume velocity U into a solid angle Ω gives <span class="mono">p = jωρU/(Ωr)</span> and <span class="mono">R_A = ρck²/Ω</span>. Halve Ω and the pressure doubles (+6 dB) <i>and</i> the power doubles (+3 dB), because the image source in the wall doubles the radiation resistance the source works into. Corner: +18 dB SPL, +9 dB power. The System D box (W = 0.45 m) steps at <b>243 Hz</b>; the plot is the textbook first-order shelf, without the edge-diffraction ripple Lab E measured on top. The room plot uses the start values V = 100 m³, T₆₀ = 0.5 s: A = 32.2 m², r<sub>c</sub> = 0.80 m (Q = 1), 1.13 m (Q = 2), 1.60 m (Q = 4).</p><p><b>Try:</b> switch to the corner: the critical distance grows to 1.60 m, so the direct sound dominates further out. Beyond r<sub>c</sub> the listener hears the <b>power</b> response, not the on-axis one.</p>`;
}

/* ===== L11 bench 3 · micro-speaker ===== */
function benchMicroSpk() {
  const b = bench("bench-microspk", "A phone speaker: excursion for the bass, a Helmholtz low-pass in front", "lecture 11 · §3 · Beranek ch. 8");
  if (!b) return;
  const st = { Lp: 90, r: 0.10, Sd: Math.PI * MICRO.a ** 2, xmax: 0.4e-3, Vb: 1.0e-6, Vf: 0.10e-6, ah: 0.6e-3, lh: 0.8e-3, Q: 3 };
  slider(b.ctl, { label: "target SPL", min: 70, max: 110, step: 1, value: st.Lp, unit: "dB", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.Lp = v; upd(); } });
  slider(b.ctl, { label: "at distance <b>r</b> (2π, phone on a table)", min: 2, max: 50, step: 1, value: 10, unit: "cm", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.r = v / 100; upd(); } });
  slider(b.ctl, { label: "diaphragm area <b>S<sub>D</sub></b>", min: 0.3, max: 4, step: 0.01, value: st.Sd * 1e4, unit: "cm²", dom: "me", fmt: v => v.toFixed(2), onchange: v => { st.Sd = v * 1e-4; upd(); } });
  slider(b.ctl, { label: "excursion limit <b>x<sub>max</sub></b>", min: 0.1, max: 1, step: 0.05, value: 0.4, unit: "mm", dom: "me", fmt: v => v.toFixed(2), onchange: v => { st.xmax = v * 1e-3; upd(); } });
  slider(b.ctl, { label: "back volume <b>V<sub>B</sub></b>", min: 0.2, max: 5, step: 0.05, value: 1, unit: "cm³", dom: "ac", fmt: v => v.toFixed(2), onchange: v => { st.Vb = v * 1e-6; upd(); } });
  slider(b.ctl, { label: "front cavity <b>V<sub>F</sub></b>", min: 0.02, max: 0.5, step: 0.01, value: 0.10, unit: "cm³", dom: "ac", fmt: v => v.toFixed(2), onchange: v => { st.Vf = v * 1e-6; upd(); } });
  slider(b.ctl, { label: "sound-hole radius", min: 0.2, max: 1.5, step: 0.05, value: 0.6, unit: "mm", dom: "ac", fmt: v => v.toFixed(2), onchange: v => { st.ah = v * 1e-3; upd(); } });
  slider(b.ctl, { label: "Q of the hole (dust screen, illustrative)", min: 0.5, max: 8, step: 0.1, value: st.Q, dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.Q = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "x200", label: "x<sub>peak</sub> at 200 Hz", dom: "me" }, { id: "x1k", label: "x<sub>peak</sub> at 1 kHz", dom: "me" }, { id: "fmin", label: "lowest f within x<sub>max</sub>", dom: "me" }, { id: "fc", label: "f<sub>s</sub> 800 Hz → f<sub>c</sub> in the back volume", dom: "ac" }, { id: "f0", label: "front Helmholtz f₀", dom: "ac" }, { id: "mc", label: "M<sub>AH</sub>, C<sub>AF</sub>" }]);
  const px = new Plot(b.plot, { h: 240, xmin: 50, xmax: 10000, ymin: -3, ymax: 1.5, yticks: [-3, -2, -1, 0, 1], ylabel: "peak excursion (mm, log)", yfmt: v => { const x = Math.pow(10, v); return x >= 1 ? x.toFixed(1) : x >= 0.01 ? x.toFixed(3) : x.toExponential(1); }, yunit: " mm" });
  const ph = new Plot(b.plot, { h: 200, xmin: 200, xmax: 20000, ymin: -30, ymax: 20, ylabel: "front cavity + hole (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const fs = logspace(50, 10000, 300);
    const x200 = microX(200, st.Lp, st.r, st.Sd), x1k = microX(1000, st.Lp, st.r, st.Sd);
    const fmin = 1000 * Math.sqrt(x1k / st.xmax);
    px.set({ series: [{ name: "needed x_peak", color: DOMC.me, width: 2.4, pts: fs.map(f => [f, Math.log10(microX(f, st.Lp, st.r, st.Sd) * 1e3)]) }, { name: "x_max", color: DOMC.warn, thin: true, dash: "5 4", pts: [[50, Math.log10(st.xmax * 1e3)], [10000, Math.log10(st.xmax * 1e3)]] }],
      regions: [{ from: 50, to: fmin, label: "excursion-limited", color: "var(--me-soft)" }], markers: [{ x: 200, y: Math.log10(x200 * 1e3), label: `${(x200 * 1e3).toFixed(2)} mm`, color: DOMC.me }, { x: 1000, y: Math.log10(x1k * 1e3), label: `${(x1k * 1e3).toFixed(3)} mm`, color: DOMC.me }] });
    const bx = microBox(st.Sd, st.Vb), hm = microHelm(st.Vf, st.ah, st.lh);
    const fh = logspace(200, 20000, 300);
    ph.set({ series: [{ name: "1/(1 − (f/f₀)² + jf/(Qf₀))", color: DOMC.ac, pts: fh.map(f => [f, dB(1 / cabs(cx(1 - (f / hm.f0) ** 2, f / (st.Q * hm.f0))))]) }], vlines: [{ x: hm.f0, label: "f₀", color: DOMC.warn }] });
    ro({ x200: `${(x200 * 1e3).toFixed(3)} mm`, x1k: `${(x1k * 1e3).toFixed(3)} mm`, fmin: hz(fmin), fc: `${hz(bx.fc)} (V_AS ${(bx.Vas * 1e6).toFixed(2)} cm³, α ${bx.alpha.toFixed(2)})`, f0: hz(hm.f0), mc: `${hm.Mah.toFixed(0)} kg/m⁴, ${sci(hm.Caf)} m⁵/N` });
  }
  upd();
  b.note.innerHTML = `<p>The values are illustrative (a typical 15 × 11 mm unit, as in p11.py), the mechanisms are Beranek's. For a fixed SPL the cone has to move a fixed <b>volume acceleration</b>, so the excursion grows as 1/f²: <span class="mono">x<sub>peak</sub> = √2·p·Ωr/(ρω²S<sub>D</sub>)</span>. At 90 dB and 10 cm with S<sub>D</sub> = 1.21 cm²: <b>2.45 mm at 200 Hz</b> (impossible), <b>0.098 mm at 1 kHz</b>. The 1 cm³ back volume lifts f<sub>s</sub> = 800 Hz to <b>f<sub>c</sub> = 1057 Hz</b> (V<sub>AS</sub> = 0.74 cm³), and the 0.1 cm³ front cavity with a 1.2 mm × 0.8 mm hole is a Helmholtz low-pass at <b>4306 Hz</b>. The Q of the hole is not in the pre-read; the slider only shows what the dust screen does.</p><p><b>Try:</b> double S<sub>D</sub>: the excursion halves, so the lowest usable frequency drops by only √2. Bass from a phone costs area or excursion, and a phone has neither, which is why a smart amplifier models x(t) and limits it.</p>`;
}

/* ===== L11 bench 4 · nonlinear woofer, solved in time ===== */
function benchNonlinear() {
  const b = bench("bench-nonlin", "Large signal: Bl(x), K(x), Le(x), solved in time with RK4", "lecture 11 · §4 · Beranek 6.18, Klippel");
  if (!b) return;
  const st = { f: 20, V: 10, two: false };
  const chips = h("div", { class: "chips" });
  chips.append(h("button", { type: "button", class: "chip el on", onclick: (e) => { st.two = false; $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, "one tone (harmonics)"),
    h("button", { type: "button", class: "chip el", onclick: (e) => { st.two = true; $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, "+ 2 V at 1 kHz (IMD)"));
  b.ctl.append(chips);
  slider(b.ctl, { label: "drive voltage <b>V</b> (peak)", min: 0.5, max: 25, step: 0.5, value: st.V, unit: "V", dom: "el", fmt: v => v.toFixed(1), onchange: v => { st.V = v; sched(); } });
  slider(b.ctl, { label: "frequency <b>f</b>", min: 10, max: 200, step: 2, value: st.f, unit: "Hz", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.f = v; sched(); } });
  const ro = readouts(b.ctl, [{ id: "xpk", label: "x<sub>peak</sub> (X<sub>max</sub> = 6 mm)", dom: "me" }, { id: "dc", label: "DC offset of x", dom: "me" }, { id: "h2", label: "H2 / H3", dom: "ac" }, { id: "thd", label: "THD (H2–H5)", dom: "ac" }, { id: "im", label: "IMD sidebands f₂ ± f₁ / f₂ ± 2f₁" }]);
  const pw = new Plot(b.plot, { h: 220, xlog: false, xmin: 0, xmax: 2, ymin: -15, ymax: 15, xlabel: "time (periods)", ylabel: "x (mm), + = outward", xfmt: v => v.toFixed(2), yfmt: v => v.toFixed(2), yunit: " mm" });
  const ps = new Plot(b.plot, { h: 200, xlog: false, xmin: 0.5, xmax: 5.5, ymin: -80, ymax: 0, xticks: [1, 2, 3, 4, 5].map(v => ({ v, l: v === 1 ? "f" : v + "f" })), xlabel: "harmonic of the cone acceleration (= far-field pressure)", ylabel: "dB re fundamental", xfmt: v => v.toFixed(0) + "·f", yfmt: v => v.toFixed(1), yunit: " dB" });
  const pp = new Plot(b.plot, { h: 180, xlog: false, xmin: -12, xmax: 12, ymin: 0.4, ymax: 1.4, xlabel: "x (mm), + = outward", ylabel: "re small-signal value", xfmt: v => v.toFixed(1) + " mm", yfmt: v => v.toFixed(3) });
  let pending = false;
  function sched() { if (pending) return; pending = true; setTimeout(() => { pending = false; upd(); }, 0); }
  const stems = (pts) => pts.flatMap(([x, y]) => [[x, -200], [x, y], [x, NaN]]);
  function upd() {
    const r = nlTone(st.f, st.V);
    const tt = Array.from(r.x, (_, k) => k / r.per);
    const ymax = Math.max(2, Math.ceil(Math.max(...Array.from(r.x, v => Math.abs(v))) * 1e3 * 1.15));
    pw.set({ ymin: -ymax, ymax, series: [
      { name: "x(t), nonlinear", color: DOMC.me, width: 2.4, pts: tt.map((t, k) => [t, r.x[k] * 1e3]) },
      { name: "fundamental + DC only", color: DOMC.ink3, thin: true, dash: "5 4", pts: tt.map(t => [t, (r.dc + r.x1.re * Math.cos(TAU * t) - r.x1.im * Math.sin(TAU * t)) * 1e3]) },
      { name: "±X_max", color: DOMC.warn, thin: true, dash: "2 3", pts: [[0, 6], [2, 6], [2, NaN], [0, -6], [2, -6]] }] });
    const xs = linspace(-12e-3, 12e-3, 241), lo = r.dc - r.xpk, hi = r.dc + r.xpk;
    pp.set({ series: [{ name: "Bl(x)/Bl₀", color: DOMC.el, pts: xs.map(x => [x * 1e3, nlBl(x) / NL.BL0]) }, { name: "C_MS(x)/C_MS0", color: DOMC.me, pts: xs.map(x => [x * 1e3, NL.K0 / nlK(x)]) }, { name: "Le(x)/Le₀", color: DOMC.ac, pts: xs.map(x => [x * 1e3, nlLe(x) / NL.LE0]) }],
      regions: [{ from: lo * 1e3, to: hi * 1e3, label: "swept", color: "var(--me-soft)" }], vlines: [{ x: -6, label: "−X_max", color: DOMC.ink3 }, { x: 6, label: "X_max", color: DOMC.ink3 }] });
    let im = "switch on the second tone";
    if (st.two) {
      const t2 = nlTwoTone(st.f, st.V);
      ps.set({ xmin: 800, xmax: 1200, xticks: null, xlabel: "frequency near f₂ = 1 kHz (acceleration spectrum)", xfmt: v => v.toFixed(0) + " Hz", series: [{ name: "spectrum re the 1 kHz line", color: DOMC.ac, pts: stems(t2.spec.map(([f, a]) => [f, Math.max(-79.9, dB(a / t2.a2))])) }] });
      im = `${(t2.im2 * 100).toFixed(2)} % / ${(t2.im3 * 100).toFixed(2)} %`;
    } else {
      ps.set({ xmin: 0.5, xmax: 5.5, xticks: [1, 2, 3, 4, 5].map(v => ({ v, l: v === 1 ? "f" : v + "f" })), xlabel: "harmonic of the cone acceleration (= far-field pressure)", xfmt: v => v.toFixed(0) + "·f", series: [{ name: "harmonics", color: DOMC.ac, width: 4, pts: stems(r.h.map((v, k) => [k + 1, Math.max(-79.9, dB(v))])) }] });
    }
    ro({ xpk: `${(r.xpk * 1e3).toFixed(2)} mm`, dc: `${(r.dc * 1e3).toFixed(2)} mm`, h2: `${(r.h[1] * 100).toFixed(2)} % / ${(r.h[2] * 100).toFixed(2)} %`, thd: `${(r.thd * 100).toFixed(2)} %`, im });
  }
  upd();
  b.note.innerHTML = `<p>The System D woofer (Scan-Speak 26W/8534G00, Lab D fit: Bl 8.28 T·m, M<sub>MS</sub> 44.3 g in a baffle, C<sub>MS</sub> 1.174 mm/N, f<sub>s</sub> 22.1 Hz) with <b>assumed</b> shapes: Bl falls to 82 % at ±6 mm (centred 0.5 mm outward), C<sub>MS</sub> to 71 % outward and 80 % inward, Le 1.80 mH inward, 1.20 mH outward. The state is (ψ = Le·i, u, x), integrated with RK4 exactly as p11.py does: 256 samples per period, 4 sub-steps, 40 periods to settle, 10 analysed. It reproduces the script: <b>20 Hz, 10 V → x 8.97 mm, H3 36.7 %, THD 37.3 %</b>; <b>40 Hz, 10 V → THD 3.66 %</b>; the two-tone 10 V at 40 Hz + 2 V at 1 kHz gives sidebands of <b>14.3 %</b> (±40 Hz) and <b>4.4 %</b> (±80 Hz): switch on the second tone and set f = 40 Hz.</p><p><b>Try:</b> keep 10 V and go from 20 to 100 Hz: x shrinks ten-fold and the distortion goes with it. Distortion is a large-excursion, low-frequency problem. Below f<sub>s</sub> the cone moves 1.71 mm per volt, so X<sub>max</sub> is reached at only 3.5 V. The symmetric Bl drop gives mostly H3; the offsets and Le(x) give H2 and pull the mean position inward (negative DC).</p>`;
}

/* ===== boot ===== */
document.addEventListener("DOMContentLoaded", () => {
  benchPiston(); benchSpace(); benchMicroSpk(); benchNonlinear();
});
