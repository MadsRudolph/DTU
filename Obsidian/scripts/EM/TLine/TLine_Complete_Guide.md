# TLine.m - Complete Guide

> **Comprehensive Reference for All 10 Modes**  
> Master transmission line analysis completely

---

## 📖 Quick Navigation

- [Mode 1: Full Analysis](#mode-1-full-transmission-line-analysis)
- [Mode 2: Impedance Transform](#mode-2-impedance-transformation)
- [Mode 3: Gamma/Z Conversion](#mode-3-reflection-coefficient-conversion)
- [Mode 4: Find Load (Q13/Q14)](#mode-4-find-load-from-input-q1314)
- [Mode 5: Quarter-Wave](#mode-5-quarter-wave-transformer)
- [Mode 6: Special Lengths](#mode-6-special-lengths)
- [Mode 7: Series Element (Q11)](#mode-7-series-element-q11)
- [Mode 8: Shunt Element](#mode-8-shunt-element)
- [Mode 9: Complex Circuit](#mode-9-complex-circuit)
- [Mode 10: Stub Design (Q12)](#mode-10-stub-design-q12)

---

## Mode 1: Full Transmission Line Analysis

**Purpose:** Complete TL analysis - Z_in, Γ, VSWR, everything

### Syntax
```matlab
r = TLine(Z0, ZL, len_lambda)              % Length in wavelengths
r = TLine(Z0, ZL, len_m, freq, vp)         % Length in meters
r = TLine(Z0, ZL, len_m, freq, vp, alpha)  % Lossy line
```

### Parameters
- `Z0` - Characteristic impedance (Ω)
- `ZL` - Load impedance (Ω)
- `len_lambda` - Length in wavelengths
- `len_m` - Length in meters
- `freq` - Frequency (Hz)
- `vp` - Phase velocity (m/s)
- `alpha` - Attenuation constant (Np/m, optional)

### Example
```matlab
% 50Ω line, 100Ω load, 0.3λ long
r = TLine(50, 100, 0.3);

% Access results:
r.Z_in          % Input impedance
r.Gamma_L       % Load reflection coefficient
r.Gamma_in      % Input reflection coefficient
r.VSWR          % Voltage standing wave ratio
r.z_vmax        % Distance to first Vmax (λ)
r.z_vmin        % Distance to first Vmin (λ)
r.P_delivered   % Power delivered
r.RL_dB         % Return loss (dB)
```

### Key Formulas
```
Z_in = Z₀(Z_L + jZ₀tan(βℓ))/(Z₀ + jZ_Ltan(βℓ))
Γ_in = Γ_L × exp(-j2βℓ)
VSWR = (1 + |Γ|)/(1 - |Γ|)
```

---

## Mode 2: Impedance Transformation

**Purpose:** Find Z_in given Z_L, or vice versa

### Syntax
```matlab
r = TLine('Zin', Z0, ZL, len_lambda)   % Find input impedance
r = TLine('ZL', Z0, Zin, len_lambda)   % Find load impedance
```

### Example
```matlab
% Find Z_in at 0.25λ from 100Ω load on 50Ω line
r = TLine('Zin', 50, 100, 0.25);
r.Z_in  % = 25 Ω (quarter-wave inverts)

% Reverse: Find Z_L given Z_in
r = TLine('ZL', 50, 25, 0.25);
r.ZL    % = 100 Ω
```

---

## Mode 3: Reflection Coefficient Conversion

**Purpose:** Convert between Γ and Z, or propagate Γ

### Syntax
```matlab
r = TLine('Gamma', Z0, Z)                 % Z → Γ
r = TLine('Z', Z0, Gamma)                 % Γ → Z
r = TLine('Gamma_in', Gamma_L, len)       % Propagate L→Input
r = TLine('Gamma_L', Gamma_in, len)       % Propagate Input→L
```

### Example
```matlab
% Convert impedance to Gamma
r = TLine('Gamma', 50, 75+1j*25);
r.Gamma  % Complex reflection coefficient

% Propagate Gamma toward source
Gamma_L = 0.5*exp(1j*pi/6);
r = TLine('Gamma_in', Gamma_L, 0.3);
r.Gamma_in  % At input (0.3λ from load)
```

### Key Formulas
```
Γ = (Z - Z₀)/(Z + Z₀)
Z = Z₀(1 + Γ)/(1 - Γ)
Γ_in = Γ_L × exp(-j2βℓ)
```

---

## Mode 4: Find Load from Input (Q13/Q14)

**Purpose:** Given Γ at input, find Γ_L and Z_L (solves Q13 AND Q14!)

### Syntax
```matlab
r = TLine('load', Z0, Gamma_A, len_lambda)
```

### Example
```matlab
% Q13/Q14 exam problem
Gamma_A = 0.539 * exp(1j*deg2rad(166));
r = TLine('load', 75, Gamma_A, 0.3);

% Q13 answer:
r.Gamma_L  % Reflection coefficient at load

% Q14 answer:
r.Z_L      % Load impedance
```

### Physics
```
Γ_L = Γ_A × exp(+j2βℓ)  [Note: POSITIVE phase shift toward load]
Z_L = Z₀(1 + Γ_L)/(1 - Γ_L)
```

---

## Mode 5: Quarter-Wave Transformer

**Purpose:** Design matching transformer

### Syntax
```matlab
r = TLine('QW', Z_source, Z_load)
```

### Example
```matlab
% Match 50Ω to 200Ω
r = TLine('QW', 50, 200);
r.Z_qw  % = 100 Ω (required transformer impedance)
```

### Formula
```
Z_QW = √(Z_source × Z_load)
```

---

## Mode 6: Special Lengths

**Purpose:** Quick calculation for λ/4 or λ/2 lines

### Syntax
```matlab
r = TLine('lambda/4', Z0, ZL)  % Quarter-wave
r = TLine('lambda/2', Z0, ZL)  % Half-wave
```

### Example
```matlab
% λ/4: Impedance inversion
r = TLine('lambda/4', 50, 200);
r.Z_in  % = 12.5 Ω = Z₀²/Z_L

% λ/2: Transparency
r = TLine('lambda/2', 50, 200);
r.Z_in  % = 200 Ω = Z_L
```

---

## Mode 7: Series Element (Q11)

**Purpose:** TL with series C or L at input

### Syntax
```matlab
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp)
r = TLine('series_L', Z0, ZL, len_m, L, freq, vp)
```

### Example (Q11 Exam)
```matlab
c0 = 3e8;
r = TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0);

% Results:
r.Z_TL      % TL input impedance
r.Z_element % Capacitor impedance
r.Z_A       % Total impedance (Q11 answer)
```

### Formula
```
Z_A = Z_C + Z_TL  (series)
where Z_C = 1/(jωC), Z_L = jωL
```

---

## Mode 8: Shunt Element

**Purpose:** TL with shunt C or L at input

### Syntax
```matlab
r = TLine('shunt_C', Z0, ZL, len_m, C, freq, vp)
r = TLine('shunt_L', Z0, ZL, len_m, L, freq, vp)
```

### Example
```matlab
r = TLine('shunt_C', 50, 75, 0.1, 2e-12, 10e9, 2e8);
r.Z_A  % Total input impedance
```

### Formula
```
Y_A = Y_C + Y_TL  (shunt)
Z_A = 1/Y_A
```

---

## Mode 9: Complex Circuit

**Purpose:** Multiple elements in sequence

### Syntax
```matlab
r = TLine('circuit', Z0, ZL, len_m, freq, vp, ...
          'series_C', C1, 'shunt_L', L1, ...)
```

### Example
```matlab
r = TLine('circuit', 50, 100, 0.1, 10e9, 2e8, ...
          'series_C', 1e-12, 'shunt_L', 5e-9);
r.Z_A  % Final impedance after all elements
```

---

## Mode 10: Stub Design (Q12)

**Purpose:** Find stub length to realize target impedance

### Syntax
```matlab
r = TLine('stub', Z_target, Z0)              % Both short & open
r = TLine('stub', Z_target, Z0, 'short')     % Short only
r = TLine('stub', Z_target, Z0, 'open')      % Open only
```

### Example (Q12 Exam)
```matlab
r = TLine('stub', 1j*30, 75, 'short');
r.short.len_lambda  % Stub length (Q12 answer)
r.short.beta_l_deg  % Electrical angle
```

### Formulas
```
Short stub: Z_in = jZ₀tan(βℓ)
Open stub:  Z_in = -jZ₀cot(βℓ)
```

---

## Complete Output Reference

### Basic Analysis Mode
```matlab
r.Z0, r.ZL, r.len_lambda
r.Z_in          ⭐ Input impedance
r.Gamma_L       ⭐ Load Gamma
r.Gamma_in      ⭐ Input Gamma
r.VSWR          ⭐ VSWR
r.z_vmax        Distance to Vmax (λ)
r.z_vmin        Distance to Vmin (λ)
r.P_delivered   Power fraction
r.RL_dB         Return loss (dB)
```

### Q13/Q14 Mode
```matlab
r.Gamma_L       ⭐ Q13 answer
r.Z_L           ⭐ Q14 answer
r.VSWR          Bonus info
```

### Q11 Mode (series/shunt)
```matlab
r.Z_A           ⭐ Q11 answer
r.Z_TL          TL input impedance
r.Z_element     Element impedance
```

### Q12 Mode (stub)
```matlab
r.short.len_lambda      ⭐ Q12 answer (short)
r.open.len_lambda       Alternative (open)
r.short.beta_l_deg      Electrical angle
```

---

## Quick Reference Table

| Task | Mode | Syntax | Output |
|------|------|--------|--------|
| Basic analysis | 1 | `TLine(Z0, ZL, len)` | `r.Z_in`, `r.VSWR` |
| Q13/Q14 | 4 | `TLine('load', Z0, Γ_A, len)` | `r.Gamma_L`, `r.Z_L` |
| Q11 | 7 | `TLine('series_C', ...)` | `r.Z_A` |
| Q12 | 10 | `TLine('stub', Z, Z0, 'short')` | `r.short.len_lambda` |
| QW design | 5 | `TLine('QW', Z1, Z2)` | `r.Z_qw` |
| Get Γ from Z | 3 | `TLine('Gamma', Z0, Z)` | `r.Gamma` |

---

[← Master Index](TLine_MASTER_INDEX.md)
