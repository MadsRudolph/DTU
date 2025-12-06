# coulomb_pair.m - Troubleshooting Guide

> **Quick Error Diagnosis**

---

## Problem 1: "Charges must not coincide" Error

### Symptoms
```matlab
>> [F12, F21] = coulomb_pair(q1, q2, r1, r2);
Error: Charges must not coincide.
```

### Diagnosis
**r1 and r2 are identical** - charges at same location

### Solution
```matlab
% Check positions
>> r1
r1 =
   1
   0
   0

>> r2
r2 =
   1    % Same as r1!
   0
   0

❌ Problem: r1 == r2

✅ Fix: Use different positions
r2 = [2; 0; 0];  % Different from r1
```

---

## Problem 2: Forces Way Too Large/Small

### Symptoms
```matlab
>> norm(F12)
ans = 8.99e15  % Unrealistically huge!
```

### Diagnosis
**Wrong units** - forgot to convert to Coulombs or meters

### Solution
```matlab
❌ Wrong:
q1 = 5;     % Meant 5 μC, but this is 5 C!
r1 = [100; 0; 0];  % Meant 100 cm, but this is 100 m!

✅ Correct:
q1 = 5e-6;           % 5 μC = 5×10⁻⁶ C
r1 = [100*1e-2; 0; 0];  % 100 cm = 1 m
% Or simply:
r1 = [1; 0; 0];      % 1 m directly
```

**Rule:** Always use SI units (C and m)

---

## Problem 3: F12 ≠ -F21

### Symptoms
```matlab
>> F12 + F21
ans =
   0.0001  % Should be 0!
   0.0002
   0
```

### Diagnosis
**Numerical precision** - not a real problem if small

### Solution
```matlab
% Check relative error
error = norm(F12 + F21) / norm(F12);

if error < 1e-10
    fprintf('OK: Numerical precision\n');
else
    fprintf('Problem: Check calculation\n');
end

% For practical purposes:
% error < 1e-6 is fine
```

---

## Problem 4: Wrong Force Direction

### Symptoms
```matlab
% Expected repulsion but got attraction
```

### Diagnosis
**Sign of charges incorrect**

### Solution
```matlab
% Check charge signs
fprintf('q1 = %.2e (should be %s)\n', q1, sign_str(q1));
fprintf('q2 = %.2e (should be %s)\n', q2, sign_str(q2));

% If both same sign → repel
% If opposite signs → attract

% Verify direction
r_12 = r1 - r2;  % Direction from q2 to q1
dot_product = dot(F12, r_12);

if q1*q2 > 0  % Same sign
    if dot_product > 0
        fprintf('✓ Repulsion (correct)\n');
    else
        fprintf('✗ Wrong direction!\n');
    end
else  % Opposite sign
    if dot_product < 0
        fprintf('✓ Attraction (correct)\n');
    else
        fprintf('✗ Wrong direction!\n');
    end
end
```

---

## Problem 5: Dimensions Error

### Symptoms
```matlab
>> [F12, F21] = coulomb_pair(q1, q2, r1, r2);
Error: Matrix dimensions must agree
```

### Diagnosis
**Row vectors instead of column vectors**

### Solution
```matlab
❌ Wrong:
r1 = [1, 0, 0];  % Row vector (commas)

✅ Correct:
r1 = [1; 0; 0];  % Column vector (semicolons)

% Quick fix for existing row vector:
r1 = r1(:);  % Converts to column
```

---

## 🔧 Diagnostic Script

```matlab
fprintf('=== coulomb_pair Diagnostic ===\n\n');

% Test 1: Simple repulsion
q1 = 1e-6;
q2 = 1e-6;
r1 = [0; 0; 0];
r2 = [1; 0; 0];

[F12, F21] = coulomb_pair(q1, q2, r1, r2);

fprintf('Test 1: Same sign (repulsion)\n');
fprintf('  F12 magnitude: %.4e N\n', norm(F12));
fprintf('  Expected: ~0.009 N\n');
fprintf('  Direction: F12 should point in -x\n');
fprintf('  F12 = [%.4f; %.4f; %.4f]\n\n', F12);

% Test 2: Simple attraction
q2 = -1e-6;
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

fprintf('Test 2: Opposite sign (attraction)\n');
fprintf('  F12 magnitude: %.4e N\n', norm(F12));
fprintf('  Expected: ~0.009 N\n');
fprintf('  Direction: F12 should point in +x\n');
fprintf('  F12 = [%.4f; %.4f; %.4f]\n\n', F12);

% Test 3: Newton's 3rd law
error = norm(F12 + F21);
fprintf('Test 3: Newton''s 3rd law\n');
fprintf('  |F12 + F21| = %.4e\n', error);
fprintf('  Expected: < 1e-10\n');
if error < 1e-10
    fprintf('  ✓ PASS\n');
else
    fprintf('  ✗ FAIL\n');
end

fprintf('\n=== Tests complete ===\n');
```

---

## ✅ Pre-Submission Checklist

- [ ] Used column vectors: `[x; y; z]` with semicolons
- [ ] Charges in Coulombs (use e-6 for μC)
- [ ] Distances in meters
- [ ] r1 ≠ r2 (different positions)
- [ ] Checked: F12 + F21 ≈ 0
- [ ] Force direction makes sense:
  - Same signs → repel (away from each other)
  - Opposite signs → attract (toward each other)
- [ ] Magnitude reasonable (typically mN to μN range)

---

## 💡 Quick Fixes

### Fix 1: Convert to Column Vectors
```matlab
% If you have row vectors:
r1 = r1(:);  % Force to column
r2 = r2(:);
```

### Fix 2: Check Units
```matlab
% Quick unit check
fprintf('Charge magnitude: %.2e C\n', abs(q1));
fprintf('Distance: %.2f m\n', norm(r1-r2));
% Charges should be ~10⁻⁶ to 10⁻⁹ C
% Distances should be ~0.01 to 10 m
```

### Fix 3: Verify Direction
```matlab
% Same sign → dot product should be positive
if q1*q2 > 0
    assert(dot(F12, r1-r2) > 0, 'Wrong direction!');
else
    assert(dot(F12, r1-r2) < 0, 'Wrong direction!');
end
```

---

[← Master Index](coulomb_pair_MASTER_INDEX.md)
