%% Midterm Template — 34722 Linear Control Design 1
%  Reusable code blocks for typical exam problems.
%  Copy the sections you need, fill in your numbers.
clear all; clc; close all;
set(0, 'DefaultAxesFontSize', 14);
set(0, 'DefaultLineLineWidth', 1.5);

s = tf('s');  % define s-variable for easy TF creation

%% ========================================================================
%  BLOCK A: TRANSFER FUNCTION — DEFINE & ANALYZE
%  ========================================================================

% --- Option 1: From expression ---
% G = 5 / (s^2 + 3*s + 2);

% --- Option 2: From coefficients G(s) = num(s)/den(s) ---
% num = [5];           % e.g. 5
% den = [1 3 2];       % e.g. s^2 + 3s + 2
% G = tf(num, den);

% --- Analyze ---
% pole(G)              % pole locations → stability check
% zero(G)              % zero locations
% dcgain(G)            % DC gain = G(0) = steady-state gain
% bandwidth(G)         % bandwidth in rad/s

%% ========================================================================
%  BLOCK B: ODE → TRANSFER FUNCTION
%  ========================================================================
%  Given: a2*y'' + a1*y' + a0*y = b1*u' + b0*u
%  G(s) = (b1*s + b0) / (a2*s^2 + a1*s + a0)

% a2 = 1; a1 = 3; a0 = 2;
% b1 = 0; b0 = 5;
% G = tf([b1 b0], [a2 a1 a0]);

%% ========================================================================
%  BLOCK C: SECOND-ORDER SYSTEM PARAMETERS
%  ========================================================================
%  G(s) = Kss * wn^2 / (s^2 + 2*zeta*wn*s + wn^2)

% wn   = sqrt(den(end));          % natural frequency
% zeta = den(end-1) / (2*wn);    % damping ratio
% Kss  = num(end) / wn^2;        % DC gain

% --- Or define from specs ---
% wn = 10; zeta = 0.7; Kss = 1;
% G = Kss * wn^2 / (s^2 + 2*zeta*wn*s + wn^2);

% --- Key formulas ---
% overshoot_pct = exp(-pi*zeta / sqrt(1-zeta^2)) * 100;
% wd = wn * sqrt(1 - zeta^2);         % damped frequency
% ts = 4 / (zeta * wn);               % settling time (2%)
% tr = 1.8 / wn;                      % rise time (approx)

%% ========================================================================
%  BLOCK D: STEP RESPONSE & TIME-DOMAIN ANALYSIS
%  ========================================================================

% figure;
% step(G);
% grid on; title('Step Response');

% info = stepinfo(G);
% fprintf('Rise time:     %.4f s\n', info.RiseTime);
% fprintf('Settling time: %.4f s\n', info.SettlingTime);
% fprintf('Overshoot:     %.2f %%\n', info.Overshoot);
% fprintf('Final value:   %.4f\n', info.SettlingMin);  % or dcgain(G)*step_size

% --- Step response with specific input magnitude ---
% U0 = 3;  % step size
% [y, t] = step(U0 * G);
% plot(t, y); xlabel('Time [s]'); ylabel('Output');

%% ========================================================================
%  BLOCK E: IMPULSE RESPONSE & ARBITRARY INPUT
%  ========================================================================

% figure;
% impulse(G);
% grid on; title('Impulse Response');

% --- Custom input signal ---
% t = 0:0.01:10;
% u = sin(2*t);                     % or any signal
% lsim(G, u, t);

%% ========================================================================
%  BLOCK F: BODE PLOT & STABILITY MARGINS
%  ========================================================================

% figure;
% bode(G); grid on;

% figure;
% margin(G);  % shows Gm, Pm on the plot

% [Gm, Pm, Wcg, Wcp] = margin(G);
% fprintf('Gain margin:    %.2f dB (at %.2f rad/s)\n', 20*log10(Gm), Wcg);
% fprintf('Phase margin:   %.2f deg (at %.2f rad/s)\n', Pm, Wcp);

%% ========================================================================
%  BLOCK G: BLOCK DIAGRAM REDUCTION — CLOSED-LOOP
%  ========================================================================
%
%  Standard negative feedback:
%    G_cl = Forward / (1 + Loop_gain)
%    G_cl = C*G / (1 + C*G*H)
%
%  Using MATLAB:
%    G_cl = feedback(C*G, H);       % negative feedback (default)
%    G_cl = feedback(C*G, H, +1);   % positive feedback

% C = Kp;                 % controller
% H = 1;                  % sensor (unity feedback if H=1)
% G_ol = C * G;           % open-loop TF
% G_cl = feedback(G_ol, H);
% G_cl = minreal(G_cl);   % simplify

%% ========================================================================
%  BLOCK H: P-CONTROLLER DESIGN
%  ========================================================================

% Kp = 15;
% G_ol = Kp * G;
% G_cl = feedback(G_ol, 1);

% --- Steady-state error for step input r ---
% r = 1;
% ess = r / (1 + Kp * dcgain(G));
% fprintf('Steady-state error: %.4f\n', ess);

% --- Check margins ---
% [Gm, Pm, Wcg, Wcp] = margin(G_ol);
% fprintf('Phase margin: %.2f deg\n', Pm);

%% ========================================================================
%  BLOCK I: PI-CONTROLLER DESIGN
%  ========================================================================

% Kp = 5; tau_i = 0.5;
% C_PI = Kp * (1 + 1/(tau_i * s));
% G_ol = C_PI * G;
% G_cl = feedback(G_ol, 1);

%% ========================================================================
%  BLOCK J: PID-CONTROLLER DESIGN
%  ========================================================================

% Kp = 5; tau_i = 0.5; tau_d = 0.1;
% C_PID = Kp * (1 + 1/(tau_i*s) + tau_d*s);
% G_ol = C_PID * G;
% G_cl = feedback(G_ol, 1);

%% ========================================================================
%  BLOCK K: ZIEGLER-NICHOLS (OPEN-LOOP METHOD)
%  ========================================================================
%  From open-loop step response:
%    L   = dead time (delay before response starts)
%    tau = time constant (tangent line intersection)
%    R   = slope = (delta_y / delta_u) / tau

% L = 0.1; tau = 1.0; delta_y = 2; delta_u = 1;
% R = (delta_y / delta_u) / tau;
%
% % P controller
% Kp_P = 1 / (R * L);
%
% % PI controller
% Kp_PI = 0.9 / (R * L);
% Ti_PI = L / 0.3;
%
% % PID controller
% Kp_PID = 1.2 / (R * L);
% Ti_PID = 2 * L;
% Td_PID = 0.5 * L;

%% ========================================================================
%  BLOCK L: ZIEGLER-NICHOLS (CLOSED-LOOP METHOD)
%  ========================================================================
%  Ku = ultimate gain (sustained oscillation)
%  Pu = oscillation period

% Ku = 20; Pu = 0.5;
%
% % P controller
% Kp_P = 0.5 * Ku;
%
% % PI controller
% Kp_PI = 0.45 * Ku;
% Ti_PI = Pu / 1.2;
%
% % PID controller
% Kp_PID = 0.6 * Ku;
% Ti_PID = 0.5 * Pu;
% Td_PID = 0.125 * Pu;

%% ========================================================================
%  BLOCK M: LOW-PASS FILTER IN FEEDBACK LOOP
%  ========================================================================

% wc = 50;                                % break frequency [rad/s]
% G_filt = wc / (s + wc);                 % 1st-order LP filter
%
% G_ol_filt = Kp * G * G_filt;            % filtered open-loop
% G_cl_filt = Kp*G / (1 + Kp*G*G_filt);  % closed-loop (filter in feedback)
% G_cl_filt = minreal(G_cl_filt);
%
% [~, Pm_filt, ~, ~] = margin(G_ol_filt);
% fprintf('Phase margin with filter: %.2f deg\n', Pm_filt);

%% ========================================================================
%  BLOCK N: FREQUENCY RESPONSE — EVALUATE G(jw)
%  ========================================================================

% w = 10;  % frequency in rad/s
% Gjw = evalfr(G, 1j*w);
% mag = abs(Gjw);
% phase_deg = rad2deg(angle(Gjw));
% mag_dB = 20*log10(mag);
%
% fprintf('At w = %.2f rad/s:\n', w);
% fprintf('  |G(jw)| = %.4f (%.2f dB)\n', mag, mag_dB);
% fprintf('  angle   = %.2f deg\n', phase_deg);

% --- Sinusoidal steady-state output ---
% A_in = 2; w_in = 5;
% A_out = A_in * abs(evalfr(G, 1j*w_in));
% phi_out = angle(evalfr(G, 1j*w_in));
% fprintf('Input:  %.1f * sin(%.1f * t)\n', A_in, w_in);
% fprintf('Output: %.4f * sin(%.1f * t + %.2f deg)\n', A_out, w_in, rad2deg(phi_out));

%% ========================================================================
%  BLOCK O: LAPLACE — SYMBOLIC
%  ========================================================================

% syms t_sym s_sym
%
% % Forward transform
% f = exp(-3*t_sym) * sin(5*t_sym);
% F = laplace(f, t_sym, s_sym);
% fprintf('F(s) = '); pretty(F)
%
% % Inverse transform
% F2 = 5 / (s_sym^2 + 3*s_sym + 2);
% f2 = ilaplace(F2, s_sym, t_sym);
% fprintf('f(t) = '); pretty(f2)
%
% % Partial fractions
% [r, p, k] = residue([5], [1 3 2]);
% % r = residues, p = poles, k = direct term

%% ========================================================================
%  BLOCK P: SYSTEM IDENTIFICATION (from data)
%  ========================================================================

% % Load and prepare data
% data = readtable('logfile.txt');
% t = table2array(data(:,1));
% u = table2array(data(:, col_input));
% y = table2array(data(:, col_output));
% Ts = t(2) - t(1);
%
% % Trim to step region
% idx = find(u >= threshold, 1, 'first');
% t = t(idx:end); u = u(idx:end); y = y(idx:end);
% t = t - t(1);
%
% % Remove offsets
% u = u - u(1);
% y = y - y(1);
%
% % Identify
% idd = iddata(y, u, Ts);
% G_est = tfest(idd, 2, 0);    % 2 poles, 0 zeros
% compare(idd, G_est);

%% ========================================================================
%  BLOCK Q: COMPARE MULTIPLE SYSTEMS
%  ========================================================================

% figure;
% step(G1, G2, G3);
% legend('System 1', 'System 2', 'System 3');
% grid on;

% figure;
% bode(G1, 'b', G2, 'r--');
% legend('G1', 'G2');
% grid on;

% figure;
% subplot(1,2,1); step(G1, G2); legend('G1','G2'); title('Step');
% subplot(1,2,2); bode(G1, G2); legend('G1','G2'); title('Bode');

%% ========================================================================
%  BLOCK R: FINAL VALUE THEOREM
%  ========================================================================

% % For step input of magnitude U0:
% U0 = 5;
% y_final = U0 * dcgain(G);
% fprintf('Final value (FVT): %.4f\n', y_final);
%
% % For ramp input u(t) = t → U(s) = 1/s^2:
% % y_final = lim_{s->0} s * G(s) * (1/s^2) = lim G(s)/s
% % Only works if system has integrator

%% ========================================================================
%  BLOCK S: DC MOTOR MODEL
%  ========================================================================
%  Electrical:  La*dIa/dt = Va - Ra*Ia - Kemf*wm
%  Mechanical:  Jm*dwm/dt = Km*Ia - Bm*wm - TL
%
%  TF from Va to wm (no load, La ≈ 0):
%    G(s) = Km / (Jm*Ra*s + Ra*Bm + Km*Kemf)

% Ra = 1; La = 0; Km = 0.01; Kemf = Km; Jm = 0.001; Bm = 0.0001;
% G_motor = Km / (Jm*Ra*s + Ra*Bm + Km*Kemf);

fprintf('=== Midterm Template Ready ===\n');
fprintf('Uncomment the blocks you need and fill in your values.\n');
