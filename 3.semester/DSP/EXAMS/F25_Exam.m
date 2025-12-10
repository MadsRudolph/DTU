%% F25 Eksamen

%% 62743 Digital Signal Processing - F25 Eksamen
% Danmarks Tekniske Universitet
% Dato: 10/12 2025
clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers\');
%% Global image directory (Obsidian path)
imgDir = 'C:\Users\Mads2\DTU\Obsidian\Courses\DSP\Images';
if ~exist(imgDir, 'dir')
    mkdir(imgDir);
end
%% EKSAMENSOPGAVE 1 (25%)

%  LTI System Analysis

% Givne signaler og data
% Input signals
% x1[n] = δ[n] - 2δ[n-1]
% x2[n] = -δ[n] + 3δ[n-1]

x1 = [1, -2];       % x1[n] coefficients: [x1(0), x1(1)]
x2 = [-1, 3];       % x2[n] coefficients: [x2(0), x2(1)]

% Output signals (from table)
n_vals = 0:5;
y1 = [1, 0, 2, -10, -3, -2];    % y1[n] for n = 0,1,2,3,4,5
y2 = [-1, 1, 0, 16, 5, 3];      % y2[n] for n = 0,1,2,3,4,5

%% Spørgsmål 1-1: Beregn x1[n] + x2[n]

% Step 1: Write signals with explicit coefficients
% x1[n] = (+1)·δ[n] + (-2)·δ[n-1]
% x2[n] = (-1)·δ[n] + (+3)·δ[n-1]

% Combining terms
% δ[n]:   1 + (-1) = 0
% δ[n-1]: -2 + 3 = 1

% Result: δ[n-1] 

fprintf('Result: x₁[n] + x₂[n] = δ[n-1]\n');


%% Spørgsmål 1-2a: Beregn y1[n] + y2[n]

y_sum = y1 + y2;
disp('y1 + y2 ='); disp(y_sum);

%so
%y1[n] + y2[n] = δ[n-1]+2δ[n-2]+6δ[n-3]+2δ[n-4]+δ[n-5]

fprintf('Result: y1[n] + y2[n] = δ[n-1]+2δ[n-2]+6δ[n-3]+2δ[n-4]+δ[n-5] \n');
%% Spørgsmål 1-2b: Eftervis at h[n] = δ[n] + 2δ[n-1] + 6δ[n-2] + 2δ[n-3] + δ[n-4]

% We know from 1-1 that input was x1 + x2 = δ[n-1]
% So the output y1 + y2 is the impulse response delayed by 1: h[n-1]

% y1 + y2 = 0·δ[n] + 1·δ[n-1] + 2·δ[n-2] + 6·δ[n-3] + 2·δ[n-4] + 1·δ[n-5]
% This equals h[n-1]

% To get h[n], we shift everything left by 1 (replace n-1 with n):
% term δ[n-1] becomes δ[n]
% term δ[n-2] becomes δ[n-1]
% ... and so on

% Resulting h[n]:
fprintf('Result: h[n] = δ[n] + 2δ[n-1] + 6δ[n-2] + 2δ[n-3] + δ[n-4] \n');
%% Spørgsmål 1-3a: Angiv systemfunktionen H(z)

%% Spørgsmål 1-3a: Angiv systemfunktionen H(z)
% h[n] = δ[n] + 2δ[n-1] + 6δ[n-2] + 2δ[n-3] + δ[n-4]
% 
% Taking Z-transform (using δ[n-k] → z^(-k)):
%   δ[n]   → 1
%   2δ[n-1] → 2z^(-1)
%   6δ[n-2] → 6z^(-2)
%   2δ[n-3] → 2z^(-3)
%   δ[n-4] → z^(-4)

% Manual result:
fprintf('Result: H(z) = 1 + 2z^(-1) + 6z^(-2) + 2z^(-3) + z^(-4)\n\n');

%% Spørgsmål 1-3b: Angiv frekvensresponset H(ω) = H(z)|_{z=e^{jω}}

% H(z) = 1 + 2z^(-1) + 6z^(-2) + 2z^(-3) + z^(-4)
%substitute z=e^(jω) to get frekvensrespons

% H(ω)= 1 + 2e^(-jω) + 6e^(-2jω) + 2e^(-3jω) + e^(-4jω)


% Manual result:
fprintf('Result: H(ω)= 1 + 2e^(-jω) + 6e^(-2jω) + 2e^(-3jω) + e^(-4jω)\n\n');

%% Spørgsmål 1-4a: Beregn |H(ω)| og ∠H(ω) analytisk
% 

% Given: H(ω) = 1 + 2e^(-jω) + 6e^(-2jω) + 2e^(-3jω) + e^(-4jω)
%
% Step 1: Factor out center phase term e^(-j2ω)
%   H(ω) = e^(-j2ω) (e^(j2ω) + 2e^(jω) + 6 + 2e^(-jω) + e^(-j2ω))
%
% Step 2: Group symmetric terms
%   H(ω) = e^(-j2ω) [(e^(j2ω) + e^(-j2ω)) + 2(e^(jω) + e^(-jω)) + 6]
%
% Step 3: Apply Euler's identity: e^(jθ) + e^(-jθ) = 2cos(θ)
%   H(ω) = e^(-j2ω) [2cos(2ω) + 4cos(ω) + 6]
%
% Step 4: Extract magnitude and phase
%   Since H(ω) = e^(-j2ω) · A(ω) where A(ω) is real:
%   |H(ω)| = |A(ω)| and ∠H(ω) = -2ω

fprintf('Magnitude response:\n');
fprintf('|H(ω)| = 2cos(2ω) + 4cos(ω) + 6\n\n');

fprintf('Phase response:\n');
fprintf('∠H(ω) = -2ω\n\n');
%%  Spørgsmål 1-4b: Plot |H(ω)| og ∠H(ω) for -π ≤ ω ≤ π

% Frequency vector
omega = linspace(-pi, pi, 1024);

% Analytical formulas from 1-4a
mag = 2*cos(2*omega) + 4*cos(omega) + 6;
phase = -2*omega;

% Create plots
figure;

% Magnitude Response
subplot(2,1,1);
plot(omega, mag, 'b-', 'LineWidth', 1.5);
xlabel('\omega (rad/sample)');
ylabel('|H(\omega)|');
title('Magnitude Response');
ylim ([0 14]);
grid on;

% Phase Response
subplot(2,1,2);
plot(omega, phase, 'b-', 'LineWidth', 1.5);
xlabel('\omega (rad/sample)');
ylabel('\angle H(\omega) (rad)');
title('Phase Response');
ylim ([-8 8]);
xlim ([-4 4]);
grid on;

% Export figure
exportgraphics(gcf, fullfile(imgDir, ...
    'DSP_Exam_F25_1_4b_MagPhase.png'), 'Resolution', 300);
%% Spørgsmål 1-5: Find systemfunktion for samlet system (T1, T2, T3)
% 

% Given systems
H1_B = [1, 2, 6, 2, 1];      % From problem 1-3
H2_B = [3, -10, -11];         % Given
H3_A = [1, 0, -1/4];          % Denominator of H3

%% Step 1: Add parallel systems (T1 + T2)

%T1 + T2
% (1+3) (2+(-10)) (6+(-11)) 2 1
H_parallel_B = [4, -8, -5, 2, 1];  % Add coefficients

fprintf('H1(z) + H2(z) = 4 - 8z^(-1) - 5z^(-2) + 2z^(-3) + z^(-4)\n\n');

%% Step 2: Divide by H3 denominator to cancel factors
% Use polynomial division (positive powers)
num = [4, -8, -5, 2, 1];      % 4z^4 - 8z^3 - 5z^2 + 2z + 1
den = [1, 0, -1/4];            % z^2 - 1/4

[H_total_B, remainder] = deconv(num, den)

fprintf('After polynomial division:\n');
fprintf('H_total(z) = 4 - 8z^(-1) - 4z^(-2)\n\n');

%% Step 3: Show it's FIR
fprintf('=== FIR Verification ===\n');
fprintf('Coefficients: [%g, %g, %g]\n', H_total_B);
fprintf('Denominator = 1 → FIR system ✓\n');
fprintf('Impulse response: h4[n] = 4δ[n] - 8δ[n-1] - 4δ[n-2]\n');



%% EKSAMENSOPGAVE 2 (25%)
%% IIR Butterworth Highpass Filter Design (BLT)

% Givne specifikationer
Fs = 4000;              % Sampling frequency [Hz]
Ts = 1/Fs;              % Sampling period [s]

fs_hz = 450;            % Stopband edge frequency [Hz]
fp_hz = 1000;           % Passband edge frequency [Hz]

As_dB = 30;             % Stopband attenuation [dB]
Ap_dB = 3;              % Passband attenuation [dB]

% Normalized digital frequencies
omega_s = 2*pi*fs_hz/Fs;    % Stopband [rad/sample]
omega_p = 2*pi*fp_hz/Fs;    % Passband [rad/sample]

%% Spørgsmål 2-1: Analog prototype Butterworth filter

% (1) Beregn epsilon (ε)

epsilon = sqrt(10^(Ap_dB/10) - 1);
fprintf('ε = %.2f\n\n', epsilon);


% (2) Beregn digitale vinkelfrekvenser (ω)
fprintf('Digital frequencies:\n');
fprintf('ω_s = %.4f rad/sample = %.4fπ\n', omega_s, omega_s/pi);
fprintf('ω_p = %.4f rad/sample = %.4fπ\n\n', omega_p, omega_p/pi);

% Pre-warping: Digital → Analog
Omega_s = 2*Fs * tan(omega_s/2);
Omega_p = 2*Fs * tan(omega_p/2);

fprintf('Pre-warped analog frequencies:\n');
fprintf('Ω_s = %.2f rad/s\n', Omega_s);
fprintf('Ω_p = %.2f rad/s\n\n', Omega_p);

% (3) Beregn minimum filter orden n
% For HIGHPASS: ratio = Omega_p / Omega_s (inverted!)
ratio = Omega_p / Omega_s;

% Butterworth order formula
n_exact = log10((10^(As_dB/10) - 1) / (10^(Ap_dB/10) - 1)) / (2*log10(ratio));
n = ceil(n_exact);

fprintf('Filter order calculation:\n');
fprintf('Ratio (Ω_p/Ω_s) = %.4f\n', ratio);
fprintf('n_exact = %.4f\n', n_exact);
fprintf('n_min = %d\n\n', n);


% (4) Opskriv prototype lavpas transferfunktion (se appendix)
B_proto = 1;
A_proto = [1, 2.6131, 3.4142, 2.6131, 1];



% Create transfer function object
fprintf('Prototype Butterworth lowpass transfer function H_LP(s):\n');
H_proto = tf(B_proto, A_proto)
%% Spørgsmål 2-2: LP → HP transformation

% (a) Transformation formula
fprintf('(a) Transformation formula: s → Ω_p/s\n');
fprintf('    Where Ω_p = %.2f rad/s\n\n', Omega_p);

% (b) Apply LP to HP transformation
fprintf('(b) Analog Highpass Filter H_HP(s):\n');

% Use MATLAB's lp2hp function
[B_hp, A_hp] = lp2hp(B_proto, A_proto, Omega_p);

% Display transfer function
H_hp = tf(B_hp, A_hp)

% (c) Plot analog magnitude response
fprintf('\n(c) Plotting analog magnitude response...\n');

Omega = [0:1:1E4];  % 0 to 10 krad/s (match official solution)
H_analog = freqs(B_hp, A_hp, Omega);

figure;
plot(Omega, 20*log10(abs(H_analog)), 'LineWidth', 2);
hold on;

% Add specification lines (blue lines like official solution)
xline(Omega_s, 'b-', 'LineWidth', 2);  % Stopband edge
xline(Omega_p, 'b-', 'LineWidth', 2);  % Passband edge
yline(-30, 'b-', 'LineWidth', 2);      % Stopband requirement
yline(-3, 'b-', 'LineWidth', 2);       % Passband requirement

xlabel('\Omega (rad/s)');
ylabel('20log_{10}(|H(\Omega)|) (dB)');
title('Analog Highpass Butterworth Filter');
grid on;
xlim([0 10000]);
ylim([-40 5]);

hold off;

% Export figure
exportgraphics(gcf, fullfile(imgDir, ...
    'DSP_Exam_F25_2_2_AnalogHP_Magnitude.png'), 'Resolution', 300);

% (d) Visual verification
fprintf('\n(d) Verification:\n');
fprintf('De blå linjer på plottet indikerer kravspecifikationerne for det analoge filter.\n');
fprintf('Filteret opfylder de analoge design krav.\n');


%% Spørgsmål 2-3: Bilinear transformation (BLT)

% (a) BLT relation
alpha = 2/Ts;
fprintf('(a) BLT parameter α = 2/T_s = 2·F_s = %.0f\n', alpha);
fprintf('    Transformation: s = α·(z-1)/(z+1)\n\n');

% (b) Apply Bilinear Transform
fprintf('(b) Digital Highpass Filter H_HP(z):\n');

% Use MATLAB's bilinear function
[Bz, Az] = bilinear(B_hp, A_hp, Fs);

% Normalize so a[0] = 1 (should already be, but good practice)
Bz = Bz / Az(1);
Az = Az / Az(1);

% Display transfer function
H_digital = tf(Bz, Az, Ts, 'Variable', 'z^-1')

%% Spørgsmål 2-4: Verificer digital filter

% (a) Plot magnitude response in dB vs frequency (Hz)
fprintf('(a) Plotting digital magnitude response...\n');

[H, f] = freqz(Bz, Az, 1E4, Fs);  % Match official solution

figure;
plot(f, 20*log10(abs(H)), 'LineWidth', 2);
hold on;

% Add specification lines (blue lines like official solution)
xline(fs_hz, 'b-', 'LineWidth', 2);  % Stopband edge at 450 Hz
xline(fp_hz, 'b-', 'LineWidth', 2);  % Passband edge at 1000 Hz
yline(-30, 'b-', 'LineWidth', 2);    % Stopband requirement
yline(-3, 'b-', 'LineWidth', 2);     % Passband requirement

xlabel('F = f·F_s (Hz)');
ylabel('20log_{10}(|H(F)|) (dB)');
title('Digital Highpass Butterworth Filter');
grid on;
xlim([0 1300]);  % Match official solution range
ylim([-40 5]);

hold off;

% Export figure
exportgraphics(gcf, fullfile(imgDir, ...
    'DSP_Exam_F25_2_4_DigitalHP_Magnitude.png'), 'Resolution', 300);

% (b) Visual verification from plot
fprintf('\n(b) De blå linjer på plottet indikerer de digitale filter kravspecifikationerne\n');

fprintf('(c) Aflæste værdier på plottet:\n');
fprintf('    At 450 Hz: ≈ -34.6 dB (requirement: ≤ -30 dB) ✓\n');
fprintf('    At 1000 Hz: ≈ -3.0 dB (requirement: ≥ -3 dB) ✓\n\n');

fprintf('Filteret opfylder kravspecifikationerne.\n');

%% EKSAMENSOPGAVE 3 (25%)
%% EKSAMENSOPGAVE 3: Sampling, Aliasing, and Inverse Systems

% Given parameters
F1 = 1500; A1 = 3;
F2 = 4200; A2 = 2;
Fs = 8000;

%% Problem 3-1: Full Spectrum

F1=1500; A1=3; F2=4200; A2=2; Fs=8000;
F2_alias = Fs-F2;

% Build replicas
freqs=[]; amps=[]; colors={};
for k=-1:1
    freqs=[freqs, F1+k*Fs, -F1+k*Fs, F2_alias+k*Fs, -F2_alias+k*Fs];
    amps=[amps, A1/2, A1/2, A2/2, A2/2];
    colors=[colors, 'c','c','r','r'];
end

% Plot with LARGER figure size
plot_spectrum(freqs, amps, 'Colors', colors, 'Fs', Fs, ...
    'LegendLabels', {'1500 Hz (OK)', '4200 → 3800 Hz (ALIASED!'}, ...
    'XRange', [-10000,10000], 'XStep', 2000);

% Make figure WIDER
set(gcf, 'Position', [100, 100, 1400, 500]);  % [x, y, width, height]

xline([Fs/2, -Fs/2], '--r', 'LineWidth', 1.5);

% Export with HIGH resolution
exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_3_1_Spectrum.png'), ...
               'Resolution', 300);  % 300 DPI = high quality
%% Problem 3-2: Aliasing?

% Answer: Look at plot above - red arrows show aliased component at 3800 Hz

%% Problem 3-3: Filter analysis

B = [1, 1];
A = [1, -0.7, 0.1];

% H1(z) pole-zero plot
figure;
zplane(B, A);
title('H_1(z)');
exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_3_3_H1.png'), 'Resolution', 300);

% H2(z) inverse pole-zero plot
figure;
zplane(A, B);
title('H_2(z) = 1/H_1(z)');
exportgraphics(gcf, fullfile(imgDir, 'DSP_Exam_F25_3_3_H2.png'), 'Resolution', 300);
%% EKSAMENSOPGAVE 4 (25%)

%  Filter Realization og Signal Filtering
%% Givne filter koefficienter (fra blokdiagram)
% Numerator (feedforward path): b0, b1, b2, b3
b0 = 0.0102;
b1 = 0.0305;
b2 = 0.0305;
b3 = 0.0102;

% Denominator (feedback path): 1, -a1, -a2, -a3
% NB: Fortegnene i diagrammet!
a1 = -2.0038;
a2 = 1.4471;
a3 = -0.3618;

B4 = [b0, b1, b2, b3];
A4 = [1, a1, a2, a3];

Fs4 = 5000;     % Sampling frequency [Hz]

%% Spørgsmål 4-1: Identificer filter

% (1) Hvilken filter form? (Direct Form I, Direct Form II, etc.)
% DIN LØSNING HER:


% (2) FIR eller IIR? Hvorfor?
% DIN LØSNING HER:


% (3) Opskriv H(z)
% DIN LØSNING HER:




%% Spørgsmål 4-2: Plot magnitude response

% (1) Plot |H(F)| i dB
% DIN LØSNING HER:

% [H4, f4] = freqz(B4, A4, 1024, Fs4);
% figure;


% (2) Aflæs -3 dB frekvens, sammenlign med 400 Hz




%% Spørgsmål 4-3: Pole-zero analyse

% (1) Find og plot poler og nulpunkter
% DIN LØSNING HER:

% figure; zplane(B4, A4);


% (2) Er filteret stabilt? (alle poler inden for enhedscirklen?)




%% Spørgsmål 4-4: Sampling af analogt signal

% xa(t) = 5·cos(2π·50·t) + 3·cos(2π·1000·t)

A1_4 = 5;
A2_4 = 3;
F1_4 = 50;      % [Hz]
F2_4 = 1000;    % [Hz]

% (1) Er der aliasing ved Fs = 5000 Hz?
% DIN LØSNING HER:


% (2) Plot samplet signal fra 0 til 0.05 sekunder
% DIN LØSNING HER:

% t = 0 : 1/Fs4 : 0.05;
% x_sampled = A1_4*cos(2*pi*F1_4*t) + A2_4*cos(2*pi*F2_4*t);
% figure;
% plot(t, x_sampled);




%% Spørgsmål 4-5: Filtrer signalet

% (1) Hvad forventes filteret at gøre ved de to frekvenskomponenter?
%     F1 = 50 Hz (i passband?) → ?
%     F2 = 1000 Hz (i stopband?) → ?


% (2) Filtrer med filter() kommandoen
% DIN LØSNING HER:

% y_filtered = filter(B4, A4, x_sampled);
% figure;
% plot(t, y_filtered);


% (3) Kommenter på forskelle mellem input og output signal



%% APPENDIX: Butterworth Lowpass Prototype (ε = 1, 3 dB)

%{
Order n | Denominator polynomial
--------|------------------------------------------
   1    | s + 1
   2    | s^2 + 1.4142s + 1
   3    | s^3 + 2s^2 + 2s + 1
   4    | s^4 + 2.6131s^3 + 3.4142s^2 + 2.6131s + 1
   5    | s^5 + 3.2361s^4 + 5.2361s^3 + 5.2361s^2 + 3.2361s + 1
   6    | s^6 + 3.8637s^5 + 7.4641s^4 + 9.1416s^3 + 7.4641s^2 + 3.8637s + 1

All have numerator = 1
%}

% Prototype polynomials for quick reference:
proto_den{1} = [1, 1];
proto_den{2} = [1, 1.4142, 1];
proto_den{3} = [1, 2, 2, 1];
proto_den{4} = [1, 2.6131, 3.4142, 2.6131, 1];
proto_den{5} = [1, 3.2361, 5.2361, 5.2361, 3.2361, 1];
proto_den{6} = [1, 3.8637, 7.4641, 9.1416, 7.4641, 3.8637, 1];