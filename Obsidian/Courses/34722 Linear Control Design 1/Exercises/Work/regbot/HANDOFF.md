---
course: "34722"
course-name: "Linear Control Design 1"
type: handoff
tags: [LCD, regbot, handoff]
date: 2026-04-15
---
# REGBOT Balance Assignment — Session Handoff

> [!abstract] Purpose
> Complete context for a fresh Claude Code session to pick up this project. Read this file top to bottom; everything you need — repos, file layout, current state of each task, gotchas, next steps — is here.
>
> **Deadline: 17 May 2026.**

---

## 1. Where to Resume

**Current status:** Tasks 1–3 are designed in MATLAB and verified in Simulink. The balance recovery from a 10° initial tilt works. The velocity loop tracks `v_ref = 0.5 m/s` cleanly. Nothing has been tested on the physical REGBOT yet.

**Next decision point:** pick one of:

1. **Physical REGBOT Test 3a** (`vel=0, bal=1, log=15 : time=10`) — validate Task 2 on the real robot before layering on Task 4.
2. **Task 4** (position outer loop) — same pattern as Task 3, one layer further out.
3. **Report writing** — LaTeX report submodule has Task 1 + Task 2 written; Task 3 and Task 4 sections still have TODOs.
4. **Physical Test 3b** (square run at 0.8 m/s) — note: sim shows limit-cycle growth at 0.8 m/s step; real-world smoothness might make this work, might not.

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
└── lib/                        ← 9 helper function files
    ├── describe_plant.m
    ├── identify_tf.m
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
├── PLAN.md                        ← 5-phase plan until deadline (older, less important)
├── Images/                        ← all plots from MATLAB + Simulink scope screenshots
└── Report/                        ← LaTeX report (submodule, junction)
```

---

## 3. The MATLAB Workflow (Important)

The script was split so `regbot_mg.m` is fast to load and the design work is quarantined in per-task files.

- **To just simulate:** open Simulink — `regbot_mg.m` loads via `PreLoadFcn` (or run it manually first). No plots, no linearise, no design math. Takes under a second.
- **To redesign a controller:** run the corresponding `design_taskN_*.m` script. Each one:
  1. Calls `regbot_mg` at the top to get physical params + prior-task gains in the workspace.
  2. Does the full Lecture 10 workflow with all intermediate values printed to the command window.
  3. Generates all plots for the report.
  4. Pushes the new gains to the base workspace (so you can immediately test in Simulink).
  5. Ends by printing a copy-pasteable gains block. Example:
     ```
     ==============================================================
       Copy-paste this block into regbot_mg.m (Task 2 gains)
     ==============================================================
         Kptilt = 1.1372;
         titilt = 0.2000;
         tdtilt = 0.1355;
         tipost = 0.1682;
     ```
  6. You paste that block into the matching "Committed controller gains" heading in `regbot_mg.m` and commit.

Never edit gains inside `regbot_mg.m` by hand — always derive them from a design script so the Bode/Nyquist/step plots are reproducible.

### Helpers in `lib/`

All loaded automatically when `regbot_mg.m` runs (it adds its folder + `lib/` to the MATLAB path). Call them from any script without special setup:

- `print_tf(name, G)` — pretty-print a transfer function in polynomial form.
- `identify_tf(model, inBlockPath, outBlockPath)` — linearise a Simulink model between two top-level block paths, return a minimum-realisation `tf`.
- `describe_plant(G)` — compact poles/zeros/DC-gain/RHP-count summary.
- `plot_pz_stability(G, title)` — pole-zero map with LHP/RHP shading.
- `plot_nyquist_critical(G, title)` — Nyquist with (−1, 0) highlighted.
- `save_plot(fig, closure, title, dir, name)` — thin wrapper to save a figure with title + grid.
- `pick_image_dir()` — returns the Obsidian Images path if available, else `docs/images`. `FORCE_LOCAL = true` in the source forces local.
- `poly_to_str`, `ternary` — internal helpers.

---

## 4. Simulink Model State

### Top level (as currently wired)

```
v_ref ── Sum(+−) ── Vel_PI ── Kpvel_gain ── Tilt_Controller(subsystem)
          ↑                                         ↓
     wheel_vel_filter ←──── wheel_vel_filter output (tap)
                                                    ↓
                    vel_ref ── Wheel-speed PI ── Limit9v ── robot with balance
                                                                ↓
                                                    pitch, gyro, x_position, lin_vel
                                                                ↓
                                                pitch, gyro → Tilt_Controller
```

Top-level blocks that `linearize()` calls reference by name (case-sensitive):

- `/vel_ref` — gain block at balance output / wheel-speed input.
- `/Limit9v` — the ±9 V saturation block.
- `/wheel_vel_filter` — the 1/(twvlp·s + 1) low-pass.
- `/robot with balance` — the Simscape Multibody robot model (outputs pitch, gyro, x_position, lin_vel; inputs motor_Voltage, desturb_force).
- `/Kpvel_gain` — Gain block that outputs `theta_ref`. **Must be named exactly `Kpvel_gain`**; Task 3 design script references it.

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

The gyro Lead is combined with pitch **before** the error sum (multiplicative `(τ_d s + 1)` Lead), not added in parallel after the PI blocks (additive `τ_d s`). The distinction matters — see Plain-English Guide section 7 and "What bit us" section 8 in the Obsidian note.

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
| | `Kptilt` | 1.1372 | \|L(jω_c)\| = 1 | — |
| **3 — Velocity outer loop** (plant: `Gvel,outer`, 9th order, stable, RHP zero at +8.51 rad/s) | ω_c | 1 rad/s (limited by RHP zero: `ω_c ≤ z/5`) | 1 | 1.00 |
| | γ_M | 60° min | 60° | 64.2° |
| | GM | upper bound | — | +7.84 dB |
| | N_i | 3 | standard | — |
| | `Kpvel` | 0.1616 | \|L(jω_c)\| = 1 | — |
| | `tivel` | 3.0000 s | N_i/ω_c | — |
| | Lead | none (PI alone gave PM) | — | — |
| **4 — Position** | — | not started | — | — |

### Simulation state (what's been verified)

- **Task 2 (balance):** 10° initial tilt → recovery to 0° in ~1 s, motor voltage peaks 1.3 V (far below ±9 V limit). `regbot_task2_sim_recovery_10deg.png` in Images/.
- **Task 3 (velocity) at 0.5 m/s step:** clean tracking with visible RHP-zero inverse response (wheel vel dips to −0.3 m/s at t = 1 s before climbing to 0.52 m/s). Pitch peaks ~7°, motor voltage ~2.15 V, settling ~5 s.
- **Task 3 at 0.8 m/s step:** limit-cycle growth. Pitch swings ±23°, oscillation period ~1.5 s (near the plant's complex pole pair). Large-signal nonlinearities break the linear design. See gotchas section.

---

## 6. What Works, What Might Bite

### Works cleanly

- End-to-end MATLAB script runs without errors.
- Every `print_tf` prints a clean polynomial.
- `linearize()` identifies `Gtilt`, `Gwv`, and `Gvel,outer` reproducibly. Numbers match across runs to 4+ decimals.
- Task 2 MATLAB design reproduces all the documented values when re-run.
- Simulink model compiles with any valid gain set. Setting any task's gain to 0 breaks only that loop (the lower-layer ones still work).

### Known gotchas

- **Block naming for `linearize()` is case-sensitive.** We have `VEL_CTRL_OUT_BLOCK = '/Kpvel_gain'` in `design_task3_velocity.m`. The Simulink block has to be named exactly `Kpvel_gain` — not `kpvel_gain`, not `KpvelGain`.
- **Task 3 phase unwrapping is iffy** at `ω_c = 1`: `bode()` reports `+262°` which is equivalent to `−98°`. The script's `if phi_Lead <= 0` fallback saved it, but if someone changes `wc_vel`, the unwrap math could produce wrong `phi_Lead`. Robust fix (not yet applied): wrap phase to `[−180°, 180°]` before using. Worth tightening later.
- **Nonlinear limit cycling at large `v_ref` commands.** Pitch >20° breaks the linearisation. If Task 3 needs full-speed step responses, add a `Saturation` block on `theta_ref` (±0.175 rad ≈ ±10°) with anti-windup on the velocity PI integrator. Simplest anti-windup: swap the PI `Transfer Fcn` for a Simulink `PID Controller` block in "clamping" mode.
- **Negative gain margin is OK** for Task 2 (unstable plant). If `margin(L_tilt)` ever reports a positive GM, something's been mis-wired.
- **Autosave files (`*.slx.autosave`, `*.asv`) and build artefacts (`slprj/`, `*.slxc`) are gitignored.** Don't panic if they show up — they regenerate on use.
- **`startAngle` in `regbot_mg.m`.** Set to 0 for velocity tracking tests, 10 for balance recovery tests. The physical robot always starts at 0 (held still), this variable is purely a simulation initial condition.

---

## 7. Obsidian Documentation State

`REGBOT Balance Assignment.md` is the primary reference. Sections in order:

1. Intro + Preparation checklist.
2. **Plain-English Guide — Start Here if You're New to This** — nine sub-sections covering the whole pedagogy from the broom analogy to why Task 2 needs Lecture 10 Method 2, the four-step recipe, physical meanings of each knob, and the gotchas we hit. Any teammate without a strong linear-control background should read this first.
3. Control Architecture Overview (mermaid diagram — cascaded loops).
4. Tasks 1–4 abstract descriptions (from the course brief).
5. Mandatory Report instructions (course brief).
6. Design Workflow Checklist.
7. Key Design Principles (Lecture 10 takeaways).
8. **Progress Log** — chronological log of sessions. Session 1 (2026-04-15) has the detailed writeup:
   - Plant identification via `linearize()` (Gwv, Gtilt prints and plots).
   - Task 1 design with verification.
   - **Task 2 — Balance Controller (Lecture 10 Method 2)** with full step-by-step derivation, mermaid for the Method 2 workflow, block-by-block table for the Simulink implementation, all intermediate design values, and the Simulink IC recovery screenshot.
   - **Task 3 — Velocity outer loop (in progress)** — mermaid for top level + inside the subsystem, block-by-block table, build order, design rationale.
9. Next Session — Planned Work.

Mermaid diagrams use a **muted pastel palette** for Obsidian dark mode compatibility. The palette is consistent across all diagrams:
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
| `balance-controller.tex` | ✅ Written (full Lecture 10 Method 2 writeup + figures) |
| `velocity-controller.tex` | Stub — Task 3 TODO |
| `position-controller.tex` | Stub — Task 4 TODO |
| `conclusion.tex` | Stub |

The Report's `images/` folder has Task 1 and Task 2 figures copied in. When Task 3 artwork needs to appear in the report, copy the matching Task 3 images from `regbot/Images/` into `Report/images/` and reference from the new section.

---

## 8. Recent Commits (top of each branch)

### `MadsRudolph/DTU` — main
- `e7d3a1d` Add beginner-friendly Plain-English Guide to REGBOT Balance note
- `e7d63ba` REGBOT Task 3: velocity outer loop + Obsidian writeup
- `62d0728` Bump REGBOT-Balance submodule: drop unused starter image
- `e045654` Bump REGBOT-Balance submodule: subsystem refactor + MATLAB split
- `301c348` REGBOT balance: Task 2 restructure + Simulink IC verification

### `Skab101/REGBOT-Balance` — main
- `7c363aa` Task 3: velocity outer loop (PI at wc = 1 rad/s)
- `7e714e4` Drop unused starter image motor to velocity.png
- `191ac40` Split MATLAB into thin loader + per-task design scripts + lib/ helpers
- `74b0744` Refactor balance controller into a Simulink subsystem
- `839a7b0` Task 2: align balance controller with Lecture 10 Method 2

### `MadsRudolph/REGBOT-Balance-assignment` (Report) — main
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

- "Help me do the physical REGBOT Test 3a to verify Task 2 on the real robot."
- "Let's start Task 4 — position outer loop."
- "Let's fill in the Task 3 and Task 4 LaTeX report sections."
- "Help me tighten the phase-unwrapping logic in design_task3_velocity.m so ω_c changes don't break the Lead math."
- "Add saturation + anti-windup to the Task 3 velocity controller so the 0.8 m/s step works."

---

*Document last updated: 2026-04-15 — end of session covering the Simulink Lead-placement fix, MATLAB split into per-task design scripts + lib/, balance-controller subsystem refactor, Task 3 design and wiring, and the Plain-English Guide.*
