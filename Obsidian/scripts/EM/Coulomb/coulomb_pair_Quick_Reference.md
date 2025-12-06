# coulomb_pair.m - Quick Reference Card

> **1-Minute Cheat Sheet**

---

## ⚡ One-Liner

```matlab
[F12, F21] = coulomb_pair(q1, q2, r1, r2)
% F12 = force ON q1 DUE TO q2
% F21 = force ON q2 DUE TO q1
```

---

## 📊 Syntax

```matlab
% Charges in Coulombs [C]
q1 = 2e-6;         % 2 μC
q2 = -3e-6;        % -3 μC

% Positions in meters [m] (column vectors!)
r1 = [x1; y1; z1];
r2 = [x2; y2; z2];

% Calculate
[F12, F21] = coulomb_pair(q1, q2, r1, r2);
```

---

## 🔢 Key Formula

```
|F| = k_e · |q₁q₂| / r²

k_e = 8.99 × 10⁹ N·m²/C²
```

---

## 📐 Unit Conversions

| Prefix | Factor | Example |
|--------|--------|---------|
| μC (micro) | 10⁻⁶ | `q = 5e-6` |
| nC (nano) | 10⁻⁹ | `q = 10e-9` |
| pC (pico) | 10⁻¹² | `q = 100e-12` |
| cm | 10⁻² | `r = [10;0;0]*1e-2` |
| mm | 10⁻³ | `r = [5;0;0]*1e-3` |

---

## ⚖️ Newton's Third Law

```
F₂₁ = -F₁₂  (always!)

Verify: norm(F12 + F21) should be ≈ 0
```

---

## 🧲 Force Direction

```
Same sign (++ or --):    Repel (push apart)
Opposite sign (+−):      Attract (pull together)
```

---

## ⚠️ Common Mistakes

```matlab
❌ r1 = [1, 0, 0]       // Row vector (commas)
✅ r1 = [1; 0; 0]       // Column vector (semicolons)

❌ q = 5                // Forgot unit conversion
✅ q = 5e-6             // 5 μC in Coulombs

❌ r1 = r2              // Same position → error
✅ r1 ≠ r2              // Different positions
```

---

## 💡 Pro Tips

1. **Always use column vectors** (semicolons)
2. **Check signs:** Same → repel, opposite → attract
3. **Verify:** F12 + F21 ≈ 0
4. **Multiple charges:** Sum forces (superposition)
5. **Units:** C for charge, m for distance, N for force

---

**Print this for exam!** 📄

[← Master Index](coulomb_pair_MASTER_INDEX.md)
