---
title: Divergence Example (E-field)
type: formula
tags: [electromagnetics, formula, examples, vector-operators]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05
---
### 🧩 Example — Divergence of a Vector Field

Let the electric field be:
$$
\mathbf E = \hat{\mathbf x}(2xz^2 + y) - \hat{\mathbf y}(yz).
$$

We want to find $\nabla\!\cdot\!\mathbf E$ in **Cartesian coordinates**.

---

**Step 1 — Recall the definition**

In Cartesian form:
$$
\nabla\!\cdot\!\mathbf E =
\frac{\partial E_x}{\partial x} +
\frac{\partial E_y}{\partial y} +
\frac{\partial E_z}{\partial z}.
$$

---

**Step 2 — Substitute the components**

From $\mathbf E = (E_x, E_y, E_z)$:
$$
E_x = 2xz^2 + y, \qquad
E_y = -yz, \qquad
E_z = 0.
$$

Compute each derivative:
$$
\begin{aligned}
\frac{\partial E_x}{\partial x} &= 2z^2, \\[4pt]
\frac{\partial E_y}{\partial y} &= -z, \\[4pt]
\frac{\partial E_z}{\partial z} &= 0.
\end{aligned}
$$

---

**Step 3 — Sum the partials**
$$
\nabla\!\cdot\!\mathbf E = 2z^2 - z.
$$

> ✅ **Result:**  
> The divergence is a **scalar** quantity representing the **net flux density** leaving each point in space.  
> Here, it depends on $z$, meaning the field has varying source strength along the $z$-axis.

---

> [!tip]
> - A **positive** divergence means **field lines are spreading out** (a source).  
> - A **negative** divergence means **field lines are converging** (a sink).  
> - If $\nabla\!\cdot\!\mathbf E = 0$, the field is **solenoidal**, with no net source inside the region.


---

---
