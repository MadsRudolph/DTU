# PlaneWaveCheck Documentation - Master Index

> **Tool:** `PlaneWaveCheck.m`  
> **Purpose:** Verify if E and H fields represent a valid uniform plane wave  
> **Methods:** Full mode (exp term), Maxwell mode (γ explicit)

---

## 📍 Navigation

| Quick Start | Complete Guide | Quick Reference | Troubleshooting | Exam Examples |
|:-----------:|:--------------:|:---------------:|:---------------:|:-------------:|
| [📖 3 min](PlaneWaveCheck_Quick_Start.md) | [📚 15 min](PlaneWaveCheck_Complete_Guide.md) | [📋 1 min](PlaneWaveCheck_Quick_Reference.md) | [🔧 Fix issues](PlaneWaveCheck_Troubleshooting.md) | [📝 Practice](PlaneWaveCheck_Exam_Examples.md) |

**Other resources:** [Helpers.md](Helpers.md) · [Documentation Summary](PlaneWaveCheck_Documentation_Summary.md)

---

## ⚠️ Which Mode Should I Use?

```
What format is your problem?
│
├─► γ = [j...; ...; ...] given separately    (FORMAT A)
│   │
│   │   Example: E₀ = [2;0;0], H₀ = [0;-5.3e-3;0], γ = [0;0;j3]
│   │
│   └─► Use MAXWELL mode
│       PlaneWaveCheck('maxwell', E0, H0, gamma)
│
└─► exp(-j(ax + by + cz)) in field expression (FORMAT B)
    │
    │   Example: E = E₀[0;j;0] exp(-j(20x+10z))
    │
    └─► Use FULL mode
        PlaneWaveCheck('full', E, H, k, eta)
```

**⚠️ Basic mode is only a quick sanity check - it CANNOT confirm a plane wave!**

---

## Two Main Verification Methods

| Mode | Problem Format | Usage | What It Checks |
|------|----------------|-------|----------------|
| **Full** | exp(-j...) term | `PlaneWaveCheck('full', E, H, k)` | Orthogonality + H=(1/η)(k̂×E) |
| **Maxwell** | γ given explicitly | `PlaneWaveCheck('maxwell', E0, H0, γ)` | Full Maxwell equations + physical ωε, ωμ |

### Basic Mode (Limited Use)

```matlab
PlaneWaveCheck(E, H, k)   % ⚠️ Only checks orthogonality!
```

- Can **rule OUT** plane wave if orthogonality fails
- **CANNOT confirm** plane wave (doesn't check impedance relation)
- Output: "CANNOT DETERMINE" if orthogonality passes

---

## The 4-Step Verification (Formelsamling)

| Step | Condition | What It Checks |
|------|-----------|----------------|
| **1a** | k · E = 0 | E transverse to propagation |
| **1b** | k · H = 0 | H transverse to propagation |
| **1c** | E · H = 0 | E perpendicular to H |
| **2** | k̂ = k/\|k\| | Normalize wave vector |
| **3** | H = (1/η)(k̂ × E) | **Impedance relation** ← Required! |
| **4** | (E × H) · k > 0 | Right-hand rule (Poynting) |

**ANY failure → NOT a valid plane wave**

---

## Quick Usage Examples

### Format B: exp(-j...) Problems → Use Full Mode

```matlab
% Given: E = 5ŷ·exp(-j(20x+10z)), H = (1/120π)ẑ·exp(-j(20x+10z))
E = [0; 5; 0];              % 5 V/m in ŷ
H = [0; 0; 1/(120*pi)];     % A/m in ẑ
k = [20; 0; 10];            % From phase term exp(-j(20x+10z))

result = PlaneWaveCheck('full', E, H, k);
% → Checks all 4 steps, gives definitive answer
```

### Format A: γ Given Explicitly → Use Maxwell Mode

```matlab
% Given: E₀, H₀, γ as separate vectors
E0 = [2; 0; 0];
H0 = [0; -5.309e-3; 0];
gamma = [0; 0; 1j*3];       % Note: j3 → 1j*3 in MATLAB

result = PlaneWaveCheck('maxwell', E0, H0, gamma);
% → Checks Maxwell equations, verifies ωε and ωμ are physical
```

---

## Mode Comparison

| Feature | Basic Mode | Full Mode | Maxwell Mode |
|---------|------------|-----------|--------------|
| k·E = 0 | ✓ | ✓ | ✓ (via γ) |
| k·H = 0 | ✓ | ✓ | ✓ (via γ) |
| E·H = 0 | ✓ | ✓ | ✓ |
| H = (1/η)(k̂ × E) | ✗ | ✓ | ✓ (via ωε/ωμ) |
| Physical ωε, ωμ | ✗ | ✗ | ✓ |
| **Can confirm plane wave** | ✗ | ✓ | ✓ |
| **Can rule out plane wave** | ✓ | ✓ | ✓ |

---

## Common Exam Examples

### E24 Q18 - Fails k·H Check

```matlab
% Given: Ẽ = ĵ5e^(-j(20x+10z)), H̃ = ẑ(1/120π)e^(-j(20x+10z))
E = [0; 5; 0];
H = [0; 0; 1/(120*pi)];
k = [20; 0; 10];

PlaneWaveCheck('full', E, H, k);
% → k·H = 10 ≠ 0 → NOT a plane wave!
```

### Q1 Type - Fails ωε Check (Maxwell Mode)

```matlab
E0 = [2; 0; 0];
H0 = [0; -5.309e-3; 0];
gamma = [0; 0; 1j*3];

PlaneWaveCheck('maxwell', E0, H0, gamma);
% → ωε is NEGATIVE → NOT a plane wave (even though orthogonal!)
```

### Q2 Type - Valid Plane Wave (Maxwell Mode)

```matlab
E0 = [0; 1j*2; 5];
H0 = [0; -37.5e-3; 1j*15e-3];
gamma = [1j*10; 0; 0];

PlaneWaveCheck('maxwell', E0, H0, gamma);
% → ωε and ωμ both POSITIVE → IS a plane wave!
```

---

## Documentation Guides

| Guide | Time | Content |
|-------|------|---------|
| 📖 [Quick Start](PlaneWaveCheck_Quick_Start.md) | 3 min | Get running fast |
| 📚 [Complete Guide](PlaneWaveCheck_Complete_Guide.md) | 15 min | Full theory + all features |
| 📋 [Quick Reference](PlaneWaveCheck_Quick_Reference.md) | 1 min | Cheat sheet |
| 🔧 [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) | As needed | Fix common issues |
| 📝 [Exam Examples](PlaneWaveCheck_Exam_Examples.md) | 10 min | Practice problems |

---

## Learning Paths

### Path 1: "Exam Tomorrow" (5 min)
1. Quick Reference → know the 4 steps + mode decision
2. Quick Start → Q18 and Q1/Q2 examples
3. Ready for exam!

### Path 2: "Understand Everything" (25 min)
1. Complete Guide → theory and all modes
2. Exam Examples → practice problems
3. Troubleshooting → edge cases

### Path 3: "Which Mode Do I Use?" (2 min)
1. Look at decision tree above
2. Format A (γ explicit) → Maxwell mode
3. Format B (exp term) → Full mode

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using basic mode for exam | Can't confirm plane wave | Use 'full' or 'maxwell' |
| j = direction vs j = √-1 | Treating ĵ as imaginary | ĵ means ŷ unit vector |
| Forgot k·H check | Only checked E⊥H | Use 'full' mode (checks all) |
| Fields orthogonal but invalid | Basic says OK, actually NOT | Use 'maxwell' for γ problems |

---

## Related Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `PlaneWaveCheck` | Verify plane wave | Given E, H, k or γ |
| `Polarization` | Analyze polarization | Given E phasor |
| `poynting_pw` | Calculate power flow | Need S and H |
| `Medium` | Get η for material | Full mode with dielectric |

---

## Version History

- **v3.0** (Current): Clear mode separation
  - Basic mode now returns "CANNOT DETERMINE" (not false positives)
  - Clear decision guide: Format A → Maxwell, Format B → Full
  - Updated documentation
  
- **v2.0**: Added Maxwell mode for complex phasors
  
- **v1.0**: Basic orthogonality check only

---

## 📍 Quick Links

| [Quick Start](PlaneWaveCheck_Quick_Start.md) | [Complete Guide](PlaneWaveCheck_Complete_Guide.md) | [Quick Reference](PlaneWaveCheck_Quick_Reference.md) | [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) | [Exam Examples](PlaneWaveCheck_Exam_Examples.md) |
|:---:|:---:|:---:|:---:|:---:|

**Back to:** [Helpers.md](Helpers.md)
