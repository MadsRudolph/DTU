---
course: "34722"
course-name: "Linear Control Design 1"
type: cheatsheet
tags: [LCD, midterm, cheatsheet]
date: 2026-03-18
---
# Midterm Cheatsheet — Linear Control Design 1

> [!abstract] Quick Navigation
> Jump to the section matching your problem type:
> - [[#1 — Laplace Transforms]] — ODE to s-domain, inverse transforms, tables
> - [[#2 — Transfer Functions]] — Deriving TFs, poles/zeros, stability
> - [[#3 — Block Diagram Reduction]] — Closed-loop formula, series/parallel/feedback
> - [[#4 — First-Order Systems]] — Time constant, DC gain, step response
> - [[#5 — Second-Order Systems]] — Damping, natural frequency, overshoot
> - [[#6 — Controllers (P / PI / PID)]] — Tuning, steady-state error, Ziegler-Nichols
> - [[#7 — Bode Plots and Stability Margins]] — Gain/phase margin, crossover frequency
> - [[#8 — Low-Pass Filter Design]] — Noise filtering, phase margin trade-off
> - [[#9 — Frequency Response]] — Phasors, evaluating G(jw)
> - [[#10 — System Identification]] — tfest, iddata, compare
> - [[#11 — MATLAB Quick Reference]] — All commands in one place

---

## 1 — Laplace Transforms

### Transform Rules (zero initial conditions)

| Operation | Time Domain | s-Domain |
|-----------|-------------|----------|
| Scaling | $Af(t)$ | $AF(s)$ |
| Sum | $f_1 + f_2$ | $F_1 + F_2$ |
| **Derivative** | $\dot{f}(t)$ | $sF(s) - f(0)$ |
| **2nd derivative** | $\ddot{f}(t)$ | $s^2F(s) - sf(0) - \dot{f}(0)$ |
| **Integration** | $\int_0^t f(\tau)d\tau$ | $\frac{F(s)}{s}$ |
| Final value | $\lim_{t\to\infty} f(t)$ | $\lim_{s\to 0} sF(s)$ |
| Initial value | $f(0^+)$ | $\lim_{s\to\infty} sF(s)$ |

> [!tip] With zero ICs
> Derivative = multiply by $s$, Integration = divide by $s$

### Common Transform Pairs

| $f(t)$ | $F(s)$ |
|--------|--------|
| $\delta(t)$ (impulse) | $1$ |
| $u(t)$ (step) | $\frac{1}{s}$ |
| $e^{-at}$ | $\frac{1}{s+a}$ |
| $t$ | $\frac{1}{s^2}$ |
| $te^{-at}$ | $\frac{1}{(s+a)^2}$ |
| $\sin(\omega t)$ | $\frac{\omega}{s^2+\omega^2}$ |
| $\cos(\omega t)$ | $\frac{s}{s^2+\omega^2}$ |
| $e^{-at}\sin(\omega t)$ | $\frac{\omega}{(s+a)^2+\omega^2}$ |
| $e^{-at}\cos(\omega t)$ | $\frac{s+a}{(s+a)^2+\omega^2}$ |

### How to: ODE → Transfer Function

1. Take Laplace of every term (assume zero ICs)
2. Replace $\dot{y} \to sY$, $\ddot{y} \to s^2Y$, etc.
3. Collect $Y(s)$ on one side, $U(s)$ on the other
4. $G(s) = \frac{Y(s)}{U(s)}$

**Example:** $\ddot{y} + 3\dot{y} + 2y = 5u$

$$s^2Y + 3sY + 2Y = 5U \quad\Rightarrow\quad G(s) = \frac{5}{s^2 + 3s + 2}$$

### How to: Inverse Laplace (Partial Fractions)

1. Factor denominator: $\frac{5}{(s+1)(s+2)}$
2. Partial fractions: $\frac{A}{s+1} + \frac{B}{s+2}$
3. Solve for A, B (cover-up or system of equations)
4. Use table: $\frac{1}{s+a} \to e^{-at}$

**MATLAB:** `[r, p, k] = residue(num, den)`

---

## 2 — Transfer Functions

### Definition

$$G(s) = \frac{Y(s)}{U(s)} = \frac{b_m s^m + \cdots + b_0}{s^n + a_{n-1}s^{n-1} + \cdots + a_0}$$

- **Zeros:** roots of numerator → $G(s) = 0$
- **Poles:** roots of denominator → $G(s) = \infty$

### DC Gain (Steady-State Gain)

$$K_{ss} = G(0) = \lim_{s \to 0} G(s) = \frac{b_0}{a_0}$$

For a step input of magnitude $U_0$: $\quad Y_{ss} = K_{ss} \cdot U_0$

### Stability from Poles

| Pole Location | Behaviour | Stable? |
|---------------|-----------|---------|
| Real, left half-plane ($s = -a$) | $e^{-at}$ decays | **Yes** |
| Real, right half-plane ($s = +a$) | $e^{+at}$ grows | **No** |
| Complex, LHP ($s = -a \pm jb$) | Damped oscillation | **Yes** |
| Complex, RHP ($s = +a \pm jb$) | Growing oscillation | **No** |
| On imaginary axis ($s = \pm jb$) | Sustained oscillation | Marginal |

> [!important] Rule
> **ALL poles must be in the left half-plane (negative real part) for stability.**

### Electronic Component Impedances

| Component | $Z(s)$ |
|-----------|--------|
| Resistor | $R$ |
| Capacitor | $\frac{1}{sC}$ |
| Inductor | $sL$ |

**Voltage divider in s-domain:** $H(s) = \frac{Z_2(s)}{Z_1(s) + Z_2(s)}$

**RC low-pass:** $H(s) = \frac{1}{sRC + 1} = \frac{1}{\tau s + 1}$

---

## 3 — Block Diagram Reduction

### The Golden Formula (Negative Feedback)

$$\boxed{\frac{Y}{R} = \frac{\text{Forward path}}{1 + \text{Loop gain}}}$$

**Standard feedback loop:**
```
r → Σ(+,−) → [C] → [G] → y
     ↑                   │
     └──── [H] ←─────────┘
```

$$\frac{Y}{R} = \frac{C \cdot G}{1 + C \cdot G \cdot H}$$

> [!warning] Positive feedback
> If the feedback is **positive** (+), use $1 - \text{Loop gain}$ instead.

### Reduction Rules

| Configuration | Result |
|---------------|--------|
| **Series:** $[G_1] \to [G_2]$ | $G_1 \cdot G_2$ |
| **Parallel:** $[G_1] + [G_2]$ | $G_1 + G_2$ |
| **Feedback:** $G$ with feedback $H$ | $\frac{G}{1 + GH}$ |

### How to: Reduce Complex Diagrams

1. Identify the **innermost loop** first
2. Reduce it using the feedback formula
3. Work outward, reducing series/parallel connections
4. Repeat until you have a single block

### How to: Build a Block Diagram from ODE

1. Isolate the highest derivative: $\ddot{x} = \frac{1}{M}(F - kx - \beta\dot{x})$
2. That becomes the input to a chain of $\frac{1}{s}$ integrators
3. Each state variable ($\dot{x}$, $x$) feeds back through its coefficient

---

## 4 — First-Order Systems

### Standard Form

$$G(s) = K_{ss} \cdot \frac{\omega_b}{s + \omega_b} = \frac{K_{ss}}{\tau s + 1}$$

| Parameter | Symbol | Relation |
|-----------|--------|----------|
| DC gain | $K_{ss}$ | $G(0)$ |
| Break frequency | $\omega_b$ | Pole location |
| Time constant | $\tau$ | $\frac{1}{\omega_b}$ |

### Step Response

$$y(t) = K_{ss} \cdot U_0 \cdot (1 - e^{-t/\tau})$$

| Time | Value |
|------|-------|
| $t = \tau$ | **63.2%** of final |
| $t = 2\tau$ | 86.5% |
| $t = 3\tau$ | 95.0% |
| $t = 4\tau$ | 98.2% |
| $t = 5\tau$ | 99.3% (≈ settled) |

> [!tip] Quick estimate
> Settling time $\approx 4\tau$ to $5\tau$

### How to: Identify First-Order TF from Step Response

1. Measure final value → $K_{ss} = \frac{y_{final}}{u_{step}}$
2. Find time when output reaches 63.2% of final → that's $\tau$
3. $G(s) = \frac{K_{ss}}{\tau s + 1}$

---

## 5 — Second-Order Systems

### Standard Form

$$G(s) = K_{ss} \cdot \frac{\omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

| Parameter | Symbol | How to extract |
|-----------|--------|----------------|
| Natural frequency | $\omega_n$ | $\sqrt{\text{constant term}}$ |
| Damping ratio | $\zeta$ | $\frac{\text{middle coeff}}{2\omega_n}$ |
| DC gain | $K_{ss}$ | $\frac{\text{numerator coeff}}{\omega_n^2}$ |

### Poles

$$s_{1,2} = -\zeta\omega_n \pm j\omega_n\sqrt{1 - \zeta^2}$$

### Damping Classification

| $\zeta$ | Type | Response |
|---------|------|----------|
| $0 < \zeta < 1$ | **Underdamped** | Oscillates, overshoots |
| $\zeta = 1$ | **Critically damped** | Fastest without overshoot |
| $\zeta > 1$ | **Overdamped** | Slow, no overshoot |

### Key Formulas

$$\text{Overshoot: } M_P = e^{-\pi\zeta / \sqrt{1-\zeta^2}} \times 100\%$$

$$\text{Damped frequency: } \omega_d = \omega_n\sqrt{1-\zeta^2}$$

$$\text{Settling time (2\%): } t_s \approx \frac{4}{\zeta\omega_n}$$

$$\text{Rise time: } t_r \approx \frac{1.8}{\omega_n} \quad (\text{for } \zeta \approx 0.5\text{–}0.8)$$

### Quick Reference Table

| $\zeta$ | Overshoot | Character |
|---------|-----------|-----------|
| 0.3 | 37% | Very oscillatory |
| 0.5 | 16% | Moderately oscillatory |
| **0.7** | **5%** | **Good design target** |
| 1.0 | 0% | No overshoot, slower |

---

## 6 — Controllers (P / PI / PID)

### Controller Equations

| Controller | Time Domain | Transfer Function $C(s)$ |
|------------|-------------|--------------------------|
| **P** | $u = K_p e$ | $K_p$ |
| **PI** | $u = K_p(e + \frac{1}{\tau_i}\int e\,dt)$ | $K_p(1 + \frac{1}{\tau_i s})$ |
| **PD** | $u = K_p(e + \tau_d \dot{e})$ | $K_p(1 + \tau_d s)$ |
| **PID** | $u = K_p(e + \frac{1}{\tau_i}\int e\,dt + \tau_d \dot{e})$ | $K_p(1 + \frac{1}{\tau_i s} + \tau_d s)$ |

### What Each Term Does

| Term | Effect | Downside |
|------|--------|----------|
| **P** | Immediate response, reduces error | Steady-state error remains |
| **I** | Eliminates steady-state error | Can cause overshoot/windup |
| **D** | Reduces overshoot, speeds settling | Amplifies noise |

### Steady-State Error with P-Controller

For a step input $r$:

$$e_{ss} = \frac{r}{1 + K_p \cdot G(0)}$$

> [!important]
> P-controller alone **always** has steady-state error. Only I-action eliminates it.

### Ziegler-Nichols — Open-Loop Method

From step response: measure delay $L$ and slope $R = \frac{\Delta Y / \Delta U}{\tau}$

| Controller | $K_p$ | $T_i$ | $T_d$ |
|------------|--------|--------|--------|
| P | $\frac{1}{RL}$ | — | — |
| PI | $\frac{0.9}{RL}$ | $\frac{L}{0.3}$ | — |
| PID | $\frac{1.2}{RL}$ | $2L$ | $0.5L$ |

### Ziegler-Nichols — Closed-Loop Method

Increase $K_p$ until sustained oscillation → ultimate gain $K_u$, period $P_u$

| Controller | $K_p$ | $T_i$ | $T_d$ |
|------------|--------|--------|--------|
| P | $0.5 K_u$ | — | — |
| PI | $0.45 K_u$ | $\frac{P_u}{1.2}$ | — |
| PID | $0.6 K_u$ | $0.5 P_u$ | $0.125 P_u$ |

---

## 7 — Bode Plots and Stability Margins

### Reading a Bode Plot

- **Magnitude plot:** $20\log_{10}|G(j\omega)|$ in dB vs. $\omega$
- **Phase plot:** $\angle G(j\omega)$ in degrees vs. $\omega$
- Both use **log scale** for frequency

### Key Frequencies

| Name | Definition | What happens there |
|------|------------|--------------------|
| **Gain crossover** $\omega_{gc}$ | $|G(j\omega)| = 1$ (0 dB) | Phase margin is read here |
| **Phase crossover** $\omega_{pc}$ | $\angle G(j\omega) = -180°$ | Gain margin is read here |
| **Break frequency** $\omega_b$ | Pole/zero location | Slope changes by ±20 dB/dec |

### Stability Margins

$$\text{Gain margin: } G_m = \frac{1}{|G(j\omega_{pc})|} \quad\text{(in dB: } 20\log_{10} G_m\text{)}$$

$$\text{Phase margin: } \phi_m = 180° + \angle G(j\omega_{gc})$$

| Condition | Meaning |
|-----------|---------|
| $\phi_m > 0$ | **Stable** |
| $\phi_m < 0$ | **Unstable** |
| $\phi_m \geq 45°$ | Good robustness |
| $\phi_m \geq 30°$ | Acceptable |

### Bode Plot Slope Rules

| Element | Magnitude slope change | Phase change |
|---------|----------------------|--------------|
| Pole at $\omega_b$ | $-20$ dB/dec | $0° \to -90°$ |
| Zero at $\omega_b$ | $+20$ dB/dec | $0° \to +90°$ |
| Integrator $\frac{1}{s}$ | $-20$ dB/dec always | Fixed $-90°$ |
| Double pole | $-40$ dB/dec | $0° \to -180°$ |

### How to: Sketch a Bode Plot

1. Write $G(s)$ in standard form (factor out DC gain)
2. Mark each pole/zero break frequency on the $\omega$-axis
3. Start with the DC gain at low frequency
4. At each break: change slope by $\pm 20$ dB/dec
5. Phase: transitions happen over roughly one decade centered on each break

---

## 8 — Low-Pass Filter Design

### First-Order Low-Pass Filter

$$G_{filt}(s) = \frac{\omega_c}{s + \omega_c}$$

- DC gain = 1 (passes low frequencies unchanged)
- Rolls off at $-20$ dB/dec above $\omega_c$
- Adds phase lag: up to $-90°$ at high frequencies

### Design for Feedback Loop

**Open-loop with filter:** $G_{ol} = K_p \cdot G \cdot G_{filt}$

**Closed-loop:** $G_{cl} = \frac{K_p G}{1 + K_p G \cdot G_{filt}}$

### Design Constraint

Phase margin reduction $\leq 30°$:

$$\phi_{m,filtered} \geq \phi_{m,unfiltered} - 30°$$

**Strategy:** Start with high $\omega_c$ (small phase lag), decrease until PM loss reaches 30°.

---

## 9 — Frequency Response

### Evaluating $G(j\omega)$

Substitute $s = j\omega$ into $G(s)$, then compute magnitude and phase.

**Example:** $G(s) = \frac{5}{s + 2}$ at $\omega = 3$

$$G(j3) = \frac{5}{j3 + 2} = \frac{5}{2 + j3}$$

$$|G| = \frac{5}{\sqrt{2^2 + 3^2}} = \frac{5}{\sqrt{13}} = 1.39$$

$$\angle G = -\arctan\frac{3}{2} = -56.3°$$

### Sinusoidal Steady-State

If input is $u(t) = A\sin(\omega t)$, the steady-state output is:

$$y_{ss}(t) = A \cdot |G(j\omega)| \cdot \sin(\omega t + \angle G(j\omega))$$

> [!tip] The output has the **same frequency** as the input, just scaled and shifted.

---

## 10 — System Identification

### Process

```matlab
% 1. Load data
data = readtable('logfile.txt');

% 2. Extract signals
t = table2array(data(:,1));     % time
u = table2array(data(:,col_u)); % input (voltage)
y = table2array(data(:,col_y)); % output (velocity)
Ts = t(2) - t(1);              % sampling time

% 3. Trim to step region
idx = find(u >= threshold, 1, 'first');

% 4. Remove offsets (signals start from 0)
u = u - u(1);
y = y - y(1);

% 5. Create iddata and estimate
idd = iddata(y, u, Ts);
G = tfest(idd, num_poles, num_zeros);

% 6. Validate
compare(idd, G);
```

### Choosing Model Order

| Model | When to use |
|-------|-------------|
| 1 pole, 0 zeros | Simple first-order (exponential rise) |
| 2 poles, 0 zeros | Second-order (overshoot or two time constants) |
| 2 poles, 1 zero | If there's an initial fast transient |

---

## 11 — MATLAB Quick Reference

### Transfer Functions

```matlab
s = tf('s');
G = 5 / (s^2 + 3*s + 2);        % from expression
G = tf([5], [1 3 2]);            % from coefficients
```

### Properties

```matlab
pole(G)                           % pole locations
zero(G)                           % zero locations
dcgain(G)                         % steady-state gain G(0)
bandwidth(G)                      % bandwidth (rad/s)
```

### Responses

```matlab
step(G)                           % step response plot
impulse(G)                        % impulse response
[y, t] = step(G, tfinal);        % extract data
info = stepinfo(G);               % rise time, overshoot, etc.
lsim(G, u, t)                    % response to custom input
```

### Frequency Domain

```matlab
bode(G)                           % Bode plot
margin(G)                         % Bode + margin annotations
[Gm, Pm, Wcg, Wcp] = margin(G);  % extract margins
nyquist(G)                        % Nyquist plot
evalfr(G, 1j*w)                   % evaluate G(jw)
```

### Block Diagram Operations

```matlab
G_series  = G1 * G2;              % series
G_par     = G1 + G2;              % parallel
G_cl      = feedback(G, H);      % G / (1 + G*H)
G_cl      = feedback(G*C, H);    % C*G / (1 + C*G*H)
G_simple  = minreal(G);          % pole-zero cancellation
```

### Symbolic

```matlab
syms s t
F = laplace(exp(-2*t), t, s);    % → 1/(s+2)
f = ilaplace(1/(s+2), s, t);    % → exp(-2t)
[r, p, k] = residue(num, den);  % partial fractions
```

### System Identification

```matlab
idd = iddata(y, u, Ts);
G = tfest(idd, npoles, nzeros);
compare(idd, G);
```

### Filters and Closed-Loop

```matlab
G_filt = tf(wc, [1 wc]);         % 1st-order LP filter
G_ol = Kp * G;                   % open loop with P-controller
G_cl = feedback(Kp*G, G_filt);   % closed loop: Kp*G / (1+Kp*G*Gfilt)
```

---

> [!nav]
> [[34722 Linear Control Design 1|34722 Home]]
