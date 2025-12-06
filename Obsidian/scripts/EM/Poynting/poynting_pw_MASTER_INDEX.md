# poynting_pw.m - Master Documentation Index

> **Central hub for all poynting_pw.m documentation**  
> The Q22-Q23 solver - H-field phasor and Poynting vector calculator

---

## 📚 Complete Documentation Suite

| Document | Purpose | Time | When to Use |
|----------|---------|------|-------------|
| [**Quick Start**](poynting_pw_Quick_Start.md) | Get started NOW | 3 min | First time using poynting_pw |
| [**Complete Guide**](poynting_pw_Complete_Guide.md) | Master everything | 20 min | Deep learning & reference |
| [**Quick Reference**](poynting_pw_Quick_Reference.md) | Exam cheat sheet | 1 min | During exams/quick lookup |
| [**Troubleshooting**](poynting_pw_Troubleshooting.md) | Fix problems | 3 min | When something's wrong |
| [**Exam Examples**](poynting_pw_Exam_Examples.md) | Q22-Q23 problems | 10 min | Practice & preparation |

---

## 🎯 Quick Navigation

### By Your Situation

**"I've never used poynting_pw before"**
→ Start with [Quick Start Guide](poynting_pw_Quick_Start.md) (3 min)

**"I need to solve Q22/Q23 NOW"**
→ Use [Quick Reference Card](poynting_pw_Quick_Reference.md) (1 min)

**"Something's not working"**
→ Check [Troubleshooting Guide](poynting_pw_Troubleshooting.md) (3 min)

**"I want to understand this completely"**
→ Read [Complete Guide](poynting_pw_Complete_Guide.md) (20 min)

**"Show me Q22-Q23 examples"**
→ See [Exam Examples](poynting_pw_Exam_Examples.md) (10 min)

---

## 🚀 Recommended Learning Paths

### Path 1: "Exam Tomorrow" (15 minutes)
1. [Quick Start](poynting_pw_Quick_Start.md) - 3 min
2. [Exam Examples](poynting_pw_Exam_Examples.md) - 10 min  
3. [Quick Reference](poynting_pw_Quick_Reference.md) - 1 min
4. Practice Q22-Q23 - 1 min

**Result:** Ready for Q22 and Q23

---

### Path 2: "Master This Tool" (40 minutes)
1. [Quick Start](poynting_pw_Quick_Start.md) - 3 min
2. [Complete Guide](poynting_pw_Complete_Guide.md) - 20 min
3. [Exam Examples](poynting_pw_Exam_Examples.md) - 10 min
4. [Troubleshooting](poynting_pw_Troubleshooting.md) - 3 min
5. Practice - 4 min

**Result:** Complete mastery of poynting_pw

---

### Path 3: "Quick Q22-Q23 Solving" (4 minutes)
1. [Quick Start](poynting_pw_Quick_Start.md) - 3 min
2. Solve Q22-Q23 - 1 min

**Result:** Questions answered

---

### Path 4: "Debugging" (3-10 minutes)
1. [Troubleshooting Guide](poynting_pw_Troubleshooting.md) - 3 min
2. Check [Complete Guide](poynting_pw_Complete_Guide.md) if needed - 7 min

**Result:** Error fixed

---

## 📋 What poynting_pw.m Does

**poynting_pw.m** is the **Q22-Q23 specialist** - calculates H-field phasor and Poynting vector for plane waves.

### Core Capabilities
✅ **Calculate H-field phasor** - Q22 answer in one call
✅ **Calculate Poynting vector** - Q23 answer in same call
✅ **Handle time-domain form** - a·cos + b·sin conversion
✅ **Vector phasor mode** - Direct E-field input
✅ **Auto-format output** - mA/m for H, W/m² for S

### Three Input Modes

**Mode 1: Time-Domain** (Q22-Q23 Exam Format)
```matlab
% E = E₀(a·cos(ψ) + b·sin(ψ)), β vector
poynting_pw('time', a, b, E0, beta_vec)
```

**Mode 2: Vector Phasor**
```matlab
% Given E phasor directly
poynting_pw(E_phasor, k_hat, eta)
```

**Mode 3: Scalar** (Original)
```matlab
% Simple power calculation
poynting_pw(E0, eta, A, phi)
```

---

## 🎓 Q22-Q23 Exam Problems

### What They Ask

**Q22:** "Calculate the H-field phasor" → `r.H_phasor` (in mA/m)

**Q23:** "Calculate the time-average Poynting vector" → `r.S_avg` (in W/m²)

### The One-Liner Solution

```matlab
% Given: E = E₀(a·cos + b·sin), β = (βx, βy, βz)
a = [2; 1; 0];  b = [0; -1; -2];  E0 = 10;  beta_vec = [2; -4; 2];
r = poynting_pw('time', a, b, E0, beta_vec);

% Q22 answer:
r.H_phasor  % Already in mA/m in output

% Q23 answer:
r.S_avg     % Already in W/m² in output
```

**Total time:** 30 seconds

---

## ⚡ The Core Pattern

### Q22-Q23 Pattern (95% of problems)
```matlab
% Extract from problem:
a = [ax; ay; az];      % Cosine coefficients
b = [bx; by; bz];      % Sine coefficients  
E0 = value;            % Amplitude
beta_vec = [βx; βy; βz];  % Beta vector

% Solve:
r = poynting_pw('time', a, b, E0, beta_vec);

% Get answers:
H = r.H_phasor;  % Q22 (mA/m)
S = r.S_avg;     % Q23 (W/m²)
```

---

## 🔍 Quick Decision Tree

```
What form is your E-field?

├─ Time-domain: E = E₀(a·cos + b·sin)?
│  └─ poynting_pw('time', a, b, E0, beta_vec)
│     → Solves Q22 AND Q23!

├─ Phasor: Ẽ given directly?
│  └─ poynting_pw(E_phasor, k_hat, eta)
│     → Get H and S

└─ Scalar power problem?
   └─ poynting_pw(E0, eta, A, phi)
      → Get |S| and P
```

---

## 📊 Quick Formulas

### H-field from E-field
```
H̃ = (1/η) · k̂ × Ẽ
```

### Poynting Vector
```
S̄ = ½ · Re{Ẽ × H̃*}
```

### Phasor from Time-Domain
```
E = E₀(a·cos(ψ) + b·sin(ψ))
Ẽ = E₀(a - jb)
```

---

## 💡 Pro Tips

1. **Q22-Q23 shortcut:** One function call solves both!
2. **Time-domain mode:** Most common for exams
3. **Output already formatted:** H in mA/m, S in W/m²
4. **Check units:** E₀ in V/m → H in mA/m automatically
5. **Verify direction:** S should point along k̂ for plane wave
6. **Default η = 377 Ω:** For air, don't need to specify

---

## ✅ Pre-Exam Checklist

- [ ] Know time-domain syntax: `poynting_pw('time', a, b, E0, beta)`
- [ ] Can extract a and b from E = E₀(a·cos + b·sin)
- [ ] Know Q22 answer: `r.H_phasor` (mA/m)
- [ ] Know Q23 answer: `r.S_avg` (W/m²)
- [ ] Remember: One call solves both Q22 AND Q23
- [ ] Understand: a = cosine coeffs, b = sine coeffs
- [ ] Know conversion: Ẽ = E₀(a - jb)

---

## 📖 Document Descriptions

### [Quick Start Guide](poynting_pw_Quick_Start.md)
**What:** 3-minute crash course  
**When:** First time or Q22-Q23 prep  
**Contains:** The one pattern, examples, mistakes

### [Complete Guide](poynting_pw_Complete_Guide.md)
**What:** Comprehensive 20-minute reference  
**When:** Deep learning or all modes  
**Contains:** All 3 modes, theory, formulas

### [Quick Reference Card](poynting_pw_Quick_Reference.md)
**What:** 1-minute lookup sheet  
**When:** During exams  
**Contains:** One-liner, syntax, quick formulas

### [Troubleshooting Guide](poynting_pw_Troubleshooting.md)
**What:** Error diagnosis  
**When:** Results seem wrong  
**Contains:** Common errors, fixes

### [Exam Examples](poynting_pw_Exam_Examples.md)
**What:** Q22-Q23 solutions  
**When:** Practice  
**Contains:** Real exam problems with complete solutions

---

## 🔗 Related Documentation

- [Polarization](Polarization_MASTER_INDEX.md) - Often used together for wave analysis
- [Medium](Medium_MASTER_INDEX.md) - For material properties (affects η)
- [Helpers](Helpers.md) - All EM MATLAB tools

---

## 📝 Quick Example

```matlab
% Given: E = 10([2;1;0]cos(ψ) + [0;-1;-2]sin(ψ))
%        β = (2, -4, 2) rad/m

a = [2; 1; 0];
b = [0; -1; -2];
E0 = 10;
beta_vec = [2; -4; 2];

r = poynting_pw('time', a, b, E0, beta_vec);

% Q22: H̃₀ = ?
r.H_phasor  % Shows in mA/m

% Q23: S̄ = ?
r.S_avg     % Shows in W/m²
```

---

**Last Updated:** 2025-12-06  
**Version:** 1.0  
**Modes Covered:** 3 (complete)  
**Exam Focus:** Q22-Q23
