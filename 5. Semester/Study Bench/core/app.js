/* The Analogy Bench — core: maths, plots, circuit drawing, page plumbing.
   The benches themselves (one per interactive playground) live in benches.js. */
"use strict";

/* ---------- constants & small maths ---------- */
const RHO = 1.18, C0 = 344, EPS0 = 8.85e-12;
const TAU = 2 * Math.PI;

const cx = (re, im = 0) => ({ re, im });
const cadd = (a, b) => cx(a.re + b.re, a.im + b.im);
const csub = (a, b) => cx(a.re - b.re, a.im - b.im);
const cmul = (a, b) => cx(a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re);
const cinv = (a) => { const d = a.re * a.re + a.im * a.im; return cx(a.re / d, -a.im / d); };
const cdiv = (a, b) => cmul(a, cinv(b));
const cabs = (a) => Math.hypot(a.re, a.im);
const carg = (a) => Math.atan2(a.im, a.re) * 180 / Math.PI;
const cscale = (a, k) => cx(a.re * k, a.im * k);
const par = (a, b) => cinv(cadd(cinv(a), cinv(b)));
const jw = (f) => cx(0, TAU * f);
const ZL = (f, L) => cx(0, TAU * f * L);
const ZC = (f, C) => cx(0, -1 / (TAU * f * C));
const ZR = (R) => cx(R, 0);
const dB = (x) => 20 * Math.log10(Math.max(x, 1e-300));

const SUP = { "-": "⁻", "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹" };
function sci(x, d = 3) {
  if (!isFinite(x)) return "∞";
  if (x === 0) return "0";
  const ax = Math.abs(x);
  if (ax >= 1e-2 && ax < 1e5) {
    const s = Number(x.toPrecision(d));
    return String(s);
  }
  const e = Math.floor(Math.log10(ax));
  const m = x / Math.pow(10, e);
  return `${Number(m.toPrecision(d))}×10${String(e).split("").map(c => SUP[c]).join("")}`;
}
function hz(f) {
  if (f >= 1000) return `${Number((f / 1000).toPrecision(3))} kHz`;
  return `${Number(f.toPrecision(3))} Hz`;
}
function logspace(a, b, n) {
  const out = [], la = Math.log10(a), lb = Math.log10(b);
  for (let i = 0; i < n; i++) out.push(Math.pow(10, la + (lb - la) * i / (n - 1)));
  return out;
}
function linspace(a, b, n) {
  const out = [];
  for (let i = 0; i < n; i++) out.push(a + (b - a) * i / (n - 1));
  return out;
}
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
function h(tag, attrs = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") el.className = v;
    else if (k === "html") el.innerHTML = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v);
  }
  for (const kid of kids) if (kid != null) el.append(kid);
  return el;
}
const DOMC = { el: "var(--el)", me: "var(--me)", ac: "var(--ac)", ink: "var(--ink)", ink2: "var(--ink-2)", ink3: "var(--ink-3)", warn: "var(--warn)" };

/* small complex linear solver (Gaussian elimination, partial pivoting) */
function csolve(A, b) {
  const n = b.length, M = A.map((r, i) => r.map(v => ({ ...v })).concat([{ ...b[i] }]));
  for (let c = 0; c < n; c++) {
    let p = c; for (let r = c + 1; r < n; r++) if (cabs(M[r][c]) > cabs(M[p][c])) p = r;
    [M[c], M[p]] = [M[p], M[c]];
    const piv = M[c][c];
    for (let r = c + 1; r < n; r++) { const f = cdiv(M[r][c], piv); for (let k = c; k <= n; k++) M[r][k] = csub(M[r][k], cmul(f, M[c][k])); }
  }
  const x = Array(n);
  for (let r = n - 1; r >= 0; r--) { let s = M[r][n]; for (let k = r + 1; k < n; k++) s = csub(s, cmul(M[r][k], x[k])); x[r] = cdiv(s, M[r][r]); }
  return x;
}
/* ---------- special functions for the piston radiation impedance ---------- */
function besselJ1(x) {
  // power series — fine up to x ≈ 12 in double precision
  let term = x / 2, sum = term, m = 0;
  while (m < 60) {
    m++;
    term *= -(x * x / 4) / (m * (m + 1));
    sum += term;
    if (Math.abs(term) < 1e-16 * Math.abs(sum)) break;
  }
  return sum;
}
function struveH1(x) {
  // H1(x) = Σ (-1)^m (x/2)^(2m+2) / (Γ(m+3/2) Γ(m+5/2))
  const g15 = Math.sqrt(Math.PI) / 2; // Γ(1.5)
  let g1 = g15, g2 = 1.5 * g15;     // Γ(m+1.5), Γ(m+2.5) for m=0
  let pw = Math.pow(x / 2, 2), sum = 0, m = 0;
  while (m < 80) {
    const term = ((m % 2) ? -1 : 1) * pw / (g1 * g2);
    sum += term;
    if (Math.abs(term) < 1e-16 * Math.abs(sum) && m > 2) break;
    m++;
    g1 *= (m + 0.5); g2 *= (m + 1.5);
    pw *= (x * x / 4);
  }
  return sum;
}
/* exact normalised radiation impedance of a baffled piston, Z / (ρc/S) */
function pistonZnorm(ka) {
  if (ka < 1e-6) return cx(0, 0);
  return cx(1 - besselJ1(2 * ka) / ka, struveH1(2 * ka) / ka);
}
/* Beranek's lumped fit for the same thing (absolute, Pa·s/m³) */
function pistonZlumped(f, a) {
  const S = Math.PI * a * a;
  const MA1 = 8 * RHO / (3 * Math.PI * Math.PI * a);
  const RA1 = 0.441 * RHO * C0 / S, RA2 = RHO * C0 / S;
  const CA1 = 5.94 * a * a * a / (RHO * C0 * C0);
  return par(ZL(f, MA1), cadd(ZR(RA2), par(ZR(RA1), ZC(f, CA1))));
}

/* ---------- Plot: SVG line chart with log/linear axes and a hover layer ---------- */
class Plot {
  constructor(container, opts) {
    this.c = container;
    this.o = Object.assign({
      w: 640, h: 300, ml: 54, mr: 16, mt: 14, mb: 36,
      xlog: true, xmin: 10, xmax: 20000, ymin: -40, ymax: 20,
      xlabel: "frequency", ylabel: "", xfmt: hz, yfmt: (y) => Number(y.toPrecision(3)),
      xticks: null, yticks: null, series: [], markers: [], regions: [], vlines: [],
    }, opts);
    this.wrap = h("div", { class: "plot" });
    this.legend = h("div", { class: "plot-legend" });
    this.c.append(this.wrap, this.legend);
    this.render();
  }
  x(v) { const o = this.o, a = o.xlog ? Math.log10(v) : v, lo = o.xlog ? Math.log10(o.xmin) : o.xmin, hi = o.xlog ? Math.log10(o.xmax) : o.xmax; return o.ml + (a - lo) / (hi - lo) * (o.w - o.ml - o.mr); }
  y(v) { const o = this.o; const t = (v - o.ymin) / (o.ymax - o.ymin); return o.mt + (1 - Math.max(-0.05, Math.min(1.05, t))) * (o.h - o.mt - o.mb); }
  set(patch) { Object.assign(this.o, patch); this.render(); }
  ticksX() {
    const o = this.o;
    if (o.xticks) return o.xticks;
    if (!o.xlog) { const n = 6, s = (o.xmax - o.xmin) / n; return linspace(o.xmin, o.xmax, n + 1).map(v => ({ v, l: o.xfmt(v) })); }
    const out = [];
    for (let d = Math.floor(Math.log10(o.xmin)); d <= Math.ceil(Math.log10(o.xmax)); d++) {
      for (const m of [1, 2, 5]) { const v = m * Math.pow(10, d); if (v >= o.xmin * 0.999 && v <= o.xmax * 1.001) out.push({ v, l: m === 1 || m === 2 || m === 5 ? o.xfmt(v) : "", minor: m !== 1 }); }
    }
    return out;
  }
  ticksY() {
    const o = this.o;
    if (o.yticks) return o.yticks.map(v => ({ v, l: o.yfmt(v) }));
    const span = o.ymax - o.ymin, raw = span / 5, p = Math.pow(10, Math.floor(Math.log10(raw)));
    const step = [1, 2, 2.5, 5, 10].map(k => k * p).find(s => span / s <= 7) || p * 10;
    const out = [];
    for (let v = Math.ceil(o.ymin / step) * step; v <= o.ymax + 1e-9; v += step) out.push({ v: Number(v.toFixed(10)), l: o.yfmt(Number(v.toFixed(10))) });
    return out;
  }
  render() {
    const o = this.o, X = (v) => this.x(v), Y = (v) => this.y(v);
    const parts = [];
    parts.push(`<svg viewBox="0 0 ${o.w} ${o.h}" role="img" aria-label="${o.ylabel} versus ${o.xlabel}">`);
    parts.push(`<defs><clipPath id="clip-${this._id ||= Math.random().toString(36).slice(2)}"><rect x="${o.ml}" y="${o.mt}" width="${o.w - o.ml - o.mr}" height="${o.h - o.mt - o.mb}"/></clipPath></defs>`);
    for (const r of o.regions) {
      const x1 = X(Math.max(r.from, o.xmin)), x2 = X(Math.min(r.to, o.xmax));
      if (x2 > x1) parts.push(`<rect class="region" x="${x1}" y="${o.mt}" width="${x2 - x1}" height="${o.h - o.mt - o.mb}" fill="${r.color}"/><text class="region-lbl" x="${(x1 + x2) / 2}" y="${o.mt + 12}" text-anchor="middle">${r.label || ""}</text>`);
    }
    for (const t of this.ticksX()) parts.push(`<line class="grid" x1="${X(t.v)}" x2="${X(t.v)}" y1="${o.mt}" y2="${o.h - o.mb}" ${t.minor ? 'stroke-dasharray="2 4"' : ""}/>`);
    for (const t of this.ticksY()) parts.push(`<line class="grid" x1="${o.ml}" x2="${o.w - o.mr}" y1="${Y(t.v)}" y2="${Y(t.v)}"/>`);
    parts.push(`<line class="axis" x1="${o.ml}" x2="${o.w - o.mr}" y1="${o.h - o.mb}" y2="${o.h - o.mb}"/><line class="axis" x1="${o.ml}" x2="${o.ml}" y1="${o.mt}" y2="${o.h - o.mb}"/>`);
    for (const t of this.ticksX()) if (t.l) parts.push(`<text x="${X(t.v)}" y="${o.h - o.mb + 14}" text-anchor="middle">${t.l}</text>`);
    for (const t of this.ticksY()) parts.push(`<text x="${o.ml - 6}" y="${Y(t.v) + 3.5}" text-anchor="end">${t.l}</text>`);
    parts.push(`<text class="ttl" x="${(o.ml + o.w - o.mr) / 2}" y="${o.h - 4}" text-anchor="middle">${o.xlabel}</text>`);
    parts.push(`<text class="ttl" transform="translate(12 ${(o.mt + o.h - o.mb) / 2}) rotate(-90)" text-anchor="middle">${o.ylabel}</text>`);
    for (const v of o.vlines) parts.push(`<line x1="${X(v.x)}" x2="${X(v.x)}" y1="${o.mt}" y2="${o.h - o.mb}" stroke="${v.color || DOMC.ink3}" stroke-width="1" stroke-dasharray="5 4"/><text x="${X(v.x) + 4}" y="${o.mt + 11}" fill="${v.color || DOMC.ink3}">${v.label || ""}</text>`);
    parts.push(`<g clip-path="url(#clip-${this._id})">`);
    for (const s of o.series) {
      let d = "", pen = false;
      for (const [px, py] of s.pts) {
        if (!isFinite(py) || px < o.xmin || px > o.xmax) { pen = false; continue; }
        d += (pen ? "L" : "M") + X(px).toFixed(1) + " " + Y(py).toFixed(1); pen = true;
      }
      parts.push(`<path class="series ${s.thin ? "thin" : ""}" d="${d}" stroke="${s.color}" ${s.width ? `stroke-width="${s.width}"` : ""}/>`);
    }
    parts.push(`</g>`);
    for (const m of o.markers) {
      if (m.x < o.xmin || m.x > o.xmax) continue;
      parts.push(`<circle class="marker" cx="${X(m.x)}" cy="${Y(m.y)}" r="4.5" stroke="${m.color || DOMC.ink}"/>`);
      if (m.label) parts.push(`<text x="${X(m.x) + (m.dx ?? 8)}" y="${Y(m.y) + (m.dy ?? -8)}" fill="${m.color || DOMC.ink}" ${m.anchor ? `text-anchor="${m.anchor}"` : ""}>${m.label}</text>`);
    }
    parts.push(`<g class="hover" style="display:none"><line class="cross" y1="${o.mt}" y2="${o.h - o.mb}"/><rect class="tipbox" rx="3"/><text class="tip"></text></g>`);
    parts.push(`<rect class="hit" x="${o.ml}" y="${o.mt}" width="${o.w - o.ml - o.mr}" height="${o.h - o.mt - o.mb}" fill="transparent"/></svg>`);
    this.wrap.innerHTML = parts.join("");
    this.legend.innerHTML = o.series.length > 1 ? o.series.map(s => `<span><i style="background:${s.color}"></i>${s.name}</span>`).join("") : "";
    this.hover();
  }
  hover() {
    const svg = $("svg", this.wrap), hit = $(".hit", svg), g = $(".hover", svg), line = $(".cross", g), box = $(".tipbox", g), txt = $(".tip", g);
    const o = this.o;
    const move = (ev) => {
      const pt = svg.createSVGPoint(); pt.x = ev.clientX; pt.y = ev.clientY;
      const p = pt.matrixTransform(svg.getScreenCTM().inverse());
      const lo = o.xlog ? Math.log10(o.xmin) : o.xmin, hi = o.xlog ? Math.log10(o.xmax) : o.xmax;
      let xv = lo + (p.x - o.ml) / (o.w - o.ml - o.mr) * (hi - lo); if (o.xlog) xv = Math.pow(10, xv);
      const lines = [`${o.xfmt(xv)}`];
      for (const s of o.series) {
        if (!s.pts.length) continue;
        let best = s.pts[0];
        for (const q of s.pts) if (Math.abs(Math.log(q[0]) - Math.log(xv)) < Math.abs(Math.log(best[0]) - Math.log(xv))) best = q;
        if (isFinite(best[1])) lines.push(`${s.name}: ${o.yfmt(best[1])}${o.yunit || ""}`);
      }
      g.style.display = "";
      line.setAttribute("x1", p.x); line.setAttribute("x2", p.x);
      txt.innerHTML = lines.map((l, i) => `<tspan x="0" dy="${i ? 13 : 0}">${l}</tspan>`).join("");
      const bw = Math.max(...lines.map(l => l.length)) * 6.6 + 12, bh = lines.length * 13 + 8;
      const bx = p.x + 12 + bw > o.w - o.mr ? p.x - 12 - bw : p.x + 12, by = Math.min(Math.max(p.y - bh / 2, o.mt), o.h - o.mb - bh);
      box.setAttribute("x", bx); box.setAttribute("y", by); box.setAttribute("width", bw); box.setAttribute("height", bh);
      txt.setAttribute("transform", `translate(${bx + 6} ${by + 13})`);
    };
    hit.addEventListener("mousemove", move);
    hit.addEventListener("mouseleave", () => { g.style.display = "none"; });
  }
}

/* ---------- Polar plot ---------- */
function polarSVG(fn, opts = {}) {
  const w = opts.w || 320, cxp = w / 2, cyp = w / 2, R = w / 2 - 26;
  const parts = [`<svg viewBox="0 0 ${w} ${w}" class="polar" role="img" aria-label="polar pattern">`];
  for (const r of [0.25, 0.5, 0.75, 1]) parts.push(`<circle cx="${cxp}" cy="${cyp}" r="${R * r}" fill="none" stroke="var(--plot-grid)"/>`);
  for (let a = 0; a < 360; a += 30) { const t = a * Math.PI / 180; parts.push(`<line x1="${cxp}" y1="${cyp}" x2="${cxp + R * Math.cos(t)}" y2="${cyp - R * Math.sin(t)}" stroke="var(--plot-grid)"/>`); }
  for (const [a, l] of [[0, "0°"], [90, "90°"], [180, "180°"], [270, "270°"]]) { const t = a * Math.PI / 180; parts.push(`<text x="${cxp + (R + 14) * Math.cos(t)}" y="${cyp - (R + 14) * Math.sin(t) + 4}" text-anchor="middle" font-family="var(--font-mono)" font-size="11" fill="var(--ink-3)">${l}</text>`); }
  for (const [r, l] of [[0.5, "−6 dB"], [1, "0 dB"]]) parts.push(`<text x="${cxp + 3}" y="${cyp - R * r - 3}" font-family="var(--font-mono)" font-size="10" fill="var(--ink-3)">${l}</text>`);
  const curves = Array.isArray(fn) ? fn : [{ fn, color: DOMC.ac }];
  for (const cv of curves) {
    let d = "";
    for (let i = 0; i <= 360; i++) { const t = i * Math.PI / 180, r = Math.min(1, Math.max(0, cv.fn(t))) * R; d += (i ? "L" : "M") + (cxp + r * Math.cos(t)).toFixed(1) + " " + (cyp - r * Math.sin(t)).toFixed(1); }
    parts.push(`<path d="${d}Z" fill="${cv.color}" fill-opacity="${cv.fill ?? 0.12}" stroke="${cv.color}" stroke-width="${cv.width || 2}" ${cv.dash ? `stroke-dasharray="${cv.dash}"` : ""}/>`);
  }
  parts.push(`</svg>`);
  return parts.join("");
}

/* ---------- circuit drawing (SVG strings) ---------- */
/* every element is drawn between two points; horizontal or vertical only */
const CK = {
  wire: (x1, y1, x2, y2, col = DOMC.ink) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="1.6"/>`,
  dot: (x, y, col = DOMC.ink) => `<circle cx="${x}" cy="${y}" r="3" fill="${col}"/>`,
  gnd: (x, y, col = DOMC.ink) => `<g stroke="${col}" stroke-width="1.6"><line x1="${x}" y1="${y}" x2="${x}" y2="${y + 8}"/><line x1="${x - 9}" y1="${y + 8}" x2="${x + 9}" y2="${y + 8}"/><line x1="${x - 5}" y1="${y + 12}" x2="${x + 5}" y2="${y + 12}"/><line x1="${x - 2}" y1="${y + 16}" x2="${x + 2}" y2="${y + 16}"/></g>`,
  label: (x, y, t, col = DOMC.ink, anchor = "middle", size = 12) => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="var(--font-mono)" font-size="${size}" fill="${col}">${t}</text>`,
  note: (x, y, t, col = DOMC.ink2, anchor = "middle") => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="var(--font-body)" font-size="11.5" fill="${col}">${t}</text>`,
};
/* generic two-terminal: draws leads + a body of length 36 centred between p1 and p2 */
function twoT(x1, y1, x2, y2, body, col, label, lpos = 1) {
  const horiz = y1 === y2, len = horiz ? x2 - x1 : y2 - y1, s = Math.sign(len), L = Math.abs(len), B = 40;
  const a = (L - B) / 2;
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
  const out = [];
  if (horiz) { out.push(CK.wire(x1, y1, x1 + s * a, y1, col), CK.wire(x2 - s * a, y2, x2, y2, col)); }
  else { out.push(CK.wire(x1, y1, x1, y1 + s * a, col), CK.wire(x2, y2 - s * a, x2, y2, col)); }
  const rot = horiz ? 0 : 90;
  out.push(`<g transform="translate(${mx} ${my}) rotate(${rot})" stroke="${col}" fill="none" stroke-width="1.6">${body}</g>`);
  if (label) out.push(CK.label(horiz ? mx : mx + 16 * lpos, horiz ? my - 12 * lpos : my + 4, label, col, horiz ? "middle" : (lpos > 0 ? "start" : "end")));
  return out.join("");
}
const BODY = {
  R: `<path d="M-20 0 l4 -7 8 14 8 -14 8 14 8 -14 4 7"/>`,
  L: `<path d="M-20 0 a5 5 0 0 1 10 0 a5 5 0 0 1 10 0 a5 5 0 0 1 10 0 a5 5 0 0 1 10 0"/>`,
  C: `<path d="M-20 0 h16 M4 0 h16 M-4 -10 v20 M4 -10 v20"/>`,
  V: `<circle r="11"/><path d="M-20 0 h9 M11 0 h9 M-4 -0 h8 M0 -4 v8" transform="translate(-4 0) scale(0.7)"/><path d="M4 0 h6" transform="translate(2 0) scale(0.7)"/>`,
  I: `<circle r="11"/><path d="M-20 0 h9 M11 0 h9 M-6 0 h12 M2 -4 l4 4 -4 4"/>`,
  Z: `<rect x="-14" y="-8" width="28" height="16"/><path d="M-20 0 h6 M14 0 h6"/>`,
  E: `<path d="M-20 0 h8 M12 0 h8 M0 -12 l12 12 -12 12 -12 -12z M-4 0 h8 M0 -4 v8"/>`,
  G: `<path d="M-20 0 h8 M12 0 h8 M0 -12 l12 12 -12 12 -12 -12z M-6 0 h12 M2 -4 l4 4 -4 4"/>`,
};
const RES = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.R, col, label, lp);
const IND = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.L, col, label, lp);
const CAP = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.C, col, label, lp);
const VSRC = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.V, col, label, lp);
const ISRC = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.I, col, label, lp);
const ZBOX = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.Z, col, label, lp);
const DEPV = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.E, col, label, lp);
const DEPI = (x1, y1, x2, y2, col, label, lp) => twoT(x1, y1, x2, y2, BODY.G, col, label, lp);
function svgWrap(w, hgt, inner, cls = "") { return `<svg viewBox="0 0 ${w} ${hgt}" class="${cls}" role="img">${inner}</svg>`; }

/* ---------- maths rendering ---------- */
function renderMath(root = document) {
  if (!window.katex) return;
  for (const el of $$(".m, .M", root)) {
    if (el.dataset.done) continue;
    try { katex.render(el.textContent, el, { displayMode: el.classList.contains("M"), throwOnError: false, strict: "ignore" }); el.dataset.done = "1"; }
    catch (e) { /* leave the source visible */ }
  }
}

/* ---------- controls factory ---------- */
function slider(ctl, spec) {
  // spec: {id, label, min, max, step, value, unit, dom, log, fmt}
  const wrap = h("div", { class: `ctl ${spec.dom || ""}` });
  const out = h("output");
  const lab = h("label", {}, h("span", { html: spec.label }), out);
  const inp = h("input", { type: "range", min: spec.log ? Math.log10(spec.min) : spec.min, max: spec.log ? Math.log10(spec.max) : spec.max, step: spec.log ? 0.01 : spec.step, value: spec.log ? Math.log10(spec.value) : spec.value });
  const val = () => spec.log ? Math.pow(10, Number(inp.value)) : Number(inp.value);
  const show = () => { out.textContent = (spec.fmt ? spec.fmt(val()) : sci(val())) + (spec.unit ? " " + spec.unit : ""); };
  inp.addEventListener("input", () => { show(); spec.onchange && spec.onchange(val()); });
  wrap.append(lab, inp); ctl.append(wrap); show();
  return { get: val, set: (v) => { inp.value = spec.log ? Math.log10(v) : v; show(); }, el: wrap };
}
function readouts(ctl, keys) {
  const box = h("div", { class: "readouts" });
  const map = {};
  for (const k of keys) { const v = h("span", { class: `v ${k.dom || ""}` }); box.append(h("div", {}, h("span", { class: "k", html: k.label }), v)); map[k.id] = v; }
  ctl.append(box);
  return (vals) => { for (const [k, v] of Object.entries(vals)) if (map[k]) map[k].textContent = v; };
}
function bench(id, title, eyebrow, opts = {}) {
  const root = document.getElementById(id);
  if (!root) return null;
  root.classList.add("bench");
  const head = h("div", { class: "bench-head" }, h("h4", { html: title }), h("span", { class: "eyebrow", html: eyebrow }));
  const body = h("div", { class: "bench-body" + (opts.one ? " one" : "") });
  const plot = h("div", { class: "bench-plot" });
  const ctl = h("div", { class: "bench-ctl" });
  body.append(plot); if (!opts.one) body.append(ctl);
  const note = h("div", { class: "bench-note" });
  body.append(note);
  root.append(head, body);
  return { root, plot, ctl, note };
}

/* ---------- quiz ---------- */
const PROGRESS_KEY = "analogy-bench-progress";
function loadProgress() { try { return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}"); } catch { return {}; } }
function saveProgress(p) { try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(p)); } catch { } }
function buildQuiz(root, lecture, questions) {
  const prog = loadProgress();
  const box = h("div", { class: "quiz" });
  box.append(h("div", { class: "eyebrow" }, `Check yourself · ${/^\d+$/.test(lecture) ? "lecture" : "lab"} ${lecture}`));
  questions.forEach((q, qi) => {
    const key = `${lecture}.${qi}`;
    const why = h("div", { class: "why", hidden: "" });
    const opts = h("div", { class: "opts" });
    q.a.forEach((txt, ai) => {
      const b = h("button", { class: "opt", type: "button", html: txt });
      b.addEventListener("click", () => {
        $$(".opt", opts).forEach(o => o.classList.remove("right", "wrong"));
        b.classList.add(ai === q.c ? "right" : "wrong");
        if (ai !== q.c) $$(".opt", opts)[q.c].classList.add("right");
        why.innerHTML = (ai === q.c ? "<b>Right.</b> " : "<b>Not quite.</b> ") + q.why; why.hidden = false;
        renderMath(why);
        const p = loadProgress(); p[key] = ai === q.c; saveProgress(p); updateProgress();
      });
      opts.append(b);
    });
    box.append(h("div", { class: "q" }, h("div", { class: "qt", html: `${qi + 1}. ${q.q}` }), opts, why));
    if (prog[key]) { $$(".opt", opts)[q.c].classList.add("right"); }
  });
  root.append(box);
}
let TOTAL_Q = 0;
function updateProgress() {
  const p = loadProgress(), done = Object.values(p).filter(Boolean).length;
  const bar = $(".progress-bar i"), lbl = $(".progress-lbl");
  if (bar) bar.style.width = `${TOTAL_Q ? Math.round(100 * done / TOTAL_Q) : 0}%`;
  if (lbl) lbl.textContent = `${done} / ${TOTAL_Q} checks passed`;
  for (const a of $$(".wire a[data-quiz]")) {
    const lec = a.dataset.quiz, n = Number(a.dataset.n || 0);
    const ok = Array.from({ length: n }, (_, i) => p[`${lec}.${i}`]).every(Boolean) && n > 0;
    a.classList.toggle("done", ok);
  }
}

/* ---------- audio (Helmholtz "hear it") ---------- */
let AC = null;
function beep(f, dur = 1.2) {
  try {
    AC ||= new (window.AudioContext || window.webkitAudioContext)();
    const o = AC.createOscillator(), g = AC.createGain();
    o.type = "sine"; o.frequency.value = f;
    g.gain.setValueAtTime(0, AC.currentTime);
    g.gain.linearRampToValueAtTime(0.25, AC.currentTime + 0.03);
    g.gain.exponentialRampToValueAtTime(0.001, AC.currentTime + dur);
    o.connect(g).connect(AC.destination); o.start(); o.stop(AC.currentTime + dur + 0.05);
  } catch (e) { }
}

/* ---------- page plumbing ---------- */
function setupNav() {
  const links = $$(".wire a");
  const secs = links.map(a => document.getElementById(a.getAttribute("href").slice(1))).filter(Boolean);
  const io = new IntersectionObserver((ents) => {
    for (const e of ents) if (e.isIntersecting) { links.forEach(a => a.classList.toggle("active", a.getAttribute("href") === "#" + e.target.id)); }
  }, { rootMargin: "-20% 0px -70% 0px" });
  secs.forEach(s => io.observe(s));
}
function setupTheme() {
  const btn = $(".theme-btn"); if (!btn) return;
  const root = document.documentElement;
  const apply = (t) => { if (t) root.setAttribute("data-theme", t); else root.removeAttribute("data-theme"); btn.textContent = t === "dark" ? "Theme: dark" : t === "light" ? "Theme: light" : "Theme: system"; };
  let cur = null; try { cur = localStorage.getItem("analogy-bench-theme"); } catch { }
  apply(cur);
  btn.addEventListener("click", () => { cur = cur === null ? "dark" : cur === "dark" ? "light" : null; try { cur ? localStorage.setItem("analogy-bench-theme", cur) : localStorage.removeItem("analogy-bench-theme"); } catch { } apply(cur); });
}
