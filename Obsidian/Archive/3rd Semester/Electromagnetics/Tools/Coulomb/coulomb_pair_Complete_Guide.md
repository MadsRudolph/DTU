# coulomb_pair.m - Complete Guide

> **Comprehensive Reference for Coulomb Force Calculations**

---

## Function Overview

**coulomb_pair** calculates the electrostatic force between two point charges using Coulomb's Law in vector form.

### Syntax
```matlab
[F12, F21] = coulomb_pair(q1, q2, r1, r2)
```

### Parameters
- `q1` - Charge 1 in Coulombs [C]
- `q2` - Charge 2 in Coulombs [C]
- `r1` - Position vector of q₁ [3×1] in meters [m]
- `r2` - Position vector of q₂ [3×1] in meters [m]

### Returns
- `F12` - Force on q₁ due to q₂ [3×1 vector] in Newtons [N]
- `F21` - Force on q₂ due to q₁ [3×1 vector] in Newtons [N]

### Example
```matlab
q1 = 1e-6;         % 1 μC
q2 = -2e-6;        % -2 μC
r1 = [0; 0; 0];    % Origin
r2 = [1; 0; 0];    % 1 m in x-direction

[F12, F21] = coulomb_pair(q1, q2, r1, r2);
```

---

## Theory

### Coulomb's Law

**Scalar form (magnitude only):**
```
|F| = k_e · |q₁||q₂| / r²
```

**Vector form (magnitude and direction):**
```
F⃗₁₂ = (k_e · q₁q₂ / r²) · r̂₁₂
```

where:
- `k_e` = Coulomb's constant = 8.9875 × 10⁹ N·m²/C²
- `k_e = 1/(4πε₀)` where ε₀ = 8.854 × 10⁻¹² F/m
- `r̂₁₂` = unit vector from q₂ to q₁
- `r̂₁₂ = (r₁ - r₂) / |r₁ - r₂|`

### Physical Constants

```matlab
eps0 = 8.854e-12;  % Permittivity of free space [F/m]
k_e = 1/(4*pi*eps0);  % Coulomb's constant
k_e ≈ 8.9875e9;    % [N·m²/C²]
```

---

## Force Direction

### Sign Convention

**Same sign charges (both + or both -):**
- Product q₁q₂ > 0
- **Repulsive force**
- F⃗₁₂ points from q₂ toward q₁ (away from q₂)
- Forces push charges apart

**Opposite sign charges (+/- or -/+):**
- Product q₁q₂ < 0
- **Attractive force**
- F⃗₁₂ points from q₁ toward q₂ (toward q₂)
- Forces pull charges together

### Vector Calculation

```matlab
% Direction from q2 to q1
R12 = r1 - r2;

% Distance
d = norm(R12);

% Unit vector
u12 = R12 / d;

% Force magnitude
F_mag = k_e * q1 * q2 / d^2;

% Force vector
F12 = F_mag * u12;
```

**Note:** The sign of q₁q₂ automatically gives the correct direction!

---

## Newton's Third Law

The function returns **both forces** as an action-reaction pair:

```
F⃗₂₁ = -F⃗₁₂
```

**Always verify:**
```matlab
check = F12 + F21;
% Should be [0; 0; 0] (within numerical precision)
```

---

## Multiple Charges

### Superposition Principle

The total force on a charge from multiple other charges is the **vector sum** of individual forces:

```
F⃗_total = F⃗₁ + F⃗₂ + F⃗₃ + ...
```

### Example: Three Charges
```matlab
% Force on q1 from q2 and q3
[F12, ~] = coulomb_pair(q1, q2, r1, r2);
[F13, ~] = coulomb_pair(q1, q3, r1, r3);

% Net force on q1
F_net = F12 + F13;

% Magnitude
F_total = norm(F_net);
```

### Example: N Charges
```matlab
% Force on q1 from charges q2...qN
F_net = [0; 0; 0];

for i = 2:N
    [F1i, ~] = coulomb_pair(q1, q(i), r1, r(:,i));
    F_net = F_net + F1i;
end
```

---

## Units and Conversions

### Charge Units

| Unit | Symbol | Conversion | MATLAB |
|------|--------|------------|--------|
| Coulomb | C | 1 | `1` |
| Microcoulomb | μC | 10⁻⁶ C | `1e-6` |
| Nanocoulomb | nC | 10⁻⁹ C | `1e-9` |
| Picocoulomb | pC | 10⁻¹² C | `1e-12` |
| Elementary charge | e | 1.6×10⁻¹⁹ C | `1.6e-19` |

### Distance Units

| Unit | Symbol | Conversion | MATLAB |
|------|--------|------------|--------|
| Meter | m | 1 | `1` |
| Centimeter | cm | 10⁻² m | `1e-2` or `*0.01` |
| Millimeter | mm | 10⁻³ m | `1e-3` or `*0.001` |
| Micrometer | μm | 10⁻⁶ m | `1e-6` |
| Nanometer | nm | 10⁻⁹ m | `1e-9` |
| Angstrom | Å | 10⁻¹⁰ m | `1e-10` |

### Force Units

| Unit | Symbol | Conversion | Typical Range |
|------|--------|------------|---------------|
| Newton | N | 1 | Macroscopic |
| Millinewton | mN | 10⁻³ N | Common |
| Micronewton | μN | 10⁻⁶ N | Small charges |
| Nanonewton | nN | 10⁻⁹ N | Atomic scale |

---

## Typical Values

### Example Scenarios

**1. Two 1 μC charges, 1 cm apart:**
```matlab
F = 8.99e9 * (1e-6)² / (0.01)² = 89.9 N
% Very strong!
```

**2. Two electrons, 1 nm apart:**
```matlab
e = 1.6e-19;
F = 8.99e9 * e² / (1e-9)² = 0.23 nN
% Tiny at atomic scale
```

**3. Typical exam problem: μC charges, meter separation:**
```matlab
F ≈ 1-100 mN
% Millinewton range
```

---

## Complete Output

```matlab
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% F12: Force vector on q1
% - 3×1 column vector
% - Units: Newtons [N]
% - Direction: determined by sign of charges
% - Magnitude: |F12| = k_e·|q1·q2|/r²

% F21: Force vector on q2
% - 3×1 column vector
% - Units: Newtons [N]
% - Equal magnitude to F12
% - Opposite direction: F21 = -F12
```

---

## Advanced Topics

### Electric Field

The electric field **E⃗** at a point is the force per unit charge:

```matlab
% Field created by q2 at position r1
[F12, ~] = coulomb_pair(1, q2, r1, r2);  % Test charge = 1 C
E = F12;  % E field [N/C or V/m]

% For actual charge q1:
F12 = q1 * E;
```

### Potential Energy

Electrostatic potential energy between two charges:

```matlab
r = norm(r1 - r2);
U = k_e * q1 * q2 / r;  % [Joules]
```

### Work and Energy

Work done moving a charge in an electric field:

```matlab
% Work = -ΔU
W = -k_e * q1 * q2 * (1/r_final - 1/r_initial);
```

---

## Error Handling

### Built-in Checks

The function checks for:
```matlab
if d12 == 0
    error('Charges must not coincide.');
end
```

### User Checks

```matlab
% Verify Newton's 3rd law
assert(norm(F12 + F21) < 1e-10, 'Newton 3rd law violated!');

% Check reasonable magnitude
assert(norm(F12) < 1e6, 'Force unrealistically large!');

% Verify units
assert(all(size(r1) == [3,1]), 'Position must be 3×1 column vector');
```

---

## Limitations

**Point charge assumption:**
- Charges must be much smaller than separation
- Not valid for extended charge distributions

**Free space:**
- Assumes vacuum (ε = ε₀)
- For other media, use ε = ε_r·ε₀ and modify k_e

**Static charges:**
- Assumes charges at rest
- For moving charges, need relativistic corrections

---

## Related Concepts

### Gauss's Law
```
∮ E⃗·dA⃗ = Q_enclosed/ε₀
```

### Electric Field Lines
- Field lines point away from positive charges
- Field lines point toward negative charges
- Density of lines proportional to field strength

### Equipotential Surfaces
- Surfaces of constant potential
- Perpendicular to electric field lines
- For point charge: concentric spheres

---

## Quick Reference

### Key Formulas
```matlab
% Force magnitude
F = k_e * |q1*q2| / r²

% Force vector
F⃗₁₂ = (k_e * q1*q2 / r²) * (r⃗₁ - r⃗₂) / |r⃗₁ - r⃗₂|

% Constants
k_e = 8.99e9 N·m²/C²
ε₀ = 8.854e-12 F/m
```

### Common Conversions
```matlab
1 μC = 1e-6 C
1 cm = 1e-2 m
1 mN = 1e-3 N
```

---

[← Master Index](coulomb_pair_MASTER_INDEX.md)
