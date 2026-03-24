# TLine.m - Master Documentation Index

> **Central hub for all TLine.m documentation**  
> The ultimate transmission line calculator - 10 modes, infinite possibilities

---

## 📚 Complete Documentation Suite

| Document | Purpose | Time | When to Use |
|----------|---------|------|-------------|
| [**Quick Start**](TLine_Quick_Start.md) | Get started NOW | 5 min | First time using TLine |
| [**Complete Guide**](TLine_Complete_Guide.md) | Master everything | 45 min | Deep learning & reference |
| [**Quick Reference**](TLine_Quick_Reference.md) | Exam cheat sheet | 2 min | During exams/quick lookup |
| [**Troubleshooting**](TLine_Troubleshooting.md) | Fix problems | 5-10 min | When something's wrong |
| [**Exam Examples**](TLine_Exam_Examples.md) | Real problems | 20 min | Practice & preparation |

---

## 🎯 Quick Navigation

### By Your Situation

**"I've never used TLine before"**
→ Start with [Quick Start Guide](TLine_Quick_Start.md) (5 min)

**"I need to solve this problem NOW"**
→ Use [Quick Reference Card](TLine_Quick_Reference.md) (2 min)

**"Something's not working"**
→ Check [Troubleshooting Guide](TLine_Troubleshooting.md) (5 min)

**"I want to master this completely"**
→ Read [Complete Guide](TLine_Complete_Guide.md) (45 min)

**"Show me real exam problems"**
→ See [Exam Examples](TLine_Exam_Examples.md) (20 min)

---

## 🚀 Recommended Learning Paths

### Path 1: "Exam Tomorrow" (25 minutes)
1. [Quick Start](TLine_Quick_Start.md) - 5 min
2. [Exam Examples](TLine_Exam_Examples.md) - 15 min  
3. [Quick Reference](TLine_Quick_Reference.md) - 2 min
4. Practice - 3 min

**Result:** Ready for most exam problems

---

### Path 2: "Master This Tool" (1.5 hours)
1. [Quick Start](TLine_Quick_Start.md) - 5 min
2. [Complete Guide](TLine_Complete_Guide.md) - 45 min
3. [Exam Examples](TLine_Exam_Examples.md) - 20 min
4. [Troubleshooting](TLine_Troubleshooting.md) - 5 min
5. Practice - 15 min

**Result:** Complete mastery of TLine.m

---

### Path 3: "Quick Problem Solving" (10 minutes)
1. [Quick Start](TLine_Quick_Start.md) - 5 min
2. Solve your problem - 3 min
3. [Quick Reference](TLine_Quick_Reference.md) for next time - 2 min

**Result:** Problem solved, ready for more

---

### Path 4: "Debugging" (5-20 minutes)
1. [Troubleshooting Guide](TLine_Troubleshooting.md) - 5 min
2. Check [Complete Guide](TLine_Complete_Guide.md) if needed - 15 min

**Result:** Problem identified and fixed

---

## 📋 What TLine.m Does

**TLine.m** is the ULTIMATE transmission line calculator with **10 powerful modes:**

### Core Analysis (Modes 1-3)
✅ **Full TL analysis** - Z_in, Γ, VSWR, everything
✅ **Impedance transformation** - Find Z_in or Z_L
✅ **Reflection coefficients** - Γ ↔ Z conversions

### Advanced Features (Modes 4-6)
✅ **Find load from input** - Solve Q13/Q14 exam types
✅ **Quarter-wave transformer** - Auto-design matching
✅ **Special lengths** - λ/4 and λ/2 shortcuts

### Circuit Analysis (Modes 7-9)
✅ **TL + series elements** - Capacitors/inductors
✅ **TL + shunt elements** - Complete circuits
✅ **Complex circuits** - Multiple elements

### Design Tools (Mode 10)
✅ **Stub design** - Realize any reactance

---

## 🎓 Common Exam Problem Types

| Problem Type | Example Question | TLine Mode | Time |
|--------------|------------------|------------|------|
| **Basic analysis** | "Find Z_in of 50Ω line..." | `TLine(50, 100, 0.3)` | 30s |
| **Find Γ_L from Γ_A** | "Given Γ at input, find load" (Q13/Q14) | `TLine('load', ...)` | 1min |
| **QW transformer** | "Design matching transformer" | `TLine('QW', 50, 100)` | 30s |
| **TL + capacitor** | "Find Z_A with series C" (Q11) | `TLine('series_C', ...)` | 1min |
| **Stub to realize Z** | "Find stub length for j30Ω" (Q12) | `TLine('stub', 1j*30, 75, 'short')` | 30s |
| **VSWR calculation** | "What is the VSWR?" | `TLine(Z0, ZL, len).VSWR` | 20s |
| **Impedance at distance** | "Find Z at 0.25λ from load" | `TLine('Zin', Z0, ZL, 0.25)` | 30s |

---

## ⚡ The Core Patterns

### Pattern 1: Basic Analysis (80% of problems)
```matlab
r = TLine(Z0, ZL, len_lambda);
% Get: Z_in, Gamma_L, Gamma_in, VSWR, everything
```

### Pattern 2: Find Load (Q13/Q14)
```matlab
r = TLine('load', Z0, Gamma_A, len_lambda);
% Output: r.Gamma_L (Q13), r.Z_L (Q14)
```

### Pattern 3: TL + Element (Q11)
```matlab
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp);
% Output: r.Z_A (total impedance at input)
```

### Pattern 4: Stub Design (Q12)
```matlab
r = TLine('stub', Z_target, Z0, 'short');
% Output: r.short.len_lambda (stub length)
```

---

## 🔍 Quick Search Index

**By Problem Type:**
- **Basic TL analysis** → [Quick Start](TLine_Quick_Start.md)
- **Q11 (TL + element)** → [Exam Examples § Q11](TLine_Exam_Examples.md)
- **Q12 (stub design)** → [Exam Examples § Q12](TLine_Exam_Examples.md)
- **Q13/Q14 (find load)** → [Exam Examples § Q13-Q14](TLine_Exam_Examples.md)
- **Quarter-wave** → [Complete Guide § QW Mode](TLine_Complete_Guide.md)
- **VSWR** → [Complete Guide § Full Analysis](TLine_Complete_Guide.md)
- **Wrong results** → [Troubleshooting](TLine_Troubleshooting.md)

**By Mode:**
- Full analysis → Mode 1
- Impedance transform → Mode 2
- Gamma/Z conversion → Mode 3
- Find load → Mode 4
- QW transformer → Mode 5
- Special lengths → Mode 6
- Series element → Mode 7
- Shunt element → Mode 8
- Circuit → Mode 9
- Stub design → Mode 10

---

## 📖 Document Descriptions

### [Quick Start Guide](TLine_Quick_Start.md)
**What:** 5-minute crash course on using TLine  
**When:** First time using TLine or quick refresher  
**Contains:** 4 essential patterns, common modes, mistakes

### [Complete Guide](TLine_Complete_Guide.md)
**What:** Comprehensive 45-minute reference  
**When:** Deep learning or detailed questions  
**Contains:** All 10 modes, theory, workflows, advanced topics

### [Quick Reference Card](TLine_Quick_Reference.md)
**What:** 2-minute lookup sheet  
**When:** During exams or quick syntax check  
**Contains:** One-liners, essential fields, quick patterns

### [Troubleshooting Guide](TLine_Troubleshooting.md)
**What:** Error diagnosis and solutions  
**When:** Something's not working correctly  
**Contains:** Common errors, fixes, diagnostic tools

### [Exam Examples](TLine_Exam_Examples.md)
**What:** Real exam-style problems with solutions  
**When:** Practice or learning problem patterns  
**Contains:** Q11-Q14 solutions, exam strategies

---

## 💡 Pro Tips

1. **Know your modes:** 10 modes, pick the right one
2. **Length units:** λ for normalized, meters with freq/vp
3. **Q13/Q14 shortcut:** Use `TLine('load', ...)` - solves both!
4. **Q11 pattern:** `TLine('series_C', ...)` or `'series_L'`
5. **Q12 pattern:** `TLine('stub', Z_target, Z0, 'short')`
6. **Check VSWR:** `r.VSWR` tells you match quality
7. **Use aliases:** `r.Z_in` = `r.Z_A` (same thing)

---

## 🎯 Quick Decision Tree

```
What do you need to do?

├─ Basic analysis (Z_in, VSWR, Gamma)?
│  └─ TLine(Z0, ZL, len_lambda)

├─ Find load from measurement at input? (Q13/Q14)
│  └─ TLine('load', Z0, Gamma_A, len_lambda)

├─ Design quarter-wave transformer?
│  └─ TLine('QW', Z_source, Z_load)

├─ TL with capacitor/inductor? (Q11)
│  ├─ Series: TLine('series_C', ...) or TLine('series_L', ...)
│  └─ Shunt: TLine('shunt_C', ...) or TLine('shunt_L', ...)

├─ Realize impedance with stub? (Q12)
│  └─ TLine('stub', Z_target, Z0, 'short')

├─ Just convert Gamma ↔ Z?
│  ├─ TLine('Gamma', Z0, Z)
│  └─ TLine('Z', Z0, Gamma)

└─ Propagate Gamma along line?
   ├─ Load → Input: TLine('Gamma_in', Gamma_L, len)
   └─ Input → Load: TLine('Gamma_L', Gamma_in, len)
```

---

## ✅ Before Your Exam Checklist

- [ ] Read [Quick Start Guide](TLine_Quick_Start.md)
- [ ] Practice [Exam Examples](TLine_Exam_Examples.md) (Q11-Q14)
- [ ] Print [Quick Reference Card](TLine_Quick_Reference.md)
- [ ] Know basic pattern: `r = TLine(Z0, ZL, len_lambda)`
- [ ] Know Q13/Q14 shortcut: `TLine('load', ...)`
- [ ] Know Q11 pattern: `TLine('series_C', ...)`
- [ ] Know Q12 pattern: `TLine('stub', ...)`
- [ ] Remember: length in λ (not meters unless with freq/vp)

---

## 🔗 Related Documentation

- [StubMatch](StubMatch_MASTER_INDEX.md) - Single-stub matching (uses TLine internally)
- [Medium](Medium_MASTER_INDEX.md) - Material properties for TL design
- [Helpers](Helpers.md) - All EM MATLAB tools

---

**Last Updated:** 2025-12-06  
**Version:** 1.0  
**TLine Modes:** 10 (complete coverage)
