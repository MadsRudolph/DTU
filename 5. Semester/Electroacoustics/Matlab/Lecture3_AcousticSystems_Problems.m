%% Lecture 3 - Acoustic systems: problem solving, worked
% 34870 Electroacoustics | 7 September 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% official solution's answer is written in the text so you can compare.
%
% Numbering: the lecture slides call these Problems 2.1-2.4, the official
% solution sheet (34870_Solutions3.pdf) calls them 3.1-3.4. The solution
% sheet's numbers are used here.
%
% The LTspice versions are in LTspice/Lecture 3 - Acoustic Systems/.
%
% Air (from the sheet):
rho = 1.18     % air density [kg/m^3]
c = 344        % speed of sound [m/s]

%% The formulas used in this whole problem set
% We use the acoustic *impedance* analogy: pressure p is a voltage, volume
% velocity U (m^3/s) is a current. The acoustic impedance is
%
% $$Z_A = \frac{p}{U}$$
%
% *Open tube = acoustic mass (an inductor).* At low frequency the air in the
% tube moves as one plug. Pushing a mass of air rho*l*S with a force p*S gives
%
% $$M_A = \frac{\rho\,l}{S}$$
%
% *Closed volume = acoustic compliance (a capacitor to ground).* The air in a
% closed box is compressed like a spring. The pressure is measured against
% the outside, so the capacitor always goes to ground:
%
% $$C_A = \frac{V}{\rho c^2}$$
%
% *Resonance of a mass and a compliance in series:*
%
% $$f_0 = \frac{1}{2\pi\sqrt{M_A C_A}}$$
%
% Symbols: l tube length [m], S tube cross-section [m^2], V box volume [m^3].

%% Problem 3.1a - What do the tube and the box represent?
% An open tube connected to a closed box.
%
% * The *open tube* is an *acoustic mass* M_A, an inductor. The air in it
%   moves back and forth as one plug.
% * The *closed box* is an *acoustic compliance* C_A, a capacitor to
%   ground. Its air is squeezed like a spring.

%% Problem 3.1b - Which assumptions must hold for the lumped model?
% Official solution (with its own tick marks):
%
% * "?" the dimensions are much smaller than the wavelength (rule of thumb:
%   below lambda/10). This is the one to check every time, which is why it
%   gets a question mark.
% * OK: the element is homogeneous (the whole tube is one mass, the whole
%   box one spring).
% * OK: idealised rigid walls (the box walls do not move).

%% Problem 3.1c - The circuit, driven by a volume velocity U from outside
% The official circuit: a current source I1 = U, then the inductor L1 =
% M_tube in series, then the capacitor C1 = C_box to ground.
%
% The same volume velocity flows through the tube and into the box, so the
% two elements are in *series*. The capacitor ends on ground because the box
% pressure is measured against the outside air.

%% Problem 3.1d - Resonance frequency
% The impedance seen by the source is the sum of the two:
%
% $$Z_A = j\omega M_A + \frac{1}{j\omega C_A}$$
%
% At resonance the two reactances cancel, $Z_A = 0$:
%
% $$0 = j\omega_0 M_A + \frac{1}{j\omega_0 C_A} \quad\Longrightarrow\quad \omega_0 = \frac{1}{\sqrt{M_A C_A}}, \qquad f_0 = \frac{1}{2\pi\sqrt{M_A C_A}}$$
%
% Put in M_A = rho*l/S and C_A = V/(rho*c^2) and rho cancels. This is the
% Helmholtz resonator formula:
%
% $$f_0 = \frac{c}{2\pi}\sqrt{\frac{S}{l\,V}}$$

%% Problem 3.2b - Choose tube and box for f_0 = 100 Hz
% Any pair with M_A*C_A = 1/(2*pi*100)^2 works. Solving the resonance
% formula for C_A:
%
% $$C_A = \frac{1}{(2\pi f_0)^2\,M_A}$$
%
% The official solution picks M_A = 100 kg/m^4. Official: C_A = 2.53e-8 m^5/N
f_0 = 100          % wanted resonance [Hz]
M_A = 100          % chosen acoustic mass [kg/m^4]
C_A = 1/((2*pi*f_0)^2*M_A)
%%
% *What tube and box is that?* Pick a tube length of 5 cm and solve
% $M_A = \rho l/S$ for the cross-section, $S = \rho l / M_A$:
l = 0.05           % tube length, 5 cm [m]
S = rho*l/M_A
r_tube_cm = sqrt(S/pi)*100
%%
% and the box volume from $C_A = V/(\rho c^2)$, so $V = C_A\rho c^2$, in litres:
V = C_A*rho*c^2
V_litre = V*1000
%%
% So a tube 5 cm long with a radius of 1.4 cm on a 3.5 litre box
% (about 15 cm on each side).
%
% *Does it fulfil 3.1b?* The wavelength at 100 Hz is $\lambda = c/f$, and
% every dimension must be below about $\lambda/10$:
lambda = c/f_0
lambda_over_10 = lambda/10
box_side = V^(1/3)
%%
% Tube 0.05 m and box 0.15 m are both below 0.34 m, so the lumped model is
% fine.

%% Problem 3.2c - Plot the impedance and explain the curve
% The LTspice circuit is LTspice/Lecture 3 - Acoustic Systems/
% P3-2_Helmholtz_100Hz.asc (plot V(p_in); the source is 1 m^3/s, so the
% voltage IS the impedance). Here the same thing from the formula:
%
% $$Z_A = j\omega M_A + \frac{1}{j\omega C_A}$$
f = logspace(0, 4, 4000);      % 1 Hz ... 10 kHz
jw = 1j*2*pi*f;
Z_A = jw*M_A + 1./(jw*C_A);
figure;
subplot(2,1,1);
semilogx(f, 20*log10(abs(Z_A)), 'LineWidth', 1.5); grid on;
ylabel('|Z_A| [dB re 1 Pa s/m^3]'); title('Problem 3.2: tube in a box, tuned to 100 Hz');
subplot(2,1,2);
semilogx(f, angle(Z_A)*180/pi, 'LineWidth', 1.5); grid on;
xlabel('Frequency [Hz]'); ylabel('Phase [deg]');
%%
% *Reading the curve* (same as the official LTspice plot):
%
% * Low frequency: the box term 1/(omega*C_A) is huge. The box is a stiff
%   spring, the phase is -90 degrees, |Z_A| falls 20 dB per decade.
% * At 100 Hz the two terms cancel and |Z_A| drops to zero (no losses in
%   the model, so the dip is infinitely deep).
% * High frequency: the tube term omega*M_A wins, the air plug is too
%   heavy to move, the phase is +90 degrees and |Z_A| rises 20 dB per decade.

%% Problem 3.3a - Tube (12 cm, diameter 10 cm) in a 23 L box: the elements
% Given:
l = 0.12           % effective tube length, 12 cm [m]
r_1 = 0.05         % tube radius, diameter 10 cm [m]
V = 0.023          % box volume, 23 L [m^3]
%%
% Tube cross-section and acoustic mass, $M_{A1} = \rho l / (\pi r^2)$.
%
% Official: 18.03 kg/m^4
S_1 = pi*r_1^2
M_A1 = rho*l/S_1
%%
% Box compliance, $C_A = V/(\rho c^2)$. Official: 1.65e-7 m^5/N
C_A = V/(rho*c^2)
%%
% Circuit: the same as 3.1c. Source U, then M_A1 in series, then C_A to
% ground.

%% Problem 3.3b - Resonance frequency
% $$f_A = \frac{1}{2\pi\sqrt{M_{A1}C_A}}$$
%
% Official: 92.4 Hz
f_A = 1/(2*pi*sqrt(M_A1*C_A))

%% Problem 3.3c - A second, narrow tube (1 cm diameter) in the box
% Same length, radius 5 mm. The mass goes with 1/r^2, so it is 100 times
% heavier:
%
% $$M_{A2} = \frac{\rho l}{\pi r_2^2}$$
%
% Official: 1803 kg/m^4
r_2 = 0.005        % narrow tube radius, diameter 1 cm [m]
M_A2 = rho*l/(pi*r_2^2)
%%
% *The circuit:* the narrow tube connects the box to the outside air, where
% the pressure is (almost) zero. So M_A2 goes from the box node to ground,
% in parallel with C_A. (Adding its radiation impedance would be more
% exact; it is left out here, as in the official solution.)
%
% Source U -> M_A1 -> box node p_v -> (C_A to ground) and (M_A2 to ground).

%% Problem 3.3d - Pressure inside the box
% The box pressure is the voltage on the box node (across C_A). The source
% is a current source, so M_A1 in series with it does not change the
% current that reaches the box: all of U goes into C_A || M_A2.
%
% $$p_v = U\cdot\left(\frac{1}{j\omega C_A}\;\Big\|\;j\omega M_{A2}\right)$$
%
% A capacitor in parallel with an inductor has an *anti-resonance*: the
% impedance (and so the box pressure) becomes infinite at
%
% $$f_B = \frac{1}{2\pi\sqrt{M_{A2}C_A}}$$
%
% Official: 9.2 Hz
f_B = 1/(2*pi*sqrt(M_A2*C_A))
%%
% Shape: at DC all the air escapes through the narrow tube, so p_v = 0. It
% rises to the peak at 9.2 Hz, then falls as 1/f because the narrow tube's
% mass blocks and the box acts as a plain compliance again.
f = logspace(0, 3, 30000);     % 1 Hz ... 1 kHz, fine grid for the sharp peaks
jw = 1j*2*pi*f;
U = 1;                          % 1 m^3/s, as in the LTspice circuit
Z_box = 1./(jw*C_A + 1./(jw*M_A2));
p_v = U*Z_box;
figure;
semilogx(f, 20*log10(abs(p_v)), 'LineWidth', 1.5); grid on;
xlabel('Frequency [Hz]'); ylabel('|p_v| for U = 1 m^3/s [dB re 1 Pa]');
title('Problem 3.3d: pressure inside the box');

%% Problem 3.3e - Impedance seen from the opening of the large tube
% The source sees M_A1 in series with the box node:
%
% $$Z_{in} = j\omega M_{A1} + \left(\frac{1}{j\omega C_A}\Big\|\,j\omega M_{A2}\right)$$
%
% * a *peak* (anti-resonance) at f_B = 9.2 Hz, from C_A || M_A2,
% * a *dip* (resonance) where Z_in = 0. Setting the imaginary part to zero
%   gives
%
% $$f_{res} = \frac{1}{2\pi}\sqrt{\frac{M_{A1}+M_{A2}}{M_{A1}M_{A2}C_A}}$$
f_res = 1/(2*pi)*sqrt((M_A1 + M_A2)/(M_A1*M_A2*C_A))
%%
% 92.8 Hz, just above the 92.4 Hz of b): the narrow tube is 100 times
% heavier, so it barely changes anything near 92 Hz.
Z_in_wide = jw*M_A1 + Z_box;

%% Problem 3.3f - LTspice: plot the impedance, compare with b)
% LTspice/Lecture 3 - Acoustic Systems/P3-3_Tubes_in_Box.asc, top row
% (only M_A1 and C_A, as in the official circuit). Plot V(p_in_f).
% Because the source is a volume-velocity source, the pressure it has to
% produce to keep U = 1 m^3/s IS the impedance. The minimum is the
% resonance.
Z_in_f = jw*M_A1 + 1./(jw*C_A);
[~, k] = min(abs(Z_in_f));
f_dip = f(k)
%%
% Official: minimum at 92.4 Hz, matching b).
figure;
semilogx(f, 20*log10(abs(Z_in_f)), f, 20*log10(abs(Z_in_wide)), '--', 'LineWidth', 1.5);
grid on; xlim([1 1000]);
xlabel('Frequency [Hz]'); ylabel('|Z_{in}| [dB re 1 Pa s/m^3]');
legend('f) wide tube + box', 'e) with the narrow tube too', 'Location', 'north');
title('Problem 3.3e/f: impedance seen from the wide tube');

%% Problem 3.3g - Drive from the narrow tube instead
% Swap the two tubes: now M_A2 is in series with the source and M_A1 is the
% tube to the outside.
%
% $$Z_{in} = j\omega M_{A2} + \left(\frac{1}{j\omega C_A}\Big\|\,j\omega M_{A1}\right)$$
%
% * the *peak* now comes from C_A || M_A1, at the same frequency as b):
f_peak_g = 1/(2*pi*sqrt(M_A1*C_A))
%%
% * the *dip* (Z_in = 0) is the same symmetric formula as in e), so it
%   stays at 92.8 Hz.
%
% So peak and dip sit right next to each other (92.4 and 92.8 Hz). Official:
% "the (anti-)resonance frequencies become almost the same since then the
% impedance peak is now determined by Ma1||Cav and the minimum
% Ma2+Ma1||Cav is dominated by Ma1."
Z_in_narrow = jw*M_A2 + 1./(jw*C_A + 1./(jw*M_A1));
figure;
semilogx(f, 20*log10(abs(Z_in_narrow)), 'LineWidth', 1.5); grid on;
xlim([86 100]);
xlabel('Frequency [Hz]'); ylabel('|Z_{in}| [dB re 1 Pa s/m^3]');
title('Problem 3.3g: driven from the narrow tube (zoom 86-100 Hz)');

%% Problem 3.4 - Dynamic microphone: the equivalent network
% The diaphragm makes the volume velocity U (a current source). Behind it
% is the small volume V1, a canal with porous material, and the larger
% volume V2. The official circuit, element by element:
%
% * U: current source (the diaphragm pumping air).
% * C_AV1: the small volume V1, a capacitor from the first node to ground.
% * R_A1 and M_A1 in series: the canal. The porous material is a
%   resistance, the air plug in the canal is a mass. Both carry the same
%   volume velocity, so they are in series.
% * C_AV2: the large volume V2, a capacitor to ground at the end.
%
% No numbers are given, so there is nothing to calculate. Note what it
% does: at high frequency C_AV1 short-circuits U to ground before the flow
% reaches V2, a low-pass. This circuit comes back in the dynamic microphone
% of Lecture 4B.

%% Summary
% * Open tube = acoustic mass M_A = rho*l/S (inductor). Closed volume =
%   compliance C_A = V/(rho*c^2) (capacitor, always to ground).
% * Tube + box in series is a Helmholtz resonator, f_0 = 1/(2*pi*sqrt(M_A*C_A)).
% * Valid only while every dimension is below about lambda/10.
% * A tube that opens to the outside goes to ground (outside pressure ~ 0).
% * Driven by a volume velocity, a series M-C gives an impedance dip
%   (resonance), a parallel M || C gives a peak (anti-resonance).
% * Tube + box: 18.03 kg/m^4, 1.65e-7 m^5/N, 92.4 Hz; with the narrow tube
%   the box pressure peaks at 9.2 Hz.
