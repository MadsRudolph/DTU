%% T12 - Hearing: ERB, power-spectrum model of masking, combination tones, loudness
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: ERB (and Bark critical band, third octave) at a frequency, the
% masked threshold of a tone in noise with a rectangular ERB filter, the
% noise density needed to mask a tone, combination-tone frequencies and
% levels, which tones share a filter, loudness in sone from phon.
%
% Matches: Psychological Acoustics exercise (Week 9), all pre-filled:
% P1.1 ERB 35.5 / 132.6 / 1104.1 Hz, P1.2 thresholds 50.3 / 56.0 / 65.2 dB,
% P1.3 20 Hz noise 47.8 dB, P3.2 combination tones 900/800/700 Hz at
% 37.5/25.0/12.5 dB, P3.3 noise density 21.9 dB/Hz and 36.7 dB at 700 Hz.
% Also 2022 MC14 and 2023 MC14 (two tones: same or separate filters).

%% Constants
P0 = 1e-12;                % reference intensity [W/m^2] (levels in dB SPL)

%% A - Bandwidth scales (F in kHz!)
% $$\mathrm{ERB} = 24.7(4.37F+1),\quad \mathrm{CB} = 25+75(1+1.4F^2)^{0.69},\quad \Delta f_{1/3} = 0.232f$$
F = [0.1 1 10];                          % GIVEN centre frequencies [kHz]
ERB = 24.7*(4.37*F + 1)                  % 35.5 132.6 1104.1 Hz (official)
CB_bark = 25 + 75*(1 + 1.4*F.^2).^0.69
third_oct = (2^(1/6) - 2^(-1/6))*F*1000
% ERB is narrower than a third octave above ~200 Hz.

%% B - Masked threshold of a tone in noise (power-spectrum model, rectangular filter)
% $$P_s = k\,N_0\,\min(\Delta f_{noise},\mathrm{ERB})\qquad L_s = N_{0,dB}+10\log_{10}k+10\log_{10}\min(\Delta f,\mathrm{ERB})$$
N0_dB = 40;                              % GIVEN noise spectrum level [dB/Hz]
k = 0.3;                                 % GIVEN SNR at the filter output
df_noise = Inf;                          % GIVEN noise bandwidth [Hz] (Inf = broadband)
Ls = N0_dB + 10*log10(k) + 10*log10(min(df_noise, ERB))   % 50.3 56.0 65.2 dB (official P1.2)
Ls_20Hz = N0_dB + 10*log10(k) + 10*log10(min(20, ERB))    % 47.8 dB everywhere (official P1.3)
% Narrowest filter -> least noise -> lowest threshold (low f easiest).

%% C - Combination tones (f1 < f2) and their levels
% $$f_{CT} = f_1 - n(f_2-f_1)\quad(n=1: 2f_1-f_2),\qquad L_{CT} = L_1 + 125(f_{CT}-1)\ \text{(sheet rule, f in kHz)}$$
f1 = 1;  f2 = 1.1;  L1 = 50;             % GIVEN [kHz], [kHz], [dB]
nCT = 1:3;
f_CT = f1 - nCT*(f2 - f1)                % 0.9 0.8 0.7 kHz (official)
L_CT = L1 + 125*(f_CT - 1)               % 37.5 25.0 12.5 dB (official)

%% D - Noise density that just masks the tones (P3.3)
% Strongest tone sets it: N0 = P_s/(k ERB) at its frequency.
ERB_09 = 24.7*(4.37*f_CT(1) + 1)         % 121.8 Hz (official)
N0_req_dB = L_CT(1) - 10*log10(k) - 10*log10(ERB_09)   % 21.9 dB/Hz (official)
Ls_at_CT = N0_req_dB + 10*log10(k) + 10*log10(24.7*(4.37*f_CT + 1))
masked = Ls_at_CT >= L_CT                % all true: 36.7 dB at 700 Hz > 12.5 (official)

%% E - Do two tones fall in the same auditory filter? (rectangular ERB)
fa = 850;  fb = 900;                     % GIVEN [Hz] (2022 MC14)
ERB_mid = 24.7*(4.37*(fa + fb)/2000 + 1)
same_filter = abs(fb - fa) < ERB_mid     % true -> one tone, beating at |fb - fa| Hz
beat_rate = abs(fb - fa)
% 2023 MC14: 400 and 600 Hz: ERB ~ 68 Hz << 200 Hz -> two separate tones.
same_filter_2023 = abs(600 - 400) < 24.7*(4.37*0.5 + 1)

%% F - Loudness: sone from phon (1 sone = 40 phon, +10 phon = twice as loud)
% $$N = 2^{(L_N-40)/10}\ \mathrm{sone}$$
L_phon = [40 50 60];
N_sone = 2.^((L_phon - 40)/10)
% Noise wider than the ERB at fixed power is LOUDER (loudness summation):
% at 100 Hz (ERB 35.5) a 50 Hz band > a 20 Hz band; at 1 kHz both fit -> equal.

%% G - Facts for the multiple choice (no calculation)
% Base = high f (stiff, narrow), apex = low f. OHC amplify (level dependent,
% compressive, only near CF); IHC sense. Filters broaden with level on the
% LOW side; masking spreads UPWARD in frequency. Sensorineural loss: OHC
% damage -> higher threshold, broader filters, less compression,
% loudness recruitment (loudness grows faster), weaker combination tones.
% Notched noise avoids off-frequency listening. Forward masking ~200 ms,
% backward ~20 ms.
