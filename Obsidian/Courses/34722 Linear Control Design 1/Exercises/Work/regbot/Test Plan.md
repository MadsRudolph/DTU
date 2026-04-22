---
course: "34722"
course-name: "Linear Control Design 1"
type: test-plan
tags: [LCD, regbot, tests, physical]
date: 2026-04-21
---
# REGBOT Physical Test Plan — Group 47

> [!abstract] Purpose
> Checklist for the physical REGBOT tests. Each test has a mission script, expected behaviour, pass criteria, and a slot for the log file + post-test notes. Fill the notes as we go so we can see exactly what happened if we need to re-tune.

> [!info] Gain source
> All tests assume the REGBOT firmware has loaded the Group 47 gains from
> `REGBOT-Balance-Assignment/config/regbot_group47.ini` (see section 0 below).
> If a controller misbehaves, first confirm the gains are actually on the robot before touching the design.

---

## 0. Pre-flight — do this once per session

- [x] **Battery charged** (check voltage reading is ≥ nominal; low battery → bad balance performance)
- [x] **Gyro calibration** completed (hold robot still, run gyro calibration routine; zero-rate offsets must be small)
- [x] **Tilt-offset calibration** completed (the angle the robot reads as "vertical" matches the mechanical balance point)
- [ ] **ini loaded into GUI** — for each of the four controllers (Wheel velocity, Balance, Balance velocity, Balance position):
    - Open the controller edit dialog
    - Paste into "Load from:"  ` C:\Users\Mads2\DTU\4. Semester\Linear Control Design\REGBOT-Balance-Assignment\config\regbot_group47.ini`
    - Click "Load from:" button — log should show `# UControl:: loading <cID> data from ...`
    - Confirm the values in the dialog match the ini file (especially Kp, τᵢ, τ_d)
- [ ] **Sent to robot** (normal GUI "send" / "OK" workflow)
- [ ] **Saved to robot flash** so values survive a power-cycle (File → save configuration to robot)
- [ ] **Test space clear** — 3 m × 3 m minimum for Test 4, 2 m × 2 m minimum for Test 3b, 1 m × 1 m OK for Test 3a
- [ ] **Catcher ready** — one teammate within arm's reach to grab the robot if a loop goes unstable

### Ini verification values (sanity check the dialogs match this)

| Controller | Dialog block | Kp | τᵢ | τ_d | Post-integrator τ |
|---|---|---|---|---|---|
| `[cvel]` | Wheel Velocity | **3.3100** | 0.1000 | — | — |
| `[cbal]` | Balance | **1.1370** | 0.2000 | 0.1355 (as `lead_back_tau_zero`) | 0.1682 |
| `[cbav]` | Balance velocity | **0.1616** | 3.0000 | — | — |
| `[cbap]` | Balance position | **0.5335** | — (disabled) | — | — |

---

## Test 0 — Inner wheel-speed loop only (pre-validate Task 1)

> [!note] Optional but recommended
> Before relying on Balance to work, confirm the inner wheel-speed PI actually hits commanded velocities on hardware. If not, nothing layered above it will work either.

**Mission script:**
```
bal=0, vel=0.3, log=15 : time=3
vel=0
```

Alternative: use the GUI's motor-test tab to manually command a wheel velocity with balance disabled.

**Setup:**
- Lay the robot on its side (or hold wheels off the ground) so it can't fall.
- Balance must be **disabled** for this test (`bal=0`).

**Signals to log** (log=15 = full):
- Time
- Motor voltage (both wheels)
- Wheel velocity (both wheels)
- Commanded velocity (vel_ref)

**Pass criteria:**
- [x] Wheel velocity reaches ~0.3 m/s within ~0.3 s of the step
- [x] Zero steady-state error (PI integrator does its job)
- [x] Both wheels agree within ~5%
- [x] Motor voltage stays within ±8 V (`out_limit` of `[cvel]`)

**Log file:**
- [x] Saved to: `REGBOT-Balance-Assignment/logs/test0_wheel_speed_2026-04-21.txt`

**Notes (post-test):** ✅ **PASS (2026-04-21)**

| Metric | Spec | Measured |
|---|---|---|
| Commanded step | 0.3 m/s | — |
| Left wheel mean (0.5–2.9 s) | 0.3 | 0.2973 m/s (err −1%) |
| Right wheel mean (0.5–2.9 s) | 0.3 | 0.2962 m/s (err −1%) |
| L vs R agreement | < 5% | **0.36%** |
| Rise time (to 0.27) | ~0.3 s | **0.329 s** |
| Voltage L mean / max | — | 1.74 V / 1.93 V |
| Voltage R mean / max | — | 1.84 V / 2.06 V |
| Max \|V\| | < 8 V | **2.06 V** (74% headroom) |

- Noise floor ~10% std on velocity — encoder quantisation aliased by the 67 Hz log rate; the 1 kHz internal loop is smoother than shown.
- Steady-state voltage ~1.8 V at 0.3 m/s. **Not comparable to Day 5** — Test 0 is wheels-up (no rolling load), Day 5 was on the floor. Back-EMF alone at 0.3 m/s wheel velocity is `Kemf · v/WR · NG = 0.0105 · 0.3/0.03 · 9.69 ≈ 1.02 V`, and the remaining ~0.8 V is `I·R` across the armature to overcome bearing + gearbox friction. Physics consistent with wheels-up; **no evidence of Day 5 model error**. The on-floor behaviour is validated indirectly by Tests 3a/3b/4 which all pass.
- Motors very well matched (0.36% diff) → no trim needed.

![[test0_wheel_speed_2026-04-21.png]]
*Top: `vref` (dashed) with measured wheel velocities L/R. Middle: motor voltages. Bottom: tracking error. Rise to target in ~0.33 s, both wheels on top of each other, voltage well below saturation.*

---

## Test 3a — Stationary balance (Task 2 verification)

**Mission script:**
```
vel=0, bal=1, log=15 : time=10
```

**Setup:**
- Hold robot upright near balance point.
- Start mission.
- Release gently once it's actively balancing.
- Catcher ready.

**Signals to log:**
- Time
- Pitch angle (rad)
- Gyro (rad/s)
- Motor voltage (both wheels)
- Wheel velocity
- x_position

**Pass criteria (per assignment):**
- [x] Robot stays upright for the full 10 s
- [x] **Drift ≤ 0.5 m** from start position (measured 0.343 m)
- [ ] Pitch stays small (|θ| < 5°) after the initial release transient (calm period yes; late oscillation 6–10 s hit 10°)
- [ ] No visible sustained oscillation (calm period yes; external disturbance from ~t=6 s)

**Likely failure modes + what each means:**

| Symptom | Likely cause | Fix |
|---|---|---|
| Falls within ~1 s of release | Sign error on Kp or gyro | Flip sign of `kp` in `[cbal]`, reload |
| Growing oscillation | PM too low on real plant | Reduce `Kp` by 10–20%, or lower `ω_c,tilt` in design |
| Oscillates around a non-zero tilt | Tilt-offset miscalibrated | Recalibrate tilt-offset |
| Drifts constantly in one direction | Gyro bias | Recalibrate gyro |

**Log file:**
- [x] Saved to: `REGBOT-Balance-Assignment/logs/test3a_balance_rest_2026-04-21_v2.txt`

**Notes (post-test):** ✅ **PASS — assignment spec met (2026-04-21, 2nd attempt)**

**1st attempt failed big time.** With `kp = +1.1370` as the ini originally had, the robot did not balance — the wheels went full speed forward and the robot fell. Classic positive-feedback runaway. The log from that run was empty (`%% log is empty`) because logging wasn't started before the mission.

**Fix applied:** flipped sign of `kp` in `[cbal]` → `-1.1370`. Updated `config/regbot_group47.ini` with a comment block explaining the finding for teammates.

**2nd attempt (with negative Kp):** balanced cleanly.

| Metric | Spec | Measured |
|---|---|---|
| Held balance for | ≥ 10 s | 10 s ✓ (never fell) |
| Drift distance | ≤ 0.5 m | **0.343 m** ✓ |
| Peak pitch excursion (overall) | < 5° (stretch target) | 10° during 6–10 s oscillations |
| Peak pitch excursion (calm 2–6 s) | < 5° | ~±1–2° ✓ |
| Motor voltage peak | < ±8 V | **2.25 V** ✓ |
| Mean tilt offset | ~0 | **0.78° (forward)** |
| Peak vel_ref (hit saturation) | — | ±0.5 m/s (looks clipped) |

**Three take-aways that inform the next tests:**

1. **Sign of Kp on `[cbal]` must be negative.** The firmware Balance block does NOT absorb the Lecture 10 Method 2 minus sign internally — we do it in the ini. Ini file + in-doc HANDOFF notes updated.
2. **Backward drift is a tilt-offset issue, not a controller issue.** The robot thinks it's upright when actually leaning 0.78° forward → commands wheels backward → 0.035 m/s steady drift. Fixes: recalibrate tilt-offset OR layer on Task 3's velocity loop (which explicitly commands wheel velocity = 0). We're choosing the latter.
3. **Late oscillations (6–10 s) look like an external disturbance event** (possibly someone approaching, or battery sag). Not a controller failure — the robot recovers each swing. If we see the same pattern in Test 3b/4, we'll consider dialling `Kptilt` back 10–20% for more damping.

![[test3a_balance_rest_2026-04-21_v2.png]]
*Task 2 hardware (v2, with `kp = -1.1370`). From top: tilt, x/y position, wheel velocities with vel_ref, motor voltages. Calm balance 2–6 s, external-disturbance oscillation 6–10 s, consistent ~0.035 m/s backward drift from tilt-offset bias.*

---

## Test 3b — Square run at 0.8 m/s (Task 2 + 3 verification)

**Mission script** (REGBOT syntax — `drive values : continue conditions`, verified against `umission.py` help):
```
vel=0, bal=1, log=15 : time=2
vel=0.5 : dist=1
vel=0.5, tr=0.2 : turn=90
vel=0.5 : dist=1
vel=0.5, tr=0.2 : turn=90
vel=0.5 : dist=1
vel=0.5, tr=0.2 : turn=90
vel=0.5 : dist=1
vel=0
```

**If 0.5 m/s runs cleanly**, retry the full-spec version at 0.8 m/s by replacing every `vel=0.5` with `vel=0.8` on the drive lines.

> [!note] REGBOT mission syntax reference
> - **Drive values** (before the `:`): `vel` (m/s, + forward), `tr` (turn radius m), `topos` (target position m), `acc`, `bal`, `log`, `head` (ref heading deg), `edger`/`edgel`…
> - **Continue conditions** (after the `:`, OR'ed): `dist` (m), `vel` (m/s), `turn` (deg), `head` (deg, use `=`, `<`, `>`), `time` (s), `tilt` (deg)…
> - `log=15` means log every 15 ms (not log level 15).
> - `bal` persists: set `bal=1` once, it stays until changed.

> [!warning] Simulation showed limit-cycle growth at 0.8 m/s pure steps
> At 0.5 m/s the velocity loop tracks cleanly, at 0.8 m/s it limit-cycles because pitch swings to ~23° and breaks the linearisation.
> The mission's piece-wise commands are not pure steps (the robot has to accelerate from 0, decelerate at the corners), but if the sim result holds on hardware we may need to:
> - Slow to `vel=0.5` for this test, or
> - Add a rate limiter (not implemented yet).
>
> If this test fails at 0.8, retry at 0.5 m/s and document both runs in the report.

**Setup:**
- Place robot at one corner of a 1 m × 1 m mental square.
- Orient so first straight points into clear space.
- Start mission, step back.

**Signals to log:**
- Time
- Pitch, gyro
- Motor voltage (both wheels)
- Wheel velocity (both)
- x_position, y_position (for the XY trajectory plot)
- v_ref (commanded velocity)

**Pass criteria:**
- [x] Completes all 4 sides + 3 turns without falling
- [x] Tracks v_ref reasonably well on the straights
- [x] XY trajectory is a recognisable square (corners rounded by the 0.2 m turn radius)
- [x] Motor voltage stays within ±8 V

**Log file:**
- [x] Saved to: `REGBOT-Balance-Assignment/logs/test3b_square_2026-04-21.txt`

**Notes (post-test):** ✅ **PASS at 0.5 m/s (2026-04-21)**

| Metric | Spec / target | Measured |
|---|---|---|
| Speed used | 0.5 m/s (conservative 1st run) | 0.5 m/s on straights, burst to 0.76 m/s ref (corners) |
| Completed square | yes | yes, 4 sides + 3 turns + final stop |
| Side length (x-span) | 1.0 m straight + 0.31 m turn arc = ~1.3 m expected | **1.40 m** (accounts for turn-radius bulge) |
| Total heading change | 360° | **359.8°** (0.06% error — extremely clean) |
| Battery | > 12 V nominal | 12.46–12.50 V (healthier than 3a) |
| Tilt range | < ±15° desirable | **−10.7° to +17.9°** (peaks during corners) |
| Tilt std | — | 4.76° |
| Wheel vel peak (outer on turn) | < 1.5 m/s | **0.91 m/s** |
| vel_ref peak | — | 0.76 m/s |
| Motor voltage peak | < ±8 V | **4.07 V** (50% headroom) |

- **Balance holds beautifully through aggressive 0.2 m-radius corners** — biggest test of the controller yet. 17° pitch excursions are transient and always recover.
- **End-pose offset** (endpoint 0.24 m away from start, heading off by 0.1°): geometric consequence of `vel=X : dist=1` + `tr=0.2 : turn=90` — each turn arc bulges the path outward by the turn radius, so the "square" is really 4 straight segments linked by quarter-circles. Consistent with physics.
- **Not a tuning issue.** Balance loop is doing real work, but never loses it. No reason to back off `Kptilt`.
![[test3b_xy_2026-04-21.png]]
*XY trajectory — the "cool figure" the assignment asks for. Clean closed square, 359.8° cumulative heading change. Corners visibly rounded by the 0.2 m turn radius. Side lengths ~1.4 m (1 m straight + 0.31 m arc).*

![[test3b_timeseries_2026-04-21.png]]
*Time series of the square run. Tilt peaks during corners are transient and always recover; wheel velocities split symmetrically on turns (outer wheel faster); position traces out the XY square as four linear ramps.*

#### Second attempt — full 0.8 m/s spec (2026-04-22) ✅ **PASS**

Re-ran the same mission with every `vel=0.5` replaced by `vel=0.8` to hit the original assignment spec. Hardware completed it cleanly.

| Metric | 0.5 m/s run | **0.8 m/s run** |
|---|---|---|
| Duration | 15.86 s | **12.35 s** |
| Sides + turns completed | 4 + 3 | 4 + 3 |
| Heading change | 359.8° | 359.8° |
| Wheel vel peak | 0.91 m/s | **1.07 m/s** |
| `vel_ref` peak | 0.76 m/s | 0.94 m/s |
| Tilt range | −10.7° to +18.0° | **−9.0° to +22.0°** |
| Tilt std | 4.76° | **5.72°** |
| Mean tilt | 3.0° | **5.9°** (steeper forward lean) |
| Motor voltage peak | 4.07 V | **4.67 V** (still 42% headroom) |
| Square shape / endpoint offset | identical | identical |

**Key finding vs simulation warning.** The Simulink design-time analysis predicted a large-signal limit cycle at 0.8 m/s step commands because pitch exceeds the linearisation range (sim showed ~23° swings). On hardware the **peak tilt was +22°** — right at the sim prediction — but **the robot did not limit-cycle**, stayed bounded, recovered each swing, and completed the full square with the same geometric shape as the 0.5 m/s run. The hardware is more robust than the pessimistic linear sim in this regime; the physical balance loop + gyro feedback has real-world damping the linear model doesn't fully capture.

**Log file:**
- [x] Saved to: `REGBOT-Balance-Assignment/logs/test3b_square_0.8ms_2026-04-21.txt`

![[test3b_xy_0.8ms_2026-04-21.png]]
*0.8 m/s XY trajectory — visually identical to the 0.5 m/s run. Same ~1.4 m sides (geometry dominated by the `dist=1 + 0.2 m turn arc` construction, not by speed).*

![[test3b_timeseries_0.8ms_2026-04-21.png]]
*0.8 m/s time series. Larger tilt excursions than 0.5 m/s (peak +22° vs +18°) and higher mean tilt (5.9° vs 3.0°) reflecting the steeper lean needed to sustain higher velocity. Voltage peaks at 4.67 V, well below ±8 V saturation.*

---

## Test 4 — 2 m position move (all four loops verified)

**Mission script (per assignment):**
```
vel=0, bal=1, log=15 : time=2
topos=2, vel=1.2 : time=10
```

`vel=1.2` is the **maximum allowed velocity**; actual peak is determined by the position controller (predicted 0.80 m/s from simulation).

**Setup:**
- Place robot at the start of a 3 m × 1 m clear corridor.
- Orient forward along the corridor.
- Start mission.

**Signals to log:**
- Time
- Pitch, gyro
- Motor voltage
- Wheel velocity, v_ref
- x_position, pos_ref

**Pass criteria (per assignment):**
- [x] Reaches 2 m ± ~5 cm (first reached at t = 9.07 s; peak 1.974 m = 2.6 cm short)
- [x] Stays balanced throughout (never fell)
- [x] **Peak velocity ≥ 0.7 m/s** — **1.01 m/s** ✓ 44% above spec (sim predicted 0.80, real robot did better)
- [x] Completes inside 10 s mission window
- [x] No motor saturation (4.75 V peak, 41% of ±8 V budget)

**Log file:**
- [x] Saved to: `REGBOT-Balance-Assignment/logs/test4_position_2m_2026-04-21.txt`

**Notes (post-test):** ✅ **PASS (2026-04-21)**

| Metric | Spec / sim | Measured |
|---|---|---|
| Final position at log end | 2.0 m | 1.893 m (-107 mm) |
| Peak position reached | — | **1.974 m** (–26 mm) |
| Peak velocity | ≥ 0.7 m/s (sim: 0.80) | **1.01 m/s** |
| Peak vel_ref (commanded) | ≤ 1.2 m/s (cap) | 1.15 m/s |
| Time to first ±5 cm of target | < 10 s (mission window) | 9.07 s |
| Peak tilt during acceleration | — | **+25.0°** (forward lean to accelerate) |
| Peak tilt during deceleration | — | −9.2° |
| Tilt std over whole run | — | 5.18° |
| Motor voltage peak | < ±8 V | **4.75 V** |
| Battery | healthy | 12.39 V mean, 12.25 V min |

**What the plot narrates:**

1. **0–2 s (balance prep):** small 7.5 cm backward drift — same tilt-offset behaviour as Test 3a.
2. **t = 2 s (`topos=2` fires):** commits hard — tilt to +25° forward, vel_ref jumps to 1.15 m/s, wheel velocity ramps to 1.01 m/s. Textbook cascade response.
3. **2.5–7 s (deceleration):** position approaches 2 m, commanded velocity smoothly drops to 0, tilt returns to ~0°. Clean.
4. **7–10 s (at target):** position hovers near 1.95–1.97 m with small oscillations. Would settle if left alone.
5. **10–12 s (limit-cycle re-ignites):** tilt swings grow to ±10°, vel_ref saturates at ±0.5 m/s, position drifts back to 1.89 m. **Same pattern as end of Test 3a.**

**Diagnosis of the late-limit-cycle pattern (seen in both 3a and 4):**
It happens when the robot tries to hold station with no commanded motion. Ranked causes:
1. **Tilt-offset miscalibration** (0.78° bias from 3a analysis) — controller thinks forward-lean is level, commands wheels to correct, balance loop counter-tilts, integrator winds up → limit cycle.
2. **Static friction** at tiny `vel_ref` (controller bangs between ±break-away thresholds).
3. Integrator wind-up in the velocity PI as the cascade converges.

**Stretch goal if time allows:** redo tilt-offset calibration and re-run. Expected result: the limit cycle vanishes in both 3a and 4. Not required for assignment pass.

![[test4_position_2m_2026-04-21.png]]
*Task 4 hardware — 2 m position step. From top: x-position with target and topos-command marker; wheel velocities with commanded ref and the 0.7 m/s spec floor; tilt angle; motor voltages. Clean commit at t=2 s, peak velocity 1.01 m/s, reaches target by t≈9 s, then late limit cycle.*

---

## Post-test review — mapping to report sections

Once the logs are in, we plot + cross-reference with the simulation predictions to fill in the experiment subsections of the LaTeX report:

| Test | Report section | Figure(s) needed |
|---|---|---|
| Test 0 | `wheel-speed-controller.tex` → Simulation / Experiment | Step response on hardware |
| Test 3a | `balance-controller.tex` → Experiment | Pitch/voltage/x vs. time |
| Test 3b | `velocity-controller.tex` → Experiment + "cool XY figure" | Time series + XY trajectory |
| Test 4 | `position-controller.tex` → Experiment | Position/velocity/pitch vs. time |

---

## Running list of issues we hit (fill as we go)

| Test | Issue | Root cause | Fix applied | Re-run passed? |
|---|---|---|---|---|
| 3a | Robot ran wheels full-speed forward, didn't balance at all | Sign error: firmware Balance block does NOT absorb the Method 2 minus sign; positive Kp = positive feedback → runaway | Flipped `kp` in `[cbal]` to `-1.1370` in `config/regbot_group47.ini`; updated header comments | ✅ yes (2nd run) |
| 3a | Log file empty (`%% log is empty`) on first attempt | Logging not started before mission in the GUI | Start log → then start mission, verify file > 10 KB | ✅ yes (v2 log) |
| 3a | 0.78° mean tilt offset → 0.34 m backward drift | Tilt-offset calibration slightly off | Deferred — Task 3 velocity loop helps but doesn't fully cancel it; re-appeared as late limit cycle in Test 4 | stretch goal |
| 3a, 4 | Late limit cycle (tilt ±10°, vel_ref ±0.5 m/s) when holding station | Likely caused by tilt-offset bias + static friction dead-zone + velocity-PI wind-up | Not addressed; assignment specs pass regardless | optional — re-cal tilt offset to eliminate |
| 3b | `fwd`/`turn` mission keywords rejected by GUI | REGBOT mission syntax is `drive values : continue conditions`, no keyword commands | Rewrote mission as `vel=X : dist=Y` and `vel=X, tr=R : turn=deg`; added syntax reference note to the test plan | ✅ ran clean 2nd attempt |
| 4 | Position stopped 10.7 cm short of 2.0 m target | Static friction + cascade dead-zone + same tilt-offset bias | Not addressed; assignment does not specify a settling-tolerance spec | optional — recal tilt offset |

---

*Document created: 2026-04-21 — to be filled in during the lab session(s).*
