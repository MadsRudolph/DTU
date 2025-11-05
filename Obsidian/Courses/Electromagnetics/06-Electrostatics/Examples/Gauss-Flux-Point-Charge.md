---
title: "Gauss Flux Point Charge"
type: formula
tags: [electromagnetics, electrostatics, formula, examples]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05
updated: "2025-11-05"
---
## 🧮 Example — Gauss Flux of a Point Charge

> **Problem statement:**  
> An electric charge $Q$ at rest, placed in free space at $(x, y, z) = (0,0,0)$, creates an electrostatic field:
> $$
> \mathbf E = \hat{\mathbf R}\,\frac{Q}{4\pi\varepsilon_0 R^2},
> $$
> where $\varepsilon_0$ is the free-space permittivity and $R$ is the distance from the charge to the point of evaluation.  
> Show that the **total electric flux** of $\mathbf E$ through the surface enclosing the charge equals:
> $$
> \oint_S \mathbf E\cdot d\mathbf s = \frac{Q}{\varepsilon_0}.
> $$

---

### 🧭 Step 1 — Choose the coordinate system

Because the field $\mathbf E$ is **radial** and depends only on $R$, the **spherical coordinate system** is the natural choice.

For a sphere of radius $R_0$ centered at the origin:

- The field magnitude is constant:  
  $$
  E = \frac{Q}{4\pi\varepsilon_0 R_0^2}.
  $$
- The field direction $\hat{\mathbf R}$ is normal to the surface everywhere.  
- Hence $\mathbf E$ is **parallel to** $d\mathbf s$, and their dot product simplifies to $E\,dS$.

---

### 🧩 Step 2 — Differential surface element

## Differential elements in different coordinate systems

| **Type**                 | **Cartesian**                                                                                                                    | **Cylindrical**                                                                                                                                       | **Spherical**                                                                                                                                                                                         |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Differential length**  | $d\boldsymbol{\ell} = \hat{\mathbf x}\,dx + \hat{\mathbf y}\,dy + \hat{\mathbf z}\,dz$                                           | $d\boldsymbol{\ell} = \hat{\mathbf r}\,dr + \hat{\boldsymbol\phi}\,r\,d\phi + \hat{\mathbf z}\,dz$                                                    | $d\boldsymbol{\ell} = \hat{\mathbf R}\,dR + \hat{\boldsymbol\theta}\,R\,d\theta + \hat{\boldsymbol\phi}\,R\sin\theta\,d\phi$                                                                          |
| **Differential surface** | $d\mathbf s_x = \hat{\mathbf x}\,dy\,dz$<br>$d\mathbf s_y = \hat{\mathbf y}\,dz\,dx$<br>$d\mathbf s_z = \hat{\mathbf z}\,dx\,dy$ | $d\mathbf s_r = \hat{\mathbf r}\,r\,d\phi\,dz$<br>$d\mathbf s_\phi = \hat{\boldsymbol\phi}\,dr\,dz$<br>$d\mathbf s_z = \hat{\mathbf z}\,r\,dr\,d\phi$ | $d\mathbf s_R = \hat{\mathbf R}\,R^2\sin\theta\,d\theta\,d\phi$<br>$d\mathbf s_\theta = \hat{\boldsymbol\theta}\,R\sin\theta\,dR\,d\phi$<br>$d\mathbf s_\phi = \hat{\boldsymbol\phi}\,R\,dR\,d\theta$ |
| **Differential volume**  | $dV = dx\,dy\,dz$                                                                                                                | $dV = r\,dr\,d\phi\,dz$                                                                                                                               | $dV = R^2\sin\theta\,dR\,d\theta\,d\phi$                                                                                                                                                              |
For the **surface of a sphere**, $R = R_0$ is constant, so only the **radial** element contributes (the normal direction is $\hat{\mathbf R}$).  
Thus, the spherical differential surface element is:
$$
d\mathbf s = \hat{\mathbf R}\,R_0^2\sin\theta\,d\theta\,d\phi.
$$

> This represents a small patch on the sphere formed by two arcs:
> one of length $R_0\,d\theta$ (north–south) and another of length $R_0\sin\theta\,d\phi$ (east–west).  
> Their product gives the area $R_0^2\sin\theta\,d\theta\,d\phi$ oriented radially outward.

Substituting $\mathbf E$:
$$
\mathbf E\cdot d\mathbf s
= \left(\frac{Q}{4\pi\varepsilon_0 R_0^2}\right)
R_0^2\sin\theta\,d\theta\,d\phi.
$$

---

### 🧮 Step 3 — Compute the flux integral

Integrate over the full spherical surface:
$$
\begin{aligned}
\oint_S \mathbf E\cdot d\mathbf s
&= \int_{\phi=0}^{2\pi} \int_{\theta=0}^{\pi}
\frac{Q}{4\pi\varepsilon_0 R_0^2}\,
R_0^2\sin\theta \, d\theta\, d\phi \\[4pt]
&= \frac{Q}{4\pi\varepsilon_0}
\left( \int_{0}^{2\pi} d\phi \right)
\left( \int_{0}^{\pi} \sin\theta \, d\theta \right) \\[4pt]
&= \frac{Q}{4\pi\varepsilon_0} \cdot (2\pi)\cdot (2) \\[4pt]
&= \boxed{\frac{Q}{\varepsilon_0}}.
\end{aligned}
$$

---

### 💡 Step 4 — Interpret the result

- The **flux** through any closed surface enclosing the charge is independent of the radius $R_0$.  
- This verifies **Gauss’s law** for a point charge:
  $$
  \oint_S \mathbf D\cdot d\mathbf s = Q_{\text{enc}}, \qquad
  \mathbf D = \varepsilon_0 \mathbf E.
  $$
  Therefore:
  $$
  \oint_S \mathbf E\cdot d\mathbf s = \frac{Q_{\text{enc}}}{\varepsilon_0}.
  $$

---

### 🧠 Concept checks

- **Symmetry:** Spherical coordinates make $E$ constant on $S$, and $\mathbf E \parallel d\mathbf s$.  
- **Physical meaning:** The flux counts how many field lines leave the surface — each charge contributes $Q/\varepsilon_0$, regardless of the surface shape.  
- **Units:** $[\mathbf E]=\mathrm{V/m}$ and $[d\mathbf s]=\mathrm{m}^2\hat{n}$, so $\mathbf E\cdot d\mathbf s$ gives $\mathrm{V\cdot m}$; multiplying by $\varepsilon_0$ yields coulombs.

---

> [!summary]
> **Result:**  
> For a point charge $Q$ at the origin,
> $$
> \boxed{\displaystyle \oint_S \mathbf E\cdot d\mathbf s = \frac{Q}{\varepsilon_0}}.
> $$
> This holds for *any* closed surface enclosing the charge, not only for a sphere.

---