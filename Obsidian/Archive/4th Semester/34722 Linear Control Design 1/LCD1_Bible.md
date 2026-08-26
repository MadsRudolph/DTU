# 34722 Linear Control Design 1 — The LCD1 Bible

This comprehensive study guide distills the 12 core lectures into the essential concepts, equations, and problem-solving techniques for the exam. Each section includes a solved example and a practice problem for you to solve at the board.

## Table of Contents
- [Chapter 1: System Modeling & Laplace (Lectures 2, 3, 5)](#chapter-1-system-modeling--laplace-lectures-2-3-5)
- [Chapter 2: Time & Frequency Domain Specs (Lecture 4)](#chapter-2-time--frequency-domain-specs-lecture-4)
- [Chapter 3: Stability & Nyquist (Lectures 6, 7, 10)](#chapter-3-stability--nyquist-lectures-6-7-10)
- [Chapter 4: Controller Design (PI-Lead) (Lectures 8, 9)](#chapter-4-controller-design-pi-lead-lectures-8-9)
- [Chapter 5: Steady-State Error & Disturbances (Lectures 11, 12)](#chapter-5-steady-state-error--disturbances-lectures-11-12)

---

## Chapter 1: System Modeling & Laplace (Lectures 2, 3, 5)

### Core Concepts
- **Transfer Functions (TF):** The ratio of the Laplace transform of the output to the input, assuming zero initial conditions: $H(s) = Y(s)/U(s)$.
- **Block Diagram Reduction:**
  - **Series:** $H = A \cdot B$
  - **Parallel:** $H = A + B$ (signals summed at a junction add, never multiply).
  - **Feedback Loop:** For forward path $G$ and feedback path $H$ (negative feedback), the closed-loop TF is $T = \frac{G}{1 + GH}$.
- **Linearization:** Non-linear systems $\dot{x} = f(x, u)$ must be linearized around an equilibrium point $(x_0, u_0)$. The small-signal model is $\Delta\dot{x} \approx A\Delta x + B\Delta u$, where $A$ and $B$ are the Jacobian matrices evaluated at the equilibrium.
- **Initial and Final Value Theorems:**
  - IVT: $y(0^+) = \lim_{s \to \infty} s Y(s)$
  - FVT: $y(\infty) = \lim_{s \to 0} s Y(s)$. FVT is only valid if all poles of $sY(s)$ are in the strictly open left half-plane (no unstable or purely oscillating signals).

### Solved Example
**Problem:** A forward path $A \cdot B$ has two feedback taps from the output, $C$ and $D$, summed at one junction and fed back negatively around $B$. Reduce the diagram to one transfer function.
**Solution:**
1. Signals summed at a junction are a PARALLEL connection, so the two taps combine as $(C + D)$ — not the product.
2. The inner loop closes around $B$ only. Applying the feedback rule gives $B / (1 + B(C+D))$.
3. $A$ is in series outside the loop, giving the final transfer function $H = \frac{AB}{1 + B(C+D)}$.

### Practice Problem (Your Turn!)
**Question:** What does it mean to linearize a nonlinear model, and when is the linear model valid?
*(Hint: Think about equilibrium points, Jacobians, and small-signal deviations.)*

---

## Chapter 2: Time & Frequency Domain Specs (Lecture 4)

### Core Concepts
- **Standard 2nd-Order System:** 
  $G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$
- **Damping Ratio ($\zeta$) and Overshoot ($M_p$):**
  $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ and $\zeta = \frac{\ln(1/M_p)}{\sqrt{\pi^2 + \ln^2(1/M_p)}}$
  *Quick values:* $\zeta=0.5 \Rightarrow M_p \approx 16\%$, $\zeta=0.7 \Rightarrow M_p \approx 5\%$, $\zeta=1.0 \Rightarrow M_p = 0\%$.
- **Time-Domain Specs:**
  - Damped frequency: $\omega_d = \omega_n\sqrt{1-\zeta^2}$
  - Settling time (2%): $t_s \approx \frac{4}{\zeta\omega_n}$ (The envelope is $e^{-\zeta\omega_n t}$).
  - Rise time: $t_r \approx \frac{1.8}{\omega_n}$.
- **Right-Half-Plane (RHP) Zeros:** A system with an RHP zero will initially move in the wrong direction (undershoot) before rising. It is non-minimum phase.

### Solved Example
**Problem:** A closed loop has 10% overshoot and $\omega_n = 5$ rad/s. What is the damped frequency, and why can it never equal $\omega_n$?
**Solution:**
1. From $M_p = 0.10$, we find $\zeta \approx 0.59$.
2. The damped frequency is $\omega_d = \omega_n\sqrt{1-\zeta^2} = 5 \cdot 0.807 \approx 4.0$ rad/s.
3. $\omega_d = \omega_n$ would require $\zeta = 0$ (zero damping, 100% overshoot), contradicting the 10% overshoot. Any finite overshoot means $\omega_d$ is strictly below $\omega_n$.

### Practice Problem (Your Turn!)
**Question:** A step response shows 1.23% overshoot and settles (2%) in 1 s. Find $\zeta$ and $\omega_n$, and dismiss the impossible option "$\zeta = -0.8$".

---

## Chapter 3: Stability & Nyquist (Lectures 6, 7, 10)

### Core Concepts
- **Bode Plots:**
  - Integrator ($1/s$): $-20$ dB/dec initial slope, $-90^\circ$ phase everywhere.
  - Simple Pole ($1/(s/p + 1)$): Adds $-20$ dB/dec slope and $-45^\circ$ phase at the corner $\omega=p$. Phase goes from $0$ to $-90^\circ$.
  - RHP Zero: Magnitude rises $+20$ dB/dec (like a normal zero), but phase SUBTRACTS $90^\circ$ (like a pole).
- **Stability Margins:**
  - Gain Margin (GM): Distance to $-1$ in gain at the phase-crossover frequency ($\angle G = -180^\circ$). $GM = 1/|G(j\omega_{pc})|$.
  - Phase Margin ($\gamma_M$): Extra phase lag before instability at the gain-crossover frequency ($|G| = 1$). $\gamma_M = 180^\circ + \angle G(j\omega_{gc})$.
- **Nyquist Criterion ($Z = N + P$):**
  - $Z$ = closed-loop RHP poles (must be 0 for stability).
  - $P$ = open-loop RHP poles.
  - $N$ = clockwise encirclements of $-1$.
  - For a stable plant ($P=0$), the plot must not encircle $-1$. For an unstable plant ($P>0$), it must encircle $-1$ counter-clockwise exactly $P$ times ($N=-P$).

### Solved Example
**Problem:** For a stable open-loop plant whose Nyquist plot crosses the negative real axis at $-0.125$, for which gains $K$ is the closed loop stable? Why does gain "scale" the plot?
**Solution:**
1. Gain $K$ multiplies $G(j\omega)$, scaling the entire Nyquist plot radially. The new crossing is at $-0.125K$.
2. Since the plant is stable ($P=0$), we must not encircle $-1$. Thus, the crossing must stay to the right of $-1$: $-0.125K > -1 \Rightarrow K < 8$. 
3. The system is stable for $0 < K < 8$. The GM is $1/0.125 = 8$, matching the critical gain.

### Practice Problem (Your Turn!)
**Question:** Using a Routh argument, for which $K$ is $s^3 + s^2 + 10s + K$ stable?

---

## Chapter 4: Controller Design (PI-Lead) (Lectures 8, 9)

### Core Concepts
- **Phase-Budget Equation:** At the crossover frequency $\omega_c$:
  $-180^\circ + \gamma_M = \angle G(j\omega_c) + \phi_{Lead} + \phi_{PI}$
- **Proportional (P) Design:** Gain moves no phase! First, find the $\omega_c$ where the plant phase $\angle G = -180^\circ + \gamma_M$. Then set $K_P = 1/|G(j\omega_c)|$.
- **Lead Compensator:** $C_{Lead} = K_c \frac{s+z}{s+p}$ ($z < p$). 
  - Adds a positive phase bump to improve margins and speed.
  - The maximum phase boost is $\phi_{max} = \arcsin\frac{\alpha-1}{\alpha+1}$ where $\alpha = p/z > 1$.
  - The peak occurs at the geometric mean $\omega_c = \sqrt{zp}$.
- **PI Compensator:** $C_{PI} = K_P \frac{\tau_i s + 1}{\tau_i s}$.
  - Adds an integrator to kill steady-state step error.
  - Costs phase lag at crossover: $\phi_{PI} = \arctan(N_i) - 90^\circ$, where the zero is at $\omega_c/N_i$.

### Solved Example
**Problem:** Design a pure P-controller for a $45^\circ$ phase margin on $G = 1/(s(s+15))$.
**Solution:**
1. Phase pins the crossover (gain moves no phase!): $\omega_c$ must sit where $\angle G = -180^\circ + 45^\circ = -135^\circ$.
2. $\angle G = -90^\circ - \arctan(\omega/15) = -135^\circ \Rightarrow \arctan(\omega/15) = 45^\circ \Rightarrow \omega_c = 15$ rad/s.
3. Gain sets the crossover: $K_P = 1/|G(j15)| = 15 \cdot |j15+15| = 15 \cdot 15\sqrt{2} \approx 318$.

### Practice Problem (Your Turn!)
**Question:** In a PI-Lead controller, what is the PI part for, what does it cost, and how do you place its zero?

---

## Chapter 5: Steady-State Error & Disturbances (Lectures 11, 12)

### Core Concepts
- **System Type:** The number of integrators (poles at the origin) in the open-loop transfer function $L(s)$.
- **Steady-State Error (Unity Feedback):** $e_{ss} = \lim_{s \to 0} s \frac{R(s)}{1 + L(s)}$.
  - **Type 0:** Step error $= \frac{1}{1+K_p}$ ($K_p = L(0)$).
  - **Type 1:** Step error $= 0$, Ramp error $= \frac{1}{K_v}$.
- **Sensitivity ($S$) & Complementary Sensitivity ($T$):**
  - $S = \frac{1}{1+L}$: Maps reference to error, and output disturbances to output.
  - $T = \frac{L}{1+L}$: Maps reference to output.
  - $S + T = 1$ everywhere. Design pushes $|S|$ down at low frequencies (tracking) and $|T|$ down at high frequencies (noise rejection).
- **Disturbance Rejection:** If an integrator is *before* the disturbance injection point (e.g., in the controller), step disturbances are perfectly rejected in steady-state. If the integrator is *after* (e.g., in the plant), it cannot reject it perfectly.

### Solved Example
**Problem:** $C(0) \cdot G(0) = 0.03$ in a unity type-0 loop and the reference is a step of size 30. What is the steady-state error?
**Solution:**
1. For a step size of 30, $R(s) = 30/s$.
2. $e_{ss} = 30 \cdot \frac{1}{1 + L(0)} = 30 \cdot \frac{1}{1 + 0.03}$.
3. $e_{ss} = 30 / 1.03 \approx 29.1$. (Trap: Don't forget the $1+$ in the denominator!)

### Practice Problem (Your Turn!)
**Question:** The closed-loop $|T(j\omega)|$ is 0 dB at low frequency. What does that say about the steady-state error — and does lower bandwidth mean a faster system?

---
*Good luck with the exam preparation! Focus on the quick derivation loops rather than memorizing long texts.*
