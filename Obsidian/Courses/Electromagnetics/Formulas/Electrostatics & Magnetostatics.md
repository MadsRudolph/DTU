---
title: Lecture 18 Electrostatics & Magnetostatics
type: formula
tags:
  - Electromagnetics
  - formula
  - Coordinate-Systems
  - Electrostatics
  - Magnetostatics
aliases: []
links:
  formulas: []
  related: []
updated: 2025-11-05
---

> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Electrostatics & Magnetostatics — Quick Formula Sheet]]  
> **Quick refs:** [[MOC – Maxwell’s Equations]] · [[MOC – Coordinate Systems]] · [[MOC – Vector Operators]]  

> For **Electromagnetics (Applied)** — condensed reference of static-field relationships (electrostatics & magnetostatics).  
> Constants: $\mu_0 = 4\pi\times10^{-7}$ H/m, $\epsilon_0 = 1/(\mu_0 c^2)$, $c = 3\times10^8$ m/s, $\eta_0 = 377\ \Omega$.

---

## 🧭 Coordinate Systems

| System | Coordinates | Cartesian relations | Differential elements |
|:--|:--|:--|:--|
| **Cartesian** | $(x, y, z)$ | – | $d\ell = \hat{x}\,dx + \hat{y}\,dy + \hat{z}\,dz$<br>$dS = dx\,dy\,\hat{z}$ (etc.)<br>$dV = dx\,dy\,dz$ |
| **Cylindrical** | $(r, \phi, z)$ | $x = r\cos\phi$, $y = r\sin\phi$, $z = z$ | $d\ell = \hat{r}\,dr + \hat{\phi}\,r\,d\phi + \hat{z}\,dz$<br>$dS_r = r\,d\phi\,dz\,\hat{r}$<br>$dV = r\,dr\,d\phi\,dz$ |
| **Spherical** | $(R, \theta, \phi)$ | $x = R\sin\theta\cos\phi$, $y = R\sin\theta\sin\phi$, $z = R\cos\theta$ | $d\ell = \hat{R}\,dR + \hat{\theta}\,R\,d\theta + \hat{\phi}\,R\sin\theta\,d\phi$<br>$dS_R = R^2\sin\theta\,d\theta\,d\phi\,\hat{R}$<br>$dV = R^2\sin\theta\,dR\,d\theta\,d\phi$ |

> [!tip]
> • Use **cylindrical** symmetry for long wires or coax lines.  
> • Use **spherical** symmetry for point charges or spheres.  
> • Unit vectors rotate with position in cylindrical/spherical coordinates.

---

### 📐 Cartesian Coordinates
- Point defined by $(x, y, z)$ — three perpendicular axes.  
- Unit vectors: $\hat{x}, \hat{y}, \hat{z}$ (constant everywhere).  
- A vector:  
  $$
  \mathbf{A} = A_x\hat{x} + A_y\hat{y} + A_z\hat{z}
  $$
- Differential elements:  
  $$
  d\ell = \hat{x}\,dx + \hat{y}\,dy + \hat{z}\,dz,\quad dV = dx\,dy\,dz
  $$
> [!example]
> Ideal for uniform geometries like rectangular boxes, plates, or fields that vary along straight lines.

---

### 🌀 Cylindrical Coordinates
- Point defined by $(r, \phi, z)$  
  - $r$: distance from $z$-axis  
  - $\phi$: angle from $x$-axis (in $xy$-plane)  
  - $z$: same as Cartesian  
- Relations to Cartesian:  
  $$
  x = r\cos\phi,\quad y = r\sin\phi,\quad z = z
  $$
- Unit vectors:
  $$
  \hat{r} = \cos\phi\,\hat{x} + \sin\phi\,\hat{y},\quad
  \hat{\phi} = -\sin\phi\,\hat{x} + \cos\phi\,\hat{y},\quad
  \hat{z} = \hat{z}
  $$
- A vector:  
  $$
  \mathbf{A} = A_r\hat{r} + A_\phi\hat{\phi} + A_z\hat{z}
  $$
- Differential elements:  
  $$
  d\ell = \hat{r}\,dr + \hat{\phi}\,r\,d\phi + \hat{z}\,dz,\quad dV = r\,dr\,d\phi\,dz
  $$
> [!example]
> Use when symmetry is around an **axis** — wires, solenoids, coaxial cables, or cylinders.

---

### 🌍 Spherical Coordinates
- Point defined by $(R, \theta, \phi)$  
  - $R$: distance from origin  
  - $\theta$: angle from the $z$-axis (zenith angle)  
  - $\phi$: azimuth angle (in $xy$-plane)
- Relations to Cartesian:  
  $$
  x = R\sin\theta\cos\phi,\quad y = R\sin\theta\sin\phi,\quad z = R\cos\theta
  $$
- Unit vectors:
  $$
  \hat{R},\ \hat{\theta},\ \hat{\phi}
  $$
  These **change direction** with position (not fixed like $\hat{x}, \hat{y}, \hat{z}$).
- A vector:  
  $$
  \mathbf{A} = A_R\hat{R} + A_\theta\hat{\theta} + A_\phi\hat{\phi}
  $$
- Differential elements:  
  $$
  d\ell = \hat{R}\,dR + \hat{\theta}\,R\,d\theta + \hat{\phi}\,R\sin\theta\,d\phi,\quad dV = R^2\sin\theta\,dR\,d\theta\,d\phi
  $$
> [!example]
> Use for problems with **point or spherical symmetry** — e.g., electric field of a point charge, or inside/outside a sphere.

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
### 🔄 Transforming from Cartesian → Spherical Components

We can also express the spherical components $(A_R, A_\theta, A_\phi)$ in terms of the Cartesian ones $(A_x, A_y, A_z)$.

Using the same geometric relations:

$$
\begin{aligned}
A_R &= A_x\sin\theta\cos\phi + A_y\sin\theta\sin\phi + A_z\cos\theta \\[4pt]
A_\theta &= A_x\cos\theta\cos\phi + A_y\cos\theta\sin\phi - A_z\sin\theta \\[4pt]
A_\phi &= -A_x\sin\phi + A_y\cos\phi
\end{aligned}
$$

> [!note]
> - $A_R$ points **radially outward** from the origin.  
> - $A_\theta$ points **downward** (increasing $\theta$).  
> - $A_\phi$ points **azimuthally**, tangent to constant-$R$, constant-$\theta$ circles.

---

**Matrix form (for quick reference):**

$$
\begin{bmatrix}
A_R \\[4pt] A_\theta \\[4pt] A_\phi
\end{bmatrix}
=
\begin{bmatrix}
\sin\theta\cos\phi & \sin\theta\sin\phi & \cos\theta \\[4pt]
\cos\theta\cos\phi & \cos\theta\sin\phi & -\sin\theta \\[4pt]
-\sin\phi & \cos\phi & 0
\end{bmatrix}
\begin{bmatrix}
A_x \\[4pt] A_y \\[4pt] A_z
\end{bmatrix}
$$

and conversely (from spherical → Cartesian):

$$
\begin{bmatrix}
A_x \\[4pt] A_y \\[4pt] A_z
\end{bmatrix}
=
\begin{bmatrix}
\sin\theta\cos\phi & \cos\theta\cos\phi & -\sin\phi \\[4pt]
\sin\theta\sin\phi & \cos\theta\sin\phi & \cos\phi \\[4pt]
\cos\theta & -\sin\theta & 0
\end{bmatrix}
\begin{bmatrix}
A_R \\[4pt] A_\theta \\[4pt] A_\phi
\end{bmatrix}
$$

> [!tip]
> Keep this matrix handy when verifying that $\mathbf{E}$ or $\mathbf{H}$ fields are **transverse** or **radially symmetric** in spherical problems.  
> It also helps simplify boundary conditions and power density calculations.

---
### 🧪 Worked Example — Cartesian → Cylindrical (with vector components)

> Given **P** in Cartesian: $P(x,y,z)=(3,-1,2)$  
> and **A** in Cartesian: $\mathbf A = 5\,\hat{\mathbf x}-4\,\hat{\mathbf y}-1\,\hat{\mathbf z}$,  
> express **(i)** $P$ in cylindrical coordinates $(r,\phi,z)$ and **(ii)** $\mathbf A$ in cylindrical components $(A_r, A_\phi, A_z)$ **evaluated at $P$**.

#### Step 1 — Point conversion (Cartesian → Cylindrical)

- **Radius** (distance to the $z$-axis):
$$
r=\sqrt{x^2+y^2}=\sqrt{3^2+(-1)^2}=\sqrt{10}\approx 3.162
$$

- **Azimuth $\phi$ (quadrant-safe).**  
  $\phi=\tan^{-1}(y/x)$ fails in QII/QIII. Use a quadrant-aware definition (equivalent to $\operatorname{atan2}(y,x)$):
$$
\phi=\pi+\arccos\!\Big(\frac{x}{\sqrt{x^2+y^2}}\Big)-\pi\,\frac{y}{|y|}.
$$
For $(x,y)=(3,-1)$:
$$
\begin{aligned}
\phi
&=\pi+\arccos\!\Big(\tfrac{3}{\sqrt{10}}\Big)-\pi(-1)
= \arccos\!\Big(\tfrac{3}{\sqrt{10}}\Big)+2\pi \\
&\approx -18.435^\circ \quad(\text{or }341.565^\circ\ \text{mod }360^\circ).
\end{aligned}
$$

- **Height:** $z=2$.

**Result (point):**  
$\boxed{(r,\phi,z)\approx(3.162,\;341.6^\circ,\;2)}$

> *Why this formula?* The $\frac{y}{|y|}$ factor enforces the correct **sign of rotation** around the $z$-axis, so $\phi$ lands in the right quadrant.

---

#### Step 2 — Unit vectors & component relations at $P$

Cylindrical basis (depends on $\phi$):
$$
\hat{\mathbf r}=\cos\phi\,\hat{\mathbf x}+\sin\phi\,\hat{\mathbf y},\qquad
\hat{\boldsymbol\phi}=-\sin\phi\,\hat{\mathbf x}+\cos\phi\,\hat{\mathbf y},\qquad
\hat{\mathbf z}=\hat{\mathbf z}.
$$

Project $\mathbf A$ onto the rotating basis:
$$
\boxed{
\begin{aligned}
A_r &= A_x\cos\phi + A_y\sin\phi,\\
A_\phi &= -A_x\sin\phi + A_y\cos\phi,\\
A_z &= A_z.
\end{aligned}}
$$

At $\phi\approx -18.435^\circ$:
$$
\cos\phi\approx 0.94868,\qquad \sin\phi\approx -0.31623
$$

Compute:
$$
\begin{aligned}
A_r &= (5)(0.94868)+(-4)(-0.31623)\approx 4.743+1.265=6.008,\\[2mm]
A_\phi &= -(5)(-0.31623)+(-4)(0.94868)\approx 1.581-3.795=-2.214,\\[2mm]
A_z &= -1.
\end{aligned}
$$

**Result (vector at $P$):**  
$\boxed{\mathbf A(P)=6.008\,\hat{\mathbf r}\;-\;2.214\,\hat{\boldsymbol\phi}\;-\;\hat{\mathbf z}}$

> **Sanity checks**  
> • Magnitude preserved: $A_r^2+A_\phi^2+A_z^2\approx 42 = 5^2+(-4)^2+(-1)^2$.  
> • Sign intuition: with $\phi$ slightly negative and $A_x>0, A_y<0$, the azimuthal component is **negative**.

---

> [!details]- MATLAB template — Cartesian → Cylindrical (point + vector)
> ```matlab
> % File: cart2cyl_point_vector.m
> % Convert a point P=[x y z] and Cartesian vector A=[Ax Ay Az]
> % to cylindrical coordinates and components at that point.
> % Uses atan2 for correct quadrant handling (matches the robust phi formula).
> %
> % Example:
> %   [r,phi,phi_deg,z,Ar,Aphi,Az] = cart2cyl_point_vector([3 -1 2],[5 -4 -1]);
> %   fprintf('(r,phi,z) = (%.3f, %.3f deg, %.3f)\n', r, phi_deg, z);
> %   fprintf('A = %.3f rhat  %+ .3f phihat  %+ .3f zhat\n', Ar, Aphi, Az);
> 
> function [r,phi,phi_deg,z,Ar,Aphi,Az] = cart2cyl_point_vector(P,A)
>   arguments
>     P (1,3) double  % [x y z]
>     A (1,3) double  % [Ax Ay Az]
>   end
> 
>   x = P(1); y = P(2); z = P(3);
>   Ax = A(1); Ay = A(2); Az = A(3);
> 
>   % --- Point conversion
>   r   = hypot(x,y);       % sqrt(x^2 + y^2)
>   phi = atan2(y,x);       % robust azimuth in radians (-pi, pi]
>   phi_deg = rad2deg(phi);
> 
>   % --- Vector components in cylindrical basis
>   c = cos(phi); s = sin(phi);
>   Ar   =  Ax*c + Ay*s;
>   Aphi = -Ax*s + Ay*c;
>   % z-component unchanged
>   Az   = Az;
> end
> 
> % --- Quick test (uncomment):
> % [r,phi,phi_deg,z,Ar,Aphi,Az] = cart2cyl_point_vector([3 -1 2],[5 -4 -1]);
> % fprintf('(r,phi,z) = (%.3f, %.3f deg, %.3f)\n', r, phi_deg, z);
> % fprintf('A = %.3f rhat  %+ .3f phihat  %+ .3f zhat\n', Ar, Aphi, Az);
> ```

---

## ⚡ Electrostatics  (∂/∂t = 0, J = 0)

**Fundamental laws**

- **Coulomb’s law:**  
  $$\mathbf E = \frac{1}{4\pi\epsilon}\frac{q}{R^2}\hat{R}$$
- **Flux density:** $\mathbf D = \epsilon\mathbf E$
- **Gauss’s law (integral form):**  
  $$\oint_S \mathbf D\!\cdot\!d\mathbf s = Q_{\text{enc}}$$
- **Differential form:** $\nabla\!\cdot\!\mathbf D = \rho_v$
- **Electrostatic potential:**  
  $$\mathbf E = -\nabla V,\quad V_{21} = -\int_{P_1}^{P_2}\mathbf E\!\cdot\!d\boldsymbol\ell$$
- **Energy density:** $w_E = \tfrac{1}{2}\epsilon E^2$


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
> Together, they form the **mathematical backbone of Maxwell’s equations**.
