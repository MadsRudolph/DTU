%% Lecture 5 - Radiation of sound: monopoles, dipoles and pistons
% 34840 Fundamentals of Acoustics and Noise Control | 29 September 2026
%
% Worked learning document for 34840_Problems5.pdf. Every formula is first
% written as an equation, then calculated in one plain MATLAB line. Lines
% without a semicolon print their result. The official answer from
% "34840_Solutions week 5.pdf" is written in the comment next to it.
%
% Constants follow the official solutions: rho = 1.2 kg/m^3, c = 344 m/s.
% SPL always uses RMS pressure. Power from a monopole uses PEAK |Q|.

%% Constants
% $$\rho c = 1.2\cdot344 = 412.8\ \mathrm{Pa\,s/m}$$
rho = 1.2;            % air density [kg/m^3]
c = 344;              % speed of sound [m/s] (the solutions use 344)
p_ref = 20e-6;        % reference RMS pressure [Pa]
I_ref = 1e-12;        % reference intensity [W/m^2]
W_ref = 1e-12;        % reference power [W]
rho_c = rho*c         % characteristic impedance [Pa s/m]

%% Problem 1 - Intensity level and power level from one SPL reading
% An omnidirectional source gives 86 dB at 1 m in an anechoic room.
% The near-field velocity is 90 degrees out of phase with pressure, so it
% carries no active intensity: I = p_rms^2/(rho c) holds at any distance.
%
% $$p_{rms} = p_{ref}\,10^{L_p/20}$$
p1 = p_ref*10^(86/20)                 % 0.399 Pa (solution: 0.4 Pa)
%
% $$I_r = \frac{p_{rms}^2}{\rho c}$$
I1 = p1^2/rho_c                       % 0.386 mW/m^2 (solution: 0.39 mW/m^2)
%
% $$L_I = 10\log_{10}(I/I_{ref})$$
L_I1 = 10*log10(I1/I_ref)             % 85.86 dB (solution: 85.9 dB)
%
% $$P_a = I_r\,4\pi r^2$$
W1 = I1*4*pi*1^2                      % 4.85 mW (solution: 4.9 mW)
%
% $$L_W = 10\log_{10}(P_a/W_{ref})$$
L_W1 = 10*log10(W1/W_ref)             % 96.86 dB (solution: 96.9 dB)
% Shortcut: L_W = L_I + 10*log10(4*pi*r^2) = 85.86 + 10.99 dB.

%% Problem 2 - SPL at 3 m and 10 m from a 20 mW monopole (250 Hz)
% Free field: the power spreads over a sphere of area 4*pi*r^2.
%
% $$p_{rms}^2 = \frac{P_a\,\rho c}{4\pi r^2},\qquad L_p = 10\log_{10}\frac{p_{rms}^2}{p_{ref}^2}$$
W2 = 20e-3;                           % sound power [W]
L_p3 = 10*log10(W2*rho_c/(4*pi*3^2)/p_ref^2)    % 82.61 dB (solution: 82.6 dB)
L_p10 = 10*log10(W2*rho_c/(4*pi*10^2)/p_ref^2)  % 72.15 dB (solution: 72.1 dB)
% Note: 72.155 rounds to 72.2; the sheet truncates to 72.1.
% The two levels differ by 20*log10(10/3) = 10.46 dB (inverse distance law).

%% Problem 3 - Same source 10 cm from a large rigid screen
% The wall is replaced by an in-phase image source 2h away (h = 0.10 m).
% The volume velocity Q is assumed unchanged by the wall.
%
% $$k = \frac{2\pi f}{c}$$
f = 250;                              % frequency [Hz]
k = 2*pi*f/c                          % 4.566 rad/m
h = 0.10;                             % source-to-wall distance [m]
kh = k*h                              % 0.457: wall is close in wavelengths
%
% $$P_{a,\mathrm{wall}} = P_{a,\mathrm{free}}\left(1+\frac{\sin 2kh}{2kh}\right)$$
W3 = W2*(1 + sin(2*kh)/(2*kh))        % 37.3 mW (solution: 37.3 mW)
%
% $$L_W = 10\log_{10}(P_a/W_{ref})$$
L_W3 = 10*log10(W3/W_ref)             % 105.72 dB (solution: 105.7 dB)
% Limit check: kh -> 0 gives a factor 2 (+3 dB); kh >> 1 gives factor 1.

%% Problem 4 - Two real sources 20 cm apart, in phase
% Exactly the problem-3 geometry (separation 2h = 0.2 m), but the "image"
% is now a real source that also radiates, so the total doubles.
%
% $$P_{a,\mathrm{total}} = 2\,P_{a,\mathrm{free}}\left(1+\frac{\sin 2kh}{2kh}\right)$$
W4 = 2*W2*(1 + sin(2*kh)/(2*kh))      % 74.7 mW (solution: 74.6 mW = 2 x 37.3)

%% Problem 5 - The same two sources in antiphase (a dipole)
% First get the volume velocity of one source from its free-field power.
%
% $$P_a = \frac{\rho c k^2 |Q|^2}{8\pi}\;\Rightarrow\;|Q| = \sqrt{\frac{8\pi P_a}{\rho c k^2}}$$
Q5 = sqrt(8*pi*W2/(rho_c*k^2))        % 0.00764 m^3/s (solution: 0.0076 m^3/s)
%
% Low-frequency dipole power (h = half the separation = 0.1 m):
% $$P_{a,\mathrm{dipole}} \approx \frac{\rho c\,h^2 k^4 |Q|^2}{6\pi}$$
W5 = rho_c*h^2*k^4*Q5^2/(6*pi)        % 5.56 mW (solution: 5.6 mW)
%
% Exact (no small-kh approximation), integrating sin^2(kh cos theta):
% $$P_{a,\mathrm{dipole}} = 2P_{a,\mathrm{free}}\left(1-\frac{\sin 2kh}{2kh}\right)$$
W5_exact = 2*W2*(1 - sin(2*kh)/(2*kh))  % 5.33 mW (solution: approx is ~5 % high)
%
% How much worse than a single source?
ratio_vs_single = W2/W5               % 3.6 x less power than ONE source
ratio_vs_inphase = W4/W5              % 13.4 x less than the in-phase pair

%% Exam A.1 - Three sirens at 3, 4 and 20 km give 74.5 dB together
% Different frequencies -> incoherent -> add mean-square pressures.
% Monopole far field: p_rms is proportional to 1/r, so p_4km = (3/4) p_3km,
% p_20km = (3/20) p_3km.
%
% $$p_{tot}^2 = p_{3}^2\left(1+\tfrac{9}{16}+\tfrac{9}{400}\right)$$
p_tot = p_ref*10^(74.5/20)            % 0.106 Pa total RMS
factor = sqrt(1 + 9/16 + 9/400)       % 1.259 (solution: 1.26)
p_3km = p_tot/factor                  % 0.0843 Pa RMS (solution: 0.0843 Pa)
L_3km = 20*log10(p_3km/p_ref)         % 72.5 dB (solution: 72.5 dB)

%% Exam A.2 - Pressure 40 m from one siren
% $$p_{40} = p_{3km}\,\frac{3000}{40},\qquad \hat p_{40} = \sqrt2\,p_{40}$$
p_40_rms = p_3km*3000/40              % 6.33 Pa RMS (110.0 dB)
p_40_peak = sqrt(2)*p_40_rms          % 8.95 Pa amplitude (solution: 8.94 Pa)

%% Multiple choice 1 - Sources A and B in antiphase
% B: two equal tones, 103 dB total -> each tone 103 - 10*log10(2) dB.
%
% $$L_{tone} = L_{tot} - 10\log_{10}2$$
L_tone_B = 103 - 10*log10(2)          % 99.99 dB, i.e. 100 dB each
% The 1000 Hz tones of A and B (both 100 dB) cancel in antiphase; the
% 1500 Hz tone of B is left alone at 100 dB.  Answer a) 100 dB SPL.

%% Multiple choice 2 - Baffled loudspeaker, then the same cone in a tube
% ka << 1, so the baffled piston is a monopole on a rigid plane:
% $$p_{rms}(r) = \frac{\rho\omega Q_{rms}}{2\pi r}\;\Rightarrow\;Q_{rms} = \frac{2\pi r\,p_{rms}}{\rho\omega}$$
a = 0.059;                            % cone radius [m]
omega = 2*pi*50;                      % [rad/s]
ka = omega/c*a                        % 0.054: monopole approximation fine
Q_mc2 = 2*pi*1*0.1/(rho*omega)        % 1.67e-3 m^3/s RMS
%
% Infinite tube: plane wave, acoustic impedance rho c / S (no decay along tube)
% $$p_{tube} = \frac{\rho c}{\pi a^2}\,Q_{rms}$$
p_tube = rho_c/(pi*a^2)*Q_mc2         % 62.9 Pa (c = 344); 62.7 Pa (c = 343). Answer c) 62.8 Pa
% Same Q assumed in both cases (the cone velocity is set by the driver).

%% Lecture extra - slide 37 source comparison (f = 40 Hz, |Q| = 0.1, h = 0.05 m)
% $$|\hat p| = \frac{\rho\omega|Q|}{4\pi r},\quad P_a = \frac{\rho c k^2|Q|^2}{8\pi}$$
k40 = 2*pi*40/c                       % 0.731 rad/m (kh = 0.037)
p_mono_5m = rho*2*pi*40*0.1/(4*pi*5)/sqrt(2)   % 0.34 Pa RMS (slide: 0.34 Pa, 84.6 dB)
W_mono = rho_c*k40^2*0.1^2/(8*pi)     % 88 mW (slide: 88 mW, 109.5 dB)
W_dip = 8*(k40*0.05)^2/6*W_mono       % 0.16 mW (slide: 0.16 mW, 82.0 dB)

%% Lecture extra - baffled piston, directivity and radiation mass
% $$D(\theta) = \frac{2J_1(ka\sin\theta)}{ka\sin\theta}$$
% -3 dB where ka*sin(theta) = 1.616, first null where ka*sin(theta) = 3.832.
ka_values = [0.5 1 2 5];
D_at_30deg = 2*besselj(1,ka_values*sin(pi/6))./(ka_values*sin(pi/6))
%
% Mechanical radiation mass of one side of a baffled piston (ka << 1):
% $$M_{m,r} = \frac{8\rho a^3}{3}$$
M_rad_65mm = 8*rho*0.065^3/3          % 0.88 g for a 6.5-inch cone (a = 65 mm)

%% The answers to remember
% P1: 85.9 dB, 96.9 dB | P2: 82.6 dB, 72.1 dB | P3: 37.3 mW, 105.7 dB
% P4: 74.6 mW | P5: 5.6 mW (exact 5.33 mW) | A.1: 0.0843 Pa (72.5 dB)
% A.2: 8.94 Pa amplitude | MC1: a) 100 dB | MC2: c) 62.8 Pa
