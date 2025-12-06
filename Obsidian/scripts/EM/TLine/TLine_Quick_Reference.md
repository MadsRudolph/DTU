# TLine.m - Quick Reference Card

> **2-Minute Lookup Sheet**  
> Essential syntax and patterns for exams and quick reference

---

## ⚡ One-Liners (Copy & Paste)

```matlab
% BASIC ANALYSIS (most common)
r = TLine(Z0, ZL, len_lambda);

% Q13/Q14: FIND LOAD FROM INPUT
r = TLine('load', Z0, Gamma_A, len_lambda);

% Q11: TL + SERIES ELEMENT
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp);
r = TLine('series_L', Z0, ZL, len_m, L, freq, vp);

% Q11: TL + SHUNT ELEMENT
r = TLine('shunt_C', Z0, ZL, len_m, C, freq, vp);
r = TLine('shunt_L', Z0, ZL, len_m, L, freq, vp);

% Q12: STUB DESIGN
r = TLine('stub', Z_target, Z0, 'short');
r = TLine('stub', Z_target, Z0, 'open');

% QUARTER-WAVE TRANSFORMER
r = TLine('QW', Z_source, Z_load);

% GAMMA ↔ Z CONVERSION
r = TLine('Gamma', Z0, Z);
r = TLine('Z', Z0, Gamma);

% PROPAGATE GAMMA
r = TLine('Gamma_in', Gamma_L, len_lambda);   % L → Input
r = TLine('Gamma_L', Gamma_in, len_lambda);   % Input → L
```

---

## 📊 Essential Output Fields

| What You Need | Field | Example |
|---------------|-------|---------|
| **Input impedance** | `r.Z_in` or `r.Z_A` | `r.Z_in` |
| **Load impedance** | `r.ZL` or `r.Z_L` | `r.Z_L` |
| **Load Gamma** | `r.Gamma_L` | Q13 answer |
| **Input Gamma** | `r.Gamma_in` | Given in problem |
| **VSWR** | `r.VSWR` | `r.VSWR` |
| **TL impedance** | `r.Z_TL` | Before element |
| **Element impedance** | `r.Z_element` | C or L |
| **Stub length** | `r.short.len_lambda` | Q12 answer |
| **QW impedance** | `r.Z_qw` | Transformer Z₀ |

---

## 🎯 Exam Quick Patterns

### Q13: Find Gamma_L
```matlab
% Given: Gamma_A, Z0, length
r = TLine('load', Z0, Gamma_A, len_lambda);
answer = r.Gamma_L;  % Magnitude and angle
```

### Q14: Find Z_L  
```matlab
% Same call as Q13!
r = TLine('load', Z0, Gamma_A, len_lambda);
answer = r.Z_L;  % Real and imaginary parts
```

### Q11: Find Z_A with element
```matlab
% Series capacitor
c0 = 3e8;
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp);
answer = r.Z_A;

% Series inductor
r = TLine('series_L', Z0, ZL, len_m, L, freq, vp);
answer = r.Z_A;
```

### Q12: Stub length
```matlab
% Realize Z = jX with short stub
r = TLine('stub', 1j*X, Z0, 'short');
answer = r.short.len_lambda;  % In wavelengths
```

### Basic: Find Z_in
```matlab
r = TLine(Z0, ZL, len_lambda);
answer = r.Z_in;
```

### Basic: Find VSWR
```matlab
r = TLine(Z0, ZL, len_lambda);
answer = r.VSWR;
```

---

## 📐 Special Cases

### Quarter-Wave Line (λ/4)
```matlab
% Z_in = Z₀²/Z_L
r = TLine(50, 100, 0.25);
r.Z_in  % = 25 Ω
```

### Half-Wave Line (λ/2)
```matlab
% Z_in = Z_L (transparent)
r = TLine(50, 100, 0.5);
r.Z_in  % = 100 Ω
```

### Matched Line (Z_L = Z0)
```matlab
r = TLine(50, 50, 0.3);
r.Gamma_L  % = 0
r.VSWR     % = 1
```

### Short Circuit (Z_L = 0)
```matlab
r = TLine(50, 0, 0.25);
r.Z_in  % = ∞ (open at λ/4)
```

### Open Circuit (Z_L = ∞)
```matlab
r = TLine(50, 1e10, 0.25);
r.Z_in  % ≈ 0 (short at λ/4)
```

---

## 🔢 Quick Formulas

### Reflection Coefficient
```
Γ = (Z_L - Z0)/(Z_L + Z0)
Z = Z0(1 + Γ)/(1 - Γ)
```

### VSWR
```
VSWR = (1 + |Γ|)/(1 - |Γ|)
```

### Input Impedance
```
Z_in = Z0(Z_L + jZ0·tan(βℓ))/(Z0 + jZ_L·tan(βℓ))
```

### Quarter-Wave
```
Z_QW = √(Z_source × Z_load)
```

### Stub (Short)
```
Z_in = jZ0·tan(βℓ)
```

---

## ⚠️ Common Mistakes (AVOID!)

### ❌ Wrong Length Units
```matlab
❌ TLine(50, 100, 0.5)        // Thought 0.5m, actually 0.5λ
✅ TLine(50, 100, 0.5)        // 0.5 wavelengths
✅ TLine(50, 100, 0.5, f, vp) // 0.5 meters with freq/vp
```

### ❌ Wrong Mode for Q13/Q14
```matlab
❌ Two separate calls
✅ TLine('load', Z0, Gamma_A, len)  // Solves both!
```

### ❌ Wrong Field Access
```matlab
❌ r.Z                        // Doesn't exist
✅ r.Z_in   or   r.Z_A        // Correct

❌ r.len                      // Doesn't exist  
✅ r.short.len_lambda         // Stub length
```

### ❌ Missing vp for Physical Length
```matlab
❌ TLine('series_C', Z0, ZL, 0.017, C, freq)  // Missing vp
✅ TLine('series_C', Z0, ZL, 0.017, C, freq, 0.79*c0)
```

---

## 📋 Pre-Exam Checklist

- [ ] Know basic pattern: `TLine(Z0, ZL, len_lambda)`
- [ ] Know Q13/Q14 shortcut: `TLine('load', ...)`
- [ ] Know Q11 pattern: `TLine('series_C', ...)` or `'series_L'`
- [ ] Know Q12 pattern: `TLine('stub', Z_target, Z0, 'short')`
- [ ] Remember length units (λ vs meters)
- [ ] Know output fields: `r.Z_in`, `r.Gamma_L`, `r.Z_A`
- [ ] Know stub access: `r.short.len_lambda`

---

## 💡 Pro Tips for Exams

1. **Q13/Q14 together:** One `TLine('load', ...)` call
2. **Check units:** Length in λ unless with freq/vp
3. **Use Z_A = Z_in:** They're the same (aliases)
4. **QW shortcut:** `√(Z₁×Z₂)` for quick mental check
5. **Stub → reactance only:** Can't realize real impedance
6. **VSWR ≥ 1 always:** If < 1, something's wrong

---

## 🧪 Quick Tests

### Test 1: Basic λ/4
```matlab
TLine(50, 200, 0.25).Z_in  % Should be 12.5 Ω
```

### Test 2: λ/2
```matlab
TLine(50, 200, 0.5).Z_in   % Should be 200 Ω
```

### Test 3: Matched
```matlab
TLine(50, 50, 0.3).VSWR    % Should be 1.0
```

### Test 4: Q13/Q14
```matlab
r = TLine('load', 75, 0.5*exp(1j*pi/3), 0.3);
r.Gamma_L  % Should have |Γ| = 0.5
r.Z_L      % Should be complex
```

---

## 🔗 Need More?

**Quick problems:** [Quick Start Guide](TLine_Quick_Start.md) (5 min)  
**Deep dive:** [Complete Guide](TLine_Complete_Guide.md) (45 min)  
**Real exams:** [Exam Examples](TLine_Exam_Examples.md) (20 min)  
**Problems:** [Troubleshooting](TLine_Troubleshooting.md) (5 min)  
**Navigation:** [Master Index](TLine_MASTER_INDEX.md)

---

**Print this page for exams!** 📄

[← Master Index](TLine_MASTER_INDEX.md)
