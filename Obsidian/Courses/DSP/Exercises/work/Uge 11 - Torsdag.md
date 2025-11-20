  > Exercise sheet: [[62743 E25 Digital Signal Processing Uge 11 Torsdag.pdf]]  
> Solution sheet: [[62743 E25 Digital Signal Processing Uge 11 Torsdag solutions.pdf]]  
> Slides: [[62743 E25 Digital filter design FIR part2.pdf]]  
> MATLAB live script: [Open](file:///C:/Users/Mads2/DTU/3.semester/DSP/UGE%2011/Torsdag.mlx)

---
# Week 11 — FIR Design (Windowing & Frequency Sampling)

---

## 📘 Concept Overview

This Thursday is about **two FIR design methods**:

1. **Fourier-transform method + windowing**  
   - Start from an **ideal LP frequency response** (brick-wall).  
   - Compute **ideal impulse response** (sinc-shaped, infinite length, non-causal).  
   - Truncate around $n=0$ → corresponds to a **rectangular window** in time.  
   - This gives strong **Gibbs oscillations** (ripples) in the stopband.  
   - Apply a smoother window (e.g. **Hamming**) to reduce sidelobes at the cost of a wider transition band.

2. **Frequency-sampling method**  
   - Sample the desired frequency response $H_d(e^{j\omega})$ at equally spaced $\omega_k$.  
   - For **linear-phase FIR** with **symmetric** impulse response, only $K+1$ points are needed.  
   - Use a cosine-series formula to recover the **FIR coefficients** $b[n]$.  

Key ideas from the slides:

- **Windowing trade-off**:  
  - Rectangular window: narrowest main lobe, but high sidelobes ($\approx -13$ dB).  
  - Hamming window: wider main lobe, but much lower sidelobes ($\approx -40$ dB).  
- **Linear phase**: symmetric FIR ($h[n] = h[M-n]$) ⇒  
  $$
  H(e^{j\omega}) = e^{-j\omega K} A(\omega),
  $$
  where $A(\omega)$ is real and approximately non-negative in the passband ⇒ **pure delay** $K$ samples.

---

## Exercise 1 — FIR LP via Fourier Transform + Window

**Given**

- FIR **low-pass** filter  
- $N_\text{taps} = 23$  
- $F_c = 2000~\text{Hz}$  
- $F_s = 8000~\text{Hz}$  

---

### 1-A) Ideal LP impulse response and FIR coefficients (rectangular window)

> **Task**  
> 1. Find the **ideal LP impulse response** using Fourier transform.  
> 2. Truncate to $23$ taps and form a **causal FIR**.  
> 3. Plot the impulse response.

**Theory**

Relationship between analog frequency $F$ (Hz) and discrete-time angular frequency $\omega$ (rad/sample):

$$
\omega = 2\pi \frac{F}{F_s}.
$$

Cutoff angular frequency:

$$
\omega_c = 2\pi \frac{F_c}{F_s} 
         = 2\pi\frac{2000}{8000}
         = 0.5\pi~\text{rad/sample}.
$$

Ideal LP amplitude response:

$$
H_{\text{LP,ideal}}(e^{j\omega}) =
\begin{cases}
1, & |\omega| \le \omega_c,\\
0, & \omega_c < |\omega| \le \pi.
\end{cases}
$$

Inverse DTFT gives the (infinite-length) ideal impulse response:

- For $n \neq 0$:
  $$
  h_{\text{LP,ideal}}[n] =
  \dfrac{\sin(\omega_c n)}{\pi n}.
  $$

- For $n = 0$:
  $$
  h_{\text{LP,ideal}}[0] = \dfrac{\omega_c}{\pi} = 0.5.
  $$

Using MATLAB’s normalized $\text{sinc}$:
- By definition $\text{sinc}(x) = \dfrac{\sin(\pi x)}{\pi x}$, so we can write
  $$
  h_{\text{LP,ideal}}[n] = \frac{\omega_c}{\pi}
  \,\text{sinc}\!\left(\frac{\omega_c}{\pi}n\right)
  = \frac{\omega_c}{\pi}\,\text{sinc}(0.5n).
  $$

**Truncation to 23 taps**

For $N_\text{taps} = 23$:

- Filter order: $M = N_\text{taps} - 1 = 22$  
- $N_\text{taps} = 2K+1 \Rightarrow K = 11$  

We keep the samples for $n = -K,\dots,K = -11,\dots,11$.  
A **causal** FIR is obtained by shifting:

$$
b[n] = h_{\text{LP,ideal}}[n-K], \quad n = 0,1,\dots,22.
$$

So the 23-tap rectangular-window coefficients are:

$$
b[n] = \frac{\omega_c}{\pi}\,\text{sinc}\big(0.5(n-11)\big), \quad n=0,\dots,22.
$$

> [!code]- MATLAB (1-A)
> ```matlab
> Fs  = 8000;
> Fc  = 2000;
> wc  = 2*pi*Fc/Fs;         % 0.5*pi
>
> Ntaps1 = 23;
> M1     = Ntaps1 - 1;      % 22
> K1     = M1/2;            % 11
> n1     = 0:M1;            % 0..22
> n1c    = n1 - K1;         % -11..11
>
> % Ideal LP impulse response (centered)
> hLP_centered = (wc/pi) * sinc((wc/pi)*n1c);
>
> % Rectangular-window FIR coefficients (causal)
> b_rect = hLP_centered;    % b[n] = h[n-K1]
>
> figure;
> stem(n1, b_rect, 'filled'); grid on;
> xlabel('n'); ylabel('h_{\text{rect}}[n]');
> title('23-tap LP (rectangular window) impulse response');
> ```
> MATLAB docs: [`sinc`](https://www.mathworks.com/help/signal/ref/sinc.html), [`stem`](https://www.mathworks.com/help/matlab/ref/stem.html)

![[Images/DSP_U11_Torsdag_1A_rect_impulse.png]]

---

### 1-B) Magnitude response vs normalized angular frequency

> **Task**  
> Use `freqz` to plot the **magnitude response** versus normalized angular frequency $\omega$ and overlay the **ideal LP brick-wall**.

**Frequency response**

For an FIR with coefficients $b[n]$:

$$
H(e^{j\omega}) = \sum_{n=0}^{M} b[n] e^{-j\omega n}.
$$

Using `freqz(b,1,N)` we sample $H(e^{j\omega})$ for $N$ points in $[0,\pi]$.

The ideal LP magnitude:

$$
|H_{\text{ideal}}(e^{j\omega})| =
\begin{cases}
1, & 0 \le \omega \le \omega_c,\\
0, & \omega_c < \omega \le \pi.
\end{cases}
$$

> [!code]- MATLAB (1-B)
> ```matlab
> Nw = 2048;
> [H_rect, w_rect] = freqz(b_rect, 1, Nw);  % w_rect in [0,pi]
>
> H_ideal_w = double(w_rect <= wc);        % ideal brick-wall
>
> figure;
> plot(w_rect/pi, abs(H_rect), 'LineWidth', 1.5); hold on;
> plot(w_rect/pi, H_ideal_w, '--', 'LineWidth', 1.5);
> grid on;
> xlabel('\omega/\pi'); ylabel('|H(e^{j\omega})|');
> title('23-tap LP: magnitude vs normalized frequency');
> legend('Realized LP', 'Ideal LP', 'Location','best');
> ```
> MATLAB docs: [`freqz`](https://www.mathworks.com/help/signal/ref/freqz.html)
![[Images/DSP_U11_Torsdag_1B_mag_norm.png]]
![[Images/DSP_U11_Torsdag_1B_mag_norm.png]]
![[Images/DSP_U11_Torsdag_1B_mag_norm.png]]

![[Images/DSP_U11_Torsdag_1B_mag_norm.png]]

---

### 1-C) Magnitude vs frequency in Hz and first side-lobe level

> **Task**  
> 1. State the relation between frequency $F$ [Hz] and normalized angular frequency $\omega$.  
> 2. State the maximum frequency that avoids aliasing.  
> 3. Plot the magnitude vs $F$ [Hz] and overlay the ideal LP.  
> 4. Plot the **log-magnitude** $H_{\text{dB}}(F)$ and note the first **side-lobe peak**.

**Relations**

$$
\omega = 2\pi \frac{F}{F_s}
\quad\Rightarrow\quad
F = \frac{\omega}{2\pi} F_s.
$$

The **Nyquist frequency** is:

$$
F_\text{max} = \frac{F_s}{2} = 4000~\text{Hz}.
$$

**Magnitude vs frequency**

We map $w_{\text{rect}}$ (rad/sample) to $F$ (Hz):

$$
F = \frac{w_{\text{rect}}}{2\pi} F_s.
$$

Log-magnitude in dB:

$$
H_{\text{dB}}(F) = 20\log_{10} |H(F)|.
$$

For a rectangular-window design you should observe:

- A **narrow transition region** near $F_c = 2000~\text{Hz}$.  
- **Gibbs oscillations** (side-lobes) in the stopband; the first side-lobe is typically around $\approx -13$ dB relative to the passband.

> [!code]- MATLAB (1-C)
> ```matlab
> F = w_rect*Fs/(2*pi);      % Hz
>
> % Linear magnitude
> figure;
> plot(F, abs(H_rect), 'LineWidth', 1.5); hold on;
> plot(F, double(w_rect <= wc), '--', 'LineWidth', 1.5);
> grid on;
> xlabel('F [Hz]'); ylabel('|H(F)|');
> title('23-tap LP: magnitude vs frequency');
> xline(Fs/2, ':k', 'F_s/2');
> legend('Realized LP', 'Ideal LP', 'Location','best');
>
> % Log magnitude (dB)
> HdB_rect = 20*log10(abs(H_rect)+eps);
> figure;
> plot(F, HdB_rect, 'LineWidth', 1.5); grid on;
> xlabel('F [Hz]'); ylabel('H_{\text{dB}}(F) [dB]');
> title('23-tap LP: log-magnitude (rectangular window)');
>
> % Optional: crude search for the first stopband peak
> idx_sb = find(F > Fc);                 % stopband
> [peak_sb, idx_local] = max(HdB_rect(idx_sb));
> F_peak = F(idx_sb(idx_local));
> fprintf('First visible stopband peak ~ %.2f dB at F ≈ %.1f Hz\n', ...
>         peak_sb, F_peak);
> ```
> MATLAB docs: [`freqz`](https://www.mathworks.com/help/signal/ref/freqz.html)

![[Images/DSP_U11_Torsdag_1C_mag_Hz.png]]

![[Images/DSP_U11_Torsdag_1C_logmag_rect.png]]

---

### 1-D) Hamming window expression

> **Task**  
> Write the expression for the **Hamming window** $w_{\text{Ham}}[n]$ for $n=0,\dots,M$.

For a length-$N$ window with $M = N-1$:

$$
w_{\text{Ham}}[n] =
0.54 - 0.46\cos\left(\frac{2\pi n}{M}\right), \quad n=0,1,\dots,M.
$$

For this exercise: $N = 23$, so $M = 22$.

---

### 1-E) Hamming window coefficients and stem plot

> **Task**  
> Compute the **Hamming window coefficients** and plot them.  
> What should the minimum and maximum $x$-axis values be?

We use the formula with $M = 22$:

$$
w_{\text{Ham}}[n] =
0.54 - 0.46\cos\left(\frac{2\pi n}{22}\right), \quad n = 0,\dots,22.
$$

So the $x$-axis for the stem plot should run from **$n=0$ to $n=22$**.

> [!code]- MATLAB (1-E)
> ```matlab
> M1 = 22;
> n1 = 0:M1;
>
> % Manual Hamming window
> wHam = 0.54 - 0.46*cos(2*pi*n1/M1);
>
> % (Optional) Compare with built-in hamming()
> wHam_builtin = hamming(M1+1).';
> max_diff = max(abs(wHam - wHam_builtin));
> fprintf('Max diff(manual, built-in) = %.2e\n', max_diff);
>
> figure;
> stem(n1, wHam, 'filled'); grid on;
> xlabel('n'); ylabel('w_{\text{Ham}}[n]');
> title('23-point Hamming window');
> xlim([0 M1]);   % 0..22
> ```
> MATLAB docs: [`hamming`](https://www.mathworks.com/help/signal/ref/hamming.html), [`stem`](https://www.mathworks.com/help/matlab/ref/stem.html)

![[Images/DSP_U11_Torsdag_1E_hamming_window.png]]

---

### 1-F) Windowed impulse response $h_w[n]$

> **Task**  
> Use
> $$
> h_w[n] = h_{\text{LP,ideal}}[n-K] \, w_{\text{Ham}}[n], \quad n=0,\dots,M
> $$
> to compute and plot the **windowed impulse response**.

We already have:

- $h_{\text{LP,ideal}}[n-K] = b[n]$ from 1-A.  
- $w_{\text{Ham}}[n]$ from 1-E.

So:

$$
h_w[n] = b[n]\;w_{\text{Ham}}[n],\quad n=0,\dots,22.
$$

> [!code]- MATLAB (1-F)
> ```matlab
> % Rectangular LP coefficients from 1-A
> % b_rect = hLP_centered;
>
> h_w = b_rect .* wHam;      % windowed FIR coefficients
>
> figure;
> stem(n1, h_w, 'filled'); grid on;
> xlabel('n'); ylabel('h_w[n]');
> title('23-tap LP with Hamming window (impulse response)');
> ```
> MATLAB docs: [`hamming`](https://www.mathworks.com/help/signal/ref/hamming.html), [`stem`](https://www.mathworks.com/help/matlab/ref/stem.html)

![[Images/DSP_U11_Torsdag_1F_impulse_hamming.png]]

---

### 1-G) Comparison: rectangular vs Hamming on log scale

> **Task**  
> 1. Plot the **log-magnitude** of the windowed FIR vs $F$ [Hz].  
> 2. Overlay the log-magnitude of the **rectangular** design from 1-C.  
> 3. Comment on the **first side-lobe level** and the **transition width**.

Let $H_{\text{Ham}}(e^{j\omega})$ be the frequency response of $h_w[n]$:

$$
H_{\text{dB,Ham}}(F) = 20\log_{10}\left|H_{\text{Ham}}(F)\right|.
$$

**Observed effects**

- The **Hamming window** significantly **reduces side-lobe levels** (stopband ripples).  
  - Rectangular: first side-lobe around $\approx -13$ dB.  
  - Hamming: first side-lobe around $\approx -40$ dB.
- In exchange, the **main lobe widens**, i.e. the **transition band** around $F_c$ becomes **wider**.  
- This is the classic **windowing trade-off**: lower sidelobes vs wider transition.

> [!code]- MATLAB (1-G)
> ```matlab
> [H_ham, ~] = freqz(h_w, 1, w_rect);   % reuse w_rect and F from 1-C
> HdB_ham = 20*log10(abs(H_ham)+eps);
>
> figure;
> plot(F, HdB_rect, 'LineWidth', 1.5); hold on;
> plot(F, HdB_ham, 'LineWidth', 1.5);
> grid on;
> xlabel('F [Hz]'); ylabel('H_{\text{dB}}(F) [dB]');
> title('23-tap LP: rectangular vs Hamming (log-magnitude)');
> legend('Rectangular (simple truncation)', ...
>        'Hamming-windowed', 'Location','best');
>
> % Optional: quick comparison of dominant stopband peaks
> idx_sb = find(F > Fc);
> [peak_rect, iR] = max(HdB_rect(idx_sb));
> [peak_ham,  iH] = max(HdB_ham(idx_sb));
> fprintf('Rectangular: first visible stopband peak ~ %.2f dB\n', peak_rect);
> fprintf('Hamming:    first visible stopband peak ~ %.2f dB\n', peak_ham);
> ```
> MATLAB docs: [`freqz`](https://www.mathworks.com/help/signal/ref/freqz.html)

![[Images/DSP_U11_Torsdag_1G_logmag_rect_vs_hamming.png]]

---

## Exercise 2 — Frequency-Sampling Design (7-tap LP)

**Given**

- FIR **low-pass** filter  
- $N_\text{taps} = 7$  
- Linear phase, **symmetric** impulse response  
- Cutoff $\omega_c = 0.3\pi$  

We design using the **frequency-sampling method**.

---

### 2-A) Parameters $M$ and $K$

> **Task**  
> Determine $M$ and $K$ for a **7-tap** linear-phase FIR.

Number of taps:

$$
N_\text{taps} = 7 = M+1 \quad\Rightarrow\quad M = 6.
$$

For **Type I** linear-phase (odd length):

$$
M = 2K \quad\Rightarrow\quad K = \frac{M}{2} = 3.
$$

So:

- $M = 6$  
- $K = 3$  

---

### 2-B) Sampled frequencies $\omega_k$

> **Task**  
> For $k = 0,\dots,K$, compute
> $$
> \omega_k = \frac{2\pi k}{M+1}.
> $$

We have $M+1 = 7$:

$$
\omega_k = \frac{2\pi k}{7},\quad k=0,1,2,3.
$$

Numerically:

- $k = 0$: $\omega_0 = 0$  
- $k = 1$: $\omega_1 = \dfrac{2\pi}{7} \approx 0.8976 \approx 0.286\pi$  
- $k = 2$: $\omega_2 = \dfrac{4\pi}{7} \approx 1.7952 \approx 0.571\pi$  
- $k = 3$: $\omega_3 = \dfrac{6\pi}{7} \approx 2.6928 \approx 0.857\pi$

> [!code]- MATLAB (2-B)
> ```matlab
> K2 = 3;
> M2 = 2*K2;           % 6
> Ntaps2 = M2 + 1;     % 7
>
> k  = 0:K2;
> wk = 2*pi*k/(M2+1);  % omega_k
> fprintf('w_k/pi = ['); fprintf(' %.4f', wk/pi); fprintf(' ]\n');
> ```

---

### 2-C) Which $\omega_k$ are in the passband?

> **Task**  
> For each $\omega_k$, determine if $\omega_k \le \omega_c$ (passband) or $\omega_k > \omega_c$ (stopband), given $\omega_c = 0.3\pi$.

We have:

- $\omega_c = 0.3\pi \approx 0.9425$  

Compare:

- $\omega_0 = 0 \le 0.3\pi$ ⇒ **passband**  
- $\omega_1 = \dfrac{2\pi}{7} \approx 0.286\pi < 0.3\pi$ ⇒ **passband**  
- $\omega_2 = \dfrac{4\pi}{7} \approx 0.571\pi > 0.3\pi$ ⇒ **stopband**  
- $\omega_3 = \dfrac{6\pi}{7} \approx 0.857\pi > 0.3\pi$ ⇒ **stopband**

So:

- Passband samples: $k = 0,1$  
- Stopband samples: $k = 2,3$

> [!code]- MATLAB (2-C)
> ```matlab
> wc2 = 0.3*pi;
> in_pass = wk <= wc2;
> fprintf('Passband flags (k=0..3): '); disp(in_pass);
> ```

---

### 2-D) Desired sampled values $H[k]$

> **Task**  
> Specify $H[k]$ for $k=0,\dots,K$ for an **ideal LP**.

For an ideal low-pass with passband up to $\omega_c$:

$$
H[k] =
\begin{cases}
1, & \omega_k \le \omega_c,\\
0, & \omega_k > \omega_c.
\end{cases}
$$

From 2-C:

- $H[0] = 1$, $H[1] = 1$, $H[2] = 0$, $H[3] = 0$.

> [!code]- MATLAB (2-D)
> ```matlab
> Hk = double(in_pass);    % [1 1 0 0]
> fprintf('H[k] = ['); fprintf(' %.1f', Hk); fprintf(' ]\n');
> ```

---

### 2-E) Coefficients $b[n]$ for $n = 0,\dots,K$

> **Task**  
> Use the **frequency-sampling formula**:
> $$
> b[n] = h[n] =
> \frac{1}{2K+1}\left(
> H[0] + 2 \sum_{k=1}^{K} H[k]
> \cos\left(\frac{2\pi k (n-K)}{2K+1}\right)
> \right), \quad n = 0,\dots,K.
> $$
> Insert $M$, $K$ and $H[k]$ and compute $b[0],\dots,b[3]$ in MATLAB.

Here $K = 3$, so $2K+1 = 7$, and

$$
b[n] = \frac{1}{7}\left(
H[0] + 2\sum_{k=1}^{3} H[k]
\cos\left(\frac{2\pi k (n-3)}{7}\right)
\right).
$$

Since $H[2]=H[3]=0$, only $H[1]$ contributes:

$$
b[n] = \frac{1}{7}\left(
1 + 2\cos\left(\frac{2\pi (n-3)}{7}\right)
\right), \quad n = 0,1,2,3.
$$

Numerically:

- $b[0] \approx -0.11456$  
- $b[1] \approx 0.07928$  
- $b[2] \approx 0.32100$  
- $b[3] \approx 0.42857$

> [!code]- MATLAB (2-E)
> ```matlab
> K2 = 3;
> M2 = 2*K2;
> Ntaps2 = M2 + 1;          % 7
>
> k   = 0:K2;
> wk  = 2*pi*k/(M2+1);
> wc2 = 0.3*pi;
> Hk  = double(wk <= wc2);  % [1 1 0 0]
>
> n_left = 0:K2;
> b_left = zeros(size(n_left));
>
> for ii = 1:length(n_left)
>     n = n_left(ii);
>     k_vec = 1:K2;
>     inner = sum( Hk(2:end) .* cos(2*pi*k_vec*(n-K2)/(2*K2+1)) );
>     b_left(ii) = (1/(2*K2+1)) * ( Hk(1) + 2*inner );
> end
>
> fprintf('b[0..3] = ['); fprintf(' %.4f', b_left); fprintf(' ]\n');
> % Expect approximately: [-0.1146  0.0793  0.3210  0.4286]
> ```

---

### 2-F) Use symmetry to get all 7 coefficients

> **Task**  
> Use the symmetry relation
> $$
> b[n] = h[n] = h[M-n],\quad n = 0,1,\dots,K-1
> $$
> to determine $b[4],b[5],b[6]$ and list all $b[0],\dots,b[6]$.

For a symmetric FIR of order $M=6$:

- $b[6] = b[0] \approx -0.11456$  
- $b[5] = b[1] \approx 0.07928$  
- $b[4] = b[2] \approx 0.32100$

So the full coefficient vector is:

$$
\begin{aligned}
b[0] &\approx -0.11456,\\
b[1] &\approx 0.07928,\\
b[2] &\approx 0.32100,\\
b[3] &\approx 0.42857,\\
b[4] &\approx 0.32100,\\
b[5] &\approx 0.07928,\\
b[6] &\approx -0.11456.
\end{aligned}
$$

> [!code]- MATLAB (2-F)
> ```matlab
> % From 2-E: b_left = [b0 b1 b2 b3]
> b2 = zeros(1, Ntaps2);
> b2(1:K2+1)        = b_left;        % n=0..3
> b2(Ntaps2:-1:K2+2) = b_left(1:K2); % n=4..6
>
> fprintf('Full b[n] = ['); fprintf(' %.4f', b2); fprintf(' ]\n');
> ```

---

### 2-G) Transfer function and frequency response

> **Task**  
> 1. Write the transfer function $H(z)$ in terms of $b[n]$.  
> 2. Use `freqz` to plot **magnitude** and **phase**.

The FIR transfer function:

$$
H(z) = \sum_{n=0}^{6} b[n] z^{-n}.
$$

With the computed coefficients:

$$
\begin{aligned}
H(z) \approx
& -0.11456
+ 0.07928 z^{-1}
+ 0.32100 z^{-2}
+ 0.42857 z^{-3} \\
& + 0.32100 z^{-4}
+ 0.07928 z^{-5}
- 0.11456 z^{-6}.
\end{aligned}
$$

The filter is **linear-phase** (Type I), so the phase is approximately a straight line in the passband with group delay $K = 3$ samples.

> [!code]- MATLAB (2-G)
> ```matlab
> Nw2 = 2048;
> [H2, w2] = freqz(b2, 1, Nw2);
> HdB2 = 20*log10(abs(H2)+eps);
>
> figure;
> subplot(2,1,1);
> plot(w2/pi, abs(H2), 'LineWidth', 1.5); grid on;
> xlabel('\omega/\pi'); ylabel('|H(e^{j\omega})|');
> title('7-tap LP (frequency sampling): magnitude');
>
> subplot(2,1,2);
> plot(w2/pi, unwrap(angle(H2)), 'LineWidth', 1.5); grid on;
> xlabel('\omega/\pi'); ylabel('\angle H(e^{j\omega}) [rad]');
> title('7-tap LP (frequency sampling): phase');
> ```
> MATLAB docs: [`freqz`](https://www.mathworks.com/help/signal/ref/freqz.html)

![[Images/DSP_U11_Torsdag_2H_freqsampling_mag_phase.png]]

---
