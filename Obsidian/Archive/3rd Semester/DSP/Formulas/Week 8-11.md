---
course: "62743"
course-name: "Digital Signal Processing"
type: formula
date: 2025-12-10
tags:
  - DSP
  - formula
  - weeks-8-11
---
# DTU 62743 DSP Formula Sheet: Weeks 8-11 (Lars)

**Filter Structures & FIR/IIR Design**  
**Strict adherence to DTU course materials (E19-F25 exam solutions)**

---

## 📋 Table of Contents

### Weeks 8-9: Digital Filter Structures

- [[#8.1 Basic Concepts]]
- [[#8.2 Direct Form I]]
- [[#8.3 Extracting Transfer Function from Block Diagram]]
- [[#8.4 Direct Form II (Canonical)]]
- [[#8.5 Cascade Form]]
- [[#8.6 Parallel Form]]
- [[#8.7 MATLAB Filter Implementation]]

### Week 10: IIR Filter Design (Butterworth, BLT)

- [[#10.1 IIR Design Overview]]
- [[#10.2 Bilinear Transform (BLT)]]
- [[#10.3 Frequency Prewarping]]
- [[#10.4 Butterworth Prototype]]
- [[#10.5 Analog Frequency Transformations]]
- [[#10.6 Complete BLT Design Workflow]]
- [[#10.7 Chebyshev Type I Filters]]

### Week 11: FIR Filter Design

- [[#11.1 FIR vs IIR Comparison]]
- [[#11.2 FIR Design by Windowing]]
- [[#11.3 Window Functions]]
- [[#11.4 FIR Design by Frequency Sampling]]
- [[#11.5 Linear Phase FIR]]

---

## Weeks 8-9 - Digital Filter Structures

### Overview

Digital filters can be implemented in different structural forms. The choice affects:

- Memory requirements (number of delays)
- Numerical precision (quantization effects)
- Computational efficiency
- Hardware/software complexity

**Course schedule:**

- **Week 8** (Lars): Digital Filter Structures (Parts 1-2/3)
- **Week 9** (Lars): Digital Filter Structures (Part 3/3)

These weeks cover the fundamental realization structures tested heavily in exams [[E21 Exam]], [[E22 Exam]], [[F25 Exam]].

---

### 8.1 Basic Concepts

**Transfer Function:** $$H(z) = \frac{Y(z)}{X(z)} = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + a_2 z^{-2} + \cdots + a_N z^{-N}}$$

**Difference Equation:** $$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$$

**Key distinction:**

- **FIR (Finite Impulse Response):** No feedback ($a_k = 0$ for all $k > 0$)
- **IIR (Infinite Impulse Response):** Has feedback ($a_k \neq 0$ for some $k > 0$)

---

### 8.2 Direct Form I [[E22 Exam]], [[F25 Exam]], [[E21 Exam]]

**Block diagram:**

```
x[n] → [FIR Section] → + → y[n]
              ↓         ↑
          [Delay]   [IIR Feedback]
```

**Structure:**

- **Two separate delay lines**
- FIR (feedforward) section: $\sum b_k x[n-k]$
- IIR (feedback) section: $-\sum a_k y[n-k]$

**Characteristics:**

- Total delays: $M + N$ (where $M$ = numerator order, $N$ = denominator order)
- Easy to implement from difference equation
- More memory usage than Direct Form II

**Transfer function:** $$H(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}}$$

**Difference equation:** $$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{k=1}^{N} a_k y[n-k]$$

**Example from** [[E22 Exam]]:

- Filter with $M=3, N=3$
- Requires 6 delay elements total
- FIR path: $b_0 x[n] + b_1 x[n-1] + b_2 x[n-2] + b_3 x[n-3]$
- IIR path: $-a_1 y[n-1] - a_2 y[n-2] - a_3 y[n-3]$

### 8.3 Extracting Transfer Function from Block Diagram [CRITICAL - [[E22 Exam]], [[F25 Exam]], [[E21 Exam]]]

**This is heavily tested! You MUST know how to:**

**Step 1: Identify the structure**

- Look for feedback loops → IIR (Direct Form I or II)
- No feedback → FIR
- Count delay blocks

**Step 2: Read coefficients from diagram**

- Multiplier blocks (triangles/gains) → filter coefficients
- Feedforward path (x[n] to output) → $b_k$ coefficients
- Feedback path (y[n] back to input) → $-a_k$ coefficients
    - **IMPORTANT:** Signs in diagram are usually negated!

**Step 3: Write transfer function** $$H(z) = \frac{b_0 + b_1 z^{-1} + \cdots + b_M z^{-M}}{1 + a_1 z^{-1} + \cdots + a_N z^{-N}}$$

**Example from** [[E22 Exam]] (Filter 3):

```
Given diagram shows:
- Feedforward: 0.7772, -2.3317, 2.3317, -0.7772
- Feedback: 2.4986, -2.1153, 0.6041
```

**Extract coefficients:**

- $b_0 = 0.7772$, $b_1 = -2.3317$, $b_2 = 2.3317$, $b_3 = -0.7772$
- $a_1 = -2.4986$, $a_2 = 2.1153$, $a_3 = -0.6041$ (note sign flip!)

**Transfer function:** $$H(z) = \frac{0.7772 - 2.3317z^{-1} + 2.3317z^{-2} - 0.7772z^{-3}}{1 - 2.4986z^{-1} + 2.1153z^{-2} - 0.6041z^{-3}}$$

### 8.4 Direct Form II (Canonical) [[E22 Exam]], [[F25 Exam]]

**Block diagram:**

```
x[n] → [IIR Section] → w[n] → [FIR Section] → y[n]
```

**Structure:**

- **Single shared delay line** (canonical form)
- IIR section processes first: $w[n] = x[n] - \sum a_k w[n-k]$
- FIR section processes second: $y[n] = \sum b_k w[n-k]$

**Characteristics:**

- Total delays: $\max(M, N)$ (minimum possible)
- More memory-efficient than Direct Form I
- Standard in MATLAB `filter()` function
- Also called "Direct Form II Transposed" when signal flow reversed

**State variable:** $w[n]$ is the intermediate signal

**How to identify Direct Form II:**

- Look for **intermediate node $w[n]$** (not visible at output)
- Feedback connects to **same delay line** as feedforward
- **Single delay chain** shared by both paths

**Example from** [[E22 Exam]]:

- Same $M=3, N=3$ filter now requires only 3 delays
- Memory saving: 50% reduction compared to Direct Form I

**MATLAB implementation:**

```matlab
% Direct Form II is the default in filter()
y = filter(b, a, x);
```

### 8.5 Cascade Form [[E21 Exam]]

**Concept:** Factor $H(z)$ into product of second-order sections (SOS):

$$H(z) = G \prod_{k=1}^{K} H_k(z)$$

where each $H_k(z)$ is a biquad (second-order):

$$H_k(z) = \frac{b_{0k} + b_{1k} z^{-1} + b_{2k} z^{-2}}{1 + a_{1k} z^{-1} + a_{2k} z^{-2}}$$

**Advantages:**

- Better numerical properties (reduced quantization errors)
- Each section can be scaled independently
- Easier to implement in fixed-point arithmetic

**Design procedure:**

1. Find poles and zeros of $H(z)$
2. Pair complex conjugate poles together
3. Pair complex conjugate zeros together
4. Match pole/zero pairs to minimize interaction
5. Implement as series connection

**Example from** [[E21 Exam]] Problem 4:

Given two cascaded systems: $$H_1(z) = \frac{1 + 2z^{-1}}{1 + 0.5z^{-1}}$$ $$H_2(z) = \frac{1 - z^{-1}}{1 - 0.25z^{-1}}$$

Total transfer function: $$H(z) = H_1(z) \cdot H_2(z) = \frac{(1 + 2z^{-1})(1 - z^{-1})}{(1 + 0.5z^{-1})(1 - 0.25z^{-1})}$$

Expand: $$H(z) = \frac{1 + z^{-1} - 2z^{-2}}{1 + 0.25z^{-1} - 0.125z^{-2}}$$

**Difference equation:** $$y[n] = -0.25y[n-1] + 0.125y[n-2] + x[n] + x[n-1] - 2x[n-2]$$

### 8.6 Parallel Form

**Concept:** Use partial fraction expansion to express $H(z)$ as sum:

$$H(z) = C + \sum_{k=1}^{K} \frac{A_k}{1 - p_k z^{-1}}$$

**Advantages:**

- Parallel computation possible
- Failure of one section doesn't completely fail the filter
- Easy to modify individual resonances

**MATLAB:**

```matlab
[r, p, k] = residue(b, a);
% r = residues (numerators)
% p = poles
% k = direct term
```

**Design notes:**

- Use for filters with well-separated poles
- Each path is a first-order section
- Combine complex conjugate pairs into second-order real sections

### 8.7 MATLAB Filter Implementation

**Apply filter (Direct Form II default):**

```matlab
y = filter(b, a, x);
```

**Design and apply in cascade (SOS format):**

```matlab
[sos, g] = tf2sos(b, a);  % Convert to second-order sections
y = sosfilt(sos, x);       % Filter using cascade
```

**Visualize filter structure:**

```matlab
fvtool(b, a);              % Filter Visualization Tool
```

---

## Week 10 - IIR Filter Design

### 10.1 IIR Design Overview

**IIR (Infinite Impulse Response) filters:**

- Designed from analog prototypes (Butterworth, Chebyshev, Elliptic)
- Sharp transitions with lower order than FIR
- Non-linear phase (group delay varies with frequency)
- May be unstable if not designed carefully

**Design workflow:**

1. **Prewarping:** Digital specs → Analog specs
2. **Analog prototype:** Design LP prototype filter in s-domain
3. **Frequency transformation:** LP → HP/BP/BS if needed
4. **Bilinear Transform (BLT):** Convert $H(s)$ → $H(z)$
5. **Verify:** Check magnitude response meets specs

This follows the course exactly [[Uge 10 - Tirsdag]], [[Uge 10 - Torsdag]].

### 10.2 Bilinear Transform (BLT)

**Mapping:** $$s = \frac{2}{T_s} \frac{1 - z^{-1}}{1 + z^{-1}} = \alpha \frac{1 - z^{-1}}{1 + z^{-1}}$$

where $\alpha = 2/T_s = 2F_s$ (typical choice).

**Key property:**

- Maps **entire j$\Omega$ axis** (analog) to **unit circle** (digital)
- No aliasing
- Causes **frequency warping** (non-linear mapping)

**Inverse mapping (z to s):** $$z = \frac{1 + sT_s/2}{1 - sT_s/2}$$

**MATLAB:**

```matlab
[bz, az] = bilinear(b_analog, a_analog, Fs);
```

### 10.3 Frequency Prewarping [CRITICAL - **EVERY IIR EXAM PROBLEM**]

**The Problem:** BLT warps frequencies non-linearly: $$\Omega = \frac{2}{T_s} \tan\left(\frac{\omega}{2}\right) = 2F_s \tan\left(\frac{\omega}{2}\right)$$

**The Solution:** **Pre-warp** the digital frequency specs **before** designing the analog filter:

$$\boxed{\Omega_{\text{analog}} = \frac{2}{T_s} \tan\left(\frac{\omega_{\text{digital}}}{2}\right)}$$

Or in Hz: $$\boxed{\Omega_{\text{analog}} = 2F_s \tan\left(\pi \frac{F_{\text{digital}}}{F_s}\right)}$$

**Example from** [[Uge 10 - Tirsdag]]:

- Digital passband edge: $F_p = 500$ Hz
- Sampling frequency: $F_s = 2000$ Hz
- Analog passband edge: $$\Omega_p = 2 \cdot 2000 \cdot \tan\left(\pi \frac{500}{2000}\right) = 4000 \cdot \tan(\pi/4) = 4000 \text{ rad/s}$$

**EXAM WARNING:** **Forgetting prewarping is the #1 reason for failing IIR problems!**

### 10.4 Butterworth Prototype

**Magnitude-squared function:** $$|H_a(j\Omega)|^2 = \frac{1}{1 + (\Omega/\Omega_c)^{2n}}$$

**Properties:**

- **Maximally flat** passband (no ripple)
- Monotonic in both passband and stopband
- **3 dB point** at $\Omega = \Omega_c$ (cutoff frequency)

**Order determination:**

From specs $A_p$ (passband loss, dB) and $A_s$ (stopband attenuation, dB):

$$n \geq \frac{\log_{10}\left(\frac{10^{0.1A_s} - 1}{10^{0.1A_p} - 1}\right)}{2\log_{10}(\Omega_s/\Omega_p)}$$

Round up to nearest integer.

**Normalized prototype (cutoff at $\Omega_c = 1$ rad/s):**

For order $n$, poles are located at: $$s_k = e^{j\pi(2k+n-1)/(2n)}, \quad k = 1, 2, \ldots, n$$

Only use poles in **left half-plane** (stable).

**MATLAB:**

```matlab
[z, p, k] = buttap(n);      % Analog prototype poles/zeros
[b, a] = butter(n, Wn, 's'); % Directly get analog LP filter
```

**Denormalization:** Scale cutoff from 1 rad/s to $\Omega_c$: $$H(s) \bigg|_{s \to s/\Omega_c}$$

### 10.5 Analog Frequency Transformations

**LP → HP (High-Pass):** $$s \to \frac{\Omega_c^2}{s}$$

**LP → BP (Band-Pass):** $$s \to \frac{s^2 + \Omega_0^2}{B \cdot s}$$

where $\Omega_0 = \sqrt{\Omega_L \Omega_H}$ (geometric center), $B = \Omega_H - \Omega_L$ (bandwidth).

**LP → BS (Band-Stop):** $$s \to \frac{B \cdot s}{s^2 + \Omega_0^2}$$

**MATLAB:**

```matlab
[b_hp, a_hp] = lp2hp(b_lp, a_lp, Omega_c);   % LP to HP
[b_bp, a_bp] = lp2bp(b_lp, a_lp, Omega_0, B); % LP to BP
[b_bs, a_bs] = lp2bs(b_lp, a_lp, Omega_0, B); % LP to BS
```

### 10.6 Complete BLT Design Workflow [[Uge 10 - Tirsdag]]

**Example: Design digital LP Butterworth IIR filter**

**Given:**

- $F_s = 2000$ Hz
- Passband: $F_p = 500$ Hz, ripple $A_p = 3$ dB
- Stopband: $F_s = 650$ Hz, attenuation $A_s = 35$ dB

**Step 1: Prewarping** $$\Omega_p = 2F_s \tan\left(\pi \frac{F_p}{F_s}\right) = 4000 \tan(\pi/4) = 4000 \text{ rad/s}$$ $$\Omega_s = 2F_s \tan\left(\pi \frac{F_{stop}}{F_s}\right) = 4000 \tan(0.325\pi) \approx 5485 \text{ rad/s}$$

**Step 2: Determine order** $$n \geq \frac{\log_{10}((10^{3.5}-1)/(10^{0.3}-1))}{2\log_{10}(5485/4000)} \approx 5.1 \to n = 6$$

**Step 3: Design analog LP prototype**

```matlab
[b_proto, a_proto] = butter(6, 1, 's');  % Normalized (Omega_c = 1)
```

**Step 4: Denormalize to $\Omega_p$**

```matlab
[b_lp, a_lp] = lp2lp(b_proto, a_proto, Omega_p);
```

**Step 5: Apply BLT**

```matlab
[b_digital, a_digital] = bilinear(b_lp, a_lp, Fs);
```

**Step 6: Verify**

```matlab
[H, w] = freqz(b_digital, a_digital, 1024);
plot(w/(2*pi)*Fs, 20*log10(abs(H)));
```

### 10.7 Chebyshev Type I Filters [[E21 Exam]], [[E23 Exam]]

**Magnitude-squared:** $$|H_a(j\Omega)|^2 = \frac{1}{1 + \varepsilon^2 T_n^2(\Omega/\Omega_p)}$$

where $T_n(x)$ is the **Chebyshev polynomial** of order $n$.

**Properties:**

- **Equiripple** in passband (ripple magnitude = $A_p$ dB)
- Monotonic in stopband
- **Sharper transition** than Butterworth for same order

**Ripple factor:** $$\varepsilon = \sqrt{10^{0.1 A_p} - 1}$$

**Example from** [[E23 Exam]]:

- $A_p = 3$ dB
- $\varepsilon = \sqrt{10^{0.3} - 1} = \sqrt{1.9953 - 1} = 0.9976 \approx 1.000$

**Order determination:** $$n \geq \frac{\cosh^{-1}\sqrt{\frac{10^{0.1A_s}-1}{10^{0.1A_p}-1}}}{\cosh^{-1}(\Omega_s/\Omega_p)}$$

**MATLAB:**

```matlab
[b, a] = cheby1(n, Rp, Wn, 's');  % Rp = passband ripple (dB)
```

**Prototype table:** Use Appendix in exam (Chebyshev Type I coefficients for $A_p = 3$ dB)

---

## Week 11 - FIR Filter Design

### 11.1 FIR vs IIR Comparison [[FIIR & IIR]]

|Property|**FIR**|**IIR**|
|---|---|---|
|**Impulse Response**|Finite (ends after $M$ samples)|Infinite (decays)|
|**Stability**|Always stable|Can be unstable|
|**Phase**|Can be exactly linear|Generally nonlinear|
|**Design**|Windowing, freq sampling|Analog prototypes + BLT|
|**Efficiency**|Needs many taps for sharp transitions|Sharp transitions with low order|
|**Feedback**|None|Has feedback|

**When to use FIR:**

- Linear phase is critical (audio, data comms)
- Guaranteed stability required
- Symmetric impulse response desired

**When to use IIR:**

- Computational efficiency is critical
- Sharp transitions needed with low order
- Phase distortion acceptable

### 11.2 FIR Design by Windowing [[Uge 11 - Tirsdag]], [[Uge 11 - Torsdag]]

**Concept:**

1. Start with **ideal frequency response** $H_d(e^{j\omega})$ (e.g., brick-wall LP)
2. Compute **ideal impulse response** via inverse DTFT: $$h_d[n] = \frac{1}{2\pi}\int_{-\pi}^{\pi} H_d(e^{j\omega})e^{j\omega n}d\omega$$
3. **Problem:** $h_d[n]$ is infinite and non-causal
4. **Solution:**
    - Truncate to length $N$
    - Shift to make causal
    - Apply **window function** to reduce Gibbs oscillations

**Ideal LP impulse response:** $$h_{\text{LP}}[n] = \begin{cases} \frac{\omega_c}{\pi}, & n = 0 \ \frac{\sin(\omega_c n)}{\pi n}, & n \neq 0 \end{cases}$$

**FIR coefficients (causal, windowed):** $$b[n] = h_d[n-K] \cdot w[n], \quad n = 0, 1, \ldots, M$$

where:

- $M = N - 1$ (filter order)
- $K = M/2$ (delay to make causal, assuming odd $N$)
- $w[n]$ is the window function

### 11.3 Window Functions

**Rectangular Window:** $$w_{\text{rect}}[n] = 1, \quad 0 \leq n \leq M$$

- **Pros:** Narrowest main lobe (sharpest transition)
- **Cons:** High sidelobes (~-13 dB) → Gibbs oscillations

**Hamming Window:** $$w_{\text{Ham}}[n] = 0.54 - 0.46\cos\left(\frac{2\pi n}{M}\right), \quad 0 \leq n \leq M$$

- **Sidelobes:** ~-40 dB
- **Transition:** Wider than rectangular
- **Most commonly used** in exams [[E19 Exam]], [[E20 Exam]], [[E22 Exam]]

**Hanning Window:** $$w_{\text{Han}}[n] = 0.5 - 0.5\cos\left(\frac{2\pi n}{M}\right), \quad 0 \leq n \leq M$$

- **Sidelobes:** ~-31 dB
- **Slightly wider transition** than Hamming

**Blackman Window:** $$w_{\text{Blk}}[n] = 0.42 - 0.5\cos\left(\frac{2\pi n}{M}\right) + 0.08\cos\left(\frac{4\pi n}{M}\right)$$

- **Sidelobes:** ~-58 dB (best stopband)
- **Widest transition**
- Used in [[E19 Exam]], [[F23 Exam]]

**MATLAB:**

```matlab
w_rect = rectwin(M+1);
w_hamming = hamming(M+1);
w_hanning = hanning(M+1);
w_blackman = blackman(M+1);

% Apply window
h_windowed = h_ideal .* w_hamming';
```

**Exam note:** **Always check which window is specified!** Hamming ≠ Hanning ≠ Blackman

### 11.4 FIR Design by Frequency Sampling [[Uge 11 - Torsdag]]

**Concept:** Sample the desired frequency response at $N$ equally spaced points, then use inverse DFT to get FIR coefficients.

**For linear-phase Type I FIR** (odd length, symmetric): Only need to specify $K+1$ samples where $K = (N-1)/2$.

**Frequency sampling formula:** $$b[n] = \frac{1}{N}\left[H_d[0] + 2\sum_{k=1}^{K} H_d[k]\cos\left(\frac{2\pi k(n-K)}{N}\right)\right]$$

**Example from** [[Uge 11 - Torsdag]]:

Design 7-tap LP with cutoff at $\omega_c = 0.3\pi$:

- $N = 7$, $K = 3$
- Sample $H_d(e^{j\omega})$ at $\omega_k = 2\pi k/7$, $k = 0, 1, 2, 3$
- Use formula above to compute $b[0], \ldots, b[6]$

**Advantages:**

- Can specify arbitrary frequency response
- Exact match at sample frequencies

**Disadvantages:**

- Large ripple between sample points if too few samples
- Not as commonly used as windowing

### 11.5 Linear Phase FIR

**Condition for linear phase:** $$h[n] = h[M-n], \quad n = 0, 1, \ldots, M$$

(symmetric impulse response)

**Phase response:** $$\angle H(e^{j\omega}) = -\omega K$$

where $K = M/2$ is the **group delay** (constant for all frequencies).

**Why it matters:**

- No phase distortion
- All frequency components delayed by same amount
- Critical for audio and data communications

**Type I FIR** (most common):

- Odd length $N = M+1$
- Symmetric: $h[n] = h[M-n]$
- Can realize any filter type (LP, HP, BP, BS)

**Frequency response factorization:** $$H(e^{j\omega}) = e^{-j\omega K} A(\omega)$$

where $A(\omega)$ is **real-valued** amplitude function.

**Example from** [[E23 Exam]] Problem 1:

Given symmetric FIR, extract $A(\omega)$ by factoring out $e^{-j\omega K}$ and using Euler's identity.

---

## Exam Strategy for Weeks 8-11

### Most Common Question Types

**Weeks 8-9 (Structures):**

1. **Identify filter structure** from block diagram [[E22 Exam]], [[F25 Exam]]
2. **Extract $b_k$ and $a_k$ coefficients** from diagram
3. **Write transfer function $H(z)$** from coefficients
4. **Count delay elements** (Direct Form I vs II)
5. **Cascade form:** combine multiple sections [[E21 Exam]]

**Week 10 (IIR Design):**

1. **Prewarping:** digital → analog frequencies [**EVERY IIR PROBLEM**]
2. **Butterworth order determination**
3. **Chebyshev $\varepsilon$ calculation** [[E21 Exam]], [[E23 Exam]]
4. **Apply BLT:** analog $H(s)$ → digital $H(z)$
5. **Frequency transformations:** LP → HP/BP/BS

**Week 11 (FIR Design):**

1. **Window selection:** Hamming vs Hanning vs Blackman
2. **Compute windowed impulse response**
3. **Plot magnitude response** and identify sidelobes
4. **Compare window effects** on transition width
5. **Linear phase verification**

### Critical Formulas to Memorize

1. **Prewarping (BLT):** $$\Omega = 2F_s \tan\left(\pi \frac{F}{F_s}\right)$$
    
2. **Butterworth order:** $$n \geq \frac{\log_{10}((10^{0.1A_s}-1)/(10^{0.1A_p}-1))}{2\log_{10}(\Omega_s/\Omega_p)}$$
    
3. **Chebyshev ripple factor:** $$\varepsilon = \sqrt{10^{0.1A_p} - 1}$$
    
4. **Hamming window:** $$w[n] = 0.54 - 0.46\cos(2\pi n/M)$$
    
5. **Hanning window:** $$w[n] = 0.5 - 0.5\cos(2\pi n/M)$$
    
6. **Ideal LP impulse response:** $$h[n] = \frac{\sin(\omega_c n)}{\pi n}, \quad h[0] = \frac{\omega_c}{\pi}$$
    

### Common Mistakes to Avoid

1. **Forgetting prewarping** in IIR design (instant fail!)
2. **Sign errors** reading feedback coefficients from diagrams
3. **Confusing Hamming and Hanning windows**
4. **Wrong Direct Form** identification
5. **Not checking stability** after BLT (poles inside unit circle)
6. **Forgetting to shift** ideal impulse response to make causal

### MATLAB Quick Reference

```matlab
% Filter structures
y = filter(b, a, x);               % Direct Form II (default)
[sos, g] = tf2sos(b, a);           % Convert to cascade
y = sosfilt(sos, x);               % Cascade filter

% IIR design (Butterworth)
Omega_p = 2*Fs*tan(pi*Fp/Fs);      % Prewarp
[b, a] = butter(n, Omega_p, 's');  % Analog prototype
[bz, az] = bilinear(b, a, Fs);     % BLT to digital

% IIR design (Chebyshev)
eps = sqrt(10^(Ap/10) - 1);        % Ripple factor
[b, a] = cheby1(n, Ap, Omega_p, 's');
[bz, az] = bilinear(b, a, Fs);

% FIR design (windowing)
wc = 2*pi*Fc/Fs;                   % Digital cutoff
n = 0:M;
h_ideal = sin(wc*(n-M/2))./(pi*(n-M/2));
h_ideal(M/2+1) = wc/pi;            % Fix n=0 case
w = hamming(M+1)';                 % Window
b_fir = h_ideal .* w;              % Windowed FIR

% Frequency response
[H, w] = freqz(b, a, 1024);
mag_dB = 20*log10(abs(H));
phase = angle(H);

% TECHNIQUE: Automatic Cutoff Frequency Detection
% High-resolution frequency response
F_vec = linspace(0, Fs/2, 10000);      % Many points for accuracy
[H, F] = freqz(b, a, F_vec, Fs);
Mag_dB = 20*log10(abs(H));

% Find -3 dB cutoff (lowpass)
idx_3dB = find(Mag_dB >= -3, 1, 'last');  % Last point above -3 dB
F_cutoff = F(idx_3dB);

% Find stopband edge (e.g., -30 dB)
idx_stop = find(Mag_dB <= -30, 1, 'first');
F_stop = F(idx_stop);

% Visualize with markers
figure; plot(F, Mag_dB); grid on;
yline(-3, '--r', '-3 dB');
xline(F_cutoff, '--g', sprintf('%.1f Hz', F_cutoff));
```

> [!tip] Finding Cutoff Frequencies **The `find()` technique for detecting threshold crossings:**
> 
> ```matlab
> % Pattern: find(condition, N, direction)
> idx = find(Mag_dB >= -3, 1, 'last');  % Passband edge
> F_cutoff = F(idx);
> ```
> 
> **When to use `'last'` vs `'first'`:**
> 
> - **Lowpass cutoff:** `find(Mag >= -3, 1, 'last')` → end of passband
> - **Highpass cutoff:** `find(Mag >= -3, 1, 'first')` → start of passband
> - **Stopband edge:** `find(Mag <= -30, 1, 'first')` → where attenuation is sufficient
> 
> **Why high resolution matters:**
> 
> ```matlab
> F = linspace(0, Fs/2, 10000);  % GOOD: Accurate detection
> F = linspace(0, Fs/2, 512);    % BAD: May miss exact cutoff
> ```
> 
> **Complete visualization:**
> 
> ```matlab
> % Mark detected frequency on plot
> xline(F_cutoff, '--g', sprintf('%.1f Hz', F_cutoff), ...
>       'LineWidth', 1.5, 'FontSize', 12);
> 
> % Compare with specification
> xline(400, '--k', '400 Hz (spec)');
> ```
> 
> **Used in:** F25 Q4-2, E23 Q2-4, F24 Q4-3
> 
> **See:** [[Cutoff_Frequency_Detection_Technique]] for complete guide


% Verification pattern (for specifications, aliasing, stability checks)
% See: [[DSP_Verification_Template]] for complete patterns
```matlab
fprintf('\n=== [What Checking] ===\n');
fprintf('Criterion: [threshold]\n\n');
for i = 1:N
    fprintf('[Item]: %.2f\n', value);
    if value [OPERATOR] threshold
        fprintf('  %.2f [OP] %.2f → PASS ✓\n\n', value, threshold);
    else
        fprintf('  %.2f [OP] %.2f → FAIL ✗\n\n', value, threshold);
    end
end
```

---

## Verification Against Exams

**Filter structures appear in:**

- [[E21 Exam]] Q4: Cascade form ✓
- [[E22 Exam]] Q2: Direct Form I/II identification ✓
- [[F25 Exam]] Q4: Direct Form I diagram ✓

**IIR design (BLT) appears in:**

- [[E21 Exam]] Q2: Chebyshev LP design ✓
- [[E23 Exam]] Q2: Chebyshev HP design ✓
- [[F24 Exam]] Q4: Butterworth BS design ✓
- [[F25 Exam]] Q2: Butterworth HP design ✓

**FIR design appears in:**

- [[E19 Exam]] Q2: Windowing with Blackman ✓
- [[E20 Exam]] Q4: Hanning window ✓
- [[E22 Exam]] Q4: Hamming window ✓
- [[E23 Exam]] Q4: Blackman window ✓
- [[F23 Exam]] Q4: Blackman window ✓

---

**See also:**

- [[Week 1-4]] - Foundation
- [[Week 5-7]] - Z-domain and DFT
- [[Week 12-13]] - Multirate DSP
- [[Digital_Filter_Design_IIR_Part_2]] - Additional IIR material

---