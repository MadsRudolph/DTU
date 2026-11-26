%% T05 - Intensity, sound power, standing-wave ratio and absorbed power
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: intensity from complex p and u (with a phase), plane-wave
% intensity and power from an SPL, intensity/power levels, absorption
% from a measured standing-wave ratio (Lmax/Lmin in a tube), incident,
% reflected and absorbed power.
%
% Matches: Week 4 P2 (pre-filled: 1.54 mW), Week 4 P4.1-4.2 (pre-filled:
% alpha = 0.69, absorbed 0.87 uW, L_W = 59.4 dB), Week 4 MC3, Lecture 7
% slide 38 (SWR 3 -> 0.75), any "I = 1/2 Re{p u*}" step in the old
% exams (2022 P3.4, 2023 P3.2, 2024 P2.2: see T07 for the two-source line).

%% Constants
rho = 1.2;  c = 343;
rho_c = rho*c              % [Pa s/m]
p_ref = 20e-6;  I_ref = 1e-12;  W_ref = 1e-12;

%% A - Intensity from complex amplitudes (works in ANY field)
% $$I = \tfrac12\Re\{P\,U^*\} = p_{rms}u_{rms}\cos\phi$$
P_A = 0.02 + 0.0275j;                  % GIVEN complex pressure amplitude [Pa]
U_A = (107.4 - 44.6j)*1e-6;            % GIVEN complex particle-velocity amplitude [m/s]
I_A = 0.5*real(P_A*conj(U_A))          % 459 nW/m^2 (2024 P2.2 at r1 = 0.1 m)
phase_deg = angle(P_A/U_A)*180/pi      % p leads u by this angle
Q_reactive = 0.5*imag(P_A*conj(U_A))   % reactive part: stored, not transported

%% B - Plane travelling wave: SPL -> intensity -> power (Week 4 P2)
% $$p_{rms} = p_{ref}10^{L_p/20},\quad I = \frac{p_{rms}^2}{\rho c},\quad W = I S$$
Lp_B = 82;  S_B = 10;                  % GIVEN [dB], area perpendicular to the wave [m^2]
p_rms_B = p_ref*10^(Lp_B/20)
I_B = p_rms_B^2/rho_c
W_B = I_B*S_B                          % 1.54 mW (official)
LI_B = 10*log10(I_B/I_ref)             % L_I = L_p - 0.14 dB for a plane wave
LW_B = 10*log10(W_B/W_ref)
% Spherical (free field): W = 4 pi r^2 I.  Hemisphere / baffle: W = 2 pi r^2 I.
% Tube: W = I S_tube. Diffuse field onto a wall: I_inc = p^2/(4 rho c) (T10).

%% C - Standing-wave tube: absorption from Lmax and Lmin (Week 4 P4)
% $$s = 10^{(L_{max}-L_{min})/20},\quad |R| = \frac{s-1}{s+1},\quad \alpha = 1-|R|^2 = \frac{4s}{(s+1)^2}$$
Lmax = 85;  Lmin = 74;  S_tube = 0.01; % GIVEN [dB], [dB], tube area [m^2]
s = 10^((Lmax - Lmin)/20)
R_mag = (s - 1)/(s + 1)
alpha = 1 - R_mag^2                    % 0.69 (official)
% If the SWR is given as a ratio n already, use s = n directly (n = 3 -> 0.75).

%% D - Incident, reflected and absorbed power (rms values throughout)
% $$p_i = \frac{p_{max}+p_{min}}{2},\quad p_r = \frac{p_{max}-p_{min}}{2},\quad W_{abs} = \frac{S\,(p_i^2-p_r^2)}{\rho c} = \frac{S\,p_{max}p_{min}}{\rho c}$$
p_max = p_ref*10^(Lmax/20)
p_min = p_ref*10^(Lmin/20)
p_inc = (p_max + p_min)/2
p_refl = (p_max - p_min)/2
W_inc = S_tube*p_inc^2/rho_c
W_abs = S_tube*p_max*p_min/rho_c       % 0.87 uW (official, with rho c = 413)
LW_abs = 10*log10(W_abs/W_ref)         % 59.4 dB (official)
% Check: W_abs = alpha * W_inc
W_abs_check = alpha*W_inc

%% E - Energy densities (peak phasors)
% $$\bar w_p = \frac{|P|^2}{4\rho c^2},\qquad \bar w_k = \frac{\rho |U|^2}{4}$$
w_p = abs(P_A)^2/(4*rho*c^2)
w_k = rho*abs(U_A)^2/4

%% F - Power through an acoustic port, or into a resistance
% $$W = \tfrac12\Re\{P Q^*\} = \tfrac12|Q|^2\Re\{Z_a\}$$
Q_F = 1e-4;  Za_F = 4e5 + 2e5j;       % GIVEN volume velocity [m^3/s], impedance [Pa s/m^3]
W_F = 0.5*abs(Q_F)^2*real(Za_F)
