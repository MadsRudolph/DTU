%% Lecture 10 - Physiological Acoustics
% 34840 Fundamentals of Acoustics and Noise Control | 10 November 2026
%
% Worked learning document for 34840_Physiological_Acoustics_Exercise_2026.pdf
% (Torsten Dau). Every formula is first written as an equation, then
% calculated in one plain MATLAB line. Lines without a semicolon print
% their result.
%
% Official solutions: 34840_Physiological_Acoustics_Solutions_2026.pdf.
% The official answer is written in the comment next to each result.
%
% Bonus section at the end: outer- and middle-ear numbers from the course
% text (ch. 2.2), which the exercise does not ask for but the exam can.
%
% Figures go to the vault Images/Lecture10/ folder.

%% Problem 1 - Greenwood place-frequency map, cochlea 34 mm long
% Location x is measured from the base (stapes end) IN METRES.
%
% $$F_c(x) = A\cdot10^{-Gx} - B,\quad A = 20682,\ G = 61.765\ \mathrm{m^{-1}},\ B = 140.6$$
A = 20682; G = 61.765; B = 140.6;
L_cochlea = 0.034;                        % cochlear length [m]
F_high = A*10^(-G*0) - B                  % 20541 Hz at the base, x = 0 (official: 20541 Hz)
F_low = A*10^(-G*L_cochlea) - B           % 23.7 Hz at the apex, x = 34 mm (official: 24 Hz)
%
% Inverse map, used in Problem 3 and handy for the exam:
% $$x = -\frac{1}{G}\log_{10}\frac{F_c + B}{A}$$
x_1kHz_mm = -log10((1000 + B)/A)/G*1e3    % 1 kHz sits 20.4 mm from the base
x_4kHz_mm = -log10((4000 + B)/A)/G*1e3    % 4 kHz sits 11.3 mm from the base

%% Problem 2a - SNR of one ABR sweep, and what doubling n does
EP = 0.3e-6;                              % evoked potential [V]
N = 3e-6;                                 % background noise per sweep [V]
rate = 20;                                % sweeps per second
%
% $$\mathrm{SNR}_1 = \frac{EP}{N},\qquad \mathrm{SNR}_{1,\mathrm{dB}} = 20\log_{10}\frac{EP}{N}$$
SNR1 = EP/N                               % 0.1 (official: 0.1)
SNR1_dB = 20*log10(SNR1)                  % -20 dB (official: -20 dB)
%
% Averaging: $\bar N = N/\sqrt n$, so $\mathrm{SNR}_{avg} = \mathrm{SNR}_1\sqrt n$.
% $$\Delta = 20\log_{10}(\mathrm{SNR}_1\sqrt{2n}) - 20\log_{10}(\mathrm{SNR}_1\sqrt{n}) = 10\log_{10}2$$
dSNR_double_dB = 10*log10(2)              % +3.01 dB per doubling (official: +3.01 dB)

%% Problem 2b - Sweeps and time for SNR_avg = +10 dB
% $$n = \left(\frac{10^{\mathrm{SNR_{target,dB}}/20}}{\mathrm{SNR}_1}\right)^2$$
SNR_target_dB = 10;
n_b = (10^(SNR_target_dB/20)/SNR1)^2      % 1000 sweeps (official: 1000)
t_b = n_b/rate                            % 50 s (official: 50 s)

%% Problem 2c - 10 % artifact sweeps with 10x the noise
% Independent noise: POWERS add, not amplitudes.
% $$P = \frac{n_1N_1^2 + n_2N_2^2}{n_1+n_2},\qquad N_{\rm eff} = \sqrt P$$
n_c = 1000; N1 = 3e-6; N2 = 30e-6;
P = (0.9*n_c*N1^2 + 0.1*n_c*N2^2)/n_c     % 9.81e-11 V^2 = 98.1 uV^2 (official: 98.1 uV^2)
N_eff = sqrt(P)                           % 9.905 uV (official: 9.905 uV)
%
% $$\bar N = \frac{N_{\rm eff}}{\sqrt n},\qquad \mathrm{SNR}_{avg} = 20\log_{10}\frac{EP}{\bar N}$$
Nbar_c = N_eff/sqrt(n_c)                  % 0.3132 uV (official: 0.3132 uV)
SNR_c_dB = 20*log10(EP/Nbar_c)            % -0.37 dB (official: -0.37 dB)
%
% Without rejection, the residual noise must reach $N_{target} = EP/10^{10/20}$:
% $$n = \frac{P}{N_{target}^2}$$
N_target = EP/10^(SNR_target_dB/20)       % 0.0949 uV (official: 0.0949 uV)
n_noRej = P/N_target^2                    % 10 900 sweeps (official: 10 900)
t_noRej = n_noRej/rate                    % 545 s (official: 545 s)
%
% With rejection: only clean sweeps are averaged, but 10 % are thrown away.
% $$n_{clean} = \left(\frac{N_1}{N_{target}}\right)^2,\qquad n_{total} = \frac{n_{clean}}{0.9}$$
n_clean = (N1/N_target)^2                 % 1000 (official: 1000)
n_rej = n_clean/0.9                       % 1111 sweeps (official: 1111)
t_rej = n_rej/rate                        % 55.6 s (official: 55.6 s)
time_ratio = t_noRej/t_rej                % 9.81 (official: 9.8)
%
% Same thing in dB: the artifacts raise the noise power by 10*log10(P/N1^2).
noise_penalty_dB = 10*log10(P/N1^2)       % 10.4 dB more noise power -> 10.9x the sweeps

%% Problem 3 - CEOAE roundtrip times -> cochlear place -> frequency
% Roundtrip = forward + backward, so the forward trip is half of it.
% $$x = c_{BM}\,\frac{t_{rt}}{2},\qquad c_{BM} = 3\ \mathrm{m/s}$$
c_BM = 3;
t_rt = [12 7 5]*1e-3;                     % roundtrip times [s]
x_oae = c_BM*t_rt/2                       % 0.018, 0.0105, 0.0075 m (official: same)
%
% $$F = A\cdot10^{-Gx} - B$$
F_oae = A*10.^(-G*x_oae) - B              % 1458.3, 4505.2, 6977.4 Hz (official: 1458.3, 4505.2, 6977.4 Hz)

%% Bonus (course text 2.2) - outer and middle ear
% Ear canal = tube closed at the ear drum, open at the entrance: quarter-wave resonator.
% $$f_{res} = \frac{c}{4L}$$
f_canal = 340/(4*0.025)                   % 3400 Hz (course text: 3.4 kHz, c = 340, L = 25 mm)
%
% Air -> water at normal incidence, no middle ear (Lecture 2):
% $$\tau = \frac{4 Z_1 Z_2}{(Z_1+Z_2)^2}$$
Z_air = 1.2*343;                          % 411.6 Pa s/m
Z_water = 1000*1480;                      % 1.48e6 Pa s/m
tau = 4*Z_air*Z_water/(Z_air + Z_water)^2 % 1.11e-3: only 0.1 % of the power gets in
TL_air_water_dB = -10*log10(tau)          % 29.5 dB lost
%
% Middle ear transformer: lever 1.3 x area ratio 14.
% $$\frac{p_{oval}}{p_{drum}} = \frac{A_{drum}}{A_{footplate}}\cdot\frac{l_1}{l_2}$$
ratio_middle_ear = 14*1.3                 % 18.2 (course text: 18)
gain_middle_ear_dB = 20*log10(ratio_middle_ear) % 25.2 dB (course text: approx. 25 dB)

%% Figures (headless, light theme) -> vault Images/Lecture10/
outdir = fullfile(getenv('HOME'), 'DTU', 'Obsidian', 'Courses', ...
    '34840 Fundamentals of Acoustics and Noise Control', 'Images', 'Lecture10');
if ~exist(outdir, 'dir'); mkdir(outdir); end

x_mm = linspace(0, 34, 500);
fig1 = figure('Visible', 'off', 'Position', [100 100 760 420]);
theme(fig1, 'light');
semilogy(x_mm, A*10.^(-G*x_mm/1e3) - B, 'LineWidth', 1.6); hold on; grid on;
semilogy(x_oae*1e3, F_oae, 'o', 'MarkerSize', 8, 'LineWidth', 1.5);
text(x_oae*1e3 + 0.6, F_oae*1.15, {'P3: 12 ms', 'P3: 7 ms', 'P3: 5 ms'});
semilogy([0 34], [F_high F_low], 's', 'MarkerSize', 8, 'LineWidth', 1.5);
text(0.6, F_high*0.75, '20.5 kHz (base)');
text(27, F_low*1.6, '24 Hz (apex)');
xlabel('Distance from the base x (mm)'); ylabel('Characteristic frequency (Hz)');
title('Greenwood map, F = 20682·10^{-61.765x} - 140.6 (x in m)');
ylim([15 3e4]);
exportgraphics(fig1, fullfile(outdir, 'greenwood_map.png'), 'Resolution', 150);

n_axis = logspace(0, 4.5, 300);
fig2 = figure('Visible', 'off', 'Position', [100 100 760 420]);
theme(fig2, 'light');
semilogx(n_axis, 20*log10(EP./(N1./sqrt(n_axis))), 'LineWidth', 1.6); hold on; grid on;
semilogx(n_axis, 20*log10(EP./(N_eff./sqrt(n_axis))), 'LineWidth', 1.6);
yline(10, '--', '+10 dB target');
semilogx([n_b n_noRej], [10 10], 'o', 'MarkerSize', 8, 'LineWidth', 1.5);
xlabel('Number of averaged sweeps n'); ylabel('SNR after averaging (dB)');
legend('clean sweeps, N = 3 \muV', '10 % artifacts, N_{eff} = 9.9 \muV', 'Location', 'northwest');
title('Averaging gains 10log_{10}2 = 3 dB per doubling of n');
exportgraphics(fig2, fullfile(outdir, 'abr_averaging_snr.png'), 'Resolution', 150);
