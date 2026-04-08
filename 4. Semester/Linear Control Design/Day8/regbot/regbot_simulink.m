%% REGBOT Position Controller — Simulink Simulation
%  Day 8 — 34722 Linear Control Design 1
%  Builds and runs a Simulink model with the PI-Lead controller
%  (Lead in feedback), including motor voltage saturation.
%
%  Run regbot_position_controller.m FIRST to get controller parameters
%  in the workspace, OR this script loads them from Day5 and recomputes.
clear all; clc; close all;

% Figure export path
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

%% ========================================================================
%  SECTION 1: Recompute Controller (same as regbot_position_controller.m)
%  ========================================================================

load('../../Day5/Day5_results.mat');
s = tf('s');

G_vel = G_floor_avg;
G_pos = minreal(G_vel * (1/s));

% Design parameters
N_i = 5;  alpha = 0.1;  gamma_M = 60;

% Phase balance
w = logspace(-1, 5, 5000);
[~, P_bode, w_out] = bode(G_pos, w);
P_bode = squeeze(P_bode);

phi_i = rad2deg(-atan(1/N_i));
phi_m = rad2deg(asin((1 - alpha)/(1 + alpha)));
phi_G_req = -180 + gamma_M - phi_i - phi_m;

i_c = find(P_bode <= phi_G_req, 1, 'first');
omega_c = w_out(i_c);

tau_i = N_i / omega_c;
tau_d = 1 / (omega_c * sqrt(alpha));

C_PI = (1 + 1/(tau_i*s));
C_D  = (tau_d*s + 1) / (alpha*tau_d*s + 1);

G_ol_noK = minreal(C_PI * C_D * G_pos);
K_P = 1 / abs(freqresp(G_ol_noK, omega_c));

fprintf('Controller: K_P=%.4f, tau_i=%.4f, tau_d=%.4f, alpha=%.2f\n', ...
    K_P, tau_i, tau_d, alpha);

%% ========================================================================
%  SECTION 2: Extract TF Polynomials for Simulink
%  ========================================================================

[num_vel, den_vel] = tfdata(G_vel, 'v');   % Velocity TF
[num_pi,  den_pi]  = tfdata(C_PI, 'v');    % PI controller
[num_cd,  den_cd]  = tfdata(C_D, 'v');     % Lead controller

fprintf('\nG_vel: num = [%s], den = [%s]\n', num2str(num_vel), num2str(den_vel));
fprintf('C_PI:  num = [%s], den = [%s]\n', num2str(num_pi), num2str(den_pi));
fprintf('C_D:   num = [%s], den = [%s]\n', num2str(num_cd), num2str(den_cd));

%% ========================================================================
%  SECTION 3: Build Simulink Model Programmatically
%  ========================================================================

model_name = 'regbot_position_sim';

% Close if already open
if bdIsLoaded(model_name)
    close_system(model_name, 0);
end
new_system(model_name);
open_system(model_name);

% --- Add blocks ---
% Step input: 0.5 m at t = 0.1 s
add_block('simulink/Sources/Step', [model_name '/Step']);
set_param([model_name '/Step'], 'Time', '0.1', 'After', '0.5', 'Before', '0');

% Sum: reference - feedback
add_block('simulink/Math Operations/Sum', [model_name '/Sum']);
set_param([model_name '/Sum'], 'Inputs', '+-');

% K_P gain
add_block('simulink/Math Operations/Gain', [model_name '/K_P']);
set_param([model_name '/K_P'], 'Gain', num2str(K_P));

% C_PI transfer function
add_block('simulink/Continuous/Transfer Fcn', [model_name '/C_PI']);
set_param([model_name '/C_PI'], ...
    'Numerator', mat2str(num_pi), ...
    'Denominator', mat2str(den_pi));

% Saturation: +/- 9 V
add_block('simulink/Discontinuities/Saturation', [model_name '/Saturation_9V']);
set_param([model_name '/Saturation_9V'], 'UpperLimit', '9', 'LowerLimit', '-9');

% G_vel: voltage -> velocity
add_block('simulink/Continuous/Transfer Fcn', [model_name '/G_vel']);
set_param([model_name '/G_vel'], ...
    'Numerator', mat2str(num_vel), ...
    'Denominator', mat2str(den_vel));

% Integrator: velocity -> position (1/s)
add_block('simulink/Continuous/Integrator', [model_name '/Integrator']);

% C_D (Lead) in feedback branch
add_block('simulink/Continuous/Transfer Fcn', [model_name '/C_D']);
set_param([model_name '/C_D'], ...
    'Numerator', mat2str(num_cd), ...
    'Denominator', mat2str(den_cd));

% To Workspace blocks
add_block('simulink/Sinks/To Workspace', [model_name '/pos_out']);
set_param([model_name '/pos_out'], 'VariableName', 'pos_data', 'SaveFormat', 'Timeseries');

add_block('simulink/Sinks/To Workspace', [model_name '/volt_out']);
set_param([model_name '/volt_out'], 'VariableName', 'volt_data', 'SaveFormat', 'Timeseries');

% --- Position blocks ---
% Row layout: Step -> Sum -> K_P -> C_PI -> Sat -> G_vel -> Int -> pos_out
%                ^                                               |
%                |--- C_D <--------------------------------------+

positions = {
    '/Step',           [50  100  80  120];
    '/Sum',            [140 100  160 120];
    '/K_P',            [220 100  260 120];
    '/C_PI',           [310 100  390 120];
    '/Saturation_9V',  [440 100  490 120];
    '/G_vel',          [540 100  620 120];
    '/Integrator',     [670 100  710 120];
    '/pos_out',        [780 100  840 120];
    '/C_D',            [400 200  480 220];
    '/volt_out',       [540 50   600 70];
};

for k = 1:size(positions, 1)
    set_param([model_name positions{k,1}], 'Position', positions{k,2});
end

% --- Connect blocks ---
% Forward path
add_line(model_name, 'Step/1',          'Sum/1');
add_line(model_name, 'Sum/1',           'K_P/1');
add_line(model_name, 'K_P/1',           'C_PI/1');
add_line(model_name, 'C_PI/1',          'Saturation_9V/1');
add_line(model_name, 'Saturation_9V/1', 'G_vel/1');
add_line(model_name, 'G_vel/1',         'Integrator/1');
add_line(model_name, 'Integrator/1',    'pos_out/1');

% Feedback: position -> C_D -> Sum(-)
add_line(model_name, 'Integrator/1',    'C_D/1');
add_line(model_name, 'C_D/1',           'Sum/2');

% Voltage logging: tap after saturation
add_line(model_name, 'Saturation_9V/1', 'volt_out/1');

% Set simulation parameters
set_param(model_name, 'StopTime', '5', 'Solver', 'ode45');

% Save model
save_system(model_name);
fprintf('\nSimulink model "%s" created and saved.\n', model_name);

%% ========================================================================
%  SECTION 4: Run Simulation
%  ========================================================================

fprintf('Running simulation...\n');
sim_out = sim(model_name, 'StopTime', '5');

% Extract data from sim output
pos_ts  = sim_out.get('pos_data');
volt_ts = sim_out.get('volt_data');
t_sim   = pos_ts.Time;
x_sim   = squeeze(pos_ts.Data);
t_volt  = volt_ts.Time;
u_sim   = squeeze(volt_ts.Data);

fprintf('Simulation complete. %d samples.\n', length(t_sim));

%% ========================================================================
%  SECTION 5: Plot Results — Saturation at +/- 9 V
%  ========================================================================

figure(1); clf;
aa = subplot(2,1,1);
plot(t_sim, x_sim);
hold on;
plot(t_sim, 0.5*ones(size(t_sim)), '--k');
hold off;
grid on;
ylabel('$x, x_{ref}$ in m');
legend({'$x$', '$x_{ref}$'}, 'interpreter', 'latex');
title('Simulink: PI-Lead (feedback), saturation $\pm 9$ V');

bb = subplot(2,1,2);
plot(t_volt, u_sim);
hold on;
yline(9, '--r');
yline(-9, '--r');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('Motor voltage [V]');
legend({'$u$', '$\pm 9$ V limit'}, 'interpreter', 'latex');
linkaxes([aa, bb], 'x');
xlim([0 3]);
saveas(gcf, [img_path 'day8_simulink_9V.png']);

% Step info from simulation
idx_01 = find(t_sim >= 0.1, 1);  % step happens at t=0.1
x_shifted = x_sim(idx_01:end);
t_shifted = t_sim(idx_01:end) - 0.1;
x_final = x_shifted(end);

% Rise time (10% to 90%)
idx_10 = find(x_shifted >= 0.1*x_final, 1);
idx_90 = find(x_shifted >= 0.9*x_final, 1);
tr_sim = t_shifted(idx_90) - t_shifted(idx_10);

% Settling (2%)
settled = abs(x_shifted - x_final) <= 0.02*x_final;
for k = length(settled):-1:1
    if ~settled(k); break; end
end
ts_sim = t_shifted(min(k+1, length(t_shifted)));

% Overshoot
Mp_sim = (max(x_shifted) - x_final) / x_final * 100;

fprintf('\n=== Simulink Results (sat +/-9V) ===\n');
fprintf('Final value:   %.4f m\n', x_final);
fprintf('Rise time:     %.4f s\n', tr_sim);
fprintf('Settling time: %.4f s\n', ts_sim);
fprintf('Overshoot:     %.2f %%\n', Mp_sim);
fprintf('Steady-state error: %.4f m\n', abs(0.5 - x_final));

%% ========================================================================
%  SECTION 6: Compare with MATLAB (no saturation) result
%  ========================================================================

G_ol = K_P * G_ol_noK;
G_cl_fb = minreal(K_P*C_PI*G_pos / (1 + K_P*C_PI*C_D*G_pos));

[y_lin, t_lin] = step(G_cl_fb, 0:0.001:5);

figure(2); clf;
plot(t_sim - 0.1, x_sim);   % shift Simulink so step is at t=0
hold on;
plot(t_lin, 0.5*y_lin);     % scale by 0.5 m step size
plot(t_lin, 0.5*ones(size(t_lin)), '--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('Position [m]');
title('MATLAB (linear) vs Simulink (with saturation)');
legend({'Simulink ($\pm 9$ V sat)', 'MATLAB (no sat)', 'Reference'}, ...
    'interpreter', 'latex');
xlim([0 3]);
saveas(gcf, [img_path 'day8_simulink_vs_matlab.png']);

%% ========================================================================
%  SECTION 7: Repeat with tighter saturation (+/- 3 V)
%  ========================================================================

set_param([model_name '/Saturation_9V'], 'UpperLimit', '3', 'LowerLimit', '-3');
save_system(model_name);

fprintf('\nRunning simulation with +/-3V saturation...\n');
sim_out_3V = sim(model_name, 'StopTime', '5');

pos_ts3  = sim_out_3V.get('pos_data');
volt_ts3 = sim_out_3V.get('volt_data');
t_sim3   = pos_ts3.Time;
x_sim3   = squeeze(pos_ts3.Data);
t_v3     = volt_ts3.Time;
u_sim3   = squeeze(volt_ts3.Data);

figure(3); clf;
aa = subplot(2,1,1);
plot(t_sim, x_sim);
hold on;
plot(t_sim3, x_sim3);
plot(t_sim, 0.5*ones(size(t_sim)), '--k');
hold off;
grid on;
ylabel('$x, x_{ref}$ in m');
legend({'$\pm 9$ V', '$\pm 3$ V', 'Reference'}, 'interpreter', 'latex');
title('Effect of saturation limits on step response');

bb = subplot(2,1,2);
plot(t_volt, u_sim);
hold on;
plot(t_v3, u_sim3);
yline(9, '--r');
yline(-9, '--r');
yline(3, '--m');
yline(-3, '--m');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('Motor voltage [V]');
linkaxes([aa, bb], 'x');
xlim([0 5]);
saveas(gcf, [img_path 'day8_simulink_sat_comparison.png']);

% Reset saturation back to 9V
set_param([model_name '/Saturation_9V'], 'UpperLimit', '9', 'LowerLimit', '-9');
save_system(model_name);

idx_01_3 = find(t_sim3 >= 0.1, 1);
x_final3 = x_sim3(end);
fprintf('\n=== Simulink Results (sat +/-3V) ===\n');
fprintf('Final value:   %.4f m\n', x_final3);
fprintf('Steady-state error: %.4f m\n', abs(0.5 - x_final3));
fprintf('(Tighter saturation -> slower response, but PI still eliminates e_ss)\n');

fprintf('\n=== Done. Close model with: close_system(''%s'') ===\n', model_name);
