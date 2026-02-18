---
course: "34722"
course-name: "Linear Control Design 1"
type: lecture-note
week: 7
tags: [LCD, lecture]
date: 2026-02-18
---
# Lesson 3 - Laplace Transform and Transfer Functions

> [!abstract] Lecture Overview
> Lesson 3/13 — Teachers: Silvia Tolu & Dimitrios Papageorgiou
> Topics: Hand-tuning PD/PID controllers, the Laplace Transform, phasors, transfer functions from physical systems, block diagram construction.
> Schedule: 13:00–15:00 Lecture, 15:00–17:00 Block diagram exercises.

> [!example] Related Materials
> - Slides: [[3_Laplace_TF.pdf]]
> - Exercise: [[Day 3 - Block Diagram Exercise]]
> - Assignment: [[Assignment_3_BlockDiagrams.pdf]]
> - Previous: [[Lesson 2 - Block Diagrams and Control Concepts]]

---

## 1. Hand-Tuning: PD and PID Controllers

Building on P and PI from Lesson 2, this lecture introduces derivative action.

### PD Controller

$$u(t) = K_p\left(e(t) + \tau_d \frac{d}{dt}e(t)\right)$$

The derivative term reacts to the **rate of change** of the error — it provides a "kick" when the reference changes suddenly (step input), speeding up the initial response.

**Tuning recipe:**
1. Start with a reasonable $K_p$ (from hand-tuning experience)
2. Set $\tau_d$ in the same order as the observed rise time
3. If oscillation/overshoot → increase $\tau_d$, decrease $K_p$
4. To make faster → decrease $\tau_d$, increase $K_p$

**Example values:** $K_p = 50$, $\tau_d = 0.1$ s → refined to $K_p = 500$, $\tau_d = 0.02$ s

![[3_Laplace_TF.pdf#page=3]]

### PID Controller

$$u(t) = K_p\left(e(t) + \frac{1}{\tau_i}\int e(t)\,dt + \tau_d \frac{d}{dt}e(t)\right)$$

Combines all three actions: P (proportional), I (integral, removes steady-state error), D (derivative, improves transient response).

**Tuning guidelines:**

| Parameter | Increase | Decrease |
|-----------|----------|----------|
| $K_p$ | Faster response, less SS error, more overshoot | More stable, slower |
| $\tau_i$ | Weaker I-action, more stable | Faster SS error removal, more oscillation |
| $\tau_d$ | More damping, less overshoot | Faster rise time, less damping |

> [!warning] I-term speed
> If $\tau_i$ is too small (I-action too fast), the system may oscillate violently. A practical starting point: $\tau_i \approx$ time to reach steady state.

![[3_Laplace_TF.pdf#page=5]]

---

## 2. Modelling from First Principles

$$\text{Physical System} \xrightarrow{\text{Assumptions}} \text{Math Model} \xrightarrow{\text{Linearize + Laplace}} \text{Transfer Function } G(s)$$

**Example: Mass-Spring System**

Physical system: mass $m$ on a spring with stiffness $K$, subject to gravity $g$ and external force $f(t)$.

$$\sum F = m\ddot{x}(t) \quad \Rightarrow \quad \ddot{x}(t) = -\frac{k}{m}x(t) + g + \frac{1}{m}f(t)$$

To build the block diagram:
1. **Isolate** the highest derivative ($\ddot{x}$)
2. **Add integrators** ($\frac{1}{s}$) — as many as the order of the equation
3. **Add feedback** for lower-order terms ($x$ fed back through $k/m$)
4. **Add inputs** ($f$ through $1/m$, constant $g$)

![[3_Laplace_TF.pdf#page=12]]

---

## 3. The Laplace Transform

### Definition

$$F(s) = \mathcal{L}\{f(t)\} = \int_0^{\infty} f(t) \, e^{-st} \, dt$$

where $s = \sigma + j\omega$ is a complex frequency variable.

**Key properties:**
- $f(t) = 0$ for $t < 0$ (causal signals)
- Differential equations become **polynomial** algebra in $s$
- $s$ can be interpreted as a frequency: $j\omega$ is the physical frequency

### Laplace Calculation Rules

| $f(t)$ | $F(s)$ | Operation |
|--------|--------|-----------|
| $Af(t)$ | $AF(s)$ | Scaling |
| $f_1 + f_2$ | $F_1 + F_2$ | Addition |
| $\frac{d}{dt}f(t)$ | $sF(s) - f(0)$ | Differentiation |
| $\frac{d^2}{dt^2}f(t)$ | $s^2 F(s) - sf(0) - f'(0)$ | 2nd derivative |
| $\int_0^t f(\tau)\,d\tau$ | $\frac{1}{s}F(s)$ | Integration |
| $\lim_{t \to 0} f(t)$ | $\lim_{s \to \infty} sF(s)$ | Initial value |
| $\lim_{t \to \infty} f(t)$ | $\lim_{s \to 0} sF(s)$ | Final value |

![[3_Laplace_TF.pdf#page=15]]

### Common Laplace Pairs

| $f(t)$ | $F(s)$ | Description |
|--------|--------|-------------|
| $\delta(t)$ | $1$ | Unit impulse |
| $u(t)$ (step) | $\frac{1}{s}$ | Unit step |
| $e^{-at}$ | $\frac{1}{s+a}$ | Exponential decay |
| $t$ | $\frac{1}{s^2}$ | Ramp |
| $te^{-at}$ | $\frac{1}{(s+a)^2}$ | Damped ramp |
| $\sin(bt)$ | $\frac{b}{s^2+b^2}$ | Sine |
| $\cos(bt)$ | $\frac{s}{s^2+b^2}$ | Cosine |
| $e^{-at}\sin(bt)$ | $\frac{b}{(s+a)^2+b^2}$ | Damped sine |

![[3_Laplace_TF.pdf#page=16]]

---

## 4. Transfer Functions from Physical Systems

### Water Tank Example

Input: flow rate $Q(t)$ [m$^3$/s], Output: water height $h(t)$ [m], Tank area: $A = r^2\pi$

$$h(t) = \frac{1}{A}\int_0^t Q(\tau)\,d\tau \quad \Rightarrow \quad \frac{H(s)}{Q(s)} = \frac{1}{r^2\pi \cdot s}$$

Block diagram: $Q(s) \to [1/r^2\pi] \to [1/s] \to H(s)$

### RL Circuit Example

Input: voltage $V(s)$, Output: current $I(s)$

$$V(s) \to \Sigma(+,-) \to [1/L] \to [1/s] \to I(s), \quad \text{feedback: } I \to [R] \to (-)\Sigma$$

Transfer function (closed-loop reduction):

$$\frac{I(s)}{V(s)} = \frac{1/(Ls)}{1 + R/(Ls)} = \frac{1}{Ls + R}$$

**Limiting cases:**
- $L \to 0$: $\frac{I}{V} \to \frac{1}{R}$ (Ohm's law, pure resistor)
- Steady state ($s \to 0$): $I_{ss} = \frac{A}{R}$ for a step input of amplitude $A$

![[3_Laplace_TF.pdf#page=20]]

---

## 5. Control Questions — Laplace Domain

### Question 1: Constant Input Through a Transfer Function

Given: $G(s) = \frac{s}{s+10}$, constant input $v(t) = 5$

**a)** Laplace of a constant: $V(s) = \frac{5}{s}$

**b)** Output in s-domain:
$$\dot{x}(s) = V(s) \cdot G(s) = \frac{5}{s} \cdot \frac{s}{s+10} = \frac{5}{s+10}$$

**c)** Inverse Laplace (using $\frac{1}{s+a} \leftrightarrow e^{-at}$):
$$\dot{x}(t) = 5e^{-10t}$$

### Question 2: Exponential Input

Given: $v(t) = e^{-3t}$, same $G(s)$

$$V(s) = \frac{1}{s+3}, \quad \dot{X}(s) = \frac{1}{s+3} \cdot \frac{s}{s+10} = \frac{s}{(s+3)(s+10)}$$

Partial fraction expansion → $\dot{x}(t) = 1.43e^{-10t} - 0.43e^{-3t}$

![[3_Laplace_TF.pdf#page=25]]

---

## 6. Electronic Components in Laplace Domain

### Capacitor

$$v_C(t) = \frac{1}{C}\int_0^t i_C(\tau)\,d\tau \quad \Rightarrow \quad Z_C(s) = \frac{V_C(s)}{I_C(s)} = \frac{1}{sC}$$

### Inductor

$$v_L(t) = L\frac{d}{dt}i(t) \quad \Rightarrow \quad Z_L(s) = \frac{V_L(s)}{I(s)} = sL$$

> [!tip] Audio Relevance
> These impedances are the foundation of filter design:
> - Low-pass: $\frac{1}{sC}$ dominates at high frequency → attenuates
> - High-pass: $sL$ dominates at low frequency → attenuates
> - The $s = j\omega$ substitution connects directly to Bode plot analysis

![[3_Laplace_TF.pdf#page=27]]

---

## 7. Frequency, Phasors, and the Laplace Connection

### Key Principle

> In a **linear system**, if a sinusoidal signal goes **in**, a sinusoidal signal comes **out** at the **same frequency**, but with changed **amplitude** and **phase**.

### Phasor Representation

A sinusoid $f(\omega, t) = A\cos(\omega t + \theta)$ is represented as:

$$F = Ae^{j\theta} = A(\cos\theta + j\sin\theta) = A\angle\theta$$

The phasor is a **complex number** encoding amplitude $A$ and phase $\theta$.

### Laplace-Phasor Connection

The phasor is a **special case** of the Laplace transform where $\sigma = 0$:

$$s = \sigma + j\omega \xrightarrow{\sigma = 0} s = j\omega$$

So evaluating $G(j\omega)$ gives the **frequency response** (magnitude and phase) directly.

![[3_Laplace_TF.pdf#page=33]]

---

## 8. Phasor Examples

### Example I: First-Order System

$$G(s) = \frac{10}{s + 312}, \quad \omega = 628 \text{ rad/s}, \quad u(t) = \cos(\omega t)$$

Evaluate at $s = j\omega$:

$$G(j\omega) = \frac{10}{j628 + 312}$$

- Denominator magnitude: $A = \sqrt{628^2 + 312^2} = 700$
- $M = \frac{10}{700} = 0.0143$
- $\varphi = 0 - \arctan\frac{628}{312} = -63.6°$

$$G(j\omega) = 0.0143 \, e^{-j63.6°}$$

```matlab
s = tf('s'); G = 10/(s + 312);
z = evalfr(G, 628*i);
z_mag = abs(z);                    % 0.0143
z_phase = rad2deg(angle(z));       % -63.6°
```

### Example II: Second-Order System (Mass-Spring-Damper)

$$G(s) = \frac{40}{s^2 + 4s + 40} \quad (\omega_0 = \sqrt{40}, \; \zeta = 0.316)$$

$$G(j\omega) = \frac{40}{(j\omega)^2 + 4j\omega + 40} = \frac{40}{(-\omega^2 + 40) + 4j\omega}$$

| $\omega$ | $M$ | $\varphi$ |
|-----------|-----|-----------|
| $0.1$ | $\approx 1.0$ | $-0.57°$ |
| $1000$ | $\approx 40 \cdot 10^{-6}$ | $-180°$ |
| $\sqrt{40}$ | $\approx 1.5$ | $-90°$ |

> [!note] Resonance at $\omega = \omega_0$
> At $\omega = \sqrt{40} \approx 6.32$ rad/s, the real part of the denominator vanishes ($-\omega^2 + 40 = 0$), leaving only the imaginary part $4j\omega$. The phase is exactly $-90°$ and the magnitude peaks — this is **resonance**.

![[3_Laplace_TF.pdf#page=41]]

---

## 9. Mass-Spring-Damper Transfer Function

From Newton's second law: $M\ddot{y} = -ky - \beta\dot{y} + F$

With $k = \omega_0^2$, $\beta = 2\zeta\omega_0$, $M = 1$:

$$G(s) = \frac{\omega_0^2}{s^2 + 2\zeta\omega_0 s + \omega_0^2}$$

**Simulink implementation** (from the lecture):

$$y(s) = \frac{40}{s^2 + 4s + 40}u(s) \quad \Leftrightarrow \quad \ddot{y} = -40y - 4\dot{y} + 40u$$

Block diagram: $u \to [40] \to \Sigma(+,-,-) \to [1/s] \to \dot{y} \to [1/s] \to y$, with feedback $\dot{y} \to [4]$ and $y \to [40]$ to the summing junction.

![[3_Laplace_TF.pdf#page=47]]

---

## Key Formulas

> [!abstract] Quick Reference
> | Concept | Formula |
> |---------|---------|
> | Laplace transform | $F(s) = \int_0^\infty f(t)e^{-st}dt$ |
> | Integration in s | $\int f \to \frac{1}{s}F(s)$ |
> | Differentiation in s | $\dot{f} \to sF(s) - f(0)$ |
> | Closed-loop TF | $\frac{\text{Forward}}{1 + \text{Loop}}$ |
> | Frequency response | $G(j\omega) = Me^{j\varphi}$ |
> | Capacitor impedance | $Z_C = \frac{1}{sC}$ |
> | Inductor impedance | $Z_L = sL$ |
> | Final value theorem | $\lim_{t\to\infty} f(t) = \lim_{s\to 0} sF(s)$ |

---

> [!nav]
> [[Lesson 2 - Block Diagrams and Control Concepts|← Lesson 2]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
