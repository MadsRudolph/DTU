%% Lab D - Loudspeaker impedance and near field, worked through our own data
% 34870 Electroacoustics | Group 10, System D, measured 6 October 2026
%
% How to read this: every step states the formula first, the MATLAB line is
% that same formula typed in, and the result appears right below it. Where
% the data sheet or the brief has a number, it is written in the text so you
% can compare.
%
% The data are the cleaned files in the labs repo (Labs/Lab D/data/). Each
% one holds fn (frequency), specn (the two measured spectra) and the
% corrected Z (impedance runs) or H (near-field runs, Pa/V). Only the files
% without _rN are loaded: those are the best of the repeats.
%
% Run this from the Matlab folder (5. Semester/Electroacoustics/Matlab).
D = fullfile('..', 'Labs', 'Lab D', 'data');
tw = load(fullfile(D, 'labD_tweeter.mat'));        % tweeter, in the DALI box
mid = load(fullfile(D, 'labD_midrange.mat'));      % midrange, in the DALI box (port closed)
wf = load(fullfile(D, 'labD_woofer_free.mat'));    % woofer, free air (back cover off)
wc = load(fullfile(D, 'labD_woofer_closed.mat'));  % woofer, closed box, vents plugged
v160 = load(fullfile(D, 'labD_vent_L160.mat'));    % woofer, one vent open, tube 160 mm
v200 = load(fullfile(D, 'labD_vent_L200.mat'));
v240 = load(fullfile(D, 'labD_vent_L240.mat'));
nc160 = load(fullfile(D, 'labD_nf_cone_L160.mat'));   % near field at the cone
nc200 = load(fullfile(D, 'labD_nf_cone_L200.mat'));
nc240 = load(fullfile(D, 'labD_nf_cone_L240.mat'));
nv160 = load(fullfile(D, 'labD_nf_vent_L160.mat'));   % near field at the vent
nv200 = load(fullfile(D, 'labD_nf_vent_L200.mat'));
nv240 = load(fullfile(D, 'labD_nf_vent_L240.mat'));
%%
% Air at 20 C (the room temperature was not written down, 20 C is assumed):
c = 343.2      % speed of sound (m/s)
rho = 1.204    % air density (kg/m^3)

%% Part 1 - DC resistance (multimeter)
% The voice coil's wire resistance, measured with no signal. At very low
% frequency the impedance curve has to land on these values; that is the
% check that the impedance measurement is right.
R_E_tw = 3.4     % tweeter (ohm)
R_E_mid = 4.6    % midrange (ohm)
R_E_wf = 5.7     % woofer (ohm), data sheet: 5.7

%% Part 2 - How the impedance is measured
% The amplifier drives the speaker through a known resistor R. The card
% records the amplifier voltage V_amp (AI0) and the speaker voltage V_loud
% (AI1). The same current flows through R and the speaker, so
%
% $$I = \frac{V_{amp}-V_{loud}}{R}, \qquad Z_L = \frac{V_{loud}}{I} = R\,\frac{V_{loud}/V_{amp}}{1-V_{loud}/V_{amp}}$$
%
% Two things went wrong on the day and are corrected in the files:
%
% * The script was given R = R_E instead of the 32.9 ohm resistor.
% * AI0 sat on a 9.4 V DC offset and read only HALF the amplifier voltage
%   (a bridged amplifier output). So V_amp = 2*AI0.
%
% Check that the stored Z is exactly this formula, on the tweeter:
R = 32.9                                      % the series resistor (ohm)
G = tw.specn(:,2) ./ (2*tw.specn(:,1));       % V_loud / V_amp
Z_check = R * G ./ (1 - G);
largest_difference = max(abs(Z_check - tw.Z))
%%
% Zero: the file's Z is the formula above. With the factor 2 the curve lands
% on R_E at low frequency and the woofer's free-air peak lands on the data
% sheet's 117 ohm. Without it, |Z| would come out about half as big.

%% Part 2a - The three units' impedances (for the crossover)
figure('Name', 'labD_fig1_three_units');
subplot(2,1,1);
loglog(tw.fn, abs(tw.Z), mid.fn, abs(mid.Z), wc.fn, abs(wc.Z), 'LineWidth', 1.4);
grid on; xlim([10 24000]); ylim([2 150]);
ylabel('|Z| (\Omega)');
legend('tweeter (DALI box)', 'midrange (DALI box)', 'woofer (closed box)', 'Location', 'north');
title('Input impedance of the three units');
subplot(2,1,2);
semilogx(tw.fn, rad2deg(angle(tw.Z)), mid.fn, rad2deg(angle(mid.Z)), wc.fn, rad2deg(angle(wc.Z)), 'LineWidth', 1.4);
grid on; xlim([10 24000]); ylim([-90 90]); yticks(-90:45:90);
xlabel('Frequency (Hz)'); ylabel('phase of Z (\circ)');
%%
% *How to read an impedance curve*, left to right:
%
% # *Low frequency:* |Z| = R_E and the phase is 0. Only the wire.
% # *The peak is the mechanical resonance.* Through the motor, the
%   mechanical impedance appears inverted on the electrical side:
%
% $$Z_E = R_E + j\omega L_E + \frac{(Bl)^2}{Z_M}, \qquad Z_M = j\omega M_{MS} + R_{MS} + \frac{1}{j\omega C_{MS}}$$
%
% At resonance Z_M is smallest (just R_MS), so (Bl)^2/Z_M is largest: the
% cone moves the most and its back-EMF opposes the current the most.
%
% # *The phase tells you which side of the resonance you are on.* Below the
%   peak the cone is stiffness-controlled; 1/(jwC) inverted becomes jw(..),
%   so it looks like an INDUCTANCE (+ phase). Above the peak the cone is
%   mass-controlled and looks like a CAPACITANCE (- phase). The phase crosses
%   0 going down exactly at the resonance. That is the precise way to read f
%   (the graders want resonances read from impedance and phase, not from a
%   pressure peak).
% # *High frequency:* the voice-coil inductance L_E makes |Z| rise again and
%   the phase go positive.
%
% Read the three peaks:
k = tw.fn < 5000;                    % tweeter: ignore the inductive rise up top
[Zmax_tw, i] = max(abs(tw.Z(k)))
f_tw = tw.fn(i)
k = mid.fn < 1000;
[Zmax_mid, i] = max(abs(mid.Z(k)))
f_mid = mid.fn(i)
%%
% Tweeter 1.45 kHz, only 6.7 ohm: a small, heavily damped peak (low Q). Midrange 90 Hz, 19 ohm: that is the 5 1/4" driver IN its DALI
% box, not in free air. The woofer (closed box) peaks at 42 Hz and 123 ohm.
%
% *What the project uses:* the midrange and tweeter curves, as they are. A
% passive crossover sees this impedance, not a resistor: around 1.45 kHz the
% tweeter is 6.7 ohm instead of 3.6, and at 10 kHz the midrange is 3x its
% R_E. A filter designed for a nominal resistor moves its corner.

%% Part 2b1 - Woofer T-S parameters in free air (brief, Appendix B)
% The method uses only the magnitude curve:
%
% $$r_c = \frac{Z_{max}}{R_E}, \qquad Z_r = \sqrt{R_E Z_{max}}, \qquad Q_M = \frac{f_0\sqrt{r_c}}{f_2-f_1}, \qquad Q_E = \frac{Q_M}{r_c-1}, \qquad Q_T = \frac{Q_M}{r_c}$$
%
% f1 and f2 are where |Z| = Z_r on each side of the peak. Z_r is the
% geometric mean, so on a log axis it sits halfway between R_E and Z_max.
k = wf.fn > 5 & wf.fn < 200;
f = wf.fn(k); Zm = abs(wf.Z(k));
[Zmax, i0] = max(Zm)
f_s = f(i0)
%%
% Data sheet: f_s = 23 Hz, Z_o = 117 ohm.
r_c = Zmax / R_E_wf
Z_r = sqrt(R_E_wf * Zmax)
%%
% The two crossings of Z_r, by linear interpolation between the two points
% on either side (lo = last point under Z_r below the peak, hi = first point
% under Z_r above it):
lo = find(Zm(1:i0) < Z_r, 1, 'last');
f1 = interp1(Zm(lo:lo+1), f(lo:lo+1), Z_r)
hi = i0 - 1 + find(Zm(i0:end) < Z_r, 1);
f2 = interp1(Zm(hi-1:hi), f(hi-1:hi), Z_r)
%%
% Check: f_s should be the geometric mean of f1 and f2.
sqrt(f1*f2)
%%
Q_MS = f_s * sqrt(r_c) / (f2 - f1)
Q_ES = Q_MS / (r_c - 1)
Q_TS = Q_MS / r_c
%%
% Data sheet: Q_MS = 9.12, Q_ES = 0.42, Q_TS = 0.40. Our Q_MS is close; Q_ES
% and Q_TS are about 20 % higher (see the discussion after V_AS).
%
% *What the Q's mean.* Q_MS is the suspension's own damping (lossy rubber),
% Q_ES the damping by the back-EMF driving current through R_E. Q_ES is 20x
% smaller, so the electrical damping dominates and Q_TS is close to Q_ES.
figure('Name', 'labD_fig2_free_air_method');
subplot(2,1,1);
loglog(f, Zm, 'LineWidth', 1.4); hold on;
yline([R_E_wf Z_r Zmax], ':', {'R_E', 'Z_r = \surd(R_E Z_{max})', 'Z_{max}'});
plot([f1 f_s f2], [Z_r Zmax Z_r], 'o', 'MarkerFaceColor', 'auto');
grid on; xlim([5 200]); ylabel('|Z| (\Omega)');
title('Woofer in free air: the Appendix B construction');
subplot(2,1,2);
semilogx(f, rad2deg(angle(wf.Z(k))), 'LineWidth', 1.4);
xline([f1 f_s f2], ':', {'f_1', 'f_s', 'f_2'});
grid on; xlim([5 200]); ylim([-90 90]); yticks(-90:45:90);
xlabel('Frequency (Hz)'); ylabel('phase of Z (\circ)');
%%
% Notice that at f1 and f2 the phase is about +-45 deg: those are the
% half-power points of the motional part, the same idea as the -3 dB
% points of any resonance.

%% Part 2b2 - Closed box
% Same method, same formulas. The box's air is an extra spring behind the
% cone, so the resonance moves up.
k = wc.fn > 5 & wc.fn < 200;
f = wc.fn(k); Zm = abs(wc.Z(k));
[Zmax_c, i0] = max(Zm)
f_c = f(i0)
r_cc = Zmax_c / R_E_wf
Z_rc = sqrt(R_E_wf * Zmax_c);
lo = find(Zm(1:i0) < Z_rc, 1, 'last');
f1c = interp1(Zm(lo:lo+1), f(lo:lo+1), Z_rc)
hi = i0 - 1 + find(Zm(i0:end) < Z_rc, 1);
f2c = interp1(Zm(hi-1:hi), f(hi-1:hi), Z_rc)
Q_MC = f_c * sqrt(r_cc) / (f2c - f1c)
Q_EC = Q_MC / (r_cc - 1)
Q_TC = Q_MC / r_cc
%%
figure('Name', 'labD_fig3_free_vs_closed');
subplot(2,1,1);
semilogx(wf.fn, abs(wf.Z), wc.fn, abs(wc.Z), 'LineWidth', 1.4);
grid on; xlim([5 300]); ylabel('|Z| (\Omega)');
legend('free air', 'closed box (88 L)');
title('Woofer: free air against closed box');
subplot(2,1,2);
semilogx(wf.fn, rad2deg(angle(wf.Z)), wc.fn, rad2deg(angle(wc.Z)), 'LineWidth', 1.4);
grid on; xlim([5 300]); ylim([-90 90]); yticks(-90:45:90);
xlabel('Frequency (Hz)'); ylabel('phase of Z (\circ)');

%% Part 2b3 - Box volume and V_AS (Lecture 8, added-compliance method)
% Inner dimensions, no filling, so the effective volume is the physical one:
V_B = 0.435 * 0.45 * 0.45     % (m^3)
V_B_litre = V_B * 1000
%%
% The box's air spring adds to the suspension's. Springs in parallel add
% their stiffnesses, i.e. 1/C_total = 1/C_MS + 1/C_box. The mass is the same
% in both measurements, so f^2 is proportional to the stiffness:
%
% $$\frac{f_c^2}{f_s^2} = 1 + \frac{V_{AS}}{V_B} \quad\Rightarrow\quad V_{AS} = V_B\left[\left(\frac{f_c}{f_s}\right)^2 - 1\right]$$
%
% (The group report has this without the square. The square matters: it
% would give 74 L instead of 209 L.)
alpha = (f_c / f_s)^2 - 1
V_AS = V_B * alpha
V_AS_litre = V_AS * 1000
%%
% Data sheet: 150 L. The same theory says Q_TC/Q_TS should equal f_c/f_s
% (both are sqrt(1+alpha)). Check it:
f_c / f_s
Q_TC / Q_TS
%%
% They disagree by 6 %. Using the Q ratio instead gives:
V_AS_from_Q = V_B * ((Q_TC / Q_TS)^2 - 1) * 1000     % (litre)
%%
% *Why our V_AS is larger than the data sheet's.* The method assumes the
% moving mass is the same in both measurements. It is not quite: in free
% air the cone carries air mass on both sides, in the box the rear air
% mass is different (and our "free air" was with the back cover off, the
% driver still in the box, so its rear sees a short wide tube). Add to that
% the spread between samples of the same driver (+-15 % on V_AS is normal)
% and a box that may not be perfectly airtight. The sensible statement is
% a range: 175-215 L from our data, 150 L on the data sheet.
%
% From V_AS and the cone area the remaining parameters follow:
%
% $$C_{AS} = \frac{V_{AS}}{\rho c^2},\quad C_{MS} = \frac{C_{AS}}{S_D^2},\quad M_{MS} = \frac{1}{\omega_s^2 C_{MS}},\quad Bl = \sqrt{\frac{\omega_s R_E M_{MS}}{Q_{ES}}},\quad R_{MS} = \frac{\omega_s M_{MS}}{Q_{MS}}$$
S_D = pi * (0.211/2)^2          % effective cone area (m^2), data sheet D = 211 mm
w_s = 2*pi*f_s;
C_MS = V_AS / (rho*c^2) / S_D^2  % (m/N), data sheet 0.95e-3
M_MS = 1 / (w_s^2 * C_MS)        % (kg), data sheet 50.5 g
Bl = sqrt(w_s * R_E_wf * M_MS / Q_ES)   % (T m), data sheet 10.1
R_MS = w_s * M_MS / Q_MS         % (kg/s), data sheet 0.80
%%
% Every one of these inherits V_AS's error: M_MS goes as 1/V_AS, and Bl as
% sqrt(M_MS/Q_ES). That is why the project should take f_s and the Q's from
% our measurement and say clearly where V_AS comes from.

%% Part 2b4 - Vented box: two peaks and a dip
figure('Name', 'labD_fig4_vented');
subplot(2,1,1);
semilogx(wc.fn, abs(wc.Z), 'k', v160.fn, abs(v160.Z), v200.fn, abs(v200.Z), v240.fn, abs(v240.Z), 'LineWidth', 1.4);
grid on; xlim([5 150]); ylabel('|Z| (\Omega)');
legend('closed', 'vent 160 mm', 'vent 200 mm', 'vent 240 mm');
title('Woofer box: one closed-box peak becomes two vented-box peaks');
subplot(2,1,2);
semilogx(wc.fn, rad2deg(angle(wc.Z)), 'k', v160.fn, rad2deg(angle(v160.Z)), v200.fn, rad2deg(angle(v200.Z)), v240.fn, rad2deg(angle(v240.Z)), 'LineWidth', 1.4);
grid on; xlim([5 150]); ylim([-90 90]); yticks(-90:45:90);
xlabel('Frequency (Hz)'); ylabel('phase of Z (\circ)');
%%
% *Why two peaks.* The box air (a spring, C_AB) and the air plug in the vent
% (a mass, M_AP) form a Helmholtz resonator. Coupled to the cone's own
% mass-spring, two resonators give two modes: f_L where cone and vent air
% move together, f_H where they move against each other.
%
% *Why the dip is f_b.* At the Helmholtz resonance the vent air swings by
% itself, and the pressure it builds in the box holds the cone still. A still
% cone makes no back-EMF, so |Z| drops towards R_E. The phase crosses 0 going
% UP there (between two peaks it must). The dip in |Z| is where the vent
% does all the work, which is why it is the vent tuning.
%
% Read the dip on each curve (search between the two peaks, 15-35 Hz):
k = v160.fn > 15 & v160.fn < 35; [~, i] = min(abs(v160.Z(k))); f160 = v160.fn(k);
fb_160 = f160(i)
k = v200.fn > 15 & v200.fn < 35; [~, i] = min(abs(v200.Z(k))); f200 = v200.fn(k);
fb_200 = f200(i)
k = v240.fn > 15 & v240.fn < 35; [~, i] = min(abs(v240.Z(k))); f240 = v240.fn(k);
fb_240 = f240(i)
%%
% *The calculation.* A Helmholtz resonator:
%
% $$f_b = \frac{c}{2\pi}\sqrt{\frac{S_P}{V_B\,L_{eff}}}, \qquad L_{eff} = L + 0.85a + 0.61a = L + 1.46a$$
%
% The air moving in a tube drags extra air along at each end: 0.85a at the
% flanged end (inside, on the baffle) and 0.61a at the free end. Leaving
% out this end correction (as the group report does) makes every f_b too
% high (26.5 / 23.7 / 21.6 Hz).
a_P = 0.065/2          % vent radius (m)
S_P = pi*a_P^2         % vent area (m^2)
L = [0.160 0.200 0.240];
fb_calc = c/(2*pi) * sqrt(S_P ./ (V_B * (L + 1.46*a_P)))
%%
% Measured 23.4 / 22.8 / 21.5 Hz, calculated 23.3 / 21.3 / 19.8 Hz. Both go
% down as the tube gets longer (more air mass), and the longest tube is the
% furthest off: the measured dip moves less than the formula says.

%% Part 3 - Near field at the cone and at the vent
% Close to a small source (r << a, ka << 1) the pressure only depends on
% the volume velocity and the radiation MASS in front of it:
%
% $$p_{near} = j\omega M_{A1}U, \qquad M_{A1} = \frac{8\rho}{3\pi^2 a}$$
%
% Far away, p_far = j w rho U / (2 pi r): the same j w U, so the near-field
% curve has the far-field SHAPE. A small room cannot give you an anechoic
% 20 Hz; a microphone 1 cm from the cone can.
%
% The near-field files hold H = p / V_loud in Pa/V. Both channels are on
% the same NI card with a shared clock, so the phase is valid here (unlike
% the sound card in Lab E).
figure('Name', 'labD_fig5_near_field');
subplot(2,1,1);
semilogx(nc160.fn, 20*log10(abs(nc160.H)), nc200.fn, 20*log10(abs(nc200.H)), nc240.fn, 20*log10(abs(nc240.H)), 'LineWidth', 1.4); hold on;
set(gca, 'ColorOrderIndex', 1);
semilogx(nv160.fn, 20*log10(abs(nv160.H)), '--', nv200.fn, 20*log10(abs(nv200.H)), '--', nv240.fn, 20*log10(abs(nv240.H)), '--', 'LineWidth', 1.4);
grid on; xlim([8 300]); ylim([-25 20]);
ylabel('|p/V| (dB re 1 Pa/V)');
legend('cone 160', 'cone 200', 'cone 240', 'vent 160', 'vent 200', 'vent 240', 'Location', 'southeast', 'NumColumns', 2);
title('Near field: cone (solid) and vent (dashed)');
subplot(2,1,2);
semilogx(nc200.fn, rad2deg(angle(nc200.H)), nv200.fn, rad2deg(angle(nv200.H)), 'LineWidth', 1.4);
grid on; xlim([8 100]); ylim([-180 180]); yticks(-180:90:180);
legend('cone 200 mm', 'vent 200 mm');
xlabel('Frequency (Hz)'); ylabel('phase (\circ)');
%%
% *What you see.*
%
% * The cone has a deep, broad notch near f_b: the vent holds it still.
% * The vent is strong from about f_b down: below f_b it is the vent that
%   radiates. Above f_b the vent's own output falls (12 dB/octave), and
%   what the vent microphone hears up there is mostly the cone, 10 cm away.
% * Cone and vent are about 180 deg apart below f_b: the vent air moves out
%   while the cone moves in. That is why a vented box falls at 24 dB/octave
%   below f_b: the two cancel.
% * The sharp wiggle at 56 Hz in every curve is the room, not the speaker
%   (next section).
%
% Read the cone notch (search 12-60 Hz; analyse_labD searches from 5 Hz and
% finds noise at 6 Hz for two of the runs):
k = nc160.fn > 12 & nc160.fn < 60; [~, i] = min(abs(nc160.H(k))); f = nc160.fn(k);
fb_nf_160 = f(i)
k = nc200.fn > 12 & nc200.fn < 60; [~, i] = min(abs(nc200.H(k))); f = nc200.fn(k);
fb_nf_200 = f(i)
k = nc240.fn > 12 & nc240.fn < 60; [~, i] = min(abs(nc240.H(k))); f = nc240.fn(k);
fb_nf_240 = f(i)
%%
% The notch is broad and flat-bottomed, so its lowest point jumps around by
% a Hz or two with noise. The impedance dip is the better estimate of f_b;
% the near field confirms it and shows the vent taking over.

%% Part 3 - Adding cone and vent: the far-field response of the vented box
% Because p_near ~ U/a, the two near-field pressures cannot be added as they
% are: the vent is smaller, so the same U gives a higher pressure in front
% of it. Scale each by its radius to get something proportional to U:
%
% $$p_{far} \propto U_{cone} + U_{vent} \propto a_D\,p_{cone} + a_P\,p_{vent}$$
a_D = 0.211/2       % cone radius (m)
H_sum = (a_D*nc200.H + a_P*nv200.H) / a_D;    % normalised to the cone's level
figure('Name', 'labD_fig6_near_field_sum');
semilogx(nc200.fn, 20*log10(abs(nc200.H)), nv200.fn, 20*log10(abs(nv200.H*a_P/a_D)), nc200.fn, 20*log10(abs(H_sum)), 'k', 'LineWidth', 1.4);
grid on; xlim([8 300]); ylim([-35 20]);
xlabel('Frequency (Hz)'); ylabel('|p/V| (dB re 1 Pa/V, cone scale)');
legend('cone', 'vent x a_P/a_D', 'sum = far-field shape', 'Location', 'southeast');
title('Vent 200 mm: cone + vent, each scaled to volume velocity');
%%
% The sum is the vented box's far-field response: flat down to about f_b,
% then a steep 24 dB/octave fall, because below f_b the vent and cone are
% out of phase and cancel. In the project this curve is what the woofer's
% circuit analogy has to reproduce.

%% Part 3 - Room modes
% The lab is a rectangular room 3.35 x 3.05 x 3.09 m. Its axial modes are
% half a wavelength across each dimension:
%
% $$f_{n} = \frac{c}{2}\,\frac{n}{L_{room}}$$
room = [3.35 3.05 3.09];
f_axial = c ./ (2*room)
%%
% 3.05 m and 3.09 m are nearly equal, so two modes stack at 55.5-56.3 Hz.
% A strong double mode is exactly what the near-field curves show at 56 Hz.
% The impedance curves do not show it: it is acoustic, not electrical.

%% What goes to the project
% * *Woofer:* f_s = 22.7 Hz, Q_MS 9.9, Q_ES 0.51, Q_TS 0.49, V_AS 175-215 L
%   (data sheet 150 L). Vent tuning 23.4 / 22.8 / 21.5 Hz for 160 / 200 /
%   240 mm. The near-field curves to validate the woofer-box circuit.
% * *Midrange and tweeter:* their complex impedances, as measured, for the
%   passive crossover.
% * The woofer's impedance is not needed for the crossover: its crossover is
%   digital.
