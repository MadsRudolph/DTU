# Medium.m - Troubleshooting Guide

> **Quick Error Diagnosis and Fixes**  
> Find your problem below and jump to the solution

---

## 🔍 Error Quick Finder

**Jump directly to your problem:**

1. [Wavelength seems wrong (way too large/small)](#problem-1-wavelength-way-off)
2. [Skin depth is NaN or Inf](#problem-2-skin-depth-is-nan-or-inf)
3. [Classification doesn't match expectations](#problem-3-wrong-classification)
4. [Impedance is complex when it should be real](#problem-4-unexpected-complex-impedance)
5. [Alpha is zero but material has losses](#problem-5-alpha-is-zero-but-should-have-loss)
6. [Results don't match manual calculation](#problem-6-results-dont-match-manual)
7. [Error: "Unknown mode"](#problem-7-unknown-mode-error)

---

## Problem 1: Wavelength Way Off

### Symptoms
```matlab
>> r = Medium(4, 10);
>> r.lambda

ans = 29979245.7997  % Way too large! Should be ~1.5 cm
```

### Diagnosis
**Wrong units** - You used MHz or GHz instead of Hz

### Solution
```matlab
❌ Wrong:
r = Medium(4, 10);           % Thought this was 10 GHz
r = Medium(4, 10*10^9);      % Complicated notation

✅ Correct:
r = Medium(4, 10e9);         % 10 GHz in Hz
```

### Explanation
Medium ALWAYS expects frequency in **Hz**, not MHz or GHz.

**Quick conversion:**
- 10 MHz → `10e6` Hz
- 2.4 GHz → `2.4e9` Hz
- 900 MHz → `900e6` Hz

### Verification
```matlab
% Wavelength in free space at 10 GHz should be 3 cm
r = Medium('free', 10e9);
r.lambda * 100  % Should be ~3 cm
```

---

## Problem 2: Skin Depth is NaN or Inf

### Symptoms
```matlab
>> r = Medium(4, 10e9);
>> r.skin_depth

ans = Inf
```

### Diagnosis
**Lossless material** - Skin depth only exists for lossy/conductive materials

### Solution

**If material should be lossless:**
```matlab
✅ This is correct behavior
% Lossless materials have infinite skin depth
% Use r.lambda instead
```

**If material should be lossy:**
```matlab
❌ Wrong:
r = Medium(80, 1e6);         % Missing sigma

✅ Correct:
r = Medium(80, 4, 1e6);      % Include conductivity
r.skin_depth                 % Now has finite value
```

**If you want conductor skin depth:**
```matlab
✅ Correct:
r = Medium('conductor', 5.8e7, 1e9);  % Copper
r.skin_depth * 1e6           % δ in μm
```

### Quick Check
```matlab
% These should have infinite skin depth:
Medium(4, 10e9).skin_depth   % Inf (lossless)

% These should have finite skin depth:
Medium(4, 0.01, 10e9).skin_depth        % Finite (lossy)
Medium('conductor', 5.8e7, 1e9).skin_depth % Finite (conductor)
```

---

## Problem 3: Wrong Classification

### Symptoms
```matlab
>> r = Medium(50, 1.5, 900e6);
>> r.classification

ans = 'Good Conductor'  % Expected 'Low-Loss Dielectric'
```

### Diagnosis
**Check loss tangent** - Material classification based on tan(δ)

### Solution

**View the classification:**
```matlab
r = Medium(50, 1.5, 900e6);
fprintf('tan(δ) = %.4f\n', r.tan_delta);
fprintf('Type: %s\n', r.classification);
```

**Classification rules:**
| tan(δ) | Classification |
|--------|----------------|
| < 0.01 | Lossless (approx) |
| < 0.1 | Low-Loss Dielectric |
| 0.1 - 10 | Quasi-Conductor |
| > 10 | Good Conductor |

**If classification is wrong:**

1. **Check if you used right mode:**
   ```matlab
   ❌ Wrong for metal:
   r = Medium(1, 5.8e7, 1e9);  % Lossy mode
   
   ✅ Correct for metal:
   r = Medium('conductor', 5.8e7, 1e9);
   ```

2. **Verify your parameters:**
   ```matlab
   % Double-check sigma value
   fprintf('σ = %.3e S/m\n', r.sigma);
   fprintf('ω = %.3e rad/s\n', r.omega);
   fprintf('ε = %.3e F/m\n', r.eps_r * 8.854e-12);
   ```

### When Classification Matters
- Tells you if you picked the right analysis mode
- Validates your input parameters
- Indicates which approximations are valid

---

## Problem 4: Unexpected Complex Impedance

### Symptoms
```matlab
>> r = Medium(4, 10e9);
>> r.eta

ans = 188.3651 + 0.0000i  % Why complex for lossless?
```

### Diagnosis
**MATLAB displays complex numbers** - Even when imaginary part is zero

### Solution

**Check if it's actually complex:**
```matlab
% Method 1: Check imaginary part
if abs(imag(r.eta)) < 1e-10
    fprintf('Effectively real: %.2f Ω\n', real(r.eta));
end

% Method 2: Use abs() for magnitude
eta_mag = abs(r.eta);  % Always gives magnitude

% Method 3: Check angle
eta_angle = angle(r.eta) * 180/pi;  % Should be 0 or 180
```

**For lossless materials:**
```matlab
r = Medium(4, 10e9);
abs(r.eta)              % Magnitude (real for lossless)
```

**For lossy materials:**
```matlab
r = Medium(50, 1.5, 900e6);
abs(r.eta)              % Magnitude
angle(r.eta) * 180/pi   % Phase angle in degrees
```

### When to Expect Complex η

- **Lossless:** η is real (but MATLAB shows +0.0000i)
- **Lossy:** η has both real and imaginary parts
- **Conductor:** η = (1+j) × R_s

---

## Problem 5: Alpha is Zero But Should Have Loss

### Symptoms
```matlab
>> r = Medium(50, 0.001, 900e6);
>> r.alpha

ans = 0  % Should have some attenuation
```

### Diagnosis
**Conductivity too small** - Material effectively lossless

### Solution

**Check loss tangent:**
```matlab
r = Medium(50, 0.001, 900e6);
fprintf('tan(δ) = %.3e\n', r.tan_delta);
% If tan(δ) < 0.01, material is effectively lossless
```

**If you expect more loss:**
1. **Verify sigma value:**
   ```matlab
   fprintf('σ = %.3e S/m\n', r.sigma);  % Check if too small
   ```

2. **Try higher frequency:**
   ```matlab
   r = Medium(50, 0.001, 10e9);  % Higher freq → more loss
   ```

3. **Use correct sigma:**
   ```matlab
   % Typical values:
   % Seawater:  sigma = 4 S/m
   % Tissue:    sigma = 0.5-2 S/m
   % Dry soil:  sigma = 0.001-0.01 S/m
   ```

### Quick Test
```matlab
% This should have loss:
r = Medium(80, 4, 1e6);
r.alpha  % Should be ~1.9 Np/m

% This should be lossless:
r = Medium(80, 0, 1e6);
r.alpha  % Should be 0
```

---

## Problem 6: Results Don't Match Manual

### Symptoms
```matlab
% Your manual calculation: λ = 1.5 cm
>> r = Medium(4, 10e9);
>> r.lambda * 100

ans = 1.4989  % Close but not exact
```

### Diagnosis
**Rounding differences** or **different constant values**

### Solution

**Check your constants:**
```matlab
% Medium.m uses:
eps0 = 8.854187817e-12  % F/m
mu0 = 4*pi*1e-7         % H/m
c0 = 2.99792458e8       % m/s

% If you used different values, results will differ slightly
```

**Verify calculation:**
```matlab
r = Medium(4, 10e9);

% Wavelength should be:
% λ = c0 / (f × √ε_r) = 3e8 / (10e9 × 2) = 1.5 cm
expected = 3e8 / (10e9 * sqrt(4));
actual = r.lambda;
fprintf('Expected: %.4e m\n', expected);
fprintf('Actual:   %.4e m\n', actual);
fprintf('Diff:     %.2e m\n', abs(expected - actual));
```

**Common sources of difference:**
1. Using c₀ = 3×10⁸ instead of 2.998×10⁸
2. Using rounded ε₀ or μ₀ values
3. Different π precision
4. Rounding intermediate steps

### When to Worry
- **< 1% difference:** Normal rounding
- **> 5% difference:** Check your calculation
- **> 50% difference:** Wrong units or formula

---

## Problem 7: "Unknown Mode" Error

### Symptoms
```matlab
>> r = Medium('copper', 5.8e7, 1e9);
Error: Unknown mode: copper. Run Medium() for help.
```

### Diagnosis
**Invalid mode string** - Typo in mode name

### Solution

**Valid mode strings:**
```matlab
✅ Correct modes:
Medium('conductor', ...)  % Not 'copper', 'metal', etc.
Medium('tand', ...)       % Not 'tangent', 'losstan', etc.
Medium('skin', ...)       % Not 'skindepth', 'penetration', etc.
Medium('free', ...)       % Not 'freespace', 'vacuum', etc.

❌ Common mistakes:
Medium('copper', ...)     % Use 'conductor'
Medium('tangent', ...)    % Use 'tand'
Medium('skindepth', ...)  % Use 'skin'
Medium('vacuum', ...)     % Use 'free'
```

**Case doesn't matter:**
```matlab
Medium('CONDUCTOR', ...)  % Works
Medium('Conductor', ...)  % Works
Medium('conductor', ...)  % Works
```

---

## 🔧 Diagnostic Script

**Run this to check your Medium setup:**

```matlab
fprintf('=== Medium.m Diagnostic ===\n\n');

% Test 1: Basic lossless
fprintf('Test 1: Lossless dielectric\n');
r1 = Medium(4, 10e9);
fprintf('  λ = %.4f cm (should be ~1.5 cm)\n', r1.lambda * 100);
fprintf('  η = %.2f Ω (should be ~188 Ω)\n', abs(r1.eta));

% Test 2: Conductor
fprintf('\nTest 2: Conductor\n');
r2 = Medium('conductor', 5.8e7, 1e9);
fprintf('  δ = %.2f μm (should be ~2.1 μm)\n', r2.skin_depth * 1e6);

% Test 3: Lossy
fprintf('\nTest 3: Lossy material\n');
r3 = Medium(80, 4, 1e6);
fprintf('  α = %.2f Np/m (should be ~1.9 Np/m)\n', r3.alpha);
fprintf('  Classification: %s\n', r3.classification);

% Test 4: Free space
fprintf('\nTest 4: Free space\n');
r4 = Medium('free', 3e8);
fprintf('  λ₀ = %.2f m (should be 1.0 m)\n', r4.lambda);
fprintf('  η₀ = %.2f Ω (should be ~377 Ω)\n', r4.eta);

fprintf('\n=== All tests complete ===\n');
```

**Expected output:**
```
Test 1: Lossless dielectric
  λ = 1.4989 cm (should be ~1.5 cm)
  η = 188.37 Ω (should be ~188 Ω)

Test 2: Conductor
  δ = 2.10 μm (should be ~2.1 μm)

Test 3: Lossy material
  α = 1.88 Np/m (should be ~1.9 Np/m)
  Classification: Good Conductor

Test 4: Free space
  λ₀ = 1.00 m (should be 1.0 m)
  η₀ = 376.73 Ω (should be ~377 Ω)
```

---

## ✅ Pre-Submission Checklist

Before submitting your homework or exam:

- [ ] Frequency in Hz (not MHz or GHz)
- [ ] Conductivity in S/m (not mS/m or kS/m)
- [ ] Used correct mode ('conductor' for metals)
- [ ] Classification makes sense
- [ ] Results are physically reasonable
- [ ] Units converted for final answer

---

## 🆘 Still Having Problems?

**Check these resources:**

1. **[Quick Start Guide](Medium_Quick_Start.md)** - Verify basic usage
2. **[Complete Guide](Medium_Complete_Guide.md)** - Detailed explanations
3. **[Exam Examples](Medium_Exam_Examples.md)** - See working examples
4. **MATLAB help** - Type `Medium()` with no arguments

**Common issue not listed here?**
→ Review the [Complete Guide](Medium_Complete_Guide.md) for detailed theory

---

[← Master Index](Medium_MASTER_INDEX.md) | [Complete Guide →](Medium_Complete_Guide.md)
