%% 34840 Lab exercise — preparation (i): lowest eigenfrequencies of the lab room
% Room 4.38 x 3.13 x 3.29 m (x length, y width, z height). Guide p. 1, course text 3.1.

%% Speed of sound at the room temperature
% c = 331.3 + 0.606*theta   [m/s], theta in degC (change theta on the lab day)
theta = 20;
c = 331.3 + 0.606*theta

%% Room
Lx = 4.38; Ly = 3.13; Lz = 3.29;
% V = Lx*Ly*Lz
V = Lx*Ly*Lz
% S = 2(LxLy + LxLz + LyLz)
S = 2*(Lx*Ly + Lx*Lz + Ly*Lz)

%% Eigenfrequencies  f = c/2 * sqrt((nx/Lx)^2 + (ny/Ly)^2 + (nz/Lz)^2)
f100 = c/2*sqrt((1/Lx)^2)                 % 39.2 Hz  axial
f001 = c/2*sqrt((1/Lz)^2)                 % 52.2 Hz  axial (height before width!)
f010 = c/2*sqrt((1/Ly)^2)                 % 54.9 Hz  axial
f101 = c/2*sqrt((1/Lx)^2 + (1/Lz)^2)      % 65.3 Hz  tangential
f110 = c/2*sqrt((1/Lx)^2 + (1/Ly)^2)      % 67.4 Hz  tangential
f011 = c/2*sqrt((1/Ly)^2 + (1/Lz)^2)      % 75.7 Hz  tangential (spare)
f200 = c/2*sqrt((2/Lx)^2)                 % 78.4 Hz  axial (spare)

%% Temperature sensitivity  df/f = dc/c = 0.606/c per kelvin
dfrel = 0.606/c                           % 0.18 % per K

%% Sabine sanity check  A = 0.161 V / T,  alpha_mean = A / S
T_empty = 10;  A_empty = 0.161*V/T_empty  % 0.73 m^2
alpha_empty = A_empty/S                   % about 0.01

%% Schroeder frequency  fS = 2000 sqrt(T/V)
fS_empty = 2000*sqrt(T_empty/V)           % about 940 Hz for T = 10 s
