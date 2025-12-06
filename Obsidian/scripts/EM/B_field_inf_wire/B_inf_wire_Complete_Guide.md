# B_inf_wire.m - Complete Guide

> **Comprehensive Reference for Magnetic Field Calculations**

---

## Function Overview

**B_inf_wire** calculates the magnetic field magnitude around an infinitely long, straight, current-carrying wire using Ampère's Law.

### Syntax
```matlab
B = B_inf_wire(I, r)
B = B_inf_wire(I, r, mu_r)
```

### Parameters
- `I` - Current in Amperes [A]
- `r` - Radial distance from wire in meters [m] (scalar or array)
- `mu_r` - Relative permeability (optional, default: 1)

### Returns
- `B` - Magnetic field magnitude in Tesla [T]
  - Scalar if `r` is scalar
  - Array if `r` is array (element-wise calculation)

### Example
```matlab
I = 5;       % 5 A
r = 0.02;    % 2 cm = 0.02 m

B = B_inf_wire(I, r);
% B = 5.0e-05 T = 50 μT
```

---

## Theory

### Ampère's Law

**Integral form:**
```
∮ B⃗·dℓ⃗ = μI_enclosed
```

**For infinite straight wire:**
- Symmetry: B-field is constant at fixed radius
- Path: Choose circular path of radius r
- Result: B(2πr) = μI

**Solving for B:**
```
B = μI / (2πr)
```

### Permeability

```
μ = μ₀μᵣ

μ₀ = 4π × 10⁻⁷ H/m  (permeability of free space)
μᵣ = relative permeability (dimensionless)
```

**Typical values:**
- Vacuum/air: μᵣ = 1
- Water: μᵣ ≈ 1
- Copper: μᵣ ≈ 1  
- Iron: μᵣ ≈ 1000-5000
- Mumetal: μᵣ ≈ 20,000-100,000

---

## Magnetic Field Properties

### Magnitude

```
|B| = μI / (2πr)
```

**Scaling:**
- **Linear in current:** B ∝ I
- **Inverse in distance:** B ∝ 1/r

**Example:**
```matlab
% Double current → double B
B1 = B_inf_wire(5, 0.02);
B2 = B_inf_wire(10, 0.02);
% B2 = 2*B1

% Double distance → half B
B1 = B_inf_wire(10, 0.01);
B2 = B_inf_wire(10, 0.02);
% B2 = B1/2
```

### Direction

**Right-hand rule:**
1. Point thumb along current direction
2. Curl fingers around wire
3. Fingers point in B-field direction

**Mathematical form:**
```
B⃗ = (μI/2πr) φ̂

where φ̂ is tangent to circle (in cylindrical coordinates)
```

**Note:** `B_inf_wire` returns **magnitude only**

---

## Units and Conversions

### Current Units

| Unit | Symbol | Conversion | MATLAB |
|------|--------|------------|--------|
| Ampere | A | 1 | `1` |
| Milliampere | mA | 10⁻³ A | `1e-3` |
| Microampere | μA | 10⁻⁶ A | `1e-6` |
| Kiloampere | kA | 10³ A | `1e3` |

### Distance Units

| Unit | Symbol | Conversion | MATLAB |
|------|--------|------------|--------|
| Meter | m | 1 | `1` |
| Centimeter | cm | 10⁻² m | `1e-2` or `*0.01` |
| Millimeter | mm | 10⁻³ m | `1e-3` or `*0.001` |
| Micrometer | μm | 10⁻⁶ m | `1e-6` |

### B-field Units

| Unit | Symbol | Conversion | Typical Use |
|------|--------|------------|-------------|
| Tesla | T | 1 | SI unit |
| Millitesla | mT | 10⁻³ T | Strong fields |
| Microtesla | μT | 10⁻⁶ T | Common range |
| Nanotesla | nT | 10⁻⁹ T | Weak fields |
| Gauss | G | 10⁻⁴ T | CGS unit |

---

## Typical Values

### Reference Fields

| Source | B-field |
|--------|---------|
| Earth's magnetic field | ~50 μT |
| Refrigerator magnet | ~5 mT |
| MRI machine | 1-3 T |
| Strongest lab magnet | ~45 T |

### Wire Examples

```matlab
% Household wire (1 A at 1 cm)
B = B_inf_wire(1, 0.01);
% B = 20 μT (less than Earth's field)

% Power line (100 A at 10 m)
B = B_inf_wire(100, 10);
% B = 2 μT (small at distance)

% Close to strong current (10 A at 1 mm)
B = B_inf_wire(10, 0.001);
% B = 2 mT (quite strong!)
```

---

## Array Input

### Multiple Distances

```matlab
% Calculate B at several distances
I = 10;
r = [0.01, 0.02, 0.05, 0.10];  % m

B = B_inf_wire(I, r);

>> B * 1e6  % μT
ans =
   200   100    40    20

% Can also use linspace
r = linspace(0.01, 0.10, 10);
B = B_inf_wire(10, r);
```

### Plotting B vs r

```matlab
% Create distance array
r = linspace(0.001, 0.1, 100);  % 1 mm to 10 cm

% Calculate B-field
I = 10;
B = B_inf_wire(I, r);

% Plot
figure;
plot(r*100, B*1e6, 'LineWidth', 2);
xlabel('Distance [cm]');
ylabel('B-field [μT]');
title('Magnetic Field vs Distance (I = 10 A)');
grid on;

% Log-log plot shows 1/r relationship
figure;
loglog(r*100, B*1e6, 'LineWidth', 2);
xlabel('Distance [cm]');
ylabel('B-field [μT]');
title('B-field vs Distance (log-log)');
grid on;
% Slope = -1 confirms B ∝ 1/r
```

---

## Advanced Topics

### Vector Form (Manual)

```matlab
% Wire along z-axis at origin, current in +z
% Find B-field vector at point P = (x, y, 0)

I = 10;
P = [0.01; 0.02; 0];  % Point in space

% Distance from wire (in xy-plane)
r_perp = sqrt(P(1)^2 + P(2)^2);

% Magnitude
B_mag = B_inf_wire(I, r_perp);

% Direction: tangent to circle, perpendicular to radial
radial = [P(1); P(2); 0] / r_perp;
B_direction = cross([0; 0; 1], radial);  % φ̂ direction

% B-field vector
B_vec = B_mag * B_direction;

fprintf('B = [%.2e, %.2e, %.2e] T\n', B_vec);
```

### Multiple Wires (Superposition)

```matlab
% Two parallel wires
I1 = 10;  pos1 = [0; 0; 0];      % Wire 1 at origin
I2 = -10; pos2 = [0.1; 0; 0];    % Wire 2 at x=10cm (opposite current)

% Point of interest
P = [0.05; 0.02; 0];

% Distance to each wire
r1 = norm(P(1:2) - pos1(1:2));
r2 = norm(P(1:2) - pos2(1:2));

% B-field magnitude from each
B1 = B_inf_wire(abs(I1), r1);
B2 = B_inf_wire(abs(I2), r2);

% Direction vectors (must calculate manually)
% ... (requires full vector treatment)
```

### Finite Wire Correction

The infinite wire approximation is valid when:
```
L >> r  (wire length >> distance from wire)
```

**Rule of thumb:** Use infinite approximation if L > 10r

For finite wire, Biot-Savart law is needed:
```
B = (μI/4πr) * (cosθ₁ - cosθ₂)
```

---

## Magnetic Materials

### Non-Magnetic Materials (μᵣ ≈ 1)

```matlab
% Most materials
B = B_inf_wire(I, r);  % Default μᵣ = 1
```

**Examples:**
- Air, vacuum: μᵣ = 1.000...
- Water: μᵣ ≈ 1.000
- Copper, aluminum: μᵣ ≈ 1.000
- Wood, plastic: μᵣ ≈ 1.000

### Ferromagnetic Materials (μᵣ >> 1)

```matlab
% Iron core
B_iron = B_inf_wire(I, r, 1000);

% Compare to air
B_air = B_inf_wire(I, r);

% Enhancement
factor = B_iron / B_air;  % = μᵣ
```

**Typical μᵣ values:**
- Iron: 200-5000 (depends on purity)
- Nickel: 100-600
- Cobalt: 250
- Mumetal: 20,000-100,000
- Ferrite: 10-10,000

**Note:** μᵣ is not constant - depends on B-field strength (saturation)

---

## Relationship to Other EM Concepts

### Coulomb's Law Analogy

| Electric | Magnetic |
|----------|----------|
| E = kq/r² | B = μI/(2πr) |
| Point charge | Line current |
| 1/r² falloff | 1/r falloff |
| Radial field | Circular field |

### Faraday's Law

```
∇×E = -∂B/∂t
```

Changing B-field induces E-field (used in transformers, inductors)

### Lorentz Force

```matlab
% Force on charge q moving with velocity v in B-field
F = q * cross(v, B);

% Force on current I in wire of length L
F = I * L * B;  % (if perpendicular)
```

---

## Error Handling

### Built-in Checks

```matlab
if any(r <= 0)
    error('Distance r must be positive.');
end
```

### User Validation

```matlab
% Check reasonable values
assert(I > 0, 'Current should be positive');
assert(all(r > 0), 'All distances must be positive');

% Typical range check
B = B_inf_wire(I, r);
if B*1e6 > 1000
    warning('B-field > 1 mT. Very strong! Check inputs.');
elseif B*1e6 < 0.1
    warning('B-field < 0.1 μT. Very weak! Check inputs.');
end
```

---

## Limitations

**Infinite wire assumption:**
- Wire must be much longer than distance: L >> r
- Straight wire (no curvature)
- Constant current throughout

**Not valid for:**
- Finite-length wires (use Biot-Savart)
- Curved wires (loops, solenoids)
- Time-varying currents (radiation effects)

**Magnitude only:**
- Function returns |B| only
- For direction, use right-hand rule
- For full vector, manual calculation needed

---

## Quick Reference

### Key Formulas

```matlab
% Ampère's law (infinite wire)
B = μI / (2πr)

% Permeability
μ = μ₀μᵣ
μ₀ = 4π × 10⁻⁷ H/m

% Constants
mu0 = 4*pi*1e-7;
```

### Common Conversions

```matlab
1 mA = 1e-3 A
1 cm = 1e-2 m
1 μT = 1e-6 T
1 G = 1e-4 T
```

### Scaling Laws

```
I₂ = 2I₁  →  B₂ = 2B₁   (linear)
r₂ = 2r₁  →  B₂ = B₁/2  (inverse)
```

---

[← Master Index](B_inf_wire_MASTER_INDEX.md)
