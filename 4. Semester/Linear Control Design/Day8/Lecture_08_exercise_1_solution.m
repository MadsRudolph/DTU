clear all;
clc;

s = tf('s');                    % Define complex variable
G = 40/(s*(s + 10)^2);          % System to control

p = pole(G);                    % Find poles
w = linspace(1e-1,20,1000);     % Define frequency range for Bode plot

[M,P,w_out] = bode(G,w);        % Get magnitude and phase
M = mag2db(squeeze(M));
P = squeeze(P);

[g_M,p_M,w_pi,w_c] = margin(G); % Get omega_c and omega_pi (and margins)
ii = find(w_out >= w_c,1);      % Find index for omega_c
jj = find(w_out >= w_pi,1);     % Find index for omega_pi
kk = find(P <= -120,1);         % Find index for -120 degrees frequency
K_P = db2mag(-M(kk));           % Calculate K_P from magnitude at -120 degrees

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(1);
aa = subplot(2,1,1);
semilogx(w_out,M);              % Plot P in logarithmic scale for x
hold on;
scatter(w_out(ii),M(ii),54,'markerFaceColor','k','MarkerEdgeColor',' k');   % Plot G(omega_c*j)
scatter(w_out(kk),M(kk),54,'markerFaceColor','k','MarkerEdgeColor',' k');   % Plot G(omega_120*j)
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
set(gca,'xtick',[]);
ylim([-60 20]);

bb = subplot(2,1,2);
semilogx(w_out,P);              % Plot P in logarithmic scale for x
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');   % Plot -180 degrees line
semilogx(w_out,-120*ones(size(w_out)),'--k');   % Plot -120 degrees line
scatter(w_out(jj),P(jj),54,'markerFaceColor','k','MarkerEdgeColor',' k');   % Plot G(omega_pi*j)
scatter(w_out(kk),P(kk),54,'markerFaceColor','k','MarkerEdgeColor',' k');   % Plot G(omega_120*j)
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
ylim([-270 -90]);
linkaxes([aa,bb],'x');

%% Close the loop
G_cl = minreal(K_P*G/(1 + K_P*G));  % Define closed-loop transfer function

[y,t] = step(G_cl,0:0.01:5);        % Get step response of G_cl
figure(2);
plot(t,y);                          % Plot step response
hold on;
plot(t,ones(size(t)),'--k');        % Plot step reference
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');

stepinfo(G_cl)                      % Get step response info

%% Error
G_e = minreal(1/(1 + K_P*G));       % Define the Error transfer function
ess = freqresp(s*G_e*1/s,0);        % Calculate steady state error
