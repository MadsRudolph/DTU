---
tags: [34722, lcd, exam, theory, handoff]
course: 34722 Linear Control Design 1
purpose: Bootstrap a fresh Claude Code session to work through the 10 Theoretical Exercises with Mads in MATLAB and build a worked walkthrough doc in parallel
---
# HANDOFF — Theory Walkthrough Session

> [!info] What this session is
> Mads and you work through the **10 Theoretical Exercises** of 34722 Linear Control Design 1 **together**, one at a time, **solving each in MATLAB**, and writing up a **walkthrough document in parallel** as you go. The exam is **multiple-choice, Tue 2-June-2026** — this is exam prep, the goal is that Mads can *reproduce these cold*.

---
## ▶️ First actions (do these before anything else)
1. You're in `C:\Users\Mads2\DTU` (auto-loads `CLAUDE.md` + memory — read them; they hold the binding conventions).
2. Read the exercise source PDF: [[LCD1 Theory Exercises.pdf]] (in `Exercises/Solutions/Past Exams/`). If it's missing locally, the PDFs are gitignored/Drive-backed — fetch with `python Obsidian/scripts/drive-sync/download.py`.
3. Read the **existing reference note** (terse, already styled with callouts): [[P7 — Theory Exercises (Worked Proofs & Derivations)]]. Don't duplicate it — see "Decision point 0" below.
4. Skim the **verified solve-script** and the **practice skeleton** (paths in the assets table). The solve-script already reproduces every facit — it's your answer key, but **don't lead with the answer** (hints-first, see workflow).

---
## 🤝 Decision point 0 — which doc do we write?
P7 already exists as the concise "proofs & derivations" reference. Mads asked for a **walkthrough document built in parallel** while solving. At kickoff, confirm with Mads which he wants:
- **(Recommended) New file** `Walkthroughs/W-Theory — Worked Exercises.md`, matching the format of the sibling worked exams [[W-F22 — Worked Exam]] and [[W-ReExam F22 — Worked Exam]] — a learning-oriented, step-by-step log of *how we solved each one together*. P7 stays the terse reference; cross-link the two.
- **(Alt) Deepen P7 in place** as you go, rather than a second doc.

Default to the new file unless Mads says otherwise.

---
## 🔁 The workflow (per CLAUDE.md conventions — follow exactly)
- **Hints-first.** When Mads says "let's do Q4", give a *small hint*, then **STOP and wait**. Full walkthrough only on explicit "walk me through it / do it for me". Do not dump the solution unprompted.
- **One exercise at a time.** Solve in MATLAB live (you can run `matlab -batch "..."` for snippets, or point Mads at the section in `solve_Theory.m`), confirm the number, *then* write that question's section into the walkthrough doc.
- **English** in the Obsidian walkthrough (conversational, teaching tone). **Danish** in any MATLAB `.m` comments. **Mermaid** over ASCII if a diagram helps.
- **Match the established callout styling** (Antigravity restyled all the worked notes — keep it consistent):
  - `> [!info]` — top "Exam Resources" block (links + script paths + PDF wikilink)
  - `> [!example]- Approach` / `Derivation` / `Solution` — foldable (the `-` collapses it), holds the method + math
  - `> [!success] Facit: …` — the answer
  - `> [!warning] Trap` — the planted gotcha
  - `> [!danger] Misprint` — only if the problem has a typo
  - `> [!tip] Key Trick` / `> [!note] Why it matters` — the takeaway
  - `> [!todo] Review Checklist` — a "got wrong / review" `- [ ]` list at the end
  - PDF references as wikilinks `[[LCD1 Theory Exercises.pdf]]`; figures as embeds `![[Q1_lead_phase.png]]`
- **Embed graphs** where they help (Mads explicitly wants this). Two already exist; generate more via the `MAKE_FIGS` flow below.

---
## 📋 The 10 exercises (facit = your private answer key — reveal via hints, not upfront)
| # | What it asks | Result | Type |
|---|---|---|---|
| Q1 | Lead `C_D`: prove max-phase frequency & angle | `ω_m=1/(τ_d√α)`, `φ_m=asin((1−α)/(1+α))`, gain `1/√α` | proof |
| Q2 | 1st-order LPF metrics | `ω_c=ω_BW=1/τ`, `t_r≈2.2τ`, `t_s≈4τ` | proof |
| Q3 | P-Lag phase at `ω_c=N_i/τ_i` | `φ_L=atan(N_i(1−β)/(1+βN_i²))`; `β→∞ ⇒ −atan(1/N_i)` | proof |
| Q4 (Exam'21) | Poles of `y⁗+9y‴+20ÿ=71u` | `{0,0,−4,−5}` → unstable, type-2 | numeric |
| Q5 (Exam'21) | `ess`, `K_P=2` in **feedback** branch | `0.2` (still `1/(1+K_PG(0))`) | numeric |
| Q6 (Exam'21) | Nested loop, find `K₂` | `79.17` | numeric |
| Q7 (ReExam'21) | DC gain of telescoping cascade + unity fb | `0.8` | numeric |
| Q8 (Exam'22) | Pick feed-forward `F_d` | `F_d=D/G₁` + fast `(n−2)`-order LPF → **(d)** | concept |
| Q9 (ReExam'22) | Two nested P-controllers, find `K_P` | `4` (quadratic `K_P²−3K_P−4=0`) | numeric |
| Q10 | Prove P-Lag cuts `ess` by `β`; `β→∞⇒PI⇒ess→0` | factor `β` | proof |

---
## 🧮 Assets (all verified, present in the repo)
| Asset | Path | Role |
|---|---|---|
| Verified solve-script | `4. Semester/Linear Control Design/EXAM/Scripts/solved/solve_Theory.m` | Reproduces every facit; MATLAB-checks the proofs numerically. Run: `matlab -batch "solve_Theory"` |
| Practice skeleton | `4. Semester/Linear Control Design/EXAM/Scripts/practice/practice_Theory.m` | Givens pre-loaded, `NaN; % TODO` blanks, proofs as comment-prompts — what Mads fills in |
| Reference note | `Exam Prep/P7 — Theory Exercises (Worked Proofs & Derivations).md` | Terse worked proofs, already callout-styled |
| Figures (2) | `Obsidian/Courses/34722 Linear Control Design 1/Images/exam/Theory/` | `Q1_lead_phase.png`, `Q2_firstorder_bode.png` |
| Source PDF | `Exercises/Solutions/Past Exams/LCD1 Theory Exercises.pdf` | The actual problem statements (+ official Solutions manual) |

---
## 🖼️ Generating new figures (MAKE_FIGS pattern)
`solve_Theory.m` has a `MAKE_FIGS = false` flag and a `FIGURER` section at the bottom that `exportgraphics` PNGs to `Images/exam/Theory/`. To add a graph for a new question:
1. Add an `exportgraphics(...)` block in the `if MAKE_FIGS` section.
2. **Temporarily** `Edit` the flag to `true` (note: setting it on the `-batch` command line gets wiped by the `clear` at the top — you must edit the in-file flag), run `matlab -batch "solve_Theory"`, then **Edit it back to `false`**.
3. Embed with `![[Qn_name.png]]` in the walkthrough.

---
## ⚠️ Binding rules (do not violate)
- **Never** add `Co-Authored-By: Claude` or any AI mention to commit messages.
- **Do not commit** unless Mads explicitly asks. When he does: stage **by explicit path**, never `git add -A` (a broken nested git repo at `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/Report` aborts repo-wide adds). Don't fix that submodule without a go-ahead.
- PDFs are gitignored/Drive-backed — pushing is handled by the `drive-sync-push` skill (`upload.py --scan/--sync` then stage the manifest). Don't try to `git add` PDFs.
- Keep math/numbers/facit **byte-exact** — they're verified. The walkthrough adds *narrative*, not new computation.

---
## ✅ Definition of done (for this session's scope)
- Each exercise Mads chose to cover has: a section in the walkthrough doc with the styled callouts, the MATLAB that nails it, a `![[ ]]` graph where useful, the facit, and the trap.
- The walkthrough is cross-linked to [[P7 — Theory Exercises (Worked Proofs & Derivations)]], [[00 LCD1 — Exam Hub]], and [[LCD1 Theory Exercises.pdf]].
- If a new `W-Theory` file was created, add it to the practice-loop table in [[00 LCD1 — Exam Hub]].
