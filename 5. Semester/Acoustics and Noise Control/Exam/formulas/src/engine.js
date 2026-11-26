// Solver: propagate known values through a topic's formulas.
// A formula with exactly one unknown is solved numerically for it (bracket scan + bisection),
// so every quantity can be the unknown without writing inverse formulas by hand.

(function (root) {
  'use strict';

  function grid(domain) {
    const pts = [];
    const logspan = (lo, hi, n) => { for (let i = 0; i <= n; i++) pts.push(10 ** (lo + (hi - lo) * i / n)); };
    switch (domain) {
      case 'db': for (let x = -500; x <= 500; x += 0.25) pts.push(x); break;
      case 'unit': for (let i = 0; i <= 4000; i++) pts.push(i / 4000); logspan(-12, -3.4, 120); break;
      case 'sym': for (let i = -4000; i <= 4000; i++) pts.push(i / 4000); break;
      case 'ge1': logspan(0, 15, 900); break;
      case 'deg90': for (let i = 0; i <= 3600; i++) pts.push(i / 40); break;
      case 'any': {
        const pos = []; for (let i = 0; i <= 1200; i++) pos.push(10 ** (-15 + 30 * i / 1200));
        for (let i = pos.length - 1; i >= 0; i--) pts.push(-pos[i]);
        pts.push(0); pts.push(...pos); break;
      }
      default: logspan(-15, 15, 6000);
    }
    return pts.sort((a, b) => a - b);
  }
  const GRIDS = {};
  const gridFor = d => GRIDS[d] || (GRIDS[d] = grid(d));

  // All roots of g on the domain; poles are rejected.
  function solve1(g, domain) {
    const xs = gridFor(domain || 'pos');
    const ys = xs.map(x => { const y = g(x); return Number.isFinite(y) ? y : NaN; });
    const roots = [];
    for (let i = 0; i < xs.length; i++) {
      if (ys[i] === 0) { roots.push(xs[i]); continue; }
      if (i === 0) continue;
      const ya = ys[i - 1], yb = ys[i];
      if (!Number.isFinite(ya) || !Number.isFinite(yb) || ya === 0 || Math.sign(ya) === Math.sign(yb)) continue;
      let a = xs[i - 1], b = xs[i], fa = ya;
      for (let it = 0; it < 200; it++) {
        const mid = (a + b) / 2;
        if (mid === a || mid === b) break;
        const fm = g(mid);
        if (!Number.isFinite(fm)) { a = NaN; break; }
        if (fm === 0) { a = b = mid; break; }
        if (Math.sign(fm) === Math.sign(fa)) { a = mid; fa = fm; } else b = mid;
      }
      if (!Number.isFinite(a)) continue;
      const x = (a + b) / 2, gx = Math.abs(g(x));
      if (gx <= 1e-6 * Math.max(Math.abs(ya), Math.abs(yb)) || gx < 1e-12) roots.push(x);
    }
    const out = [];
    for (const r of roots) if (!out.some(o => Math.abs(o - r) <= 1e-9 * Math.max(1, Math.abs(r)))) out.push(r);
    return out;
  }

  // Pick the root: closest to a hint if given, else the smallest magnitude.
  function pick(roots, hint) {
    if (!roots.length) return undefined;
    if (hint !== undefined) return roots.reduce((b, r) => Math.abs(r - hint) < Math.abs(b - hint) ? r : b);
    return roots.reduce((b, r) => Math.abs(r) < Math.abs(b) ? r : b);
  }

  // topic: formula topic; given: {key: number}; consts: {key: number}
  // returns { values, info: {key: {from, roots}}, rows: [{solved, mismatch, unknowns}] }
  function propagate(topic, given, consts) {
    const values = Object.assign({}, consts, given);
    const info = {};
    const rows = topic.formulas.map(() => ({ solved: null, mismatch: null, unknowns: [] }));
    const domainOf = k => (topic.vars[k] && topic.vars[k][3]) || 'pos';
    let changed = true, guard = 0, order = 0;
    while (changed && guard++ < 50) {
      changed = false;
      topic.formulas.forEach((F, i) => {
        if (rows[i].solved) return;
        const unk = F.vars.filter(k => !(k in values));
        if (unk.length !== 1) return;
        const key = unk[0];
        if (domainOf(key) === 'int') return;
        const g = x => F.f(Object.assign({}, values, { [key]: x }));
        const roots = solve1(g, domainOf(key));
        if (!roots.length) { rows[i].noSolution = key; return; }
        const x = pick(roots, F.prefer ? F.prefer(values) : undefined);
        values[key] = x;
        info[key] = { from: i, roots, order: order++ };
        rows[i].solved = key;
        changed = true;
      });
    }
    // consistency of formulas where everything is known but nothing was solved from them
    topic.formulas.forEach((F, i) => {
      const unk = F.vars.filter(k => !(k in values));
      rows[i].unknowns = unk;
      if (rows[i].solved || unk.length) return;
      const r0 = F.f(values);
      if (!Number.isFinite(r0)) return;
      // re-solve one given (or computed) variable from the others and compare
      for (const key of F.vars) {
        if (domainOf(key) === 'int') continue;
        const g = x => F.f(Object.assign({}, values, { [key]: x }));
        const roots = solve1(g, domainOf(key));
        if (!roots.length) { rows[i].mismatch = { key, value: undefined }; return; }
        const x = pick(roots, values[key]);
        const ok = Math.abs(x - values[key]) <= 2e-3 * Math.max(Math.abs(x), Math.abs(values[key])) + (domainOf(key) === 'db' ? 0.02 : 1e-12);
        if (!ok) rows[i].mismatch = { key, value: x };
        return;
      }
    });
    return { values, info, rows };
  }

  // Parse a number or a small arithmetic expression: 2*(5*8+5*3), 1.5e-3, 2k, sqrt(2), pi, 10^(3/10)
  function parseInput(raw) {
    if (raw === undefined || raw === null) return undefined;
    let s = String(raw).trim();
    if (!s) return undefined;
    s = s.replace(/,/g, '.').replace(/[×·]/g, '*').replace(/−/g, '-').replace(/π/g, 'pi').replace(/√/g, 'sqrt');
    s = s.replace(/(\d)\s*k\b/g, '$1e3').replace(/(\d)\s*M\b/g, '$1e6');
    const check = s.replace(/\b(sqrt|log10|log|ln|exp|sin|cos|tan|asin|acos|atan|abs|pi)\b/g, '').replace(/[0-9eE.+\-*/()^\s]/g, '');
    if (check.length) return NaN;
    const js = s.replace(/\^/g, '**')
      .replace(/\bpi\b/g, '(Math.PI)')
      .replace(/\bln\(/g, 'Math.log(').replace(/\blog\(/g, 'Math.log10(')
      .replace(/\b(sqrt|log10|exp|sin|cos|tan|asin|acos|atan|abs)\(/g, 'Math.$1(');
    try {
      const v = Function('"use strict";return (' + js + ')')();
      return typeof v === 'number' ? v : NaN;
    } catch (e) { return NaN; }
  }

  function fmt(x, unit) {
    if (x === undefined || x === null || Number.isNaN(x)) return '';
    if (!Number.isFinite(x)) return x > 0 ? '∞' : '−∞';
    if (unit === 'dB' || unit === 'phon' || unit === 'dB/Hz') return (Math.round(x * 100) / 100).toString();
    const ax = Math.abs(x);
    if (ax === 0) return '0';
    if (ax >= 1e6 || ax < 1e-3) {
      const [m, e] = x.toExponential(3).split('e');
      return Number(m).toString() + 'e' + Number(e);
    }
    return Number(x.toPrecision(4)).toString();
  }

  // Plain-text worked line: substitute numbers into the formula's txt.
  function substitute(txt, values, keys) {
    const sorted = keys.slice().sort((a, b) => b.length - a.length);
    const re = new RegExp('\\b(' + sorted.join('|') + ')\\b', 'g');
    return txt.replace(re, k => {
      const s = fmt(values[k]);
      return /^-|e/.test(s) ? '(' + s + ')' : s;
    }).replace(/\*/g, '·').replace(/\bpi\b/g, 'π').replace(/sqrt/g, '√');
  }

  const api = { solve1, propagate, parseInput, fmt, substitute };
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.ENGINE = api;
})(typeof self !== 'undefined' ? self : this);
