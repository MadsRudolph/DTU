%% T15 - Sound insulation: mass law, two rooms, composite walls, f_c, double walls
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: R from the mass law (normal / field incidence), L2 in a
% receiving room (or R from measured levels), composite walls (door,
% window, crack), the R a weak element needs, critical frequency and its
% change with thickness or stacking, single-wall model above f_c, double
% wall f0 and f_d and its gain, flanking, impact level L_n.
%
% Matches: 2023 MC8 (block B: L2 = 37.9 dB), 2023 MC10 (field = normal
% - 5 dB), 2022 MC8 (block D: window >= 40.5 dB), 2022 MC9 (block E:
% stacked plates keep f_c = 3000 Hz), 2024 MC8 (block E: 10 -> 15 cm
% concrete, -63 Hz), 2024 MC11 (block F: double gypsum +32.1 dB), sheet
% "Problems 11" P3 (block C2: window 28.5 dB), slides 18-19 (35.4 dB,
% 39.6 dB).

%% Constants
rho = 1.2;  c = 343;
rho_c = rho*c

%% A - Mass law
% $$R_0 = 20\log_{10}\frac{\omega m}{2\rho c}\approx 20\log_{10}(f m) - 42.4\ \text{(normal)},\qquad R_{field} = R_0 - 5\ \mathrm{dB}$$
% m = mass per AREA = density x thickness [kg/m^2]
m_A = 2300*0.10;  f_A = 500;             % GIVEN
R0_A = 20*log10(2*pi*f_A*m_A/(2*rho_c))
R_field_A = R0_A - 5
R_random_A = R0_A - 10*log10(0.23*R0_A)
% +6 dB per doubling of mass or frequency.

%% B - Two rooms (2023 MC8)
% $$R = L_1 - L_2 + 10\log_{10}\frac{S}{A_2},\qquad A_2 = \frac{0.16 V_2}{T_2}$$
L1_B = 80;  R_B = 40;  S_B = 4*3;  V2 = 60;  T2 = 0.5;   % GIVEN (S = PARTITION area)
A2 = 55.3*V2/(c*T2)
L2_B = L1_B - R_B + 10*log10(S_B/A2)     % 37.9 dB (official)
% Measured version: R = L1 - L2 + 10 log10(S/A2).

%% C - Composite wall (door, window, crack): add transmitted POWER
% $$\tau_i = 10^{-R_i/10},\qquad R_{res} = -10\log_{10}\frac{\sum S_i\tau_i}{\sum S_i}$$
S_i = [18 2];  R_i = [44 26];            % GIVEN areas [m^2] and R [dB] (slide 18)
R_res = -10*log10(sum(S_i.*10.^(-R_i/10))/sum(S_i))   % 35.4 dB
% Crack: aperture tau = 1 (slide 19: 10 m^2 at 50 dB, 1e-3 m^2 gap)
R_crack = -10*log10(((10 - 1e-3)*10^(-5) + 1e-3)/10)  % 39.6 dB
%
% C2 - R of one element from the result (sheet P3: 20 m^2 at 45 dB -> 40 dB with 1 m^2 window)
S_tot = 20;  R_res_C2 = 40;  S_win = 1;  R_wall = 45;   % GIVEN
R_win_C2 = -10*log10((S_tot*10^(-R_res_C2/10) - (S_tot - S_win)*10^(-R_wall/10))/S_win)   % 28.5 dB (official)

%% D - Minimum R of a window for a target total (2022 MC8)
S_tot_D = 25;  R_target = 50;  R_wall_D = 55;  S_win_D = 2;   % GIVEN
R_win_D = -10*log10((S_tot_D*10^(-R_target/10) - (S_tot_D - S_win_D)*10^(-R_wall_D/10))/S_win_D)   % 40.5 dB (official D)

%% E - Critical frequency (coincidence)
% $$B = \frac{E h^3}{12(1-\nu^2)},\quad m = \rho_M h,\quad f_c = \frac{c^2}{2\pi}\sqrt{\frac{m}{B}}\ \propto\frac1h$$
E = 2.6e10;  rho_M = 2300;  nu = 0.2;    % GIVEN concrete (2024 MC8)
h = [0.10 0.15];                         % GIVEN thicknesses [m]
B = E*h.^3/(12*(1 - nu^2))
m_E = rho_M*h
fc = c^2/(2*pi)*sqrt(m_E./B)             % 189 and 126 Hz
dfc = fc(2) - fc(1)                      % -63 Hz (official)
% Thin-plate shortcut: f_c = c^2/(1.8 c_L h), c_L = sqrt(E/(rho_M (1-nu^2)))
cL = sqrt(E/(rho_M*(1 - nu^2)));
fc_rule = c^2./(1.8*cL*h)
% n loose stacked layers: B and m both x n -> f_c UNCHANGED (2022 MC9: 3000 Hz).
% One layer of double thickness: f_c halves (1500 Hz, the trap option).
fc_stacked = 3000*sqrt(2/2)
fc_double_thick = 3000*sqrt(2/8)
% Above f_c (resonant transmission, loss factor eta):
% $$R \approx R_0 + 10\log_{10}\frac{2\eta f}{\pi f_c}$$   (rises 9 dB/octave)
eta = 0.02;
R_above_fc = R0_A + 10*log10(2*eta*f_A/(pi*fc(1)))
% Coincidence at angle theta: f_co = f_c / sin^2(theta) >= f_c.

%% F - Double wall (2024 MC11: two 13 mm gypsum boards, 1200 kg/m^3, d = 10 cm, 600 Hz)
m1 = 1200*0.013;  m2 = m1;  d = 0.10;  f_F = 600;   % GIVEN
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{\rho}{d}\left(\frac1{m_1}+\frac1{m_2}\right)},\qquad f_d = \frac{c}{2\pi d}$$
f0_dw = c/(2*pi)*sqrt(rho/d*(1/m1 + 1/m2))   % 67.7 Hz mass-air-mass resonance
fd_dw = c/(2*pi*d)                       % 546 Hz (official)
% Field mass law for each leaf (as the question says), then the range rule:
% f < f0: one wall of m1+m2. f0 < f < fd: R1 + R2 + 20 log10(2kd). f > fd: R1 + R2 + 6.
R1 = 20*log10(2*pi*f_F*m1/(2*rho_c)) - 5     % 32.08 dB (official)
R2 = 20*log10(2*pi*f_F*m2/(2*rho_c)) - 5
R_double = R1 + R2 + 6                   % f_F > f_d here
R_together = 20*log10(2*pi*f_F*(m1 + m2)/(2*rho_c)) - 5
gain_double = R_double - R_together      % 32.1 dB (official)
% If f0 < f < fd use this instead:
R_mid_range = R1 + R2 + 20*log10(2*(2*pi*f_F/c)*d)

%% G - Flanking and impact sound
% $$R' = -10\log_{10}\left(10^{-R/10}+\sum_i 10^{-R_{F,i}/10}\right),\qquad L_n = L_2 + 10\log_{10}\frac{A_2}{10}$$
R_app = -10*log10(10^(-55/10) + 4*10^(-62/10))   % 52.5 dB
Ln = 65 + 10*log10((0.161*50/0.5)/10)            % 67.1 dB
% Enclosure around a machine: Delta L = R + 10 log10(alpha_inside).
