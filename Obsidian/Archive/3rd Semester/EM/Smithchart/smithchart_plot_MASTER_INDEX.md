# smithchart_plot.m - Master Documentation Index

> **Central hub for all smithchart_plot.m documentation**  
> Visualize impedances on the Smith Chart

---

## 📚 Complete Documentation Suite

| Document | Purpose | Time | When to Use |
|----------|---------|------|-------------|
| [**Quick Start**](smithchart_plot_Quick_Start.md) | Get started NOW | 2 min | First time using smithchart_plot |
| [**Complete Guide**](smithchart_plot_Complete_Guide.md) | Master everything | 15 min | Deep learning & reference |
| [**Quick Reference**](smithchart_plot_Quick_Reference.md) | Exam cheat sheet | 1 min | During exams/quick lookup |
| [**Troubleshooting**](smithchart_plot_Troubleshooting.md) | Fix problems | 2 min | When something's wrong |
| [**Exam Examples**](smithchart_plot_Exam_Examples.md) | Real problems | 8 min | Practice & preparation |

---

## 🎯 Quick Navigation

### By Your Situation

**"I've never used smithchart_plot before"**
→ Start with [Quick Start Guide](smithchart_plot_Quick_Start.md) (2 min)

**"I need to visualize an impedance NOW"**
→ Use [Quick Reference Card](smithchart_plot_Quick_Reference.md) (1 min)

**"Something's not working"**
→ Check [Troubleshooting Guide](smithchart_plot_Troubleshooting.md) (2 min)

**"I want to understand this completely"**
→ Read [Complete Guide](smithchart_plot_Complete_Guide.md) (15 min)

**"Show me examples"**
→ See [Exam Examples](smithchart_plot_Exam_Examples.md) (8 min)

---

## 🚀 Recommended Learning Paths

### Path 1: "Exam Tomorrow" (10 minutes)
1. [Quick Start](smithchart_plot_Quick_Start.md) - 2 min
2. [Exam Examples](smithchart_plot_Exam_Examples.md) - 8 min

**Result:** Can visualize any impedance

---

### Path 2: "Master This Tool" (30 minutes)
1. [Quick Start](smithchart_plot_Quick_Start.md) - 2 min
2. [Complete Guide](smithchart_plot_Complete_Guide.md) - 15 min
3. [Exam Examples](smithchart_plot_Exam_Examples.md) - 8 min
4. [Troubleshooting](smithchart_plot_Troubleshooting.md) - 2 min
5. Practice - 3 min

**Result:** Complete mastery of Smith Chart plotting

---

### Path 3: "Quick Visualization" (2 minutes)
1. [Quick Start](smithchart_plot_Quick_Start.md) - 2 min
2. Plot your impedance

**Result:** Chart created

---

### Path 4: "Debugging" (2-5 minutes)
1. [Troubleshooting Guide](smithchart_plot_Troubleshooting.md) - 2 min
2. Check [Complete Guide](smithchart_plot_Complete_Guide.md) if needed - 3 min

**Result:** Error fixed

---

## 📋 What smithchart_plot.m Does

**smithchart_plot** is a **visualization tool** - it plots impedances on the Smith Chart for easy analysis.

### Core Capabilities
✅ **Plot impedance** - From Z₀ and Z_L
✅ **Plot Gamma** - Directly from reflection coefficient
✅ **Calculate conversions** - Auto-computes z_L and Γ
✅ **Multiple points** - Use hold on for comparisons
✅ **Works everywhere** - Built-in or manual Smith chart

### Two Input Modes

**Mode 1: Impedance** (Most Common)
```matlab
smithchart_plot(Z0, ZL)
smithchart_plot(Z0, ZL, 'label')
```

**Mode 2: Gamma Directly**
```matlab
smithchart_plot('Gamma', Gamma)
smithchart_plot('Gamma', Gamma, 'label')
```

---

## 🎓 Exam Use (Q10 Type)

### What They Ask

**Q10 Example:** "Plot the load impedance Z_L = 15 - j37.5 Ω on a 75 Ω Smith chart"

### The One-Liner Solution

```matlab
smithchart_plot(75, 15 - 1j*37.5)
```

**Total time:** 10 seconds

---

## ⚡ The Core Pattern

### Pattern 1: Single Point (90% of cases)

```matlab
% Given Z₀ and Z_L
Z0 = 75;
ZL = 15 - 1j*37.5;

smithchart_plot(Z0, ZL);
% Chart appears with point plotted
```

### Pattern 2: Multiple Points

```matlab
smithchart_plot(50, 100);
hold on
smithchart_plot(50, 25-1j*25, 'Z_L');
hold off
```

### Pattern 3: From Gamma

```matlab
Gamma = 0.5*exp(1j*pi/4);
smithchart_plot('Gamma', Gamma);
```

---

## 🔍 Quick Decision Tree

```
What do you have?

├─ Impedance Z_L and Z₀?
│  └─ smithchart_plot(Z0, ZL)

├─ Reflection coefficient Γ?
│  └─ smithchart_plot('Gamma', Gamma)

└─ Multiple points to compare?
   └─ Use hold on between plots
```

---

## 📊 What Gets Plotted

### Automatic Calculations

From your inputs, smithchart_plot computes and displays:
- **Normalized impedance:** z_L = Z_L/Z₀
- **Reflection coefficient:** Γ = (z_L - 1)/(z_L + 1)
- **Magnitude:** |Γ|
- **Angle:** ∠Γ (degrees)

### Visual Elements
- Red circle marker at impedance location
- Optional label
- Grid lines (resistance & reactance circles)
- Key points marked (short, open, matched)

---

## 💡 Pro Tips

1. **No RF Toolbox needed** - Creates its own Smith chart if needed
2. **Auto-normalizes** - Just give Z₀ and Z_L
3. **Console output** - Shows all conversions
4. **Multiple plots** - Use hold on for comparison
5. **Demo mode** - Run with no arguments to see example
6. **Verify calculations** - Check console for Γ values

---

## ✅ Pre-Exam Checklist

- [ ] Know basic syntax: `smithchart_plot(Z0, ZL)`
- [ ] Can add labels: `smithchart_plot(Z0, ZL, 'name')`
- [ ] Understand console shows Γ and z_L
- [ ] Know how to plot multiple points (hold on)
- [ ] Remember: Works with or without RF Toolbox
- [ ] Can plot from Gamma: `smithchart_plot('Gamma', Gamma)`

---

## 📖 Document Descriptions

### [Quick Start Guide](smithchart_plot_Quick_Start.md)
**What:** 2-minute crash course  
**When:** First time or quick visualization  
**Contains:** Two essential patterns, examples

### [Complete Guide](smithchart_plot_Complete_Guide.md)
**What:** Comprehensive 15-minute reference  
**When:** Deep learning or all features  
**Contains:** Both modes, theory, customization

### [Quick Reference Card](smithchart_plot_Quick_Reference.md)
**What:** 1-minute lookup sheet  
**When:** During exams  
**Contains:** One-liners, syntax, formulas

### [Troubleshooting Guide](smithchart_plot_Troubleshooting.md)
**What:** Error diagnosis  
**When:** Results seem wrong  
**Contains:** Common errors, fixes

### [Exam Examples](smithchart_plot_Exam_Examples.md)
**What:** Real plotting examples  
**When:** Practice  
**Contains:** Q10 type problems with solutions

---

## 🔗 Related Documentation

- [TLine](TLine_MASTER_INDEX.md) - Often used together for transmission line analysis
- [StubMatch](StubMatch_MASTER_INDEX.md) - Stub matching visualization
- [Helpers](Helpers.md) - All EM MATLAB tools

---

## 📝 Quick Example

```matlab
% Q10 type problem
Z0 = 75;
ZL = 15 - 1j*37.5;

smithchart_plot(Z0, ZL, 'Load');

% Console output:
% === Smith Chart Point ===
%   Z0 = 75.00 Ohm
%   ZL = 15.0000 -37.5000j Ohm
%   zL (normalized) = 0.2000 -0.5000j
%   Gamma = -0.5000 -0.5000j
%   |Gamma| = 0.7071, angle = -135.00 deg
% =========================
%
% [Chart appears with point plotted]
```

---

## 🎯 Key Features

### Automatic Mode Selection
- **Has RF Toolbox?** → Uses MATLAB's smithplot
- **No RF Toolbox?** → Draws custom Smith chart
- **Works either way!**

### Console Information
Always shows:
- Input impedance (Z_L)
- Normalized impedance (z_L)
- Reflection coefficient (Γ)
- Magnitude and angle

### Visualization
- Resistance circles (constant R)
- Reactance arcs (constant X)
- Unit circle (|Γ| = 1)
- Key points labeled
- Your point highlighted

---

## 📐 Smith Chart Basics

### Key Points
- **Center (Γ = 0):** Matched load (Z_L = Z₀)
- **Right edge (Γ = 1):** Open circuit
- **Left edge (Γ = -1):** Short circuit
- **Upper half:** Inductive (positive reactance)
- **Lower half:** Capacitive (negative reactance)

### Constant Circles
- **Horizontal circles:** Constant resistance
- **Vertical arcs:** Constant reactance
- **Complete circle:** |Γ| = 1 (lossless)

---

**Last Updated:** 2025-12-06  
**Version:** 1.0  
**Modes Covered:** 2 (complete)  
**Use Case:** Visualization & verification
