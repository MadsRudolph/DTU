# poynting_pw.m - Quick Start Guide

> **3-Minute Crash Course**  
> Master Q22-Q23 in minutes

---

## TL;DR - The One Pattern You Need

```matlab
% Q22-Q23 Exam Pattern
% Given: E = E₀(a·cos(ψ) + b·sin(ψ)), β vector

a = [2; 1; 0];       % Extract from cosine term
b = [0; -1; -2];     % Extract from sine term
E0 = 10;             % Amplitude
beta_vec = [2; -4; 2];  % Beta vector

r = poynting_pw('time', a, b, E0, beta_vec);

% Q22 Answer:
H_phasor = r.H_phasor;  % mA/m (already formatted!)

% Q23 Answer:
S_avg = r.S_avg;        % W/m² (already formatted!)
```

**That's it!** One function call solves both Q22 AND Q23.

---

## The Q22-Q23 Pattern

### Problem Format

You'll see this in the exam:

> The electric field of a plane wave is:
> ```
> E = E₀([ax; ay; az]cos(ωt - β·r) + [bx; by; bz]sin(ωt - β·r))
> ```
> with β = (βx, βy, βz) rad/m and E₀ = X V/m.
>
> **Q22:** Find the magnetic field phasor H̃₀ in mA/m.
> **Q23:** Find the time-average Poynting vector S̄ in W/m².

### Solution Steps

**Step 1:** Extract coefficients
```matlab
a = [ax; ay; az];      % From cos term
b = [bx; by; bz];      % From sin term
E0 = value;            % Given amplitude
beta_vec = [βx; βy; βz];  % Beta components
```

**Step 2:** One function call
```matlab
r = poynting_pw('time', a, b, E0, beta_vec);
```

**Step 3:** Read answers
```matlab
% Q22: Look at console output or:
r.H_phasor  % Already in mA/m

% Q23: Look at console output or:
r.S_avg     % Already in W/m²
```

---

## Complete Example

### Given
```
E = 10([2x̂ + ŷ]cos(ωt - β·r) + [-ŷ - 2ẑ]sin(ωt - β·r)) V/m
β = (2, -4, 2) rad/m
```

**Q22:** Find H̃₀ (mA/m)  
**Q23:** Find S̄ (W/m²)

### Solution
```matlab
% Step 1: Extract
a = [2; 1; 0];       % cos coefficients
b = [0; -1; -2];     % sin coefficients  
E0 = 10;             % amplitude
beta_vec = [2; -4; 2];  % beta vector

% Step 2: Solve
r = poynting_pw('time', a, b, E0, beta_vec);

% Console shows:
% ==========================================
%    PLANE WAVE: H-FIELD & POYNTING (Q22-Q23)
% ==========================================
%   Ẽ₀ = [20.0-0.0j; 10.0+10.0j; 0.0+20.0j] V/m
%   k̂ = [0.4082, -0.8165, 0.4082]
%   η = 377 Ω
% ------------------------------------------
%   Q22: H̃₀ = (1/η)·k̂ × Ẽ₀
%   H̃₀ = [42.17+0.00j; 10.54-21.08j; -47.71+21.08j] mA/m
% ------------------------------------------
%   Q23: S̄ = ½·Re{Ẽ × H̃*}
%   S̄ = [54.110; -108.220; 54.110] W/m²
%   |S̄| = 132.583 W/m²
% ==========================================

% Step 3: Extract answers
>> r.H_phasor
ans =
   0.0422 + 0.0000i
   0.0105 - 0.0211i
  -0.0477 + 0.0211i

% Note: Values in A/m, multiply by 1000 for mA/m
% Or read from console (already shows mA/m)

>> r.S_avg
ans =
   54.110
 -108.220
   54.110
```

---

## What You Get Back

```matlab
r = poynting_pw('time', a, b, E0, beta_vec);

% Core outputs (Q22-Q23)
r.H_phasor    % H-field phasor [A/m] (×1000 for mA/m)
r.S_avg       % Poynting vector [W/m²]
r.S_mag       % |S̄| magnitude [W/m²]

% Additional info
r.E_phasor    % E-field phasor [V/m]
r.k_hat       % Propagation direction
r.eta         % Intrinsic impedance [Ω]
r.beta_vec    % Beta vector [rad/m]
r.beta_mag    % |β| [rad/m]
```

---

## Key Conversions

### Time-Domain → Phasor
```
E(t) = E₀(a·cos(ψ) + b·sin(ψ))

Phasor: Ẽ = E₀(a - jb)
```

### Example
```
E = 10([2;1;0]cos + [0;-1;-2]sin)

Ẽ = 10([2;1;0] - j[0;-1;-2])
  = 10[2; 1+j; 2j]
  = [20; 10+10j; 20j] V/m
```

---

## Common Mistakes

### ❌ Mistake 1: Wrong Sign in Conversion

```matlab
❌ Wrong:
E_phasor = E0 * (a + 1j*b);  % Plus sign!

✅ Correct:
E_phasor = E0 * (a - 1j*b);  % Minus sign!
```

**Rule:** Ẽ = E₀(a - jb), not (a + jb)

---

### ❌ Mistake 2: Wrong Vector Type

```matlab
❌ Wrong:
a = [2, 1, 0];  % Row vector (commas)

✅ Correct:
a = [2; 1; 0];  % Column vector (semicolons)
```

---

### ❌ Mistake 3: Swapping a and b

```matlab
% Given: E = E₀([2;1;0]cos + [0;-1;-2]sin)

❌ Wrong:
a = [0; -1; -2];   % These are sine coeffs!
b = [2; 1; 0];     % These are cosine coeffs!

✅ Correct:
a = [2; 1; 0];     % Cosine coefficients
b = [0; -1; -2];   % Sine coefficients
```

---

### ❌ Mistake 4: Forgetting 'time' Keyword

```matlab
❌ Wrong:
r = poynting_pw(a, b, E0, beta_vec);

✅ Correct:
r = poynting_pw('time', a, b, E0, beta_vec);
```

---

## Quick Formulas

### H from E
```
H̃ = (1/η) · k̂ × Ẽ
```

### Poynting Vector
```
S̄ = ½ · Re{Ẽ × H̃*}
```

### k̂ from β
```
k̂ = β/|β|
```

---

## Units Reference

| Quantity | Given Units | Output Units |
|----------|-------------|--------------|
| E₀ | V/m | - |
| Ẽ | V/m | V/m |
| H̃ | - | A/m (console: mA/m) |
| β | rad/m | rad/m |
| S̄ | - | W/m² |
| η | - | Ω (default 377) |

**Note:** Console displays H in mA/m, but `r.H_phasor` is in A/m. Multiply by 1000 if needed.

---

## Quick Cheat Sheet

### Q22-Q23 One-Liner
```matlab
% Extract a, b, E0, beta_vec from problem
r = poynting_pw('time', a, b, E0, beta_vec);
% Read console for answers in correct units
```

### Alternative: Direct Phasor
```matlab
% If you already have E phasor
r = poynting_pw(E_phasor, k_hat);
% Or specify eta:
r = poynting_pw(E_phasor, k_hat, eta);
```

---

## ✅ 60-Second Self-Test

**Given:**
```
E = 5([1;0;1]cos(ψ) + [0;1;0]sin(ψ)) V/m
β = (3, 0, 3) rad/m
```

**Try solving (without looking):**
```matlab
a = ?
b = ?
E0 = ?
beta_vec = ?

r = poynting_pw('time', a, b, E0, beta_vec);
```

**Answers:**
```matlab
a = [1; 0; 1];
b = [0; 1; 0];
E0 = 5;
beta_vec = [3; 0; 3];

r = poynting_pw('time', a, b, E0, beta_vec);
```

---

## 🎯 What's Next?

**Ready for exam:**
→ Print the [Quick Reference Card](poynting_pw_Quick_Reference.md) (1 min)

**Want more practice:**
→ Work through [Exam Examples](poynting_pw_Exam_Examples.md) (10 min)

**Need theory:**
→ Read the [Complete Guide](poynting_pw_Complete_Guide.md) (20 min)

**Having issues:**
→ Check [Troubleshooting Guide](poynting_pw_Troubleshooting.md) (3 min)

---

## 💡 Remember

1. **One call solves Q22 AND Q23**
2. **Conversion:** Ẽ = E₀(a - jb) [MINUS sign]
3. **a = cosine coeffs, b = sine coeffs**
4. **Console shows answers in exam units**
5. **Default η = 377 Ω for air**

**You're ready for Q22-Q23!** 🚀

---

[← Back to Master Index](poynting_pw_MASTER_INDEX.md) | [Complete Guide →](poynting_pw_Complete_Guide.md)
