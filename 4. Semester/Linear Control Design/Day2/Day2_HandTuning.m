%% Day 2 - Hand-Tuning of P/PI Controllers
%  DC Motor: voltage -> angular position
%  Simulink model: DC_motor_Ex_1.slx
clear all; clc; close all;

% Plot settings
set(0, 'DefaultTextInterpreter', 'none');
set(0, 'DefaultAxesFontSize', 14);
set(0, 'DefaultLineLineWidth', 1.5);

% Image export path
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

% Shared settings
ref = 1;  % Position reference [rad]

%% ========================================================================
%  PART 1a: P-Controller — ~6s settling time (Load OFF)
%  ========================================================================
K_P      = 0.008;   % Tune this: ~6s settling
tau_i    = inf;
K_I_gain = 0;
Load     = 0;
t_f      = 20;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 1a: P-Controller (K_P = %.4f, ~6s settling)', K_P));
exportgraphics(fig, [img_path 'ex2_part1a_P_6s.png'], 'Resolution', 200);

%% ========================================================================
%  PART 1b: P-Controller — ~2.5s settling, overshoot <=2% (Load OFF)
%  ========================================================================
K_P      = 0.015;    % Tune this: faster, ~2.5s settling, <=2% overshoot
tau_i    = inf;
K_I_gain = 0;
Load     = 0;
t_f      = 20;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 1b: P-Controller (K_P = %.4f, ~2.5s settling)', K_P));
exportgraphics(fig, [img_path 'ex2_part1b_P_fast.png'], 'Resolution', 200);

%% ========================================================================
%  PART 2a: P-Controller with disturbance (Load ON)
%  ========================================================================
K_P      = 0.008;   % Best K_P from Part 1a
tau_i    = inf;
K_I_gain = 0;
Load     = 0.0001;
t_f      = 30;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 2a: P-Controller (K_P = %.4f, Load ON)', K_P));
exportgraphics(fig, [img_path 'ex2_part2a_P_with_load.png'], 'Resolution', 200);

%% ========================================================================
%  PART 2b: PI-Controller with disturbance (Load ON)
%  ========================================================================
K_P      = 0.008;   % Start from Part 1 value, adjust as needed
tau_i    = 5;       % Tune this: integrator time constant [s]
K_I_gain = 1/tau_i;
Load     = 0.0001;
t_f      = 30;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 2b: PI-Controller (K_P = %.4f, tau_i = %.1f, Load ON)', K_P, tau_i));
exportgraphics(fig, [img_path 'ex2_part2b_PI_with_load.png'], 'Resolution', 200);

%% ========================================================================
%  PART 3a: Ziegler-Nichols — Find K_u (Load OFF)
%  ========================================================================
K_P      = 0.0483;   % Increase until sustained oscillations
tau_i    = inf;
K_I_gain = 0;
Load     = 0;
t_f      = 20;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 3a: Finding K_u (K_P = %.4f)', K_P));
exportgraphics(fig, [img_path 'ex2_part3a_finding_Ku.png'], 'Resolution', 200);

% Fill in after finding sustained oscillations:
K_u = 0.0483;             % Ultimate gain
P_u = 1;             % Ultimate period [s]

% Calculate Ziegler-Nichols parameters
fprintf('=== Ziegler-Nichols Closed-Loop Results ===\n');
fprintf('K_u = %.4f, P_u = %.4f s\n\n', K_u, P_u);

K_P_zn_P     = 0.5 * K_u;
K_P_zn_PI    = 0.45 * K_u;
tau_i_zn     = P_u / 1.2;
K_P_zn_PID   = 0.6 * K_u;
tau_i_zn_PID = 0.5 * P_u;
tau_d_zn     = 0.125 * P_u;

fprintf('P:   K_p = %.4f\n', K_P_zn_P);
fprintf('PI:  K_p = %.4f, tau_i = %.4f s\n', K_P_zn_PI, tau_i_zn);
fprintf('PID: K_p = %.4f, tau_i = %.4f s, tau_d = %.4f s\n', ...
    K_P_zn_PID, tau_i_zn_PID, tau_d_zn);

%% ========================================================================
%  PART 3b: Z-N P-Controller (Load OFF)
%  >>> Uncomment after filling in K_u and P_u <<<
%  ========================================================================
K_P      = K_P_zn_P;
tau_i    = inf;
K_I_gain = 0;
Load     = 0;
t_f      = 20;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 3b: Z-N P-Controller (K_P = %.4f, Load OFF)', K_P));
exportgraphics(fig, [img_path 'ex2_part3b_ZN_P_no_load.png'], 'Resolution', 200);

% ========================================================================
% PART 3c: Z-N P-Controller (Load ON)
% >>> Uncomment after filling in K_u and P_u <<<
% ========================================================================
K_P      = K_P_zn_P;
tau_i    = inf;
K_I_gain = 0;
Load     = 0.0001;
t_f      = 30;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 3c: Z-N P-Controller (K_P = %.4f, Load ON)', K_P));
exportgraphics(fig, [img_path 'ex2_part3c_ZN_P_with_load.png'], 'Resolution', 200);

% ========================================================================
% PART 3d: Z-N PI-Controller (Load ON)
% >>> Uncomment after filling in K_u and P_u <<<
% ========================================================================
K_P      = K_P_zn_PI;
tau_i    = tau_i_zn;
K_I_gain = 1/tau_i;
Load     = 0.0001;
t_f      = 30;

out = sim('DC_motor_Ex_1', 'StopTime', num2str(t_f));
[t, position, voltage, ref_sig] = extract_signals(out);

fig = plot_results(t, position, ref_sig, voltage, ...
    sprintf('Part 3d: Z-N PI-Controller (K_P = %.4f, tau_i = %.2f, Load ON)', K_P, tau_i));
exportgraphics(fig, [img_path 'ex2_part3d_ZN_PI_with_load.png'], 'Resolution', 200);

%% ========================================================================
%  Helper Functions
%  ========================================================================
function [t, position, voltage, ref_sig] = extract_signals(out)
    t        = out.tout;
    position = squeeze(out.position.Data);
    voltage  = squeeze(out.voltage.Data);
    ref_sig  = interp1(out.reference.Time, squeeze(out.reference.Data), t, 'previous', 'extrap');
end

function fig = plot_results(t, position, reference, voltage, title_str)
    fig = figure;

    % Top: Position and reference
    subplot(2, 1, 1);
    plot(t, position, 'b');
    hold on;
    plot(t, reference, 'r--');
    hold off;
    grid on;
    ylabel('Position [rad]');
    legend('Position y(t)', 'Reference r(t)', 'Location', 'best');
    title(title_str);

    % Bottom: Applied voltage
    subplot(2, 1, 2);
    plot(t, voltage, 'b');
    grid on;
    ylabel('Voltage [V]');
    xlabel('Time [s]');
    title('Control Signal');
end
