%% T01 - Plane wave hitting a surface (absorber, wall, other medium)
% 34840 exam toolkit. Fill in the GIVEN block, run, read the printed lines.
%
% Solves: a plane wave at normal incidence on a surface with a known
% absorption coefficient alpha, reflection coefficient R or surface
% impedance Z. Gives the total pressure, particle velocity and net
% intensity at a distance d in front of the surface, the standing-wave
% max/min, and the transmission into a second medium (air/water).
%
% Matches: exam 2024 part 1 P1.1 (pre-filled), exam 2023 part 1 P1 (see T02
% for the driven-tube version), Week 2 P3, Week 4 P3, 2022 MC1 (bubbles),
% 2024 MC Venus absorber.
%
% Pre-filled with exam 2024 P1.1. Official answers: |p| = 0.89 Pa at
% 400 Hz and 0.86 Pa at 630 Hz, 0.6 m in front of the absorber.
%
% Conventions: peak complex amplitudes, e^{j w t}. Surface at x = 0, the
% wave comes from x < 0, so a point d in front of the surface is x = -d.

%% Constants (exam sheet: c = 343, rho = 1.2)
rho = 1.2;                 % air density [kg/m^3]
c = 343;                   % speed of sound [m/s]
rho_c = rho*c              % characteristic impedance of air [Pa s/m]
p_ref = 20e-6;             % reference pressure [Pa]

%% GIVEN - edit these (vectors = one entry per frequency)
f = [400 630];             % frequencies [Hz]
p_i = [0.9 0.4+0.4j];      % incident complex pressure AMPLITUDES [Pa]
alpha = [0.9999 0.19];     % absorption coefficients (set [] if you know Z instead)
R_sign = +1;               % sheet says "positive reflection coefficient" -> +1
d = 0.6;                   % distance in front of the surface [m]

%% Step 1 - Reflection coefficient
% From alpha (real R with a known sign):
% $$\alpha = 1-|R|^2 \;\Rightarrow\; R = \pm\sqrt{1-\alpha}$$
R = R_sign*sqrt(1 - alpha)
%
% If you know the surface impedance Z instead, use this line:
% $$R = \frac{Z-\rho c}{Z+\rho c}$$
% Z = 500 + 1000j;  R = (Z - rho_c)./(Z + rho_c)
% Hard wall: R = +1 (pressure max at the wall). Soft (pressure release,
% e.g. air bubbles in water, open tube end): R = -1. Z = rho c: R = 0.

%% Step 2 - Wavenumber and position
% $$k = \frac{2\pi f}{c},\qquad x = -d$$
k = 2*pi*f/c
x = -d;

%% Step 3 - Total pressure in front of the surface
% $$p(x) = p_i e^{-jkx} + R\,p_i e^{+jkx}$$
p = p_i.*exp(-1j*k*x) + R.*p_i.*exp(1j*k*x)
p_amp = abs(p)                       % 0.89 and 0.86 Pa (official 2024 P1.1)
p_rms = p_amp/sqrt(2)
Lp = 20*log10(p_rms/p_ref)

%% Step 4 - Particle velocity (note the minus sign on the reflected wave)
% $$u(x) = \frac{p_i e^{-jkx} - R\,p_i e^{+jkx}}{\rho c}$$
u = (p_i.*exp(-1j*k*x) - R.*p_i.*exp(1j*k*x))/rho_c
u_amp = abs(u)

%% Step 5 - Net (active) intensity towards the surface
% $$I = \tfrac12\Re\{p\,u^*\} = \frac{|p_i|^2(1-|R|^2)}{2\rho c}$$
I = 0.5*real(p.*conj(u))
I_check = abs(p_i).^2.*(1 - abs(R).^2)/(2*rho_c)   % must equal I
% Sanity: I is the same at every x (lossless air) and >= 0.

%% Step 6 - Standing-wave pattern
% $$|p|_{max} = |p_i|(1+|R|),\quad |p|_{min} = |p_i|(1-|R|),\quad s = \frac{1+|R|}{1-|R|}$$
p_max = abs(p_i).*(1 + abs(R))
p_min = abs(p_i).*(1 - abs(R))
SWR = p_max./p_min
% R > 0: pressure max AT the surface, minima at d = lambda/4, 3lambda/4 ...
% R < 0: pressure min at the surface, maxima at lambda/4 ...
lambda = c./f
d_first_min = lambda/4               % first pressure minimum in front (R > 0)

%% Step 7 - Transmission into a second medium (normal incidence)
% Example: air -> water (Week 4 P3, sheet ~30 dB). Swap z1/z2 for water -> air.
z1 = rho_c;                          % medium the wave comes from [Pa s/m]
z2 = 1000*1480;                      % medium it goes into (water) [Pa s/m]
%
% $$R_{12} = \frac{z_2-z_1}{z_2+z_1},\qquad T_p = \frac{p_t}{p_i} = 1+R_{12} = \frac{2z_2}{z_1+z_2}$$
R12 = (z2 - z1)/(z2 + z1)
Tp = 2*z2/(z1 + z2)                  % ~2 into water: pressure DOUBLES ...
%
% $$\tau = \frac{4 z_1 z_2}{(z_1+z_2)^2} = 1-R_{12}^2$$
tau = 4*z1*z2/(z1 + z2)^2            % ... but the power hardly gets in
atten_dB = -10*log10(tau)            % 29.5 dB (Week 4 P3: "about 30 dB"), same both ways
% Pressure "attenuation factor" asked on Week 2: p_i/p_t = 1/Tp.
pi_over_pt_dB = 20*log10(1/Tp)

%% Matching impedance for an ideal absorber (2024 MC Venus)
% Ideal absorber at normal incidence: Z_surface = rho c of the medium.
% Venus: rho = 0.1 g/cm^3 = 100 kg/m^3, c = 500 m/s -> 50 000 kg/(s m^2).
Z_ideal_venus = 100*500
