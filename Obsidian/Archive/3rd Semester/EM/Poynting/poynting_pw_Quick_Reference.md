# poynting_pw.m - Quick Reference Card

> **1-Minute Q22-Q23 Cheat Sheet**

---

## ⚡ The One-Liner

```matlab
% Q22-Q23 Exam Pattern
a = [ax; ay; az];  b = [bx; by; bz];  E0 = value;  beta_vec = [βx; βy; βz];
r = poynting_pw('time', a, b, E0, beta_vec);

% Q22: r.H_phasor (console shows mA/m)
% Q23: r.S_avg (console shows W/m²)
```

---

## 📊 Essential Outputs

| Answer | Field | Units | Where |
|--------|-------|-------|-------|
| **Q22** | `r.H_phasor` | A/m (console: mA/m) | H-field phasor |
| **Q23** | `r.S_avg` | W/m² | Poynting vector |
| Magnitude | `r.S_mag` | W/m² | \|S̄\| |

---

## 🎯 Extraction Guide

### From Problem Statement
```
E = E₀([ax;ay;az]cos(ωt-β·r) + [bx;by;bz]sin(ωt-β·r))
```

### To MATLAB
```matlab
a = [ax; ay; az];      % cos coefficients
b = [bx; by; bz];      % sin coefficients
E0 = value;            % amplitude
beta_vec = [βx; βy; βz];  % beta vector
```

---

## 🔢 Quick Formulas

```
Ẽ = E₀(a - jb)              [Phasor conversion]
k̂ = β/|β|                   [Direction]
H̃ = (1/η)·k̂ × Ẽ            [H-field]
S̄ = ½·Re{Ẽ × H̃*}           [Poynting vector]
```

---

## ⚠️ Common Mistakes

```matlab
❌ E_phasor = E0 * (a + 1j*b)   // Wrong sign!
✅ E_phasor = E0 * (a - 1j*b)   // Correct

❌ a = [ax, ay, az]             // Row vector
✅ a = [ax; ay; az]             // Column vector

❌ poynting_pw(a, b, E0, beta)  // Missing 'time'
✅ poynting_pw('time', a, b, E0, beta)  // Correct
```

---

## 💡 Pro Tips

1. **Console output** already formatted (mA/m, W/m²)
2. **One call** solves both Q22 AND Q23
3. **Default η = 377** for air (don't need to specify)
4. **Minus sign:** Ẽ = E₀(a - jb), not plus
5. **Read console** for formatted answers

---

## ✅ Quick Check

```matlab
% Input vectors must be columns (semicolons!)
a = [2; 1; 0];    ✓
b = [0; -1; -2];  ✓

% Phasor conversion uses minus
Ẽ = E0*(a - 1j*b)  ✓
```

---

**Print this for exam!** 📄

[← Master Index](poynting_pw_MASTER_INDEX.md)
