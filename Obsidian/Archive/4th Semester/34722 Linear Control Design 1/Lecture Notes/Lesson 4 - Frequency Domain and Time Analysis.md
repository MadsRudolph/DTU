---
course: "34722"
course-name: "Linear Control Design 1"
type: lecture-note
week: 8
tags: [LCD, lecture]
date: 2026-02-25
---
# Lesson 4 - Frequency Domain and Time Analysis

> [!abstract] Lecture Overview
> Lesson 4/13 — Teachers: Silvia Tolu & Dimitrios Papageorgiou
> Topics: Steady-state gain, break frequency, time constant, poles and zeros in the s-plane, stability from pole location, 2nd order systems, damping ratio, natural frequency.
> Schedule: 13:00–15:00 Lecture, 15:00–17:00 Introduction to REGBOT.

> [!example] Related Materials
> - Slides: [[4_Frequency_and_Time_Analysis_NoSol.pdf]]
> - Textbook: Pages 233–237 (2nd order systems)
> - Previous: [[Lesson 3 - Laplace Transform and Transfer Functions]]

---

## 1. Properties in the Frequency Domain

### 1.1 Steady-State (Static) Gain

The complex frequency variable is $s = \sigma + j\omega$, where $\omega$ is the signal frequency and $\sigma$ is zero for real (physical) frequencies.

For a system $H(s) \to G(s) \to Y(s)$ with a step input $H(s) = \frac{h_0}{s}$, the **steady-state gain** (also called static gain or DC gain) is defined as:

$$K_{ss} = \lim_{s \to 0} G(s)$$

This applies **only to stable systems**. The DC gain tells us the ratio of the steady-state output to a constant input — it corresponds to the gain at zero frequency.

**Example with a 1st order system:** For $G(s) = \frac{b}{s+a}$, rewrite as $G(s) = \frac{b}{a} \cdot \frac{a}{s+a}$ to see:

$$K_{ss} = \lim_{s \to 0} \frac{b}{s+a} = \frac{b}{a}$$

### 1.2 Steady-State Output and the Final Value Theorem

The steady-state output can be found using the **Final Value Theorem**:

$$Y_{ss} = \lim_{t \to \infty} y(t) = \lim_{s \to 0} s \cdot Y(s) = \lim_{s \to 0} s \cdot H(s) \cdot G(s)$$

For a step input of magnitude $h_0$ through $G(s) = \frac{b}{s+a}$:

$$Y(s) = \frac{h_0}{s} \cdot \frac{b}{a} \cdot \frac{a}{s+a}$$

Partial fraction expansion gives:

$$Y(s) = h_0 \frac{b}{a}\left(\frac{1}{s} - \frac{1}{s+a}\right)$$

Inverse Laplace transform:

$$y(t) = h_0 \frac{b}{a}\left(1 - e^{-at}\right)$$

Since $\lim_{t\to\infty}(1-e^{-at}) = 1$ (for $a > 0$), the steady-state output is $Y_{ss} = h_0 \cdot \frac{b}{a} = h_0 \cdot K_{ss}$.

**Numerical example:** $G(s) = \frac{220}{s^2 + 10s + 100}$, unit step input ($h_0 = 1$):

$$K_{ss} = \lim_{s\to 0} \frac{220}{s^2+10s+100} = \frac{220}{100} = 2.2$$

$$Y_{ss} = \lim_{s\to 0} s \cdot \frac{1}{s} \cdot G(s) = 2.2$$

> [!tip] MATLAB
> Use the function `dcgain(G)` to compute the steady-state gain of a transfer function.

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=3]]

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=6]]

### 1.3 Break Frequency and Time Constant

For a 1st order system $G(s) = \frac{b}{s+a}$, we can write it in standard forms:

$$G(s) = K_{ss}\frac{\omega_b}{s + \omega_b} = K_{ss}\frac{1}{\frac{1}{\omega_b}s + 1} = K_{ss}\frac{1}{\tau_b s + 1}$$

where:
- $\omega_b = a$ is the **break frequency** [rad/s] — the frequency where the system's magnitude response begins to roll off
- $\tau_b = \frac{1}{\omega_b}$ is the **time constant** [s]

**Physical meaning of $\tau_b$:** The time constant expresses the time the step response takes to reach **63.2%** of the way from the start value to the steady-state value. This comes from $1 - e^{-1} = 0.632$.

At $t = \tau_b$: $e^{-\omega_b t} = e^{-t/\tau_b} = e^{-1} = 0.3679$, so the output is at $1 - 0.3679 = 63.2\%$ of its final value.

The tangent to the step response at $t = 0$ intersects the steady-state value at $t = \tau_b$.

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=7]]

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=8]]

### 1.4 Control Question: Finding $K_{ss}$ and $\omega_b$

**Given:** $G(s) = \frac{150}{3s + 30}$

**a) Steady-state gain:**

$$G(s) = \frac{150}{3(s+10)} = \frac{50}{s+10} = 5 \cdot \frac{10}{s+10}$$

$$K_{ss} = \lim_{s\to 0} \frac{150}{3s+30} = \frac{150}{30} = 5$$

**b) Break frequency:** From the standard form $K_{ss}\frac{\omega_b}{s+\omega_b} = 5 \cdot \frac{10}{s+10}$:

$$\omega_b = 10 \text{ [rad/s]}$$

### 1.5 Control Question: From Step Response Plot

Given a unit step response that settles to $y_{ss} = 0.2$ with one pole:

**a)** $K_{ss} = \frac{y_{ss}}{h_0} = \frac{0.2}{1} = 0.2$

**b)** From the plot, 63% of 0.2 = 0.126 is reached at $\tau \approx 20$ s, so $\omega_b = \frac{1}{\tau} = 0.05$ rad/s

**c)** Transfer function: $G(s) = 0.2\frac{0.05}{s + 0.05} = 0.2\frac{1}{20s + 1}$

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=10]]

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=11]]

---

## 2. Poles and Zeros in the S-Plane

### 2.1 The S-Plane (Complex Frequency Plane)

The s-plane is the complex plane with $s = \sigma + j\omega$:
- **Horizontal axis** ($\sigma$): real part — controls exponential growth/decay
- **Vertical axis** ($j\omega$): imaginary part — represents physical frequencies
- The $j\omega$-axis itself represents physical (real) frequencies; DC is at the origin

For a transfer function $G(s) = \frac{s+0.5}{(s+1)(s+3)}$:
- **Poles** ($\times$): values of $s$ where $|G(s)| = \infty$ (roots of the denominator) — here at $s = -1$ and $s = -3$
- **Zeros** ($\circ$): values of $s$ where $|G(s)| = 0$ (roots of the numerator) — here at $s = -0.5$

A pole closer to the $j\omega$-axis (e.g. $s = -1$) is a **slow pole** (large time constant $\tau = 1$). A pole further left (e.g. $s = -3$) is a **fast pole** (small time constant $\tau = 1/3$).

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=12]]

### 2.2 First-Order Poles: Left Half-Plane (Stable)

**Example:** $G(s) = \frac{1}{s+3}$ — single pole at $s = -3$ (left half-plane).

For a unit step input $U(s) = \frac{1}{s}$:

$$Y(s) = \frac{1}{s} \cdot \frac{1}{s+3} = \frac{1}{3}\cdot\frac{3}{s(s+3)}$$

$$y(t) = 0.33(1 - e^{-3t})$$

The system parameters:
- $K_{ss} = \frac{1}{3} = 0.33$
- $\omega_b = 3$ rad/s (break frequency = pole location)
- $\tau = \frac{1}{3}$ s (time constant)

The output rises exponentially to a bounded steady-state value — this is **stable** behaviour.

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=14]]

### 2.3 First-Order Poles: Right Half-Plane (Unstable)

**Example:** $G_2(s) = \frac{-1}{s-3}$ — pole at $s = +3$ (right half-plane).

For a unit step input:

$$y_2(t) = 0.33(1 - e^{+3t})$$

The $e^{+3t}$ term grows without bound. The output diverges to infinity — the system is **unstable**.

> [!important] Stability Rule for Poles
> - **Pole in the left half-plane** ($\text{Re}(s) < 0$): Stable — exponential decay $e^{-at}$
> - **Pole in the right half-plane** ($\text{Re}(s) > 0$): Unstable — exponential growth $e^{+at}$
> - **Pole on the imaginary axis** ($\text{Re}(s) = 0$): Marginally stable — sustained oscillation

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=16]]

### 2.4 Effect of Zeros on the Step Response

Zeros do not affect stability (that's determined by poles alone), but they shape the transient response.

**Zero in the left half-plane** (minimum-phase zero): $G(s) = \frac{K(1.25s + 1)}{(0.3s+1)(s+1)}$, zero at $s = -0.8$.

The output can be decomposed as $Y(s) = (1.25s + 1) \cdot V(s)$, giving $y(t) = 1.25\dot{v}(t) + v(t)$. The derivative term $1.25\dot{v}(t)$ adds a "kick" that speeds up the initial response — the output overshoots before settling.

**Zero in the right half-plane** (non-minimum-phase zero): $G(s) = \frac{K(-1.25s + 1)}{(0.3s+1)(s+1)}$, zero at $s = +0.8$.

Now $y(t) = -1.25\dot{v}(t) + v(t)$. The negative derivative term initially drives the output in the **wrong direction** — the response dips below zero before rising. This "undershoot" or "inverse response" is characteristic of right-half-plane zeros and is a well-known challenge in control design.

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=19]]

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=20]]

---

## 3. Second-Order Systems with Real Poles

A 2nd order system with two real poles can be written as the cascade of two 1st order systems:

$$G(s) = \frac{K}{(\tau_1 s + 1)(\tau_2 s + 1)}$$

The step response is always slower than a single 1st order system because the signal must pass through two "filters". The relative size of $\tau_1$ and $\tau_2$ determines the shape:

- $\tau_2 \ll \tau_1$: The fast pole is negligible; response looks 1st order with $\tau \approx \tau_1$
- $\tau_1 = \tau_2$: Response has an S-shaped curve (inflection point), slowest for given dominant time constant
- $\tau_2 \gg \tau_1$: The second pole dominates and further slows the response

> [!note] Key Insight
> Adding a second real pole always makes the system slower — never faster. The system must "charge up" two energy-storage elements in sequence.

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=17]]

---

## 4. Second-Order Systems with Complex Poles

### 4.1 When Do Complex Poles Arise?

For $G(s) = \frac{b_0}{s^2 + a_1 s + a_0}$, the poles are:

$$s_{1,2} = \frac{-a_1 \pm \sqrt{a_1^2 - 4a_0}}{2}$$

- $a_1^2 - 4a_0 \geq 0$: **Real** roots (two distinct or repeated poles)
- $a_1^2 - 4a_0 < 0$: **Complex conjugate** roots (oscillatory behaviour)

### 4.2 Standard Second-Order Form

The standard form uses the **natural frequency** $\omega_n$ and **damping ratio** $\zeta$:

$$G(s) = K_{ss} \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

The condition for complex poles is $\zeta < 1$ (since $(2\zeta\omega_n)^2 < 4\omega_n^2$).

**Alternative filter notation** using quality factor $Q$:

$$G(s) = \frac{\omega_0^2}{s^2 + \frac{\omega_0}{Q}s + \omega_0^2}, \quad \zeta = \frac{1}{2Q}$$

### 4.3 Three Important Frequencies

For $G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$:

1. **Natural frequency $\omega_n$** — The frequency of free oscillation with no damping ($\zeta = 0$). This is the "ideal" oscillation frequency.

2. **Damped frequency $\omega_d$** — The actual frequency of free oscillation when $0 < \zeta < 1$:
$$\omega_d = \omega_n\sqrt{1 - \zeta^2}$$

3. **Resonance frequency $\omega_r$** — The input frequency that maximizes the output amplitude (only exists for $0 < \zeta < 1/\sqrt{2} \approx 0.707$):
$$\omega_r = \omega_n\sqrt{1 - 2\zeta^2}$$

**Peak overshoot** of the step response:

$$M_P = e^{\frac{-\pi\zeta}{\sqrt{1-\zeta^2}}}$$

### 4.4 Damping Ratio Classification

The damping ratio $\zeta$ completely determines the qualitative character of the step response:

| $\zeta$ | Behaviour | Description |
|---------|-----------|-------------|
| $< 0$ | Unstable | Poles in right half-plane, output grows without bound |
| $= 0$ | Undamped | Perpetual oscillation at $\omega_n$, never settles |
| $0 < \zeta < 1$ | Underdamped | Damped oscillation, overshoot before settling |
| $= 1$ | Critically damped | Fastest settling without overshoot, repeated real poles |
| $> 1$ | Overdamped | No oscillation, slower than critically damped, two real poles |

> [!tip] Design Sweet Spot
> In practice, $\zeta \approx 0.7$ (critically damped-ish) is often a good design target — it gives fast response with minimal overshoot (~5%). The value $\zeta = 1/\sqrt{2} \approx 0.707$ is particularly common in filter design (Butterworth response).

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=28]]

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=29]]

### 4.5 Complex Poles in the S-Plane

For $G(s) = \frac{4}{s^2 + 2 \cdot 0.707 \cdot 2s + 4}$ with $\zeta = 0.707$ and $\omega_n = 2$ rad/s:

The poles are at $s = -\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2} = -1.4 \pm j1.4$.

In the s-plane:
- The **real part** $-\zeta\omega_n = -1.4$ determines the decay rate (distance from imaginary axis)
- The **imaginary part** $\omega_n\sqrt{1-\zeta^2} = 1.4$ determines the oscillation frequency
- The **distance from origin** $= \omega_n = 2$ (the natural frequency)
- The **angle from the negative real axis** $= \arccos(\zeta)$

> [!important] Complex Poles Always Come in Conjugate Pairs
> For a system with real coefficients, complex poles always appear as $s = -a \pm jb$. You can never have a single isolated complex pole.

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=30]]

---

## 5. Stability from Pole Locations

### 5.1 Summary of Pole-Location Rules

| Pole Location | Impulse Response | Stability |
|---------------|-----------------|-----------|
| Real, left half-plane ($s = -a$) | Decaying exponential $e^{-at}$ | **Stable** |
| Real, right half-plane ($s = +a$) | Growing exponential $e^{+at}$ | **Unstable** |
| Complex pair, LHP ($s = -a \pm jb$) | Decaying oscillation $e^{-at}\sin(bt)$ | **Stable** |
| Complex pair, RHP ($s = +a \pm jb$) | Growing oscillation $e^{+at}\sin(bt)$ | **Unstable** |
| Single pair on $j\omega$-axis ($s = \pm jb$) | Sustained oscillation $\sin(bt)$ | **Marginally stable** |
| Multiple pairs on $j\omega$-axis | Growing oscillation $t\sin(bt)$ | **Unstable** |
| Single root at origin ($s = 0$) | Constant (ramp for step input) | **Marginally stable** |
| Double root at origin ($s = 0$, multiplicity 2) | Ramp $t$ | **Unstable** |

### 5.2 Unstable Systems

Characteristics of unstable systems:
- Small perturbations remove the system from equilibrium (e.g. inverted pendulum)
- A bounded input produces an unbounded output (e.g. constant motor torque gives infinite angular position)
- At least one pole in the RHP guarantees instability

**Example:** $G_1(s) = \frac{1}{s-1}$ gives $\dot{y} = y + u$, with solution $y(t) = y_0 e^t + \int_0^t e^{t-\tau}u(\tau)\,d\tau$. Regardless of input, $|y(t)| \to \infty$.

**Multiple imaginary poles:** $G_2(s) = \frac{1}{(s^2+1)^2}$ with impulse input gives $y(t) = 0.5\sin(t) - 0.5t\cos(t)$. The $t\cos(t)$ term grows linearly — unstable despite poles on the imaginary axis.

> [!question] How to stabilize an unstable system?
> This will be covered in **Lecture 10** — feedback control can move poles from the RHP to the LHP.

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=33]]

![[4_Frequency_and_Time_Analysis_NoSol.pdf#page=34]]

---

## 6. Control Questions

### 6.1 S-Plane Analysis

**1)** $G(s) = \frac{100}{s^2 + 7s + 10}$

a) Denominator: $s^2 + 7s + 10 = (s+2)(s+5)$ — poles at $s = -2$ and $s = -5$. No zeros (constant numerator).

b) Both poles are in the LHP — system is **stable**.

**2)** $G(s) = \frac{s-2}{0.5s - 2}$

a) $K_{ss} = \lim_{s\to 0} \frac{s-2}{0.5s-2} = \frac{-2}{-2} = 1$

b) Zero at $s = 2$ (numerator = 0). Pole at $s = 4$ (denominator $0.5s - 2 = 0$).

c) Pole at $s = 4$ is in the RHP — system is **unstable**.

### 6.2 Comparing Systems

**1)** $G_1(s) = \frac{10}{s+100}$ vs. $G_2(s) = \frac{1000}{s^2+14s+100}$

$G_1$ has $\omega_b = 100$ rad/s (time constant $\tau = 0.01$ s). $G_2$ has $\omega_n = 10$ rad/s. $G_1$ is much faster since its pole is at $s = -100$ compared to $G_2$'s poles near $s = -7 \pm j\sqrt{51}$.

**2)** $G_2(s) = \frac{1000}{s^2 + 10s + 100}$

a) Discriminant: $10^2 - 4 \cdot 100 = -300 < 0$ — **yes, complex poles**

b) $\omega_n = \sqrt{100} = 10$ rad/s

c) $2\zeta\omega_n = 10 \Rightarrow \zeta = \frac{10}{2\cdot 10} = 0.5$

d) $M_P = e^{-\pi \cdot 0.5/\sqrt{1-0.25}} = e^{-\pi/\sqrt{3}} \approx e^{-1.814} \approx 16.3\%$

### 6.3 Complete Analysis Example

$G(s) = \frac{s^2 + 7s + 324}{(0.01s+1)(s^2+5s+400)}$

a) Real pole from $(0.01s+1)$: $s = -100$. Numerator discriminant: $49 - 1296 < 0$ — complex zeros. Denominator $s^2+5s+400$: discriminant $25 - 1600 < 0$ — complex poles.

b) Zeros: $s = \frac{-7 \pm j\sqrt{1247}}{2} \approx -3.5 \pm j17.7$. Poles: $s = \frac{-5 \pm j\sqrt{1575}}{2} \approx -2.5 \pm j19.8$

c) All poles in LHP — **stable**

e) $\omega_n = \sqrt{400} = 20$ rad/s, $\zeta = \frac{5}{2\cdot 20} = 0.125$

f) The most **dominant pole** is the one closest to the imaginary axis: the complex pair at $\approx -2.5 \pm j19.8$ (real part $-2.5$, vs. the real pole at $-100$).

---

## Key Takeaways

1. **Steady-state gain** $K_{ss} = \lim_{s\to 0} G(s)$ gives the DC amplification. Use the Final Value Theorem for the steady-state output: $Y_{ss} = \lim_{s\to 0} s \cdot Y(s)$.

2. **Break frequency** $\omega_b$ and **time constant** $\tau_b = 1/\omega_b$ characterize 1st order dynamics. The time constant is the time to reach 63.2% of steady state.

3. **Poles determine stability:** LHP = stable (decaying), RHP = unstable (growing), imaginary axis = marginally stable (sustained oscillation).

4. **Zeros shape the transient:** LHP zeros speed up the response (can cause overshoot). RHP zeros cause initial inverse response (undershoot).

5. **2nd order standard form** $\frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$ is parameterized by natural frequency $\omega_n$ and damping ratio $\zeta$. The damping ratio determines oscillatory ($\zeta < 1$) vs. non-oscillatory ($\zeta \geq 1$) behaviour.

6. **The dominant pole** (closest to the $j\omega$-axis) determines the slowest dynamics and dominates the overall system response.

---

## Key Formulas

> [!abstract] Quick Reference
> | Concept | Formula |
> |---------|---------|
> | Steady-state gain | $K_{ss} = \lim_{s \to 0} G(s)$ |
> | Final value theorem | $Y_{ss} = \lim_{s \to 0} s \cdot Y(s)$ |
> | 1st order standard form | $G(s) = K_{ss}\frac{\omega_b}{s+\omega_b} = K_{ss}\frac{1}{\tau_b s + 1}$ |
> | Time constant | $\tau_b = \frac{1}{\omega_b}$ |
> | 63% rule | $1 - e^{-1} = 0.632$ |
> | 2nd order standard form | $G(s) = K_{ss}\frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$ |
> | Damped frequency | $\omega_d = \omega_n\sqrt{1 - \zeta^2}$ |
> | Resonance frequency | $\omega_r = \omega_n\sqrt{1 - 2\zeta^2}$ |
> | Peak overshoot | $M_P = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ |
> | Quality factor | $Q = \frac{1}{2\zeta}$ |
> | Complex poles | $s = -\zeta\omega_n \pm j\omega_n\sqrt{1-\zeta^2}$ |

---

> [!nav]
> [[Lesson 3 - Laplace Transform and Transfer Functions|← Lesson 3]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
