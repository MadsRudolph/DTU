%% REGBOT Position Controller — Plot Experimental Results
%  Day 8 — 34722 Linear Control Design 1
%
%  Usage:
%    log_file = '../logs/log_position.txt'; regbot_plot_results
%    log_file = '../logs/log_position_half_kp.txt'; regbot_plot_results
%
%  If log_file is not set, defaults to '../logs/log_position.txt'.

if ~exist('log_file', 'var')
    log_file = '../logs/log_position.txt';
end
clc; close all;

img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

%% ========================================================================
%  SECTION 1: Load REGBOT Log
%  ========================================================================

fprintf('Loading: %s\n', log_file);
opts = detectImportOptions(log_file, 'FileType', 'text');
opts.CommentStyle = '%';
data = readtable(log_file, opts);
data = fillmissing(data, 'nearest');

t    = table2array(data(:,1));     % time [s]
u_L  = table2array(data(:,8));     % left motor voltage [V]
u_R  = table2array(data(:,9));     % right motor voltage [V]
v_L  = table2array(data(:,10));    % left wheel velocity [m/s]
v_R  = table2array(data(:,11));    % right wheel velocity [m/s]
x    = table2array(data(:,14));    % pose x (driven distance) [m]

T_s = t(2) - t(1);
x = x - x(1);

fprintf('Loaded %d samples, Ts = %.1f ms\n', length(t), T_s*1000);

%% ========================================================================
%  SECTION 2: Plot REGBOT Results
%  ========================================================================

[~, log_name, ~] = fileparts(log_file);

figure(1); clf;
aa = subplot(3,1,1);
plot(t, x);
hold on;
plot(t, 0.5*ones(size(t)), '--k');
hold off;
grid on;
ylabel('$x, x_{ref}$ in m');
legend({'$x$', '$x_{ref} = 0.5$ m'}, 'interpreter', 'latex');
title(sprintf('REGBOT: %s', strrep(log_name, '_', '\_')));

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
saveas(gcf, [img_path 'day8_' log_name '.png']);

%% ========================================================================
%  SECTION 3: Step Response Metrics
%  ========================================================================

u_avg = (u_L + u_R) / 2;
idx_step = find(abs(u_avg) > 1, 1, 'first');
t_r = t(idx_step:end) - t(idx_step);
x_r = x(idx_step:end) - x(idx_step);
x_ref = 0.5;
x_final = x_r(end);

% Rise time (10% to 90%)
idx_10 = find(x_r >= 0.1*x_ref, 1);
idx_90 = find(x_r >= 0.9*x_ref, 1);
if ~isempty(idx_10) && ~isempty(idx_90)
    tr = t_r(idx_90) - t_r(idx_10);
else
    tr = NaN;
end

% Overshoot
Mp = (max(x_r) - x_ref) / x_ref * 100;

% Settling (2%)
settled = abs(x_r - x_ref) <= 0.02*x_ref;
ts = NaN;
for k = length(settled):-1:1
    if ~settled(k); ts = t_r(min(k+1, length(t_r))); break; end
end
if all(settled); ts = t_r(1); end

fprintf('\n=== Results: %s ===\n', log_name);
fprintf('Final position: %.4f m\n', x_final);
fprintf('Steady-state error: %.4f m\n', abs(x_ref - x_final));
fprintf('Rise time (10-90%%): %.4f s\n', tr);
fprintf('Overshoot: %.2f %%\n', Mp);
fprintf('Settling time (2%%): %.4f s\n', ts);

%% ========================================================================
%  SECTION 4: Compare with linear model (optional)
%  ========================================================================

if exist('../../Day5/Day5_results.mat', 'file')
    load('../../Day5/Day5_results.mat');
    s = tf('s');
    G_pos = minreal(G_floor_avg * (1/s));

    % Use conservative design (N_i=3, alpha=0.3)
    N_i = 3;  alpha = 0.3;  gamma_M = 60;
    w = logspace(-1, 5, 5000);
    [~, P_bode, w_out] = bode(G_pos, w);
    P_bode = squeeze(P_bode);

    phi_i = rad2deg(-atan(1/N_i));
    phi_m = rad2deg(asin((1-alpha)/(1+alpha)));
    phi_G_req = -180 + gamma_M - phi_i - phi_m;
    i_c = find(P_bode <= phi_G_req, 1);
    omega_c = w_out(i_c);

    tau_i = N_i/omega_c;
    tau_d = 1/(omega_c*sqrt(alpha));
    C_PI = (1 + 1/(tau_i*s));
    C_D = (tau_d*s+1)/(alpha*tau_d*s+1);
    G_ol_noK = minreal(C_PI*C_D*G_pos);
    K_P = 1/abs(freqresp(G_ol_noK, omega_c));

    G_cl_fb = minreal(K_P*C_PI*G_pos / (1 + K_P*C_PI*C_D*G_pos));
    [y_lin, t_lin] = step(G_cl_fb, 0:0.001:5);

    figure(2); clf;
    plot(t_r, x_r, 'b', 'LineWidth', 2);
    hold on;
    plot(t_lin, 0.5*y_lin, 'r--', 'LineWidth', 1.5);
    plot(t_lin, 0.5*ones(size(t_lin)), '--k');
    hold off;
    grid on;
    xlabel('$t$ in s');
    ylabel('Position [m]');
    title('REGBOT vs MATLAB (linear model)');
    legend({'REGBOT', 'MATLAB (linear)', 'Reference'}, ...
        'interpreter', 'latex', 'Location', 'southeast');
    xlim([0 min(5, t_r(end))]);
    saveas(gcf, [img_path 'day8_' log_name '_vs_matlab.png']);
end
