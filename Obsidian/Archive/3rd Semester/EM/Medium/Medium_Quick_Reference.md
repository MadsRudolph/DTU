# Medium.m - Quick Reference Card

> **2-Minute Lookup Sheet**  
> Essential syntax and patterns for exams and quick reference

---

## ⚡ One-Liners (Copy & Paste)

```matlab
% LOSSLESS (glass, air, plastics)
r = Medium(eps_r, freq);

% LOSSY (tissue, soil, seawater)
r = Medium(eps_r, sigma, freq);

% CONDUCTOR (copper, aluminum, gold)
r = Medium('conductor', sigma, freq);

% FROM LOSS TANGENT
r = Medium('tand', eps_r, tan_delta, freq);

% SKIN DEPTH ONLY
r = Medium('skin', sigma, freq);

% FREE SPACE BASELINE
r = Medium('free', freq);
```

---

## 📊 Essential Output Fields

| What You Need | Field | Units | Example |
|---------------|-------|-------|---------|
| **Wavelength** | `r.lambda` | m | `r.lambda * 100` → cm |
| **Phase velocity** | `r.up` | m/s | `r.up / 3e8` → v/c |
| **Attenuation** | `r.alpha` | Np/m | `r.alpha * 8.686` → dB/m |
| **Phase constant** | `r.beta` | rad/m | `2*pi/r.beta` → λ |
| **Impedance** | `r.eta` | Ω | `abs(r.eta)` → magnitude |
| **Skin depth** | `r.skin_depth` | m | `r.skin_depth * 1e6` → μm |
| **Refractive index** | `r.n` | - | `r.n` |
| **Material type** | `r.classification` | string | See table below |

---

## 🎯 Quick Input Reference

### Lossless Material
```matlab
r = Medium(eps_r, freq)
r = Medium(eps_r, freq, mu_r)  % if magnetic
```
**When:** σ = 0 (no losses)  
**Examples:** Air, glass, PE, PTFE

### Lossy Material
```matlab
r = Medium(eps_r, sigma, freq)
r = Medium(eps_r, sigma, freq, mu_r)
r = Medium(eps_r, sigma, freq, mu_r, 'Name')
```
**When:** 0 < σ < 10⁶ S/m  
**Examples:** Tissue, soil, seawater

### Good Conductor
```matlab
r = Medium('conductor', sigma, freq)
r = Medium('conductor', sigma, freq, mu_r)
```
**When:** σ > 10⁶ S/m (metals)  
**Examples:** Copper, aluminum, gold

### From Loss Tangent
```matlab
r = Medium('tand', eps_r, tan_delta, freq)
```
**When:** Given tan(δ) instead of σ

### Skin Depth Only
```matlab
r = Medium('skin', sigma, freq)
```
**When:** Only need δ, nothing else

### Free Space
```matlab
r = Medium('free', freq)
```
**When:** Need λ₀, η₀, k₀ baselines

---

## 📐 Material Classification

| tan(δ) | Classification | Example |
|--------|----------------|---------|
| < 0.01 | Lossless (approx) | Air, glass |
| < 0.1 | Low-Loss Dielectric | Teflon, FR4 |
| 0.1 - 10 | Quasi-Conductor | Wet soil |
| > 10 | Good Conductor | Metals |

**Quick check:**
```matlab
r = Medium(eps_r, sigma, freq);
fprintf('%s\n', r.classification);
```

---

## 🔢 Common Material Properties

### Dielectrics (Lossless)
```matlab
Air:     eps_r = 1.0
Glass:   eps_r = 4-6
Teflon:  eps_r = 2.1
FR4:     eps_r = 4.4
```

### Conductors
```matlab
Copper:    sigma = 5.8e7 S/m
Aluminum:  sigma = 3.8e7 S/m
Gold:      sigma = 4.1e7 S/m
Silver:    sigma = 6.1e7 S/m
```

### Lossy Materials
```matlab
Seawater:      eps_r = 80,  sigma = 4 S/m
Muscle tissue: eps_r = 50,  sigma = 1.5 S/m  (at 900 MHz)
Dry soil:      eps_r = 3,   sigma = 0.001 S/m
Wet soil:      eps_r = 25,  sigma = 0.1 S/m
```

---

## 🧮 Quick Conversions

### Length
```matlab
cm = r.lambda * 100
mm = r.lambda * 1000
μm = r.skin_depth * 1e6
```

### Attenuation
```matlab
dB/m = r.alpha * 8.686
loss_dB = r.alpha * distance * 8.686
```

### Velocity
```matlab
v_relative = r.up / 3e8        % Fraction of c
wavelength_ratio = r.lambda / r.lambda0
```

### Impedance
```matlab
mag = abs(r.eta)
phase = angle(r.eta) * 180/pi  % degrees
```

---

## 🎓 Exam Quick Patterns

### Pattern 1: Wavelength in Material
```matlab
% Q: "Find λ in glass (ε_r=4) at 10 GHz"
r = Medium(4, 10e9);
lambda_cm = r.lambda * 100;  % Answer in cm
```

### Pattern 2: Skin Depth
```matlab
% Q: "Find δ in copper at 1 GHz"
r = Medium('conductor', 5.8e7, 1e9);
delta_um = r.skin_depth * 1e6;  % Answer in μm
```

### Pattern 3: Attenuation Over Distance
```matlab
% Q: "Loss in 10 cm of tissue?"
r = Medium(50, 1.5, 900e6);
loss_dB = r.alpha * 0.1 * 8.686;  % 10 cm = 0.1 m
```

### Pattern 4: Phase Velocity
```matlab
% Q: "Phase velocity in material?"
r = Medium(eps_r, freq);
v_p = r.up;  % m/s
```

### Pattern 5: Material Classification
```matlab
% Q: "Is this a conductor or dielectric?"
r = Medium(eps_r, sigma, freq);
type = r.classification;
```

---

## ⚠️ Common Mistakes (AVOID!)

### ❌ Wrong Units
```matlab
❌ Medium(4, 10)           // freq in MHz? NO!
✅ Medium(4, 10e6)         // freq in Hz

❌ Medium(1, 5800, 1e9)    // sigma in kS/m? NO!
✅ Medium(1, 5.8e7, 1e9)   // sigma in S/m
```

### ❌ Wrong Mode
```matlab
❌ Medium(1, 5.8e7, 1e9)            // copper as lossy
✅ Medium('conductor', 5.8e7, 1e9)  // use conductor mode

❌ Medium('conductor', 4, 10e9)     // glass as conductor
✅ Medium(4, 10e9)                  // use lossless mode
```

### ❌ Missing Arguments
```matlab
❌ Medium(80, 1e6)          // forgot sigma for seawater
✅ Medium(80, 4, 1e6)       // include all three

❌ Medium(4)                // forgot frequency
✅ Medium(4, 10e9)          // include frequency
```

### ❌ Wrong Field Name
```matlab
❌ r.wavelength             // doesn't exist
✅ r.lambda                 // correct

❌ r.phase_velocity         // doesn't exist
✅ r.up                     // correct
```

---

## 🧪 Quick Tests

### Test 1: Basic Wavelength
```matlab
r = Medium(1, 3e8);  % Air at 300 MHz
r.lambda             % Should be 1.0 m
```

### Test 2: Skin Depth
```matlab
r = Medium('conductor', 5.8e7, 1e9);  % Copper at 1 GHz
r.skin_depth * 1e6   % Should be ~2.1 μm
```

### Test 3: Classification
```matlab
r = Medium(4, 0.001, 1e9);  % Low-loss material
r.classification     % Should be 'Low-Loss Dielectric'
```

---

## 📋 Pre-Exam Checklist

- [ ] Know lossless pattern: `r = Medium(eps_r, freq)`
- [ ] Know conductor pattern: `r = Medium('conductor', sigma, freq)`
- [ ] Remember units: freq in Hz, sigma in S/m
- [ ] Know output fields: `r.lambda`, `r.skin_depth`, etc.
- [ ] Can convert: m → cm, Np/m → dB/m
- [ ] Understand `r.classification` output

---

## 💡 Pro Tips for Exams

1. **Check classification** - Tells you if you used right mode
2. **Use 'conductor' mode** - For any metal (σ > 10⁶)
3. **Convert units early** - Get λ in cm: `r.lambda * 100`
4. **Free space baseline** - Compare with `Medium('free', freq)`
5. **Loss in dB** - Multiply `r.alpha * 8.686` for dB/m

---

## 🔗 Need More?

**Quick problems:** [Quick Start Guide](Medium_Quick_Start.md) (5 min)  
**Deep dive:** [Complete Guide](Medium_Complete_Guide.md) (30 min)  
**Real exams:** [Exam Examples](Medium_Exam_Examples.md) (15 min)  
**Problems:** [Troubleshooting](Medium_Troubleshooting.md) (5 min)  
**Navigation:** [Master Index](Medium_MASTER_INDEX.md)

---

**Print this page for exams!** 📄

[← Master Index](Medium_MASTER_INDEX.md)
