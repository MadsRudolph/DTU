clear all;
clc;

% Figure export path (Obsidian images folder)
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

s = tf('s');                        % Define complex variable
G = 3.3/(s^3 + 5*s^2 + 2.1*s + 1); % System to control (type-0)
p = pole(G);                        % Find the poles of G
fprintf('Poles of G(s): '); disp(p');

w = linspace(1e-2,120,1000);        % Define frequency range for Bode plot
[M,P,w_out] = bode(G,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);

% Define Ni and gamma_M
N_i = 3;
gamma_M = 60;

% Phase contributions
phi_i = rad2deg(-atan(1/N_i));              % PI phase contribution at omega_c
phi_G = -180 + gamma_M - phi_i;            % Required plant phase at omega_c

fprintf('PI phase contribution: %.2f deg\n', phi_i);
fprintf('Required plant phase at omega_c: %.2f deg\n', phi_G);

i_c = find(P <= phi_G,1,'first');           % Index of new cross-over frequency
omega_c = w_out(i_c);                       % New crossover frequency
fprintf('New crossover frequency: %.3f rad/s\n', omega_c);

% PI controller time constant and transfer function
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));
fprintf('PI time constant tau_i: %.4f s\n', tau_i);

% Open-loop transfer function (without K_P)
G_ol = minreal(C_PI*G);

% P-controller gain (set magnitude to 0 dB at omega_c)
K_P = 1/abs(freqresp(G_ol,omega_c));
fprintf('K_P: %.4f\n', K_P);

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

% Bode plot of G(s) with crossover point
figure(1); clf;
aa = subplot(2,1,1);
semilogx(w_out,M,'Color',[84 130 15]./255);
hold on;
scatter(w_out(i_c),M(i_c),25,'markerFaceColor','k','MarkerEdgeColor','k');
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
semilogx(w_out,P,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');
semilogx(w_out,phi_G*ones(size(w_out)),'--r');
scatter(w_out(i_c),P(i_c),25,'markerFaceColor','k','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
ylim([-275 0]);
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_ex2_bode.png']);

% Bode plot of open-loop with controller
[M_ol,P_ol,w_ol] = bode(K_P*G_ol,w);
M_ol = mag2db(squeeze(M_ol));
P_ol = squeeze(P_ol);

figure(3); clf;
aa = subplot(2,1,1);
semilogx(w_ol,M_ol);
hold on;
yline(0,'--k');
hold off;
grid on;
ylabel('$\vert G_{ol} \vert$ in dB');
set(gca,'xtick',[]);
title('Open-loop: $K_P \cdot C_{PI} \cdot G$');

bb = subplot(2,1,2);
semilogx(w_ol,P_ol);
hold on;
semilogx(w_ol,-180*ones(size(w_ol)),'--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_ex2_bode_ol.png']);

%% Step responses
T = 54;

G_cl = K_P*G/(1 + K_P*G);                 % Closed-loop with P controller
[y,t] = step(G_cl,0:0.01:T);

G_cl_PI = K_P*G*C_PI/(1 + K_P*G*C_PI);    % Closed-loop with PI controller
[y_PI,t] = step(G_cl_PI,0:0.01:T);

figure(2); clf;
plot(t,y_PI);
hold on;
plot(t,y,':');
plot(t,ones(size(t)),'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'PI', 'P', 'Reference'},'interpreter','latex');
xlim([0 T]);
saveas(gcf, [img_path 'day8_ex2_step.png']);

%% Step response info
fprintf('\n--- P controller ---\n');
si_P = stepinfo(G_cl);
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', si_P.RiseTime, si_P.SettlingTime, si_P.Overshoot);

fprintf('\n--- PI controller ---\n');
si_PI = stepinfo(G_cl_PI);
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', si_PI.RiseTime, si_PI.SettlingTime, si_PI.Overshoot);

%% Steady-state errors
G_e_P = minreal(1/(1 + K_P*G));
G_e_PI = minreal(1/(1 + K_P*C_PI*G));
ess_P = freqresp(s*G_e_P*1/s,0);
ess_PI = freqresp(s*G_e_PI*1/s,0);
fprintf('\nSteady-state error (P):  %.4f\n', ess_P);
fprintf('Steady-state error (PI): %.4f\n', ess_PI);
