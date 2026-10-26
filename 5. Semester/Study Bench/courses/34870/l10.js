/* The Analogy Bench — the lumped-element crash course and lecture 10 (mixed models,
   metamaterials). Physics first (pure functions), then the benches, then the boot. */
"use strict";

/* ===== L10 · physics: ear drum, five-layer wall, metamaterial dispersion ===== */
const L10_AIR = { rho: 1.2, c: 343 };
const EAR_BRANCHES = [{ R: 50.6e6, C: 1.9e-12, L: 9400 }, { R: 31.1e6, C: 2.1e-12, L: 983.8 }];
function earDrum(f, br = EAR_BRANCHES) {  // slide 2: two series R-L-C branches in parallel, Pa·s/m³
  const z = br.map(b => cadd(cadd(ZR(b.R), ZL(f, b.L)), ZC(f, b.C)));
  return par(z[0], z[1]);
}
const WALL_LAYERS = [  // slide 4, normal incidence, per unit area
  { name: "drywall", rho: 600, c: 6000, l: 0.01, soft: false },
  { name: "insulation", rho: 200, c: 500, l: 0.03, soft: true },
  { name: "brick", rho: 2000, c: 3600, l: 0.05, soft: false },
  { name: "air gap", rho: 1.2, c: 343, l: 0.01, soft: true },
  { name: "wood", rho: 550, c: 4000, l: 0.02, soft: false },
];
const m2mul = (A, B) => [[cadd(cmul(A[0][0], B[0][0]), cmul(A[0][1], B[1][0])), cadd(cmul(A[0][0], B[0][1]), cmul(A[0][1], B[1][1]))],
                         [cadd(cmul(A[1][0], B[0][0]), cmul(A[1][1], B[1][0])), cadd(cmul(A[1][0], B[0][1]), cmul(A[1][1], B[1][1]))]];
function layerMatrix(f, L, asLine) {
  const w = TAU * f;
  if (asLine) {  // exact 1-D layer = lossless transmission line
    const k = w / L.c, Z0 = L.rho * L.c, c = Math.cos(k * L.l), s = Math.sin(k * L.l);
    return [[cx(c, 0), cx(0, Z0 * s)], [cx(0, s / Z0), cx(c, 0)]];
  }
  if (L.soft) return [[cx(1, 0), cx(0, 0)], [cx(0, w * L.l / (L.rho * L.c * L.c)), cx(1, 0)]];  // shunt compliance l/(ρc²)
  return [[cx(1, 0), cx(0, w * L.rho * L.l)], [cx(0, 0), cx(1, 0)]];                               // series mass ρl
}
function wallT(f, layers, mode) {  // mode: "lem" | "mixed" | "tmm"; returns p_out/p_in (complex)
  let M = [[cx(1, 0), cx(0, 0)], [cx(0, 0), cx(1, 0)]];
  for (const L of layers) M = m2mul(M, layerMatrix(f, L, mode === "tmm" || (mode === "mixed" && L.soft)));
  const Rout = L10_AIR.rho * L10_AIR.c;
  return cinv(cadd(M[0][0], cscale(M[0][1], 1 / Rout)));
}
function wallPeaks(layers, mode, f1 = 50, f2 = 20000, n = 6000) {
  const fs = logspace(f1, f2, n), y = fs.map(f => cabs(wallT(f, layers, mode)));
  const out = [];
  for (let i = 1; i < n - 1; i++) if (y[i] > y[i - 1] && y[i] > y[i + 1]) out.push(fs[i]);
  return out;
}
function wallLumpedPeaks(layers) {  // the two hand formulas of §4.2 (masses between the soft layers)
  const M = layers.filter(L => !L.soft).map(L => L.rho * L.l), C = layers.filter(L => L.soft).map(L => L.l / (L.rho * L.c * L.c));
  const fA = Math.sqrt((1 / (M[0] + M[1]) + 1 / M[2]) / C[1]) / TAU;  // air gap between (drywall+brick) and wood
  const fB = Math.sqrt((1 / M[0] + 1 / (M[1] + M[2])) / C[0]) / TAU;  // insulation between drywall and (brick+wood)
  const ins = layers[1], fBc = Math.sqrt((1 / (M[0] + ins.rho * ins.l / 3) + 1 / (M[1] + M[2])) / C[0]) / TAU;
  return { fA, fB, fBc, m: layers.reduce((s, L) => s + L.rho * L.l, 0) };
}
/* dispersion: Bragg chain and locally resonant chain; returns ω/ω0 for kd in [0, π] */
const braggW = (kd) => 2 * Math.abs(Math.sin(kd / 2));
function resonantW(kd, mu, OR) {  // both branches of W²/Ω² − W(1+μ+a/Ω²) + a = 0, W = (ω/ω0)²
  const a = 2 * (1 - Math.cos(kd)), A = 1 / (OR * OR), B = -(1 + mu + a / (OR * OR)), C = a;
  const d = Math.sqrt(B * B - 4 * A * C);
  return [Math.sqrt((-B - d) / (2 * A)), Math.sqrt((-B + d) / (2 * A))];
}
function resonantGap(mu, OR) { return { lo: resonantW(Math.PI, mu, OR)[0], hi: OR * Math.sqrt(1 + mu) }; }

/* ===== Crash course · physics of the four recipe systems ===== */
/* all values SI; each returns the response the bench plots, plus what the readouts need */
function recipeSys(key, p, f) {
  const w = TAU * f;
  if (key === "msd") {          // force on a mass, spring + damper to the wall
    const Z = cadd(cadd(ZL(f, p.M), ZC(f, p.C)), ZR(p.R));
    return { y: cscale(cinv(Z), 1), Z };                                   // u per newton
  }
  if (key === "base") {         // shaker base moves with u_b, spring ∥ damper up to a mass
    const Zsr = cadd(ZR(p.R), ZC(f, p.C));                                 // spring + damper share u_b − u_m → series (impedance analogy)
    return { y: cdiv(Zsr, cadd(Zsr, ZL(f, p.M))) };                        // u_m / u_b: current divider
  }
  if (key === "helm") {         // sound pressure on a bottle: neck R_A + M_A, cavity C_A
    const Zc = ZC(f, p.C), Z = cadd(cadd(ZR(p.R), ZL(f, p.M)), Zc);
    return { y: cdiv(Zc, Z), Z };                                          // p_cavity / p_outside: voltage divider
  }
  if (key === "two") {          // force on M1, link spring ∥ damper to a free M2
    const Zlink = cadd(ZR(p.R), ZC(f, p.C)), Zm2 = ZL(f, p.M2);
    const Z = cadd(ZL(f, p.M), par(Zlink, Zm2));                           // what the force sees
    const u1 = cinv(Z), u2 = cmul(u1, cdiv(Zlink, cadd(Zlink, Zm2)));      // per newton
    return { y: u1, y2: u2, Z };
  }
}
function recipeNumbers(key, p) {
  if (key === "msd" || key === "base" || key === "helm") return { f0: 1 / (TAU * Math.sqrt(p.M * p.C)), Q: Math.sqrt(p.M / p.C) / p.R };
  const fa = 1 / (TAU * Math.sqrt(p.M2 * p.C));                            // M2 on the link: the absorber (u1 → 0)
  const fr = 1 / (TAU * Math.sqrt(p.C * p.M * p.M2 / (p.M + p.M2)));       // the two masses bouncing against each other
  return { fa, fr };
}

/* ===== Crash course · the reading rules: impedance of five small networks ===== */
const ZNETS = {
  srlc: { name: "R + L + C in series", els: ["R", "L", "C"], Z: (f, v) => cadd(cadd(ZR(v.R), ZL(f, v.L)), ZC(f, v.C)) },
  prlc: { name: "R ∥ L ∥ C", els: ["R", "L", "C"], Z: (f, v) => par(par(ZR(v.R), ZL(f, v.L)), ZC(f, v.C)) },
  spk:  { name: "R₂ + (R ∥ L ∥ C)", els: ["R2", "R", "L", "C"], Z: (f, v) => cadd(ZR(v.R2), par(par(ZR(v.R), ZL(f, v.L)), ZC(f, v.C))) },
  rlpc: { name: "(R + L) ∥ C", els: ["R", "L", "C"], Z: (f, v) => par(cadd(ZR(v.R), ZL(f, v.L)), ZC(f, v.C)) },
  rl:   { name: "R + L", els: ["R", "L"], Z: (f, v) => cadd(ZR(v.R), ZL(f, v.L)) },
};
const ZDOM = {  // names, units and slider ranges per domain (impedance analogy throughout)
  el: { tag: "electrical", unit: "Ω", R: ["R", "Ω", 0.5, 200, 8], R2: ["R₂", "Ω", 0.5, 50, 6], L: ["L", "mH", 0.1, 1000, 10, 1e-3], C: ["C", "µF", 0.1, 1000, 10, 1e-6] },
  me: { tag: "mechanical", unit: "Ns/m", R: ["R<sub>M</sub>", "Ns/m", 0.05, 50, 1], R2: ["R<sub>M2</sub>", "Ns/m", 0.05, 20, 0.5], L: ["M<sub>M</sub>", "g", 1, 1000, 10, 1e-3], C: ["C<sub>M</sub>", "mm/N", 0.01, 10, 1, 1e-3] },
  ac: { tag: "acoustical", unit: "Pa·s/m³", R: ["R<sub>A</sub>", "Pa·s/m³", 1e3, 1e7, 1e5], R2: ["R<sub>A2</sub>", "Pa·s/m³", 1e3, 1e6, 5e4], L: ["M<sub>A</sub>", "kg/m⁴", 10, 1e5, 500], C: ["C<sub>A</sub>", "m⁵/N", 1e-11, 1e-6, 1e-8] },
};

/* ===== Crash course · crossing a transducer ===== */
const CROSS_ELS = {   // the 315 SWR of Problems 7: Bl 11.6 T·m, S_D 519 cm²
  mass: { name: "cone mass M<sub>MD</sub>", start: "me", kind: "L", v: 74.6e-3 },
  spring: { name: "suspension C<sub>MS</sub>", start: "me", kind: "C", v: 0.55e-3 },
  damper: { name: "damping R<sub>MS</sub>", start: "me", kind: "R", v: 3.25 },
  box: { name: "box air V<sub>AB</sub> = 30 L", start: "ac", kind: "C", v: 0.030 / (RHO * C0 * C0) },
  air: { name: "air load M<sub>A1</sub> (front)", start: "ac", kind: "L", v: null },
};
function crossValues(el, Bl, S) {   // the same element in all three domains; impedance analogy for M and A, the electrical side after the gyrator
  const toMe = el.start === "me" ? 1 : S * S;     // Z_M = S² Z_A
  const a = Math.sqrt(S / Math.PI);
  const v0 = el.v ?? 8 * RHO / (3 * Math.PI * Math.PI * a);
  let me, ac;
  if (el.kind === "C") { me = el.start === "me" ? v0 : v0 / (S * S); ac = me * S * S; }   // compliance: C_M = C_A / S²
  else { me = el.start === "me" ? v0 : v0 * toMe; ac = me / (S * S); }                  // mass, resistance: M_M = S² M_A
  // gyrator Z_E = (Bl)²/Z_M: mass → C = M/(Bl)², compliance → L = (Bl)² C_M, damper → R = (Bl)²/R_M
  const el2 = el.kind === "L" ? { kind: "C", v: me / (Bl * Bl) } : el.kind === "C" ? { kind: "L", v: Bl * Bl * me } : { kind: "R", v: Bl * Bl / me };
  return { me, ac, el: el2 };
}

/* ===== mechanical sketch kit (SVG strings, same spirit as CK) ===== */
const MK = {
  ground: (x1, x2, y) => `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke="var(--ink)" stroke-width="2"/>` +
    Array.from({ length: Math.floor((x2 - x1) / 10) }, (_, i) => `<line x1="${x1 + 4 + i * 10}" y1="${y + 1}" x2="${x1 - 4 + i * 10}" y2="${y + 9}" stroke="var(--ink-3)" stroke-width="1.2"/>`).join(""),
  mass: (x, y, w, hh, label) => `<rect x="${x}" y="${y}" width="${w}" height="${hh}" rx="4" fill="var(--me-soft)" stroke="var(--me)" stroke-width="2"/>` + CK.label(x + w / 2, y + hh / 2 + 4, label, DOMC.me, "middle", 13),
  spring: (x1, y1, x2, y2, label) => {   // horizontal or vertical zigzag
    const horiz = y1 === y2, L = horiz ? x2 - x1 : y2 - y1, n = 7, lead = L * 0.15, seg = (L - 2 * lead) / n;
    let d = horiz ? `M${x1} ${y1} h${lead}` : `M${x1} ${y1} v${lead}`;
    for (let i = 0; i < n; i++) d += horiz ? ` l${seg / 2} ${i % 2 ? 7 : -7} l${seg / 2} ${i % 2 ? -7 : 7}` : ` l${i % 2 ? 7 : -7} ${seg / 2} l${i % 2 ? -7 : 7} ${seg / 2}`;
    d += horiz ? ` h${lead}` : ` v${lead}`;
    return `<path d="${d}" fill="none" stroke="var(--me)" stroke-width="1.8"/>` + (label ? CK.label(horiz ? (x1 + x2) / 2 : x1 - 12, horiz ? y1 - 12 : (y1 + y2) / 2 + 4, label, DOMC.me, horiz ? "middle" : "end", 11.5) : "");
  },
  damper: (x1, y1, x2, y2, label) => {  // dashpot: cup on one side, piston on the other
    const horiz = y1 === y2, L = horiz ? x2 - x1 : y2 - y1, m = L / 2;
    const g = horiz
      ? `<path d="M${x1} ${y1} h${m - 4} M${x1 + m - 4} ${y1 - 8} v16 M${x1 + m - 12} ${y1 - 11} h20 v22 h-20 M${x1 + m + 8} ${y1} H${x2}"/>`
      : `<path d="M${x1} ${y1} v${m - 4} M${x1 - 8} ${y1 + m - 4} h16 M${x1 - 11} ${y1 + m - 12} v20 h22 v-20 M${x1} ${y1 + m + 8} V${y2}"/>`;
    return `<g fill="none" stroke="var(--me)" stroke-width="1.8">${g}</g>` + (label ? CK.label(horiz ? (x1 + x2) / 2 : x1 + 16, horiz ? y1 + 26 : (y1 + y2) / 2 + 4, label, DOMC.me, horiz ? "middle" : "start", 11.5) : "");
  },
  force: (x1, y1, x2, y2, label, col = DOMC.ink) => {  // straight arrow from (x1,y1) to (x2,y2)
    const a = Math.atan2(y2 - y1, x2 - x1), hx = (s) => x2 - 9 * Math.cos(a + s), hy = (s) => y2 - 9 * Math.sin(a + s);
    return `<path d="M${x1} ${y1} L${x2} ${y2} M${hx(0.45)} ${hy(0.45)} L${x2} ${y2} L${hx(-0.45)} ${hy(-0.45)}" fill="none" stroke="${col}" stroke-width="2"/>` + (label ? CK.label((x1 + x2) / 2 + (x1 === x2 ? 8 : 0), (y1 + y2) / 2 + (x1 === x2 ? 4 : -8), label, col, x1 === x2 ? "start" : "middle", 12) : "");
  },
  vel: (x, y, label) => `<path d="M${x} ${y + 12} v-24 M${x - 4} ${y - 6} l4 -6 4 6" fill="none" stroke="var(--warn)" stroke-width="1.6"/>` + CK.label(x + 7, y + 4, label, DOMC.warn, "start", 11.5),
};
const sub = (b, s) => `${b}<tspan font-size='9' dy='3'>${s}</tspan>`;

/* ===== Crash course bench 1 · from sketch to circuit, one step at a time ===== */
const RECIPES = {
  msd: {
    name: "mass on a spring", short: "force on a mass, spring and damper to the wall",
    p: { M: 0.02, C: 1e-3, R: 0.5 }, dom: "me",
    sliders: [["M", "mass <b>M<sub>M</sub></b>", 2, 200, "g", 1e-3], ["C", "compliance <b>C<sub>M</sub></b> = 1/k", 0.05, 10, "mm/N", 1e-3], ["R", "damper <b>R<sub>M</sub></b>", 0.05, 10, "Ns/m", 1]],
    sketch: () => MK.ground(30, 210, 182) + MK.spring(80, 112, 80, 182, "k") + MK.damper(160, 112, 160, 182, "R_M") + MK.mass(50, 72, 140, 40, "M_M") + MK.force(120, 18, 120, 70, "f") + MK.vel(205, 92, "u"),
    vels: "<b>One</b> velocity, <span class='mono'>u</span>, the mass's. The top of the spring and the top of the damper move with the mass; their bottoms sit on the wall (u = 0, ground). So all three elements see the same u.",
    mob: () => svgWrap(320, 200, [ISRC(40, 160, 40, 40, DOMC.me, "f", -1), CK.wire(40, 40, 260, 40), CK.dot(110, 40), CK.dot(180, 40), CK.dot(260, 40),
      CAP(110, 40, 110, 160, DOMC.me, sub("M", "M"), 1), IND(180, 40, 180, 160, DOMC.me, sub("C", "M"), 1), RES(260, 40, 260, 160, DOMC.me, "1/" + sub("R", "M"), 1),
      CK.wire(40, 160, 260, 160), CK.gnd(150, 160), CK.label(150, 28, "node u", DOMC.warn, "middle", 11)].join("")),
    imp: () => svgWrap(320, 200, [VSRC(40, 160, 40, 40, DOMC.me, "f", -1), CK.wire(40, 40, 90, 40), IND(90, 40, 170, 40, DOMC.me, sub("M", "M")), CAP(170, 40, 250, 40, DOMC.me, sub("C", "M")), CK.wire(250, 40, 290, 40),
      RES(290, 40, 290, 160, DOMC.me, sub("R", "M"), 1), CK.wire(290, 160, 40, 160), CK.gnd(165, 160), CK.label(165, 100, "loop current u", DOMC.warn, "middle", 11)].join("")),
    rule: "Mobility: three elements between node u and ground → all in <b>parallel</b>. Impedance analogy is the dual: one node pair becomes one loop, so all in <b>series</b>. Same physics: <span class='mono'>f = (jωM + 1/jωC + R)·u</span>.",
    ylabel: "velocity per newton |u/f|  (dB re 1 m/(N·s))",
  },
  base: {
    name: "shaker table", short: "the base moves; spring and damper carry the motion up to a mass",
    p: { M: 0.1, C: 0.25e-3, R: 2 }, dom: "me",
    sliders: [["M", "mass <b>M<sub>M</sub></b>", 10, 1000, "g", 1e-3], ["C", "compliance <b>C<sub>M</sub></b>", 0.02, 5, "mm/N", 1e-3], ["R", "damper <b>R<sub>M</sub></b>", 0.1, 30, "Ns/m", 1]],
    sketch: () => MK.ground(30, 210, 190) + `<rect x="40" y="160" width="160" height="16" rx="3" fill="var(--surface-2,var(--rule))" stroke="var(--ink-2)" stroke-width="1.6"/>` + CK.label(120, 172, "shaker, imposes u_b", DOMC.ink2, "middle", 10.5) + MK.spring(85, 100, 85, 160, "k") + MK.damper(155, 100, 155, 160, "R_M") + MK.mass(55, 60, 130, 40, "M_M") + MK.vel(205, 80, "u_m") + MK.vel(212, 168, "u_b"),
    vels: "<b>Two</b> velocities: the base's <span class='mono'>u_b</span> (set by the shaker: a <b>velocity source</b>) and the mass's <span class='mono'>u_m</span>. Spring and damper sit side by side between the two, so both see the <i>difference</i> u_b − u_m. The mass is measured against the fixed world: ground.",
    mob: () => svgWrap(340, 200, [VSRC(40, 160, 40, 40, DOMC.me, sub("u", "b"), -1), CK.wire(40, 40, 100, 40), CK.dot(100, 40), CK.wire(100, 20, 100, 64),
      IND(100, 20, 240, 20, DOMC.me, sub("C", "M")), RES(100, 64, 240, 64, DOMC.me, "1/" + sub("R", "M"), -1), CK.wire(240, 20, 240, 64), CK.wire(240, 42, 290, 42), CK.dot(290, 42),
      CAP(290, 42, 290, 160, DOMC.me, sub("M", "M"), 1), CK.wire(40, 160, 290, 160), CK.gnd(165, 160), CK.label(100, 108, "node u_b", DOMC.warn, "middle", 11), CK.label(290, 30, "node u_m", DOMC.warn, "middle", 11)].join("")),
    imp: () => svgWrap(320, 200, [ISRC(40, 160, 40, 40, DOMC.me, sub("u", "b"), -1), CK.wire(40, 40, 260, 40), CK.dot(130, 40), CK.dot(260, 40),
      IND(130, 40, 130, 160, DOMC.me, sub("M", "M"), 1), CAP(260, 40, 260, 100, DOMC.me, sub("C", "M"), 1), RES(260, 100, 260, 160, DOMC.me, sub("R", "M"), 1),
      CK.wire(40, 160, 260, 160), CK.gnd(195, 160), CK.label(130, 28, "u_m = current in M", DOMC.warn, "middle", 11)].join("")),
    rule: "Mobility keeps the <b>physical drawing</b>: spring and damper side by side between the same two velocities → side by side between the same two nodes. In the impedance analogy they share the velocity difference, so they are in <b>series</b>, and that branch is in <b>parallel</b> with the mass because both carry the same force. The shaker becomes a current source. Output: a current divider.",
    ylabel: "transmissibility |u_m / u_b|  (dB)",
  },
  helm: {
    name: "Helmholtz bottle", short: "sound outside a bottle: air plug in the neck on a cavity spring",
    p: { M: 1000, C: 1.33e-8, R: 2e5 }, dom: "ac",
    sliders: [["M", "neck mass <b>M<sub>A</sub></b> = ρl*/S", 100, 1e4, "kg/m⁴", 1], ["C", "cavity <b>C<sub>A</sub></b> = V/ρc²", 1e-9, 1e-7, "m⁵/N", 1], ["R", "neck loss <b>R<sub>A</sub></b>", 1e4, 3e6, "Pa·s/m³", 1]],
    sketch: () => `<rect x="60" y="90" width="120" height="92" rx="10" fill="var(--ac-soft)" stroke="var(--ac)" stroke-width="2"/><rect x="104" y="44" width="32" height="46" fill="var(--el-soft)" stroke="var(--ac)" stroke-width="2"/>` +
      `<rect x="107" y="56" width="26" height="16" fill="var(--ac)" opacity="0.55"/>` + CK.label(120, 142, "C_A cavity", DOMC.ac, "middle", 12) + CK.label(145, 66, "M_A + R_A (neck)", DOMC.ac, "start", 11) +
      `<path d="M40 22 q8 -8 16 0 t16 0 t16 0 t16 0" fill="none" stroke="var(--ink-2)" stroke-width="1.6"/>` + CK.label(20, 26, "p", DOMC.ink, "middle", 13) + MK.ground(30, 210, 190),
    vels: "Acoustics: <b>one</b> volume velocity <span class='mono'>U</span> flows in through the neck and is stored in the cavity. The air plug feels the pressure <i>difference</i> p − p_cav; the cavity feels p_cav against ambient (ground: always ground a volume).",
    mob: () => svgWrap(320, 200, [ISRC(40, 160, 40, 40, DOMC.ac, "p", -1), CK.wire(40, 40, 260, 40), CK.dot(110, 40), CK.dot(180, 40), CK.dot(260, 40),
      CAP(110, 40, 110, 160, DOMC.ac, sub("M", "A"), 1), IND(180, 40, 180, 160, DOMC.ac, sub("C", "A"), 1), RES(260, 40, 260, 160, DOMC.ac, "1/" + sub("R", "A"), 1),
      CK.wire(40, 160, 260, 160), CK.gnd(150, 160), CK.label(150, 28, "node U  (nobody draws it like this)", DOMC.ink3, "middle", 11)].join("")),
    imp: () => svgWrap(320, 200, [VSRC(40, 160, 40, 40, DOMC.ac, "p", -1), CK.wire(40, 40, 60, 40), RES(60, 40, 140, 40, DOMC.ac, sub("R", "A")), IND(140, 40, 220, 40, DOMC.ac, sub("M", "A")), CK.wire(220, 40, 270, 40), CK.dot(270, 40),
      CAP(270, 40, 270, 160, DOMC.ac, sub("C", "A"), 1), CK.wire(270, 160, 40, 160), CK.gnd(155, 160), CK.label(270, 28, "p_cav", DOMC.warn, "middle", 11)].join("")),
    rule: "Acoustics is drawn in the <b>impedance analogy</b> (pressure = voltage), because then a volume is a capacitor <b>to ground</b>, exactly like the cavity's pressure is measured against the atmosphere. Neck elements share U → series. Output: a voltage divider, p_cav/p = Z_C/(Z_R + Z_M + Z_C).",
    ylabel: "cavity pressure gain |p_cav / p|  (dB)",
  },
  two: {
    name: "two masses", short: "force on M₁, a soft link to a free M₂ (problem 2.4 / vibration absorber)",
    p: { M: 0.2, M2: 0.05, C: 0.5e-3, R: 0.3 }, dom: "me",
    sliders: [["M", "driven mass <b>M₁</b>", 10, 1000, "g", 1e-3], ["M2", "free mass <b>M₂</b>", 5, 500, "g", 1e-3], ["C", "link <b>C<sub>M</sub></b>", 0.02, 5, "mm/N", 1e-3], ["R", "link loss <b>R<sub>M</sub></b>", 0.01, 10, "Ns/m", 1]],
    sketch: () => MK.ground(20, 220, 150) + MK.mass(40, 96, 56, 54, "M₁") + MK.mass(160, 96, 56, 54, "M₂") + MK.spring(96, 110, 160, 110, "k") + MK.damper(96, 136, 160, 136, "") + CK.label(128, 160, "R_M", DOMC.me, "middle", 11) +
      MK.force(4, 123, 38, 123, "") + CK.label(12, 112, "f", DOMC.ink, "middle", 12) + `<path d="M50 84 h24 M68 80 l6 4 -6 4" fill="none" stroke="var(--warn)" stroke-width="1.6"/>` + CK.label(68, 76, "u₁", DOMC.warn, "middle", 11) + `<path d="M170 84 h24 M188 80 l6 4 -6 4" fill="none" stroke="var(--warn)" stroke-width="1.6"/>` + CK.label(188, 76, "u₂", DOMC.warn, "middle", 11) + CK.note(120, 185, "frictionless floor: both masses measured against ground"),
    vels: "<b>Two</b> velocities, <span class='mono'>u₁</span> and <span class='mono'>u₂</span> → two nodes besides ground. Each mass hangs between its own velocity and ground. The link (spring ∥ damper) sits between u₁ and u₂, so it sees u₁ − u₂.",
    mob: () => svgWrap(340, 200, [ISRC(40, 160, 40, 40, DOMC.me, "f", -1), CK.wire(40, 40, 150, 40), CK.dot(100, 40), CAP(100, 40, 100, 160, DOMC.me, "M₁", 1), CK.wire(150, 20, 150, 64),
      IND(150, 20, 250, 20, DOMC.me, sub("C", "M")), RES(150, 64, 250, 64, DOMC.me, "1/" + sub("R", "M"), -1), CK.wire(250, 20, 250, 64), CK.wire(250, 42, 300, 42), CK.dot(300, 42),
      CAP(300, 42, 300, 160, DOMC.me, "M₂", 1), CK.wire(40, 160, 300, 160), CK.gnd(200, 160), CK.label(100, 28, "node u₁", DOMC.warn, "middle", 11), CK.label(300, 30, "node u₂", DOMC.warn, "middle", 11)].join("")),
    imp: () => svgWrap(330, 200, [VSRC(40, 160, 40, 40, DOMC.me, "f", -1), CK.wire(40, 40, 70, 40), IND(70, 40, 150, 40, DOMC.me, "M₁"), CK.wire(150, 40, 290, 40), CK.dot(200, 40), CK.dot(290, 40),
      CAP(200, 40, 200, 100, DOMC.me, sub("C", "M"), 1), RES(200, 100, 200, 160, DOMC.me, sub("R", "M"), 1), IND(290, 40, 290, 160, DOMC.me, "M₂", 1),
      CK.wire(40, 160, 290, 160), CK.gnd(120, 160), CK.label(110, 70, "u₁", DOMC.warn, "middle", 11)].join("")),
    rule: "Mobility again mirrors the sketch. Dualise for the impedance analogy: M₁ carries all of u₁ → in series with the source; the link and M₂ carry the <b>same force</b> (what the spring pushes, M₂ feels) → in <b>parallel</b>. A lossless L ∥ C blocks completely at its resonance: that is the <b>vibration absorber</b>: M₁ stands still while M₂ dances.",
    ylabel: "velocity per newton  (dB re 1 m/(N·s))",
  },
};
const RECIPE_STEPS = ["1 · look at the sketch", "2 · count the velocities", "3 · mobility circuit (copy the drawing)", "4 · impedance circuit (the dual)", "5 · solve and read the curve"];
function benchRecipe() {
  const b = bench("bench-recipe", "From sketch to circuit, one step at a time", "crash course · the method", { one: true });
  if (!b) return;
  const st = { key: "msd", step: 0, p: {} };
  const ctlTop = h("div", { class: "bench-ctl", style: "border-left:0;border-bottom:1px solid var(--rule)" });
  b.plot.before(ctlTop);
  const chips = h("div", { class: "chips" });
  for (const [k, r] of Object.entries(RECIPES)) chips.append(h("button", { class: "chip" + (k === st.key ? " on" : ""), type: "button", onclick: (e) => { st.key = k; st.step = 0; $$(".chip", chips).forEach(c => c.classList.toggle("on", c === e.target)); build(); } }, r.name));
  const stepper = h("div", { class: "seg" });
  RECIPE_STEPS.forEach((s, i) => stepper.append(h("button", { type: "button", onclick: () => { st.step = i; show(); } }, s)));
  ctlTop.append(chips, stepper);
  const grid = h("div", {});
  b.plot.append(grid);
  const sliderBox = h("div", { class: "bench-ctl", style: "border-left:0;border-top:1px solid var(--rule)" });
  b.plot.after(sliderBox);
  let plot, ro, cells;
  function build() {
    const r = RECIPES[st.key];
    st.p = { ...r.p };
    grid.innerHTML = "";
    const cell = (title, inner, cap = "") => { const d = h("div", { class: "circuit" }); d.innerHTML = `<div class="eyebrow" style="margin-bottom:4px">${title}</div>${inner}${cap ? `<div class="cap">${cap}</div>` : ""}`; return d; };
    const sk = cell("the system", svgWrap(240, 200, r.sketch()), r.short);
    const ve = h("div", { class: "circuit" }); ve.innerHTML = `<div class="eyebrow" style="margin-bottom:4px">the velocities</div><p class="small" style="max-width:none">${r.vels}</p>`;
    const mo = cell("mobility analogy · velocity = voltage", r.mob(), "every element between the two velocities its ends see; masses always to ground");
    const im = cell("impedance analogy · force/pressure = voltage", r.imp(), "the dual: nodes ↔ loops, parallel ↔ series, L ↔ C, R ↔ 1/R");
    const two1 = h("div", { class: "two" }, sk, ve), two2 = h("div", { class: "two" }, mo, im);
    const rule = h("div", { class: "small", style: "margin:4px 2px 10px", html: `<p style="max-width:none"><b>The rule here.</b> ${r.rule}</p>` });
    const pbox = h("div", {});
    grid.append(two1, two2, rule, pbox);
    cells = [[sk], [ve], [mo], [im, rule], [pbox]];
    plot = new Plot(pbox, { h: 250, xmin: 10, xmax: st.key === "helm" ? 2000 : 1000, ymin: -60, ymax: 30, ylabel: r.ylabel, yfmt: v => v.toFixed(1), yunit: " dB" });
    sliderBox.innerHTML = "";
    for (const [k, lab, lo, hi, unit, sc] of r.sliders) slider(sliderBox, { label: lab, min: lo, max: hi, value: r.p[k] / sc, log: true, unit, dom: r.dom, onchange: v => { st.p[k] = v * sc; upd(); } });
    ro = readouts(sliderBox, st.key === "two" ? [{ id: "fa", label: "absorber f_a = 1/2π√(M₂C)", dom: "me" }, { id: "fr", label: "masses vs each other", dom: "me" }] : [{ id: "f0", label: "f₀ = 1/2π√(MC)", dom: r.dom }, { id: "Q", label: "Q = √(M/C)/R" }]);
    show(); upd();
  }
  function show() {
    $$("button", stepper).forEach((x, i) => x.classList.toggle("on", i === st.step));
    cells.forEach((group, i) => group.forEach(el => { el.style.opacity = i <= st.step ? "1" : "0.07"; el.style.transition = "opacity .25s"; }));
    sliderBox.style.display = st.step >= 4 ? "" : "none";
    const msg = [
      "Before anything else: what moves, what is fixed, what drives it? Then press step 2.",
      "Count the <b>distinct velocities</b> (mechanics) or pressures (acoustics). Each becomes a node in the mobility circuit, plus ground for the fixed world.",
      "<b>Mobility analogy</b> (velocity ↔ voltage): draw one node per velocity and put each element between the two velocities its ends see. Masses always go to ground, because Newton measures acceleration against the fixed world. A force is a current source.",
      "<b>Impedance analogy</b> (force ↔ voltage): take the dual. Elements that share a velocity go in series; elements that share a force go in parallel. Mass → inductor, compliance → capacitor, damper → R. This is the circuit the slides use for acoustics.",
      "Now it is circuit analysis: dividers, resonances, asymptotes. Drag the sliders and watch f₀ and Q move.",
    ][st.step];
    b.note.innerHTML = `<p>${msg}</p><p class="muted">Work each step on paper first, then reveal it. Four systems cover every topology you meet in lectures 2–9: one loop, a velocity source, an acoustic divider and a two-node chain.</p>`;
  }
  function upd() {
    const r = RECIPES[st.key], fs = logspace(10, plot.o.xmax, 360);
    const res = fs.map(f => recipeSys(st.key, st.p, f));
    const s = [{ name: st.key === "two" ? "|u₁/f| (driven mass)" : r.ylabel.split("  ")[0], color: DOMC[r.dom], pts: fs.map((f, i) => [f, dB(cabs(res[i].y))]) }];
    if (st.key === "two") s.push({ name: "|u₂/f| (free mass)", color: DOMC.el, pts: fs.map((f, i) => [f, dB(cabs(res[i].y2))]) });
    const all = s.flatMap(x => x.pts.map(p => p[1])).filter(isFinite);
    const top = Math.ceil(Math.max(...all) / 10) * 10 + 5, bot = Math.max(Math.floor(Math.min(...all) / 10) * 10, top - 90);
    const n = recipeNumbers(st.key, st.p);
    const vlines = st.key === "two" ? [{ x: n.fa, label: "f_a", color: DOMC.warn }, { x: n.fr, label: "f_r", color: DOMC.ink3 }] : [{ x: n.f0, label: "f₀", color: DOMC.warn }];
    plot.set({ ymin: bot, ymax: top, series: s, vlines });
    if (st.key === "two") ro({ fa: hz(n.fa), fr: hz(n.fr) }); else ro({ f0: hz(n.f0), Q: n.Q.toFixed(2) });
  }
  build();
}

/* ===== Crash course bench 2 · read an impedance curve (with a guessing game) ===== */
const ZNET_STORY = {
  srlc: "<b>Series: the largest impedance wins.</b> Low f the spring (1/ωC) is huge, high f the mass (ωL) is; the curve rides the upper asymptote and dips to <b>R</b> exactly where ωL = 1/ωC. A force-driven mass–spring–damper, a Helmholtz bottle, the acoustic loop of every microphone.",
  prlc: "<b>Parallel: the smallest impedance wins.</b> Low f the inductor shorts everything, high f the capacitor does; in between the two cancel and only <b>R</b> is left: a <b>peak</b>. The same resonator as the series one, seen as a node: the mobility analogy, or mechanics seen through a gyrator.",
  spk: "<b>A floor plus a peak.</b> R₂ in series sets the floor at both ends; the parallel tank lifts it to R₂ + R at resonance. This is the loudspeaker's input impedance: R<sub>e</sub> plus the mechanics turned upside down by (Bl)² (lecture 4, Lab D).",
  rlpc: "<b>Rise, peak, fall.</b> Low f: R, then ωL takes over (rising), until the capacitor in parallel becomes smaller and shorts it: an <b>anti-resonance</b> (peak), then a −20 dB/decade fall. The shaker's 2nd feature in lecture 2, or a coil with winding capacitance.",
  rl: "<b>Flat, then rising.</b> R until ωL = R at f = R/(2πL), then +20 dB/decade. The blocked voice coil (R<sub>e</sub> + jωL<sub>e</sub>) or a lossy tube.",
};
function benchZRead() {
  const b = bench("bench-zread", "Read any impedance curve: series takes the biggest, parallel the smallest", "crash course · reading curves");
  if (!b) return;
  const st = { net: "srlc", dom: "me", v: {}, mystery: null, guessed: false };
  const domSeg = h("div", { class: "seg" });
  for (const [k, d] of Object.entries(ZDOM)) domSeg.append(h("button", { type: "button", class: k === st.dom ? "on" : "", onclick: (e) => { st.dom = k; $$("button", domSeg).forEach(x => x.classList.toggle("on", x === e.target)); st.mystery = null; build(); } }, d.tag));
  const netChips = h("div", { class: "chips" });
  for (const [k, n] of Object.entries(ZNETS)) netChips.append(h("button", { class: "chip" + (k === st.net ? " on" : ""), type: "button", "data-k": k, onclick: () => pick(k) }, n.name));
  const dice = h("button", { class: "btn", type: "button" }, "🎲 mystery network: guess it");
  dice.addEventListener("click", roll);
  const verdict = h("div", { class: "small" });
  b.ctl.append(domSeg, netChips, dice, verdict);
  const sbox = h("div", {}); b.ctl.append(sbox);
  const ro = readouts(b.ctl, [{ id: "f0", label: "where reactances cross" }, { id: "lo", label: "slope at the low end" }, { id: "hi", label: "slope at the high end" }]);
  const pm = new Plot(b.plot, { h: 260, ymin: -20, ymax: 60, ylabel: "|Z|  (dB re 1 unit)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const pp = new Plot(b.plot, { h: 140, ymin: -90, ymax: 90, yticks: [-90, -45, 0, 45, 90], ylabel: "phase (°)", yfmt: v => v.toFixed(0) + "°" });
  function pick(k) {
    if (st.mystery && !st.guessed) {   // a guess
      st.guessed = true;
      const ok = k === st.mystery;
      verdict.innerHTML = `<p style="max-width:none">${ok ? "✓ <b>Right.</b>" : `✗ It was <b>${ZNETS[st.mystery].name}</b>.`} Asymptotes now shown, sliders unlocked.</p>`;
      st.net = st.mystery;
      $$(".chip", netChips).forEach(c => c.classList.toggle("on", c.dataset.k === st.net));
      build(true); return;
    }
    st.mystery = null; st.net = k;
    $$(".chip", netChips).forEach(c => c.classList.toggle("on", c.dataset.k === k));
    verdict.innerHTML = ""; build();
  }
  function roll() {
    const keys = Object.keys(ZNETS); st.mystery = keys[Math.floor(Math.random() * keys.length)]; st.guessed = false;
    const D = ZDOM[st.dom];
    for (const e of ["R", "R2", "L", "C"]) { const [, , lo, hi] = D[e]; const sc = D[e][5] || 1; st.v[e] = Math.pow(10, Math.log10(lo) + (0.2 + 0.6 * Math.random()) * (Math.log10(hi) - Math.log10(lo))) * sc; }
    $$(".chip", netChips).forEach(c => c.classList.remove("on"));
    verdict.innerHTML = `<p style="max-width:none"><b>Which network made this curve?</b> Click one of the chips above. Read the two ends first (which slope?), then the middle (peak or dip? down to what?).</p>`;
    sbox.innerHTML = ""; upd();
  }
  function build(keep) {
    const D = ZDOM[st.dom], n = ZNETS[st.net];
    if (!keep) for (const e of ["R", "R2", "L", "C"]) st.v[e] = D[e][4] * (D[e][5] || 1);
    sbox.innerHTML = "";
    for (const e of n.els) { const [lab, unit, lo, hi] = D[e], sc = D[e][5] || 1; slider(sbox, { label: `<b>${lab}</b>`, min: lo, max: hi, value: st.v[e] / sc, log: true, unit, dom: st.dom, onchange: v => { st.v[e] = v * sc; upd(); } }); }
    upd();
  }
  function upd() {
    const D = ZDOM[st.dom], key = st.mystery || st.net, n = ZNETS[key], hide = st.mystery && !st.guessed;
    const fs = logspace(10, 20000, 360), Z = fs.map(f => n.Z(f, st.v));
    const curve = fs.map((f, i) => [f, dB(cabs(Z[i]))]);
    const asym = [];
    if (!hide) {
      if (n.els.includes("L")) asym.push({ name: "ωL line (mass)", color: DOMC.el, thin: true, dash: "5 4", pts: fs.map(f => [f, dB(TAU * f * st.v.L)]) });
      if (n.els.includes("C")) asym.push({ name: "1/ωC line (spring)", color: DOMC.ac, thin: true, dash: "5 4", pts: fs.map(f => [f, dB(1 / (TAU * f * st.v.C))]) });
      asym.push({ name: "R", color: DOMC.ink3, thin: true, dash: "2 3", pts: fs.map(f => [f, dB(st.v.R)]) });
      if (n.els.includes("R2")) asym.push({ name: "R₂", color: DOMC.ink3, thin: true, dash: "2 3", pts: fs.map(f => [f, dB(st.v.R2)]) });
    }
    const ys = curve.map(p => p[1]);
    const top = Math.ceil((Math.max(...ys) + 10) / 10) * 10, bot = Math.min(Math.floor((Math.min(...ys) - 10) / 10) * 10, top - 40);
    pm.set({ ymin: Math.max(bot, top - 120), ymax: top, ylabel: `|Z|  (dB re 1 ${D.unit})`, series: [...asym, { name: "|Z|", color: DOMC[st.dom], width: 3, pts: curve }] });
    pp.set({ series: [{ name: "phase", color: DOMC[st.dom], pts: fs.map((f, i) => [f, carg(Z[i])]) }] });
    const slope = (i, j) => (ys[j] - ys[i]) / Math.log10(fs[j] / fs[i]);
    const lo = slope(0, 10), hi = slope(349, 359);
    const sl = (s) => `${s >= 0 ? "+" : ""}${s.toFixed(0)} dB/dec ${Math.abs(s) < 4 ? "(flat: R)" : s > 0 ? "(mass-like)" : "(spring-like)"}`;
    const f0 = n.els.includes("C") ? 1 / (TAU * Math.sqrt(st.v.L * st.v.C)) : st.v.R / (TAU * st.v.L);
    ro({ f0: hide ? "?" : hz(f0), lo: sl(lo), hi: sl(hi) });
    b.note.innerHTML = hide
      ? `<p>The ends tell you which element dominates there: <b>+20 dB/decade</b> and +90° is a mass (jω), <b>−20 dB/decade</b> and −90° a spring (1/jω), flat and 0° a resistor. A <b>dip</b> means a series resonance (reactances cancel, only R left), a <b>peak</b> a parallel one.</p>`
      : `<p>${ZNET_STORY[key]}</p><p class="muted">Dashed lines: each element's own impedance. Every |Z| curve is built from these straight lines: in series follow the biggest, in parallel follow the smallest, and where two lines cross with opposite slopes there is a resonance. The units change with the domain tab; the shapes never do.</p>`;
  }
  build();
}

/* ===== Crash course bench 3 · crossing a transducer: S keeps the type, Bl flips it ===== */
function benchCross() {
  const b = bench("bench-cross", "Cross a transducer: what does each element turn into?", "crash course · S and Bl · 315 SWR of Problems 7");
  if (!b) return;
  const st = { el: "mass", Bl: 11.6, S: 519e-4 };
  const chips = h("div", { class: "chips" });
  for (const [k, e] of Object.entries(CROSS_ELS)) chips.append(h("button", { class: "chip" + (k === st.el ? " on" : ""), type: "button", html: e.name, onclick: (ev) => { st.el = k; $$(".chip", chips).forEach(c => c.classList.toggle("on", c === ev.currentTarget)); upd(); } }));
  b.ctl.append(chips);
  slider(b.ctl, { label: "force factor <b>Bl</b> (gyrator)", min: 1, max: 25, step: 0.1, value: 11.6, unit: "T·m", dom: "el", onchange: v => { st.Bl = v; upd(); } });
  slider(b.ctl, { label: "diaphragm area <b>S<sub>D</sub></b> (transformer)", min: 10, max: 1200, step: 1, value: 519, unit: "cm²", dom: "ac", onchange: v => { st.S = v * 1e-4; upd(); } });
  const ro = readouts(b.ctl, [{ id: "ac", label: "acoustic side (÷S² or ×S²)", dom: "ac" }, { id: "me", label: "mechanical side", dom: "me" }, { id: "el", label: "electrical side, (Bl)²/Z_M", dom: "el" }]);
  const stage = h("div", {}); b.plot.append(stage);
  const plot = new Plot(b.plot, { h: 220, xmin: 10, xmax: 2000, ymin: -40, ymax: 40, ylabel: "|Z| re its value at 100 Hz (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const KIND = { L: ["jω element", IND], C: ["1/jω element", CAP], R: ["real element", RES] };
  const fmt = (dom, kind, v) => {
    if (dom === "el") return kind === "L" ? `L = ${sci(v * 1e3)} mH` : kind === "C" ? `C = ${sci(v * 1e3)} mF` : `R = ${sci(v)} Ω`;
    if (dom === "me") return kind === "L" ? `M_M = ${sci(v * 1e3)} g` : kind === "C" ? `C_M = ${sci(v * 1e3)} mm/N` : `R_M = ${sci(v)} Ns/m`;
    return kind === "L" ? `M_A = ${sci(v)} kg/m⁴` : kind === "C" ? `C_A = ${sci(v)} m⁵/N` : `R_A = ${sci(v)} Pa·s/m³`;
  };
  function upd() {
    const e = CROSS_ELS[st.el], v = crossValues(e, st.Bl, st.S);
    const card = (x, col, title, kind, txt) => {
      const [kname, draw] = KIND[kind];
      return `<g transform="translate(${x} 0)"><rect x="0" y="6" width="190" height="128" rx="6" fill="${col.replace(")", "-soft)")}" stroke="${col}" stroke-width="1.4"/>
        ${CK.label(95, 28, title, col, "middle", 13)}${draw(55, 70, 135, 70, col, "")}${CK.wire(20, 70, 55, 70, col)}${CK.wire(135, 70, 170, 70, col)}
        ${CK.label(95, 104, txt, DOMC.ink, "middle", 12)}${CK.label(95, 122, kname, DOMC.ink2, "middle", 10.5)}</g>`;
    };
    const arrow = (x, top, bot) => `<path d="M${x} 62 h36 M${x + 30} 57 l6 5 -6 5 M${x + 36} 82 h-36 M${x + 6} 77 l-6 5 6 5" fill="none" stroke="var(--ink-2)" stroke-width="1.4"/>${CK.label(x + 18, 50, top, DOMC.ink2, "middle", 10.5)}${CK.label(x + 18, 100, bot, DOMC.ink2, "middle", 10.5)}`;
    stage.innerHTML = `<div class="circuit">${svgWrap(660, 140, [
      card(0, DOMC.el, "electrical", v.el.kind, fmt("el", v.el.kind, v.el.v)), arrow(196, "Bl", "gyrator"),
      card(238, DOMC.me, "mechanical", e.kind, fmt("me", e.kind, v.me)), arrow(434, "S_D", "transformer"),
      card(470, DOMC.ac, "acoustical", e.kind, fmt("ac", e.kind, v.ac)),
    ].join(""))}<div class="cap">start: ${e.start === "me" ? "mechanical" : "acoustical"} · ${e.kind === v.el.kind ? "the gyrator keeps a resistor a resistor" : "the gyrator swaps L ↔ C"}</div></div>`;
    const fs = logspace(10, 2000, 200), rel = (kind, f) => kind === "L" ? dB(f / 100) : kind === "C" ? dB(100 / f) : 0;
    plot.set({ series: [
      { name: "acoustical", color: DOMC.ac, width: 5, pts: fs.map(f => [f, rel(e.kind, f)]) },
      { name: "mechanical", color: DOMC.me, pts: fs.map(f => [f, rel(e.kind, f)]) },
      { name: "electrical", color: DOMC.el, pts: fs.map(f => [f, rel(v.el.kind, f)]) }] });
    ro({ ac: fmt("ac", e.kind, v.ac), me: fmt("me", e.kind, v.me), el: fmt("el", v.el.kind, v.el.v) });
    const why = { L: "A mass becomes a <b>capacitor</b> C = M/(Bl)² at the terminals: the heavier the cone, the bigger the capacitor, the lower its impedance at high frequency. That is why the motional peak falls away on the right like a capacitor.", C: "A compliance becomes an <b>inductor</b> L = (Bl)²·C<sub>M</sub>: a soft suspension is a big inductor. Below resonance the terminals see this inductor shunting the peak.", R: "A damper becomes a resistor <b>R = (Bl)²/R<sub>M</sub></b>: <i>less</i> mechanical damping gives a <i>bigger</i> electrical resistor, which is why a lightly damped driver has a tall impedance peak (Lab D: 117 Ω on the 26W)." }[e.kind];
    b.note.innerHTML = `<p><b>Transformer (S):</b> <span class="mono">f = S·p, U = S·u</span> → <span class="mono">Z_M = S²·Z_A</span>. Same kind of element on both sides, only scaled: a box stays a spring, an air load stays a mass. <b>Gyrator (Bl):</b> <span class="mono">f = Bl·i, v = Bl·u</span> → <span class="mono">Z_E = (Bl)²/Z_M</span>. Dividing by Z flips jω into 1/jω, so series turns parallel and L swaps with C. On the plot the acoustical and mechanical lines lie on top of each other; the electrical one is the mirror image.</p><p>${why}</p><p class="muted">Try the box: 30 L of air is a mechanical spring of ${sci(crossValues(CROSS_ELS.box, st.Bl, st.S).me * 1e3)} mm/N at the cone, stiffer than the 0.55 mm/N suspension (that ratio is the α of lecture 8), and an inductor at the terminals.</p>`;
  }
  upd();
}

/* ===== L10 bench · the lumped ear drum (slide 2) ===== */
function benchEarDrum() {
  const b = bench("bench-eardrum", "A real boundary: the ear drum as two R-L-C branches", "lecture 10 · slide 2");
  if (!b) return;
  const st = { k1: 1, k2: 1 };
  slider(b.ctl, { label: "damping of branch 1 (× R₁ = 50.6 MΩ)", min: 0.1, max: 3, step: 0.05, value: 1, unit: "×", dom: "ac", fmt: v => v.toFixed(2), onchange: v => { st.k1 = v; upd(); } });
  slider(b.ctl, { label: "damping of branch 2 (× R₂ = 31.1 MΩ)", min: 0.1, max: 3, step: 0.05, value: 1, unit: "×", dom: "ac", fmt: v => v.toFixed(2), onchange: v => { st.k2 = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "f1", label: "branch 1: f₁, Q₁", dom: "ac" }, { id: "f2", label: "branch 2: f₂, Q₂", dom: "ac" }, { id: "z20", label: "|Z| at 20 Hz" }, { id: "V", label: "equivalent volume (C₁+C₂)ρc²" }]);
  const pm = new Plot(b.plot, { h: 240, xmin: 20, xmax: 20000, ymin: 150, ymax: 200, ylabel: "|Z_ED|  (dB re 1 Pa·s/m³)", yfmt: v => v.toFixed(1), yunit: " dB" });
  const pp = new Plot(b.plot, { h: 140, xmin: 20, xmax: 20000, ymin: -90, ymax: 90, yticks: [-90, -45, 0, 45, 90], ylabel: "phase (°)", yfmt: v => v.toFixed(0) + "°" });
  function upd() {
    const br = EAR_BRANCHES.map((x, i) => ({ ...x, R: x.R * (i ? st.k2 : st.k1) }));
    const fs = logspace(20, 20000, 400), Z = fs.map(f => earDrum(f, br));
    const fr = br.map(x => 1 / (TAU * Math.sqrt(x.L * x.C))), Q = br.map(x => Math.sqrt(x.L / x.C) / x.R);
    pm.set({ series: [{ name: "|Z_ED|", color: DOMC.ac, pts: fs.map((f, i) => [f, dB(cabs(Z[i]))]) }, { name: "stiffness only, 1/ω(C₁+C₂)", color: DOMC.ink3, thin: true, dash: "5 4", pts: fs.map(f => [f, dB(1 / (TAU * f * (br[0].C + br[1].C)))]) }],
      vlines: [{ x: fr[0], label: "f₁", color: DOMC.warn }, { x: fr[1], label: "f₂", color: DOMC.warn }] });
    pp.set({ series: [{ name: "phase", color: DOMC.ac, pts: fs.map((f, i) => [f, carg(Z[i])]) }] });
    ro({ f1: `${hz(fr[0])}, ${Q[0].toFixed(2)}`, f2: `${hz(fr[1])}, ${Q[1].toFixed(2)}`, z20: `${sci(cabs(earDrum(20, br)))} Pa·s/m³`, V: `${((br[0].C + br[1].C) * RHO * C0 * C0 * 1e6).toFixed(2)} cm³` });
  }
  upd();
  b.note.innerHTML = `<p>Lumped models assume sound-hard walls. A real boundary is not hard, so you <b>terminate the circuit with its surface impedance</b>. Here: two series R-L-C branches in parallel (the slide's values). Below 1 kHz it is just a spring, about half a cubic centimetre of air (phase −90°, −20 dB/decade on the dashed line). The two broad dips are the branch resonances at 1.19 and 3.50 kHz (Q 1.39 and 0.70), and above them the phase turns positive: mass-controlled.</p><p><b>Try:</b> lower branch 1's damping to 0.2×: a sharp dip appears at 1.19 kHz. Each branch is one series resonator, and in parallel the one whose impedance is <i>lowest</i> takes over (the reading rule of the crash course).</p>`;
}

/* ===== L10 bench · the five-layer wall, three ways (slides 4–9) ===== */
function benchWall() {
  const b = bench("bench-wall", "Five-layer wall: lumped, mixed and transfer-matrix models side by side", "lecture 10 · slides 4–9");
  if (!b) return;
  const st = { ins: 3, gap: 1, show: { lem: true, mixed: true, tmm: true } };
  slider(b.ctl, { label: "insulation thickness", min: 0.5, max: 10, step: 0.5, value: 3, unit: "cm", dom: "ac", onchange: v => { st.ins = v; upd(); } });
  slider(b.ctl, { label: "air-gap thickness", min: 0.2, max: 5, step: 0.1, value: 1, unit: "cm", dom: "ac", onchange: v => { st.gap = v; upd(); } });
  const chips = h("div", { class: "chips" });
  for (const [k, l] of [["lem", "LEM (all lumped)"], ["mixed", "mixed: masses + lines"], ["tmm", "TMM (all lines)"]]) chips.append(h("button", { class: "chip on", type: "button", onclick: (e) => { st.show[k] = !st.show[k]; e.target.classList.toggle("on", st.show[k]); upd(); } }, l));
  b.ctl.append(chips);
  const ro = readouts(b.ctl, [{ id: "ml", label: "mass law at 20 Hz, m'' = Σρl" }, { id: "p1", label: "1st peak: hand / LEM / TMM" }, { id: "p2", label: "2nd peak: hand / LEM / TMM" }, { id: "p2c", label: "2nd, ⅓ insulation mass added" }, { id: "dev", label: "LEM vs TMM, worst below 1 kHz" }]);
  const plot = new Plot(b.plot, { h: 320, xmin: 20, xmax: 20000, ymin: -200, ymax: 0, ylabel: "transmission |p_out / p_in|  (dB)", yfmt: v => v.toFixed(1), yunit: " dB" });
  function upd() {
    const layers = WALL_LAYERS.map(L => ({ ...L }));
    layers[1].l = st.ins / 100; layers[3].l = st.gap / 100;
    const fs = logspace(20, 20000, 700);
    const cur = { lem: fs.map(f => dB(cabs(wallT(f, layers, "lem")))), mixed: fs.map(f => dB(cabs(wallT(f, layers, "mixed")))), tmm: fs.map(f => dB(cabs(wallT(f, layers, "tmm")))) };
    const col = { lem: DOMC.el, mixed: DOMC.me, tmm: DOMC.ac }, nm = { lem: "LEM", mixed: "mixed", tmm: "TMM" };
    const series = Object.keys(cur).filter(k => st.show[k]).map(k => ({ name: nm[k], color: col[k], width: k === "tmm" ? 4 : 1.8, pts: fs.map((f, i) => [f, cur[k][i]]) }));
    const hp = wallLumpedPeaks(layers), pl = wallPeaks(layers, "lem"), pt = wallPeaks(layers, "tmm");
    const ml = dB(L10_AIR.rho * L10_AIR.c / (TAU * 20 * hp.m));
    const dev = Math.max(...fs.map((f, i) => f <= 1000 ? Math.abs(cur.lem[i] - cur.tmm[i]) : 0));
    const half = layers.filter(L => L.soft).map(L => L.c / (2 * L.l));
    plot.set({ series, vlines: [{ x: half[0], label: "ins.", color: DOMC.ink3 }, ...(half[1] < 20000 ? [{ x: half[1], label: "gap", color: DOMC.ink3 }] : [])] });
    ro({ ml: `${ml.toFixed(1)} dB (m'' = ${hp.m.toFixed(0)} kg/m²)`, p1: `${hz(hp.fA)} / ${pl[0] ? hz(pl[0]) : "–"} / ${pt[0] ? hz(pt[0]) : "–"}`, p2: `${hz(hp.fB)} / ${pl[1] ? hz(pl[1]) : "–"} / ${pt[1] ? hz(pt[1]) : "–"}`, p2c: hz(hp.fBc), dev: `${dev.toFixed(2)} dB` });
  }
  upd();
  b.note.innerHTML = `<p>Each layer is a two-port; the chain is one matrix product and <span class="mono">p_out/p_in = 1/(A + B/ρ₀c₀)</span>. <b>LEM</b>: stiff layers are series masses ρl, soft ones shunt compliances l/ρc². <b>TMM</b>: every layer is an exact transmission line. <b>Mixed</b>: masses lumped, soft layers as lines. Start values = the slide: 20 Hz at −31.4 dB (mass law), peaks at 189 Hz (all three), 2731 Hz (LEM) vs 2393 Hz (TMM), then insulation thickness resonances near 9 and 17 kHz that only the line models have.</p><p><b>Why the mixed model is enough:</b> the stiff layers' own thickness resonances (c/2l = 300, 36, 100 kHz) are far above the band, so they may stay lumped. The insulation weighs as much as the drywall and resonates at 8.3 kHz, so it must be a line. <b>Try:</b> thicken the insulation to 8 cm and watch the LEM drift off below 1 kHz; thin it to 1 cm and LEM and TMM agree almost to 5 kHz.</p>`;
}

/* ===== L10 bench · band gaps: Bragg vs local resonance (slide 18) ===== */
function benchMeta() {
  const b = bench("bench-meta", "Band gaps: a mass-spring chain, and one with resonators inside", "lecture 10 · slides 17–18");
  if (!b) return;
  const st = { mu: 1, OR: 0.5 };
  slider(b.ctl, { label: "resonator mass ratio <b>μ = m<sub>R</sub>/m</b>", min: 0.05, max: 5, step: 0.05, value: 1, dom: "me", fmt: v => v.toFixed(2), onchange: v => { st.mu = v; upd(); } });
  slider(b.ctl, { label: "resonator tuning <b>ω<sub>R</sub>/ω₀</b>", min: 0.1, max: 1.8, step: 0.01, value: 0.5, dom: "me", fmt: v => v.toFixed(2), onchange: v => { st.OR = v; upd(); } });
  const ro = readouts(b.ctl, [{ id: "bragg", label: "Bragg gap starts at", dom: "me" }, { id: "gap", label: "local-resonance gap", dom: "me" }, { id: "rel", label: "relative width" }]);
  const pd = new Plot(b.plot, { h: 280, xlog: false, xmin: 0, xmax: 1, ymin: 0, ymax: 2.6, xlabel: "wavenumber kd/π  (1 = edge of the Brillouin zone)", ylabel: "ω / ω₀", xfmt: v => v.toFixed(2), yfmt: v => v.toFixed(3) });
  const pm = new Plot(b.plot, { h: 170, xlog: false, xmin: 0, xmax: 2.6, ymin: -6, ymax: 6, xlabel: "ω / ω₀", ylabel: "m_eff / m", xfmt: v => v.toFixed(2), yfmt: v => v.toFixed(2) });
  function upd() {
    const ks = linspace(0.001, 1, 240);
    const br = ks.map(k => resonantW(k * Math.PI, st.mu, st.OR));
    const g = resonantGap(st.mu, st.OR);
    const flat = (y, name, color) => ({ name, color, thin: true, dash: "4 4", pts: [[0, y], [1, y]] });
    pd.set({ series: [
      { name: "plain chain 2|sin(kd/2)|", color: DOMC.ink3, pts: ks.map(k => [k, braggW(k * Math.PI)]) },
      { name: "with resonators, lower branch", color: DOMC.me, width: 2.6, pts: ks.map((k, i) => [k, br[i][0]]) },
      { name: "upper branch", color: DOMC.ac, width: 2.6, pts: ks.map((k, i) => [k, br[i][1]]) },
      flat(g.lo, "gap bottom", DOMC.warn), flat(g.hi, "gap top", DOMC.warn), flat(2, "Bragg limit 2ω₀", DOMC.ink3)] });
    const ws = linspace(0.005, 2.6, 600).filter(w => Math.abs(w - st.OR) > 0.004);
    pm.set({ series: [{ name: "m_eff/m = 1 + μ/(1 − ω²/ω_R²)", color: DOMC.me, pts: ws.map(w => [w, 1 + st.mu / (1 - (w / st.OR) ** 2)]).flatMap((p, i, a) => i && a[i - 1][0] < st.OR && p[0] > st.OR ? [[st.OR, NaN], p] : [p]) }, { name: "0", color: DOMC.ink3, thin: true, pts: [[0, 0], [2.6, 0]] }],
      vlines: [{ x: st.OR, label: "ω_R", color: DOMC.warn }, { x: g.hi, label: "m_eff = 0", color: DOMC.ink3 }] });
    ro({ bragg: "2.000 ω₀ (kd = π)", gap: `${g.lo.toFixed(3)} … ${g.hi.toFixed(3)} ω₀`, rel: `${(200 * (g.hi - g.lo) / (g.hi + g.lo)).toFixed(0)} %` });
  }
  upd();
  b.note.innerHTML = `<p><b>Grey:</b> masses on springs, nothing else. Long waves travel at <span class="mono">c = ω₀d</span>; at <span class="mono">kd = π</span> (wavelength = two cells) the curve flattens at 2ω₀, group velocity zero, and above that nothing propagates: the <b>Bragg</b> gap, which needs cells about half a wavelength long. <b>Coloured:</b> hang a resonator m<sub>R</sub> on a spring inside each mass. Just above ω<sub>R</sub> the resonator moves against the mass and the <b>effective mass turns negative</b> (lower plot): no wave can travel, so a gap opens around ω<sub>R</sub>, from ${"0.484"} to 0.707 ω₀ with the start values (μ = 1, ω<sub>R</sub> = 0.5 ω₀).</p><p><b>Try:</b> slide ω<sub>R</sub> down to 0.2: the gap follows it to low frequency while the cell size stays the same: a <b>sub-wavelength</b> band gap, the whole point of metamaterials. Raise μ and the gap widens (its top is ω<sub>R</sub>√(1+μ)).</p>`;
}

/* ===== boot ===== */
document.addEventListener("DOMContentLoaded", () => {
  benchRecipe(); benchZRead(); benchCross();
  benchEarDrum(); benchWall(); benchMeta();
});
