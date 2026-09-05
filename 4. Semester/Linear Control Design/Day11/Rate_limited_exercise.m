clear all;
clc;

s = tf('s');        % Define the complex variable s
G = 5/(10*s + 1);   % Define the transfer function

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

%% PI-Lead controller design
N_i = 2;
alpha = 0.1;
w = linspace(1e-2,254,10000);       % Define frequency range for Bode plot

p = pole(G);
i_dp = find(real(p) == max(real(p)),1);
d_pole = p(i_dp);
omega_dp = abs(real(d_pole));

t_r = 10;
omega_c = 3;

[M,P,w_out] = bode(G,w);            % Get magnitude and phase of G
M = mag2db(squeeze(M));
P = squeeze(P);

i_c = find(w_out <= omega_c,1,'last');
i_d = find(w_out >= omega_dp,1,'first');

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

% Bode plots of original system and open-loop system
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
out = sim('rate_limited_systems_exercise');
% Plot simulation outpus and control signals
for i = 1:size(out.y.Data,2)
    figure(54);
    subplot(2,1,i);
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
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(50,i)),'}{s}$']));
end

for i = 1:size(out.y.Data,2)
    figure(12);
    subplot(2,1,i);
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
    title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(50,i)),'}{s}$']));
end

%% Test different omega_c
w_c = [1.5 2 2.5 3 4];
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
    out = sim('rate_limited_systems_exercise');
    
    figure(25);
    aa = subplot(2,1,1);
    plot(out.y.Time,out.y.Data(:,1));
    hold on;
    
    bb = subplot(2,1,2);
    plot(out.y.Time,out.y.Data(:,2));
    hold on;
    legend_c(i) = strcat(['$\omega_c = ', num2str(omega_c),'$ rad/s']);
end
figure(25);
aa = subplot(2,1,1);
plot(out.r.Time,out.r.Data(:,1),'--k');
plot(out.r.Time,0.063*ones(size(out.r.Data(:,1))),'--m');
hold off;
grid on;
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(50,1)),'}{s}$']));
legend(strcat([legend_c,'$r(t)$','$63\%$']),'interpreter','latex');
bb = subplot(2,1,2);
plot(out.r.Time,out.r.Data(:,2),'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$r(t),y(t)$');
title(strcat(['$r(s) = \displaystyle \frac{',num2str(out.r.Data(50,2)),'}{s}$']));
