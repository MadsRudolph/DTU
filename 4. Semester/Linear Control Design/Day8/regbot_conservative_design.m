%% REGBOT Position Controller — Conservative Design
%  Day 8 — 34722 Linear Control Design 1
%  More conservative parameters: N_i=3, alpha=0.3
clear all; clc;

load('../Day5/Day5_results.mat');
s = tf('s');
G_pos = minreal(G_floor_avg * (1/s));

% Conservative design parameters
N_i = 3;  alpha = 0.3;  gamma_M = 60;

w = logspace(-1, 5, 5000);
[~, P_bode, w_out] = bode(G_pos, w);
P_bode = squeeze(P_bode);

phi_i = rad2deg(-atan(1/N_i));
phi_m = rad2deg(asin((1 - alpha)/(1 + alpha)));
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

fprintf('============================================\n');
fprintf('  REGBOT CONSERVATIVE CONTROLLER\n');
fprintf('  N_i = %d, alpha = %.1f, gamma_M = %d deg\n', N_i, alpha, gamma_M);
fprintf('============================================\n');
fprintf('  K_P      = %.4f\n', K_P);
fprintf('  tau_i    = %.4f\n', tau_i);
fprintf('  tau_zero = %.4f\n', tau_d);
fprintf('  tau_pole = %.4f\n', alpha * tau_d);
fprintf('============================================\n');
fprintf('  omega_c      = %.2f rad/s\n', omega_c);
fprintf('  Phase margin = %.2f deg\n', pm);
fprintf('============================================\n');
