clear all;
clc;

% Figure export path (Obsidian images folder)
img_path = 'C:/Users/Mads2/DTU/Obsidian/Courses/34722 Linear Control Design 1/Images/';

% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

s = tf('s');                    % Define complex variable
G = 40/(s*(s + 10)^2);         % Transfer function (type-1 system with integrator)

p = pole(G);                   % Find poles: 0, -10, -10
fprintf('Poles of G(s): '); disp(p');

w = linspace(1e-1,20,1000);    % Define frequency range for Bode plot
[M,P,w_out] = bode(G,w);       % Get magnitude and phase
M = mag2db(squeeze(M));
P = squeeze(P);

[g_M,p_M,w_pi,w_c] = margin(G); % Get omega_c, omega_pi and margins
ii = find(w_out >= w_c,1);     % Index for omega_c
jj = find(w_out >= w_pi,1);    % Index for omega_pi
kk = find(P <= -120,1);        % Index for -120 degrees (phase margin = 60 deg)

omega_c = w_out(kk);           % New crossover frequency at -120 deg phase
K_P = db2mag(-M(kk));          % Calculate K_P from magnitude at -120 degrees

fprintf('Original crossover frequency: %.3f rad/s\n', w_c);
fprintf('New crossover frequency (at -120 deg): %.3f rad/s\n', omega_c);
fprintf('Required K_P: %.4f\n', K_P);
fprintf('Original gain margin: %.2f dB\n', mag2db(g_M));
fprintf('Original phase margin: %.2f deg\n', p_M);

%% Bode plot of G(s)
figure(1); clf;
aa = subplot(2,1,1);
semilogx(w_out,M);
hold on;
scatter(w_out(ii),M(ii),54,'markerFaceColor','k','MarkerEdgeColor','k');
scatter(w_out(kk),M(kk),54,'markerFaceColor','k','MarkerEdgeColor','k');
yline(0,'--k');
hold off;
grid on;
ylabel('$\vert G \vert$ in dB');
set(gca,'xtick',[]);
ylim([-60 20]);

bb = subplot(2,1,2);
semilogx(w_out,P);
hold on;
semilogx(w_out,-180*ones(size(w_out)),'--k');
semilogx(w_out,-120*ones(size(w_out)),'--k');
scatter(w_out(jj),P(jj),54,'markerFaceColor','k','MarkerEdgeColor','k');
scatter(w_out(kk),P(kk),54,'markerFaceColor','k','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G$ in deg');
ylim([-270 -90]);
linkaxes([aa,bb],'x');
saveas(gcf, [img_path 'day8_ex1_bode.png']);

%% Close the loop
G_cl = minreal(K_P*G/(1 + K_P*G));  % Closed-loop transfer function

% Step response
[y,t] = step(G_cl,0:0.01:5);
figure(2); clf;
plot(t,y);
hold on;
plot(t,ones(size(t)),'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
title('Closed-loop step response (P controller)');
legend({'$G_{cl}$', 'Reference'},'interpreter','latex');
saveas(gcf, [img_path 'day8_ex1_step.png']);

fprintf('\n--- Step response info ---\n');
si = stepinfo(G_cl);
fprintf('Rise time:     %.4f s\n', si.RiseTime);
fprintf('Settling time: %.4f s\n', si.SettlingTime);
fprintf('Overshoot:     %.2f %%\n', si.Overshoot);
fprintf('Peak:          %.4f\n', si.Peak);

%% Error
G_e = minreal(1/(1 + K_P*G));  % Error transfer function
ess = freqresp(s*G_e*1/s,0);   % Steady state error
fprintf('\nSteady-state error: %.4f\n', ess);
fprintf('(Type-1 system -> zero steady-state error for step input)\n');
