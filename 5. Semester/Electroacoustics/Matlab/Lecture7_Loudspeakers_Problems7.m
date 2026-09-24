%% Lecture 7 - Moving-coil loudspeakers: Problems 7, worked
% 34870 Electroacoustics | 24 September 2026
%
% How to read this: every step first states the formula, then the MATLAB line
% is that same formula typed in, and the result appears right below it. The
% sheet's answer is written in the text so you can compare.
%
% All values are in SI units (kg, m, s, ohm). Grams and mm/N from the sheet
% are converted when they are typed in.
%
% Air (from the sheet):
rho = 1.2      % air density [kg/m^3]
c = 344        % speed of sound [m/s]

%% The formulas used in this whole problem set
% A loudspeaker below a few hundred Hz behaves like one mass-spring-damper,
% driven by the voice coil. Five numbers (the Thiele-Small parameters)
% describe it:
%
% *Resonance frequency* (mass and suspension spring):
%
% $$f_S = \frac{1}{2\pi\sqrt{M_{MS}\,C_{MS}}}$$
%
% *Mechanical Q* (how much the suspension damps the resonance):
%
% $$Q_{MS} = \frac{1}{R_{MS}}\sqrt{\frac{M_{MS}}{C_{MS}}}$$
%
% *Electrical Q* (how much the coil and amplifier damp it: the back-EMF
% drives a current through R_E that brakes the cone):
%
% $$Q_{ES} = \frac{R_E}{(Bl)^2}\sqrt{\frac{M_{MS}}{C_{MS}}}$$
%
% *Total Q* (both dampings together):
%
% $$Q_{TS} = \frac{Q_{MS}\,Q_{ES}}{Q_{MS} + Q_{ES}}$$
%
% *Equivalent volume* (the air volume that is as stiff as the suspension):
%
% $$V_{AS} = \rho c^2 S_D^2 C_{MS}$$
%
% Symbols: M_MS moving mass including the air [kg], C_MS suspension
% compliance [m/N], R_MS suspension damping [Ns/m], Bl force factor [Tm],
% R_E coil resistance [ohm], S_D cone area [m^2].

%% Problem 1a - Find f_S, Q_MS, Q_ES, Q_TS and V_AS
% Given, for the driver mounted in a baffle:
M_MS = 38e-3       % moving mass, 38 g [kg]
R_MS = 1.5         % mechanical damping [Ns/m]
C_MS = 0.9e-3      % compliance, 0.9 mm/N [m/N]
Bl = 5             % force factor [Tm]
R_E = 6            % coil resistance [ohm]
a = 0.10           % cone radius, 10 cm [m]
%%
% The cone area is a circle:
%
% $$S_D = \pi a^2$$
S_D = pi*a^2
%%
% *Resonance frequency.* $f_S = \frac{1}{2\pi\sqrt{M_{MS}C_{MS}}}$
%
% Sheet: 27.2 Hz
f_S = 1/(2*pi*sqrt(M_MS*C_MS))
%%
% *Mechanical Q.* $Q_{MS} = \frac{1}{R_{MS}}\sqrt{M_{MS}/C_{MS}}$
%
% Sheet: 4.3
Q_MS = 1/R_MS*sqrt(M_MS/C_MS)
%%
% *Electrical Q.* $Q_{ES} = \frac{R_E}{(Bl)^2}\sqrt{M_{MS}/C_{MS}}$
%
% Sheet: 1.56
Q_ES = R_E/Bl^2*sqrt(M_MS/C_MS)
%%
% *Total Q.* $Q_{TS} = \frac{Q_{MS}Q_{ES}}{Q_{MS}+Q_{ES}}$
%
% Sheet: 1.15
Q_TS = Q_MS*Q_ES/(Q_MS + Q_ES)
%%
% *Equivalent volume.* $V_{AS} = \rho c^2 S_D^2 C_{MS}$, in m^3, then in
% litres (1 m^3 = 1000 L).
%
% Sheet: 126 litre
V_AS = rho*c^2*S_D^2*C_MS
V_AS_litre = V_AS*1000
%%
% *What it means:* Q_ES is much smaller than Q_MS, so the electrical damping
% is the one that matters, and Q_TS ends up close to Q_ES. Q_TS = 1.15 is
% above 0.707, so this driver has a small peak at resonance.

%% Problem 1b - The same driver in free air
% In free air Q_ES is measured to 1.5. Find Q_MS and the moving mass.
%
% *The idea:* R_E, Bl and C_MS belong to the driver itself, so they are the
% same in free air. Only the air load on the cone changes, and with it
% M_MS. So we take the Q_ES formula and solve it for the mass:
%
% $$Q_{ES} = \frac{R_E}{(Bl)^2}\sqrt{\frac{M_{MS}}{C_{MS}}} \quad\Longrightarrow\quad M_{MS} = \left(\frac{Q_{ES}\,(Bl)^2}{R_E}\right)^2 C_{MS}$$
Q_ES_free = 1.5
M_MS_free = (Q_ES_free*Bl^2/R_E)^2*C_MS
%%
% In grams. Sheet: 35.2 g
M_MS_free_gram = M_MS_free*1000
%%
% Now the mechanical Q with the new mass, $Q_{MS} = \frac{1}{R_{MS}}\sqrt{M_{MS}/C_{MS}}$.
%
% Sheet: 4.17
Q_MS_free = 1/R_MS*sqrt(M_MS_free/C_MS)
%%
% *Check that this makes sense.* On a baffle each side of the cone carries
% an air mass (radiation mass)
%
% $$M_{A1} = \frac{8\rho}{3\pi^2 a}$$
%
% In free air the two sides share one M_A1, so the mass should drop by
% $S_D^2 M_{A1}$. That gives 34.8 g, close to the 35.2 g above.
M_A1 = 8*rho/(3*pi^2*a)
air_mass_one_side_gram = S_D^2*M_A1*1000
38 - air_mass_one_side_gram
%%
% Less mass means the resonance moves UP in free air:
f_S_free = 1/(2*pi*sqrt(M_MS_free*C_MS))

%% Problem 2 - Fill in the missing data for the 315 SWR
% From the data sheet:
%
% * free air: M_MS = 80.2 g, Q_ES = 0.49
% * common: C_MS = 0.55 mm/N, Bl = 11.6 Tm, V_AS = 210 L, R_MS = 3.25 Ns/m
% * baffled: M_MS = 88.2 g
%
% Each missing number comes from one of the five formulas, solved for the
% unknown.
Bl = 11.6          % [Tm]
C_MS = 0.55e-3     % 0.55 mm/N [m/N]
R_MS = 3.25        % [Ns/m]
V_AS = 0.210       % 210 L [m^3]
M_MS_free = 80.2e-3    % free air, 80.2 g [kg]
Q_ES_free = 0.49       % free air
M_MS = 88.2e-3         % baffled, 88.2 g [kg]
%%
% *Resonance frequency in free air.* $f_S = \frac{1}{2\pi\sqrt{M_{MS}C_{MS}}}$
% with the free-air mass.
%
% Sheet: 23.96 Hz
f_S_free = 1/(2*pi*sqrt(M_MS_free*C_MS))
%%
% *Cone area from V_AS.* Solve $V_{AS} = \rho c^2 S_D^2 C_{MS}$ for S_D:
%
% $$S_D = \sqrt{\frac{V_{AS}}{\rho c^2 C_{MS}}}$$
S_D = sqrt(V_AS/(rho*c^2*C_MS))
%%
% In cm^2 (1 m^2 = 10 000 cm^2). Sheet: 519 cm^2
S_D_cm2 = S_D*1e4
%%
% *Coil resistance from the free-air Q_ES.* Write Q_ES with omega_S instead
% of the square root (they are the same thing, since
% $\sqrt{M/C} = \omega_S M$):
%
% $$Q_{ES} = \frac{R_E\,\omega_S M_{MS}}{(Bl)^2} \quad\Longrightarrow\quad R_E = \frac{Q_{ES}\,(Bl)^2}{\omega_S M_{MS}}, \qquad \omega_S = 2\pi f_S$$
%
% Sheet: 5.46 ohm
R_E = Q_ES_free*Bl^2/(2*pi*f_S_free*M_MS_free)
%%
% *Electrical Q on the baffle.* Same formula, now with the baffled mass and
% the baffled resonance frequency.
f_S = 1/(2*pi*sqrt(M_MS*C_MS))
%%
% Sheet: 0.515
Q_ES = R_E*2*pi*f_S*M_MS/Bl^2
%%
% *Free check:* the impedance peak is $Z_{max} = R_E + (Bl)^2/R_{MS}$, and
% the data sheet says "maximum impedance 46.9 ohm".
Z_max = R_E + Bl^2/R_MS

%% Problem 3.1 - Efficiency
% Efficiency = acoustic power out / electrical power in. Above resonance the
% cone is mass controlled and the coil impedance is about R_E. Working it
% through (lecture slide 18), the frequency cancels and what is left is
%
% $$\eta = \frac{\rho}{2\pi c}\;\frac{1}{R_E}\left(\frac{Bl\,S_D}{M_{MS}}\right)^2$$
%
% Use the baffled mass (the speaker is in a baffle). Sheet: 0.47 %
eta = rho/(2*pi*c) * 1/R_E * (Bl*S_D/M_MS)^2
eta_percent = eta*100
%%
% So less than half a percent of the electrical power becomes sound. The
% rest heats the voice coil.

%% Problem 3.2 - Sensitivity (pressure at 1 m for 1 V)
% Above resonance the pressure 1 m away is flat and equal to
%
% $$p_{1m} = \frac{\rho}{2\pi}\,\frac{Bl\,S_D}{R_E\,M_{MS}}\cdot e_g$$
%
% with e_g = 1 V.
e_g = 1
p_1m = rho/(2*pi) * Bl*S_D/(R_E*M_MS) * e_g
%%
% In dB relative to 1 Pa/V: $20\log_{10}(p_{1m})$. Sheet: -12.4 dB
sensitivity_dB = 20*log10(p_1m)
%%
% The same as a sound pressure level (re 20 µPa), for 1 V and for 2.83 V
% (1 W into 8 ohm). The data sheet measured 89.3 dB at 2.83 V.
SPL_1V = 20*log10(p_1m/20e-6)
SPL_2V83 = 20*log10(2.83*p_1m/20e-6)

%% Problem 3.3 - Cone displacement at 50 Hz and 200 Hz, 4 V
% Displacement is a low-pass filter with the same resonance and Q as the
% speaker:
%
% $$x_D = \frac{Bl\,C_{MS}}{R_E}\;\frac{e_g}{\left|\,1 - (f/f_S)^2 + j\,\dfrac{f/f_S}{Q_{TS}}\,\right|}$$
%
% The first fraction is the displacement at very low frequency (the force
% Bl*e_g/R_E pushing on the spring). The second part is the usual resonance
% denominator: about 1 far below f_S, large far above it.
%
% We need Q_TS for the baffled speaker first:
Q_MS = 2*pi*f_S*M_MS/R_MS
Q_TS = Q_MS*Q_ES/(Q_MS + Q_ES)
e_g = 4
%%
% Low-frequency displacement, in mm:
x_static_mm = Bl*C_MS/R_E*e_g*1000
%%
% *At 50 Hz.* Sheet: 0.76 mm
f = 50;
x_50Hz_mm = Bl*C_MS/R_E*e_g / abs(1 - (f/f_S)^2 + 1j*(f/f_S)/Q_TS) * 1000
%%
% *At 200 Hz.* Sheet: 59.9 µm (printed as "m", a typo)
f = 200;
x_200Hz_um = Bl*C_MS/R_E*e_g / abs(1 - (f/f_S)^2 + 1j*(f/f_S)/Q_TS) * 1e6
%%
% Four times the frequency gives about 1/13 of the displacement. Far above
% resonance it becomes 1/16, because the mass takes over.

%% Problem 3.4 - Maximum SPL before the coil leaves the magnet gap
% The coil is 26 mm long and the gap is 8 mm high. The coil is longer than
% the gap (overhung), so it can move this far before windings leave the
% gap:
%
% $$x_{max} = \frac{l_{vc} - h_{mg}}{2}$$
x_max = (26e-3 - 8e-3)/2
%%
% The far-field pressure from a moving piston at distance r is set by its
% acceleration, $\omega^2 x$:
%
% $$p = \frac{\omega^2\,\rho\,S_D\,x}{2\pi r}, \qquad \omega = 2\pi f$$
%
% x_max is a peak value, so divide by sqrt(2) for the rms pressure, then
% convert to dB SPL.
r = 1;
f = 50;
p_peak_50Hz = (2*pi*f)^2*rho*S_D*x_max/(2*pi*r)
SPL_max_50Hz = 20*log10(p_peak_50Hz/sqrt(2)/20e-6)
%%
% Sheet: 109.9 dB. Now at 200 Hz (sheet: 133.9 dB):
f = 200;
p_peak_200Hz = (2*pi*f)^2*rho*S_D*x_max/(2*pi*r)
SPL_max_200Hz = 20*log10(p_peak_200Hz/sqrt(2)/20e-6)
%%
% *Reality check:* how many volts would that take? From 3.3, 4 V gives
% 0.76 mm at 50 Hz and 0.060 mm at 200 Hz, and displacement scales with
% voltage:
volts_needed_50Hz = 4 * x_max/(x_50Hz_mm/1000)
volts_needed_200Hz = 4 * x_max/(x_200Hz_um/1e6)
%%
% 600 V would burn the coil long before. At high frequency the real limit is
% heat, at low frequency it is excursion. The data sheet's "max linear SPL
% 110 dB" is the 50 Hz number.

%% Problem 4 - The loudspeaker model over frequency
% Problem 4 asks for this in LTspice (the finished model is in
% LTspice/Problems 7 - Loudspeaker/). Here we compute the same three
% curves: input impedance, sound pressure and displacement.
%
% *Step 1: the air load.* Each side of the cone pushes on air. For a piston
% in a baffle at low frequency that air acts as a mass
% $M_{A1} = 8\rho/(3\pi^2 a)$ per side. Seen from the cone it adds
% $2 S_D^2 M_{A1}$ to the mass.
%
% The data sheet's 88.2 g already includes that air. The model adds the
% air separately, so we need the mass WITHOUT air, the diaphragm mass:
%
% $$M_{MD} = M_{MS} - 2S_D^2M_{A1}$$
a = sqrt(S_D/pi)
M_A1 = 8*rho/(3*pi^2*a)
M_MD = M_MS - 2*S_D^2*M_A1
M_MD_gram = M_MD*1000
%%
% *Step 2: the full air load (not just the mass).* At higher frequency the
% air load also has a resistive part, the part that actually radiates
% sound. Leach's circuit for a baffled piston is
%
% $$Z_{ar} = j\omega M_{A1} \;\parallel\; \left[R_{A2} + \left(R_{A1}\parallel \frac{1}{j\omega C_{A1}}\right)\right]$$
%
% with these element values:
R_A1 = 0.441*rho*c/S_D
R_A2 = rho*c/S_D
C_A1 = 5.94*a^3/(rho*c^2)
%%
% *Step 3: the frequency axis* (5 Hz to 20 kHz, 2000 points, log spaced)
% and $j\omega$.
f = logspace(log10(5), log10(20000), 2000);
jw = 1j*2*pi*f;
%%
% The air-load circuit from step 2, typed in (a parallel connection is
% 1/(1/Z1 + 1/Z2)):
Z_ar = 1 ./ ( 1./(jw*M_A1) + 1./(R_A2 + 1./(1/R_A1 + jw*C_A1)) );
%%
% *Step 4: mechanical impedance of the moving cone.* Mass, damper, spring,
% plus the air load on both sides transformed by S_D^2:
%
% $$Z_M = j\omega M_{MD} + R_{MS} + \frac{1}{j\omega C_{MS}} + 2S_D^2 Z_{ar}$$
Z_M = jw*M_MD + R_MS + 1./(jw*C_MS) + 2*S_D^2*Z_ar;
%%
% *Step 5: what the amplifier sees.* The coil is a gyrator: the mechanical
% impedance shows up at the terminals as (Bl)^2 / Z_M:
%
% $$Z_E = R_E + \frac{(Bl)^2}{Z_M}$$
Z_E = R_E + Bl^2./Z_M;
%%
% *Step 6: from 1 V to cone velocity, volume velocity, pressure and
% displacement.*
%
% $$i = \frac{e_g}{Z_E}, \quad u = \frac{Bl\,i}{Z_M}, \quad U = S_D\,u, \quad p_{far} = \frac{j\omega\rho\,U}{2\pi r}, \quad p_{near} = Z_{ar}\,U, \quad x = \frac{u}{j\omega}$$
e_g = 1;
i = e_g./Z_E;
u = Bl*i./Z_M;
U = S_D*u;
p_far = jw*rho.*U/(2*pi*1);
p_near = Z_ar.*U;
x = u./jw;

%% Problem 4.1 - Check the model: where is the impedance peak?
% The impedance peak should sit at the resonance, f_S = 22.9 Hz on the data
% sheet, with a height of about R_E + (Bl)^2/R_MS = 46.9 ohm.
[Z_peak, k] = max(abs(Z_E))
f_peak = f(k)
%%
% The peak is slightly lower than 46.9 ohm because the air's radiation
% resistance adds a little damping.
figure;
semilogx(f, abs(Z_E), 'LineWidth', 1.5);
grid on; xlim([5 20000]);
xlabel('Frequency [Hz]'); ylabel('|Z_E| [\Omega]');
title('Input impedance, voice coil = R_E only');

%% Problem 4.2 - Far-field and near-field sound pressure
% Far field (1 m) and near field (microphone right at the cone), both for
% 1 V, as SPL:
%
% $$L_p = 20\log_{10}\frac{|p|}{20\,\mu\text{Pa}}$$
SPL_far = 20*log10(abs(p_far)/20e-6);
SPL_near = 20*log10(abs(p_near)/20e-6);
figure;
semilogx(f, SPL_far, f, SPL_near, 'LineWidth', 1.5);
grid on; xlim([5 20000]); ylim([40 110]);
xlabel('Frequency [Hz]'); ylabel('SPL for 1 V [dB]');
legend('far field, 1 m', 'near field', 'Location', 'southeast');
title('Sound pressure');
%%
% Both curves have the same shape at low frequency. The near field is higher
% by
%
% $$\frac{p_{near}}{p_{far}} = \frac{16\,r}{3\pi a}$$
near_minus_far_dB = 20*log10(16*1/(3*pi*a))
%%
% That is why you can measure close to the cone (no anechoic room needed)
% and subtract 22.4 dB to get the far-field response. It only works while
% ka < 1, i.e. below this frequency:
f_ka1 = c/(2*pi*a)

%% Problem 4.3 - Add the lossy voice-coil inductance
% A real voice coil is not an ideal inductor. Eddy currents in the iron pole
% piece make it rise more slowly with frequency. The sheet's model is
%
% $$Z_L = L_E^*\,(j\omega)^n, \qquad L_E^* = 0.0106,\; n = 0.76$$
%
% It simply goes in series with R_E:
%
% $$Z_E = R_E + L_E^*(j\omega)^n + \frac{(Bl)^2}{Z_M}$$
L_star = 0.0106;
n = 0.76;
Z_E_lossy = R_E + L_star*jw.^n + Bl^2./Z_M;
%%
% For comparison, an ideal 2.8 mH inductor (the data sheet's L_E):
Z_E_ideal = R_E + jw*2.8e-3 + Bl^2./Z_M;
figure;
semilogx(f, abs(Z_E), f, abs(Z_E_lossy), f, abs(Z_E_ideal), '--', 'LineWidth', 1.5);
grid on; xlim([5 20000]); ylim([0 60]);
xlabel('Frequency [Hz]'); ylabel('|Z_E| [\Omega]');
legend('R_E only', 'lossy L_E (j\omega)^{0.76}', 'ideal 2.8 mH', 'Location', 'north');
title('Input impedance with the coil inductance');
%%
% At 1 kHz: R_E only, lossy model, ideal inductor (ohm). The ideal inductor
% rises far too fast. The lossy model is what real speakers measure like.
k = find(f >= 1000, 1);
Z_at_1kHz = [abs(Z_E(k)), abs(Z_E_lossy(k)), abs(Z_E_ideal(k))]

%% Displacement over frequency (links back to 3.3)
% The same model gives the cone displacement. Here at 4 V, in mm, with the
% 9 mm limit from 3.4 drawn in.
figure;
loglog(f, 4*abs(x)*1000, 'LineWidth', 1.5);
hold on; yline(x_max*1000, 'r--', 'x_{max} = 9 mm'); hold off;
grid on; xlim([5 2000]); ylim([1e-3 20]);
xlabel('Frequency [Hz]'); ylabel('Displacement at 4 V [mm]');
title('Cone displacement');

%% Summary
% * f_S, Q_MS, Q_ES, Q_TS and V_AS all come from M_MS, C_MS, R_MS, Bl, R_E and S_D.
% * The electrical damping usually dominates, so Q_TS is close to Q_ES.
% * Free air has half the air mass of a baffle, so f_S is higher there.
% * Above f_S the pressure is flat at (rho/2pi) Bl S_D/(R_E M_MS) per volt.
% * Efficiency is below 1 %; the rest heats the coil.
% * Displacement grows 4x for every octave lower: bass is limited by
%   excursion, treble by heat.
% * In a model that includes the air load, use the mass without air, M_MD.
