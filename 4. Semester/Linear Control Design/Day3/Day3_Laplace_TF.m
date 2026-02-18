%% Day 3 - Laplace Transform, Transfer Functions & Frequency Response
%  34722 Linear Control Design 1 — Lecture 3 Companion
%  Topics: Symbolic Laplace, TF creation, frequency response, phasors,
%          partial fractions, block diagram verification.
clear all; clc; close all;

% Plot settings
set(0, 'DefaultTextInterpreter', 'none');
set(0, 'DefaultAxesFontSize', 14);
set(0, 'DefaultLineLineWidth', 1.5);

% Image export path
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

%% ========================================================================
%  SECTION 1: Symbolic Laplace Transforms
%  Verify the Laplace table from Lecture 3, Slide 16
%  ========================================================================
syms t s

fprintf('=== Laplace Transform Table Verification ===\n\n');

fprintf('  %-14s  %-25s  %s\n', 'f(t)', 'F(s)', 'Expected');
fprintf('  %s\n', repmat('-', 1, 65));

% Each row: name, f(t), expected F(s) string
fprintf('  %-14s  %-25s  %s\n', 'exp(-3t)',    char(laplace(exp(-3*t), t, s)),    '1/(s+3)');
fprintf('  %-14s  %-25s  %s\n', 't (ramp)',    char(laplace(t, t, s)),            '1/s^2');
fprintf('  %-14s  %-25s  %s\n', 'sin(5t)',     char(laplace(sin(5*t), t, s)),     '5/(s^2+25)');
fprintf('  %-14s  %-25s  %s\n', 'cos(5t)',     char(laplace(cos(5*t), t, s)),     's/(s^2+25)');
fprintf('  %-14s  %-25s  %s\n', 't*exp(-2t)',  char(laplace(t*exp(-2*t), t, s)),  '1/(s+2)^2');

% Inverse transforms
fprintf('\n=== Inverse Laplace ===\n\n');
F_test = 1 / (s^2 + 4*s + 40);
f_test = ilaplace(F_test, s, t);
fprintf('  L^{-1}{ 1/(s^2+4s+40) } = %s\n', char(f_test));
fprintf('  (damped sine — poles at s = -2 +/- j6)\n');

%% ========================================================================
%  SECTION 2: Laplace Rules — Differentiation and Integration
%  Show that d/dt -> s and integral -> 1/s
%  ========================================================================
fprintf('\n=== Laplace Differentiation Rule ===\n');
fprintf('  Rule: L{df/dt} = s*F(s) - f(0)\n\n');

syms t s
f_t = exp(-2*t);
F_s = laplace(f_t, t, s);               % 1/(s+2)

% Differentiation: L{df/dt} should equal s*F(s) - f(0)
df_t = diff(f_t, t);                     % -2*exp(-2t)
L_df = laplace(df_t, t, s);
f_0  = double(subs(f_t, t, 0));          % f(0) = 1

fprintf('  f(t) = exp(-2t),  f(0) = %d\n', f_0);
fprintf('  F(s) = %s\n', char(F_s));
fprintf('  L{df/dt}      = %s\n', char(L_df));
fprintf('  s*F(s) - f(0)  = %s\n', char(s * F_s - f_0));

% Check they are equal
check = double(subs(s * F_s - f_0 - L_df, s, 5));   % Evaluate at s=5
fprintf('  Numerical check at s=5: difference = %.6f  (should be 0)\n', check);

fprintf('\n=== Laplace Integration Rule ===\n');
fprintf('  Rule: L{int f dt} = F(s)/s\n\n');

int_f = int(f_t, 0, t);
L_int = laplace(int_f, t, s);
fprintf('  L{int f dt}  = %s\n', char(L_int));
fprintf('  F(s)/s       = %s\n', char(F_s / s));

check_int = double(subs(L_int - F_s / s, s, 5));
fprintf('  Numerical check at s=5: difference = %.6f  (should be 0)\n', check_int);

%% ========================================================================
%  SECTION 3: Transfer Functions — Creation and Inspection
%  ========================================================================
fprintf('\n=== Transfer Function Creation ===\n\n');

% First-order system from the lecture
s = tf('s');
G1 = 10 / (s + 312);

% Second-order system (mass-spring-damper)
G2 = 40 / (s^2 + 4*s + 40);

fprintf('G1 (first-order):\n');  G1
fprintf('G2 (second-order):\n'); G2

% Poles and zeros
fprintf('G1 poles: ');  disp(pole(G1)');
fprintf('G2 poles: ');  disp(pole(G2)');
fprintf('G1 DC gain: %.4f\n', dcgain(G1));
fprintf('G2 DC gain: %.4f\n', dcgain(G2));

% Natural frequency and damping of G2
wn = sqrt(40);
zeta = 4 / (2 * wn);
fprintf('G2 natural frequency: w0 = %.2f rad/s\n', wn);
fprintf('G2 damping ratio:     zeta = %.3f (underdamped)\n', zeta);

%% ========================================================================
%  SECTION 4: Step and Impulse Response
%  ========================================================================
s = tf('s');
G1 = 10 / (s + 312);
G2 = 40 / (s^2 + 4*s + 40);

fig1 = figure('Name', 'Step and Impulse Response');

subplot(2, 2, 1);
step(G1); title('G1: Step Response'); grid on;

subplot(2, 2, 2);
step(G2); title('G2: Step Response'); grid on;

subplot(2, 2, 3);
impulse(G1); title('G1: Impulse Response'); grid on;

subplot(2, 2, 4);
impulse(G2); title('G2: Impulse Response'); grid on;

exportgraphics(fig1, [img_path 'ex3_step_impulse.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 5: Control Question 1 — Constant Input (Slide 25)
%  G(s) = s/(s+10), v(t) = 5
%  Expected: xdot(t) = 5*exp(-10t)
%  ========================================================================
s = tf('s');
G = s / (s + 10);

t = 0:0.001:1;
u = 5 * ones(size(t));
[y, t_out] = lsim(G, u, t);

% Analytical solution
y_exact = 5 * exp(-10 * t);

fig2 = figure('Name', 'Q1: Constant Input');
plot(t_out, y, 'b', t, y_exact, 'r--');
xlabel('Time [s]'); ylabel('xdot(t)');
title('Q1: G(s) = s/(s+10), v(t) = 5');
legend('lsim', '5 exp(-10t)', 'Location', 'best');
grid on;

exportgraphics(fig2, [img_path 'ex3_Q1_constant_input.png'], 'Resolution', 200);

% Symbolic verification
fprintf('\n=== Q1: Symbolic Verification ===\n');
syms s_sym t_sym
Xdot_s = (5 / s_sym) * (s_sym / (s_sym + 10));
xdot_t = ilaplace(Xdot_s, s_sym, t_sym);
fprintf('  xdot(t) = %s\n', char(xdot_t));

%% ========================================================================
%  SECTION 6: Control Question 2 — Exponential Input (Slide 26)
%  G(s) = s/(s+10), v(t) = exp(-3t)
%  Expected: xdot(t) = 10/7*exp(-10t) - 3/7*exp(-3t)
%  ========================================================================
s = tf('s');
G = s / (s + 10);

t = 0:0.001:2;
u = exp(-3 * t);
[y, t_out] = lsim(G, u, t);

% Analytical solution
y_exact = (10/7) * exp(-10 * t) - (3/7) * exp(-3 * t);

fig3 = figure('Name', 'Q2: Exponential Input');
plot(t_out, y, 'b', t, y_exact, 'r--');
xlabel('Time [s]'); ylabel('xdot(t)');
title('Q2: G(s) = s/(s+10), v(t) = exp(-3t)');
legend('lsim', 'Analytical', 'Location', 'best');
grid on;

exportgraphics(fig3, [img_path 'ex3_Q2_exponential_input.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 7: Partial Fraction Expansion
%  Xdot(s) = s / ((s+3)(s+10))
%  ========================================================================
fprintf('\n=== Partial Fraction Expansion ===\n');

num = [1, 0];                            % s
den = conv([1, 3], [1, 10]);             % (s+3)(s+10) = s^2 + 13s + 30

[r, p, k] = residue(num, den);

fprintf('  Xdot(s) = s / ((s+3)(s+10))\n\n');
for i = 1:length(r)
    fprintf('  Residue r%d = %+.4f  at pole p%d = %.1f\n', i, r(i), i, p(i));
end
fprintf('\n  => xdot(t) = %.4f*exp(%.0ft) + %.4f*exp(%.0ft)\n', ...
    r(1), p(1), r(2), p(2));

%% ========================================================================
%  SECTION 8: Frequency Response — Phasor Evaluation
%  Lecture 3, Slides 33-41
%  ========================================================================
fprintf('\n=== Frequency Response: First-Order System (Slide 35) ===\n');

s = tf('s');
G1 = 10 / (s + 312);

w = 628;                                  % rad/s
z = evalfr(G1, 1j * w);
M = abs(z);
phi = rad2deg(angle(z));

fprintf('  G(j%.0f) = %.4f at angle %.1f deg\n', w, M, phi);
fprintf('  y(t) = %.4f * cos(%.0f*t + (%.1f deg))\n\n', M, w, phi);

% ---

fprintf('=== Frequency Response: Second-Order System (Slide 41) ===\n');

G2 = 40 / (s^2 + 4*s + 40);

w_test = [0.1, sqrt(40), 1000];
labels = {'Low freq', 'Resonance', 'High freq'};

fprintf('  %-12s  %10s  %10s  %10s\n', 'Region', 'w [rad/s]', '|G(jw)|', 'angle [deg]');
fprintf('  %s\n', repmat('-', 1, 50));

for k = 1:length(w_test)
    z = evalfr(G2, 1j * w_test(k));
    fprintf('  %-12s  %10.2f  %10.4f  %10.1f\n', ...
        labels{k}, w_test(k), abs(z), rad2deg(angle(z)));
end

%% ========================================================================
%  SECTION 9: Bode Plot — Frequency Sweep
%  Preview of Lesson 6
%  ========================================================================
s = tf('s');
G2 = 40 / (s^2 + 4*s + 40);

w = logspace(-1, 3, 1000);
[mag, phase] = bode(G2, w);
mag = squeeze(mag);
phase = squeeze(phase);

fig4 = figure('Name', 'Bode Plot');

subplot(2, 1, 1);
semilogx(w, 20*log10(mag), 'b');
xlabel('w [rad/s]'); ylabel('|G(jw)| [dB]');
title('G(s) = 40/(s^2+4s+40) — Magnitude');
grid on;
xline(sqrt(40), 'r--', 'w_0 = sqrt(40)');

subplot(2, 1, 2);
semilogx(w, phase, 'b');
xlabel('w [rad/s]'); ylabel('angle G(jw) [deg]');
title('Phase');
grid on;
xline(sqrt(40), 'r--', 'w_0 = sqrt(40)');
yline(-90, 'k--', '-90 deg');

exportgraphics(fig4, [img_path 'ex3_bode_second_order.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 10: Phasor Example — RL Circuit (Slide 32)
%  i_s(t) = 2*cos(1000t), R = 1.2 Ohm, L = 0.6 mH
%  ========================================================================
fprintf('\n=== Phasor Example: RL Circuit ===\n');

w = 1000;              % rad/s
R = 1.2;               % Ohm
L = 0.6e-3;            % H

I_s = 2;               % Current phasor magnitude (phase = 0)

Z = R + 1j * w * L;    % Complex impedance
fprintf('  Z = %.2f + j%.2f = %.3f at angle %.1f deg\n', ...
    real(Z), imag(Z), abs(Z), rad2deg(angle(Z)));

V_out = Z * I_s;
fprintf('  V_out = %.3f at angle %.1f deg\n', abs(V_out), rad2deg(angle(V_out)));
fprintf('  v_out(t) = %.2f * cos(%d*t + %.1f deg)\n', ...
    abs(V_out), w, rad2deg(angle(V_out)));

%% ========================================================================
%  SECTION 11: Component Impedance vs Frequency
%  ========================================================================
C_val = 1e-6;  % 1 uF
L_val = 1e-3;  % 1 mH
R_val = 100;   % 100 Ohm

w = logspace(1, 6, 1000);

Z_R = R_val * ones(size(w));
Z_C = 1 ./ (w * C_val);
Z_L = w * L_val;

fig5 = figure('Name', 'Component Impedance');
loglog(w, Z_R, 'k', w, Z_C, 'b', w, Z_L, 'r');
xlabel('w [rad/s]'); ylabel('|Z| [Ohm]');
title('Component Impedance vs Frequency');
legend('R = 100 Ohm', 'C = 1 uF', 'L = 1 mH', 'Location', 'best');
grid on;

% Mark resonant frequency
w_res = 1 / sqrt(L_val * C_val);
xline(w_res, 'g--', sprintf('w_0 = %.0f rad/s', w_res));

exportgraphics(fig5, [img_path 'ex3_impedance_vs_freq.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 12: Block Diagram Verification
%  Verify hand-calculated TFs from Day 3 Block Diagram Exercises
%  ========================================================================
s = tf('s');

% --- Exercise 1: y/u = G/(s+GH) ---
G_val = 5;  H_val = 2;

forward = G_val / s;
T_block   = feedback(forward, H_val);
T_formula = G_val / (s + G_val * H_val);

fig6 = figure('Name', 'Block Diagram Verification');

subplot(2, 2, 1);
step(T_block, 'b', T_formula, 'r--');
legend('blocks', 'formula');
title('Ex 1: G/(s+GH)');
grid on;

% --- Exercise 3: x/tau = R/(s(Js+B)) ---
J = 0.01;  B_val = 0.1;  R_val = 0.05;

inner = feedback(1/(J*s), B_val);
T_block   = inner * R_val / s;
T_formula = R_val / (s * (J*s + B_val));

subplot(2, 2, 2);
step(T_block, 'b', T_formula, 'r--', 5);
legend('blocks', 'formula');
title('Ex 3: R / (s(Js+B))');
grid on;

% --- Exercise 4: y/u = D(Gs+K)/((1+DG)s+DK) ---
G_val = 3;  K_val = 2;  D_val = 4;

% Forward: parallel (G + K/s) * D, feedback from y
parallel_path = G_val + K_val / s;
forward = parallel_path * D_val;
T_block   = feedback(forward, 1);
T_formula = D_val*(G_val*s + K_val) / ((1 + D_val*G_val)*s + D_val*K_val);

subplot(2, 2, 3);
step(T_block, 'b', T_formula, 'r--');
legend('blocks', 'formula');
title('Ex 4: D(Gs+K) / ((1+DG)s+DK)');
grid on;

% --- Exercise 5: y/u = AB/(Cs^2+Ds+1) ---
A = 2;  B_v = 20;  C_v = 0.025;  D_v = 0.1;

inner_fwd = (1/C_v) * (1/s);
inner     = feedback(inner_fwd, D_v);
outer_fwd = inner * (1/s);
outer     = feedback(outer_fwd, 1);
T_block   = outer * A * B_v;
T_formula = A * B_v / (C_v * s^2 + D_v * s + 1);

subplot(2, 2, 4);
step(T_block, 'b', T_formula, 'r--');
legend('blocks', 'formula');
title('Ex 5: AB / (Cs^2+Ds+1)');
grid on;

exportgraphics(fig6, [img_path 'ex3_block_verification.png'], 'Resolution', 200);

fprintf('\n=== All sections complete ===\n');
