#!/usr/bin/env node
// Builds one self-contained offline file: acoustics-formulas.html (KaTeX and its fonts inlined).
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const KATEX = path.join(ROOT, '..', 'app', 'vendor', 'katex');
const read = p => fs.readFileSync(p, 'utf8');
const safeJs = s => s.replace(/<\/script/gi, '<\\/script');

const katexCss = read(path.join(KATEX, 'katex.min.css')).replace(/@font-face\{[^}]+\}/g, rule => {
  const m = rule.match(/url\(fonts\/([A-Za-z0-9_-]+\.woff2)\)/);
  const file = m && path.join(KATEX, 'fonts', m[1]);
  if (!file || !fs.existsSync(file)) return '';
  return rule.replace(/src:[^;}]+/, `src:url(data:font/woff2;base64,${fs.readFileSync(file).toString('base64')}) format("woff2")`);
});

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Acoustics formulas · 34840</title>
<style>${katexCss}</style>
<style>${read(path.join(ROOT, 'src', 'style.css'))}</style>
</head>
<body>
<div class="shell">
  <aside class="side">
    <div class="brand">Acoustics formulas<span>34840 · works offline</span></div>
    <input id="search" placeholder="Search  ( / )" spellcheck="false" autocomplete="off">
    <nav id="topics"></nav>
    <nav id="examnotes" title="Opens in Obsidian"></nav>
    <div class="side-foot">
      <div id="consts"></div>
      <button id="theme">Dark</button>
    </div>
  </aside>
  <main id="main"></main>
</div>
<div id="toast"></div>
<script>${safeJs(read(path.join(KATEX, 'katex.min.js')))}</script>
<script>${safeJs(read(path.join(ROOT, 'src', 'formulas.js')))}</script>
<script>${safeJs(read(path.join(ROOT, 'src', 'engine.js')))}</script>
<script>${safeJs(read(path.join(ROOT, 'src', 'app.js')))}</script>
</body>
</html>
`;
const out = path.join(ROOT, 'acoustics-formulas.html');
fs.writeFileSync(out, html);
const ext = html.match(/https?:\/\/[^\s"'<>)]+/g) || [];
console.log(`wrote ${path.basename(out)} (${(html.length / 1024).toFixed(0)} KB)`);
if (ext.length) console.log(`note: ${ext.length} URL strings inside (KaTeX licence/docs text), none are loaded`);
