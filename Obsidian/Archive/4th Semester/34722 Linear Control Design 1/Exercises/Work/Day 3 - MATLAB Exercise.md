---
course: "34722"
course-name: "Linear Control Design 1"
type: exercise
tags: [LCD, exercise, MATLAB]
date: 2026-02-18
---
# Day 3 - MATLAB: Laplace, Transfer Functions & Frequency Response

> [!abstract] Overview
> MATLAB companion for Lecture 3. Covers symbolic Laplace transforms, transfer function creation and analysis, frequency response evaluation (phasors), partial fraction expansion, and block diagram verification.

> [!info] Files
> - Script: [Day3_Laplace_TF.m](file:///C:/Users/Mads2/DTU/4.%20Semester/Linear%20Control%20Design/Day3/Day3_Laplace_TF.m)

> [!example] Related Materials
> - Lecture notes: [[Lesson 3 - Laplace Transform and Transfer Functions]]
> - Block diagram exercises: [[Day 3 - Block Diagram Exercise]]
> - Slides: [[3_Laplace_TF.pdf|Lecture 3 -- Laplace & Transfer Functions]]
> - Previous MATLAB: [[Day 1 - MATLAB Exercise]]

---

## Section 1: Symbolic Laplace Transforms

Using the Symbolic Math Toolbox to compute Laplace transforms and verify the table from the lecture.

```matlab
syms t s

% Forward transforms — verify the Laplace table
laplace(exp(-3*t), t, s)      % e^{-3t} -> 1/(s+3)
laplace(t, t, s)              % Ramp -> 1/s^2
laplace(sin(5*t), t, s)       % sin(5t) -> 5/(s^2+25)
laplace(cos(5*t), t, s)       % cos(5t) -> s/(s^2+25)
laplace(t*exp(-2*t), t, s)    % t*e^{-2t} -> 1/(s+2)^2

% Inverse transforms — going back to time domain
ilaplace(1/s, s, t)           % 1/s -> 1 (step)
ilaplace(1/(s+3), s, t)       % 1/(s+3) -> e^{-3t}
ilaplace(5/(s^2+25), s, t)    % 5/(s^2+25) -> sin(5t)
ilaplace(1/(s^2+4*s+40), s, t) % Second-order -> damped sine
```

> [!tip] Verifying Lecture Slide 16
> Run each pair and confirm they match the Laplace table from the lecture. The damped sine result from `ilaplace(1/(s^2+4*s+40))` should give $e^{-2t}\sin(6t)/6$, matching the poles at $s = -2 \pm j6$.

---

## Section 2: Laplace Rules — Differentiation and Integration

Demonstrate that differentiation becomes multiplication by $s$, and integration becomes division by $s$.

```matlab
syms t s

% Differentiation rule: L{df/dt} = s*F(s) - f(0)
% Example: f(t) = e^{-2t}, so f(0) = 1
f_t = exp(-2*t);
F_s = laplace(f_t, t, s);         % 1/(s+2)
df_t = diff(f_t, t);              % -2*e^{-2t}
Ldf = laplace(df_t, t, s);        % -2/(s+2)

% Verify numerically: s*F(s) - f(0) should equal L{df/dt}
check = double(subs(s*F_s - 1 - Ldf, s, 5))   % Should be 0

% Integration rule: L{int(f)} = F(s)/s
int_f = int(f_t, 0, t);
L_int = laplace(int_f, t, s);
check_int = double(subs(L_int - F_s/s, s, 5))  % Should be 0
```

> [!note] Key Insight
> When we assume **zero initial conditions** ($f(0) = 0$), the differentiation rule simplifies to $\mathcal{L}\{\dot{f}\} = sF(s)$. This is the standard assumption when working with transfer functions.

---

## Section 3: Transfer Functions — Creation and Analysis

### 3.1 Creating Transfer Functions

Three ways to define the same transfer function $G(s) = \frac{10}{s + 312}$ from Lecture 3:

```matlab
% Method 1: Numerator/denominator coefficient vectors
G1 = tf([10], [1, 312]);

% Method 2: Using the s variable directly (most readable)
s = tf('s');
G2 = 10 / (s + 312);

% Method 3: Zero-pole-gain form
G3 = zpk([], [-312], 10);   % zeros, poles, gain
```

### 3.2 Inspecting Transfer Functions

```matlab
s = tf('s');
G = 10 / (s + 312);

pole(G)      % -312 (the system's natural mode)
zero(G)      % empty (no zeros)
dcgain(G)    % 0.0321 = G(0) = 10/312
```

---

## Section 4: Step and Impulse Response

Visualising how the systems from Lecture 3 behave in the time domain.

```matlab
s = tf('s');
G1 = 10 / (s + 312);
G2 = 40 / (s^2 + 4*s + 40);

figure;
subplot(2,2,1); step(G1);    title('G1: Step');    grid on;
subplot(2,2,2); step(G2);    title('G2: Step');    grid on;
subplot(2,2,3); impulse(G1); title('G1: Impulse'); grid on;
subplot(2,2,4); impulse(G2); title('G2: Impulse'); grid on;
```

![[ex3_step_impulse.png]]

> [!tip] What to Observe
> - **First-order** ($G_1$): Step response rises exponentially to $G(0) = 10/312$ with time constant $\tau = 1/312 \approx 3.2$ ms. No overshoot.
> - **Second-order** ($G_2$): Step response oscillates and overshoots (~35%) because $\zeta = 0.316 < 1$ (underdamped). The natural frequency is $\omega_0 = \sqrt{40} \approx 6.32$ rad/s, so the oscillation period is $T \approx 2\pi/6 \approx 1$ s.

---

## Section 5: Control Questions from the Lecture

Reproducing the worked examples from Lecture 3, Slide 25–26.

### 5.1 Question 1: Constant Input (Slide 25)

$G(s) = \frac{s}{s+10}$, input $v(t) = 5$ (step of magnitude 5).

```matlab
s = tf('s');
G = s / (s + 10);

t = 0:0.001:1;
u = 5 * ones(size(t));
[y, t_out] = lsim(G, u, t);

% Analytical solution overlay
y_exact = 5 * exp(-10 * t);

figure;
plot(t_out, y, 'b', t, y_exact, 'r--');
legend('lsim', '5 exp(-10t)');
xlabel('Time [s]'); ylabel('xdot(t)');
title('Q1: G(s) = s/(s+10), v(t) = 5');
grid on;
```

![[ex3_Q1_constant_input.png]]

> [!success] Expected Result
> $\dot{x}(t) = 5e^{-10t}$ — starts at 5, decays to 0 with time constant 0.1 s.

### 5.2 Question 2: Exponential Input (Slide 26)

Same $G(s)$, input $v(t) = e^{-3t}$.

```matlab
s = tf('s');
G = s / (s + 10);

t = 0:0.001:2;
u = exp(-3*t);
[y, t_out] = lsim(G, u, t);

% Analytical solution
y_exact = (10/7)*exp(-10*t) - (3/7)*exp(-3*t);

figure;
plot(t_out, y, 'b', t, y_exact, 'r--');
legend('lsim', 'Analytical');
xlabel('Time [s]'); ylabel('xdot(t)');
title('Q2: G(s) = s/(s+10), v(t) = exp(-3t)');
grid on;
```

![[ex3_Q2_exponential_input.png]]

### 5.3 Partial Fraction Expansion

MATLAB can do partial fractions numerically with `residue`:

```matlab
num = [1, 0];                         % s
den = conv([1, 3], [1, 10]);          % (s+3)(s+10)

[r, p, k] = residue(num, den)
% r = [-3/7; 10/7]   (residues)
% p = [-3; -10]       (poles)
% => xdot(t) = -3/7*e^{-3t} + 10/7*e^{-10t}
```

> [!tip] `residue` is Your Best Friend
> For any rational transfer function, `residue(num, den)` returns the partial fraction coefficients. Each residue $r_i$ at pole $p_i$ corresponds to a term $r_i \cdot e^{p_i t}$ in the time domain.

---

## Section 6: Frequency Response — Evaluating $G(j\omega)$

This is the **phasor/frequency response** calculation from Lecture 3, Slides 33–41.

### 6.1 First-Order System (Slide 35)

$G(s) = \frac{10}{s + 312}$ at $\omega = 628$ rad/s.

```matlab
s = tf('s');
G = 10 / (s + 312);

w = 628;
z = evalfr(G, 1j * w);       % Evaluate G(jw)

M = abs(z)                    % 0.0143
phi = rad2deg(angle(z))       % -63.6 degrees
% => y(t) = 0.0143 * cos(628t - 63.6 deg)
```

### 6.2 Second-Order System at Multiple Frequencies (Slide 41)

$G(s) = \frac{40}{s^2 + 4s + 40}$ — evaluate at three frequencies to see the resonance.

```matlab
s = tf('s');
G = 40 / (s^2 + 4*s + 40);

w_test = [0.1, sqrt(40), 1000];
for k = 1:length(w_test)
    z = evalfr(G, 1j * w_test(k));
    fprintf('w = %8.2f:  |G| = %.4f,  angle = %.1f deg\n', ...
        w_test(k), abs(z), rad2deg(angle(z)));
end
```

**Expected output:**

| Frequency | $\omega$ [rad/s] | $|G(j\omega)|$ | $\angle G$ |
|---|---|---|---|
| Low freq | 0.1 | $\approx 1.0$ | $-0.6°$ |
| Resonance | 6.32 | $\approx 1.58$ | $-90°$ |
| High freq | 1000 | $\approx 4 \times 10^{-5}$ | $-180°$ |

> [!important] Resonance Peak
> At $\omega = \sqrt{40}$ the gain is **greater than 1** — the system amplifies the input. This only happens for underdamped systems ($\zeta < 1/\sqrt{2} \approx 0.707$).

### 6.3 Frequency Sweep — Preview of Bode Plot

```matlab
s = tf('s');
G = 40 / (s^2 + 4*s + 40);

w = logspace(-1, 3, 1000);
[mag, phase] = bode(G, w);
mag = squeeze(mag); phase = squeeze(phase);

figure;
subplot(2,1,1);
semilogx(w, 20*log10(mag), 'b');
title('Magnitude [dB]'); grid on;
xline(sqrt(40), 'r--', 'w_0');

subplot(2,1,2);
semilogx(w, phase, 'b');
title('Phase [deg]'); grid on;
xline(sqrt(40), 'r--', 'w_0');
yline(-90, 'k--');
```

![[ex3_bode_second_order.png]]

> [!tip] Shortcut
> `bode(G)` with no arguments lets MATLAB auto-select the frequency range. This is the Bode plot you will study in Lesson 6.

---

## Section 7: Phasor Calculations

### 7.1 RL Circuit Phasor Example (Slide 32)

$i_s(t) = 2\cos(1000t)$, $R = 1.2\,\Omega$, $L = 0.6$ mH.

```matlab
w = 1000;  R = 1.2;  L = 0.6e-3;

Z = R + 1j * w * L;          % 1.2 + j0.6
V_out = Z * 2;                % Ohm's law: V = Z * I

abs(V_out)                    % 2.683
rad2deg(angle(V_out))         % 26.57 degrees
% => v_out(t) = 2.68 * cos(1000t + 26.6 deg)
```

### 7.2 Component Impedance vs Frequency

```matlab
C = 1e-6;  L = 1e-3;  R = 100;
w = logspace(1, 6, 1000);

figure;
loglog(w, R*ones(size(w)), 'k', ...
       w, 1./(w*C), 'b', ...
       w, w*L, 'r');
legend('R', '1/(wC)', 'wL');
title('Component Impedance vs Frequency');
xlabel('w [rad/s]'); ylabel('|Z| [Ohm]');
grid on;
xline(1/sqrt(L*C), 'g--', 'w_0 = 1/sqrt(LC)');
```

![[ex3_impedance_vs_freq.png]]

> [!note] Crossover Frequency
> The capacitor and inductor impedances cross at $\omega_0 = 1/\sqrt{LC}$. Below this frequency, the capacitor dominates (high impedance); above it, the inductor dominates. This is the **resonant frequency** of an LC circuit.

---

## Section 8: Block Diagram Verification

Use MATLAB to verify the hand-calculated transfer functions from [[Day 3 - Block Diagram Exercise]].

```matlab
s = tf('s');

% Exercise 1: G/(s+GH)
forward = 5/s;
T1_block   = feedback(forward, 2);
T1_formula = 5 / (s + 10);

% Exercise 3: R/(s(Js+B))
inner = feedback(1/(0.01*s), 0.1);
T3_block   = inner * 0.05/s;
T3_formula = 0.05 / (s*(0.01*s + 0.1));

% Exercise 4: D(Gs+K)/((1+DG)s+DK)
fwd4 = (3 + 2/s) * 4;
T4_block   = feedback(fwd4, 1);
T4_formula = 4*(3*s+2) / (13*s + 8);

% Exercise 5: AB/(Cs^2+Ds+1)
inner5 = feedback(40/s, 0.1);
outer5 = feedback(inner5/s, 1);
T5_block   = outer5 * 40;
T5_formula = 40 / (0.025*s^2 + 0.1*s + 1);

figure;
subplot(2,2,1); step(T1_block,'b',T1_formula,'r--'); title('Ex 1'); legend('blocks','formula'); grid on;
subplot(2,2,2); step(T3_block,'b',T3_formula,'r--',5); title('Ex 3'); legend('blocks','formula'); grid on;
subplot(2,2,3); step(T4_block,'b',T4_formula,'r--'); title('Ex 4'); legend('blocks','formula'); grid on;
subplot(2,2,4); step(T5_block,'b',T5_formula,'r--'); title('Ex 5'); legend('blocks','formula'); grid on;
```

![[ex3_block_verification.png]]

---

## Key MATLAB Functions — Lecture 3

| Function | Description | Lecture Context |
|----------|-------------|-----------------|
| `laplace(f, t, s)` | Symbolic Laplace transform | Verify Laplace table |
| `ilaplace(F, s, t)` | Symbolic inverse Laplace | Time-domain solution |
| `tf(num, den)` | Create transfer function | Build $G(s)$ from coefficients |
| `s = tf('s')` | Define $s$ variable | Build $G(s)$ directly |
| `evalfr(G, w*1j)` | Evaluate $G(j\omega)$ | Phasor/frequency response |
| `abs(z)` | Magnitude of complex number | $M = \|G(j\omega)\|$ |
| `angle(z)` | Phase in radians | $\varphi = \angle G(j\omega)$ |
| `rad2deg(x)` | Convert radians to degrees | Display phase |
| `residue(num, den)` | Partial fraction expansion | Inverse Laplace by hand |
| `bode(G)` | Bode plot (magnitude + phase) | Preview of Lesson 6 |
| `feedback(G, H)` | Closed-loop: $G/(1+GH)$ | Block diagram reduction |
| `pole(G)`, `zero(G)` | System poles and zeros | Stability insight |
| `dcgain(G)` | Evaluate $G(0)$ | Steady-state gain |

---

> [!nav]
> [[Day 1 - MATLAB Exercise|← Day 1 MATLAB]]
>
> [[34722 Linear Control Design 1|34722 Home]]
>
> [[Day 3 - Block Diagram Exercise|Day 3 Block Diagrams →]]
