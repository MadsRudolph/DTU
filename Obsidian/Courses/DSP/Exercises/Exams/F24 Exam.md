> Exam set: [[62743 F24 Exam-1.pdf]]  
> Solution sheet: [[62743 F24 Exam student solutions1.pdf]]  
> Matlab document: [Open](<file:///C:/Users/Mads2/DTU/3.semester/DSP/EXAMS/E24.mlx>)

---
# 62743 — F24 Exam (Digital Signal Processing)  
---

## 📘 Big-Picture Overview

This document contains **fully worked solutions** to the **F24 written exam** in 62743 Digital Signal Processing.  

For each exam problem, you get:

- A short **context / theory recap** in your own words.  
- Full **derivations** with all intermediate steps (not just final answers).  
- **MATLAB templates** you can re-use in the exam (copy → adapt parameters).  
- Clear tagging of key formulas and interpretations.

Structure:

1. **Problem 1 – LTI systems in time & z-domain**  
2. **Problem 2 – Sampling, aliasing & analog AA-filter**  
3. **Problem 3 – Sampling criteria, discrete filter & min-phase / all-pass factorization**  
4. **Problem 4 – BLT IIR bandstop Butterworth design**  
---

# Problem 1 — LTI Systems, Impulse Response and z-Domain

> **Given**
> Two discrete-time input signals
> $$
> x_1[n] = 3\delta[n] + 2\delta[n-1], \qquad
> x_2[n] = \delta[n] + 2\delta[n-1]
> $$
> are applied separately to an unknown **LTI system** with outputs $y_1[n]$ and $y_2[n]$ given in a table (omitted here; values are used when needed).  
> You are asked to determine:
> 1. $x_1[n] - x_2[n]$  
> 2. The **impulse response** $h[n]$  
> 3. The **system function** $H(z)$  
> 4. The system function $H_2(z)$ and ROC for a second LTI system  
> 5. The cascade system $H_3(z)$ and its impulse response $h_3[n]$; decide FIR/IIR.

---

## 1-1) Difference of inputs

We simply subtract term-by-term:
$$
\begin{aligned}
x_1[n] - x_2[n]
&= \big(3\delta[n] + 2\delta[n-1]\big) - \big(\delta[n] + 2\delta[n-1]\big) \\
&= (3-1)\delta[n] + (2-2)\delta[n-1] \\
&= 2\delta[n].
\end{aligned}
$$

So
$$
\boxed{x_1[n]-x_2[n] = 2\delta[n]}
$$

> [!code]- MATLAB — 1-1 quick check
> ```matlab
> % Problem 1-1: x1[n] - x2[n]
> n = -1:3;
> delta = @(k) double(k == 0);
> x1 = 3*delta(n) + 2*delta(n-1);
> x2 =     delta(n) + 2*delta(n-1);
> xdiff = x1 - x2;   % should be 2*delta[n]
> disp([n; x1; x2; xdiff].');
> ```

---

## 1-2) Impulse response from LTI + linearity

> We know the impulse response is the output to a **unit impulse input**:
> $$
 h[n] = y_h[n] \quad \text{when} \quad x[n] = \delta[n].
 $$

From 1-1 we already found
$$
x_1[n] - x_2[n] = 2\delta[n] \;\Rightarrow\; \delta[n] = \tfrac12\big(x_1[n]-x_2[n]\big).
$$

Because the system is **linear and time-invariant**, the output to $\delta[n]$ is
$$
\begin{aligned}
h[n] &= \text{output to } \delta[n]
      = \text{output to } \frac12(x_1[n]-x_2[n]) \\
     &= \frac12\big(y_1[n]-y_2[n]\big).
\end{aligned}
$$

Using the table values (read from the exam sheet) gives the sequence:​

- For $n < 0$ and $n>4$: all outputs $0$.  
- For $n=0,1,2,3$ we compute $\frac12(y_1[n]-y_2[n])$:
  - $n=0$: $\frac12(12-4) = 4$  
  - $n=1$: $\frac12(-28-(-4)) = \frac12(-24) = -12$  
  - $n=2$: $\frac12(-21-(-23)) = \frac12(2) = 1$  
  - $n=3$: $\frac12(-7-(-1)) = \frac12(-6) = -3$  

So
$$
h[n] =
\begin{cases}
4,     & n=0,\\
-12,   & n=1,\\
1,     & n=2,\\
-3,    & n=3,\\
0,     & \text{otherwise},
\end{cases}
$$
which we can write compactly in delta notation:
$$
\boxed{h[n] = 4\delta[n]-12\delta[n-1]+\delta[n-2]-3\delta[n-3]}
$$

> [!code]- MATLAB — 1-2 compute $h[n]$ from the table
> ```matlab
> % Problem 1-2: compute h[n] = 0.5 * (y1[n] - y2[n])
> n = 0:4;
> y1 = [12 -28 -21 -7 -6];   % from exam table
> y2 = [ 4  -4 -23 -1 -6];   % from exam table
> h  = 0.5*(y1 - y2);
> 
> n_full = -1:5;
> h_full = zeros(size(n_full));
> h_full(ismember(n_full,n)) = h;
> stem(n_full,h_full,'filled'); grid on;
> xlabel('n'); ylabel('h[n]');
> title('Impulse response h[n] from 0.5 (y_1[n] - y_2[n])');
> ```

![[Images/DSP_Exam_F24_1_ImpulseResponse.png]]

---

## 1-3) System function $H(z)$

For a causal FIR impulse response of length $4$, the **system function** is the $z$-transform
$$
H(z)=\sum_{n=0}^3 h[n] z^{-n}
    = 4 - 12z^{-1}+z^{-2}-3z^{-3}.
$$

So
$$
\boxed{H(z)=4 - 12z^{-1}+z^{-2}-3z^{-3}}
$$

This is a **finite polynomial in $z^{-1}$** → a causal **FIR** filter.

> [!code]- MATLAB — 1-3 polynomial form
> ```matlab
> % Problem 1-3: H(z) from h[n]
> h = [4 -12 1 -3];
> % H(z) = 4 - 12 z^-1 + 1 z^-2 - 3 z^-3
> % Numerator for e.g. freqz is just h:
> B = h;
> A = 1;   % FIR
> ```

---

## 1-4) Second LTI system: system function and ROC

> Given difference equation
> $$
> y[n] + \frac14 y[n-2] = x[n].
> $$

### Z-transform and $H_2(z)$

Take the $z$-transform assuming **initial rest** (no extra terms):

$$
Y(z) + \frac14 z^{-2}Y(z) = X(z).
$$

Factor $Y(z)$:
$$
Y(z)\left(1 + \frac14 z^{-2}\right) = X(z).
$$

So the **system function** is
$$
H_2(z) = \frac{Y(z)}{X(z)} = \frac{1}{1 + \tfrac14 z^{-2}}.
$$

Sometimes it is nicer to clear negative powers:
$$
H_2(z) = \frac{z^2}{z^2 + \tfrac14}
       = \frac{z^2}{\left(z+\tfrac{i}{2}\right)\left(z-\tfrac{i}{2}\right)}.
$$

**Poles** at $z=\pm j/2$; zeros at $z=0$ (double zero).

### ROC and stability

- Difference equation is **causal** (only non-future $y[n]$’s), and “initial rest” implies the ROC is outside the outermost pole:
  $$
  \text{ROC: } |z| > \tfrac12.
  $$
- For BIBO stability, the ROC must include the **unit circle** $|z|=1$. Since $1 > 1/2$, the unit circle is inside the ROC → the system is **stable**.

So we summarize:
$$
\boxed{H_2(z)=\dfrac{1}{1+\tfrac14 z^{-2}},\quad \text{ROC: } |z|>\tfrac12,\quad \text{stable, causal.}}
$$

#### Pole–zero and ROC illustration

The figure below shows:

- poles at $z=\pm j/2$ (on the circle $|z|=1/2$),
- a **shaded ROC** for $|z|>1/2$,
- the **unit circle** lying inside the ROC, confirming stability.

![[Images/DSP_F24_1_4_ROC.png|350]]

> [!code]- MATLAB — 1-4: pole-zero and ROC plots
> ```matlab
> % 1-4) Second LTI system: y[n] + (1/4) y[n-2] = x[n]
> % H2(z) = 1 / (1 + 1/4 z^{-2})
> 
> B2 = 1;
> A2 = [1 0 1/4];    % corresponds to 1 + 0 z^{-1} + 1/4 z^{-2}
> 
> p2 = roots(A2);
> z2 = roots(B2);
> 
> fprintf('\n1-4) Second LTI system H2(z)\n');
> fprintf('H2(z) = 1 / (1 + 1/4 z^{-2})\n');
> fprintf('Poles:\n'); disp(p2.');
> fprintf('Zeros:\n'); disp(z2.');
> fprintf('ROC for stability and causality: |z| > 1/2.\n');
> 
> % --- Pole-zero plot (saved separately if you like) ---
> figure;
> zplane(B2, A2);
> title('H_2(z): Pole-zero plot');
> axis equal;
> grid on;
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_F24_1_4_pz.png'), 'Resolution', 300);
> 
> % --- ROC illustration: |z| > 1/2, unit circle, poles ---
> r_pole = 0.5;          % radius of pole circle
> r_unit = 1.0;          % unit circle
> theta = linspace(0, 2*pi, 400);
> 
> x_pole = r_pole * cos(theta);
> y_pole = r_pole * sin(theta);
> x_unit = r_unit * cos(theta);
> y_unit = r_unit * sin(theta);
> 
> figure;
> hold on; grid on; axis equal;
> 
> % Shade ROC: |z| > 1/2 up to some outer radius (say 1.5)
> r_outer = 1.5;
> [R, T] = meshgrid(linspace(r_pole, r_outer, 50), theta);
> Xroc = R .* cos(T);
> Yroc = R .* sin(T);
> 
> % light shading for ROC
> surf(Xroc, Yroc, zeros(size(Xroc)), ...
>     'EdgeColor', 'none', 'FaceAlpha', 0.15);
> view(2);   % 2D view
> 
> % Draw pole circle (|z| = 0.5) and unit circle
> plot(x_pole, y_pole, 'k--', 'LineWidth', 1.0);      % |z| = 0.5
> plot(x_unit, y_unit, 'k-',  'LineWidth', 1.2);      % |z| = 1
> 
> % Mark poles and zeros explicitly
> plot(real(p2), imag(p2), 'rx', 'MarkerSize', 10, 'LineWidth', 2);
> plot(real(z2), imag(z2), 'bo', 'MarkerSize', 8,  'LineWidth', 1.5);
> 
> % Axes and annotations
> xlabel('Re\{z\}');
> ylabel('Im\{z\}');
> title('ROC for H_2(z): |z| > 1/2 (stable, causal)');
> 
> text(0.1, 0, '|z|=1', 'FontSize', 10);
> text(r_pole+0.02, 0, '|z|=1/2', 'FontSize', 10);
> 
> xlim([-r_outer r_outer]);
> ylim([-r_outer r_outer]);
> 
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_F24_1_4_ROC.png'), 'Resolution', 300);
> ```

---

## 1-5) Cascade of the two systems: $H_3(z)$, $h_3[n]$, FIR/IIR?

We now cascade the systems with $H(z)$ and $H_2(z)$:
$$
H_3(z) = H(z) H_2(z) =
\frac{4-12z^{-1}+z^{-2}-3z^{-3}}{1 + \tfrac14 z^{-2}}.
$$

Multiply numerator and denominator by $z^2$:
$$
H_3(z) =
\frac{(4-12z^{-1}+z^{-2}-3z^{-3})z^2}{z^2+\tfrac14}
= \frac{4z^2 - 12z + 1 - 3z^{-1}}{z^2 + \tfrac14}.
$$

From the solution sheet we know that the **polynomial division** simplifies dramatically:​
$$
4z^3 - 12z^2 + z - 3 = (z^2 + \tfrac14)(4z - 12).
$$

Dividing numerator and denominator:

$$
H_3(z) = \frac{4z - 12}{z} = 4 - 12z^{-1}.
$$

So the cascade **collapses back** to a 2-tap FIR (!).

Therefore, the impulse response is

$$
\boxed{h_3[n]=4\delta[n]-12\delta[n-1]}
$$

This has only two nonzero samples ⇒ **FIR** system.

> [!theory] **Why does a cascade of an FIR and an IIR sometimes become FIR?**  
> In general:
> $$
> H_{\text{tot}}(z) = \frac{N_1(z)}{D_1(z)}\frac{N_2(z)}{D_2(z)}
> =\frac{N_1(z)N_2(z)}{D_1(z)D_2(z)}.
> $$
> If one factor in the numerator cancels a factor in the denominator, we can remove poles and zeros.  
> In this problem, **all poles** of $H_2(z)$ cancel with zeros hidden in $H(z)$, leaving a pure polynomial in $z^{-1}$ → FIR.

> [!code]- MATLAB — 1-5 cascade and verify
> ```matlab
> % Problem 1-5: cascade H(z) and H2(z)
> B  = [4 -12 1 -3];      % H(z)
> A  = 1;
> B2 = 1;                 % H2(z) = 1 / (1 + 0*z^-1 + 1/4 z^-2)
> A2 = [1 0 1/4];
> 
> % Cascade: multiply polynomials
> B3 = conv(B,B2);
> A3 = conv(A,A2);
> 
> % Simplify with tf (Control System Toolbox) or just use residuez:
> [r,p,k] = residuez(B3,A3);  % optional: partial fraction
> 
> % Use symbolic tool or manual factor from solution:
> B3_simplified = [4 -12];    % from algebraic simplification
> A3_simplified = 1;
> 
> h3 = B3_simplified;         % impulse response: [4 -12]
> ```

![[Images/DSP_Exam_F24_1_Cascade_h3.png]]

---

# Problem 2 — Sampling, Aliasing and Analog AA-Filter

> **Given analog signal**  
> $$
 x_A(t) = A_1\cos(2\pi F_1 t) + A_2\cos(2\pi F_2 t)
 $$
> with
> $$
 A_1 = 3,\quad F_1 = 200~\text{Hz},\qquad
 A_2 = 1.5,\quad F_2 = 750~\text{Hz}.
 $$
> Several questions ask about:
> - **Minimum sampling frequency** (Nyquist)  
> - **Aliasing** when $F_s=1000$ Hz  
> - Computing the spectrum numerically with FFT  
> - Designing an analog **4th-order Butterworth AA-filter** with $F_p=350$ Hz  
> - Plotting the analog AA-filter magnitude response.

---

## 2-1) Minimum sampling frequency to avoid aliasing

### (a) Nyquist condition

For a real, band-limited analog signal
$$
x_A(t) = \sum_k A_k \cos(2\pi F_k t),
$$
the **highest frequency** sets the Nyquist rate:
$$
F_s \ge 2F_{\max},\quad F_{\max} = \max_k F_k.
$$

### (b) Numerical value

Here
$$
F_{\max} = F_2 = 750~\text{Hz},
$$
so the minimum sampling frequency is
$$
F_{s,\min} = 2\cdot 750 = 1500~\text{Hz}.
$$

---

> [!code]- MATLAB — 2-1 Nyquist helper
> ```matlab
> % Problem 2-1: Nyquist sampling frequency
> F1 = 200; F2 = 750;
> Fmax = max(F1,F2);
> Fs_min = 2*Fmax;
> fprintf('Minimum Fs to avoid aliasing = %.1f Hz\n', Fs_min);
> ```

---

## 2-2) Aliasing when $F_s = 1000$ Hz

### (a) Does aliasing occur?

Check Nyquist:
$$
F_s = 1000~\text{Hz},\quad \frac{F_s}{2} = 500~\text{Hz}.
$$

- $F_1 = 200~\text{Hz} < 500$ → OK  
- $F_2 = 750~\text{Hz} > 500$ → violates Nyquist

So **aliasing occurs** due to the $750$ Hz component.

### (b) Aliased frequency

For a single sinusoid at $F_2$ sampled at $F_s$, the discrete-time spectrum is periodic with period $F_s$. The observed baseband frequency is the **folded** frequency
$$
F_{2,\text{alias}} = |F_2 - kF_s|
$$
for some integer $k$ chosen so that $F_{2,\text{alias}} \in [0,F_s/2]$.  

A convenient formula for a single fold above Nyquist is
$$
F_{\text{alias}} = F_2 - 2\,(F_2 - F_s/2).
$$

Plug in values:
$$
F_{2,\text{alias}} = 750 - 2\big(750 - 500\big) = 750 - 2\cdot 250 = 250~\text{Hz}.
$$

So the 750 Hz tone **appears at 250 Hz** in the sampled spectrum.

> [!code]- MATLAB — 2-2 aliasing computation
> ```matlab
> % Problem 2-2: alias frequency for F2 at Fs = 1000 Hz
> Fs = 1000;
> F2 = 750;
> F_alias = F2 - 2*(F2 - Fs/2);
> fprintf('Aliased frequency of 750 Hz at Fs=1000 Hz is %.1f Hz\n', F_alias);
> ```

---

## 2-3) Spectrum of sampled signal (FFT)

> Use $F_s=1000$ Hz and $N = 10^5$ samples to compute and plot $|X_A[k]|$ vs frequency. 

### Steps

1. **Time vector** using sampling period $T_s = 1/F_s$:
   $$
   t[n] = n T_s,\quad n = 0,\dots,N-1.
   $$
2. **Sample the analog signal**:
   $$
   x_A[n] = x_A(t[n]).
   $$
3. Compute **DFT** using FFT:
   $$
   X_A[k] = \text{fft}(x_A[n]).
   $$
4. **Center** spectrum with `fftshift` and scale by $1/N$ for meaningful amplitudes.  
5. Build a **frequency vector** in Hz:
   $$
   f_k = \frac{k}{N}F_s,\quad \text{or (centered)}\; f_k \in [-F_s/2,F_s/2].
   $$
6. Plot $|X_A[k]|$ vs $f_k$ and compare peaks with expected alias frequencies.

### Expected result

- A strong line at $F_1 = 200$ Hz (no alias)  
- A strong line near **250 Hz** instead of 750 Hz, confirming the aliasing result from 2-2.

> [!code]- MATLAB — 2-3 spectrum template
> ```matlab
> % Problem 2-3: spectrum of sampled x_A[n]
> Fs = 1000;               % sampling frequency
> N  = 1e5;                % number of samples
> Ts = 1/Fs;
> 
> n  = 0:N-1;
> t  = n*Ts;
> 
> A1 = 3;  F1 = 200;
> A2 = 1.5;F2 = 750;
> 
> xA = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t);
> 
> % FFT and frequency axis
> XA   = fft(xA);
> XA_s = fftshift(XA)/N;           % scaled, centered
> 
> f = (-N/2:N/2-1)*(Fs/N);         % frequency vector in Hz
> 
> figure;
> plot(f, abs(XA_s)); grid on;
> xlabel('Frequency f [Hz]');
> ylabel('|X_A(f)| (scaled)');
> title('Magnitude spectrum of sampled x_A[n]');
> xlim([-600 600]);               % zoom around baseband
> ```

![[Images/DSP_Exam_F24_2_Spectrum_Aliased.png]]

---

## 2-4) 4th-order analog Butterworth AA-filter

We insert an **analog low-pass Butterworth anti-aliasing filter** before the sampler:  

- Type: 4th-order Butterworth LP  
- Passband edge: $F_p = 350$ Hz  

### (a) Prototype coefficients

From the **Butterworth LP prototype table** in Appendix 1: (3 dB normalized LP, $\varepsilon = 1$) for order $n = 4$:

The prototype transfer function is
$$
H_\text{proto}(s) = \frac{\beta_0}{s^4 + \alpha_3 s^3 + \alpha_2 s^2 + \alpha_1 s + \alpha_0},
$$
with
$$
\beta_0 = 1,\quad
\alpha_4 = 1,\quad
\alpha_3 = 2.6131,\quad
\alpha_2 = 3.4142,\quad
\alpha_1 = 2.6131,\quad
\alpha_0 = 1.
$$

So explicitly
$$
H_\text{proto}(s) = \frac{1}{s^4 + 2.6131\,s^3 + 3.4142\,s^2 + 2.6131\,s + 1}.
$$

### (b) Transform prototype → analog low-pass with $F_p = 350$ Hz

We design an analog LP with cutoff at $\Omega_p = 2\pi F_p$ using the standard low-pass frequency scaling
$$
s \;\mapsto\; \frac{s}{\Omega_p}.
$$

In MATLAB this is done with `lp2lp`:

> [!code]- MATLAB — 2-4 AA-filter design  
> ```matlab
> % Problem 2-4: 4th-order analog Butterworth AA-filter
> Fp = 350;                  % Hz
> Omegap = 2*pi*Fp;          % rad/s
> 
> % Prototype (n = 4) from Appendix 1 table
> B_proto = 1;
> A_proto = [1 2.6131 3.4142 2.6131 1];
> 
> % Scale to desired cutoff using lp2lp
> [B_AA, A_AA] = lp2lp(B_proto, A_proto, Omegap);
> 
> % Build transfer function object (optional)
> H_AA = tf(B_AA, A_AA);
> 
> disp('Analog AA filter H_AA(s) = ');
> H_AA
> ```

From the solution sheet, one possible numerical form is:
$$
H_{AA}(s) \approx
\frac{2.339\cdot 10^{13}}
{s^4 + 5747s^3 + 1.651\cdot 10^7 s^2 + 2.779\cdot 10^{10}s + 2.339\cdot 10^{13}}.
$$

---

## 2-5) Magnitude of AA-filter

We want $|H_{AA}(j\Omega)|$ as a function of **analog frequency** $F$ in Hz.  

Steps:

1. Make a frequency grid $F \in [0, F_{\max}]$ (e.g. up to a few kHz).  
2. Convert to angular frequency $\Omega = 2\pi F$.  
3. Use `freqs(B_AA, A_AA, Omega)` to evaluate the analog frequency response.  
4. Plot $|H_{AA}(j\Omega)|$ vs $F$.

> [!code]- MATLAB — 2-5 AA magnitude plot
> ```matlab
> % Problem 2-5: magnitude response of analog AA filter
> Fmax_plot = 2000;                     % Hz
> F = linspace(0, Fmax_plot, 2000);     % freq axis in Hz
> Omega = 2*pi*F;                       % rad/s
> 
> H_aa = freqs(B_AA, A_AA, Omega);      % analog frequency response
> 
> figure;
> plot(F, abs(H_aa), 'LineWidth', 1.5); grid on;
> xlabel('Analog frequency F [Hz]');
> ylabel('|H_{AA}(j\Omega)|');
> title('Analog AA-filter magnitude response (Butterworth, 4th order)');
> xline(Fp, '--r', 'F_p');
> ```

![[Images/DSP_Exam_F24_2_AA_Filter_Magnitude.png]]

Interpreting the plot:

- Below $F_p = 350$ Hz: magnitude close to 1 (little attenuation).  
- Above $F_p$: magnitude rolls off smoothly with Butterworth characteristic, strongly attenuating components near and above 750 Hz → reduces aliasing in the sampled system.

---

# Problem 3 — Sampling Criteria, Discrete Filter, Min-Phase / All-Pass

This problem mixes **sampling theory**, a simple **FIR filter**, and **factorization** of an LTI system into minimum-phase and all-pass parts.  

---

## 3-1) Sampling criteria for a band-limited signal

> Given: analog signal $f_a(t)$ with Fourier transform $F_a(\Omega)$ supported on $|\Omega|\le 200$ rad/s (from the exam spectrum plot).  
> Consider sampling with angular sampling frequencies
> $$
 \Omega_s \in \{200, 400, 500\}\,\text{rad/s}.
 $$
> For each case, decide if the **sampling criterion** is fulfilled.

Nyquist condition in angular form:
$$
\Omega_s \ge 2\Omega_{\max},
\qquad \Omega_{\max} = 200~\text{rad/s}.
$$

### Case (a) $\Omega_s = 200$ rad/s

$$
\Omega_s = 200 < 2\cdot 200 = 400
\Rightarrow \text{criterion NOT fulfilled (aliasing).}
$$

### Case (b) $\Omega_s = 400$ rad/s

$$
\Omega_s = 400 = 2\cdot 200
\Rightarrow \text{criterion JUST fulfilled (critical sampling).}
$$

### Case (c) $\Omega_s = 500$ rad/s

$$
\Omega_s = 500 > 400
\Rightarrow \text{criterion clearly fulfilled (oversampling).}
$$

---

## 3-2) New signal with $\Omega_{\max} = 250$ rad/s

> New band-limited signal $g_a(t)$ with maximum angular frequency $\Omega_{\max} = 250$ rad/s.  
> Which of the same three sampling frequencies satisfy Nyquist now?

Again
$$
\Omega_s \ge 2\Omega_{\max} = 2\cdot 250 = 500~\text{rad/s}.
$$

- $\Omega_s=200$ rad/s: $200<500$ → **no**  
- $\Omega_s=400$ rad/s: $400<500$ → **no**  
- $\Omega_s=500$ rad/s: $500=500$ → **yes, exactly at Nyquist**

So **only** $\Omega_s=500$ rad/s satisfies the sampling criterion.

---

## 3-3) Discrete filter: impulse response and frequency response

> Difference equation  
> $$
 y[n] = 0.5\,x[n-1] + 0.7\,x[n].
 $$

### (a) Impulse response and stability/causality

Impulse response is defined as the output for input $x[n]=\delta[n]$:

Compute for a few $n$:
- $n=0$: $y[0] = 0.5\,x[-1] + 0.7\,x[0] = 0.7$  
- $n=1$: $y[1] = 0.5\,x[0]  + 0.7\,x[1] = 0.5$  
- $n\ge 2$ or $n<0$: all $x[\cdot]=0$ → $y[n]=0$.

So
$$
h[n] = 0.7\delta[n] + 0.5\delta[n-1].
$$

**Causality:** $h[n] = 0$ for $n<0$ → causal.  

**Stability:** finite-length impulse response (2 non-zero values) → absolutely summable → BIBO stable.

### (b) Frequency response

Definition:
$$
H_{\text{filter}}(\omega) = \sum_{n} h[n]e^{-j\omega n}
= 0.7e^{-j\omega\cdot 0} + 0.5e^{-j\omega\cdot 1}
= 0.7 + 0.5e^{-j\omega}.
$$

So
$$
\boxed{H_{\text{filter}}(\omega) = 0.7 + 0.5e^{-j\omega}}.
$$

> [!code]- MATLAB — 3-3 filter analysis
> ```matlab
> % Problem 3-3: FIR filter
> h = [0.7 0.5];            % h[0], h[1]
> 
> % Frequency response
> Nw = 1024;
> [Hf, w] = freqz(h, 1, Nw);
> 
> figure;
> subplot(2,1,1);
> plot(w, abs(Hf)); grid on;
> xlabel('\omega [rad/sample]'); ylabel('|H(e^{j\omega})|');
> title('Magnitude of H_{filter}(e^{j\omega})');
> 
> subplot(2,1,2);
> plot(w, unwrap(angle(Hf))); grid on;
> xlabel('\omega [rad/sample]'); ylabel('\angle H(e^{j\omega}) [rad]');
> title('Phase of H_{filter}(e^{j\omega})');
> ```

![[Images/DSP_Exam_F24_3_FIR_MagPhase.png]]

---

## 3-4) Factorization into minimum-phase and all-pass parts

> Given causal LTI system function  
> $$
 H(z) =
 \frac{(1+3z^{-1})(1-\tfrac12 z^{-1})}{z^{-1}(1+\tfrac13 z^{-1})}.
 $$
> Find
> - $H_{\min}(z)$: minimum-phase system  
> - $H_{\text{ap}}(z)$: all-pass system  
> such that $H(z) = H_{\min}(z)\,H_{\text{ap}}(z)$ (up to a gain factor).

---

### Step 1 — Locate zeros and poles

Rewrite numerator/denominator in standard form:

- Factor $(1+3z^{-1})$ gives a zero at $z=-3$ (**outside** unit circle)  
- Factor $(1-\tfrac12 z^{-1})$ gives a zero at $z=\tfrac12$ (**inside**)  
- Factor $z^{-1}$ corresponds to a pole at $z=0$ (**inside**)  
- Factor $(1+\tfrac13 z^{-1})$ gives a pole at $z=-\tfrac13$ (**inside**)

So:

- Zeros: $z=-3$ and $z=0.5$  
- Poles: $z=0$ and $z=-1/3$

A **minimum-phase** system must have **all zeros inside** the unit circle (poles also inside for causal/stable).  
The “bad” zero is $z=-3$; its **reflected** (minimum-phase) version is
$$
z_{\text{ref}} = \frac{1}{\overline{-3}} = -\tfrac13.
$$

---

### Step 2 — All-pass section for the “bad” zero

For a first-order all-pass whose **zero** is at $z_0$ (outside) and **pole** is at $p$ (inside) with
$$
z_0 = \frac{1}{\overline{p}},
$$
a convenient form is
$$
H_{\text{ap}}(z) = G\,\frac{1 - z_0 z^{-1}}{1 - p z^{-1}},
$$
where the gain $G$ is chosen so that $|H_{\text{ap}}(e^{j\omega})| = 1$.

Here we want
- zero at $z_0 = -3$  
- pole at $p = -\tfrac13$  

These satisfy $z_0 = 1/\overline{p}$, so the all-pass factor is
$$
H_{\text{ap}}(z)
= G\,\frac{1 - (-3) z^{-1}}{1 - (-\tfrac13) z^{-1}}
= G\,\frac{1 + 3z^{-1}}{1 + \tfrac13 z^{-1}}.
$$

Check that it is all-pass (up to the constant $G$):

- zeros: $z=-3$
- poles: $z=-\tfrac13$
- indeed $-3 = 1/\overline{-\tfrac13}$ ⇒ zero and pole are reciprocal conjugates.

To make it **strictly all-pass** (unit magnitude on the unit circle), choose $G=\tfrac13$ (you can verify that this normalizes the magnitude to 1). So one clean choice is:
$$
H_{\text{ap}}(z)
= \frac13\,\frac{1 + 3z^{-1}}{1 + \tfrac13 z^{-1}}.
$$

---

### Step 3 — Remaining minimum-phase part

We now write
$$
H(z) = H_{\min}(z)\,H_{\text{ap}}(z).
$$

Start from the original $H(z)$:
$$
H(z) = \frac{(1+3z^{-1})(1-\tfrac12 z^{-1})}{z^{-1}(1+\tfrac13 z^{-1})}.
$$

Divide out the chosen all-pass:
$$
H_{\min}(z)
= \frac{H(z)}{H_{\text{ap}}(z)}
= \frac{\displaystyle
\frac{(1+3z^{-1})(1-\tfrac12 z^{-1})}{z^{-1}(1+\tfrac13 z^{-1})}}
{\displaystyle
\frac13\,\frac{1 + 3z^{-1}}{1 + \tfrac13 z^{-1}} }.
$$

Cancel the common factors $(1+3z^{-1})$ and $(1+\tfrac13 z^{-1})$:
$$
H_{\min}(z)
= 3\,\frac{1-\tfrac12 z^{-1}}{z^{-1}}.
$$

So we can take
$$
\boxed{
H_{\min}(z) = 3\,\frac{1-\tfrac12 z^{-1}}{z^{-1}},
\qquad
H_{\text{ap}}(z) = \frac13\,\frac{1 + 3z^{-1}}{1 + \tfrac13 z^{-1}}
}
$$
and then
$$
H(z) = H_{\min}(z)\,H_{\text{ap}}(z)
$$
exactly.

---

### Step 4 — Check minimum-phase property

For
$$
H_{\min}(z) = 3\,\frac{1-\tfrac12 z^{-1}}{z^{-1}},
$$
multiply numerator and denominator by $z$:
$$
H_{\min}(z) = 3\,\frac{z - \tfrac12}{1}.
$$

- Zero at $z = 0.5$ (inside unit circle)  
- No finite poles (only at $z=\infty$ in this normalized form)

So **all zeros are inside** the unit circle and there are no unstable poles ⇒ $H_{\min}(z)$ is **minimum-phase**

---

> [!code]- MATLAB — 3-4 factorization check
> ```matlab
> % Problem 3-4: verify H(z) = Hmin(z)*Hap(z)
> syms z
> 
> H  = (1+3*z^-1)*(1-0.5*z^-1)/(z^-1*(1+1/3*z^-1));
> Hmin = 3*(1-0.5*z^-1)/(z^-1);
> Hap  = (1/3)*(1+3*z^-1)/(1+1/3*z^-1);
> 
> H_simplified = simplify(Hmin*Hap);
> disp(H_simplified);   % should simplify to H
> ```

---

# Problem 4 — BLT IIR Bandstop Butterworth Design

> Goal: design a **digital IIR bandstop Butterworth filter** using the **Bilinear Transform (BLT)** with  
> $$\alpha = \frac{2}{T_s},\quad T_s = \frac{1}{F_s}.$$
> Specifications (digital, normalized by $F_s$):  
> - Lower/upper **passband** edges:  
>   $$f_{pL} = \frac{45.0}{F_s},\quad f_{pH} = \frac{55.5}{F_s}$$
> - Lower/upper **stopband** edges:  
>   $$f_{sL} = \frac{48.0}{F_s},\quad f_{sH} = \frac{52.1}{F_s}$$
> - Passband ripple: $A_p = 3$ dB  
> - Stopband attenuation: $A_s = 20$ dB  
> - Sampling frequency: $F_s = 5000$ Hz

Workflow:

1. **Prewarping:** digital $\to$ analog edge frequencies.  
2. Design analog **prototype low-pass Butterworth**.  
3. Transform prototype $\to$ analog **bandstop** $H_{BS}(s)$.  
4. Apply **BLT** to get digital $H_{BS}(z)$.  
5. Check frequency response vs specifications.

---

## 4-1) Analog prototype: edge frequencies, order, transfer function

### (a) Prewarped analog edge frequencies

Digital normalized frequency (in Hz) is $f = F/F_s$, and corresponding digital angular frequency is
$$
\omega = 2\pi f = 2\pi \frac{F}{F_s}.
$$

Under BLT with parameter $\alpha=2/T_s$, the **frequency warping** relation between **analog** angular frequency $\Omega$ and **digital** angular frequency $\omega$ is
$$
\Omega = \alpha \tan\left(\frac{\omega}{2}\right)
      = \frac{2}{T_s}\tan\left(\frac{\omega}{2}\right)
      = 2F_s \tan\left(\pi\frac{F}{F_s}\right).
$$

So for each digital edge at $F$ Hz we compute
$$
\Omega = 2F_s \tan\left(\pi \frac{F}{F_s}\right).
$$

Using the given numerical values and $F_s=5000$ Hz, the solution sheet gives approximately:​

- Stopband edges:
  $$
  \Omega_{sL} \approx 3.01\cdot 10^2~\text{rad/s},\quad
  \Omega_{sH} \approx 3.27\cdot 10^2~\text{rad/s};
  $$
- Passband edges:
  $$
  \Omega_{pL} \approx 2.82\cdot 10^2~\text{rad/s},\quad
  \Omega_{pH} \approx 3.49\cdot 10^2~\text{rad/s}.
  $$

> [!code]- MATLAB — 4-1a prewarping helper
> ```matlab
> % Problem 4-1a: prewarp edge frequencies
> Fs   = 5000;
> fpL  = 45.0;  fpH  = 55.5;
> fsL  = 48.0;  fsH  = 52.1;
> 
> prewarp = @(F) 2*Fs*tan(pi*F/Fs);   % F in Hz -> Omega in rad/s
> 
> omega_pL = prewarp(fpL);
> omega_pH = prewarp(fpH);
> omega_sL = prewarp(fsL);
> omega_sH = prewarp(fsH);
> 
> fprintf('Omega_sL = %.2e rad/s\n', omega_sL);
> fprintf('Omega_sH = %.2e rad/s\n', omega_sH);
> fprintf('Omega_pL = %.2e rad/s\n', omega_pL);
> fprintf('Omega_pH = %.2e rad/s\n', omega_pH);
> ```

### (b) Minimum prototype order $n$

For a **Butterworth low-pass** prototype, amplitude squared is
$$
|H(j\Omega)|^2 = \frac{1}{1+\epsilon^2 \left(\frac{\Omega}{\Omega_c}\right)^{2n}}.
$$

- Passband ripple $A_p$ and stopband attenuation $A_s$ define
  $$
  \epsilon^2 = 10^{A_p/10}-1,\qquad
  \left(\frac{\Omega_s}{\Omega_p}\right)^{2n}
  = \frac{10^{A_s/10}-1}{10^{A_p/10}-1}.
  $$

For bandstop design we form an effective **stopband frequency ratio** $v_s \approx 2.56$ (see solution) and passband ratio $v_p\approx 1$.

With $A_p=3$ dB, $A_s=20$ dB we get
$$
\epsilon^2 = 10^{0.3}-1 \approx 1,\quad \Rightarrow \epsilon \approx 1.
$$

Then the Butterworth order formula is
$$
n \ge \frac{\log_{10}\Big(\frac{10^{A_s/10}-1}{10^{A_p/10}-1}\Big)}{2\log_{10}(v_s)}.
$$

Numerically this yields
$$
n \approx 2.44 \Rightarrow n_{\min} = 3.
$$

So we choose **3rd-order prototype**.

### (c) Prototype transfer function for $n=3$

From the Butterworth prototype table (3 dB, $n=3$):​  
$$
H_{\text{proto}}(s) = \frac{1}{s^3 + 2s^2 + 2s + 1}.
$$`

In MATLAB:

> [!code]- MATLAB — 4-1c prototype
> ```matlab
> % Problem 4-1c: 3rd-order Butterworth prototype
> B_proto = 1;
> A_proto = [1 2 2 1];       % s^3 + 2 s^2 + 2 s + 1
> H_proto = tf(B_proto, A_proto);
> ```

---

## 4-2) Analog bandstop filter $H_{BS}(s)$

### (a) Transform LP prototype → bandstop

A LP prototype $H_{\text{proto}}(s)$ is transformed to a **bandstop** filter with center frequency
$$
\Omega_0 = \sqrt{\Omega_{sL}\Omega_{sH}} \approx 3.14\cdot 10^2~\text{rad/s},
$$
and bandwidth
$$
B = \Omega_{pH} - \Omega_{pL} \approx 66.0~\text{rad/s},
$$
using transformation
$$
s \mapsto \frac{s^2 + \Omega_0^2}{Bs}.
$$

In MATLAB this is easily done via `lp2bs`:

> [!code]- MATLAB — 4-2a bandstop transform
> ```matlab
> % Problem 4-2a: analog bandstop from LP prototype
> Omega0 = sqrt(omega_sL*omega_sH);
> B      = omega_pH - omega_pL;
> 
> [B_BS, A_BS] = lp2bs(B_proto, A_proto, Omega0, B);
> H_BS = tf(B_BS, A_BS);
> disp('Analog bandstop H_BS(s) = ');
> H_BS
> ```

From the solution sheet, one numeric form is:
$$
H_{BS}(s) =
\frac{s^6 - 1.148\cdot 10^{-13}s^5 + 2.964\cdot 10^5 s^4 - 2.269\cdot 10^{-8}s^3
      + 2.928\cdot 10^{10} s^2 - 1.121\cdot 10^{-3}s + 9.642\cdot 10^{14}}
     {s^6 + 132.1 s^5 + 3.051\cdot 10^5 s^4 + 2.638\cdot 10^7 s^3
      + 3.014\cdot 10^{10} s^2 + 1.289\cdot 10^{12} s + 9.642\cdot 10^{14}}.
$$

### (b) Magnitude of $H_{BS}(j\Omega)$

We can now compute and plot the analog frequency response using `freqs`:

> [!code]- MATLAB — 4-2b analog BS magnitude
> ```matlab
> % Problem 4-2b: analog bandstop magnitude
> Omega = linspace(0, 3000, 4000);   % rad/s
> H_bs  = freqs(B_BS, A_BS, Omega);
> 
> figure;
> plot(Omega/(2*pi), abs(H_bs), 'LineWidth', 1.5); grid on;
> xlabel('Analog frequency F [Hz]');
> ylabel('|H_{BS}(j\Omega)|');
> title('Analog bandstop magnitude response');
> 
> hold on;
> xline(omega_pL/(2*pi), '--g', 'F_{pL}');
> xline(omega_pH/(2*pi), '--g', 'F_{pH}');
> xline(omega_sL/(2*pi), '--r', 'F_{sL}');
> xline(omega_sH/(2*pi), '--r', 'F_{sH}');
> ```

![[Images/DSP_Exam_F24_4_Analog_Bandstop_Magnitude.png]]

Interpretation: low attenuation in passbands (below $\Omega_{pL}$ and above $\Omega_{pH}$), strong notch around $\Omega_0$, and at least 20 dB attenuation within the stopband between $\Omega_{sL}$ and $\Omega_{sH}$.

---

## 4-3) Digital bandstop filter $H_{BS}(z)$ via BLT

We now map the **analog bandstop** into the **digital z-domain** using the Bilinear Transform
$$
s = \frac{2}{T_s}\frac{1 - z^{-1}}{1 + z^{-1}}
   = 2F_s \frac{1 - z^{-1}}{1 + z^{-1}}.
$$

In MATLAB this is done via `bilinear` with numerator/denominator of the analog filter:​

> [!code]- MATLAB — 4-3a BLT and digital frequency response
> ```matlab
> % Problem 4-3a: bilinear transform -> digital IIR
> [Bz, Az] = bilinear(B_BS, A_BS, Fs);
> 
> % Digital transfer function (optional):
> H_BS_z = tf(Bz, Az, 1/Fs);   % sample time Ts = 1/Fs
> 
> % Magnitude response in dB vs f*Fs (Hz)
> f = linspace(0, Fs/2, 2000);    % 0..Nyquist
> [Hdig, wdig] = freqz(Bz, Az, f, Fs);  % wdig is in Hz here
> 
> MagdB = 20*log10(abs(Hdig));
> 
> figure;
> plot(f, MagdB, 'LineWidth', 1.5); grid on;
> xlabel('f [Hz]'); ylabel('|H_{BS}(e^{j\omega})| [dB]');
> title('Digital bandstop IIR (BLT) — magnitude in dB');
> hold on;
> xline(45,  '--g', 'f_{pL}');
> xline(55.5,'--g', 'f_{pH}');
> xline(48,  '--r', 'f_{sL}');
> xline(52.1,'--r', 'f_{sH}');
> ```

![[Images/DSP_Exam_F24_4_Digital_Bandstop_Magnitude_dB.png]]

From the solution sheet, the digital transfer function can be written as:​
$$
H_{BS}(z)
= \frac{0.9869 - 5.91z^{-1} + 14.76z^{-2} - 19.67z^{-3} + 14.76z^{-4} - 5.91z^{-5} + 0.9869z^{-6}}
       {1 - 5.962z^{-1} + 14.82z^{-2} - 19.67z^{-3} + 14.69z^{-4} - 5.858z^{-5} + 0.974z^{-6}}.
$$

### (b) Attenuation at band edges

Using the plotted magnitude in dB vs $f$, we read off approximate values at the specified edges:

- At 45 Hz (lower passband edge): $\approx -2.9$ dB  
- At 55.5 Hz (upper passband edge): $\approx -3.1$ dB  
- At 48 Hz (lower stopband edge): $\approx -24.5$ dB  
- At 52.1 Hz (upper stopband edge): $\approx -24.5$ dB  
- The notch center around 50 Hz reaches about $-108.5$ dB


### (c) Compare to specifications

- **Passband requirement:** $A_p = 3$ dB max ripple  
  - At 45 Hz and 55.5 Hz, attenuation is around $3$ dB → satisfies the spec.
- **Stopband requirement:** $A_s = 20$ dB min attenuation  
  - At 48 Hz and 52.1 Hz, attenuation is about $24.5$ dB → better than required.
- The deep notch at 50 Hz gives much more suppression than required at the center frequency.

Hence, the designed **digital IIR bandstop filter** meets and exceeds the stated specifications.

> [!code]- MATLAB — 4-3b quick numeric check of edges
> ```matlab
> % Problem 4-3b: numeric attenuation at specified frequencies
> f_edges = [45 48 50 52.1 55.5];
> [H_edges, ~] = freqz(Bz, Az, f_edges, Fs);
> Att_edges_dB = 20*log10(abs(H_edges));
> 
> table(f_edges(:), Att_edges_dB(:), ...
>       'VariableNames', {'Frequency_Hz','Magnitude_dB'})
> ```

---
## Appendix 1 — Butterworth lowpass prototype filters

3 dB Butterworth lowpass prototype transfer functions ($\varepsilon = 1$)

| Order $n$ | Lowpass prototype transfer function $H_{\text{LP}}(s)$ |
|:---------:|:------------------------------------------------------|
| 1 | $H_{\text{LP}}(s) = \frac{1}{s + 1}$ |
| 2 | $H_{\text{LP}}(s) = \frac{1}{s^2 + 1.4142\,s + 1}$ |
| 3 | $H_{\text{LP}}(s) = \frac{1}{s^3 + 2s^2 + 2s + 1}$ |
| 4 | $H_{\text{LP}}(s) = \frac{1}{s^4 + 2.6131\,s^3 + 3.4142\,s^2 + 2.6131\,s + 1}$ |
| 5 | $H_{\text{LP}}(s) = \frac{1}{s^5 + 3.2361\,s^4 + 5.2361\,s^3 + 5.2361\,s^2 + 3.2361\,s + 1}$ |
| 6 | $H_{\text{LP}}(s) = \frac{1}{s^6 + 3.8637\,s^5 + 7.4641\,s^4 + 9.1416\,s^3 + 7.4641\,s^2 + 3.8637\,s + 1}$ |
