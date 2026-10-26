%% Lab E - Loudspeaker response in free field, worked through our own data
% 34870 Electroacoustics | Group 10, System D, measured 20 October 2026
%
% How to read this: every step states the formula first, the MATLAB line is
% that same formula typed in, and the result appears right below it.
%
% The data are in the labs repo (Labs/Lab E/data/). Each file holds fn
% (frequency) and H = p/V in Pa/V (pressure at the UMIK over the sound
% card's line-out voltage). The system files hold three columns of H:
% woofer, midrange, tweeter, measured in ONE run.
%
% Run this from the Matlab folder (5. Semester/Electroacoustics/Matlab).
% diffrac.m is in this folder.
D = fullfile('..', 'Labs', 'Lab E', 'data');
box0 = load(fullfile(D, 'labE_box_0.mat'));        % 3" driver in its small box
box30 = load(fullfile(D, 'labE_box_30.mat'));
cir0 = load(fullfile(D, 'labE_circle_0.mat'));     % on the circular screen, centred
cir30 = load(fullfile(D, 'labE_circle_30.mat'));
iec0 = load(fullfile(D, 'labE_iec_0.mat'));        % on the IEC screen, off-centre
iec15 = load(fullfile(D, 'labE_iec_15.mat'));
iec30 = load(fullfile(D, 'labE_iec_30.mat'));
iec60 = load(fullfile(D, 'labE_iec_60.mat'));
sys0 = load(fullfile(D, 'labE_system_0.mat'));     % System D, vent plugged
sys30 = load(fullfile(D, 'labE_system_30.mat'));
%%
c = 343.2      % speed of sound at the measured 20 C (m/s)
r = 2.44       % microphone distance (m)
%%
% Above 18.4 kHz the UMIK channel jumps by about 20 dB in every run (a
% microphone artefact, not the speakers), so every plot stops at 18 kHz.
% The frequency vector is the same in all Part 1 files:
f = box0.fn;

%% Part 1 - One driver, three mountings
figure('Name', 'labE_fig1_mountings');
subplot(2,1,1);
semilogx(f, 20*log10(abs(box0.H)), f, 20*log10(abs(cir0.H)), f, 20*log10(abs(iec0.H)), 'LineWidth', 1.4);
grid on; xlim([50 18000]); ylim([-35 20]);
ylabel('|p/V| (dB re 1 Pa/V)');
legend('small box', 'circular screen, centred', 'IEC screen, off-centre', 'Location', 'south');
title('3" driver at 2.44 m, 0\circ');
subplot(2,1,2);
semilogx(f, 20*log10(abs(box30.H)), f, 20*log10(abs(cir30.H)), f, 20*log10(abs(iec30.H)), 'LineWidth', 1.4);
grid on; xlim([50 18000]); ylim([-35 20]);
xlabel('Frequency (Hz)'); ylabel('|p/V| (dB re 1 Pa/V)');
title('30\circ');
%%
% *No phase here, on purpose.* The UMIK is a USB microphone with its own
% clock, and every run starts with a random delay between the sound card's
% output and the microphone. So the absolute phase of a single run means
% nothing. (In Part 2 the three units are measured in ONE run, so their
% phase DIFFERENCES are valid.) Say this once in the quiz: the graders
% want phase on every complex quantity, unless you explain why not.
%
% *Three things to see:*
%
% # Below about 150 Hz all three fall together: that is the driver's own
%   resonance and the anechoic chamber running out, not the baffle.
% # The small box sits about 6 dB under the screens at 250-600 Hz (the
%   baffle step, next section).
% # The circular screen has deep, regular dips (1.06 and 2.1 kHz); the IEC
%   screen is much smoother.

%% Part 1 - The baffle step
% A source in a big baffle radiates into half space (2 pi); the baffle acts
% like a mirror, adding an image source right on top of the real one. For
% the same cone movement (volume velocity) that doubles the pressure:
% +6 dB compared with a source radiating into full space (4 pi). At low
% frequency the small box's front is much smaller than the wavelength, so
% it is "no baffle", while the screens are "a baffle": we expect up to
% 6 dB between them.
k = f > 250 & f < 600;
step_dB = mean(20*log10(abs(cir0.H(k)))) - mean(20*log10(abs(box0.H(k))))
k = f > 3000 & f < 8000;
high_dB = mean(20*log10(abs(cir0.H(k)))) - mean(20*log10(abs(box0.H(k))))
%%
% About 6 dB at 250-600 Hz (5.7 dB averaged over both screens), about 0 dB
% above 3 kHz: at high frequency even the
% small box's front is many wavelengths wide, so it is a baffle too.

%% Part 1 - Circular screen: where the dips come from
% Every point on the screen's edge re-radiates the wave that reaches it,
% with inverted sign. With the driver in the centre, every edge point is
% a = 0.30 m from the driver, so all those edge waves arrive at the mic
% TOGETHER, a path difference Delta behind the direct wave:
%
% $$\Delta = a + \sqrt{a^2 + r^2} - r$$
a = 0.30
Delta = a + sqrt(a^2 + r^2) - r
%%
% The edge wave is inverted, so it ADDS when it is half a wavelength late
% and CANCELS when it is a whole wavelength late:
%
% $$f_{peak} = \frac{(2n-1)\,c}{2\Delta}, \qquad f_{dip} = \frac{n\,c}{\Delta}$$
f_peaks = [1 3] * c / (2*Delta)
f_dips = [1 2] * c / Delta
%%
% Find the measured first dip:
k = f > 800 & f < 1400; [Hmin, i] = min(abs(cir0.H(k))); fk = f(k);
f_dip1_measured = fk(i)
level_dB = 20*log10(Hmin)
%%
% 1059 Hz against 1078 Hz predicted (2 %), and the second dip at 2115 Hz
% against 2156. *At 30 deg* the edge points are no longer equally far
% from the mic, the edge waves arrive spread out in time, and the ripple
% smears out. *On the IEC screen* the driver is off-centre: the edges are
% between 0.20 and 0.44 m away, so the edge waves never line up. That is
% why the IEC screen is the standard baffle for measuring a driver.

%% Part 1 - diffrac.m: the circle as a model
% diffrac.m (Terai's method) puts a line of edge sources along the baffle's
% outline and adds their contributions to the direct sound. The circle is
% given as a polygon with many corners. The source is either a point (a
% tiny radius) or a piston with the driver's radius (rule of thumb for a
% 3" driver: a = 3 cm).
%
% It draws its own figures; those (and only those) are closed again.
th = linspace(0, 2*pi, 200)';
corners = [a*cos(th) a*sin(th)];
ours = findobj('Type', 'figure');
[~, ~, fd, Hpoint] = diffrac(corners, r, [0 0; 30 0], 0.001);
[~, ~, ~, Hpiston] = diffrac(corners, r, [0 0; 30 0], 0.03);
close(setdiff(findobj('Type', 'figure'), ours))
%%
% diffrac returns dB "re free field": an infinite baffle would be +6 dB
% everywhere. The measured curve also contains the driver's own response,
% so it is shifted to the model's mean level over 300 Hz - 5 kHz before
% comparing (only the SHAPE is compared):
km = f > 300 & f < 5000; kd = fd > 300 & fd < 5000;
shift_0 = mean(Hpiston(kd,1)) - mean(20*log10(abs(cir0.H(km))))
shift_30 = mean(Hpiston(kd,2)) - mean(20*log10(abs(cir30.H(km))))
%%
figure('Name', 'labE_fig2_circle_diffrac');
subplot(2,1,1);
semilogx(f, 20*log10(abs(cir0.H)) + shift_0, 'k', fd, Hpoint(:,1), fd, Hpiston(:,1), 'LineWidth', 1.3);
grid on; xlim([100 18000]); ylim([-10 15]);
ylabel('dB re free field');
legend('measured (shifted)', 'diffrac, point source', 'diffrac, piston a = 3 cm', 'Location', 'south');
title('Circular screen, 0\circ');
subplot(2,1,2);
semilogx(f, 20*log10(abs(cir30.H)) + shift_30, 'k', fd, Hpoint(:,2), fd, Hpiston(:,2), 'LineWidth', 1.3);
grid on; xlim([100 18000]); ylim([-10 15]);
xlabel('Frequency (Hz)'); ylabel('dB re free field');
title('Circular screen, 30\circ');
%%
% * The dips line up with the measurement: the model is right about WHERE
%   the diffraction is.
% * The point source keeps rippling at full strength to 20 kHz. The piston
%   ripples less and less above a few kHz, and so does the measurement. A
%   piston with ka > 1 sends little sound sideways along the baffle, so the
%   edges get less to diffract.
% * At 30 deg the piston model falls off above ~8 kHz: that is the piston's
%   own directivity (next section).

%% Part 1 - IEC screen: directivity against a piston
% Divide each off-axis curve by the 0 deg curve. The driver and the baffle
% are in both, so they cancel, and what is left is how the driver beams.
% A rigid piston in a baffle beams like:
%
% $$D(\theta) = \frac{2J_1(x)}{x}, \qquad x = ka\sin\theta = \frac{2\pi f}{c}\,a\sin\theta$$
a_s = 0.03                                  % 3" driver: radius about 3 cm
x60 = 2*pi*f/c * a_s * sind(60);
D60 = 2*besselj(1, x60) ./ x60;
x30 = 2*pi*f/c * a_s * sind(30);
D30 = 2*besselj(1, x30) ./ x30;
figure('Name', 'labE_fig3_iec_directivity');
semilogx(f, 20*log10(abs(iec15.H./iec0.H)), f, 20*log10(abs(iec30.H./iec0.H)), f, 20*log10(abs(iec60.H./iec0.H)), 'LineWidth', 1.3); hold on;
set(gca, 'ColorOrderIndex', 2);
semilogx(f, 20*log10(abs(D30)), '--', f, 20*log10(abs(D60)), '--', 'LineWidth', 1.3);
grid on; xlim([300 18000]); ylim([-40 8]);
xlabel('Frequency (Hz)'); ylabel('off-axis / on-axis (dB)');
legend('15\circ', '30\circ', '60\circ', 'piston 30\circ', 'piston 60\circ', 'Location', 'southwest');
title('IEC screen: measured beaming against a rigid piston, a = 3 cm');
%%
% Where does the piston reach -3 dB, and its first null? 2J1(x)/x = 0.707 at
% x = 1.62, and the first null is at x = 3.83:
f_3dB_60 = 1.62 * c / (2*pi*a_s*sind(60))
f_null_60 = 3.83 * c / (2*pi*a_s*sind(60))
%%
% Measured at 60 deg: -3 dB at 3.45 kHz, null at 7.96 kHz. The rigid piston
% is spot on. At 15-30 deg the measured nulls come EARLY above 10 kHz: up
% there the cone no longer moves as one rigid piece (break-up), so its
% effective size and shape change.

%% Part 2 - System D: the three units
% All three units were measured in one run (Nmeas = 3, switched between
% units during the beeps), at 0 and 30 deg, the woofer's vent plugged
% (the chamber is not anechoic at very low frequency anyway).
fs = sys0.fn;
Hw = sys0.H(:,1); Hm = sys0.H(:,2); Ht = sys0.H(:,3);
figure('Name', 'labE_fig4_system');
semilogx(fs, 20*log10(abs(Hw)), fs, 20*log10(abs(Hm)), fs, 20*log10(abs(Ht)), 'LineWidth', 1.4); hold on;
set(gca, 'ColorOrderIndex', 1);
semilogx(fs, 20*log10(abs(sys30.H(:,1))), ':', fs, 20*log10(abs(sys30.H(:,2))), ':', fs, 20*log10(abs(sys30.H(:,3))), ':', 'LineWidth', 1.2);
xline(2600, '--', 'DALI crossover 2.6 kHz', 'LabelVerticalAlignment', 'bottom');
grid on; xlim([50 18000]); ylim([-50 20]);
xlabel('Frequency (Hz)'); ylabel('|p/V| (dB re 1 Pa/V)');
legend('woofer 0\circ', 'midrange 0\circ', 'tweeter 0\circ', 'woofer 30\circ', 'midrange 30\circ', 'tweeter 30\circ', 'Location', 'southwest', 'NumColumns', 2);
title('System D at 2.44 m, solid 0\circ, dotted 30\circ');
%%
% Average levels in the bands that matter:
k = fs > 150 & fs < 600;
woofer_low = mean(20*log10(abs(Hw(k))))
mid_low = mean(20*log10(abs(Hm(k))))
k = fs > 1000 & fs < 3000;
mid_band = mean(20*log10(abs(Hm(k))))
tweeter_band = mean(20*log10(abs(Ht(k))))
%%
% *Beaming.* A piston starts to beam when the wavelength gets as small as
% its circumference, ka = 1:
%
% $$f_{ka=1} = \frac{c}{2\pi a}$$
a_units = [0.211 0.105 0.025] / 2;          % woofer, midrange, tweeter radius (m)
f_ka1 = c ./ (2*pi*a_units)
%%
% Woofer 520 Hz, midrange 1.04 kHz, tweeter 4.4 kHz. And the measurement:
k = fs > 3000 & fs < 8000;
beaming_30_dB = mean(20*log10(abs(sys30.H(k,:)))) - mean(20*log10(abs(sys0.H(k,:))))
%%
% Woofer -15.6 dB, midrange -7.5 dB, tweeter -0.7 dB at 30 deg in 3-8 kHz.
% The woofer must hand over well before it beams; the tweeter barely beams.
%
% *What the curves say about the crossover:*
%
% * The tweeter is about 9 dB louder than the midrange in its band, so the
%   crossover must attenuate it by about 9 dB.
% * The tweeter and the midrange cross near 950 Hz, but the tweeter's
%   resonance is at 1.45 kHz (Lab D impedance). Crossing at 950 Hz would
%   drive it at and below its resonance, with large excursion. A crossover
%   around 2.5-3 kHz keeps an octave of margin. DALI's own crossover for
%   this box is at 2.6 kHz.
% * The woofer to midrange crossover goes well below 1.5 kHz (the woofer
%   beams above that, and has break-up peaks at 2.5-3 kHz).

%% Part 2 - Phase: removing the delay
% Each measured phase contains three things:
%
% $$\varphi_{meas} = \varphi_{unit} - 2\pi f\,\tau, \qquad \tau = \frac{\text{flight distance}}{c} + \text{card delay}$$
%
% The delay tau is a phase that grows linearly with f and wraps hundreds of
% times. The course's phaseunwrap.m removes it with a distance d, then
% unwraps:
%
% $$\varphi_{comp} = \varphi_{meas} + 2\pi f\,\frac{d}{c}$$
%
% (phaseunwrap.m uses c = 345 and draws into the current figure, so here
% the same formula is typed in.) One d is used for ALL three units, found
% as the value that makes the three phases flattest. Here d = -1.15 m:
% negative, because the card delay in this run was SHORTER than the flight
% time, so "distance" here is not a physical distance.
d = -1.15
phi_w = rad2deg(unwrap(angle(Hw) + 2*pi*fs*d/345));
phi_m = rad2deg(unwrap(angle(Hm) + 2*pi*fs*d/345));
k_t = fs > 515;                      % the tweeter is only noise below ~500 Hz
phi_t = rad2deg(unwrap(angle(Ht(k_t)) + 2*pi*fs(k_t)*d/345));
%%
% Unwrapping fixes the phase only up to whole turns (360 deg). Shift the
% woofer and the tweeter by whole turns so that all three sit close
% together at 1 kHz; that changes nothing physical.
phi_w = phi_w - 360*round((interp1(fs, phi_w, 1000) - interp1(fs, phi_m, 1000))/360);
phi_t = phi_t - 360*round((interp1(fs(k_t), phi_t, 1000) - interp1(fs, phi_m, 1000))/360);
%%
% *Why the tweeter phase goes wild below 500 Hz:* there it is 30-50 dB down,
% in the noise, and the phase of noise is random. unwrap works upwards from
% the lowest frequency, so every random jump there adds a whole turn
% (360 deg) to the ENTIRE rest of the curve. Unwrap only inside the band
% where the unit actually plays.
%
% *The cleaner way:* the RELATIVE phase between two units in the same run.
% The delay is the same for both, so it cancels, and nothing needs to be
% unwrapped or compensated:
%
% $$\Delta\varphi = \angle\frac{H_a}{H_b} = \varphi_a - \varphi_b$$
rel_wm = rad2deg(angle(Hw ./ Hm));
rel_tm = rad2deg(angle(Ht ./ Hm));
at300 = [interp1(fs, rel_wm, 300) interp1(fs, rel_tm, 300)]
at3000 = [interp1(fs, rel_wm, 3000) interp1(fs, rel_tm, 3000)]
%%
figure('Name', 'labE_fig5_phase');
subplot(2,1,1);
semilogx(fs, phi_w, fs, phi_m, fs(k_t), phi_t, 'LineWidth', 1.3);
grid on; xlim([50 18000]);
ylabel('phase (\circ)');
legend('woofer', 'midrange', 'tweeter (> 515 Hz)', 'Location', 'northwest');
title('Phase after compensation, d = -1.15 m for all three');
subplot(2,1,2);
k = fs > 100 & fs < 4000;
semilogx(fs(k), rel_wm(k), fs(k_t & fs < 10000), rel_tm(k_t & fs < 10000), 'LineWidth', 1.3);
xline(2600, '--', '2.6 kHz');
grid on; xlim([50 18000]); ylim([-180 180]); yticks(-180:90:180);
xlabel('Frequency (Hz)'); ylabel('relative phase (\circ)');
legend('woofer - midrange', 'tweeter - midrange', 'Location', 'southwest');
title('Relative phase: every common delay cancels');
%%
% * *Woofer - midrange:* -12 deg at 300 Hz. They are nearly in phase where
%   they will cross, with the woofer's acoustic centre a little further
%   back.
% * *Tweeter - midrange:* +163 deg at 300 Hz, +76 deg at 3 kHz. Below its
%   resonance a tweeter acts as a second-order high-pass, which gives up to
%   +180 deg. Near the crossover it is about 90 deg ahead.
% * So the crossover cannot just assume the units are in phase: the filter
%   orders and the tweeter's polarity are chosen against THIS curve, so that
%   the two outputs add instead of cancelling around 2.6 kHz.

%% What goes to the project
% * The magnitude AND phase of each unit at the listening position (0 deg),
%   in one run, for the crossover design.
% * The tweeter needs about 9 dB of attenuation; the mid/tweeter crossover
%   belongs around 2.5-3 kHz; the woofer hands over well below 1.5 kHz.
% * Below about 100 Hz Lab E is not valid (chamber, plugged vent): the woofer
%   box's low end comes from Lab D's near-field measurements.
