%% T08 - Loudspeaker driver: volume velocity, SPL, power, excursion, headphone cavity
% 34840 exam toolkit. Fill in the GIVEN block, run, read the printed lines.
%
% Solves: a moving-coil driver (Re, Bl, M, K, Rt, radius a) driven by a
% voltage, in an infinite baffle (2 pi) or as a small closed box in free
% space (4 pi). Volume velocity, far-field pressure and SPL, radiated power,
% excursion, resonance and Q, electrical impedance, piston directivity,
% closed-box stiffness, and a sealed headphone cavity.
%
% Matches: exam 2022 part 1 P1 (pre-filled: Q = 0.0022 m^3/s, |p(5 m)| =
% 0.106 Pa, W = 2.1 mW), Week 8 P3.1-3.2 (block F: 81.65 / 67.49 /
% 80.96 dB), Week 8 P4 (block G: 8.53 dB, sheet 8.55).

%% Constants
rho = 1.2;  c = 343;
rho_c = rho*c
p_ref = 20e-6;  W_ref = 1e-12;

%% GIVEN - edit these
Re = 5;                    % DC resistance [ohm]
Bl = 1*2;                  % force factor B*l [T m]
M = 10e-3;                 % moving mass [kg]
K = 1500;                  % suspension stiffness [N/m]
Rt = 2.5;                  % TOTAL damping [N s/m] (already includes (Bl)^2/Re)
a = 0.06;                  % cone radius [m]
e_rms = 4;                 % drive voltage, RMS [V] (sheet values are rms unless "amplitude")
f = 200;                   % [Hz]
r = 5;                     % distance [m]
Omega = 2*pi;              % 2*pi infinite baffle, 4*pi small box in free space

%% Step 1 - Basics
% $$S = \pi a^2,\quad \omega = 2\pi f,\quad k = \omega/c,\quad ka$$
S = pi*a^2
w = 2*pi*f;
k = w/c;
ka = k*a                   % ka < 1: monopole / omnidirectional (0.22 here)
e_hat = sqrt(2)*e_rms      % amplitude: the formulas below use peak values

%% Step 2 - Mechanical impedance and resonance
% $$Z_M = R_t + j\left(\omega M - \frac{K}{\omega}\right),\quad f_s = \frac{1}{2\pi}\sqrt{K/M},\quad Q_t = \frac{\sqrt{KM}}{R_t}$$
Z_M = Rt + 1j*(w*M - K/w)  % 2.5 + 11.37j N s/m (official)
f_s = sqrt(K/M)/(2*pi)
Q_t = sqrt(K*M)/Rt
% f >> f_s: mass controlled (flat SPL). f << f_s: stiffness controlled (-12 dB/oct).

%% Step 3 - Force, velocity, volume velocity
% $$F = Bl\,\frac{e}{R_e},\qquad U = \frac{F}{Z_M},\qquad Q = S\,U$$
F = Bl*e_hat/Re
U = F/Z_M
Q = S*U
Q_amp = abs(Q)             % 0.0022 m^3/s (official 2022 P1.1)

%% Step 4 - Far-field pressure and SPL
% $$|p| = \frac{\rho\,\omega\,|Q|}{\Omega\,r}$$
p_amp = rho*w*Q_amp/(Omega*r)          % 0.106 Pa (official)
Lp = 20*log10(p_amp/sqrt(2)/p_ref)

%% Step 5 - Radiated power
% $$W = \Omega r^2 I = \Omega r^2\frac{|p|^2}{2\rho c}$$
W = Omega*r^2*p_amp^2/(2*rho_c)        % 2.1 mW (official)
LW = 10*log10(W/W_ref)
% Same thing: baffle W = rho c k^2 |Q|^2/(4 pi); free monopole /(8 pi).
W_check = rho_c*k^2*Q_amp^2/(2*Omega)

%% Step 6 - Excursion
% $$x = \frac{U}{j\omega}$$
x_amp_mm = abs(U)/w*1e3
% Flat SPL needs constant acceleration -> x grows as 1/f^2 below the top.

%% Step 7 - Mass-controlled shortcut (f >> f_s): frequency independent
% $$|p| = \frac{\rho\,S\,Bl\,e}{\Omega\, r\, R_e\, M}\quad\text{(baffle: }\Omega = 2\pi)$$
p_mass_ctrl = rho*S*Bl*e_hat/(Omega*r*Re*M)

%% Step 8 - Electrical impedance
% $$Z_e = R_e + \frac{(Bl)^2}{Z_M}\quad(\text{+ } j\omega L_e \text{ if given})$$
Z_e = Re + Bl^2/Z_M
Z_e_at_fs = Re + Bl^2/Rt                % peak at resonance
R_electrical = Bl^2/Re                  % part of Rt that is electrical damping

%% Step 9 - Piston directivity (baffled, far field)
% $$D = \frac{2J_1(ka\sin\theta)}{ka\sin\theta}:\ -3\,\mathrm{dB}\ \text{at}\ 1.62,\ -6\,\mathrm{dB}\ \text{at}\ 2.22,\ \text{null at}\ 3.83$$
theta = 30;                             % GIVEN angle [deg]
xD = k*a*sind(theta);
D_dB = 20*log10(abs(2*besselj(1,xD)/xD))
f_minus3dB = 1.62*c/(2*pi*a*sind(theta))
f_first_null = 3.83*c/(2*pi*a*sind(theta))

%% Step 10 - Closed box adds air stiffness
% $$K_{box} = \frac{\rho c^2 S^2}{V_{box}},\qquad f_c = \frac{1}{2\pi}\sqrt{\frac{K+K_{box}}{M}}$$
V_box = 20e-3;                          % GIVEN box volume [m^3]
K_box = rho*c^2*S^2/V_box
f_c_box = sqrt((K + K_box)/M)/(2*pi)
% Internal pressure at excursion x: p = rho c^2 S x / V (Week 4 P5).

%% F - Pre-filled check: Week 8 P3 (Bl 8, Re 5, a 6 cm, M 20 g, 2.8 V rms, baffle, 2 m)
S_F = pi*0.06^2;  e_F = 2.8*sqrt(2);  w300 = 2*pi*300;  w30 = 2*pi*30;
Lp300_massctrl = 20*log10(rho*S_F*8*e_F/(2*pi*2*5*0.020)/sqrt(2)/p_ref)   % 81.65 dB (sheet)
Z30 = 18 + 1j*(w30*0.020 - 2000/w30);
Z300 = 18 + 1j*(w300*0.020 - 2000/w300);
Lp30_full = 20*log10(rho*w30*S_F*8*e_F/(5*abs(Z30))/(2*pi*2)/sqrt(2)/p_ref)     % 67.49 dB (sheet)
Lp300_full = 20*log10(rho*w300*S_F*8*e_F/(5*abs(Z300))/(2*pi*2)/sqrt(2)/p_ref)  % 80.96 dB (sheet)

%% G - Sealed cavity (headphone on the ear), then free field (Week 8 P4)
% $$C_A = \frac{V}{\rho c^2},\quad |p_{cav}| = \frac{|Q|}{\omega C_A}\ \Rightarrow\ |Q| = \omega C_A |p_{cav}|,\quad |p_{free}| = \frac{\rho\omega|Q|}{4\pi r}$$
V_cav = 50e-6;  L_cav = 100;  f_G = 100;  r_G = 0.5;   % GIVEN
C_A = V_cav/(rho*c^2)
p_cav = p_ref*10^(L_cav/20)             % 2 Pa (rms; ratio is all that matters)
Q_G = 2*pi*f_G*C_A*p_cav
Lp_free = 20*log10(rho*2*pi*f_G*Q_G/(4*pi*r_G)/p_ref)   % 8.53 dB (sheet 8.55)
% Cavity pressure follows DISPLACEMENT, free field follows ACCELERATION.
