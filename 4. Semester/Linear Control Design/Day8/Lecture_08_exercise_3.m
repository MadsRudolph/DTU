clear all;
clc;

s = tf('s');                        % Define complex variable
G = 0;                              % Define the transfer function

% Define Ni, alpha and gamma_M
N_i = 3;
alpha = 0.3;
gamma_M = 60;
% Define phase contributions from PI and P-Lead and phase of G at new
% cross-over frequency.
phi_i = 0;
phi_m = 0;
phi_G = 0;

omega_c = 0;       % Plot the Bode and get omega_c

% PI controller time constant and transfer function
tau_i = 0;
C_PI = 0;

% P-Lead controller time constant and transfer function
tau_d = 0;
C_D = 0;

% Open-loop transfer function
G_ol = 0;
% P-controller gain
K_P = 0;

%% Plots
set(0,'DefaultTextInterpreter','latex');
set(0,'DefaultAxesFontSize',15);
set(0,'DefaultLineLineWidth', 2);

T = 5.4; % Time to simulate for step responses
G_cl_P = 0;             % Closed-loop with P controller
G_cl_PI = 0;            % Closed-loop with PI controller
G_cl = 0;               % Closed-loop with PI-Lead controller
