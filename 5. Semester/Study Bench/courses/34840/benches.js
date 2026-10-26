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

/* L4: pure SI models, verified against Week4/check_week4.py. */
function helmholtz4(V, d, l) {
  const S = Math.PI*d*d/4, M = 1.2*l/S, K = 1.2*CA*CA/V;
  return {S, M, K, f0: Math.sqrt(K/M)/TAU};
}
function power4(L, S, phi=0) {
  const p = PREF*10**(L/20), I = p*p/ZAIR*Math.cos(phi*Math.PI/180);
  return {p, I, W:S*I};
}
function transmission4(z1,z2) {
  const R=(z2-z1)/(z2+z1), T=2*z2/(z1+z2), tau=T*T*z1/z2;
  return {R,T,tau,atten:-10*Math.log10(tau)};
}
function absorption4(Lmax,Lmin,S) {
  const pmax=PREF*10**(Lmax/20), pmin=PREF*10**(Lmin/20), pi=(pmax+pmin)/2, pr=(pmax-pmin)/2;
  const R=pr/pi, alpha=1-R*R, W=S*pmax*pmin/ZAIR;
  return {pmax,pmin,pi,pr,R,alpha,W,LW:10*Math.log10(W/1e-12)};
}
function cabinet4(V,d,m,xpp) {
  const S=Math.PI*d*d/4, M=m/S**2, K=1.2*CA**2/V, p=K*S*xpp/2/Math.sqrt(2);
  return {S,M,K,p,f0:Math.sqrt(K/M)/TAU,L:LP(p)};
}
function benchHelmholtz4() {
  const b=bench('bench-helmholtz','The bottle: neck mass meets the air spring','lecture 4 · problem 1'); if(!b)return;
  const st={V:400,d:20,l:21};
  for(const [key,label,min,max,unit] of [['V','cavity volume',100,1000,'ml'],['d','neck diameter',10,40,'mm'],['l','effective neck length',10,80,'mm']]) slider(b.ctl,{label,min,max,step:1,value:st[key],unit,onchange:v=>{st[key]=v;upd();}});
  const ro=readouts(b.ctl,[{id:'f',label:'resonance f₀'},{id:'M',label:'acoustic mass'},{id:'K',label:'acoustic stiffness'}]);
  const plot=new Plot(b.plot,{xmin:20,xmax:3000,ymin:0,ymax:8,ylabel:'|Z| / √(MK)',yfmt:v=>v.toFixed(1)});
  function upd(){const a=helmholtz4(st.V*1e-6,st.d/1000,st.l/1000);plot.set({series:[{name:'ideal series impedance',color:DOMC.ac,pts:logspace(20,3000,500).map(f=>[f,Math.abs(TAU*f*a.M-a.K/(TAU*f))/Math.sqrt(a.M*a.K)])}],markers:[{x:a.f0,y:0,label:a.f0.toFixed(1)+' Hz'}]});ro({f:a.f0.toFixed(1)+' Hz',M:a.M.toFixed(2)+' kg/m⁴',K:(a.K/1e6).toFixed(2)+' MN/m⁵'});}
  upd();b.note.innerHTML='<p>Start values reproduce 333.8 Hz. Increase cavity volume and watch the minimum move left. The ideal impedance is zero at resonance; real losses leave a finite resistance. The top of the plot is cropped to show the resonance region.</p>';
}
function benchPower4(){
  const b=bench('bench-power4','Pressure can oscillate without carrying net energy','lecture 4 · problem 2');if(!b)return;
  const st={L:82,S:10,phi:0};
  for(const [key,label,min,max,step,unit] of [['L','pressure level',40,100,1,'dB'],['S','perpendicular area',1,20,0.5,'m²'],['phi','pressure–velocity phase',0,90,1,'°']])slider(b.ctl,{label,min,max,step,value:st[key],unit,onchange:v=>{st[key]=v;upd();}});
  const ro=readouts(b.ctl,[{id:'p',label:'RMS pressure'},{id:'I',label:'mean intensity'},{id:'W',label:'mean power'}]);
  const plot=new Plot(b.plot,{xlog:false,xmin:0,xmax:90,ymin:0,ymax:1.05,xlabel:'phase difference (°)',ylabel:'active fraction cos φ',xfmt:v=>v.toFixed(0),yfmt:v=>v.toFixed(2)});
  function upd(){const a=power4(st.L,st.S,st.phi);ro({p:a.p.toFixed(4)+' Pa',I:(a.I*1000).toFixed(4)+' mW/m²',W:(a.W*1000).toFixed(4)+' mW'});plot.set({series:[{name:'cos φ',color:DOMC.ac,pts:linspace(0,90,91).map(x=>[x,Math.cos(x*Math.PI/180)])}],markers:[{x:st.phi,y:Math.cos(st.phi*Math.PI/180),label:st.phi+'°'}]});}
  upd();b.note.innerHTML='<p>At 0° this is Problem 2: 82 dB across 10 m² gives 1.535 mW. For the phase experiment, velocity magnitude stays fixed at pᵣₘₛ/413 while phase changes; nonzero phase represents a different field, not a single travelling plane wave. At 90° average flow is zero.</p>';
}
function benchTransmission4(){
  const b=bench('bench-transmission4','Twice the pressure, a thousandth of the power','lecture 4 · problem 3');if(!b)return;
  const st={ratio:1.48e6/413,reverse:0};
  const ratioControl=slider(b.ctl,{label:'water / air impedance ratio',min:1,max:10000,log:true,value:st.ratio,fmt:v=>v.toFixed(1),onchange:v=>{st.ratio=v;upd();}});
  ratioControl.el.querySelector('input').step='any'; ratioControl.set(st.ratio);
  segCtl(b.ctl,st,'reverse',[[0,'Air → water'],[1,'Water → air']],upd);
  const ro=readouts(b.ctl,[{id:'T',label:'transmitted pressure / incident'},{id:'tau',label:'transmitted power fraction'},{id:'A',label:'intensity attenuation'}]);
  const plot=new Plot(b.plot,{xmin:1,xmax:10000,ymin:0,ymax:35,xlabel:'impedance ratio',ylabel:'intensity attenuation (dB)',xfmt:v=>v.toFixed(0)});
  function upd(){const a=transmission4(st.reverse?413*st.ratio:413,st.reverse?413:413*st.ratio);ro({T:a.T.toFixed(6),tau:(100*a.tau).toFixed(4)+' %',A:a.atten.toFixed(3)+' dB'});plot.set({series:[{name:'either direction',color:DOMC.ac,pts:logspace(1,10000,201).map(x=>[x,transmission4(1,x).atten])}],markers:[{x:st.ratio,y:a.atten,label:a.atten.toFixed(2)+' dB'}]});}
  upd();b.note.innerHTML='<p>Swap direction: the pressure transmission changes dramatically, but power transmission stays the same. These are ideal lossless media at normal incidence: the remaining energy is reflected, not dissipated.</p>';
}
function benchAbsorption4(){
  const b=bench('bench-absorption4','Read absorbed power from standing-wave extrema','lecture 4 · problem 4 and exam A');if(!b)return;
  const st={min:74,delta:11,S:0.01};const controls={};
  for(const [key,label,min,max,step,unit] of [['min','minimum SPL',40,100,0.1,'dB'],['delta','maximum − minimum',0,40,0.1,'dB'],['S','tube area',0.001,0.02,0.0001,'m²']])controls[key]=slider(b.ctl,{label,min,max,step,value:st[key],unit,fmt:v=>v.toFixed(key==='S'?5:1),onchange:v=>{st[key]=v;upd();}});
  Object.values(controls).forEach(c=>{c.el.querySelector('input').step='any';});
  b.ctl.append(h('button',{type:'button',class:'chip',onclick:()=>{const R=Math.sqrt(0.9),S=Math.PI*0.05**2,p=Math.sqrt(413*1e-5/S);st.min=LP(p*(1-R));st.delta=20*Math.log10((1+R)/(1-R));st.S=S;Object.entries(controls).forEach(([k,c])=>c.set(st[k]));upd();}},'Exam A preset: 10% absorption, 1 µW'));
  const ro=readouts(b.ctl,[{id:'a',label:'absorption α'},{id:'W',label:'absorbed power'},{id:'LW',label:'sound power level'},{id:'max',label:'maximum SPL'},{id:'I',label:'net intensity'}]);
  const plot=new Plot(b.plot,{xlog:false,xmin:0,xmax:0.5,ymin:40,ymax:110,xlabel:'distance along tube (m)',ylabel:'pressure level (dB)',xfmt:v=>v.toFixed(2)});
  function upd(){const a=absorption4(st.min+st.delta,st.min,st.S);ro({a:a.alpha.toFixed(4),W:(a.W*1e6).toFixed(4)+' µW',LW:a.LW.toFixed(2)+' dB re 1 pW',max:(st.min+st.delta).toFixed(2)+' dB',I:(a.W/st.S*1000).toFixed(4)+' mW/m²'});plot.set({ymin:st.min-3,ymax:st.min+st.delta+3,series:[{name:'1 kHz pressure envelope',color:DOMC.el,pts:linspace(0,0.5,401).map(x=>[x,LP(Math.sqrt(a.pi*a.pi+a.pr*a.pr+2*a.pi*a.pr*Math.cos(2*TAU*1000/CA*x)))])}]});}
  upd();b.note.innerHTML='<p>Problem 4 starts at 85/74 dB: α = 0.686, W = 0.863 µW and Lw = 59.36 dB. The curve uses a pressure maximum as its distance origin; extrema alone do not determine the reflection phase or the wall position. Exam A has no specified frequency; its preset uses this same illustrative 1 kHz plot.</p>';
}
function benchCabinet4(){
  const b=bench('bench-cabinet4','A sealed loudspeaker box is an air spring','lecture 4 · problem 5');if(!b)return;
  const st={V:16,d:150,m:20,x:4};
  for(const [key,label,min,max,step,unit] of [['V','cabinet volume',4,40,1,'litres'],['d','cone diameter',80,250,1,'mm'],['m','moving mass',5,80,1,'g'],['x','peak-to-peak excursion',0.1,4,0.1,'mm']])slider(b.ctl,{label,min,max,step,value:st[key],unit,onchange:v=>{st[key]=v;upd();}});
  const ro=readouts(b.ctl,[{id:'f',label:'natural frequency'},{id:'M',label:'acoustic mass'},{id:'K',label:'acoustic stiffness'},{id:'L',label:'internal SPL'},{id:'p',label:'internal RMS pressure'}]);
  const plot=new Plot(b.plot,{xlog:false,xmin:0.1,xmax:4,ymin:100,ymax:160,xlabel:'peak-to-peak excursion (mm)',ylabel:'internal SPL (dB)',xfmt:v=>v.toFixed(1)});
  function upd(){const a=cabinet4(st.V/1000,st.d/1000,st.m/1000,st.x/1000);ro({f:a.f0.toFixed(2)+' Hz',M:a.M.toFixed(3)+' kg/m⁴',K:(a.K/1e6).toFixed(4)+' MN/m⁵',L:a.L.toFixed(2)+' dB',p:a.p.toFixed(2)+' Pa'});plot.set({series:[{name:'uniform sealed cavity',color:DOMC.el,pts:linspace(0.1,4,101).map(x=>[x,cabinet4(st.V/1000,st.d/1000,st.m/1000,x/1000).L])}],markers:[{x:st.x,y:a.L,label:a.L.toFixed(1)+' dB'}]});}
  upd();b.note.innerHTML='<p>Defaults give 59.07 Hz and 140.85 dB inside the cabinet. The 4 mm limit is peak-to-peak, so peak displacement is 2 mm. Changing mass shifts resonance but cannot change pressure at a prescribed displacement in this ideal model. Suspension stiffness and external radiation loading are neglected.</p>';
}
document.addEventListener('DOMContentLoaded',()=>{benchHelmholtz4();benchPower4();benchTransmission4();benchAbsorption4();benchCabinet4();renderMath();});

/* L5: radiation. Constants as in the official week-5 solutions (ρ = 1.2, c = 344). */
const C5 = 344, RHO5 = 1.2, Z5 = RHO5 * C5, W0 = 1e-12, I0 = 1e-12;
const LW5 = (W) => 10 * Math.log10(Math.max(W, 1e-30) / W0);
const sinc5 = (x) => Math.abs(x) < 1e-9 ? 1 : Math.sin(x) / x;
const dir5 = (x) => Math.abs(x) < 1e-9 ? 1 : 2 * besselJ1(x) / x;
/* monopole: power W (W) seen at distance r (m); p²/ρc holds at any distance */
function monopole5(W, r) {
  const I = W / (4 * Math.PI * r * r), p = Math.sqrt(I * Z5);
  return { I, p, Lp: LP(p), LI: 10 * Math.log10(I / I0), LW: LW5(W) };
}
function monoFromLp5(Lp, r) { const p = PREF * 10 ** (Lp / 20); return p * p / Z5 * 4 * Math.PI * r * r; }
/* one monopole of free-field power W at f; wall at h, or a twin 2h away (in phase / antiphase) */
function wall5(f, h, W) {
  const k = TAU * f / C5, kh = k * h, s = sinc5(2 * kh), Q = Math.sqrt(8 * Math.PI * W / (Z5 * k * k));
  return { k, kh, s, Q, wall: W * (1 + s), pair: 2 * W * (1 + s), dipExact: 2 * W * (1 - s), dipApprox: Z5 * h * h * k ** 4 * Q * Q / (6 * Math.PI), lambda: C5 / f };
}
/* baffled piston of radius a at f; prms measured on axis at r in the baffle, then a matched tube */
function piston5(f, a, prms = 0.1, r = 1) {
  const k = TAU * f / C5, ka = k * a, R1 = 1 - besselJ1(2 * ka) / ka, X1 = struveH1(2 * ka) / ka;
  const Qf = ka * ka / R1, Qrms = TAU * r * prms / (RHO5 * TAU * f), ptube = Z5 / (Math.PI * a * a) * Qrms;
  return { k, ka, R1, X1, Qf, DI: 10 * Math.log10(Qf), th3: ka > 1.6163 ? Math.asin(1.6163 / ka) * 180 / Math.PI : null, th0: ka > 3.8317 ? Math.asin(3.8317 / ka) * 180 / Math.PI : null, Mrad: 8 * RHO5 * a ** 3 / 3, Qrms, ptube, gain: 20 * Math.log10(ptube / prms) };
}
/* incoherent sources of equal power at distances d: level of the nearest from the total */
function sirens5(Ltot, d) {
  const sum = d.reduce((s, x) => s + (d[0] / x) ** 2, 0), ptot = PREF * 10 ** (Ltot / 20), p1 = ptot / Math.sqrt(sum);
  return { sum, p1, L1: LP(p1) };
}

function benchMonopole5() {
  const b = bench("bench-monopole5", "One SPL reading gives intensity and power", "lecture 5 · problems 1, 2 and A"); if (!b) return;
  const st = { W: 20, r: 3 };
  const cW = slider(b.ctl, { label: "sound power <b>W</b>", min: 0.01, max: 1000, log: true, value: st.W, unit: "mW", dom: "ac", fmt: v => v < 1 ? v.toFixed(3) : v.toFixed(2), onchange: v => { st.W = v; upd(); } });
  const cr = slider(b.ctl, { label: "distance <b>r</b>", min: 0.1, max: 100, log: true, value: st.r, unit: "m", fmt: v => v.toFixed(2), onchange: v => { st.r = v; upd(); } });
  const chips = h("div", { class: "chips" });
  chips.append(h("button", { type: "button", class: "chip", onclick: () => { st.W = monoFromLp5(86, 1) * 1e3; st.r = 1; cW.set(st.W); cr.set(1); upd(); } }, "Problem 1: 86 dB at 1 m"));
  chips.append(h("button", { type: "button", class: "chip", onclick: () => { st.W = 20; st.r = 3; cW.set(20); cr.set(3); upd(); } }, "Problem 2: 20 mW"));
  b.ctl.append(chips);
  for (const c of [cW, cr]) c.el.querySelector("input").step = "any"; cW.set(st.W); cr.set(st.r);
  const ro = readouts(b.ctl, [{ id: "p", label: "p_rms at r", dom: "el" }, { id: "Lp", label: "L_p at r", dom: "el" }, { id: "LI", label: "L_I at r (I = p²/ρc)", dom: "ac" }, { id: "L10", label: "L_p at 10 m", dom: "el" }, { id: "LW", label: "L_W re 1 pW", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 0.1, xmax: 100, ymin: 40, ymax: 130, xlabel: "distance r (m)", ylabel: "level (dB)", xfmt: v => Number(v.toPrecision(2)) + " m", yfmt: v => v.toFixed(1), xticks: [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100].map(v => ({ v, l: String(v) })) });
  const rs = logspace(0.1, 100, 200);
  function upd() {
    const W = st.W / 1e3, a = monopole5(W, st.r), a10 = monopole5(W, 10);
    plot.set({ series: [{ name: "L_p (−6 dB per doubling of r)", color: DOMC.el, pts: rs.map(r => [r, monopole5(W, r).Lp]) }, { name: "L_W (does not depend on r)", color: DOMC.ac, pts: rs.map(r => [r, a.LW]) }], markers: [{ x: st.r, y: a.Lp, label: `${a.Lp.toFixed(1)} dB at ${st.r.toFixed(2)} m`, color: DOMC.el }, { x: 10, y: a10.Lp, label: `${a10.Lp.toFixed(2)} dB`, color: DOMC.el, dy: 16 }] });
    ro({ p: `${a.p.toFixed(4)} Pa`, Lp: `${a.Lp.toFixed(2)} dB`, LI: `${a.LI.toFixed(2)} dB`, L10: `${a10.Lp.toFixed(2)} dB`, LW: `${a.LW.toFixed(2)} dB (${(W * 1e3).toFixed(3)} mW)` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problem 2: 20 mW gives <b>82.6 dB at 3 m</b> and 72.15 dB at 10 m (the sheet prints 72.1). The Problem 1 chip sets the power that gives 86 dB at 1 m: <b>L_I = 85.86 dB</b> (0.14 dB below L_p, because ρc = 412.8, not 400) and <b>L_W = 96.86 dB</b> (L_I + 11 dB at 1 m). For a monopole the near-field velocity is in quadrature with the pressure, so <span class="mono">I = p²/ρc</span> holds at any distance and no frequency is needed. Exam A uses the same 1/r law the other way round: the 3 km siren gives 0.0843 Pa, and 75× closer (40 m) gives 6.33 Pa rms, 8.94 Pa peak.</p>`;
}

function benchWall5() {
  const b = bench("bench-wall5", "A wall, a twin, an antiphase twin: the source's own power changes", "lecture 5 · problems 3, 4, 5 · slides 30, 35"); if (!b) return;
  const st = { f: 250, h: 0.10, W: 20 };
  const cf = slider(b.ctl, { label: "frequency <b>f</b>", min: 20, max: 2000, log: true, value: st.f, unit: "Hz", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.f = v; upd(); } });
  const chh = slider(b.ctl, { label: "wall distance <b>h</b> (twin spacing 2h)", min: 0.01, max: 2, log: true, value: st.h, unit: "m", fmt: v => v.toFixed(3), onchange: v => { st.h = v; upd(); } });
  const cw = slider(b.ctl, { label: "free-field power of one source", min: 1, max: 100, log: true, value: st.W, unit: "mW", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.W = v; upd(); } });
  for (const [c, v] of [[cf, st.f], [chh, st.h], [cw, st.W]]) { c.el.querySelector("input").step = "any"; c.set(v); }
  const ro = readouts(b.ctl, [{ id: "kh", label: "kh = 2πfh/c" }, { id: "s", label: "sin 2kh / 2kh" }, { id: "Q", label: "|Q| of one source (peak)", dom: "me" }, { id: "wall", label: "next to the wall", dom: "ac" }, { id: "pair", label: "in-phase pair, total", dom: "ac" }, { id: "dip", label: "antiphase, small-kh formula", dom: "ac" }, { id: "dipx", label: "antiphase, exact", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 0.01, xmax: 20, ymin: -40, ymax: 10, xlabel: "kh", ylabel: "power re one free source (dB)", xfmt: v => Number(v.toPrecision(2)), yfmt: v => v.toFixed(1), xticks: [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20].map(v => ({ v, l: String(v) })) });
  const xs = logspace(0.01, 20, 400), d10 = (x) => 10 * Math.log10(Math.max(x, 1e-12));
  function upd() {
    const a = wall5(st.f, st.h, st.W / 1e3), W = st.W / 1e3;
    plot.set({ series: [
      { name: "rigid wall (×2 → +3 dB)", color: DOMC.ac, pts: xs.map(x => [x, d10(1 + sinc5(2 * x))]) },
      { name: "in-phase twin, total (×4 → +6 dB)", color: DOMC.me, pts: xs.map(x => [x, d10(2 * (1 + sinc5(2 * x)))]) },
      { name: "antiphase twin (dipole), exact", color: DOMC.el, pts: xs.map(x => [x, d10(2 * (1 - sinc5(2 * x)))]) },
      { name: "dipole, small-kh formula (8/6)(kh)²", color: DOMC.el, dash: "5 4", thin: true, pts: xs.map(x => [x, d10(8 / 6 * x * x)]) }],
      markers: [{ x: a.kh, y: d10(a.wall / W), label: `${(a.wall * 1e3).toFixed(1)} mW`, color: DOMC.ac, dy: 16 }, { x: a.kh, y: d10(a.pair / W), label: `${(a.pair * 1e3).toFixed(1)} mW`, color: DOMC.me }, { x: a.kh, y: d10(a.dipExact / W), label: `${(a.dipExact * 1e3).toFixed(2)} mW`, color: DOMC.el, dy: 16 }],
      vlines: [{ x: Math.PI / 2, label: "h = λ/4" }] });
    ro({ kh: a.kh.toFixed(4), s: a.s.toFixed(4), Q: `${(a.Q * 1e3).toFixed(2)}×10⁻³ m³/s`, wall: `${(a.wall * 1e3).toFixed(1)} mW · ${LW5(a.wall).toFixed(1)} dB`, pair: `${(a.pair * 1e3).toFixed(2)} mW`, dip: `${(a.dipApprox * 1e3).toFixed(2)} mW`, dipx: `${(a.dipExact * 1e3).toFixed(2)} mW` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problems 3–5: 250 Hz, h = 0.10 m, 20 mW per source, kh = 0.457. Wall: <b>37.3 mW, 105.7 dB</b>. In-phase twin 20 cm apart: <b>74.7 mW</b> (sheet 74.6 = 2 × 37.3). Antiphase twin: <b>5.56 mW</b> with the slide-35 formula (sheet 5.6), 5.33 mW exact. Slide h towards zero: the wall goes to +3 dB, the twin to +6 dB, the dipole dives at 6 dB per halving of kh (power ∝ f⁴). Past h = λ/4 every curve settles near its "no interaction" value: 0 dB, +3 dB, +3 dB. Each source is held at a fixed |Q|, so the neighbour's pressure on its surface changes the power it delivers.</p>`;
}

function benchPiston5() {
  const b = bench("bench-piston5", "The baffled piston: from half-space monopole to a beam", "lecture 5 · course text §1.6.2 · MC 2"); if (!b) return;
  const st = { f: 50, a: 0.059 };
  const cpf = slider(b.ctl, { label: "frequency <b>f</b>", min: 20, max: 10000, log: true, value: st.f, unit: "Hz", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.f = v; upd(); } });
  slider(b.ctl, { label: "piston radius <b>a</b>", min: 0.01, max: 0.2, step: 0.001, value: st.a, unit: "m", dom: "me", fmt: v => v.toFixed(3), onchange: v => { st.a = v; upd(); } });
  cpf.el.querySelector("input").step = "any"; cpf.set(st.f);
  const ro = readouts(b.ctl, [{ id: "ka", label: "ka" }, { id: "R", label: "R₁ = 1 − J₁(2ka)/ka", dom: "ac" }, { id: "X", label: "X₁ = H₁(2ka)/ka", dom: "me" }, { id: "Q", label: "Q(f) = (ka)²/R₁ · DI" }, { id: "th", label: "−3 dB half-angle · null" }, { id: "M", label: "air mass per side 8ρa³/3", dom: "me" }, { id: "tube", label: "MC 2: 0.1 Pa baffled → tube", dom: "el" }]);
  const stage = h("div", { style: "display:flex;flex-direction:column;gap:8px" });
  const pol = h("div", { style: "width:min(100%,300px);margin:0 auto" }), pl = h("div");
  stage.append(pol, pl); b.plot.append(stage);
  const plot = new Plot(pl, { h: 280, xmin: 0.02, xmax: 10, ymin: 0, ymax: 1.2, xlabel: "ka", ylabel: "R₁, X₁ (re ρc/S)", xfmt: v => Number(v.toPrecision(2)), yfmt: v => v.toFixed(2), xticks: [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10].map(v => ({ v, l: String(v) })) });
  const xs = logspace(0.02, 10, 300);
  const curveR = xs.map(x => [x, 1 - besselJ1(2 * x) / x]), curveX = xs.map(x => [x, struveH1(2 * x) / x]);
  function upd() {
    const a = piston5(st.f, st.a);
    pol.innerHTML = polarSVG([{ fn: (t) => Math.cos(t) >= 0 ? Math.abs(dir5(a.ka * Math.sin(t))) : 0, color: DOMC.ac }], { w: 300 }) + `<div class="small" style="text-align:center">|2J₁(ka sin θ)/(ka sin θ)|, front half space (baffle on the vertical)</div>`;
    plot.set({ series: [{ name: "R₁ (resistance)", color: DOMC.ac, pts: curveR }, { name: "X₁ (air-mass reactance)", color: DOMC.me, pts: curveX }], markers: [{ x: a.ka, y: a.R1, label: `R₁ ${a.R1.toFixed(3)}`, color: DOMC.ac }, { x: a.ka, y: a.X1, label: `X₁ ${a.X1.toFixed(3)}`, color: DOMC.me, dy: 16 }], vlines: [{ x: 3.8317, label: "first null" }] });
    ro({ ka: a.ka.toFixed(4), R: a.R1.toPrecision(4), X: a.X1.toPrecision(4), Q: `${a.Qf.toFixed(2)} · ${a.DI.toFixed(1)} dB`, th: `${a.th3 === null ? "none" : a.th3.toFixed(1) + "°"} · ${a.th0 === null ? "none (ka < 3.83)" : a.th0.toFixed(1) + "°"}`, M: `${(a.Mrad * 1e3).toFixed(2)} g`, tube: `${a.ptube.toFixed(1)} Pa (+${a.gain.toFixed(1)} dB)` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are MC 2: a = 5.9 cm at 50 Hz, ka = 0.054. The polar is a half circle: a monopole on a rigid plane, Q(f) = 2 (3 dB). Fitting a rigid tube of the same cross section turns the tiny load <span class="mono">ρck²/2π</span> into the full <span class="mono">ρc/S</span>, so the same volume velocity gives <b>62.9 Pa</b> (answer c, 62.8 Pa; the spread is the value of c). Now raise f: the beam narrows once ka passes about 1.6, and the first null appears at ka = 3.83. R₁ overshoots to about 1.09 near ka ≈ 2–3, X₁ peaks near ka ≈ 1 and then decays: the air mass stops riding along.</p>`;
}
document.addEventListener('DOMContentLoaded', () => { benchMonopole5(); benchWall5(); benchPiston5(); renderMath(); });

/* L7: absorbers. ρ = 1.2, c = 344 as in the notes; the slide-36 impedance example uses ρc = 414. */
const RHO7 = 1.2, C7 = 344, ZSLIDE7 = 414;
/* α from a locally reacting surface impedance Z (N·s/m³), normalised by zc */
function alphaTheta7(Zr, Zi, th, zc = ZSLIDE7) {
  const c = Math.cos(th), R = cdiv(cx(Zr * c - zc, Zi * c), cx(Zr * c + zc, Zi * c));
  return 1 - (R.re * R.re + R.im * R.im);
}
function paris7(r, x) {
  const q = r * r + x * x, t = Math.abs(x) < 1e-12 ? 1 / (r + 1) : Math.atan(x / (r + 1)) / x;
  return 8 * r / q * (1 - r / q * Math.log((r + 1) ** 2 + x * x) + (r * r - x * x) / q * t);
}
function surface7(Zr, Zi, zc = ZSLIDE7) {
  const R = cdiv(cx(Zr - zc, Zi), cx(Zr + zc, Zi)), r = Zr / zc, x = Zi / zc;
  let num = 0; const N = 2000; for (let i = 0; i < N; i++) { const th = (i + 0.5) / N * Math.PI / 2; num += alphaTheta7(Zr, Zi, th, zc) * Math.sin(2 * th); } num *= Math.PI / 2 / N;
  return { R, r, x, an: 1 - (R.re * R.re + R.im * R.im), ar: paris7(r, x), arNum: num, arWrong: paris7(Zr, Zi) };
}
const swr7 = (n) => 4 / (n + 1 / n + 2);
/* membrane and perforated panel on the same cavity */
function panel7(h, rhoP, L, d, a) {
  const m = rhoP * h, K = RHO7 * C7 * C7 / L, fr = Math.sqrt(K / m) / TAU;
  const P = Math.PI * d * d / 4 / (a * a), leff = h + 0.8 * d, f0 = C7 / TAU * Math.sqrt(P / (L * leff));
  return { m, fr, P, leff, f0, mHole: RHO7 * leff / P, fQuarter: C7 / (4 * L) };
}
/* ISO 354 sample test, then the lecture-hall budget (Sabine 0.16 V/A) */
function reverb7(Vc, Sc, T1, T2, Vh, Tnow, Ttarget, nStud, Astud) {
  const alpha = 0.16 * Vc / Sc * (1 / T2 - 1 / T1), Anow = 0.16 * Vh / Tnow, Atarget = 0.16 * Vh / Ttarget, Ast = nStud * Astud;
  const Amat = Atarget - Anow - Ast, S = Amat / alpha;
  return { alpha, Anow, Atarget, Ast, Amat, S, Sround: Math.ceil(S), Tcheck: 0.16 * Vh / (Anow + Ast + Math.ceil(S) * alpha) };
}

function benchSurface7() {
  const b = bench("bench-surface7", "From a surface impedance to α: normal, oblique, random", "lecture 7 · slides 35–36, 38"); if (!b) return;
  const st = { r: 500, x: 1000, n: 3 };
  slider(b.ctl, { label: "Re Z<sub>n</sub>", min: 10, max: 3000, step: 10, value: st.r, unit: "N·s/m³", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.r = v; upd(); } });
  slider(b.ctl, { label: "Im Z<sub>n</sub>", min: -3000, max: 3000, step: 10, value: st.x, unit: "N·s/m³", dom: "me", fmt: v => v.toFixed(0), onchange: v => { st.x = v; upd(); } });
  slider(b.ctl, { label: "tube: standing-wave ratio <b>n</b>", min: 1, max: 20, step: 0.1, value: st.n, fmt: v => v.toFixed(1), onchange: v => { st.n = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "z", label: "ζ = Z/ρc" }, { id: "R", label: "R(0)" }, { id: "an", label: "α_n = 1 − |R|²", dom: "ac" }, { id: "ar", label: "α_r (Paris)", dom: "ac" }, { id: "bad", label: "α_r, forgot ÷ρc", dom: "el" }, { id: "sw", label: "α₀ from n", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 300, xlog: false, xmin: 0, xmax: 90, ymin: 0, ymax: 1, xlabel: "angle of incidence θ (°)", ylabel: "α(θ)", xfmt: v => v.toFixed(0) + "°", yfmt: v => v.toFixed(2) });
  function upd() {
    const a = surface7(st.r, st.x);
    plot.set({ series: [{ name: "α(θ), locally reacting", color: DOMC.ac, pts: linspace(0, 89.9, 300).map(t => [t, alphaTheta7(st.r, st.x, t * Math.PI / 180)]) }, { name: "α_r (diffuse average)", color: DOMC.me, dash: "5 4", pts: [[0, a.ar], [90, a.ar]] }], markers: [{ x: 0, y: a.an, label: `α_n ${a.an.toFixed(3)}`, color: DOMC.ac, dx: 8 }] });
    ro({ z: `${a.r.toFixed(3)} ${a.x < 0 ? "−" : "+"} j${Math.abs(a.x).toFixed(3)}`, R: `${a.R.re.toFixed(4)} ${a.R.im < 0 ? "−" : "+"} j${Math.abs(a.R.im).toFixed(4)}`, an: a.an.toFixed(4), ar: `${a.ar.toFixed(3)} (∫: ${a.arNum.toFixed(3)})`, bad: a.arWrong.toFixed(4), sw: swr7(st.n).toFixed(3) });
  }
  upd();
  b.note.innerHTML = `<p>Start values are slide 36, <span class="mono">Z = 500 + j1000</span> with ρc = 414: <b>α_n = 0.451</b>, <b>α_r = 0.53</b>. The bracket after α_r is a numerical <span class="mono">∫α(θ) sin2θ dθ</span> and agrees with the closed form. Forgetting to divide by ρc gives 0.0032, the slide's deliberate nonsense. Set Z = 414 + j0: α_n = 1, yet α_r is only about 0.91, because every curve falls to 0 at grazing incidence. Try a real ζ ≈ 1.6 (Z ≈ 660) for the best possible α_r, about 0.95. The SWR slider is the tube method: n = 3 gives 0.75, n = 1 total absorption.</p>`;
}

function benchPanel7() {
  const b = bench("bench-panel7", "Same cavity spring, two masses: the panel or the air in the holes", "lecture 7 · problems 2.1, 2.2 · slides 19–28"); if (!b) return;
  const st = { h: 20, rho: 600, L: 50, d: 10, a: 30 };
  for (const [key, label, min, max, step, unit, dom] of [["h", "panel thickness <b>h</b> (= neck length)", 2, 40, 1, "mm", "me"], ["rho", "panel density", 200, 2500, 50, "kg/m³", "me"], ["L", "cavity depth <b>L</b>", 5, 300, 1, "mm", "ac"], ["d", "hole diameter <b>d</b>", 1, 30, 0.5, "mm", "el"], ["a", "hole spacing <b>a</b>", 5, 100, 1, "mm", "el"]]) slider(b.ctl, { label, min, max, step, value: st[key], unit, dom, fmt: v => String(v), onchange: v => { st[key] = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "m", label: "panel mass m = ρh", dom: "me" }, { id: "fr", label: "membrane f_r = (1/2π)√(ρc²/mL)", dom: "me" }, { id: "P", label: "perforation P = πd²/4a²", dom: "el" }, { id: "f0", label: "perforated f₀ = (c/2π)√(P/L(l+0.8d))", dom: "el" }, { id: "mh", label: "hole mass per area ρ(l+δ)/P", dom: "el" }, { id: "q", label: "porous λ/4 at this depth: c/4L", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 5, xmax: 300, ymin: 1.2, ymax: 4, xlabel: "cavity depth L (mm)", ylabel: "frequency (Hz)", xfmt: v => v.toFixed(0) + " mm", yfmt: v => String(Math.round(10 ** v)), yticks: [20, 50, 100, 200, 500, 1000, 2000, 5000].map(v => Math.log10(v)), xticks: [5, 10, 20, 50, 100, 200, 300].map(v => ({ v, l: String(v) })) });
  const Ls = logspace(5, 300, 200), lg = (v) => Math.log10(v);
  function upd() {
    const g = (L) => panel7(st.h / 1e3, st.rho, L / 1e3, st.d / 1e3, st.a / 1e3), a = g(st.L);
    plot.set({ series: [{ name: "membrane f_r", color: DOMC.me, pts: Ls.map(L => [L, lg(g(L).fr)]) }, { name: "perforated f₀", color: DOMC.el, pts: Ls.map(L => [L, lg(g(L).f0)]) }, { name: "porous layer λ/4 (c/4L)", color: DOMC.ac, dash: "5 4", pts: Ls.map(L => [L, lg(g(L).fQuarter)]) }], markers: [{ x: st.L, y: lg(a.fr), label: `${a.fr.toFixed(1)} Hz`, color: DOMC.me }, { x: st.L, y: lg(a.f0), label: `${a.f0.toFixed(0)} Hz`, color: DOMC.el }] });
    ro({ m: `${a.m.toFixed(2)} kg/m²`, fr: `${a.fr.toFixed(1)} Hz`, P: `${(a.P * 100).toFixed(2)} %`, f0: `${a.f0.toFixed(1)} Hz`, mh: `${a.mHole.toFixed(3)} kg/m² (${(a.m / a.mHole).toFixed(1)}× lighter)`, q: `${a.fQuarter.toFixed(0)} Hz` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problem 2: 20 mm plywood at 600 kg/m³, 50 mm cavity. Solid panel: <b>77 Hz</b> (77.4; 76.9 with the slide's ρc² = 1.4×10⁵). Drill 10 mm holes on a 30 mm grid: P = 8.73 %, <b>432 Hz</b>. The cavity spring is the same in both; the air plugs weigh 0.385 kg/m² against the panel's 12, about 31× lighter, and √31 × 77 ≈ 432. Deepen the cavity: both resonances fall as 1/√L. The dashed line is where a porous layer filling the same depth would start to work (λ/4): for 50 mm that is 1.7 kHz, which is why bass needs resonators.</p>`;
}

function benchReverb7() {
  const b = bench("bench-reverb7", "Test a sample in the reverberation room, then size it for the hall", "lecture 7 · problems 1.1, 1.2 · slide 40"); if (!b) return;
  const st = { T1: 5.2, T2: 3.0, Tnow: 3.1, Tt: 0.8, n: 40 };
  for (const [key, label, min, max, step, unit] of [["T1", "chamber T, empty (200 m³)", 1, 10, 0.1, "s"], ["T2", "chamber T, 10 m² sample", 0.5, 10, 0.1, "s"], ["Tnow", "hall T now (300 m³, no people)", 0.5, 6, 0.1, "s"], ["Tt", "hall target T", 0.3, 2, 0.05, "s"], ["n", "students (0.42 m² each)", 0, 150, 1, ""]]) slider(b.ctl, { label, min, max, step, value: st[key], unit, fmt: v => key === "n" ? v.toFixed(0) : v.toFixed(2), onchange: v => { st[key] = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "al", label: "α = (0.16V/S)(1/T₂ − 1/T₁)", dom: "ac" }, { id: "An", label: "A now · A target", dom: "ac" }, { id: "As", label: "A students", dom: "ac" }, { id: "Am", label: "A the material must add", dom: "ac" }, { id: "S", label: "area needed", dom: "el" }, { id: "T", label: "check: T with that area" }]);
  const plot = new Plot(b.plot, { h: 300, xlog: false, xmin: 0, xmax: 150, ymin: 0, ymax: 3.5, xlabel: "absorber area in the hall (m²)", ylabel: "T₅₀₀ (s)", xfmt: v => v.toFixed(0), yfmt: v => v.toFixed(1) });
  function upd() {
    const a = reverb7(200, 10, st.T1, st.T2, 300, st.Tnow, st.Tt, st.n, 0.42);
    const ok = a.alpha > 0 && a.S > 0;
    plot.set({ series: [{ name: "with the students", color: DOMC.ac, pts: linspace(0, 150, 151).map(S => [S, 48 / (a.Anow + a.Ast + S * Math.max(a.alpha, 0))]) }, { name: "empty hall", color: DOMC.me, dash: "5 4", pts: linspace(0, 150, 151).map(S => [S, 48 / (a.Anow + S * Math.max(a.alpha, 0))]) }], vlines: ok ? [{ x: a.S, label: `${a.S.toFixed(1)} m²` }] : [], markers: [{ x: 0, y: 48 / (a.Anow + a.Ast), label: "students only", dx: 8, dy: -8, color: DOMC.ac }, ...(ok ? [{ x: a.S, y: st.Tt, label: `target ${st.Tt.toFixed(2)} s`, color: DOMC.el }] : [])] });
    ro({ al: a.alpha.toFixed(3), An: `${a.Anow.toFixed(2)} · ${a.Atarget.toFixed(2)} m²`, As: `${a.Ast.toFixed(1)} m²`, Am: `${a.Amat.toFixed(2)} m²`, S: !(a.alpha > 0) ? "T₂ must be below T₁" : a.S <= 0 ? "none needed" : `${a.S.toFixed(1)} m² → ${a.Sround} m²`, T: ok ? `${a.Tcheck.toFixed(3)} s` : "—" });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problem 1: the chamber gives <b>α = 0.451</b> (sheet 0.45). In the hall: A now 15.48 m², target 60.0 m², students 16.8 m², so the material must add 27.7 m², <b>61.4 m² → 62 m²</b>, rounded up, and the check gives 0.797 s. Work in absorption areas, which add; reverberation times do not. Drop the students to zero and see how much more absorber an empty-room design would need. The dashed curve shows the hall without the students.</p>`;
}
document.addEventListener('DOMContentLoaded', () => { benchSurface7(); benchPanel7(); benchReverb7(); renderMath(); });

/* L6: room modes and the diffuse field. c = 343, ρ = 1.2 (RMS pressures) as in the week-6 solutions. */
const C6 = 343, RHO6 = 1.2;
function roomModes6(lx, ly, lz, fmax, c = C6) {
  const out = [], nm = (l) => Math.floor(2 * l * fmax / c);
  for (let i = 0; i <= nm(lx); i++) for (let j = 0; j <= nm(ly); j++) for (let k = 0; k <= nm(lz); k++) {
    if (!i && !j && !k) continue;
    const f = c / 2 * Math.hypot(i / lx, j / ly, k / lz);
    if (f > fmax) continue;
    const nz = (i > 0) + (j > 0) + (k > 0);
    out.push({ n: [i, j, k], f, type: ["", "axial", "tangential", "oblique"][nz], centre: i % 2 === 0 && j % 2 === 0 && k % 2 === 0 });
  }
  return out.sort((a, b) => a.f - b.f);
}
function modeCount6(lx, ly, lz, f, c = C6) {
  const V = lx * ly * lz, S = 2 * (lx * ly + lx * lz + ly * lz), L = 4 * (lx + ly + lz), x = f / c;
  return { V, S, L, obl: 4 * Math.PI * V / 3 * x ** 3, full: 4 * Math.PI * V / 3 * x ** 3 + Math.PI * S / 4 * x ** 2 + L / 8 * x, density: 4 * Math.PI * V / c ** 3 * f * f };
}
/* group equal frequencies (degenerate modes), tolerance in Hz */
function degenerate6(modes, tol = 1e-6) {
  const g = []; for (const m of modes) { const last = g[g.length - 1]; if (last && Math.abs(last.f - m.f) < tol) last.modes.push(m.n); else g.push({ f: m.f, modes: [m.n] }); } return g;
}
/* diffuse-field steady state, Problem 3 */
function roomLevel6(V, T, P1, duty, Lff, rff) {
  const A = 55.3 * V / (C6 * T), zc = RHO6 * C6;
  const p1 = 4 * P1 * zc / A, pff = (PREF * 10 ** (Lff / 20)) ** 2, P2 = pff / zc * 4 * Math.PI * rff * rff, p2 = 4 * P2 * zc / A;
  const L = (x) => 10 * Math.log10(x / PREF ** 2);
  return { A, p1on: Math.sqrt(p1), L1on: L(p1), Leq1: L(p1 * duty), P2, L2: L(p2), Leq: L(p1 * duty + p2), rrev: Math.sqrt(A / (16 * Math.PI)), fS: 2000 * Math.sqrt(T / V) };
}
/* level vs distance, Q = 1: direct + reverberant (with 1 − ᾱ when S is known) */
const lpRel6 = (r, A, abar = 0) => 10 * Math.log10(1 / (4 * Math.PI * r * r) + 4 * (1 - abar) / A);
/* Sabine vs Eyring with absorption on the ceiling only */
function sabEyr6(lx, ly, lz, aCeil, aRest) {
  const V = lx * ly * lz, S = 2 * (lx * ly + lx * lz + ly * lz), A = lx * ly * aCeil + (S - lx * ly) * aRest, ab = A / S;
  const T1 = (lm, a) => 0.04 * lm / a; /* course text §3.4.4: T ≈ 0.04 l_m / ᾱ */
  return { V, S, A, ab, lm: 4 * V / S, sab: 55.3 * V / (C6 * A), eyr: 55.3 * V / (-C6 * S * Math.log(1 - ab)), lm2: Math.PI * lx * ly / (2 * (lx + ly)), T2d: T1(Math.PI * lx * ly / (2 * (lx + ly)), aRest), Tlen: T1(lx, aRest), Twid: T1(ly, aRest), Thgt: T1(lz, (aCeil + aRest) / 2) };
}

function benchRoomModes6() {
  const b = bench("bench-roommodes6", "A room is a 3-D organ pipe: find its modes", "lecture 6 · problems 1, 2 · slides 13–19"); if (!b) return;
  const st = { lx: 5, ly: 4, lz: 3, fmax: 80, fc: 50, T: 0.5 };
  const ctl = {};
  for (const [key, label, min, max, step, unit] of [["lx", "length l<sub>x</sub>", 1, 20, 0.1, "m"], ["ly", "width l<sub>y</sub>", 1, 20, 0.1, "m"], ["lz", "height l<sub>z</sub>", 1, 10, 0.1, "m"], ["fmax", "list modes up to", 30, 250, 1, "Hz"], ["T", "reverberation time (for f_S)", 0.2, 5, 0.1, "s"]]) ctl[key] = slider(b.ctl, { label, min, max, step, value: st[key], unit, fmt: v => key === "fmax" ? v.toFixed(0) : v.toFixed(1), onchange: v => { st[key] = v; upd(); } });
  segCtl(b.ctl, st, "fc", [[31.5, "31.5"], [40, "40"], [50, "50"], [63, "63"], [80, "80"], [100, "100"], [125, "125 Hz"]], () => upd());
  const chips = h("div", { class: "chips" });
  for (const [lab, d, fm] of [["Problem 1: 5 × 4 × 3 m", [5, 4, 3], 80], ["Problem 2: 3 m cube", [3, 3, 3], 130], ["Slide 16 room 5.7 × 7.0 × 4.8", [5.7, 7, 4.8], 80], ["Lab room 4.38 × 3.13 × 3.29", [4.38, 3.13, 3.29], 80]]) chips.append(h("button", { type: "button", class: "chip", onclick: () => { [st.lx, st.ly, st.lz] = d; st.fmax = fm; for (const k of ["lx", "ly", "lz", "fmax"]) ctl[k].set(st[k]); upd(); } }, lab));
  b.ctl.append(chips);
  const ro = readouts(b.ctl, [{ id: "ax", label: "axial building blocks c/2l" }, { id: "N", label: "modes ≤ f_max: counted · N(f) formula" }, { id: "band", label: "modes in the third-octave band", dom: "ac" }, { id: "cen", label: "pressure max at the centre (all indices even)", dom: "el" }, { id: "deg", label: "degenerate groups" }, { id: "fs", label: "Schroeder f_S ≈ 2000√(T/V)" }]);
  const pl1 = h("div"), pl2 = h("div"), list = h("div", { class: "small", style: "font-family:var(--font-mono);line-height:1.6;margin-top:6px" });
  b.plot.append(pl1, list, pl2);
  const plot = new Plot(pl1, { h: 240, xlog: false, xmin: 0, xmax: 80, ymin: 0, ymax: 3.4, ml: 84, xlabel: "frequency (Hz)", ylabel: "", xfmt: v => v.toFixed(1) + " Hz", yfmt: v => ["", "oblique", "tangential", "axial"][Math.round(v)] || "", yticks: [1, 2, 3] });
  const plot2 = new Plot(pl2, { h: 220, xlog: false, xmin: 0, xmax: 80, ymin: 0, ymax: 10, xlabel: "frequency (Hz)", ylabel: "modes below f", xfmt: v => v.toFixed(0) + " Hz", yfmt: v => v.toFixed(1) });
  const H6 = { axial: 3, tangential: 2, oblique: 1 }, COL = { axial: DOMC.el, tangential: DOMC.me, oblique: DOMC.ac };
  function upd() {
    const ms = roomModes6(st.lx, st.ly, st.lz, st.fmax), fl = st.fc / 2 ** (1 / 6), fu = st.fc * 2 ** (1 / 6);
    const sticks = (t) => ms.filter(m => m.type === t).flatMap(m => [[m.f, 0], [m.f, H6[t]], [m.f, NaN]]);
    plot.set({ xmax: st.fmax, series: ["axial", "tangential", "oblique"].map(t => ({ name: t, color: COL[t], width: 2.5, pts: sticks(t) })), regions: [{ from: fl, to: fu, color: DOMC.ac, label: `${st.fc} Hz band` }] });
    const fs = linspace(0, st.fmax, 300), cnt = (f) => ms.filter(m => m.f <= f).length;
    const mc = modeCount6(st.lx, st.ly, st.lz, st.fmax);
    plot2.set({ xmax: st.fmax, ymax: Math.max(4, mc.full * 1.15, ms.length * 1.15), series: [{ name: "counted", color: DOMC.ink, pts: fs.map(f => [f, cnt(f)]) }, { name: "N(f), all three terms", color: DOMC.el, pts: fs.map(f => [f, modeCount6(st.lx, st.ly, st.lz, f).full]) }, { name: "oblique term 4πVf³/3c³ only", color: DOMC.ac, dash: "5 4", pts: fs.map(f => [f, modeCount6(st.lx, st.ly, st.lz, f).obl]) }] });
    list.innerHTML = ms.slice(0, 24).map(m => `<span style="color:${COL[m.type]}">(${m.n.join(",")}) ${m.f.toFixed(1)}</span>${m.centre ? "●" : ""}`).join(" · ") + (ms.length > 24 ? ` · … ${ms.length - 24} more` : "") + `<br><span style="color:var(--ink-3)">● = pressure maximum at the room centre</span>`;
    const inb = ms.filter(m => m.f >= fl && m.f <= fu), deg = degenerate6(ms, 1e-6).filter(g => g.modes.length > 1);
    ro({ ax: [st.lx, st.ly, st.lz].map(l => (C6 / (2 * l)).toFixed(2)).join(" · ") + " Hz", N: `${ms.length} · ${mc.full.toFixed(1)}`, band: `${fl.toFixed(1)}–${fu.toFixed(1)} Hz: ${inb.length ? inb.map(m => `(${m.n.join(",")}) ${m.f.toFixed(1)}`).join(", ") : "none"}`, cen: ms.filter(m => m.centre).map(m => `(${m.n.join(",")})`).join(", ") || "none", deg: deg.length ? deg.map(g => `${g.f.toFixed(1)} Hz ×${g.modes.length}`).join(" · ") : "none", fs: `${(2000 * Math.sqrt(st.T / (st.lx * st.ly * st.lz))).toFixed(0)} Hz` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problem 1, the 5 × 4 × 3 m room up to 80 Hz: <b>34.3, 42.9, 54.9, 57.2, 66.7, 68.6, 71.5, 79.3 Hz</b>. Only (2,0,0) has a pressure maximum at the centre, because an odd index puts a nodal plane through the middle. The 50 Hz band (44.5–56.1 Hz) holds only (1,1,0). The 3 m cube chip gives Problem 2's degenerate groups at <b>57, 81, 114 and 128 Hz</b>; (1,1,1) at 99 Hz has no partner. The lower plot is the mode count: the oblique term alone is poor at low frequency, while the three-term formula gives 8.6 against 8 counted. The modal density grows as Vf², and the Schroeder frequency marks where the modes overlap and the diffuse-field statistics take over. (The 1-D version of this is the closed–closed tube on the lecture 2 bench.)</p>`;
}

function benchRoomLevel6() {
  const b = bench("bench-roomlevel6", "The diffuse field: energy in = energy absorbed", "lecture 6 · problem 3 · slides 22–24, 47–51"); if (!b) return;
  const st = { V: 210, T: 3.1, P: 10, duty: 1 / 3, Lff: 70 };
  for (const [key, label, min, max, step, unit, fmt] of [["V", "room volume V", 20, 5000, 10, "m³", v => v.toFixed(0)], ["T", "reverberation time T (500 Hz octave)", 0.2, 6, 0.1, "s", v => v.toFixed(1)], ["P", "source 1 power", 0.1, 100, 0.1, "mW", v => v.toFixed(1)], ["duty", "source 1 on-fraction", 0.05, 1, 0.01, "", v => v.toFixed(2)], ["Lff", "source 2: free-field L_p at 4 m", 40, 100, 0.5, "dB", v => v.toFixed(1)]]) { const c = slider(b.ctl, { label, min, max, step, value: st[key], unit, fmt, onchange: v => { st[key] = v; upd(); } }); if (key === "duty") { c.el.querySelector("input").step = "any"; c.set(st.duty); } }
  const ro = readouts(b.ctl, [{ id: "A", label: "A = 55.3V/(cT)", dom: "ac" }, { id: "on", label: "source 1 on: p_rms · L_p", dom: "el" }, { id: "eq1", label: "L_eq, source 1", dom: "el" }, { id: "s2", label: "source 2: power · reverberant L_p", dom: "me" }, { id: "eq", label: "L_eq, both (add p²)", dom: "ac" }, { id: "rr", label: "reverberation distance √(A/16π)" }, { id: "fs", label: "Schroeder f_S" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 0.1, xmax: 30, ymin: -40, ymax: 10, xlabel: "distance from source r (m)", ylabel: "L_p − L_W (dB), Q = 1", xfmt: v => Number(v.toPrecision(2)) + " m", yfmt: v => v.toFixed(0), xticks: [0.1, 0.2, 0.5, 1, 2, 5, 10, 20].map(v => ({ v, l: String(v) })) });
  const rs = logspace(0.1, 30, 200);
  function upd() {
    const a = roomLevel6(st.V, st.T, st.P / 1e3, st.duty, st.Lff, 4);
    plot.set({ series: [{ name: "direct + reverberant", color: DOMC.ac, pts: rs.map(r => [r, lpRel6(r, a.A)]) }, { name: "direct only (free field)", color: DOMC.el, dash: "5 4", pts: rs.map(r => [r, 10 * Math.log10(1 / (4 * Math.PI * r * r))]) }, { name: "reverberant only, 10 log(4/A)", color: DOMC.me, dash: "2 4", pts: rs.map(r => [r, 10 * Math.log10(4 / a.A)]) }], vlines: [{ x: a.rrev, label: `r_rev ${a.rrev.toFixed(2)} m` }] });
    ro({ A: `${a.A.toFixed(2)} m²`, on: `${a.p1on.toFixed(3)} Pa · ${a.L1on.toFixed(1)} dB`, eq1: `${a.Leq1.toFixed(1)} dB`, s2: `${(a.P2 * 1e3).toFixed(2)} mW · ${a.L2.toFixed(1)} dB`, eq: `${a.Leq.toFixed(1)} dB`, rr: `${a.rrev.toFixed(2)} m`, fs: `${a.fS.toFixed(0)} Hz` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problem 3: 210 m³, T = 3.1 s, so A = 10.9 m². Source 1 (10 mW, on 5 of every 15 min) gives 1.23 Pa, 95.8 dB while on and <b>L_eq = 91.0 dB</b>: average p², not dB, so −4.8 dB for one third of the time. Source 2 (70 dB at 4 m in free field, 1.95 mW) gives 88.7 dB in the room, and both together <b>93.0 dB</b>. The reverberation distance is only 0.47 m, so the reverberant formula holds almost everywhere. Raise T and watch the plateau climb 3 dB for every doubling; the direct line never moves.</p>`;
}

function benchSabine6() {
  const b = bench("bench-sabine6", "Sabine, Eyring, and a room that ignores both", "lecture 6 · slides 25–34 · course text §3.4.4"); if (!b) return;
  const st = { lx: 20, ly: 10, lz: 5, ac: 0.8, ar: 0.1 };
  for (const [key, label, min, max, step, unit] of [["lx", "length", 2, 40, 0.5, "m"], ["ly", "width", 2, 30, 0.5, "m"], ["lz", "height", 2, 15, 0.5, "m"], ["ac", "ceiling α", 0.01, 0.99, 0.01, ""], ["ar", "walls and floor α", 0.01, 0.99, 0.01, ""]]) slider(b.ctl, { label, min, max, step, value: st[key], unit, dom: key[0] === "a" ? "ac" : "", fmt: v => v.toFixed(key[0] === "a" ? 2 : 1), onchange: v => { st[key] = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "VS", label: "V · S · ᾱ" }, { id: "sab", label: "Sabine 0.16V/(Sᾱ)", dom: "ac" }, { id: "eyr", label: "Eyring 0.16V/(−S ln(1−ᾱ))", dom: "ac" }, { id: "d2", label: "2-D horizontal (l_m = πS_x/U)", dom: "el" }, { id: "dir", label: "1-D: length · width · height", dom: "el" }]);
  const plot = new Plot(b.plot, { h: 300, xlog: false, xmin: 0.01, xmax: 1, ymin: 0, ymax: 4, xlabel: "mean absorption coefficient ᾱ", ylabel: "T (s)", xfmt: v => v.toFixed(2), yfmt: v => v.toFixed(1) });
  function upd() {
    const a = sabEyr6(st.lx, st.ly, st.lz, st.ac, st.ar), xs = linspace(0.01, 0.99, 200);
    const ymax = Math.max(1, Math.min(10, a.sab * 3));
    plot.set({ ymax, series: [{ name: "Sabine", color: DOMC.ac, pts: xs.map(x => [x, 55.3 * a.V / (C6 * a.S * x)]) }, { name: "Eyring", color: DOMC.me, pts: xs.map(x => [x, 55.3 * a.V / (-C6 * a.S * Math.log(1 - x))]) }], markers: [{ x: a.ab, y: a.sab, label: `${a.sab.toFixed(2)} s`, color: DOMC.ac }, { x: a.ab, y: a.eyr, label: `${a.eyr.toFixed(2)} s`, color: DOMC.me, dy: 16 }], vlines: [{ x: 0.3, label: "ᾱ = 0.3" }] });
    ro({ VS: `${a.V.toFixed(0)} m³ · ${a.S.toFixed(0)} m² · ${a.ab.toFixed(3)}`, sab: `${a.sab.toFixed(2)} s`, eyr: `${a.eyr.toFixed(2)} s`, d2: `${a.T2d.toFixed(1)} s (l_m ${a.lm2.toFixed(1)} m)`, dir: `${a.Tlen.toFixed(1)} · ${a.Twid.toFixed(1)} · ${a.Thgt.toFixed(1)} s` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are slide 30 (text Fig. 3.4.3): 20 × 10 × 5 m, ceiling α = 0.8, the rest 0.1, so A = 210 m² and ᾱ = 0.30. Sabine gives <b>0.77 s</b> and Eyring <b>0.65 s</b>. They agree below ᾱ ≈ 0.3, and only Eyring goes to zero for an anechoic room. The 2-D and 1-D readouts follow sound travelling only horizontally or along one axis, with the text's T ≈ 0.04 l_m/ᾱ: 4.2 s horizontally, 8.0 / 4.0 / 0.4 s along length, width and height. Horizontally the sound never meets the ceiling. With all the absorption on one surface the real decay is bent and much longer than either formula, and scattering objects pull it back towards Sabine.</p>`;
}
document.addEventListener('DOMContentLoaded', () => { benchRoomModes6(); benchRoomLevel6(); benchSabine6(); renderMath(); });

/* Lab: room 4.38 × 3.13 × 3.29 m (x length, y width, z height), V = 45.1 m³; c = 331.3 + 0.606 θ */
const LAB = { lx: 4.38, ly: 3.13, lz: 3.29, V: 45.1, S: 76.8 };
const cAir = (theta) => 331.3 + 0.606 * theta;
const AW_OCT = [[125, -16.1], [250, -8.6], [500, -3.2], [1000, 0], [2000, 1.2], [4000, 1.0]];
/* synthetic ensemble-averaged decay: main slope T1, a tail at tailDb (re start) with slope T2, a floor SNR dB down */
function decayLab(T1, tailDb, T2, snr, t) {
  const w = 10 ** (tailDb / 10), e = (1 - w) * 10 ** (-6 * t / T1) + w * 10 ** (-6 * t / T2) + 10 ** (-snr / 10);
  return 10 * Math.log10(e / (1 + 10 ** (-snr / 10)));
}
function decayTimes(T1, tailDb, T2, snr) {
  const cross = (L) => { let a = 0, b = 60; if (decayLab(T1, tailDb, T2, snr, b) > L) return null; for (let i = 0; i < 80; i++) { const m = (a + b) / 2; if (decayLab(T1, tailDb, T2, snr, m) > L) a = m; else b = m; } return (a + b) / 2; };
  const t5 = cross(-5), t25 = cross(-25), t35 = cross(-35);
  return { t5, t25, t35, T20: t25 === null ? null : 3 * (t25 - t5), T30: t35 === null ? null : 2 * (t35 - t5) };
}
/* part C: per-octave Lp (position-averaged) and T → L_W, A-weighted, total L_WA */
function soundPowerLab(Lp, T, V = LAB.V) {
  const bands = Lp.map((L, i) => {
    const LW = L - 14 + 10 * Math.log10(V) - 10 * Math.log10(T[i]);
    const p2 = (PREF * 10 ** (L / 20)) ** 2, A = 0.161 * V / T[i], W = p2 * A / (4 * 1.2 * 343);
    return { f: AW_OCT[i][0], LW, LWA: LW + AW_OCT[i][1], LWexact: 10 * Math.log10(W / 1e-12), A };
  });
  return { bands, LWA: 10 * Math.log10(bands.reduce((s, b) => s + 10 ** (b.LWA / 10), 0)), LW: 10 * Math.log10(bands.reduce((s, b) => s + 10 ** (b.LW / 10), 0)) };
}

function benchLabModes() {
  const b = bench("bench-labmodes", "The lab room's lowest modes, and where to find their minima", "lab · preparation (i) · part A"); if (!b) return;
  const st = { th: 20 };
  slider(b.ctl, { label: "room temperature θ", min: 10, max: 30, step: 0.5, value: 20, unit: "°C", dom: "el", fmt: v => v.toFixed(1), onchange: v => { st.th = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "c", label: "c = 331.3 + 0.606 θ" }, { id: "fs", label: "Schroeder f_S, T = 2–10 s" }]);
  const pl = h("div"), tbl = h("div", { class: "table-wrap" });
  b.plot.append(pl, tbl);
  const COL = { axial: DOMC.el, tangential: DOMC.me, oblique: DOMC.ac }, H = { axial: 3, tangential: 2, oblique: 1 };
  const plot = new Plot(pl, { h: 220, xlog: false, xmin: 30, xmax: 90, ymin: 0, ymax: 3.4, ml: 84, xlabel: "frequency (Hz)", ylabel: "", xfmt: v => v.toFixed(1) + " Hz", yfmt: v => ["", "oblique", "tangential", "axial"][Math.round(v)] || "", yticks: [1, 2, 3] });
  const where = (n) => ["length", "width", "height"].map((d, i) => n[i] ? `${n[i]} along the ${d}` : "").filter(Boolean).join(", ");
  function upd() {
    const c = cAir(st.th), ms = roomModes6(LAB.lx, LAB.ly, LAB.lz, 90, c);
    plot.set({ series: ["axial", "tangential", "oblique"].map(t => ({ name: t, color: COL[t], width: 2.5, pts: ms.filter(m => m.type === t).flatMap(m => [[m.f, 0], [m.f, H[t]], [m.f, NaN]]) })) });
    tbl.innerHTML = `<table><tr><th>#</th><th>mode</th><th>type</th><th>predicted</th><th>pressure minima to find</th><th>measured</th></tr>${ms.slice(0, 7).map((m, i) => `<tr><td>${i < 5 ? i + 1 : "(" + (i + 1) + ")"}</td><td>(${m.n.join(",")})</td><td style="color:${COL[m.type]}">${m.type}</td><td>${m.f.toFixed(1)} Hz</td><td>${where(m.n)}</td><td class="small">fill in after the lab</td></tr>`).join("")}</table>`;
    ro({ c: `${c.toFixed(2)} m/s`, fs: `${(2000 * Math.sqrt(2 / LAB.V)).toFixed(0)}–${(2000 * Math.sqrt(10 / LAB.V)).toFixed(0)} Hz` });
  }
  upd();
  b.note.innerHTML = `<p>At 20 °C (c = 343.4 m/s) the five lowest modes are <b>39.2 (1,0,0), 52.2 (0,0,1), 54.9 (0,1,0), 65.3 (1,0,1), 67.4 (1,1,0) Hz</b>. The room is taller than it is wide, so the height mode comes before the width mode. Each kelvin moves every mode by about +0.17 %. The two close pairs, 52/55 and 65/67 Hz, need a slow sweep in steps of about 0.2 Hz; the minima pattern tells them apart. The same room also fits on the lecture 6 mode finder.</p>`;
}

function benchDecayLab() {
  const b = bench("bench-decaylab", "T20 or T30? A decay with a slow tail and a noise floor", "lab · part B"); if (!b) return;
  const st = { T1: 2, tail: -60, T2: 6, snr: 60 };
  for (const [key, label, min, max, step, unit] of [["T1", "main decay T", 0.3, 10, 0.1, "s"], ["tail", "slow tail level (−60 = none)", -60, -10, 1, "dB"], ["T2", "tail decay T", 0.5, 20, 0.1, "s"], ["snr", "SNR (start level − noise floor)", 20, 80, 1, "dB"]]) slider(b.ctl, { label, min, max, step, value: st[key], unit, fmt: v => v.toFixed(key === "T1" || key === "T2" ? 1 : 0), onchange: v => { st[key] = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "t20", label: "T20 = 3(t₋₂₅ − t₋₅)", dom: "ac" }, { id: "t30", label: "T30 = 2(t₋₃₅ − t₋₅)", dom: "me" }, { id: "nf", label: "no floor: T20 · T30" }, { id: "v", label: "verdict", dom: "el" }]);
  const plot = new Plot(b.plot, { h: 300, xlog: false, xmin: 0, xmax: 4, ymin: -80, ymax: 5, xlabel: "time after the cut (s)", ylabel: "level (dB re start)", xfmt: v => v.toFixed(2) + " s", yfmt: v => v.toFixed(0) });
  function upd() {
    const d = decayTimes(st.T1, st.tail, st.T2, st.snr), d0 = decayTimes(st.T1, st.tail, st.T2, 200);
    const tmax = Math.min(30, Math.max(1.5 * (d0.T30 || st.T1), 1.2 * st.T1)), ts = linspace(0, tmax, 400);
    const fit = (t0, T) => T === null ? [] : [[t0, -5], [tmax, -5 - 60 * (tmax - t0) / T]];
    plot.set({ xmax: tmax, series: [{ name: "decay (ensemble average)", color: DOMC.ink, pts: ts.map(t => [t, decayLab(st.T1, st.tail, st.T2, st.snr, t)]) }, { name: "T20 line", color: DOMC.ac, dash: "5 4", pts: fit(d.t5, d.T20) }, { name: "T30 line", color: DOMC.me, dash: "5 4", pts: fit(d.t5, d.T30) }], vlines: [d.t25, d.t35].filter(x => x !== null).map((x, i) => ({ x, label: i ? "−35 dB" : "−25 dB" })) });
    const f = (x) => x === null ? "never reached" : `${x.toFixed(2)} s`;
    const ratio = d.T20 && d.T30 ? d.T30 / d.T20 : null;
    ro({ t20: f(d.T20), t30: f(d.T30), nf: `${f(d0.T20)} · ${f(d0.T30)}`, v: st.snr < 35 ? "SNR < 35 dB: even T20 is unsafe" : st.snr < 45 ? "SNR < 45 dB: T30 reads into the floor; use T20" : ratio && ratio > 1.1 ? `T30/T20 = ${ratio.toFixed(2)}: double slope, not diffuse` : "straight decay: T20 ≈ T30, use T30" });
  }
  upd();
  b.note.innerHTML = `<p>This is a simplified model, not the lab script. It uses a smooth, ensemble-averaged energy envelope: two exponential slopes plus a constant noise floor. T20 and T30 are read from the −5/−25/−35 dB crossings rather than from a regression on the Schroeder integral, so a real single decay will be noisier. The start is a healthy 2 s decay with 60 dB SNR, where T20 = T30. Lower the SNR below about 45 dB and the −35 dB point sinks into the floor, so <b>T30 runs long</b> while T20 holds. Lower it below about 30 dB and T20 goes too. Raise the tail level to about −20 dB with a 6 s tail: T30 &gt; T20 even with no noise, which is the double slope of a room with all its absorption on one wall.</p>`;
}

function benchSoundPowerLab() {
  const b = bench("bench-soundpowerlab", "Part C: the vacuum cleaner's sound power from L_p and T", "lab · part C"); if (!b) return;
  const EX_L = [72, 74, 75, 74, 71, 67], EX_T = [3.0, 2.6, 2.4, 2.2, 1.9, 1.5];
  const st = { L: EX_L.slice(), T: EX_T.slice() };
  const grid = h("div", { style: "display:grid;grid-template-columns:auto 1fr 1fr;gap:4px 8px;align-items:center;font-size:12.5px" });
  grid.append(h("span", {}, "octave"), h("span", {}, "L_p (dB, p² averaged)"), h("span", {}, "T (s)"));
  const inp = (arr, i, step) => { const e = h("input", { type: "number", step, value: arr[i], style: "width:100%;font:inherit" }); e.addEventListener("input", () => { const v = Number(e.value); if (isFinite(v) && v > 0) { arr[i] = v; upd(); } }); return e; };
  AW_OCT.forEach(([f], i) => grid.append(h("span", {}, f >= 1000 ? `${f / 1000}k` : String(f)), inp(st.L, i, "0.1"), inp(st.T, i, "0.01")));
  b.ctl.append(grid);
  const ro = readouts(b.ctl, [{ id: "LW", label: "total L_W (unweighted)", dom: "ac" }, { id: "LWA", label: "total L_WA", dom: "el" }, { id: "chk", label: "check vs p²A/4ρc route" }]);
  const tbl = h("div", { class: "table-wrap" });
  const pl = h("div"); b.plot.append(pl, tbl);
  const plot = new Plot(pl, { h: 260, xmin: 90, xmax: 5600, ymin: 40, ymax: 100, xlabel: "octave band", ylabel: "dB re 1 pW", xticks: AW_OCT.map(([f]) => ({ v: f, l: f >= 1000 ? f / 1000 + "k" : String(f) })), yfmt: v => v.toFixed(0) });
  function upd() {
    const r = soundPowerLab(st.L, st.T);
    plot.set({ series: [{ name: "L_W per band", color: DOMC.ac, pts: r.bands.map(x => [x.f, x.LW]) }, { name: "L_WA per band", color: DOMC.el, pts: r.bands.map(x => [x.f, x.LWA]) }], markers: r.bands.map(x => ({ x: x.f, y: x.LWA, color: DOMC.el })) });
    tbl.innerHTML = `<table><tr><th>octave</th>${r.bands.map(x => `<th>${x.f >= 1000 ? x.f / 1000 + "k" : x.f}</th>`).join("")}</tr><tr><td>A (m²) = 0.161V/T</td>${r.bands.map(x => `<td>${x.A.toFixed(2)}</td>`).join("")}</tr><tr><td>L_W</td>${r.bands.map(x => `<td>${x.LW.toFixed(1)}</td>`).join("")}</tr><tr><td>A-weighting</td>${AW_OCT.map(a => `<td>${a[1] > 0 ? "+" : ""}${a[1]}</td>`).join("")}</tr><tr><td>L_WA</td>${r.bands.map(x => `<td>${x.LWA.toFixed(1)}</td>`).join("")}</tr></table>`;
    const dev = Math.max(...r.bands.map(x => Math.abs(x.LW - x.LWexact)));
    ro({ LW: `${r.LW.toFixed(1)} dB`, LWA: `${r.LWA.toFixed(1)} dB(A)`, chk: `max ${dev.toFixed(2)} dB difference` });
  }
  upd();
  b.note.innerHTML = `<p><b>The start values are made-up examples, not measurements: fill in after the lab.</b> Use the p² averaged over the three positions (then 10 log) and the chosen T20 or T30 per band. Each band uses <span class="mono">L_W = L_p − 14 + 10 log V − 10 log T</span> with V = 45.1 m³, so 10 log V = 16.5 dB. The check computes <span class="mono">W = p²A/4ρc</span> directly; the "−14" absorbs ρc ≈ 400, which leaves a difference of about 0.1 dB. A household vacuum cleaner is typically 75–85 dB(A). A result far outside that range means a units or averaging slip.</p>`;
}
document.addEventListener('DOMContentLoaded', () => { benchLabModes(); benchDecayLab(); benchSoundPowerLab(); renderMath(); });

/* L8: loudspeakers. ρ = 1.2, c = 343 reproduce every printed answer on Problems 8 (rms values). */
const C8 = 343, RHO8 = 1.2, Z8 = RHO8 * C8;
/* baffled driver: p (rms) on axis and at angle th (deg); mass = true drops K and Rt (P3.1) */
function driver8(p, f, th = 0, massOnly = false) {
  const w = TAU * f, S = Math.PI * p.a * p.a, k = w / C8, ka = k * p.a;
  const X = w * p.M - (massOnly ? 0 : p.K / w), R = massOnly ? 0 : p.Rt, Zm = Math.hypot(R, X);
  const Q = S * p.Bl * p.e / (p.Re * Zm), pr = RHO8 * w * Q / (TAU * p.r), x = Q / S / w;
  const s = ka * Math.sin(th * Math.PI / 180), D = Math.abs(s) < 1e-9 ? 1 : Math.abs(2 * besselJ1(s) / s);
  return { S, ka, Zm, Q, p: pr, Lp: LP(pr), Lth: LP(pr * D), D, x, fs: Math.sqrt(p.K / p.M) / TAU, Qt: Math.sqrt(p.K * p.M) / p.Rt, Rel: p.Bl ** 2 / p.Re, pflat: RHO8 * S * p.Bl * p.e / (TAU * p.r * p.Re * p.M) };
}
/* one level reading, spherical (half = false) or hemispherical (half = true) spreading */
function space8(Lp0, r0, r, half) {
  const p0 = PREF * 10 ** (Lp0 / 20), p = p0 * r0 / r, I = p * p / Z8, W = (half ? TAU : 2 * TAU) * r * r * I;
  return { p, Lp: LP(p), LI: 10 * Math.log10(I / 1e-12), W, LW: 10 * Math.log10(W / 1e-12) };
}
/* sealed cavity V (m³) at level Lin, then the same Q as a free-field monopole at r */
function headphone8(V, Lin, f, r, d) {
  const w = TAU * f, CA = V / (RHO8 * C8 * C8), pin = PREF * 10 ** (Lin / 20), Q = w * CA * pin, pf = RHO8 * w * Q / (2 * TAU * r);
  return { CA, pin, Q, pf, Lf: LP(pf), drop: 20 * Math.log10(pf / pin), ka: w / C8 * d / 2 };
}

function benchDriver8() {
  const b = bench("bench-driver8", "One driver in a baffle: spring, mass, then the beam", "lecture 8 · problems 3.1, 3.2 · pages 7–18"); if (!b) return;
  const st = { Bl: 8, Re: 5, a: 6, M: 20, K: 2000, Rt: 18, e: 2.8, th: 0, mass: false };
  const sl = {};
  for (const [key, label, min, max, step, unit, dom] of [["Bl", "force factor <b>Bl</b>", 1, 20, 0.1, "T·m", "el"], ["Re", "coil resistance <b>R_e</b>", 2, 16, 0.1, "Ω", "el"], ["a", "cone radius <b>a</b>", 1, 20, 0.1, "cm", "ac"], ["M", "moving mass <b>M</b>", 2, 150, 1, "g", "me"], ["K", "suspension stiffness <b>K</b>", 100, 10000, 50, "N/m", "me"], ["Rt", "total damping <b>R_t</b>", 0.5, 60, 0.5, "N·s/m", "me"], ["e", "voltage (rms)", 0.5, 20, 0.1, "V", "el"], ["th", "listening angle <b>θ</b>", 0, 90, 1, "°", "ac"]]) sl[key] = slider(b.ctl, { label, min, max, step, value: st[key], unit, dom, fmt: v => String(v), onchange: v => { st[key] = v; upd(); } });
  const chips = h("div", { class: "chips" });
  const mk = (label, on) => h("button", { type: "button", class: "chip" + (st.mass === on ? " on" : ""), onclick: (e) => { st.mass = on; $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, label);
  chips.append(mk("3.2: with K and R_t", false), mk("3.1: mass only", true));
  b.ctl.append(chips);
  const ro = readouts(b.ctl, [{ id: "fs", label: "f_s = (1/2π)√(K/M) · Q_t", dom: "me" }, { id: "rel", label: "electrical damping (Bl)²/R_e", dom: "el" }, { id: "flat", label: "flat level ρS·Bl·e/(2πrR_eM), r = 2 m", dom: "ac" }, { id: "l30", label: "L_p at 30 Hz", dom: "ac" }, { id: "l300", label: "L_p at 300 Hz · Q", dom: "ac" }, { id: "l900", label: "L_p at 900 Hz · Q", dom: "ac" }, { id: "x", label: "excursion at 30 Hz · 300 Hz (rms)", dom: "me" }, { id: "ka", label: "ka = 1 at · first null at θ" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 10, xmax: 10000, ymin: 40, ymax: 100, xlabel: "frequency (Hz)", ylabel: "SPL at 2 m (dB)", yfmt: v => v.toFixed(0) });
  const fs = logspace(10, 10000, 400);
  function upd() {
    const p = { Bl: st.Bl, Re: st.Re, a: st.a / 100, M: st.M / 1000, K: st.K, Rt: st.Rt, e: st.e, r: 2 }, g = (f, th = 0, m = st.mass) => driver8(p, f, th, m);
    const a30 = g(30), a300 = g(300), a900 = g(900), f1 = C8 / (TAU * p.a), s = Math.sin(st.th * Math.PI / 180), fnull = s > 0 ? 3.8317 * C8 / (TAU * p.a * s) : null;
    const series = [{ name: "on axis", color: DOMC.ac, pts: fs.map(f => [f, g(f).Lp]) }, { name: "mass only (no K, R_t)", color: DOMC.me, dash: "5 4", thin: true, pts: fs.map(f => [f, g(f, 0, true).Lp]) }];
    if (st.th > 0) series.push({ name: `at ${st.th}° (piston directivity)`, color: DOMC.el, pts: fs.map(f => [f, Math.max(g(f, st.th).Lth, 0)]) });
    plot.set({ series, markers: [{ x: 30, y: a30.Lp, label: `${a30.Lp.toFixed(2)} dB`, color: DOMC.ac }, { x: 300, y: a300.Lp, label: `${a300.Lp.toFixed(2)}`, color: DOMC.ac, dy: 16 }, { x: 900, y: a900.Lp, label: `${a900.Lp.toFixed(2)}`, color: DOMC.ac }], vlines: [{ x: a30.fs, label: "f_s" }, { x: f1, label: "ka = 1" }], regions: [{ from: 10, to: Math.min(a30.fs, 9000), color: DOMC.me, label: "spring" }, { from: Math.min(a30.fs * 2, 9000), to: Math.min(f1, 10000), color: DOMC.ac, label: "mass: flat" }] });
    ro({ fs: `${a30.fs.toFixed(1)} Hz · ${a30.Qt.toFixed(2)}`, rel: `${a30.Rel.toFixed(1)} N·s/m`, flat: `${LP(a30.pflat).toFixed(2)} dB (${a30.pflat.toFixed(3)} Pa)`, l30: `${a30.Lp.toFixed(2)} dB`, l300: `${a300.Lp.toFixed(2)} dB · ${(a300.Q * 1e3).toFixed(3)}×10⁻³ m³/s`, l900: `${a900.Lp.toFixed(2)} dB · ${(a900.Q * 1e3).toFixed(3)}×10⁻³ m³/s`, x: `${(a30.x * 1e3).toFixed(2)} mm · ${(a300.x * 1e3).toFixed(3)} mm`, ka: `${hz(f1)} · ${fnull ? hz(fnull) : "θ = 0: none"}` });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problem 3: Bl = 8 Tm, R_e = 5 Ω, a = 6 cm, M = 20 g, 2.8 V rms, 2 m in a baffle. With K = 2000 N/m and R_t = 18 N·s/m (3.2): <b>67.49 dB at 30 Hz, 80.96 dB at 300 Hz</b>, f_s = 50.3 Hz. Press "mass only" (3.1): both 300 Hz and 900 Hz give <b>81.65 dB</b>, with Q = 1.344 and 0.448 ×10⁻³ m³/s. A third of the volume velocity at three times the frequency gives the same pressure. Below f_s the curve falls 12 dB/octave; drop R_t to 2 to see the resonance peak, and see how much of the 18 is electrical (12.8). Set θ = 30° or 60°: above ka ≈ 1.6/sin θ the off-axis curve falls away from the on-axis one, which is what page 12 shows for an 8.5 cm cone. Above ka ≈ 1 the real cone also breaks up, so the piston model is only a guide there.</p>`;
}

function benchSpace8() {
  const b = bench("bench-space8", "One SPL reading: free space or a baffle", "lecture 8 · problems 1, 2 · page 5"); if (!b) return;
  const st = { L0: LP(0.1 / Math.SQRT2), r0: 1, r: 0.75, half: false };
  const cL = slider(b.ctl, { label: "measured L_p", min: 40, max: 120, step: 0.01, value: st.L0, unit: "dB", dom: "el", fmt: v => v.toFixed(2), onchange: v => { st.L0 = v; upd(); } });
  const c0 = slider(b.ctl, { label: "measured at r₀", min: 0.1, max: 10, step: 0.05, value: st.r0, unit: "m", fmt: v => v.toFixed(2), onchange: v => { st.r0 = v; upd(); } });
  const cr = slider(b.ctl, { label: "wanted at r", min: 0.1, max: 10, step: 0.05, value: st.r, unit: "m", fmt: v => v.toFixed(2), onchange: v => { st.r = v; upd(); } });
  const chips = h("div", { class: "chips" });
  const set = (L0, r0, r, half) => { Object.assign(st, { L0, r0, r, half }); cL.set(L0); c0.set(r0); cr.set(r); $$(".chip", chips).forEach((x, i) => x.classList.toggle("on", (i === 0) === !half)); upd(); };
  chips.append(h("button", { type: "button", class: "chip on", onclick: () => set(LP(0.1 / Math.SQRT2), 1, 0.75, false) }, "P1: free space (4π)"), h("button", { type: "button", class: "chip", onclick: () => set(78, 2.5, 1, true) }, "P2: infinite baffle (2π)"));
  b.ctl.append(chips);
  const ro = readouts(b.ctl, [{ id: "Lp", label: "L_p at r", dom: "el" }, { id: "LI", label: "L_I at r (I = p²/ρc)", dom: "ac" }, { id: "W", label: "sound power W", dom: "ac" }, { id: "LW", label: "L_W re 1 pW", dom: "ac" }, { id: "alt", label: "L_W with the other spreading law" }]);
  const plot = new Plot(b.plot, { h: 280, xmin: 0.1, xmax: 10, ymin: 40, ymax: 120, xlabel: "distance r (m)", ylabel: "level (dB)", xfmt: v => Number(v.toPrecision(2)) + " m", yfmt: v => v.toFixed(0), xticks: [0.1, 0.2, 0.5, 1, 2, 5, 10].map(v => ({ v, l: String(v) })) });
  const rs = logspace(0.1, 10, 200);
  function upd() {
    const a = space8(st.L0, st.r0, st.r, st.half), o = space8(st.L0, st.r0, st.r, !st.half);
    plot.set({ series: [{ name: "L_p (−6 dB per doubling of r)", color: DOMC.el, pts: rs.map(r => [r, space8(st.L0, st.r0, r, st.half).Lp]) }, { name: "L_W (independent of r)", color: DOMC.ac, pts: [[0.1, a.LW], [10, a.LW]] }], markers: [{ x: st.r0, y: st.L0, label: "reading", color: DOMC.el, dy: 16 }, { x: st.r, y: a.Lp, label: `${a.Lp.toFixed(2)} dB`, color: DOMC.el }] });
    ro({ Lp: `${a.Lp.toFixed(2)} dB`, LI: `${a.LI.toFixed(2)} dB`, W: a.W < 0.01 ? `${(a.W * 1e3).toFixed(4)} mW` : `${a.W.toFixed(4)} W`, LW: `${a.LW.toFixed(2)} dB (${st.half ? "2πr²" : "4πr²"})`, alt: `${o.LW.toFixed(2)} dB (${st.half ? "+" : "−"}3.01 dB)` });
  }
  upd();
  b.note.innerHTML = `<p>P1: a 0.1 Pa amplitude at 1 m is 0.0707 Pa rms, 70.97 dB. At 0.75 m: <b>73.47 dB, L_I 73.34 dB</b>, and through a sphere <b>W = 0.153 mW, L_W 81.84 dB</b>. P2 (chip): 78 dB at 2.5 m in a baffle gives <b>85.96 dB and 85.83 dB at 1 m</b>, and through a hemisphere <b>2.41 mW, 93.82 dB</b>. L_I sits 0.13 dB under L_p because ρc = 411.6, not 400. The last readout shows the 3 dB you lose or gain by picking the wrong spreading law.</p>`;
}

function benchHeadphone8() {
  const b = bench("bench-headphone8", "A headphone on the head, then in free space", "lecture 8 · problem 4 · page 31"); if (!b) return;
  const st = { V: 50, L: 100, f: 100, r: 0.5 };
  for (const [key, label, min, max, step, unit, dom] of [["V", "sealed volume <b>V</b>", 1, 200, 1, "cm³", "ac"], ["L", "level inside the cup", 60, 120, 1, "dB", "el"], ["f", "frequency <b>f</b>", 20, 1000, 1, "Hz", "el"], ["r", "free-field distance <b>r</b>", 0.1, 3, 0.05, "m", ""]]) slider(b.ctl, { label, min, max, step, value: st[key], unit, dom, fmt: v => String(v), onchange: v => { st[key] = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "CA", label: "C_A = V/ρc²", dom: "ac" }, { id: "Q", label: "Q = ωC_A·p_in", dom: "me" }, { id: "Lf", label: "free field L_p = ρωQ/4πr", dom: "el" }, { id: "drop", label: "p_free/p_in = k²V/4πr" }, { id: "ka", label: "ka (40 mm driver)" }]);
  const plot = new Plot(b.plot, { h: 280, xmin: 20, xmax: 1000, ymin: -20, ymax: 120, xlabel: "frequency (Hz)", ylabel: "SPL (dB)", yfmt: v => v.toFixed(0) });
  const fs = logspace(20, 1000, 200);
  function upd() {
    const g = (f) => headphone8(st.V * 1e-6, st.L, f, st.r, 0.04), a = g(st.f);
    plot.set({ series: [{ name: "inside the sealed cup (held at the set level)", color: DOMC.el, pts: [[20, st.L], [1000, st.L]] }, { name: "same Q radiated into free space", color: DOMC.ac, pts: fs.map(f => [f, g(f).Lf]) }], markers: [{ x: st.f, y: a.Lf, label: `${a.Lf.toFixed(2)} dB`, color: DOMC.ac }] });
    ro({ CA: `${sci(a.CA)} m⁵/N`, Q: `${sci(a.Q)} m³/s`, Lf: `${a.Lf.toFixed(2)} dB`, drop: `${a.drop.toFixed(2)} dB`, ka: a.ka.toFixed(3) });
  }
  upd();
  b.note.innerHTML = `<p>Start values are Problem 4: 100 dB in 50 cm³ at 100 Hz needs only Q = 4.45×10⁻⁷ m³/s. The same Q in free space at 0.5 m gives <b>8.53 dB</b> (the sheet's 8.55 is c rounding), 91.5 dB down. In the cup, pressure follows volume <i>displacement</i> (p = Q/jωC_A). In free space it follows volume <i>acceleration</i>, so for the same in-cup level the outside rises 12 dB per octave. A stiffness-controlled diaphragm below its resonance has constant displacement, and that is why a sealed headphone has flat bass. Halve the volume and the same driver gives 6 dB more inside.</p>`;
}
document.addEventListener('DOMContentLoaded', () => { benchDriver8(); benchSpace8(); benchHeadphone8(); renderMath(); });
