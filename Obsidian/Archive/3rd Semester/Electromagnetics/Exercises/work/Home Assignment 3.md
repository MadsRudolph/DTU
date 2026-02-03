
> 🔗 [[MOC – Electromagnetics]]  
> **Context:** Electrostatics & magnetostatics in matter – conductors with cavities, charge distributions, capacitors, Ampère’s law, Lorentz force, and inductors.

> [!info] 🧩 Quick Formula Recap — HA3
>
> **Gauss’ law (electric)**
> - $\displaystyle \oint_S \mathbf D\cdot d\mathbf s = Q_{\text{enc}}$  
> - $\displaystyle \mathbf D = \varepsilon \mathbf E,\quad \varepsilon = \varepsilon_0\varepsilon_r$
> - **Conductor in electrostatics:** $\mathbf E = 0$ inside; any excess free charge lives on surfaces.
>
> **Symmetric charge distributions**
> - Uniform sphere, charge density $\rho_v$:
>   $$
>   Q_{\text{tot}} = \rho_v \frac{4}{3}\pi r_s^3
>   $$
>   $$
>   E(r) =
>   \begin{cases}
>   \dfrac{\rho_v r}{3\varepsilon}, & r<r_s\\[4pt]
>   \dfrac{Q_{\text{tot}}}{4\pi\varepsilon r^2}, & r\ge r_s
>   \end{cases}
>   $$
>
> **Electrostatic work**
> - $\displaystyle W = q\int_{\mathbf r_1}^{\mathbf r_2}\mathbf E\cdot d\mathbf l$  
> - If motion is perpendicular to $\mathbf E$ → $W=0$.
>
> **Capacitance**
> - Parallel plates: $\displaystyle C=\frac{\varepsilon A}{d}$, with $E_{\max}=V_{\max}/d$ (dielectric strength).  
> - Two parallel wires (radius $R$, spacing $d$):
>   $$
>   C' = \frac{\pi\varepsilon}{\operatorname{arcosh}\!\bigl(\dfrac{d}{2R}\bigr)},
>   \qquad C = C'\ell
>   $$
>
> **Magnetostatics**
> - Ampère: $\displaystyle \oint_C \mathbf H\cdot d\mathbf l = I_{\text{free,enc}}$  
> - Right–hand rule: thumb along current, fingers curl in direction of $\mathbf B$; or fingers along current loop, thumb along $\mathbf B$ at its center.
> - Lorentz force: $\displaystyle \mathbf F = q\,\mathbf v\times \mathbf B$.
>
> **Fields from simple currents**
> - Long straight wire: $\displaystyle H_\phi = \dfrac{I}{2\pi\rho}$  
> - Square loop (side $\ell$) at center:
>   $$
>   H = \frac{2\sqrt{2}I}{\pi\ell}
>   $$
>
> **Inductance**
> - Long solenoid: $\displaystyle L=\frac{\mu N^2 A}{\ell}$  
> - Toroid (mean path length $\ell_m$, cross-section area $A$):
>   $$
>   L=\frac{\mu N^2 A}{\ell_m},\qquad \mu = \mu_0\mu_r
>   $$
>
> **Unit reminders**
> - $1~\text{fC}=10^{-15}$ C, $1~\text{nC}=10^{-9}$ C  
> - $1~\text{mm}=10^{-3}$ m, $1~\text{cm}=10^{-2}$ m  

---

## Section 1 — Conductor with a cavity (Q1–Q2)

![[Images/Section1.png]]

> [!summary] **Question 1 — Regions with non-zero $\vec E$**
>
> A neutral conductor has an air-filled cavity (**Region 1**). The conductor itself is **Region 2**, and the exterior is **Region 3**.  
> Four point charges inside the cavity (not touching the conductor):
> $$
> Q_1=7~\text{fC},\quad Q_2=-2~\text{fC},\quad Q_3=-3~\text{fC},\quad Q_4=2~\text{fC}.
> $$
> **Which regions have non-zero electrostatic field $\vec E$?**

💡 **Concept**

- Electrostatic equilibrium in a perfect conductor:
  $$
  \mathbf E = 0 \quad \text{everywhere inside the conductor (Region 2).}
  $$
- Charges in the cavity produce an electric field in the cavity volume (Region 1).
- The net cavity charge induces equal and opposite surface charge on the **inner surface**, and a compensating charge on the **outer surface**, which creates a field in Region 3.

🧮 **Reasoning**

Total charge in the cavity:

$$
Q_{\text{cav}} = 7-2-3+2 = 4~\text{fC}\neq 0.
$$

- Region 1: non-zero field due to the four charges.  
- Region 2: field must be zero in an ideal conductor.  
- Region 3: non-zero field due to induced net charge on the outer surface.

✅ **Answer:** $\boxed{\text{Regions 1 and 3}}$

> [!code]- MATLAB — Cavity charge & non-zero field regions (reusable)
>  How to use: Change `Q_fC` (and `is_conductor_neutral` if needed) for your problem, run the cell, and read off which regions have non-zero E from the printed 0/1 flags.
> ```matlab
> %% HA3 – Section 1, Q1
> % Compute total cavity charge and which regions have non-zero E
> % Assumptions:
> %   - Ideal conductor (E = 0 inside metal)
> %   - Conductor as a whole is electrically neutral
> 
> % ---- INPUTS (edit for new problems) ----
> Q_fC = [7, -2, -3, 2];   % charges in the cavity [fC]
> is_conductor_neutral = true;
> 
> % ---- CORE CALCULATION ----
> Q_cav = sum(Q_fC);        % [fC] total free charge in cavity
> 
> % Region 1 (cavity): non-zero E if net charge is non-zero
> E_R1_nonzero = (Q_cav ~= 0);
> 
> % Region 2 (conductor): ideal conductor → E = 0
> E_R2_nonzero = false;
> 
> % Region 3 (outside): if conductor is neutral and Q_cav ≠ 0,
> % there will be induced charge on the outer surface → non-zero E.
> if is_conductor_neutral && (Q_cav ~= 0)
>     E_R3_nonzero = true;
> else
>     % (more general logic could go here)
>     E_R3_nonzero = false;
> end
> 
> % ---- OUTPUT / DISPLAY ----
> fprintf('Total cavity charge Q_cav = %.2f fC\n', Q_cav);
> fprintf('Non-zero E in Region 1: %d\n', E_R1_nonzero);
> fprintf('Non-zero E in Region 2: %d\n', E_R2_nonzero);
> fprintf('Non-zero E in Region 3: %d\n', E_R3_nonzero);
> 
> % Interpretation: 1 = true, 0 = false
> ```

---

> [!summary] **Question 2 — Charge on the outer conducting surface**
>
> **What is the total charge on the conducting surface between Region 2 and 3?**

💡 **Concept**

- Choose a Gaussian surface **inside** the conductor, hugging the inner cavity surface. Since $\mathbf E=0$ there:
  $$
  Q_{\text{enc}} = Q_{\text{cav}} + Q_{\text{inner}} = 0
  \Rightarrow Q_{\text{inner}} = -Q_{\text{cav}}.
  $$
- The **total conductor** is given as neutral:
  $$
  Q_{\text{conductor}} = Q_{\text{inner}} + Q_{\text{outer}} = 0
  \Rightarrow Q_{\text{outer}} = -Q_{\text{inner}}.
  $$

🧮 **Derivation**

1. Inner surface charge:
   $$
   Q_{\text{inner}} = -Q_{\text{cav}} = -4~\text{fC}.
   $$
2. Outer surface charge:
   $$
   Q_{\text{outer}} = -Q_{\text{inner}} = +4~\text{fC}.
   $$

✅ **Answer:** $\boxed{Q_{\text{outer}} = 4~\text{fC}}$

🧩 **Interpretation**

The conductor “rearranges” its charges so that:

- The field inside the metal is zero.  
- The conductor’s net charge remains zero.  

This forces $-4$ fC onto the inner cavity surface and $+4$ fC onto the outer surface.

> [!code]- MATLAB — Induced inner/outer surface charges (reusable)
>  How to use: Set `Q_fC` to the cavity charges and `Q_conductor_total_fC` to the net conductor charge, run the cell, and read off `Q_inner` and `Q_outer` from the console.
> ```matlab
> %% HA3 – Section 1, Q2
> % Compute induced charges on inner and outer surfaces of a neutral conductor
> % given the charges inside the cavity.
> 
> % ---- INPUTS (edit for new problems) ----
> Q_fC = [7, -2, -3, 2];   % charges in cavity [fC]
> Q_conductor_total_fC = 0; % net charge of the whole conductor [fC]
> 
> % ---- CORE CALCULATION ----
> Q_cav_fC    = sum(Q_fC);
> Q_inner_fC  = -Q_cav_fC;                      % from Gauss' law (inside metal)
> Q_outer_fC  = Q_conductor_total_fC - Q_inner_fC;
> 
> % ---- OUTPUT / DISPLAY ----
> fprintf('Total cavity charge   Q_cav    = %.2f fC\n', Q_cav_fC);
> fprintf('Inner surface charge Q_inner  = %.2f fC\n', Q_inner_fC);
> fprintf('Outer surface charge Q_outer  = %.2f fC\n', Q_outer_fC);
> 
> % For this HA3 case: Q_cav = 4 fC → Q_inner = -4 fC, Q_outer = +4 fC
> ```

---

## Section 2 — Charge distributions & electrostatic work (Q3–Q4)

> [!summary] **Question 3 — Field of a uniformly charged sphere in a dielectric**
>
> A sphere of radius $r_s = 2.2~\text{cm}$ carries a uniform volume charge density $\rho_v = 4.0~\text{nC/m}^3$.  
> It is embedded in a dielectric with $\varepsilon_r = 2.1$.  
> **Find** the electric field magnitude at $R=4.5~\text{cm}$ from the center, in $\text{V/m}$.

💡 **Concept**

For $R>r_s$, a uniformly charged sphere behaves like a **point charge** $Q$ at its center:

$$
E(R) = \frac{Q}{4\pi\varepsilon R^2},\quad Q=\rho_v\frac{4}{3}\pi r_s^3.
$$

🧮 **Derivation**

Convert to SI:

- $r_s = 2.2~\text{cm} = 0.022~\text{m}$  
- $R = 4.5~\text{cm} = 0.045~\text{m}$  
- $\rho_v = 4.0~\text{nC/m}^3 = 4.0\times 10^{-9}~\text{C/m}^3$  
- $\varepsilon = \varepsilon_0\varepsilon_r = 8.854\times 10^{-12}\cdot 2.1~\text{F/m}$

Total charge:

$$
Q = \rho_v\frac{4}{3}\pi r_s^3
  \approx 1.78\times 10^{-13}~\text{C}.
$$

Field at $R$:

$$
E(R) = \frac{Q}{4\pi\varepsilon R^2}
      \approx 0.377~\text{V/m}.
$$

✅ **Answer:** $\boxed{E(4.5~\text{cm}) \approx 0.38~\text{V/m}}$

![[Images/EM_HA3_Q3_Esphere.png]]

> [!info] **What this graph shows & why it’s useful**
>
> - The **x-axis** is the distance from the center, $r$ in cm.  
> - The **y-axis** is the magnitude of the electric field, $E(r)$ in V/m.  
> - For $0<r<r_s$, the field grows **linearly** with $r$ (Gauss’ law inside a uniform volume charge: $E\propto r$).  
> - For $r>r_s$, the sphere behaves like a **point charge** and the field falls off as $1/r^2$.  
> - The graph lets you:
>   - Visually confirm the **piecewise behaviour** (linear inside, $1/r^2$ outside).  
>   - Read off $E$ at your homework radius $R=4.5$ cm and see it matches $\approx0.38$ V/m.  
>   - Use it as a quick **sanity check** when doing similar Gauss-law problems (is your computed $E(R)$ on the right side of the peak and roughly the right size?).

> [!code]- MATLAB — Uniformly charged sphere in a dielectric (reusable)
>  How to use: Set `rs_cm`, `R_cm`, `rho_nCpm3`, and `eps_r` for your case.
>  Run the cell to get E(R) and an annotated E(r) plot exported for Obsidian.
> ```matlab
> %% HA3 – Section 2, Q3
> % Field of a uniformly charged sphere embedded in a dielectric
> % Computes E(R) and (optionally) E(r) profile inside/outside the sphere.
> 
> % ---- INPUTS (edit for new problems) ----
> rs_cm      = 2.2;    % sphere radius [cm]
> R_cm       = 4.5;    % observation radius [cm]
> rho_nCpm3  = 4.0;    % volume charge density [nC/m^3]
> eps_r      = 2.1;    % relative permittivity of surrounding dielectric
> RUN_PLOT   = true;   % set false if you only want the numeric value at R
> 
> % ---- CONSTANTS ----
> eps0   = 8.854e-12;           % [F/m]
> 
> % ---- UNIT CONVERSIONS ----
> rs   = rs_cm * 1e-2;          % [m]
> R    = R_cm  * 1e-2;          % [m]
> rho  = rho_nCpm3 * 1e-9;      % [C/m^3]
> eps  = eps0 * eps_r;          % [F/m]
> 
> % ---- TOTAL CHARGE ----
> Qtot = rho * (4/3)*pi*rs^3;   % [C]
> 
> % ---- FIELD AT R (outside or inside) ----
> if R > rs
>     % Outside: behaves like a point charge
>     E_R = Qtot / (4*pi*eps*R^2);
> else
>     % Inside: linear in r
>     E_R = rho * R / (3*eps);
> end
> 
> fprintf('Total charge Q = %.3e C\n', Qtot);
> fprintf('E(R = %.2f cm) = %.3f V/m\n', R_cm, E_R);
> 
> % ---- OPTIONAL: E(r) profile for visualization + export to Obsidian ----
> if RUN_PLOT
>     % extend r far enough so the curve passes the point R
>     r_max = max(2*rs, 1.1*R);      % [m]
>     r     = linspace(0, r_max, 400);   % [m]
>     E_r   = zeros(size(r));
> 
>     inside  = (r > 0) & (r <= rs);
>     outside = (r > rs);
> 
>     E_r(inside)  = rho .* r(inside)  / (3*eps);
>     E_r(outside) = Qtot ./ (4*pi*eps.*r(outside).^2);
> 
>     figure;
>     plot(r*100, E_r, 'LineWidth', 1.5); grid on; hold on;
>     xlabel('r [cm]');
>     ylabel('E(r) [V/m]');
>     title('Electric field of uniformly charged sphere in dielectric');
> 
>     % ---- DOTTED GUIDES THROUGH THE HOMEWORK POINT ----
>     xline(R_cm, ':', sprintf('R = %.1f cm', R_cm), ...
>           'LabelVerticalAlignment','bottom', ...
>           'LabelHorizontalAlignment','center');
>     yline(E_R, ':', sprintf('E(R) = %.2f V/m', E_R), ...
>           'LabelHorizontalAlignment','left', ...
>           'LabelVerticalAlignment','middle');
>     plot(R_cm, E_R, 'o', 'MarkerSize', 6);   % intersection marker
> 
>     % ---- EXPORT TO OBSIDIAN IMAGES FOLDER ----
>     imgDir = 'C:\Users\Mads2\DTU\Obsidian\Courses\Electromagnetics\Images';
>     if ~exist(imgDir,'dir')
>         mkdir(imgDir);
>     end
>     exportgraphics(gcf, fullfile(imgDir, 'EM_HA3_Q3_Esphere.png'), ...
>                    'Resolution', 300);
> end
> ```



---

> [!summary] **Question 4 — Work done moving a charge in a uniform field**
>
> A charge $Q = 1~\text{nC}$ is (slowly) moved along the $x$-axis from $x_1 = 2~\text{mm}$ to $x_2 = 7~\text{mm}$ in a uniform electric field  
> $\vec E = -5\,\hat{\mathbf y}~\text{V/m}$.  
> **What is the work required to move the charge?**

💡 **Concept**

Work done by the electric field:

$$
W = Q\int_{\mathbf r_1}^{\mathbf r_2} \vec E\cdot d\vec l.
$$

If motion is **perpendicular** to $\vec E$, then $\vec E\cdot d\vec l = 0$ everywhere and $W=0$.

🧮 **Derivation**

- Displacement is along $\hat{\mathbf x}$.  
- Field is along $-\hat{\mathbf y}$.

Thus the dot product:

$$
\vec E\cdot d\vec l = (-5\hat{\mathbf y})\cdot (dx\,\hat{\mathbf x}) = 0.
$$

Therefore

$$
W = 0.
$$

✅ **Answer:** $\boxed{W = 0~\text{J}}$

🧩 **Interpretation**

Electrostatic potential only depends on movement **along** the field lines.  
Moving purely sideways in a uniform field changes neither potential energy nor potential.

> [!code]- MATLAB — Work moving a charge in a uniform E-field (reusable)
>  How to use: Set `Q_nC`, the field vector `E_vec`, and start/end positions `r1`/`r2` (in mm here), run the cell, and read off the computed work W.
> ```matlab
> %% HA3 – Section 2, Q4
> % Work required to move a point charge in a uniform electric field
> % W = Q * E · (r2 - r1) for constant E.
> 
> % ---- INPUTS (edit for new problems) ----
> Q_nC  = 1.0;                         % charge [nC]
> E_vec = [0, -5, 0];                  % uniform E-field [V/m] as [Ex Ey Ez]
> x1_mm = 2.0;                         % initial x-position [mm]
> x2_mm = 7.0;                         % final   x-position [mm]
> 
> % (You can also set full 3D positions, e.g. r1 = [x1 y1 z1], r2 = [x2 y2 z2])
> r1_mm = [x1_mm, 0, 0];               % [mm]
> r2_mm = [x2_mm, 0, 0];               % [mm]
> 
> % ---- UNIT CONVERSIONS ----
> Q  = Q_nC * 1e-9;                    % [C]
> r1 = r1_mm * 1e-3;                   % [m]
> r2 = r2_mm * 1e-3;                   % [m]
> 
> % ---- CORE CALCULATION ----
> dl = r2 - r1;                        % displacement vector [m]
> W  = Q * dot(E_vec, dl);            % work done by field [J]
> 
> % ---- OUTPUT / DISPLAY ----
> fprintf('Displacement dl = [%.3e %.3e %.3e] m\n', dl);
> fprintf('Work W = %.3e J\n', W);
> 
> if abs(W) < 1e-15
>     fprintf('Result is numerically ~0 J (motion perpendicular to E).\n');
> end
> ```

---

## Section 3 — Capacitors (Q5–Q6)

> [!summary] **Question 5 — Capacitance of two parallel wires**
>
> Two parallel cylindrical wires form a capacitor.  
> - Radius: $R = 0.23~\text{mm}$  
> - Length: $\ell = 105~\text{cm}$  
> - Center–to–center distance: $d = 1.2~\text{mm}$  
> - Dielectric: $\varepsilon_r = 94$  
>
> **Find** the capacitance $C$ in nF.

💡 **Concept**

Capacitance per unit length for two parallel wires:

$$
C' = \frac{\pi\varepsilon}{\operatorname{arcosh}\!\left(\frac{d}{2R}\right)},
\qquad C = C'\,\ell.
$$

🧮 **Derivation**

Convert to SI:

- $R = 0.23~\text{mm} = 0.00023~\text{m}$  
- $d = 1.2~\text{mm} = 0.0012~\text{m}$  
- $\ell = 105~\text{cm} = 1.05~\text{m}$  
- $\varepsilon = \varepsilon_0\varepsilon_r = 8.854\times 10^{-12}\cdot 94$

Capacitance:

$$
C' = \frac{\pi\varepsilon}{\operatorname{arcosh}\!\left(\dfrac{d}{2R}\right)}
\approx 1.62\times 10^{-9}~\text{F/m},
$$
$$
C = C'\ell \approx 1.70\times 10^{-9}~\text{F} = 1.70~\text{nF}.
$$

✅ **Answer:** $\boxed{C \approx 1.70~\text{nF}}$

> [!code]- MATLAB — Two parallel wires capacitance (reusable)
> How to use: Set `R_mm`, `d_mm`, `ell_cm`, and `eps_r` for your geometry and run. The script prints $C'$ in F/m and $C$ in nF.
> ```matlab
> %% HA3 – Section 3, Q5
> % Capacitance of two parallel cylindrical wires in a dielectric
> 
> % ---- INPUTS (edit for new problems) ----
> R_mm   = 0.23;    % wire radius [mm]
> d_mm   = 1.2;     % center-to-center distance [mm]
> ell_cm = 105;     % wire length [cm]
> eps_r  = 94;      % relative permittivity of dielectric
> 
> % ---- CONSTANTS ----
> eps0 = 8.854e-12;           % [F/m]
> 
> % ---- UNIT CONVERSIONS ----
> R   = R_mm   * 1e-3;        % [m]
> d   = d_mm   * 1e-3;        % [m]
> ell = ell_cm * 1e-2;        % [m]
> eps = eps0 * eps_r;         % [F/m]
> 
> % ---- CAPACITANCE PER UNIT LENGTH & TOTAL ----
> % MATLAB uses acosh() for inverse hyperbolic cosine
> C_per_m = pi*eps / acosh(d/(2*R));   % [F/m]
> C       = C_per_m * ell;             % [F]
> 
> fprintf('C'' = %.3e F/m\n', C_per_m);
> fprintf('C  = %.3f nF\n', C*1e9);
> 
> % Quick sanity checks
> if d <= 2*R
>     warning('Geometry invalid: d must be > 2R for two separate wires.');
> end
> ```

---

> [!summary] **Question 6 — Plate area with capacitance and breakdown constraints**
>
> A parallel-plate capacitor must satisfy:
> - Capacitance: $C = 744~\text{pF}$  
> - Max voltage: $V_{\max} = 1.22~\text{kV}$  
> - Dielectric: $\varepsilon_r = 182$, dielectric strength $E_{\max} = 35~\text{kV/mm}$  
>
> **Find** the required area $A$ of each plate in $\text{mm}^2$.

💡 **Concept**

We must satisfy **both**:

1. Breakdown: $E = V_{\max}/d \le E_{\max}$ → choose $d = V_{\max}/E_{\max}$.
2. Capacitance: $C = \varepsilon A/d$ → solve for $A$.

🧮 **Derivation**

1. Convert units and find $d$:
   $$
   E_{\max} = 35~\frac{\text{kV}}{\text{mm}}
            = 3.5\times 10^{7}~\text{V/m},
   $$
   $$
   V_{\max} = 1.22\times 10^{3}~\text{V},
   $$
   $$
   d = \frac{V_{\max}}{E_{\max}}
     \approx 3.49\times 10^{-5}~\text{m}.
   $$

2. Capacitance condition with $\varepsilon = \varepsilon_0\varepsilon_r$:

   $$
   A = \frac{C d}{\varepsilon}
     = \frac{744\times 10^{-12}\cdot 3.49\times 10^{-5}}
            {8.854\times 10^{-12}\cdot 182}
     \approx 1.61\times 10^{-5}~\text{m}^2.
   $$

3. Convert to $\text{mm}^2$:

   $$
   A_{\text{mm}^2} = A\cdot 10^{6} \approx 16.094~\text{mm}^2.
   $$

✅ **Answer:** $\boxed{A \approx 16.094~\text{mm}^2}$

🧩 **Interpretation**

The dielectric strength fixes the **minimum spacing**; once $d$ is set, the only way to hit the required $C$ is by choosing the proper plate area.

> [!code]- MATLAB — Parallel-plate area with breakdown limit (reusable)
> How to use: Set `C_pF`, `Vmax_kV`, `Emax_kV_per_mm`, and `eps_r`. Run to get the minimum plate spacing `d` and the required plate area `A` in mm².
> ```matlab
> %% HA3 – Section 3, Q6
> % Plate area of a parallel-plate capacitor with breakdown constraint
> 
> % ---- INPUTS (edit for new problems) ----
> C_pF          = 744;   % capacitance [pF]
> Vmax_kV       = 1.22;  % maximum voltage [kV]
> Emax_kV_per_mm = 35;   % dielectric strength [kV/mm]
> eps_r         = 182;   % relative permittivity of dielectric
> 
> % ---- CONSTANTS ----
> eps0 = 8.854e-12;      % [F/m]
> 
> % ---- UNIT CONVERSIONS ----
> C    = C_pF * 1e-12;          % [F]
> Vmax = Vmax_kV * 1e3;         % [V]
> Emax = Emax_kV_per_mm * 1e6;  % [V/m]   (1 kV/mm = 1e6 V/m)
> eps  = eps0 * eps_r;          % [F/m]
> 
> % ---- BREAKDOWN-LIMITED SPACING ----
> d = Vmax / Emax;              % [m]
> 
> % ---- REQUIRED AREA ----
> A      = C * d / eps;         % [m^2]
> A_mm2  = A * 1e6;             % [mm^2]
> 
> fprintf('Breakdown-limited spacing d = %.3f mm\n', d*1e3);
> fprintf('Required plate area A       = %.2f mm^2\n', A_mm2);
> 
> % Optional: sanity check that E at Vmax is right on the limit
> E_check = Vmax / d;
> fprintf('E(Vmax) = %.2e V/m (should equal Emax = %.2e V/m)\n', ...
>         E_check, Emax);
> ```


---
## Section 4 — Ampère’s law & Lorentz force (Q7–Q9)

> [!summary] **Question 7 — Correct sketches for current and $\vec B$**
>
> Several sketches show either:  
> - a circular **current** with a central $\vec B$ indicated by $\odot$ (out of page) / $\otimes$ (into page), or  
> - a central **current** ($\odot$ / $\otimes$) and a circular $\vec B$.  
>
> **Which sketches have consistent directions according to the right-hand rule?**

**Sketches**

| Sketch 1          | Sketch 2          |
| ----------------- | ----------------- |
| ![[Images/1.png]] | ![[Images/2.png]] |

| Sketch 3          | Sketch 4          |
| ----------------- | ----------------- |
| ![[Images/3.png]] | ![[Images/4.png]] |

💡 **Concept**

- **Straight wire:** thumb along current $I$, fingers curl in direction of $\vec B$.  
- **Current loop:** fingers along current direction, thumb gives the direction of $\vec B$ through the loop.

🧮 **Reasoning**

All four sketches use the **same circular direction** for the ring (clockwise as seen from the viewer).

1. **Sketch 1 — Loop current clockwise, $\vec B$ out of page ($\odot$)**  
   - For a clockwise loop, curling fingers clockwise makes the thumb point **into** the page.  
   - Here $\vec B$ is drawn **out** of the page → mismatch. ✖ Incorrect.

2. **Sketch 2 — Loop current clockwise, $\vec B$ into page ($\otimes$)**  
   - Clockwise loop → thumb points **into** the page.  
   - $\vec B$ is into the page → consistent with the right-hand rule. ✔ Correct.

3. **Sketch 3 — Current out of page ($\odot$), $\vec B$ clockwise**  
   - For a straight current **out** of the page, fingers curl **counter-clockwise** around the wire.  
   - $\vec B$ is drawn clockwise → wrong sense. ✖ Incorrect.

4. **Sketch 4 — Current into page ($\otimes$), $\vec B$ clockwise**  
   - For a straight current **into** the page, fingers curl **clockwise**.  
   - $\vec B$ is clockwise → correct. ✔ Correct.

✅ **Answer:** $\boxed{\text{Sketches 2 and 4 are correct}}$


---
> [!summary] **Question 8 — Path of a moving positive charge in $\vec B$**
>
> A positive charge $+q$ moves with constant velocity $\vec u$ to the right, in a magnetic flux density $\vec B$ that points **into** the page.  
> Three possible curved paths (1 up, 2 straight, 3 down) are shown.  
> **Which path does the charge follow?**

![[Images/Section6.png]]

💡 **Concept**

Magnetic force (Lorentz):

$$
\mathbf F = q\,\mathbf u\times\mathbf B.
$$

For $q>0$, the direction is that of $\mathbf u\times\mathbf B$.

🧮 **Direction**

Take coordinates:

- $\vec u$ along $+\hat{\mathbf x}$ (to the right)  
- $\vec B$ along $-\hat{\mathbf z}$ (into page)

Then

$$
\mathbf u\times\mathbf B
= \hat{\mathbf x}\times(-\hat{\mathbf z})
= -(\hat{\mathbf x}\times\hat{\mathbf z})
= -(-\hat{\mathbf y})
= +\hat{\mathbf y},
$$

which is **upward**.

✅ **Answer:** $\boxed{\text{Path 1}}$ (deflection upward)

🧩 **Interpretation**

A positive charge curves in the direction given by the usual right-hand rule.  
A negative charge would follow the opposite (downward) path.
> [!code]- MATLAB — Lorentz force direction & radius (reusable)
> How to use: Set `q_C`, `u_vec`, and `B_vec` for your case.  
> - The script prints the Lorentz force vector and its direction.  
> - If you also give the particle mass `m_kg` and `u_vec ⟂ B_vec`, it computes the circular orbit radius.
> ```matlab
> %% HA3 – Section 4, Q8
> % Direction of motion of a charged particle in a magnetic field
> % F = q * (u x B)
> 
> % ---- INPUTS (edit for new problems) ----
> q_C   = +1;                  % charge [C] (sign matters for direction)
> u_vec = [1, 0, 0];           % velocity vector [m/s] (here: +x direction)
> B_vec = [0, 0, -1];          % magnetic flux density [T] (here: into page = -z)
> m_kg  = [];                  % particle mass [kg], optional (leave [] if unknown)
> 
> % ---- CORE CALCULATION ----
> u_vec = u_vec(:).';          % ensure row vector
> B_vec = B_vec(:).';
> 
> F_vec = q_C * cross(u_vec, B_vec);   % Lorentz force [N] (up to scaling if u,B normalized)
> 
> % Unit direction (if non-zero)
> if norm(F_vec) > 0
>     F_hat = F_vec / norm(F_vec);
> else
>     F_hat = [NaN, NaN, NaN];
> end
> 
> fprintf('u   = [%g  %g  %g]\n', u_vec);
> fprintf('B   = [%g  %g  %g]\n', B_vec);
> fprintf('F   = q (u x B) = [%g  %g  %g]  [N (up to scaling)]\n', F_vec);
> fprintf('F-hat direction = [%g  %g  %g]\n', F_hat);
> 
> % ---- OPTIONAL: circular-motion radius if u ⟂ B and mass known ----
> if ~isempty(m_kg)
>     u_mag = norm(u_vec);
>     B_mag = norm(B_vec);
>     if u_mag > 0 && B_mag > 0
>         R_orbit = m_kg * u_mag / (abs(q_C) * B_mag);  % [m]
>         fprintf('Assuming u ⟂ B: orbit radius R = %.3g m\n', R_orbit);
>     end
> end
> 
> % For the HA3 Q8 setup:
> %   q > 0, u = +x, B = -z → F points along +y (upward) → Path 1.
> ```


---
## Section 3 — Capacitors & Square Loop Field (Q5–Q6–Q9)

> [!summary] **Question 9 — $\lvert\vec H\rvert$ at the center of a square current loop (via Biot–Savart)**
>
> A square loop of wire with side length $\ell = 4.2~\text{mm}$ carries a current $I = 2.69~\text{mA}$.  
> It is in a magnetic medium with $\mu_r = 5$.  
> **Find** the magnitude of the magnetic field intensity $\lvert\vec H\rvert$ at the center, in $\text{A/m}$.

💡 **Concept (Biot–Savart for a finite straight segment)**

Biot–Savart’s law for **magnetic flux density** is

$$
\mathrm d\vec B
= \frac{\mu_0}{4\pi}\frac{I\,\mathrm d\vec\ell\times\hat{\mathbf R}}{R^2}.
$$

For a **straight finite wire** carrying current $I$, the magnitude of the **magnetic field intensity** due to that segment at a point a perpendicular distance $R$ away is

$$
H_{\text{seg}}
= \frac{I}{4\pi R}\bigl(\sin\theta_1 + \sin\theta_2\bigr),
$$

where:

- $R$ is the perpendicular distance from the point to the wire,
- $\theta_1$ and $\theta_2$ are the angles from the perpendicular line to each end of the wire,
- $\vec B = \mu_0\vec H$ in free space (or more generally $\vec B = \mu\vec H$).

For a **closed current loop**, the total $\vec H$ at a point is the vector sum of the contributions from all segments.

---

🧮 **Biot–Savart derivation for the square loop**

We place the square loop symmetrically around the origin and look at the field at the center.

- Side length: $\ell$  
- Distance from center to each side:
  $$
  a = \frac{\ell}{2}.
  $$

Consider **one side** of the square:

- The observation point (center) is at perpendicular distance $R = a$ from that side.
- The wire runs symmetrically about the perpendicular, so the angles to each end are equal:
  $$
  \theta_1 = \theta_2 = \theta.
  $$

Geometry to find $\theta$:

- Half of the side length is $\ell/2$, and the perpendicular distance is $a = \ell/2$.  
- So
  $$
  \tan\theta = \frac{\ell/2}{a} = \frac{\ell/2}{\ell/2} = 1
  \Rightarrow \theta = 45^\circ.
  $$
- Hence
  $$
  \sin\theta = \sin 45^\circ = \frac{1}{\sqrt{2}}.
  $$

Now use the **finite-wire Biot–Savart result** for $\vec H$:

1. One side:
   $$
   H_{\text{side}}
   = \frac{I}{4\pi a}\bigl(\sin\theta + \sin\theta\bigr)
   = \frac{I}{4\pi a}\bigl(2\sin\theta\bigr)
   = \frac{I}{2\pi a}\sin\theta.
   $$

   Insert $a = \ell/2$ and $\sin\theta = 1/\sqrt{2}$:

   $$
   H_{\text{side}}
   = \frac{I}{2\pi(\ell/2)}\cdot\frac{1}{\sqrt{2}}
   = \frac{I}{\pi\ell}\cdot\frac{1}{\sqrt{2}}.
   $$

2. Total field from all four sides:

   Each side gives the **same magnitude and direction** at the center (by symmetry), so

   $$
   H_{\text{tot}}
   = 4H_{\text{side}}
   = 4\left(\frac{I}{\pi\ell}\cdot\frac{1}{\sqrt{2}}\right)
   = \frac{4}{\sqrt{2}}\cdot\frac{I}{\pi\ell}
   = \frac{2\sqrt{2}I}{\pi\ell}.
   $$

   This is exactly the compact formula we used earlier, but now derived directly from **Biot–Savart**.

---

🔢 **Numeric evaluation**

Convert to SI:

- $\ell = 4.2~\text{mm} = 4.2\times 10^{-3}~\text{m}$  
- $I = 2.69~\text{mA} = 2.69\times 10^{-3}~\text{A}$

Then

$$
H
= \frac{2\sqrt{2}I}{\pi\ell}
= \frac{2\sqrt{2}\cdot 2.69\times 10^{-3}}{\pi\cdot 4.2\times 10^{-3}}
\approx 0.577~\text{A/m}.
$$

✅ **Answer:** $\boxed{|\vec H| \approx 0.577~\text{A/m}}$

🧩 **Interpretation**

- The result is **independent of $\mu_r$** because Biot–Savart on $\vec H$ depends only on the **free current geometry**.  
- The medium’s $\mu_r$ only changes $\vec B$ via $\vec B = \mu\vec H$:
  $$
  \vec B = \mu_0\mu_r\vec H.
  $$

---

> [!code]- MATLAB — Square current loop field at center (Biot–Savart-based formula)
> How to use: Set `ell_mm`, `I_mA`, and (optionally) `mu_r`.  
> The closed form used here comes from integrating Biot–Savart for each straight segment and summing the four sides.
> ```matlab
> %% HA3 – Section 7, Q9
> % |H| at the center of a square current loop
> % Biot–Savart result for each straight side:
> %   H_side = I/(4πR) * (sinθ1 + sinθ2)
> % For a square at its center: R = ℓ/2, θ1 = θ2 = 45°
> % → H_side = I/(πℓ) * 1/√2
> % Total from 4 sides:
> %   H_center = 4 * H_side = (2*sqrt(2)*I) / (pi*ell)
> %
> % where:
> %   I   = current [A]
> %   ell = side length [m]
> 
> % ---- INPUTS (edit for new problems) ----
> ell_mm = 4.2;       % side length ℓ [mm]
> I_mA   = 2.69;      % current I [mA]
> mu_r   = 5;         % relative permeability of medium (only affects B, not H)
> 
> % ---- CONSTANTS ----
> mu0 = 4*pi*1e-7;    % [H/m] vacuum permeability
> 
> % ---- UNIT CONVERSIONS ----
> ell = ell_mm * 1e-3;    % [m]
> I   = I_mA   * 1e-3;    % [A]
> 
> % ---- CORE CALCULATION (Biot–Savart closed form) ----
> H_center = (2*sqrt(2)*I) / (pi*ell);   % [A/m]
> B_center = mu0 * mu_r * H_center;      % [T] (optional)
> 
> % ---- OUTPUT ----
> fprintf('Square side ℓ = %.2f mm, current I = %.2f mA\n', ell_mm, I_mA);
> fprintf('|H_center| = %.3f A/m\n', H_center);
> fprintf('|B_center| = %.3e T  (for μ_r = %.2f)\n', B_center, mu_r);
> 
> % For the HA3 numbers:
> %   ℓ = 4.2 mm, I = 2.69 mA → |H_center| ≈ 0.577 A/m ≈ 0.58 A/m
> ```

---

## Section 5 — Inductors (Q10–Q11)

> [!summary] **Question 10 — Inductance of a toroidal inductor**
>
> A toroidal inductor with rectangular cross-section has:
> - Height: $h = 4.4~\text{mm}$  
> - Inner radius: $a = 8~\text{mm}$  
> - Outer radius: $b = 12~\text{mm}$  
> - Windings: $N = 56$  
> - Core relative permeability: $\mu_r = 130$  
>
> **Find** its inductance $L$ in $\mu\text{H}$.

💡 **Concept**

Approximate the toroid using:

- Cross-section area: $A \approx h(b-a)$  
- Mean radius: $r_m = (a+b)/2$  
- Magnetic path length: $\ell_m \approx 2\pi r_m$  
- Permeability: $\mu = \mu_0\mu_r$

Inductance:

$$
L = \frac{\mu N^2 A}{\ell_m}.
$$

🧮 **Derivation**

Convert to meters:

- $h = 4.4\times 10^{-3}~\text{m}$  
- $a = 8\times 10^{-3}~\text{m}$  
- $b = 12\times 10^{-3}~\text{m}$  

Area:

$$
A = h(b-a)
  = 4.4\times10^{-3}\cdot 4\times10^{-3}
  = 1.76\times 10^{-5}~\text{m}^2.
$$

Mean path length:

$$
r_m = \frac{a+b}{2} = 10\times10^{-3}~\text{m},\quad
\ell_m = 2\pi r_m \approx 6.283\times10^{-2}~\text{m}.
$$

Permeability:

$$
\mu = \mu_0\mu_r
    = (4\pi\times10^{-7})\cdot 130.
$$

Inductance:

$$
L = \frac{\mu N^2 A}{\ell_m}
  \approx 1.44\times 10^{-4}~\text{H}
  = 143.5~\mu\text{H}.
$$

✅ **Answer:** $\boxed{L \approx 143.5~\mu\text{H}}$

> [!code]- MATLAB — Toroidal inductor inductance (reusable)
> How to use: Set `h_mm`, `a_mm`, `b_mm`, `N`, and `mu_r` for your core.  
> Run the cell to get $L$ in henry and in $\mu$H.
> ```matlab
> %% HA3 – Section 5, Q10
> % Inductance of a toroidal inductor with rectangular cross-section
> %   L = μ * N^2 * A / ℓ_m
> % where:
> %   A   = h * (b - a)
> %   ℓ_m ≈ 2π * r_m,   r_m = (a + b)/2
> 
> % ---- INPUTS (edit for new problems) ----
> h_mm = 4.4;      % core height [mm]
> a_mm = 8.0;      % inner radius [mm]
> b_mm = 12.0;     % outer radius [mm]
> N    = 56;       % number of turns
> mu_r = 130;      % relative permeability of core
> 
> % ---- CONSTANTS ----
> mu0 = 4*pi*1e-7;         % [H/m]
> 
> % ---- UNIT CONVERSIONS ----
> h = h_mm * 1e-3;         % [m]
> a = a_mm * 1e-3;         % [m]
> b = b_mm * 1e-3;         % [m]
> 
> % ---- GEOMETRY ----
> A    = h * (b - a);              % cross-section area [m^2]
> rm   = 0.5 * (a + b);            % mean radius [m]
> ellm = 2*pi*rm;                  % magnetic path length [m]
> 
> % ---- PERMEABILITY ----
> mu = mu0 * mu_r;                 % [H/m]
> 
> % ---- INDUCTANCE ----
> L_H   = mu * N^2 * A / ellm;     % [H]
> L_uH  = L_H * 1e6;               % [µH]
> 
> fprintf('Toroid geometry: h = %.2f mm, a = %.2f mm, b = %.2f mm\n', ...
>         h_mm, a_mm, b_mm);
> fprintf('Cross-section area A = %.3e m^2\n', A);
> fprintf('Mean path length ℓ_m = %.3e m\n', ellm);
> fprintf('Inductance L = %.3e H  (%.1f µH)\n', L_H, L_uH);
> 
> % For the HA3 numbers: L ≈ 1.44e-4 H ≈ 144 µH
> ```

---

> [!summary] **Question 11 — Number of turns for a solenoid on a ferrite rod**
>
> You want an inductor with inductance $L = 584~\mu\text{H}$.  
> - Ferrite rod: diameter $d_f = 5.0~\text{mm}$, $\mu_r = 200$  
> - Copper wire: diameter $d_w = 0.2~\text{mm}$  
> - One **single layer** of windings (turns tightly side-by-side)  
>
> **Find** the number of turns $N$ (round up to nearest integer).

💡 **Concept**

- Cross-section area of the rod:
  $$
  A = \pi\left(\frac{d_f}{2}\right)^2.
  $$
- For a single layer, coil length is approximately
  $$
  \ell \approx N d_w.
  $$
- Solenoid inductance:
  $$
  L = \frac{\mu N^2 A}{\ell} = \frac{\mu N^2 A}{N d_w}
    = \frac{\mu N A}{d_w}
    \Rightarrow
    N = \frac{L d_w}{\mu A}.
  $$

🧮 **Derivation**

Convert units:

- $d_f = 5.0\times 10^{-3}~\text{m}$  
- $d_w = 0.2\times 10^{-3}~\text{m}$  
- $L = 584\times 10^{-6}~\text{H}$  

Area:

$$
A = \pi\left(\frac{d_f}{2}\right)^2
  = \pi(2.5\times10^{-3})^2
  \approx 1.96\times10^{-5}~\text{m}^2.
$$

Permeability:

$$
\mu = \mu_0\mu_r = (4\pi\times10^{-7})\cdot 200.
$$

Number of turns:

$$
N = \frac{L d_w}{\mu A}
  \approx 23.7.
$$

Round **up** to the nearest integer:

$$
N = 24~\text{turns}.
$$

✅ **Answer:** $\boxed{N = 24\ \text{turns}}$

🧩 **Interpretation**

With $N=24$ and $\ell\approx 24d_w$, the actual inductance comes out slightly above the target (about $592~\mu\text{H}$), which is acceptable given the rounding and core tolerances.
> [!code]- MATLAB — Solenoid turns on ferrite rod (single-layer, reusable)
> How to use: Set `L_uH`, `df_mm`, `dw_mm`, and `mu_r` for your rod + wire.  
> Run the cell to get the continuous-turn solution and the rounded-up integer, plus the actual inductance with that integer number of turns.
> ```matlab
> %% HA3 – Section 5, Q11
> % Number of turns for a single-layer solenoid on a ferrite rod
> %
> % Model:
> %   Rod diameter       = d_f
> %   Wire diameter      = d_w
> %   Single layer → coil length ℓ ≈ N * d_w
> %   Cross-section      A = π (d_f/2)^2
> %   μ = μ0 * μ_r
> %   L = μ N^2 A / ℓ = μ N A / d_w  →  N = L d_w / (μ A)
> 
> % ---- INPUTS (edit for new problems) ----
> L_uH  = 584;     % target inductance [µH]
> df_mm = 5.0;     % ferrite rod diameter [mm]
> dw_mm = 0.2;     % copper wire diameter [mm]
> mu_r  = 200;     % relative permeability of ferrite
> 
> % ---- CONSTANTS ----
> mu0 = 4*pi*1e-7;     % [H/m]
> 
> % ---- UNIT CONVERSIONS ----
> L   = L_uH * 1e-6;        % [H]
> df  = df_mm * 1e-3;       % [m]
> dw  = dw_mm * 1e-3;       % [m]
> mu  = mu0 * mu_r;         % [H/m]
> 
> % ---- GEOMETRY ----
> A = pi * (df/2)^2;        % cross-sectional area of rod [m^2]
> 
> % ---- CONTINUOUS NUMBER OF TURNS ----
> N_cont = L * dw / (mu * A);   % continuous solution
> N_int  = ceil(N_cont);        % round up to nearest integer
> 
> % ---- CHECK ACTUAL L FOR N_int ----
> % Using single-layer approximation ℓ ≈ N_int * d_w:
> L_actual = mu * N_int * A / dw;   % from L = μ N A / d_w
> 
> % ---- OUTPUT ----
> fprintf('Target inductance L_target = %.1f µH\n', L_uH);
> fprintf('Rod diameter d_f = %.1f mm, wire diameter d_w = %.3f mm\n', ...
>         df_mm, dw_mm);
> fprintf('Relative permeability μ_r = %.1f\n', mu_r);
> 
> fprintf('\nContinuous solution  N = %.3f turns\n', N_cont);
> fprintf('Rounded up integer   N = %d turns\n', N_int);
> fprintf('Resulting L(N_int)   = %.1f µH\n', L_actual*1e6);
> 
> % For the HA3 numbers:
> %   N_cont ≈ 23.7 → N_int = 24 turns
> %   L_actual ≈ 592 µH (slightly above 584 µH, which is fine in practice)
> ```

---

Recent in same folder

```dataview
LIST
FROM "Courses/Electromagnetics"
WHERE file.folder = this.file.folder AND file.path != this.file.path
SORT file.mtime desc
LIMIT 5
```
