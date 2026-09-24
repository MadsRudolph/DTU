%% Lecture 1 - Analogies, introduction: problems 1.1 to 1.3, worked
% 34870 Electroacoustics | 31 August 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% official solution's answer is written in the text so you can compare.
%
% The LTspice versions of all three problems are in
% LTspice/Lecture 1 - Analogies/ (P1_1_DC_Duality.asc, P1_2_AC_Duality.asc,
% P1_3_Series_Resonator.asc).

%% The idea behind this whole problem set: duality
% Every circuit has a dual. You get it by swapping
%
% * voltage <-> current (so a voltage source becomes a current source),
% * series <-> parallel (a mesh becomes a node),
% * impedance Z <-> admittance Y (R becomes a conductance G = 1/R, an
%   inductor L becomes a capacitor with the same number, and a capacitor
%   becomes an inductor).
%
% The two circuits then obey exactly the same equations, just with the names
% swapped:
%
% $$v = Z\,i,\quad \sum_{mesh} v = 0,\quad \sum_{node} i = 0 \qquad\Longleftrightarrow\qquad i = Y\,v,\quad \sum_{mesh} i = 0,\quad \sum_{node} v = 0$$
%
% This is why the mechanical world can be drawn in two ways (impedance
% analogy and mobility analogy): they are each other's duals.

%% Problem 1.1 - Duality of a DC circuit: the mathematical proof
% The circuit: a source v0 drives Z1 in series, then Z2 and Z3 in parallel.
% We want v3, the voltage across Z2 || Z3.
%
% *Mesh M1* (Kirchhoff's voltage law around the source loop):
%
% $$v_0 = Z_1 i_1 + v_3$$
%
% *Node N1* (Kirchhoff's current law where Z1 meets Z2 and Z3):
%
% $$i_1 = \frac{v_3}{Z_2} + \frac{v_3}{Z_3}$$
%
% Put the second into the first and solve for v3:
%
% $$v_3 = v_0\,\frac{Z_2 Z_3}{Z_1(Z_2+Z_3) + Z_2 Z_3}$$
%
% *The dual circuit* is a current source i0 with Y1 in parallel, then Y2 in
% series, then Y3. The same two laws with the names swapped (node N1 becomes a
% current rule, mesh M1 a voltage rule) give
%
% $$v_3 = v_0\,\frac{Y_1}{Y_2+Y_3+Y_1} = \frac{v_0}{Z_1\left(1/Z_2 + 1/Z_3\right) + 1}$$
%
% which is the same expression (multiply top and bottom by Z2 Z3). So the
% two circuits are really one set of equations.

%% Problem 1.1 - The LTspice numbers
% Given (the official LTspice circuit):
v0 = 10      % source voltage [V]
Z1 = 100     % R1 [ohm]
Z2 = 2000    % R2, 2k [ohm]
Z3 = 500     % R3 [ohm]
%%
% *Voltage across R2 || R3.* $v_3 = v_0\,\frac{Z_2 Z_3}{Z_1(Z_2+Z_3) + Z_2 Z_3}$
%
% Official solution: 8 V
v3 = v0*Z2*Z3/(Z1*(Z2+Z3) + Z2*Z3)
%%
% *Current through R1* (Ohm's law on the voltage that is left for R1),
% $i_1 = (v_0 - v_3)/Z_1$. Official solution: 20 mA
i1 = (v0 - v3)/Z1
%%
% *Voltage across R1*, $v_1 = Z_1 i_1$. Official solution: 2 V
v1 = Z1*i1
%%
% *Currents in the two parallel resistors*, $i_2 = v_3/Z_2$ and
% $i_3 = v_3/Z_3$. Official solution: i3 = 16 mA (and so i2 = 4 mA)
i2 = v3/Z2
i3 = v3/Z3
%%
% *The dual circuit in LTspice.* LTspice only knows resistors, so the dual's
% conductances are typed in as resistor values: "G1" = 1/R1 = 10m, "G2" =
% 1/R2 = 0.5m, "G3" = 1/R3 = 2m, and the source becomes a 10 A current
% source. The numbers stay, the units swap: every current of the original
% circuit shows up as a voltage in the dual, and every voltage as a current.
G1 = 1/Z1
G2 = 1/Z2
G3 = 1/Z3
%%
% In the dual, the source current splits between G1 (as a "resistance" 10m)
% and G2 + G3 in series. The voltage across the source is the parallel
% combination times the current:
%
% $$V_{d,1} = i_0\,\frac{G_1\,(G_2+G_3)}{G_1 + G_2 + G_3}$$
%
% Official solution: 20 mV (the same number as i1 = 20 mA)
i0 = 10
V_d1 = i0*G1*(G2+G3)/(G1+G2+G3)
%%
% Current through "G2", $I_{G2} = V_{d,1}/(G_2+G_3)$. Official: 8 A (= v3 = 8 V)
I_G2 = V_d1/(G2+G3)
%%
% Current through "G1", $I_{G1} = V_{d,1}/G_1$. Official: 2 A (= v1 = 2 V)
I_G1 = V_d1/G1
%%
% Voltage across "G3", $V_{G3} = G_3 I_{G2}$. Official: 16 mV (= i3 = 16 mA)
V_G3 = G3*I_G2

%% Problem 1.2 - Duality of an AC circuit
% The circuit: a 2 V AC source drives L1 in series, then C3 and L2 in
% parallel. The dual: a 2 A AC source with C1 in parallel, then L3 in
% series, then C2. Each element keeps its number: L1 = 1 mH became C1 = 1 mF,
% C3 = 2 uF became L3 = 2 uH, L2 = 4 mH became C2 = 4 mF.
V = 2         % source amplitude [V] (and 2 A in the dual)
L1 = 1e-3     % 1 mH [H]
C3 = 2e-6     % 2 uF [F]
L2 = 4e-3     % 4 mH [H]
%%
% *The output voltage.* L1 and the parallel pair (C3 || L2) form a voltage
% divider:
%
% $$\frac{V_{out}}{V} = \frac{Z_p}{j\omega L_1 + Z_p},\qquad Z_p = \frac{1}{j\omega C_3 + \frac{1}{j\omega L_2}}$$
%
% Dividing top and bottom by Z_p gives a cleaner form:
%
% $$\frac{V_{out}}{V} = \frac{1}{1 + \frac{L_1}{L_2} - \omega^2 L_1 C_3}$$
%
% The dual gives exactly the same formula with C1, L3, C2 in place of L1, C3,
% L2, so I(C2) in the dual is the same curve as V(vout).
%
% *Low frequency* (omega -> 0): $V_{out} = V\,\frac{L_2}{L_1+L_2}$, in dB.
% The official plot is flat at about 4 dB.
V_out_LF = V*L2/(L1+L2)
V_out_LF_dB = 20*log10(V_out_LF)
%%
% *Resonance* where the denominator is zero:
%
% $$\omega_0^2 = \frac{1 + L_1/L_2}{L_1 C_3}, \qquad f_0 = \frac{\omega_0}{2\pi}$$
%
% The official plot peaks a little under 4 kHz.
f_0 = sqrt((1 + L1/L2)/(L1*C3))/(2*pi)
%%
% *The frequency response*, 20 Hz to 20 kHz like the official .ac line.
f = logspace(log10(20), log10(20000), 3000);
w = 2*pi*f;
H = V ./ (1 + L1/L2 - w.^2*L1*C3);
figure;
subplot(2,1,1);
semilogx(f, 20*log10(abs(H)), 'LineWidth', 1.5);
grid on; xlim([20 20000]); ylim([-30 90]);
ylabel('|V_{out}| = |I(C2)| [dB]');
title('Problem 1.2: V(vout) and its dual I(C2), one curve');
subplot(2,1,2);
semilogx(f, angle(H)*180/pi, 'LineWidth', 1.5);
grid on; xlim([20 20000]);
xlabel('Frequency [Hz]'); ylabel('Phase [deg]');
%%
% *The note on the sheet* ("check default component settings, e.g. series
% resistance for inductor"): LTspice silently gives every inductor
% Rser = 1 mOhm. That makes the top circuit slightly lossy while the dual
% (capacitors have no default loss) stays ideal, so the two peaks are not
% the same height. The exact dual of a 1 mOhm series resistance in an
% inductor is a 1/1m = 1 kOhm parallel resistance on the matching capacitor.
% The LTspice file has both, and then the curves agree to every digit (the
% peak is 62 dB). Without losses the peak would be infinite.

%% Problem 1.3 - Series resonator: the equations
% Given (the LTspice Quick Guide circuit):
R = 10       % [ohm]
L = 10e-3    % 10 mH [H]
C = 2e-6     % 2 uF [F]
v = 1        % AC 1 [V]
%%
% *The mesh equation.* The source voltage is shared by the three elements:
%
% $$v = Ri + L\frac{di}{dt} + \frac{1}{C}\int i\,dt = i\left(R + j\omega L + \frac{1}{j\omega C}\right)$$
%
% so the current is
%
% $$i = \frac{v}{R + j\omega L + \frac{1}{j\omega C}}$$
%
% *Resonance* is where the two imaginary parts cancel, jwL = -1/(jwC):
%
% $$\omega_0 = \frac{1}{\sqrt{LC}}$$
%
% Official solution: 1125.46 Hz
omega_0 = 1/sqrt(L*C)
f_0 = omega_0/(2*pi)
%%
% At resonance only R is left, so the impedance is at its minimum and the
% current at its maximum:
%
% $$Z_{min} = R, \qquad i_{max} = \frac{v}{R}$$
%
% Official solution: 100 mA
Z_min = R
i_max = v/R
%%
% *Quality factor and bandwidth.* How sharp the peak is:
%
% $$Q = \frac{1}{R}\sqrt{\frac{L}{C}}, \qquad BW = \frac{f_0}{Q} = \frac{R}{2\pi L}$$
%
% Official solution: BW = 159 Hz
Q = 1/R*sqrt(L/C)
BW = R/(2*pi*L)

%% Problem 1.3 - Plot current and impedance (amplitude and phase)
% Same sweep as the official plot (10 Hz to about 30 kHz). The impedance is
% $Z = R + j\omega L + 1/(j\omega C)$ and the current $i = v/Z$.
f = logspace(1, log10(30000), 3000);
jw = 1j*2*pi*f;
Z = R + jw*L + 1./(jw*C);
i = v./Z;
figure;
subplot(2,1,1);
semilogx(f, 20*log10(abs(i)), f, 20*log10(abs(Z)), 'LineWidth', 1.5);
grid on; xlim([10 30000]);
ylabel('[dB re 1 A or 1 \Omega]');
legend('current i', 'impedance Z', 'Location', 'south');
title('Problem 1.3: series resonator');
subplot(2,1,2);
semilogx(f, angle(i)*180/pi, f, angle(Z)*180/pi, 'LineWidth', 1.5);
grid on; xlim([10 30000]); ylim([-90 90]);
xlabel('Frequency [Hz]'); ylabel('Phase [deg]');
%%
% Below f_0 the capacitor dominates (Z falls 20 dB per decade, phase -90
% degrees), above f_0 the inductor dominates (Z rises, phase +90 degrees).
% At f_0 the phase passes through 0 and |Z| = 10 ohm = 20 dB, i = 100 mA =
% -20 dB.

%% Problem 1.3 - The same resonator in the mechanical and acoustical domain
% In the impedance analogy the three element types map one to one:
%
% * resistor R <-> damper R_M [kg/s] <-> acoustic resistance R_A [Pa s/m^3]
% * inductor L <-> mass M_M [kg] <-> acoustic mass M_A [kg/m^4]
% * capacitor C <-> compliance C_M [m/N] <-> acoustic compliance C_A [m^5/N]
%
% So to get the same behaviour we simply keep the numbers and change the
% units. Mechanically this is a mass on a spring and a damper, pushed by a
% force f (the sketch on the slide). Acoustically it is a tube (the mass of
% air in the neck, with some flow resistance) on a closed box (the
% compliance), driven by a volume velocity: a Helmholtz resonator.
%
% *Mechanical.* Official solution: R_M = 10 kg/s, M_M = 10 g,
% k = 1/C_M = 0.5 MN/m
R_M = R            % [kg/s]
M_M = L            % [kg]
M_M_gram = M_M*1000
C_M = C            % [m/N]
%%
% The spring stiffness is $k = 1/C_M$, in MN/m (1 MN = 10^6 N):
k_MN_per_m = 1/C_M/1e6
%%
% *Acoustical.* Official solution: R_A = 10 Pa s/m^3, M_A = 10 g/m^4,
% C_A = 0.2 dm^5/N
R_A = R            % [Pa s/m^3]
M_A = L            % [kg/m^4]
M_A_gram_per_m4 = M_A*1000
C_A = C            % [m^5/N]
%%
% In dm^5 (1 dm = 0.1 m, so 1 dm^5 = 10^-5 m^5):
C_A_dm5_per_N = C_A/1e-5
%%
% Same f_0 = 1125 Hz, same Q = 7.07 in all three domains. The LTspice file
% draws all three loops next to each other.

%% Summary
% * A circuit and its dual (series <-> parallel, V <-> I, L <-> C, R <-> 1/R)
%   obey the same equations: 1.1 gives v3 = 8 V and, in the dual, 8 A.
% * LTspice has no conductance element, so dual values are typed in as
%   "resistances" with the same numbers: the units swap.
% * LTspice's default inductor Rser = 1 mOhm breaks exact duality; its dual is
%   Rpar = 1 kOhm on the matching capacitor.
% * Series resonator: f_0 = 1/(2 pi sqrt(LC)) = 1125 Hz, Z_min = R = 10 ohm,
%   i_max = 100 mA, Q = 7.07, bandwidth R/(2 pi L) = 159 Hz.
% * In the impedance analogy mass = L, compliance = C, damper = R, so the same
%   numbers in kg/s, kg, m/N (or Pa s/m^3, kg/m^4, m^5/N) give the same
%   resonator.
