clear all;
clc;

% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

s = tf('s');                    % Define complex variable
G = 0*s;                        % Define the transfer function

p = 0;                          % Find poles

omega_c = 0;                    % Plot bode and find omega_c
K_P = 0;                        % Calculate K_P from magnitude at -120 degrees

% Close the loop
G_cl = 0;                       % Define closed-loop transfer function

% Plot step response

stepinfo(G_cl)                  % Get step response info

% Error
G_e = 0;                        % Define the Error transfer function
ess = 0;                        % Calculate steady state error
