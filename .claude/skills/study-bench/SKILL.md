---
name: study-bench
description: REQUIRED whenever a lecture note, problem set or lab note for 34870 Electroacoustics or 34840 Acoustics and Noise Control is written or updated in the vault — the Study Bench site (study.madsrudolph.dev, one interactive site per course) must be extended with the same material and redeployed, from either PC. Also use for "update the bench", "add lecture N to the site", "the study site", "study.madsrudolph.dev", "Analogy Bench", "Sound Bench", or when a new course should get a site.
---

# The Study Bench — keep the sites in step with the lecture notes

The project lives in `5. Semester/Study Bench/` (repo-relative): `core/` (app.js toolkit +
style.css), `courses/<code>/` (one self-contained site per course: index.html, benches.js,
problems.js, quiz.js, optional theme.css / labs.js / diagrams.js), `hub/index.html` (the landing
page listing the courses), `build.py` → `dist/` (hub at the root, each course under `dist/<code>/`).
Public at **https://study.madsrudolph.dev** (courses at `/34870/`, `/34840/`), LAN mirror at
http://192.168.50.220 (CT 116 `study`, self-syncs every 30 min), and one Claude artifact per
course (URLs in the README). 34870 = *The Analogy Bench*, 34840 = *The Sound Bench*. One section per lecture, one interactive bench per
idea, one quiz per lecture. Labs get the same treatment: one section per lab
(`#labA` is the template, benches in `src/labs.js`, quiz key `"A"`), with a bench per
lab part that solves the lab's circuit live and reproduces the runthrough's numbers. Every number shown must reproduce the worked answers
in the notes. Convention that bit us once: the official sheets take a microphone's front air mass
as a **piston in a tube** (0.6133ρ/πa), not the baffled piston (8ρ/3π²a); `dynMic`/`condMic` take `front`.

**Rule:** a 34870 lecture note without a matching site section is unfinished
work. Do the note first, then the site, then deploy, in the same task.

## 0. One-time per PC

```bash
cd "5. Semester/Study Bench" && npm install
npx wrangler whoami || npx wrangler login     # opens a browser once; token lands in ~/.config/.wrangler
```

If `wrangler login` cannot run (headless, no browser), still do everything else,
commit + push, and tell Mads the public deploy is pending on the other PC. The
GitHub Actions workflow `.github/workflows/analogy-bench.yml` deploys on push
instead once the `CLOUDFLARE_API_TOKEN` repo secret exists.

## 1. Read before writing

- The lecture note you just wrote (`Obsidian/Courses/<course>/Lecture Notes/Lecture N - ….md`), the
  slides if the note is thin, and the problem sheet + official solutions in `Exercises/` (pdftotext; scanned ones via pdftoppm + Read).
- `courses/<code>/index.html` — the last existing `<section class="lecture" id="lN">` is the template.
- `courses/<code>/benches.js` — one `benchXxx()` per playground; `benchDynMic` (34870) and
  `benchSpherical` (34840) are the reference pattern (sliders → physics → `Plot` → readouts → note).
- `core/app.js` — the toolkit: `bench(id, title, eyebrow)`, `slider(ctl, spec)`,
  `readouts(ctl, keys)`, `class Plot` (log-x SVG chart with hover), `polarSVG`,
  circuit helpers (`RES IND CAP VSRC ISRC ZBOX DEPV DEPI CK.wire CK.gnd CK.label svgWrap`),
  complex maths (`cx cadd cmul cdiv par ZL ZC ZR dB`), `sci()`, `hz()`, constants `RHO C0`.
- `courses/<code>/quiz.js` — `QUIZZES["N"] = [{q, a:[...], c: index, why}]` (labs use the letter, e.g. `"A"`).
- `courses/<code>/problems.js` — `window.PROBLEMS["N"] = [{id, title, tag, given, hint, sol, bench, benchLabel}]`, rendered
  into `<div id="problems-N">` as collapsible cards (statement → hint → official solution → bench link).
  Every lecture gets its problem set here: statements from the slides/sheet, solutions from the
  official `Exercises/34870_SolutionsN*.pdf` (pdftotext; scanned ones via pdftoppm + Read) and the vault's worked notes.
- `courses/34870/labs.js` — lab benches; `csolve(A, b)` is a small complex linear solver for nodal/loop equations of any lab circuit.
- `courses/34870/diagrams.js` — static circuits; `diagMap()` draws the hero timeline (add the new lecture node there).

## 2. Add the lecture (or lab)

1. **Section** in `courses/<code>/index.html`, after the previous lecture and before `#cheat`:
   `lec-head` (eyebrow: lecture number, date, lecturer; h2; meta: book refs, problem sheet)
   → `.one-idea` (one sentence, the whole lecture) → blocks: *The picture* (a
   `diag-*` div or table), the **bench** (`<div id="bench-xxx"></div>`), *Formulas*
   (`.formulas` cards with `.M` KaTeX), *The trap* (`.callout.trap`), anything the
   lecturer said that is not in the books (`.callout.real`), then `<div id="quiz-N"></div>`.
   Plain, conversational English. Colour words: `.el .me .ac` = electrical / mechanical / acoustical.
2. **Nav**: add `<li><a href="#lN" data-quiz="N">…` to `.wire` in the rail.
3. **Bench(es)** in `courses/<code>/benches.js` + call them in the boot block at the bottom.
   Physics in a pure function (`dynMic(p)` style) so it can be unit-checked.
   Start values = the problem sheet's numbers; readouts must show the sheet's answers.
4. **Problems**: every problem of the lecture/sheet in `courses/<code>/problems.js` with the official answers in `tag`,
   a hint, the full solution, and a link to the bench that reproduces it; add `<div id="problems-N">` before the quiz.
5. **Quiz**: 4–5 questions in `courses/<code>/quiz.js`, each `why` teaches something.
6. **Hero map**: add a node (34870: `diagMap()` in `diagrams.js`; 34840: the inline SVG in the hero) and bump the counts on `hub/index.html`; the summary section
   `#cheat` gets a row/line if the lecture adds an element, coupling or response shape.
7. KaTeX: inline `<span class="m">…</span>`, display `<div class="M">…</div>`; escape `<` as `&lt;`.

## 3. Verify (do not skip)

```bash
cd "5. Semester/Study Bench" && node -e '
const fs=require("fs");global.window={};global.document={addEventListener(){},getElementById(){return null},querySelector(){return null},querySelectorAll(){return []}};
global.localStorage={getItem(){return null},setItem(){}};global.performance={now:()=>0};global.requestAnimationFrame=()=>{};
const src=fs.readFileSync("core/app.js","utf8")+"\n"+fs.readFileSync("courses/<code>/benches.js","utf8")+"\n;module.exports={dynMic,condMic /* + your new function */};";
const m={};new Function("module","require",src)(m,require);const L=m.exports;
// call your physics function with the sheet values and print what the sheet says
'
```

Then `python3 build.py`, open `dist/<code>/index.html` once in the browser (launch config
`study-bench`, port 8642) and look at the new section: KaTeX rendered, plot not
clipped, markers where the sheet says.

## 4. Deploy and record

```bash
cd "5. Semester/Study Bench"
npm run deploy:cf            # build + wrangler deploy → study.madsrudolph.dev
curl -s -o /dev/null -w "%{http_code}\n" https://study.madsrudolph.dev/
```

- LAN mirror updates itself within 30 min; `./deploy.sh` forces it (needs SSH to 192.168.50.200).
- Claude artifact: republish `dist/<code>/artifact.html` with the `files` map (all .js + style.css + theme.css + katex.min.js from `dist/<code>/`), passing the course's artifact `url` from the README; the public site is primary.
- Update the "Done so far" bullet in `CLAUDE.md` (which lectures the site covers),
  then `git add` the bench folder + note + CLAUDE.md, commit ("Add lecture N to the
  Analogy Bench"), `git pull --rebase --autostash`, push. Never add AI attribution.

## Adding a whole new course

Copy the shape of `courses/34840/` (index.html with rail + hero + sections, theme.css that
remaps `--el/--me/--ac` to the course's three meanings, benches.js, problems.js, quiz.js),
add a card on `hub/index.html`, add the course folder names to the hook in
`.claude/settings.json`, publish its own artifact, list the URL in the README.

## Design rules that keep it one site

Copper = electrical, steel blue = mechanical, teal = acoustical — never reassign.
Fraunces / IBM Plex Sans / IBM Plex Mono. No new libraries. Every plot gets the
hover layer for free from `Plot`; every bench ends with a `b.note` that says what to
try. Regions on plots are labelled with two or three words. Keep the "one idea"
honest: if it does not fit one sentence, the section is not understood yet.
