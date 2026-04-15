---
course: "34722"
course-name: "Linear Control Design 1"
type: handoff
tags: [LCD, regbot, handoff]
date: 2026-04-15
---
# REGBOT Balance Assignment — Session Handoff

> [!abstract] Purpose
> Comprehensive summary of all work done on the REGBOT balance assignment so far. Start a fresh Claude Code session by pointing it at this file to resume work with full context.

---

## 1. Project Setup — What Exists

### Git repos and submodules

| Path | Purpose | Remote |
|---|---|---|
| `C:\Users\Mads2\DTU` | Main DTU repo (personal notes + work) | `MadsRudolph/DTU` |
| `4. Semester\Linear Control Design\REGBOT-Balance-Assignment` | Team MATLAB/Simulink repo (submodule) | `Skab101/REGBOT-Balance` (org) |
| `Obsidian\...\regbot\Report` | LaTeX report (submodule) | `MadsRudolph/REGBOT-Balance-assignment` |
| `4. Semester\Linear Control Design\Day1-Day10` | Personal MATLAB work per day | not git — local only |

### Windows junction

- `REGBOT-Balance-Assignment\Report` → junction to `Obsidian\...\regbot\Report`
- Created with `New-Item -ItemType Junction` via PowerShell
- Not tracked in git (added to `.gitignore`)
- Teammates must recreate it on their PCs

### Key file locations

| File | Path |
|---|---|
| MATLAB script | `REGBOT-Balance-Assignment\simulink\regbot_mg.m` |
| Simulink model | `REGBOT-Balance-Assignment\simulink\regbot_1mg.slx` |
| Plot outputs | `Obsidian\...\regbot\Images\` (auto-detected) or `simulink\images\` |
| Assignment brief | `Obsidian\...\regbot\REGBOT Balance Assignment.md` |
| Project plan | `Obsidian\...\regbot\PLAN.md` |
| LaTeX report | `Obsidian\...\regbot\Report\main.tex` + `sections\*.tex` |

---

## 2. Team and Deadline

- **Group 47** — Andreas Skånning (s241123), Jonas Beck Jensen (s240324), Mads Rudolph (s246132), Sigurd Hestbech Christiansen (s245534)
- **Deadline:** 17 May 2026
- **Today:** 15 April 2026 (~4.5 weeks remaining)

---

## 3. The Four Tasks

| Task | Description | Status |
|---|---|---|
| 1 | Wheel-speed PI controller (inner loop) | ✅ Designed + verified in MATLAB |
| 2 | Balance controller (stabilises inverted pendulum) | ✅ Designed in MATLAB, 🚧 **broken in Simulink** |
| 3 | Velocity outer loop | ⏳ Not started |
| 4 | Position outermost loop | ⏳ Not started |

---

## 4. Plant Identification

Two transfer functions identified from the Simulink model via `linearize()`:

### $G_{wv}(s)$ — voltage → wheel velocity
- 6th order
- DC gain: 0.270 (m/s)/V
- 1 RHP pole at $+10.6$ rad/s
- Not directly used for controller design (Day 5 model used instead for Task 1)

### $G_{tilt}(s)$ — vel_ref → tilt angle
- 7th order
- DC gain: $5.04 \times 10^{-4}$
- 1 RHP pole at $+8.7$ rad/s (inverted pendulum falling mode)
- Plant peak magnitude: 0.588 at $\omega = 5.95$ rad/s
- Used for Task 2 balance controller design

### Day 5 black-box plant
- $G_{vel}(s) = \dfrac{13.34}{s + 35.71}$ (from Day 5 measurements)
- Used for Task 1

> [!important] Interpretation
> Both identified plants have **1 RHP pole** — physically consistent with the inverted pendulum. By Nyquist: $Z = N + P \Rightarrow$ need **1 CCW encirclement of $-1$** for stability.

---

## 5. Design Values (Current)

### Task 1 — Wheel-speed PI (plant: $G_{vel,day5}$)

| Parameter | Value |
|---|---|
| $\omega_c$ | 30 rad/s (achieved 29.9) |
| $\gamma_M$ target | $\geq 60°$ (achieved 121.6°) |
| $N_i$ | 3 |
| `tiwv` | 0.10 s |
| `Kpwv` | 3.31 |
| `Kffwv` | 0 |

### Task 2 — Balance (plant: $G_{tilt}$)

Controller = post-integrator + outer PI-Lead.

| Parameter | Value | Role |
|---|---|---|
| $\omega_{c,tilt}$ | 15 rad/s | Target crossover |
| $\gamma_M$ target | 60° | Phase margin |
| $N_i$ | 3 | PI zero placement |
| `tipost` | 0.1682 s | Post-integrator time constant (= 1/peak of $|G_{tilt}|$) |
| `titilt` | 0.200 s | Outer PI time constant |
| `tdtilt` | 0.1355 s | Gyro-based Lead gain |
| `Kptilt` | 1.137 | Overall loop gain |

**Total controller:**
$$C_{total}(s) = K_p \cdot \underbrace{\frac{-(\tau_{ip}s + 1)}{\tau_{ip}s}}_{\text{sign-flip + post-int}} \cdot \underbrace{\frac{\tau_i s + 1}{\tau_i s}}_{\text{outer PI}} \cdot \underbrace{(\tau_d s + 1)}_{\text{Lead (gyro)}}$$

**MATLAB verification:**
- Closed-loop poles all in LHP ✓
- `margin(L_tilt)` reports: $\omega_c = 15$ rad/s, $\gamma_M = 60°$, GM = -4.6 dB (negative GM is OK when $P = 1$ — it's the lower bound)
- Initial condition response (10° → 0°) in ~1.5 s with small undershoot ✓ (in MATLAB linear model)

---

## 6. MATLAB Script Structure (`regbot_mg.m`)

Organized in numbered steps:

1. **STEP 0** — Setup (paths, s, model name, auto-detect output folder)
2. **STEP 1** — REGBOT physical parameters (used by Simulink model)
3. **STEP 2** — Day 5 plant definition + print
4. **STEP 3** — TASK 1 PI design (sets `Kpwv`, `tiwv`, `Kffwv` — must come before STEP 4!)
5. **STEP 4** — `linearize()` Simulink → $G_{wv}$, $G_{tilt}$ (placeholder values for `Kptilt`, `titilt`, `tdtilt`, `tipost` set here so model compiles)
6. **STEP 5** — Plot plants (Bode, PZ maps, Nyquist)
7. **STEP 6** — TASK 2A: Post-integrator (finds $|G|$ peak, builds $G_{tilt,post}$)
8. **STEP 7** — TASK 2B: Outer PI-Lead on $G_{tilt,post}$ (overwrites placeholders with real values)
9. **STEP 8, 9** — Task 3/4 stubs

Helper functions at bottom: `pick_image_dir`, `identify_tf`, `describe_plant`, `save_plot`, `plot_pz_stability`, `plot_nyquist_critical`, `print_tf`, `poly_to_str`.

**Plot output auto-detection:**
- If Obsidian vault folder exists → save there
- Otherwise → `simulink\images\` (gitignored)
- `FORCE_LOCAL = true` overrides

---

## 7. Simulink Model Structure

### Existing wheel-velocity loop (unchanged)
- Inside the main model: `vel_ref → [PI using Kpwv, tiwv] → [Limit9v ±9V] → motor_Voltage → robot with balance`
- `wheel_vel_filter` on feedback path
- `Push Newton` step block → `desturb_force` on robot

### Inside `robot with balance` subsystem
- Motor model → ground-to-regbot → Motors_and_wheels → balance-joint
- `balance-joint` has `start angle` input that tilts the joint's reference by `startAngle`
- `compensate for start angle` block adds `startAngle/180*pi` to the q output so `pitch` = physical tilt from vertical
- Outputs: `pitch`, `gyro`, `x_position`, `lin_vel`

### User-added balance controller (CURRENT — has structural bug)

```
[Constant 0] ──► Sum(+−) ──► Gain(-1) ──► TF[post-int] ──► TF[outer PI] ──► Sum(++) ──► Gain[Kptilt] ──► vel_ref
                  │                                                            ▲
                 pitch                                                         │
                                                            gyro ──► Gain[tdtilt]
```

- Transfer Fcn 1 (post-integrator): Num `[tipost 1]`, Den `[tipost 0]` ✓
- Transfer Fcn 2 (outer PI): Num `[titilt 1]`, Den `[titilt 0]` ✓
- Feedback sum (first): signs `+ -` (confirmed correct)
- Gain = -1 after sum (confirmed present)
- Gyro path: `gyro → Gain(tdtilt) → second Sum(++)`

---

## 8. What Works

- ✅ Script runs end-to-end without errors
- ✅ Transfer functions print in polynomial form (via `print_tf`)
- ✅ MATLAB design is mathematically stable (all closed-loop poles in LHP)
- ✅ MATLAB initial-condition response (`initial()` on state-space): smooth recovery from 10° tilt in ~1.5 s
- ✅ **Simulink baseline: with `startAngle = 0`, push = 0 — pitch stays at 0, voltage stays at 0 for 10 s** (confirmed stable baseline)
- ✅ First Sum block sign fix (changed from `++` to `+-`) — this was an earlier bug, now resolved

---

## 9. What Doesn't Work (Open Issue)

**Any disturbance in Simulink causes voltage to saturate at $\pm 9$ V and never recover.**

### Symptoms observed across tests

| Test | Result |
|---|---|
| `startAngle = 0`, push = 0 | ✅ pitch stays at 0 |
| `startAngle = 0`, push = 1 N | ❌ voltage saturates at -9 V, pitch settles at -3° |
| `startAngle = 5`, push = 0, `wc_tilt = 15` | ❌ voltage saturates, pitch settles at -3° |
| `startAngle = 10`, push = 0, `wc_tilt = 10` | ❌ voltage saturates, pitch settles at -3° |
| `startAngle = 1`, push = 0, `wc_tilt = 15` | ❌ voltage saturates, pitch settles at -3° |

### Current diagnosis (last message before handoff)

**The gyro-based Lead is wired WRONG in Simulink.**

The user's structure implements:
$$C_\text{actual}(s) = K_p \left[ C_{PI,post}(s)\cdot C_{PI}(s) + \tau_d s \right]$$

But the intended design was:
$$C_\text{intended}(s) = K_p \cdot C_{PI,post}(s) \cdot C_{PI}(s) \cdot (\tau_d s + 1)$$

The difference:
- Intended: Lead $(\tau_d s + 1)$ is **in series** with $C_{PI,post} \cdot C_{PI}$ (multiplicative)
- Actual: $\tau_d s$ is **added in parallel**, bypassing the PI blocks

At higher frequencies the actual controller has much LESS phase boost than intended → effective phase margin is far below 60° → system is nearly unstable → any disturbance saturates the motor.

### Proposed fix (NOT YET APPLIED by user)

Move the `tdtilt · gyro` contribution to the **feedback path** (before the error sum), instead of after the PI blocks:

```
pitch ──┐
        ├──► Sum(++) ──► as feedback into main Sum(+-) with reference 0
gyro ──► Gain(tdtilt) ──┘
```

This realises: feedback = $(\tau_d s + 1) \cdot \theta = \tau_d \dot\theta + \theta$ = Lead applied to pitch.

The resulting characteristic equation matches the intended design exactly (loop gain is the same due to multiplicative commutativity).

### Also consider — gyro sign

If gyro convention is opposite to what we assume (gyro positive when pitch decreasing), `tdtilt` should be negated. User hasn't verified this yet.

---

## 10. Things Already Tried (Don't Repeat)

- ❌ Putting `Gtilt` and `-(C_PI_post)` as Fcn blocks in Simulink (Fcn blocks can't hold transfer functions — caused linearize to fail)
- ❌ Wrong sign on first Sum block (was `++`, now fixed to `+-`)
- ❌ Tuning `wc_tilt` from 15 to 10 (no improvement — still saturates)
- ❌ Reducing push and startAngle to small values (1 N, 1°, 5°) — still saturates
- ❌ Waiting for Simulink variables to be defined late in script (fixed by placeholder values in STEP 4 before `linearize`)

---

## 11. Documentation Status

| File | Status |
|---|---|
| `REGBOT Balance Assignment.md` | Progress log up to Task 2 design (includes mermaid diagram of **current wrong** Simulink structure) |
| `PLAN.md` | 5-phase plan until deadline |
| `Report/sections/introduction.tex` | ✅ Written |
| `Report/sections/control-architecture.tex` | ✅ Written |
| `Report/sections/wheel-speed-controller.tex` | ✅ Written (Task 1 complete) |
| `Report/sections/balance-controller.tex` | Partially written (plant ID done, controller design TODO) |
| `Report/sections/velocity-controller.tex` | Stub |
| `Report/sections/position-controller.tex` | Stub |
| `Report/sections/conclusion.tex` | Stub |

---

## 12. Recommended Next Steps (Fresh Session)

### Priority 1 — Fix the Simulink Lead structure

Apply the fix from section 9:
1. Delete the second `Sum(++)` block after PI and its connection to `tdtilt` gain
2. Add a NEW `Sum(++)` block BEFORE the error sum
3. Route `pitch` and `tdtilt × gyro` into this new sum
4. Route its output into the second input of the error sum (where pitch was going directly before)

After the fix, re-run simulation with `startAngle = 5`, push = 0. Expected: pitch falls from ~5° to 0 in ~1.5 s without voltage saturation.

### Priority 2 — Verify gyro sign

While investigating, plot `pitch` and `gyro` on the same scope during a disturbance. When pitch rises, gyro should be positive. If not, negate `tdtilt` in the script.

### Priority 3 — If controller still doesn't work

Alternative implementation: replace the gyro-based Lead with a proper Transfer Fcn block using a small filter pole:
- Series Lead in the forward path: Num `[tdtilt 1]`, Den `[alpha*tdtilt 1]` with `alpha = 0.1`
- This implements $(\tau_d s + 1)/(0.1\tau_d s + 1)$ — a proper Lead with a noise filter
- Remove the gyro feedback path entirely

### Priority 4 — Once Simulink works

1. Fix the documentation (update the mermaid diagram in `REGBOT Balance Assignment.md` to show the correct gyro placement)
2. Record working simulation plots, commit to repos
3. Physical REGBOT test (Test 3a: `vel=0, bal=1, log=15 : time=10`)
4. Move to Task 3 (velocity outer loop)

---

## 13. Cheat Sheet — Starting a Fresh Session

Paste this into a new Claude Code chat:

```
Read C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1\Exercises\Work\regbot\HANDOFF.md
and then help me fix the Simulink Lead structure as described in section 9.
```

Or for a specific task:

```
Read C:\Users\Mads2\DTU\Obsidian\Courses\34722 Linear Control Design 1\Exercises\Work\regbot\HANDOFF.md
and then help me move to Task 3 (velocity outer loop).
```

---

*Document created: 2026-04-15*
*Status: Task 2 balance controller designed in MATLAB, Simulink implementation debugging ongoing.*
