# StubMatch Troubleshooting Guide

## 🔧 Quick Problem Solver

**Having issues with StubMatch?** Find your problem below and jump to the solution.

---

## 📋 Error Quick Finder

| Symptom | Jump To |
|---------|---------|
| Outputs are huge (d = 1234 mm) | [#wrong-units](#wrong-units) |
| "✓ Matched" doesn't appear | [#no-match](#no-match) |
| Gets NaN or empty results | [#no-solution](#no-solution) |
| Different from manual calculation | [#different-results](#different-results) |
| Two solutions - which one? | [#which-solution](#which-solution) |
| Stub length > 0.5λ | [#long-stub](#long-stub) |
| Results don't match answer choices | [#wrong-answer](#wrong-answer) |

---

## 🚨 Problem 1: Outputs Are Huge <a name="wrong-units"></a>

### Symptom
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
fprintf('d = %.2f mm\n', r.d_mm);
% Output: d = 1337.00 mm  ← Way too large!
```

### Cause
**You used wavelength in centimeters instead of meters!**

### Diagnosis
```matlab
% You probably did this:
lambda = 12;  % Thought: "12 cm from the problem"

% StubMatch expects METERS:
lambda = 0.12;  % Correct: 12 cm = 0.12 m
```

### Fix
```matlab
❌ WRONG:
lambda = 13.3;  % cm - will give huge errors
r = StubMatch(ZL, Z0, 'short', lambda);

✓ CORRECT:
lambda = 0.133;  % meters (13.3 cm)
r = StubMatch(ZL, Z0, 'short', lambda);
```

### Prevention
```matlab
% Always convert explicitly:
lambda_cm = 13.3;              % What the problem gives
lambda_m = lambda_cm / 100;    % Convert to meters
r = StubMatch(ZL, Z0, 'short', lambda_m);
```

### Quick Check
```matlab
% Reasonable ranges for typical problems:
% λ should be: 0.01 to 1 meter (1 cm to 100 cm)
% d should be: 1 to 100 mm (typically)
% ℓ should be: 1 to 100 mm (typically)

% If you see d = 1234 mm, lambda was probably wrong!
```

---

## 🚨 Problem 2: No Match Indicator <a name="no-match"></a>

### Symptom
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
% Output shows:
% Check: y = 0.523 -0.234j  ← Not matched!
```

Instead of:
```
✓ Matched (y = 1.001)  ← Should see this
```

### Possible Causes

#### Cause 1: Wrong Stub Type
```matlab
% Problem says "short-circuited stub"
❌ r = StubMatch(ZL, Z0, 'open', lambda);   % Wrong!

✓ r = StubMatch(ZL, Z0, 'short', lambda);  % Correct
```

**Fix:** Check problem statement for stub type.

#### Cause 2: Typo in ZL
```matlab
% Problem: ZL = 100 + j50
❌ ZL = 100 - 1j*50;  % Wrong sign!
❌ ZL = 10 + 1j*50;   % Wrong magnitude!
❌ ZL = 100 + 1j*5;   // Wrong imaginary part!

✓ ZL = 100 + 1j*50;   // Correct
```

**Fix:** Double-check your ZL input.

#### Cause 3: Numerical Tolerance
```matlab
% This is actually OK:
% Check: y = 1.001 +0.002j  ← Close enough!

% This is not OK:
% Check: y = 0.523 -0.234j  ← Way off!
```

**Fix:** If y is within 0.01 of 1.0, it's fine. Otherwise, check inputs.

### Diagnosis Steps

```matlab
% Step 1: Verify inputs
fprintf('ZL = %.2f %+.2fj\n', real(ZL), imag(ZL));
fprintf('Z0 = %.2f\n', Z0);
fprintf('Type: %s\n', stub_type);
fprintf('Lambda: %.4f m\n', lambda);

% Step 2: Check if match quality is acceptable
y_check = r.Y_in_check * r.Z0;
error = abs(y_check - 1);
fprintf('Match error: %.4f\n', error);

if error < 0.01
    fprintf('✓ Good enough!\n');
else
    fprintf('❌ Check your inputs!\n');
end
```

---

## 🚨 Problem 3: NaN or Empty Results <a name="no-solution"></a>

### Symptom
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
fprintf('d = %.2f\n', r.d);
% Output: d = NaN
```

### Possible Causes

#### Cause 1: Load Already Matched
```matlab
% If ZL = Z0, no stub needed!
ZL = 50;
Z0 = 50;
r = StubMatch(ZL, Z0, 'short');
% Returns NaN - load already matched

✓ Check: abs(ZL - Z0) > 0.01
```

#### Cause 2: Pure Real Load
```matlab
% For pure resistance, use λ/4 transformer instead
ZL = 100;      % No imaginary part
Z0 = 50;
% Stub matching may not be appropriate

✓ Use: TLine('QW', Z0, ZL)  % Quarter-wave transformer
```

#### Cause 3: Extreme Impedance
```matlab
% Very large or very small impedances
ZL = 1e6 + 1j*1e6;  % Huge
Z0 = 50;
% Numerical solver may fail

✓ Check if impedances are realistic
```

### Fix
```matlab
% For pure real loads:
if abs(imag(ZL)) < 0.01
    fprintf('Pure real load - use λ/4 transformer\n');
    r_qw = TLine('QW', Z0, real(ZL));
else
    r = StubMatch(ZL, Z0, 'short', lambda);
end
```

---

## 🚨 Problem 4: Different from Manual Calculation <a name="different-results"></a>

### Symptom
"I calculated d = 20 mm by hand, but StubMatch gives d = 25 mm"

### Possible Reasons

#### Reason 1: Different Solution
```matlab
% You found Solution 2, StubMatch shows Solution 1
r = StubMatch(ZL, Z0, 'short', lambda);

fprintf('Solution 1: d = %.1f mm\n', r.d_mm);
fprintf('Solution 2: d = %.1f mm\n', r.d_alt_mm);

% Check: Does your 20 mm match r.d_alt_mm?
```

#### Reason 2: Calculation Error
Manual calculations involve:
- Complex division (error-prone)
- Quadratic formula (two solutions!)
- Sign errors
- Unit conversions

**Most likely:** Your manual calculation has an error.

**Fix:** Trust StubMatch (it's been validated).

#### Reason 3: Different Convention
```matlab
% Some books measure from generator, not load
% StubMatch measures from load

% If your textbook uses opposite convention:
d_from_generator = lambda/2 - r.d;
```

### Verification
```matlab
% Check both your calculation and StubMatch:
fprintf('Manual: d = 20 mm\n');
fprintf('StubMatch Solution 1: d = %.1f mm\n', r.d_mm);
fprintf('StubMatch Solution 2: d = %.1f mm\n', r.d_alt_mm);

% If neither matches, re-check manual calculation
% If Solution 2 matches, you found the other solution
```

---

## 🚨 Problem 5: Which Solution to Use? <a name="which-solution"></a>

### Symptom
"I have two solutions - which one is correct?"

### Understanding the Two Solutions

```
SOLUTION 1:  (preferred)
  d = 0.1234 λ = 14.81 mm
  ℓ = 0.0567 λ = 6.80 mm

SOLUTION 2:  (alternative)
  d = 0.3766 λ = 45.19 mm
  ℓ = 0.4433 λ = 53.20 mm
```

**Both are mathematically correct!**

### Decision Rules

#### Rule 1: Default to Solution 1
```matlab
% Unless told otherwise, use Solution 1
d = r.d_mm;    ✓ 
l = r.l_mm;    ✓
```

**Reasons:**
- Closer to load → less line loss
- Shorter total length
- Industry standard

#### Rule 2: If Problem Specifies
```matlab
% "Use solution closest to d = 40 mm"
if abs(r.d_mm - 40) < abs(r.d_alt_mm - 40)
    fprintf('Use Solution 1\n');
else
    fprintf('Use Solution 2\n');
end
```

#### Rule 3: Minimum Total Length
```matlab
total1 = r.d_mm + r.l_mm;
total2 = r.d_alt_mm + r.l_alt_mm;

if total1 < total2
    fprintf('Use Solution 1 (total = %.2f mm)\n', total1);
else
    fprintf('Use Solution 2 (total = %.2f mm)\n', total2);
end
```

#### Rule 4: Practical Constraints
```matlab
% "Stub position must be > 30 mm from load"
if r.d_mm > 30
    fprintf('Use Solution 1: d = %.2f mm\n', r.d_mm);
elseif r.d_alt_mm > 30
    fprintf('Use Solution 2: d = %.2f mm\n', r.d_alt_mm);
else
    fprintf('Neither solution meets constraint!\n');
end
```

### Summary
```
Use Solution 1 when:
✓ No specific requirement
✓ Want minimum loss
✓ Exam problem (default)

Use Solution 2 when:
✓ Specifically asked for
✓ Solution 1 blocked by obstacle
✓ Special design requirement
```

---

## 🚨 Problem 6: Stub Length > 0.5λ <a name="long-stub"></a>

### Symptom
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
% Shows: ℓ = 0.58 λ
```

"Isn't max stub length 0.5λ?"

### Explanation

**For practical stubs:**
- Typical range: 0 < ℓ < 0.5λ
- But mathematically: ℓ can be > 0.5λ

**Why?** Stub admittance is **periodic** with period 0.5λ.

### Fix

```matlab
% Reduce by 0.5λ if needed:
if r.l > 0.5
    l_reduced = r.l - 0.5;
    fprintf('Original: ℓ = %.4f λ\n', r.l);
    fprintf('Reduced:  ℓ = %.4f λ\n', l_reduced);
end
```

**Example:**
```
ℓ = 0.58 λ  →  Equivalent to 0.08 λ
ℓ = 0.73 λ  →  Equivalent to 0.23 λ
```

### When This Happens
Usually with **Solution 2** (alternative solution):
```
SOLUTION 2:
  ℓ = 0.4433 λ  ← Still < 0.5λ (typical)
```

If ℓ > 0.5λ for Solution 1, might indicate unusual load impedance.

---

## 🚨 Problem 7: Doesn't Match Answer Choices <a name="wrong-answer"></a>

### Symptom
```matlab
r = StubMatch(ZL, Z0, 'short', lambda);
fprintf('d = %.2f mm\n', r.d_mm);
% Output: d = 24.54 mm

% Answer choices:
% A) 12.3 mm
% B) 24.5 mm  ← Close but not exact
% C) 36.7 mm
% D) 48.9 mm
```

### Possible Issues

#### Issue 1: Rounding
```matlab
// Your result: 24.54 mm
// Choice B: 24.5 mm

// This is fine! Within rounding tolerance.
✓ Answer: B
```

#### Issue 2: Need Alternative Solution
```matlab
// Check Solution 2:
fprintf('Solution 1: d = %.2f mm\n', r.d_mm);
fprintf('Solution 2: d = %.2f mm\n', r.d_alt_mm);

// Maybe answer is Solution 2?
```

#### Issue 3: Wrong Parameter
```matlab
// You calculated d, but question asks for ℓ
❌ fprintf('Answer: %.2f mm\n', r.d_mm);   % Wrong parameter
✓ fprintf('Answer: %.2f mm\n', r.l_mm);   % Correct parameter
```

#### Issue 4: Wrong Units
```matlab
// Question asks for cm, you gave mm
✓ fprintf('Answer: %.2f cm\n', r.d_mm/10);
```

### Systematic Check
```matlab
% Compare with all choices
choices_mm = [12.3, 24.5, 36.7, 48.9];

% Check d (Solution 1)
[~, idx] = min(abs(choices_mm - r.d_mm));
fprintf('d (Sol 1) matches choice %d: %.2f mm\n', idx, choices_mm(idx));

// Check d (Solution 2)
[~, idx] = min(abs(choices_mm - r.d_alt_mm));
fprintf('d (Sol 2) matches choice %d: %.2f mm\n', idx, choices_mm(idx));

% Check ℓ (Solution 1)
[~, idx] = min(abs(choices_mm - r.l_mm));
fprintf('ℓ (Sol 1) matches choice %d: %.2f mm\n', idx, choices_mm(idx));

% Check ℓ (Solution 2)
[~, idx] = min(abs(choices_mm - r.l_alt_mm));
fprintf('ℓ (Sol 2) matches choice %d: %.2f mm\n', idx, choices_mm(idx));
```

---

## 📋 Pre-Submission Checklist

Before you submit your answer, verify:

### Input Verification
```matlab
% 1. Is lambda in METERS?
assert(lambda < 1, 'Lambda too large - should be in meters!');
assert(lambda > 0.001, 'Lambda too small - check units!');

% 2. Is stub type correct?
fprintf('Stub type: %s\n', stub_type);
% Problem says "short" → verify stub_type = 'short'

% 3. Is ZL typed correctly?
fprintf('ZL = %.2f %+.2fj Ω\n', real(ZL), imag(ZL));
% Check against problem statement

% 4. Is Z0 correct?
fprintf('Z0 = %.2f Ω\n', Z0);
```

### Output Verification
```matlab
% 5. Does it show "✓ Matched"?
% Should see in output

% 6. Are results reasonable?
fprintf('d = %.4f λ = %.2f mm\n', r.d, r.d_mm);
fprintf('ℓ = %.4f λ = %.2f mm\n', r.l, r.l_mm);

% Typical ranges:
% d: 0.05λ to 0.45λ
% ℓ: 0.05λ to 0.45λ

% 7. Using correct solution?
% Default: Solution 1 (r.d_mm, r.l_mm)

% 8. Using correct parameter?
% Question asks for d → use r.d_mm
% Question asks for ℓ → use r.l_mm

% 9. Using correct units?
% mm, cm, or λ?
```

---

## 🔍 Diagnostic Script

**Run this to debug your StubMatch call:**

```matlab
function diagnose_stubmatch(ZL, Z0, stub_type, lambda)
    %% StubMatch Diagnostic Tool
    
    fprintf('\n=== STUBMATCH DIAGNOSTIC ===\n\n');
    
    % Check inputs
    fprintf('INPUTS:\n');
    fprintf('-------\n');
    fprintf('ZL = %.3f %+.3fj Ω\n', real(ZL), imag(ZL));
    fprintf('Z0 = %.3f Ω\n', Z0);
    fprintf('Stub type: %s\n', stub_type);
    
    if nargin >= 4
        fprintf('Lambda: %.4f m = %.2f cm\n', lambda, lambda*100);
        
        % Check if lambda reasonable
        if lambda > 1
            warning('Lambda > 1 m - Did you mean to use cm?');
        end
        if lambda < 0.001
            warning('Lambda < 1 mm - Seems too small');
        end
    end
    
    % Check load impedance
    fprintf('\nLOAD CHECK:\n');
    fprintf('-----------\n');
    if abs(ZL - Z0) < 0.01
        warning('ZL ≈ Z0 - Load already matched!');
    end
    
    if abs(imag(ZL)) < 0.01
        warning('ZL is purely real - consider λ/4 transformer');
    end
    
    % Run StubMatch
    fprintf('\nRUNNING STUBMATCH:\n');
    fprintf('------------------\n');
    
    if nargin >= 4
        r = StubMatch(ZL, Z0, stub_type, lambda);
    else
        r = StubMatch(ZL, Z0, stub_type);
    end
    
    % Check results
    fprintf('\nRESULTS CHECK:\n');
    fprintf('--------------\n');
    
    if isnan(r.d)
        error('No solution found! Check inputs.');
    end
    
    % Check match quality
    y_check = r.Y_in_check * r.Z0;
    error = abs(y_check - 1);
    
    fprintf('Match quality: %.4f\n', error);
    if error < 0.01
        fprintf('✓ Good match!\n');
    else
        warning('Poor match - check inputs!');
    end
    
    % Check if results reasonable
    if r.d > 0.5 || r.d < 0
        warning('d = %.4f λ outside typical range [0, 0.5λ]', r.d);
    end
    
    if r.l > 0.5 || r.l < 0
        warning('ℓ = %.4f λ outside typical range [0, 0.5λ]', r.l);
    end
    
    fprintf('\n=== END DIAGNOSTIC ===\n\n');
end

% Usage:
% diagnose_stubmatch(ZL, Z0, 'short', lambda);
```

---

## 🆘 Still Stuck?

### Step 1: Start Fresh
```matlab
clear all; clc;

% Type everything from scratch
% Don't copy-paste (might have hidden characters)
```

### Step 2: Use Example That Works
```matlab
% Known working example:
ZL = 142 + 1j*42.5;
Z0 = 75;
lambda = 0.1335;

r = StubMatch(ZL, Z0, 'short', lambda);
% Should give: d ≈ 24.5 mm, ℓ ≈ 19.4 mm

% If this doesn't work, installation issue
```

### Step 3: Check StubMatch Installation
```matlab
% Make sure StubMatch.m is in your path
which StubMatch
% Should show: /path/to/StubMatch.m

% If "not found":
addpath('path/to/Helpers');
```

### Step 4: Check MATLAB Version
```matlab
version
% StubMatch requires MATLAB R2016b or later
```

### Step 5: Read Complete Guide
See [StubMatch_Complete_Guide.md](StubMatch_Complete_Guide.md) for full details.

---

## 📞 Quick Help Reference

| Problem | Quick Fix |
|---------|-----------|
| d = 1234 mm (huge) | Lambda in cm, not meters |
| No "✓ Matched" | Wrong stub type or ZL typo |
| NaN result | Load matched or pure real |
| Doesn't match manual | Check both solutions |
| Which solution? | Default to Solution 1 |
| ℓ > 0.5λ | Can reduce by 0.5λ |
| Wrong answer | Check units, parameter, solution |

---

**Most problems solved by checking wavelength units!** ✓

*For complete guide, see [StubMatch_Complete_Guide.md](StubMatch_Complete_Guide.md)*
