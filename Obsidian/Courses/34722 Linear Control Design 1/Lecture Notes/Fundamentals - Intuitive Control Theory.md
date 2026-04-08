---
course: "34722"
course-name: "Linear Control Design 1"
type: study-guide
tags: [LCD, fundamentals, intuition]
date: 2026-04-08
---
# Fundamentals - Intuitive Control Theory

> [!abstract] Purpose
> This document builds up control theory from scratch with focus on **intuition first, math second**. Every concept answers: *What problem does this solve?* and *Why do we need this?*
> Written as a companion to the lecture notes — use this when the math in the lectures feels disconnected.

> [!example] Related Materials
> - [[Lesson 2 - Block Diagrams and Control Concepts]]
> - [[Lesson 3 - Laplace Transform and Transfer Functions]]
> - [[Lesson 4 - Frequency Domain and Time Analysis]]
> - [[Lesson 8 - Position Controller Design]]
> - [[Lesson 9 - PI-Lead Design with Specifications]]
> - [[Midterm Cheatsheet]]

---

## Table of Contents

1. [[#1. The Problem: Why Do We Need Control?|The Problem: Why Control?]]
2. [[#2. The Feedback Loop|The Feedback Loop]]
3. [[#3. Block Diagrams: Reading the Wiring Diagram|Block Diagrams]]
4. [[#4. Why Laplace? The Motivation for s-Domain|Why Laplace?]]
5. [[#5. Transfer Functions: The Language of Control|Transfer Functions]]
6. [[#6. Poles and Zeros: The DNA of a System|Poles and Zeros]]
7. [[#7. Stability: The Non-Negotiable Requirement|Stability]]
8. [[#8. Bode Plots: Seeing the System|Bode Plots]]
9. [[#9. The Nyquist Plot: Another Stability View|Nyquist Plot]]
10. [[#10. Controller Design: P, I, D and Their Combinations|Controller Design: P, I, D]]
11. [[#11. Type-n Systems and Steady-State Error|Type-n Systems]]
12. [[#12. Connecting It All: The Design Flow|The Design Flow]]
13. [[#13. Quick Reference: "What Does This Mean Physically?"|Quick Reference]]
14. [[#14. Common Mistakes and Misconceptions|Common Mistakes]]

**Companion documents:**
- [[Diagnostic Guide - What Went Wrong|Diagnostic Guide]] — symptom-based troubleshooting
- [[Worked Example - REGBOT Position Controller|Worked Example]] — complete PILead design walkthrough

---

## 1. The Problem: Why Do We Need Control?

> [!example] Detailed Treatment
> - Open vs. closed loop, block diagrams: [[Lesson 2 - Block Diagrams and Control Concepts#2. Modelling Recap|Lesson 2]]
> - REGBOT open-loop characterization: [[Day 4 - REGBOT Introduction]]

### 1.1 The Real World is Unpredictable

You have a system (a motor, a robot, a heater) and you want it to do something specific: drive at 1 m/s, balance upright, maintain 22 degrees C.

The naive approach: calculate the exact input needed and send it. This is **open-loop control**. It fails because:
- The system is never exactly what your model says (friction changes, batteries drain)
- Disturbances hit the system (wind, hills, someone opens a window)
- Your model is always an approximation

> [!important] Core Insight
> Open-loop control is like driving with your eyes closed — you calculated the right steering angle at the start, but you can't correct when things change.

### 1.2 The Solution: Measure and Correct

**Closed-loop (feedback) control** = measure the output, compare to what you want, adjust.

That's it. The entire field of control theory is about doing this *well*.

---

## 2. The Feedback Loop

### 2.1 The Structure

```
r(t) ──→ [+] ──→ e(t) ──→ [ Controller C(s) ] ──→ u(t) ──→ [ System G(s) ] ──→ y(t)
          [-]                                                                     │
           └──────────────────────────────────────────────────────────────────────┘
```

| Signal | Name | Meaning | REGBOT Example |
|--------|------|---------|----------------|
| $r(t)$ | Reference | What you *want* | "Drive 1 m/s" |
| $y(t)$ | Output | What you *actually have* | Measured speed from encoder |
| $e(t) = r(t) - y(t)$ | Error | What you're *missing* | "I'm 0.2 m/s too slow" |
| $u(t)$ | Control signal | What you *send* to the system | Voltage to motor |

> [!tip] Key Point
> The controller only sees the **error**. It doesn't know if the error is because the reference changed, or because a disturbance hit the system. It just tries to make $e(t) \to 0$.

### 2.2 The Fundamental Trade-off

Control design is always a compromise between:

| Want | But... |
|------|--------|
| Fast response (short rise time) | Risk overshoot and oscillation |
| No overshoot (smooth approach) | Slow response |
| Zero steady-state error | Need integrator, which adds phase lag and hurts stability |
| Robust to disturbances | Need high gain, which risks instability |

**There is no perfect controller.** Every design is a trade-off. The skill is knowing which trade-offs matter for your application.

---

## 3. Block Diagrams: Reading the Wiring Diagram

> [!example] Detailed Treatment
> - Block diagram elements and construction: [[Lesson 2 - Block Diagrams and Control Concepts#3. Block Diagram Modelling|Lesson 2, Section 3]]
> - Block diagram exercises: [[Day 3 - Block Diagram Exercise]]
> - [[Assignment_3_BlockDiagrams.pdf|Assignment 3 PDF]]

### 3.1 What is a Block Diagram?

A block diagram is a **visual map** of how signals flow through your system. Instead of staring at differential equations, you can *see* the structure.

Each block has a simple job:

| Symbol | What It Does | Example |
|--------|-------------|---------|
| **Rectangle** ($G(s)$) | Multiplies input by transfer function | Motor: input voltage → output speed |
| **Circle** ($\Sigma$) | Adds or subtracts signals | $e = r - y$ (error = reference minus output) |
| **Arrow** | Carries a signal from one place to another | The measured speed going back to the summation |
| **Branch point** | Copies a signal to two destinations | Speed goes both to the output AND back to feedback |

> [!tip] How to Read a Block Diagram
> Follow the arrows like water flowing through pipes. Each block transforms the "water" as it passes through. The summation nodes mix or subtract streams.

### 3.2 Why Block Diagrams Matter

They let you:
1. **See the feedback structure** — where is the loop? What's being measured?
2. **Combine blocks into one transfer function** — simplify complex systems
3. **Identify what you can change** — the controller block is what you design

### 3.3 The Three Rules for Reducing Block Diagrams

Any block diagram, no matter how complex, can be reduced using just three rules:

**Rule 1: Series (cascade)** — blocks in a row multiply:

```
U → [G₁] → [G₂] → Y    =    U → [G₁ · G₂] → Y
```

$$G_{total}(s) = G_1(s) \cdot G_2(s)$$

*Why:* The output of $G_1$ becomes the input of $G_2$. In the $s$-domain, that's just multiplication.

**Rule 2: Parallel** — blocks side by side add:

```
    ┌→ [G₁] →┐
U → ┤         ├→ [+] → Y    =    U → [G₁ + G₂] → Y
    └→ [G₂] →┘
```

$$G_{total}(s) = G_1(s) + G_2(s)$$

*Why:* Both blocks get the same input, and their outputs are summed.

**Rule 3: Feedback loop** — the most important one:

```
R → [+] → [G] → Y
     [-]          │
      └────[H]←───┘
```

$$T(s) = \frac{G(s)}{1 + G(s)H(s)}$$

*Why:* This is the closed-loop formula. If $H = 1$ (unity feedback), it simplifies to $\frac{G}{1+G}$.

> [!important] The Feedback Formula is Everything
> Almost every problem in this course comes down to applying $\frac{\text{Forward}}{1 + \text{Loop}}$. If you can identify the forward path and the loop gain in a block diagram, you can write the transfer function directly.

### 3.4 Tips for Complex Block Diagrams

When a diagram has multiple loops or nested structures:

1. **Start from the innermost loop** and reduce it first
2. **Move branch points** and **summation nodes** to simplify (you can move them if you compensate with a gain block)
3. **Redraw after each step** — don't try to do it all at once
4. **Check your answer:** Does the DC gain make sense? If $G(0) = 5$ and $H(0) = 1$, then $T(0) = 5/6 \approx 0.83$.

---

## 4. Why Laplace? The Motivation for s-Domain

> [!example] Detailed Treatment
> - Laplace rules and properties: [[Lesson 3 - Laplace Transform and Transfer Functions]]
> - Practice: [[Day 3 - MATLAB Exercise]]

### 4.1 The Problem with Time Domain

In the time domain, a simple feedback system gives us this equation for the output:

$$y(t) = \int_0^t g(\tau) \cdot u(t - \tau) \, d\tau$$

This is a **convolution integral** — very hard to work with. And if you close the loop, you get integro-differential equations that are painful to solve.

### 4.2 What Laplace Does

The Laplace transform converts:
- **Derivatives** $\to$ multiplication by $s$
- **Integrals** $\to$ division by $s$
- **Convolution** $\to$ simple multiplication

So this nightmare:
$$m\ddot{y}(t) + b\dot{y}(t) + ky(t) = u(t)$$

Becomes this algebra:
$$ms^2 Y(s) + bsY(s) + kY(s) = U(s)$$
$$Y(s)(ms^2 + bs + k) = U(s)$$
$$\frac{Y(s)}{U(s)} = \frac{1}{ms^2 + bs + k}$$

> [!important] Core Insight
> Laplace doesn't add information. It **rephrases** the same system in a language where feedback, stability, and design are much easier to work with. It's a tool, not new physics.

### 4.3 What is $s$?

$s = \sigma + j\omega$ is the **complex frequency variable**.

- $j\omega$ alone: the frequency of oscillation (what you see on a Bode plot)
- $\sigma$ alone: exponential growth ($\sigma > 0$) or decay ($\sigma < 0$)
- Together: $e^{st} = e^{\sigma t} \cdot e^{j\omega t}$ = a signal that oscillates at frequency $\omega$ while growing/decaying at rate $\sigma$

You don't need to think about $s$ deeply for most controller design. Just know: **$s$ is to differential equations what a wrench is to bolts** — it makes them easy to manipulate.

---

## 5. Transfer Functions: The Language of Control

> [!example] Detailed Treatment
> - Transfer function derivation and manipulation: [[Lesson 3 - Laplace Transform and Transfer Functions]]
> - DC gain, break frequency, time constant: [[Lesson 4 - Frequency Domain and Time Analysis#1. Properties in the Frequency Domain|Lesson 4, Section 1]]
> - REGBOT motor model: [[Day 5 - Black Box Modeling]]

### 5.1 What is a Transfer Function?

A transfer function $G(s)$ is the **input-output relationship** of a system in the $s$-domain:

$$G(s) = \frac{Y(s)}{U(s)}$$

It tells you: "For any input signal, multiply by $G(s)$ to get the output signal."

> [!tip] Analogy
> A transfer function is like a recipe scaling factor. If $G(s) = 2$, every input gets doubled. If $G(s) = \frac{1}{s+1}$, the system filters and smooths the input — high frequencies get attenuated, low frequencies pass through.

### 5.2 System Order: Reading it from the Transfer Function

The **order** of a system = the degree of the **denominator** polynomial in $G(s)$.

$$G(s) = \frac{N(s)}{D(s)} \quad \Rightarrow \quad \text{Order} = \deg(D(s)) = \text{number of poles}$$

| Transfer Function | Denominator | Order | Poles |
|---|---|---|---|
| $\frac{5}{s + 3}$ | $s + 3$ (degree 1) | 1st | one real pole |
| $\frac{10}{s^2 + 4s + 9}$ | $s^2 + 4s + 9$ (degree 2) | 2nd | two poles (may be complex) |
| $\frac{s+1}{s^3 + 2s^2 + s + 5}$ | degree 3 | 3rd | three poles |
| $\frac{13.34}{s + 35.71}$ (REGBOT velocity) | degree 1 | 1st | one real pole at $-35.71$ |
| $\frac{13.34}{s(s + 35.71)}$ (REGBOT position) | degree 2 | 2nd | poles at $0$ and $-35.71$ |

> [!important] Physical Meaning of Order
> The order equals the number of **independent energy stores** in the system. Each energy store contributes one pole:
> - 1 capacitor or 1 inductor → 1st order
> - 1 mass + 1 spring → 2nd order (kinetic + potential energy)
> - REGBOT motor (1 mechanical time constant) → 1st order
> - REGBOT position (motor + integration of velocity) → 2nd order

**Going the other way:** If you know a system is $n$th order, you know:
- The denominator has degree $n$
- There are exactly $n$ poles
- The step response has $n$ exponential/oscillatory modes
- The system is described by an $n$th order ODE

> [!tip] Quick Check
> Count the powers of $s$ in the denominator. That's the order. The numerator degree (number of zeros) does not affect the order — it affects the *shape* of the response but not the fundamental dynamics.

### 5.3 Why Transfer Functions Matter

With transfer functions, feedback becomes **algebra**:

**Closed-loop transfer function:**
$$T(s) = \frac{C(s)G(s)}{1 + C(s)G(s)}$$

This is the **most important formula in the course**. It says: the closed-loop behavior equals the forward path divided by $(1 + \text{loop gain})$.

> [!important] Where This Comes From
> Start with the loop:
> - $E(s) = R(s) - Y(s)$
> - $Y(s) = C(s)G(s) \cdot E(s) = C(s)G(s)(R(s) - Y(s))$
> - $Y(s) + C(s)G(s)Y(s) = C(s)G(s)R(s)$
> - $Y(s)(1 + C(s)G(s)) = C(s)G(s)R(s)$
> - $T(s) = \frac{Y(s)}{R(s)} = \frac{C(s)G(s)}{1 + C(s)G(s)}$

### 5.4 The REGBOT Motor Example

From Day 4/5, the REGBOT velocity model is:

$$G_{vel}(s) = \frac{13.34}{s + 35.71} = \frac{0.373}{0.028s + 1}$$

This tells us:
- **DC gain** $K_{ss} = \frac{13.34}{35.71} = 0.373$ (m/s)/V — each volt gives 0.373 m/s at steady state
- **Time constant** $\tau = \frac{1}{35.71} = 0.028$ s — the motor reaches 63.2% of its final speed in 28 ms
- **One pole** at $s = -35.71$ — the system is stable (pole in left half-plane) and fast

---

## 6. Poles and Zeros: The DNA of a System

> [!example] Detailed Treatment
> - Poles, zeros, and s-plane: [[Lesson 4 - Frequency Domain and Time Analysis#2. Poles and Zeros in the s-Plane|Lesson 4, Section 2]]
> - 2nd order systems, $\zeta$ and $\omega_n$: [[Lesson 4 - Frequency Domain and Time Analysis#3. Second-Order Systems|Lesson 4, Section 3]]

### 6.1 What Are Poles and Zeros?

Every transfer function can be written as:

$$G(s) = K \cdot \frac{(s - z_1)(s - z_2)\cdots}{(s - p_1)(s - p_2)\cdots}$$

- **Zeros** ($z_i$): values of $s$ where $G(s) = 0$ (output vanishes)
- **Poles** ($p_i$): values of $s$ where $G(s) \to \infty$ (output blows up)

### 6.2 Why Poles Determine Everything

The poles of a system determine its **natural response** — how it behaves when you kick it and let go.

Each pole at $s = p$ contributes a term $e^{pt}$ to the time response:

| Pole Location | $e^{pt}$ Behavior | Meaning |
|---------------|-------------------|---------|
| Real, negative ($p = -a$) | $e^{-at}$ | Exponential decay — **stable** |
| Real, positive ($p = +a$) | $e^{+at}$ | Exponential growth — **unstable** |
| $p = 0$ | $e^{0} = 1$ | Constant — **marginally stable** (integrator) |
| Complex $p = -a \pm j\omega$ | $e^{-at}\sin(\omega t)$ | Decaying oscillation — **stable, oscillatory** |
| Complex $p = +a \pm j\omega$ | $e^{+at}\sin(\omega t)$ | Growing oscillation — **unstable** |

> [!important] Core Insight
> **Poles in the left half-plane (LHP)** = stable. **Poles in the right half-plane (RHP)** = unstable. This is the single most important rule in control theory.

### 6.3 Pole Location and System Behavior

For a second-order system $G(s) = \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$:

- $\omega_n$ = **natural frequency** — how fast the system oscillates
- $\zeta$ = **damping ratio** — how quickly the oscillations die out

| $\zeta$ | Behavior | Pole Type |
|---------|----------|-----------|
| $\zeta > 1$ | Overdamped (no oscillation, sluggish) | Two real poles |
| $\zeta = 1$ | Critically damped (fastest without oscillation) | Repeated real pole |
| $0 < \zeta < 1$ | Underdamped (oscillates, then settles) | Complex conjugate poles |
| $\zeta = 0$ | Undamped (oscillates forever) | Purely imaginary poles |

> [!tip] Intuition for $\zeta$
> Think of $\zeta$ as "how much shock absorber" the system has. A car with $\zeta = 0.1$ bounces like crazy over speed bumps. A car with $\zeta = 0.7$ absorbs the bump with one small overshoot. A car with $\zeta = 2$ crawls over the bump.

### 6.4 The Dominant Pole Approximation

If a system has multiple poles, the **dominant pole** (closest to the imaginary axis = slowest) determines the overall behavior.

Example: poles at $s = -2$ and $s = -50$.
- The $s = -50$ pole dies out in $\sim 0.06$ s ($\tau = 1/50$)
- The $s = -2$ pole dies out in $\sim 1.5$ s ($\tau = 1/2$)
- After 0.1 s, only the $s = -2$ pole matters — it **dominates**

---

## 7. Stability: The Non-Negotiable Requirement

> [!example] Detailed Treatment
> - Stability from pole locations: [[Lesson 4 - Frequency Domain and Time Analysis]]
> - Gain and phase margin from Bode plots: [[Day 6 - Bode and P-Controller Design]]
> - Nyquist stability: [[7_Nyquist_Plot_and_Stability.pdf|Lecture 7 slides]]

### 7.1 What is Stability?

A system is **BIBO stable** (Bounded-Input Bounded-Output) if every bounded input produces a bounded output. In practice: the system doesn't blow up.

**Necessary and sufficient condition:** All poles of the closed-loop transfer function must be in the LHP (negative real part).

### 7.2 How Feedback Can Create Instability

This is counterintuitive: feedback, which is supposed to help, can make things *worse*.

Consider the loop gain $L(s) = C(s)G(s)$. The closed-loop poles are the roots of:

$$1 + L(s) = 0$$

This means the closed-loop poles depend on the **controller**. A bad controller moves the poles into the RHP, making the system unstable.

> [!important] Physical Intuition
> Instability from feedback happens when the correction signal arrives **too late** (too much phase lag). By the time the system reacts, the error has reversed, so the "correction" actually makes things worse. The system chases its own tail with ever-growing oscillations.

### 7.3 Stability Margins: How Close to the Edge?

We don't just want stability — we want a **margin of safety**.

- **Gain margin (GM):** How much can we increase the gain before instability? Measured in dB. Want: $\geq 6$ dB.
- **Phase margin (PM / $\gamma_M$):** How much extra phase lag can the system tolerate before instability? Measured in degrees. Want: $\geq 45°$.

> [!tip] Phase Margin Intuition
> Phase margin answers: "At the frequency where the loop gain equals 1 (the system can self-sustain oscillations), how far are we from the critical 180 degrees of phase lag that would cause instability?"
>
> $\gamma_M = 60°$ means we could add 60 more degrees of lag before the system goes unstable. That's comfortable.
> $\gamma_M = 5°$ means we're barely stable. Any model uncertainty could push us over the edge.

---

## 8. Bode Plots: Seeing the System

> [!example] Detailed Treatment
> - Frequency response, break frequency: [[Lesson 4 - Frequency Domain and Time Analysis#1. Properties in the Frequency Domain|Lesson 4, Section 1]]
> - Bode plot construction and stability margins: [[Day 6 - Bode and P-Controller Design]]
> - Bode slides: [[6_bode_plot_and_stability.pdf|Lecture 6 slides]]

### 8.1 What is a Bode Plot?

A Bode plot shows how a system responds to sinusoidal inputs at **different frequencies**:
- **Magnitude plot** (top): how much the system amplifies or attenuates each frequency (in dB)
- **Phase plot** (bottom): how much the system delays each frequency (in degrees)

### 8.2 Why Frequency Domain?

Real-world signals are combinations of many frequencies. The Bode plot tells you what the system does to each frequency component:
- Low frequencies (slow changes): usually passed through
- High frequencies (fast changes, noise): usually attenuated

### 8.3 Reading a Bode Plot

For $G(s) = \frac{0.373}{0.028s + 1}$ (REGBOT motor):

- At low frequencies ($\omega \ll 35.7$ rad/s): magnitude $\approx 0.373$ ($-8.6$ dB), phase $\approx 0°$
- At the break frequency ($\omega = 35.7$ rad/s): magnitude drops by 3 dB, phase = $-45°$
- At high frequencies ($\omega \gg 35.7$ rad/s): magnitude drops at $-20$ dB/decade, phase $\to -90°$

> [!important] Core Insight
> Each pole adds $-90°$ of phase and $-20$ dB/decade of magnitude rolloff. Each zero adds $+90°$ of phase and $+20$ dB/decade. This is why we care about poles and zeros — they shape the Bode plot, which determines stability margins and performance.

### 8.4 Key Frequencies on the Bode Plot

| Frequency                             | What Happens                 | Why It Matters                   |
| ------------------------------------- | ---------------------------- | -------------------------------- |
| DC ($\omega = 0$)                     | Magnitude = DC gain          | Determines steady-state behavior |
| Break frequency ($\omega_b = 1/\tau$) | Magnitude starts rolling off | Separates "pass" from "reject"   |
| Crossover frequency ($\omega_c$)      | $L(j\omega)= 1$ (0 dB)       | **Phase margin is read here**    |
| Phase crossover ($\omega_{pc}$)       | $\angle L(j\omega) = -180°$  | **Gain margin is read here**     |

---

## 9. The Nyquist Plot: Another Stability View

> [!example] Detailed Treatment
> - Nyquist criterion and examples: [[7_Nyquist_Plot_and_Stability.pdf|Lecture 7 slides]]

### 9.1 What is a Nyquist Plot?

A Bode plot shows magnitude and phase on *separate* graphs. A Nyquist plot shows them *together* on one picture: it's the curve you get by plotting $L(j\omega)$ (the loop gain evaluated at every frequency) as a point in the **complex plane**.

- The **x-axis** is the real part of $L(j\omega)$
- The **y-axis** is the imaginary part of $L(j\omega)$
- Each frequency $\omega$ gives one point. Sweeping $\omega$ from $0$ to $\infty$ traces out a curve.

> [!tip] Analogy
> If a Bode plot is like reading a table of "magnitude at frequency X, phase at frequency X", the Nyquist plot is like plotting all those values as dots on a map. You get a single curve that shows the whole story at once.

### 9.2 The Critical Point: $-1 + 0j$

Remember from stability theory: the system goes unstable when the loop gain has magnitude 1 and phase $-180°$. In the complex plane, that's the point $-1 + 0j$.

The **Nyquist stability criterion** says:

> [!important] Nyquist Criterion (Simplified)
> For a system with **no open-loop RHP poles** (which covers most systems in this course):
>
> **The closed-loop system is stable if and only if the Nyquist curve does NOT encircle the point $-1$.**
>
> "Encircle" means the curve loops around $-1$ as you trace it. If the curve passes to the right of $-1$, you're safe. If it wraps around $-1$, the system is unstable.

### 9.3 Reading Stability Margins from Nyquist

The Nyquist plot makes margins very visual:

- **Phase margin:** The Nyquist curve crosses the unit circle (distance 1 from origin) at some point. The angle between that crossing point and the negative real axis is the phase margin.
- **Gain margin:** The curve crosses the negative real axis at some point with magnitude $|L|$. The gain margin is $1/|L|$ — how much you could scale up the curve before it reaches $-1$.

```
        Im
        │        ╭──── Nyquist curve
        │      ╱
        │    ╱
────────┼──●────────── Re
   -1   │  ╲       (curve passes to the right of -1: STABLE)
        │    ╲
        │      ╲
```

### 9.4 Nyquist vs. Bode: When to Use Which?

| | Bode Plot | Nyquist Plot |
|---|---|---|
| **Shows** | Magnitude and phase separately | Both together in complex plane |
| **Best for** | Controller design (reading margins, choosing $\omega_c$) | Stability analysis (especially tricky cases) |
| **Design tool?** | Yes — the primary design tool in this course | Mostly an analysis tool |
| **Handles delay?** | Harder to see delay effects | Naturally shows how delay spirals the curve toward $-1$ |

> [!tip] For This Course
> You'll primarily *design* controllers using Bode plots and *verify* stability using Nyquist. The Bode plot is your everyday tool; Nyquist is the safety check.

---

## 10. Controller Design: P, I, D and Their Combinations

> [!example] Detailed Treatment in Lecture Notes
> - P and PI basics, Ziegler-Nichols tuning: [[Lesson 2 - Block Diagrams and Control Concepts#6. Controllers|Lesson 2, Section 6]]
> - P-controller design via Bode plot: [[Day 6 - Bode and P-Controller Design]]
> - PI and Lead design procedure: [[Lesson 8 - Position Controller Design]]
> - PILead with time-domain specifications: [[Lesson 9 - PI-Lead Design with Specifications]]

The three building blocks of classical control are **Proportional**, **Integral**, and **Derivative** action. Each one responds to a different aspect of the error signal. Understanding them individually is the key to understanding any controller combination.

---

### 10.1 P-Controller (Proportional): React to the Present

$$C(s) = K_p$$

**Time domain:** $u(t) = K_p \cdot e(t)$

**What it sees:** The error *right now*.
**What it does:** Produces a control signal proportional to the current error. Big error = big correction. Small error = small correction.

> [!tip] Analogy: Steering a Car
> You see you're drifting 1 meter to the right. You turn the wheel left. The further you've drifted, the harder you turn. That's P-control — your correction is proportional to the current error.

**On a Bode plot:** $C(j\omega) = K_p$ at all frequencies. Pure gain, no phase shift. It lifts the entire magnitude curve up by $20\log_{10}(K_p)$ dB without touching the phase.

**The steady-state error problem — worked through:**

Consider a unity-feedback system with plant $G(s) = \frac{1}{s + 1}$ and P-controller $C(s) = K_p$. The closed-loop transfer function is:

$$T(s) = \frac{K_p \cdot \frac{1}{s+1}}{1 + K_p \cdot \frac{1}{s+1}} = \frac{K_p}{s + 1 + K_p}$$

For a unit step input $R(s) = 1/s$, the steady-state output (Final Value Theorem):

$$y_{ss} = \lim_{s \to 0} s \cdot \frac{1}{s} \cdot \frac{K_p}{s + 1 + K_p} = \frac{K_p}{1 + K_p}$$

So the steady-state error is:

$$e_{ss} = 1 - \frac{K_p}{1 + K_p} = \frac{1}{1 + K_p}$$

| $K_p$ | $y_{ss}$ | $e_{ss}$ |
|--------|----------|----------|
| 1 | 0.50 | 0.50 |
| 10 | 0.91 | 0.091 |
| 100 | 0.99 | 0.0099 |
| $\infty$ | 1.00 | 0 |

> [!important] Key Takeaway
> P-control can make $e_{ss}$ small by using high gain, but it can **never** make it exactly zero. You'd need infinite gain, which makes the system unstable. This is the fundamental reason we need integral action.

**Summary — P-controller effects:**

| Property | Effect of Increasing $K_p$ |
|----------|---------------------------|
| Rise time | Decreases (faster) |
| Overshoot | Increases |
| Steady-state error | Decreases (but never zero) |
| Stability | Degrades (less phase margin, eventually unstable) |
| Noise sensitivity | Unchanged (gain is flat across frequency) |

---

### 10.2 I-Action (Integral): Remember the Past

$$C_I(s) = \frac{K_i}{s}$$

**Time domain:** $u(t) = K_i \int_0^t e(\tau) \, d\tau$

**What it sees:** The *accumulated* error over all past time.
**What it does:** Even if the current error is tiny, if it has persisted for a long time, the integral is large and the control signal keeps growing.

> [!tip] Analogy: A Dripping Tap Filling a Bucket
> Each moment of error adds a drop to the bucket. The bucket (integral) never empties on its own. Even a tiny persistent drip (small constant error) eventually fills the bucket (large control signal). The only way to stop the bucket from filling is to stop the drip entirely — i.e., drive the error to *exactly* zero.

**Why it kills steady-state error — the mathematical argument:**

Suppose at steady state there is a constant error $e_{ss} \neq 0$. Then:

$$u(t) = K_i \int_0^t e_{ss} \, d\tau = K_i \cdot e_{ss} \cdot t \to \infty$$

The control signal grows without bound. But a physical system responds to increasing input by changing its output, which changes the error. The only equilibrium is when $e_{ss} = 0$, because that's the only value where the integral stops growing.

> [!important] The Integrator as a Pole at the Origin
> In the $s$-domain, $\frac{1}{s}$ is a pole at $s = 0$. This makes the loop gain **infinite at DC** ($\omega = 0$):
> $$|L(j\omega)| = |C(j\omega) \cdot G(j\omega)| \to \infty \text{ as } \omega \to 0$$
>
> From the closed-loop error transfer function $E(s) = \frac{1}{1 + L(s)} R(s)$, infinite loop gain at DC means $E(0) = 0$. Zero steady-state error — guaranteed by the math.

**On a Bode plot:** $\frac{1}{s}$ contributes:
- Magnitude: $-20$ dB/decade slope at all frequencies (drops continuously)
- Phase: $-90°$ at all frequencies

That constant $-90°$ phase is the cost. It eats directly into your phase margin.

**I-action alone is rarely used** because the $-90°$ phase lag makes it very easy to destabilize the system. It's almost always paired with P.

**Summary — I-action effects:**

| Property | Effect of Adding I-action |
|----------|--------------------------|
| Steady-state error | Eliminated (for step inputs) |
| Rise time | Can decrease slightly (more total gain at low freq) |
| Overshoot | Increases (phase lag reduces stability) |
| Stability | Degrades ($-90°$ phase at all frequencies) |
| Settling time | Often increases (oscillations take longer to die) |
| Disturbance rejection | Improved at low frequencies |

---

### 10.3 D-Action (Derivative): Predict the Future

$$C_D(s) = K_d \cdot s$$

**Time domain:** $u(t) = K_d \cdot \frac{de(t)}{dt}$

**What it sees:** The *rate of change* of the error.
**What it does:** If the error is changing fast (approaching the target quickly), it *brakes*. If the error is changing slowly, it does nothing.

> [!tip] Analogy: Braking a Car
> You're approaching a stop sign. P-action says "I'm still 10 meters away, keep driving." D-action says "I'm approaching at 50 km/h — that's too fast, I need to brake NOW even though I'm not there yet." D-action responds to *how fast* the error is changing, not how big it is.

**Why it reduces overshoot:**

When the output approaches the reference, $e(t)$ is decreasing rapidly — its derivative is large and negative. D-action produces a large negative (braking) control signal, slowing the approach before the system overshoots.

**On a Bode plot:** $K_d \cdot s$ contributes:
- Magnitude: $+20$ dB/decade (increases with frequency)
- Phase: $+90°$ at all frequencies

That $+90°$ is valuable — it directly adds to your phase margin. But the rising magnitude at high frequencies is a disaster: it **amplifies noise**.

> [!warning] Pure D is Never Used in Practice
> Real signals have high-frequency noise. A pure derivative amplifies noise infinitely. That's why we always use **filtered derivative** (Lead controller) instead:
> $$C_D(s) = K_d \cdot \frac{s}{(\tau_f s + 1)}$$
> The filter $\frac{1}{\tau_f s + 1}$ rolls off the gain at high frequencies, limiting noise amplification.

**Summary — D-action effects:**

| Property | Effect of Adding D-action |
|----------|--------------------------|
| Steady-state error | No effect (D sees rate of change, not constant offset) |
| Rise time | Slight increase (braking effect slows initial approach) |
| Overshoot | Significantly decreased (anticipatory braking) |
| Stability | Improved ($+90°$ phase boost) |
| Settling time | Decreased (less oscillation) |
| Noise sensitivity | Greatly increased (amplifies high-frequency noise) |

---

### 10.4 Side-by-Side Comparison: P vs I vs D

To build intuition, here's what each component "cares about":

```
                Past              Present           Future
                 │                   │                 │
     I-action ◄──┘                   │                 └──► D-action
     (integral of error)             │                     (derivative of error)
                                     │
                         P-action ◄──┘
                      (current error)
```

| | P | I | D |
|---|---|---|---|
| **Responds to** | Current error | Accumulated past error | Rate of change of error |
| **Transfer function** | $K_p$ | $K_i/s$ | $K_d s$ |
| **Phase contribution** | $0°$ | $-90°$ | $+90°$ |
| **Magnitude slope** | $0$ dB/dec (flat) | $-20$ dB/dec | $+20$ dB/dec |
| **Steady-state error** | Reduces, never zero | Eliminates | No effect |
| **Overshoot** | Increases with gain | Increases | Decreases |
| **Speed** | Increases with gain | Slight increase | Slight decrease |
| **Stability** | Neutral | Hurts ($-90°$) | Helps ($+90°$) |
| **Noise** | Neutral | Neutral | Amplifies |
| **Analogy** | Steering correction | Persistent nudge | Anticipatory braking |

---

### 10.5 Combinations: PI, PD, PID

#### 10.5.1 PI-Controller

$$C_{PI}(s) = K_p + \frac{K_i}{s} = K_p\left(1 + \frac{1}{\tau_i s}\right) = K_p \frac{\tau_i s + 1}{\tau_i s}$$

where $\tau_i = K_p / K_i$ is the **integral time constant**.

**What it is structurally:** A pole at $s = 0$ and a zero at $s = -1/\tau_i$.

**How the pieces work together:**
- The **integrator** (pole at origin) gives infinite DC gain $\to$ zero steady-state error
- The **zero** at $s = -1/\tau_i$ partially recovers the phase lost by the integrator

**Phase contribution of PI:**

$$\angle C_{PI}(j\omega) = \arctan(\omega \tau_i) - 90°$$

| Frequency | Phase |
|-----------|-------|
| $\omega \ll 1/\tau_i$ | $\approx -90°$ (integrator dominates) |
| $\omega = 1/\tau_i$ | $-45°$ (zero kicks in) |
| $\omega \gg 1/\tau_i$ | $\approx 0°$ (zero cancels integrator phase) |

> [!important] Design Rule for PI
> Place the PI zero **well below** the crossover frequency ($1/\tau_i \ll \omega_c$). This means at $\omega_c$, the phase penalty from PI is small (close to $0°$ instead of $-90°$).
>
> In the course, this is controlled by $N_i$: $\tau_i = N_i / \omega_c$, with $N_i \geq 3$ ensuring the zero is at least 3x below crossover. Higher $N_i$ = less phase penalty but slower integral action.

**When to use PI:** When you need zero steady-state error for step inputs and the plant has enough phase margin to absorb the (small) phase penalty.

#### 10.5.2 PD-Controller

$$C_{PD}(s) = K_p + K_d s = K_p(1 + \tau_d s)$$

where $\tau_d = K_d / K_p$ is the **derivative time constant**.

**What it is structurally:** A zero at $s = -1/\tau_d$. No poles (in the ideal case).

**How the pieces work together:**
- **P** provides the baseline correction
- **D** (the zero) adds phase lead around $\omega = 1/\tau_d$, improving stability

**The noise problem:** In practice, pure PD amplifies noise at high frequencies. Always use a filtered version:

$$C_{PD}(s) = K_p \cdot \frac{\tau_d s + 1}{\alpha\tau_d s + 1}, \quad 0 < \alpha < 1$$

This is exactly the **Lead controller** from the course. The denominator $\alpha\tau_d s + 1$ is the noise filter — it limits the high-frequency gain to $1/\alpha$ instead of infinity.

**When to use PD/Lead:** When you need more phase margin at the crossover frequency (system is close to instability or you want less overshoot).

#### 10.5.3 PID-Controller

$$C_{PID}(s) = K_p\left(1 + \frac{1}{\tau_i s} + \tau_d s\right)$$

**The complete package:** Combines all three actions.

| Component | Job | Frequency Range |
|-----------|-----|-----------------|
| I | Zero steady-state error | Low frequencies ($\omega \ll \omega_c$) |
| P | Baseline correction | Mid frequencies (around $\omega_c$) |
| D | Phase boost, overshoot reduction | High frequencies (around $\omega_c$ and above) |

> [!tip] PID as "Division of Labor"
> Think of PID as three specialists working together:
> - **I** handles the long game — "we've been off-target for a while, let me slowly correct"
> - **P** handles the present — "we're off by this much, correct proportionally"
> - **D** handles fast changes — "we're approaching too fast, slow down!"
>
> Each one dominates in its frequency range and is largely passive outside it.

**In this course** we use the **PILead** form, which is a practical PID:

$$C_{PILead}(s) = K_p \cdot \underbrace{\frac{\tau_i s + 1}{\tau_i s}}_{\text{PI}} \cdot \underbrace{\frac{\tau_d s + 1}{\alpha\tau_d s + 1}}_{\text{Lead (filtered D)}}$$

This separates the controller into modular, independently tunable blocks rather than mixing all three gains.

---

### 10.6 Summary: How Each Component Affects the Bode Plot

Understanding what happens on the Bode plot is the key to the design procedure:

| Component | Magnitude Effect | Phase Effect |
|-----------|-----------------|--------------|
| $K_p$ (gain) | Shifts entire curve up/down | No effect |
| $\frac{1}{\tau_i s}$ (integrator) | $-20$ dB/dec slope, infinite gain at DC | $-90°$ everywhere |
| Zero at $-1/\tau_i$ | $+20$ dB/dec above $1/\tau_i$ | $+45°$ at $1/\tau_i$, $+90°$ well above |
| Zero at $-1/\tau_d$ | $+20$ dB/dec above $1/\tau_d$ | $+45°$ at $1/\tau_d$, $+90°$ well above |
| Pole at $-1/(\alpha\tau_d)$ | $-20$ dB/dec above $1/(\alpha\tau_d)$ | $-45°$ at $1/(\alpha\tau_d)$, $-90°$ well above |

**The net effect of PILead on the Bode plot:**
1. At **very low frequencies**: magnitude rises steeply (integrator) $\to$ huge gain $\to$ small errors
2. At **mid frequencies** (near $\omega_c$): the lead zero boosts phase, the PI zero has already recovered from integrator lag
3. At **high frequencies**: the lead pole rolls off gain $\to$ noise rejection

---

### 10.7 Choosing a Controller: Decision Guide

```
Do you need zero steady-state error?
├── No → P or PD/Lead may suffice
└── Yes → You need I-action (PI or PILead)
        │
        Does the plant have enough phase margin with just PI?
        ├── Yes → Use PI
        └── No → Add Lead (→ PILead)
```

| Controller | Use When... | REGBOT Example |
|------------|------------|----------------|
| P | Simple, fast response okay, $e_{ss}$ acceptable | Velocity control (Day 6) |
| PI | Need $e_{ss} = 0$, plant is simple enough | — |
| Lead (PD) | Need more phase margin / less overshoot | — |
| PILead | Need $e_{ss} = 0$ AND more phase margin | Position control (Day 8-9) |

---

### 10.8 The PILead Design Procedure (Phase Balance)

This is the "cookbook" from Lessons 8-9, but now you understand *why* each step exists:

> [!important] The Design Procedure (Phase Balance Equation)
> At the crossover frequency $\omega_c$, the total phase must equal the desired phase margin minus 180 degrees:
> $$\angle C(j\omega_c) + \angle G(j\omega_c) = \gamma_M - 180°$$
>
> You know $\angle G(j\omega_c)$ from the Bode plot of your plant. You choose $\gamma_M$ (typically 50-65 degrees). The controller must provide the remaining phase. This single equation drives the entire design.

**Step-by-step with the "why":**

| Step | Action                                                                                            | Why                                                               |
| ---- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1    | Choose $\omega_c$ from specs                                                                      | $\omega_c$ determines closed-loop bandwidth (speed)               |
| 2    | Choose $\gamma_M$ from specs                                                                      | $\gamma_M$ determines overshoot and robustness                    |
| 3    | Read $\angle G(j\omega_c)$ from Bode plot                                                         | This is the plant's phase at the frequency where we want $L=1$    |
| 4    | Calculate needed controller phase: $\phi_C = \gamma_M - 180° - \angle G(j\omega_c)$               | The controller must supply whatever phase the plant doesn't       |
| 5    | Choose $N_i \geq 3$, compute PI phase: $\phi_{PI} = \arctan(N_i) - 90°$                           | PI contributes a small negative phase (smaller with larger $N_i$) |
| 6    | Required lead phase: $\phi_{Lead} = \phi_C - \phi_{PI}$                                           | Lead must make up the remainder                                   |
| 7    | Calculate $\alpha$ from $\phi_{Lead}$: $\alpha = \frac{1 - \sin\phi_{Lead}}{1 + \sin\phi_{Lead}}$ | Determines how aggressive the lead is                             |
| 8    | Calculate $\tau_i$, $\tau_d$ from $\omega_c$, $N_i$, $\alpha$                                     | Places the PI zero and lead zero/pole at the right frequencies    |
| 9    | Calculate $K_p$ so $L(j\omega_c)= 1$                                                              | Sets the gain to hit the crossover frequency exactly              |

---

## 11. Type-n Systems and Steady-State Error

> [!example] Detailed Treatment
> - Type-n systems and steady-state error: [[Lesson 9 - PI-Lead Design with Specifications]]
> - Integrator discussion: [[Lesson 8 - Position Controller Design]]

### 11.1 What is a "Type-n" System?

The **type number** of a control loop = the number of **integrators** ($1/s$ terms) in the **open-loop** transfer function $L(s) = C(s)G(s)$.

| Open-loop $L(s)$ | Integrators | Type |
|---|---|---|
| $\frac{10}{s + 5}$ | 0 | Type-0 |
| $\frac{10}{s(s + 5)}$ | 1 ($s$ in denominator) | Type-1 |
| $\frac{10}{s^2(s + 5)}$ | 2 ($s^2$ in denominator) | Type-2 |

The integrators can come from the **plant** (e.g., position is the integral of velocity) or the **controller** (PI adds one integrator).

> [!tip] How to Count
> Factor the denominator of $L(s)$ and count how many bare $s$ factors there are. The rest of the poles (like $s + 5$) don't count — only the ones at the origin ($s = 0$).

### 11.2 Why Type Number Matters: The Steady-State Error Rules

The type number tells you **what kinds of reference signals the system can track with zero error**:

| System Type | Step input ($r = \text{const}$) | Ramp input ($r = t$) | Parabola input ($r = t^2$) |
|---|---|---|---|
| Type-0 | $e_{ss} = \frac{1}{1 + K_p} \neq 0$ | $e_{ss} = \infty$ | $e_{ss} = \infty$ |
| Type-1 | $e_{ss} = 0$ ✓ | $e_{ss} = \frac{1}{K_v} \neq 0$ | $e_{ss} = \infty$ |
| Type-2 | $e_{ss} = 0$ ✓ | $e_{ss} = 0$ ✓ | $e_{ss} = \frac{1}{K_a} \neq 0$ |

Where $K_p$, $K_v$, $K_a$ are position, velocity, and acceleration error constants.

> [!important] The Simple Rule
> **Each integrator "eats" one level of input complexity:**
> - 0 integrators → can't perfectly track even a constant (step)
> - 1 integrator → can track a constant, but not a ramp
> - 2 integrators → can track a constant and a ramp, but not a parabola
>
> Pattern: Type-$n$ system has $e_{ss} = 0$ for inputs up to $t^{n-1}$, and non-zero $e_{ss}$ for $t^n$.

### 11.3 Why Does This Work? (Intuition)

Think of it this way: an integrator's output keeps growing as long as its input is non-zero. 

**Type-0 with a step input:** The error settles to some constant. There's no integrator to "push" it to zero, so it stays.

**Type-1 with a step input:** If there's any constant error, the integrator accumulates it and pushes the control signal up. The error *must* go to zero because that's the only equilibrium.

**Type-1 with a ramp input:** The reference keeps increasing at a constant rate. The integrator can keep up with a constant rate, but it needs a constant non-zero error to feed it. So $e_{ss} \neq 0$ but is finite.

**Type-2 with a ramp input:** The second integrator accumulates the remaining constant error from the first, pushing it to zero. Now both can be zero.

> [!tip] Analogy: Gears in a Car
> - **Type-0:** A car without cruise control. Give it a constant throttle and it reaches some speed, but probably not exactly 100 km/h.
> - **Type-1:** Cruise control that adjusts throttle until speed matches the target. Works perfectly for constant speed, but if you want to accelerate at a constant rate, it'll always lag a bit.
> - **Type-2:** Cruise control that *also* tracks acceleration. Can perfectly follow a speed ramp.

### 11.4 REGBOT Examples

| System | Plant | Controller | Loop $L(s)$ | Type | $e_{ss}$ to step |
|---|---|---|---|---|---|
| Velocity with P | $\frac{13.34}{s+35.71}$ | $K_p$ | $\frac{13.34 K_p}{s+35.71}$ | Type-0 | $\frac{1}{1+K_p K_{ss}} \neq 0$ |
| Velocity with PI | $\frac{13.34}{s+35.71}$ | $K_p\frac{\tau_i s + 1}{\tau_i s}$ | $\frac{(\ldots)}{s(s+35.71)}$ | Type-1 | $0$ ✓ |
| Position with PI | $\frac{13.34}{s(s+35.71)}$ | $K_p\frac{\tau_i s + 1}{\tau_i s}$ | $\frac{(\ldots)}{s^2(s+35.71)}$ | Type-2 | $0$ ✓ (also ramp!) |

> [!important] Design Implication
> When the specification says $e_{ss} = 0$ for a step input, you need at least **Type-1** → at least one integrator in the loop. If the plant doesn't have one, your controller must add one (→ use PI or PILead).

---

## 12. Connecting It All: The Design Flow

```
Specifications (rise time, overshoot, e_ss)
         │
         ▼
Map to frequency-domain specs (ω_c, γ_M, system type)
         │
         ▼
Measure/model the plant G(s) (e.g., from REGBOT step response)
         │
         ▼
Read Bode plot of G(s) at desired ω_c
         │
         ▼
Design C(s) using phase balance equation
         │
         ▼
Simulate closed-loop response
         │
         ▼
Test on real system (REGBOT)
         │
         ▼
Iterate if needed
```

### 12.1 Specification Mapping

| Time-domain spec | Maps to... | How? |
|-----------------|------------|------|
| Rise time $t_r$ | Crossover frequency $\omega_c$ | $\omega_c \approx 1.8/t_r$ (for 2nd order) |
| Overshoot $M_p$ | Phase margin $\gamma_M$ | $\gamma_M \approx 100\zeta$ degrees (for $\zeta < 0.7$), and $M_p = e^{-\pi\zeta/\sqrt{1-\zeta^2}}$ |
| Steady-state error $e_{ss} = 0$ | System type | Need integrator in loop (PI controller) |
| Settling time $t_s$ | Also relates to $\omega_c$ and $\zeta$ | $t_s \approx 4.6/(\zeta\omega_n)$ |

---

## 13. Quick Reference: "What Does This Mean Physically?"

| Concept | Physical Meaning |
|---------|-----------------|
| Transfer function $G(s)$ | How the system transforms input to output |
| Pole at $s = -a$ | Exponential mode with time constant $\tau = 1/a$ |
| Complex poles $-a \pm j\omega$ | Oscillation at $\omega$, decaying at rate $a$ |
| Zero at $s = -z$ | Frequency where system output cancels |
| DC gain $K_{ss}$ | Amplification of constant (DC) signals |
| Crossover frequency $\omega_c$ | Bandwidth of control — how fast the loop reacts |
| Phase margin $\gamma_M$ | Safety buffer before instability |
| Gain margin GM | How much gain increase before instability |
| Integrator ($1/s$) | Memory — accumulates error over time |
| Time constant $\tau$ | Time to reach 63.2% of final value |
| Damping ratio $\zeta$ | Amount of "shock absorption" in the response |
| Natural frequency $\omega_n$ | Oscillation frequency without damping |

---

## 14. Common Mistakes and Misconceptions

> [!warning] Misconception: "Higher gain is always better"
> Higher gain gives faster response but reduces stability margins. There is always an optimal range.

> [!warning] Misconception: "Stability means the system works well"
> A system can be stable but have 50% overshoot, 10 second settling time, and non-zero steady-state error. Stability is the **minimum** requirement, not the goal.

> [!warning] Misconception: "The Laplace transform changes the system"
> No. It changes the **representation**. The physical system is the same. Laplace is a mathematical tool, like switching from Cartesian to polar coordinates.

> [!warning] Misconception: "Phase margin is just a number to calculate"
> Phase margin directly predicts transient behavior. $\gamma_M \approx 45°$ gives $\sim 20\%$ overshoot. $\gamma_M \approx 65°$ gives $\sim 5\%$ overshoot. It's the most practical design parameter.

---

*Last updated: 2026-04-08*
*Status: Sections 1-14 cover material through Lesson 9. To be extended as new topics are introduced.*
