---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise, MATLAB, Simulink, REGBOT]
date: 2026-03-25
---
# Day 8 & 9 - Position Controller Design for REGBOT

> [!abstract] Exercise Overview
> Design a PI-Lead position controller for the REGBOT with no steady-state error and a phase margin of 60 degrees or better. Validate the design in MATLAB, Simulink, and on the physical REGBOT.

> [!info] Files
> - MATLAB scripts: [Day8 folder](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day8/)
> - Exercise scripts: `Lecture_08_exercise_1.m`, `Lecture_08_exercise_2.m`, `Lecture_08_exercise_3.m`
> - Solutions: `Lecture_08_exercise_1_solution.m`, `Lecture_08_exercise_2_solution.m`, `Lecture_08_exercise_3_solution.m`
> - Helper scripts: `K_P_bode_plot.m`, `K_P_step_Nyquist.m`, `P_controller_bode.m`

> [!example] Related Materials
> - Previous exercise: [[Day 6 - Bode Plot and P-Controller Design]]
> - Prerequisite: Transfer functions from [[Day 5 - Black Box Modeling]]
> - Lecture slides: [[Lecture_08_PI_LEAD_design.pdf]]

---

## Objective

Design a position controller for the REGBOT and evaluate in simulation (MATLAB and Simulink) and with experiments.

## Requirements

- PI-Lead control design (Lecture 8)
- Time-domain specifications (Lecture 9)
- Working with MATLAB and Simulink (Lecture 1)
- Working with REGBOT (Lecture 4)

---

## Task 1: Transfer Function from Voltage to Position

Starting from the voltage-velocity transfer function identified in Day 5, find the transfer function $G(s)$ from voltage to forward position (along $x$).

> [!tip] Key Insight
> Position is the integral of velocity, so multiply the velocity transfer function by $\frac{1}{s}$:
>
> $$G(s) = G_{vel}(s) \cdot \frac{1}{s}$$

---

## Task 2: PI-Lead Position Controller Design

Design a PI-Lead controller such that:
- **No steady-state error** in position
- **Phase margin $\geq 60°$**

### Step 2.1: Bode Plot of $G(s)$

```matlab
bode(G);
grid on;
```

### Step 2.2: Select Initial Parameters

Choose starting values:
- $N_i = 5$ (PI zero placement factor)
- $\alpha = 0.1$ (Lead controller ratio)

### Step 2.3: Find Crossover Frequency $\omega_c$

Using the phase-balance equation and the Bode plot of $G(s)$, find the new crossover frequency $\omega_c$ such that the required phase margin is achieved.

> [!note] Phase-Balance Equation
> The phase contributions of all controller parts must sum to give the desired phase margin at $\omega_c$.

### Step 2.4: PI Controller Design

Find the time constant $\tau_i$ associated with the zero of the PI part:

$$\tau_i = \frac{N_i}{\omega_c}$$

The PI transfer function:

$$C_{PI}(s) = \frac{\tau_i s + 1}{\tau_i s}$$

### Step 2.5: Lead Controller Design

Find the time constant $\tau_d$ associated with the Lead part:

$$C_D(s) = \frac{\tau_d s + 1}{\alpha \tau_d s + 1}$$

### Step 2.6: Proportional Gain $K_P$

Find $K_P$ such that the combined open-loop transfer function has 0 dB magnitude at $\omega_c$:

$$G_{ol}(s) = K_P \cdot C_{PI}(s) \cdot C_D(s) \cdot G(s)$$

$$|G_{ol}(j\omega_c)| = 1 \quad (0 \text{ dB})$$

### Step 2.7: Closed-Loop Transfer Function

Calculate $G_{cl}(s)$ for two architectures:

**a) Lead in forward branch:**

$$G_{cl}(s) = \frac{K_P \cdot C_{PI}(s) \cdot C_D(s) \cdot G(s)}{1 + K_P \cdot C_{PI}(s) \cdot C_D(s) \cdot G(s)}$$

**b) Lead in feedback branch:**

$$G_{cl}(s) = \frac{K_P \cdot C_{PI}(s) \cdot G(s)}{1 + K_P \cdot C_{PI}(s) \cdot C_D(s) \cdot G(s)}$$

### Step 2.8: Step Response Evaluation

```matlab
step(G_cl_a);  % Lead in forward
hold on;
step(G_cl_b);  % Lead in feedback
legend('Lead Forward', 'Lead Feedback');
stepinfo(G_cl_a)
stepinfo(G_cl_b)
```

**Evaluate:**
- Is there steady-state error?
- Is the final value reached in less than 10 sec?
- Which architecture has the smallest overshoot?
- Which has the fastest convergence?

> [!warning] Design Iteration
> Readjust $N_i$ and $\alpha$ so that:
> - No steady-state error
> - Convergence below 10 seconds

---

## Task 3: Simulink Implementation

### Setting Up the Model

1. Open Simulink: type `simulink` in MATLAB command line
2. Select "Blank Model"
3. Add blocks from Library Browser:
   - **Sources:** Step block (start at $t = 0.1$ s, step size $= 0.5$ m)
   - **Continuous:** Transfer Function blocks for $G_{vu}$, $C_{PI}$, $C_D$, $K_P$, integrator ($1/s$)
   - **Commonly Used:** Sum, Gain
   - **Sinks:** Scope, To Workspace
   - **Discontinuities:** Saturation (limits: $-9$ to $+9$)

> [!important] Architecture
> Use only the case of **Lead in the feedback branch**.

### Block Diagram

```
                          ┌──────────┐
Position  ──►(Sum)──►│Saturation│──►[G_vu]──►[1/s]──► pos ──► To Workspace
  step       -│      └──────────┘                        │
              │                                          │
              └────────[C_D]◄────[C_PI]◄────[K_P]◄──────┘
```

### Extracting Polynomials for Transfer Function Blocks

```matlab
[num_G, den_G] = tfdata(G, 'v');   % Get polynomials from transfer functions
```

### Running the Simulation

```matlab
% Method 1
sim('model_name', 5);   % simulate for 5 seconds
plot(simout);

% Method 2 (newer MATLAB versions)
regbot_sim = sim("model_name", 5);
plot(regbot_sim.simout);
```

**Compare** Simulink results with MATLAB simulation from Task 2. Does the saturation affect performance? What happens with limits at $-3$ and $+3$?

---

## Task 4: REGBOT Implementation

### Controller Setup

1. **Bypass velocity controller:** Enable, set $K_{ff} = 1$, $K_p = 0$
2. **Activate heading controller:** set $K_p = 1$
3. **Position controller** (Lead/Lag in feedback):

```
K_P      = 111.73
tau_i    = 0.1358
tau_zero = 0.0859
tau_pole = 0.00859
```

### Mission Script

```
vel=0, log=10 : time=0.1
vel=3, topos=0.5: log=0
```

- `time=0.1` — wait 0.1 s for comparison with simulation
- `vel=3` — max reference to speed controller (3V motor voltage since $K_{ff} = 1$)
- `topos=0.5` — target distance 0.5 m
- `log=0` — stop when log is full

### Data Logging

Log the following signals:
- Motor voltage
- Wheel velocity
- Robot pose

### Analysis

Load data in MATLAB, plot "Pose x" (driven distance / position reference) and compare with simulated results.

---

## How to Present Results

> [!important] Required Plots
> 1. **Bode plots** of $G(s)$, $C_{PI}(s)$, $C_D(s)$ on the same plot (use `hold on`, `hold off`)
> 2. **Bode plot** of $G_{ol}(s)$ with crossover frequency shown
> 3. **Bode plot** of $G_{cl}(s)$ for both architectures (Lead forward and Lead feedback) with bandwidth frequency
> 4. **Step response** of $G_{cl}(s)$ for both architectures on the same plot
> 5. **Experimental results** from REGBOT: position, position reference, and voltages

### REGBOT Plot Template

```matlab
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(5);
aa = subplot(2,1,1);
  plot(t, x);
  hold on;
  plot(t, 0.5*ones(size(t)), '--k');
  hold off;
  grid on;
  ylabel('$x, x_{ref}$ in m');
  legend({'$x$', '$x_{ref}$'}, 'interpreter', 'latex');

bb = subplot(2,1,2);
  plot(t, u_L);
  hold on;
  plot(t, u_R);
  hold off;
  grid on;
  xlabel('$t$ in s');
  ylabel('$u_L, u_R$ in V');
  legend({'$u_L$', '$u_R$'}, 'interpreter', 'latex');

linkaxes([aa, bb], 'x');
```

---

## Results

### Exercise 1: P Controller — $G(s) = \frac{40}{s(s+10)^2}$

**System analysis:**
- Poles: $s = 0, -10, -10$ (type-1 system — integrator at origin)
- Original $\omega_c = 0.399$ rad/s, $\gamma_M = 85.4°$ (stable but very slow)

**Design for $\gamma_M = 60°$:**
- New $\omega_c = 2.69$ rad/s (6.7x faster)
- $K_P = 7.21$

| Metric | Value |
|---|---|
| Rise time | 0.451 s |
| Settling time | 1.413 s |
| Overshoot | 7.87% |
| $e_{ss}$ | 0 (type-1 system) |

![[day8_ex1_bode.png]]
![[day8_ex1_step.png]]

> [!tip] Key Insight
> Type-1 systems achieve zero steady-state error with just a P controller. The integrator in the plant eliminates the need for a PI part.

---

### Exercise 2: PI Controller — $G(s) = \frac{3.3}{s^3 + 5s^2 + 2.1s + 1}$

**System analysis:**
- Poles: $s = -4.59$, $s = -0.205 \pm 0.419j$ (type-0, oscillatory complex pair near imaginary axis)
- PI phase contribution: $\phi_i = -18.43°$
- Required plant phase: $\phi_G = -101.57°$

**Design ($N_I = 3$, $\gamma_M = 60°$):**
- $\omega_c = 0.49$ rad/s, $\tau_i = 6.12$ s, $K_P = 0.269$

| Metric | P controller | PI controller |
|---|---|---|
| Rise time | 2.09 s | 4.42 s |
| Settling time | 21.65 s | 38.05 s |
| Overshoot | 38.69% | 0% |
| $e_{ss}$ | 0.530 | 0 |

![[day8_ex2_bode.png]]
![[day8_ex2_bode_ol.png]]
![[day8_ex2_step.png]]

> [!warning] Trade-off
> The PI controller eliminates steady-state error and overshoot, but at the cost of much slower response. The PI phase penalty (-18.4°) forces a lower crossover frequency. This motivates adding a Lead part to recover speed.

---

### Exercise 3: PI-Lead Controller — $G(s) = \frac{40}{(s+1)(s+10)^2}$

**System analysis:**
- Type-0 system, stable, needs PI for zero $e_{ss}$

**Design ($N_I = 3$, $\alpha = 0.3$, $\gamma_M = 60°$):**
- PI: $\phi_i = -18.43°$, Lead: $\phi_m = +32.58°$ (net: $+14.15°$)
- $\omega_c = 5.30$ rad/s, $\tau_i = 0.567$ s, $\tau_d = 0.345$ s, $K_P = 8.96$
- Achieved phase margin: $59.04°$, gain margin: $12.51$ dB

| Metric | P | PI | PI-Lead (fwd) | PI-Lead (fb) |
|---|---|---|---|---|
| Rise time | 0.34 s | 0.32 s | 0.22 s | 0.72 s |
| Settling time | 1.12 s | 1.95 s | 1.58 s | 1.19 s |
| Overshoot | 12.3% | 31.5% | 11.4% | 1.3% |
| $e_{ss}$ | 0.218 | 0 | 0 | 0 |
| Bandwidth | — | — | 10.20 rad/s | 3.12 rad/s |

![[day8_ex3_component_bode.png]]
![[day8_ex3_bode_ol.png]]
![[day8_ex3_step.png]]
![[day8_ex3_bode_cl.png]]

> [!success] Architecture Comparison
> - **PI-Lead (forward):** fastest response (0.22s rise), good for reference tracking. But amplifies high-frequency reference content $\to$ larger control signals.
> - **PI-Lead (feedback):** smoothest response (1.3% overshoot), best for disturbance rejection. Lower bandwidth (3.1 vs 10.2 rad/s) means less aggressive control effort.
> - For the REGBOT, we use **Lead in feedback** to avoid aggressive motor voltages.

---

---

### REGBOT Position Controller Design

**Plant:** Floor velocity TF from Day 5, multiplied by $1/s$ for position:

$$G_{pos}(s) = \frac{G_{vel}(s)}{s} = \frac{128400}{s^3 + 32720s^2 + 355900s}$$

- Type-1 system (integrator at origin)
- Fast pole at $s = -32712$ (nearly instantaneous), slow pole at $s = -10.9$
- Original margins: $\gamma_M = 88.1°$ at $\omega_c = 0.36$ rad/s (very slow)

**Design ($N_I = 5$, $\alpha = 0.1$, $\gamma_M = 60°$):**

| Parameter | Value |
|---|---|
| $\phi_i$ (PI) | $-11.31°$ |
| $\phi_m$ (Lead) | $+54.90°$ |
| $\omega_c$ | 36.82 rad/s |
| $\tau_i$ | 0.1358 s |
| $\tau_d$ | 0.0859 s |
| $K_P$ | 111.73 |

**Achieved margins:** $\gamma_M = 60.0°$, gain margin = 58.2 dB.

| Metric | PI-Lead (forward) | PI-Lead (feedback) |
|---|---|---|
| Rise time | 0.032 s | 0.133 s |
| Settling time | 0.300 s | 0.215 s |
| Overshoot | 17.21% | 1.15% |
| Bandwidth | 58.4 rad/s | 15.8 rad/s |
| $e_{ss}$ | 0 | 0 |

![[day8_regbot_bode_plant.png]]
![[day8_regbot_component_bode.png]]
![[day8_regbot_bode_ol.png]]
![[day8_regbot_step.png]]
![[day8_regbot_bode_cl.png]]

> [!important] REGBOT Controller Values
> ```
> K_P   = 111.73
> tau_i = 0.1358 s
> tau_d = 0.0859 s
> alpha = 0.10
> ```
> Use **Lead in feedback** architecture for smoother control effort.

> [!warning] Saturation
> With $K_P = 112$ and a 0.5 m step, the initial control signal is $\sim 56$ V — far exceeding the $\pm 9$ V motor limit. The saturation will limit the actual voltage, making the real response slower than the linear simulation. The PI integrator will wind up during saturation and correct any residual error.

---

### Simulink Results

Simulink model with Lead-in-feedback architecture, including motor voltage saturation.

**With $\pm 9$ V saturation:**

| Metric | MATLAB (linear) | Simulink ($\pm 9$ V) |
|---|---|---|
| Rise time | 0.133 s | 0.164 s |
| Settling time | 0.215 s | 0.742 s |
| Overshoot | 1.15% | 26.47% |
| $e_{ss}$ | 0 | 0 |

The saturation causes **integrator windup**: while the motor is saturated at 9V, the PI integrator keeps accumulating error. When the system catches up, the integrator has built up excess control effort, causing significant overshoot (26.5% vs 1.15% without saturation). With $\pm 3$ V limits, the response is even slower but still converges to zero error.

![[day8_simulink_9V.png]]
![[day8_simulink_vs_matlab.png]]
![[day8_simulink_sat_comparison.png]]

### REGBOT Experimental Results

**First attempt** ($K_P = 111.73$, $N_I = 5$, $\alpha = 0.1$):

| Metric | Simulink ($\pm 9$ V) | REGBOT (experiment) |
|---|---|---|
| Rise time | 0.164 s | 0.660 s |
| Settling time | 0.742 s | 26.4 s |
| Overshoot | 26.5% | 80.3% |
| $e_{ss}$ | 0 m | 0.013 m |

![[day8_regbot_results.png]]
![[day8_regbot_vs_matlab.png]]

> [!warning] Controller Too Aggressive
> The high $K_P = 112$ causes severe integrator windup and sustained oscillations on the real REGBOT. The identified transfer function (57% fit) doesn't perfectly match the real system — model mismatch at high gain leads to much worse performance than predicted. Need to retune with more conservative parameters.

**Second attempt** ($K_P = 21.20$, $N_I = 3$, $\alpha = 0.3$):

| Metric | REGBOT (attempt 1) | REGBOT (attempt 2) |
|---|---|---|
| $K_P$ | 111.73 | 21.20 |
| Rise time | 0.660 s | 0.720 s |
| Settling time | 26.4 s | 19.6 s |
| Overshoot | 80.3% | 60.3% |
| $e_{ss}$ | 0.013 m | 0.0005 m |

![[day8_regbot_conservative.png]]
![[day8_regbot_comparison.png]]

**Third attempt** ($K_P = 10.60$, $N_I = 3$, $\alpha = 0.3$, same $\tau$ values):

| Metric | Attempt 1 | Attempt 2 | Attempt 3 |
|---|---|---|---|
| $K_P$ | 111.73 | 21.20 | 10.60 |
| Rise time | 0.660 s | 0.720 s | 0.730 s |
| Settling time | 26.4 s | 19.6 s | 10.8 s |
| Overshoot | 80.3% | 60.3% | 60.1% |
| $e_{ss}$ | 0.013 m | 0.0005 m | 0.0001 m |

![[day8_regbot_half_kp.png]]
![[day8_regbot_all_attempts.png]]

**Fourth attempt** ($K_P = 10.60$ with training wheels):

| Metric | No support | With training wheels |
|---|---|---|
| Rise time | 0.730 s | 0.680 s |
| Settling time | 10.8 s | 4.2 s |
| Overshoot | 60.1% | 57.0% |
| $e_{ss}$ | 0.0001 m | 0.0001 m |

![[day8_regbot_support.png]]
![[day8_regbot_support_comparison.png]]

> [!note] Analysis
> - **Overshoot** plateaus around 57–60% regardless of $K_P$ or training wheels — the identified transfer function (57% fit) doesn't capture the real dynamics accurately enough. The model likely underestimates delay and friction nonlinearities.
> - **Training wheels** dramatically improve settling time (10.8s → 4.2s) by removing tilt disturbances, but don't fix overshoot.
> - **Steady-state error** is effectively zero in all cases ($< 0.001$ m) — the PI controller works as designed.
> - **Best result**: $K_P = 10.6$ with training wheels — reaches 0.5m target, settles in ~4s, zero $e_{ss}$.

---

## Key Observations

> [!success] Summary
> - **Type-1 systems** (with plant integrator) achieve zero $e_{ss}$ with P control alone
> - **Type-0 systems** need PI for zero $e_{ss}$, but PI introduces phase penalty that degrades speed/stability
> - **Lead compensation** recovers the phase lost from PI, enabling higher crossover frequencies and faster response
> - **Lead placement** matters: forward path = higher bandwidth + larger control signals; feedback path = lower bandwidth + smoother response
> - The **phase balance equation** $-180° + \gamma_M = \phi_G + \phi_i + \phi_m$ is the core design tool
> - **Saturation + integrator windup** is the dominant real-world issue: the PI integrator accumulates error while the motor is saturated, causing large overshoot that linear analysis doesn't predict
> - **Model accuracy matters**: the 57%-fit Day 5 transfer function leads to significant theory-vs-reality mismatch, especially at high gains. Iterative tuning on the real system is essential
> - **Lower $K_P$** reduces settling time on the real REGBOT even though linear theory predicts slower response — avoiding saturation is more important than maximizing crossover frequency

---

> [!nav]
> [[Day 6 - Bode Plot and P-Controller Design|← Day 6]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
