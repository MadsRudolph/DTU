# B_inf_wire.m - Troubleshooting Guide

> **Quick Error Diagnosis**

---

## Problem 1: "Distance r must be positive" Error

### Symptoms
```matlab
>> B = B_inf_wire(5, 0);
Error: Distance r must be positive.

>> B = B_inf_wire(5, -0.02);
Error: Distance r must be positive.
```

### Diagnosis
**Distance is zero or negative**

### Solution
```matlab
❌ Wrong:
r = 0;      % At the wire
r = -0.02;  % Negative distance

✅ Correct:
r = 0.001;  % Very close, but positive
r = 0.02;   % Positive distance
```

**Rule:** Distance must be r > 0

---

## Problem 2: B-field Way Too Large

### Symptoms
```matlab
>> B = B_inf_wire(5, 2);
B = 5.0000e-07  % Only 0.5 μT (way too small!)

% Or:
>> B = B_inf_wire(500, 0.02);
B = 0.0050  % 5 mT (way too large!)
```

### Diagnosis
**Wrong units** - forgot conversions

### Solution
```matlab
❌ Wrong:
I = 500;  % Meant 500 mA but forgot to convert!
r = 2;    % Meant 2 cm but this is 2 m!

✅ Correct:
I = 500e-3;  % 500 mA = 0.5 A
r = 0.02;    % 2 cm = 0.02 m

B = B_inf_wire(I, r);
```

**Checklist:**
- Current in **Amperes** (use e-3 for mA)
- Distance in **meters** (use e-2 for cm)
- Result in **Tesla** (multiply by 1e6 for μT)

---

## Problem 3: Getting Array When Expected Scalar

### Symptoms
```matlab
>> r = [0.01, 0.02];
>> B = B_inf_wire(5, r);
B =
   1.0e-04  5.0e-05  % Got array, expected scalar!
```

### Diagnosis
**r is an array** - function returns array

### Solution
```matlab
% If you want a single value:
r = 0.01;  % Scalar input
B = B_inf_wire(5, r);  % Scalar output

% If you want multiple values (this is a feature!):
r = [0.01, 0.02, 0.05];
B = B_inf_wire(5, r);  % Array output
```

**This is not an error** - it's a feature for calculating multiple distances!

---

## Problem 4: Result Seems Wrong

### Symptoms
```matlab
>> B = B_inf_wire(10, 0.01);
B = 2.0e-04

% Is this right? Expected something else...
```

### Diagnosis
**Need to verify calculation**

### Solution
```matlab
% Manual calculation:
I = 10;  % A
r = 0.01;  % m
mu0 = 4*pi*1e-7;

B_manual = mu0 * I / (2*pi*r);

fprintf('Function: B = %.4e T\n', B);
fprintf('Manual:   B = %.4e T\n', B_manual);

% Should match!
```

**Quick check:**
```matlab
% I = 10 A, r = 1 cm → B should be ~200 μT
B_uT = B * 1e6;
fprintf('B = %.0f μT\n', B_uT);
% Should get: B = 200 μT
```

---

## Problem 5: Don't Know Direction

### Symptoms
```
"The function only gives me magnitude. Where does B point?"
```

### Diagnosis
**B_inf_wire returns magnitude only**

### Solution

**Use right-hand rule:**

```
1. Point thumb along current direction
2. Curl fingers around wire
3. Fingers show B-field direction
```

**Example:**
```matlab
% Wire along z-axis, current in +z direction
% At point (x=1cm, y=0, z=0):

B_mag = B_inf_wire(5, 0.01);  % Magnitude

% Direction: B points in -y direction
% (Fingers curl from +x toward -y)
```

**The function gives:**
- ✅ Magnitude: |B| = μI/(2πr)
- ❌ Direction: Use right-hand rule

---

## 🔧 Diagnostic Script

```matlab
fprintf('=== B_inf_wire Diagnostic ===\n\n');

% Test 1: Standard calculation
I = 10;  % 10 A
r = 0.01;  % 1 cm

B = B_inf_wire(I, r);

fprintf('Test 1: Standard calculation\n');
fprintf('  I = %g A, r = %g m\n', I, r);
fprintf('  B = %.4e T = %.1f μT\n', B, B*1e6);
fprintf('  Expected: ~200 μT\n');
if abs(B*1e6 - 200) < 1
    fprintf('  ✓ PASS\n\n');
else
    fprintf('  ✗ FAIL\n\n');
end

% Test 2: Array input
r_array = [0.01, 0.02, 0.05];
B_array = B_inf_wire(10, r_array);

fprintf('Test 2: Array input\n');
fprintf('  Distances: ');
fprintf('%.2f m  ', r_array);
fprintf('\n');
fprintf('  B-fields:  ');
fprintf('%.0f μT  ', B_array*1e6);
fprintf('\n');
fprintf('  Expected: 200 μT, 100 μT, 40 μT\n');
fprintf('  ✓ PASS\n\n');

% Test 3: Inverse relationship
B1 = B_inf_wire(10, 0.01);
B2 = B_inf_wire(10, 0.02);

fprintf('Test 3: Inverse relationship (r doubles)\n');
fprintf('  B1 = %.0f μT (at 1 cm)\n', B1*1e6);
fprintf('  B2 = %.0f μT (at 2 cm)\n', B2*1e6);
fprintf('  Ratio B1/B2 = %.2f\n', B1/B2);
fprintf('  Expected: 2.00\n');
if abs(B1/B2 - 2) < 0.01
    fprintf('  ✓ PASS\n\n');
else
    fprintf('  ✗ FAIL\n\n');
end

% Test 4: Linear in current
B1 = B_inf_wire(5, 0.02);
B2 = B_inf_wire(10, 0.02);

fprintf('Test 4: Linear in current (I doubles)\n');
fprintf('  B1 = %.0f μT (I = 5 A)\n', B1*1e6);
fprintf('  B2 = %.0f μT (I = 10 A)\n', B2*1e6);
fprintf('  Ratio B2/B1 = %.2f\n', B2/B1);
fprintf('  Expected: 2.00\n');
if abs(B2/B1 - 2) < 0.01
    fprintf('  ✓ PASS\n\n');
else
    fprintf('  ✗ FAIL\n\n');
end

fprintf('=== Tests complete ===\n');
```

---

## ✅ Pre-Submission Checklist

- [ ] Current in Amperes (use e-3 for mA)
- [ ] Distance in meters (use e-2 for cm)
- [ ] Distance is positive (r > 0)
- [ ] Result in Tesla (multiply by 1e6 for μT)
- [ ] Typical range check: 1-100 μT for normal cases
- [ ] Direction from right-hand rule (not from function)
- [ ] Scaling verified:
  - Double distance → half B-field
  - Double current → double B-field

---

## 💡 Quick Fixes

### Fix 1: Convert Units Automatically
```matlab
% Define helper for unit conversion
cm2m = @(x) x * 1e-2;
mA2A = @(x) x * 1e-3;
T2uT = @(x) x * 1e6;

% Use:
I = mA2A(500);  % 500 mA → 0.5 A
r = cm2m(2);    % 2 cm → 0.02 m
B = B_inf_wire(I, r);
B_uT = T2uT(B);  % Convert to μT
```

### Fix 2: Sanity Check Function
```matlab
function check_B(I, r, B)
    % Quick sanity check
    expected = 4*pi*1e-7 * I / (2*pi*r);
    error = abs(B - expected) / expected * 100;
    
    fprintf('Current: %g A\n', I);
    fprintf('Distance: %g m\n', r);
    fprintf('B-field: %.1f μT\n', B*1e6);
    fprintf('Error: %.2f%%\n', error);
    
    if error < 1
        fprintf('✓ Calculation OK\n');
    else
        fprintf('✗ Check your inputs!\n');
    end
end
```

### Fix 3: Verify Direction (Conceptual)
```matlab
% For wire along z-axis, current in +z
% B-field at point (x, y, 0):

% Magnitude from function
B_mag = B_inf_wire(I, sqrt(x^2 + y^2));

% Direction from right-hand rule:
% - Thumb: +z (current direction)
% - Fingers curl in xy-plane
% - At (x,y): B points in tangent direction

% Tangent to circle at (x,y): perpendicular to radial
B_direction = [-y; x; 0] / sqrt(x^2 + y^2);

% Full vector
B_vector = B_mag * B_direction;
```

---

[← Master Index](B_inf_wire_MASTER_INDEX.md)
