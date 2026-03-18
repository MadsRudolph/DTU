clear all;
clc;

s = tf('s');
G_1 = 1.075/(s^3 + 5*s^2 + 2.1*s + 1); % 1.3*(s + 2)/(s^3 + s^2 + 6*s + 1)
G_2 = 0.13*1.5/(s*(2*s + 1)*(s + 1));
G_2 = 25*(s - 1)/((s^2 - 3)*(2*s + 1)*(s + 1));

W=logspace(-2,2,1000);

[M,P,w] = bode(G_1,W);
M = mag2db(squeeze(M));
P = squeeze(P);
[K_M,gamma_M,w_pi,w_c] = margin(G_1);
[M_2,P_2,w_2] = bode(G_2,W);
M_2 = mag2db(squeeze(M_2));
P_2 = squeeze(P_2);

w = log10(squeeze(w));

% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(1);
aa = subplot(2,1,1);
plot(w,M);
hold on;
plot(w,M_2);
% plot(w,M_2,'k');
plot(w,zeros(size(w)),'--k');
line([log10(w_c),log10(w_c)],[min(min(M),min(M_2)),max(max(M),max(M_2))],...
      'color',[0.5 0.5 0.75],'lineStyle',':');
line([log10(w_pi),log10(w_pi)],[min(min(M),min(M_2)),max(max(M),max(M_2))],...
      'color',[0.5 0.5 0.25],'lineStyle',':');
hold off;
grid on;
ylabel('$\vert G(j\omega) \vert$ in dB');
legend({'$G_1$','$G_2$','$0$ dB','$\omega = \omega_c$','$\omega = \omega_{\pi}$'},'interpreter','latex');
ylim([min(min(M),min(M_2)),max(max(M),max(M_2))]);

bb = subplot(2,1,2);
plot(w,P);
hold on;
plot(w,P_2);
plot(w,-180*ones(size(w)),'--k');
line([log10(w_c),log10(w_c)],[-200,max(max(P),max(P_2))],...
      'color',[0.5 0.5 0.75],'lineStyle',':');
line([log10(w_pi),log10(w_pi)],[-200,max(max(P),max(P_2))],...
      'color',[0.5 0.5 0.25],'lineStyle',':');
hold off;
grid on;
xlabel('$\omega$ in logscale ($10^{\omega}$)');
ylabel('$\angle G(j\omega)$ in degrees');
legend({'$\angle G(j\omega)$','$-180^o$'},'interpreter','latex');
% ylim([-200,max(max(P),max(P_2))]);
linkaxes([aa,bb],'x');

%% Nyquist plots
s = 1i*(0:0.001:1000);
GG_1 = squeeze(freqresp(4*G_1,s)); % 1.075./(s.^3 + 5*s.^2 + 2.1*s + 1); % 1.3*(s + 2)./(s.^3 + s.^2 + 6*s + 1)
GG_2 = squeeze(freqresp(G_2,s)); % 0.13*1.5./(s.*(2*s + 1).*(s + 1));
GG_unit = 1*exp(1i*(0:0.001:2*pi)); % 1.5./(s - 0.5);
figure(2);
% nyquist(G_1);
plot(real(GG_1),imag(GG_1),'b');
hold on;
plot(real(GG_2),imag(GG_2),'r');
i_1 = find(angle(GG_1) <= -pi/4,1);
scatter(real(GG_1(i_1)),imag(GG_1(i_1)),54,'>',...
        'markerFaceColor','b','MarkerEdgeColor','b');
i_2 = find(abs(GG_2) <= 1.2,1);
scatter(real(GG_2(i_2)),imag(GG_2(i_2)),54,'>',...
        'markerFaceColor','r','MarkerEdgeColor','r');
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\Re\{G(s)\}$');
ylabel('$\Im\{G(s)\}$');
axis equal;
% axis([-1.54 1.54 -1.5 1.5]);

%% Exercise plots
s = 1i*(0:0.001:1000);
GG_1 = squeeze(freqresp(4*G_1,s));
GG_2 = squeeze(freqresp(G_2,s));
GG_4 = squeeze(freqresp(1/1.6651*G_2,s));
GG_5 = squeeze(freqresp(1/2*G_2,s));
GG_unit = 1*exp(1i*(0:0.001:2*pi));
figure(4);
plot(real(GG_2),imag(GG_2),'r');
hold on;
plot(real(GG_4),imag(GG_4),'--r');
plot(real(GG_5),imag(GG_5),'Color',[84 130 15]./255);
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\Re\{G(s)\}$');
ylabel('$\Im\{G(s)\}$');
axis equal;
legend({'$G_2$','$\displaystyle \frac{1}{1.6651}G_2$','$\displaystyle \frac{1}{2}G_2$'},'interpreter','latex');
% axis([-2.54 1.54 -1.5 2.5]);

%% Bode and Nyquist plots
figure(3);
cc = subplot(2,2,1);
plot(w,M);
hold on;
plot(w,zeros(size(w)),'--k');
line([log10(w_c),log10(w_c)],[min(min(M),min(M_2)),max(max(M),max(M_2))],...
      'color',[0.5 0.5 0.75],'lineStyle',':');
line([log10(w_pi),log10(w_pi)],[min(min(M),min(M_2)),max(max(M),max(M_2))],...
      'color',[0.5 0.5 0.25],'lineStyle',':');
hold off;
grid on;
ylabel('$\vert G(j\omega) \vert$ in dB');
title('Bode plot');
legend({'$G_1$','$0$ dB','$\omega = \omega_c$','$\omega = \omega_{\pi}$'},'interpreter','latex');
ylim([min(min(M),min(M_2)),max(max(M),max(M_2))]);

dd = subplot(2,2,3);
plot(w,P);
hold on;
plot(w,-180*ones(size(w)),'--k');
line([log10(w_c),log10(w_c)],[-300,max(max(P),max(P_2))],...
      'color',[0.5 0.5 0.75],'lineStyle',':');
line([log10(w_pi),log10(w_pi)],[-300,max(max(P),max(P_2))],...
      'color',[0.5 0.5 0.25],'lineStyle',':');
hold off;
grid on;
xlabel('$\omega$ in logscale ($10^{\omega}$)');
ylabel('$\angle G(j\omega)$ in degrees');
legend({'$\angle G(j\omega)$','$-180^o$'},'interpreter','latex');
linkaxes([cc,dd],'x');

ee = subplot(2,2,[2 4]);
plot(real(GG_1),imag(GG_1),'b');
hold on;
scatter(real(GG_1(i_1)),imag(GG_1(i_1)),54,'>',...
        'markerFaceColor','b','MarkerEdgeColor','b');
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\Re\{G(s)\}$');
ylabel('$\Im\{G(s)\}$');
title('Nyquist plot');
axis equal;
axis([-1.1254 1.1254 -1.5 1.5]);
