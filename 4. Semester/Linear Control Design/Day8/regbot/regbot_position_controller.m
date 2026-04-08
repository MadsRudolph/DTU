%% REGBOT Position Controller Design (PI-Lead)
%  Day 8 & 9 — 34722 Linear Control Design 1
%  Designs a PI-Lead position controller using the floor transfer function
%  identified in Day 5.
clear all; clc; close all;

% Figure export path
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

% Plot settings
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

%% ========================================================================
%  SECTION 1: Load Day 5 Transfer Function
%  ========================================================================

load('../../Day5/Day5_results.mat');
s = tf('s');

G_vel = G_floor_avg;        % Voltage -> velocity (on floor)
fprintf('=== Velocity TF (floor avg) ===\n');
G_vel

fprintf('DC gain: %.4f (m/s)/V\n', dcgain(G_vel));
fprintf('Poles: '); disp(pole(G_vel)');

%% ========================================================================
%  SECTION 2: Position Transfer Function
%  Position = integral of velocity -> multiply by 1/s
%  ========================================================================

G_pos = G_vel * (1/s);      % Voltage -> position (type-1 system)
G_pos = minreal(G_pos);

fprintf('\n=== Position TF: G_vel(s) / s ===\n');
G_pos
fprintf('Poles: '); disp(pole(G_pos)');
fprintf('System type: %d (number of poles at origin)\n', ...
    sum(abs(pole(G_pos)) < 1e-6));

%% ========================================================================
%  SECTION 3: Bode Plot of G_pos(s)
%  ========================================================================

w = logspace(-1, 5, 5000);
[M,P_bode,w_out] = bode(G_pos,w);
M = mag2db(squeeze(M));
P_bode = squeeze(P_bode);

figure(1); clf;
aa = subplot(2,1,1);
semilogx(w_out, M, 'Color', [84 130 15]./255);
hold on; yline(0,'--k'); hold off;
grid on;
ylabel('$\vert G_{pos} \vert$ in dB');
set(gca,'xtick',[]);
title('Open-loop Bode: $G_{pos}(s) = G_{vel}(s)/s$');

bb = subplot(2,1,2);
semilogx(w_out, P_bode, 'Color', [84 130 15]./255);
hold on;
semilogx(w_out, -180*ones(size(w_out)), '--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{pos}$ in deg');
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_regbot_bode_plant.png']);

%% ========================================================================
%  SECTION 4: Assess Controller Needs
%  ========================================================================

% Type-1 system: already has an integrator -> zero e_ss for step with P
% But we still want PI for robustness + Lead for phase margin
% The exercise requires PI-Lead with gamma_M >= 60 deg

[gm_orig, pm_orig, wpi_orig, wc_orig] = margin(G_pos);
fprintf('\n=== Original Plant Margins ===\n');
fprintf('Gain margin:  %.2f dB\n', mag2db(gm_orig));
fprintf('Phase margin: %.2f deg at omega_c = %.2f rad/s\n', pm_orig, wc_orig);

%% ========================================================================
%  SECTION 5: PI-Lead Controller Design
%  ========================================================================

% Design parameters
N_i = 5;            % PI zero placement factor (from exercise spec)
alpha = 0.1;        % Lead controller ratio (from exercise spec)
gamma_M = 60;       % Target phase margin [deg]

% Phase contributions
phi_i = rad2deg(-atan(1/N_i));                      % PI phase at omega_c
phi_m = rad2deg(asin((1 - alpha)/(1 + alpha)));     % Lead phase at omega_c
phi_G_req = -180 + gamma_M - phi_i - phi_m;         % Required plant phase

fprintf('\n=== Design Parameters ===\n');
fprintf('N_i = %d, alpha = %.2f, gamma_M = %d deg\n', N_i, alpha, gamma_M);
fprintf('PI phase:   %.2f deg\n', phi_i);
fprintf('Lead phase: %.2f deg\n', phi_m);
fprintf('Required plant phase at omega_c: %.2f deg\n', phi_G_req);

% Find crossover frequency where plant has the required phase
i_c = find(P_bode <= phi_G_req, 1, 'first');
if isempty(i_c)
    error('Could not find crossover frequency. Try different N_i or alpha.');
end
omega_c = w_out(i_c);
fprintf('New crossover frequency: %.3f rad/s\n', omega_c);

% PI controller
tau_i = N_i / omega_c;
C_PI = (1 + 1/(tau_i*s));
fprintf('PI: tau_i = %.4f s\n', tau_i);

% Lead controller
tau_d = 1 / (omega_c * sqrt(alpha));
C_D = (tau_d*s + 1) / (alpha*tau_d*s + 1);
fprintf('Lead: tau_d = %.4f s\n', tau_d);

% Open-loop without K_P
G_ol_noK = minreal(C_PI * C_D * G_pos);

% Proportional gain (set |G_ol| = 0 dB at omega_c)
K_P = 1 / abs(freqresp(G_ol_noK, omega_c));
fprintf('K_P: %.4f\n', K_P);

% Full open-loop
G_ol = K_P * G_ol_noK;

%% ========================================================================
%  SECTION 6: Verify Design — Open-Loop Margins
%  ========================================================================

[gm_des, pm_des, wpi_des, wc_des] = margin(G_ol);
fprintf('\n=== Designed Open-Loop Margins ===\n');
fprintf('Gain margin:  %.2f dB\n', mag2db(gm_des));
fprintf('Phase margin: %.2f deg at omega_c = %.2f rad/s\n', pm_des, wc_des);

%% ========================================================================
%  SECTION 7: Bode Plots — Components
%  ========================================================================

[M_pi, P_pi] = bode(C_PI, w);
M_pi = mag2db(squeeze(M_pi)); P_pi = squeeze(P_pi);
[M_cd, P_cd] = bode(C_D, w);
M_cd = mag2db(squeeze(M_cd)); P_cd = squeeze(P_cd);

figure(2); clf;
aa = subplot(2,1,1);
semilogx(w_out, M, 'Color', [84 130 15]./255);
hold on;
semilogx(w_out, M_pi, 'r--');
semilogx(w_out, M_cd, 'b-.');
scatter(w_out(i_c), M(i_c), 40, 'markerFaceColor', 'k', 'MarkerEdgeColor', 'k');
hold off;
grid on;
ylabel('$\vert \cdot \vert$ in dB');
set(gca,'xtick',[]);
legend({'$G_{pos}(s)$','$C_{PI}(s)$','$C_D(s)$'},'interpreter','latex');
title('Component Bode Plots');

bb = subplot(2,1,2);
semilogx(w_out, P_bode, 'Color', [84 130 15]./255);
hold on;
semilogx(w_out, P_pi, 'r--');
semilogx(w_out, P_cd, 'b-.');
semilogx(w_out, -180*ones(size(w_out)), '--k');
scatter(w_out(i_c), P_bode(i_c), 40, 'markerFaceColor', 'k', 'MarkerEdgeColor', 'k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle \cdot$ in deg');
ylim([-275 90]);
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_regbot_component_bode.png']);

%% ========================================================================
%  SECTION 8: Bode Plot — Open-Loop with Controller
%  ========================================================================

[M_ol, P_ol] = bode(G_ol, w);
M_ol = mag2db(squeeze(M_ol)); P_ol = squeeze(P_ol);

figure(3); clf;
aa = subplot(2,1,1);
semilogx(w_out, M_ol);
hold on; yline(0, '--k'); hold off;
grid on;
ylabel('$\vert G_{ol} \vert$ in dB');
set(gca,'xtick',[]);
title(sprintf('Open-loop: $K_P \\cdot C_{PI} \\cdot C_D \\cdot G_{pos}$ ($\\gamma_M = %.1f^\\circ$)', pm_des));

bb = subplot(2,1,2);
semilogx(w_out, P_ol);
hold on;
semilogx(w_out, -180*ones(size(w_out)), '--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_regbot_bode_ol.png']);

%% ========================================================================
%  SECTION 9: Closed-Loop — Both Architectures
%  ========================================================================

% Lead in forward branch
G_cl_fwd = minreal(K_P*C_PI*C_D*G_pos / (1 + K_P*C_PI*C_D*G_pos));

% Lead in feedback branch (used for REGBOT)
G_cl_fb = minreal(K_P*C_PI*G_pos / (1 + K_P*C_PI*C_D*G_pos));

%% ========================================================================
%  SECTION 10: Step Response Comparison
%  ========================================================================

T_sim = 10;  % seconds

[y_fwd, t_fwd] = step(G_cl_fwd, 0:0.001:T_sim);
[y_fb,  t_fb]  = step(G_cl_fb,  0:0.001:T_sim);

figure(4); clf;
plot(t_fwd, y_fwd);
hold on;
plot(t_fb, y_fb);
plot(t_fb, ones(size(t_fb)), '--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'PI-Lead (forward)', 'PI-Lead (feedback)', 'Reference'}, ...
    'interpreter', 'latex', 'Location', 'southeast');
xlim([0 T_sim]);
saveas(gcf, [img_path 'day8_regbot_step.png']);

%% ========================================================================
%  SECTION 11: Step Response Info
%  ========================================================================

fprintf('\n=== Step Response Info ===\n');

si_fwd = stepinfo(G_cl_fwd);
fprintf('--- PI-Lead (forward) ---\n');
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', ...
    si_fwd.RiseTime, si_fwd.SettlingTime, si_fwd.Overshoot);

si_fb = stepinfo(G_cl_fb);
fprintf('--- PI-Lead (feedback) ---\n');
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', ...
    si_fb.RiseTime, si_fb.SettlingTime, si_fb.Overshoot);

%% ========================================================================
%  SECTION 12: Closed-Loop Bode — Both Architectures
%  ========================================================================

figure(5); clf;
bode(G_cl_fwd, G_cl_fb);
grid on;
legend({'PI-Lead (forward)', 'PI-Lead (feedback)'}, 'interpreter', 'latex');
title('Closed-loop Bode plot');
saveas(gcf, [img_path 'day8_regbot_bode_cl.png']);

bw_fwd = bandwidth(G_cl_fwd);
bw_fb  = bandwidth(G_cl_fb);
fprintf('\nBandwidth (forward):  %.2f rad/s\n', bw_fwd);
fprintf('Bandwidth (feedback): %.2f rad/s\n', bw_fb);

%% ========================================================================
%  SECTION 13: Steady-State Error Check
%  ========================================================================

ess = freqresp(s * (1/(1 + G_ol)) * (1/s), 0);
fprintf('\nSteady-state error: %.6f (should be ~0 for type-1 + PI)\n', abs(ess));

%% ========================================================================
%  SECTION 14: Print Controller Summary for REGBOT GUI
%  ========================================================================

fprintf('\n');
fprintf('============================================\n');
fprintf('  REGBOT CONTROLLER PARAMETERS\n');
fprintf('============================================\n');
fprintf('  K_P   = %.4f\n', K_P);
fprintf('  tau_i  = %.4f s  (PI zero: 1/tau_i = %.2f rad/s)\n', tau_i, 1/tau_i);
fprintf('  tau_d  = %.4f s  (Lead zero: 1/tau_d = %.2f rad/s)\n', tau_d, 1/tau_d);
fprintf('  alpha  = %.4f     (Lead pole: 1/(alpha*tau_d) = %.2f rad/s)\n', alpha, 1/(alpha*tau_d));
fprintf('  N_i    = %d\n', N_i);
fprintf('============================================\n');
fprintf('  Phase margin: %.2f deg\n', pm_des);
fprintf('  Crossover:    %.2f rad/s\n', wc_des);
fprintf('  Bandwidth:    %.2f rad/s (feedback arch.)\n', bw_fb);
fprintf('============================================\n');
