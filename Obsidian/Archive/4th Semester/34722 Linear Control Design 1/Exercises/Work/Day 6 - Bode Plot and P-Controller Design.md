---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise, MATLAB]
date: 2026-03-18
---
# Day 6 - Bode Plot and Proportional Controller Design

> [!abstract] Exercise Overview
> Calculate open-loop and closed-loop transfer functions with a proportional (P) controller. Analyze system behavior through Bode plots, assess the effect of a low-pass filter on stability and robustness, and refine the filter design to limit phase margin reduction to 30 degrees.

> [!info] Files
> - MATLAB script: [Day6.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day6/Day6.m)
> - Prerequisite: Transfer functions from [[Day 5 - Black Box Modeling]]

> [!example] Related Materials
> - Previous exercise: [[Day 5 - Black Box Modeling]]
> - Lecture slides: [[6_Bode_plot&Stability.pdf]]

---

## Requirements

Design and analyze a P-controller for the REGBOT velocity system:
1. Compare Bode plots for **wheels up** and **on floor** transfer functions
2. Design an open-loop system with a **P-controller** ($K_p \leq 15$)
3. Add a **1st-order low-pass filter** to reduce measurement noise
4. Evaluate **open-loop** and **closed-loop** step responses

**Deliverables:**
- Bode plots for "wheels up" and "wheels down" scenarios
- Open-loop TF with P-controller Bode plot, including phase margin analysis
- Speed measurement plot with applied low-pass filter
- Bode plot and step response for the filtered open-loop system
- Step response simulation for the closed-loop system with P-controller and low-pass filter

---

## Theory

### Proportional Controller

A P-controller simply scales the error signal by a gain $K_p$:

$$G_{ol}(s) = K_p \cdot G(s)$$

Increasing $K_p$ increases the crossover frequency (faster response) but reduces phase margin (less stable).

### Low-Pass Filter

A first-order low-pass filter attenuates high-frequency noise:

$$G_{filt}(s) = \frac{\omega_c}{s + \omega_c}$$

where $\omega_c$ is the **break frequency** (cutoff). The filter introduces phase lag, reducing the phase margin. The design goal is to choose $\omega_c$ large enough to preserve stability while filtering noise.

### Closed-Loop Transfer Function

With the P-controller and filter in the feedback path:

$$G_{cl}(s) = \frac{K_p \cdot G(s)}{1 + K_p \cdot G(s) \cdot G_{filt}(s)}$$

> [!important] Note
> The filter is in the **feedback loop** (it filters the measured velocity), not in the forward path. This is why $G_{filt}$ appears in the denominator but not the numerator.

---

## Task 1: Bode Plot Comparison

Compare the Bode plots of the wheels-up and on-floor transfer functions from Day 5:

```matlab
bode(G_wu_avg, 'b', G_floor_avg, 'r');
legend('Wheels Up', 'On Floor');
```

**What to look for:**
- **DC gain difference** — floor friction changes the steady-state gain
- **Bandwidth difference** — floor contact reduces bandwidth significantly
- **Phase rolloff** — both are 2-pole systems, so phase approaches $-180°$

---

## Task 2: Open-Loop with P-Controller

Create the open-loop TF and analyze margins:

```matlab
Kp = 15;
G_ol = Kp * G_wu_avg;
margin(G_ol);
[Gm, Pm, Wcg, Wcp] = margin(G_ol);
```

**Key values to extract:**
| Parameter | Symbol | MATLAB |
|-----------|--------|--------|
| Gain margin | $G_m$ | `Gm` (linear), `20*log10(Gm)` (dB) |
| Phase margin | $\phi_m$ | `Pm` (degrees) |
| Gain crossover freq | $\omega_{gc}$ | `Wcp` (rad/s) |
| Phase crossover freq | $\omega_{pc}$ | `Wcg` (rad/s) |

---

## Task 3: Low-Pass Filter Design

### Plotting Noisy Measurements

Plot the raw wheel speed from Day 5 to visualize the noise:

```matlab
plot(t_raw, vL_raw, 'b', t_raw, vR_raw, 'r');
title('Raw Wheel Speed Measurements (Noisy)');
```

### Designing the Filter

The filter must satisfy: **phase margin reduction $\leq 30°$**.

Strategy: iteratively adjust the break frequency $\omega_c$ until the phase margin with the filter is at most 30° less than without:

$$\phi_{m,filtered} \geq \phi_{m,unfiltered} - 30°$$

```matlab
PM_target = Pm - 30;   % minimum acceptable PM

wc_candidates = logspace(0, 4, 500);
for i = length(wc_candidates):-1:1
    G_filt_try = tf(wc_try, [1 wc_try]);
    G_ol_filt_try = Kp * G_wu_avg * G_filt_try;
    [~, Pm_try, ~, ~] = margin(G_ol_filt_try);
    if Pm_try >= PM_target
        wc_best = wc_try;
    else
        break;
    end
end
```

### Filtered Open-Loop

```matlab
G_filt = tf(wc_best, [1 wc_best]);
G_ol_filt = Kp * G_wu_avg * G_filt;
margin(G_ol_filt);
```

---

## Task 4: System Response Evaluation

Generate Bode plot and step response for the filtered open-loop:

```matlab
figure;
subplot(2,1,1); margin(G_ol_filt);
subplot(2,1,2); step(G_ol_filt);
```

Compare the filtered vs unfiltered open-loop:

```matlab
bode(G_ol, 'b', G_ol_filt, 'r--');
legend('Without Filter', 'With Filter');
```

---

## Task 5: Closed-Loop Simulation

Derive and simulate the closed-loop system:

```matlab
G_cl = Kp * G_wu_avg / (1 + Kp * G_wu_avg * G_filt);
G_cl = minreal(G_cl);
step(G_cl);
info = stepinfo(G_cl);
```

**Step response metrics to report:**

| Metric | Value |
|--------|-------|
| Rise time | `info.RiseTime` |
| Settling time | `info.SettlingTime` |
| Overshoot | `info.Overshoot` % |
| DC gain | `dcgain(G_cl)` |

---

## Results

> [!todo] Fill in after running Day6.m
> Run the MATLAB script and paste results / screenshots here.

### Bode Comparison: Wheels Up vs Floor

![[day6_bode_comparison.png]]

### Open-Loop with P-Controller

![[day6_open_loop_P.png]]

### Raw Speed Measurements (Noise)

![[day6_speed_noise.png]]

### Filter Effect on Open-Loop

![[day6_filter_effect.png]]

### Filtered Open-Loop: Bode + Step

![[day6_filtered_OL.png]]

### Closed-Loop Step Response

![[day6_closed_loop_step.png]]

---

## Key Observations

> [!success] Summary
> - *Fill in after running the exercise*

---

> [!nav]
> [[Day 5 - Black Box Modeling|← Day 5]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
