%% T10 - Reverberation time, absorption area, diffuse-field level, sound power in a room
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: Sabine and Eyring T, the absorption area A from T, the alpha a
% surface needs for a target T, the steady-state level from L_W (direct +
% reverberant), reverberation distance, L_W from a reverberation-room
% measurement, the ISO 354 absorption coefficient, Leq of an on/off source.
%
% Matches: 2022 MC5 (block A: ceiling only -> 1.6 s), 2022 MC7 (block E:
% ISO 354 -> 0.8), 2023 MC5 (block B: walls/floor alpha -> 0.1), 2024 MC4
% (block B2: studio walls+ceiling -> 0.4), 2023 MC7 (block C: L_p at the
% receiver -> 66 dB), Week 6 P3 (block D: 1.23 Pa, Leq 91 dB, total 93 dB),
% Week 7 P1 (block F: alpha 0.45, 62 m^2), slide 30 (Sabine 0.77 s,
% Eyring 0.65 s).

%% Constants
rho = 1.2;  c = 343;
rho_c = rho*c
p_ref = 20e-6;  W_ref = 1e-12;

%% A - Room, surfaces, Sabine and Eyring (2022 MC5: absorber only on the ceiling)
lx = 10;  ly = 13;  lz = 8;            % GIVEN [m]
alpha_ceiling = 0.8;  alpha_rest = 0;  % GIVEN
V = lx*ly*lz
S_floor = lx*ly;
S_walls = 2*(lx + ly)*lz;
S = 2*S_floor + S_walls
% $$A = \sum_i S_i\alpha_i\ (+\,4mV\ \text{air}),\qquad \bar\alpha = A/S$$
A = S_floor*alpha_ceiling + (S_floor + S_walls)*alpha_rest
alpha_mean = A/S
% $$T_{Sabine} = \frac{55.3\,V}{c\,A}\approx\frac{0.16\,V}{A},\qquad T_{Eyring} = \frac{0.16\,V}{-S\ln(1-\bar\alpha)}$$
T_sabine = 55.3*V/(c*A)                % 1.6 s (official, answer C)
T_eyring = 55.3*V/(-c*S*log(1 - alpha_mean))
% Sabine for alpha_mean < 0.3, Eyring above. Absorption on ONE surface only
% -> not diffuse -> the real T is longer than both (scatterers help).
% Ceiling-only shortcut: T = 0.16 h / alpha.
T_ceiling_rule = 0.16*lz/alpha_ceiling

%% B - Unknown alpha of the other surfaces from a measured T (2023 MC5)
% 6 x 7 x 3 m, ceiling 0.8, T = 0.44 s -> walls + floor alpha?
% $$A = \frac{0.16V}{T},\qquad \alpha_x = \frac{A - S_{known}\alpha_{known}}{S_x}$$
V_B = 6*7*3;  S_ceil_B = 6*7;  S_rest_B = 6*7 + 2*(6 + 7)*3;   % GIVEN geometry
A_B = 0.16*V_B/0.44
alpha_walls_B = (A_B - S_ceil_B*0.8)/S_rest_B        % 0.10 (answer)
%
% 2024 MC4: 5 x 8 x 3 m studio, floor alpha 0.1, target T = 0.4 s -> walls + ceiling?
V_B2 = 5*8*3;  S_floor_B2 = 5*8;  S_rest_B2 = 5*8 + 2*(5 + 8)*3;
A_B2 = 0.16*V_B2/0.4
alpha_needed_B2 = (A_B2 - S_floor_B2*0.1)/S_rest_B2  % 0.37 -> option 0.4

%% C - Steady-state SPL from L_W: direct + reverberant (2023 MC7)
% $$L_p = L_W + 10\log_{10}\left(\frac{Q}{4\pi r^2}+\frac{4}{R}\right),\qquad R = \frac{A}{1-\bar\alpha}\approx A$$
LW_C = 75;  V_C = 200;  T_C = 1;  Qdir = 1;              % GIVEN
src = [1 1 1.7];  rec = [3 8 1.2];                       % GIVEN positions [m]
r_C = norm(rec - src)
A_C = 0.16*V_C/T_C
Lp_C = LW_C + 10*log10(Qdir/(4*pi*r_C^2) + 4/A_C)        % 66 dB (answer)
% Reverberation (critical) distance, direct = reverberant:
% $$r_{rev} = \sqrt{\frac{Q A}{16\pi}}\approx 0.14\sqrt{QA}$$
r_rev = sqrt(Qdir*A_C/(16*pi))
% Far from the source: L_p = L_W + 10 log10(4/A). Double A: -3 dB.

%% D - Source power -> room pressure; on/off source Leq (Week 6 P3)
% $$p^2 = \frac{4 W \rho c}{A}$$
W_D = 10e-3;  V_D = 210;  T_D = 3.1;                     % GIVEN [W], [m^3], [s]
A_D = 55.3*V_D/(c*T_D)
p2_on = 4*W_D*rho_c/A_D
p_on = sqrt(p2_on)                                       % 1.23 Pa (official)
Leq_D = 10*log10(p2_on*(5/15)/p_ref^2)                   % on 5 of 15 min -> 91 dB (official)
% Second source given as 70 dB at 4 m in free field -> W = p^2/(rho c) 4 pi r^2
W_D2 = (p_ref*10^(70/20))^2/rho_c*4*pi*4^2               % 1.95 mW (official 2 mW)
Leq_total_D = 10*log10((p2_on*(5/15) + 4*W_D2*rho_c/A_D)/p_ref^2)   % 93 dB (official)

%% E - ISO 354 absorption coefficient (reverberation room) (2022 MC7)
% $$\alpha = \frac{0.16V}{S}\left(\frac{1}{T_2}-\frac{1}{T_1}\right)\ (+\alpha_{floor})$$
V_E = 150;  S_E = 9;  T1 = 5;  T2 = 2;                   % GIVEN (T1 empty, T2 with sample)
alpha_E = 0.16*V_E/S_E*(1/T2 - 1/T1)                     % 0.8 (official, answer D)

%% F - Design: how much absorber for a target T (Week 7 P1)
V_F = 300;  T_now = 3.1;  T_target = 0.8;                % GIVEN
A_people = 40*0.42;                                      % GIVEN 40 students x 0.42 m^2
alpha_F = 0.16*200/10*(1/3.0 - 1/5.2)                    % material alpha from ISO 354: 0.45
S_needed = (0.16*V_F/T_target - 0.16*V_F/T_now - A_people)/alpha_F   % 61.4 -> 62 m^2 (sheet)

%% G - Sound power from a reverberation-room measurement
% $$L_W = \overline{L_p} + 10\log_{10}V - 10\log_{10}T - 14\ \mathrm{dB}$$
Lp_G = 85;  V_G = 200;  T_G = 4;                         % GIVEN
LW_G = Lp_G + 10*log10(V_G) - 10*log10(T_G) - 14

%% H - Diffuse-field basics
% Incident intensity on a wall: I = p^2/(4 rho c) (a quarter of the plane wave)
% Decay: L(t) = L0 - 60 t/T. T20 = 3 (t_-25 - t_-5), T30 = 2 (t_-35 - t_-5).
% Air absorption: A = sum S alpha + 4 m V.  Mean free path l_m = 4V/S.
l_m = 4*V/S
decay_rate = 60/T_sabine                                  % dB/s
% Slide 30 check: 20 x 10 x 5 m, ceiling 0.8, others 0.1
A_s30 = 200*0.8 + 500*0.1;
T_s30_sabine = 55.3*1000/(c*A_s30)                       % 0.77 s
T_s30_eyring = 55.3*1000/(-c*700*log(1 - A_s30/700))     % 0.65 s
