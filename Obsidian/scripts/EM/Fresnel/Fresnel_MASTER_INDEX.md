# Fresnel Documentation - Master Index

> **Tool:** `Fresnel.m`  
> **Purpose:** Calculate reflection/transmission coefficients for EM waves at interfaces  
> **Covers:** Normal/oblique incidence, Snell's law, Brewster angle, critical angle, TIR

---

## 📍 Navigation

| Quick Start | Complete Guide | Quick Reference |
|:-----------:|:--------------:|:---------------:|
| [📖 3 min](Fresnel_Quick_Start.md) | [📚 15 min](Fresnel_Complete_Guide.md) | [📋 1 min](Fresnel_Quick_Reference.md) |

**Other resources:** [Helpers.md](Helpers.md)

---

## Six Calculation Modes

| Mode | Usage | What It Calculates |
|------|-------|-------------------|
| **Normal** | `Fresnel(ε₁, ε₂)` | Γ, τ, R, T at θ=0° |
| **Oblique** | `Fresnel(ε₁, ε₂, θᵢ)` | Γ_TE, Γ_TM, τ, R, T at angle |
| **Snell** | `Fresnel('snell', n₁, n₂, θᵢ)` | Transmission angle θₜ |
| **Brewster** | `Fresnel('brewster', ε₁, ε₂)` | Brewster angle (Γ_TM = 0) |
| **Critical** | `Fresnel('critical', ε₁, ε₂)` | Critical angle for TIR |
| **K-vector** | `Fresnel('kvec', β, ε₂, plane)` | Angles from wave vector |

---

## Quick Decision Guide

```
What do you need?
│
├─► Reflection/transmission at normal incidence
│   └─► Fresnel(eps_r1, eps_r2)
│
├─► Reflection/transmission at an angle
│   └─► Fresnel(eps_r1, eps_r2, theta_i)
│
├─► Find transmitted angle (Snell's law)
│   └─► Fresnel('snell', n1, n2, theta_i)
│
├─► Find Brewster angle (no TM reflection)
│   └─► Fresnel('brewster', eps_r1, eps_r2)
│
├─► Find critical angle (TIR threshold)
│   └─► Fresnel('critical', eps_r1, eps_r2)
│
└─► Angles from wave vector k
    └─► Fresnel('kvec', beta, eps_r2, 'xy')
```

---

## Key Formulas

### Normal Incidence (θ = 0°)
```
Γ = (η₂ - η₁)/(η₂ + η₁)    where η = √(μ/ε)
τ = 2η₂/(η₂ + η₁)
R = |Γ|²
T = 1 - R
```

### Oblique Incidence
```
TE (s-pol):  Γ_TE = (η₂cosθᵢ - η₁cosθₜ)/(η₂cosθᵢ + η₁cosθₜ)
TM (p-pol):  Γ_TM = (η₂cosθₜ - η₁cosθᵢ)/(η₂cosθₜ + η₁cosθᵢ)
```

### Special Angles
```
Snell's Law:    n₁sinθᵢ = n₂sinθₜ
Brewster:       θ_B = arctan(n₂/n₁)
Critical:       θ_c = arcsin(n₂/n₁)    (only if n₁ > n₂)
```

---

## Quick Examples

### Normal Incidence: Air → Glass
```matlab
r = Fresnel(1, 4);        % εᵣ₁=1 (air), εᵣ₂=4 (glass)
% Γ = -0.333, R = 11.1%, T = 88.9%
```

### Oblique at 45°
```matlab
r = Fresnel(1, 4, 45);    % Both TE and TM
r = Fresnel(1, 4, 45, 'TE');  % TE only
r = Fresnel(1, 4, 45, 'TM');  % TM only
```

### Special Angles
```matlab
Fresnel('brewster', 1, 4)   % θ_B = 63.43°
Fresnel('critical', 4, 1)   % θ_c = 30° (glass→air)
```

### Snell's Law
```matlab
r = Fresnel('snell', 1, 1.5, 30);  % Find θₜ
% θₜ = 19.47°
```

---

## Output Fields

```matlab
result = Fresnel(1, 4, 30);

% Material properties
result.eps_r1, eps_r2     % Relative permittivities
result.eta1, eta2         % Intrinsic impedances [Ω]
result.n1, n2             % Refractive indices

% Angles
result.theta_i            % Incident angle [deg]
result.theta_t            % Transmitted angle [deg]
result.theta_Brewster     % Brewster angle [deg] (oblique mode)

% Coefficients (field amplitude)
result.Gamma_TE           % TE reflection coefficient
result.Gamma_TM           % TM reflection coefficient
result.tau_TE             % TE transmission coefficient
result.tau_TM             % TM transmission coefficient

% Power ratios
result.R_TE, R_TM         % Power reflectance
result.T_TE, T_TM         % Power transmittance

% TIR flag
result.TIR                % true if total internal reflection
```

---

## TE vs TM Polarization

| Name | Also Called | E-field Orientation |
|------|-------------|---------------------|
| **TE** | s-polarization, perpendicular | E ⊥ plane of incidence |
| **TM** | p-polarization, parallel | E ∥ plane of incidence |

**Memory aid:** TE = "Transverse Electric" = E is transverse to the plane of incidence

---

## Common Exam Scenarios

| Scenario | Command | Key Result |
|----------|---------|------------|
| Air to glass, normal | `Fresnel(1, 4)` | Γ = -1/3 |
| Air to glass, 45° | `Fresnel(1, 4, 45)` | TE ≠ TM |
| Brewster angle | `Fresnel('brewster', 1, 4)` | θ_B ≈ 63° |
| Glass to air, TIR | `Fresnel('critical', 4, 1)` | θ_c = 30° |
| Verify TIR occurs | `Fresnel(4, 1, 45)` | TIR = true |

---

## Related Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `Fresnel` | Interface coefficients | Reflection/transmission |
| `Medium` | Material properties | Get η, n, α, β |
| `TLine` | Transmission lines | Impedance matching |
| `PlaneWaveCheck` | Verify plane wave | Field validation |

---

## 📍 Quick Links

| [Quick Start](Fresnel_Quick_Start.md) | [Complete Guide](Fresnel_Complete_Guide.md) | [Quick Reference](Fresnel_Quick_Reference.md) |
|:---:|:---:|:---:|

**Back to:** [Helpers.md](Helpers.md)
