// 34840 Exam App — Interactive UI Controller

(function () {
  'use strict';

  const P = window.AcousticsPhysics;
  const SOLVERS = window.SOLVERS_META;
  const MC = window.MC_DATA;
  const CS = window.CHEATSHEET_DATA;

  let activeTab = 'solvers';
  let activeSolverId = SOLVERS[0].id;
  const solverState = {};
  const globalConsts = { rho: 1.2, c: 343 };

  // Initialize default state for each solver
  for (const s of SOLVERS) {
    solverState[s.id] = {};
    for (const f of s.fields) {
      solverState[s.id][f.id] = f.default;
    }
  }

  function renderMath(tex, displayMode = false) {
    if (window.katex) {
      try {
        return window.katex.renderToString(tex, { displayMode, throwOnError: false });
      } catch (e) {
        return `<code>${escapeHtml(tex)}</code>`;
      }
    }
    return `<code>${escapeHtml(tex)}</code>`;
  }

  function escapeHtml(str) {
    return String(str ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function showToast(msg) {
    let t = document.getElementById('app-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'app-toast';
      t.style.cssText = 'position:fixed;bottom:18px;right:18px;background:var(--accent);color:#fff;padding:9px 15px;border-radius:7px;font-weight:700;font-size:13px;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,0.25);transition:opacity 0.2s;';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.opacity = '1';
    clearTimeout(t._timer);
    t._timer = setTimeout(() => { t.style.opacity = '0'; }, 1800);
  }

  function copyText(text, label = 'Copied to clipboard') {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => showToast(label)).catch(() => fallbackCopy(text, label));
    } else {
      fallbackCopy(text, label);
    }
  }

  function fallbackCopy(text, label) {
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast(label);
  }

  // --- Navigation ---
  function switchTab(tabId) {
    activeTab = tabId;
    document.querySelectorAll('.nav-tab').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    document.querySelectorAll('.view-panel').forEach(panel => {
      panel.classList.toggle('active', panel.id === `view-${tabId}`);
    });
  }

  function selectSolver(solverId, presetIdx = null) {
    const s = SOLVERS.find(item => item.id === solverId || item.code === solverId);
    if (!s) return;
    activeSolverId = s.id;
    if (presetIdx !== null && s.presets && s.presets[presetIdx]) {
      applyPreset(s, s.presets[presetIdx]);
    }
    switchTab('solvers');
    renderSolverSidebar();
    renderActiveSolver();
  }

  function applyPreset(solver, preset) {
    // Reset to defaults first
    for (const f of solver.fields) {
      solverState[solver.id][f.id] = f.default;
    }
    for (const [k, v] of Object.entries(preset.values)) {
      if (k === 'c' || k === 'rho') {
        globalConsts[k] = Number(v);
        const inp = document.getElementById(`const-${k}`);
        if (inp) inp.value = v;
      } else {
        solverState[solver.id][k] = v;
      }
    }
    updateRhoCDisplay();
  }

  // --- Universal "Which Solver?" Finder ---
  function buildSearchIndex() {
    const index = [];
    for (const s of SOLVERS) {
      index.push({
        type: 'Solver',
        tag: s.code,
        title: `${s.code} — ${s.title}`,
        sub: `Matches: ${s.matches}`,
        searchText: `${s.code} ${s.title} ${s.keywords} ${s.matches} ${s.description}`.toLowerCase(),
        action: () => selectSolver(s.id)
      });
      if (s.presets) {
        s.presets.forEach((pr, idx) => {
          index.push({
            type: 'Preset',
            tag: `${s.code} Preset`,
            title: pr.name,
            sub: `${s.code} — ${s.shortTitle}`,
            searchText: `${pr.name} ${s.code} ${s.shortTitle} ${s.keywords}`.toLowerCase(),
            action: () => selectSolver(s.id, idx)
          });
        });
      }
    }
    for (const sec of CS.sections) {
      index.push({
        type: 'Cheat Sheet',
        tag: `Cheat Sheet (${sec.solver})`,
        title: sec.title,
        sub: sec.items.map(i => i.label).join(' · '),
        searchText: `${sec.title} ${sec.keywords} ${sec.items.map(i => i.label + ' ' + i.note).join(' ')}`.toLowerCase(),
        action: () => {
          switchTab('cheatsheet');
          const el = document.getElementById(sec.id);
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }
    for (const q of MC) {
      index.push({
        type: 'Old Exam MC',
        tag: `${q.id} (${q.solver})`,
        title: `${q.id} [${q.topic}]: ${q.question.slice(0, 85)}…`,
        sub: `Answer ${q.answer}: ${q.reason.slice(0, 90)}…`,
        searchText: `${q.id} ${q.topic} ${q.question} ${q.reason} ${q.trap}`.toLowerCase(),
        action: () => {
          switchTab('mc');
          const el = document.getElementById(`mc-${q.id}`);
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }
    return index;
  }

  let searchIndex = [];

  function setupFinder() {
    searchIndex = buildSearchIndex();
    const input = document.getElementById('finder-input');
    const resultsBox = document.getElementById('finder-results');
    let currentMatches = [];

    function runFinder(q) {
      const tokens = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
      if (!tokens.length) {
        resultsBox.classList.remove('open');
        return;
      }
      const scored = [];
      for (const item of searchIndex) {
        let score = 0;
        let allMatch = true;
        for (const tok of tokens) {
          if (item.searchText.includes(tok)) {
            score += item.title.toLowerCase().includes(tok) ? 4 : 2;
            if (item.type === 'Solver') score += 2;
          } else {
            allMatch = false;
          }
        }
        if (allMatch || score >= 4) {
          scored.push({ item, score: allMatch ? score + 10 : score });
        }
      }
      scored.sort((a, b) => b.score - a.score);
      currentMatches = scored.slice(0, 12).map(s => s.item);

      if (!currentMatches.length) {
        resultsBox.innerHTML = `<div class="finder-item"><div class="finder-item-sub">No direct match — try words like "reverberation", "A-weighted", "wall", "loudspeaker", "Helmholtz", "ERB", "deflection".</div></div>`;
      } else {
        resultsBox.innerHTML = currentMatches.map((m, idx) => `
          <div class="finder-item ${idx === 0 ? 'active' : ''}" data-idx="${idx}">
            <div>
              <div class="finder-item-title">${escapeHtml(m.title)}</div>
              <div class="finder-item-sub">${escapeHtml(m.sub)}</div>
            </div>
            <span class="finder-tag">${escapeHtml(m.tag)}</span>
          </div>
        `).join('');
        resultsBox.querySelectorAll('.finder-item').forEach(el => {
          el.addEventListener('click', () => {
            const idx = Number(el.dataset.idx);
            if (currentMatches[idx]) {
              currentMatches[idx].action();
              resultsBox.classList.remove('open');
              input.value = '';
            }
          });
        });
      }
      resultsBox.classList.add('open');
    }

    input.addEventListener('input', () => runFinder(input.value));
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        resultsBox.classList.remove('open');
        input.blur();
      } else if (e.key === 'Enter' && currentMatches.length > 0) {
        e.preventDefault();
        currentMatches[0].action();
        resultsBox.classList.remove('open');
        input.value = '';
      }
    });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.finder-wrap')) {
        resultsBox.classList.remove('open');
      }
    });
    // Keyboard shortcut '/' or Ctrl+K
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        input.focus();
        input.select();
      } else if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        input.focus();
      }
    });
  }

  // --- Solvers View ---
  function renderSolverSidebar(filterText = '') {
    const listEl = document.getElementById('solver-list');
    const q = filterText.toLowerCase().trim();
    const filtered = SOLVERS.filter(s =>
      !q || `${s.code} ${s.title} ${s.shortTitle} ${s.keywords} ${s.matches}`.toLowerCase().includes(q)
    );
    listEl.innerHTML = filtered.map(s => `
      <div class="solver-nav-item ${s.id === activeSolverId ? 'active' : ''}" data-id="${s.id}">
        <span class="solver-code">${s.code}</span>
        <div>
          <div>${escapeHtml(s.shortTitle)}</div>
          <div style="font-size:11px;color:var(--text-muted)">${escapeHtml(s.lecture)}</div>
        </div>
      </div>
    `).join('');
    listEl.querySelectorAll('.solver-nav-item').forEach(el => {
      el.addEventListener('click', () => selectSolver(el.dataset.id));
    });
  }

  function renderActiveSolver() {
    const solver = SOLVERS.find(s => s.id === activeSolverId);
    if (!solver) return;
    const container = document.getElementById('solver-main');

    const presetsHtml = (solver.presets || []).map((pr, idx) =>
      `<button class="btn btn-sm preset-btn" data-idx="${idx}">${escapeHtml(pr.name)}</button>`
    ).join('');

    const decisionsHtml = (solver.decisions || []).map(d => `
      <div class="decision-box">
        <span class="decision-tag">⚠ Decision Point: ${escapeHtml(d.tag)}</span>
        ${escapeHtml(d.text)}
      </div>
    `).join('');

    const fieldsHtml = solver.fields.map(f => {
      const val = solverState[solver.id][f.id];
      let inputEl = '';
      if (f.type === 'select') {
        inputEl = `<select class="field-input" data-field="${f.id}">
          ${f.options.map(o => `<option value="${escapeHtml(o.value)}" ${String(o.value) === String(val) ? 'selected' : ''}>${escapeHtml(o.label)}</option>`).join('')}
        </select>`;
      } else {
        inputEl = `<input class="field-input" type="${f.type === 'number' ? 'number' : 'text'}" ${f.step ? `step="${f.step}"` : ''} data-field="${f.id}" value="${escapeHtml(val)}" title="${escapeHtml(f.help || '')}">`;
      }
      return `
        <div class="field-group">
          <label class="field-label">
            <span>${escapeHtml(f.label)}</span>
            <span class="field-unit">${escapeHtml(f.unit || '')}</span>
          </label>
          ${inputEl}
        </div>
      `;
    }).join('');

    container.innerHTML = `
      <div class="card">
        <div class="solver-title-row">
          <div>
            <h2 class="solver-title"><span class="brand-badge">${solver.code}</span> ${escapeHtml(solver.title)}</h2>
            <div class="solver-matches"><strong>Matches:</strong> ${escapeHtml(solver.matches)}</div>
          </div>
          <div style="display:flex;gap:6px;flex-wrap:wrap;">
            <button class="btn btn-sm" id="btn-reset-solver">Reset to Pre-filled Exam Problem</button>
          </div>
        </div>
        <p style="margin:8px 0 0;font-size:13.5px;color:var(--text-muted)">${escapeHtml(solver.description)}</p>
        <div class="decisions-grid">${decisionsHtml}</div>
        ${presetsHtml ? `<div class="presets-bar"><span style="font-size:12px;font-weight:700;align-self:center;color:var(--text-muted);">Presets:</span>${presetsHtml}</div>` : ''}
      </div>

      <div class="card">
        <div style="font-weight:700;margin-bottom:10px;font-size:14.5px;">Given Parameters (Edit numbers — results update live)</div>
        <div class="fields-grid" id="solver-fields">${fieldsHtml}</div>
      </div>

      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:8px;">
          <span style="font-weight:700;font-size:15px;">Live Results (Click any card to copy number)</span>
          <div style="display:flex;gap:8px;">
            <button class="btn btn-sm" id="btn-copy-working">Copy Worked Solution</button>
            <button class="btn btn-sm btn-primary" id="btn-add-handin">+ Add to Part 1 Hand-in Builder</button>
          </div>
        </div>
        <div class="highlights-grid" id="solver-highlights"></div>
        <div id="solver-warnings" style="margin-top:10px;"></div>
      </div>

      <div class="card">
        <div style="font-weight:700;font-size:15px;margin-bottom:10px;">Step-by-Step Worked Solution (Formula → Substituted Numbers → Result with Units)</div>
        <div id="solver-steps"></div>
        <div id="solver-extra-table"></div>
        <div style="margin-top:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
            <label style="font-weight:700;font-size:13px;">Ready-to-Paste Hand-in Text (Plain Text / Markdown for Part 1 PDF):</label>
            <button class="btn btn-sm" id="btn-copy-plain">Copy Plain Text</button>
          </div>
          <textarea class="copy-box" id="solver-plain-output" readonly></textarea>
        </div>
      </div>
    `;

    // Bind events
    container.querySelectorAll('.preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = Number(btn.dataset.idx);
        applyPreset(solver, solver.presets[idx]);
        renderActiveSolver();
      });
    });

    document.getElementById('btn-reset-solver').addEventListener('click', () => {
      for (const f of solver.fields) solverState[solver.id][f.id] = f.default;
      globalConsts.rho = 1.2;
      globalConsts.c = 343;
      document.getElementById('const-rho').value = 1.2;
      document.getElementById('const-c').value = 343;
      updateRhoCDisplay();
      renderActiveSolver();
    });

    container.querySelectorAll('[data-field]').forEach(inp => {
      inp.addEventListener('input', () => {
        const fid = inp.dataset.field;
        solverState[solver.id][fid] = inp.value;
        computeAndRenderResults(solver);
      });
    });

    computeAndRenderResults(solver);
  }

  function computeAndRenderResults(solver) {
    const inputs = Object.assign({}, solverState[solver.id], {
      rho: globalConsts.rho,
      c: globalConsts.c
    });
    let res;
    try {
      res = P.runSolver(solver.id, inputs);
    } catch (err) {
      document.getElementById('solver-highlights').innerHTML = `<div class="decision-box">Input error: ${escapeHtml(err.message)}</div>`;
      return;
    }

    // Highlights
    const hlBox = document.getElementById('solver-highlights');
    hlBox.innerHTML = res.highlights.map(h => `
      <div class="highlight-card" style="cursor:pointer;" title="Click to copy ${escapeHtml(h.value)} ${escapeHtml(h.unit)}" data-copy="${escapeHtml(h.value)} ${escapeHtml(h.unit)}">
        <div class="highlight-label">${escapeHtml(h.label)}</div>
        <div class="highlight-val-row">
          <span class="highlight-val">${escapeHtml(h.value)}</span>
          <span class="highlight-unit">${escapeHtml(h.unit)}</span>
        </div>
        <div class="highlight-sub">${escapeHtml(h.sub || '')}</div>
      </div>
    `).join('');
    hlBox.querySelectorAll('.highlight-card').forEach(card => {
      card.addEventListener('click', () => copyText(card.dataset.copy.trim(), `Copied: ${card.dataset.copy.trim()}`));
    });

    // Dynamic warnings
    const warnBox = document.getElementById('solver-warnings');
    warnBox.innerHTML = (res.warnings || []).map(w => `
      <div style="font-size:12.5px;padding:6px 10px;background:var(--bg-subtle);border-left:3px solid var(--accent);margin-top:5px;border-radius:4px;">
        ${escapeHtml(w)}
      </div>
    `).join('');

    // Steps
    const stepsBox = document.getElementById('solver-steps');
    stepsBox.innerHTML = res.steps.map(st => `
      <div class="step-item">
        <div class="step-title">${escapeHtml(st.title)}</div>
        <div class="step-formula">${renderMath(st.latex, true)}</div>
        <div class="step-sub"><strong>Substituted:</strong> ${escapeHtml(st.sub)}</div>
        <div class="step-res">⇒ ${escapeHtml(st.result)}</div>
      </div>
    `).join('');

    // Extra table for T09 Room Modes
    const extraTable = document.getElementById('solver-extra-table');
    if (solver.id === 'T09_room_modes' && res.vars.modeList) {
      const modes = res.vars.modeList.slice(0, 25);
      extraTable.innerHTML = `
        <div style="margin-top:10px;overflow-x:auto;">
          <div style="font-weight:700;font-size:13.5px;margin-bottom:6px;">Room Modes Table (first ${modes.length} modes below f_max):</div>
          <table class="data-table">
            <thead>
              <tr><th>#</th><th>(n_x, n_y, n_z)</th><th>f [Hz]</th><th>Type</th><th>Centre of Room</th></tr>
            </thead>
            <tbody>
              ${modes.map((m, idx) => `
                <tr class="${m.centreAudible ? 'oct-row' : ''}">
                  <td style="text-align:center">${idx + 1}</td>
                  <td style="text-align:center">(${m.nx}, ${m.ny}, ${m.nz})</td>
                  <td>${P.fmtFixed(m.f, 2)} Hz</td>
                  <td style="text-align:center">${m.typeName}</td>
                  <td style="text-align:center">${m.centreAudible ? 'MAX (all even)' : 'Node (0 Pa)'}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } else {
      extraTable.innerHTML = '';
    }

    // Build plain-text working for Part 1 PDF
    const givenSummary = solver.fields
      .map(f => `${f.label.replace(/^[A-Z0-9/()\s-]+:\s*/, '')}: ${solverState[solver.id][f.id]} ${f.unit || ''}`.trim())
      .join(', ');
    const plainLines = [
      `=== ${solver.code}: ${solver.title} ===`,
      `Constants: rho = ${globalConsts.rho} kg/m^3, c = ${globalConsts.c} m/s, rho*c = ${P.fmtNum(globalConsts.rho * globalConsts.c)} Pa*s/m, p_ref = 20 uPa`,
      `Given: ${givenSummary}`,
      '',
      ...res.steps.map(st => `${st.title}\n  Formula: ${st.latex}\n  Numbers: ${st.sub}\n  Result:  ${st.result}\n`),
      `Summary Answers:`,
      ...res.highlights.map(h => `  • ${h.label}: ${h.value} ${h.unit} (${h.sub})`)
    ].join('\n');

    const plainTa = document.getElementById('solver-plain-output');
    plainTa.value = plainLines;

    document.getElementById('btn-copy-working').onclick = () => copyText(plainLines, 'Copied full worked solution');
    document.getElementById('btn-copy-plain').onclick = () => copyText(plainLines, 'Copied plain-text working');
    document.getElementById('btn-add-handin').onclick = () => {
      const handinTa = document.getElementById('handin-scratchpad');
      handinTa.value = (handinTa.value ? handinTa.value + '\n\n' : '') + plainLines;
      try { localStorage.setItem('34840_handin_pad', handinTa.value); } catch (e) {}
      showToast('Added to Part 1 Hand-in Builder tab!');
    };
  }

  // --- Quick Tools View ---
  function renderQuickTools() {
    const container = document.getElementById('view-tools');
    const bandRowsHtml = P.FA_TABLE.map((f, i) => {
      const isOct = P.OCTAVE_CENTRES.includes(f);
      const fl3 = f / Math.pow(2, 1 / 6);
      const fu3 = f * Math.pow(2, 1 / 6);
      const fl1 = isOct ? f / Math.SQRT2 : null;
      const fu1 = isOct ? f * Math.SQRT2 : null;
      return `
        <tr class="${isOct ? 'oct-row' : ''}">
          <td style="text-align:center">${f} ${isOct ? '★' : ''}</td>
          <td>${P.fmtFixed(fl3, 1)} – ${P.fmtFixed(fu3, 1)}</td>
          <td>${isOct ? `${P.fmtFixed(fl1, 1)} – ${P.fmtFixed(fu1, 1)}` : '—'}</td>
          <td>${P.KA_TABLE[i] > 0 ? '+' : ''}${P.fmtFixed(P.KA_TABLE[i], 1)}</td>
          <td>${P.KC_TABLE[i] > 0 ? '+' : ''}${P.fmtFixed(P.KC_TABLE[i], 1)}</td>
        </tr>
      `;
    }).join('');

    container.innerHTML = `
      <div class="tools-grid">
        <!-- Tool 1: dB Calculator -->
        <div class="card">
          <h3 style="margin-top:0">1. Quick dB Add / Subtract / Coherent Phase</h3>
          <div class="field-group" style="margin-bottom:8px;">
            <label class="field-label"><span>Uncorrelated Levels to Add / Average (comma-sep)</span><span class="field-unit">dB</span></label>
            <input class="field-input" id="qt-db-list" value="70, 75, 80, 42">
          </div>
          <div id="qt-db-res" class="step-res" style="margin-bottom:12px;"></div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px;">
            <div class="field-group">
              <label class="field-label"><span>Total Level (Source+Bg)</span><span class="field-unit">dB</span></label>
              <input class="field-input" type="number" id="qt-bg-tot" value="80">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Background Level L_bg</span><span class="field-unit">dB</span></label>
              <input class="field-input" type="number" id="qt-bg-bg" value="75">
            </div>
          </div>
          <div id="qt-bg-res" class="step-res" style="margin-bottom:12px;"></div>

          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
            <div class="field-group">
              <label class="field-label"><span>Coherent L₁</span><span class="field-unit">dB</span></label>
              <input class="field-input" type="number" id="qt-coh-l1" value="90">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Coherent L₂</span><span class="field-unit">dB</span></label>
              <input class="field-input" type="number" id="qt-coh-l2" value="90">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Phase φ</span><span class="field-unit">deg</span></label>
              <input class="field-input" type="number" id="qt-coh-phi" value="120">
            </div>
          </div>
          <div id="qt-coh-res" class="step-res"></div>
        </div>

        <!-- Tool 2: Pa / W/m^2 / W <-> dB -->
        <div class="card">
          <h3 style="margin-top:0">2. Acoustic Quantities ↔ dB Converter</h3>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:8px;">
            <div class="field-group">
              <label class="field-label"><span>Pressure p</span><span class="field-unit">Pa</span></label>
              <input class="field-input" type="number" step="0.01" id="qt-p-val" value="0.02">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Peak or RMS?</span></label>
              <select class="field-input" id="qt-p-mode">
                <option value="peak">Peak Amplitude (÷√2)</option>
                <option value="rms">RMS Pressure</option>
              </select>
            </div>
            <div class="field-group">
              <label class="field-label"><span>Or from SPL L_p</span><span class="field-unit">dB</span></label>
              <input class="field-input" type="number" step="0.5" id="qt-lp-val" value="80">
            </div>
          </div>
          <div id="qt-p-res" class="step-res" style="margin-bottom:12px;"></div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div class="field-group">
              <label class="field-label"><span>Intensity I [W/m²] → L_I</span></label>
              <input class="field-input" type="text" id="qt-i-val" value="459.3e-9">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Power W [W] → L_W</span></label>
              <input class="field-input" type="text" id="qt-w-val" value="2.1e-3">
            </div>
          </div>
          <div id="qt-iw-res" class="step-res"></div>
        </div>

        <!-- Tool 3: Wavelength, k, ka, kr & Near Field -->
        <div class="card">
          <h3 style="margin-top:0">3. λ, k, ka, kr, Near-Field Phase & c(T)</h3>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
            <div class="field-group">
              <label class="field-label"><span>Frequency f</span><span class="field-unit">Hz</span></label>
              <input class="field-input" type="number" id="qt-wave-f" value="189">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Distance / Radius r (or a)</span><span class="field-unit">m</span></label>
              <input class="field-input" type="number" step="0.05" id="qt-wave-r" value="0.5">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Air Temp T</span><span class="field-unit">°C</span></label>
              <input class="field-input" type="number" id="qt-wave-t" value="20">
            </div>
          </div>
          <div id="qt-wave-res" class="step-res"></div>
        </div>

        <!-- Tool 4: Unit, Material & Deflection Converter -->
        <div class="card">
          <h3 style="margin-top:0">4. Wall Surface Mass, Deflection & Unit Helper</h3>
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:8px;">
            <div class="field-group">
              <label class="field-label"><span>Bulk Density ρ_M</span><span class="field-unit">kg/m³</span></label>
              <input class="field-input" type="number" id="qt-mat-rho" value="1200">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Thickness h</span><span class="field-unit">mm</span></label>
              <input class="field-input" type="number" id="qt-mat-h" value="13">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Freq for Mass Law</span><span class="field-unit">Hz</span></label>
              <input class="field-input" type="number" id="qt-mat-f" value="600">
            </div>
          </div>
          <div id="qt-mat-res" class="step-res" style="margin-bottom:12px;"></div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div class="field-group">
              <label class="field-label"><span>Static Deflection ξ₀</span><span class="field-unit">cm</span></label>
              <input class="field-input" type="number" step="0.1" id="qt-def-cm" value="1.0">
            </div>
            <div class="field-group">
              <label class="field-label"><span>Density in g/cm³</span><span class="field-unit">g/cm³</span></label>
              <input class="field-input" type="number" step="0.05" id="qt-dens-gcm" value="0.1">
            </div>
          </div>
          <div id="qt-def-res" class="step-res"></div>
        </div>
      </div>

      <!-- Tool 5: Octave & Third-Octave Band Classifier + Full A/C Table -->
      <div class="card" style="margin-top:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:10px;">
          <h3 style="margin:0">5. Octave / Third-Octave Band Lookup & A/C-Weighting (Table 1.3.2)</h3>
          <div style="display:flex;align-items:center;gap:8px;">
            <label style="font-weight:700;font-size:13px;">Check Any Frequency f [Hz]:</label>
            <input class="field-input" type="number" id="qt-band-f" value="400" style="width:110px;">
            <span id="qt-band-lookup-res" style="font-family:var(--font-mono);font-weight:700;color:var(--accent);"></span>
          </div>
        </div>
        <div style="max-height:360px;overflow-y:auto;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nominal f_c [Hz] (★ = 1/1 Oct)</th>
                <th>1/3-Octave Edges [Hz] (f_c·2^{±1/6})</th>
                <th>1/1-Octave Edges [Hz] (f_c/√2 .. f_c√2)</th>
                <th>A-Weighting K_A [dB]</th>
                <th>C-Weighting K_C [dB]</th>
              </tr>
            </thead>
            <tbody>${bandRowsHtml}</tbody>
          </table>
        </div>
      </div>
    `;

    function updateQuickTools() {
      const C = { rho: globalConsts.rho, c: globalConsts.c, rho_c: globalConsts.rho * globalConsts.c, p_ref: 20e-6 };

      // 1. dB list
      const list = P.parseNumberList(document.getElementById('qt-db-list').value);
      if (list.length) {
        const sumE = list.reduce((a, b) => a + Math.pow(10, b / 10), 0);
        const lSum = 10 * Math.log10(sumE);
        const lAvg = 10 * Math.log10(sumE / list.length);
        document.getElementById('qt-db-res').textContent = `Uncorrelated Sum = ${P.fmtFixed(lSum, 2)} dB  |  Energy Average = ${P.fmtFixed(lAvg, 2)} dB (N = ${list.length})`;
      }
      const lTot = Number(document.getElementById('qt-bg-tot').value);
      const lBg = Number(document.getElementById('qt-bg-bg').value);
      const diffBg = Math.pow(10, lTot / 10) - Math.pow(10, lBg / 10);
      document.getElementById('qt-bg-res').textContent = diffBg > 0
        ? `Background-Corrected Source L_src = ${P.fmtFixed(10 * Math.log10(diffBg), 2)} dB (ΔL = ${P.fmtFixed(lTot - lBg, 1)} dB)`
        : 'Invalid: L_tot must exceed L_bg';

      const l1 = Number(document.getElementById('qt-coh-l1').value);
      const l2 = Number(document.getElementById('qt-coh-l2').value);
      const phi = Number(document.getElementById('qt-coh-phi').value);
      const p1 = C.p_ref * Math.pow(10, l1 / 20);
      const p2 = C.p_ref * Math.pow(10, l2 / 20);
      const pCoh = Math.sqrt(p1 * p1 + p2 * p2 + 2 * p1 * p2 * Math.cos(phi * Math.PI / 180));
      const lCoh = pCoh > 0 ? 20 * Math.log10(pCoh / C.p_ref) : -Infinity;
      document.getElementById('qt-coh-res').textContent = `Coherent Sum (φ=${phi}°) = ${P.fmtFixed(lCoh, 2)} dB (Incoherent would be ${P.fmtFixed(10 * Math.log10(Math.pow(10, l1 / 10) + Math.pow(10, l2 / 10)), 2)} dB)`;

      // 2. Pressure & SPL
      const pVal = Number(document.getElementById('qt-p-val').value);
      const pMode = document.getElementById('qt-p-mode').value;
      const pRms = pMode === 'peak' ? pVal / Math.SQRT2 : pVal;
      const pPeak = pMode === 'peak' ? pVal : pVal * Math.SQRT2;
      const lpFromP = pRms > 0 ? 20 * Math.log10(pRms / C.p_ref) : -Infinity;
      const lpIn = Number(document.getElementById('qt-lp-val').value);
      const pRmsFromLp = C.p_ref * Math.pow(10, lpIn / 20);
      document.getElementById('qt-p-res').textContent = `${pVal} Pa (${pMode}) ⇒ p_rms = ${P.fmtNum(pRms, 4)} Pa, p̂ = ${P.fmtNum(pPeak, 4)} Pa, L_p = ${P.fmtFixed(lpFromP, 2)} dB  |  From ${lpIn} dB ⇒ p_rms = ${P.fmtNum(pRmsFromLp, 4)} Pa (p̂ = ${P.fmtNum(pRmsFromLp * Math.SQRT2, 4)} Pa)`;

      const iVal = Number(document.getElementById('qt-i-val').value);
      const wVal = Number(document.getElementById('qt-w-val').value);
      const lI = iVal > 0 ? 10 * Math.log10(iVal / 1e-12) : -Infinity;
      const lW = wVal > 0 ? 10 * Math.log10(wVal / 1e-12) : -Infinity;
      document.getElementById('qt-iw-res').textContent = `I = ${P.fmtNum(iVal, 4)} W/m² ⇒ L_I = ${P.fmtFixed(lI, 2)} dB  |  W = ${P.fmtNum(wVal, 4)} W ⇒ L_W = ${P.fmtFixed(lW, 2)} dB`;

      // 3. Wave & near field
      const wf = Number(document.getElementById('qt-wave-f').value);
      const wr = Number(document.getElementById('qt-wave-r').value);
      const wt = Number(document.getElementById('qt-wave-t').value);
      const lam = C.c / wf;
      const w = 2 * Math.PI * wf;
      const k = w / C.c;
      const kr = k * wr;
      const nfPhase = Math.atan(1 / kr) * 180 / Math.PI;
      const cTemp = 20.05 * Math.sqrt(273.15 + wt);
      document.getElementById('qt-wave-res').textContent = `λ = ${P.fmtNum(lam, 4)} m (λ/4 = ${P.fmtNum(lam / 4, 3)} m, λ/2 = ${P.fmtNum(lam / 2, 3)} m) · k = ${P.fmtNum(k, 4)} rad/m · kr (or ka) = ${P.fmtFixed(kr, 3)} · Monopole p–u phase = ${P.fmtFixed(nfPhase, 1)}° · c(${wt}°C) = ${P.fmtFixed(cTemp, 1)} m/s`;

      // 4. Material & deflection
      const mRho = Number(document.getElementById('qt-mat-rho').value);
      const mH = Number(document.getElementById('qt-mat-h').value) / 1000;
      const mF = Number(document.getElementById('qt-mat-f').value);
      const mSurf = mRho * mH;
      const R0 = 20 * Math.log10((2 * Math.PI * mF * mSurf) / (2 * C.rho_c));
      document.getElementById('qt-mat-res').textContent = `Surface mass m = ${P.fmtFixed(mSurf, 2)} kg/m² · At ${mF} Hz: R₀ (normal) = ${P.fmtFixed(R0, 2)} dB, R_field (-5 dB) = ${P.fmtFixed(R0 - 5, 2)} dB`;

      const defCm = Number(document.getElementById('qt-def-cm').value);
      const xi0 = defCm / 100;
      const f0 = Math.sqrt(9.81 / xi0) / (2 * Math.PI);
      const gcm = Number(document.getElementById('qt-dens-gcm').value);
      document.getElementById('qt-def-res').textContent = `ξ₀ = ${defCm} cm (${xi0} m) ⇒ f₀ = ${P.fmtFixed(f0, 2)} Hz, Isolation starts at √2·f₀ = ${P.fmtFixed(Math.SQRT2 * f0, 2)} Hz  |  ${gcm} g/cm³ = ${gcm * 1000} kg/m³`;

      // 5. Band classifier
      const bf = Number(document.getElementById('qt-band-f').value);
      const ka = P.interpAWeight(bf);
      const kc = P.interpCWeight(bf);
      let octMatch = 'None';
      for (const oc of P.OCTAVE_CENTRES) {
        if (bf >= oc / Math.SQRT2 && bf < oc * Math.SQRT2) {
          octMatch = `${oc} Hz [${P.fmtFixed(oc / Math.SQRT2, 1)}–${P.fmtFixed(oc * Math.SQRT2, 1)} Hz]`;
          break;
        }
      }
      document.getElementById('qt-band-lookup-res').textContent = `1/1 Octave: ${octMatch} · K_A(${bf} Hz) = ${ka > 0 ? '+' : ''}${P.fmtFixed(ka, 2)} dB · K_C = ${kc > 0 ? '+' : ''}${P.fmtFixed(kc, 2)} dB`;
    }

    container.querySelectorAll('input, select').forEach(el => {
      el.addEventListener('input', updateQuickTools);
    });
    updateQuickTools();
  }

  // --- Cheat Sheet & Worked Part 1 View ---
  function renderCheatSheet(filterQuery = '') {
    const container = document.getElementById('cs-content');
    const q = filterQuery.toLowerCase().trim();

    const filteredSecs = CS.sections.filter(sec =>
      !q || `${sec.title} ${sec.keywords} ${sec.items.map(i => i.label + ' ' + i.note + ' ' + i.formula).join(' ')}`.toLowerCase().includes(q)
    );

    const filteredP1 = CS.workedPart1.filter(p =>
      !q || `${p.year} ${p.problem} ${p.summary} ${p.steps.join(' ')}`.toLowerCase().includes(q)
    );

    const secsHtml = filteredSecs.map(sec => `
      <div class="card" id="${sec.id}" style="margin-bottom:14px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:8px;">
          <h3 style="margin:0;color:var(--accent);">${escapeHtml(sec.title)}</h3>
          <button class="btn btn-sm cs-jump-solver" data-solver="${sec.solver}">Open Solver ${sec.solver} →</button>
        </div>
        ${sec.items.map(item => `
          <div class="step-item" style="margin-bottom:8px;">
            <div style="font-weight:700;font-size:13.5px;">${escapeHtml(item.label)}</div>
            <div class="step-formula">${renderMath(item.formula, true)}</div>
            <div style="font-size:13px;color:var(--text-muted);">${escapeHtml(item.note)}</div>
          </div>
        `).join('')}
      </div>
    `).join('');

    const p1Html = filteredP1.map(p => `
      <div class="card" style="margin-bottom:12px;border-left:4px solid var(--accent);">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;flex-wrap:wrap;gap:8px;">
          <h3 style="margin:0;font-size:16px;">${escapeHtml(p.problem)}</h3>
          <button class="btn btn-sm cs-jump-solver" data-solver="${p.solver}">Load in ${p.solver} →</button>
        </div>
        <div style="font-size:13.5px;color:var(--text-muted);margin-bottom:8px;">${escapeHtml(p.summary)}</div>
        <ol style="margin:0;padding-left:20px;font-size:13.5px;">
          ${p.steps.map(st => `<li style="margin-bottom:4px;">${escapeHtml(st)}</li>`).join('')}
        </ol>
      </div>
    `).join('');

    container.innerHTML = `
      ${secsHtml}
      <h2 style="margin:20px 0 10px;">Worked Part 1 Old Exam Problems (2022–2024)</h2>
      ${p1Html}
    `;

    container.querySelectorAll('.cs-jump-solver').forEach(btn => {
      btn.addEventListener('click', () => selectSolver(btn.dataset.solver));
    });
  }

  // --- Multiple-Choice Drill View (All 45 Questions 2022–2024) ---
  const mcUserChoices = {};
  let mcYearFilter = 'ALL';
  let mcTopicFilter = 'ALL';
  let mcSearchQuery = '';
  let mcRevealAll = false;

  function renderMCView() {
    const listContainer = document.getElementById('mc-list');
    const q = mcSearchQuery.toLowerCase().trim();

    const filtered = MC.filter(item => {
      if (mcYearFilter !== 'ALL' && String(item.year) !== mcYearFilter) return false;
      if (mcTopicFilter !== 'ALL' && item.topic !== mcTopicFilter) return false;
      if (q && !`${item.id} ${item.topic} ${item.question} ${item.reason} ${item.trap}`.toLowerCase().includes(q)) return false;
      return true;
    });

    // Update score badge
    const answeredIds = Object.keys(mcUserChoices);
    const correctCount = answeredIds.filter(id => {
      const qObj = MC.find(m => m.id === id);
      return qObj && mcUserChoices[id] === qObj.answer;
    }).length;
    document.getElementById('mc-score').textContent = `Score: ${correctCount} / ${answeredIds.length} answered (${filtered.length} shown of ${MC.length})`;

    listContainer.innerHTML = filtered.map(item => {
      const chosen = mcUserChoices[item.id];
      const showAns = mcRevealAll || Boolean(chosen);
      return `
        <div class="mc-card" id="mc-${item.id}">
          <div class="mc-header">
            <div>
              <span class="brand-badge">${escapeHtml(item.id)}</span>
              <span style="font-weight:700;margin-left:8px;color:var(--accent);">${escapeHtml(item.topic)}</span>
            </div>
            <button class="btn btn-sm mc-jump-solver" data-solver="${item.solver}">Open Solver ${item.solver} →</button>
          </div>
          <div style="font-weight:600;font-size:14.5px;margin-bottom:8px;">${escapeHtml(item.question)}</div>
          <div class="mc-options">
            ${['A', 'B', 'C', 'D'].map(letter => {
              let cls = '';
              if (showAns) {
                if (letter === item.answer) cls = 'correct';
                else if (chosen === letter && letter !== item.answer) cls = 'wrong';
              }
              return `
                <button class="mc-opt ${cls}" data-id="${item.id}" data-letter="${letter}">
                  <strong>${letter})</strong>
                  <span>${escapeHtml(item.options[letter])}</span>
                </button>
              `;
            }).join('')}
          </div>
          <div class="mc-explain ${showAns ? 'visible' : ''}">
            <div><strong>Correct Answer: ${item.answer}</strong> — ${escapeHtml(item.reason)}</div>
            <div style="margin-top:4px;color:var(--warn);"><strong>Classic Trap:</strong> ${escapeHtml(item.trap)}</div>
          </div>
        </div>
      `;
    }).join('');

    listContainer.querySelectorAll('.mc-opt').forEach(btn => {
      btn.addEventListener('click', () => {
        mcUserChoices[btn.dataset.id] = btn.dataset.letter;
        renderMCView();
      });
    });

    listContainer.querySelectorAll('.mc-jump-solver').forEach(btn => {
      btn.addEventListener('click', () => selectSolver(btn.dataset.solver));
    });
  }

  // --- Final Checklist & Part 1 Hand-in Builder View ---
  function renderChecklistView() {
    const container = document.getElementById('view-checklist');
    let savedChecks = {};
    let savedPad = '';
    try {
      savedChecks = JSON.parse(localStorage.getItem('34840_checks') || '{}');
      savedPad = localStorage.getItem('34840_handin_pad') || '';
    } catch (e) {}

    container.innerHTML = `
      <div class="tools-grid">
        <div class="card no-print">
          <h3 style="margin-top:0">Exam-Day Time Plan (4 Hours: 09:00–13:00)</h3>
          <table class="data-table" style="font-family:var(--font-sans);">
            <thead>
              <tr><th>Time</th><th>Phase</th><th>Action</th></tr>
            </thead>
            <tbody>
              ${CS.checklist.timePlan.map(tp => `
                <tr>
                  <td style="text-align:left;white-space:nowrap;font-family:var(--font-mono);font-weight:700;">${escapeHtml(tp.time)}</td>
                  <td style="text-align:left;font-weight:700;color:var(--accent);">${escapeHtml(tp.phase)}</td>
                  <td style="text-align:left;">${escapeHtml(tp.detail)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>

          <h3 style="margin:16px 0 8px;">Interactive Final-Check List</h3>
          <div>
            ${CS.checklist.items.map(it => `
              <label style="display:flex;align-items:flex-start;gap:8px;padding:7px 0;border-bottom:1px solid var(--border);cursor:pointer;">
                <input type="checkbox" class="chk-item" data-id="${it.id}" ${savedChecks[it.id] ? 'checked' : ''} style="margin-top:3px;">
                <span><strong>[${escapeHtml(it.cat)}]</strong> ${escapeHtml(it.text)}</span>
              </label>
            `).join('')}
          </div>
        </div>

        <div class="card">
          <div class="no-print" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin-bottom:8px;">
            <h3 style="margin:0">Part 1 Hand-in Scratchpad & PDF Builder</h3>
            <div style="display:flex;gap:6px;flex-wrap:wrap;">
              <button class="btn btn-sm" id="btn-pad-copy">Copy All</button>
              <button class="btn btn-sm" id="btn-pad-download">Download .md</button>
              <button class="btn btn-sm btn-primary" id="btn-pad-print">Print / Save as PDF</button>
              <button class="btn btn-sm" id="btn-pad-clear">Clear</button>
            </div>
          </div>
          <p class="no-print" style="margin:0 0 8px;font-size:12.5px;color:var(--text-muted);">
            Click <strong>"+ Add to Part 1 Hand-in Builder"</strong> in any solver to append its step-by-step solution here. Edit freely, then copy into your document or click <strong>Print / Save as PDF</strong>.
          </p>
          <textarea class="copy-box" id="handin-scratchpad" style="min-height:420px;" placeholder="Your Part 1 worked solutions will appear here...">${escapeHtml(savedPad)}</textarea>
          <pre id="handin-print-view" style="display:none;white-space:pre-wrap;font-family:var(--font-mono);font-size:12.5px;"></pre>
        </div>
      </div>
    `;

    container.querySelectorAll('.chk-item').forEach(cb => {
      cb.addEventListener('change', () => {
        savedChecks[cb.dataset.id] = cb.checked;
        try { localStorage.setItem('34840_checks', JSON.stringify(savedChecks)); } catch (e) {}
      });
    });

    const pad = document.getElementById('handin-scratchpad');
    pad.addEventListener('input', () => {
      try { localStorage.setItem('34840_handin_pad', pad.value); } catch (e) {}
    });

    document.getElementById('btn-pad-copy').addEventListener('click', () => copyText(pad.value, 'Copied full Part 1 hand-in'));
    document.getElementById('btn-pad-clear').addEventListener('click', () => {
      pad.value = '';
      try { localStorage.removeItem('34840_handin_pad'); } catch (e) {}
    });
    document.getElementById('btn-pad-download').addEventListener('click', () => {
      const blob = new Blob([pad.value], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = '34840_exam_part1.md';
      a.click();
      URL.revokeObjectURL(url);
    });
    document.getElementById('btn-pad-print').addEventListener('click', () => {
      const pv = document.getElementById('handin-print-view');
      pv.textContent = pad.value;
      pv.style.display = 'block';
      pad.style.display = 'none';
      container.classList.add('print-target');
      window.print();
      pv.style.display = 'none';
      pad.style.display = 'block';
      container.classList.remove('print-target');
    });
  }

  function updateRhoCDisplay() {
    const el = document.getElementById('const-rhoc');
    if (el) el.textContent = P.fmtNum(globalConsts.rho * globalConsts.c, 4);
  }

  // --- Boot ---
  function init() {
    // Nav tabs
    document.querySelectorAll('.nav-tab').forEach(btn => {
      btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // Global constants
    const rhoInp = document.getElementById('const-rho');
    const cInp = document.getElementById('const-c');
    rhoInp.addEventListener('input', () => {
      globalConsts.rho = Number(rhoInp.value) || 1.2;
      updateRhoCDisplay();
      renderActiveSolver();
    });
    cInp.addEventListener('input', () => {
      globalConsts.c = Number(cInp.value) || 343;
      updateRhoCDisplay();
      renderActiveSolver();
    });
    document.getElementById('btn-reset-consts').addEventListener('click', () => {
      globalConsts.rho = 1.2;
      globalConsts.c = 343;
      rhoInp.value = 1.2;
      cInp.value = 343;
      updateRhoCDisplay();
      renderActiveSolver();
    });

    // Theme toggle
    const themeBtn = document.getElementById('btn-theme');
    themeBtn.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
      themeBtn.textContent = isDark ? 'Dark Theme' : 'Light Theme';
    });

    // Sidebar filter
    const sbFilter = document.getElementById('sidebar-filter');
    sbFilter.addEventListener('input', () => renderSolverSidebar(sbFilter.value));

    // Cheat sheet search
    const csSearch = document.getElementById('cs-search');
    csSearch.addEventListener('input', () => renderCheatSheet(csSearch.value));

    // MC controls
    document.getElementById('mc-year-filter').addEventListener('change', (e) => {
      mcYearFilter = e.target.value;
      renderMCView();
    });
    document.getElementById('mc-topic-filter').addEventListener('change', (e) => {
      mcTopicFilter = e.target.value;
      renderMCView();
    });
    document.getElementById('mc-search').addEventListener('input', (e) => {
      mcSearchQuery = e.target.value;
      renderMCView();
    });
    document.getElementById('btn-mc-reveal').addEventListener('click', (e) => {
      mcRevealAll = !mcRevealAll;
      e.target.textContent = mcRevealAll ? 'Hide Answers (Quiz Mode)' : 'Study Mode: Reveal All 45 Answers';
      renderMCView();
    });
    document.getElementById('btn-mc-reset').addEventListener('click', () => {
      for (const k of Object.keys(mcUserChoices)) delete mcUserChoices[k];
      mcRevealAll = false;
      document.getElementById('btn-mc-reveal').textContent = 'Study Mode: Reveal All 45 Answers';
      renderMCView();
    });

    setupFinder();
    renderSolverSidebar();
    renderActiveSolver();
    renderQuickTools();
    renderCheatSheet();
    renderMCView();
    renderChecklistView();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
