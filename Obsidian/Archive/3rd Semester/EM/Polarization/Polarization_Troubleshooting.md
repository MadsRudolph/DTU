# Polarization.m - Troubleshooting Guide

> **Quick Error Diagnosis and Fixes**

---

## 🔍 Error Quick Finder

1. [[#Problem 1: Wrong Handedness|Wrong handedness (RHCP vs LHCP)]]
2. [[#Problem 2: AR is NaN or Wrong|AR is NaN or wrong]]
3. [[#Problem 3: Wrong Type|Type is wrong (expected circular, got elliptical)]]
4. [[#Problem 4: Undefined Function|Error: "Undefined function"]]
5. [[#Problem 5: Doesn't Match Manual|Results don't match manual calculation]]

---

## Problem 1: Wrong Handedness

### Symptoms
```matlab
>> r = Polarization([1; 1j; 0]);
>> r.handedness
ans = 'LHCP'   % Expected RHCP!
```

### Diagnosis
**Wrong sign for y-component**

### Solution
```matlab
❌ Wrong:
F = [1; 1j; 0];    % LHCP (plus j)

✅ Correct for RHCP:
F = [1; -1j; 0];   % RHCP (minus j)
```

### Rule
**For +z propagation:**
- RHCP → use `-j`
- LHCP → use `+j`

**Memory:** RHCP = **R**ight = **-**j (minus)

---

## Problem 2: AR is NaN or Wrong

### Symptoms
```matlab
>> r = Polarization([0; 0; 0]);
>> r.AR
ans = NaN
```

### Diagnosis
**Zero field vector**

### Solution
```matlab
❌ Wrong:
F = [0; 0; 0];     % Zero vector

✅ Correct:
F = [1; -1j; 0];   % Non-zero phasor
```

### Check
```matlab
if norm(F) < 1e-10
    error('Field vector is too small');
end
```

---

## Problem 3: Wrong Type

### Symptoms
```matlab
>> r = Polarization([1; -1.01j; 0]);
>> r.type
ans = 'Elliptical'   % Expected Circular!
```

### Diagnosis
**Numerical precision** - not exactly equal magnitudes

### Solution
```matlab
% For circular: |Ex| must exactly equal |Ey|
✅ Exact circular:
F = [1; -1j; 0];      % |1| = |-1j| = 1

❌ Almost circular:
F = [1; -1.01j; 0];   % |1| ≠ |1.01j|
% This is slightly elliptical
```

### Check AR
```matlab
if abs(r.AR - 1) < 0.01
    disp('Nearly circular (AR ≈ 1)');
end
```

---

## Problem 4: Undefined Function

### Symptoms
```matlab
>> Polarization([1; -1j; 0])
Error: Undefined function or variable 'Polarization'.
```

### Diagnosis
**Function not in path** or **typo**

### Solution
```matlab
% 1. Add path
addpath('path/to/helpers');

% 2. Check spelling
❌ Wrong:
polarization([1; -1j; 0])  % lowercase 'p'

✅ Correct:
Polarization([1; -1j; 0])  % Capital 'P'
```

---

## Problem 5: Doesn't Match Manual

### Symptoms
```matlab
% Manual: RHCP
>> r = Polarization([1; 1j; 0]);
>> r.handedness
ans = 'LHCP'   % Different from manual!
```

### Diagnosis
**Different handedness convention**

### Solution
**Check convention used:**
- **IEEE (this tool):** Looking along k̂ direction
- **Physics:** Looking against k̂ direction

```matlab
% IEEE convention (Polarization.m uses this):
% RHCP in +z: E rotates clockwise looking in +z direction
F_RHCP = [1; -1j; 0];

% If your textbook uses opposite convention:
% Swap RHCP ↔ LHCP interpretations
```

---

## 🔧 Diagnostic Script

```matlab
fprintf('=== Polarization.m Diagnostic ===\n\n');

% Test 1: RHCP
fprintf('Test 1: RHCP\n');
r1 = Polarization([1; -1j; 0]);
fprintf('  Type: %s (should be Circular)\n', r1.type);
fprintf('  Hand: %s (should be RHCP)\n', r1.handedness);
fprintf('  AR: %.2f (should be 1.00)\n\n', r1.AR);

% Test 2: LHCP
fprintf('Test 2: LHCP\n');
r2 = Polarization([1; 1j; 0]);
fprintf('  Type: %s (should be Circular)\n', r2.type);
fprintf('  Hand: %s (should be LHCP)\n', r2.handedness);
fprintf('  AR: %.2f (should be 1.00)\n\n', r2.AR);

% Test 3: Linear
fprintf('Test 3: Linear\n');
r3 = Polarization([1; 1; 0]);
fprintf('  Type: %s (should be Linear)\n', r3.type);
fprintf('  Hand: %s (should be N/A)\n', r3.handedness);
fprintf('  AR: %g (should be Inf)\n\n', r3.AR);

fprintf('=== All tests complete ===\n');
```

---

## ✅ Pre-Submission Checklist

- [ ] Used column vectors (semicolons)
- [ ] Correct sign for RHCP/LHCP
- [ ] Non-zero field vector
- [ ] Checked output type matches expectation
- [ ] AR makes sense (1, ∞, or between)
- [ ] Handedness convention understood

---

[← Master Index](Polarization_MASTER_INDEX.md)
