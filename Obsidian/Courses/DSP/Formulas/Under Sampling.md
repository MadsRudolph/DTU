> Quick refs: [[62743 E25 Under Sampling.pdf]]  
> Exercises: [[62743 E25 Digital Signal Processing Uge 12 Torsdag.pdf]]  
> Worked examples: [[Uge 12 - Torsdag]]

---

# Bandpass Sampling & Under-Sampling — Formula Sheet

## 📋 Table of Contents

1. [[#1-overview--notation|1. Overview & notation]]  
2. [[#2-baseband-vs-bandpass-signals|2. Baseband vs bandpass signals]]  
3. [[#3-bandpass-modulation--spectra|3. Bandpass modulation & spectra]]  
4. [[#4-classical-sampling-theorem-vs-bandpass-sampling|4. Classical sampling theorem vs bandpass sampling]]  
5. [[#5-integer-band-positioning-f_s--2b|5. Integer band positioning ($F_s = 2B$)]]  
   - [[#51-definitions|5.1 Definitions]]  
   - [[#52-odd-m--non-inverted-alias|5.2 Odd $m$ → non-inverted alias]]  
   - [[#53-even-m--inverted-alias|5.3 Even $m$ → inverted alias]]  
6. [[#6-arbitrary-band-positioning-f_s-≥-2b|6. Arbitrary band positioning ($F_s \ge 2B$)]]  
   - [[#61-no-overlap-condition-for-a-given-k|6.1 No-overlap condition for a given $k$]]  
   - [[#62-k_max-and-minimum-sampling-frequency|6.2 $k_\text{max}$ and minimum sampling frequency]]  
7. [[#7-practical-design-recipe-for-under-sampling|7. Practical design recipe for under-sampling]]  
8. [[#8-matlab-patterns-for-bandpass-under-sampling|8. MATLAB patterns for bandpass under-sampling]]

---

## 1. Overview & notation

We distinguish:

- **Analog signal**: $x_a(t)$, spectrum $X_a(F)$, $F$ in Hz.  
- **Discrete-time signal**: $x[n] = x_a(nT_s)$ with sampling period $T_s$ and sampling frequency
  $$
  F_s = \frac{1}{T_s}, \qquad F_\text{Nyq} = \frac{F_s}{2}.
  $$
- **Digital angular frequency** (rad/sample):
  $$
  \omega = 2\pi \frac{F}{F_s}
  \quad\Longleftrightarrow\quad
  F = \frac{\omega}{2\pi} F_s.
  $$

Key bandwidth definitions used in bandpass sampling:

- Lower and upper band-edges:
  $$
  F_L, \; F_H \quad [\text{Hz}]
  $$
- Bandwidth:
  $$
  B = F_H - F_L.
  $$

---

## 2. Baseband vs bandpass signals

### Baseband signal

- Spectrum centred around DC:
  $$
  X_a(F) \approx 0 \quad \text{for } |F| > B.
  $$
- Support approximately in $[-B, B]$.

### Bandpass signal

- Spectrum centred around some **carrier frequency** $F_\text{carrier}$:
  $$
  X_a(F) \approx 0 \quad \text{for } F \notin [F_L,F_H] \cup [-F_H,-F_L].
  $$
- Typically,
  $$
  F_L \approx F_\text{carrier}, \qquad F_H = F_L + B.
  $$

Intuition:

- Baseband: all content around $0$ Hz.  
- Bandpass: content around $\pm F_\text{carrier}$, with local bandwidth $B$.

---

## 3. Bandpass modulation & spectra

Slides use a sinusoidal baseband example:

- Baseband data:
  $$
  m(t) = \cos(2\pi F_0 t).
  $$
- **Double-sideband suppressed carrier (DSB-SC)**:
  $$
  x_1(t) = A_m m(t)\cos(2\pi F_\text{carrier} t).
  $$
  Spectral lines at $F_\text{carrier} \pm F_0$.
- **Standard AM**:
  $$
  x_2(t) = A_c\bigl[1 + m(t)\bigr]\cos(2\pi F_\text{carrier} t).
  $$

Product-to-sum identity (used heavily in Exercise 1):

$$
\cos\alpha \cos\beta
= \tfrac{1}{2}\cos(\alpha - \beta) + \tfrac{1}{2}\cos(\alpha + \beta).
$$

Example used in the exercises:

- Data frequency: $F_\text{data} = 1~\text{kHz}$  
- Carrier: $F_\text{carrier} = 16~\text{kHz}$  
- Signal:
  $$
  x_a(t) = \cos(2\pi F_\text{data} t)\cos(2\pi F_\text{carrier} t).
  $$

Then

$$
x_a(t) = \tfrac{1}{2}\cos\bigl(2\pi(F_\text{carrier} - F_\text{data})t\bigr)
       + \tfrac{1}{2}\cos\bigl(2\pi(F_\text{carrier} + F_\text{data})t\bigr),
$$

so spectrum has impulses at

$$
F = \pm(F_\text{carrier} - F_\text{data}),\ \pm(F_\text{carrier} + F_\text{data})
$$

with amplitude $0.25$.

---

## 4. Classical sampling theorem vs bandpass sampling

For a **low-pass / baseband** signal with bandwidth $B$:

- **Nyquist condition**:
  $$
  F_s \ge 2B \quad\Rightarrow\quad \text{no aliasing.}
  $$

For a **bandpass** signal with upper edge $F_H$:

- Direct application of sampling theorem:
  $$
  F_s \ge 2F_H.
  $$
  This can be impossible for very high carrier frequencies (optical comms slide example).

**Idea of bandpass sampling / under-sampling**:

- Instead of sampling at $\ge 2F_H$, we allow **controlled aliasing** so that one alias of the band lands in baseband without overlapping with other aliases.  
- Goal: choose $F_s$ such that:
  - the baseband alias still occupies bandwidth $B$, and  
  - different aliased copies of the band **do not overlap**.

---

## 5. Integer band positioning ($F_s = 2B$)

### 5.1 Definitions

In these special-case slides, we assume:

- Band edges:
  $$
  F_L, \quad F_H, \quad B = F_H - F_L
  $$
- **Integer band positioning**:
  $$
  F_H = m B, \quad m \in \mathbb{Z}.
  $$
- Sampling frequency chosen as:
  $$
  F_s = 2B.
  $$

Interpretation:

- The sampling replicas are spaced by $F_s = 2B$.  
- Because $F_H$ is an integer multiple of $B$, the replicas line up so that one alias of the band falls neatly into baseband.

The slides show two cases:

- $F_H = 5B$ (integer $m=5$) → non-inverted alias.  
- $F_H = 4B$ (integer $m=4$) → inverted alias.

---

### 5.2 Odd $m$ → non-inverted alias

If

$$
F_H = m B, \quad F_s = 2B, \quad m \text{ odd},
$$

then:

- The under-sampled spectrum in baseband is a **non-inverted** copy of the original baseband data spectrum (i.e. “same shape”).  
- This is the case used in Exercise 1-G:
  - $B = 4~\text{kHz}$,
  - $F_H = 20~\text{kHz}$,
  - $m = F_H/B = 5$ (odd),
  - $F_s = 2B = 8~\text{kHz}$.

Amplitude behaviour:

- Each baseband alias receives contributions from **two symmetric sidebands** (left and right), so line amplitudes become
  $$
  A_\text{alias} = 0.25 + 0.25 = 0.5
  $$
  in the exercise example.

---

### 5.3 Even $m$ → inverted alias

If

$$
F_H = m B, \quad F_s = 2B, \quad m \text{ even},
$$

then:

- The alias in baseband is **spectrally inverted (mirrored)**.  
- This is seen in Exercise 1-I:
  - $B = 4~\text{kHz}$,
  - $F_H = 16~\text{kHz}$,
  - $m = 4$ (even),
  - $F_s = 8~\text{kHz}$,
  - The baseband copy is reversed in frequency (low/high edges swapped).

In both odd and even cases:

- Aliasing is **intentional** and **controlled**.  
- As long as there is no overlap between replicas, we can reconstruct the data signal (possibly with an additional spectrum-reversal step when $m$ is even).

---

## 6. Arbitrary band positioning ($F_s \ge 2B$)

Integer band positioning $F_H = mB$ is a special, “nice” case.  
For general bandpass signals we use a more general inequality involving an integer $k$ that counts how many band copies fit between DC and $F_H$.

### 6.1 No-overlap condition for a given $k$

From the slides (“Arbitrary Band Positioning and Under-Sampling II”):

To avoid overlap of aliases for a **given integer $k \ge 2$**, $F_s$ must satisfy:

$$
\begin{cases}
2F_H \le k F_s, \\[4pt]
(k-1) F_s \le 2F_L.
\end{cases}
$$

This is equivalent to the **band of possible sampling frequencies**:

$$
\boxed{
  \frac{2F_H}{k} \;\le\; F_s \;\le\; \frac{2F_L}{k-1}
}
$$

If $F_s$ is chosen in this interval, the under-sampled aliases **do not overlap** for that $k$.

Interpretation:

- $k$ counts how many non-overlapping “bands” of width $B$ can be fitted in the range $[0, F_H]$.  
- Each admissible $k$ gives a **valid interval** of sampling frequencies.

The slide also shows the **general version** of “no overlap” for arbitrary $k$ and $F_s$; the box above is the practically used one.

---

### 6.2 $k_\text{max}$ and minimum sampling frequency

From “Arbitrary Band Positioning and Under-Sampling V / VI”:

We want to know the **maximum number of bands** $k_\text{max}$ that fit between DC and $F_H$ without overlap.

Result:

$$
k_\text{max} = \left\lfloor \frac{F_H}{B} \right\rfloor
$$

(floor = round down).

Then the **minimum allowable sampling frequency** with no aliasing is

$$
F_{s,\min} = \frac{2F_H}{k_\text{max}}.
$$

- For **large $k_\text{max}$**, this can be **much smaller than $2F_H$**, giving significant reduction in required sampling frequency.  
- This is the main motivation behind under-sampling in e.g. RF / optical front-ends.

---

## 7. Practical design recipe for under-sampling

The slides + exercises essentially suggest this workflow:

1. **Determine band edges and bandwidth**
   $$
   F_L,\ F_H, \quad B = F_H - F_L.
   $$
2. **Check integer band positioning**
   - Compute
     $$
     m = \frac{F_H}{B}.
     $$
   - If $m$ is an integer and you can choose
     $$
     F_s = 2B,
     $$
     then:
       - $m$ odd → non-inverted spectrum in baseband.  
       - $m$ even → inverted spectrum in baseband (can be fixed digitally).
3. **If $m$ is not an integer** (arbitrary band positioning):
   - For each integer $k = 2,3,\dots$:
     1. Compute candidate interval
        $$
        \frac{2F_H}{k} \le F_s \le \frac{2F_L}{k-1}.
        $$
     2. If interval is non-empty, any $F_s$ in it is acceptable (no alias overlap).
   - Optionally, use
     $$
     k_\text{max} = \left\lfloor\frac{F_H}{B}\right\rfloor, \quad
     F_{s,\min} = \frac{2F_H}{k_\text{max}}
     $$
     to find the **lowest reasonable** sample rate.
4. **Check inversion**:
   - For integer band positioning, parity of $m$ decides inversion.  
   - For arbitrary positioning, inversion pattern depends on how the band folds; may require explicit spectrum-reversal in the digital post-processing.
5. **Verify by simulation**:
   - Build a discrete-time model of $x_a(t)$ with very high reference sampling frequency $F_{s,\text{ref}} \gg 2F_H$.  
   - Numerically “sample” at candidate $F_s$ and inspect the spectrum via FFT to confirm that:
     - aliases do not overlap,  
     - baseband copy is what you expect (inverted or not).

---

## 8. MATLAB patterns for bandpass under-sampling

These are the patterns used in Exercise 1-F–1-I.

### 8.1 High-rate reference simulation (no aliasing)

> [!code]- MATLAB — Reference bandpass signal and spectrum
> ```matlab
> %% Reference simulation (very high Fs, no aliasing)
> clear; close all; clc;
> 
> Fdata    = 1e3;     % [Hz]
> Fcarrier = 16e3;    % [Hz]
> 
> Fs_ref   = 100 * Fcarrier;   % very high Fs
> Ts_ref   = 1 / Fs_ref;
> deltaf   = 50;               % frequency resolution [Hz]
> N_ref    = Fs_ref / deltaf;
> 
> n_ref = 0:N_ref-1;
> t_ref = n_ref * Ts_ref;
> 
> xa_ref = cos(2*pi*Fdata.*t_ref) .* cos(2*pi*Fcarrier.*t_ref);
> 
> % Two-sided FFT
> XA_ref   = fft(xa_ref, N_ref);
> XA_ref_s = fftshift(XA_ref);
> f_ref    = (-N_ref/2:N_ref/2-1) * (Fs_ref/N_ref);
> 
> figure;
> stem(f_ref/1e3, abs(XA_ref_s)/N_ref, 'filled'); grid on;
> xlabel('F [kHz]');
> ylabel('|X_a(F)|');
> title('Reference spectrum (no aliasing)');
> xlim([-40 40]);
> ```

---

### 8.2 Under-sampling at a candidate $F_s$

> [!code]- MATLAB — Test a specific under-sampling frequency
> ```matlab
> %% Under-sample reference signal at candidate Fs
> Fs_test = 8e3;                  % e.g. 2B
> 
> % Pick every R'th sample from reference to emulate sampling at Fs_test
> R = round(Fs_ref / Fs_test);    % integer ratio (assumes Fs_ref multiple)
> 
> xa_s = xa_ref(1:R:end);         % discrete-time samples at Fs_test
> N_s  = numel(xa_s);
> n_s  = 0:N_s-1;
> t_s  = n_s / Fs_test;
> 
> % Time-domain (short window)
> figure;
> stem(t_s*1e3, xa_s, 'filled'); grid on;
> xlim([0 5]);
> xlabel('t [ms]');
> ylabel('Amplitude');
> title(sprintf('Samples at F_s = %.1f kHz', Fs_test/1e3));
> 
> % Spectrum at Fs_test
> XA_s   = fft(xa_s, N_s);
> XA_s_s = fftshift(XA_s);
> f_s    = (-N_s/2:N_s/2-1) * (Fs_test/N_s);
> 
> figure;
> stem(f_s/1e3, abs(XA_s_s)/N_s, 'filled'); grid on;
> xlabel('F [kHz]');
> ylabel('|X(F)|');
> title(sprintf('Two-sided spectrum at F_s = %.1f kHz', Fs_test/1e3));
> xlim([-6 6]);
> ```

---

### 8.3 Quick helper to scan admissible $F_s$ intervals

> [!code]- MATLAB — Compute admissible Fs intervals for arbitrary band positioning
> ```matlab
> %% Compute admissible Fs intervals for bandpass under-sampling
> FL = 16e3;              % [Hz]
> FH = 20e3;              % [Hz]
> B  = FH - FL;
> 
> kmax = floor(FH / B);
> fprintf('k_max = %d\n', kmax);
> 
> for k = 2:kmax
>   Fs_min_k = 2*FH / k;
>   Fs_max_k = 2*FL / (k-1);
>   if Fs_min_k <= Fs_max_k
>       fprintf('k = %d:  Fs in [%.1f, %.1f] kHz\n', ...
>           k, Fs_min_k/1e3, Fs_max_k/1e3);
>   end
> end
> 
> Fs_min_global = 2*FH / kmax;
> fprintf('Lowest possible Fs (no aliasing): %.1f kHz\n', Fs_min_global/1e3);
> ```

Use these snippets together with the inequalities in Sections 5–7 to design and verify valid under-sampling schemes for exam problems and projects.
