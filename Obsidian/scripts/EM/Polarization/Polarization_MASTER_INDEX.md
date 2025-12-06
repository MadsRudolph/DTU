# Polarization.m - Master Documentation Index

> **Central hub for all Polarization.m documentation**  
> Complete polarization analysis - RHCP, LHCP, linear, elliptical

---

## 📚 Complete Documentation Suite

| Document | Purpose | Time | When to Use |
|----------|---------|------|-------------|
| [**Quick Start**](Polarization_Quick_Start.md) | Get started NOW | 5 min | First time using Polarization |
| [**Complete Guide**](Polarization_Complete_Guide.md) | Master everything | 30 min | Deep learning & reference |
| [**Quick Reference**](Polarization_Quick_Reference.md) | Exam cheat sheet | 2 min | During exams/quick lookup |
| [**Troubleshooting**](Polarization_Troubleshooting.md) | Fix problems | 5 min | When something's wrong |
| [**Exam Examples**](Polarization_Exam_Examples.md) | Real problems | 15 min | Practice & preparation |

---

## 🎯 Quick Navigation

### By Your Situation

**"I've never used Polarization before"**
→ Start with [Quick Start Guide](Polarization_Quick_Start.md) (5 min)

**"I need to solve this problem NOW"**
→ Use [Quick Reference Card](Polarization_Quick_Reference.md) (2 min)

**"Something's not working"**
→ Check [Troubleshooting Guide](Polarization_Troubleshooting.md) (5 min)

**"I want to master this completely"**
→ Read [Complete Guide](Polarization_Complete_Guide.md) (30 min)

**"Show me real exam problems"**
→ See [Exam Examples](Polarization_Exam_Examples.md) (15 min)

---

## 🚀 Recommended Learning Paths

### Path 1: "Exam Tomorrow" (20 minutes)
1. [Quick Start](Polarization_Quick_Start.md) - 5 min
2. [Exam Examples](Polarization_Exam_Examples.md) - 10 min  
3. [Quick Reference](Polarization_Quick_Reference.md) - 2 min
4. Practice - 3 min

**Result:** Ready for most polarization problems

---

### Path 2: "Master This Tool" (1 hour)
1. [Quick Start](Polarization_Quick_Start.md) - 5 min
2. [Complete Guide](Polarization_Complete_Guide.md) - 30 min
3. [Exam Examples](Polarization_Exam_Examples.md) - 15 min
4. [Troubleshooting](Polarization_Troubleshooting.md) - 5 min
5. Practice - 5 min

**Result:** Complete mastery of polarization analysis

---

### Path 3: "Quick Problem Solving" (7 minutes)
1. [Quick Start](Polarization_Quick_Start.md) - 5 min
2. Solve your problem - 2 min

**Result:** Problem solved

---

### Path 4: "Debugging" (5-15 minutes)
1. [Troubleshooting Guide](Polarization_Troubleshooting.md) - 5 min
2. Check [Complete Guide](Polarization_Complete_Guide.md) if needed - 10 min

**Result:** Error fixed

---

## 📋 What Polarization.m Does

**Polarization.m** analyzes electromagnetic wave polarization with **3 input modes:**

### Core Capabilities
✅ **Detect polarization type** - Linear, Circular, or Elliptical
✅ **Determine handedness** - RHCP, LHCP, or N/A
✅ **Calculate axial ratio** - AR and AR_dB
✅ **Find semi-axes** - Major and minor axes
✅ **Get tilt angle** - Ellipse orientation

### Three Input Modes

**Mode 1: Complex Phasor** (Most Common)
```matlab
Polarization([1; -1j; 0])  % RHCP wave
```

**Mode 2: Amplitude/Phase**
```matlab
Polarization('ap', Ex, Ey, phi_x, phi_y)  % Given magnitudes and phases
```

**Mode 3: Time-Domain**
```matlab
Polarization(u, v, beta)  % u·cos + v·sin form
```

---

## 🎓 Common Exam Problem Types

| Problem Type | Example | Solution Time |
|--------------|---------|---------------|
| **Identify type** | "Is this RHCP or LHCP?" | 30 sec |
| **Axial ratio** | "Calculate AR in dB" | 30 sec |
| **From amplitude/phase** | "Given Ex=10, Ey=5, φx=0°, φy=90°" | 1 min |
| **Linear or elliptical?** | "Determine polarization type" | 30 sec |
| **Handedness** | "Right or left circular?" | 30 sec |

---

## ⚡ The Three Core Patterns

### Pattern 1: Complex Phasor (90% of problems)
```matlab
% Given: E = x̂(1) + ŷ(-j)
F = [1; -1j; 0];
r = Polarization(F);
% Get: r.type, r.handedness, r.AR
```

### Pattern 2: Amplitude/Phase
```matlab
% Given: |Ex|=10, |Ey|=5, φx=0°, φy=90°
r = Polarization('ap', 10, 5, 0, 90);
% Get: r.type, r.handedness, r.AR
```

### Pattern 3: Time-Domain
```matlab
% Given: E = a·cos(ψ) + b·sin(ψ)
r = Polarization(a, b, beta);
% Get: r.type, r.handedness
```

---

## 🔍 Quick Decision Tree

```
What form is your E-field?

├─ Complex phasor (E = Ex·x̂ + Ey·ŷ)?
│  └─ Polarization([Ex; Ey; 0])

├─ Amplitude and phase (|Ex|, |Ey|, φx, φy)?
│  └─ Polarization('ap', Ex, Ey, phi_x, phi_y)

└─ Time-domain (a·cos + b·sin)?
   └─ Polarization(a, b, beta)
```

---

## 📊 Quick Recognition Guide

### RHCP (Right-Hand Circular)
- E rotates **clockwise** looking along propagation
- Phasor: `[1; -1j; 0]` for +z propagation
- AR = 1 (0 dB)

### LHCP (Left-Hand Circular)  
- E rotates **counter-clockwise** looking along propagation
- Phasor: `[1; 1j; 0]` for +z propagation
- AR = 1 (0 dB)

### Linear
- E oscillates along a line
- Phasor: Real and imaginary parts parallel
- AR = ∞ (Inf dB)
- Examples: `[1; 1; 0]`, `[1; 0; 0]`

### Elliptical
- E traces an ellipse
- Between linear and circular
- 1 < AR < ∞

---

## 📖 Document Descriptions

### [Quick Start Guide](Polarization_Quick_Start.md)
**What:** 5-minute crash course  
**When:** First time or quick refresher  
**Contains:** 3 essential patterns, recognition guide, mistakes

### [Complete Guide](Polarization_Complete_Guide.md)
**What:** Comprehensive 30-minute reference  
**When:** Deep learning or detailed questions  
**Contains:** All 3 modes, theory, formulas, advanced topics

### [Quick Reference Card](Polarization_Quick_Reference.md)
**What:** 2-minute lookup sheet  
**When:** During exams or quick syntax check  
**Contains:** One-liners, recognition patterns, quick tests

### [Troubleshooting Guide](Polarization_Troubleshooting.md)
**What:** Error diagnosis and solutions  
**When:** Something's not working  
**Contains:** Common errors, fixes, diagnostic tools

### [Exam Examples](Polarization_Exam_Examples.md)
**What:** Real exam-style problems  
**When:** Practice or learning patterns  
**Contains:** Complete solutions, strategies

---

## 💡 Pro Tips

1. **Most common:** Complex phasor mode - `Polarization([Ex; Ey; Ez])`
2. **RHCP vs LHCP:** Sign of imaginary part in +z propagation
3. **Check AR:** 1 = circular, ∞ = linear, between = elliptical
4. **Default direction:** +z if not specified
5. **Quick test:** `[1; -1j; 0]` is always RHCP in +z

---

## ✅ Pre-Exam Checklist

- [ ] Know complex phasor syntax: `Polarization([Ex; Ey; Ez])`
- [ ] Remember RHCP: `[1; -1j; 0]` in +z
- [ ] Remember LHCP: `[1; 1j; 0]` in +z
- [ ] Know output fields: `r.type`, `r.handedness`, `r.AR`
- [ ] Can identify linear: AR = ∞
- [ ] Can identify circular: AR = 1
- [ ] Understand handedness convention

---

## 🔗 Related Documentation

- [poynting_pw](poynting_pw_MASTER_INDEX) - Often used together for wave analysis
- [Medium](Medium_MASTER_INDEX.md) - Material properties
- [Helpers](Helpers.md) - All EM MATLAB tools

---

**Last Updated:** 2025-12-06  
**Version:** 1.0  
**Modes Covered:** 3 (complete)
