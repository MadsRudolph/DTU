%% REGBOT Position Controller — Simulink Simulation (Day 8)
%  34722 Linear Control Design 1
%  Run regbot_position_design.m FIRST, or this script recomputes everything.
clear all; clc; close all;

img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

grey = [0.6 0.6 0.6];

%% Recompute controller (v2 model)
s = tf('s');
G_vel = 2.198 / (s + 5.985);
G_pos = minreal(G_vel / s);

N_i = 3;  alpha = 0.3;  gamma_M = 60;

w = logspace(-2, 3, 5000);
[~, P_bode, w_out] = bode(G_pos, w);
P_bode = squeeze(P_bode);

phi_i = rad2deg(-atan(1/N_i));
phi_m = rad2deg(asin((1-alpha)/(1+alpha)));
phi_G_req = -180 + gamma_M - phi_i - phi_m;

i_c = find(P_bode <= phi_G_req, 1);
omega_c = w_out(i_c);

tau_i = N_i / omega_c;
tau_d = 1 / (omega_c * sqrt(alpha));
C_PI = (tau_i*s + 1) / (tau_i*s);
C_D  = (tau_d*s + 1) / (alpha*tau_d*s + 1);

G_ol_noK = minreal(C_PI * C_D * G_pos);
K_P = 1 / abs(freqresp(G_ol_noK, omega_c));

fprintf('K_P=%.4f, tau_i=%.4f, tau_zero=%.4f, tau_pole=%.4f\n', ...
    K_P, tau_i, tau_d, alpha*tau_d);

%% Extract TF polynomials for Simulink blocks
[num_vel, den_vel] = tfdata(G_vel, 'v');
[num_pi,  den_pi]  = tfdata(C_PI, 'v');
[num_cd,  den_cd]  = tfdata(C_D, 'v');

%% Build Simulink model
model_name = 'regbot_position_sim';

if bdIsLoaded(model_name)
    close_system(model_name, 0);
end
new_system(model_name);
open_system(model_name);

% Step input: 0.5 m at t = 0.1 s
add_block('simulink/Sources/Step', [model_name '/Step']);
set_param([model_name '/Step'], 'Time', '0.1', 'After', '0.5', 'Before', '0');

% Sum block
add_block('simulink/Math Operations/Sum', [model_name '/Sum']);
set_param([model_name '/Sum'], 'Inputs', '+-');

% K_P gain
add_block('simulink/Math Operations/Gain', [model_name '/K_P']);
set_param([model_name '/K_P'], 'Gain', num2str(K_P));

% C_PI
add_block('simulink/Continuous/Transfer Fcn', [model_name '/C_PI']);
set_param([model_name '/C_PI'], 'Numerator', mat2str(num_pi), 'Denominator', mat2str(den_pi));

% Saturation +/- 9V
add_block('simulink/Discontinuities/Saturation', [model_name '/Saturation']);
set_param([model_name '/Saturation'], 'UpperLimit', '9', 'LowerLimit', '-9');

% G_vel
add_block('simulink/Continuous/Transfer Fcn', [model_name '/G_vel']);
set_param([model_name '/G_vel'], 'Numerator', mat2str(num_vel), 'Denominator', mat2str(den_vel));

% Integrator (1/s)
add_block('simulink/Continuous/Integrator', [model_name '/Integrator']);

% C_D (Lead) in feedback
add_block('simulink/Continuous/Transfer Fcn', [model_name '/C_D']);
set_param([model_name '/C_D'], 'Numerator', mat2str(num_cd), 'Denominator', mat2str(den_cd));

% To Workspace
add_block('simulink/Sinks/To Workspace', [model_name '/pos_out']);
set_param([model_name '/pos_out'], 'VariableName', 'pos_data', 'SaveFormat', 'Timeseries');
add_block('simulink/Sinks/To Workspace', [model_name '/volt_out']);
set_param([model_name '/volt_out'], 'VariableName', 'volt_data', 'SaveFormat', 'Timeseries');

% Position blocks
positions = {
    '/Step',       [50  100  80  120];
    '/Sum',        [140 100  160 120];
    '/K_P',        [220 100  260 120];
    '/C_PI',       [310 100  390 120];
    '/Saturation', [440 100  490 120];
    '/G_vel',      [540 100  620 120];
    '/Integrator', [670 100  710 120];
    '/pos_out',    [780 100  840 120];
    '/C_D',        [400 200  480 220];
    '/volt_out',   [540 50   600 70];
};
for k = 1:size(positions, 1)
    set_param([model_name positions{k,1}], 'Position', positions{k,2});
end

% Connect: forward path
add_line(model_name, 'Step/1',        'Sum/1');
add_line(model_name, 'Sum/1',         'K_P/1');
add_line(model_name, 'K_P/1',         'C_PI/1');
add_line(model_name, 'C_PI/1',        'Saturation/1');
add_line(model_name, 'Saturation/1',  'G_vel/1');
add_line(model_name, 'G_vel/1',       'Integrator/1');
add_line(model_name, 'Integrator/1',  'pos_out/1');
% Feedback: position -> C_D -> Sum(-)
add_line(model_name, 'Integrator/1',  'C_D/1');
add_line(model_name, 'C_D/1',         'Sum/2');
% Voltage logging
add_line(model_name, 'Saturation/1',  'volt_out/1');

set_param(model_name, 'StopTime', '5', 'Solver', 'ode45');
save_system(model_name);

%% Run simulation (+/- 9V)
fprintf('Running simulation (+/-9V)...\n');
sim_out = sim(model_name, 'StopTime', '5');

pos_ts  = sim_out.get('pos_data');
volt_ts = sim_out.get('volt_data');
t_sim   = pos_ts.Time;
x_sim   = squeeze(pos_ts.Data);
u_sim   = squeeze(volt_ts.Data);
t_volt  = volt_ts.Time;

%% Plot 1: Simulink result with voltage
figure(1); clf;
aa = subplot(2,1,1);
plot(t_sim, x_sim); hold on;
plot(t_sim, 0.5*ones(size(t_sim)), '--', 'Color', grey);
hold off; grid on;
ylabel('$x, x_{ref}$ [m]');
legend({'$x$', '$x_{ref}$'}, 'interpreter', 'latex');
title('Simulink: PI-Lead (feedback), saturation $\pm 9$ V');

bb = subplot(2,1,2);
plot(t_volt, u_sim); hold on;
yline(9, '--r'); yline(-9, '--r');
hold off; grid on;
xlabel('$t$ [s]');
ylabel('Motor voltage [V]');
legend({'$u$', '$\pm 9$ V limit'}, 'interpreter', 'latex');
linkaxes([aa, bb], 'x');
xlim([0 3]);
saveas(gcf, [img_path 'day8_simulink_9V.png']);

%% Plot 2: MATLAB (linear) vs Simulink (with saturation)
G_cl_fb = minreal(K_P*C_PI*G_pos / (1 + K_P*C_PI*C_D*G_pos));
[y_lin, t_lin] = step(G_cl_fb, 0:0.001:5);

figure(2); clf;
plot(t_sim - 0.1, x_sim); hold on;
plot(t_lin, 0.5*y_lin);
plot(t_lin, 0.5*ones(size(t_lin)), '--', 'Color', grey);
hold off; grid on;
xlabel('$t$ [s]');
ylabel('Position [m]');
legend({'Simulink ($\pm 9$ V)', 'MATLAB (no sat)', 'Reference'}, 'interpreter', 'latex');
xlim([0 3]);
saveas(gcf, [img_path 'day8_simulink_vs_matlab.png']);

%% Run with +/- 3V saturation
set_param([model_name '/Saturation'], 'UpperLimit', '3', 'LowerLimit', '-3');
save_system(model_name);

fprintf('Running simulation (+/-3V)...\n');
sim_out_3V = sim(model_name, 'StopTime', '5');

pos_ts3 = sim_out_3V.get('pos_data');
volt_ts3 = sim_out_3V.get('volt_data');
t_sim3  = pos_ts3.Time;
x_sim3  = squeeze(pos_ts3.Data);
u_sim3  = squeeze(volt_ts3.Data);
t_v3    = volt_ts3.Time;

%% Plot 3: Compare saturation limits
figure(3); clf;
aa = subplot(2,1,1);
plot(t_sim, x_sim); hold on;
plot(t_sim3, x_sim3);
plot(t_sim, 0.5*ones(size(t_sim)), '--', 'Color', grey);
hold off; grid on;
ylabel('$x, x_{ref}$ [m]');
legend({'$\pm 9$ V', '$\pm 3$ V', 'Reference'}, 'interpreter', 'latex');
title('Effect of saturation limits');

bb = subplot(2,1,2);
plot(t_volt, u_sim); hold on;
plot(t_v3, u_sim3);
yline(9, '--r'); yline(-9, '--r');
yline(3, '--m'); yline(-3, '--m');
hold off; grid on;
xlabel('$t$ [s]');
ylabel('Motor voltage [V]');
linkaxes([aa, bb], 'x');
xlim([0 5]);
saveas(gcf, [img_path 'day8_simulink_sat_comparison.png']);

% Reset back to 9V
set_param([model_name '/Saturation'], 'UpperLimit', '9', 'LowerLimit', '-9');
save_system(model_name);

fprintf('\nDone. Close model with: close_system(''%s'')\n', model_name);
