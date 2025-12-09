# DTU 62743 DSP Formula Sheet: Weeks 12-13 (Lars)
**Multirate DSP & Exam Review - Strict adherence to DTU course materials (E19-F25)**

---

## **Week 12 - Multirate Digital Signal Processing**

### **12.1 Decimation (Down-sampling)** [Uge 12 Tirsdag]

**Definition:**
Reduce sampling rate by integer factor $M$

**Discrete-time relation:**
$$x_D[n] = x[Mn]$$

Keep every $M$-th sample, discard others

**Frequency domain effect:**
- Spectrum **compresses by factor M**
- Spectrum **replicates** at intervals of $\frac{2\pi}{M}$
- **ALIASING occurs** if signal energy exists above new Nyquist frequency

**New sampling frequency:**
$$F_s' = \frac{F_s}{M}$$

**New Nyquist frequency:**
$$F_{\max}' = \frac{F_s'}{2} = \frac{F_s}{2M}$$

**Example:**
- Original: $F_s = 8000$ Hz, Nyquist = 4000 Hz
- Decimate by $M = 2$
- New: $F_s' = 4000$ Hz, Nyquist' = 2000 Hz
- **Any frequency component above 2000 Hz will alias!**

### **12.2 Anti-Aliasing (AA) Filter Before Decimation** [Uge 12]

**Purpose:**
Remove frequency content above new Nyquist frequency **BEFORE** decimation

**Requirements:**
- **Passband:** $0 \leq F \leq F_{\text{pass}}$ (preserve desired content)
- **Transition:** $F_{\text{pass}} < F < F_{\text{stop}}$
- **Stopband:** $F_{\text{stop}} \leq F \leq \frac{F_s}{2}$ (must attenuate)

**Critical constraint:**
$$F_{\text{stop}} \leq \frac{F_s'}{2} = \frac{F_s}{2M}$$

**Design approach (FIR LP):**
1. Choose cutoff: $\omega_c = 2\pi F_c/F_s$ where $F_c < F_s/(2M)$
2. Design FIR lowpass (windowing method)
3. Apply filter: $x_{\text{filtered}}[n] = x[n] * h_{\text{AA}}[n]$
4. Then decimate: $x_D[n] = x_{\text{filtered}}[Mn]$

**MATLAB:**
```matlab
% Design AA filter
Fc = Fs/(2*M) - transition_width;      % Cutoff below new Nyquist
wc = 2*pi*Fc/Fs;
h_AA = fir1(M_order, Fc/(Fs/2), hamming(M_order+1));

% Filter then decimate
x_filtered = filter(h_AA, 1, x);
x_decimated = x_filtered(1:M:end);     % Keep every M-th sample

% Or use decimate() which does both
x_decimated = decimate(x, M);          % Uses Chebyshev AA filter
```

### **12.3 Spectrum After Decimation**

**Original spectrum:** $X(e^{j\omega})$, $\omega \in [-\pi, \pi]$

**After decimation by M:**
$$X_D(e^{j\omega}) = \frac{1}{M}\sum_{k=0}^{M-1} X\left(e^{j(\omega - 2\pi k)/M}\right)$$

**In frequency (Hz):**
- Original peaks at $F_1, F_2, \ldots$
- After decimation: peaks remain but spectrum compressed
- If $F_i > F_s'/(2) = F_s/(2M)$, then $F_i$ aliases to:
  $$F_{i,\text{alias}} = \left|F_i - k\frac{F_s}{M}\right|$$
  for appropriate integer $k$

**Example from Uge 12 Tirsdag:**
- Signal: $F_1 = 1000$ Hz, $F_2 = 3500$ Hz
- Original $F_s = 8000$ Hz
- Decimate by $M = 2$ → $F_s' = 4000$ Hz, Nyquist' = 2000 Hz
- $F_1 = 1000$ Hz < 2000 Hz ✓ (no aliasing)
- $F_2 = 3500$ Hz > 2000 Hz ✗ (ALIASES!)
- $F_{2,\text{alias}} = |3500 - 4000| = 500$ Hz

### **12.4 Interpolation (Up-sampling)** [Uge 12]

**Definition:**
Increase sampling rate by integer factor $L$

**Zero-insertion:**
$$x_{\uparrow L}[n] = \begin{cases}
x[n/L], & n = 0, \pm L, \pm 2L, \ldots \\
0, & \text{otherwise}
\end{cases}$$

**Or in MATLAB:**
```matlab
x_upsampled = zeros(1, L*length(x));
x_upsampled(1:L:end) = x;
```

**New sampling frequency:**
$$F_s^{(U)} = L \cdot F_s$$

**Frequency domain effect:**
- Spectrum **expands by factor L**
- Original spectrum now occupies $[0, 2\pi/L]$
- **Images appear** at $k\frac{2\pi}{L}$ for $k = 1, 2, \ldots, L-1$

### **12.5 Interpolation (Reconstruction) Filter** [Uge 12]

**Purpose:**
- Remove the $(L-1)$ spectral images created by zero-insertion
- Smooth the signal (fill in zeros)

**Requirements:**
- **Lowpass filter** with cutoff $\omega_c = \pi/L$
- **🚨 CRITICAL: Gain = L** to compensate amplitude scaling
- **Linear phase** (FIR) to preserve waveform

**⚠️ INTERPOLATION GAIN WARNING [Uge 12 Lecture Slides] ⚠️**
After zero-insertion (upsampling), the signal amplitude is reduced by factor $L$.
**You MUST use a gain of L in the interpolation filter**, otherwise:
- Energy loss of $1/L$
- Wrong output amplitude
- **Exam mistake:** Using gain = 1 → incorrect result!

**Why gain = L?**
Zero-insertion spreads the energy over L samples, so the filter must amplify by L to restore correct amplitude.

**Ideal interpolation filter:**
$$h_{\text{interp}}[n] = \begin{cases}
L \cdot \dfrac{\sin(\pi n/L)}{\pi n}, & n \neq 0 \\
1, & n = 0
\end{cases}$$

**Practical design:**
```matlab
% Design reconstruction LP filter
Fc = Fs/(2*L);                         % New cutoff
wc = 2*pi*Fc/Fs_new;
h_interp = L * fir1(M, Fc/(Fs_new/2), hamming(M+1));

% Apply after zero-insertion
x_interpolated = filter(h_interp, 1, x_upsampled);
```

**Or use built-in:**
```matlab
x_interpolated = interp(x, L);         % Zero-insert + LP filter
```

### **12.6 Polyphase Implementation** [Advanced - E24]

**Concept:**
Efficient decimation/interpolation by avoiding computation on zero samples

**Decimation:**
Instead of: Filter → Decimate
Do: Polyphase decomposition → compute only needed samples

**Computational savings:**
- Standard: $N_{\text{taps}}$ multiplies per input sample
- Polyphase: $N_{\text{taps}}/M$ multiplies per output sample

**Not typically required in basic exam problems**, but good to know

### **12.7 Combined Decimation & Interpolation** [Uge 12]

**Rational resampling by $L/M$:**

**Method 1 (inefficient):**
1. Interpolate by $L$
2. Then decimate by $M$
3. Final rate: $F_s' = (L/M) F_s$

**Method 2 (efficient - polyphase):**
- Combine filters before processing
- Significant computational savings

**MATLAB:**
```matlab
% Simple method
x_resampled = decimate(interp(x, L), M);

% Efficient method
x_resampled = resample(x, L, M);       % Uses polyphase
```

---

## **12.8 Bandpass Sampling (Under-sampling)** [Uge 12 Torsdag, E23]

### **Concept**
Sample a **bandpass signal** at rate **BELOW** standard Nyquist rate of $2F_{\max}$

**Requirements:**
- Signal is band-limited to $[F_L, F_H]$
- Bandwidth: $B = F_H - F_L$
- Can use $F_s \geq 2B$ instead of $F_s \geq 2F_H$!

### **Theory**

**Standard Nyquist (lowpass):**
$$F_s \geq 2F_{\max}$$

**Bandpass sampling (under-sampling):**
$$F_s \geq 2B$$

**Plus integer band positioning constraint:**
$$\frac{2F_H}{k} \leq F_s \leq \frac{2F_L}{k-1}$$

for positive integer $k$

**Maximum $k$:**
$$k_{\max} = \left\lfloor \frac{F_H}{B} \right\rfloor$$

**🚨 CRITICAL: Spectrum Inversion Rule [Uge 12 Torsdag] 🚨**

**Define:**
$$m = \frac{F_H}{B}$$

**Spectrum orientation after sampling:**
- If $m$ is **ODD** → Spectrum is **INVERTED** (flipped/reverted)
- If $m$ is **EVEN** → Spectrum is **NORMAL** (not inverted)

**Why this matters:**
When the spectrum inverts, upper sideband becomes lower sideband and vice versa. This affects demodulation!

**Example check:**
For $F_H = 17$ kHz, $B = 2$ kHz:
$$m = \frac{17}{2} = 8.5$$

$m$ is not an integer, so use $k = \lfloor m \rfloor = 8$ for calculations.

**If using $F_s = 2B$:**
When $m$ is an integer AND $F_s = 2B$, this is a valid sampling rate.
Check if $m$ is odd/even to determine if spectrum inverts.

### **Example from Uge 12 Torsdag**

**AM modulated signal:**
$$x_a(t) = \cos(2\pi F_{\text{data}} t)\cos(2\pi F_{\text{carrier}} t)$$

With:
- $F_{\text{data}} = 1$ kHz
- $F_{\text{carrier}} = 16$ kHz

**Frequency expansion:**
$$x_a(t) = \frac{1}{2}\cos(2\pi 15\text{ kHz} \cdot t) + \frac{1}{2}\cos(2\pi 17\text{ kHz} \cdot t)$$

**Band:**
- $F_L = 15$ kHz
- $F_H = 17$ kHz
- $B = 2$ kHz

**Standard Nyquist:**
$$F_s \geq 2 \times 17 = 34 \text{ kHz}$$

**Bandpass sampling:**
$$F_s \geq 2B = 4 \text{ kHz}$$

**Much lower sampling rate possible!**

**Integer band positioning:**
$$k_{\max} = \left\lfloor \frac{17}{2} \right\rfloor = 8$$

For $k=1$: $34 \leq F_s \leq 30$ (impossible)
For $k=2$: $17 \leq F_s \leq 15$ (impossible)
For $k=3$: $11.33 \leq F_s \leq 10$ (impossible)
...
For $k=8$: $4.25 \leq F_s \leq 3.75$ (impossible)

**Need to check valid ranges carefully!**

### **Aliasing in Bandpass Sampling**

**After sampling at $F_s$:**
- Baseband replica appears at $[0, B]$
- Original band $[F_L, F_H]$ folds down
- Proper choice of $F_s$ places replica correctly

**Frequency of baseband replica:**
$$F_{\text{base}} = \left|F_c - k\frac{F_s}{2}\right|$$

where $k$ is chosen to minimize $F_{\text{base}}$

---

## **Week 13 - Exam Review & Mixed Exercises**

### **13.1 Complete Highpass Filter Design** [Uge 13 Tirsdag]

**Two approaches:**

#### **Approach 1: FIR Highpass (Fourier Transform Method)**

**Step 1: Ideal impulse response**
$$h_{\text{HP,ideal}}[n] = \delta[n] - h_{\text{LP,ideal}}[n]$$

where
$$h_{\text{LP,ideal}}[n] = \begin{cases}
\dfrac{\sin(\omega_c n)}{\pi n}, & n \neq 0 \\
\dfrac{\omega_c}{\pi}, & n = 0
\end{cases}$$

**Step 2: Truncate to $N_{\text{taps}}$ samples**

**Step 3: Make causal (shift by $K = M/2$)**

**Step 4: Apply window (Hamming/Blackman)**

**Step 5: Verify frequency response**

#### **Approach 2: IIR Highpass (Bilinear Transform)**

**Step 1: Digital specs → angular frequencies**
$$\omega_p = 2\pi f_p/F_s$$

**Step 2: PREWARP to analog domain**
$$\Omega_p = \frac{2}{T_s}\tan\left(\frac{\omega_p}{2}\right)$$

**Step 3: Design Butterworth LP prototype**
$$n \geq \frac{A_s - A_p}{20\log_{10}(\Omega_s/\Omega_p)}$$

**Step 4: LP→HP transformation**
$$s \rightarrow \frac{\Omega_p}{s}$$

**Step 5: Apply BLT**
$$s = \frac{2}{T_s}\frac{z-1}{z+1}$$

**Step 6: Extract coefficients and difference equation**

### **13.2 Key Comparisons**

#### **FIR vs IIR Highpass**

| Feature            | FIR HP                       | IIR HP                       |
|--------------------|------------------------------|------------------------------|
| Phase              | Linear (symmetric)           | Nonlinear                    |
| Order              | Higher (23-51 taps typical)  | Lower (4-8 typical)          |
| Transition         | Gradual (controlled by taps) | Sharp (order-dependent)      |
| Stability          | Always stable                | Must check poles             |
| Design effort      | Straightforward              | More complex (prewarp!)      |
| Computation        | More multiplies              | Fewer multiplies             |
| Stopband ripple    | Controlled by window         | Monotonic (Butterworth)      |

#### **Window Comparison**

| Window      | Main Lobe | Stopband Atten | Use Case                     |
|-------------|-----------|----------------|------------------------------|
| Rectangular | 4π/M      | -13 dB         | Sharp transition, high ripple|
| **Hanning** | 8π/M      | -32 dB         | **Most frequent** [E20,E22,F24]|
| Hamming     | 8π/M      | -43 dB         | Textbook standard, Mock Exam |
| Blackman    | 12π/M     | -58 dB         | Best stopband [E19]          |

### **13.3 Mixed Design Problem Strategy**

**Given a filtering requirement, choose:**

**Use FIR when:**
- Linear phase is critical (audio, communications)
- Stability must be guaranteed
- Can afford higher computational cost

**Use IIR when:**
- Sharp transition required
- Computational efficiency critical
- Phase distortion acceptable

**For multirate systems:**
- Use FIR for AA and interpolation filters (stability + linear phase)
- Can use IIR for sharp pre-filters if phase OK

### **13.4 Systematic Problem-Solving Checklist**

#### **For ANY Filter Design Problem:**

1. ☐ Identify filter type (LP, HP, BP, BS)
2. ☐ Identify design method (FIR or IIR)
3. ☐ Convert all frequencies to proper units
4. ☐ **If IIR: PREWARP IMMEDIATELY**
5. ☐ Design using appropriate method
6. ☐ Verify with freqz() plot
7. ☐ Check specifications are met
8. ☐ Extract difference equation if requested

#### **For Multirate Problems:**

1. ☐ Calculate new sampling frequency: $F_s' = F_s/M$ or $F_s' = LF_s$
2. ☐ Calculate new Nyquist: $F_{\max}' = F_s'/2$
3. ☐ Check for aliasing: any components > $F_{\max}'$?
4. ☐ Design AA filter (decimation) or interpolation filter
5. ☐ Determine aliased frequencies if applicable
6. ☐ Draw spectrum before and after operation

#### **For Filter Structure Problems:**

1. ☐ Count total delays
   - Direct Form I: $M + N$
   - Direct Form II: $\max(M, N)$
2. ☐ Identify feedback (IIR) vs no feedback (FIR)
3. ☐ Extract coefficients from diagram
4. ☐ Write transfer function $H(z)$
5. ☐ Write difference equation

---

## **Comprehensive Exam Strategy**

### **Top 10 Most Tested Concepts (E19-F25)**

1. **BLT Prewarping** [E23, F24, F21] - ALWAYS do this!
2. **Aliasing formula** $F_{\text{alias}} = F - 2(F - F_s/2)$ [F24]
3. **Ideal filter impulse responses** (sinc functions) [E19, E20, Uge 11]
4. **Filter structure identification** (Direct Form I/II) [E22, F25]
5. **Window trade-offs** (Hanning most common in E20, E22, F24) [See Week 11 sheet]
6. **Decimation AA filter design** [Uge 12]
7. **Linear phase from symmetry** [E23]
8. **LP→HP transformation** [E23, Uge 13]
9. **Butterworth order calculation** [E23, F21]
10. **Step→impulse conversion** $h[n] = y_{\text{step}}[n] - y_{\text{step}}[n-1]$ [E23, F24]

### **Formula Quick Reference Sheet**

**Frequency Conversions:**
$$\omega = 2\pi\frac{F}{F_s}, \quad \Omega = 2\pi F, \quad \Omega = \frac{2}{T_s}\tan\left(\frac{\omega}{2}\right)$$

**Sampling:**
$$F_s \geq 2F_{\max}, \quad F_{\text{alias}} = F - 2(F - F_s/2)$$

**Ideal Filters:**
$$h_{\text{LP}}[n] = \frac{\sin(\omega_c n)}{\pi n}, \quad h_{\text{HP}}[n] = \delta[n] - h_{\text{LP}}[n]$$

**Windows:**
$$w_{\text{Hamming}}[n] = 0.54 - 0.46\cos\left(\frac{2\pi n}{M}\right)$$

**IIR Design:**
$$n_{\text{Butterworth}} \geq \frac{A_s - A_p}{20\log_{10}(\Omega_s/\Omega_p)}$$

**Multirate:**
$$F_s' = \frac{F_s}{M} \text{ (decimation)}, \quad F_s' = LF_s \text{ (interpolation)}$$
$$\text{Interpolation filter gain = } L \text{ (CRITICAL!)}$$
$$m = F_H/B \text{ (odd } m \text{ → spectrum inverts)}$$

**Filter Structures:**
- Direct Form I delays: $M + N$
- Direct Form II delays: $\max(M, N)$

### **Common Exam Mistakes (Learn from Others!)**

1. ❌ **Skipping prewarping in IIR design** → Filter won't meet specs!
2. ❌ **Forgetting factor of 2 in aliasing formula** → Wrong aliased frequency
3. ❌ **Not making FIR causal** (forgetting shift by K) → Non-causal filter
4. ❌ **Wrong window formula** (mixing Hamming/Hanning) → Wrong attenuation
   - Hamming: ~-53 dB stopband (often cited as >50 dB)
   - Hanning: ~-44 dB stopband  
   - Blackman: ~-74 dB stopband
   - **Check exam carefully which window is specified!**
5. ❌ **Confusing $\omega$ and $\Omega$** → Unit errors
6. ❌ **Not checking Nyquist before decimation** → Unexpected aliasing
7. ❌ **Counting wrong delays in structures** → Incorrect answer
8. ❌ **Forgetting gain L in interpolation filter** → Amplitude scaling error
9. ❌ **Using rectangular window by default** → High stopband ripple
10. ❌ **Not verifying specs with freqz** → Design doesn't meet requirements

### **Time Management Tips**

**Typical exam structure (3 hours, 100 points):**
- Problem 1: ~25 points (usually z-domain/DTFT)
- Problem 2: ~25 points (usually sampling/aliasing/AA filter)
- Problem 3: ~25 points (usually IIR or FIR design)
- Problem 4: ~25 points (usually filter structures or multirate)

**Suggested allocation:**
- 40 minutes per problem
- 10 minutes reading/planning
- 10 minutes final checks

**If stuck:**
- Skip to next sub-question
- Write what you know (partial credit!)
- Come back if time permits

### **MATLAB Exam Sanity Checks**

```matlab
% Always verify your design meets specs!

%% Check 1: Stability (IIR only)
poles = roots(a);
if all(abs(poles) < 1)
    disp('✓ Filter is stable');
else
    disp('✗ UNSTABLE - check your design!');
end

%% Check 2: Passband attenuation
[H, f] = freqz(b, a, 2048, Fs);
Hp_mag = interp1(f, abs(H), Fp);
Hp_dB = 20*log10(Hp_mag);
fprintf('Passband atten at %.1f Hz: %.2f dB (spec: ≤ %.1f dB)\n', ...
        Fp, abs(Hp_dB), Ap);

%% Check 3: Stopband attenuation
Hs_mag = interp1(f, abs(H), Fs_stop);
Hs_dB = 20*log10(Hs_mag);
fprintf('Stopband atten at %.1f Hz: %.2f dB (spec: ≤ %.1f dB)\n', ...
        Fs_stop, abs(Hs_dB), As);

%% Check 4: Linear phase (FIR only)
if all(abs(b - fliplr(b)) < 1e-10)
    disp('✓ Symmetric coefficients → Linear phase');
else
    disp('✗ Not symmetric');
end

%% Check 5: Decimation - aliasing check
F_new_Nyquist = Fs / (2*M);
fprintf('New Nyquist after decimation: %.1f Hz\n', F_new_Nyquist);
% Check if any signal components exceed this!
```

### **Final Pre-Exam Checklist**

**Formulas memorized:**
- ☐ BLT prewarping: $\Omega = \frac{2}{T_s}\tan(\omega/2)$
- ☐ Aliasing: $F_{\text{alias}} = F - 2(F - F_s/2)$
- ☐ Ideal LP: $h[n] = \sin(\omega_c n)/(\pi n)$
- ☐ Hamming: $w[n] = 0.54 - 0.46\cos(2\pi n/M)$

**MATLAB ready:**
- ☐ Know how to use: `buttord`, `butter`, `bilinear`
- ☐ Know how to use: `fir1` with window
- ☐ Know how to use: `freqz`, `filter`
- ☐ Know how to use: `decimate`, `interp`
- ☐ Can plot magnitude response in dB

**Concepts clear:**
- ☐ When to use FIR vs IIR
- ☐ Window trade-offs (Hanning most frequent in recent exams: E20, E22, F24)
- ☐ Direct Form I vs II delay counts
- ☐ Why prewarping is necessary (frequency mapping nonlinear)
- ☐ How decimation causes aliasing

**Practice problems done:**
- ☐ At least 2 IIR design problems (with prewarping!)
- ☐ At least 2 FIR design problems (with windowing)
- ☐ At least 1 multirate problem (decimation + AA filter)
- ☐ At least 1 filter structure problem (identifying forms)

---
