%% Lecture 11 - Radiation and acoustic environment: Problems 11, worked
% 34870 Electroacoustics | 2 November 2026 | Finn Agerkvist
% 
% How to read this: every step first states the formula, then the MATLAB line 
% is that same formula typed in, and the result appears right below it.
%
% Official solutions (34870Solutions11.pdf, 3-Nov) cover Problems 1 and 2 only, and
% they agree with this script: the same network, a flat 84-85 dB of power below the
% knee, and an efficiency of about 0.3 %. One difference: the official polar plots
% use 1.5, 3 and *6* kHz, while the sheet asks for 5 kHz; this script follows the sheet.
% There is no official solution for Problem 3 (diffrac).
% 
% The sheet's header says "Problems 10"; it is the sheet filed with lecture 
% 11 (34870-Problems11.pdf, dated 30-Oct). diffrac.m (Problem 3) is in this folder.
% 
% Air (from the sheet):

rho = 1.2      % air density [kg/m^3]
c = 344        % speed of sound [m/s]

% Figures for the vault note are written here when the folder exists:
imgDir = fullfile(getenv('HOME'), 'DTU', 'Obsidian', 'Courses', ...
    '34870 Electroacoustics', 'Images', 'Lecture11');
saveFigs = isfolder(fileparts(imgDir));
if saveFigs && ~isfolder(imgDir), mkdir(imgDir); end
%% The formulas used in this problem set (slides 15-22)
% *Piston in an infinite baffle, far field.* Adding up the point sources on 
% the piston gives the on-axis monopole-like term times a directivity:
% 
% $$p(r,\theta) = \frac{j\omega\rho U}{2\pi r}e^{j(\omega t-kr)}\cdot   \frac{2J_1(ka\sin\theta)}{ka\sin\theta}$$
% 
% *Directivity function* (depends on frequency and radius only through ka):
% 
% $$D(ka,\theta) = \frac{p(\theta)}{p(0)} = \frac{2J_1(ka\sin\theta)}{ka\sin\theta}$$
% 
% *Radiated power* from the volume velocity U and the real part of the radiation 
% impedance:
% 
% $$P_A = \tfrac{1}{2}\,\mathrm{Re}(Z_{A,R})\,|U|^2, \qquad   \mathrm{Re}(Z_{A,R}) 
% = \frac{\rho c}{\pi a^2}\left(1 - \frac{J_1(2ka)}{ka}\right)$$
% 
% Symbols: a piston radius [m], k = omega/c wavenumber [1/m], U volume velocity 
% [m^3/s] (Jacobsen calls it Q; the slides use U, as here), J_1 the Bessel function 
% of the first kind, order 1 (MATLAB: besselj(1, x)).
%% Problem 1 - Directivity of a 6 cm piston at 1.5, 3 and 5 kHz

a1 = 0.06                  % piston radius [m]
f1 = [1500 3000 5000]      % frequencies [Hz]
%% 
% *Size against wavelength.* The piston starts to beam once ka is about 1, and 
% the first null appears when ka sin(theta) reaches the first zero of J_1, which 
% is 3.832:
% 
% $$ka = \frac{2\pi f a}{c}$$

ka1 = 2*pi*f1*a1/c
%% 
% So 1.5 kHz is mildly directive (ka = 1.64, no null), 3 kHz is close to the 
% edge (ka = 3.29 < 3.83, still no null in front), and 5 kHz has a null and a 
% side lobe (ka = 5.48).
% 
% *Angle of the first null* (only where ka > 3.832):
% 
% $$\sin\theta_0 = \frac{3.832}{ka}$$

theta0_5k = asind(3.832/ka1(3))     % [deg]
%% 
% *-6 dB half-angle.* D = 0.5 when the argument x = ka sin(theta) solves 2J_1(x)/x 
% = 0.5, i.e. x = 2.215:

x6 = fzero(@(x) 2*besselj(1,x)./x - 0.5, 2)
theta6 = asind(min(x6./ka1, 1))     % [deg], 90 means "never down 6 dB"
%% 
% *Directivity on a grid of angles.* sin(theta) = 0 at the front gives 0/0; 
% the limit is 1, so a tiny offset avoids the NaN:

theta = linspace(-pi/2, pi/2, 721);           % front half-plane (baffle)
x = ka1(:) * sin(theta) + eps;                % rows = frequencies
D = 2*besselj(1, x)./x;
DdB = 20*log10(abs(D));
%% 
% *Polar plot.* As the sheet hints, a negative dB value as a radius flips the 
% plot. Choose a dynamic range (40 dB) and plot DdB + 40, clipped at 0:

range = 40;
R = max(DdB + range, 0);
fig1 = figure('Name', 'L11_P1_directivity');
theme(fig1, 'light');
polarplot(theta, R, 'LineWidth', 1.5);      % one line per row of R
ax = gca;
ax.ThetaZeroLocation = 'top'; ax.ThetaLim = [-90 90];
ax.RLim = [0 range]; ax.RTick = 0:10:range;
ax.RTickLabel = string((0:10:range) - range) + " dB";
legend(compose('%.1f kHz  (ka = %.2f)', f1'/1e3, ka1'), 'Location', 'southoutside');
title('Problem 1: piston in a baffle, a = 6 cm');
if saveFigs, exportgraphics(fig1, fullfile(imgDir, 'L11_P1_directivity.png'), 'Resolution', 150); end
%% 
% Reading the plot: at 1.5 kHz the response is down only about 3 dB at 90 degrees, 
% at 3 kHz the beam narrows to +-42 degrees at -6 dB, and at 5 kHz the -6 dB beam 
% is +-24 degrees, with a null at 44 degrees and a side lobe beyond it (peak -17.6 
% dB, the classic first side lobe of a piston).

sidelobe_dB = max(DdB(3, abs(theta) > deg2rad(theta0_5k)))
%% Problem 2 - Radiated power of a baffled driver
% Given (L_E ignored):

S_D = 500e-4       % cone area, 500 cm^2 [m^2]
Bl = 10            % force factor [Tm]
R_E = 5            % coil resistance [ohm]
M_MS = 0.100       % moving mass incl. air load, 100 g [kg]
E_g = 1            % generator voltage amplitude [V]
%% 
% Equivalent piston radius:
% 
% $$a = \sqrt{S_D/\pi}$$

a = sqrt(S_D/pi)          % [m]
%% Problem 2a - Volume velocity above resonance (mass control)
% Above f_S the cone is mass controlled: the suspension spring and the damping 
% no longer matter. With L_E ignored, and the back-EMF small compared with E_g 
% in this region (checked below), the coil current is E_g/R_E and Newton gives
% 
% $$u = \frac{F}{j\omega M_{MS}} = \frac{Bl\,E_g}{j\omega M_{MS}R_E}, \qquad   
% U = S_D u = \frac{S_D\,Bl\,E_g}{j\omega\,M_{MS}\,R_E}$$
% 
% For these numbers the constant is exactly 1:

U_const = S_D*Bl*E_g/(M_MS*R_E)     % [m^3/s * rad/s], so |U| = 1/omega
%% 
% $$|U| = \frac{1}{\omega}\ \mathrm{m^3/s} \qquad\text{(1 V, above resonance)}$$
% 
% A volume velocity falling as 1/omega is a *constant volume acceleration*, 
% which is exactly what slide 9 asks for to radiate a constant power from a small 
% source.
% 
% *Check of the back-EMF assumption.* The full mass-controlled current is E_g 
% / (R_E + (Bl)^2/(j omega M_MS)); the motional term is small once omega >> (Bl)^2/(R_E 
% M_MS):

f_emf = Bl^2/(R_E*M_MS)/(2*pi)      % [Hz]
%% 
% That is 32 Hz, so the approximation is good from about 100 Hz up (at 100 Hz 
% the motional term is 0.32 R_E, which costs 0.4 dB). The 1/omega law is the textbook 
% "mass-controlled" result and the sheet asks for exactly that.
%% Problem 2b - Radiated power: exact Re(Z_AR) vs. the network

f = logspace(log10(20), log10(20000), 600);
w = 2*pi*f;
k = w/c;
U = U_const./(1j*w);                 % from 2a
%% 
% *Exact (analytical) real part* for the piston in an infinite baffle:
% 
% $$\mathrm{Re}(Z_{A,R}) = \frac{\rho c}{\pi a^2}\left(1 - \frac{J_1(2ka)}{ka}\right)$$

ReZ_exact = rho*c/(pi*a^2) * (1 - besselj(1, 2*k*a)./(k*a));
%% 
% *Network approximation* (Lecture 3, baffled piston): M_A1 in parallel with 
% [R_A2 + (R_A1 parallel C_A1)]:
% 
% $$M_{A1} = \frac{8\rho}{3\pi^2 a},\quad R_{A1} = \frac{0.441\rho c}{\pi a^2},\quad   
% R_{A2} = \frac{\rho c}{\pi a^2},\quad C_{A1} = \frac{5.94\,a^3}{\rho c^2}$$

M_A1 = 8*rho/(3*pi^2*a)
R_A1 = 0.441*rho*c/(pi*a^2)
R_A2 = rho*c/(pi*a^2)
C_A1 = 5.94*a^3/(rho*c^2)
%%
Z_RC = R_A1./(1 + 1j*w*R_A1*C_A1);           % R_A1 || C_A1
Z_net = (1j*w*M_A1 .* (R_A2 + Z_RC)) ./ (1j*w*M_A1 + R_A2 + Z_RC);
ReZ_net = real(Z_net);
%% 
% *Power* with both:
% 
% $$P_A = \tfrac{1}{2}\,\mathrm{Re}(Z_{A,R})\,|U|^2$$

P_exact = 0.5*ReZ_exact.*abs(U).^2;
P_net = 0.5*ReZ_net.*abs(U).^2;
%% 
% *Low-frequency limit.* For ka << 1, 1 - J_1(2ka)/(ka) is about (ka)^2/2, so 
% Re(Z_AR) is about rho omega^2/(2 pi c): twice the free-field monopole of slide 
% 9, because the baffle confines the power to a half-space. With |U| = 1/omega 
% the omegas cancel:
% 
% $$P_{A,LF} = \frac{1}{2}\cdot\frac{\rho\omega^2}{2\pi c}\cdot\frac{1}{\omega^2} 
% = \frac{\rho}{4\pi c}$$

P_LF = rho/(4*pi*c)               % [W], flat
P_LF_dB = 10*log10(P_LF/1e-12)    % [dB re 1 pW]
%% 
% *High-frequency limit.* For ka >> 1, Re(Z_AR) tends to rho c/S_D (a plane 
% wave over the cone area) and the power falls as 1/omega^2, i.e. 6 dB/octave. 
% The knee is where the two asymptotes meet:
% 
% $$\frac{\rho\omega^2}{2\pi c} = \frac{\rho c}{\pi a^2} \;\Rightarrow\; ka 
% = \sqrt{2}$$

f_knee = sqrt(2)*c/(2*pi*a)       % [Hz]
%%
fig2 = figure('Name', 'L11_P2_power');
theme(fig2, 'light');
semilogx(f, 10*log10(P_exact/1e-12), 'LineWidth', 1.6); hold on
semilogx(f, 10*log10(P_net/1e-12), '--', 'LineWidth', 1.6);
yline(P_LF_dB, ':', 'rho/(4 pi c)');
xline(f_knee, ':', sprintf('ka = sqrt 2 (%.0f Hz)', f_knee));
hold off; grid on
xlabel('Frequency [Hz]'); ylabel('P_A [dB re 1 pW]');
legend('exact Re(Z_{AR}) (Bessel)', 'network M_{A1}, R_{A1}, R_{A2}, C_{A1}', 'Location', 'southwest');
title('Problem 2b: radiated power, 1 V, mass-controlled region');
xlim([20 20000]); ylim([P_LF_dB-50 P_LF_dB+5]);
if saveFigs, exportgraphics(fig2, fullfile(imgDir, 'L11_P2_power.png'), 'Resolution', 150); end
%% 
% *How close is the network?* Largest dB difference, below and above the knee:

dP = 10*log10(P_net./P_exact);
max_dev_below_knee = max(abs(dP(f < f_knee)))   % [dB]
max_dev_overall = max(abs(dP))                  % [dB]
%% 
% The network is a smooth fit: it has the right low- and high-frequency asymptotes 
% and is within a fraction of a dB through the knee, but it cannot reproduce the 
% small ripple of the exact curve above ka = 2 (the J_1(2ka) oscillation). For 
% a loudspeaker model that ripple is irrelevant.
%% Problem 2c - Efficiency
% Electrical input power: in the mass-controlled region the current is E_g/R_E 
% and all input power is dissipated in R_E:
% 
% $$P_E = \frac{1}{2}\frac{E_g^2}{R_E}$$

P_E = 0.5*E_g^2/R_E               % [W]
%% 
% Efficiency, in the flat (low-frequency, mass-controlled) region:
% 
% $$\eta_0 = \frac{P_{A}}{P_E} = \frac{\rho\,(Bl)^2 S_D^2}{2\pi c\,R_E\,M_{MS}^2}$$

eta0 = P_LF/P_E
eta0_formula = rho*Bl^2*S_D^2/(2*pi*c*R_E*M_MS^2)
eta0_percent = 100*eta0
%% 
% About 0.28 %: typical for a direct-radiator woofer (0.1-1 %). The formula 
% is the reference efficiency of Lecture 7. Above the knee the efficiency falls 
% with the power, 6 dB/octave:

eta = P_exact/P_E;
fig3 = figure('Name', 'L11_P2_efficiency');
theme(fig3, 'light');
semilogx(f, 100*eta, 'LineWidth', 1.6); grid on
xlabel('Frequency [Hz]'); ylabel('\eta [%]');
title(sprintf('Problem 2c: efficiency, \\eta_0 = %.3f %%', eta0_percent));
xlim([20 20000]);
%% Problem 3 - Cabinet diffraction with diffrac.m (slides 29-39)
% diffrac(corners, r, angles, source_radius, fs) implements Terai's thin- baffle 
% model of slide 32: the direct sound from the source plus a line of edge sources 
% along the baffle rim, each delayed by its path and with a sign inversion. It 
% returns dB re the free field: an infinite baffle would be +6 dB at all frequencies. 
% (It uses c = 343 m/s internally.)
% 
% *Hand prediction for the centred circle, on axis.* Every edge point is at 
% the same distance, so the whole rim arrives at once and the effect is strongest. 
% The extra path of the diffracted wave is
% 
% $$\Delta = R + \sqrt{r^2 + R^2} - r$$
% 
% and because the edge inverts the wave, the diffracted wave *adds* when Delta 
% = lambda/2 (and 3/2, 5/2 ...) and *cancels* when Delta = lambda:

R_b = 0.30                         % baffle radius [m]
r_obs = 2                          % observation distance [m]
Delta = R_b + sqrt(r_obs^2 + R_b^2) - r_obs   % [m]
f_max1 = 343/(2*Delta)             % first peak [Hz]
f_min1 = 343/Delta                 % first dip [Hz]
%% 
% Below about f_max1/2 the baffle is too small to matter: the response sits 
% near 0 dB (free field, the sound wraps round). Well above, it oscillates around 
% +6 dB (the baffle step).
%% Problem 3a - Point source in the centre of a 30 cm circular baffle
% A circle is a polygon with many corners (the help asks for > 100). source_radius 
% = 1 mm makes it effectively a monopole:

phi = linspace(0, 2*pi, 201)';
circ = [R_b*cos(phi) R_b*sin(phi)];
angles3 = [0 0; 30 0; 60 0];       % [azimuth elevation] in degrees
[t3, h3, f3, H3] = diffrac(circ, r_obs, angles3, 0.001, 44100);
%% 
% diffrac draws its own figures (edge/source geometry, then impulse and frequency 
% response per angle). The three angles together:

fig4 = figure('Name', 'L11_P3a_circle');
theme(fig4, 'light');
semilogx(f3, H3, 'LineWidth', 1.3); grid on
xline([f_max1 f_min1], ':', {'\Delta = \lambda/2', '\Delta = \lambda'});
xlabel('Frequency [Hz]'); ylabel('dB re free field');
legend('0^\circ (on axis)', '30^\circ', '60^\circ', 'Location', 'northwest');
title('Problem 3a: monopole in the centre of a circular baffle, R = 30 cm, r = 2 m');
xlim([50 20000]); ylim([-10 14]);
if saveFigs, exportgraphics(fig4, fullfile(imgDir, 'L11_P3a_circle.png'), 'Resolution', 150); end
%% 
% Read off the on-axis peak and dip and compare with the hand prediction:

band = f3 > 200 & f3 < 3000;
fb = f3(band); Hb = H3(band, 1);
[pk, ipk] = max(Hb); f_pk = fb(ipk)
pk_dB = pk
[dp, idp] = min(Hb(fb > f_pk)); fbb = fb(fb > f_pk); f_dp = fbb(idp)
dp_dB = dp
%% 
% * *On axis* the edge contributions all arrive together, so the ripple is large: 
% a peak of +9.9 dB at Delta = lambda/2 (538 Hz) and a dip to -1.3 dB at Delta 
% = lambda (1.08 kHz), 11 dB below the peak, repeating up the band around the 
% +6 dB baffle step (slide 31).
% * *At 30 and 60 degrees* the path to each edge point is different, the diffracted 
% arrivals smear out over time, and the ripple shrinks. Off axis is smoother: 
% the symmetric, centred source is the worst case for the on-axis response.
%% Problem 3b - Source off centre
% diffrac always puts the source at (0,0), so moving the source is done by moving 
% the baffle the other way. Shift the circle by 10 cm in x and 5 cm in y:

offset = [0.10 0.05]
[~, ~, fb3, Hoff] = diffrac(circ + offset, r_obs, angles3, 0.001, 44100);
%%
fig5 = figure('Name', 'L11_P3b_offset');
theme(fig5, 'light');
semilogx(f3, H3(:,1), 'LineWidth', 1.3); hold on
semilogx(fb3, Hoff, 'LineWidth', 1.3); hold off; grid on
xlabel('Frequency [Hz]'); ylabel('dB re free field');
legend('centred, 0^\circ', 'offset, 0^\circ', 'offset, 30^\circ', 'offset, 60^\circ', 'Location', 'northwest');
title('Problem 3b: source 11 cm off centre on the same circle');
xlim([50 20000]); ylim([-10 14]);
if saveFigs, exportgraphics(fig5, fullfile(imgDir, 'L11_P3b_offset.png'), 'Resolution', 150); end
%% 
% The edge distances now range from 19 to 41 cm, so the diffracted wave is spread 
% out in time and the deep on-axis notches are filled in. The step from 0 to +6 
% dB is still there (the baffle is the same size), but the ripple on top is halved 
% (11.2 -> 5.1 dB, 300 Hz-5 kHz): this is why drivers are placed off centre (slide 
% 40, "asymmetric driver placement").

ripple_centred = max(H3(f3>300 & f3<5000,1)) - min(H3(f3>300 & f3<5000,1))   % [dB]
ripple_offset = max(Hoff(fb3>300 & fb3<5000,1)) - min(Hoff(fb3>300 & fb3<5000,1)) % [dB]
%% Problem 3c - Your own baffle shapes
% Two typical cabinet fronts, same source (a 5 cm piston rather than a point, 
% like a real tweeter/midrange), on axis:
%% 
% * a 20 x 35 cm rectangle with the driver centred left-right and 7.5 cm above 
% the middle (the typical "two-way" front),
% * the same rectangle with the driver also 3 cm off the left-right centre,
% * the same outline with 5 cm chamfered corners (a cheap way to soften the 
% edges).

W = 0.20; Hh = 0.35; yoff = 0.075; xoff = 0.03;
rect = [ W/2  Hh/2;  W/2 -Hh/2; -W/2 -Hh/2; -W/2  Hh/2];
ch = 0.05;
cham = [ W/2 Hh/2-ch;  W/2 -Hh/2+ch;  W/2-ch -Hh/2; -W/2+ch -Hh/2; ...
        -W/2 -Hh/2+ch; -W/2  Hh/2-ch; -W/2+ch Hh/2;  W/2-ch Hh/2];
shapes = {rect - [0 yoff], rect - [xoff yoff], cham - [xoff yoff]};
names = {'rectangle, centred in x', 'rectangle, 3 cm off in x', 'chamfered, 3 cm off in x'};
[~, ~, fs3, H_rect] = diffrac(shapes{1}, r_obs, [0 0], 0.025, 44100);
[~, ~, ~, H_off] = diffrac(shapes{2}, r_obs, [0 0], 0.025, 44100);
[~, ~, ~, H_cham] = diffrac(shapes{3}, r_obs, [0 0], 0.025, 44100);
Hs = [H_rect H_off H_cham];
%%
fig6 = figure('Name', 'L11_P3c_shapes');
theme(fig6, 'light');
semilogx(fs3, Hs, 'LineWidth', 1.3); grid on
xlabel('Frequency [Hz]'); ylabel('dB re free field');
legend(names, 'Location', 'northwest');
title('Problem 3c: 20 x 35 cm front, 5 cm piston, on axis, r = 2 m');
xlim([100 20000]); ylim([-10 14]);
if saveFigs, exportgraphics(fig6, fullfile(imgDir, 'L11_P3c_shapes.png'), 'Resolution', 150); end
%% 
% What to look for: the narrow front puts the baffle step higher (about c/(pi 
% W) to c/(pi H), several hundred Hz) than the 60 cm circle. Moving the driver 
% off the left-right symmetry line makes the two side edges arrive at different 
% times and reduces the ripple. Chamfers barely help in this thin-baffle model, 
% because the edge is still a sharp line of sources; real roundovers work by making 
% the edge *gradual* over a distance comparable with the wavelength (slide 40), 
% which diffrac cannot represent. Result: ripple 3.4 dB centred, 2.8 dB off centre, 
% 2.8 dB chamfered (500 Hz-8 kHz): the offset helps, the chamfer does not.

mid = fs3>500 & fs3<8000;
ripple_shapes = max(Hs(mid,:)) - min(Hs(mid,:))   % [dB] rect, offset, chamfered