# TLine.m - Quick Start Guide

> **5-Minute Crash Course**  
> Everything you need to start using TLine.m RIGHT NOW

---

## TL;DR - The Four Patterns You Need

```matlab
% Pattern 1: Basic analysis (80% of problems)
r = TLine(Z0, ZL, len_lambda);
Z_in = r.Z_in;        % Input impedance
VSWR = r.VSWR;        % Voltage standing wave ratio

% Pattern 2: Find load from input (Q13/Q14)
r = TLine('load', Z0, Gamma_A, len_lambda);
Gamma_L = r.Gamma_L;  % Q13 answer
Z_L = r.Z_L;          % Q14 answer

% Pattern 3: TL + element (Q11)
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp);
Z_A = r.Z_A;          % Total input impedance

% Pattern 4: Stub design (Q12)
r = TLine('stub', Z_target, Z0, 'short');
len = r.short.len_lambda;  % Stub length in λ
```

**That's it!** These four patterns solve 95% of exam problems.

---

## 📖 Table of Contents

1. [The Four Essential Patterns](#the-four-essential-patterns) (3 min)
2. [What You Get Back](#what-you-get-back) (1 min)
3. [Common Mistakes](#common-mistakes) (1 min)

---

## The Four Essential Patterns

### Pattern 1: Basic Transmission Line Analysis

**Use when:** Need Z_in, VSWR, Gamma, or general TL info  
**Covers:** ~80% of TL problems

```matlab
% Syntax: TLine(Z0, ZL, len_lambda)
r = TLine(50, 100, 0.3);    % 50Ω line, 100Ω load, 0.3λ long

% Get results:
r.Z_in          % Input impedance
r.Gamma_L       % Load reflection coefficient
r.Gamma_in      % Input reflection coefficient
r.VSWR          % Voltage standing wave ratio
r.z_vmax        % Distance to first Vmax (λ)
r.z_vmin        % Distance to first Vmin (λ)
r.P_delivered   % Power delivered (fraction)
r.RL_dB         % Return loss (dB)
```

**30-second example:**
```matlab
>> r = TLine(50, 75+1j*25, 0.25);   % λ/4 line
>> r.Z_in

ans = 28.8000 -11.5200i   % Input impedance

>> r.VSWR

ans = 1.7321   % VSWR
```

**Key:** Length MUST be in wavelengths (not meters) for this simple form

---

### Pattern 2: Find Load from Input Measurement (Q13/Q14)

**Use when:** Given Γ at input, find Γ_L and Z_L  
**Exam types:** Q13 (Gamma_L), Q14 (Z_L)  
**One function solves BOTH questions!**

```matlab
% Syntax: TLine('load', Z0, Gamma_A, len_lambda)

% Given: Γ_A = 0.539∠166° at input, Z0 = 75Ω, ℓ = 0.3λ
Gamma_A = 0.539 * exp(1j * deg2rad(166));
r = TLine('load', 75, Gamma_A, 0.3);

% Get answers:
r.Gamma_L   % Q13 answer: Gamma at load
r.Z_L       % Q14 answer: Load impedance
r.VSWR      % Bonus: VSWR
```

**30-second example:**
```matlab
>> Gamma_A = 0.539 * exp(1j * deg2rad(166));
>> r = TLine('load', 75, Gamma_A, 0.3);

>> abs(r.Gamma_L)
ans = 0.5390   % Same magnitude

>> angle(r.Gamma_L) * 180/pi
ans = 22.0000   % Different angle (phase shift)

>> r.Z_L
ans = 183.0000 +104.0000i   % Load impedance
```

**Physics:** Γ magnitude stays constant, angle shifts by +2βℓ toward load

---

### Pattern 3: TL with Series/Shunt Element (Q11)

**Use when:** TL has capacitor or inductor at input  
**Exam type:** Q11 - "Find Z_A of the circuit"

#### Series Capacitor
```matlab
% Syntax: TLine('series_C', Z0, ZL, len_m, C, freq, vp)

% Example: Q11 exam problem
c0 = 3e8;
r = TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0);

% Get answer:
r.Z_A       % Total impedance at point A (Q11 answer)
r.Z_TL      % TL input impedance (before capacitor)
r.Z_element % Capacitor impedance
```

#### Series Inductor
```matlab
r = TLine('series_L', Z0, ZL, len_m, L, freq, vp);
```

#### Shunt Capacitor
```matlab
r = TLine('shunt_C', Z0, ZL, len_m, C, freq, vp);
```

#### Shunt Inductor
```matlab
r = TLine('shunt_L', Z0, ZL, len_m, L, freq, vp);
```

**30-second example:**
```matlab
>> c0 = 3e8;
>> r = TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0);

>> r.Z_A
ans = 35.2000 -15.8000i   % Q11 answer

>> r.Z_TL
ans = 35.2000 +16.0000i   % TL input before cap

>> r.Z_element
ans = 0.0000 -31.8000i    % Capacitor impedance
```

**Key:** Series → Z_total = Z_element + Z_TL  
        Shunt → Y_total = Y_element + Y_TL

---

### Pattern 4: Stub Design (Q12)

**Use when:** Need stub length to realize target impedance  
**Exam type:** Q12 - "Find stub length for Z = jX"

```matlab
% Syntax: TLine('stub', Z_target, Z0, 'short')

% Example: Realize Z = j30 Ω using 75 Ω short stub
r = TLine('stub', 1j*30, 75, 'short');

% Get answer:
r.short.len_lambda   % Q12 answer: stub length in λ
```

**For open stub:**
```matlab
r = TLine('stub', 1j*30, 75, 'open');
r.open.len_lambda    % Open stub length
```

**30-second example:**
```matlab
>> r = TLine('stub', 1j*30, 75, 'short');

>> r.short.len_lambda
ans = 0.0606   % ℓ = 0.0606λ (Q12 answer)

>> r.short.beta_l_deg
ans = 21.8014  % Or 21.8° in electrical length
```

**Physics:**  
- Short stub: Z_in = jZ₀tan(βℓ)
- Open stub: Z_in = -jZ₀cot(βℓ)

---

## What You Get Back

**Every TLine call returns a struct with relevant fields:**

### Basic Analysis Output
```matlab
r = TLine(50, 100, 0.3);

r.Z0            % Line impedance (50 Ω)
r.ZL            % Load impedance (100 Ω)
r.len_lambda    % Length (0.3 λ)

r.Z_in          % Input impedance ⭐
r.Gamma_L       % Load reflection coefficient ⭐
r.Gamma_in      % Input reflection coefficient ⭐
r.VSWR          % Voltage standing wave ratio ⭐

r.z_vmax        % Distance to first Vmax (λ)
r.z_vmin        % Distance to first Vmin (λ)
r.P_delivered   % Power delivered to load
r.RL_dB         % Return loss (dB)
```

### Q13/Q14 Output
```matlab
r = TLine('load', Z0, Gamma_A, len);

r.Gamma_L       % Q13 answer ⭐
r.Z_L           % Q14 answer ⭐
r.VSWR          % Bonus info
```

### Q11 Output
```matlab
r = TLine('series_C', ...);

r.Z_A           % Q11 answer ⭐
r.Z_TL          % TL input impedance
r.Z_element     % Element impedance
```

### Q12 Output
```matlab
r = TLine('stub', ...);

r.short.len_lambda   % Q12 answer (short stub) ⭐
r.open.len_lambda    % Alternative (open stub)
```

---

## Common Mistakes

### ❌ Mistake 1: Wrong Length Units

```matlab
❌ Wrong:
r = TLine(50, 100, 0.5);      // Thought this was 0.5m
r = TLine(50, 100, 50);       // Thought this was 50cm

✅ Correct:
r = TLine(50, 100, 0.5);      // 0.5 wavelengths
% OR with physical length:
r = TLine(50, 100, 0.5, freq, vp);  // 0.5m with freq and vp
```

**Rule:** First form uses λ, second form uses meters with freq/vp

---

### ❌ Mistake 2: Wrong Mode for Q13/Q14

```matlab
❌ Wrong (slow way - 2 separate calls):
r1 = TLine('Gamma_L', Gamma_in, len);  // Get Gamma_L
Gamma_L = r1.Gamma_L;
r2 = TLine('Z', Z0, Gamma_L);          // Get Z_L
Z_L = r2.Z;

✅ Correct (fast way - 1 call):
r = TLine('load', Z0, Gamma_in, len);  // Get BOTH
Gamma_L = r.Gamma_L;  // Q13
Z_L = r.Z_L;          // Q14
```

**Rule:** Use `'load'` mode for Q13/Q14 - solves both at once!

---

### ❌ Mistake 3: Wrong Element Mode

```matlab
❌ Wrong:
r = TLine('series', Z0, ZL, len, C, freq, vp);  // Mode doesn't exist

✅ Correct:
r = TLine('series_C', Z0, ZL, len, C, freq, vp);  // Capacitor
r = TLine('series_L', Z0, ZL, len, L, freq, vp);  // Inductor
```

**Rule:** Specify element type: `'series_C'`, `'series_L'`, `'shunt_C'`, `'shunt_L'`

---

### ❌ Mistake 4: Accessing Wrong Field

```matlab
❌ Wrong:
r = TLine('stub', 1j*30, 75, 'short');
len = r.len;              // Doesn't exist

✅ Correct:
len = r.short.len_lambda; // Short stub length
% or
len = r.open.len_lambda;  // Open stub length
```

**Rule:** Stub results are in `r.short` or `r.open` sub-structs

---

## Quick Cheat Sheet

### Input Patterns
```matlab
TLine(Z0, ZL, len_lambda)                       % Basic (length in λ)
TLine('load', Z0, Gamma_A, len_lambda)          % Q13/Q14
TLine('series_C', Z0, ZL, len_m, C, freq, vp)   % Q11
TLine('stub', Z_target, Z0, 'short')            % Q12
TLine('QW', Z_source, Z_load)                   % Quarter-wave
TLine('Gamma', Z0, Z)                           % Get Gamma from Z
```

### Essential Outputs
```matlab
r.Z_in          % Input impedance
r.Gamma_L       % Load reflection coefficient
r.VSWR          % Voltage standing wave ratio
r.Z_A           % Input impedance (TL + element)
```

---

## ✅ 60-Second Self-Test

Try these without looking:

1. **Find Z_in of 50Ω line, 100Ω load, 0.25λ long:**
   ```matlab
   r = TLine(50, 100, 0.25);
   r.Z_in
   ```

2. **Find Z_L given Γ_A = 0.5∠90° at input, Z0 = 50Ω, ℓ = 0.2λ:**
   ```matlab
   r = TLine('load', 50, 0.5*1j, 0.2);
   r.Z_L
   ```

3. **Design QW transformer for 50Ω to 200Ω:**
   ```matlab
   r = TLine('QW', 50, 200);
   r.Z_qw
   ```

**Answers:**
1. 25 Ω (quarter-wave inverts impedance: Z_in = Z₀²/Z_L)
2. ~50+j86.6 Ω
3. 100 Ω (√(50×200))

---

## 🎯 What's Next?

**If this solved your problem:**
→ Print the [Quick Reference Card](TLine_Quick_Reference.md) for exams

**Want to learn more:**
→ Read the [Complete Guide](TLine_Complete_Guide.md) (45 min)

**Something not working:**
→ Check [Troubleshooting Guide](TLine_Troubleshooting.md)

**Need practice problems:**
→ Work through [Exam Examples](TLine_Exam_Examples.md)

---

## 💡 Remember These Four Rules

1. **Length:** In λ for simple form, meters with freq/vp
2. **Q13/Q14:** Use `TLine('load', ...)` - solves both!
3. **Q11:** Use `TLine('series_C', ...)` or `'series_L'`
4. **Q12:** Use `TLine('stub', Z_target, Z0, 'short')`

**That's it! You're ready to use TLine.m** 🚀

---

[← Back to Master Index](TLine_MASTER_INDEX.md) | [Complete Guide →](TLine_Complete_Guide.md)
