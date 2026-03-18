clear all;
clc;

s = tf('s');
G = 0.1/((s)*(s^2 + 3*s + 1)); % G = 1.3*(s + 2)/(s^3 + s^2 + 6*s + 1)
G_1 = 10*G;

W=logspace(-2,2,1000);

[M,P,w] = bode(G,W);
M = mag2db(squeeze(M));
P = squeeze(P);
[K_M,gamma_M,w_pi,w_c] = margin(G);
[M_1,P_1,w_1] = bode(G_1,W);
M_1 = mag2db(squeeze(M_1));
P_1 = squeeze(P_1);
[K_M_1,gamma_M_1,w_pi_1,w_c_1] = margin(G_1);

[M_2,P_2,w_2] = bode(K_M*G,W);
M_2 = mag2db(squeeze(M_2));
P_2 = squeeze(P_2);
[K_M_2,gamma_M_2,w_pi_2,w_c_2] = margin(K_M*G);

w = log10(squeeze(w));

% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(1);
aa = subplot(2,1,1);
plot(w,M);
hold on;
plot(w,M_1);
% plot(w,M_2,'k');
plot(w,zeros(size(w)),'--k');
line([log10(w_c),log10(w_c)],[min(min(M),min(M_1)),max(max(M),max(M_1))],...
      'color',[0.5 0.5 0.5],'lineStyle',':');
line([log10(w_c_1),log10(w_c_1)],[min(min(M),min(M_1)),max(max(M),max(M_1))],...
      'color',[0.5 0.5 0.5],'lineStyle',':');
hold off;
grid on;
ylabel('$\vert G(j\omega) \vert$ in dB');
legend({'$K_p = 1$','$K_p = 10$','$0$ dB','$\omega = \omega_c$'},'interpreter','latex');

bb = subplot(2,1,2);
plot(w,P);
hold on;
plot(w,-180*ones(size(w)),'--k');
hold off;
grid on;
xlabel('$\omega$ in logscale ($10^{\omega}$)');
ylabel('$\angle G(j\omega)$ in degrees');
legend({'$\angle G(j\omega)$','$-180^o$'},'interpreter','latex');
linkaxes([aa,bb],'x');

%% Phase margin plots
figure(2);
aa = subplot(2,1,1);
plot(w,M);
hold on;
plot(w,zeros(size(w)),'--k');
line([log10(w_c),log10(w_c)],[min(min(M),min(M_1)),max(max(M),max(M_1))],...
      'color',[0.5 0.5 0.75],'lineStyle',':');
line([log10(w_pi),log10(w_pi)],[min(min(M),min(M_1)),max(max(M),max(M_1))],...
      'color',[0.5 0.5 0.25],'lineStyle',':');
hold off;
grid on;
ylabel('$\vert G(j\omega) \vert$ in dB');
legend({'$\vert G(j\omega) \vert$','$0$ dB','$\omega = \omega_c$','$\omega = \omega_{\pi}$'},'interpreter','latex');

bb = subplot(2,1,2);
plot(w,P);
hold on;
plot(w,-180*ones(size(w)),'--k');
line([log10(w_c),log10(w_c)],[-300,max(P)],...
      'color',[0.5 0.5 0.75],'lineStyle',':');
line([log10(w_pi),log10(w_pi)],[-300,max(P)],...
      'color',[0.5 0.5 0.25],'lineStyle',':');
hold off;
grid on;
xlabel('$\omega$ in logscale ($10^{\omega}$)');
ylabel('$\angle G(j\omega)$ in degrees');
legend({'$\angle G(j\omega)$','$-180^o$'},'interpreter','latex');
linkaxes([aa,bb],'x');
