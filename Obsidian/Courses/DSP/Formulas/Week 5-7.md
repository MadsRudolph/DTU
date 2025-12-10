# DTU 62743 DSP Formula Sheet: Weeks 5-7 (Maryam)
**Z-Domain Continuation, DFT, and Sampling**  
**Strict adherence to DTU course materials (E19-F25 exam solutions)**

---

## 📋 Table of Contents

### Week 5: Z-Domain Analysis (Continuation)
- [[#5.1 Higher-Order Systems]]
- [[#5.2 Frequency Response from Z-Transform]]
- [[#5.3 Stability Check]]
- [[#5.4 ROC (Region of Convergence)]]
- [[#5.5 Inverse Systems]]
- [[#5.6 All-Pass Filters & Minimum Phase Decomposition]]
- [[#5.7 Minimum Phase Decomposition]]

### Week 6: Discrete Fourier Transform (DFT)
- [[#6.1 From DTFT to DFT]]
- [[#6.2 DFT Properties]]
- [[#6.3 DFT via FFT]]
- [[#6.4 Frequency Resolution]]
- [[#6.5 DFT Magnitude Spectrum]]

### Week 7: Sampling of Analog Signals
- [[#7.1 Nyquist Sampling Theorem]]
- [[#7.2 Aliasing]]
- [[#7.3 Frequency Conversion]]
- [[#7.4 Sampling Process]]
- [[#7.5 Spectral Replication]]
- [[#7.6 Anti-Aliasing (AA) Filter]]
- [[#7.7 Bandpass Sampling (Under-sampling)]]

---

## Week 5 - Z-Domain Analysis (Continuation)

### 5.1 Higher-Order Systems

**Second-order transfer function:**
$$H(z) = G \frac{1 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}}$$

**Difference equation** (from [[DSPMartaUge05tirsdag]]):
$$y[n] + a_1 y[n-1] + a_2 y[n-2] = x[n] + b_1 x[n-1] + b_2 x[n-2]$$

Or in standard form:
$$y[n] = -a_1 y[n-1] - a_2 y[n-2] + x[n] + b_1 x[n-1] + b_2 x[n-2]$$

**General form for any order:**
$$y[n] = -\sum_{k=1}^{N} a_k y[n-k] + \sum_{k=0}^{M} b_k x[n-k]$$

### 5.2 Frequency Response from Z-Transform

**Evaluate at unit circle:**
$$H(e^{j\omega}) = H(z)\bigg|_{z=e^{j\omega}}$$

**For second-order systems:**
- Compute at specific frequencies: $\omega = 0$ (DC), $\omega = \pi$ (Nyquist)
- $H(1)$ = DC gain
- $H(-1)$ = Nyquist frequency gain

### 5.3 Stability Check

**Pole analysis:**
- All poles must satisfy $|p_k| < 1$ (inside unit circle)
- For second-order: solve $1 + a_1 z^{-1} + a_2 z^{-2} = 0$
- Multiply by $z^2$: $z^2 + a_1 z + a_2 = 0$

**MATLAB:**
```matlab
poles = roots([1 a1 a2]);
if all(abs(poles) < 1)
    disp('System is stable');
end
```

### 5.4 ROC (Region of Convergence)

**For causal systems:**
- ROC: $|z| > r_{\max}$, where $r_{\max}$ is the largest pole magnitude
- Stable and causal: all poles inside unit circle

**For anti-causal systems:**
- ROC: $|z| < r_{\min}$

### 5.5 Inverse Systems

**Condition for stable inverse:**
$$H_{\text{inv}}(z) = \frac{1}{H(z)}$$

- **All ZEROS of $H(z)$ must be inside unit circle** for stable inverse
- This is the **minimum phase condition** [[E20 Exam]], [[F25 Exam]]

**Example from exams:**
- If $H(z)$ has a zero at $z = 1.2$ (outside unit circle), the inverse system is **unstable**

### 5.6 All-Pass Filters & Minimum Phase Decomposition [[E22 Exam]], [[F24 Exam]], [[E24 Exam]]

**All-Pass Filter Definition:**
A system $H_{ap}(z)$ is **all-pass** if:
$$|H_{ap}(e^{j\omega})| = 1 \quad \text{for all } \omega$$

**Pole-Zero Symmetry Rule (CRITICAL):**
- For every pole $p$ inside the unit circle, there is a **zero at $1/p^*$** (reciprocal conjugate)
- Poles and zeros are **mirror images** across the unit circle

**First-Order All-Pass:**
$$H_{ap}(z) = \frac{z^{-1} - a^*}{1 - az^{-1}}, \quad |a| < 1$$

Or equivalently:
$$H_{ap}(z) = G \frac{1 - z_0 z^{-1}}{1 - p z^{-1}}$$

where $z_0 = 1/p^*$ (zero is reciprocal conjugate of pole).

**Gain Normalization:**
To ensure $|H_{ap}(e^{j\omega})| = 1$ exactly, choose:
$$G = \frac{|p|}{|z_0|} = |p|^2$$

For real poles/zeros: $G = p^2$ if $p$ is the pole location.

---

### 5.7 Minimum Phase Decomposition [[F24 Exam]]

**Any causal stable system can be factored as:**
$$H(z) = H_{min}(z) \cdot H_{ap}(z)$$

**Where:**
- $H_{min}(z)$ = **minimum phase** (all zeros inside unit circle)
- $H_{ap}(z)$ = **all-pass** (handles zeros outside unit circle)

**Decomposition Procedure:**

**Step 1:** Identify zeros of $H(z)$
- Zeros **inside** UC → keep in $H_{min}(z)$
- Zeros **outside** UC → move to $H_{ap}(z)$

**Step 2:** For each "bad" zero $z_0$ outside UC:
- Create all-pass section: 
  $$H_{ap,k}(z) = G \frac{1 - z_0 z^{-1}}{1 - (1/z_0^*) z^{-1}}$$
- Replace $z_0$ with its **reflected version** $1/z_0^*$ in $H_{min}(z)$

**Step 3:** Combine:
$$H(z) = H_{min}(z) \cdot \prod_k H_{ap,k}(z)$$

**Example from** [[F24 Exam]]:

Given: $H(z) = \frac{(1+3z^{-1})(1-\tfrac12 z^{-1})}{z^{-1}(1+\tfrac13 z^{-1})}$

- Zero at $z = -3$ (outside) → use all-pass
- Zero at $z = 0.5$ (inside) → keep in $H_{min}$

**All-pass for $z_0 = -3$:**
$$H_{ap}(z) = \frac13 \frac{1 + 3z^{-1}}{1 + \tfrac13 z^{-1}}$$

**Minimum phase:**
$$H_{min}(z) = 3 \frac{1 - \tfrac12 z^{-1}}{z^{-1}}$$

**Check:** $H(z) = H_{min}(z) \cdot H_{ap}(z)$ ✓

---

**MATLAB Verification:**
```matlab
% Check if system is all-pass
[b, a] = ... % your filter coefficients
[H, w] = freqz(b, a, 1024);
mag = abs(H);
is_allpass = all(abs(mag - 1) < 1e-6);  % Should be 1 everywhere

% Decompose system (manual)
zeros_H = roots(b);
poles_H = roots(a);

% Identify zeros outside UC
bad_zeros = zeros_H(abs(zeros_H) > 1);

% For each bad zero, create all-pass section
% ... (see F24 exam solution for complete code)
```

---

**Common Exam Questions:**
1. **Prove a system is all-pass** → Show $|H(e^{j\omega})| = 1$ for all $\omega$
2. **Find $H_{min}(z)$ and $H_{ap}(z)$** → Use decomposition procedure
3. **Check if inverse is stable** → All zeros must be inside UC (minimum phase)

---

## Week 6 - Discrete Fourier Transform (DFT)

### 6.1 From DTFT to DFT

**DTFT (continuous in frequency):**
$$X(\omega) = \sum_{n=-\infty}^{\infty} x[n] e^{-j\omega n}$$

**DFT (sampled at $N$ frequencies):**
$$X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\frac{2\pi}{N}kn}, \quad k = 0, 1, \ldots, N-1$$

**Sampling frequencies:**
$$\omega_k = \frac{2\pi}{N} k$$

**Relationship:**
$$X[k] = X(\omega)\bigg|_{\omega = \frac{2\pi k}{N}}$$

### 6.2 DFT Properties

**Periodicity:**
$$X[k + N] = X[k]$$

**Symmetry (for real signals):**
$$X[k] = X^*[N-k]$$
- Only need to compute $k = 0, 1, \ldots, N/2$ for real signals

**Inverse DFT:**
$$x[n] = \frac{1}{N} \sum_{k=0}^{N-1} X[k] e^{j\frac{2\pi}{N}kn}$$

### 6.3 DFT via FFT

**MATLAB computation:**
```matlab
N = length(x);
X = fft(x);              % DFT via FFT algorithm
```

**Frequency vector (Hz):**
```matlab
Fs = 1000;               % Sampling frequency
f = (0:N-1) * (Fs/N);    % Frequency bins
```

**Two-sided spectrum (centered):**
```matlab
X_centered = fftshift(X);
f_centered = (-N/2:N/2-1) * (Fs/N);
```

### 6.4 Frequency Resolution

**Frequency bin spacing:**
$$\Delta f = \frac{F_s}{N}$$

**To improve resolution:**
- Increase $N$ (longer signal)
- Zero-padding: append zeros to signal before FFT

**Example:**
- $F_s = 1000$ Hz, $N = 100$ samples → $\Delta f = 10$ Hz
- $F_s = 1000$ Hz, $N = 1000$ samples → $\Delta f = 1$ Hz

### 6.5 DFT Magnitude Spectrum

**Power spectrum (one-sided):**
```matlab
X = fft(x);
P = (1/N) * abs(X(1:N/2+1)).^2;  % Power
P(2:end-1) = 2*P(2:end-1);        % Account for negative frequencies
f = (0:N/2) * (Fs/N);
```

**Magnitude in dB:**
```matlab
Mag_dB = 20*log10(abs(X));
```

---

## Week 7 - Sampling of Analog Signals

### 7.1 Nyquist Sampling Theorem [[F24 Exam]], [[E23 Exam]]

**Fundamental rule:**
$$F_s \geq 2F_{\max}$$

Or in angular frequency:
$$\Omega_s \geq 2\Omega_{\max}$$

**Where:**
- $F_s$ = sampling frequency (Hz)
- $F_{\max}$ = highest frequency in analog signal
- $\Omega_s = 2\pi F_s$ (rad/s)

**Critical sampling:**
$$F_s = 2F_{\max}$$ (minimum, but prone to errors in practice)

**Practical sampling:**
$$F_s = (2.5 \text{ to } 10) \times F_{\max}$$

### 7.2 Aliasing [[F24 Exam]]

**Occurs when:**
$$F_s < 2F_{\max}$$

**Aliased frequency formula (single fold):**
$$F_{\text{alias}} = F - 2(F - F_s/2)$$

**Or alternatively:**
$$F_{\text{alias}} = |F - kF_s|$$
where $k$ is chosen so $F_{\text{alias}} \in [0, F_s/2]$

**Example from** [[F24 Exam]]:
- Analog signal: $F_1 = 200$ Hz, $F_2 = 750$ Hz
- Sampling: $F_s = 1000$ Hz → $F_s/2 = 500$ Hz
- $F_1 = 200$ Hz < 500 Hz ✓ (no aliasing)
- $F_2 = 750$ Hz > 500 Hz ✗ (aliasing!)
- $F_{2,\text{alias}} = 750 - 2(750 - 500) = 250$ Hz

### 7.3 Frequency Conversion

**Analog to digital:**
$$\omega = 2\pi \frac{F}{F_s} = \Omega T_s$$

**Where:**
- $\omega$ = digital angular frequency (rad/sample)
- $F$ = analog frequency (Hz)
- $\Omega = 2\pi F$ = analog angular frequency (rad/s)
- $T_s = 1/F_s$ = sampling period (s)

**Digital Nyquist frequency:**
$$\omega_{\max} = \pi \text{ rad/sample}$$

### 7.4 Sampling Process [[DSPMartaUge07tirsdag]]

**Impulse train model:**
$$s(t) = \sum_{k=-\infty}^{\infty} \delta(t - kT_s)$$

**Sampled signal:**
$$x_s(t) = x_a(t) \cdot s(t) = \sum_{k=-\infty}^{\infty} x_a(kT_s) \delta(t - kT_s)$$

**Discrete-time signal:**
$$x[n] = x_a(nT_s)$$

### 7.5 Spectral Replication

**After sampling, spectrum repeats:**
$$X_s(\omega) = \frac{1}{T_s} \sum_{k=-\infty}^{\infty} X_a\left(\omega - \frac{2\pi k}{T_s}\right)$$

**Replicas centered at:**
$$\omega = \pm 2\pi k, \quad k = 0, 1, 2, \ldots$$

**Or in Hz:**
$$F = \pm kF_s, \quad k = 0, 1, 2, \ldots$$

### 7.6 Anti-Aliasing (AA) Filter

**Purpose:**
- Remove frequencies above $F_s/2$ before sampling

**Requirements:**
- **Passband:** $0 \leq F \leq F_p$ (keep signal content)
- **Stopband:** $F_s/2 \leq F$ (attenuate to prevent aliasing)
- **Transition band:** $F_p < F < F_s/2$

**Example specs:**
- $F_p = 350$ Hz (passband edge)
- $F_s = 1000$ Hz → $F_s/2 = 500$ Hz
- Need attenuation > 30 dB for $F > 500$ Hz

**MATLAB (analog Butterworth AA-filter):**
```matlab
Fp = 350;           % Passband edge (Hz)
Fs_samp = 1000;     % Sampling frequency
Omega_p = 2*pi*Fp;  % Convert to rad/s

% Design 4th-order Butterworth
[b_analog, a_analog] = butter(4, Omega_p, 's');

% Frequency response
Omega = linspace(0, 2*pi*600, 1000);
H_analog = freqs(b_analog, a_analog, Omega);
```

### 7.7 Bandpass Sampling (Under-sampling)

**For bandpass signals with bandwidth $B$:**

If signal occupies $[F_L, F_H]$ with $B = F_H - F_L$:

**Integer band positioning:**
$$\frac{2F_H}{k} \leq F_s \leq \frac{2F_L}{k-1}$$

for positive integer $k$.

**Minimum sampling rate:**
$$F_s \geq 2B$$
(can be much less than $2F_H$!)

**Example from exams:**
- Carrier modulated signal: $F_{\text{carrier}} = 16$ kHz, $F_{\text{data}} = 1$ kHz
- Band: $[15 \text{ kHz}, 17 \text{ kHz}]$, $B = 2$ kHz
- Standard Nyquist: $F_s \geq 34$ kHz
- Bandpass sampling: $F_s \geq 4$ kHz (much lower!)

**See also:** [[Under Sampling]] for complete bandpass sampling formulas

---

## Exam Strategy for Weeks 5-7

### Most Common Question Types

**Week 5 (Z-domain continuation):**
1. Second-order difference equations → transfer function
2. Stability checks via pole locations
3. Inverse system stability (check zeros inside unit circle)
4. Frequency response evaluation at DC and Nyquist
5. **All-pass filter identification** [[E22 Exam]]
6. **Minimum phase decomposition** [[F24 Exam]]

**Week 6 (DFT):**
1. Computing DFT manually for short sequences
2. FFT in MATLAB with proper scaling
3. Frequency resolution calculations
4. Spectrum plotting (two-sided vs. one-sided)
5. Zero-padding effects

**Week 7 (Sampling):**
1. Nyquist frequency calculation: $F_s \geq 2F_{\max}$
2. Aliasing frequency formula: $F_{\text{alias}} = F - 2(F - F_s/2)$
3. Frequency conversion: $\omega = 2\pi F/F_s$
4. AA-filter specifications
5. Spectrum replication diagrams

### Critical Formulas to Memorize

1. **Difference equation ↔ Transfer function:**
   $$y[n] = -\sum a_k y[n-k] + \sum b_k x[n-k] \quad \Leftrightarrow \quad H(z) = \frac{\sum b_k z^{-k}}{1 + \sum a_k z^{-k}}$$

2. **All-pass magnitude:**
   $$|H_{ap}(e^{j\omega})| = 1 \text{ for all } \omega$$

3. **Pole-zero reciprocal:**
   $$\text{Zero at } z_0 = 1/p^* \text{ for pole at } p$$

4. **DFT definition:**
   $$X[k] = \sum_{n=0}^{N-1} x[n] e^{-j\frac{2\pi}{N}kn}$$

5. **Nyquist theorem:**
   $$F_s \geq 2F_{\max}$$

6. **Aliasing formula:**
   $$F_{\text{alias}} = F - 2(F - F_s/2)$$

7. **Frequency conversion:**
   $$\omega = 2\pi \frac{F}{F_s}$$

### Common Mistakes to Avoid

1. **Forgetting to check zeros for inverse system stability** (not just poles!)
2. **Missing the reciprocal conjugate relationship** in all-pass filters
3. **Wrong aliasing formula** - missing the "2" factor
4. **Confusing $\omega$ (rad/sample) with $\Omega$ (rad/s)**
5. **Forgetting $1/N$ scaling in inverse DFT**
6. **Not centering FFT output with fftshift for two-sided spectrum**
7. **Mixing up DC gain $H(1)$ and Nyquist gain $H(-1)$**

### MATLAB Quick Reference

```matlab
% Z-domain
poles = roots(a);                    % Find poles
zeros = roots(b);                    % Find zeros
[H, w] = freqz(b, a, N);            % Frequency response
mag_check = all(abs(abs(H)-1)<1e-6); % Check all-pass

% DFT/FFT
X = fft(x);                          % DFT via FFT
X_centered = fftshift(X);            % Center spectrum
f = (0:N-1) * (Fs/N);               % Frequency vector

% Sampling
Ts = 1/Fs;                           % Sampling period
omega = 2*pi*F/Fs;                   % Digital frequency
F_alias = F - 2*(F - Fs/2);         % Aliased frequency

% Analog filters (for AA)
[b, a] = butter(n, Wn, 's');        % Analog Butterworth
H = freqs(b, a, Omega);              % Analog frequency response
```

---

## Verification Against Exams

**Week 5 concepts appear in:**
- [[E20 Exam]]: Stable inverse systems (zero check)
- [[E22 Exam]]: All-pass filter identification
- [[E23 Exam]]: Second-order systems and ROC
- [[F24 Exam]]: Minimum phase decomposition ✓✓
- [[F25 Exam]]: Minimum phase systems

**Week 6 (DFT) appears in:**
- All exams: FFT spectrum computation
- [[F24 Exam]]: DFT with zero-padding
- [[E23 Exam]]: Frequency resolution

**Week 7 (Sampling) appears in:**
- [[F24 Exam]] Problem 2: Nyquist, aliasing, AA-filter design ✓
- [[E23 Exam]] Problem 3: Sampling criterion with spectral plots ✓
- Multiple exams: Frequency conversion

---

**See also:**
- [[Week 1-4]] - Foundation concepts
- [[Week 8-11]] - Filter structures and design
- [[Week 12-13]] - Multirate DSP
- [[DSP-Bible]] - Complete MATLAB reference

---
