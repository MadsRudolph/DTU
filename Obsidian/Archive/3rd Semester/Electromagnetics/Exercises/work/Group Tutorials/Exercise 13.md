> Quick refs: [[Courses/Electromagnetics/Formulas/Plane Waves in Lossy Media]], [[Courses/Electromagnetics/Formulas/EM Material Parameters]]  
> Source: [[exercises+results.pdf]]   

---

# Exercise 13 — Plane Wave: Propagation in Lossy Media

---

## 13.1 — Classifying Media & Computing Wave Parameters

> **Given**  
> For each material, assume time-harmonic fields with angular frequency $\omega = 2\pi f$ and constitutive parameters:
>
> (a) **Glass**  
> - $\mu_r = 1$  
> - $\varepsilon_r = 5$  
> - $\sigma = 10~\text{pS/m} = 1.0\times 10^{-11}~\text{S/m}$  
> - $f = 10~\text{GHz}$  
>
> (b) **Tissue**  
> - $\mu_r = 1$  
> - $\varepsilon_r = 12$  
> - $\sigma = 0.3~\text{S/m}$  
> - $f = 100~\text{MHz}$  
>
> (c) **Wood**  
> - $\mu_r = 1$  
> - $\varepsilon_r = 3$  
> - $\sigma = 0.1~\text{mS/m} = 1.0\times 10^{-4}~\text{S/m}$  
> - $f = 1~\text{kHz}$  
>
> **Tasks**
> - Classify each material as:
>   - low-loss dielectric  
>   - quasi-conductor  
>   - good conductor  
> - Compute:
>   - complex propagation constant $\gamma = \alpha + j\beta$  
>   - attenuation constant $\alpha$  
>   - phase constant $\beta$  
>   - wavelength $\lambda$  
>   - phase velocity $u_p$  
>   - intrinsic impedance $\eta$  

---

### Theory recap

For a uniform plane wave in a **linear, isotropic, homogeneous lossy medium** (Ulaby & Ravaioli, plane-wave propagation in lossy media):

- Constitutive parameters:
  $$
  \varepsilon = \varepsilon_0\varepsilon_r,\quad
  \mu = \mu_0\mu_r,\quad
  \sigma\ \text{(conductivity)}.
  $$
- Complex permittivity:
  $$
  \tilde{\varepsilon} = \varepsilon - j\frac{\sigma}{\omega}.
  $$
- Propagation constant:
  $$
  \gamma = \alpha + j\beta
  = \sqrt{j\omega\mu\,(\sigma + j\omega\varepsilon)}.
  $$
  A convenient explicit form:
  $$
  \alpha = \omega\sqrt{\frac{\mu\varepsilon}{2}}
  \left[
  \sqrt{1 + \left(\frac{\sigma}{\omega\varepsilon}\right)^2} - 1
  \right]^{1/2},
  $$
  $$
  \beta = \omega\sqrt{\frac{\mu\varepsilon}{2}}
  \left[
  \sqrt{1 + \left(\frac{\sigma}{\omega\varepsilon}\right)^2} + 1
  \right]^{1/2}.
  $$
- Intrinsic impedance:
  $$
  \eta = \sqrt{\frac{j\omega\mu}{\sigma + j\omega\varepsilon}}.
  $$
- Wavelength and phase velocity:
  $$
  \lambda = \frac{2\pi}{\beta},
  \qquad
  u_p = \frac{\omega}{\beta}.
  $$

**Classification** (using the loss tangent):
$$
\tan\delta = \frac{\sigma}{\omega\varepsilon}.
$$

- **Low-loss dielectric**: $\tan\delta \ll 1$  
- **Good conductor**: $\tan\delta \gg 1$  
- **Quasi-conductor**: neither limit; $\tan\delta \sim 1$ to $10$ (intermediate regime)

---

### Geometry / setup

- All cases assume **homogeneous bulk materials**, no boundaries are explicitly considered.
- The wave is assumed to propagate as a **uniform plane wave**; propagation direction does not affect scalar quantities $\alpha, \beta, \lambda, u_p, \eta$ in a homogeneous medium.
- We use:
  - $\varepsilon_0 \approx 8.854\times 10^{-12}~\text{F/m}$  
  - $\mu_0 \approx 4\pi\times 10^{-7}~\text{H/m}$  

---

### Derivation & classification

We outline the logic and then give the final values (numerically matching the official table

#### (a) Glass at 10 GHz

1. Compute
   $$
   \omega = 2\pi f = 2\pi\cdot 10^{10}~\text{rad/s},
   \quad
   \varepsilon = 5\varepsilon_0,
   \quad
   \mu = \mu_0.
   $$
2. Loss tangent:
   $$
   \tan\delta = \frac{\sigma}{\omega\varepsilon}
   \approx \frac{10^{-11}}{2\pi\cdot 10^{10}\cdot 5\varepsilon_0} \ll 1.
   $$
   Very small → **low-loss dielectric**.
3. Plugging into the general expressions yields:
   - $\gamma = 8.42\times 10^{-10} + j\,469\ \text{m}^{-1}$  
   - $\alpha = 8.42\times 10^{-10}~\text{m}^{-1}$  
   - $\beta = 469~\text{m}^{-1}$  
   - $\lambda = 2\pi/\beta \approx 1.34\times 10^{-2}~\text{m}$  
   - $u_p = \omega/\beta \approx 1.34\times 10^{8}~\text{m/s}$  
   - $\eta \approx 168 + j\,3.03\times 10^{-10}~\Omega$

Matches the official table.

---

#### (b) Tissue at 100 MHz

1. Parameters:
   $$
   \omega = 2\pi\cdot 10^{8},
   \quad
   \varepsilon = 12\varepsilon_0,
   \quad
   \mu = \mu_0,
   \quad
   \sigma = 0.3~\text{S/m}.
   $$
2. Loss tangent:
   $$
   \tan\delta = \frac{\sigma}{\omega\varepsilon}
   \approx O(1).
   $$
   → **quasi-conductor** (intermediate).
3. From formulas:
   - $\gamma = 9.75 + j\,12.2\ \text{m}^{-1}$  
   - $\alpha = 9.75~\text{m}^{-1}$  
   - $\beta = 12.2~\text{m}^{-1}$  
   - $\lambda \approx 0.512~\text{m}$  
   - $u_p \approx 5.20\times 10^{7}~\text{m/s}$  
   - $\eta \approx 39.5 + j\,31.7~\Omega$

Matches the official table.

---

#### (c) Wood at 1 kHz

1. Parameters:
   $$
   \omega = 2\pi\cdot 10^{3},
   \quad
   \varepsilon = 3\varepsilon_0,
   \quad
   \mu = \mu_0,
   \quad
   \sigma = 10^{-4}~\text{S/m}.
   $$
2. Loss tangent:
   $$
   \tan\delta = \frac{\sigma}{\omega\varepsilon}
   = \frac{10^{-4}}{2\pi\cdot 10^{3}\cdot 3\varepsilon_0}.
   $$
   Numerically this is $\gg 1$ for this parameter set as interpreted in the solution sheet, so the medium is treated as a **good conductor** in that context (following the classification and numbers in the official solution).
3. Using the good-conductor-dominant general formulas:
   - $\gamma = (6.23 + j\,6.29)\times 10^{-4}\ \text{m}^{-1}$  
   - $\alpha = 6.23\times 10^{-4}~\text{m}^{-1}$  
   - $\beta = 6.29\times 10^{-4}~\text{m}^{-1}$  
   - $\lambda \approx 9.99\times 10^{3}~\text{m}$  
   - $u_p \approx 9.99\times 10^{6}~\text{m/s}$  
   - $\eta \approx 6.29 + j\,6.28~\Omega$

Again, matches the official values.

---

Here is the updated Obsidian Markdown content. I have replaced the older script with the **improved, modular version** we created, while keeping your LaTeX table and notes intact.

You can copy and paste this entire block directly into Obsidian.

---

### Final boxed results — Exercise 13.1

We summarize in the same style as the solution sheet:

$$\boxed{ \begin{array}{c|c|c|c|c|c|c} \text{Material} & \text{type} & \gamma~[\text{m}^{-1}] & \alpha~[\text{m}^{-1}] & \beta~[\text{m}^{-1}] & \lambda~[\text{m}] & u_p~[\text{m/s}] & \eta~[\Omega] \\ \hline \text{glass} & \text{low-loss diel.} & 8.42\cdot 10^{-10} + j\,469 & 8.42\cdot 10^{-10} & 469 & 1.34\cdot 10^{-2} & 1.34\cdot 10^{8} & 168 + j\,3.03\cdot 10^{-10} \\[4pt] \text{tissue} & \text{quasi-conductor} & 9.75 + j\,12.2 & 9.75 & 12.2 & 5.12\cdot 10^{-1} & 5.20\cdot 10^{7} & 39.5 + j\,31.7 \\[4pt] \text{wood} & \text{good conductor} & (6.23 + j\,6.29)\cdot 10^{-4} & 6.23\cdot 10^{-4} & 6.29\cdot 10^{-4} & 9.99\cdot 10^{3} & 9.99\cdot 10^{6} & 6.29 + j\,6.28 \end{array} }$$

**Notes**

- These three examples show all regimes:
    
    - **Glass**: almost lossless, $u_p \approx c/\sqrt{\varepsilon_r}$, $\alpha$ tiny.
        
    - **Tissue**: comparable conduction and displacement currents — **strong attenuation** with still “wave-like” behavior.
        
    - **Wood** (as parameterized in the sheet): treated as **good conductor** with $\alpha \approx \beta$ and small $|\eta|$.
        
- Very exam-typical: “Given $(\mu_r,\varepsilon_r,\sigma,f)$, classify the material and compute $\gamma,\lambda,u_p,\eta$.”
    

---

### MATLAB — Exercise 13.1 (Improved Modular Script)
> [!code]- MATLAB 13.1 (Modular & Improved)
> ```matlab
> % ============================================================================
> % LOSSY MEDIA ANALYZER - Exercise 13.1 (Modular Version)
> % ============================================================================
> 
> clear; clc;
> 
> %% ======================== 1. DEFINE MATERIALS ==============================
> % Format: new_material(list, 'Name', epsilon_r, mu_r, sigma, frequency);
> 
> materials = []; % Initialize empty list
> 
> % Material 1: Glass (10 GHz)
> materials = new_material(materials, 'Glass', 5, 1, 10e-12, 10e9);
> 
> % Material 2: Tissue (100 MHz)
> materials = new_material(materials, 'Tissue', 12, 1, 0.3, 100e6);
> 
> % Material 3: Wood (1 kHz)
> materials = new_material(materials, 'Wood', 3, 1, 0.1e-3, 1e3);
> 
> %% ======================== 2. RUN ANALYSIS ==================================
> fprintf('\n========================================\n');
> fprintf('    LOSSY MEDIA ANALYSIS RESULTS\n');
> fprintf('========================================\n');
> 
> % Loop through the struct array
> for i = 1:length(materials)
>     analyze_and_print(materials(i));
> end
> 
> fprintf('========================================\n');
> fprintf('Analysis Complete! (%d materials processed)\n', length(materials));
> fprintf('========================================\n\n');
> 
> %% ======================== 3. HELPER FUNCTIONS ==============================
> 
> function list = new_material(list, name, er, mur, sigma, freq)
>     % Helper to append a new material to the list safely
>     newMat.name = name;
>     newMat.er = er;
>     newMat.mur = mur;
>     newMat.sigma = sigma;
>     newMat.freq = freq;
>     
>     if isempty(list)
>         list = newMat;
>     else
>         list(end+1) = newMat;
>     end
> end
> 
> function analyze_and_print(m)
>     % Constants
>     eps0 = 8.854e-12; 
>     mu0 = 4*pi*1e-7;   
> 
>     % Inputs
>     omega = 2*pi*m.freq;
>     eps = eps0 * m.er;
>     mu = mu0 * m.mur;
>     
>     % --- Physics Calculations ---
>     j = 1j;
>     gamma = sqrt(j*omega*mu*(m.sigma + j*omega*eps));
>     alpha = real(gamma);
>     beta = imag(gamma);
>     
>     lambda = 2*pi/beta;
>     up = omega/beta;
>     eta = sqrt(j*omega*mu/(m.sigma + j*omega*eps));
>     tand = m.sigma/(omega*eps);
>     
>     % Classification Logic
>     if tand < 0.1
>         type = 'Low-Loss Dielectric';
>     elseif tand > 10
>         type = 'Good Conductor';
>     else
>         type = 'Quasi-Conductor';
>     end
> 
>     % --- Display ---
>     fprintf('\n--- %s (f = %.2e Hz) ---\n', m.name, m.freq);
>     fprintf('  [Props] er=%.2f, ur=%.2f, sig=%.2e S/m\n', m.er, m.mur, m.sigma);
>     fprintf('  [Class] tan(d)=%.3e  ->  %s\n', tand, type);
>     fprintf('  [Waves] a=%.3e Np/m,  b=%.3e rad/m\n', alpha, beta);
>     fprintf('          w=%.3e m,     up=%.3e m/s\n', lambda, up);
>     fprintf('          n=%.3f + j%.3f Ohms\n', real(eta), imag(eta));
> end
> ```


## 13.2 — Dry Soil vs. Frequency

> **Given**  
> Dry soil: $\varepsilon_r = 2.5,\ \mu_r = 1,\ \sigma = 1.0\times 10^{-4}~\text{S/m}$.  
> For each frequency, classify the medium and compute $\gamma, \alpha, \beta, \lambda, u_p, \eta$:
>
> (a) $f = 60~\text{Hz}$  
> (b) $f = 1~\text{kHz}$  
> (c) $f = 1~\text{MHz}$  
> (d) $f = 1~\text{GHz}$  

---

### Theory recap

Same formulas as in 13.1, with **one fixed medium** and **varying frequency**.

Key behavior:

- $\omega\varepsilon$ scales linearly with $f$, while $\sigma$ is constant.
- Therefore
  $$
  \tan\delta(f) = \frac{\sigma}{\omega\varepsilon} \propto \frac{1}{f}.
  $$
- As $f$ increases:
  - $\tan\delta$ decreases.
  - Low frequencies → conduction dominates → **good conductor**.
  - High frequencies → displacement current dominates → **low-loss dielectric**; intermediate → **quasi-conductor**.

This is exactly what the solution table illustrates

---

### Results & classification

Using the same general formulas as before, we obtain:

$$
\boxed{
\begin{array}{c|c|c|c|c|c|c}
f & \text{type} & \gamma~[\text{m}^{-1}] & \alpha & \beta & \lambda & u_p & \eta \\
\hline
60~\text{Hz} &
\text{good conductor} &
(1.54 + j\,1.54)\cdot 10^{-4} &
1.54\cdot 10^{-4} &
1.54\cdot 10^{-4} &
4.08\cdot 10^{4} &
2.45\cdot 10^{6} &
1.54 + j\,1.54
\\[4pt]
1~\text{kHz} &
\text{good conductor} &
(6.28 + j\,6.29)\cdot 10^{-4} &
6.28\cdot 10^{-4} &
6.29\cdot 10^{-4} &
9.99\cdot 10^{3} &
9.99\cdot 10^{6} &
6.29 + j\,6.29
\\[4pt]
1~\text{MHz} &
\text{quasi-conductor} &
(1.13 + j\,3.50)\cdot 10^{-2} &
1.13\cdot 10^{-2} &
3.50\cdot 10^{-2} &
1.79\cdot 10^{2} &
1.79\cdot 10^{8} &
2.04\cdot 10^{2} + j\,65.8
\\[4pt]
1~\text{GHz} &
\text{low-loss diel.} &
1.12\cdot 10^{-2} + j\,33.1 &
1.12\cdot 10^{-2} &
33.1 &
1.90\cdot 10^{-1} &
1.90\cdot 10^{8} &
2.38\cdot 10^{2} + j\,8.57\cdot 10^{-2}
\end{array}
}
$$

(All numeric values match the official solution table.)

**Notes**

- Dry soil transitions from “very lossy / conductor-like” at low $f$ to “dielectric-like” at high $f$.
- A classic exam pattern: *“Same medium, varying frequency → how do $\alpha,\beta,\eta$ and classification change?”*

---

### MATLAB — Exercise 13.2 (frequency sweep for dry soil)
> [!code]- MATLAB 13.2 (Dry Soil Analysis)
> ```matlab
> % ============================================================================
> % EXERCISE 13.2 SOLVER: Dry Soil Analysis
> % ============================================================================
> 
> clear; clc;
> 
> %% ======================== 1. DEFINE MATERIALS ==============================
> % Problem Statement: Dry Soil
> % Parameters: er = 2.5, mur = 1, sigma = 1e-4 S/m
> % Frequencies: 60 Hz, 1 kHz, 1 MHz, 1 GHz
> 
> materials = []; 
> 
> % Define the constant properties for Dry Soil
> er_soil = 2.5;
> mur_soil = 1;
> sig_soil = 1e-4; % 1 * 10^-4
> 
> % Add the 4 cases from the exercise:
> % usage: new_material(list, 'Name', er, mur, sigma, freq)
> 
> % Case a) 60 Hz
> materials = new_material(materials, 'Dry Soil (a)', er_soil, mur_soil, sig_soil, 60);
> 
> % Case b) 1 kHz (1e3 Hz)
> materials = new_material(materials, 'Dry Soil (b)', er_soil, mur_soil, sig_soil, 1e3);
> 
> % Case c) 1 MHz (1e6 Hz)
> materials = new_material(materials, 'Dry Soil (c)', er_soil, mur_soil, sig_soil, 1e6);
> 
> % Case d) 1 GHz (1e9 Hz)
> materials = new_material(materials, 'Dry Soil (d)', er_soil, mur_soil, sig_soil, 1e9);
> 
> 
> %% ======================== 2. RUN ANALYSIS ==================================
> fprintf('\n========================================\n');
> fprintf('    EXERCISE 13.2 RESULTS\n');
> fprintf('========================================\n');
> 
> for i = 1:length(materials)
>     analyze_and_print(materials(i));
> end
> 
> fprintf('========================================\n');
> fprintf('Analysis Complete!\n');
> fprintf('========================================\n\n');
> 
> 
> %% ======================== 3. HELPER FUNCTIONS ==============================
> 
> function list = new_material(list, name, er, mur, sigma, freq)
>     newMat.name = name;
>     newMat.er = er;
>     newMat.mur = mur;
>     newMat.sigma = sigma;
>     newMat.freq = freq;
>     
>     if isempty(list)
>         list = newMat;
>     else
>         list(end+1) = newMat;
>     end
> end
> 
> function analyze_and_print(m)
>     % Constants
>     eps0 = 8.854e-12; 
>     mu0 = 4*pi*1e-7;   
> 
>     % Inputs
>     omega = 2*pi*m.freq;
>     eps = eps0 * m.er;
>     mu = mu0 * m.mur;
>     
>     % --- Physics Calculations ---
>     j = 1j;
>     gamma = sqrt(j*omega*mu*(m.sigma + j*omega*eps));
>     alpha = real(gamma);
>     beta = imag(gamma);
>     
>     lambda = 2*pi/beta;
>     up = omega/beta;
>     eta = sqrt(j*omega*mu/(m.sigma + j*omega*eps));
>     tand = m.sigma/(omega*eps);
>     
>     % Classification Logic
>     if tand < 0.1
>         type = 'Low-Loss Dielectric';
>     elseif tand > 10
>         type = 'Good Conductor';
>     else
>         type = 'Quasi-Conductor';
>     end
> 
>     % --- Display ---
>     fprintf('\n--- %s [f = %.0e Hz] ---\n', m.name, m.freq);
>     fprintf('  Classification: %s (tan(d) = %.3e)\n', type, tand);
>     fprintf('  gamma (prop)  = %.3e + j%.3e [1/m]\n', alpha, beta);
>     fprintf('  alpha (atten) = %.3e [Np/m]\n', alpha);
>     fprintf('  beta (phase)  = %.3e [rad/m]\n', beta);
>     fprintf('  lambda        = %.3e [m]\n', lambda);
>     fprintf('  u_p (velocity)= %.3e [m/s]\n', up);
>     fprintf('  eta (imp)     = %.3e + j%.3e [Ohms]\n', real(eta), imag(eta));
> end
> ```
---

## 13.3 — Skin Depth in Seawater (1 kHz–10 GHz)

> **Given**  
> Seawater parameters:
> - $\mu_r = 1$  
> - $\varepsilon_r = 80$  
> - $\sigma = 4~\text{S/m}$  
>
> **Task**  
> Plot the **skin depth** $\delta_s$ versus frequency for $f \in [1~\text{kHz},\,10~\text{GHz}]$ on a **log–log** scale.  
> The official solution shows a log–log plot with $\delta_s$ decreasing strongly with frequency.  

---

### Theory recap — skin depth

For a uniform plane wave in a lossy medium:

- Attenuation constant: $\alpha$ (in Np/m).  
- **Skin depth**:
  $$
  \delta_s = \frac{1}{\alpha}.
  $$

General $\alpha$ (from lossy-medium formulas):
$$
\alpha = \omega\sqrt{\frac{\mu\varepsilon}{2}}
\left[
\sqrt{1 + \left(\frac{\sigma}{\omega\varepsilon}\right)^2} - 1
\right]^{1/2}.
$$

For a **good conductor** ($\sigma \gg \omega\varepsilon$) we often use the approximation:
$$
\alpha \approx \sqrt{\frac{\omega\mu\sigma}{2}},
\qquad
\delta_s \approx \sqrt{\frac{2}{\omega\mu\sigma}}.
$$

For seawater:
- At lower frequencies, $\sigma$ is large compared to $\omega\varepsilon$ → good-conductor approximation is valid.  
- At higher GHz range, $\omega\varepsilon$ becomes comparable; using the **general formula** is safest across the whole band.

---

### Qualitative behavior

- As $f$ increases, $\delta_s$ **decreases roughly as $1/\sqrt{f}$** in the conductor-like regime.  
- For seawater with $\sigma=4~\text{S/m}$:
  - At kHz frequencies, $\delta_s$ is on the order of **meters**.  
  - At MHz, on the order of **decimeters**.  
  - At GHz, on the order of **centimeters** or less.
- This explains why radio waves at higher frequencies cannot penetrate deeply into seawater (important for submarine communication, etc.).

---

### MATLAB — Exercise 13.3 (skin depth plot for seawater)
> [!code]- MATLAB 13.3 (Skin Depth Plotter)
> ```matlab
> % ============================================================================
> % EXERCISE 13.3: Skin Depth of Seawater
> % ============================================================================
> 
> clear; clc; close all;
> 
> %% --- 1. Parameters ---
> eps0 = 8.854e-12;
> mu0  = 4*pi*1e-7;
> 
> % Seawater
> er    = 80;
> mur   = 1;
> sigma = 4; % S/m
> 
> % Derived
> eps = eps0 * er;
> mu  = mu0 * mur;
> 
> %% --- 2. Calculation ---
> % Log-spaced frequency vector from 1 kHz to 10 GHz
> f = logspace(3, 10, 500); % 10^3 to 10^10 Hz
> w = 2*pi*f;
> 
> % Complex propagation constant (Exact formula)
> % Gamma = alpha + j*beta = sqrt(j*w*mu*(sigma + j*w*eps))
> gamma = sqrt(1j .* w .* mu .* (sigma + 1j .* w .* eps));
> 
> alpha = real(gamma);      % Attenuation constant [Np/m]
> delta_s = 1 ./ alpha;     % Skin depth [m]
> 
> %% --- 3. Plotting ---
> figure('Color', 'w');
> loglog(f, delta_s, 'LineWidth', 2, 'Color', 'b');
> grid on;
> 
> % Formatting
> title('Skin Depth vs. Frequency (Seawater)');
> xlabel('Frequency f [Hz]');
> ylabel('Skin Depth \delta_s [m]');
> xlim([1e3, 1e10]);
> 
> % Add markers for specific points
> hold on;
> marker_freqs = [1e3, 1e6, 1e9, 10e9];
> marker_indices = dsearchn(f', marker_freqs'); % Find nearest indices
> loglog(f(marker_indices), delta_s(marker_indices), 'ro', 'MarkerFaceColor', 'r');
> 
> % Annotation
> text(1.5e3, 5, 'Good Conductor (\propto 1/\surd{f})', 'FontSize', 10);
> text(1e8, 0.05, 'Dielectric limit \rightarrow', 'FontSize', 10, 'HorizontalAlignment', 'right');
> ```