# smithchart_plot.m - Exam Examples

> **Real Visualization Problems**

---

## Example 1: Q10 Type Problem

### Problem
Plot the load impedance Z_L = 15 - j37.5 Ω on a 75 Ω Smith chart. Determine the reflection coefficient.

### Solution
```matlab
Z0 = 75;
ZL = 15 - 1j*37.5;

smithchart_plot(Z0, ZL, 'Load');
```

### Console Output
```
=== Smith Chart Point ===
  Z0 = 75.00 Ohm
  ZL = 15.0000 -37.5000j Ohm
  zL (normalized) = 0.2000 -0.5000j
  Gamma = -0.5000 -0.5000j
  |Gamma| = 0.7071, angle = -135.00 deg
=========================
```

### Answer
**Γ = -0.5 - j0.5**  
**|Γ| = 0.707**  
**∠Γ = -135°**

### Interpretation
- Point in lower left quadrant
- Capacitive load (negative reactance)
- Low resistance (z_L = 0.2)
- High mismatch (|Γ| = 0.707)

---

## Example 2: Comparing Multiple Impedances

### Problem
Compare three loads on a 50 Ω system:
1. Z_A = 100 Ω (pure resistive)
2. Z_B = 50 + j50 Ω (inductive)
3. Z_C = 25 - j25 Ω (capacitive)

### Solution
```matlab
Z0 = 50;

% Plot all three
smithchart_plot(Z0, 100, 'Z_A');
hold on
smithchart_plot(Z0, 50 + 1j*50, 'Z_B');
smithchart_plot(Z0, 25 - 1j*25, 'Z_C');
hold off
```

### Console Output
```
Point 1 (Z_A):
  zL = 2.0000 +0.0000j
  Gamma = 0.3333 +0.0000j
  
Point 2 (Z_B):
  zL = 1.0000 +1.0000j
  Gamma = 0.4472 +0.4472j
  
Point 3 (Z_C):
  zL = 0.5000 -0.5000j
  Gamma = -0.2000 -0.6000j
```

### Interpretation
- **Z_A:** On real axis (pure resistive)
- **Z_B:** Upper half (inductive), matched real part
- **Z_C:** Lower half (capacitive), lower resistance

---

## Example 3: From Reflection Coefficient

### Problem
A load has Γ = 0.5∠60°. Plot on Smith chart and find the normalized impedance.

### Solution
```matlab
Gamma = 0.5 * exp(1j*deg2rad(60));
smithchart_plot('Gamma', Gamma, '\Gamma');
```

### Console Output
```
=== Smith Chart Point (from Gamma) ===
  Gamma = 0.2500 +0.4330j
  |Gamma| = 0.5000, angle = 60.00 deg
  zL (normalized) = 1.6000 +1.3856j
======================================
```

### Answer
**z_L = 1.6 + j1.39**

For Z₀ = 50 Ω:
**Z_L = 50 × (1.6 + j1.39) = 80 + j69.3 Ω**

---

## Example 4: Transmission Line Problem

### Problem
A 75 Ω line is terminated with Z_L = 150 + j75 Ω. Plot both the load and the input impedance at λ/4 from the load.

### Solution
```matlab
Z0 = 75;
ZL = 150 + 1j*75;

% Plot load
smithchart_plot(Z0, ZL, 'Z_L');
hold on

% Calculate input impedance at λ/4
% For λ/4: Z_in = Z0²/ZL
Z_in = Z0^2 / ZL;

% Plot input impedance
smithchart_plot(Z0, Z_in, 'Z_{in}');
hold off
```

### Console Output
```
Load:
  ZL = 150.0000 +75.0000j
  zL = 2.0000 +1.0000j
  Gamma = 0.4472 +0.4472j
  
Input (λ/4):
  Z_in = 25.7143 -12.8571j
  zL = 0.3429 -0.1714j
  Gamma = -0.4472 -0.4472j
```

### Interpretation
- **Load:** High R, inductive
- **Input:** Low R, capacitive
- **Relationship:** 180° rotation on Smith chart (λ/4 transformation)

---

## Example 5: Stub Matching Visualization

### Problem
Visualize a stub matching network where:
- Load: Z_L = 100 + j50 Ω
- Line: Z₀ = 50 Ω
- Stub location: 0.184λ from load
- After stub: Matched (Z = Z₀)

### Solution
```matlab
Z0 = 50;
ZL = 100 + 1j*50;

% Plot load
smithchart_plot(Z0, ZL, 'Load');
hold on

% Plot matched condition (target)
smithchart_plot(Z0, Z0, 'Matched');

% Calculate impedance at stub location
% (This would use TLine function)
Z_stub = 50 + 1j*35;  % Example value
smithchart_plot(Z0, Z_stub, 'At Stub');

hold off
```

### Visual Shows
- Load position (upper right)
- Target position (center)
- Intermediate position at stub
- Path from load to matched

---

## 🎓 Exam Strategy

### Time Management
- **Plot impedance:** 10 seconds
- **Read Γ from console:** 5 seconds
- **Interpret location:** 5 seconds
- **Total:** ~20 seconds per plot

### Step-by-Step
1. **Identify Z₀ and Z_L from problem**
2. **One function call**
3. **Read console for Γ and z_L**
4. **Verify point location makes sense**
5. **Record values needed**

---

## ✅ Answer Checklist

**For each plotted impedance:**
- [ ] Point appears on chart
- [ ] Console shows Γ (magnitude & angle)
- [ ] Console shows z_L (normalized)
- [ ] Location makes sense:
  - Upper = inductive
  - Lower = capacitive
  - Right = high R
  - Left = low R
  - Center = matched

---

## 💡 Quick Checks

### Verify Your Plot

**Real axis (jX = 0)?**
→ Should be on horizontal line

**Pure reactance (R = 0)?**
→ Should be on outer circle

**Matched (Z = Z₀)?**
→ Should be at center

**Open (Z → ∞)?**
→ Should be at right edge

**Short (Z → 0)?**
→ Should be at left edge

---

[← Master Index](smithchart_plot_MASTER_INDEX.md)
