clear all;
clc;

s = tf('s');                        % Define complex variable
G = 3.3/(s^3 + 5*s^2 + 2.1*s + 1);  % System to control

K_P = [1 0.54 0.3508 0.12];         % Different values of K_P
colours = ['b','m','g','r'];
ess = 1./(1 + K_P*dcgain(G));       % Associated steady state errors

% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

legend_c = string(K_P);
figure(1);
for j = 1:length(K_P)
    [y,t] = step(G*K_P(j)/(1 + G*K_P(j)),0:0.01:50); % Obtain step response
    plot(t,y,colours(j));                            % Plot step response
    hold on;
    legend_c(j) = strcat(['$K_p = ', num2str(K_P(j)),'$']);
end
figure(1);
plot(t,ones(size(t)),'--k');
hold off;
grid on;
xlabel('$t$ in s');
ylabel('$y(t)$');
legend([legend_c],'interpreter','latex');

%% Nyquist plots
s = 1i*(0:0.001:1000);                      % Define range for s variable
figure(2);
GG_unit = 1*exp(1i*(0:0.001:2*pi));         % Define unit circle
for j = 1:length(K_P)
    GG = squeeze(freqresp(K_P(j)*G,s));     % Obtain frequency response
    plot(real(GG),imag(GG),colours(j));     % Plot in w-plane
    hold on;
    i = find(angle(GG) <= -pi/4,1);
    scatter(real(GG(i)),imag(GG(i)),54,'>',...
        'markerFaceColor',colours(j),'MarkerEdgeColor',colours(j));
end
legend_n = [];
for j = 1:length(K_P)
    legend_n = [legend_n legend_c(j) ''];
end
legend_n = legend_n(1:end-1);
figure(2);
plot(real(GG_unit),imag(GG_unit),'-.k');    % Plot unit circle
scatter(-1,0,54,'markerFaceColor','g','MarkerEdgeColor','k');
hold off;
grid on;
xlabel('$\Re\{G(s)\}$');
ylabel('$\Im\{G(s)\}$');
axis equal;
legend(legend_n,'interpreter','latex');




