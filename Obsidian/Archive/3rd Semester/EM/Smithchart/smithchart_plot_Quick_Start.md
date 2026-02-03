# smithchart_plot.m - Quick Start Guide

> **2-Minute Crash Course**  
> Visualize impedances on Smith Chart instantly

---

## TL;DR - The One Pattern You Need

```matlab
% Given Z₀ and Z_L
Z0 = 75;
ZL = 15 - 1j*37.5;

smithchart_plot(Z0, ZL);
```

**That's it!** Chart appears with your impedance plotted.

---

## The Two Essential Patterns

### Pattern 1: Plot Impedance (90% of cases)

```matlab
% From impedance values
Z0 = 50;
ZL = 100 + 1j*50;

smithchart_plot(Z0, ZL);

% Console shows:
% === Smith Chart Point ===
%   Z0 = 50.00 Ohm
%   ZL = 100.0000 +50.0000j Ohm
%   zL (normalized) = 2.0000 +1.0000j
%   Gamma = 0.4472 +0.4472j
%   |Gamma| = 0.6325, angle = 45.00 deg
% =========================
%
% [Chart appears]
```

### Pattern 2: From Gamma Directly

```matlab
% If you already have Γ
Gamma = 0.5 * exp(1j*pi/4);

smithchart_plot('Gamma', Gamma);

% Console shows:
% === Smith Chart Point (from Gamma) ===
%   Gamma = 0.3536 +0.3536j
%   |Gamma| = 0.5000, angle = 45.00 deg
%   zL (normalized) = 1.6667 +0.8889j
% ======================================
```

---

## Complete Example (Q10 Type)

### Problem
Plot Z_L = 15 - j37.5 Ω on a 75 Ω Smith chart.

### Solution
```matlab
Z0 = 75;
ZL = 15 - 1j*37.5;

smithchart_plot(Z0, ZL, 'Load');
```

### What You Get

**Console Output:**
```
=== Smith Chart Point ===
  Z0 = 75.00 Ohm
  ZL = 15.0000 -37.5000j Ohm
  zL (normalized) = 0.2000 -0.5000j
  Gamma = -0.5000 -0.5000j
  |Gamma| = 0.7071, angle = -135.00 deg
=========================
```

**Visual:**
- Smith chart appears
- Red circle at your impedance
- Label "Load" next to point
- All grid lines visible

---

## Adding Multiple Points

```matlab
% Plot first point
smithchart_plot(50, 100);
hold on

% Plot second point
smithchart_plot(50, 25 - 1j*25, 'Z_L');
hold on

% Plot third point from Gamma
smithchart_plot('Gamma', 0.3 + 1j*0.4, 'Point');
hold off
```

**Result:** All three points on same chart

---

## What You Get Back

### Console Information
- **Z₀:** Characteristic impedance
- **Z_L:** Load impedance
- **z_L:** Normalized impedance (Z_L/Z₀)
- **Γ:** Reflection coefficient
- **|Γ|:** Magnitude
- **∠Γ:** Angle in degrees

### Visual Chart
- Smith chart grid
- Your point(s) highlighted
- Optional labels
- Key points marked (short, open, matched)

---

## Key Formulas (Automatic)

```
Normalized impedance:
z_L = Z_L / Z₀

Reflection coefficient:
Γ = (z_L - 1) / (z_L + 1)

From Gamma to z:
z_L = (1 + Γ) / (1 - Γ)
```

**You don't calculate these** - smithchart_plot does it automatically!

---

## Common Mistakes

### ❌ Mistake 1: Forgetting Z₀

```matlab
❌ Wrong:
smithchart_plot(100 + 1j*50)  // Missing Z₀

✅ Correct:
smithchart_plot(50, 100 + 1j*50)  // Z₀, Z_L
```

---

### ❌ Mistake 2: Wrong Order

```matlab
❌ Wrong:
smithchart_plot(ZL, Z0)  // Backwards!

✅ Correct:
smithchart_plot(Z0, ZL)  // Z₀ first
```

---

### ❌ Mistake 3: Missing 'Gamma' Keyword

```matlab
❌ Wrong:
smithchart_plot(0.5 + 1j*0.3)  // Thinks it's Z₀

✅ Correct:
smithchart_plot('Gamma', 0.5 + 1j*0.3)
```

---

## Quick Tips

1. **No RF Toolbox?** Works anyway - draws its own chart
2. **Demo mode:** Run `smithchart_plot()` with no arguments
3. **Console is helpful:** Shows all conversions
4. **Labels optional:** Third argument adds label
5. **Hold for multiple:** Use `hold on` between plots

---

## Smith Chart Reading

### Key Locations

```
Center (Γ = 0):        Matched (Z_L = Z₀)
Right edge (Γ = 1):    Open circuit
Left edge (Γ = -1):    Short circuit
Upper half:            Inductive (+jX)
Lower half:            Capacitive (-jX)
```

### What the Circles Mean

- **Horizontal circles:** Constant resistance
- **Vertical arcs:** Constant reactance
- **Outer circle:** |Γ| = 1 (lossless, VSWR = ∞)

---

## ✅ 60-Second Self-Test

**Given:**
```
Z₀ = 50 Ω
Z_L = 75 + j50 Ω
```

**Try plotting (without looking):**
```matlab
smithchart_plot(?, ?)
```

**Answer:**
```matlab
smithchart_plot(50, 75 + 1j*50)
```

**Expected output:** Chart with point in upper right quadrant (inductive, high R)

---

## 🎯 What's Next?

**Ready for exam:**
→ Print the [Quick Reference Card](smithchart_plot_Quick_Reference.md) (1 min)

**Want examples:**
→ Work through [Exam Examples](smithchart_plot_Exam_Examples.md) (8 min)

**Need theory:**
→ Read the [Complete Guide](smithchart_plot_Complete_Guide.md) (15 min)

**Having issues:**
→ Check [Troubleshooting Guide](smithchart_plot_Troubleshooting.md) (2 min)

---

## 💡 Remember

1. **Order:** Z₀ first, then Z_L
2. **Auto-calculates:** z_L and Γ
3. **Console helpful:** Shows all values
4. **Works everywhere:** No RF Toolbox needed
5. **Use labels:** Third argument for clarity

**You're ready to visualize any impedance!** 📊

---

[← Back to Master Index](smithchart_plot_MASTER_INDEX.md) | [Complete Guide →](smithchart_plot_Complete_Guide.md)
