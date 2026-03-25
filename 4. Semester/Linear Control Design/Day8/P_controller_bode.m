clear all;
clc;

s = tf('s');                            % Define complex variable
G = 3.3/(s^3 + 5*s^2 + 2.1*s + 1);      % System to control

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

w = linspace(1e-1,2,1000);              % Define range for the Bode plot
K_p = 1;

G_ol = K_p*G;                           % Open-loop transfer function
[M,P,w_out] = bode(G_ol,w);             % Get magnitude and phase from Bode
M = mag2db(squeeze(M));
P = squeeze(P);
[g_M,p_M,w_pi,w_c] = margin(G);         % Get margins, omega_c and omega_pi
gamma_M = 60;                           % Desired phase margin
ii = find(w_out >= w_c,1);              % Find closest freqeuncy to omega_c
jj = find(w_out >= w_pi,1);             % Find closest freqeuncy to omega_pi
kk = find(P <= -120,1);                 % Find freqeuncy where phase = -120 degrees

figure(1);
aa = subplot(2,1,1);
semilogx(w_out,M);                      % Plot M in logarithmic scale for x
hold on;
scatter(w_out(ii),M(ii),54);            % Plot G(omega_c*j)
hold off;
grid on;
ylabel('$\vert G_{ol} \vert$ in dB');
set(gca,'xtick',[]);
ylim([-10 20]);

bb = subplot(2,1,2);
semilogx(w_out,P);                      % Plot P in logarithmic scale for x
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');   % Plot -180 degrees line
semilogx(w_out,-120*ones(size(w_out)),'--k');   % Plot -120 degrees line
scatter(w_out(jj),P(jj),54);                    % Plot G(omega_c*j)
scatter(w_out(kk),P(kk),54);                    % Plot G(omega_120*j)
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
ylim([-225 0]);
linkaxes([aa,bb],'x');

figure(2);
[y,t] = step(G*0.3508/(1 + G*0.3505),0:0.01:50);    % Get step response of closed-loop transfer function
plot(t,y);                                          % Plot step response
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
ylim([0 1.1]);

