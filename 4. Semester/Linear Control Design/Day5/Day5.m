%% Day 5 - Black Box Modeling for REGBOT
%  34722 Linear Control Design 1 — Exercise 5 Companion
%  Topics: System identification using tfest, compare wheels-up vs
%          on-the-floor transfer functions (voltage -> velocity).
clear all; clc; close all;

% Plot settings
set(0, 'DefaultTextInterpreter', 'none');
set(0, 'DefaultAxesFontSize', 14);
set(0, 'DefaultLineLineWidth', 1.5);

% Image export path
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

%% ========================================================================
%  SECTION 1: Load Log Data (Wheels Up)
%  ========================================================================

log_file_up = 'log_wheels_up.txt';

opts = detectImportOptions(log_file_up, 'FileType', 'text');
opts.CommentStyle = '%';
data = readtable(log_file_up, opts);
data = fillmissing(data, 'nearest');

t   = table2array(data(:,1));          % time stamps [s]
u_L = table2array(data(:,8));          % left motor voltage [V]
u_R = table2array(data(:,9));          % right motor voltage [V]
v_L = table2array(data(:,10));         % left motor velocity [m/s]
v_R = table2array(data(:,11));         % right motor velocity [m/s]
T_s = t(2) - t(1);

fprintf('Loaded %d samples from "%s", Ts = %.1f ms\n\n', ...
    length(t), log_file_up, T_s*1000);

%% ========================================================================
%  SECTION 2: Plot Raw Data
%  ========================================================================

fig1 = figure('Name', 'Raw Log Data (Wheels Up)', 'Position', [100 100 900 600]);

subplot(2, 1, 1);
plot(t, u_L, 'b', t, u_R, 'r');
xlabel('Time [s]'); ylabel('Voltage [V]');
title('Motor Voltage — Raw (Wheels Up)');
legend('Left', 'Right', 'Location', 'best');
grid on;

subplot(2, 1, 2);
plot(t, v_L, 'b', t, v_R, 'r');
xlabel('Time [s]'); ylabel('Velocity [m/s]');
title('Motor Velocity — Raw (Wheels Up)');
legend('Left', 'Right', 'Location', 'best');
grid on;

exportgraphics(fig1, [img_path 'day5_raw_data_up.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 3: Trim Data to the Step Region
%  The data contains three phases:
%    1) 0->3V startup transient (velocity ramps up from 0)
%    2) 3V->4V step (the step we want to identify)
%    3) Motor shutdown (voltage drops to 0, velocity coasts)
%  We need to isolate ONLY the 3V->4V step region.
%
%  Strategy:
%    - Find where voltage crosses the midpoint (3.5V) = step moment
%    - Include N samples BEFORE the step (steady state at 3V)
%    - Find where voltage drops below 3V again = end of useful data
%  ========================================================================

V_before = 3;                              % voltage before the step
V_after  = 4;                              % voltage after the step
V_mid    = (V_before + V_after) / 2;       % midpoint to detect the step

u_avg_raw = (u_L + u_R) / 2;

% Find the step moment: where voltage first crosses the midpoint
idx_step = find(u_avg_raw >= V_mid, 1, 'first');
if isempty(idx_step)
    error('Could not find voltage step. Check your data.');
end

% Include N_pre samples BEFORE the step for steady-state baseline
N_pre = min(50, idx_step - 1);            % ~50 samples before step
idx_start = idx_step - N_pre;

% Find end of useful data: where voltage drops back below V_mid
% (motor shutdown or mission end)
idx_end_candidates = find(u_avg_raw(idx_step:end) < V_mid, 1, 'first');
if ~isempty(idx_end_candidates)
    idx_end = idx_step + idx_end_candidates - 2;  % one sample before drop
else
    idx_end = length(t);                           % use all data after step
end

fprintf('Step detected at t = %.4f s (sample %d)\n', t(idx_step), idx_step);
fprintf('Using data from sample %d to %d (%d samples)\n', ...
    idx_start, idx_end, idx_end - idx_start + 1);

% Trim all signals
t   = t(idx_start:idx_end);
u_L = u_L(idx_start:idx_end);
u_R = u_R(idx_start:idx_end);
v_L = v_L(idx_start:idx_end);
v_R = v_R(idx_start:idx_end);

% Offset time so t=0 is at the step moment
t = t - t(N_pre + 1);

fprintf('Time range: [%.4f, %.4f] s (step at t=0)\n\n', t(1), t(end));

%% ========================================================================
%  SECTION 4: Remove Offsets
%  Subtract the pre-step baseline so all signals start from 0.
%  ========================================================================

u_L_offset = mean(u_L(1:N_pre));
u_R_offset = mean(u_R(1:N_pre));
v_L_offset = mean(v_L(1:N_pre));
v_R_offset = mean(v_R(1:N_pre));

u_L = u_L - u_L_offset;
u_R = u_R - u_R_offset;
v_L = v_L - v_L_offset;
v_R = v_R - v_R_offset;

fprintf('Offsets removed (pre-step baseline averages):\n');
fprintf('  u_L offset = %.3f V,  u_R offset = %.3f V\n', u_L_offset, u_R_offset);
fprintf('  v_L offset = %.3f m/s, v_R offset = %.3f m/s\n\n', v_L_offset, v_R_offset);

%% ========================================================================
%  SECTION 5: Remove Outliers
%  ========================================================================

v_L = medfilt1(v_L, 5);
v_R = medfilt1(v_R, 5);

%% ========================================================================
%  SECTION 6: Plot Trimmed and Offset-Removed Data
%  ========================================================================

fig2 = figure('Name', 'Trimmed Data (Wheels Up)', 'Position', [100 100 900 600]);

subplot(2, 1, 1);
plot(t, u_L, 'b', t, u_R, 'r');
xlabel('Time [s]'); ylabel('\Delta Voltage [V]');
title('Motor Voltage — Trimmed & Offset Removed (Wheels Up)');
legend('Left', 'Right', 'Location', 'best');
xline(0, 'k--', 'Step');
grid on;

subplot(2, 1, 2);
plot(t, v_L, 'b', t, v_R, 'r');
xlabel('Time [s]'); ylabel('\Delta Velocity [m/s]');
title('Motor Velocity — Trimmed & Offset Removed (Wheels Up)');
legend('Left', 'Right', 'Location', 'best');
xline(0, 'k--', 'Step');
grid on;

exportgraphics(fig2, [img_path 'day5_trimmed_up.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 7: Compute Averages and Prepare Identification Data
%  ========================================================================

vel  = 1/2 * (v_L + v_R);               % average wheel velocity
volt = 1/2 * (u_L + u_R);               % average voltage

idd_L   = iddata(v_L, u_L, T_s);        % left wheel
idd_R   = iddata(v_R, u_R, T_s);        % right wheel
idd_avg = iddata(vel, volt, T_s);        % average

%% ========================================================================
%  SECTION 8: Identify Transfer Functions using tfest
%  ========================================================================

np = 2;                                   % number of poles
nz = 0;                                   % number of zeros

G_wu_L   = tfest(idd_L,   np, nz);       % left wheel TF
G_wu_R   = tfest(idd_R,   np, nz);       % right wheel TF
G_wu_avg = tfest(idd_avg, np, nz);       % average TF

fprintf('=== Identified Transfer Functions (Wheels Up) ===\n\n');
fprintf('--- Left Wheel ---\n');
G_wu_L
fprintf('--- Right Wheel ---\n');
G_wu_R
fprintf('--- Average ---\n');
G_wu_avg

%% ========================================================================
%  SECTION 9: Compare Model vs Measured — step command
%  Use only data from the step onward (t >= 0).
%  ========================================================================

idx_t0 = find(t >= 0, 1, 'first');

v_L_step = v_L(idx_t0:end) - v_L(idx_t0);
v_R_step = v_R(idx_t0:end) - v_R(idx_t0);
vel_step = vel(idx_t0:end) - vel(idx_t0);
t_step   = t(idx_t0:end) - t(idx_t0);

% --- Left Wheel ---
fig3 = figure('Name', 'Model vs Measured — Left (Wheels Up)', ...
    'Position', [100 100 800 500]);
[y_L, t_L] = step(G_wu_L, t_step(end));
plot(t_L, y_L, 'r--', 'LineWidth', 2); hold on;
plot(t_step, v_L_step, 'b');
hold off;
legend('Estimated (tfest)', 'Measured', 'Location', 'best');
xlabel('Time [s]'); ylabel('\Delta Velocity [m/s]');
title('Left Wheel — Model vs Measured (Wheels Up)');
grid on;

exportgraphics(fig3, [img_path 'day5_model_vs_meas_L_up.png'], 'Resolution', 200);

% --- Right Wheel ---
fig4 = figure('Name', 'Model vs Measured — Right (Wheels Up)', ...
    'Position', [100 100 800 500]);
[y_R, t_R] = step(G_wu_R, t_step(end));
plot(t_R, y_R, 'r--', 'LineWidth', 2); hold on;
plot(t_step, v_R_step, 'b');
hold off;
legend('Estimated (tfest)', 'Measured', 'Location', 'best');
xlabel('Time [s]'); ylabel('\Delta Velocity [m/s]');
title('Right Wheel — Model vs Measured (Wheels Up)');
grid on;

exportgraphics(fig4, [img_path 'day5_model_vs_meas_R_up.png'], 'Resolution', 200);

% --- Average ---
fig5 = figure('Name', 'Model vs Measured — Average (Wheels Up)', ...
    'Position', [100 100 800 500]);
[y_avg, t_avg] = step(G_wu_avg, t_step(end));
plot(t_avg, y_avg, 'r--', 'LineWidth', 2); hold on;
plot(t_step, vel_step, 'b');
hold off;
legend('Estimated (tfest)', 'Measured', 'Location', 'best');
xlabel('Time [s]'); ylabel('\Delta Velocity [m/s]');
title('Average — Model vs Measured (Wheels Up)');
grid on;

exportgraphics(fig5, [img_path 'day5_model_vs_meas_avg_up.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 10: Compare using the compare command
%  ========================================================================

fig6 = figure('Name', 'compare() — Wheels Up', 'Position', [100 100 900 700]);

subplot(3, 1, 1);
compare(idd_L, G_wu_L);
title('Left Wheel — compare()');
grid on;

subplot(3, 1, 2);
compare(idd_R, G_wu_R);
title('Right Wheel — compare()');
grid on;

subplot(3, 1, 3);
compare(idd_avg, G_wu_avg);
title('Average — compare()');
grid on;

exportgraphics(fig6, [img_path 'day5_compare_up.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 11: Transfer Function Analysis (Bode, Step, Poles)
%  ========================================================================

fig7 = figure('Name', 'TF Analysis — Wheels Up', 'Position', [100 100 900 700]);

subplot(2, 2, 1);
step(G_wu_L, G_wu_R, G_wu_avg);
legend('Left', 'Right', 'Average', 'Location', 'best');
title('Step Response (Wheels Up)');
grid on;

subplot(2, 2, 2);
impulse(G_wu_L, G_wu_R, G_wu_avg);
legend('Left', 'Right', 'Average', 'Location', 'best');
title('Impulse Response (Wheels Up)');
grid on;

subplot(2, 2, [3, 4]);
bode(G_wu_L, G_wu_R, G_wu_avg);
legend('Left', 'Right', 'Average', 'Location', 'best');
title('Bode Plot (Wheels Up)');
grid on;

exportgraphics(fig7, [img_path 'day5_tf_analysis_up.png'], 'Resolution', 200);

fprintf('=== Wheels-Up Analysis Complete ===\n');
fprintf('Poles (avg):  '); disp(pole(G_wu_avg)');
fprintf('DC gain (avg): %.4f (m/s)/V\n', dcgain(G_wu_avg));
fprintf('Fit %%:         see compare() plots\n\n');

%% ========================================================================
%  ========================================================================
%  SECTION 12: ON THE FLOOR — Repeat the identification
%  ========================================================================
%  ========================================================================

fprintf('========================================\n');
fprintf('  ON THE FLOOR IDENTIFICATION\n');
fprintf('========================================\n\n');

log_file_floor = 'log_on_floor.txt';

if ~isfile(log_file_floor)
    fprintf('Log file "%s" not found.\n', log_file_floor);
    fprintf('Place your on-the-floor log file here and re-run from this section.\n');
    fprintf('Skipping floor identification.\n\n');
    has_floor = false;
else
    has_floor = true;
end

if has_floor
    opts_f = detectImportOptions(log_file_floor, 'FileType', 'text');
    opts_f.CommentStyle = '%';
    data_f = readtable(log_file_floor, opts_f);
    data_f = fillmissing(data_f, 'nearest');

    t_f   = table2array(data_f(:,1));
    uL_f  = table2array(data_f(:,8));
    uR_f  = table2array(data_f(:,9));
    vL_f  = table2array(data_f(:,10));
    vR_f  = table2array(data_f(:,11));
    Ts_f  = t_f(2) - t_f(1);

    fprintf('Loaded %d samples from "%s", Ts = %.1f ms\n\n', ...
        length(t_f), log_file_floor, Ts_f*1000);

    %% Plot raw floor data
    fig_f1 = figure('Name', 'Raw Log Data (Floor)', 'Position', [100 100 900 600]);

    subplot(2, 1, 1);
    plot(t_f, uL_f, 'b', t_f, uR_f, 'r');
    xlabel('Time [s]'); ylabel('Voltage [V]');
    title('Motor Voltage — Raw (On Floor)');
    legend('Left', 'Right', 'Location', 'best');
    grid on;

    subplot(2, 1, 2);
    plot(t_f, vL_f, 'b', t_f, vR_f, 'r');
    xlabel('Time [s]'); ylabel('Velocity [m/s]');
    title('Motor Velocity — Raw (On Floor)');
    legend('Left', 'Right', 'Location', 'best');
    grid on;

    exportgraphics(fig_f1, [img_path 'day5_raw_data_floor.png'], 'Resolution', 200);

    %% Trim — find the step, include pre-step baseline, cut before bad data
    u_avg_f = (uL_f + uR_f) / 2;
    v_avg_f_raw = (vL_f + vR_f) / 2;

    idx_step_f = find(u_avg_f >= V_mid, 1, 'first');
    if isempty(idx_step_f)
        error('Could not find voltage step in floor data.');
    end

    N_pre_f = min(50, idx_step_f - 1);
    idx_start_f = idx_step_f - N_pre_f;

    % End detection: use THREE criteria (whichever comes first)
    %  1) Voltage drops below midpoint (motor shutdown)
    %  2) Maximum time window after step (default 4s — adjust if needed)
    %  3) Velocity drops significantly (robot hit something)
    max_floor_duration = 4;  % seconds of useful data after step

    % Criterion 1: voltage drop
    idx_vdrop = find(u_avg_f(idx_step_f:end) < V_mid, 1, 'first');
    if ~isempty(idx_vdrop)
        idx_end_v = idx_step_f + idx_vdrop - 2;
    else
        idx_end_v = length(t_f);
    end

    % Criterion 2: max time window
    idx_end_t = find(t_f >= t_f(idx_step_f) + max_floor_duration, 1, 'first');
    if isempty(idx_end_t); idx_end_t = length(t_f); end

    % Criterion 3: velocity collapse (drops below 50% of its peak)
    v_after = v_avg_f_raw(idx_step_f:end);
    v_peak = max(medfilt1(v_after, 21));  % smoothed peak
    idx_collapse = find(medfilt1(v_after, 21) < 0.5 * v_peak, 1, 'first');
    if ~isempty(idx_collapse) && idx_collapse > 50  % ignore first 50 samples
        idx_end_c = idx_step_f + idx_collapse - 2;
    else
        idx_end_c = length(t_f);
    end

    idx_end_f = min([idx_end_v, idx_end_t, idx_end_c]);

    fprintf('Floor trim: step at sample %d, end at %d\n', idx_step_f, idx_end_f);
    fprintf('  (voltage drop: %d, max time: %d, vel collapse: %d)\n', ...
        idx_end_v, idx_end_t, idx_end_c);

    t_f  = t_f(idx_start_f:idx_end_f);
    uL_f = uL_f(idx_start_f:idx_end_f);
    uR_f = uR_f(idx_start_f:idx_end_f);
    vL_f = vL_f(idx_start_f:idx_end_f);
    vR_f = vR_f(idx_start_f:idx_end_f);
    t_f  = t_f - t_f(N_pre_f + 1);

    %% Remove offsets (pre-step baseline)
    uL_f_off = mean(uL_f(1:N_pre_f));
    uR_f_off = mean(uR_f(1:N_pre_f));
    vL_f_off = mean(vL_f(1:N_pre_f));
    vR_f_off = mean(vR_f(1:N_pre_f));

    uL_f = uL_f - uL_f_off;
    uR_f = uR_f - uR_f_off;
    vL_f = vL_f - vL_f_off;
    vR_f = vR_f - vR_f_off;

    %% Outlier removal
    vL_f = medfilt1(vL_f, 5);
    vR_f = medfilt1(vR_f, 5);

    %% Averages
    vel_f  = 1/2 * (vL_f + vR_f);
    volt_f = 1/2 * (uL_f + uR_f);

    %% Prepare iddata
    idd_L_f   = iddata(vL_f, uL_f, Ts_f);
    idd_R_f   = iddata(vR_f, uR_f, Ts_f);
    idd_avg_f = iddata(vel_f, volt_f, Ts_f);

    %% Identify transfer functions (floor)
    G_floor_L   = tfest(idd_L_f,   np, nz);
    G_floor_R   = tfest(idd_R_f,   np, nz);
    G_floor_avg = tfest(idd_avg_f, np, nz);

    fprintf('=== Identified Transfer Functions (On Floor) ===\n\n');
    fprintf('--- Left Wheel ---\n');
    G_floor_L
    fprintf('--- Right Wheel ---\n');
    G_floor_R
    fprintf('--- Average ---\n');
    G_floor_avg

    %% Compare — floor
    fig8 = figure('Name', 'compare() — On Floor', 'Position', [100 100 900 700]);

    subplot(3, 1, 1);
    compare(idd_L_f, G_floor_L);
    title('Left Wheel — compare() (On Floor)');
    grid on;

    subplot(3, 1, 2);
    compare(idd_R_f, G_floor_R);
    title('Right Wheel — compare() (On Floor)');
    grid on;

    subplot(3, 1, 3);
    compare(idd_avg_f, G_floor_avg);
    title('Average — compare() (On Floor)');
    grid on;

    exportgraphics(fig8, [img_path 'day5_compare_floor.png'], 'Resolution', 200);

    %% Step comparison — floor average
    idx_t0_f = find(t_f >= 0, 1, 'first');

    vel_step_f = vel_f(idx_t0_f:end) - vel_f(idx_t0_f);
    t_step_f   = t_f(idx_t0_f:end) - t_f(idx_t0_f);

    fig9 = figure('Name', 'Model vs Measured — Average (Floor)', ...
        'Position', [100 100 800 500]);
    [y_f, t_yf] = step(G_floor_avg, t_step_f(end));
    plot(t_yf, y_f, 'r--', 'LineWidth', 2); hold on;
    plot(t_step_f, vel_step_f, 'b');
    hold off;
    legend('Estimated (tfest)', 'Measured', 'Location', 'best');
    xlabel('Time [s]'); ylabel('\Delta Velocity [m/s]');
    title('Average — Model vs Measured (On Floor)');
    grid on;

    exportgraphics(fig9, [img_path 'day5_model_vs_meas_floor.png'], 'Resolution', 200);

    %% TF Analysis — floor
    fig10 = figure('Name', 'TF Analysis — On Floor', 'Position', [100 100 900 700]);

    subplot(2, 2, 1);
    step(G_floor_L, G_floor_R, G_floor_avg);
    legend('Left', 'Right', 'Average', 'Location', 'best');
    title('Step Response (On Floor)');
    grid on;

    subplot(2, 2, 2);
    impulse(G_floor_L, G_floor_R, G_floor_avg);
    legend('Left', 'Right', 'Average', 'Location', 'best');
    title('Impulse Response (On Floor)');
    grid on;

    subplot(2, 2, [3, 4]);
    bode(G_floor_L, G_floor_R, G_floor_avg);
    legend('Left', 'Right', 'Average', 'Location', 'best');
    title('Bode Plot (On Floor)');
    grid on;

    exportgraphics(fig10, [img_path 'day5_tf_analysis_floor.png'], 'Resolution', 200);

    fprintf('Poles (floor avg):  '); disp(pole(G_floor_avg)');
    fprintf('DC gain (floor avg): %.4f (m/s)/V\n\n', dcgain(G_floor_avg));
end

%% ========================================================================
%  SECTION 13: Side-by-Side Comparison — Wheels Up vs Floor
%  ========================================================================

if has_floor
    fig11 = figure('Name', 'Wheels Up vs Floor', 'Position', [100 100 900 500]);

    subplot(1, 2, 1);
    step(G_wu_avg, G_floor_avg);
    legend('Wheels Up', 'On Floor', 'Location', 'best');
    title('Step Response Comparison');
    grid on;

    subplot(1, 2, 2);
    bode(G_wu_avg, G_floor_avg);
    legend('Wheels Up', 'On Floor', 'Location', 'best');
    title('Bode Plot Comparison');
    grid on;

    exportgraphics(fig11, [img_path 'day5_up_vs_floor.png'], 'Resolution', 200);

    fprintf('=== Comparison: Wheels Up vs On Floor ===\n');
    fprintf('                     Wheels Up       On Floor\n');
    fprintf('DC gain (m/s)/V:     %.4f          %.4f\n', ...
        dcgain(G_wu_avg), dcgain(G_floor_avg));
    fprintf('Poles (wheels up):   '); disp(pole(G_wu_avg)');
    fprintf('Poles (on floor):    '); disp(pole(G_floor_avg)');
end

fprintf('\n=== All sections complete ===\n');
