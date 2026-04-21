---
course: "34722"
course-name: "Linear Control Design 1"
type: handoff
tags: [LCD, regbot, handoff]
date: 2026-04-21
---
# REGBOT Balance Assignment — Session Handoff

> [!abstract] Purpose
> Complete context for a fresh Claude Code session to pick up this project. Read this file top to bottom; everything you need — repos, file layout, current state of each task, gotchas, next steps — is here.
>
> **Deadline: 17 May 2026.**

---

## 1. Where to Resume

**Current status:** Tasks 1–4 are designed in MATLAB and verified in Simulink.
- Task 2: balance recovery from 10° initial tilt works.
- Task 3: velocity tracking at 0.5 m/s step is clean (RHP-zero inverse response visible and expected); 0.8 m/s step triggers large-signal limit cycles in the non-linear model.
- Task 4: 2 m position step reaches peak velocity 0.80 m/s (spec ≥ 0.7 ✓), settles at 2 m cleanly, closed-loop stable with PM = 59°, GM = 23.2 dB.

**Nothing has been tested on the physical REGBOT yet.**

**Next decision point:** pick one of:

1. **Physical REGBOT tests** — start with Test 3a (`vel=0, bal=1, log=15 : time=10`) for Task 2, then Test 3b (square run), then Test 4 (2 m position move). All four controllers are ready for it.
2. **Report polish + submission** — LaTeX is written for Tasks 1–4 and Task 2 polish. Final pass, add physical-test plots and comments, export PDF, submit as `Group_47.pdf` on Learn.
3. **Tune any controller that underperforms on the real robot** — bring the gain back into the matching `design_task*.m`, iterate, copy new block into `regbot_mg.m`.
4. **Fix the 0.8 m/s limit cycle in Task 3** (if needed) — add `Saturation` on `theta_ref` (±0.175 rad) with anti-windup on the velocity PI integrator. Simplest: swap the PI `Transfer Fcn` for Simulink's `PID Controller` block in "clamping" mode.

---

## 2. Repos and File Layout

### Three git repositories

| Path | Role | Remote |
|---|---|---|
| `C:\Users\Mads2\DTU` | Main DTU repo (Obsidian vault + personal work) | `MadsRudolph/DTU` |
| `4. Semester\Linear Control Design\REGBOT-Balance-Assignment` | Team MATLAB/Simulink repo (submodule) | `Skab101/REGBOT-Balance` |
| `Obsidian\...\regbot\Report` | LaTeX report (submodule, junction from REGBOT-Balance-Assignment\Report) | `MadsRudolph/REGBOT-Balance-assignment` |

### MATLAB/Simulink layout — `REGBOT-Balance-Assignment/simulink/`

```
simulink/
├── regbot_1mg.slx              ← the Simulink model
├── regbot_mg.m                 ← THIN workspace loader (physical params + committed gains)
├── design_task1_wheel.m        ← standalone Task 1 design (PI on Gvel,day5)
├── design_task2_balance.m      ← standalone Task 2 design (Lecture 10 Method 2)
├── design_task3_velocity.m     ← standalone Task 3 design (PI on Gvel,outer)
├── design_task4_position.m     ← standalone Task 4 design (P on Gpos,outer)
└── lib/                        ← 9 helper function files
    ├── describe_plant.m
    ├── identify_tf.m           ← 4-arg: (model, in, out, out_port=1)
    ├── pick_image_dir.m
    ├── plot_nyquist_critical.m
    ├── plot_pz_stability.m
    ├── poly_to_str.m
    ├── print_tf.m
    ├── save_plot.m
    └── ternary.m
```

### Obsidian layout — `Obsidian/Courses/34722 Linear Control Design 1/Exercises/Work/regbot/`

```
regbot/
├── REGBOT Balance Assignment.md   ← primary note — read this first
├── HANDOFF.md                     ← this file
├── PLAN.md                        ← older 5-phase plan (superseded by this note)
├── Images/                        ← all plots from MATLAB + Simulink scope screenshots
└── Report/                        ← LaTeX report (submodule, junction)
```

> [!note] Mirror in the MATLAB submodule
> A `docs/` folder in the `REGBOT-Balance-Assignment` submodule contains a copy of `REGBOT Balance Assignment.md` + images for teammates who don't have the Obsidian vault set up. If you edit one, remember to mirror to the other (they can drift otherwise).

---

## 3. The MATLAB Workflow (Important)

The script was split so `regbot_mg.m` is fast to load and the design work is quarantined in per-task files.

- **To just simulate:** open Simulink — `regbot_mg.m` loads via `PreLoadFcn` (or run it manually first). No plots, no linearise, no design math. Takes under a second.
- **To redesign a controller:** run the corresponding `design_taskN_*.m` script. Each one:
  1. Calls `regbot_mg` at the top to get physical params + prior-task gains in the workspace.
  2. Temporarily sets the current loop's gain to 0 (breaking the loop at that point) before calling `linearize()`.
  3. Does the full Lecture 10 workflow with all intermediate values printed to the command window.
  4. Generates all plots for the report.
  5. Pushes the new gains to the base workspace (so you can immediately test in Simulink).
  6. Ends by printing a copy-pasteable gains block. Example:
     ```
     ==============================================================
       Copy-paste this block into regbot_mg.m (Task 4 gains)
     ==============================================================
         Kppos = 0.5335;
         tdpos = 0.0273;
     ```
  7. You paste that block into the matching "Committed controller gains" heading in `regbot_mg.m` and commit.

Never edit gains inside `regbot_mg.m` by hand — always derive them from a design script so the Bode/Nyquist/step plots are reproducible.

### Helpers in `lib/`

All loaded automatically when `regbot_mg.m` runs (it adds its folder + `lib/` to the MATLAB path). Call them from any script without special setup:

- `print_tf(name, G)` — pretty-print a transfer function in polynomial form.
- `identify_tf(model, in_block, out_block, out_port)` — linearise a Simulink model between two top-level block paths, return a minimum-realisation `tf`. The optional `out_port` (default 1) selects which output port of the out_block to measure — used for `/robot with balance` where port 1 = pitch, port 3 = x_position.
- `describe_plant(G)` — compact poles/zeros/DC-gain/RHP-count summary.
- `plot_pz_stability(G, title)` — pole-zero map with LHP/RHP shading.
- `plot_nyquist_critical(G, title)` — Nyquist with (−1, 0) highlighted.
- `save_plot(fig, closure, title, dir, name)` — thin wrapper to save a figure with title + grid.
- `pick_image_dir()` — returns the Obsidian Images path if available, else `docs/images`. `FORCE_LOCAL = true` in the source forces local.
- `poly_to_str`, `ternary` — internal helpers.

---

## 4. Simulink Model State

### Top level (as currently wired — all four loops)

```
pos_ref ── Sum(+−) ── Kppos_gain ── (acts as v_ref) ── Sum_vel(+−) ── Vel_PI ── Kpvel_gain ── Tilt_Controller(subsystem)
              ↑                                             ↑                                       ↓
      x_position (tap)                              wheel_vel_filter (tap)                    vel_ref out
                                                                                                    ↓
                                                                              Wheel-speed PI ── Limit9v ── robot with balance
                                                                                                            ↓
                                                                                  pitch, gyro, x_position, lin_vel
                                                                                                            ↓
                                                                                      pitch, gyro → Tilt_Controller
```

Top-level blocks that `linearize()` calls reference by name (case-sensitive):

- `/vel_ref` — gain block at balance output / wheel-speed input. Used by Task 2 design.
- `/Limit9v` — the ±9 V saturation block. Used by Task 1-style ID of Gwv.
- `/wheel_vel_filter` — the 1/(twvlp·s + 1) low-pass. Used by Task 3 design (velocity feedback point).
- `/robot with balance` — the Simscape Multibody robot model. Outputs (port order) **1 = pitch, 2 = gyro, 3 = x_position, 4 = wheel_vel/lin_vel**. Inputs are motor_Voltage and desturb_force.
- `/Kpvel_gain` — Gain block that outputs `theta_ref`. **Exact name required by** `design_task3_velocity.m`.
- `/Kppos_gain` — Gain block that outputs the velocity-reference branch. **Exact name required by** `design_task4_position.m`.

### Balance controller subsystem (Task 2 wiring)

Three inports, one outport:

- **In1:** pitch (rad)
- **In2:** gyro (rad/s)
- **In3:** theta_ref (rad) — added during Task 3. Replaced the hard-coded `Constant = 0` block.
- **Out1:** vel_ref (m/s)

Internal topology (critical — we broke this once, don't break it again):

```
pitch ──┐
        ├── Sum(++) ─── Sum(+−) ── Gain(−1) ── TF_post ── TF_PI ── Kptilt ── vel_ref
gyro·τd ┘                ↑
                      theta_ref (In3)
```

The gyro Lead is combined with pitch **before** the error sum (multiplicative `(τ_d s + 1)` Lead), not added in parallel after the PI blocks (additive `τ_d s`). See Plain-English Guide section 7 in the Obsidian note.

---

## 5. Current Design Values

| Task | Parameter | Value | Spec | Achieved |
|---|---|---|---|---|
| **1 — Wheel-speed PI** (plant: `Gvel,day5 = 13.34/(s+35.71)`) | ω_c | 30 rad/s | ≥30 | 29.9 rad/s |
| | γ_M | 60° min | 60° | 121.6° |
| | N_i | 3 | standard | — |
| | `Kpwv` | 3.31 | — | — |
| | `tiwv` | 0.10 s | — | — |
| | `Kffwv` | 0 | — | — |
| **2 — Balance (Lecture 10 Method 2)** (plant: `Gtilt`, 7th order, 1 RHP pole at +8.7 rad/s) | ω_c | 15 rad/s | 15 | 15.00 |
| | γ_M | 60° | 60° | 60.0° |
| | GM | lower bound (negative OK) | — | −4.6 dB |
| | N_i | 3 | standard | — |
| | `tipost` | 0.1682 s | 1/ω_peak of \|Gtilt\| | — |
| | `titilt` | 0.200 s | N_i/ω_c | — |
| | `tdtilt` | 0.1355 s | tan(φ_Lead)/ω_c | — |
| | `Kptilt` | 1.1370 | \|L(jω_c)\| = 1 | — |
| **3 — Velocity outer loop** (plant: `Gvel,outer`, 9th order, stable, RHP zero at +8.51 rad/s) | ω_c | 1 rad/s (limited by RHP zero: `ω_c ≤ z/5`) | 1 | 1.00 |
| | γ_M | 60° min | 60° | 64.2° |
| | GM | upper bound | — | +7.84 dB |
| | N_i | 3 | standard | — |
| | `Kpvel` | 0.1616 | \|L(jω_c)\| = 1 | — |
| | `tivel` | 3.0000 s | N_i/ω_c | — |
| | Lead | none (PI alone gave PM) | — | — |
| **4 — Position outermost loop** (plant: `Gpos,outer`, has a free integrator `v→x` already, so no I-term needed) | ω_c | 0.6 rad/s (iterated 0.2 → 0.5 → 0.6 to hit mission-speed spec) | ≈ ω_c,vel / 1.7 | 0.60 |
| | γ_M | 60° target | 59° | 59° |
| | GM | upper bound | — | +23.2 dB |
| | `Kppos` | 0.5335 | \|L(jω_c)\| = 1 | — |
| | `tdpos` | 0.0273 s | wanted by script (+0.94° phase) but dropped — see gotchas | — |

### Simulation state (what's been verified)

- **Task 2 (balance):** 10° initial tilt → recovery to 0° in ~1 s, motor voltage peaks 1.3 V. `regbot_task2_sim_recovery_10deg.png` in Images/.
- **Task 3 (velocity) at 0.5 m/s step:** clean tracking with visible RHP-zero inverse response. Pitch peaks ~7°, settling ~5 s.
- **Task 3 at 0.8 m/s step:** limit-cycle growth. Pitch swings ±23°, large-signal nonlinearities break the linear design. Acceptable for ramped mission profiles; would need saturation + anti-windup for pure step commands.
- **Task 4 (position) 2 m step:** peak velocity 0.80 m/s (spec ≥ 0.7 m/s ✓), settles at 2 m, closed-loop stable.

---

## 6. What Works, What Might Bite

### Works cleanly

- End-to-end MATLAB scripts run without errors.
- Every `print_tf` prints a clean polynomial.
- `linearize()` identifies `Gwv`, `Gtilt`, `Gvel,outer`, and `Gpos,outer` reproducibly. Numbers match across runs to 4+ decimals.
- Simulink model compiles with any valid gain set. Setting any task's gain to 0 breaks only that loop (the lower-layer ones still work).

### Known gotchas

- **Block naming for `linearize()` is case-sensitive.** `Kpvel_gain` and `Kppos_gain` must be named exactly that.
- **`robot with balance` output ports are ordered 1=pitch, 2=gyro, 3=x_position, 4=lin_vel.** Use the 4th arg of `identify_tf` (`out_port`) to pick the right one. Task 4 design uses port 3.
- **Phase unwrapping.** `bode()` returns unwrapped phase. For Tasks 3 and 4, the raw `φ_G` reads as `+262°` (really `−98°`) at low ω because of how MATLAB wraps. Task 4 now wraps `φ_G` to `(−180°, 180°]` via mod arithmetic before using it in the Lead formula; Task 3 still relies on the `if phi_Lead <= 0` fallback (which happened to work). If you change `wc_vel`, update Task 3 the same way Task 4 was fixed.
- **Pure-Lead TFs are improper.** Simulink rejects a standalone `(τ_d s + 1)` Transfer Fcn. For Task 2 we use the gyro shortcut (`τ_d · gyro + pitch` ≡ `(τ_d s + 1)·pitch`) so no problem. For Task 4 the design script *wanted* a 0.94° Lead (tdpos = 0.027 s) but Simulink can't host the block without a filter pole, and that tiny amount of PM isn't worth one — Lead was dropped. If you ever do need a proper Lead, use `(τ_d s + 1)/(α·τ_d s + 1)` with `α = 0.1`.
- **Nonlinear limit cycling at large `v_ref` commands.** Pitch >20° breaks the linearisation. If needed for testing full-speed steps, add `Saturation` on `theta_ref` with anti-windup.
- **Negative gain margin is OK** for Task 2 (unstable plant). If `margin(L_tilt)` ever reports positive GM, something's been mis-wired.
- **Autosave files (`*.slx.autosave`, `*.asv`) and build artefacts (`slprj/`, `*.slxc`) are gitignored.** Don't panic if they show up.
- **`startAngle` in `regbot_mg.m`.** Set to 0 for velocity/position tracking tests, 10 for balance recovery tests. Physical robot always starts at 0 — this is purely a simulation initial condition.

---

## 7. Obsidian Documentation State

`REGBOT Balance Assignment.md` is the primary reference. Sections in order:

1. Intro + Preparation checklist.
2. **Plain-English Guide — Start Here if You're New to This** — nine sub-sections covering the whole pedagogy from the broom analogy through the four-step recipe to the gotchas. Anyone without a strong linear-control background should read this first.
3. Control Architecture Overview (mermaid diagram — cascaded loops).
4. Tasks 1–4 abstract descriptions (from the course brief).
5. Mandatory Report instructions.
6. Design Workflow Checklist.
7. Key Design Principles.
8. **Progress Log** — chronological detail:
   - Session 1 (2026-04-15): plant ID, Task 1, Task 2 Lecture 10 Method 2 writeup, Task 3 mermaids + block-by-block table.
   - Session 2 (2026-04-21): Task 4 added to the note (position controller wiring, design numbers, mermaid if present).
9. Next Session — Planned Work.

Mermaid diagrams use a **muted pastel palette** for Obsidian dark mode compatibility. Consistent across all diagrams:
- `ref` / `start` → slate (#475569)
- `ctrl` / `step` → sage (#4b6b3a)
- `plant` / `done` → muted violet (#5b4b7a)
- `fb` → dusty rose (#7a4141)
- `sum` → neutral (#374151)
- `out` / `decis` → muted gold (#8b6914)

### LaTeX report state — `Report/sections/`

| File | Status |
|---|---|
| `introduction.tex` | ✅ Written |
| `control-architecture.tex` | ✅ Written |
| `wheel-speed-controller.tex` | ✅ Written (Task 1 complete) |
| `balance-controller.tex` | ✅ Written (polished — full Method 2 writeup, IC recovery + velocity tracking figures) |
| `velocity-controller.tex` | ✅ Written (Task 3) |
| `position-controller.tex` | ✅ Written (Task 4) |
| `conclusion.tex` | Likely stub — verify before final compile |

Task 3 and Task 4 images are in `Report/images/`.

---

## 8. Recent Commits (top of each branch)

### `MadsRudolph/DTU` — main
- `9a8676e` Refresh REGBOT HANDOFF.md with end-of-session state (previous)
- `e7d3a1d` Add beginner-friendly Plain-English Guide to REGBOT Balance note
- `e7d63ba` REGBOT Task 3: velocity outer loop + Obsidian writeup
- `62d0728` Bump REGBOT-Balance submodule: drop unused starter image
- `e045654` Bump REGBOT-Balance submodule: subsystem refactor + MATLAB split

### `Skab101/REGBOT-Balance` — main
- `46f1cee` Task 4: position outermost loop (P at wc = 0.6 rad/s)
- `7c363aa` Task 3: velocity outer loop (PI at wc = 1 rad/s)
- `7e714e4` Drop unused starter image motor to velocity.png
- `191ac40` Split MATLAB into thin loader + per-task design scripts + lib/ helpers
- `74b0744` Refactor balance controller into a Simulink subsystem

### `MadsRudolph/REGBOT-Balance-assignment` (Report) — main
- `bc46ffc` Tasks 3 + 4 writeup and Task 2 polish
- `8dd29e8` Task 2: Lecture 10 Method 2 writeup with full design trace

---

## 9. Team and Deadline

- **Group 47:**
  - Andreas Skånning (s241123)
  - Jonas Beck Jensen (s240324)
  - Mads Rudolph (s246132)
  - Sigurd Hestbech Christiansen (s245534)
- **Deadline:** 17 May 2026
- **Report:** max 5 pages, filename `Group_47.pdf`, one submission per group, uploaded to Learn (Course Content → Assignments → REGBOT balance).

---

## 10. Commit Rules

- **No mention of Claude/AI in commit messages.** No `Co-Authored-By`, no "(with Claude)" trailers. Clean commits only.
- **Prefer two commits over one** when changes span concerns (e.g. the Simulink subsystem refactor was committed separately from the MATLAB split).
- **DTU main staging must be selective** — there are lots of unrelated modifications across other courses. Only stage REGBOT-related files. Specifically don't stage `.claude/settings.local.json`.

---

## 11. Cheat Sheet — Starting a Fresh Claude Code Session

Paste this to resume:

```
Read C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1\Exercises\Work\regbot\HANDOFF.md
```

Then pick one:

- "Help me run the physical REGBOT tests (3a, 3b, 4) and collect the plots for the report."
- "Final pass on the report — verify all sections compile cleanly and finish the conclusion."
- "A controller misbehaves on the real robot — help me re-tune."
- "Fix the 0.8 m/s limit cycle in Task 3 with a saturation + anti-windup on theta_ref."

---

*Document last updated: 2026-04-21 — Tasks 1–4 all designed in MATLAB and verified in Simulink, controllers ready for physical REGBOT testing.*
