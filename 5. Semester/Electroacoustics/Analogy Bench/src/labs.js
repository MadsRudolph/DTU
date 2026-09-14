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
  const fs = logspace(10, 1000, 500);
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
      ? `<p><b>Pressure source:</b> the inlet is held at 1 Pa, so the ladder's natural frequencies are those of a <b>short-circuited</b> inlet — the peaks sit at the <b>minima of Z_in</b> (77, 180, 355 Hz). Below them the output is set by the input impedance, which already at 10 Hz is the series air masses, not the 25 kPa·s/m³ losses. Above the last peak each chamber section adds −18 dB/oct.</p>`
      : `<p><b>Volume-velocity source:</b> the flow is forced in whatever pressure it takes. At low frequency the chambers cannot store flow, so U_out = U_in (0 dB). The inlet is an <b>open circuit</b>, so the peaks sit at the <b>maxima of Z_in</b> (47 and 176 Hz), exactly where the pressure-source response had its dips — and there the silencer <i>amplifies</i> by +26 dB. A real exhaust sits between the two ideal sources; that is why silencer design has to know the source impedance.</p>` + `<p class="muted">Every chamber capacitor is grounded. The tube-end radiation of a 2 mm pipe is a pure mass here (ka = 0.037 at 1 kHz), so p_open ≈ jωM_A1·U_out; the 40 mm effective length already contains the end correction, so pipe 7 is shortened to 38.77 mm when the network is on. Above ~350 Hz the 100 mm pipe is no longer small against λ/10: the steep roll-off is not to be trusted there.</p>`;
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

document.addEventListener("DOMContentLoaded", () => { benchLab1(); benchLab2(); benchLab4(); });
