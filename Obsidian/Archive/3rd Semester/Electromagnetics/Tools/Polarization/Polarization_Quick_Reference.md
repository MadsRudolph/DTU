# Polarization.m - Quick Reference Card

> **2-Minute Exam Lookup Sheet**

---

## ⚡ One-Liners

```matlab
% COMPLEX PHASOR (most common)
r = Polarization([Ex; Ey; Ez]);
r = Polarization([Ex; Ey; Ez], k_hat);

% AMPLITUDE/PHASE
r = Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg);

% TIME-DOMAIN
r = Polarization(a, b, beta);
```

---

## 📊 Essential Outputs

| What You Need | Field | Example |
|---------------|-------|---------|
| **Type** | `r.type` | 'Circular', 'Linear', 'Elliptical' |
| **Handedness** | `r.handedness` | 'RHCP', 'LHCP', 'N/A' |
| **Axial ratio** | `r.AR` | 1 (circular), ∞ (linear) |
| **AR in dB** | `r.AR_dB` | 0 (circular), ∞ (linear) |
| **Major axis** | `r.major` | Semi-axis length |
| **Minor axis** | `r.minor` | Semi-axis length |
| **Tilt angle** | `r.tilt_deg` | Degrees |

---

## 🎯 Quick Recognition

### RHCP vs LHCP (+z propagation)
```matlab
[1; -1j; 0]  → RHCP  (minus j)
[1; +1j; 0]  → LHCP  (plus j)
```

**Memory:** RHCP = **R**ight = **-**j

### Polarization Types
```matlab
AR = 1     → Circular
AR = ∞     → Linear
1 < AR < ∞ → Elliptical
```

### Common Patterns
```matlab
% RHCP
[1; -1j; 0]      % Standard
[E0; -E0*j; 0]   % Scaled

% LHCP
[1; 1j; 0]       % Standard
[E0; E0*j; 0]    % Scaled

% Linear
[1; 0; 0]        % x-polarized
[0; 1; 0]        % y-polarized
[1; 1; 0]        % 45° diagonal
[1; 2; 0]        % Any real ratio

% Elliptical
[2; -1j; 0]      % RHCP elliptical
[1; -0.5j; 0]    % RHCP elliptical
```

---

## 🧪 Quick Tests

```matlab
% Test 1: RHCP
Polarization([1; -1j; 0])
% Should be: Circular, RHCP, AR=1

% Test 2: LHCP
Polarization([1; 1j; 0])
% Should be: Circular, LHCP, AR=1

% Test 3: Linear
Polarization([1; 1; 0])
% Should be: Linear, N/A, AR=∞

% Test 4: Elliptical
Polarization([2; -1j; 0])
% Should be: Elliptical, RHCP, AR≈2.4
```

---

## 📐 Quick Formulas

### Phasor to Type
```
If Re(F) × Im(F) = 0 → Linear
If |Re(F)| = |Im(F)| and Re(F) ⊥ Im(F) → Circular
Otherwise → Elliptical
```

### Handedness (IEEE convention)
```
hand = k̂ · (Re(F) × Im(F))
hand > 0 → RHCP
hand < 0 → LHCP
```

### Axial Ratio
```
AR = major_axis / minor_axis
AR_dB = 20·log₁₀(AR)
```

---

## ⚠️ Common Mistakes

### ❌ Wrong Vector Type
```matlab
❌ [1, -1j, 0]     % Row vector (commas)
✅ [1; -1j; 0]     % Column vector (semicolons)
```

### ❌ Wrong RHCP Sign
```matlab
❌ [1; 1j; 0]      % This is LHCP, not RHCP!
✅ [1; -1j; 0]     % RHCP in +z
```

### ❌ Missing 'ap' Keyword
```matlab
❌ Polarization(10, 5, 0, 90)
✅ Polarization('ap', 10, 5, 0, 90)
```

---

## 📋 Pre-Exam Checklist

- [ ] Know syntax: `Polarization([Ex; Ey; Ez])`
- [ ] Remember: RHCP = `[1; -1j; 0]` in +z
- [ ] Remember: LHCP = `[1; 1j; 0]` in +z
- [ ] Know: AR=1 → circular, AR=∞ → linear
- [ ] Can identify type from phasor
- [ ] Can identify handedness
- [ ] Know output fields

---

## 💡 Pro Tips

1. **Default direction:** +z if not specified
2. **RHCP shortcut:** Look for `-j` in +z
3. **Linear test:** All real or all imaginary
4. **Circular test:** Equal magnitudes + 90° phase
5. **Verify:** Use `r.AR` - should be 1 or ∞ for pure types

---

## 🔗 Need More?

**Quick start:** [Quick Start Guide](Polarization_Quick_Start.md) (5 min)  
**Deep dive:** [Complete Guide](Polarization_Complete_Guide.md) (30 min)  
**Examples:** [Exam Examples](Polarization_Exam_Examples.md) (15 min)  
**Problems:** [Troubleshooting](Polarization_Troubleshooting.md) (5 min)  
**Navigation:** [Master Index](Polarization_MASTER_INDEX.md)

---

**Print this page for exams!** 📄

[← Master Index](Polarization_MASTER_INDEX.md)
