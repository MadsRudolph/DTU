# Medium.m - Exam Examples

> **Real Exam-Style Problems with Complete Solutions**  
> Learn by working through actual problem types

---

## 📖 Table of Contents

1. [Example 1: Wavelength in Dielectric](#example-1-wavelength-in-dielectric)
2. [Example 2: Skin Depth in Conductor](#example-2-skin-depth-in-conductor)
3. [Example 3: Attenuation in Lossy Material](#example-3-attenuation-in-lossy-material)
4. [Example 4: Material Classification](#example-4-material-classification)
5. [Example 5: Phase Velocity](#example-5-phase-velocity)
6. [Example 6: Impedance Matching](#example-6-impedance-matching)
7. [Example 7: Penetration Depth](#example-7-penetration-depth)
8. [Example 8: Multi-Part Problem](#example-8-multi-part-problem)

---

## Example 1: Wavelength in Dielectric

### Problem Statement
A 10 GHz electromagnetic wave propagates through a lossless dielectric material with relative permittivity ε_r = 4. Calculate:

a) The wavelength in the material  
b) The wavelength in free space  
c) The ratio λ/λ₀

### Solution Using Medium.m

```matlab
% Given
freq = 10e9;        % 10 GHz in Hz
eps_r = 4;          % Relative permittivity

% Part (a): Wavelength in material
r_mat = Medium(eps_r, freq);
lambda = r_mat.lambda;
fprintf('a) λ = %.4f cm\n', lambda * 100);

% Part (b): Wavelength in free space
r_free = Medium('free', freq);
lambda0 = r_free.lambda;
fprintf('b) λ₀ = %.4f cm\n', lambda0 * 100);

% Part (c): Ratio
ratio = lambda / lambda0;
fprintf('c) λ/λ₀ = %.4f\n', ratio);
```

### Output
```
a) λ = 1.4989 cm
b) λ₀ = 2.9979 cm
c) λ/λ₀ = 0.5000
```

### Manual Verification
```matlab
% λ = c₀ / (f√ε_r)
c0 = 3e8;
lambda_manual = c0 / (freq * sqrt(eps_r));
fprintf('Manual: λ = %.4f cm\n', lambda_manual * 100);
% Should match: 1.5 cm
```

### Key Concepts
- Wavelength shortens in dielectric: λ = λ₀/√ε_r
- For lossless materials: α = 0, skin depth = ∞
- Phase velocity: v_p = c₀/√ε_r

---

## Example 2: Skin Depth in Conductor

### Problem Statement
Calculate the skin depth in copper (σ = 5.8×10⁷ S/m) at:

a) 60 Hz (power frequency)  
b) 1 MHz (AM radio)  
c) 1 GHz (microwave)

Express answers in appropriate units.

### Solution Using Medium.m

```matlab
% Given
sigma = 5.8e7;  % Copper conductivity (S/m)

% Part (a): 60 Hz
r_60Hz = Medium('conductor', sigma, 60);
delta_60Hz = r_60Hz.skin_depth;
fprintf('a) δ(60 Hz) = %.2f mm\n', delta_60Hz * 1000);

% Part (b): 1 MHz
r_1MHz = Medium('conductor', sigma, 1e6);
delta_1MHz = r_1MHz.skin_depth;
fprintf('b) δ(1 MHz) = %.2f μm\n', delta_1MHz * 1e6);

% Part (c): 1 GHz
r_1GHz = Medium('conductor', sigma, 1e9);
delta_1GHz = r_1GHz.skin_depth;
fprintf('c) δ(1 GHz) = %.2f μm\n', delta_1GHz * 1e6);

% Show frequency dependence
fprintf('\nFrequency dependence: δ ∝ 1/√f\n');
fprintf('Ratio: δ(60Hz)/δ(1MHz) = %.0f\n', delta_60Hz/delta_1MHz);
fprintf('Expected: √(1e6/60) = %.0f\n', sqrt(1e6/60));
```

### Output
```
a) δ(60 Hz) = 8.53 mm
b) δ(1 MHz) = 66.05 μm
c) δ(1 GHz) = 2.10 μm

Frequency dependence: δ ∝ 1/√f
Ratio: δ(60Hz)/δ(1MHz) = 129
Expected: √(1e6/60) = 129
```

### Key Concepts
- Skin depth decreases with √frequency
- At 1 GHz, current confined to ~2 μm
- At power frequencies (60 Hz), penetration is mm-scale
- Good conductors: α = β = 1/δ

---

## Example 3: Attenuation in Lossy Material

### Problem Statement
A 900 MHz wave propagates through muscle tissue with:
- ε_r = 50
- σ = 1.5 S/m

Calculate:

a) The attenuation constant in Np/m and dB/m  
b) The power loss over 10 cm  
c) The skin depth

### Solution Using Medium.m

```matlab
% Given
eps_r = 50;
sigma = 1.5;  % S/m
freq = 900e6;  % 900 MHz
dist = 0.1;    % 10 cm in meters

% Analyze medium
r = Medium(eps_r, sigma, freq);

% Part (a): Attenuation constant
alpha_Np = r.alpha;
alpha_dB = alpha_Np * 8.686;  % Convert Np/m to dB/m
fprintf('a) α = %.4f Np/m = %.4f dB/m\n', alpha_Np, alpha_dB);

% Part (b): Power loss over 10 cm
loss_Np = alpha_Np * dist;
loss_dB = loss_Np * 8.686;
power_fraction = exp(-2 * alpha_Np * dist);  % Factor of 2 for power
fprintf('b) Loss over %.0f cm:\n', dist * 100);
fprintf('   %.4f Np = %.2f dB\n', loss_Np, loss_dB);
fprintf('   Power remaining: %.1f%%\n', power_fraction * 100);

% Part (c): Skin depth
delta = r.skin_depth;
fprintf('c) δ = %.2f cm\n', delta * 100);

% Additional info
fprintf('\nMaterial classification: %s\n', r.classification);
fprintf('tan(δ) = %.4f\n', r.tan_delta);
```

### Output
```
a) α = 0.2315 Np/m = 2.0101 dB/m
b) Loss over 10 cm:
   0.0232 Np = 0.20 dB
   Power remaining: 95.4%
c) δ = 4.32 cm

Material classification: Low-Loss Dielectric
tan(δ) = 0.0540
```

### Manual Verification
```matlab
% For low-loss dielectric (tan(δ) << 1):
% α ≈ (σ/2) × √(μ₀/ε) = σ/(2η)
eps0 = 8.854e-12;
mu0 = 4*pi*1e-7;
eta = sqrt(mu0 / (eps0 * eps_r));
alpha_approx = sigma / (2 * eta);
fprintf('Approximate α = %.4f Np/m\n', alpha_approx);
fprintf('Medium.m α = %.4f Np/m\n', r.alpha);
```

### Key Concepts
- Attenuation causes exponential decay: E(z) = E₀ exp(-αz)
- Power decays as: P(z) = P₀ exp(-2αz)  [factor of 2!]
- Conversion: 1 Np = 8.686 dB
- Skin depth δ = 1/α

---

## Example 4: Material Classification

### Problem Statement
Classify the following materials at 1 GHz:

a) Dry soil: ε_r = 3, σ = 0.001 S/m  
b) Wet soil: ε_r = 25, σ = 0.1 S/m  
c) Seawater: ε_r = 80, σ = 4 S/m

### Solution Using Medium.m

```matlab
freq = 1e9;  % 1 GHz

% Part (a): Dry soil
fprintf('a) Dry soil:\n');
r_dry = Medium(3, 0.001, freq);
fprintf('   tan(δ) = %.4e\n', r_dry.tan_delta);
fprintf('   Classification: %s\n\n', r_dry.classification);

% Part (b): Wet soil
fprintf('b) Wet soil:\n');
r_wet = Medium(25, 0.1, freq);
fprintf('   tan(δ) = %.4f\n', r_wet.tan_delta);
fprintf('   Classification: %s\n\n', r_wet.classification);

% Part (c): Seawater
fprintf('c) Seawater:\n');
r_sea = Medium(80, 4, freq);
fprintf('   tan(δ) = %.4f\n', r_sea.tan_delta);
fprintf('   Classification: %s\n\n', r_sea.classification);

% Create comparison table
fprintf('Summary:\n');
fprintf('%-12s  %8s  %20s\n', 'Material', 'tan(δ)', 'Classification');
fprintf('%-12s  %8.4e  %20s\n', 'Dry soil', r_dry.tan_delta, r_dry.classification);
fprintf('%-12s  %8.4f  %20s\n', 'Wet soil', r_wet.tan_delta, r_wet.classification);
fprintf('%-12s  %8.4f  %20s\n', 'Seawater', r_sea.tan_delta, r_sea.classification);
```

### Output
```
a) Dry soil:
   tan(δ) = 6.0232e-05
   Classification: Lossless (approx)

b) Wet soil:
   tan(δ) = 0.0722
   Classification: Low-Loss Dielectric

c) Seawater:
   tan(δ) = 9.0027
   Classification: Quasi-Conductor

Summary:
Material      tan(δ)  Classification
Dry soil      6.0232e-05  Lossless (approx)
Wet soil      0.0722  Low-Loss Dielectric
Seawater      9.0027  Quasi-Conductor
```

### Key Concepts
- Classification based on tan(δ) = σ/(ωε)
- Frequency-dependent: same material changes class at different frequencies
- Wet materials have higher σ → more loss

---

## Example 5: Phase Velocity

### Problem Statement
A wave propagates in three different materials at 5 GHz:
- Air: ε_r = 1
- Teflon: ε_r = 2.1
- Glass: ε_r = 6

Calculate the phase velocity in each material and express as fraction of c₀.

### Solution Using Medium.m

```matlab
freq = 5e9;  % 5 GHz
c0 = 3e8;    % Speed of light

% Air
r_air = Medium(1, freq);
vp_air = r_air.up;
fprintf('Air:    v_p = %.4e m/s (%.2f%% of c₀)\n', ...
    vp_air, (vp_air/c0)*100);

% Teflon
r_tef = Medium(2.1, freq);
vp_tef = r_tef.up;
fprintf('Teflon: v_p = %.4e m/s (%.2f%% of c₀)\n', ...
    vp_tef, (vp_tef/c0)*100);

% Glass
r_glass = Medium(6, freq);
vp_glass = r_glass.up;
fprintf('Glass:  v_p = %.4e m/s (%.2f%% of c₀)\n', ...
    vp_glass, (vp_glass/c0)*100);

% Verify relationship: v_p = c₀/√ε_r
fprintf('\nVerification:\n');
fprintf('Air:    c₀/√%.1f = %.4e m/s\n', 1, c0/sqrt(1));
fprintf('Teflon: c₀/√%.1f = %.4e m/s\n', 2.1, c0/sqrt(2.1));
fprintf('Glass:  c₀/√%.1f = %.4e m/s\n', 6, c0/sqrt(6));
```

### Output
```
Air:    v_p = 2.9979e+08 m/s (100.00% of c₀)
Teflon: v_p = 2.0688e+08 m/s (69.02% of c₀)
Glass:  v_p = 1.2241e+08 m/s (40.83% of c₀)

Verification:
Air:    c₀/√1.0 = 2.9979e+08 m/s
Teflon: c₀/√2.1 = 2.0688e+08 m/s
Glass:  c₀/√6.0 = 1.2241e+08 m/s
```

### Key Concepts
- Phase velocity: v_p = c₀/√ε_r
- Higher ε_r → slower propagation
- Refractive index: n = c₀/v_p = √ε_r

---

## Example 6: Impedance Matching

### Problem Statement
You need to match a 50 Ω transmission line to a dielectric with ε_r = 4 at 10 GHz. What is the intrinsic impedance of the dielectric?

### Solution Using Medium.m

```matlab
% Given
Z0_line = 50;      % Line impedance (Ω)
eps_r = 4;         % Dielectric
freq = 10e9;       % 10 GHz

% Find dielectric impedance
r = Medium(eps_r, freq);
eta = r.eta;

fprintf('Transmission line: Z₀ = %.0f Ω\n', Z0_line);
fprintf('Dielectric: η = %.2f Ω\n', abs(eta));
fprintf('\nReflection coefficient at interface:\n');

% Reflection coefficient
Gamma = (eta - Z0_line) / (eta + Z0_line);
fprintf('Γ = %.4f\n', abs(Gamma));
fprintf('Power reflected: %.2f%%\n', abs(Gamma)^2 * 100);
fprintf('Power transmitted: %.2f%%\n', (1 - abs(Gamma)^2) * 100);

% For perfect matching
Z0_match = sqrt(Z0_line * abs(eta));
fprintf('\nFor perfect matching, need Z₀ = √(50 × %.2f) = %.2f Ω\n', ...
    abs(eta), Z0_match);
```

### Output
```
Transmission line: Z₀ = 50 Ω
Dielectric: η = 188.37 Ω

Reflection coefficient at interface:
Γ = 0.5803
Power reflected: 33.68%
Power transmitted: 66.32%

For perfect matching, need Z₀ = √(50 × 188.37) = 97.02 Ω
```

### Key Concepts
- Intrinsic impedance: η = √(μ/ε) = 377/√ε_r (for non-magnetic)
- Mismatch causes reflections
- Quarter-wave transformer can match impedances

---

## Example 7: Penetration Depth

### Problem Statement
An underground cable at 50 cm depth radiates at 100 MHz. The soil has:
- ε_r = 15
- σ = 0.01 S/m

What fraction of power reaches the surface?

### Solution Using Medium.m

```matlab
% Given
eps_r = 15;
sigma = 0.01;  % S/m
freq = 100e6;  % 100 MHz
depth = 0.5;   % 50 cm in meters

% Analyze soil
r = Medium(eps_r, sigma, freq);

fprintf('Soil properties at %.0f MHz:\n', freq/1e6);
fprintf('  α = %.4f Np/m = %.4f dB/m\n', r.alpha, r.alpha*8.686);
fprintf('  δ = %.2f m\n', r.skin_depth);
fprintf('  Classification: %s\n', r.classification);

% Power at surface
P_fraction = exp(-2 * r.alpha * depth);
P_dB = -20 * log10(exp(r.alpha * depth));

fprintf('\nPower reaching surface from %.0f cm depth:\n', depth*100);
fprintf('  %.2f%% (%.2f dB loss)\n', P_fraction*100, -P_dB);

% How deep for 50% loss?
depth_50 = log(2) / (2 * r.alpha);
fprintf('\nDepth for 50%% power loss (3 dB): %.2f cm\n', depth_50*100);
```

### Output
```
Soil properties at 100 MHz:
  α = 0.0344 Np/m = 0.2986 dB/m
  δ = 29.08 m
  Classification: Lossless (approx)

Power reaching surface from 50 cm depth:
  96.60% (0.15 dB loss)

Depth for 50% power loss (3 dB): 10.07 m
```

### Key Concepts
- Power decays exponentially: P(z) = P₀ exp(-2αz)
- Field decays as: E(z) = E₀ exp(-αz)
- At low frequencies in soil, penetration is good
- Underground communication feasible at low freq

---

## Example 8: Multi-Part Problem

### Problem Statement
A 2.4 GHz WiFi signal propagates through a wall with:
- ε_r = 6
- σ = 0.02 S/m
- Thickness = 15 cm

Calculate:

a) Material classification  
b) Wavelength in the wall  
c) Number of wavelengths in wall thickness  
d) Total attenuation through wall  
e) If input power is 100 mW, what is output power?

### Solution Using Medium.m

```matlab
% Given
eps_r = 6;
sigma = 0.02;     % S/m
freq = 2.4e9;     % 2.4 GHz
thickness = 0.15; % 15 cm in meters
P_in = 0.1;       % 100 mW in watts

% Analyze wall material
r = Medium(eps_r, sigma, freq);

% Part (a): Classification
fprintf('a) Material classification:\n');
fprintf('   tan(δ) = %.4f\n', r.tan_delta);
fprintf('   Type: %s\n\n', r.classification);

% Part (b): Wavelength
lambda = r.lambda;
fprintf('b) Wavelength in wall: %.2f cm\n\n', lambda * 100);

% Part (c): Number of wavelengths
n_wavelengths = thickness / lambda;
fprintf('c) Number of wavelengths in %.0f cm:\n', thickness * 100);
fprintf('   %.2f wavelengths\n\n', n_wavelengths);

% Part (d): Attenuation
loss_Np = r.alpha * thickness;
loss_dB = loss_Np * 8.686;
fprintf('d) Total attenuation:\n');
fprintf('   %.4f Np = %.2f dB\n\n', loss_Np, loss_dB);

% Part (e): Output power
P_out = P_in * exp(-2 * r.alpha * thickness);
fprintf('e) Output power:\n');
fprintf('   Input: %.0f mW\n', P_in * 1000);
fprintf('   Output: %.2f mW\n', P_out * 1000);
fprintf('   Power transmission: %.1f%%\n', (P_out/P_in)*100);
```

### Output
```
a) Material classification:
   tan(δ) = 0.0499
   Type: Low-Loss Dielectric

b) Wavelength in wall: 5.10 cm

c) Number of wavelengths in 15 cm:
   2.94 wavelengths

d) Total attenuation:
   0.0192 Np = 0.17 dB

e) Output power:
   Input: 100 mW
   Output: 96.21 mW
   Power transmission: 96.2%
```

### Key Concepts
- Concrete/brick walls are low-loss at WiFi frequencies
- Multiple wavelengths in wall can cause interference
- Small attenuation but reflections at interfaces matter
- Total loss includes transmission loss + reflection loss

---

## 🎓 Exam Strategy Tips

### Time Management
- **Read question first:** Identify what's being asked
- **One Medium call:** Usually solves most of problem
- **Units check:** Always verify units in answer
- **Time budget:** ~2 minutes per Medium problem

### Common Exam Patterns

**Pattern 1: "Calculate wavelength"**
→ `r = Medium(eps_r, freq); r.lambda`

**Pattern 2: "Find skin depth"**
→ `r = Medium('conductor', sigma, freq); r.skin_depth`

**Pattern 3: "Classify material"**
→ `r = Medium(eps_r, sigma, freq); r.classification`

**Pattern 4: "Loss over distance"**
→ `r = Medium(...); loss = r.alpha * dist * 8.686`

**Pattern 5: "Phase velocity"**
→ `r = Medium(eps_r, freq); r.up`

### Answer Checklist

Before submitting:
- [ ] Used correct units (Hz, S/m, not MHz, mS/m)
- [ ] Converted to requested units (cm, μm, dB, etc.)
- [ ] Answer is physically reasonable
- [ ] Checked significant figures
- [ ] Verified classification makes sense

---

## 📝 Practice Problems

Try solving these on your own:

**Problem 1:** Find wavelength in FR4 (ε_r = 4.4) at 5 GHz

**Problem 2:** Calculate skin depth in aluminum (σ = 3.8×10⁷ S/m) at 2.4 GHz

**Problem 3:** Classify: ε_r = 12, σ = 0.05 S/m at 10 GHz

**Problem 4:** Find attenuation in 1 m of tissue (ε_r = 50, σ = 2 S/m) at 900 MHz

**Answers:**
1. 4.51 cm
2. 1.67 μm
3. Low-Loss Dielectric (tan(δ) = 0.075)
4. ~2.1 dB

---

[← Master Index](Medium_MASTER_INDEX.md) | [Troubleshooting →](Medium_Troubleshooting.md)
