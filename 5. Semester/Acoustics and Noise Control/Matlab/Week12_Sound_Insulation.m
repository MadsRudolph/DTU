%% Lecture 12 - Sound Insulation
% 34840 Fundamentals of Acoustics and Noise Control | 24 November 2026
%
% Worked learning document for the sound insulation lecture (Jonas
% Brunskog, deck 34840_sound_insulation_2026.pdf). The official sheet is
% 34840_Problems 11_2026.pdf (numbered 11, filed under module 12 on Learn),
% worked first against 34840_Solutions 11_2026.pdf. Then the deck's own
% examples and the sound insulation questions from the old exams (2022-2024 part 2).
% Every formula is first written as an equation, then calculated in one
% plain MATLAB line. Lines without a semicolon print their result.
%
% Expected answers (deck or official exam solution) are written in the
% comments next to each result.
%
% Constants: rho = 1.2 kg/m^3, c = 343 m/s (the 2024 exam solution uses
% these). Course text: chapter 5 of Fundamentals_of_acoustics_2022.pdf.
%
% Figures go to the vault: Images/Lecture12/.

%% Constants
rho = 1.2;            % air density [kg/m^3]
c = 343;              % speed of sound [m/s]
rho_c = rho*c         % characteristic impedance [Pa s/m]
img = fullfile('..','..','..','Obsidian','Courses', ...
    '34840 Fundamentals of Acoustics and Noise Control','Images','Lecture12');
if ~exist(img,'dir'), mkdir(img); end

%% ===== Official sheet: 34840_Problems 11_2026.pdf (sound insulation) =====
% Learn files it under module 12, but it carries the number 11. Solutions:
% 34840_Solutions 11_2026.pdf (handwritten 31200 solution + typed problem 3).

%% Sheet problem 1.1 - Radio next door, A-weighted level in the bedroom
% Partition S = 15 m^2, bedroom V = 50 m^3, octave bands 125 Hz - 4 kHz.
%
% $$L_2 = L_1 - R' + 10\log_{10}\frac{S\,T_2}{0.16\,V}$$
fo = [125 250 500 1000 2000 4000];
Rp = [40 42 49 55 61 67];
L1o = [70 77 78 78 79 75];
T2 = [1.0 1.0 1.2 1.2 1.0 0.8];
corr = 10*log10(15*T2/(0.16*50))          % 2.7 2.7 3.5 3.5 2.7 1.8 (solution: same)
L2o = L1o - Rp + corr                     % 32.7 37.7 32.5 26.5 20.7 9.8
KA = [-16.1 -8.6 -3.2 0 1.2 1.0];         % A-weighting, octave bands (Table 1.3.2)
%
% $$L_A = 10\log_{10}\sum_i 10^{0.1(L_{2,i}+K_i)}$$
LA_bed = 10*log10(sum(10.^((L2o + KA)/10)))   % 33.7 dB (sheet: 34 dB, solution 33.7)

%% Sheet problem 2.2 - Factory windows: required R
% Hall 16 x 16 x 14 m, T = 2.5 s, L1 = 89 dB(A), windows 32 m^2 with
% R = 17 dB, observation point 40 m away: measured 43 dB, limit 40 dB.
%
% $$L_2 = L_1 - R - 10\log_{10}\frac{8\pi r^2}{S}\quad\text{(2.1: diffuse inside, half-space point source outside)}$$
L2_win = 89 - 17 - 10*log10(8*pi*40^2/32)    % 41.0 dB from the windows
%
% Background from all other paths (uncorrelated, energy subtraction):
Lb = 10*log10(10^(4.3) - 10^(L2_win/10))     % 38.7 dB
L2_new = 10*log10(10^(4.0) - 10^(Lb/10))     % 34.2 dB allowed from the windows
dL_needed = L2_win - L2_new                  % 6.8 dB
%
% $$A = \frac{55.3V}{cT},\qquad A_{new} = A + S_{ceil}(\alpha_2 - \alpha_1),\qquad \Delta L = 10\log\frac{A_{new}}{A}$$
A_hall = 55.3*16*16*14/(c*2.5)               % 231 m^2
A_hall_new = A_hall + 16^2*(0.85 - 0.05)     % 436 m^2
dL_abs = 10*log10(A_hall_new/A_hall)         % 2.8 dB
R_new_windows = 17 + dL_needed - dL_abs      % 21.0 dB (sheet/solution: 21 dB)

%% Sheet problem 3 - Window cut into a wall
% Wall 20 m^2 at 45 dB; with a 1 m^2 window the total is 40 dB.
%
% $$S\tau_{res} = S_1\tau_1 + S_2\tau_2$$
tau_win = (20*10^(-4) - 19*10^(-4.5))/1      % 1.40e-3
R_win3 = -10*log10(tau_win)                  % 28.5 dB (solution: 28.5; sheet prints 28.4)

%% ===== Extra practice: deck examples and old exam questions =====

%% Problem 1 - The mass law and its "-43 dB" shortcut (slide 23)
% Normal incidence, limp wall of surface mass m:
%
% $$R_0 = 20\log_{10}\frac{\omega m}{2\rho c} = 20\log_{10}(f m) - 43$$
%
% Slide 27's example wall, m = 55 kg/m^2:
m55 = 55;
R0_55_100 = 20*log10(2*pi*100*m55/(2*rho_c))    % 32.5 dB (slide 27 plot: about 33)
R0_55_1k = 20*log10(2*pi*1000*m55/(2*rho_c))    % 52.5 dB
%
% The shortcut's constant is really $20\log_{10}(\pi/\rho c)$:
shortcut_const = 20*log10(pi/rho_c)              % -42.35 dB (slide rounds to -43)
%
% +6 dB per doubling of f or of m:
dR_double = 20*log10(2)                          % 6.02 dB

%% Problem 2 - Normal, random and field incidence (slides 40-41)
% $$R_{random} = R_0 - 10\log_{10}(0.23 R_0),\qquad R_{field} = R_0 - 5\ \mathrm{dB}$$
R_random_55_1k = R0_55_1k - 10*log10(0.23*R0_55_1k)   % 41.7 dB (about 11 dB under R0)
R_field_55_1k = R0_55_1k - 5                           % 47.5 dB
%
% 2023 exam part 2, Q10: in a diffuse field R is about ... than at normal
% incidence. Answer: 5 dB lower (field incidence).

%% Problem 3 - Two rooms: R from measured levels (slides 9-10), 2023 exam Q8
% Source room 80 dB, wall 4 m x 3 m with R = 40 dB, receiver room
% V = 60 m^3 and T = 0.5 s. Find L2.
%
% $$R = L_1 - L_2 + 10\log_{10}\frac{S}{A_2},\qquad A_2 = \frac{55.3\,V}{c\,T}$$
S_w = 4*3                                  % 12 m^2
A2 = 55.3*60/(c*0.5)                       % 19.35 m^2 (Sabine, 0.161 V/T gives 19.32)
L2 = 80 - 40 + 10*log10(S_w/A2)            % 37.9 dB (official: 37.9 dB)

%% Problem 4 - Wall with a door (slide 18)
% S1 = 18 m^2 at 44 dB, S2 = 2 m^2 at 26 dB.
%
% $$R_{res} = -10\log_{10}\Big(\frac1S\sum_i S_i\,10^{-0.1R_i}\Big)$$
R_res_door = -10*log10((18*10^(-4.4) + 2*10^(-2.6))/20)   % 35.4 dB (slide: 35 dB from the chart)

%% Problem 5 - A crack in a wall (slide 19)
% Wall 10 m^2 at 50 dB, crack 3 m x 1/3 mm with tau = 1.
S_ap = 3*(1/3)*1e-3                                       % 1e-3 m^2
R_res_crack = -10*log10(((10 - S_ap)*10^(-5) + S_ap*1)/10)   % 39.6 dB (slide: 40 dB)
% Ceiling set by the aperture alone, R <= -10 log(S_ap/S):
R_ceiling = -10*log10(S_ap/10)                            % 40 dB

%% Problem 6 - Minimum R of a window, 2022 exam part 2 Q8
% Total 25 m^2 must reach 50 dB, wall alone 55 dB, window 2 m^2.
%
% $$R_{win} = -10\log_{10}\Big(\frac{S\,10^{-0.1R_{res}} - S_{wall}10^{-0.1R_{wall}}}{S_{win}}\Big)$$
R_window = -10*log10((25*10^(-5) - 23*10^(-5.5))/2)       % 40.5 dB (official: 40.5 dB, D)

%% Problem 7 - Critical frequency of a concrete wall, 2024 exam part 2 Q8
% E = 2.6e10 Pa, rho_M = 2300 kg/m^3, nu = 0.2, eta = 0.02; h = 10 -> 15 cm.
E = 2.6e10; rho_M = 2300; nu = 0.2; eta = 0.02;
%
% $$B = \frac{E h^3}{12(1-\nu^2)},\qquad f_c = \frac{c^2}{2\pi}\sqrt{\frac{m}{B}},\qquad m = \rho_M h$$
h1 = 0.10; h2 = 0.15;
B1 = E*h1^3/(12*(1-nu^2))                 % 2.26e6 N m
m1 = rho_M*h1                             % 230 kg/m^2
fc1 = c^2/(2*pi)*sqrt(m1/B1)              % 189.0 Hz
fc2 = c^2/(2*pi)*sqrt(rho_M*h2/(E*h2^3/(12*(1-nu^2))))   % 126.0 Hz
dfc = fc2 - fc1                           % -63.0 Hz (official: -63 Hz)
% f_c is proportional to 1/h: 1.5 times thicker, f_c divided by 1.5.

%% Problem 8 - Stacking plates, 2022 exam part 2 Q9
% Two loose (unbonded) plates: B and m both double, so f_c is unchanged.
fc_stack = 3000*sqrt(2/2)                 % 3000 Hz (official: 3000 Hz, C)
% A single plate of double thickness instead: B x 8, m x 2, f_c halves.
fc_thick = 3000*sqrt(2/8)                 % 1500 Hz (the trap option B)

%% Problem 9 - The 10 cm concrete wall, all four models at 500 Hz
% $$R_0 = 20\log\frac{\omega m}{2\rho c},\quad R_{f<f_c} = R_0 + 20\log|1-(f/f_c)^2| - 5,$$
% $$R_{f\ge f_c} = R_0 + 10\log\frac{2\eta f}{\pi f_c},\quad R_{max} = 20\log\frac{\rho_M c_L}{2\rho c} - 5$$
R0_500 = 20*log10(2*pi*500*m1/(2*rho_c))                 % 58.9 dB
R_res_500 = R0_500 + 10*log10(2*eta*500/(pi*fc1))        % 44.1 dB (500 Hz is above f_c)
cL = sqrt(E/rho_M)                                       % 3362 m/s
R_max = 20*log10(rho_M*cL/(2*rho_c)) - 5                 % 74.5 dB upper limit
% Resonant drop right at f_c: 10 log(2 eta / pi)
dR_at_fc = 10*log10(2*eta/pi)                            % -19.0 dB under R0

%% Problem 10 - Upper limits for thick walls (slide 26)
% $$R_{N,max} = 20\log_{10}\frac{\rho_M c_L}{2\rho c}$$  (normal incidence)
% Typical rho_M and c_L (my values, not given on the slide):
RNmax_wood = 20*log10(500*4000/(2*rho_c))               % 67.7 dB (slide: 68)
RNmax_concrete = 20*log10(2300*3500/(2*rho_c))          % 79.8 dB (slide: 80)
RNmax_steel = 20*log10(7800*5100/(2*rho_c))             % 93.7 dB (slide: 94)

%% Problem 11 - Double gypsum wall, 2024 exam part 2 Q11
% Two 13 mm boards, rho = 1200 kg/m^3, d = 10 cm, f = 600 Hz, field mass
% law for each board.
mg = 1200*0.013                           % 15.6 kg/m^2
d = 0.10; f11 = 600;
%
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{\rho}{d}\Big(\frac1{m_1}+\frac1{m_2}\Big)},\qquad f_d = \frac{c}{2\pi d}$$
f0_dw = c/(2*pi)*sqrt(rho/d*(1/mg + 1/mg))   % 67.7 Hz mass-air-mass resonance
fd_dw = c/(2*pi*d)                           % 546 Hz (official: 546 Hz)
%
% $$R_{1}=R_{2}=20\log\frac{\omega m}{2\rho c}-5,\qquad R_{f\ge f_d}=R_1+R_2+6$$
R1_g = 20*log10(2*pi*f11*mg/(2*rho_c)) - 5   % 32.08 dB (official: 32.08 dB)
R_apart = 2*R1_g + 6                          % 70.2 dB
R_together = 20*log10(2*pi*f11*2*mg/(2*rho_c)) - 5   % 38.1 dB (one 31.2 kg/m^2 leaf)
gain_dw = R_apart - R_together                % 32.1 dB (official answer: 32.1 dB)

%% Problem 12 - Single-number rating R_w of the concrete wall (slide 13)
% Model the 10 cm wall in the 16 one-third octave bands 100-3150 Hz, then
% shift the ISO 717-1 reference curve in 1 dB steps until the sum of
% unfavourable deviations is as large as possible but <= 32 dB.
fb = [100 125 160 200 250 315 400 500 630 800 1000 1250 1600 2000 2500 3150];
R0b = 20*log10(2*pi*fb*m1/(2*rho_c));
Rb = min((fb < fc1).*(R0b + 20*log10(abs(1 - (fb/fc1).^2)) - 5) + (fb >= fc1).*(R0b + 10*log10(2*eta*fb/(pi*fc1))), R_max)
ref = [33 36 39 42 45 48 51 52 53 54 55 56 56 56 56 56] - 52;   % reference curve, 0 at 500 Hz
cand = 20:80;                                                     % candidate R_w values
unfav = sum(max(ref' + cand - Rb', 0), 1);                        % sum of unfavourable deviations
Rw_concrete = max(cand(unfav <= 32))                              % 48 dB for this model
unfav_at_Rw = unfav(cand == Rw_concrete)                          % 31.0 dB (<= 32 dB)

%% Problem 13 - Impact sound and flanking (course text 5.4 and 5.6, own numbers)
% $$L_n = L_2 + 10\log_{10}\frac{A_2}{A_0},\quad A_0 = 10\ \mathrm{m^2}$$
% Tapping machine upstairs gives L2 = 65 dB in a 50 m^3 room with T = 0.5 s.
A2_imp = 0.161*50/0.5                     % 16.1 m^2
Ln = 65 + 10*log10(A2_imp/10)             % 67.1 dB
%
% $$R' = -10\log_{10}\Big(10^{-0.1R} + \sum_i 10^{-0.1R_{F,i}}\Big)$$
% Wall R = 55 dB plus four flanking paths at 62 dB each:
R_app = -10*log10(10^(-5.5) + 4*10^(-6.2))     % 52.5 dB

%% Figure 1 - Single wall: mass law, coincidence and the upper limit
f = logspace(log10(50), log10(5000), 600);
R0f = 20*log10(2*pi*f*m1/(2*rho_c));
Rforced = R0f + 20*log10(abs(1 - (f/fc1).^2)) - 5;
Rres = R0f + 10*log10(2*eta*f/(pi*fc1));
Rmodel = min((f < fc1).*Rforced + (f >= fc1).*Rres, R_max);
fig1 = figure('Visible','off'); theme(fig1,'light');
semilogx(f, R0f, '--', 'LineWidth', 1.2); hold on;
semilogx(f, R0f - 5, ':', 'LineWidth', 1.4);
semilogx(f, Rmodel, 'LineWidth', 2);
semilogx(fb, Rb, 'o', 'MarkerSize', 5);
yline(R_max, '-.', 'upper limit 74.5 dB');
xline(fc1, ':', 'f_c = 189 Hz', 'LabelVerticalAlignment', 'bottom');
grid on; ylim([10 90]); xlim([50 5000]);
xlabel('Frequency [Hz]'); ylabel('Sound reduction index R [dB]');
legend('R_0 normal-incidence mass law', 'R_0 - 5 field incidence', 'Model: forced below f_c, resonant above', '1/3-octave values for R_w', 'Location', 'southeast');
title('10 cm concrete wall: m = 230 kg/m^2, \eta = 0.02');
exportgraphics(fig1, fullfile(img, 'Lecture12_single_wall.png'), 'Resolution', 150);

%% Figure 2 - Double gypsum wall vs the same mass in one leaf
k = 2*pi*f/c;
Rdw = 10*log10((2*pi*f*2*mg/(2*rho_c).*sin(k*d)).^2 + (2*pi*f*2*mg/(2*rho_c).*cos(k*d) - (2*pi*f).^2*mg^2/(2*rho_c^2).*sin(k*d)).^2);
Rone = 20*log10(2*pi*f*2*mg/(2*rho_c));
Rmid = 20*log10((2*pi*f).^3*mg^2*d/(2*rho^2*c^3));
Rhigh = 20*log10((2*pi*f).^2*mg^2/(2*rho_c^2));
fig2 = figure('Visible','off'); theme(fig2,'light');
semilogx(f, Rdw, 'LineWidth', 2); hold on;
semilogx(f, Rone, '--', 'LineWidth', 1.2);
semilogx(f(f>f0_dw & f<fd_dw), Rmid(f>f0_dw & f<fd_dw), ':', 'LineWidth', 1.6);
semilogx(f(f>=fd_dw), Rhigh(f>=fd_dw), '-.', 'LineWidth', 1.4);
xline(f0_dw, ':', 'f_0 = 68 Hz', 'LabelVerticalAlignment', 'bottom'); xline(fd_dw, ':', 'f_d = 546 Hz', 'LabelVerticalAlignment', 'bottom');
grid on; ylim([0 110]); xlim([50 5000]);
xlabel('Frequency [Hz]'); ylabel('R_0, normal incidence [dB]');
legend('Double wall, full mass-law model', 'Same 31.2 kg/m^2 in one leaf', 'R_1+R_2+20 log(2kd), 18 dB/oct', 'R_1+R_2+6 dB, 12 dB/oct', 'Location', 'southeast');
title('Two 13 mm gypsum boards, 10 cm apart (no absorber, no coincidence)');
exportgraphics(fig2, fullfile(img, 'Lecture12_double_wall.png'), 'Resolution', 150);
