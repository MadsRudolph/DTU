# Lesson 2 - Block Diagrams and Control Concepts

> [!abstract] Lecture Overview
> Lesson 2/13 — Teachers: Silvia Tolu & Dimitrios Papageorgiou
> Topics: Block diagram modelling, control process introduction, controller design & hand-tuning, Ziegler-Nichols tuning.
> Reference: Feedback Control Techniques textbook, Chapters 2–3.

> [!example] Related Materials
> - Slides: [[2_block_control_concept.pdf]]
> - Exercise: [[Day 2 - Hand-Tuning Exercise]]
> - Quiz: [[Quiz 1 - Block Diagrams and Control Concepts]]
> - Previous: [[Day 1 - MATLAB Exercise]]
> - Prerequisites: [[Pretest Answers]]

---

## 1. Course Roadmap

The overall course flow for understanding and designing control systems:

1. **Modelling** — Derive mathematical models from physical systems
2. **Math** — Laplace transforms ($\mathcal{L}\{x(t)\}$)
3. **Block Diagrams** — Graphical representation of system relationships *(this lecture)*
4. **Stability** — Determine if a system is stable
5. **Frequency Domain** — Bode plots, frequency response
6. **Time Domain** — Step response, transient behaviour
7. **Controller Design** — Design controllers to meet specifications

---

## 2. Modelling Recap

The path from a physical system to a transfer function:

$$\text{Physical System} \xrightarrow{\text{First Principles}} \text{Nonlinear Model} \xrightarrow{\text{Linearization + Laplace}} \text{Transfer Function}$$

A nonlinear system is described by state equations:

$$\dot{x}(t) = f(x(t), u(t), t), \quad y(t) = g(x(t), u(t), t)$$

After linearization around a stationary point and Laplace transformation:

$$Y(s) = G(s) \cdot U(s)$$

---

## 3. Block Diagram Modelling

### 3.1 Basic Elements

A block diagram provides a **system overview** and is the link between physics and mathematics.

| Element | Description |
|---------|-------------|
| **Signals** $(x, y)$ | Input and output variables (arrows) |
| **Multiplication block** | Relates input to output via a function: $y = f(x)$ |
| **Summation block** | Adds/subtracts signals: $y = x_1 \pm x_2$ |
| **Branching** | Splits a signal to multiple destinations |
| **Integration** | $\frac{1}{s}$ block (integrates input over time) |

> [!tip] Building Block Diagrams
> Start from the **output** and work backwards step by step towards the input. This makes it easier to identify the physical meaning of each block.

### 3.2 Example: Aircraft Drag

For an aircraft where drag $D(t) = k \cdot v(t)$ is proportional to speed:

$$v(t) = \int \frac{1}{m} \left[ \text{Thrust}(t) - D(t) \right] dt + v_0$$

The block diagram contains:
- A summation node: $\text{Thrust}(t) - D(t)$
- A gain block: $\frac{1}{m}$
- An integrator: $\frac{1}{s}$
- A feedback path for $D(t) = k \cdot v(t)$

### 3.3 Reduction to Transfer Function

For a standard feedback loop:

$$\frac{X(s)}{R(s)} = \frac{G(s) \cdot C(s)}{1 + G(s) \cdot C(s) \cdot H(s)}$$

> [!important] Loop Reduction Rule
> For any feedback loop, the transfer function is:
> - **Numerator** = forward branch
> - **Denominator** = $1 +$ loop gain (product of all blocks in the loop)
>
> With negative feedback the denominator is $1 + \text{loop}$; with positive feedback it becomes $1 - \text{loop}$.

### 3.4 Laplace Notation in Block Diagrams

When using Laplace transforms:
- Integration becomes $\frac{1}{s}$
- Differentiation becomes $s$
- Arithmetic rules apply where $s$ is treated as a variable

---

## 4. DC Motor Model

A DC motor is modelled as an electromechanical system with two coupled subsystems.

### 4.1 Electrical Subsystem

Using Kirchhoff's voltage law for the armature circuit:

$$V_a - V_R - V_L - V_{emf} = 0$$

$$L_a \dot{I}_a = V_a - R_a I_a - V_{emf}$$

Where:
- $V_a$ = applied motor voltage (input)
- $R_a I_a$ = resistive voltage drop
- $L_a \dot{I}_a$ = inductive voltage
- $V_{emf} = K_{emf} \cdot \omega_m$ = back-EMF (electro-motive force)

### 4.2 Mechanical Subsystem

Euler's 2nd law for the motor inertia:

$$J_m \dot{\omega}_m = K_m I_a - B_m \omega_m - \tau_L$$

Where:
- $J_m$ = mass moment of inertia
- $B_m$ = viscous friction coefficient
- $K_m$ = motor torque constant [Nm/A]
- $K_{emf}$ = back-EMF constant [V/(rad/s)]
- $\tau_L$ = load torque (disturbance)

> [!note] Motor Constants
> In SI units, $K_m$ and $K_{emf}$ are numerically equal: $K_m = K_{emf}$ (Nm/A = V·s/rad).
> Reference: Textbook pages 99–100.

### 4.3 Combined Block Diagram

The full DC motor block diagram couples both subsystems:
- Electrical: $V_a \to$ summation $\to \frac{1}{L_a} \to \frac{1}{s} \to I_a$ with feedback from $R_a$ and $V_{emf}$
- Mechanical: $K_m I_a \to$ summation $\to \frac{1}{J_m} \to \frac{1}{s} \to \omega_m$ with feedback from $B_m$ and $\tau_L$
- Coupling: $V_{emf} = K_{emf} \cdot \omega_m$ feeds back into the electrical subsystem

---

## 5. Control Process Introduction

### 5.1 Heating System Example

A room heating system illustrates the control problem:
- **Control variable (input)**: Valve position $u$ [0–5V]
- **Output to control**: Room temperature $T$
- **Disturbances**: External power loss $P_T$, supplementary sources $P_S$
- **Actuator**: Valve controlling water flow to radiator

### 5.2 Open-Loop vs Closed-Loop

**Open-loop** (no feedback): The controller output depends only on the reference — it cannot account for disturbances or model errors. This is unrealistic for most real systems.

**Closed-loop** (with feedback): A sensor measures the output and feeds it back. The controller acts on the error $e = T_{ref} - T_{measured}$.

> [!success] Benefits of Closed-Loop Control
> - Accurately tracks the reference (setpoint)
> - Compensates for model variations and uncertainties
> - Reduces oscillations and improves stability
> - Rejects or reduces disturbances
> - Improves transient response and system speed

---

## 6. Controller Types

### 6.1 Feed-Forward (FF) Controller

The FF controller uses a known relationship between input and output:

$$u = K_{ff} \cdot (T_{ref} - 10)$$

From calibration data ($u = 0 \Rightarrow T = 10°C$, $u = 5 \Rightarrow T = 30°C$):

$$K_{ff} = \frac{5}{30 - 10} = 0.25$$

| Advantages | Disadvantages |
|------------|---------------|
| Does not introduce instability | Does not account for disturbances |
| Constant $u$ for constant reference | Cannot correct modelling errors |
| Simple structure | No feedback correction |

### 6.2 P-Controller

The proportional controller outputs a signal proportional to the error:

$$u(t) = K_p \cdot e(t) = K_p \cdot (r(t) - y_m(t))$$

**Effect of $K_p$:**

| Higher $K_p$ | Lower $K_p$ |
|--------------|-------------|
| Smaller steady-state error | Larger steady-state error |
| Faster rise time | Slower settling time |
| Risk of overshoot & instability | More stable but less accurate |
| Amplifies measurement noise | Less noise sensitivity |

> [!warning] P-Controller Limitations
> - **Steady-state error**: A P-controller alone often leaves a permanent offset ($T_{measured} = T_{ref} - \frac{u}{K_p}$). As $K_p \to \infty$, the error approaches zero, but this causes instability.
> - **Noise amplification**: Large $K_p$ amplifies sensor noise directly to the actuator.
> - **Instability with delay**: Systems with significant time delays (e.g., heating: valve 1s, radiator 2min, room 15min) can oscillate with high $K_p$.

### 6.3 I-Controller

The integral controller integrates the error over time:

$$u(t) = K_I \int e(t) \, dt, \quad K_I = \frac{K_p}{\tau_i}$$

Where $\tau_i$ is the integrator time constant — the time to approach the desired value.

- **Eliminates steady-state error**: As long as $e(t) \neq 0$, the integral keeps growing
- **Risk**: Can cause instability if $K_I$ is too large (too fast integration)
- **Tuning**: Reduce $K_I$ (increase $\tau_i$) to reduce overshoot at the cost of slower response

### 6.4 PI-Controller

Combines proportional and integral action:

$$u(t) = K_p \left( e(t) + \frac{1}{\tau_i} \int e(t) \, dt \right)$$

> [!tip] Hand-Tuning Recipe for PI
> 1. **Start with P only**: Set $K_p$ for fast response with no overshoot
> 2. **Add I-term**: Set $\tau_i$ to roughly the time it takes the output to reach steady state
> 3. **Refine**:
>    - Decrease $K_p$ → more stable, less overshoot
>    - Increase $K_p$ → faster, more accurate
>    - Decrease $\tau_i$ → removes stationary error faster
>    - Increase $\tau_i$ → more stable system
> 4. A slightly smaller $K_p$ usually allows for a faster $\tau_i$

### 6.5 FF + P Combination

Combining feed-forward with a P-controller gives better disturbance rejection:

$$u = K_{ff}(T_{ref} - 10) + K_p(T_{ref} - T_m)$$

> [!example] Numerical Example
> With $K_{ff} = 0.25$, $K_p = 1$, $T_{ref} = 20°C$, and a 2°C disturbance:
> - **FF only**: $T_m = 18°C$ (2°C error)
> - **FF + P**: $T_m = 19.6°C$ (0.4°C error — much closer to target)

---

## 7. Time-Domain Specifications

Key metrics for evaluating controller performance on a step response:

| Specification | Description |
|---------------|-------------|
| **Rise time** | Time for output to go from 10% to 90% of final value |
| **Overshoot** | How much the output exceeds the final value (%) |
| **Settling time** | Time for the output to stay within a tolerance band |
| **Steady-state error** | Permanent offset between reference and output as $t \to \infty$ |

---

## 8. Ziegler-Nichols Tuning

Systematic methods for initial PID tuning — provides a starting point for further refinement.

### 8.1 Open-Loop Method

Apply a step input to the open-loop system and analyse the response curve:

1. Make a step change in $u(t)$
2. Calculate process gain: $A = \Delta Y / \Delta U$
3. Find the inflection point and draw a tangent
4. Determine time delay $L$ (where tangent crosses initial value)
5. Calculate time constant $\tau$ (at 63% of total change)
6. Slope $R = A / \tau$

The system is approximated as a first-order plus dead time:

$$\frac{Y(s)}{U(s)} = \frac{A \cdot e^{-Ls}}{\tau s + 1}$$

**Ziegler-Nichols Open-Loop Tuning Rules:**

| Controller | $K_p$ | $T_i$ | $T_d$ |
|------------|--------|--------|--------|
| P | $\frac{1}{RL}$ | — | — |
| PI | $\frac{0.9}{RL}$ | $\frac{L}{0.3}$ | — |
| PID | $\frac{1.2}{RL}$ | $2L$ | $0.5L$ |

### 8.2 Closed-Loop Method

Uses the system in closed-loop with only proportional control:

1. Apply a step reference input
2. Start with a low gain $K$ and gradually increase
3. Find **ultimate gain** $K_u$: the gain where the system sustains continuous oscillation
4. Measure the **ultimate period** $P_u$ of the oscillation

**Ziegler-Nichols Closed-Loop Tuning Rules:**

| Controller | $K_p$ | $T_i$ | $T_d$ |
|------------|--------|--------|--------|
| P | $0.5 K_u$ | — | — |
| PI | $0.45 K_u$ | $\frac{P_u}{1.2}$ | — |
| PID | $0.6 K_u$ | $0.5 P_u$ | $0.125 P_u$ |

> [!example] Closed-Loop Example
> Given $K_u = 4$ and $P_u = 3$ s, the PID parameters are:
> - $K_p = 0.6 \times 4 = 2.4$
> - $T_i = 0.5 \times 3 = 1.5$ s
> - $T_d = 0.125 \times 3 = 0.375$ s

> [!warning] Limitations of Ziegler-Nichols
> - Not optimal — lacks generality
> - Open-loop method only works with **open-loop stable** systems
> - Bringing a closed-loop system to marginal stability can be problematic/dangerous
> - Difficult to accurately determine $L$, $\tau$, $R$ from the response curve
> - Best used as a **starting point** for further manual tuning
> - Other tuning rules exist but are dedicated to specific system types

---

## Key Takeaways

1. **Block diagrams** connect physics to math — use standard elements (gain, summation, integrator, branching) to represent system dynamics
2. **Loop reduction**: $\text{TF} = \frac{\text{forward}}{1 + \text{loop}}$ is the fundamental rule
3. **P-control** is simple but has steady-state error and noise/stability trade-offs
4. **I-control** eliminates steady-state error but can introduce overshoot and instability
5. **PI-control** combines both — tune $K_p$ first, then add $\tau_i$
6. **Ziegler-Nichols** gives systematic initial tuning parameters (open-loop or closed-loop method)
7. All tuning methods are starting points — real systems require iterative refinement
