%% T07 - Two (or more) monopoles: interference, line between sources, rigid wall, dipole
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: total complex pressure, particle velocity and intensity on the
% line between two monopoles (in phase or antiphase), cancellation
% frequencies/positions, a monopole near a rigid wall (image source:
% power and intensity), dipole power, and pressure from any number of
% sources at any 2-D positions (subwoofer arrays).
%
% Matches: exam 2024 part 1 P2.2 (pre-filled block A: p_rms 24/0/24 mPa,
% u_rms 82.2/58.7/82.2 um/s, I = +459.3/0/-459.3 nW/m^2), exam 2023 part 1
% P3 (block B: wall power 32.7/36.6/54.4 uW, intensity 0/0.78/2.45 uW/m^2
% - the official numbers are ~2 % low, they appear to use rho ~ 1.18),
% exam 2022 part 1 P3 (block C: 1500/2500 Hz, x_c = 2.172 m, Q1/Q2 = 1.188,
% I = 8.33 uW/m^2), hand-in P2.3 (block E), Week 5 P3-P5, slide 37.

%% Constants
rho = 1.2;  c = 343;
rho_c = rho*c
p_ref = 20e-6;

%% A - Two sources on the x axis, field points between them (2024 P2.2)
% Source 1 at x = 0, source 2 at x = D. Positive direction = from 1 to 2.
f_A = 500;  D = 0.4;                    % GIVEN [Hz], spacing [m]
Q1 = 1e-5;  Q2 = -1e-5;                 % GIVEN complex Q amplitudes (antiphase: minus)
x = [0.1 0.2 0.3];                      % GIVEN field points on the line [m]
w_A = 2*pi*f_A;  k_A = w_A/c;
r1 = x;  r2 = D - x;
%
% $$p_i = \frac{j\omega\rho Q_i}{4\pi r_i}e^{-jkr_i},\qquad p = p_1 + p_2$$
p1 = 1j*w_A*rho*Q1./(4*pi*r1).*exp(-1j*k_A*r1);
p2 = 1j*w_A*rho*Q2./(4*pi*r2).*exp(-1j*k_A*r2);
p_tot = p1 + p2                         % 0.02 + 0.0275j Pa at x = 0.1 (official)
p_rms_A = abs(p_tot)/sqrt(2)            % 24, 0, 24 mPa (official)
%
% Velocity along +x: source 1 pushes outward = +x, source 2 outward = -x.
% $$u_x = \frac{p_1}{\rho c}\left(1+\frac{1}{jkr_1}\right) - \frac{p_2}{\rho c}\left(1+\frac{1}{jkr_2}\right)$$
u_tot = p1/rho_c.*(1 + 1./(1j*k_A*r1)) - p2/rho_c.*(1 + 1./(1j*k_A*r2))
u_rms_A = abs(u_tot)/sqrt(2)            % 82.2, 58.7, 82.2 um/s (official)
%
% $$I_x = \tfrac12\Re\{p\,u_x^*\}$$
I_A = 0.5*real(p_tot.*conj(u_tot))      % +459.3, 0, -459.3 nW/m^2 (official)

%% B - Monopole at distance h from a rigid wall (2023 P3) = source + image
% Power, h = 2 m, three frequencies with their own Q:
% $$W = \frac{\rho c k^2|Q|^2}{8\pi}\left(1+\frac{\sin 2kh}{2kh}\right)$$
h = 2;                                  % GIVEN distance source-wall [m]
f_B = [20 200 2000];                    % GIVEN [Hz]
Q_B = [3e-3 4e-4 5e-5];                 % GIVEN amplitudes [m^3/s]
k_B = 2*pi*f_B/c
kh = k_B*h
W_wall = rho_c*k_B.^2.*Q_B.^2/(8*pi).*(1 + sin(2*kh)./(2*kh))   % 33.2/37.3/55.3 uW (official 32.7/36.6/54.4)
W_free = rho_c*k_B.^2.*Q_B.^2/(8*pi)
gain_dB = 10*log10(W_wall./W_free)      % kh -> 0: +3 dB. kh > pi/2: ~0 dB.
%
% Intensity on the line source -> wall, 200 Hz. Image source at 2h.
% r = distance from the real source; the image is at 2h - r on the far side.
f_B2 = 200;  Q_B2 = 4e-4;               % GIVEN
r_B = [2 1.5 1];                        % 0, 0.5, 1 m from the wall
w_B = 2*pi*f_B2;  k_B2 = w_B/c;
pr = 1j*w_B*rho*Q_B2./(4*pi*r_B).*exp(-1j*k_B2*r_B);                 % real source
pim = 1j*w_B*rho*Q_B2./(4*pi*(2*h - r_B)).*exp(-1j*k_B2*(2*h - r_B)); % image (in phase)
abs_pr = abs(pr)                        % 0.0240 0.0320 0.0480 Pa (official 0.0236 0.0315 0.0472)
abs_pim = abs(pim)
% Official shortcut (two opposite travelling waves, cross terms ignored):
% $$I \approx \frac{|p_1|^2-|p_2|^2}{2\rho c}$$
I_B_simple = (abs(pr).^2 - abs(pim).^2)/(2*rho_c)   % 0 / 0.80 / 2.49 uW/m^2 (official 0 / 0.78 / 2.45)
% Exact, with near-field terms (velocity towards the wall = +):
u_B = pr/rho_c.*(1 + 1./(1j*k_B2*r_B)) - pim/rho_c.*(1 + 1./(1j*k_B2*(2*h - r_B)));
I_B_exact = 0.5*real((pr + pim).*conj(u_B))
% Sanity: I = 0 AT the rigid wall (u = 0 there).

%% C - In-phase sources D apart: where/when do they cancel? (2022 P3)
D_C = 4;  f0_C = 500;  Lp_mid = 80;     % GIVEN spacing [m], lowest cancel freq [Hz], SPL at midpoint
% Cancellation needs equal |p| and 180 deg: path difference = odd half wavelengths.
% $$\Delta x = \frac{\lambda_0}{2} = \frac{c}{2f_0},\qquad f_n = (2n+1)f_0$$
f_cancel = (2*(0:3) + 1)*f0_C           % 500 1500 2500 3500 Hz (official)
dx = c/(2*f0_C)
x_c = D_C/2 + dx/2                      % 2.172 m from source 1 (official)
% Equal |p| at x_c: |Q1|/x_c = |Q2|/(D - x_c)
Q1_over_Q2 = x_c/(D_C - x_c)            % 1.188: source 1 must be 18.8 % stronger (official)
% Midpoint, in phase: p1 + p2 = p_rms,tot with p1 = 1.188 p2. Opposite directions:
p_rms_mid = p_ref*10^(Lp_mid/20)        % 0.2 Pa
p2_mid = p_rms_mid/(1 + Q1_over_Q2)
p1_mid = Q1_over_Q2*p2_mid
I_C = (p1_mid^2 - p2_mid^2)/rho_c       % 8.33 uW/m^2 (official), towards source 2

%% D - Dipole: two antiphase monopoles 2h apart
% $$W = \frac{\rho c k^2|Q|^2}{4\pi}\left(1-\frac{\sin 2kh}{2kh}\right)\approx\frac{\rho c h^2k^4|Q|^2}{6\pi}\quad(kh\ll1)$$
f_D = 40;  Q_D = 0.1;  h_D = 0.05;      % GIVEN (slide 37: kh = 0.037)
k_D = 2*pi*f_D/c;
W_dip = rho_c*k_D^2*Q_D^2/(4*pi)*(1 - sin(2*k_D*h_D)/(2*k_D*h_D))
W_dip_small = rho_c*h_D^2*k_D^4*Q_D^2/(6*pi)
W_mono = rho_c*k_D^2*Q_D^2/(8*pi)
dip_vs_mono_dB = 10*log10(W_dip/W_mono) % about -27.5 dB: a dipole is a poor low-f radiator
% Far field: p = rho w Q/(2 pi r) sin(kh cos(theta)): figure-of-eight, null at 90 deg.

%% E - Any number of sources at any 2-D positions (pressure only)
% $$p(\mathbf x) = \sum_i \frac{j\omega\rho Q_i}{4\pi |\mathbf x-\mathbf x_i|}e^{-jk|\mathbf x-\mathbf x_i|}$$
f_E = 20;                               % GIVEN [Hz]
xs = [-10 10];  ys = [0 0];             % GIVEN source positions [m] (example values)
Qs = [1 1]*0.01;                        % GIVEN complex Q of each source [m^3/s]
xp = [-20 -10 0 10 20];  yp = [19 19 19 19 19];   % GIVEN field points [m]
k_E = 2*pi*f_E/c;
r_E = sqrt((xp(:) - xs).^2 + (yp(:) - ys).^2);    % rows = points, columns = sources
p_E = (1j*2*pi*f_E*rho*exp(-1j*k_E*r_E)./(4*pi*r_E))*Qs(:)
Lp_E = 20*log10(abs(p_E)/sqrt(2)/p_ref)
% Calibrate Q from "each source gives L0 at point X": |Q| = 4 pi r p_amp/(w rho).
