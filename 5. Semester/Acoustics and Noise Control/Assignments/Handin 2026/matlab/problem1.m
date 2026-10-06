%% 34840 hand-in 2026 - Problem 1 (coral reef)
% Mads Rudolph, s246132
clear; clc;

rho = 1000;     % water density [kg/m^3]
c = 1480;       % speed of sound in water [m/s]
Z0 = rho*c      % characteristic impedance of water [Pa s/m]

%% Q1.1 absorption coefficient
p_i = 3;        % incident amplitude (peak) [Pa]
I_t = 2.1e-6;   % measured total intensity [W/m^2]

% incident intensity, I = p^2/(2*rho*c)
I_i = p_i^2/(2*Z0)

% total intensity = I_i - I_r = alpha*I_i
alpha = I_t/I_i

%% Q1.2 surface impedance
% alpha = 1 - |R|^2
R = sqrt(1 - alpha)

% Z is real so R is real, R = +0.556 or -0.556
% Z = Z0*(1+R)/(1-R)
Z_pos = Z0*(1 + R)/(1 - R)     % R > 0, harder than water
Z_neg = Z0*(1 - R)/(1 + R)     % R < 0, softer than water

Z_pos/Z0
Z_neg/Z0
