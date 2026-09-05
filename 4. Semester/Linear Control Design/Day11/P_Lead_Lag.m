clear all;
clc;

s = tf('s');                        % Define complex variable
w = linspace(1e-1,100,10000);        % Define frequency range for Bode plot

G = 5000*(s + 7)*(s + 12)/((s + 4)*(s + 9)*(s + 17)*(s + 5)*(s + 70));
gamma_M = 70;
alpha = 0.2;                        % Define alpha
Beta = 2;                           % Define beta
N_i = 3;
[M,P,w_out] = bode(G,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);
phi_m = rad2deg(asin((1 - alpha)/(1 + alpha)));
phi_L = rad2deg(atan(N_i*(1 - Beta)/(1 + Beta*N_i^2)));
phi_G = -180 + gamma_M - phi_m - phi_L;

i_c = find(P <= phi_G,1,'first');   % Get index for new crossover frequency
omega_c = w_out(i_c);               % Crossover frequency
tau_i = N_i/omega_c;                % P-Lag zero location (as time constant)
tau_d = 1/(omega_c*sqrt(alpha));    % P-Lead zero location (as time constant)
C_L = (tau_i*s + 1)/(tau_i*s + 1/Beta);     % P-Lag transfer function
C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1);    % P-Lead transfer function
G_ol = minreal(C_D*C_L*G);   % Open-loop transfer function (no gain)

K_P = 1/abs(freqresp(G_ol,omega_c*1i));  % Calculate K_P
[M_ol,P_ol,w_out] = bode(K_P*G_ol,w);   % Get magnitude and phase of G_ol
M_ol = mag2db(squeeze(M_ol));
P_ol = squeeze(P_ol);

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(1);
a1 = subplot(2,1,1);
semilogx(w_out,M,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,M_ol,'Color',[4 145 245]./255);
scatter(w_out(i_c),M_ol(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G_{ol} \vert$ in dB');
title('Open-loop Bode plot');
legend({'$G(s)$','$G_{ol}(s)$'},'interpreter','latex');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,P_ol,'Color',[4 145 245]./255);
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_c),P_ol(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
linkaxes([a1,b1],'x');

%% Step responses
T = 5.421; % Time to simulate for step responses
T_s = 0.001;
step_size = 1;
G_cl = minreal(step_size*K_P*G_ol/(1 + K_P*G_ol));                 % Closed-loop with P controller
[y,t] = step(G_cl,0:T_s:T);
G_ue_P_Lead_Lag = minreal(K_P*C_L*C_D);
u_P_Lead_Lag = lsim(G_ue_P_Lead_Lag,step_size - y,t);

G_cl_P = K_P*G/(1 + K_P*G); % Closed-loop with P controller
[y_P,t] = step(step_size*G_cl_P,0:T_s:T);
G_ue_P = K_P*tf(1);
u_P = lsim(G_ue_P,step_size - y_P,t);

C_PI = (tau_i*s + 1)/(tau_i*s);
G_cl_PI_Lead = minreal(K_P*C_PI*C_D*G/(1 + K_P*C_PI*C_D*G)); %Closed-loop with PI-Lead controller
[y_PI_LEad,t] = step(step_size*G_cl_PI_Lead,0:T_s:T);
G_ue_PI_LEad = minreal(K_P*C_PI*C_D);
u_PI_LEad = lsim(G_ue_PI_LEad,step_size - y_PI_LEad,t);


% Step response
figure(2);
cc = subplot(2,1,1);
plot(t,y);    % Plot control usage for PI-Lead_Lag controller
hold on;
plot(t,y_P);  % Plot control usage for P controller
plot(t,y_PI_LEad);  % Plot control usage for PI-Lead controller
plot(t,step_size*ones(size(t)),'--k');    % Plot step reference
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'P-Lead-Lag' ,'P','PI-Lead'},'interpreter','latex');
xlim([0 T]);
% ylim([0 1.1]);

dd = subplot(2,1,2);
plot(t,u_P_Lead_Lag);    % Plot PI-Lead_Lag controller output
hold on;
plot(t,u_P);  % Plot step response of closed-loop with P controller
plot(t,u_PI_LEad);  % Plot step response of closed-loop with PI-Lead controller with the lead in the feedback branch
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
title('Control usage');
% legend({'P-Lead-Lag (feedback)' ,'P','PI-Lead'},'interpreter','latex');
xlim([0 T]);
% ylim([0 1.1]);
magnifyOnFigure(dd);

