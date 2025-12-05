---
title: EM MATLAB Helpers
type: helper
tags: [Electromagnetics, MATLAB, helpers]
aliases: [EM helpers, EM MATLAB toolbox]
links: [
  "Formulas/Plane Waves",
  "Formulas/Transmission Lines",
  "Formulas/Electrostatics & Magnetostatics"
]
updated: 2025-12-04
---
------

# EM MATLAB Helpers

> Central reference for all EM helper scripts.  
> When using any helper in an exercise/exam solution, reference this note.

---

## 🚀 Quick Start - How to Use These Helpers

**IMPORTANT:** Before using any helper function, add this line at the top of your MATLAB script or Live Script:

> [!warning] Remember
> 
> ```matlab
> % Add this at the top of your live script (one time)
> addpath('C:\Users\Mads2\DTU\3.semester\Electromagnetics\Helpers');
> ```

This tells MATLAB where to find your helper functions. Without this line, MATLAB will say "Undefined function or variable" when you try to call them.

**After adding the path, you can call any helper like:**

```matlab
r = Medium(4, 10e9);                    % Analyze medium properties
r = TLine(50, 100, 0.3);                % Transmission line analysis
r = Polarization([1; -1j; 0]);          % Polarization analysis
r = Fresnel(1, 4, 45);                  % Oblique incidence
r = StubMatch(100+1j*50, 50, 'short');  % Stub matching design
```

## Overview

Current helpers (consolidated toolkit):

|Function|Purpose|
|---|---|
|`Medium`|Wave parameters in materials (lossless/lossy/conductor)|
|`TLine`|Transmission line analysis (Z, Γ, VSWR, QW transformer)|
|`Polarization`|Wave polarization (type, handedness, axial ratio)|
|`Fresnel`|Reflection/transmission at interfaces|
|`StubMatch`|Single-stub impedance matching|
|`poynting_pw`|H-field phasor & Poynting vector (Q22-Q23 type)|
|`coulomb_pair`|Coulomb force between point charges|
|`B_inf_wire`|B-field around infinite wire|
|`rect2pol`|Complex number to polar form|
|`smithchart_plot`|Smith chart visualization|

Each subsection below explains:

- **When to use**
- **Inputs / outputs**
- **Quick usage examples**

---

## 1. `Medium` — Wave parameters in materials

### Purpose

This unified function calculates everything about **electromagnetic wave propagation in any material** - from perfect dielectrics to good conductors.

**What it calculates:**

- Attenuation constant (α) and phase constant (β)
- Wavelength (λ) and phase velocity (u_p)
- Intrinsic impedance (η)
- Loss tangent and material classification
- Skin depth (for lossy materials)

### When to use it

Use `Medium` when you see:

- **"A wave propagates through a material with ε_r = ... and σ = ..."**
- **"Find the wavelength in a dielectric..."**
- **"Calculate skin depth in copper..."**
- **"Classify the material as conductor or insulator..."**
- **"What is the attenuation constant?"**

### Signature & Modes

```matlab
% Lossless dielectric
Medium(eps_r, freq)
Medium(eps_r, freq, mu_r)

% Lossy medium
Medium(eps_r, sigma, freq)
Medium(eps_r, sigma, freq, mu_r)
Medium(eps_r, sigma, freq, mu_r, 'Name')

% From loss tangent
Medium('tand', eps_r, tan_delta, freq)

% Good conductor
Medium('conductor', sigma, freq)
Medium('conductor', sigma, freq, mu_r)

% Skin depth only
Medium('skin', sigma, freq)

% Free space
Medium('free', freq)
```

### Examples

```matlab
% Lossless glass at 10 GHz
Medium(4, 10e9)

% Seawater at 1 MHz
Medium(80, 4, 1e6, 1, 'Seawater')

% Copper at 1 GHz (skin depth)
Medium('conductor', 5.8e7, 1e9)

% From loss tangent
Medium('tand', 4, 0.02, 5e9)

% Free space parameters
Medium('free', 2.4e9)
```

### Output Fields

|Field|Description|
|---|---|
|`alpha`|Attenuation constant (Np/m)|
|`beta`|Phase constant (rad/m)|
|`lambda`|Wavelength (m)|
|`up`|Phase velocity (m/s)|
|`eta`|Intrinsic impedance (Ω)|
|`tan_delta`|Loss tangent|
|`classification`|Material type|
|`skin_depth`|Skin depth (m)|

---

## 2. `TLine` — Transmission line calculator

### Purpose

This unified function handles **all transmission line calculations** - impedance transformation, reflection coefficients, VSWR, quarter-wave transformer design, and **TL circuits with series/shunt elements**.

**What it calculates:**

- Input impedance (Z_in)
- Reflection coefficients (Γ_L, Γ_in)
- VSWR and return loss
- Voltage max/min positions
- Quarter-wave transformer design
- **TL + series capacitor/inductor** (exam Q11 type problems)
- **TL + shunt capacitor/inductor**
- **Complex circuits with multiple elements**

### When to use it

Use `TLine` when you see:

- **"A transmission line with Z₀ = 50 Ω is connected to..."**
- **"Find the input impedance..."**
- **"Calculate the reflection coefficient..."**
- **"Design a quarter-wave transformer..."**
- **"What is the VSWR?"**
- **"A series capacitor is connected at the input of the TL..."**
- **"Calculate Z_A of the circuit shown..."**
- **"What should be the electrical length to realize Z = jX?"** (stub design)
- **"Find the stub length to produce an impedance of..."**
- **"Given Γ at plane A, find Γ_L at the load..."** ← NEW (Q13 type)
- **"What is the load impedance Z_L?"** ← NEW (Q14 type)

### Signature & Modes

```matlab
% Full analysis (length in wavelengths)
TLine(Z0, ZL, len_lambda)

% Full analysis (length in meters)
TLine(Z0, ZL, len, freq, vp)
TLine(Z0, ZL, len, freq, vp, alpha)   % lossy

% Impedance transformation
TLine('Zin', Z0, ZL, len_lambda)      % find Z_in
TLine('ZL', Z0, Zin, len_lambda)      % find ZL

% Reflection coefficient
TLine('Gamma', Z0, Z)                 % Γ from impedance
TLine('Z', Z0, Gamma)                 % Z from Γ
TLine('Gamma_in', Gamma_L, len_lambda)% Gamma_L → Gamma_in (load to input)
TLine('Gamma_L', Gamma_in, len_lambda)% Gamma_in → Gamma_L (input to load)

% Find load from input measurement (Q13/Q14 exam type) - NEW
TLine('load', Z0, Gamma_A, len_lambda)% find both Γ_L and Z_L

% Quarter-wave transformer
TLine('QW', Z_source, Z_load)

% Special lengths
TLine('lambda/4', Z0, ZL)
TLine('lambda/2', Z0, ZL)

% Stub design - find length to realize target impedance (NEW)
TLine('stub', Z_target, Z0)           % both short & open solutions
TLine('stub', Z_target, Z0, 'short')  % short stub only
TLine('stub', Z_target, Z0, 'open')   % open stub only

% TL + Series element at input
TLine('series_C', Z0, ZL, len_m, C, freq, vp)   % series capacitor
TLine('series_L', Z0, ZL, len_m, L, freq, vp)   % series inductor

% TL + Shunt element at input
TLine('shunt_C', Z0, ZL, len_m, C, freq, vp)    % shunt capacitor
TLine('shunt_L', Z0, ZL, len_m, L, freq, vp)    % shunt inductor

% Complex circuit with multiple elements
TLine('circuit', Z0, ZL, len_m, freq, vp, ...
      'series_C', C1, 'shunt_L', L1, ...)
```

### Examples

```matlab
% Basic: 50Ω line, 100Ω load, 0.3λ long
TLine(50, 100, 0.3)

% With frequency: 50Ω, 75Ω load, 0.5m, 1GHz, 2e8 m/s
TLine(50, 75, 0.5, 1e9, 2e8)

% Quarter-wave transformer design
TLine('QW', 50, 100)

% Find Gamma from load impedance
TLine('Gamma', 50, 75+1j*25)

% Find input impedance
TLine('Zin', 50, 100+1j*50, 0.25)

% =============================================
% Q12 EXAM TYPE: Stub to realize target impedance
% =============================================
% Realize Z_A = j30 Ω using 75 Ω short-circuited stub
TLine('stub', 1j*30, 75, 'short')
% Answer: ℓ = 0.0606 λ

% =============================================
% Q13/Q14 EXAM TYPE: Find Γ_L and Z_L from Γ_A
% =============================================
% Given: Γ_A = 0.539∠166° at input, Z0 = 75Ω, ℓ = 0.3λ
Gamma_A = 0.539 * exp(1j * deg2rad(166));
r = TLine('load', 75, Gamma_A, 0.3);
% Q13 Answer: Γ_L = 0.539∠22°
% Q14 Answer: Z_L = (183 + j104) Ω

% =============================================
% Q11 EXAM TYPE: TL with series capacitor
% =============================================
% Given: f=5GHz, vp=0.79*c0, Z0=60Ω, ℓ=17mm, ZL=25+j30Ω, C=1pF
c0 = 2.998e8;
TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0)

% TL with shunt inductor
TLine('shunt_L', 50, 75+1j*25, 0.1, 10e-9, 1e9, 2e8)

% Complex circuit: TL + series C + shunt L
TLine('circuit', 50, 100, 0.1, 1e9, 2e8, ...
      'series_C', 1e-12, 'shunt_L', 5e-9)
```

### Output Fields

|Field|Description|
|---|---|
|`Z_in`|Input impedance (Ω)|
|`Z_A`|Input impedance alias (Ω)|
|`Z_TL`|TL input impedance before elements (Ω)|
|`Z_element`|Element impedance (Ω)|
|`Gamma_L`|Load reflection coefficient|
|`Gamma_in`|Input reflection coefficient|
|`VSWR`|Voltage standing wave ratio|
|`z_vmax`|First V_max from load (λ)|
|`z_vmin`|First V_min from load (λ)|
|`P_delivered`|Fraction of power to load|
|`RL_dB`|Return loss (dB)|

### Q11 Exam Example (TL + Series Capacitor)

**Problem:** Calculate Z_A of circuit with:

- f = 5 GHz, vp = 0.79·c₀
- Z₀ = 60 Ω, ℓ = 17 mm
- Z_L = (25 + j30) Ω
- Series capacitor C = 1 pF at input

**Solution:**

```matlab
c0 = 2.998e8;
r = TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0);

% Output:
%   Z_TL = 72.44 + j49.13 Ω  (TL input impedance)
%   Z_C  = -j31.83 Ω         (capacitor impedance)
%   Z_A  = 72.44 + j17.30 Ω  (total = Z_C + Z_TL)
%   |Z_A| = 74.48 Ω ∠ 13.4°
```

---

## 3. `Polarization` — Wave polarization analysis

### Purpose

This unified function analyzes the **polarization state of electromagnetic waves** - determining type (linear/circular/elliptical), handedness, and axial ratio.

**What it calculates:**

- Polarization type
- Handedness (RHCP/LHCP)
- Axial ratio (AR) and AR in dB
- Major/minor semi-axes
- Tilt angle

### When to use it

Use `Polarization` when you see:

- **"Determine the polarization of the wave..."**
- **"Is this RHCP or LHCP?"**
- **"Calculate the axial ratio..."**
- **"The phasor is E = x̂ + jŷ..."**

### Signature & Modes

```matlab
% MODE 1: Complex phasor (most common)
Polarization(F)                % assumes +z propagation
Polarization(F, k_hat)         % specify direction

% MODE 2: Time-domain (u·cos + v·sin form)
Polarization(u, v, beta)

% MODE 3: Amplitude and phase
Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg)
Polarization('ap', Ex, Ey, phi_x_deg, phi_y_deg, k_hat)
```

### Examples

```matlab
% RHCP wave in +z direction
Polarization([1; -1j; 0])

% LHCP wave in +x direction
Polarization([0; 1; 1j], [1;0;0])

% Linear polarization (45°)
Polarization([1; 1; 0])

% From amplitude/phase: Ex=10, Ey=5, φx=0°, φy=90°
Polarization('ap', 10, 5, 0, 90)

% Time-domain: E = x̂·cos(ψ) + ŷ·sin(ψ)
Polarization([1;0;0], [0;1;0], [0;0;1])
```

### Output Fields

|Field|Description|
|---|---|
|`type`|'Linear', 'Circular', or 'Elliptical'|
|`handedness`|'RHCP', 'LHCP', or 'N/A'|
|`AR`|Axial ratio (1=circular, Inf=linear)|
|`AR_dB`|Axial ratio in dB|
|`major`|Major semi-axis amplitude|
|`minor`|Minor semi-axis amplitude|
|`tilt_deg`|Tilt angle (degrees)|

### Quick Reference Table

|Phasor|Type|Handedness|
|---|---|---|
|`[1; 0; 0]`|Linear|N/A|
|`[1; 1; 0]`|Linear (45°)|N/A|
|`[1; -1j; 0]`|Circular|RHCP (+z)|
|`[1; 1j; 0]`|Circular|LHCP (+z)|
|`[1; 0.5j; 0]`|Elliptical|LHCP (+z)|

---

## 4. `Fresnel` — Reflection/transmission at interfaces

### Purpose

This unified function calculates **what happens when waves hit boundaries** - reflection coefficients, transmission, Brewster angle, critical angle, and Snell's law.

**What it calculates:**

- Reflection coefficients (Γ_TE, Γ_TM)
- Transmission coefficients
- Power reflected/transmitted
- Brewster and critical angles
- Transmission angle (Snell's law)

### When to use it

Use `Fresnel` when you see:

- **"A wave hits the interface between air and glass..."**
- **"Find the reflection coefficient at 45° incidence..."**
- **"Calculate the Brewster angle..."**
- **"What is the critical angle for total internal reflection?"**

### Signature & Modes

```matlab
% Normal incidence
Fresnel(eps_r1, eps_r2)
Fresnel(eps_r1, eps_r2, mu_r1, mu_r2)

% Oblique incidence
Fresnel(eps_r1, eps_r2, theta_i)        % TE and TM
Fresnel(eps_r1, eps_r2, theta_i, 'TE')  % TE only
Fresnel(eps_r1, eps_r2, theta_i, 'TM')  % TM only

% Snell's law
Fresnel('snell', n1, n2, theta_i)

% Special angles
Fresnel('brewster', eps_r1, eps_r2)
Fresnel('critical', eps_r1, eps_r2)

% From wave vector
Fresnel('kvec', beta, eps_r2, plane)
```

### Examples

```matlab
% Normal incidence: air to glass
Fresnel(1, 4)

% Oblique at 45 degrees
Fresnel(1, 4, 45)

% TM wave at 30 degrees
Fresnel(1, 2.25, 30, 'TM')

% Brewster angle
Fresnel('brewster', 1, 4)

% Critical angle (glass to air)
Fresnel('critical', 4, 1)

% Snell's law
Fresnel('snell', 1, 1.5, 30)
```

### Output Fields

|Field|Description|
|---|---|
|`Gamma_TE`|TE reflection coefficient|
|`Gamma_TM`|TM reflection coefficient|
|`tau_TE`|TE transmission coefficient|
|`tau_TM`|TM transmission coefficient|
|`R_TE`, `R_TM`|Power reflectance|
|`T_TE`, `T_TM`|Power transmittance|
|`theta_i`|Incident angle (deg)|
|`theta_t`|Transmitted angle (deg)|
|`theta_Brewster`|Brewster angle (deg)|
|`theta_critical`|Critical angle (deg)|

---

## 5. `StubMatch` — Single-stub matching

### Purpose

This function designs **single-stub impedance matching networks** - finding the stub position and length to match any load to a transmission line.

**What it calculates:**

- Distance from load to stub (d)
- Stub length (l)
- Both possible solutions
- Verification of match

### When to use it

Use `StubMatch` when you see:

- **"Design a single-stub matching network..."**
- **"Match a load of ZL = ... to a 50Ω line..."**
- **"Find the stub length and position..."**
- **"What is the correct length d / ℓ?"** (Q16/Q17 type)

### Signature

```matlab
% Basic (normalized, lengths in λ)
StubMatch(ZL, Z0)                      % Short stub (default)
StubMatch(ZL, Z0, 'short')             % Short stub
StubMatch(ZL, Z0, 'open')              % Open stub

% With wavelength (physical lengths in mm)
StubMatch(ZL, Z0, 'short', lambda)     % Give λ in meters
StubMatch(ZL, Z0, 'short', 0.133)      % λ = 13.3 cm

% With frequency and permittivity (auto-calculate λ)
StubMatch(ZL, Z0, 'short', freq, eps_r)
```

### Examples

```matlab
% =============================================
% Q15-Q17 EXAM TYPE: Stub matching with λ
% =============================================
% Given: ZL = 142+j42.5 Ω, Z0 = 75 Ω, λ = 13.3 cm
r = StubMatch(142+1j*42.5, 75, 'short', 0.133);
% Q16 Answer: r.d_mm = 24.5 mm
% Q17 Answer: r.l_mm = 19.4 mm

% Using frequency and permittivity instead
StubMatch(142+1j*42.5, 75, 'short', 1550e6, 2.1)

% Basic usage (normalized only)
StubMatch(100+1j*50, 50, 'short')
```

### Output Fields

|Field|Description|
|---|---|
|`d`|Distance load→stub (λ)|
|`l`|Stub length (λ)|
|`d_mm`|Distance in mm (if λ given)|
|`l_mm`|Stub length in mm (if λ given)|
|`d_alt`|Alternative distance (λ)|
|`l_alt`|Alternative stub length (λ)|
|`lambda`|Wavelength used (m)|

---

## 6. `poynting_pw` — H-field phasor & Poynting vector

### Purpose

Calculate **magnetic field phasor** and **time-average Poynting vector** for plane waves. Solves Q22-Q23 type exam problems.

### When to use it

Use `poynting_pw` when you see:

- **"What is the magnetic phasor amplitude?"**
- **"Find the time-average Poynting vector"**
- **"Given E-field in form a·cos + b·sin..."**

### Signature & Modes

```matlab
% MODE 1: From time-domain (a·cos + b·sin form) — Q22-Q23 type
r = poynting_pw('time', a, b, E0, beta_vec)
r = poynting_pw('time', a, b, E0, beta_vec, eta)  % custom η

% MODE 2: From E-field phasor directly
r = poynting_pw(E_phasor, beta_vec)
r = poynting_pw(E_phasor, beta_vec, eta)

% MODE 3: Simple scalar (original)
r = poynting_pw(E0, eta, A, phi)
```

### Example (Q22-Q23)

```matlab
% Given: E = E0*[2;1;0]*cos(Φ) + E0*[0;-1;-2]*sin(Φ)
%        β = (2, -4, 2) rad/m, E0 = 10 V/m
a = [2; 1; 0];
b = [0; -1; -2];
E0 = 10;
beta_vec = [2; -4; 2];

r = poynting_pw('time', a, b, E0, beta_vec);

% Q22 Answer: r.H_phasor = [-10.8-j54.2; 21.7-j21.7; 54.2+j10.8] mA/m
% Q23 Answer: r.S_avg = [0.542; -1.08; 0.542] W/m²
```

### Output Fields

|Field|Description|
|---|---|
|`E_phasor`|Electric field phasor [V/m]|
|`H_phasor`|Magnetic field phasor [A/m]|
|`k_hat`|Propagation direction unit vector|
|`S_avg`|Time-average Poynting vector [W/m²]|
|`S_mag`|Magnitude of Poynting vector [W/m²]|

### Theory

**Phasor conversion:** $\vec{E} = \vec{a}\cos\Phi + \vec{b}\sin\Phi \Rightarrow \tilde{\vec{E}}_0 = E_0(\vec{a} - j\vec{b})$

**H-field:** $\tilde{\vec{H}}_0 = \frac{1}{\eta}\hat{k} \times \tilde{\vec{E}}_0$

**Poynting:** $\bar{\vec{S}} = \frac{1}{2}\text{Re}{\tilde{\vec{E}} \times \tilde{\vec{H}}^*}$

---

## 7. `coulomb_pair` — Coulomb force

### Purpose

Calculate **vector Coulomb force** between two point charges.

### Signature

```matlab
[F12, F21] = coulomb_pair(q1, q2, r1, r2)
```

**Inputs:**

- `q1`, `q2` — Charges [C]
- `r1`, `r2` — Position vectors [x; y; z] [m]

### Example

```matlab
q1 = 1e-9;  q2 = -2e-9;
r1 = [0; 0; 0];  r2 = [1; 0; 0];
[F12, F21] = coulomb_pair(q1, q2, r1, r2);
```

---

## 8. `B_inf_wire` — B-field of infinite wire

### Purpose

Calculate **magnetic field magnitude** around an infinitely long current-carrying wire.

### Signature

```matlab
B = B_inf_wire(I, r)
B = B_inf_wire(I, r, mu_r)
```

### Example

```matlab
B = B_inf_wire(5, 0.02);   % 5 A, 2 cm from wire
% B = 50 μT
```

---

## 9. `rect2pol` — Complex to polar

### Purpose

Convert complex number to **magnitude and angle** (in degrees).

### Signature

```matlab
[r, a] = rect2pol(x)
```

### Example

```matlab
[mag, angle_deg] = rect2pol(3 + 4j);
% mag = 5, angle_deg = 53.13°
```

---

## 10. `smithchart_plot` — Smith chart visualization

### Purpose

Plot points on a **Smith chart** from either impedance or reflection coefficient. Automatically calculates and displays normalized impedance and Γ.

### When to use it

Use `smithchart_plot` when you need to:

- **Visualize a load impedance on the Smith chart**
- **Verify normalized impedance calculations**
- **Plot reflection coefficient positions**
- **Check which region of the Smith chart a point falls in**

### Signature

```matlab
smithchart_plot(Z0, ZL)                  % Plot load impedance (simplest)
smithchart_plot(Z0, ZL, 'label')         % With custom label
smithchart_plot('Gamma', Gamma)          % Plot Γ directly
smithchart_plot('Gamma', Gamma, 'label') % Γ with label
smithchart_plot()                        % Demo mode
```

### Examples

```matlab
% Q10 Example: ZL = 15 - j37.5 Ω on 75 Ω line
smithchart_plot(75, 15 - 1j*37.5)

% Output:
%   zL (normalized) = 0.2 - j0.5
%   Gamma = -0.5385 - j0.3077
%   |Gamma| = 0.6202, angle = -150.26°

% Plot multiple points
smithchart_plot(50, 100, 'Z_1')
hold on
smithchart_plot(50, 25 - 1j*25, 'Z_2')

% Plot reflection coefficient directly
smithchart_plot('Gamma', 0.5*exp(1j*pi/4), 'My Point')
```

### Output

The function prints:

- Original impedance Z_L
- Normalized impedance z_L = Z_L/Z_0
- Reflection coefficient Γ (rectangular and polar form)

And plots the point on a Smith chart with:

- Red marker at the Γ location
- Label showing normalized impedance

### Smith Chart Regions

|Region|Condition|Meaning|
|---|---|---|
|Right half|Re(z) > 1|High resistance|
|Left half|Re(z) < 1|Low resistance|
|Upper half|Im(z) > 0|Inductive (L)|
|Lower half|Im(z) < 0|Capacitive (C)|
|Center|z = 1|Matched|
|Edge (|Γ|=1)|

---

## Quick Reference Card

```matlab
%% MEDIUM PROPERTIES
Medium(4, 10e9)                        % Lossless dielectric
Medium(80, 4, 1e6, 1, 'Seawater')       % Lossy medium
Medium('conductor', 5.8e7, 1e9)        % Good conductor
Medium('free', 2.4e9)                  % Free space

%% TRANSMISSION LINES
TLine(50, 100, 0.3)                    % Full analysis
TLine('Gamma', 50, 75+1j*25)           % Get Γ from Z
TLine('Zin', 50, 100, 0.25)            % Input impedance
TLine('QW', 50, 100)                   % Quarter-wave design
TLine('load', 75, 0.539*exp(1j*2.9), 0.3)  % Q13/Q14: Γ_A → Γ_L, Z_L
TLine('stub', 1j*30, 75, 'short')      % Q12: stub design

%% TL + ELEMENTS (Q11 exam type)
c0 = 2.998e8;
TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0)  % Series cap
TLine('series_L', 50, 75, 0.1, 10e-9, 1e9, 2e8)              % Series ind
TLine('shunt_C', 50, 75, 0.1, 1e-12, 1e9, 2e8)               % Shunt cap
TLine('shunt_L', 50, 75, 0.1, 10e-9, 1e9, 2e8)               % Shunt ind

%% STUB MATCHING (Q15-Q17 exam type)
StubMatch(142+1j*42.5, 75, 'short', 0.133)  % With λ → d_mm, l_mm
StubMatch(142+1j*42.5, 75, 'short', 1550e6, 2.1)  % With freq, eps_r
StubMatch(100+1j*50, 50, 'short')           % Normalized (λ = 1)

%% POLARIZATION
Polarization([1; -1j; 0])              % RHCP in +z
Polarization([1; 1j; 0], [0;0;1])      % LHCP in +z
Polarization('ap', 10, 5, 0, 90)       % From amplitude/phase

%% FRESNEL/INTERFACES
Fresnel(1, 4)                          % Normal incidence
Fresnel(1, 4, 45)                      % Oblique at 45°
Fresnel('brewster', 1, 4)              % Brewster angle
Fresnel('critical', 4, 1)              % Critical angle

%% PLANE WAVE H-FIELD & POYNTING (Q22-Q23 exam type)
a = [2;1;0]; b = [0;-1;-2]; E0 = 10;
beta_vec = [2; -4; 2];
r = poynting_pw('time', a, b, E0, beta_vec);  % H_phasor, S_avg

%% UTILITIES
B = B_inf_wire(5, 0.02);               % B-field
[F12, F21] = coulomb_pair(q1, q2, r1, r2);
[r, a] = rect2pol(z);
smithchart_plot(75, 15-1j*37.5)        % Smith chart
```

---

## Migration Guide: Old → New Functions

If you have scripts using the old function names, here's how to update them:

|Old Function|New Equivalent|
|---|---|
|`lossy_media(eps_r, sigma, freq)`|`Medium(eps_r, sigma, freq)`|
|`plane_wave_lossless(eps_r, freq)`|`Medium(eps_r, freq)`|
|`rt_normal_incidence(eps1, eps2)`|`Fresnel(eps1, eps2)`|
|`tl_section(Z0, ZL, freq, len, vp)`|`TLine(Z0, ZL, len, freq, vp)`|
|`qw_transformer(R1, RL, freq, vp)`|`TLine('QW', R1, RL)`|
|`polarization_analyzer(F, k)`|`Polarization(F, k)`|
|`WavePolarization(F, k)`|`Polarization(F, k)`|
|`AxialRatio(F)`|`Polarization(F)`|
|`openstub(ZL, Z0, Z0s)`|`StubMatch(ZL, Z0, 'open', Z0s)`|
|`shortstub(ZL, Z0, Z0s)`|`StubMatch(ZL, Z0, 'short', Z0s)`|
|`TransmissionAngle(beta, eps_r, plane)`|`Fresnel('kvec', beta, eps_r, plane)`|
|`TransmittedPower(...)`|`Fresnel(eps1, eps2, theta)` → use `T_TM`|