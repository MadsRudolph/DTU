# Fresnel Complete Guide

> **Purpose:** Comprehensive reference for reflection and transmission at interfaces  
> **Based on:** Fresnel equations for electromagnetic waves

---

## 📍 Navigation

[← Master Index](Fresnel_MASTER_INDEX.md) · [Quick Start](Fresnel_Quick_Start.md) · [Quick Reference](Fresnel_Quick_Reference.md)

---

## Table of Contents

1. [Theory: Fresnel Equations](#1-theory-fresnel-equations)
2. [Normal Incidence Mode](#2-normal-incidence-mode)
3. [Oblique Incidence Mode](#3-oblique-incidence-mode)
4. [Snell's Law Mode](#4-snells-law-mode)
5. [Brewster Angle Mode](#5-brewster-angle-mode)
6. [Critical Angle Mode](#6-critical-angle-mode)
7. [Wave Vector Mode](#7-wave-vector-mode)
8. [Output Fields Reference](#8-output-fields-reference)
9. [Exam Examples](#9-exam-examples)

---

## 1. Theory: Fresnel Equations

### Boundary Conditions

At an interface between two media, the tangential components of E and H must be continuous:

```
E₁ₜ = E₂ₜ    (tangential E continuous)
H₁ₜ = H₂ₜ    (tangential H continuous)
```

These conditions lead to the Fresnel equations.

### Intrinsic Impedance

For a lossless dielectric:
```
η = √(μ/ε) = η₀√(μᵣ/εᵣ) = 377√(μᵣ/εᵣ)  [Ω]
```

For non-magnetic materials (μᵣ = 1):
```
η = η₀/√εᵣ = 377/√εᵣ  [Ω]
```

### Refractive Index

```
n = c₀/v = √(εᵣμᵣ)
```

For non-magnetic: n = √εᵣ

### Reflection and Transmission Coefficients

**Reflection coefficient Γ:** Ratio of reflected to incident E-field amplitude

**Transmission coefficient τ:** Ratio of transmitted to incident E-field amplitude

**Power reflectance R:** Fraction of power reflected
```
R = |Γ|²
```

**Power transmittance T:** Fraction of power transmitted
```
T = 1 - R = 1 - |Γ|²
```

---

## 2. Normal Incidence Mode

### Syntax

```matlab
Fresnel(eps_r1, eps_r2)              % Non-magnetic materials
Fresnel(eps_r1, eps_r2, mu_r1, mu_r2)  % Magnetic materials
```

### Formulas

At normal incidence (θᵢ = 0°), TE and TM are identical:

```
Γ = (η₂ - η₁)/(η₂ + η₁)

τ = 2η₂/(η₂ + η₁)

R = |Γ|² = [(η₂ - η₁)/(η₂ + η₁)]²

T = 1 - R = 4η₁η₂/(η₁ + η₂)²
```

### Example: Air to Glass

```matlab
r = Fresnel(1, 4);

% Results:
%   η₁ = 377 Ω (air)
%   η₂ = 188.5 Ω (glass, n=2)
%   Γ = (188.5 - 377)/(188.5 + 377) = -1/3 = -0.333
%   R = 1/9 = 11.1%
%   T = 8/9 = 88.9%
```

**Physical interpretation of Γ < 0:** The reflected E-field is inverted (180° phase shift). This happens when going from lower to higher refractive index.

---

## 3. Oblique Incidence Mode

### Syntax

```matlab
Fresnel(eps_r1, eps_r2, theta_i)           % Both TE and TM
Fresnel(eps_r1, eps_r2, theta_i, 'TE')     % TE only
Fresnel(eps_r1, eps_r2, theta_i, 'TM')     % TM only
Fresnel(eps_r1, eps_r2, theta_i, pol, mu_r1, mu_r2)  % Magnetic
```

### TE vs TM Polarization

**TE (Transverse Electric) = s-polarization:**
- E-field is **perpendicular** to the plane of incidence
- E-field is parallel to the interface

**TM (Transverse Magnetic) = p-polarization:**
- E-field is **parallel** to the plane of incidence
- E-field has component normal to interface

### Fresnel Equations (Oblique)

**TE (s-polarization):**
```
Γ_TE = (η₂cosθᵢ - η₁cosθₜ)/(η₂cosθᵢ + η₁cosθₜ)

τ_TE = 2η₂cosθᵢ/(η₂cosθᵢ + η₁cosθₜ)
```

**TM (p-polarization):**
```
Γ_TM = (η₂cosθₜ - η₁cosθᵢ)/(η₂cosθₜ + η₁cosθᵢ)

τ_TM = 2η₂cosθᵢ/(η₂cosθₜ + η₁cosθᵢ)
```

### Example: 45° Incidence

```matlab
r = Fresnel(1, 4, 45);

% Results:
%   θᵢ = 45°
%   θₜ = 20.70° (from Snell's law)
%   Γ_TE = -0.409
%   Γ_TM = -0.158
%   R_TE = 16.7%
%   R_TM = 2.5%
%   θ_B = 63.43° (Brewster angle)
```

**Key observation:** TM has less reflection than TE at most angles, and zero reflection at the Brewster angle.

---

## 4. Snell's Law Mode

### Syntax

```matlab
Fresnel('snell', n1, n2, theta_i)     % Using refractive indices
Fresnel('snell', eps_r1, eps_r2, theta_i)  % Using permittivities (>3)
```

### Formula

```
n₁ sin(θᵢ) = n₂ sin(θₜ)

θₜ = arcsin[(n₁/n₂) sin(θᵢ)]
```

### Example

```matlab
r = Fresnel('snell', 1, 1.5, 30);

% n₁sinθᵢ = 1 × sin(30°) = 0.5
% sinθₜ = 0.5/1.5 = 0.333
% θₜ = 19.47°
```

### Total Internal Reflection

If n₁ > n₂ and θᵢ is large enough:
```
sin(θₜ) = (n₁/n₂)sin(θᵢ) > 1  → No real solution!
```

This is Total Internal Reflection (TIR).

```matlab
r = Fresnel('snell', 1.5, 1, 45);
% θᵢ = 45° > θ_c = 41.8° → TIR!
% r.TIR = true
% r.theta_t = NaN
```

---

## 5. Brewster Angle Mode

### Syntax

```matlab
Fresnel('brewster', eps_r1, eps_r2)
Fresnel('brewster', eps_r1, eps_r2, mu_r1, mu_r2)  % Magnetic
```

### Formula

For non-magnetic materials:
```
θ_B = arctan(n₂/n₁) = arctan(√(ε₂/ε₁))
```

### Physical Meaning

At the Brewster angle:
- **Γ_TM = 0** (no TM reflection!)
- Γ_TE ≠ 0 (TE still reflects)
- The reflected and transmitted rays are perpendicular

### Example

```matlab
r = Fresnel('brewster', 1, 4);

% n₂/n₁ = 2/1 = 2
% θ_B = arctan(2) = 63.43°
```

**Verification:**
```matlab
r = Fresnel(1, 4, 63.43);
% Γ_TM ≈ 0 (within numerical precision)
```

---

## 6. Critical Angle Mode

### Syntax

```matlab
Fresnel('critical', eps_r1, eps_r2)
```

### Formula

Critical angle exists only when n₁ > n₂ (dense to less dense):
```
θ_c = arcsin(n₂/n₁)
```

For θᵢ > θ_c: Total Internal Reflection (TIR)

### Example: Glass to Air

```matlab
r = Fresnel('critical', 4, 1);

% n₁ = 2 (glass), n₂ = 1 (air)
% θ_c = arcsin(1/2) = 30°
```

**Verification:**
```matlab
Fresnel(4, 1, 25)   % θᵢ < θ_c → Normal transmission
Fresnel(4, 1, 35)   % θᵢ > θ_c → TIR!
```

### No Critical Angle Case

```matlab
r = Fresnel('critical', 1, 4);  % Air to glass
% n₁ = 1 < n₂ = 2
% No critical angle - TIR not possible in this direction
```

---

## 7. Wave Vector Mode

### Syntax

```matlab
Fresnel('kvec', beta, eps_r2, plane)
```

- `beta`: Wave vector [kx; ky; kz]
- `eps_r2`: Permittivity of second medium
- `plane`: Interface plane ('xy', 'xz', or 'yz')

### Purpose

Extract incidence angle from a wave vector when the problem gives k instead of θᵢ.

### Example

```matlab
beta = [5; 0; 10];  % Wave propagating in xz-plane
r = Fresnel('kvec', beta, 4, 'xy');  % Interface is xy-plane

% Calculates angle between k and normal to xy-plane (z-axis)
% θᵢ = arccos(|k·ẑ|/|k|) = arccos(10/11.18) = 26.57°
```

---

## 8. Output Fields Reference

### Common Fields (All Modes)

| Field | Description | Units |
|-------|-------------|-------|
| `eps_r1`, `eps_r2` | Relative permittivities | - |
| `mu_r1`, `mu_r2` | Relative permeabilities | - |
| `eta1`, `eta2` | Intrinsic impedances | Ω |
| `n1`, `n2` | Refractive indices | - |

### Angle Fields

| Field | Description | Units |
|-------|-------------|-------|
| `theta_i` | Incident angle | degrees |
| `theta_t` | Transmitted angle | degrees |
| `theta_Brewster` | Brewster angle | degrees |
| `theta_critical` | Critical angle | degrees |

### Coefficient Fields

| Field | Description | Range |
|-------|-------------|-------|
| `Gamma`, `Gamma_TE`, `Gamma_TM` | Reflection coefficients | -1 to +1 (or complex) |
| `tau`, `tau_TE`, `tau_TM` | Transmission coefficients | 0 to 2 |
| `R`, `R_TE`, `R_TM` | Power reflectance | 0 to 1 |
| `T`, `T_TE`, `T_TM` | Power transmittance | 0 to 1 |

### Status Fields

| Field | Description |
|-------|-------------|
| `TIR` | `true` if total internal reflection |
| `TIR_possible` | `true` if critical angle exists |

---

## 9. Exam Examples

### Example 1: Basic Normal Incidence

**Problem:** A plane wave in air hits glass (εᵣ = 2.25) at normal incidence. Find Γ and percentage of power reflected.

```matlab
r = Fresnel(1, 2.25);

% η₁ = 377 Ω, η₂ = 377/1.5 = 251.3 Ω
% Γ = (251.3 - 377)/(251.3 + 377) = -0.2
% R = 0.04 = 4%

fprintf('Γ = %.3f\n', r.Gamma);
fprintf('R = %.1f%%\n', r.R * 100);
```

### Example 2: Find Brewster and Critical Angles

**Problem:** For a glass-air interface (n_glass = 1.5), find Brewster angle and critical angle.

```matlab
% Critical angle (glass to air - requires n₁ > n₂)
r = Fresnel('critical', 2.25, 1);
fprintf('θ_c = %.2f°\n', r.theta_critical);  % 41.81°

% Brewster angle (glass to air)
r = Fresnel('brewster', 2.25, 1);
fprintf('θ_B = %.2f°\n', r.theta_Brewster);  % 33.69°
```

### Example 3: Verify TIR

**Problem:** Light goes from glass (n=1.5) to air at 50°. Does TIR occur?

```matlab
r = Fresnel(2.25, 1, 50);

if r.TIR
    fprintf('TIR occurs! All power reflected.\n');
else
    fprintf('Normal transmission. θₜ = %.2f°\n', r.theta_t);
end

% Output: TIR occurs! (since 50° > θ_c = 41.81°)
```

### Example 4: Compare TE and TM

**Problem:** At 60° incidence from air to glass (n=1.5), compare TE and TM reflection.

```matlab
r = Fresnel(1, 2.25, 60);

fprintf('TE: Γ = %.4f, R = %.2f%%\n', r.Gamma_TE, r.R_TE*100);
fprintf('TM: Γ = %.4f, R = %.2f%%\n', r.Gamma_TM, r.R_TM*100);
fprintf('Brewster angle = %.2f°\n', r.theta_Brewster);

% TE: Γ = -0.382, R = 14.6%
% TM: Γ = -0.056, R = 0.3% (near Brewster!)
% Brewster = 56.31° (close to 60°)
```

---

## Summary: Which Mode to Use


---

## 📍 Navigation

[← Master Index](Fresnel_MASTER_INDEX.md) · [Quick Start](Fresnel_Quick_Start.md) · [Quick Reference](Fresnel_Quick_Reference.md)
