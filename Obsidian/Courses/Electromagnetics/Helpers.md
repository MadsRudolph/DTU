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
---

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
|`poynting_pw`|Poynting vector and power calculations|
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

This unified function handles **all transmission line calculations** - impedance transformation, reflection coefficients, VSWR, and quarter-wave transformer design.

**What it calculates:**

- Input impedance (Z_in)
- Reflection coefficients (Γ_L, Γ_in)
- VSWR and return loss
- Voltage max/min positions
- Quarter-wave transformer design

### When to use it

Use `TLine` when you see:

- **"A transmission line with Z₀ = 50 Ω is connected to..."**
- **"Find the input impedance..."**
- **"Calculate the reflection coefficient..."**
- **"Design a quarter-wave transformer..."**
- **"What is the VSWR?"**

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
TLine('Gamma_in', Gamma_L, len_lambda)% propagate Γ

% Quarter-wave transformer
TLine('QW', Z_source, Z_load)

% Special lengths
TLine('lambda/4', Z0, ZL)
TLine('lambda/2', Z0, ZL)
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
```

### Output Fields

|Field|Description|
|---|---|
|`Z_in`|Input impedance (Ω)|
|`Gamma_L`|Load reflection coefficient|
|`Gamma_in`|Input reflection coefficient|
|`VSWR`|Voltage standing wave ratio|
|`z_vmax`|First V_max from load (λ)|
|`z_vmin`|First V_min from load (λ)|
|`P_delivered`|Fraction of power to load|
|`RL_dB`|Return loss (dB)|

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

### Signature

```matlab
StubMatch(ZL, Z0)                    % Short stub (default)
StubMatch(ZL, Z0, 'open')            % Open stub
StubMatch(ZL, Z0, 'short')           % Short stub
StubMatch(ZL, Z0, type, Z0_stub)     % Different stub impedance
```

### Examples

```matlab
% Match 100+j50 Ω to 50 Ω with short stub
StubMatch(100+1j*50, 50, 'short')

% Match with open stub
StubMatch(100+1j*50, 50, 'open')

% Different stub impedance
StubMatch(75+1j*25, 50, 'short', 75)
```

### Output Fields

|Field|Description|
|---|---|
|`d`|Distance load→stub (λ)|
|`l`|Stub length (λ)|
|`d_alt`|Alternative distance|
|`l_alt`|Alternative stub length|
|`type`|'open' or 'short'|

---

## 6. `poynting_pw` — Poynting vector and power

### Purpose

Calculate **time-average Poynting vector and power** through a surface for plane waves.

### Signature

```matlab
pw = poynting_pw(E0, eta, A, phi)
```

**Inputs:**

- `E0` — Field magnitude [V/m]
- `eta` — Intrinsic impedance [Ω]
- `A` — Area [m²]
- `phi` — Angle to surface normal [rad]

### Example

```matlab
eta0 = 120*pi;
pw = poynting_pw(10, eta0, 0.01, 0);   % 10 V/m, normal incidence, 1 cm²
% pw.S_mag = 0.133 W/m²
% pw.P_incident = 1.33 mW
```

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

Plot points on a **Smith chart** from either Γ or impedance.

### Signature

```matlab
smithchart_plot('Gamma', Gamma, [], [])
smithchart_plot('Load', [], Z0, ZL)
```

### Example

```matlab
smithchart_plot('Load', [], 50, 100+1j*50)
```

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

%% STUB MATCHING
StubMatch(100+1j*50, 50, 'short')      % Short stub
StubMatch(75, 50, 'open')              % Open stub

%% POLARIZATION
Polarization([1; -1j; 0])              % RHCP in +z
Polarization([1; 1j; 0], [0;0;1])      % LHCP in +z
Polarization('ap', 10, 5, 0, 90)       % From amplitude/phase

%% FRESNEL/INTERFACES
Fresnel(1, 4)                          % Normal incidence
Fresnel(1, 4, 45)                      % Oblique at 45°
Fresnel('brewster', 1, 4)              % Brewster angle
Fresnel('critical', 4, 1)              % Critical angle

%% UTILITIES
B = B_inf_wire(5, 0.02);               % B-field
[F12, F21] = coulomb_pair(q1, q2, r1, r2);
pw = poynting_pw(E0, eta, A, phi);
[r, a] = rect2pol(z);
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
