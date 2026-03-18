---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise]
date: 2026-03-04
---
# Day 5 - Black Box Modeling for REGBOT

> [!abstract] Exercise Overview
> Find the transfer function from motor voltage to robot speed using MATLAB's System Identification toolbox (`tfest`). Identify models for wheels-up and on-the-floor driving, then compare estimated transfer functions against measured data.

> [!info] Files
> - REGBOT GUI setup: [[Regbot GUI]]
> - MATLAB script: [Day5.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day5/Day5.m)
> - Given examples: [sysID_Example_1.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day5/Given_Files/sysID_Example_1.m), [sysID_Example_2.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day5/Given_Files/sysID_Example_2.m)

> [!example] Related Materials
> - Previous exercise: [[Day 4 - REGBOT Introduction]]

---

## Requirements

Find the transfer function from motor voltage to robot speed (at normal speeds) when:
1. Driving with **wheels up** (not on the floor)
2. Driving **on the floor**

**Deliverables:**
- Evaluate the identified transfer functions against the measured data

---

## Setup

### Controller Settings

| Parameter | Value | Reason |
|-----------|-------|--------|
| $K_p$ | 0 | No proportional feedback |
| $K_{ff}$ | 1 | Feedforward gain = 1, commanded value goes directly to motor |
| Velocity controller | **Enabled** | |
| Heading controller | **Disabled** | |

> [!important] Motor Nonlinearity
> The motor does not run at voltages below ~1 V (dead zone). Always keep the motor voltage in the range **1–6 V** with some margin. Use step inputs within this range, e.g. from 3 V to 4 V.

> [!tip] Encoder Calibration
> The encoder calibration can provide better data and better estimation of the transfer function.

---

## Missions

### Wheels Up — Step Response

```
vel=3, log=2 : time=0.5
vel=4 : log=0
```

| Line | What happens |
|------|-------------|
| 1 | Drive at 3 V for 0.5 s (reach steady state), start logging at 2 ms |
| 2 | Step to 4 V, run until log buffer is full |

### On the Floor — Step Response

Driving on the floor requires a **longer sampling time** (and plenty of space).

```
vel=3, log=4 : time=0.5
vel=4 : log=0
```

> [!tip]
> Use `log = 3` or `log = 4` ms when driving on the floor to capture the full response over a longer distance.

---

## MATLAB Data Analysis

### Loading the Log File

The REGBOT log files contain `%` comment headers that must be skipped:

```matlab
opts = detectImportOptions('log_wheels_up.txt', 'FileType', 'text');
opts.CommentStyle = '%';
data = readtable('log_wheels_up.txt', opts);
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

The raw data contains three phases that must be separated:
1. **0 → 3 V startup** — velocity ramps up from rest (not useful for identification)
2. **3 V → 4 V step** — the step response we want to identify
3. **Motor shutdown** — voltage drops to 0, velocity coasts down

We trim by finding where the voltage crosses the midpoint (3.5 V) and include a small baseline window before the step:

```matlab
V_mid = 3.5;
u_avg = (u_L + u_R) / 2;
idx_step = find(u_avg >= V_mid, 1, 'first');
N_pre = min(50, idx_step - 1);
idx_start = idx_step - N_pre;
```

### Removing Offsets

Subtract the **pre-step baseline mean** so all signals start from 0:

```matlab
u_L = u_L - mean(u_L(1:N_pre));
v_L = v_L - mean(v_L(1:N_pre));
```

> [!warning] Outlier Removal
> Check for outliers (spikes) in the data before proceeding. The script uses `medfilt1` (median filter, window=5) to remove spikes automatically.

---

## Transfer Function Identification

### Preparing Identification Data

Compute average voltage and velocity, then create `iddata` objects:

```matlab
vel  = 1/2 * (v_L + v_R);       % average wheel velocity
volt = 1/2 * (u_L + u_R);       % average voltage

idd_L   = iddata(v_L, u_L, T_s);    % left wheel data
idd_R   = iddata(v_R, u_R, T_s);    % right wheel data
idd_avg = iddata(vel, volt, T_s);   % average data
```

### Estimating Transfer Functions

Use `tfest` to identify transfer functions (2 poles, 0 zeros — try other combinations as needed):

```matlab
G_wu_L   = tfest(idd_L, 2, 0);      % left wheel
G_wu_R   = tfest(idd_R, 2, 0);      % right wheel
G_wu_avg = tfest(idd_avg, 2, 0);    % average
```

---

## Results — Wheels Up

### Raw Log Data

Motor voltage and velocity as recorded from the REGBOT with wheels raised. The three phases are clearly visible: 0→3 V startup transient (0–0.5 s), the 3 V→4 V step (at t ≈ 0.5 s), and motor shutdown (t ≈ 3.2 s). The velocity is noisy due to the encoder resolution at 2 ms sampling.

![[day5_raw_data_up.png]]

### Trimmed Step Response

Data trimmed to the 3 V→4 V step region with the startup transient and shutdown removed. Offsets subtracted using the pre-step baseline mean. The vertical dashed line marks the step moment (t = 0). Before the step, signals hover around zero; after, the velocity rises to a new steady state.

![[day5_trimmed_up.png]]

### Model vs. Measured — Average

The `tfest`-identified 2nd order transfer function (red dashed) overlaid on the measured average velocity (blue). The model settles to ~0.33 m/s, sitting right in the mean of the noisy data. The fast rise time (~0.05 s) indicates the wheels-up system has very little inertia.

![[day5_model_vs_meas_avg_up.png]]

### compare() Validation

MATLAB's `compare` function applied to all three `iddata` sets. Fit percentages are moderate (L: 28%, R: 36%, Avg: 45%) — this is due to the high measurement noise rather than a poor model shape. The model (blue line) tracks the mean trend of the data (grey) correctly.

![[day5_compare_up.png]]

### Transfer Function Analysis

Step response, impulse response, and Bode plot of the three identified transfer functions (left, right, average). The step response settles within ~0.1 s. The Bode plot shows rolloff beginning around 10–100 rad/s with -180° phase at high frequencies, consistent with a 2-pole system.

![[day5_tf_analysis_up.png]]

---

## Results — On the Floor

### Raw Log Data

Motor voltage and velocity recorded while driving on the floor. The robot drove at 3 V, then stepped to 4 V. Around t ≈ 6 s the robot hit a wall, causing erratic voltage and velocity readings. The data after the collision is unusable and is automatically trimmed out by the script (max 4 s window + velocity collapse detection).

![[day5_raw_data_floor.png]]

### Model vs. Measured — Average

The identified floor transfer function (red dashed) overlaid on the measured average velocity (blue), using only the clean data before the wall collision. The model captures the step response well: a slower rise time (~0.2 s) compared to wheels-up, settling to ~0.36 m/s. The floor adds friction and load which slows the dynamics.

![[day5_model_vs_meas_floor.png]]

### compare() Validation

The `compare` function on the trimmed floor data. Fit percentages are improved over the previous (broken) attempt: L: 41%, R: 49%, Avg: 57%. The higher fit compared to wheels-up is partly because the floor response is slower (less high-frequency noise dominance).

![[day5_compare_floor.png]]

### Transfer Function Analysis

Step response, impulse response, and Bode plot for the on-floor transfer functions. The step response settles in ~0.5 s (much slower than wheels-up). The Bode plot shows a lower bandwidth, reflecting the added inertia from floor contact.

![[day5_tf_analysis_floor.png]]

---

## Results — Comparison

### Wheels Up vs. On the Floor

Side-by-side comparison of the average transfer functions from both conditions:

![[day5_up_vs_floor.png]]

| Property | Wheels Up | On Floor |
|----------|-----------|----------|
| DC gain | ~0.33 (m/s)/V | ~0.36 (m/s)/V |
| Rise time | ~0.05 s | ~0.2 s |
| Settling time | ~0.1 s | ~0.5 s |
| Bandwidth | Higher (~100 rad/s) | Lower (~10 rad/s) |

The floor adds friction and load, which:
- **Slows the response** significantly (4× longer rise time)
- **Reduces bandwidth** — the Bode magnitude drops off at lower frequencies
- **Slightly increases DC gain** — more voltage is needed per unit speed, but the steady-state ratio changes due to the different friction/load balance

---

## Key Observations

> [!success] Summary
> - The **2-pole, 0-zero model** captures both step responses well despite noisy encoder data
> - **Wheels up**: fast dynamics (~0.05 s rise time), high bandwidth — minimal load on the motors
> - **On floor**: significantly slower dynamics (~0.2 s rise time) — floor friction and robot weight add inertia and damping
> - **Fit percentages** are limited by encoder noise (28–57%), not by model structure — the model shapes track the data mean correctly
> - The **floor data required careful trimming** — the robot hit a wall at t ≈ 6 s, producing unusable data that was automatically excluded
> - Left and right wheels show **slight asymmetry** in both conditions, visible in the individual wheel fits

---

> [!nav]
> [[Day 4 - REGBOT Introduction|← Day 4]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> [[Day 6 - Bode Plot and P-Controller Design|Day 6 →]]
