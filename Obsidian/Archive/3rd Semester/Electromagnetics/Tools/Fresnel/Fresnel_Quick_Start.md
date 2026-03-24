# Fresnel - Quick Start Guide

> ⏱️ **Time:** 3 minutes  
> **Goal:** Calculate reflection and transmission at interfaces

**Navigation:** [Master Index](Fresnel_MASTER_INDEX.md) · [Complete Guide](Fresnel_Complete_Guide.md) · [Quick Reference](Fresnel_Quick_Reference.md)

---

## Step 1: What Do You Need?

| Task | Command |
|------|---------|
| Γ, τ, R, T at normal incidence | `Fresnel(ε₁, ε₂)` |
| Γ, τ, R, T at an angle | `Fresnel(ε₁, ε₂, θᵢ)` |
| Transmitted angle (Snell) | `Fresnel('snell', n₁, n₂, θᵢ)` |
| Brewster angle | `Fresnel('brewster', ε₁, ε₂)` |
| Critical angle (TIR) | `Fresnel('critical', ε₁, ε₂)` |

---

## Step 2: Identify Your Inputs

### For εᵣ (relative permittivity)
| Material | εᵣ |
|----------|-----|
| Air/vacuum | 1 |
| Glass | 4-6 |
| Water | 80 |
| Typical dielectric | 2-10 |

### For refractive index n
```
n = √εᵣ    (for non-magnetic materials)
```

| Material | n |
|----------|---|
| Air | 1.0 |
| Glass | 1.5-2.0 |
| Water | 1.33 |

---

## Example 1: Normal Incidence (Air → Glass)

**Problem:** Light goes from air (εᵣ=1) to glass (εᵣ=4) at normal incidence. Find reflection coefficient and power reflected.

```matlab
r = Fresnel(1, 4);
```

**Output:**
```
==========================================
     FRESNEL: NORMAL INCIDENCE           
==========================================
  Medium 1: eps_r = 1.000, mu_r = 1.000
  Medium 2: eps_r = 4.000, mu_r = 1.000
------------------------------------------
  eta1 = 376.73 Ohm
  eta2 = 188.37 Ohm
  n1 = 1.0000, n2 = 2.0000
------------------------------------------
  Gamma = -0.3333 +0.0000j
  |Gamma| = 0.3333
  tau = 0.6667
------------------------------------------
  R (reflected power) = 0.1111 (11.11%)
  T (transmitted power) = 0.8889 (88.89%)
==========================================
```

**Answer:** Γ = -1/3, R = 11.1% reflected

---

## Example 2: Oblique Incidence at 45°

**Problem:** Same interface but at 45° incidence. Find TE and TM coefficients.

```matlab
r = Fresnel(1, 4, 45);
```

**Output shows both polarizations:**
- θₜ = 20.70° (from Snell's law)
- Γ_TE = -0.4094
- Γ_TM = -0.1584
- Brewster angle = 63.43°

**To get just one polarization:**
```matlab
r = Fresnel(1, 4, 45, 'TE');   % TE only
r = Fresnel(1, 4, 45, 'TM');   % TM only
```

---

## Example 3: Find Brewster Angle

**Problem:** At what angle does TM have zero reflection?

```matlab
r = Fresnel('brewster', 1, 4);
```

**Output:**
```
=== Brewster Angle ===
  n1 = 1.0000, n2 = 2.0000
  theta_B = 63.4349 deg
  At this angle: Gamma_TM = 0 (no TM reflection)
======================
```

**Formula:** θ_B = arctan(n₂/n₁) = arctan(2/1) = 63.43°

---

## Example 4: Critical Angle and TIR

**Problem:** Find critical angle for glass → air (internal reflection).

```matlab
r = Fresnel('critical', 4, 1);
```

**Output:**
```
=== Critical Angle ===
  n1 = 2.0000 > n2 = 1.0000
  theta_c = 30.0000 deg
  For theta_i > theta_c: Total Internal Reflection
======================
```

**Verify TIR occurs at 45°:**
```matlab
r = Fresnel(4, 1, 45);   % Glass to air at 45°
% Output: TOTAL INTERNAL REFLECTION (TIR)
% R_TE = R_TM = 1 (100% reflected)
```

---

## Example 5: Snell's Law

**Problem:** Light enters water (n=1.33) from air at 30°. Find transmission angle.

```matlab
r = Fresnel('snell', 1, 1.33, 30);
```

**Output:**
```
=== Snell's Law ===
  n1 = 1.0000, n2 = 1.3300
  theta_i = 30.00 deg
  theta_t = 22.08 deg
===================
```

---

## Key Formulas (Quick Reference)

### Normal Incidence
```
Γ = (η₂ - η₁)/(η₂ + η₁)
τ = 2η₂/(η₂ + η₁)
R = |Γ|²
T = 1 - R
```

### Special Angles
```
Snell:     sin(θₜ) = (n₁/n₂)sin(θᵢ)
Brewster:  θ_B = arctan(n₂/n₁)
Critical:  θ_c = arcsin(n₂/n₁)   (requires n₁ > n₂)
```

### TE vs TM
| | TE (s-pol) | TM (p-pol) |
|-|------------|------------|
| E-field | ⊥ to plane | ∥ to plane |
| Zero at Brewster | No | **Yes** |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Wrong ε order | Glass→air vs air→glass | n₁ is incident medium |
| Forgetting √ | n = εᵣ instead of n = √εᵣ | Fresnel handles this automatically |
| TIR direction | TIR only dense→less dense | Need n₁ > n₂ for critical angle |
| Angle in radians | MATLAB trig uses radians | Fresnel uses degrees! |

---

## Output Fields You'll Use Most

```matlab
r = Fresnel(1, 4, 30);

r.Gamma_TE    % TE reflection coefficient
r.Gamma_TM    % TM reflection coefficient  
r.R_TE        % Power reflected (TE)
r.R_TM        % Power reflected (TM)
r.theta_t     % Transmitted angle
r.TIR         % true if total internal reflection
```

---

## Next Steps

- 📋 [Quick Reference](Fresnel_Quick_Reference.md) - Cheat sheet for exam
- 📚 [Complete Guide](Fresnel_Complete_Guide.md) - Full theory and all modes

---

**Navigation:** [Master Index](Fresnel_MASTER_INDEX.md) · [Complete Guide](Fresnel_Complete_Guide.md) · [Quick Reference](Fresnel_Quick_Reference.md)
