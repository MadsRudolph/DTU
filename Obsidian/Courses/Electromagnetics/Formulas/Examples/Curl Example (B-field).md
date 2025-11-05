---
title: Curl Example (B-field)
type: formula
tags: [electromagnetics, formula, examples, vector-operators]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05
---
### 🧩 Example — Curl of a Vector Field

Let the magnetic field be
$$
\mathbf B = \hat{\mathbf x}\,(z x^2 + y) \;-\; \hat{\mathbf y}.
$$

We want $\nabla\times\mathbf B$ in **Cartesian coordinates**.

---

**Step 1 — Recall the Cartesian curl**
$$
\nabla\times\mathbf B =
\begin{vmatrix}
\hat{\mathbf x} & \hat{\mathbf y} & \hat{\mathbf z} \\
\frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\
B_x & B_y & B_z
\end{vmatrix}
=
\hat{\mathbf x}\!\left(\frac{\partial B_z}{\partial y}-\frac{\partial B_y}{\partial z}\right)
+ \hat{\mathbf y}\!\left(\frac{\partial B_x}{\partial z}-\frac{\partial B_z}{\partial x}\right)
+ \hat{\mathbf z}\!\left(\frac{\partial B_y}{\partial x}-\frac{\partial B_x}{\partial y}\right).
$$

---

**Step 2 — Identify components and partials**
$$
B_x = z x^2 + y,\qquad B_y = -1,\qquad B_z = 0.
$$

Compute the needed derivatives:
$$
\begin{aligned}
\frac{\partial B_z}{\partial y} &= 0, & \frac{\partial B_y}{\partial z} &= 0,\\[2pt]
\frac{\partial B_x}{\partial z} &= x^2, & \frac{\partial B_z}{\partial x} &= 0,\\[2pt]
\frac{\partial B_y}{\partial x} &= 0, & \frac{\partial B_x}{\partial y} &= 1.
\end{aligned}
$$

---

**Step 3 — Assemble the components**
$$
\begin{aligned}
(\nabla\times\mathbf B)_x &= 0 - 0 = 0,\\
(\nabla\times\mathbf B)_y &= x^2 - 0 = x^2,\\
(\nabla\times\mathbf B)_z &= 0 - 1 = -1.
\end{aligned}
$$

**Result**
$$
\boxed{\nabla\times\mathbf B = 0\,\hat{\mathbf x} + x^2\,\hat{\mathbf y} - 1\,\hat{\mathbf z}}
\;=\;
\begin{pmatrix}0\\ x^2\\ -1\end{pmatrix}.
$$

> 💡 **Interpretation:** The curl is a **vector** pointing along the local axis of rotation (right-hand rule).  
> Here the field has **positive $y$-directed circulation** that grows with $x$ and a **constant clockwise** rotation about the $z$-axis (negative $\hat{\mathbf z}$ component).

---
