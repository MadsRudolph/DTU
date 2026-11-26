// UI for the formula sheets. Plain DOM, no framework.
(function () {
  'use strict';
  const { TOPICS, CONSTANTS, aWeight, COURSE_DIR, EXAM_NOTES } = window.FORMULAS;
  const obsidian = rel => 'obsidian://open?path=' + encodeURIComponent(COURSE_DIR + rel);
  const E = window.ENGINE;
  const $ = (sel, el = document) => el.querySelector(sel);
  const h = (tag, attrs = {}, ...kids) => {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === 'class') el.className = v;
      else if (k === 'html') el.innerHTML = v;
      else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
      else if (v !== undefined && v !== null && v !== false) el.setAttribute(k, v);
    }
    for (const kid of kids.flat()) if (kid !== null && kid !== undefined && kid !== false) el.append(kid.nodeType ? kid : document.createTextNode(kid));
    return el;
  };
  const tex = (s, display) => {
    try { return katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; }
  };

  // ---------------- state ----------------
  const KEY = 'acoustics-formula-sheets-v1';
  let store = {};
  try { store = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { store = {}; }
  store.topics = store.topics || {};
  store.consts = store.consts || {};
  store.widgets = store.widgets || {};
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(store)); } catch (e) { /* private mode */ } };
  const constValues = () => Object.fromEntries(Object.entries(CONSTANTS).map(([k, c]) => {
    const v = E.parseInput(store.consts[k]);
    return [k, Number.isFinite(v) ? v : c.value];
  }));

  let current = null;     // topic object
  let lastResult = null;

  // ---------------- sidebar ----------------
  function buildSidebar() {
    const nav = $('#topics');
    nav.innerHTML = '';
    TOPICS.forEach(t => {
      nav.append(h('a', { href: '#' + t.id, 'data-id': t.id }, t.title));
    });
    const cbox = $('#consts');
    cbox.innerHTML = '';
    const ex = $('#examnotes');
    ex.innerHTML = '';
    EXAM_NOTES.forEach(([label, rel]) => ex.append(h('a', { href: obsidian(rel) }, label)));
    cbox.append(h('button', { class: 'const-copy', title: 'Copy the constants as one MATLAB line', onclick: () => copyText(CONST_LINE(), 'Constants copied') }, 'Copy constants for MATLAB'));
    Object.entries(CONSTANTS).filter(([, c]) => c.editable).forEach(([k, c]) => {
      const inp = h('input', { value: store.consts[k] ?? String(c.value), 'aria-label': c.name, spellcheck: 'false' });
      inp.addEventListener('input', () => {
        store.consts[k] = inp.value; save();
        inp.classList.toggle('invalid', !Number.isFinite(E.parseInput(inp.value)));
        refresh();
      });
      cbox.append(h('label', { class: 'const', title: c.name }, h('span', { class: 'sym', html: tex(c.sym) }), inp, h('span', { class: 'unit' }, c.unit)));
    });
    markNav();
  }
  function markNav() {
    document.querySelectorAll('#topics a').forEach(a => {
      const id = a.dataset.id;
      a.classList.toggle('active', current && current.id === id);
      const t = store.topics[id];
      a.classList.toggle('used', !!t && Object.values(t).some(v => String(v).trim() !== ''));
    });
  }

  // ---------------- topic page ----------------
  function showTopic(id, focusFormula) {
    const t = TOPICS.find(x => x.id === id) || TOPICS[0];
    current = t;
    store.topics[t.id] = store.topics[t.id] || {};
    const main = $('#main');
    main.innerHTML = '';
    main.append(
      h('header', { class: 'topic-head' },
        h('div', {},
          h('h1', {}, t.title),
          h('p', { class: 'blurb' }, t.blurb),
          t.notes ? h('p', { class: 'notes' }, 'In Obsidian: ', ...t.notes.flatMap(([label, rel], j) => [j ? ' · ' : '', h('a', { href: obsidian(rel), title: rel.split('/').pop().replace(/\.md$/, '') }, label)])) : null),
        h('div', { class: 'actions' },
          h('button', { onclick: copyMatlab, title: 'Constants, your given values and the MATLAB line of every formula used, ready to paste into a live script' }, 'Copy as MATLAB'),
          h('button', { onclick: copyWorking, title: 'Copy the given values and every worked step as plain text' }, 'Copy working'),
          h('button', { onclick: clearTopic }, 'Clear'))),
      h('p', { class: 'help' }, 'Type what you know. Whatever follows from it appears in blue, with the working underneath. Fields accept arithmetic, like 2*(5*8 + 5*3) or 4*pi.')
    );
    t.formulas.forEach((F, i) => main.append(formulaRow(t, F, i)));
    (t.widgets || []).forEach(w => main.append(WIDGETS[w](t)));
    markNav();
    refresh();
    if (focusFormula !== undefined) {
      const el = document.getElementById(`f-${t.id}-${focusFormula}`);
      if (el) { el.scrollIntoView({ block: 'center' }); el.classList.add('flash'); setTimeout(() => el.classList.remove('flash'), 1400); const i = $('input', el); if (i) i.focus(); }
    } else main.scrollTop = 0, window.scrollTo(0, 0);
  }

  function formulaRow(t, F, i) {
    const fields = F.vars.map(k => {
      const [sym, unit, name] = t.vars[k];
      const inp = h('input', { 'data-key': k, inputmode: 'decimal', spellcheck: 'false', autocomplete: 'off', 'aria-label': name });
      inp.addEventListener('input', () => {
        const s = inp.value;
        if (s.trim() === '') delete store.topics[t.id][k]; else store.topics[t.id][k] = s;
        save(); refresh(inp);
      });
      inp.addEventListener('focus', () => { if (inp.classList.contains('computed')) inp.select(); });
      inp.addEventListener('keydown', e => {
        if (e.key === 'Escape') { inp.value = ''; inp.dispatchEvent(new Event('input')); }
      });
      return h('label', { class: 'field', title: name + (unit ? ` (${unit})` : '') },
        h('span', { class: 'sym', html: tex(sym) }), inp, unit ? h('span', { class: 'unit' }, unit) : null);
    });
    return h('section', { class: 'formula', id: `f-${t.id}-${i}`, 'data-i': i },
      h('h3', {}, F.name),
      h('div', { class: 'tex', html: tex(F.tex, true) }),
      matlabBox(t, F, i),
      h('div', { class: 'fields' }, fields),
      h('p', { class: 'where' }, ...F.vars.flatMap((k, j) => {
        const [sym, unit, name] = t.vars[k];
        return [j ? h('span', { class: 'sep' }, ' · ') : '', h('span', { html: tex(sym) }), ` ${name}${unit ? ' (' + unit + ')' : ''}`];
      }), ...whereConsts(F)),
      h('div', { class: 'work' }),
      F.note ? h('p', { class: 'note' }, F.note) : null);
  }

  function givenNumbers(t) {
    const g = {};
    for (const [k, raw] of Object.entries(store.topics[t.id] || {})) {
      const v = E.parseInput(raw);
      if (Number.isFinite(v)) g[k] = v;
    }
    return g;
  }

  function refresh(activeInput) {
    if (!current) return;
    const t = current;
    const raws = store.topics[t.id] || {};
    const consts = constValues();
    const res = E.propagate(t, givenNumbers(t), consts);
    lastResult = res;
    document.querySelectorAll('#main .formula').forEach(sec => {
      const i = +sec.dataset.i, F = t.formulas[i], row = res.rows[i];
      sec.querySelectorAll('input[data-key]').forEach(inp => {
        const k = inp.dataset.key, unit = t.vars[k][1];
        const raw = raws[k];
        inp.classList.remove('computed', 'given', 'invalid');
        if (raw !== undefined) {
          inp.classList.add(Number.isFinite(E.parseInput(raw)) ? 'given' : 'invalid');
          if (inp !== activeInput && inp !== document.activeElement) inp.value = raw;
          else if (inp !== activeInput && inp.value !== raw) inp.value = raw;
          inp.title = '';
        } else if (k in res.info) {
          inp.classList.add('computed');
          if (inp !== activeInput) inp.value = E.fmt(res.values[k], unit);
          inp.title = 'Worked out from: ' + t.formulas[res.info[k].from].name;
        } else {
          if (inp !== activeInput) inp.value = '';
          inp.title = '';
        }
      });
      const mb = $('.mlbox', sec);
      if (mb) mb._auto(row.solved);
      const work = $('.work', sec);
      work.innerHTML = '';
      work.className = 'work';
      if (row.solved) {
        work.append(workLine(t, F, row.solved, res, consts));
        const alt = res.info[row.solved].roots.filter(r => r !== res.values[row.solved]);
        if (alt.length) work.append(h('div', { class: 'alt' }, `Other solution${alt.length > 1 ? 's' : ''}: ${alt.slice(0, 4).map(r => E.fmt(r, t.vars[row.solved][1])).join(', ')} ${t.vars[row.solved][1]}. Type the one you want if the blue value is the wrong branch.`));
        sec.classList.add('active');
      } else if (row.mismatch) {
        const k = row.mismatch.key;
        work.classList.add('warn');
        work.append(row.mismatch.value === undefined
          ? `These values can’t all hold at once.`
          : `These values disagree: with the others, this formula gives ${plainSym(t, k)} = ${E.fmt(row.mismatch.value, t.vars[k][1])} ${t.vars[k][1]}.`);
        sec.classList.add('active');
      } else if (row.noSolution) {
        work.classList.add('warn');
        work.append(`No real value of ${plainSym(t, row.noSolution)} fits these numbers.`);
        sec.classList.add('active');
      } else {
        sec.classList.toggle('active', F.vars.some(k => k in raws || k in res.info));
      }
    });
    document.querySelectorAll('#main .widget').forEach(w => w._update && w._update(res));
    markNav();
  }

  const GREEK = { alpha: 'α', tau: 'τ', lambda: 'λ', omega: 'ω', varphi: 'φ', phi: 'φ', rho: 'ρ', theta: 'θ', zeta: 'ζ', xi: 'ξ', eta: 'η', nu: 'ν', Omega: 'Ω', Delta: 'Δ', ell: 'ℓ', max: 'max', min: 'min' };
  const plainSym = (t, k) => t.vars[k][0]
    .replace(/\\(rm|mathrm|bar|hat)\b ?/g, '')
    .replace(/\\([A-Za-z]+)/g, (m, w) => GREEK[w] || w)
    .replace(/[{}]/g, '').replace(/_/g, '').replace(/\s+/g, '');

  // "T = 55.3·120/(343·48) = 0.4031 s"
  function workText(t, F, key, res, consts) {
    const unit = t.vars[key][1];
    const keys = F.vars.concat(Object.keys(consts));
    const val = `${E.fmt(res.values[key], unit)}${unit ? ' ' + unit : ''}`;
    if (key === F.vars[0]) {
      const rhs = F.txt.slice(F.txt.indexOf('=') + 1).trim();
      return `${plainSym(t, key)} = ${E.substitute(rhs, res.values, keys)} = ${val}`;
    }
    const known = F.vars.filter(k => k !== key).map(k => `${plainSym(t, k)} = ${E.fmt(res.values[k], t.vars[k][1])}`).join(', ');
    return `${plainSym(t, key)} = ${val}   (solved from ${F.txt.replace(/\*/g, '·')}, with ${known})`;
  }
  function workLine(t, F, key, res, consts) {
    return h('div', { class: 'line' }, workText(t, F, key, res, consts));
  }

  // constants used by a formula, named once so every symbol on the row is explained
  function whereConsts(F) {
    const used = Object.keys(CONSTANTS).filter(k => new RegExp('\\b' + k + '\\b').test(F.txt));
    return used.flatMap(k => [h('span', { class: 'sep' }, ' · '), h('span', { html: tex(CONSTANTS[k].sym) }), ` ${CONSTANTS[k].name} = ${E.fmt(constValues()[k])} ${CONSTANTS[k].unit}`]);
  }
  // MATLAB line for the chosen unknown: the page's own result picks it, or click a symbol
  const INV = window.INVERSES || {};
  function matlabLine(t, F, i, key) {
    const lines = INV[`${t.id}_${i}`] || {};
    const line = lines[key] || (key === F.vars[0] ? E.toMatlab(F) : null);
    if (!line) return null;
    const v = lastResult && lastResult.values[key];
    return line.replace('GUESS', Number.isFinite(v) ? E.fmt(v) : '1');
  }
  function matlabBox(t, F, i) {
    const lines = INV[`${t.id}_${i}`] || {};
    const keys = F.vars.filter(k => lines[k] || k === F.vars[0]);
    const code = h('code', {});
    const btn = h('button', { class: 'ml-copy', title: 'Copy this line' }, 'copy');
    const chips = h('span', { class: 'ml-for' });
    const box = h('div', { class: 'mlbox' }, h('div', { class: 'ml' }, code, btn), chips);
    let sel = F.vars[0], manual = false;
    const show = () => {
      code.textContent = matlabLine(t, F, i, sel) || '';
      chips.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.k === sel));
    };
    if (keys.length > 1) {
      chips.append(h('span', { class: 'lab' }, 'MATLAB for '));
      keys.forEach(k => chips.append(h('button', { 'data-k': k, html: tex(t.vars[k][0]), title: `Line that gives ${t.vars[k][2]}`,
        onclick: () => { sel = k; manual = true; show(); } })));
    }
    $('.ml', box).addEventListener('click', () => copyText(code.textContent, 'MATLAB line copied'));
    box._auto = k => { if (!manual) sel = k && keys.includes(k) ? k : F.vars[0]; show(); };
    show();
    return box;
  }
  const CONST_LINE = () => { const c = constValues(); return `rho = ${c.rho}; c = ${c.c}; p0 = 20e-6; I0 = 1e-12; W0 = 1e-12; g = 9.81;`; };

  // Paste-ready MATLAB: constants, given values, then each formula used, in the order it was solved.
  function copyMatlab() {
    const t = current, res = lastResult, raws = store.topics[t.id] || {};
    const lines = [`%% ${t.title}`, CONST_LINE()];
    const given = Object.keys(raws).filter(k => Number.isFinite(E.parseInput(raws[k])));
    given.forEach(k => lines.push(`${k} = ${raws[k].trim()};${' '.repeat(Math.max(1, 14 - k.length - raws[k].trim().length))}% ${t.vars[k][2]}${t.vars[k][1] ? ', ' + t.vars[k][1] : ''}`));
    const solved = Object.entries(res.info).sort((a, b) => a[1].order - b[1].order);
    solved.forEach(([k, inf]) => {
      const F = t.formulas[inf.from];
      const line = matlabLine(t, F, inf.from, k);
      lines.push(line || `${k} = ${E.fmt(res.values[k])}   % from ${E.toMatlab(F)}`);
    });
    if (!solved.length) lines.push('% Nothing worked out yet: every formula line on this page:', ...t.formulas.map(F => E.toMatlab(F)));
    copyText(lines.join('\n'), 'MATLAB copied');
  }
  function copyText(text, msg) {
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(() => toast(msg || 'Copied'), () => fallbackCopy(text, msg));
    else fallbackCopy(text, msg);
  }

  function copyWorking() {
    const t = current, res = lastResult, consts = constValues();
    const raws = store.topics[t.id] || {};
    const lines = [t.title, ''];
    const given = Object.keys(raws).filter(k => Number.isFinite(E.parseInput(raws[k])));
    if (given.length) lines.push('Given: ' + given.map(k => `${plainSym(t, k)} = ${E.fmt(E.parseInput(raws[k]), t.vars[k][1])} ${t.vars[k][1]}`.trim()).join(', '));
    lines.push(`Constants: c = ${consts.c} m/s, ρ = ${consts.rho} kg/m³`, '');
    Object.entries(res.info).sort((a, b) => a[1].order - b[1].order).forEach(([k, inf]) => {
      const F = t.formulas[inf.from];
      lines.push(`${F.name}: ${workText(t, F, k, res, consts)}`);
    });
    copyText(lines.join('\n'), 'Working copied');
  }
  function fallbackCopy(text, msg) {
    const ta = h('textarea', {}, text);
    document.body.append(ta); ta.select();
    try { document.execCommand('copy'); toast(msg || 'Copied'); } catch (e) { toast('Copy failed'); }
    ta.remove();
  }
  function clearTopic() {
    store.topics[current.id] = {};
    delete store.widgets[current.id];
    save();
    showTopic(current.id);
  }
  let toastTimer;
  function toast(msg) {
    const el = $('#toast');
    el.textContent = msg; el.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => el.classList.remove('show'), 1200);
  }

  // ---------------- search ----------------
  function search(q) {
    const main = $('#main');
    const words = q.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = [];
    TOPICS.forEach(t => t.formulas.forEach((F, i) => {
      const hay = [t.title, F.name, F.note || '', F.txt, ...F.vars.map(k => t.vars[k][2])].join(' ').toLowerCase();
      if (words.every(w => hay.includes(w))) hits.push({ t, F, i });
    }));
    main.innerHTML = '';
    main.append(h('header', { class: 'topic-head' }, h('div', {}, h('h1', {}, 'Search'), h('p', { class: 'blurb' }, hits.length ? `${hits.length} formula${hits.length > 1 ? 's' : ''} match “${q}”. Enter opens the first.` : `Nothing matches “${q}”.`))));
    const list = h('div', { class: 'results' });
    hits.forEach(({ t, F, i }, n) => {
      list.append(h('a', { class: 'result' + (n === 0 ? ' first' : ''), href: `#${t.id}/${i}`, onclick: () => { $('#search').value = ''; } },
        h('span', { class: 'r-name' }, F.name), h('span', { class: 'r-topic' }, t.title),
        h('span', { class: 'r-tex', html: tex(F.tex) })));
    });
    main.append(list);
    current = null; markNav();
    return hits;
  }

  // ---------------- widgets ----------------
  const wstate = (t, name) => (store.widgets[t.id] = store.widgets[t.id] || {}, store.widgets[t.id][name] = store.widgets[t.id][name] || {});
  const wInput = (st, key, attrs = {}) => {
    const inp = h('input', Object.assign({ value: st[key] || '', spellcheck: 'false', autocomplete: 'off' }, attrs));
    inp.addEventListener('input', () => { st[key] = inp.value; save(); inp.dispatchEvent(new Event('recalc', { bubbles: true })); });
    return inp;
  };
  const list = s => String(s || '').split(/[\s,;]+/).filter(Boolean).map(E.parseInput);
  const dbSum = Ls => 10 * Math.log10(Ls.reduce((a, L) => a + 10 ** (L / 10), 0));
  const out = (label, value, unit) => h('div', { class: 'out' }, h('span', { class: 'o-label' }, label), h('span', { class: 'o-val' }, value), unit ? h('span', { class: 'unit' }, unit) : null);

  const WIDGETS = {
    combine(t) {
      const st = wstate(t, 'combine');
      const res = h('div', { class: 'outs' });
      const res2 = h('div', { class: 'outs' });
      const w = h('section', { class: 'widget' },
        h('h3', {}, 'Combine levels'),
        h('p', { class: 'note' }, 'Incoherent sources (noise, different frequencies). Separate the numbers with commas or spaces.'),
        h('div', { class: 'fields' },
          h('label', { class: 'field wide' }, h('span', { class: 'lab' }, 'Levels'), wInput(st, 'L', { placeholder: '85, 82, 79' }), h('span', { class: 'unit' }, 'dB')),
          h('label', { class: 'field wide' }, h('span', { class: 'lab' }, 'Durations'), wInput(st, 't', { placeholder: 'optional' })),
          h('label', { class: 'field' }, h('span', { class: 'lab' }, 'over'), wInput(st, 'T', { placeholder: 'Σt' }))),
        res,
        h('h3', { class: 'sub' }, 'Subtract background'),
        h('div', { class: 'fields' },
          h('label', { class: 'field' }, h('span', { class: 'lab' }, 'Total'), wInput(st, 'Lt'), h('span', { class: 'unit' }, 'dB')),
          h('label', { class: 'field' }, h('span', { class: 'lab' }, 'Background'), wInput(st, 'Lb'), h('span', { class: 'unit' }, 'dB'))),
        res2);
      const upd = () => {
        res.innerHTML = ''; res2.innerHTML = '';
        const Ls = list(st.L).filter(Number.isFinite);
        if (Ls.length) {
          res.append(out('Sum', E.fmt(dbSum(Ls), 'dB'), 'dB'), out('Energy average', E.fmt(dbSum(Ls) - 10 * Math.log10(Ls.length), 'dB'), 'dB'));
          const ts = list(st.t).filter(Number.isFinite);
          if (ts.length === Ls.length) {
            const T = E.parseInput(st.T);
            const tot = Number.isFinite(T) ? T : ts.reduce((a, b) => a + b, 0);
            const Leq = 10 * Math.log10(Ls.reduce((a, L, i) => a + ts[i] * 10 ** (L / 10), 0) / tot);
            res.append(out('L_eq', E.fmt(Leq, 'dB'), 'dB'));
          } else if (ts.length) res.append(h('div', { class: 'alt' }, 'Give one duration per level.'));
        }
        const Lt = E.parseInput(st.Lt), Lb = E.parseInput(st.Lb);
        if (Number.isFinite(Lt) && Number.isFinite(Lb)) {
          const d = 10 ** (Lt / 10) - 10 ** (Lb / 10);
          res2.append(d > 0 ? out('Source alone', E.fmt(10 * Math.log10(d), 'dB'), 'dB') : h('div', { class: 'warn' }, 'The background is louder than the total.'));
          if (d > 0 && Lt - Lb < 3) res2.append(h('div', { class: 'alt' }, 'Less than 3 dB above the background: a shaky measurement.'));
        }
      };
      w.addEventListener('recalc', upd); upd();
      return w;
    },

    bandtable(t) {
      const st = wstate(t, 'bands');
      const OCT = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000];
      const THIRD = [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000];
      // course table (rounded to 0.1 dB)
      const FA = [20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000, 20000];
      const KA = [-50.5, -44.7, -39.4, -34.6, -30.2, -26.2, -22.5, -19.1, -16.1, -13.4, -10.9, -8.6, -6.6, -4.8, -3.2, -1.9, -0.8, 0.0, 0.6, 1.0, 1.2, 1.3, 1.2, 1.0, 0.5, -0.1, -1.1, -2.5, -4.3, -6.6, -9.3];
      const aw = f => { const i = FA.indexOf(f); return i >= 0 ? KA[i] : Math.round(aWeight(f) * 10) / 10; };
      const body = h('div', {});
      const outs = h('div', { class: 'outs' });
      const sel = h('div', { class: 'seg' });
      const w = h('section', { class: 'widget' }, h('h3', {}, 'Band levels to L_A'),
        h('p', { class: 'note' }, 'Type the band levels you have; empty bands are skipped.'), sel, body, outs);
      const draw = () => {
        sel.innerHTML = '';
        ['Octave', 'Third octave'].forEach((lab, j) => sel.append(h('button', { class: (st.third ? 1 : 0) === j ? 'on' : '', onclick: () => { st.third = !!j; save(); draw(); } }, lab)));
        body.innerHTML = '';
        const bands = st.third ? THIRD : OCT;
        st.L = st.L || {};
        const tbl = h('table', { class: 'bands' }, h('tr', {}, h('th', {}, 'f_c (Hz)'), h('th', {}, 'L (dB)'), h('th', {}, 'A (dB)'), h('th', {}, 'L_A (dB)')));
        bands.forEach(f => {
          const inp = h('input', { value: st.L[f] || '', inputmode: 'decimal', spellcheck: 'false' });
          const la = h('td', { class: 'num computed' });
          inp.addEventListener('input', () => { st.L[f] = inp.value; save(); calc(); });
          inp._f = f; inp._la = la;
          tbl.append(h('tr', {}, h('td', { class: 'num' }, f >= 1000 ? (f / 1000) + 'k' : String(f)), h('td', {}, inp), h('td', { class: 'num muted' }, aw(f).toFixed(1)), la));
        });
        body.append(tbl);
        const calc = () => {
          const Ls = [], LAs = [];
          tbl.querySelectorAll('input').forEach(inp => {
            const L = E.parseInput(inp.value);
            if (Number.isFinite(L)) { const la = L + aw(inp._f); Ls.push(L); LAs.push(la); inp._la.textContent = la.toFixed(1); }
            else inp._la.textContent = '';
          });
          outs.innerHTML = '';
          if (Ls.length) outs.append(out('Total, unweighted', E.fmt(dbSum(Ls), 'dB'), 'dB'), out('Total, A-weighted', E.fmt(dbSum(LAs), 'dB'), 'dB(A)'));
        };
        calc();
      };
      draw();
      return w;
    },

    modes(t) {
      const st = wstate(t, 'modes');
      const body = h('div', {});
      const w = h('section', { class: 'widget' }, h('h3', {}, 'All modes up to a frequency'),
        h('p', { class: 'note' }, 'Uses L_x, L_y and L_z from above.'),
        h('div', { class: 'fields' },
          h('label', { class: 'field' }, h('span', { class: 'lab' }, 'up to'), wInput(st, 'fmax', { placeholder: '120' }), h('span', { class: 'unit' }, 'Hz')),
          h('label', { class: 'field' }, h('span', { class: 'lab' }, 'mark band at'), wInput(st, 'fc', { placeholder: 'optional' }), h('span', { class: 'unit' }, 'Hz, third octave'))),
        body);
      w._update = res => {
        body.innerHTML = '';
        const { Lx, Ly, Lz, c } = res.values;
        if (![Lx, Ly, Lz].every(Number.isFinite)) { body.append(h('p', { class: 'alt' }, 'Fill in L_x, L_y and L_z above.')); return; }
        const fmax = E.parseInput(st.fmax) || 120, fc = E.parseInput(st.fc);
        const lo = fc * 2 ** (-1 / 6), hi = fc * 2 ** (1 / 6);
        const modes = [];
        const N = n => Math.ceil(2 * fmax * n / c) + 1;
        for (let a = 0; a <= N(Lx); a++) for (let b = 0; b <= N(Ly); b++) for (let d = 0; d <= N(Lz); d++) {
          if (!a && !b && !d) continue;
          const f = c / 2 * Math.sqrt((a / Lx) ** 2 + (b / Ly) ** 2 + (d / Lz) ** 2);
          if (f <= fmax) modes.push({ n: [a, b, d], f });
        }
        modes.sort((x, y) => x.f - y.f);
        const kind = n => ['', 'axial', 'tangential', 'oblique'][n.filter(Boolean).length];
        const tbl = h('table', { class: 'bands' }, h('tr', {}, h('th', {}, '(n_x, n_y, n_z)'), h('th', {}, 'f (Hz)'), h('th', {}, 'type')));
        modes.slice(0, 80).forEach(m => {
          const inBand = Number.isFinite(fc) && m.f >= lo && m.f < hi;
          tbl.append(h('tr', { class: inBand ? 'hit' : '' }, h('td', {}, `(${m.n.join(', ')})`), h('td', { class: 'num' }, m.f.toFixed(1)), h('td', { class: 'muted' }, kind(m.n))));
        });
        if (Number.isFinite(fc)) body.append(h('p', { class: 'alt' }, `Band ${E.fmt(lo)}–${E.fmt(hi)} Hz holds ${modes.filter(m => m.f >= lo && m.f < hi).length} mode(s).`));
        body.append(tbl);
        if (modes.length > 80) body.append(h('p', { class: 'alt' }, `${modes.length - 80} more not shown.`));
      };
      w.addEventListener('recalc', () => refresh());
      return w;
    },

    composite(t) {
      const st = wstate(t, 'composite');
      st.rows = st.rows || [{ S: '', R: '' }, { S: '', R: '' }, { S: '', R: '' }];
      const body = h('div', {});
      const outs = h('div', { class: 'outs' });
      const target = wInput(st, 'target', { placeholder: 'optional' });
      const w = h('section', { class: 'widget' }, h('h3', {}, 'Composite wall'),
        h('p', { class: 'note' }, 'A wall with a door, a window or a gap. Leave one R empty and give the target to find what that element needs.'),
        body,
        h('div', { class: 'fields' }, h('label', { class: 'field' }, h('span', { class: 'lab' }, 'target R'), target, h('span', { class: 'unit' }, 'dB'))),
        outs);
      const draw = () => {
        body.innerHTML = '';
        const tbl = h('table', { class: 'bands' }, h('tr', {}, h('th', {}, 'element'), h('th', {}, 'S (m²)'), h('th', {}, 'R (dB)'), h('th', {})));
        st.rows.forEach((r, i) => {
          const mk = key => { const inp = h('input', { value: r[key], inputmode: 'decimal', spellcheck: 'false' }); inp.addEventListener('input', () => { r[key] = inp.value; save(); calc(); }); return inp; };
          tbl.append(h('tr', {}, h('td', { class: 'muted' }, String(i + 1)), h('td', {}, mk('S')), h('td', {}, mk('R')),
            h('td', {}, st.rows.length > 1 ? h('button', { class: 'x', title: 'Remove', onclick: () => { st.rows.splice(i, 1); save(); draw(); } }, '×') : null)));
        });
        body.append(tbl, h('button', { class: 'add', onclick: () => { st.rows.push({ S: '', R: '' }); save(); draw(); } }, '+ element'));
        calc();
      };
      const calc = () => {
        outs.innerHTML = '';
        const rows = st.rows.map(r => ({ S: E.parseInput(r.S), R: E.parseInput(r.R) })).filter(r => Number.isFinite(r.S));
        if (!rows.length) return;
        const Stot = rows.reduce((a, r) => a + r.S, 0);
        const missing = rows.filter(r => !Number.isFinite(r.R));
        const tsum = rows.filter(r => Number.isFinite(r.R)).reduce((a, r) => a + r.S * 10 ** (-r.R / 10), 0);
        if (!missing.length) {
          outs.append(out('Composite R', E.fmt(-10 * Math.log10(tsum / Stot), 'dB'), 'dB'), out('Total area', E.fmt(Stot), 'm²'));
        } else if (missing.length === 1) {
          const T = E.parseInput(st.target);
          if (!Number.isFinite(T)) { outs.append(h('p', { class: 'alt' }, 'Give a target R to solve for the empty one.')); return; }
          const need = Stot * 10 ** (-T / 10) - tsum;
          outs.append(need > 0
            ? out('Needed R for the empty element', E.fmt(-10 * Math.log10(need / missing[0].S), 'dB'), 'dB')
            : h('div', { class: 'warn' }, 'Not possible: the other elements already let through more than the target allows.'));
        } else outs.append(h('p', { class: 'alt' }, 'Leave at most one R empty.'));
      };
      target.addEventListener('recalc', calc);
      draw();
      return w;
    },
  };

  // ---------------- routing, keys, theme ----------------
  function route() {
    const [id, i] = location.hash.slice(1).split('/');
    showTopic(id || (store.last || TOPICS[0].id), i !== undefined ? +i : undefined);
    store.last = current.id; save();
  }

  function init() {
    buildSidebar();
    const s = $('#search');
    let hits = [];
    s.addEventListener('input', () => { if (s.value.trim()) hits = search(s.value.trim()); else route(); });
    s.addEventListener('keydown', e => {
      if (e.key === 'Enter' && hits.length) { location.hash = `${hits[0].t.id}/${hits[0].i}`; s.value = ''; s.blur(); if (location.hash === `#${hits[0].t.id}/${hits[0].i}`) route(); }
      if (e.key === 'Escape') { s.value = ''; s.blur(); route(); }
    });
    document.addEventListener('keydown', e => {
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') { e.preventDefault(); s.focus(); }
    });
    const themeBtn = $('#theme');
    const applyTheme = th => { document.documentElement.dataset.theme = th; themeBtn.textContent = th === 'dark' ? 'Light' : 'Dark'; };
    applyTheme(store.theme || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
    themeBtn.addEventListener('click', () => { store.theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'; save(); applyTheme(store.theme); });
    window.addEventListener('hashchange', route);
    route();
  }
  document.addEventListener('DOMContentLoaded', init);
})();
