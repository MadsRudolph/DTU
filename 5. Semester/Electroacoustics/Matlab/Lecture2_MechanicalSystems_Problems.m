%% Lecture 2 - Analogies for mechanical systems: problems 2.1 to 2.4 and bonus problems 5, 6
% 34870 Electroacoustics | 3 September 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% official solution's answer is written in the text so you can compare.
%
% The LTspice versions are in LTspice/Lecture 2 - Mechanical Systems/
% (P2_1_Graphical_Conversion.asc, P2_2_Mass_Spring.asc,
% P2_3_Equivalent_Sources.asc, P2_4_Two_Mass.asc).

%% The formulas used in this whole problem set
% Mechanical network variables: force f [N] and velocity u [m/s]. Three
% elements, each with an impedance Z_M = f/u:
%
% $$Z_{damper} = R_M, \qquad Z_{mass} = j\omega M_M, \qquad Z_{spring} = \frac{1}{j\omega C_M}, \quad C_M = \frac{1}{k}$$
%
% The mobility is the inverse, $Y_M = u/f = 1/Z_M$.
%
% *Two ways to draw it:*
%
% * Impedance analogy: force = voltage, velocity = current. Mass = inductor,
%   compliance = capacitor, damper = resistor R_M. Elements that share one
%   velocity are in SERIES.
% * Mobility analogy: velocity = voltage, force = current. Mass = capacitor
%   (to ground: a mass always moves relative to the fixed reference),
%   compliance = inductor, damper = resistor 1/R_M. Elements that share one
%   velocity are in PARALLEL.
%
% The two circuits are each other's duals (lecture 1): series <-> parallel,
% voltage source <-> current source.

%% Problem 2.1a - Convert the impedance circuit to the mobility circuit
% *The sheet's circuit (impedance analogy)*, from left to right: a velocity
% source u1 (a current source) with C_M1 across it; then M_M1 and R_M1 in
% series along the top; R_M2 from that node to ground; M_M2 in series; C_M3
% to ground; then M_M3 and R_M3 in series to ground at the end.
%
% *Rule:* every series element becomes a parallel (shunt) element and the
% other way round, mass L becomes C, compliance C becomes L, R becomes 1/R,
% and the current source becomes a voltage source. The dual, from left to
% right (the official solution's second LTspice circuit):
%
% * voltage source u1 (a velocity source), then C_M1 as an inductor in series
%   (the shunt capacitor became a series inductor),
% * node u_M1: M_M1 as a capacitor to ground and R_M1 as 1/R_M1 to ground
%   (the series pair became a parallel pair),
% * 1/R_M2 in series (the shunt resistor became a series resistor),
% * node u_M2: M_M2 as a capacitor to ground,
% * C_M3 as an inductor in series,
% * node u_M3: M_M3 as a capacitor and 1/R_M3 to ground.
%
% Every node voltage in the mobility circuit is the velocity of one mass,
% and every current is a force. That is the practical advantage: you can read
% the velocities straight off the nodes.

%% Problem 2.1b - The mechanical sketch
% Read the impedance circuit as "what shares a velocity" (the official
% solution's sketch): the source u1 pushes one end of spring C_M1. The other
% end of C_M1 moves the mass M_M1. M_M1 is held to the ground (wall) by the
% damper R_M1. From M_M1 a damper R_M2 connects to the mass M_M2, from M_M2
% a spring C_M3 to the mass M_M3, and M_M3 is held to the wall by the damper
% R_M3. Every mass is also "virtually" connected to ground, because its
% velocity is always measured against the fixed reference.

%% Problem 2.1 - Check the conversion with numbers
% The official LTspice files use these values (C_M2 is defined but not used
% anywhere in the circuit):
u1 = 2          % source velocity [m/s]
R_M1 = 1        % [kg/s]
R_M2 = 2        % [kg/s]
R_M3 = 3        % [kg/s]
M_M1 = 10e-3    % 10 g [kg]
M_M2 = 2.5*M_M1 % 25 g [kg]
M_M3 = 4*M_M1   % 40 g [kg]
C_M1 = 1e-3     % 1 mm/N [m/N]
C_M3 = 0.3*C_M1 % 0.3 mm/N [m/N]
f = logspace(0, 4, 2000);
jw = 1j*2*pi*f;
%%
% *Impedance circuit*, from the far end towards the source. Series
% impedances add, parallel ones combine as $1/(1/Z_a + 1/Z_b)$:
%
% $$Z_4 = j\omega M_{M3} + R_{M3}, \quad Z_3 = \frac{1}{j\omega C_{M3} + 1/Z_4}, \quad Z_b = j\omega M_{M2} + Z_3, \quad Z_2 = \frac{1}{1/R_{M2} + 1/Z_b}, \quad Z_a = j\omega M_{M1} + R_{M1} + Z_2$$
Z_4 = jw*M_M3 + R_M3;
Z_3 = 1./(jw*C_M3 + 1./Z_4);
Z_b = jw*M_M2 + Z_3;
Z_2 = 1./(1/R_M2 + 1./Z_b);
Z_a = jw*M_M1 + R_M1 + Z_2;
%%
% The source current u1 splits between C_M1 and the rest (current divider),
% which gives the velocity of M_M1; then each velocity follows from the force
% on the next branch:
%
% $$u_{M1} = u_1\frac{1/Z_a}{j\omega C_{M1} + 1/Z_a}, \quad u_{M2} = u_{M1}\frac{Z_2}{Z_b}, \quad u_{M3} = u_{M2}\frac{Z_3}{Z_4}$$
u_M1_imp = u1*(1./Z_a)./(jw*C_M1 + 1./Z_a);
u_M2_imp = u_M1_imp.*Z_2./Z_b;
u_M3_imp = u_M2_imp.*Z_3./Z_4;
%%
% *Mobility circuit*, the same way but with mobilities (now series
% mobilities add and parallel ones combine):
%
% $$Y_4 = \frac{1}{j\omega M_{M3} + R_{M3}}, \quad Y_3 = j\omega C_{M3} + Y_4, \quad Y_b = \frac{1}{j\omega M_{M2} + 1/Y_3}, \quad Y_2 = \frac{1}{R_{M2}} + Y_b, \quad Y_a = \frac{1}{j\omega M_{M1} + R_{M1} + 1/Y_2}$$
Y_4 = 1./(jw*M_M3 + R_M3);
Y_3 = jw*C_M3 + Y_4;
Y_b = 1./(jw*M_M2 + 1./Y_3);
Y_2 = 1/R_M2 + Y_b;
Y_a = 1./(jw*M_M1 + R_M1 + 1./Y_2);
%%
% The voltage source u1 sees C_M1 (series) and then Ya: a voltage divider.
% Then each node velocity follows:
%
% $$u_{M1} = u_1\frac{Y_a}{j\omega C_{M1} + Y_a}, \quad u_{M2} = u_{M1}\frac{Y_b}{Y_2}, \quad u_{M3} = u_{M2}\frac{Y_4}{Y_3}$$
u_M1_mob = u1*Y_a./(jw*C_M1 + Y_a);
u_M2_mob = u_M1_mob.*Y_b./Y_2;
u_M3_mob = u_M2_mob.*Y_4./Y_3;
%%
% The two circuits give the same velocities (largest relative difference,
% should be at rounding level):
max_difference = max(abs([u_M1_mob./u_M1_imp - 1, u_M2_mob./u_M2_imp - 1, u_M3_mob./u_M3_imp - 1]))
figure;
loglog(f, abs(u_M1_imp), f, abs(u_M2_imp), f, abs(u_M3_imp), 'LineWidth', 1.5);
hold on;
loglog(f(1:50:end), abs(u_M1_mob(1:50:end)), 'ko', f(1:50:end), abs(u_M2_mob(1:50:end)), 'ks', ...
       f(1:50:end), abs(u_M3_mob(1:50:end)), 'kd');
hold off; grid on; xlim([1 1e4]);
xlabel('Frequency [Hz]'); ylabel('|u| [m/s]');
legend('u_{M1}', 'u_{M2}', 'u_{M3}', 'mobility circuit (markers)', 'Location', 'southwest');
title('Problem 2.1: impedance (lines) and mobility (markers) circuit');

%% Problem 2.2a - Mass on a spring: the model
% Given (typical low-frequency loudspeaker values):
M_M = 20e-3      % 20 g [kg]
k = 1000         % spring stiffness [N/m]
R_M = 0.5        % damping [Ns/m]
%%
% The compliance is the inverse stiffness, $C_M = 1/k$, i.e. 1 mm/N:
C_M = 1/k
%%
% Mass, spring and damper all move with the same velocity u, so in the
% impedance analogy they are in series:
%
% $$Z_M = R_M + j\omega M_M + \frac{1}{j\omega C_M}$$
%
% *Resonance* where the mass and spring parts cancel:
%
% $$0 = j\omega_0 M_M + \frac{1}{j\omega_0 C_M} \;\Longrightarrow\; \omega_0 = \frac{1}{\sqrt{M_M C_M}}$$
%
% Official solution: 223.6 rad/s, 35.6 Hz
omega_0 = 1/sqrt(M_M*C_M)
f_0 = omega_0/(2*pi)
%%
% Quality factor and -3 dB bandwidth:
%
% $$Q = \frac{1}{R_M}\sqrt{\frac{M_M}{C_M}}, \qquad BW = \frac{f_0}{Q} = \frac{R_M}{2\pi M_M}$$
Q = 1/R_M*sqrt(M_M/C_M)
BW = R_M/(2*pi*M_M)

%% Problem 2.2b - Driven by a 10 N force: the velocity
% A force source pushes on Z_M, so
%
% $$u = \frac{F}{Z_M}$$
F = 10;
f = logspace(0, 3, 3000);
jw = 1j*2*pi*f;
Z_M = R_M + jw*M_M + 1./(jw*C_M);
u = F./Z_M;
%%
% *At resonance* only R_M is left, so $u(\omega_0) = F/R_M$. In dB re 1 m/s.
% Official plot: 20 m/s, 26 dB
u_at_f0 = F/R_M
u_at_f0_dB = 20*log10(u_at_f0)
%%
% *Below resonance* the spring dominates: $u \approx j\omega C_M F$, rising
% 20 dB per decade. At 1 Hz (official plot: about -24 dB):
u_1Hz_dB = 20*log10(2*pi*1*C_M*F)
%%
% *Above resonance* the mass dominates: $u \approx F/(j\omega M_M)$, falling
% 20 dB per decade. At 1 kHz:
u_1kHz_dB = 20*log10(F/(2*pi*1000*M_M))
%%
figure;
subplot(2,1,1);
semilogx(f, 20*log10(abs(u)), 'LineWidth', 1.5);
grid on; xlim([1 1000]); ylim([-30 50]);
ylabel('|u| [dB re 1 m/s]');
title('Problem 2.2b: velocity for a 10 N force');
subplot(2,1,2);
semilogx(f, angle(u)*180/pi, 'LineWidth', 1.5);
grid on; xlim([1 1000]); ylim([-90 90]);
xlabel('Frequency [Hz]'); ylabel('Phase [deg]');
%%
% So: spring controlled below 35.6 Hz (+20 dB/decade, phase +90 degrees),
% a sharp peak of 20 m/s at 35.6 Hz with Q = 8.9 (bandwidth 4 Hz), mass
% controlled above (-20 dB/decade, phase -90 degrees).

%% Problem 2.2c - Driven by a 1 m/s velocity: the force
% Now the source fixes u and the force is what the system pushes back with:
%
% $$f = Z_M\,u$$
u_src = 1;
f_force = Z_M*u_src;
%%
% At resonance the force has its MINIMUM, $f(\omega_0) = R_M u$
% (official plot: -6 dB). At 1 Hz the spring needs a large force,
% $1/(\omega C_M)$ (official plot: about 44 dB):
f_at_f0 = R_M*u_src
f_at_f0_dB = 20*log10(f_at_f0)
f_1Hz_dB = 20*log10(u_src/(2*pi*1*C_M))
%%
figure;
semilogx(f, 20*log10(abs(u)), f, 20*log10(abs(f_force)), 'LineWidth', 1.5);
grid on; xlim([1 1000]); ylim([-30 50]);
xlabel('Frequency [Hz]'); ylabel('[dB]');
legend('velocity for 10 N [dB re 1 m/s]', 'force for 1 m/s [dB re 1 N]', 'Location', 'north');
title('Problem 2.2: force drive vs velocity drive');
%%
% *Why it looks different:* with a force source we plot u = F/Z_M (the
% mobility), with a velocity source f = Z_M u (the impedance). One is the
% inverse of the other, so the velocity peak becomes a force dip. At
% resonance the mass and spring cancel and the system is easiest to move:
% a given force gives the most velocity, and a given velocity needs the
% least force. The two curves are mirror images around the level at
% resonance.

%% Problem 2.3a - The driver as a source: impedance and admittance
% Same driver as 2.2, now pushed by a Lorentz force of 10 N.
%
% $$Z_M = R_M + j\left(\omega M_M - \frac{1}{\omega C_M}\right) = 0.5\,\tfrac{kg}{s} + j\left(\omega\cdot 20\,g - \frac{1}{\omega}\cdot 10^3\,\tfrac{kg}{s^2}\right)$$
%
% $$Y_M = \frac{1}{Z_M} = \frac{1}{R_M} \,\Big\|\, j\omega C_M \,\Big\|\, \frac{1}{j\omega M_M}$$
%
% (the "||" is the parallel rule for the dual: the three mobilities are in
% parallel in the mobility circuit). At resonance the imaginary part is zero:
%
% Official solution: Z_M(w0) = 0.5 kg/s, Y_M(w0) = 2 s/kg
Z_M_at_f0 = R_M
Y_M_at_f0 = 1/R_M

%% Problem 2.3b - Norton and Thevenin force sources
% A real source is an ideal source plus its own internal impedance. Here
% the internal impedance is the driver's own Z_M.
%
% * Impedance analogy, *Thevenin*: the force f_Th = 10 N (a voltage source)
%   in series with Z_M.
% * Mobility analogy, *Norton*: the force f_No = 10 N (a current source) in
%   parallel with Y_M.
%
% Both describe the same thing: the Lorentz force acts on the moving mass,
% and part of it is used up in moving the mass, spring and damper
% themselves.

%% Problem 2.3c - Convert to a velocity source
% Source conversion (Thevenin <-> Norton):
%
% $$\text{impedance analogy: } u_{No} = \frac{f_{Th}}{Z_M}, \qquad \text{mobility analogy: } u_{Th} = Y_M\,f_{No}$$
%
% So the equivalent velocity source is a velocity source u_No in parallel
% with Z_M (impedance analogy), or u_Th in series with Y_M (mobility
% analogy). It depends on frequency, because Z_M does. At resonance:
%
% $$u(\omega_0) = f\cdot Y_M(\omega_0) = 10\,N \cdot 2\,\tfrac{s}{kg}$$
%
% Official solution: 20 m/s
F = 10
u_eq_at_f0 = F*Y_M_at_f0
%%
% Over frequency (linear axis, like the official plot):
u_eq = F./Z_M;
figure;
semilogx(f, abs(u_eq), 'LineWidth', 1.5);
grid on; xlim([1 1000]);
xlabel('Frequency [Hz]'); ylabel('|u_{No}| = |u_{Th}| [m/s]');
title('Problem 2.3: equivalent velocity source of the driver (10 N)');
%%
% The LTspice file draws all four versions (Thevenin and Norton in both
% analogies, the frequency-dependent sources as Laplace sources) with a
% load, and all four give the same load velocity.

%% Problem 2.4 - Two masses: the equivalent circuit
% A force f pushes M1. M1 is coupled to M2 by a spring C1 and a damper R1
% side by side.
%
% *Reading the sketch:* the spring and the damper both see the relative
% velocity u1 - u2 (they are mechanically in parallel), so in the
% impedance analogy they are in SERIES: $Z_c = R_1 + 1/(j\omega C_1)$. M2
% only moves with u2 and carries the force that went through the coupling.
%
% *Impedance circuit* (official solution): force source, M1 as an inductor
% in series (it carries u1), then the node splits into the branch R1 + C1
% (carrying u1 - u2) and the inductor M2 (carrying u2), both to ground.
%
% *Mobility circuit*: force = current source into node u1, M1 as a
% capacitor from u1 to ground, C1 (inductor) parallel with 1/R1 between
% node u1 and node u2, M2 as a capacitor from u2 to ground.
%
% Given (official .param line):
F = 1           % force [N]
R_1 = 0.3       % Rm1 [kg/s]
M_1 = 1e-3      % Mm1, 1 g [kg]
M_2 = 2e-3      % Mm2, 2 g [kg]
C_1 = 10e-3     % Cm1, 10 mm/N [m/N]
f = logspace(0, 4, 4000);
jw = 1j*2*pi*f;
%%
% *The formulas.* Input impedance: M1 in series with (coupling || M2):
%
% $$Z_c = R_1 + \frac{1}{j\omega C_1}, \qquad Z_{in} = j\omega M_1 + \frac{1}{1/Z_c + 1/(j\omega M_2)}$$
%
% then the velocities (the u1 current splits between Z_c and M2):
%
% $$u_1 = \frac{F}{Z_{in}}, \qquad u_2 = u_1\,\frac{Z_c}{Z_c + j\omega M_2}$$
Z_c = R_1 + 1./(jw*C_1);
Z_in = jw*M_1 + 1./(1./Z_c + 1./(jw*M_2));
u_1 = F./Z_in;
u_2 = u_1.*Z_c./(Z_c + jw*M_2);
%%
% *What to expect.* At low frequency the coupling is stiff and both masses
% move together: $u = F/(j\omega(M_1+M_2))$. At 1 Hz (official plot: about
% 34 dB):
u_1Hz_dB = 20*log10(F/(2*pi*1*(M_1+M_2)))
%%
% *u1 has a dip* where M2 on the spring C1 resonates by itself. In the
% circuit the parallel pair (C1 branch || M2) is an anti-resonance there, so
% its impedance is HIGH (without R1 it would be infinite and u1 would be
% zero: M2 swings and holds M1 still). With R1 = 0.3 kg/s the dip is only
% a few dB deep (0.5 dB vs 3.5 dB on the M1 + M2 mass line). Frequency:
%
% $$f_{dip} = \frac{1}{2\pi\sqrt{M_2 C_1}}$$
f_dip = 1/(2*pi*sqrt(M_2*C_1))
%%
% *Both masses resonate* against each other on the spring with the reduced
% mass $M_r = M_1 M_2/(M_1+M_2)$:
%
% $$f_r = \frac{1}{2\pi\sqrt{M_r C_1}}, \qquad Q = \frac{1}{R_1}\sqrt{\frac{M_r}{C_1}}$$
M_r = M_1*M_2/(M_1+M_2)
f_r = 1/(2*pi*sqrt(M_r*C_1))
Q_r = 1/R_1*sqrt(M_r/C_1)
%%
% Q is below 1, so this resonance is heavily damped and the u1 bump lands
% higher than f_r. Where u1 actually peaks between 40 and 200 Hz:
k_range = find(f > 40 & f < 200);
[u1_peak, k] = max(abs(u_1(k_range)));
f_u1_peak = f(k_range(k))
%%
% Above that, u1 falls as the mass line of M1 alone, $F/(j\omega M_1)$, and u2
% falls 40 dB/decade faster (it is decoupled through the spring).
figure;
subplot(2,1,1);
semilogx(f, 20*log10(abs(u_1)), f, 20*log10(abs(u_2)), 'LineWidth', 1.5);
grid on; xlim([1 1e4]); ylim([-90 40]);
ylabel('|u| [dB re 1 m/s]'); legend('u_1', 'u_2');
title('Problem 2.4: two-mass system, 1 N');
subplot(2,1,2);
semilogx(f, angle(u_1)*180/pi, f, angle(u_2)*180/pi, 'LineWidth', 1.5);
grid on; xlim([1 1e4]);
xlabel('Frequency [Hz]'); ylabel('Phase [deg]');

%% Problem 2.4 - The limiting cases
% Each case changes one element to an extreme value and recomputes u1, u2
% with the same formulas as above. "Infinite" is 1e6 and "zero" 1e-9 or
% less, far enough to show the limit.
%
% *M1 -> infinity:* M1 is too heavy to move. Official: u1 = 0, u2 = 0.
M_1_big = 1e6;
Z_in_a = jw*M_1_big + 1./(1./Z_c + 1./(jw*M_2));
u_1a = F./Z_in_a;
u_2a = u_1a.*Z_c./(Z_c + jw*M_2);
%%
% *M2 -> infinity:* M2 becomes a wall, so M1 sits on a spring + damper
% fixed to ground: a single resonator at $1/(2\pi\sqrt{M_1 C_1})$ = 50 Hz.
% Official: u1 below the reference at low frequency, u2 = 0.
M_2_big = 1e6;
Z_in_b = jw*M_1 + 1./(1./Z_c + 1./(jw*M_2_big));
u_1b = F./Z_in_b;
u_2b = u_1b.*Z_c./(Z_c + jw*M_2_big);
f_M1_on_C1 = 1/(2*pi*sqrt(M_1*C_1))
%%
% *C1 -> 0:* an infinitely stiff spring locks the two masses together.
% Official: u1 = u2 (one mass M1 + M2).
Z_c_c = R_1 + 1./(jw*1e-12);
Z_in_c = jw*M_1 + 1./(1./Z_c_c + 1./(jw*M_2));
u_1c = F./Z_in_c;
u_2c = u_1c.*Z_c_c./(Z_c_c + jw*M_2);
%%
% *R1 -> infinity:* an infinitely stiff damper locks them too. Official:
% u1 = u2.
Z_c_d = 1e9 + 1./(jw*C_1);
Z_in_d = jw*M_1 + 1./(1./Z_c_d + 1./(jw*M_2));
u_1d = F./Z_in_d;
u_2d = u_1d.*Z_c_d./(Z_c_d + jw*M_2);
%%
% *R1 -> 0 and C1 -> infinity:* no damper and an infinitely soft spring: no
% coupling at all. M1 moves freely, $u_1 = F/(j\omega M_1)$, which is MORE
% than the reference at low frequency (only one mass to push), and nothing
% reaches M2. Official: u1 >= u1ref, u2 = 0.
Z_c_e = 1e-9 + 1./(jw*1e6);
Z_in_e = jw*M_1 + 1./(1./Z_c_e + 1./(jw*M_2));
u_1e = F./Z_in_e;
u_2e = u_1e.*Z_c_e./(Z_c_e + jw*M_2);
%%
figure;
semilogx(f, 20*log10(abs(u_1)), 'k', 'LineWidth', 2); hold on;
semilogx(f, 20*log10(abs(u_1b)), f, 20*log10(abs(u_1c)), '--', ...
         f, 20*log10(abs(u_1e)), 'LineWidth', 1.3); hold off;
grid on; xlim([1 1e4]); ylim([-60 40]);
xlabel('Frequency [Hz]'); ylabel('|u_1| [dB re 1 m/s]');
legend('reference', 'M_2 \rightarrow \infty', 'C_1 \rightarrow 0 (same as R_1 \rightarrow \infty)', ...
       'R_1 \rightarrow 0 & C_1 \rightarrow \infty', 'Location', 'southwest');
title('Problem 2.4: u_1 in the limiting cases (M_1 \rightarrow \infty gives u_1 = 0)');
%%
% Numbers at 10 Hz in dB re 1 m/s, reference first (u1 then u2 for each
% case). The very negative numbers are "zero".
k10 = find(f >= 10, 1);
reference_u1_u2 = 20*log10(abs([u_1(k10), u_2(k10)]))
M1_inf_u1_u2 = 20*log10(abs([u_1a(k10), u_2a(k10)]))
M2_inf_u1_u2 = 20*log10(abs([u_1b(k10), u_2b(k10)]))
C1_zero_u1_u2 = 20*log10(abs([u_1c(k10), u_2c(k10)]))
R1_inf_u1_u2 = 20*log10(abs([u_1d(k10), u_2d(k10)]))
no_coupling_u1_u2 = 20*log10(abs([u_1e(k10), u_2e(k10)]))
%%
% This reproduces the official table:
%
% * M1 -> inf: u1 = 0, u2 = 0
% * M2 -> inf: u1 < u1ref at low f (M1 now hangs on a spring), u2 = 0
% * C1 -> 0: u1 = u2
% * R1 -> inf: u1 = u2
% * R1 -> 0 and C1 -> inf: u1 >= u1ref, u2 = 0
%
% In the circuit picture: M1 -> inf is an open circuit (infinite L) in the
% source path, M2 -> inf opens the M2 branch, C1 -> 0 or R1 -> inf opens the
% coupling branch so all of u1 flows through M2, and R1 -> 0 with C1 -> inf
% shorts the coupling branch so nothing flows through M2.

%% Bonus problem 5a - Refrigerator on four elastic feet
% *The system:* the compressor pushes with a force F on the rigid body M_mb.
% The body stands on four feet, each a spring C_mf with a damper R_mf, on a
% rigid floor.
%
% *Mechanical sketch:* one mass on one spring and one damper to the floor.
% Four springs in parallel (they all compress by the same amount) are one
% spring with compliance C_mf/4 (four times stiffer). Four dampers in
% parallel are one damper 4 R_mf. The mass is connected "virtually" to
% ground, because its velocity is measured against the floor.
%
% *Impedance analogy:* everything moves with the one velocity u of the body,
% so the force source drives M_mb, C_mf/4 and 4 R_mf in SERIES:
%
% $$Z = j\omega M_{mb} + \frac{4}{j\omega C_{mf}} + 4R_{mf}$$
%
% *Mobility analogy:* the dual, a current source (the force) feeding three
% elements in PARALLEL: a capacitor M_mb, an inductor C_mf/4 and a resistor
% 1/(4 R_mf), all to ground. The node voltage is the body velocity.

%% Bonus problem 5b - Compressor on its own suspension
% Now the compressor (mass M_mc) sits on a suspension C_ms with damping
% R_ms inside the body, and the force acts on the compressor mass.
%
% *Physics:* the force F moves the compressor mass. The suspension C_ms ||
% R_ms carries the force from the compressor to the body, and the body sits
% on the feet as in 5a.
%
% *Impedance analogy* (official solution): force source, then M_mc in series
% (it carries the compressor velocity u), then a node that splits into two
% branches to ground: C_ms + R_ms in series (the suspension, it carries
% u - u_m), and M_mb + C_mf/4 + 4 R_mf in series (the body on its feet, it
% carries u_m). So the suspension and damper, mechanically in series with
% the circuit from a), appear in PARALLEL with it; the compressor mass,
% mechanically in parallel with the rest, appears in SERIES.
%
% $$Z_{in} = j\omega M_{mc} + \left(R_{ms} + \frac{1}{j\omega C_{ms}}\right) \Big\| \left(j\omega M_{mb} + \frac{4}{j\omega C_{mf}} + 4R_{mf}\right)$$
%
% *Mobility analogy:* current source F into node u with M_mc as a capacitor
% to ground; C_ms (inductor) in parallel with 1/R_ms between node u and
% node u_m; at node u_m the body circuit of 5a: M_mb capacitor, C_mf/4
% inductor and 1/(4 R_mf) to ground.
%
% This is exactly the two-mass system of problem 2.4 with the second mass
% standing on the feet. Above the resonance of the compressor suspension,
% the force reaching the body drops, and so does the noise: the suspension
% works as a vibration isolator.

%% Bonus problem 6a - Car suspension, one wheel
% The same system as 5a (a mass on a spring and a damper) but the SOURCE is
% different: the wheel follows the road, so the road imposes a velocity u
% on the bottom of the suspension. Wheel and suspension masses are ignored
% and the car mass per wheel is M_mc/4.
%
% *Impedance analogy:* the source velocity (a current source) is shared
% between moving the car body and compressing the suspension, so the two are
% two PARALLEL branches: one branch is R_s + C_s in series, the other is the
% inductor M_mc/4. The car velocity is the current in the M_mc/4 branch.
%
% *Mobility analogy:* a voltage source u, then C_s (inductor) in parallel
% with 1/R_s in SERIES, then the car mass M_mc/4 as a capacitor to ground.
% The car velocity is the voltage on that capacitor. This is a second-order
% low-pass filter: slow road waves pass straight to the car, fast bumps are
% filtered out.

%% Bonus problem 6b - Packers inside the spring
% When the spring is compressed far enough, the rubber packer C_p is squeezed
% too. The packer and the spring then take the same compression side by side:
% mechanically two springs in parallel.
%
% * Impedance analogy: C_s and C_p in SERIES (two capacitors in series).
% * Mobility analogy: C_s and C_p as two inductors in PARALLEL.
%
% Either way the total compliance is
%
% $$C_{tot} = \frac{C_s C_p}{C_s + C_p}$$
%
% which is smaller than the smaller of the two: the suspension is stiffer,
% which is what the packers are for (the car cannot bottom out).

%% Bonus problem 6c - Add the wheel mass and the tyre
% The wheel (with suspension parts) is a mass M_s, and the tyre is a spring
% C_t with damping R_t between the road and the wheel. These parts sit
% between the source and the old system, and so they do in the circuit.
%
% * Impedance analogy: velocity source u with the tyre branch R_t + C_t
%   across it (the road velocity either compresses the tyre or moves the
%   rest), then M_s in series, then the old system: R_s + C_s in parallel
%   with M_mc/4.
% * Mobility analogy: voltage source u, C_t (inductor) || 1/R_t in series,
%   node "wheel" with M_s as a capacitor to ground, then C_s || 1/R_s in
%   series, node "car" with M_mc/4 as a capacitor to ground.
%
% The packer is left out (not active). Compare with 5b: the same ladder
% shape, a mass on a spring on a mass on a spring, only driven by a velocity
% from the bottom instead of a force from the top.

%% Summary
% * Impedance analogy: force = voltage, velocity = current, mass = L,
%   compliance = C. Mobility analogy: the dual, velocity = voltage, mass = C
%   to ground, compliance = L, damper = 1/R.
% * Converting between them: series <-> parallel, L <-> C, R <-> 1/R,
%   V source <-> I source. 2.1 checks it numerically: same velocities.
% * Mass on a spring: f_0 = 1/(2 pi sqrt(M C)) = 35.6 Hz. Force drive gives a
%   velocity PEAK of F/R_M = 20 m/s; velocity drive gives a force DIP to R_M u
%   = 0.5 N.
% * A real source = ideal source + the driver's own Z_M; u_No = f_Th/Z_M and
%   u_Th = Y_M f_No, 20 m/s at resonance for 10 N.
% * Two masses: u1 dips at 1/(2 pi sqrt(M2 C1)) = 35.6 Hz, both masses
%   resonate on the reduced mass (61.6 Hz undamped, peak at 71 Hz because
%   Q = 0.86). The limiting cases open or short one branch.
% * Things that share a velocity are in series in the impedance analogy;
%   springs side by side (packers) add stiffness.
