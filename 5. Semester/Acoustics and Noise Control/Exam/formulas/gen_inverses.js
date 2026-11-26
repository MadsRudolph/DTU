// node gen_inverses.js > /tmp/.../gen_inverses_run.m ; matlab -batch gen_inverses_run  -> src/inverses.json
// MATLAB's Symbolic Math Toolbox solves every formula for every variable; the branch that
// reproduces a known-good sample point is kept. Unsolvable cases fall back to fzero on the page.
'use strict';
const path = require('path');
const { TOPICS, CONSTANTS } = require('./src/formulas.js');
const E = require('./src/engine.js');
const consts = Object.fromEntries(Object.entries(CONSTANTS).map(([k, v]) => [k, v.value]));
const SAMPLE = { db: 63.7, unit: 0.37, sym: 0.41, ge1: 2.3, deg90: 33, int: 2, any: 47, pos: 1.73 };
const out = ['jobs = {};'];
for (const T of TOPICS) T.formulas.forEach((F, i) => {
  if (F.noInverse) return;
  const lhs = F.vars[0];
  const vals = {};
  F.vars.slice(1).forEach((k, j) => vals[k] = SAMPLE[T.vars[k][3] || 'pos'] * (1 + 0.13 * j));
  if (lhs === 'th') vals.ka = 5.2;
  if (lhs === 'B') vals.fu = 2 * vals.fl;
  if (lhs === 'alpha_s') vals.T2 = 0.6 * vals.T1;
  if (lhs === 'pd') { vals.k = 1.1; vals.d = 0.4; }
  const roots = E.solve1(x => F.f(Object.assign({}, consts, vals, { [lhs]: x })), T.vars[lhs][3]);
  if (!roots.length) return;
  vals[lhs] = roots[0];
  const eq = F.sym || F.txt.replace('=', '==').replace(/\bln\(/g, 'log(');
  const all = Object.assign({}, consts, vals);
  const used = Object.keys(all).filter(k => new RegExp('\\b' + k + '\\b').test(eq));
  const doms = used.map(k => (T.vars[k] && T.vars[k][3]) || 'pos');
  const V = k => k + '_v';                       // MATLAB reads I, E, ... as built-ins: suffix every name
  const exact = str => str.replace(/(\d+)\.(\d+)/g, (m, i, f) => `(${i}${f}/1${'0'.repeat(f.length)})`);   // 55.3 -> (553/10)
  const eqV = exact(eq).replace(new RegExp('\\b(' + used.join('|') + ')\\b', 'g'), m => V(m));
  out.push(`jobs{end+1} = struct('id', '${T.id}/${i}', 'eq', '${eqV}', 'vars', {{${F.vars.map(k => `'${V(k)}'`).join(' ')}}}, 'names', {{${used.map(k => `'${V(k)}'`).join(' ')}}}, 'doms', {{${doms.map(d => `'${d}'`).join(' ')}}}, 'vals', [${used.map(k => all[k]).join(' ')}], 'ints', {{${F.vars.filter(k => T.vars[k][3] === 'int').map(k => `'${V(k)}'`).join(' ')}}});`);
});
out.push(`
res = struct();
for j = 1:numel(jobs)
  J = jobs{j};
  S = sym(J.names);
  for q = 1:numel(S)
    switch J.doms{q}
      case {'db','any','sym'}, assume(S(q), 'real');
      otherwise, assume(S(q), 'positive');
    end
  end
  eqn = str2sym(J.eq);
  entry = struct();
  for v = J.vars
    name = v{1};
    if any(strcmp(J.ints, name)), continue; end
    x = S(strcmp(J.names, name));
    want = J.vals(strcmp(J.names, name));
    try
      sols = solve(eqn, x, 'Real', true, 'IgnoreAnalyticConstraints', true);
    catch
      sols = sym([]);
    end
    best = ''; err = Inf;
    others = J.names(~strcmp(J.names, name));
    for s = reshape(sols, 1, [])
      if contains(char(s), 'root(') || contains(char(s), 'piecewise'), continue; end
      try
        val = double(subs(s, sym(others), J.vals(~strcmp(J.names, name))));
      catch, continue; end
      e = abs(val - want) / max(1, abs(want));
      if isreal(val) && e < err, err = e; best = char(simplify(s)); end
    end
    if err < 1e-6, entry.(name(1:end-2)) = best; end
  end
  res.(strrep(J.id, '/', '_')) = entry;
end
fid = fopen('${path.join(__dirname, 'src', 'inverses.json')}', 'w'); fprintf(fid, '%s', jsonencode(res, 'PrettyPrint', true)); fclose(fid);
disp('INVERSES DONE')
`);
console.log(out.join('\n'));
