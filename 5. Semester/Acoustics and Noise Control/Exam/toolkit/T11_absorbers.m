%% T11 - Absorbers: porous (lambda/4), membrane, Helmholtz, perforated panel, alpha from Z
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: resonance frequency of membrane / Helmholtz / perforated-panel
% absorbers (and the reverse: depth, volume or mass for a target f), the
% porous-absorber lambda/4 frequency, alpha at normal, oblique and random
% incidence from a surface impedance, alpha from a standing-wave ratio,
% reflected level.
%
% Matches: Week 7 P2.1 (block A: 77 Hz), Week 7 P2.2 (block C: 432 Hz),
% 2023 MC6 (block A2: 2.1 kg/m^2, 0.1 m -> 130 Hz), 2024 MC7 (block A3:
% 350 Hz, 0.2 kg/m^2 -> 15 cm), 2024 MC6 (block B2: Helmholtz 140 Hz ->
% 0.015 m^3), Week 4 P1 (block B: bottle 334 Hz), slide 36 (block E:
% alpha_n 0.451, alpha_r 0.53), 2022 MC6 (block F: Z = 1 gives the
% smallest alpha 0.0097), slide 5 (reflected 67/60/50 dB).

%% Constants
rho = 1.2;  c = 343;
rho_c = rho*c
rho_c2 = rho*c^2           % 1.41e5 Pa

%% A - Membrane (panel) absorber
% $$f_r = \frac{1}{2\pi}\sqrt{\frac{\rho c^2}{m L}}\approx\frac{60}{\sqrt{mL}}$$
% m = mass per AREA [kg/m^2] = density x thickness, L = cavity depth [m]
m_panel = 600*0.020                    % GIVEN 20 mm plywood, 600 kg/m^3 -> 12 kg/m^2
L_cav = 0.050;                         % GIVEN cavity depth [m]
f_membrane = 1/(2*pi)*sqrt(rho_c2/(m_panel*L_cav))   % 77 Hz (sheet)
f_rule = 60/sqrt(m_panel*L_cav)
% 2023 MC6: m = 2.1 kg/m^2, L = 0.1 m
f_A2 = 1/(2*pi)*sqrt(rho_c2/(2.1*0.1))             % 130 Hz (answer)
% Reverse, 2024 MC7: depth for 350 Hz with m = 0.2 kg/m^2
% $$L = \frac{\rho c^2}{m(2\pi f_r)^2}$$
L_A3 = rho_c2/(0.2*(2*pi*350)^2)                    % 0.146 m -> 15 cm (answer)

%% B - Helmholtz resonator
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{s}{V\,l_{eff}}},\qquad s = \frac{\pi d^2}{4},\qquad l_{eff} = l + \delta,\ \delta\approx0.8d$$
% (If the sheet gives the EFFECTIVE length, do not add delta again.)
V_B = 400e-6;  d_B = 0.020;  l_eff_B = 0.021;       % GIVEN Week 4 P1 bottle
s_B = pi*d_B^2/4
f_helmholtz = c/(2*pi)*sqrt(s_B/(V_B*l_eff_B))      % 334 Hz (sheet)
% Reverse, 2024 MC6: volume for 140 Hz, neck d = 5 cm, l = 2 cm, no end correction
% $$V = \frac{s}{l_{eff}}\left(\frac{c}{2\pi f_0}\right)^2$$
s_B2 = pi*0.05^2/4;
V_B2 = s_B2/0.02*(c/(2*pi*140))^2                   % 0.0149 m^3 -> 0.015 (answer)

%% C - Perforated panel absorber
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{P}{L(l+\delta)}},\qquad P = \frac{\pi d^2}{4a^2}\ \text{(holes d on a square grid a)}$$
d_C = 0.010;  a_C = 0.030;  l_C = 0.020;  L_C = 0.050;   % GIVEN hole, grid, panel thickness, cavity
P_C = pi*d_C^2/(4*a_C^2)                            % 0.087 (a FRACTION, not %)
delta_C = 0.8*d_C
f_perf = c/(2*pi)*sqrt(P_C/(L_C*(l_C + delta_C)))   % 431 Hz with c = 343 (sheet 432 uses c = 344)

%% D - Porous absorber: works above the lambda/4 frequency (distance from the WALL)
% $$f_{min}\approx\frac{c}{4d}\ \ (\text{peaks at } d=\lambda/4, 3\lambda/4,\ \text{dip at } \lambda/2)$$
d_D = 0.07;                                         % GIVEN distance/thickness [m]
f_quarter = c/(4*d_D)
f_half_dip = c/(2*d_D)
% Diffuse incidence: already good above d = lambda/8.

%% E - alpha from surface impedance Z (slide 36, Z = 500 + 1000j, slide used rho c = 414)
Z = 500 + 1000j;                                    % GIVEN [N s/m^3]
z0 = 414;                                           % use rho_c in the exam
% Normal: $$R = \frac{Z-\rho c}{Z+\rho c},\quad \alpha_n = 1-|R|^2$$
R_n = (Z - z0)/(Z + z0)
alpha_n = 1 - abs(R_n)^2                            % 0.451 (slide)
% Oblique (locally reacting): $$R(\theta) = \frac{Z\cos\theta-\rho c}{Z\cos\theta+\rho c}$$
theta = 45;
alpha_theta = 1 - abs((Z*cosd(theta) - z0)/(Z*cosd(theta) + z0))^2
% Random (Paris), with zeta = Z/(rho c) = r + jx (NORMALISE FIRST):
zeta = Z/z0;  r = real(zeta);  x = imag(zeta);
% $$\alpha_r = \frac{8r}{r^2+x^2}\left[1-\frac{r}{r^2+x^2}\ln\left((r+1)^2+x^2\right)+\frac{r^2-x^2}{x(r^2+x^2)}\tan^{-1}\frac{x}{r+1}\right]$$
alpha_r = 8*r/(r^2+x^2)*(1 - r/(r^2+x^2)*log((r+1)^2+x^2) + (r^2-x^2)/(x*(r^2+x^2))*atan(x/(r+1)))   % 0.53 (slide)
% Same by numerical integration (works for x = 0 too):
% $$\alpha_r = \int_0^{\pi/2}\alpha(\theta)\sin 2\theta\,d\theta$$
alpha_r_int = integral(@(th) (1 - abs((zeta*cos(th) - 1)./(zeta*cos(th) + 1)).^2).*sin(2*th), 0, pi/2)

%% F - Which impedance absorbs least? (2022 MC6, normal incidence)
Z_F = [1 100 1000 10000];
alpha_F = 1 - abs((Z_F - rho_c)./(Z_F + rho_c)).^2    % 0.0097 0.63 0.83 0.15 -> Z = 1 (answer A)
% Best match Z = rho c gives alpha = 1. Very low OR very high Z reflects.

%% G - Standing-wave ratio n (pressure ratio, NOT dB) and reflected level
% $$\alpha_0 = 1-\left(\frac{n-1}{n+1}\right)^2 = \frac{4n}{(n+1)^2}$$
n_G = 3;
alpha_G = 1 - ((n_G - 1)/(n_G + 1))^2               % 0.75
% Reflected energy (1 - alpha): L_refl = L_inc + 10 log10(1 - alpha)
L_refl = 70 + 10*log10(1 - [0.5 0.9 0.99])          % 67 / 60 / 50 dB (slide 5)
