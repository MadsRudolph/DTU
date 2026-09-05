clear all;
clc;

s = tf('s');                            % Define the complex variable s
G = 900/((s + 1)*(s^2 + 50*s + 900));   % Define the transfer function

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

out = sim('rate_limited_systems');      % Run the model in Simulink

for i = 1:size(out.y.Data,2)            % Plot all the outputs
    figure(i);
    plot(out.y.Time,out.y.Data(:,i));
    hold on;
    plot(out.u.Time,out.u2.Data(:,i));
    plot(out.u.Time,out.u.Data(:,i),'--k');
    hold off;
    grid on;
    xlabel('$t$ in s');
    ylabel('$u(t),y(t)$');
    legend({'$y(t)$','$u_2(t)$','$u(t)$'},'interpreter','latex');
    title(strcat(['$u(s) = \displaystyle \frac{',num2str(out.u.Data(100,i)),'}{s}$']));
end

figure(45);
plot(out.y.Time,out.y.Data(:,i));
hold on;
plot(out.y_2.Time,out.y_2.Data,'Color',[84 130 15]./255);
plot(out.u.Time,out.u.Data(:,i),'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$u(t),y(t)$');
legend({'$y(t)$','$y_{unlim}(t)$','$u(t)$'},'interpreter','latex');
title(strcat(['$u(s) = \displaystyle \frac{',num2str(out.u.Data(100,i)),'}{s}$']));



%% PI-Lead controller design
N_i = 3;
alpha = 0.1;
gamma_M = deg2rad(60);
w = linspace(1e-2,254,10000);       % Define frequency range for Bode plot
[M,P,w_out] = bode(G,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);

phi_i = atan(-1/N_i);
phi_m = asin((1 - alpha)/(1 + alpha));
phi_G = rad2deg((-pi + gamma_M - phi_i - phi_m));

i_c = find(P <= phi_G,1,'first');
omega_c = w_out(i_c);

% PI controller time constant and transfer function
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));
[num_PI,den_PI] = tfdata(C_PI,'v');
% P-Lead controller time constant and transfer function
tau_d = 1/(omega_c*sqrt(alpha));
C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1);
[num_D,den_D] = tfdata(C_D,'v');
% Open-loop transfer function
G_ol = minreal(C_PI*C_D*G);
% P-controller gain
K_P = 1/abs(freqresp(G_ol,omega_c));

[M_ol,P_ol,w_out] = bode(K_P*G_ol,w);   % Get magnitude and phase of G_ol
M_ol = mag2db(squeeze(M_ol));
P_ol = squeeze(P_ol);

% Bode plots
figure(6);
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
ylim([-275 0]);
linkaxes([a1,b1],'x');

simTime = 25;   % Set Simulation time
out = sim('rate_limited_systems_controller_design'); % Run the model

for i = 1:size(out.y.Data,2)-1  % Plot the first five output cases
    figure(54);
    subplot(2,2,i);
    plot(out.y.Time,out.y.Data(:,i));
    hold on;
    plot(out.r.Time,out.r.Data(:,i),'--k');
    hold off;
    grid on;
    if (i > 2)
        xlabel('$t$ in s');
    end
    ylabel('$r(t),y(t)$');
    if (i == 2)
        legend({'$y(t)$','$r(t)$'},'interpreter','latex');
    end
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(100,i)),'}{s}$']));
end

for i = 1:size(out.y.Data,2)-1 % Plot the first five input cases
    figure(12);
    aa = subplot(2,2,i);
    plot(out.u.Time,out.u.Data(:,i),'Color',[84 130 15]./255);
    hold on;
    plot(out.u_l.Time,out.u_l.Data(:,i),'Color',[4 145 245]./255);
    hold off;
    grid on;
    if (i > 2)
        xlabel('$t$ in s');
    end
    ylabel('$u(t)$');
    if (i == 2)
        legend({'$u(t)$','$u_{unlim}(t)$'},'interpreter','latex');
    end
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(100,i)),'}{s}$']));
%     magnifyOnFigure(aa);
end

%% Controller re-design
p = pole(G);
i_dp = find(real(p) == max(real(p)),1); % Find the dominant pole
d_pole = p(i_dp);
omega_dp = abs(real(d_pole));
omega_c = 4;
i_c = find(w_out <= omega_c,1,'last');  % Index for crossover frequency
i_d = find(w_out >= omega_dp,1,'first');% Index for dominant pole

% Bode plots
figure(8);
a1 = subplot(2,1,1);
semilogx(w_out,M,'Color',[84 130 15]./255);
hold on;
scatter(w_out(i_d),M(i_d),25,'markerFaceColor','k','MarkerEdgeColor',' k');
scatter(w_out(i_c),M(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
title('System Bode plot');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_d),P(i_d),25,'markerFaceColor','k','MarkerEdgeColor',' k');
scatter(w_out(i_c),P(i_c),25,'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
ylim([-275 0]);
linkaxes([a1,b1],'x');


% PI controller time constant and transfer function
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));
[num_PI,den_PI] = tfdata(C_PI,'v');
% P-Lead controller time constant and transfer function
tau_d = 1/(omega_c*sqrt(alpha));
C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1);
[num_D,den_D] = tfdata(C_D,'v');
% Open-loop transfer function
G_ol = minreal(C_PI*C_D*G);
% P-controller gain
K_P = 1/abs(freqresp(G_ol,omega_c));

[M_ol,P_ol,w_out] = bode(K_P*G_ol,w);   % Get magnitude and phase of G_ol
M_ol = mag2db(squeeze(M_ol));
P_ol = squeeze(P_ol);

% Bode plots
figure(6);
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
ylim([-275 0]);
linkaxes([a1,b1],'x');

simTime = 25;
out = sim('rate_limited_systems_controller_design');
% Plot simulation outpus and control signals
for i = 1:size(out.y.Data,2)-1
    figure(54);
    subplot(2,2,i);
    plot(out.y.Time,out.y.Data(:,i));
    hold on;
    plot(out.r.Time,out.r.Data(:,i),'--k');
    hold off;
    grid on;
    if (i > 2)
        xlabel('$t$ in s');
    end
    ylabel('$r(t),y(t)$');
    if (i == 2)
        legend({'$y(t)$','$r(t)$'},'interpreter','latex');
    end
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(100,i)),'}{s}$']));
end

for i = 1:size(out.y.Data,2)-1
    figure(12);
    subplot(2,2,i);
    plot(out.u.Time,out.u.Data(:,i),'Color',[84 130 15]./255);
    hold on;
    plot(out.u_l.Time,out.u_l.Data(:,i),'Color',[4 145 245]./255);
    hold off;
    grid on;
    if (i > 2)
        xlabel('$t$ in s');
    end
    ylabel('$u(t)$');
    if (i == 2)
        legend({'$u(t)$','$u_{unlim}(t)$'},'interpreter','latex');
    end
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(100,i)),'}{s}$']));
end

%% Test different omega_c
w_c = [1.5 2 2.5 3 4 5];
legend_c = string(w_c);
for i = 1:length(w_c)
   omega_c = w_c(i);
   % PI controller time constant and transfer function
    tau_i = N_i/omega_c;
    C_PI = (1 + 1/(tau_i*s));
    [num_PI,den_PI] = tfdata(C_PI,'v');
    % P-Lead controller time constant and transfer function
    tau_d = 1/(omega_c*sqrt(alpha));
    C_D = (tau_d*s + 1)/(alpha*tau_d*s + 1);
    [num_D,den_D] = tfdata(C_D,'v');
    % Open-loop transfer function
    G_ol = minreal(C_PI*C_D*G);
    % P-controller gain
    K_P = 1/abs(freqresp(G_ol,omega_c));
    
    simTime = 25;
    out = sim('rate_limited_systems_controller_design');
    
    figure(25);
    plot(out.y.Time,out.y.Data(:,4));
    hold on;
    legend_c(i) = strcat(['$\omega_c = ', num2str(omega_c),'$ rad/s']);
end
figure(25);
plot(out.r.Time,out.r.Data(:,4),'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(100,4)),'}{s}$']));
legend(legend_c,'interpreter','latex');
