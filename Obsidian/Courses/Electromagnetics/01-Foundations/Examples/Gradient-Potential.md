---
title: "Gradient Potential"
type: formula
tags: [electromagnetics, foundations, formula, examples, vector-operators]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05
updated: "2025-11-05"
---
### 🧩 Example — Gradient of a Scalar Field

Let the scalar potential be:
$$
V = x^2 - y z - 3.
$$

We want to find $\nabla V$ in **Cartesian coordinates**.

---

**Step 1 — Recall the definition**

In Cartesian form:
$$
\nabla V =
\hat{\mathbf x}\frac{\partial V}{\partial x} +
\hat{\mathbf y}\frac{\partial V}{\partial y} +
\hat{\mathbf z}\frac{\partial V}{\partial z}.
$$

---

**Step 2 — Compute the partial derivatives**
$$
\begin{aligned}
\frac{\partial V}{\partial x} &= 2x, \\[4pt]
\frac{\partial V}{\partial y} &= -z, \\[4pt]
\frac{\partial V}{\partial z} &= -y.
\end{aligned}
$$

---

**Step 3 — Combine components**
$$
\nabla V = (2x)\,\hat{\mathbf x} + (-z)\,\hat{\mathbf y} + (-y)\,\hat{\mathbf z}.
$$

or equivalently,
$$
\boxed{\nabla V =
\begin{pmatrix}
2x\\[2pt]
-z\\[2pt]
-y
\end{pmatrix}}
$$

> ✅ **Result:**  
> The gradient is a **vector** that points in the direction of **maximum increase** of $V$.  
> In electrostatics, the **electric field** is related by $\mathbf E = -\nabla V$, meaning it points in the direction of *decreasing potential*.

---

> [!tip]
> - Large magnitude of $\nabla V$ → potential changes rapidly (strong field).  
> - Small magnitude → slow variation (weak field).  
> - Direction of $\nabla V$ → direction of steepest ascent of the scalar field.

---