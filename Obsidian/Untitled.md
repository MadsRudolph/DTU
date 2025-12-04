---

## title: EM MATLAB Helpers type: helper tags: [Electromagnetics, MATLAB, helpers] aliases: [EM helpers, EM MATLAB toolbox] links: [ "Formulas/Plane Waves", "Formulas/Transmission Lines", "Formulas/Electrostatics & Magnetostatics" ] updated: 2025-12-04

# EM MATLAB Helpers

> Central reference for all EM helper scripts.  
> When using any helper in an exercise/exam solution, reference this note.

---

## 🚀 Quick Start - How to Use These Helpers

**IMPORTANT:** Before using any helper function, add this line at the top of your MATLAB script or Live Script:

```matlab
% Add this at the top of your live script (one time)
addpath('C:\Users\Mads2\DTU\3.semester\Electromagnetics\Helpers');
```

This tells MATLAB where to find your helper functions. Without this line, MATLAB will say "Undefined function or variable" when you try to call them.

**After adding the path, you can call any helper like:**

```matlab
pw = plane_wave_lossless(4, 1e9);           % Calculate lossless wave parameters
result = lossy_media(8, 0.01, 5e9);         % Analyze lossy medium
tl = tl_section(50, 75, 1e9, 0.1, 2e8);    % Solve transmission line problem
```

---

## Overview

Current helpers:

1. `lossy_media` — General lossy medium ($\alpha$, $\beta$, $\gamma$, $\eta$, $\tan\delta$, classification)
2. `plane_wave_lossless` — Lossless plane wave parameters ($\lambda$, $\beta$, $u_p$, $\eta$)
3. `rt_normal_incidence` — Reflection / transmission @ normal incidence (Fresnel)
4. `tl_section` — Single TL section: $\Gamma_L$, $\Gamma_{in}$, $Z_{in}$, VSWR, $V_{\max}/V_{\min}$ positions
5. `qw_transformer` — Quarter-wave transformer design ($R_{qw}$, check)
6. `poynting_pw` — Poynting vector and power through an area
7. `coulomb_pair` — Force between two point charges in 3D
8. `B_inf_wire` — B-field around an infinitely long straight current

Each subsection below explains:

- **When to use**
- **Inputs / outputs**
- **Quick usage examples**
- **MATLAB implementation**

---

## 1. `lossy_media` — General lossy medium analyzer

### Purpose

This function calculates everything you need when a **wave travels through a material that has some conductivity** (like seawater, wet soil, or imperfect dielectrics).

**What it calculates:**

- How fast the wave dies out ($\alpha$ - attenuation)
- How the wave phase changes ($\beta$ - phase constant)
- Wave impedance ($\eta$)
- Wavelength and velocity
- Whether the material is a good insulator, quasi-conductor, or good conductor

### When to use it

Use `lossy_media` when you see:

- **"A wave propagates through seawater with σ = ..."**
- **"Find the loss tangent of..."**
- **"Calculate skin depth in..."**
- **"The material has conductivity σ = ... and permittivity ε_r = ..."**
- Any problem mentioning **attenuation constant α** or **lossy propagation**

**Example problems:**

- "A 5 GHz wave travels through a material with ε_r = 8 and σ = 0.01 S/m. Find the attenuation."
- "Classify the material as conductor or insulator based on its loss tangent."
- "Calculate how far the wave travels before its amplitude drops to 1/e."

### Signature

- `result = lossy_media(epsilon_r, sigma, freq)`
- `result = lossy_media(epsilon_r, sigma, freq, mu_r)`
- `result = lossy_media(epsilon_r, sigma, freq, mu_r, name)`

**Inputs**

- `epsilon_r` — Relative permittivity (dimensionless)
- `sigma` — Conductivity in S/m
- `freq` — Frequency in Hz
- `mu_r` — Relative permeability (default `1`)
- `name` — String for printing (default `'Material'`)

**Outputs**

Struct `result` with fields:

- `tan_delta`, `classification`
- `alpha`, `beta`, `gamma`
- `wavelength`, `phase_velocity`
- `impedance` (complex $\eta$)
- plus the basic parameters

### Example usage

- Q26-style:
    
    ```matlab
    result = lossy_media(8, 0.01, 5e9);
    ```
    
- Named material:
    
    ```matlab
    glass = lossy_media(5, 10e-12, 10e9, 1, 'Glass');
    ```
    

### MATLAB — `lossy_media.m`

> [!code]- MATLAB — lossy_media.m
> 
> ```matlab
> function result = lossy_media(epsilon_r, sigma, freq, mu_r, name)
>    % =========================================================================
>    % LOSSY MEDIA ANALYZER - Main Function
>    % =========================================================================
>    % Usage:
>    %   result = lossy_media(epsilon_r, sigma, freq)
>    %   result = lossy_media(epsilon_r, sigma, freq, mu_r)
>    %   result = lossy_media(epsilon_r, sigma, freq, mu_r, 'Name')
>    %
>    % Inputs:
>    %   epsilon_r : Relative permittivity (dimensionless)
>    %   sigma     : Conductivity (S/m)
>    %   freq      : Frequency (Hz)
>    %   mu_r      : Relative permeability (default = 1)
>    %   name      : Material name for display (default = 'Material')
>    %
>    % Output:
>    %   result    : Struct with all computed parameters
>    % =========================================================================
> 
>    % Handle optional arguments
>    if nargin < 4
>        mu_r = 1;
>    end
>    if nargin < 5
>        name = 'Material';
>    end
> 
>    % Constants
>    eps0 = 8.854e-12;         % Permittivity of free space (F/m)
>    mu0  = 4*pi*1e-7;         % Permeability of free space (H/m)
> 
>    % Derived parameters
>    omega = 2*pi*freq;
>    eps   = eps0 * epsilon_r;
>    mu    = mu0  * mu_r;
> 
>    % --- Physics Calculations ---
>    j = 1j;
> 
>    % Complex propagation constant
>    gamma = sqrt(j*omega*mu*(sigma + j*omega*eps));
>    alpha = real(gamma);              % Attenuation constant (Np/m)
>    beta  = imag(gamma);              % Phase constant (rad/m)
> 
>    % Wave parameters
>    lambda = 2*pi/beta;               % Wavelength (m)
>    up     = omega/beta;              % Phase velocity (m/s)
>    eta    = sqrt(j*omega*mu/(sigma + j*omega*eps));  % Intrinsic impedance (Ohm)
> 
>    % Loss tangent
>    tan_delta = sigma/(omega*eps);
> 
>    % Classification
>    if tan_delta < 0.1
>        classification = 'Low-Loss Dielectric (Good Insulator)';
>    elseif tan_delta > 10
>        classification = 'Good Conductor';
>    else
>        classification = 'Quasi-Conductor';
>    end
> 
>    % --- Package Results ---
>    result.name          = name;
>    result.frequency     = freq;
>    result.epsilon_r     = epsilon_r;
>    result.mu_r          = mu_r;
>    result.sigma         = sigma;
>    result.tan_delta     = tan_delta;
>    result.classification= classification;
>    result.alpha         = alpha;
>    result.beta          = beta;
>    result.wavelength    = lambda;
>    result.phase_velocity= up;
>    result.impedance     = eta;
>    result.gamma         = gamma;
> 
>    % --- Display Results ---
>    fprintf('\n========================================\n');
>    fprintf('  %s @ %.2e Hz\n', name, freq);
>    fprintf('========================================\n');
>    fprintf('Properties:\n');
>    fprintf('  ε_r = %.2f\n', epsilon_r);
>    fprintf('  μ_r = %.2f\n', mu_r);
>    fprintf('  σ   = %.2e S/m\n', sigma);
>    fprintf('\nClassification:\n');
>    fprintf('  tan(δ) = %.3e\n', tan_delta);
>    fprintf('  Type   = %s\n', classification);
>    fprintf('\nWave Parameters:\n');
>    fprintf('  α (attenuation) = %.3e Np/m\n', alpha);
>    fprintf('  β (phase const) = %.3e rad/m\n', beta);
>    fprintf('  λ (wavelength)  = %.3e m\n', lambda);
>    fprintf('  u_p (velocity)  = %.3e m/s\n', up);
>    fprintf('  η (impedance)   = %.3f + j%.3f Ω\n', real(eta), imag(eta));
>    fprintf('========================================\n\n');
> end
> ```

---

## 2. `plane_wave_lossless` — Lossless plane wave parameters

### Purpose

This function calculates basic wave properties when a **wave travels through a perfect material with no losses** (like air, vacuum, or ideal glass).

**What it calculates:**

- Wavelength ($\lambda$)
- Phase constant ($\beta$)
- Wave velocity ($u_p$)
- Impedance ($\eta$)
- Refractive index ($n$)

### When to use it

Use `plane_wave_lossless` when you see:

- **"A wave propagates in air at frequency f = ..."**
- **"Find the wavelength in a dielectric with ε_r = ..."**
- **"Calculate the phase velocity in glass..."**
- **NO mention of conductivity (σ) or losses**
- Problems about **lossless dielectrics**

**Example problems:**

- "A 1 GHz wave travels in air. What is its wavelength?"
- "Find the phase velocity in a material with ε_r = 4."
- "Calculate the intrinsic impedance of free space."
- "What is the refractive index of a material with ε_r = 9?"

**Key difference from `lossy_media`:** Use this when σ = 0 (no conductivity). If σ ≠ 0, use `lossy_media` instead.

### Signature

- `pw = plane_wave_lossless(epsilon_r, freq)`
- `pw = plane_wave_lossless(epsilon_r, freq, mu_r)`

**Inputs**

- `epsilon_r` — Relative permittivity
- `freq` — Frequency [Hz]
- `mu_r` — Relative permeability (default 1)

**Outputs**

Struct `pw` with:

- `beta`, `wavelength`, `phase_velocity`, `eta`, `k0`, `n`

### Example

```matlab
pw = plane_wave_lossless(4, 1e9);   % ε_r = 4, 1 GHz
```

### MATLAB — `plane_wave_lossless.m`

> [!code]- MATLAB — plane_wave_lossless.m
> 
> ```matlab
> function pw = plane_wave_lossless(epsilon_r, freq, mu_r)
>    % PLANE_WAVE_LOSSLESS  Basic parameters for a lossless plane wave
>    %
>    %   pw = plane_wave_lossless(epsilon_r, freq)
>    %   pw = plane_wave_lossless(epsilon_r, freq, mu_r)
>    %
>    % Returns a struct with beta, wavelength, phase velocity and eta.
> 
>    if nargin < 3
>        mu_r = 1;
>    end
> 
>    eps0 = 8.854e-12;
>    mu0  = 4*pi*1e-7;
>    c0   = 1/sqrt(eps0*mu0);
> 
>    eps = eps0 * epsilon_r;
>    mu  = mu0 * mu_r;
> 
>    omega = 2*pi*freq;
>    beta  = omega * sqrt(mu*eps);      % rad/m
>    lambda= 2*pi / beta;               % m
>    up    = omega / beta;              % m/s
>    eta   = sqrt(mu/eps);              % ohms
>    n     = c0 / up;                   % refractive index
>    k0    = omega/c0;                  % free-space wavenumber
> 
>    pw.epsilon_r      = epsilon_r;
>    pw.mu_r           = mu_r;
>    pw.freq           = freq;
>    pw.beta           = beta;
>    pw.wavelength     = lambda;
>    pw.phase_velocity = up;
>    pw.eta            = eta;
>    pw.n              = n;
>    pw.k0             = k0;
> 
>    % --- Display Results ---
>    fprintf('\n========================================\n');
>    fprintf('  Lossless Plane Wave @ %.2e Hz\n', freq);
>    fprintf('========================================\n');
>    fprintf('Properties:\n');
>    fprintf('  ε_r = %.2f\n', epsilon_r);
>    fprintf('  μ_r = %.2f\n', mu_r);
>    fprintf('\nWave Parameters:\n');
>    fprintf('  β (phase const)  = %.3e rad/m\n', beta);
>    fprintf('  λ (wavelength)   = %.3e m\n', lambda);
>    fprintf('  u_p (velocity)   = %.3e m/s\n', up);
>    fprintf('  η (impedance)    = %.2f Ω\n', eta);
>    fprintf('  n (refr. index)  = %.4f\n', n);
>    fprintf('  k_0 (free space) = %.3e rad/m\n', k0);
>    fprintf('========================================\n\n');
> end
> ```

---

## 3. `rt_normal_incidence` — Reflection / transmission (normal incidence)

### Purpose

This function calculates **what happens when a wave hits the boundary between two materials** (like air hitting glass, or going from one dielectric to another).

**What it calculates:**

- Reflection coefficient ($\Gamma$) - how much bounces back
- Transmission coefficient ($t$) - how much goes through
- Power reflected ($R$) - percentage of power bounced back
- Power transmitted ($T$) - percentage of power that continues

### When to use it

Use `rt_normal_incidence` when you see:

- **"A wave traveling in air hits a glass surface..."**
- **"Find the reflection coefficient at the interface..."**
- **"What fraction of power is reflected when..."**
- **"Calculate transmission at the boundary between..."**
- Any problem about **waves crossing from one material to another at 90° angle**

**Example problems:**

- "A wave in air (ε_r = 1) hits glass (ε_r = 4). Find the reflection coefficient."
- "What percentage of power is transmitted through the air-dielectric interface?"
- "Calculate Γ at the boundary between two materials."
- "How much power is reflected back when a wave enters water?"

**Important:** This only works for **normal incidence** (wave hits straight on, not at an angle). Both materials must be lossless.

### Signature

- `rt = rt_normal_incidence(eps_r1, eps_r2)`
- `rt = rt_normal_incidence(eps_r1, eps_r2, mu_r1, mu_r2)`

Assumes lossless, non-dispersive media.

**Inputs**

- `eps_r1`, `eps_r2` — Relative permittivities
- `mu_r1`, `mu_r2` — Relative permeabilities (default 1)

**Outputs**

Struct `rt` with:

- `eta1`, `eta2`
- `Gamma`, `t`
- `R`, `T` (power fractions, should satisfy $R+T = 1$ for lossless)

### Example

```matlab
air_to_glass = rt_normal_incidence(1, 4);   % μ_r = 1 in both
```

### MATLAB — `rt_normal_incidence.m`

> [!code]- MATLAB — rt_normal_incidence.m
> 
> ```matlab
> function rt = rt_normal_incidence(eps_r1, eps_r2, mu_r1, mu_r2)
>    % RT_NORMAL_INCIDENCE  Fresnel coefficients for normal incidence
>    %
>    %   rt = rt_normal_incidence(eps_r1, eps_r2)
>    %   rt = rt_normal_incidence(eps_r1, eps_r2, mu_r1, mu_r2)
>    %
>    % Lossless, simple media. Returns Gamma, t, R, T and intrinsic impedances.
> 
>    if nargin < 3
>        mu_r1 = 1;
>    end
>    if nargin < 4
>        mu_r2 = 1;
>    end
> 
>    eps0 = 8.854e-12;
>    mu0  = 4*pi*1e-7;
> 
>    eps1 = eps0 * eps_r1;
>    eps2 = eps0 * eps_r2;
>    mu1  = mu0  * mu_r1;
>    mu2  = mu0  * mu_r2;
> 
>    eta1 = sqrt(mu1/eps1);
>    eta2 = sqrt(mu2/eps2);
> 
>    Gamma = (eta2 - eta1) / (eta2 + eta1);
>    t     = 2*eta2 / (eta2 + eta1);
> 
>    % Power reflection / transmission (normal incidence, lossless)
>    R = abs(Gamma)^2;
>    T = 1 - R;
> 
>    rt.eps_r1 = eps_r1;
>    rt.eps_r2 = eps_r2;
>    rt.mu_r1  = mu_r1;
>    rt.mu_r2  = mu_r2;
>    rt.eta1   = eta1;
>    rt.eta2   = eta2;
>    rt.Gamma  = Gamma;
>    rt.t      = t;
>    rt.R      = R;
>    rt.T      = T;
> end
> ```

---

## 4. `tl_section` — Single transmission line section

### Purpose

This function solves **all the standard transmission line calculations** - when you have a cable/line connected to a load and need to find impedances, reflections, and voltage patterns.

**What it calculates:**

- Reflection at the load ($\Gamma_L$)
- Reflection at the input ($\Gamma_{in}$)
- Input impedance ($Z_{in}$) - what the generator "sees"
- VSWR (Voltage Standing Wave Ratio)
- Where voltage max/min occur on the line

### When to use it

Use `tl_section` when you see:

- **"A transmission line with Z₀ = 50 Ω is connected to a load..."**
- **"Find the input impedance of a line with length..."**
- **"Calculate VSWR for a mismatched line..."**
- **"Where is the first voltage maximum located?"**
- **"A coaxial cable is terminated with ZL = ..."**

**Example problems:**

- "A 50 Ω line, 10 cm long, is connected to a load ZL = 25 - j25 Ω at 1 GHz. Find Zin."
- "Calculate the VSWR on a line with a 75 Ω load and 50 Ω characteristic impedance."
- "Find the reflection coefficient at the input of a λ/4 line."
- "Where does the first voltage maximum occur from the load?"

**Typical setup:** You have a transmission line (coax, microstrip, etc.) with known Z₀, length ℓ, and velocity factor vp, connected to some load ZL.

### Signature

- `tl = tl_section(Z0, ZL, freq, len, vp)`
- `tl = tl_section(Z0, ZL, freq, len, vp, alpha)`

Assumes a uniform line with characteristic impedance $Z_0$.

**Inputs**

- `Z0` — Characteristic impedance [$\Omega$]
- `ZL` — Load impedance (complex allowed) [$\Omega$]
- `freq` — Frequency [Hz]
- `len` — Physical length $\ell$ [m]
- `vp` — Phase velocity on line [m/s] (e.g. `0.66*c0`)
- `alpha` — Attenuation constant [Np/m] (default `0` → lossless)

**Outputs**

Struct `tl` with:

- `beta`, `lambda`, `gamma`
- `Gamma_L`, `Gamma_in`
- `Z_in`
- `VSWR`
- For lossless: `z_vmax`, `z_vmin` (first maximum/minimum from load)

### Example

```matlab
c0 = 3e8;
vp = 0.66*c0;
tl = tl_section(50, 25-1j*25, 1e9, 0.1, vp);
```

### MATLAB — `tl_section.m`

> [!code]- MATLAB — tl_section.m
> 
> ```matlab
> function tl = tl_section(Z0, ZL, freq, len, vp, alpha)
>    % TL_SECTION  Single uniform TL section helper
>    %
>    %   tl = tl_section(Z0, ZL, freq, len, vp)
>    %   tl = tl_section(Z0, ZL, freq, len, vp, alpha)
>    %
>    % Computes Gamma_L, Gamma_in, Z_in, VSWR and Vmax/Vmin positions
>    % (for the lossless case).
> 
>    if nargin < 6
>        alpha = 0;   % lossless default
>    end
> 
>    omega = 2*pi*freq;
>    beta  = omega/vp;
>    gamma = alpha + 1j*beta;
>    lambda= 2*pi/beta;
> 
>    % Reflection coefficient at load
>    Gamma_L = (ZL - Z0) / (ZL + Z0);
> 
>    % Input reflection coefficient at z = -len
>    Gamma_in = Gamma_L * exp(-2*gamma*len);
> 
>    % Input impedance (general lossy formula)
>    Z_in = Z0 * (ZL + Z0 * tanh(gamma*len)) ./ ...
>               (Z0 + ZL * tanh(gamma*len));
> 
>    % VSWR (if |Γ_L| < 1)
>    magGL = abs(Gamma_L);
>    if magGL < 1
>        VSWR = (1 + magGL)/(1 - magGL);
>    else
>        VSWR = Inf;
>    end
> 
>    % Vmax/Vmin positions (only meaningful if alpha ~ 0)
>    if alpha == 0 && magGL ~= 0
>        % Distance from load to first Vmax / Vmin
>        phiL   = angle(Gamma_L);
>        z_vmax = ( -phiL )/(2*beta);
>        z_vmin = ( pi - phiL )/(2*beta);
> 
>        % Normalize to 0..lambda
>        z_vmax = mod(z_vmax, lambda);
>        z_vmin = mod(z_vmin, lambda);
>    else
>        z_vmax = NaN;
>        z_vmin = NaN;
>    end
> 
>    tl.Z0      = Z0;
>    tl.ZL      = ZL;
>    tl.freq    = freq;
>    tl.len     = len;
>    tl.vp      = vp;
>    tl.alpha   = alpha;
>    tl.beta    = beta;
>    tl.lambda  = lambda;
>    tl.gamma   = gamma;
> 
>    tl.Gamma_L = Gamma_L;
>    tl.Gamma_in= Gamma_in;
>    tl.Z_in    = Z_in;
>    tl.VSWR    = VSWR;
>    tl.z_vmax  = z_vmax;
>    tl.z_vmin  = z_vmin;
> end
> ```

---

## 5. `qw_transformer` — Quarter-wave transformer design

### Purpose

This function designs a **matching section** to connect a load to a transmission line with no reflections. It uses a special λ/4 (quarter-wavelength) section to make the impedances match perfectly.

**What it calculates:**

- Required impedance of the matching section ($R_{qw}$)
- Length of the matching section (λ/4)
- Verification that the match works correctly

### When to use it

Use `qw_transformer` when you see:

- **"Design a quarter-wave transformer to match..."**
- **"Match a 100 Ω load to a 50 Ω line..."**
- **"Find the characteristic impedance of a λ/4 matching section..."**
- **"Eliminate reflections using a quarter-wave transformer..."**

**Example problems:**

- "Design a λ/4 transformer to match a 100 Ω antenna to a 50 Ω line at 1 GHz."
- "What Z₀ is needed for a quarter-wave matching section between 75 Ω and 300 Ω?"
- "Find the physical length of a λ/4 transformer at 2.4 GHz."

**Key concept:** The magic formula is $R_{qw} = \sqrt{R_1 \times R_L}$. This only works with **purely resistive (real) loads** - no reactance allowed!

### Signature

- `qw = qw_transformer(R1, RL, freq, vp)`

Assumes lossless TL and purely real load.

**Inputs**

- `R1` — Real characteristic impedance of main line
- `RL` — Real load
- `freq` — Frequency [Hz]
- `vp` — Phase velocity [m/s]

**Outputs**

Struct `qw` with:

- `R_qw` — Required characteristic impedance of $\lambda/4$ section
- `lambda` — Wavelength
- `len_qw` — $\lambda/4$ length
- `Z_in_check` — Input impedance looking into $\lambda/4$ + load (should be $\approx R_1$)

### Example

```matlab
c0 = 3e8;
vp = 0.7*c0;
qw = qw_transformer(50, 100, 1e9, vp);
```

### MATLAB — `qw_transformer.m`

> [!code]- MATLAB — qw_transformer.m
> 
> ```matlab
> function qw = qw_transformer(R1, RL, freq, vp)
>    % QW_TRANSFORMER  Quarter-wave transformer helper (real load)
>    %
>    %   qw = qw_transformer(R1, RL, freq, vp)
>    %
>    % Computes the required R_qw and λ/4 length, and checks the match.
> 
>    if ~isreal(R1) || ~isreal(RL)
>        error('R1 and RL must be real (resistive).');
>    end
> 
>    omega = 2*pi*freq;
>    beta  = omega/vp;
>    lambda= 2*pi/beta;
> 
>    R_qw  = sqrt(R1*RL);
>    len_qw= lambda/4;
> 
>    % Check using standard λ/4 input impedance formula
>    Z_in_check = R_qw^2 / RL;
> 
>    qw.R1         = R1;
>    qw.RL         = RL;
>    qw.freq       = freq;
>    qw.vp         = vp;
>    qw.lambda     = lambda;
>    qw.len_qw     = len_qw;
>    qw.R_qw       = R_qw;
>    qw.Z_in_check = Z_in_check;
> end
> ```

---

## 6. `poynting_pw` — Poynting vector and power (plane wave)

### Purpose

This function calculates **how much electromagnetic power flows through a surface** when hit by a plane wave. Think of it as calculating "watts per square meter" and total power.

**What it calculates:**

- Power density (W/m²) - how concentrated the power is
- Total power (W) - passing through a given area
- Works for waves hitting surfaces at angles

### When to use it

Use `poynting_pw` when you see:

- **"Calculate the power density of a plane wave with E₀ = ..."**
- **"How much power passes through an area of..."**
- **"Find the Poynting vector magnitude..."**
- **"A wave with electric field |E| = ... hits a surface..."**
- **"What is the power flux through..."**

**Example problems:**

- "A plane wave in air has |E| = 10 V/m. Find the power density."
- "Calculate the power passing through a 10 cm² surface."
- "A wave hits a solar panel at 30°. How much power is collected?"
- "What is the time-average Poynting vector for this wave?"

**Key formula:** Power density = $|E_0|^2 / (2|\eta|)$. If the wave hits at an angle, multiply by cos(angle).

### Signature

- `pw = poynting_pw(E0, eta, A, phi)`

**Inputs**

- `E0` — Field magnitude ($|E_0|$) [V/m]
- `eta` — Intrinsic impedance (complex allowed) [$\Omega$]
- `A` — Area [m²]
- `phi` — Angle between **Poynting vector** and surface normal