---
title: Exercise 18 — Coordinate Systems and Vector Operators
type: exercise
tags: [Electromagnetics, exercises, coordinates, vector-operators]
aliases: []
links: {"formulas": ["[[MOC – Coordinate Systems]]","[[MOC – Vector Operators]]"], "related": ["[[MOC – Exercises]]","[[MOC – Electromagnetics]]"]}
updated: 2025-11-07
---
> Quick refs: [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]]

---

# 18.1 — Coordinate Transforms & Components

## 🅐 Cartesian → Cylindrical / Spherical

> **Given**  
> Point: $P(x,y,z)=(3,-1,2)$  
> Vector: $\mathbf A = 5\hat{\mathbf x}-4\hat{\mathbf y}-\hat{\mathbf z}$  
>
> (i) Express $P$ and $\mathbf A$ in **cylindrical** coordinates and components.  
> (ii) Express $P$ and $\mathbf A$ in **spherical** coordinates and components.

---

### 🔹 (i) Cylindrical coordinates

**Theory recap**

- Conversion formulas:
  $$
  r = \sqrt{x^2 + y^2}, \qquad
  \phi = \pi + \big(\arccos\!\frac{x}{\sqrt{x^2 + y^2}} - \pi\big)\frac{y}{|y|}, \qquad
  z = z
  $$
  > This version of $\phi$ ensures correct **quadrant handling** (same as `atan2(y,x)`).

- Unit vectors:
  $$
  \hat{\mathbf r} = \cos\phi\,\hat{\mathbf x} + \sin\phi\,\hat{\mathbf y}, \quad
  \hat{\boldsymbol\phi} = -\sin\phi\,\hat{\mathbf x} + \cos\phi\,\hat{\mathbf y}, \quad
  \hat{\mathbf z} = \hat{\mathbf z}
  $$

- Vector components:
  $$
  \begin{aligned}
  A_r &= A_x\cos\phi + A_y\sin\phi,\\
  A_\phi &= -A_x\sin\phi + A_y\cos\phi,\\
  A_z &= A_z
  \end{aligned}
  $$

---

**Calculations**

Given  
$x = 3$, $y = -1$, $z = 2$,  
$A_x = 5$, $A_y = -4$, $A_z = -1$.

1️⃣ Compute $r$ and $\phi$:
$$
r = \sqrt{x^2 + y^2} = \sqrt{3^2 + (-1)^2} = \sqrt{10} = 3.1623
$$

$$
\phi = \pi + \left(\arccos\frac{3}{\sqrt{10}} - \pi\right)\frac{-1}{|-1|}
      = \arccos\!\frac{3}{\sqrt{10}} + 2\pi
$$

$$
\phi = 5.9614~\text{rad} = 341.565^\circ
$$

So the point in cylindrical coordinates:
$$
\boxed{P(r,\phi,z) = (3.162,\ 341.6^\circ,\ 2)}
$$

---

2️⃣ Compute $A_r$, $A_\phi$, and $A_z$:

Use $\cos\phi = x/r = 3/\sqrt{10} = 0.94868$ and $\sin\phi = y/r = -1/\sqrt{10} = -0.31623$:

$$
\begin{aligned}
A_r   &= A_x\cos\phi + A_y\sin\phi 
       = (5)(0.94868) + (-4)(-0.31623) 
       = 4.7434 + 1.2649 = 6.0083, \\[4pt]
A_\phi &= -A_x\sin\phi + A_y\cos\phi 
       = -(5)(-0.31623) + (-4)(0.94868)
       = 1.5811 - 3.7947 = -2.2136, \\[4pt]
A_z   &= -1
\end{aligned}
$$

$$
\boxed{
\mathbf A = 6.01\,\hat{\mathbf r} - 2.21\,\hat{\boldsymbol\phi} - 1.00\,\hat{\mathbf z}
}
$$

---

**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.1(a)(i) — Cylindrical components of A at P
>% Point and vector (Cartesian)
>x = 3;  y = -1;  z = 2;
>A = [5, -4, -1];   % [Ax Ay Az]
>
>% Cylindrical radius and angle
>r   = hypot(x, y);
>phi_robust = pi + (acos(x/r) - pi) * (y/abs(y));   % robust quadrant-safe phi
>phi_atan2  = atan2(y, x);                          % comparison (should match modulo 2*pi)
>
>% Exact cos/sin from coordinates
>c = x/r;
>s = y/r;
>
>% Cylindrical components of A at P
>Ar   = A(1)*c + A(2)*s;
>Aphi = -A(1)*s + A(2)*c;
>Az   = A(3);
>
>% Optional: reconstruct Ax, Ay to check consistency
>Ax_chk = Ar*c - Aphi*s;
>Ay_chk = Ar*s + Aphi*c;
>
>% ---- Display ----
>fprintf('r = %.6f\n', r);
>fprintf('phi_robust = %.6f rad  (%.3f deg)\n', phi_robust, rad2deg(phi_robust));
>fprintf('phi_atan2  = %.6f rad  (%.3f deg)\n\n', phi_atan2,  rad2deg(phi_atan2));
>
>fprintf('Ar   = %.6f\n', Ar);
>fprintf('Aphi = %.6f\n', Aphi);
>fprintf('Az   = %.6f\n\n', Az);
>
>fprintf('Rebuild check -> Ax: %.6f (orig %.6f),  Ay: %.6f (orig %.6f)\n', ...
>        Ax_chk, A(1), Ay_chk, A(2));
>```

---

### 🔹 (ii) Spherical coordinates

**Theory recap**

- Conversion formulas:
  $$
  R = \sqrt{x^2 + y^2 + z^2},\qquad
  \theta = \arctan\!\left(\frac{\sqrt{x^2+y^2}}{z}\right),\qquad
  \phi = \pi + \big(\arccos\!\frac{x}{\sqrt{x^2 + y^2}} - \pi\big)\frac{y}{|y|}
  $$
- Unit vectors and component transforms: see [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]].
### Cartesian → Spherical vector components

> Angle convention: $\theta$ is the polar angle from $+z$ (zenith), $\phi$ is the azimuth in the $xy$-plane from $+x$.

$$
\begin{aligned}
A_R &= A_x\,\sin\theta\cos\phi \;+\; A_y\,\sin\theta\sin\phi \;+\; A_z\,\cos\theta,\\[6pt]
A_\theta &= A_x\,\cos\theta\cos\phi \;+\; A_y\,\cos\theta\sin\phi \;-\; A_z\,\sin\theta,\\[6pt]
A_\phi &= -A_x\,\sin\phi \;+\; A_y\,\cos\phi.
\end{aligned}
$$
---

**Your calculation space**

Given  
$x = 3$, $y = -1$, $z = 2$,  
$A_x = 5$, $A_y = -4$, $A_z = -1$.

1️⃣ Compute $R$ , $\theta$ and $\phi$:
$$
R = \sqrt{x^2 + y^2 + z^2} = \sqrt{3^2+(-1)^2+2^2} = \sqrt{14} = 3.742
$$

$$
\theta = \arctan\!\left(\frac{\sqrt{x^2+y^2}}{z}\right)
      = 1.0068~\text{rad}
$$

$$
\theta = 1.0068~\text{rad} = 57.69^\circ
$$
$$
\phi = \pi + \left(\arccos\frac{3}{\sqrt{10}} - \pi\right)\frac{-1}{|-1|}
      = \arccos\!\frac{3}{\sqrt{10}} + 2\pi
$$
$$
\phi = 5.9614~\text{rad} = 341.565^\circ
$$
So the point in spherical coordinates:
$$
\boxed{P(R,\theta,\phi) = (3.742,\ 57.69^\circ,\ 341.6^\circ)}
$$

2️⃣ Compute $A_R$, $A_\theta$, and $A_\phi$:

$$
\begin{aligned}
A_R &= A_x\sin\theta\cos\phi + A_y\sin\theta\sin\phi + A_z\cos\theta \\[4pt]
    &= (5)(0.84515)(0.94868) + (-4)(0.84515)(-0.31623) + (-1)(0.53452) \\[4pt]
    &= 4.012 + 1.070 - 0.535 \\[4pt]
    &= 4.547
\end{aligned}
$$

$$
\begin{aligned}
A_\theta &= A_x\cos\theta\cos\phi + A_y\cos\theta\sin\phi - A_z\sin\theta \\[4pt]
         &= (5)(0.53452)(0.94868) + (-4)(0.53452)(-0.31623) - (-1)(0.84515) \\[4pt]
         &= 2.535 + 0.677 + 0.845 \\[4pt]
         &= 4.057
\end{aligned}
$$

$$
\begin{aligned}
A_\phi &= -A_x\sin\phi + A_y\cos\phi \\[4pt]
       &= -(5)(-0.31623) + (-4)(0.94868) \\[4pt]
       &= 1.581 - 3.795 \\[4pt]
       &= -2.214
\end{aligned}
$$

So the vector in spherical components evaluated at $P$ is:

$$
\boxed{
\mathbf A = 4.55\,\hat{\mathbf R} + 4.06\,\hat{\boldsymbol\theta} - 2.21\,\hat{\boldsymbol\phi}
}
$$
**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% Cartesian → Spherical (point + vector components)
>% Angle convention: theta = polar angle from +z (0..pi), phi = azimuth from +x in xy-plane (-pi..pi]
>
>function [R,theta,phi_robust,phi_atan2,AR,Ath,Aphi] = cart2sph_vec_phiRobust(x,y,z,Ax,Ay,Az)
>  % --- lengths
>  r = hypot(x,y);
>  R = hypot(r,z);
>
>  % --- angles
>  theta = atan2(r, z);                 % robust theta in [0, pi]
>
>  % your quadrant-safe phi (same as in your cylindrical script)
>  % guard y==0 to avoid division-by-zero in y/abs(y)
>  if y == 0
>    sgn = 1;  % convention: if y=0 choose +1 so phi=acos(x/r) when r>0
>  else
>    sgn = y/abs(y);
>  end
>  if r > 0
>    phi_robust = pi + (acos(x/r) - pi)*sgn;
>  else
>    phi_robust = 0;     % point on z-axis → define phi=0 by convention
>  end
>
>  % comparison (should match modulo 2*pi)
>  phi_atan2 = atan2(y, x);
>
>  % exact trig from coordinates
>  if r > 0
>    cphi = x/r; sphi = y/r;
>  else
>    cphi = 1;  sphi = 0;
>  end
>  if R > 0
>    sth = r/R; cth = z/R;
>  else
>    sth = 0;   cth = 1;
>  end
>
>  % --- spherical components of A at (x,y,z)
>  AR   =  Ax*sth*cphi + Ay*sth*sphi + Az*cth;
>  Ath  =  Ax*cth*cphi + Ay*cth*sphi - Az*sth;
>  Aphi = -Ax*sphi     + Ay*cphi;
>end
>
>% ------------------- Demo with your values -------------------
>% Point P = (3, -1, 2), Vector A = [5, -4, -1]
>x=3; y=-1; z=2;
>Ax=5; Ay=-4; Az=-1;
>
>[R,theta,phi_robust,phi_atan2,AR,Ath,Aphi] = cart2sph_vec_phiRobust(x,y,z,Ax,Ay,Az);
>
>fprintf('R      = %.6f\n', R);
>fprintf('theta  = %.6f rad (%.3f deg)\n', theta, rad2deg(theta));
>fprintf('phi_rb = %.6f rad (%.3f deg)\n', phi_robust,  rad2deg(phi_robust));
>fprintf('phi_a2 = %.6f rad (%.3f deg)\n\n', phi_atan2,   rad2deg(phi_atan2));
>
>fprintf('AR     = %.6f\n', AR);
>fprintf('Atheta = %.6f\n', Ath);
>fprintf('Aphi   = %.6f\n', Aphi);
>```


---

## 🅑 Cylindrical → Cartesian / Spherical

> **Given**  
> $P(r,\phi,z)=(5,3\pi/5,-2)$  
> $\mathbf A = 5\hat{\mathbf r}+1\hat{\boldsymbol\phi}+2\hat{\mathbf z}$  
>
> (i) Convert $P$ and $\mathbf A$ to **Cartesian**.  
> (ii) Convert $P$ and $\mathbf A$ to **spherical**.

---

### 🔹 (i) To Cartesian

**Theory recap**

$$
x = r\cos\phi,\quad y = r\sin\phi,\quad z = z
$$
and
$$
\begin{aligned}
A_x &= A_r\cos\phi - A_\phi\sin\phi,\\
A_y &= A_r\sin\phi + A_\phi\cos\phi,\\
A_z &= A_z
\end{aligned}
$$

**Your calculation space**

1️⃣ Compute $(x,y,z)$:  
$$
x = r\cos\phi = 5\cos(\frac{3\pi}{5})=-1.545
$$
$$
y = r\sin\phi = 5\sin(\frac{3\pi}{5}) =4.755
$$
$$
z=-2
$$
So the point in cartesian coordinates:
$$
\boxed{P(x,y,z) = (-1.545,\ 4.755,\ -2)}
$$
2️⃣ Compute $(A_x,A_y,A_z)$:  
$$
A_x = \_\_\_\_, \quad A_y = \_\_\_\_, \quad A_z = \_\_\_\_
$$

---

### 🔹 (ii) To Spherical

Use relations from [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]] to compute $(R,\theta,\phi)$ and corresponding $(A_R,A_\theta,A_\phi)$.

---

## 🅒 Spherical → Cartesian / Cylindrical

> **Given**  
> $(R,\theta,\phi)=(3,\pi/3,\pi/5)$  
> $\mathbf A = 3\hat{\boldsymbol\theta}-\hat{\boldsymbol\phi}$  
>
> (i) Convert to **Cartesian**.  
> (ii) Convert to **cylindrical**.

---

### 🔹 (i) To Cartesian

**Theory recap**

$$
\begin{aligned}
x &= R\sin\theta\cos\phi,\\
y &= R\sin\theta\sin\phi,\\
z &= R\cos\theta
\end{aligned}
$$

and
$$
\begin{aligned}
A_x &= A_R\sin\theta\cos\phi + A_\theta\cos\theta\cos\phi - A_\phi\sin\phi,\\
A_y &= A_R\sin\theta\sin\phi + A_\theta\cos\theta\sin\phi + A_\phi\cos\phi,\\
A_z &= A_R\cos\theta - A_\theta\sin\theta
\end{aligned}
$$

**Your calculation space**

1️⃣ Compute $(x,y,z)$:  
$$
x = \_\_\_\_, \quad y = \_\_\_\_, \quad z = \_\_\_\_
$$

2️⃣ Compute $(A_x,A_y,A_z)$:  
$$
A_x = \_\_\_\_, \quad A_y = \_\_\_\_, \quad A_z = \_\_\_\_
$$

---

### 🔹 (ii) To Cylindrical

Use transformations via [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]] to find $(r,\phi,z)$ and $(A_r,A_\phi,A_z)$.

---

# 18.2 — Differential Operators (∇, ∇·, ∇×)

> **Given**  
> a) $V=-x+2yx+2z^2$ → Find $\nabla V$  
> b) $\mathbf A=\hat{\mathbf r}\cos\phi+\hat{\boldsymbol\phi}\,r-\hat{\mathbf z}\sin\phi$ → Find $\nabla\!\cdot\!\mathbf A$  
> c) $\mathbf A=\hat{\boldsymbol\theta}\dfrac{\sin\theta\cos\phi}{R^2}$ → Find $\nabla\times\mathbf A$

**Theory references:**  
See the gradient, divergence, and curl operator tables in [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]].

---

# 18.3 — Integral Theorems (Gauss & Stokes)

> **Given**  
> a) Point charge $Q$ at origin — show $\displaystyle \oint_S \mathbf E\cdot d\mathbf s = \dfrac{Q}{\varepsilon_0}$.  
> b) Long wire on $z$-axis carrying $I$ — show $\displaystyle \oint_C \mathbf H\cdot d\boldsymbol\ell = I$.

**Theory recap**

- **Gauss’s law:** $\displaystyle \oint_S \mathbf D\!\cdot\!d\mathbf s = Q_{\text{enc}}$  
- **Ampère’s law:** $\displaystyle \oint_C \mathbf H\!\cdot\!d\boldsymbol\ell = I_{\text{enc}}$

---

