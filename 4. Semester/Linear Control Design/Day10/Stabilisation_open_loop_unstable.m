clear all;
clc;

s = tf('s');                                % Define the complex variable s
G = 0.5*(s + 1)/((0.1*s + 1)*(-0.01*s + 1));% Define the transfer function
% Nyquist plots for G, -G and -3*G
[re_G,im_G,w] = nyquist(G,[-1e4:0.05:1e4]);
re_G = squeeze(re_G);
im_G = squeeze(im_G);
GG_unit = 1*exp(1i*(0:0.001:2*pi));

[G_real,G_imag,w] = nyquist(-G,[-1e4:0.1:1e4]);
G_real = squeeze(G_real);
G_imag = squeeze(G_imag);

[G_real_2,G_imag_2,w] = nyquist(-3*G,[-1e4:0.1:1e4]);
G_real_2 = squeeze(G_real_2);
G_imag_2 = squeeze(G_imag_2);

K_p_s = -3;
G_s = minreal(K_p_s*G/(1 + K_p_s*G));

w = linspace(1e-1,10000,500000);
[M_u,P_u,w_out] = bode(G,w);
M_u = mag2db(squeeze(M_u));
P_u = squeeze(P_u);

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

% Nyquist plots
figure(1)
plot(re_G,im_G,'r');
hold on;
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
i = find(angle(re_G + 1i*im_G) >= pi/3,1);
scatter(re_G(i),im_G(i),54,'<',...
    'markerFaceColor','r','MarkerEdgeColor','r');
hold off;
grid on;
xlabel('$\Re\{G(s)\}$');
ylabel('$\Im\{G(s)\}$');
title('Nyquist plot of $G(s)$');
axis equal;

figure(2)
plot(G_real,G_imag,'b');
hold on;
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
i = 98295;
scatter(G_real(i),G_imag(i),54,'>',...
    'markerFaceColor','b','MarkerEdgeColor','b');
hold off;
grid on;
xlabel('$\Re\{-G(s)\}$');
ylabel('$\Im\{-G(s)\}$');
title('Nyquist plot of $-G(s)$');
axis equal;

figure(3)
plot(G_real_2,G_imag_2,'b');
hold on;
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
i = 98295;
scatter(G_real_2(i),G_imag_2(i),54,'>',...
    'markerFaceColor','b','MarkerEdgeColor','b');
hold off;
grid on;
xlabel('$\Re\{-3G(s)\}$');
ylabel('$\Im\{-3G(s)\}$');
title('Nyquist plot of $-3G(s)$');
axis equal;

%% New design (Method 1)
[M_s,P_s,w_out] = bode(G_s,w);
M_s = mag2db(squeeze(M_s));
P_s = squeeze(P_s);

% Bode plots
figure(4);
a1 = subplot(2,1,1);
semilogx(w_out,M_u,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,M_s,'Color','m','lineStyle','-');
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
title('Open-loop Bode plot');
set(gca,'xtick',[]);
b1 = subplot(2,1,2);
semilogx(w_out,P_u,'Color',[84 130 15]./255);
hold on;
semilogx(w_out,P_s,'Color','m','lineStyle','-');
semilogx(w_out,-180*ones(size(w_out)),'--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
legend({'$G(s)$',' $G_s(s)$'},'interpreter','latex');
linkaxes([a1,b1],'x');
xlim([0 w(end)]);

N_i = 3;
omega_c = 2000;
i_c = find(w_out >= omega_c,1,'first');
% PI controller time constant and transfer function
tau_i = N_i/omega_c;
C_PI = (1 + 1/(tau_i*s));
[M_PI,P_PI,w_out] = bode(C_PI,w);
M_PI = mag2db(squeeze(M_PI));
P_PI = squeeze(P_PI);

G_ol = C_PI*G_s;
K_P = 1/abs(freqresp(G_ol,omega_c*1i));

G_cl = minreal(K_P*G_ol/(1 + K_P*G_ol));
G_u = minreal(K_P*C_PI/(1 + K_P*G_ol));

figure(5);
a1 = subplot(2,1,1);
semilogx(w_out,M_s,'Color','m');
hold on;
semilogx(w_out,M_PI,'Color','g','lineStyle','--');
semilogx(w_out,mag2db(K_P) + M_s + M_PI,'Color','b','lineStyle','-');
scatter(w_out(i_c),mag2db(K_P) + M_s(i_c) + M_PI(i_c),25,...
                'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
title('Open-loop Bode plot');
legend({'$G_s(s)$',' $G_{PI}(s)$',' $G_{ol}(s)$'},'interpreter','latex');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P_s,'Color','m');
hold on;
semilogx(w_out,P_PI,'Color','g','lineStyle','--');
semilogx(w_out,P_s + P_PI,'Color','b','lineStyle','-');
scatter(w_out(i_c),P_s(i_c) + P_PI(i_c),25,'markerFaceColor','k',...
                'MarkerEdgeColor',' k');
semilogx(w_out,-180*ones(size(w_out)),'--k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
linkaxes([a1,b1],'x');
xlim([0 w(end)]);

T = 0.05421; % Time to simulate for step responses
T_s = 0.0001;
[y,t] = step(G_cl,0:T_s:T);
[u,t] = step(G_u,0:T_s:T);
stepinfo(G_cl)

% Step response
figure(6);
aa = subplot(2,1,1);
plot(t,y);          % Plot step response of closed-loop with P controller
hold on;
plot(t,ones(size(t)),'--k');    % Plot step reference
hold off;
grid on;
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'$y(t)$' ,'$r(t)$'},'interpreter','latex');
ylim([0 1.2]);
set(gca,'xtick',[]);

bb = subplot(2,1,2);
plot(t,u);
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
linkaxes([aa,bb],'x');
xlim([0 T]);

%% Alternative design (Method 2)
G_s = -G; % Include the sign from the stabilsing K_P
[M_s,P_s,w_out] = bode(G_s,w);
M_s = mag2db(squeeze(M_s));
P_s = squeeze(P_s);
i_i = find(M_s == max(M_s),1,'first'); % Point at which the positive slope ends
omega_i = w_out(i_i);
tau_i = 1/omega_i;
C_PI = (1 + 1/(tau_i*s));
[M_PI,P_PI,w_out] = bode(C_PI,w);
M_PI = mag2db(squeeze(M_PI));
P_PI = squeeze(P_PI);
omega_c = 2000; % A large crossover frequency for increased bandwidth (over the peak)
i_c = find(w_out >= omega_c,1,'first');

G_ol = C_PI*G_s;
K_P = 1/abs(freqresp(G_ol,omega_c*1i));

G_cl = minreal(K_P*G_ol/(1 + K_P*G_ol));
G_u = minreal(K_P*C_PI/(1 + K_P*G_ol));
% Bode plots
figure(7);
a1 = subplot(2,1,1);
semilogx(w_out,M_s,'Color','m','lineStyle','-');
hold on;
semilogx(w_out,M_PI,'Color','g','lineStyle','--');
semilogx(w_out,mag2db(K_P) + M_s + M_PI,'Color','b','lineStyle','-');
scatter(w_out(i_c),mag2db(K_P) + M_s(i_c) + M_PI(i_c),25,...
                'markerFaceColor','k','MarkerEdgeColor',' k');
scatter(w_out(i_i),M_s(i_i),25,'markerFaceColor','k',...
                'MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G_{ol} \vert$ in dB');
title('Open-loop Bode plot');
legend({'$G_s(s)$','$C_{PI}(s)$','$G_{ol}(s)$'},'interpreter','latex');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P_s,'Color','m','lineStyle','-');
hold on;
semilogx(w_out,P_PI,'Color','g','lineStyle','--');
semilogx(w_out,P_s + P_PI,'Color','b','lineStyle','-');
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_c),P_s(i_c) + P_PI(i_c),25,'markerFaceColor','k',...
                'MarkerEdgeColor',' k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
linkaxes([a1,b1],'x');
xlim([0 w(end)]);

T = 0.5421; % Time to simulate for step responses
T_s = 0.0001;
[y,t] = step(G_cl,0:T_s:T);
[u,t] = step(G_u,0:T_s:T);

stepinfo(G_cl)
% Step response
figure(8);
aa = subplot(2,1,1);
plot(t,y);          % Plot step response of closed-loop with P controller
hold on;
plot(t,ones(size(t)),'--k');    % Plot step reference
hold off;
grid on;
ylabel('$y(t)$');
title('Closed-loop step response');
legend({'$y(t)$' ,'$r(t)$'},'interpreter','latex');
ylim([0 1.2]);
set(gca,'xtick',[]);

bb = subplot(2,1,2);
plot(t,u);
grid on;
xlabel('$t$ in s');
ylabel('$u(t)$');
linkaxes([aa,bb],'x');
xlim([0 T]);

% Closed-loop Bode plots
[M_cl,P_cl,w_out] = bode(G_cl,w);
M_cl = mag2db(squeeze(M_cl));
P_cl = squeeze(P_cl);
i_BW = find(M_cl <= M_cl(1) - 3,1,'first'); % index for omega_BW
omega_BW = w_out(i_BW);
figure(9);
a1 = subplot(2,1,1);
semilogx(w_out,M_cl,'Color','b','lineStyle','-');
hold on;
semilogx(w_out,-3*ones(size(M_cl)),'Color','k','lineStyle','--');
scatter(w_out(i_BW), M_cl(i_BW),25,...
                'markerFaceColor','k','MarkerEdgeColor',' k');
hold off;
grid on;
ylabel('$\vert G_{cl} \vert$ in dB');
title('Closed-loop Bode plot');
legend({'$G_{cl}(s)$','$-3 dB$'},'interpreter','latex');
set(gca,'xtick',[]);

b1 = subplot(2,1,2);
semilogx(w_out,P_cl,'Color','b','lineStyle','-');
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');
scatter(w_out(i_BW),P_cl(i_BW),25,'markerFaceColor','k',...
                'MarkerEdgeColor',' k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{cl}$ in deg');
linkaxes([a1,b1],'x');
xlim([0 w(end)]);



