# PlaneWaveCheck Documentation Summary

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)

---

## Tool Overview

**PlaneWaveCheck.m** verifies if given E and H field vectors represent a valid uniform plane wave using the 5-step method from the course Formelsamling Section 4.

---

## The 5-Step Verification Method

Based on "Plane Waves Formelsamling" guidelines:

| Step | Guideline | Condition | Implementation |
|------|-----------|-----------|----------------|
| 1a | #1 | k · E = 0 | Orthogonality check with tolerance |
| 1b | #1 | k · H = 0 | Orthogonality check with tolerance |
| 1c | #1 | E · H = 0 | Orthogonality check with tolerance |
| 2 | #2 | k̂ = k/\|k\| | Normalization before cross products |
| 3 | #3 | H = (1/η)(k̂ × E) | Impedance relation verification |
| 4 | #4 | (E × H) · k > 0 | Right-hand rule / Poynting direction |

**Guideline #5** (phasor phase consistency) is implicitly checked through Step 3 when η is complex.

---

## Usage Modes

### Basic Mode (Steps 1-2)
```matlab
PlaneWaveCheck(E_vec, H_vec, k_vec)
PlaneWaveCheck(E_vec, H_vec, kx, ky, kz)
```
- Checks orthogonality only
- Uses direction vectors
- Fast for exam problems

### Full Mode (All 5 Steps)
```matlab
PlaneWaveCheck('full', E, H, k)        % η = 377 Ω
PlaneWaveCheck('full', E, H, k, eta)   % Custom η
```
- Complete verification
- Checks field magnitudes
- Verifies power flow direction

### Phasor Mode
```matlab
PlaneWaveCheck('phasor', E_phasor, H_phasor, k_vec)
```
- Extracts directions from complex phasors
- Basic orthogonality check

---

## Key Implementation Details

### Tolerance
- Uses `tol = 1e-6` as recommended in Formelsamling MATLAB tip
- Scaled by vector magnitudes for robustness
- Prevents floating-point false negatives

### Impedance Check (Step 3)
- Calculates expected H = (1/η)(k̂ × E)
- Uses 1% relative tolerance for magnitude comparison
- Handles complex η for lossy media

### Poynting Check (Step 4)
- Verifies (E × H) · k > 0
- Ensures power flows in +k direction
- Catches sign errors in H

---

## Documentation Suite

| Document | Purpose | Size |
|----------|---------|------|
| MASTER_INDEX.md | Navigation hub | ~3 KB |
| Quick_Start.md | 3-min crash course | ~4 KB |
| Complete_Guide.md | Full theory + reference | ~8 KB |
| Quick_Reference.md | 1-min cheat sheet | ~2 KB |
| Troubleshooting.md | Problem diagnosis | ~5 KB |
| Exam_Examples.md | Practice problems | ~6 KB |

**Total:** ~28 KB documentation

---

## Example: E24 Q18

The classic exam trap that this tool catches:

```matlab
% Given: Ẽ = ĵ5e^(-j(20x+10z)), H̃ = ẑ(1/120π)e^(-j(20x+10z))
E_dir = [0; 1; 0];    % ŷ
H_dir = [0; 0; 1];    % ẑ  
k_vec = [20; 0; 10];  % From phase term

result = PlaneWaveCheck(E_dir, H_dir, k_vec);
```

**Result:** NOT a plane wave
- k·E = 0 ✓
- k·H = 10 ✗ ← H not transverse!
- E·H = 0 ✓

**Lesson:** Students often check E⊥H but forget H⊥k!

---

## Output Structure

```matlab
result.is_plane_wave      % Final verdict
result.full_mode          % Mode used

% Step 1: Orthogonality
result.k_dot_E, k_dot_H, E_dot_H
result.cond1_pass, cond2_pass, cond3_pass
result.orthogonality_pass

% Step 2: Normalization
result.k_hat, k_mag

% Step 3: Impedance (full mode)
result.eta, H_expected, impedance_error
result.cond4_pass

% Step 4: Poynting (full mode)
result.poynting_vec, poynting_dot_k
result.cond5_pass
```

---

## Compliance with Guidelines

| Formelsamling Guideline | Status |
|------------------------|--------|
| 1. Zero dot product rule | ✅ Implemented |
| 1b. Tolerance (1e-6) | ✅ Implemented |
| 2. Normalization of k | ✅ Implemented |
| 3. Cross product H = (1/η)(k̂ × E) | ✅ Implemented |
| 4. Right-hand rule (E × H) || k | ✅ Implemented |
| 5. Phasor phase consistency | ✅ Implicit in Step 3 |

---

## Integration

### With Helpers.md
PlaneWaveCheck is documented in Section 7 of the Helpers.md master reference.

### With Other Tools
- Use `Medium.m` to get η for different materials
- Use `Polarization.m` for detailed polarization analysis
- Use `poynting_pw.m` for power calculations

---

## Version

**v2.0** - Complete implementation following all 5 Formelsamling guidelines
- Full 5-step verification
- Basic and Full modes
- Proper numerical tolerance
- Comprehensive output structure

---

## 📍 Navigation

[← Master Index](PlaneWaveCheck_MASTER_INDEX.md) · [Quick Start](PlaneWaveCheck_Quick_Start.md) · [Complete Guide](PlaneWaveCheck_Complete_Guide.md) · [Quick Reference](PlaneWaveCheck_Quick_Reference.md) · [Troubleshooting](PlaneWaveCheck_Troubleshooting.md) · [Exam Examples](PlaneWaveCheck_Exam_Examples.md)
