---
title: Electrostatics II — Quick Formula Sheet
type: formula
tags: [Electromagnetics, Electrostatics, Conductors, Dielectrics, GaussLaw]
aliases: [Electrostatics II, Dielectrics, Conductors]
links: 
  - "[[MOC – Electromagnetics]]"
  - "[[MOC – Lectures]]"
  - "[[MOC – Exercises]]"
  - "[[Courses/Electromagnetics/Formulas/Electrostatics I — Quick Formula Sheet]]"
updated: 2025-11-12
---
---
title: Electrostatics II — Quick Formula Sheet
type: formula
tags: [Electromagnetics, Electrostatics, Conductors, Dielectrics, GaussLaw]
aliases: [Electrostatics II, Dielectrics, Conductors]
links: 
  - "[[MOC – Electromagnetics]]"
  - "[[MOC – Lectures]]"
  - "[[MOC – Exercises]]"
  - "[[Courses/Electromagnetics/Formulas/Electrostatics I — Quick Formula Sheet]]"
updated: 2025-11-12
---

> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Courses/Electromagnetics/Formulas/Electrostatics II — Quick Formula Sheet]]  
> **Quick refs:** [[Formulas/Electrostatics I — Quick Formula Sheet]] · [[MOC – Maxwell’s Equations]] · [[Formulas/Boundary Conditions — Quick Formula Sheet]]  
> For **30035 Engineering Electromagnetics – Fall 2025** (DTU Space, Rasmus E. Jacobsen).  
> Complete reference for **Electrostatics II** (Lecture 20 · 12 Nov 2025).  
> 📘 Textbook: *Ulaby & Ravaioli – Fundamentals of Applied Electromagnetics*, 8th Ed., Ch. 4-1 → 4-6.

---

## ⚙️ Conductors in Electrostatics (Ch. 4-1 → 4-2)

> [!note] **Physical meaning**
> - Conductors contain **free charges** that move under an applied field.  
> - At equilibrium, internal forces cancel → $\mathbf{E}=0$ inside.  
> - Excess charge accumulates **only on the surface**.

| Property | Mathematical form | Explanation |
|:--|:--|:--|
| **No internal field** | $\mathbf{E}=0$ | Charges move until field cancels |
| **No volume charge** | $\rho_v=0$ | All charge moves to surface |
| **Force balance** | $\mathbf{F}=q_k\mathbf{E}=0$ | Rest condition |
| **Surface field** | $E_n = \dfrac{\rho_s}{\varepsilon_0}$ | From Gauss’s law |
| **Tangential field** | $E_t = 0$ | Otherwise charges would move |
| **Potential** | $V=\text{const}$ | Conductor = equipotential |
| **Gauss surface (small patch)** | $\displaystyle \oint_{\Delta S} \mathbf{E}\cdot d\mathbf{s} = \frac{Q_s}{\varepsilon_0}$ | Defines $\rho_s$ on surface |
| **Field direction** | $\mathbf{E}\perp$ surface | Field lines orthogonal to surface |

> [!example] **Inside a conductor**
> $$
> \nabla \cdot \mathbf{E} = \frac{\rho_v}{\varepsilon_0} = 0, \qquad \mathbf{E} = 0
> $$  
> All charges reside on the outer surface where  
> $$
> \mathbf{E}_n = \frac{\rho_s}{\varepsilon_0}\hat{\mathbf{n}}
> $$

> [!tip]
> **Field enhancement:** $\rho_s$ grows near sharp edges or points (lightning-rod effect).

> [!summary] **Main conclusions**
> - $\mathbf{E}=0$ and $\rho_v=0$ inside the conductor.  
> - $\rho_s\neq0$ and $E_n\neq0$ on the surface.  
> - $\mathbf{E}_t=0$ and $\mathbf{E}\perp$ surface.  
> - $V=\text{const}$ throughout the conductor.  

---

## 🛡️ Electrostatic Shielding (Faraday Cage)

| Case | Field Region | Description |
|:--|:--|:--|
| **External charge near conductor** | $E_{\text{inside}}=0$ | Field lines terminate on induced surface charges. |
| **Charge inside isolated cavity** | $E_{\text{outside}}\neq0$ | Induced charges appear on inner and outer walls. |
| **Charge inside grounded cavity** | $E_{\text{outside}}=0$ | Ground fixes potential → perfect shielding. |

---

## 🧲 Dielectrics and Polarization (Ch. 4-3 → 4-6)

> [!note] **Bound vs Free charges**
> - *Free charges* move freely → conduction.  
> - *Bound charges* only shift slightly → polarization $\mathbf{P}$.  
> - $\mathbf{P}$ = dipole moment per unit volume [C/m²].

### Fundamental Relations

| Quantity | Equation | Description |
|:--|:--|:--|
| **Electric flux density** | $\mathbf{D} = \varepsilon_0\mathbf{E} + \mathbf{P}$ | Total flux incl. polarization |
| **Polarization field** | $\mathbf{P} = \varepsilon_0 \chi_e \mathbf{E}$ | Linear relation (simple dielectric) |
| **Constitutive relation** | $\mathbf{D} = \varepsilon_0(1+\chi_e)\mathbf{E} = \varepsilon\mathbf{E}$ | General form |
| **Permittivity** | $\varepsilon = \varepsilon_0(1+\chi_e) = \varepsilon_0 \varepsilon_r$ | Absolute permittivity |
| **Relative permittivity** | $\varepsilon_r = 1+\chi_e$ | Dimensionless |
| **Gauss (differential)** | $\nabla\cdot\mathbf{D} = \rho_v$ | Free charge density only |
| **Gauss (integral)** | $\displaystyle \oint_S\mathbf{D}\cdot d\mathbf{s} = Q_{\text{free}}$ | Flux form |
| **Simple medium** | $\mathbf{D}=\varepsilon\mathbf{E}$ | Linear isotropic homogeneous |
| **General medium** | $P_i = \varepsilon_0\sum_j \chi_{ij}E_j$ | Anisotropic case |

---

### 💡 Polarization Mechanisms

| Mechanism | Description | Example |
|:--|:--|:--|
| Electronic | Electron cloud shift | All materials |
| Ionic | Ion displacement | NaCl crystal |
| Orientational | Dipole rotation | Water molecules |
| Interfacial | Surface charge separation | Heterogeneous materials |


---
## 🧮 Electric Susceptibility

> [!info] **Defines how easily a medium polarizes under an electric field**

### 🧠 General Material
$$
\begin{bmatrix}
P_x(\mathbf{R}) \\ P_y(\mathbf{R}) \\ P_z(\mathbf{R})
\end{bmatrix}
=
\varepsilon_0
\begin{bmatrix}
\chi_{xx} & \chi_{xy} & \chi_{xz} \\
\chi_{yx} & \chi_{yy} & \chi_{yz} \\
\chi_{zx} & \chi_{zy} & \chi_{zz}
\end{bmatrix}
\begin{bmatrix}
E_x(\mathbf{R}) \\ E_y(\mathbf{R}) \\ E_z(\mathbf{R})
\end{bmatrix}
$$

$\boldsymbol{\chi} = \boldsymbol{\chi}(\mathbf{R}, \mathbf{E})$ — the **electric susceptibility tensor**.

A **general material** is:
- **anisotropic:** $\mathbf{P}$ not parallel to $\mathbf{E}$  
- **non-linear:** $\chi_{ij}$ depends on $\mathbf{E}$  
- **inhomogeneous:** $\chi_{ij}$ varies with position  

$$
\boldsymbol{\chi} = \boldsymbol{\chi}(\mathbf{R}, \mathbf{E}, f, T)
$$

---

### 💎 Simple Material
$$
\mathbf{P}(\mathbf{R}) = \varepsilon_0 \chi_e \mathbf{E}(\mathbf{R})
$$

Where $\chi_e$ is constant.

A **simple material** is:
- **isotropic:** $\mathbf{P}\parallel\mathbf{E}$  
- **linear:** $\chi_e$ independent of $\mathbf{E}$  
- **homogeneous:** $\chi_e$ independent of position  


---

### 🧭 Reformulated Gauss’s Law

$$
\nabla\!\cdot\!\mathbf{D} = \rho_{v,\text{free}}, \qquad 
\oint_S\mathbf{D}\cdot d\mathbf{s} = Q_{\text{free}}
$$

$$
\mathbf{D} = \varepsilon_0\mathbf{E} + \mathbf{P}
\Rightarrow
\mathbf{E} = \frac{\mathbf{D}}{\varepsilon}
$$

---

## 🧮 Example — Dielectric Sphere with a Free Charge

> [!summary] **Context**
> A spherical region filled with a **homogeneous dielectric material** of permittivity $\varepsilon$ contains a **free point charge** $Q_{\text{free}}$ at its center.  
> We want to find the **electric displacement field** $\mathbf{D}$ and **electric field** $\mathbf{E}$.

---

### ⚡ Step 1 — Choose the Correct Gauss’s Law Form

In a **dielectric**, it’s easier to work with the $\mathbf{D}$-field since it only accounts for **free charge**:
$$
\oint_S \mathbf{D} \cdot d\mathbf{s} = Q_{\text{free}}
$$

If we instead use $\mathbf{E}$, the equation would include **bound charges**:
$$
\oint_S \mathbf{E} \cdot d\mathbf{s} = \frac{Q_{\text{tot}}}{\varepsilon_0}
$$
where $Q_{\text{tot}} = Q_{\text{free}} + Q_{\text{bound}}$ (often unknown).

> 💡 Using $\mathbf{D}$ avoids the need to know the bound charge distribution.

---

### 🧭 Step 2 — Apply Spherical Symmetry

The system is spherically symmetric →  
$\mathbf{D}$ points radially outward, so we write:
$$
\mathbf{D} = \hat{\mathbf{R}} D_R(R)
$$

The Gaussian surface $S$ is a sphere of radius $R$ centered on the charge.

---

### 🧩 Step 3 — Integrate Over the Gaussian Surface

$$
\oint_S \mathbf{D} \cdot d\mathbf{s}
= D_R(R) \oint_S \hat{\mathbf{R}} \cdot d\mathbf{s}
= D_R(R) \int_0^{2\pi} \!\! \int_0^{\pi} R^2 \sin\theta \, d\theta \, d\phi
= D_R(R) \, 4\pi R^2
$$

Set equal to $Q_{\text{free}}$:

$$
D_R(R) \, 4\pi R^2 = Q_{\text{free}}
\quad \Rightarrow \quad
D_R(R) = \frac{Q_{\text{free}}}{4\pi R^2}
$$

---

### 🧲 Step 4 — Relate $\mathbf{E}$ to $\mathbf{D}$

Using $\mathbf{D} = \varepsilon \mathbf{E}$ (valid for simple linear dielectrics):

$$
\mathbf{E} = \frac{\mathbf{D}}{\varepsilon}
= \hat{\mathbf{R}} \frac{Q_{\text{free}}}{4\pi \varepsilon R^2}
$$

This looks identical to the **Coulomb field**, except $\varepsilon_0$ is replaced by $\varepsilon$.

---

### 📊 Step 5 — Interpret Physically

| Quantity | Symbol | Expression | Notes |
|:--|:--|:--|:--|
| Displacement field | $\mathbf{D}$ | $\displaystyle \hat{\mathbf{R}} \frac{Q_{\text{free}}}{4\pi R^2}$ | Depends only on free charge |
| Electric field | $\mathbf{E}$ | $\displaystyle \hat{\mathbf{R}} \frac{Q_{\text{free}}}{4\pi \varepsilon R^2}$ | Reduced in dielectric |
| Relation | $\mathbf{E} = \dfrac{\mathbf{D}}{\varepsilon}$ | Linear isotropic medium |
| Flux | $\displaystyle \oint_S \mathbf{D}\cdot d\mathbf{s}=Q_{\text{free}}$ | Independent of $\varepsilon$ |

---

> [!tip]
> The dielectric **reduces** the field strength by a factor of $\varepsilon_r$:
> $$
> E_{\text{dielectric}} = \frac{E_{\text{vacuum}}}{\varepsilon_r}
> $$

---

> [!example]
> For vacuum: $\varepsilon = \varepsilon_0$ → same form,  
> $\displaystyle \mathbf{E} = \hat{\mathbf{R}} \frac{Q_{\text{free}}}{4\pi \varepsilon_0 R^2}$  
>  
> For dielectric: replace $\varepsilon_0$ with $\varepsilon$,  
> $\displaystyle \mathbf{E} = \hat{\mathbf{R}} \frac{Q_{\text{free}}}{4\pi \varepsilon R^2}$

---

> [!summary]
> **Result:**  
> The $\mathbf{D}$-field behaves exactly as if the space were vacuum,  
> while the $\mathbf{E}$-field is reduced by the material permittivity.  
> The dielectric constant simply scales the field strength.

---

## 🧩 Summary Table — Electrostatics II Key Formulas

| Concept | Formula | Context |
|:--|:--|:--|
| **Coulomb Force** | $\mathbf{F}=\dfrac{q_1q_2}{4\pi\varepsilon R^2}\hat{\mathbf{R}}$ | Replace $\varepsilon_0→\varepsilon$ in dielectrics |
| **Polarization density** | $\mathbf{P}=\varepsilon_0\chi_e\mathbf{E}$ | Linear isotropic dielectric |
| **Flux density** | $\mathbf{D}=\varepsilon_0\mathbf{E}+\mathbf{P}=\varepsilon\mathbf{E}$ | Definition of $\mathbf{D}$ |
| **Relative permittivity** | $\varepsilon_r=1+\chi_e$ | Dimensionless ratio |
| **Gauss law for $\mathbf{D}$** | $\displaystyle \oint_S\mathbf{D}\cdot d\mathbf{s}=Q_{\text{free}}$ | Free charge only |
| **Dielectric strength** | $|E|_{\max}=E_{\text{ds}}$ | Breakdown threshold |
| **Equipotential surface (conductor)** | $V=\text{const},\ E_t=0,\ E_n=\rho_s/\varepsilon_0$ | Static equilibrium |
| **Field continuity (bdry)** | $E_{1t}=E_{2t},\ D_{1n}-D_{2n}=\rho_s$ | Boundary conditions |

---

**Key Sources & Citations:**  
- Lecture 20 Slides – Rasmus E. Jacobsen, DTU Space (2025-11-12)  
- *Ulaby & Ravaioli*, *Fundamentals of Applied Electromagnetics*, 8th Ed., Ch. 4-1 → 4-6  
- DTU 30035 Summary Slides – Electrostatics II 
