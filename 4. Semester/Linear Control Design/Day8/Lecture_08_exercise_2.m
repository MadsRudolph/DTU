clear all;
clc;

s = tf('s');                        % Define complex variable
G = 0*s;                            % Define the transfer function
p = 0;                      % Find the poles of G

% Define Ni and gamma_M
N_i = 3;
gamma_M = 60;
% Define phase contributions from PI and P-Lead and phase of G at new
% cross-over frequency IN DEGREES.
phi_i = 0;
phi_G = 0;
omega_c = w_out(i_c);       % Plot the Bode of G and get omega_c

% PI controller time constant and transfer function
tau_i = 0;
C_PI = 0*s;

% Open-loop transfer function
G_ol = minreal(C_PI*G);

% P-controller gain
K_P = 0;

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

T = 54; % Time to simulate for step responses

G_cl = 0;                   % Closed-loop with P controller
G_cl_PI = 0;                % Closed-loop with PI controller

% Step response
% Plot step response of closed-loop with PI controller
% Plot step response of closed-loop with P controller
