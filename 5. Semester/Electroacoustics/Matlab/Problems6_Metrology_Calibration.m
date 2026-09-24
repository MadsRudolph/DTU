%% Problems 6 - Metrology and calibration, worked
% 34870 Electroacoustics | 24 September 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% official solution's answer is written in the text so you can compare.
%
% The microphone is the one from Problems 5, all values in SI units.
rho = 1.18         % air density [kg/m^3]
c = 344            % speed of sound [m/s]
eps0 = 8.85e-12    % permittivity [F/m]
C_MD = 4e-6        % diaphragm compliance [m/N]
M_MD = 0.050e-3    % diaphragm mass, 0.050 g [kg]
R_MD = 1           % diaphragm damping [Ns/m]
r = 9e-3           % effective diaphragm radius, 9 mm [m]
M_AS = 100         % backplate holes, acoustic mass [kg/m^4]
R_AS = 1e7         % backplate holes, acoustic resistance [Ns/m^5]
V_AB2 = 1e-6       % back volume, 1 cm^3 [m^3]
E = 200            % polarisation voltage [V]
x_0 = 20e-6        % gap, 20 µm [m]
R_L = 500e6        % load resistance, 500 Mohm [ohm]
%%
% The quantities from Problems 5 that we need again:
S_D = pi*r^2
C_AB2 = V_AB2/(rho*c^2)
M_A1 = 0.6133*rho/(pi*r)

%% Two words that sound alike
% * *Pressure sensitivity* M (mV/Pa): how many volts the microphone gives
% per pascal.
% * *Sensitivity coefficient* (GUM): how much a result moves when one input
% moves, the partial derivative $\partial M/\partial x_i$.
%
% The GUM rule for uncorrelated inputs: every input's standard uncertainty,
% times its sensitivity coefficient, added in quadrature:
%
% $$u_c(M) = \sqrt{\sum_i \left(\frac{\partial M}{\partial x_i}\right)^2 u^2(x_i)}$$

%% Problem 1a - The sensitivity coefficients from the theory
% From Problems 5, below resonance
%
% $$M = \frac{E\,S_D\,C_{MT}}{x_0}, \qquad C_{MT} = \frac{1}{\dfrac{1}{C_{MD}} + \dfrac{S_D^2}{C_{AB2}}}$$
%
% M_MD and R_MD are not in this formula at all (below resonance only the
% springs count), so
%
% $$\frac{\partial M}{\partial M_{MD}} = 0, \qquad \frac{\partial M}{\partial R_{MD}} = 0$$
%
% For C_MD use the chain rule, $\frac{\partial M}{\partial C_{MD}} = \frac{E S_D}{x_0}\frac{\partial C_{MT}}{\partial C_{MD}}$.
% C_MT is 1/v with $v = 1/C_{MD} + S_D^2/C_{AB2}$, and $dv/dC_{MD} = -1/C_{MD}^2$,
% so the quotient rule gives $\frac{\partial C_{MT}}{\partial C_{MD}} = -\frac{1}{v^2}\cdot\left(-\frac{1}{C_{MD}^2}\right)$:
%
% $$\frac{\partial M}{\partial C_{MD}} = \frac{E\,S_D}{x_0}\;\frac{1}{C_{MD}^2\left(\dfrac{1}{C_{MD}} + \dfrac{S_D^2}{C_{AB2}}\right)^2}$$

%% Problem 1b - The numbers
% Official solution: 2.3701e3 (V/Pa)/(m/N)
dM_dM_MD = 0
dM_dR_MD = 0
dM_dC_MD = E*S_D/x_0 * 1/(C_MD^2*(1/C_MD + S_D^2/C_AB2)^2)
%%
% What it means: if C_MD grew by 1e-7 m/N (2.5 %), M would grow by
% 2370 * 1e-7 = 0.24 mV/Pa.

%% Problem 1c - Combined standard uncertainty
% The standard deviations are 10 % of the values:
u_M_MD = 0.1*M_MD
u_R_MD = 0.1*R_MD
u_C_MD = 0.1*C_MD
%%
% $$u_c(M) = \sqrt{\left(\frac{\partial M}{\partial M_{MD}}u(M_{MD})\right)^2 + \left(\frac{\partial M}{\partial R_{MD}}u(R_{MD})\right)^2 + \left(\frac{\partial M}{\partial C_{MD}}u(C_{MD})\right)^2}$$
%
% Official solution: 0.948 mV/Pa
u_c_M = sqrt((dM_dM_MD*u_M_MD)^2 + (dM_dR_MD*u_R_MD)^2 + (dM_dC_MD*u_C_MD)^2)
u_c_M_mV = u_c_M*1000
%%
% Relative to M itself:
M = E*S_D/(x_0*(1/C_MD + S_D^2/C_AB2))
relative_uncertainty_percent = u_c_M/M*100
%%
% A 10 % spread in C_MD gives only 9.7 % in M, because the back-volume air
% spring (which is not uncertain here) carries 3.5 % of the total
% stiffness:
air_share_of_stiffness_percent = (S_D^2/C_AB2)/(1/C_MD + S_D^2/C_AB2)*100

%% Problem 1d - Comment on the hypotheses
% * *Neglecting other contributions:* E, x_0, S_D and C_AB2 (temperature and
% static pressure) are also uncertain, and M depends on E/x_0 directly, so
% in a real budget they matter at least as much as C_MD.
% * *No correlation:* a condenser microphone is a tightly coupled system. A
% softer diaphragm (larger C_MD) is pulled further towards the backplate by
% the polarisation voltage, so x_0 shrinks. C_MD and x_0 are therefore
% correlated, and the uncorrelated formula is only an exercise. (Official
% solution: "too simplistic and only valid as an exercise".)

%% Problem 1 as a finite difference (what Problem 2c does in LTspice)
% Change C_MD by +10 % and -10 % and recompute M, instead of taking the
% derivative:
M_Cplus = E*S_D/(x_0*(1/(1.1*C_MD) + S_D^2/C_AB2))
M_Cminus = E*S_D/(x_0*(1/(0.9*C_MD) + S_D^2/C_AB2))
%%
% The changes in mV/Pa:
dM_plus_mV = (M_Cplus - M)*1000
dM_minus_mV = (M_Cminus - M)*1000
%%
% The slope between the two points is the sensitivity coefficient again
% (compare 2370.1):
dM_dC_MD_finite = (M_Cplus - M_Cminus)/(0.2*C_MD)
%%
% +0.945 and -0.951 are not equal: M(C_MD) curves slightly, so the
% derivative is only exact for small steps.

%% Problem 2 - The same thing with the circuit
% LTspice file: LTspice/Problems 5-6 - Condenser Microphone/P6_Q2_Sensitivity.asc.
% It is the Problems 5 Q2b circuit with a .step over 14 runs (nominal, then
% M_MD, R_MD, C_MD at x0.9 and x1.1, all of it once without and once with
% Gpb). A .meas line prints M at 250 Hz for every run in the error log.
%
% Here the same circuit is solved in MATLAB (the formulas are explained in
% the Problems 5 script). The elements that do not change:
C_AB1 = C_AB2/200;
C_E0 = eps0*S_D/x_0;
Elec_Gain = E*C_E0/x_0;
R_A1 = 0.5045*rho*c/(pi*r^2);
R_A2 = rho*c/(pi*r^2);
C_A1 = 0.55*pi^2*r^3/(rho*c^2);
f = logspace(0, 5, 3000);
jw = 1j*2*pi*f;
Z_ar = 1 ./ ( 1./(jw*M_A1) + 1./(R_A2 + 1./(1/R_A1 + jw*C_A1)) );
Z_B = 1 ./ ( jw*C_AB1 + 1./(R_AS + jw*M_AS + 1./(jw*C_AB2)) );
Y_E = jw*C_E0 + 1/R_L;
T = 1 + Z_ar/R_A2;
%%
% The response for 1 Pa, nominal values, Gpb off (T = 1):
%
% $$e = \frac{\text{Elec\_Gain}}{Y_E}\cdot\frac{S_D}{j\omega M_{MD} + R_{MD} + \dfrac{1}{j\omega C_{MD}} + S_D^2(Z_{ar}+Z_B) - \dfrac{(E C_{MD}/x_0)\,\text{Elec\_Gain}}{R_L Y_E\, j\omega C_{MD}}}$$
e_nom = Elec_Gain./Y_E .* S_D./(jw*M_MD + R_MD + 1./(jw*C_MD) + S_D^2*(Z_ar + Z_B) - (E*C_MD/x_0)*Elec_Gain./(R_L*Y_E.*jw*C_MD));

%% Problem 2a - M at 250 Hz
k250 = find(f >= 250, 1);
M_250_mV = abs(e_nom(k250))*1000
%%
% Official solution: 9.6 mV/Pa. The circuit gives 9.83, the same as
% Problems 5 (9.8). The 2 % difference comes from the official figure,
% where the electrical source gain is typed as 1.1m instead of
% E C_E0/x_0 = 1.126m. The output is proportional to that gain:
Elec_Gain
M_250_with_rounded_gain_mV = M_250_mV*1.1e-3/Elec_Gain
%%
figure;
semilogx(f, abs(e_nom)*1000, 'LineWidth', 1.5);
grid on; xlim([10 1e5]);
xlabel('Frequency [Hz]'); ylabel('M [mV/Pa] (linear, as the sheet asks)');
title('Problems 5 Q2b circuit, Gpb off');

%% Problem 2b - f_0 and Q from the simulated response (the slide method)
% Lecture 6B slide 20:
%
% # f_0 is where the phase has dropped 90 degrees from its low-frequency
% value.
% # Q is the linear ratio $|M(f_0)| / |M(f \ll f_0)|$.
%
% Phase drop relative to 250 Hz, in degrees:
phase_drop = (angle(e_nom(k250)) - unwrap(angle(e_nom)))*180/pi;
k0 = find(f > 250 & phase_drop >= 90, 1);
%%
% The 90 degree point falls between two frequency points (k0-1 and k0), so
% interpolate between them (what the cursor does by eye):
f_0_sim = interp1(phase_drop(k0-1:k0), f(k0-1:k0), 90)
Q_sim = interp1(f(k0-1:k0), abs(e_nom(k0-1:k0)), f_0_sim)/abs(e_nom(k250))
%%
% The theory from Problems 5:
M_MT = M_MD + S_D^2*(M_A1 + M_AS);
C_MT = 1/(1/C_MD + S_D^2/C_AB2);
R_MT = R_MD + S_D^2*R_AS;
f_0 = 1/(2*pi*sqrt(M_MT*C_MT))
Q = 2*pi*f_0*M_MT/R_MT
%%
% Close, but f_0 is 0.8 % higher and Q 6 % lower in the circuit. That is
% real physics, not a mistake: at 10 kHz ka = 1.6, so the air in front is
% no longer a pure mass M_A1. It has less mass and some radiation resistance
% (R_A1, R_A2), and the hand formula leaves that out:
ka_at_f0 = 2*pi*f_0*r/c

%% Problem 2c - Vary M_MD, R_MD, C_MD by 10 % in the circuit
% The circuit response at 250 Hz, with one value changed at a time (Gpb
% off). Each line is the formula from above at f = 250 Hz with one value
% times 1.1. First the elements at 250 Hz only:
jw250 = jw(k250);
Zar250 = Z_ar(k250);
ZB250 = Z_B(k250);
YE250 = Y_E(k250);
%%
% Nominal:
M250 = abs(Elec_Gain/YE250 * S_D/(jw250*M_MD + R_MD + 1/(jw250*C_MD) + S_D^2*(Zar250 + ZB250) - (E*C_MD/x_0)*Elec_Gain/(R_L*YE250*jw250*C_MD)))
%%
% M_MD + 10 %:
M250_Mplus = abs(Elec_Gain/YE250 * S_D/(jw250*1.1*M_MD + R_MD + 1/(jw250*C_MD) + S_D^2*(Zar250 + ZB250) - (E*C_MD/x_0)*Elec_Gain/(R_L*YE250*jw250*C_MD)));
dM_Mplus_mV = (M250_Mplus - M250)*1000
%%
% R_MD + 10 %:
M250_Rplus = abs(Elec_Gain/YE250 * S_D/(jw250*M_MD + 1.1*R_MD + 1/(jw250*C_MD) + S_D^2*(Zar250 + ZB250) - (E*C_MD/x_0)*Elec_Gain/(R_L*YE250*jw250*C_MD)));
dM_Rplus_mV = (M250_Rplus - M250)*1000
%%
% C_MD + 10 % and - 10 % (C_MD also sits in the Mech_Gain = E C_MD/x_0 of
% the electrostatic source):
M250_Cplus = abs(Elec_Gain/YE250 * S_D/(jw250*M_MD + R_MD + 1/(jw250*1.1*C_MD) + S_D^2*(Zar250 + ZB250) - (E*1.1*C_MD/x_0)*Elec_Gain/(R_L*YE250*jw250*1.1*C_MD)));
M250_Cminus = abs(Elec_Gain/YE250 * S_D/(jw250*M_MD + R_MD + 1/(jw250*0.9*C_MD) + S_D^2*(Zar250 + ZB250) - (E*0.9*C_MD/x_0)*Elec_Gain/(R_L*YE250*jw250*0.9*C_MD)));
dM_Cplus_mV = (M250_Cplus - M250)*1000
dM_Cminus_mV = (M250_Cminus - M250)*1000
%%
% Official solution: M_MD and R_MD negligible, C_MD +0.922 / -0.929 mV/Pa.
% We get +0.946 / -0.952. Again the official numbers are ours times
% 1.1/1.126 (the rounded gain):
dM_C_with_rounded_gain_mV = [dM_Cplus_mV, dM_Cminus_mV]*1.1e-3/Elec_Gain
%%
% And the sensitivity coefficient from the two circuit points, compared
% with 2370.1 from Problem 1:
dM_dC_MD_circuit = (M250_Cplus - M250_Cminus)/(0.2*C_MD)
%%
% Mass and damping change M by less than 0.001 mV/Pa at 250 Hz. Only the
% spring matters, as the theory in Problem 1 said.

%% Problem 2d - What else do the changes do, and does Gpb matter?
% *Gpb at 250 Hz.* With Gpb on, the drive is T p_i instead of p_i. At 250 Hz:
T_at_250Hz = abs(T(k250))
%%
% That is 1.0007, so Gpb changes M by less than 0.1 % at 250 Hz. It acts only near and
% above ka = 1 (6.1 kHz).
%
% *Over the whole band* the changes do matter. Below resonance the
% microphone is stiffness controlled (C_MD sets the level). At and above
% resonance mass and damping take over: M_MD moves f_0, and R_MD sets
% the height of the peak. The three curves with +10 % (Gpb off):
e_Mplus = Elec_Gain./Y_E .* S_D./(jw*1.1*M_MD + R_MD + 1./(jw*C_MD) + S_D^2*(Z_ar + Z_B) - (E*C_MD/x_0)*Elec_Gain./(R_L*Y_E.*jw*C_MD));
e_Rplus = Elec_Gain./Y_E .* S_D./(jw*M_MD + 1.1*R_MD + 1./(jw*C_MD) + S_D^2*(Z_ar + Z_B) - (E*C_MD/x_0)*Elec_Gain./(R_L*Y_E.*jw*C_MD));
e_Cplus = Elec_Gain./Y_E .* S_D./(jw*M_MD + R_MD + 1./(jw*1.1*C_MD) + S_D^2*(Z_ar + Z_B) - (E*1.1*C_MD/x_0)*Elec_Gain./(R_L*Y_E.*jw*1.1*C_MD));
e_T = T.*e_nom;
figure;
semilogx(f, abs(e_nom)*1000, 'k', f, abs(e_Mplus)*1000, f, abs(e_Rplus)*1000, f, abs(e_Cplus)*1000, f, abs(e_T)*1000, '--', 'LineWidth', 1.3);
grid on; xlim([100 1e5]);
xlabel('Frequency [Hz]'); ylabel('M [mV/Pa]');
legend('nominal', 'M_{MD} +10 %', 'R_{MD} +10 %', 'C_{MD} +10 %', 'nominal with Gpb (approx. T x M)', 'Location', 'northwest');
title('2d: where each parameter acts');
%%
% (The dashed curve multiplies by T, which is what Gpb does for a still
% diaphragm. The exact circuit, P6_Q2_Sensitivity.asc runs 8-14, differs a
% little because the diaphragm moves; see P5_2d_FreeField.asc.)

%% Problem 3a - Pistonphone: the impedance analogy
% A heavy, rigid piston driven by a cam moves the same volume whatever it
% pushes against. So it is a *volume-velocity source* U_i (a current
% source). The closed cavity is a compliance $C_A = V/(\rho c^2)$ to
% ground, and the microphone's acoustic impedance Z_A sits in parallel with
% it:
%
%   U_i (current source) -> node p -> C_A to ground, and Z_A (microphone) to ground
%
% (Official solution, Problem 3a.)

%% Problem 3b - What an ideal pistonphone requires
% The pressure is the source current times the parallel impedance:
%
% $$p = \left(\frac{1}{j\omega C_A} \parallel Z_A\right) U_i$$
%
% For p not to depend on which microphone is inserted, the microphone must
% take almost none of the volume velocity:
%
% $$Z_A \gg \frac{1}{\omega C_A} \quad\Longrightarrow\quad C_A \gg \frac{1}{\omega Z_A}$$
%
% So a *large cavity volume* makes the pressure independent of the
% microphone. But the cavity must stay small compared with the wavelength,
% or it stops being a lumped compliance. And $C_A = V/(\gamma p_s)$
% contains the static pressure p_s, which is why a pistonphone comes with a
% barometer correction.
%
% *An example with our microphone* (the 10 cm^3 cavity is an illustration,
% it is not in the sheet). Below resonance the microphone is also a
% compliance, $C_{A,mic} = S_D^2 C_{MT}$. Two compliances in parallel add,
% so the microphone lowers the pressure by the factor
%
% $$\frac{p}{p_{no\,mic}} = \frac{C_A}{C_A + C_{A,mic}}$$
V_cavity = 10e-6       % illustration: a 10 cm^3 cavity [m^3]
C_A = V_cavity/(rho*c^2)
C_A_mic = S_D^2*C_MT
pressure_ratio_dB = 20*log10(C_A/(C_A + C_A_mic))
%%
% The microphone "looks like" a volume of $\rho c^2 C_{A,mic}$ (in cm^3):
mic_equivalent_volume_cm3 = rho*c^2*C_A_mic*1e6
%%
% So even a 10 cm^3 cavity is only disturbed by 0.03 dB. That is why the
% pistonphone is a reference device.

%% Problem 3c - The commercial calibrator, what is in it
% Going through the sketch (official solution 3c):
%
% * *Piezo bar + diaphragm:* a pressure source p_a with its own acoustic
% mass, resistance and compliance, M_as, R_as, C_as, in series.
% * *Volume V1 in front of the diaphragm*, where the microphone sits: a
% compliance C_a1 to ground, with the microphone Z_a in parallel.
% * *Volume V2 behind the diaphragm:* a compliance C_a2.
% * *The long narrow tube* from V2 to the far volume V3: an acoustic mass
% M_ah with a resistance R_ah.
% * *Volume V3:* a compliance C_a3.
% * The small leak around the diaphragm (from V1 to V2) is R_a4 + M_a4.

%% Problem 3d - The impedance analogy of the calibrator
% (Official solution, figure d.) Described element by element:
%
% * The source p in series with R_as, M_as, C_as runs from the V2 node to
% the V1 node (the diaphragm pumps air from the back into the front).
% * V1 node: C_a1 to ground, and the microphone Z_a to ground.
% * V2 node: C_a2 to ground, and the tube R_ah + M_ah in series with C_a3 to
% ground (the Helmholtz resonator made of the tube and V3).
% * The leak R_a4 + M_a4 in parallel with the source branch, V2 to V1.
%
% *Two resonances:*
%
% * the diaphragm on its suspension, M_as with C_as, and
% * the Helmholtz resonator, M_ah with C_a3.
%
% Both are tuned to the calibration frequency. At resonance a series L-C
% is almost a short, so the source impedance seen by the microphone becomes
% very small. That is the same requirement as in 3b (pressure independent of
% the microphone), reached here in a very small device.

%% Summary
% * $M = E S_D C_{MT}/x_0$ contains only C_MD, so $\partial M/\partial M_{MD} = \partial M/\partial R_{MD} = 0$.
% * $\partial M/\partial C_{MD} = 2370$ (V/Pa)/(m/N), and with u(C_MD) = 10 %
%   the combined standard uncertainty is u_c(M) = 0.948 mV/Pa (9.7 % of M).
% * In the circuit, M_250 = 9.83 mV/Pa and ±10 % C_MD moves it +0.946 / -0.952
%   mV/Pa. The official 9.6 and +0.922 / -0.929 come from the gain rounded to 1.1m.
% * Below resonance C_MD sets the level. At and above resonance M_MD and R_MD
%   shape the response. Gpb (T(s)) does nothing at 250 Hz.
% * The pistonphone is a volume-velocity source into a cavity compliance:
%   a large cavity (compared with the microphone) makes p independent of the
%   microphone.
% * The calibrator uses two tuned resonances (diaphragm and Helmholtz) to
%   get a very low source impedance.
