# B_inf_wire.m - Exam Examples

> **Real Magnetostatics Problems**

---

## Example 1: Basic Single Wire

### Problem
A long straight wire carries a current of 5 A. Find the magnetic field magnitude at a distance of 2 cm from the wire.

### Solution
```matlab
% Given
I = 5;       % Current [A]
r = 0.02;    % Distance [m] (2 cm)

% Calculate
B = B_inf_wire(I, r);

>> B
B = 5.0000e-05  % Tesla

% In microtesla
>> B * 1e6
ans = 50  % μT
```

### Answer
**B = 50 μT** at 2 cm from the wire

### Interpretation
- Earth's magnetic field ≈ 50 μT (same order of magnitude!)
- B-field decreases with distance (1/r)
- Direction: circles the wire (right-hand rule)

---

## Example 2: Multiple Distances

### Problem
A wire carries 10 A. Find B-field at distances of:
(a) 1 cm
(b) 2 cm  
(c) 5 cm
(d) 10 cm

Verify the inverse relationship.

### Solution
```matlab
% Current
I = 10;  % A

% Distances
r = [0.01, 0.02, 0.05, 0.10];  % m

% Calculate all at once
B = B_inf_wire(I, r);

>> B * 1e6  % In μT
ans =
   200   100    40    20
```

### Answers
(a) **B = 200 μT** at 1 cm  
(b) **B = 100 μT** at 2 cm  
(c) **B = 40 μT** at 5 cm  
(d) **B = 20 μT** at 10 cm

### Verification
```matlab
% Distance doubles: 1→2 cm, 2→4 cm (not in list), 5→10 cm
% B-field should halve

>> B(1) / B(2)  % 1 cm vs 2 cm
ans = 2.0000

>> B(3) / B(4)  % 5 cm vs 10 cm
ans = 2.0000

% ✓ Verified: B ∝ 1/r
```

---

## Example 3: Magnetic Material (Iron Core)

### Problem
A wire carrying 2 A is embedded in iron with μᵣ = 1000. Find the B-field at 1 cm from the wire. Compare with air.

### Solution
```matlab
% Given
I = 2;
r = 0.01;

% In air (μᵣ = 1)
B_air = B_inf_wire(I, r);

% In iron (μᵣ = 1000)
B_iron = B_inf_wire(I, r, 1000);

>> B_air * 1e6
ans = 40  % μT

>> B_iron * 1e3
ans = 40  % mT (note: millitesla!)

>> B_iron / B_air
ans = 1000  % Exactly μᵣ
```

### Answer
- **In air: B = 40 μT**
- **In iron: B = 40 mT** (1000× stronger)

### Physical Insight
- Magnetic materials amplify B-field
- B_material = μᵣ × B_air
- Iron: μᵣ ≈ 1000-5000 (very magnetic)

---

## Example 4: Two Parallel Wires

### Problem
Two long parallel wires separated by 10 cm carry currents of 5 A each:
(a) Same direction
(b) Opposite directions

Find the B-field at the midpoint.

### Solution

**(a) Same direction:**
```matlab
% Wire 1 at x = -5 cm, Wire 2 at x = +5 cm
% Midpoint at x = 0

I = 5;  % Same current
r = 0.05;  % 5 cm to each wire

% B-field from each wire
B1 = B_inf_wire(I, r);
B2 = B_inf_wire(I, r);

% At midpoint, both fields point same direction
% (check with right-hand rule)
B_total = B1 + B2;  % Add magnitudes

>> B_total * 1e6
ans = 40  % μT
```

**Answer (a): B = 40 μT** (fields reinforce)

**(b) Opposite directions:**
```matlab
% Same magnitudes
B1 = B_inf_wire(5, 0.05);
B2 = B_inf_wire(5, 0.05);

% But opposite directions → cancel
B_total = B1 - B2;  % Subtract

>> B_total
ans = 0
```

**Answer (b): B = 0** (fields cancel)

---

## Example 5: Finding Current from B-field

### Problem
The magnetic field at 3 cm from a wire is measured to be 67 μT. Find the current in the wire.

### Solution

**Given:** B = 67 μT = 67×10⁻⁶ T, r = 0.03 m

**Formula:** B = μ₀I/(2πr) → I = B(2πr)/μ₀

```matlab
% Given
B = 67e-6;  % T
r = 0.03;   % m
mu0 = 4*pi*1e-7;

% Solve for I
I = B * 2*pi*r / mu0;

>> I
I = 10.0535  % A ≈ 10 A

% Verify
B_check = B_inf_wire(I, r);

>> B_check * 1e6
ans = 67.0000  % μT ✓
```

### Answer
**I ≈ 10 A**

### Method
Rearrange Ampère's law: **I = B·2πr/μ₀**

---

## Example 6: Coaxial Cable

### Problem
A coaxial cable has:
- Inner conductor (radius 1 mm): carries +10 A
- Outer conductor (inner radius 5 mm): carries -10 A (return current)

Find B-field at:
(a) r = 2 mm (between conductors)
(b) r = 10 mm (outside cable)

### Solution

**(a) Between conductors (r = 2 mm):**
```matlab
% Only inner conductor contributes
I_inner = 10;
r = 0.002;  % 2 mm

B = B_inf_wire(I_inner, r);

>> B * 1e6
ans = 1000  % μT = 1 mT
```

**Answer (a): B = 1 mT**

**(b) Outside cable (r = 10 mm):**
```matlab
% Both conductors contribute
I_net = 10 - 10;  % Opposite currents cancel

% Net current enclosed = 0
B = 0;  % No field outside
```

**Answer (b): B = 0**

### Principle
- Inside: Only enclosed current matters
- Outside: Opposite currents cancel

---

## Example 7: Force Between Wires

### Problem
Two parallel wires 5 cm apart carry I₁ = 10 A and I₂ = 5 A in the same direction. Find the force per unit length between them.

### Solution
```matlab
% B-field from wire 1 at wire 2's location
I1 = 10;
d = 0.05;  % separation

B1 = B_inf_wire(I1, d);

% Force per unit length on wire 2
I2 = 5;
F_per_L = I2 * B1;  % F/L = I₂B₁

>> F_per_L
F_per_L = 2.0000e-04  % N/m

% In mN/m
>> F_per_L * 1e3
ans = 0.2000  % mN/m
```

### Answer
**F/L = 0.2 mN/m** (attractive force)

### Direction
Same current direction → **Attractive** (wires pull together)

---

## 🎓 Exam Strategy

### Time Management
- **Read problem:** 10 seconds
- **Extract I and r:** 10 seconds  
- **Function call:** 5 seconds
- **Convert units:** 5 seconds
- **Total:** ~30 seconds per calculation

### Step-by-Step Approach
1. **Identify current** and convert to Amperes
2. **Identify distance** and convert to meters
3. **One function call**
4. **Convert result** to appropriate units (usually μT)
5. **Apply right-hand rule** if direction needed

---

## ✅ Answer Checklist

For each problem:
- [ ] Current in Amperes (not mA)
- [ ] Distance in meters (not cm)
- [ ] Result in reasonable range (1-100 μT typical)
- [ ] Units specified (T, mT, μT, G)
- [ ] Direction specified if asked (right-hand rule)
- [ ] Scaling verified if multiple distances

---

## 💡 Quick Checks

### Verify Magnitude
```matlab
% Order of magnitude estimate:
% I ~ 10 A, r ~ 1 cm → B ~ 200 μT

I = 10;
r = 0.01;
B = B_inf_wire(I, r);

fprintf('B = %.0f μT (expect ~200)\n', B*1e6);
```

### Verify Scaling
```matlab
% Test inverse relationship
r1 = 0.01;  r2 = 0.02;
B1 = B_inf_wire(10, r1);
B2 = B_inf_wire(10, r2);

assert(abs(B1/B2 - 2) < 0.01, 'Scaling error!');
```

---

[← Master Index](B_inf_wire_MASTER_INDEX.md)
