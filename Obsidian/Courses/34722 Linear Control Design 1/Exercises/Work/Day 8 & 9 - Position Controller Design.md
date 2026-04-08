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
> - REGBOT controller: `regbot_position_controller_v2.m`
> - Simulink model: `regbot_position_sim.slx`
> - Results plotting: `regbot_plot_results.m`, `regbot_simulink.m`

> [!example] Related Materials
> - Lecture exercises: [[Lecture 8 - PI-Lead Controller Design Exercises]]
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

Velocity TF from Day 5 → multiply by $\frac{1}{s}$ to get position:

```matlab
s = tf('s');
G_vel = 2.198 / (s + 5.985);       % Day 5 velocity TF (1-pole, training wheels)
G = minreal(G_vel / s);             % Position TF = velocity * 1/s
```

$$G(s) = \frac{2.198}{s(s + 5.985)}$$

Poles: $s = 0$ and $s = -5.985$. The pole at $s = 0$ makes it **type-1** (has an integrator), so it will have zero steady-state error.

---

## Task 2: PI-Lead Position Controller Design

Goal: no steady-state error, phase margin $\geq 60°$.

### Step 1: Look at the Bode plot of $G(s)$

```matlab
w = logspace(-2, 3, 5000);
[M, P, w_out] = bode(G, w);
M = mag2db(squeeze(M));
P = squeeze(P);
```

### Step 2: Pick $N_i$ and $\alpha$

```matlab
N_i   = 3;       % How far below omega_c to place the PI zero (start with 5)
alpha = 0.3;     % Lead ratio, between 0 and 1 (start with 0.1)
gamma_M = 60;    % Desired phase margin [deg]
```

### Step 3: Find $\omega_c$ using the phase-balance equation

Each controller part adds phase at $\omega_c$. We need the total to give $60°$ margin:

$$\underbrace{\angle G(j\omega_c)}_{\text{plant phase}} + \underbrace{\phi_i}_{\text{PI (negative)}} + \underbrace{\phi_m}_{\text{Lead (positive)}} = -180° + 60°$$

Rearranging — the plant phase we need:

$$\phi_G = -180° + 60° - \phi_i - \phi_m$$

```matlab
phi_i = rad2deg(-atan(1/N_i));              % PI phase (always negative)
phi_m = rad2deg(asin((1-alpha)/(1+alpha))); % Lead phase (always positive)
phi_G_req = -180 + gamma_M - phi_i - phi_m; % Required plant phase

% Find where the plant phase crosses phi_G_req => that's omega_c
i_c = find(P <= phi_G_req, 1, 'first');
omega_c = w_out(i_c);
```

### Step 4: Build the PI controller

The PI zero goes at $\omega_c / N_i$ (well below crossover so it doesn't mess up phase too much):

```matlab
tau_i = N_i / omega_c;
C_PI = (tau_i*s + 1) / (tau_i*s);    % = 1 + 1/(tau_i*s)
```

### Step 5: Build the Lead controller

```matlab
tau_d = 1 / (omega_c * sqrt(alpha));
C_D = (tau_d*s + 1) / (alpha*tau_d*s + 1);
```

### Step 6: Find $K_P$

We need $|K_P \cdot C_{PI} \cdot C_D \cdot G| = 1$ at $\omega_c$ (0 dB):

```matlab
G_ol_noK = minreal(C_PI * C_D * G);
K_P = 1 / abs(freqresp(G_ol_noK, omega_c));
```

Bode plot of all three components ($G$, $C_{PI}$, $C_D$):

![[day8_regbot_component_bode.png]]

Open-loop Bode ($K_P \cdot C_{PI} \cdot C_D \cdot G$) with $\omega_c$ marked:

![[day8_regbot_bode_ol.png]]

### Step 7: Close the loop — two ways

```matlab
% a) Lead in forward path (faster, more overshoot)
G_cl_fwd = minreal(K_P*C_PI*C_D*G / (1 + K_P*C_PI*C_D*G));

% b) Lead in feedback path (smoother, less overshoot)
G_cl_fb = minreal(K_P*C_PI*G / (1 + K_P*C_PI*C_D*G));
```

Closed-loop Bode for both architectures:

![[day8_regbot_bode_cl.png]]

### Step 8: Compare step responses

```matlab
step(G_cl_fwd); hold on; step(G_cl_fb); hold off;
legend('Lead forward', 'Lead feedback');
stepinfo(G_cl_fwd)
stepinfo(G_cl_fb)
```

![[day8_regbot_step.png]]

### Results

With $N_i = 3$, $\alpha = 0.3$, $\gamma_M = 60°$:

**Phase balance:**

| | Value |
|---|---|
| $\phi_i$ (PI) | $-18.43°$ |
| $\phi_m$ (Lead) | $+32.58°$ |
| $\phi_G$ required | $-134.14°$ |
| $\omega_c$ | 5.82 rad/s |

**Controller parameters:**

| | Value |
|---|---|
| $\tau_i$ | 0.5159 s |
| $\tau_d$ (zero) | 0.3140 s |
| $\tau_d \cdot \alpha$ (pole) | 0.0942 s |
| $K_P$ | 11.47 |

Achieved phase margin: $59.97°$. Initial control effort: $11.47 \times 0.5 = 5.7$ V (below the 9 V limit).

**Step response comparison:**

| Metric | Lead forward | Lead feedback |
|---|---|---|
| Rise time | 0.202 s | 0.449 s |
| Settling time | 1.858 s | 2.129 s |
| Overshoot | 17.2% | 7.8% |
| $e_{ss}$ | 0 | 0 |

Feedback is smoother (7.8% vs 17.2% overshoot). Forward is faster (0.2 s vs 0.4 s rise). Both converge well under 10 s.

> [!important] REGBOT Controller Values (Lead in feedback)
> ```
> K_P      = 11.47
> tau_i    = 0.5159
> tau_zero = 0.3140
> tau_pole = 0.0942
> ```

---

## Task 3: Simulink Implementation

Implement the closed-loop in Simulink to test with motor voltage saturation ($\pm 9$ V).

> [!important] Architecture
> Use only **Lead in the feedback branch**.

### Block Diagram

```
                     ┌──────────┐
Position  ──►(Sum)──►│Saturation│──►[G_vu]──►[1/s]──► pos
  step       -│      └──────────┘                       │
              │                                         │
              └────────[C_D]◄────[C_PI]◄────[K_P]◄─────┘
```

- `G_vu` = velocity TF from Day 5 (not the full position TF — the $1/s$ integrator is separate)
- Saturation limits: $-9$ to $+9$ V (same as the real REGBOT motor)
- Step: start at $t = 0.1$ s, size $= 0.5$ m

### Setting up the Transfer Function blocks

To get the numerator/denominator polynomials from MATLAB TF objects:

```matlab
[num_vel, den_vel] = tfdata(G_vel, 'v');   % Velocity TF
[num_pi,  den_pi]  = tfdata(C_PI, 'v');    % PI controller
[num_cd,  den_cd]  = tfdata(C_D, 'v');     % Lead controller
```

### Running the Simulation

```matlab
sim_out = sim("regbot_position_sim", 5);   % simulate 5 seconds
plot(sim_out.pos_data);                     % plot position output
```

### Results: Simulink with $\pm 9$ V saturation

Since our controller gives 5.7 V initial effort (below the 9 V limit), the saturation barely affects the response:

![[day8_simulink_9V.png]]

### MATLAB (linear) vs Simulink (with saturation)

![[day8_simulink_vs_matlab.png]]

### What happens with tighter saturation ($\pm 3$ V)?

With $\pm 3$ V limits the motor saturates, making the response slower — but the PI integrator still eliminates steady-state error:

![[day8_simulink_sat_comparison.png]]

---

## Task 4: REGBOT Implementation

Implement the designed PI-Lead controller on the physical REGBOT using the "Control" tab.

### Controller Setup

1. **Bypass velocity controller:** Enable, set $K_{ff} = 1$, $K_p = 0$
2. **Activate heading controller:** set $K_p = 1$ (or hand-tuned value)
3. **Position controller** (Lead/Lag in feedback): set the values from Task 2

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

### Results: REGBOT Experiment

With the v2 controller ($K_P = 11.46$, training wheels):

| Metric | Value |
|---|---|
| Rise time | 0.680 s |
| Settling time | 3.56 s |
| Overshoot | 21.9% |
| $e_{ss}$ | 0.004 m |

![[day8_log_position_v2.png]]

The initial control effort (5.7 V) stays below the 9 V saturation limit, avoiding integrator windup. Steady-state error is effectively zero.

---

## How to Present Results

> [!important] Required Plots
> 1. **Bode plots** of $G(s)$, $C_{PI}(s)$, $C_D(s)$ on the same plot (use `hold on`, `hold off`)
> 2. **Bode plot** of $G_{ol}(s)$ with crossover frequency shown
> 3. **Bode plot** of $G_{cl}(s)$ for both architectures (Lead forward and Lead feedback) with bandwidth frequency
> 4. **Step response** of $G_{cl}(s)$ for both architectures on the same plot
> 5. **Experimental results** from REGBOT: position, position reference, and voltages

---

> [!nav]
> [[Day 6 - Bode Plot and P-Controller Design|← Day 6]]
>
> [[Lecture 8 - PI-Lead Controller Design Exercises|Lecture Exercises]]
>
> [[34722 Linear Control Design 1|34722 Home]]
