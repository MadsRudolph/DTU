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

1. **Bypass velocity controller:** Enable controller with $K_{ff} = 1$ and $K_p = 0$
2. **Activate heading controller** (set $K_p$ as from hand-tuning, or $K_p = 1$)
3. Set position controller values as designed in Tasks 2-3

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

> [!todo] Fill in after completing the exercise
> Run the MATLAB scripts and paste results / screenshots here.

### Bode Plots: $G(s)$, $C_{PI}(s)$, $C_D(s)$

![[day8_component_bode.png]]

### Open-Loop $G_{ol}(s)$ with Crossover Frequency

![[day8_open_loop_bode.png]]

### Closed-Loop $G_{cl}(s)$ — Both Architectures

![[day8_closed_loop_bode.png]]

### Step Response Comparison

![[day8_step_response.png]]

### Simulink Results

![[day8_simulink_results.png]]

### REGBOT Experimental Results

![[day8_regbot_results.png]]

---

## Key Observations

> [!success] Summary
> - *Fill in after running the exercise*

---

> [!nav]
> [[Day 6 - Bode Plot and P-Controller Design|← Day 6]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
