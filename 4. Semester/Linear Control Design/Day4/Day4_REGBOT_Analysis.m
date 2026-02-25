%% Day 4 - REGBOT Introduction: Data Logging & Analysis
%  34722 Linear Control Design 1 — Exercise 4 Companion
%  Topics: Load REGBOT log data, trim step response, plot motor performance,
%          estimate transfer function parameters (Kss, omega_b, tau).
clear all; clc; close all;

% Plot settings
set(0, 'DefaultTextInterpreter', 'none');
set(0, 'DefaultAxesFontSize', 14);
set(0, 'DefaultLineLineWidth', 1.5);

% Image export path
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

%% ========================================================================
%  SECTION 1: Load Log Data
%  Place your .txt log file in this folder and update the filename below.
%  ========================================================================

% --- UPDATE THIS FILENAME ---
log_file = 'log_velocity.txt';

if ~isfile(log_file)
    fprintf('Log file "%s" not found.\n', log_file);
    fprintf('Place your REGBOT log file in:\n  %s\n', pwd);
    fprintf('Then update the log_file variable and re-run.\n\n');
    fprintf('--- Running with DEMO DATA instead ---\n\n');
    use_demo = true;
else
    use_demo = false;
end

%% ========================================================================
%  SECTION 2: Parse Data
%  ========================================================================

if use_demo
    % Generate synthetic demo data resembling a 3V -> 4V step
    T_s = 0.004;                          % 4 ms sampling
    t_demo = (0:T_s:3)';
    N = length(t_demo);

    % Step occurs at t = 1 s
    step_idx = find(t_demo >= 1, 1, 'first');

    % Simulated motor voltage
    u_demo = 3 * ones(N, 1);
    u_demo(step_idx:end) = 4;

    % Simulated velocity: 1st order response to voltage
    % G(s) = Kss * wb / (s + wb), Kss ~ 0.5 m/s per V, wb ~ 5 rad/s
    Kss_true = 0.5;
    wb_true  = 5;
    tau_true = 1 / wb_true;

    v_base = Kss_true * 3 * (1 - exp(-wb_true * t_demo));
    v_step = zeros(N, 1);
    t_after = t_demo(step_idx:end) - t_demo(step_idx);
    v_step(step_idx:end) = Kss_true * 1 * (1 - exp(-wb_true * t_after));

    v_demo = v_base + v_step;
    % Add small noise
    rng(42);
    v_demo = v_demo + 0.005 * randn(N, 1);

    t   = t_demo;
    u_L = u_demo;
    u_R = u_demo;
    v_L = v_demo;
    v_R = v_demo + 0.003 * randn(N, 1);   % slight asymmetry

    fprintf('Demo data generated: %d samples, Ts = %.0f ms\n', N, T_s*1000);
    fprintf('True parameters: Kss = %.2f, wb = %.1f rad/s, tau = %.2f s\n\n', ...
        Kss_true, wb_true, tau_true);
else
    data = readtable(log_file);
    data = fillmissing(data, 'nearest');

    t   = table2array(data(:,1));          % time stamps [s]
    u_L = table2array(data(:,8));          % left motor voltage [V]
    u_R = table2array(data(:,9));          % right motor voltage [V]
    v_L = table2array(data(:,10));         % left motor velocity [m/s]
    v_R = table2array(data(:,11));         % right motor velocity [m/s]
    T_s = t(2) - t(1);

    fprintf('Loaded %d samples from "%s", Ts = %.1f ms\n\n', length(t), log_file, T_s*1000);
end

%% ========================================================================
%  SECTION 3: Plot Raw Data (before trimming)
%  ========================================================================

fig1 = figure('Name', 'Raw Log Data', 'Position', [100 100 900 600]);

subplot(2, 1, 1);
plot(t, u_L, 'b', t, u_R, 'r');
xlabel('Time [s]'); ylabel('Voltage [V]');
title('Motor Voltage — Raw');
legend('Left', 'Right', 'Location', 'best');
grid on;

subplot(2, 1, 2);
plot(t, v_L, 'b', t, v_R, 'r');
xlabel('Time [s]'); ylabel('Velocity [m/s]');
title('Motor Velocity — Raw');
legend('Left', 'Right', 'Location', 'best');
grid on;

exportgraphics(fig1, [img_path 'day4_raw_data.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 4: Trim Data to Step Region
%  Strategy: first find the STABLE low-voltage region (3V), then find
%  where the step to 4V actually occurs. This avoids initial spikes.
%  Adjust the thresholds below to match your data.
%  ========================================================================

% --- ADJUST THESE THRESHOLDS ---
V_before = 3;                              % voltage before the step
V_after  = 4;                              % voltage after the step
V_tol    = 0.5;                            % tolerance for "stable" region

% Use the average of left and right voltage to be robust against asymmetry
u_avg = (u_L + u_R) / 2;

% Step 1: Find the stable low-voltage region (where voltage is near V_before)
idx_stable = find(abs(u_avg - V_before) < V_tol, 1, 'first');
if isempty(idx_stable); idx_stable = 1; end

% Step 2: From that stable region, find where voltage first rises to V_after
idx_step = find(u_avg(idx_stable:end) >= V_after - V_tol, 1, 'first');
idx_step = idx_stable + idx_step - 1;

if isempty(idx_step)
    warning('Could not find voltage step from %.0fV to %.0fV. Using full dataset.', V_before, V_after);
    idx_step = 1;
end

% Step 3: Include a small window BEFORE the step to capture v_0
n_before = min(20, idx_step - 1);          % ~20 samples before the step
idx_start = idx_step - n_before;

% Trim
t_trim   = t(idx_start:end);
u_L_trim = u_L(idx_start:end);
u_R_trim = u_R(idx_start:end);
v_L_trim = v_L(idx_start:end);
v_R_trim = v_R(idx_start:end);

% Offset time so t=0 is at the step
t_trim = t_trim - t_trim(n_before + 1);

fprintf('Step detected at original t = %.3f s\n', t(idx_step));
fprintf('Trimmed to %d samples (%.0f before step, rest after)\n\n', ...
    length(t_trim), n_before);

%% ========================================================================
%  SECTION 5: Remove Outliers (optional)
%  Spikes in the data can be removed by median filtering.
%  ========================================================================

% Simple median filter (window = 5 samples)
v_L_clean = medfilt1(v_L_trim, 5);
v_R_clean = medfilt1(v_R_trim, 5);

% Check how many points changed significantly
n_outliers_L = sum(abs(v_L_trim - v_L_clean) > 3 * std(v_L_clean));
n_outliers_R = sum(abs(v_R_trim - v_R_clean) > 3 * std(v_R_clean));

fprintf('Outliers removed: %d (left), %d (right)\n\n', n_outliers_L, n_outliers_R);

%% ========================================================================
%  SECTION 6: Plot Trimmed Step Response
%  ========================================================================

fig2 = figure('Name', 'Trimmed Step Response', 'Position', [100 100 900 600]);

subplot(2, 1, 1);
plot(t_trim, u_L_trim, 'b', t_trim, u_R_trim, 'r');
xlabel('Time [s]'); ylabel('Voltage [V]');
title('Motor Voltage — After Step');
legend('Left', 'Right', 'Location', 'best');
grid on;

subplot(2, 1, 2);
plot(t_trim, v_L_clean, 'b', t_trim, v_R_clean, 'r');
xlabel('Time [s]'); ylabel('Velocity [m/s]');
title('Motor Velocity — After Step');
legend('Left', 'Right', 'Location', 'best');
grid on;

exportgraphics(fig2, [img_path 'day4_trimmed_step.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 7: Estimate Transfer Function Parameters
%  From the step response, estimate Kss (DC gain), tau (time constant),
%  and omega_b (break frequency) for a 1st order model:
%
%    G(s) = Kss * omega_b / (s + omega_b) = Kss / (tau*s + 1)
%
%  ========================================================================

% Use the average of left and right wheels
v_avg = (v_L_clean + v_R_clean) / 2;

% Index where t=0 (the step moment) in the trimmed data
idx_t0 = find(t_trim >= 0, 1, 'first');

% Initial value: average velocity BEFORE the step (t < 0 region)
if idx_t0 > 1
    v_0 = mean(v_avg(1:idx_t0-1));
    u_0 = mean((u_L_trim(1:idx_t0-1) + u_R_trim(1:idx_t0-1)) / 2);
else
    v_0 = v_avg(1);
    u_0 = (u_L_trim(1) + u_R_trim(1)) / 2;
end

% Steady-state value: average of last 20% of data (well after settling)
n_ss  = round(0.2 * length(v_avg));
v_ss  = mean(v_avg(end-n_ss:end));
u_ss  = mean((u_L_trim(end-n_ss:end) + u_R_trim(end-n_ss:end)) / 2);

% Step amplitudes
delta_v = v_ss - v_0;
delta_u = u_ss - u_0;

% DC gain: (m/s) per Volt
if abs(delta_u) > 0.01
    Kss_est = delta_v / delta_u;
else
    Kss_est = v_ss;
    fprintf('Warning: voltage step too small, using absolute Kss.\n');
end

% Time constant: find when response reaches 63.2% of final change
% Only search AFTER the step (t >= 0)
target_63 = v_0 + 0.632 * delta_v;
v_after_step = v_avg(idx_t0:end);
t_after_step = t_trim(idx_t0:end);
idx_63 = find(v_after_step >= target_63, 1, 'first');

if ~isempty(idx_63)
    tau_est = t_after_step(idx_63);
else
    tau_est = NaN;
    warning('Could not estimate time constant from data.');
end

wb_est = 1 / tau_est;

fprintf('=== Estimated 1st Order Parameters ===\n');
fprintf('  Steady-state velocity:  v_ss  = %.4f m/s\n', v_ss);
fprintf('  Velocity step:          dv    = %.4f m/s\n', delta_v);
fprintf('  Voltage step:           du    = %.2f V\n', delta_u);
fprintf('  DC gain:                Kss   = %.4f (m/s)/V\n', Kss_est);
fprintf('  Time constant:          tau   = %.4f s\n', tau_est);
fprintf('  Break frequency:        wb    = %.2f rad/s\n', wb_est);
fprintf('\n  G(s) = %.4f * %.2f / (s + %.2f)\n', Kss_est, wb_est, wb_est);
fprintf('  G(s) = %.4f / (%.4f*s + 1)\n\n', Kss_est, tau_est);

%% ========================================================================
%  SECTION 8: Overlay Model with Measured Data
%  ========================================================================

% 1st order model: v(t) = v_0 + delta_v * (1 - exp(-t/tau))  for t >= 0
%                  v(t) = v_0                                 for t < 0
v_model = v_0 * ones(size(t_trim));
after = t_trim >= 0;
v_model(after) = v_0 + delta_v * (1 - exp(-t_trim(after) / tau_est));

fig3 = figure('Name', 'Model vs Measured', 'Position', [100 100 800 500]);
plot(t_trim, v_avg, 'b', t_trim, v_model, 'r--', 'LineWidth', 1.5);
xlabel('Time [s]'); ylabel('Velocity [m/s]');
title('1st Order Model vs Measured Step Response');
legend('Measured (avg L+R)', ...
    sprintf('Model: Kss=%.3f (m/s)/V, tau=%.3fs', Kss_est, tau_est), ...
    'Location', 'best');
grid on;

% Mark key points
hold on;
if ~isnan(tau_est)
    plot(tau_est, target_63, 'ko', 'MarkerSize', 10, 'MarkerFaceColor', 'g');
    xline(tau_est, 'k--', sprintf('tau = %.3f s', tau_est));
    yline(target_63, 'k:', sprintf('63.2%% = %.3f m/s', target_63));
end
xline(0, 'g-', 'Step', 'LineWidth', 1.5, 'LabelOrientation', 'horizontal');
yline(v_ss, 'r:', sprintf('v_{ss} = %.3f m/s', v_ss));
yline(v_0, 'b:', sprintf('v_0 = %.3f m/s', v_0));
hold off;

exportgraphics(fig3, [img_path 'day4_model_vs_measured.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 9: Transfer Function in MATLAB
%  Create the estimated TF and verify with built-in tools.
%  ========================================================================

s = tf('s');
G_est = Kss_est * wb_est / (s + wb_est);

fprintf('=== MATLAB Transfer Function ===\n');
G_est

fprintf('DC gain (dcgain):     %.4f\n', dcgain(G_est));
fprintf('Pole:                 s = %.2f\n', pole(G_est));
fprintf('Bandwidth (rad/s):    %.2f\n', bandwidth(G_est));

fig4 = figure('Name', 'Estimated TF Analysis', 'Position', [100 100 900 700]);

subplot(2, 2, 1);
step(G_est);
title('Step Response of G_{est}(s)');
grid on;

subplot(2, 2, 2);
impulse(G_est);
title('Impulse Response of G_{est}(s)');
grid on;

subplot(2, 2, [3, 4]);
bode(G_est);
title('Bode Plot of G_{est}(s)');
grid on;

exportgraphics(fig4, [img_path 'day4_tf_analysis.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 10: Mission Plotting Template
%  After running your full mission (2+ speeds, 2+ turns), load the
%  mission log and plot the complete performance.
%  ========================================================================

% --- UPDATE THIS FILENAME ---
mission_file = 'log_mission.txt';

if isfile(mission_file)
    m_data = readtable(mission_file);
    m_data = fillmissing(m_data, 'nearest');

    m_t   = table2array(m_data(:,1));
    m_uL  = table2array(m_data(:,8));
    m_uR  = table2array(m_data(:,9));
    m_vL  = table2array(m_data(:,10));
    m_vR  = table2array(m_data(:,11));
    m_t   = m_t - m_t(1);

    fig5 = figure('Name', 'Mission Performance', 'Position', [100 100 900 800]);

    subplot(3, 1, 1);
    plot(m_t, m_uL, 'b', m_t, m_uR, 'r');
    xlabel('Time [s]'); ylabel('Voltage [V]');
    title('Mission — Motor Voltage');
    legend('Left', 'Right', 'Location', 'best');
    grid on;

    subplot(3, 1, 2);
    plot(m_t, m_vL, 'b', m_t, m_vR, 'r');
    xlabel('Time [s]'); ylabel('Velocity [m/s]');
    title('Mission — Motor Velocity');
    legend('Left', 'Right', 'Location', 'best');
    grid on;

    subplot(3, 1, 3);
    % Differential velocity -> turning
    plot(m_t, m_vL - m_vR, 'y', 'LineWidth', 1.5);
    xlabel('Time [s]'); ylabel('v_L - v_R [m/s]');
    title('Mission — Differential Velocity (Turning Indicator)');
    grid on;

    exportgraphics(fig5, [img_path 'day4_mission.png'], 'Resolution', 200);

    fprintf('Mission data plotted: %d samples\n', length(m_t));
else
    fprintf('Mission file "%s" not found — skipping mission plots.\n', mission_file);
    fprintf('After your mission, place the log here and re-run this section.\n');
end

fprintf('\n=== All sections complete ===\n');
