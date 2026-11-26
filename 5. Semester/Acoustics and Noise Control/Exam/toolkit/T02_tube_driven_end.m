%% T02 - Tube / tunnel driven by a vibrating end wall (piston), any termination
% 34840 exam toolkit. Fill in the GIVEN block, run, read the printed lines.
%
% Solves: a uniform tube (or long tunnel) whose end wall vibrates with a
% known velocity amplitude U0. The other end has a termination with
% reflection coefficient R (absorber alpha = 1 -> R = 0; hard wall or
% water -> R ~ +1; open end -> R ~ -1). Gives p and u anywhere, the SPL,
% and the ideal tube resonances and pressure-node positions.
%
% Matches: exam 2023 part 1 P1.1 + P1.2 (pre-filled), Week 2 P1-P2 (tube
% resonances, nodes), Lecture 4 closed tube, ear canal (c/4L).
%
% Pre-filled with exam 2023 P1: f = 240 Hz, U0 = 1 mm/s, L = 20 m, field
% point 8 m from the vibrating wall. Official answers: 83.1 dB with the
% absorber (R = 0; the exact number is 83.3 dB, the solution rounds
% 0.413/sqrt2 to 0.286 Pa), 109.9 dB with the water-soaked absorber
% (solution approximates R = 1).
%
% Conventions: peak amplitudes, e^{j w t}. Termination at x = 0, vibrating
% wall at x = -L. Positive velocity points towards the termination.

%% Constants
rho = 1.2;                 % [kg/m^3]
c = 343;                   % [m/s]
rho_c = rho*c              % [Pa s/m]
p_ref = 20e-6;             % [Pa]

%% GIVEN - edit these
f = 240;                   % frequency [Hz]
U0 = 1e-3;                 % velocity AMPLITUDE of the vibrating wall [m/s]
L = 20;                    % tube length [m]
x_from_wall = 8;           % field point, distance from the vibrating wall [m]
Z_end = 1000*1480;         % termination impedance [Pa s/m] (water here)

%% Step 1 - Wavenumber and field point
% $$k = 2\pi f/c,\qquad x = -L + x_{wall}$$
k = 2*pi*f/c
x = -L + x_from_wall;

%% Case A - Perfect absorber at the far end (alpha = 1, R = 0): pure travelling wave
% $$|p| = \rho c\,|U_0|\quad\text{(same everywhere)}$$
p_A = rho_c*U0
Lp_A = 20*log10(p_A/sqrt(2)/p_ref)   % 83.3 dB (official 83.1, see header)

%% Case B - General termination R (here: water)
% $$R = \frac{Z_{end}-\rho c}{Z_{end}+\rho c}$$
R = (Z_end - rho_c)/(Z_end + rho_c)
%
% Field: $p = A(e^{-jkx} + R e^{jkx})$, $u = \frac{A}{\rho c}(e^{-jkx} - R e^{jkx})$.
% Velocity condition at the wall, $u(-L) = U_0$:
% $$A = \frac{\rho c\,U_0}{e^{jkL} - R\,e^{-jkL}}$$
A = rho_c*U0/(exp(1j*k*L) - R*exp(-1j*k*L))
p_B = A*(exp(-1j*k*x) + R*exp(1j*k*x))
Lp_B = 20*log10(abs(p_B)/sqrt(2)/p_ref)     % ~110 dB (official 109.9 with R = 1)
%
% Same with the official shortcut R = 1 exactly (rigid end):
A_R1 = rho_c*U0/(exp(1j*k*L) - exp(-1j*k*L))
p_R1 = A_R1*2*cos(k*x)
Lp_R1 = 20*log10(abs(p_R1)/sqrt(2)/p_ref)   % 109.9 dB (official 2023 P1.2)
% Sanity: rigid end + driven end is a closed-closed tube. The response
% blows up where sin(kL) = 0, i.e. f = n c /(2L). Check how close we are:
sin_kL = sin(k*L)
f_nearest_res = round(f/(c/(2*L)))*c/(2*L)

%% Ideal tube resonances (no driving needed)
% $$\text{open-open and closed-closed: } f_n = \frac{n c}{2L},\qquad \text{closed-open: } f_n = \frac{(2n-1)c}{4L}$$
L_tube = 0.025;            % e.g. ear canal 25 mm (closed at the drum, open at the entrance)
n = 1:4;
f_open_open = n*c/(2*L_tube)
f_closed_open = (2*n - 1)*c/(4*L_tube)      % 3.43 kHz for the ear canal
%
% Pressure NODES measured from a rigid end: d = (2n+1) lambda/4
lambda = c/1000;           % at 1 kHz, for example
d_nodes = (2*(0:3) + 1)*lambda/4
% Frequency scales with c: f2/f1 = c2/c1 = sqrt(T2/T1) (T in kelvin).
c_at_T = 20.05*sqrt(273.15 + 20)            % 343.3 m/s at 20 C
