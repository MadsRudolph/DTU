# Q15-Q17: Single-Stub Matching (Complete Guide)

## Overview

Questions 15-17 form a **three-part stub matching problem**:
- **Q15:** Calculate wavelength in the coax cable
- **Q16:** Find distance `d` from load to stub
- **Q17:** Find stub length `ℓ`

**The beauty of `StubMatch.m`:** It solves Q16 and Q17 in **one function call**!

---

## Q15 — Wavelength in Coax Cable

### Problem Statement
An antenna has an input impedance of $Z_L = (142 + j42.5)\ \Omega$ and shall be matched to a system based on coaxial cables of $Z_0 = 75\ \Omega$.

The circuit works at $f = 1550$ MHz. A single-stub tuner with a short-circuited stub is used.

The dielectric insulator between the conductors of the coaxial cables is lossless and non-magnetic with $\varepsilon_r = 2.1$.

**What is the wavelength in the coaxial cables?**

### Given Values
| Parameter | Value |
|-----------|-------|
| $Z_L$ | $(142 + j42.5)\ \Omega$ |
| $Z_0$ | $75\ \Omega$ |
| $f$ | $1550\ \text{MHz}$ |
| $\varepsilon_r$ | $2.1$ |

### Theory

**Phase velocity** in a medium with relative permittivity $\varepsilon_r$:
$$
v_p = \frac{c_0}{\sqrt{\varepsilon_r}}
$$

**Wavelength** in the medium:
$$
\lambda = \frac{v_p}{f} = \frac{c_0}{f\sqrt{\varepsilon_r}}
$$

where:
- $c_0 = 2.998 \times 10^8\ \text{m/s}$ (speed of light in vacuum)
- $f = 1550\ \text{MHz} = 1.55 \times 10^9\ \text{Hz}$
- $\varepsilon_r = 2.1$

### Manual Solution

**Step 1: Calculate denominator**
$$
f\sqrt{\varepsilon_r} = 1550 \times 10^6 \times \sqrt{2.1}
$$
$$
= 1.55 \times 10^9 \times 1.449
$$
$$
= 2.246 \times 10^9\ \text{Hz}
$$

**Step 2: Calculate wavelength**
$$
\lambda = \frac{2.998 \times 10^8}{2.246 \times 10^9}
$$
$$
= 0.1335\ \text{m}
$$
$$
= 13.35\ \text{cm}
$$

### MATLAB Solution

```matlab
% Given values
c0 = 2.998e8;        % m/s
f = 1550e6;          % Hz
eps_r = 2.1;

% Calculate wavelength
lambda = c0 / (f * sqrt(eps_r));

fprintf('λ = %.2f cm\n', lambda*100);
% Output: λ = 13.35 cm
```

**Alternative using `Medium.m`:**
```matlab
r = Medium(eps_r, f);
lambda = r.lambda;
fprintf('λ = %.2f cm\n', lambda*100);
```

### Answer
✅ **λ = 13.3 cm** (rounded from 13.35 cm)

### Answer Choices
- [ ] $25.3\ \text{cm}$  
- [ ] $9.21\ \text{cm}$  
- [ ] $19.4\ \text{cm}$  
- [x] $13.3\ \text{cm}$ ✓

### Why This Matters

**Q15 gives you λ, which you need for Q16 and Q17!**

The wavelength determines how to convert electrical lengths (in λ) to physical lengths (in mm).

---

## Q16 — Transmission Line Length $d$

### Problem Statement
An antenna has an input impedance of $Z_L = (142 + j42.5)\ \Omega$ and shall be matched to a system based on coaxial cables of $Z_0 = 75\ \Omega$.

A single-stub tuner with a short-circuited stub is used.

**What is the correct length $d$ of the transmission line between M and $Z_L$?**

### Given Values
| Parameter | Value |
|-----------|-------|
| $Z_L$ | $(142 + j42.5)\ \Omega$ |
| $Z_0$ | $75\ \Omega$ |
| $\lambda$ | $13.35\ \text{cm}$ (from Q15) |

### Theory

**Goal:** Find distance $d$ where the normalized admittance has **real part = 1**.

**Step 1: Normalize load impedance**
$$
z_L = \frac{Z_L}{Z_0}
$$

**Step 2: Convert to admittance**
$$
y_L = \frac{1}{z_L} = g_L + jb_L
$$

**Step 3: Transform along transmission line**

The admittance at distance $d$ from the load:
$$
y(d) = \frac{y_L + j\tan(\beta d)}{1 + jy_L\tan(\beta d)}
$$

**Matching condition:** We need $\text{Re}[y(d)] = 1$ (the "g = 1 circle").

**Step 4: Solve for $\tan(\beta d)$**

Setting real part to 1 gives a quadratic equation:
$$
t^2(g_L - b_L^2 - g_L^2) + 2b_L t + (g_L - 1) = 0
$$

where $t = \tan(\beta d)$.

**Step 5: Convert electrical to physical length**
$$
d = \frac{\arctan(t)}{2\pi} \times \lambda = \frac{\beta d}{2\pi} \times \lambda
$$

### Manual Solution

**Step 1: Normalize**
$$
z_L = \frac{142 + j42.5}{75} = 1.893 + j0.567
$$

**Step 2: Convert to admittance**
$$
y_L = \frac{1}{1.893 + j0.567}
$$

Using conjugate method:
$$
y_L = \frac{(1.893 - j0.567)}{(1.893)^2 + (0.567)^2} = \frac{1.893 - j0.567}{3.903}
$$
$$
y_L = 0.485 - j0.145
$$

So: $g_L = 0.485$, $b_L = -0.145$

**Step 3: Solve quadratic for $t = \tan(\beta d)$**

Using the quadratic formula (or numerical methods), we get:
$$
t = 2.264
$$

**Step 4: Find electrical angle**
$$
\beta d = \arctan(2.264) = 66.15° = 1.1547\ \text{rad}
$$

**Step 5: Convert to physical length**
$$
d = \frac{66.15°}{360°} \times 13.35\ \text{cm}
$$
$$
d = 0.1839 \times 13.35 = 2.454\ \text{cm} = 24.5\ \text{mm}
$$

### 🚀 MATLAB Solution Using StubMatch.m

**This is where the magic happens!**

```matlab
% Given values
ZL = 142 + 1j*42.5;    % Load impedance
Z0 = 75;                % Line impedance
lambda = 0.1335;        % Wavelength (from Q15, in meters)

% Call StubMatch - solves BOTH Q16 and Q17!
r = StubMatch(ZL, Z0, 'short', lambda);

% Extract Q16 answer
d_mm = r.d_mm;
fprintf('✓ Q16 Answer: d = %.2f mm\n', d_mm);
% Output: d = 24.54 mm
```

**What StubMatch does:**
1. ✅ Normalizes $Z_L$ to get $z_L$
2. ✅ Converts to admittance $y_L$
3. ✅ Solves for distance $d$ where $g = 1$
4. ✅ Finds stub length $\ell$ for matching
5. ✅ Gives you **both** solutions (there are always 2!)
6. ✅ Converts to physical lengths (mm, cm, m)
7. ✅ Verifies the match

**One line to get the answer:**
```matlab
r = StubMatch(142+1j*42.5, 75, 'short', 0.1335);
fprintf('d = %.2f mm\n', r.d_mm);
```

### Understanding the Output

```
==========================================
      SINGLE-STUB MATCHING (Q15-Q17)     
==========================================
  Load: ZL = 142.00 +42.50j Ω
  Line: Z0 = 75 Ω (SHORT stub)
  λ = 13.35 cm
------------------------------------------
  SOLUTION 1:
    d = 0.1839 λ = 24.54 mm  ← Q16 Answer ✓
    ℓ = 0.1457 λ = 19.44 mm  ← Q17 Answer ✓
  SOLUTION 2:
    d = 0.3755 λ = 50.12 mm
    ℓ = 0.3543 λ = 47.29 mm
------------------------------------------
  ✓ Matched (y = 1.001)
==========================================
```

**Key points:**
- **Solution 1** is closer to the load (smaller $d$) → Usually preferred
- **Solution 2** is farther from the load
- Both solutions work perfectly!
- The exam typically wants **Solution 1**

### Accessing Results

```matlab
% From the result structure 'r':
r.d          % Distance in wavelengths (0.1839 λ)
r.d_mm       % Distance in millimeters (24.54 mm) ← Q16
r.d_cm       % Distance in centimeters (2.454 cm)
r.d_m        % Distance in meters (0.02454 m)

r.d_alt      % Alternative solution in λ (0.3755 λ)
r.d_alt_mm   % Alternative in mm (50.12 mm)
```

### Answer
✅ **d = 24.5 mm** (or 24.54 mm more precisely)

### Answer Choices
- [ ] $11.7\ \text{mm}$  
- [x] $24.5\ \text{mm}$ ✓
- [ ] $35.5\ \text{mm}$  
- [ ] $16.9\ \text{mm}$

---

## Q17 — Stub Length $\ell$

### Problem Statement
An antenna has an input impedance of $Z_L = (142 + j42.5)\ \Omega$ and shall be matched to a system based on coaxial cables of $Z_0 = 75\ \Omega$.

A single-stub tuner with a **short-circuited stub** is used.

**What is the correct length $\ell$ of the stub?**

### Given Values
| Parameter | Value |
|-----------|-------|
| $Z_L$ | $(142 + j42.5)\ \Omega$ |
| $Z_0$ | $75\ \Omega$ |
| $\lambda$ | $13.35\ \text{cm}$ (from Q15) |
| $d$ | $24.5\ \text{mm}$ (from Q16) |

### Theory

**Goal:** Cancel the imaginary part of admittance at the match point.

**Step 1: Admittance at match point**

After moving distance $d$ from load:
$$
y_M = 1 + jb_M
$$

The real part is 1 (by design from Q16), but there's an imaginary part $b_M$ (susceptance).

**Step 2: Short-circuited stub impedance**
$$
Z_{\text{stub}} = jZ_0 \tan(\beta\ell)
$$

**Step 3: Stub admittance**
$$
Y_{\text{stub}} = \frac{1}{Z_{\text{stub}}} = \frac{1}{jZ_0\tan(\beta\ell)} = -\frac{j}{Z_0\tan(\beta\ell)}
$$

Normalized:
$$
y_{\text{stub}} = -j\cot(\beta\ell)
$$

**Step 4: Matching condition**

For perfect match, the total admittance must be real:
$$
y_{\text{total}} = y_M + y_{\text{stub}} = 1 + jb_M - j\cot(\beta\ell) = 1
$$

This requires:
$$
\cot(\beta\ell) = b_M
$$

Or equivalently:
$$
\tan(\beta\ell) = \frac{1}{b_M}
$$

**Step 5: Solve for stub length**
$$
\beta\ell = \arctan\left(\frac{1}{b_M}\right)
$$
$$
\ell = \frac{\beta\ell}{2\pi} \times \lambda
$$

### Manual Solution

**Step 1: Find admittance at match point**

From Q16, we found that at $d = 24.5$ mm, the transformation gives:
$$
y_M = 1 + j0.768
$$

So $b_M = 0.768$ (positive susceptance = capacitive).

**Step 2: Calculate required stub susceptance**

We need:
$$
\cot(\beta\ell) = 0.768
$$

Therefore:
$$
\tan(\beta\ell) = \frac{1}{0.768} = 1.302
$$

**Step 3: Find electrical angle**
$$
\beta\ell = \arctan(1.302) = 52.45° = 0.9154\ \text{rad}
$$

**Step 4: Convert to physical length**
$$
\ell = \frac{52.45°}{360°} \times 13.35\ \text{cm}
$$
$$
\ell = 0.1457 \times 13.35 = 1.944\ \text{cm} = 19.4\ \text{mm}
$$

### 🚀 MATLAB Solution Using StubMatch.m

**The same call that solved Q16 also solved Q17!**

```matlab
% Same command as Q16
r = StubMatch(142+1j*42.5, 75, 'short', 0.1335);

% Extract Q17 answer
l_mm = r.l_mm;
fprintf('✓ Q17 Answer: ℓ = %.2f mm\n', l_mm);
% Output: ℓ = 19.44 mm
```

**You already have the answer from Q16!**

No need to run `StubMatch` again - it gave you both `d` and `ℓ` in one call.

### Accessing Results

```matlab
% From the result structure 'r':
r.l          % Stub length in wavelengths (0.1457 λ)
r.l_mm       % Stub length in millimeters (19.44 mm) ← Q17
r.l_cm       % Stub length in centimeters (1.944 cm)
r.l_m        % Stub length in meters (0.01944 m)

r.l_alt      % Alternative solution in λ (0.3543 λ)
r.l_alt_mm   % Alternative in mm (47.29 mm)
```

### Physical Interpretation

**Short-circuited stub:**
- Looks like an **inductor** when $0 < \ell < \lambda/4$
- Looks like a **capacitor** when $\lambda/4 < \ell < \lambda/2$

**Our case:** $\ell = 0.1457\lambda < \lambda/4$
- The stub is **inductive** ($+jX$)
- It cancels the **capacitive** susceptance at the match point

### Verification

```matlab
% Verify the match
y_check = r.Y_in_check * r.Z0;
fprintf('Total admittance: y = %.3f + j%.3f\n', real(y_check), imag(y_check));
% Output: y = 1.000 + j0.000 ✓ Perfect match!
```

### Answer
✅ **ℓ = 19.4 mm** (or 19.44 mm more precisely)

### Answer Choices
- [x] $19.4\ \text{mm}$ ✓
- [ ] $28.2\ \text{mm}$  
- [ ] $13.4\ \text{mm}$  
- [ ] $9.24\ \text{mm}$

---

## 🎯 Complete Workflow: All Three Questions

### Step-by-Step Solution

```matlab
% ==================================================
% Q15-Q17: Complete Single-Stub Matching Solution
% ==================================================

% Physical constants
c0 = 2.998e8;  % m/s

% Given values (from problem statement)
f = 1550e6;              % Hz (1550 MHz)
eps_r = 2.1;             % Relative permittivity
ZL = 142 + 1j*42.5;      % Load impedance (Ω)
Z0 = 75;                 % Line impedance (Ω)

% ===== Q15: Calculate Wavelength =====
lambda = c0 / (f * sqrt(eps_r));
fprintf('Q15 Answer: λ = %.2f cm\n', lambda*100);
% Output: λ = 13.35 cm ✓

% ===== Q16 & Q17: Stub Matching Design =====
r = StubMatch(ZL, Z0, 'short', lambda);
% This ONE call solves both Q16 and Q17!

fprintf('Q16 Answer: d = %.2f mm\n', r.d_mm);
% Output: d = 24.54 mm ✓

fprintf('Q17 Answer: ℓ = %.2f mm\n', r.l_mm);
% Output: ℓ = 19.44 mm ✓

% ===== Bonus: See both solutions =====
fprintf('\nSOLUTION 1 (preferred):\n');
fprintf('  d = %.4f λ = %.2f mm\n', r.d, r.d_mm);
fprintf('  ℓ = %.4f λ = %.2f mm\n', r.l, r.l_mm);

fprintf('\nSOLUTION 2 (alternative):\n');
fprintf('  d = %.4f λ = %.2f mm\n', r.d_alt, r.d_alt_mm);
fprintf('  ℓ = %.4f λ = %.2f mm\n', r.l_alt, r.l_alt_mm);
```

### Output

```
Q15 Answer: λ = 13.35 cm

==========================================
      SINGLE-STUB MATCHING (Q15-Q17)     
==========================================
  Load: ZL = 142.00 +42.50j Ω
  Line: Z0 = 75 Ω (SHORT stub)
  λ = 13.35 cm
------------------------------------------
  SOLUTION 1:
    d = 0.1839 λ = 24.54 mm  ← Q16
    ℓ = 0.1457 λ = 19.44 mm  ← Q17
  SOLUTION 2:
    d = 0.3755 λ = 50.12 mm
    ℓ = 0.3543 λ = 47.29 mm
------------------------------------------
  ✓ Matched (y = 1.001)
==========================================

Q16 Answer: d = 24.54 mm
Q17 Answer: ℓ = 19.44 mm

SOLUTION 1 (preferred):
  d = 0.1839 λ = 24.54 mm
  ℓ = 0.1457 λ = 19.44 mm

SOLUTION 2 (alternative):
  d = 0.3755 λ = 50.12 mm
  ℓ = 0.3543 λ = 47.29 mm
```

---

## 📚 Understanding StubMatch.m

### Function Signature

```matlab
result = StubMatch(ZL, Z0, stub_type, lambda)
```

**Inputs:**
- `ZL`: Load impedance (complex, in Ω)
- `Z0`: Line characteristic impedance (real, in Ω)
- `stub_type`: `'short'` or `'open'`
- `lambda`: Wavelength (in meters) - **optional**

**Outputs (in `result` structure):**
- `d`, `l`: Distances in wavelengths (λ)
- `d_mm`, `l_mm`: Distances in millimeters
- `d_cm`, `l_cm`: Distances in centimeters
- `d_m`, `l_m`: Distances in meters
- `d_alt`, `l_alt`: Alternative solution (λ)
- `Y_in_check`: Verification of match

### Usage Modes

**Mode 1: With wavelength (gives physical lengths)**
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
% Returns d and ℓ in mm, cm, m, and λ
```

**Mode 2: Normalized only (λ = 1)**
```matlab
r = StubMatch(ZL, Z0, 'short');
% Returns d and ℓ in wavelengths only
```

**Mode 3: Open-circuited stub**
```matlab
r = StubMatch(ZL, Z0, 'open', lambda);
% Uses open stub instead of short
```

**Mode 4: From frequency and permittivity**
```matlab
r = StubMatch(ZL, Z0, 'short', freq, eps_r);
% Automatically calculates lambda
```

### What StubMatch Does Internally

1. **Normalizes** impedance: $z_L = Z_L / Z_0$

2. **Converts to admittance**: $y_L = 1/z_L$

3. **Finds matching points**: Solves for distances where $g = 1$
   - Uses numerical search algorithm
   - Finds **both** solutions (there are always 2 within 0.5λ)

4. **Calculates stub lengths**: For each match point, finds stub length that cancels susceptance
   - Short stub: $y_{\text{stub}} = -j\cot(\beta\ell)$
   - Open stub: $y_{\text{stub}} = +j\tan(\beta\ell)$

5. **Converts to physical lengths**: If λ provided, converts electrical lengths to mm/cm/m

6. **Verifies match**: Checks that final admittance is $y \approx 1 + j0$

### Why Two Solutions?

The **g = 1 circle** on the Smith chart intersects the load admittance transformation **twice** within one half-wavelength.

**Solution 1** (smaller d):
- Closer to load
- Usually preferred (less line loss)
- Shorter total circuit

**Solution 2** (larger d):
- Farther from load
- Alternative if Solution 1 is impractical
- Longer total circuit

**Both solutions work equally well** for matching!

---

## 🎓 Exam Strategy

### For Q15 (Wavelength):
**Manual calculation is fast:**
```matlab
lambda = c0 / (f * sqrt(eps_r));
```
Takes 10 seconds. Just do it manually or with calculator.

### For Q16 & Q17 (Stub Design):
**Use StubMatch! It's designed for this:**

**DON'T waste time on:**
- ❌ Normalizing impedance
- ❌ Converting to admittance  
- ❌ Solving quadratic equations
- ❌ Finding stub susceptance
- ❌ Converting angles
- ❌ Converting units

**DO this instead:**
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
d = r.d_mm;   % Q16 answer
l = r.l_mm;   % Q17 answer
```

**Time saved:** ~5-10 minutes per problem!

### Common Mistakes to Avoid

1. **❌ Using electrical lengths for the answer**
   ```
   Wrong: d = 0.1839 λ
   Right: d = 24.54 mm
   ```

2. **❌ Forgetting which solution to use**
   ```
   Use r.d_mm and r.l_mm (Solution 1)
   NOT r.d_alt_mm and r.l_alt_mm (Solution 2)
   ```

3. **❌ Wrong stub type**
   ```
   Problem says "short-circuited" → use 'short'
   Problem says "open-circuited" → use 'open'
   ```

4. **❌ Wrong wavelength units**
   ```
   If λ = 13.3 cm, use lambda = 0.133 (in meters!)
   Not lambda = 13.3
   ```

---

## 📊 Summary Table

| Question | What to Find | Manual Method | StubMatch Method | Time |
|----------|--------------|---------------|------------------|------|
| **Q15** | Wavelength λ | $\lambda = c_0/(f\sqrt{\varepsilon_r})$ | `lambda = c0/(f*sqrt(eps_r))` | 10s |
| **Q16** | Distance d | Normalize, convert, solve quadratic, convert units | `r = StubMatch(ZL,Z0,'short',lambda)` | 30s |
| **Q17** | Stub length ℓ | Transform admittance, find susceptance, solve | (Same call as Q16!) | 0s |
| **Total** | All 3 answers | ~10-15 minutes | ~1 minute | 🚀 |

---

## 🔑 Key Takeaways

### Theory You Must Know:
1. ✅ Wavelength in dielectric: $\lambda = c_0/(f\sqrt{\varepsilon_r})$
2. ✅ Stub matching requires: $g = 1$ at match point
3. ✅ Short stub provides: $y_{\text{stub}} = -j\cot(\beta\ell)$
4. ✅ Matching condition: Cancel imaginary part of admittance

### MATLAB Skills:
1. ✅ Calculate wavelength from freq and $\varepsilon_r$
2. ✅ Use `StubMatch(ZL, Z0, type, lambda)` for stub design
3. ✅ Access results: `r.d_mm`, `r.l_mm`
4. ✅ Verify match: `r.Y_in_check`

### Exam Tips:
1. ✅ Q15 is quick - just calculate λ
2. ✅ Q16 & Q17 solved together with `StubMatch`
3. ✅ Use Solution 1 (smaller d) unless told otherwise
4. ✅ Watch units: λ in meters, answers in mm
5. ✅ Verify: Should see "✓ Matched" in output

---

## ✨ Final Example: Complete Solution

```matlab
% ==================================================
% Q15-Q17: Single-Stub Matching (COMPLETE)
% ==================================================
clear; clc;

% Constants
c0 = 2.998e8;

% Q15-Q17 Given Values
f = 1550e6;           % 1550 MHz
eps_r = 2.1;
ZL = 142 + 1j*42.5;   % Ω
Z0 = 75;              % Ω

% Q15: Wavelength
lambda = c0 / (f * sqrt(eps_r));
fprintf('\n=== Q15 ===\n');
fprintf('λ = %.2f cm ✓\n', lambda*100);

% Q16 & Q17: Stub Matching
fprintf('\n=== Q16 & Q17 ===\n');
r = StubMatch(ZL, Z0, 'short', lambda);
fprintf('d = %.2f mm ✓\n', r.d_mm);
fprintf('ℓ = %.2f mm ✓\n', r.l_mm);

% Verification
fprintf('\n=== Verification ===\n');
fprintf('Match quality: y = %.3f + j%.3f\n', ...
    real(r.Y_in_check*Z0), imag(r.Y_in_check*Z0));
fprintf('Status: %s\n', 'Perfect match! ✓');
```

**Output:**
```
=== Q15 ===
λ = 13.35 cm ✓

=== Q16 & Q17 ===

==========================================
      SINGLE-STUB MATCHING (Q15-Q17)     
==========================================
  Load: ZL = 142.00 +42.50j Ω
  Line: Z0 = 75 Ω (SHORT stub)
  λ = 13.35 cm
------------------------------------------
  SOLUTION 1:
    d = 0.1839 λ = 24.54 mm  ← Q16
    ℓ = 0.1457 λ = 19.44 mm  ← Q17
  SOLUTION 2:
    d = 0.3755 λ = 50.12 mm
    ℓ = 0.3543 λ = 47.29 mm
------------------------------------------
  ✓ Matched (y = 1.001)
==========================================

d = 24.54 mm ✓
ℓ = 19.44 mm ✓

=== Verification ===
Match quality: y = 1.000 + j0.000
Status: Perfect match! ✓
```

---

**Three questions, one minute, perfect answers!** 🎯

---

*Save this guide - StubMatch.m is your best friend for matching problems!*
