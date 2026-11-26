// Turn MATLAB symbolic output into readable element-wise MATLAB:
//   (20*log(p/p0))/log(10) -> 20*log10(p./p0),  x^(1/2) -> sqrt(x),  (553*V)/(10*T*c) -> 55.3*V./(T.*c)
'use strict';

function tokenize(s) {
  const toks = []; let i = 0;
  while (i < s.length) {
    const ch = s[i];
    if (/\s/.test(ch)) { i++; continue; }
    const num = s.slice(i).match(/^(\d+\.?\d*|\.\d+)(e[+-]?\d+)?/i);
    if (num) { toks.push({ t: 'num', v: num[0] }); i += num[0].length; continue; }
    const id = s.slice(i).match(/^[A-Za-z_]\w*/);
    if (id) { toks.push({ t: 'id', v: id[0] }); i += id[0].length; continue; }
    toks.push({ t: 'op', v: ch }); i++;
  }
  return toks;
}

function parse(s) {
  const T = tokenize(s); let p = 0;
  const peek = () => T[p], eat = v => { if (T[p] && T[p].v === v) { p++; return true; } return false; };
  function expr() {
    const terms = [{ sign: 1, x: term() }];
    while (peek() && (peek().v === '+' || peek().v === '-')) { const sg = T[p++].v === '+' ? 1 : -1; terms.push({ sign: sg, x: term() }); }
    return terms.length === 1 && terms[0].sign === 1 ? terms[0].x : { t: 'add', terms };
  }
  function term() {
    const num = [unary()], den = [];
    while (peek() && (peek().v === '*' || peek().v === '/')) { const op = T[p++].v; (op === '*' ? num : den).push(unary()); }
    return num.length === 1 && !den.length ? num[0] : { t: 'mul', num, den };
  }
  function unary() { if (eat('-')) return { t: 'neg', x: unary() }; if (eat('+')) return unary(); return power(); }
  function power() { const b = primary(); if (eat('^')) return { t: 'pow', b, e: unary() }; return b; }
  function primary() {
    const tk = T[p++];
    if (!tk) throw new Error('unexpected end in ' + s);
    if (tk.t === 'num') return { t: 'num', v: Number(tk.v) };
    if (tk.t === 'id') {
      if (eat('(')) { const args = [expr()]; while (eat(',')) args.push(expr()); if (!eat(')')) throw new Error(') expected in ' + s); return { t: 'call', f: tk.v, args }; }
      return { t: 'var', n: tk.v };
    }
    if (tk.v === '(') { const e = expr(); if (!eat(')')) throw new Error(') expected in ' + s); return e; }
    throw new Error('bad token ' + tk.v + ' in ' + s);
  }
  const e = expr();
  if (p !== T.length) throw new Error('trailing input in ' + s);
  return e;
}

const isNum = n => n.t === 'num';
const isConst = n => n.t === 'num' || (n.t === 'var' && n.n === 'pi') || (n.t === 'call' && n.args.every(a => constVal(a) !== null));
const constVal = n => {
  if (n.t === 'num') return n.v;
  if (n.t === 'neg') { const v = constVal(n.x); return v === null ? null : -v; }
  if (n.t === 'mul') { let v = 1; for (const a of n.num) { const x = constVal(a); if (x === null) return null; v *= x; } for (const a of n.den) { const x = constVal(a); if (x === null) return null; v /= x; } return v; }
  return null;
};
const isLog10Den = n => n.t === 'call' && n.f === 'log' && n.args.length === 1 && constVal(n.args[0]) === 10;
const gcd = (a, b) => b ? gcd(b, a % b) : a;
function decimal(a, b) {
  let d = b; while (d % 2 === 0) d /= 2; while (d % 5 === 0) d /= 5;
  return d === 1 ? String(Number((a / b).toPrecision(12))) : null;
}

function simplify(n) {
  switch (n.t) {
    case 'num': case 'var': return n;
    case 'neg': { const x = simplify(n.x); return x.t === 'neg' ? x.x : { t: 'neg', x }; }
    case 'call': return { t: 'call', f: n.f, args: n.args.map(simplify) };
    case 'add': return { t: 'add', terms: n.terms.map(({ sign, x }) => ({ sign, x: simplify(x) })) };
    case 'pow': {
      const b = simplify(n.b), e = simplify(n.e), ev = constVal(e);
      if (ev === 0.5) return { t: 'call', f: 'sqrt', args: [b] };
      if (ev === -0.5) return { t: 'mul', num: [{ t: 'num', v: 1 }], den: [{ t: 'call', f: 'sqrt', args: [b] }] };
      return { t: 'pow', b, e };
    }
    case 'mul': {
      // flatten nested products/quotients
      let num = [], den = [], outerSign = 1;
      const push = (x, into, other) => {
        if (x.t === 'neg') { outerSign = -outerSign; return push(x.x, into, other); }
        if (x.t === 'mul') { x.num.forEach(a => push(a, into, other)); x.den.forEach(a => push(a, other, into)); } else into.push(x);
      };
      n.num.map(simplify).forEach(x => push(x, num, den));
      n.den.map(simplify).forEach(x => push(x, den, num));
      // log(x)/log(10) -> log10(x)
      const li = den.findIndex(isLog10Den);
      if (li >= 0) {
        const logs = num.filter(x => x.t === 'call' && x.f === 'log');
        const sums = num.filter(x => x.t === 'add');
        const allLogAdd = a => a.terms.every(({ x }) => (x.t === 'call' && x.f === 'log') || (x.t === 'mul' && x.den.length === 0 && x.num.filter(y => y.t === 'call' && y.f === 'log').length === 1 && x.num.every(y => isNum(y) || (y.t === 'call' && y.f === 'log'))));
        const toLog10 = x => x.t === 'call' && x.f === 'log' ? { t: 'call', f: 'log10', args: x.args } : x.t === 'mul' ? { t: 'mul', num: x.num.map(toLog10), den: x.den } : x;
        if (logs.length === 1 && !sums.length) { den.splice(li, 1); num = num.map(x => x === logs[0] ? toLog10(x) : x); }
        else if (!logs.length && sums.length === 1) {
          // each term: c*log(x) -> c*log10(x); B*log(10) -> B; anything else -> give up
          const conv = y => {
            const fac = y.t === 'mul' && !y.den.length ? y.num : [y];
            const l10 = fac.findIndex(isLog10Den);
            if (l10 >= 0) { const rest = fac.filter((_, j) => j !== l10); return rest.length ? (rest.length === 1 ? rest[0] : { t: 'mul', num: rest, den: [] }) : { t: 'num', v: 1 }; }
            const lg = fac.filter(z => z.t === 'call' && z.f === 'log');
            if (lg.length === 1 && fac.every(z => z === lg[0] || isNum(z))) return toLog10(y);
            return null;
          };
          const terms = sums[0].terms.map(({ sign, x: y }) => ({ sign, x: conv(y) }));
          if (terms.every(t => t.x)) { den.splice(li, 1); num = num.map(x => x === sums[0] ? simplify({ t: 'add', terms }) : x); }
        }
      }
      // numeric coefficient
      let a = 1, b = 1, sign = 1;
      const strip = (arr, into) => arr.filter(x => {
        if (x.t === 'neg') { sign = -sign; x = x.x; }
        if (isNum(x) && Number.isInteger(x.v)) { into === 'a' ? (a *= x.v) : (b *= x.v); return false; }
        return true;
      });
      const unneg = arr => arr.map(x => { if (x.t === 'neg') { sign = -sign; return x.x; } return x; });
      num = strip(unneg(num), 'a'); den = strip(unneg(den), 'b');
      const g = gcd(Math.abs(a), Math.abs(b)) || 1; a /= g; b /= g;
      const coef = [];
      const dec = Math.abs(a) === 1 && b !== 1 ? null : decimal(a, b);   // keep x/10, Q/(4*pi*r^2)
      const rdec = dec === null && Math.abs(a) !== 1 ? decimal(b, Math.abs(a)) : null;   // 10/553 -> /55.3
      if (rdec !== null) {
        if (a < 0) sign = -sign;
        if (!num.length) num.push({ t: 'num', v: 1 });
        den.unshift({ t: 'num', v: Number(rdec), s: rdec });
      } else if (dec !== null) { if (dec !== '1' || !num.length) coef.push({ t: 'num', v: Number(dec), s: dec }); }
      else { if (a !== 1 || !num.length) coef.push({ t: 'num', v: a }); if (b !== 1) den.unshift({ t: 'num', v: b }); }
      let out = { t: 'mul', num: coef.concat(num.length ? num : coef.length ? [] : [{ t: 'num', v: 1 }]), den };
      if (out.num.length === 1 && !out.den.length) out = out.num[0];
      return sign * outerSign < 0 ? { t: 'neg', x: out } : out;
    }
  }
  return n;
}

// precedence: add 1, mul 2, neg 3, pow 4, atom 5
function print(n, parent = 0) {
  const wrap = (s, prec) => prec < parent ? '(' + s + ')' : s;
  switch (n.t) {
    case 'num': return n.s || String(n.v);
    case 'var': return n.n;
    case 'call': return n.f + '(' + n.args.map(a => print(a, 0)).join(', ') + ')';
    case 'neg': return wrap('-' + print(n.x, n.x.t === 'mul' ? 2 : 3), 3);
    case 'add': {
      let s = '';
      n.terms.forEach(({ sign, x }, i) => {
        let xs = print(x, 1), sg = sign;
        if (x.t === 'neg') { sg = -sg; xs = print(x.x, 2); }
        s += i === 0 ? (sg < 0 ? '-' + xs : xs) : (sg < 0 ? ' - ' : ' + ') + xs;
      });
      return wrap(s, 1);
    }
    case 'mul': {
      let s = '';
      n.num.forEach((x, i) => {
        const xs = print(x, 2.5);
        if (i === 0) s = xs;
        else s += (isConst(n.num[i - 1]) || isConst(x) ? '*' : '.*') + xs;
      });
      if (!n.num.length) s = '1';
      const numericOnly = n.den.every(isConst);
      if (n.den.length === 1) s += (numericOnly ? '/' : './') + print(n.den[0], 4);
      else if (n.den.length > 1) s += (numericOnly ? '/(' : './(') + n.den.map((x, i) => (i ? (isConst(n.den[i - 1]) || isConst(x) ? '*' : '.*') : '') + print(x, 2.5)).join('') + ')';
      return wrap(s, 2);
    }
    case 'pow': {
      const both = isNum(n.b) && constVal(n.e) !== null;
      return wrap(print(n.b, 5) + (both ? '^' : '.^') + print(n.e, 5), 4);
    }
  }
}

const toMatlab = s => print(simplify(parse(s)));
module.exports = { toMatlab, parse, simplify, print };

if (require.main === module) {
  for (const s of ['(20*log(p/p0))/log(10)', '(2^(1/2)*pk)/2', 'I^(1/2)*c^(1/2)*rho^(1/2)', '(553*V)/(10*T*c)', '10^(LI/10)*I0',
    'Lp - (10*log(Q/(4*pi*r^2)))/log(10) - (10*log((W0*c*rho)/p0^2))/log(10)', '(1 - alpha)^(1/2)', '-(c*rho*(R + 1))/(R - 1)', '(12353*x)/200000'])
    console.log(s.padEnd(70), '->', toMatlab(s));
}
