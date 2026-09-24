%% Lecture 4A - Transducers: problem solving, worked
% 34870 Electroacoustics | 10 September 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% official solution's answer (34870_Solutions4A) is written in the text so
% you can compare.
%
% The LTspice versions are in LTspice/Lecture 4A - Transducers/. Problem
% 4.4 is drawn there in BOTH analogies on one sheet, and the two agree.

%% The formulas used in this whole problem set
% *Mechanical <-> acoustic (a vibrating surface S).* The surface pushes air,
% and the air pushes back on the surface:
%
% $$U = S\,u \qquad f = S\,p$$
%
% u is the surface velocity [m/s], U the volume velocity [m^3/s], p the
% pressure difference between the two sides [Pa], f the force [N].
% Seen from the mechanics, an acoustic impedance is scaled by S^2:
%
% $$Z_M = S^2 Z_A$$
%
% *Electrical <-> mechanical (a voice coil in a magnet, Bl).* Lorentz force
% and induced voltage:
%
% $$f = Bl\,i \qquad v = Bl\,u$$
%
% Seen from the electrical terminals, the mechanical impedance is
% *inverted* (a gyrator):
%
% $$Z_{E,mot} = \frac{(Bl)^2}{Z_M}$$
%
% *Radiation impedance of a piston in a baffle* (lecture 3), one side:
%
% $$Z_{ar} = j\omega M_{A1}\;\Big\|\;\left[R_{A2} + \left(R_{A1}\,\Big\|\,\frac{1}{j\omega C_{A1}}\right)\right]$$
%
% $$M_{A1} = \frac{8\rho}{3\pi^2 a},\quad R_{A1} = \frac{0.441\rho c}{S},\quad R_{A2} = \frac{\rho c}{S},\quad C_{A1} = \frac{5.94\,a^3}{\rho c^2}$$
%
% At low frequency only M_A1 matters: the piston carries some air along.

%% Problem 4.1a+b - The bass-reflex box: the circuit
% The lecture-3 box (vent 12 cm long, 10 cm diameter, 23 L) now gets a
% loudspeaker: a massless piston in the baffle, as big as the vent, moving
% with velocity u.
%
% The official circuit, element by element:
%
% * Mechanical side (mobility analogy): a voltage source V1 = u, the
%   imposed velocity.
% * G1: a controlled current source U = S*u that pushes air from the back
%   node pb (inside the box) to the front node pf (outside).
% * G2: the reaction force f = S*p, p = pf - pb, drawn back from the
%   velocity node. It changes nothing here because u is imposed; it
%   matters as soon as the piston has a mass.
% * Front (pf to ground): the piston's radiation impedance Z_Ar.
% * Back (pb to ground): the box compliance C_A, in parallel with the vent
%   mass M_A followed by the vent's own outer radiation impedance Z_Ar.
%   Ground is both the far field and the box's reference, which is why box
%   and vent end up in parallel.
%
% The piston and the vent have the same diameter, so both Z_Ar are the
% same. LTspice: P4-1_BassReflex_Box.asc.
%
% Given (lecture 3's air):
rho = 1.18         % [kg/m^3]
c = 344            % [m/s]
a = 0.05           % piston and vent radius, diameter 10 cm [m]
l = 0.12           % vent length, 12 cm [m]
V = 0.023          % box, 23 L [m^3]
%%
% Area, vent mass $M_A = \rho l/S$ and box compliance $C_A = V/(\rho c^2)$:
S = pi*a^2
M_A = rho*l/S
C_A = V/(rho*c^2)
%%
% The radiation elements from the formulas at the top:
M_A1 = 8*rho/(3*pi^2*a)
R_A1 = 0.441*rho*c/S
R_A2 = rho*c/S
C_A1 = 5.94*a^3/(rho*c^2)

%% Problem 4.1c - Acoustic impedance seen by the piston
% The same U goes out through the front and in through the back, so front
% and back are in *series*:
%
% $$Z_A = \frac{p}{U} = \frac{p_f - p_b}{U} = Z_{Ar} + \left(\frac{1}{j\omega C_A}\;\Big\|\;\left(j\omega M_A + Z_{Ar}\right)\right)$$
f = logspace(1, log10(20000), 200000);   % 10 Hz ... 20 kHz, very fine (the peak is sharp)
jw = 1j*2*pi*f;
Z_Ar = 1./( 1./(jw*M_A1) + 1./(R_A2 + 1./(1/R_A1 + jw*C_A1)) );
Z_back = 1./( jw*C_A + 1./(jw*M_A + Z_Ar) );
Z_A = Z_Ar + Z_back;
%%
% The peak is the box-vent anti-resonance (C_A in parallel with the vent):
[Z_A_max, k] = max(abs(Z_A))
f_peak = f(k)
%%
% Official: Z_A,max = 995e3 Pa s/m^3 ("not 995 kOhm, watch units!").
% We get 1.09e6 at 79.4 Hz. The peak is extremely sharp (only the vent's
% radiation resistance damps it), so the value you read off depends on how
% close a sweep point lands on the top. The LTspice sheet with 2000 points
% per decade gives 1.085e6. Same order, same place.
%
% *Why 79 Hz and not the 92.4 Hz of lecture 3?* The vent's outer radiation
% mass M_A1 adds to the vent mass:
%
% $$f_B = \frac{1}{2\pi\sqrt{(M_A + M_{A1})\,C_A}}$$
f_B_lecture3 = 1/(2*pi*sqrt(M_A*C_A))
f_B_with_radiation = 1/(2*pi*sqrt((M_A + M_A1)*C_A))
%%
figure;
loglog(f, abs(Z_A), 'LineWidth', 1.5); grid on; xlim([10 20000]);
xlabel('Frequency [Hz]'); ylabel('|Z_A| [Pa s/m^3]');
title('Problem 4.1c: acoustic impedance seen by the piston');
%%
% Reading it: low down the vent short-circuits the box, so only the front
% radiation is left (small). At 79 Hz the box and vent anti-resonance gives
% the peak. Just above it the vent mass and the box cancel (a dip), then
% the box alone (falling as 1/f), until the front radiation resistance
% rho*c/S takes over at high frequency:
R_A2_plateau = R_A2

%% Problem 4.1d - Far field: pressure over distance
% Treat the whole box as a point source. A point source in free space with
% volume velocity U gives
%
% $$p(r,t) = \frac{j\omega\rho U}{4\pi r}\,e^{j(\omega t - kr)} = \frac{j f\rho S u}{2r}\,e^{j(\omega t - kr)}$$
%
% (using $\omega/4\pi = f/2$ and U = S*u). The magnitude falls as 1/r: half
% the pressure (-6 dB) for every doubling of distance. The official plot is
% for f = 1 kHz and u = 1 m/s.
f_1 = 1000         % [Hz]
u = 1              % [m/s]
r = linspace(0.1, 10, 500);
p = 1j*f_1*rho*S*u./(2*r).*exp(-1j*2*pi*f_1*r/c);
%%
% At 1 m:
p_1m = abs(1j*f_1*rho*S*u/(2*1))
figure;
plot(r, abs(p), 'LineWidth', 1.5); grid on;
xlabel('Distance r [m]'); ylabel('|p| [Pa]');
title('Problem 4.1d: pressure over distance, 1 kHz, u = 1 m/s');
%%
% Same curve as the official one (47 Pa at 10 cm, falling as 1/r). The
% official expression uses rho = 1.2 and c = 343, which changes the numbers
% by 1.7 %. At 1 kHz the vent adds almost nothing (its mass blocks), so
% U = S*u from the piston alone is enough.

%% Problem 4.2a - Force on a baffled piston: the circuit
% A force f acts on a piston of mass M_mp and area S in an infinite
% baffle. Official circuit (mobility on the mechanical side):
%
% * current source f0 into the velocity node u,
% * the piston mass M_mp: a capacitor from u to ground,
% * G2: the reaction force f = S*p drawn back out of node u,
% * G: the volume velocity U = S*u pushed into the acoustic side,
% * acoustic side: Z_ar for the front and Z_ar for the back, in series.
%
% The total acoustic load is therefore 2*Z_ar, and p is the pressure
% *difference* between the two sides, not the pressure on one side.

%% Problem 4.2b - Total mechanical impedance seen from the force
% Follow the hint: $p = 2Z_{ar}U = 2Z_{ar}S u$. The reaction force is then
%
% $$f = S p = 2S^2 Z_{ar}\,u$$
%
% which is the same as an impedance $f/u = 2S^2Z_{ar}$ in series with the
% piston mass. So
%
% $$Z_m = \frac{f_0}{u} = j\omega M_{mp} + 2S^2 Z_{ar}$$
%
% At low frequency $Z_{ar} \approx j\omega M_{A1}$ and the piston simply looks
% heavier by $2S^2M_{A1}$ (the air it carries on both sides).

%% Problem 4.2c - A baffle of thickness d
% The back of the piston now sits at the bottom of a short tube of length d
% and area S. While d is much smaller than the wavelength (rule of thumb:
% d < lambda/10) the air in it moves as one plug, an acoustic mass
%
% $$M_a = \frac{\rho\,d}{S}$$
%
% in series with the back radiation impedance. Use the *geometric* length d:
% the radiation impedance already contains the end correction.

%% Problem 4.2d - An enclosure of volume V on the back
% The back no longer radiates. The box compliance C_a = V/(rho*c^2), to
% ground, takes the place of the back Z_ar. Now the tube DOES need its end
% correction inside the box:
%
% $$M_a^* = M_a + M_{A1}$$
%
% So the back branch is M_a* in series with C_a to ground.

%% Problem 4.2e - The radiation impedance network
% Replace Z_ar by the lecture-3 network (formula at the top): M_A1 in
% parallel with [R_A2 in series with (R_A1 || C_A1)].

%% Problem 4.3a+b - Voice coil on a suspension: impedance analogy
% Coil: DC resistance R_E, inductance L_E, mass M_MC, force factor Bl, on a
% suspension with compliance C_MS and damping R_MS.
%
% Official circuit (impedance analogy): the electrical loop is R_E, L_E and
% a controlled voltage source Bl*u (the induced voltage). The mechanical
% loop is a controlled voltage source Bl*i (the force) driving M_MC (an
% inductor), C_MS (a capacitor) and R_MS (a resistor) in series; its loop
% current is the velocity u.
%
% From the terminals: $v = (R_E + j\omega L_E)i + Bl\,u$, and the mechanics
% gives $u = Bl\,i/Z_M$. Divide by i:
%
% $$Z_E = R_E + j\omega L_E + \frac{Bl\,u}{i} = R_E + j\omega L_E + \frac{(Bl)^2}{j\omega M_{MC} + R_{MS} + \dfrac{1}{j\omega C_{MS}}}$$
%
% The mechanical impedance appears *inverted* (the gyrator).

%% Problem 4.3c+d - Mobility analogy, and the comparison
% Official circuit (mobility): the electrical loop ends in a voltage source
% Bl*u controlled by the velocity node; on the mechanical side a current
% source f = Bl*i feeds the node u, with M_MC as a capacitor, 1/R_MS as a
% resistor and C_MS as an inductor, all to ground (in parallel).
%
% Calculating the mechanical admittance and inverting gives exactly the
% same Z_E as above. The two analogies describe the same physics.

%% Problem 4.3e - Velocity and forces versus the driving current
% The coil, the suspension spring and the damper all move with the same
% velocity:
%
% $$u = \frac{Bl}{j\omega M_{MC} + R_{MS} + \dfrac{1}{j\omega C_{MS}}}\,i$$
%
% and the Lorentz force is split between them, $f = f_{Mmc} + f_{Rms} + f_{Cms}$:
%
% $$f_{Mmc} = j\omega M_{MC}\,u = \frac{Bl}{1 + \dfrac{R_{MS}}{j\omega M_{MC}} - \dfrac{1}{\omega^2 M_{MC}C_{MS}}}\,i \qquad f_{Cms} = \frac{u}{j\omega C_{MS}} = \frac{Bl}{-\omega^2 M_{MC}C_{MS} + j\omega C_{MS}R_{MS} + 1}\,i$$
%
% * Below resonance the spring takes the whole force (f_Cms -> Bl*i).
% * Above resonance the mass takes it (f_Mmc -> Bl*i).
% * At resonance mass and spring cancel and the damper takes all of it,
%   u = Bl*i/R_MS.
% The numbers are plotted in 4.4b below.

%% Problem 4.4a - LTspice: Problem 4.2 with numbers, both analogies
% Values from the official .params:
rho = 1.2          % [kg/m^3]
c = 343            % [m/s]
S = 0.01           % piston area, 100 cm^2 [m^2]
M_mp = 0.02        % piston mass, 20 g [kg]
V = 0.04           % box, 40 L [m^3]
d = 0.02           % baffle thickness, 2 cm [m]
%%
% Equivalent radius, tube, box and radiation elements:
a = sqrt(S/pi)
M_a = rho*d/S
C_a = V/(rho*c^2)
M_A1 = 8*rho/(3*pi^2*a)
R_A1 = 0.441*rho*c/S
R_A2 = rho*c/S
C_A1 = 5.94*a^3/(rho*c^2)
%%
% The official circuit (4.2c, d and e all in): front radiation Z_ar, then
% the back tube with end correction M_a + M_A1, then the box C_a:
%
% $$Z_M = \frac{f}{u} = j\omega M_{mp} + S^2\left[Z_{ar} + j\omega(M_a + M_{A1}) + \frac{1}{j\omega C_a}\right]$$
%
% LTspice: P4-4a_Piston_Box.asc, impedance analogy on top (plot V(f)),
% mobility analogy below (plot 1/V(u_m)). The two curves coincide.
f = logspace(0, log10(20000), 200000);    % 1 Hz ... 20 kHz
jw = 1j*2*pi*f;
Z_ar = 1./( 1./(jw*M_A1) + 1./(R_A2 + 1./(1/R_A1 + jw*C_A1)) );
Z_M = jw*M_mp + S^2*(Z_ar + jw*(M_a + M_A1) + 1./(jw*C_a));
[Z_M_min, k] = min(abs(Z_M))
f_min = f(k)
Z_M_min_dB = 20*log10(Z_M_min)
%%
% Official: minimum at 20.4 Hz (marker at -40.5 dB). The frequency agrees.
% The depth does not: at the bottom only the tiny front radiation
% resistance is left (about 0.9 mN s/m, -61 dB). A dip this narrow is only
% as deep as the sweep point that lands nearest to it, so the official
% marker (-40.5 dB) sits on its flank. The physics is the same.
%
% *Check by hand:* at low frequency every air mass adds to the piston and
% the box is a spring C_a/S^2. The moving mass and resonance:
%
% $$M_{tot} = M_{mp} + S^2(M_{A1} + M_a + M_{A1}), \qquad f_0 = \frac{1}{2\pi\sqrt{M_{tot}\,C_a/S^2}}$$
M_tot = M_mp + S^2*(M_A1 + M_a + M_A1)
M_tot_gram = M_tot*1000
f_0 = 1/(2*pi*sqrt(M_tot*C_a/S^2))
%%
figure;
subplot(2,1,1);
semilogx(f, 20*log10(abs(Z_M)), 'LineWidth', 1.5); grid on; xlim([1 20000]);
ylabel('|Z_M| [dB re 1 Ns/m]'); title('Problem 4.4a: mechanical impedance f/u');
subplot(2,1,2);
semilogx(f, angle(Z_M)*180/pi, 'LineWidth', 1.5); grid on; xlim([1 20000]);
xlabel('Frequency [Hz]'); ylabel('Phase [deg]');
%%
% Below 20 Hz the box spring (-90 degrees), above it the mass line
% (+90 degrees), exactly like the official plot.

%% Problem 4.4b - LTspice: Problem 4.3 with numbers, both analogies
% Values:
l = 3              % coil wire length in the gap [m]
B = 0.7            % flux density [T]
M_MC = 10e-3       % coil mass, 10 g [kg]
C_MS = 1e-3        % suspension compliance, 1 mm/N [m/N]
R_MS = 2           % suspension damping [Ns/m]
R_E = 5            % coil resistance [ohm]
L_E = 0.3e-3       % coil inductance, 0.3 mH [H]
Bl = l*B
%%
% $$Z_E = R_E + j\omega L_E + \frac{(Bl)^2}{j\omega M_{MC} + R_{MS} + \dfrac{1}{j\omega C_{MS}}}$$
%
% LTspice: P4-4b_Voice_Coil.asc. It is driven by i = 1 A, so the input
% voltage V(v) (and V(v_m) for the mobility version) IS Z_E.
Z_M_coil = jw*M_MC + R_MS + 1./(jw*C_MS);
Z_E = R_E + jw*L_E + Bl^2./Z_M_coil;
%%
% The motional peak sits at the mechanical resonance, height
% $R_E + (Bl)^2/R_{MS}$:
f_0_coil = 1/(2*pi*sqrt(M_MC*C_MS))
Z_E_peak_hand = R_E + Bl^2/R_MS
%%
% From the curve (the coil inductance moves it a hair). Official: 51 Hz,
% 7.2 ohm
k = find(f < 1000);
[Z_E_peak, j] = max(abs(Z_E(k)))
f_peak = f(k(j))
%%
figure;
semilogx(f, abs(Z_E), 'LineWidth', 1.5); grid on; xlim([1 20000]);
xlabel('Frequency [Hz]'); ylabel('|Z_E| [\Omega]');
title('Problem 4.4b: electrical impedance of the coil on its suspension');
%%
% Flat at R_E = 5 ohm, a small motional bump at 50 Hz, then the coil
% inductance takes over above $R_E/(2\pi L_E)$:
f_L = R_E/(2*pi*L_E)
%%
% *Velocity and forces for i = 1 A (Problem 4.3e):*
%
% $$u = \frac{Bl\,i}{Z_M}, \qquad f_{Mmc} = j\omega M_{MC}u, \quad f_{Rms} = R_{MS}u, \quad f_{Cms} = \frac{u}{j\omega C_{MS}}$$
%
% In LTspice: I(Vu), and the voltage drops V(m1)-V(m2), V(m3), V(m2)-V(m3).
i = 1;
u = Bl*i./Z_M_coil;
f_Mmc = jw*M_MC.*u;
f_Rms = R_MS*u;
f_Cms = u./(jw*C_MS);
figure;
loglog(f, abs(f_Mmc), f, abs(f_Rms), f, abs(f_Cms), 'LineWidth', 1.5); grid on;
xlim([1 20000]); ylim([1e-3 5]);
yline(Bl*i, 'k--', 'Bl i');
xlabel('Frequency [Hz]'); ylabel('Force [N] for i = 1 A');
legend('coil mass', 'damper', 'suspension spring', 'Location', 'southwest');
title('Problem 4.4b: where the Lorentz force goes');
%%
% At resonance the damper takes the whole Bl*i, so the velocity there is
u_at_resonance = Bl*i/R_MS

%% Problem 4.4c - Coil glued to the piston
% Rigidly connected means the same velocity, so the mechanical impedances
% simply add (the masses add, the springs add):
%
% $$Z_E = R_E + j\omega L_E + \frac{(Bl)^2}{Z_{M,coil} + Z_{M,piston}}$$
%
% LTspice: P4-4c_Coil_on_Piston.asc (both analogies again).
Z_E_c = R_E + jw*L_E + Bl^2./(Z_M_coil + Z_M);
[Z_E_c_peak, j] = max(abs(Z_E_c(k)))
f_peak_c = f(k(j))
%%
% Official: 33.0 Hz, 7.2 ohm.
%
% *Check by hand:* the mass is now coil + piston + all the air; the springs
% add as stiffnesses, $1/C_{MS} + S^2/C_a$:
M_c = M_MC + M_tot
C_c = 1/(1/C_MS + S^2/C_a)
f_0_c = 1/(2*pi*sqrt(M_c*C_c))
%%
% The peak height stays at R_E + (Bl)^2/R_MS = 7.2 ohm, because at the
% resonance the damping is still (almost only) R_MS. The radiation
% resistance at 33 Hz is tiny.
figure;
semilogx(f, abs(Z_E), f, abs(Z_E_c), '--', 'LineWidth', 1.5); grid on;
xlim([1 20000]);
xlabel('Frequency [Hz]'); ylabel('|Z_E| [\Omega]');
legend('b) coil alone', 'c) coil on the piston + box', 'Location', 'northwest');
title('Problem 4.4c: the piston moves the motional peak down');

%% Summary
% * A vibrating surface couples mechanics and acoustics with S: U = S*u,
%   f = S*p. An acoustic impedance looks like S^2*Z_A from the mechanics.
% * A voice coil couples electrics and mechanics with Bl: f = Bl*i,
%   v = Bl*u. The mechanics looks INVERTED from the terminals, (Bl)^2/Z_M:
%   a mechanical resonance becomes an impedance peak.
% * Front and back of a piston carry the same U, so their acoustic loads
%   are in series; p is the pressure difference.
% * Bass-reflex box: the vent's radiation mass pulls the tuning from 92 Hz
%   to 79 Hz; far away the box is a point source, |p| ~ 1/r.
% * Piston + box: 20.4 Hz. Coil alone: 7.2 ohm at 50 Hz. Coil on the
%   piston: 7.2 ohm at 33 Hz.
% * Impedance and mobility analogies give identical results (checked in
%   LTspice to 1e-11).
