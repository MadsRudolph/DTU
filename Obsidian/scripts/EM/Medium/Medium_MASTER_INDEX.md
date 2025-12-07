# Medium.m - Master Documentation Index

> **Central hub for all Medium.m documentation**  
> Choose your learning path below based on your needs and available time.

---

## 📚 Complete Documentation Suite

| Document                                         | Purpose           | Time     | When to Use               |
| ------------------------------------------------ | ----------------- | -------- | ------------------------- |
| [**Quick Start**](Medium_Quick_Start.md)         | Get started NOW   | 5 min    | First time using Medium   |
| [**Complete Guide**](Medium_Complete_Guide.md)   | Master everything | 30 min   | Deep learning & reference |
| [**Quick Reference**](Medium_Quick_Reference.md) | Exam cheat sheet  | 2 min    | During exams/quick lookup |
| [**Troubleshooting**](Medium_Troubleshooting.md) | Fix problems      | 5-10 min | When something's wrong    |
| [**Exam Examples**](Medium_Exam_Examples.md)     | Real problems     | 15 min   | Practice & preparation    |

---

## 🎯 Quick Navigation

### By Your Situation

**"I've never used Medium before"**
→ Start with [Quick Start Guide](Medium_Quick_Start.md) (5 min)

**"I need to solve this problem NOW"**
→ Use [Quick Reference Card](Medium_Quick_Reference.md) (2 min)

**"Something's not working"**
→ Check [Troubleshooting Guide](Medium_Troubleshooting.md) (5 min)

**"I want to master this completely"**
→ Read [Complete Guide](Medium_Complete_Guide.md) (30 min)

**"Show me real exam problems"**
→ See [Exam Examples](Medium_Exam_Examples.md) (15 min)

---

## 🚀 Recommended Learning Paths

### Path 1: "Exam Tomorrow" (20 minutes)
1. [Quick Start](Medium_Quick_Start.md) - 5 min
2. [Exam Examples](Medium_Exam_Examples.md) - 10 min  
3. [Quick Reference](Medium_Quick_Reference.md) - 2 min
4. Practice - 3 min

**Result:** Ready for basic exam problems

---

### Path 2: "Master This Tool" (1 hour)
1. [Quick Start](Medium_Quick_Start.md) - 5 min
2. [Complete Guide](Medium_Complete_Guide.md) - 30 min
3. [Exam Examples](Medium_Exam_Examples.md) - 15 min
4. [Troubleshooting](Medium_Troubleshooting.md) - 5 min
5. Practice - 5 min

**Result:** Complete mastery of Medium.m

---

### Path 3: "Quick Problem Solving" (10 minutes)
1. [Quick Start](Medium_Quick_Start.md) - 5 min
2. Solve your problem - 2 min
3. [Quick Reference](Medium_Quick_Reference.md) for next time - 2 min

**Result:** Problem solved, ready for more

---

### Path 4: "Debugging" (5-15 minutes)
1. [Troubleshooting Guide](Medium_Troubleshooting.md) - 5 min
2. Check [Complete Guide](Medium_Complete_Guide.md) if needed - 10 min

**Result:** Problem identified and fixed

---

## 📋 What Medium.m Does

**Medium.m** calculates electromagnetic wave propagation in ANY material:

✅ **Lossless dielectrics** (glass, air, plastics)
✅ **Lossy materials** (tissue, soil, seawater)  
✅ **Good conductors** (copper, aluminum, gold)
✅ **Free space** (vacuum calculations)

**It calculates:**
- Wavelength (λ) and phase velocity (v_p)
- Attenuation (α) and phase constant (β)
- Intrinsic impedance (η)
- Loss tangent and material classification
- Skin depth (δ)

---

## 🎓 Common Exam Problem Types

| Problem Type | Example Question | Solution |
|--------------|------------------|----------|
| **Wavelength in material** | "Find λ in glass (ε_r=4) at 10 GHz" | `r = Medium(4, 10e9); r.lambda` |
| **Skin depth** | "Find δ in copper at 1 GHz" | `r = Medium('conductor', 5.8e7, 1e9); r.skin_depth` |
| **Material classification** | "Is this a conductor or dielectric?" | `r = Medium(eps_r, sigma, freq); r.classification` |
| **Attenuation** | "How much loss over 1m?" | `r = Medium(eps_r, sigma, freq); loss_dB = r.alpha*8.686` |
| **Phase velocity** | "What is v_p in the material?" | `r = Medium(eps_r, freq); r.up` |

---

## ⚡ The One Pattern (90% of Problems)

```matlab
% For lossless materials (glass, air, etc.)
r = Medium(eps_r, freq);

% For lossy materials (tissue, soil, etc.)
r = Medium(eps_r, sigma, freq);

% For conductors (copper, aluminum, etc.)
r = Medium('conductor', sigma, freq);

% Get what you need:
wavelength = r.lambda;        % Wavelength
velocity = r.up;              % Phase velocity
impedance = r.eta;            % Intrinsic impedance
skin_depth = r.skin_depth;    % Skin depth (if lossy)
classification = r.classification;  % Material type
```

---

## 🔍 Quick Search Index

**By Topic:**
- **Wavelength calculation** → [Quick Start](Medium_Quick_Start.md) or [Complete Guide § Basic Usage](Medium_Complete_Guide.md)
- **Skin depth** → [Complete Guide § Conductor Mode](Medium_Complete_Guide.md)
- **Loss tangent** → [Complete Guide § Material Classification](Medium_Complete_Guide.md)
- **Attenuation** → [Complete Guide § Lossy Materials](Medium_Complete_Guide.md)
- **Wrong results** → [Troubleshooting](Medium_Troubleshooting.md)
- **Unit errors** → [Troubleshooting](Medium_Troubleshooting.md)
- **Exam problems** → [Exam Examples](Medium_Exam_Examples.md)

**By Input Type:**
- Two arguments (eps_r, freq) → Lossless mode
- Three arguments (eps_r, sigma, freq) → Lossy mode
- String first ('conductor', ...) → Special modes

---

## 📖 Document Descriptions

### [Quick Start Guide](Medium_Quick_Start.md)
**What:** 5-minute crash course on using Medium  
**When:** First time using Medium or quick refresher  
**Contains:** Essential pattern, 3 main modes, common mistakes

### [Complete Guide](Medium_Complete_Guide.md)
**What:** Comprehensive 30-minute reference  
**When:** Deep learning or detailed questions  
**Contains:** All modes, theory, workflows, advanced topics

### [Quick Reference Card](Medium_Quick_Reference.md)
**What:** 2-minute lookup sheet  
**When:** During exams or quick syntax check  
**Contains:** One-liners, essential fields, quick patterns

### [Troubleshooting Guide](Medium_Troubleshooting.md)
**What:** Error diagnosis and solutions  
**When:** Something's not working correctly  
**Contains:** Common errors, fixes, diagnostic tools

### [Exam Examples](Medium_Exam_Examples.md)
**What:** Real exam-style problems with solutions  
**When:** Practice or learning problem patterns  
**Contains:** Step-by-step solutions, exam strategies

---

## 💡 Pro Tips

1. **Units matter:** freq in Hz (not MHz), sigma in S/m (not mS/m)
2. **Check classification:** r.classification tells you if you picked the right mode
3. **Skin depth only for conductors:** Use `Medium('skin', ...)` for quick checks
4. **Loss tangent helps:** If tan(δ) > 10, material is a good conductor
5. **Free space baseline:** Use `Medium('free', freq)` to get λ₀, η₀, etc.

---

## 🎯 Quick Decision Tree

```
Need to analyze a material?
│
├─ Is it a good conductor (metal)?
│  └─ YES → Medium('conductor', sigma, freq)
│
├─ Is it lossless (σ = 0)?
│  └─ YES → Medium(eps_r, freq)
│
├─ Is it lossy (σ > 0)?
│  └─ YES → Medium(eps_r, sigma, freq)
│
├─ Have loss tangent instead of σ?
│  └─ YES → Medium('tand', eps_r, tan_delta, freq)
│
├─ Just need skin depth?
│  └─ YES → Medium('skin', sigma, freq)
│
└─ Need free space parameters?
   └─ YES → Medium('free', freq)
```

---

## 📞 Need Help?

**Quick fixes:**
- Check [Troubleshooting Guide](Medium_Troubleshooting.md)
- Verify units (Hz, S/m, not MHz, mS/m)
- Compare with [Exam Examples](Medium_Exam_Examples.md)

**Understanding:**
- Read relevant section in [Complete Guide](Medium_Complete_Guide.md)
- Check theory in your textbook
- Practice with [Exam Examples](Medium_Exam_Examples.md)

---

## ✅ Before Your Exam Checklist

- [ ] Read [Quick Start Guide](Medium_Quick_Start.md)
- [ ] Practice [Exam Examples](Medium_Exam_Examples.md)
- [ ] Print [Quick Reference Card](Medium_Quick_Reference.md)
- [ ] Know the one pattern: `r = Medium(eps_r, freq)`
- [ ] Remember units: freq in Hz, sigma in S/m
- [ ] Understand r.classification output

---

**Last Updated:** 2025-12-06  
**Version:** 1.0  
**Related:** [TLine](TLine_MASTER_INDEX.md) | [StubMatch](StubMatch_MASTER_INDEX.md) | [Helpers](Helpers.md)
