# Polarization.m - Complete Guide

> **Comprehensive Reference for All 3 Modes**

---

## Mode 1: Complex Phasor

**Most common mode** - Use for exam problems

### Syntax
```matlab
r = Polarization(F)              % +z propagation (default)
r = Polarization(F, k_hat)       % Specify propagation direction
```

### Parameters
- `F` - Complex phasor vector [3×1] or [2×1]
- `k_hat` - Propagation direction (optional, default [0;0;1])

### Example
```matlab
% RHCP wave in +z
F = [1; -1j; 0];
r = Polarization(F);

% Access results:
r.type         % 'Circular'
r.handedness   % 'RHCP'
r.AR           % 1.0
```

### Theory
The complex phasor represents:
```
E(r,t) = Re{F̃ · exp(j(ωt - k·r))}
```

**Polarization detection:**
1. **Linear:** Re(F) || Im(F) (parallel)
2. **Circular:** |Re(F)| = |Im(F)| and Re(F) ⊥ Im(F)
3. **Elliptical:** Everything else

**Handedness (IEEE):**
```
hand = k̂ · (Re(F) × Im(F))
hand > 0 → RHCP
hand < 0 → LHCP
```

---

## Mode 2: Amplitude/Phase

**Use when:** Given |E| and φ instead of complex form

### Syntax
```matlab
r = Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg)
r = Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg, k_hat)
```

### Parameters
- `Ex`, `Ey` - Field magnitudes (V/m)
- `phi_x_deg`, `phi_y_deg` - Phases (degrees)
- `k_hat` - Propagation direction (optional)

### Example
```matlab
% Given amplitudes and phases
r = Polarization('ap', 10, 5, 0, 90);
```

### Conversion
```matlab
Fx = Ex · exp(j·φx)
Fy = Ey · exp(j·φy)
F = [Fx; Fy; 0]
```

---

## Mode 3: Time-Domain

**Use when:** Field given as a·cos + b·sin

### Syntax
```matlab
r = Polarization(a, b, beta)
```

### Parameters
- `a` - Cosine coefficient vector [3×1]
- `b` - Sine coefficient vector [3×1]
- `beta` - Phase vector [3×1] in rad/m

### Field Form
```
E(t) = a·cos(ωt - β·r) + b·sin(ωt - β·r)
```

### Conversion to Phasor
```
F̃ = a - j·b
```

### Example
```matlab
a = [2; 1; 0];
b = [0; -1; -2];
beta = [2; -4; 2];

r = Polarization(a, b, beta);
```

---

## Complete Output Reference

```matlab
r = Polarization([1; -1j; 0]);

% Type classification
r.type         % 'Linear', 'Circular', or 'Elliptical'
r.handedness   % 'RHCP', 'LHCP', or 'N/A'

% Axial ratio
r.AR           % 1 = circular, ∞ = linear
r.AR_dB        % AR in dB

% Ellipse parameters
r.major        % Major semi-axis
r.minor        % Minor semi-axis
r.tilt         % Tilt angle (radians)
r.tilt_deg     % Tilt angle (degrees)

% Phasor details
r.F            % Complex phasor used
r.Fr           % Real part of F
r.Fi           % Imaginary part of F
r.k_hat        % Propagation direction
```

---

## Polarization Types

### Linear
- AR = ∞
- Real and imaginary parts parallel
- Examples: [1; 2; 0], [1j; 2j; 0], [1; 1; 0]

### Circular
- AR = 1 (0 dB)
- Equal magnitudes, 90° phase difference
- RHCP: [1; -1j; 0] in +z
- LHCP: [1; 1j; 0] in +z

### Elliptical
- 1 < AR < ∞
- General case between linear and circular
- Handedness: RHCP or LHCP

---

## Handedness Convention

**IEEE Convention (used by Polarization.m):**
- Looking in the direction of propagation
- RHCP: E rotates clockwise
- LHCP: E rotates counter-clockwise

**For +z propagation:**
- RHCP: [1; -1j; 0] (minus j)
- LHCP: [1; 1j; 0] (plus j)

---

## Quick Reference Table

| Phasor | Type | Handedness | AR |
|--------|------|------------|-----|
| `[1; -1j; 0]` | Circular | RHCP | 1 |
| `[1; 1j; 0]` | Circular | LHCP | 1 |
| `[1; 1; 0]` | Linear | N/A | ∞ |
| `[1; 0; 0]` | Linear | N/A | ∞ |
| `[2; -1j; 0]` | Elliptical | RHCP | 2.41 |

---

[← Master Index](Polarization_MASTER_INDEX.md)
