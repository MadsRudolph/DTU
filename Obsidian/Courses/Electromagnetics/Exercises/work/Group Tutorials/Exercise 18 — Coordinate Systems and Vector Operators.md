---
title: Exercise 18 — Coordinate Systems and Vector Operators
type: exercise
tags: [Electromagnetics, exercises, coordinates, vector-operators]
aliases: []
links: {"formulas": ["[[MOC – Coordinate Systems]]","[[MOC – Vector Operators]]"], "related": ["[[MOC – Exercises]]","[[MOC – Electromagnetics]]"]}
updated: 2025-11-07
---
> Quick refs: [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]]
> Important vector components transformation see: [[L18_Coordinate_Systems_Integrals_Differential_Space_Operators_Theorems.pdf]]
---

# 18.1 — Coordinate Transforms & Components

## A) Cartesian → Cylindrical / Spherical

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

# 18.1 — Coordinate Transforms & Components

## B) Cylindrical → Cartesian / Spherical

> **Given**  
> Point: $P(r,\phi,z) = (5,\ 3\pi/5,\ -2)$  
> Vector: $\mathbf A = 5\hat{\mathbf r} + \hat{\boldsymbol\phi} + 2\hat{\mathbf z}$  
>
> (i) Express $P$ and $\mathbf A$ in **Cartesian** coordinates and components.  
> (ii) Express $P$ and $\mathbf A$ in **spherical** coordinates and components.

---

### 🔹 (i) Cartesian coordinates

**Theory recap**

- Conversion formulas:
  $$
  x = r\cos\phi, \qquad
  y = r\sin\phi, \qquad
  z = z
  $$

- Unit vectors:
  $$
  \hat{\mathbf r} = \cos\phi\,\hat{\mathbf x} + \sin\phi\,\hat{\mathbf y}, \quad
  \hat{\boldsymbol\phi} = -\sin\phi\,\hat{\mathbf x} + \cos\phi\,\hat{\mathbf y}, \quad
  \hat{\mathbf z} = \hat{\mathbf z}
  $$

- Vector components:
  $$
  \begin{aligned}
  A_x &= A_r\cos\phi - A_\phi\sin\phi,\\
  A_y &= A_r\sin\phi + A_\phi\cos\phi,\\
  A_z &= A_z
  \end{aligned}
  $$

---

**Calculations**

Given  
$r = 5$, $\phi = 3\pi/5 \approx 1.885$ rad $= 108^\circ$, $z = -2$,  
$A_r = 5$, $A_\phi = 1$, $A_z = 2$.

---

1️⃣ Compute $x$, $y$, and $z$:

$$
\cos\phi = \cos(108^\circ) = -\cos(72^\circ) \approx -0.3090, \qquad
\sin\phi = \sin(108^\circ) \approx 0.9511
$$

$$
x = r\cos\phi = (5)(-0.3090) = -1.545, \qquad
y = r\sin\phi = (5)(0.9511) = 4.755, \qquad
z = -2
$$

So the point in Cartesian coordinates:
$$
\boxed{P(x,y,z) = (-1.545,\ 4.755,\ -2)}
$$

---

2️⃣ Compute $A_x$, $A_y$, and $A_z$:

$$
\begin{aligned}
A_x &= A_r\cos\phi - A_\phi\sin\phi
       = (5)(-0.3090) - (1)(0.9511)
       = -1.545 - 0.9511 = -2.496, \\[4pt]
A_y &= A_r\sin\phi + A_\phi\cos\phi
       = (5)(0.9511) + (1)(-0.3090)
       = 4.755 - 0.3090 = 4.446, \\[4pt]
A_z &= 2
\end{aligned}
$$

$$
\boxed{
\mathbf A = -2.50\,\hat{\mathbf x} + 4.45\,\hat{\mathbf y} + 2.00\,\hat{\mathbf z}
}
$$

---

**Verification (optional in MATLAB)**  
>[!code]- matlab
>```matlab
>% 18.1(b)(i) — Cylindrical → Cartesian
>% Point and vector
>r = 5; phi = 3*pi/5; z = -2;
>A = [5, 1, 2];   % [Ar Aphi Az]
>
>% Conversion to Cartesian
>x = r*cos(phi);
>y = r*sin(phi);
>
>Ax = A(1)*cos(phi) - A(2)*sin(phi);
>Ay = A(1)*sin(phi) + A(2)*cos(phi);
>Az = A(3);
>
>% ---- Display ----
>fprintf('x = %.3f,  y = %.3f,  z = %.3f\n', x, y, z);
>fprintf('Ax = %.3f,  Ay = %.3f,  Az = %.3f\n', Ax, Ay, Az);
>```

---
### 🔹 (ii) Spherical coordinates

**Theory recap**

- Conversion formulas:
  $$
  R = \sqrt{r^2 + z^2}, \qquad 
  \theta = \arccos\!\left(\frac{z}{R}\right), \qquad 
  \phi = \phi
  $$

- Unit vectors and component transforms: see [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]].

- Cylindrical → Spherical vector components:
  $$
  A_R = \sin\theta\,A_r + \cos\theta\,A_z, \qquad
  A_\theta = \cos\theta\,A_r - \sin\theta\,A_z, \qquad
  A_\phi = A_\phi
  $$

---

**Calculations**

Given  
$r = 5$, $\phi = 108^\circ$, $z = -2$,  
$A_r = 5$, $A_\phi = 1$, $A_z = 2$.

---

1️⃣ Compute $R$, $\theta$, and $\phi$:

$$
R = \sqrt{r^2 + z^2} = \sqrt{25 + 4} = \sqrt{29} = 5.385
$$

$$
\theta = \arccos\!\left(\frac{z}{R}\right)
= \arccos\!\left(\frac{-2}{5.385}\right)
\approx 1.951~\text{rad} = 112^\circ
$$

$$
\phi = 108^\circ
$$

So the point in spherical coordinates:
$$
\boxed{P(R,\theta,\phi) = (5.385,\ 112^\circ,\ 108^\circ)}
$$

---

2️⃣ Compute $A_R$, $A_\theta$, and $A_\phi$:

Use $\cos\theta = z/R \approx -0.3714$ and $\sin\theta = r/R \approx 0.9285$.

$$
\begin{aligned}
A_R &= \sin\theta\,A_r + \cos\theta\,A_z
     = (0.9285)(5) + (-0.3714)(2)
     = 4.642 - 0.743 = 3.899, \\[6pt]
A_\theta &= \cos\theta\,A_r - \sin\theta\,A_z
          = (-0.3714)(5) - (0.9285)(2)
          = -1.857 - 1.857 = -3.714, \\[6pt]
A_\phi &= A_\phi = 1
\end{aligned}
$$

So the vector in spherical components evaluated at $P$ is:

$$
\boxed{
\mathbf A = 3.90\,\hat{\mathbf R} - 3.71\,\hat{\boldsymbol\theta} + 1.00\,\hat{\boldsymbol\phi}
}
$$
---
**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.1(b)(ii) — Spherical components of A at P from cylindrical
>% Point and vector (cylindrical)
>r = 5; phi = 3*pi/5; z = -2;
>A = [5, 1, 2]; % [Ar Aphi Az]
>
>% Spherical radius and theta
>R = hypot(r, z);
>theta = acos(z/R); % theta in [0, pi]
>
>% Sin/cos theta from coordinates (exact)
>sth = r/R;
>cth = z/R;
>
>% Spherical components of A at P
>AR = sth*A(1) + cth*A(3);
>Atheta = cth*A(1) - sth*A(3);
>Aphi = A(2);
>
>% Optional: reconstruct Ar, Az to check consistency
>Ar_chk = sth*AR + cth*Atheta;
>Az_chk = cth*AR - sth*Atheta;
>
>% ---- Display ----
>fprintf('R = %.3f\n', R);
>fprintf('theta = %.3f rad (%.3f deg)\n', theta, rad2deg(theta));
>fprintf('phi = %.3f rad (%.3f deg)\n\n', phi, rad2deg(phi));
>
>fprintf('AR = %.3f\n', AR);
>fprintf('Atheta = %.3f\n', Atheta);
>fprintf('Aphi = %.3f\n\n', Aphi);
>
>fprintf('Rebuild check -> Ar: %.3f (orig %.3f), Az: %.3f (orig %.3f)\n', ...
>        Ar_chk, A(1), Az_chk, A(3));
>```

---
## C) Spherical → Cartesian / Cylindrical

> **Given**  
> Point: $P(R,\theta,\phi) = (3,\ \pi/3,\ \pi/5)$  
> Vector: $\mathbf A = 3\hat{\boldsymbol\theta} - \hat{\boldsymbol\phi}$  
>
> (i) Express $P$ and $\mathbf A$ in **Cartesian** coordinates and components.  
> (ii) Express $P$ and $\mathbf A$ in **cylindrical** coordinates and components.

---

### 🔹 (i) Cartesian coordinates

**Theory recap**

- Conversion formulas:
  $$
  x = R\sin\theta\cos\phi, \qquad
  y = R\sin\theta\sin\phi, \qquad
  z = R\cos\theta
  $$

- Unit vectors and component transforms: see [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]].

- Spherical → Cartesian vector components:
  $$
  \begin{aligned}
  A_x &= \sin\theta\cos\phi\,A_R + \cos\theta\cos\phi\,A_\theta - \sin\phi\,A_\phi,\\[4pt]
  A_y &= \sin\theta\sin\phi\,A_R + \cos\theta\sin\phi\,A_\theta + \cos\phi\,A_\phi,\\[4pt]
  A_z &= \cos\theta\,A_R - \sin\theta\,A_\theta
  \end{aligned}
  $$

---

**Calculations**

Given  
$R = 3$, $\theta = \pi/3 \approx 1.047$ rad $= 60^\circ$, $\phi = \pi/5 \approx 0.628$ rad $= 36^\circ$,  
$A_R = 0$, $A_\theta = 3$, $A_\phi = -1$.

---

1️⃣ Compute $x$, $y$, and $z$:

$$
\cos\phi = \cos(36^\circ) \approx 0.8090, \qquad
\sin\phi = \sin(36^\circ) \approx 0.5878
$$

$$
\sin\theta = \sin(60^\circ) = \frac{\sqrt{3}}{2} \approx 0.8660, \qquad
\cos\theta = \cos(60^\circ) = 0.5
$$

$$
x = R\sin\theta\cos\phi = (3)(0.8660)(0.8090) \approx 2.102, \qquad
y = R\sin\theta\sin\phi = (3)(0.8660)(0.5878) \approx 1.527, \qquad
z = (3)(0.5) = 1.5
$$

So the point in Cartesian coordinates:
$$
\boxed{P(x,y,z) = (2.102,\ 1.527,\ 1.5)}
$$

---

2️⃣ Compute $A_x$, $A_y$, and $A_z$:

$$
\begin{aligned}
A_x &= \sin\theta\cos\phi\,A_R + \cos\theta\cos\phi\,A_\theta - \sin\phi\,A_\phi \\[4pt]
    &= (0)(0.8660)(0.8090) + (0.5)(0.8090)(3) - (0.5878)(-1) \\[4pt]
    &= 1.214 + 0.588 = 1.802, \\[6pt]
A_y &= \sin\theta\sin\phi\,A_R + \cos\theta\sin\phi\,A_\theta + \cos\phi\,A_\phi \\[4pt]
    &= (0)(0.8660)(0.5878) + (0.5)(0.5878)(3) + (0.8090)(-1) \\[4pt]
    &= 0.882 - 0.809 = 0.073, \\[6pt]
A_z &= \cos\theta\,A_R - \sin\theta\,A_\theta
    = (0)(0.5) - (0.8660)(3) = -2.598
\end{aligned}
$$

So the vector in Cartesian components is:
$$
\boxed{
\mathbf A = 1.80\,\hat{\mathbf x} + 0.07\,\hat{\mathbf y} - 2.60\,\hat{\mathbf z}
}
$$

---
**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.1(c)(ii) — Cartesian components of A at P from spherical
>% Point and vector (spherical)
>R = 3; theta = pi/3; phi = pi/5;
>A = [0, 3, -1]; % [AR Atheta Aphi]
>
>% Sin/cos
>sth = sin(theta); cth = cos(theta);
>sp = sin(phi); cp = cos(phi);
>
>% Cartesian point
>x = R*sth*cp;
>y = R*sth*sp;
>z = R*cth;
>
>% Cartesian components of A at P
>Ax = sth*cp*A(1) + cth*cp*A(2) - sp*A(3);
>Ay = sth*sp*A(1) + cth*sp*A(2) + cp*A(3);
>Az = cth*A(1) - sth*A(2);
>
>% Optional: reconstruct AR, Atheta, Aphi to check consistency
>AR_chk      = sth*cp*Ax + sth*sp*Ay + cth*Az;
>Atheta_chk  = cth*cp*Ax + cth*sp*Ay - sth*Az;
>Aphi_chk    = -sp*Ax + cp*Ay;
>
>% ---- Display ----
>fprintf('x = %.3f\n', x);
>fprintf('y = %.3f\n', y);
>fprintf('z = %.3f\n\n', z);
>
>fprintf('Ax = %.3f\n', Ax);
>fprintf('Ay = %.3f\n', Ay);
>fprintf('Az = %.3f\n\n', Az);
>
>fprintf('Rebuild check -> AR: %.3f (orig %.3f), Atheta: %.3f (orig %.3f), Aphi: %.3f (orig %.3f)\n', ...
>        AR_chk, A(1), Atheta_chk, A(2), Aphi_chk, A(3));
>```

---
### 🔹 (ii) Cylindrical coordinates

**Theory recap**

- Conversion formulas:
  $$
  r = R\sin\theta, \qquad
  \phi = \phi, \qquad
  z = R\cos\theta
  $$

- Unit vectors and component transforms: see [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]].

- Spherical → Cylindrical vector components:
  $$
  A_r = \sin\theta\,A_R + \cos\theta\,A_\theta, \qquad
  A_\phi = A_\phi, \qquad
  A_z = \cos\theta\,A_R - \sin\theta\,A_\theta
  $$

---

**Calculations**

Given  
$R = 3$, $\theta = 60^\circ$, $\phi = 36^\circ$,  
$A_R = 0$, $A_\theta = 3$, $A_\phi = -1$.

---

1️⃣ Compute $r$, $\phi$, and $z$:

$$
r = R\sin\theta = (3)(0.8660) = 2.598, \qquad
\phi = 36^\circ, \qquad
z = (3)(0.5) = 1.5
$$

So the point in cylindrical coordinates:
$$
\boxed{P(r,\phi,z) = (2.598,\ 36^\circ,\ 1.5)}
$$

---

2️⃣ Compute $A_r$, $A_\phi$, and $A_z$:

$$
\begin{aligned}
A_r &= \sin\theta\,A_R + \cos\theta\,A_\theta
     = (0.8660)(0) + (0.5)(3) = 1.5, \\[6pt]
A_\phi &= A_\phi = -1, \\[6pt]
A_z &= \cos\theta\,A_R - \sin\theta\,A_\theta
     = (0.5)(0) - (0.8660)(3) = -2.598
\end{aligned}
$$

So the vector in cylindrical components is:
$$
\boxed{
\mathbf A = 1.50\,\hat{\mathbf r} - 1.00\,\hat{\boldsymbol\phi} - 2.60\,\hat{\mathbf z}
}
$$

---

**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.1(c)(ii) — Cylindrical components of A at P from spherical
>% Point and vector (spherical)
>R = 3; theta = pi/3; phi = pi/5;
>A = [0, 3, -1]; % [AR Atheta Aphi]
>
>% Sin/cos theta
>sth = sin(theta);
>cth = cos(theta);
>
>% Cylindrical point
>r = R*sth;
>phi_out = phi;
>z = R*cth;
>
>% Cylindrical components of A at P
>Ar = sth*A(1) + cth*A(2);
>Aphi = A(3);
>Az = cth*A(1) - sth*A(2);
>
>% Optional: reconstruct AR, Atheta to check consistency
>AR_chk = sth*Ar + cth*Az;
>Atheta_chk = cth*Ar - sth*Az;
>
>% ---- Display ----
>fprintf('r = %.3f\n', r);
>fprintf('phi = %.3f rad (%.3f deg)\n', phi_out, rad2deg(phi_out));
>fprintf('z = %.3f\n\n', z);
>
>fprintf('Ar = %.3f\n', Ar);
>fprintf('Aphi = %.3f\n', Aphi);
>fprintf('Az = %.3f\n\n', Az);
>
>fprintf('Rebuild check -> AR: %.3f (orig %.3f), Atheta: %.3f (orig %.3f)\n', ...
>        AR_chk, A(1), Atheta_chk, A(2));
>```

---

# 18.2 — Vector Differential Operators

---

## A) Gradient

> **Given**  
> Scalar field: $V = -x + 2yx + 2z^2$  
>  
> Compute the gradient $\nabla V$ in Cartesian coordinates.

---

**Theory recap**

- The gradient of a scalar field $V(x, y, z)$ in Cartesian coordinates is:
  $$
  \nabla V = 
  \frac{\partial V}{\partial x}\hat{\mathbf x} +
  \frac{\partial V}{\partial y}\hat{\mathbf y} +
  \frac{\partial V}{\partial z}\hat{\mathbf z}
  $$
- It represents the direction and magnitude of the steepest ascent of $V$.

---

**Calculations**

1️⃣ Compute partial derivatives:

$$
\frac{\partial V}{\partial x} = -1 + 2y, \qquad
\frac{\partial V}{\partial y} = 2x, \qquad
\frac{\partial V}{\partial z} = 4z
$$

So the gradient is:
$$
\boxed{
\nabla V = (2y - 1)\hat{\mathbf x} + 2x\hat{\mathbf y} + 4z\hat{\mathbf z}
}
$$

---

**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.2(a) — Gradient of V in Cartesian
>syms x y z
>V = -x + 2*y*x + 2*z^2;
>
>gradV = [diff(V, x), diff(V, y), diff(V, z)]
>```

---

## B) Divergence

> **Given**  
> Vector field: $\mathbf A = \cos\phi\,\hat{\mathbf r} + r\,\hat{\boldsymbol\phi} - \sin\phi\,\hat{\mathbf z}$  
>  
> Compute the divergence $\nabla\!\cdot\!\mathbf A$ in cylindrical coordinates.

---

**Theory recap**

- Divergence in cylindrical coordinates $(r, \phi, z)$:
  $$
  \nabla\!\cdot\!\mathbf A
  = \frac{1}{r}\frac{\partial (rA_r)}{\partial r}
  + \frac{1}{r}\frac{\partial A_\phi}{\partial \phi}
  + \frac{\partial A_z}{\partial z}
  $$

- It measures the net outflow of the field per unit volume.

---

**Calculations**

Components:  
$A_r = \cos\phi$, $A_\phi = r$, $A_z = -\sin\phi$

---

1️⃣ Compute terms:

$$
\frac{1}{r}\frac{\partial (rA_r)}{\partial r}
= \frac{1}{r}\frac{\partial (r\cos\phi)}{\partial r}
= \frac{1}{r}(\cos\phi)
= \frac{\cos\phi}{r}
$$

$$
\frac{1}{r}\frac{\partial A_\phi}{\partial \phi}
= \frac{1}{r}\frac{\partial r}{\partial \phi} = 0, \qquad
\frac{\partial A_z}{\partial z} = \frac{\partial (-\sin\phi)}{\partial z} = 0
$$

So the divergence is:
$$
\boxed{
\nabla\!\cdot\!\mathbf A = \frac{\cos\phi}{r}
}
$$

---

**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.2(b) — Divergence of A in cylindrical
>syms r phi z
>Ar = cos(phi);
>Aphi = r;
>Az = -sin(phi);
>
>divA = (1/r)*diff(r*Ar, r) + (1/r)*diff(Aphi, phi) + diff(Az, z)
>```

---

## C) Curl

> **Given**  
> Vector field: $\mathbf A = \dfrac{\sin\theta \cos\phi}{R^2}\, \hat{\boldsymbol\theta}$  
>  
> Compute the curl $\nabla\times\mathbf A$ in spherical coordinates.

---

**Theory recap**

- Curl in spherical coordinates $(R, \theta, \phi)$:

$$
\begin{aligned}
(\nabla\times\mathbf A)_R &= \frac{1}{R\sin\theta}
\left(
\frac{\partial (\sin\theta A_\phi)}{\partial \theta}
- \frac{\partial A_\theta}{\partial \phi}
\right), \\[6pt]
(\nabla\times\mathbf A)_\theta &= \frac{1}{R}
\left(
\frac{1}{\sin\theta}\frac{\partial A_R}{\partial \phi}
- \frac{\partial (R A_\phi)}{\partial R}
\right), \\[6pt]
(\nabla\times\mathbf A)_\phi &= \frac{1}{R}
\left(
\frac{\partial (R A_\theta)}{\partial R}
- \frac{\partial A_R}{\partial \theta}
\right)
\end{aligned}
$$

- It measures the rotation of the field.

---

**Calculations**

Components:  
$A_R = 0$, $A_\theta = \dfrac{\sin\theta \cos\phi}{R^2}$, $A_\phi = 0$.

---

1️⃣ $R$–component:

$$
\frac{\partial A_\theta}{\partial \phi}
= \frac{\sin\theta(-\sin\phi)}{R^2}, \qquad
-\frac{\partial A_\theta}{\partial \phi}
= \frac{\sin\theta \sin\phi}{R^2}
$$

$$
(\nabla\times\mathbf A)_R
= \frac{1}{R\sin\theta} \cdot \frac{\sin\theta \sin\phi}{R^2}
= \frac{\sin\phi}{R^3}
$$

---

2️⃣ $\theta$–component:

$$
(\nabla\times\mathbf A)_\theta = 0
$$

---

3️⃣ $\phi$–component:

$$
R A_\theta = \frac{\sin\theta \cos\phi}{R}, \qquad
\frac{\partial (R A_\theta)}{\partial R}
= -\frac{\sin\theta \cos\phi}{R^2}
$$

$$
(\nabla\times\mathbf A)_\phi
= \frac{1}{R}\left(-\frac{\sin\theta \cos\phi}{R^2}\right)
= -\frac{\sin\theta \cos\phi}{R^3}
$$

---

So the curl is:
$$
\boxed{
\nabla\times\mathbf A
= \frac{\sin\phi}{R^3}\hat{\mathbf R}
- \frac{\sin\theta\cos\phi}{R^3}\hat{\boldsymbol\phi}
}
$$

---

**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.2(c) — Curl of A in spherical
>syms R theta phi
>AR = 0;
>Atheta = sin(theta)*cos(phi)/R^2;
>Aphi = 0;
>
>curlR = (1/(R*sin(theta))) * ( diff(sin(theta)*Aphi, theta) - diff(Atheta, phi) );
>curlTheta = (1/R) * ( (1/sin(theta))*diff(AR, phi) - diff(R*Aphi, R) );
>curlPhi = (1/R) * ( diff(R*Atheta, R) - diff(AR, theta) );
>
>[curlR, curlTheta, curlPhi]
>```

---
# 18.3 — Integral Forms of Maxwell’s Equations

---

## ⚡ Gauss’s Law: Electric Flux Through Closed Surface

> **Given**  
> Point charge $Q$ at origin in free space.  
>  
> Electrostatic field:  
> $$
> \mathbf E = \hat{\mathbf R}\,\frac{Q}{4\pi\varepsilon_0 R^2}
> $$
>  
> Show that the total flux of $\mathbf E$ through any surface enclosing the charge is $\dfrac{Q}{\varepsilon_0}$.

---

**Theory recap**

- Gauss’s law in integral form:  
  $$
  \oint_S \mathbf E \cdot d\mathbf a = \frac{Q_{\text{enc}}}{\varepsilon_0}
  $$
  where $S$ is any closed surface and $Q_{\text{enc}}$ is the enclosed charge.

- For a point charge, use spherical symmetry:  
  Choose a spherical surface of radius $R$ centered at the origin.

- On this surface, $\mathbf E$ is constant in magnitude and radial, so $\mathbf E \cdot d\mathbf a = E\,da$.

- Differential area element in spherical coordinates:  
  $$
  d\mathbf a = \hat{\mathbf R}\,R^2 \sin\theta\,d\theta\,d\phi
  $$

---

**Calculations**

1️⃣ **Flux integral:**

$$
\oint_S \mathbf E \cdot d\mathbf a
= \int_0^{2\pi} \int_0^{\pi}
\left(\frac{Q}{4\pi\varepsilon_0 R^2}\right)
R^2 \sin\theta\, d\theta\, d\phi
$$

Simplify:

$$
= \frac{Q}{4\pi\varepsilon_0}
\int_0^{2\pi} d\phi
\int_0^{\pi} \sin\theta\, d\theta
= \frac{Q}{4\pi\varepsilon_0} \cdot (2\pi)\cdot(2)
= \frac{Q}{\varepsilon_0}
$$

---

This holds for any enclosing surface by **Gauss’s theorem**, but a **spherical surface** simplifies the calculation.

$$
\boxed{
\oint_S \mathbf E \cdot d\mathbf a = \frac{Q}{\varepsilon_0}
}
$$

---

**Verification (optional in MATLAB/SymPy)**
>[!code]- matlab
>```matlab
>% 18.3(a) — Verify Gauss’s law for a point charge
>syms Q eps0 R theta phi positive
>
>% Electric field magnitude
>E_mag = Q / (4*pi*eps0*R^2);
>
>% Differential area element
>da = R^2 * sin(theta);
>
>% Flux integral
>flux = int(int(E_mag * da, theta, 0, pi), phi, 0, 2*pi);
>
>% Simplify and verify
>simplify(flux)  % Should be Q/eps0
>```

---

## ⚡ Ampere’s Law: Circulation of Magnetic Field

> **Given**  
> Steady current $I$ in infinite wire along z-axis at $(x,y)=(0,0)$.  
>  
> Magnetostatic field:  
> $$
> \mathbf B = \hat{\boldsymbol\phi}\,\frac{\mu_0 I}{2\pi r}, \quad \text{for } r>0
> $$
>  
> Show that the circulation of $\mathbf B$ around any closed loop enclosing the wire is $\mu_0 I$.

---

**Theory recap**

- Ampere’s law in integral form:  
  $$
  \oint_C \mathbf B \cdot d\boldsymbol\ell = \mu_0 I_{\text{encl}}
  $$
  where $C$ is a closed loop and $I_{\text{encl}}$ is the current enclosed by $C$.

- For an infinite straight wire, use **cylindrical symmetry**:  
  Choose a circular loop of radius $r$ in a plane perpendicular to the wire, centered on it.

- On this loop, $\mathbf B$ is constant in magnitude and tangential, so  
  $\mathbf B \cdot d\boldsymbol\ell = B\,d\ell$.

- Differential length element:  
  $$
  d\boldsymbol\ell = \hat{\boldsymbol\phi}\, r\, d\phi
  $$

- Direction follows the **right-hand rule**.

---

**Calculations**

1️⃣ **Circulation integral:**

$$
\oint_C \mathbf B \cdot d\boldsymbol\ell
= \int_0^{2\pi} \left( \frac{\mu_0 I}{2\pi r} \right) r\, d\phi
= \frac{\mu_0 I}{2\pi} \int_0^{2\pi} d\phi
= \frac{\mu_0 I}{2\pi} \cdot 2\pi
= \mu_0 I
$$

---

This holds for **any enclosing loop** by Ampere’s theorem, but the circular choice simplifies the calculation.

$$
\boxed{
\oint_C \mathbf B \cdot d\boldsymbol\ell = \mu_0 I
}
$$

---

**Verification (optional in MATLAB)**
>[!code]- matlab
>```matlab
>% 18.3(b) — Verify Ampere’s law for infinite wire (fixed version)
>% Note: 'I' is reserved for sqrt(-1) in MATLAB's symbolic engine.
>% Use I0 instead for the current.
>
>syms mu0 I0 r phi positive
>
>% Magnetic field magnitude
>B_mag = mu0 * I0 / (2*pi*r);
>
>% Differential length element (circumference segment)
>dL = r;
>
>% Circulation integral
>circ = int(B_mag * dL, phi, 0, 2*pi);
>
>% Simplify result
>simplify(circ)   % Should return mu0*I0
>```
