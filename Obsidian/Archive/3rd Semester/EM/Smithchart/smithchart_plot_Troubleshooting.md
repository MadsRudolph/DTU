# smithchart_plot.m - Troubleshooting Guide

> **Quick Error Diagnosis**

---

## Problem 1: "Undefined function 'smithplot'"

### Symptoms
```matlab
>> smithchart_plot(50, 100)
Warning: RF Toolbox not found, using manual Smith chart
[Chart appears anyway]
```

### Diagnosis
**No RF Toolbox installed** - This is NOT an error!

### Solution
**Nothing needed!** The function automatically draws its own Smith chart.

**Note:** This warning is informational only. The chart works perfectly without RF Toolbox.

---

## Problem 2: Point Not Visible

### Symptoms
```matlab
>> smithchart_plot(50, 100)
% Chart appears but no red point
```

### Diagnosis
**Point exactly at edge or outside unit circle**

### Solution
Check console output for |Γ|:
```matlab
% If |Γ| > 1:
% Load has negative resistance (unusual)
% Or calculation error

% Verify inputs:
Z0 = 50;
ZL = 100;  % Should be complex for most cases

% Recalculate:
smithchart_plot(Z0, ZL)
```

---

## Problem 3: Wrong Argument Error

### Symptoms
```matlab
>> smithchart_plot(100)
Error: Not enough input arguments
```

### Diagnosis
**Missing Z₀ or Z_L**

### Solution
```matlab
❌ Wrong:
smithchart_plot(100)  % Only one argument

✅ Correct:
smithchart_plot(50, 100)  % Z₀, Z_L
```

**Rule:** Need both Z₀ and Z_L (or use 'Gamma' mode)

---

## Problem 4: Point in Wrong Location

### Symptoms
```matlab
% Expected upper half, got lower half
```

### Diagnosis
**Sign error in imaginary part**

### Solution
```matlab
% Check your Z_L sign:
❌ ZL = 100 - 1j*50  % Capacitive (lower half)
✅ ZL = 100 + 1j*50  % Inductive (upper half)

% MATLAB imaginary unit:
✅ 1j or 1i  % Correct
❌ j or i    % May be variables!
```

---

## Problem 5: Multiple Points Not Showing

### Symptoms
```matlab
smithchart_plot(50, 100);
smithchart_plot(50, 50);  % Only second point shows
```

### Diagnosis
**Forgot `hold on`**

### Solution
```matlab
❌ Wrong:
smithchart_plot(50, 100);
smithchart_plot(50, 50);  % Replaces first

✅ Correct:
smithchart_plot(50, 100);
hold on
smithchart_plot(50, 50);  % Adds to chart
hold off
```

---

## 🔧 Diagnostic Script

```matlab
fprintf('=== smithchart_plot Diagnostic ===\n\n');

% Test 1: Matched load (center)
Z0 = 50;
ZL = 50;
smithchart_plot(Z0, ZL, 'Matched');
fprintf('Expected: Point at center (Gamma = 0)\n\n');
pause(2);

% Test 2: Open (right edge)
figure;
smithchart_plot(50, 1e6, 'Open');  % Very high Z ≈ open
fprintf('Expected: Point near right edge (Gamma ≈ 1)\n\n');
pause(2);

% Test 3: Short (left edge)
figure;
smithchart_plot(50, 0.001, 'Short');  % Very low Z ≈ short
fprintf('Expected: Point near left edge (Gamma ≈ -1)\n\n');

% Test 4: Complex impedance
figure;
smithchart_plot(50, 100 + 1j*50, 'Load');
fprintf('Expected: Point in upper right quadrant\n\n');

fprintf('=== Tests complete ===\n');
```

---

## ✅ Pre-Submission Checklist

- [ ] Used correct syntax: `smithchart_plot(Z0, ZL)`
- [ ] Z₀ comes first, Z_L second
- [ ] Used 1j or 1i for imaginary unit
- [ ] Check console for Γ values
- [ ] Used `hold on` for multiple points
- [ ] Sign of reactance correct (+j inductive, -j capacitive)
- [ ] If using Gamma mode, included 'Gamma' keyword

---

## 💡 Quick Fixes

### Chart Doesn't Appear
```matlab
% Make sure figure window isn't hidden
% Try:
figure;
smithchart_plot(Z0, ZL);
```

### Values Look Wrong
```matlab
% Check console output:
% Console shows z_L and Γ
% Verify these match your expectations
```

### Can't See Label
```matlab
% Label might be off-screen
% Try shorter label or different point
smithchart_plot(Z0, ZL, 'ZL');  % Short label
```

---

[← Master Index](smithchart_plot_MASTER_INDEX.md)
