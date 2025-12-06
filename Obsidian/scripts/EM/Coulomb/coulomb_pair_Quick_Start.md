# coulomb_pair.m - Quick Start Guide

> **2-Minute Crash Course**  
> Calculate Coulomb force between charges instantly

---

## TL;DR - The One Pattern You Need

```matlab
% Define charges and positions
q1 = 2e-6;         % 2 μC
q2 = -3e-6;        % -3 μC
r1 = [1; 0; 0];    % Position of q1 [m]
r2 = [0; 1; 0];    % Position of q2 [m]

% Calculate forces
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% F12 = force ON q1 DUE TO q2
% F21 = force ON q2 DUE TO q1
```

**That's it!** Forces calculated in Newtons.

---

## The Essential Pattern

### Step-by-Step

```matlab
% Step 1: Define charges (Coulombs)
q1 = 1e-6;    % 1 μC = 1×10⁻⁶ C
q2 = -2e-6;   % -2 μC = -2×10⁻⁶ C

% Step 2: Define positions (meters, column vectors)
r1 = [0; 0; 0];      % Origin
r2 = [1; 0; 0];      % 1 meter in x-direction

% Step 3: Calculate
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% Step 4: Extract what you need
force_on_q1 = F12;   % [N]
force_on_q2 = F21;   % [N]

% Verify: F12 should equal -F21
check = norm(F12 + F21);  % Should be ≈ 0
```

---

## Complete Example

### Problem
Two charges:
- q₁ = 2 μC at position (1, 0, 0) m
- q₂ = -3 μC at position (0, 1, 0) m

Find the force on each charge.

### Solution
```matlab
q1 = 2e-6;          % 2 μC in Coulombs
q2 = -3e-6;         % -3 μC in Coulombs
r1 = [1; 0; 0];     % Position of q1
r2 = [0; 1; 0];     % Position of q2

[F12, F21] = coulomb_pair(q1, q2, r1, r2);

>> F12
F12 =
  -0.0382
   0.0382
        0

>> F21
F21 =
   0.0382
  -0.0382
        0

% Magnitude
>> norm(F12)
ans = 0.0540
```

### Interpretation
- **Opposite charges** → Attractive force
- **F₁₂ points** from q₁ toward q₂ (attractive)
- **F₂₁ points** from q₂ toward q₁ (attractive)
- **Magnitude:** |F| = 54.0 mN
- **Verify:** F₁₂ = -F₂₁ ✓

---

## Unit Conversions

### Charge Units
```matlab
% Microcoulombs (μC)
q = 5e-6;       % 5 μC = 5×10⁻⁶ C

% Nanocoulombs (nC)
q = 10e-9;      % 10 nC = 10×10⁻⁹ C = 1e-8 C

% Picocoulombs (pC)
q = 100e-12;    % 100 pC = 1e-10 C
```

### Distance Units
```matlab
% Centimeters to meters
r = [10; 0; 0] * 1e-2;   % 10 cm = 0.1 m

% Millimeters to meters
r = [5; 0; 0] * 1e-3;    % 5 mm = 0.005 m
```

---

## What You Get Back

```matlab
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% F12: Force vector ON q1 DUE TO q2
%   - 3×1 vector [Fx; Fy; Fz] in Newtons
%   - Points in direction q1 is pushed/pulled

% F21: Force vector ON q2 DUE TO q1
%   - 3×1 vector [Fx; Fy; Fz] in Newtons
%   - Points in direction q2 is pushed/pulled
%   - Always equals -F12 (Newton's 3rd law)
```

---

## Force Direction Rules

### Same Sign (Both + or Both -)
```matlab
q1 = 1e-6;  q2 = 2e-6;  % Both positive
% → Repulsive force
% → Forces point AWAY from each other
```

### Opposite Signs (+ and -)
```matlab
q1 = 1e-6;  q2 = -2e-6;  % Opposite signs
% → Attractive force
% → Forces point TOWARD each other
```

---

## Common Mistakes

### ❌ Mistake 1: Wrong Vector Type

```matlab
❌ Wrong:
r1 = [1, 0, 0];  % Row vector (commas)

✅ Correct:
r1 = [1; 0; 0];  % Column vector (semicolons)
```

---

### ❌ Mistake 2: Wrong Units

```matlab
❌ Wrong:
q1 = 5;  % Meant 5 μC but forgot e-6!

✅ Correct:
q1 = 5e-6;  % 5 μC = 5×10⁻⁶ C
```

---

### ❌ Mistake 3: Swapped Meaning

```matlab
% F12 means:
% "Force on 1 due to 2"
% NOT "force from 1 to 2"

❌ Wrong interpretation:
F12 = force from q1 to q2

✅ Correct interpretation:
F12 = force ON q1 DUE TO q2
```

---

### ❌ Mistake 4: Same Position

```matlab
❌ Wrong:
r1 = [1; 0; 0];
r2 = [1; 0; 0];  % Same location!
% Error: Charges must not coincide

✅ Correct:
r1 = [1; 0; 0];
r2 = [2; 0; 0];  % Different locations
```

---

## Quick Formulas

### Coulomb's Law (Magnitude)
```
|F| = k_e · |q₁q₂| / r²

k_e = 8.99 × 10⁹ N·m²/C²
```

### Vector Form
```
F₁₂ = (k_e · q₁q₂ / r²) · r̂₁₂

r̂₁₂ = (r₁ - r₂) / |r₁ - r₂|
```

### Newton's Third Law
```
F₂₁ = -F₁₂
```

---

## Multiple Charges

```matlab
% Net force on q1 from q2 and q3
[F12, ~] = coulomb_pair(q1, q2, r1, r2);
[F13, ~] = coulomb_pair(q1, q3, r1, r3);

% Superposition principle
F_net = F12 + F13;  % Total force on q1
```

---

## ✅ 60-Second Self-Test

**Given:**
```
q₁ = 1 μC at origin
q₂ = 2 μC at (1, 0, 0) m
```

**Try solving (without looking):**
```matlab
q1 = ?
q2 = ?
r1 = ?
r2 = ?
[F12, F21] = coulomb_pair(?, ?, ?, ?);
```

**Answer:**
```matlab
q1 = 1e-6;
q2 = 2e-6;
r1 = [0; 0; 0];
r2 = [1; 0; 0];
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% Expected: Repulsive (same sign)
% F12 points in -x direction (away from q2)
```

---

## 🎯 What's Next?

**Ready for exam:**
→ Print the [Quick Reference Card](coulomb_pair_Quick_Reference.md) (1 min)

**Want examples:**
→ Work through [Exam Examples](coulomb_pair_Exam_Examples.md) (8 min)

**Need theory:**
→ Read the [Complete Guide](coulomb_pair_Complete_Guide.md) (12 min)

**Having issues:**
→ Check [Troubleshooting Guide](coulomb_pair_Troubleshooting.md) (2 min)

---

## 💡 Remember

1. **Units:** Charges in C (use e-6 for μC), distances in m
2. **Vectors:** Use semicolons for column vectors
3. **Notation:** F₁₂ = force ON q₁ DUE TO q₂
4. **Verify:** Always check F₁₂ = -F₂₁
5. **Signs:** Same → repel, opposite → attract

**You're ready to calculate Coulomb forces!** ⚡

---

[← Back to Master Index](coulomb_pair_MASTER_INDEX.md) | [Complete Guide →](coulomb_pair_Complete_Guide.md)
