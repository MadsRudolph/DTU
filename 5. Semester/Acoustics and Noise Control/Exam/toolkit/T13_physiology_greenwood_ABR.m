%% T13 - Physiological acoustics: Greenwood map, OAE latency, ABR averaging, ear numbers
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: characteristic frequency at a place on the basilar membrane (and
% the reverse), OAE roundtrip time -> place -> frequency, ABR signal
% averaging (SNR per sweep, sweeps and time needed, artifacts with and
% without rejection), ear-canal resonance, middle-ear gain, air-water loss.
%
% Matches: Physiological Acoustics exercise (Week 10), all pre-filled:
% P1 20541 Hz at the base, 23.7 Hz at the apex; P2 SNR -20 dB, +3.01 dB
% per doubling, 1000 sweeps / 50 s, artifacts 10 900 sweeps / 545 s,
% rejection 1111 sweeps / 55.6 s; P3 7.5/10.5/18 mm -> 6977/4505/1458 Hz.

%% A - Greenwood map (exercise form: x from the BASE, in METRES)
% $$F_c(x) = A\,10^{-Gx} - B,\qquad x = -\frac{1}{G}\log_{10}\frac{F_c+B}{A}$$
A = 20682;  G = 61.765;  B = 140.6;      % GIVEN constants (G per metre)
L_cochlea = 0.034;                       % GIVEN length [m]
F_base = A*10^(-G*0) - B                 % 20541 Hz (official)
F_apex = A*10^(-G*L_cochlea) - B         % 23.7 Hz (official)
f_query = 1000;                          % GIVEN frequency [Hz]
x_of_f_mm = -1/G*log10((f_query + B)/A)*1000   % 20.4 mm from the base
mm_per_octave = log10(2)/G*1000          % ~4.9 mm where B is negligible

%% B - OAE: roundtrip time -> place -> frequency
% $$x = c_{BM}\frac{t_{rt}}{2}$$  (halve the roundtrip!)
c_BM = 3;                                % GIVEN travelling-wave speed [m/s]
t_rt = [12 7 5]*1e-3;                    % GIVEN roundtrip times [s]
x_oae = c_BM*t_rt/2                      % 18, 10.5, 7.5 mm
F_oae = A*10.^(-G*x_oae) - B             % 1458.3 4505.2 6977.4 Hz (official)
% DPOAE frequency for primaries f1 < f2: 2 f1 - f2.
f_dp = 2*2000 - 2400                     % 1600 Hz

%% C - ABR averaging
% $$\mathrm{SNR}_1 = 20\log_{10}\frac{EP}{N},\qquad \mathrm{SNR}_n = \mathrm{SNR}_1 + 10\log_{10}n$$
EP = 0.3e-6;  N1 = 3e-6;  rate = 20;     % GIVEN signal, noise rms [V], sweeps per second
SNR_target_dB = 10;                      % GIVEN
SNR1_dB = 20*log10(EP/N1)                % -20 dB (official)
gain_per_doubling = 10*log10(2)          % +3.01 dB (official)
n_needed = 10^((SNR_target_dB - SNR1_dB)/10)   % 1000 sweeps (official)
t_needed = n_needed/rate                 % 50 s (official)
%
% 10 % artifact sweeps with 10x the noise: average the POWERS
% $$N_{eff}^2 = \sum_i w_i N_i^2$$
frac_bad = 0.1;  N_bad = 30e-6;          % GIVEN
N_eff = sqrt((1 - frac_bad)*N1^2 + frac_bad*N_bad^2)   % 9.905 uV (official)
n_noRej = (N_eff/(EP/10^(SNR_target_dB/20)))^2         % 10 900 sweeps (official)
t_noRej = n_noRej/rate                   % 545 s (official)
n_rej = n_needed/(1 - frac_bad)          % 1111 presented sweeps (official)
t_rej = n_rej/rate                       % 55.6 s (official)

%% D - Outer and middle ear (course text 2.2)
% Ear canal = closed-open tube: $$f = \frac{c}{4L}$$
f_canal = 340/(4*0.025)                  % 3.4 kHz
% Middle ear: area ratio 14 x lever 1.3 -> pressure gain
ME_gain_dB = 20*log10(14*1.3)            % ~25 dB
% Air -> water without it: tau = 4 Z1 Z2/(Z1+Z2)^2
tau_aw = 4*412*1.48e6/(412 + 1.48e6)^2
loss_aw_dB = -10*log10(tau_aw)           % ~29.5 dB
