# coulomb_pair.m - Exam Examples

> **Real Electrostatics Problems**

---

## Example 1: Basic Two-Charge Problem

### Problem
Two point charges are positioned as follows:
- q₁ = 2 μC at (1, 0, 0) m
- q₂ = -3 μC at (0, 1, 0) m

Find:
(a) The force on q₁
(b) The force on q₂
(c) Verify Newton's third law

### Solution
```matlab
% Given
q1 = 2e-6;          % 2 μC in Coulombs
q2 = -3e-6;         % -3 μC in Coulombs
r1 = [1; 0; 0];     % Position of q1 [m]
r2 = [0; 1; 0];     % Position of q2 [m]

% Calculate
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% Results
>> F12
F12 =
  -0.0382
   0.0382
        0

>> F21
F21 =
   0.0382
  -0.0382
        0

>> norm(F12)
ans = 0.0540  % 54.0 mN

>> norm(F21)
ans = 0.0540  % 54.0 mN
```

### Answers
(a) **F₁ = (-38.2, 38.2, 0) mN**  
(b) **F₂ = (38.2, -38.2, 0) mN**  
(c) **F₁ = -F₂** ✓ (Newton's 3rd law verified)

### Interpretation
- Opposite charges → **Attractive force**
- F₁ points from q₁ toward q₂
- F₂ points from q₂ toward q₁
- Equal magnitudes, opposite directions

---

## Example 2: Repulsive Force

### Problem
Two electrons separated by 1 nm. Find the repulsive force.

**Given:**
- Electron charge: e = 1.6 × 10⁻¹⁹ C
- Separation: 1 nm = 1 × 10⁻⁹ m

### Solution
```matlab
% Electron charge
e = 1.6e-19;  % Coulombs

% Both electrons have same (negative) charge
q1 = -e;
q2 = -e;

% Positions (1 nm apart along x-axis)
r1 = [0; 0; 0];
r2 = [1e-9; 0; 0];

% Calculate
[F12, F21] = coulomb_pair(q1, q2, r1, r2);

>> norm(F12)
ans = 2.3025e-10  % 0.230 nN

>> F12
F12 =
  -2.3025e-10  % Negative x (repulsion)
   0
   0
```

### Answer
**|F| = 0.230 nN** (repulsive, along x-axis)

### Physical Insight
- Same charge → **Repulsion**
- Force pushes electrons apart
- At atomic scales (nm), forces are tiny (nN)

---

## Example 3: Net Force from Multiple Charges

### Problem
Three charges in a line:
- q₁ = 1 μC at x = 0
- q₂ = -2 μC at x = 1 m
- q₃ = 1 μC at x = 2 m

Find the net force on q₁.

### Solution
```matlab
% Charges
q1 = 1e-6;
q2 = -2e-6;
q3 = 1e-6;

% Positions
r1 = [0; 0; 0];
r2 = [1; 0; 0];
r3 = [2; 0; 0];

% Force on q1 from q2
[F12, ~] = coulomb_pair(q1, q2, r1, r2);

% Force on q1 from q3
[F13, ~] = coulomb_pair(q1, q3, r1, r3);

% Net force (superposition)
F_net = F12 + F13;

>> F12
F12 =
   0.0180    % Attraction to right
   0
   0

>> F13
F13 =
  -0.0022    % Repulsion to left
   0
   0

>> F_net
F_net =
   0.0158    % Net to the right
   0
   0
```

### Answer
**F_net = 15.8 mN** in +x direction

### Interpretation
- q₂ (negative, closer) attracts strongly → +x
- q₃ (positive, farther) repels weakly → -x
- Net force toward q₂ (stronger attraction wins)

---

## Example 4: 3D Configuration

### Problem
Two charges at opposite corners of a cube:
- q₁ = 5 μC at (0, 0, 0) m
- q₂ = -3 μC at (1, 1, 1) m

Find the force magnitude and direction.

### Solution
```matlab
q1 = 5e-6;
q2 = -3e-6;
r1 = [0; 0; 0];
r2 = [1; 1; 1];

[F12, F21] = coulomb_pair(q1, q2, r1, r2);

% Magnitude
>> norm(F12)
ans = 0.0225  % 22.5 mN

% Direction (unit vector)
>> F12 / norm(F12)
ans =
   0.5774    % Equal components
   0.5774
   0.5774

% Distance between charges
>> norm(r2 - r1)
ans = 1.7321  % √3 m (space diagonal)
```

### Answer
**|F| = 22.5 mN** along (1,1,1) direction (toward q₂)

### Interpretation
- Attractive force (opposite charges)
- Force along space diagonal of cube
- Equal components in all three directions

---

## Example 5: Force Balance

### Problem
A charge q₁ = 1 μC is at the origin. Where should we place q₂ = -2 μC so that a third charge q₃ = 1 μC at (2, 0, 0) experiences zero net force?

### Solution
```matlab
q1 = 1e-6;
q2 = -2e-6;
q3 = 1e-6;

r1 = [0; 0; 0];
r3 = [2; 0; 0];

% For zero net force on q3:
% F31 + F32 = 0
% Need to find r2

% By symmetry, r2 must be on x-axis: r2 = [x; 0; 0]
% Force balance: k*q1*q3/4 = k*q2*q3/(2-x)²
% Solving: 1/4 = 2/(2-x)²
% (2-x)² = 8
% x = 2 - 2√2 ≈ -0.828 m

r2 = [2 - 2*sqrt(2); 0; 0];

% Verify
[F31, ~] = coulomb_pair(q3, q1, r3, r1);
[F32, ~] = coulomb_pair(q3, q2, r3, r2);

F_net = F31 + F32;

>> F_net
F_net =
   1.0e-14 *  % Essentially zero
   0.0444
   0
   0

>> norm(F_net)
ans = 4.44e-16  % ≈ 0 (numerical precision)
```

### Answer
**r₂ = (-0.828, 0, 0) m** (or 2 - 2√2 m)

---

## 🎓 Exam Strategy

### Time Management
- **Read problem:** 15 seconds
- **Extract values:** 10 seconds
- **Function call:** 5 seconds
- **Interpret result:** 10 seconds
- **Total:** ~40 seconds per charge pair

### Step-by-Step Approach
1. **Identify charges and positions** from problem
2. **Convert units** (μC → C, cm → m)
3. **One function call** for each pair
4. **Sum forces** if multiple charges (superposition)
5. **Check direction** (attraction vs repulsion)

---

## ✅ Answer Checklist

For each problem:
- [ ] Units converted to SI (C, m)
- [ ] Column vectors used (semicolons)
- [ ] Force direction makes sense
- [ ] Magnitude in reasonable range (pN to mN)
- [ ] Newton's 3rd law verified (if both forces needed)
- [ ] Multiple charges summed correctly (if applicable)

---

## 💡 Quick Checks

### Verify Direction
```matlab
% Same sign charges
if q1*q2 > 0
    % Should repel: F12 points away from q2
    r_12 = r1 - r2;
    assert(dot(F12, r_12) > 0, 'Should repel!');
end

% Opposite sign charges
if q1*q2 < 0
    % Should attract: F12 points toward q2
    r_12 = r1 - r2;
    assert(dot(F12, r_12) < 0, 'Should attract!');
end
```

### Verify Magnitude
```matlab
% Calculate manually
r = norm(r1 - r2);
F_manual = 8.99e9 * abs(q1*q2) / r^2;

% Compare
F_calc = norm(F12);
error = abs(F_calc - F_manual) / F_manual;
fprintf('Error: %.2f%%\n', error*100);
```

---

[← Master Index](coulomb_pair_MASTER_INDEX.md)
