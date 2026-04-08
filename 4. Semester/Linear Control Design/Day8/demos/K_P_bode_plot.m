clear all;
clc;

s = tf('s');                        % Define complex variable
G = 3.3/(s^3 + 5*s^2 + 2.1*s + 1);  % System to control

set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

w = linspace(0,1,1000);
K_p = 0.1*[1 2 4 5];                % Different values of K_P

legend_c = string(K_p);
for i = 1:length(K_p)
    legend_c(i) = strcat(['$K_p = ', num2str(K_p(i)),'$']);
    G_ol = K_p(i)*G;            % Define open-loop transfer function
    [M,P,w_out] = bode(G_ol,w); % Get magnitude and phase from bode plot
    M = mag2db(squeeze(M));
    figure(1);
    aa = subplot(2,1,1);
    semilogx(w_out,M);          % Plot magnitude
    grid on;
    hold on;
    bb = subplot(2,1,2);
    semilogx(w_out,squeeze(P),'k'); % Plot phase
    grid on;
    hold on;
    e_ss = 1/(1 + K_p(i)*3.3);  % Steady-state error
end
figure(1);
aa = subplot(2,1,1);
legend(legend_c,'interpreter','latex');
hold off;
ylabel('$\vert G_{ol} \vert$ in dB');
bb = subplot(2,1,2);
hold off;
xlabel('$\omega$ in rad/s');
ylabel('$\angle G_{ol}$ in deg');
linkaxes([aa,bb],'x');






