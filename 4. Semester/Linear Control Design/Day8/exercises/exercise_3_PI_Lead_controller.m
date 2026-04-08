clear all;
clc;

% Figure export path (Obsidian images folder)
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

s = tf('s');                        % Define complex variable
G = 40/((s + 1)*(s + 10)^2);       % System to control (type-0, stable)

w = linspace(1e-2,120,1000);        % Define frequency range for Bode plot
[M,P,w_out] = bode(G,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);

% Define Ni, alpha and gamma_M
N_i = 3;
alpha = 0.3;
gamma_M = 60;

% Phase contributions
phi_i = rad2deg(-atan(1/N_i));                  % PI phase contribution
phi_m = rad2deg(asin((1 - alpha)/(1 + alpha))); % Lead phase contribution
phi_G = -180 + gamma_M - phi_i - phi_m;         % Required plant phase

fprintf('PI phase contribution:   %.2f deg\n', phi_i);
fprintf('Lead phase contribution: %.2f deg\n', phi_m);
fprintf('Required plant phase:    %.2f deg\n', phi_G);

i_c = find(P <= phi_G,1);          % Index of new cross-over frequency
omega_c = w_out(i_c);              % New crossover frequency
fprintf('New crossover frequency: %.3f rad/s\n', omega_c);

% PI controller
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));
fprintf('PI: tau_i = %.4f s\n', tau_i);

% Lead controller
tau_d = 1/(omega_c*sqrt(alpha));
C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1);
fprintf('Lead: tau_d = %.4f s, alpha = %.2f\n', tau_d, alpha);

% Open-loop transfer function (without K_P)
G_ol = minreal(C_PI*C_D*G);

% P-controller gain
K_P = 1/abs(freqresp(G_ol,omega_c));
fprintf('K_P: %.4f\n', K_P);

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

% --- Figure 1: Component Bode plots (G, C_PI, C_D) ---
[M_pi,P_pi] = bode(C_PI,w);
M_pi = mag2db(squeeze(M_pi)); P_pi = squeeze(P_pi);
[M_cd,P_cd] = bode(C_D,w);
M_cd = mag2db(squeeze(M_cd)); P_cd = squeeze(P_cd);

figure(1); clf;
aa = subplot(2,1,1);
semilogx(w_out,M,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,M_pi,'r--');
semilogx(w_out,M_cd,'b-.');
scatter(w_out(i_c),M(i_c),25,'markerFaceColor','k','MarkerEdgeColor','k');
hold off;
grid on;
ylabel('$\vert \cdot \vert$ in dB');
set(gca,'xtick',[]);
legend({'$G(s)$','$C_{PI}(s)$','$C_D(s)$'},'interpreter','latex');

bb = subplot(2,1,2);
semilogx(w_out,P,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,P_pi,'r--');
semilogx(w_out,P_cd,'b-.');
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_c),P(i_c),25,'markerFaceColor','k','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle \cdot$ in deg');
ylim([-275 90]);
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_ex3_component_bode.png']);

% --- Figure 3: Open-loop Bode with full controller ---
[M_ol,P_ol,w_ol] = bode(K_P*G_ol,w);
M_ol = mag2db(squeeze(M_ol)); P_ol = squeeze(P_ol);

figure(3); clf;
aa = subplot(2,1,1);
semilogx(w_ol,M_ol);
hold on;
yline(0,'--k');
hold off;
grid on;
ylabel('$\vert G_{ol} \vert$ in dB');
set(gca,'xtick',[]);
title('Open-loop: $K_P \cdot C_{PI} \cdot C_D \cdot G$');

bb = subplot(2,1,2);
semilogx(w_ol,P_ol);
hold on;
semilogx(w_ol,-180*ones(size(w_ol)),'--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_ex3_bode_ol.png']);

% Verify margins
[gm,pm] = margin(K_P*G_ol);
fprintf('\nOpen-loop gain margin: %.2f dB\n', mag2db(gm));
fprintf('Open-loop phase margin: %.2f deg\n', pm);

%% Step responses
T = 5.4;

G_cl_P = K_P*G/(1 + K_P*G);                     % P only
[y_P,t] = step(G_cl_P,0:0.01:T);

G_cl_PI = K_P*G*C_PI/(1 + K_P*G*C_PI);          % PI only
[y_PI,t] = step(G_cl_PI,0:0.01:T);

G_cl = K_P*G_ol/(1 + K_P*G_ol);                 % PI-Lead (forward)
[y,t] = step(G_cl,0:0.01:T);

G_cl_fb = K_P*G*C_PI/(1 + K_P*G*C_PI*C_D);      % PI-Lead (feedback)
[y_fb,t] = step(G_cl_fb,0:0.01:T);

figure(2); clf;
plot(t,y);
hold on;
plot(t,y_fb);
plot(t,y_PI,':');
plot(t,y_P,':');
plot(t,ones(size(t)),'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'PI-Lead (forward)', 'PI-Lead (feedback)', 'PI', 'P', 'Reference'},...
    'interpreter','latex','Location','southeast');
xlim([0 T]);
saveas(gcf, [img_path 'day8_ex3_step.png']);

% --- Figure 4: Closed-loop Bode (both architectures) ---
figure(4); clf;
bode(G_cl, G_cl_fb);
grid on;
legend({'PI-Lead (forward)', 'PI-Lead (feedback)'},'interpreter','latex');
title('Closed-loop Bode plot');
saveas(gcf, [img_path 'day8_ex3_bode_cl.png']);

%% Step response info
fprintf('\n--- P controller ---\n');
si = stepinfo(G_cl_P);
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', si.RiseTime, si.SettlingTime, si.Overshoot);

fprintf('--- PI controller ---\n');
si = stepinfo(G_cl_PI);
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', si.RiseTime, si.SettlingTime, si.Overshoot);

fprintf('--- PI-Lead (forward) ---\n');
si = stepinfo(G_cl);
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', si.RiseTime, si.SettlingTime, si.Overshoot);

fprintf('--- PI-Lead (feedback) ---\n');
si = stepinfo(G_cl_fb);
fprintf('Rise time: %.4f s | Settling: %.4f s | Overshoot: %.2f%%\n', si.RiseTime, si.SettlingTime, si.Overshoot);

%% Steady-state errors
ess_P = freqresp(s*(1/(1 + K_P*G))*1/s, 0);
ess_PI_Lead = freqresp(s*(1/(1 + K_P*C_PI*C_D*G))*1/s, 0);
fprintf('\nSteady-state error (P):       %.4f\n', ess_P);
fprintf('Steady-state error (PI-Lead): %.4f\n', ess_PI_Lead);

%% Bandwidth comparison
bw_fwd = bandwidth(G_cl);
bw_fb = bandwidth(G_cl_fb);
fprintf('\nBandwidth (forward):  %.2f rad/s\n', bw_fwd);
fprintf('Bandwidth (feedback): %.2f rad/s\n', bw_fb);
