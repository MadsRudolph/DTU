# Electromagnetics — EXAM PREPARATION MASTER NOTE  
*DTU 30035 — Engineering Electromagnetics (Bachelor level)*

This is your **central exam command center**:  
All topics → heatmap → attack plan → risk map.  
Use this page as the index for all other notes (Lectures, Exercises, Home Assignments, Exams, Maple/MATLAB helpers).

---


# 1) EM TOPIC MAP  
Full overview of everything examinable.

---

## A. Foundations — Maxwell & Math Tools (🟥)

- Maxwell’s equations (time domain + phasor form)  
- Constitutive relations:  
  $\mathbf D=\varepsilon\mathbf E,\ \mathbf B=\mu\mathbf H,\ \mathbf J=\sigma\mathbf E$
- Coordinate systems:
  - Cartesian / Cylindrical / Spherical  
  - Differential elements, Jacobians  
- Vector operators: $\nabla V$, $\nabla\cdot\mathbf A$, $\nabla\times\mathbf A$  
- Vector theorems: Gauss & Stokes  
- Interpretation of divergence, curl, gradient in field problems  

### Linked Exercises
- [[Exercise 18 — Coordinate Systems and Vector Operators]] — coordinate transforms (Cartesian ↔ cylindrical ↔ spherical) and full use of $\nabla$, $\nabla\cdot$, $\nabla\times$ in different coordinate systems (🟥 essential, math core for everything else)  
  - Tags: #math-heavy · #geometry-reasoning  

> Use this section as the **math backbone**: every EM exam problem can hide a coordinate/operator trap.

---

## B. Transmission Lines (TLs) (🟥)

- Travelling waves in 1D:  
  $y(z,t)=A_0 e^{-\alpha z}\cos(\omega t-\beta z-\phi_0)$, phasor $A_0 e^{-(\alpha+j\beta)z}$  
- Per-unit-length parameters: $R', L', G', C'$  
- Propagation constant: $\gamma = \alpha + j\beta$  
- Characteristic impedance: $Z_0=\sqrt{Z_s'/Y_p'}$  
- General TL solutions:  
  $\tilde V(z)=\tilde V^+e^{-\gamma z}+\tilde V^-e^{+\gamma z}$,  
  $\tilde I(z)=\frac{\tilde V^+}{Z_0}e^{-\gamma z}-\frac{\tilde V^-}{Z_0}e^{+\gamma z}$  
- Reflection at load:  
  $\Gamma_L=\dfrac{Z_L-Z_0}{Z_L+Z_0}$  
- Input impedance:  
  $Z_\text{in}(z)=Z_0\frac{Z_L+Z_0\tanh(\gamma z)}{Z_0+Z_L\tanh(\gamma z)}$ (general)  
  $Z_\text{in}=Z_0\dfrac{Z_L+jZ_0\tan\beta\ell}{Z_0+jZ_L\tan\beta\ell}$ (lossless)  
- Special lengths:  
  - $\ell=\lambda/2 \Rightarrow Z_\text{in}=Z_L$  
  - $\ell=\lambda/4 \Rightarrow Z_\text{in}=Z_0^2/Z_L$  
- Power on TL: $\bar P = \dfrac{1}{2}\Re\{\tilde V\tilde I^*\}$  

### Linked Exercises
- (To link when TL exercise markdowns are integrated, e.g. single-terminated TL, quarter-wave transformer, stub tuner problems.)

---

## C. Smith Chart & Matching (🟥)

- Normalized impedance: $z = Z/Z_0$  
- Mapping: $\Gamma = \dfrac{z-1}{z+1}$, $z = \dfrac{1+\Gamma}{1-\Gamma}$  
- Circles of constant resistance and reactance  
- Movement along line ↔ rotation along SWR circle  
  - Towards generator: clockwise on chart  
  - Towards load: counter-clockwise  
- VSWR: $\text{VSWR} = \dfrac{1+|\Gamma_L|}{1-|\Gamma_L|}$  
- Quarter-wave transformer: $Z_\text{qw}=\sqrt{Z_0 Z_L}$ (real load)  
- Single-stub and L-network matching (high-level recipes)  

### Linked Exercises
- (To link once your TL/Smith matching exercises and Home Assignment sections are imported as separate markdown.)

---

## D. Plane Waves & Power Flow (🟥)

- Wave equation (phasor form):  
  $$\nabla^2\mathbf E - \gamma^2 \mathbf E = 0$$
- Uniform plane-wave solution:  
  $\mathbf E(\mathbf r)=\mathbf E_0 e^{-\gamma\hat\beta\cdot\mathbf r}$,  
  $\mathbf H(\mathbf r)=\mathbf H_0 e^{-\gamma\hat\beta\cdot\mathbf r}$  
- Lossless medium:  
  - $\gamma=j\beta$, $\beta=\omega\sqrt{\mu\varepsilon}$  
  - Phase velocity $u_p = \omega/\beta$  
  - Intrinsic impedance $\eta=\sqrt{\mu/\varepsilon}$  
- Transverse conditions:  
  - $\hat\beta\cdot\mathbf E_0 = 0$  
  - $\hat\beta\cdot\mathbf H_0 = 0$  
  - $\hat\beta, \mathbf E_0, \mathbf H_0$ form a right-handed triad  
- E–H relations (time-harmonic):  
  $$\boldsymbol\gamma \times \tilde{\mathbf H}_0 = -j\omega\varepsilon\tilde{\mathbf E}_0,\quad
  \boldsymbol\gamma \times \tilde{\mathbf E}_0 = +j\omega\mu\tilde{\mathbf H}_0$$
- Poynting vector:  
  $$\mathbf S(\mathbf r,t) = \mathbf E\times\mathbf H,\quad
  \langle \mathbf S\rangle = \frac{1}{2}\Re\{\mathbf E\times\mathbf H^*\}$$
  In lossless uniform plane wave:  
  $$\langle S\rangle = \frac{|E_0|^2}{2\eta} = \frac{\eta|H_0|^2}{2}$$

### Linked Exercises
- [[Home Assignment 1]] — plane-wave verification with full $\boldsymbol\gamma\cdot\mathbf E = \boldsymbol\gamma\cdot\mathbf H = 0$ checks, $\boldsymbol\gamma\times\mathbf E$ / $\boldsymbol\gamma\times\mathbf H$ consistency, and Poynting vector + total power on tilted surfaces (🟥, derivation + computation)  
  - Tags: #math-heavy · #field-intuition  

---

## E. Reflection & Transmission (🟥)

- Boundary conditions (source-free simple media):  
  - Tangential $\mathbf E$: continuous  
  - Normal $\mathbf D$: jump given by $\rho_s^\text{free}$  
  - Tangential $\mathbf H$: continuous (unless surface current)  
  - Normal $\mathbf B$: continuous  
- Normal incidence (non-magnetic media, $\mu_1=\mu_2$):  
  $$\Gamma = \frac{\eta_2-\eta_1}{\eta_2+\eta_1},\quad
    t = \frac{2\eta_2}{\eta_2+\eta_1}$$
  $$R = |\Gamma|^2,\quad T = 1-R$$
- PEC limit: $\eta_2\to 0 \Rightarrow \Gamma=-1$, standing wave, no transmitted power  
- Oblique incidence:  
  - Snell: $n_1\sin\theta_i = n_2\sin\theta_t$  
  - TE ($E\perp$ plane of incidence) vs TM ($H\perp$ plane)  
  - Fresnel coefficients $r_\text{TE}$, $r_\text{TM}$, $t_\text{TE}$, $t_\text{TM}$  
  - Brewster angle (TM): $r_\text{TM}=0$  
  - Critical angle and total internal reflection (from higher to lower index)

### Linked Exercises
- [[Home Assignment 2]] — normal and oblique incidence at dielectric boundaries, TE/TM Fresnel coefficients, Brewster angle, and power conservation ($R + T = 1$) (🟥, boundary conditions + geometry)  
  - Tags: #math-heavy · #boundary-conditions · #geometry-reasoning  

> This section is the **interface glue**: link plane waves to real materials and power budgets.

---

## F. Electrostatics (🟥)

- Coulomb’s law (discrete & continuous)  
- Gauss’s Law:  
  $$\oint_S \mathbf E\cdot d\mathbf s = \frac{Q_\text{enc}}{\varepsilon_0}$$
- Electric potential:
  $$\mathbf E = -\nabla V,\quad V(\mathbf r)= -\int \mathbf E\cdot d\mathbf l$$
- Conductors in electrostatics:
  - $E=0$ inside conductor  
  - Excess charge on surface  
  - $\rho_s = \varepsilon_0 E_n$  
  - Conductors are equipotential surfaces  
- Dielectrics & $\mathbf D$-field:
  - $\mathbf D = \varepsilon \mathbf E$ (linear)  
  - $\nabla\cdot\mathbf D = \rho_\text{free}$  
  - Normal $D$: jump given by $\rho_s^\text{free}$  
  - Tangential $E$: continuous  
- Capacitors:
  - $C = Q/V$  
  - Parallel-plate, coaxial, spherical  
  - Series/parallel combinations  
- Dielectric strength & breakdown:
  - Max field $E_\text{max}$ before breakdown  
  - $V_\text{max} = E_\text{max} \cdot d_\text{effective}$  

### Linked Exercises
- [[Exercise 19 — Electrostatics]] — Coulomb force between point charges, total charge from non-uniform line/surface densities, field on the axis of a charged ring, and capacitance + breakdown comparison for parallel-plate vs spherical geometries (🟥, integral setup + units)  
  - Tags: #math-heavy · #geometry-reasoning · #field-intuition · #boundary-conditions  

- [[Home Assignment 3]] — uniformly charged sphere embedded in a dielectric (piecewise $E(r)$ inside/outside), work done in a uniform electric field for motion $\perp \mathbf E$, and link to magnetostatics via solenoid inductance problem (🟧, conceptual + computation)  
  - Tags: #math-heavy · #field-intuition  

---

## G. Magnetostatics (🟧)

- Lorentz force:
  $$\mathbf F_\text{em} = q(\mathbf E + \mathbf u\times\mathbf B)$$
- Steady currents, current density $\mathbf J$  
- Maxwell magnetostatics:
  $$\nabla\times\mathbf H = \mathbf J,\quad \nabla\cdot\mathbf B = 0$$
- Fields from wires and loops:
  - Infinite straight wire: $B_\phi = \mu_0 I /(2\pi\rho)$  
  - Finite wire, loop: Biot–Savart / vector potential approach  
- Solenoids:
  - Ideal long solenoid: $B_\text{inside} \approx \mu_0 n I$  
  - $B$ outside is very small due to cancellation  
- Inductance:
  $$L = \mu N^2 A / \ell$$
  and energy $W = \tfrac{1}{2}LI^2$

### Linked Exercises
- [[Exercise 20 - Magnetostatics]] — Lorentz force on moving charges ($q>0$ vs $q<0$), 3D cross-product reasoning in Cartesian and cylindrical coordinates, direction of $\mathbf B$ around a straight wire, and qualitative Ampère loop argument for solenoid field inside vs outside (🟥, geometry + field intuition)  
  - Tags: #geometry-reasoning · #field-intuition  

- [[Home Assignment 3]] — inductance and required turns for a solenoid on a ferrite rod using $L = \mu N^2 A/\ell$ with careful unit handling (🟧, algebra + units)  
  - Tags: #math-heavy · #geometry-reasoning  

---

# 2) EXAM HEATMAP  
Likelihood + importance per topic.

| Topic                       | Importance | Notes |
|----------------------------|-----------|-------|
| TLs & power on TLs         | 🟥        | Classic analytical problems (reflection, SWR, $Z_\text{in}$) |
| Smith chart + matching     | 🟥        | Often the “design” part: read/plot impedances, match a complex load |
| Plane waves & power        | 🟥        | Plane-wave checks, $\eta,\beta,\lambda,u_p$, Poynting vector |
| Reflection & transmission  | 🟥        | Normal incidence almost guaranteed; TE/TM often appears |
| Electrostatics core        | 🟥        | Gauss, conductors, capacitors, charge distributions |
| Magnetostatics basics      | 🟧        | Wires, solenoids, Lorentz force; often conceptual + 1–2 computations |
| Lossy media & skin depth   | 🟧        | Appears regularly as classification / short calc |
| TE/TM oblique details      | 🟧        | Usually one sub-question (Brewster / critical angle) |
| Full polarization analysis | 🟨        | Nice-to-have; may appear as a short theory Q |
| Advanced matching networks | 🟨        | Beyond quarter-wave / single-stub is less likely |

---

# 3) ATTACK PLAN (WEEK BEFORE EXAM)

## Day 1 — Foundations & Coordinates
- Rewrite: unit-vector transforms and differential elements for cylindrical/spherical.  
- Drill: 2–3 problems with grad/div/curl in non-Cartesian coordinates.  
- Goal: never hesitate when switching coordinates.

## Day 2 — TLs & Smith Chart
- TL core:
  - Derive reflection coefficient, $Z_\text{in}$ (lossless + lossy forms).  
  - Solve 3 example problems: open, short, complex load.  
- Smith chart:
  - Practice normalize → plot → rotate → denormalize.  
  - One full quarter-wave matching example.

## Day 3 — Plane Waves & Power
- From Maxwell to plane-wave equation once (no notes).  
- Plane wave tasks:
  - Given $\mathbf E_0$, $\boldsymbol\gamma$: check if valid, find $\mathbf H_0$, $\eta$, $\beta$, $\lambda$, $u_p$.  
- Redo [[Home Assignment 1]] completely on paper.  

## Day 4 — Reflection & Transmission
- Derive Fresnel coefficients at normal incidence from BCs.  
- Solve:
  - 2 normal-incidence problems (dielectric–dielectric, dielectric–PEC).  
  - 1 TE and 1 TM oblique problem including Brewster angle.  
- Redo key problems from [[Home Assignment 2]].

## Day 5 — Electrostatics
- Gauss law patterns:
  - Sphere, infinite cylinder, infinite plane.  
- Redo:
  - Charge-distribution integrals from [[Exercise 19 — Electrostatics]].  
  - Sphere-in-dielectric E-field from [[Home Assignment 3]].  
- Add: 1 capacitor + dielectric-strength problem.

## Day 6 — Magnetostatics
- Lorentz force:
  - Do 3 cross-product problems in different coordinates.  
- Ampère’s law:
  - B-field around wire, qualitative solenoid reasoning.  
- Redo [[Exercise 20 - Magnetostatics]] and inductance problem from [[Home Assignment 3]].  

## Day 7 — Full Mock + Condensed Review
- Sit one full past exam under timed conditions.  
- Mark where you lost time or points.  
- Build:
  - 1-page **formula sheet** (TL + plane waves + electrostatics).  
  - 1-page **tricks & mistakes** sheet (from section 5 below).

---

# 4) RISK LEVEL (HONEST ASSESSMENT)

## Strengths
- Good structure of notes (Home Assignments, Exercises well documented).  
- Comfortable with MATLAB/Maple-style numeric checks.  
- Intuitive feel for fields once vectors are set up correctly.

## Medium-Risk Areas
- Coordinate operator formulas (div/curl in cylindrical/spherical) under pressure.  
- Electrostatics integrals with non-uniform densities (dropping r-factors / 2π).  
- TE/TM formula selection and remembering power coefficients.  
- Unit conversions (mm, nm, fC, kV/mm, µH).

## High-Risk Under Time Pressure
- Cross-product directions for Lorentz force and plane-wave E/H relations.  
- Using correct RMS vs peak in power density formulas.  
- Keeping track of medium indices in Fresnel (who is 1, who is 2).  
- Applying Gauss law in wrong coordinate system or with wrong differential element.

## Overall
- **Conceptual risk: Low–Medium**  
- **Execution / speed risk: Medium–High** (especially vector math + units)  
- **Grade potential: High** if you enforce structured setups and unit checks.

---

# 5) 🔥 HIGH-RISK ERROR PATTERNS

From [[Exercise 18 — Coordinate Systems and Vector Operators]],  
[[Exercise 19 — Electrostatics]], [[Exercise 20 - Magnetostatics]],  
[[Home Assignment 1]], [[Home Assignment 2]], [[Home Assignment 3]]:

1. **Coordinate & operator slips**
   - Wrong Jacobian / missing metric factors in cylindrical/spherical divergence/curl.  
   - Treating components like coordinates when transforming (using $x = r\cos\phi$ directly on $A_x$).  

2. **Unit conversion mistakes**
   - Not converting mm, nm, fC, nC, kV/mm, µH to SI before using formulas.  
   - Mixing up V/m vs kV/mm in dielectric-strength problems.

3. **Plane-wave consistency**
   - Accepting $(\mathbf E_0, \mathbf H_0, \boldsymbol\gamma)$ triplets that violate $\boldsymbol\gamma\cdot\mathbf E_0=0$ or $\boldsymbol\gamma\cdot\mathbf H_0=0$.  
   - Sign errors in $\boldsymbol\gamma\times\mathbf E$ and $\boldsymbol\gamma\times\mathbf H$; forgetting the time convention.

4. **Power & RMS**
   - Plugging RMS magnitudes into formulas intended for peak (or vice versa).  
   - Forgetting to project onto surface normal ($\langle S_n\rangle = \langle S\rangle\cos\varphi$).

5. **Reflection & TE/TM confusion**
   - Using TM formulas when situation is TE, or mixing the definitions of TE/TM relative to plane of incidence.  
   - Forgetting $\cos\theta_t / \cos\theta_i$ in power transmission.

6. **Electrostatics integrals & breakdown**
   - Dropping a factor of r in $dS = r\,dr\,d\phi$.  
   - Treating $E_\text{max}$ as a voltage limit instead of a field limit.

7. **Magnetostatics geometry**
   - Computing $q(\mathbf B\times\mathbf u)$ instead of $q(\mathbf u\times\mathbf B)$.  
   - Wrong direction of $\mathbf B$ around wires on +x vs +y axis.  
   - Not using Ampère loops to argue $B_\text{outside}\approx 0$ for long solenoids.

---

# 6) MUST-REVISIT EXERCISES (HIGHEST EXAM VALUE)

Do these **on paper**, then compare with your existing solutions.

## Foundations & Coordinates
- [[Exercise 18 — Coordinate Systems and Vector Operators]]  
  - Redo at least:
    - One full coordinate transform chain (Cartesian → cylindrical → spherical and back).  
    - One gradient, one divergence, one curl in cylindrical/spherical **without** looking up formulas.

## Electrostatics
- [[Exercise 19 — Electrostatics]]  
  - Coulomb force problem with full vector directions and units.  
  - One complete non-uniform charge-distribution integral (disc or line).  
  - Capacitance + dielectric-strength comparison (parallel-plate vs spherical).

- [[Home Assignment 3]]  
  - Derive $E(r)$ inside and outside a uniformly charged dielectric sphere using Gauss.  
  - Work in uniform field for motion perpendicular to $\mathbf E$ (prove $W=0$ directly).  

## Plane Waves & Power
- [[Home Assignment 1]]  
  - Verify which proposals are valid plane waves using:
    - $\boldsymbol\gamma\cdot\mathbf E_0=0$, $\boldsymbol\gamma\cdot\mathbf H_0=0$  
    - $\boldsymbol\gamma\times\mathbf E_0$ and $\boldsymbol\gamma\times\mathbf H_0$ equations.  
  - Recompute power density and total power on tilted surfaces.

## Reflection & Transmission
- [[Home Assignment 2]]  
  - Redo normal-incidence cases from scratch (derive $\Gamma$, $R$, $T$).  
  - One TE and one TM oblique case including Brewster angle.  
  - Check $R+T=1$ for all lossless examples.

## Magnetostatics
- [[Exercise 20 - Magnetostatics]]  
  - All Lorentz-force subproblems with explicit cross-product calculations.  
  - Direction of $\mathbf B$ around wire using diagrams + right-hand rule.  
  - Qualitative Ampère argument for solenoid fields.

- [[Home Assignment 3]]  
  - Inductance/turns calculation for ferrite rod solenoid; pay attention to units and $\mu_r$.

---

# 7) Maple / MATLAB I MUST RERUN BEFORE EXAM

Reopen and re-execute your EM scripts / worksheets that support these topics, focusing on **understanding every step**:

- Script/worksheet for [[Home Assignment 1]] — plane waves & power (check vector operations and power integration).  
- Script/worksheet for [[Home Assignment 2]] — reflection/transmission plots vs angle or frequency.  
- Script/worksheet for [[Home Assignment 3]] — charged sphere E-field, plotting $E(r)$ inside/outside, and solenoid inductance checks.  
- Any TL/Smith chart helper scripts (when you have them) — verify implementations of $\Gamma$, $Z_\text{in}$, power, and mapping onto Smith chart.

Use this page as your **index** and navigation hub.  
From here jump to:

- `[[MOC – Electromagnetics]]`  
- `[[MOC – Lectures]]`  
- `[[Exercise 18 — Coordinate Systems and Vector Operators]]`  
- `[[Exercise 19 — Electrostatics]]`  
- `[[Exercise 20 - Magnetostatics]]`  
- `[[Home Assignment 1]]`, `[[Home Assignment 2]]`, `[[Home Assignment 3]]`  
- Any past exam solution notes you add later.

92486
