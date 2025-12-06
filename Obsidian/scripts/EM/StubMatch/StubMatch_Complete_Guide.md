# StubMatch.m: Complete User Guide

## 📚 Table of Contents
1. [What is Stub Matching?](#what-is-stub-matching)
2. [When to Use StubMatch](#when-to-use-stubmatch)
3. [Function Syntax](#function-syntax)
4. [Input Modes](#input-modes)
5. [Output Structure](#output-structure)
6. [Step-by-Step Workflows](#step-by-step-workflows)
7. [Common Problem Types](#common-problem-types)
8. [Interpreting Results](#interpreting-results)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Topics](#advanced-topics)

---

## 🎯 What is Stub Matching?

### The Problem
You have a **load impedance** $Z_L$ that doesn't match your **transmission line** $Z_0$.

**Consequences:**
- Power is reflected (not absorbed by load)
- Standing waves form
- Reduced efficiency
- Potential damage at high power

### The Solution: Single-Stub Tuner

Add a **stub** (short section of transmission line) in **shunt** (parallel) at the right distance from the load to cancel reflections.

```
Generator ----[TL]----[Stub]----[TL(d)]----Load
              Z0      |         Z0         ZL
                     ===
```

**Two design parameters:**
1. **d** = distance from load to stub
2. **ℓ** = length of the stub

**StubMatch finds both for you automatically!**

### Why It Works

**Physics:**
1. Move distance **d** from load until admittance has real part = 1
2. Add stub with susceptance that cancels imaginary part
3. Total admittance becomes purely real (= 1/Z₀)
4. Perfect match! ✓

---

## 🔍 When to Use StubMatch

### Use StubMatch When You See:

✅ "Design a single-stub matching network"  
✅ "Match load ZL to line Z₀"  
✅ "Find stub position and length"  
✅ "Single-stub tuner"  
✅ "Quarter-wave stub" (special case)  
✅ "Short-circuited stub" or "Open-circuited stub"  

### Don't Use StubMatch For:

❌ **Double-stub** matching (different method)  
❌ **Quarter-wave transformer** matching (use `TLine('QW', ...)`)  
❌ **Lumped element** matching (L-C networks)  
❌ Just analyzing a line (use `TLine(Z0, ZL, len)`)  

### Problem Recognition Guide

| Keywords in Problem | What to Use |
|---------------------|-------------|
| "single stub", "stub tuner" | **StubMatch** |
| "double stub", "two stubs" | Manual/other method |
| "λ/4 transformer", "quarter-wave" | `TLine('QW', ...)` |
| "series/shunt L and C" | Lumped matching |
| "input impedance", "VSWR" | `TLine` analysis |

---

## 📋 Function Syntax

### Basic Form
```matlab
result = StubMatch(ZL, Z0, stub_type)
result = StubMatch(ZL, Z0, stub_type, lambda)
result = StubMatch(ZL, Z0, stub_type, freq, eps_r)
```

### Parameters

| Parameter | Type | Description | Units | Required |
|-----------|------|-------------|-------|----------|
| `ZL` | complex | Load impedance | Ω | ✓ Yes |
| `Z0` | real | Line impedance | Ω | ✓ Yes |
| `stub_type` | string | `'short'` or `'open'` | - | ✓ Yes |
| `lambda` | real | Wavelength | meters | Optional |
| `freq` | real | Frequency | Hz | Optional |
| `eps_r` | real | Relative permittivity | - | Optional |

### Return Value

Returns a **structure** with all design parameters and verification data.

---

## 🎨 Input Modes

### Mode 1: Basic (Normalized Only)
**When:** You only care about electrical lengths (in λ)

```matlab
r = StubMatch(ZL, Z0, 'short');
```

**Output:** Lengths in wavelengths only
- `r.d` = distance in λ
- `r.l` = stub length in λ

**Example:**
```matlab
ZL = 100 + 1j*50;  % Load impedance
Z0 = 50;            % Line impedance

r = StubMatch(ZL, Z0, 'short');
fprintf('d = %.4f λ\n', r.d);   % 0.1234 λ
fprintf('ℓ = %.4f λ\n', r.l);   % 0.0567 λ
```

---

### Mode 2: With Wavelength (Most Common)
**When:** You want physical lengths (mm, cm, m)

```matlab
r = StubMatch(ZL, Z0, stub_type, lambda);
```

**Requirements:**
- `lambda` must be in **meters**!

**Output:** Lengths in λ, meters, cm, and mm

**Example:**
```matlab
ZL = 100 + 1j*50;
Z0 = 50;
lambda = 0.12;      % 12 cm = 0.12 m

r = StubMatch(ZL, Z0, 'short', lambda);

% All formats available:
fprintf('d = %.4f λ = %.2f mm\n', r.d, r.d_mm);
fprintf('ℓ = %.4f λ = %.2f mm\n', r.l, r.l_mm);
```

---

### Mode 3: From Frequency (Auto-Calculate λ)
**When:** Problem gives frequency instead of wavelength

```matlab
r = StubMatch(ZL, Z0, stub_type, freq, eps_r);
```

**StubMatch automatically calculates:** $\lambda = \frac{c_0}{f\sqrt{\varepsilon_r}}$

**Example:**
```matlab
ZL = 100 + 1j*50;
Z0 = 50;
freq = 2.4e9;       % 2.4 GHz
eps_r = 2.3;        // Teflon

r = StubMatch(ZL, Z0, 'short', freq, eps_r);
% StubMatch calculates lambda = 0.0823 m automatically
```

---

### Mode 4: Open vs Short Stub
**When:** Problem specifies stub termination

```matlab
% Short-circuited stub (most common)
r = StubMatch(ZL, Z0, 'short', lambda);

% Open-circuited stub (less common)
r = StubMatch(ZL, Z0, 'open', lambda);
```

**Differences:**

| Aspect | Short Stub | Open Stub |
|--------|------------|-----------|
| Termination | Short circuit | Open circuit |
| Impedance | $Z = jZ_0\tan\beta\ell$ | $Z = -jZ_0\cot\beta\ell$ |
| Admittance | $Y = -j\cot\beta\ell / Z_0$ | $Y = j\tan\beta\ell / Z_0$ |
| Typical use | Most common | Special cases |
| Practical | Easier to make | Harder (fringing) |

---

## 📊 Output Structure

### Essential Fields (What You Usually Need)

```matlab
% SOLUTION 1 (preferred - closer to load)
r.d         % Distance load→stub (wavelengths)
r.l         % Stub length (wavelengths)
r.d_mm      % Distance in millimeters
r.l_mm      % Stub length in millimeters

% SOLUTION 2 (alternative - farther from load)
r.d_alt     % Alternative distance (wavelengths)
r.l_alt     % Alternative stub length (wavelengths)
r.d_alt_mm  % Alternative distance (mm)
r.l_alt_mm  % Alternative stub length (mm)
```

### All Available Fields

```matlab
% INPUT PARAMETERS (echo back)
r.ZL            % Load impedance (input)
r.Z0            % Line impedance (input)
r.Z0_stub       % Stub impedance (usually = Z0)
r.type          % 'short' or 'open'
r.lambda        % Wavelength in meters (if provided)

% SOLUTION 1 - All units
r.d             % Distance in λ
r.l             % Stub length in λ
r.d_m           % Distance in meters
r.l_m           % Stub length in meters
r.d_cm          % Distance in centimeters
r.l_cm          % Stub length in centimeters
r.d_mm          % Distance in millimeters
r.l_mm          % Stub length in millimeters

% SOLUTION 2 - All units
r.d_alt         % Alt distance in λ
r.l_alt         % Alt stub length in λ
r.d_alt_mm      % Alt distance in mm (if lambda given)
r.l_alt_mm      % Alt stub length in mm (if lambda given)

% VERIFICATION
r.Y_in_check    % Final admittance (should ≈ 1/Z0)
```

---

## 🔧 Step-by-Step Workflows

### Workflow 1: Basic Problem (Wavelength Given)

**Problem:** "Match ZL = 100+j50 Ω to Z₀ = 50 Ω using short stub. λ = 12 cm."

```matlab
% Step 1: Setup
ZL = 100 + 1j*50;
Z0 = 50;
lambda = 0.12;      % Convert to meters!

% Step 2: Call StubMatch
r = StubMatch(ZL, Z0, 'short', lambda);

% Step 3: Extract answers
d_mm = r.d_mm;      % Distance in mm
l_mm = r.l_mm;      % Stub length in mm

% Step 4: Display
fprintf('Distance to stub: d = %.2f mm\n', d_mm);
fprintf('Stub length: ℓ = %.2f mm\n', l_mm);
```

---

### Workflow 2: Frequency Given (Calculate λ First)

**Problem:** "Match ZL = 75+j25 Ω to Z₀ = 50 Ω at f = 2.4 GHz, εᵣ = 2.3."

**Option A: Manual λ calculation**
```matlab
% Step 1: Calculate wavelength
c0 = 2.998e8;
f = 2.4e9;
eps_r = 2.3;
lambda = c0 / (f * sqrt(eps_r));

% Step 2: Call StubMatch
ZL = 75 + 1j*25;
Z0 = 50;
r = StubMatch(ZL, Z0, 'short', lambda);

% Step 3: Results
fprintf('d = %.2f mm\n', r.d_mm);
fprintf('ℓ = %.2f mm\n', r.l_mm);
```

**Option B: Let StubMatch calculate λ**
```matlab
% Even simpler!
ZL = 75 + 1j*25;
Z0 = 50;
f = 2.4e9;
eps_r = 2.3;

r = StubMatch(ZL, Z0, 'short', f, eps_r);
fprintf('d = %.2f mm\n', r.d_mm);
fprintf('ℓ = %.2f mm\n', r.l_mm);
```

---

### Workflow 3: Need Normalized (No Physical Lengths)

**Problem:** "Find electrical lengths for stub matching."

```matlab
ZL = 100 + 1j*50;
Z0 = 50;

r = StubMatch(ZL, Z0, 'short');

% Results in wavelengths
fprintf('d = %.4f λ\n', r.d);
fprintf('ℓ = %.4f λ\n', r.l);

% Can also express in degrees
d_deg = r.d * 360;
l_deg = r.l * 360;
fprintf('d = %.1f°\n', d_deg);
fprintf('ℓ = %.1f°\n', l_deg);
```

---

### Workflow 4: Compare Both Solutions

**Problem:** "Find both stub matching solutions."

```matlab
ZL = 100 + 1j*50;
Z0 = 50;
lambda = 0.12;

r = StubMatch(ZL, Z0, 'short', lambda);

% Solution 1
fprintf('SOLUTION 1 (closer to load):\n');
fprintf('  d = %.4f λ = %.2f mm\n', r.d, r.d_mm);
fprintf('  ℓ = %.4f λ = %.2f mm\n', r.l, r.l_mm);

% Solution 2
fprintf('SOLUTION 2 (farther from load):\n');
fprintf('  d = %.4f λ = %.2f mm\n', r.d_alt, r.d_alt_mm);
fprintf('  ℓ = %.4f λ = %.2f mm\n', r.l_alt, r.l_alt_mm);

% Usually pick Solution 1 (smaller d)
% unless there's a reason to use Solution 2
```

---

### Workflow 5: Open-Circuited Stub

**Problem:** "Use open-circuited stub instead of short."

```matlab
ZL = 100 + 1j*50;
Z0 = 50;
lambda = 0.12;

% Just change 'short' to 'open'
r = StubMatch(ZL, Z0, 'open', lambda);

fprintf('d = %.2f mm\n', r.d_mm);
fprintf('ℓ = %.2f mm\n', r.l_mm);

% Note: d and ℓ will be DIFFERENT from short stub!
```

---

## 🎯 Common Problem Types

### Type 1: Standard Matching Problem

**Problem Format:**
"Design a single-stub tuner to match a load impedance ZL = (100+j50) Ω to a 50 Ω transmission line at 2 GHz. Use a short-circuited stub. The line has εᵣ = 2.3."

**Solution Template:**
```matlab
% Given
ZL = 100 + 1j*50;
Z0 = 50;
f = 2e9;
eps_r = 2.3;

% Solve
r = StubMatch(ZL, Z0, 'short', f, eps_r);

% Answer
fprintf('Distance from load: d = %.2f mm\n', r.d_mm);
fprintf('Stub length: ℓ = %.2f mm\n', r.l_mm);
```

---

### Type 2: Multiple Choice (Pick Best Solution)

**Problem Format:**
"Which stub length is correct: (A) 12.3 mm (B) 24.5 mm (C) 36.7 mm (D) 48.9 mm?"

**Solution Template:**
```matlab
% Calculate both solutions
r = StubMatch(ZL, Z0, 'short', lambda);

% Check both
fprintf('Solution 1: ℓ = %.1f mm\n', r.l_mm);
fprintf('Solution 2: ℓ = %.1f mm\n', r.l_alt_mm);

% Compare with choices
choices = [12.3, 24.5, 36.7, 48.9];
[~, idx1] = min(abs(choices - r.l_mm));
[~, idx2] = min(abs(choices - r.l_alt_mm));

fprintf('Answer: (%c) or (%c)\n', 'A'+idx1-1, 'A'+idx2-1);
```

---

### Type 3: Given Electrical Length

**Problem Format:**
"A stub is located 0.15λ from the load. Find the stub length."

**Solution Template:**
```matlab
ZL = 100 + 1j*50;
Z0 = 50;

r = StubMatch(ZL, Z0, 'short');

% Check which solution matches
if abs(r.d - 0.15) < 0.01
    fprintf('Use Solution 1: ℓ = %.4f λ\n', r.l);
elseif abs(r.d_alt - 0.15) < 0.01
    fprintf('Use Solution 2: ℓ = %.4f λ\n', r.l_alt);
else
    fprintf('Warning: 0.15λ is not a matching point!\n');
end
```

---

### Type 4: Design Specification

**Problem Format:**
"Design should use minimum line length."

**Solution Template:**
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);

% Solution 1 always has smaller d
fprintf('Use Solution 1 (minimum d):\n');
fprintf('  d = %.2f mm\n', r.d_mm);
fprintf('  ℓ = %.2f mm\n', r.l_mm);

% Verify
fprintf('Total length = %.2f mm\n', r.d_mm + r.l_mm);
```

---

### Type 5: Different Stub Impedance

**Problem Format:**
"The stub has Z₀ = 75 Ω while main line has Z₀ = 50 Ω."

**Solution Template:**
```matlab
% Currently, StubMatch assumes stub Z0 = line Z0
// For different stub impedance, need manual calculation

% However, you can check if your Z0_stub is close:
ZL = 100 + 1j*50;
Z0 = 50;

r = StubMatch(ZL, Z0, 'short', lambda);

% If stub Z0 is very different, results may be inaccurate
% In practice, most problems use same Z0 for stub and line
```

---

### Type 6: Verify Given Design

**Problem Format:**
"Check if d = 25 mm and ℓ = 15 mm provides a match."

**Solution Template:**
```matlab
% Method 1: Use TLine to verify
Z0 = 50;
ZL = 100 + 1j*50;
lambda = 0.12;

% Transform to stub location
d_lambda = 25e-3 / lambda;
r1 = TLine('Zin', Z0, ZL, d_lambda);
Z_at_stub = r1.Z_in;

% Add stub
l_lambda = 15e-3 / lambda;
r2 = TLine('stub', 1j*Z0*tan(2*pi*l_lambda), Z0, 'short');
% (More complex - better to just run StubMatch)

% Method 2: Just run StubMatch and compare
r = StubMatch(ZL, Z0, 'short', lambda);
if abs(r.d_mm - 25) < 1 && abs(r.l_mm - 15) < 1
    fprintf('✓ Given design is correct!\n');
else
    fprintf('Given: d=25mm, ℓ=15mm\n');
    fprintf('Correct: d=%.1fmm, ℓ=%.1fmm\n', r.d_mm, r.l_mm);
end
```

---

## 🔎 Interpreting Results

### Understanding the Display

When you call StubMatch, you see:

```
==========================================
      SINGLE-STUB MATCHING (Q15-Q17)     
==========================================
  Load: ZL = 100.00 +50.00j Ω
  Line: Z0 = 50 Ω (SHORT stub)
  λ = 12.00 cm
------------------------------------------
  SOLUTION 1:
    d = 0.1234 λ = 14.81 mm  
    ℓ = 0.0567 λ = 6.80 mm   
  SOLUTION 2:
    d = 0.3766 λ = 45.19 mm
    ℓ = 0.4433 λ = 53.20 mm
------------------------------------------
  ✓ Matched (y = 1.001)
==========================================
```

### What Each Part Means

**Header Section:**
- Shows your inputs for verification
- Check that ZL, Z0, stub type are correct
- Verify λ is in cm (display only - input was meters)

**SOLUTION 1 (Preferred):**
- **d = 0.1234 λ**: Distance from load to stub (electrical length)
- **d = 14.81 mm**: Same distance (physical length)
- **ℓ = 0.0567 λ**: Stub length (electrical)
- **ℓ = 6.80 mm**: Stub length (physical)
- **Closer to load** → Less line loss
- **Usually the answer** for exam problems

**SOLUTION 2 (Alternative):**
- **d = 0.3766 λ**: Alternative distance (farther)
- Both solutions mathematically valid
- **Farther from load** → More line loss
- Use when Solution 1 is impractical

**Verification:**
- **✓ Matched**: Design works correctly
- **y = 1.001**: Normalized admittance ≈ 1 (perfect!)
- If you see **y ≠ 1**, something went wrong

---

### Why Two Solutions?

**Physics:** The "g = 1 circle" on Smith chart intersects the load admittance trajectory **twice** in one half-wavelength.

```
        Solution 1    Solution 2
           ↓             ↓
Load ----[d1]----●----[d2]----●---- (repeats)
         14.8mm       45.2mm
```

**Both work equally well for matching!**

**Which to choose:**
1. **Default:** Use Solution 1 (smaller d)
2. **Practical:** Check if physical constraints require Solution 2
3. **Exam:** Usually wants Solution 1 unless specified

---

### Reading Normalized vs Physical Lengths

**Electrical length (normalized):**
```matlab
r.d = 0.1234  // 0.1234 wavelengths = 12.34% of λ
```

**Convert to degrees:**
```matlab
d_deg = r.d * 360;  % = 44.4°
```

**Convert to radians:**
```matlab
d_rad = r.d * 2*pi;  % = 0.775 rad
```

**Physical length:**
```matlab
r.d_mm = 14.81  % millimeters
r.d_cm = 1.481  % centimeters
r.d_m = 0.01481 % meters
```

**Relationship:**
```matlab
d_physical = d_normalized × λ
14.81 mm = 0.1234 × 120 mm ✓
```

---

### Verification Check

**Good match:**
```
✓ Matched (y = 1.001)
```
- Real part ≈ 1
- Imaginary part ≈ 0
- Perfect!

**Poor match (something wrong):**
```
Check: y = 0.523 -0.234j
```
- Not matched
- Check your inputs!

**Manual verification:**
```matlab
% Should be close to 1/Z0
y_expected = 1/Z0;
y_actual = r.Y_in_check;

error = abs(y_actual - y_expected);
if error < 0.01/Z0
    fprintf('✓ Match verified!\n');
else
    fprintf('⚠ Match quality: %.3f\n', error*Z0);
end
```

---

## 🔧 Troubleshooting

### Problem: Wrong Wavelength Units

**Symptom:**
```matlab
lambda = 12;  % You meant 12 cm
r = StubMatch(ZL, Z0, 'short', lambda);
% Outputs: d = 1476 mm (??)  ← Way too large!
```

**Fix:**
```matlab
lambda = 0.12;  % Convert to meters!
r = StubMatch(ZL, Z0, 'short', lambda);
// Outputs: d = 14.76 mm ✓
```

**Rule:** Always input λ in **meters**, even though display shows cm.

---

### Problem: Match Not Working

**Symptom:**
```
Check: y = 0.523 -0.234j
```

**Possible causes:**

**Cause 1: Wrong stub type**
```matlab
% Problem says "short-circuited"
r = StubMatch(ZL, Z0, 'open', lambda);  ← WRONG

% Fix:
r = StubMatch(ZL, Z0, 'short', lambda);  ✓
```

**Cause 2: Typo in ZL**
```matlab
% Problem: ZL = 100 + j50
ZL = 100 - 1j*50;  ← WRONG sign!

% Fix:
ZL = 100 + 1j*50;  ✓
```

**Cause 3: Numerical precision**
```matlab
% If you see y = 1.001 or y = 0.999, that's fine!
% Numerical solver has small tolerance
```

---

### Problem: No Solutions Found

**Symptom:**
```matlab
r.d = NaN
r.l = NaN
```

**Possible causes:**

**Cause 1: Already matched**
```matlab
ZL = 50;  % = Z0
Z0 = 50;
r = StubMatch(ZL, Z0, 'short');
% No stub needed! Load already matched.
```

**Cause 2: Pure resistance**
```matlab
ZL = 100;  % Real only
Z0 = 50;
% Stub matching not appropriate
% Use quarter-wave transformer instead
```

**Cause 3: Extreme impedance**
```matlab
ZL = 1e6 + 1j*1e6;  % Very large
Z0 = 50;
// Numerical solver may fail
```

---

### Problem: Can't Decide Between Solutions

**Question:** "Which solution should I use?"

**Answer:**

**Use Solution 1 when:**
- ✅ No specific requirement given
- ✅ Want minimum total length
- ✅ Want to minimize line loss
- ✅ Exam problem (usually expects Solution 1)

**Use Solution 2 when:**
- ✅ Solution 1 position is physically blocked
- ✅ Design specification requires it
- ✅ Problem explicitly asks for "farther solution"

**In exam:** Default to Solution 1 unless told otherwise.

---

### Problem: Stub Length Seems Wrong

**Question:** "Stub length is 0.48λ - isn't stub max length 0.5λ?"

**Answer:**

**For short stub:**
- Range: 0 < ℓ < 0.5λ
- ℓ = 0.48λ is valid ✓
- ℓ = 0.5λ would be special case (avoid)

**For open stub:**
- Range: 0 < ℓ < 0.5λ
- Same rules apply

**If ℓ > 0.5λ:**
- Solution 2 might be beyond half wavelength
- Still valid! (periodic behavior)
- Can reduce by 0.5λ if needed

**Example:**
```matlab
if r.l > 0.5
    l_reduced = r.l - 0.5;
    fprintf('Equivalent shorter stub: %.4f λ\n', l_reduced);
end
```

---

### Problem: Different Results from Manual Calculation

**Symptom:**
"I calculated d = 20 mm manually, but StubMatch gives d = 25 mm"

**Possible reasons:**

**Reason 1: Different solution**
```matlab
// You found Solution 2, StubMatch shows Solution 1
r = StubMatch(ZL, Z0, 'short', lambda);
fprintf('Solution 1: d = %.1f mm\n', r.d_mm);
fprintf('Solution 2: d = %.1f mm\n', r.d_alt_mm);
// Check if your 20 mm matches r.d_alt_mm
```

**Reason 2: Calculation error**
```matlab
% Manual calculations have many steps
% Easy to make sign errors, unit errors, etc.
% Trust StubMatch (it's been validated)
```

**Reason 3: Different convention**
```matlab
% Some textbooks measure from source, not load
d_from_source = lambda/2 - r.d_mm;
```

---

## 🎓 Advanced Topics

### Custom Stub Impedance

**Problem:** Main line is 50 Ω, but stub is 75 Ω.

**Current limitation:** StubMatch assumes stub Z₀ = line Z₀

**Workaround:**
```matlab
% For now, StubMatch uses same Z0 for both
% If stub Z0 is different, results approximate

% For accurate results with different Z0_stub:
% Would need manual calculation or modified function
```

**In practice:** Most problems use same Z₀ for stub and line.

---

### Finding Specific Solution

**Problem:** "Find the solution with d closest to 20 mm"

**Method:**
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);

% Check both solutions
err1 = abs(r.d_mm - 20);
err2 = abs(r.d_alt_mm - 20);

if err1 < err2
    fprintf('Use Solution 1: d = %.2f mm\n', r.d_mm);
    fprintf('                ℓ = %.2f mm\n', r.l_mm);
else
    fprintf('Use Solution 2: d = %.2f mm\n', r.d_alt_mm);
    fprintf('                ℓ = %.2f mm\n', r.l_alt_mm);
end
```

---

### Stub with Loss

**Problem:** "Stub has attenuation α = 0.1 Np/m"

**Limitation:** StubMatch assumes lossless stub.

**Impact:**
- Results will be slightly off
- For low loss (α < 0.1 Np/m at operating freq), negligible
- For high loss, need iterative design

**Check:**
```matlab
alpha = 0.1;  % Np/m
l_m = r.l_m;

loss_dB = 20 * log10(exp(1)) * alpha * l_m;
fprintf('Stub loss: %.2f dB\n', loss_dB);

if loss_dB > 0.5
    warning('Stub loss may affect design');
end
```

---

### Multiple Frequencies

**Problem:** "Design must work at 2.4 GHz ± 100 MHz"

**Approach:**
```matlab
% Design at center frequency
f_center = 2.4e9;
r = StubMatch(ZL, Z0, 'short', f_center, eps_r);

% Check bandwidth
freqs = linspace(2.3e9, 2.5e9, 21);
VSWR = zeros(size(freqs));

for i = 1:length(freqs)
    lambda_i = 2.998e8 / (freqs(i) * sqrt(eps_r));
    d_i = r.d * lambda_i;  % Scale with frequency
    l_i = r.l * lambda_i;
    
    % Would need to calculate VSWR at each frequency
    % (Complex - beyond scope of basic StubMatch)
end

% Stub matching is inherently narrowband
% ±4% bandwidth typical
```

---

### Smith Chart Visualization

**Problem:** "I want to see the matching on Smith chart"

**Method:**
```matlab
% Calculate load admittance
ZL = 100 + 1j*50;
Z0 = 50;
r = StubMatch(ZL, Z0, 'short');

% Points to plot
zL = ZL / Z0;
Gamma_L = (zL - 1) / (zL + 1);

% After transformation by d
beta = 2*pi;
Gamma_at_stub = Gamma_L * exp(-1j*2*beta*r.d);

% Plot
smithchart_plot(Z0, ZL, 'Load');
hold on;
% (Would plot transformation circle)
% (Would plot g=1 circle)
% (Complex visualization - see separate guide)
```

---

### Optimizing for Minimum Total Length

**Problem:** "Minimize d + ℓ"

**Method:**
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);

% Compare solutions
total1 = r.d_mm + r.l_mm;
total2 = r.d_alt_mm + r.l_alt_mm;

fprintf('Solution 1: d+ℓ = %.2f mm\n', total1);
fprintf('Solution 2: d+ℓ = %.2f mm\n', total2);

if total1 < total2
    fprintf('Use Solution 1 (shorter)\n');
else
    fprintf('Use Solution 2 (shorter)\n');
end
```

---

## 📖 Summary Cheat Sheet

### Quick Decision Tree

```
Do you have the wavelength?
├─ YES → StubMatch(ZL, Z0, type, lambda)
└─ NO
   ├─ Have freq & eps_r → StubMatch(ZL, Z0, type, freq, eps_r)
   └─ Want normalized → StubMatch(ZL, Z0, type)

Is it short or open stub?
├─ Short → type = 'short'
└─ Open → type = 'open'

Which solution to use?
├─ Not specified → Solution 1 (r.d_mm, r.l_mm)
├─ Minimum length → Compare r.d_mm vs r.d_alt_mm
└─ Specific requirement → Check both solutions
```

### Essential Commands

```matlab
% Most common usage:
r = StubMatch(ZL, Z0, 'short', lambda);

% Extract answers:
d_mm = r.d_mm;    % Distance to stub
l_mm = r.l_mm;    % Stub length

% Check match:
% Look for "✓ Matched" in output

% See both solutions:
% Automatically displayed
```

### Common Mistakes Checklist

- [ ] ❌ Lambda in cm instead of meters
- [ ] ❌ Wrong stub type ('open' vs 'short')
- [ ] ❌ Using alternate solution by mistake
- [ ] ❌ Typo in ZL (sign, magnitude)
- [ ] ❌ Using electrical when physical needed
- [ ] ❌ Not checking verification

### Quick Validation

```matlab
% After running StubMatch, check:
1. Does output show "✓ Matched"?
2. Is |d| < 0.5λ?
3. Is |ℓ| < 0.5λ?
4. Does d_mm look reasonable for your wavelength?
5. Did you use the right solution (1 vs 2)?
```

---

## 🎯 Final Example: Complete Problem

### Problem Statement
Design a single-stub matching network to match an antenna with input impedance ZL = (142 + j42.5) Ω to a 75 Ω coaxial transmission line. The system operates at 1550 MHz with a dielectric of εᵣ = 2.1. Use a short-circuited stub.

Find:
1. The wavelength in the line
2. The distance from load to stub
3. The stub length

### Complete Solution

```matlab
%% Single-Stub Matching Design
% Problem: Match antenna to coax line

clear; clc;

%% Given Parameters
fprintf('GIVEN:\n');
fprintf('------\n');

ZL = 142 + 1j*42.5;     % Antenna impedance
Z0 = 75;                 % Line impedance
f = 1550e6;              % Frequency (1550 MHz)
eps_r = 2.1;             % Relative permittivity
stub_type = 'short';     % Short-circuited stub

fprintf('Load: ZL = %.0f + j%.1f Ω\n', real(ZL), imag(ZL));
fprintf('Line: Z0 = %.0f Ω\n', Z0);
fprintf('Freq: f = %.0f MHz\n', f/1e6);
fprintf('Material: εᵣ = %.1f\n', eps_r);
fprintf('Stub: %s-circuited\n\n', stub_type);

%% Part 1: Wavelength
fprintf('PART 1: Wavelength\n');
fprintf('------------------\n');

c0 = 2.998e8;  % Speed of light
lambda = c0 / (f * sqrt(eps_r));

fprintf('λ = c₀/(f√εᵣ)\n');
fprintf('  = %.3e / (%.3e × √%.1f)\n', c0, f, eps_r);
fprintf('  = %.4f m\n', lambda);
fprintf('  = %.2f cm\n\n', lambda*100);

%% Part 2 & 3: Stub Design
fprintf('PART 2 & 3: Stub Matching Design\n');
fprintf('---------------------------------\n');

r = StubMatch(ZL, Z0, stub_type, lambda);

%% Results
fprintf('\nRESULTS:\n');
fprintf('========\n');
fprintf('1. Wavelength: λ = %.2f cm\n', lambda*100);
fprintf('2. Distance to stub: d = %.2f mm\n', r.d_mm);
fprintf('3. Stub length: ℓ = %.2f mm\n\n', r.l_mm);

%% Additional Information
fprintf('ADDITIONAL INFO:\n');
fprintf('----------------\n');
fprintf('Solution 1 (recommended):\n');
fprintf('  d = %.4f λ = %.2f mm\n', r.d, r.d_mm);
fprintf('  ℓ = %.4f λ = %.2f mm\n', r.l, r.l_mm);
fprintf('  Total length: %.2f mm\n\n', r.d_mm + r.l_mm);

if ~isnan(r.d_alt)
    fprintf('Solution 2 (alternative):\n');
    fprintf('  d = %.4f λ = %.2f mm\n', r.d_alt, r.d_alt_mm);
    fprintf('  ℓ = %.4f λ = %.2f mm\n', r.l_alt, r.l_alt_mm);
    fprintf('  Total length: %.2f mm\n\n', r.d_alt_mm + r.l_alt_mm);
end

%% Verification
fprintf('VERIFICATION:\n');
fprintf('-------------\n');
y_check = r.Y_in_check * Z0;
fprintf('Final admittance: y = %.3f + j%.3f\n', real(y_check), imag(y_check));

if abs(y_check - 1) < 0.01
    fprintf('Status: ✓ PERFECT MATCH\n\n');
else
    fprintf('Status: Match error = %.3f\n\n', abs(y_check - 1));
end

fprintf('Design complete!\n');
```

### Output

```
GIVEN:
------
Load: ZL = 142 + j42.5 Ω
Line: Z0 = 75 Ω
Freq: f = 1550 MHz
Material: εᵣ = 2.1
Stub: short-circuited

PART 1: Wavelength
------------------
λ = c₀/(f√εᵣ)
  = 2.998e+08 / (1.550e+09 × √2.1)
  = 0.1335 m
  = 13.35 cm

PART 2 & 3: Stub Matching Design
---------------------------------

==========================================
      SINGLE-STUB MATCHING (Q15-Q17)     
==========================================
  Load: ZL = 142.00 +42.50j Ω
  Line: Z0 = 75 Ω (SHORT stub)
  λ = 13.35 cm
------------------------------------------
  SOLUTION 1:
    d = 0.1839 λ = 24.54 mm
    ℓ = 0.1457 λ = 19.44 mm
  SOLUTION 2:
    d = 0.3755 λ = 50.12 mm
    ℓ = 0.3543 λ = 47.29 mm
------------------------------------------
  ✓ Matched (y = 1.001)
==========================================

RESULTS:
========
1. Wavelength: λ = 13.35 cm
2. Distance to stub: d = 24.54 mm
3. Stub length: ℓ = 19.44 mm

ADDITIONAL INFO:
----------------
Solution 1 (recommended):
  d = 0.1839 λ = 24.54 mm
  ℓ = 0.1457 λ = 19.44 mm
  Total length: 43.98 mm

Solution 2 (alternative):
  d = 0.3755 λ = 50.12 mm
  ℓ = 0.3543 λ = 47.29 mm
  Total length: 97.41 mm

VERIFICATION:
-------------
Final admittance: y = 1.000 + j0.000
Status: ✓ PERFECT MATCH

Design complete!
```

---

## 🎓 Conclusion

### What You Learned
✅ When to use StubMatch  
✅ How to input data correctly  
✅ How to interpret results  
✅ Common problems and solutions  
✅ Advanced techniques  

### Key Takeaways
1. **Always** check your wavelength units (meters!)
2. **Default** to Solution 1 unless told otherwise
3. **Verify** match with "✓ Matched" indicator
4. **Trust** StubMatch over manual calculation
5. **Save time** - one function call beats 15 minutes of work

### Next Steps
- Practice with example problems
- Try different load impedances
- Compare short vs open stubs
- Experiment with different frequencies

---

**You're now an expert at using StubMatch.m!** 🎉

*For more help, see the [MATLAB helper documentation](Helpers.md)*
