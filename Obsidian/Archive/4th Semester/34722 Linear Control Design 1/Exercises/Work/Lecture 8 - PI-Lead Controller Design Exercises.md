---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise, MATLAB, PI, Lead, controller-design]
date: 2026-03-25
---
# Lecture 8 - PI-Lead Controller Design Exercises

> [!abstract] Overview
> Three in-class exercises building up controller complexity: P → PI → PI-Lead. Each uses a textbook transfer function given on the lecture slides.

> [!info] Files
> - MATLAB scripts: [Day8 folder](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day8/)
> - Exercise templates: `Lecture_08_exercise_1.m`, `Lecture_08_exercise_2.m`, `Lecture_08_exercise_3.m`
> - Solutions: `Lecture_08_exercise_1_solution.m`, `Lecture_08_exercise_2_solution.m`, `Lecture_08_exercise_3_solution.m`

> [!example] Related Materials
> - Lecture slides: [[Lecture_08_PI_LEAD_design.pdf]]
> - REGBOT application: [[Day 8 & 9 - Position Controller Design]]

> [!info] Note
> The transfer functions in Exercises 1–3 are given on the lecture slides. The exercise MATLAB templates have `G = 0*s;` as a placeholder — fill in during the lecture.

---

## Exercise 1: P Controller on a Type-1 System

$$G(s) = \frac{40}{s(s + 10)^2}$$

This system is already **type-1** — there is an integrator ($s$) in the denominator. The poles are at $s = 0, -10, -10$.

### Why Type-1 Matters

The **system type** equals the number of free integrators (poles at $s = 0$) in the open-loop transfer function. For a unit step input, the steady-state error is:

$$e_{ss} = \frac{1}{1 + K_v} \quad \text{where } K_v = \lim_{s \to 0} s \cdot G_{ol}(s)$$

For a type-1 system, $K_v \to \infty$, so $e_{ss} = 0$ — **zero steady-state error with just a P controller**, no PI needed.

### Design Procedure: P Controller for $\gamma_M = 60°$

The goal is to find $K_P$ such that the phase margin is exactly $60°$.

**Step 1:** A phase margin of $60°$ means the phase at the crossover frequency must be $-120°$ (since $\gamma_M = -180° - \angle G(j\omega_c)$). From the Bode plot, find the frequency $\omega_c$ where $\angle G(j\omega_c) = -120°$.

**Step 2:** At this new $\omega_c$, the magnitude $|G(j\omega_c)|$ is not 0 dB. Choose $K_P$ to shift it to 0 dB:

$$K_P = \frac{1}{|G(j\omega_c)|}$$

### MATLAB

```matlab
s = tf('s');
G = 40/(s*(s + 10)^2);

w = linspace(1e-1, 20, 1000);
[M, P, w_out] = bode(G, w);
M = mag2db(squeeze(M));
P = squeeze(P);

kk = find(P <= -120, 1);         % Find where phase = -120 deg
omega_c = w_out(kk);              % New crossover frequency
K_P = db2mag(-M(kk));             % K_P to make magnitude = 0 dB

G_cl = minreal(K_P*G/(1 + K_P*G));
step(G_cl);
stepinfo(G_cl)
```

### Results

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
> For type-1 systems, a simple P controller achieves zero $e_{ss}$ to a step. The only design variable is $K_P$, chosen to meet the phase margin requirement. This is the simplest case — Exercises 2 and 3 address type-0 systems where PI and Lead parts are needed.

---

## Exercise 2: PI Controller on a Type-0 System

$$G(s) = \frac{3.3}{s^3 + 5s^2 + 2.1s + 1}$$

Poles: $s = -4.59$ and $s = -0.205 \pm 0.419j$ (oscillatory pair near the imaginary axis).

### The Problem with P Control on Type-0 Systems

A type-0 system has no free integrator, so with just a P controller, the steady-state error to a step input is:

$$e_{ss} = \frac{1}{1 + K_P \cdot G(0)} \neq 0$$

No matter how large $K_P$ is, there will always be a nonzero $e_{ss}$. To get $e_{ss} = 0$, we need to **add an integrator** — that's what the PI controller does.

### PI Controller Design

The PI transfer function is:

$$C_{PI}(s) = 1 + \frac{1}{\tau_i s} = \frac{\tau_i s + 1}{\tau_i s}$$

The $\frac{1}{\tau_i s}$ term adds a pole at $s = 0$ (integrator) and a zero at $s = -1/\tau_i$. The zero is placed well below $\omega_c$ so it doesn't affect phase margin too much — this is controlled by $N_i$.

### Phase-Balance Design Procedure

**Goal:** Find $\omega_c$ and $\tau_i$ such that $\gamma_M = 60°$.

**Step 1 — PI phase contribution at $\omega_c$:**

The PI controller adds phase at the crossover frequency:

$$\phi_i = -\arctan\left(\frac{1}{N_i}\right)$$

With $N_i = 3$: $\phi_i = -18.43°$ (always negative — PI always costs phase).

**Step 2 — Required plant phase at $\omega_c$:**

For the total phase at $\omega_c$ to give $\gamma_M = 60°$:

$$\angle G(j\omega_c) + \phi_i = -180° + \gamma_M$$

$$\phi_G = -180° + \gamma_M - \phi_i = -180° + 60° - (-18.43°) = -101.57°$$

**Step 3 — Find $\omega_c$ from Bode plot:**

Look up where $\angle G(j\omega) = \phi_G = -101.57°$. This gives the new crossover frequency.

**Step 4 — PI time constant:**

$$\tau_i = \frac{N_i}{\omega_c}$$

The zero is placed at $\omega_c / N_i$, i.e., $N_i$ times below crossover — far enough to keep the phase penalty small.

**Step 5 — Find $K_P$:**

Compute the open-loop $C_{PI}(s) \cdot G(s)$ and find $K_P$ so the magnitude is 0 dB at $\omega_c$:

$$K_P = \frac{1}{|C_{PI}(j\omega_c) \cdot G(j\omega_c)|}$$

### MATLAB

```matlab
s = tf('s');
G = 3.3/(s^3 + 5*s^2 + 2.1*s + 1);

N_i = 3;
gamma_M = 60;

% Step 1-2: Phase contributions
phi_i = rad2deg(-atan(1/N_i));           % PI phase at omega_c
phi_G = -180 + gamma_M - phi_i;          % Required plant phase

% Step 3: Find omega_c from Bode plot
w = linspace(1e-2, 120, 1000);
[M, P, w_out] = bode(G, w);
P = squeeze(P);
i_c = find(P <= phi_G, 1, 'first');
omega_c = w_out(i_c);

% Step 4: PI time constant and transfer function
tau_i = N_i / omega_c;
C_PI = (1 + 1/(tau_i*s));

% Step 5: Proportional gain
G_ol = minreal(C_PI * G);
K_P = 1 / abs(freqresp(G_ol, omega_c));

% Compare P vs PI closed-loop
G_cl_P  = K_P*G / (1 + K_P*G);
G_cl_PI = K_P*C_PI*G / (1 + K_P*C_PI*G);
step(G_cl_PI); hold on; step(G_cl_P); hold off;
legend('PI', 'P');
```

### Why $N_i$ Matters

$N_i$ controls the trade-off between phase penalty and integral action speed:
- **Large $N_i$** (e.g., 10): zero far below $\omega_c$ → small phase penalty, but slow integral action (takes longer to eliminate $e_{ss}$)
- **Small $N_i$** (e.g., 2): zero closer to $\omega_c$ → larger phase penalty (forces lower $\omega_c$), but faster integral correction

### Results

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

> [!warning] PI Trade-off
> Adding PI always costs phase ($\phi_i < 0$), which forces a **lower crossover frequency** compared to P-only. This means slower response. The result: zero $e_{ss}$ but at the cost of speed and settling time. Exercise 3 adds a Lead part to recover this lost speed.

---

## Exercise 3: PI-Lead Controller on a Type-0 System

$$G(s) = \frac{40}{(s+1)(s+10)^2}$$

This is type-0, so PI is needed for zero $e_{ss}$. But PI alone makes the system slow (as seen in Exercise 2). The **Lead compensator** adds positive phase to recover what PI took away.

### Lead Controller

$$C_D(s) = \frac{\tau_d s + 1}{\alpha \tau_d s + 1}, \quad 0 < \alpha < 1$$

The Lead adds a **zero** at $s = -1/\tau_d$ and a **pole** at $s = -1/(\alpha \tau_d)$. Since $\alpha < 1$, the pole is further left than the zero, so in the frequency range between them the Lead contributes **positive phase**.

The maximum phase boost from the Lead is:

$$\phi_m = \arcsin\left(\frac{1 - \alpha}{1 + \alpha}\right)$$

With $\alpha = 0.3$: $\phi_m = +32.58°$.

### Phase-Balance with PI + Lead

Now the balance equation includes both contributions:

$$\angle G(j\omega_c) + \phi_i + \phi_m = -180° + \gamma_M$$

$$\phi_G = -180° + \gamma_M - \phi_i - \phi_m$$

The Lead adds positive phase ($\phi_m > 0$), so the required plant phase $\phi_G$ becomes **more negative** — meaning we can push $\omega_c$ higher. This is the whole point: Lead lets us have a faster system while keeping the desired phase margin.

### Design Procedure

**Steps 1–4** are the same as Exercise 2 (PI design), but with $\phi_m$ included:

$$\phi_G = -180° + \gamma_M - \phi_i - \phi_m$$

**Step 5 — Lead time constant:**

$$\tau_d = \frac{1}{\omega_c \sqrt{\alpha}}$$

**Step 6 — Find $K_P$:**

$$K_P = \frac{1}{|C_{PI}(j\omega_c) \cdot C_D(j\omega_c) \cdot G(j\omega_c)|}$$

### Two Closed-Loop Architectures

The Lead can be placed in either the **forward** or **feedback** path. The open-loop (and therefore stability margins) is the same, but the closed-loop differs:

**a) Lead in forward path:**

$$G_{cl}(s) = \frac{K_P \cdot C_{PI}(s) \cdot C_D(s) \cdot G(s)}{1 + K_P \cdot C_{PI}(s) \cdot C_D(s) \cdot G(s)}$$

The Lead zero appears in the numerator → faster rise time, higher bandwidth, but more overshoot and larger control signals.

**b) Lead in feedback path:**

$$G_{cl}(s) = \frac{K_P \cdot C_{PI}(s) \cdot G(s)}{1 + K_P \cdot C_{PI}(s) \cdot C_D(s) \cdot G(s)}$$

The Lead zero is **not** in the numerator → smoother response, less overshoot, lower bandwidth.

### Results

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
> - **PI-Lead (forward):** fastest response (0.22s rise), good for reference tracking. But amplifies high-frequency reference content → larger control signals.
> - **PI-Lead (feedback):** smoothest response (1.3% overshoot), best for disturbance rejection. Lower bandwidth (3.1 vs 10.2 rad/s) means less aggressive control effort.
> - For the REGBOT, we use **Lead in feedback** to avoid aggressive motor voltages.

---

> [!nav]
> [[Day 8 & 9 - Position Controller Design|→ REGBOT Position Controller]]
>
> [[34722 Linear Control Design 1|34722 Home]]
