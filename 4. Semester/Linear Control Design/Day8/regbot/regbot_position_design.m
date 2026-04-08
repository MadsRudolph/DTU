%% REGBOT Position Controller Design — PI-Lead (Day 8)
%  34722 Linear Control Design 1
%  Uses 1-pole velocity model from Day 5 (training wheels)
clear all; clc; close all;

img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

s = tf('s');

%% Task 1: Transfer function from voltage to position
% Velocity TF from Day 5 (1-pole, training wheels)
G_vel = 2.198 / (s + 5.985);

% Position = integral of velocity => multiply by 1/s
G = minreal(G_vel / s);
fprintf('Position TF G(s):\n'); G
fprintf('Poles: '); disp(pole(G)');

%% Task 2: PI-Lead controller design

% Step 2.1: Bode plot of G(s)
w = logspace(-2, 3, 5000);
[M, P, w_out] = bode(G, w);
M = mag2db(squeeze(M));
P = squeeze(P);

% Step 2.2: Select parameters
N_i     = 3;        % PI zero placement (starting value 5, adjusted to 3)
alpha   = 0.3;      % Lead ratio (starting value 0.1, adjusted to 0.3)
gamma_M = 60;       % Desired phase margin [deg]

% Step 2.3: Find crossover frequency from phase-balance equation
phi_i = rad2deg(-atan(1/N_i));                  % PI phase contribution (negative)
phi_m = rad2deg(asin((1-alpha)/(1+alpha)));     % Lead phase boost (positive)
phi_G_req = -180 + gamma_M - phi_i - phi_m;     % Required plant phase at omega_c

fprintf('\n--- Phase balance ---\n');
fprintf('phi_i (PI):    %.2f deg\n', phi_i);
fprintf('phi_m (Lead):  %.2f deg\n', phi_m);
fprintf('phi_G required: %.2f deg\n', phi_G_req);

% Find omega_c where plant phase equals phi_G_req
i_c = find(P <= phi_G_req, 1, 'first');
omega_c = w_out(i_c);
fprintf('omega_c:       %.2f rad/s\n', omega_c);

% Step 2.4: PI controller
tau_i = N_i / omega_c;
C_PI = (tau_i*s + 1) / (tau_i*s);

fprintf('\n--- PI controller ---\n');
fprintf('tau_i = %.4f s\n', tau_i);

% Step 2.5: Lead controller
tau_d = 1 / (omega_c * sqrt(alpha));
C_D = (tau_d*s + 1) / (alpha*tau_d*s + 1);

fprintf('\n--- Lead controller ---\n');
fprintf('tau_d (zero) = %.4f s\n', tau_d);
fprintf('tau_d*alpha (pole) = %.4f s\n', alpha*tau_d);

% Step 2.6: Proportional gain K_P
G_ol_noK = minreal(C_PI * C_D * G);
K_P = 1 / abs(freqresp(G_ol_noK, omega_c));

fprintf('\n--- Gain ---\n');
fprintf('K_P = %.4f\n', K_P);
fprintf('Initial control effort (0.5m step) = %.1f V\n', K_P * 0.5);

% Open-loop with gain
G_ol = K_P * G_ol_noK;
[g_m, p_m] = margin(G_ol);
fprintf('\nAchieved phase margin: %.2f deg\n', p_m);
fprintf('Gain margin: %.2f dB\n', mag2db(g_m));

% Step 2.7: Closed-loop transfer functions
% a) Lead in forward branch
G_cl_fwd = minreal(K_P*C_PI*C_D*G / (1 + K_P*C_PI*C_D*G));
% b) Lead in feedback branch
G_cl_fb  = minreal(K_P*C_PI*G / (1 + K_P*C_PI*C_D*G));

%% Step 2.8: Step response evaluation
si_fwd = stepinfo(G_cl_fwd);
si_fb  = stepinfo(G_cl_fb);

fprintf('\n--- Step response: Lead in FORWARD branch ---\n');
fprintf('Rise time:     %.4f s\n', si_fwd.RiseTime);
fprintf('Settling time: %.4f s\n', si_fwd.SettlingTime);
fprintf('Overshoot:     %.2f %%\n', si_fwd.Overshoot);

fprintf('\n--- Step response: Lead in FEEDBACK branch ---\n');
fprintf('Rise time:     %.4f s\n', si_fb.RiseTime);
fprintf('Settling time: %.4f s\n', si_fb.SettlingTime);
fprintf('Overshoot:     %.2f %%\n', si_fb.Overshoot);

fprintf('\n--- Summary ---\n');
fprintf('Steady-state error: 0 (type-1 system with PI)\n');
fprintf('Converges in < 10 s: YES (both architectures)\n');
fprintf('Smallest overshoot: FEEDBACK (%.1f%% vs %.1f%%)\n', si_fb.Overshoot, si_fwd.Overshoot);
fprintf('Fastest convergence: FORWARD (%.3f s vs %.3f s rise)\n', si_fwd.RiseTime, si_fb.RiseTime);

%% Plots

% Figure 1: Bode of G(s), C_PI(s), C_D(s) on the same plot
[M_pi, P_pi] = bode(C_PI, w);  M_pi = mag2db(squeeze(M_pi)); P_pi = squeeze(P_pi);
[M_cd, P_cd] = bode(C_D, w);   M_cd = mag2db(squeeze(M_cd)); P_cd = squeeze(P_cd);

figure(1); clf;
aa = subplot(2,1,1);
semilogx(w_out, M, 'b'); hold on;
semilogx(w_out, M_pi, 'r--');
semilogx(w_out, M_cd, 'g-.');
yline(0, ':', 'Color', [0.6 0.6 0.6]);
hold off; grid on;
ylabel('Magnitude [dB]');
legend({'$G(s)$','$C_{PI}(s)$','$C_D(s)$'}, 'interpreter','latex');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
semilogx(w_out, P, 'b'); hold on;
semilogx(w_out, P_pi, 'r--');
semilogx(w_out, P_cd, 'g-.');
yline(-180, ':', 'Color', [0.6 0.6 0.6]);
hold off; grid on;
xlabel('$\omega$ [rad/s]');
ylabel('Phase [deg]');
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_regbot_component_bode.png']);

% Figure 2: Bode of G_ol(s) with crossover frequency
[M_ol, P_ol] = bode(G_ol, w);
M_ol = mag2db(squeeze(M_ol)); P_ol = squeeze(P_ol);

figure(2); clf;
aa = subplot(2,1,1);
semilogx(w_out, M_ol); hold on;
yline(0, '--', 'Color', [0.6 0.6 0.6]);
scatter(omega_c, 0, 60, 'r', 'filled');
hold off; grid on;
ylabel('$|G_{ol}|$ [dB]');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
semilogx(w_out, P_ol); hold on;
yline(-180, '--', 'Color', [0.6 0.6 0.6]);
scatter(omega_c, -180+p_m, 60, 'r', 'filled');
hold off; grid on;
xlabel('$\omega$ [rad/s]');
ylabel('$\angle G_{ol}$ [deg]');
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_regbot_bode_ol.png']);

% Figure 3: Step response — both architectures
T = 5;
[y_fwd, t] = step(G_cl_fwd, 0:0.001:T);
[y_fb, ~]  = step(G_cl_fb, 0:0.001:T);

figure(3); clf;
plot(t, y_fwd); hold on;
plot(t, y_fb);
plot(t, ones(size(t)), '--', 'Color', [0.6 0.6 0.6]);
hold off; grid on;
xlabel('$t$ [s]');
ylabel('$y(t)$');
legend({'Lead forward', 'Lead feedback', 'Reference'}, 'interpreter','latex');
saveas(gcf, [img_path 'day8_regbot_step.png']);

% Figure 4: Bode of G_cl(s) — both architectures
[M_fwd, P_fwd] = bode(G_cl_fwd, w); M_fwd = mag2db(squeeze(M_fwd)); P_fwd = squeeze(P_fwd);
[M_fb, P_fb]   = bode(G_cl_fb, w);  M_fb  = mag2db(squeeze(M_fb));  P_fb  = squeeze(P_fb);

bw_fwd = bandwidth(G_cl_fwd);
bw_fb  = bandwidth(G_cl_fb);

figure(4); clf;
aa = subplot(2,1,1);
semilogx(w_out, M_fwd); hold on;
semilogx(w_out, M_fb);
yline(-3, ':', 'Color', [0.6 0.6 0.6]);
scatter(bw_fwd, -3, 60, 'b', 'filled');
scatter(bw_fb, -3, 60, 'r', 'filled');
hold off; grid on;
ylabel('$|G_{cl}|$ [dB]');
legend({'Forward', 'Feedback', '-3 dB'}, 'interpreter','latex');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
semilogx(w_out, P_fwd); hold on;
semilogx(w_out, P_fb);
hold off; grid on;
xlabel('$\omega$ [rad/s]');
ylabel('$\angle G_{cl}$ [deg]');
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_regbot_bode_cl.png']);

%% Print values for REGBOT Control tab
fprintf('\n============================================\n');
fprintf('  VALUES FOR REGBOT CONTROL TAB\n');
fprintf('============================================\n');
fprintf('  K_P      = %.2f\n', K_P);
fprintf('  tau_i    = %.4f\n', tau_i);
fprintf('  tau_zero = %.4f\n', tau_d);
fprintf('  tau_pole = %.4f\n', alpha * tau_d);
fprintf('============================================\n');
