clear all;
clc;

s = tf('s');
G = 7.603/(s^2 + 11.35*s + 25.59); % To behave like 1st order LPF

w = linspace(1e-2,254,1000);        % Define frequency range for Bode plot

[M,P,w_out] = bode(G,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);

% Since we want first order system behaviour, we set gamma_M = 90 degrees
gamma_M = 90;
% Since we want first order system behaviour, we set omega_c = 1/tau
tau = 0.05;
omega_c = 1/tau;
i_c = find(w_out <= omega_c,1,'last');   % Get the index of the new cross-over frequency
phi_G = P(i_c);

% Choose Ni
N_i = 3;
phi_i = rad2deg(-atan(1/N_i));

phi_m = -180 + gamma_M - phi_i - phi_G;

% Find alpha
alpha = (1 - sin(deg2rad(phi_m)))/(1 + sin(deg2rad(phi_m)));
% In case phi_m is larger than 90 degrees, we need to add another LEad part
phi_m_2 = phi_m - rad2deg(asin((1 - alpha)/(1 + alpha)));
alpha_2 = (1 - sin(deg2rad(phi_m_2)))/(1 + sin(deg2rad(phi_m_2)));

% PI controller time constant and transfer function
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));

% P-Lead controller time constant and transfer function
tau_d = 1/(omega_c*sqrt(alpha));
tau_d_2 = 1/(omega_c*sqrt(alpha_2));
C_D_extra = minreal((tau_d_2*s + 1)/(alpha_2*tau_d_2*s + 1)); % 1 if phi_m < 90
C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1)*C_D_extra;

% Open-loop transfer function
G_ol = minreal(C_PI*C_D*G);

% P-controller gain
K_P = 1/abs(freqresp(G_ol,omega_c))
[M_ol,P_ol,w_out] = bode(K_P*G_ol,w);   % Get magnitude and phase of G_ol
M_ol = mag2db(squeeze(M_ol));
P_ol = squeeze(P_ol);

[M_PI,P_PI,w_out] = bode(C_PI,w);% PI controller transfer function
M_PI = mag2db(squeeze(M_PI));
P_PI = squeeze(P_PI);
[M_D,P_D,w_out] = bode(C_D,w);% P-Lead controller transfer function
M_D = mag2db(squeeze(M_D));
P_D = squeeze(P_D);

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

% Bode plots
figure(1);
a1 = subplot(2,1,1);
semilogx(w_out,M_ol,'Color',[84 130 15]./255);
hold on;
scatter(w_out(i_c),M_ol(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G_{ol} \vert$ in dB');
title('Open-loop Bode plot');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P_ol,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_c),P_ol(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
ylim([-275 0]);
linkaxes([a1,b1],'x');

%% Before control
figure(4);
a2 = subplot(2,1,1);
semilogx(w_out,M,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,M_PI,'--r');
semilogx(w_out,M_D,'Color',[4 145 245]./255,'lineStyle','--');
scatter(w_out(i_c),M(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
scatter(w_out(i_c),M_PI(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
scatter(w_out(i_c),M_D(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
set(gca,'xtick',[]);
title('Open-loop Bode plot');
legend({'$G(s)$' ,'$C_{PI}(s)$', '$C_D(s)$'},'interpreter','latex');

b2 = subplot(2,1,2);
semilogx(w_out,P,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,P_PI,'--r');
semilogx(w_out,P_D,'Color',[4 145 245]./255,'lineStyle','--');
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_c),P(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
scatter(w_out(i_c),P_PI(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
scatter(w_out(i_c),P_D(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
% ylim([-275 0]);
linkaxes([a2,b2],'x');

%% Step responses
T = 5.421; % Time to simulate for step responses
T_s = 0.001;
G_cl = K_P*G_ol/(1 + K_P*G_ol);                 % Closed-loop with P controller
[y,t] = step(G_cl,0:T_s:T);

G_cl_PI_Lead_fb = K_P*G*C_PI/(1 + K_P*G*C_PI*C_D); % Closed-loop with PI-Lead controller with the lead in the feedback branch
[y_PI_Lead_fb,t] = step(G_cl_PI_Lead_fb,0:T_s:T);
stepinfo(G_cl)
% Step response
figure(2);
plot(t,y);          % Plot step response of closed-loop with P controller
hold on;
plot(t,y_PI_Lead_fb);  % Plot step response of closed-loop with PI-Lead controller with the lead in the feedback branch
plot(t,ones(size(t)),'--k');    % Plot step reference
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'PI-Lead' ,'PI-Lead (feedback)'},'interpreter','latex');
xlim([0 T]);




