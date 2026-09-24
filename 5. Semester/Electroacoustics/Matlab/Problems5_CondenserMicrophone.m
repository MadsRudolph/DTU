%% Problems 5 - Condenser microphone, worked
% 34870 Electroacoustics | 24 September 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% sheet's answer (or the official solution's) is written in the text so you
% can compare.
%
% All values are in SI units (kg, m, s, ohm). Grams, cm^3 and µm from the
% sheet are converted when they are typed in.
%
% Air (from the sheet) and the permittivity of air (from the official
% solution):
rho = 1.18         % air density [kg/m^3]
c = 344            % speed of sound [m/s]
eps0 = 8.85e-12    % permittivity [F/m]

%% The given microphone
% Mechanical system (the diaphragm):
C_MD = 4e-6        % diaphragm compliance [m/N]
M_MD = 0.050e-3    % diaphragm mass, 0.050 g [kg]
R_MD = 1           % diaphragm damping [Ns/m]
r = 9e-3           % effective diaphragm radius, 9 mm [m]
%%
% Acoustic system behind the diaphragm (the backplate holes and the back
% volume):
M_AS = 100         % acoustic mass of the backplate holes [kg/m^4]
R_AS = 1e7         % acoustic resistance of the backplate holes [Ns/m^5]
V_AB2 = 1e-6       % back volume, 1 cm^3 [m^3]
%%
% Electrical system:
E = 200            % polarisation voltage [V]
x_0 = 20e-6        % gap between diaphragm and backplate, 20 µm [m]
R_L = 500e6        % load resistance, 500 Mohm [ohm]

%% The model in one picture
% Sound pressure pushes on the diaphragm (area S_D). The diaphragm is a
% mass-spring-damper. Two pieces of air add to it:
%
% * In front, the air that moves with the diaphragm (the radiation mass
% M_A1).
% * Behind, the air is pushed through the holes in the backplate (M_AS,
% R_AS) into the back volume, which acts as a spring (C_AB2).
%
% Everything acoustic is moved to the mechanical side by multiplying by
% S_D^2, and then the whole microphone is one mass, one spring and one
% damper:
%
% $$M_{MT} = M_{MD} + S_D^2\,(M_{A1} + M_{AS}), \qquad \frac{1}{C_{MT}} = \frac{1}{C_{MD}} + \frac{S_D^2}{C_{AB2}}, \qquad R_{MT} = R_{MD} + S_D^2 R_{AS}$$
%
% The two springs (diaphragm and back volume) push on the diaphragm at the
% same time, so their stiffnesses 1/C add. The small air layer between the
% diaphragm and the backplate (C_AB1) is left out, because the sheet says
% it is more than 200 times smaller than the back volume.

%% Problem 1 - The totals
% *Diaphragm area.* $S_D = \pi r^2$
S_D = pi*r^2
%%
% *Radiation mass in front.* The official solution treats the microphone as
% a piston at the end of a tube (unflanged), which gives
%
% $$M_{A1} = \frac{0.6133\,\rho}{\pi r}$$
%
% Official solution: 25.595 kg/m^4
M_A1 = 0.6133*rho/(pi*r)
%%
% *Back volume as a spring.* A closed volume V is an acoustic compliance
%
% $$C_{AB2} = \frac{V_{AB2}}{\rho c^2}$$
%
% Official solution: 7.1615 pF (in m^5/N)
C_AB2 = V_AB2/(rho*c^2)
%%
% The air layer between diaphragm and backplate, 200 times smaller (only
% used in the circuit of Problem 2):
C_AB1 = C_AB2/200
%%
% *Total mass.* $M_{MT} = M_{MD} + S_D^2(M_{A1}+M_{AS})$
%
% Official solution: 5.8133e-5 kg
M_MT = M_MD + S_D^2*(M_A1 + M_AS)
%%
% *Total compliance.* $C_{MT} = \left(\frac{1}{C_{MD}} + \frac{S_D^2}{C_{AB2}}\right)^{-1}$
%
% Official solution: 3.8604e-6 m/N
C_MT = 1/(1/C_MD + S_D^2/C_AB2)
%%
% *Total damping.* $R_{MT} = R_{MD} + S_D^2 R_{AS}$
%
% Official solution: 1.6475 Ns/m
R_MT = R_MD + S_D^2*R_AS

%% Problem 1a - Resonance frequency
% Mass and total spring resonate at
%
% $$f_0 = \frac{1}{2\pi\sqrt{M_{MT}\,C_{MT}}}$$
%
% Sheet: 10.6 kHz (official solution: 10624 Hz)
f_0 = 1/(2*pi*sqrt(M_MT*C_MT))
f_0_kHz = f_0/1000

%% Problem 1b - Quality factor
% How sharp the resonance is: mass reactance at f_0 divided by the damping,
%
% $$Q = \frac{2\pi f_0\,M_{MT}}{R_{MT}}$$
%
% Sheet: 2.3 (official solution: 2.3554)
Q = 2*pi*f_0*M_MT/R_MT

%% Problem 1c - Pressure sensitivity below resonance
% Below f_0 the diaphragm is stiffness controlled: a pressure p gives a
% force S_D p, which squeezes the total spring by x = C_MT S_D p. The
% polarised capacitor turns a displacement x into a voltage E x / x_0. So
%
% $$M = \frac{e}{p} = \frac{E\,S_D\,C_{MT}}{x_0}$$
%
% Sheet: 9.8 mV/Pa
M = E*S_D*C_MT/x_0
M_mV_per_Pa = M*1000
%%
% Note that M_MD and R_MD do not appear: below resonance only the springs
% matter. That is the whole point of Problems 6.

%% Problem 2a - The equivalent circuit
% The LTspice circuit is in
% LTspice/Problems 5-6 - Condenser Microphone/P5_2b_Pressure.asc (built
% like the official solution). Element by element:
%
% * *Electrical:* a current source (E C_E0/x_0) u feeds C_E0 in parallel
% with R_L. That is the Norton form of "a voltage E x/x_0 in series with the
% capacitor C_E0". V(out) is the microphone's output voltage.
% * *Mechanical (impedance analogy, a loop):* C_MD, M_MD and R_MD in series
% with a force source S_D (p_B - p_F). The loop current is the diaphragm
% velocity u. Across C_MD sits a current source (E C_MD/x_0) i: the
% electrostatic force from the charge on the capacitor, again in Norton form.
% * *Acoustical (impedance analogy):* the diaphragm moves the volume
% velocity U = S_D u from the front node to the back node. At the back:
% C_AB1 to ground, then M_AS and R_AS in series to C_AB2. At the front: the
% radiation impedance of a piston at the end of a tube, up to the 1 Pa sound
% source p_i.
%
% *The two coupling gains* of the official solution:
%
% $$C_{E0} = \frac{\varepsilon_0 S_D}{x_0}, \qquad \text{Elec\_Gain} = \frac{E\,C_{E0}}{x_0}, \qquad \text{Mech\_Gain} = \frac{E\,C_{MD}}{x_0}$$
%
% Official solution: C_E0 = 112.6 pF, Elec_Gain = 0.0011, Mech_Gain = 40
C_E0 = eps0*S_D/x_0
C_E0_pF = C_E0*1e12
Elec_Gain = E*C_E0/x_0
Mech_Gain = E*C_MD/x_0
%%
% *The front radiation impedance* (unflanged tube). The official solution's
% values:
%
% $$M_{A1} = \frac{0.6133\rho}{\pi r}, \quad R_{A1} = \frac{0.5045\rho c}{\pi r^2}, \quad R_{A2} = \frac{\rho c}{\pi r^2}, \quad C_{A1} = \frac{0.55\pi^2 r^3}{\rho c^2}$$
%
% Official solution: R_A1 = 8.0476e5, R_A2 = 1.5952e6, C_A1 = 2.8339e-11
R_A1 = 0.5045*rho*c/(pi*r^2)
R_A2 = rho*c/(pi*r^2)
C_A1 = 0.55*pi^2*r^3/(rho*c^2)
%%
% They are connected as $M_{A1}$ in parallel with $[R_{A2} + (R_{A1}\parallel C_{A1})]$.
% At low frequency the mass shorts the rest, so it is just the M_A1 of
% Problem 1. At high frequency it becomes R_A2 = rho c / S_D, the
% impedance of a plane wave.

%% Problem 2b - Test the circuit with the values from Problem 1
% Here is the same circuit solved directly in MATLAB (LTspice gives the same
% numbers to 9 digits: run p5.py --verify). First the frequency axis,
% 1 Hz to 100 kHz, and $j\omega$:
f = logspace(0, 5, 3000);
jw = 1j*2*pi*f;
%%
% *Front radiation impedance* (a parallel connection is 1/(1/Z1 + 1/Z2)):
%
% $$Z_{ar} = j\omega M_{A1} \;\parallel\; \left[R_{A2} + \left(R_{A1} \parallel \frac{1}{j\omega C_{A1}}\right)\right]$$
Z_ar = 1 ./ ( 1./(jw*M_A1) + 1./(R_A2 + 1./(1/R_A1 + jw*C_A1)) );
%%
% *Back impedance:* C_AB1 in parallel with the holes and the back volume,
%
% $$Z_B = \frac{1}{j\omega C_{AB1}} \;\parallel\; \left[R_{AS} + j\omega M_{AS} + \frac{1}{j\omega C_{AB2}}\right]$$
Z_B = 1 ./ ( jw*C_AB1 + 1./(R_AS + jw*M_AS + 1./(jw*C_AB2)) );
%%
% *Diaphragm:* $Z_{MD} = j\omega M_{MD} + R_{MD} + \frac{1}{j\omega C_{MD}}$
Z_MD = jw*M_MD + R_MD + 1./(jw*C_MD);
%%
% *Electrical load:* the admittance of C_E0 in parallel with R_L,
% $Y_E = j\omega C_{E0} + 1/R_L$
Y_E = jw*C_E0 + 1/R_L;
%%
% *Solve for the velocity.* The force S_D p_i drives the diaphragm, which
% sees its own impedance plus both air loads (times S_D^2). The last term
% is the electrostatic force from the current in R_L; with R_L = 500 Mohm
% it is tiny, a little extra damping.
%
% $$u = \frac{S_D\,p_i}{Z_{MD} + S_D^2 (Z_{ar} + Z_B) - \dfrac{\text{Mech\_Gain}\cdot\text{Elec\_Gain}}{R_L\,Y_E\,j\omega C_{MD}}}$$
%
% *Output voltage:* the current source Elec_Gain*u into Y_E,
%
% $$e = \frac{\text{Elec\_Gain}\cdot u}{Y_E}$$
%
% With p_i = 1 Pa, e is the sensitivity in V/Pa.
p_i = 1;
u = S_D*p_i ./ (Z_MD + S_D^2*(Z_ar + Z_B) - Mech_Gain*Elec_Gain./(R_L*Y_E.*jw*C_MD));
e_pressure = Elec_Gain*u./Y_E;
%%
% Sensitivity at 250 Hz, in mV/Pa. Problem 1c: 9.8 mV/Pa
k250 = find(f >= 250, 1);
M_250_mV = abs(e_pressure(k250))*1000
%%
% The peak, and where it is (it sits a little below f_0 because Q > 0.7):
[M_peak, k] = max(abs(e_pressure));
M_peak_mV = M_peak*1000
f_peak = f(k)
%%
figure;
semilogx(f, 20*log10(abs(e_pressure)), 'LineWidth', 1.5);
grid on; xlim([1 1e5]); ylim([-75 -25]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
title('Pressure response, values of Problem 1 (T(s) = 1)');
%%
% Flat at -40.2 dB (9.8 mV/Pa) from a few Hz, a +7 dB peak near 10 kHz
% (Q = 2.36), then it falls 12 dB per octave above resonance. The small
% drop at the very bottom is C_E0 with R_L, a high-pass at
%
% $$f_{low} = \frac{1}{2\pi R_L C_{E0}}$$
f_low = 1/(2*pi*R_L*C_E0)

%% Problem 2c - Make the pressure response as flat as possible
% Two knobs:
%
% * *Top end:* the peak comes from Q = 2.36. The flattest second-order
% response has Q = 1/sqrt(2) = 0.707 (no peak, the widest flat band). Q only
% depends on the damping, and the easy damping to change is R_AS (the holes
% in the backplate). Solve $Q = \sqrt{M_{MT}/C_{MT}}/R_{MT}$ for R_MT, and
% $R_{MT} = R_{MD} + S_D^2 R_{AS}$ for R_AS:
%
% $$R_{AS} = \frac{\sqrt{M_{MT}/C_{MT}}\,/\,0.707 - R_{MD}}{S_D^2}$$
R_AS_flat = (sqrt(M_MT/C_MT)/(1/sqrt(2)) - R_MD)/S_D^2
R_AS_flat_Mohm = R_AS_flat/1e6
%%
% * *Bottom end:* raise R_L to 1 Gohm (the official solution's choice),
% which halves f_low:
R_L_opt = 1e9
f_low_opt = 1/(2*pi*R_L_opt*C_E0)
%%
% The same response with these two values (only Z_B and Y_E change):
Z_B_flat = 1 ./ ( jw*C_AB1 + 1./(R_AS_flat + jw*M_AS + 1./(jw*C_AB2)) );
Y_E_opt = jw*C_E0 + 1/R_L_opt;
u_flat = S_D*p_i ./ (Z_MD + S_D^2*(Z_ar + Z_B_flat) - Mech_Gain*Elec_Gain./(R_L_opt*Y_E_opt.*jw*C_MD));
e_flat = Elec_Gain*u_flat./Y_E_opt;
figure;
semilogx(f, 20*log10(abs(e_pressure)), f, 20*log10(abs(e_flat)), 'LineWidth', 1.5);
grid on; xlim([1 1e5]); ylim([-75 -25]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
legend('Problem 1 values (R_{AS} = 10 M, R_L = 500 M)', 'R_{AS} = 69 M, R_L = 1 G (Q = 0.707)', 'Location', 'southwest');
title('2c: flattest pressure response');
%%
% The flat band now reaches to about 10 kHz (-3 dB at f_0) without a peak.
% The price: nothing, for a pressure microphone. But see 2d.

%% Problem 2d - Include T(s): the microphone in a free field
% In a free field the microphone is in the way of the sound wave. Its stiff
% diaphragm reflects the wave, so the pressure on the diaphragm is more than
% the incident pressure p_i. For a diaphragm that reflects everything
% (Lecture 6, Leach eq. 5.1):
%
% $$p_D = T(s)\,p_i, \qquad T(s) = 1 + \frac{Z_{ar}}{R_{A2}}, \qquad R_{A2} = \frac{\rho c}{S_D}$$
%
% * Low frequency: Z_ar is a tiny mass, T = 1 (no effect).
% * High frequency: Z_ar -> R_A2, T = 2: pressure doubling, +6 dB.
%
% *In the circuit* this is the generator Gpb: a current source
% p_i / R_A2 pushed into the front node. That current flows through Z_ar and
% adds $p_i Z_{ar}/R_{A2}$ to the pressure. The gain is 1/R_A2.
%
% Official solution: 1/R_A2 = 6.2689e-7
Gpb_gain = 1/R_A2
%%
T = 1 + Z_ar/R_A2;
%%
% |T| at 1 kHz, at ka = 1 (6.1 kHz) and at 20 kHz:
f_ka1 = c/(2*pi*r)
T_1k_6k_20k = abs(T([find(f >= 1000, 1), find(f >= f_ka1, 1), find(f >= 20000, 1)]))
%%
% The diaphragm is blocked in T(s), but in the circuit it moves, so the
% free-field response is the same u formula with $T\,p_i$ as the drive:
u_ff = S_D*T*p_i ./ (Z_MD + S_D^2*(Z_ar + Z_B) - Mech_Gain*Elec_Gain./(R_L*Y_E.*jw*C_MD));
e_freefield = Elec_Gain*u_ff./Y_E;
figure;
semilogx(f, 20*log10(abs(e_pressure)), f, 20*log10(abs(e_freefield)), 'LineWidth', 1.5);
hold on; semilogx(f, 20*log10(abs(T)) - 40, 'k--'); hold off;
grid on; xlim([1 1e5]); ylim([-75 -25]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
legend('pressure response (T = 1)', 'free-field response (with T)', '|T(s)|, shifted to -40 dB', 'Location', 'southwest');
title('2d: the effect of T(s), Problem 1 values');
%%
% The peak grows from 22.5 to about 39 mV/Pa. LTspice file:
% P5_2d_FreeField.asc (Tsw = 1 switches Gpb on).
M_peak_ff_mV = max(abs(e_freefield))*1000

%% Problem 2e - Optimise the free-field response
% A free-field microphone must be flat *including* T(s). T already lifts the
% top by up to 6 dB, so the capsule itself should droop there: more
% damping than Q = 0.707. The official solution chooses R_AS = 80 Mohm
% and R_L = 1 Gohm:
R_AS_opt = 80e6
%%
% Its Q (as a pressure microphone) is well below 0.707:
Q_opt = sqrt(M_MT/C_MT)/(R_MD + S_D^2*R_AS_opt)
%%
Z_B_opt = 1 ./ ( jw*C_AB1 + 1./(R_AS_opt + jw*M_AS + 1./(jw*C_AB2)) );
u_opt = S_D*T*p_i ./ (Z_MD + S_D^2*(Z_ar + Z_B_opt) - Mech_Gain*Elec_Gain./(R_L_opt*Y_E_opt.*jw*C_MD));
e_opt = Elec_Gain*u_opt./Y_E_opt;
u_opt_p = S_D*p_i ./ (Z_MD + S_D^2*(Z_ar + Z_B_opt) - Mech_Gain*Elec_Gain./(R_L_opt*Y_E_opt.*jw*C_MD));
e_opt_pressure = Elec_Gain*u_opt_p./Y_E_opt;
figure;
semilogx(f, 20*log10(abs(e_freefield)), f, 20*log10(abs(e_opt)), f, 20*log10(abs(e_opt_pressure)), '--', 'LineWidth', 1.5);
grid on; xlim([1 1e5]); ylim([-75 -25]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
legend('free field, Problem 1 values', 'free field, R_{AS} = 80 M, R_L = 1 G', 'same capsule, pressure response', 'Location', 'southwest');
title('2e: optimised free-field response (official values)');
%%
% Ripple of the optimised free-field curve from 20 Hz to 8 kHz, in dB
% relative to 250 Hz, and its -3 dB point:
band = f >= 20 & f <= 8000;
ripple_dB = [min(20*log10(abs(e_opt(band))/abs(e_opt(k250)))), max(20*log10(abs(e_opt(band))/abs(e_opt(k250))))]
f_minus3dB = f(find(f > 250 & abs(e_opt) < abs(e_opt(k250))/sqrt(2), 1))
%%
% So 0 to +1.5 dB up to 8 kHz and -3 dB at about 17 kHz. The official
% solution calls it "a compromise between sensitivity at the highest
% frequencies and the amount of ripple": less R_AS gives more top end but
% a bigger bump, more R_AS a smoother curve that rolls off earlier.
% LTspice file: P5_2ce_Optimised.asc (run 1 without T, run 2 with T).

%% Summary
% * f_0 = 10.6 kHz, Q = 2.36, M = 9.8 mV/Pa. M_A1 is the unflanged-tube
%   mass 0.6133 rho/(pi r).
% * Below resonance only the springs count: $M = E S_D C_{MT}/x_0$.
% * Circuit: Norton current sources (E C_E0/x_0) u and (E C_MD/x_0) i
%   carry the electrostatic coupling. U = S_D u links the diaphragm to the
%   air in front and behind.
% * R_L sets the low-frequency corner, 1/(2 pi R_L C_E0), and R_AS sets Q.
%   The flattest pressure response is R_AS = 69 Mohm (Q = 0.707).
% * T(s) = 1 + Z_ar/R_A2 (the generator Gpb = p_i/R_A2) adds up to +6 dB at
%   the top. A free-field microphone needs extra damping to cancel it:
%   R_AS = 80 Mohm gives 0 to +1.5 dB up to 8 kHz.
