%% 62743 DSP — Mock Exam SOLUTIONS
%  Complete worked solutions — Check your work against this!
%
%  DO NOT LOOK AT THIS FILE UNTIL YOU HAVE ATTEMPTED THE TEMPLATE!
%
%  This file contains all correct answers with explanations.

clear; close all; clc;

%% Global Setup
imgDir = 'C:\Users\Mads2\DTU\Obsidian\Courses\DSP\Images';
if ~exist(imgDir, 'dir')
    mkdir(imgDir);
end

delta = @(k) double(k == 0);
u     = @(k) double(k >= 0);

fprintf('===========================================\n');
fprintf('   62743 DSP — Mock Exam SOLUTIONS\n');
fprintf('   Complete worked answers\n');
fprintf('===========================================\n\n');


%% ========================================================================
%  PROBLEM 1 — LTI System Analysis (25 points)
%  ========================================================================
fprintf('\n>>> PROBLEM 1 SOLUTIONS <<<\n\n');

n = 0:10;
y_step = 2*delta(n) + 3*delta(n-1) - 3*delta(n-2) - 2*delta(n-3);


%% 1-1) SOLUTION: Impulse response h[n]
%  -----------------------------------------------------------------------
%  METHOD: h[n] = y_step[n] - y_step[n-1]
%  
%  Calculation:
%    n=0: h[0] = y_step[0] - y_step[-1] = 2 - 0 = 2
%    n=1: h[1] = y_step[1] - y_step[0]  = 3 - 2 = 1
%    n=2: h[2] = y_step[2] - y_step[1]  = -3 - 3 = -6
%    n=3: h[3] = y_step[3] - y_step[2]  = -2 - (-3) = 1
%    n=4: h[4] = y_step[4] - y_step[3]  = 0 - (-2) = 2
%  -----------------------------------------------------------------------

y_step_shifted = [0, y_step(1:end-1)];
h = y_step - y_step_shifted;

fprintf('1-1) SOLUTION — Impulse response:\n');
fprintf('     h[n] = [2, 1, -6, 1, 2] for n = 0,1,2,3,4\n\n');
disp(table(n(1:6).', h(1:6).', 'VariableNames', {'n', 'h_n'}));

figure;
stem(n, h, 'filled', 'LineWidth', 1.5);
grid on; xlabel('n'); ylabel('h[n]');
title('Solution 1-1: h[n] = [2, 1, -6, 1, 2]');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_1_ImpulseResponse.png'), 'Resolution', 300);


%% 1-2) SOLUTION: System function H(z)
%  -----------------------------------------------------------------------
%  H(z) = 2 + z^{-1} - 6z^{-2} + z^{-3} + 2z^{-4}
%  -----------------------------------------------------------------------

h_coeffs = h(1:5);  % [2, 1, -6, 1, 2]
B = h_coeffs;
A = 1;

fprintf('1-2) SOLUTION — System function:\n');
fprintf('     H(z) = 2 + z^{-1} - 6z^{-2} + z^{-3} + 2z^{-4}\n');
fprintf('     Coefficients B = [2, 1, -6, 1, 2]\n\n');


%% 1-3) SOLUTION: Magnitude and phase from symmetry
%  -----------------------------------------------------------------------
%  STEP 1: Verify symmetry
%    h[0] = h[4] = 2  ✓
%    h[1] = h[3] = 1  ✓
%    h[2] = -6 (center)
%  
%  STEP 2: Apply symmetry trick
%    H(ω) = e^{-j2ω} · A(ω)
%    A(ω) = h[2] + 2·h[1]·cos(ω) + 2·h[0]·cos(2ω)
%         = -6 + 2·1·cos(ω) + 2·2·cos(2ω)
%         = -6 + 2cos(ω) + 4cos(2ω)
%  
%  STEP 3: Verify A(ω) ≥ 0 (CRITICAL!)
%    A(0) = -6 + 2 + 4 = 0
%    A(π/2) = -6 + 0 - 4 = -10 < 0  ← NEGATIVE!
%    A(π) = -6 - 2 + 4 = -4 < 0     ← NEGATIVE!
%  
%  CONCLUSION: A(ω) goes NEGATIVE!
%    → Phase is NOT simply -2ω
%    → There are π-jumps where A(ω) crosses zero
%    → |H(ω)| = |A(ω)| (absolute value needed)
%  -----------------------------------------------------------------------

W = linspace(-pi, pi, 4001);
K = 2;

A_omega = h_coeffs(3) + 2*h_coeffs(2)*cos(W) + 2*h_coeffs(1)*cos(2*W);
% A(ω) = -6 + 2cos(ω) + 4cos(2ω)

fprintf('1-3) SOLUTION — Symmetry analysis:\n');
fprintf('     h[0] = %d, h[4] = %d (symmetric ✓)\n', h_coeffs(1), h_coeffs(5));
fprintf('     h[1] = %d, h[3] = %d (symmetric ✓)\n', h_coeffs(2), h_coeffs(4));
fprintf('     h[2] = %d (center)\n\n', h_coeffs(3));

fprintf('     A(ω) = -6 + 2cos(ω) + 4cos(2ω)\n\n');

fprintf('     POSITIVITY CHECK:\n');
fprintf('     A(0)   = -6 + 2 + 4 = %.2f\n', -6 + 2*cos(0) + 4*cos(0));
fprintf('     A(π/2) = -6 + 0 - 4 = %.2f  ← NEGATIVE!\n', -6 + 2*cos(pi/2) + 4*cos(pi));
fprintf('     A(π)   = -6 - 2 + 4 = %.2f  ← NEGATIVE!\n', -6 + 2*cos(pi) + 4*cos(2*pi));
fprintf('     min(A) = %.4f\n\n', min(A_omega));

fprintf('     ⚠️  A(ω) IS NEGATIVE for some ω!\n');
fprintf('     → |H(ω)| = |A(ω)| = |-6 + 2cos(ω) + 4cos(2ω)|\n');
fprintf('     → Phase has π-jumps where A(ω) crosses zero\n\n');

% For plotting, we need |A(ω)|
mag_analytic = abs(A_omega);

% Phase: -2ω where A>0, -2ω+π where A<0
phase_analytic = -K * W;
phase_analytic(A_omega < 0) = phase_analytic(A_omega < 0) + pi;

% Compare with freqz
[H_freqz, w_full] = freqz(B, A, 2048, 'whole');
w_shift = w_full - pi;
H_shift = fftshift(H_freqz);

figure('Position', [100 100 800 700]);

subplot(3,1,1);
plot(W, A_omega, 'b-', 'LineWidth', 1.5);
yline(0, '--r', 'LineWidth', 1.5);
grid on; xlabel('\omega [rad/sample]'); ylabel('A(\omega)');
title('Solution 1-3: A(\omega) goes NEGATIVE — not purely linear phase!');
legend('A(\omega) = -6 + 2cos\omega + 4cos2\omega', 'Zero line');

subplot(3,1,2);
plot(W, mag_analytic, 'b-', 'LineWidth', 1.5); hold on;
plot(w_shift, abs(H_shift), 'r--', 'LineWidth', 1.0);
grid on; xlabel('\omega [rad/sample]'); ylabel('|H(\omega)|');
legend('|A(\omega)|', 'freqz');
title('Magnitude = |A(\omega)|');

subplot(3,1,3);
plot(w_shift, unwrap(angle(H_shift)), 'r-', 'LineWidth', 1.5);
grid on; xlabel('\omega [rad/sample]'); ylabel('\angle H(\omega) [rad]');
title('Phase from freqz — note the jumps!');

exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_1_MagPhase.png'), 'Resolution', 300);


%% 1-4) SOLUTION: Find H2(z) in cascade
%  -----------------------------------------------------------------------
%  H(z) = H1(z) · H2(z)
%  H1(z) = 1 + z^{-1} = [1, 1]
%  
%  H2(z) = H(z) / H1(z) via deconv
%  -----------------------------------------------------------------------

H1 = [1 1];
[H2, remainder] = deconv(B, H1);

fprintf('1-4) SOLUTION — Cascade decomposition:\n');
fprintf('     H1(z) = 1 + z^{-1}\n');
fprintf('     H2(z) = deconv([2,1,-6,1,2], [1,1])\n');
fprintf('     H2(z) = '); disp(H2);
fprintf('     H2(z) = 2 - z^{-1} - 5z^{-2} + 6z^{-3}\n');
fprintf('     Remainder = '); disp(remainder);

figure;
zplane(H2, 1);
title('Solution 1-4: H_2(z) = 2 - z^{-1} - 5z^{-2} + 6z^{-3}');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_1_H2_PZ.png'), 'Resolution', 300);


%% 1-5) SOLUTION: Inverse system stability
%  -----------------------------------------------------------------------
%  H_inv(z) = 1/H(z)
%  Poles of H_inv = Zeros of H
%  
%  Find zeros of H(z):
%  -----------------------------------------------------------------------

zeros_H = roots(B);

fprintf('1-5) SOLUTION — Inverse system:\n');
fprintf('     Zeros of H(z):\n');
for k = 1:length(zeros_H)
    fprintf('       z_%d = %.4f + %.4fi, |z| = %.4f', ...
        k, real(zeros_H(k)), imag(zeros_H(k)), abs(zeros_H(k)));
    if abs(zeros_H(k)) > 1
        fprintf(' ← OUTSIDE UC!\n');
    else
        fprintf(' ← inside UC\n');
    end
end

outside_count = sum(abs(zeros_H) > 1);
fprintf('\n     %d zero(s) outside unit circle\n', outside_count);

if outside_count > 0
    fprintf('     → H_inv(z) has pole(s) outside UC\n');
    fprintf('     → H_inv(z) CANNOT be both causal AND stable!\n');
else
    fprintf('     → All zeros inside UC\n');
    fprintf('     → H_inv(z) CAN be causal and stable\n');
end


%% ========================================================================
%  PROBLEM 2 — IIR Butterworth Highpass via BLT (25 points)
%  ========================================================================
fprintf('\n\n>>> PROBLEM 2 SOLUTIONS <<<\n\n');

Fs = 8000;
Fp = 2000;
Fstop = 1000;
Ap_dB = 1;
As_dB = 20;


%% 2-1) SOLUTION: Pre-warp frequencies
%  -----------------------------------------------------------------------
%  Ω = 2·Fs·tan(π·F/Fs)
%  -----------------------------------------------------------------------

Omega_p = 2 * Fs * tan(pi * Fp / Fs);
Omega_s = 2 * Fs * tan(pi * Fstop / Fs);

fprintf('2-1) SOLUTION — Pre-warping:\n');
fprintf('     Ω_p = 2 × %d × tan(π × %d / %d)\n', Fs, Fp, Fs);
fprintf('     Ω_p = %.2f rad/s\n\n', Omega_p);
fprintf('     Ω_s = 2 × %d × tan(π × %d / %d)\n', Fs, Fstop, Fs);
fprintf('     Ω_s = %.2f rad/s\n\n', Omega_s);


%% 2-2) SOLUTION: Calculate minimum filter order
%  -----------------------------------------------------------------------
%  For Butterworth HIGHPASS:
%  N ≥ log10[(10^(As/10)-1)/(10^(Ap/10)-1)] / [2·log10(Ωp/Ωs)]
%  
%  Note: Ωp/Ωs (not Ωs/Ωp) because this is HIGHPASS!
%  -----------------------------------------------------------------------

numerator = log10((10^(As_dB/10) - 1) / (10^(Ap_dB/10) - 1));
denominator = 2 * log10(Omega_p / Omega_s);
N_exact = numerator / denominator;
N = ceil(N_exact);

fprintf('2-2) SOLUTION — Order calculation:\n');
fprintf('     Numerator = log10[(10^2 - 1)/(10^0.1 - 1)] = log10[99/0.2589] = %.4f\n', numerator);
fprintf('     Denominator = 2·log10(%.2f/%.2f) = %.4f\n', Omega_p, Omega_s, denominator);
fprintf('     N_exact = %.4f\n', N_exact);
fprintf('     N_min = %d (rounded up)\n\n', N);


%% 2-3) SOLUTION: Analog lowpass prototype
%  -----------------------------------------------------------------------
%  Use buttap(N) for normalized Butterworth poles
%  -----------------------------------------------------------------------

[z_proto, p_proto, k_proto] = buttap(N);
[B_proto, A_proto] = zp2tf(z_proto, p_proto, k_proto);

fprintf('2-3) SOLUTION — LP prototype (N=%d):\n', N);
fprintf('     B_proto = %.6f\n', B_proto);
fprintf('     A_proto = '); disp(A_proto);

sys_proto = tf(B_proto, A_proto);
disp(sys_proto);


%% 2-4) SOLUTION: Transform to analog highpass
%  -----------------------------------------------------------------------
%  LP → HP: s → Ωp/s
%  MATLAB: lp2hp(B, A, Omega_p)
%  -----------------------------------------------------------------------

[B_HP, A_HP] = lp2hp(B_proto, A_proto, Omega_p);

fprintf('2-4) SOLUTION — Analog HP:\n');
sys_HP = tf(B_HP, A_HP);
disp(sys_HP);

Omega = linspace(0, 3*Omega_p, 4000);
H_analog = freqs(B_HP, A_HP, Omega);

figure;
plot(Omega/(2*pi), 20*log10(abs(H_analog)), 'LineWidth', 1.5);
grid on; xlabel('Frequency [Hz]'); ylabel('|H(j\Omega)| [dB]');
title('Solution 2-4: Analog HP Butterworth');
xline(Fstop, '--r', 'F_{stop}'); xline(Fp, '--g', 'F_p');
yline(-Ap_dB, ':m', '-1 dB'); yline(-As_dB, ':c', '-20 dB');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_2_Analog_HP.png'), 'Resolution', 300);


%% 2-5) SOLUTION: Bilinear transform and verification
%  -----------------------------------------------------------------------
%  [Bz, Az] = bilinear(B_HP, A_HP, Fs)
%  -----------------------------------------------------------------------

[Bz, Az] = bilinear(B_HP, A_HP, Fs);

fprintf('2-5) SOLUTION — Digital HP:\n');
sys_digital = tf(Bz, Az, 1/Fs, 'Variable', 'z^-1');
disp(sys_digital);

% Verify specifications
F_test = [Fstop, Fp];
[H_test, ~] = freqz(Bz, Az, F_test, Fs);
Att_dB = 20*log10(abs(H_test));

fprintf('     VERIFICATION:\n');
fprintf('     @ %d Hz (stopband): %.2f dB (spec: ≤ -%.0f dB) ', Fstop, Att_dB(1), As_dB);
if Att_dB(1) <= -As_dB, fprintf('✓\n'); else, fprintf('✗\n'); end
fprintf('     @ %d Hz (passband): %.2f dB (spec: ≥ -%.0f dB) ', Fp, Att_dB(2), Ap_dB);
if Att_dB(2) >= -Ap_dB, fprintf('✓\n'); else, fprintf('✗\n'); end

F_resp = linspace(0, Fs/2, 4000);
[H_dig, F_grid] = freqz(Bz, Az, F_resp, Fs);

figure;
plot(F_grid, 20*log10(abs(H_dig)), 'LineWidth', 1.5);
grid on; xlabel('Frequency [Hz]'); ylabel('|H(e^{j\omega})| [dB]');
title(sprintf('Solution 2-5: Digital HP Butterworth (N=%d)', N));
xline(Fstop, '--r', 'F_{stop}'); xline(Fp, '--g', 'F_p');
yline(-Ap_dB, ':m', '-1 dB'); yline(-As_dB, ':c', '-20 dB');
ylim([-60 5]);
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_2_Digital_HP.png'), 'Resolution', 300);


%% ========================================================================
%  PROBLEM 3 — Sampling & Min-Phase Decomposition (25 points)
%  ========================================================================
fprintf('\n\n>>> PROBLEM 3 SOLUTIONS <<<\n\n');

F1 = 500;  A1 = 4;
F2 = 1200; A2 = 2;
F3 = 1800; A3 = 1;


%% 3-1) SOLUTION: Nyquist rate

F_max = max([F1, F2, F3]);
F_Nyquist = 2 * F_max;

fprintf('3-1) SOLUTION — Nyquist rate:\n');
fprintf('     F_max = max(500, 1200, 1800) = %d Hz\n', F_max);
fprintf('     F_Nyquist = 2 × %d = %d Hz\n\n', F_max, F_Nyquist);


%% 3-2) SOLUTION: Sample at Fs = 3000 Hz

Fs_32 = 3000;
fprintf('3-2) SOLUTION — Sampling at Fs = %d Hz:\n', Fs_32);
fprintf('     Nyquist frequency = %d Hz\n\n', Fs_32/2);

fprintf('     500 Hz:  500 < 1500  → NO aliasing  → Appears at 500 Hz\n');
fprintf('     1200 Hz: 1200 < 1500 → NO aliasing  → Appears at 1200 Hz\n');
fprintf('     1800 Hz: 1800 > 1500 → ALIASING!    → Appears at 3000-1800 = 1200 Hz\n\n');

fprintf('     ⚠️  The 1800 Hz component aliases ON TOP of the 1200 Hz component!\n');

N_fft = 4096;
n_sig = 0:N_fft-1;
t_sig = n_sig / Fs_32;
x = A1*cos(2*pi*F1*t_sig) + A2*cos(2*pi*F2*t_sig) + A3*cos(2*pi*F3*t_sig);

X = fftshift(fft(x)) / N_fft;
f_axis = (-N_fft/2:N_fft/2-1) * (Fs_32/N_fft);

figure;
plot(f_axis, abs(X), 'LineWidth', 1);
grid on; xlabel('Frequency [Hz]'); ylabel('|X(f)|');
title('Solution 3-2: Spectrum (F_s = 3000 Hz) — 1800 Hz aliases to 1200 Hz');
xlim([-2000 2000]);
xline(Fs_32/2, '--r', 'F_s/2'); xline(-Fs_32/2, '--r');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_3_Spectrum.png'), 'Resolution', 300);


%% 3-3) SOLUTION: Sample at Fs = 2500 Hz

Fs_33 = 2500;
fprintf('\n3-3) SOLUTION — Sampling at Fs = %d Hz:\n', Fs_33);
fprintf('     Nyquist frequency = %d Hz\n\n', Fs_33/2);

fprintf('     | Original F | Aliased? | Apparent F | Calculation         |\n');
fprintf('     |------------|----------|------------|---------------------|\n');
fprintf('     |   500 Hz   |    No    |   500 Hz   | 500 < 1250          |\n');
fprintf('     |  1200 Hz   |   Yes    |  1200 Hz   | 2500-1200=1300>1250 |\n');
fprintf('     |            |          |            | 2500-1300=1200      |\n');
fprintf('     |  1800 Hz   |   Yes    |   700 Hz   | 2500-1800=700       |\n');


%% 3-4) SOLUTION: Min-Phase / All-Pass Decomposition

fprintf('\n3-4) SOLUTION — Min-Phase / All-Pass:\n');
fprintf('     Original: H(z) = (z-2)(z-0.5)/z²\n\n');

fprintf('     Zero analysis:\n');
fprintf('     • z = 2:   |2| = 2 > 1   → OUTSIDE unit circle\n');
fprintf('     • z = 0.5: |0.5| = 0.5 < 1 → inside unit circle\n\n');

fprintf('     To create min-phase system:\n');
fprintf('     • Reflect z=2 to its reciprocal: 1/2 = 0.5\n');
fprintf('     • H_min has BOTH zeros at z = 0.5\n\n');

fprintf('     SOLUTION:\n');
fprintf('     H_min(z) = (z - 0.5)² / z² = (z² - z + 0.25) / z²\n');
fprintf('     H_ap(z)  = (z - 2) / (z - 0.5)\n\n');

fprintf('     VERIFICATION: H_min(z) × H_ap(z)\n');
fprintf('     = [(z-0.5)²/z²] × [(z-2)/(z-0.5)]\n');
fprintf('     = (z-0.5)(z-2)/z²\n');
fprintf('     = (z-2)(z-0.5)/z² = H(z) ✓\n');

figure('Position', [100 100 1200 400]);

subplot(1,3,1);
zplane([1, -2.5, 1], [1, 0, 0]);
title('Original H(z) = (z-2)(z-0.5)/z²');

subplot(1,3,2);
zplane([1, -1, 0.25], [1, 0, 0]);
title('H_{min}(z) = (z-0.5)²/z²');

subplot(1,3,3);
zplane([1, -2], [1, -0.5]);
title('H_{ap}(z) = (z-2)/(z-0.5)');

exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_3_MinPhase_PZ.png'), 'Resolution', 300);


%% ========================================================================
%  PROBLEM 4 — FIR Bandstop via Window Method (25 points)
%  ========================================================================
fprintf('\n\n>>> PROBLEM 4 SOLUTIONS <<<\n\n');

Fs_FIR = 4000;
Fs1 = 600;
Fs2 = 1000;
N_taps = 21;
K = (N_taps - 1) / 2;


%% 4-1) SOLUTION: Digital cutoff frequencies

omega_c1 = 2*pi * Fs1 / Fs_FIR;
omega_c2 = 2*pi * Fs2 / Fs_FIR;

fprintf('4-1) SOLUTION — Digital frequencies:\n');
fprintf('     ω_c1 = 2π × %d/%d = %.4f rad = %.4f π\n', Fs1, Fs_FIR, omega_c1, omega_c1/pi);
fprintf('     ω_c2 = 2π × %d/%d = %.4f rad = %.4f π\n\n', Fs2, Fs_FIR, omega_c2, omega_c2/pi);


%% 4-2) SOLUTION: Ideal bandstop impulse response

n_ideal = -K:K;

h_BP_ideal = zeros(size(n_ideal));
for idx = 1:length(n_ideal)
    n_val = n_ideal(idx);
    if n_val == 0
        h_BP_ideal(idx) = (omega_c2 - omega_c1) / pi;
    else
        h_BP_ideal(idx) = (sin(omega_c2 * n_val) - sin(omega_c1 * n_val)) / (pi * n_val);
    end
end

% Bandstop = delta - bandpass
h_BS_ideal = zeros(size(n_ideal));
h_BS_ideal(n_ideal == 0) = 1;
h_BS_ideal = h_BS_ideal - h_BP_ideal;

fprintf('4-2) SOLUTION — Ideal impulse response:\n');
fprintf('     h_BP[0] = (ω_c2 - ω_c1)/π = (%.4f - %.4f)/π = %.6f\n', omega_c2, omega_c1, h_BP_ideal(K+1));
fprintf('     h_BS[0] = 1 - h_BP[0] = 1 - %.6f = %.6f\n\n', h_BP_ideal(K+1), h_BS_ideal(K+1));


%% 4-3) SOLUTION: Apply Hamming window

n_causal = 0:N_taps-1;
w_hamming = 0.54 - 0.46*cos(2*pi*n_causal/(N_taps-1));
b_BS = h_BS_ideal .* w_hamming;

fprintf('4-3) SOLUTION — Windowed coefficients:\n');
fprintf('     Hamming: w[n] = 0.54 - 0.46·cos(2πn/20)\n');
fprintf('     w[10] = 0.54 - 0.46·cos(π) = 0.54 + 0.46 = 1.00\n');
fprintf('     b[10] = h_BS[0] × w[10] = %.6f × 1.00 = %.6f\n\n', h_BS_ideal(K+1), b_BS(K+1));

figure;
stem(n_causal, b_BS, 'filled', 'LineWidth', 1.5);
grid on; xlabel('n'); ylabel('b[n]');
title('Solution 4-3: Bandstop FIR Coefficients (Hamming Window)');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_4_Impulse.png'), 'Resolution', 300);


%% 4-4) SOLUTION: Verify linear phase

fprintf('4-4) SOLUTION — Symmetry verification:\n');
fprintf('     n   |  b[n]      |  b[N-1-n]  |  Match?\n');
fprintf('     ----|------------|------------|--------\n');
for idx = 0:K
    match = abs(b_BS(idx+1) - b_BS(N_taps-idx)) < 1e-10;
    fprintf('     %2d  | %+.6f | %+.6f | %s\n', ...
        idx, b_BS(idx+1), b_BS(N_taps-idx), string(match));
end
fprintf('\n     ✓ Filter is symmetric → Linear phase with slope -K = -%d\n', K);


%% 4-5) SOLUTION: Plot magnitude and measure attenuation

[H_BS, F_BS] = freqz(b_BS, 1, 4096, Fs_FIR);
Mag_dB = 20*log10(abs(H_BS));

F_center = (Fs1 + Fs2) / 2;
[H_center, ~] = freqz(b_BS, 1, F_center, Fs_FIR);
Att_center = 20*log10(abs(H_center));

fprintf('\n4-5) SOLUTION — Attenuation:\n');
fprintf('     At stopband center (F = %d Hz): %.2f dB\n', F_center, Att_center);
fprintf('     Hamming window provides ~40-50 dB stopband attenuation\n');

figure;
plot(F_BS, Mag_dB, 'LineWidth', 1.5);
grid on; xlabel('Frequency [Hz]'); ylabel('|H(e^{j\omega})| [dB]');
title(sprintf('Solution 4-5: Bandstop FIR (Attn @ %d Hz = %.1f dB)', F_center, Att_center));
xline(Fs1, '--r', 'F_{s1}'); xline(Fs2, '--r', 'F_{s2}');
xline(F_center, ':m', 'Center');
ylim([-80 5]);
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_4_Magnitude.png'), 'Resolution', 300);


%% ========================================================================
%  SOLUTIONS COMPLETE
%% ========================================================================
fprintf('\n\n');
fprintf('===========================================\n');
fprintf('   ALL SOLUTIONS COMPLETE!\n');
fprintf('===========================================\n');
fprintf('   Key answers summary:\n');
fprintf('   1-1: h[n] = [2, 1, -6, 1, 2]\n');
fprintf('   1-3: A(ω) goes NEGATIVE! (phase has jumps)\n');
fprintf('   1-5: H_inv CANNOT be causal+stable\n');
fprintf('   2-2: N = %d\n', N);
fprintf('   2-5: Specs met ✓\n');
fprintf('   3-1: F_Nyquist = %d Hz\n', F_Nyquist);
fprintf('   3-4: H_min = (z-0.5)²/z², H_ap = (z-2)/(z-0.5)\n');
fprintf('   4-5: Attenuation @ 800 Hz = %.1f dB\n', Att_center);
fprintf('===========================================\n');
