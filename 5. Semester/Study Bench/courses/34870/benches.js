/* The Analogy Bench — the playgrounds, one per idea. Each function builds
   its controls, computes the physics live, and draws the plot. */
"use strict";

const FREQ = logspace(10, 20000, 320);

/* ===== L1 · Phasor stage: the three elements as rotating arrows ===== */
function benchPhasor() {
  const b = bench("bench-phasor", "One element, three worlds, one rotating arrow", "lecture 1");
  if (!b) return;
  const ELEM = {
    R: { name: "Real element (R)", phase: 0, el: ["resistor R", "v = R·i"], me: ["damper R<sub>M</sub>", "f = R<sub>M</sub>·u"], ac: ["porous plug R<sub>A</sub>", "p = R<sub>A</sub>·U"], note: "Across and through are <b>in phase</b>. Energy goes in and never comes back — heat." },
    L: { name: "Differentiating element (jω)", phase: 90, el: ["inductor L", "v = jωL·i"], me: ["mass M<sub>M</sub>", "f = jωM<sub>M</sub>·u"], ac: ["open tube M<sub>A</sub>", "p = jωM<sub>A</sub>·U"], note: "Across <b>leads</b> through by 90°. You must push (across) <i>before</i> it moves (through) — inertia." },
    C: { name: "Integrating element (1/jω)", phase: -90, el: ["capacitor C", "v = i / (jωC)"], me: ["spring C<sub>M</sub>", "f = u / (jωC<sub>M</sub>)"], ac: ["closed box C<sub>A</sub>", "p = U / (jωC<sub>A</sub>)"], note: "Across <b>lags</b> through by 90°. It has to move (through) <i>first</i> before it pushes back (across) — a spring." },
  };
  let cur = "L", t0 = performance.now();
  const stage = h("div", { class: "stage" });
  b.plot.append(stage);
  const chips = h("div", { class: "chips" });
  for (const k of ["R", "L", "C"]) chips.append(h("button", { class: "chip" + (k === cur ? " on" : ""), type: "button", onclick: (e) => { cur = k; $$(".chip", chips).forEach(c => c.classList.toggle("on", c === e.target)); draw(); } }, ELEM[k].name));
  b.ctl.append(chips);
  const info = h("div", { class: "small" });
  b.ctl.append(info);
  function draw() {
    const e = ELEM[cur];
    info.innerHTML = `<p style="max-width:none"><span class="tag el">electrical</span> ${e.el[0]} — <span class="mono">${e.el[1]}</span></p><p style="max-width:none"><span class="tag me">mechanical</span> ${e.me[0]} — <span class="mono">${e.me[1]}</span></p><p style="max-width:none"><span class="tag ac">acoustic</span> ${e.ac[0]} — <span class="mono">${e.ac[1]}</span></p>`;
    b.note.innerHTML = `<p>${e.note}</p><p class="muted">The arrows are the phasors <span class="mono">e<sup>jωt</sup></span> rotating counter-clockwise. The trace on the right is what an oscilloscope would show. The <b>through</b> variable (current / velocity / volume velocity) is the grey arrow; the <b>across</b> variable (voltage / force / pressure) is the black one.</p>`;
  }
  draw();
  const W = 640, H = 260;
  function frame(now) {
    if (!stage.isConnected) return;
    const w = (now - t0) / 1000 * 1.2; // rad/s of the demo
    const ph = ELEM[cur].phase * Math.PI / 180;
    const cxp = 130, cyp = 130, R = 85;
    const ax = cxp + R * Math.cos(w + ph), ay = cyp - R * Math.sin(w + ph);
    const tx = cxp + R * 0.7 * Math.cos(w), ty = cyp - R * 0.7 * Math.sin(w);
    let trA = "", trT = "";
    for (let i = 0; i <= 200; i++) { const tt = w - i * 0.05; const x = 280 + i * 1.7; trA += (i ? "L" : "M") + x.toFixed(1) + " " + (cyp - R * Math.sin(tt + ph)).toFixed(1); trT += (i ? "L" : "M") + x.toFixed(1) + " " + (cyp - R * 0.7 * Math.sin(tt)).toFixed(1); }
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}">
      <circle cx="${cxp}" cy="${cyp}" r="${R}" fill="none" stroke="var(--plot-grid)"/>
      <line x1="${cxp - R - 10}" x2="${cxp + R + 10}" y1="${cyp}" y2="${cyp}" stroke="var(--plot-grid)"/><line y1="${cyp - R - 10}" y2="${cyp + R + 10}" x1="${cxp}" x2="${cxp}" stroke="var(--plot-grid)"/>
      <line x1="${cxp}" y1="${cyp}" x2="${tx}" y2="${ty}" stroke="var(--ink-3)" stroke-width="3" stroke-linecap="round"/><circle cx="${tx}" cy="${ty}" r="4" fill="var(--ink-3)"/>
      <line x1="${cxp}" y1="${cyp}" x2="${ax}" y2="${ay}" stroke="var(--ink)" stroke-width="3" stroke-linecap="round"/><circle cx="${ax}" cy="${ay}" r="4" fill="var(--ink)"/>
      <path d="M ${cxp + 28} ${cyp} A 28 28 0 ${Math.abs(ph) > Math.PI ? 1 : 0} ${ph >= 0 ? 0 : 1} ${cxp + 28 * Math.cos(ph)} ${cyp - 28 * Math.sin(ph)}" fill="none" stroke="var(--warn)" stroke-width="1.5" transform="rotate(${-w * 180 / Math.PI} ${cxp} ${cyp})"/>
      <text x="${cxp}" y="${cyp + R + 26}" text-anchor="middle" font-family="var(--font-mono)" font-size="11" fill="var(--ink-2)">phase of across vs through: ${ELEM[cur].phase > 0 ? "+" : ""}${ELEM[cur].phase}°</text>
      <line x1="280" x2="620" y1="${cyp}" y2="${cyp}" stroke="var(--plot-grid)"/>
      <path d="${trT}" fill="none" stroke="var(--ink-3)" stroke-width="2"/><path d="${trA}" fill="none" stroke="var(--ink)" stroke-width="2"/>
      <text x="280" y="${cyp - R - 6}" font-family="var(--font-mono)" font-size="11" fill="var(--ink-2)">time →  (black = across, grey = through)</text>
    </svg>`;
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

/* ===== L2 · Series resonator: force-driven vs velocity-driven ===== */
function benchResonator() {
  const b = bench("bench-resonator", "Mass–spring–damper: the same curve in every domain", "lecture 2 · problem 2.2");
  if (!b) return;
  const st = { M: 20, C: 1, R: 0.5, mode: "f" };
  const seg = h("div", { class: "seg" });
  const modes = [["f", "drive with force f (10 N)"], ["u", "drive with velocity u (1 m/s)"]];
  for (const [k, l] of modes) seg.append(h("button", { type: "button", class: k === st.mode ? "on" : "", onclick: (e) => { st.mode = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  const sM = slider(b.ctl, { label: "mass <b>M<sub>M</sub></b>", min: 2, max: 100, step: 1, value: 20, unit: "g", dom: "me", onchange: v => { st.M = v; upd(); } });
  const sC = slider(b.ctl, { label: "compliance <b>C<sub>M</sub></b> = 1/k", min: 0.1, max: 10, step: 0.1, value: 1, unit: "mm/N", dom: "me", onchange: v => { st.C = v; upd(); } });
  const sR = slider(b.ctl, { label: "damping <b>R<sub>M</sub></b>", min: 0.05, max: 10, step: 0.05, value: 0.5, unit: "Ns/m", dom: "me", onchange: v => { st.R = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "resonance f₀" }, { id: "Q", label: "Q" }, { id: "peak", label: "at f₀" }, { id: "k", label: "stiffness k" }]);
  const pm = new Plot(b.plot, { h: 230, ymin: -60, ymax: 40, ylabel: "response (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const pp = new Plot(b.plot, { h: 150, ymin: -90, ymax: 90, yticks: [-90, -45, 0, 45, 90], ylabel: "phase (°)", yfmt: v => v.toFixed(0) + "°" });
  function upd() {
    const M = st.M / 1000, C = st.C / 1000, R = st.R;
    const f0 = 1 / (TAU * Math.sqrt(M * C)), Q = Math.sqrt(M / C) / R;
    const Zm = (f) => cadd(cadd(ZL(f, M), ZC(f, C)), ZR(R));
    const force = st.mode === "f";
    const pts = FREQ.map(f => { const Z = Zm(f); const r = force ? cscale(cinv(Z), 10) : Z; return [f, r]; });
    pm.set({
      ylabel: force ? "velocity |u| (dB re 1 m/s)" : "force |f| (dB re 1 N)",
      series: [{ name: force ? "|u| for f = 10 N" : "|f| for u = 1 m/s", color: DOMC.me, pts: pts.map(([f, r]) => [f, dB(cabs(r))]) }],
      markers: [{ x: f0, y: dB(force ? 10 / R : R), label: force ? `peak ${sci(10 / R)} m/s` : `dip ${sci(R)} N`, color: DOMC.me }],
      regions: [{ from: 10, to: f0 / 3, color: DOMC.ac, label: "spring rules" }, { from: f0 * 3, to: 20000, color: DOMC.el, label: "mass rules" }],
    });
    pp.set({ series: [{ name: "phase", color: DOMC.me, pts: pts.map(([f, r]) => [f, carg(r)]) }] });
    ro({ f0: hz(f0), Q: Q.toFixed(2), peak: force ? `u = f/R = ${sci(10 / R)} m/s` : `f = R·u = ${sci(R)} N`, k: `${sci(1 / C)} N/m` });
    b.note.innerHTML = force
      ? `<p><b>Force source → impedance analogy, series RLC.</b> At resonance the mass's <span class="mono">jωM</span> and the spring's <span class="mono">1/jωC</span> cancel, so only the damper is left: <span class="mono">u = f / R<sub>M</sub></span> — a <b>peak</b>. Below f₀ the spring wins (velocity rises with frequency, +6 dB/oct, phase +90°); above it the mass wins (−6 dB/oct, phase −90°).</p>`
      : `<p><b>Velocity source → the same physics, upside down.</b> Now you impose the motion and ask what force it costs. At resonance the reactances cancel and the source only has to overcome the damper: <span class="mono">f = R<sub>M</sub>·u</span> — a <b>dip</b>. Same f₀, same Q, mirrored curve. That mirror is duality: resonance = impedance minimum = admittance maximum.</p>`;
  }
  upd();
}

/* ===== L2 · Impedance vs mobility: one system drawn both ways ===== */
function benchDual() {
  const root = document.getElementById("bench-dual"); if (!root) return;
  const imp = svgWrap(320, 200, [
    VSRC(40, 160, 40, 40, DOMC.me, "f", -1),
    CK.wire(40, 40, 90, 40), IND(90, 40, 170, 40, DOMC.me, "M<tspan font-size='9' dy='3'>M</tspan>"), CAP(170, 40, 250, 40, DOMC.me, "C<tspan font-size='9' dy='3'>M</tspan>"), CK.wire(250, 40, 290, 40),
    RES(290, 40, 290, 160, DOMC.me, "R<tspan font-size='9' dy='3'>M</tspan>", 1), CK.wire(290, 160, 40, 160), CK.dot(40, 160), CK.gnd(165, 160),
    CK.label(165, 100, "u  (mesh current)", DOMC.ink2, "middle", 11), CK.note(160, 190, "impedance analogy: f ↔ voltage, u ↔ current — one series loop"),
  ].join(""));
  const mob = svgWrap(320, 200, [
    ISRC(40, 160, 40, 40, DOMC.me, "f", -1), CK.wire(40, 40, 260, 40), CK.dot(110, 40), CK.dot(180, 40), CK.dot(260, 40),
    CAP(110, 40, 110, 160, DOMC.me, "M<tspan font-size='9' dy='3'>M</tspan>", 1), IND(180, 40, 180, 160, DOMC.me, "C<tspan font-size='9' dy='3'>M</tspan>", 1), RES(260, 40, 260, 160, DOMC.me, "1/R<tspan font-size='9' dy='3'>M</tspan>", 1),
    CK.wire(40, 160, 260, 160), CK.gnd(150, 160), CK.label(150, 28, "node u  (velocity = node voltage)", DOMC.ink2, "middle", 11),
    CK.note(160, 190, "mobility analogy: u ↔ voltage, f ↔ current — one node, elements in parallel"),
  ].join(""));
  root.innerHTML = `<div class="two"><div class="circuit">${imp}<div class="cap">Z_M = f/u = jωM + 1/(jωC) + R</div></div><div class="circuit">${mob}<div class="cap">Y_M = u/f = 1/(jωM) ∥ jωC ∥ 1/R</div></div></div>`;
}

/* ===== L3 · Helmholtz bottle with sound ===== */
function benchHelmholtz() {
  const b = bench("bench-helmholtz", "The bottle: a tube is a mass, a box is a spring", "lecture 3 · problems 2.1–2.3");
  if (!b) return;
  const st = { l: 5, a: 1, V: 1.88, flange: true };
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  slider(b.ctl, { label: "neck length <b>l</b>", min: 1, max: 30, step: 0.5, value: 5, unit: "cm", dom: "ac", onchange: v => { st.l = v; upd(); } });
  slider(b.ctl, { label: "neck radius <b>a</b>", min: 0.3, max: 5, step: 0.1, value: 1, unit: "cm", dom: "ac", onchange: v => { st.a = v; upd(); } });
  slider(b.ctl, { label: "cavity volume <b>V</b>", min: 0.1, max: 30, step: 0.1, value: 1.88, unit: "L", dom: "ac", onchange: v => { st.V = v; upd(); } });
  const seg = h("div", { class: "seg" });
  for (const [k, l] of [[true, "with end correction"], [false, "bare length"]]) seg.append(h("button", { type: "button", class: k === st.flange ? "on" : "", onclick: (e) => { st.flange = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  const ro = readouts(b.ctl, [{ id: "f0", label: "f₀", dom: "ac" }, { id: "lam", label: "λ/10 at f₀" }, { id: "MA", label: "M_A = ρl*/S", dom: "ac" }, { id: "CA", label: "C_A = V/ρc²", dom: "ac" }]);
  const btn = h("button", { class: "btn", type: "button" }, "▶ hear f₀");
  b.ctl.append(btn);
  let f0 = 100;
  btn.addEventListener("click", () => beep(f0));
  function upd() {
    const a = st.a / 100, l = st.l / 100, V = st.V / 1000, S = Math.PI * a * a;
    const lstar = l + (st.flange ? 0.8488 * a + 0.6133 * a : 0); // flanged inner end + unflanged outer end
    const MA = RHO * lstar / S, CA = V / (RHO * C0 * C0);
    f0 = 1 / (TAU * Math.sqrt(MA * CA));
    const lam = C0 / f0, ok = lstar < lam / 10 && Math.cbrt(V) < lam / 10;
    ro({ f0: hz(f0), lam: `${(lam / 10 * 100).toFixed(0)} cm ${ok ? "✓ lumped OK" : "✗ too big"}`, MA: `${sci(MA)} kg/m⁴`, CA: `${sci(CA)} m⁵/N` });
    const neckW = Math.max(14, Math.min(90, a * 100 * 14)), neckH = Math.max(16, Math.min(150, l * 100 * 5)), boxS = Math.max(50, Math.min(190, 60 * Math.cbrt(V * 1000) / 1.2));
    const cxp = 200, top = 210 - neckH - boxS;
    stage.innerHTML = `<svg viewBox="0 0 640 260">
      <rect x="${cxp - boxS / 2}" y="${210 - boxS}" width="${boxS}" height="${boxS}" rx="8" fill="var(--ac-soft)" stroke="var(--ac)" stroke-width="2"/>
      <rect x="${cxp - neckW / 2}" y="${Math.max(10, 210 - boxS - neckH)}" width="${neckW}" height="${neckH}" fill="var(--el-soft)" stroke="var(--el)" stroke-width="2"/>
      <g class="plug"><rect x="${cxp - neckW / 2 + 3}" y="${Math.max(10, 210 - boxS - neckH) + neckH * 0.35}" width="${neckW - 6}" height="${neckH * 0.3}" fill="var(--el)" opacity="0.7"><animate attributeName="y" values="${Math.max(10, 210 - boxS - neckH) + neckH * 0.25};${Math.max(10, 210 - boxS - neckH) + neckH * 0.45};${Math.max(10, 210 - boxS - neckH) + neckH * 0.25}" dur="${Math.max(0.35, 60 / f0).toFixed(2)}s" repeatCount="indefinite"/></rect></g>
      <text x="${cxp + boxS / 2 + 10}" y="${210 - boxS / 2}" font-family="var(--font-mono)" font-size="12" fill="var(--ac)">V = ${st.V} L → C_A (spring)</text>
      <text x="${cxp + neckW / 2 + 10}" y="${Math.max(10, 210 - boxS - neckH) + neckH / 2 + 4}" font-family="var(--font-mono)" font-size="12" fill="var(--el)">air plug in neck → M_A (mass)</text>
      <text x="${cxp}" y="240" text-anchor="middle" font-family="var(--font-mono)" font-size="12" fill="var(--ink-2)">l* = ${(lstar * 100).toFixed(2)} cm · S = ${sci(S)} m²</text>
      <g transform="translate(420 40)">
        ${ISRC(20, 140, 20, 30, DOMC.ac, "U", -1)}${CK.wire(20, 30, 60, 30)}${IND(60, 30, 140, 30, DOMC.ac, "M_A neck")}${CK.wire(140, 30, 170, 30)}${CAP(170, 30, 170, 140, DOMC.ac, "C_A box", 1)}${CK.wire(170, 140, 20, 140)}${CK.gnd(95, 140)}${CK.dot(170, 30)}
        ${CK.note(100, 175, "series L–C: f₀ = 1 / (2π √(M_A C_A))")}
      </g>
    </svg>`;
    b.note.innerHTML = `<p><span class="mono">f₀ = (c/2π)·√(S / (l*·V))</span> — the ρ cancels, only geometry and the speed of sound remain. The animation bobs at a rate proportional to f₀ (not the real rate). The end correction adds <span class="mono">0.85a</span> for the flanged inner end and <span class="mono">0.61a</span> for the free outer end: a short fat neck is mostly end correction.</p><p>The lumped model is only trustworthy while everything is smaller than λ/10. Make the bottle huge or the neck long and the readout flags it.</p>`;
  }
  upd();
}

/* ===== L3 · Where the lumped tube model breaks ===== */
function benchTube() {
  const b = bench("bench-tube", "Exact tube vs. lumped element: watch the approximation fail", "lecture 3 · §3");
  if (!b) return;
  const st = { l: 20, closed: false };
  const seg = h("div", { class: "seg" });
  for (const [k, l] of [[false, "open end → mass"], [true, "closed end → spring"]]) seg.append(h("button", { type: "button", class: k === st.closed ? "on" : "", onclick: (e) => { st.closed = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  slider(b.ctl, { label: "tube length <b>l</b>", min: 2, max: 100, step: 1, value: 20, unit: "cm", dom: "ac", onchange: v => { st.l = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "flim", label: "l = λ/10 at" }, { id: "fq", label: "l = λ/4 at" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 20, xmax: 5000, ymin: -30, ymax: 40, ylabel: "|Z| / (ρc/S)  (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const l = st.l / 100, flim = C0 / (10 * l), fq = C0 / (4 * l);
    const exact = [], lump = [];
    for (const f of logspace(20, 5000, 500)) {
      const kl = TAU * f / C0 * l;
      exact.push([f, dB(Math.abs(st.closed ? -1 / Math.tan(kl) : Math.tan(kl)))]);
      lump.push([f, dB(st.closed ? 1 / kl : kl)]);
    }
    plot.set({
      series: [{ name: "exact (plane wave)", color: DOMC.ac, pts: exact }, { name: st.closed ? "lumped C_A = V/ρc²" : "lumped M_A = ρl/S", color: DOMC.ink2, thin: true, pts: lump }],
      vlines: [{ x: flim, label: "λ/10", color: DOMC.ok }, { x: fq, label: "λ/4", color: DOMC.warn }],
    });
    ro({ flim: hz(flim), fq: hz(fq) });
    b.note.innerHTML = st.closed
      ? `<p>A closed tube: <span class="mono">Z = −j(ρc/S)·cot(kl)</span>. At low frequency <span class="mono">cot(kl) ≈ 1/kl</span>, which is exactly a capacitor <span class="mono">1/(jωC_A)</span> with <span class="mono">C_A = V/ρc²</span>. Past λ/10 the curves part; at λ/4 the real tube resonates (|Z| → 0) while the lumped spring knows nothing about it.</p>`
      : `<p>An open tube: <span class="mono">Z = j(ρc/S)·tan(kl)</span>. At low frequency <span class="mono">tan(kl) ≈ kl</span>, which is exactly an inductor <span class="mono">jωM_A</span> with <span class="mono">M_A = ρl/S</span>. Past λ/10 the curves part; at λ/4 the real tube has an impedance <i>peak</i> (a standing wave) the lumped mass cannot show.</p>`;
  }
  upd();
}

/* ===== L3 · Radiation impedance of a baffled piston ===== */
function benchRadiation() {
  const b = bench("bench-radiation", "What the air in front of a piston looks like", "lecture 3 · §8b");
  if (!b) return;
  const st = { a: 10 };
  slider(b.ctl, { label: "piston radius <b>a</b>", min: 0.5, max: 20, step: 0.5, value: 10, unit: "cm", dom: "ac", onchange: v => { st.a = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f1", label: "ka = 1 at", dom: "ac" }, { id: "MA1", label: "M_A1 (low ka)", dom: "ac" }, { id: "RA2", label: "R_A2 = ρc/S (high ka)", dom: "ac" }, { id: "mass", label: "air load mass S²M_A1" }]);
  const plot = new Plot(b.plot, { h: 300, xlog: true, xmin: 0.05, xmax: 5, ymin: 0, ymax: 1.2, ylabel: "Z / (ρc/S)", xlabel: "ka  (= 2πfa/c)", xfmt: v => Number(v.toPrecision(2)), yfmt: v => v.toFixed(2), xticks: [0.05, 0.1, 0.2, 0.5, 1, 2, 5].map(v => ({ v, l: String(v) })) });
  function upd() {
    const a = st.a / 100, S = Math.PI * a * a, norm = RHO * C0 / S;
    const kas = logspace(0.05, 5, 300);
    const exR = [], exX = [], luR = [], luX = [];
    for (const ka of kas) {
      const z = pistonZnorm(ka); exR.push([ka, z.re]); exX.push([ka, z.im]);
      const f = ka * C0 / (TAU * a), zl = cscale(pistonZlumped(f, a), 1 / norm); luR.push([ka, zl.re]); luX.push([ka, zl.im]);
    }
    plot.set({ series: [
      { name: "exact real part (radiates power)", color: DOMC.ac, pts: exR }, { name: "exact imaginary part (mass-like)", color: DOMC.el, pts: exX },
      { name: "lumped fit, real", color: DOMC.ac, thin: true, pts: luR }, { name: "lumped fit, imag", color: DOMC.el, thin: true, pts: luX }],
      vlines: [{ x: 1, label: "ka = 1", color: DOMC.ink3 }] });
    const MA1 = 8 * RHO / (3 * Math.PI * Math.PI * a);
    ro({ f1: hz(C0 / (TAU * a)), MA1: `${sci(MA1)} kg/m⁴`, RA2: `${sci(norm)} Pa·s/m³`, mass: `${sci(S * S * MA1 * 1000)} g` });
  }
  upd();
  b.note.innerHTML = `<p>Below <span class="mono">ka ≈ 1</span> the imaginary part dominates and grows like ω: the piston just drags a lump of air along — a <b>mass</b> <span class="mono">M_A1 = 8ρ/(3π²a)</span>. Above it the real part flattens to <span class="mono">ρc/S</span>: the piston <b>radiates</b> efficiently. The dashed lines are Beranek's four-element fit (<span class="mono">M_A1 ∥ [R_A2 + (R_A1 ∥ C_A1)]</span>) — good enough to put in LTspice.</p><p>The same curve is the front load of every loudspeaker cone and every microphone diaphragm in this course.</p>`;
}

/* ===== L4 · Which controlled source? ===== */
function benchCoupling() {
  const root = document.getElementById("bench-coupling"); if (!root) return;
  root.classList.add("bench");
  const st = { from: "across", to: "across" };
  const table = { "across→across": ["E", "voltage-controlled voltage source", "VCVS", "e.g. v = Bl·u in the mobility analogy: the back-EMF voltage is set by the velocity (a node voltage)"], "through→through": ["F", "current-controlled current source", "CCCS", "e.g. f = Bl·i in the mobility analogy: the force (a current) is set by the coil current"], "across→through": ["G", "voltage-controlled current source", "VCCS", "e.g. U = S·u in the mobility analogy: the volume velocity (a current) is set by the diaphragm velocity (a node voltage)"], "through→across": ["H", "current-controlled voltage source", "CCVS", "e.g. f = Bl·i in the impedance analogy: the force (a voltage) is set by the coil current"] };
  const head = h("div", { class: "bench-head" }, h("h4", {}, "Pick the source from the pair of variables it connects"), h("span", { class: "eyebrow" }, "lecture 4 · §2a"));
  const body = h("div", { class: "bench-body one" });
  const stage = h("div", { class: "bench-plot" });
  const ctl = h("div", { class: "bench-ctl", style: "border-left:0;border-top:1px solid var(--rule)" });
  const mk = (key, label) => { const c = h("div", { class: "chips" }, h("span", { class: "small", style: "align-self:center" }, label)); for (const v of ["across", "through"]) c.append(h("button", { type: "button", class: "chip" + (st[key] === v ? " on" : ""), onclick: (e) => { st[key] = v; $$(".chip", c).forEach(x => x.classList.toggle("on", x === e.target)); draw(); } }, v + (v === "across" ? " (v · u · p)" : " (i · f · U)"))); return c; };
  ctl.append(mk("from", "control variable (input):"), mk("to", "output variable:"));
  const out = h("div", {});
  ctl.append(out);
  body.append(stage, ctl); root.append(head, body);
  function draw() {
    const k = `${st.from}→${st.to}`, [letter, name, abbr, ex] = table[k];
    const inVolt = st.from === "across", outVolt = st.to === "across";
    stage.innerHTML = svgWrap(640, 170, [
      // input side
      inVolt ? `${CK.wire(60, 40, 60, 130, DOMC.ink)}${CK.label(40, 90, "+", DOMC.ink2)}${CK.label(40, 125, "−", DOMC.ink2)}${CK.label(60, 28, "control voltage", DOMC.ink2, "middle", 11)}${CK.dot(60, 40)}${CK.dot(60, 130)}`
        : `${CK.wire(20, 85, 120, 85, DOMC.ink)}${`<path d="M95 79 l8 6 -8 6" fill="none" stroke="${DOMC.ink}" stroke-width="1.6"/>`}${CK.label(70, 70, "control current", DOMC.ink2, "middle", 11)}`,
      `<path d="M150 85 h120" stroke="${DOMC.ink3}" stroke-width="1.5" stroke-dasharray="4 4"/><path d="M262 79 l8 6 -8 6" fill="none" stroke="${DOMC.ink3}" stroke-width="1.5"/>`,
      CK.label(210, 72, "× factor (S, Bl, E/x₀ …)", DOMC.ink2, "middle", 11),
      // the source itself
      outVolt ? DEPV(320, 140, 320, 30, DOMC.ink, "") : DEPI(320, 140, 320, 30, DOMC.ink, ""),
      CK.label(360, 60, letter, DOMC.ink, "start", 40),
      CK.label(360, 90, abbr, DOMC.ink2, "start", 12),
      CK.label(360, 110, name, DOMC.ink2, "start", 12),
      CK.label(320, 160, outVolt ? "output: a voltage (across)" : "output: a current (through)", DOMC.ink2, "middle", 11),
    ].join(""));
    out.innerHTML = `<p style="max-width:none" class="small"><b>SPICE letter ${letter}.</b> ${ex}. In KiCad only E and G exist as symbols; sense a current as the voltage across a small resistor and use E or G instead.</p>`;
  }
  draw();
}

/* ===== L4 · Loudspeaker / coil impedance: the motional peak ===== */
function benchSpeakerZ() {
  const b = bench("bench-speakerz", "The impedance peak: mechanics seen from the terminals", "lecture 4 · problem 4.4b");
  if (!b) return;
  const st = { Bl: 2.1, Re: 5, Le: 0.3, M: 10, C: 1, R: 2 };
  slider(b.ctl, { label: "force factor <b>Bl</b>", min: 0.2, max: 12, step: 0.1, value: 2.1, unit: "T·m", dom: "el", onchange: v => { st.Bl = v; upd(); } });
  slider(b.ctl, { label: "coil resistance <b>R<sub>e</sub></b>", min: 1, max: 16, step: 0.5, value: 5, unit: "Ω", dom: "el", onchange: v => { st.Re = v; upd(); } });
  slider(b.ctl, { label: "coil inductance <b>L<sub>e</sub></b>", min: 0, max: 3, step: 0.05, value: 0.3, unit: "mH", dom: "el", onchange: v => { st.Le = v; upd(); } });
  slider(b.ctl, { label: "moving mass <b>M<sub>mc</sub></b>", min: 1, max: 60, step: 0.5, value: 10, unit: "g", dom: "me", onchange: v => { st.M = v; upd(); } });
  slider(b.ctl, { label: "suspension <b>C<sub>ms</sub></b>", min: 0.1, max: 5, step: 0.05, value: 1, unit: "mm/N", dom: "me", onchange: v => { st.C = v; upd(); } });
  slider(b.ctl, { label: "mech. damping <b>R<sub>ms</sub></b>", min: 0.2, max: 10, step: 0.1, value: 2, unit: "Ns/m", dom: "me", onchange: v => { st.R = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "f₀ (mech. resonance)", dom: "me" }, { id: "pk", label: "|Z_E| peak = R_e + (Bl)²/R_ms", dom: "el" }, { id: "Rmot", label: "R_mot = (Bl)²/R_ms", dom: "el" }, { id: "Lmot", label: "L_mot = (Bl)²·C_ms", dom: "el" }, { id: "Cmot", label: "C_mot = M/(Bl)²", dom: "el" }, { id: "Qm", label: "Q_m" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 10, xmax: 10000, ymin: 0, ymax: 30, ylabel: "|Z_E|  (Ω)", yfmt: v => v.toFixed(1), yunit: " Ω" });
  function upd() {
    const Bl = st.Bl, Re = st.Re, Le = st.Le / 1000, M = st.M / 1000, C = st.C / 1000, R = st.R;
    const f0 = 1 / (TAU * Math.sqrt(M * C)), pk = Re + Bl * Bl / R;
    const ze = (f) => cadd(cadd(ZR(Re), ZL(f, Le)), cscale(cinv(cadd(cadd(ZL(f, M), ZC(f, C)), ZR(R))), Bl * Bl));
    const blocked = (f) => cadd(ZR(Re), ZL(f, Le));
    const pts = FREQ.filter(f => f <= 10000).map(f => [f, cabs(ze(f))]);
    const ymax = Math.max(12, Math.ceil(Math.max(...pts.map(p => p[1])) * 1.15 / 5) * 5);
    plot.set({ ymax, series: [{ name: "|Z_E| free (with motion)", color: DOMC.el, pts }, { name: "blocked coil R_e + jωL_e", color: DOMC.ink2, thin: true, pts: FREQ.filter(f => f <= 10000).map(f => [f, cabs(blocked(f))]) }], markers: [{ x: f0, y: pk, label: `${pk.toFixed(2)} Ω at ${hz(f0)}`, color: DOMC.el }] });
    ro({ f0: hz(f0), pk: `${pk.toFixed(2)} Ω`, Rmot: `${sci(Bl * Bl / R)} Ω`, Lmot: `${sci(Bl * Bl * C * 1000)} mH`, Cmot: `${sci(M / (Bl * Bl) * 1000)} mF`, Qm: (Math.sqrt(M / C) / R).toFixed(2) });
  }
  upd();
  b.note.innerHTML = `<p>The voice coil is a <b>gyrator</b>: <span class="mono">Z_E = R_e + jωL_e + (Bl)² / Z_M</span>. Dividing by Z_M turns the mechanical <i>series</i> resonance (impedance minimum, velocity maximum) into an electrical <i>parallel</i> resonance — the famous <b>peak</b>. At f₀ the cone moves most, so the back-EMF <span class="mono">Bl·u</span> is largest and the current smallest.</p><p>Every element crosses over as its dual: mass → capacitor, compliance → inductor, damper → resistor, all scaled by (Bl)². Turn Bl down to 0.2 and the peak vanishes: with a weak motor the terminals cannot see the mechanics.</p>`;
}

/* ===== L4 · Dynamic microphone designer ===== */
function dynMic(p) {
  // returns totals and transfer function for the Leach/VCH dynamic pressure mic
  const a = p.a, SD = Math.PI * a * a;
  const MA1 = p.front === "baffle" ? 8 * RHO / (3 * Math.PI * Math.PI * a) : 0.6133 * RHO / (Math.PI * a); // official sheets: piston in a tube
  const CAB = p.V / (RHO * C0 * C0);
  const MMT = p.MMD + SD * SD * MA1;
  const RMT = p.RMS + SD * SD * p.RAF + p.Bl * p.Bl / (p.RE + p.RL);
  const CMT = 1 / (1 / p.CMS + SD * SD / CAB);
  const f0 = 1 / (TAU * Math.sqrt(MMT * CMT)), Q = Math.sqrt(MMT / CMT) / RMT;
  const div = p.RL / (p.RE + p.RL);
  const M = div * p.Bl * SD / RMT;
  const fa = f0 * (Math.sqrt(1 + 1 / (4 * Q * Q)) - 1 / (2 * Q)), fb = f0 * (Math.sqrt(1 + 1 / (4 * Q * Q)) + 1 / (2 * Q));
  const H = (f) => cscale(cinv(cadd(cadd(ZL(f, MMT), ZC(f, CMT)), ZR(RMT))), div * p.Bl * SD);
  return { SD, MA1, CAB, MMT, RMT, CMT, f0, Q, M, fa, fb, H };
}
function benchDynMic() {
  const b = bench("bench-dynmic", "Design a dynamic microphone: felt, back volume, magnet", "lecture 4B · problems 4.1–4.2");
  if (!b) return;
  const st = { RAF: 3.56e7, V: 10.8, Bl: 20, RL: 47000, front: "tube" };
  const segF = h("div", { class: "seg" });
  for (const [k, l] of [["tube", "front air mass: piston in a tube (sheet)"], ["baffle", "baffled piston"]]) segF.append(h("button", { type: "button", class: k === st.front ? "on" : "", onclick: (e) => { st.front = k; $$("button", segF).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(segF);
  slider(b.ctl, { label: "felt resistance <b>R<sub>AF</sub></b>", min: 1e6, max: 1e9, log: true, value: 3.56e7, unit: "Ns/m⁵", dom: "ac", onchange: v => { st.RAF = v; upd(); } });
  slider(b.ctl, { label: "back volume <b>V<sub>AB</sub></b>", min: 0.5, max: 60, step: 0.1, value: 10.8, unit: "cm³", dom: "ac", onchange: v => { st.V = v; upd(); } });
  slider(b.ctl, { label: "force factor <b>Bl</b>", min: 1, max: 40, step: 0.5, value: 20, unit: "T·m", dom: "el", onchange: v => { st.Bl = v; upd(); } });
  slider(b.ctl, { label: "load <b>R<sub>L</sub></b>", min: 100, max: 1e6, log: true, value: 47000, unit: "Ω", dom: "el", fmt: v => sci(v, 2), onchange: v => { st.RL = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "f₀", dom: "me" }, { id: "Q", label: "Q" }, { id: "M", label: "sensitivity M", dom: "el" }, { id: "MdB", label: "M in dB re 1 V/Pa", dom: "el" }, { id: "band", label: "−3 dB band" }, { id: "MMT", label: "M_MT", dom: "me" }, { id: "RMT", label: "R_MT", dom: "me" }, { id: "CMT", label: "C_MT", dom: "me" }]);
  const plot = new Plot(b.plot, { h: 300, ymin: -100, ymax: -40, ylabel: "|e/p|  (dB re 1 V/Pa)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const r = dynMic({ a: 0.0127, MMD: 0.2e-3, RMS: 1, CMS: 0.21e-3, RE: 200, RL: st.RL, Bl: st.Bl, V: st.V * 1e-6, RAF: st.RAF, front: st.front });
    const pts = FREQ.map(f => [f, dB(cabs(r.H(f)))]);
    plot.set({ series: [{ name: "sensitivity", color: DOMC.el, pts }],
      markers: [{ x: r.f0, y: dB(cabs(r.H(r.f0))), label: `f₀ ${hz(r.f0)}`, color: DOMC.me }, { x: r.fa, y: dB(cabs(r.H(r.fa))), label: hz(r.fa), color: DOMC.ink2, dx: -6, anchor: "end" }, { x: r.fb, y: dB(cabs(r.H(r.fb))), label: hz(r.fb), color: DOMC.ink2 }],
      regions: [{ from: 10, to: r.fa, color: DOMC.ac, label: "spring, +6 dB/oct" }, { from: r.fa, to: r.fb, color: DOMC.me, label: "damping — flat" }, { from: r.fb, to: 20000, color: DOMC.el, label: "mass, −6 dB/oct" }] });
    ro({ f0: hz(r.f0), Q: r.Q.toFixed(3), M: `${sci(r.M * 1000)} mV/Pa`, MdB: `${dB(r.M).toFixed(1)} dB`, band: `${hz(r.fa)} – ${hz(r.fb)}`, MMT: `${sci(r.MMT * 1000)} g`, RMT: `${sci(r.RMT)} Ns/m`, CMT: `${sci(r.CMT * 1000)} mm/N` });
  }
  upd();
  b.note.innerHTML = `<p>Starting values are the Problems 4 design: 1-inch diaphragm, <span class="mono">M_MD = 0.2 g</span>, <span class="mono">C_MS = 0.21 mm/N</span>, <span class="mono">R_MS = 1 Ns/m</span>, <span class="mono">R_E = 200 Ω</span>. The whole three-domain circuit collapses to one series loop: <span class="mono">e/p = −Bl·S_D / (jωM_MT + R_MT + 1/jωC_MT)</span>. The front air mass follows the official solution (piston in a tube, <span class="mono">M_A1 = 0.6133ρ/πa = 18.1</span>); the baffled value (25.1) gives 10.6 cm³ instead of 10.8 for the same f₀.</p><p><b>Try:</b> lower the felt resistance — sensitivity goes up, bandwidth shrinks, a hump appears. Shrink the back volume — the air spring stiffens and f₀ climbs. A dynamic mic lives in its <b>damping-controlled</b> middle, so the felt is the designer's main knob.</p>`;
}

/* ===== L5 · Polar patterns ===== */
function benchPolar() {
  const b = bench("bench-polar", "One dial from omni to figure-8", "lecture 5 · §2e");
  if (!b) return;
  const st = { B: 1 };
  const stage = h("div", { style: "display:grid;grid-template-columns:1fr 1fr;gap:8px;align-items:center" }); b.plot.append(stage);
  const presets = [["omni", 0], ["subcardioid", 0.5], ["cardioid", 1], ["supercardioid", Math.sqrt(3)], ["hypercardioid", 3], ["figure-8", Infinity]];
  const chips = h("div", { class: "chips" });
  for (const [n, v] of presets) chips.append(h("button", { type: "button", class: "chip" + (v === st.B ? " on" : ""), onclick: (e) => { st.B = v; $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); sl.set(isFinite(v) ? v : 12); upd(); } }, n));
  b.ctl.append(chips);
  const sl = slider(b.ctl, { label: "gradient share <b>B</b> = Δl / Δl′", min: 0, max: 12, step: 0.05, value: 1, dom: "ac", fmt: v => v >= 12 ? "∞" : v.toFixed(2), onchange: v => { st.B = v >= 12 ? Infinity : v; $$(".chip", chips).forEach(x => x.classList.remove("on")); upd(); } });
  const ro = readouts(b.ctl, [{ id: "rear", label: "response at 180°" }, { id: "null", label: "null angle" }, { id: "side", label: "at 90°" }]);
  function R(t) { return isFinite(st.B) ? Math.abs(1 + st.B * Math.cos(t)) / (1 + st.B) : Math.abs(Math.cos(t)); }
  function upd() {
    const B = st.B;
    const pressure = isFinite(B) ? 1 / (1 + B) : 0, grad = isFinite(B) ? B / (1 + B) : 1;
    stage.innerHTML = `<div>${polarSVG(R, { w: 300 })}<div class="small" style="text-align:center">R(θ) = |1 + B cos θ| / (1 + B)</div></div>
      <div>${polarSVG([{ fn: () => pressure, color: DOMC.ac, fill: 0.08, dash: "5 4" }, { fn: (t) => grad * Math.abs(Math.cos(t)), color: DOMC.el, fill: 0.08, dash: "5 4" }], { w: 300 })}<div class="small" style="text-align:center"><span class="ac">pressure part</span> + <span class="el">gradient part</span> (the two ingredients)</div></div>`;
    const rear = R(Math.PI), nul = isFinite(B) && B >= 1 ? Math.acos(-1 / B) * 180 / Math.PI : (isFinite(B) ? NaN : 90);
    ro({ rear: `${(20 * Math.log10(Math.max(rear, 1e-4))).toFixed(1)} dB`, null: isNaN(nul) ? "none (B < 1)" : `${nul.toFixed(0)}°`, side: `${(20 * Math.log10(Math.max(R(Math.PI / 2), 1e-4))).toFixed(1)} dB` });
  }
  upd();
  b.note.innerHTML = `<p>A closed back gives pure pressure (the circle, no direction). An open back with an external path Δl gives pure gradient (cos θ, the figure-8). A <b>combination microphone</b> adds an internal delayed path Δl′ and mixes the two in the ratio <span class="mono">B = Δl/Δl′</span>. Every pattern on a spec sheet is this one dial.</p><p>Cardioid (B = 1) is where the rear null first appears. Beyond it the null moves forward to the sides and a rear lobe grows back — that is the whole super/hyper story.</p>`;
}

/* ===== L5 · Proximity effect ===== */
function benchProximity() {
  const b = bench("bench-proximity", "Why singers lean in: the proximity effect", "lecture 5 · §2d");
  if (!b) return;
  const st = { r: 0.37 };
  slider(b.ctl, { label: "distance to source <b>r</b>", min: 0.02, max: 3, log: true, value: 0.37, unit: "m", dom: "ac", fmt: v => v.toFixed(2), onchange: v => { st.r = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "fk", label: "kr = 1 at", dom: "ac" }, { id: "b100", label: "boost at 100 Hz" }]);
  const plot = new Plot(b.plot, { h: 280, xmin: 20, xmax: 20000, ymin: -5, ymax: 40, ylabel: "gradient boost |1 + 1/(jkr)|  (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fac = (f, r) => Math.hypot(1, 1 / (TAU * f / C0 * r));
  function upd() {
    plot.set({ series: [
      { name: `r = ${st.r.toFixed(2)} m`, color: DOMC.ac, pts: FREQ.map(f => [f, dB(fac(f, st.r))]) },
      { name: "r = 5 cm", color: DOMC.el, thin: true, pts: FREQ.map(f => [f, dB(fac(f, 0.05))]) },
      { name: "r = 1.5 m", color: DOMC.me, thin: true, pts: FREQ.map(f => [f, dB(fac(f, 1.5))]) },
      { name: "plane wave (r → ∞)", color: DOMC.ink3, thin: true, pts: FREQ.map(f => [f, 0]) }],
      vlines: [{ x: C0 / (TAU * st.r), label: "kr = 1", color: DOMC.ac }] });
    ro({ fk: hz(C0 / (TAU * st.r)), b100: `${dB(fac(100, st.r)).toFixed(1)} dB` });
  }
  upd();
  b.note.innerHTML = `<p>Close to a point source the wave is spherical, and its gradient picks up an extra term: <span class="mono">dp/dr ∝ jk·p·(1 + 1/(jkr))</span>. Far away (kr ≫ 1) that bracket is 1 and you get the plane-wave gradient. Close in and at low frequency (kr ≪ 1) it explodes — free bass for a gradient microphone. This is exactly what rescues the ribbon mic's 12 dB/oct low-frequency roll-off, provided you are near the source.</p>`;
}

/* ===== L5 · Condenser microphone ===== */
function condMic(p) {
  const SD = Math.PI * p.a * p.a;
  const MA1 = p.front === "baffle" ? 8 * RHO / (3 * Math.PI * Math.PI * p.a) : 0.6133 * RHO / (Math.PI * p.a); // official sheets: piston in a tube
  const CAB2 = p.V / (RHO * C0 * C0);
  const MMT = p.MMD + SD * SD * (MA1 + p.MAS);
  const RMT = p.RMD + SD * SD * p.RAS;
  const CMT = 1 / (1 / p.CMD + SD * SD / CAB2);
  const f0 = 1 / (TAU * Math.sqrt(MMT * CMT)), Q = Math.sqrt(MMT / CMT) / RMT;
  const M = p.E * SD * CMT / p.x0;
  const CE0 = EPS0 * SD / p.x0;
  const fl = 1 / (TAU * p.RL * CE0);
  const H = (f) => {
    const x = f / f0;
    const core = cdiv(cx(M, 0), cx(1 - x * x, x / Q));
    const hp = cdiv(cx(0, f / fl), cx(1, f / fl)); // C_E0 into R_L' — the low-frequency droop
    return cmul(core, hp);
  };
  return { SD, MA1, CAB2, MMT, RMT, CMT, f0, Q, M, CE0, fl, H };
}
function benchCondenser() {
  const b = bench("bench-condenser", "Design a condenser microphone: bias, gap, back volume", "lecture 5 · problem 5.1");
  if (!b) return;
  const st = { E: 200, x0: 20, V: 1, RAS: 1e7, RL: 5e8, front: "tube" };
  const segF = h("div", { class: "seg" });
  for (const [k, l] of [["tube", "front air mass: piston in a tube (sheet)"], ["baffle", "baffled piston"]]) segF.append(h("button", { type: "button", class: k === st.front ? "on" : "", onclick: (e) => { st.front = k; $$("button", segF).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(segF);
  slider(b.ctl, { label: "polarization <b>E</b>", min: 20, max: 300, step: 5, value: 200, unit: "V", dom: "el", onchange: v => { st.E = v; upd(); } });
  slider(b.ctl, { label: "gap <b>x₀</b>", min: 5, max: 60, step: 1, value: 20, unit: "µm", dom: "me", onchange: v => { st.x0 = v; upd(); } });
  slider(b.ctl, { label: "back volume <b>V<sub>AB2</sub></b>", min: 0.1, max: 6, step: 0.05, value: 1, unit: "cm³", dom: "ac", onchange: v => { st.V = v; upd(); } });
  slider(b.ctl, { label: "backplate damping <b>R<sub>AS</sub></b>", min: 1e6, max: 3e8, log: true, value: 1e7, unit: "Ns/m⁵", dom: "ac", onchange: v => { st.RAS = v; upd(); } });
  slider(b.ctl, { label: "load <b>R<sub>L</sub>′</b>", min: 1e6, max: 1e10, log: true, value: 5e8, unit: "Ω", dom: "el", fmt: v => sci(v, 2), onchange: v => { st.RL = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "f₀", dom: "me" }, { id: "Q", label: "Q" }, { id: "M", label: "sensitivity", dom: "el" }, { id: "MdB", label: "dB re 1 V/Pa", dom: "el" }, { id: "CE0", label: "capsule C_E0", dom: "el" }, { id: "fl", label: "LF droop corner", dom: "el" }]);
  const plot = new Plot(b.plot, { h: 300, ymin: -70, ymax: -20, ylabel: "|e_oc/p|  (dB re 1 V/Pa)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const r = condMic({ a: 0.009, MMD: 5e-5, CMD: 4e-6, RMD: 1, MAS: 100, RAS: st.RAS, V: st.V * 1e-6, E: st.E, x0: st.x0 * 1e-6, RL: st.RL, front: st.front });
    const pts = FREQ.map(f => [f, dB(cabs(r.H(f)))]);
    const fpk = r.Q > 0.7071 ? r.f0 * Math.sqrt(1 - 1 / (2 * r.Q * r.Q)) : null;
    plot.set({ series: [{ name: "open-circuit sensitivity", color: DOMC.el, pts }],
      markers: [{ x: r.f0, y: dB(cabs(r.H(r.f0))), label: `f₀ ${hz(r.f0)}`, color: DOMC.me }].concat(fpk ? [{ x: fpk, y: dB(cabs(r.H(fpk))), label: `peak +${(dB(cabs(r.H(fpk))) - dB(r.M)).toFixed(1)} dB`, color: DOMC.el, dy: 14, anchor: "end", dx: -6 }] : []),
      regions: [{ from: 10, to: r.f0 / 2, color: DOMC.ac, label: "compliance — flat" }, { from: r.f0 * 2, to: 20000, color: DOMC.el, label: "mass, −12 dB/oct" }] });
    ro({ f0: hz(r.f0), Q: r.Q.toFixed(2), M: `${sci(r.M * 1000)} mV/Pa`, MdB: `${dB(r.M).toFixed(1)} dB`, CE0: `${sci(r.CE0 * 1e12)} pF`, fl: hz(r.fl) });
  }
  upd();
  b.note.innerHTML = `<p>Starting values are Problem 5.1: 9 mm diaphragm, <span class="mono">M_MD = 0.05 g</span>, <span class="mono">C_MD = 4 µm/N</span>, <span class="mono">R_MD = 1 Ns/m</span>, <span class="mono">M_AS = 100 kg/m⁴</span>. Sensitivity is <span class="mono">M = E·S_D·C_MT / x₀</span>: more volts, a bigger diaphragm, a softer diaphragm or a smaller gap all help — and the response is <b>flat below f₀</b> because the diaphragm is compliance-controlled there.</p><p><b>Try:</b> a smaller back volume stiffens the air spring, raising f₀ but lowering sensitivity (C_MT drops). Drop R_L′ to 1 MΩ and the low end droops: the capsule is a few pF driving the load, a high-pass you must keep below the audio band.</p>`;
}

/* ===== L5 · The three response shapes ===== */
function benchShapes() {
  const b = bench("bench-shapes", "Three microphones, three shapes, one second-order system", "lecture 4 + 5 · the big picture");
  if (!b) return;
  const st = { Q: 0.5 };
  slider(b.ctl, { label: "Q of the moving system", min: 0.1, max: 5, log: true, value: 0.5, dom: "me", fmt: v => v.toFixed(2), onchange: v => { st.Q = v; upd(); } });
  const plot = new Plot(b.plot, { h: 300, xmin: 0.01, xmax: 100, ymin: -50, ymax: 15, ylabel: "normalised response (dB)", xlabel: "f / f₀", xfmt: v => Number(v.toPrecision(2)), yfmt: v => v.toFixed(1), yunit: " dB", xticks: [0.01, 0.1, 1, 10, 100].map(v => ({ v, l: String(v) })) });
  function upd() {
    const Q = st.Q, xs = logspace(0.01, 100, 400);
    const den = (x) => cx(1 - x * x, x / Q);
    const lp = xs.map(x => [x, dB(cabs(cdiv(cx(1, 0), den(x))))]);
    const bp = xs.map(x => [x, dB(cabs(cdiv(cx(0, x / Q), den(x))))]);
    const hp = xs.map(x => [x, dB(cabs(cdiv(cx(-x * x, 0), den(x))))]);
    plot.set({ series: [
      { name: "condenser (pressure) — low-pass, compliance-controlled", color: DOMC.el, pts: lp },
      { name: "dynamic (pressure) — band-pass, damping-controlled", color: DOMC.me, pts: bp },
      { name: "dynamic gradient / ribbon — high-pass, mass-controlled", color: DOMC.ac, pts: hp }] });
  }
  upd();
  b.note.innerHTML = `<p>All three share the same denominator <span class="mono">jωM_MT + R_MT + 1/jωC_MT</span>. What differs is what multiplies it: the condenser's <span class="mono">E/(jωx₀)</span> puts a <span class="mono">1/jω</span> on top and cancels the spring — flat where the spring rules, so it is used <b>below</b> resonance. The moving coil's <span class="mono">Bl</span> is frequency-independent, so the output follows velocity — flat only where the damper rules, <b>around</b> resonance. The gradient mic adds one more <span class="mono">jω</span> from <span class="mono">dp/dx</span> — flat only where the mass rules, <b>above</b> resonance. Same circuit, three places to sit on it.</p>`;
}

/* ===== L4 · Coupled piston in a box (Problem 4.2) — reflected impedances ===== */
function benchPistonBox() {
  const b = bench("bench-pistonbox", "What a piston feels: air load, box spring, radiation damping", "lecture 4 · problems 4.2 / 4.4a");
  if (!b) return;
  const st = { V: 40, M: 20, S: 100, box: true };
  const seg = h("div", { class: "seg" });
  for (const [k, l] of [[true, "closed box on the back"], [false, "both sides open (baffle)"]]) seg.append(h("button", { type: "button", class: k === st.box ? "on" : "", onclick: (e) => { st.box = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  slider(b.ctl, { label: "piston area <b>S</b>", min: 10, max: 500, step: 5, value: 100, unit: "cm²", dom: "ac", onchange: v => { st.S = v; upd(); } });
  slider(b.ctl, { label: "piston mass <b>M<sub>mp</sub></b>", min: 2, max: 100, step: 1, value: 20, unit: "g", dom: "me", onchange: v => { st.M = v; upd(); } });
  slider(b.ctl, { label: "box volume <b>V</b>", min: 2, max: 200, step: 1, value: 40, unit: "L", dom: "ac", onchange: v => { st.V = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "air", label: "air load per side S²M_A1", dom: "me" }, { id: "kbox", label: "box stiffness S²/C_AB", dom: "me" }, { id: "f0", label: "piston-on-box f₀", dom: "me" }, { id: "fka", label: "ka = 1 at", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 5, xmax: 5000, ymin: -20, ymax: 60, ylabel: "|Z_M,tot| = |f/u|  (dB re 1 Ns/m)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const S = st.S * 1e-4, a = Math.sqrt(S / Math.PI), M = st.M / 1000, V = st.V / 1000;
    const CAB = V / (RHO * C0 * C0), MA1 = 8 * RHO / (3 * Math.PI * Math.PI * a);
    const Zm = (f) => {
      const zr = pistonZlumped(f, a);
      const back = st.box ? ZC(f, CAB) : zr;
      return cadd(ZL(f, M), cscale(cadd(zr, back), S * S));
    };
    const fs = logspace(5, 5000, 400);
    const pts = fs.map(f => [f, dB(cabs(Zm(f)))]);
    const Mtot = M + S * S * MA1 * (st.box ? 1 : 2);
    const f0 = st.box ? 1 / (TAU * Math.sqrt(Mtot * CAB / (S * S))) : null;
    plot.set({ series: [{ name: "total mechanical impedance", color: DOMC.me, pts }, { name: "piston mass alone jωM_mp", color: DOMC.ink2, thin: true, pts: fs.map(f => [f, dB(TAU * f * M)]) }],
      markers: f0 ? [{ x: f0, y: dB(cabs(Zm(f0))), label: `f₀ ≈ ${hz(f0)}`, color: DOMC.me }] : [], vlines: [{ x: C0 / (TAU * a), label: "ka = 1", color: DOMC.ac }] });
    ro({ air: `${sci(S * S * MA1 * 1000)} g`, kbox: st.box ? `${sci(S * S / CAB)} N/m` : "—", f0: f0 ? hz(f0) : "— (no spring)", fka: hz(C0 / (TAU * a)) });
    b.note.innerHTML = st.box
      ? `<p>The acoustic loads come across the diaphragm as <span class="mono">S²·Z_A</span>. The sealed box is a compliance to ground, so the piston feels a <b>stiffness</b> <span class="mono">S²/C_AB</span>; together with its mass (plus the front air load) that makes a resonance — the low dip. Below it the box spring rules (|Z| falls with frequency), above it the mass rules, and only the tiny radiation resistance damps the dip. This is the sealed-box loudspeaker in miniature.</p>`
      : `<p>Both sides radiate: <span class="mono">Z_M = jωM_mp + 2S²Z_ar</span>. At low frequency the radiation impedance is a mass, so the piston simply looks <b>heavier</b> (the "air load"). Above ka ≈ 1 it turns resistive: the piston is finally doing work on the air.</p>`;
  }
  upd();
}

/* ===== L6 · scattering: T = 1 + Z_ar/(ρc/S) for the standard capsule sizes ===== */
function tubeEndZ6(f, a) { // piston in the end of a long tube (the "piston on a cylinder" of the microphone slides)
  const S = Math.PI * a * a, MA1 = 0.6133 * RHO / (Math.PI * a), CA1 = 0.55 * Math.PI * Math.PI * a * a * a / (RHO * C0 * C0);
  const RA1 = 0.5045 * RHO * C0 / S, RA2 = RHO * C0 / S;
  return par(ZL(f, MA1), cadd(ZR(RA2), par(ZR(RA1), ZC(f, CA1))));
}
function scatterT(f, a) { const S = Math.PI * a * a; return cadd(cx(1, 0), cscale(tubeEndZ6(f, a), S / (RHO * C0))); }
const MIC_SIZES = { "1": ["1 inch", 0.0127], "2": ["1/2 inch", 0.00635], "4": ["1/4 inch", 0.003175], "8": ["1/8 inch", 0.0015875] };
function benchScatter() {
  const b = bench("bench-scatter", "A microphone is an obstacle: the pressure on its own diaphragm", "lecture 6A · Leach 5.1 · Lab B");
  if (!b) return;
  const st = { size: "2" };
  const chips = h("div", { class: "chips" });
  for (const [k, [n]] of Object.entries(MIC_SIZES)) chips.append(h("button", { type: "button", class: "chip" + (k === st.size ? " on" : ""), onclick: (e) => { st.size = k; $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, n));
  b.ctl.append(chips);
  const ro = readouts(b.ctl, [{ id: "k1", label: "kR = 1 at", dom: "ac" }, { id: "k3", label: "numerical +10 dB peak (kR ≈ 3) at", dom: "ac" }, { id: "t1k", label: "|T| at 1 kHz" }, { id: "t10k", label: "|T| at 10 kHz" }, { id: "hf", label: "high-frequency limit" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 100, xmax: 100000, ymin: -2, ymax: 12, ylabel: "pressure on the diaphragm re undisturbed field (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fs = logspace(100, 100000, 400), cols = { "1": DOMC.el, "2": DOMC.me, "4": DOMC.ac, "8": DOMC.ink2 };
  const NUM = [[0.1, 0.1], [0.2, 0.3], [0.5, 1.5], [1, 4], [2, 8.3], [3, 10], [4.5, 5], [6, -1], [7.5, 6], [9, 10]]; // read off slide 6
  function upd() {
    const a = MIC_SIZES[st.size][1];
    const series = Object.entries(MIC_SIZES).map(([k, [n, r]]) => ({ name: `${n}: |T| plane-reflection model`, color: cols[k], thin: k !== st.size, width: k === st.size ? 2.6 : undefined, pts: fs.map(f => [f, dB(cabs(scatterT(f, r)))]) }));
    series.push({ name: `${MIC_SIZES[st.size][0]}: numerical, edges included (slide 6)`, color: DOMC.warn, pts: NUM.map(([kr, v]) => [kr * C0 / (TAU * a), v]) });
    plot.set({ series, vlines: [{ x: C0 / (TAU * a), label: "kR = 1", color: cols[st.size] }] });
    ro({ k1: hz(C0 / (TAU * a)), k3: hz(3 * C0 / (TAU * a)), t1k: `${dB(cabs(scatterT(1000, a))).toFixed(2)} dB`, t10k: `${dB(cabs(scatterT(10000, a))).toFixed(2)} dB`, hf: "+6.02 dB (T → 2, pressure doubling)" });
  }
  upd();
  b.note.innerHTML = `<p>Treat the front of the capsule as a plane reflector with an infinitely stiff diaphragm: the reflected volume velocity equals the incident one and drives the radiation impedance, so <span class="mono">p_D = p_i·(1 + Z_ar/(ρc/S)) = T·p_i</span>. At low frequency Z_ar is a small mass and nothing happens; at high frequency Z_ar → ρc/S and the pressure <b>doubles</b>, as at any rigid wall. The red curve is the full numerical solution from the slides: the edges add diffracted waves that push the first peak to about +10 dB at kR ≈ 3 and then carve a dip near kR ≈ 6 — the plane model is only trusted <b>up to the first peak</b>.</p><p>Everything scales with size: a 1-inch capsule is disturbed from 4 kHz, a 1/8-inch one not until 34 kHz. Bigger means more sensitive but lower maximum frequency.</p>`;
}

/* ===== L6 · pressure response vs free-field response of the Problem 5 capsule ===== */
function benchFreeField() {
  const b = bench("bench-freefield", "Pressure microphone or free-field microphone? Same capsule, different damping", "lecture 6A · Problems 5 Q2 d–e · Lab C");
  if (!b) return;
  const st = { RAS: 1e7, V: 1 };
  slider(b.ctl, { label: "backplate damping <b>R<sub>AS</sub></b>", min: 1e6, max: 3e8, log: true, value: 1e7, unit: "Ns/m⁵", dom: "ac", onchange: v => { st.RAS = v; upd(); } });
  slider(b.ctl, { label: "back volume <b>V<sub>AB2</sub></b>", min: 0.1, max: 6, step: 0.05, value: 1, unit: "cm³", dom: "ac", onchange: v => { st.V = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "f₀", dom: "me" }, { id: "Q", label: "Q" }, { id: "pf", label: "pressure response: ripple to 20 kHz" }, { id: "ff", label: "free-field response: ripple to 20 kHz" }, { id: "verdict", label: "this capsule is a better…" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 100, xmax: 100000, ymin: -60, ymax: -25, ylabel: "sensitivity (dB re 1 V/Pa)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fs = logspace(100, 100000, 400);
  function upd() {
    const r = condMic({ a: 0.009, MMD: 5e-5, CMD: 4e-6, RMD: 1, MAS: 100, RAS: st.RAS, V: st.V * 1e-6, E: 200, x0: 20e-6, RL: 5e8, front: "tube" });
    const P = fs.map(f => [f, dB(cabs(r.H(f)))]), F = fs.map(f => [f, dB(cabs(r.H(f)) * cabs(scatterT(f, 0.009)))]);
    const rip = (pts) => { const v = pts.filter(p => p[0] <= 20000 && p[0] >= 200).map(p => p[1]); return Math.max(...v) - Math.min(...v); };
    plot.set({ series: [{ name: "pressure response (what the actuator in Lab C measures)", color: DOMC.me, pts: P }, { name: "free-field response = pressure response × |T| (axial incidence)", color: DOMC.el, pts: F }] });
    const rp = rip(P), rf = rip(F);
    ro({ f0: hz(r.f0), Q: r.Q.toFixed(2), pf: `${rp.toFixed(1)} dB`, ff: `${rf.toFixed(1)} dB`, verdict: rp < rf ? "pressure microphone" : "free-field microphone" });
  }
  upd();
  b.note.innerHTML = `<p>The scattering gain T is not part of the capsule: it is what the body does to the field. A <b>pressure microphone</b> is tuned so the capsule alone is flat (Q ≈ 0.7). A <b>free-field microphone</b> is deliberately <em>over</em>-damped so its pressure response droops by the same amount that T rises, and the product is flat for sound arriving on axis. Raise R_AS from the Problem 5 value and watch the verdict flip.</p><p>This is also the Lab C picture: the electrostatic actuator pulls on the diaphragm directly, so it measures the lower curve — for a B&K 4191 free-field capsule that curve <em>should</em> droop.</p>`;
}

/* ===== L6 · GUM uncertainty budget for M = E·S_D·C_MT / x0 ===== */
function benchUncertainty() {
  const b = bench("bench-uncertainty", "An uncertainty budget: which input actually moves the sensitivity?", "lecture 6B · GUM · Problems 6 Q1");
  if (!b) return;
  const st = { uC: 10, ux: 0, uE: 0, uV: 0, r: 0 };
  slider(b.ctl, { label: "u(<b>C<sub>MD</sub></b>) diaphragm compliance", min: 0, max: 20, step: 0.5, value: 10, unit: "%", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.uC = v; upd(); } });
  slider(b.ctl, { label: "u(<b>x₀</b>) gap", min: 0, max: 20, step: 0.5, value: 0, unit: "%", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.ux = v; upd(); } });
  slider(b.ctl, { label: "u(<b>E</b>) polarization voltage", min: 0, max: 5, step: 0.1, value: 0, unit: "%", dom: "el", fmt: v => v.toFixed(1), onchange: v => { st.uE = v; upd(); } });
  slider(b.ctl, { label: "u(<b>V<sub>AB</sub></b>) back volume", min: 0, max: 20, step: 0.5, value: 0, unit: "%", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.uV = v; upd(); } });
  slider(b.ctl, { label: "correlation r(C<sub>MD</sub>, x₀)", min: -1, max: 1, step: 0.05, value: 0, fmt: v => v.toFixed(2), onchange: v => { st.r = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "M", label: "M", dom: "el" }, { id: "cC", label: "∂M/∂C_MD" }, { id: "uc", label: "combined u_c(M)", dom: "el" }, { id: "rel", label: "relative · expanded (k = 2)" }]);
  const stage = h("div", { class: "stage" }); b.plot.append(stage);
  function upd() {
    const E = 200, x0 = 20e-6, a = 0.009, S = Math.PI * a * a, CMD = 4e-6, V = 1e-6, RC2 = RHO * C0 * C0, CAB = V / RC2;
    const CMT = 1 / (1 / CMD + S * S / CAB), M = E * S * CMT / x0;
    const c = { C: E * S / x0 * CMT * CMT / (CMD * CMD), x: -M / x0, E: M / E, V: E * S / x0 * CMT * CMT * S * S / (CAB * CAB) / RC2 };
    const u = { C: st.uC / 100 * CMD, x: st.ux / 100 * x0, E: st.uE / 100 * E, V: st.uV / 100 * V };
    const contrib = [["C_MD", c.C * u.C, DOMC.me], ["x₀", c.x * u.x, DOMC.me], ["E", c.E * u.E, DOMC.el], ["V_AB", c.V * u.V, DOMC.ac], ["M_MD", 0, DOMC.ink3], ["R_MD", 0, DOMC.ink3]];
    let var_ = contrib.reduce((t, x) => t + x[1] * x[1], 0) + 2 * (c.C * u.C) * (c.x * u.x) * st.r;
    const uc = Math.sqrt(Math.max(var_, 0));
    ro({ M: `${(M * 1e3).toFixed(2)} mV/Pa`, cC: `${sci(c.C, 5)} (V/Pa)/(m/N)`, uc: `${(uc * 1e3).toFixed(3)} mV/Pa`, rel: `${(100 * uc / M).toFixed(1)} % · ±${(2e3 * uc).toFixed(2)} mV/Pa` });
    const W = 640, H = 250, x0p = 110, x1 = 600, top = 30, rowH = 30, max = Math.max(uc, ...contrib.map(x => Math.abs(x[1])), 1e-9);
    let g = "";
    contrib.forEach(([n, v, col], i) => { const y = top + i * rowH, w = Math.abs(v) / max * (x1 - x0p); g += `<text x="${x0p - 10}" y="${y + 15}" text-anchor="end" font-size="12" fill="var(--ink)">${n}</text><rect x="${x0p}" y="${y + 3}" width="${Math.max(w, 0.5)}" height="16" rx="3" fill="${col}" opacity="0.8"/><text x="${x0p + w + 6}" y="${y + 15}" font-size="11" fill="var(--ink-2)">${(Math.abs(v) * 1e3).toFixed(3)} mV/Pa${v < 0 ? "  (negative coefficient)" : ""}</text>`; });
    const y = top + 6 * rowH + 8, w = uc / max * (x1 - x0p);
    g += `<line x1="${x0p}" x2="${x1}" y1="${y - 4}" y2="${y - 4}" stroke="var(--rule)"/><text x="${x0p - 10}" y="${y + 15}" text-anchor="end" font-size="12" font-weight="600" fill="var(--ink)">u_c(M)</text><rect x="${x0p}" y="${y + 3}" width="${Math.max(w, 0.5)}" height="16" rx="3" fill="var(--ink)"/><text x="${x0p + w + 6}" y="${y + 15}" font-size="11" fill="var(--ink)">${(uc * 1e3).toFixed(3)} mV/Pa</text>`;
    stage.innerHTML = `<svg viewBox="0 0 ${W} ${H}"><text x="${x0p}" y="18" font-size="11" fill="var(--ink-2)">contribution |∂M/∂x_i|·u(x_i) of each input; the bottom bar is their root-sum-square${st.r ? " plus the correlation term" : ""}</text>${g}</svg>`;
  }
  upd();
  b.note.innerHTML = `<p><span class="mono">u_c²(y) = Σ (∂f/∂x_i)²·u²(x_i)</span> — each input contributes its standard uncertainty times a <b>sensitivity coefficient</b> (nothing to do with the microphone's sensitivity M). In the flat band M = E·S_D·C_MT/x₀ contains neither the diaphragm mass nor its damping, so their coefficients are exactly zero; with the sheet's 10 % on C_MD alone the answer is <b>0.948 mV/Pa</b> (9.7 %, not 10 %, because the certain air spring carries part of the stiffness).</p><p>Now break the sheet's assumptions: give x₀ an uncertainty, then correlate it with C_MD. A softer diaphragm sags further under the bias, so the two are physically correlated; with M ∝ C_MT/x₀ a positive correlation makes the contributions partly <em>cancel</em>, a negative one makes them add. That is solution 1d's point: the uncorrelated budget is an exercise, not a calibration certificate.</p>`;
}

/* ===== L6 · pistonphone ===== */
function benchPistonphone() {
  const b = bench("bench-pistonphone", "The pistonphone: a known volume pumped into a closed cavity", "lecture 6B · Problems 6 Q3 · Lab C");
  if (!b) return;
  const st = { V: 20, dV: 4.47, Veq: 10, ps: 101.325 };
  slider(b.ctl, { label: "cavity volume <b>V</b>", min: 1, max: 100, log: true, value: 20, unit: "cm³", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.V = v; upd(); } });
  slider(b.ctl, { label: "piston stroke volume <b>ΔV</b> (rms)", min: 0.1, max: 20, step: 0.01, value: 4.47, unit: "mm³", dom: "me", fmt: v => v.toFixed(2), onchange: v => { st.dV = v; upd(); } });
  slider(b.ctl, { label: "microphone equivalent volume", min: 0, max: 300, step: 1, value: 10, unit: "mm³", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.Veq = v; upd(); } });
  slider(b.ctl, { label: "static pressure <b>p<sub>s</sub></b>", min: 85, max: 105, step: 0.1, value: 101.325, unit: "kPa", fmt: v => v.toFixed(1), onchange: v => { st.ps = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "spl", label: "level in the cavity", dom: "ac" }, { id: "mic", label: "change caused by this microphone" }, { id: "baro", label: "change vs 101.325 kPa" }, { id: "lam", label: "cavity size / λ at 250 Hz" }]);
  const plot = new Plot(b.plot, { h: 280, xmin: 1, xmax: 100, ymin: -3, ymax: 0.2, xlabel: "cavity volume (cm³)", ylabel: "level change when the microphone is inserted (dB)", xfmt: v => `${Number(v.toPrecision(2))}`, yfmt: v => v.toFixed(2), yunit: " dB", xticks: [1, 2, 5, 10, 20, 50, 100].map(v => ({ v, l: String(v) })) });
  const Vs = logspace(1, 100, 200), err = (V, Veq) => 20 * Math.log10(V / (V + Veq / 1000));
  function upd() {
    const g = 1.4, p = g * st.ps * 1e3 * (st.dV * 1e-9) / (st.V * 1e-6 + st.Veq * 1e-9), spl = 20 * Math.log10(p / 20e-6);
    plot.set({ series: [{ name: `this microphone (${st.Veq.toFixed(0)} mm³)`, color: DOMC.ac, pts: Vs.map(V => [V, err(V, st.Veq)]) }, { name: "1-inch lab standard (≈ 150 mm³)", color: DOMC.el, thin: true, pts: Vs.map(V => [V, err(V, 150)]) }, { name: "1/2-inch capsule (≈ 10 mm³)", color: DOMC.me, thin: true, pts: Vs.map(V => [V, err(V, 10)]) }], markers: [{ x: st.V, y: err(st.V, st.Veq), label: `${err(st.V, st.Veq).toFixed(3)} dB`, color: DOMC.ac }] });
    ro({ spl: `${spl.toFixed(2)} dB re 20 µPa`, mic: `${err(st.V, st.Veq).toFixed(3)} dB`, baro: `${(20 * Math.log10(st.ps / 101.325)).toFixed(2)} dB`, lam: `${(Math.cbrt(st.V * 1e-6) / (C0 / 250) * 100).toFixed(1)} % of λ` });
  }
  upd();
  b.note.innerHTML = `<p>A heavy cam-driven piston is a <b>volume-velocity source</b>; a closed cavity is a compliance <span class="mono">C_A = V/γp_s</span>. So <span class="mono">p = U/(jωC_A) = γ·p_s·ΔV/V</span>: geometry and the barometer, nothing else — that is why it is the laboratory reference (250 Hz, 124 dB). The microphone's own compliance (its "equivalent volume") sits in parallel and steals a little: <span class="mono">p = (1/jωC_A ∥ Z_A)·U</span>. The demand from Problem 3b follows at once: make <span class="mono">Z_A ≫ 1/ωC_A</span>, i.e. a <b>big cavity</b> — but still small against the wavelength. And since p ∝ p_s, a pistonphone comes with a barometric correction; a feedback-controlled 94 dB calibrator does not need one.</p>`;
}

/* ===== L2 · Problem 2.4: two masses and the five limits ===== */
function twoMass(f, p) {
  const Yl = cadd(ZC(f, p.C1), ZR(p.R1));
  return csolve([[cadd(ZL(f, p.M1), Yl), cscale(Yl, -1)], [cscale(Yl, -1), cadd(ZL(f, p.M2), Yl)]], [cx(1, 0), cx(0, 0)]);
}
function benchTwoMass() {
  const b = bench("bench-twomass", "Problem 2.4 · two masses, one link, five limits", "lecture 2 · problem 2.4");
  if (!b) return;
  const REF = { M1: 1e-3, M2: 2e-3, C1: 10e-3, R1: 0.3 };
  const CASES = { ref: ["reference", {}], m1: ["M₁ → ∞", { M1: 1e3 }], m2: ["M₂ → ∞", { M2: 1e3 }], c1: ["C₁ → 0", { C1: 1e-12 }], r1: ["R₁ → ∞", { R1: 1e9 }], none: ["R₁ → 0 & C₁ → ∞", { R1: 1e-9, C1: 1e9 }] };
  let cur = "ref";
  const chips = h("div", { class: "chips" });
  for (const [k, [l]] of Object.entries(CASES)) chips.append(h("button", { type: "button", class: "chip" + (k === cur ? " on" : ""), onclick: (e) => { cur = k; $$(".chip", chips).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(chips);
  const ro = readouts(b.ctl, [{ id: "lo", label: "u₁ at 10 Hz", dom: "me" }, { id: "lo2", label: "u₂ at 10 Hz", dom: "me" }, { id: "hi", label: "u₂ / u₁ at 10 kHz" }]);
  const plot = new Plot(b.plot, { h: 300, xmin: 1, xmax: 10000, ymin: -80, ymax: 40, ylabel: "velocity (dB re 1 m/s per N)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fs = logspace(1, 10000, 400);
  const ref = fs.map(f => twoMass(f, REF));
  function upd() {
    const p = Object.assign({}, REF, CASES[cur][1]);
    const rows = fs.map(f => twoMass(f, p));
    plot.set({ series: [
      { name: "u₁ (driven mass)", color: DOMC.me, pts: fs.map((f, i) => [f, dB(cabs(rows[i][0]))]) },
      { name: "u₂ (free mass)", color: DOMC.ac, pts: fs.map((f, i) => [f, dB(cabs(rows[i][1]))]) },
      { name: "reference u₁", color: DOMC.ink3, thin: true, pts: fs.map((f, i) => [f, dB(cabs(ref[i][0]))]) }] });
    const i10 = 133, iend = fs.length - 1;
    ro({ lo: `${sci(cabs(rows[i10][0]))} m/s`, lo2: `${sci(cabs(rows[i10][1]))} m/s`, hi: sci(cabs(rows[iend][1]) / cabs(rows[iend][0]), 2) });
    b.note.innerHTML = `<p><b>${CASES[cur][0]}.</b> ` + {
      ref: "Below the link resonance (≈ 62 Hz: reduced mass 0.67 g on 10 mm/N) the two masses move together as 3 g. At it they swing against each other. Above it the link cannot transmit force and u₂ falls away 12 dB/oct faster than u₁.",
      m1: "The driven mass is a wall. Nothing moves: both curves drop to the floor.",
      m2: "M₂ is a wall, so M₁ now sits on C₁ against it: a plain mass-spring with resonance at 1/(2π√(1 g · 10 mm/N)) ≈ 50 Hz. Below it u₁ is <i>smaller</i> than the reference (spring-controlled instead of free), u₂ = 0.",
      c1: "A rigid rod: one 3 g body, u₁ = u₂ everywhere (the dashed reference is only equal at low frequency).",
      r1: "An infinitely stiff damper is also a rod: u₁ = u₂ everywhere.",
      none: "No link at all: M₁ alone is lighter than the 3 g pair, so u₁ is at or above the reference; M₂ never moves.",
    }[cur] + "</p>";
  }
  upd();
}

/* ===== boot ===== */
document.addEventListener("DOMContentLoaded", () => {
  renderMath();
  benchPhasor(); benchResonator(); benchDual(); benchHelmholtz(); benchTube(); benchRadiation();
  benchCoupling(); benchSpeakerZ(); benchPistonBox(); benchDynMic();
  benchPolar(); benchProximity(); benchCondenser(); benchShapes(); benchTwoMass();
  benchScatter(); benchFreeField(); benchUncertainty(); benchPistonphone();
  if (window.QUIZZES) { for (const [lec, qs] of Object.entries(QUIZZES)) { const root = document.getElementById(`quiz-${lec}`); if (root) { buildQuiz(root, lec, qs); TOTAL_Q += qs.length; const a = $(`.wire a[data-quiz="${lec}"]`); if (a) a.dataset.n = qs.length; } } }
  updateProgress();
  setupNav(); setupTheme();
  renderMath();
});
