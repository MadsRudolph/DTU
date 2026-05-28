# Midterm Cheatsheet — 34722 Linear Control Design 1

> Copy-paste MATLAB sections as needed. All blocks are self-contained.

---

## Setup (run first)

```matlab
clear all; clc; close all;
s = tf('s');
```

---

## 1. Define Transfer Function

### From expression
```matlab
G = 5 / (s^2 + 3*s + 2);
```

### From coefficients
```matlab
num = [5];          % numerator coefficients (highest power first)
den = [1 3 2];      % denominator: s^2 + 3s + 2
G = tf(num, den);
```

### From ODE: a2*y'' + a1*y' + a0*y = b1*u' + b0*u
```matlab
a2 = 1; a1 = 3; a0 = 2;
b1 = 0; b0 = 5;
G = tf([b1 b0], [a2 a1 a0]);
```

### Analyze
```matlab
pole(G)          % pole locations
zero(G)          % zero locations
dcgain(G)        % DC gain Kss = G(0)
bandwidth(G)     % bandwidth [rad/s]
```

---

## 2. First-Order System

### Standard form: G(s) = Kss * wb / (s + wb) = Kss / (tau*s + 1)

```matlab
% Given G(s), extract parameters:
[num_c, den_c] = tfdata(G, 'v');
wb = den_c(2) / den_c(1);        % break frequency = pole location
tau = 1 / wb;                     % time constant
Kss = dcgain(G);                  % DC gain

fprintf('Kss  = %.4f\n', Kss);
fprintf('wb   = %.4f rad/s\n', wb);
fprintf('tau  = %.4f s\n', tau);
fprintf('63%% at t = %.4f s\n', tau);
fprintf('Settled (~5tau) at t = %.4f s\n', 5*tau);
```

### Build from specs
```matlab
Kss = 2; wb = 10;
G = Kss * wb / (s + wb);
% or equivalently:
tau = 1/wb;
G = Kss / (tau*s + 1);
```

### Identify from step response
```matlab
% 1. Measure final value → Kss = y_final / u_step
% 2. Find time when output = 63.2% of final → that's tau
% 3. wb = 1/tau
Kss = 0.2; tau = 20;
G = Kss / (tau*s + 1);
```

---

## 3. Second-Order System

### Standard form: G(s) = Kss * wn^2 / (s^2 + 2*zeta*wn*s + wn^2)

```matlab
% Given G(s), extract parameters:
[num_c, den_c] = tfdata(G, 'v');
wn   = sqrt(den_c(3) / den_c(1));          % natural frequency
zeta = den_c(2) / (2 * wn * den_c(1));     % damping ratio
Kss  = num_c(end) / (den_c(1) * wn^2);     % DC gain

fprintf('wn   = %.4f rad/s\n', wn);
fprintf('zeta = %.4f\n', zeta);
fprintf('Kss  = %.4f\n', Kss);

% Derived quantities
wd = wn * sqrt(1 - zeta^2);                      % damped frequency
Mp = exp(-pi*zeta / sqrt(1 - zeta^2)) * 100;     % overshoot %
ts = 4 / (zeta * wn);                             % settling time (2%)
tr = 1.8 / wn;                                    % rise time (approx)

fprintf('wd   = %.4f rad/s (damped freq)\n', wd);
fprintf('Mp   = %.2f %% overshoot\n', Mp);
fprintf('ts   = %.4f s (settling)\n', ts);
fprintf('tr   = %.4f s (rise time)\n', tr);
```

### Check if poles are complex
```matlab
[num_c, den_c] = tfdata(G, 'v');
discriminant = den_c(2)^2 - 4*den_c(1)*den_c(3);
if discriminant < 0
    fprintf('Complex conjugate poles (underdamped)\n');
else
    fprintf('Real poles\n');
end
```

### Build from specs
```matlab
wn = 10; zeta = 0.7; Kss = 1;
G = Kss * wn^2 / (s^2 + 2*zeta*wn*s + wn^2);
```

### Damping reference
```
zeta = 0.3 → 37% overshoot (very oscillatory)
zeta = 0.5 → 16% overshoot
zeta = 0.7 → 5%  overshoot (good design target)
zeta = 1.0 → 0%  overshoot (critically damped)
```

---

## 4. Poles, Zeros & Stability

```matlab
p = pole(G);
z = zero(G);

fprintf('Poles:\n');
for i = 1:length(p)
    fprintf('  s = %.4f + j%.4f  (real part %.4f → %s)\n', ...
        real(p(i)), imag(p(i)), real(p(i)), ...
        ternary(real(p(i)) < 0, 'STABLE', 'UNSTABLE'));
end

fprintf('\nZeros:\n');
for i = 1:length(z)
    fprintf('  s = %.4f + j%.4f\n', real(z(i)), imag(z(i)));
end

% Stability check
if all(real(p) < 0)
    fprintf('\nSystem is STABLE (all poles in LHP)\n');
else
    fprintf('\nSystem is UNSTABLE (pole in RHP)\n');
end
```

### Quick stability helper (if ternary not available)
```matlab
p = pole(G);
fprintf('Poles: '); disp(p');
if all(real(p) < 0)
    fprintf('STABLE\n');
else
    fprintf('UNSTABLE\n');
end
```

### Dominant pole
```matlab
p = pole(G);
[~, idx] = max(real(p));  % closest to imaginary axis
fprintf('Dominant pole: s = %.4f + j%.4f\n', real(p(idx)), imag(p(idx)));
fprintf('Dominant time constant: tau = %.4f s\n', -1/real(p(idx)));
```

---

## 5. Step & Impulse Response

```matlab
figure;
step(G); grid on; title('Step Response');
info = stepinfo(G);
fprintf('Rise time:     %.4f s\n', info.RiseTime);
fprintf('Settling time: %.4f s\n', info.SettlingTime);
fprintf('Overshoot:     %.2f %%\n', info.Overshoot);
fprintf('DC gain:       %.4f\n', dcgain(G));
```

### With specific step size
```matlab
U0 = 3;
[y, t] = step(U0 * G);
figure; plot(t, y); grid on;
xlabel('Time [s]'); ylabel('Output');
title(sprintf('Step response (U0 = %g)', U0));
```

### Impulse response
```matlab
figure; impulse(G); grid on;
```

### Custom input (lsim)
```matlab
t = 0:0.01:10;
u = sin(2*t);         % any input signal
figure; lsim(G, u, t); grid on;
```

---

## 6. Final Value Theorem

```matlab
% For step input of magnitude U0:
U0 = 5;
y_final = U0 * dcgain(G);
fprintf('Steady-state output (FVT): %.4f\n', y_final);
```

```matlab
% Manual FVT: lim_{s→0} s * U(s) * G(s)
% Step of magnitude U0: U(s) = U0/s
% y_ss = lim_{s→0} s * (U0/s) * G(s) = U0 * G(0) = U0 * dcgain(G)
```

---

## 7. Frequency Response — Evaluate G(jw)

```matlab
w = 10;  % frequency [rad/s]
Gjw = evalfr(G, 1j*w);
mag = abs(Gjw);
phase_deg = rad2deg(angle(Gjw));
mag_dB = 20*log10(mag);

fprintf('At w = %.2f rad/s:\n', w);
fprintf('  |G(jw)|  = %.4f  (%.2f dB)\n', mag, mag_dB);
fprintf('  angle    = %.2f deg\n', phase_deg);
```

### Sinusoidal steady-state output
```matlab
% Input: u(t) = A_in * sin(w * t)
% Output: y(t) = A_in * |G(jw)| * sin(w * t + angle(G(jw)))

A_in = 2; w = 5;
Gjw = evalfr(G, 1j*w);
A_out = A_in * abs(Gjw);
phi = rad2deg(angle(Gjw));

fprintf('Input:  %.2f * sin(%.2f * t)\n', A_in, w);
fprintf('Output: %.4f * sin(%.2f * t + (%.2f deg))\n', A_out, w, phi);
```

### Evaluate at multiple frequencies
```matlab
w_vec = [0.1, 1, 10, 100];
fprintf('%-10s %-12s %-10s %-10s\n', 'w [rad/s]', '|G(jw)|', 'dB', 'Phase [deg]');
for i = 1:length(w_vec)
    Gjw = evalfr(G, 1j*w_vec(i));
    fprintf('%-10.2f %-12.4f %-10.2f %-10.2f\n', ...
        w_vec(i), abs(Gjw), 20*log10(abs(Gjw)), rad2deg(angle(Gjw)));
end
```

---

## 8. Bode Plot & Stability Margins

```matlab
figure; bode(G); grid on;
```

```matlab
figure; margin(G);  % Bode plot with margin annotations
```

```matlab
[Gm, Pm, Wcg, Wcp] = margin(G);
fprintf('Gain margin:     %.2f  (%.2f dB) at w = %.2f rad/s\n', Gm, 20*log10(Gm), Wcg);
fprintf('Phase margin:    %.2f deg at w = %.2f rad/s\n', Pm, Wcp);

if Pm > 45
    fprintf('→ Good robustness (PM > 45 deg)\n');
elseif Pm > 30
    fprintf('→ Acceptable (PM > 30 deg)\n');
elseif Pm > 0
    fprintf('→ Stable but low margin\n');
else
    fprintf('→ UNSTABLE (negative phase margin)\n');
end
```

### Compare Bode of two systems
```matlab
figure;
bode(G1, 'b', G2, 'r--'); grid on;
legend('G1', 'G2');
```

---

## 9. Block Diagram Reduction

### Closed-loop (negative feedback)
```matlab
% G_cl = Forward / (1 + Loop)
% G_cl = C*G / (1 + C*G*H)

C = 5;       % controller (e.g. Kp)
H = 1;       % sensor TF (unity feedback)
G_ol = C * G;
G_cl = feedback(G_ol, H);
G_cl = minreal(G_cl);    % cancel common poles/zeros
```

### Series & parallel
```matlab
G_series = G1 * G2;         % series connection
G_parallel = G1 + G2;       % parallel connection
```

### Positive feedback
```matlab
G_cl = feedback(G_ol, H, +1);  % positive feedback: 1 - Loop
```

### Nested loops (reduce inside-out)
```matlab
% Inner loop first
G_inner = feedback(G2, H2);
% Then outer loop
G_total = feedback(C * G_inner, H1);
```

---

## 10. P-Controller Design

```matlab
Kp = 15;
G_ol = Kp * G;                  % open-loop with P
G_cl = feedback(G_ol, 1);       % closed-loop (unity feedback)

% Steady-state error for unit step
r = 1;
ess = r / (1 + Kp * dcgain(G));
fprintf('Steady-state error: %.4f\n', ess);
fprintf('DC gain of CL:      %.4f\n', dcgain(G_cl));

% Margins
[Gm, Pm, Wcg, Wcp] = margin(G_ol);
fprintf('Phase margin: %.2f deg\n', Pm);

figure;
subplot(2,1,1); margin(G_ol); title('Open-Loop Bode');
subplot(2,1,2); step(G_cl); grid on; title('Closed-Loop Step');
```

---

## 11. PI Controller

```matlab
Kp = 5; tau_i = 0.5;
C_PI = Kp * (1 + 1/(tau_i * s));
G_ol = C_PI * G;
G_cl = feedback(G_ol, 1);
G_cl = minreal(G_cl);

fprintf('PI: Kp = %.2f, tau_i = %.2f\n', Kp, tau_i);
fprintf('DC gain CL: %.4f\n', dcgain(G_cl));

figure;
subplot(2,1,1); margin(G_ol);
subplot(2,1,2); step(G_cl); grid on;
```

---

## 12. PID Controller

```matlab
Kp = 5; tau_i = 0.5; tau_d = 0.1;
C_PID = Kp * (1 + 1/(tau_i*s) + tau_d*s);
G_ol = C_PID * G;
G_cl = feedback(G_ol, 1);
G_cl = minreal(G_cl);

figure;
step(G_cl); grid on;
title(sprintf('PID: Kp=%.1f, ti=%.2f, td=%.2f', Kp, tau_i, tau_d));
```

---

## 13. Ziegler-Nichols — Closed-Loop Method

```matlab
Ku = 20;    % ultimate gain (sustained oscillation)
Pu = 0.5;   % oscillation period [s]

% P controller
Kp_P = 0.5 * Ku;

% PI controller
Kp_PI = 0.45 * Ku;
Ti_PI = Pu / 1.2;

% PID controller
Kp_PID = 0.6 * Ku;
Ti_PID = 0.5 * Pu;
Td_PID = 0.125 * Pu;

fprintf('=== Ziegler-Nichols (Closed-Loop) ===\n');
fprintf('P:   Kp = %.4f\n', Kp_P);
fprintf('PI:  Kp = %.4f, Ti = %.4f\n', Kp_PI, Ti_PI);
fprintf('PID: Kp = %.4f, Ti = %.4f, Td = %.4f\n', Kp_PID, Ti_PID, Td_PID);
```

---

## 14. Ziegler-Nichols — Open-Loop Method

```matlab
L = 0.1;       % dead time [s]
tau = 1.0;     % time constant [s]
delta_y = 2;   % output change
delta_u = 1;   % input change
A = delta_y / delta_u;  % process gain
R = A / tau;             % slope

% P controller
Kp_P = 1 / (R * L);

% PI controller
Kp_PI = 0.9 / (R * L);
Ti_PI = L / 0.3;

% PID controller
Kp_PID = 1.2 / (R * L);
Ti_PID = 2 * L;
Td_PID = 0.5 * L;

fprintf('=== Ziegler-Nichols (Open-Loop) ===\n');
fprintf('R = %.4f, A = %.4f\n', R, A);
fprintf('P:   Kp = %.4f\n', Kp_P);
fprintf('PI:  Kp = %.4f, Ti = %.4f\n', Kp_PI, Ti_PI);
fprintf('PID: Kp = %.4f, Ti = %.4f, Td = %.4f\n', Kp_PID, Ti_PID, Td_PID);
```

---

## 15. Low-Pass Filter Design

```matlab
wc = 50;                              % cutoff frequency [rad/s]
G_filt = wc / (s + wc);              % 1st-order low-pass

% Open-loop with filter
Kp = 15;
G_ol_filt = Kp * G * G_filt;

% Closed-loop (filter in feedback path)
G_cl_filt = Kp*G / (1 + Kp*G*G_filt);
G_cl_filt = minreal(G_cl_filt);

[~, Pm_filt] = margin(G_ol_filt);
fprintf('Phase margin with filter: %.2f deg\n', Pm_filt);
```

### Find max filter cutoff with PM reduction ≤ 30 deg
```matlab
Kp = 15;
[~, Pm_no_filt] = margin(Kp * G);
PM_target = Pm_no_filt - 30;

wc_best = NaN;
wc_candidates = logspace(0, 4, 500);
for i = length(wc_candidates):-1:1
    wc_try = wc_candidates(i);
    G_filt_try = tf(wc_try, [1 wc_try]);
    [~, Pm_try] = margin(Kp * G * G_filt_try);
    if Pm_try >= PM_target
        wc_best = wc_try;
    else
        break;
    end
end
fprintf('Best wc = %.2f rad/s (PM >= %.2f deg)\n', wc_best, PM_target);
```

---

## 16. Laplace — Symbolic

### Forward transform
```matlab
syms t_sym s_sym
f = exp(-3*t_sym) * sin(5*t_sym);
F = laplace(f, t_sym, s_sym);
fprintf('F(s) = '); disp(F);
```

### Inverse transform
```matlab
syms t_sym s_sym
F = 5 / (s_sym^2 + 3*s_sym + 2);
f = ilaplace(F, s_sym, t_sym);
fprintf('f(t) = '); disp(f);
```

### Partial fractions
```matlab
num = [5];
den = [1 3 2];
[r, p, k] = residue(num, den);
fprintf('Partial fractions:\n');
for i = 1:length(r)
    fprintf('  %.4f / (s - (%.4f))\n', r(i), p(i));
end
% r = residues, p = poles, k = direct term
% f(t) = sum of r(i) * exp(p(i)*t)
```

---

## 17. System Identification (tfest)

```matlab
% Load data
opts = detectImportOptions('logfile.txt', 'FileType', 'text');
opts.CommentStyle = '%';
data = readtable('logfile.txt', opts);
data = fillmissing(data, 'nearest');

t = table2array(data(:,1));
u = table2array(data(:,8));    % input column
y = table2array(data(:,10));   % output column
Ts = t(2) - t(1);

% Trim to step region
V_mid = 3.5;
idx_step = find(u >= V_mid, 1, 'first');
N_pre = min(50, idx_step - 1);
t = t(idx_step-N_pre:end);
u = u(idx_step-N_pre:end);
y = y(idx_step-N_pre:end);

% Remove offsets
u = u - mean(u(1:N_pre));
y = y - mean(y(1:N_pre));

% Identify transfer function
idd = iddata(y, u, Ts);
G_est = tfest(idd, 2, 0);    % 2 poles, 0 zeros
compare(idd, G_est);
```

---

## 18. Electronic Components in s-Domain

### RC Low-Pass Filter
```matlab
R = 1000;   % Ohms
C_val = 1e-6; % Farads
tau = R * C_val;
H = 1 / (tau*s + 1);
fprintf('RC LP: tau = %.6f s, fc = %.2f Hz\n', tau, 1/(2*pi*tau));
```

### RL Circuit (V → I)
```matlab
R = 1.2; L = 0.6e-3;
G_RL = 1 / (L*s + R);
```

### Impedances
```matlab
% Z_R = R
% Z_C = 1/(s*C)
% Z_L = s*L
% Voltage divider: H(s) = Z2 / (Z1 + Z2)
```

---

## 19. DC Motor Model

```matlab
Ra = 1; La = 0.01; Km = 0.01; Kemf = Km; Jm = 0.001; Bm = 0.0001;

% Full model (Va → omega_m)
G_motor = Km / (La*Jm*s^2 + (La*Bm + Ra*Jm)*s + Ra*Bm + Km*Kemf);

% Simplified (La ≈ 0)
G_motor_simple = Km / (Jm*Ra*s + Ra*Bm + Km*Kemf);

pole(G_motor)
dcgain(G_motor)
step(G_motor); grid on;
```

---

## 20. Quick Formulas Reference

```
LAPLACE:
  derivative → multiply by s:  dy/dt → sY(s)
  integral   → divide by s:    ∫y dt → Y(s)/s
  step input: U(s) = 1/s
  exponential e^(-at): 1/(s+a)

TRANSFER FUNCTION:
  DC gain: Kss = G(0) = lim_{s→0} G(s)
  Final value: y_ss = lim_{s→0} s * Y(s)

1ST ORDER: G = Kss * wb / (s + wb)
  tau = 1/wb
  63.2% at t = tau
  settled at t ≈ 4-5*tau

2ND ORDER: G = Kss * wn^2 / (s^2 + 2*z*wn*s + wn^2)
  wn = sqrt(constant term in den)
  zeta = (middle coeff) / (2*wn)
  overshoot = exp(-pi*z/sqrt(1-z^2)) * 100%
  wd = wn*sqrt(1-z^2)
  ts ≈ 4/(z*wn)

CLOSED-LOOP:
  G_cl = Forward / (1 + Loop_gain)
  G_cl = C*G / (1 + C*G*H)

P-CONTROLLER STEADY-STATE ERROR:
  ess = r / (1 + Kp*G(0))

BODE:
  Gain crossover wgc: |G(jw)| = 0 dB → read PM here
  Phase crossover wpc: angle(G(jw)) = -180° → read GM here
  Phase margin = 180° + angle(G(j*wgc))
  Pole → -20 dB/dec, 0→-90° phase
  Zero → +20 dB/dec, 0→+90° phase
  Integrator 1/s → -20 dB/dec always, fixed -90°

STABILITY:
  All poles in LHP (Re < 0) → stable
  Any pole in RHP (Re > 0) → unstable
  PM > 0 → stable, PM ≥ 45° → robust

SINUSOIDAL STEADY STATE:
  u(t) = A*sin(w*t)
  y(t) = A*|G(jw)|*sin(w*t + angle(G(jw)))
```

---

## 21. All-in-One Analysis Block

Paste this, fill in your G(s), and run to get everything at once:

```matlab
clear all; clc; close all;
s = tf('s');

%% === FILL IN YOUR TRANSFER FUNCTION ===
G = 220 / (s^2 + 10*s + 100);

%% === ANALYSIS ===
[num_c, den_c] = tfdata(G, 'v');
p = pole(G);
z = zero(G);

fprintf('=== Transfer Function ===\n');
G
fprintf('Poles: '); disp(p');
fprintf('Zeros: '); disp(z');
fprintf('DC gain (Kss): %.4f\n', dcgain(G));

% Stability
if all(real(p) < 0)
    fprintf('STABLE (all poles in LHP)\n');
else
    fprintf('UNSTABLE\n');
end

% Order detection
order = length(den_c) - 1;
fprintf('System order: %d\n\n', order);

if order == 1
    wb = den_c(2)/den_c(1);
    tau = 1/wb;
    fprintf('=== 1st Order Parameters ===\n');
    fprintf('Break freq wb = %.4f rad/s\n', wb);
    fprintf('Time const tau = %.4f s\n', tau);
    fprintf('63%% at t = %.4f s\n', tau);
    fprintf('Settled at t ≈ %.4f s\n', 5*tau);
elseif order == 2
    wn = sqrt(den_c(3)/den_c(1));
    zeta = den_c(2) / (2*wn*den_c(1));
    Kss = num_c(end) / (den_c(1)*wn^2);
    fprintf('=== 2nd Order Parameters ===\n');
    fprintf('wn   = %.4f rad/s\n', wn);
    fprintf('zeta = %.4f\n', zeta);
    fprintf('Kss  = %.4f\n', Kss);
    if zeta < 1
        wd = wn*sqrt(1-zeta^2);
        Mp = exp(-pi*zeta/sqrt(1-zeta^2))*100;
        fprintf('wd   = %.4f rad/s (damped)\n', wd);
        fprintf('Mp   = %.2f %% overshoot\n', Mp);
        fprintf('Type: Underdamped\n');
    elseif zeta == 1
        fprintf('Type: Critically damped\n');
    else
        fprintf('Type: Overdamped\n');
    end
    ts = 4/(zeta*wn);
    fprintf('ts   ≈ %.4f s (settling)\n', ts);
end

% Step response metrics
info = stepinfo(G);
fprintf('\n=== Step Response ===\n');
fprintf('Rise time:     %.4f s\n', info.RiseTime);
fprintf('Settling time: %.4f s\n', info.SettlingTime);
fprintf('Overshoot:     %.2f %%\n', info.Overshoot);

% Margins
[Gm, Pm, Wcg, Wcp] = margin(G);
fprintf('\n=== Margins ===\n');
fprintf('Gain margin:  %.2f dB at %.2f rad/s\n', 20*log10(Gm), Wcg);
fprintf('Phase margin: %.2f deg at %.2f rad/s\n', Pm, Wcp);

% Plots
figure('Position', [100 100 1200 800]);
subplot(2,2,1); step(G); grid on; title('Step Response');
subplot(2,2,2); impulse(G); grid on; title('Impulse Response');
subplot(2,2,[3 4]); margin(G); title('Bode Plot with Margins');
```

---

## 22. Block Diagram with Feedback — Phase at a Frequency

**Problem pattern:** Given a block diagram with forward path and feedback, find the
phase of the closed-loop (or open-loop) TF at a specific frequency.

### Method

1. **Reduce the block diagram** to a single transfer function G(s)
2. **Substitute s = jω** at the given frequency
3. **Compute the phase:** `angle(G(jω))` in degrees

### Worked Example (Midterm Q2)

```
u → [A(s)] → (+,-) → [1/J] → ÿ → [1/s²] → y
                ↑                              |
                └────── [B(s)] ←───────────────┘
```

With A(s) = 1, J = 1, B(s) = 0:

```matlab
s = tf('s');

A = 1;
J = 1;
B_fb = 0;

% Forward path (from summing junction to y): (1/J) * (1/s^2)
G_fwd = (1/J) * (1/s^2);

% With B(s) = 0, feedback is zero → no loop
% Closed-loop = A * G_fwd / (1 + A * G_fwd * B_fb)
% But B_fb = 0, so denominator = 1
% G_total = A * G_fwd = 1/s^2
G_total = A * G_fwd;

% Evaluate at w = 1 rad/s
w = 1;
Gjw = evalfr(G_total, 1j*w);
fprintf('G(j*%.1f) = %.4f + j*%.4f\n', w, real(Gjw), imag(Gjw));
fprintf('|G|   = %.4f\n', abs(Gjw));
fprintf('Phase = %.1f deg\n', rad2deg(angle(Gjw)));
```

**Output:** Phase = -180°

**Why:** G(s) = 1/s². Each 1/s contributes -90° phase.
Two integrators → -90° + -90° = **-180°**.

### Quick phase rules (no MATLAB needed)

```
1/s     → -90°   (one integrator)
1/s²    → -180°  (two integrators)
1/s³    → -270°  (three integrators)
s       → +90°   (one differentiator)
K       → 0°     (pure gain, positive K)
-K      → ±180°  (negative gain)

1/(s+a) at w:  phase = -arctan(w/a)
  w << a → ≈ 0°
  w = a  → -45°
  w >> a → ≈ -90°
```

### General: phase of any TF at a frequency

```matlab
s = tf('s');

% Define your TF
G = 1 / (s^2 + 3*s + 2);

% Pick frequency
w = 1;

Gjw = evalfr(G, 1j*w);
fprintf('Phase at w=%.2f: %.2f deg\n', w, rad2deg(angle(Gjw)));
```

### By hand (no MATLAB)

Substitute s = jω into G(s), then:
1. Compute the **real** and **imaginary** parts of the complex number
2. Phase = arctan(imag/real), adjusted for quadrant

Example: G(s) = 1/s², w = 1
- G(j·1) = 1/(j)² = 1/(-1) = -1 + 0j
- Phase = arctan(0 / -1) = 180° → but in negative real axis → **-180°**
