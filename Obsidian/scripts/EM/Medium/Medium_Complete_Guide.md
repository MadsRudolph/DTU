# Medium.m - Complete Guide

> **Comprehensive 30-Minute Reference**  
> Everything you need to master electromagnetic wave propagation in materials

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Theory & Background](#theory--background)
3. [Function Modes](#function-modes)
4. [Complete Workflows](#complete-workflows)
5. [Output Structure](#output-structure)
6. [Common Problem Types](#common-problem-types)
7. [Advanced Topics](#advanced-topics)
8. [Reference Tables](#reference-tables)

---

## Introduction

### What is Medium.m?

**Medium.m** is a unified MATLAB function that calculates electromagnetic wave propagation parameters in ANY type of material - from perfect lossless dielectrics to lossy materials to good conductors.

**One function replaces dozens of formulas.**

### When to Use Medium

Use Medium.m when you need to:
- Calculate wavelength in a material
- Find skin depth in conductors
- Determine attenuation constants
- Calculate intrinsic impedance
- Classify materials (conductor vs dielectric)
- Find phase velocity or propagation constant

### What Medium Calculates

| Category | Parameters |
|----------|------------|
| **Propagation** | α (attenuation), β (phase constant), γ (complex propagation constant) |
| **Wave** | λ (wavelength), v_p (phase velocity), n (refractive index) |
| **Impedance** | η (intrinsic impedance), R_s (surface resistance) |
| **Loss** | tan(δ) (loss tangent), δ (skin depth), classification |

---

## Theory & Background

### Maxwell's Equations in Materials

In a homogeneous material, plane wave propagation is governed by:

**Complex propagation constant:**
```
γ = α + jβ = √(jωμ(σ + jωε))
```

Where:
- α = attenuation constant (Np/m)
- β = phase constant (rad/m)
- μ = μ_r μ₀ (permeability)
- ε = ε_r ε₀ (permittivity)
- σ = conductivity (S/m)
- ω = 2πf (angular frequency)

**Wave equation solution:**
```
E(z) = E₀ e^(-αz) e^(-jβz)
     = E₀ e^(-γz)
```

The wave attenuates by factor e^(-αz) and phase shifts by βz.

### Material Classification

Materials are classified by **loss tangent:**

```
tan(δ) = σ/(ωε)
```

| tan(δ) Range | Classification | Behavior |
|--------------|----------------|----------|
| < 0.01 | Lossless (approx) | α ≈ 0, β ≈ ω√(με) |
| 0.01 - 0.1 | Low-Loss Dielectric | Small attenuation |
| 0.1 - 10 | Quasi-Conductor | Moderate loss |
| > 10 | Good Conductor | α ≈ β |

### Key Parameters

**Wavelength:**
```
λ = 2π/β  (in material)
λ₀ = c₀/f  (in free space)
```

**Phase Velocity:**
```
v_p = ω/β = fλ
For lossless: v_p = c₀/√(ε_r μ_r)
```

**Intrinsic Impedance:**
```
η = √(jωμ/(σ + jωε))
For lossless: η = √(μ/ε) = (μ₀/ε₀)√(μ_r/ε_r) = 377√(μ_r/ε_r)
```

**Skin Depth:**
```
δ = 1/α
For good conductor: δ = √(2/(ωμσ)) = 1/√(πfμσ)
```

---

## Function Modes

Medium.m has 6 modes to handle different types of problems.

### Mode 1: Lossless Dielectric

**Use when:** Material has σ = 0 (no conductivity)  
**Examples:** Air, glass, plastics, ceramics

**Syntax:**
```matlab
result = Medium(eps_r, freq)
result = Medium(eps_r, freq, mu_r)
```

**Parameters:**
- `eps_r` - Relative permittivity (dimensionless)
- `freq` - Frequency (Hz)
- `mu_r` - Relative permeability (default: 1)

**Example:**
```matlab
% Glass at 10 GHz
r = Medium(4, 10e9);

% Results:
r.lambda        % Wavelength in glass
r.up            % Phase velocity
r.eta           % Intrinsic impedance (real)
r.n             % Refractive index = √ε_r
r.alpha         % = 0 (lossless)
r.skin_depth    % = Inf (no attenuation)
```

**Physics:**
- No attenuation: α = 0
- Real impedance: η = 377/√ε_r Ω
- Wavelength shortened: λ = λ₀/√ε_r
- Phase velocity reduced: v_p = c₀/√ε_r

---

### Mode 2: Lossy Material

**Use when:** Material has 0 < σ < 10⁶ S/m  
**Examples:** Tissue, soil, seawater, lossy dielectrics

**Syntax:**
```matlab
result = Medium(eps_r, sigma, freq)
result = Medium(eps_r, sigma, freq, mu_r)
result = Medium(eps_r, sigma, freq, mu_r, 'Name')
```

**Parameters:**
- `eps_r` - Relative permittivity
- `sigma` - Conductivity (S/m)
- `freq` - Frequency (Hz)
- `mu_r` - Relative permeability (default: 1)
- `'Name'` - Optional label for display

**Example:**
```matlab
% Muscle tissue at 900 MHz
r = Medium(50, 1.5, 900e6, 1, 'Muscle');

% Results:
r.alpha         % Attenuation constant
r.beta          % Phase constant
r.skin_depth    % Penetration depth
r.tan_delta     % Loss tangent
r.classification % Material type
r.eta           % Complex impedance
```

**Physics:**
- Finite attenuation: α > 0
- Complex impedance: η has phase
- Wave decays exponentially
- Skin depth: δ = 1/α

**Approximations:**

For **low-loss** (tan(δ) << 1):
```matlab
α ≈ (σ/2)√(μ/ε) = σ/(2η)
β ≈ ω√(με)
η ≈ √(μ/ε)
```

For **quasi-conductor** (tan(δ) ≈ 1):
```matlab
α ≈ β ≈ ω√(με/2)√(1 + σ/(ωε))
```

---

### Mode 3: Good Conductor

**Use when:** σ > 10⁶ S/m (metals)  
**Examples:** Copper, aluminum, gold, silver

**Syntax:**
```matlab
result = Medium('conductor', sigma, freq)
result = Medium('conductor', sigma, freq, mu_r)
```

**Parameters:**
- `sigma` - Conductivity (S/m)
- `freq` - Frequency (Hz)
- `mu_r` - Relative permeability (default: 1)

**Example:**
```matlab
% Copper at 1 GHz
r = Medium('conductor', 5.8e7, 1e9);

% Results:
r.alpha         % = β for good conductor
r.beta          % = α
r.skin_depth    % Very small (μm scale)
r.Rs            % Surface resistance
r.eta           % = (1+j)R_s
```

**Physics:**

For good conductors (σ >> ωε):
```
α = β = √(πfμσ) = 1/δ
δ = √(2/(ωμσ)) = 1/√(πfμσ)
η = (1+j)√(ωμ/(2σ)) = (1+j)R_s
R_s = √(ωμ/(2σ))  [surface resistance]
```

**Key Properties:**
- Equal attenuation and phase: α = β
- Impedance at 45°: η = (1+j)R_s
- Skin depth inversely proportional to √f
- Current confined to surface

---

### Mode 4: From Loss Tangent

**Use when:** Given tan(δ) instead of σ  
**Examples:** Material datasheets often specify tan(δ)

**Syntax:**
```matlab
result = Medium('tand', eps_r, tan_delta, freq)
result = Medium('tand', eps_r, tan_delta, freq, mu_r)
```

**Parameters:**
- `eps_r` - Relative permittivity
- `tan_delta` - Loss tangent
- `freq` - Frequency (Hz)
- `mu_r` - Relative permeability (default: 1)

**Example:**
```matlab
% FR4 substrate: ε_r = 4.4, tan(δ) = 0.02 at 5 GHz
r = Medium('tand', 4.4, 0.02, 5e9);

% Function calculates:
sigma = tan_delta * omega * eps;
% Then uses lossy mode
```

**Conversion:**
```
tan(δ) = σ/(ωε)
σ = tan(δ) × ω × ε
```

---

### Mode 5: Skin Depth Only

**Use when:** Only need skin depth, nothing else  
**Examples:** Quick conductor analysis

**Syntax:**
```matlab
result = Medium('skin', sigma, freq)
result = Medium('skin', sigma, freq, mu_r)
```

**Parameters:**
- `sigma` - Conductivity (S/m)
- `freq` - Frequency (Hz)
- `mu_r` - Relative permeability (default: 1)

**Example:**
```matlab
% Skin depth in copper at 100 MHz
r = Medium('skin', 5.8e7, 100e6);
delta = r.skin_depth;  % 6.6 μm
```

**Use case:**
- Fast calculation
- Only care about penetration depth
- Conductor loss estimation

---

### Mode 6: Free Space

**Use when:** Need vacuum/air baseline parameters  
**Examples:** Wavelength in free space, comparing with materials

**Syntax:**
```matlab
result = Medium('free', freq)
```

**Parameters:**
- `freq` - Frequency (Hz)

**Example:**
```matlab
% Free space at 2.4 GHz
r = Medium('free', 2.4e9);

% Results:
r.lambda0       % = c₀/f
r.eta0          % = 377 Ω
r.k0            % = 2π/λ₀
r.c0            % = 2.998×10⁸ m/s
```

**Constants provided:**
- c₀ = 2.99792458×10⁸ m/s
- η₀ = 376.73 Ω
- ε₀ = 8.854×10⁻¹² F/m
- μ₀ = 4π×10⁻⁷ H/m

---

## Complete Workflows

### Workflow 1: Find Wavelength in Material

**Problem:** Calculate λ at frequency f in material with ε_r

**Solution:**
```matlab
% Input
eps_r = 4;      % Material permittivity
freq = 10e9;    % Frequency in Hz

% Calculate
r = Medium(eps_r, freq);
lambda_m = r.lambda * 100;  % Convert to cm

% Display
fprintf('λ = %.2f cm\n', lambda_m);
```

**One-liner:**
```matlab
lambda_cm = Medium(4, 10e9).lambda * 100;
```

---

### Workflow 2: Calculate Skin Depth

**Problem:** Find δ in conductor at frequency f

**Solution:**
```matlab
% Input
sigma = 5.8e7;   % Copper conductivity
freq = 1e9;      % 1 GHz

% Calculate
r = Medium('conductor', sigma, freq);
delta_um = r.skin_depth * 1e6;  % Convert to μm

% Display
fprintf('δ = %.2f μm\n', delta_um);
```

---

### Workflow 3: Determine Material Type

**Problem:** Classify material given ε_r, σ, and f

**Solution:**
```matlab
% Input
eps_r = 50;
sigma = 1.5;
freq = 900e6;

% Analyze
r = Medium(eps_r, sigma, freq);

% Display
fprintf('tan(δ) = %.4f\n', r.tan_delta);
fprintf('Classification: %s\n', r.classification);
```

---

### Workflow 4: Calculate Attenuation Over Distance

**Problem:** Find power loss over distance d

**Solution:**
```matlab
% Input
eps_r = 80;
sigma = 4;
freq = 1e6;
distance = 1.0;  % meters

% Calculate
r = Medium(eps_r, sigma, freq);
loss_Np = r.alpha * distance;
loss_dB = loss_Np * 8.686;
power_fraction = exp(-2 * r.alpha * distance);

% Display
fprintf('Loss: %.2f dB\n', loss_dB);
fprintf('Power remaining: %.1f%%\n', power_fraction*100);
```

**Key:** Power decays as exp(-2αz), field as exp(-αz)

---

### Workflow 5: Compare Material with Free Space

**Problem:** How much does material affect wavelength?

**Solution:**
```matlab
freq = 5e9;
eps_r = 2.25;

% Material
r_mat = Medium(eps_r, freq);

% Free space
r_free = Medium('free', freq);

% Compare
ratio = r_mat.lambda / r_free.lambda;
fprintf('λ/λ₀ = %.4f = 1/√%.2f\n', ratio, eps_r);
```

---

## Output Structure

Every Medium call returns a struct with these fields:

### Always Present

| Field | Description | Units |
|-------|-------------|-------|
| `eps_r` | Relative permittivity | - |
| `mu_r` | Relative permeability | - |
| `sigma` | Conductivity | S/m |
| `freq` | Frequency | Hz |
| `omega` | Angular frequency | rad/s |
| `classification` | Material type | string |

### Wave Parameters

| Field | Description | Units |
|-------|-------------|-------|
| `gamma` | Complex propagation constant | 1/m |
| `alpha` | Attenuation constant | Np/m |
| `beta` | Phase constant | rad/m |
| `lambda` | Wavelength | m |
| `up` | Phase velocity | m/s |
| `n` | Refractive index | - |

### Impedance

| Field | Description | Units |
|-------|-------------|-------|
| `eta` | Intrinsic impedance | Ω |
| `Rs` | Surface resistance (conductors) | Ω |

### Loss Metrics

| Field | Description | Units |
|-------|-------------|-------|
| `tan_delta` | Loss tangent | - |
| `skin_depth` | Skin depth | m |

### Mode-Specific

**Free space mode adds:**
- `c0` - Speed of light
- `eta0` - Free space impedance
- `k0` - Free space wavenumber
- `lambda0` - Free space wavelength

---

## Common Problem Types

### Type 1: Wavelength Calculation

**Pattern:** "Find λ in material at frequency f"

```matlab
r = Medium(eps_r, freq);
lambda = r.lambda;  % in meters
lambda_cm = lambda * 100;  % in cm
```

### Type 2: Skin Depth

**Pattern:** "Find skin depth in conductor"

```matlab
r = Medium('conductor', sigma, freq);
delta = r.skin_depth;  % in meters
delta_um = delta * 1e6;  % in micrometers
```

### Type 3: Material Classification

**Pattern:** "What type of material is this?"

```matlab
r = Medium(eps_r, sigma, freq);
fprintf('Classification: %s\n', r.classification);
fprintf('tan(δ) = %.4f\n', r.tan_delta);
```

### Type 4: Attenuation

**Pattern:** "How much loss over distance d?"

```matlab
r = Medium(eps_r, sigma, freq);
loss_dB = r.alpha * distance * 8.686;  % Np/m to dB/m
```

### Type 5: Phase Velocity

**Pattern:** "What is v_p in the material?"

```matlab
r = Medium(eps_r, freq);
v_p = r.up;  % m/s
v_rel = v_p / 3e8;  % fraction of c
```

---

## Advanced Topics

### Frequency Sweeps

Analyze material over frequency range:

```matlab
freqs = logspace(6, 10, 100);  % 1 MHz to 10 GHz
eps_r = 4;
sigma = 0.01;

alpha = zeros(size(freqs));
for i = 1:length(freqs)
    r = Medium(eps_r, sigma, freqs(i));
    alpha(i) = r.alpha;
end

loglog(freqs, alpha);
xlabel('Frequency (Hz)');
ylabel('Attenuation (Np/m)');
```

### Penetration Depth vs Frequency

```matlab
freqs = logspace(6, 9, 100);
sigma = 5.8e7;  % Copper

delta = zeros(size(freqs));
for i = 1:length(freqs)
    r = Medium('conductor', sigma, freqs(i));
    delta(i) = r.skin_depth * 1e6;  % Convert to μm
end

loglog(freqs/1e6, delta);
xlabel('Frequency (MHz)');
ylabel('Skin Depth (μm)');
title('Copper Skin Depth vs Frequency');
grid on;
```

### Material Comparison

```matlab
freq = 1e9;
materials = {
    'Air', 1, 0;
    'Glass', 4, 0;
    'FR4', 4.4, 0.02*2*pi*freq*8.854e-12*4.4;
    'Tissue', 50, 1.5;
};

fprintf('%-10s %8s %8s %12s\n', 'Material', 'λ (cm)', 'α (dB/m)', 'Type');
for i = 1:size(materials, 1)
    name = materials{i,1};
    eps_r = materials{i,2};
    sigma = materials{i,3};
    
    r = Medium(eps_r, sigma, freq);
    fprintf('%-10s %8.2f %8.2f %12s\n', name, r.lambda*100, ...
        r.alpha*8.686, r.classification);
end
```

---

## Reference Tables

### Common Materials

**Lossless Dielectrics:**
| Material | ε_r | Typical Use |
|----------|-----|-------------|
| Air/Vacuum | 1.0 | Reference |
| Teflon (PTFE) | 2.1 | Low-loss substrate |
| Polyethylene | 2.25 | Cables |
| Glass | 4-6 | Windows, fibers |
| FR4 | 4.4 | PCB substrate |
| Alumina | 9.8 | Ceramic substrate |

**Conductors:**
| Material | σ (S/m) | Notes |
|----------|---------|-------|
| Silver | 6.1×10⁷ | Best conductor |
| Copper | 5.8×10⁷ | Standard |
| Gold | 4.1×10⁷ | Corrosion resistant |
| Aluminum | 3.8×10⁷ | Lightweight |
| Brass | 1.6×10⁷ | Alloy |

**Lossy Materials:**
| Material | ε_r | σ (S/m) @ 1 GHz |
|----------|-----|-----------------|
| Dry soil | 3 | 0.001 |
| Wet soil | 25 | 0.1 |
| Seawater | 80 | 4 |
| Muscle tissue | 50 | 1.5 @ 900 MHz |
| Fat tissue | 10 | 0.1 @ 900 MHz |

### Unit Conversions

**Frequency:**
```matlab
MHz_to_Hz = 1e6
GHz_to_Hz = 1e9
```

**Length:**
```matlab
m_to_cm = 100
m_to_mm = 1000
m_to_um = 1e6
```

**Attenuation:**
```matlab
Np_to_dB = 8.686
dB_to_Np = 1/8.686
```

**Conductivity:**
```matlab
% No conversion needed - always use S/m
```

### Quick Formulas

**Lossless material:**
```
λ = c₀/(f√ε_r)
v_p = c₀/√ε_r
η = 377/√ε_r  [Ω]
n = √ε_r
```

**Good conductor:**
```
δ = 1/√(πfμσ)
α = β = 1/δ
R_s = √(πfμ/σ)
```

**General lossy:**
```
tan(δ) = σ/(ωε)
Low-loss: α ≈ σ/(2η)
```

---

[← Master Index](Medium_MASTER_INDEX.md)
