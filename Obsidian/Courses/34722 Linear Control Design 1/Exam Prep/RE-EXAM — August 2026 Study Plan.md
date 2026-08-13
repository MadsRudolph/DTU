---
tags: [34722, lcd, exam, reexam, plan, oral]
course: 34722 Linear Control Design 1
purpose: 12-day plan for the ORAL re-exam — understanding and explain-aloud fluency, not tool speed
exam: "ORAL re-exam: Monday 25 August 2026, 15 minutes, questions in the style of the written exam. NO aids/solver."
---
# RE-EXAM — August 2026 Study Plan (ORAL — 25 Aug, 15 min)

> [!info] Quick Links
> Hub: [[00 LCD1 — Exam Hub]] · Post-mortem: [[W-F26 — Worked Exam (MCQ)]] · Formulas: [[Exam Formula Cheat-Sheet]] · Patterns: P1–P7 notes

> [!important] ⚠️ FORMAT CHANGE (learned 13-Aug)
> **15-minute ORAL exam, 25 August 2026.** Questions in the style of the written exam, but *you* solve
> and explain at the board — **no solver, no aids**. The June diagnosis still holds (theory was there,
> finishing wasn't), but the training target flips: from *clicking the right option fast* to
> **deriving, sketching and explaining out loud from memory**.
>
> This is good news: an oral examiner rewards exactly the understanding you have and punishes exactly
> the trap-guessing that sank the MCQ. Nobody hands you five options with a planted reciprocal —
> you build the answer, and method points exist.

---
## 🎯 What 15 oral minutes actually tests

1. **Hand-solve fluency** on the same P1–P7 patterns — but showing every step on paper/board.
2. **Sketching** — Bode asymptotes, Nyquist shapes, step responses, drawn free-hand and labelled.
3. **Saying the why** — what PM *means*, why a lead adds phase, why an integrator kills step-ess,
   Z = N + P in words, what an RHP zero forbids.
4. **Formula recall from memory** — the cheat-sheet must move into your head.
5. **Composure under a clock** — 15 min is 2–3 questions; hesitation costs a whole question.

## 🛠 The toolchain (repurposed — the solver is now the sparring partner)

- **🎤 Oral Trainer** (new mode in `lcd1-exam-suite`): draws random exam-style prompts, runs a
  2-minute speaking timer, then reveals the model answer + key points + the worked derivation.
  Self-grade → it re-serves what you're weak on. THIS is the daily driver.
- **"Show the working"** in the solver: after every hand-solve, run the same numbers and diff your
  derivation line-by-line against the engine's. Your steps must match *before* the reveal.
- **🎛 Bode Lab**: sketch the Bode by hand FIRST, then place the poles/zeros and compare.
- **Phone voice memo**: record 2-minute explanations; listen back. Cringe = learning.
- **NotebookLM** (`nlm.bat ask "..." --notebook-id lcd1`): fact-check your phrasing against the
  actual lecture slides when unsure how the course defines something.

## 📚 The daily loop (every study day, ~4 focused hours)

1. **Blank-sheet derivation (45 min):** today's pattern — write the core results from MEMORY on an
   empty page (formulas + one worked example). Then open the P-note and mark every gap in red.
2. **Sketch drills (30 min):** 5 hand sketches (Bode/Nyquist/step for given G's) → verify in Bode Lab
   / Plot TF. A sketch you can't draw is a question you can't answer.
3. **Oral drills (60–90 min):** 8–12 Oral Trainer prompts. Stand up. Speak OUT LOUD, full sentences,
   as if the examiner is there. Reveal, self-grade honestly, note misses below.
4. **Verify pass (30 min):** re-run today's hand-solves through the solver; every mismatch gets a
   red-pen line in the miss log.

---
## 📅 The 12 days (13 → 24 Aug, exam Mon 25 Aug)

### Phase 0 — Reset for oral (Wed 13 Aug)
- [ ] Read this plan; set up a **whiteboard/A4 stack + phone for voice memos**.
- [ ] **Baseline formula test:** blank sheet, 20 min, write every formula you know (Mp↔ζ, phase
  budget, ess table, lead design, ω_d, t_s, Z=N+P). Score it against [[Exam Formula Cheat-Sheet]] —
  that's the memorization backlog.
- [ ] First Oral Trainer session (10 prompts, all patterns) to calibrate the weak-topic tracker.

### Phase 1 — Pattern blocks, oral-first (Thu 14 – Wed 20 Aug)
Worst-first order from the June misses. Each day = the daily loop on that block.

| Day | Block | Must be able to SAY and DERIVE |
|---|---|---|
| Thu 14 | **P6 I: P & Lead design** | The phase-budget equation from scratch; why K moves no phase; lead: why zero-before-pole, α ↔ φ_max ↔ 1/√α; design a lead at the board. |
| Fri 15 | **P6 II: PI-Lead + feedforward** | PI phase cost −atan(1/N_i)... full budget with all three terms; prefilter idea; why an RHP zero forces static feed-forward (F(0), never 1/G). |
| Sat 16 | **P3: Stability & Nyquist** | Nyquist criterion in words (Z = N + P), stable-K both directions (stable plant 0<K<GM; RHP plant K>K_crit and WHY the interval flips), GM/PM definitions + read-off. |
| Sun 17 | **P4: Second-order** | Normalise an ODE → ζ, ωₙ; Mp↔ζ derivation sketch; ω_d = ωₙ√(1−ζ²); t_s = 4/(ζωₙ); sketch step responses for ζ = 0.2/0.7/1. |
| Mon 18 | **P5: ess & sensitivities** | Type table FROM the error constants (derive, don't recite); the 1/(1+K_pos) divide; disturbance-ess: integrator BEFORE the injection rejects, after doesn't; S+T=1. |
| Tue 19 | **P2: Bode fluency** | Sketch any G(s) as asymptotes in <2 min; reverse: read poles/zeros/type off a plot; the integrator signature (−90° start + low ω_c); RHP-zero phase signature. |
| Wed 20 | **P1 + P7: Modelling & theory** | Block reduction at the board (parallel C+D vs cascade!); nested loops by hand (the ReExam'22 Q9 quadratic); IVT/FVT; the standard proofs in P7. |

### Phase 2 — Mock orals (Thu 21 – Sat 23 Aug)
Simulate the real thing: **15-minute blocks, 3 random questions, standing, speaking, no notes.**
- [ ] Thu 21: 3 × 15-min mocks from the Oral Trainer (random across all patterns). Record them.
- [ ] Fri 22: 3 × mocks using the **F26 paper as oral questions** — solve each aloud at the board,
  then check against [[W-F26 — Worked Exam (MCQ)]]. The 17 June misses MUST all be clean now.
- [ ] Sat 23: 2 × mocks + weak-topic repair from the Trainer stats. If any pattern still red →
  its Phase-1 day gets a compressed repeat.
- **Grader mindset per mock:** Did I state the method first? Did I finish the algebra (+1's,
  inequality directions)? Did I sanity-check physics out loud? That's the June trap list, spoken.

### Exam eve (Sun 24 Aug)
- [ ] One blank-sheet formula test (target: complete from memory).
- [ ] Skim the trap card + Hub — *say* each trap aloud once with its fix.
- [ ] One relaxed Trainer session (Good/Easy items only — confidence, not cramming). Sleep.

### Exam day (Mon 25 Aug)
- Opening move for ANY question: **name the pattern out loud** ("this is a steady-state-error
  question; the system is type 1 because..."), then derive. Method first, numbers second.
- If stuck: say what you DO know about the setup — orals give partial credit for structure.

---
## 🎙 The oral answer template (drill until automatic)

1. **Classify:** "This is a [pattern] question."
2. **State the governing relation** before touching numbers.
3. **Derive/sketch**, narrating each step.
4. **Sanity-check aloud** ("negative ζ would be unstable, so this root is discarded").
5. **Conclude with the number/statement AND its meaning.**

## 📊 Miss log (fill after every session)

| Date | Prompt/topic | What failed (recall / derivation / sketch / wording) | Fix |
|---|---|---|---|
| | | | |
