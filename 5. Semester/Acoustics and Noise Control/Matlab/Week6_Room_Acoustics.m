%% Lecture 6 - Room modes and the diffuse sound field
% 34840 Fundamentals of Acoustics and Noise Control | 6 October 2026
%
% Worked learning document for 34840_Problems_roomacoustics6.pdf. Every
% formula is first written as an equation, then calculated in one plain
% MATLAB line. Lines without a semicolon print their result. The official
% answer from "Solution 6.pdf" (and the answers printed on the sheet) is
% written in the comment next to it.
%
% Room acoustics uses RMS pressures throughout: p^2 is a mean square.
% c = 343 m/s at 20 degrees C (the sheet's answers need 343, not 344).

%% Constants
% $$\rho c = 1.2\cdot343 = 411.6\ \mathrm{Pa\,s/m}$$
rho = 1.2;            % air density [kg/m^3]
c = 343;              % speed of sound at 20 C [m/s]
p_ref = 20e-6;        % reference RMS pressure [Pa]
W_ref = 1e-12;        % reference power [W]
rho_c = rho*c         % characteristic impedance [Pa s/m]

%% Problem 1.1 - Natural frequencies below 80 Hz in a 5 x 4 x 3 m room
% $$f_{n_x,n_y,n_z} = \sqrt{\left(n_x\frac{c}{2l_x}\right)^2+\left(n_y\frac{c}{2l_y}\right)^2+\left(n_z\frac{c}{2l_z}\right)^2}$$
% First the three axial "building blocks" c/(2l):
lx = 5; ly = 4; lz = 3;               % room dimensions [m]
fx = c/(2*lx)                         % 34.30 Hz = (1,0,0)
fy = c/(2*ly)                         % 42.88 Hz = (0,1,0)
fz = c/(2*lz)                         % 57.17 Hz = (0,0,1)
%
% Then combine them, lowest first:
f_100 = fx                            % 34.3 Hz axial      (sheet: 34.3; Solution 6 prints 34.4, a slip)
f_010 = fy                            % 42.9 Hz axial      (solution: 42.9 Hz)
f_110 = sqrt(fx^2 + fy^2)             % 54.9 Hz tangential (solution: 54.9 Hz)
f_001 = fz                            % 57.2 Hz axial      (solution: 57.2 Hz)
f_101 = sqrt(fx^2 + fz^2)             % 66.7 Hz tangential (solution: 66.7 Hz)
f_200 = 2*fx                          % 68.6 Hz axial      (solution: 68.6 Hz)
f_011 = sqrt(fy^2 + fz^2)             % 71.5 Hz tangential (solution: 71.5 Hz)
f_111 = sqrt(fx^2 + fy^2 + fz^2)      % 79.3 Hz oblique    (solution: 79.3 Hz)
f_210 = sqrt((2*fx)^2 + fy^2)         % 80.9 Hz: first mode ABOVE 80 Hz
%
% Check with the mode-count formula (V = 60 m^3, S = 94 m^2, L = 48 m):
% $$N(f) \approx \frac{4\pi V}{3}\left(\frac fc\right)^3+\frac{\pi S}{4}\left(\frac fc\right)^2+\frac L8\frac fc$$
V1 = lx*ly*lz;                        % 60 m^3
S1 = 2*(lx*ly + lx*lz + ly*lz);       % 94 m^2
L1 = 4*(lx + ly + lz);                % 48 m
N_80 = 4*pi*V1/3*(80/c)^3 + pi*S1/4*(80/c)^2 + L1/8*80/c   % 8.6 (8 counted above)

%% Problem 1.2 - Which modes have a pressure maximum at the centre?
% $$p \propto \cos\left(\frac{n\pi}{2}\right)\ \text{at the centre: zero for odd } n$$
cos_centre_n1 = cos(1*pi/2)           % 6e-17, i.e. 0: (1,0,0) has a nodal plane through the centre
cos_centre_n2 = cos(2*pi/2)           % -1: (2,0,0) has a maximum there
% Only modes with ALL indices even qualify -> only (2,0,0). (solution: (2,0,0))

%% Problem 1.3 - Modes in the 50 Hz one-third octave band
% $$f_l = \frac{f_c}{2^{1/6}},\qquad f_u = f_c\,2^{1/6}$$
f_l = 50/2^(1/6)                      % 44.5 Hz (solution: 44.5 Hz)
f_u = 50*2^(1/6)                      % 56.1 Hz (solution: 56.1 Hz)
% 42.9 < 44.5 and 57.2 > 56.1, so only (1,1,0) at 54.9 Hz is inside.

%% Problem 2 - Degenerate modes in a 3 x 3 x 3 m cube
% $$f = \frac{c}{2l}\sqrt{n_x^2+n_y^2+n_z^2}$$
% Every permutation of the indices gives the same frequency.
f_cube = c/(2*3)                      % 57.17 Hz
f_sum1 = f_cube*sqrt(1)               % 57.2 Hz:  (1,0,0) (0,1,0) (0,0,1)            (solution: 57 Hz)
f_sum2 = f_cube*sqrt(2)               % 80.8 Hz:  (1,1,0) (1,0,1) (0,1,1)            (solution: 81 Hz)
f_sum3 = f_cube*sqrt(3)               % 99.0 Hz:  (1,1,1) ONLY -> not degenerate, skip it
f_sum4 = f_cube*sqrt(4)               % 114.3 Hz: (2,0,0) (0,2,0) (0,0,2)            (solution: 114 Hz)
f_sum5 = f_cube*sqrt(5)               % 127.8 Hz: six permutations of (2,1,0)        (solution: 128 Hz)

%% Problem 3.1 - Intermittent 10 mW source in a reverberant room
% Get the equivalent absorption area from Sabine's formula:
% $$T = \frac{55.3\,V}{c\,A}\;\Rightarrow\;A = \frac{55.3\,V}{c\,T}$$
P1 = 10e-3;                           % source power [W]
V3 = 210;                             % room volume [m^3]
T3 = 3.1;                             % reverberation time [s]
A3 = 55.3*V3/(c*T3)                   % 10.92 m^2
%
% Steady-state reverberant field while the source is on:
% $$p_s^2 = \frac{4P_a\rho c}{A}$$
p_on2 = 4*P1*rho_c/A3                 % 1.508 Pa^2
p_on = sqrt(p_on2)                    % 1.23 Pa (solution: 1.23 Pa)
L_on = 10*log10(p_on2/p_ref^2)        % 95.8 dB while the source runs
%
% On 5 of every 15 minutes: average the MEAN SQUARE over time.
% $$L_{eq} = 10\log_{10}\frac{p_{on}^2/3}{p_{ref}^2}$$
L_eq1 = 10*log10(p_on2/3/p_ref^2)     % 91.0 dB (solution: 91 dB)
%
% Is the room really diffuse / reverberant at 500 Hz?
% $$r_{rev} = \sqrt{\frac{A}{16\pi}},\qquad f_S \approx 2000\sqrt{T/V}$$
r_rev3 = sqrt(A3/(16*pi))             % 0.47 m: reverberant almost everywhere
f_Schroeder = 2000*sqrt(T3/V3)        % 243 Hz, well below 500 Hz

%% Problem 3.2 - Add a continuous source (70 dB at 4 m in free field)
% Power from the free-field level (monopole: I = p^2/(rho c) at any r):
% $$P_a = \frac{p_{ff}^2}{\rho c}4\pi r^2$$
p_ff2 = (p_ref*10^(70/20))^2          % 0.0040 Pa^2 (0.063 Pa)
P2 = p_ff2/rho_c*4*pi*4^2             % 1.95 mW (solution: 2 mW)
%
% Its reverberant pressure in the room:
% $$p_2^2 = \frac{4P_2\rho c}{A}$$
p2_2 = 4*P2*rho_c/A3                  % 0.295 Pa^2
p2 = sqrt(p2_2)                       % 0.54 Pa (solution: 0.54 Pa)
L2 = 10*log10(p2_2/p_ref^2)           % 88.7 dB
%
% Uncorrelated sources: add mean squares.
% $$L_{eq} = 10\log_{10}\frac{p_{on}^2/3 + p_2^2}{p_{ref}^2}$$
L_eq_total = 10*log10((p_on2/3 + p2_2)/p_ref^2)   % 93.0 dB (solution: 93 dB)

%% Lecture extra - slide 30 / text Fig. 3.4.3: Sabine vs Eyring
% 20 x 10 x 5 m, ceiling alpha = 0.8, other surfaces alpha = 0.1.
% $$A = \sum S_i\alpha_i,\quad \bar\alpha = A/S$$
V4 = 20*10*5                          % 1000 m^3
S4 = 2*(20*10 + 20*5 + 10*5)          % 700 m^2
A4 = 200*0.8 + 500*0.1                % 210 m^2
alpha_m = A4/S4                       % 0.30
%
% $$T_{Sabine} = \frac{55.3\,V}{cA},\qquad T_{Eyring} = \frac{55.3\,V}{-cS\ln(1-\bar\alpha)}$$
T_sabine = 55.3*V4/(c*A4)             % 0.77 s (text: 0.8 s)
T_eyring = 55.3*V4/(-c*S4*log(1 - alpha_m))   % 0.65 s (text: 0.6 s)
%
% One-dimensional decay along the 20 m length (hard end walls):
% $$T = \frac{13.8\,l_m}{c\,\bar\alpha}$$
T_length = 13.8*20/(c*0.1)            % 8.0 s (text: 8.0 s) - non-diffuse rooms ring much longer

%% Lecture extra - steady-state level vs distance, reverberation distance
% $$L_p = L_W + 10\log_{10}\left(\frac{1}{4\pi r^2}+\frac{4}{A}\right)$$
LW = 100;                             % example source, 10 mW
Lp_1m = LW + 10*log10(1/(4*pi*1^2) + 4/A3)    % 96.5 dB at 1 m: already within 1 dB of the reverberant limit
Lp_far = LW + 10*log10(4/A3)          % 95.6 dB: the reverberant limit
% The 0.14 dB constant that the dB form neglects:
% $$10\log_{10}\frac{\rho c\,P_{ref}}{A_0\,p_{ref}^2}$$
const_dB = 10*log10(rho_c*W_ref/(1*p_ref^2))  % 0.12 dB here (text: 0.14 dB with rho = 1.204)

%% The answers to remember
% 1.1: 34.3, 42.9, 54.9, 57.2, 66.7, 68.6, 71.5, 79.3 Hz | 1.2: (2,0,0)
% 1.3: (1,1,0) only | 2: 57, 81, 114, 128 Hz | 3.1: 91 dB | 3.2: 93 dB
