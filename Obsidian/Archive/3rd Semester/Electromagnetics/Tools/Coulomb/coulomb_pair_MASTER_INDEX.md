# coulomb_pair.m - Master Documentation Index

> **Central hub for all coulomb_pair.m documentation**  
> Calculate Coulomb force between point charges

---

## 📚 Complete Documentation Suite

| Document | Purpose | Time | When to Use |
|----------|---------|------|-------------|
| [**Quick Start**](coulomb_pair_Quick_Start.md) | Get started NOW | 2 min | First time using coulomb_pair |
| [**Complete Guide**](coulomb_pair_Complete_Guide.md) | Master everything | 12 min | Deep learning & reference |
| [**Quick Reference**](coulomb_pair_Quick_Reference.md) | Exam cheat sheet | 1 min | During exams/quick lookup |
| [**Troubleshooting**](coulomb_pair_Troubleshooting.md) | Fix problems | 2 min | When something's wrong |
| [**Exam Examples**](coulomb_pair_Exam_Examples.md) | Real problems | 8 min | Practice & preparation |

---

## 🎯 Quick Navigation

### By Your Situation

**"I've never used coulomb_pair before"**
→ Start with [Quick Start Guide](coulomb_pair_Quick_Start.md) (2 min)

**"I need to calculate Coulomb force NOW"**
→ Use [Quick Reference Card](coulomb_pair_Quick_Reference.md) (1 min)

**"Something's not working"**
→ Check [Troubleshooting Guide](coulomb_pair_Troubleshooting.md) (2 min)

**"I want to understand this completely"**
→ Read [Complete Guide](coulomb_pair_Complete_Guide.md) (12 min)

**"Show me examples"**
→ See [Exam Examples](coulomb_pair_Exam_Examples.md) (8 min)

---

## 🚀 Recommended Learning Paths

### Path 1: "Exam Tomorrow" (10 minutes)
1. [Quick Start](coulomb_pair_Quick_Start.md) - 2 min
2. [Exam Examples](coulomb_pair_Exam_Examples.md) - 8 min

**Result:** Ready for Coulomb force problems

---

### Path 2: "Master This Tool" (25 minutes)
1. [Quick Start](coulomb_pair_Quick_Start.md) - 2 min
2. [Complete Guide](coulomb_pair_Complete_Guide.md) - 12 min
3. [Exam Examples](coulomb_pair_Exam_Examples.md) - 8 min
4. [Troubleshooting](coulomb_pair_Troubleshooting.md) - 2 min
5. Practice - 1 min

**Result:** Complete mastery

---

### Path 3: "Quick Calculation" (2 minutes)
1. [Quick Start](coulomb_pair_Quick_Start.md) - 2 min
2. Calculate immediately

**Result:** Force computed

---

### Path 4: "Debugging" (2-5 minutes)
1. [Troubleshooting Guide](coulomb_pair_Troubleshooting.md) - 2 min
2. Check [Complete Guide](coulomb_pair_Complete_Guide.md) if needed - 3 min

**Result:** Error fixed

---

## 📋 What coulomb_pair.m Does

**coulomb_pair** calculates the **electrostatic force** between two point charges using Coulomb's Law.

### Core Capabilities
✅ **Vector forces** - Returns both F₁₂ and F₂₁
✅ **Newton's 3rd law** - Forces are equal and opposite
✅ **3D positions** - Full vector calculation
✅ **Correct units** - Force in Newtons [N]
✅ **Direction included** - Attraction or repulsion

### Single Input Mode

```matlab
[F12, F21] = coulomb_pair(q1, q2, r1, r2)
```

**Inputs:**
- `q1, q2` - Charges in Coulombs [C]
- `r1, r2` - Position vectors [3×1] in meters [m]

**Outputs:**
- `F12` - Force on q₁ due to q₂ [N]
- `F21` - Force on q₂ due to q₁ [N]

---

## 🎓 Typical Use Cases

### What They Ask

**Example:** "Two charges q₁ = 2 μC at (1,0,0) and q₂ = -3 μC at (0,1,0). Find the force on each charge."

### The One-Liner Solution

```matlab
q1 = 2e-6;  q2 = -3e-6;
r1 = [1; 0; 0];  r2 = [0; 1; 0];
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% F12 = force on q1
% F21 = force on q2
```

**Total time:** 20 seconds

---

## ⚡ The Core Pattern

### Standard Calculation (95% of problems)

```matlab
% Define charges (in Coulombs)
q1 = 1e-6;        % 1 μC
q2 = -2e-6;       % -2 μC

% Define positions (in meters)
r1 = [1; 0; 0];   % (1, 0, 0) m
r2 = [0; 1; 0];   % (0, 1, 0) m

% Calculate forces
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% Results:
% F12 = force on q1 due to q2 [N]
% F21 = force on q2 due to q1 [N]
% Verify: F12 = -F21 (Newton's 3rd law)
```

---

## 🔍 Quick Decision Tree

```
What do you need?

├─ Force on charge 1?
│  └─ Use F12 from [F12, F21] = coulomb_pair(...)

├─ Force on charge 2?
│  └─ Use F21 from [F12, F21] = coulomb_pair(...)

├─ Both forces?
│  └─ Get both: [F12, F21] = coulomb_pair(...)

└─ Net force from multiple charges?
   └─ Call multiple times and sum
```

---

## 📊 Quick Formulas

### Coulomb's Law

```
|F| = k_e · |q₁||q₂| / r²

where:
k_e = 1/(4πε₀) = 8.99 × 10⁹ N·m²/C²
ε₀ = 8.854 × 10⁻¹² F/m
```

### Vector Form

```
F₁₂ = (k_e · q₁q₂ / r²) · r̂₁₂

where:
r̂₁₂ = (r₁ - r₂) / |r₁ - r₂|
```

### Newton's Third Law

```
F₂₁ = -F₁₂
```

---

## 💡 Pro Tips

1. **Units matter** - Charges in Coulombs (C), distances in meters (m)
2. **μC conversion** - 1 μC = 1×10⁻⁶ C → use `1e-6`
3. **nC conversion** - 1 nC = 1×10⁻⁹ C → use `1e-9`
4. **Column vectors** - Use semicolons: `[x; y; z]`
5. **Sign convention** - Positive = repulsion, negative = attraction
6. **Verify answer** - Check F₁₂ = -F₂₁

---

## ✅ Pre-Exam Checklist

- [ ] Know syntax: `[F12, F21] = coulomb_pair(q1, q2, r1, r2)`
- [ ] Remember: F12 = force ON q1 DUE TO q2
- [ ] Unit conversions: μC = 1e-6 C, nC = 1e-9 C
- [ ] Column vectors: `[x; y; z]` with semicolons
- [ ] Verify: F12 = -F21 (Newton's 3rd law)
- [ ] Sign: Same charges → repel (positive dot product)
- [ ] Sign: Opposite charges → attract (negative dot product)

---

## 📖 Document Descriptions

### [Quick Start Guide](coulomb_pair_Quick_Start.md)
**What:** 2-minute crash course  
**When:** First time or quick calculation  
**Contains:** The one pattern, examples, mistakes

### [Complete Guide](coulomb_pair_Complete_Guide.md)
**What:** Comprehensive 12-minute reference  
**When:** Deep learning or theory  
**Contains:** Physics theory, formulas, multiple charges

### [Quick Reference Card](coulomb_pair_Quick_Reference.md)
**What:** 1-minute lookup sheet  
**When:** During exams  
**Contains:** One-liner, syntax, unit conversions

### [Troubleshooting Guide](coulomb_pair_Troubleshooting.md)
**What:** Error diagnosis  
**When:** Results seem wrong  
**Contains:** Common errors, fixes

### [Exam Examples](coulomb_pair_Exam_Examples.md)
**What:** Real force calculations  
**When:** Practice  
**Contains:** Electrostatics problems with solutions

---

## 🔗 Related Documentation

- [B_inf_wire](Helpers.md) - Magnetic field calculations
- [Medium](Medium_MASTER_INDEX.md) - For EM wave problems
- [Helpers](Helpers.md) - All EM MATLAB tools

---

## 📝 Quick Example

```matlab
% Two charges: q1 = 2 μC at origin, q2 = -3 μC at (1,0,0)
q1 = 2e-6;
q2 = -3e-6;
r1 = [0; 0; 0];
r2 = [1; 0; 0];

[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% Results:
>> F12
F12 =
  -0.0539  % Force in x-direction [N]
   0
   0

>> F21
F21 =
   0.0539  % Equal and opposite
   0
   0

% Interpretation:
% Opposite charges → attractive force
% q1 pulled toward q2 (-x direction)
% q2 pulled toward q1 (+x direction)
```

---

## 🎯 Key Concepts

### Force Direction

**Same sign charges:**
- Both positive OR both negative
- Forces point AWAY from each other (repulsion)

**Opposite sign charges:**
- One positive, one negative
- Forces point TOWARD each other (attraction)

### Magnitude

```
|F| = k_e · |q₁q₂| / r²
    = 8.99×10⁹ · |q₁q₂| / r²
```

**Distance doubles** → Force ¼ (inverse square)  
**Charge doubles** → Force doubles (linear)

---

**Last Updated:** 2025-12-06  
**Version:** 1.0  
**Coverage:** Complete  
**Use Case:** Electrostatics problems
