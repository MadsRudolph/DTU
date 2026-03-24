# FIR Filter Design by Windowing - Complete Guide

**Understanding window functions for FIR filter design (Week 11)**

---

## 📋 Table of Contents

- [[#Why Windowing?]]
- [[#The Core Concept]]
- [[#Step-by-Step Procedure]]
- [[#Window Function Comparison]]
- [[#How to Choose a Window]]
- [[#Trade-offs and Specifications]]
- [[#Common Exam Patterns]]
- [[#Worked Examples]]
- [[#MATLAB Implementation]]

---

## Why Windowing?

### The Fundamental Problem

**Goal:** Design a digital filter with desired frequency response $H_d(e^{j\omega})$

**The ideal filter:**
$$h_d[n] = \text{IDTFT}\{H_d(e^{j\omega})\}$$

**The problem:** 
- Ideal filters have **infinite length** impulse response
- We can only implement **finite length** filters
- Need to "truncate" the infinite sequence

**Example - Ideal Lowpass Filter:**
$$h_d[n] = \frac{\sin(\omega_c n)}{\pi n} \quad \text{for } -\infty < n < \infty$$

This goes on forever! We need to cut it off at some point.

---

## The Core Concept

### What is Windowing?

**Windowing = Multiplying the ideal impulse response by a window function**

$$h[n] = h_d[n] \cdot w[n]$$

Where:
- $h_d[n]$ = ideal (infinite) impulse response
- $w[n]$ = window function (finite length)
- $h[n]$ = actual FIR filter (finite length)

**Window function properties:**
- **Finite length:** $w[n] = 0$ for $|n| > M/2$ (or for $n < 0, n > M$)
- **Smooth taper:** Goes smoothly to zero at edges (reduces ripples)
- **Centered:** Usually symmetric around $n = M/2$

---

### Frequency Domain View

**Time domain multiplication = Frequency domain convolution**

$$H(e^{j\omega}) = \frac{1}{2\pi} \int_{-\pi}^{\pi} H_d(e^{j\theta}) W(e^{j(\omega-\theta)}) d\theta$$

**What this means:**
- Sharp transitions in $H_d$ get **smoothed out** (transition band)
- Discontinuities in $H_d$ create **ripples** in passband/stopband
- Better window = Less ripples, but wider transitions

---

### The Rectangular Window Problem

**Simplest approach: Just truncate (rectangular window)**

$$w_{\text{rect}}[n] = \begin{cases} 1 & 0 \leq n \leq M \\ 0 & \text{otherwise} \end{cases}$$

**Frequency response:**
$$W_{\text{rect}}(e^{j\omega}) = e^{-j\omega M/2} \frac{\sin(\omega(M+1)/2)}{\sin(\omega/2)}$$

**Problems with rectangular window:**
- High sidelobes in frequency domain (~-13 dB)
- Creates large **Gibbs oscillations** (ripples near cutoff)
- Ripples don't decrease as M increases
- Poor stopband attenuation

**This is why we use better windows!**

---

## Step-by-Step Procedure

### FIR Filter Design Using Windows

**Given:**
- Cutoff frequency $\omega_c$ or $f_c$
- Filter type (lowpass, highpass, bandpass)
- Filter order $M$ (or length $N = M+1$)

**Procedure:**

#### Step 1: Determine Ideal Impulse Response

**For Lowpass:**
$$h_d[n] = \frac{\omega_c}{\pi} \cdot \frac{\sin(\omega_c(n-M/2))}{\omega_c(n-M/2)} = \frac{\omega_c}{\pi} \text{sinc}(\omega_c(n-M/2))$$

**Special case:** At $n = M/2$ (center):
$$h_d[M/2] = \frac{\omega_c}{\pi}$$

**For Highpass:**
$$h_d[n] = \delta[n-M/2] - \frac{\omega_c}{\pi} \text{sinc}(\omega_c(n-M/2))$$

**For Bandpass:** (cutoffs $\omega_1, \omega_2$)
$$h_d[n] = \frac{\omega_2}{\pi} \text{sinc}(\omega_2(n-M/2)) - \frac{\omega_1}{\pi} \text{sinc}(\omega_1(n-M/2))$$

#### Step 2: Choose Window Function

Select based on specifications (see [[#How to Choose a Window]])

Common choices:
- **Hamming:** Good all-around (most common in exams)
- **Hann (Hanning):** Similar to Hamming
- **Blackman:** Best stopband, widest transition
- **Kaiser:** Adjustable trade-off (advanced)

#### Step 3: Apply Window

$$h[n] = h_d[n] \cdot w[n] \quad \text{for } n = 0, 1, 2, \ldots, M$$

**Result:** FIR filter coefficients $b = [h[0], h[1], \ldots, h[M]]$

#### Step 4: Implement Filter

$$y[n] = \sum_{k=0}^{M} h[k] x[n-k]$$

Or in MATLAB:
```matlab
y = filter(h, 1, x);
```

---

## Window Function Comparison

### Common Window Functions

#### 1. Rectangular Window

$$w[n] = \begin{cases} 1 & 0 \leq n \leq M \\ 0 & \text{otherwise} \end{cases}$$

**Properties:**
- Narrowest main lobe → Sharpest transition
- Highest sidelobes → Worst stopband attenuation (~-21 dB)
- Gibbs oscillations (ripples) don't decay

**Use when:** You need the sharpest possible transition and can tolerate ripples

---

#### 2. Hamming Window ⭐ (Most Common)

$$w[n] = 0.54 - 0.46\cos\left(\frac{2\pi n}{M}\right) \quad \text{for } 0 \leq n \leq M$$

**Properties:**
- Moderate main lobe width
- Low sidelobes (~-43 dB)
- Good stopband attenuation
- **Best general-purpose window**

**Use when:** Default choice for most applications

**MATLAB:** `hamming(M+1)`

---

#### 3. Hann (Hanning) Window

$$w[n] = 0.5 - 0.5\cos\left(\frac{2\pi n}{M}\right) = 0.5\left[1 - \cos\left(\frac{2\pi n}{M}\right)\right]$$

**Properties:**
- Similar to Hamming
- Slightly wider main lobe than Hamming
- Slightly worse sidelobes than Hamming (~-31 dB)
- Goes to zero at endpoints (Hamming doesn't)

**Use when:** Similar to Hamming, slightly smoother

**MATLAB:** `hann(M+1)` or `hanning(M+1)`

---

#### 4. Blackman Window

$$w[n] = 0.42 - 0.5\cos\left(\frac{2\pi n}{M}\right) + 0.08\cos\left(\frac{4\pi n}{M}\right)$$

**Properties:**
- Wide main lobe → Wide transition band
- Very low sidelobes (~-74 dB)
- Excellent stopband attenuation
- **Best for high attenuation requirements**

**Use when:** Need very good stopband attenuation, can accept wider transition

**MATLAB:** `blackman(M+1)`

---

#### 5. Kaiser Window (Advanced)

$$w[n] = \frac{I_0\left(\beta\sqrt{1-\left(\frac{2n-M}{M}\right)^2}\right)}{I_0(\beta)}$$

where $I_0$ is the zeroth-order modified Bessel function of the first kind.

**Properties:**
- **Adjustable parameter** $\beta$ controls trade-off
- Higher $\beta$ → Lower sidelobes, wider main lobe
- Can meet specific stopband attenuation requirements
- **Most flexible window**

**Use when:** Have specific attenuation requirements

**MATLAB:** `kaiser(M+1, beta)`

---

### Window Comparison Table

| Window | Main Lobe Width | Sidelobe Level | Stopband Atten. | Transition Width | Use Case |
|--------|----------------|----------------|-----------------|------------------|----------|
| **Rectangular** | Narrowest | -13 dB | -21 dB | Narrowest | Sharp transition, accept ripples |
| **Hamming** ⭐ | Moderate | -43 dB | -53 dB | Moderate | **General purpose (default)** |
| **Hann** | Moderate | -31 dB | -44 dB | Moderate | Similar to Hamming |
| **Blackman** | Wide | -58 dB | -74 dB | Wide | High attenuation needed |
| **Kaiser** | Adjustable | Adjustable | Adjustable | Adjustable | Specific requirements |

**Main lobe width:** How wide the transition band will be
**Sidelobe level:** Peak ripple in stopband
**Stopband attenuation:** Minimum attenuation in stopband

---

## How to Choose a Window

### Decision Tree

```
Do you have SPECIFIC attenuation requirements?
├─ YES → Use Kaiser window
│         Calculate β from As requirement
│         β ≈ 0.5842(As-21)^0.4 + 0.07886(As-21)
│
└─ NO → Go to general selection:
    
    What's your priority?
    
    ├─ SHARP TRANSITION (narrow transition band)
    │  └─ Use Rectangular (but expect ripples!)
    │
    ├─ BALANCED (good all-around)
    │  └─ Use Hamming ⭐ (DEFAULT CHOICE)
    │
    └─ HIGH ATTENUATION (very low stopband)
       └─ Use Blackman (but wider transition)
```

---

### Specification-Driven Choice

**Given filter specifications:**

1. **Stopband attenuation $A_s$:**
   - $A_s < 40$ dB → Hamming or Rectangular
   - $40 \leq A_s < 60$ dB → Hamming
   - $60 \leq A_s < 80$ dB → Blackman
   - $A_s \geq 80$ dB → Kaiser with appropriate β

2. **Transition width $\Delta\omega$:**
   - Narrow ($\Delta\omega < 0.2\pi$) → Need high order, use Hamming
   - Moderate → Hamming works well
   - Wide ($\Delta\omega > 0.4\pi$) → Can use Blackman

3. **Passband ripple $\delta_p$:**
   - Usually fixed by window choice
   - Can't independently control with basic windows
   - Use Kaiser if need specific ripple

---

### Exam Strategy

**If problem says:**
- "Design FIR filter" with no window specified → **Use Hamming**
- "Use windowing method" → **Use Hamming** (unless specified)
- "Stopband attenuation must be at least X dB" → Match window to requirement
- Gives you a window type → Use that specific window

**Default exam choice: Hamming window** ⭐

It's the best compromise between:
- Transition band width (moderate)
- Stopband attenuation (good, ~53 dB)
- Implementation simplicity (built into MATLAB)

---

## Trade-offs and Specifications

### The Fundamental Trade-off

**You cannot have both:**
- Sharp transition (narrow transition band)
- Low ripples (high stopband attenuation)

**With a fixed filter order M:**

```
Better stopband     ←→     Sharper transition
(lower ripples)            (narrow transition band)

Blackman            Hamming            Rectangular
(best attenuation)  (balanced)         (sharpest)
```

---

### Effect of Filter Order

**Increasing M (filter order):**
- ✅ **Narrows** transition band (sharper cutoff)
- ✅ **Improves** stopband attenuation slightly
- ❌ **Increases** computational cost
- ❌ **Increases** group delay (M/2 samples)

**Relationship:**
$$\Delta\omega \propto \frac{1}{M} \quad \text{(transition width decreases as M increases)}$$

**Empirical formulas for Hamming:**

Filter order estimate:
$$M \approx \frac{3.3\pi}{\Delta\omega}$$

where $\Delta\omega = \omega_s - \omega_p$ (transition width in radians/sample)

Or in Hz:
$$M \approx \frac{3.3 F_s}{\Delta F}$$

where $\Delta F = F_s - F_p$ (transition width in Hz)

---

### Design Specifications

**Typical FIR design problem:**

**Given:**
- Passband edge: $f_p$ or $\omega_p$
- Stopband edge: $f_s$ or $\omega_s$
- Passband ripple: $\delta_p$ or $A_p$ (dB)
- Stopband attenuation: $\delta_s$ or $A_s$ (dB)
- Sampling frequency: $F_s$

**Find:**
- Filter order $M$
- Window type
- Cutoff frequency $\omega_c$ (usually midpoint of transition)

**Standard approach:**

1. **Choose window** based on $A_s$
2. **Calculate order** from $\Delta\omega = \omega_s - \omega_p$
3. **Set cutoff** at $\omega_c = (\omega_p + \omega_s)/2$ (midpoint)
4. **Design filter** using windowing method

---

## Common Exam Patterns

### Pattern 1: Direct Filter Design

**Problem:** Design a lowpass FIR filter with cutoff 1000 Hz, order 50, $F_s = 8000$ Hz using Hamming window.

**Solution:**
```matlab
M = 50;                  % Order
fc = 1000;               % Cutoff [Hz]
Fs = 8000;               % Sampling [Hz]

% MATLAB does all the work!
b = fir1(M, fc/(Fs/2), 'low', hamming(M+1));
a = 1;
```

**That's it!** `fir1` handles:
- Computing ideal response $h_d[n]$
- Applying Hamming window
- Centering and normalizing

---

### Pattern 2: Meet Specifications

**Problem:** Design FIR lowpass to meet: $f_p = 2$ kHz, $f_s = 3$ kHz, $A_s \geq 50$ dB, $F_s = 10$ kHz

**Solution:**

Step 1: Choose window from $A_s = 50$ dB
→ Hamming provides ~53 dB ✓

Step 2: Calculate order from transition width
$$\Delta f = f_s - f_p = 3000 - 2000 = 1000 \text{ Hz}$$
$$M \approx \frac{3.3 \cdot F_s}{\Delta f} = \frac{3.3 \cdot 10000}{1000} = 33$$

Round up: $M = 34$ (or higher to be safe)

Step 3: Set cutoff at midpoint
$$f_c = \frac{f_p + f_s}{2} = \frac{2000 + 3000}{2} = 2500 \text{ Hz}$$

Step 4: Design
```matlab
M = 34;
fc = 2500;
Fs = 10000;
b = fir1(M, fc/(Fs/2), 'low', hamming(M+1));
```

---

### Pattern 3: Linear Phase Analysis

**Problem:** Given symmetric FIR coefficients, show filter has linear phase.

**Solution approach:**

1. **Check symmetry:** $h[k] = h[M-k]$ for all $k$

2. **Write frequency response:**
$$H(e^{j\omega}) = \sum_{n=0}^{M} h[n] e^{-j\omega n}$$

3. **Factor out center phase:**
$$H(e^{j\omega}) = e^{-j\omega M/2} \sum_{n=0}^{M} h[n] e^{-j\omega(n-M/2)}$$

4. **Use symmetry to show remaining sum is real:**

For even $M$:
$$H(e^{j\omega}) = e^{-j\omega M/2} \left[h[M/2] + 2\sum_{k=0}^{M/2-1} h[k]\cos(\omega(M/2-k))\right]$$

5. **Conclude:**
- Magnitude: $|H(e^{j\omega})| = |\text{real amplitude}|$
- Phase: $\angle H(e^{j\omega}) = -\omega M/2$ (linear!)

**This appears in almost every exam!** [[E23 Exam]] Q1, [[F23 Exam]] Q1

---

### Pattern 4: Window Comparison

**Problem:** Compare Hamming and Blackman windows for same filter order.

**Answer:**
- **Hamming:** Narrower transition, moderate attenuation (~53 dB)
- **Blackman:** Wider transition, better attenuation (~74 dB)
- **Same order M** → Blackman trades transition width for better stopband

**Plot both and observe:**
- Hamming has sharper cutoff
- Blackman has lower ripples in stopband

---

## Worked Examples

### Example 1: Basic Lowpass Design

**Design lowpass FIR filter:**
- Cutoff: 1200 Hz
- Order: 40
- Sampling: 8000 Hz
- Window: Hamming

**Solution:**
```matlab
% Given
M = 40;
fc = 1200;
Fs = 8000;

% Design using fir1
b = fir1(M, fc/(Fs/2), 'low', hamming(M+1));
a = 1;

% Check results
fprintf('Filter order: M = %d\n', M);
fprintf('Number of coefficients: %d\n', length(b));
fprintf('Filter type: FIR Lowpass\n');

% Verify linear phase (check symmetry)
is_symmetric = all(abs(b - fliplr(b)) < 1e-10);
if is_symmetric
    fprintf('✓ Filter has linear phase (symmetric coefficients)\n');
end

% Plot magnitude response
[H, f] = freqz(b, a, 1024, Fs);
figure;
plot(f, 20*log10(abs(H)));
xlabel('Frequency [Hz]');
ylabel('Magnitude [dB]');
title('FIR Lowpass - Hamming Window');
grid on;
```

**Expected results:**
- 41 coefficients (M+1)
- Symmetric (linear phase)
- -3 dB near 1200 Hz
- ~53 dB stopband attenuation

---

### Example 2: Meeting Specifications

**Design lowpass to meet:**
- $f_p = 1.5$ kHz (passband edge)
- $f_s = 2.0$ kHz (stopband edge)
- $A_s \geq 45$ dB (stopband attenuation)
- $F_s = 10$ kHz

**Solution:**

```matlab
% Step 1: Choose window from As
As = 45;  % Need at least 45 dB
% Hamming provides ~53 dB → OK!

% Step 2: Calculate order
fp = 1500; fs = 2000; Fs = 10000;
Delta_f = fs - fp;  % Transition width [Hz]

M = ceil(3.3 * Fs / Delta_f);  % Hamming formula
fprintf('Estimated order: M = %d\n', M);

% Step 3: Set cutoff at midpoint
fc = (fp + fs)/2;
fprintf('Cutoff frequency: fc = %.0f Hz\n', fc);

% Step 4: Design
b = fir1(M, fc/(Fs/2), 'low', hamming(M+1));
a = 1;

% Step 5: Verify specs
[H, f] = freqz(b, a, 10000, Fs);
Mag_dB = 20*log10(abs(H));

% Find actual -3 dB point
idx = find(Mag_dB >= -3, 1, 'last');
fc_actual = f(idx);

% Find stopband attenuation
idx_stop = find(f >= fs, 1, 'first');
As_actual = -max(Mag_dB(idx_stop:end));

fprintf('\n--- Verification ---\n');
fprintf('Measured cutoff (-3 dB): %.1f Hz\n', fc_actual);
fprintf('Stopband attenuation: %.1f dB\n', As_actual);

if As_actual >= As
    fprintf('✓ Specification met!\n');
else
    fprintf('✗ Increase M and try again\n');
end
```

---

### Example 3: Comparing Windows

**Compare Hamming vs Blackman for M = 50:**

```matlab
M = 50;
fc = 1000;
Fs = 8000;

% Design with both windows
b_hamming = fir1(M, fc/(Fs/2), 'low', hamming(M+1));
b_blackman = fir1(M, fc/(Fs/2), 'low', blackman(M+1));

% Frequency responses
[H_ham, f] = freqz(b_hamming, 1, 10000, Fs);
[H_blk, f] = freqz(b_blackman, 1, 10000, Fs);

% Plot comparison
figure;
plot(f, 20*log10(abs(H_ham)), 'b', 'DisplayName', 'Hamming');
hold on;
plot(f, 20*log10(abs(H_blk)), 'r', 'DisplayName', 'Blackman');
hold off;

xlabel('Frequency [Hz]');
ylabel('Magnitude [dB]');
title('Window Comparison: Hamming vs Blackman');
legend('Location', 'best');
grid on;
xlim([0 2000]);
ylim([-100 5]);

% Measure transition widths
% (Frequency from -3 dB to -40 dB)
idx_3dB_ham = find(20*log10(abs(H_ham)) >= -3, 1, 'last');
idx_40dB_ham = find(20*log10(abs(H_ham)) <= -40, 1, 'first');
trans_ham = f(idx_40dB_ham) - f(idx_3dB_ham);

idx_3dB_blk = find(20*log10(abs(H_blk)) >= -3, 1, 'last');
idx_40dB_blk = find(20*log10(abs(H_blk)) <= -40, 1, 'first');
trans_blk = f(idx_40dB_blk) - f(idx_3dB_blk);

fprintf('\n--- Window Comparison ---\n');
fprintf('Hamming transition width: %.1f Hz\n', trans_ham);
fprintf('Blackman transition width: %.1f Hz\n', trans_blk);
fprintf('Ratio: %.2f (Blackman is wider)\n', trans_blk/trans_ham);

% Stopband attenuation
As_ham = -min(20*log10(abs(H_ham(2000:end))));
As_blk = -min(20*log10(abs(H_blk(2000:end))));

fprintf('\nHamming stopband: %.1f dB\n', As_ham);
fprintf('Blackman stopband: %.1f dB\n', As_blk);
fprintf('Difference: %.1f dB (Blackman is better)\n', As_blk - As_ham);
```

**Expected observation:**
- Blackman has ~1.5× wider transition
- Blackman has ~20 dB better stopband attenuation

---

## MATLAB Implementation

### Using `fir1` (Recommended)

**Syntax:**
```matlab
b = fir1(M, Wn, 'ftype', window)
```

**Parameters:**
- `M`: Filter order (number of coefficients = M+1)
- `Wn`: Normalized cutoff frequency (cutoff / Nyquist)
  - For $f_c$ in Hz: `Wn = fc/(Fs/2)`
  - For $\omega_c$ in rad/sample: `Wn = wc/pi`
- `'ftype'`: Filter type
  - `'low'`: Lowpass (default)
  - `'high'`: Highpass
  - `'bandpass'`: Bandpass (Wn is 2-element vector)
  - `'stop'`: Bandstop (Wn is 2-element vector)
- `window`: Window function vector
  - `hamming(M+1)` - Hamming
  - `hann(M+1)` - Hann
  - `blackman(M+1)` - Blackman
  - `kaiser(M+1, beta)` - Kaiser

**Examples:**
```matlab
% Lowpass with Hamming (most common)
b = fir1(50, 0.25, 'low', hamming(51));

% Highpass with Blackman
b = fir1(60, 0.4, 'high', blackman(61));

% Bandpass [0.2, 0.6] with Hann
b = fir1(40, [0.2 0.6], 'bandpass', hann(41));

% Kaiser with beta = 5
b = fir1(50, 0.3, 'low', kaiser(51, 5));
```

---

### Manual Implementation (For Understanding)

**If you want to understand what `fir1` does:**

```matlab
% Manual FIR lowpass design with Hamming window

M = 50;                    % Order
wc = 0.25*pi;              % Cutoff [rad/sample]

% Step 1: Generate ideal impulse response
n = 0:M;                   % Sample indices
h_ideal = wc/pi * sinc(wc/pi * (n - M/2));

% Handle special case at center (avoids 0/0)
h_ideal(M/2 + 1) = wc/pi;  % n = M/2

% Step 2: Apply Hamming window
w = hamming(M+1)';         % Transpose to row vector
h = h_ideal .* w;          % Element-wise multiplication

% Step 3: Normalize (optional, fir1 does this)
h = h / sum(h);            % DC gain = 1

% Result: h is the FIR filter coefficients
b = h;
a = 1;
```

---

### Common MATLAB Pitfalls

**Pitfall 1: Wrong window length**
```matlab
% ❌ WRONG - window length doesn't match
b = fir1(50, 0.3, 'low', hamming(50));  % Should be 51!

% ✓ CORRECT - length must be M+1
b = fir1(50, 0.3, 'low', hamming(51));
```

**Pitfall 2: Wrong normalization**
```matlab
% ❌ WRONG - using frequency in Hz directly
fc = 1000; Fs = 8000;
b = fir1(50, fc, 'low', hamming(51));  % Wrong!

% ✓ CORRECT - normalize by Nyquist
b = fir1(50, fc/(Fs/2), 'low', hamming(51));
```

**Pitfall 3: Forgetting `a = 1`**
```matlab
% ❌ WRONG - freqz needs denominator
[H, w] = freqz(b);  % Might work but ambiguous

% ✓ CORRECT - explicitly specify a = 1
[H, w] = freqz(b, 1);  % Clear that it's FIR
```

---

## Summary - Quick Reference

### Key Concepts
1. **Windowing** = Truncating infinite ideal response with finite window
2. **Trade-off**: Sharp transition ↔ Low ripples
3. **Default choice**: Hamming window (balanced performance)
4. **Linear phase**: Guaranteed by symmetric coefficients

### Window Selection Quick Guide
```
Need sharp transition?     → Rectangular (but ripples!)
General purpose?           → Hamming ⭐ (DEFAULT)
Need high attenuation?     → Blackman
Have specific specs?       → Kaiser
```

### MATLAB Quick Start
```matlab
% Most common exam solution:
M = 50;                          % Order
fc = 1000; Fs = 8000;            % Frequencies
b = fir1(M, fc/(Fs/2), 'low', hamming(M+1));
a = 1;
```

### Order Estimation (Hamming)
$$M \approx \frac{3.3 F_s}{\Delta F} \quad \text{or} \quad M \approx \frac{3.3\pi}{\Delta\omega}$$

### Exam Red Flags
- ✅ Always normalize frequency: `fc/(Fs/2)` not `fc`
- ✅ Window length must be `M+1` not `M`
- ✅ Check linear phase by verifying symmetry
- ✅ Default to Hamming unless specified otherwise

---

**You now understand FIR windowing! Ready to tackle those exam problems!** 🎯📊
