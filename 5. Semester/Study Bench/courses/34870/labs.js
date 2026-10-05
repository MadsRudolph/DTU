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
// the measured curve of one capsule, normalised to its 100-500 Hz level (shape only)
function labCshape(key) {
  const M = window.LABC_MEAS; if (!M) return null;
  const mag = M[key + "_dB"], ph = M[key + "_ph"], band = M.f.map((f, i) => f >= 100 && f <= 500 ? mag[i] : null).filter(v => v !== null);
  const ref = band.reduce((a, b) => a + b, 0) / band.length;
  return { mag: M.f.map((f, i) => [f, mag[i] - ref]), ph: M.f.map((f, i) => [f, ph[i]]) };
}
function benchLabC() {
  const b = bench("bench-labC", "Read f_s and Q off the actuator response, get the backplate for LTspice", "Lab C · B&K 4133 / 4134 · measured 29 Sep 2026");
  if (!b) return;
  const MS = window.LABC_MEAS;
  const st = { fs: MS ? MS.fs34 : 20000, Q: MS ? MS.Q34 : 0.84, view: "mag", ov: MS ? "m34" : "none" };
  const seg = h("div", { class: "seg" });
  for (const [k, l] of [["mag", "magnitude"], ["ph", "phase"]]) seg.append(h("button", { type: "button", class: st.view === k ? "on" : "", onclick: (e) => { st.view = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  let sFs, sQ;
  if (MS) {
    const seg2 = h("div", { class: "seg" });
    for (const [k, l] of [["m34", "our 4134 (Mic 1)"], ["m33", "our 4133 (Mic 2)"], ["none", "no data"]]) seg2.append(h("button", { type: "button", class: st.ov === k ? "on" : "", onclick: (e) => {
      st.ov = k; $$("button", seg2).forEach(x => x.classList.toggle("on", x === e.target));
      if (k !== "none") { st.fs = MS["fs" + k.slice(1)]; st.Q = MS["Q" + k.slice(1)]; sFs.set(st.fs); sQ.set(st.Q); }
      upd(); } }, l));
    b.ctl.append(seg2);
  }
  sFs = slider(b.ctl, { label: "resonance <b>f<sub>s</sub></b> (phase −90°)", min: 8000, max: 28000, step: 10, value: st.fs, unit: "Hz", dom: "me", fmt: v => v.toFixed(0), onchange: v => { st.fs = v; upd(); } });
  sQ = slider(b.ctl, { label: "quality factor <b>Q</b> = |H(f<sub>s</sub>)|/|H(low)|", min: 0.2, max: 2, step: 0.005, value: st.Q, unit: "", dom: "ac", fmt: v => v.toFixed(3), onchange: v => { st.Q = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "lq", label: "20 log Q (level at f_s)" }, { id: "f3", label: "−3 dB at" }, { id: "mmt", label: "total moving mass M_MT", dom: "me" }, { id: "mas", label: "backplate mass M_AS", dom: "ac" }, { id: "ras", label: "backplate resistance R_AS", dom: "ac" }, { id: "typ", label: "looks like" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 20, xmax: 45000, ymin: -25, ymax: 10, ylabel: "response re low frequency (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const fr = logspace(20, 45000, 500);
  const H = (f, fs, Q) => cinv(cx(1 - (f / fs) * (f / fs), f / fs / Q));
  function upd() {
    const m = labCmodel(st.fs, st.Q), mag = fr.map(f => dB(cabs(H(f, st.fs, st.Q)))), ph = fr.map(f => carg(H(f, st.fs, st.Q)));
    const i3 = mag.findIndex(v => v < -3), meas = st.ov !== "none" ? labCshape(st.ov) : null, mname = st.ov === "m34" ? "measured 4134" : "measured 4133";
    ro({ lq: `${(20 * Math.log10(st.Q)).toFixed(1)} dB`, f3: i3 > 0 ? hz(fr[i3]) : "above 45 kHz", mmt: `${(m.MMT * 1e6).toFixed(2)} mg (diaphragm 1.5 mg)`, mas: m.MAS > 0 ? `${m.MAS.toFixed(1)} kg/m⁴` : "negative: f_s too high for this diaphragm", ras: `${sci(m.RAS, 3)} Pa·s/m³`, typ: st.Q < 0.6 ? "free-field type (droops early)" : st.Q <= 1.1 ? "pressure type (flat)" : "under-damped (peak)" });
    if (st.view === "mag") {
      const series = [{ name: "second-order model", color: DOMC.ac, pts: fr.map((f, i) => [f, mag[i]]) }];
      if (meas) series.push({ name: mname, color: DOMC.el, width: 2.2, pts: meas.mag });
      else series.push({ name: "free-field-like, Q = 0.34", color: DOMC.ink3, thin: true, pts: fr.map(f => [f, dB(cabs(H(f, 22930, 0.34)))]) }, { name: "pressure-like, Q = 0.84", color: DOMC.ink3, thin: true, pts: fr.map(f => [f, dB(cabs(H(f, 20221, 0.84)))]) });
      plot.set({ ymin: -25, ymax: 10, ylabel: "response re low frequency (dB)", yunit: " dB", series, vlines: [{ x: st.fs, label: "f_s", color: DOMC.me }], markers: [{ x: st.fs, y: 20 * Math.log10(st.Q), label: `Q = ${st.Q.toFixed(2)}`, color: DOMC.ac }] });
    } else {
      const series = [{ name: "second-order model", color: DOMC.me, pts: fr.map((f, i) => [f, ph[i]]) }];
      if (meas) series.push({ name: mname, color: DOMC.el, width: 2.2, pts: meas.ph });
      plot.set({ ymin: -190, ymax: 10, ylabel: "phase (degrees)", yunit: "°", series, vlines: [{ x: st.fs, label: "f_s", color: DOMC.me }], markers: [{ x: st.fs, y: -90, label: "−90°", color: DOMC.me }] });
    }
    b.note.innerHTML = `<p>The actuator pulls on the diaphragm with an electric field, so this is the <b>pressure response</b>: a second-order low-pass <span class="mono">1/(1 − x² + jx/Q)</span>, <span class="mono">x = f/f_s</span>. Two numbers describe it. With the brief's data (S<sub>D</sub> = 62.9 mm², C<sub>MT</sub> = 18.4 µm/N, the back cavity stiffens the diaphragm by 9 %) they turn into the two unknowns of the LTspice model: <b>M<sub>MT</sub> = 1/((2πf<sub>s</sub>)²C<sub>MT</sub>)</b>, then M<sub>AS</sub> = (M<sub>MT</sub> − M<sub>MD</sub>)/S<sub>D</sub>² − M<sub>A1</sub> and R<sub>AS</sub> = √(M<sub>MT</sub>/C<sub>MT</sub>)/(Q·S<sub>D</sub>²).</p>`
      + (meas ? (st.ov === "m34"
        ? `<p><b>Our 4134</b> (Mic 1): f<sub>s</sub> = 20.2 kHz from the −90° crossing, Q = 0.84 from the level there. The model lies on the measurement within a few tenths of a dB up to 20 kHz. Try the whole-curve fit, 20.8 kHz and Q = 0.81: hardly any difference, a textbook second-order system.</p>`
        : `<p><b>Our 4133</b> (Mic 2): f<sub>s</sub> = 22.9 kHz, Q = 0.34. Up to 20 kHz this single mass–spring–damper follows the measured shape within 0.5 dB and 5°. Switch to <b>phase</b>: above resonance the measurement falls slowly between about 12 and 25 kHz and then faster than the model, up to 19° off. The whole-curve fit (21.1 kHz, Q = 0.39) matches the magnitude better and the −90° point worse. Its damping comes from an air film squeezed through a slotted backplate, and that resistance changes with frequency.</p>`) : "")
      + `<p class="muted">Without any backplate mass this diaphragm would resonate at ${hz(m.f0bare)}; a measured f_s near 20 kHz means the air moving in the backplate holes adds a lot of moving mass. Model sensitivity E·S<sub>D</sub>·C<sub>MT</sub>/x<sub>0</sub> = ${(m.M * 1e3).toFixed(2)} mV/Pa for both capsules (the brief's appendix: accept it).</p>`;
  }
  upd();
}

// ---------------------------------------------------------------- Lab C: the capsule element by element, in absolute units
function condCapsule(p, f) {
  // p: E [V], x0 [m], V [m^3] back volume, MAS [kg/m^4], RAS [Pa s/m^3]; diaphragm mass, compliance and radius from the brief
  const SD = Math.PI * LABC.a * LABC.a, CAB = p.V / (1.18 * 344 * 344), MA1 = 0.6133 * 1.18 / (Math.PI * LABC.a);
  const CMT = 1 / (1 / LABC.CMD + SD * SD / CAB), MMT = LABC.MMD + SD * SD * (MA1 + p.MAS), RMT = SD * SD * p.RAS;
  const M = p.E * SD * CMT / p.x0, w = 2 * Math.PI * f;
  return { SD, CAB, CMT, MMT, RMT, M, CE0: 8.854e-12 * SD / p.x0, fs: 1 / (2 * Math.PI * Math.sqrt(MMT * CMT)), Q: Math.sqrt(MMT / CMT) / RMT,
           H: cdiv(cx(M, 0), cx(1 - w * w * MMT * CMT, w * RMT * CMT)) };
}
function benchLabCcapsule() {
  const b = bench("bench-labCcap", "Build the capsule: polarisation, gap, back volume and backplate, against our two microphones", "Lab C · three-domain model in absolute units · dB re 1 V/Pa");
  if (!b) return;
  const MS = window.LABC_MEAS;
  const PRE = { m34: { E: 200, x0: 20.77, V: 126.4, MAS: 420.5, RAS: 1.294e8 }, m33: { E: 200, x0: 20.77, V: 126.4, MAS: 231.4, RAS: 2.803e8 } };
  const st = Object.assign({ view: "mag", show: "both" }, PRE.m34), sl = {};
  const seg = h("div", { class: "seg" });
  for (const [k, l] of [["m34", "our 4134 values"], ["m33", "our 4133 values"]]) seg.append(h("button", { type: "button", class: k === "m34" ? "on" : "", onclick: (e) => {
    Object.assign(st, PRE[k]); for (const key of Object.keys(sl)) sl[key].set(st[key]); $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  const seg2 = h("div", { class: "seg" });
  for (const [k, l] of [["mag", "magnitude"], ["ph", "phase"]]) seg2.append(h("button", { type: "button", class: st.view === k ? "on" : "", onclick: (e) => { st.view = k; $$("button", seg2).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg2);
  sl.E = slider(b.ctl, { label: "polarisation voltage <b>E</b>", min: 50, max: 300, step: 1, value: st.E, unit: "V", dom: "el", fmt: v => v.toFixed(0), onchange: v => { st.E = v; upd(); } });
  sl.x0 = slider(b.ctl, { label: "air gap <b>x<sub>0</sub></b>", min: 10, max: 40, step: 0.01, value: st.x0, unit: "µm", dom: "el", fmt: v => v.toFixed(2), onchange: v => { st.x0 = v; upd(); } });
  sl.V = slider(b.ctl, { label: "back volume <b>V<sub>B</sub></b>", min: 20, max: 1000, step: 1, log: true, value: st.V, unit: "mm³", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.V = v; upd(); } });
  sl.MAS = slider(b.ctl, { label: "backplate mass <b>M<sub>AS</sub></b>", min: 0, max: 1000, step: 0.5, value: st.MAS, unit: "kg/m⁴", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.MAS = v; upd(); } });
  sl.RAS = slider(b.ctl, { label: "backplate resistance <b>R<sub>AS</sub></b>", min: 2e7, max: 1e9, log: true, value: st.RAS, unit: "Pa·s/m³", dom: "ac", fmt: v => sci(v, 3), onchange: v => { st.RAS = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "M", label: "sensitivity E·S<sub>D</sub>·C<sub>MT</sub>/x<sub>0</sub>", dom: "el" }, { id: "cmt", label: "total compliance C<sub>MT</sub>", dom: "me" }, { id: "fs", label: "f<sub>s</sub>", dom: "me" }, { id: "Q", label: "Q", dom: "ac" }, { id: "ce", label: "rest capacitance C<sub>E0</sub>", dom: "el" }]);
  const plot = new Plot(b.plot, { h: 330, xmin: 20, xmax: 45000, ymin: -56, ymax: -32, ylabel: "sensitivity (dB re 1 V/Pa)", yfmt: v => v.toFixed(0), yunit: " dB" });
  const fr = logspace(20, 45000, 400);
  function upd() {
    const p = { E: st.E, x0: st.x0 * 1e-6, V: st.V * 1e-9, MAS: st.MAS, RAS: st.RAS };
    const pts = fr.map(f => condCapsule(p, f).H), m = condCapsule(p, 1000);
    ro({ M: `${(m.M * 1e3).toFixed(2)} mV/Pa = ${dB(m.M).toFixed(2)} dB`, cmt: `${(m.CMT * 1e6).toFixed(2)} µm/N`, fs: hz(m.fs), Q: m.Q.toFixed(3), ce: `${(m.CE0 * 1e12).toFixed(1)} pF` });
    const series = [], mag = st.view === "mag";
    series.push({ name: "model", color: DOMC.ink, width: 1.8, pts: fr.map((f, i) => [f, mag ? dB(cabs(pts[i])) : carg(pts[i])]) });
    if (MS) {
      series.push({ name: "measured 4134 (Mic 1)", color: DOMC.el, width: 2.2, pts: MS.f.map((f, i) => [f, mag ? MS.m34_dB[i] : MS.m34_ph[i]]) });
      series.push({ name: "measured 4133 (Mic 2)", color: DOMC.me, width: 2.2, pts: MS.f.map((f, i) => [f, mag ? MS.m33_dB[i] : MS.m33_ph[i]]) });
    }
    plot.set(mag ? { ymin: -56, ymax: -32, ylabel: "sensitivity (dB re 1 V/Pa)", yunit: " dB", yfmt: v => v.toFixed(0), series, vlines: [{ x: m.fs, label: "f_s", color: DOMC.me }], markers: [] }
                 : { ymin: -190, ymax: 15, ylabel: "phase (degrees)", yunit: "°", yfmt: v => v.toFixed(0), series, vlines: [{ x: m.fs, label: "f_s", color: DOMC.me }], markers: [{ x: m.fs, y: -90, label: "−90°", color: DOMC.me }] });
    b.note.innerHTML = `<p><b>What each knob does.</b> <span class="el">E</span> and <span class="el">x<sub>0</sub></span> only move the curve up and down: the output voltage is E·x/x<sub>0</sub>, so the electrical side sets the level and nothing else (a smaller gap also means a bigger C<sub>E0</sub> and less E before the diaphragm collapses onto the backplate). The <span class="ac">back volume</span> is a spring in series with the diaphragm's tension: shrink it and the capsule gets stiffer, less sensitive and higher in f<sub>s</sub>. <span class="ac">M<sub>AS</sub></span> is the air pushed through the backplate holes: it sets f<sub>s</sub>. <span class="ac">R<sub>AS</sub></span> is the viscous loss in the thin air film and the holes: it sets Q and nothing else.</p>`
      + `<p>Load <b>our 4134</b> and the model sits on Mic 1 within 0.2 dB at low frequency (10.98 measured, 11.14 model). Load <b>our 4133</b>: the shape is roughly right, but the level is 1.4 dB below Mic 2 (13.03 mV/Pa). The brief gives one E, x<sub>0</sub> and C<sub>MD</sub> for both types; in reality the 4133 and 4134 differ by about 30 % in compliance and 10 % in gap (appendix of the brief). Try x<sub>0</sub> ≈ 17.8 µm to put the 4133 on its level.</p>`;
  }
  upd();
}

// ---------------------------------------------------------------- Lab B: a standing wave in front of a hard face (why the measured 0° curve has a notch)
function benchLabBgap() {
  const b = bench("bench-labBgap", "Why our 0° curve has a notch: a standing wave in front of a hard face", "Lab B · theory · infinite rigid wall, BEM and measurement");
  if (!b || !window.LABB) return;
  const D = window.LABB, M = window.LABB_MEAS, c = 343.4, st = { d: 0.022 };
  slider(b.ctl, { label: "microphone distance from the face <b>d</b>", min: 0, max: 6, step: 0.1, value: st.d * 100, unit: "cm", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.d = v / 100; upd(); } });
  const ro = readouts(b.ctl, [{ id: "n1", label: "first null, d = λ/4", dom: "ac" }, { id: "n2", label: "second null, d = 3λ/4" }, { id: "meas", label: "our 0° notch, measured" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 100, xmax: 10000, ymin: -30, ymax: 12, ylabel: "pressure re the incident wave (dB)", yfmt: v => v.toFixed(0), yunit: " dB" });
  const fr = logspace(100, 10000, 700);
  let mn = null;
  if (M) { const m0 = M.dB[0], nt = M.f.map((f, k) => f > 3000 && f < 4500 ? m0[k] : 99), i = nt.indexOf(Math.min(...nt)); mn = { f: M.f[i], v: m0[i] }; }
  function upd() {
    const n1 = c / (4 * st.d), wall = fr.map(f => [f, Math.max(-60, dB(2 * Math.abs(Math.cos(2 * Math.PI * f * st.d / c))))]);
    ro({ n1: st.d > 0 ? hz(n1) : "none (on the face)", n2: st.d > 0 ? hz(3 * n1) : "none", meas: mn ? `${mn.v.toFixed(1)} dB at ${hz(mn.f)}` : "—" });
    const series = [{ name: `infinite rigid wall, d = ${(st.d * 100).toFixed(1)} cm`, color: DOMC.ac, pts: wall },
      { name: "BEM, face centre", color: DOMC.ink3, thin: true, pts: D.f.map((f, k) => [f, D.centre[0][k]]) },
      { name: "BEM, 3 cm in front", color: DOMC.me, thin: true, pts: D.f.map((f, k) => [f, D.fp[0][k]]) }];
    if (M) series.push({ name: "measured 0°, 22 Sep", color: DOMC.el, width: 2.2, pts: M.f.map((f, k) => [f, M.dB[0][k]]) });
    plot.set({ series, vlines: st.d > 0 && n1 < 10000 ? [{ x: n1, label: "λ/4", color: DOMC.ac }] : [], markers: mn ? [{ x: mn.f, y: mn.v, label: `${mn.v.toFixed(1)} dB`, color: DOMC.el }] : [] });
  }
  b.note.innerHTML = `<p><b>The picture.</b> A plane wave hits a hard face and comes straight back. In front of the face the two waves add: <span class="mono">p = p<sub>i</sub>(e<sup>jkd</sup> + e<sup>−jkd</sup>)</span>, so <span class="mono">|p|/|p<sub>i</sub>| = 2|cos kd|</span>. On the face (d = 0) that is the +6 dB of pressure doubling at every frequency; a distance d away there are nulls wherever d is an odd number of quarter wavelengths. Slide d to about 2.2 cm and the first null lands on our measured −18 dB notch at 3.9 kHz.</p>`
    + `<p><b>What the infinite wall gets wrong.</b> It says +6 dB at low frequency, but the real face is finite: below ka ≈ 0.5 the wave flows round the mock-up and the gain is 0 dB. It also ignores the rim diffraction that lifts the face centre to +9.9 dB. The full BEM solution at the field point 3 cm in front has both effects, and its notch sits at 4.0 kHz rather than the wall's 2.9 kHz: the wave reflected by a 25 cm face is not a plane wave, and close to the face its phase differs from the infinite-wall case. The lesson for the report: our curve above 2 kHz is the pressure a few cm <i>in front</i> of the face, not on it.</p>`;
  upd();
}

// ---------------------------------------------------------------- Lab D: one woofer in free air, a closed box and a vented box
// Same model as Lab D/matlab/test_labD.m: R_E + jωL_E + (Bl)²/Z_M, with Z_M = jωM_MS + R_MS + 1/(jωC_MS) + S_D²·Z_A(back).
const LABD = { rho: 1.2041, c: 343.2, RE: 6.0, LE: 0.4e-3, fs: 40, Qms: 4, Qes: 0.45, Vas: 25, VB: 20.125, aP: 0.0175, L: 0.10, N: 1, QL: 7, a: 0.065 };
function labDgrid(f1, f2) {   // the measurement's tones: 48 per octave on a 0.125 Hz grid
  const out = [];
  for (let k = 0; ; k++) { const f = 0.125 * Math.round(f1 * Math.pow(2, k / 48) / 0.125); if (f > f2) break; if (f >= f1 && f !== out[out.length - 1]) out.push(f); }
  return out;
}
function labDwoofer(p) {
  const ws = TAU * p.fs, CAS = p.Vas * 1e-3 / (p.rho * p.c * p.c), SD = Math.PI * p.a * p.a, CMS = CAS / (SD * SD);
  const MMS = 1 / (ws * ws * CMS), RMS = ws * MMS / p.Qms, Bl = Math.sqrt(ws * p.RE * MMS / p.Qes);
  const CAB = p.VB * 1e-3 / (p.rho * p.c * p.c), SP = Math.PI * p.aP * p.aP;
  const MAP = p.rho * (p.L + 1.46 * p.aP) / (p.N * SP), RAL = p.QL / Math.sqrt(CAB / MAP);
  const back = (f, mode) => mode === "free" ? cx(0) : mode === "closed" ? ZC(f, CAB)
    : cinv(cadd(cadd(cinv(cx(0, TAU * f * MAP)), cx(1 / RAL)), cx(0, TAU * f * CAB)));
  const zm = (f, mode) => cadd(cadd(cadd(cx(0, TAU * f * MMS), cx(RMS)), ZC(f, CMS)), cscale(back(f, mode), SD * SD));
  const Z = (f, mode) => cadd(cadd(cx(p.RE), cx(0, TAU * f * p.LE)), cdiv(cx(Bl * Bl), zm(f, mode)));
  // 1 V straight on the terminals (Part 3: resistor shorted): cone and port volume velocities, out of the box positive
  const flows = (f) => {
    const i = cinv(Z(f, "vent")), UD = cscale(cdiv(cscale(i, Bl), zm(f, "vent")), SD);
    const pB = cscale(cmul(UD, back(f, "vent")), -1), UP = cdiv(pB, cx(0, TAU * f * MAP));
    return { UD, UP };
  };
  return { SD, CMS, MMS, RMS, Bl, CAB, MAP, Z, flows, fb: 1 / (TAU * Math.sqrt(MAP * CAB)), fc: p.fs * Math.sqrt(1 + p.Vas / p.VB) };
}
// Appendix B on a curve: parabola on the peak in log f, f1/f2 interpolated in log f at √(R_E Z_max)
function labDts(fn, Zm, RE) {
  let i0 = 0; for (let k = 1; k < Zm.length; k++) if (Zm[k] > Zm[i0]) i0 = k;
  const x = [-1, 0, 1].map(d => Math.log(fn[i0 + d])), y = [-1, 0, 1].map(d => Zm[i0 + d]);
  const den = (x[0] - x[1]) * (x[0] - x[2]) * (x[1] - x[2]);
  const A = (x[2] * (y[1] - y[0]) + x[1] * (y[0] - y[2]) + x[0] * (y[2] - y[1])) / den;
  const B = (x[2] * x[2] * (y[0] - y[1]) + x[1] * x[1] * (y[2] - y[0]) + x[0] * x[0] * (y[1] - y[2])) / den;
  const C = (x[1] * x[2] * (x[1] - x[2]) * y[0] + x[2] * x[0] * (x[2] - x[0]) * y[1] + x[0] * x[1] * (x[0] - x[1]) * y[2]) / den;
  const lf0 = -B / (2 * A), f0 = Math.exp(lf0), Zmax = A * lf0 * lf0 + B * lf0 + C, rc = Zmax / RE, Zr = Math.sqrt(RE * Zmax);
  let lo = i0; while (lo > 0 && Zm[lo] >= Zr) lo--;
  let hi = i0; while (hi < Zm.length - 1 && Zm[hi] >= Zr) hi++;
  const li = (a, b) => Math.exp(Math.log(fn[a]) + (Zr - Zm[a]) / (Zm[b] - Zm[a]) * (Math.log(fn[b]) - Math.log(fn[a])));
  const f1 = li(lo, lo + 1), f2 = li(hi - 1, hi), QM = f0 * Math.sqrt(rc) / (f2 - f1);
  return { f0, Zmax, rc, Zr, f1, f2, QM, QE: QM / (rc - 1), QT: QM / rc };
}
function labDfb(fn, Zc) {   // two peaks; the minimum between them and the upward phase zero
  const Zm = Zc.map(cabs), pk = [];
  for (let k = 1; k < Zm.length - 1; k++) if (Zm[k] > Zm[k - 1] && Zm[k] >= Zm[k + 1]) pk.push(k);
  pk.sort((a, b) => Zm[b] - Zm[a]); const [a, b] = pk.slice(0, 2).sort((u, v) => u - v);
  let im = a; for (let k = a; k <= b; k++) if (Zm[k] < Zm[im]) im = k;
  let fph = NaN;
  for (let k = a; k < b; k++) { const p1 = carg(Zc[k]), p2 = carg(Zc[k + 1]); if (p1 < 0 && p2 >= 0) { fph = fn[k] + (0 - p1) / (p2 - p1) * (fn[k + 1] - fn[k]); break; } }
  return { fL: fn[a], fH: fn[b], fmin: fn[im], fph };
}
function benchLabD() {
  const b = bench("bench-labD", "One woofer, three backs: read f_S, the Q's, V_AS and f_B off the impedance", "Lab D · parts 2b1–2b4 · synthetic woofer from test_labD.m");
  if (!b) return;
  const st = Object.assign({}, LABD, { view: "all" });
  const seg = h("div", { class: "seg" });
  for (const [k, l] of [["all", "all three"], ["free", "free air"], ["closed", "closed box"], ["vent", "vented"]]) seg.append(h("button", { type: "button", class: st.view === k ? "on" : "", onclick: (e) => { st.view = k; $$("button", seg).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg);
  slider(b.ctl, { label: "driver resonance <b>f<sub>S</sub></b>", min: 20, max: 80, step: 0.5, value: st.fs, unit: "Hz", dom: "me", fmt: v => v.toFixed(1), onchange: v => { st.fs = v; upd(); } });
  slider(b.ctl, { label: "electrical Q <b>Q<sub>ES</sub></b>", min: 0.2, max: 1.2, step: 0.01, value: st.Qes, unit: "", dom: "el", fmt: v => v.toFixed(2), onchange: v => { st.Qes = v; upd(); } });
  slider(b.ctl, { label: "equivalent volume <b>V<sub>AS</sub></b>", min: 5, max: 80, step: 0.5, value: st.Vas, unit: "L", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.Vas = v; upd(); } });
  slider(b.ctl, { label: "box volume <b>V<sub>B</sub></b>", min: 5, max: 60, step: 0.125, value: st.VB, unit: "L", dom: "ac", fmt: v => v.toFixed(3), onchange: v => { st.VB = v; upd(); } });
  slider(b.ctl, { label: "vent tube length <b>L<sub>P</sub></b> (radius 17.5 mm)", min: 0.01, max: 0.3, step: 0.005, value: st.L, unit: "mm", dom: "ac", fmt: v => (v * 1000).toFixed(0), onchange: v => { st.L = v; upd(); } });
  const seg2 = h("div", { class: "seg" });
  for (const [k, l] of [[1, "one vent open"], [2, "both vents open"]]) seg2.append(h("button", { type: "button", class: st.N === k ? "on" : "", onclick: (e) => { st.N = k; $$("button", seg2).forEach(x => x.classList.toggle("on", x === e.target)); upd(); } }, l));
  b.ctl.append(seg2);
  const ro = readouts(b.ctl, [{ id: "free", label: "free air: f_S, Z_max", dom: "me" }, { id: "f12", label: "f₁ / f₂ at √(R_E Z_max)" }, { id: "q", label: "Q_MS / Q_ES / Q_TS read back", dom: "el" },
    { id: "cl", label: "closed box: f_C, Q_TC" }, { id: "vas", label: "V_AS = V_B[(f_C/f_S)² − 1]", dom: "ac" }, { id: "fb", label: "vented: f_B phase 0 / |Z| min / formula", dom: "ac" }]);
  const plot = new Plot(b.plot, { h: 330, xmin: 5, xmax: 500, ymin: 0, ymax: 70, ylabel: "|Z| (Ω)", yfmt: v => v.toFixed(0), yunit: " Ω" });
  const fn = labDgrid(1, 1000), sel = fn.map((f, k) => f <= 500 ? k : -1).filter(k => k >= 0), fs5 = sel.map(k => fn[k]);
  function upd() {
    const W = labDwoofer(st), Zs = {};
    for (const m of ["free", "closed", "vent"]) Zs[m] = fs5.map(f => W.Z(f, m));
    const tf = labDts(fs5, Zs.free.map(cabs), st.RE), tc = labDts(fs5, Zs.closed.map(cabs), st.RE), vb = labDfb(fs5, Zs.vent);
    const vas = st.VB * ((tc.f0 / tf.f0) ** 2 - 1);
    ro({ free: `${tf.f0.toFixed(2)} Hz, ${tf.Zmax.toFixed(1)} Ω (r_c = ${tf.rc.toFixed(2)})`, f12: `${tf.f1.toFixed(2)} / ${tf.f2.toFixed(2)} Hz at ${tf.Zr.toFixed(1)} Ω`,
      q: `${tf.QM.toFixed(2)} / ${tf.QE.toFixed(3)} / ${tf.QT.toFixed(3)}`, cl: `${tc.f0.toFixed(2)} Hz, Q_TC = ${tc.QT.toFixed(3)} (f_C/f_S = ${(tc.f0 / tf.f0).toFixed(3)})`,
      vas: `${vas.toFixed(2)} L (α = ${((tc.f0 / tf.f0) ** 2 - 1).toFixed(3)})`, fb: `${vb.fph.toFixed(1)} / ${vb.fmin.toFixed(1)} / ${W.fb.toFixed(1)} Hz` });
    const col = { free: DOMC.me, closed: DOMC.el, vent: DOMC.ac }, nm = { free: "free air", closed: "closed box", vent: `vented, L = ${(st.L * 1000).toFixed(0)} mm` };
    const show = st.view === "all" ? ["free", "closed", "vent"] : [st.view];
    const series = show.map(m => ({ name: nm[m], color: col[m], width: show.length === 1 ? 2.4 : 1.8, pts: fs5.map((f, k) => [f, cabs(Zs[m][k])]) }));
    const markers = [], vlines = [];
    if (show.includes("free")) { series.push({ name: "√(R_E Z_max), free air", color: DOMC.ink3, thin: true, pts: [[5, tf.Zr], [500, tf.Zr]] }); markers.push({ x: tf.f1, y: tf.Zr, label: "f₁", color: DOMC.me }, { x: tf.f2, y: tf.Zr, label: "f₂", color: DOMC.me }); vlines.push({ x: tf.f0, label: "f_S", color: DOMC.me }); }
    if (show.includes("closed")) vlines.push({ x: tc.f0, label: "f_C", color: DOMC.el });
    if (show.includes("vent")) vlines.push({ x: vb.fph, label: "f_B", color: DOMC.ac });
    plot.set({ ymax: Math.max(20, 10 * Math.ceil(Math.max(tf.Zmax, tc.Zmax) / 10 + 0.5)), series, markers, vlines });
  }
  b.note.innerHTML = `<p>This is the measurement of Part 2b done on paper. The woofer is invented (f<sub>S</sub> = 40 Hz, Q<sub>MS</sub> = 4, Q<sub>ES</sub> = 0.45, V<sub>AS</sub> = 25 L, R<sub>E</sub> = 6 Ω, L<sub>E</sub> = 0.4 mH), the box is 20.1 L and the vent 17.5 mm in radius: exactly what <span class="mono">test_labD.m</span> uses. The readouts apply the brief's Appendix B to the curve, the way <span class="mono">analyse_labD</span> does on the real data, and land back on the inputs: 39.99 Hz, 59.3 Ω, f₁ = 27.22 and f₂ = 58.54 Hz, Q<sub>MS</sub> = 4.01, Q<sub>ES</sub> = 0.452, f<sub>C</sub> = 59.88 Hz, V<sub>AS</sub> = 25.00 L. At 100 mm the vent gives f<sub>B</sub> = 33.5 Hz from the phase against 33.7 Hz from the formula.</p>`
    + `<p><b>Try:</b> make the box smaller and watch f<sub>C</sub> and Q<sub>TC</sub> rise together by √(1 + α). Lengthen the vent: both peaks slide down and the dip (f<sub>B</sub>) with them. Open the second vent: twice the area halves M<sub>AP</sub>, so f<sub>B</sub> rises by √2. The |Z| minimum always sits a little above the phase zero, which is why the lab script reports both.</p>`;
  upd();
}
function benchLabDnear() {
  const b = bench("bench-labDnear", "Near field at the cone and at the vent: the notch and the peak at f_B", "Lab D · part 3 · same woofer, 1 V on the terminals");
  if (!b) return;
  const st = Object.assign({}, LABD);
  slider(b.ctl, { label: "vent tube length <b>L<sub>P</sub></b>", min: 0.01, max: 0.3, step: 0.005, value: st.L, unit: "mm", dom: "ac", fmt: v => (v * 1000).toFixed(0), onchange: v => { st.L = v; upd(); } });
  slider(b.ctl, { label: "box loss <b>Q<sub>L</sub></b>", min: 2, max: 30, step: 0.5, value: st.QL, unit: "", dom: "ac", fmt: v => v.toFixed(1), onchange: v => { st.QL = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "fb", label: "f_B from the formula", dom: "ac" }, { id: "notch", label: "cone notch (between ½ and 2 f_B)" }, { id: "peak", label: "vent peak" }, { id: "dep", label: "notch depth below the cone's level at 2 f_B", dom: "me" }]);
  const plot = new Plot(b.plot, { h: 330, xmin: 5, xmax: 500, ymin: 40, ymax: 130, ylabel: "near-field SPL at 1 V (dB re 20 µPa)", yfmt: v => v.toFixed(0), yunit: " dB" });
  const fr = logspace(5, 500, 900);
  const MA1 = (a) => 8 * st.rho / (3 * Math.PI * Math.PI * a);
  function upd() {
    const W = labDwoofer(st), aP = st.aP;
    const F = fr.map(f => W.flows(f));
    const pc = F.map((q, k) => dB(cabs(q.UD) * TAU * fr[k] * MA1(st.a) / 2e-5)), pv = F.map((q, k) => dB(cabs(q.UP) * TAU * fr[k] * MA1(aP) / 2e-5));
    const ff = F.map((q, k) => dB(cabs(cadd(q.UD, q.UP)) * TAU * fr[k] * st.rho / (TAU * 1) / 2e-5));
    let iN = -1, iP = 0; for (let k = 0; k < fr.length; k++) { const w = fr[k] > 0.5 * W.fb && fr[k] < 2 * W.fb; if (w && (iN < 0 || pc[k] < pc[iN])) iN = k; if (fr[k] > 10 && pv[k] > pv[iP]) iP = k; }
    const k2 = fr.findIndex(f => f >= 2 * W.fb);
    ro({ fb: hz(W.fb), notch: `${hz(fr[iN])}`, peak: `${hz(fr[iP])}`, dep: `${(pc[k2] - pc[iN]).toFixed(1)} dB` });
    plot.set({ series: [{ name: "cone, near field", color: DOMC.me, width: 2.2, pts: fr.map((f, k) => [f, pc[k]]) }, { name: "vent, near field", color: DOMC.ac, width: 2.2, pts: fr.map((f, k) => [f, pv[k]]) },
      { name: "far field at 1 m, cone + vent", color: DOMC.ink3, thin: true, pts: fr.map((f, k) => [f, ff[k]]) }], vlines: [{ x: W.fb, label: "f_B", color: DOMC.ac }] });
  }
  b.note.innerHTML = `<p>Close to a piston the pressure is set by the air mass in front of it, <span class="mono">p<sub>near</sub> = jω M<sub>A1</sub> U</span> with <span class="mono">M<sub>A1</sub> = 8ρ/(3π²a)</span>. So each near-field curve has the far-field shape of its own radiator, and the level depends on its own radius. Here the cone has a = 6.5 cm and the vent 1.75 cm, which is why the vent curve sits so high: the two levels can only be added after scaling each one, which the grey far-field line does properly (ρω(U<sub>D</sub> + U<sub>P</sub>)/2πr).</p>`
    + `<p><b>What to look for in the lab:</b> the cone's <b>notch</b> sits at f<sub>B</sub>, the same tuning the impedance dip gives, and the vent's <b>peak</b> sits close to it but not on it (at 100 mm: notch 33.6 Hz, formula 33.7 Hz, vent peak 31.1 Hz). Read f<sub>B</sub> off the cone notch. Raise Q<sub>L</sub> (fewer losses) and the notch gets deeper. Below f<sub>B</sub> cone and vent move in antiphase, so the far field falls at 24 dB/octave even though each near-field curve does not. Real data will also show room modes, so measure the room.</p>`;
  upd();
}

document.addEventListener("DOMContentLoaded", () => { benchLab1(); benchLab2(); benchLab4(); benchLabB(); benchLabBgap(); benchLabC(); benchLabCcapsule(); benchLabD(); benchLabDnear(); });
