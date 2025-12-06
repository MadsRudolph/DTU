# poynting_pw.m - Complete Guide

> **Comprehensive Reference for All 3 Modes**

---

## Mode 1: Time-Domain (Q22-Q23)

**Most common mode** - Used for exam Q22-Q23

### Syntax
```matlab
r = poynting_pw('time', a, b, E0, beta_vec)
r = poynting_pw('time', a, b, E0, beta_vec, eta)
```

### Parameters
- `a` - Cosine coefficient vector [3×1]
- `b` - Sine coefficient vector [3×1]
- `E0` - Amplitude (V/m)
- `beta_vec` - Phase vector [3×1] (rad/m)
- `eta` - Intrinsic impedance (optional, default 377 Ω)

### Field Form
```
E(t) = E₀(a·cos(ωt - β·r) + b·sin(ωt - β·r))
```

### Conversion to Phasor
```
Ẽ = E₀(a - jb)
```

### Example
```matlab
a = [2; 1; 0];
b = [0; -1; -2];
E0 = 10;
beta_vec = [2; -4; 2];

r = poynting_pw('time', a, b, E0, beta_vec);
```

### Theory
1. **Convert to phasor:** Ẽ = E₀(a - jb)
2. **Get direction:** k̂ = β/|β|
3. **Calculate H:** H̃ = (1/η)·k̂ × Ẽ
4. **Calculate S:** S̄ = ½·Re{Ẽ × H̃*}

---

## Mode 2: Vector Phasor

**Use when:** E-field phasor given directly

### Syntax
```matlab
r = poynting_pw(E_phasor, k_hat)
r = poynting_pw(E_phasor, k_hat, eta)
r = poynting_pw(E_phasor, beta_vec)  % Auto-normalizes to k̂
```

### Parameters
- `E_phasor` - E-field phasor [3×1] (V/m)
- `k_hat` - Propagation direction (unit vector)
- `beta_vec` - Or full beta vector (auto-normalizes)
- `eta` - Intrinsic impedance (optional, default 377 Ω)

### Example
```matlab
E_phasor = [20; 10+1j*10; 1j*20];
k_hat = [0.408; -0.816; 0.408];

r = poynting_pw(E_phasor, k_hat);
```

---

## Mode 3: Scalar (Original)

**Use when:** Simple power calculation

### Syntax
```matlab
r = poynting_pw(E0, eta, A, phi)
```

### Parameters
- `E0` - Field magnitude (V/m)
- `eta` - Intrinsic impedance (Ω)
- `A` - Area (m²)
- `phi` - Angle between S and surface normal

### Example
```matlab
r = poynting_pw(10, 377, 0.5, 0);
% |S| = 100/(2×377) = 0.133 W/m²
% P = S·A·cos(φ)
```

---

## Complete Output Reference

```matlab
r = poynting_pw('time', a, b, E0, beta_vec);

% Q22-Q23 answers
r.H_phasor    % H-field phasor [A/m]
r.S_avg       % Poynting vector [W/m²]
r.S_mag       % |S̄| [W/m²]

% Supporting info
r.E_phasor    % E-field phasor [V/m]
r.k_hat       % Propagation direction
r.beta_vec    % Beta vector [rad/m]
r.beta_mag    % |β| [rad/m]
r.eta         % Impedance [Ω]
r.a, r.b, r.E0  % Original inputs (mode 1)
```

---

## Theory

### Plane Wave Relations

For a plane wave in a medium with impedance η:

**Phasor relation:**
```
H̃ = (1/η) · k̂ × Ẽ
```

**Time-average Poynting vector:**
```
S̄ = ½ · Re{Ẽ × H̃*}
```

**Alternative (direct from E):**
```
S̄ = (|Ẽ|²)/(2η) · k̂
```

### Intrinsic Impedance

**Free space:**
```
η₀ = √(μ₀/ε₀) = 377 Ω (exact: 376.73 Ω)
```

**General medium:**
```
η = √(μ/ε) = η₀√(μᵣ/εᵣ)
```

**Good conductor:**
```
η = (1+j)√(πfμ/σ)
```

---

## Mode Comparison

| Feature | Time-Domain | Vector Phasor | Scalar |
|---------|-------------|---------------|--------|
| **Input** | a, b, E₀, β | Ẽ, k̂ | E₀, η, A, φ |
| **Use** | Q22-Q23 | Pre-computed Ẽ | Power only |
| **Output** | Full (H, S) | Full (H, S) | |S|, P |
| **Typical** | Exam problems | Analysis | Simple calc |

---

## Quick Reference

### Formulas
```matlab
% Phasor from time-domain
Ẽ = E₀(a - jb)

% Direction from beta
k̂ = β/|β|

% H from E
H̃ = (1/η)·k̂ × Ẽ

% Poynting vector
S̄ = ½·Re{Ẽ × H̃*}

% Magnitude
|S̄| = |Ẽ|²/(2η)
```

### Units
```
E: V/m
H: A/m (console shows mA/m)
β: rad/m
η: Ω
S: W/m²
```

---

## Advanced Topics

### Non-Air Media

```matlab
% Calculate η for material
eps_r = 2.25;
mu_r = 1;
eta0 = 377;
eta = eta0 * sqrt(mu_r/eps_r);  % = 251 Ω

% Use in function
r = poynting_pw('time', a, b, E0, beta_vec, eta);
```

### Lossy Media

For lossy media with complex β:
```matlab
beta_complex = beta_real + 1j*alpha;
% Use magnitude for k̂
beta_mag = abs(beta_complex);
k_hat = beta_real/beta_mag;  % Real part
```

---

[← Master Index](poynting_pw_MASTER_INDEX.md)
