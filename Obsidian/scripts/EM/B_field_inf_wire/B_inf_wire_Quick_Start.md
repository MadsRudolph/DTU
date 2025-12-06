# B_inf_wire.m - Quick Start Guide

> **2-Minute Crash Course**  
> Calculate magnetic field around a wire instantly

---

## TL;DR - The One Pattern You Need

```matlab
% Current and distance
I = 5;       % 5 Amperes
r = 0.02;    % 2 cm = 0.02 m

% Calculate B-field
B = B_inf_wire(I, r);

% Result: B in Tesla [T]
% Typical: B ≈ 50 μT
```

**That's it!** Magnetic field calculated in 10 seconds.

---

## The Essential Pattern

### Step-by-Step

```matlab
% Step 1: Define current (Amperes)
I = 10;  % 10 A

% Step 2: Define distance (meters)
r = 0.05;  % 5 cm = 0.05 m

% Step 3: Calculate
B = B_inf_wire(I, r);

% Step 4: Convert to μT if needed
B_microT = B * 1e6;

fprintf('B = %.1f μT\n', B_microT);
```

---

## Complete Example

### Problem
A wire carries 5 A of current. Find the magnetic field at:
(a) 1 cm from the wire
(b) 2 cm from the wire
(c) 5 cm from the wire

### Solution
```matlab
I = 5;  % Current in Amperes

% Distances in meters
r = [0.01, 0.02, 0.05];

% Calculate B-field
B = B_inf_wire(I, r);

>> B
B =
   1.0000e-04    5.0000e-05    2.0000e-05

% In microtesla:
>> B * 1e6
ans =
   100    50    20
```

### Answer
(a) **B = 100 μT** at 1 cm  
(b) **B = 50 μT** at 2 cm  
(c) **B = 20 μT** at 5 cm

### Verification
- Distance doubles → B-field halves ✓
- B ∝ 1/r (inverse relationship) ✓

---

## Unit Conversions

### Current Units
```matlab
% Amperes (A)
I = 5;  % 5 A

% Milliamperes (mA)
I = 500e-3;  % 500 mA = 0.5 A

% Kiloamperes (kA)
I = 0.01;  % 10 A = 0.01 kA
```

### Distance Units
```matlab
% Centimeters to meters
r = 2 * 1e-2;  % 2 cm = 0.02 m

% Millimeters to meters
r = 5 * 1e-3;  % 5 mm = 0.005 m

% Just use meters directly
r = 0.02;  % 2 cm = 0.02 m
```

### B-field Units
```matlab
% Result is in Tesla [T]
B = B_inf_wire(I, r);

% Convert to microtesla (μT)
B_uT = B * 1e6;

% Convert to millitesla (mT)
B_mT = B * 1e3;

% Convert to Gauss (G)
B_G = B * 1e4;  % 1 T = 10,000 G
```

---

## With Magnetic Material

```matlab
% Current and distance
I = 5;
r = 0.02;

% Relative permeability
mu_r = 1000;  % Iron core

% Calculate
B = B_inf_wire(I, r, mu_r);

% Result: B is 1000× larger than in air
```

---

## Multiple Distances

```matlab
% Current
I = 10;

% Array of distances
r = [0.01, 0.02, 0.03, 0.05, 0.10];  % meters

% One call for all
B = B_inf_wire(I, r);

% Results:
>> B * 1e6  % In μT
ans =
   200   100    66.7    40    20
```

---

## What You Get Back

```matlab
B = B_inf_wire(I, r);

% B: Magnetic field magnitude
%   - Scalar if r is scalar
%   - Array if r is array
%   - Units: Tesla [T]
%   - Typical range: 1-100 μT
%   - Direction: NOT included (use right-hand rule)
```

---

## Direction (Right-Hand Rule)

**B_inf_wire gives MAGNITUDE only.**

**Direction:**
1. Point thumb along current direction
2. Fingers curl around wire
3. Fingers show B-field direction

```
    Thumb → Current (I)
    Fingers → B-field circles wire
```

---

## Common Mistakes

### ❌ Mistake 1: Wrong Units

```matlab
❌ Wrong:
I = 5;  r = 2;  % Meant 2 cm but forgot conversion!
B = B_inf_wire(I, r);  % B at 2 m (way too far!)

✅ Correct:
I = 5;  r = 0.02;  % 2 cm = 0.02 m
B = B_inf_wire(I, r);
```

---

### ❌ Mistake 2: Negative Distance

```matlab
❌ Wrong:
r = -0.02;  % Negative distance!
% Error: Distance r must be positive

✅ Correct:
r = 0.02;  % Always positive
```

---

### ❌ Mistake 3: Zero Distance

```matlab
❌ Wrong:
r = 0;  % At the wire!
% Error: Distance r must be positive

✅ Correct:
r = 0.001;  % Very close, but not zero
```

---

### ❌ Mistake 4: Expecting Direction

```matlab
❌ Wrong:
B_vector = B_inf_wire(I, r);  % Expecting vector

✅ Correct:
B_magnitude = B_inf_wire(I, r);  % It's a scalar
% For direction: use right-hand rule
```

---

## Quick Formulas

### Ampère's Law

```
B = μI / (2πr)

μ = μ₀μᵣ
μ₀ = 4π × 10⁻⁷ H/m
```

### Typical Values

```
I = 1 A, r = 1 cm   → B ≈ 20 μT
I = 5 A, r = 2 cm   → B ≈ 50 μT
I = 10 A, r = 5 cm  → B ≈ 40 μT
```

**Compare:** Earth's magnetic field ≈ 50 μT

---

## ✅ 60-Second Self-Test

**Given:**
```
Wire with I = 10 A
Find B at r = 2 cm
```

**Try solving (without looking):**
```matlab
I = ?
r = ?
B = B_inf_wire(?, ?);
```

**Answer:**
```matlab
I = 10;
r = 0.02;  % 2 cm in meters
B = B_inf_wire(I, r);

% Expected: B = 1.0e-04 T = 100 μT
```

---

## Quick Checks

### Verify Inverse Relationship

```matlab
% Double distance → half B-field
B1 = B_inf_wire(10, 0.01);
B2 = B_inf_wire(10, 0.02);

% Check: B2 should equal B1/2
ratio = B1/B2;  % Should be 2.0
```

### Verify Linear in Current

```matlab
% Double current → double B-field
B1 = B_inf_wire(5, 0.02);
B2 = B_inf_wire(10, 0.02);

% Check: B2 should equal 2*B1
ratio = B2/B1;  % Should be 2.0
```

---

## 🎯 What's Next?

**Ready for exam:**
→ Print the [Quick Reference Card](B_inf_wire_Quick_Reference.md) (1 min)

**Want examples:**
→ Work through [Exam Examples](B_inf_wire_Exam_Examples.md) (8 min)

**Need theory:**
→ Read the [Complete Guide](B_inf_wire_Complete_Guide.md) (12 min)

**Having issues:**
→ Check [Troubleshooting Guide](B_inf_wire_Troubleshooting.md) (2 min)

---

## 💡 Remember

1. **Units:** Current in A, distance in m
2. **Result:** B in Tesla (often μT range)
3. **Array input:** Can calculate multiple distances
4. **Direction:** Use right-hand rule
5. **Scaling:** B ∝ 1/r (inverse)

**You're ready to calculate magnetic fields!** 🧲

---

[← Back to Master Index](B_inf_wire_MASTER_INDEX.md) | [Complete Guide →](B_inf_wire_Complete_Guide.md)
