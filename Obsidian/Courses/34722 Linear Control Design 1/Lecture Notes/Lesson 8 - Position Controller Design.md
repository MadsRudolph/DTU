---
course: "34722"
course-name: "Linear Control Design 1"
type: lecture-note
lesson: 8
tags: [LCD, lecture]
date: 2026-03-25
---
# Lesson 8 - Position Controller Design (PILead)

> [!abstract] Lecture Overview
> Lesson 8/13 — Teacher: Dimitrios Papageorgiou
> Topics: Systematic PILead controller design using the phase balance equation. Covers P, PI, and PILead (PID with filtered derivative) design in the frequency domain.
> "Probably the most important lecture of the class" — this lecture lays the foundation for all controller designs revisited throughout the rest of the course.

> [!example] Related Materials
> - Slides: [[Lecture_08_PI_LEAD_design.pdf]]
> - Exercise: [[Day 8 & 9 - Position Controller Design]]
> - MATLAB scripts: `Lecture_08_exercise_1.m`, `Lecture_08_exercise_2.m`, `Lecture_08_exercise_3.m`
> - Previous: [[Lesson 4 - Frequency Domain and Time Analysis]]

---

## 1. Closed-Loop Fundamentals (Recap)

### 1.1 Block Diagram Setup

The benchmark block diagram used throughout this lecture:

$$R(s) \;\longrightarrow\; \boxed{\sum} \;\longrightarrow\; e(s) \;\longrightarrow\; \boxed{K(s)} \;\longrightarrow\; \boxed{G(s)} \;\longrightarrow\; Y(s)$$

with feedback from $Y(s)$ back to the summation node.

- $G(s)$: plant transfer function (assumed known, e.g. from system identification)
- $K(s)$: controller (three variations today: P, PI, PILead)
- We assume $G(s)$ is **open-loop stable** (all poles in left half-plane), or at worst has **one pole at the origin** (pure integrator)

### 1.2 Key Transfer Functions

| Transfer function | Formula |
|---|---|
| **Loop (open-loop)** $G_{OL}(s)$ | $K(s) \cdot G(s)$ |
| **Closed-loop** (reference to output) | $\dfrac{K(s)\,G(s)}{1 + K(s)\,G(s)}$ |
| **Error** (reference to error) | $\dfrac{1}{1 + K(s)\,G(s)}$ |

> [!tip] Same denominator
> Both the closed-loop and error transfer functions share the same denominator $1 + K(s)G(s)$. This must be the case because the stability properties of a closed-loop system are unique — they cannot depend on which input-output pair you examine. The **forward branch** changes, but the **characteristic polynomial** (denominator) is always the same.

**Useful identity:** The error transfer function equals $1 - G_{CL}(s)$, since $e = r - y = r - G_{CL}\,r$.

> [!warning] Exam tip
> If asked to identify which transfer function is the error TF from a list, **exclude any that have different poles** from the closed-loop TF. In the same closed-loop system, all transfer functions must have identical poles.

---

## 2. Proportional (P) Controller Design

### 2.1 Setup

The simplest controller: $K(s) = K_p$ (just a gain).

$$G_{OL}(s) = K_p \cdot G(s), \qquad G_{CL}(s) = \frac{K_p\,G(s)}{1 + K_p\,G(s)}, \qquad G_e(s) = \frac{1}{1 + K_p\,G(s)}$$

### 2.2 Effect on Bode Plot

Multiplying by $K_p$ shifts the magnitude plot **vertically** by $20\log_{10}(K_p)$ dB. The **phase is unchanged**. This moves the crossover frequency to the right (for $K_p > 1$) or left (for $K_p < 1$).

**Trade-off:** Increasing $K_p$:
- Reduces steady-state error (good)
- Moves crossover frequency rightward toward higher frequencies where phase drops (bad)
- Decreases phase margin $\Rightarrow$ less robustness, more oscillations

### 2.3 Steady-State Error with P Controller

Using the **Final Value Theorem**: for a unit step input to a stable system,

$$e_{ss} = \lim_{s \to 0} s \cdot G_e(s) \cdot \frac{1}{s} = G_e(0) = \frac{1}{1 + K_p \cdot G(0)}$$

> [!important] Key result
> For a **stable system** (finite $G(0)$), a P controller can make the steady-state error small but **never zero** (that would require $K_p \to \infty$).
>
> **Exception:** If the plant already contains an integrator ($G(0) = \infty$), then even a P controller achieves zero steady-state error.

### 2.4 The Phase Balance Equation (P Controller)

Given a **phase margin specification** $\gamma_M$ (e.g., $60^\circ$):

$$\boxed{\angle G(j\omega_c) = \gamma_M - \pi}$$

This is the simplest form of the phase balance equation (slide 7). Since the P controller is just a gain, it contributes no phase.

**Design procedure:**
1. Compute the required phase: $\angle G(j\omega_c^{\text{new}}) = \gamma_M - 180^\circ$
2. Go to the Bode phase plot of $G(s)$ and find the frequency $\omega_c^{\text{new}}$ where this phase occurs
3. Read the magnitude $|G(j\omega_c^{\text{new}})|$ in dB at that frequency
4. Set $K_p$ so that the magnitude becomes 0 dB at $\omega_c^{\text{new}}$:

$$K_p = \frac{1}{|G(j\omega_c^{\text{new}})|}$$

or equivalently: $K_p[\text{dB}] = -|G(j\omega_c^{\text{new}})|[\text{dB}]$

> [!warning] Units
> Don't use $K_p$ in dB in your controller! Convert: $K_p = 10^{K_p[\text{dB}]/20}$

### 2.5 Example 1: P Controller for a Stable System

**System:** $G(s) = \dfrac{3.3}{s^3 + 5s^2 + 2.1s + 1}$ (3rd order, stable — $G_{DC} = G(0) = 3.3$)

**Specification:** $\gamma_M = 60^\circ$

1. Phase balance: $\angle G(j\omega_c) = -180^\circ + 60^\circ = -120^\circ$
2. From Bode plot: $\omega_c = 0.56$ rad/s
3. Magnitude at $\omega_c$: $-9.1$ dB (too high — need to reduce!)
4. $K_P = 10^{-9.1/20} = 0.3508$

**Results:**
- $G_{CL}(s) = \dfrac{0.3508\,G(s)}{1 + 0.3508\,G(s)}$
- Static error: $e_{ss} = \dfrac{1}{1 + 0.3508 \times 3.3} = 0.4635$ (46% error!)
- Step response settles to about 0.54 instead of 1

**Observation:** Increasing $K_P$ reduces steady-state error but increases oscillations (less phase margin). On the Nyquist plot, larger $K_P$ values push the curve closer to the $-1$ point.

| $K_P$ | $e_{ss}$ |
|---|---|
| 0.1 | 0.75 (75%) |
| 0.2 | 0.60 (60%) |
| 0.4 | 0.43 (43%) |
| 0.5 | 0.38 (38%) |
| 1.0 | 0.23 (23%) |

![[Lecture_08_PI_LEAD_design.pdf#page=9]]

### 2.6 Example 2: P Controller for a System with Integrator

**System:** $G(s) = \dfrac{40}{s(s+10)^2}$ (3rd order, marginally stable — pole at origin)

**Specification:** $\gamma_M = 60^\circ$

1. Phase balance: $\angle G(j\omega_c) = -120^\circ$
2. From Bode plot: $\omega_c^{\text{new}} = 2.68959$ rad/s
3. Magnitude at $\omega_c$: $-17.159$ dB
4. $K_P = 10^{17.159/20} = 7.21$

**Results:**
- Poles: $[0, -10, -10]$, no zeros
- $e_{ss} = 0$ (because $G(0) = \infty$ due to the integrator!)
- Overshoot: $\approx 7.88\%$, Rise time: 0.45 s, Settling time: 1.41 s

> [!important] Why zero steady-state error with just P?
> The plant itself contains a pure integrator ($1/s$). This means $G(0) = \infty$, so $e_{ss} = 1/(1 + K_P \cdot \infty) = 0$. You do **not** need a PI controller if the system already has an integrator. But for stable systems (finite $G(0)$), P alone cannot achieve zero error.

> [!tip] Useful MATLAB commands
> ```matlab
> s = tf('s');
> G = 40 / (s*(s+10)^2);
> Kp = 7.21;
> G_cl = Kp*G / (1 + Kp*G);
> G_e = 1 / (1 + Kp*G);
> step(G_cl, 0:0.01:5);    % step response
> stepinfo(G_cl)            % overshoot, rise time, etc.
> ess = freqresp(s*G_e*1/s, 0);  % steady-state error
> ```

![[Lecture_08_PI_LEAD_design.pdf#page=13]]

---

## 3. Proportional-Integral (PI) Controller Design

### 3.1 Motivation: Eliminating Steady-State Error

For stable systems without a built-in integrator, P control always leaves a nonzero steady-state error. The solution: **add an integrator to the controller**.

### 3.2 Pure Integrator — The Problem

A pure integrator $1/s$ in the controller:
- Gives infinite gain at DC ($\omega = 0$) $\Rightarrow$ kills steady-state error
- But introduces a **permanent $-90^\circ$ phase penalty** across all frequencies
- This eats into phase margin, hurting stability

### 3.3 The PI Transfer Function

To limit the phase damage, add a **zero** after the integrator pole:

$$C_{PI}(s) = 1 + \frac{1}{\tau_i s} = \frac{\tau_i s + 1}{\tau_i s}$$

- **Pole** at $s = 0$ (the integrator — always at origin)
- **Zero** at $s = -1/\tau_i$, i.e. at frequency $\omega_i = 1/\tau_i$ (chosen by the designer)

**Implementation:** The PI controller can be realized as two parallel paths: the error passes through $(1/\tau_i) \cdot (1/s)$ (the integral path) and is added to the direct error signal (the proportional path).

![[Lecture_08_PI_LEAD_design.pdf#page=14]]

**What this achieves:** At low frequencies, acts like a pure integrator (infinite gain, kills steady-state error). At frequencies above $\omega_i = 1/\tau_i$, the zero cancels the pole's phase penalty, so the PI acts as if it's not there. This is visible on the Bode plot: the PI starts with $-90^\circ$ phase and $-20$ dB/decade slope, then flattens out after the break frequency $\omega_i$.

![[Lecture_08_PI_LEAD_design.pdf#page=15]]

### 3.4 The $N_i$ Parameter

$$N_i = \frac{\omega_c^{\text{new}}}{\omega_i} = \frac{\omega_c^{\text{new}}}{1/\tau_i} = \omega_c^{\text{new}} \cdot \tau_i$$

$N_i$ is the ratio of the new crossover frequency to the zero frequency of the PI. It controls **how far before** the crossover frequency the zero kicks in:

| $N_i$ | Zero location | Behavior |
|---|---|---|
| Large (e.g. 90) | Very far left of $\omega_c$ | Phase penalty cancelled early $\Rightarrow$ good phase margin, but slow error elimination |
| Small (e.g. 2) | Close to $\omega_c$ | Prolonged high gains $\Rightarrow$ fast error elimination, but $-90^\circ$ penalty persists near $\omega_c$ $\Rightarrow$ poor phase margin |

**Good starting point:** $N_i = 3$

### 3.5 Phase Contribution of PI at Crossover

$$\phi_{PI} = -\arctan\left(\frac{1}{N_i}\right) \quad \text{(in radians — convert to degrees!)}$$

For $N_i = 3$: $\phi_{PI} = -\arctan(1/3) \approx -0.32$ rad $\approx -18.4^\circ$

### 3.6 Phase Balance Equation (PI Controller)

The open-loop phase at the new crossover frequency is the sum of the plant phase and the PI phase:

$$\angle G_{OL}(j\omega_c) = \angle G(j\omega_c) + \angle C_{PI}(j\omega_c)$$

For the desired phase margin $\gamma_M$, we need $\angle G_{OL}(j\omega_c) = -\pi + \gamma_M$, so:

$$-\pi + \gamma_M = \angle G(j\omega_c) - \arctan\left(\frac{1}{N_i}\right)$$

Rearranging (this is the **phase balance equation** from slide 19):

$$\boxed{\angle G(j\omega_c) = \gamma_M - \pi + \arctan\left(\frac{1}{N_i}\right)}$$

> [!warning] Radians vs Degrees
> The $\arctan$ formula gives radians. The Bode plot shows degrees. **Never mix them.** This is a popular exam pitfall — multiple choice options often include the result with wrong unit conversion.

### 3.7 PI Design Procedure

1. Choose $N_i$ (start with 3)
2. Calculate $\phi_{PI} = -\arctan(1/N_i)$, convert to degrees
3. Phase balance: $\angle G(j\omega_c) = -180^\circ + \phi_m - \phi_{PI}$
4. Find $\omega_c^{\text{new}}$ from Bode phase plot of $G(s)$
5. Calculate $\tau_i = N_i / \omega_c^{\text{new}}$, which fully defines the PI transfer function
6. Form the open-loop: $K_{PI}(s) \cdot G(s)$ and evaluate its magnitude at $\omega_c^{\text{new}}$
7. Set $K_p = 1 / |K_{PI}(j\omega_c) \cdot G(j\omega_c)|$

### 3.8 Example: PI Controller Design

**System:** $G(s) = \dfrac{3.3}{s^3 + 5s^2 + 2.1s + 1}$ (3rd order, stable)

**Specification:** $\gamma_M = 60^\circ$, $N_i = 3$

**Poles:** $[-4.5899,\; -0.205 \pm j0.4193]$ — all in left half-plane, so stable.

1. Phase contribution: $\varphi_i = -\arctan(1/3) = -0.3218$ rad $= -18.4349^\circ$
2. Phase balance: $\angle G(j\omega_c) = 60^\circ + 18.4349^\circ - 180^\circ = -101.565^\circ$
3. From Bode plot: $\omega_c = 0.49044$ rad/s
4. $\tau_i = N_i / \omega_c = 3 / 0.49044 = 6.117$ s
5. $K_P = \dfrac{1}{|C_{PI}(j\omega_c) \cdot G(j\omega_c)|} = 0.2686$

**Full PI controller:** $C_{PI}(s) = 0.2686 \cdot \left(1 + \dfrac{1}{9.52s}\right)$, where $\tau_i \cdot K_P$ gives the effective integrator time constant.

The PI controller **eliminates steady-state error** but introduces significant overshoot compared to P-only.

![[Lecture_08_PI_LEAD_design.pdf#page=17]]

### 3.9 Effect of $N_i$ on PI Performance

The slides show four cases comparing different $N_i$ values:

| $N_i$ | PI zero location | Behavior |
|---|---|---|
| 90 | Very far left | PI effect cancelled very early, good phase margin, slow error correction |
| 18 | Moderately left | Moderate balance |
| 8 | Closer to $\omega_c$ | More aggressive, faster error kill, reduced phase margin |
| 3 | Near $\omega_c$ | Most aggressive, fastest error correction, least phase margin |

![[Lecture_08_PI_LEAD_design.pdf#page=18]]

---

## 4. PILead Controller Design (The "D" Part)

### 4.1 Motivation: Recovering Phase Margin

The PI controller introduces a phase penalty near the crossover frequency. If the original system already had a tight phase margin, the PI penalty makes things worse. We need a component that **adds positive phase** near $\omega_c$.

### 4.2 Why Not a Pure Derivative?

A pure zero ($\tau_d s + 1$) would:
- Add $+90^\circ$ phase (good)
- But amplify high-frequency signals (noise) without bound (bad)

### 4.3 The Lead Part Transfer Function

$$K_{\text{lead}}(s) = \frac{\tau_d s + 1}{\alpha \tau_d s + 1}$$

- **Zero** at $s = -1/\tau_d$
- **Pole** at $s = -1/(\alpha\tau_d)$, where $0 < \alpha \ll 1$

Since $\alpha < 1$, the pole is at a higher frequency than the zero. This creates a **phase bump** between the zero and pole frequencies:
- Below the zero: no effect
- Between zero and pole: phase increases (the useful part)
- Above the pole: phase and amplitude effects cancel out

> [!tip] Relationship to PID
> The lead part is essentially a **filtered derivative** — it's the D in PID but with a low-pass filter ($1/(\alpha\tau_d s + 1)$) to prevent noise amplification. This is why the controller is called PI**Lead** rather than PID.

### 4.4 Phase and Amplitude Contribution of the Lead Part

The **maximum positive phase shift** occurs at frequency $\omega_m = \dfrac{1}{\tau_d\sqrt{\alpha}}$:

$$\varphi_m = \arctan\left(\frac{1-\alpha}{2\sqrt{\alpha}}\right) = \arcsin\left(\frac{1 - \alpha}{1 + \alpha}\right) \quad \text{(in radians — convert to degrees!)}$$

This is always **positive** — the lead part adds phase at the crossover frequency.

The **amplitude contribution** (not in dB) at $\omega_m$ is:

$$|C_D(j\omega_m)| = \frac{1}{\sqrt{\alpha}}$$

For $\alpha = 0.1$: $\varphi_m = \arcsin(0.9/1.1) \approx 54.9^\circ$, amplitude $= 1/\sqrt{0.1} \approx 3.16$ ($\approx 10$ dB)
For $\alpha = 0.3$: $\varphi_m = \arcsin(0.7/1.3) = 0.5686$ rad $= 32.579^\circ$, amplitude $= 1/\sqrt{0.3} \approx 1.83$ ($\approx 5.2$ dB)

![[Lecture_08_PI_LEAD_design.pdf#page=24]]

### 4.5 Calculating Lead Parameters from $\omega_c$

The key insight: place the **maximum phase bump** exactly at the new crossover frequency. So:

$$\omega_m = \omega_c^{\text{new}} = \frac{1}{\tau_d \sqrt{\alpha}}$$

Therefore:

$$\tau_d = \frac{1}{\omega_c^{\text{new}} \sqrt{\alpha}}$$

### 4.6 Phase Balance Equation (PILead Controller)

Now the open-loop includes three components: $G_{OL} = K_P \cdot C_{PI} \cdot C_D \cdot G$. The phase balance at $\omega_c$:

$$-\pi + \gamma_M = \angle G(j\omega_c) - \arctan\left(\frac{1}{N_i}\right) + \arcsin\left(\frac{1-\alpha}{1+\alpha}\right)$$

Rearranging (the **phase balance equation** from slide 25):

$$\boxed{\angle G(j\omega_c) = \gamma_M - \arcsin\left(\frac{1-\alpha}{1+\alpha}\right) - \pi + \arctan\left(\frac{1}{N_i}\right)}$$

### 4.7 Full PILead Design Procedure — Cookbook Recipe (Slide 31)

**Given:** A plant $G(s)$.

> [!abstract] Cookbook Recipe
> **Step 1:** Select $\gamma_M$, $N_i$, $\alpha$ (see design guidelines table in Section 5)
>
> **Step 2:** Calculate $\varphi_i$ and $\varphi_m$ (remember to convert to degrees!):
> $$\varphi_i = -\arctan\left(\frac{1}{N_i}\right) \qquad \varphi_m = \arcsin\left(\frac{1-\alpha}{1+\alpha}\right)$$
>
> **Step 3:** Calculate the phase of $G(s)$ at the new crossover frequency from the phase balance equation:
> $$\varphi_G \triangleq \gamma_M - \varphi_i - 180^\circ - \varphi_m$$
>
> **Step 4:** Find $\omega_c$ from the Bode plot of $G(s)$ as the frequency at which $\angle G(j\omega_c) = \varphi_G$
>
> **Step 5:** Find the remaining parameters $\tau_i$, $\tau_d$, $K_P$ from:
> $$\tau_d = \frac{1}{\omega_c\sqrt{\alpha}}, \quad \tau_i = N_i \frac{1}{\omega_c}, \quad K_P = \frac{1}{\left|C_{PI}(s) \cdot C_D(s) \cdot G(s)\right|}\bigg|_{s=j\omega_c}$$
>
> **Step 6:** Plot the step response of the closed-loop system and possibly iterate with new $\gamma_M$, $N_i$, $\alpha$.

### 4.8 Example: PILead Controller Design

**System:** $G(s) = \dfrac{40}{(s+1)(s+10)^2}$ (3rd order, stable)

**Specification:** $\gamma_M = 60^\circ$, $N_i = 3$, $\alpha = 0.3$

1. **PI phase contribution:** $\varphi_i = -\arctan(1/3) = -0.3218$ rad $= -18.4349^\circ$
2. **Lead phase contribution:** $\varphi_m = \arcsin(0.7/1.3) = 0.5686$ rad $= 32.579^\circ$
3. **Phase balance:** $\angle G(j\omega_c) = 60^\circ + 18.4349^\circ - 180^\circ - 32.579^\circ = -134.144^\circ$
4. **From Bode plot:** $\omega_c = 5.29484$ rad/s
5. **Controller parameters:**
   - $\tau_d = \dfrac{1}{\omega_c\sqrt{\alpha}} = \dfrac{1}{5.29484 \cdot \sqrt{0.3}} = 0.3448$
   - $\tau_i = N_i \cdot \dfrac{1}{\omega_c} = 3 \cdot \dfrac{1}{5.29484} = 0.5666$
   - $K_P = \dfrac{1}{|C_{PI}(j\omega_c) \cdot C_D(j\omega_c) \cdot G(j\omega_c)|} = 8.9622$

![[Lecture_08_PI_LEAD_design.pdf#page=30]]

**Step response comparison (slide 30):**
- **P only (yellow, dotted):** does not reach 1 (steady-state error), some overshoot
- **PI (red, dotted):** reaches 1 (no steady-state error), but large overshoot (~40%)
- **PILead (blue, solid):** reaches 1, much less overshoot
- **PILead with Lead in feedback (magenta):** slowest but smoothest response

> [!info] Teaser: Lead in the feedback path
> If the lead part $C_D(s)$ is placed in the **feedback branch** instead of the forward path, the response is slightly slower but significantly smoother — it helps reduce overshoot and noise effects. This will be explained in a future lecture.

---

## 5. Design Guidelines (Lookup Table from Slide 32)

| Parameter | Large value | Small value | Starting point |
|---|---|---|---|
| $\gamma_M$ | Robustness, small overshoot | Sensitivity to disturbances, large overshoot | $60^\circ$ (must be positive for stability) |
| $N_i$ | Small negative phase shift (less overshoot), but slow error correction | Large negative phase shift (more overshoot), but fast error correction | $3$ (range: $[2, 10]$) |
| $\alpha$ | Small positive phase shift (smaller phase margin, more overshoot), large settling time, but less noise amplification | Large positive phase shift (greater phase margin, less overshoot), small settling time, but high noise amplification | $0.2$ (range: $[0.02, 1]$) |

> [!tip] Iterative design
> These are starting points, not gospel. After the first design, plot the step response and evaluate overshoot, settling time, and steady-state error. Adjust $N_i$ and $\alpha$ and repeat. The lecturer emphasized that **practice** is the most important thing — run the MATLAB examples yourself.

---

## 6. Summary of the Three Controllers

| Controller | Transfer function | Eliminates SS error? | Phase effect at $\omega_c$ |
|---|---|---|---|
| **P** | $K_p$ | No (for stable systems) | None |
| **PI** | $K_p \cdot \dfrac{\tau_i s + 1}{\tau_i s}$ | Yes (integrator at DC) | Penalty: $-\arctan(1/N_i)$ |
| **PILead** | $K_p \cdot \dfrac{\tau_i s + 1}{\tau_i s} \cdot \dfrac{\tau_d s + 1}{\alpha \tau_d s + 1}$ | Yes | Penalty + Bonus: net depends on $N_i, \alpha$ |

### The Unified Design Method

Regardless of controller type, the procedure is always:

1. Write the **phase balance equation** (include contributions from all controller components)
2. Find the **crossover frequency** from the Bode phase plot of $G(s)$
3. Calculate the **controller parameters** ($\tau_i$, $\tau_d$) from $\omega_c$
4. Determine $K_p$ by making the open-loop magnitude equal 0 dB at $\omega_c$

> [!abstract] Key takeaway
> The philosophy behind PILead design is **frequency windowing**: each component does its job in a specific frequency range and is "deactivated" elsewhere.
> - **PI**: infinite gain at DC (kills error), cancelled by zero before $\omega_c$
> - **Lead**: phase bump centered at $\omega_c$ (helps stability), cancelled by pole at higher frequencies (avoids noise amplification)

---

## 7. MATLAB Workflow

```matlab
% Define system
s = tf('s');
G = 40 / ((s+1)*(s+2)*(s+10));

% Design parameters
phi_m = 60;           % desired phase margin [deg]
Ni = 3;               % PI zero placement ratio
alpha = 0.3;          % Lead pole-zero spacing

% Phase contributions
phi_PI = -atand(1/Ni);                           % [deg]
phi_lead = asind((1-alpha)/(1+alpha));            % [deg]

% Required phase of G at new crossover
phi_G_required = -180 + phi_m - phi_PI - phi_lead;  % [deg]

% Find crossover frequency from Bode plot
[mag, phase, w] = bode(G);
mag = squeeze(mag); phase = squeeze(phase);
% Find frequency where phase = phi_G_required
idx = find(phase <= phi_G_required, 1);
wc_new = w(idx);

% Controller parameters
tau_i = Ni / wc_new;
tau_d = 1 / (wc_new * sqrt(alpha));

% Controller transfer functions
K_PI = (tau_i*s + 1) / (tau_i*s);
K_lead = (tau_d*s + 1) / (alpha*tau_d*s + 1);

% Calculate Kp
[mag_at_wc, ~] = bode(K_PI * K_lead * G, wc_new);
Kp = 1 / mag_at_wc;

% Full controller and closed-loop
K = Kp * K_PI * K_lead;
G_cl = K*G / (1 + K*G);

% Evaluate
step(G_cl)
stepinfo(G_cl)
margin(K*G)
```

---

## 8. Exercise: Position Control of the REGBOT

Today's exercise: **position control of the REGBOT** (group work).
- Given: transfer function from voltage to **velocity**
- Need to add an integrator ($1/s$) to get from voltage to **position**
- Then apply the PILead design procedure

---

## 9. Next Lecture (Lecture 9)

- Design based on **time-domain specifications** (not just phase margin)
- Transform closed-loop specifications into open-loop specifications for design
- Decide which controller parts are needed for a given system
- Design feedback controllers based on closed-loop system time-domain specifications
- This lecture's specifications are "control theoretic" (phase margin); next lecture's will be "engineering" (overshoot, speed, accuracy)
