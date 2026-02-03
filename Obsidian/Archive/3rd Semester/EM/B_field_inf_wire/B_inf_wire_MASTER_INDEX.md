# B_inf_wire.m - Master Documentation Index

> **Central hub for all B_inf_wire.m documentation**  
> Calculate magnetic field around an infinite current-carrying wire

---

## 📚 Complete Documentation Suite

| Document | Purpose | Time | When to Use |
|----------|---------|------|-------------|
| [**Quick Start**](B_inf_wire_Quick_Start.md) | Get started NOW | 2 min | First time using B_inf_wire |
| [**Complete Guide**](B_inf_wire_Complete_Guide.md) | Master everything | 12 min | Deep learning & reference |
| [**Quick Reference**](B_inf_wire_Quick_Reference.md) | Exam cheat sheet | 1 min | During exams/quick lookup |
| [**Troubleshooting**](B_inf_wire_Troubleshooting.md) | Fix problems | 2 min | When something's wrong |
| [**Exam Examples**](B_inf_wire_Exam_Examples.md) | Real problems | 8 min | Practice & preparation |

---

## 🎯 Quick Navigation

### By Your Situation

**"I've never used B_inf_wire before"**
→ Start with [Quick Start Guide](B_inf_wire_Quick_Start.md) (2 min)

**"I need to calculate B-field NOW"**
→ Use [Quick Reference Card](B_inf_wire_Quick_Reference.md) (1 min)

**"Something's not working"**
→ Check [Troubleshooting Guide](B_inf_wire_Troubleshooting.md) (2 min)

**"I want to understand this completely"**
→ Read [Complete Guide](B_inf_wire_Complete_Guide.md) (12 min)

**"Show me examples"**
→ See [Exam Examples](B_inf_wire_Exam_Examples.md) (8 min)

---

## 🚀 Recommended Learning Paths

### Path 1: "Exam Tomorrow" (10 minutes)
1. [Quick Start](B_inf_wire_Quick_Start.md) - 2 min
2. [Exam Examples](B_inf_wire_Exam_Examples.md) - 8 min

**Result:** Ready for B-field problems

---

### Path 2: "Master This Tool" (25 minutes)
1. [Quick Start](B_inf_wire_Quick_Start.md) - 2 min
2. [Complete Guide](B_inf_wire_Complete_Guide.md) - 12 min
3. [Exam Examples](B_inf_wire_Exam_Examples.md) - 8 min
4. [Troubleshooting](B_inf_wire_Troubleshooting.md) - 2 min
5. Practice - 1 min

**Result:** Complete mastery

---

### Path 3: "Quick Calculation" (1 minute)
1. [Quick Start](B_inf_wire_Quick_Start.md) - 1 min
2. Calculate immediately

**Result:** B-field computed

---

### Path 4: "Debugging" (2-5 minutes)
1. [Troubleshooting Guide](B_inf_wire_Troubleshooting.md) - 2 min
2. Check [Complete Guide](B_inf_wire_Complete_Guide.md) if needed - 3 min

**Result:** Error fixed

---

## 📋 What B_inf_wire.m Does

**B_inf_wire** calculates the **magnetic field magnitude** around an infinitely long, straight, current-carrying wire using Ampère's Law.

### Core Capabilities
✅ **Ampère's Law** - Automatic application
✅ **Vector capable** - Handles arrays of distances
✅ **Magnetic materials** - Optional μᵣ parameter
✅ **Correct units** - Field in Tesla [T]
✅ **Magnitude only** - Direction by right-hand rule

### Two Input Modes

```matlab
% Non-magnetic medium (air/vacuum)
B = B_inf_wire(I, r)

% Magnetic medium
B = B_inf_wire(I, r, mu_r)
```

**Inputs:**
- `I` - Current in Amperes [A]
- `r` - Radial distance(s) from wire in meters [m]
- `mu_r` - Relative permeability (default: 1)

**Output:**
- `B` - Magnetic field magnitude in Tesla [T]

---

## 🎓 Typical Use Cases

### What They Ask

**Example:** "A wire carries 5 A. Find the magnetic field at 2 cm from the wire."

### The One-Liner Solution

```matlab
B = B_inf_wire(5, 0.02);  % 5 A, 2 cm

% B = 5.0e-05 T = 50 μT
```

**Total time:** 10 seconds

---

## ⚡ The Core Pattern

### Standard Calculation (95% of problems)

```matlab
% Current in wire
I = 5;  % [A]

% Distance from wire
r = 0.02;  % 2 cm = 0.02 m

% Calculate B-field
B = B_inf_wire(I, r);

% Result: B in Tesla [T]
% Typical: 1-100 μT range
```

---

## 🔍 Quick Decision Tree

```
What do you need?

├─ B-field in air/vacuum?
│  └─ B = B_inf_wire(I, r)

├─ B-field in magnetic material?
│  └─ B = B_inf_wire(I, r, mu_r)

├─ B-field at multiple distances?
│  └─ r = [r1, r2, r3, ...];
│     B = B_inf_wire(I, r);

└─ Direction of B-field?
   └─ Use right-hand rule
      (Thumb: current, Fingers: B circles wire)
```

---

## 📊 Quick Formulas

### Ampère's Law for Infinite Wire

```
B = μI / (2πr)

where:
μ = μ₀μᵣ
μ₀ = 4π × 10⁻⁷ H/m
μᵣ = relative permeability (1 for air)
```

### Direction

**Right-hand rule:**
- Thumb points along current direction
- Fingers curl in direction of B-field
- B-field circles the wire

---

## 💡 Pro Tips

1. **Units matter** - Current in A, distance in m
2. **Typical values** - B-field usually in μT range
3. **Array input** - Can calculate multiple distances at once
4. **Direction** - Use right-hand rule (not given by function)
5. **μᵣ ≈ 1** - Most materials (air, copper, plastic)
6. **μᵣ >> 1** - Ferromagnetic materials (iron, nickel)

---

## ✅ Pre-Exam Checklist

- [ ] Know syntax: `B = B_inf_wire(I, r)`
- [ ] Remember: B = μI/(2πr)
- [ ] Unit conversions: mA = 1e-3 A, cm = 1e-2 m
- [ ] Typical range: 1-100 μT for normal currents/distances
- [ ] Direction: Right-hand rule (thumb = I, fingers = B)
- [ ] Default μᵣ = 1 (air/vacuum)
- [ ] Array input: r can be vector for multiple distances

---

## 📖 Document Descriptions

### [Quick Start Guide](B_inf_wire_Quick_Start.md)
**What:** 2-minute crash course  
**When:** First time or quick calculation  
**Contains:** The one pattern, examples, mistakes

### [Complete Guide](B_inf_wire_Complete_Guide.md)
**What:** Comprehensive 12-minute reference  
**When:** Deep learning or theory  
**Contains:** Ampère's law, magnetic materials, theory

### [Quick Reference Card](B_inf_wire_Quick_Reference.md)
**What:** 1-minute lookup sheet  
**When:** During exams  
**Contains:** One-liner, syntax, unit conversions

### [Troubleshooting Guide](B_inf_wire_Troubleshooting.md)
**What:** Error diagnosis  
**When:** Results seem wrong  
**Contains:** Common errors, fixes

### [Exam Examples](B_inf_wire_Exam_Examples.md)
**What:** Real magnetostatics problems  
**When:** Practice  
**Contains:** B-field calculations with solutions

---

## 🔗 Related Documentation

- [coulomb_pair](coulomb_pair_MASTER_INDEX.md) - Electric force (E&M analogue)
- [Medium](Medium_MASTER_INDEX.md) - For EM wave problems
- [Helpers](Helpers.md) - All EM MATLAB tools

---

## 📝 Quick Example

```matlab
% Wire carrying 10 A, find B at 1 cm, 2 cm, 5 cm

I = 10;  % Amperes
r = [0.01, 0.02, 0.05];  % meters

B = B_inf_wire(I, r);

>> B
B =
   2.0000e-04    1.0000e-04    4.0000e-05

% In microtesla:
>> B * 1e6
ans =
   200    100    40

% Interpretation:
% At 1 cm: 200 μT
% At 2 cm: 100 μT (half distance → half field)
% At 5 cm: 40 μT
```

---

## 🎯 Key Concepts

### Ampère's Law

**For infinite wire:**
```
∮ B⃗·dℓ⃗ = μI

Simplifies to: B(2πr) = μI
Therefore: B = μI/(2πr)
```

### Magnetic Field Properties

- **Circulates** around wire (not radial)
- **Inversely proportional** to distance (1/r)
- **Proportional** to current (linear in I)
- **No beginning/end** (closed loops)

### Typical Values

| Current | Distance | B-field |
|---------|----------|---------|
| 1 A | 1 cm | 20 μT |
| 5 A | 2 cm | 50 μT |
| 10 A | 5 cm | 40 μT |
| 100 A | 10 cm | 200 μT |

**Earth's field:** ~50 μT (for comparison)

---

## 🔬 Physical Insight

### Wire Geometry

```
        Distance r
    ←────────────→
    
    ║  I (current into page)
    ║
    ║     ⊙ Point P
    ║
    ║
```

**B-field at P:**
- Magnitude: B = μI/(2πr)
- Direction: Perpendicular to plane (I, r)
- Circles the wire (right-hand rule)

---

## 📏 Distance Scaling

**Key relationship:**
```
If distance doubles → B-field halves
If distance triples → B-field is 1/3

B ∝ 1/r  (inverse relationship)
```

**Example:**
```matlab
B1 = B_inf_wire(10, 0.01);  % 10 A at 1 cm
B2 = B_inf_wire(10, 0.02);  % 10 A at 2 cm

% B2 = B1/2 (exactly)
```

---

**Last Updated:** 2025-12-06  
**Version:** 1.0  
**Coverage:** Complete  
**Use Case:** Magnetostatics, B-field calculations
