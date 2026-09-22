/* The Analogy Bench — Lab A: analogy circuits, solved live in the browser.
   Same physics as the KiCad/ngspice runthrough in the vault; the numbers the
   quiz wants (51.3 Hz, 1288 Hz, 47/176 Hz, 43.7 Hz, 4.90/158.5/733 Hz) fall out. */
"use strict";

/* radiation network of a baffled piston, BOTH faces in series (Lab A part 3) */
function pistonBothSides(f, a) { return cscale(pistonZlumped(f, a), 2); }
/* piston in a long tube (unflanged end), Lab A part 2d */
function tubeEndZ(f, a) {
  const S = Math.PI * a * a;
  const MA1 = 0.6133 * RHO / (Math.PI * a), CA1 = 0.55 * Math.PI * Math.PI * a * a * a / (RHO * C0 * C0);
  const RA1 = 0.5045 * RHO * C0 / S, RA2 = RHO * C0 / S;
  return par(ZL(f, MA1), cadd(ZR(RA2), par(ZR(RA1), ZC(f, CA1))));
}

/* ===== Part 1 (+3): dual-diaphragm loudspeaker, mobility analogy, two velocity nodes ===== */
const P1 = { Mmvc: 6e-3, Cmsp: 1.3e-3, Rmsp: 0.5, Mmd: 5e-3, Cmsr: 2.7e-3, Rmsr: 0.22, stiff: { Cmd: 1e-10, Rmd: 5000 }, soft: { Cmd: 3e-6, Rmd: 5 }, Si: 60e-4, So: 210e-4 };
function dualDiaphragm(f, link, air) {
  // mobility analogy: node "voltages" are velocities, "currents" are forces, so an element's
  // admittance is numerically the mechanical impedance it represents
  const Ymass = (M) => ZL(f, M), Ycomp = (C) => ZC(f, C), Ydamp = (R) => ZR(R);
  const ai = Math.sqrt(P1.Si / Math.PI), ao = Math.sqrt(P1.So / Math.PI);
  let Yvc = cadd(cadd(Ymass(P1.Mmvc), Ycomp(P1.Cmsp)), Ydamp(P1.Rmsp));
  let Yd = cadd(cadd(Ymass(P1.Mmd), Ycomp(P1.Cmsr)), Ydamp(P1.Rmsr));
  if (air) { Yvc = cadd(Yvc, cscale(pistonBothSides(f, ai), P1.Si * P1.Si)); Yd = cadd(Yd, cscale(pistonBothSides(f, ao), P1.So * P1.So)); }
  const Yl = cadd(Ycomp(link.Cmd), Ydamp(link.Rmd));
  const [uvc, ud] = csolve([[cadd(Yvc, Yl), cscale(Yl, -1)], [cscale(Yl, -1), cadd(Yd, Yl)]], [cx(1, 0), cx(0, 0)]);
  const ZM = cinv(uvc);
  const far = cscale(cmul(cx(0, TAU * f * RHO), cadd(cscale(uvc, P1.Si), cscale(ud, P1.So))), 1 / (TAU * 1)); // half space, 1 m
  const pfi = air ? cmul(pistonZlumped(f, ai), cscale(uvc, P1.Si)) : cx(0, 0), pfo = air ? cmul(pistonZlumped(f, ao), cscale(ud, P1.So)) : cx(0, 0);
  return { uvc, ud, ZM, far, pfi, pfo };
}
function benchLab1() {
  const b = bench("bench-lab1", "Part 1 & 3 · the dual-diaphragm loudspeaker", "Lab A · mobility analogy, 2 nodes");
  if (!b) return;
  const st = { link: "soft", air: false, view: "u" };
  const mk = (key, opts) => { const seg = h("div", { class: "seg" }); for (const [k, l] of opts) seg.append(h("button", { type: "button", class: st[key] === k ? "on" : "", onclick: (e) => { st[key] = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l)); b.ctl.append(seg); };
  mk("link", [["stiff", "stiff link (rod)"], ["soft", "soft link C_md = 3 µm/N"]]);
  mk("air", [[false, "in vacuum (part 1)"], [true, "with air load (part 3)"]]);
  mk("view", [["u", "velocities"], ["z", "|Z_M| = F/u_vc"], ["p", "pressures (part 3b)"]]);
  const ro = readouts(b.ctl, [{ id: "f1", label: "first resonance", dom: "me" }, { id: "u1", label: "u_vc there" }, { id: "dip", label: "coil dip (absorber)", dom: "me" }, { id: "f2", label: "second resonance", dom: "me" }, { id: "zmin", label: "|Z_M| floor" }, { id: "hf", label: "Z_M at 10 kHz" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 10, xmax: 10000, ymin: -70, ymax: 10, ylabel: "velocity (dB re 1 m/s per N)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fs = logspace(10, 10000, 500);
  function upd() {
    const link = P1[st.link], rows = fs.map(f => ({ f, r: dualDiaphragm(f, link, st.air) }));
    // features
    const uvc = rows.map(x => cabs(x.r.uvc)), ud = rows.map(x => cabs(x.r.ud));
    const i1 = uvc.indexOf(Math.max(...uvc.slice(0, 200)));
    let idip = -1, i2 = -1;
    if (st.link === "soft") { const seg = uvc.slice(200); idip = 200 + seg.indexOf(Math.min(...seg.slice(0, 200))); const seg2 = uvc.slice(idip); i2 = idip + seg2.indexOf(Math.max(...seg2)); }
    const z10k = rows[rows.length - 1].r.ZM;
    ro({ f1: hz(fs[i1]), u1: `${uvc[i1].toFixed(3)} m/s per N`, dip: idip > 0 ? `${hz(fs[idip])} · |Z| = ${cabs(rows[idip].r.ZM).toFixed(0)} Ns/m` : "— (one body)", f2: i2 > 0 ? hz(fs[i2]) : "—", zmin: `${cabs(rows[i1].r.ZM).toFixed(3)} Ns/m (= R_tot)`, hf: `${z10k.re.toFixed(1)} + j${z10k.im.toFixed(0)} Ns/m` });
    if (st.view === "u") plot.set({ ymin: -70, ymax: 10, ylabel: "velocity (dB re 1 m/s per N)", series: [{ name: "u_vc coil + inner cone", color: DOMC.me, pts: rows.map((x, i) => [x.f, dB(uvc[i])]) }, { name: "u_d outer cone", color: DOMC.ac, pts: rows.map((x, i) => [x.f, dB(ud[i])]) }], markers: [{ x: fs[i1], y: dB(uvc[i1]), label: `${hz(fs[i1])}`, color: DOMC.me }].concat(idip > 0 ? [{ x: fs[idip], y: dB(uvc[idip]), label: `dip ${hz(fs[idip])}`, color: DOMC.me, dy: 16 }, { x: fs[i2], y: dB(uvc[i2]), label: hz(fs[i2]), color: DOMC.me }] : []) });
    else if (st.view === "z") plot.set({ ymin: -10, ymax: 60, ylabel: "|Z_M| (dB re 1 Ns/m)", series: [{ name: "|Z_M| = 1/V(u_vc)", color: DOMC.me, pts: rows.map(x => [x.f, dB(cabs(x.r.ZM))]) }, { name: "mass line ω·11 g", color: DOMC.ink3, thin: true, pts: fs.map(f => [f, dB(TAU * f * 0.011)]) }, { name: "mass line ω·6 g", color: DOMC.ink3, thin: true, pts: fs.map(f => [f, dB(TAU * f * 0.006)]) }], markers: [{ x: fs[i1], y: dB(cabs(rows[i1].r.ZM)), label: `min ${cabs(rows[i1].r.ZM).toFixed(2)}`, color: DOMC.me, dy: 16 }].concat(idip > 0 ? [{ x: fs[idip], y: dB(cabs(rows[idip].r.ZM)), label: `max ${cabs(rows[idip].r.ZM).toFixed(0)}`, color: DOMC.me }] : []) });
    else plot.set({ ymin: -40, ymax: 40, ylabel: "pressure (dB re 1 Pa per N)", series: st.air ? [{ name: "in front of inner cone", color: DOMC.me, pts: rows.map(x => [x.f, dB(cabs(x.r.pfi))]) }, { name: "in front of outer cone", color: DOMC.ac, pts: rows.map(x => [x.f, dB(cabs(x.r.pfo))]) }, { name: "far field, 1 m on axis, half space", color: DOMC.el, pts: rows.map(x => [x.f, dB(cabs(x.r.far))]) }] : [{ name: "far field, 1 m (no air load on the cones)", color: DOMC.el, pts: rows.map(x => [x.f, dB(cabs(x.r.far))]) }], markers: [] });
    b.note.innerHTML = st.link === "stiff"
      ? `<p><b>Stiff link:</b> the 6 g coil and the 5 g cone are one 11 g body on the two suspensions in parallel (stiffnesses add: C_tot = 0.878 mm/N). One resonance, ${hz(fs[i1])}${st.air ? " (down from 51.3 Hz: the air adds 0.5 g + 3.4 g of co-moving mass)" : ""}; below it the springs rule, above it the mass. The impedance floor at resonance is the total damping, 0.72 Ns/m.</p>`
      : `<p><b>Soft link:</b> up to ~300 Hz nothing changes. Around ${idip > 0 ? hz(fs[idip]) : "1.3 kHz"} the outer cone on its soft spring is a <b>tuned absorber</b>: its reaction force cancels the drive and the coil almost stops (the dip), while |Z_M| shows a wall. Just above, the two masses swing in anti-phase (second resonance). Above that the soft link cannot transmit force: the big cone drops out 12 dB/oct faster and the light inner cone alone carries the treble — a <b>mechanical crossover</b>.${st.air ? " With air the absorber sits lower (the outer cone weighs 8.4 g with its air) and 17 Ns/m of radiation resistance damps it: the dip is shallower, the wall lower (334 → 129 Ns/m)." : ""}</p>`;
  }
  upd();
}

/* ===== Part 2: car silencer ladder, impedance analogy ===== */
function silencer(f, opts) {
  const a = 2e-3, S = Math.PI * a * a, R = 25e3;
  const tube = (l) => cadd(ZR(R), ZL(f, RHO * l / S));
  const Y = (V) => cx(0, TAU * f * V / (RHO * C0 * C0));
  const l7 = opts.rad ? 38.77e-3 : 40e-3, Zrad = opts.rad ? tubeEndZ(f, a) : cx(0, 0);
  // walk the ladder backwards from U7 = 1
  const U7 = cx(1, 0);
  const pout = cmul(U7, Zrad);
  const p6 = cadd(pout, cmul(U7, tube(l7)));
  const U5 = cadd(U7, cmul(p6, Y(42.4e-6)));
  const p4 = cadd(p6, cmul(U5, tube(100e-3)));
  const U3 = cadd(U5, cmul(p4, Y(100.5e-6)));
  const p2 = cadd(p4, cmul(U3, tube(80e-3)));
  const U1 = cadd(U3, cmul(p2, Y(15.7e-6)));
  const pin = cadd(p2, cmul(U1, tube(25e-3)));
  return { Uin: U1, pin, Zin: cdiv(pin, U1), U3: cdiv(U3, U1), U5: cdiv(U5, U1), U7: cdiv(U7, U1), pout: cdiv(pout, U1) };
}
function benchLab2() {
  const b = bench("bench-lab2", "Part 2 · the car silencer: four pipes, three chambers", "Lab A · impedance analogy, ladder");
  if (!b) return;
  const st = { src: "U", view: "out", rad: false };
  const mk = (key, opts) => { const seg = h("div", { class: "seg" }); for (const [k, l] of opts) seg.append(h("button", { type: "button", class: st[key] === k ? "on" : "", onclick: (e) => { st[key] = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l)); b.ctl.append(seg); };
  mk("src", [["p", "pressure source (2a)"], ["U", "volume-velocity source (2b)"]]);
  mk("view", [["out", "U_out"], ["pipes", "U in each pipe (2c)"], ["zin", "Z_in"], ["pout", "p at the opening (2d)"], ["spl", "SPL at 10 m (2e)"]]);
  mk("rad", [[false, "ideal open end"], [true, "with tube-end radiation"]]);
  const ro = readouts(b.ctl, [{ id: "pk", label: "peaks", dom: "ac" }, { id: "hf", label: "at 1 kHz" }, { id: "lim", label: "lumped valid below" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 10, xmax: 1000, ymin: -130, ymax: 30, ylabel: "|U_out / U_in| (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fs = logspace(10, 1000, 3000);
  const peaksOf = (arr) => { const out = []; for (let i = 2; i < arr.length - 2; i++) if (arr[i] > arr[i - 1] && arr[i] > arr[i + 1] && arr[i] > arr[i - 2] && arr[i] > arr[i + 2]) out.push(i); return out; };
  function upd() {
    const rows = fs.map(f => ({ f, r: silencer(f, { rad: st.rad }) }));
    const pS = st.src === "p";
    const Uout = rows.map(x => pS ? cabs(cdiv(x.r.U7, x.r.Zin)) : cabs(x.r.U7)); // per Pa or per m³/s
    const pk = peaksOf(Uout.map(dB)).slice(0, 4);
    let series = [], markers = [], y = {};
    if (st.view === "out") { y = pS ? { ymin: -270, ymax: -80, ylabel: "|U_out / p_in| (dB re 1 m³/s per Pa)" } : { ymin: -130, ymax: 50, ylabel: "|U_out / U_in| (dB)" }; series = [{ name: pS ? "U_out for p_in = 1 Pa" : "U_out for U_in = 1 m³/s", color: DOMC.ac, pts: rows.map((x, i) => [x.f, dB(Uout[i])]) }]; markers = pk.map(i => ({ x: fs[i], y: dB(Uout[i]), label: hz(fs[i]), color: DOMC.ac })); }
    else if (st.view === "pipes") { const g = (k) => rows.map(x => [x.f, dB(pS ? cabs(cdiv(x.r[k], x.r.Zin)) : cabs(x.r[k]))]); y = pS ? { ymin: -270, ymax: -80, ylabel: "|U_pipe / p_in| (dB)" } : { ymin: -130, ymax: 50, ylabel: "|U_pipe / U_in| (dB)" }; series = [{ name: "pipe 1 (= source)", color: DOMC.ink3, pts: rows.map(x => [x.f, dB(pS ? 1 / cabs(x.r.Zin) : 1)]) }, { name: "pipe 3", color: DOMC.el, pts: g("U3") }, { name: "pipe 5", color: DOMC.me, pts: g("U5") }, { name: "pipe 7", color: DOMC.ac, pts: g("U7") }]; }
    else if (st.view === "zin") { y = { ymin: 100, ymax: 200, ylabel: "|Z_in| (dB re 1 Pa·s/m³)" }; series = [{ name: "input impedance of the ladder", color: DOMC.ac, pts: rows.map(x => [x.f, dB(cabs(x.r.Zin))]) }]; }
    else if (st.view === "pout") { const pp = rows.map(x => pS ? cabs(cdiv(x.r.pout, x.r.Zin)) : cabs(x.r.pout)); y = { ymin: -60, ymax: 120, ylabel: pS ? "|p_open / p_in| (dB)" : "|p_open| (dB re 1 Pa, U_in = 1 m³/s)" }; series = [{ name: st.rad ? "pressure at the opening = Z_rad · U_out" : "ideal open end: p_open = 0 (switch the radiation on)", color: DOMC.ac, pts: rows.map((x, i) => [x.f, st.rad ? dB(pp[i]) : -200]) }]; if (st.rad) series.push({ name: "check: ω·M_A1·|U_out|", color: DOMC.ink3, thin: true, pts: rows.map((x, i) => [x.f, dB(TAU * x.f * 115.2 * Uout[i])]) }); }
    else { const spl = rows.map((x, i) => dB(RHO * x.f * Uout[i] / (2 * 10) / 20e-6)); y = { ymin: 0, ymax: 140, ylabel: "SPL at 10 m (dB re 20 µPa, U_in = 1 m³/s)" }; series = [{ name: "with silencer", color: DOMC.ac, pts: rows.map((x, i) => [x.f, spl[i]]) }, { name: "bare pipe (U_out = U_in)", color: DOMC.ink3, thin: true, pts: rows.map(x => [x.f, dB(RHO * x.f * (pS ? 1 / cabs(x.r.Zin) : 1) / 20 / 20e-6)]) }]; }
    plot.set(Object.assign({ series, markers, regions: [{ from: 344, to: 1000, color: DOMC.warn, label: "pipe 5 > λ/10" }] }, y));
    ro({ pk: pk.map(i => hz(fs[i])).join(" · ") || "—", hf: st.view === "spl" ? `${dB(RHO * 1000 * Uout[Uout.length - 1] / 20 / 20e-6).toFixed(1)} dB SPL` : `${dB(Uout[Uout.length - 1]).toFixed(1)} dB`, lim: "344 Hz (100 mm pipe)" });
    b.note.innerHTML = pS
      ? `<p><b>Pressure source:</b> the inlet is held at 1 Pa, so the ladder's natural frequencies are those of a <b>short-circuited</b> inlet — the peaks sit at the <b>minima of Z_in</b> (77, 180, 356 Hz; −98.8, −112.1, −141.6 dB). Below them the output is set by the input impedance, which already at 10 Hz is the series air masses, not the 25 kPa·s/m³ losses. Above the last peak each chamber section adds −18 dB/oct.</p>`
      : `<p><b>Volume-velocity source:</b> the flow is forced in whatever pressure it takes. At low frequency the chambers cannot store flow, so U_out = U_in (0 dB). The inlet is an <b>open circuit</b>, so the peaks sit at the <b>maxima of Z_in</b> (47, 176 and 191 Hz), exactly where the pressure-source response had its dips — and there the silencer <i>amplifies</i> by about +40 dB, limited only by the pipe losses. A real exhaust sits between the two ideal sources; that is why silencer design has to know the source impedance.</p>` + `<p class="muted"><b>Do not put a leak resistor across the flow source:</b> at those peaks |Z_in| is 0.3–1.5 GΩ, and a 100 MΩ “DC leak” steals most of the flow (it cost 13 dB in the first ngspice run). Sweep with 2000 points per decade; the peaks have Q &gt; 100. Every chamber capacitor is grounded. The tube-end radiation of a 2 mm pipe is a pure mass here (ka = 0.037 at 1 kHz), so p_open ≈ jωM_A1·U_out; the 40 mm effective length already contains the end correction, so pipe 7 is shortened to 38.77 mm when the network is on. Above ~350 Hz the 100 mm pipe is no longer small against λ/10: the steep roll-off is not to be trusted there.</p>`;
  }
  upd();
}

/* ===== Part 4: coil driving two masses, electrical + mechanical ===== */
const P4 = { Rc: 0.5, Le: 10e-6, Bl: 1.5, Mmc: 5e-3, Cms: 1e-5, Rms: 1, Mm1: 0.1, Cms2: 1e-2, Rms2: 0.1 };
function coilSystem(f, emfSign) {
  const Ze = cadd(ZR(P4.Rc), ZL(f, P4.Le));
  const Yms = cadd(ZC(f, P4.Cms), ZR(P4.Rms));
  const Y1 = cadd(cadd(cadd(ZL(f, P4.Mm1), ZC(f, P4.Cms2)), ZR(P4.Rms2)), Yms);
  // unknowns [i, u_c, u_1]; v = 1
  const A = [
    [Ze, cx(emfSign * P4.Bl, 0), cx(0, 0)],
    [cx(-P4.Bl, 0), cadd(ZL(f, P4.Mmc), Yms), cscale(Yms, -1)],
    [cx(0, 0), cscale(Yms, -1), Y1],
  ];
  const [i, uc, u1] = csolve(A, [cx(1, 0), cx(0, 0), cx(0, 0)]);
  return { i, uc, u1, ZE: cinv(i), ZM: cdiv(cscale(i, P4.Bl), uc) };
}
function benchLab4() {
  const b = bench("bench-lab4", "Part 4 · a coil, two masses, and the sign of the back-EMF", "Lab A · electrical ↔ mechanical");
  if (!b) return;
  const st = { emf: 1, view: "u" };
  const mk = (key, opts) => { const seg = h("div", { class: "seg" }); for (const [k, l] of opts) seg.append(h("button", { type: "button", class: st[key] === k ? "on" : "", onclick: (e) => { st[key] = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l)); b.ctl.append(seg); };
  mk("view", [["u", "velocities"], ["zm", "Z_M = Bl·i / u_c"], ["ze", "Z_E = v / i"]]);
  mk("emf", [[1, "back-EMF correct (+Bl·u)"], [0, "no back-EMF"], [-1, "sign flipped (−Bl·u)"]]);
  const ro = readouts(b.ctl, [{ id: "f1", label: "rigid-body mode", dom: "me" }, { id: "u1", label: "u_c there" }, { id: "fa", label: "coil stops (anti-res.)", dom: "me" }, { id: "f2", label: "coil-on-spring mode", dom: "me" }, { id: "ze1", label: "Z_E peak", dom: "el" }, { id: "ed", label: "electrical damping (Bl)²/R_c" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 1, xmax: 10000, ymin: -90, ymax: 40, ylabel: "velocity (dB re 1 m/s per V)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fs = logspace(1, 10000, 600);
  function upd() {
    const rows = fs.map(f => ({ f, r: coilSystem(f, st.emf) }));
    const uc = rows.map(x => cabs(x.r.uc)), u1 = rows.map(x => cabs(x.r.u1));
    const i1 = uc.slice(0, 250).indexOf(Math.max(...uc.slice(0, 250)));
    const mid = uc.slice(250, 450), ia = 250 + mid.indexOf(Math.min(...mid));
    const hi = uc.slice(ia), i2 = ia + hi.indexOf(Math.max(...hi));
    const ze = rows.map(x => cabs(x.r.ZE));
    ro({ f1: hz(fs[i1]), u1: `${uc[i1].toFixed(3)} m/s per V`, fa: `${hz(fs[ia])} · u_c = ${sci(uc[ia], 2)}`, f2: hz(fs[i2]), ze1: `${ze[i1].toFixed(1)} Ω at ${hz(fs[i1])}`, ed: st.emf === 1 ? "4.5 Ns/m" : st.emf === 0 ? "0 (removed)" : "−4.5 Ns/m (negative!)" });
    if (st.view === "u") plot.set({ ymin: -90, ymax: 40, ylabel: "velocity (dB re 1 m/s per V)", series: [{ name: "u_c coil", color: DOMC.me, pts: rows.map((x, i) => [x.f, dB(uc[i])]) }, { name: "u_1 the 100 g mass", color: DOMC.ac, pts: rows.map((x, i) => [x.f, dB(u1[i])]) }], markers: [{ x: fs[i1], y: dB(uc[i1]), label: `${hz(fs[i1])} · ${uc[i1].toFixed(2)}`, color: DOMC.me }, { x: fs[ia], y: dB(uc[ia]), label: `coil stops ${hz(fs[ia])}`, color: DOMC.me, dy: 16 }, { x: fs[i2], y: dB(uc[i2]), label: hz(fs[i2]), color: DOMC.me }] });
    else if (st.view === "zm") plot.set({ ymin: -30, ymax: 90, ylabel: "|Z_M| (dB re 1 Ns/m)", series: [{ name: "mechanical impedance seen by the Lorentz force", color: DOMC.me, pts: rows.map(x => [x.f, dB(cabs(x.r.ZM))]) }], markers: [{ x: fs[i1], y: dB(cabs(rows[i1].r.ZM)), label: `min ≈ R_ms2`, color: DOMC.me, dy: 16 }, { x: fs[ia], y: dB(cabs(rows[ia].r.ZM)), label: `max ${sci(cabs(rows[ia].r.ZM), 2)}`, color: DOMC.me }, { x: fs[i2], y: dB(cabs(rows[i2].r.ZM)), label: `min ≈ R_ms`, color: DOMC.me, dy: 16 }] });
    else plot.set({ ymin: -10, ymax: 35, ylabel: "|Z_E| (dB re 1 Ω)", series: [{ name: "electrical impedance at the terminals", color: DOMC.el, pts: rows.map((x, i) => [x.f, dB(ze[i])]) }, { name: "blocked coil R_c + jωL_e", color: DOMC.ink3, thin: true, pts: fs.map(f => [f, dB(cabs(cadd(ZR(P4.Rc), ZL(f, P4.Le))))]) }], markers: [{ x: fs[i1], y: dB(ze[i1]), label: `${ze[i1].toFixed(1)} Ω`, color: DOMC.el }, { x: fs[i2], y: dB(ze[i2]), label: `${ze[i2].toFixed(2)} Ω`, color: DOMC.el }] });
    b.note.innerHTML = (st.emf === 1
      ? `<p><b>Correct sign.</b> Three things happen: at ${hz(fs[i1])} both masses ride together on the soft C_ms2 (rigid-body mode) — broad, because the electrical damping (Bl)²/R_c = 4.5 Ns/m dominates and holds the peak to 0.65 m/s per V. At ${hz(fs[ia])} the 100 g mass resonates on the stiff C_ms and swallows all the force: the coil <b>stops</b> (tuned-mass-damper) and Z_E collapses to the blocked R_c. At ${hz(fs[i2])} the 5 g coil bounces on C_ms against the now-stationary mass.</p>`
      : st.emf === 0 ? `<p><b>No back-EMF:</b> the 5 Hz mode is damped only by R_ms2 and the peak shoots up to ~30 m/s per V, the current at resonance is 2 A instead of 44 mA, and Z_E is a flat R_c. Physically wrong — the coil always induces a voltage when it moves.</p>`
      : `<p><b>Flipped sign = negative damping.</b> The 5 Hz peak barely moves but the 724 Hz mode grows from 0.54 to 0.89 m/s per V and Z_E loses its low peak: the "back"-EMF now feeds energy in. This is what the brief means by "pay attention to the signs of the dependent generators", and it is the first thing to check when a coupled circuit misbehaves: the low resonance must be <i>small</i>.</p>`)
      + `<p class="muted">Z_M contains no electrical damping (the transducer is lossless; the back-EMF acts on the electrical side). Z_E = R_c + jωL_e + (Bl)²/Z_M: every minimum of Z_M is a maximum of Z_E, scaled by (Bl)² = 2.25 — the impedance conversion of lecture 4, live.</p>`;
  }
  upd();
}


// ---------------------------------------------------------------- Lab B: scattering by the microphone mock-up (course BEM data)
const LABB_OBJ = { mock: ["mock-up 250 mm", 0.250], "1": ["1 inch", 0.02377], "2": ["1/2 inch", 0.0127], "4": ["1/4 inch", 0.00635], "8": ["1/8 inch", 0.003175] };
function benchLabB() {
  const b = bench("bench-labB", "The mock-up in a plane wave: pick the angle, then shrink it to a real microphone", "Lab B · course BEM model · D = 250 mm, L = 855 mm · measured 22 Sep 2026");
  if (!b || !window.LABB) return;
  const D = window.LABB, M = window.LABB_MEAS, st = { obj: "mock", q: "centre", src: "both", on: new Set([0, 45, 90]) };
  const mk = (key, opts) => { const seg = h("div", { class: "seg" }); for (const [k, l] of opts) seg.append(h("button", { type: "button", class: st[key] === k ? "on" : "", onclick: (e) => { st[key] = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l)); b.ctl.append(seg); };
  mk("obj", Object.entries(LABB_OBJ).map(([k, v]) => [k, v[0]]));
  mk("q", [["centre", "centre of the face"], ["avg", "averaged over the face"], ["fp", "3 cm in front"], ["flat", "centre, flat back end"]]);
  if (M) mk("src", [["bem", "BEM only"], ["both", "BEM + measured 22 Sep"], ["meas", "measured only"]]);
  const chips = h("div", { class: "chips" });
  for (const a of D.ang) chips.append(h("button", { type: "button", class: "chip" + (st.on.has(a) ? " on" : ""), onclick: (e) => { st.on.has(a) ? st.on.delete(a) : st.on.add(a); e.target.classList.toggle("on"); upd(); } }, a + "°"));
  b.ctl.append(chips);
  const ro = readouts(b.ctl, [{ id: "s", label: "scale factor" }, { id: "k1", label: "ka = 1 at", dom: "ac" }, { id: "pk", label: "0° maximum, BEM", dom: "ac" }, { id: "mk", label: "0° maximum, measured", dom: "ac" }, { id: "nt", label: "0° notch, measured" }]);
  const plot = new Plot(b.plot, { h: 330, xmin: 50, xmax: 5400, ymin: -12, ymax: 12, ylabel: "pressure re the undisturbed wave (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const cols = ["#3b82d6", "#6aa5e8", "#1fa88a", "#5cc4a9", "#a3a844", "#d9822b", "#d9503f", "#a565c9", "#8a8a8a", "#b0a090"];
  function upd() {
    const s = 0.250 / LABB_OBJ[st.obj][1], fx = D.f.map(f => f * s), c = 343.4, a = LABB_OBJ[st.obj][1] / 2;
    const showB = st.src !== "meas", showM = !!M && st.src !== "bem";
    const y0 = D[st.q][0], ip = y0.indexOf(Math.max(...y0));
    let mpk = "—", mnt = "—", mx = null;
    if (M) {
      const m0 = M.dB[0], lo = M.f.map((f, k) => f > 200 && f < 2000 ? m0[k] : -99), im = lo.indexOf(Math.max(...lo));
      const nt = M.f.map((f, k) => f > 3000 && f < 4500 ? m0[k] : 99), inn = nt.indexOf(Math.min(...nt));
      mpk = `+${m0[im].toFixed(1)} dB at ${hz(M.f[im] * s)}`; mnt = `${m0[inn].toFixed(1)} dB at ${hz(M.f[inn] * s)}`;
      mx = showM && st.on.has(0) ? { x: M.f[im] * s, y: m0[im], label: `${m0[im].toFixed(1)} dB measured`, color: cols[0] } : null;
    }
    ro({ s: st.obj === "mock" ? "1 (as measured)" : `× ${s.toFixed(1)} in frequency`, k1: hz(c / (2 * Math.PI * a)), pk: `${y0[ip] >= 0 ? "+" : ""}${y0[ip].toFixed(1)} dB at ${hz(fx[ip])}`, mk: mpk, nt: mnt });
    const series = [];
    if (showB) for (const [i, ang] of D.ang.entries()) if (st.on.has(ang)) series.push({ name: ang + "° BEM", color: cols[i], thin: showM, pts: fx.map((f, k) => [f, D[st.q][i][k]]) });
    if (showM) for (const [i, ang] of M.ang.entries()) if (st.on.has(ang)) series.push({ name: ang + "° measured", color: cols[D.ang.indexOf(ang)], width: 2.2, pts: M.f.map((f, k) => [f * s, M.dB[i][k]]) });
    const markers = []; if (showB && st.on.has(0)) markers.push({ x: fx[ip], y: y0[ip], label: `${y0[ip].toFixed(1)} dB BEM`, color: cols[0] }); if (mx) markers.push(mx);
    plot.set({ xmin: 50 * s, xmax: (showM ? 10000 : 5400) * s, ymin: showM || st.q === "fp" ? -25 : -12, ymax: 12, series, vlines: [{ x: c / (2 * Math.PI * a), label: "ka = 1", color: DOMC.ink3 }], markers });
    b.note.innerHTML = ({
      centre: `<p><b>The point the lab intends to measure.</b> Below ka ≈ 0.3 the body is invisible: 0 dB at every angle. Head-on the pressure climbs past the +6 dB of an infinite wall to <b>+9.9 dB at ka ≈ 3</b>, because the waves diffracted at the rim all reach the centre in phase, then it ripples. At 90° the face does not block the wave and the curve stays within about 2 dB. From behind (180°) there is still +2 dB: the bright spot on the axis of the shadow.</p>`,
      avg: `<p><b>What a real diaphragm feels</b>: the pressure averaged over the face with a parabolic weight. Same story, but lower at high ka (+6.2 instead of +9.9 dB at 4 kHz, 0°), because the pressure is not uniform across the face once the wavelength is comparable to it. This is one reason the datasheet corrections sit a little below our centre-point measurement.</p>`,
      fp: `<p><b>3 cm in front of the face.</b> The rigid face makes a standing wave in front of itself; where the distance is λ/4 the incident and reflected waves cancel: a notch of more than 20 dB near 4 kHz at 0° (λ/4 = 2.1 cm, the diffraction pulls it a little). <b>This is the curve we measured on 22 Sep</b>: the UMIK tip sat 2–3 cm in front of the face, and with the measured curves on, the two 0° lines lie on top of each other from 100 Hz to 5 kHz.</p>`,
      flat: `<p><b>Flat instead of round back end.</b> At 0° the difference is below 0.25 dB: the front face decides. The back only matters when the sound comes from behind.</p>` })[st.q]
      + (showM ? `<p><b>Measured 22 Sep 2026</b> (Group 10, UMIK 708-0332 at 2.8 m, seven angles 0–90°, normalised by the no-mock-up run at the same position). Up to 2 kHz within about 1 dB of the face-centre BEM at every angle; above that the tip gap takes over: the 0° maximum is +8.6 dB at 1.16 kHz instead of +9.9 at 1.35 kHz and there is a −18 dB notch at 3.9 kHz. The oblique BEM curves are not reliable above ≈ 4 kHz (8 circumferential terms), so compare the notch <i>positions</i> there, not their depths.</p>` : "")
      + (st.obj === "mock" ? "" : `<p class="muted">Scaled to a ${LABB_OBJ[st.obj][0]} microphone (D = ${(LABB_OBJ[st.obj][1] * 1000).toFixed(2)} mm): same shape, every frequency × ${s.toFixed(1)}. Compare with the B&K free-field corrections in the brief: the 1 inch type 4145 peaks at about +10 dB near 13 kHz; our measured 0° maximum lands at ${hz(1155 * s)}.</p>`)
      + `<p class="muted">BEM with 8 circumferential terms: the last few points of the oblique curves (above ≈ 4 kHz on the mock-up) are not reliable.</p>`;
  }
  upd();
}


// ---------------------------------------------------------------- Lab C: actuator response of a condenser capsule -> backplate mass and resistance
const LABC = { a: 8.95e-3 / 2, x0: 20.77e-6, E: 200, MMD: 1.5e-6, CMD: 0.02e-3, V: 126.4e-9 };
function labCmodel(fs, Q) {
  const SD = Math.PI * LABC.a * LABC.a, CAB = LABC.V / (1.18 * 344 * 344), MA1 = 0.6133 * 1.18 / (Math.PI * LABC.a);
  const CMT = 1 / (1 / LABC.CMD + SD * SD / CAB), MMT = 1 / (Math.pow(2 * Math.PI * fs, 2) * CMT);
  return { SD, CAB, MA1, CMT, MMT, MAS: (MMT - LABC.MMD) / (SD * SD) - MA1, RAS: Math.sqrt(MMT / CMT) / Q / (SD * SD), M: LABC.E * SD * CMT / LABC.x0,
           f0bare: 1 / (2 * Math.PI * Math.sqrt((LABC.MMD + SD * SD * MA1) * CMT)) };
}
function benchLabC() {
  const b = bench("bench-labC", "Read f_s and Q off the actuator response, get the backplate for LTspice", "Lab C · B&K 4133 / 4134 · data from the brief");
  if (!b) return;
  const st = { fs: 20000, Q: 0.45, view: "mag" };
  const seg = h("div", { class: "seg" });
  for (const [k, l] of [["mag", "magnitude"], ["ph", "phase"]]) seg.append(h("button", { type: "button", class: st.view === k ? "on" : "", onclick: (e) => { st.view = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  slider(b.ctl, { label: "resonance <b>f<sub>s</sub></b> (phase −90°)", min: 8000, max: 28000, step: 100, value: st.fs, unit: "Hz", dom: "me", onchange: v => { st.fs = v; upd(); } });
  slider(b.ctl, { label: "quality factor <b>Q</b> = |H(f<sub>s</sub>)|/|H(low)|", min: 0.2, max: 2, step: 0.01, value: st.Q, unit: "", dom: "ac", onchange: v => { st.Q = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "lq", label: "20 log Q (level at f_s)" }, { id: "f3", label: "−3 dB at" }, { id: "mmt", label: "total moving mass M_MT", dom: "me" }, { id: "mas", label: "backplate mass M_AS", dom: "ac" }, { id: "ras", label: "backplate resistance R_AS", dom: "ac" }, { id: "typ", label: "looks like" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 20, xmax: 60000, ymin: -25, ymax: 10, ylabel: "response re low frequency (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fr = logspace(20, 60000, 500);
  const H = (f, fs, Q) => cinv(cx(1 - (f / fs) * (f / fs), f / fs / Q));
  function upd() {
    const m = labCmodel(st.fs, st.Q), mag = fr.map(f => dB(cabs(H(f, st.fs, st.Q)))), ph = fr.map(f => carg(H(f, st.fs, st.Q)) * 180 / Math.PI);
    const i3 = mag.findIndex(v => v < -3);
    ro({ lq: `${(20 * Math.log10(st.Q)).toFixed(1)} dB`, f3: i3 > 0 ? hz(fr[i3]) : "above 60 kHz", mmt: `${(m.MMT * 1e6).toFixed(2)} mg (diaphragm 1.5 mg)`, mas: m.MAS > 0 ? `${m.MAS.toFixed(0)} kg/m⁴` : "negative: f_s too high for this diaphragm", ras: `${sci(m.RAS, 3)} Pa·s/m³`, typ: st.Q < 0.6 ? "free-field type (droops early)" : st.Q <= 1.1 ? "pressure type (flat)" : "under-damped (peak)" });
    if (st.view === "mag") plot.set({ ymin: -25, ymax: 10, ylabel: "response re low frequency (dB)", yunit: " dB", series: [{ name: "this capsule", color: DOMC.ac, pts: fr.map((f, i) => [f, mag[i]]) }, { name: "free-field-like, Q = 0.45", color: DOMC.ink3, thin: true, pts: fr.map(f => [f, dB(cabs(H(f, 20000, 0.45)))]) }, { name: "pressure-like, Q = 0.95", color: DOMC.ink3, thin: true, pts: fr.map(f => [f, dB(cabs(H(f, 20000, 0.95)))]) }], vlines: [{ x: st.fs, label: "f_s", color: DOMC.me }], markers: [{ x: st.fs, y: 20 * Math.log10(st.Q), label: `Q = ${st.Q.toFixed(2)}`, color: DOMC.ac }] });
    else plot.set({ ymin: -190, ymax: 10, ylabel: "phase re low frequency (degrees)", yunit: "°", series: [{ name: "this capsule", color: DOMC.me, pts: fr.map((f, i) => [f, ph[i]]) }], vlines: [{ x: st.fs, label: "f_s", color: DOMC.me }], markers: [{ x: st.fs, y: -90, label: "−90°", color: DOMC.me }] });
    b.note.innerHTML = `<p>The actuator pulls on the diaphragm with an electric field, so this is the <b>pressure response</b>: a second-order low-pass <span class="mono">1/(1 − x² + jx/Q)</span>, <span class="mono">x = f/f_s</span>. Two numbers describe it. With the brief's data (S<sub>D</sub> = 62.9 mm², C<sub>MT</sub> = 18.4 µm/N, the back cavity stiffens the diaphragm by 9 %) they turn into the two unknowns of the LTspice model: <b>M<sub>MT</sub> = 1/((2πf<sub>s</sub>)²C<sub>MT</sub>)</b>, then M<sub>AS</sub> = (M<sub>MT</sub> − M<sub>MD</sub>)/S<sub>D</sub>² − M<sub>A1</sub> and R<sub>AS</sub> = √(M<sub>MT</sub>/C<sub>MT</sub>)/(Q·S<sub>D</sub>²).</p>`
      + `<p class="muted">Without any backplate mass this diaphragm would resonate at ${hz(m.f0bare)}; a measured f_s near 20 kHz means the air in the backplate holes about doubles the moving mass. Model sensitivity E·S<sub>D</sub>·C<sub>MT</sub>/x<sub>0</sub> = ${(m.M * 1e3).toFixed(1)} mV/Pa (nominal 12.5: the brief's appendix says to accept that).</p>`;
  }
  upd();
}

document.addEventListener("DOMContentLoaded", () => { benchLab1(); benchLab2(); benchLab4(); benchLabB(); benchLabC(); });
