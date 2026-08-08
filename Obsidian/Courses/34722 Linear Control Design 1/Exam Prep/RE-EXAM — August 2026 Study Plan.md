---
tags: [34722, lcd, exam, reexam, plan]
course: 34722 Linear Control Design 1
purpose: Day-by-day plan to pass the August 2026 re-exam, built from the 3/20 F26 post-mortem
exam: Multiple-choice re-exam, August 2026 (⚠️ confirm exact date on DTU selvbetjening)
---
# RE-EXAM — August 2026 Study Plan

> [!info] Quick Links
> Hub: [[00 LCD1 — Exam Hub]] · Post-mortem: [[W-F26 — Worked Exam (MCQ)]] · App recipes: [[W-F26 — Solve It With The LCD1 Solver]] · Formulas: [[Exam Formula Cheat-Sheet]]

> [!summary] The one-line diagnosis (from the sat attempt, 3/20)
> **The theory was there — the finish wasn't.** Nearly every miss was the trap
> distractor next to the right answer: a reciprocal, the raw input value, the
> marginal gain instead of the inequality, a non-physical sign. So this plan is
> **drill + ritual**, not re-learning: every solved question ends with the
> 5-point trap check, and every session uses the LCD1 Solver app the way it will
> be used on exam day.

---
## 🎯 The 5-point trap check (recite before answering ANY question)

From [[W-F26 — Worked Exam (MCQ)]] §trap-list — this is the whole difference between 3/20 and passing:

1. **Finish the inequality / the "+1"** — `ess = input/(1+K_pos)` not `/K_pos`; critical gain gives `K > K_min`, not `K = K_min`.
2. **Lead vs lag orientation** — lead = zero before pole, raises gain `1/√α`. Never grab the reciprocal.
3. **Kill impossible options first** — negative ζ, `ω_d = ωn` with stated overshoot, unstable "stable" answers.
4. **Bode origin behaviour** — phase → −90° at low ω + low crossover ⟹ pole at origin; low-freq level = steady-state.
5. **Feed-forward needs DC; RHP zero forbids `1/G`** — static `F(0)`, `F_d(0)` when the plant has a RHP zero.

---
## 📅 The plan (12 days, adjust to the real exam date)

⚠️ **First action: confirm the re-exam date/time on selvbetjening and write it here.** The phases compress or stretch to fit; keep the last two days as-is.

### Phase 0 — Reset (Day 1)
- [ ] Re-read [[W-F26 — Worked Exam (MCQ)]] end-to-end, including every ❌ explanation.
- [ ] Copy the 5-point trap check by hand onto a card. It sits next to the keyboard for every session below.
- [ ] Verify the app: `Launch-Desktop-App.bat` starts, `npm test` green (453 tests as of 8-Aug), Smart Paste routes a pasted F26 Q14/Q16/Q17 to the right tool (new — added 8-Aug).
- [ ] Re-run the 4 MATLAB solve-scripts (`matlab -batch "solve_S20"` etc.) so the facit-reproduction muscle memory is back.

### Phase 1 — Weakness-ordered pattern drills (Days 2–5, one block per day)
Miss counts from F26, drilled worst-first. Each day: read the P-note, redo the F26 misses **by hand**, then redo them **in the app** per [[W-F26 — Solve It With The LCD1 Solver]], then pull that pattern's questions from two old papers ([[Exam Question Pattern Analysis]] has the per-exam map).

| Day | Block | F26 misses | Notes |
|---|---|---|---|
| 2 | **P6 Controller design** | Q16 Q17 Q18 Q19 | [[P6 — Controller Design (P, Lead, PI-Lead, Feedforward)]] — 4 misses, biggest block on every paper. Phase budget 3 ways + lead orientation + feedforward DC rule. |
| 3 | **P4 + P5** (2nd-order & ess) | Q2 Q4 Q9 · Q5 Q13 Q14 | [[P4 — Second-Order Specs (Time & Frequency)]], [[P5 — Steady-State Error & System Type]] — normalise the ODE first; `Mp` relative to final value; the `1+K_pos` divide. |
| 4 | **P3 Stability & Nyquist** | Q3 Q15 | [[P3 — Stability, Margins & Nyquist]] — stable-K interval BOTH ways (stable plant vs RHP pole ⟹ `K > 1/|x|`), the F26 Q15 inequality trap. |
| 5 | **P1 + P2 + P7** | Q6 Q10 · Q8 · Q12 Q20 | Parallel-vs-cascade feedback (`C+D` not `CD`), IVT/FVT, Bode integrator signature, the theory statements. |

### Phase 2 — Timed papers under exam conditions (Days 6–9)
App open, formula sheet printed, trap card visible, phone off. **Log every miss** in a table at the bottom of this note: question → which trap (1–5) → 1-line fix.

- [ ] Day 6: **F22 (20 Q)** — timed. Check with `solve_F22.m` + [[W-F22 — Worked Exam]]. Remember the Q19 α-misprint (0.01, not 0.001).
- [ ] Day 7: **REExam F21 (20 Q)** — timed. The Q17 φ_G = −151° (not −15) read-off trap.
- [ ] Day 8: **Mock Exam 1** (`lcd1-exam-suite/mock-exams/`) — the paper the app was stress-tested on; regenerate the PDF if missing.
- [ ] Day 9: **ReExam F22 (10 Q) + S21 (10 Q)** — the two short papers back-to-back.

**Pass bar:** ≥ 16/20 on each 20-question paper by Day 9. Under that → the missed pattern gets a repeat drill inserted before Phase 3.

### Phase 3 — Close the loop (Days 10–11)
- [ ] Day 10: **Re-sit F26 cold** (`Past Exams/F26 MCQ (sat 2-June-2026).pdf`) — the exact paper that scored 3/20. Target: **≥ 18/20**. This is the single best predictor for the re-exam.
- [ ] Day 10: Any pattern still missing → its P-note + 3 more questions of that type from [[Exam Question Pattern Analysis]].
- [ ] Day 11: **Theory pass** — [[P7 — Theory Exercises (Worked Proofs & Derivations)]] + `solve_Theory.m`; the statement-questions (F26 Q12/Q13 style) are ~15% of the paper and pure recall.

### Exam eve + day (Day 12)
- [ ] Skim only: Hub trap list, the 5-point card, [[Exam Formula Cheat-Sheet]] §4 (corrected bandwidth formula — the helper scripts have the typo).
- [ ] App warm-start: launch once, leave it open. **No source edits after this point** (edits without `npm run build` silently don't ship).
- [ ] Sleep. The June attempt failed on finishing-steps, and finishing-steps are the first thing fatigue kills.

---
## 🔁 The per-question exam-day loop (drill until automatic)

1. **Smart Paste** the whole question → check the routed tool makes sense.
2. Paste the options → read the **flagged** one.
3. **Sanity-check physics** (trap check #3) — can this answer exist?
4. **Finish the algebra** the tool didn't do (trap #1: the `+1`, the inequality direction).
5. No flag / conceptual question → the Hub fast-index → P-note pattern → eliminate impossible options → pick.
6. > 8 min stuck → mark, move on, return at the end.

---
## 📊 Miss log (fill during Phase 2/3)

| Paper | Q | Trap # | What happened / the fix |
|---|---|---|---|
| | | | |
