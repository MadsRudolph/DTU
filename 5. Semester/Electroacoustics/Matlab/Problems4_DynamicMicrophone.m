%% Problems 4 - Dynamic microphones (lecture 4B), worked
% 34870 Electroacoustics | 24 September 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% sheet's answer (in square brackets on the sheet) and the official solution
% are written in the text so you can compare.
%
% All values are in SI units (kg, m, s, ohm). Grams, mm/N, cm^3 and inches
% from the sheet are converted when they are typed in.
%
% Air (from the sheet):
rho = 1.18     % air density [kg/m^3]
c = 344        % speed of sound [m/s]

%% The formulas used in this whole problem set
% A dynamic microphone is a diaphragm with a voice coil in a magnet gap.
% Sound pushes the diaphragm, the coil moves, and the motion induces a
% voltage Bl*u. Everything that resists the motion can be moved to the
% mechanical side and added up into one mass, one resistance and one
% compliance (one spring):
%
% *Total mass* (diaphragm + the air it has to push in front of it):
%
% $$M_{MT} = M_{MD} + S_D^2 M_{A1}$$
%
% *Total compliance* (the suspension and the air in the back volume are two
% springs acting on the same diaphragm, so their stiffnesses 1/C add):
%
% $$C_{MT} = \frac{1}{\dfrac{1}{C_{MS}} + \dfrac{S_D^2}{C_{AB}}}, \qquad C_{AB} = \frac{V_{AB}}{\rho c^2}$$
%
% *Total resistance* (suspension + felt behind the diaphragm + the coil
% braking against the load resistor):
%
% $$R_{MT} = R_{MS} + S_D^2 R_{AF} + \frac{(Bl)^2}{R_E + R_L}$$
%
% With those three, the microphone is a second-order band-pass:
%
% $$\frac{e}{p_i} = -\frac{R_L}{R_E+R_L}\cdot\frac{Bl\,S_D}{j\omega M_{MT} + R_{MT} + \dfrac{1}{j\omega C_{MT}}}$$
%
% Below the resonance the spring rules (+6 dB/octave), above it the mass
% rules (-6 dB/octave), and in the middle only R_MT is left, so the
% response is flat there. A dynamic microphone is *damping controlled*.
%
% *Resonance, Q, sensitivity* (the peak value of the band-pass, at f_0):
%
% $$f_0 = \frac{1}{2\pi\sqrt{M_{MT}C_{MT}}}, \qquad Q = \frac{2\pi f_0 M_{MT}}{R_{MT}}, \qquad M = \frac{R_L}{R_E+R_L}\cdot\frac{Bl\,S_D}{R_{MT}}$$
%
% Symbols: M_MD diaphragm + coil mass [kg], C_MS suspension compliance [m/N],
% R_MS suspension damping [Ns/m], S_D diaphragm area [m^2], M_A1 front air
% mass [kg/m^4], C_AB back-volume compliance [m^5/N], R_AF felt resistance
% [Ns/m^5], Bl force factor [Tm], R_E coil resistance, R_L amplifier input
% resistance [ohm].

%% Problem 1a - Total moving mass and total compliance with a 30 cm^3 back volume
% Given:
M_MD = 0.2e-3      % diaphragm + coil mass, 0.2 g [kg]
R_MS = 1           % suspension damping [Ns/m]
C_MS = 0.21e-3     % suspension compliance, 0.21 mm/N [m/N]
d = 0.0254         % diaphragm diameter, 1 inch [m]
Bl = 20            % force factor [Tm]
R_E = 200          % coil resistance [ohm]
R_L = 47e3         % load (amplifier) resistance, 47 kohm [ohm]
V_AB = 30e-6       % back volume, 30 cm^3 [m^3]
%%
% Radius and area of the diaphragm:
%
% $$a = d/2, \qquad S_D = \pi a^2$$
a = d/2
S_D = pi*a^2
%%
% *The air in front of the diaphragm.* The diaphragm has to push some air
% along with it. The official solution models the front as a piston at the
% end of a tube (the capsule housing), which gives the air mass
%
% $$M_{A1} = 0.6133\,\frac{\rho}{\pi a}$$
%
% (A piston in an infinite baffle would give $8\rho/(3\pi^2 a) = 25.1$
% kg/m^4 instead; with that one the answers in b-d drift by about 2 %.)
%
% Official solution: 18.14 kg/m^4
M_A1 = 0.6133*rho/(pi*a)
%%
% *Total mass.* $M_{MT} = M_{MD} + S_D^2 M_{A1}$, then in grams.
%
% Sheet: 0.205 g
M_MT = M_MD + S_D^2*M_A1
M_MT_gram = M_MT*1000
%%
% The air adds only 0.005 g, so the moving mass is almost all diaphragm and
% coil.
%
% *Back-volume compliance.* A closed volume of air is a spring:
%
% $$C_{AB} = \frac{V_{AB}}{\rho c^2}$$
C_AB = V_AB/(rho*c^2)
%%
% *Total compliance.* $C_{MT} = 1/(1/C_{MS} + S_D^2/C_{AB})$, then in mm/N.
%
% Sheet: 0.168 mm/N
C_MT = 1/(1/C_MS + S_D^2/C_AB)
C_MT_mm_per_N = C_MT*1000
%%
% The back volume makes the diaphragm stiffer: 0.21 mm/N alone, 0.168 mm/N
% with the 30 cm^3 of air behind it.

%% Problem 1b - Back volume for a 1 kHz resonance
% The mass is fixed, so the resonance can only be moved with the
% compliance. Solve $f_0 = 1/(2\pi\sqrt{M_{MT}C_{MT}})$ for C_MT:
%
% $$C_{MT} = \frac{1}{(2\pi f_0)^2 M_{MT}}$$
f_0 = 1000         % desired resonance [Hz]
C_MT2 = 1/((2*pi*f_0)^2*M_MT)
%%
% Then take the stiffness of the suspension out again. What is left is the
% stiffness the back volume must supply:
%
% $$\frac{S_D^2}{C_{AB}} = \frac{1}{C_{MT}} - \frac{1}{C_{MS}} \quad\Longrightarrow\quad C_{AB} = \frac{S_D^2}{\dfrac{1}{C_{MT}} - \dfrac{1}{C_{MS}}}$$
C_AB2 = S_D^2/(1/C_MT2 - 1/C_MS)
%%
% And back to a volume, $V_{AB} = C_{AB}\,\rho c^2$, in cm^3 (1 m^3 = 10^6 cm^3).
%
% Sheet: 10.8 cm^3
V_AB2 = C_AB2*rho*c^2
V_AB2_cm3 = V_AB2*1e6
%%
% A smaller volume is a stiffer spring, so the resonance moves up: 30 cm^3
% gives about 850 Hz, 10.8 cm^3 gives 1 kHz.
f_0_with_30cm3 = 1/(2*pi*sqrt(M_MT*C_MT))

%% Problem 1c - Felt resistance for 1 mV/Pa, and the bandwidth
% In the flat middle of the band only R_MT is left, so the sensitivity is
%
% $$M = \frac{Bl\,S_D}{R_{MT}} \quad\Longrightarrow\quad R_{MT} = \frac{Bl\,S_D}{M}$$
%
% (The official solution leaves out the factor $R_L/(R_E+R_L) = 0.9958$;
% with 47 kohm against 200 ohm that is only -0.04 dB, so we do the same.)
M = 1e-3           % wanted sensitivity, 1 mV/Pa [V/Pa]
R_MT = Bl*S_D/M
%%
% R_MT is made of three parts. Solve $R_{MT} = R_{MS} + S_D^2R_{AF} + (Bl)^2/(R_E+R_L)$ for the felt:
%
% $$R_{AF} = \frac{R_{MT} - R_{MS} - \dfrac{(Bl)^2}{R_E+R_L}}{S_D^2}$$
%
% Sheet: 3.56e7 Ns/m^5
R_AF = (R_MT - R_MS - Bl^2/(R_E + R_L))/S_D^2
%%
% The electrical damping (Bl)^2/(R_E+R_L) is only 0.0085 Ns/m here, because
% the 47 kohm load lets almost no current flow. Nearly all of the 10.1 Ns/m
% comes from the felt.
electrical_damping = Bl^2/(R_E + R_L)
%%
% *Q and bandwidth.* $Q = 2\pi f_0 M_{MT}/R_{MT}$, and for a band-pass the
% -3 dB bandwidth is
%
% $$BW = f_b - f_a = \frac{f_0}{Q}$$
%
% Sheet: 7.88 kHz
Q = 2*pi*f_0*M_MT/R_MT
BW = f_0/Q
BW_kHz = BW/1000
%%
% Q = 0.127 is very heavily damped. That is on purpose: the heavier the
% damping, the wider the flat band.

%% Problem 1d - The -3 dB frequencies f_a and f_b
% Two facts about a second-order band-pass: the two -3 dB points sit
% symmetrically around f_0 on a log axis, and their distance is the
% bandwidth:
%
% $$f_a f_b = f_0^2, \qquad f_b - f_a = \frac{f_0}{Q}$$
%
% Solving those two together gives
%
% $$f_{a} = f_0\left(\sqrt{1 + \frac{1}{4Q^2}} - \frac{1}{2Q}\right), \qquad f_{b} = f_0\left(\sqrt{1 + \frac{1}{4Q^2}} + \frac{1}{2Q}\right)$$
%
% (The official solution writes $f_a = f_0/a_1$, $f_b = f_0 a_1$ and
% solves $BW = f_0a_1 - f_0/a_1$ for a_1 = 8.006; it is the same thing.)
%
% Sheet: 125 Hz and 8.01 kHz
f_a = f_0*(sqrt(1 + 1/(4*Q^2)) - 1/(2*Q))
f_b = f_0*(sqrt(1 + 1/(4*Q^2)) + 1/(2*Q))
f_b_kHz = f_b/1000
%%
% Check: $f_b - f_a$ should be the bandwidth from 1c, and $f_af_b$ should be
% $f_0^2 = 10^6$.
f_b - f_a
f_a*f_b
%%
% *The finished design over frequency.* A frequency axis from 10 Hz to
% 100 kHz and $j\omega$:
f = logspace(1, 5, 2000);
jw = 1j*2*pi*f;
%%
% The band-pass from the top of this script, with the 1b and 1c values
% (C_MT2 and R_MT):
%
% $$\frac{e}{p_i} = -\frac{Bl\,S_D}{j\omega M_{MT} + R_{MT} + 1/(j\omega C_{MT})}$$
H_1 = -Bl*S_D./(jw*M_MT + R_MT + 1./(jw*C_MT2));
figure;
semilogx(f, 20*log10(abs(H_1)), 'LineWidth', 1.5);
hold on; xline([f_a f_b], 'r--'); yline(20*log10(M) - 3, 'k:'); hold off;
grid on; xlim([10 1e5]); ylim([-90 -55]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
title('Problem 1: the designed microphone (1 mV/Pa = -60 dB)');

%% Problem 2 - The microphone as a circuit (LTspice)
% The LTspice models are in
% LTspice/Problems 4 - Dynamic Microphone/ (written by p4.py, one .asc per
% part). They use the official solution's circuit, the impedance analogy in
% all three domains, so each domain is one loop:
%
% * *Acoustical loop:* the incident pressure p_i (1 V = 1 Pa) drives volume
%   velocity through the front air mass M_A1 (an inductor), then through the
%   diaphragm, then through the back network (felt R_AF and back volume
%   C_AB, a resistor and a capacitor to ground). The diaphragm is an F
%   source that forces the loop current to be U = S_D u.
% * *Mechanical loop:* the pressure difference across the diaphragm,
%   p_D = p_front - p_back, becomes a force S_D p_D (an E source). It drives
%   the velocity u through M_MD (inductor), R_MS (resistor) and C_MS
%   (capacitor). An H source adds the coil's reaction force Bl*i.
% * *Electrical loop:* an H source makes the induced voltage Bl*u, which
%   drives a current through R_E into the load R_L. The voltage across R_L
%   is the output. Since p_i = 1 Pa, V(out) is the sensitivity in V/Pa.
%
% Here we compute the same thing directly. The only change from problem 1 is
% that the back network is now written as one acoustic impedance Z_B (so we
% can change it in 2c and 2d):
%
% $$Z_M = j\omega M_{MD} + R_{MS} + \frac{1}{j\omega C_{MS}} + \frac{(Bl)^2}{R_E+R_L}$$
%
% $$\frac{e}{p_i} = -\frac{R_L}{R_E+R_L}\cdot\frac{Bl\,S_D}{Z_M + S_D^2\left(j\omega M_{A1} + Z_B\right)}$$
%
% With $Z_B = R_{AF} + 1/(j\omega C_{AB})$ this is exactly the band-pass
% from problem 1.
Z_M = jw*M_MD + R_MS + 1./(jw*C_MS) + Bl^2/(R_E + R_L);

%% Problem 2a - The model with V = 5 cm^3 and R_AF = 2e7 Ns/m^5
% LTspice file: P4_2a_Basic.asc (plot V(out)).
V = 5e-6           % back volume, 5 cm^3 [m^3]
R_AF_2a = 2e7      % felt resistance [Ns/m^5]
C_AB_2a = V/(rho*c^2)
%%
% Back impedance: felt in series with the volume,
% $Z_B = R_{AF} + 1/(j\omega C_{AB})$, then the response:
Z_B_2a = R_AF_2a + 1./(jw*C_AB_2a);
H_2a = -R_L/(R_E + R_L)*Bl*S_D./(Z_M + S_D^2*(jw*M_A1 + Z_B_2a));
%%
% The hand numbers for this design, from the formulas at the top:
C_MT_2a = 1/(1/C_MS + S_D^2/C_AB_2a)
R_MT_2a = R_MS + S_D^2*R_AF_2a + Bl^2/(R_E + R_L)
f_0_2a = 1/(2*pi*sqrt(M_MT*C_MT_2a))
Q_2a = 2*pi*f_0_2a*M_MT/R_MT_2a
M_2a_mV = R_L/(R_E + R_L)*Bl*S_D/R_MT_2a*1000
M_2a_dB = 20*log10(M_2a_mV/1000)
f_a_2a = f_0_2a*(sqrt(1 + 1/(4*Q_2a^2)) - 1/(2*Q_2a))
f_b_2a = f_0_2a*(sqrt(1 + 1/(4*Q_2a^2)) + 1/(2*Q_2a))
%%
% LTspice gives the same: peak 1.643 mV/Pa (-55.69 dB re 1 V/Pa) at
% 1.22 kHz, -3 dB band 291 Hz to 5.07 kHz.
%
% The smaller volume (5 instead of 10.8 cm^3) is stiffer, so f_0 moves up to
% 1.2 kHz. The weaker felt (2e7 instead of 3.56e7) damps less, so the
% sensitivity goes up to 1.64 mV/Pa and the band gets narrower.
figure;
semilogx(f, 20*log10(abs(H_2a)), 'LineWidth', 1.5);
grid on; xlim([10 1e5]); ylim([-90 -50]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
title('Problem 2a: V = 5 cm^3, R_{AF} = 2e7 Ns/m^5');

%% Problem 2b - Sensitivity 0.3 mV/Pa and 3 mV/Pa
% LTspice file: P4_2b_Sensitivity.asc (it steps R_AF over the three values
% with .step param Raf list ...).
%
% The sensitivity is $M = \frac{R_L}{R_E+R_L}\frac{Bl\,S_D}{R_{MT}}$, and
% the felt is the only term in R_MT we can easily change. Same steps as in
% 1c, now keeping the $R_L/(R_E+R_L)$ factor so the peak lands exactly on
% the target:
%
% $$R_{AF} = \frac{1}{S_D^2}\left(\frac{R_L}{R_E+R_L}\cdot\frac{Bl\,S_D}{M} - R_{MS} - \frac{(Bl)^2}{R_E+R_L}\right)$$
M_low = 0.3e-3     % 0.3 mV/Pa [V/Pa]
M_high = 3e-3      % 3 mV/Pa [V/Pa]
R_AF_low = (R_L/(R_E + R_L)*Bl*S_D/M_low - R_MS - Bl^2/(R_E + R_L))/S_D^2
R_AF_high = (R_L/(R_E + R_L)*Bl*S_D/M_high - R_MS - Bl^2/(R_E + R_L))/S_D^2
%%
% More felt (1.27e8) gives LESS sensitivity; less felt (9.2e6) gives more.
% The back volume is not touched, so f_0 stays at 1.22 kHz.
H_low = -R_L/(R_E + R_L)*Bl*S_D./(Z_M + S_D^2*(jw*M_A1 + R_AF_low + 1./(jw*C_AB_2a)));
H_high = -R_L/(R_E + R_L)*Bl*S_D./(Z_M + S_D^2*(jw*M_A1 + R_AF_high + 1./(jw*C_AB_2a)));
figure;
semilogx(f, 20*log10(abs(H_low)), f, 20*log10(abs(H_2a)), f, 20*log10(abs(H_high)), 'LineWidth', 1.5);
grid on; xlim([10 1e5]); ylim([-100 -45]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
legend('R_{AF} = 1.27e8: 0.3 mV/Pa', 'R_{AF} = 2e7: 1.64 mV/Pa (2a)', 'R_{AF} = 9.2e6: 3 mV/Pa', 'Location', 'south');
title('Problem 2b: the felt sets the sensitivity');
%%
% *What it shows:* the bandwidth is $f_0/Q = R_{MT}/(2\pi M_{MT})$ and the
% sensitivity is $Bl\,S_D/R_{MT}$. Both depend on the same R_MT, so their
% product is fixed:
%
% $$M\cdot BW = \frac{Bl\,S_D}{2\pi M_{MT}}$$
%
% Ten times the sensitivity costs ten times the bandwidth. LTspice: 0.300
% mV/Pa with a band of about 56 Hz - 26.2 kHz, and 3.00 mV/Pa with only
% 477 Hz - 3.09 kHz (the bandwidths computed below).
M_times_BW = Bl*S_D/(2*pi*M_MT)
Q_low = 2*pi*f_0_2a*M_MT/(R_MS + S_D^2*R_AF_low + Bl^2/(R_E + R_L));
Q_high = 2*pi*f_0_2a*M_MT/(R_MS + S_D^2*R_AF_high + Bl^2/(R_E + R_L));
BW_low_kHz = f_0_2a/Q_low/1000
BW_high_kHz = f_0_2a/Q_high/1000

%% Problem 2c - More treble: two back cavities joined by a damped tube
% LTspice file: P4_2c_TwoCavities.asc.
%
% The sheet's figure: a small cavity V_1 right behind the diaphragm, a
% narrow tube with damping material, and a large cavity V_2. The official
% solution starts from the problem-1 design (R_AF = 35.5e6, V = 10.8 cm^3,
% C_AB = 77.5 pF in LTspice units) and splits it like this:
%
% * C_AB1 = 0.3e-12 m^5/N: the small cavity V_1 (a tiny 0.04 cm^3)
% * R_AT = 35.5e6 Ns/m^5: the felt, now sitting IN the tube
% * M_AT = 50 kg/m^4: the air mass of the tube
% * C_AB2 = 76e-12 m^5/N: the large cavity V_2 (10.6 cm^3)
%
% In the circuit, C_AB1 goes from the back of the diaphragm to ground, and
% in parallel with it the tube (R_AT + M_AT in series) leads to C_AB2:
%
% $$Z_B = \frac{1}{j\omega C_{AB1} + \dfrac{1}{R_{AT} + j\omega M_{AT} + \dfrac{1}{j\omega C_{AB2}}}}$$
C_AB1 = 0.3e-12    % small cavity V1 [m^5/N]
R_AT = 35.5e6      % damping in the tube [Ns/m^5]
M_AT = 50          % air mass in the tube [kg/m^4]
C_AB2 = 76e-12     % large cavity V2 [m^5/N]
V_1_cm3 = C_AB1*rho*c^2*1e6
V_2_cm3 = C_AB2*rho*c^2*1e6
%%
% The reference (the official's blue curve) is the problem-1 design, with
% the felt directly behind the diaphragm:
R_AF_ref = 35.5e6
C_AB_ref = 77.5e-12
H_ref = -R_L/(R_E + R_L)*Bl*S_D./(Z_M + S_D^2*(jw*M_A1 + R_AF_ref + 1./(jw*C_AB_ref)));
%%
% The split back network typed in (the 1T leak in the LTspice file is not
% needed here):
Z_B_2c = 1./(jw*C_AB1 + 1./(R_AT + jw*M_AT + 1./(jw*C_AB2)));
H_2c = -R_L/(R_E + R_L)*Bl*S_D./(Z_M + S_D^2*(jw*M_A1 + Z_B_2c));
%%
% *What happens physically.* At low and middle frequencies the small cavity
% is a very weak path (a tiny capacitor), so all the flow goes through the
% felt into V_2, and the microphone is the same as the problem-1 design. At
% high frequencies the small cavity takes over: its impedance
% $1/(\omega C_{AB1})$ drops below R_AT at about
%
% $$f_{bypass} = \frac{1}{2\pi R_{AT} C_{AB1}}$$
f_bypass_kHz = 1/(2*pi*R_AT*C_AB1)/1000
%%
% Above that, the air just goes in and out of V_1 and no longer has to
% squeeze through the felt. The damping disappears, and the moving mass now
% resonates with the stiff little cavity V_1:
%
% $$f_{V1} = \frac{1}{2\pi}\sqrt{\frac{1/C_{MS} + S_D^2/C_{AB1}}{M_{MT}}}$$
f_V1_kHz = 1/(2*pi)*sqrt((1/C_MS + S_D^2/C_AB1)/M_MT)/1000
%%
% That second resonance, around 10 kHz, lifts the top end just where the
% mass roll-off would have pulled it down.
figure;
semilogx(f, 20*log10(abs(H_ref)), f, 20*log10(abs(H_2c)), 'LineWidth', 1.5);
grid on; xlim([10 1e5]); ylim([-110 -55]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
legend('problem-1 design (felt + one volume)', '2c: V_1 + damped tube + V_2', 'Location', 'south');
title('Problem 2c: two back cavities extend the treble');
%%
% Where does each curve fall 3 dB below its 1 kHz value, on the high side?
k1 = find(f >= 1000, 1);
f_3dB_high_ref_kHz = f(find(f > 1000 & abs(H_ref) < abs(H_ref(k1))/sqrt(2), 1))/1000
f_3dB_high_2c_kHz = f(find(f > 1000 & abs(H_2c) < abs(H_2c(k1))/sqrt(2), 1))/1000
%%
% *Things to try:* a bigger V_1 moves the second resonance down and bypasses
% the felt earlier; a smaller R_AT makes the step up sharper but also turns
% the V_1/V_2 pair into a resonator with a dip. The damping has to be in
% the tube for the transition to be smooth.

%% Problem 2d - More bass: a vent tube in the large cavity
% LTspice file: P4_2d_Vent.asc (this is the official solution's compensated
% microphone, the red curve).
%
% A tube goes from V_2 to the outside air. In the circuit it is R_AP + M_AP
% from the V_2 node back to the incident pressure p_i (not to ground, since
% the outside air at the back of the microphone is at the sound pressure
% too). Official values:
M_AP = 80e3        % air mass in the vent [kg/m^4]
R_AP = 3e6         % damping in the vent [Ns/m^5]
%%
% *Physics.* The vent mass and the big cavity make a Helmholtz resonator:
%
% $$f_H = \frac{1}{2\pi\sqrt{M_{AP}\,C_{AB2}}}$$
f_H = 1/(2*pi*sqrt(M_AP*C_AB2))
%%
% Near f_H the air in the vent swings strongly, and in the right phase to
% push on the back of the diaphragm with the sound: that is the bump that
% props up the bass. Far below f_H the vent simply lets the sound pressure
% into the back, both sides of the diaphragm see the same pressure, and the
% output drops fast (12 dB/octave extra) - the price of the bass boost.
%
% *Maths.* Now the pressure behind the diaphragm has two causes: the
% diaphragm's own flow U through Z_B (as before, now including the vent),
% plus a fraction alpha of p_i that leaks in through the vent:
%
% $$p_{back} = Z_B\,U + \alpha\,p_i$$
%
% Z_B is the back network seen from the diaphragm with the vent grounded:
%
% $$Z_B = \frac{1}{j\omega C_{AB1} + \dfrac{1}{R_{AT} + j\omega M_{AT} + Z_2}}, \qquad Z_2 = \frac{1}{j\omega C_{AB2} + \dfrac{1}{R_{AP} + j\omega M_{AP}}}$$
Z_vent = R_AP + jw*M_AP;
Z_2 = 1./(jw*C_AB2 + 1./Z_vent);
Z_B_2d = 1./(jw*C_AB1 + 1./(R_AT + jw*M_AT + Z_2));
%%
% alpha is two voltage dividers: p_i through the vent onto V_2 (which sees
% C_AB2 in parallel with the tube + V_1), then from V_2 through the tube
% onto V_1:
%
% $$\alpha = \frac{Z_{2'}}{Z_{vent} + Z_{2'}}\cdot\frac{1/(j\omega C_{AB1})}{R_{AT} + j\omega M_{AT} + 1/(j\omega C_{AB1})}, \qquad Z_{2'} = \frac{1}{j\omega C_{AB2} + \dfrac{1}{R_{AT} + j\omega M_{AT} + 1/(j\omega C_{AB1})}}$$
Z_2p = 1./(jw*C_AB2 + 1./(R_AT + jw*M_AT + 1./(jw*C_AB1)));
alpha = Z_2p./(Z_vent + Z_2p) .* (1./(jw*C_AB1))./(R_AT + jw*M_AT + 1./(jw*C_AB1));
%%
% Only the pressure DIFFERENCE drives the diaphragm, so p_i is replaced by
% $(1-\alpha)\,p_i$:
%
% $$\frac{e}{p_i} = -\frac{R_L}{R_E+R_L}\cdot\frac{Bl\,S_D\,(1-\alpha)}{Z_M + S_D^2\left(j\omega M_{A1} + Z_B\right)}$$
%
% At DC alpha = 1 and the output is zero: that is the vent short-circuiting
% the pressure.
H_2d = -R_L/(R_E + R_L)*Bl*S_D*(1 - alpha)./(Z_M + S_D^2*(jw*M_A1 + Z_B_2d));
figure;
semilogx(f, 20*log10(abs(H_ref)), f, 20*log10(abs(H_2c)), '--', f, 20*log10(abs(H_2d)), 'LineWidth', 1.5);
grid on; xlim([10 1e5]); ylim([-110 -55]);
xlabel('Frequency [Hz]'); ylabel('Sensitivity [dB re 1 V/Pa]');
legend('problem-1 design', '2c: two cavities', '2d: two cavities + vent (official red curve)', 'Location', 'south');
title('Problem 2d: the vent extends the bass');
%%
% The low -3 dB point, relative to the 1 kHz value, before and after:
f_3dB_low_ref = f(find(f < 1000 & abs(H_ref) >= abs(H_ref(k1))/sqrt(2), 1))
f_3dB_low_2d = f(find(f < 1000 & abs(H_2d) >= abs(H_2d(k1))/sqrt(2), 1))
f_3dB_high_2d_kHz = f(find(f > 1000 & abs(H_2d) < abs(H_2d(k1))/sqrt(2), 1))/1000
%%
% So the band grows from 125 Hz - 8 kHz to about 46 Hz - 13 kHz (-3 dB
% relative to the 1 kHz level; LTspice gives the same numbers).
%
% Compared with the official plot: the blue curve is at -60 dB (1 mV/Pa) and
% slopes off from about 1 kHz both ways; the red curve is flat at -60 dB
% from about 60 Hz to 7 kHz, has a small bump just above 50 Hz and falls
% steeply below it. The curves above are the same.
%
% *Things to try:* a bigger M_AP or C_AB2 moves the bump down; less R_AP
% makes the bump taller (with too little it becomes a peak followed by a
% dip).

%% Summary
% * A dynamic microphone is one band-pass: M_MT = M_MD + S_D^2 M_A1,
%   C_MT from the suspension and the back volume, R_MT from suspension,
%   felt and coil.
% * It works in the flat, damping-controlled middle: M = Bl S_D / R_MT.
% * 1a: 0.205 g and 0.168 mm/N. 1b: 10.8 cm^3 for 1 kHz. 1c: R_AF =
%   3.56e7 Ns/m^5, Q = 0.127, BW = 7.88 kHz. 1d: 125 Hz and 8.01 kHz.
% * Sensitivity times bandwidth is fixed (2b): more felt, less output but a
%   wider band.
% * A small cavity behind the diaphragm bypasses the felt at high frequency
%   and adds a second resonance near 10 kHz (2c).
% * A vent from the large cavity to the outside is a Helmholtz resonator that
%   lifts the bass around f_H, and cuts steeply below it (2d).
% * The front air mass follows the official convention, a piston in a tube:
%   M_A1 = 0.6133 rho/(pi a).
