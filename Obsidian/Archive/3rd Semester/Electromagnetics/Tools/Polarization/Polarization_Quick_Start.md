# Polarization.m - Quick Start Guide

> **5-Minute Crash Course**  
> Everything you need to analyze polarization RIGHT NOW

---

## TL;DR - The Three Patterns You Need

```matlab
% Pattern 1: Complex phasor (90% of problems)
r = Polarization([1; -1j; 0]);
type = r.type;           % 'Linear', 'Circular', or 'Elliptical'
hand = r.handedness;     % 'RHCP', 'LHCP', or 'N/A'
AR = r.AR;               % Axial ratio

% Pattern 2: Amplitude and phase
r = Polarization('ap', 10, 5, 0, 90);
% Given: |Ex|=10, |Ey|=5, φx=0°, φy=90°

% Pattern 3: Time-domain (a·cos + b·sin)
a = [2; 1; 0];  b = [0; -1; -2];  beta = [2; -4; 2];
r = Polarization(a, b, beta);
```

**That's it!** These three patterns handle all polarization problems.

---

## 📖 Table of Contents

1. [[#Pattern 1: Complex Phasor]] (2 min)
2. [[#Pattern 2: Amplitude/Phase]] (1 min)
3. [[#Pattern 3: Time-Domain]] (1 min)
4. [[#Quick Recognition Guide]] (1 min)

---

## Pattern 1: Complex Phasor

**Use when:** Given E-field as complex phasor (90% of problems)

### Syntax
```matlab
r = Polarization(F)              % +z propagation (default)
r = Polarization(F, k_hat)       % Specify direction
```

### Examples

#### RHCP (Right-Hand Circular)
```matlab
% E = x̂ - ŷj (rotates clockwise in +z)
F = [1; -1j; 0];
r = Polarization(F);

>> r.type
ans = 'Circular'

>> r.handedness
ans = 'RHCP'

>> r.AR
ans = 1
```

#### LHCP (Left-Hand Circular)
```matlab
% E = x̂ + ŷj (rotates counter-clockwise in +z)
F = [1; 1j; 0];
r = Polarization(F);

>> r.type
ans = 'Circular'

>> r.handedness
ans = 'LHCP'

>> r.AR
ans = 1
```

#### Linear (45°)
```matlab
% E = x̂ + ŷ (diagonal)
F = [1; 1; 0];
r = Polarization(F);

>> r.type
ans = 'Linear'

>> r.handedness
ans = 'N/A'

>> r.AR
ans = Inf
```

#### Elliptical
```matlab
% E = 2x̂ - ŷj (ellipse, RHCP)
F = [2; -1j; 0];
r = Polarization(F);

>> r.type
ans = 'Elliptical'

>> r.handedness
ans = 'RHCP'

>> r.AR
ans = 2.4142  % Between 1 and Inf
```

### Key Points
- **Default:** +z propagation if k_hat not specified
- **RHCP in +z:** Use `-j` for y-component
- **LHCP in +z:** Use `+j` for y-component
- **Linear:** Real and imaginary parts parallel
- **Check AR:** 1 = circular, ∞ = linear, between = elliptical

---

## Pattern 2: Amplitude/Phase

**Use when:** Given |E| and φ instead of complex phasor

### Syntax
```matlab
r = Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg)
r = Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg, k_hat)
```

### Example
```matlab
% Given: |Ex| = 10 V/m, |Ey| = 5 V/m
%        φx = 0°, φy = 90°

r = Polarization('ap', 10, 5, 0, 90);

>> r.type
ans = 'Elliptical'

>> r.handedness
ans = 'RHCP'

>> r.AR
ans = 2.0000

>> r.AR_dB
ans = 6.0206
```

### Conversion
Internally converts to phasor:
```
Fx = Ex × exp(j·φx) = 10 × exp(j·0°) = 10
Fy = Ey × exp(j·φy) = 5 × exp(j·90°) = 5j
F = [10; 5j; 0]
```

---

## Pattern 3: Time-Domain

**Use when:** E-field given as **a**·cos(ψ) + **b**·sin(ψ)

### Syntax
```matlab
r = Polarization(a, b, beta)
% E(t) = a·cos(ωt - β·r) + b·sin(ωt - β·r)
```

### Example
```matlab
% Given: E = [2x̂ + ŷ]cos(ψ) + [-ŷ - 2ẑ]sin(ψ)
%        β = [2; -4; 2]

a = [2; 1; 0];
b = [0; -1; -2];
beta = [2; -4; 2];

r = Polarization(a, b, beta);

>> r.type
ans = 'Elliptical'

>> r.handedness
ans = 'RHCP'
```

### Conversion
Internally converts to phasor:
```
F = a - j·b
```

---

## Quick Recognition Guide

### How to Identify Polarization Type

#### Is it RHCP or LHCP?

**For +z propagation:**
```matlab
[1; -1j; 0]  → RHCP  (minus j)
[1; +1j; 0]  → LHCP  (plus j)
```

**Memory trick:** 
- RHCP: **R**ight = **-**j (minus)
- LHCP: **L**eft = **+**j (plus)

#### Is it Linear?

Check if AR = ∞:
```matlab
r = Polarization(F);
if isinf(r.AR)
    disp('Linear polarization')
end
```

**Or manually:** Real and imaginary parts parallel
```matlab
F = [1; 2; 0];     % Linear (all real)
F = [1j; 2j; 0];   % Linear (all imaginary)
F = [1; 1; 0];     % Linear (same ratio)
```

#### Is it Circular?

Check if AR = 1:
```matlab
r = Polarization(F);
if abs(r.AR - 1) < 0.01
    disp('Circular polarization')
end
```

**Or manually:** Equal magnitudes, 90° phase difference
```matlab
F = [1; -1j; 0];   % Circular (|1| = |-j|, phase diff = 90°)
F = [3; -3j; 0];   % Circular (scaled RHCP)
```

#### Is it Elliptical?

Everything else:
```matlab
1 < r.AR < ∞  →  Elliptical
```

---

## What You Get Back

```matlab
r = Polarization([1; -1j; 0]);

% Type and handedness
r.type         % 'Linear', 'Circular', or 'Elliptical'
r.handedness   % 'RHCP', 'LHCP', or 'N/A'

% Axial ratio
r.AR           % 1 = circular, ∞ = linear
r.AR_dB        % AR in dB (0 = circular, ∞ = linear)

% Ellipse parameters
r.major        % Major semi-axis
r.minor        % Minor semi-axis  
r.tilt_deg     % Tilt angle (degrees)

% Phasor
r.F            % Complex phasor used
r.k_hat        % Propagation direction
```

---

## Common Mistakes

### ❌ Mistake 1: Wrong Sign for RHCP/LHCP

```matlab
❌ Wrong:
F = [1; 1j; 0];    % Thought this was RHCP
% Actually LHCP!

✅ Correct:
F = [1; -1j; 0];   % RHCP in +z (minus j)
F = [1; 1j; 0];    % LHCP in +z (plus j)
```

**Remember:** In +z propagation, RHCP uses `-j`

---

### ❌ Mistake 2: Forgetting Semicolons

```matlab
❌ Wrong:
F = [1, -1j, 0];   % Row vector (comma)

✅ Correct:
F = [1; -1j; 0];   % Column vector (semicolon)
```

---

### ❌ Mistake 3: Wrong Amplitude/Phase Syntax

```matlab
❌ Wrong:
r = Polarization(10, 5, 0, 90);  // Missing 'ap'

✅ Correct:
r = Polarization('ap', 10, 5, 0, 90);  // Need 'ap' keyword
```

---

### ❌ Mistake 4: Confusing AR with VSWR

```matlab
% AR (Axial Ratio) - Polarization
AR = 1     → Circular
AR = ∞     → Linear

% VSWR (Standing Wave Ratio) - Transmission lines  
VSWR = 1   → Matched
VSWR = ∞   → Total reflection

// Don't mix these up!
```

---

## Quick Cheat Sheet

### Input Forms
```matlab
% Complex phasor (most common)
Polarization([Ex; Ey; Ez])
Polarization([Ex; Ey; Ez], k_hat)

% Amplitude/Phase
Polarization('ap', Ex, Ey, phi_x, phi_y)

% Time-domain
Polarization(a, b, beta)
```

### Output Fields
```matlab
r.type         % Type of polarization
r.handedness   % RHCP/LHCP/N/A
r.AR           % Axial ratio
r.AR_dB        % AR in dB
r.major, r.minor  % Semi-axes
r.tilt_deg     % Tilt angle
```

### Quick Tests
```matlab
% RHCP
Polarization([1; -1j; 0])     % AR=1, RHCP

% LHCP  
Polarization([1; 1j; 0])      % AR=1, LHCP

% Linear
Polarization([1; 1; 0])       % AR=∞, Linear

% Check
r.AR == 1       % Circular
isinf(r.AR)     % Linear
```

---

## ✅ 60-Second Self-Test

Try these without looking:

1. **What type is [1; -1j; 0]?**
   ```matlab
   r = Polarization([1; -1j; 0]);
   r.type  % ?
   r.handedness  % ?
   ```

2. **What type is [2; 2; 0]?**
   ```matlab
   r = Polarization([2; 2; 0]);
   r.type  % ?
   ```

3. **Given |Ex|=5, |Ey|=5, φx=0°, φy=90°, what type?**
   ```matlab
   r = Polarization('ap', 5, 5, 0, 90);
   r.type  % ?
   ```

**Answers:**
1. Circular, RHCP (equal magnitudes, -j indicates right-hand)
2. Linear (all real → parallel components)
3. Circular (equal magnitudes, 90° phase diff)

---

## 🎯 What's Next?

**If this solved your problem:**
→ Print the [Quick Reference Card](Polarization_Quick_Reference.md) for exams

**Want to learn more:**
→ Read the [Complete Guide](Polarization_Complete_Guide.md) (30 min)

**Something not working:**
→ Check [Troubleshooting Guide](Polarization_Troubleshooting.md)

**Need practice:**
→ Work through [Exam Examples](Polarization_Exam_Examples.md)

---

## 💡 Remember These Rules

1. **Most common:** Complex phasor `Polarization([Ex; Ey; Ez])`
2. **RHCP in +z:** Use `-j` for y-component
3. **LHCP in +z:** Use `+j` for y-component
4. **AR = 1:** Circular
5. **AR = ∞:** Linear
6. **1 < AR < ∞:** Elliptical

**You're ready to analyze polarization!** 🚀

---

[← Back to Master Index](Polarization_MASTER_INDEX.md) | [Complete Guide →](Polarization_Complete_Guide.md)
