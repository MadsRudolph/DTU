%% REGBOT Position Controller v2 — Using 1-pole floor model
%  Day 8 — 34722 Linear Control Design 1
%  Redesign using the improved Day 5 identification (training wheels).
clear all; clc; close all;

img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

%% Load new TF
load('../../Day5/Day5_results_v2.mat');
s = tf('s');

% Use 1-pole model (same fit as 2-pole, simpler and more robust)
G_vel = G_1p_avg;
fprintf('=== Velocity TF (1-pole, training wheels) ===\n');
G_vel
fprintf('DC gain: %.4f, Pole: %.4f, tau: %.4f s\n', ...
    dcgain(G_vel), pole(G_vel), -1/pole(G_vel));

% Position TF: multiply by 1/s
G_pos = minreal(G_vel * (1/s));
fprintf('\n=== Position TF ===\n');
G_pos

%% Design: N_i=3, alpha=0.3, gamma_M=60
N_i = 3;  alpha = 0.3;  gamma_M = 60;

w = logspace(-2, 4, 5000);
[~, P_bode, w_out] = bode(G_pos, w);
P_bode = squeeze(P_bode);

phi_i = rad2deg(-atan(1/N_i));
phi_m = rad2deg(asin((1-alpha)/(1+alpha)));
phi_G_req = -180 + gamma_M - phi_i - phi_m;

i_c = find(P_bode <= phi_G_req, 1);
omega_c = w_out(i_c);

tau_i = N_i / omega_c;
tau_d = 1 / (omega_c * sqrt(alpha));
C_PI = (1 + 1/(tau_i*s));
C_D  = (tau_d*s + 1) / (alpha*tau_d*s + 1);

G_ol_noK = minreal(C_PI * C_D * G_pos);
K_P = 1 / abs(freqresp(G_ol_noK, omega_c));

[~, pm] = margin(K_P * G_ol_noK);

fprintf('\n============================================\n');
fprintf('  REGBOT CONTROLLER v2 (1-pole model)\n');
fprintf('  N_i = %d, alpha = %.1f, gamma_M = %d deg\n', N_i, alpha, gamma_M);
fprintf('============================================\n');
fprintf('  K_P      = %.4f\n', K_P);
fprintf('  tau_i    = %.4f\n', tau_i);
fprintf('  tau_zero = %.4f\n', tau_d);
fprintf('  tau_pole = %.4f\n', alpha * tau_d);
fprintf('============================================\n');
fprintf('  omega_c      = %.2f rad/s\n', omega_c);
fprintf('  Phase margin = %.2f deg\n', pm);
fprintf('  Initial control (0.5m step) = %.1f V\n', K_P * 0.5);
fprintf('============================================\n');

%% Step response prediction
G_cl_fb = minreal(K_P*C_PI*G_pos / (1 + K_P*C_PI*C_D*G_pos));
si = stepinfo(G_cl_fb);

fprintf('\nLinear step response (feedback arch.):\n');
fprintf('  Rise time:     %.4f s\n', si.RiseTime);
fprintf('  Settling time: %.4f s\n', si.SettlingTime);
fprintf('  Overshoot:     %.2f %%\n', si.Overshoot);
fprintf('  Bandwidth:     %.2f rad/s\n', bandwidth(G_cl_fb));

%% Plot step response
[y, t] = step(G_cl_fb, 0:0.001:5);
figure(1); clf;
plot(t, 0.5*y);
hold on;
plot(t, 0.5*ones(size(t)), '--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('Position [m]');
title('Predicted step response (v2, 1-pole model)');
legend({'PI-Lead (feedback)', 'Reference'}, 'interpreter', 'latex');
saveas(gcf, [img_path 'day8_regbot_v2_predicted.png']);
