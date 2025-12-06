# TLine.m - Troubleshooting Guide

> **Quick Error Diagnosis and Fixes**

---

## 🔍 Error Quick Finder

1. [Results seem completely wrong](#problem-1-results-completely-wrong)
2. [Q13/Q14: Gamma_L doesn't make sense](#problem-2-q1314-gamma_l-wrong)
3. [Q11: Z_A is way off](#problem-3-q11-z_a-way-off)
4. [Q12: Stub length is negative or > 0.5](#problem-4-q12-bad-stub-length)
5. [VSWR < 1 (impossible!)](#problem-5-vswr-less-than-1)
6. [Error: "Unknown mode"](#problem-6-unknown-mode-error)
7. [Results don't match manual calculation](#problem-7-doesnt-match-manual)

---

## Problem 1: Results Completely Wrong

### Symptoms
```matlab
>> r = TLine(50, 100, 0.3);
>> r.Z_in
ans = 1.0e+10 * (huge number)
```

### Diagnosis
**Wrong length units** - Gave meters instead of wavelengths

### Solution
```matlab
❌ Wrong:
r = TLine(50, 100, 0.3);     // If you meant 0.3m

✅ Correct for λ:
r = TLine(50, 100, 0.3);     // 0.3 wavelengths

✅ Correct for meters:
r = TLine(50, 100, 0.3, freq, vp);  // Include freq and vp
```

### Rule
- **Without freq/vp:** Length is in wavelengths (λ)
- **With freq/vp:** Length is in meters

---

## Problem 2: Q13/Q14 Gamma_L Wrong

### Symptoms
```matlab
>> r = TLine('load', 75, Gamma_A, 0.3);
>> abs(r.Gamma_L)
ans = 2.5   % > 1 is impossible!
```

### Diagnosis
**Gave Z instead of Gamma** or **wrong direction**

### Solution
```matlab
❌ Wrong:
Gamma_A = 75 + 50*1j;  // This is impedance, not Gamma!
r = TLine('load', 75, Gamma_A, 0.3);

✅ Correct:
% First convert Z to Gamma if needed:
Gamma_A = (Z_A - Z0)/(Z_A + Z0);
% Or given directly in polar:
Gamma_A = 0.539 * exp(1j * deg2rad(166));
r = TLine('load', 75, Gamma_A, 0.3);
```

### Verification
```matlab
% |Gamma| must be ≤ 1
if abs(r.Gamma_L) > 1
    error('Something wrong - |Gamma| cannot exceed 1');
end
```

---

## Problem 3: Q11 Z_A Way Off

### Symptoms
```matlab
>> r = TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0);
>> r.Z_A
ans = 35 + 500i   % Imaginary part way too large
```

### Diagnosis  
**Missing c0 definition** or **wrong freq/vp units**

### Solution
```matlab
❌ Wrong:
r = TLine('series_C', 60, ZL, 17e-3, 1e-12, 5e9, 0.79);
% vp should be in m/s, not fraction!

✅ Correct:
c0 = 3e8;  % or 2.998e8
r = TLine('series_C', 60, ZL, 17e-3, 1e-12, 5e9, 0.79*c0);
% Now vp = 0.79 × 3×10^8 m/s
```

### Check Your Inputs
```matlab
fprintf('freq = %.3e Hz\n', freq);
fprintf('vp = %.3e m/s\n', vp);
fprintf('C = %.3e F\n', C);
fprintf('len = %.3e m\n', len);
```

---

## Problem 4: Q12 Bad Stub Length

### Symptoms
```matlab
>> r = TLine('stub', 1j*30, 75, 'short');
>> r.short.len_lambda
ans = -0.15   % Negative!
```

### Diagnosis
**Target impedance is wrong sign** or **used wrong stub type**

### Solution
```matlab
❌ Wrong:
r = TLine('stub', -1j*30, 75, 'short');  // Wrong sign

✅ Correct:
r = TLine('stub', 1j*30, 75, 'short');   // Positive jX

% For capacitive (negative):
r = TLine('stub', -1j*30, 75, 'short');
% Length will be in range [0, 0.5]
```

### Valid Range
```matlab
% Stub length should be in [0, 0.5] λ
if r.short.len_lambda < 0 || r.short.len_lambda > 0.5
    % May need to add/subtract 0.5λ
    len_adj = mod(r.short.len_lambda, 0.5);
end
```

---

## Problem 5: VSWR Less Than 1

### Symptoms
```matlab
>> r = TLine(50, 25, 0.3);
>> r.VSWR
ans = 0.5   % Impossible! VSWR ≥ 1 always
```

### Diagnosis
**Logic error** - This shouldn't happen with TLine.m

### Solution
```matlab
% VSWR is always ≥ 1
% If you see < 1, you may have calculated it manually wrong

% TLine.m calculates:
VSWR = (1 + |Gamma|) / (1 - |Gamma|)

% Verify:
Gamma_mag = abs(r.Gamma_L);
VSWR_check = (1 + Gamma_mag) / (1 - Gamma_mag);
fprintf('VSWR should be: %.4f\n', VSWR_check);
```

---

## Problem 6: "Unknown Mode" Error

### Symptoms
```matlab
>> r = TLine('series', Z0, ZL, len, C, freq, vp);
Error: Unknown mode: series
```

### Diagnosis
**Incomplete mode name** - Missing element type

### Solution
```matlab
❌ Wrong modes:
TLine('series', ...)       // Incomplete
TLine('shunt', ...)        // Incomplete
TLine('stub_short', ...)   // Wrong format
TLine('QWT', ...)          // Typo

✅ Correct modes:
TLine('series_C', ...)     // Series capacitor
TLine('series_L', ...)     // Series inductor
TLine('shunt_C', ...)      // Shunt capacitor
TLine('shunt_L', ...)      // Shunt inductor
TLine('stub', ...)         // Stub design
TLine('QW', ...)           // Quarter-wave
TLine('load', ...)         // Find load (Q13/Q14)
```

---

## Problem 7: Doesn't Match Manual

### Symptoms
```matlab
% Manual: Z_in = 50 + j25
>> r = TLine(50, 100, 0.3);
>> r.Z_in
ans = 48.5 + j26.3   % Close but not exact
```

### Diagnosis
**Rounding differences** or **different formula**

### Solution
**Check your formula:**
```matlab
% TLine uses:
% Z_in = Z0 * (ZL + jZ0*tan(βℓ)) / (Z0 + jZL*tan(βℓ))

% Verify step by step:
beta_l = 2*pi*len_lambda;
tan_bl = tan(beta_l);
Z_in_manual = Z0 * (ZL + 1j*Z0*tan_bl) / (Z0 + 1j*ZL*tan_bl);
fprintf('Manual: %.2f %+.2fj\n', real(Z_in_manual), imag(Z_in_manual));
fprintf('TLine:  %.2f %+.2fj\n', real(r.Z_in), imag(r.Z_in));
```

**Common sources:**
- Using degrees instead of radians
- Rounding π
- Different tan calculation
- Forgetting j in formula

---

## 🔧 Diagnostic Script

```matlab
fprintf('=== TLine.m Diagnostic ===\n\n');

% Test 1: Basic λ/4
fprintf('Test 1: Quarter-wave impedance inversion\n');
r1 = TLine(50, 200, 0.25);
fprintf('  Z_in = %.2f Ω (should be 12.5 Ω)\n', r1.Z_in);

% Test 2: λ/2  
fprintf('\nTest 2: Half-wave transparency\n');
r2 = TLine(50, 200, 0.5);
fprintf('  Z_in = %.2f Ω (should be 200 Ω)\n', r2.Z_in);

% Test 3: Matched line
fprintf('\nTest 3: Matched line\n');
r3 = TLine(50, 50, 0.3);
fprintf('  VSWR = %.4f (should be 1.0)\n', r3.VSWR);
fprintf('  Gamma = %.4f (should be 0.0)\n', abs(r3.Gamma_L));

% Test 4: Q13/Q14
fprintf('\nTest 4: Find load from input\n');
Gamma_A = 0.5 * exp(1j*pi/6);
r4 = TLine('load', 50, Gamma_A, 0.2);
fprintf('  |Gamma_L| = %.4f (should be 0.5)\n', abs(r4.Gamma_L));

fprintf('\n=== All tests complete ===\n');
```

---

## ✅ Pre-Submission Checklist

Before submitting homework/exam:

- [ ] Length in correct units (λ vs meters)
- [ ] For Q13/Q14: Used `TLine('load', ...)`
- [ ] For Q11: Used correct mode ('series_C', 'series_L', etc.)
- [ ] For Q12: Used `TLine('stub', ...)`
- [ ] |Gamma| ≤ 1 always
- [ ] VSWR ≥ 1 always
- [ ] Results are physically reasonable
- [ ] Units converted for final answer

---

[← Master Index](TLine_MASTER_INDEX.md) | [Complete Guide →](TLine_Complete_Guide.md)
