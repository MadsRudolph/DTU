/* The Sound Bench — lectures 9–12 (hearing, physiological acoustics, vibration isolation,
   sound insulation). Written 26-Nov-2026 from the vault notes (decks only, no recordings)
   and the exercise sheets + official solutions. Physics first (pure functions), then benches. */
"use strict";


/* ===== L9 · hearing: frequency selectivity and masking ===== */
const erb = (fHz) => 24.7 * (4.37 * fHz / 1000 + 1);
const barkCB = (fHz) => 25 + 75 * Math.pow(1 + 1.4 * (fHz / 1000) ** 2, 0.69);
function maskedThreshold(p) {                                     // power-spectrum model, rectangular filter: Ls = N0 + 10log k + 10log min(BW, ERB)
  const E = erb(p.f);
  return { E, cb: barkCB(p.f), third: 0.2316 * p.f, Ls: p.N0 + 10 * Math.log10(p.k) + 10 * Math.log10(Math.min(p.BW, E)) };
}

function benchERB9() {
  const b = bench("bench-erb9", "How wide is an auditory filter? Masking by band-limited noise", "lecture 9 · exercise 1"); if (!b) return;
  const st = { f: 1000, N0: 40, k: 0.3, BW: 1000 };
  slider(b.ctl, { label: "tone / centre frequency <b>f</b>", min: 50, max: 15000, value: st.f, log: true, dom: "el", fmt: v => hz(v), onchange: v => { st.f = v; upd(); } });
  slider(b.ctl, { label: "noise spectrum level <b>N₀</b>", min: 0, max: 80, step: 1, value: st.N0, unit: "dB/Hz", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.N0 = v; upd(); } });
  slider(b.ctl, { label: "noise bandwidth", min: 5, max: 5000, value: st.BW, log: true, dom: "ac", fmt: v => hz(v), onchange: v => { st.BW = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "erb", label: "ERB = 24.7(4.37F + 1)", dom: "el" }, { id: "cmp", label: "Bark critical band / third octave" }, { id: "ls", label: "masked threshold L_s (k = 0.3)", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 270, xmin: 5, xmax: 5000, ymin: 30, ymax: 90, xlabel: "noise bandwidth", ylabel: "masked threshold (dB SPL)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const r = maskedThreshold(st), bws = logspace(5, 5000, 200);
    plot.set({ series: [{ name: `threshold at ${hz(st.f)}`, color: DOMC.ac, pts: bws.map(w => [w, maskedThreshold({ ...st, BW: w }).Ls]) }],
      vlines: [{ x: r.E, label: "ERB", color: DOMC.el }, { x: st.BW, label: "noise", color: DOMC.ink }] });
    ro({ erb: `${r.E.toFixed(1)} Hz`, cmp: `${r.cb.toFixed(0)} Hz / ${r.third.toFixed(0)} Hz`, ls: `${r.Ls.toFixed(1)} dB` });
  }
  upd();
  b.note.innerHTML = `<p>The power-spectrum model: only the noise inside the auditory filter around the tone masks it, and the tone is just heard when its power is k times that noise power. With a rectangular filter of width ERB, <span class="m">L_s = N_0 + 10\\log k + 10\\log\\min(B, \\mathrm{ERB})</span>. The threshold rises 3 dB per doubling of the noise band until the band fills the filter, then stops: Fletcher's band-widening experiment. Exercise 1: ERB = <b>35.5 / 132.6 / 1104 Hz</b> at 0.1 / 1 / 10 kHz; wideband noise at 40 dB/Hz masks up to <b>50.3 / 56.0 / 65.2 dB</b>; a 20 Hz band masks <b>47.8 dB</b> at all three (narrower than every filter). All as the official solution.</p><p><b>Try:</b> above about 200 Hz the ERB is narrower than a third octave; that is why third-octave analysis over-estimates masking in the mid range.</p>`;
  renderMath(b.note);
}

/* ===== L10 · physiological acoustics ===== */
const GW = { A: 20682, a: 61.765, k: 140.6, L: 0.034 };          // Greenwood, x in metres from the base
const greenwoodF = (x) => GW.A * Math.pow(10, -GW.a * x) - GW.k;
const greenwoodX = (F) => -Math.log10((F + GW.k) / GW.A) / GW.a;
function abrAverage(p) {                                          // p: {EP, N, frac, Nart, target, rate} in µV, dB, sweeps/s
  const P = (1 - p.frac) * p.N * p.N + p.frac * p.Nart * p.Nart;   // mean noise power per sweep
  const Neff = Math.sqrt(P);
  const snr1 = 20 * Math.log10(p.EP / Neff), snrClean1 = 20 * Math.log10(p.EP / p.N);
  const nNeed = Math.pow(10, (p.target - snr1) / 10), nClean = Math.pow(10, (p.target - snrClean1) / 10) / (1 - p.frac);
  return { P, Neff, snr1, snrClean1, nNeed, nClean, tNeed: nNeed / p.rate, tClean: nClean / p.rate };
}
const oaeX = (tMs, v = 3) => v * tMs / 1000 / 2;                  // round trip at v m/s → place

function benchGreenwood10() {
  const b = bench("bench-greenwood10", "Where on the basilar membrane? The Greenwood map", "lecture 10 · exercise 1 + 3"); if (!b) return;
  const st = { f: 1000, t: 12 };
  slider(b.ctl, { label: "tone frequency <b>f</b>", min: 25, max: 20000, value: st.f, log: true, dom: "el", fmt: v => hz(v), onchange: v => { st.f = v; upd(); } });
  slider(b.ctl, { label: "OAE round-trip time", min: 1, max: 20, step: 0.5, value: st.t, unit: "ms", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.t = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "x", label: "place of f (from the base)", dom: "el" }, { id: "ends", label: "base / apex (34 mm)" }, { id: "oct", label: "one octave up moves" }, { id: "oae", label: "OAE: x = 3 m/s · t/2 → f", dom: "me" }]);
  const plot = new Plot(b.plot, { h: 280, xlog: false, xmin: 0, xmax: 34, ymin: 1, ymax: 4.5, yticks: [1, 2, 3, 4], xlabel: "distance from the base x (mm)", xfmt: v => v.toFixed(0) + " mm", ylabel: "characteristic frequency (log)", yfmt: v => hz(Math.pow(10, v)) });
  function upd() {
    const xs = linspace(0, 34, 200);
    const x = greenwoodX(st.f) * 1000, xo = oaeX(st.t) * 1000, fo = greenwoodF(xo / 1000);
    plot.set({ series: [{ name: "F = 20682·10^(−61.765x) − 140.6", color: DOMC.ac, pts: xs.map(v => [v, Math.log10(Math.max(10, greenwoodF(v / 1000)))]) }],
      vlines: [{ x, label: hz(st.f), color: DOMC.el }, { x: Math.min(34, xo), label: "OAE", color: DOMC.me }] });
    ro({ x: `${x.toFixed(1)} mm`, ends: `${hz(greenwoodF(0))} / ${greenwoodF(GW.L).toFixed(1)} Hz`, oct: `${(x - greenwoodX(2 * st.f) * 1000).toFixed(1)} mm`, oae: `${xo.toFixed(1)} mm → ${hz(fo)}` });
  }
  upd();
  b.note.innerHTML = `<p>Exercise 1: the base (x = 0) maps to <b>20 541 Hz</b>, the apex (34 mm) to <b>23.7 Hz</b> (official: 24 Hz). 1, 2 and 4 kHz sit at 20.4, 15.9 and 11.3 mm. Exercise 3: a travelling wave at 3 m/s with an OAE round trip of 12 / 7 / 5 ms reaches 18 / 10.5 / 7.5 mm, i.e. <b>1458 / 4505 / 6977 Hz</b>, as in the official solution.</p><p><b>Try:</b> move f by octaves above 1 kHz: each octave is about 4.9 mm. The map is logarithmic because the membrane stiffness falls exponentially from base to apex. The frequency axis is logarithmic, so the map is almost a straight line.</p>`;
}

function benchABR10() {
  const b = bench("bench-abr10", "Digging an ABR out of the EEG: averaging and artefact rejection", "lecture 10 · exercise 2"); if (!b) return;
  const st = { EP: 0.3, N: 3, frac: 0.1, Nart: 30, target: 10, rate: 20 };
  for (const [k, label, min, max, step, unit, dom] of [["EP", "evoked potential", 0.05, 1, 0.01, "µV", "el"], ["N", "background EEG noise (rms)", 0.5, 10, 0.1, "µV", "me"], ["frac", "share of sweeps with artefacts", 0, 0.5, 0.01, "", "me"], ["Nart", "artefact sweep noise", 3, 60, 1, "µV", "me"], ["target", "target SNR", 0, 20, 1, "dB", "ac"]])
    slider(b.ctl, { label, min, max, step, value: st[k], unit, dom, fmt: v => k === "frac" ? (v * 100).toFixed(0) + " %" : String(v), onchange: v => { st[k] = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "s1", label: "SNR of one sweep (clean / mixed)", dom: "el" }, { id: "ne", label: "effective noise √P" }, { id: "n", label: "sweeps for target, no rejection", dom: "ac" }, { id: "nr", label: "… with rejection (keep only clean)", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 260, xmin: 1, xmax: 1e5, ymin: -40, ymax: 30, xlabel: "number of sweeps n", xfmt: v => v >= 1000 ? (v / 1000) + "k" : String(v), ylabel: "SNR after averaging (dB)", yfmt: v => v.toFixed(0), yunit: " dB" });
  function upd() {
    const r = abrAverage(st), ns = logspace(1, 1e5, 200);
    plot.set({ series: [{ name: "all sweeps (artefacts included)", color: DOMC.el, pts: ns.map(n => [n, r.snr1 + 10 * Math.log10(n)]) }, { name: "artefact sweeps rejected", color: DOMC.ac, pts: ns.map(n => [n, r.snrClean1 + 10 * Math.log10(n * (1 - st.frac))]) }],
      vlines: [{ x: r.nNeed, label: "no rejection", color: DOMC.el }, { x: r.nClean, label: "rejection", color: DOMC.ac }] });
    ro({ s1: `${r.snrClean1.toFixed(1)} / ${r.snr1.toFixed(2)} dB`, ne: `${r.Neff.toFixed(3)} µV (P ${r.P.toFixed(1)} µV²)`, n: `${Math.round(r.nNeed)} (${r.tNeed.toFixed(0)} s at 20/s)`, nr: `${Math.round(r.nClean)} (${r.tClean.toFixed(1)} s)` });
  }
  upd();
  b.note.innerHTML = `<p>Exercise 2 start values: EP 0.3 µV in 3 µV of EEG is <b>−20 dB</b> per sweep. Averaging n sweeps lowers independent noise by √n, so the SNR rises 10 log n (<b>+3 dB per doubling</b>): +10 dB needs 1000 sweeps (50 s at 20 sweeps/s). With 10 % of sweeps at 30 µV the mean noise power is 98.1 µV² (√ = 9.905 µV): now +10 dB needs about <b>10 900 sweeps (545 s)</b>; throwing the artefact sweeps away needs only <b>1111 (55.6 s)</b>, 9.8× faster. All as the official solution.</p><p><b>Try:</b> set artefacts to 0 %: both curves meet. Raise the artefact level: a few loud sweeps dominate the noise power, which is why every clinical ABR system rejects them.</p>`;
}

/* ===== L11 · structure-borne sound and vibration isolation ===== */
const transT = (W, z) => Math.sqrt((1 + (2 * z * W) ** 2) / ((1 - W * W) ** 2 + (2 * z * W) ** 2));
const f0FromDeflection = (xi, g = 9.81) => Math.sqrt(g / xi) / TAU;
const critFreq = (h, cL, c = 344) => c * c / (1.8 * cL * h);

function benchIso11() {
  const b = bench("bench-iso11", "A machine on springs: transmissibility and isolation", "lecture 11 · problems 2–3 · old exam"); if (!b) return;
  const st = { xi: 10, z: 0.05, f: 25 };
  slider(b.ctl, { label: "static deflection <b>ξ₀</b>", min: 0.5, max: 50, step: 0.1, value: st.xi, unit: "mm", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.xi = v; upd(); } });
  slider(b.ctl, { label: "damping ratio <b>ζ</b>", min: 0.005, max: 1, step: 0.005, value: st.z, dom: "me", fmt: v => v.toFixed(3), onchange: v => { st.z = v; upd(); } });
  slider(b.ctl, { label: "forcing frequency <b>f</b>", min: 1, max: 200, value: st.f, log: true, dom: "el", fmt: v => hz(v), onchange: v => { st.f = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "f₀ = (1/2π)√(g/ξ₀)", dom: "me" }, { id: "iso", label: "isolation starts at √2·f₀" }, { id: "T", label: "T at f (force to the floor)", dom: "el" }, { id: "pk", label: "peak at resonance ≈ 1/2ζ" }]);
  const plot = new Plot(b.plot, { h: 280, xmin: 1, xmax: 200, ymin: -50, ymax: 40, xlabel: "frequency", ylabel: "20 log T (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const f0 = f0FromDeflection(st.xi / 1000), fs = logspace(1, 200, 400), T = transT(st.f / f0, st.z);
    plot.set({ series: [{ name: `ζ = ${st.z}`, color: DOMC.me, pts: fs.map(f => [f, dB(transT(f / f0, st.z))]) }, { name: "undamped", color: DOMC.ink3, thin: true, pts: fs.map(f => [f, Math.max(-60, Math.min(60, dB(transT(f / f0, 1e-4))))]) }],
      regions: [{ from: Math.SQRT2 * f0, to: 200, label: "isolates", color: "var(--ac-soft)" }], vlines: [{ x: f0, label: "f₀", color: DOMC.warn }, { x: st.f, label: "f", color: DOMC.el }] });
    ro({ f0: hz(f0), iso: hz(Math.SQRT2 * f0), T: `${T.toFixed(3)} (${dB(T).toFixed(1)} dB)`, pk: `${dB(transT(1, st.z)).toFixed(1)} dB` });
  }
  upd();
  b.note.innerHTML = `<p><span class="m">T = \\sqrt{\\dfrac{1 + (2\\zeta\\Omega)^2}{(1-\\Omega^2)^2 + (2\\zeta\\Omega)^2}}</span>, Ω = f/f₀. Start values are the old-exam question: 10 mm of static deflection gives <b>f₀ = 4.98 Hz</b>, so the mounts only start to help above <b>√2·f₀ = 7.04 Hz</b>. Every curve passes T = 1 at Ω = √2, whatever ζ; above it the undamped curve falls 12 dB/octave (Ω = 3: −18.1 dB, Ω = 10: −39.9 dB).</p><p><b>Try:</b> set f = 50 Hz (Ω ≈ 10) and raise ζ from 0.01 to 0.5: the isolation drops from about −40 to −20 dB, because the damper is a stiff path at high frequency. Damping only helps when you pass through the resonance (start-up, run-down). In 34870 terms this is a current divider in the mobility analogy.</p>`;
  renderMath(b.note);
}

function benchBending11() {
  const b = bench("bench-bend11", "Bending waves and the critical frequency of a plate", "lecture 11 · deck + course text ch. 6"); if (!b) return;
  const mats = [["4 mm glass", 0.004, 5151], ["100 mm concrete", 0.1, 3360], ["200 mm concrete", 0.2, 3360], ["13 mm gypsum", 0.013, 2000]];
  const st = { h: 0.004, cL: 5151 };
  const chips = h("div", { class: "chips" });
  const pick = (e, hh, c) => { st.h = hh; st.cL = c; sh.set(hh * 1000); sc.set(c); chips.querySelectorAll(".chip").forEach(x => x.classList.toggle("on", x === e.target)); upd(); };
  for (const [n, hh, c] of mats) chips.append(h("button", { type: "button", class: "chip me" + (hh === st.h ? " on" : ""), onclick: (e) => pick(e, hh, c) }, n));
  b.ctl.append(chips);
  const sh = slider(b.ctl, { label: "thickness <b>h</b>", min: 1, max: 300, value: st.h * 1000, log: true, unit: "mm", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.h = v / 1000; upd(); } });
  const sc = slider(b.ctl, { label: "longitudinal speed <b>c_L</b>", min: 500, max: 6000, step: 10, value: st.cL, unit: "m/s", dom: "me", fmt: v => v.toFixed(0), onchange: v => { st.cL = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "fc", label: "f_c = c²/(1.8·c_L·h)", dom: "ac" }, { id: "cb", label: "c_B at 1 kHz = √(1.8·c_L·h·f)", dom: "me" }]);
  const plot = new Plot(b.plot, { h: 260, xmin: 20, xmax: 20000, ymin: 0, ymax: 1000, xlabel: "frequency", ylabel: "wave speed (m/s)", yfmt: v => v.toFixed(0), yunit: " m/s" });
  function upd() {
    const fc = critFreq(st.h, st.cL), fs = logspace(20, 20000, 300);
    plot.set({ series: [{ name: "bending wave c_B (∝ √f)", color: DOMC.me, pts: fs.map(f => [f, Math.sqrt(1.8 * st.cL * st.h * f)]) }, { name: "sound in air, 344 m/s", color: DOMC.ac, pts: [[20, 344], [20000, 344]] }],
      vlines: [{ x: fc, label: "f_c", color: DOMC.warn }] });
    ro({ fc: hz(fc), cb: `${Math.sqrt(1.8 * st.cL * st.h * 1000).toFixed(0)} m/s` });
  }
  upd();
  b.note.innerHTML = `<p>Bending waves are dispersive: <span class="m">c_B = \\sqrt{1.8\\,c_L h f}</span> grows with √f. Where c_B reaches the speed of sound in air the plate couples perfectly to the air: the <b>critical (coincidence) frequency</b> <span class="m">f_c = c^2/(1.8\\,c_L h)</span>. 4 mm glass: <b>3190 Hz</b>; 100 mm concrete: <b>196 Hz</b>; 200 mm: <b>98 Hz</b>. Thick heavy walls have f_c low; thin light panels high. This is the dip in the sound-insulation curve of lecture 12.</p>`;
  renderMath(b.note);
}

/* ===== L12 · sound insulation (ρ = 1.2, c = 343, as the Week 12 note) ===== */
const SI = { rho: 1.2, c: 343 };
const massLawR0 = (f, m) => 20 * Math.log10(TAU * f * m / (2 * SI.rho * SI.c));
function singleWall(f, p) {                                  // p: {h, rhoM, E, nu, eta}
  const m = p.rhoM * p.h, B = p.E * p.h ** 3 / (12 * (1 - p.nu * p.nu));
  const fc = SI.c * SI.c / TAU * Math.sqrt(m / B);
  const cL = Math.sqrt(p.E / (p.rhoM * (1 - p.nu * p.nu)));
  const Rmax = 20 * Math.log10(p.rhoM * cL / (2 * SI.rho * SI.c)) - 5;
  const R0 = massLawR0(f, m), above = R0 + 10 * Math.log10(2 * p.eta * f / (Math.PI * fc));
  let R = f < fc ? Math.max(R0 - 5 + 20 * Math.log10(Math.abs(1 - (f / fc) ** 2) + 1e-12), above) : above;
  return { m, fc, Rmax, R0, R: Math.min(R, Rmax) };
}
function doubleWall(f, m1, m2, d) {
  const f0 = SI.c / TAU * Math.sqrt(SI.rho / d * (1 / m1 + 1 / m2)), fd = SI.c / (TAU * d), k = TAU * f / SI.c;
  const R1 = massLawR0(f, m1) - 5, R2 = massLawR0(f, m2) - 5, Rsum = massLawR0(f, m1 + m2) - 5;
  const R = f < f0 ? Rsum : f < fd ? Math.max(Rsum, R1 + R2 + 20 * Math.log10(2 * k * d)) : R1 + R2 + 6;
  return { f0, fd, R, Rsum };
}
const compositeR = (parts) => { const S = parts.reduce((a, p) => a + p.S, 0); return -10 * Math.log10(parts.reduce((a, p) => a + p.S * Math.pow(10, -p.R / 10), 0) / S); };
const receiveLevel = (L1, R, S, V, T) => L1 - R + 10 * Math.log10(S / (55.3 * V / (SI.c * T)));

function benchWall12() {
  const b = bench("bench-wall12", "One wall: mass law, coincidence dip, upper limit", "lecture 12 · deck pp. 20–27"); if (!b) return;
  const st = { h: 0.10, rhoM: 2300, E: 2.6e10, nu: 0.2, eta: 0.02 };
  const mats = [["concrete", 2300, 2.6e10, 0.2, 0.02, 0.10], ["gypsum board", 800, 2.5e9, 0.3, 0.02, 0.0125], ["glass", 2500, 7e10, 0.24, 0.005, 0.004]];
  const chips = h("div", { class: "chips" });
  const pick = (e, x) => { st.rhoM = x[1]; st.E = x[2]; st.nu = x[3]; st.eta = x[4]; st.h = x[5]; sh.set(x[5] * 1000); chips.querySelectorAll(".chip").forEach(c => c.classList.toggle("on", c === e.target)); upd(); };
  for (const x of mats) chips.append(h("button", { type: "button", class: "chip me" + (x[0] === "concrete" ? " on" : ""), onclick: (e) => pick(e, x) }, x[0]));
  b.ctl.append(chips);
  const sh = slider(b.ctl, { label: "thickness <b>h</b>", min: 2, max: 300, value: st.h * 1000, log: true, unit: "mm", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.h = v / 1000; upd(); } });
  slider(b.ctl, { label: "loss factor <b>η</b>", min: 0.001, max: 0.2, value: st.eta, log: true, dom: "me", fmt: v => v.toFixed(3), onchange: v => { st.eta = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "m", label: "surface mass m = ρ_M h", dom: "me" }, { id: "fc", label: "f_c = (c²/2π)√(m/B)", dom: "ac" }, { id: "r", label: "R at 100 Hz / 1 kHz", dom: "el" }, { id: "max", label: "upper limit 20log(ρ_M c_L/2ρc) − 5" }]);
  const plot = new Plot(b.plot, { h: 280, xmin: 50, xmax: 5000, ymin: 0, ymax: 90, xlabel: "frequency", ylabel: "R (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const fs = logspace(50, 5000, 400), w = singleWall(1000, st);
    plot.set({ series: [{ name: "R (field incidence, with coincidence)", color: DOMC.el, pts: fs.map(f => [f, singleWall(f, st).R]) }, { name: "normal-incidence mass law R₀", color: DOMC.ink3, thin: true, pts: fs.map(f => [f, massLawR0(f, w.m)]) }],
      vlines: [{ x: w.fc, label: "f_c", color: DOMC.warn }] });
    ro({ m: `${w.m.toFixed(1)} kg/m²`, fc: hz(w.fc), r: `${singleWall(100, st).R.toFixed(1)} / ${w.R.toFixed(1)} dB`, max: `${w.Rmax.toFixed(1)} dB` });
  }
  upd();
  b.note.innerHTML = `<p>Mass law: <span class="m">R_0 = 20\\log(\\omega m/2\\rho c)</span> (the deck's 20 log(f m) − 43; exact −42.35): <b>+6 dB per doubling</b> of mass or frequency; field incidence is about 5 dB lower. At the <b>critical frequency</b> the bending wave in the wall matches the trace of the sound wave and the wall lets sound through; above it, <span class="m">R = R_0 + 10\\log(2\\eta f/\\pi f_c)</span>, so damping matters only there. 10 cm concrete: m = 230 kg/m², <b>f_c = 189 Hz</b>, upper limit about 74.5 dB. (The vibration lecture's c²/(1.8 c_L h) gives 196 Hz with c_L = 3360 m/s: same physics, different material values.)</p><p><b>Try:</b> make the concrete thicker: f_c falls as 1/h (B ∝ h³, m ∝ h). Pick glass: f_c sits in the speech range, which is why thin windows are weak at 2–4 kHz.</p>`;
  renderMath(b.note);
}

function benchDouble12() {
  const b = bench("bench-double12", "Two leaves with air between: the double wall", "lecture 12 · deck pp. 28–33 · 2024 Q8, Q11"); if (!b) return;
  const st = { m1: 15.6, m2: 15.6, d: 0.10 };
  slider(b.ctl, { label: "leaf 1 <b>m₁</b>", min: 2, max: 100, step: 0.1, value: st.m1, unit: "kg/m²", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.m1 = v; upd(); } });
  slider(b.ctl, { label: "leaf 2 <b>m₂</b>", min: 2, max: 100, step: 0.1, value: st.m2, unit: "kg/m²", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.m2 = v; upd(); } });
  slider(b.ctl, { label: "cavity <b>d</b>", min: 10, max: 300, step: 1, value: st.d * 1000, unit: "mm", dom: "ac", fmt: v => v.toFixed(0), onchange: v => { st.d = v / 1000; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f0", label: "mass-air-mass f₀", dom: "warn" }, { id: "fd", label: "f_d = c/2πd", dom: "ac" }, { id: "g", label: "gain over one wall of m₁+m₂ at 500 Hz", dom: "el" }]);
  const plot = new Plot(b.plot, { h: 280, xmin: 20, xmax: 5000, ymin: 0, ymax: 120, xlabel: "frequency", ylabel: "R (dB, field incidence, no coincidence)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const fs = logspace(20, 5000, 400), a = doubleWall(500, st.m1, st.m2, st.d);
    plot.set({ series: [{ name: "double wall", color: DOMC.el, pts: fs.map(f => [f, doubleWall(f, st.m1, st.m2, st.d).R]) }, { name: "one wall of the same total mass", color: DOMC.ink3, pts: fs.map(f => [f, doubleWall(f, st.m1, st.m2, st.d).Rsum]) }],
      vlines: [{ x: a.f0, label: "f₀", color: DOMC.warn }, { x: a.fd, label: "f_d", color: DOMC.ac }] });
    ro({ f0: hz(a.f0), fd: hz(a.fd), g: `${(a.R - a.Rsum).toFixed(1)} dB` });
  }
  upd();
  b.note.innerHTML = `<p>The air in the cavity is a spring between two masses: <span class="m">f_0 = \\frac{c}{2\\pi}\\sqrt{\\frac{\\rho}{d}\\left(\\frac1{m_1}+\\frac1{m_2}\\right)}</span>. Below f₀ the leaves move together (one wall of mass m₁+m₂); at f₀ the wall is <i>worse</i> than a single leaf; above it R climbs 18 dB/octave, <span class="m">R_1+R_2+20\\log 2kd</span>, until the cavity stops being thin at <span class="m">f_d = c/2\\pi d</span>, then <span class="m">R_1+R_2+6</span> (12 dB/oct). Start values: two 15.6 kg/m² gypsum boards 10 cm apart: <b>f₀ = 67.7 Hz, f_d = 546 Hz</b>. A simplified model: no coincidence, no cavity absorption, no flanking.</p><p><b>Try:</b> halve d: f₀ rises by √2. The whole trick is to put f₀ below the range you care about (wide cavity, heavy leaves).</p>`;
  renderMath(b.note);
}

function benchComposite12() {
  const b = bench("bench-comp12", "A wall with a door, and the level next door", "lecture 12 · deck slides 18–19 · 2023 Q8"); if (!b) return;
  const st = { S: 20, R: 44, Sd: 2, Rd: 26, L1: 80, V: 60, T: 0.5 };
  for (const [k, label, min, max, step, unit, dom] of [["S", "total wall area S", 2, 60, 1, "m²", "me"], ["R", "wall R", 20, 70, 1, "dB", "el"], ["Sd", "door / window area", 0, 10, 0.1, "m²", "me"], ["Rd", "door R", 5, 50, 1, "dB", "el"], ["L1", "source room level L₁", 50, 110, 1, "dB", "ac"], ["V", "receiving room volume", 10, 300, 1, "m³", "ac"], ["T", "receiving room T", 0.2, 2, 0.05, "s", "ac"]])
    slider(b.ctl, { label, min, max, step, value: st[k], unit, dom, fmt: v => String(v), onchange: v => { st[k] = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "rc", label: "composite R", dom: "el" }, { id: "l2", label: "L₂ = L₁ − R + 10log(S/A₂)", dom: "ac" }, { id: "a", label: "A₂ = 55.3V/(cT)" }]);
  const plot = new Plot(b.plot, { h: 220, xlog: false, xmin: 0, xmax: 10, ymin: 0, ymax: 70, xlabel: "door / window area (m²)", xfmt: v => v.toFixed(0) + " m²", ylabel: "composite R (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const parts = (sd) => [{ S: st.S - sd, R: st.R }, { S: sd, R: st.Rd }];
    const Rc = compositeR(parts(Math.min(st.Sd, st.S))), A = 55.3 * st.V / (SI.c * st.T);
    plot.set({ series: [{ name: "composite R", color: DOMC.el, pts: linspace(0, 10, 101).map(x => [x, compositeR(parts(Math.min(x, st.S)))]) }], vlines: [{ x: st.Sd, label: "now", color: DOMC.ink }] });
    ro({ rc: `${Rc.toFixed(1)} dB`, l2: `${receiveLevel(st.L1, Rc, st.S, st.V, st.T).toFixed(1)} dB`, a: `${A.toFixed(1)} m² Sabine` });
  }
  upd();
  b.note.innerHTML = `<p>Transmission coefficients add by area, not the R values: <span class="m">R = -10\\log\\big(\\tfrac1S\\sum S_i 10^{-R_i/10}\\big)</span>. Start values: an 18 m² wall at 44 dB with a 2 m² door at 26 dB gives <b>35.4 dB</b> (slide 18 reads 35 off its chart): the weak door wins. Two rooms: <span class="m">L_2 = L_1 - R + 10\\log(S/A_2)</span>; 2023 Q8 (80 dB, R = 40, S = 12 m², 60 m³, 0.5 s) gives <b>37.9 dB</b>: set S = 12, R = 40, door area 0.</p><p><b>Try:</b> a 1 m² opening (R = 0) in a 45 dB wall caps the whole wall near 13 dB: leaks dominate.</p>`;
  renderMath(b.note);
}

document.addEventListener("DOMContentLoaded", () => { benchERB9(); benchGreenwood10(); benchABR10(); benchIso11(); benchBending11(); benchWall12(); benchDouble12(); benchComposite12(); renderMath(); });
