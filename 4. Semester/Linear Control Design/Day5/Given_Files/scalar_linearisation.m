clear all;
clc;

x = linspace(-4*pi/10,4*pi/10,1000);
y = x./(cos(x).^3);

y_1 = 1/(cos(1)^3);
dydx_1 = (cos(1)^3 + 3*1*cos(1)^2*sin(1))/cos(1)^6;

y_lin = dydx_1*(x - 1) + y_1;

% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

figure(1);
plot(x,y);
hold on;
plot(x,y_lin);
scatter(1,y_1,54);
hold off;
grid on;
xlabel('$x$');
ylabel('$y$');
legend({'nonlinear','linearised'}, 'interpreter','latex');
title('Linearisation of $y = \frac{x}{\cos^3(x)}$ about $x = 1$.');

