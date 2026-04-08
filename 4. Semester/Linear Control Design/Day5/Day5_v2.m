%% Day 5 v2 — Re-identification with training wheels
%  Compare new floor TF with old one, try 1-pole and 2-pole models.
clear all; clc; close all;

img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

set(0, 'DefaultTextInterpreter', 'none');
set(0, 'DefaultAxesFontSize', 14);
set(0, 'DefaultLineLineWidth', 1.5);

%% Load new log
log_file = 'log_on_floor_v2.txt';
opts = detectImportOptions(log_file, 'FileType', 'text');
opts.CommentStyle = '%';
data = readtable(log_file, opts);
data = fillmissing(data, 'nearest');

t   = table2array(data(:,1));
u_L = table2array(data(:,8));
u_R = table2array(data(:,9));
v_L = table2array(data(:,10));
v_R = table2array(data(:,11));
T_s = t(2) - t(1);

fprintf('Loaded %d samples from "%s", Ts = %.1f ms\n\n', length(t), log_file, T_s*1000);

%% Plot raw data
figure(1); clf;
subplot(2,1,1);
plot(t, u_L, 'b', t, u_R, 'r');
xlabel('Time [s]'); ylabel('Voltage [V]');
title('Motor Voltage - Raw (Floor v2, training wheels)');
legend('Left', 'Right'); grid on;

subplot(2,1,2);
plot(t, v_L, 'b', t, v_R, 'r');
xlabel('Time [s]'); ylabel('Velocity [m/s]');
title('Motor Velocity - Raw');
legend('Left', 'Right'); grid on;

%% Trim to step region
V_mid = 3.5;
u_avg_raw = (u_L + u_R) / 2;
idx_step = find(u_avg_raw >= V_mid, 1, 'first');
N_pre = min(50, idx_step - 1);
idx_start = idx_step - N_pre;

% End detection
max_duration = 6;
idx_end_v = find(u_avg_raw(idx_step:end) < V_mid, 1, 'first');
if ~isempty(idx_end_v); idx_end_v = idx_step + idx_end_v - 2; else; idx_end_v = length(t); end
idx_end_t = find(t >= t(idx_step) + max_duration, 1, 'first');
if isempty(idx_end_t); idx_end_t = length(t); end

v_avg_raw = (v_L + v_R) / 2;
v_after = v_avg_raw(idx_step:end);
v_peak = max(medfilt1(v_after, 21));
idx_collapse = find(medfilt1(v_after, 21) < 0.5 * v_peak, 1, 'first');
if ~isempty(idx_collapse) && idx_collapse > 50
    idx_end_c = idx_step + idx_collapse - 2;
else
    idx_end_c = length(t);
end

idx_end = min([idx_end_v, idx_end_t, idx_end_c]);

fprintf('Step at sample %d (t=%.3fs), end at %d\n', idx_step, t(idx_step), idx_end);

t   = t(idx_start:idx_end);
u_L = u_L(idx_start:idx_end);
u_R = u_R(idx_start:idx_end);
v_L = v_L(idx_start:idx_end);
v_R = v_R(idx_start:idx_end);
t   = t - t(N_pre + 1);

%% Remove offsets
u_L = u_L - mean(u_L(1:N_pre));
u_R = u_R - mean(u_R(1:N_pre));
v_L = v_L - mean(v_L(1:N_pre));
v_R = v_R - mean(v_R(1:N_pre));

%% Outlier removal
v_L = medfilt1(v_L, 5);
v_R = medfilt1(v_R, 5);

%% Averages and iddata
vel  = (v_L + v_R) / 2;
volt = (u_L + u_R) / 2;

idd_L   = iddata(v_L, u_L, T_s);
idd_R   = iddata(v_R, u_R, T_s);
idd_avg = iddata(vel, volt, T_s);

%% Identify: 2 poles (same as before)
G_2p_L   = tfest(idd_L,   2, 0);
G_2p_R   = tfest(idd_R,   2, 0);
G_2p_avg = tfest(idd_avg, 2, 0);

%% Identify: 1 pole
G_1p_L   = tfest(idd_L,   1, 0);
G_1p_R   = tfest(idd_R,   1, 0);
G_1p_avg = tfest(idd_avg, 1, 0);

%% Print results
fprintf('\n=== 2-pole model (average) ===\n');
G_2p_avg
fprintf('Poles: '); disp(pole(G_2p_avg)');
fprintf('DC gain: %.4f\n', dcgain(G_2p_avg));

fprintf('\n=== 1-pole model (average) ===\n');
G_1p_avg
fprintf('Poles: '); disp(pole(G_1p_avg)');
fprintf('DC gain: %.4f\n', dcgain(G_1p_avg));

%% Compare fits
figure(2); clf;
subplot(2,1,1);
compare(idd_avg, G_2p_avg, G_1p_avg);
title('Average - compare() (Floor v2)');
legend('Measured', '2-pole', '1-pole'); grid on;

subplot(2,1,2);
compare(idd_L, G_2p_L, G_1p_L);
title('Left - compare()');
legend('Measured', '2-pole', '1-pole'); grid on;

exportgraphics(gcf, [img_path 'day5_v2_compare.png'], 'Resolution', 200);

%% Step response overlay
idx_t0 = find(t >= 0, 1);
vel_step = vel(idx_t0:end) - vel(idx_t0);
t_step = t(idx_t0:end) - t(idx_t0);

[y_2p, t_2p] = step(G_2p_avg, t_step(end));
[y_1p, t_1p] = step(G_1p_avg, t_step(end));

figure(3); clf;
plot(t_step, vel_step, 'b'); hold on;
plot(t_2p, y_2p, 'r--', 'LineWidth', 2);
plot(t_1p, y_1p, 'g-.', 'LineWidth', 2);
hold off;
legend('Measured', '2-pole', '1-pole');
xlabel('Time [s]'); ylabel('\Delta Velocity [m/s]');
title('Model vs Measured (Floor v2, training wheels)');
grid on;
exportgraphics(gcf, [img_path 'day5_v2_model_vs_meas.png'], 'Resolution', 200);

%% Compare with old identification
load('Day5_results.mat', 'G_floor_avg');
G_old = G_floor_avg;

fprintf('\n=== Comparison: Old vs New ===\n');
fprintf('                  Old (no support)    New (training wheels)\n');
fprintf('DC gain:          %.4f               %.4f\n', dcgain(G_old), dcgain(G_2p_avg));
fprintf('Old poles:  '); disp(pole(G_old)');
fprintf('New poles:  '); disp(pole(G_2p_avg)');

figure(4); clf;
subplot(1,2,1);
step(G_old, G_2p_avg, G_1p_avg);
legend('Old (no support)', 'New 2-pole', 'New 1-pole');
title('Step Response Comparison'); grid on;

subplot(1,2,2);
bode(G_old, G_2p_avg, G_1p_avg);
legend('Old (no support)', 'New 2-pole', 'New 1-pole');
title('Bode Comparison'); grid on;

exportgraphics(gcf, [img_path 'day5_v2_old_vs_new.png'], 'Resolution', 200);

%% Save new results
G_floor_avg_v2_2p = G_2p_avg;
G_floor_avg_v2_1p = G_1p_avg;
save('Day5_results_v2.mat', 'G_2p_L', 'G_2p_R', 'G_2p_avg', ...
    'G_1p_L', 'G_1p_R', 'G_1p_avg', 'T_s', ...
    'G_floor_avg_v2_2p', 'G_floor_avg_v2_1p');
fprintf('\nSaved to Day5_results_v2.mat\n');
