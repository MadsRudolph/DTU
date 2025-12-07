# PlaneWaveCheck - Quick Start Guide

> ⏱️ **Time:** 3 minutes  
> **Goal:** Learn which mode to use and verify plane waves quickly

**Navigation:** [Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)

---

## Step 1: Which Mode Do I Use?

```
What format is your problem?
│
├─► γ = [j...; ...; ...] given separately    (FORMAT A)
│   │
│   └─► Use MAXWELL mode
│       PlaneWaveCheck('maxwell', E0, H0, gamma)
│
└─► exp(-j(ax + by + cz)) in field expression (FORMAT B)
    │
    └─► Use FULL mode
        PlaneWaveCheck('full', E, H, k)
```

| Problem Format | Example | Mode to Use |
|----------------|---------|-------------|
| γ given explicitly | E₀=[2;0;0], H₀=[...], γ=[0;0;j3] | `'maxwell'` |
| exp(-j...) in field | E = E₀·exp(-j(20x+10z)) | `'full'` |

**⚠️ Basic mode (no quotes) only checks orthogonality - use `'full'` for exams!**

---

## Step 2: Extract Your Inputs

### For Format B (exp term) → Full Mode

Given: `E = E₀ŷ·exp(-j(20x+10z))`

```matlab
% 1. E direction and magnitude
E = [0; E0; 0];        % ŷ direction

% 2. H direction and magnitude  
H = [0; 0; H0];        % ẑ direction

% 3. k from phase term: exp(-j(20x + 0y + 10z))
k = [20; 0; 10];       % [coeff_x; coeff_y; coeff_z]
```

### For Format A (γ explicit) → Maxwell Mode

Given: E₀, H₀, γ as separate vectors

```matlab
% Just use them directly (handle complex components)
E0 = [2; 0; 0];
H0 = [0; -5.309e-3; 0];
gamma = [0; 0; 1j*3];   % j3 → 1j*3 in MATLAB
```

---

## Step 3: Run the Check

### Full Mode (Format B)

```matlab
result = PlaneWaveCheck('full', E, H, k);
```

**Output shows:**
- ✓ or ✗ for each of the 4 steps
- **Definitive answer:** IS or IS NOT a plane wave

### Maxwell Mode (Format A)

```matlab
result = PlaneWaveCheck('maxwell', E0, H0, gamma);
```

**Output shows:**
- Transverse checks (γ·E=0, γ·H=0)
- Maxwell equation verification
- ωε and ωμ values (must be real, positive)
- **Definitive answer:** IS or IS NOT a plane wave

---

## Complete Examples

### Example 1: E24 Q18 (Format B → Full Mode)

**Problem:** Is this a plane wave?
```
E = ĵ5·exp(-j(20x+10z)) V/m
H = k̂(1/120π)·exp(-j(20x+10z)) A/m
```

**Solution:**
```matlab
E = [0; 5; 0];              % ĵ means ŷ direction
H = [0; 0; 1/(120*pi)];     % k̂ means ẑ direction
k = [20; 0; 10];            % From exp(-j(20x+10z))

result = PlaneWaveCheck('full', E, H, k);
```

**Result:** `k·H = 10 ≠ 0` → **NOT a plane wave!**

---

### Example 2: Q1 Type (Format A → Maxwell Mode)

**Problem:** Is this a plane wave?
```
E₀ = [2; 0; 0] V/m
H₀ = [0; -5.309; 0] mA/m
γ = [0; 0; j3] m⁻¹
```

**Solution:**
```matlab
E0 = [2; 0; 0];
H0 = [0; -5.309e-3; 0];      % Convert mA/m to A/m
gamma = [0; 0; 1j*3];        % j3 → 1j*3

result = PlaneWaveCheck('maxwell', E0, H0, gamma);
```

**Result:** `ωε = -0.00796` (NEGATIVE!) → **NOT a plane wave!**

⚠️ **Trap:** Fields ARE orthogonal, but basic mode would miss this!

---

### Example 3: Q2 Type (Format A → Maxwell Mode)

**Problem:** Is this a plane wave?
```
E₀ = [0; j2; 5] V/m
H₀ = [0; -37.5; j15] mA/m
γ = [j10; 0; 0] m⁻¹
```

**Solution:**
```matlab
E0 = [0; 1j*2; 5];
H0 = [0; -37.5e-3; 1j*15e-3];
gamma = [1j*10; 0; 0];

result = PlaneWaveCheck('maxwell', E0, H0, gamma);
```

**Result:** `ωε = 0.075`, `ωμ = 0.02` (both positive) → **IS a plane wave!**

---

## The 4 Conditions (Formelsamling)

A valid plane wave must satisfy ALL of these:

| Step | Condition | Meaning |
|------|-----------|---------|
| 1a | k · E = 0 | E ⊥ propagation |
| 1b | k · H = 0 | H ⊥ propagation |
| 1c | E · H = 0 | E ⊥ H |
| 2 | k̂ = k/\|k\| | Normalize k |
| 3 | H = (1/η)(k̂ × E) | **Impedance relation** |
| 4 | (E × H)·k > 0 | Right-hand rule |

**Step 3 is REQUIRED** - basic mode skips it!

---

## Common Traps

### Trap 1: ĵ ≠ j

```
E = ĵ5·exp(...)  
```
- ĵ (j-hat) = ŷ unit vector = `[0; 1; 0]`
- j (no hat) = √(-1) = `1j` in MATLAB

### Trap 2: Orthogonal ≠ Valid

Fields can be perfectly orthogonal but **still invalid** if:
- Wrong H magnitude (fails impedance check)
- Unphysical ωε or ωμ (fails Maxwell check)

**Always use `'full'` or `'maxwell'` mode for exams!**

### Trap 3: Forgetting k·H

Most common error! E⊥H passes, but k·H ≠ 0.

---

## When to Use Each Mode

| Mode | Use When | Can Confirm? | Can Rule Out? |
|------|----------|--------------|---------------|
| Basic | Quick sanity check | ✗ No | ✓ Yes |
| **Full** | exp(-j...) problems | ✓ Yes | ✓ Yes |
| **Maxwell** | γ given explicitly | ✓ Yes | ✓ Yes |

---

## Next Steps

- 📋 [Quick Reference](PlaneWaveCheck_Quick_Reference.md) - Cheat sheet for exam
- 📝 [Exam Examples](PlaneWaveCheck_Exam_Examples.md) - More practice problems
- 📚 [Complete Guide](PlaneWaveCheck_Complete_Guide.md) - Full theory

---

**Navigation:** [Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)
