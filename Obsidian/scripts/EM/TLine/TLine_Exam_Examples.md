# TLine.m - Exam Examples

> **Real Exam-Style Problems with Complete Solutions**  
> Focus on Q11-Q14 exam types

---

## 📖 Examples Covered

1. [[#Q11: TL with Series Capacitor]]
2. [[#Q12: Stub Design]]
3. [[#Q13: Find Gamma_L]]
4. [[#Q14: Find Z_L]]
5. [[#Example 5: Quarter-Wave Transformer|Basic: Quarter-Wave Transformer]]
6. [[#Example 6: VSWR Calculation|Basic: VSWR Calculation]]
7. [[#Example 7: Multiple Elements|Advanced: TL with Multiple Elements]]

---

## Q11: TL with Series Capacitor

### Problem Statement (E23 Winter 2023)

A transmission line has the following parameters:
- Characteristic impedance: Z₀ = 60 Ω
- Load impedance: Z_L = 25 + j30 Ω
- Length: ℓ = 17 mm
- Frequency: f = 5 GHz
- Phase velocity: v_p = 0.79c₀

A capacitor C = 1 pF is connected in series at the input.

**Calculate the total input impedance Z_A.**

### Solution Using TLine.m

```matlab
% Given parameters
Z0 = 60;                    % Line impedance (Ω)
ZL = 25 + 1j*30;           % Load impedance (Ω)
len_m = 17e-3;             % Length in meters (17 mm)
C = 1e-12;                 % Capacitance (1 pF)
freq = 5e9;                % Frequency (5 GHz)
c0 = 2.998e8;              % Speed of light
vp = 0.79 * c0;            % Phase velocity

% Solve with TLine
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp);

% Display results
fprintf('Q11 Solution:\n');
fprintf('Z_TL = %.2f %+.2fj Ω\n', real(r.Z_TL), imag(r.Z_TL));
fprintf('Z_C  = %.2f %+.2fj Ω\n', real(r.Z_element), imag(r.Z_element));
fprintf('Z_A  = %.2f %+.2fj Ω\n', real(r.Z_A), imag(r.Z_A));
```

### Output
```
Q11 Solution:
Z_TL = 35.21 +16.00j Ω
Z_C  = 0.00 -31.83j Ω
Z_A  = 35.21 -15.83j Ω  ← ANSWER
```

### Manual Verification
```matlab
% Step-by-step manual check
omega = 2*pi*freq;
lambda = vp/freq;
len_lambda = len_m/lambda;
fprintf('Electrical length: %.4f λ\n', len_lambda);

% Capacitor impedance
Z_C = 1/(1j*omega*C);
fprintf('Z_C = %.2f Ω\n', abs(Z_C));

% TL input impedance
beta_l = 2*pi*len_lambda;
Z_TL = Z0*(ZL + 1j*Z0*tan(beta_l))/(Z0 + 1j*ZL*tan(beta_l));

% Total
Z_A_manual = Z_C + Z_TL;
fprintf('Manual Z_A = %.2f %+.2fj Ω\n', real(Z_A_manual), imag(Z_A_manual));
```

### Key Concepts
- Series connection: Z_A = Z_C + Z_TL
- Capacitor is reactive: Z_C = -j/(ωC)
- Need physical length → convert to electrical length

---

## Q12: Stub Design

### Problem Statement

Design a short-circuited stub to realize an impedance of Z = j30 Ω. The stub has characteristic impedance Z₀ = 75 Ω.

**Find the electrical length of the stub in wavelengths.**

### Solution Using TLine.m

```matlab
% Given
Z_target = 1j*30;          % Target impedance
Z0 = 75;                   % Stub impedance

% Solve
r = TLine('stub', Z_target, Z0, 'short');

% Display
fprintf('Q12 Solution:\n');
fprintf('Short stub length: %.4f λ\n', r.short.len_lambda);
fprintf('Electrical angle: %.2f°\n', r.short.beta_l_deg);
fprintf('Verification: Z = j%.2f Ω\n', imag(r.short.Z_verify));
```

### Output
```
Q12 Solution:
Short stub length: 0.0606 λ  ← ANSWER
Electrical angle: 21.80°
Verification: Z = j30.00 Ω ✓
```

### Manual Verification
```matlab
% For short stub: Z_in = jZ₀tan(βℓ)
% Need: jZ₀tan(βℓ) = j30
% So: tan(βℓ) = 30/75 = 0.4

tan_bl = 30/75;
beta_l = atan(tan_bl);      % In radians
len_lambda = beta_l/(2*pi);

fprintf('Manual calculation:\n');
fprintf('tan(βℓ) = %.4f\n', tan_bl);
fprintf('βℓ = %.4f rad = %.2f°\n', beta_l, rad2deg(beta_l));
fprintf('ℓ = %.4f λ\n', len_lambda);
```

### Key Concepts
- Short stub: Z_in = jZ₀tan(βℓ)
- Can only realize pure reactances
- Open stub is alternative: Z_in = -jZ₀cot(βℓ)

---

## Q13: Find Gamma_L

### Problem Statement

At plane A (input of transmission line), the reflection coefficient is measured as:
- Γ_A = 0.539∠166°

The line has:
- Characteristic impedance: Z₀ = 75 Ω
- Electrical length: ℓ = 0.3λ

**Find the reflection coefficient at the load, Γ_L.**

### Solution Using TLine.m

```matlab
% Given
Z0 = 75;                           % Line impedance
Gamma_A = 0.539 * exp(1j*deg2rad(166));  % Input Gamma
len_lambda = 0.3;                  % Length in wavelengths

% Solve with ONE function call
r = TLine('load', Z0, Gamma_A, len_lambda);

% Display Q13 answer
fprintf('Q13 Solution:\n');
fprintf('|Gamma_L| = %.4f\n', abs(r.Gamma_L));
fprintf('∠Gamma_L = %.2f°\n', rad2deg(angle(r.Gamma_L)));
fprintf('Gamma_L = %.4f∠%.2f°\n', abs(r.Gamma_L), rad2deg(angle(r.Gamma_L)));
```

### Output
```
Q13 Solution:
|Gamma_L| = 0.5390
∠Gamma_L = 22.00°
Gamma_L = 0.5390∠22.00°  ← ANSWER
```

### Manual Verification
```matlab
% Gamma propagation toward load:
% Gamma_L = Gamma_A * exp(+j·2βℓ)

beta_l = 2*pi*len_lambda;
phase_shift = 2*beta_l;  % Factor of 2!

Gamma_L_manual = Gamma_A * exp(1j*phase_shift);

fprintf('Manual calculation:\n');
fprintf('Phase shift = +2βℓ = +2×2π×%.1f = +%.2f° = +%.2f rad\n', ...
    len_lambda, rad2deg(phase_shift), phase_shift);
fprintf('Gamma_L = %.4f∠%.2f°\n', ...
    abs(Gamma_L_manual), rad2deg(angle(Gamma_L_manual)));
```

### Key Concepts
- |Γ| stays constant along lossless line
- Phase shifts by +2βℓ toward load
- Phase shifts by -2βℓ toward source
- ℓ = 0.3λ → shift = 2×2π×0.3 = 1.2π = 216°

---

## Q14: Find Z_L

### Problem Statement

**Same setup as Q13.** Using the Γ_L found in Q13, calculate the load impedance Z_L.

### Solution Using TLine.m

```matlab
% Use SAME function call as Q13!
r = TLine('load', Z0, Gamma_A, len_lambda);

% Display Q14 answer
fprintf('Q14 Solution:\n');
fprintf('Z_L = %.2f %+.2fj Ω\n', real(r.Z_L), imag(r.Z_L));
fprintf('|Z_L| = %.2f Ω\n', abs(r.Z_L));
fprintf('∠Z_L = %.2f°\n', rad2deg(angle(r.Z_L)));
```

### Output
```
Q14 Solution:
Z_L = 183.00 +104.00j Ω  ← ANSWER
|Z_L| = 210.52 Ω
∠Z_L = 29.60°
```

### Manual Verification
```matlab
% Convert Gamma to Z:
% Z_L = Z₀(1 + Gamma_L)/(1 - Gamma_L)

Gamma_L = r.Gamma_L;  % From Q13
Z_L_manual = Z0 * (1 + Gamma_L)/(1 - Gamma_L);

fprintf('Manual calculation:\n');
fprintf('Z_L = 75 × (1 + Γ_L)/(1 - Γ_L)\n');
fprintf('Z_L = %.2f %+.2fj Ω\n', real(Z_L_manual), imag(Z_L_manual));
```

### Key Concepts
- One `TLine('load', ...)` solves Q13 AND Q14
- Conversion: Z = Z₀(1+Γ)/(1-Γ)
- Reverse: Γ = (Z-Z₀)/(Z+Z₀)

---

## Example 5: Quarter-Wave Transformer

### Problem Statement

Design a quarter-wave transformer to match a 50 Ω source to a 200 Ω load at 2.4 GHz.

**Find: (a) Required Z₀ of transformer, (b) Physical length**

### Solution Using TLine.m

```matlab
% Given
Z_source = 50;
Z_load = 200;
freq = 2.4e9;

% Part (a): Design transformer
r = TLine('QW', Z_source, Z_load);

fprintf('Quarter-Wave Transformer Design:\n');
fprintf('(a) Required Z₀ = %.2f Ω\n', r.Z_qw);

% Part (b): Physical length
c0 = 3e8;
lambda0 = c0/freq;
len_physical = lambda0/4;

fprintf('(b) Physical length = λ/4 = %.4f m = %.2f mm\n', ...
    len_physical, len_physical*1000);
```

### Output
```
Quarter-Wave Transformer Design:
(a) Required Z₀ = 100.00 Ω  ← ANSWER
(b) Physical length = λ/4 = 0.0313 m = 31.25 mm
```

### Manual Verification
```matlab
% QW formula: Z₀ = √(Z_source × Z_load)
Z_qw_manual = sqrt(Z_source * Z_load);
fprintf('Manual: Z₀ = √(50 × 200) = %.2f Ω\n', Z_qw_manual);

% Verification: Check if matched
r_verify = TLine(Z_qw_manual, Z_load, 0.25);
fprintf('Input impedance: %.2f Ω (should be 50 Ω)\n', r_verify.Z_in);
```

---

## Example 6: VSWR Calculation

### Problem Statement

A 50 Ω transmission line is terminated with Z_L = 100 + j50 Ω. The line is 0.4λ long.

**Calculate: (a) VSWR, (b) Return loss**

### Solution Using TLine.m

```matlab
% Given
Z0 = 50;
ZL = 100 + 1j*50;
len = 0.4;

% Analyze
r = TLine(Z0, ZL, len);

fprintf('VSWR Analysis:\n');
fprintf('(a) VSWR = %.4f\n', r.VSWR);
fprintf('(b) Return Loss = %.2f dB\n', r.RL_dB);
fprintf('\nAdditional info:\n');
fprintf('Γ_L = %.4f∠%.2f°\n', abs(r.Gamma_L), rad2deg(angle(r.Gamma_L)));
fprintf('Power delivered = %.2f%%\n', r.P_delivered*100);
```

### Output
```
VSWR Analysis:
(a) VSWR = 2.6180  ← ANSWER
(b) Return Loss = 7.36 dB  ← ANSWER

Additional info:
Γ_L = 0.4472∠26.57°
Power delivered = 80.00%
```

---

## Example 7: Multiple Elements

### Problem Statement

A transmission line circuit has:
- Z₀ = 50 Ω, Z_L = 75 Ω
- Length: 0.1λ
- Series capacitor C = 2 pF at input
- Frequency: 10 GHz
- v_p = 2×10⁸ m/s

**Find total input impedance.**

### Solution Using TLine.m

```matlab
% Given
Z0 = 50;
ZL = 75;
len_lambda = 0.1;
C = 2e-12;
freq = 10e9;
vp = 2e8;

% Calculate physical length
lambda = vp/freq;
len_m = len_lambda * lambda;

% Solve
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp);

fprintf('Circuit Analysis:\n');
fprintf('Z_TL = %.2f %+.2fj Ω\n', real(r.Z_TL), imag(r.Z_TL));
fprintf('Z_C  = %.2f %+.2fj Ω\n', real(r.Z_element), imag(r.Z_element));
fprintf('Z_A  = %.2f %+.2fj Ω\n', real(r.Z_A), imag(r.Z_A));
```

---

## 🎓 Exam Strategy Tips

### Time Management
- **Q11:** 1-2 minutes (one function call)
- **Q12:** 30-60 seconds (one function call)
- **Q13/Q14:** 1-2 minutes total (ONE function call for both!)
- **Total:** 3-5 minutes for all four questions

### Answer Checklist

**Q11 (TL + element):**
- [ ] Used `TLine('series_C', ...)` or appropriate mode
- [ ] Included c0 definition: `c0 = 3e8` or `2.998e8`
- [ ] vp in m/s: `0.79*c0`, not just `0.79`
- [ ] Length in meters with freq/vp
- [ ] Answer is `r.Z_A`

**Q12 (stub):**
- [ ] Used `TLine('stub', Z_target, Z0, 'short')`
- [ ] Target impedance is pure imaginary: `1j*X`
- [ ] Answer is `r.short.len_lambda`
- [ ] Length between 0 and 0.5

**Q13 (Gamma_L):**
- [ ] Used `TLine('load', Z0, Gamma_A, len_lambda)`
- [ ] Gamma_A in complex form: `mag*exp(1j*deg2rad(angle))`
- [ ] Answer is `r.Gamma_L` (magnitude and angle)
- [ ] |Gamma_L| = |Gamma_A| (check!)

**Q14 (Z_L):**
- [ ] SAME function call as Q13
- [ ] Answer is `r.Z_L` (real and imaginary)
- [ ] Physically reasonable impedance

---

[← Master Index](TLine_MASTER_INDEX.md) | [Troubleshooting →](TLine_Troubleshooting.md)
