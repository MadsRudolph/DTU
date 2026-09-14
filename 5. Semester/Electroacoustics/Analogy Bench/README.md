# The Analogy Bench

Interactive study site for **34870 Electroacoustics, lectures 0–5** (analogies,
mechanical and acoustic systems, transducers, dynamic / directional / condenser
microphones). Every plot is computed live in the browser from the same formulas
as the lecture notes; the bench start values reproduce the worked problem answers
(Problem 4.4b, Problems 4 design, Problem 5.1).

- **Public:** https://study.madsrudolph.dev — Cloudflare Worker with static assets (`wrangler.jsonc`, `npm run deploy:cf`), custom domain on the madsrudolph.dev zone.
- **Home server (LAN):** http://192.168.50.220 — Proxmox CT 116 `study`, nginx (`npm run deploy:lan`).
- **Anywhere:** https://claude.ai/code/artifact/a2ca9f90-949a-40ad-bea6-2fe4bf114277 (Claude artifact, same build; republish from the session that owns it or pass the URL as `url`).
- **Source:** `src/` (`index.html`, `style.css`, `app.js` maths + plots + circuit
  drawing, `benches.js` the playgrounds, `diagrams.js` static circuits, `quiz.js`).
- **Build:** `python3 build.py` → `dist/`. Inlines the KaTeX stylesheet with its
  fonts as data URIs so the bundle has no external stylesheet/font requests
  (Google Fonts for the page type is the one optional external request).
  `dist/artifact.html` is the same page without the html/head/body skeleton, for
  publishing as a Claude artifact.
- **Deploy:** `npm run deploy:cf` (public) and/or `./deploy.sh` (LAN: build → scp to the Proxmox host → `pct push` → CT 116).
- **Local preview:** `.claude/launch.json` config `analogy-bench` (python http.server on 8642).

Cloudflare auth is the Wrangler OAuth login in `~/.config/.wrangler/config/default.toml`
(scopes: workers, routes, zone read). `npm install` once per clone to get wrangler.
