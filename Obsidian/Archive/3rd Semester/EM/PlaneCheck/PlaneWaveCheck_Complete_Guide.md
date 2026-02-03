# PlaneWaveCheck Complete Guide

> **Purpose:** Comprehensive reference for plane wave verification  
> **Based on:** Course Formelsamling Section 4 - "How to Check if Plane Wave"

---

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples →](PlaneWaveCheck_Exam_Examples.md)

---

## ⚠️ Which Mode Should I Use?

```
What format is your problem?
│
├─► γ = [j...; ...; ...] given separately    (FORMAT A)
│   │
│   │   Example: E₀ = [2;0;0], H₀ = [0;-5.3e-3;0], γ = [0;0;j3]
│   │
│   └─► Use MAXWELL mode
│       PlaneWaveCheck('maxwell', E0, H0, gamma)
│
└─► exp(-j(ax + by + cz)) in field expression (FORMAT B)
    │
    │   Example: E = E₀[0;j;0] exp(-j(20x+10z))
    │
    └─► Use FULL mode
        PlaneWaveCheck('full', E, H, k, eta)
```

**⚠️ Basic mode is only a quick sanity check - it CANNOT confirm a plane wave!**

---

## Table of Contents

1. [Theory: What Makes a Plane Wave](#1-theory-what-makes-a-plane-wave)
2. [The 5-Step Verification Method](#2-the-5-step-verification-method)
3. [Usage Modes](#3-usage-modes)
4. [Extracting Vectors from Phasors](#4-extracting-vectors-from-phasors)
5. [Numerical Tolerance](#5-numerical-tolerance)
6. [Output Fields Reference](#6-output-fields-reference)
7. [Complete Examples](#7-complete-examples)

---

## 1. Theory: What Makes a Plane Wave

A **uniform plane wave** is a TEM (Transverse Electromagnetic) wave where:
- Electric and magnetic fields are perpendicular to the direction of propagation
- Fields are uniform in planes perpendicular to propagation
- E and H are perpendicular to each other
- Field magnitudes are related by the intrinsic impedance

### Maxwell's Equations Implications

For a plane wave propagating in direction k̂:

```
∇ × E = -jωμH    →    k × E = ωμH
∇ × H = jωεE     →    k × H = -ωεE
∇ · E = 0        →    k · E = 0
∇ · H = 0        →    k · H = 0
```

These lead to the fundamental plane wave conditions checked by `PlaneWaveCheck`.

---

## 2. The 5-Step Verification Method

Based on Formelsamling Section 4:

### Step 1: Orthogonality Check (Guideline #1)

Three dot products must all equal zero:

| Condition | Physical Meaning | Formula |
|-----------|-----------------|---------|
| k · E = 0 | E is transverse (perpendicular to propagation) | ∇ · E = 0 |
| k · H = 0 | H is transverse (perpendicular to propagation) | ∇ · H = 0 |
| E · H = 0 | E and H are perpendicular to each other | TEM wave |

**MATLAB Tip:** Use tolerance for floating-point comparison:
```matlab
tol = 1e-6;  % Recommended tolerance
pass = abs(dot(k, E)) < tol;
```

### Step 2: Normalize k (Guideline #2)

Before checking cross-product relations, normalize the wave vector:

```matlab
k_hat = k / norm(k);  % Unit vector in propagation direction
```

**Why?** The field relationships use direction, not magnitude of the phase constant.

### Step 3: Impedance Relation (Guideline #3)

The magnetic field must satisfy:

```
H = (1/η)(k̂ × E)
```

Or equivalently:
```
E = -η(k̂ × H)
```

**Impedance values:**
- Free space: η₀ = √(μ₀/ε₀) ≈ 377 Ω
- Lossless dielectric: η = √(μ/ε) = η₀/√(εᵣ)
- Lossy medium: ηc is complex

### Step 4: Right-Hand Rule (Guideline #4)

The Poynting vector must point in the propagation direction:

```
S = E × H    must be parallel to k
(E × H) · k > 0    (positive dot product)
```

This verifies power flows in the +k direction.

### Step 5: Phasor Phase Consistency (Guideline #5)

For lossless media, E and H phasors should be in phase. For lossy media, the phase difference relates to the complex impedance angle.

This is implicitly checked in Step 3 when η is complex.

---

## 3. Usage Modes

### Mode Decision Summary

| Problem Format | Mode | Can Confirm? | Can Rule Out? |
|----------------|------|--------------|---------------|
| γ given explicitly | `'maxwell'` | ✓ Yes | ✓ Yes |
| exp(-j...) term | `'full'` | ✓ Yes | ✓ Yes |
| Quick sanity check | basic | ✗ No | ✓ Yes |

### Full Mode (For Format B: exp term problems)

Complete verification including orthogonality, impedance, and Poynting checks:

```matlab
% Syntax
result = PlaneWaveCheck('full', E, H, k)        % η = 377 Ω
result = PlaneWaveCheck('full', E, H, k, eta)   % custom η

% Example - free space
E = [10; 0; 0];           % 10 V/m
H = [0; 10/377; 0];       % H = E/η₀
k = [0; 0; 5];
result = PlaneWaveCheck('full', E, H, k);

% Example - dielectric (εᵣ = 4, η = 377/2 = 188.5 Ω)
eta_dielectric = 377 / sqrt(4);
result = PlaneWaveCheck('full', E, H, k, eta_dielectric);
```

**Use when:** Problem gives fields as `E = E₀·exp(-j(kx·x + ky·y + kz·z))`

### Maxwell Mode (For Format A: γ given explicitly)

For complex phasor fields, use Maxwell mode which verifies the actual Maxwell equations:

```matlab
% Syntax
result = PlaneWaveCheck('maxwell', E0, H0, gamma)

% gamma is the COMPLEX propagation vector (e.g., γ = jβ for lossless)
```

**What Maxwell mode checks:**

1. **Transverse conditions:** γ · E₀ = 0, γ · H₀ = 0
2. **Maxwell relations:**
   - γ × H₀ = -jωε E₀
   - γ × E₀ = +jωμ H₀
3. **Physical sanity:** ωε and ωμ must be REAL, POSITIVE, and CONSISTENT

**Use when:** Problem gives E₀, H₀, and γ as separate vectors.

**Example - NOT a plane wave (Q1 type):**

```matlab
E0 = [2; 0; 0];              % V/m
H0 = [0; -5.309e-3; 0];      % A/m
gamma = [0; 0; 1j*3];        % γ = jβẑ

result = PlaneWaveCheck('maxwell', E0, H0, gamma);
% Fields are orthogonal, BUT ωε is NEGATIVE!
% → NOT a plane wave (would require unphysical ε < 0)
```

**Example - Valid plane wave (Q2 type):**

```matlab
E0 = [0; 1j*2; 5];               % Complex phasor
H0 = [0; -37.5e-3; 1j*15e-3];    % Complex phasor
gamma = [1j*10; 0; 0];           % γ = jβx̂

result = PlaneWaveCheck('maxwell', E0, H0, gamma);
% ωε = 0.075, ωμ = 0.02 (both positive)
% → IS a valid plane wave!
```

**When to use Maxwell mode:**
- Complex phasor fields (Q1/Q2 type problems)
- When basic mode says "valid" but you're unsure
- To verify physical realizability in a real medium

---

## 4. Extracting Vectors from Phasors

### Extracting k from Phase Terms

The wave vector k comes from the spatial phase term:

| Field Expression | Phase Term | k Vector |
|-----------------|------------|----------|
| E₀ e^(-jβz) | -jβz | [0; 0; β] |
| E₀ e^(-j(20x+10z)) | -j(20x+10z) | [20; 0; 10] |
| E₀ e^(-j(k_x·x + k_y·y + k_z·z)) | general | [k_x; k_y; k_z] |

**Pattern:** Coefficient of each spatial variable becomes that component of k.

### Extracting Directions from Field Phasors

**Critical:** The imaginary unit j in a phasor represents **phase**, not direction!

| Phasor | Direction | Explanation |
|--------|-----------|-------------|
| ĵ5e^(-jφ) | ŷ | "ĵ" is the ŷ unit vector |
| [0; j5; 0] | ŷ | j is phase (90°), direction is ŷ |
| [10; 0; 0] | x̂ | Real coefficient, x-direction |
| [1; -j; 0] | x̂-ŷ plane | Circular polarization |

**Rule:** Extract the **magnitude** of each component to get direction.

---

## 5. Numerical Tolerance

### Why Tolerance Matters

Floating-point arithmetic rarely gives exact zeros:
```matlab
dot([1;0;0], [0;1;0])  % Might give 1e-16, not exactly 0
```

### Recommended Tolerance

The script uses `tol = 1e-6` as recommended in the Formelsamling MATLAB tip.

Tolerance is scaled by vector magnitudes:
```matlab
scale = max([norm(k), norm(E), norm(H), 1]);
tol_scaled = 1e-6 * scale;
```

### Impedance Tolerance

For Step 3 (impedance check), uses 1% relative tolerance:
```matlab
impedance_error = norm(H - H_expected) / norm(H_expected);
pass = impedance_error < 0.01;  % 1% tolerance
```

---

## 6. Output Fields Reference

### All Modes

| Field | Type | Description |
|-------|------|-------------|
| `is_plane_wave` | boolean | Final verdict |
| `full_mode` | boolean | Whether full verification was used |
| `tolerance` | double | Numerical tolerance used |

### Input Vectors

| Field | Type | Description |
|-------|------|-------------|
| `E_vec` | [3×1] | Electric field vector |
| `H_vec` | [3×1] | Magnetic field vector |
| `k_vec` | [3×1] | Wave vector |

### Step 1: Orthogonality

| Field | Type | Description |
|-------|------|-------------|
| `k_dot_E` | double | k · E (should be ≈ 0) |
| `k_dot_H` | double | k · H (should be ≈ 0) |
| `E_dot_H` | double | E · H (should be ≈ 0) |
| `cond1_pass` | boolean | k · E ≈ 0? |
| `cond2_pass` | boolean | k · H ≈ 0? |
| `cond3_pass` | boolean | E · H ≈ 0? |
| `orthogonality_pass` | boolean | All three pass? |

### Step 2: Normalization

| Field | Type | Description |
|-------|------|-------------|
| `k_hat` | [3×1] | Unit vector k̂ = k/|k| |
| `k_mag` | double | Magnitude |k| |

### Step 3: Impedance (Full Mode Only)

| Field | Type | Description |
|-------|------|-------------|
| `eta` | double | Intrinsic impedance used |
| `H_expected` | [3×1] | Expected H = (1/η)(k̂ × E) |
| `impedance_error` | double | Relative error |
| `cond4_pass` | boolean | Impedance relation satisfied? |

### Step 4: Poynting Vector

| Field | Type | Description |
|-------|------|-------------|
| `poynting_vec` | [3×1] | S = E × H |
| `poynting_dot_k` | double | (E × H) · k |
| `cond5_pass` | boolean | Power flows in +k direction? (Full mode) |

---

## 7. Complete Examples

### Example 1: Standard Plane Wave (Valid)

```matlab
% E in x̂, H in ŷ, propagating in +ẑ
E = [1; 0; 0];
H = [0; 1; 0];
k = [0; 0; 10];

result = PlaneWaveCheck(E, H, k);
% Output: IS a plane wave ✓
```

### Example 2: E24 Q18 (Invalid)

```matlab
% E in ŷ, H in ẑ, k = 20x̂ + 10ẑ
E_dir = [0; 1; 0];
H_dir = [0; 0; 1];
k_vec = [20; 0; 10];

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
% Output: NOT a plane wave
% Reason: k · H = 10 ≠ 0 (H not transverse!)
```

### Example 3: Full Verification - Correct

```matlab
% Proper plane wave with correct magnitudes
E = [10; 0; 0];           % 10 V/m in x̂
H = [0; 10/377; 0];       % H = E/η₀ in ŷ
k = [0; 0; 5];            % Propagating in ẑ

result = PlaneWaveCheck('full', E, H, k);
% Output: IS a plane wave ✓
% All 5 conditions satisfied
```

### Example 4: Full Verification - Wrong H Magnitude

```matlab
% Orthogonality OK, but wrong H magnitude
E = [10; 0; 0];           % 10 V/m
H = [0; 0.1; 0];          % WRONG! Should be 10/377 ≈ 0.0265
k = [0; 0; 5];

result = PlaneWaveCheck('full', E, H, k);
% Output: NOT a plane wave
% Reason: H ≠ (1/η)(k̂ × E)
% impedance_error ≈ 277% (way off!)
```

### Example 5: Diagonal Propagation (Valid)

```matlab
% Wave propagating in x-z plane
E = [0; 1; 0];                    % ŷ (perpendicular to x-z plane)
H = [1; 0; -1] / sqrt(2);         % In x-z plane, ⊥ to k
k = [1; 0; 1];                    % Diagonal in x-z plane

result = PlaneWaveCheck(E, H, k);
% Output: IS a plane wave ✓
% k·E = 0, k·H = 0, E·H = 0
```

### Example 6: Lossy Medium with Complex η

```matlab
% Lossy dielectric with complex impedance
E = [100; 0; 0];                  % V/m
eta_c = 200 * exp(1j*pi/6);       % Complex impedance, 30° phase
k_hat = [0; 0; 1];
H_expected = (1/eta_c) * cross(k_hat, E);

result = PlaneWaveCheck('full', E, H_expected, [0;0;10], eta_c);
% Output: IS a plane wave ✓
```

---

## Summary: 5-Step Checklist

```
□ Step 1a: k · E = 0?
□ Step 1b: k · H = 0?     ← Don't forget!
□ Step 1c: E · H = 0?
□ Step 2:  k̂ = k/|k| computed
□ Step 3:  H = (1/η)(k̂ × E)?
□ Step 4:  (E × H) · k > 0?

ALL must pass → Valid Plane Wave
ANY fails → NOT a plane wave
```

---

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples →](PlaneWaveCheck_Exam_Examples.md)
