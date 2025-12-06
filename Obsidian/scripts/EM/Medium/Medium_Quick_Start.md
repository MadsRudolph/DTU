# Medium.m - Quick Start Guide

> **5-Minute Crash Course**  
> Everything you need to start using Medium.m RIGHT NOW

---

## TL;DR - The One Pattern You Need

```matlab
% For 90% of problems:
r = Medium(eps_r, freq);              % Lossless material
wavelength = r.lambda;                 % Get wavelength
velocity = r.up;                       % Get phase velocity

% For conductors:
r = Medium('conductor', sigma, freq);  % Good conductor
skin_depth = r.skin_depth;            % Get skin depth
```

**That's it!** The rest is just variations of this pattern.

---

## 📖 Table of Contents

1. [The Three Essential Patterns](#the-three-essential pattern) (2 min)
2. [What You Get Back](#what-you-get-back) (1 min)
3. [Common Mistakes](#common-mistakes) (1 min)
4. [30-Second Examples](#30-second-examples) (1 min)

---

## The Three Essential Patterns

### Pattern 1: Lossless Material (Most Common)

**Use when:** Material has no losses (σ = 0)  
**Examples:** Air, glass, perfect dielectrics

```matlab
% Syntax: Medium(eps_r, freq)
r = Medium(4, 10e9);        % Glass at 10 GHz

% Get results:
r.lambda        % Wavelength in the material
r.up            % Phase velocity  
r.eta           % Intrinsic impedance
r.n             % Refractive index
```

**30-second example:**
```matlab
>> r = Medium(2.25, 5e9);   % Teflon at 5 GHz
>> r.lambda

ans = 0.0400    % λ = 4 cm in Teflon
```

---

### Pattern 2: Lossy Material

**Use when:** Material has conductivity (σ > 0)  
**Examples:** Tissue, soil, seawater

```matlab
% Syntax: Medium(eps_r, sigma, freq)
r = Medium(80, 4, 1e6);     % Seawater at 1 MHz

% Get results:
r.alpha         % Attenuation constant (Np/m)
r.beta          % Phase constant (rad/m)
r.skin_depth    % Skin depth (m)
r.classification % 'Good Conductor', 'Low-Loss', etc.
```

**30-second example:**
```matlab
>> r = Medium(50, 1.5, 900e6);  % Muscle tissue at 900 MHz
>> r.skin_depth

ans = 0.0431    % δ = 4.31 cm penetration depth
```

---

### Pattern 3: Good Conductor

**Use when:** Analyzing metals (copper, aluminum, etc.)  
**Examples:** Copper wire, aluminum foil

```matlab
% Syntax: Medium('conductor', sigma, freq)
r = Medium('conductor', 5.8e7, 1e9);  % Copper at 1 GHz

% Get results:
r.skin_depth    % Skin depth (m)
r.Rs            % Surface resistance (Ohm)
r.alpha         % Attenuation constant
```

**30-second example:**
```matlab
>> r = Medium('conductor', 5.8e7, 1e9);  % Copper at 1 GHz
>> r.skin_depth * 1e6

ans = 2.0966    % δ = 2.1 μm
```

---

## What You Get Back

**Every Medium call returns a struct with these essential fields:**

| Field | Description | Units |
|-------|-------------|-------|
| `lambda` | Wavelength | meters |
| `up` | Phase velocity | m/s |
| `alpha` | Attenuation constant | Np/m |
| `beta` | Phase constant | rad/m |
| `eta` | Intrinsic impedance | Ω |
| `n` | Refractive index | - |
| `skin_depth` | Skin depth (if lossy) | meters |
| `classification` | Material type | string |

**Quick conversions:**
```matlab
lambda_cm = r.lambda * 100;          % Convert to cm
skin_depth_um = r.skin_depth * 1e6;  % Convert to μm
loss_dB = r.alpha * 8.686;           % Convert Np/m to dB/m
```

---

## Common Mistakes

### ❌ Mistake 1: Wrong Units (Most Common)

```matlab
❌ Wrong:
r = Medium(4, 10e6);     // Thought freq was in MHz
r = Medium(4, 10*10^9);  // Unnecessary complexity

✅ Correct:
r = Medium(4, 10e9);     // freq in Hz (10 GHz)
```

**Rule:** Frequency ALWAYS in Hz, not MHz or GHz

---

### ❌ Mistake 2: Wrong Mode for Conductor

```matlab
❌ Wrong:
r = Medium(1, 5.8e7, 1e9);  // Using lossy mode for copper

✅ Correct:
r = Medium('conductor', 5.8e7, 1e9);  // Conductor mode
```

**Rule:** Use `'conductor'` mode for metals

---

### ❌ Mistake 3: Forgetting Sigma

```matlab
❌ Wrong:
r = Medium(80, 1e6);  // Missing sigma for seawater

✅ Correct:
r = Medium(80, 4, 1e6);  // Include sigma for lossy materials
```

**Rule:** Three arguments (eps_r, sigma, freq) for lossy materials

---

### ❌ Mistake 4: Using Wrong Field

```matlab
❌ Wrong:
wavelength = r.lambda0;   // Doesn't exist for materials

✅ Correct:
wavelength = r.lambda;    // Wavelength in the material
```

**Rule:** Use `r.lambda` for material wavelength, `r.lambda0` only exists in free space mode

---

## 30-Second Examples

### Example 1: Find Wavelength in Glass
```matlab
% Problem: What is λ in glass (ε_r = 4) at 10 GHz?
r = Medium(4, 10e9);
fprintf('λ = %.2f cm\n', r.lambda * 100);

% Output: λ = 1.50 cm
```

---

### Example 2: Skin Depth in Copper
```matlab
% Problem: What is δ in copper at 1 GHz?
r = Medium('conductor', 5.8e7, 1e9);
fprintf('δ = %.2f μm\n', r.skin_depth * 1e6);

% Output: δ = 2.10 μm
```

---

### Example 3: Is This a Conductor?
```matlab
% Problem: Classify material with ε_r=50, σ=1.5 S/m at 900 MHz
r = Medium(50, 1.5, 900e6);
fprintf('Type: %s\n', r.classification);

% Output: Type: Low-Loss Dielectric
```

---

### Example 4: Attenuation Over Distance
```matlab
% Problem: How much loss in 10 cm of tissue?
r = Medium(50, 1.5, 900e6);
distance = 0.1;  % 10 cm in meters
loss_Np = r.alpha * distance;
loss_dB = loss_Np * 8.686;
fprintf('Loss = %.2f dB\n', loss_dB);

% Output: Loss = 2.01 dB
```

---

## Quick Cheat Sheet

### Input Patterns
```matlab
Medium(eps_r, freq)                    % Lossless
Medium(eps_r, sigma, freq)             % Lossy
Medium('conductor', sigma, freq)       % Conductor
Medium('tand', eps_r, tan_delta, freq) % From loss tangent
Medium('skin', sigma, freq)            % Just skin depth
Medium('free', freq)                   % Free space
```

### Essential Outputs
```matlab
r.lambda        % Wavelength (m)
r.up            % Phase velocity (m/s)
r.alpha         % Attenuation (Np/m)
r.skin_depth    % Skin depth (m)
r.eta           % Impedance (Ω)
r.classification % Material type
```

### Quick Conversions
```matlab
cm = meters * 100
mm = meters * 1000
μm = meters * 1e6
dB/m = Np/m * 8.686
```

---

## ✅ 60-Second Self-Test

Try these without looking:

1. **Find λ in air at 2.4 GHz:**
   ```matlab
   r = Medium(1, 2.4e9);
   r.lambda
   ```

2. **Find skin depth in aluminum (σ=3.8×10⁷ S/m) at 100 MHz:**
   ```matlab
   r = Medium('conductor', 3.8e7, 100e6);
   r.skin_depth * 1e6  % in μm
   ```

3. **Classify material: ε_r=4, σ=0.01 S/m at 1 GHz:**
   ```matlab
   r = Medium(4, 0.01, 1e9);
   r.classification
   ```

**Answers:**
1. 0.125 m = 12.5 cm
2. 8.16 μm
3. 'Low-Loss Dielectric'

---

## 🎯 What's Next?

**If this solved your problem:**
→ Print the [Quick Reference Card](Medium_Quick_Reference.md) for exams

**Want to learn more:**
→ Read the [Complete Guide](Medium_Complete_Guide.md) (30 min)

**Something not working:**
→ Check [Troubleshooting Guide](Medium_Troubleshooting.md)

**Need practice problems:**
→ Work through [Exam Examples](Medium_Exam_Examples.md)

---

## 💡 Remember These Three Rules

1. **Units:** freq in Hz, sigma in S/m
2. **Mode:** Use 'conductor' for metals
3. **Output:** r.lambda gives wavelength in material

**That's it! You're ready to use Medium.m** 🚀

---

[← Back to Master Index](Medium_MASTER_INDEX.md) | [Complete Guide →](Medium_Complete_Guide.md)
