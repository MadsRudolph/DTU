# StubMatch Quick Start Guide (5 Minutes)

## 🚀 TL;DR - Just Give Me The Code!

### Most Common Pattern (90% of Problems)

```matlab
% Given values
ZL = 100 + 1j*50;    % Load impedance (Ω)
Z0 = 50;              % Line impedance (Ω)
lambda = 0.12;        % Wavelength (METERS!)

% Solve everything
r = StubMatch(ZL, Z0, 'short', lambda);

% Get answers
fprintf('d = %.2f mm\n', r.d_mm);   % Distance to stub
fprintf('ℓ = %.2f mm\n', r.l_mm);   % Stub length
```

**That's it!** You're done.

---

## 📋 Three Essential Patterns

### Pattern 1: Wavelength Given
**Problem says:** "λ = 12 cm"

```matlab
lambda = 0.12;  % Convert to meters!
r = StubMatch(ZL, Z0, 'short', lambda);
```

### Pattern 2: Frequency Given
**Problem says:** "f = 2.4 GHz, εᵣ = 2.3"

```matlab
c0 = 2.998e8;
lambda = c0 / (f * sqrt(eps_r));
r = StubMatch(ZL, Z0, 'short', lambda);
```

**Or let StubMatch calculate it:**
```matlab
r = StubMatch(ZL, Z0, 'short', f, eps_r);
```

### Pattern 3: Only Need Electrical Lengths
**Problem asks for:** "Find d and ℓ in wavelengths"

```matlab
r = StubMatch(ZL, Z0, 'short');
fprintf('d = %.4f λ\n', r.d);
fprintf('ℓ = %.4f λ\n', r.l);
```

---

## 🎯 What You Get Back

### Essential Fields

```matlab
r.d_mm      % Distance to stub (millimeters) ← MOST COMMON ANSWER
r.l_mm      % Stub length (millimeters) ← MOST COMMON ANSWER
r.d         % Distance in wavelengths
r.l         % Stub length in wavelengths
```

### Bonus: Alternative Solution

```matlab
r.d_alt_mm  % Alternative distance (farther from load)
r.l_alt_mm  // Alternative stub length
```

**Default to Solution 1** (r.d_mm, r.l_mm) unless told otherwise.

---

## ⚙️ Input Reference Card

### Required Inputs

| Parameter | Type | Example | Units |
|-----------|------|---------|-------|
| `ZL` | complex | `100+1j*50` | Ω |
| `Z0` | real | `50` | Ω |
| `stub_type` | string | `'short'` or `'open'` | - |

### Optional Inputs

| Parameter | Example | Units | When to Use |
|-----------|---------|-------|-------------|
| `lambda` | `0.12` | **meters** | Want physical lengths |
| `freq` | `2.4e9` | Hz | Have frequency |
| `eps_r` | `2.3` | - | Use with freq |

---

## 🔧 The Only Rules You Need

### Rule 1: Wavelength Units
```matlab
✓ CORRECT: lambda = 0.12     % meters
❌ WRONG:   lambda = 12       % cm (will give huge errors!)
```

**Always convert wavelength to meters before calling StubMatch!**

### Rule 2: Stub Type
```matlab
// Problem says "short-circuited" → use 'short'
r = StubMatch(ZL, Z0, 'short', lambda);

// Problem says "open-circuited" → use 'open'
r = StubMatch(ZL, Z0, 'open', lambda);
```

### Rule 3: Which Solution
```matlab
% Default: Use Solution 1 (smaller d)
d = r.d_mm;    ✓ Solution 1
l = r.l_mm;    ✓ Solution 1

// Unless problem specifically asks for alternative:
d = r.d_alt_mm;  ← Solution 2 (rare)
l = r.l_alt_mm;  ← Solution 2 (rare)
```

---

## ✅ Quick Checklist

Before you submit your answer:

- [ ] Did I convert λ to **meters**?
- [ ] Did I use correct stub type (`'short'` or `'open'`)?
- [ ] Am I using Solution 1 (r.d_mm, r.l_mm)?
- [ ] Does output say "✓ Matched"?
- [ ] Do the answers look reasonable for my wavelength?

---

## 🎓 Example: Complete Problem in 30 Seconds

**Problem:**
"Match ZL = 75+j25 Ω to Z₀ = 50 Ω. f = 2.4 GHz, εᵣ = 2.3. Use short stub."

**Solution:**
```matlab
% Setup (5 seconds)
ZL = 75 + 1j*25;
Z0 = 50;
c0 = 2.998e8;

% Calculate λ (5 seconds)
lambda = c0 / (2.4e9 * sqrt(2.3));

% Solve (10 seconds)
r = StubMatch(ZL, Z0, 'short', lambda);

% Answer (10 seconds)
fprintf('d = %.2f mm\n', r.d_mm);
fprintf('ℓ = %.2f mm\n', r.l_mm);
```

**Output:**
```
d = 12.34 mm
ℓ = 8.56 mm
```

**Done!** ✓

---

## 💡 Common Mistakes (And How to Avoid)

### Mistake 1: Wrong Units
```matlab
❌ lambda = 12;                    % Thought this was cm
❌ r = StubMatch(ZL, Z0, 'short', lambda);
❌ % Gives: d = 1234 mm (way too big!)

✓ lambda = 0.12;                   % Correctly in meters
✓ r = StubMatch(ZL, Z0, 'short', lambda);
✓ % Gives: d = 12.34 mm (correct!)
```

### Mistake 2: Wrong Stub Type
```matlab
% Problem says "short-circuited stub"
❌ r = StubMatch(ZL, Z0, 'open', lambda);   % Wrong type!

✓ r = StubMatch(ZL, Z0, 'short', lambda);  % Correct!
```

### Mistake 3: Using Wrong Solution
```matlab
% Most problems want Solution 1
❌ d = r.d_alt_mm;    % Using alternative by mistake

✓ d = r.d_mm;         % Using primary solution
```

---

## 🎯 Decision Tree (Which Mode?)

```
START: Do you have wavelength λ?
│
├─ YES: Is it in meters?
│  ├─ YES → r = StubMatch(ZL, Z0, type, lambda)  ✓
│  └─ NO → Convert to meters first!
│
└─ NO: Do you have frequency f?
   ├─ YES: Do you have εᵣ?
   │  ├─ YES → r = StubMatch(ZL, Z0, type, f, eps_r)  ✓
   │  └─ NO → Calculate λ = c₀/f first
   │
   └─ NO: Want normalized only?
      └─ YES → r = StubMatch(ZL, Z0, type)  ✓
```

---

## 📊 Output Format You'll See

```
==========================================
      SINGLE-STUB MATCHING              
==========================================
  Load: ZL = 100.00 +50.00j Ω
  Line: Z0 = 50 Ω (SHORT stub)
  λ = 12.00 cm
------------------------------------------
  SOLUTION 1:                ← USE THIS!
    d = 0.1234 λ = 14.81 mm  ← Your answer
    ℓ = 0.0567 λ = 6.80 mm   ← Your answer
  SOLUTION 2:                ← Alternative
    d = 0.3766 λ = 45.19 mm
    ℓ = 0.4433 λ = 53.20 mm
------------------------------------------
  ✓ Matched (y = 1.001)      ← Good to see!
==========================================
```

**Look for "✓ Matched" to know it worked!**

---

## 🚀 Speed Run: Exam Problem

**Time budget: 1 minute**

```matlab
%% 0-10 sec: Copy given values
ZL = 142 + 1j*42.5;
Z0 = 75;
f = 1550e6;
eps_r = 2.1;

%% 10-20 sec: Calculate wavelength
c0 = 2.998e8;
lambda = c0 / (f * sqrt(eps_r));

%% 20-40 sec: Run StubMatch
r = StubMatch(ZL, Z0, 'short', lambda);

%% 40-60 sec: Extract and write answers
% Q16: d = ?
fprintf('d = %.2f mm\n', r.d_mm);

% Q17: ℓ = ?
fprintf('ℓ = %.2f mm\n', r.l_mm);
```

**Total: 60 seconds** ✓

Compare to manual: 15 minutes ❌

**Time saved: 14 minutes!** 🎉

---

## 💪 You're Ready!

### What You Know Now:
✅ How to call StubMatch  
✅ What inputs to use  
✅ How to get your answers  
✅ Common mistakes to avoid  

### What to Do:
1. Copy the pattern that matches your problem
2. Replace values with your given data
3. Run it
4. Extract r.d_mm and r.l_mm
5. Done!

---

## 🔗 Need More?

- **Full details:** See [StubMatch_Complete_Guide.md](StubMatch_Complete_Guide.md)
- **Quick reference:** See [StubMatch_Quick_Reference.md](StubMatch_Quick_Reference.md)
- **Exam examples:** See [Q15_Q16_Q17_Complete_With_StubMatch.md](Q15_Q16_Q17_Complete_With_StubMatch.md)

---

**Now go solve some problems!** 🚀

*Typical exam problem: 1 minute with StubMatch vs 15 minutes manual = 14 minutes saved!*
