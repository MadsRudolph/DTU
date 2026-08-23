# AGENTS.md — LCD1 oral-exam review loop (any AI agent)

You are helping **Mads** prepare for the **34722 Linear Control Design 1 ORAL re-exam:
Monday 25 August 2026, 15 minutes, no aids**. Questions are in the style of the written
exam, solved and explained at the board. He failed the June MCQ 3/20 — mostly on trap
distractors (reciprocals, dropped `+1`, sign errors), not theory gaps.

This folder contains a three-part study system. Your job as the reviewing agent is the
two workflows below: **"check my board"** and **"review my oral session"**. Everything is
plain files — no special tooling needed beyond reading images and editing JSON.

All paths below are absolute so they work from any working directory.

---

## The system at a glance

| Part | What | Where |
|---|---|---|
| Closed Loop | interactive crash-course site (8 modules, labs, quizzes) | `C:\Users\Mads2\DTU\4. Semester\Linear Control Design\EXAM\Closed-Loop.html` — served at `/course` |
| Loop Pad | S-Pen whiteboard app (Samsung tablet) — Mads derives answers by hand, saves boards as PNGs | `C:\Users\Mads2\DTU\4. Semester\Linear Control Design\EXAM\loop-pad\` |
| Oral Trainer | records spoken answers in the lcd1-exam-suite Electron app | `C:\Users\Mads2\lcd1-exam-suite\` |

The Loop Pad server (`python server.py` in the loop-pad folder, port 8321, also public at
https://pad.madsrudolph.dev via a Cloudflare tunnel) must be running for the tablet to
save boards. You normally don't need to touch the server — you work on the files it writes.

---

## Workflow 1 — "check my board"

When Mads says *check my board* (or similar):

1. **Find the newest board(s).** PNGs live in
   `...\EXAM\loop-pad\boards\<YYYY-MM-DD>\<HHMMSS>_<slug>.png`,
   each with a sidecar `<same name>.json`:
   ```json
   {"title": "...", "id": "...", "saved": "2026-08-23T14:05:12",
    "strokes": 12, "qid": "q-ess-3", "prompt": "the question text"}
   ```
   Review every board newer than the last feedback entry (see step 4), newest last.

2. **Look up the question.** If `qid` is non-empty, find that entry in
   `...\EXAM\loop-pad\questions.json` (38 questions, schema
   `{id, pattern, kind, prompt, points, answer}`). Grade the handwriting against that
   entry's `points` (the key steps an examiner wants) and `answer` — not just generic
   correctness. If `qid` is empty it's free practice; grade against standard LCD1 theory.

3. **Read the PNG as an image** and check the math line by line: algebra slips, sign
   errors, dropped `+1` terms, reciprocal confusions, wrong formulas, missing steps from
   `points`. Also say what's *good* — this is exam confidence training.

4. **Append a feedback entry** to `...\EXAM\loop-pad\feedback.json` (a JSON array —
   append to it, never overwrite existing entries; keep the file valid JSON):
   ```json
   {"board": "140512_step-response.png",
    "time": "14:07",
    "verdict": "partly",
    "notes": ["ζ from Mp is right (0.46)", "t_s: you wrote 4/ωn — it is 4/(ζωn)", "..."],
    "svg": "<circle cx='812' cy='430' r='60' fill='none' stroke='#B23B3B' stroke-width='6'/><text x='890' y='445' fill='#B23B3B' font-size='42' font-weight='bold'>4/(ζωn)!</text>"}
   ```
   - `verdict`: `correct` | `partly` | `wrong`.
   - `notes`: short bullet strings; shown as a list in the app.
   - `svg`: **an SVG fragment, not a full `<svg>` document** (it is injected via
     innerHTML into an existing `<g>`). Coordinates are the **pixel coordinates of the
     PNG you just read** — annotate as if drawing on the image. The app maps it back
     onto the canvas automatically. Red ink `#B23B3B`, `stroke-width` 5–8 and
     `font-size` 36–48 (the exports are ~2400 px wide). Circle the error, put the
     correction next to it. Omit `svg` (or use `""`) if nothing to mark.
   - Only the **newest** entry's `svg` gets overlaid on the tablet, so if reviewing
     several boards, put annotations on the board Mads is most likely still viewing
     (the newest) and cover the rest in `notes` of their own entries.

5. The tablet app polls `feedback.json` every 5 s — the review appears by itself.
   Then tell Mads the verdict in chat too, with the reasoning.

---

## Workflow 2 — "review my oral session"

When Mads says *review my oral session*:

1. Run `python tools/transcribe-oral.py` in `C:\Users\Mads2\lcd1-exam-suite\`
   (uses faster-whisper; skips already-transcribed takes).
2. Read `C:\Users\Mads2\lcd1-exam-suite\oral-sessions\<YYYY-MM-DD>\REPORT.md` —
   one transcript per recorded answer, each tagged with its question id.
3. Grade each transcript against the same question bank
   (`spike/oral-bank.js` in the suite, or the exported `loop-pad\questions.json` —
   same 38 items): did he hit the `points`, was the terminology right, would it
   convince an examiner in a 15-minute oral? Give a Good / Almost / Rework verdict
   per answer plus what to say differently.

---

## Grading knowledge sources (in trust order)

1. `...\EXAM\loop-pad\questions.json` — the `points`/`answer` fields are the rubric.
2. `C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1\Formulas\Exam Formula Cheat-Sheet.md`
3. `...\34722 Linear Control Design 1\Exam Prep\W-F26 — Worked Exam (MCQ).md` — all 20 June questions worked, with the traps Mads fell for.
4. `...\Exam Prep\RE-EXAM — August 2026 Study Plan.md` — the 48-hour emergency plan and priorities.
5. `Closed-Loop.html` — the course content he's learning from.

Course conventions: lead compensator uses α < 1 (`C = K(ατs+1)/(τs+1)` form per the
cheat-sheet — check it, don't assume), phase-budget method `∠C + ∠G = γ_M − 180°` at
crossover, settling time `t_s = 4/(ζω_n)`, `M_p ↔ ζ` via the standard second-order
relation. When in doubt, the cheat-sheet wins.

---

## Rules

- **Never commit or push** `boards/` or `feedback.json` (gitignored personal data), and
  never add AI/`Co-Authored-By` mentions to any commit in these repos.
- Don't restructure the loop-pad app or server — it is frozen until after the exam.
- Encourage speed: 2 days to the exam; short feedback loops beat long essays.
