---
title: Operator Forms (Cartesian–Cylindrical–Spherical)
type: formula
tags: [electromagnetics, formula, vector-operators]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05
---
## 📊 Differential Operator Forms in Common Coordinate Systems

The following tables summarize the mathematical forms of the **gradient**, **divergence**, and **curl** operators for the three most used coordinate systems in electromagnetics.

---

### 🧱 Cartesian Coordinates $(x, y, z)$

| Operator | Expression |
|:--|:--|
| **Gradient** | $\displaystyle \nabla V = \hat{\mathbf x}\frac{\partial V}{\partial x} + \hat{\mathbf y}\frac{\partial V}{\partial y} + \hat{\mathbf z}\frac{\partial V}{\partial z}$ |
| **Divergence** | $\displaystyle \nabla\!\cdot\!\mathbf A = \frac{\partial A_x}{\partial x} + \frac{\partial A_y}{\partial y} + \frac{\partial A_z}{\partial z}$ |
| **Curl** | $\displaystyle \nabla\!\times\!\mathbf A = \begin{vmatrix} \hat{\mathbf x} & \hat{\mathbf y} & \hat{\mathbf z} \\[2pt] \frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\[2pt] A_x & A_y & A_z \end{vmatrix}$ <br> **Expanded:** $\displaystyle \nabla\!\times\!\mathbf A = \hat{\mathbf x}\!\left(\frac{\partial A_z}{\partial y}-\frac{\partial A_y}{\partial z}\right) + \hat{\mathbf y}\!\left(\frac{\partial A_x}{\partial z}-\frac{\partial A_z}{\partial x}\right) + \hat{\mathbf z}\!\left(\frac{\partial A_y}{\partial x}-\frac{\partial A_x}{\partial y}\right)$ |

> **Use:** Ideal for rectangular geometries — parallel plates, cubical volumes, or uniform Cartesian fields.

---

### 🌀 Cylindrical Coordinates $(r, \phi, z)$

| Operator | Expression |
|:--|:--|
| **Gradient** | $\displaystyle \nabla V = \hat{\mathbf r}\frac{\partial V}{\partial r} + \hat{\boldsymbol\phi}\frac{1}{r}\frac{\partial V}{\partial \phi} + \hat{\mathbf z}\frac{\partial V}{\partial z}$ |
| **Divergence** | $\displaystyle \nabla\!\cdot\!\mathbf A = \frac{1}{r}\frac{\partial (r A_r)}{\partial r} + \frac{1}{r}\frac{\partial A_\phi}{\partial \phi} + \frac{\partial A_z}{\partial z}$ |
| **Curl** | $\displaystyle \nabla\!\times\!\mathbf A = \begin{vmatrix} \hat{\mathbf r} & \hat{\boldsymbol\phi} & \hat{\mathbf z} \\[2pt] \frac{\partial}{\partial r} & \frac{1}{r}\frac{\partial}{\partial \phi} & \frac{\partial}{\partial z} \\[2pt] A_r & A_\phi & A_z \end{vmatrix}$ <br> **Expanded:** $\displaystyle \nabla\!\times\!\mathbf A = \hat{\mathbf r}\!\left(\frac{1}{r}\frac{\partial A_z}{\partial \phi} - \frac{\partial A_\phi}{\partial z}\right) + \hat{\boldsymbol\phi}\!\left(\frac{\partial A_r}{\partial z} - \frac{\partial A_z}{\partial r}\right) + \hat{\mathbf z}\!\frac{1}{r}\!\left[\frac{\partial}{\partial r}(rA_\phi) - \frac{\partial A_r}{\partial \phi}\right]$ |

> **Use:** Perfect for problems with **axial symmetry** (long wires, coaxial lines, solenoids).  
> Note the $1/r$ factors — they appear because $\phi$ is an angle, not a length.

---

### 🌍 Spherical Coordinates $(R, \theta, \phi)$

| Operator | Expression |
|:--|:--|
| **Gradient** | $\displaystyle \nabla V = \hat{\mathbf R}\frac{\partial V}{\partial R} + \hat{\boldsymbol\theta}\frac{1}{R}\frac{\partial V}{\partial \theta} + \hat{\boldsymbol\phi}\frac{1}{R\sin\theta}\frac{\partial V}{\partial \phi}$ |
| **Divergence** | $\displaystyle \nabla\!\cdot\!\mathbf A = \frac{1}{R^2}\frac{\partial (R^2 A_R)}{\partial R} + \frac{1}{R\sin\theta}\frac{\partial (A_\theta\sin\theta)}{\partial \theta} + \frac{1}{R\sin\theta}\frac{\partial A_\phi}{\partial \phi}$ |
| **Curl** | $\displaystyle \nabla\!\times\!\mathbf A = \frac{1}{R\sin\theta}\begin{vmatrix} \hat{\mathbf R} & R\hat{\boldsymbol\theta} & R\sin\theta\,\hat{\boldsymbol\phi} \\[2pt] \frac{\partial}{\partial R} & \frac{\partial}{\partial \theta} & \frac{\partial}{\partial \phi} \\[2pt] A_R & R A_\theta & R\sin\theta\,A_\phi \end{vmatrix}$ <br> **Expanded:** $\displaystyle \nabla\!\times\!\mathbf A = \hat{\mathbf R}\frac{1}{R\sin\theta}\!\left[\frac{\partial}{\partial \theta}(A_\phi\sin\theta) - \frac{\partial A_\theta}{\partial \phi}\right] + \hat{\boldsymbol\theta}\frac{1}{R}\!\left[\frac{1}{\sin\theta}\frac{\partial A_R}{\partial \phi} - \frac{\partial (RA_\phi)}{\partial R}\right] + \hat{\boldsymbol\phi}\frac{1}{R}\!\left[\frac{\partial (R A_\theta)}{\partial R} - \frac{\partial A_R}{\partial \theta}\right]$ |

> **Use:** Suited for **radial or spherical symmetry** — point charges, spheres, and radiating fields.  
> The geometry introduces factors of $R$ and $\sin\theta$ because small changes in angles sweep curved surfaces.

---

### 🧠 Summary Insight

| Operator | Output | Physical interpretation (in electromagnetics) |
|:--|:--|:--|
| **$\nabla V$** | Vector | Points in direction of fastest change of potential → gives $\mathbf E$ field direction. |
| **$\nabla\!\cdot\!\mathbf A$** | Scalar | Measures how much field “spreads out” → relates to charge or current density. |
| **$\nabla\!\times\!\mathbf A$** | Vector | Measures how much field “circulates” → relates to induced or steady magnetic fields. |

> [!tip]
> **Shortcut to remember:**  
> - Use Cartesian for simple, rectangular problems.  
> - Use Cylindrical when symmetry is around an **axis**.  
> - Use Spherical when symmetry is around a **point**.

---

### 🔗 Connection to Maxwell’s Equations (Static Cases)

| Law | Differential Form | Integral Form | Field Type |
|:--|:--|:--|:--|
| **Gauss’s Law (E-field)** | $\nabla\!\cdot\!\mathbf D = \rho_v$ | $\displaystyle \oint_S \mathbf D\!\cdot\!d\mathbf s = Q_{\text{enc}}$ | Electrostatics |
| **Faraday’s Law (Static)** | $\nabla\!\times\!\mathbf E = 0$ | $\displaystyle \oint_C \mathbf E\!\cdot\!d\boldsymbol\ell = 0$ | Electrostatics |
| **Ampère’s Law (Static)** | $\nabla\!\times\!\mathbf H = \mathbf J$ | $\displaystyle \oint_C \mathbf H\!\cdot\!d\boldsymbol\ell = I_{\text{enc}}$ | Magnetostatics |
| **Gauss’s Law (B-field)** | $\nabla\!\cdot\!\mathbf B = 0$ | $\displaystyle \oint_S \mathbf B\!\cdot\!d\mathbf s = 0$ | Magnetostatics |

---

> [!summary]
> The operators **∇ (del), ∇·, and ∇×** translate spatial variation into physics:
> - **Gradient** → creates $\mathbf E$ from scalar potential.  
> - **Divergence** → quantifies charge or current sources.  
> - **Curl** → captures rotational or circulating behavior of fields.  
> Together, they form the **mathematical backbone of Maxwell's equations**.

> [!details]- 🔗 Related examples
> - [[Examples/Gradient Example (Potential)]]
> - [[Examples/Divergence Example (E-field)]]
> - [[Examples/Curl Example (B-field)]]
