%% Lecture 9 - Hearing: frequency selectivity and masking
% 34840 Fundamentals of Acoustics and Noise Control | 3 November 2026
%
% Worked learning document for 34840_Psychological_Acoustics_Exercise_2026.pdf.
% Every formula is first written as an equation, then calculated in one
% plain MATLAB line. Lines without a semicolon print their result.
%
% Checked 26-Nov against 34840_Psychological_Acoustics_Solutions_2026.doc:
% every number agrees. One slip in the official text: in 3.3 it writes the
% noise density as "153.9 mW/Hz"; the number is 1.539e-10 W/(m^2 Hz), i.e.
% 153.9 pW/(m^2 Hz) (pico, not milli).
%
% Model used throughout (power spectrum model of masking, deck page 25):
%   P_s = k * integral W(f) N(f) df,  with W rectangular, 1 ERB wide,
%   so P_s = k * N0 * (noise bandwidth inside the filter).
% Levels are intensity levels re P0 = 1e-12 W/m^2 (same number as dB SPL).

%% Constants
P0 = 1e-12;           % reference intensity [W/m^2]
k = 0.3;              % signal-to-noise ratio at the filter output at threshold

%% Problem 1.1 - ERB at 0.1, 1 and 10 kHz
%
% $$\mathrm{ERB} = 24.7\,(4.37F + 1),\qquad F\ \text{in kHz}$$
ERB_01 = 24.7*(4.37*0.1 + 1)          % 35.5 Hz (official: 35.5 Hz)
ERB_1 = 24.7*(4.37*1 + 1)             % 132.6 Hz (official: 132.6 Hz)
ERB_10 = 24.7*(4.37*10 + 1)           % 1104.1 Hz (official: 1104.1 Hz)

%% Problem 1.2 - Masked threshold in broadband noise, 40 dB/Hz
% The noise is wider than every filter, so the whole ERB is filled.
%
% $$N_0 = P_0\,10^{40/10},\qquad P_s = k\,N_0\,\mathrm{ERB},\qquad L_s = 10\log_{10}\frac{P_s}{P_0}$$
N0 = P0*10^(40/10)                    % 1e-8 W/(m^2 Hz)
Ls_01 = 10*log10(k*N0*ERB_01/P0)      % 50.3 dB (official: 50.3 dB)
Ls_1 = 10*log10(k*N0*ERB_1/P0)        % 56.0 dB (official: 56.0 dB)
Ls_10 = 10*log10(k*N0*ERB_10/P0)      % 65.2 dB (official: 65.2 dB)
% Easiest to detect at 0.1 kHz: the narrowest filter lets the least noise in.
%
% Same thing in dB, without linear units:
% $$L_s = N_{0,\mathrm{dB}} + 10\log_{10}k + 10\log_{10}\mathrm{ERB}$$
Ls_1_dB = 40 + 10*log10(k) + 10*log10(ERB_1)   % 56.0 dB, same

%% Problem 1.3 - Same, but the noise is only 20 Hz wide
% 20 Hz < ERB at all three frequencies, so the filter sees only 20 Hz of noise.
%
% $$P_s = k\,N_0\,\min(\Delta f_{noise},\ \mathrm{ERB})$$
Ls_20 = 10*log10(k*N0*20/P0)          % 47.8 dB at all three (official: 47.8 dB)

%% Problem 2 - Loudness of 20 Hz and 50 Hz noise bands, same intensity
% Louder = spreads over more than one auditory filter (loudness summation).
ERB_100Hz = ERB_01                    % 35.5 Hz: 20 Hz fits inside, 50 Hz does not
% -> fc = 100 Hz: the 50 Hz noise is louder (official: the 50 Hz noise)
ERB_1kHz = ERB_1                      % 132.6 Hz: both fit inside one filter
% -> fc = 1 kHz: equally loud (official: same loudness)

%% Problem 3.2 - Combination tones f1 - n(f2 - f1)
% f1 = 1 kHz, f2 = 1.1 kHz, L1 = L2 = 50 dB SPL.
%
% $$f_{CT} = f_1 - n\,(f_2 - f_1),\qquad L_{CT} = L_1 + 125\,(f_{CT} - 1)\quad (f\ \text{in kHz})$$
f1 = 1; f2 = 1.1; L1 = 50;
fCT1 = f1 - 1*(f2 - f1)               % 0.9 kHz (official: 900 Hz)
fCT2 = f1 - 2*(f2 - f1)               % 0.8 kHz (official: 800 Hz)
fCT3 = f1 - 3*(f2 - f1)               % 0.7 kHz (official: 700 Hz)
LCT1 = L1 + 125*(fCT1 - 1)            % 37.5 dB SPL (official: 37.5)
LCT2 = L1 + 125*(fCT2 - 1)            % 25.0 dB SPL (official: 25.0)
LCT3 = L1 + 125*(fCT3 - 1)            % 12.5 dB SPL (official: 12.5)
% The 2f1-f2 tone (n = 1) is the strongest and lies closest to f1.

%% Problem 3.3 - Noise density that just masks all three
% One rectangular filter per tone; ERB at 900 Hz:
ERB_09 = 24.7*(4.37*fCT1 + 1)         % 121.8 Hz (official: 121.8 Hz)
% 800 and 700 Hz lie 100 and 200 Hz away, outside the 900 Hz filter.
%
% $$N_0 = \frac{P_s}{k\,\mathrm{ERB}},\qquad P_s = P_0\,10^{L_{CT}/10}$$
Ps_09 = P0*10^(LCT1/10)               % 5.62e-9 W/m^2
N0_req = Ps_09/(k*ERB_09)             % 1.54e-10 W/(m^2 Hz) (official writes 153.9 "mW/Hz": should be pW)
N0_req_dB = 10*log10(N0_req/P0)       % 21.9 dB/Hz (official: 21.9 dB/Hz)
%
% Check the weaker tones: the masked threshold this noise creates in their filters.
% $$L_s = N_{0,\mathrm{dB}} + 10\log_{10}(k\,\mathrm{ERB})$$
ERB_08 = 24.7*(4.37*fCT2 + 1)         % 111.0 Hz
ERB_07 = 24.7*(4.37*fCT3 + 1)         % 100.3 Hz
Ls_08 = N0_req_dB + 10*log10(k*ERB_08)  % 37.1 dB > 25.0, masked
Ls_07 = N0_req_dB + 10*log10(k*ERB_07)  % 36.7 dB > 12.5, masked (official: 36.7 dB)

%% Extra - Three bandwidth scales from the deck (page 32) and the text (§2.6)
% $$\Delta f_{Bark} = 25 + 75\,(1 + 1.4F^2)^{0.69},\qquad \Delta f_{1/3} = (2^{1/6} - 2^{-1/6})f = 0.232f$$
CB_01 = 25 + 75*(1 + 1.4*0.1^2)^0.69  % 100.7 Hz (ERB: 35.5)
CB_1 = 25 + 75*(1 + 1.4*1^2)^0.69     % 162.2 Hz (ERB: 132.6)
CB_2 = 25 + 75*(1 + 1.4*2^2)^0.69     % 300.8 Hz (ERB: 240.6; Fletcher on page 24: ~400 Hz)
CB_10 = 25 + 75*(1 + 1.4*10^2)^0.69   % 2306 Hz (ERB: 1104)
third_1 = (2^(1/6) - 2^(-1/6))*1000   % 231.6 Hz at 1 kHz
%
% Where ERB equals a third-octave band: 24.7(4.37F + 1) = 232F
F_cross = 24.7/(232 - 24.7*4.37)      % 0.199 kHz; above ~200 Hz the ear is sharper than 1/3 octave
%
% Rounded-exponential filter (page 29): W(g) = (1+pg)e^(-pg), g = |f-fc|/fc.
% Its area is 4fc/p, so ERB = 4fc/p and p = 4fc/ERB (my derivation, not on the slides).
p_1k = 4*1000/ERB_1                   % 30.2 at 1 kHz

%% Figure - ERB, critical band (Bark) and third-octave bandwidth vs centre frequency
F = logspace(log10(0.02), log10(20), 400);    % kHz
fig = figure('Visible','off');
theme(fig,'light');
loglog(1000*F, 24.7*(4.37*F + 1), 'LineWidth', 1.8); hold on
loglog(1000*F, 25 + 75*(1 + 1.4*F.^2).^0.69, 'LineWidth', 1.8);
loglog(1000*F, 232*F, '--', 'LineWidth', 1.5);
loglog([100 1000 10000], [ERB_01 ERB_1 ERB_10], 'ko', 'MarkerFaceColor', 'k');
grid on; xlim([20 20000]); ylim([10 5000]);
xlabel('Centre frequency (Hz)'); ylabel('Bandwidth (Hz)');
legend('ERB = 24.7(4.37F+1)', 'Critical band (Bark) = 25+75(1+1.4F^2)^{0.69}', ...
    'One-third octave = 0.232f', 'Problem 1.1: 35.5 / 132.6 / 1104 Hz', 'Location', 'northwest');
title('Auditory filter bandwidth vs centre frequency');
outDir = fullfile(getenv('HOME'), 'DTU', 'Obsidian', 'Courses', ...
    '34840 Fundamentals of Acoustics and Noise Control', 'Images', 'Lecture9');
if ~exist(outDir, 'dir'); mkdir(outDir); end
exportgraphics(fig, fullfile(outDir, 'bandwidth_scales.png'), 'Resolution', 150);
