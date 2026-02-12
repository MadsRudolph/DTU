clear all;
clc;

T_s = 0.01;
t = 0:T_s:100;                              % Define the vector of time (t = 0, 0.01, 0.02, ..., 100)
x = 2*sin(2*pi*0.1*t) + 4.5*tanh(0.1*t);    % Define a function of time (same lenght as t)

t_f = t(end);                               % Final time
X = timeseries(x,t,'name','X');             % Put the data in a "timeseries" object

G_n = [1 1];                                % Transfer function numerator
G_d = [1 0.12 1];                           % Transfer function denominator

%% Run Simulink model and plot
out = sim('Simulink_intro');    % Output that contains all signals in Simulink

% Save Y_1..Y_5 obtained from Simulink in arrays (optional)
Y_1 = out.Y_1;
Y_2 = out.Y_2;
Y_3 = out.Y_3;
Y_4 = out.Y_4;
Y_5 = out.Y_5;

%% Plotting
% Set some properties for plotting (optional)
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',20);
set(0,'DefaultLineLineWidth', 2);

figure(1);
plot(t,Y_1);
grid on;
xlabel('$t$ in s');
ylabel('$Y_1$');

figure(2);
plot(t,Y_2);
grid on;
xlabel('$t$ in s');
ylabel('$Y_2$');

figure(3);
plot(t,Y_3);
grid on;
xlabel('$t$ in s');
ylabel('$Y_3$');

figure(4);
plot(t,Y_4);
grid on;
xlabel('$t$ in s');
ylabel('$Y_4$');

figure(5);                          % Define a specific figure
plot(t,Y_5);                        % Plot Y_5 against time
grid on;                            % Enable grid
xlabel('$t$ in s');                 % Place label on x-axis
ylabel('$Y_5$ in m');               % Place label on y-axis
title('Mass-sping-damper system');  % Place title
