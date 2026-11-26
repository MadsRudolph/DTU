%% T06 - One monopole: pressure, particle velocity, near field, intensity, power
% 34840 exam toolkit. Fill in the GIVEN block, run, read the printed lines.
%
% Solves: a monopole (small source, ka << 1) with volume velocity Q in free
% space (4 pi) or on a rigid plane / in a baffle (2 pi). Pressure and
% particle velocity amplitudes at given radii, the p-u phase (near field),
% intensity, radiated power, levels, and SPL <-> L_W conversions.
%
% Matches: exam 2024 part 1 P2.1 (pre-filled: |p| = 30/15/10 mPa,
% |u| = 108/41.5/25.9 um/s at 0.1/0.2/0.3 m), 2024 MC1 (phase at 189 Hz,
% 0.5 m = 30 deg, pre-filled), 2023 MC2 (near field: u decays faster than
% 1/r), Week 2 P4, Week 5 P1-P2, Week 8 P1 (pre-filled block E: 73.47 dB,
% 73.34 dB, 81.84 dB).

%% Constants
rho = 1.2;  c = 343;
rho_c = rho*c
p_ref = 20e-6;  I_ref = 1e-12;  W_ref = 1e-12;

%% GIVEN - edit these
Q = 1e-5;                  % volume velocity AMPLITUDE [m^3/s]
f = 500;                   % [Hz]
r = [0.1 0.2 0.3];         % field radii [m]
Omega = 4*pi;              % 4*pi free field, 2*pi on a rigid plane / in a baffle

%% Step 1 - k and kr (is it near field?)
% $$\omega = 2\pi f,\qquad k = \omega/c$$
w = 2*pi*f
k = w/c
kr = k*r                   % kr < 1: near field matters for u

%% Step 2 - Pressure
% $$P(r) = \frac{j\omega\rho Q}{\Omega\, r}e^{-jkr}\qquad(\Omega = 4\pi \text{ or } 2\pi)$$
P = 1j*w*rho*Q./(Omega*r).*exp(-1j*k*r)
p_amp = abs(P)             % 30, 15, 10 mPa (official 2024 P2.1)
p_rms = p_amp/sqrt(2)
Lp = 20*log10(p_rms/p_ref)

%% Step 3 - Particle velocity (radial) with the near-field term
% $$U_r = \frac{P}{\rho c}\left(1+\frac{1}{jkr}\right)$$
U = P/rho_c.*(1 + 1./(1j*kr))
u_amp = abs(U)             % 108, 41.5, 25.9 um/s (official 2024 P2.1)
% Sanity: p falls as 1/r, u falls FASTER near the source (1/r^2 term).

%% Step 4 - Phase between p and u, specific impedance
% $$\arg\frac{P}{U_r} = \arctan\frac{1}{kr}\qquad Z_s = \frac{\rho c}{1+1/(jkr)}$$
phase_deg = atan(1./kr)*180/pi
Zs = rho_c./(1 + 1./(1j*kr))
% 2024 MC1: f = 189 Hz, r = 0.5 m:
phase_MC = atan(1/(2*pi*189/c*0.5))*180/pi     % 30 deg (official)

%% Step 5 - Intensity (near-field term carries no active power)
% $$I = \tfrac12\Re\{P U^*\} = \frac{|P|^2}{2\rho c} = \frac{p_{rms}^2}{\rho c}\quad\text{(any r)}$$
I = 0.5*real(P.*conj(U))
I_check = p_amp.^2/(2*rho_c)

%% Step 6 - Radiated power
% Free field: $$W = \frac{\rho c k^2 |Q|^2}{8\pi}$$   (peak Q; rms Q -> divide by 4 pi)
W_free = rho_c*k^2*abs(Q)^2/(8*pi)
% Any solid angle: W = Omega r^2 I  (same at every r)
W_from_I = Omega*r(1)^2*I(1)
LW = 10*log10(W_from_I/W_ref)
% On a rigid plane (2 pi, kh -> 0): same Q gives 2x the power (+3 dB) and
% 2x the pressure (+6 dB). Two equal in-phase monopoles close together:
% 4x power (+6 dB). Dipole: see T07.

%% Step 7 - SPL <-> sound power in free field
% $$L_p = L_W - 10\log_{10}(\Omega r^2) + 10\log_{10}\frac{\rho c\,W_{ref}}{p_{ref}^2 \cdot 1\,\mathrm{m^2}}$$
% (the last term is -0.14 dB with rho c = 411.6; often dropped)
Lp_from_LW = LW - 10*log10(Omega*r.^2) + 10*log10(rho_c*W_ref/p_ref^2)
% Distance law: L(r2) = L(r1) + 20 log10(r1/r2): -6 dB per doubling.

%% E - Pre-filled check: Week 8 P1 (amplitude 0.1 Pa at 1 m, free field)
p1_rms = 0.1/sqrt(2);                   % GIVEN 0.1 Pa amplitude at 1 m
Lp_075 = 20*log10(p1_rms/0.75/p_ref)    % 73.47 dB at 0.75 m (sheet 73.46)
LI_075 = 10*log10((p1_rms/0.75)^2/rho_c/I_ref)   % 73.34 dB (sheet)
LW_E = 10*log10(4*pi*1^2*p1_rms^2/rho_c/W_ref)   % 81.84 dB (sheet 81.83)

%% F - Pulsating sphere of radius a with surface velocity U_a
% $$Q = 4\pi a^2 U_a,\qquad Z_{a,r} = \frac{\rho c}{4\pi a^2}\frac{jka}{1+jka}$$
a_s = 0.05;  U_a = 0.01;                % GIVEN radius [m], surface velocity amplitude [m/s]
Q_s = 4*pi*a_s^2*U_a
Zar = rho_c/(4*pi*a_s^2)*(1j*k*a_s)/(1 + 1j*k*a_s)
W_sphere = 0.5*abs(Q_s)^2*real(Zar)
