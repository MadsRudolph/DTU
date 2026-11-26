%% T04 - Spectral components into octave / third-octave bands, A-weighting
% 34840 exam toolkit. Fill in the GIVEN blocks, run, read the printed lines.
%
% Solves: a list of tones with complex amplitudes (several sources,
% harmonics) -> SPL per octave or third-octave band. Components at the SAME
% frequency are added as complex numbers first (coherent), then different
% frequencies in a band are added as mean squares. Then A-weighted levels.
%
% Matches: exam 2023 part 1 P2 (pre-filled: 250/500/1000/2000 Hz bands
% = 70.9 / 77.0 / 70.1 / 57.0 dB; detuned string -> 1000 Hz band 67.1 dB),
% exam 2022 part 1 P2 (alternative GIVEN below: 500/1000/2000 = 71.9 /
% 62.73 / 46.53 dB, 250 Hz band empty = -Inf), exam 2024 part 1 P1.2
% (A-weighted, pre-filled: 89.7 dB(A)), Week 3 P3, slides 34-35 (81.5 dB,
% 77.2 dB(A)), Week 4 MC1 (third octaves into octaves).

%% Constants
p_ref = 20e-6;             % [Pa]

%% GIVEN - edit these: every component, its frequency and complex AMPLITUDE
% 2023 P2: string 1 at 334 Hz with harmonics x2, x3; string 2 at 501 Hz.
f = [334 2*334 3*334  501 2*501 3*501];            % [Hz]
P = [0.1 0.001j 0.04  0.2 0.05  0.02j];             % complex amplitudes [Pa]
% 2022 P2 instead (uncomment):
% f = [400 800 1200  600 900 1200 1500];
% P = [0.1 0.02 0.01  0.05j 0.03j 0.01j 0.006j];
fc = 1000*2.^(-3:1)';      % octave centres 125 ... 2000 Hz (column)
n_oct = 1;                 % 1 = octave bands, 3 = third-octave bands

%% Step 1 - Merge components at the same frequency (coherent sum)
% $$P_{f} = \sum_{\text{same } f} P_i$$
[f_u, ~, idx] = unique(f);
P_u = accumarray(idx(:), P(:)).'      % one complex amplitude per distinct frequency
f_u

%% Step 2 - Band edges
% $$f_l = f_c\,2^{-1/(2n)},\qquad f_u = f_c\,2^{+1/(2n)}$$
edges = [fc*2^(-1/(2*n_oct)), fc*2^(1/(2*n_oct))]  % rows = bands [f_l f_u]

%% Step 3 - Which component sits in which band (rows = bands)
in_band = (f_u >= edges(:,1)) & (f_u < edges(:,2))

%% Step 4 - Band mean square: add |P|^2/2 of the different frequencies
% $$p_{rms,band}^2 = \sum_{i\in\text{band}} \frac{|P_i|^2}{2}$$
p2_band = in_band*(abs(P_u(:)).^2/2)
p_rms_band = sqrt(p2_band)
Lp_band = 10*log10(p2_band/p_ref^2)     % 2023: -Inf 71.0 77.0 70.1 57.0 dB (official prints 70.9: it rounds p_rms to 0.07 Pa)
% An empty band is -Inf dB (zero mean square), NOT 0 dB.
Lp_total = 10*log10(sum(p2_band)/p_ref^2)

%% Step 5 - "Out of tune" version (2023 Q2.2): string 1 drops 1 %
% The two 1002 Hz components are no longer at the same frequency -> add
% as mean squares instead of complex amplitudes.
f_detuned = [0.99*f(1:3) f(4:6)];
in_det = (f_detuned >= edges(:,1)) & (f_detuned < edges(:,2));
Lp_band_detuned = 10*log10(in_det*(abs(P(:)).^2/2)/p_ref^2)   % 1000 Hz band: 67.1 dB (official)

%% A-weighting table (course text Table 1.3.2, third-octave nominal values)
fA = [20 25 31.5 40 50 63 80 100 125 160 200 250 315 400 500 630 800 1000 ...
      1250 1600 2000 2500 3150 4000 5000 6300 8000 10000 12500 16000 20000];
KA = [-50.5 -44.7 -39.4 -34.6 -30.2 -26.2 -22.5 -19.1 -16.1 -13.4 -10.9 -8.6 ...
      -6.6 -4.8 -3.2 -1.9 -0.8 0 0.6 1.0 1.2 1.3 1.2 1.0 0.5 -0.1 -1.1 -2.5 -4.3 -6.6 -9.3];
% Octave centres 31.5 ... 8000: -39.4 -26.2 -16.1 -8.6 -3.2 0 +1.2 +1.0 -1.1
% C-weighting (octaves 31.5 ... 8000): -3.0 -0.8 -0.2 0 0 0 -0.2 -0.8 -3.0
%
% Analytic A-filter from the slides (use for any frequency):
% $$H_A = 7.4\times10^{9}\frac{(j\omega)^4}{(j\omega+129.4)^2(j\omega+676.7)(j\omega+4636)(j\omega+76655)^2}$$
w1k = 2*pi*1000;
HA_1k_dB = 20*log10(abs(7.4e9*(1j*w1k)^4/((1j*w1k+129.4)^2*(1j*w1k+676.7)*(1j*w1k+4636)*(1j*w1k+76655)^2)))   % ~0 dB check

%% B - A-weighted level of tones (2024 P1.2: two tones at 0.6 m)
% Weight EACH component first, then add mean squares.
% $$p_{A,rms} = \frac{|p|}{\sqrt2}10^{K_A/20},\qquad L_A = 10\log_{10}\frac{\sum p_{A,rms}^2}{p_{ref}^2}$$
f_B = [400 630];                        % GIVEN [Hz]
p_B = [0.89 0.86];                      % GIVEN amplitudes [Pa] (from T01)
K_B = interp1(log10(fA), KA, log10(f_B))       % -4.8 and -1.9 dB
pA_rms = p_B/sqrt(2).*10.^(K_B/20)             % 0.36 and 0.50 Pa (official)
LA_B = 10*log10(sum(pA_rms.^2)/p_ref^2)        % 89.7 dB(A) (official 2024 P1.2)

%% C - A-weighted total from band levels (slides 34-35)
% $$L_Z = 10\log_{10}\sum 10^{L_i/10},\qquad L_A = 10\log_{10}\sum 10^{(L_i+K_i)/10}$$
fc_C = [125 250 500 1000];               % GIVEN band centres [Hz]
L_C = [70 75 80 42];                     % GIVEN band levels [dB]
K_C = interp1(log10(fA), KA, log10(fc_C))
LZ_C = 10*log10(sum(10.^(L_C/10)))       % 81.5 dB (slide 34)
LA_C = 10*log10(sum(10.^((L_C + K_C)/10)))   % 77.2 dB(A) (slide 35)

%% D - Third octaves into octaves (3 third-octaves per octave)
% $$L_{oct} = 10\log_{10}\left(10^{L_1/10}+10^{L_2/10}+10^{L_3/10}\right)$$
L_thirds = [55 55 55];                   % GIVEN the three third-octave levels
L_oct = 10*log10(sum(10.^(L_thirds/10))) % +4.8 dB for three equal bands

%% E - Harmonic series into bands (Week 3 P3 style)
% Harmonics of f0: n*f0. Count how many fall in a band:
f0 = 769;                                % GIVEN fundamental [Hz]
harm = f0*(1:30);
n_in_4k = sum(harm >= 4000/sqrt(2) & harm < 4000*sqrt(2))   % 4 harmonics (n = 4..7)
% Equal-amplitude harmonics: L_band = L_one + 10 log10(N_in_band).
