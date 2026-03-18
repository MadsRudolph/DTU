%% Day 6 - Bode Plot and Proportional Controller Design
%  34722 Linear Control Design 1 — Exercise 6 Companion
%  Topics: Bode plots, P-controller, low-pass filter design,
%          phase margin analysis, open-loop and closed-loop responses.
%
%  PREREQUISITE: Run Day5.m first to generate G_wu_avg and G_floor_avg
%                (or load them from a saved .mat file).
clear all; clc; close all;

% Plot settings
set(0, 'DefaultTextInterpreter', 'none');
set(0, 'DefaultAxesFontSize', 14);
set(0, 'DefaultLineLineWidth', 1.5);

% Image export path
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

%% ========================================================================
%  SECTION 0: Load Transfer Functions from Day 5
%  ========================================================================

fprintf('Loading Day 5 transfer functions...\n');
load('../Day5/Day5_results.mat');
fprintf('Loaded: G_wu_avg, G_floor_avg, T_s\n\n');

%% ========================================================================
%  SECTION 1: Bode Plots — Wheels Up vs On Floor
%  Task 1: Compare Bode plots for both configurations.
%  ========================================================================

fig1 = figure('Name', 'Bode: Wheels Up vs Floor', 'Position', [100 100 900 600]);
bode(G_wu_avg, 'b', G_floor_avg, 'r');
legend('Wheels Up', 'On Floor', 'Location', 'best');
title('Bode Plot Comparison: Wheels Up vs On Floor');
grid on;

exportgraphics(fig1, [img_path 'day6_bode_comparison.png'], 'Resolution', 200);

fprintf('=== Task 1: Bode Plot Comparison ===\n');
fprintf('DC gain (wheels up):  %.4f (m/s)/V\n', dcgain(G_wu_avg));
fprintf('DC gain (on floor):   %.4f (m/s)/V\n', dcgain(G_floor_avg));
fprintf('Bandwidth (wheels up):  '); bandwidth(G_wu_avg)
fprintf('Bandwidth (on floor):   '); bandwidth(G_floor_avg)
fprintf('\n');

%% ========================================================================
%  SECTION 2: Open-Loop Transfer Function with P-Controller
%  Task 2: G_ol = Kp * G_wu_avg, with Kp limited to 15.
%  Determine break frequency, crossover frequency, and phase margin.
%  ========================================================================

Kp = 15;                                % P-controller gain (max allowed)
G_ol = Kp * G_wu_avg;                   % open-loop TF

fig2 = figure('Name', 'Open-Loop with P-Controller', 'Position', [100 100 900 600]);
margin(G_ol);
title(sprintf('Open-Loop Bode Plot: G_{ol} = K_p * G, K_p = %g', Kp));
grid on;

exportgraphics(fig2, [img_path 'day6_open_loop_P.png'], 'Resolution', 200);

% Extract margin values
[Gm, Pm, Wcg, Wcp] = margin(G_ol);

fprintf('=== Task 2: Open-Loop with P-Controller (Kp = %g) ===\n', Kp);
fprintf('Gain margin:       %.2f dB (at %.2f rad/s)\n', 20*log10(Gm), Wcg);
fprintf('Phase margin:      %.2f deg (at %.2f rad/s)\n', Pm, Wcp);
fprintf('Crossover freq:    %.2f rad/s\n', Wcp);
fprintf('\n');

%% ========================================================================
%  SECTION 3: Noise Reduction via Low-Pass Filter
%  Task 3: Design a 1st-order low-pass filter G_filt = wc / (s + wc)
%  such that the phase margin reduction is at most 30 degrees.
%  ========================================================================

% --- Plot raw wheel speed to show noise ---
% (Load Day 5 log data again for the noise plot)
log_file = '../Day5/log_wheels_up.txt';
if isfile(log_file)
    opts = detectImportOptions(log_file, 'FileType', 'text');
    opts.CommentStyle = '%';
    data = readtable(log_file, opts);
    data = fillmissing(data, 'nearest');
    t_raw   = table2array(data(:,1));
    vL_raw  = table2array(data(:,10));
    vR_raw  = table2array(data(:,11));

    fig3 = figure('Name', 'Wheel Speed Noise', 'Position', [100 100 900 400]);
    plot(t_raw, vL_raw, 'b', t_raw, vR_raw, 'r');
    xlabel('Time [s]'); ylabel('Velocity [m/s]');
    title('Raw Wheel Speed Measurements (Noisy)');
    legend('Left', 'Right', 'Location', 'best');
    grid on;

    exportgraphics(fig3, [img_path 'day6_speed_noise.png'], 'Resolution', 200);
else
    fprintf('WARNING: Could not find %s for noise plot.\n', log_file);
    fprintf('Place your log file or adjust the path.\n');
end

% --- Design the low-pass filter ---
% Target: phase margin reduction <= 30 deg
PM_target = Pm - 30;           % minimum acceptable PM after adding filter

fprintf('=== Task 3: Low-Pass Filter Design ===\n');
fprintf('Phase margin without filter: %.2f deg\n', Pm);
fprintf('Target PM (max 30 deg loss): >= %.2f deg\n', PM_target);
fprintf('\n');

% Iteratively find the break frequency
% Start high (minimal phase loss) and decrease until PM drops too much
wc_candidates = logspace(0, 4, 500);     % 1 to 10000 rad/s
wc_best = wc_candidates(end);            % start with highest (least phase lag)

for i = length(wc_candidates):-1:1
    wc_try = wc_candidates(i);
    G_filt_try = tf(wc_try, [1 wc_try]);
    G_ol_filt_try = Kp * G_wu_avg * G_filt_try;
    [~, Pm_try, ~, ~] = margin(G_ol_filt_try);

    if Pm_try >= PM_target
        wc_best = wc_try;
    else
        break;  % PM dropped below target, use previous value
    end
end

fprintf('Selected filter break frequency: %.2f rad/s (%.2f Hz)\n', ...
    wc_best, wc_best/(2*pi));

% Create the filter with selected break frequency
G_filt = tf(wc_best, [1 wc_best]);

% Updated open-loop with filter
G_ol_filt = Kp * G_wu_avg * G_filt;

[Gm_f, Pm_f, Wcg_f, Wcp_f] = margin(G_ol_filt);

fprintf('Phase margin with filter:    %.2f deg\n', Pm_f);
fprintf('Phase margin reduction:      %.2f deg\n', Pm - Pm_f);
fprintf('Gain margin with filter:     %.2f dB\n', 20*log10(Gm_f));
fprintf('Crossover freq with filter:  %.2f rad/s\n\n', Wcp_f);

%% ========================================================================
%  SECTION 4: System Response Evaluation
%  Task 4: Bode plot and step response for the filtered open-loop TF.
%  ========================================================================

fig4 = figure('Name', 'Filtered Open-Loop', 'Position', [100 100 1000 800]);

subplot(2, 1, 1);
margin(G_ol_filt);
title(sprintf('Bode: G_{ol} = K_p * G * G_{filt}, wc = %.1f rad/s', wc_best));
grid on;

subplot(2, 1, 2);
step(G_ol_filt);
title('Step Response: Filtered Open-Loop');
xlabel('Time [s]'); ylabel('Amplitude');
grid on;

exportgraphics(fig4, [img_path 'day6_filtered_OL.png'], 'Resolution', 200);

% Compare filtered vs unfiltered open-loop
fig5 = figure('Name', 'Filter Effect on Open-Loop', 'Position', [100 100 900 600]);
bode(G_ol, 'b', G_ol_filt, 'r--');
legend('Without Filter', 'With Filter', 'Location', 'best');
title('Open-Loop Bode: Effect of Low-Pass Filter');
grid on;

exportgraphics(fig5, [img_path 'day6_filter_effect.png'], 'Resolution', 200);

%% ========================================================================
%  SECTION 5: Closed-Loop System Simulation
%  Task 5: G_cl = Kp*G / (1 + Kp*G*G_filt)
%  ========================================================================

G_cl = Kp * G_wu_avg / (1 + Kp * G_wu_avg * G_filt);
G_cl = minreal(G_cl);                   % simplify if possible

fig6 = figure('Name', 'Closed-Loop Step Response', 'Position', [100 100 900 500]);
step(G_cl);
title(sprintf('Closed-Loop Step Response: K_p = %g, wc_{filt} = %.1f rad/s', ...
    Kp, wc_best));
xlabel('Time [s]'); ylabel('Amplitude');
grid on;

% Extract step info
info = stepinfo(G_cl);

exportgraphics(fig6, [img_path 'day6_closed_loop_step.png'], 'Resolution', 200);

fprintf('=== Task 5: Closed-Loop System ===\n');
fprintf('Rise time:     %.4f s\n', info.RiseTime);
fprintf('Settling time: %.4f s\n', info.SettlingTime);
fprintf('Overshoot:     %.2f %%\n', info.Overshoot);
fprintf('Peak:          %.4f\n', info.Peak);
fprintf('DC gain (CL):  %.4f\n', dcgain(G_cl));
fprintf('\n');

% Bode of closed-loop
fig7 = figure('Name', 'Closed-Loop Bode', 'Position', [100 100 900 600]);
bode(G_cl);
title('Closed-Loop Bode Plot');
grid on;

exportgraphics(fig7, [img_path 'day6_closed_loop_bode.png'], 'Resolution', 200);

%% ========================================================================
%  Summary
%  ========================================================================

fprintf('=== Day 6 Complete ===\n');
fprintf('All figures exported to:\n  %s\n', img_path);
