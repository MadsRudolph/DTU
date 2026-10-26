%% Lecture 8 - Loudspeakers
% 34840 Fundamentals of Acoustics and Noise Control | 27 October 2026
%
% Worked learning document for 34840_Problems_8.pdf. Every formula is
% first written as an equation, then calculated in one plain MATLAB line.
% Lines without a semicolon print their result.
%
% No official solutions yet: the answers are my own, DERIVED, NOT YET
% CHECKED AGAINST OFFICIAL SOLUTIONS. The sheet prints final answers, and
% they are written in the comments next to each result.
%
% Constants: rho = 1.2 kg/m^3, c = 343 m/s (these reproduce the sheet).

%% Constants
rho = 1.2;            % air density [kg/m^3]
c = 343;              % speed of sound [m/s]
rho_c = rho*c         % characteristic impedance [Pa s/m]
p_ref = 20e-6;        % reference pressure [Pa]
I_0 = 1e-12;          % reference intensity [W/m^2]
W_0 = 1e-12;          % reference power [W]

%% Problem 1 - Small Bluetooth speaker in free space (monopole, 4*pi)
% Amplitude 0.1 Pa at 1 m, below 100 Hz, size < 6 cm, so ka << 1.
%
% $$p_{rms}(r) = \frac{\hat p_1}{\sqrt2}\,\frac{1\,\mathrm m}{r}$$
p1_rms = 0.1/sqrt(2)                  % 0.0707 Pa at 1 m
p075 = p1_rms/0.75                    % 0.0943 Pa at 0.75 m
Lp_075 = 20*log10(p075/p_ref)         % 73.47 dB (sheet: 73.46)
%
% $$I = \frac{p_{rms}^2}{\rho c}\quad\text{(any distance, for a monopole)}$$
I_075 = p075^2/rho_c                  % 2.16e-5 W/m^2
LI_075 = 10*log10(I_075/I_0)          % 73.34 dB (sheet: 73.34)
%
% $$W = 4\pi r^2 I$$
W1 = 4*pi*1^2*p1_rms^2/rho_c          % 1.527e-4 W (sheet: 0.000153 W)
LW1 = 10*log10(W1/W_0)                % 81.84 dB (sheet: 81.83)

%% Problem 2 - Speaker in an infinite baffle (half space, 2*pi)
% a = 5 cm, 50 Hz, 78 dB at 2.5 m.
%
% $$L_p(r_2) = L_p(r_1) + 20\log_{10}\frac{r_1}{r_2}$$
ka2 = 2*pi*50/c*0.05                  % 0.046, a monopole on a rigid plane
Lp_1m = 78 + 20*log10(2.5/1)          % 85.96 dB (sheet: 85.96)
p_1m = p_ref*10^(Lp_1m/20)            % 0.397 Pa
I_1m = p_1m^2/rho_c                   % 3.83e-4 W/m^2
LI_1m = 10*log10(I_1m/I_0)            % 85.83 dB (sheet: 85.83)
%
% $$W = 2\pi r^2 I\quad\text{(hemisphere)}$$
W2 = 2*pi*1^2*I_1m                    % 2.41e-3 W (sheet: 0.0024 W)
LW2 = 10*log10(W2/W_0)                % 93.82 dB (sheet: 93.82)

%% Problem 3.1 - Mass-controlled driver in a baffle
% Bl = 8 Tm, Re = 5 ohm, a = 6 cm, M = 20 g, 2.8 V rms, r = 2 m.
Bl = 8; Re = 5; a = 0.06; M = 0.020; e_g = 2.8; r = 2;
S = pi*a^2                            % 0.01131 m^2
%
% $$Q = \frac{S\,Bl\,e_g}{j\omega R_e M}$$
w300 = 2*pi*300;
w900 = 2*pi*900;
Q300 = S*Bl*e_g/(w300*Re*M)           % 1.344e-3 m^3/s (sheet: 1.34e-3)
Q900 = S*Bl*e_g/(w900*Re*M)           % 0.448e-3 m^3/s (sheet: 0.448e-3)
%
% $$p = \frac{\rho\,\omega\,Q}{2\pi r}$$
Lp300 = 20*log10(rho*w300*Q300/(2*pi*r)/p_ref)   % 81.65 dB (sheet: 81.65)
Lp900 = 20*log10(rho*w900*Q900/(2*pi*r)/p_ref)   % 81.65 dB (sheet: 81.65)
%
% The frequency drops out: $p = \rho S Bl e_g / (2\pi r R_e M)$.
p_flat = rho*S*Bl*e_g/(2*pi*r*Re*M)   % 0.242 Pa

%% Problem 3.2 - Add the suspension K and the total damping Rt
K = 2000; Rt = 18;
%
% $$f_s = \frac{1}{2\pi}\sqrt{K/M},\qquad Q_t = \frac{\sqrt{KM}}{R_t}$$
f_s = sqrt(K/M)/(2*pi)                % 50.3 Hz
Q_t = sqrt(K*M)/Rt                    % 0.35
R_el = Bl^2/Re                        % 12.8 Ns/m of the 18 is electrical damping
%
% $$Z_M = j\omega M + R_t + \frac{K}{j\omega}$$
w30 = 2*pi*30;
Z30 = 1j*w30*M + Rt + K/(1j*w30)      % 18 - 6.84j Ns/m (spring wins)
Z300 = 1j*w300*M + Rt + K/(1j*w300)   % 18 + 36.64j Ns/m (mass wins)
%
% $$|p| = \frac{\rho\omega}{2\pi r}\,\frac{S\,Bl\,e_g}{R_e\,|Z_M|}$$
Lp30_k = 20*log10(rho*w30*S*Bl*e_g/(Re*abs(Z30))/(2*pi*r)/p_ref)    % 67.49 dB (sheet: 67.49)
Lp300_k = 20*log10(rho*w300*S*Bl*e_g/(Re*abs(Z300))/(2*pi*r)/p_ref) % 80.96 dB (sheet: 80.96)
%
% Excursion $x = U/j\omega$ at the two frequencies [mm rms]:
x30 = S*Bl*e_g/(Re*abs(Z30))/S/w30*1e3       % 1.23 mm
x300 = S*Bl*e_g/(Re*abs(Z300))/S/w300*1e3    % 0.058 mm

%% Problem 4 - Headphone on the head, then off
% 100 dB in 50 cm^3 at 100 Hz, sealed. Then free space at 0.5 m.
%
% $$C_A = \frac{V}{\rho c^2},\qquad p = \frac{Q}{j\omega C_A}$$
V = 50e-6;
C_A = V/(rho*c^2)                     % 3.54e-10 m^5/N
p_in = p_ref*10^(100/20)              % 2 Pa
w100 = 2*pi*100;
Q_hp = w100*C_A*p_in                  % 4.45e-7 m^3/s
%
% $$p_{free} = \frac{\rho\omega Q}{4\pi r}$$
p_free = rho*w100*Q_hp/(4*pi*0.5)     % 5.34e-5 Pa
Lp_free = 20*log10(p_free/p_ref)      % 8.53 dB (sheet: 8.55; c = 343 vs ~342.6)
ka4 = w100/c*0.02                     % 0.037, so a small monopole
