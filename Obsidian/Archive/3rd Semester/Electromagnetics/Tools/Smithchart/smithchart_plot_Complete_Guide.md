# smithchart_plot.m - Complete Guide

> **Comprehensive Reference for Smith Chart Visualization**

---

## Mode 1: Impedance Plotting

**Most common mode** - Plot from Z₀ and Z_L

### Syntax
```matlab
smithchart_plot(Z0, ZL)
smithchart_plot(Z0, ZL, 'label')
```

### Parameters
- `Z0` - Characteristic impedance (Ω)
- `ZL` - Load impedance (Ω, can be complex)
- `label` - Optional text label for point

### Example
```matlab
Z0 = 50;
ZL = 100 + 1j*50;

smithchart_plot(Z0, ZL, 'Load');
```

### What It Does
1. **Normalizes:** z_L = Z_L / Z₀
2. **Calculates Γ:** Γ = (z_L - 1) / (z_L + 1)
3. **Displays:** Console output with all values
4. **Plots:** Point on Smith chart

---

## Mode 2: Gamma Plotting

**Use when:** You already have the reflection coefficient

### Syntax
```matlab
smithchart_plot('Gamma', Gamma)
smithchart_plot('Gamma', Gamma, 'label')
```

### Parameters
- `'Gamma'` - Mode keyword (required)
- `Gamma` - Reflection coefficient (complex)
- `label` - Optional text label

### Example
```matlab
Gamma = 0.5 * exp(1j*pi/4);
smithchart_plot('Gamma', Gamma, '\Gamma_L');
```

### What It Does
1. **Calculates z_L:** z_L = (1 + Γ) / (1 - Γ)
2. **Displays:** Console output
3. **Plots:** Point on Smith chart

---

## Complete Output Reference

### Console Output (Impedance Mode)

```matlab
>> smithchart_plot(75, 15 - 1j*37.5)

=== Smith Chart Point ===
  Z0 = 75.00 Ohm
  ZL = 15.0000 -37.5000j Ohm
  zL (normalized) = 0.2000 -0.5000j
  Gamma = -0.5000 -0.5000j
  |Gamma| = 0.7071, angle = -135.00 deg
=========================
```

### Console Output (Gamma Mode)

```matlab
>> smithchart_plot('Gamma', 0.5*exp(1j*pi/4))

=== Smith Chart Point (from Gamma) ===
  Gamma = 0.3536 +0.3536j
  |Gamma| = 0.5000, angle = 45.00 deg
  zL (normalized) = 1.6667 +0.8889j
======================================
```

---

## Theory

### Smith Chart Fundamentals

The Smith chart is a **graphical representation of the complex Γ plane** mapped onto a unit circle.

**Basic mapping:**
```
z_L = (1 + Γ) / (1 - Γ)
Γ = (z_L - 1) / (z_L + 1)
```

### Key Properties

**Normalized impedance:**
```
z_L = r + jx  (where r, x are normalized)
Z_L = Z₀ · z_L  (actual impedance)
```

**Reflection coefficient:**
```
Γ = |Γ| · e^(jθ)
|Γ| ≤ 1 for passive loads
```

### Chart Regions

| Location | Impedance | Γ |
|----------|-----------|---|
| Center | z_L = 1 (matched) | Γ = 0 |
| Right edge | z_L → ∞ (open) | Γ = +1 |
| Left edge | z_L → 0 (short) | Γ = -1 |
| Upper half | +jx (inductive) | Im(Γ) > 0 |
| Lower half | -jx (capacitive) | Im(Γ) < 0 |
| Real axis | x = 0 (pure R) | Im(Γ) = 0 |
| Outer circle | r = 0 (pure X) | \|Γ\| = 1 |

---

## Multiple Points

### Syntax
```matlab
% Plot first point
smithchart_plot(Z0, ZL1, 'Point 1');
hold on

% Add more points
smithchart_plot(Z0, ZL2, 'Point 2');
smithchart_plot(Z0, ZL3, 'Point 3');

% Finish
hold off
```

### Example: Impedance Transformation
```matlab
% Show impedance at different points on transmission line
Z0 = 50;
ZL = 100 + 1j*50;

smithchart_plot(Z0, ZL, 'Load');
hold on

% At λ/8
Z_18 = 62 + 1j*65;  % Example value
smithchart_plot(Z0, Z_18, '\lambda/8');

% At λ/4
Z_14 = Z0^2 / ZL;
smithchart_plot(Z0, Z_14, '\lambda/4');

hold off
```

---

## Chart Elements

### Resistance Circles

**Constant r circles:**
- Center: (r/(r+1), 0)
- Radius: 1/(r+1)
- Examples: r = 0, 0.2, 0.5, 1, 2, 5

### Reactance Arcs

**Constant x arcs:**
- Center: (1, 1/x)
- Radius: |1/x|
- Upper half: x > 0 (inductive)
- Lower half: x < 0 (capacitive)

### Special Points

```matlab
% Matched load
Γ = 0, z_L = 1

% Short circuit
Γ = -1, z_L = 0

% Open circuit
Γ = +1, z_L → ∞

% Pure reactance (lossless)
|Γ| = 1, r = 0
```

---

## Advanced Topics

### VSWR Circles

All points with the same VSWR lie on a circle centered at origin.

**Radius:** |Γ|

**VSWR:**
```
VSWR = (1 + |Γ|) / (1 - |Γ|)
```

### Constant SWR Circle
```matlab
% Plot all impedances with VSWR = 2
VSWR = 2;
Gamma_mag = (VSWR - 1) / (VSWR + 1);  % = 0.333

% Points lie on circle with |Γ| = 0.333
```

### Admittance Chart

The Smith chart can also represent **admittance** by rotating 180°.

**Conversion:**
```
z_L = 1 / y_L
y_L = 1 / z_L
```

To read admittance:
1. Plot impedance normally
2. Rotate 180° around center
3. Read as admittance

---

## Customization

### Without RF Toolbox

The function draws its own Smith chart with:
- Resistance circles: 0, 0.2, 0.5, 1, 2, 5
- Reactance arcs: ±0.2, ±0.5, ±1, ±2, ±5
- Unit circle
- Key points labeled

### With RF Toolbox

Uses MATLAB's built-in `smithplot` function for enhanced features.

---

## Quick Reference

### Formulas
```matlab
% Normalization
z_L = Z_L / Z₀

% Reflection coefficient
Γ = (z_L - 1) / (z_L + 1)

% Reverse
z_L = (1 + Γ) / (1 - Γ)
Z_L = Z₀ · z_L

% VSWR
VSWR = (1 + |Γ|) / (1 - |Γ|)
```

### Location Rules
```
Right → High R
Left → Low R
Up → Inductive
Down → Capacitive
Center → Matched
Edge → |Γ| = 1
```

---

## Demo Mode

```matlab
% Run with no arguments for demo
smithchart_plot()

% Shows example:
% Z₀ = 75 Ω
% Z_L = 15 - j37.5 Ω
```

---

[← Master Index](smithchart_plot_MASTER_INDEX.md)
