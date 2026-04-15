---
course: "34722"
course-name: "Linear Control Design 1"
type: assignment
tags: [LCD, assignment, REGBOT, balance, final]
date: 2026-04-15
---
# REGBOT Balance Assignment

> [!abstract] Goal
> Design, implement and test a control strategy for the REGBOT such that we achieve motion while keeping balance.

> [!example] Related Materials
> - [[Lecture_10_Unstable_systems.pdf|Lecture 10 Slides]]
> - [[Fundamentals - Intuitive Control Theory|Fundamentals Guide]]
> - [[Diagnostic Guide - What Went Wrong|Diagnostic Guide]]
> - [[Worked Example - REGBOT Position Controller|Worked Example]]
> - [[Day 5 - Black Box Modeling]] — voltage-to-velocity transfer function
> - [[Day 8 & 9 - Position Controller Design]] — prior PILead design

---

## Preparation

Before you start designing:

- [ ] Watch `REGBOT balance introduction.mp4` (Resources/Videos and Tutorials)
- [ ] Review the **REGBOT control architecture** slides (included in Lecture 10 slides)
- [ ] Download starter files from Resources/REGBOT balance resources:
    - `regbot_1mg` — REGBOT system with wheel velocity control loop
    - `regbot_mg` — associated model file
- [ ] Calibrate the **gyro** and **tilt-offset** before testing on the robot
- [ ] Install MATLAB packages (from **Add-Ons** in the Home tab):
    - **Simscape Multibody** (required to simulate the model)
    - **Simulink Control Design**

> [!warning] Before Testing on REGBOT
> Implement all controllers (designed in MATLAB) in the **Simulink model** first. Only test on the physical REGBOT after simulation confirms the design works.

---

## Control Architecture Overview

The REGBOT balance problem requires a **cascaded control** structure with multiple nested loops:

```
Position ref ──► [Position Ctrl] ──► Velocity ref ──► [Velocity Ctrl] ──► Balance ref
                                                                               │
                                                                               ▼
                                                       [Balance Ctrl] ──► Voltage ──► REGBOT
```

Each task in this assignment builds the next inner/outer loop in this cascade.

---

## Tasks

### Task 1 — Wheel Speed Controller (PI)

**Design a PI-controller** for the wheel velocity loop.

- **Transfer function to control:** voltage-to-velocity $G_{vel}(s)$ identified on [[Day 5 - Black Box Modeling|Day 5]]
- **Controller type:** PI
- **Source:** your own design from previous exercises

---

### Task 2 — Balance Controller (PI + Post-Integrator)

**Design a balance controller** so the REGBOT can balance itself and maintain balance during a mission.

> [!important] Post-Integrator
> Include a **"post-integrator"** — a second PI block in the open loop.
> - Treat it as an **additional design element** when computing controller phase and $K_P$
> - Its phase contribution must be added when calculating the total open-loop phase
> - Its gain must be accounted for when solving $|L(j\omega_c)| = 1$
>
> See Lecture 10 slides for details on the post-integrator design.

**Design checklist:**
- [ ] Identify the balance transfer function (angle-to-tilt or similar unstable plant)
- [ ] Include post-integrator in the open loop
- [ ] Compute phase contribution from all elements
- [ ] Calculate $K_P$ such that $|L(j\omega_c)| = 1$
- [ ] Verify stability via Nyquist (REGBOT balance is open-loop unstable!)

---

### Task 3 — Velocity Controller (in Balance State)

**Design a velocity controller** so the REGBOT can move at a given speed forwards/backwards while balancing.

#### Test 3a — Zero velocity (stationary balance)

**Expected:** REGBOT balances in place. Some small movement is acceptable, e.g. drift within approximately **0.5 m** from the starting point.

#### Test 3b — Square run at 0.8 m/s

**Expected:** REGBOT makes a **square run** while staying in balance:
- Side length: **1 m**
- Turning radius: **0.2 m**

---

### Task 4 — Position Controller (in Balance State)

**Design a position controller** for moving the REGBOT to a given position while balancing.

#### Test sequence

The REGBOT must execute:

| Step | State |
|------|-------|
| (a) | Robot stands still |
| (b) | Robot finds the balance |
| (c) | Robot moves a distance of **2 m** with max speed exceeding **0.7 m/s** |
| (d) | Robot stops |

#### Example mission script

```
vel=0, bal=1, log=15 : time=2
topos=2, vel=1.2 : time=10
```

Where:
- `topos=2` → target distance in meters
- `vel=1.2` → maximum speed during movement (m/s)
- `bal=1` → balance mode enabled
- `log=15` → logging level

---

## Mandatory Report — Hand-in Instructions

> [!tip] Submission Details
> - **Max length:** 5 pages
> - **Submit on:** Learn under *Course Content* → *Assignments* → *REGBOT balance*
> - **One submission per group** (only the most recent is kept)
> - **Filename format:** `Group_XX.pdf`
> - **Front page:** full names and student numbers

### Required Content

#### Front Matter
- [ ] Full names and student numbers

#### General Architecture
- [ ] A few lines on the overall control architecture used

#### For Each Design Step, Document:
- [ ] Which transfer function is being controlled
- [ ] Which controllers are in the open loop, and **why**
- [ ] Design parameters and how they were found:
    - $N_i$
    - $\alpha$
    - $\tau_d$
    - $\tau_i$
    - $K_P$
    - $\gamma_M$
    - $\omega_c$
- [ ] **Bode plot** of the open-loop transfer function (showing phase margin)
- [ ] **Step response** of the closed-loop system from Simulink
- [ ] **Step response** from the REGBOT (include the mission script used)
- [ ] **Comments** comparing simulation vs. experiment

#### Extras
- [ ] General comments on findings and methods
- [ ] A cool **XY-plane plot** showing REGBOT motion during Task 4
- [ ] (Optional) Video link to controller tests

> [!important] Style
> Be **precise, accurate, and short**.

---

## Design Workflow Checklist

Follow this order to systematically work through the assignment:

1. **Preparation** — watch intro video, calibrate REGBOT, install MATLAB packages
2. **Task 1** — PI velocity controller (reuse from earlier)
3. **Simulink model** — verify velocity controller works in sim
4. **Task 2** — Balance controller with post-integrator
5. **Simulink** — confirm balance loop closes (REGBOT stays upright in sim)
6. **Physical test** — balance at zero velocity (Test 3a)
7. **Task 3** — Outer velocity controller
8. **Physical test** — square run (Test 3b)
9. **Task 4** — Position controller
10. **Physical test** — 2 m position move (Test 4)
11. **Report** — compile Bode plots, step responses, XY-plot, mission scripts

---

## Key Design Principles (from Course)

> [!tip] Reminders from Fundamentals
> - The balance plant is **open-loop unstable** → Nyquist stability criterion requires **CCW encirclement** of $-1$ per RHP pole (see [[Fundamentals - Intuitive Control Theory#9. The Nyquist Plot Another Stability View|Fundamentals, Section 9]])
> - For zero steady-state error to a **step** reference, you need **at least one integrator** in the loop (see [[Fundamentals - Intuitive Control Theory#11. Type-n Systems and Steady-State Error|Type-n systems]])
> - The post-integrator makes the loop Type-2 → zero error for both step and ramp references
> - Phase margin target: typically $\gamma_M = 50°$–$65°$ for balance between speed and overshoot

---

*Last updated: 2026-04-15*
