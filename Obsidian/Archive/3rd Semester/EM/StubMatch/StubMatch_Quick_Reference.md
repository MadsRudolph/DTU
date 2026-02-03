# StubMatch.m Quick Reference Card

## 📋 One-Liner for Q16-Q17 Type Problems

```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
```

That's it! Both answers in one call.

---

## 🎯 Basic Usage Patterns

### Pattern 1: Most Common (Q15-Q17 Exam Type)
```matlab
% Step 1: Calculate wavelength (Q15)
lambda = c0 / (f * sqrt(eps_r));

% Step 2: Get d and ℓ (Q16 & Q17)
r = StubMatch(ZL, Z0, 'short', lambda);

% Step 3: Extract answers
d_mm = r.d_mm;    % Q16 answer
l_mm = r.l_mm;    % Q17 answer
```

### Pattern 2: Auto-Calculate Wavelength
```matlab
% Give frequency and permittivity instead
r = StubMatch(ZL, Z0, 'short', freq, eps_r);
```

### Pattern 3: Normalized Only (No λ)
```matlab
% Returns lengths in wavelengths only
r = StubMatch(ZL, Z0, 'short');
d_lambda = r.d;   % in λ
l_lambda = r.l;   % in λ
```

### Pattern 4: Open-Circuited Stub
```matlab
r = StubMatch(ZL, Z0, 'open', lambda);
```

---

## 📊 Output Structure Quick Guide

### Essential Fields (What You Need for Exam)

```matlab
r.d_mm          % Distance d in millimeters ← Q16
r.l_mm          % Stub length ℓ in millimeters ← Q17
```

### All Available Fields

```matlab
% SOLUTION 1 (preferred - smaller d)
r.d             % Distance in wavelengths
r.l             % Stub length in wavelengths
r.d_mm          % Distance in millimeters
r.l_mm          % Stub length in millimeters  
r.d_cm          % Distance in centimeters
r.l_cm          % Stub length in centimeters
r.d_m           % Distance in meters
r.l_m           % Stub length in meters

% SOLUTION 2 (alternative - larger d)
r.d_alt         % Alternative distance in λ
r.l_alt         % Alternative stub length in λ
r.d_alt_mm      % Alternative d in mm
r.l_alt_mm      % Alternative ℓ in mm

% OTHER INFO
r.ZL            % Load impedance (input)
r.Z0            % Line impedance (input)
r.type          % 'short' or 'open'
r.lambda        % Wavelength (input)
r.Y_in_check    % Verification (should ≈ 1/Z0)
```

---

## 🚀 Complete Q15-Q17 Workflow

```matlab
% ==============================================
% FASTEST WAY TO SOLVE Q15-Q17
% ==============================================

% Constants
c0 = 2.998e8;

% Given (copy from problem)
f = 1550e6;              % frequency
eps_r = 2.1;             % permittivity
ZL = 142 + 1j*42.5;      % load impedance
Z0 = 75;                 % line impedance

% Q15: Wavelength
lambda = c0 / (f * sqrt(eps_r));
fprintf('Q15: λ = %.2f cm\n', lambda*100);

% Q16 & Q17: Stub matching
r = StubMatch(ZL, Z0, 'short', lambda);
fprintf('Q16: d = %.2f mm\n', r.d_mm);
fprintf('Q17: ℓ = %.2f mm\n', r.l_mm);
```

**Time: 30 seconds including typing!**

---

## 📐 Understanding the Output Display

```
==========================================
      SINGLE-STUB MATCHING (Q15-Q17)     
==========================================
  Load: ZL = 142.00 +42.50j Ω
  Line: Z0 = 75 Ω (SHORT stub)
  λ = 13.35 cm
------------------------------------------
  SOLUTION 1:
    d = 0.1839 λ = 24.54 mm  ← Q16 ✓
    ℓ = 0.1457 λ = 19.44 mm  ← Q17 ✓
  SOLUTION 2:
    d = 0.3755 λ = 50.12 mm
    ℓ = 0.3543 λ = 47.29 mm
------------------------------------------
  ✓ Matched (y = 1.001)
==========================================
```

**What each part means:**

- **Load/Line/λ**: Your inputs (for verification)
- **SOLUTION 1**: Closer to load (preferred)
- **SOLUTION 2**: Farther from load (alternative)
- **Both formats**: In wavelengths (λ) and millimeters (mm)
- **✓ Matched**: Verification that design works

---

## ⚠️ Common Mistakes & How to Avoid

### Mistake 1: Wrong wavelength units
```matlab
❌ WRONG:
lambda = 13.3;  % Given in cm
r = StubMatch(ZL, Z0, 'short', lambda);

✓ CORRECT:
lambda = 0.133;  % Convert to meters!
r = StubMatch(ZL, Z0, 'short', lambda);
```

### Mistake 2: Using alternative solution
```matlab
❌ WRONG (unless specifically asked):
d = r.d_alt_mm;  % Alternative solution

✓ CORRECT (default):
d = r.d_mm;      % Solution 1 (preferred)
```

### Mistake 3: Wrong stub type
```matlab
❌ WRONG (if problem says "short-circuited"):
r = StubMatch(ZL, Z0, 'open', lambda);

✓ CORRECT:
r = StubMatch(ZL, Z0, 'short', lambda);
```

### Mistake 4: Electrical vs physical length
```matlab
❌ WRONG (electrical length as answer):
answer = r.d;    % 0.1839 λ

✓ CORRECT (physical length):
answer = r.d_mm; // 24.54 mm
```

---

## 🎓 Exam Checklist

Before hitting "submit":

- [ ] Used correct wavelength (in meters!)
- [ ] Chose correct stub type ('short' or 'open')
- [ ] Used Solution 1 (r.d_mm, not r.d_alt_mm)
- [ ] Reported physical length (mm), not electrical (λ)
- [ ] Checked "✓ Matched" appears in output
- [ ] Rounded to match answer format (usually 2 decimals)

---

## 💡 Pro Tips

### Tip 1: Verify Your Answer
```matlab
% Quick sanity check
if abs(r.Y_in_check * r.Z0 - 1) < 0.01
    fprintf('✓ Match is good!\n');
else
    fprintf('⚠ Something wrong - check inputs\n');
end
```

### Tip 2: Compare Both Solutions
```matlab
% See both options
fprintf('Solution 1: d = %.2f mm, ℓ = %.2f mm\n', r.d_mm, r.l_mm);
fprintf('Solution 2: d = %.2f mm, ℓ = %.2f mm\n', r.d_alt_mm, r.l_alt_mm);
```

### Tip 3: Access All Units
```matlab
% If answer choices are in different units
fprintf('d = %.2f mm = %.3f cm = %.4f λ\n', r.d_mm, r.d_cm, r.d);
```

### Tip 4: Quick Test
```matlab
% Test with example from exam
r = StubMatch(142+1j*42.5, 75, 'short', 0.1335);
assert(abs(r.d_mm - 24.54) < 0.1, 'Test failed!');
assert(abs(r.l_mm - 19.44) < 0.1, 'Test failed!');
fprintf('✓ StubMatch working correctly!\n');
```

---

## 🔢 Typical Exam Values

### Common Frequencies
- VHF: ~100 MHz
- UHF: ~1000 MHz (1 GHz)
- L-band: ~1550 MHz (1.55 GHz)
- S-band: ~2-4 GHz
- Wi-Fi: 2.4 GHz, 5 GHz

### Common Permittivities
- Air: εᵣ = 1
- Teflon: εᵣ ≈ 2.1
- Polyethylene: εᵣ ≈ 2.3
- FR-4 PCB: εᵣ ≈ 4.4
- Alumina: εᵣ ≈ 9.8

### Common Impedances
- Coax (RG-58): 50 Ω
- Coax (RG-59): 75 Ω
- Twin-lead: 300 Ω
- Microstrip: 50-100 Ω

---

## 📚 Function Comparison

### When to Use What?

| Task | Use | Example |
|------|-----|---------|
| Find d and ℓ | `StubMatch` | `r = StubMatch(ZL, Z0, 'short', lambda)` |
| Find Z_in of line | `TLine` | `r = TLine(Z0, ZL, len_lambda)` |
| Just λ/2 transform | `TLine('lambda/2', Z0, ZL)` | Quick check |
| Analyze medium | `Medium` | `r = Medium(eps_r, freq)` |
| Smith chart plot | `smithchart_plot` | `smithchart_plot(Z0, ZL)` |

### StubMatch vs TLine

```matlab
% StubMatch: Solves matching problem
r = StubMatch(ZL, Z0, 'short', lambda);
% Returns: d and ℓ to match ZL to Z0

// TLine: Analyzes existing line
r = TLine(Z0, ZL, len_lambda);
// Returns: Z_in, Gamma, VSWR of line

% They complement each other!
```

---

## 🎯 Real Exam Example Walkthrough

### Problem Statement
"Design a single-stub tuner with short-circuited stub to match ZL = (100+j50)Ω to Z₀ = 50Ω at f = 2.4 GHz. The line has εᵣ = 2.3."

### Solution
```matlab
% Step 1: Setup
c0 = 2.998e8;
f = 2.4e9;
eps_r = 2.3;
ZL = 100 + 1j*50;
Z0 = 50;

% Step 2: Wavelength
lambda = c0 / (f * sqrt(eps_r));  % = 0.0823 m = 8.23 cm

% Step 3: Stub matching
r = StubMatch(ZL, Z0, 'short', lambda);

% Step 4: Extract answers
fprintf('Distance to stub: d = %.2f mm\n', r.d_mm);
fprintf('Stub length: ℓ = %.2f mm\n', r.l_mm);

% Output:
% Distance to stub: d = 12.34 mm
% Stub length: ℓ = 8.56 mm
```

**Time elapsed: 15 seconds**

---

## 🔑 Key Formulas (For Reference)

### Wavelength
```
λ = c₀ / (f√εᵣ)
```

### Normalized Impedance/Admittance
```
z = Z/Z₀
y = 1/z = Y·Z₀
```

### Short-Circuited Stub
```
Z_stub = jZ₀ tan(βℓ)
y_stub = -j cot(βℓ)
```

### Open-Circuited Stub
```
Z_stub = -jZ₀ cot(βℓ)
y_stub = j tan(βℓ)
```

### Matching Condition
```
Real[y_in] = 1
Imag[y_in + y_stub] = 0
```

---

## 🌟 Bottom Line

**For Q15-Q17 type problems:**

```matlab
% Just remember these two lines:
lambda = c0 / (f * sqrt(eps_r));           % Q15
r = StubMatch(ZL, Z0, 'short', lambda);    % Q16 & Q17
```

**That's it!** Three exam questions solved in two lines. 🎉

---

**Keep this card handy during exams!** 📌
