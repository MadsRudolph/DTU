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

In Lesson 2 we saw P and PI controllers. This lecture completes the picture by adding derivative action, giving us the full PID controller.

### 1.1 PD Controller

$$u(t) = K_p\left(e(t) + \tau_d \frac{d}{dt}e(t)\right)$$

**What the D-term does physically:** The derivative term looks at how *fast* the error is changing, not just how big it is. When the reference suddenly jumps (a step input), the derivative of the error spikes, producing a large initial control signal. This "kick" gets the system moving quickly — like pressing the gas pedal harder at the start rather than gradually ramping up.

**Why this helps:** A P-controller alone only reacts to the current error. If the error is still large, it pushes hard; once the error is small, it eases off. The problem is that by the time the error is small, the system already has momentum and overshoots. The D-term acts as a **brake** — when the error is decreasing rapidly (meaning the system is approaching the target), the D-term produces a *negative* contribution that slows the approach, reducing overshoot.

> [!tip] Analogy
> Think of parking a car. The P-term is the distance to the parking spot (error). The D-term is your speed of approach. Even if you're still far away, if you're approaching too fast, you need to brake. That's what the D-term does.

**Tuning recipe:**
1. Start with a reasonable $K_p$ (from hand-tuning experience in Lesson 2)
2. Set $\tau_d$ in the same order of magnitude as the observed **rise time** of the P-only response
3. If there is still oscillation or overshoot → **increase** $\tau_d$ (more braking) and **decrease** $K_p$
4. To make the system faster → **decrease** $\tau_d$ and **increase** $K_p$

**Example from lecture:** Starting with $K_p = 50$, $\tau_d = 0.1$ s, the system tracks the 10° reference in about 0.3 s. Refining to $K_p = 500$, $\tau_d = 0.02$ s gives a much faster response (~0.05 s) while keeping overshoot minimal.

![[3_Laplace_TF.pdf#page=3]]

![[3_Laplace_TF.pdf#page=4]]

### 1.2 PID Controller

$$u(t) = K_p\left(e(t) + \frac{1}{\tau_i}\int e(t)\,dt + \tau_d \frac{d}{dt}e(t)\right)$$

The PID controller combines all three actions. Each term addresses a different aspect of the control problem:

| Term | What it does | What it fixes |
|------|-------------|---------------|
| **P** ($K_p \cdot e$) | Reacts to current error | Provides immediate response |
| **I** ($\frac{K_p}{\tau_i}\int e\,dt$) | Accumulates past error | Eliminates steady-state error |
| **D** ($K_p \tau_d \dot{e}$) | Predicts future error (from rate of change) | Reduces overshoot, improves transient |

**How the three terms interact:** The P-term does most of the work. The I-term slowly builds up to eliminate any remaining offset that P alone cannot fix (recall from Lesson 2: P-controllers have steady-state error). The D-term dampens the response to prevent the P and I terms from causing overshoot.

> [!warning] I-term speed matters
> If $\tau_i$ is too small (I-action too aggressive), the integral builds up rapidly, causing the system to oscillate violently. This is especially dangerous because the integral "remembers" — even after the error is zero, the accumulated integral continues to drive the output, causing the system to overshoot in the other direction (known as **integral windup**).
>
> A practical starting point: set $\tau_i \approx$ the time it takes the P-only system to reach steady state.

### 1.3 PID Tuning Summary

**Effect of changing each parameter:**

| Parameter | Increase | Decrease |
|-----------|----------|----------|
| $K_p$ | Faster response, less steady-state error, **but** more overshoot and risk of instability | More stable and less overshoot, **but** slower and larger steady-state error |
| $\tau_i$ | Weaker I-action → more stable, **but** slower steady-state error removal | Stronger I-action → faster removal of SS error, **but** more oscillation risk |
| $\tau_d$ | More damping → less overshoot, **but** slower overall response | Less damping → faster rise time, **but** more overshoot |

**Initial parameter estimates (from lecture slide 7):**
- **$K_p$**: Estimate $K_p \approx u_0 / e_0$, where $u_0$ is the expected control effort and $e_0$ is the initial error from a step change
- **$\tau_i$**: Start with $\tau_i \approx$ time for the output to reach steady state
- **$\tau_d$**: Start with $\tau_d \approx \tau_i$ or based on the observed rise time

![[3_Laplace_TF.pdf#page=5]]

![[3_Laplace_TF.pdf#page=8]]

---

## 2. Modelling from First Principles

Before we can control a system, we need a mathematical model of it. This section covers the process of going from a physical system to a transfer function.

### 2.1 The Modelling Pipeline

$$\text{Physical System} \xrightarrow[\text{Simplifications}]{\text{Assumptions}} \text{Math Model} \xrightarrow{\text{Linearize + Laplace}} \text{Transfer Function } G(s)$$

**Step 1 — Physical system:** Identify what you're controlling (a motor, a tank, a room, etc.)

**Step 2 — Assumptions:** Simplify the real system. For example, "the object is a particle" (no mass distribution), "friction is linear", "temperature is uniform". These simplifications make the math tractable while hopefully capturing the essential dynamics.

**Step 3 — First principles:** Apply fundamental physical laws:
- **Mechanics:** Newton's laws ($F = ma$, $\tau = J\dot{\omega}$)
- **Electrical:** Kirchhoff's laws, Ohm's law ($V = RI$, $V = L\frac{dI}{dt}$, $I = C\frac{dV}{dt}$)
- **Thermodynamics:** Energy balance, heat flow
- **Fluid dynamics:** Mass conservation, flow equations

**Step 4 — Linearize** around an operating point (if the model is nonlinear)

**Step 5 — Laplace transform** to get $Y(s) = G(s) \cdot U(s)$

![[3_Laplace_TF.pdf#page=9]]

### 2.2 Example: Mass-Spring System

**Physical system:** A mass $m$ hanging from a spring with stiffness constant $k$, subject to gravity $g$ and an external perturbation force $f(t)$.

**Assumptions:** The object is a point mass (no inertia distribution), the spring is linear (force proportional to displacement), and we measure displacement $x(t)$ from the equilibrium position.

**Applying Newton's 2nd law:**

$$\sum F = m\ddot{x}(t) \quad \Rightarrow \quad f_k + f(t) + mg = m\ddot{x}(t)$$

Where the spring force $f_k = -k \cdot x(t)$ (restoring force, proportional to displacement).

Rearranging to isolate the highest derivative:

$$\ddot{x}(t) = -\frac{k}{m}x(t) + g + \frac{1}{m}f(t)$$

This is a **second-order ODE**. The key insight for building the block diagram is that we have $\ddot{x}$ expressed in terms of $x$ and the inputs — which means we need feedback from $x$ back to create $\ddot{x}$.

### 2.3 Building the Block Diagram from the ODE

The method from the lecture (5 steps):

1. **Isolate the highest derivative** ($\ddot{x}$) — this becomes the "starting signal" of the chain
2. **Add integrators** ($\frac{1}{s}$) — as many as the order of the equation (here: 2). Each integrator reduces the derivative order: $\ddot{x} \to [1/s] \to \dot{x} \to [1/s] \to x$
3. **Add feedback** — every term on the right side of the equation that involves a state variable ($x$, $\dot{x}$) creates a feedback path. Here: $x$ fed back through gain $k/m$ to the (−) of the summing junction
4. **Add inputs** — the external force $f(t)$ enters through gain $1/m$ and gravity $g$ enters as a constant, both at the summing junction
5. **Set constants and gains** — label each block with its physical parameter

![[3_Laplace_TF.pdf#page=11]]

![[3_Laplace_TF.pdf#page=12]]

> [!important] Why This Method Works
> Integration is the fundamental operation. We start from $\ddot{x}$ (acceleration) and integrate twice to get position $x$. The feedback paths "close the loop" — the current position $x$ affects the acceleration through the spring force $-\frac{k}{m}x$. This is exactly how physical systems work: the current state determines the forces, which determine the acceleration, which changes the state.

---

## 3. The Laplace Transform

The Laplace transform is the **central mathematical tool** of this course. It converts differential equations (hard to solve) into algebraic equations (easy to solve), and it connects the time domain to the frequency domain.

### 3.1 Why Do We Need Laplace?

Consider a simple differential equation like $\dot{y} + 3y = 5u$. To find $y(t)$ given some input $u(t)$, we'd need to solve this ODE — which requires techniques like integrating factors or variation of parameters. For higher-order or coupled systems, this becomes very tedious.

The Laplace transform converts this to: $sY(s) + 3Y(s) = 5U(s)$, which is just algebra:

$$Y(s) = \frac{5}{s + 3}U(s)$$

We can now read off the transfer function $G(s) = \frac{5}{s+3}$ directly, and we can find $y(t)$ by looking up the inverse Laplace transform in a table. **No differential equations to solve.**

### 3.2 Definition

$$F(s) = \mathcal{L}\{f(t)\} = \int_0^{\infty} f(t) \, e^{-st} \, dt$$

where $s = \sigma + j\omega$ is a **complex frequency variable**.

**What this means intuitively:** The Laplace transform decomposes a time signal into a sum of complex exponentials $e^{st} = e^{(\sigma + j\omega)t}$. The real part $\sigma$ captures growth/decay, and the imaginary part $j\omega$ captures oscillation. So $F(s)$ tells us "how much" of each exponential mode is present in $f(t)$.

**Key properties:**
- $f(t) = 0$ for $t < 0$ — we only consider causal (one-sided) signals
- Differential equations become **polynomial** algebra in $s$
- The variable $s$ can be interpreted as a generalized frequency
- The inverse transform recovers $f(t)$ from $F(s)$

$$\mathcal{L}^{-1}\{F(s)\} = f(t) = \frac{1}{2\pi j}\int_{\sigma_1 - j\infty}^{\sigma_1 + j\infty} F(s)e^{st}\,ds$$

> [!note] Electrical Engineering Convention
> In electrical engineering, $j$ (not $i$) denotes the imaginary unit $\sqrt{-1}$, because $i$ is already used for current. MATLAB uses both: `i` and `j` are equivalent.

![[3_Laplace_TF.pdf#page=14]]

### 3.3 Laplace Calculation Rules

These rules are the "grammar" for converting between time-domain operations and s-domain algebra:

| $f(t)$ | $F(s)$ | Operation | Why it works |
|--------|--------|-----------|-------------|
| $Af(t)$ | $AF(s)$ | Scaling | Linearity of the integral |
| $f_1(t) + f_2(t)$ | $F_1(s) + F_2(s)$ | Addition | Linearity |
| $f_1(t) - f_2(t)$ | $F_1(s) - F_2(s)$ | Subtraction | Linearity |
| $\frac{d}{dt}f(t)$ | $sF(s) - f(0)$ | Differentiation | Integration by parts; $f(0)$ is the initial condition |
| $\frac{d^2}{dt^2}f(t)$ | $s^2 F(s) - sf(0) - f'(0)$ | 2nd derivative | Apply differentiation rule twice |
| $\int_0^t f(\tau)\,d\tau$ | $\frac{1}{s}F(s)$ | Integration | Division by $s$ = integration in time |
| $\lim_{t \to 0} f(t)$ | $\lim_{s \to \infty} sF(s)$ | Initial value theorem | |
| $\lim_{t \to \infty} f(t)$ | $\lim_{s \to 0} sF(s)$ | Final value theorem | Only valid if the limit exists (stable system) |

> [!important] The Two Most Important Rules
> 1. **Differentiation → multiplication by $s$**: This is why differential equations become polynomials! Every $\frac{d}{dt}$ in the time domain turns into multiplying by $s$. A second-order ODE with $\ddot{y}$ becomes a polynomial $s^2 Y(s)$.
> 2. **Integration → division by $s$**: This is why integrators in block diagrams are represented as $\frac{1}{s}$. Time-domain integration is equivalent to dividing by $s$ in the Laplace domain.
>
> **When we assume zero initial conditions** (as we usually do for transfer functions), $f(0) = 0$ and $f'(0) = 0$, so differentiation simplifies to just $sF(s)$.

![[3_Laplace_TF.pdf#page=15]]

### 3.4 Common Laplace Transform Pairs

These are the "vocabulary" — memorize the most common ones:

| $f(t)$ | $F(s)$ | Description | Shape |
|--------|--------|-------------|-------|
| $\delta(t)$ | $1$ | Unit impulse | Single spike at $t=0$ |
| $u(t)$ (step) | $\frac{1}{s}$ | Unit step | Jumps from 0 to 1 at $t=0$ |
| $e^{-at}$ | $\frac{1}{s+a}$ | Exponential decay | Decays to 0 with time constant $1/a$ |
| $t$ | $\frac{1}{s^2}$ | Ramp | Linearly increasing |
| $t^2$ | $\frac{2}{s^3}$ | Quadratic | Accelerating increase |
| $te^{-at}$ | $\frac{1}{(s+a)^2}$ | Damped ramp | Rises then falls back to zero |
| $\sin(bt)$ | $\frac{b}{s^2+b^2}$ | Sine wave | Oscillates forever |
| $\cos(bt)$ | $\frac{s}{s^2+b^2}$ | Cosine wave | Oscillates forever |
| $e^{-at}\sin(bt)$ | $\frac{b}{(s+a)^2+b^2}$ | Damped sine | Oscillates and decays |

> [!tip] Pattern Recognition
> - **Poles on the real axis** ($s = -a$) give **exponential** behaviour: $e^{-at}$
> - **Poles on the imaginary axis** ($s = \pm jb$) give **oscillating** behaviour: $\sin(bt)$, $\cos(bt)$
> - **Complex poles** ($s = -a \pm jb$) give **damped oscillation**: $e^{-at}\sin(bt)$
> - The **location of the poles** determines the character of the time response — this is a preview of stability analysis in later lectures.

![[3_Laplace_TF.pdf#page=16]]

---

## 4. Transfer Functions from Physical Systems

Now we combine modelling (Section 2) with Laplace (Section 3) to derive transfer functions for real systems.

### 4.1 Water Tank Example

**Physical system:** A round vessel (radius $r$) being filled by a tap with volumetric flow rate $Q(t)$ [m$^3$/s]. We want to find the transfer function from flow rate to water height $h(t)$.

**First principles:** Conservation of mass — the water flowing in must increase the volume:

$$\dot{V}(t) = Q(t), \quad V(t) = A \cdot h(t), \quad A = r^2\pi$$

Therefore: $A \cdot \dot{h}(t) = Q(t)$, or:

$$h(t) = \frac{1}{A}\int_0^t Q(\tau)\,d\tau = \frac{1}{r^2\pi}\int_0^t Q(\tau)\,d\tau$$

**Laplace transform:**

$$H(s) = \frac{1}{r^2\pi} \cdot \frac{1}{s} \cdot Q(s) \quad \Rightarrow \quad \frac{H(s)}{Q(s)} = \frac{1}{r^2\pi \cdot s}$$

**Block diagram:** $Q(s) \to \left[\frac{1}{r^2\pi}\right] \to \left[\frac{1}{s}\right] \to H(s)$

> [!note] Physical Interpretation
> The transfer function has a $\frac{1}{s}$ (integrator), which makes physical sense: the tank **accumulates** water over time. A constant flow rate $Q$ causes the height to increase linearly ($h = \frac{Q}{A}t$) — the system is an **integrator**. This also means the system is marginally stable (pole at $s = 0$).

![[3_Laplace_TF.pdf#page=18]]

### 4.2 RL Circuit Example

**Physical system:** A series RL circuit. Input: voltage $V(s)$. Output: current $I(s)$.

**From Kirchhoff's voltage law:** $V = V_R + V_L = RI + L\frac{dI}{dt}$

**In Laplace domain** (zero initial conditions): $V(s) = RI(s) + LsI(s) = (Ls + R)I(s)$

**Transfer function:**

$$\frac{I(s)}{V(s)} = \frac{1}{Ls + R}$$

**As a block diagram with feedback:** We can also derive this using the block diagram approach. Rearranging KVL: $L\dot{I} = V - RI$, so $\dot{I} = \frac{1}{L}(V - RI)$.

This gives the block diagram:

$$V(s) \to \Sigma(+,-) \to \left[\frac{1}{L}\right] \to \left[\frac{1}{s}\right] \to I(s), \quad \text{feedback: } I \to [R] \to (-)\Sigma$$

Applying the closed-loop formula: Forward = $\frac{1}{Ls}$, Loop gain = $\frac{R}{Ls}$

$$\frac{I(s)}{V(s)} = \frac{1/(Ls)}{1 + R/(Ls)} = \frac{1}{Ls + R}$$

Same result — the two approaches (direct algebra vs. block diagram reduction) always agree.

**Limiting cases — building intuition:**

- **If $L \to 0$** (pure resistor, no inductance):
  $\frac{I}{V} = \frac{1}{Ls + R} \to \frac{1}{R}$ — this is just **Ohm's law**: $I = V/R$. The inductor's energy storage is negligible.

- **Steady state** (step input of amplitude $A$, using Final Value Theorem):
  $I_{ss} = \lim_{s \to 0} s \cdot \frac{A}{s} \cdot \frac{1}{Ls + R} = \frac{A}{R}$ — at steady state, the inductor acts like a wire ($V_L = L\frac{dI}{dt} = 0$ since current is constant), so again $I = V/R$.

![[3_Laplace_TF.pdf#page=20]]

![[3_Laplace_TF.pdf#page=21]]

---

## 5. Control Questions — Worked Examples

These examples from the lecture show the complete workflow: start with a physical input, express it in Laplace domain, multiply by the transfer function, and inverse-transform back to the time domain.

### 5.1 Question 1: Constant Input Through a Transfer Function

**Setup:** A block with transfer function $G(s) = \frac{s}{s+10}$, constant input voltage $v(t) = 5$, output is speed $\dot{x}(t)$.

**Step a) — Laplace of the input:**
A constant $v(t) = 5$ that turns on at $t = 0$ is a step of magnitude 5. Since $v(t) = 0$ for $t < 0$:

$$V(s) = \frac{5}{s}$$

(Using the Laplace pair: step function $\leftrightarrow \frac{1}{s}$, scaled by 5.)

**Step b) — Output in s-domain:**
The output is simply input times transfer function:

$$\dot{X}(s) = V(s) \cdot G(s) = \frac{5}{s} \cdot \frac{s}{s+10}$$

The $s$ in the numerator and denominator **cancel**:

$$\dot{X}(s) = \frac{5}{s+10}$$

**Step c) — Inverse Laplace to get the time-domain output:**
From the Laplace table: $\frac{a}{s+a} \leftrightarrow ae^{-at}$, or more directly, $\frac{1}{s+a} \leftrightarrow e^{-at}$

$$\boxed{\dot{x}(t) = 5e^{-10t}}$$

**Physical interpretation:** The speed starts at 5 (at $t = 0$) and decays exponentially to zero with a time constant of $\tau = 1/10 = 0.1$ s. After about 0.5 s (5 time constants), the speed is essentially zero.

![[3_Laplace_TF.pdf#page=25]]

### 5.2 Question 2: Exponential Input

**Setup:** Same $G(s) = \frac{s}{s+10}$, but now the input is $v(t) = e^{-3t}$.

$$V(s) = \frac{1}{s+3}, \quad \dot{X}(s) = V(s) \cdot G(s) = \frac{1}{s+3} \cdot \frac{s}{s+10} = \frac{s}{(s+3)(s+10)}$$

This requires **partial fraction expansion** to inverse-transform:

$$\frac{s}{(s+3)(s+10)} = \frac{A}{s+3} + \frac{B}{s+10}$$

Solving: $A = \frac{-3}{-3+10} = \frac{-3}{7} \approx -0.43$ and $B = \frac{-10}{-10+3} = \frac{-10}{-7} \approx 1.43$

$$\dot{X}(s) = \frac{-0.43}{s+3} + \frac{1.43}{s+10}$$

$$\boxed{\dot{x}(t) = 1.43e^{-10t} - 0.43e^{-3t}}$$

**Physical interpretation:** The output is a combination of two exponentials. The fast mode ($e^{-10t}$, from the system's pole at $s = -10$) decays quickly, and the slow mode ($e^{-3t}$, from the input's "pole" at $s = -3$) dominates at later times. The response initially starts positive, dips slightly negative, then decays to zero.

> [!tip] MATLAB shortcut
> Instead of doing partial fractions by hand, MATLAB can handle the entire calculation symbolically:
> ```matlab
> syms s t;
> Vs = laplace(exp(-3*t));           % 1/(s+3)
> Gs = s/(s+10);
> Xds = Vs * Gs;                     % s/((s+3)(s+10))
> xdt = ilaplace(Xds);               % Symbolic inverse Laplace
> t_vec = 0:0.01:2;
> plot(t_vec, double(subs(xdt, t, t_vec)));
> ```

![[3_Laplace_TF.pdf#page=26]]

---

## 6. Electronic Components in Laplace Domain

The Laplace transform gives us a unified way to handle electronic components — resistors, capacitors, and inductors all become simple algebraic expressions.

### 6.1 Capacitor

**Time domain:** The voltage across a capacitor is the integral of the current flowing through it:

$$v_C(t) = \frac{1}{C}\int_0^t i_C(\tau)\,d\tau$$

**Laplace domain:** Integration becomes division by $s$:

$$V_C(s) = \frac{1}{sC} \cdot I_C(s)$$

**Impedance** (transfer function from current to voltage):

$$Z_C(s) = \frac{V_C(s)}{I_C(s)} = \frac{1}{sC}$$

**Physical intuition:** At **low frequency** ($\omega \to 0$, so $s \to 0$), $Z_C \to \infty$ — the capacitor blocks DC (acts as an open circuit). At **high frequency** ($\omega \to \infty$), $Z_C \to 0$ — the capacitor is a short circuit. This is why capacitors are used in **high-pass filters** (they pass high frequencies and block low frequencies).

![[3_Laplace_TF.pdf#page=27]]

### 6.2 Inductor

**Time domain:** The voltage across an inductor is proportional to the rate of change of current:

$$v_L(t) = L\frac{d}{dt}i(t)$$

**Laplace domain:** Differentiation becomes multiplication by $s$:

$$V_L(s) = sL \cdot I(s)$$

**Impedance:**

$$Z_L(s) = \frac{V_L(s)}{I(s)} = sL$$

**Physical intuition:** At **low frequency**, $Z_L \to 0$ — the inductor is a short circuit (it passes DC freely). At **high frequency**, $Z_L \to \infty$ — the inductor blocks rapid changes in current. This is why inductors are used in **low-pass filters**.

### 6.3 Summary: Component Impedances

| Component | Time Domain | Laplace Impedance $Z(s)$ | DC ($\omega = 0$) | High freq ($\omega \to \infty$) |
|-----------|-------------|--------------------------|------|-----------|
| Resistor | $v = Ri$ | $R$ | $R$ | $R$ |
| Capacitor | $v = \frac{1}{C}\int i\,dt$ | $\frac{1}{sC}$ | $\infty$ (open) | $0$ (short) |
| Inductor | $v = L\frac{di}{dt}$ | $sL$ | $0$ (short) | $\infty$ (open) |

> [!tip] Audio Relevance
> These impedances are the foundation of **analog filter design** — directly relevant to the 34655 Integrated Analog Electronics course:
> - **RC low-pass filter:** $H(s) = \frac{1/(sC)}{R + 1/(sC)} = \frac{1}{sRC + 1}$ — first-order rolloff
> - **RL high-pass filter:** $H(s) = \frac{sL}{R + sL} = \frac{s}{s + R/L}$ — first-order rolloff
> - **RLC bandpass/notch:** Combines both → second-order transfer functions
> - The $s = j\omega$ substitution connects directly to **Bode plot** analysis (Lesson 6)

![[3_Laplace_TF.pdf#page=29]]

---

## 7. Frequency, Phasors, and the Laplace Connection

This section connects three ideas: frequency response of linear systems, phasor notation from AC circuit analysis, and the Laplace transform. Understanding how these relate is fundamental to the rest of the course.

### 7.1 The Key Principle of Linear Systems

> [!important] Sinusoidal Steady-State Property
> In a **linear, time-invariant (LTI) system**, if the input is a sinusoidal signal at frequency $\omega$, then the steady-state output is **also** a sinusoid at the **same frequency** $\omega$, but with potentially different **amplitude** and **phase**.

This is a profound result. It means that to fully characterize a system's frequency behaviour, we only need to know how it scales the amplitude and shifts the phase at each frequency. This is exactly what the transfer function $G(j\omega)$ tells us.

**Example from the lecture:** If $f_1(t) = \cos(\omega t)$ is the input to an integrator $k\int_0^t$, the output $f_2(t)$ is also sinusoidal at the same frequency, but with different amplitude and a phase shift of $-90°$ (sine is cosine shifted by $-90°$).

![[3_Laplace_TF.pdf#page=30]]

### 7.2 Phasor Representation

A phasor is a compact way to represent a sinusoidal signal using a **complex number**. Instead of writing $f(t) = A\cos(\omega t + \theta)$ — which has three parameters — we capture everything in:

$$F = Ae^{j\theta} = A(\cos\theta + j\sin\theta) = A\angle\theta$$

- $A$ = amplitude (magnitude of the complex number)
- $\theta$ = phase (angle of the complex number)
- $\omega$ = frequency (implicit — we know what frequency we're analyzing)

**Why phasors are useful:** Multiplying two phasors is simple — magnitudes multiply, phases add. Division: magnitudes divide, phases subtract. This turns the problem of analyzing sinusoidal circuits from trigonometric identities into simple complex algebra.

**Back to time domain:** $f(t) = \text{Re}\{Fe^{j\omega t}\} = \text{Re}\{Ae^{j(\omega t + \theta)}\} = A\cos(\omega t + \theta)$

![[3_Laplace_TF.pdf#page=31]]

### 7.3 Phasor Example: RL Circuit

From the lecture: $i_s(t) = 2\cos(1000t)$, $R = 1.2\,\Omega$, $L = 0.6\,\text{mH}$

The phasor current: $\mathbf{I}_s = 2\angle 0°$

The impedance: $\mathbf{Z} = R + j\omega L = 1.2 + j(1000)(0.0006) = 1.2 + j0.6$

Converting to polar: $|\mathbf{Z}| = \sqrt{1.2^2 + 0.6^2} = 1.34$, $\angle\mathbf{Z} = \arctan(0.6/1.2) = 26.6°$

Output voltage (Ohm's law in phasor form):

$$\mathbf{V}_{out} = \mathbf{Z} \cdot \mathbf{I}_s = (1.34\angle 26.6°)(2\angle 0°) = 2.68\angle 26.6°$$

**Back to time domain:** $v_{out}(t) = 2.68\cos(1000t + 26.6°)$

> [!success] The Power of Phasors
> We computed the output voltage using only **algebra** (multiplying complex numbers) — no differential equations, no integration. This is the entire point of working in the frequency/phasor domain.

![[3_Laplace_TF.pdf#page=32]]

### 7.4 The Laplace-Phasor Connection

The phasor is a **special case** of the Laplace transform. Recall that $s = \sigma + j\omega$. When we set $\sigma = 0$:

$$s = j\omega$$

So **evaluating a transfer function at $s = j\omega$** gives the **frequency response** — the gain and phase shift that the system applies to a sinusoid at frequency $\omega$.

$$G(j\omega) = |G(j\omega)| \cdot e^{j\angle G(j\omega)} = M \cdot e^{j\varphi}$$

- $M = |G(j\omega)|$ = gain (how much the amplitude is scaled)
- $\varphi = \angle G(j\omega)$ = phase shift (how much the phase is shifted)

> [!important] This Is What Bode Plots Show
> A Bode plot (Lesson 6) simply plots $M$ and $\varphi$ as functions of $\omega$. The magnitude plot shows $20\log_{10}(M)$ in dB, and the phase plot shows $\varphi$ in degrees. The Laplace transfer function $G(s)$ contains all the information needed to construct the Bode plot — just substitute $s = j\omega$.

![[3_Laplace_TF.pdf#page=33]]

---

## 8. Phasor/Frequency Response Examples

### 8.1 Example I: First-Order System

**Given:** $G(s) = \frac{10}{s + 312}$, input $u(t) = \cos(\omega t)$ at $\omega = 628$ rad/s.

**Step 1:** Substitute $s = j\omega$:

$$G(j628) = \frac{10}{j628 + 312}$$

**Step 2:** Find the magnitude and phase of the denominator.

The denominator is a complex number: $312 + j628$

$$|312 + j628| = \sqrt{312^2 + 628^2} = \sqrt{97344 + 394384} = \sqrt{491728} \approx 701$$

$$\angle(312 + j628) = \arctan\frac{628}{312} = \arctan(2.013) = 63.6°$$

**Step 3:** Compute the transfer function magnitude and phase.

Since the numerator is real ($10 = 10\angle 0°$):

$$M = \frac{|10|}{|312 + j628|} = \frac{10}{701} = 0.0143$$

$$\varphi = 0° - 63.6° = -63.6°$$

$$G(j628) = 0.0143 \, e^{-j63.6°}$$

**Step 4:** Write the output.

$$y(t) = M \cdot \cos(\omega t + \varphi) = 0.0143 \cos(628t - 63.6°)$$

**Physical interpretation:** At $\omega = 628$ rad/s (~100 Hz), the system attenuates the input by a factor of 70 ($M = 0.0143$) and shifts it by $-63.6°$. This makes sense for a first-order low-pass system with a pole at $s = -312$ (cutoff at 312 rad/s ≈ 50 Hz) — at twice the cutoff frequency, there is significant attenuation.

**MATLAB verification:**
```matlab
s = tf('s'); G = 10/(s + 312);
z = evalfr(G, 628*i);
z_mag = abs(z);                    % 0.0143
z_phase = rad2deg(angle(z));       % -63.6°
```

![[3_Laplace_TF.pdf#page=35]]

### 8.2 Example II: Second-Order System (Mass-Spring-Damper)

**Given:** $G(s) = \frac{40}{s^2 + 4s + 40}$, input $u(t) = \cos(\omega t)$.

This represents a **mass-spring-damper** system with $\omega_0 = \sqrt{40} \approx 6.32$ rad/s and damping ratio $\zeta = \frac{4}{2\sqrt{40}} = 0.316$ (underdamped).

**Frequency response:** Substitute $s = j\omega$:

$$G(j\omega) = \frac{40}{(j\omega)^2 + 4j\omega + 40} = \frac{40}{(-\omega^2 + 40) + j(4\omega)}$$

The denominator has a **real part** $(-\omega^2 + 40)$ and an **imaginary part** $(4\omega)$.

**Magnitude:**

$$M = |G(j\omega)| = \frac{40}{\sqrt{(-\omega^2 + 40)^2 + (4\omega)^2}}$$

**Phase:**

$$\varphi = 0° - \arctan\frac{4\omega}{-\omega^2 + 40}$$

**Evaluating at three frequencies:**

| $\omega$ [rad/s] | Real part | Imag part | $M$ | $\varphi$ | Physical meaning |
|---|---|---|---|---|---|
| $0.1$ | $\approx 40$ | $0.4$ | $\approx 1.0$ | $-0.57°$ | Low freq: output ≈ input (near DC gain = 1) |
| $1000$ | $\approx -10^6$ | $4000$ | $\approx 4 \times 10^{-5}$ | $-180°$ | High freq: heavily attenuated, inverted |
| $\sqrt{40}$ | $0$ | $4\sqrt{40}$ | $\approx 1.58$ | $-90°$ | **Resonance**: gain > 1, 90° phase lag |

> [!important] Resonance at $\omega = \omega_0 = \sqrt{40}$
> At the **natural frequency**, the real part of the denominator vanishes: $-\omega_0^2 + 40 = -40 + 40 = 0$. Only the imaginary part $4j\omega_0$ remains in the denominator. This makes the magnitude **peak** (the system amplifies the input!) and the phase is exactly $-90°$.
>
> The peak magnitude is $M = \frac{40}{4\omega_0} = \frac{40}{4\sqrt{40}} = \frac{\sqrt{40}}{4} \approx 1.58$. For a system with lower damping ($\zeta < 0.316$), this peak would be even higher — a lightly damped spring-mass system resonates strongly at its natural frequency.
>
> This is why wine glasses shatter at a specific pitch, and why soldiers break step when crossing bridges.

![[3_Laplace_TF.pdf#page=41]]

---

## 9. Mass-Spring-Damper: From Physics to Simulink

This section ties everything together: starting from Newton's law, deriving the transfer function, and implementing it as a block diagram in Simulink.

### 9.1 Deriving the Transfer Function

From Newton's second law for a mass-spring-damper system:

$$M\ddot{y} = -ky - \beta\dot{y} + F$$

where $k$ is the spring constant, $\beta$ is the damping coefficient, $M$ is the mass, and $F$ is the applied force.

Rearranging: $M\ddot{y} + \beta\dot{y} + ky = F$

Laplace transform (zero initial conditions): $Ms^2Y + \beta sY + kY = F(s)$

$$\frac{Y(s)}{F(s)} = \frac{1}{Ms^2 + \beta s + k}$$

### 9.2 Standard Second-Order Form

With $M = 1$, $k = \omega_0^2$, and $\beta = 2\zeta\omega_0$ (where $\zeta$ is the damping ratio):

$$G(s) = \frac{\omega_0^2}{s^2 + 2\zeta\omega_0 s + \omega_0^2}$$

**For the lecture example** ($\omega_0^2 = 40$, $2\zeta\omega_0 = 4$):

$$G(s) = \frac{40}{s^2 + 4s + 40}$$

### 9.3 Block Diagram Implementation

To implement this in Simulink (or any simulation environment), we convert the transfer function back to a differential equation and build the integrator chain:

$$y(s)(s^2 + 4s + 40) = 40 \cdot u(s) \quad \Leftrightarrow \quad \ddot{y} = 40u - 4\dot{y} - 40y$$

**Simulink block diagram:**

```
u ──→ [40] ──→ Σ(+,−,−) ──→ [1/s] ──→ ẏ ──→ [1/s] ──→ y
                   ↑                    │               │
                   │       [4] ◄────────┘               │
                   │        │                           │
                   │        ▼                           │
                   └────────+───── [40] ◄───────────────┘
```

**Signal flow:**
1. Input $u$ scaled by 40
2. Summing junction: $40u - 4\dot{y} - 40y$, which equals $\ddot{y}$
3. First integrator: $\ddot{y} \to \dot{y}$
4. Second integrator: $\dot{y} \to y$
5. Two feedback paths: $\dot{y}$ through gain 4, and $y$ through gain 40

The step response shows ~35% overshoot and oscillatory settling — consistent with $\zeta = 0.316$ (underdamped).

![[3_Laplace_TF.pdf#page=47]]

---

## Key Takeaways

1. **PD controller** adds derivative action that acts as a "brake" — it reduces overshoot by opposing rapid changes. **PID** combines all three actions: P for immediate response, I for steady-state accuracy, D for transient improvement.

2. **Modelling from first principles:** Apply Newton/Kirchhoff/conservation laws → get an ODE → isolate the highest derivative → build the integrator chain → add feedback.

3. **The Laplace transform** converts differential equations into algebra. The two most important rules: differentiation $\to$ multiply by $s$, integration $\to$ divide by $s$.

4. **Transfer functions** $G(s) = Y(s)/U(s)$ are the ratio of output to input in the Laplace domain. They completely characterize an LTI system's behaviour.

5. **Frequency response** is obtained by evaluating $G(j\omega)$: the magnitude tells you the gain, and the angle tells you the phase shift at each frequency. This is the foundation for Bode plots (Lesson 6).

6. **Phasors** are a special case of the Laplace transform ($s = j\omega$). They let us solve sinusoidal steady-state problems using only complex algebra — no differential equations needed.

7. **Resonance** occurs when the input frequency matches the system's natural frequency. At resonance, the system amplifies the input (gain > 1 for underdamped systems) and the phase is $-90°$.

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
> | Magnitude | $M = \frac{|\text{num}|}{|\text{den}|}$ |
> | Phase | $\varphi = \angle\text{num} - \angle\text{den}$ |
> | Capacitor impedance | $Z_C = \frac{1}{sC}$ |
> | Inductor impedance | $Z_L = sL$ |
> | 2nd order standard form | $\frac{\omega_0^2}{s^2 + 2\zeta\omega_0 s + \omega_0^2}$ |
> | Final value theorem | $\lim_{t\to\infty} f(t) = \lim_{s\to 0} sF(s)$ |
> | PID controller | $u = K_p(e + \frac{1}{\tau_i}\int e\,dt + \tau_d\dot{e})$ |

---

> [!nav]
> [[Lesson 2 - Block Diagrams and Control Concepts|← Lesson 2]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> &nbsp;
