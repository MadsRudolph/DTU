# B_inf_wire.m - Quick Reference Card

> **1-Minute Cheat Sheet**

---

## ⚡ One-Liner

```matlab
B = B_inf_wire(I, r)
% B = magnetic field magnitude [T]
```

---

## 📊 Syntax

```matlab
% Non-magnetic (air/vacuum)
B = B_inf_wire(I, r)

% Magnetic material
B = B_inf_wire(I, r, mu_r)

% Multiple distances
r = [r1, r2, r3];
B = B_inf_wire(I, r);
```

---

## 🔢 Key Formula

```
B = μI / (2πr)

μ₀ = 4π × 10⁻⁷ H/m
μ = μ₀μᵣ  (μᵣ = 1 for air)
```

---

## 📐 Unit Conversions

| Quantity | Conversion | Example |
|----------|-----------|---------|
| mA → A | × 10⁻³ | `I = 500e-3` (500 mA) |
| cm → m | × 10⁻² | `r = 2*1e-2` (2 cm) |
| mm → m | × 10⁻³ | `r = 5*1e-3` (5 mm) |
| T → μT | × 10⁶ | `B*1e6` |
| T → mT | × 10³ | `B*1e3` |
| T → G | × 10⁴ | `B*1e4` |

---

## 🧲 Direction (Right-Hand Rule)

```
Thumb → Current direction (I)
Fingers → B-field circles wire
```

**Function returns magnitude only!**

---

## 📊 Typical Values

```
I = 1 A, r = 1 cm   → B ≈ 20 μT
I = 5 A, r = 2 cm   → B ≈ 50 μT
I = 10 A, r = 5 cm  → B ≈ 40 μT
```

**Earth's field:** ~50 μT

---

## ⚖️ Scaling Laws

```
Distance doubles  → B halves    (B ∝ 1/r)
Current doubles   → B doubles   (B ∝ I)
```

---

## ⚠️ Common Mistakes

```matlab
❌ r = 2            // Forgot cm→m conversion
✅ r = 0.02         // 2 cm = 0.02 m

❌ r = 0            // Zero distance → error
✅ r = 0.001        // Very close but not zero

❌ r = -0.02        // Negative → error
✅ r = 0.02         // Always positive
```

---

## 💡 Pro Tips

1. **Typical range:** 1-100 μT for normal problems
2. **Array input:** Calculate multiple distances at once
3. **μᵣ ≈ 1:** Most materials (air, copper, plastic)
4. **μᵣ >> 1:** Ferromagnetic (iron: ~1000-5000)
5. **Direction:** Right-hand rule (not from function)

---

**Print this for exam!** 📄

[← Master Index](B_inf_wire_MASTER_INDEX.md)
