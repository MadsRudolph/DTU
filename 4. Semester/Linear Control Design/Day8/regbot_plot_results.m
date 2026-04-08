%% REGBOT Position Controller — Plot Experimental Results
%  Day 8 — 34722 Linear Control Design 1
%  Loads REGBOT log, plots position and voltage, compares with Simulink.
clear all; clc; close all;

img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

%% ========================================================================
%  SECTION 1: Load REGBOT Log
%  ========================================================================

opts = detectImportOptions('log_position.txt', 'FileType', 'text');
opts.CommentStyle = '%';
data = readtable('log_position.txt', opts);
data = fillmissing(data, 'nearest');

t    = table2array(data(:,1));     % time [s]
u_L  = table2array(data(:,8));     % left motor voltage [V]
u_R  = table2array(data(:,9));     % right motor voltage [V]
v_L  = table2array(data(:,10));    % left wheel velocity [m/s]
v_R  = table2array(data(:,11));    % right wheel velocity [m/s]
x    = table2array(data(:,14));    % pose x (driven distance) [m]

T_s = t(2) - t(1);
fprintf('Loaded %d samples, Ts = %.1f ms\n', length(t), T_s*1000);
fprintf('Time range: [%.3f, %.3f] s\n', t(1), t(end));

%% ========================================================================
%  SECTION 2: Offset position so it starts at 0
%  ========================================================================

x = x - x(1);   % position relative to start

%% ========================================================================
%  SECTION 3: Plot REGBOT Results
%  ========================================================================

figure(1); clf;
aa = subplot(3,1,1);
plot(t, x);
hold on;
plot(t, 0.5*ones(size(t)), '--k');
hold off;
grid on;
ylabel('$x, x_{ref}$ in m');
legend({'$x$', '$x_{ref} = 0.5$ m'}, 'interpreter', 'latex');
title('REGBOT Experimental Results');

bb = subplot(3,1,2);
plot(t, u_L, t, u_R);
hold on;
yline(9, '--r'); yline(-9, '--r');
hold off;
grid on;
ylabel('Voltage [V]');
legend({'$u_L$', '$u_R$', '$\pm 9$ V'}, 'interpreter', 'latex');

cc = subplot(3,1,3);
plot(t, v_L, t, v_R);
grid on;
xlabel('$t$ in s');
ylabel('Velocity [m/s]');
legend({'$v_L$', '$v_R$'}, 'interpreter', 'latex');

linkaxes([aa, bb, cc], 'x');
saveas(gcf, [img_path 'day8_regbot_results.png']);

%% ========================================================================
%  SECTION 4: Compare with Simulink
%  ========================================================================

% Reload controller and run Simulink for comparison
load('../Day5/Day5_results.mat');
s = tf('s');

G_vel = G_floor_avg;
G_pos = minreal(G_vel * (1/s));

N_i = 5;  alpha = 0.1;  gamma_M = 60;
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

% Linear (no saturation)
G_cl_fb = minreal(K_P*C_PI*G_pos / (1 + K_P*C_PI*C_D*G_pos));
[y_lin, t_lin] = step(G_cl_fb, 0:0.001:5);

% Find step moment in REGBOT data (when voltage first exceeds 1V)
u_avg = (u_L + u_R) / 2;
idx_step = find(abs(u_avg) > 1, 1, 'first');
t_regbot = t(idx_step:end) - t(idx_step);
x_regbot = x(idx_step:end) - x(idx_step);

figure(2); clf;
plot(t_regbot, x_regbot, 'b', 'LineWidth', 2);
hold on;
plot(t_lin, 0.5*y_lin, 'r--', 'LineWidth', 1.5);
plot(t_lin, 0.5*ones(size(t_lin)), '--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('Position [m]');
title('REGBOT vs MATLAB (linear model)');
legend({'REGBOT (experiment)', 'MATLAB (no saturation)', 'Reference'}, ...
    'interpreter', 'latex', 'Location', 'southeast');
xlim([0 min(3, t_regbot(end))]);
saveas(gcf, [img_path 'day8_regbot_vs_matlab.png']);

%% ========================================================================
%  SECTION 5: Step Response Metrics from REGBOT Data
%  ========================================================================

x_final = x_regbot(end);
x_ref = 0.5;

% Rise time (10% to 90% of final value)
idx_10 = find(x_regbot >= 0.1*x_ref, 1);
idx_90 = find(x_regbot >= 0.9*x_ref, 1);
if ~isempty(idx_10) && ~isempty(idx_90)
    tr = t_regbot(idx_90) - t_regbot(idx_10);
else
    tr = NaN;
end

% Overshoot
Mp = (max(x_regbot) - x_ref) / x_ref * 100;

% Settling (2%)
settled = abs(x_regbot - x_ref) <= 0.02*x_ref;
ts = NaN;
for k = length(settled):-1:1
    if ~settled(k)
        ts = t_regbot(min(k+1, length(t_regbot)));
        break;
    end
end

fprintf('\n=== REGBOT Experimental Results ===\n');
fprintf('Final position: %.4f m (ref: %.1f m)\n', x_final, x_ref);
fprintf('Steady-state error: %.4f m\n', abs(x_ref - x_final));
fprintf('Rise time (10-90%%): %.4f s\n', tr);
fprintf('Overshoot: %.2f %%\n', Mp);
fprintf('Settling time (2%%): %.4f s\n', ts);
