# poynting_pw.m - Troubleshooting Guide

> **Quick Error Diagnosis**

---

## Problem 1: H-field Has Wrong Sign

### Symptoms
```matlab
>> r = poynting_pw('time', a, b, E0, beta);
% H components have opposite sign from expected
```

### Diagnosis
**Used plus instead of minus in phasor conversion**

### Solution
```matlab
❌ Wrong conversion:
Ẽ = E0 * (a + 1j*b)

✅ Correct conversion:
Ẽ = E0 * (a - 1j*b)
```

**Rule:** Phasor = E₀(a - jb), always MINUS

---

## Problem 2: Wrong Units

### Symptoms
```matlab
% Expected H in mA/m, but values are in A/m
```

### Diagnosis
**Reading from struct instead of console**

### Solution
```matlab
% Console output (formatted):
% H̃₀ = [42.17+0.00j; ...] mA/m  ← Use this for exam

% Struct (raw):
>> r.H_phasor
ans = 0.0422 + 0.0000i  ← This is in A/m

% Convert if needed:
H_mA = r.H_phasor * 1000;  % mA/m
```

**Tip:** Read console for exam-formatted answers

---

## Problem 3: Error "Unknown mode"

### Symptoms
```matlab
>> r = poynting_pw(a, b, E0, beta);
Error: Unknown mode
```

### Diagnosis
**Missing 'time' keyword**

### Solution
```matlab
❌ Wrong:
poynting_pw(a, b, E0, beta_vec)

✅ Correct:
poynting_pw('time', a, b, E0, beta_vec)
```

---

## Problem 4: Swapped a and b

### Symptoms
```matlab
% Results completely wrong
```

### Diagnosis
**Confused cos and sin coefficients**

### Solution
```matlab
% Given: E = E₀([2;1;0]cos + [0;-1;-2]sin)

❌ Wrong:
a = [0; -1; -2];   % Sin coeffs!
b = [2; 1; 0];     % Cos coeffs!

✅ Correct:
a = [2; 1; 0];     % Cos coeffs
b = [0; -1; -2];   % Sin coeffs
```

**Rule:** a = cos term, b = sin term

---

## Problem 5: Row vs Column Vectors

### Symptoms
```matlab
>> r = poynting_pw('time', a, b, E0, beta);
Error in cross product
```

### Diagnosis
**Used commas (row vectors) instead of semicolons (column vectors)**

### Solution
```matlab
❌ Wrong:
a = [2, 1, 0];  % Commas!

✅ Correct:
a = [2; 1; 0];  % Semicolons!
```

---

## 🔧 Diagnostic Script

```matlab
fprintf('=== poynting_pw Diagnostic ===\n\n');

% Test 1: Simple case
a = [1; 0; 0];
b = [0; 1; 0];
E0 = 1;
beta = [0; 0; 1];

r = poynting_pw('time', a, b, E0, beta);

fprintf('E-field: [%.2f%+.2fj; ...]\n', real(r.E_phasor(1)), imag(r.E_phasor(1)));
fprintf('Expected: [1.00-0.00j; ...]\n\n');

fprintf('H-field magnitude: %.4f A/m\n', abs(r.H_phasor(2)));
fprintf('Expected: ~0.0027 A/m (1/377)\n\n');

fprintf('S magnitude: %.4f W/m²\n', r.S_mag);
fprintf('Expected: ~0.0013 W/m² (1²/(2×377))\n\n');

fprintf('=== Test complete ===\n');
```

---

## ✅ Pre-Submission Checklist

- [ ] Used column vectors (semicolons)
- [ ] Correct conversion: Ẽ = E₀(a - jb)
- [ ] a = cos coefficients
- [ ] b = sin coefficients
- [ ] Included 'time' keyword
- [ ] Read console for formatted output
- [ ] Units make sense (mA/m, W/m²)

---

[← Master Index](poynting_pw_MASTER_INDEX.md)
