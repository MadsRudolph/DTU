# PlaneWaveCheck Exam Examples

> **Purpose:** Practice problems with complete solutions

---

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md)

---

## ⚠️ Which Mode to Use?

| Problem Format | Mode | Example |
|----------------|------|---------|
| γ given explicitly | `'maxwell'` | E₀=[2;0;0], γ=[0;0;j3] |
| exp(-j...) term | `'full'` | E = E₀·exp(-j(20x+10z)) |

**⚠️ Basic mode cannot confirm plane waves - use `'full'` for definitive answers!**

---

## Example 1: E24 Q18 - The Classic Trap (Format B → Full Mode)

### Problem Statement
Given the fields:
```
Ẽ = ĵ5e^(-j(20x+10z)) V/m
H̃ = ẑ(1/120π)e^(-j(20x+10z)) A/m
```
Do these represent a uniform plane wave?

### Solution

**Step 1: Identify format** → exp(-j...) term → Use **Full Mode**

**Step 2: Extract vectors from phasors**

From **Ẽ = ĵ5e^(-j(20x+10z))**:
- Direction: ĵ means ŷ (the j in "ĵ" is the unit vector, not √-1!)
- E = [0; 5; 0]

From **H̃ = ẑ(1/120π)e^(-j(20x+10z))**:
- Direction: ẑ
- H = [0; 0; 1/(120*pi)]

From **phase term e^(-j(20x+10z))**:
- k = [20; 0; 10]

**Step 3: Run PlaneWaveCheck**
```matlab
E = [0; 5; 0];
H = [0; 0; 1/(120*pi)];
k = [20; 0; 10];

result = PlaneWaveCheck('full', E, H, k);  % Use 'full' mode!
```

**Step 4: Analyze output**
```
STEP 1: ORTHOGONALITY CHECK
    1. k · E = 0        ✓ PASS (E ⊥ k)
    2. k · H = 10       ✗ FAIL (H not ⊥ k)
    3. E · H = 0        ✓ PASS (E ⊥ H)

✗ RESULT: This is NOT a valid plane wave
  Failed conditions: k·H≠0
```

**Answer:** NOT a uniform plane wave

**Why?** H has a component in the ẑ direction, but k also has a ẑ component (10ẑ). Therefore k·H ≠ 0.

---

## Example 2: Standard +z Propagation (Valid, Format B)

### Problem
Verify this is a plane wave:
```
E = x̂ E₀ cos(ωt - βz)
H = ŷ (E₀/η₀) cos(ωt - βz)
```

### Solution
```matlab
E = [10; 0; 0];          % x̂ direction, 10 V/m
H = [0; 10/377; 0];      % ŷ direction, E₀/η₀
k = [0; 0; 5];           % +ẑ (from -βz phase)

result = PlaneWaveCheck('full', E, H, k);  % Use 'full' mode!
```

**Output:**
```
    1. k · E = 0   ✓ PASS
    2. k · H = 0   ✓ PASS
    3. E · H = 0   ✓ PASS

✓ RESULT: This IS a valid UNIFORM PLANE WAVE
```

### Full Verification
```matlab
E0 = 10;  % V/m
eta0 = 377;
E = [E0; 0; 0];
H = [0; E0/eta0; 0];
k = [0; 0; 5];

result = PlaneWaveCheck('full', E, H, k);
```

**Output:**
```
STEP 3: IMPEDANCE RELATION
    Expected H = [0, 0.0265, 0]
    Actual   H = [0, 0.0265, 0]
    4. H = (1/η)(k̂ × E)   ✓ PASS (error = 0.00%)

STEP 4: RIGHT-HAND RULE
    S = E × H = [0, 0, 0.265]
    (E × H) · k = 1.327   ✓ PASS (S || k)

✓ RESULT: This IS a valid UNIFORM PLANE WAVE
    All 5 conditions satisfied.
```

---

## Example 3: +x Propagation (Valid)

### Problem
Wave propagating in +x direction:
```
E = ŷ E₀ e^(-jβx)
H = -ẑ (E₀/η₀) e^(-jβx)
```

### Solution
```matlab
E_dir = [0; 1; 0];   % ŷ
H_dir = [0; 0; -1];  % -ẑ (note the negative!)
k_vec = [1; 0; 0];   % +x̂

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
```

**Check manually:**
- k·E = [1,0,0]·[0,1,0] = 0 ✓
- k·H = [1,0,0]·[0,0,-1] = 0 ✓
- E·H = [0,1,0]·[0,0,-1] = 0 ✓

**Verify right-hand rule:**
- E × H = [0,1,0] × [0,0,-1] = [-1,0,0] = -x̂
- But k = +x̂, so (E × H)·k = -1 < 0 ???

**Wait!** Let's reconsider the H direction for proper right-hand rule:
```matlab
% For E in +ŷ, k in +x̂:
% k̂ × E = [1,0,0] × [0,1,0] = [0,0,1] = +ẑ
% So H should be in +ẑ, not -ẑ!

H_dir = [0; 0; 1];  % +ẑ (corrected)
result = PlaneWaveCheck(E_dir, H_dir, k_vec);
```

**Lesson:** Direction of H matters for full mode!

---

## Example 4: Diagonal Propagation (Valid)

### Problem
Wave propagating at 45° in the x-z plane:
```
k = x̂ + ẑ
E = ŷ E₀
H = ?
```

### Solution

**Step 1: Determine H direction**

H must be perpendicular to both k and E.
- k = [1; 0; 1]
- E = [0; 1; 0] (ŷ)
- H ∝ k̂ × E

```matlab
k = [1; 0; 1];
k_hat = k / norm(k);  % [0.707; 0; 0.707]
E = [0; 1; 0];
H_dir = cross(k_hat, E);  % [0.707; 0; -0.707] ∝ (x̂ - ẑ)
```

**Step 2: Verify**
```matlab
E_dir = [0; 1; 0];
H_dir = [1; 0; -1] / sqrt(2);  % Normalized
k_vec = [1; 0; 1];

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
```

**Output:**
```
    1. k · E = 0   ✓ PASS
    2. k · H = 0   ✓ PASS  (1×0.707 + 0×0 + 1×(-0.707) = 0)
    3. E · H = 0   ✓ PASS

✓ RESULT: This IS a valid UNIFORM PLANE WAVE
```

---

## Example 5: Longitudinal E-field (Invalid)

### Problem
Can this be a plane wave?
```
E = x̂ E₀ e^(-jβx)
H = ŷ H₀ e^(-jβx)
```

### Solution
```matlab
E_dir = [1; 0; 0];   % x̂
H_dir = [0; 1; 0];   % ŷ
k_vec = [1; 0; 0];   % +x̂ (same as E direction!)

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
```

**Output:**
```
    1. k · E = 1   ✗ FAIL (E not ⊥ k)
    2. k · H = 0   ✓ PASS
    3. E · H = 0   ✓ PASS

✗ RESULT: This is NOT a valid plane wave
  Failed conditions: k·E≠0
```

**Why invalid:** E is parallel to k (longitudinal), not transverse!

---

## Example 6: E and H Not Perpendicular (Invalid)

### Problem
```
E = (x̂ + ŷ) E₀ e^(-jβz)
H = (x̂ + ŷ) H₀ e^(-jβz)
```

### Solution
```matlab
E_dir = [1; 1; 0] / sqrt(2);
H_dir = [1; 1; 0] / sqrt(2);  % Same direction as E!
k_vec = [0; 0; 1];

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
```

**Output:**
```
    1. k · E = 0   ✓ PASS
    2. k · H = 0   ✓ PASS
    3. E · H = 1   ✗ FAIL (E not ⊥ H)

✗ RESULT: This is NOT a valid plane wave
  Failed conditions: E·H≠0
```

---

## Example 7: Full Mode - Impedance Mismatch

### Problem
In free space, we have:
```
E = x̂ 100 V/m
H = ŷ 0.5 A/m
k = ẑ 10 rad/m
```
Is this a valid plane wave?

### Solution
```matlab
E = [100; 0; 0];
H = [0; 0.5; 0];
k = [0; 0; 10];

result = PlaneWaveCheck('full', E, H, k);
```

**Output:**
```
STEP 1: ORTHOGONALITY CHECK
    1. k · E = 0   ✓ PASS
    2. k · H = 0   ✓ PASS
    3. E · H = 0   ✓ PASS

STEP 3: IMPEDANCE RELATION
  H = (1/η)(k̂ × E),  η = 377.00 Ω
    Expected H = [0, 0.2653, 0]
    Actual   H = [0, 0.5, 0]
    4. H = (1/η)(k̂ × E)   ✗ FAIL (error = 88.4%)

✗ RESULT: This is NOT a valid plane wave
  Failed conditions: H≠(1/η)(k̂×E)
```

**Analysis:**
- Orthogonality: All three conditions pass ✓
- Impedance: H should be 100/377 = 0.265 A/m, not 0.5 A/m ✗

**Correct H:**
```matlab
H_correct = [0; 100/377; 0];  % [0; 0.2653; 0]
result = PlaneWaveCheck('full', E, H_correct, k);
% Now passes all 5 conditions!
```

---

## Self-Test Problems

### Problem A
```
E = ẑ 10 e^(-j5y) V/m
H = x̂ (10/377) e^(-j5y) A/m
```
Is this a plane wave? What are E_dir, H_dir, k_vec?

<details>
<summary>Answer</summary>

```matlab
E_dir = [0; 0; 1];   % ẑ
H_dir = [1; 0; 0];   % x̂
k_vec = [0; 5; 0];   % +ŷ (from -j5y)

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
% ✓ IS a plane wave (all orthogonality conditions pass)
```
</details>

### Problem B
```
E = ŷ 5 e^(-j(3x+4z)) V/m
H = (4x̂ - 3ẑ) (5/377)/5 e^(-j(3x+4z)) A/m
```
Is this a plane wave?

<details>
<summary>Answer</summary>

```matlab
E_dir = [0; 1; 0];           % ŷ
H_dir = [4; 0; -3] / 5;      % Normalized
k_vec = [3; 0; 4];           % From phase term

% Check k·H = 3×(4/5) + 0 + 4×(-3/5) = 12/5 - 12/5 = 0 ✓
result = PlaneWaveCheck(E_dir, H_dir, k_vec);
% ✓ IS a plane wave
```
</details>

### Problem C
What's wrong with this wave?
```
E = x̂ 10 + ŷ 5 e^(-jβz)
H = (x̂ 5 + ŷ 10)/377 e^(-jβz)
```

<details>
<summary>Answer</summary>

E·H = (10×5 + 5×10)/377 = 100/377 ≠ 0

E and H are not perpendicular! NOT a plane wave.

```matlab
E_dir = [10; 5; 0];
H_dir = [5; 10; 0];
k_vec = [0; 0; 1];

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
% ✗ Fails E·H = 0 condition
```
</details>

---

## Maxwell Mode Examples (Complex Phasors)

### Example 8: Q1 Type - NOT a Plane Wave (Tricky!)

**Given phasors:**
```
E₀ = [2; 0; 0] V/m
H₀ = [0; -5.309; 0] mA/m
γ  = [0; 0; j3] m⁻¹
```

**The trap:** These fields ARE orthogonal! k·E = 0, k·H = 0, E·H = 0 all pass.
But is it a valid plane wave?

```matlab
E0 = [2; 0; 0];              % V/m
H0 = [0; -5.309e-3; 0];      % A/m (convert from mA/m!)
gamma = [0; 0; 1j*3];        % Complex γ = jβ

result = PlaneWaveCheck('maxwell', E0, H0, gamma);
```

**Output:**
```
══════════════════════════════════════════════════════════════════
     MAXWELL PLANE WAVE VERIFICATION (Cross-Product Method)       
══════════════════════════════════════════════════════════════════
  INPUT PHASORS:
    E₀ = [2; 0; 0] V/m
    H₀ = [0; -0.005309; 0] A/m
    γ  = [0; 0; j3] m⁻¹
──────────────────────────────────────────────────────────────────
  STEP 1: TRANSVERSE CHECK
    E₀ · γ = 0   ✓
    H₀ · γ = 0   ✓
──────────────────────────────────────────────────────────────────
  STEP 3: MAXWELL RELATIONS
    ωε components: -0.00796    ← NEGATIVE!
    ωμ components: -0.00796    ← NEGATIVE!
──────────────────────────────────────────────────────────────────
  STEP 4: PHYSICAL SANITY CHECKS
    ωε positive?   ✗ NO (negative or zero)
    ωμ positive?   ✗ NO (negative or zero)
══════════════════════════════════════════════════════════════════
  ✗ RESULT: This is NOT a valid plane wave
    Failed checks: ωε not positive, ωμ not positive
══════════════════════════════════════════════════════════════════
```

**Answer:** NOT a plane wave

**Why?** Although the fields are orthogonal, the Maxwell relations require **negative** ε and μ to be satisfied. This is not physical for a standard lossless medium.

**Key lesson:** Basic mode would say "valid" but Maxwell mode catches this!

---

### Example 9: Q2 Type - Valid Plane Wave

**Given phasors:**
```
E₀ = [0; j2; 5] V/m
H₀ = [0; -37.5; j15] mA/m
γ  = [j10; 0; 0] m⁻¹
```

```matlab
E0 = [0; 1j*2; 5];               % V/m (note: j2 → 1j*2 in MATLAB)
H0 = [0; -37.5e-3; 1j*15e-3];    % A/m
gamma = [1j*10; 0; 0];           % γ = jβx̂

result = PlaneWaveCheck('maxwell', E0, H0, gamma);
```

**Output:**
```
══════════════════════════════════════════════════════════════════
     MAXWELL PLANE WAVE VERIFICATION (Cross-Product Method)       
══════════════════════════════════════════════════════════════════
  STEP 1: TRANSVERSE CHECK
    E₀ · γ = 0   ✓
    H₀ · γ = 0   ✓
──────────────────────────────────────────────────────────────────
  STEP 3: MAXWELL RELATIONS
    ωε components: 0.075, 0.075    ← Both positive and equal!
    ωμ components: 0.02, 0.02      ← Both positive and equal!
──────────────────────────────────────────────────────────────────
  STEP 4: PHYSICAL SANITY CHECKS
    ωε real?       ✓ YES
    ωε positive?   ✓ YES
    ωε consistent? ✓ YES
    ωμ real?       ✓ YES
    ωμ positive?   ✓ YES
    ωμ consistent? ✓ YES
══════════════════════════════════════════════════════════════════
  ✓ RESULT: This IS a valid UNIFORM PLANE WAVE
    Maxwell relations satisfied with physical ωε and ωμ.
    ωε = 0.075,  ωμ = 0.02
══════════════════════════════════════════════════════════════════
```

**Answer:** IS a valid plane wave

**Why?** Both ωε and ωμ are real, positive, and consistent across all components. The fields satisfy Maxwell's equations with physical material parameters.

---

## Summary: Exam Strategy

1. **Extract vectors carefully**
   - E direction from field component
   - H direction from field component  
   - k from phase term coefficients

2. **Watch for traps**
   - j in "ĵ" is unit vector, not √-1
   - H⊥k often forgotten (E24 Q18!)
   - Direction matters in full mode
   - **Orthogonal ≠ plane wave** (Q1 type!)

3. **Use appropriate mode**
   - Basic: direction-only questions
   - Full: magnitude verification required
   - **Maxwell: complex phasors (Q1/Q2 type)**

4. **Check all conditions**
   - k·E = 0
   - k·H = 0 ← Don't forget!
   - E·H = 0
   - H = (1/η)(k̂ × E)
   - (E × H)·k > 0
   - **ωε, ωμ real, positive, consistent** (Maxwell mode)

---

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md)
