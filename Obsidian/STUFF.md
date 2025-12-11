
pin: 57165

---

## Intrinsic Impedance of Air

**Definition**  
The _intrinsic impedance_ of a medium is

$$  
\eta = \sqrt{\frac{\mu}{\varepsilon}}  
$$

It expresses the ratio between the electric and magnetic fields in a uniform plane wave.

---

### Air ≈ Vacuum

For practical engineering work:

- $\varepsilon_r \approx 1$
    
- $\mu_r \approx 1$
    

Therefore, air has (almost) the same intrinsic impedance as vacuum.

---

### Numerical Value

$$  
\eta_0 = \sqrt{\frac{\mu_0}{\varepsilon_0}}  
\approx 376.730313668~\Omega \approx 377~\Omega  
$$

---

### Interpretation

- The intrinsic impedance tells us the ratio $E/H$ in a plane wave traveling in air.
    
- It is essential when computing reflection coefficients, Poynting vectors, and general wave propagation behavior.
    

---
# Gamma ↔ Impedance Conversion - Quick Reference

## 🎯 The Two Fundamental Formulas

### From Impedance to Gamma

```
Γ = (Z - Z₀)/(Z + Z₀)
```

### From Gamma to Impedance

```
Z = Z₀ · (1 + Γ)/(1 - Γ)
```

**These are inverses of each other!**

---

## 📐 Step-by-Step: Γ → Z (Q14 Type)

### Given

- Γ = 0.539∠22°
- Z₀ = 75 Ω

### Method 1: Rectangular Form (Most Common)

**Step 1: Convert Γ to rectangular**

```
Γ = 0.539∠22°
  = 0.539(cos 22° + j sin 22°)
  = 0.4998 + j0.2019
```

**Step 2: Calculate numerator (1 + Γ)**

```
1 + Γ = 1 + (0.4998 + j0.2019)
      = 1.4998 + j0.2019
```

**Step 3: Calculate denominator (1 - Γ)**

```
1 - Γ = 1 - (0.4998 + j0.2019)
      = 0.5002 - j0.2019    ← Note: sign change on imaginary!
```

**Step 4: Divide using conjugate method**

```
Conjugate of (0.5002 - j0.2019) = 0.5002 + j0.2019

Numerator × conjugate:
  (1.4998 + j0.2019)(0.5002 + j0.2019) = 0.7094 + j0.4038

Denominator × conjugate:
  (0.5002)² + (0.2019)² = 0.2910

Division: (0.7094 + j0.4038)/0.2910 = 2.438 + j1.387
```

**Step 5: Multiply by Z₀**

```
Z = 75 × (2.438 + j1.387)
  = 182.85 + j104.03 Ω
  ≈ 183 + j104 Ω ✓
```

### Method 2: Polar Form (Alternative)

**Step 1: Convert to polar**

```
1 + Γ = 1.4998 + j0.2019 = 1.513∠7.67°
1 - Γ = 0.5002 - j0.2019 = 0.539∠-22.0°
```

**Step 2: Divide in polar**

```
(1 + Γ)/(1 - Γ) = (1.513∠7.67°)/(0.539∠-22.0°)
                = (1.513/0.539)∠(7.67° - (-22.0°))
                = 2.805∠29.67°
```

**Step 3: Multiply by Z₀**

```
Z = 75 × 2.805∠29.67°
  = 210.4∠29.67° Ω
```

**Step 4: Convert back to rectangular**

```
Z = 210.4(cos 29.67° + j sin 29.67°)
  = 183 + j104 Ω ✓
```

---

## 📐 Step-by-Step: Z → Γ (Reverse)

### Given

- Z = 183 + j104 Ω
- Z₀ = 75 Ω

### Method: Rectangular Form

**Step 1: Calculate numerator (Z - Z₀)**

```
Z - Z₀ = (183 + j104) - 75
       = 108 + j104
```

**Step 2: Calculate denominator (Z + Z₀)**

```
Z + Z₀ = (183 + j104) + 75
       = 258 + j104
```

**Step 3: Divide using conjugate**

```
Conjugate of (258 + j104) = 258 - j104

Numerator × conjugate:
  (108 + j104)(258 - j104) = 38664 + j15576

Denominator × conjugate:
  258² + 104² = 77380

Division: (38664 + j15576)/77380 = 0.4998 + j0.2013
```

**Step 4: Convert to polar (optional)**

```
Γ = 0.4998 + j0.2013
  = 0.539∠22.0° ✓
```

---

## 🔢 Complex Division Cheat Sheet

### The Conjugate Method

**To divide (a + jb)/(c + jd):**

1. **Find conjugate** of denominator: (c - jd)
    
2. **Multiply both** numerator and denominator by conjugate:
    
    ```
    (a + jb)(c - jd)
    ───────────────
    (c + jd)(c - jd)
    ```
    
3. **Numerator** (FOIL method):
    
    ```
    Real part:      a×c - b×d
    Imaginary part: a×d + b×c
    ```
    
4. **Denominator** (always real!):
    
    ```
    c² + d²
    ```
    
5. **Final result:**
    
    ```
    (ac - bd) + j(ad + bc)
    ─────────────────────
          c² + d²
    ```
    

### Example: (1.4998 + j0.2019)/(0.5002 - j0.2019)

```
a = 1.4998,  b = 0.2019
c = 0.5002,  d = -0.2019

Conjugate: (0.5002 + j0.2019)

Numerator:
  Real: 1.4998×0.5002 - 0.2019×0.2019 = 0.7094
  Imag: 1.4998×0.2019 + 0.2019×0.5002 = 0.4038
  Result: 0.7094 + j0.4038

Denominator:
  0.5002² + 0.2019² = 0.2910

Final:
  (0.7094 + j0.4038)/0.2910 = 2.438 + j1.387 ✓
```

---

## 💻 MATLAB One-Liners

### Γ → Z

```matlab
% Given
Gamma = 0.539 * exp(1j*deg2rad(22));
Z0 = 75;

% Calculate
Z = Z0 * (1 + Gamma) / (1 - Gamma);
% Result: Z = 182.8 + j104.1 Ω

% Or use TLine:
r = TLine('Z', Z0, Gamma);
Z = r.Z;
```

### Z → Γ

```matlab
% Given
Z = 183 + 1j*104;
Z0 = 75;

% Calculate
Gamma = (Z - Z0) / (Z + Z0);
% Result: Gamma = 0.4998 + j0.2013 = 0.539∠22.0°

% Or use TLine:
r = TLine('Gamma', Z0, Z);
Gamma = r.Gamma;
```

---

## ⚠️ Common Mistakes Checklist

### Converting Γ → Z

- [ ] ❌ Using (1 - Γ)/(1 + Γ) instead of (1 + Γ)/(1 - Γ)
- [ ] ❌ Forgetting to change sign: 1 - (a + jb) = (1-a) - jb, not (1-a) + jb
- [ ] ❌ Not using conjugate method for complex division
- [ ] ❌ Forgetting to multiply by Z₀ at the end
- [ ] ❌ Using Γ_A when you need Γ_L (or vice versa)

### Converting Z → Γ

- [ ] ❌ Using (Z + Z₀)/(Z - Z₀) instead of (Z - Z₀)/(Z + Z₀)
- [ ] ❌ Wrong sign in subtraction
- [ ] ❌ Not normalizing angle to (-180°, 180°]

---

## 📊 Quick Verification Table

|Input|Expected Output|Check|
|---|---|---|
|Γ = 0|Z = Z₀|Matched load|
|Γ = 1|Z = ∞|Open circuit|
|Γ = -1|Z = 0|Short circuit|
|Γ = 0.5∠0°|Z = 3Z₀|Real, high Z|
|Γ = 0.5∠180°|Z = Z₀/3|Real, low Z|

**Use these to check your formulas!**

---

## 🎨 Visual Flow Chart

```
Γ → Z Conversion:
─────────────────

Γ (polar)
    ↓
Convert to rectangular
    ↓
Calculate 1 + Γ
Calculate 1 - Γ
    ↓
Divide (using conjugate)
    ↓
Multiply by Z₀
    ↓
Z (rectangular)
    ↓
Convert to polar (optional)
```

```
Z → Γ Conversion:
─────────────────

Z (any form)
    ↓
Calculate Z - Z₀
Calculate Z + Z₀
    ↓
Divide (using conjugate)
    ↓
Γ (rectangular)
    ↓
Convert to polar (optional)
```

---

## 📝 Complete Example Walkthrough

### Problem

Given Γ_L = 0.539∠22° at the load, Z₀ = 75 Ω.  
Find Z_L.

### Solution

```
Step 1: Γ → rectangular
  Γ = 0.539(cos 22° + j sin 22°)
    = 0.4998 + j0.2019

Step 2: Numerator
  1 + Γ = 1.4998 + j0.2019

Step 3: Denominator  
  1 - Γ = 0.5002 - j0.2019

Step 4: Divide
  Using conjugate (0.5002 + j0.2019):
  
  Num × conj = (0.7094 + j0.4038)
  Den × conj = 0.2910
  
  Result = 2.438 + j1.387

Step 5: Multiply by Z₀
  Z = 75(2.438 + j1.387)
    = 183 + j104 Ω ✓
```

### Verify with MATLAB

```matlab
Gamma = 0.539*exp(1j*deg2rad(22));
Z = 75*(1+Gamma)/(1-Gamma);
fprintf('Z = %.0f + j%.0f Ω\n', real(Z), imag(Z));
% Output: Z = 183 + j104 Ω ✓
```

---

## 🔑 Key Takeaways

1. **Remember the formulas:**
    
    - Γ → Z: `Z = Z₀(1 + Γ)/(1 - Γ)`
    - Z → Γ: `Γ = (Z - Z₀)/(Z + Z₀)`
2. **Use conjugate method** for complex division
    
3. **Watch the signs** especially in (1 - Γ)
    
4. **Verify** with MATLAB or TLine.m
    
5. **Check limits** (Γ=0 → Z=Z₀, etc.)
    

---

_Keep this card for all Γ ↔ Z conversion problems!_ 📌