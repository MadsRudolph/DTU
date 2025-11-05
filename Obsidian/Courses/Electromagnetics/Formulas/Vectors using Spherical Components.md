---
title: Vectors using Spherical Components
type: formula
tags: [electromagnetics, formula, coordinate-systems, vector-operators]
aliases: []
links: {"formulas": [], "related": []}
updated: 2025-11-05
---
### 🧭 Vectors using Spherical Components

A vector can be expressed in both **Cartesian** and **spherical** components:

$$
\mathbf{A} =
\begin{pmatrix}
A_x \\ A_y \\ A_z
\end{pmatrix}
=
A_x\hat{x} + A_y\hat{y} + A_z\hat{z}
=
A_R\hat{R} + A_\theta\hat{\theta} + A_\phi\hat{\phi}
=
\begin{pmatrix}
A_R \\ A_\theta \\ A_\phi
\end{pmatrix}
$$

> [!tip]
> The spherical components $(A_R, A_\theta, A_\phi)$ are **not equal** to $(A_x, A_y, A_z)$ —  
> the unit vectors change direction with position.  
> This is why we represent vectors as **linear combinations of unit vectors**.

---

**Transforming between spherical and Cartesian components**

To find the *x*-component:

$$
A_x = \hat{x}\!\cdot\!\mathbf{A}(R, \theta, \phi)
= \hat{x}\!\cdot\!(A_R\hat{R} + A_\theta\hat{\theta} + A_\phi\hat{\phi})
$$

with:

$$
\hat{x}\!\cdot\!\hat{R} = \sin\theta\cos\phi, \qquad
\hat{x}\!\cdot\!\hat{\theta} = \cos\theta\cos\phi, \qquad
\hat{x}\!\cdot\!\hat{\phi} = -\sin\phi
$$

so:

$$
\boxed{
A_x = A_R\sin\theta\cos\phi + A_\theta\cos\theta\cos\phi - A_\phi\sin\phi
}
$$

Similarly:

$$
A_y = A_R\sin\theta\sin\phi + A_\theta\cos\theta\sin\phi + A_\phi\cos\phi
$$

$$
A_z = A_R\cos\theta - A_\theta\sin\theta
$$

> [!example]
> - $A_R$ controls the component **radially outward**.  
> - $A_\theta$ is the **polar (vertical)** component (toward $-z$ when $\theta$ increases).  
> - $A_\phi$ is the **azimuthal** component (around the $z$-axis).

---

> 🧠 **Remember:**  
> In spherical coordinates, both the **magnitudes** and the **directions** of $\hat{R}$, $\hat{\theta}$, and $\hat{\phi}$ depend on position —  
> that’s why converting between coordinate systems is essential before applying ∇, ∇·, or ∇×.
---

> [!details]- 🔗 Related examples
> - [[Examples/Cartesian to Cylindrical (Point+Vector)]]
