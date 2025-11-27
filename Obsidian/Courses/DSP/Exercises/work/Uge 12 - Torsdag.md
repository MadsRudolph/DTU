> Quick refs: [[Under Sampling]]  
> Exercise sheet: [[62743 E25 Digital Signal Processing Uge 12 Torsdag.pdf]]  
> Solution sheet: [[62743 E25 Digital Signal Processing Uge 12 Torsdag solutions.pdf]]  
> Matlab document: [Open](<file:///C:/Users/Mads2/DTU/3.semester/DSP/UGE12/Torsdag.mlx>)

---

# Week 12 — Under-sampling of Passband Signals

---

## 📘 Concept Overview

We look at **bandpass sampling (under-sampling)** of a **passband AM signal**.

### Signal model used in the exercises

We consider

$$
x_a(t) = \cos(2\pi F_\text{data} t)\cos(2\pi F_\text{carrier} t),
$$

with

- Data (baseband) frequency:  
  $F_\text{data} = 1~\text{kHz}$  
- Carrier frequency:  
  $F_\text{carrier} = 16~\text{kHz}$ (or later $12~\text{kHz}$).

Using the product-to-sum identity, this is a **double-sideband suppressed-carrier (DSB-SC)** AM signal.

### Baseband vs bandpass + bandwidth

From the slides:

- **Baseband signal**: spectrum centered at $0$  
  $|F| \le B$
- **Bandpass signal**: spectrum around a carrier, with band edges
  $F_L, F_H$ and bandwidth
  $$
  B = F_H - F_L.
  $$

For a bandpass signal:

- Spectrum is nonzero only in approximately $[F_L, F_H]$ and $[-F_H, -F_L]$.

### Classical sampling vs bandpass sampling

- Classical **low-pass** sampling theorem:
  $$
  F_s \ge 2B \quad \Rightarrow \quad \text{no aliasing.}
  $$
- For a **bandpass** signal with upper edge $F_H$, the naïve requirement is
  $$
  F_s \ge 2F_H,
  $$
  which may be impossible in practice (optical communication example).

**Bandpass sampling idea** (from slides):

- We intentionally allow **aliasing**, but we choose $F_s$ such that:
  - One aliased copy of the band falls into baseband,
  - Different aliases **do not overlap**.

### Integer band positioning (special, “nice” case)

Define

$$
F_L, \quad F_H, \quad B = F_H - F_L, \quad m = \frac{F_H}{B}.
$$

If

- $m$ is an **integer**, and  
- we choose
  $$
  F_s = 2B,
  $$

then (slides “Integer Band Positioning and Under-Sampling I/II”):

- The band aliases exactly into baseband without overlap.
- If $m$ is **odd** → baseband spectrum is **non-inverted**.  
- If $m$ is **even** → baseband spectrum is **inverted** (mirrored).

### Arbitrary band positioning (general case)

From the “Arbitrary Band Positioning and Under-Sampling” slides:

For a given integer $k \ge 2$, no overlap of aliases if

$$
\frac{2F_H}{k} \le F_s \le \frac{2F_L}{k-1}.
$$

- Each $k$ defines an **admissible interval** of sampling frequencies.
- The **maximum** number of non-overlapping bands that fit up to $F_H$ is
  $$
  k_\text{max} = \left\lfloor \frac{F_H}{B} \right\rfloor,
  $$
  with minimum possible sampling frequency
  $$
  F_{s,\min} = \frac{2F_H}{k_\text{max}}.
  $$

In our exercise, we mainly stay in the **integer band positioning** case and use the general condition to understand why $F_s = 2.25B$ fails.

---

## Exercise 1 — Under-sampling of the AM passband signal

Given

$$
x_a(t) = \cos(2\pi F_\text{data} t)\cos(2\pi F_\text{carrier} t),
$$

with

$$
F_\text{data} = 1~\text{kHz}, \qquad F_\text{carrier} = 16~\text{kHz}.
$$

---

### 1-A) Time-domain expression with positive and negative frequencies

> Express the signal using both negative and positive frequencies analytically.

Use

$$
\cos \alpha \cos \beta
= \frac{1}{2}\cos(\alpha - \beta) + \frac{1}{2}\cos(\alpha + \beta).
$$

With $\alpha = 2\pi F_\text{data} t$ and $\beta = 2\pi F_\text{carrier} t$:

$$
\begin{aligned}
x_a(t)
&= \cos(2\pi F_\text{data} t)\cos(2\pi F_\text{carrier} t) \\
&= \frac{1}{2}\cos\bigl(2\pi(F_\text{carrier} - F_\text{data})t\bigr)
 + \frac{1}{2}\cos\bigl(2\pi(F_\text{carrier} + F_\text{data})t\bigr).
\end{aligned}
$$

Complex exponential form:

$$
\cos(2\pi F t) = \frac{1}{2}e^{j2\pi Ft} + \frac{1}{2}e^{-j2\pi Ft},
$$

so

$$
\begin{aligned}
x_a(t) 
&= \tfrac{1}{4} e^{j 2\pi (F_\text{carrier} - F_\text{data}) t}
 + \tfrac{1}{4} e^{-j 2\pi (F_\text{carrier} - F_\text{data}) t} \\
&\quad + \tfrac{1}{4} e^{j 2\pi (F_\text{carrier} + F_\text{data}) t}
 + \tfrac{1}{4} e^{-j 2\pi (F_\text{carrier} + F_\text{data}) t}.
\end{aligned}
$$

**Frequency-domain interpretation**

Spectral lines at

$$
F = \pm(F_\text{carrier} - F_\text{data}), \quad
F = \pm(F_\text{carrier} + F_\text{data}),
$$

each with amplitude $0.25$.

---

### 1-B) Analog spectrum

> Mark the frequencies in the figure below.

Compute band positions:

$$
F_\text{carrier} - F_\text{data} = 16~\text{kHz} - 1~\text{kHz} = 15~\text{kHz},
$$

$$
F_\text{carrier} + F_\text{data} = 16~\text{kHz} + 1~\text{kHz} = 17~\text{kHz}.
$$

So the analog spectrum has impulses at

$$
F = \{-17, -15, 15, 17\}~\text{kHz}
$$

each with height $0.25$.

Sketch in Obsidian:

![[DSP_U12_Torsdag_1B_analog_spectrum.png]]

---

### 1-C) Minimum sampling frequency to avoid aliasing

> According to the sampling theorem, what is the minimum sampling frequency if aliasing should be avoided?

Highest frequency present:

$$
F_\text{max} = F_\text{carrier} + F_\text{data} = 17~\text{kHz}.
$$

Nyquist:

$$
F_s \ge 2F_\text{max} = 2(F_\text{carrier} + F_\text{data}) = 34~\text{kHz}.
$$

So

$$
F_s^\text{(min)} = 34~\text{kHz}.
$$

This is the **“safe” low-pass Nyquist rate**, but later we will go **below** this using bandpass sampling.

---

### 1-D) Integer band positioning for under-sampling

Introduce the **bandwidth**

$$
B = 4~\text{kHz}.
$$

Per the slides “Baseband and Bandpass spectra”, set

$$
F_L = F_\text{carrier}, \qquad
F_H = F_L + B.
$$

For this example:

$$
F_L = 16~\text{kHz}, \qquad
F_H = 16~\text{kHz} + 4~\text{kHz} = 20~\text{kHz}.
$$

Now we apply **integer band positioning**:

- Choose sampling frequency
  $$
  F_s = 2B = 8~\text{kHz}.
  $$
- Compute
  $$
  m = \frac{F_H}{B} = \frac{20~\text{kHz}}{4~\text{kHz}} = 5.
  $$

So $m$ is an **odd integer**.

From the slides (Integer Band Positioning I):

- $F_s = 2B$ and $m$ integer means aliases line up so that **one alias lands in baseband** without overlap.
- If $m$ is odd → baseband alias is **non-inverted**.

Summary for 1-D:

- Sampling frequency:
  $$
  F_s = 2B = 8~\text{kHz}.
  $$
- Band edges:
  $$
  F_L = 16~\text{kHz}, \qquad
  F_H = 20~\text{kHz}.
  $$
- Integer band index:
  $$
  m = \frac{F_H}{B} = 5 \quad\Rightarrow\quad \text{non-inverted alias.}
  $$

This matches the **“integer band positioning, $F_H = 5B$”** slide.

---

### 1-E) Under-sampled spectrum sketch for $F_s = 2B = 8~\text{kHz}$

> Sketch the under-sampled spectrum, mark $F_s/2$, $F_L$, $F_H$, and the bandwidth $2B$ indicating the aliased windows.

Using $F_s = 8~\text{kHz}$:

- Replicas of the analog spectrum are spaced by $F_s$.
- The band $[16, 20]~\text{kHz}$ folds into the **baseband** $[-4,4]~\text{kHz}$.

Important detail:

- In the baseband interval $[-4,4]~\text{kHz}$ we get **two contributions**:
  - from the positive band $(15,17)~\text{kHz}$,
  - from the negative band $(-17,-15)~\text{kHz}$.
- By symmetry, both aliases land at the same baseband frequencies and **add**:

  $$
  0.25 + 0.25 = 0.5.
  $$

Thus in the under-sampled spectrum:

- Baseband impulses have amplitude $0.5$ instead of $0.25$.
- The shape matches the original baseband data spectrum (non-inverted, since $m$ is odd).

Sketch:

![[DSP_U12_Torsdag_1E_under_sampled_spectrum.png]]

---

### 1-F) MATLAB simulation with very high sampling frequency

> Sample the signal using a sampling frequency much higher than the minimum (no aliasing). Plot time signal and spectrum. Compare to 1-A and 1-B.

Choose reference parameters:

$$
F_\text{data} = 1~\text{kHz}, \quad
F_\text{carrier} = 16~\text{kHz},
$$

$$
F_{s,1} = 100F_\text{carrier} = 1.6~\text{MHz},
$$

$$
\Delta f = 50~\text{Hz}, \qquad
N_1 = \frac{F_{s,1}}{\Delta f}.
$$

Time vector:

$$
t_1[n] = nT_{s,1}, \qquad T_{s,1} = \frac{1}{F_{s,1}}, \quad n = 0,\dots,N_1 - 1.
$$

Sampled signal:

$$
x_{a,1}[n] = \cos(2\pi F_\text{data} t_1[n])\cos(2\pi F_\text{carrier} t_1[n]).
$$

Observations:

- Spectrum shows impulses at $\pm15~\text{kHz}$ and $\pm17~\text{kHz}$ with amplitude $0.25$.
- No aliasing since $F_{s,1} \gg 2F_H$ (fully consistent with Exercise 1-A/B).

Plots:

![[DSP_U12_Torsdag_1F_time_signal.png]]  
![[DSP_U12_Torsdag_1F_mag_spectrum_twosided.png]]

> [!code]- MATLAB — Exercise 1-F (Case 1: very high sampling frequency)
> ```matlab
> %% Exercise 1-F: Very high sampling frequency (no aliasing)
> clear; close all; clc;
> 
> lw       = 1.2;          % Line width for plots
> Fdata    = 1000;         % [Hz]
> Fcarrier = 16000;        % [Hz]
> 
> Fs1    = Fcarrier * 100; % Very high sampling frequency
> Ts1    = 1/Fs1;
> deltaf = 50;             % Desired frequency resolution [Hz]
> N1     = Fs1 / deltaf;   % Number of samples
> 
> t1 = 0:Ts1:(Ts1*(N1-1));
> 
> % Sampled AM signal
> xa1 = cos(2*pi*Fdata.*t1) .* cos(2*pi*Fcarrier.*t1);
> 
> % Time-domain plot (first 5 ms)
> figure;
> plot(t1*1e3, xa1, 'LineWidth', lw); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('Amplitude (a.u.)');
> title('Exercise 1-F: Time-domain signal (high Fs)');
> 
> % Spectrum via FFT
> XA1    = fft(xa1, N1);
> XA1_sh = fftshift(XA1);
> 
> f1 = (-N1/2:N1/2-1) * (Fs1/N1);
> 
> figure;
> stem(f1/1000, abs(XA1_sh)/N1, 'filled'); grid on;
> xlabel('Frequency [kHz]');
> ylabel('|X_a(F)|');
> title('Exercise 1-F: TWO-SIDED magnitude spectrum (high Fs)');
> xlim([-40 40]);
> ```

---

### 1-G) Under-sampling at $F_s = 2B$, $m = 5$ (odd integer)

> Reduce the sampling frequency to $2B$ and calculate time representation and spectrum. Compare with 1-F.

Now enforce **integer band positioning** from the slides:

$$
B = 4~\text{kHz}, \qquad
F_{s,2} = 2B = 8~\text{kHz}.
$$

Frequency resolution:

$$
\Delta f = 50~\text{Hz}, \qquad
N_2 = \frac{F_{s,2}}{\Delta f}.
$$

Time vector and samples:

$$
t_2[n] = nT_{s,2}, \quad T_{s,2} = \frac{1}{F_{s,2}}, \quad n = 0,\dots,N_2-1,
$$

$$
x_{a,2}[n] = \cos(2\pi F_\text{data} t_2[n])\cos(2\pi F_\text{carrier} t_2[n]).
$$

Band geometry (as in 1-D):

$$
F_L = 16~\text{kHz}, \qquad
F_H = 20~\text{kHz}, \qquad
B = 4~\text{kHz}, \qquad
m = \frac{F_H}{B} = 5.
$$

**Check with general arbitrary-band inequality**

For $k = m = 5$:

$$
\frac{2F_H}{5} = \frac{40~\text{kHz}}{5} = 8~\text{kHz},
\qquad
\frac{2F_L}{4} = \frac{32~\text{kHz}}{4} = 8~\text{kHz}.
$$

So the admissible interval collapses to the single point

$$
F_s = 8~\text{kHz},
$$

which is exactly our choice.

Observations:

- **No overlap** between aliases (we are in the white region of the $F_s/B$ vs $F_H/B$ plot).  
- Baseband alias is **non-inverted** since $m$ is odd.  
- Amplitudes in baseband are $0.5$ due to two contributing aliases.

Plots:

![[DSP_U12_Torsdag_1G_time_signal.png]]  
![[DSP_U12_Torsdag_1G_mag_spectrum_twosided.png]]

> [!code]- MATLAB — Exercise 1-G (Case 2: Fs = 2B)
> ```matlab
> %% Exercise 1-G: Under-sampling at Fs = 2B (integer band positioning, m = 5)
> clear; close all; clc;
> 
> lw       = 1.2;
> Fdata    = 1000;   % [Hz]
> Fcarrier = 16000;  % [Hz]
> B        = 4000;   % [Hz]
> 
> Fs2    = 2*B;      % = 8 kHz
> Ts2    = 1/Fs2;
> deltaf = 50;       % 50 Hz resolution
> N2     = Fs2/deltaf;
> 
> t2 = 0:Ts2:(Ts2*(N2-1));
> 
> xa2 = cos(2*pi*Fdata.*t2) .* cos(2*pi*Fcarrier.*t2);
> 
> figure;
> stem(t2*1e3, xa2, 'LineWidth', lw); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('Amplitude (a.u.)');
> title('Exercise 1-G: Time-domain signal (Fs = 2B)');
> 
> XA2    = fft(xa2, N2);
> XA2_sh = fftshift(XA2);
> f2     = (-N2/2:N2/2-1) * (Fs2/N2);
> 
> figure;
> stem(f2/1000, abs(XA2_sh)/N2, 'filled'); grid on;
> xlabel('Frequency [kHz]');
> ylabel('|X_a(F)|');
> title('Exercise 1-G: TWO-SIDED magnitude spectrum (Fs = 2B)');
> xlim([-6 6]);
> ```

---

### 1-H) Slightly higher sampling frequency $F_s = 2.25B$ (non-integer positioning)

> Increase the sampling frequency slightly from $2B$ to $2.25B$. Calculate the sampled signal and spectrum, and compare with 1-G.

Now:

$$
F_{s,3} = 2.25B = 9~\text{kHz},
$$

same

$$
F_L = 16~\text{kHz}, \quad
F_H = 20~\text{kHz}, \quad
B = 4~\text{kHz}.
$$

Time/samples:

$$
T_{s,3} = \frac{1}{F_{s,3}}, \qquad
t_3[n] = nT_{s,3}, \qquad
x_{a,3}[n] = \cos(2\pi F_\text{data} t_3[n])\cos(2\pi F_\text{carrier} t_3[n]).
$$

**Why it fails (slides + inequality):**

For arbitrary band positioning, no overlap requires

$$
\frac{2F_H}{k} \le F_s \le \frac{2F_L}{k-1}
$$

for some integer $k$.

- For $k = 5$:
  $$
  \frac{2F_H}{5} = 8~\text{kHz}, \quad
  \frac{2F_L}{4} = 8~\text{kHz} \Rightarrow F_s = 8~\text{kHz} \text{ only.}
  $$
- For $k = 4$:
  $$
  \frac{2F_H}{4} = 10~\text{kHz}, \quad
  \frac{2F_L}{3} \approx 10.67~\text{kHz}.
  $$
  Admissible interval: $[10,\,10.67]~\text{kHz}$.

Our $F_s = 9~\text{kHz}$ lies in **none** of the valid intervals → we are in the **grey “aliasing” region** in the slide.

Consequences :

- Aliases of the band overlap in frequency.
- Baseband region no longer represents the original data spectrum.
- The spectrum looks “scrambled” and cannot be used to recover $m(t)$.

Plots:

![[DSP_U12_Torsdag_1H_time_signal.png]]  
![[DSP_U12_Torsdag_1H_mag_spectrum_twosided.png]]

> [!code]- MATLAB — Exercise 1-H (Case 3: Fs = 2.25B, non-integer positioning)
> ```matlab
> %% Exercise 1-H: Fs = 2.25B (non-integer band positioning)
> clear; close all; clc;
> 
> lw       = 1.2;
> Fdata    = 1000;   % [Hz]
> Fcarrier = 16000;  % [Hz]
> B        = 4000;   % [Hz]
> 
> Fs3    = 2*B + 0.25*B;   % = 9 kHz
> Ts3    = 1/Fs3;
> deltaf = 50;             % 50 Hz resolution
> N3     = Fs3/deltaf;
> 
> t3 = 0:Ts3:(Ts3*(N3-1));
> 
> xa3 = cos(2*pi*Fdata.*t3) .* cos(2*pi*Fcarrier.*t3);
> 
> figure;
> stem(t3*1e3, xa3, 'LineWidth', lw); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('Amplitude (a.u.)');
> title('Exercise 1-H: Time-domain signal (Fs = 2.25B)');
> 
> XA3    = fft(xa3, N3);
> XA3_sh = fftshift(XA3);
> f3     = (-N3/2:N3/2-1) * (Fs3/N3);
> 
> figure;
> stem(f3/1000, abs(XA3_sh)/N3, 'filled'); grid on;
> xlabel('Frequency [kHz]');
> ylabel('|X_a(F)|');
> title('Exercise 1-H: TWO-SIDED magnitude spectrum (Fs = 2.25B)');
> xlim([-6 6]);
> ```

---

### 1-I) New carrier $F_\text{carrier} = 12~\text{kHz}$, under-sampling at $F_s = 2B$ (even $m$)

> Set the sampling frequency again to $2B$, but reduce the carrier frequency to $12~\text{kHz}$. Calculate sampled signal and spectrum; compare to 1-G.

Now:

$$
F_\text{data} = 1~\text{kHz}, \quad
F_\text{carrier} = 12~\text{kHz},
$$

same bandwidth:

$$
B = 4~\text{kHz}, \qquad
F_{s,4} = 2B = 8~\text{kHz}.
$$

New band edges:

$$
F_L = F_\text{carrier} = 12~\text{kHz}, \qquad
F_H = F_L + B = 16~\text{kHz}.
$$

Integer index:

$$
m = \frac{F_H}{B} = \frac{16~\text{kHz}}{4~\text{kHz}} = 4 \quad\text{(even)}.
$$

Per “Integer Band Positioning II” slide:

- Still **integer band positioning** with $F_s = 2B$ → aliases fit without overlap.
- But $m$ even → alias in baseband is **inverted (reversed)** compared to original baseband spectrum.

Original spectral lines:

$$
F_\text{carrier} \pm F_\text{data} = 12 \pm 1~\text{kHz}
\Rightarrow \pm 11~\text{kHz},\ \pm 13~\text{kHz}.
$$

Example alias around $3~\text{kHz}$ (from solution):

- $-13 + 2\cdot 8 = 3~\text{kHz}$,
- $11 - 8 = 3~\text{kHz}$,

two contributions adding to amplitude $0.5$.

So:

- Baseband alias is a **mirrored** version of $m(t)$’s spectrum,
- But still **usable** if we apply a digital spectrum-reversal step.

Plots:

![[DSP_U12_Torsdag_1I_time_signal.png]]  
![[DSP_U12_Torsdag_1I_mag_spectrum_twosided.png]]

> [!code]- MATLAB — Exercise 1-I (Case 4: new carrier 12 kHz, Fs = 2B, even m)
> ```matlab
> %% Exercise 1-I: Fs = 2B, Fcarrier = 12 kHz (even m -> reverted spectrum)
> clear; close all; clc;
> 
> lw       = 1.2;
> Fdata    = 1000;   % [Hz]
> Fcarrier = 12000;  % [Hz]  % new carrier
> B        = 4000;   % [Hz]
> 
> Fs4    = 2*B;      % = 8 kHz
> Ts4    = 1/Fs4;
> deltaf = 50;       % 50 Hz resolution
> N4     = Fs4/deltaf;
> 
> t4 = 0:Ts4:(Ts4*(N4-1));
> 
> xa4 = cos(2*pi*Fdata.*t4) .* cos(2*pi*Fcarrier.*t4);
> 
> figure;
> stem(t4*1e3, xa4, 'LineWidth', lw); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('Amplitude (a.u.)');
> title('Exercise 1-I: Time-domain signal (Fs = 2B, Fcarrier = 12 kHz)');
> 
> XA4    = fft(xa4, N4);
> XA4_sh = fftshift(XA4);
> f4     = (-N4/2:N4/2-1) * (Fs4/N4);
> 
> figure;
> stem(f4/1000, abs(XA4_sh)/N4, 'filled'); grid on;
> xlabel('Frequency [kHz]');
> ylabel('|X_a(F)|');
> title('Exercise 1-I: TWO-SIDED magnitude spectrum (Fs = 2B, Fcarrier = 12 kHz)');
> xlim([-6 6]);
> ```

---

### Final takeaway for Week 12

The four cases 1-F–1-I exactly illustrate the **bandpass sampling slides**:

- Using a huge $F_s$ reproduces the bandpass spectrum with **no aliasing**.  
- Choosing $F_s = 2B$ with **integer band positioning** ($F_H = mB$) and **odd $m$** gives a **non-inverted baseband replica**.  
- Slightly perturbing $F_s$ away from the admissible interval (e.g. $F_s = 2.25B$) moves us into the **forbidden “aliasing” regions** of the grey plot → baseband is unusable.  
- Changing the carrier so that $m$ becomes **even** keeps integer band positioning but **inverts** the baseband spectrum, as on “Integer Band Positioning II”.

Use this note together with [[Under Sampling]] for exam-style bandpass sampling problems.
