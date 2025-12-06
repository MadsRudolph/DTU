# smithchart_plot.m - Quick Reference Card

> **1-Minute Cheat Sheet**

---

## ⚡ One-Liner

```matlab
smithchart_plot(Z0, ZL)           % Plot impedance
smithchart_plot(Z0, ZL, 'label')  % With label
smithchart_plot('Gamma', Gamma)   % From Γ directly
```

---

## 📊 Syntax

| Mode | Syntax | Example |
|------|--------|---------|
| **Impedance** | `smithchart_plot(Z0, ZL)` | `smithchart_plot(50, 100+1j*50)` |
| **With label** | `smithchart_plot(Z0, ZL, 'name')` | `smithchart_plot(75, 15-1j*37.5, 'Load')` |
| **From Gamma** | `smithchart_plot('Gamma', Γ)` | `smithchart_plot('Gamma', 0.5*exp(1j*pi/4))` |
| **Multiple** | Use `hold on` between plots | See below |

---

## 🔢 Automatic Calculations

```
z_L = Z_L / Z₀              [Normalize]
Γ = (z_L - 1) / (z_L + 1)  [Reflection coef]
|Γ| = magnitude             [Auto-computed]
∠Γ = angle (degrees)        [Auto-computed]
```

---

## 📍 Key Points on Chart

```
Γ = 0 (center):      Z_L = Z₀ (matched)
Γ = 1 (right):       Open circuit
Γ = -1 (left):       Short circuit
Upper half:          Inductive (+jX)
Lower half:          Capacitive (-jX)
```

---

## ⚠️ Common Mistakes

```matlab
❌ smithchart_plot(ZL, Z0)           // Wrong order
✅ smithchart_plot(Z0, ZL)           // Correct

❌ smithchart_plot(ZL)               // Missing Z₀
✅ smithchart_plot(Z0, ZL)           // Include Z₀

❌ smithchart_plot(Gamma)            // Missing 'Gamma'
✅ smithchart_plot('Gamma', Gamma)   // Use keyword
```

---

## 🎯 Multiple Points

```matlab
smithchart_plot(50, 100);
hold on
smithchart_plot(50, 25-1j*25, 'Z_L');
smithchart_plot('Gamma', 0.3+1j*0.4, 'Γ_in');
hold off
```

---

## 💡 Pro Tips

1. **Console shows all values** - Check for Γ and z_L
2. **No RF Toolbox needed** - Works everywhere
3. **Demo mode:** `smithchart_plot()` (no args)
4. **Labels help:** Use third argument
5. **Hold for comparison** - Multiple points on one chart

---

**Print this for exam!** 📄

[← Master Index](smithchart_plot_MASTER_INDEX.md)
