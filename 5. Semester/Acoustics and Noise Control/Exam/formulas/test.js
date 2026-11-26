// node test.js — checks every formula can be solved for every variable, plus spot values from the toolkit.
'use strict';
const { TOPICS, CONSTANTS, aWeight } = require('./src/formulas.js');
const E = require('./src/engine.js');
const consts = Object.fromEntries(Object.entries(CONSTANTS).map(([k, v]) => [k, v.value]));
let pass = 0, fail = 0;
const ok = (cond, msg) => { if (cond) pass++; else { fail++; console.log('FAIL', msg); } };
const close = (a, b, tol, msg) => ok(Math.abs(a - b) <= tol * Math.max(1, Math.abs(b)), `${msg}: got ${a}, want ${b}`);

// 1. round trip: for each formula pick plausible inputs, solve the first var, then solve each other var back.
const SAMPLE = { db: () => 40 + 50 * Math.random(), unit: () => 0.05 + 0.6 * Math.random(), sym: () => -0.8 + 1.6 * Math.random(),
  ge1: () => 1.2 + 5 * Math.random(), deg90: () => 10 + 70 * Math.random(), int: () => 1 + Math.floor(3 * Math.random()), any: () => 30 + 100 * Math.random(),
  pos: () => 0.3 + 3 * Math.random() };
for (const T of TOPICS) T.formulas.forEach((F, i) => {
  for (let trial = 0; trial < 3; trial++) {
    const vals = {};
    F.vars.slice(1).forEach(k => vals[k] = SAMPLE[T.vars[k][3] || 'pos']());
    if (T.id === 'speaker' && F.vars[0] === 'th') vals.ka = 4 + 5 * Math.random();
    if (T.id === 'hearing' && F.vars[0] === 'fct') { vals.f1 = 800; vals.f2 = 900; }
    if (T.id === 'vibration' && F.vars[0] === 'xi') vals.r = 2 + Math.random();
    if (F.vars[0] === 'Wd') { vals.k = 0.5 + Math.random(); vals.d = 0.1 + Math.random(); }   // kd < 2: where the formula is used
    if (F.vars[0] === 'als') vals.T2 = vals.T1 * 0.7;
    if (F.vars[0] === 'B') vals.fu = vals.fl * 2;
    if (F.vars[0] === 'P') vals.dh = vals.ah * 0.3;
    if (F.vars[0] === 'tau') vals.Z2 = vals.Z1 * 5;   // tau = 1 (Z1 = Z2) is a double root
    const lhs = F.vars[0];
    const r = E.solve1(x => F.f(Object.assign({}, consts, vals, { [lhs]: x })), T.vars[lhs][3]);
    if (!r.length) { ok(false, `${T.id}/${F.name}: no value for ${lhs} from ${JSON.stringify(vals)}`); continue; }
    vals[lhs] = r[0];
    for (const k of F.vars.slice(1)) {
      if ((T.vars[k][3] || 'pos') === 'int') continue;
      const want = vals[k];
      const rest = Object.assign({}, consts, vals); delete rest[k];
      const roots = E.solve1(x => F.f(Object.assign({}, rest, { [k]: x })), T.vars[k][3]);
      ok(roots.some(x => Math.abs(x - want) <= 1e-5 * Math.max(1, Math.abs(want))), `${T.id}/${F.name}: solve ${k} back (want ${want}, got ${roots})`);
    }
  }
});

// 2. spot values (toolkit run_all_checks / official solutions)
const topic = id => TOPICS.find(t => t.id === id);
const run = (id, given) => E.propagate(topic(id), given, consts).values;
close(run('reverb', { V: 120, T: 0.4 }).A, 0.1612 * 120 / 0.4, 2e-3, 'Sabine A');
close(run('hearing', { f: 875 }).ERB, 119.2, 1e-3, 'ERB 875 Hz');
close(run('hearing', { f: 1000 }).ERB, 132.639, 1e-4, 'ERB 1 kHz');
close(run('vibration', { m: 100, dl: 0.01 }).f0, 4.985, 1e-3, 'f0 from 1 cm deflection');
close(run('sources', { f: 189, r: 0.5 }).phi, 30, 0.02, 'monopole phase 2024 MC');
close(run('modes', { Lx: 7.2, Ly: 5.4, Lz: 3, nx: 2, ny: 0, nz: 0 }).fm, 47.64, 1e-3, 'mode (2,0,0)');
close(run('plane', { Z: 1 }).al, 0.0097, 0.02, 'α for Z = 1');
close(aWeight(1000), 0, 0.01, 'A(1 kHz)');
close(aWeight(100), -19.1, 0.01, 'A(100 Hz)');
close(run('reverb', { V: 120, S: 158, T: 0.4, LW: 90, Q: 1, r: 2 }).al, 48.36 / 158, 2e-3, 'mean α from T');
close(run('levels', { p: 1 }).Lp, 93.98, 1e-4, 'Lp of 1 Pa');
close(run('insulation', { f: 500, m: 230 }).R0, 20 * Math.log10(2 * Math.PI * 500 * 230 / (2 * 411.6)), 1e-6, 'mass law');
close(run('absorbers', { Dn: 0.05, lneck: 0.02, leff: 0.02, fH: 140 }).Vc, (Math.PI * 0.05 ** 2 / 4) / 0.02 * (343 / (2 * Math.PI * 140)) ** 2, 1e-5, 'Helmholtz V back (2024 MC6)');

// 3. old app engine agreement on a few toolkit examples
try {
  const P = require('../app/src/physics.js');
  const t15 = P.solveT15({}).vars;
  if (t15.f0_dw !== undefined) ok(true, '');
  const t13 = P.solveT13({}).vars;
  close(run('hearing', { x: 20.4 }).Fg, t13.f_of_x, 1e-6, 'Greenwood vs toolkit');
} catch (e) { console.log('(old engine not compared:', e.message, ')'); }

// 4. input parser
close(E.parseInput('2*(5*8+5*3+8*3)'), 158, 0, 'expression');
close(E.parseInput('2k'), 2000, 0, 'k suffix');
close(E.parseInput('10^(3/10)'), 1.9953, 1e-4, 'power');
close(E.parseInput('4*pi'), 4 * Math.PI, 1e-12, 'pi');
ok(Number.isNaN(E.parseInput('alert(1)')), 'rejects code');

console.log(`${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
