---
title: Multirate Digital Signal Processing
type: formula
tags:
  - DSP
  - multirate
  - sampling
aliases:
  - Multirate DSP
  - Multirate Systems
links:
  - [[62743 E25 Digital Signal Processing Uge 12 Tirsdag.pdf]]
  - [[62743 E25 Multirate Digital Signal Processing.pdf]]
updated: 2025-11-24
---
> Quick refs: [[62743 E25 Multirate Digital Signal Processing.pdf]]   
> Exercises: [[62743 E25 Digital Signal Processing Uge 12 Tirsdag.pdf]]  
> Worked examples: [[Uge 12 - Tirsdag]]

---

# Multirate Digital Signal Processing — Formula Sheet

## 📋 Table of Contents

1. [[#1. Overview & Notation|1. Overview & Notation]]  
2. [[#2. Sampling Categories & Sampling Theorem|2. Sampling Categories & Sampling Theorem]]  
3. [[#3. Down-sampling (Decimation)|3. Down-sampling (Decimation)]]  
   - [[#3.1 Time-domain definition|3.1 Time-domain definition]]  
   - [[#3.2 Frequency-domain relations|3.2 Frequency-domain relations]]  
   - [[#3.3 Anti-aliasing (AA) filter|3.3 Anti-aliasing (AA) filter]]  
4. [[#4. Up-sampling (Interpolation)|4. Up-sampling (Interpolation)]]  
   - [[#4.1 Time-domain definition|4.1 Time-domain definition]]  
   - [[#4.2 Frequency-domain relations|4.2 Frequency-domain relations]]  
   - [[#4.3 Interpolation filter|4.3 Interpolation filter]]  
5. [[#5. Rational resampling by L/M|5. Rational resampling by L/M]]  
6. [[#6. Filter design recaps (Window, Frequency Sampling, Parks–McClellan)|6. Filter design recaps (Window, Frequency Sampling, Parks–McClellan)]]  
   - [[#6.1 Window-based FIR design (Fourier method)|6.1 Window-based FIR design (Fourier method)]]  
   - [[#6.2 Parks–McClellan (remez) basics|6.2 Parks–McClellan (remez) basics]]  
   - [[#6.3 Frequency sampling method & linear-phase types|6.3 Frequency sampling method & linear-phase types]]  
7. [[#7. MATLAB patterns for multirate DSP|7. MATLAB patterns for multirate DSP]]  
   - [[#7.1 Down-sampling (decimation) by M|7.1 Down-sampling (decimation) by M]]  
   - [[#7.2 Up-sampling (interpolation) by L|7.2 Up-sampling (interpolation) by L]]  
   - [[#7.3 Interpolation filter via Parks–McClellan (remez)|7.3 Interpolation filter via Parks–McClellan (remez)]]  
   - [[#7.4 Using the designed interpolation filter|7.4 Using the designed interpolation filter]]  

---

## 1. Overview & Notation

We work with three “domains”:

- **Analog signal**: $x_a(t)$ (continuous time).  
- **Discrete-time signal**: $x[n] = x_a(nT_s)$, with  
  $$
  F_s = \frac{1}{T_s}, \qquad F_\text{Nyq} = \frac{F_s}{2}.
  $$
- **Frequency variables**  
  - Analog frequency $F$ in Hz  
  - Digital angular frequency $\omega$ in rad/sample  

Relation:

$$
\omega = 2\pi \frac{F}{F_s}
\quad\Longleftrightarrow\quad
F = \frac{\omega}{2\pi}F_s.
$$

DTFT / $z$-transform:

- DTFT:
  $$
  X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n]e^{-j\omega n}.
  $$
- $z$-transform:
  $$
  X(z) = \sum_{n=-\infty}^{\infty}x[n]z^{-n},\quad z=e^{j\omega}.
  $$

---

## 2. Sampling Categories & Sampling Theorem

### Sampling categories (from slides)

- **Under-sampling** (analog → digital)
  - $F_s < 2B$ for a band-limited signal with bandwidth $B$  
  - ⇒ **frequency aliasing**.
- **Over-sampling** (analog → digital)
  - $F_s \gg 2B$  
  - Easier analog anti-aliasing filter, can down-sample later in digital domain.
- **Down-sampling** (decimation)
  - Change sample rate **downwards** in digital domain.
- **Up-sampling** (interpolation / expansion)
  - Change sample rate **upwards** in digital domain.
- **Re-sampling**
  - Sample-rate change by a rational factor $L/M$ (non-integer overall change).

### Sampling theorem & reconstruction

For an analog low-pass signal $x_a(t)$ with spectrum $X_a(F)$ supported in $|F|\le B$:

- **Nyquist condition**:
  $$
  F_s \ge 2B
  $$
  ⇒ no aliasing when sampling.

- Relation between analog and DT spectrum (from slides):
  $$
  X(F) = F_s \sum_{k=-\infty}^{\infty} X_a(F - kF_s).
  $$

- **Ideal reconstruction** from samples:
  $$
  x_a(t) = \sum_{n=-\infty}^{\infty}
  x[n]\,
  \mathrm{sinc}\!\left(\frac{\pi}{T_s}(t - nT_s)\right),
  $$
  where $\mathrm{sinc}(x) = \dfrac{\sin x}{x}$.

Slight over-sampling:

- Choosing $F_s > 2B$ makes AA-filter easier (transition region between $B$ and $F_s/2$) and allows later digital down-sampling.

---

## 3. Down-sampling (Decimation)

### 3.1 Time-domain definition

Down-sampling by integer factor $M>1$:

- Original sampling: $T_s$, $F_s = 1/T_s$.  
- New sampling: $T_s' = MT_s$, $F_s' = F_s/M$.  
- **Sample sequence**:
  $$
  x_D[n] = x[nM].
  $$

Block diagram notation: $\downarrow M$.

Effect:

- We keep every $M$’th sample and discard the rest.  
- Time axis is stretched by factor $M$.  

---

### 3.2 Frequency-domain relations

From the mathematical derivation in the slides:

- General DTFT relation:
  $$
  X_D(e^{j\omega}) = \frac{1}{M}
  \sum_{k=0}^{M-1}
  X\!\left(e^{j(\omega + 2\pi k)/M}\right),
  \qquad -\pi \le \omega \le \pi.
  $$

This shows:

- Spectrum is **compressed** by $M$ and **$M$ shifted copies** are added (folding).  
- If these copies overlap ⇒ **aliasing**.

Special cases from the slide examples:

- For $M=2$:
  $$
  X_{D2}(\omega) =
  \frac{1}{2}\left[
  X\!\left(\frac{\omega}{2}\right) +
  X\!\left(\frac{\omega}{2}-\pi\right)
  \right].
  $$
- For $M=3$:
  $$
  X_{D3}(\omega) =
  \frac{1}{3}\Big[
  X\!\left(\frac{\omega}{3}\right) +
  X\!\left(\frac{\omega}{3}-\tfrac{2\pi}{3}\right) +
  X\!\left(\frac{\omega}{3}-\tfrac{4\pi}{3}\right)
  \Big].
  $$

**No-aliasing condition**

If the original spectrum is confined to $|\omega| \le \omega_\text{max}$, then to avoid aliasing after decimation by $M$ we need:

$$
\omega_\text{max} \le \frac{\pi}{M}
\quad\Longleftrightarrow\quad
|F| \le \frac{F_s}{2M}.
$$

---

### 3.3 Anti-aliasing (AA) filter

To enforce this condition we use a **digital AA filter** before the down-sampler:

- Ideal AA filter (normalized angular frequency):
  $$
  H_D(\omega) =
  \begin{cases}
  1, & |\omega| < \dfrac{\pi}{M},\\[4pt]
  0, & \dfrac{\pi}{M} < |\omega| < \pi.
  \end{cases}
  $$

Spectral picture:

- Original $X(F)$ in $[-F_s/2, F_s/2]$.  
- After decimation by $M$, Nyquist frequency becomes $F_s' /2 = F_s/(2M)$ and we **fold** around this new Nyquist limit.  
- Without prefiltering, high-frequency content aliases into the baseband; with AA filter, that region is suppressed.

Implementation diagram (slides):

1. $x[n] \rightarrow$ AA filter $H_D(\omega)$  
2. Filter output $\rightarrow \downarrow M$  
3. Output $x_D[n]$ with sample rate $F_s/M$.

---

## 4. Up-sampling (Interpolation)

### 4.1 Time-domain definition

Up-sampling (expansion/interpolation) by factor $L>1$:

- Original sampling: $T_s$, $F_s = 1/T_s$.  
- New sampling: $T_s' = T_s/L$, $F_s' = L F_s$.

Zero-insertion (expanded sequence):

$$
x_E[n] =
\begin{cases}
x[k], & n = kL,\ k\in\mathbb Z,\\[4pt]
0, & \text{otherwise}.
\end{cases}
$$

Block diagram: $\uparrow L$.

Effect:

- We **insert $L-1$ zeros** between each original sample.  
- Time axis is compressed by factor $L$.

---

### 4.2 Frequency-domain relations

From the $z$-domain derivation (slides):

- For the expanded sequence:
  $$
  X_E(z) = X(z^L) \quad\Rightarrow\quad
  X_E(e^{j\omega}) = X(e^{j\omega L}).
  $$

Interpretation:

- Baseband spectrum is **compressed** by $L$ (in frequency), and **repeated** (images) across $[-\pi,\pi]$.  
- In normalized analog frequency, the same content now occupies a smaller fraction of the new Nyquist interval because $F_s'$ is larger.

The slide examples show:

- Zero-stuffed time-domain signal has many high-frequency components.  
- Spectrum has multiple **images** at multiples of $F_s'/L = F_s$.

---

### 4.3 Interpolation filter

We need an **interpolation / reconstruction / anti-image filter** after zero-insertion:

- Ideal interpolation filter:
  $$
  H_I(\omega) =
  \begin{cases}
  L, & |\omega| < \dfrac{\pi}{L},\\[4pt]
  0, & \dfrac{\pi}{L} < |\omega| < \pi.
  \end{cases}
  $$

Key points:

- Passband gain is $L$ to compensate for the zero-insertion (which scales average energy by $1/L$).  
- Acts as a **lowpass** that keeps the baseband and removes images.

Ideal impulse response (from FIR slides):

$$
h_I[n] = \mathrm{sinc}\!\left(\frac{n}{L}\right)
= \frac{\sin\left(\tfrac{\pi}{L}n\right)}{\tfrac{\pi}{L}n},
$$

scaled so that the passband gain is exactly $L$ and cutoff $\omega_c = \pi/L$.

---

## 5. Rational resampling by L/M

To change sample rate by a **rational factor** $L/M$:

1. **Up-sample** by $L$ (expansion).  
2. Filter by a suitable lowpass $H_{ID}(\omega)$ (interpolation + AA).  
3. **Down-sample** by $M$ (decimation).

Block diagram (slides):

- $x[n] \xrightarrow{\uparrow L} x_E[n] \xrightarrow{H_{ID}(\omega)} v[n] \xrightarrow{\downarrow M} x_{DE}[n]$.

Overall rate:

$$
F_s' = \frac{L}{M} F_s.
$$

### Combined filter $H_{ID}(\omega)$

Starting from ideal components:

- Interpolation filter:
  $$
  H_I(\omega) =
  \begin{cases}
  L, & |\omega| < \dfrac{\pi}{L},\\
  0, & \dfrac{\pi}{L} < |\omega| < \pi.
  \end{cases}
  $$
- AA filter:
  $$
  H_D(\omega) =
  \begin{cases}
  1, & |\omega| < \dfrac{\pi}{M},\\
  0, & \dfrac{\pi}{M} < |\omega| < \pi.
  \end{cases}
  $$

Combined:

$$
H_{ID}(\omega) = H_I(\omega) H_D(\omega).
$$

Cutoff:

$$
\omega_c = \min\!\left(\frac{\pi}{L}, \frac{\pi}{M}\right),
$$

so:

$$
H_{ID}(\omega) =
\begin{cases}
L, & |\omega| < \omega_c,\\
0, & \omega_c < |\omega| < \pi.
\end{cases}
$$

Slides show two cases:

- **Case I:** $\pi/M < \pi/L$ ⇒ AA filter is tighter.  
- **Case II:** $\pi/L < \pi/M$ ⇒ interpolation filter is tighter.

---

## 6. Filter design recaps (Window, Frequency Sampling, Parks–McClellan)

These are recap slides reused in the multirate lecture.

### 6.1 Window-based FIR design (Fourier method)

Recall:

1. Start from **ideal amplitude response**, e.g. ideal LP:
   $$
   H_\text{LP,ideal}(e^{j\omega}) =
   \begin{cases}
   1, & |\omega| \le \omega_c,\\
   0, & \omega_c < |\omega| \le \pi.
   \end{cases}
   $$
2. Compute **ideal impulse response** (non-causal, infinite):
   $$
   h_\text{ideal}[n] = \frac{\omega_c}{\pi}\,\mathrm{sinc}\!\left(\frac{\omega_c}{\pi}n\right).
   $$
3. Truncate symmetrically to $2K+1$ samples ($M=2K$):
   - Apply rectangular window → strong **Gibbs oscillations**.
4. Apply a smoother window $w[n]$ (Hamming, Hanning, Blackman…) to reduce sidelobes.

Window trade-off (from Li Tan table):

- Rectangular: narrowest transition, stopband $\approx -21$ dB.  
- Hamming: wider transition, stopband $\approx -53$ dB.  
- Blackman: even wider transition, stopband $\approx -75$ dB.

Rule-of-thumb for required $N_\text{taps}$ (for given transition width and stopband attenuation) is in the slides/tables and used when you design the AA filter in Exercise 1-C.

---

### 6.2 Parks–McClellan (remez) basics

Minimax / equiripple design for a linear-phase FIR:

- Weighted error:
  $$
  E(\omega) = W(\omega)\big(H_d(\omega) - A(\omega)\big),
  $$
  where $A(\omega)$ is the real amplitude of the linear-phase FIR and $H_d$ is the desired response.

- Piecewise constant weight:
  $$
  W(\omega) =
  \begin{cases}
  1/\delta_1, & \omega \text{ in passband},\\[2pt]
  1/\delta_2, & \omega \text{ in stopband},
  \end{cases}
  $$
  so that allowed ripples are $\delta_1$ (passband) and $\delta_2$ (stopband).

Empirical order estimate from the slide:

$$
M \approx \frac{-10\log_{10}(\delta_1\delta_2) - 13}{2.324(\omega_s - \omega_p)},
$$

where $\omega_p,\omega_s$ are pass-/stopband edges (rad).

---

### 6.3 Frequency sampling method & linear-phase types

#### Frequency sampling design (recap)

For an FIR filter with $M+1=2K+1$ taps (odd length):

1. **Normalized frequencies**:
   $$
   \omega_k = \frac{2\pi}{M+1}k,
   \quad k = 0,1,\dots,K.
   $$
2. **Sample desired response**:
   $$
   H[k] = H\big(e^{j\omega_k}\big).
   $$
3. **Compute impulse response coefficients** (slides formula):
   $$
   h[n] = \frac{1}{2K+1}
   \left(
   H[0] + 2\sum_{k=1}^{K} H[k]
   \cos\!\left(\frac{2\pi k (n-K)}{2K+1}\right)
   \right),\quad n = 0,1,\dots,K.
   $$
4. Impose **linear phase** by symmetry:
   $$
   h[n] = h[M-n],\quad n=0,1,\dots,K-1.
   $$

Illustrated example in slides:

- 25-tap LP FIR (linear phase) with $H_k$ patterns such as
  $[1\ 1\ 1\ 1\ 1\ 1\ 1\ 1\ 1\ 0\cdots]$ etc.  
- Sharper transitions (more abrupt $H_k$ pattern) ⇒ more Gibbs oscillations.

#### Linear-phase FIR types I–IV

With symmetry parameter $\varepsilon_\text{sym}$:

- Symmetric: $\varepsilon_\text{sym}=+1$, $h[n]=h[M-n]$  
- Anti-symmetric: $\varepsilon_\text{sym}=-1$, $h[n]=-h[M-n]$

Four types (slide table):

| Type | $\varepsilon_\text{sym}$ | $M$ (length $M+1$) | Notes / usable for |
|------|-------------------------|--------------------|--------------------|
| I    | $+1$ (sym.)             | even               | General LP/HP/BP/BS |
| II   | $+1$ (sym.)             | odd                | $H(\pi)=0$ ⇒ not HP/BS |
| III  | $-1$ (anti-sym.)        | even               | $H(0)=0$ ⇒ HP/BS/BP, not pure LP |
| IV   | $-1$ (anti-sym.)        | odd                | $H(0)=H(\pi)=0$ ⇒ special HP/BS |

Phase can be written as:

$$
H(\omega)=e^{-j\omega K} \sum_k \alpha_k\cos(k\omega)
\quad\text{or}\quad
H(\omega)=e^{-j\omega K} \sum_k \gamma_k\sin\big(\omega(k-\tfrac12)\big),
$$

depending on the type.

---

## 7. MATLAB patterns for multirate DSP

These follow the exercises in [[62743 E25 Digital Signal Processing Uge 12 Tirsdag.pdf]].

---

### 7.1 Down-sampling (decimation) by M

> [!code]- MATLAB — Time-domain decimation and spectrum
> ```matlab
> % Given: x (row vector), Fs, decimation factor M
> M      = 2;                % example
> xD     = x(1:M:end);       % keep every M'th sample
> Fs_new = Fs / M;
> 
> % Time vectors
> N      = numel(x);
> n      = 0:N-1;
> t      = n / Fs;
> 
> ND     = numel(xD);
> nD     = 0:ND-1;
> tD     = nD / Fs_new;
> 
> % Frequency response via FFT
> Nfft   = 2048;
> X      = fft(x,  Nfft);
> XD     = fft(xD, Nfft);
> f      = (0:Nfft-1) * (Fs     / Nfft);
> fD     = (0:Nfft-1) * (Fs_new / Nfft);
> 
> figure;
> subplot(2,1,1);
> plot(f,  abs(X));  grid on;
> xlabel('F [Hz]');  ylabel('|X(F)|');
> title('Original spectrum');
> 
> subplot(2,1,2);
> plot(fD, abs(XD)); grid on;
> xlabel('F [Hz]'); ylabel('|X_D(F)|');
> title(sprintf('Down-sampled spectrum (M = %d)', M));
> ```

---

### 7.2 Up-sampling (interpolation) by L

> [!code]- MATLAB — Zero-stuffing (expansion) by L
> ```matlab
> % Given: x (1xN), Fs, interpolation factor L
> L  = 3;                  % example
> N  = numel(x);
> 
> % Pre-allocate expanded signal with zeros
> xE = zeros(1, N * L);
> xE(1:L:end) = x;          % every L'th element is original sample
> 
> Fs_up = L * Fs;           % new sampling frequency
> nE    = 0:numel(xE)-1;
> tE    = nE / Fs_up;
> 
> figure;
> stem((0:N-1)/Fs, x, 'filled'); hold on;
> stem(tE, xE, 'r.'); grid on;
> legend('Original','Expanded (zeros)');
> xlabel('t [s]'); ylabel('Amplitude');
> title(sprintf('Up-sampling by L = %d (zero-stuffing)', L));
> ```

---

q### 7.3 Interpolation filter via Parks–McClellan (remez)

> [!code]- MATLAB — Interpolation filter design (Exercise 2-D style)
> ```matlab
> % Given: Fs, L, Fpass, Fstop, delta1, delta2, and order M
> L       = 3;
> Fs      = 16000;                 % example
> Fpass   = 3500;
> Fstop   = 4500;
> delta1  = 0.05;
> delta2  = 0.02;
> 
> % Normalized angular frequencies (radians)
> omega_pass = 2*pi*Fpass/Fs;
> omega_stop = 2*pi*Fstop/Fs;
> 
> % Normalized freq for remez (0..1)
> F  = [0 omega_pass omega_stop pi] / pi;
> Hd = [L L 0 0];                  % desired magnitude
> W  = [1/delta1 1/delta2];        % weights
> 
> M  = 60;                         % example order (adjust as needed)
> B  = remez(M, F, Hd, W);         % FIR interpolation filter
> 
> % Inspect frequency response
> Nfft = 4096;
> [H, w] = freqz(B, 1, Nfft);
> 
> figure;
> plot(w, abs(H), 'LineWidth', 1.5); grid on;
> xlabel('\omega [rad/sample]');
> ylabel('|H_I(\omega)|');
> title('Interpolation filter via Parks–McClellan');
> ```

---

### 7.4 Using the designed interpolation filter

> [!code]- MATLAB — Filtering the expanded signal and comparing spectra
> ```matlab
> % Assume xE is expanded signal (zeros inserted) and B is interpolation FIR
> y = filter(B, 1, xE);         % interpolated output
> 
> % Spectra before/after interpolation filter
> Nfft = 4096;
> XE   = fft(xE, Nfft);
> Y    = fft(y,  Nfft);
> fE   = (0:Nfft-1) * (Fs_up / Nfft);
> 
> figure;
> subplot(2,1,1);
> plot(fE, abs(XE)); grid on;
> xlabel('F [Hz]'); ylabel('|X_E(F)|');
> title('Spectrum of expanded (zero-stuffed) signal');
> 
> subplot(2,1,2);
> plot(fE, abs(Y)); grid on;
> xlabel('F [Hz]'); ylabel('|Y(F)|');
> title('Spectrum after interpolation filter');
> ```
