> Quick refs: [[Multirate Digital Signal Processing]]  
> Slides: [[62743 E25 Multirate Digital Signal Processing.pdf]]  
> Exercise sheet: [[62743 E25 Digital Signal Processing Uge 12 Tirsdag.pdf]]  
> Solution sheet: [[62743 E25 Digital Signal Processing Uge 12 Tirsdag solutions.pdf]]  
> Matlab document: [Open](<file:///C:/Users/Mads2/DTU/3.semester/DSP/UGE12/Tirsdag.mlx>)

---

# Week 12 — Multirate DSP (Decimation & Interpolation)

---

## 📘 Concept Overview

This week introduces **multirate signal processing**:

- **Decimation (down-sampling)** by factor $M$:
  - New sampling frequency: $F_s' = \dfrac{F_s}{M}$.
  - New Nyquist frequency: $F_{\max}' = \dfrac{F_s'}{2}$.
  - Discrete-time relation:
    $$
    x_D[n] = x[M n].
    $$
  - In frequency, the spectrum **compresses and replicates**, causing **aliasing** if energy exists above $F_{\max}'$.

- **Anti-aliasing (AA) low-pass filter** before decimation:
  - Passband: $0 \le F \le F_\text{pass}$ (must contain desired content).
  - Stopband: $F_\text{stop} \le F \le \dfrac{F_s}{2}$ with attenuation $A_s$.
  - Often designed as a **windowed ideal LP**:
    $$
    h_\text{LP,ideal}[n] =
    \begin{cases}
      \dfrac{\sin(\omega_c n)}{\pi n}, & n \neq 0 \\
      \dfrac{\omega_c}{\pi}, & n = 0
    \end{cases}
    $$
    then truncated with a chosen window (rectangular, Hamming, …).

- **Interpolation (up-sampling)** by factor $L$:
  - Insert $L-1$ zeros between samples:
    $$
    x_{\uparrow L}[n] =
    \begin{cases}
      x\!\left[\dfrac{n}{L}\right], & n = 0, \pm L, \pm 2L,\dots \\
      0, & \text{otherwise}.
    \end{cases}
    $$
  - New sampling frequency: $F_s^{(U)} = L F_s$.
  - The spectrum **expands** and creates **$L-1$ images**.

- **Interpolation filter** (reconstruction LP):
  - Removes the high-frequency images and compensates the gain by approximately $L$.
  - Designed here with **Parks–McClellan** (`firpm`) as an equiripple LP.

---

## Exercise 1 — Decimation by $M = 2$

The analog signal is
$$
x(t) = A_1 \cos(2\pi F_1 t) + A_2 \cos(2\pi F_2 t),
$$
with
- $A_1 = 5$, $F_1 = 1000~\text{Hz}$  
- $A_2 = 4$, $F_2 = 3500~\text{Hz}$  

and sampling parameters
- $F_s = 8000~\text{Hz}$  
- $N = 2^{14} = 16384$ samples.

We define
$$
T_s = \frac{1}{F_s}, \quad
n = 0,\dots,N-1,\quad
t_n = nT_s.
$$

The discrete-time signal is
$$
x[n] = x(t_n) = 5\cos(2\pi F_1 t_n) + 4\cos(2\pi F_2 t_n).
$$

---

# Exercise 1 — Sampling & Naive Down-sampling  
> Week 12 — Tuesday (Uge 12 Tirsdag)

---

## 1-A) Sampled signal and spectrum

> **Sub-questions:**  
> a) Calculate the sampled signal $x[n]$ and plot it vs. time.  
> b) Calculate and plot the spectrum $X(F)$ as a function of frequency.

We construct the discrete-time signal  
$$
x[n] = 5\cos(2\pi 1000\, nT_s) + 4\cos(2\pi 3500\, nT_s),
\qquad T_s = \frac{1}{8000}.
$$

### **Time-domain signal**

![[DSP_U12_Tirsdag_1A_time_signal.png]]

### **Two-sided magnitude spectrum**

Peaks appear at  
$\pm1000\,$Hz and $\pm3500\,$Hz.

![[DSP_U12_Tirsdag_1A_mag_spectrum_twosided.png]]

---
> [!code]- **MATLAB — Exercise 1-A**
> ```matlab
> % Common setup
> Fs  = 8000;              % Sampling frequency [Hz]
> N   = 2^14;              % Number of samples
> n   = 0:N-1;
> t   = n/Fs;              % Time axis [s]
> 
> A1 = 5;  F1 = 1000;      % Tone 1
> A2 = 4;  F2 = 3500;      % Tone 2
> 
> % Sampled signal
> x = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t);
> 
> % Time plot (first 5 ms)
> figure;
> plot(t*1e3, x, 'LineWidth', 1.0); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('x[n]');
> title('Exercise 1-A: Sampled signal x[n] at F_s = 8 kHz');
> 
> % === Two-sided FFT ===
> Nfft = N;
> X    = fft(x, Nfft);
> Xsh  = fftshift(X);
> Xmag = abs(Xsh)/Nfft;
> 
> df     = Fs/Nfft;
> f_2s   = (-Nfft/2:Nfft/2-1) * df;
> 
> figure;
> stem(f_2s, Xmag, 'filled'); grid on;
> xlabel('F [Hz]');
> ylabel('|X(F)|');
> title('Exercise 1-A: Magnitude spectrum (two-sided)');
> ```
---

### 1-B) Naive down-sampling by $M = 2$ (no AA filter)

> The sampled signal is now down-sampled with factor $M = 2$.  
> Sub-questions:  
> a) Find the new sampling frequency.  
> b) Calculate the Nyquist frequency $F_{\max}$ for the new sampling frequency.  
> c) Define the down-sampled time and frequency vectors.  
> d) Find the down-sampled signal from the sampled signal in Exercise 1-A.  
> e) Plot the down-sampled signal as a function of time.  
> f) Calculate and plot the spectrum of the down-sampled signal as a function of frequency.  
> g) Compare the spectrum to the spectrum found in 1-A and discuss observations.

---

#### a) New sampling frequency

Down-sampling halves the sampling rate:

$$
F_s' = \frac{F_s}{M} = \frac{8000}{2} = 4000~\text{Hz}.
$$

#### b) New Nyquist frequency

$$
F_{\max}' = \frac{F_s'}{2} = 2000~\text{Hz}.
$$

#### c) Down-sampled time and frequency vectors

Let the down-sampled signal $x_D[k]$ contain $N_D$ samples.

- Time vector:
  $$
  t'[k] = \frac{k}{F_s'},\quad k = 0,\dots,N_D-1.
  $$

- Frequency vector (one-sided):
  $$
  f'[m] = \frac{m}{N_D}F_s',\quad m = 0,\dots,\frac{N_D}{2}.
  $$

The frequency spacing changes, so we **cannot** simply down-sample the original frequency vector.

#### d) Down-sampled signal

Down-sampling keeps every second sample:

$$
x_D[k] = x[2k].
$$

#### e) Time-domain plot

![[DSP_U12_Tirsdag_1B_time_downsampled.png]]

#### f) Spectrum of $x_D[k]$

Two-sided magnitude spectrum:

![[DSP_U12_Tirsdag_1B_mag_downsampled_twosided.png]]

#### g) Comparison to Exercise 1-A

- The $1000$ Hz tone stays below the new Nyquist rate → no aliasing.  
- The $3500$ Hz tone violates the new Nyquist limit ($2000$ Hz):

$$
F_{\text{alias}} = |F_2 - F_s'| = |3500 - 4000| = 500~\text{Hz}.
$$

Thus, after down-sampling you observe components at **1000 Hz** and **500 Hz**, exactly matching the aliased spectrum from theory.

---

> [!code]- **MATLAB — Exercise 1-B (a–g)**
> ```matlab
> % Exercise 1-B: Naive down-sampling by M = 2 (no AA filter)
> M      = 2;            % Down-sampling factor
> Fs_D   = Fs/M;         % New sampling frequency [Hz]
> Fmax_D = Fs_D/2;       % New Nyquist frequency [Hz]
> 
> fprintf('Exercise 1-B:\n');
> fprintf('  M        = %d\n', M);
> fprintf('  Fs''      = %.0f Hz\n', Fs_D);
> fprintf('  Fmax''    = %.0f Hz\n\n', Fmax_D);
> 
> % Down-sampled signal x_D[k] = x[2k]
> xD = x(1:M:end);
> ND = numel(xD);
> kD = 0:ND-1;
> 
> % Time & frequency vectors
> tD      = kD / Fs_D;
> f_axisD = (-ND/2:ND/2-1) * (Fs_D/ND);   % two-sided frequency axis
> 
> % Plot time-domain signal
> figure;
> plot(tD*1e3, xD, 'LineWidth', 1.0); grid on;
> xlim([0 5]);
> xlabel('t'' [ms]');
> ylabel('x_D[k]');
> title('Exercise 1-B: Down-sampled signal x_D[k] (M = 2)');
> 
> % Two-sided FFT
> XD    = fft(xD, ND);
> XDsh  = fftshift(XD);
> XDmag = abs(XDsh)/ND;
> 
> figure;
> stem(f_axisD, XDmag, 'filled'); grid on;
> xlabel('F'' [Hz]');
> ylabel('|X_D(F'')|');
> title('Exercise 1-B: Two-sided magnitude spectrum (no AA filter)');
> xlim([-Fs_D/2 Fs_D/2]);
> ```

---

### 1-C) Design of anti-aliasing LP filter (Fourier-transform method)

> To avoid aliasing, design a digital AA low-pass filter with:  
> - Passband: $0$–$1855~\text{Hz}$  
> - Stopband: $2145$–$4000~\text{Hz}$  
> - Stopband attenuation: $A_s = 20~\text{dB}$  
>
> a) Determine passband and stopband frequencies.  
> b) Find the cut-off frequency.  
> c) Select a suitable window using the slide table.  
> d) Compute the minimum number of taps $N_\text{taps}$.  
> e) Compute $M$ and $K$.  
> f) Calculate and plot the **causal** impulse response.  
> g) Plot the magnitude response vs frequency.

---

### Passband & stopband

- Passband edge: $F_\text{pass} = 1855~\text{Hz}$  
- Stopband edge: $F_\text{stop} = 2145~\text{Hz}$  

These define the transition band width.

---

### Cut-off frequency

We choose the midpoint:

$$
F_c = \frac{F_\text{pass} + F_\text{stop}}{2}
= 2000~\text{Hz}.
$$

Digital (normalized) cutoff:

$$
\omega_c = 2\pi \frac{F_c}{F_s}.
$$

At the cutoff, the ideal LP magnitude is:

$$
|H(F_c)| = 0.5
\qquad\Longleftrightarrow\qquad
20\log_{10}(0.5) = -6.02~\text{dB}.
$$

This must be shown explicitly in the plots (matching the solution sheet).

---

### Window type

Required attenuation: $A_s = 20~\text{dB}$.

A **rectangular window** provides $\approx 21~\text{dB}$, therefore:

- Rectangular window is acceptable and minimal.

---

### Minimum number of taps

Rectangular-window design formula:

$$
N_\text{taps} \approx 
\left\lceil \frac{0.9}{\Delta F_\text{sharp}} \right\rceil,
\qquad
\Delta F_\text{sharp}
= \frac{F_\text{stop}-F_\text{pass}}{F_s}
= \frac{2145-1855}{8000}
= 0.03625.
$$

Thus:

$$
N_\text{taps} 
= \left\lceil \frac{0.9}{0.03625} \right\rceil
= 25.
$$

We enforce an odd number of taps:

- $N_\text{taps,AA} = 25$  
- Filter order: $M_\text{AA} = 24$  
- Symmetry index: $K_\text{AA} = M_\text{AA}/2 = 12$

---

### Impulse response (causal)

The FIR coefficients are the truncated ideal LP:

$$
h_\text{AA}[n]
= \frac{\omega_c}{\pi}\,
\text sinc\!\left(\frac{\omega_c}{\pi}(n-K_\text{AA})\right),
\qquad n = 0,\dots,M_\text{AA},
$$

where

$$
\text sinc(x) = \frac{\sin(\pi x)}{\pi x}.
$$

Impulse response:

![[DSP_U12_Tirsdag_1C_AA_impulse.png]]

---

### Magnitude response

Cutoff $F_c = 2000~\text{Hz}$ is explicitly marked with a **magenta dashed line**  


![[DSP_U12_Tirsdag_1C_AA_mag.png]]

### Log-magnitude response

Stopband attenuation ($20~\text{dB}$), passband ripple, and cutoff are shown:

![[DSP_U12_Tirsdag_1C_AA_logmag.png]]

---

> [!code]- MATLAB (1-C)
> ```matlab
> % AA filter specs
> Fpass_AA = 1855;     % Passband [Hz]
> Fstop_AA = 2145;     % Stopband [Hz]
> AsdB_AA  = 20;       % Minimum stopband attenuation [dB]
> 
> % --- Window length (rectangular) ---
> DeltaF_sharp = (Fstop_AA - Fpass_AA)/Fs;
> Ntaps_AA = ceil(0.9 / DeltaF_sharp);      % from slides
> if mod(Ntaps_AA, 2) == 0
>     Ntaps_AA = Ntaps_AA + 1;              % enforce odd length
> end
> M_AA = Ntaps_AA - 1;
> K_AA = M_AA/2;
> 
> % --- Cutoff ---
> Fc_AA = 0.5*(Fpass_AA + Fstop_AA);        % 2000 Hz
> wc_AA = 2*pi*Fc_AA/Fs;
> 
> % --- Impulse response ---
> nA          = 0:M_AA;
> nA_centered = nA - K_AA;
> hAA_centered = (wc_AA/pi) * sinc((wc_AA/pi)*nA_centered);
> b_AA         = hAA_centered;
> 
> % --- Impulse plot ---
> figure;
> stem(nA, b_AA, 'filled'); grid on;
> xlabel('n'); ylabel('h_{AA}[n]');
> title(sprintf('Anti-alias LP FIR: N_{taps} = %d', Ntaps_AA));
> 
> % --- Frequency response ---
> [H_AA, w_AA] = freqz(b_AA, 1, Nfft);
> F_AA = w_AA * Fs / (2*pi);
> 
> % Linear magnitude with cutoff
> Fc_lin = Fc_AA;
> figure;
> plot(F_AA, abs(H_AA), 'LineWidth',1); hold on; grid on;
> xline(Fpass_AA,'--g','F_{pass}');
> xline(Fstop_AA,'--r','F_{stop}');
> xline(Fc_lin,'--k','F_c');
> yline(0.5,'--k');                     % |H(Fc)| = 0.5
> xlabel('F [Hz]'); ylabel('|H_{AA}(F)|');
> title('Anti-alias LP (rectangular window) — Magnitude response');
> 
> % Log magnitude with dB cutoff -6.02 dB
> HdB_AA = 20*log10(abs(H_AA)+eps);
> Fc_dB = 20*log10(0.5);                % -6.02 dB
> 
> figure;
> plot(F_AA, HdB_AA,'LineWidth',1); hold on; grid on;
> xline(Fpass_AA,'--g','F_{pass}');
> xline(Fstop_AA,'--r','F_{stop}');
> xline(Fc_AA,'--k','F_c');
> yline(Fc_dB,'--k');                   % cutoff amplitude
> yline(-AsdB_AA,':b','-A_s');          % stopband requirement
> xlabel('F [Hz]'); ylabel('H_{AA,dB}(F) [dB]');
> title('Anti-alias LP (rectangular window) — Log magnitude');
> ```

---
### 1-D) Filtering with AA filter (no down-sampling yet)

> To avoid frequency aliasing after subsequent down-sampling, the sampled signal from 1-A is first filtered using the designed AA-filter.  
>
> Sub-questions:  
> a) Filter the sampled signal from 1-A using `filter`.  
> b) Plot the filtered signal as a function of time.  
> c) Calculate and plot the spectrum of the filtered signal as a function of frequency.  
> d) Compare the spectrum to the spectrum found in 1-A and discuss observations.

We start from the sampled signal in 1-A:

- Sampling frequency: $F_s = 8000\ \text{Hz}$  
- Two tones: $F_1 = 1000\ \text{Hz}$ and $F_2 = 3500\ \text{Hz}$  

From 1-C we designed an **anti-aliasing lowpass** with:

- Passband: $0 \le F \le F_\text{pass} = 1855\ \text{Hz}$  
- Stopband: $F \ge F_\text{stop} = 2145\ \text{Hz}$  
- Cutoff (design choice, middle of transition band):
  $$
  F_c = F_{c,\text{AA}} = \frac{F_\text{pass} + F_\text{stop}}{2}
      = 2000\ \text{Hz}.
  $$

The filter is a linear-phase FIR with coefficients $h_\text{AA}[n] = b_\text{AA}[n]$ obtained by truncating the ideal LP and applying a rectangular window.

---

#### a) Filter the sampled signal

Filtering in discrete time is convolution:

$$
x_f[n] = (h_\text{AA} * x)[n]
       = \sum_{k=-\infty}^{\infty} h_\text{AA}[k]\;x[n-k].
$$

In MATLAB we implement this as

- Numerator (FIR taps): `b_AA`  
- Denominator: `1` (no IIR feedback)

so the filtered signal is:

- $x_f[n] =$ `filter(b_AA, 1, x)`  

---

#### b) Time-domain plot of the filtered signal

Time-domain result (first $5\ \text{ms}$):

![[DSP_U12_Tirsdag_1D_time_filtered.png]]

Observations:

- The waveform is now **smooth and almost purely sinusoidal**.  
- You basically see the $1\ \text{kHz}$ tone, with a short transient at the beginning (filter startup + finite FIR length).  
- The high-frequency “wiggles” from the $3.5\ \text{kHz}$ tone are gone — our AA filter did its job.

---

#### c) Spectrum of the filtered signal

We compute the FFT of $x_f[n]$ and plot the **one-sided magnitude** $|X_f(F)|$:

$$
X_f[k] = \sum_{n=0}^{N-1} x_f[n]\;e^{-j2\pi kn/N},
\qquad
F_k = \frac{k}{N}F_s.
$$

Resulting magnitude spectrum:

![[DSP_U12_Tirsdag_1D_mag_filtered.png]]

Observations from the spectrum:

- There is a **single strong line at $F_1 = 1000\ \text{Hz}$**.  
- Around $F_2 = 3500\ \text{Hz}$ the magnitude is **very close to zero**, i.e. the high-frequency component is heavily attenuated (well beyond the required $20\ \text{dB}$ stopband attenuation).  
- Passband ripple around $1\ \text{kHz}$ is small and acceptable for this design.

---

#### d) Comparison with 1-A

In 1-A:

- The magnitude spectrum had **two distinct lines**, at $1000\ \text{Hz}$ and $3500\ \text{Hz}$.  
- The higher tone $F_2 = 3500\ \text{Hz}$ lies **above** the Nyquist frequency of the *future* down-sampled system ($F_s' = 4000\ \text{Hz} \Rightarrow F_{\max}' = 2000\ \text{Hz}$), so it would alias if we decimated directly.

After applying the AA filter (1-D):

- Only the $1000\ \text{Hz}$ tone remains in-band.  
- The spectrum now satisfies the **non-aliasing condition** for down-sampling by $M = 2$:
  $$
  F_\text{max,remaining} \le \frac{F_s}{2M} = \frac{8000}{4} = 2000\ \text{Hz}.
  $$
- This prepares the signal for safe decimation in 1-E.

So: 1-D “cleans” the spectrum such that the future down-sampling will not fold unwanted energy into the passband.  

---

> [!code]- MATLAB — Reusable snippet for Exercise 1-D
> ```matlab
> % --- Inputs ---
> % x      : sampled signal from Exercise 1-A
> % Fs     : sampling frequency [Hz] (here 8000 Hz)
> % b_AA   : AA FIR coefficients from Exercise 1-C
> % Fc_AA  : chosen cutoff frequency [Hz] (e.g. 2000 Hz)
> % imgDir : folder for saving plots
> 
> % === Exercise 1-D: Filter x[n] with AA-filter ===
> 
> % a) Filter the sampled signal
> x_filt = filter(b_AA, 1, x);
> 
> % b) Time-domain plot (first 5 ms)
> N  = numel(x_filt);
> t  = (0:N-1)/Fs;
> 
> figure;
> plot(t*1e3, x_filt, 'LineWidth', 1.0); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('x_f[n]');
> title('Exercise 1-D: AA-filtered signal x_f[n]');
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_U12_Tirsdag_1D_time_filtered.png'), 'Resolution', 300);
> 
> % c) Spectrum of the filtered signal
> Nf         = N;
> Xf         = fft(x_filt, Nf);
> Xf_mag     = abs(Xf)/Nf;
> F_axis_f   = (0:Nf-1)*Fs/Nf;
> F_pos_f    = F_axis_f(1:Nf/2+1);
> Xf_mag_pos = 2*Xf_mag(1:Nf/2+1);
> 
> figure;
> plot(F_pos_f, Xf_mag_pos, 'LineWidth', 1.0); grid on; hold on;
> xline(Fc_AA, ':k', 'F_c');
> xline(Fs/2, ':k', 'F_s/2');
> xlabel('F [Hz]');
> ylabel('|X_f(F)|');
> title('Exercise 1-D: Magnitude spectrum of AA-filtered signal');
> xlim([0 Fs/2]);
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_U12_Tirsdag_1D_mag_filtered.png'), 'Resolution', 300);
> 
> % d) To discuss: compare these plots with Exercise 1-A:
> %    - 1 kHz tone preserved
> %    - 3.5 kHz tone removed
> ```


---

### 1-E) Down-sampling after AA filtering ($M = 2$)

> After the AA-filter has been applied it is now once again attempted to down-sample the signal.  
>
> Sub-questions:  
> a) Down-sample the filtered sampled signal from exercise 1-D.  
> b) Plot the down-sampled and filtered signal as a function of time.  
> c) Plot the spectrum of the down-sampled and filtered signal as a function of frequency.  
> d) Compare the spectrum to the spectrum found in 1-B and discuss observations.

We now decimate the **already filtered** signal by $M = 2$.

---

#### a) Down-sample the filtered signal from 1-D

Down-sampling by $M = 2$:

- New sampling frequency:
  $$
  F_s' = \frac{F_s}{M}
       = \frac{8000}{2}
       = 4000\ \text{Hz}.
  $$
- New Nyquist frequency:
  $$
  F_{\max}' = \frac{F_s'}{2} = 2000\ \text{Hz}.
  $$
- Discrete-time relation:
  $$
  x_{D,\text{AA}}[k] = x_f[2k],\quad k = 0,1,\dots
  $$

MATLAB implementation:

```matlab
xD_AA = x_filt(1:M:end);
```

---

#### b) Time-domain plot of $x_{D,\text{AA}}[k]$

We plot $x_{D,\text{AA}}[k]$ versus the **new** time variable

$$
t'_k = \frac{k}{F_s'} = \frac{k}{4000} \ \text{s}.
$$

Time-domain result:

![[DSP_U12_Tirsdag_1E_time_downsampled_AA.png]]

Observations:

- The waveform still looks like a **clean 1 kHz sinusoid**.  
- Sampling is sparser in time (since $F_s'$ is halved), but the signal shape is preserved.  
- There are no strange envelopes or beat patterns, indicating that aliasing has been avoided.

For comparison, the time plot from 1-B (naive down-sampling) showed a much more distorted-looking waveform, because the aliased 3.5 kHz component folded into the baseband.

---

#### c) Spectrum of the down-sampled, filtered signal

We compute the FFT of $x_{D,\text{AA}}[k]$ using the new sampling frequency $F_s'$ to build the frequency axis $F'$:

$$
F'_k = \frac{k}{N_D}F_s',\quad 0 \le F'_k \le F_s',
$$

where $N_D$ is the number of down-sampled samples.

Resulting spectrum:

![[DSP_U12_Tirsdag_1E_mag_downsampled_AA.png]]

Observations:

- There is a **single line at $F_1' = 1000\ \text{Hz}$**, safely inside the new Nyquist interval $[0, 2000]$.  
- No additional component appears at other frequencies; in particular, there is **no alias component** around
  $$
  F_\text{alias} = |F_2 - F_s'|
                  = |3500 - 4000|
                  = 500\ \text{Hz},
  $$
  which is what showed up in the naive 1-B case.

---

#### d) Comparison to 1-B (naive down-sampling, no AA filter)

Now we compare:

- 1-B: down-sampling **without** AA filter.  
- 1-E: down-sampling **after** AA filtering.

Spectral comparison (your `DSP_U12_Tirsdag_1E_downsample_compare.png`):

![[DSP_U12_Tirsdag_1E_downsample_compare.png]]

- **Blue curve (naive)**: has a strong line at $\approx 500\ \text{Hz}$ — this is the **aliased version** of the 3.5 kHz tone. It appears because 3500 Hz is above $F_{\max}' = 2000\ \text{Hz}$, so it folds back:
  $$
  F_\text{alias} = F_s' - F_2 = 500\ \text{Hz}.
  $$
- **Orange curve (with AA filter)**: only the 1000 Hz component remains; the alias at 500 Hz is practically gone.

Time-domain comparison (your `DSP_U12_Tirsdag_1E_time_compare.png`):

![[DSP_U12_Tirsdag_1E_time_compare.png]]

- **Blue (no AA)**: waveform looks “beaty” and more distorted — it is a combination of the 1 kHz tone and the 500 Hz alias.  
- **Orange (with AA)**: waveform is close to a single sinusoid at 1 kHz, just sampled at the lower rate.

**Conclusion for 1-E:**

- The AA filter successfully removed the problematic 3.5 kHz component **before** decimation.  
- After down-sampling, the signal’s spectrum matches what we want: a single tone at 1 kHz with no aliasing artifacts.  
- Comparing 1-B and 1-E clearly illustrates the **purpose of AA filtering** in a decimation system.

---

> [!code]- MATLAB — Reusable snippet for Exercise 1-E
> ```matlab
> % --- Inputs ---
> % x_filt : AA-filtered signal from Exercise 1-D
> % Fs     : original sampling frequency [Hz] (8000 Hz)
> % M      : down-sampling factor (here 2)
> % xD, tD, fD_pos, XDmag_pos from 1-B for comparison (optional)
> % imgDir : folder for saving plots
> 
> % === Exercise 1-E: Down-sample the AA-filtered signal ===
> 
> M      = 2;
> Fs_D   = Fs / M;          % new sampling frequency [Hz]
> Fmax_D = Fs_D / 2;        % new Nyquist frequency [Hz]
> 
> fprintf('Exercise 1-E (after AA filter):\n');
> fprintf('  Down-sampling factor M = %d\n', M);
> fprintf('  New sampling rate F_s'' = %.0f Hz\n', Fs_D);
> fprintf('  New Nyquist frequency F_max'' = %.0f Hz\n\n', Fmax_D);
> 
> % a) Down-sample AA-filtered signal
> xD_AA = x_filt(1:M:end);
> ND_AA = numel(xD_AA);
> kD_AA = 0:ND_AA-1;
> tD_AA = kD_AA / Fs_D;
> 
> % b) Time-domain plot
> figure;
> plot(tD_AA*1e3, xD_AA, 'LineWidth', 1.0); grid on;
> xlim([0 5]);
> xlabel('t'' [ms]');
> ylabel('x_{D,AA}[k]');
> title('Exercise 1-E: Down-sampled AA-filtered signal (M = 2)');
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_U12_Tirsdag_1E_time_downsampled_AA.png'), 'Resolution', 300);
> 
> % c) Spectrum of down-sampled, filtered signal
> XD_AA      = fft(xD_AA, ND_AA);
> XD_AA_mag  = abs(XD_AA)/ND_AA;
> f_axisD_AA = (0:ND_AA-1)*Fs_D/ND_AA;
> fD_AA_pos  = f_axisD_AA(1:ND_AA/2+1);
> XD_AA_pos  = 2*XD_AA_mag(1:ND_AA/2+1);
> 
> figure;
> plot(fD_AA_pos, XD_AA_pos, 'LineWidth', 1.0); grid on; hold on;
> xline(Fmax_D, ':k', 'F_{max}''');
> xlabel('F'' [Hz]');
> ylabel('|X_{D,AA}(F'')|');
> title('Exercise 1-E: Magnitude spectrum after AA-filter + down-sampling');
> xlim([0 Fs_D/2]);
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_U12_Tirsdag_1E_mag_downsampled_AA.png'), 'Resolution', 300);
> 
> % d) Optional comparison with naive 1-B result (if xD, fD_pos, XDmag_pos exist)
> figure;
> plot(fD_pos, XDmag_pos, 'LineWidth', 1.0); hold on;
> plot(fD_AA_pos, XD_AA_pos, 'LineWidth', 1.0);
> grid on;
> xlabel('F'' [Hz]');
> ylabel('|X_D(F'')|');
> title('Down-sampling: without vs with AA-filter');
> legend('Naive (no AA filter)', 'With AA filter', 'Location', 'best');
> xlim([0 Fs_D/2]);
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_U12_Tirsdag_1E_downsample_compare.png'), 'Resolution', 300);
> 
> % Time-domain comparison (also optional)
> figure;
> plot(tD*1e3,   xD,    'LineWidth', 1.0); hold on;
> plot(tD_AA*1e3, xD_AA, 'LineWidth', 1.0);
> grid on;
> xlabel('t'' [ms]');
> ylabel('Amplitude');
> title('x_D[n]: before vs after AA-filtering');
> legend('No AA filter','With AA filter','Location','best');
> xlim([0 5]);
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_U12_Tirsdag_1E_time_compare.png'), 'Resolution', 300);
> ```

---

## Exercise 2 — Interpolation by $L = 3$

Now we consider **up-sampling** the same signal.

- Interpolation factor: $L = 3$  
- New sampling rate:
  $$
  F_s^{(U)} = L F_s = 3 \cdot 8000 = 24000~\text{Hz}.
  $$

---

# Exercise 2-A — Sampling the analog signal

> Given  
> The analog signal  
> $$
> x(t) = A_1\cos(2\pi F_1 t) + A_2\cos(2\pi F_2 t)
> $$
> with  
> • $A_1 = 5$, $A_2 = 4$  
> • $F_1 = 1000~\text{Hz}$  
> • $F_2 = 3500~\text{Hz}$  
>
> Sampling parameters:  
> • $F_s = 8000~\text{Hz}$  
> • $N = 2^{14} = 16384$  
>
> Sub-questions:  
> **a)** Calculate the sampled signal $x[n]$ and plot it vs. time.  
> **b)** Calculate and plot the **two-sided** magnitude spectrum.

---

## a) Sampled signal

The discrete-time signal is  
$$
x[n] = 5\cos(2\pi 1000\,nT_s) + 4\cos(2\pi 3500\,nT_s),
\qquad T_s = \frac{1}{8000}.
$$

Time-domain plot (first 5 ms):

![[DSP_U12_Tirsdag_1A_time_signal.png]]

---

## b) TWO-SIDED magnitude spectrum

We take the FFT, apply `fftshift`, and stem-plot the full spectrum  
$$
F \in [-F_s/2,\; F_s/2].
$$

Expected peaks at  
$\{-3500,\,-1000,\,+1000,\,+3500\}\,$Hz.

![[DSP_U12_Tirsdag_1A_mag_spectrum_twosided.png]]

---

## MATLAB — Exercise 2-A
> [!code]- **MATLAB (2-A)**
> ```matlab
> % Setup
> Fs  = 8000;
> N   = 2^14;
> n   = 0:N-1;
> t   = n/Fs;
> 
> A1 = 5;  F1 = 1000;
> A2 = 4;  F2 = 3500;
> 
> % Sampled signal
> x = A1*cos(2*pi*F1*t) + A2*cos(2*pi*F2*t);
> 
> % Time plot (first 5 ms)
> figure;
> plot(t*1e3, x, 'LineWidth', 1.0); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('x[n]');
> title('Exercise 2-A: Sampled signal');
> 
> % ======== TWO-SIDED FFT ========
> X      = fft(x, N);
> Xsh    = fftshift(X);
> Xmag   = abs(Xsh)/N;
> 
> df     = Fs/N;
> f_axis = (-N/2:N/2-1)*df;
> 
> figure;
> stem(f_axis, Xmag, 'filled'); grid on; hold on;
> 
> % Optional: add markers (not lines) for F1 and F2
> % (Requires exact index match—commented out in case matching fails)
> % plot(F1,  Xmag(f_axis==F1),  'ro', 'MarkerSize', 8, 'LineWidth', 2);
> 
> xlabel('F [Hz]');
> ylabel('|X(F)|');
> title('Exercise 2-A: TWO-SIDED magnitude spectrum');
> xlim([-4000 4000]);
> ```

---

# Exercise 2-B — Interpolation by factor $L=3$

> Interpolation factor: $L = 3$  
>
> Sub-questions:  
> **a)** Find the new sampling frequency.  
> **b)** Define the up-sampled time vector.  
> **c)** Form the interpolated (zero-stuffed) signal.  
> **d)** Plot the interpolated signal.  
> **e)** Plot the **two-sided** spectrum of the up-sampled signal.

---

## a) New sampling frequency

$$
F_s^{(U)} = L F_s = 3 \cdot 8000 = 24000~\text{Hz}.
$$

---

## b) Up-sampled time vector

For $N_U = LN$ samples:

$$
t^{(U)}[m] = \frac{m}{F_s^{(U)}}, \quad 0 \le m < N_U.
$$

---

## c) Zero-stuffed interpolated signal

Zero-stuffing rule:

$$
x_U[m] =
\begin{cases}
x[n], & m = nL,\\[4pt]
0, & \text{otherwise}.
\end{cases}
$$

---

## d) Time-domain plot

![[DSP_U12_Tirsdag_2A_upsampled_time.png]]

---

## e) TWO-SIDED spectrum (shows $L-1 = 2$ spectral images)

![[DSP_U12_Tirsdag_2A_upsampled_spectrum.png]]

---

## MATLAB — Exercise 2-B
> [!code]- **MATLAB (2-B)**
> ```matlab
> L    = 3;               % interpolation factor
> Fs_U = L*Fs;            % new sampling rate
> N_U  = L*N;             % new number of samples
> 
> fprintf('\nExercise 2-B:\n');
> fprintf('  New sampling rate = %.0f Hz\n', Fs_U);
> 
> % --------- Zero-stuffing ---------
> xU = zeros(1, N_U);
> xU(1:L:end) = x;
> 
> nU = 0:N_U-1;
> tU = nU/Fs_U;
> 
> % Time plot
> figure;
> stem(tU*1e3, xU, 'filled'); grid on;
> xlim([0 5]);
> xlabel('t^{(U)} [ms]');
> ylabel('x_U[m]');
> title('Exercise 2-B: Zero-stuffed signal');
> 
> % --------- TWO-SIDED FFT ---------
> XU    = fft(xU, N_U);
> XUsh  = fftshift(XU);
> XUmag = abs(XUsh)/N_U;
> 
> df_U  = Fs_U/N_U;
> fU_2s = (-N_U/2:N_U/2-1)*df_U;
> 
> figure;
> stem(fU_2s, XUmag, 'filled'); grid on;
> xlabel('F^{(U)} [Hz]');
> ylabel('|X_U(F^{(U)})|');
> title('Exercise 2-B: TWO-SIDED spectrum of zero-stuffed signal');
> xlim([-12000 12000]);   % shows all 3 images
> ```

---

## 2-C) Spectrum of the interpolated signal

In this exercise the **interpolated signal** (created in 2-B via zero-stuffing with $L = 3$) is examined in the frequency domain.

This exercise consists of:

a) Define the up-sampled frequency vector.  
b) Calculate and plot the spectrum of the interpolated signal.  
c) Compare the spectrum to the spectrum previously found in 2-A and discuss the observations.

---

### a) Up-sampled frequency vector

After up-sampling by factor $L = 3$, the new sampling frequency is

$$
F_s^{(U)} = L F_s = 3 \cdot 8000 = 24000~\text{Hz}.
$$

Let the interpolated (zero-stuffed) signal have length $N_U = L N$.  
For an $N_U$-point FFT we use a **two-sided** frequency vector

$$
f^{(U)}[k]
=
\left(k - \frac{N_U}{2}\right)\frac{F_s^{(U)}}{N_U},
\qquad k = 0,1,\dots,N_U-1.
$$

This spans

$$
-\frac{F_s^{(U)}}{2} \le f \le \frac{F_s^{(U)}}{2}
= \pm 12000~\text{Hz}.
$$

---

### b) Spectrum of the interpolated signal

The zero-stuffed sequence is

$$
x_U[m] =
\begin{cases}
x[n], & m = nL, \\
0, & \text{otherwise}.
\end{cases}
$$

Its two-sided FFT magnitude is shown below:

![[DSP_U12_Tirsdag_2C_interp_spectrum.png]]

This plot is obtained from the MATLAB code at the end of this section, using `fft`, `fftshift`, and a stem plot over the two-sided frequency axis $f^{(U)}$.

---

### c) Comparison with the spectrum from 2-A

From Exercise 2-A, the original sampled signal had tones at

- $1000~\text{Hz}$  
- $3500~\text{Hz}$

At the **original** sampling rate $F_s = 8000~\text{Hz}$ these appeared as two lines in the baseband spectrum.

After interpolation (zero-stuffing) to $F_s^{(U)} = 24000~\text{Hz}$ we observe in the figure:

1. The **original components** at $1000$ Hz and $3500$ Hz remain with the same amplitudes.
2. New **spectral images** appear, which are scaled copies of the original spectrum shifted inside the enlarged Nyquist interval $\left[-F_s^{(U)}/2,\,F_s^{(U)}/2\right]$.
3. In general, interpolation by zero-stuffing causes
   $$
   X_U(e^{j\omega}) = X(e^{j\omega L}),
   $$
   which compresses the baseband spectrum by $L$ and creates $L-1$ additional images.

So compared to 2-A, the number of visible frequency components inside the Nyquist interval has increased (due to the images), but the amplitudes of the **original** tones are unchanged. This is exactly why a **subsequent interpolation LP filter** is needed in later sub-questions: to remove the images and recover a “clean” band-limited, up-sampled signal.

---

> [!code]- MATLAB — Exercise 2-C (two-sided spectrum of interpolated signal)
> ```matlab
> %% Exercise 2-C: Spectrum of the interpolated (zero-stuffed) signal
> % Assumes from 2-A/2-B:
> %   L      = 3;
> %   Fs     = 8000;
> %   xU     = zero-stuffed sequence (length N_U = L*N);
> %   imgDir = folder for saving figures
> 
> Fs_U    = L * Fs;          % Up-sampled sampling frequency [Hz]
> N_U     = numel(xU);       % Number of samples after up-sampling
> Nfft_U  = N_U;             % FFT length (can also choose a power of 2)
> 
> fprintf('Exercise 2-C:\n');
> fprintf('  F_s^{(U)} = %.0f Hz, N_U = %d\n', Fs_U, N_U);
> 
> % ---------- Two-sided FFT of interpolated signal ----------
> XU      = fft(xU, Nfft_U);          % FFT
> XU_sh   = fftshift(XU);             % shift DC to 0 Hz (center)
> XU_mag2 = abs(XU_sh)/Nfft_U;        % magnitude, scaled by Nfft_U
> 
> % Two-sided frequency axis: [-F_s^{(U)}/2 .. F_s^{(U)}/2 - ΔF]
> df_U  = Fs_U / Nfft_U;
> fU_2s = (-Nfft_U/2 : Nfft_U/2-1) * df_U;
> 
> % ---------- Plot spectrum ----------
> figure;
> stem(fU_2s, XU_mag2, 'LineWidth', 1.0); grid on;
> xlabel('F^{(U)} [Hz]');
> ylabel('|X_U(F^{(U)})|');
> title('Exercise 2-C: Spectrum of interpolated (zero-stuffed) signal');
> xlim([-Fs_U/2 Fs_U/2]);   % = [-12000 12000] Hz for F_s^{(U)} = 24 kHz
> 
> exportgraphics(gcf, fullfile(imgDir, ...
>     'DSP_U12_Tirsdag_2C_interp_spectrum.png'), 'Resolution', 300);
> ```

---

## 2-D) Interpolation LP design using `firpm` (Parks–McClellan)

This exercise consists of the following sub-questions:

a) Find the normalized angular passband and stopband frequencies.  
b) Estimate the required filter order \(M\).  
c) Design the filter using the Parks–McClellan algorithm.  
d) Plot the magnitude response together with the filter requirements.  
e) Check if the designed filter satisfies the requirements.  
f) If not, increase \(M\) (in steps of 5).  
g) Plot the magnitude response of a filter whose order **does** satisfy the specs.  
h) Plot the impulse response of the final interpolation filter.

---

### **Given specifications**

- Passband edge: $F_\text{pass} = 3500~\text{Hz}$
- Stopband edge: $F_\text{stop} = 4500~\text{Hz}$
- Passband ripple: $\delta_1 = 0.05$  
- Stopband ripple: $\delta_2 = 0.02$  
- Interpolation factor: $L = 3$  
- Upsampled sampling frequency:  
  $$
  F_s^{(U)} = L F_s = 3\cdot 8000 = 24000~\text{Hz}
  $$

---

### **a) Normalized angular frequencies**

$$
\omega_p = 2\pi \frac{F_\text{pass}}{F_s^{(U)}} 
= 2\pi\frac{3500}{24000}
$$

$$
\omega_s = 2\pi \frac{F_\text{stop}}{F_s^{(U)}} 
= 2\pi\frac{4500}{24000}
$$

Transition width:
$$
\Delta\omega = \omega_s - \omega_p
$$

---

### **b) Order estimate $M_\text{est}$**

Worst-case ripple:
$$
\delta = \min(\delta_1, \delta_2) = 0.02
$$

Equivalent attenuation:
$$
A_\text{dB} = -20\log_{10}(\delta)
$$

Oppenheim–Hamming estimate:
$$
M_\text{est} \approx 
\left\lceil
\frac{A_\text{dB}-7.95}{2.285\Delta\omega}
\right\rceil
$$

We enforce **even $M$** so that $N_\text{taps}=M+1$ is odd (Type-I linear phase).

---

### **c–g) Filter design and verification using two trial orders**

We try:

- **Trial 1:** \(M = 28\) → *too low*  
- **Trial 2:** \(M = 47\) → *meets specs*



#### **Trial M = 28 (fails)**

![[DSP_U12_Tirsdag_2B_interp_filter_M28.png]]

#### **Trial M = 47 (passes)**

![[DSP_U12_Tirsdag_2B_interp_filter_M47.png]]

---

### **h) Impulse response of the final interpolation filter**

![[DSP_U12_Tirsdag_2B_interp_impulse_M47.png]]

---

> [!code]- **MATLAB — Exercise 2-D (full design, verification & impulse response)**
> ```matlab
> %% Exercise 2-D (a–b): Interpolation LP specs & order estimate (Parks–McClellan)
> Fpass_I = 3500;
> Fstop_I = 4500;
> delta1  = 0.05;
> delta2  = 0.02;
> 
> omega_p = 2*pi*Fpass_I/Fs_U;
> omega_s = 2*pi*Fstop_I/Fs_U;
> Delta_w = omega_s - omega_p;
> 
> delta = min(delta1, delta2);
> A_dB = -20*log10(delta);
> 
> M_est = ceil((A_dB - 7.95)/(2.285*Delta_w));
> if mod(M_est,2) ~= 0
>     M_est = M_est + 1;
> end
> Ntaps_I = M_est + 1;
> 
> fprintf('Estimated M ≈ %d (N taps = %d)\n', M_est, Ntaps_I);
> 
> % Normalized frequencies for firpm
> F_Nyq_U     = Fs_U/2;
> Fpass_normI = Fpass_I / F_Nyq_U;
> Fstop_normI = Fstop_I / F_Nyq_U;
> f_firpm = [0 Fpass_normI Fstop_normI 1];
> a_firpm = [L L 0 0];
> w_firpm = [1/delta1 1/delta2];
> 
> ymin_lin = 0;
> ymax_lin = L + delta1 + 0.5;
> 
> %% ---- Trial 1: M = 28 (fails) ----
> M_trial1 = 28;
> b_I_28 = firpm(M_trial1, f_firpm, a_firpm, w_firpm);
> [H_28, w_28] = freqz(b_I_28, 1, Nfft_U);
> figure;
> plot(w_28, abs(H_28), 'LineWidth', 1.0); grid on; hold on;
> xline(omega_p,'--k'); xline(omega_s,'--k');
> yline(L+delta1,'--k'); yline(L-delta1,'--k');
> xlabel('Normalized angular frequency, \omega');
> ylabel('Attenuation [a.u.]');
> title('Interpolation LP, M = 28 (does NOT meet specs)');
> ylim([ymin_lin ymax_lin]);
> 
> %% ---- Trial 2: M = 47 (passes) ----
> M_trial2 = 47;
> b_I_47 = firpm(M_trial2, f_firpm, a_firpm, w_firpm);
> [H_47, w_47] = freqz(b_I_47, 1, Nfft_U);
> figure;
> plot(w_47, abs(H_47), 'LineWidth', 1.0); grid on; hold on;
> xline(omega_p,'--k'); xline(omega_s,'--k');
> yline(L+delta1,'--k'); yline(L-delta1,'--k');
> xlabel('Normalized angular frequency, \omega');
> ylabel('Attenuation [a.u.]');
> title('Interpolation LP, M = 47 (meets specs)');
> ylim([ymin_lin ymax_lin]);
> 
> %% ---- Impulse response for final filter (M = 47) ----
> figure;
> stem(0:M_trial2, b_I_47, 'filled'); grid on;
> xlabel('n'); ylabel('h_I[n]');
> title('Impulse response of interpolation filter (M = 47)');
> ```

---

### 2-E) Filtering the up-sampled signal

> Use the interpolation filter to filter the interpolated (zero-stuffed) signal and examine the spectrum.

After filtering:
- Spectral images are suppressed.  
- The baseband region resembles the original spectrum, but at the higher sampling rate $F_s^{(U)}$.

Spectral comparison (before vs. after interpolation filter):

![[DSP_U12_Tirsdag_2E_interp_compare_spectrum.png]]

Time-domain comparison (first 5 ms):

![[DSP_U12_Tirsdag_2E_interp_compare_time.png]]

> [!code]- MATLAB (2-E)
> ```matlab
> % Filter zero-stuffed signal with interpolation LP
> xU_filt = filter(b_I, 1, xU);
> 
> % Spectrum of interpolated signal
> XU_filt   = fft(xU_filt, Nfft_U);
> XU_filt_m = abs(XU_filt)/Nfft_U;
> XU_f_pos  = 2*XU_filt_m(1:Nfft_U/2+1);
> 
> figure;
> plot(fU_pos, XU_pos,    'LineWidth', 1.0); hold on;
> plot(fU_pos, XU_f_pos, 'LineWidth', 1.0);
> grid on;
> xlabel('F^{(U)} [Hz]');
> ylabel('|X(F^{(U)})|');
> title('Up-sampling: before vs after interpolation filter');
> legend('Zero-stuffed','Interpolated','Location','best');
> xlim([0 Fs_U/2]);
> 
> % Time-domain comparison (short window)
> figure;
> plot(tU*1e3, xU,      'LineWidth', 0.8); hold on;
> plot(tU*1e3, xU_filt, 'LineWidth', 1.0);
> grid on;
> xlim([0 5]);
> xlabel('t^{(U)} [ms]');
> ylabel('Amplitude');
> title('Up-sampling: zero-stuffed vs interpolated (time-domain)');
> legend('Zero-stuffed','Interpolated','Location','best');
> ```
> MATLAB docs: [`filter`](https://www.mathworks.com/help/matlab/ref/filter.html), [`fft`](https://www.mathworks.com/help/matlab/ref/fft.html)

---

### 2-F) Inverse FFT back to time domain (frequency-domain viewpoint)

The exercise sheet finally asks to:

> Take the spectrum of the **filtered** interpolated signal and apply the inverse FFT to get back to time domain.

This is equivalent to what we already did via time-domain filtering, but in the frequency-domain approach you:

1. Compute the filtered spectrum $Y[k]$ (either by FFT of the time-domain filtered signal, or by pointwise multiplying the up-sampled spectrum with the filter’s frequency response).  
2. Apply the inverse FFT:
   $$
   y[n] = \text{IFFT}\{Y[k]\}.
   $$

> [!code]- MATLAB (2-F)
> ```matlab
> % Frequency-domain reconstruction via IFFT (alternative view)
> % Here we reuse the spectrum of the filtered interpolated signal:
> YU_filt = XU_filt;          % already computed in 2-E
> 
> y_ifft = ifft(YU_filt, Nfft_U);
> y_ifft = real(y_ifft);      % numerical noise -> remove tiny imag parts
> 
> % Plot a short segment in time to compare with xU_filt
> figure;
> plot(tU*1e3, xU_filt, 'LineWidth', 1.0); hold on;
> plot(tU*1e3, y_ifft,  '--', 'LineWidth', 1.0);
> grid on;
> xlim([0 5]);
> xlabel('t^{(U)} [ms]');
> ylabel('Amplitude');
> title('Time-domain: filter+IFFT vs direct time-domain filtering');
> legend('xU\_filt (time-domain)','IFFT\{Y\_U\_filt\}','Location','best');
> ```
> MATLAB docs: [`ifft`](https://www.mathworks.com/help/matlab/ref/ifft.html)

---

**Summary**

- **Decimation by $M$** requires an AA LP to prevent aliasing; we designed it via the **Fourier-transform method** and windowing (rectangular window, $N_\text{taps} = 25$).  
- **Interpolation by $L$** is implemented as *zero-stuffing + LP*: we zero-stuffed by $L=3$ and designed an equiripple interpolation filter via **Parks–McClellan**, targeting a passband gain of $L$ and specified ripples.  
- FFT/IFFT allow us to verify the equivalence between **time-domain filtering** and **frequency-domain multiplication**.

