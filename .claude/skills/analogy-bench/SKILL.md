---
name: analogy-bench
description: REQUIRED whenever a 34870 Electroacoustics lecture note, problem set or lab is written or updated in the vault — the Analogy Bench study site (study.madsrudolph.dev) must be extended with the same material and redeployed, from either PC. Also use for "update the bench", "add lecture N to the site", "the study site", "study.madsrudolph.dev", "Analogy Bench".
---

# The Analogy Bench — keep the site in step with the lecture notes

The site lives in `5. Semester/Electroacoustics/Analogy Bench/` (repo-relative).
Public at **https://study.madsrudolph.dev**, LAN mirror at http://192.168.50.220
(CT 116 `study`, self-syncs from the public site every 30 min), and a Claude
artifact (URL in the README). One section per lecture, one interactive bench per
idea, one quiz per lecture. Every number shown must reproduce the worked answers
in the notes.

**Rule:** a 34870 lecture note without a matching site section is unfinished
work. Do the note first, then the site, then deploy, in the same task.

## 0. One-time per PC

```bash
cd "5. Semester/Electroacoustics/Analogy Bench" && npm install
npx wrangler whoami || npx wrangler login     # opens a browser once; token lands in ~/.config/.wrangler
```

If `wrangler login` cannot run (headless, no browser), still do everything else,
commit + push, and tell Mads the public deploy is pending on the other PC. The
GitHub Actions workflow `.github/workflows/analogy-bench.yml` deploys on push
instead once the `CLOUDFLARE_API_TOKEN` repo secret exists.

## 1. Read before writing

- The lecture note you just wrote (or `Obsidian/Courses/34870 Electroacoustics/Lecture Notes/Lecture N - ….md`).
- `src/index.html` — the last existing `<section class="lecture" id="lN">` is the template.
- `src/benches.js` — one `benchXxx()` function per playground; `benchDynMic` and
  `benchCondenser` are the reference pattern (sliders → physics → `Plot` → readouts → note).
- `src/app.js` — the toolkit: `bench(id, title, eyebrow)`, `slider(ctl, spec)`,
  `readouts(ctl, keys)`, `class Plot` (log-x SVG chart with hover), `polarSVG`,
  circuit helpers (`RES IND CAP VSRC ISRC ZBOX DEPV DEPI CK.wire CK.gnd CK.label svgWrap`),
  complex maths (`cx cadd cmul cdiv par ZL ZC ZR dB`), `sci()`, `hz()`, constants `RHO C0`.
- `src/quiz.js` — `QUIZZES["N"] = [{q, a:[...], c: index, why}]`.
- `src/diagrams.js` — static circuits; `diagMap()` draws the hero timeline (add the new lecture node there).

## 2. Add the lecture

1. **Section** in `src/index.html`, after the previous lecture and before `#cheat`:
   `lec-head` (eyebrow: lecture number, date, lecturer; h2; meta: book refs, problem sheet)
   → `.one-idea` (one sentence, the whole lecture) → blocks: *The picture* (a
   `diag-*` div or table), the **bench** (`<div id="bench-xxx"></div>`), *Formulas*
   (`.formulas` cards with `.M` KaTeX), *The trap* (`.callout.trap`), anything the
   lecturer said that is not in the books (`.callout.real`), then `<div id="quiz-N"></div>`.
   Plain, conversational English. Colour words: `.el .me .ac` = electrical / mechanical / acoustical.
2. **Nav**: add `<li><a href="#lN" data-quiz="N">…` to `.wire` in the rail.
3. **Bench(es)** in `src/benches.js` + call them in the boot block at the bottom.
   Physics in a pure function (`dynMic(p)` style) so it can be unit-checked.
   Start values = the problem sheet's numbers; readouts must show the sheet's answers.
4. **Quiz**: 4–5 questions in `src/quiz.js`, each `why` teaches something.
5. **Hero map**: add a node in `diagMap()` (`src/diagrams.js`); the summary section
   `#cheat` gets a row/line if the lecture adds an element, coupling or response shape.
6. KaTeX: inline `<span class="m">…</span>`, display `<div class="M">…</div>`; escape `<` as `&lt;`.

## 3. Verify (do not skip)

```bash
cd "5. Semester/Electroacoustics/Analogy Bench/src" && node -e '
const fs=require("fs");global.window={};global.document={addEventListener(){},getElementById(){return null},querySelector(){return null},querySelectorAll(){return []}};
global.localStorage={getItem(){return null},setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=()=>{};
const src=fs.readFileSync("app.js","utf8")+"\n"+fs.readFileSync("benches.js","utf8")+"\n;module.exports={dynMic,condMic /* + your new function */};";
const m={};new Function("module","require",src)(m,require);const L=m.exports;
// call your physics function with the sheet values and print what the sheet says
'
```

Then `python3 build.py`, open `dist/index.html` once in the browser (launch config
`analogy-bench`, port 8642) and look at the new section: KaTeX rendered, plot not
clipped, markers where the sheet says.

## 4. Deploy and record

```bash
cd "5. Semester/Electroacoustics/Analogy Bench"
npm run deploy:cf            # build + wrangler deploy → study.madsrudolph.dev
curl -s -o /dev/null -w "%{http_code}\n" https://study.madsrudolph.dev/
```

- LAN mirror updates itself within 30 min; `./deploy.sh` forces it (needs SSH to 192.168.50.200).
- Claude artifact: republish `dist/artifact.html` + the `files` map only from the
  session that owns it (or pass its `url`); otherwise leave it, the public site is primary.
- Update the "Done so far" bullet in `CLAUDE.md` (which lectures the site covers),
  then `git add` the bench folder + note + CLAUDE.md, commit ("Add lecture N to the
  Analogy Bench"), `git pull --rebase --autostash`, push. Never add AI attribution.

## Design rules that keep it one site

Copper = electrical, steel blue = mechanical, teal = acoustical — never reassign.
Fraunces / IBM Plex Sans / IBM Plex Mono. No new libraries. Every plot gets the
hover layer for free from `Plot`; every bench ends with a `b.note` that says what to
try. Regions on plots are labelled with two or three words. Keep the "one idea"
honest: if it does not fit one sentence, the section is not understood yet.
