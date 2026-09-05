# Handoff — LCD1 Solver UX overhaul

**Audience:** Google Antigravity (or another autonomous coding agent)
**Author:** previous Claude Code session
**Date:** 2026-05-30
**Working directory:** `C:\Users\Mads2\DTU`
**Tool's home:** `4. Semester/Linear Control Design/EXAM/Solver/`
**Branch:** `main` — commit directly here.

---

## 0. Read this whole document before touching code

You're inheriting a working, fully tested deterministic backend with a thin, awkward PyQt6 frontend. Your job is **frontend polish only** — make it dramatically easier to use, without altering any solver logic, oracle tests, or the option-matching algorithm.

The user is a DTU student. They have a multiple-choice exam (course 34722 Linear Control Design 1) on **Tuesday 2 June 2026** and want to use this tool to verify answers under exam conditions. The exam is offline, no internet, no LLM. The current UX is too tedious for fast use in a real exam-prep loop.

---

## 1. What's already built and proven

A pattern-first solver for the 34722 multiple-choice exam:
- **14 generalized solver functions** across 7 problem patterns (P1 modelling, P2 Bode read-off, P3 stability, P4 second-order, P5 steady-state error, P6 controllers, P7 theory).
- Each solver is a pure Python function tested against historical exam answers (S20, S21, F22, REExam F21, Theory). `pytest -q` shows **45 passed**.
- A type-aware option matcher (NUMBER / TF / DICT / PICK) ranks pasted multiple-choice options against the computed value, with an auto-mode for DICT results.
- A PyQt6 main window with a sidebar tree (P1..P7 with variants underneath), a stacked content area, and one form per solver.
- A declarative `FormSpec → QWidget` builder so each form is ~15 lines of declarative spec, not a hand-coded widget.

### Tech stack — already pinned in `requirements.txt`

```
control==0.10.1          # python-control (note: PyPI package is "control", not "python-control")
sympy==1.13.3
numpy==2.1.3
scipy==1.14.1
matplotlib==3.9.2
PyQt6==6.7.1
pytest==8.3.3
```

Python 3.13.x. Windows 11. All offline at runtime — no network calls anywhere in the codebase.

### Repo conventions (mandatory — these break things if you violate them)

- **Stage commits by explicit path.** Never `git add -A`. There is a broken nested git repo at `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/Report` that aborts repo-wide adds.
- **Never** add `Co-Authored-By: Claude` or any AI/agent mention to commit messages. Messages must read like a developer wrote them.
- **Never** use `--no-verify` or skip hooks.
- Working directory is the DTU repo root `C:\Users\Mads2\DTU`. The solver lives at `4. Semester/Linear Control Design/EXAM/Solver/` — yes, the directory has spaces, quote your paths.

---

## 2. File map — what you can and cannot touch

```
4. Semester/Linear Control Design/EXAM/Solver/
├── run.py                              # 🟢 CAN MODIFY — launcher
├── requirements.txt                    # 🔴 leave alone unless adding deps (and only if necessary)
├── pyproject.toml                      # 🔴 leave alone
├── lcd_solver/
│   ├── __init__.py                     # 🔴 leave alone
│   ├── types.py                        # 🔴 LOCKED — Result + ResultKind contract
│   ├── tf_input.py                     # 🔴 LOCKED — parse_tf, describe_tf are tested
│   ├── match.py                        # 🔴 LOCKED — option-matching algorithm
│   ├── solvers/                        # 🔴 LOCKED — every file in here is verified against oracles
│   │   ├── p1_models.py
│   │   ├── p1_block_reduce.py
│   │   ├── p2_bode.py
│   │   ├── p3_stability.py
│   │   ├── p4_secondorder.py
│   │   ├── p5_ess.py
│   │   ├── p6_control.py
│   │   └── p7_theory.py
│   └── ui/                             # 🟢 EVERYTHING IN HERE IS YOURS
│       ├── __init__.py
│       ├── main_window.py              # 🟢 main window, sidebar, content stack
│       ├── widgets.py                  # 🟢 TFInputWidget, ResultPanel
│       ├── form_builder.py             # 🟢 FieldSpec, FormSpec, SolverFormWidget, build_form
│       └── forms.py                    # 🟢 ALL_FORMS — the declarative registry
└── tests/                              # 🔴 LOCKED — never modify, never delete
    ├── conftest.py
    ├── oracle_data.py
    ├── test_tf_input.py
    ├── test_match.py
    ├── test_p1.py … test_p7.py
```

**🟢 = free to redesign / rewrite / split / add new files.**
**🔴 = must remain functionally identical. You may add to (e.g. add a new FormSpec entry to `forms.py`), but not subtract from or change behavior.**

If you find yourself wanting to change a solver's signature or return shape, **stop and ask** — that's a backend change, not a UX change.

### Verification gate

After ANY change you make, this MUST still pass with 45 tests green:

```bash
cd "4. Semester/Linear Control Design/EXAM/Solver" && pytest -q
```

If it doesn't, you've touched something you shouldn't have.

---

## 3. The user-visible problems you're solving

The user worked through some exam questions with the tool and reported real friction:

### Problem A — "Too many blank fields per form"

Example: `P4 — 2nd-order specs` has five inputs (Mp, ζ, ω_n, t_p, t_s_2pct) and the user typically only fills one or two. The blanks are visually noisy and intimidating.

**Fix ideas:**
- Dynamically show/hide fields based on what's been entered or selected. E.g., in `P6 — PI-Lead`, the `unknown` dropdown chooses {alpha, Ni, KP} — each mode only needs a specific subset of fields, so hide the irrelevant ones.
- For forms where any subset of fields can be filled (P4 2nd-order), gray out filled-in-derived values to show what comes from where.
- Add a "Reset" / "Clear all" button.
- Add subtle placeholder text or examples in each `QLineEdit`.

### Problem B — "Match-key dropdown is awkward"

When a solver returns a dict (e.g., P4 2nd-order returns `{zeta, Mp, omega_n, omega_d, t_p, ...}`), the user must pick which key to match against. The current dropdown is a plain `QComboBox` labeled "Match against key:" and defaults to `auto`. Auto mostly works but exam distractors are designed to coincide with other dict keys — auto sometimes can't pick a winner and the user must intervene.

**Fix ideas:**
- Show the dict result as a clean **table** (key | value | unit), not a comma-joined string. Let the user click a row to "match against this key."
- After Solve, show the result-against-every-key as a heatmap — each option × each key cell colored by closeness. Visually obvious which option-key combo is the answer.
- Promote the auto-mode hints (the note column) to be more prominent — they tell the user which trap each distractor is.
- Add units next to each metric (`omega_n = 2.04 rad/s`, `t_p = 1.77 s`, `Mp = 0.17 (= 17%)`).

### Problem C — "Pattern-first navigation is too granular"

14 leaves under 7 pattern parents is fine for browsing but not for fast access during a 50-minute exam.

**Fix ideas:**
- A search box at the top of the sidebar that filters variants by name + by what they compute. ("overshoot", "K_P", "Bode", "block").
- Keyboard shortcuts: `Ctrl+1..7` to jump pattern, `↑/↓` to navigate variants, `Enter` to solve.
- A "Recently used" section at the top of the sidebar (persist to disk between launches).
- An "Examples" submenu per form that loads a pre-canned set of test inputs (pull from `tests/oracle_data.py` — it's already structured for this).

### Problem D — "Should feel like an AI but can't be one"

This is the meta-friction. The user has no LLM during the exam, so the tool must approximate the "paste a question, get an answer" feel using deterministic logic. The closer you can get to that experience while keeping it fully offline and deterministic, the better.

**Fix ideas (none require AI):**
- A "Smart paste" mode: a single large textarea where the user types their question + options together. Use **deterministic regex/keyword routing** (no LLM) to suggest the right form and pre-fill what it can detect (numbers like `γ_M = 75°`, dB values, parametric TFs). Show what was detected; user confirms.
- A "Question library" tab that contains 20-30 actual past-exam questions with their inputs pre-filled, so the user can drill against the tool.
- Display the form's "what kind of question is this?" preamble — a one-sentence description above the form, with a worked example. Currently each variant has a `title` and `variant` field in its FormSpec; consider promoting these to an `explanation` and an example.
- Live update: as the user types, the TF input echoes the parsed canonical form below. Extend this idea — show derived quantities live (DC gain, poles, etc.) for any TF-shaped input, even in solvers that don't strictly need them yet.

---

## 4. Things the user explicitly said NOT to do

- **Don't break the offline guarantee.** No new network dependencies, no LLM calls, no remote font loading, no telemetry.
- **Don't add dependencies casually.** If a UX feature truly needs a new pip package, add it to `requirements.txt` and pin it to a specific version. Default: stay within the current dep list.
- **Don't change the deterministic answer.** If the user enters a question with a known answer, the tool's computed value must remain the same as before your changes. Use the `pytest` suite as your guarantee.
- **Don't restructure the directory tree** outside of `lcd_solver/ui/`. Other folders are referenced by tests and the design spec.

---

## 5. Worked example of the current friction (so you can feel it)

This is the question the user got stuck on, ReExam F22 Q2:

> **Closed-loop TF is `K / (s² + 2s + K)`. Step response shows 17% overshoot. Find ω_d.**
> Options: 0.87, 1.0, 1.73, 2.0 rad/s.

Today's solver path (after the latest commit `fa3fdcb`):
1. User opens `P4 — Closed-loop + 1 spec → full table` (a new combo form added precisely because of this friction).
2. User types `K / (s**2 + 2*s + K)` into the closed-loop field.
3. User picks `Mp` from the dropdown and types `0.17`.
4. User pastes the four options into the options textarea.
5. User leaves match-key at `auto`.
6. User clicks Solve.
7. **Result panel shows a comma-joined string of 13 metrics** — `zeta = 0.491274, Mp = 0.17, Mp_pct = 17, omega_n = 2.03552, omega_d = 1.77295, t_p = 1.77196, t_s_2pct = 4, t_s_5pct = 3, t_r = 0.884293, omega_BW = 2.60926, omega_r = 1.46402, M_r = 1.16849, K = 4.14336`. Wall of text.
8. Options table shows `0.87 also_plausible near: t_r (Δ=1.6%)`, `1.73 also_plausible near: t_p (Δ=2.4%), omega_d (Δ=2.4%)`, `2.0 also_plausible near: omega_n (Δ=1.7%)`. Three "also_plausible" rows, no clear winner.
9. User has to mentally connect "the question asks for ω_d" to "the row with `omega_d` in its note", switch the dropdown to `omega_d`, click Solve again.

The information is all there. The presentation is the problem.

**A better experience might look like:**
- A two-pane result: left is a sortable **table of all 13 metrics with units**, right is the options ranked & colored.
- Each option's row clearly says which metric it most resembles (already true, but in a UI element that doesn't get lost in a wide table).
- Click an option's "near: omega_d" link → it re-runs the match against just that key with one click, not a dropdown change.
- Or even better: render the metrics on a small Bode-style graphic or pole-zero plot so the user has spatial intuition.

You decide. Just make this scenario fast and clear.

---

## 6. Sanity-check commands

Before declaring done:

```bash
# 1. Backend regression — must be 45 passed
cd "C:/Users/Mads2/DTU/4. Semester/Linear Control Design/EXAM/Solver" && pytest -q

# 2. Launches without error
python run.py
# Open every sidebar leaf, type something into the form, hit Solve. No tracebacks anywhere.

# 3. End-to-end smoke for the ReExam F22 Q2 case (the canonical friction example)
# Manual: P4 → Closed-loop + spec. Inputs as in section 5. Result must include omega_d ≈ 1.77,
# and `1.73` must be reachable as the answer within ≤2 clicks.
```

There is a programmatic smoke pattern you can copy from the latest commit history — see `git show fa3fdcb` for the structure (a headless QApplication, build_form, populate fields, call `_on_solve`, read back `result_panel`).

---

## 7. Suggested order of work

Don't try everything at once. Ship in passes:

**Pass 1 — result panel polish** (highest impact, smallest blast radius)
- Replace the comma-joined value string with a real table (key | value | unit) for DICT results.
- Add units. The unit table for our domain is small:
  - `omega_*` → `rad/s`
  - `t_*` → `s`
  - `Mp` → dimensionless (also show as `Mp_pct` → `%`)
  - `zeta`, `K`, `N_i`, `alpha` → dimensionless
  - `GM_dB` → `dB`, `PM_deg` → `°`
  - `K_p, K_v, K_a` → varies by system type; show as dimensionless
- Promote the note column to be more readable (line-wrap, no truncation).
- Color the option flag cell cleanly: green for match, yellow for also_plausible, red-ish for unparseable, neutral for no_match.

**Pass 2 — form polish**
- Add a one-line explanation above each form (extend `FormSpec` with an optional `explanation: str` field and surface it).
- Add field-level placeholders / tooltips. Many fields are obvious to a controls student (γ_M, ζ, ω_n) but the units and "leave blank for unknown" semantics aren't.
- Dynamic field show/hide where dropdowns drive the input set. Top priority: `P6 — PI-Lead (3-way)` — the `unknown` dropdown should hide the irrelevant fields. Same for `P7 — Nested ess` and its `architecture` dropdown.
- Reset button per form.

**Pass 3 — navigation**
- Sidebar search box (filter on title/variant text).
- Keyboard shortcut: `Ctrl+F` to focus the search.
- Persist window size, position, and last-selected form to a JSON file in `%APPDATA%` or `~/.lcd_solver/state.json`.

**Pass 4 — examples library**
- An "Examples" menu (or a button on each form) that loads pre-canned inputs. Source the values from `tests/oracle_data.py` — it already has 30+ historical exam questions with all fields and the official facit. Read the file, parse the dicts, build a "Load example…" QAction list.

**Pass 5 (optional) — smart paste**
- A separate top-level tab "Smart paste" with a single large textarea. Use deterministic regex to detect:
  - `G(s) = …` or `G(s)=` patterns → extract the TF string
  - `γ_M = X°` or `gamma_M = X` patterns → numeric
  - `α = 0.0…` → numeric
  - `ω_c =`, `ω_n =`, `M_p = X%`, `ζ = …` etc.
  - Keywords: "overshoot", "phase margin", "stable for K", "feedforward", "block diagram"
- Match the keywords to the most likely pattern, jump to that form, pre-fill detected fields.
- The user reviews and clicks Solve. No LLM involved.

Don't ship Pass 5 if it gets messy — Passes 1-4 alone are huge wins.

---

## 8. Commit policy

- One commit per pass (or per logical sub-feature within a pass — your judgment).
- Commit message style: short subject (under 70 chars), terse body if needed. **Never** mention AI/agent/LLM/Claude/Antigravity in the message.
- Stage by explicit path: `git add "4. Semester/Linear Control Design/EXAM/Solver/lcd_solver/ui/widgets.py" …`. Listing 5-10 paths is fine; do not use wildcards or `-A`.
- After every commit, `pytest -q` must show 45 passed. If it doesn't, you've broken locked code — revert and fix.

---

## 9. Where to look for context

If you need more background while working:
- `docs/superpowers/specs/2026-05-30-lcd1-solver-design.md` — the design spec
- `docs/superpowers/plans/2026-05-30-lcd1-solver.md` — the implementation plan that was executed
- `Obsidian/Courses/34722 Linear Control Design 1/Exam Prep/00 LCD1 — Exam Hub.md` — the exam's pattern taxonomy in the user's own notes; very useful for understanding what kind of question maps to what form
- `Obsidian/Courses/34722 Linear Control Design 1/Formulas/Exam Formula Cheat-Sheet.md` — the formulas the backend implements
- `Obsidian/Courses/34722 Linear Control Design 1/Exam Prep/Walkthroughs/W-F22 — Worked Exam.md` and `W-ReExam F22 — Worked Exam.md` — full worked walkthroughs of two past papers with the question wording, options, and facit
- `4. Semester/Linear Control Design/EXAM/Scripts/solved/solve_*.m` — the original MATLAB solve scripts that the Python backend was ported from

You do not need to read all of these. They exist if you want them.

---

## 10. When you think you're done

Open the GUI. Try ReExam F22 Q2 (the worked example in section 5) from scratch. If you can get to "1.73 is the answer because it's the option closest to ω_d" in **≤30 seconds and ≤5 mouse clicks**, you're done.

If it still takes scrolling, dropdown-fiddling, and squinting at a comma-joined string — you're not done yet.

Good luck.
