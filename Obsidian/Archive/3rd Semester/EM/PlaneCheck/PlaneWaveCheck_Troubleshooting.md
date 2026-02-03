# PlaneWaveCheck Troubleshooting Guide

> **Purpose:** Diagnose and fix common issues with PlaneWaveCheck

---

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)

---

## Quick Diagnostic: Which Mode Should I Use?

```
What format is your problem?
│
├─► γ = [j...; ...; ...] given separately    → Use 'maxwell'
│
└─► exp(-j(ax + by + cz)) in field           → Use 'full'
```

**⚠️ Basic mode can only rule OUT plane waves - it cannot confirm them!**

---

## Quick Diagnostic

Run this to see detailed output:
```matlab
PlaneWaveCheck()  % Demo mode shows examples
```

---

## Problem 1: "NOT a plane wave" but I think it should be

### Symptoms
- Basic mode says it's not a plane wave
- You've checked E⊥H manually and it's true

### Common Causes

**Cause A: Forgot to check k·H**
```matlab
% E24 Q18 trap: E⊥H is true, but H is NOT ⊥ k!
E = [0; 1; 0];    % ŷ
H = [0; 0; 1];    % ẑ
k = [20; 0; 10];  % 20x̂ + 10ẑ

% k·E = 0 ✓
% E·H = 0 ✓
% k·H = 10 ✗ ← THE PROBLEM!
```

**Fix:** Check the k·H output value - it should be 0.

**Cause B: Wrong k vector extraction**
```matlab
% Phase term: exp(-j(20x + 10z))
% WRONG:
k = [20; 10; 0];  % Confused y and z!

% RIGHT:
k = [20; 0; 10];  % x gets 20, z gets 10, y gets 0
```

**Cause C: Treating j as direction**
```matlab
% Phasor: ĵ5 e^(-jφ)
% WRONG: j is a direction component
E = [0; 1j*5; 0];  % Then using full phasor

% RIGHT: j is phase, ĵ means ŷ direction
E_dir = [0; 1; 0];  % Extract direction only
```

---

## Problem 2: Basic mode says "CANNOT DETERMINE"

### Symptom
```matlab
PlaneWaveCheck([10;0;0], [0;1;0], [0;0;5])
% Output: "⚠️ RESULT: CANNOT DETERMINE (verification incomplete)"
```

### Cause: Basic mode only checks orthogonality

Basic mode **cannot confirm** a plane wave - it can only rule one out. This is by design because:
- Orthogonality is NECESSARY but NOT SUFFICIENT
- The impedance relation H = (1/η)(k̂ × E) must also be checked

### Fix: Use 'full' mode

```matlab
% Full mode gives definitive answer:
PlaneWaveCheck('full', [10;0;0], [0; 10/377; 0], [0;0;5])
% Output: "✓ RESULT: This IS a valid UNIFORM PLANE WAVE"
```

---

## Problem 3: Full mode fails but orthogonality passes

### Symptom
```matlab
PlaneWaveCheck('full', [10;0;0], [0;1;0], [0;0;5])  % ✗ Full fails
% But all orthogonality checks pass
```

### Cause: Wrong H magnitude

Full mode also checks:
- **Step 3:** H = (1/η)(k̂ × E)
- **Step 4:** (E × H) · k > 0

### Fix: Use correct H magnitude

```matlab
E = [10; 0; 0];           % 10 V/m
eta = 377;                % Free space

% Calculate correct H
k_hat = [0; 0; 1];        % Unit vector in z
H_correct = (1/eta) * cross(k_hat, E);
% H_correct = [0; 0.0265; 0]  (10/377 in ŷ)

PlaneWaveCheck('full', E, H_correct, [0;0;5])  % ✓ Now passes
```

---

## Problem 3: Impedance error is huge

### Symptom
```
Step 3: H = (1/η)(k̂ × E)   ✗ FAIL (error = 277.0%)
```

### Causes and Fixes

**Cause A: H direction is correct but magnitude is wrong**
```matlab
% You have H = [0; 0.1; 0] but need H = [0; 0.0265; 0]
% Error = |0.1 - 0.0265| / 0.0265 ≈ 277%
```

**Cause B: Using wrong impedance**
```matlab
% In a dielectric with εᵣ = 4:
eta_dielectric = 377 / sqrt(4);  % = 188.5 Ω, NOT 377!

PlaneWaveCheck('full', E, H, k, eta_dielectric)
```

**Cause C: H direction is wrong**
```matlab
% k̂ × E might give different direction than your H
k_hat = [0; 0; 1];  % ẑ
E = [10; 0; 0];     % x̂
H_expected = (1/377) * cross(k_hat, E);  % Should be in +ŷ

% If your H is in -ŷ or x̂, it will fail!
```

---

## Problem 4: Poynting vector check fails

### Symptom
```
Step 4: (E × H) · k = -0.265   ✗ FAIL (S not || k)
```

### Cause: Power flowing in -k direction

The E and H vectors are oriented such that E × H points opposite to k.

### Fix: Check field orientations

For a wave propagating in +ẑ:
- E in +x̂, H in +ŷ → S in +ẑ ✓
- E in +x̂, H in -ŷ → S in -ẑ ✗
- E in -x̂, H in +ŷ → S in -ẑ ✗

```matlab
% Right-hand rule: E × H should point along k
E = [1; 0; 0];   % +x̂
H = [0; 1; 0];   % +ŷ
% cross(E, H) = [0; 0; 1] = +ẑ ✓

E = [1; 0; 0];   % +x̂
H = [0; -1; 0];  % -ŷ
% cross(E, H) = [0; 0; -1] = -ẑ ✗
```

---

## Problem 5: Floating-point precision issues

### Symptom
```
k · E = 1.2326e-15   ✗ FAIL
```

### Cause: Tolerance too strict (shouldn't happen with current script)

The script uses `tol = 1e-6` which should handle this.

### Diagnostic
```matlab
result = PlaneWaveCheck(E, H, k);
disp(result.tolerance)     % Should be 1e-6
disp(result.k_dot_E)       % Check actual value
```

### Fix (if needed): Scale vectors

```matlab
% If values are very large, numerical errors grow
E_scaled = E / max(abs(E));
H_scaled = H / max(abs(H));
k_scaled = k / max(abs(k));
PlaneWaveCheck(E_scaled, H_scaled, k_scaled)
```

---

## Problem 6: Complex phasors not working

### Symptom
Using complex phasors gives unexpected results.

### Cause: Phasor mode extracts magnitudes only

```matlab
% Phasor mode uses |component| for direction
E_phasor = [1+1j; 0; 0];  % |1+1j| = √2 in x-direction
H_phasor = [0; 1j; 0];    % |1j| = 1 in y-direction
```

### Fix: Use basic mode with explicit directions

```matlab
% Instead of phasor mode:
E_dir = [1; 0; 0];  % Manually extract direction
H_dir = [0; 1; 0];
PlaneWaveCheck(E_dir, H_dir, k)

% For full verification with actual field values:
E_actual = [real_magnitude; 0; 0];
H_actual = [0; real_magnitude/377; 0];
PlaneWaveCheck('full', E_actual, H_actual, k)
```

---

## Problem 7: Basic mode says valid, but answer key says invalid

### Symptom
- Basic mode: "IS a plane wave" ✓
- But the correct answer is "NOT a plane wave"

### Cause: Fields are orthogonal but physically impossible

This is the **Q1-type trap**. The fields satisfy orthogonality (k·E=0, k·H=0, E·H=0) but they **cannot exist in a physical medium** because they would require negative ε or μ.

### Solution: Use Maxwell Mode

```matlab
% Example: Q1 type problem
E0 = [2; 0; 0];
H0 = [0; -5.309e-3; 0];
gamma = [0; 0; 1j*3];  % Complex γ = jβ

% Basic mode - WRONG answer!
PlaneWaveCheck([2;0;0], [0;1;0], [0;0;3])  % → "IS a plane wave"

% Maxwell mode - CORRECT answer!
PlaneWaveCheck('maxwell', E0, H0, gamma)   % → "NOT a plane wave"
% Reason: ωε is NEGATIVE (unphysical)
```

### When to use Maxwell mode

- Complex phasor fields (the "E0, H0, γ" format)
- When problem asks "can this be a plane wave?"
- When you need to verify physical realizability

---

## Problem 8: Maxwell mode gives "ωε not positive" or "ωμ not positive"

### Symptom
```
✗ RESULT: This is NOT a valid plane wave
  Failed checks: ωε not positive, ωμ not positive
```

### Cause: Sign error in H field

The fields don't satisfy Maxwell's equations with positive (physical) material parameters.

### Diagnostic

```matlab
result = PlaneWaveCheck('maxwell', E0, H0, gamma);
disp(result.omega_eps)  % Should be positive real numbers
disp(result.omega_mu)   % Should be positive real numbers
```

### Fix: Check H field sign

Often H has the wrong sign. Try negating it:

```matlab
% Original
H0 = [0; -5.309e-3; 0];

% Try negating
H0_neg = -H0;
PlaneWaveCheck('maxwell', E0, H0_neg, gamma);
```

If the negated H gives a valid result, the original H was wrong.

---

## Problem 9: Maxwell mode input format confusion

### Symptom
Not sure how to format inputs for Maxwell mode.

### Solution: Use complex phasors directly

```matlab
% E0 and H0 are COMPLEX phasor amplitudes
E0 = [0; 1j*2; 5];               % [Ex; Ey; Ez] with complex values
H0 = [0; -37.5e-3; 1j*15e-3];    % [Hx; Hy; Hz] with complex values

% gamma is the COMPLEX propagation vector
% For lossless: γ = jβ
% For lossy: γ = α + jβ
gamma = [1j*10; 0; 0];  % γ = jβx̂ (propagating in +x)

% Note: j in MATLAB is 1j (not just j or i)
% E.g., j2 in math → 1j*2 in MATLAB
```

---

## Problem 7: Understanding output fields

### Reading the result structure

```matlab
result = PlaneWaveCheck('full', E, H, k);

% Quick checks:
result.is_plane_wave      % Final answer
result.orthogonality_pass % Steps 1a-1c all passed?

% Detailed diagnostics:
result.k_dot_E            % Should be ≈ 0
result.k_dot_H            % Should be ≈ 0 (often forgotten!)
result.E_dot_H            % Should be ≈ 0

% Full mode only:
result.impedance_error    % Should be < 1%
result.poynting_dot_k     % Should be > 0
```

---

## Diagnostic Script

Copy and run this to diagnose issues:

```matlab
%% PlaneWaveCheck Diagnostic Script
% Fill in your values:
E = [0; 1; 0];      % Your E direction/vector
H = [0; 0; 1];      % Your H direction/vector
k = [20; 0; 10];    % Your k vector

fprintf('=== INPUT ANALYSIS ===\n');
fprintf('E = [%.4g, %.4g, %.4g]\n', E(1), E(2), E(3));
fprintf('H = [%.4g, %.4g, %.4g]\n', H(1), H(2), H(3));
fprintf('k = [%.4g, %.4g, %.4g]\n', k(1), k(2), k(3));
fprintf('\n');

fprintf('=== MANUAL CHECKS ===\n');
fprintf('k · E = %.6g (should be ≈ 0)\n', dot(k, E));
fprintf('k · H = %.6g (should be ≈ 0)\n', dot(k, H));
fprintf('E · H = %.6g (should be ≈ 0)\n', dot(E, H));
fprintf('\n');

k_hat = k / norm(k);
fprintf('k̂ = [%.4f, %.4f, %.4f]\n', k_hat(1), k_hat(2), k_hat(3));

eta = 377;
H_expected = (1/eta) * cross(k_hat, E);
fprintf('Expected H = (1/η)(k̂ × E) = [%.4g, %.4g, %.4g]\n', ...
    H_expected(1), H_expected(2), H_expected(3));
fprintf('\n');

S = cross(E, H);
fprintf('S = E × H = [%.4g, %.4g, %.4g]\n', S(1), S(2), S(3));
fprintf('S · k = %.6g (should be > 0)\n', dot(S, k));
fprintf('\n');

fprintf('=== RUNNING PLANEWAVECHECK ===\n');
result = PlaneWaveCheck(E, H, k);
```

---

## Still Having Issues?

1. **Check the demo:** `PlaneWaveCheck()` shows working examples
2. **Compare with examples:** See [Exam Examples](PlaneWaveCheck_Exam_Examples.md)
3. **Verify extraction:** Double-check k vector from phase term
4. **Use full mode diagnostics:** Check `impedance_error` and `poynting_dot_k`
5. **Read the theory:** See [Complete Guide](PlaneWaveCheck_Complete_Guide.md)

---

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)
