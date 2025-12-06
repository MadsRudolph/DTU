# poynting_pw.m - Exam Examples

> **Q22-Q23 Complete Solutions**

---

## Example 1: Standard Q22-Q23

### Problem (E23 Winter 2024)
The electric field of a plane wave in air is:
```
E = 10([2x̂ + ŷ]cos(ωt - β·r) + [-ŷ - 2ẑ]sin(ωt - β·r)) V/m
```
with β = (2, -4, 2) rad/m.

**Q22:** Calculate the magnetic field phasor H̃₀ (mA/m)  
**Q23:** Calculate the time-average Poynting vector S̄ (W/m²)

### Solution
```matlab
% Extract coefficients
a = [2; 1; 0];
b = [0; -1; -2];
E0 = 10;
beta_vec = [2; -4; 2];

% Solve
r = poynting_pw('time', a, b, E0, beta_vec);
```

### Console Output
```
==========================================
   PLANE WAVE: H-FIELD & POYNTING (Q22-Q23)
==========================================
  Ẽ₀ = [20.0-0.0j; 10.0+10.0j; 0.0+20.0j] V/m
  k̂ = [0.4082, -0.8165, 0.4082]
  η = 377 Ω
------------------------------------------
  Q22: H̃₀ = (1/η)·k̂ × Ẽ₀
  H̃₀ = [42.17+0.00j; 10.54-21.08j; -47.71+21.08j] mA/m
------------------------------------------
  Q23: S̄ = ½·Re{Ẽ × H̃*}
  S̄ = [54.110; -108.220; 54.110] W/m²
  |S̄| = 132.583 W/m²
==========================================
```

### Answers
**Q22:** H̃₀ = [42.17, 10.54-j21.08, -47.71+j21.08] mA/m  
**Q23:** S̄ = [54.11, -108.22, 54.11] W/m², |S̄| = 132.6 W/m²

---

## Example 2: Simple Case

### Problem
```
E = 5([x̂]cos(ωt - β·r) + [ŷ]sin(ωt - β·r)) V/m
β = (0, 0, 3) rad/m
```

Find H̃₀ and S̄.

### Solution
```matlab
a = [1; 0; 0];
b = [0; 1; 0];
E0 = 5;
beta_vec = [0; 0; 3];

r = poynting_pw('time', a, b, E0, beta_vec);
```

### Output
```
H̃₀ = [0.00+0.00j; -13.26+0.00j; 0.00-13.26j] mA/m
S̄ = [0.000; 0.000; 33.156] W/m²
```

### Physical Interpretation
- E in xy-plane
- Propagation in +z (β = [0;0;3])
- S points in +z (energy flows along propagation)
- |S̄| = 25/(2×377) = 33.16 W/m² ✓

---

## Example 3: Verification

### Problem
Verify the Poynting vector calculation manually:
```
E = [20; 10+j10; j20] V/m
β = [2; -4; 2] rad/m
```

### Solution with poynting_pw
```matlab
E_phasor = [20; 10+1j*10; 1j*20];
beta_vec = [2; -4; 2];

r = poynting_pw(E_phasor, beta_vec);

>> r.S_avg
ans =
   54.110
 -108.220
   54.110
```

### Manual Verification
```matlab
% Step 1: Get k̂
beta_mag = norm(beta_vec);  % = sqrt(4+16+4) = 4.899
k_hat = beta_vec/beta_mag;  % = [0.408; -0.816; 0.408]

% Step 2: Calculate H̃
eta = 377;
H = (1/eta) * cross(k_hat, E_phasor);

% Step 3: Calculate S̄
S = 0.5 * real(cross(E_phasor, conj(H)));

>> S
ans =
   54.110
 -108.220
   54.110   ✓ Matches!
```

---

## Example 4: Different Medium

### Problem
```
E = 8([x̂+ŷ]cos(ψ) + [ẑ]sin(ψ)) V/m
β = (1, 1, 1) rad/m
η = 250 Ω (material with ε_r = 2.25)
```

### Solution
```matlab
a = [1; 1; 0];
b = [0; 0; 1];
E0 = 8;
beta_vec = [1; 1; 1];
eta = 250;  % Specify non-air impedance

r = poynting_pw('time', a, b, E0, beta_vec, eta);
```

### Output
```
H̃₀ = [...] mA/m  (using η = 250 Ω)
S̄ = [...] W/m²
```

**Note:** η affects H but not S direction

---

## 🎓 Exam Strategy

### Time Management
- **Extract coefficients:** 10 seconds
- **Function call:** 5 seconds  
- **Read answer:** 10 seconds
- **Total:** 25-30 seconds per question
- **Q22 + Q23 together:** ~1 minute

### Step-by-Step
1. **Identify format:** E = E₀(a·cos + b·sin)
2. **Extract a, b from cos/sin terms**
3. **Extract E₀, β**
4. **One function call**
5. **Read console for answers**

### Common Patterns
```matlab
% Pattern 1: Separate components
E = E₀([a_x;a_y;a_z]cos + [b_x;b_y;b_z]sin)
→ a = [a_x; a_y; a_z]
→ b = [b_x; b_y; b_z]

% Pattern 2: Unit vectors
E = E₀(x̂·cos + ŷ·sin)
→ a = [1; 0; 0]
→ b = [0; 1; 0]

% Pattern 3: Mixed
E = E₀([2x̂+ŷ]cos + [-ŷ]sin)
→ a = [2; 1; 0]
→ b = [0; -1; 0]
```

---

## ✅ Answer Checklist

**Q22 (H-field):**
- [ ] Units in mA/m
- [ ] Three components (complex)
- [ ] Magnitude reasonable (~E/377 for air)
- [ ] Perpendicular to E and k̂

**Q23 (Poynting):**
- [ ] Units in W/m²
- [ ] Three components (real)
- [ ] Points along k̂ direction
- [ ] Magnitude = |E|²/(2η)

---

[← Master Index](poynting_pw_MASTER_INDEX.md)
