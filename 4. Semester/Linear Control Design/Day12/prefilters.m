clear all;
clc;

s = tf('s');
G = (s + 1)/(s^2 + 25); % System transfer function
H = 1/(0.1*s + 1);      % Sensor transfer function

% PI controller
K_P = 13.1;
tau_i = 0.2;
C_PI = (tau_i*s + 1)/(tau_i*s);

% Open-loop transfer function
G_ol = minreal(K_P*C_PI*G*H);

% Closed-loop transfer function
G_cl = minreal(K_P*C_PI*G/(1 + G_ol));

% Bode plots
w = linspace(1e-2,254,10000);        % Define frequency range for Bode plot
[M_cl,P_cl,w_out] = bode(G_cl,w);
M_cl = mag2db(squeeze(M_cl));
P_cl = squeeze(P_cl);

i_peak = find(M_cl == max(M_cl),1,'first');
omega_peak = w_out(i_peak);
M_peak = db2mag(M_cl(i_peak));

% First order pre-filter
tau_f = sqrt(M_peak^2 - 1)/omega_peak;
G_f = 1/(tau_f*s + 1);

[M_f,P_f,w_out] = bode(G_f,w);
M_f = mag2db(squeeze(M_f));
P_f = squeeze(P_f);

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(1);
a1 = subplot(2,1,1);
semilogx(w_out,M_cl);
hold on;
semilogx(w_out,M_f,'Color',[84 130 15]./255,'lineStyle','--');
semilogx(w_out,M_cl + M_f,'Color',[4 145 245]./255,'lineStyle','-');
hold off;
grid on;
ylabel('$\vert G_{cl} \vert$ in dB');
title('Closed-loop Bode plot');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P_cl);
hold on;
semilogx(w_out,P_f,'Color',[84 130 15]./255,'lineStyle','--');
semilogx(w_out,P_cl + P_f,'Color',[4 145 245]./255,'lineStyle','-');
semilogx(w_out,-180*ones(size(w_out)),'--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{cl}$ in deg');
legend({'$G_{cl}(s)$','$G_f(s)$','$G_f(s)G_{cl}(s)$'},'interpreter','latex');
linkaxes([a1,b1],'x');
xlim([w_out(1) w_out(end)]);

% Step plots
T = 5.421; % Time to simulate for step responses
T_s = 0.001;

[y,t] = step(G_cl,0:T_s:T);
stepinfo(G_cl)

G_cl_f = G_f*G_cl; % Closed-loop with pre-filter
[y_f,t] = step(G_cl_f,0:T_s:T);
stepinfo(G_cl_f)

% Plot step response of closed-loop
figure(2);
plot(t,y);
hold on;
plot(t,y_f);  % Plot step response of closed-loop systems
plot(t,ones(size(t)),'--k');    % Plot step reference
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'$G_{cl}(s)$' ,'$G_f(s)G_{cl}(s)$'},'interpreter','latex');
xlim([0 T]);

%% Higher-order pre filters
% Find the valey point before the peak
I_val = find(w_out < omega_peak);
i_v = find(M_cl(I_val) == min(M_cl(I_val)));
omega_v = w_out(i_v);

% Lead controller as G_L
M_lead_v = 1/db2mag(M_cl(i_v));
alpha = 1/M_lead_v^2;
tau_d = 1/(omega_v*sqrt(alpha));
G_L = (tau_d*s + 1)/(alpha*tau_d*s + 1);
[M_L,P_L,w_out] = bode(G_L,w);
M_L = mag2db(squeeze(M_L));
P_L = squeeze(P_L);

% Peak eliminator
p = -11; % Choose poles faster than the fastest zeros of G_cl
G_P_1 = p^2/(s - p)^2;
M_P_1 = abs(freqresp(G_P_1,omega_peak*1i)); % Contribution from G_P_1

M_peak_new = db2mag(M_cl(i_peak) + M_L(i_peak));
zeta = 1/(2*M_peak_new*M_P_1);
G_P = minreal((s^2 + 2*zeta*omega_peak*s + omega_peak^2)/omega_peak^2*G_P_1)
[M_P,P_P,w_out] = bode(G_P,w);
M_P = mag2db(squeeze(M_P));
P_P = squeeze(P_P);

%% Bode plots G_cl,G_L,G_L*G_cl
figure(3);
a1 = subplot(2,1,1);
semilogx(w_out,M_cl);
hold on;
semilogx(w_out,M_L,'Color',[84 130 15]./255,'lineStyle','--');
semilogx(w_out,M_cl + M_L,'Color',[4 145 245]./255,'lineStyle','-');
hold off;
grid on;
ylabel('$\vert G_{cl} \vert$ in dB');
title('Closed-loop Bode plot');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P_cl);
hold on;
semilogx(w_out,P_L,'Color',[84 130 15]./255,'lineStyle','--');
semilogx(w_out,P_cl + P_L,'Color',[4 145 245]./255,'lineStyle','-');
semilogx(w_out,-180*ones(size(w_out)),'--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{cl}$ in deg');
legend({'$G_{cl}(s)$','$G_L(s)$','$G_L(s)G_{cl}(s)$'},'interpreter','latex');
linkaxes([a1,b1],'x');
xlim([w_out(1) w_out(end)]);

%% Bode plots G_cl,G_L*G_cl,G_P,G_L*G_P*G_cl
figure(4);
a1 = subplot(2,1,1);
semilogx(w_out,M_cl + M_L);
hold on;
semilogx(w_out,M_P,'Color',[84 130 15]./255,'lineStyle','--');
semilogx(w_out,M_cl + M_L + M_P,'Color',[4 145 245]./255,'lineStyle','-');
hold off;
grid on;
ylabel('$\vert G_{cl} \vert$ in dB');
title('Closed-loop Bode plot');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P_cl + P_L);
hold on;
semilogx(w_out,P_P,'Color',[84 130 15]./255,'lineStyle','--');
semilogx(w_out,P_cl + P_L + P_P,'Color',[4 145 245]./255,'lineStyle','-');
semilogx(w_out,-180*ones(size(w_out)),'--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{cl}$ in deg');
legend({'$G_L(s)G_{cl}(s)$','$G_P(s)$','$G_L(s)G_P(s)G_{cl}(s)$'},'interpreter','latex');
linkaxes([a1,b1],'x');
xlim([w_out(1) w_out(end)]);

%% Step responses
G_cl_PL = G_L*G_P*G_cl; % Closed-loop with pre-filter
[y_LP,t] = step(G_cl_PL,0:T_s:T);
stepinfo(G_cl_PL)

% Plot step response of closed-loop
figure(5);
plot(t,y,':');
hold on;
plot(t,y_f);        % With first-order pre-filter
plot(t,y_LP,'b');   % With LEad pre-filter and peak eliminator
plot(t,ones(size(t)),'--k');    % Plot step reference
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'$G_{cl}(s)$' ,'$G_f(s)G_{cl}(s)$','$G_L(s)G_P(s)G_{cl}(s)$'},'interpreter','latex');
xlim([0 T]);