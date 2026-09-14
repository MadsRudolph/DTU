/* The Sound Bench — playgrounds for 34840, lectures 1–3.
   Constants follow the problem sheets: c = 343 m/s, ρ = 1.204 kg/m³ (ρc = 413), γ = 1.401. */
"use strict";

const CA = 343, RHOA = 1.204, ZAIR = 413, GAMMA = 1.401, P0 = 101.3e3, RS = 287.05, PREF = 20e-6;
const LP = (prms) => 20 * Math.log10(Math.max(prms, 1e-30) / PREF);
const segCtl = (ctl, st, key, opts, upd) => { const seg = h("div", { class: "seg" }); for (const [k, l] of opts) seg.append(h("button", { type: "button", class: st[key] === k ? "on" : "", onclick: (e) => { st[key] = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l)); ctl.append(seg); return seg; };

/* ===== L1 · travelling plane wave with particle motion ===== */
function benchWave() {
  const b = bench("bench-wave", "A plane wave: the pattern moves at c, the air only wobbles", "lecture 1 · problem 1");
  if (!b) return;
  const st = { f: 1000, p: 1, dir: 1, run: true };
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  slider(b.ctl, { label: "frequency <b>f</b>", min: 100, max: 3000, step: 10, value: 1000, unit: "Hz", dom: "el", onchange: v => { st.f = v; ro_(); } });
  slider(b.ctl, { label: "pressure amplitude <b>p̂</b>", min: 0.1, max: 10, step: 0.1, value: 1, unit: "Pa", dom: "el", fmt: v => v.toFixed(1), onchange: v => { st.p = v; ro_(); } });
  segCtl(b.ctl, st, "dir", [[1, "travels +x"], [-1, "travels −x"]], () => { });
  const ro = readouts(b.ctl, [{ id: "lam", label: "wavelength λ = c/f", dom: "el" }, { id: "k", label: "wavenumber k = 2π/λ", dom: "el" }, { id: "u", label: "particle velocity |u| = p̂/ρc", dom: "me" }, { id: "xi", label: "displacement |ξ| = |u|/ω", dom: "me" }, { id: "T", label: "period" }]);
  function ro_() { const lam = CA / st.f, k = TAU / lam, u = st.p / ZAIR, xi = u / (TAU * st.f); ro({ lam: `${(lam * 100).toFixed(1)} cm`, k: `${k.toFixed(1)} rad/m`, u: `${(u * 1e3).toFixed(2)} mm/s`, xi: `${(xi * 1e6).toFixed(3)} µm`, T: `${(1000 / st.f).toFixed(2)} ms` }); }
  ro_();
  let t0 = performance.now();
  function frame(now) {
    if (!stage.isConnected) return;
    const t = (now - t0) / 1000 * 0.35; // slowed-down time
    const W = 640, H = 250, x0 = 30, x1 = 610, mid = 95, lam = CA / st.f, px = (x1 - x0) / 1.0; // 1 m across the stage
    const k = TAU / lam, phase = (x) => TAU * st.f * t * 0.001 * st.dir * -1 + k * x; // wave shape moves with time
    let d = ""; for (let i = 0; i <= 200; i++) { const x = i / 200, y = mid - 60 * Math.cos(TAU * st.f * t / 200 - st.dir * k * x); d += (i ? "L" : "M") + (x0 + x * px).toFixed(1) + " " + y.toFixed(1); }
    let dots = ""; for (let i = 0; i < 48; i++) { const x = (i + 0.5) / 48, disp = 6 * Math.cos(TAU * st.f * t / 200 - st.dir * k * x) * st.dir; const X = x0 + x * px + disp; const dens = Math.cos(TAU * st.f * t / 200 - st.dir * k * x); dots += `<circle cx="${X.toFixed(1)}" cy="200" r="${(4 + 2 * dens).toFixed(1)}" fill="var(--me)" opacity="${(0.45 + 0.4 * dens).toFixed(2)}"/>`; }
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">
      <line x1="${x0}" x2="${x1}" y1="${mid}" y2="${mid}" stroke="var(--plot-grid)"/>
      <path d="${d}" fill="none" stroke="var(--el)" stroke-width="2.5"/>
      <text x="${x0}" y="22" font-size="11" fill="var(--el)">sound pressure p(x, t) — the pattern travels at c = 343 m/s ${st.dir > 0 ? "→" : "←"}</text>
      <text x="${x1}" y="${mid + 4}" text-anchor="end" font-size="10" fill="var(--ink-3)">x = 1 m</text>
      <line x1="${x0}" x2="${x1}" y1="200" y2="200" stroke="var(--plot-grid)"/>
      ${dots}
      <text x="${x0}" y="175" font-size="11" fill="var(--me)">air particles — they only oscillate about their rest position (longitudinal), amplitude |ξ| = ${(st.p / ZAIR / (TAU * st.f) * 1e6).toFixed(2)} µm (exaggerated here)</text>
      <text x="${x0}" y="238" font-size="10" fill="var(--ink-3)">λ = ${(lam * 100).toFixed(1)} cm — count the crests across the metre; time is slowed by 1000×</text>
    </svg>`;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  b.note.innerHTML = `<p>Two different speeds. The <b>pattern</b> moves at the speed of sound, 343 m/s. The <b>particles</b> shuffle back and forth along the direction of travel with velocity <span class="mono">u = p/ρc</span> — for 1 Pa that is 2.4 mm/s, and the displacement is under a micrometre. Where the particles bunch up the pressure is high: pressure and velocity are <b>in phase</b> in a wave travelling one way.</p><p>Doubling the frequency halves the wavelength; the particle velocity does not change (it depends on pressure only), but the displacement halves, because <span class="mono">ξ = u/(jω)</span>. That is why you can <em>see</em> a subwoofer cone move and not a tweeter's.</p>`;
}

/* ===== L1 · adding two coherent sources ===== */
function benchPhasorSum() {
  const b = bench("bench-phasors", "Two loudspeakers, one tone: add the phasors, not the amplitudes", "lecture 1 · problem 2 · lecture 3 · problem 1.2");
  if (!b) return;
  const st = { a1: 0.5, a2: 0.5, th: 90 };
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  slider(b.ctl, { label: "source 1 amplitude", min: 0, max: 1, step: 0.01, value: 0.5, unit: "Pa", dom: "el", fmt: v => v.toFixed(2), onchange: v => { st.a1 = v; upd(); } });
  slider(b.ctl, { label: "source 2 amplitude", min: 0, max: 1, step: 0.01, value: 0.5, unit: "Pa", dom: "el", fmt: v => v.toFixed(2), onchange: v => { st.a2 = v; upd(); } });
  slider(b.ctl, { label: "phase lag of source 2 <b>θ</b>", min: 0, max: 360, step: 1, value: 90, unit: "°", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.th = v; upd(); } });
  const chips = h("div", { class: "chips" }); for (const v of [0, 90, 120, 179, 180]) chips.append(h("button", { type: "button", class: "chip", onclick: () => { st.th = v; sl.set(v); upd(); } }, `${v}°`)); b.ctl.append(chips);
  const sl = { set: (v) => { const inp = $$("input[type=range]", b.ctl)[2]; inp.value = v; inp.dispatchEvent(new Event("input")); } };
  const ro = readouts(b.ctl, [{ id: "sum", label: "|p₁ + p₂|", dom: "el" }, { id: "lvl", label: "level (peak → rms → dB)", dom: "ac" }, { id: "unc", label: "if uncorrelated instead" }]);
  function upd() {
    const th = -st.th * Math.PI / 180, p1 = cx(st.a1, 0), p2 = cx(st.a2 * Math.cos(th), st.a2 * Math.sin(th)), s = cadd(p1, p2), mag = cabs(s);
    const W = 640, H = 300, cxp = 220, cyp = 150, sc = 130;
    const arrow = (v, col, lbl, w = 3) => { const x = cxp + v.re * sc, y = cyp - v.im * sc; return `<line x1="${cxp}" y1="${cyp}" x2="${x}" y2="${y}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/><circle cx="${x}" cy="${y}" r="4" fill="${col}"/><text x="${x + 8}" y="${y - 6}" font-size="12" fill="${col}">${lbl}</text>`; };
    const x1 = cxp + p1.re * sc, y1 = cyp - p1.im * sc;
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">
      <circle cx="${cxp}" cy="${cyp}" r="${sc}" fill="none" stroke="var(--plot-grid)"/><circle cx="${cxp}" cy="${cyp}" r="${sc / 2}" fill="none" stroke="var(--plot-grid)"/>
      <line x1="${cxp - sc - 10}" x2="${cxp + sc + 10}" y1="${cyp}" y2="${cyp}" stroke="var(--plot-grid)"/><line y1="${cyp - sc - 10}" y2="${cyp + sc + 10}" x1="${cxp}" x2="${cxp}" stroke="var(--plot-grid)"/>
      <text x="${cxp + sc + 4}" y="${cyp - 4}" font-size="10" fill="var(--ink-3)">1 Pa</text>
      <line x1="${x1}" y1="${y1}" x2="${x1 + p2.re * sc}" y2="${y1 - p2.im * sc}" stroke="var(--me)" stroke-width="2" stroke-dasharray="4 3" opacity="0.7"/>
      ${arrow(p1, "var(--el)", "p₁")}${arrow(p2, "var(--me)", "p₂ (lags θ)")}${arrow(s, "var(--ink)", "p₁ + p₂", 4)}
      <text x="400" y="60" font-size="13" fill="var(--ink)">p₁ + p₂ = ${st.a1.toFixed(2)} + ${st.a2.toFixed(2)}·e<tspan font-size="9" dy="-6">−j${st.th}°</tspan></text>
      <text x="400" y="86" font-size="13" fill="var(--ink)">= ${s.re.toFixed(3)} ${s.im < 0 ? "−" : "+"} j${Math.abs(s.im).toFixed(3)} Pa</text>
      <text x="400" y="112" font-size="13" fill="var(--ink)">|p₁ + p₂| = ${mag < 1e-3 ? (mag * 1000).toFixed(1) + " mPa" : mag.toFixed(3) + " Pa"}</text>
      <text x="400" y="140" font-size="11" fill="var(--ink-2)">equal amplitudes: |1 + e<tspan font-size="8" dy="-5">−jθ</tspan><tspan dy="5">| = 2|cos(θ/2)|</tspan></text>
      <text x="400" y="160" font-size="11" fill="var(--ink-2)">= ${(2 * Math.abs(Math.cos(th / 2))).toFixed(4)} × ${st.a1.toFixed(2)}</text>
    </svg>`;
    ro({ sum: mag < 1e-3 ? `${(mag * 1000).toFixed(2)} mPa` : `${mag.toFixed(3)} Pa`, lvl: `${LP(mag / Math.SQRT2).toFixed(1)} dB`, unc: `${(Math.hypot(st.a1, st.a2)).toFixed(3)} Pa · ${LP(Math.hypot(st.a1, st.a2) / Math.SQRT2).toFixed(1)} dB` });
  }
  upd();
  b.note.innerHTML = `<p>Same tone, same distance: the two pressures are <b>coherent</b>, so you add them as complex numbers and take the magnitude afterwards. In phase they double (+6 dB), at 90° you get √2 (+3 dB), at 180° they cancel completely — and at 179° a residual of 8.7 mPa survives, 41 dB below one source alone. <b>Different</b> tones (or any two independent sources) are uncorrelated: then the mean <em>squares</em> add, and two equal sources give +3 dB regardless of phase.</p>`;
}

/* ===== L1 · speed of sound, temperature, gas, pipe ===== */
function benchSpeed() {
  const b = bench("bench-speed", "Speed of sound: temperature, gas, and what it does to a pipe", "lecture 1 · problem 4 · lecture 2 · problem 2");
  if (!b) return;
  const st = { T: 20, gas: "air", L: 1.559 };
  const GAS = { air: { g: 1.401, R: 287.05, name: "air" }, helium: { g: 1.66, R: 2077, name: "helium" }, co2: { g: 1.30, R: 188.9, name: "CO₂" } };
  slider(b.ctl, { label: "temperature <b>T</b>", min: -20, max: 40, step: 0.5, value: 20, unit: "°C", fmt: v => v.toFixed(1), onchange: v => { st.T = v; upd(); } });
  segCtl(b.ctl, st, "gas", [["air", "air"], ["helium", "helium"], ["co2", "CO₂"]], () => upd());
  slider(b.ctl, { label: "open pipe length <b>L</b>", min: 0.2, max: 3, step: 0.001, value: 1.559, unit: "m", fmt: v => v.toFixed(3), onchange: v => { st.L = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "c", label: "c = √(γ R_s T)", dom: "el" }, { id: "rel", label: "relative to air at 20 °C" }, { id: "f0", label: "open pipe f₀ = c / 2L", dom: "ac" }, { id: "semi", label: "shift in semitones" }]);
  const plot = new Plot(b.plot, { h: 260, xlog: false, xmin: -20, xmax: 40, ymin: 300, ymax: 370, xlabel: "temperature (°C)", ylabel: "c in air (m/s)", xfmt: v => `${v}°`, yfmt: v => v.toFixed(0) });
  const ts = linspace(-20, 40, 61), cAir = (T) => Math.sqrt(1.401 * 287.05 * (T + 273.15));
  function upd() {
    const g = GAS[st.gas], c = Math.sqrt(g.g * g.R * (st.T + 273.15)), c20 = cAir(20), f0 = c / (2 * st.L);
    const fref = c20 / (2 * st.L);
    plot.set({ series: [{ name: "c in air", color: DOMC.el, pts: ts.map(T => [T, cAir(T)]) }], markers: st.gas === "air" ? [{ x: st.T, y: c, label: `${c.toFixed(1)} m/s at ${st.T} °C`, color: DOMC.el }] : [] });
    ro({ c: `${c.toFixed(1)} m/s (${g.name})`, rel: `× ${(c / c20).toFixed(3)}`, f0: `${f0.toFixed(1)} Hz`, semi: `${(12 * Math.log2(f0 / fref)).toFixed(2)} semitones vs air at 20 °C` });
  }
  upd();
  b.note.innerHTML = `<p><span class="mono">c = √(γ R_s T)</span> with T in <b>kelvin</b> — the single most common slip is using °C. Air at 15 °C vs 32 °C: ratio 1.029, so an organ pipe tuned to 110 Hz in summer plays 106.9 Hz in winter, a quarter-tone flat (log₂1.029 ≈ 1/24 octave). The pipe length is fixed; only c changes, and every resonance scales with it.</p><p>Helium at 1000 m/s (the sheet's value; the formula gives ≈ 1010) raises a trumpet's fundamental by 2.91×, about an octave and a fifth. Pick helium and the pipe readout shows it.</p>`;
}

/* ===== L2 · standing wave with a partial reflection ===== */
function benchStanding() {
  const b = bench("bench-standing", "Reflection: incident + reflected = a standing-wave envelope", "lecture 2 · problem 1 · §2, §4");
  if (!b) return;
  const st = { f: 1000, R: 1, ph: 0 };
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  const presets = h("div", { class: "chips" });
  for (const [n, R, ph] of [["rigid wall (R = +1)", 1, 0], ["pressure release (R = −1)", 1, 180], ["air → water (R = 0.9994)", 0.99944, 0], ["absorber (|R| = 0.5)", 0.5, 0], ["anechoic (R = 0)", 0, 0]]) presets.append(h("button", { type: "button", class: "chip", onclick: () => { st.R = R; st.ph = ph; sR.set(R); sP.set(ph); upd(); } }, n));
  b.ctl.append(presets);
  slider(b.ctl, { label: "frequency <b>f</b>", min: 200, max: 3000, step: 10, value: 1000, unit: "Hz", dom: "el", onchange: v => { st.f = v; upd(); } });
  const sR = slider(b.ctl, { label: "|R|", min: 0, max: 1, step: 0.01, value: 1, dom: "el", fmt: v => v.toFixed(2), onchange: v => { st.R = v; upd(); } });
  const sP = slider(b.ctl, { label: "phase of R", min: 0, max: 360, step: 5, value: 0, unit: "°", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.ph = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "lam", label: "λ", dom: "el" }, { id: "swr", label: "standing wave ratio s", dom: "el" }, { id: "nodes", label: "pressure minima at" }, { id: "wall", label: "at the wall (x = 0)" }]);
  let t0 = performance.now();
  function upd() {
    const lam = CA / st.f, s = (1 + st.R) / (1 - st.R);
    const phr = st.ph * Math.PI / 180;
    // minima of |1 + R e^{j(2kx+φ)}| for x<0 measured as distance d from the wall: 2kd = π + φ (+2πn) → d = (π+φ)/(2k) ... with x = -d: e^{-jkx}+R e^{jkx} = e^{jkd} + R e^{-jkd}; |·| = |1 + R e^{-j(2kd - φ)}| min when 2kd - φ = π
    const k = TAU / lam, d0 = ((Math.PI + phr) / (2 * k)) % (lam / 2);
    const nodes = [0, 1, 2].map(n => d0 + n * lam / 2);
    ro({ lam: `${(lam * 100).toFixed(1)} cm`, swr: isFinite(s) && st.R < 1 ? s.toFixed(2) : "∞ (perfect nodes)", nodes: st.R > 0.02 ? nodes.map(d => `${(d * 100).toFixed(1)} cm`).join(" · ") : "no minima (no reflection)", wall: st.ph === 0 && st.R === 1 ? "pressure antinode, velocity node" : st.ph === 180 && st.R === 1 ? "pressure node, velocity antinode" : `|P| = ${cabs(cadd(cx(1, 0), cx(st.R * Math.cos(phr), st.R * Math.sin(phr)))).toFixed(2)} × incident` });
  }
  function frame(now) {
    if (!stage.isConnected) return;
    const t = (now - t0) / 1000, W = 640, H = 300, x0 = 30, x1 = 600, mid = 150, lam = CA / st.f, k = TAU / lam, phr = st.ph * Math.PI / 180;
    const L = 1.0; // metre shown, wall at right
    let env = "", envm = "", inst = "", vel = "";
    for (let i = 0; i <= 240; i++) {
      const d = L * (1 - i / 240); // distance from wall
      const P = cadd(cx(Math.cos(k * d), Math.sin(k * d)), cx(st.R * Math.cos(phr - k * d), st.R * Math.sin(phr - k * d))); // e^{jkd} + R e^{j(φ - kd)}
      const U = csub(cx(Math.cos(k * d), Math.sin(k * d)), cx(st.R * Math.cos(phr - k * d), st.R * Math.sin(phr - k * d)));
      const X = x0 + (x1 - x0) * i / 240, A = cabs(P) * 55, re = (P.re * Math.cos(TAU * 0.4 * t) - P.im * Math.sin(TAU * 0.4 * t)) * 55;
      env += (i ? "L" : "M") + X.toFixed(1) + " " + (mid - A).toFixed(1); envm += (i ? "L" : "M") + X.toFixed(1) + " " + (mid + A).toFixed(1);
      inst += (i ? "L" : "M") + X.toFixed(1) + " " + (mid - re).toFixed(1);
      vel += (i ? "L" : "M") + X.toFixed(1) + " " + (mid - cabs(U) * 55 + 0).toFixed(1);
    }
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">
      <rect x="${x1}" y="30" width="14" height="240" fill="var(--ink-3)" opacity="0.5"/>
      <line x1="${x0}" x2="${x1}" y1="${mid}" y2="${mid}" stroke="var(--plot-grid)"/>
      <path d="${env}" fill="none" stroke="var(--el)" stroke-width="2"/><path d="${envm}" fill="none" stroke="var(--el)" stroke-width="2"/>
      <path d="${vel}" fill="none" stroke="var(--me)" stroke-width="1.5" stroke-dasharray="5 4"/>
      <path d="${inst}" fill="none" stroke="var(--el)" stroke-width="1.2" opacity="0.5"/>
      <text x="${x0}" y="22" font-size="11" fill="var(--el)">|P(x)| envelope (solid), p(x,t) instantaneous (faint)</text>
      <text x="${x0}" y="290" font-size="11" fill="var(--me)">|U(x)| envelope (dashed) — nodes of one are antinodes of the other</text>
      <text x="${x1 - 6}" y="45" text-anchor="end" font-size="10" fill="var(--ink-3)">boundary ← 1 m →</text>
    </svg>`;
    requestAnimationFrame(frame);
  }
  upd(); requestAnimationFrame(frame);
  b.note.innerHTML = `<p>Everything here is <span class="mono">P(x) = P_i(e^{−jkx} + R e^{jkx})</span> — one incident wave, one reflected. A rigid wall forces the velocity to zero, so <span class="mono">R = +1</span>: the wall is a pressure <b>antinode</b> and the first pressure node sits a quarter wavelength away (8.6 cm at 1 kHz, then every half wavelength). A pressure-release end flips the sign. Partial reflection leaves minima that do not reach zero; the ratio of max to min is the standing wave ratio <span class="mono">s = (1+|R|)/(1−|R|)</span>, which is how |R| is measured in a tube.</p>`;
}

/* ===== L2 · tube resonances ===== */
function benchTubeModes() {
  const b = bench("bench-tubemodes", "Tube resonances: the ends decide the sequence", "lecture 2 · §3");
  if (!b) return;
  const st = { L: 0.5, ends: "oo", c: CA };
  segCtl(b.ctl, st, "ends", [["oo", "open–open"], ["co", "closed–open"], ["cc", "closed–closed"]], () => upd());
  slider(b.ctl, { label: "length <b>L</b>", min: 0.1, max: 3, step: 0.01, value: 0.5, unit: "m", fmt: v => v.toFixed(2), onchange: v => { st.L = v; upd(); } });
  segCtl(b.ctl, st, "c", [[CA, "air 343"], [1000, "helium 1000"]], () => upd());
  const ro = readouts(b.ctl, [{ id: "f", label: "first five resonances", dom: "ac" }, { id: "rule", label: "rule" }]);
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  function upd() {
    const fn = (n) => st.ends === "co" ? (2 * n - 1) * st.c / (4 * st.L) : n * st.c / (2 * st.L);
    ro({ f: [1, 2, 3, 4, 5].map(n => `${fn(n).toFixed(0)}`).join(" · ") + " Hz", rule: st.ends === "co" ? "f_n = (2n−1)·c/4L — odd harmonics only" : "f_n = n·c/2L — all harmonics" });
    const W = 640, H = 260, x0 = 60, x1 = 580;
    let g = "";
    [1, 2, 3].forEach((n, row) => {
      const y = 45 + row * 70; let d = "";
      for (let i = 0; i <= 120; i++) { const x = i / 120; const p = st.ends === "oo" ? Math.sin(n * Math.PI * x) : st.ends === "cc" ? Math.cos(n * Math.PI * x) : Math.cos((2 * n - 1) * Math.PI * x / 2); d += (i ? "L" : "M") + (x0 + x * (x1 - x0)).toFixed(1) + " " + (y - 24 * p).toFixed(1); }
      g += `<line x1="${x0}" x2="${x1}" y1="${y}" y2="${y}" stroke="var(--plot-grid)"/><path d="${d}" fill="none" stroke="var(--el)" stroke-width="2"/><text x="${x1 + 8}" y="${y + 4}" font-size="12" fill="var(--ink)">${fn(n).toFixed(0)} Hz</text><text x="${x0 - 8}" y="${y + 4}" text-anchor="end" font-size="11" fill="var(--ink-3)">n = ${n}</text>`;
    });
    const end = (x, closed) => closed ? `<rect x="${x - 4}" y="15" width="8" height="215" fill="var(--ink-3)" opacity="0.6"/>` : `<line x1="${x}" y1="15" x2="${x}" y2="230" stroke="var(--ink-3)" stroke-dasharray="3 3"/>`;
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">${end(x0, st.ends !== "oo")}${end(x1, st.ends === "cc")}${g}<text x="${(x0 + x1) / 2}" y="250" text-anchor="middle" font-size="11" fill="var(--ink-2)">pressure mode shapes — a closed end is a pressure antinode, an open end a pressure node</text></svg>`;
  }
  upd();
  b.note.innerHTML = `<p>A resonance is a round trip that comes back in phase. Open–open and closed–closed both need a whole number of half wavelengths (<span class="mono">f_n = nc/2L</span>); closed–open needs an odd number of quarter wavelengths (<span class="mono">(2n−1)c/4L</span>), so a closed organ pipe or a clarinet has only odd harmonics and sounds an octave lower than an open pipe of the same length. Real instruments add end corrections and bores that bend this, but the sequence is set by the ends.</p>`;
}

/* ===== L2 · interface between two media ===== */
function benchInterface() {
  const b = bench("bench-interface", "Two media: reflection, pressure transmission, power transmission", "lecture 2 · problem 3 · §4");
  if (!b) return;
  const MED = { air: ["air", 1.204, 343], water: ["water", 1000, 1480], helium: ["helium", 0.166, 1000], steel: ["steel", 7800, 5900] };
  const st = { m1: "air", m2: "water" };
  const mk = (key, label) => { const c = h("div", { class: "chips" }, h("span", { class: "small", style: "align-self:center" }, label)); for (const k of Object.keys(MED)) c.append(h("button", { type: "button", class: "chip" + (st[key] === k ? " on" : ""), onclick: (e) => { st[key] = k; $$(".chip", c).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, MED[k][0])); b.ctl.append(c); };
  mk("m1", "from:"); mk("m2", "into:");
  const ro = readouts(b.ctl, [{ id: "z", label: "Z₁ · Z₂ = ρc" }, { id: "R", label: "R = (Z₂−Z₁)/(Z₂+Z₁)", dom: "el" }, { id: "T", label: "T_p = P_t/P_i = 1 + R", dom: "el" }, { id: "att", label: "attenuation factor P_i/P_t" }, { id: "tau", label: "power transmitted τ", dom: "ac" }, { id: "dB", label: "in dB" }]);
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  function upd() {
    const [n1, r1, c1] = MED[st.m1], [n2, r2, c2] = MED[st.m2], Z1 = r1 * c1, Z2 = r2 * c2;
    const R = (Z2 - Z1) / (Z2 + Z1), T = 1 + R, tau = 4 * Z1 * Z2 / ((Z1 + Z2) ** 2);
    ro({ z: `${sci(Z1)} · ${sci(Z2)} Pa·s/m`, R: R.toFixed(5), T: T.toFixed(4), att: (1 / T).toFixed(T > 1 ? 3 : 1), tau: `${sci(tau)} (${(100 * tau).toFixed(tau < 0.01 ? 3 : 1)} %)`, dB: `pressure ${(20 * Math.log10(T)).toFixed(1)} dB · power ${(10 * Math.log10(tau)).toFixed(1)} dB` });
    const W = 640, H = 220, mid = 320;
    const bar = (x, y, w, hgt, col, lbl) => `<rect x="${x}" y="${y - hgt}" width="${w}" height="${hgt}" fill="${col}" opacity="0.8"/><text x="${x + w / 2}" y="${y - hgt - 6}" text-anchor="middle" font-size="11" fill="var(--ink)">${lbl}</text>`;
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">
      <rect x="0" y="0" width="${mid}" height="${H}" fill="var(--el-soft)"/><rect x="${mid}" y="0" width="${W - mid}" height="${H}" fill="var(--ac-soft)"/>
      <text x="16" y="24" font-size="13" fill="var(--ink)">${n1}   Z₁ = ${sci(Z1)}</text><text x="${mid + 16}" y="24" font-size="13" fill="var(--ink)">${n2}   Z₂ = ${sci(Z2)}</text>
      ${bar(60, 190, 60, 120, "var(--el)", "incident 1")}${bar(160, 190, 60, 120 * Math.abs(R), "var(--me)", `reflected ${R.toFixed(3)}`)}${bar(mid + 100, 190, 60, Math.min(190, 120 * T), "var(--ac)", `transmitted ${T.toFixed(3)}`)}
      <text x="${mid}" y="${H - 8}" text-anchor="middle" font-size="11" fill="var(--ink-2)">pressure amplitudes relative to the incident wave</text>
    </svg>`;
    b.note.innerHTML = `<p>${st.m1 === "air" && st.m2 === "water" ? "Air into water: almost total reflection (R = 0.9994), yet the transmitted <b>pressure</b> is twice the incident (attenuation factor 0.5 — an amplification!). No paradox: pressure continuity gives <span class='mono'>P_t = P_i + P_r ≈ 2P_i</span>, while the <em>power</em> that gets in is only 0.1 %. Turn it round (water into air) and the pressure is attenuated 1793×, 65 dB, with the same 0.1 % of power crossing." : "Continuity of pressure and of normal velocity at the interface gives <span class='mono'>R = (Z₂ − Z₁)/(Z₂ + Z₁)</span> and <span class='mono'>T_p = 1 + R</span>. The pressure ratio can exceed 1; the power fraction <span class='mono'>τ = 4Z₁Z₂/(Z₁+Z₂)²</span> never does, and it is the same in both directions."}</p>`;
  }
  upd();
}

/* ===== L2 · spherical wave near field ===== */
function benchSpherical() {
  const b = bench("bench-spherical", "Near a small source: pressure falls as 1/r, velocity does something more", "lecture 2 · problem 4 · §5–6");
  if (!b) return;
  const st = { f: 250, r: 0.1, A: 0.5 };
  slider(b.ctl, { label: "frequency <b>f</b>", min: 50, max: 4000, log: true, value: 250, unit: "Hz", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.f = v; upd(); } });
  slider(b.ctl, { label: "distance <b>r</b>", min: 0.02, max: 5, log: true, value: 0.1, unit: "m", fmt: v => v.toFixed(3), onchange: v => { st.r = v; upd(); } });
  slider(b.ctl, { label: "pressure at 1 m", min: 0.05, max: 5, step: 0.05, value: 0.5, unit: "Pa", dom: "el", fmt: v => v.toFixed(2), onchange: v => { st.A = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "kr", label: "kr (Helmholtz number)" }, { id: "p", label: "|p| = A/r", dom: "el" }, { id: "u", label: "|u_r| = |p|/ρc · √(1 + 1/(kr)²)", dom: "me" }, { id: "up", label: "plane-wave guess |p|/ρc", dom: "me" }, { id: "ph", label: "arg(p/u) = atan(1/kr)", dom: "el" }, { id: "z", label: "|Z_s| / ρc" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 0.05, xmax: 50, ymin: 0, ymax: 90, xlabel: "kr", ylabel: "phase of p/u (°)  ·  |Z_s|/ρc × 90", xfmt: v => Number(v.toPrecision(2)), yfmt: v => v.toFixed(0), xticks: [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50].map(v => ({ v, l: String(v) })) });
  const krs = logspace(0.05, 50, 300);
  function upd() {
    const k = TAU * st.f / CA, kr = k * st.r, p = st.A / st.r, u = p / ZAIR * Math.sqrt(1 + 1 / (kr * kr)), ph = Math.atan(1 / kr);
    plot.set({ series: [{ name: "phase p leads u (°)", color: DOMC.el, pts: krs.map(x => [x, Math.atan(1 / x) * 180 / Math.PI]) }, { name: "|Z_s|/ρc (×90)", color: DOMC.me, pts: krs.map(x => [x, 90 / Math.sqrt(1 + 1 / (x * x))]) }], markers: [{ x: kr, y: ph * 180 / Math.PI, label: `kr = ${kr.toFixed(2)}: ${(ph * 180 / Math.PI).toFixed(1)}°`, color: DOMC.el }], regions: [{ from: 0.05, to: 0.3, color: DOMC.me, label: "near field, reactive" }, { from: 3, to: 50, color: DOMC.ac, label: "far field, like a plane wave" }] });
    ro({ kr: kr.toFixed(3), p: `${p.toFixed(3)} Pa`, u: `${(u * 1e3).toFixed(2)} mm/s`, up: `${(p / ZAIR * 1e3).toFixed(2)} mm/s`, ph: `${ph.toFixed(3)} rad = ${(ph * 180 / Math.PI).toFixed(1)}°`, z: (1 / Math.sqrt(1 + 1 / (kr * kr))).toFixed(3) });
  }
  upd();
  b.note.innerHTML = `<p>Outgoing spherical wave: <span class="mono">P = A e^{−jkr}/r</span>, so the pressure simply spreads as 1/r (−6 dB per doubling of distance). Euler's equation then gives <span class="mono">U_r = (P/ρc)(1 + 1/(jkr))</span>: the extra term is the <b>near field</b>. Close to the source (kr ≪ 1) the velocity is much larger than the plane-wave guess and lags the pressure by up to 90° — a reactive field, sloshing without carrying power. Far away (kr ≫ 1) the wave looks plane. The dividing line is <span class="mono">r = λ/2π</span>.</p>`;
}

/* ===== L3 · levels: adding, subtracting, coherent vs not ===== */
function benchLevels() {
  const b = bench("bench-levels", "Decibels: adding sources, subtracting background", "lecture 3 · problems 1.1, 1.2, 5");
  if (!b) return;
  const st = { L1: 90, L2: 90, mode: "unc", th: 120, Lt: 80, Lb: 75 };
  slider(b.ctl, { label: "source 1 level <b>L₁</b>", min: 30, max: 110, step: 0.5, value: 90, unit: "dB", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.L1 = v; upd(); } });
  slider(b.ctl, { label: "source 2 level <b>L₂</b>", min: 30, max: 110, step: 0.5, value: 90, unit: "dB", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.L2 = v; upd(); } });
  segCtl(b.ctl, st, "mode", [["unc", "uncorrelated (different tones, noise)"], ["coh", "same tone, phase lag θ"]], () => upd());
  slider(b.ctl, { label: "phase lag <b>θ</b> (coherent only)", min: 0, max: 360, step: 1, value: 120, unit: "°", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.th = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "tot", label: "total level", dom: "ac" }, { id: "gain", label: "above the louder one" }, { id: "p", label: "rms pressures" }]);
  b.ctl.append(h("div", { class: "eyebrow", style: "margin-top:6px" }, "background correction (problem 5)"));
  slider(b.ctl, { label: "measured total <b>L_tot</b>", min: 40, max: 110, step: 0.1, value: 80, unit: "dB", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.Lt = v; upd(); } });
  slider(b.ctl, { label: "background alone <b>L_bg</b>", min: 30, max: 110, step: 0.1, value: 75, unit: "dB", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.Lb = v; upd(); } });
  const ro2 = readouts(b.ctl, [{ id: "src", label: "source alone", dom: "ac" }, { id: "warn", label: "reliability" }]);
  const plot = new Plot(b.plot, { h: 280, xlog: false, xmin: 0, xmax: 20, ymin: 0, ymax: 6.5, xlabel: "level difference L₁ − L₂ (dB)", ylabel: "increase over the louder source (dB)", xfmt: v => v.toFixed(0), yfmt: v => v.toFixed(1) });
  const ds = linspace(0, 20, 81);
  function upd() {
    const p1 = PREF * Math.pow(10, st.L1 / 20), p2 = PREF * Math.pow(10, st.L2 / 20);
    let ptot;
    if (st.mode === "unc") ptot = Math.hypot(p1, p2);
    else { const th = st.th * Math.PI / 180; ptot = Math.hypot(p1 + p2 * Math.cos(th), p2 * Math.sin(th)); }
    const Lt = LP(ptot), hi = Math.max(st.L1, st.L2);
    plot.set({ series: [{ name: "uncorrelated: 10·log(1 + 10^(−ΔL/10))", color: DOMC.ac, pts: ds.map(d => [d, 10 * Math.log10(1 + Math.pow(10, -d / 10))]) }, { name: "coherent, in phase: 20·log(1 + 10^(−ΔL/20))", color: DOMC.el, thin: true, pts: ds.map(d => [d, 20 * Math.log10(1 + Math.pow(10, -d / 20))]) }], markers: [{ x: Math.abs(st.L1 - st.L2), y: Lt - hi, label: `+${(Lt - hi).toFixed(1)} dB`, color: st.mode === "unc" ? DOMC.ac : DOMC.el }] });
    ro({ tot: `${Lt.toFixed(1)} dB`, gain: `${(Lt - hi) >= 0 ? "+" : ""}${(Lt - hi).toFixed(1)} dB`, p: `${(p1).toFixed(3)} · ${(p2).toFixed(3)} → ${ptot.toFixed(3)} Pa` });
    const ms = Math.pow(10, st.Lt / 10) - Math.pow(10, st.Lb / 10);
    ro2({ src: ms > 0 ? `${(10 * Math.log10(ms)).toFixed(1)} dB` : "— (background ≥ total?)", warn: st.Lt - st.Lb < 3 ? "unreliable: background less than 3 dB below" : st.Lt - st.Lb > 10 ? "correction < 0.5 dB" : "fine" });
  }
  upd();
  b.note.innerHTML = `<p><span class="mono">L_p = 20·log(p_rms/20 µPa)</span>. Independent sources add their <b>mean squares</b>: two equal ones give +3 dB, ten give +10 dB, and a source 10 dB below another adds only 0.4 dB. Two equal <b>coherent</b> tones give anything from +6 dB (in phase) to −∞ (antiphase); at 120° they give exactly the level of one alone, because |1 + e^{−j120°}| = 1. Background is removed by subtracting mean squares: <span class="mono">L_src = 10·log(10^{L_tot/10} − 10^{L_bg/10})</span> — 80 dB total with 75 dB background is a 78.3 dB source.</p>`;
}

/* ===== L3 · octave bands, harmonics, 1/n octaves ===== */
const OCT = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000];
function benchOctave() {
  const b = bench("bench-octave", "Octave-band analysis of a harmonic series", "lecture 3 · problems 3 and 4");
  if (!b) return;
  const st = { T: 1.3, N: 7, L: 60, n: 12, fc: 1000 };
  slider(b.ctl, { label: "period <b>T</b>", min: 0.3, max: 5, step: 0.01, value: 1.3, unit: "ms", fmt: v => v.toFixed(2), onchange: v => { st.T = v; upd(); } });
  slider(b.ctl, { label: "harmonics (fundamental + overtones)", min: 1, max: 12, step: 1, value: 7, fmt: v => v.toFixed(0), onchange: v => { st.N = v; upd(); } });
  slider(b.ctl, { label: "level of each component", min: 40, max: 90, step: 1, value: 60, unit: "dB", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.L = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "fundamental 1/T", dom: "el" }, { id: "bands", label: "band levels", dom: "ac" }, { id: "tot", label: "total (Parseval)", dom: "ac" }]);
  b.ctl.append(h("div", { class: "eyebrow", style: "margin-top:6px" }, "1/n-octave filter (problem 4)"));
  segCtl(b.ctl, st, "n", [[1, "1/1"], [3, "1/3"], [12, "1/12"], [24, "1/24"]], () => upd());
  slider(b.ctl, { label: "centre frequency <b>f_c</b>", min: 20, max: 20000, log: true, value: 1000, unit: "Hz", fmt: v => v.toFixed(0), onchange: v => { st.fc = v; upd(); } });
  const ro2 = readouts(b.ctl, [{ id: "edges", label: "f_l = f_c·2^(−1/2n) · f_u = f_c·2^(1/2n)" }, { id: "bw", label: "bandwidth f_u − f_l", dom: "ac" }]);
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  function upd() {
    const f0 = 1000 / st.T, comps = Array.from({ length: st.N }, (_, i) => (i + 1) * f0);
    const band = OCT.map(fc => { const fl = fc / Math.SQRT2, fu = fc * Math.SQRT2; const m = comps.filter(f => f >= fl && f < fu).length; return { fc, fl, fu, n: m, L: m ? st.L + 10 * Math.log10(m) : null }; });
    const tot = st.L + 10 * Math.log10(st.N);
    ro({ f0: `${f0.toFixed(1)} Hz`, bands: band.filter(x => x.n).map(x => `${x.fc >= 1000 ? x.fc / 1000 + "k" : x.fc}: ${x.L.toFixed(1)} dB (${x.n})`).join(" · "), tot: `${tot.toFixed(1)} dB` });
    const n = st.n, fl = st.fc * Math.pow(2, -1 / (2 * n)), fu = st.fc * Math.pow(2, 1 / (2 * n));
    ro2({ edges: `${fl.toFixed(1)} – ${fu.toFixed(1)} Hz`, bw: `${(fu - fl).toFixed(1)} Hz (${(100 * (fu - fl) / st.fc).toFixed(1)} % of f_c)` });
    // drawing: log-frequency axis 20 Hz .. 20 kHz
    const W = 640, H = 300, x0 = 50, x1 = 620, y0 = 250, X = (f) => x0 + (Math.log10(f) - Math.log10(20)) / 3 * (x1 - x0), Y = (L) => y0 - (L - 30) / 60 * 200;
    let g = "";
    for (const bd of band) { const xa = X(bd.fl), xb = X(bd.fu); g += `<rect x="${xa}" y="${bd.L ? Y(bd.L) : y0}" width="${xb - xa - 2}" height="${bd.L ? y0 - Y(bd.L) : 0}" fill="var(--ac)" opacity="0.35"/><text x="${(xa + xb) / 2}" y="${y0 + 14}" text-anchor="middle" font-size="10" fill="var(--ink-2)">${bd.fc >= 1000 ? bd.fc / 1000 + "k" : bd.fc}</text>` + (bd.L ? `<text x="${(xa + xb) / 2}" y="${Y(bd.L) - 5}" text-anchor="middle" font-size="10" fill="var(--ink)">${bd.L.toFixed(0)}</text>` : ""); }
    for (const f of comps) if (f >= 20 && f <= 20000) g += `<line x1="${X(f)}" x2="${X(f)}" y1="${Y(st.L)}" y2="${y0}" stroke="var(--el)" stroke-width="2"/>`;
    const fx = X(st.fc); g += `<rect x="${X(fl)}" y="40" width="${X(fu) - X(fl)}" height="16" fill="var(--me)" opacity="0.5"/><text x="${fx}" y="34" text-anchor="middle" font-size="10" fill="var(--me)">1/${n} oct at ${st.fc.toFixed(0)} Hz</text>`;
    for (const L of [40, 60, 80]) g += `<line x1="${x0}" x2="${x1}" y1="${Y(L)}" y2="${Y(L)}" stroke="var(--plot-grid)"/><text x="${x0 - 6}" y="${Y(L) + 4}" text-anchor="end" font-size="10" fill="var(--ink-3)">${L}</text>`;
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">${g}<line x1="${x0}" x2="${x1}" y1="${y0}" y2="${y0}" stroke="var(--plot-axis)"/><text x="${x0}" y="${H - 8}" font-size="11" fill="var(--ink-2)">harmonic lines (violet) · octave-band levels in dB (teal) · the 1/n-octave window (copper)</text></svg>`;
  }
  upd();
  b.note.innerHTML = `<p>Components at different frequencies are uncorrelated, so a band's level is <span class="mono">10·log Σ10^{L_i/10}</span> over the lines inside it: n equal lines give +10·log n. A 1.3 ms period puts harmonics at 769, 1538, 2308, 3077, 3846, 4615, 5385 Hz: one in the 1 kHz octave (60 dB), two in the 2 kHz octave (63 dB), four in the 4 kHz octave (66 dB). Octave edges are <span class="mono">f_c/√2</span> and <span class="mono">f_c·√2</span>; a 1/n-octave band has <span class="mono">f_u/f_l = 2^{1/n}</span>, so a 1/12-octave at 1 kHz is only 57.8 Hz wide.</p>`;
}

/* ===== L3 · A- and C-weighting ===== */
const A_TABLE = [[8, -77.8], [10, -70.4], [12.5, -63.4], [16, -56.7], [20, -50.5], [25, -44.7], [31.5, -39.4], [40, -34.6], [50, -30.2], [63, -26.2], [80, -22.5], [100, -19.1], [125, -16.1], [160, -13.4], [200, -10.9], [250, -8.6], [315, -6.6], [400, -4.8], [500, -3.2], [630, -1.9], [800, -0.8], [1000, 0], [1250, 0.6], [1600, 1.0], [2000, 1.2], [2500, 1.3], [3150, 1.2], [4000, 1.0], [5000, 0.5], [6300, -0.1], [8000, -1.1], [10000, -2.5], [12500, -4.3], [16000, -6.6], [20000, -9.3]];
function aWeight(f) { const s = cx(0, TAU * f); const num = cmul(cmul(s, s), cmul(s, s)); const p = (a) => cadd(s, cx(a, 0)); const den = cmul(cmul(cmul(p(129.4), p(129.4)), cmul(p(676.7), p(4636))), cmul(p(76655), p(76655))); return dB(cabs(cdiv(num, den))); }
function cWeight(f) { const s = cx(0, TAU * f); const p = (a) => cadd(s, cx(a, 0)); return dB(cabs(cdiv(cmul(s, s), cmul(cmul(p(129.4), p(129.4)), cmul(p(76655), p(76655)))))); }
function benchWeighting() {
  const b = bench("bench-weighting", "A-weighting: the meter's model of a not-very-sensitive ear", "lecture 3 · Matlab exercise C");
  if (!b) return;
  const st = { f: 100 };
  slider(b.ctl, { label: "frequency", min: 10, max: 20000, log: true, value: 100, unit: "Hz", fmt: v => v.toFixed(0), onchange: v => { st.f = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "A", label: "A-weighting", dom: "ac" }, { id: "C", label: "C-weighting", dom: "ac" }, { id: "ex", label: "70 dB tone here reads" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 10, xmax: 20000, ymin: -60, ymax: 10, ylabel: "relative response (dB)", yfmt: v => v.toFixed(0), yunit: " dB" });
  const fs = logspace(10, 20000, 300), a0 = aWeight(1000), c0 = cWeight(1000);
  const seriesFixed = [{ name: "A-weighting (formula)", color: DOMC.ac, pts: fs.map(f => [f, aWeight(f) - a0]) }, { name: "C-weighting", color: DOMC.me, pts: fs.map(f => [f, cWeight(f) - c0]) }, { name: "table 1.3.2, 1/3-octave values", color: DOMC.ac, thin: true, pts: A_TABLE.map(([f, v]) => [f, v]) }];
  function upd() { const A = aWeight(st.f) - a0, C = cWeight(st.f) - c0; plot.set({ series: seriesFixed, markers: [{ x: st.f, y: A, label: `${A.toFixed(1)} dB at ${hz(st.f)}`, color: DOMC.ac }] }); ro({ A: `${A.toFixed(1)} dB`, C: `${C.toFixed(1)} dB`, ex: `${(70 + A).toFixed(1)} dB(A)` }); }
  upd();
  b.note.innerHTML = `<p>At low and moderate levels the ear is much less sensitive below a few hundred hertz and above 10 kHz. The A-weighting filter, <span class="mono">H_A(s) = 7.4·10⁹ s⁴ / ((s+129.4)²(s+676.7)(s+4636)(s+76655)²)</span>, normalised to 0 dB at 1 kHz, mimics that: −19 dB at 100 Hz, −39 dB at 31.5 Hz, a slight +1 dB bump around 2–3 kHz. <span class="mono">L_A</span> is the single number almost every noise limit is written in. C-weighting is nearly flat; a big L_C − L_A difference says "low-frequency noise". In the Matlab exercise the 440 Hz sine at 74 dB reads 69.9 dB(A): −4.1 dB, read it off the curve.</p>`;
}

/* ===== L3 · time weighting: fast, slow, Leq ===== */
function benchTimeWeight() {
  const b = bench("bench-timeweight", "Fast, Slow and L_eq on a source that switches on and off", "lecture 3 · Matlab exercise A–B");
  if (!b) return;
  const st = { Lon: 85, Lbg: 70, on: 2, off: 2 };
  slider(b.ctl, { label: "source on: level", min: 60, max: 100, step: 0.5, value: 85, unit: "dB", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.Lon = v; upd(); } });
  slider(b.ctl, { label: "background", min: 40, max: 90, step: 0.5, value: 70, unit: "dB", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.Lbg = v; upd(); } });
  slider(b.ctl, { label: "on time", min: 0.1, max: 5, step: 0.1, value: 2, unit: "s", fmt: v => v.toFixed(1), onchange: v => { st.on = v; upd(); } });
  slider(b.ctl, { label: "off time", min: 0.1, max: 5, step: 0.1, value: 2, unit: "s", fmt: v => v.toFixed(1), onchange: v => { st.off = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "leq", label: "L_eq over 12 s", dom: "ac" }, { id: "F", label: "L_F (τ = 125 ms) max / min" }, { id: "S", label: "L_S (τ = 1 s) max / min" }, { id: "duty", label: "duty cycle" }]);
  const plot = new Plot(b.plot, { h: 300, xlog: false, xmin: 0, xmax: 12, ymin: 55, ymax: 100, xlabel: "time (s)", ylabel: "level (dB)", xfmt: v => `${v.toFixed(0)} s`, yfmt: v => v.toFixed(0) });
  function upd() {
    const fs = 200, N = 12 * fs, pon = Math.pow(10, st.Lon / 10), pbg = Math.pow(10, st.Lbg / 10);
    const sq = Array.from({ length: N }, (_, i) => { const t = i / fs; const ph = t % (st.on + st.off); return pbg + (ph < st.on ? pon : 0); });
    const run = (tau) => { const a = Math.exp(-1 / (tau * fs)); let y = sq[0]; return sq.map(v => (y = a * y + (1 - a) * v)); };
    const F = run(0.125), S = run(1.0), leq = 10 * Math.log10(sq.reduce((s, v) => s + v, 0) / N);
    const pts = (arr) => arr.filter((_, i) => i % 2 === 0).map((v, i) => [2 * i / fs, 10 * Math.log10(v)]);
    plot.set({ series: [{ name: "instantaneous (mean-square of the source)", color: DOMC.ink3, thin: true, pts: pts(sq) }, { name: "Fast, τ = 125 ms", color: DOMC.el, pts: pts(F) }, { name: "Slow, τ = 1 s", color: DOMC.me, pts: pts(S) }, { name: `L_eq = ${leq.toFixed(1)} dB`, color: DOMC.ac, pts: [[0, leq], [12, leq]] }] });
    const mm = (arr) => `${(10 * Math.log10(Math.max(...arr.slice(fs)))).toFixed(1)} / ${(10 * Math.log10(Math.min(...arr.slice(fs)))).toFixed(1)} dB`;
    ro({ leq: `${leq.toFixed(1)} dB`, F: mm(F), S: mm(S), duty: `${(100 * st.on / (st.on + st.off)).toFixed(0)} % on` });
  }
  upd();
  b.note.innerHTML = `<p>A sound level meter squares the pressure, then smooths it. <b>Exponential</b> smoothing with τ = 125 ms (Fast) or 1 s (Slow) is a running average that follows the source up and down — Slow rounds the corners, Fast keeps them. The <b>equivalent level</b> <span class="mono">L_eq</span> is the plain average of the squared pressure over the whole interval, so a source on half the time at 85 dB with 70 dB background gives an L_eq near 82 dB, not the 77.5 dB you get by averaging the decibels. Digitally the running average is a one-pole filter: <span class="mono">y[n] = α y[n−1] + (1−α) p²[n]</span>, α = e^{−1/(τ f_s)}.</p>`;
}

/* ===== L3 · white vs pink noise in bands ===== */
function benchNoise() {
  const b = bench("bench-noise", "White and pink noise through octave and 1/3-octave filters", "lecture 3 · §1.3.1");
  if (!b) return;
  const st = { kind: "white", n: 1 };
  segCtl(b.ctl, st, "kind", [["white", "white: constant power per Hz"], ["pink", "pink: constant power per octave"]], () => upd());
  segCtl(b.ctl, st, "n", [[1, "octave bands"], [3, "1/3-octave bands"]], () => upd());
  const ro = readouts(b.ctl, [{ id: "step", label: "band-to-band step", dom: "ac" }, { id: "oct3", label: "octave vs 1/3-octave level" }]);
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  const THIRD = [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000];
  function upd() {
    const fcs = st.n === 1 ? OCT : THIRD, bw = (fc) => fc * (Math.pow(2, 1 / (2 * st.n)) - Math.pow(2, -1 / (2 * st.n)));
    const L = fcs.map(fc => st.kind === "white" ? 40 + 10 * Math.log10(bw(fc)) : 60 - 10 * Math.log10(st.n)); // white: 40 dB per Hz reference; pink: 60 dB per octave
    const W = 640, H = 280, x0 = 50, x1 = 620, y0 = 240, X = (f) => x0 + (Math.log10(f) - Math.log10(15)) / Math.log10(25000 / 15) * (x1 - x0), Y = (l) => y0 - (l - 30) / 60 * 200;
    let g = "";
    fcs.forEach((fc, i) => { const fl = fc * Math.pow(2, -1 / (2 * st.n)), fu = fc * Math.pow(2, 1 / (2 * st.n)); g += `<rect x="${X(fl)}" y="${Y(L[i])}" width="${X(fu) - X(fl) - 1.5}" height="${y0 - Y(L[i])}" fill="${st.kind === "white" ? "var(--el)" : "var(--me)"}" opacity="0.45"/>`; if (st.n === 1 || i % 3 === 2) g += `<text x="${X(fc)}" y="${y0 + 14}" text-anchor="middle" font-size="10" fill="var(--ink-2)">${fc >= 1000 ? fc / 1000 + "k" : fc}</text>`; });
    for (const l of [40, 60, 80]) g += `<line x1="${x0}" x2="${x1}" y1="${Y(l)}" y2="${Y(l)}" stroke="var(--plot-grid)"/><text x="${x0 - 6}" y="${Y(l) + 4}" text-anchor="end" font-size="10" fill="var(--ink-3)">${l}</text>`;
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">${g}<line x1="${x0}" x2="${x1}" y1="${y0}" y2="${y0}" stroke="var(--plot-axis)"/><text x="${x0}" y="${H - 8}" font-size="11" fill="var(--ink-2)">${st.kind} noise, band levels in dB (illustrative absolute level)</text></svg>`;
    ro({ step: st.kind === "white" ? `+${(10 * Math.log10(Math.pow(2, 1 / st.n))).toFixed(1)} dB per band (bandwidth grows)` : "0 dB — flat", oct3: st.kind === "pink" ? "octave = 1/3-octave + 4.8 dB (three bands of equal power)" : "octave = 1/3-octave + 4.8 dB at the same centre" });
  }
  upd();
  b.note.innerHTML = `<p><b>White</b> noise has constant mean-square per hertz, so a constant-percentage filter passes more of it the higher its centre frequency: +3 dB per octave band, +1 dB per 1/3-octave band. <b>Pink</b> noise has constant power per octave — flat in this display, and it sounds balanced because hearing itself has roughly constant relative bandwidth. Both are stochastic: their mean square is split among bands by Parseval, so the octave level always equals the sum of its three 1/3-octaves.</p>`;
}

/* ===== boot ===== */
document.addEventListener("DOMContentLoaded", () => {
  renderMath();
  benchWave(); benchPhasorSum(); benchSpeed();
  benchStanding(); benchTubeModes(); benchInterface(); benchSpherical();
  benchLevels(); benchOctave(); benchWeighting(); benchTimeWeight(); benchNoise();
  if (window.QUIZZES) { for (const [lec, qs] of Object.entries(QUIZZES)) { const root = document.getElementById(`quiz-${lec}`); if (root) { buildQuiz(root, lec, qs); TOTAL_Q += qs.length; const a = $(`.wire a[data-quiz="${lec}"]`); if (a) a.dataset.n = qs.length; } } }
  updateProgress();
  setupNav(); setupTheme();
  renderMath();
});
