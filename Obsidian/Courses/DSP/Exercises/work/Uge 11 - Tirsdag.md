> Quick refs: [[Digital Filter Design — FIR (Part 1)]]  
> Exercise sheet: [[62743 E25 Digital Signal Processing Uge 11 Tirsdag.pdf]]  
> solution sheet: [[62743 E25 Digital Signal Processing Uge 11 Tirsdag solutions.pdf]]

---

# Week 11 — FIR Design via Fourier Transform

---

## 📘 Concept Overview

In this week you design **FIR filters** via the **Fourier-transform method**: :contentReference[oaicite:0]{index=0}  

1. Start from an **ideal frequency response** (low-pass or band-pass).  
2. Use the **inverse DTFT** to derive the **ideal impulse response** (usually infinite length, non-causal).  
3. Truncate symmetrically around 0 to obtain a **finite-length sequence**.  
4. Shift the sequence to make it **causal** and interpret the shifted samples as **FIR coefficients**.

For an *ideal low-pass* with cutoff angular frequency $\omega_c$:
- For $n \neq 0$:
  $$
  h_{\text{LP,ideal}}[n] = \frac{\sin(\omega_c n)}{\pi n}
  $$
- For $n = 0$:
  $$
  h_{\text{LP,ideal}}[0] = \frac{\omega_c}{\pi}
  $$

For an *ideal band-pass* with lower and upper angular cutoffs $\omega_L$, $\omega_H$:
- For $n \neq 0$:
  $$
  h_{\text{BP,ideal}}[n] = \frac{\sin(\omega_H n) - \sin(\omega_L n)}{\pi n}
  $$
- For $n = 0$:
  $$
  h_{\text{BP,ideal}}[0] = \frac{\omega_H - \omega_L}{\pi}
  $$

The **finite-length FIR filter** is then obtained by:
- Choosing an odd number of taps $N_\text{taps} = M+1 = 2K+1$  
- Keeping $h[n]$ only for $n=-K,\dots,K$  
- Defining filter coefficients
  $$
  b[n] = h[n-K], \quad n = 0,1,\dots,M
  $$

---

## Exercise 1 — FIR Low-pass (Fourier-transform design)

> **Given**   
> - FIR low-pass  
> - $N_\text{taps} = 7$  
> - $F_c = 800~\text{Hz}$  
> - $F_s = 8000~\text{Hz}$  

---

### 1-A) Normalized angular cut-off $\omega_c$ and ideal LP impulse response

> **Exercise description**  
> 1. Compute the **normalized digital cut-off angular frequency** $\omega_c$ (rad/sample).  
> 2. Derive the **ideal low-pass impulse response** from the DTFT.  
> 3. State whether the ideal impulse response is **finite or infinite**.

> [!theory] **Theory Recap**  
> Relationship between analog frequency $F$ (Hz) and **digital angular frequency** $\omega$ (rad/sample):
> $$
> \omega = 2\pi \frac{F}{F_s}
> $$
> For an ideal low-pass with cutoff $\omega_c$:
> $$
> H_{\text{LP,ideal}}(e^{j\omega}) =
> \begin{cases}
> 1, & |\omega| \le \omega_c,\\
> 0, & \omega_c < |\omega| \le \pi.
> \end{cases}
> $$
> Using the **inverse DTFT** gives:
> - For $n \neq 0$:
>   $$
>   h_{\text{LP,ideal}}[n] = \frac{\sin(\omega_c n)}{\pi n}
>   $$
> - For $n = 0$:
>   $$
>   h_{\text{LP,ideal}}[0] = \frac{\omega_c}{\pi}
>   $$
> This ideal impulse response extends from $n=-\infty$ to $n=+\infty$ → **infinite length**.

**Cutoff computation**

$$
\omega_c = 2\pi \frac{F_c}{F_s}
        = 2\pi \frac{800}{8000}
        = 0.2\pi
        \approx 0.6283~\text{rad/sample}.
$$

**Ideal impulse response (before truncation)**

$$
h_{\text{LP,ideal}}[n] =
\begin{cases}
\dfrac{\sin(0.2\pi n)}{\pi n}, & n \neq 0\\[4pt]
\dfrac{0.2\pi}{\pi} = 0.2, & n = 0
\end{cases}
$$

**Answer about length**

- The ideal impulse response is **infinite** (non-implementable directly).  

> [!code]- MATLAB (1-A)
> ```matlab
> % Exercise 1-A: cutoff and ideal LP impulse response (symbolic form)
> Fs = 8000;
> Fc = 800;
> wc = 2*pi*Fc/Fs;        % 0.2*pi rad/sample
> fprintf('omega_c = %.6f rad/sample (%.3f*pi)\n', wc, wc/pi);
>
> % generic anonymous function for ideal LP (infinite-length)
> hLP_ideal = @(n) (n==0).* (wc/pi) + ...
>                 (n~=0).* (sin(wc*n)./(pi*n));
> ```

---

### 1-B) Determine $K$, $M$ and calculate FIR coefficients (7 taps)

> **Exercise description**  
> Use $N_\text{taps} = 7$ and the Fourier design relation
> $$
> b_\text{LP}[n] = h[n-K], \quad n = 0,1,\dots,M
> $$
> with $N_\text{taps}=M+1=2K+1$, to determine **$K$, $M$** and compute the **filter coefficients**.

From the hint: $N_\text{taps} = M+1 = 2K+1 = 7$:

- $M = N_\text{taps} - 1 = 6$  
- $2K + 1 = 7 \Rightarrow K = 3$

We truncate the *ideal* impulse response to $n=-3,\dots,3$:

For $\omega_c = 0.2\pi$:

\[
\begin{aligned}
h[-3] &= \frac{\sin(0.2\pi\cdot(-3))}{\pi (-3)} \approx 0.100910,\\
h[-2] &= \frac{\sin(0.2\pi\cdot(-2))}{\pi (-2)} \approx 0.151365,\\
h[-1] &= \frac{\sin(0.2\pi\cdot(-1))}{\pi (-1)} \approx 0.187098,\\
h[0]  &= 0.2,\\
h[1]  &= h[-1] \approx 0.187098,\\
h[2]  &= h[-2] \approx 0.151365,\\
h[3]  &= h[-3] \approx 0.100910.
\end{aligned}
\]

Using $b_\text{LP}[n] = h[n-K] = h[n-3]$ for $n=0,\dots,6$:

\[
\begin{aligned}
b_\text{LP}[0] &= h[-3] \approx 0.100910,\\
b_\text{LP}[1] &= h[-2] \approx 0.151365,\\
b_\text{LP}[2] &= h[-1] \approx 0.187098,\\
b_\text{LP}[3] &= h[0] \approx 0.200000,\\
b_\text{LP}[4] &= h[1] \approx 0.187098,\\
b_\text{LP}[5] &= h[2] \approx 0.151365,\\
b_\text{LP}[6] &= h[3] \approx 0.100910.
\end{aligned}
\]

So the 7-tap FIR LP coefficients are:

$$
b_\text{LP} \approx
\begin{bmatrix}
0.10091 & 0.15137 & 0.18710 & 0.20000 & 0.18710 & 0.15137 & 0.10091
\end{bmatrix}.
$$

> [!code]- MATLAB (1-B)
> ```matlab
> % Exercise 1-B: 7-tap LP FIR coefficients
> Ntaps1 = 7;
> M1 = Ntaps1 - 1;       % 6
> K1 = (Ntaps1 - 1)/2;   % 3
>
> n_trunc = -K1:K1;      % -3:3
> hLP_trunc = hLP_ideal(n_trunc);   % ideal LP, truncated
>
> bLP7 = hLP_trunc;      % since n_trunc is -K..K, shifting later by K
> % Coefficients mapped as b[n] = h[n-K], n = 0..M
> % In MATLAB, we usually keep b as h(-K..K) directly:
> fprintf('bLP7 = [');
> fprintf(' %.6f', bLP7);
> fprintf(' ]\n');
> ```

---

### 1-C) Transfer function $H(z)$ for the 7-tap LP

> **Exercise description**  
> Write the FIR transfer function in the form  
> $$
> H(z) = b_0 + b_1 z^{-1} + \dots + b_6 z^{-6}.
> $$

Using the coefficients from 1-B:

\[
\begin{aligned}
H(z) &= 0.10091
      + 0.15137 z^{-1}
      + 0.18710 z^{-2}
      + 0.20000 z^{-3} \\
    &\quad+ 0.18710 z^{-4}
      + 0.15137 z^{-5}
      + 0.10091 z^{-6}.
\end{aligned}
\]

> [!code]- MATLAB (1-C)
> ```matlab
> % Exercise 1-C: transfer function for 7-tap LP
> B_LP7 = bLP7;      % numerator
> A_LP7 = 1;         % pure FIR
> % H(z) = poly2sym(fliplr(B_LP7), z^-1) if using Symbolic Toolbox
> ```

---

### 1-D) Magnitude and phase response (7 taps)

> **Exercise description**  
> Use `freqz` to plot **magnitude** and **phase** of the FIR low-pass.  
> Mark the cut-off angular frequency $\omega_c = 0.2\pi$.

> [!theory] **Theory Recap**  
> For an FIR filter with coefficients $b[n]$, the frequency response is
> $$
> H(e^{j\omega}) = \sum_{n=0}^{M} b[n] e^{-j\omega n}.
> $$
> `freqz(b,1,N)` evaluates $H(e^{j\omega})$ on $N$ points on $[0,\pi]$.  
> The phase should be **approximately linear** in the passband for a symmetric FIR.

> [!code]- MATLAB (1-D)
> ```matlab
> % Exercise 1-D: magnitude and phase for 7-tap LP
> Nfft = 2048;
> [H7, w7] = freqz(B_LP7, A_LP7, Nfft);   % w7 in rad/sample
>
> figure;
> subplot(2,1,1);
> plot(w7, abs(H7), 'LineWidth', 1.5); grid on;
> hold on; xline(wc, '--r', '\omega_c');
> xlabel('\omega [rad/sample]'); ylabel('|H(e^{j\omega})|');
> title('7-tap LP: Magnitude response');
>
> subplot(2,1,2);
> plot(w7, unwrap(angle(H7)), 'LineWidth', 1.5); grid on;
> hold on; xline(wc, '--r', '\omega_c');
> xlabel('\omega [rad/sample]'); ylabel('\angle H(e^{j\omega}) [rad]');
> title('7-tap LP: Phase response');
> ```

---

### 1-E) Impulse response plot (7 taps)

> **Exercise description**  
> Plot the **impulse response** of the designed 7-tap FIR filter.

> [!code]- MATLAB (1-E)
> ```matlab
> % Exercise 1-E: impulse response of 7-tap LP
> figure;
> stem(0:M1, B_LP7, 'filled'); grid on;
> xlabel('n'); ylabel('h[n]');
> title('7-tap LP FIR impulse response');
> ```

---

### 1-F) 51-tap LP FIR with same cutoff

> **Given**   
> - FIR low-pass  
> - $N_\text{taps} = 51$  
> - $F_c = 800~\text{Hz}$  
> - $F_s = 8000~\text{Hz}$  

> **Exercise description**  
> Repeat the design with **51 taps** and plot magnitude and phase.  
> Mark $\omega_c$ on the plots.

We have:

- $N_\text{taps} = 51 \Rightarrow M = 50$  
- $2K+1 = 51 \Rightarrow K = 25$

Truncation interval: $n = -25,\dots,25$.

Ideal (before truncation):
$$
h_{\text{LP,ideal}}[n] =
\begin{cases}
\dfrac{\sin(0.2\pi n)}{\pi n}, & n \neq 0\\[4pt]
0.2, & n = 0
\end{cases}
$$

Truncated & shifted impulse response:

$$
b_{\text{LP,51}}[n] = h_{\text{LP,ideal}}[n-K],\quad n=0,1,\dots,50,\;K=25.
$$

> [!code]- MATLAB (1-F)
> ```matlab
> % Exercise 1-F: 51-tap LP FIR
> Ntaps51 = 51;
> M51 = Ntaps51 - 1;         % 50
> K51 = (Ntaps51 - 1)/2;     % 25
>
> n_trunc51 = -K51:K51;
> hLP_trunc51 = hLP_ideal(n_trunc51);
> bLP51 = hLP_trunc51;       % symmetric coefficients
>
> [H51, w51] = freqz(bLP51, 1, Nfft);
>
> figure;
> subplot(2,1,1);
> plot(w51, abs(H51), 'LineWidth', 1.5); grid on;
> hold on; xline(wc, '--r', '\omega_c');
> xlabel('\omega [rad/sample]'); ylabel('|H(e^{j\omega})|');
> title('51-tap LP: Magnitude response');
>
> subplot(2,1,2);
> plot(w51, unwrap(angle(H51)), 'LineWidth', 1.5); grid on;
> hold on; xline(wc, '--r', '\omega_c');
> xlabel('\omega [rad/sample]'); ylabel('\angle H(e^{j\omega}) [rad]');
> title('51-tap LP: Phase response');
> ```

---

### 1-G) Comparison of 7- vs 51-tap filters

> **Exercise description**  
> Compare the **magnitude** and **phase** of the 7- and 51-tap LP filters.  
> - Comment on transition width and stopband behavior.  
> - Explain why the phase is (approximately) **linear** in the passband.  
> - Name the oscillations in the stopband and their origin.

**Observations**

- **Magnitude / transition**:  
  - 7-tap LP: wider transition band, more ripple in the stopband.  
  - 51-tap LP: much **sharper transition** (narrower transition band) and stronger attenuation in the stopband.

- **Phase**:  
  For a **symmetric FIR** ($b[n]=b[M-n]$), the phase response is **approximately linear** with frequency in the passband:
  $$
  H(e^{j\omega}) = e^{-j\omega K} \cdot A(\omega)
  $$
  where $K = M/2$ and $A(\omega)$ is real and (approximately) nonnegative in the passband.  
  The factor $e^{-j\omega K}$ introduces a **pure delay** of $K$ samples → linear phase.

- **Stopband oscillations**:  
  The ripples/oscillations seen in the stopband are **Gibbs oscillations**.  
  They arise because truncating the ideal (sinc) impulse response with a **rectangular window** corresponds to **convolving** the ideal brick-wall response with the Fourier transform of the rectangular window, which has significant sidelobes.

> [!code]- MATLAB (1-G) — Overlay
> ```matlab
> % Exercise 1-G: overlay magnitude and phase
> figure;
> subplot(2,1,1);
> plot(w7,  abs(H7),  'LineWidth', 1.5); hold on;
> plot(w51, abs(H51), 'LineWidth', 1.5);
> grid on; xline(wc, '--k', '\omega_c');
> legend('7 taps', '51 taps', 'Location','best');
> xlabel('\omega [rad/sample]'); ylabel('|H(e^{j\omega})|');
> title('LP FIR: 7 vs 51 taps (magnitude)');
>
> subplot(2,1,2);
> plot(w7,  unwrap(angle(H7)),  'LineWidth', 1.5); hold on;
> plot(w51, unwrap(angle(H51)), 'LineWidth', 1.5);
> grid on; xline(wc, '--k', '\omega_c');
> legend('7 taps', '51 taps', 'Location','best');
> xlabel('\omega [rad/sample]'); ylabel('\angle H(e^{j\omega}) [rad]');
> title('LP FIR: 7 vs 51 taps (phase)');
> ```

---

## Exercise 2 — FIR Band-pass (Fourier-transform design)

> **Given**   
> - FIR **band-pass** filter  
> - $N_\text{taps} = 9$  
> - Lower cutoff $F_L = 2000~\text{Hz}$  
> - Upper cutoff $F_H = 2400~\text{Hz}$  
> - Sampling rate $F_s = 8000~\text{Hz}$  

---

### 2-A) $\omega_L$, $\omega_H$, $K$, $M$, and band-pass impulse response

> **Exercise description**  
> 1. Compute the **normalized angular cutoffs** $\omega_L$, $\omega_H$.  
> 2. Determine $K$ and $M$ from $N_\text{taps} = M+1=2K+1$.  
> 3. Derive the **ideal band-pass impulse response** using Fourier design.  
> 4. State whether the impulse response is FIR or IIR.

**Angular cutoffs**

$$
\omega_L = 2\pi\frac{F_L}{F_s}
         = 2\pi\frac{2000}{8000}
         = 0.5\pi
         \approx 1.5708~\text{rad/sample}
$$
$$
\omega_H = 2\pi\frac{F_H}{F_s}
         = 2\pi\frac{2400}{8000}
         = 0.6\pi
         \approx 1.8850~\text{rad/sample}
$$

**Taps**

$$
N_\text{taps} = 9 \Rightarrow M = 8,\quad 2K+1 = 9 \Rightarrow K = 4.
$$

**Ideal band-pass impulse response**

From the ideal band-pass frequency response:

$$
h_{\text{BP,ideal}}[n] =
\begin{cases}
\dfrac{\sin(\omega_H n) - \sin(\omega_L n)}{\pi n}, & n \neq 0\\[4pt]
\dfrac{\omega_H - \omega_L}{\pi}, & n = 0
\end{cases}
$$

Numerically for $n=-4,\dots,4$:

\[
\begin{aligned}
h[-4] &\approx 0.075683,\\
h[-3] &\approx 0.043737,\\
h[-2] &\approx -0.093549,\\
h[-1] &\approx -0.015579,\\
h[ 0] &= 0.1,\\
h[ 1] &\approx -0.015579,\\
h[ 2] &\approx -0.093549,\\
h[ 3] &\approx 0.043737,\\
h[ 4] &\approx 0.075683.
\end{aligned}
\]

**FIR vs IIR**

- The **ideal** band-pass impulse response is **infinite length** (extends for all $n$) → conceptually **IIR**.  
- After truncation to $n=-K,\dots,K$ and shifting to $n=0,\dots,M$, the **implemented filter** is **FIR** (finite impulse response).

> [!code]- MATLAB (2-A)
> ```matlab
> % Exercise 2-A: band-pass ideal impulse response
> Fs2 = 8000;
> FL = 2000; FH = 2400;
> wL = 2*pi*FL/Fs2; % 0.5*pi
> wH = 2*pi*FH/Fs2; % 0.6*pi
>
> NtapsBP = 9;
> M_BP = NtapsBP - 1;      % 8
> K_BP = (NtapsBP - 1)/2;  % 4
>
> hBP_ideal = @(n) (n==0).*((wH - wL)/pi) + ...
>                 (n~=0).*((sin(wH*n) - sin(wL*n))./(pi*n));
>
> nBP_trunc = -K_BP:K_BP;
> hBP_trunc = hBP_ideal(nBP_trunc);
> fprintf('hBP_trunc (n=-4..4) = [');
> fprintf(' %.6f', hBP_trunc);
> fprintf(' ]\n');
> ```

---

### 2-B) FIR band-pass coefficients

> **Exercise description**  
> Use the relation
> $$
> b_\text{BP}[n] = h[n-K], \quad n = 0,1,\dots,M
> $$
> to compute the 9-tap band-pass filter coefficients.

With $K=4$, $M=8$:

\[
\begin{aligned}
b_\text{BP}[0] &= h[-4] \approx 0.075683,\\
b_\text{BP}[1] &= h[-3] \approx 0.043737,\\
b_\text{BP}[2] &= h[-2] \approx -0.093549,\\
b_\text{BP}[3] &= h[-1] \approx -0.015579,\\
b_\text{BP}[4] &= h[ 0] = 0.100000,\\
b_\text{BP}[5] &= h[ 1] \approx -0.015579,\\
b_\text{BP}[6] &= h[ 2] \approx -0.093549,\\
b_\text{BP}[7] &= h[ 3] \approx 0.043737,\\
b_\text{BP}[8] &= h[ 4] \approx 0.075683.
\end{aligned}
\]

So:

$$
b_\text{BP} \approx
\begin{bmatrix}
0.075683 & 0.043737 & -0.093549 & -0.015579 &
0.100000 & -0.015579 & -0.093549 & 0.043737 & 0.075683
\end{bmatrix}.
$$

> [!code]- MATLAB (2-B)
> ```matlab
> % Exercise 2-B: BP FIR coefficients (9 taps)
> bBP9 = hBP_trunc;    % because nBP_trunc = -K..K
> fprintf('bBP9 = [');
> fprintf(' %.6f', bBP9);
> fprintf(' ]\n');
> ```

---

### 2-C) Magnitude and phase of band-pass (9 taps)

> **Exercise description**  
> Plot **magnitude** and **phase** using `freqz`.  
> Mark $\omega_L$ and $\omega_H$ on the plot.

> [!code]- MATLAB (2-C)
> ```matlab
> % Exercise 2-C: magnitude & phase for 9-tap BP
> [HBP9, wBP9] = freqz(bBP9, 1, Nfft);
>
> figure;
> subplot(2,1,1);
> plot(wBP9, abs(HBP9), 'LineWidth', 1.5); grid on;
> hold on;
> xline(wL, '--r', '\omega_L');
> xline(wH, '--r', '\omega_H');
> xlabel('\omega [rad/sample]'); ylabel('|H(e^{j\omega})|');
> title('9-tap BP: Magnitude');
>
> subplot(2,1,2);
> plot(wBP9, unwrap(angle(HBP9)), 'LineWidth', 1.5); grid on;
> hold on;
> xline(wL, '--r', '\omega_L');
> xline(wH, '--r', '\omega_H');
> xlabel('\omega [rad/sample]'); ylabel('\angle H(e^{j\omega}) [rad]');
> title('9-tap BP: Phase');
> ```

---

### 2-D) Increase taps to 101 and compare

> **Exercise description**  
> Increase the number of taps from 9 to 101, design the new BP FIR, and plot magnitude and phase.  
> Compare with the 9-tap version.

For $N_\text{taps} = 101$:

- $M = 100$  
- $K = 50$  

Truncation interval $n = -50,\dots,50$ and:

$$
b_{\text{BP,101}}[n] = h_{\text{BP,ideal}}[n-K],\quad n = 0,\dots,100.
$$

**Expected behavior**

- The **transition regions** near $\omega_L$ and $\omega_H$ become sharper (narrower).  
- The **stopband attenuation** improves (lower sidelobes).  
- The phase remains approximately **linear** in the passband because the impulse response is still symmetric.

> [!code]- MATLAB (2-D)
> ```matlab
> % Exercise 2-D: 101-tap BP FIR and comparison
> NtapsBP101 = 101;
> M_BP101 = NtapsBP101 - 1;      % 100
> K_BP101 = (NtapsBP101 - 1)/2;  % 50
>
> nBP_trunc101 = -K_BP101:K_BP101;
> hBP_trunc101 = hBP_ideal(nBP_trunc101);
> bBP101 = hBP_trunc101;
>
> [HBP101, wBP101] = freqz(bBP101, 1, Nfft);
>
> figure;
> subplot(2,1,1);
> plot(wBP9,   abs(HBP9),   'LineWidth', 1.5); hold on;
> plot(wBP101, abs(HBP101), 'LineWidth', 1.5);
> grid on;
> xline(wL, '--k', '\omega_L');
> xline(wH, '--k', '\omega_H');
> legend('9 taps', '101 taps', 'Location','best');
> xlabel('\omega [rad/sample]'); ylabel('|H(e^{j\omega})|');
> title('BP FIR: 9 vs 101 taps (magnitude)');
>
> subplot(2,1,2);
> plot(wBP9,   unwrap(angle(HBP9)),   'LineWidth', 1.5); hold on;
> plot(wBP101, unwrap(angle(HBP101)), 'LineWidth', 1.5);
> grid on;
> xline(wL, '--k', '\omega_L');
> xline(wH, '--k', '\omega_H');
> legend('9 taps', '101 taps', 'Location','best');
> xlabel('\omega [rad/sample]'); ylabel('\angle H(e^{j\omega}) [rad]');
> title('BP FIR: 9 vs 101 taps (phase)');
> ```

---

**References**

- Exercise sheet: [[62743 E25 Digital Signal Processing Uge 11 Tirsdag.pdf]]   
- Slides: [[62743 E25 Digital filter design FIR part1.pdf]]
