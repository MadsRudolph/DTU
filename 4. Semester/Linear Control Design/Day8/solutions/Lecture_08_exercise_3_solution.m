clear all;
clc;

s = tf('s');                        % Define complex variable
G = 40/((s + 1)*(s + 10)^2);        % System to control

w = linspace(1e-2,120,1000);        % Define frequency range for Bode plot

[M,P,w_out] = bode(G,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);
% Define Ni, alpha and gamma_M
N_i = 3;
alpha = 0.3;
gamma_M = 60;
% Define phase contributions from PI and P-Lead and phase of G at new
% cross-over frequency.
phi_i = rad2deg(-atan(1/N_i));
phi_m = rad2deg(asin((1 - alpha)/(1 + alpha)));
phi_G = -180 + gamma_M - phi_i - phi_m;

i_c = find(P <= phi_G,1);   % Get the index of the new cross-over frequency
omega_c = w_out(i_c);       % Get omega_c

% PI controller time constant and transfer function
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));

% P-Lead controller time constant and transfer function
tau_d = 1/(omega_c*sqrt(alpha));
C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1);

% Open-loop transfer function
G_ol = minreal(C_PI*C_D*G);

% P-controller gain
K_P = 1/abs(freqresp(G_ol,omega_c));

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

% Bode plots
figure(1);
aa = subplot(2,1,1);
semilogx(w_out,M,'Color',[84 130 15]./255);
hold on;
scatter(w_out(i_c),M(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
set(gca,'xtick',[]);

bb = subplot(2,1,2);
semilogx(w_out,P,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_c),P(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
ylim([-275 0]);
linkaxes([aa,bb],'x');

T = 5.4; % Time to simulate for step responses
G_cl_P = K_P*G/(1 + K_P*G);                     % Closed-loop with P controller
[y_P,t] = step(G_cl_P,0:0.01:T);

G_cl_PI = K_P*G*C_PI/(1 + K_P*G*C_PI);          % Closed-loop with PI controller
[y_PI,t] = step(G_cl_PI,0:0.01:T);

G_cl = K_P*G_ol/(1 + K_P*G_ol);                 % Closed-loop with PI-Lead controller with the lead in the forward branch
[y,t] = step(G_cl,0:0.01:T);

G_cl_PI_Lead = K_P*G*C_PI/(1 + K_P*G*C_PI*C_D); % Closed-loop with PI-Lead controller with the lead in the feedback branch
[y_PI_Lead,t] = step(G_cl_PI_Lead,0:0.01:T);

% Step response
figure(2);
plot(t,y);          % Plot step response of closed-loop with P controller
hold on;
plot(t,y_PI,':');   % Plot step response of closed-loop with PI controller
plot(t,y_P,':');    % Plot step response of closed-loop with PI-Lead controller
plot(t,y_PI_Lead);  % Plot step response of closed-loop with PI-Lead controller with the lead in the feedback branch
plot(t,ones(size(t)),'--k');    % Plot step reference
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'PI-Lead' ,'PI', 'P', 'PI-Lead (feedback)'},'interpreter','latex');
xlim([0 T]);
