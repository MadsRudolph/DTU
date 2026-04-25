%% 62743 DSP -- F20 Exam Solution
% *Course:* 62743 Digital Signal Processing
%
% *Exam set:* F20 (Spring 2020)
%
% *Author:* Mads Rudolph (s246132)
%
% *Topics covered*
%
% * *Problem 1 (25%)* -- LTI system analysis: diff eq -> H(z) -> poles/zeros/stability -> h[n] -> y[n] -> energy
% * *Problem 2 (20%)* -- Spectrum analysis of V(t) via FFT, analytical decomposition, Nyquist
% * *Problem 3 (25%)* -- Causal LTI: ROC, h[n], y[n] for delta-train input, cascade/parallel realisations
% * *Problem 4 (30%)* -- IIR Butterworth highpass design via the bilinear transform (BLT)

clear; clc; close all;
addpath('C:\Users\Mads2\DTU\3.semester\DSP\Helpers');

%% Problem 1 -- LTI system analysis
% Difference equation:
%   y[n] + 0.1 y[n-1] - 0.06 y[n-2] = x[n] + 0.2 x[n-1]

%% 1-1  Bestem H(z)
% *Strategy:* z-transform both sides of the difference equation, factor, divide.
%
% $$Y(z) + 0.1\,z^{-1}Y(z) - 0.06\,z^{-2}Y(z) = X(z) + 0.2\,z^{-1}X(z)$$
%
% $$\bigl(1 + 0.1\,z^{-1} - 0.06\,z^{-2}\bigr)\,Y(z) = \bigl(1 + 0.2\,z^{-1}\bigr)\,X(z)$$
%
% *Result:*
%
% $$H(z) = \frac{Y(z)}{X(z)} = \frac{1 + 0.2\,z^{-1}}{1 + 0.1\,z^{-1} - 0.06\,z^{-2}}$$


% MATLAB coefficient vectors: element k is coefficient of z^(-k).
b = [1, 0.2];         % numerator:   1 + 0.2 z^-1
a = [1, 0.1, -0.06];  % denominator: 1 + 0.1 z^-1 - 0.06 z^-2

% Display H(z) as a discrete-time transfer function.
% Ts = -1 means unspecified sampling period.
% 'Variable','z^-1' prints it in the z^-1 form we derived.
H = tf(b, a, -1, 'Variable', 'z^-1')

%% 1-2  Poles, zeros, stability
% *Strategy:* multiply top and bottom by $z^2$ to get z-form (so the zero
% at z = 0 shows up), then read off zeros and poles from the factored form.
%
% $$H(z) = \frac{z\,(z + 0.2)}{(z + 0.3)(z - 0.2)}$$
%
% *Result:*
%
% * Zeros: $z = 0$ and $z = -0.2$
% * Poles: $z = -0.3$ and $z = +0.2$
% * All poles strictly inside the unit circle, so the system is *stable*.

% Use tf2zpk (not plain roots) so the zero at z=0 is included.
% roots(b) alone would miss it because b is only numerator in z^-1 form.
[z_all, p_all, k_gain] = tf2zpk(b, a);
fprintf('Zeros of H(z):\n');  disp(z_all);
fprintf('Poles of H(z):\n');  disp(p_all);
fprintf('Gain k = %g\n', k_gain);

% Pole-zero plot (unit circle drawn automatically)
figure('Name', 'F20 P1-2: Pole-zero diagram');
zplane(b, a);
title('F20 P1-2: Pole-zero plot');
grid on;

% Stability: causal system stable iff every pole strictly inside unit circle
pole_mag = abs(p_all);
if all(pole_mag < 1)
    fprintf('STABLE: max |pole| = %.4f < 1\n', max(pole_mag));
else
    fprintf('UNSTABLE: max |pole| = %.4f\n', max(pole_mag));
end

%% 1-3  Impulse response h[n]
% *Strategy:* MATLAB's |residuez| does the partial fraction decomposition of
% $B(z)/A(z)$ directly, returning residues $r_i$ and poles $p_i$. Read off:
%
% $$h[n] = \sum_i r_i\,p_i^{\,n}\,u[n]$$
%
% using the table pair $\frac{1}{1 - p\,z^{-1}} \leftrightarrow p^n u[n]$.
%
% *Result:*
%
% $$h[n] = 0.2\,(-0.3)^n\,u[n] + 0.8\,(0.2)^n\,u[n]$$

[r_h, p_h, k_h] = residuez(b, a);
fprintf('\n--- 1-3 PFD of H(z) via residuez ---\n');
fprintf('Residues r (one per pole):\n');  disp(r_h);
fprintf('Poles    p (in same order):\n'); disp(p_h);
fprintf('Direct term k (empty if num order < den order):\n'); disp(k_h);

% Read off h[n]: pair each residue with its pole.
fprintf('h[n] = ');
for i = 1:numel(r_h)
    sgn = '+';  if i == 1, sgn = ' '; end
    fprintf('%s %.4f * (%.4f)^n * u[n] ', sgn, r_h(i), p_h(i));
end
fprintf('\n');



%% 1-4  Output y[n] for x[n] = (-0.2)^n u[n]
% *Strategy:*
%
% # Write X(z) from the table: $x[n] = (-0.2)^n u[n] \;\Rightarrow\; X(z) = \frac{1}{1 + 0.2\,z^{-1}}$
% # Compute $Y(z) = H(z)\,X(z)$ -- multiplying rationals = convolving coefficient vectors.
% # PFD on $Y(z)$ via |residuez|.
% # Inverse transform each piece using $\frac{1}{1 - p\,z^{-1}} \leftrightarrow p^n u[n]$.
%
% *Pole-zero cancellation:* the numerator factor $(1 + 0.2\,z^{-1})$ in
% $H(z)$ and the denominator factor of $X(z)$ are identical, so they cancel.
% |residuez| handles this automatically by returning a residue $\approx 0$
% (floating-point noise) for the cancelled pole.
%
% *Result:*
%
% $$y[n] = 0.6\,(-0.3)^n\,u[n] + 0.4\,(0.2)^n\,u[n]$$

% --- 1) X(z) ---
bx = [1];        % numerator of X(z): just 1
ax = [1, 0.2];   % denominator of X(z): 1 + 0.2 z^-1 (note: +, because a = -0.2 in 1 - a z^-1)

% --- 2) Y(z) = H(z) * X(z): convolve numerators and denominators ---
by = conv(b,  bx);
ay = conv(a,  ax);

fprintf('\n--- 1-4 Y(z) coefficients ---\n');
fprintf('by = '); disp(by);
fprintf('ay = '); disp(ay);

% --- 3) PFD on Y(z) ---
[r_y, p_y, k_y] = residuez(by, ay);
fprintf('Residues r_y:\n');  disp(r_y);
fprintf('Poles    p_y:\n');  disp(p_y);
fprintf('Direct   k_y:\n');  disp(k_y);

% Highlight the cancellation: the residue paired with the pole near -0.2
% should be ~0 (floating-point noise, not exactly 0).
[~, idx_cancel] = min(abs(p_y - (-0.2)));
fprintf('Residue at the (cancelled) pole z=-0.2:  r = %.3e  (effectively zero)\n', ...
        r_y(idx_cancel));

% --- 4) Read off y[n] ---
fprintf('y[n] = ');
for i = 1:numel(r_y)
    sgn = '+';  if i == 1, sgn = ' '; end
    fprintf('%s %.4f * (%.4f)^n * u[n] ', sgn, r_y(i), p_y(i));
end
fprintf('\n');

% --- Verification: run the difference equation directly with `filter` ---
% This is independent of the analytic PFD and confirms the closed-form y[n].
N_y  = 30;
n_y  = (0:N_y-1).';
x_n  = (-0.2).^n_y;            % x[n] = (-0.2)^n u[n]  for n = 0..N-1
y_filt = filter(b, a, x_n);    % numeric output via diff eq


%% 1-5  Energy E_x and E_y
% *Definition:*
%
% $$E = \sum_{n=-\infty}^{\infty} |x[n]|^2$$
%
% For causal exponentials, each piece $a^n u[n]$ contributes a closed-form
% geometric series. For y[n] (a sum of two real exponentials), the square
% expands into three geometric pieces -- including a *cross term*.
%
% *Closed forms:*
%
% $$E_x = \frac{1}{1 - |a|^2}\quad\text{(single exponential)}$$
%
% $$E_y = \frac{A^2}{1 - p_1^2} + \frac{2AB}{1 - p_1 p_2} + \frac{B^2}{1 - p_2^2}\quad\text{(two exponentials)}$$
%
% *Result:*
%
% $$E_x = \frac{1}{0.96} \approx 1.0417 \qquad E_y \approx 1.0151$$

% --- E_x: x[n] = (-0.2)^n u[n] ---
% Closed form:  E_x = 1 / (1 - |a|^2)
a_x  = -0.2;
E_x_closed = 1 / (1 - abs(a_x)^2);

% --- E_y: y[n] = A p1^n + B p2^n   (both real) ---
% Closed form:  E_y = A^2/(1 - p1^2) + 2 A B/(1 - p1 p2) + B^2/(1 - p2^2)
A_y = 0.6;   p1 = -0.3;
B_y = 0.4;   p2 =  0.2;
E_y_closed = A_y^2/(1 - p1^2) + 2*A_y*B_y/(1 - p1*p2) + B_y^2/(1 - p2^2);

% --- Numeric verification (long horizon so the tail is negligible) ---
N_long = 200;
n_long = (0:N_long-1).';
x_long = a_x.^n_long;
y_long = filter(b, a, x_long);
E_x_num = sum(abs(x_long).^2);
E_y_num = sum(abs(y_long).^2);

fprintf('\n--- 1-5 Energy ---\n');
fprintf('E_x (closed form): %.6f\n', E_x_closed);
fprintf('E_x (numeric)    : %.6f\n', E_x_num);
fprintf('E_y (closed form): %.6f\n', E_y_closed);
fprintf('E_y (numeric)    : %.6f\n', E_y_num);




%% Problem 2 -- V(t) spectrum analysis
% *Signal:*
%
% $$V(t) = \cos(2\pi F_1 t)\bigl[1 + \cos(2\pi F_2 t)\bigr] + \tfrac{1}{3}\cos(2\pi F_3 t)$$
%
% with $F_1 = 100$ Hz, $F_2 = 130$ Hz, $F_3 = 180$ Hz.

F1 = 100;  F2 = 130;  F3 = 180;
Fs2 = 4600;                                  % sampling frequency

%% 2-1  Time domain: plot V(t), read off min/max
% *Strategy:* sample $V(t)$ at $F_s = 4600$ Hz over a horizon long enough
% to see several periods of the lowest component (30 Hz after expansion,
% period 33 ms). 50 ms is plenty.
%
% *Result:* read minimum and maximum amplitude values directly from the plot below.

T_plot = 0.05;
t1 = (0:1/Fs2:T_plot - 1/Fs2).';
V1 = cos(2*pi*F1*t1) .* (1 + cos(2*pi*F2*t1)) + (1/3)*cos(2*pi*F3*t1);

figure('Name', 'F20 P2-1: V(t) time domain');
plot(t1, V1, 'LineWidth', 1.2); grid on;
xlabel('t [s]'); ylabel('V(t)');
title('F20 P2-1: V(t) sampled at Fs = 4600 Hz');

fprintf('\n--- 2-1 V(t) min/max ---\n');
fprintf('min V(t) approx %.4f\n', min(V1));
fprintf('max V(t) approx %.4f\n', max(V1));

%% 2-2  Frequency domain: FFT with deltaF = 0.1 Hz, one-sided amplitude spectrum
% *Strategy:* frequency resolution $\Delta F$ sets $N = F_s/\Delta F$. With
% $\Delta F = 0.1$ Hz and $F_s = 4600$ Hz, $N = 46000$ samples (= 1 second).
%
% For a real signal $x[n]$ of length $N$, the FFT bin $|X[k]|$ at the cosine
% frequency equals $A N/2$ (where $A$ is the cosine amplitude). So the
% one-sided amplitude spectrum is:
%
% $$\text{amp}[k] = \begin{cases} |X[k]|/N & k = 0\;\text{or}\;k = N/2 \\ 2|X[k]|/N & \text{otherwise} \end{cases}$$
%
% *Result:* four discrete components visible in the spectrum (read off below).

deltaF = 0.1;
N2  = Fs2 / deltaF;           % 46000
t2  = (0:N2-1).'/Fs2;
V2  = cos(2*pi*F1*t2) .* (1 + cos(2*pi*F2*t2)) + (1/3)*cos(2*pi*F3*t2);

X2  = fft(V2);
f2  = (0:N2-1).' * Fs2 / N2;          % frequency axis [Hz]

% One-sided amplitude spectrum
half      = 1:N2/2 + 1;
A_amp     = abs(X2(half)) / N2;
A_amp(2:end-1) = 2 * A_amp(2:end-1);  % double interior (skip DC & Nyquist)
f_half    = f2(half);

figure('Name', 'F20 P2-2: |V(f)| amplitude spectrum');
stem(f_half, A_amp, 'filled', 'Marker', '.'); grid on;
xlim([0 500]);    % zoom to the relevant band
xlabel('f [Hz]'); ylabel('Amplitude');
title('F20 P2-2: One-sided amplitude spectrum of V(t)');

% --- Idiom: nearest-bin lookup ---
% Question form: "what is the amplitude at f = X Hz?"
% Recipe (memorise these two lines):
%
%     [~, idx] = min(abs(f_axis - f_target));    % closest bin to f_target
%     value    = y_axis(idx);                     % read off the amplitude there
%
% Why it works: abs(f_axis - f_target) is the distance from every bin to the
% target. min(...) returns [min_distance, min_index]. We discard the distance
% (~) and keep the index. Then y_axis(idx) is the value at that bin.
%
% Same two lines work for ANY (x_axis, y_axis) lookup: FFT amplitude at a
% frequency, freqz magnitude at a frequency, filter dB attenuation at the
% stopband edge, etc. Drill it once, reuse everywhere.

fprintf('\n--- 2-2 Discrete components (nearest-bin lookup) ---\n');
expected_f = [30, 100, 180, 230];
for fc = expected_f
    [~, idx] = min(abs(f_half - fc));
    fprintf('  f = %3d Hz   amplitude = %.4f\n', fc, A_amp(idx));
end

%% 2-3  Analytical rewrite of V(t) -- product-to-sum
% *Identity:*
%
% $$\cos(A)\cos(B) = \tfrac{1}{2}\bigl[\cos(A-B) + \cos(A+B)\bigr]$$
%
% Expanding $V(t) = \cos(2\pi F_1 t) + \cos(2\pi F_1 t)\cos(2\pi F_2 t) + \tfrac{1}{3}\cos(2\pi F_3 t)$ and
% applying the identity to the product:
%
% *Result:*
%
% $$V(t) = \tfrac{1}{2}\cos(2\pi\!\cdot\!30\,t) + \cos(2\pi\!\cdot\!100\,t) + \tfrac{1}{3}\cos(2\pi\!\cdot\!180\,t) + \tfrac{1}{2}\cos(2\pi\!\cdot\!230\,t)$$
%
% Four components: 30 Hz @ 0.5, 100 Hz @ 1.0, 180 Hz @ 1/3, 230 Hz @ 0.5.
% These match the FFT bins from 2-2 exactly.

fprintf('\n--- 2-3 Analytical components (expected) ---\n');
analytical = [30 0.5;  100 1.0;  180 1/3;  230 0.5];
for k = 1:size(analytical,1)
    fprintf('  f = %3d Hz   amplitude = %.4f\n', analytical(k,1), analytical(k,2));
end

%% 2-4  Minimum sampling frequency (Nyquist)
% *Trap:* reading "$F_3 = 180$ Hz" off the original expression would give
% $F_{s,\min} = 360$ Hz, which would alias the hidden 230 Hz component.
% After the rewrite in 2-3, the highest frequency is $F_1 + F_2 = 230$ Hz.
%
% *Result:*
%
% $$F_{s,\min} = 2 \cdot F_{\max} = 2 \cdot 230 = 460\;\text{Hz}$$

Fmax = max([F1, F2, F3, F1+F2, abs(F2-F1)]);
fprintf('\n--- 2-4 Minimum sampling frequency ---\n');
fprintf('Highest frequency in V(t) (after expansion) = %d Hz\n', Fmax);
fprintf('Minimum Fs = 2 * Fmax = %d Hz\n', 2*Fmax);


%% Problem 3 -- H(z) = 1 / [(1 + 0.2 z^-1)(1 - 0.8 z^-1)]
% *System:* causal LTI with system function
%
% $$H(z) = \frac{1}{(1 + \tfrac{1}{5}z^{-1})(1 - \tfrac{4}{5}z^{-1})}$$
%
% Expand the denominator factors for MATLAB:
%
% $$(1 + 0.2\,z^{-1})(1 - 0.8\,z^{-1}) = 1 - 0.6\,z^{-1} - 0.16\,z^{-2}$$

b3 = 1;
a3 = [1, -0.6, -0.16];

%% 3-1  ROC
% *Rule:* for a causal system, the ROC is outside the outermost pole.
% Poles at $z = -0.2$ and $z = +0.8$. Outermost: $|z| = 0.8$.
%
% *Result:*
%
% $$\text{ROC}: \;|z| > 0.8$$

fprintf('\n--- 3-1 ROC ---\n');
fprintf('Causal system -> ROC outside outermost pole.\n');
fprintf('Outermost pole |z| = 0.8 -> ROC: |z| > 0.8\n');

%% 3-2  Poles, zeros, pole-zero plot
% *Strategy:* multiply top and bottom by $z^2$ to convert to z-form:
%
% $$H(z) = \frac{z^2}{(z + 0.2)(z - 0.8)}$$
%
% *Result:*
%
% * Zeros: $z = 0$ (double, from $z^2$)
% * Poles: $z = -0.2$ and $z = +0.8$
% * All poles inside the unit circle, system is stable.

[z3, p3, k3] = tf2zpk(b3, a3);
fprintf('\n--- 3-2 Zeros and poles ---\n');
fprintf('Zeros:\n'); disp(z3);
fprintf('Poles:\n'); disp(p3);

figure('Name', 'F20 P3-2: Pole-zero diagram');
zplane(b3, a3);
title('F20 P3-2: Pole-zero plot');
grid on;

%% 3-3  Impulse response h[n]
% *Strategy:* PFD via |residuez|, then read off
% $h[n] = \sum_i r_i\,p_i^n\,u[n]$.
%
% *Result:*
%
% $$h[n] = 0.2\,(-0.2)^n\,u[n] + 0.8\,(0.8)^n\,u[n]$$

[r3, p3r, k3r] = residuez(b3, a3);
fprintf('\n--- 3-3 PFD of H(z) ---\n');
fprintf('Residues r:\n'); disp(r3);
fprintf('Poles    p:\n'); disp(p3r);
fprintf('Direct   k:\n'); disp(k3r);

fprintf('h[n] = ');
for i = 1:numel(r3)
    sgn = '+';  if i == 1, sgn = ' '; end
    fprintf('%s %.4f * (%.4f)^n * u[n] ', sgn, r3(i), p3r(i));
end
fprintf('\n');

[h3_n, n3_h] = impz(b3, a3, 30);
figure('Name', 'F20 P3-3: Impulse response');
stem(n3_h, h3_n, 'filled'); grid on;
xlabel('n'); ylabel('h[n]');
title('F20 P3-3: Impulse response h[n]');

%% 3-4  Output y[n] for x[n] = delta[n] + delta[n-2]
% *Strategy:* by linearity and time-invariance, the response to a sum of
% (shifted) impulses is the same sum of (shifted) impulse responses.
% No fresh PFD needed.
%
% $$x[n] = \delta[n] + \delta[n-2] \quad\Longrightarrow\quad y[n] = h[n] + h[n-2]$$
%
% *Result (closed form, with $h[n]$ from 3-3):*
%
% $$y[n] = \bigl[0.2(-0.2)^n + 0.8(0.8)^n\bigr]u[n] + \bigl[0.2(-0.2)^{n-2} + 0.8(0.8)^{n-2}\bigr]u[n-2]$$
%
% *Piecewise simplified form:*
%
% $$y[n] = \begin{cases} 0 & n < 0 \\ 1 & n = 0 \\ 0.6 & n = 1 \\ 5.2\,(-0.2)^n + 2.05\,(0.8)^n & n \geq 2 \end{cases}$$

N3 = 30;
x3 = zeros(N3, 1);  x3(1) = 1;  x3(3) = 1;     % δ[n] + δ[n-2]
y3 = filter(b3, a3, x3);                        % numeric verification

figure('Name', 'F20 P3-4: y[n]');
stem(0:N3-1, y3, 'filled'); grid on;
xlabel('n'); ylabel('y[n]');
title('F20 P3-4: Output for x[n] = \delta[n] + \delta[n-2]');

%% 3-5  Cascade and parallel realisations of H(z)
% *Cascade:* the given factored form is already a cascade of two first-order sections.
%
% $$H(z) = H_1(z)\cdot H_2(z) \;,\qquad H_1(z) = \frac{1}{1 + 0.2\,z^{-1}}\;,\quad H_2(z) = \frac{1}{1 - 0.8\,z^{-1}}$$
%
% *Parallel:* the PFD from 3-3 *is* the parallel form -- two first-order branches summed.
%
% $$H(z) = H_1'(z) + H_2'(z) \;,\qquad H_1'(z) = \frac{0.2}{1 + 0.2\,z^{-1}}\;,\quad H_2'(z) = \frac{0.8}{1 - 0.8\,z^{-1}}$$

fprintf('\n--- 3-5 Realisations ---\n');
fprintf('Cascade:  H(z) = H1(z) * H2(z)\n');
fprintf('  H1(z) = 1 / (1 + 0.2 z^-1)\n');
fprintf('  H2(z) = 1 / (1 - 0.8 z^-1)\n\n');
fprintf('Parallel: H(z) = H1''(z) + H2''(z)   (PFD branches)\n');
for i = 1:numel(r3)
    fprintf('  H%d''(z) = %.4f / (1 - (%.4f) z^-1)\n', i, r3(i), p3r(i));
end


%% Problem 4 -- IIR Butterworth highpass via BLT
% *Design specs:*
%
% * Filter type: IIR Butterworth highpass
% * Sampling frequency: $F_s = 5000$ Hz
% * Stopband edge: 100 Hz
% * Passband edge: 180 Hz
% * Stopband attenuation: $A_s = 20$ dB
% * Passband attenuation: $A_p = 3$ dB
% * BLT parameter: $\alpha = 2/T_s$
%
% *Pipeline:* prewarp -> order + LP prototype -> LP-to-HP -> BLT -> verify.

Fs4 = 5000;
Ts4 = 1/Fs4;
F_stop = 100;          % stopband edge [Hz]
F_pass = 180;          % passband edge [Hz]
As4   = 20;            % stopband attenuation [dB]
Ap4   = 3;             % passband attenuation [dB]

% Digital angular frequencies (rad/sample)
omega_s = 2*pi*F_stop/Fs4;
omega_p = 2*pi*F_pass/Fs4;

%% 4-1  Pre-warp digital edges to analog angular frequencies
% *BLT prewarping relation:*
%
% $$\Omega = \alpha\tan(\omega/2) = \frac{2}{T_s}\tan\!\left(\frac{\pi F}{F_s}\right)$$
%
% *Result:*
%
% $$\Omega_s \approx 628.7\;\text{rad/s},\qquad \Omega_p \approx 1135\;\text{rad/s}$$

Omega_s = (2/Ts4) * tan(omega_s/2);
Omega_p = (2/Ts4) * tan(omega_p/2);

fprintf('\n--- 4-1 Pre-warped analog angular frequencies ---\n');
fprintf('Omega_s = %.4f rad/s\n', Omega_s);
fprintf('Omega_p = %.4f rad/s\n', Omega_p);

%% 4-2  Butterworth order n and normalized lowpass prototype
% *Mapping HP specs to LP prototype:* via $s \to W_c/s$, the HP passband
% edge $\Omega_p$ becomes LP cutoff = 1, and the HP stopband edge $\Omega_s$
% becomes LP stopband edge $\Omega_p / \Omega_s$.
%
% *Butterworth order formula:*
%
% $$n \geq \frac{\log_{10}\!\left(\dfrac{10^{A_s/10} - 1}{10^{A_p/10} - 1}\right)}{2\,\log_{10}(\Omega_p/\Omega_s)}$$
%
% Plugging in: $n \geq 1.9956 / 0.5125 \approx 3.894 \;\Rightarrow\; n = 4$.
%
% *Normalized 4th-order Butterworth prototype:*
%
% $$H_{LP}(s) = \frac{1}{s^4 + 2.6131\,s^3 + 3.4142\,s^2 + 2.6131\,s + 1}$$

ratio_lp = Omega_p / Omega_s;
n_real   = log10((10^(As4/10) - 1) / (10^(Ap4/10) - 1)) / ...
           (2 * log10(ratio_lp));
n_order  = ceil(n_real);

fprintf('\n--- 4-2 Order and LP prototype ---\n');
fprintf('LP stopband/passband ratio: %.4f\n', ratio_lp);
fprintf('n required (real): %.4f  ->  ceiling: n = %d\n', n_real, n_order);

% Normalized Butterworth lowpass prototype (cutoff = 1 rad/s) for n = 4
[z_lp, p_lp, k_lp] = buttap(n_order);
[b_lp, a_lp]       = zp2tf(z_lp, p_lp, k_lp);

fprintf('LP prototype H_LP(s) = b_lp / a_lp:\n');
fprintf('  b_lp: '); disp(b_lp);
fprintf('  a_lp: '); disp(a_lp);

%% 4-3  Lowpass-to-Highpass transformation
% *Substitution:*
%
% $$s_{lp} \longrightarrow \frac{W_o}{s_{hp}}\;,\qquad W_o = \Omega_p \approx 1135\;\text{rad/s}$$
%
% MATLAB does the substitution analytically via |lp2hp|. The output is the
% analog highpass transfer function in the standard form
%
% $$H_{HP}(s) = \frac{\beta_M s^M + \cdots + \beta_0}{\alpha_N s^N + \cdots + \alpha_0}$$

Wo = Omega_p;
[b_hp_a, a_hp_a] = lp2hp(b_lp, a_lp, Wo);

fprintf('\n--- 4-3 Analog highpass H_HP(s) ---\n');
fprintf('  Numerator   (beta) : '); disp(b_hp_a);
fprintf('  Denominator (alpha): '); disp(a_hp_a);

%% 4-4  BLT to digital
% *Substitution:*
%
% $$s \longrightarrow \frac{2}{T_s}\,\frac{1 - z^{-1}}{1 + z^{-1}}$$
%
% MATLAB applies the BLT via |bilinear|. *Important:* do NOT pass a
% prewarp frequency to |bilinear| -- we already prewarped manually in 4-1,
% and passing |fp| would prewarp twice.
%
% Output form:
%
% $$H_{HP}(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}}$$

[b_hp_d, a_hp_d] = bilinear(b_hp_a, a_hp_a, Fs4);

fprintf('\n--- 4-4 Digital highpass H_HP(z) ---\n');
fprintf('  b: '); disp(b_hp_d);
fprintf('  a: '); disp(a_hp_d);

%% 4-5  Magnitude response and spec verification
% *Plot:* $20\log_{10}|H_{HP}(f)|$ in dB vs frequency in Hz, with spec
% lines drawn at $F_\text{stop}$, $F_\text{pass}$, $-A_s$, $-A_p$.
%
% *Spec is met when:*
%
% * $|H| \leq -20$ dB to the *left* of $F_\text{stop} = 100$ Hz (stopband)
% * $|H| \geq -3$ dB to the *right* of $F_\text{pass} = 180$ Hz (passband)
%
% Numeric spec check uses the nearest-bin lookup idiom on the |freqz| output.

[H4, F4] = freqz(b_hp_d, a_hp_d, 4096, Fs4);
H4_dB    = 20*log10(abs(H4));

figure('Name', 'F20 P4-5: HP filter magnitude response');
plot(F4, H4_dB, 'LineWidth', 1.5); grid on; hold on;
xlabel('F [Hz]'); ylabel('|H_{HP}(f)| [dB]');
title('F20 P4-5: Butterworth HP magnitude response');
xline(F_stop, '--r', sprintf('%d Hz (Fstop)', F_stop), 'LineWidth', 1.2);
xline(F_pass, '--g', sprintf('%d Hz (Fpass)', F_pass), 'LineWidth', 1.2);
yline(-As4,   '--r', sprintf('-%d dB', As4));
yline(-Ap4,   '--g', sprintf('-%d dB', Ap4));
xlim([0 500]); ylim([-80 5]);

% Spec check via the nearest-bin lookup idiom
[~, idx_stop] = min(abs(F4 - F_stop));
[~, idx_pass] = min(abs(F4 - F_pass));
fprintf('\n--- 4-5 Attenuation check ---\n');
fprintf('|H| at %d Hz (Fstop): %.2f dB   (spec: <= -%d dB)\n', ...
        F_stop, H4_dB(idx_stop), As4);
fprintf('|H| at %d Hz (Fpass): %.2f dB   (spec: >= -%d dB)\n', ...
        F_pass, H4_dB(idx_pass), Ap4);


