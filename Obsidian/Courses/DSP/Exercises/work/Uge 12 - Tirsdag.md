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

### 1-A) Sampled signal and spectrum

> a) Calculate the sampled signal $x[n]$ and plot it vs. time.  
> b) Calculate and plot the spectrum $X(F)$ as a function of frequency.

We first construct $x[n]$ and inspect:

- Time plot (zoomed to the first few milliseconds so we can see oscillations).  
- Magnitude spectrum using the FFT (one-sided spectrum up to $F_s/2$).

Time-domain signal:

![[DSP_U12_Tirsdag_1A_time_signal.png]]

Magnitude spectrum:

![[DSP_U12_Tirsdag_1A_mag_spectrum.png]]

> [!code]- MATLAB (1-A)
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
> % Spectrum (one-sided up to F_s/2)
> Nfft   = N;
> X      = fft(x, Nfft);
> Xmag   = abs(X)/Nfft;
> f_axis = (0:Nfft-1)*Fs/Nfft;
> f_pos  = f_axis(1:Nfft/2+1);
> Xpos   = 2*Xmag(1:Nfft/2+1);
> 
> figure;
> plot(f_pos, Xpos, 'LineWidth', 1.0); grid on; hold on;
> xline(F1, '--r', sprintf('F_1 = %d Hz', F1));
> xline(F2, '--r', sprintf('F_2 = %d Hz', F2));
> xlim([0 Fs/2]);
> xlabel('F [Hz]');
> ylabel('|X(F)|');
> title('Exercise 1-A: Magnitude spectrum of x[n]');
> ```
> MATLAB docs: [`fft`](https://www.mathworks.com/help/matlab/ref/fft.html), [`plot`](https://www.mathworks.com/help/matlab/ref/plot.html), [`xline`](https://www.mathworks.com/help/matlab/ref/xline.html)

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

Down-sampling by $M=2$ halves the sampling frequency:
$$
F_s' = \frac{F_s}{M} = \frac{8000}{2} = 4000~\text{Hz}.
$$

#### b) New Nyquist frequency

Nyquist frequency is half the sampling rate:
$$
F_{\max}' = \frac{F_s'}{2} = \frac{4000}{2} = 2000~\text{Hz}.
$$

#### c) Down-sampled time and frequency vectors

Let $x_D[k]$ have length $N_D$.

- Time vector:
  $$
  t'[k] = \frac{k}{F_s'}, \quad k = 0,\dots,N_D-1.
  $$
- Frequency vector (one-sided):
  $$
  f'[m] = \frac{m}{N_D}F_s', \quad m = 0,\dots,\frac{N_D}{2}.
  $$

Note: We **cannot** get the new frequency vector with `OldVector(1:M:end)` because the frequency spacing
$\Delta F' = F_s'/N_D$ changes when both $F_s$ and the number of samples change.

#### d) Down-sampled signal

Down-sampling by factor $M$ keeps every $M$’th sample:
$$
x_D[k] = x[2k], \quad k = 0,\dots,N_D-1.
$$

In MATLAB this is implemented with
`xD = x(1:M:end);`.

#### e) Time-domain plot

Time-domain behaviour of the down-sampled signal (zoom on first $5\,$ms):

![[DSP_U12_Tirsdag_1B_time_downsampled.png]]

#### f) Spectrum of the down-sampled signal

Magnitude spectrum of $x_D[k]$ (one-sided, in Hz):

![[DSP_U12_Tirsdag_1B_mag_downsampled.png]]

The FFT uses the new sampling rate $F_s' = 4000\,$Hz and the frequency vector $f'$ defined above.

#### g) Comparison to Exercise 1-A

- In 1-A the sampled signal contains two sinusoids at  
  $F_1 = 1000\,$Hz and $F_2 = 3500\,$Hz.
- After down-sampling:
  - $F_1 = 1000\,$Hz is still below the new Nyquist limit $F_{\max}' = 2000\,$Hz, so it remains unchanged.  
  - $F_2 = 3500\,$Hz is **above** $F_{\max}'$ and therefore aliases:
    $$
    F_{\text{alias}} = |F_2 - F_s'| = |3500 - 4000| = 500~\text{Hz}.
    $$
- In the spectrum of $x_D[k]$ you therefore see tones at $1000\,$Hz and $500\,$Hz instead of $1000\,$Hz and $3500\,$Hz.

This demonstrates the effect of down-sampling **without** an anti-alias filter.

> [!code]- MATLAB — Exercise 1-B (a–g)
> ```matlab
> % Exercise 1-B: Naive down-sampling by M = 2 (no AA filter)
> M      = 2;          % Down-sampling factor
> Fs_D   = Fs/M;       % a) New sampling frequency [Hz]
> Fmax_D = Fs_D/2;     % b) New Nyquist frequency [Hz]
> 
> fprintf('Exercise 1-B:\n');
> fprintf('  M        = %d\n', M);
> fprintf('  Fs''      = %.0f Hz\n', Fs_D);
> fprintf('  Fmax''    = %.0f Hz\n\n', Fmax_D);
> 
> % d) Down-sampled signal x_D[k] = x[2k]
> xD = x(1:M:end);
> ND = numel(xD);
> kD = 0:ND-1;
> 
> % c) Down-sampled time and frequency vectors
> tD      = kD / Fs_D;              % time vector t'[k]
> f_axisD = (0:ND-1) * Fs_D / ND;   % full frequency axis
> fD_pos  = f_axisD(1:ND/2+1);      % one-sided
> 
> % e) Time-domain plot
> figure;
> plot(tD*1e3, xD, 'LineWidth', 1.0); grid on;
> xlim([0 5]);
> xlabel('t'' [ms]');
> ylabel('x_D[k]');
> title('Exercise 1-B: Down-sampled signal x_D[k] (M = 2)');
> 
> % f) Spectrum of down-sampled signal
> XD        = fft(xD, ND);
> XDmag     = abs(XD)/ND;
> XDmag_pos = 2*XDmag(1:ND/2+1);
> 
> figure;
> plot(fD_pos, XDmag_pos, 'LineWidth', 1.0); grid on; hold on;
> xline(Fmax_D, ':k', 'F_{max}''');
> xlabel('F'' [Hz]');
> ylabel('|X_D(F'')|');
> title('Exercise 1-B: Magnitude spectrum after down-sampling (no AA filter)');
> xlim([0 Fs_D/2]);
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
> c) Select a suitable window type using the slide table.  
> d) Compute the minimum number of taps $N_\text{taps}$.  
> e) Compute $M$ and $K$.  
> f) Calculate and plot the **causal** impulse response.  
> g) Plot the magnitude response vs. frequency.

**Passband & stopband**

- Passband: $F_\text{pass} = 1855~\text{Hz}$  
- Stopband: $F_\text{stop} = 2145~\text{Hz}$  

**Cut-off frequency**

We choose the mid-point:
$$
F_c = \frac{F_\text{pass} + F_\text{stop}}{2}
= \frac{1855 + 2145}{2}
= 2000~\text{Hz},
$$
with normalized angular cutoff
$$
\omega_c = 2\pi \frac{F_c}{F_s}.
$$

**Window type**

- Required stopband attenuation: $A_s = 20~\text{dB}$.  
- From the window table: **rectangular window** has about $A_s \approx 21~\text{dB}$, so a rectangular window is sufficient.

**Minimum number of taps**

Using the slide formula for rectangular window:
$$
N_\text{taps} \approx \left\lceil \frac{0.9}{\Delta F_\text{sharp}} \right\rceil,
\qquad
\Delta F_\text{sharp} = \frac{F_\text{stop} - F_\text{pass}}{F_s}
= \frac{2145 - 1855}{8000}
= 0.03625.
$$

Thus:
$$
N_\text{taps} = \lceil 0.9 / 0.03625 \rceil = 25.
$$

We enforce an odd length (Type I linear-phase):

- $N_\text{taps,AA} = 25$  
- Filter order: $M_\text{AA} = 24$  
- Symmetry index: $K_\text{AA} = M_\text{AA}/2 = 12$

**Impulse response**

With a rectangular window, the causal FIR coefficients are the truncated ideal LP:

$$
h_\text{AA}[n]
= \frac{\omega_c}{\pi}\,
\operatorname{sinc}\!\left(\frac{\omega_c}{\pi}(n-K_\text{AA})\right),
\qquad n = 0,\dots,M_\text{AA},
$$

where MATLAB’s normalized sinc is

$$
\operatorname{sinc}(x) = \frac{\sin(\pi x)}{\pi x}.
$$

Impulse response:

![[DSP_U12_Tirsdag_1C_AA_impulse.png]]

Magnitude response:

![[DSP_U12_Tirsdag_1C_AA_mag.png]]

Log-magnitude (showing $\approx 20$ dB attenuation in the stopband):

![[DSP_U12_Tirsdag_1C_AA_logmag.png]]

> [!code]- MATLAB (1-C)
> ```matlab
> % AA filter specs
> Fpass_AA = 1855;     % Passband [Hz]
> Fstop_AA = 2145;     % Stopband [Hz]
> AsdB_AA  = 20;       % Stopband attenuation [dB]
> 
> DeltaF_sharp = (Fstop_AA - Fpass_AA)/Fs;
> Ntaps_AA = ceil(0.9 / DeltaF_sharp);   % rectangular window formula
> if mod(Ntaps_AA, 2) == 0
>     Ntaps_AA = Ntaps_AA + 1;           % force odd
> end
> M_AA = Ntaps_AA - 1;
> K_AA = M_AA/2;
> 
> Fc_AA = 0.5*(Fpass_AA + Fstop_AA);     % 2000 Hz
> wc_AA = 2*pi*Fc_AA/Fs;
> 
> nA          = 0:M_AA;
> nA_centered = nA - K_AA;
> hAA_centered = (wc_AA/pi) * sinc((wc_AA/pi)*nA_centered);
> b_AA         = hAA_centered;
> 
> % Impulse response
> figure;
> stem(nA, b_AA, 'filled'); grid on;
> xlabel('n'); ylabel('h_{AA}[n]');
> title(sprintf('Anti-alias LP FIR: N_{taps} = %d', Ntaps_AA));
> 
> % Frequency response
> [H_AA, w_AA] = freqz(b_AA, 1, Nfft);
> F_AA = w_AA*Fs/(2*pi);
> 
> figure;
> plot(F_AA, abs(H_AA), 'LineWidth', 1.0); grid on; hold on;
> xline(Fpass_AA, '--g', 'F_{pass}');
> xline(Fstop_AA, '--r', 'F_{stop}');
> xlabel('F [Hz]'); ylabel('|H_{AA}(F)|');
> title('Anti-alias LP (rectangular window) — Magnitude response');
> 
> HdB_AA = 20*log10(abs(H_AA)+eps);
> figure;
> plot(F_AA, HdB_AA, 'LineWidth', 1.0); grid on; hold on;
> xline(Fpass_AA, '--g', 'F_{pass}');
> xline(Fstop_AA, '--r', 'F_{stop}');
> yline(-AsdB_AA, ':k', '-A_s');
> xlabel('F [Hz]'); ylabel('H_{AA,dB}(F) [dB]');
> title('Anti-alias LP (rectangular window) — Log magnitude');
> ```
> MATLAB docs: [`sinc`](https://www.mathworks.com/help/matlab/ref/sinc.html), [`freqz`](https://www.mathworks.com/help/signal/ref/freqz.html), [`stem`](https://www.mathworks.com/help/matlab/ref/stem.html)

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

### 2-A/B) Zero-stuffing and spectrum of up-sampled signal

> a) Form the up-sampled sequence by **zero-stuffing** with factor $L=3$.  
> b) Define the new time/frequency vectors and plot the up-sampled signal and its spectrum.

Zero-stuffed sequence:
$$
x_U[m] =
\begin{cases}
x[n], & m = nL\\
0, & \text{otherwise}.
\end{cases}
$$

Time-domain (first 5 ms): many zeros between original samples:

![[DSP_U12_Tirsdag_2A_upsampled_time.png]]

Magnitude spectrum (note the $L-1=2$ spectral images):

![[DSP_U12_Tirsdag_2A_upsampled_spectrum.png]]

> [!code]- MATLAB (2-A/B)
> ```matlab
> L    = 3;                   % Interpolation factor
> Fs_U = L*Fs;                % New sampling frequency
> N_U  = L*N;                 % Number of samples after up-sampling
> 
> xU = zeros(1, N_U);
> xU(1:L:end) = x;            % zero-stuffing
> 
> nU = 0:N_U-1;
> tU = nU/Fs_U;
> 
> % Time-domain plot (first 5 ms)
> figure;
> plot(tU*1e3, xU, 'LineWidth', 1.0); grid on;
> xlim([0 5]);
> xlabel('t^{(U)} [ms]');
> ylabel('x_U[m]');
> title('Exercise 2-A: Zero-stuffed up-sampled sequence x_U[m]');
> 
> % Spectrum of up-sampled signal
> Nfft_U  = N_U;
> XU      = fft(xU, Nfft_U);
> XUmag   = abs(XU)/Nfft_U;
> f_axisU = (0:Nfft_U-1)*Fs_U/Nfft_U;
> fU_pos  = f_axisU(1:Nfft_U/2+1);
> XU_pos  = 2*XUmag(1:Nfft_U/2+1);
> 
> figure;
> plot(fU_pos, XU_pos, 'LineWidth', 1.0); grid on;
> xlabel('F^{(U)} [Hz]');
> ylabel('|X_U(F^{(U)})|');
> title('Exercise 2-A: Spectrum after zero-stuffing (images present)');
> xlim([0 Fs_U/2]);
> ```
> MATLAB docs: [`fft`](https://www.mathworks.com/help/matlab/ref/fft.html)

---

### 2-C/D) Interpolation LP design via Parks–McClellan

> Design an interpolation LP filter using the Parks–McClellan algorithm with:  
> - $F_\text{pass} = 3500~\text{Hz}$  
> - $F_\text{stop} = 4500~\text{Hz}$  
> - Passband gain $A_\text{pass} = L$  
> - Passband tolerance $\delta_1 = 0.05$  
> - Stopband tolerance $\delta_2 = 0.02$  
>
> a) Find normalized angular passband and stopband frequencies.  
> b) Estimate $M$ (filter order) using the standard formula.  
> c) Design the filter using `firpm`.  
> d) Plot the magnitude response and check if specs are met.

**Normalized angular frequencies** (with $F_s^{(U)} = 24000~\text{Hz}$):

$$
\omega_p = 2\pi\frac{F_\text{pass}}{F_s^{(U)}} 
= 2\pi \frac{3500}{24000}
\approx 0.916~\text{rad/sample},
$$
$$
\omega_s = 2\pi\frac{F_\text{stop}}{F_s^{(U)}} 
= 2\pi \frac{4500}{24000}
\approx 1.178~\text{rad/sample}.
$$

Transition width:
$$
\Delta\omega = \omega_s - \omega_p \approx 0.262~\text{rad/sample}.
$$

Worst-case ripple:
$$
\delta = \min(\delta_1, \delta_2) = 0.02
\Rightarrow
A_\text{dB} = -20\log_{10}(\delta) \approx 34~\text{dB}.
$$

Order estimate for equiripple LP (Oppenheim/Hamming):
$$
M \approx \left\lceil
\frac{A_\text{dB} - 7.95}{2.285\,\Delta\omega}
\right\rceil
\approx 44.
$$

We use an **even** $M$ to get a Type I linear-phase FIR, so $M = 44$ and $N_\text{taps} = M+1 = 45$.

The filter is designed in normalized frequency $0 \le f \le 1$ (where $1$ corresponds to $F_s^{(U)}/2$):

- Normalized passband edge:
  $$
  f_\text{pass,norm} = \frac{F_\text{pass}}{F_s^{(U)}/2}
  = \frac{3500}{12000}.
  $$
- Normalized stopband edge:
  $$
  f_\text{stop,norm} = \frac{F_\text{stop}}{F_s^{(U)}/2}
  = \frac{4500}{12000}.
  $$

Magnitude response (linear):

![[DSP_U12_Tirsdag_2B_interp_filter_mag.png]]

Log-magnitude:

![[DSP_U12_Tirsdag_2B_interp_filter_logmag.png]]

> [!code]- MATLAB (2-C/D)
> ```matlab
> % Interpolation filter specs
> Fpass_I = 3500;      % Passband edge [Hz]
> Fstop_I = 4500;      % Stopband edge [Hz]
> delta1  = 0.05;      % Passband ripple
> delta2  = 0.02;      % Stopband ripple
> 
> omega_p = 2*pi*Fpass_I/Fs_U;
> omega_s = 2*pi*Fstop_I/Fs_U;
> Delta_w = omega_s - omega_p;
> 
> delta = min(delta1, delta2);
> A_dB  = -20*log10(delta);
> 
> % Parks–McClellan order estimate
> M_est = ceil((A_dB - 7.95)/(2.285*Delta_w));
> if mod(M_est, 2) ~= 0
>     M_est = M_est + 1;   % enforce even M => Type I linear-phase
> end
> Ntaps_I = M_est + 1;
> 
> % Normalized frequencies for firpm (0..1 -> 0..F_Nyq)
> F_Nyq_U     = Fs_U/2;
> Fpass_normI = Fpass_I/F_Nyq_U;
> Fstop_normI = Fstop_I/F_Nyq_U;
> 
> f_firpm = [0 Fpass_normI Fstop_normI 1];
> a_firpm = [L L 0 0];                 % gain L in passband, 0 in stopband
> w_firpm = [1/delta1 1/delta2];       % weighting
> 
> b_I = firpm(M_est, f_firpm, a_firpm, w_firpm);
> 
> % Frequency response of interpolation filter
> [H_I, w_I] = freqz(b_I, 1, Nfft_U);
> 
> figure;
> plot(w_I, abs(H_I), 'LineWidth', 1.0); grid on; hold on;
> xline(omega_p, '--g', '\omega_p');
> xline(omega_s, '--r', '\omega_s');
> yline(L+delta1, ':k');
> yline(L-delta1, ':k');
> xlabel('\omega [rad/sample]');
> ylabel('|H_I(e^{j\omega})|');
> title('Interpolation LP (Parks–McClellan) — Magnitude');
> 
> HdB_I = 20*log10(abs(H_I)+eps);
> figure;
> plot(w_I, HdB_I, 'LineWidth', 1.0); grid on; hold on;
> xline(omega_p, '--g', '\omega_p');
> xline(omega_s, '--r', '\omega_s');
> yline(-20*log10(1-delta1), ':k');  % approx passband bound
> yline(-20*log10(delta2), ':k');    % stopband bound
> xlabel('\omega [rad/sample]');
> ylabel('H_{I,dB}(\omega) [dB]');
> title('Interpolation LP (Parks–McClellan) — Log magnitude');
> ```
> MATLAB docs: [`firpm`](https://www.mathworks.com/help/signal/ref/firpm.html), [`freqz`](https://www.mathworks.com/help/signal/ref/freqz.html)

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

