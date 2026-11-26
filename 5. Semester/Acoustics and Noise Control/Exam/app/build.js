#!/usr/bin/env node
// Build script for 34840 Exam App
// Bundles KaTeX (JS + CSS + base64-inlined WOFF2 math fonts) and all app modules
// into a single 100% self-contained offline file: exam-app.html

'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const VENDOR_KATEX = path.join(ROOT, 'vendor', 'katex');
const SRC = path.join(ROOT, 'src');
const OUT_FILE = path.join(ROOT, 'exam-app.html');

function buildInlineKatexCss() {
  const rawCss = fs.readFileSync(path.join(VENDOR_KATEX, 'katex.min.css'), 'utf8');
  const fontsDir = path.join(VENDOR_KATEX, 'fonts');

  // Replace every @font-face rule: if the .woff2 file exists locally, inline it as base64 data URI;
  // if the font file is not in vendor/katex/fonts (e.g. Fraktur/Script), strip that @font-face rule
  // so the browser never makes any file:// network requests for missing fonts.
  return rawCss.replace(/@font-face\{[^}]+\}/g, (rule) => {
    const m = rule.match(/url\(fonts\/([A-Za-z0-9_-]+\.woff2)\)/);
    if (!m) return '';
    const fontFile = path.join(fontsDir, m[1]);
    if (!fs.existsSync(fontFile)) return '';
    const b64 = fs.readFileSync(fontFile).toString('base64');
    return rule.replace(/src:[^;}]+/, `src:url(data:font/woff2;base64,${b64}) format("woff2")`);
  });
}

function readSrc(name) {
  return fs.readFileSync(path.join(SRC, name), 'utf8');
}

const katexCss = buildInlineKatexCss();
const katexJs = fs.readFileSync(path.join(VENDOR_KATEX, 'katex.min.js'), 'utf8');
const appCss = readSrc('styles.css');
const physicsJs = readSrc('physics.js');
const solversMetaJs = readSrc('solvers_meta.js');
const mcDataJs = readSrc('mc_data.js');
const cheatsheetDataJs = readSrc('cheatsheet_data.js');
const uiJs = readSrc('ui.js');

// Escape "</script" inside any JS payload just in case
function safeJs(code) {
  return code.replace(/<\/script/gi, '<\\/script');
}

const html = `<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>34840 Exam App — Fundamentals of Acoustics and Noise Control</title>
  <style id="katex-styles">${katexCss}</style>
  <style id="app-styles">${appCss}</style>
</head>
<body>
  <header class="app-header">
    <div class="header-top">
      <div class="brand">
        <span class="brand-badge">34840</span>
        <span>Acoustics &amp; Noise Control — Offline Exam Companion</span>
      </div>
      <div class="finder-wrap">
        <input
          type="text"
          id="finder-input"
          class="finder-input"
          placeholder="Which solver? Type words from the question (e.g. 'reverberation', 'A-weighted', 'two sources', 'Helmholtz', 'deflection')... [ / or Ctrl+K ]"
          autocomplete="off"
        >
        <div id="finder-results" class="finder-results"></div>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <button class="btn btn-sm" id="btn-theme">Dark Theme</button>
      </div>
    </div>
    <div class="header-bottom">
      <nav class="nav-tabs">
        <button class="nav-tab active" data-tab="solvers">1. Problem Solvers (T01–T15)</button>
        <button class="nav-tab" data-tab="tools">2. Quick Tools &amp; Tables</button>
        <button class="nav-tab" data-tab="cheatsheet">3. Cheat Sheet &amp; Worked Part 1</button>
        <button class="nav-tab" data-tab="mc">4. MC Drill (2022–2024 · 45 Qs)</button>
        <button class="nav-tab" data-tab="checklist">5. Hand-in Builder &amp; Checklist</button>
      </nav>
      <div class="consts-bar">
        <span><strong>Constants:</strong></span>
        <label>ρ <input type="number" id="const-rho" step="0.01" value="1.2"> kg/m³</label>
        <label>c <input type="number" id="const-c" step="1" value="343"> m/s</label>
        <span>⇒ ρc = <strong id="const-rhoc">411.6</strong> Pa·s/m</span>
        <span>· p_ref = 20 µPa</span>
        <button class="btn btn-sm" id="btn-reset-consts" title="Reset to exam paper standard (1.2 and 343)">Reset</button>
      </div>
    </div>
  </header>

  <!-- View 1: Problem Solvers (T01-T15) -->
  <main class="view-panel active" id="view-solvers">
    <div class="solvers-layout">
      <aside class="solver-sidebar">
        <input type="text" id="sidebar-filter" class="sidebar-filter" placeholder="Filter T01–T15 templates...">
        <div class="solver-list" id="solver-list"></div>
      </aside>
      <section class="solver-main" id="solver-main"></section>
    </div>
  </main>

  <!-- View 2: Quick Tools -->
  <section class="view-panel" id="view-tools"></section>

  <!-- View 3: Cheat Sheet & Worked Part 1 -->
  <section class="view-panel" id="view-cheatsheet">
    <div class="card" style="margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
        <div style="font-weight:700;font-size:16px;">Searchable Formula Cheat Sheet &amp; Worked 2022–2024 Part 1 Problems</div>
        <input type="text" id="cs-search" class="field-input" style="max-width:420px;width:100%;" placeholder="Filter formulas, topics, traps, or worked problems...">
      </div>
    </div>
    <div id="cs-content"></div>
  </section>

  <!-- View 4: Multiple-Choice Drill (2022-2024) -->
  <section class="view-panel" id="view-mc">
    <div class="card" style="margin-bottom:14px;">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
          <select id="mc-year-filter" class="field-input">
            <option value="ALL">All Years (2022–2024)</option>
            <option value="2022">2022 Exam (15 Qs)</option>
            <option value="2023">2023 Exam (15 Qs)</option>
            <option value="2024">2024 Exam (15 Qs)</option>
          </select>
          <select id="mc-topic-filter" class="field-input">
            <option value="ALL">All Topics (45 Qs)</option>
            <option value="Waves & Sources">Waves &amp; Sources (9 Qs)</option>
            <option value="Levels & Bands">Levels &amp; Bands (4 Qs)</option>
            <option value="Rooms & Modes">Rooms &amp; Modes (8 Qs)</option>
            <option value="Absorbers">Absorbers (4 Qs)</option>
            <option value="Sound Insulation">Sound Insulation (6 Qs)</option>
            <option value="Vibration">Vibration &amp; Isolation (6 Qs)</option>
            <option value="Hearing">Hearing: Psycho &amp; Physio (12 Qs)</option>
          </select>
          <input type="text" id="mc-search" class="field-input" style="min-width:220px;" placeholder="Search MC questions &amp; explanations...">
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
          <span id="mc-score" style="font-family:var(--font-mono);font-weight:700;font-size:13px;"></span>
          <button class="btn btn-sm btn-primary" id="btn-mc-reveal">Study Mode: Reveal All 45 Answers</button>
          <button class="btn btn-sm" id="btn-mc-reset">Reset Quiz</button>
        </div>
      </div>
    </div>
    <div id="mc-list"></div>
  </section>

  <!-- View 5: Hand-in Builder & Final Checklist -->
  <section class="view-panel" id="view-checklist"></section>

  <script id="katex-js">${safeJs(katexJs)}</script>
  <script id="physics-js">${safeJs(physicsJs)}</script>
  <script id="solvers-meta-js">${safeJs(solversMetaJs)}</script>
  <script id="mc-data-js">${safeJs(mcDataJs)}</script>
  <script id="cheatsheet-data-js">${safeJs(cheatsheetDataJs)}</script>
  <script id="ui-js">${safeJs(uiJs)}</script>
</body>
</html>
`;

fs.writeFileSync(OUT_FILE, html, 'utf8');
const sizeKB = (Buffer.byteLength(html, 'utf8') / 1024).toFixed(1);
console.log(`Built ${OUT_FILE} (${sizeKB} KB, 100% self-contained offline HTML).`);
