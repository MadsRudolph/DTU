%% 62743 DSP — Mock Exam TEMPLATE
%  Student Workspace — Fill in your solutions!
%
%  Instructions:
%  1. Read each problem in the Obsidian note (Mock_Exam_DSP.md)
%  2. Write your solution code where indicated
%  3. Run each section to check your work
%  4. Compare with SOLUTIONS file when done
%
%  HINTS are provided but solutions are NOT given!

clear; close all; clc;

%% Global Setup — DO NOT MODIFY
imgDir = 'C:\Users\Mads2\DTU\Obsidian\Courses\DSP\Images';
if ~exist(imgDir, 'dir')
    mkdir(imgDir);
end

delta = @(k) double(k == 0);
u     = @(k) double(k >= 0);

fprintf('===========================================\n');
fprintf('   62743 DSP — Mock Exam TEMPLATE\n');
fprintf('   Fill in your solutions below!\n');
fprintf('===========================================\n\n');


%% ========================================================================
%  PROBLEM 1 — LTI System Analysis (25 points)
%  ========================================================================
%
%  Given step response:
%    y_step[n] = 2δ[n] + 3δ[n-1] - 3δ[n-2] - 2δ[n-3]
%
%  Cascade structure: H(z) = H1(z) · H2(z), where H1(z) = 1 + z^{-1}
%
%  ========================================================================
fprintf('\n>>> PROBLEM 1: LTI System Analysis <<<\n\n');

n = 0:10;

% Given: Step response (DO NOT MODIFY)
y_step = 2*delta(n) + 3*delta(n-1) - 3*delta(n-2) - 2*delta(n-3);


%% 1-1) Find impulse response h[n] (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Compute h[n] from y_step[n]
%  
%  HINT: Use the relation δ[n] = u[n] - u[n-1]
%        Therefore: h[n] = y_step[n] - y_step[n-1]
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
h = zeros(size(n));  % Replace this line with your calculation!

% Step 1: Create shifted step response y_step[n-1]
% y_step_shifted = ???

% Step 2: Compute first difference
% h = ???

% ==============================================================

fprintf('1-1) Your impulse response h[n]:\n');
disp(table(n(1:6).', h(1:6).', 'VariableNames', {'n', 'h_n'}));

% Plot your result
figure;
stem(n, h, 'filled', 'LineWidth', 1.5);
grid on; xlabel('n'); ylabel('h[n]');
title('Problem 1-1: Your Impulse Response h[n]');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_1_ImpulseResponse.png'), 'Resolution', 300);


%% 1-2) Find system function H(z) (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Write H(z) from your h[n]
%  
%  HINT: For causal FIR: H(z) = Σ h[n] z^{-n}
%        Just extract the non-zero coefficients as a vector
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
% Extract non-zero support of h[n] as coefficient vector B
B = [];  % Replace with your coefficients [h[0], h[1], h[2], ...]
A = 1;   % FIR denominator (keep as 1)

% ==============================================================

fprintf('1-2) Your H(z) coefficients B = '); disp(B);


%% 1-3) Magnitude and phase from symmetry (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Find |H(ω)| and ∠H(ω) using the symmetry trick
%  
%  HINT: 
%    1. Check if h[n] is symmetric: h[0]=h[4]? h[1]=h[3]?
%    2. For length-5 symmetric FIR, center is K = 2
%    3. Factor: H(ω) = e^{-j2ω} · A(ω)
%    4. A(ω) = h[2] + 2·h[1]·cos(ω) + 2·h[0]·cos(2ω)
%    5. CRITICAL: Verify A(ω) ≥ 0 before claiming linear phase!
%  -----------------------------------------------------------------------

W = linspace(-pi, pi, 4001);

% ===================== YOUR SOLUTION HERE =====================
% Step 1: Check symmetry (fill in the fprintf)
fprintf('1-3) Symmetry check:\n');
fprintf('     h[0] = ???, h[4] = ??? (should match)\n');
fprintf('     h[1] = ???, h[3] = ??? (should match)\n');

% Step 2: Calculate analytic magnitude A(ω)
K = 2;  % Center index for length-5 FIR
A_omega = zeros(size(W));  % Replace with: h[2] + 2*h[1]*cos(W) + 2*h[0]*cos(2*W)

% Step 3: Analytic phase (linear phase)
phase_analytic = zeros(size(W));  % Replace with: -K * W

% Step 4: CRITICAL — Verify A(ω) ≥ 0
fprintf('\n     Positivity check:\n');
fprintf('     min(A(ω)) = ??? (must be >= 0!)\n');

% ==============================================================

% Compare with freqz (verification)
[H_freqz, w_full] = freqz(B, A, 2048, 'whole');
w_shift = w_full - pi;
H_shift = fftshift(H_freqz);

figure('Position', [100 100 800 600]);
subplot(2,1,1);
plot(W, A_omega, 'b-', 'LineWidth', 1.5); hold on;
plot(w_shift, abs(H_shift), 'r--', 'LineWidth', 1.0);
yline(0, '--k');
grid on; xlabel('\omega [rad/sample]'); ylabel('|H(\omega)|');
legend('Your A(\omega)', 'freqz (verification)', 'Location', 'best');
title('Problem 1-3: Magnitude Response');

subplot(2,1,2);
plot(W, phase_analytic, 'b-', 'LineWidth', 1.5); hold on;
plot(w_shift, unwrap(angle(H_shift)), 'r--', 'LineWidth', 1.0);
grid on; xlabel('\omega [rad/sample]'); ylabel('\angle H(\omega) [rad]');
legend('Your phase', 'freqz (verification)', 'Location', 'best');
title('Problem 1-3: Phase Response');

exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_1_MagPhase.png'), 'Resolution', 300);


%% 1-4) Find H2(z) in cascade (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Given H(z) = H1(z)·H2(z) with H1(z) = 1 + z^{-1}, find H2(z)
%  
%  HINT: Use polynomial division: H2 = H / H1
%        MATLAB: [H2, remainder] = deconv(B, H1)
%        The remainder should be approximately zero
%  -----------------------------------------------------------------------

H1 = [1 1];  % H1(z) = 1 + z^{-1}

% ===================== YOUR SOLUTION HERE =====================
H2 = [];        % Replace with your deconv result
remainder = []; % Check this is ~0

% ==============================================================

fprintf('1-4) Your H2(z) coefficients: '); disp(H2);
fprintf('     Remainder (should be ~0): '); disp(remainder);

figure;
zplane(H2, 1);
title('Problem 1-4: Pole-Zero Plot of Your H_2(z)');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_1_H2_PZ.png'), 'Resolution', 300);


%% 1-5) Inverse system stability (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Can H_inv(z) = 1/H(z) be both causal AND stable?
%  
%  HINT: 
%    - Poles of H_inv = Zeros of H
%    - For causal+stable: ALL poles must be inside unit circle
%    - So check: Are ALL zeros of H(z) inside |z| < 1?
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
% Step 1: Find zeros of H(z)
zeros_H = [];  % Use roots(B)

% Step 2: Check magnitudes
fprintf('1-5) Zeros of H(z):\n');
% for each zero, print its value and magnitude |z|

% Step 3: Conclusion
% Can H_inv be causal and stable? Why or why not?
fprintf('\n     Your conclusion: ???\n');

% ==============================================================


%% ========================================================================
%  PROBLEM 2 — IIR Butterworth Highpass via BLT (25 points)
%  ========================================================================
%
%  Specifications:
%    Fs = 8000 Hz, Fp = 2000 Hz, Fstop = 1000 Hz
%    Ap = 1 dB (passband ripple), As = 20 dB (stopband attenuation)
%
%  ========================================================================
fprintf('\n\n>>> PROBLEM 2: IIR Butterworth HP via BLT <<<\n\n');

Fs = 8000;
Fp = 2000;
Fstop = 1000;
Ap_dB = 1;
As_dB = 20;

fprintf('Specifications: Fs=%d Hz, Fp=%d Hz, Fstop=%d Hz\n', Fs, Fp, Fstop);
fprintf('               Ap=%.1f dB, As=%.1f dB\n', Ap_dB, As_dB);


%% 2-1) Pre-warp frequencies (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Calculate pre-warped analog frequencies Ωp and Ωs
%  
%  HINT: Ω = 2·Fs·tan(π·F/Fs)
%        NEVER use Hz directly in analog prototype formulas!
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
Omega_p = 0;  % Replace with prewarped passband frequency
Omega_s = 0;  % Replace with prewarped stopband frequency

% ==============================================================

fprintf('2-1) Your pre-warped frequencies:\n');
fprintf('     Ω_p = %.2f rad/s\n', Omega_p);
fprintf('     Ω_s = %.2f rad/s\n', Omega_s);


%% 2-2) Calculate minimum filter order (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Find minimum Butterworth order N
%  
%  HINT: N ≥ log10[(10^(As/10)-1)/(10^(Ap/10)-1)] / [2·log10(Ωp/Ωs)]
%        Note: For HIGHPASS, ratio is Ωp/Ωs (not Ωs/Ωp)!
%        Round UP to nearest integer
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
N_exact = 0;  % Calculate using the formula
N = 0;        % Ceiling of N_exact

% ==============================================================

fprintf('2-2) Your order calculation:\n');
fprintf('     N_exact = %.4f\n', N_exact);
fprintf('     N_min = %d\n', N);


%% 2-3) Analog lowpass prototype (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Get the normalized Butterworth LP prototype of order N
%  
%  HINT: Use buttap(N) to get poles, then zp2tf to get B, A
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
% [z_proto, p_proto, k_proto] = buttap(???);
% [B_proto, A_proto] = zp2tf(???);
B_proto = [];
A_proto = [];

% ==============================================================

fprintf('2-3) Your LP prototype:\n');
fprintf('     B_proto = '); disp(B_proto);
fprintf('     A_proto = '); disp(A_proto);


%% 2-4) Transform to analog highpass (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Apply LP → HP transformation
%  
%  HINT: Use lp2hp(B_proto, A_proto, Omega_p)
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
B_HP = [];  % Result of lp2hp
A_HP = [];

% ==============================================================

fprintf('2-4) Your analog HP coefficients:\n');
fprintf('     B_HP has %d coefficients\n', length(B_HP));
fprintf('     A_HP has %d coefficients\n', length(A_HP));

% Plot analog response
if ~isempty(B_HP) && ~isempty(A_HP)
    Omega = linspace(0, 3*Omega_p, 4000);
    H_analog = freqs(B_HP, A_HP, Omega);
    
    figure;
    plot(Omega/(2*pi), 20*log10(abs(H_analog)), 'LineWidth', 1.5);
    grid on; xlabel('Frequency [Hz]'); ylabel('|H(j\Omega)| [dB]');
    title('Problem 2-4: Your Analog HP Response');
    xline(Fstop, '--r', 'F_{stop}');
    xline(Fp, '--g', 'F_p');
    exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_2_Analog_HP.png'), 'Resolution', 300);
end


%% 2-5) Bilinear transform and verification (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Apply BLT to get digital filter, verify specs
%  
%  HINT: [Bz, Az] = bilinear(B_HP, A_HP, Fs)
%        Check attenuation at Fp and Fstop using freqz
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
Bz = [];  % Result of bilinear
Az = [];

% ==============================================================

% Verification (runs if you filled in Bz, Az)
if ~isempty(Bz) && ~isempty(Az)
    F_test = [Fstop, Fp];
    [H_test, ~] = freqz(Bz, Az, F_test, Fs);
    Att_dB = 20*log10(abs(H_test));
    
    fprintf('2-5) Specification verification:\n');
    fprintf('     @ %d Hz: %.2f dB (spec: ≤ -%.0f dB)\n', Fstop, Att_dB(1), As_dB);
    fprintf('     @ %d Hz: %.2f dB (spec: ≥ -%.0f dB)\n', Fp, Att_dB(2), Ap_dB);
    
    % Plot
    F_resp = linspace(0, Fs/2, 4000);
    [H_dig, F_grid] = freqz(Bz, Az, F_resp, Fs);
    
    figure;
    plot(F_grid, 20*log10(abs(H_dig)), 'LineWidth', 1.5);
    grid on; xlabel('Frequency [Hz]'); ylabel('|H(e^{j\omega})| [dB]');
    title('Problem 2-5: Your Digital HP Response');
    xline(Fstop, '--r', 'F_{stop}'); xline(Fp, '--g', 'F_p');
    yline(-Ap_dB, ':m'); yline(-As_dB, ':c');
    ylim([-60 5]);
    exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_2_Digital_HP.png'), 'Resolution', 300);
end


%% ========================================================================
%  PROBLEM 3 — Sampling & Min-Phase Decomposition (25 points)
%  ========================================================================
%
%  Signal: x_a(t) = 4cos(2π·500t) + 2cos(2π·1200t) + cos(2π·1800t)
%
%  ========================================================================
fprintf('\n\n>>> PROBLEM 3: Sampling & Min-Phase <<<\n\n');

F1 = 500;  A1 = 4;
F2 = 1200; A2 = 2;
F3 = 1800; A3 = 1;


%% 3-1) Nyquist rate (3 pts)
%  -----------------------------------------------------------------------
%  TASK: What is minimum Fs to avoid aliasing?
%  
%  HINT: F_Nyquist > 2·F_max
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
F_max = 0;       % Highest frequency in signal
F_Nyquist = 0;   % Minimum sampling rate

% ==============================================================

fprintf('3-1) Your Nyquist calculation:\n');
fprintf('     F_max = %d Hz\n', F_max);
fprintf('     F_Nyquist = %d Hz\n', F_Nyquist);


%% 3-2) Sample at Fs = 3000 Hz (7 pts)
%  -----------------------------------------------------------------------
%  TASK: Does aliasing occur? What are the apparent frequencies?
%  
%  HINT: 
%    - Nyquist frequency = Fs/2 = 1500 Hz
%    - If F > Fs/2, it aliases to F_apparent = Fs - F
%    - Digital frequency: ω = 2π·F/Fs
%  -----------------------------------------------------------------------

Fs_32 = 3000;
fprintf('\n3-2) Sampling at Fs = %d Hz (Nyquist = %d Hz):\n', Fs_32, Fs_32/2);

% ===================== YOUR SOLUTION HERE =====================
% For each frequency component, determine:
%   - Does it alias? (is F > Fs/2?)
%   - What is the apparent frequency after sampling?

fprintf('     500 Hz  → Aliased? ??? → Apparent: ??? Hz\n');
fprintf('     1200 Hz → Aliased? ??? → Apparent: ??? Hz\n');
fprintf('     1800 Hz → Aliased? ??? → Apparent: ??? Hz\n');

% ==============================================================

% Generate spectrum plot
N_fft = 4096;
n_sig = 0:N_fft-1;
t_sig = n_sig / Fs_32;
x = A1*cos(2*pi*F1*t_sig) + A2*cos(2*pi*F2*t_sig) + A3*cos(2*pi*F3*t_sig);

X = fftshift(fft(x)) / N_fft;
f_axis = (-N_fft/2:N_fft/2-1) * (Fs_32/N_fft);

figure;
plot(f_axis, abs(X), 'LineWidth', 1);
grid on; xlabel('Frequency [Hz]'); ylabel('|X(f)|');
title(sprintf('Problem 3-2: Spectrum (F_s = %d Hz)', Fs_32));
xlim([-2000 2000]);
xline(Fs_32/2, '--r', 'F_s/2'); xline(-Fs_32/2, '--r', '-F_s/2');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_3_Spectrum.png'), 'Resolution', 300);


%% 3-3) Sample at Fs = 2500 Hz (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Which components alias? What are apparent frequencies?
%  
%  HINT: Nyquist = 1250 Hz now. More aliasing!
%  -----------------------------------------------------------------------

Fs_33 = 2500;
fprintf('\n3-3) Sampling at Fs = %d Hz (Nyquist = %d Hz):\n', Fs_33, Fs_33/2);

% ===================== YOUR SOLUTION HERE =====================
fprintf('     | Original F | Aliased? | Apparent F |\n');
fprintf('     |------------|----------|------------|\n');
fprintf('     |   500 Hz   |   ???    |   ??? Hz   |\n');
fprintf('     |  1200 Hz   |   ???    |   ??? Hz   |\n');
fprintf('     |  1800 Hz   |   ???    |   ??? Hz   |\n');

% ==============================================================


%% 3-4) Min-Phase / All-Pass Decomposition (10 pts)
%  -----------------------------------------------------------------------
%  TASK: Decompose H(z) = (z-2)(z-0.5)/z² into H_min(z)·H_ap(z)
%  
%  HINT:
%    - z = 2 is OUTSIDE unit circle (|2| > 1)
%    - z = 0.5 is INSIDE unit circle (|0.5| < 1)
%    - To make min-phase: reflect z=2 to its reciprocal 1/2 = 0.5
%    - All-pass compensates: H_ap = (z-2)/(z-0.5)
%    - Result: H_min has BOTH zeros at 0.5
%  -----------------------------------------------------------------------

fprintf('\n3-4) Min-Phase / All-Pass Decomposition:\n');
fprintf('     Original H(z) = (z-2)(z-0.5)/z²\n\n');

% ===================== YOUR SOLUTION HERE =====================
% Identify which zeros are inside/outside unit circle
fprintf('     Zero at z = 2:   |z| = ??? (inside/outside UC?)\n');
fprintf('     Zero at z = 0.5: |z| = ??? (inside/outside UC?)\n\n');

% Write your decomposition
fprintf('     Your H_min(z) = ???\n');
fprintf('     Your H_ap(z)  = ???\n');

% ==============================================================

% Pole-zero plots for visualization
figure('Position', [100 100 1000 400]);

subplot(1,3,1);
% Original: (z-2)(z-0.5)/z^2 = (z^2 - 2.5z + 1)/z^2
zplane([1, -2.5, 1], [1, 0, 0]);
title('Original H(z)');

subplot(1,3,2);
% Your H_min — fill in the coefficients!
% zplane([???], [???]);
title('Your H_{min}(z)');

subplot(1,3,3);
% Your H_ap — fill in the coefficients!
% zplane([???], [???]);
title('Your H_{ap}(z)');

exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_3_MinPhase_PZ.png'), 'Resolution', 300);


%% ========================================================================
%  PROBLEM 4 — FIR Bandstop via Window Method (25 points)
%  ========================================================================
%
%  Specifications:
%    Fs = 4000 Hz, Stopband = [600, 1000] Hz, N = 21 taps, Hamming window
%
%  ========================================================================
fprintf('\n\n>>> PROBLEM 4: FIR Bandstop via Window <<<\n\n');

Fs_FIR = 4000;
Fs1 = 600;
Fs2 = 1000;
N_taps = 21;
K = (N_taps - 1) / 2;  % Center index = 10

fprintf('Specs: Fs=%d Hz, Stopband=[%d,%d] Hz, N=%d, K=%d\n', Fs_FIR, Fs1, Fs2, N_taps, K);


%% 4-1) Digital cutoff frequencies (4 pts)
%  -----------------------------------------------------------------------
%  TASK: Convert stopband edges to digital angular frequencies
%  
%  HINT: ω = 2π·F/Fs
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
omega_c1 = 0;  % Lower cutoff in rad/sample
omega_c2 = 0;  % Upper cutoff in rad/sample

% ==============================================================

fprintf('4-1) Your digital frequencies:\n');
fprintf('     ω_c1 = %.4f rad/sample (%.4f π)\n', omega_c1, omega_c1/pi);
fprintf('     ω_c2 = %.4f rad/sample (%.4f π)\n', omega_c2, omega_c2/pi);


%% 4-2) Ideal bandstop impulse response (6 pts)
%  -----------------------------------------------------------------------
%  TASK: Calculate h_BS,ideal[n] for n = -K to K
%  
%  HINT:
%    h_BS[n] = δ[n] - h_BP[n]
%    
%    where h_BP[n] = [sin(ω_c2·n) - sin(ω_c1·n)] / (π·n)  for n ≠ 0
%          h_BP[0] = (ω_c2 - ω_c1) / π
%    
%    so:  h_BS[0] = 1 - (ω_c2 - ω_c1)/π
%         h_BS[n] = -[sin(ω_c2·n) - sin(ω_c1·n)] / (π·n)  for n ≠ 0
%  -----------------------------------------------------------------------

n_ideal = -K:K;  % Indices from -10 to +10

% ===================== YOUR SOLUTION HERE =====================
h_BS_ideal = zeros(size(n_ideal));

% Calculate h_BS_ideal[n] for each n in n_ideal
% Use a loop or vectorized code
% Remember special case at n = 0!

% ==============================================================

fprintf('4-2) Your h_BS_ideal[0] = %.6f\n', h_BS_ideal(K+1));


%% 4-3) Apply Hamming window (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Apply Hamming window to truncated impulse response
%  
%  HINT: w[n] = 0.54 - 0.46·cos(2πn/(N-1)) for n = 0, 1, ..., N-1
%        b[n] = h_BS_ideal[n] · w[n]
%  -----------------------------------------------------------------------

n_causal = 0:N_taps-1;

% ===================== YOUR SOLUTION HERE =====================
w_hamming = zeros(size(n_causal));  % Calculate Hamming window
b_BS = zeros(size(n_causal));       % Windowed coefficients

% ==============================================================

fprintf('4-3) Your center coefficient b[%d] = %.6f\n', K, b_BS(K+1));

figure;
stem(n_causal, b_BS, 'filled', 'LineWidth', 1.5);
grid on; xlabel('n'); ylabel('b[n]');
title('Problem 4-3: Your Bandstop FIR Coefficients');
exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_4_Impulse.png'), 'Resolution', 300);


%% 4-4) Verify linear phase (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Show the filter is symmetric (linear phase)
%  
%  HINT: Check b[n] = b[N-1-n] for all n
%  -----------------------------------------------------------------------

fprintf('4-4) Symmetry check:\n');

% ===================== YOUR SOLUTION HERE =====================
% Print comparison: b[0] vs b[20], b[1] vs b[19], etc.
% Verify they match (or are very close)

% ==============================================================


%% 4-5) Plot magnitude and measure attenuation (5 pts)
%  -----------------------------------------------------------------------
%  TASK: Plot |H(ω)| in dB, measure attenuation at stopband center
%  
%  HINT: Use freqz(b_BS, 1, N_fft, Fs)
%        Stopband center = (600 + 1000)/2 = 800 Hz
%  -----------------------------------------------------------------------

% ===================== YOUR SOLUTION HERE =====================
% [H_BS, F_BS] = freqz(???);
% Mag_dB = 20*log10(abs(H_BS));

% Measure at F = 800 Hz
% [H_center, ~] = freqz(b_BS, 1, 800, Fs_FIR);
% Att_center = ???

fprintf('4-5) Attenuation at 800 Hz = ??? dB\n');

% ==============================================================

% Plot (runs if you calculated b_BS)
if any(b_BS ~= 0)
    [H_BS, F_BS] = freqz(b_BS, 1, 4096, Fs_FIR);
    
    figure;
    plot(F_BS, 20*log10(abs(H_BS)), 'LineWidth', 1.5);
    grid on; xlabel('Frequency [Hz]'); ylabel('|H(e^{j\omega})| [dB]');
    title('Problem 4-5: Your Bandstop Magnitude Response');
    xline(Fs1, '--r', 'F_{s1}'); xline(Fs2, '--r', 'F_{s2}');
    ylim([-80 5]);
    exportgraphics(gcf, fullfile(imgDir, 'Mock_Exam_4_Magnitude.png'), 'Resolution', 300);
end


%% ========================================================================
%  EXAM COMPLETE
%% ========================================================================
fprintf('\n\n');
fprintf('===========================================\n');
fprintf('   TEMPLATE COMPLETE!\n');
fprintf('   \n');
fprintf('   Now compare your answers with:\n');
fprintf('   Mock_Exam_DSP_SOLUTIONS.m\n');
fprintf('===========================================\n');
