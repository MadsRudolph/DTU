# Fresnel - Quick Reference Card

> 📋 **One-page cheat sheet for exams**

**Navigation:** [Master Index](Fresnel_MASTER_INDEX.md) · [Quick Start](Fresnel_Quick_Start.md) · [Complete Guide](Fresnel_Complete_Guide.md)

---

## Mode Selection

| Need | Command |
|------|---------|
| Normal incidence (θ=0) | `Fresnel(ε₁, ε₂)` |
| Oblique incidence | `Fresnel(ε₁, ε₂, θᵢ)` |
| TE only | `Fresnel(ε₁, ε₂, θᵢ, 'TE')` |
| TM only | `Fresnel(ε₁, ε₂, θᵢ, 'TM')` |
| Transmitted angle | `Fresnel('snell', n₁, n₂, θᵢ)` |
| Brewster angle | `Fresnel('brewster', ε₁, ε₂)` |
| Critical angle | `Fresnel('critical', ε₁, ε₂)` |

---

## Key Formulas

### Normal Incidence
```
η = η₀/√εᵣ = 377/√εᵣ  [Ω]
n = √εᵣ

Γ = (η₂ - η₁)/(η₂ + η₁)
τ = 2η₂/(η₂ + η₁)
R = |Γ|²,  T = 1 - R
```

### Special Angles
```
Snell:     n₁ sin θᵢ = n₂ sin θₜ
Brewster:  θ_B = arctan(n₂/n₁)
Critical:  θ_c = arcsin(n₂/n₁)  [n₁ > n₂]
```

---

## TE vs TM

| | TE (s-pol) | TM (p-pol) |
|-|------------|------------|
| E-field | ⊥ plane | ∥ plane |
| Also called | Perpendicular | Parallel |
| Zero at θ_B | No | **Yes** |

---

## Quick Examples

```matlab
% Air to glass, normal
Fresnel(1, 4)           % Γ = -1/3

% Air to glass, 45°
Fresnel(1, 4, 45)       % Both TE & TM

% Brewster angle
Fresnel('brewster', 1, 4)  % θ_B = 63.4°

% Critical angle (glass to air)
Fresnel('critical', 4, 1)  % θ_c = 30°

% Snell's law
Fresnel('snell', 1, 1.5, 30)  % θₜ = 19.5°
```

---

## Output Fields

```matlab
r.Gamma, r.Gamma_TE, r.Gamma_TM  % Reflection coeff
r.tau, r.tau_TE, r.tau_TM        % Transmission coeff
r.R, r.R_TE, r.R_TM              % Power reflectance
r.T, r.T_TE, r.T_TM              % Power transmittance
r.theta_i, r.theta_t             % Angles [deg]
r.theta_Brewster                 % Brewster angle
r.TIR                            % true if TIR
r.eta1, r.eta2                   % Impedances [Ω]
r.n1, r.n2                       % Refractive indices
```

---

## Common Values

| Material | εᵣ | n |
|----------|-----|---|
| Air | 1 | 1.0 |
| Glass | 4 | 2.0 |
| Water | 80 | 8.9 |

| Interface | θ_B | θ_c |
|-----------|-----|-----|
| Air→Glass (n=2) | 63.4° | N/A |
| Glass→Air (n=2) | 26.6° | 30° |

---

## Sign Convention

- **Γ > 0:** E-field keeps direction on reflection
- **Γ < 0:** E-field inverts on reflection
- **|Γ| = 1:** Total reflection (TIR)

---

## TIR Conditions

```
TIR occurs when:
1. n₁ > n₂  (dense to less dense)
2. θᵢ > θ_c
```

---

## Typical Exam Problems

| Given | Find | Command |
|-------|------|---------|
| ε₁, ε₂, θᵢ | Γ, R, T | `Fresnel(ε₁, ε₂, θᵢ)` |
| n₁, n₂, θᵢ | θₜ | `Fresnel('snell', n₁, n₂, θᵢ)` |
| ε₁, ε₂ | θ_B | `Fresnel('brewster', ε₁, ε₂)` |
| ε₁, ε₂ | θ_c | `Fresnel('critical', ε₁, ε₂)` |
| Check TIR | TIR? | `Fresnel(ε₁, ε₂, θᵢ)` → r.TIR |

---

**Navigation:** [Master Index](Fresnel_MASTER_INDEX.md) · [Quick Start](Fresnel_Quick_Start.md) · [Complete Guide](Fresnel_Complete_Guide.md)
