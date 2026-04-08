%% REGBOT Position Controller — Mild Design
%  Try several K_P values with N_i=3, alpha=0.3 to find one that works
%  on the real REGBOT without severe integrator windup.
clear all; clc;

load('../Day5/Day5_results.mat');
s = tf('s');
G_pos = minreal(G_floor_avg * (1/s));

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
K_P_design = 1 / abs(freqresp(G_ol_noK, omega_c));

% Test with reduced K_P values
K_P_values = [K_P_design, K_P_design/2, K_P_design/4, 5, 2];
G_cl_fb_list = {};

fprintf('tau_i    = %.4f\n', tau_i);
fprintf('tau_zero = %.4f\n', tau_d);
fprintf('tau_pole = %.4f\n', alpha * tau_d);
fprintf('\n');

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(1); clf;
hold on;
for k = 1:length(K_P_values)
    Kp = K_P_values(k);
    G_cl = minreal(Kp*C_PI*G_pos / (1 + Kp*C_PI*C_D*G_pos));
    [y, t] = step(G_cl, 0:0.001:5);
    plot(t, 0.5*y);

    si = stepinfo(G_cl);
    [~, pm] = margin(Kp * G_ol_noK);
    fprintf('K_P = %6.2f | PM = %5.1f deg | Rise = %.3fs | Settle = %.3fs | OS = %.1f%%\n', ...
        Kp, pm, si.RiseTime, si.SettlingTime, si.Overshoot);
end
plot([0 5], [0.5 0.5], '--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('Position [m]');
title('Step response for different $K_P$ (linear, no saturation)');
legend(arrayfun(@(k) sprintf('$K_P = %.1f$', k), K_P_values, 'UniformOutput', false), ...
    'interpreter', 'latex');

fprintf('\n--- Recommendation ---\n');
fprintf('Keep tau_i/tau_zero/tau_pole the same, try K_P = 5:\n');
fprintf('  K_P      = 5\n');
fprintf('  tau_i    = %.4f\n', tau_i);
fprintf('  tau_zero = %.4f\n', tau_d);
fprintf('  tau_pole = %.4f\n', alpha * tau_d);
