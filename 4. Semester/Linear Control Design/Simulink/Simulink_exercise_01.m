clear all;
clc;

T_s = 0.01;
t = 0:T_s:100;                              % Define the vector of time (t = 0, 0.01, 0.02, ..., 100)
x = 2*sin(2*pi*0.1*t) + 4.5*tanh(0.1*t);    % Define a function of time (same lenght as t)

t_f = t(end);                               % Final time
X = timeseries(x,t,'name','X');             % Put the data in a "timeseries" object

G_n = [0 0 0];	% Transfer function numerator (fill these in)
G_d = [0 0 0];	% Transfer function denominator (fill these in)

%% Run Simulink model and plot
% Save the output that contains all signals in Simulink (should be in the 
% same folder)
% e.g. out = sim('My_Model');

% Save Y_1..Y_5 obtained from Simulink in arrays
% e.g. Y_1 = out.Y_1;
Y_2 = 0;
Y_3 = 0;
Y_4 = 0;
Y_5 = 0;

%% Plotting
% Set some properties for plotting (optional)
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',20);
set(0,'DefaultLineLineWidth', 2);

figure(1);

figure(2);

figure(3);

figure(4);

figure(5);
