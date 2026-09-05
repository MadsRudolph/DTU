clear all;
clc;

s = tf('s');                          % Define the complex variable s
G = 178/((s + 1)*(0.003*s + 1));      % Define the transfer function
H = 1/(0.0009*s + 1);

gamma_M = deg2rad(70);
w = linspace(1e-2,1000,100000);       % Define frequency range for Bode plot
[M,P,w_out] = bode(G*H,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);

alpha = 0.1;
N_i = 5;

phi_i = atan(-1/N_i);
phi_m = asin((1 - alpha)/(1 + alpha));
phi_G = rad2deg((-pi + gamma_M - phi_i - phi_m));

i_c = find(P <= phi_G,1,'first');
omega_c = w_out(i_c);

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

% PI controller time constant and transfer function
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));
[num_PI,den_PI] = tfdata(C_PI,'v');
% P-Lead controller time constant and transfer function
tau_d = 1/(omega_c*sqrt(alpha));
C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1);
[num_D,den_D] = tfdata(C_D,'v');
% Open-loop transfer function
G_ol = minreal(C_PI*C_D*G*H);
% P-controller gain
K_P = 1/abs(freqresp(G_ol,omega_c));

[M_ol,P_ol,w_out] = bode(K_P*G_ol,w);   % Get magnitude and phase of G_ol
M_ol = mag2db(squeeze(M_ol));
P_ol = squeeze(P_ol);

% Bode plots
figure(2);
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
xlim([w_out(1) 1e3]);

%% Simulation
simTime = 2.5;  % Simulation time
r = [0.1 5 25 254]; % Different values for reference signal
for i = 1:size(r,2)
    % Plot simulation outpus and control signals for every reference case
    step_size = r(i);
    out = sim('saturated_systems_example');
    figure(3);
    subplot(2,2,i)
    plot(out.y.Time,out.y.Data);
    hold on;
    plot(out.r.Time,out.r.Data,'--k');
    hold off;
    grid on;
    xlabel('$t$ in s');
    ylabel('$r(t),y(t)$');
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));
    legend({'$y(t)$','$r(t)$'},'interpreter','latex');
    
    figure(4);
    aa = subplot(2,2,i);
    plot(out.u.Time,out.u.Data,'Color',[4 145 245]./255);
    hold on;
    plot(out.u_sat.Time,out.u_sat.Data,'Color',[84 130 15]./255);
    hold off;
    grid on;
    xlabel('$t$ in s');
    ylabel('$u(t)$');
    legend({'$u(t)$','$u_{sat}(t)$'},'interpreter','latex');
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));
    xlim([0 0.2]);
end

step_size = 25;
out = sim('saturated_systems_example');
figure(5);
aa = subplot(2,1,1);
plot(out.u.Time,out.u.Data,'Color',[4 145 245]./255);
hold on;
plot(out.u_sat.Time,out.u_sat.Data,'Color',[84 130 15]./255);
plot(out.P_Lead.Time,out.P_Lead.Data,'Color',[54 245 45]./255);
plot(out.I.Time,out.I.Data,'--r');
hold off;
grid on;
ylabel('$u(t)$');
legend({'$u(t)$','$u_{sat}(t)$','$u_{P-Lead}(t)$','$u_I(t)$'},'interpreter','latex');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));

bb = subplot(2,1,2);
plot(out.y.Time,out.y.Data);
hold on;
plot(out.r.Time,out.r.Data,'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$r(t),y(t)$');
legend({'$y(t)$','$r(t)$'},'interpreter','latex');
linkaxes([aa,bb],'x');
xlim([0.075 0.25]);

%% Windup mitigation
% Lag instead of I
beta = 10;
C_L = (tau_i*s + 1)/(tau_i*s+ 1/beta);
[num_L,den_L] = tfdata(C_L,'v');

% Pre-filter
tau_f = 0.07; % similar to the rise time
G_filt = 1/(tau_f*s + 1);
[num_f,den_f] = tfdata(G_filt,'v');

% Limited integrator
int_lim = 3.5;

% Anti-windup
K_a = 2;

out = sim('saturated_systems_mitigation_example');
figure(5);
aa = subplot(2,1,1);
plot(out.y.Time,out.y.Data);
hold on;
plot(out.y.Time,out.y_lag.Data);
plot(out.y.Time,out.y_filt.Data);
plot(out.y.Time,out.y_l.Data);
plot(out.y.Time,out.y_awp.Data);
plot(out.r.Time,out.r.Data,'--k');
hold off;
grid on;
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));
legend({'$y(t)$','Lag','Pre-filter','Limited I','Anti-windup','$r(t)$'},'interpreter','latex');

bb = subplot(2,1,2);
plot(out.u.Time,out.u.Data);
hold on;
plot(out.u.Time,out.u_sat_lag.Data);
plot(out.u.Time,out.u_sat_filt.Data);
plot(out.u.Time,out.u_sat_l.Data);
plot(out.u.Time,out.u_sat_awp.Data);
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
legend({'$u_{sat}(t)$','Lag','Pre-filter','Limited I','Anti-windup'},'interpreter','latex');
linkaxes([aa,bb],'x');
xlim([0.075 0.52]);

%% Different values of beta
Beta = [1 2 10 50];
legend_c = string(Beta);
for i = 1:length(Beta)
    beta = Beta(i);
    C_L = (tau_i*s + 1)/(tau_i*s+ 1/beta);
    [num_L,den_L] = tfdata(C_L,'v');
    legend_c(i) = strcat(['$\beta = ', num2str(beta),'$']);
    out = sim('saturated_systems_mitigation_example');
    figure(6);
    aa = subplot(2,1,1);
    plot(out.y.Time,out.y_lag.Data);
    hold on;
    
    bb = subplot(2,1,2);
    plot(out.y.Time,out.u_sat_lag.Data);
    hold on;
end
figure(6);
aa = subplot(2,1,1);
plot(out.r.Time,out.r.Data,'--k');
hold off;
grid on;
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));
legend(([legend_c,'$r(t)$']),'interpreter','latex');

bb = subplot(2,1,2);
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
linkaxes([aa,bb],'x');
xlim([0.075 0.25]);

%% Different values of tau_f
tau_F = [0.01 0.02 0.05 0.1];
legend_c = string(tau_F);
for i = 1:length(tau_F)
    tau_f = tau_F(i);
    G_filt = 1/(tau_f*s + 1);
    [num_f,den_f] = tfdata(G_filt,'v');
    legend_c(i) = strcat(['$\tau_f = ', num2str(tau_f),'$ s']);
    out = sim('saturated_systems_mitigation_example');
    figure(7);
    aa = subplot(2,1,1);
    plot(out.y.Time,out.y_filt.Data);
    hold on;
    
    bb = subplot(2,1,2);
    plot(out.y.Time,out.u_sat_filt.Data);
    hold on;
end
figure(7);
aa = subplot(2,1,1);
plot(out.r.Time,out.r.Data,'--k');
hold off;
grid on;
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));
legend(([legend_c,'$r(t)$']),'interpreter','latex');

bb = subplot(2,1,2);
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
linkaxes([aa,bb],'x');
xlim([0.075 0.75]);

%% Different values of int_lim
int_limit = [0.1 0.5 2.5 4];
legend_c = string(int_limit);
for i = 1:length(int_limit)
    int_lim = int_limit(i);
    legend_c(i) = strcat(['$\pm', num2str(int_lim),'$']);
    out = sim('saturated_systems_mitigation_example');
    figure(8);
    aa = subplot(2,1,1);
    plot(out.y.Time,out.y_l.Data);
    hold on;
    
    bb = subplot(2,1,2);
    plot(out.y.Time,out.u_sat_l.Data);
    hold on;
end
figure(8);
aa = subplot(2,1,1);
plot(out.r.Time,out.r.Data,'--k');
hold off;
grid on;
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));
legend(([legend_c,'$r(t)$']),'interpreter','latex');

bb = subplot(2,1,2);
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
linkaxes([aa,bb],'x');
xlim([0.075 0.25]);

%% Different values of K_a
K_A = [1 2 5 25];
legend_c = string(K_A);
for i = 1:length(K_A)
    K_a = K_A(i);
    legend_c(i) = strcat(['$K_a = ', num2str(K_a),'$']);
    out = sim('saturated_systems_mitigation_example');
    figure(9);
    aa = subplot(2,1,1);
    plot(out.y.Time,out.y_awp.Data);
    hold on;
    
    bb = subplot(2,1,2);
    plot(out.y.Time,out.u_sat_awp.Data);
    hold on;
end
figure(9);
aa = subplot(2,1,1);
plot(out.r.Time,out.r.Data,'--k');
hold off;
grid on;
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(step_size),'}{s}$']));
legend(([legend_c,'$r(t)$']),'interpreter','latex');

bb = subplot(2,1,2);
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
linkaxes([aa,bb],'x');
xlim([0.075 0.25]);
