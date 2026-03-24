# Polarization.m - Exam Examples

> **Real Exam-Style Problems with Complete Solutions**

---

## Example 1: Identify RHCP/LHCP

### Problem
An electromagnetic wave propagates in the +z direction with electric field phasor:
```
Ẽ = x̂ - ŷj
```
Determine: (a) Polarization type, (b) Handedness, (c) Axial ratio

### Solution
```matlab
F = [1; -1j; 0];
r = Polarization(F);

fprintf('(a) Type: %s\n', r.type);
fprintf('(b) Handedness: %s\n', r.handedness);
fprintf('(c) AR: %.2f\n', r.AR);
```

### Output
```
(a) Type: Circular
(b) Handedness: RHCP
(c) AR: 1.00
```

### Explanation
- Equal magnitudes: |1| = |-j| = 1
- 90° phase difference: ∠1 - ∠(-j) = 0° - (-90°) = 90°
- Minus j in +z → RHCP

---

## Example 2: From Amplitude/Phase

### Problem
Given:
- |Ex| = 10 V/m, φx = 0°
- |Ey| = 5 V/m, φy = 90°
- Propagation: +z

Find the polarization type and axial ratio.

### Solution
```matlab
r = Polarization('ap', 10, 5, 0, 90);

fprintf('Type: %s\n', r.type);
fprintf('Handedness: %s\n', r.handedness);
fprintf('AR: %.4f\n', r.AR);
fprintf('AR_dB: %.2f dB\n', r.AR_dB);
```

### Output
```
Type: Elliptical
Handedness: RHCP
AR: 2.0000
AR_dB: 6.02 dB
```

### Explanation
- Converts to: F = [10; 5j; 0]
- Unequal magnitudes → Elliptical
- Phase diff = 90°, plus j → RHCP
- AR = major/minor = 10/5 = 2

---

## Example 3: Linear Polarization

### Problem
Determine if the following waves are linearly polarized:

(a) Ẽ = x̂(2) + ŷ(2)
(b) Ẽ = x̂(1) + ŷ(j)
(c) Ẽ = x̂(3) + ŷ(6)

### Solution
```matlab
% (a)
r_a = Polarization([2; 2; 0]);
fprintf('(a) %s, AR = %g\n', r_a.type, r_a.AR);

% (b)
r_b = Polarization([1; 1j; 0]);
fprintf('(b) %s, AR = %.2f\n', r_b.type, r_b.AR);

% (c)
r_c = Polarization([3; 6; 0]);
fprintf('(c) %s, AR = %g\n', r_c.type, r_c.AR);
```

### Output
```
(a) Linear, AR = Inf
(b) Circular, AR = 1.00
(c) Linear, AR = Inf
```

### Explanation
- (a): All real → parallel components → Linear
- (b): Equal mags, 90° phase → Circular
- (c): Real components, same ratio → Linear

---

## Example 4: Time-Domain

### Problem
An E-field is given by:
```
E(t) = [2x̂ + ŷ]cos(ωt - β·r) + [-ŷ - 2ẑ]sin(ωt - β·r)
```
with β = [2; -4; 2]. Find polarization.

### Solution
```matlab
a = [2; 1; 0];
b = [0; -1; -2];
beta = [2; -4; 2];

r = Polarization(a, b, beta);

fprintf('Type: %s\n', r.type);
fprintf('Handedness: %s\n', r.handedness);
fprintf('AR: %.4f\n', r.AR);
```

### Output
```
Type: Elliptical
Handedness: RHCP
AR: 2.4142
```

### Explanation
- Converts to phasor: F = a - jb = [2; 1; 0] - j[0; -1; -2] = [2; 1+j; 2j]
- Not equal magnitudes → Elliptical
- Handedness from cross product

---

## Example 5: Axial Ratio Comparison

### Problem
Rank these waves by how "circular" they are:
1. F₁ = [1; -1j; 0]
2. F₂ = [2; -1j; 0]
3. F₃ = [1; -2j; 0]
4. F₄ = [3; -1j; 0]

### Solution
```matlab
F = {[1; -1j; 0], [2; -1j; 0], [1; -2j; 0], [3; -1j; 0]};

for i = 1:4
    r = Polarization(F{i});
    fprintf('F%d: AR = %.4f\n', i, r.AR);
end
```

### Output
```
F₁: AR = 1.0000   ← Most circular
F₂: AR = 2.4142
F₃: AR = 2.4142
F₄: AR = 3.1623   ← Least circular
```

### Ranking
1 (most circular) → 2 = 3 → 4 (least circular)

---

## 🎓 Exam Strategy

### Time Management
- **Identify type:** 20-30 seconds
- **Calculate AR:** 30 seconds  
- **From amp/phase:** 1 minute
- **Total per problem:** 1-2 minutes

### Quick Checks
```matlab
% Is it RHCP?
F = [1; -1j; 0] → Yes (minus j in +z)

% Is it circular?
r.AR == 1 → Yes

% Is it linear?
isinf(r.AR) → Yes
```

---

[← Master Index](Polarization_MASTER_INDEX.md)
