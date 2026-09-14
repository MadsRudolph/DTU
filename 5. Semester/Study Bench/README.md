# The Study Bench

Interactive study sites for the DTU 5th-semester courses, one per course, built from
the lecture notes, slides and problem sheets in the vault and kept in step with them.

- **Public:** https://study.madsrudolph.dev — hub; `/34870/` *The Analogy Bench*
  (Electroacoustics), `/34840/` *The Sound Bench* (Fundamentals of Acoustics and Noise Control).
  Cloudflare Worker with static assets (`wrangler.jsonc`, `npm run deploy:cf`).
- **Home server (LAN):** http://192.168.50.220 — Proxmox CT 116 `study`, nginx, self-syncs
  from the public site every 30 min (`mirror/`); `./deploy.sh` pushes immediately.
- **Claude artifacts (same builds):** 34870 https://claude.ai/code/artifact/a2ca9f90-949a-40ad-bea6-2fe4bf114277 · 34840 https://claude.ai/code/artifact/5c6961ee-179e-4cff-918b-79d2f86e14eb

## Layout

- `core/` — the toolkit shared by every course: `app.js` (complex maths, `Plot`, circuit
  drawing, sliders/readouts, quiz engine, KaTeX rendering) and `style.css`.
- `courses/<code>/` — one self-contained site: `index.html`, `benches.js` (the playgrounds),
  `problems.js` (problem sets with official solutions), `quiz.js`, optionally `theme.css`
  (course colours), `labs.js`, `diagrams.js`.
- `hub/index.html` — the landing page.
- `build.py` → `dist/` (hub at the root, `dist/<code>/` per course, KaTeX inlined with its
  fonts as data URIs, `artifact.html` per course, `manifest.json` for the mirror).
- `vendor/katex/` — KaTeX 0.16.22 with the fonts actually used.

## Working on it

```bash
cd "5. Semester/Study Bench"
npm install                 # once per clone (wrangler)
npx wrangler login          # once per PC
python3 build.py            # → dist/
npm run deploy:cf           # build + deploy to study.madsrudolph.dev
./deploy.sh                 # LAN mirror now (needs ssh to 192.168.50.200)
```

Local preview: launch config `study-bench` (python http.server on 8642, serving `dist/`).
The rules for adding a lecture, a lab, a problem set or a whole course are in the
project skill `.claude/skills/study-bench/SKILL.md`; a PostToolUse hook reminds Claude Code
whenever a note for one of the courses is written.
