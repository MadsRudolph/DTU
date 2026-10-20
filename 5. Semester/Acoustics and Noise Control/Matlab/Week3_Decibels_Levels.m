%% Lecture 3 - Decibels, levels, frequency analysis and measurements
% 34840 Fundamentals of Acoustics and Noise Control | 15 September 2026
%
% Worked learning document for Problems 3 (34840_Problems3.pdf), checked
% against the official 34840_Solutions03.pdf. Each section states the
% formula first, then computes it in one plain line. Lines without a
% semicolon print their result; the official answer is in the comment.
% Run from the top once, then use Run Section. No toolboxes needed.
%
% The Matlab sound-level-meter exercise (Problem 6) uses the wav files in
% the course zip; see the Week 3 note for its check values.

%% Constants
% Reference RMS pressure for SPL in air.
p_ref = 20e-6;          % [Pa]

%% Problem 1.1 - SPL of a pure tone with amplitude 0.02 Pa
% A sinusoid's RMS value is its amplitude divided by sqrt(2):
%
% $$p_{rms} = \frac{\hat p}{\sqrt 2}$$
p_hat = 0.02;                           % amplitude [Pa]
p_rms1 = p_hat/sqrt(2)                  % 0.0141 Pa
%
% $$L_p = 20\log_{10}\frac{p_{rms}}{p_{ref}}$$
Lp1 = 20*log10(p_rms1/p_ref)            % official: 57.0 dB

%% Problem 1.2 - Add a second tone 100 Hz higher, same amplitude
% Different frequencies: the cross term averages to zero, so the mean
% squares add:
%
% $$p_{rms,tot}^2 = p_{rms,1}^2 + p_{rms,2}^2$$
p_rms_tot = sqrt(p_rms1^2 + p_rms1^2)   % 0.0200 Pa
Lp12 = 20*log10(p_rms_tot/p_ref)        % official: 60.0 dB

%% Problem 2.1 - Two loudspeakers, each 90 dB, received in phase
% Same frequency and phase: the pressures add, so the pressure doubles.
%
% $$L_{tot} = L_1 + 20\log_{10}2$$
L_one = 90;                             % one loudspeaker [dB]
L21 = L_one + 20*log10(2)               % official: 96 dB

%% Problem 2.2 - 120 degree phase lag in one channel
% Add the complex amplitudes. Relative to one loudspeaker:
%
% $$\frac{|p_{tot}|}{|p|} = |1 + e^{-j\varphi}|$$
phi = 120*pi/180;                       % phase lag [rad]
gain22 = abs(1 + exp(-1j*phi))          % = 1
%
% $$L_{tot} = L_1 + 20\log_{10}|1+e^{-j\varphi}|$$
L22 = L_one + 20*log10(gain22)          % official: 90 dB

%% Problem 2.2 - The same rule for other phase lags
% $$\Delta L = 10\log_{10}(2 + 2\cos\varphi)$$
phi_deg = [0 60 90 120 150];
dL_phase = 10*log10(2 + 2*cosd(phi_deg))   % +6.02 +4.77 +3.01 0 -5.72 dB
% 180 degrees gives -Inf: complete cancellation.

%% Problem 2.3 - The two loudspeakers play different tones
% Uncorrelated: add mean squares.
%
% $$L_{tot} = 10\log_{10}\left(10^{L_1/10} + 10^{L_2/10}\right)$$
L23 = 10*log10(10^(L_one/10) + 10^(L_one/10))   % official: 93 dB

%% Problem 3 - Engine with period 1.3 ms in octave bands
% $$f_0 = \frac{1}{T}$$
T_period = 1.3e-3;                      % [s]
f0 = 1/T_period                         % 769 Hz
%
% Fundamental plus six overtones = harmonics 1 to 7:
%
% $$f_n = n f_0$$
f_harm = (1:7)*f0                       % 769 1538 2308 3077 3846 4615 5385 Hz
%
% Octave band limits:
%
% $$f_l = f_c/\sqrt 2, \quad f_u = \sqrt 2 f_c$$
fc_oct = [1000 2000 4000];
f_lower = fc_oct/sqrt(2)                % 707 1414 2828 Hz
f_upper = fc_oct*sqrt(2)                % 1414 2828 5657 Hz
%
% Harmonic 1 is in the 1 kHz band, harmonics 2-3 in the 2 kHz band and
% harmonics 4-7 in the 4 kHz band. Count them:
N_in_band = [sum(f_harm >= f_lower(1) & f_harm < f_upper(1)), ...
             sum(f_harm >= f_lower(2) & f_harm < f_upper(2)), ...
             sum(f_harm >= f_lower(3) & f_harm < f_upper(3))]   % 1 2 4
%
% N equal uncorrelated components of 60 dB:
%
% $$L_{band} = 60 + 10\log_{10}N$$
L_band = 60 + 10*log10(N_in_band)       % official: 60 63 66 dB
%
% Parseval check: the bands add back to the total of 7 components.
% $$L_{tot} = 10\log_{10}\sum 10^{L_{band}/10}$$
L_total3 = 10*log10(sum(10.^(L_band/10)))   % 68.45 dB = 60 + 10 log10(7)

%% Problem 4 - Bandwidth of a 1/12-octave filter at 1 kHz
% $$f_l = f_c\,2^{-1/(2n)}, \quad f_u = f_c\,2^{1/(2n)}$$
fc4 = 1000;                             % [Hz]
n4 = 12;                                % 1/n octave
f_l4 = fc4*2^(-1/(2*n4))                % 971.5 Hz
f_u4 = fc4*2^(1/(2*n4))                 % 1029.3 Hz
%
% $$\Delta f = f_u - f_l$$
bandwidth4 = f_u4 - f_l4                % official: 57.8 Hz

%% Problem 5 - Machine B from the A+B measurement
% Uncorrelated: subtract mean squares.
%
% $$L_B = 10\log_{10}\left(10^{L_{A+B}/10} - 10^{L_A/10}\right)$$
L_A5 = 75;                              % machine A alone [dB]
L_AB5 = 80;                             % both machines [dB]
L_B5 = 10*log10(10^(L_AB5/10) - 10^(L_A5/10))   % official: 78.3 dB
%
% The same thing as a background correction for Delta L = 5 dB:
%
% $$C = -10\log_{10}\left(1 - 10^{-\Delta L/10}\right)$$
corr5 = -10*log10(1 - 10^(-(L_AB5 - L_A5)/10))  % 1.65 dB to subtract

%% Lecture example - Background correction table
% Correction to subtract for a few level differences Delta L.
dL_bg = [3 4 5 6 8 10 15];
corr_bg = -10*log10(1 - 10.^(-dL_bg/10))   % 3.0 2.2 1.7 1.3 0.7 0.5 0.1 dB

%% Lecture example (slide 34) - Octave band levels to total SPL
% $$p_{rms}^2 = p_{ref}^2\,10^{L/10}$$
fc34 = [125 250 500 1000];
L34 = [70 75 80 42];                    % band levels [dB]
p2_34 = p_ref^2*10.^(L34/10)            % 0.0040 0.0126 0.04 6.25e-6 Pa^2 (slide rounds 0.01265 up)
%
% $$p_{rms} = \sqrt{\sum p_{rms,f_c}^2}$$
p_rms34 = sqrt(sum(p2_34))              % slide: 0.238 Pa
SPL34 = 20*log10(p_rms34/p_ref)         % slide: 81.51 dB

%% Lecture example (slide 35) - Same spectrum, A-weighted
% $$L_A = 10\log_{10}\sum 10^{(L_i + K_i)/10}$$
K34 = [-16.1 -8.6 -3.2 0];              % A-weighting [dB], text Table 1.3.2
LA34 = 10*log10(sum(10.^((L34 + K34)/10)))   % 77.2 dB(A)

%% Lecture example - A-weighting from the slide-25 transfer function
% $$H_A(j\omega) = 7.4\cdot10^9\frac{(j\omega)^4}{(j\omega+129.4)^2(j\omega+676.7)(j\omega+4636)(j\omega+76655)^2}$$
f_A = [31.5 63 125 250 440 500 1000 2000 4000 8000];
s_A = 1j*2*pi*f_A;
H_A = 7.4e9*s_A.^4./((s_A+129.4).^2.*(s_A+676.7).*(s_A+4636).*(s_A+76655).^2);
K_A = 20*log10(abs(H_A))   % table: -39.4 -26.2 -16.1 -8.6 (-4.1) -3.2 0 1.2 1.0 -1.1
%
% The 440 Hz value explains the Matlab check: 74.0 dB flat -> 69.9 dB(A).
LA_440 = 74 + K_A(5)                    % guide: 69.9 dB(A)

%% Lecture example - Plot the A-weighting curve
f_plot = logspace(log10(20), log10(20000), 400);
s_plot = 1j*2*pi*f_plot;
K_plot = 20*log10(abs(7.4e9*s_plot.^4./((s_plot+129.4).^2.*(s_plot+676.7).*(s_plot+4636).*(s_plot+76655).^2)));
figure('Name','A-weighting');
semilogx(f_plot, K_plot, 'LineWidth', 1.6); grid on;
xlabel('Frequency [Hz]'); ylabel('A-weighting [dB]');
ylim([-50 5]); title('A-weighting: the ear at moderate levels');

%% Lecture example (course text ex. 1.3.11) - Equivalent level of a duty cycle
% $$L_{eq,T} = 10\log_{10}\sum \frac{t_i}{T}10^{L_i/10}$$
t_i = [15 5 20];                        % minutes
L_i = [84 95 71];                       % dB(A)
Leq_cycle = 10*log10(sum(t_i/sum(t_i).*10.^(L_i/10)))   % text: 87.0 dB

%% Lecture example (slide 22) - Half the time 85 dB, half 66 dB
Leq_onoff = 10*log10(0.5*10^(85/10) + 0.5*10^(66/10))   % slide: 82.1 dB (measured)

%% Lecture example - Exponential detector constants at 44.1 kHz
% $$\alpha = e^{-1/(\tau f_s)}$$
fs = 44100;                             % [Hz]
alpha_F = exp(-1/(0.125*fs))            % 0.99982
alpha_S = exp(-1/(1*fs))                % 0.99998
%
% Decay rate after the source stops:
%
% $$\frac{dL}{dt} = \frac{10\log_{10}e}{\tau}$$
decay_F = 10*log10(exp(1))/0.125        % 34.7 dB/s
decay_S = 10*log10(exp(1))/1            % 4.3 dB/s

%% Lecture example - White and pink noise at 94 dB (1 Pa^2), 20 Hz - 20 kHz
% White: constant power per Hz.
% $$S = \frac{p_{rms}^2}{f_2 - f_1}$$
S_white = 1/(20000 - 20)                % 5.0e-5 Pa^2/Hz (slide 41)
% Pink: constant power per third-octave, 30 bands in the audio range.
p2_pink_third = 1/30                    % 0.033 Pa^2 per band (slide 40)
% White noise rises by this much from one third-octave band to the next:
% $$\Delta L = 10\log_{10}2^{1/3}$$
dL_white_third = 10*log10(2^(1/3))      % 1.0 dB
