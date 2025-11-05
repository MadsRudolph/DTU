---
title: "Differential Operators"
type: formula
tags: [electromagnetics, foundations, formula, vector-operators]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05

---
## ⚙️ Differential Vector Operators

In electromagnetics, we use three key differential operators to describe how scalar and vector fields **change in space**:

| Operator | Symbol | Acts on | Produces | Typical use |
|:--|:--|:--|:--|:--|
| **Gradient** | $\nabla V$ | Scalar field | Vector field | Change of potential → $\mathbf E = -\nabla V$ |
| **Divergence** | $\nabla\!\cdot\!\mathbf A$ | Vector field | Scalar field | Source strength → $\nabla\!\cdot\!\mathbf D = \rho_v$ |
| **Curl** | $\nabla\!\times\!\mathbf A$ | Vector field | Vector field | Circulation → $\nabla\!\times\!\mathbf H = \mathbf J$ |

---

### 🧭 Gradient — “rate of change” of a scalar field

The **gradient** measures *how fast* and *in what direction* a scalar quantity changes in space.  
From the slides:
$$
\nabla V \equiv \hat{\mathbf n}\frac{\partial V}{\partial n}
\quad\text{or in Cartesian form:}\quad
\nabla V = 
\hat{\mathbf x}\frac{\partial V}{\partial x}
+ \hat{\mathbf y}\frac{\partial V}{\partial y}
+ \hat{\mathbf z}\frac{\partial V}{\partial z}.
$$

- The result is a **vector** pointing in the direction of **maximum increase** of $V$.  
- Its magnitude gives the **steepest rate of change**.

**Example:**  
If $V(x,y,z)$ is an electric potential,  
then the electric field is:
$$
\mathbf E = -\nabla V.
$$
The negative sign means the field points toward *lower* potential.

> 🧠 **Intuition:**  
> Think of a “potential hill” — $\nabla V$ points uphill; $\mathbf E=-\nabla V$ points downhill.

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

### 🔹 Divergence — “how much flows out” of a point

The **divergence** measures the **net flux density** leaving a small volume.  
From the slides:
$$
\nabla\!\cdot\!\mathbf A
\equiv
\lim_{\Delta v\to0}
\frac{1}{\Delta v}
\oint_{\partial v} \mathbf A\!\cdot\!d\mathbf s.
$$

In Cartesian coordinates:
$$
\nabla\!\cdot\!\mathbf A =
\frac{\partial A_x}{\partial x}
+ \frac{\partial A_y}{\partial y}
+ \frac{\partial A_z}{\partial z}.
$$

- The result is a **scalar**.  
- If positive → **source** (outflow).  
- If negative → **sink** (inflow).  
- If zero → **solenoidal** field (no net creation or loss).

**Example in electrostatics:**  
$$
\nabla\!\cdot\!\mathbf D = \rho_v
\quad\Longrightarrow\quad
\text{charge density acts as a source of }\mathbf D.
$$

> 🧠 **Intuition:**  
> Picture field lines entering or leaving a tiny cube.  
> Divergence tells you if more lines go out than in.
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

### 🔁 Curl — “rotation” or circulation of a vector field

The **curl** measures the **tendency of a vector field to rotate** around a point.  
From the slides:
$$
\nabla\!\times\!\mathbf A
\equiv
\lim_{\Delta s\to0}
\frac{1}{\Delta s}\,
\hat{\mathbf n}\!
\oint_{\partial s}\!
\mathbf A\!\cdot\!d\boldsymbol{\ell}.
$$

In Cartesian coordinates:
$$
\nabla\!\times\!\mathbf A =
\begin{vmatrix}
\hat{\mathbf x} & \hat{\mathbf y} & \hat{\mathbf z} \\[2pt]
\frac{\partial}{\partial x} & \frac{\partial}{\partial y} & \frac{\partial}{\partial z} \\[2pt]
A_x & A_y & A_z
\end{vmatrix}
=
\hat{\mathbf x}\!\left(\frac{\partial A_z}{\partial y}-\frac{\partial A_y}{\partial z}\right)
+ \hat{\mathbf y}\!\left(\frac{\partial A_x}{\partial z}-\frac{\partial A_z}{\partial x}\right)
+ \hat{\mathbf z}\!\left(\frac{\partial A_y}{\partial x}-\frac{\partial A_x}{\partial y}\right).
$$

- The result is a **vector** pointing along the **axis of rotation**.  
- The magnitude indicates **how strong** the local circulation is.

**Example in magnetostatics:**  
$$
\nabla\!\times\!\mathbf H = \mathbf J
\quad\Longrightarrow\quad
\text{currents create circulating magnetic fields.}
$$

> 🧠 **Intuition:**  
> Imagine tiny paddles placed in the vector field — the curl tells you how they would spin.

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

### 🧩 Physical summary

| Concept | Mathematical form | Physical meaning | EM connection |
|:--|:--|:--|:--|
| **Gradient** | $\nabla V$ | Direction and rate of steepest change of a scalar | $\mathbf E=-\nabla V$ |
| **Divergence** | $\nabla\!\cdot\!\mathbf A$ | Source or sink strength (net outflow per volume) | $\nabla\!\cdot\!\mathbf D=\rho_v$ |
| **Curl** | $\nabla\!\times\!\mathbf A$ | Circulation or rotation around a point | $\nabla\!\times\!\mathbf H=\mathbf J$ |

---

> [!tip]
> These operators connect **integral laws** (like Gauss and Stokes) to their **differential forms**:
> - **Gauss’s theorem:** $\displaystyle \int_V (\nabla\!\cdot\!\mathbf A)\,dv = \oint_S \mathbf A\!\cdot\!d\mathbf s$  
> - **Stokes’s theorem:** $\displaystyle \int_S (\nabla\!\times\!\mathbf A)\!\cdot\!d\mathbf s = \oint_C \mathbf A\!\cdot\!d\boldsymbol{\ell}$  

Together, they form the mathematical bridge between **Maxwell’s integral laws** and their **point-form equations**.

---

> [!details]- 🔗 Related examples
> - [[Examples/Gradient Example (Potential)]]
> - [[Examples/Divergence Example (E-field)]]
> - [[Examples/Curl Example (B-field)]]
