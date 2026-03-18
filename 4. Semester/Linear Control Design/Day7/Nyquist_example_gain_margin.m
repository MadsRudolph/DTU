clear all;
clc;

s = tf('s');                                    % Define complex variable
G = 25*(s - 1)/((s^2 - 3)*(2*s + 1)*(s + 1));   % System to control

[~,~,w_pi,~] = margin(G);                       % Find omega_pi
M_pi = abs(freqresp(G,1i*w_pi));                % Find amplitude at omega_pi
K_M = 1/M_pi;                                   % This amplitude is 1/K_M

s = 1i*(0:0.001:1000);                    % Define range for s variable
GG_2 = squeeze(freqresp(G,s));            % Frequency response of G
GG_4 = squeeze(freqresp(1/M_pi*G,s));     % Frequency response of K_M*G
GG_5 = squeeze(freqresp(1/2*K_M*G,s));    % Frequency response of 0.5*K_M*G
GG_2m = squeeze(freqresp(-G,s));          % Frequency response of -G
GG_4m = squeeze(freqresp(-1/M_pi*G,s));   % Frequency response of -K_M*G
GG_5m = squeeze(freqresp(-1/2*K_M*G,s));  % Frequency response of -0.5*K_M*G

GG_unit = 1*exp(1i*(0:0.001:2*pi));       % Define unit circle

% Nyquist plots
figure(4);
aa = subplot(2,1,1);
plot(real(GG_2),imag(GG_2),'r');
hold on;
plot(real(GG_4),imag(GG_4),'Color',[84 130 15]./255,'lineStyle','--');
plot(real(GG_5),imag(GG_5),'Color','b');
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
hold off;
grid on;
ylabel('$\Im\{G(s)\}$');
% axis equal;
legend({'$G$','$\displaystyle K_M G$','$\displaystyle \frac{1}{2}K_M G$'},'interpreter','latex');

bb = subplot(2,1,2);
plot(real(GG_2m),imag(GG_2m),'r');
hold on;
plot(real(GG_4m),imag(GG_4m),'Color',[84 130 15]./255,'lineStyle','--');
plot(real(GG_5m),imag(GG_5m),'Color','b');
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\Re\{G(s)\}$');
ylabel('$\Im\{G(s)\}$');
% axis equal;
legend({'$-G$','$\displaystyle -K_M G$','$\displaystyle -\frac{1}{2}K_M G$'},'interpreter','latex');


figure(2);
plot(real(GG_2),imag(GG_2),'r');
hold on;
plot(real(GG_4),imag(GG_4),'Color',[84 130 15]./255);
plot(real(GG_5),imag(GG_5),'Color','b');
plot(real(GG_2m),imag(GG_2m),'r','lineStyle','--');
plot(real(GG_4m),imag(GG_4m),'Color',[84 130 15]./255,'lineStyle','--');
plot(real(GG_5m),imag(GG_5m),'Color','b','lineStyle','--');
plot(real(GG_unit),imag(GG_unit),'-.k');
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\Re\{G(s)\}$');
ylabel('$\Im\{G(s)\}$');
axis equal;
legend({'$G$','$\displaystyle K_M G$','$\displaystyle \frac{1}{2}K_M G$',...
        '$-G$','$\displaystyle -K_M G$','$\displaystyle -\frac{1}{2}K_M G$'},'interpreter','latex');
