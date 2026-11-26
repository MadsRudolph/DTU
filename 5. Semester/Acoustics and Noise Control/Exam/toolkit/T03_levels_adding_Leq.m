%% T03 - Levels: rms, adding sources, background correction, Leq
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: SPL from an amplitude, adding tones/sources (coherent = complex
% sum, incoherent = mean squares), subtracting background noise, the
% equivalent level of an on/off source or several sources over a day.
%
% Matches: 2022 MC2 (beating tuning forks, pre-filled: 0.161 Pa),
% 2022 MC3 (machine 4 h of 24 h, pre-filled: 66.2 dB), 2024 MC2 (15 min
% per hour, pre-filled: 62 dB), 2023 MC1 (two 10 dB sources: 13 dB),
% Week 3 P1, P2, P5 (pre-filled: 57.0 dB, 90 dB, 78.3 dB), hand-in P2
% (festival Leq, 24 h).

%% Constants
p_ref = 20e-6;             % [Pa]

%% A - Amplitude to SPL (Week 3 P1.1: 0.02 Pa amplitude -> 57.0 dB)
% $$p_{rms} = \hat p/\sqrt2,\qquad L_p = 20\log_{10}\frac{p_{rms}}{p_{ref}}$$
p_hat = 0.02;                                  % GIVEN amplitude [Pa]
p_rms = p_hat/sqrt(2)
Lp_A = 20*log10(p_rms/p_ref)                   % 57.0 dB (official)
% Back again: p_rms = p_ref 10^(L/20),  p_rms^2 = p_ref^2 10^(L/10)

%% B - Two tones at DIFFERENT frequencies (or a long average of a beat)
% 2022 MC2: tuning forks 0.18 and 0.14 Pa amplitude, 440.00 / 440.10 Hz,
% averaged over 10 s = one full beat period 1/0.1 Hz -> treat as incoherent.
% $$p_{rms} = \sqrt{\frac{|\hat p_1|^2}{2}+\frac{|\hat p_2|^2}{2}}$$
p1_hat = 0.18; p2_hat = 0.14;                  % GIVEN amplitudes [Pa]
beat_period = 1/abs(440.10 - 440.00)           % 10 s: equal to the averaging time
p_rms_B = sqrt(p1_hat^2/2 + p2_hat^2/2)        % 0.161 Pa (official, answer B)

%% C - Two tones at the SAME frequency (coherent): add complex amplitudes
% Week 3 P2.2: two 90 dB loudspeakers, 120 deg phase lag -> 90 dB.
% $$L = L_1 + 20\log_{10}\left|1 + \frac{\hat p_2}{\hat p_1}\right|$$
L_one = 90;                                    % GIVEN level of each [dB]
phi = 120;                                     % GIVEN phase difference [deg]
gain_C = abs(1 + exp(-1j*phi*pi/180))
L_C = L_one + 20*log10(gain_C)                 % 90 dB (official). 0 deg: +6.02, 90 deg: +3.01
% General: p_tot = |A1 + A2|/sqrt(2) with complex amplitudes A1, A2.

%% D - Uncorrelated sources: add mean squares (never add dB)
% 2023 MC1: two uncorrelated sources of 10 dB each -> 13 dB.
% $$L_{tot} = 10\log_{10}\sum_i 10^{L_i/10}$$
L_list = [10 10];                              % GIVEN levels [dB]
L_D = 10*log10(sum(10.^(L_list/10)))           % 13.0 dB (official)
% N equal sources: +10 log10(N). 6 dB apart: +1 dB. 10 dB apart: +0.4 dB.

%% E - Background-noise correction (subtract mean squares)
% Week 3 P5: A alone 75 dB, A+B 80 dB -> B = 78.3 dB.
% $$L_{src} = 10\log_{10}\left(10^{L_{tot}/10} - 10^{L_{bg}/10}\right)$$
L_tot = 80; L_bg = 75;                         % GIVEN [dB]
L_E = 10*log10(10^(L_tot/10) - 10^(L_bg/10))   % 78.3 dB (official)
% Only reliable when L_tot - L_bg >= 3 dB; ignore if > 10 dB.

%% F - Equivalent level of an on/off source
% 2022 MC3: 0.1 Pa rms while running, 4 h (50 % of 8 h) in a 24 h period.
% $$L_{eq,T} = 10\log_{10}\left(\frac{t_{on}}{T}\frac{p_{rms}^2}{p_{ref}^2}\right)$$
p_on = 0.1;  t_on = 4;  T = 24;                % GIVEN [Pa], [h], [h]
Leq_F = 10*log10(t_on/T*p_on^2/p_ref^2)        % 66.2 dB (official, answer B)
%
% 2024 MC2: 0.05 Pa rms, 15 min every hour, over 8 h -> duty cycle 1/4.
p_on2 = 0.05;  duty = 15/60;                   % GIVEN
Leq_F2 = 10*log10(duty*p_on2^2/p_ref^2)        % 61.9 -> 62 dB (official option)

%% G - Several levels L_i for durations t_i (and several sources)
% $$L_{eq,T} = 10\log_{10}\sum_i \frac{t_i}{T}10^{L_i/10}$$
% Course text ex. 1.3.11: 84 dB 15 min, 95 dB 5 min, 71 dB 20 min -> 87.0 dB
L_i = [84 95 71];  t_i = [15 5 20];            % GIVEN [dB], [min]
Leq_G = 10*log10(sum(t_i/sum(t_i).*10.^(L_i/10)))    % 87.0 dB
% Hand-in style: 6 shows of 1 h at 60 dB in 24 h -> 60 + 10log(6/24) = 54.0 dB.
% Then several uncorrelated stages: add their Leq values as in D.
Leq_stage = 60 + 10*log10(6/24)

%% H - Sound exposure level of n events (single event SEL)
% $$L_{eq,T} = L_{AE} + 10\log_{10} n - 10\log_{10}(T/1\,\mathrm{s})$$
L_AE = 90; n_ev = 100; T_s = 8*3600;           % GIVEN example values
Leq_H = L_AE + 10*log10(n_ev) - 10*log10(T_s)
