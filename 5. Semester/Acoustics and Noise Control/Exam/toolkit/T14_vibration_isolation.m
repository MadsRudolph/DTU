%% T14 - Vibration isolation: mass on springs, transmissibility, static deflection, mobility
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: natural frequency from s and m (springs in parallel/series) or
% from the static deflection, forced response (x, v, a, force on the floor),
% transmissibility T and isolation in dB, stiffness needed for a target
% T, base excitation, damping effect, force of a source bolted to a rigid
% or mobile receiver.
%
% Matches: 2022 MC11 (block A, pre-filled: 100 kg on 1 cm at 7 Hz ->
% 0.25 dB, official 0.35 dB with f0 = 5.0 Hz, ~ 0 dB), 2024 MC (block A: isolation from 7.04 Hz), 2023 MC
% (block B: 80 kg, 1.5 cm -> 4.1 Hz), 2023 MC (block E: free velocity
% 0.01 m/s, 0.1 kg, 500 Hz -> F = j3.14 N), Week 11 P3 (block C: 20.05 Hz,
% 0.231 mm, 5.49 N / 0.625 N), Week 11 P4 (block D: s = 3365 N/m).

%% Constants
g = 9.81;                  % [m/s^2]

%% A - From static deflection to f0 and transmissibility (2022 MC11, 2024 MC)
m = 100;                   % GIVEN total mass on the mounts [kg]
xi0 = 0.01;                % GIVEN static deflection under that mass [m]
f = 7;                     % GIVEN excitation frequency [Hz]
zeta = 0;                  % GIVEN damping ratio (0 = undamped)
% $$s = \frac{mg}{\xi_0},\qquad f_0 = \frac{1}{2\pi}\sqrt{\frac{s}{m}} = \frac{1}{2\pi}\sqrt{\frac{g}{\xi_0}}\approx\frac{0.5}{\sqrt{\xi_0}}$$
s = m*g/xi0                % total stiffness of all springs [N/m]
f0 = sqrt(s/m)/(2*pi)      % 4.98 Hz
f0_rule = 0.5/sqrt(xi0)
f_isolation_starts = sqrt(2)*f0          % 7.04 Hz (2024 MC answer)
% $$T = \sqrt{\frac{1+(2\zeta\Omega)^2}{(1-\Omega^2)^2+(2\zeta\Omega)^2}},\qquad \Omega = f/f_0$$
Omega = f/f0
T = sqrt((1 + (2*zeta*Omega)^2)/((1 - Omega^2)^2 + (2*zeta*Omega)^2))
T_dB = 20*log10(T)         % +0.25 dB ~ 0 dB (official: 0.35 dB with f0 rounded to 5 Hz; answer A)
isolation_dB = -T_dB       % = 10 log10(E_iso)
% Omega < sqrt2: T > 1 (no isolation). Omega = sqrt2: T = 1 for ANY damping.
% Omega >> 1 undamped: T = 1/(Omega^2 - 1), -12 dB/octave. Damping makes
% the isolation WORSE above sqrt2 (it only helps at resonance).

%% B - f0 from mass and deflection (2023 MC: 80 kg, 1.5 cm)
f0_B = sqrt(g/0.015)/(2*pi)              % 4.07 Hz -> 4.1 Hz (answer)

%% C - Forced, undamped mass-spring (Week 11 P3: s = 23.8 kN/m, m = 1.5 kg, F = 5 N)
s_C = 23.8e3;  m_C = 1.5;  F_C = 5;  w_C = [37.8 378];   % GIVEN [N/m], [kg], [N], [rad/s]
w0_C = sqrt(s_C/m_C)
f0_C = w0_C/(2*pi)                       % 20.05 Hz (official 20.1)
% $$|\xi| = \frac{F}{s\,|1-(\omega/\omega_0)^2|},\quad |v| = \omega|\xi|,\quad |a| = \omega^2|\xi|,\quad |F_f| = s|\xi|$$
xi_C = F_C./(s_C*abs(1 - (w_C/w0_C).^2)) % 0.231 mm, 0.0262 mm (official)
v_C = w_C.*xi_C
a_C = w_C.^2.*xi_C
Ff_C = s_C*xi_C                          % 5.49 N, 0.625 N (official)
% With damping r: x = F/(s - w^2 m + j w r), zeta = r/(2 sqrt(m s)).
% Below f0 stiffness controlled (x = F/s), at f0 damping controlled,
% above f0 mass controlled (x = F/(w^2 m)).

%% D - Stiffness for a target motion ratio (base excitation, Week 11 P4)
% $$\frac{u}{u_f} = \frac{1}{1-(\omega/\omega_0)^2}\ \Rightarrow\ s = \frac{-(u/u_f)\,\omega^2 m}{1-u/u_f}$$
% Above resonance the ratio is NEGATIVE (antiphase): use -0.1, not +0.1.
w_D = 2*pi*25;  m_D = 1.5;  ratio_D = -0.1;   % GIVEN
s_D = -ratio_D*w_D^2*m_D/(1 - ratio_D)        % 3365 N/m (official 3.37e3)
f0_D = sqrt(s_D/m_D)/(2*pi)                   % 7.54 Hz (official)

%% Springs combine like this
s1 = 500;  s2 = 500;
s_parallel = s1 + s2                     % side by side / mass between two springs
s_series = 1/(1/s1 + 1/s2)               % stacked

%% E - Source bolted to a receiver: force from free velocity and mobilities
% $$F = \frac{v_{free}}{Y_S + Y_R},\qquad Y_{mass} = \frac{1}{j\omega m},\quad Y_{spring} = \frac{j\omega}{s},\quad Y_{rigid} = 0$$
v_free = 0.01;  m_src = 0.1;  f_E = 500;      % GIVEN (2023 MC)
Y_S = 1/(1j*2*pi*f_E*m_src)
Y_R = 0;                                       % rigid surface
F_E = v_free/(Y_S + Y_R)                       % 0 + 3.14j N (answer "F = i 3.14 N")
% With an isolator (mobility j w/s) in series:
% $$E_{iso} = \left|1+\frac{j\omega/s}{Y_S+Y_R}\right|^2$$  (need Y_isolator >> Y_S + Y_R)
% Infinite plate input mobility: Y = 1/(8 sqrt(B' m'')), B' = E h^3/(12(1-nu^2)).
