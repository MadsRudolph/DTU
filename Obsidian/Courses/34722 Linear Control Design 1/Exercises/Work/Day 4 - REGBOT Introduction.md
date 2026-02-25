---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise]
date: 2026-02-25
---
# Day 4 - REGBOT Introduction

> [!abstract] Exercise Overview
> First hands-on session with the REGBOT robot. Design a driving mission with multiple speeds and turns, log data via the REGBOT GUI, and analyze motor performance in MATLAB.

> [!info] Files
> - REGBOT GUI setup: [[Regbot GUI]]
> - REGBOT Wiki: [rsewiki.electro.dtu.dk](https://rsewiki.electro.dtu.dk/index.php?title=Regbot_GUI)
> - Mission syntax: [Mission Wiki](https://rsewiki.electro.dtu.dk/index.php?title=Mission)
> - MATLAB script: [Day4_REGBOT_Analysis.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day4/Day4_REGBOT_Analysis.m)

> [!example] Related Materials
> - Lecture notes: [[Lesson 4 - Frequency Domain and Time Analysis]]
> - Slides: [[4_Frequency_and_Time_Analysis_NoSol.pdf]]
> - Previous exercise: [[Day 3 - Block Diagram Exercise]]

---

## Requirements

Design a driving mission for the REGBOT that includes:
- At least **2 different speed values**
- At least **2 turns**

For example: drive at $X$ m/s, turn left by $Y$ rad, drive at $Z$ m/s, turn right, etc.

**Deliverables:**
1. Discuss with group mates how to solve the task
2. Make plots of the robot mission (speed, motor voltage, motor current) to show performance

---

## Setup

> [!warning] Prerequisites
> - Battery must be **fully charged**
> - Launch REGBOT GUI from the **terminal** (not by double-clicking the file)
> - See [[Regbot GUI]] for installation and connection guide

### Controller Settings

| Parameter | Value | Reason |
|-----------|-------|--------|
| $K_p$ | 0 | No proportional feedback — open-loop voltage control |
| $K_{ff}$ | 1 | Feedforward gain = 1, so commanded value goes directly to motor |
| Velocity controller | **Enabled** | |
| Heading controller | **Disabled** | |

> [!important] Motor Nonlinearity
> The motor does not run at voltages below ~1 V (dead zone). Always keep the motor voltage in the range **1–6 V** with some margin. Use step inputs within this range, e.g. from 3 V to 4 V.

---

## Mission Syntax Reference

Each mission line has the format: `drive parameters : continue conditions`

Conditions are OR'ed — the line ends when **any** condition is met.

### Drive Parameters (left of `:`)

| Command | Unit | Description |
|---------|------|-------------|
| `vel` | m/s | Velocity (positive = forward). With $K_p=0$, $K_{ff}=1$ this maps to voltage |
| `acc` | m/s² | Acceleration limit |
| `tr` | m | Turn radius (`0` = turn in place) |
| `head` | deg | Reference heading (needs heading controller) |
| `log` | ms | Start logging at this interval |
| `topos` | m | Target position (uses max velocity) |

### Continue Conditions (right of `:`)

| Condition | Unit | Description |
|-----------|------|-------------|
| `dist` | m | Distance driven in this line |
| `turn` | deg | Angle turned (positive = left/CCW) |
| `time` | s | Maximum time in this line |
| `log` | — | True when log buffer is full (use `log=0`) |
| `head` | deg | Heading angle test |
| `ir1`, `ir2` | m | IR sensor distance |

Comparison operators: **=** (equal/greater), **\<** (less than), **\>** (greater than)

### Log Interval

| Log interval | Approximate log duration |
|---|---|
| 10 ms | ~5 seconds |
| 4 ms | ~2 seconds |

> [!tip]
> Driving on the floor probably requires a shorter sampling time (e.g. `log = 4 ms`) and plenty of space.

---

## Missions

### Mission 1: Step Response (System Identification)

For estimating the motor transfer function. Uses $K_p = 0$, $K_{ff} = 1$, heading controller **disabled**.

```
vel=3, log=4 : time=1
vel=4 : log=0
```

| Line | What happens |
|------|-------------|
| 1 | Drive at 3 V for 1 second (let motor reach steady state), start logging at 4 ms |
| 2 | Step to 4 V, run until log buffer is full |

This gives a clean 3 V → 4 V step response to extract $K_{ss}$, $\tau$, and $\omega_b$.

### Mission 2: Driving Mission (2 Speeds + 2 Turns)

For the deliverable. Uses $K_p = 0$, $K_{ff} = 1$ (open-loop voltage control).

```
vel=3, acc=1.5, log=10 : dist=1.0, time=5
vel=2, tr=0 : turn=-90, time=5
vel=4 : dist=0.5, time=5
vel=2, tr=0 : turn=90, time=5
vel=0 : time=0.5, log=0
```

| Line | Action | Exit when |
|------|--------|-----------|
| 1 | Forward at 3 V, start logging 10 ms | 1.0 m driven or 5 s |
| 2 | Spin right 90° at 2 V | 90° turned or 5 s |
| 3 | Forward at 4 V (speed 2) | 0.5 m driven or 5 s |
| 4 | Spin left 90° at 2 V | 90° turned or 5 s |
| 5 | Stop, end logging | 0.5 s or log full |

---

## MATLAB Data Analysis

### Loading the Log File

```matlab
data = readtable('log_velocity_4_volts.txt');
data = fillmissing(data, 'nearest');
```

### Assigning Variables

```matlab
t   = table2array(data(:,1));    % time stamps
u_L = table2array(data(:,8));    % left motor voltage
u_R = table2array(data(:,9));    % right motor voltage
v_L = table2array(data(:,10));   % left motor velocity
v_R = table2array(data(:,11));   % right motor velocity
T_s = t(2) - t(1);              % sampling time
```

### Trimming Data

We only want the data from the voltage step onward (e.g. the transition from 3 V to 4 V). Trim everything before the step:

```matlab
idx = find(X >= 3, 1, 'first');  % index where X first reaches 3
X = X(idx:end);                  % keep only data after the step
t = t(idx:end);
t = t - t(1);                   % offset time to start from 0
```

> [!warning] Outlier Removal
> Check for outliers (spikes) in the data. Spot them by:
> - Plotting the data and looking for sudden spikes
> - Inspecting the raw log file directly
>
> Remove them before further analysis (the MATLAB script uses `medfilt1` for this).

---

## Results

### Raw Log Data

Motor voltage and velocity as recorded from the REGBOT, before any processing.

![[day4_raw_data.png]]

### Trimmed Step Response

Data trimmed to the step region (3 V → 4 V) with outliers removed.

![[day4_trimmed_step.png]]

### 1st Order Model Fit

Estimated transfer function parameters from the 63.2% rule (3 V → 4 V step, $\Delta u = 0.84$ V):

$$G(s) = K_{ss} \frac{\omega_b}{s + \omega_b} = \frac{K_{ss}}{\tau s + 1}$$

| Parameter | Symbol | Value |
|-----------|--------|-------|
| DC gain | $K_{ss}$ | 0.373 (m/s)/V |
| Time constant | $\tau$ | 0.028 s |
| Break frequency | $\omega_b = 1/\tau$ | 35.71 rad/s |
| Pre-step velocity | $v_0$ | 0.684 m/s |
| Steady-state velocity | $v_{ss}$ | 0.998 m/s |

$$\boxed{G(s) = \frac{13.34}{s + 35.71} = \frac{0.373}{0.028s + 1}}$$

The green dot marks the 63.2% point used to estimate $\tau$.

![[day4_model_vs_measured.png]]

### Transfer Function Analysis

Step response, impulse response, and Bode plot of the estimated $G(s)$.

![[day4_tf_analysis.png]]

### Mission Performance

Full driving mission with 2 speeds (3 V and 4 V) and 2 turns (right 90°, left 90°). Bottom plot shows differential velocity ($v_L - v_R$) as a turning indicator.

![[day4_mission.png]]

The five mission phases are clearly identifiable:

| Time | Phase | Observation |
|------|-------|-------------|
| 0–1 s | Forward at 3 V | Voltage ramps up smoothly due to `acc=1.5` limit |
| ~1–2 s | Spin right 90° | Left/right voltages diverge (opposite for in-place turn) |
| ~2–3.5 s | Forward at 4 V | Both motors at higher voltage, velocity increases |
| ~3.5–4.5 s | Spin left 90° | Voltages diverge again, differential velocity flips sign |
| ~5 s | Stop | Both motors drop to 0 V |

> [!note] Startup transient
> A brief voltage spike (~5 V) occurs at $t = 0$ on one motor — this is a hardware artifact also seen in the step response and does not affect the mission.

---

## Key Observations

> [!success] Summary
> - The **1st order model** fits the step response well ($K_{ss} = 0.373$ (m/s)/V, $\tau = 0.028$ s)
> - Left and right wheels show **slight asymmetry** but track closely
> - The **two speed levels** (3 V → 4 V) are clearly visible in both voltage and velocity plots
> - The **two turns** are identifiable from voltage divergence between left/right motors and from the differential velocity plot
> - A brief **startup voltage spike** is present at $t = 0$ in both missions — this is a hardware transient

---

> [!nav]
> [[Day 3 - Block Diagram Exercise|← Day 3]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
