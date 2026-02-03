---
title: Exercise 18 — Coordinate Systems and Vector Operators
type: exercise
tags: [Electromagnetics, exercises, coordinates, vector-operators]
aliases: []
links: {"formulas": ["[[MOC – Coordinate Systems]]","[[MOC – Vector Operators]]"], "related": ["[[MOC – Exercises]]","[[MOC – Electromagnetics]]"]}
updated: 2025-11-07
---
> Quick refs: [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]]  
> Important: vector component transforms in [[L18_Coordinate_Systems_Integrals_Differential_Space_Operators_Theorems.pdf]]

---

# Exercise 18.1 — Coordinate Systems & Components

In electrostatics and magnetostatics, we use three orthogonal coordinate systems:
Cartesian, cylindrical, and spherical. This exercise practices transforming both
points and vector components between these systems.

---

## 18.1 A) Cartesian → Cylindrical / Spherical

> **Given**  
> Point:  
> $$P(x,y,z) = (3,\,-1,\,2)$$  
> Vector (Cartesian components):  
> $$\mathbf A = 5\hat{\mathbf x} - 4\hat{\mathbf y} - \hat{\mathbf z}$$  
>
> (i) Express $P$ and $\mathbf A$ in **cylindrical** coordinates and components.  
> (ii) Express $P$ and $\mathbf A$ in **spherical** coordinates and components.

---

### (i) Cylindrical coordinates

**Theory**

Cylindrical coordinates:
$$
r = \sqrt{x^2 + y^2}, \qquad
\phi = \operatorname{atan2}(y,x), \qquad
z = z
$$

Unit vectors:
$$
\hat{\mathbf r} = \cos\phi\,\hat{\mathbf x} + \sin\phi\,\hat{\mathbf y}, \quad
\hat{\boldsymbol\phi} = -\sin\phi\,\hat{\mathbf x} + \cos\phi\,\hat{\mathbf y}, \quad
\hat{\mathbf z} = \hat{\mathbf z}
$$

Component transformation (Cartesian → cylindrical):
$$
\begin{aligned}
A_r   &= A_x\cos\phi + A_y\sin\phi,\\
A_\phi &= -A_x\sin\phi + A_y\cos\phi,\\
A_z   &= A_z
\end{aligned}
$$

**Point**

Given $x=3$, $y=-1$, $z=2$:
$$
r = \sqrt{3^2 + (-1)^2} = \sqrt{10} \approx 3.162
$$

For the azimuth:
$$
\phi = \operatorname{atan2}(-1,3) \approx -18.435^\circ
$$

We can equivalently use the angle in $[0,2\pi)$:
$$
\phi \approx 5.9614~\text{rad} \approx 341.6^\circ
$$

Thus:
$$
\boxed{P(r,\phi,z) = (3.162,\ 341.6^\circ,\ 2)}
$$

**Vector**

Use
$$
\cos\phi = \frac{x}{r} = \frac{3}{\sqrt{10}} \approx 0.94868, \qquad
\sin\phi = \frac{y}{r} = \frac{-1}{\sqrt{10}} \approx -0.31623
$$

Given $A_x = 5$, $A_y = -4$, $A_z = -1$:
$$
\begin{aligned}
A_r   &= 5\cdot 0.94868 + (-4)\cdot(-0.31623)
      \approx 4.7434 + 1.2649
      \approx 6.008,\\[4pt]
A_\phi &= -5\cdot(-0.31623) + (-4)\cdot 0.94868
      \approx 1.5811 - 3.7947
      \approx -2.214,\\[4pt]
A_z   &= -1
\end{aligned}
$$

So:
$$
\boxed{\mathbf A \approx 6.01\,\hat{\mathbf r} - 2.21\,\hat{\boldsymbol\phi} - 1.00\,\hat{\mathbf z}}
$$

> [!code]- MATLAB verification
> ```matlab
> % 18.1(a)(i) — Cylindrical components of A at P
> x = 3;  y = -1;  z = 2;
> A = [5, -4, -1];   % [Ax Ay Az]
>
> r   = hypot(x, y);
> phi = atan2(y, x);     % robust quadrant-safe phi
>
> c = x/r;
> s = y/r;
>
> Ar   = A(1)*c + A(2)*s;
> Aphi = -A(1)*s + A(2)*c;
> Az   = A(3);
>
> fprintf('r = %.6f\n', r);
> fprintf('phi = %.6f rad (%.3f deg)\n', phi, rad2deg(phi));
> fprintf('Ar   = %.6f\n', Ar);
> fprintf('Aphi = %.6f\n', Aphi);
> fprintf('Az   = %.6f\n', Az);
> ```

---

### (ii) Spherical coordinates

**Theory**

Spherical coordinates:
$$
R = \sqrt{x^2 + y^2 + z^2},\qquad
\theta = \arccos\left(\frac{z}{R}\right),\qquad
\phi = \operatorname{atan2}(y,x)
$$

Angle convention:

- $\theta$: polar angle from the $+z$-axis, $0 \le \theta \le \pi$  
- $\phi$: azimuth in the $xy$-plane from $+x$-axis.

Vector components (Cartesian → spherical):
$$
\begin{aligned}
A_R &= A_x\,\sin\theta\cos\phi + A_y\,\sin\theta\sin\phi + A_z\,\cos\theta,\\[4pt]
A_\theta &= A_x\,\cos\theta\cos\phi + A_y\,\cos\theta\sin\phi - A_z\,\sin\theta,\\[4pt]
A_\phi &= -A_x\,\sin\phi + A_y\,\cos\phi
\end{aligned}
$$

**Point**

$$
R = \sqrt{3^2 + (-1)^2 + 2^2} = \sqrt{14} \approx 3.742
$$
$$
\theta = \arccos\left(\frac{2}{\sqrt{14}}\right) \approx 1.007~\text{rad} \approx 57.69^\circ
$$
$$
\phi \approx 5.9614~\text{rad} \approx 341.6^\circ
$$

Thus:
$$
\boxed{P(R,\theta,\phi) = (3.742,\ 57.69^\circ,\ 341.6^\circ)}
$$

**Vector**

Using the same $\cos\phi, \sin\phi$ as above and
$$
\sin\theta \approx 0.8452,\qquad \cos\theta \approx 0.5345
$$

we obtain numerically:
$$
\boxed{
\mathbf A \approx 4.54\,\hat{\mathbf R} + 4.06\,\hat{\boldsymbol\theta} - 2.21\,\hat{\boldsymbol\phi}
}
$$

> [!code]- MATLAB helper (Cartesian → spherical)
> ```matlab
> % Cartesian → Spherical (point + vector)
> % theta: polar from +z, phi: azimuth from +x
> function [R,theta,phi,AR,Ath,Aphi] = cart2sph_vec(x,y,z,Ax,Ay,Az)
>   r = hypot(x,y);
>   R = hypot(r,z);
>
>   theta = atan2(r, z);      % robust [0,pi]
>   phi   = atan2(y, x);      % robust (-pi,pi]
>
>   cphi = x/max(r,eps);
>   sphi = y/max(r,eps);
>   sth  = r/max(R,eps);
>   cth  = z/max(R,eps);
>
>   AR   =  Ax*sth*cphi + Ay*sth*sphi + Az*cth;
>   Ath  =  Ax*cth*cphi + Ay*cth*sphi - Az*sth;
>   Aphi = -Ax*sphi     + Ay*cphi;
> end
> ```

---

## 18.1 B) Cylindrical → Cartesian / Spherical

> **Given**  
> Point:
> $$P(r,\phi,z) = (5,\ 3\pi/5,\ -2)$$
> Vector (cylindrical components):
> $$\mathbf A = 5\hat{\mathbf r} + 1\hat{\boldsymbol\phi} + 2\hat{\mathbf z}$$
>
> (i) Express $P$ and $\mathbf A$ in Cartesian coordinates and components.  
> (ii) Express $P$ and $\mathbf A$ in spherical coordinates and components.

---

### (i) Cartesian coordinates

**Theory**

$$
x = r\cos\phi,\qquad
y = r\sin\phi,\qquad
z = z
$$

Unit vectors:
$$
\hat{\mathbf r} = \cos\phi\,\hat{\mathbf x} + \sin\phi\,\hat{\mathbf y},\quad
\hat{\boldsymbol\phi} = -\sin\phi\,\hat{\mathbf x} + \cos\phi\,\hat{\mathbf y},\quad
\hat{\mathbf z} = \hat{\mathbf z}
$$

Component transformation (cylindrical → Cartesian):
$$
\begin{aligned}
A_x &= A_r\cos\phi - A_\phi\sin\phi,\\
A_y &= A_r\sin\phi + A_\phi\cos\phi,\\
A_z &= A_z
\end{aligned}
$$

**Point**

$$
\phi = \frac{3\pi}{5} = 108^\circ,\quad
\cos\phi \approx -0.3090,\quad
\sin\phi \approx 0.9511
$$

$$
x = 5\cos\phi \approx -1.545,\qquad
y = 5\sin\phi \approx 4.755,\qquad
z = -2
$$

Thus:
$$
\boxed{P(x,y,z) = (-1.545,\ 4.755,\ -2)}
$$

**Vector**

$$
\begin{aligned}
A_x &= 5(-0.3090) - 1(0.9511)
     \approx -1.545 - 0.9511
     \approx -2.496,\\[4pt]
A_y &= 5(0.9511) + 1(-0.3090)
     \approx 4.755 - 0.3090
     \approx 4.446,\\[4pt]
A_z &= 2
\end{aligned}
$$

So:
$$
\boxed{
\mathbf A \approx -2.50\,\hat{\mathbf x} + 4.45\,\hat{\mathbf y} + 2.00\,\hat{\mathbf z}
}
$$

> [!code]- MATLAB verification
> ```matlab
> % 18.1(b)(i) — Cylindrical → Cartesian
> r = 5; phi = 3*pi/5; z = -2;
> Ar = 5; Aphi = 1; Az = 2;
>
> x = r*cos(phi);
> y = r*sin(phi);
>
> Ax = Ar*cos(phi) - Aphi*sin(phi);
> Ay = Ar*sin(phi) + Aphi*cos(phi);
>
> fprintf('P = (%.3f, %.3f, %.3f)\n', x, y, z);
> fprintf('A = (%.3f, %.3f, %.3f)\n', Ax, Ay, Az);
> ```

---

### (ii) Spherical coordinates

**Theory**

For a point given by $(r,\phi,z)$:
$$
R = \sqrt{r^2 + z^2},\qquad
\theta = \arccos\left(\frac{z}{R}\right),\qquad
\phi = \phi
$$

Cylindrical → spherical vector components:
$$
\begin{aligned}
A_R      &= \sin\theta\,A_r + \cos\theta\,A_z,\\
A_\theta &= \cos\theta\,A_r - \sin\theta\,A_z,\\
A_\phi   &= A_\phi
\end{aligned}
$$

**Point**

$$
R = \sqrt{5^2 + (-2)^2} = \sqrt{29} \approx 5.385
$$
$$
\theta = \arccos\left(\frac{-2}{\sqrt{29}}\right)
\approx 1.951~\text{rad} \approx 111.8^\circ
$$
$$
\phi = 108^\circ
$$

Thus:
$$
\boxed{P(R,\theta,\phi) = (5.385,\ 111.8^\circ,\ 108^\circ)}
$$

**Vector**

$$
\sin\theta = \frac{r}{R} \approx \frac{5}{5.385} \approx 0.9285,\qquad
\cos\theta = \frac{z}{R} \approx \frac{-2}{5.385} \approx -0.3714
$$

Given $A_r = 5$, $A_z = 2$, $A_\phi = 1$:
$$
\begin{aligned}
A_R      &= 0.9285\cdot 5 + (-0.3714)\cdot 2
         \approx 4.642 - 0.743 \approx 3.900,\\[4pt]
A_\theta &= -0.3714\cdot 5 - 0.9285\cdot 2
         \approx -1.857 - 1.857 \approx -3.714,\\[4pt]
A_\phi   &= 1
\end{aligned}
$$

So:
$$
\boxed{
\mathbf A \approx 3.90\,\hat{\mathbf R} - 3.71\,\hat{\boldsymbol\theta} + 1.00\,\hat{\boldsymbol\phi}
}
$$

> [!code]- MATLAB verification
> ```matlab
> r = 5; z = -2;
> Ar = 5; Aphi = 1; Az = 2;
>
> R = hypot(r, z);
> theta = acos(z/R);
> sth = r/R;  cth = z/R;
>
> AR    = sth*Ar + cth*Az;
> Athet = cth*Ar - sth*Az;
> % Aphi = Aphi
>
> fprintf('R = %.3f, theta = %.3f rad (%.3f deg)\n', ...
>         R, theta, rad2deg(theta));
> fprintf('AR = %.3f, Atheta = %.3f, Aphi = %.3f\n', AR, Athet, Aphi);
> ```

---

## 18.1 C) Spherical → Cartesian / Cylindrical

> **Given**  
> Point:
> $$P(R,\theta,\phi) = (3,\ \pi/3,\ \pi/5)$$
> Vector (spherical components):
> $$\mathbf A = 3\hat{\boldsymbol\theta} - \hat{\boldsymbol\phi}
> \quad\text{(i.e. } A_R = 0,\ A_\theta = 3,\ A_\phi = -1\text{)}$$
>
> (i) Express $P$ and $\mathbf A$ in Cartesian coordinates and components.  
> (ii) Express $P$ and $\mathbf A$ in cylindrical coordinates and components.

---

### (i) Cartesian coordinates

**Theory**

$$
x = R\sin\theta\cos\phi,\quad
y = R\sin\theta\sin\phi,\quad
z = R\cos\theta
$$

Spherical → Cartesian vector components:
$$
\begin{aligned}
A_x &= \sin\theta\cos\phi\,A_R + \cos\theta\cos\phi\,A_\theta - \sin\phi\,A_\phi,\\[4pt]
A_y &= \sin\theta\sin\phi\,A_R + \cos\theta\sin\phi\,A_\theta + \cos\phi\,A_\phi,\\[4pt]
A_z &= \cos\theta\,A_R - \sin\theta\,A_\theta
\end{aligned}
$$

**Point**

$$
R = 3,\quad
\theta = \frac{\pi}{3} = 60^\circ,\quad
\phi = \frac{\pi}{5} = 36^\circ
$$

$$
\sin\theta \approx 0.8660,\quad
\cos\theta = 0.5,\quad
\cos\phi \approx 0.8090,\quad
\sin\phi \approx 0.5878
$$

$$
x = 3\cdot 0.8660 \cdot 0.8090 \approx 2.102,\qquad
y = 3\cdot 0.8660 \cdot 0.5878 \approx 1.527,\qquad
z = 3\cdot 0.5 = 1.5
$$

Thus:
$$
\boxed{P(x,y,z) = (2.102,\ 1.527,\ 1.5)}
$$

**Vector**

$$
\begin{aligned}
A_x &= 0\cdot(\sin\theta\cos\phi)
    + 3\cdot(0.5\cdot 0.8090)
    - (-1)\cdot 0.5878
    \approx 1.214 + 0.588 \approx 1.802,\\[4pt]
A_y &= 0\cdot(\sin\theta\sin\phi)
    + 3\cdot(0.5\cdot 0.5878)
    + (-1)\cdot 0.8090
    \approx 0.882 - 0.809 \approx 0.073,\\[4pt]
A_z &= 0\cdot 0.5 - 3\cdot 0.8660
    \approx -2.598
\end{aligned}
$$

So:
$$
\boxed{
\mathbf A \approx 1.80\,\hat{\mathbf x} + 0.07\,\hat{\mathbf y} - 2.60\,\hat{\mathbf z}
}
$$

---

### (ii) Cylindrical coordinates

**Theory**

From spherical:
$$
r = R\sin\theta,\quad
\phi = \phi,\quad
z = R\cos\theta
$$

Spherical → cylindrical vector components:
$$
\begin{aligned}
A_r &= \sin\theta\,A_R + \cos\theta\,A_\theta,\\
A_\phi &= A_\phi,\\
A_z &= \cos\theta\,A_R - \sin\theta\,A_\theta
\end{aligned}
$$

**Point**

$$
r = 3\cdot 0.8660 \approx 2.598,\quad
\phi = 36^\circ,\quad
z = 1.5
$$

Thus:
$$
\boxed{P(r,\phi,z) = (2.598,\ 36^\circ,\ 1.5)}
$$

**Vector**

$$
\begin{aligned}
A_r &= \sin\theta\,A_R + \cos\theta\,A_\theta
     = 0.8660\cdot 0 + 0.5\cdot 3 = 1.5,\\[4pt]
A_\phi &= A_\phi = -1,\\[4pt]
A_z &= \cos\theta\,A_R - \sin\theta\,A_\theta
     = 0.5\cdot 0 - 0.8660\cdot 3 \approx -2.598
\end{aligned}
$$

So:
$$
\boxed{
\mathbf A \approx 1.50\,\hat{\mathbf r} - 1.00\,\hat{\boldsymbol\phi} - 2.60\,\hat{\mathbf z}
}
$$

---

# Exercise 18.2 — Vector Differential Operators

We consider three operators:

- Gradient $\nabla V$ (acts on scalar fields → vector)  
- Divergence $\nabla\cdot\mathbf A$ (acts on vector fields → scalar)  
- Curl $\nabla\times\mathbf A$ (acts on vector fields → vector)

They are fundamental for relating local (differential) and global (integral) forms of Maxwell’s equations.

---

## 18.2 A) Gradient

> **Given**  
> Scalar field:
> $$V(x,y,z) = -x + 2yx + 2z^2$$
> Compute $\nabla V$ in Cartesian coordinates.

**Theory**

In Cartesian coordinates:
$$
\nabla V =
\frac{\partial V}{\partial x}\hat{\mathbf x}
+ \frac{\partial V}{\partial y}\hat{\mathbf y}
+ \frac{\partial V}{\partial z}\hat{\mathbf z}
$$

**Calculation**

$$
\frac{\partial V}{\partial x} = -1 + 2y,\qquad
\frac{\partial V}{\partial y} = 2x,\qquad
\frac{\partial V}{\partial z} = 4z
$$

Thus:
$$
\boxed{
\nabla V = (2y - 1)\hat{\mathbf x} + 2x\hat{\mathbf y} + 4z\hat{\mathbf z}
}
$$

---

## 18.2 B) Divergence (cylindrical)

> **Given**  
> Vector field in cylindrical coordinates:
> $$\mathbf A = \cos\phi\,\hat{\mathbf r} + r\,\hat{\boldsymbol\phi} - \sin\phi\,\hat{\mathbf z}$$
> Compute $\nabla\cdot\mathbf A$ in cylindrical coordinates.

**Theory**

In cylindrical $(r,\phi,z)$:
$$
\nabla\cdot\mathbf A =
\frac{1}{r}\frac{\partial(rA_r)}{\partial r}
+ \frac{1}{r}\frac{\partial A_\phi}{\partial\phi}
+ \frac{\partial A_z}{\partial z}
$$

**Calculation**

Components:
$$
A_r = \cos\phi,\qquad
A_\phi = r,\qquad
A_z = -\sin\phi
$$

Then:
$$
\frac{1}{r}\frac{\partial(rA_r)}{\partial r}
= \frac{1}{r}\frac{\partial(r\cos\phi)}{\partial r}
= \frac{\cos\phi}{r}
$$
$$
\frac{1}{r}\frac{\partial A_\phi}{\partial\phi}
= \frac{1}{r}\frac{\partial r}{\partial\phi} = 0,\qquad
\frac{\partial A_z}{\partial z}
= \frac{\partial(-\sin\phi)}{\partial z} = 0
$$

So:
$$
\boxed{
\nabla\cdot\mathbf A = \frac{\cos\phi}{r}
}
$$

---

## 18.2 C) Curl (spherical)

> **Given**  
> Vector field in spherical coordinates:
> $$\mathbf A = \hat{\boldsymbol\theta}\,\frac{\sin\theta\cos\phi}{R^2}$$
> Compute $\nabla\times\mathbf A$ in spherical coordinates.

**Theory**

In spherical $(R,\theta,\phi)$:
$$
\begin{aligned}
(\nabla\times\mathbf A)_R &= \frac{1}{R\sin\theta}
\left(
\frac{\partial(\sin\theta A_\phi)}{\partial\theta}
- \frac{\partial A_\theta}{\partial\phi}
\right),\\[4pt]
(\nabla\times\mathbf A)_\theta &= \frac{1}{R}
\left(
\frac{1}{\sin\theta}\frac{\partial A_R}{\partial\phi}
- \frac{\partial(RA_\phi)}{\partial R}
\right),\\[4pt]
(\nabla\times\mathbf A)_\phi &= \frac{1}{R}
\left(
\frac{\partial(RA_\theta)}{\partial R}
- \frac{\partial A_R}{\partial\theta}
\right)
\end{aligned}
$$

Here:
$$
A_R = 0,\quad
A_\theta = \frac{\sin\theta\cos\phi}{R^2},\quad
A_\phi = 0
$$

**Calculation**

1. $R$–component:
$$
\frac{\partial A_\theta}{\partial\phi}
= \frac{\sin\theta(-\sin\phi)}{R^2},
\quad
-\frac{\partial A_\theta}{\partial\phi}
= \frac{\sin\theta\sin\phi}{R^2}
$$

$$
(\nabla\times\mathbf A)_R
= \frac{1}{R\sin\theta}\cdot\frac{\sin\theta\sin\phi}{R^2}
= \frac{\sin\phi}{R^3}
$$

2. $\theta$–component:
$$
(\nabla\times\mathbf A)_\theta = 0
$$

3. $\phi$–component:
$$
R A_\theta = \frac{\sin\theta\cos\phi}{R},\qquad
\frac{\partial(RA_\theta)}{\partial R}
= -\frac{\sin\theta\cos\phi}{R^2}
$$

$$
(\nabla\times\mathbf A)_\phi
= \frac{1}{R}\left(-\frac{\sin\theta\cos\phi}{R^2}\right)
= -\frac{\sin\theta\cos\phi}{R^3}
$$

Hence:
$$
\boxed{
\nabla\times\mathbf A
= \frac{\sin\phi}{R^3}\,\hat{\mathbf R}
- \frac{\sin\theta\cos\phi}{R^3}\,\hat{\boldsymbol\phi}
}
$$

---

# Exercise 18.3 — Integral Forms of Maxwell’s Equations

We now connect the differential fields to integral quantities via Gauss’s and Ampere’s laws.

---

## 18.3 A) Gauss’s Law — Electric Flux of a Point Charge

> **Given**  
> A point charge $Q$ at rest at the origin in free space.  
> The electrostatic field is
> $$\mathbf E = \hat{\mathbf R}\,\frac{Q}{4\pi\varepsilon_0 R^2}$$
> where $R$ is the spherical radial coordinate.  
> Show that the total flux of $\mathbf E$ through any surface enclosing the charge equals $Q/\varepsilon_0$.

**Theory**

Gauss’s law in integral form:
$$
\oint_S \mathbf E\cdot d\mathbf a = \frac{Q_{\text{enc}}}{\varepsilon_0}
$$

Because the field is spherically symmetric, choose a sphere of radius $R$ centered on the charge. On this surface:

- $\mathbf E$ is radial and constant in magnitude  
- $d\mathbf a = \hat{\mathbf R}\,R^2\sin\theta\,d\theta\,d\phi$

**Calculation**

$$
\begin{aligned}
\oint_S \mathbf E\cdot d\mathbf a
&= \int_0^{2\pi}\int_0^\pi
\frac{Q}{4\pi\varepsilon_0 R^2}
\,\hat{\mathbf R}\cdot\hat{\mathbf R}\,
R^2\sin\theta\,d\theta\,d\phi\\[4pt]
&= \frac{Q}{4\pi\varepsilon_0}
\int_0^{2\pi}\int_0^\pi \sin\theta\,d\theta\,d\phi\\[4pt]
&= \frac{Q}{4\pi\varepsilon_0}\,(2\pi)\,(2)
= \frac{Q}{\varepsilon_0}
\end{aligned}
$$

Thus:
$$
\boxed{
\oint_S \mathbf E\cdot d\mathbf a = \frac{Q}{\varepsilon_0}
}
$$

---

## 18.3 B) Ampere’s Law — Circulation of $\mathbf B$ around a Wire

> **Given**  
> A steady current $I$ flows in an infinitely long, thin wire along the $z$-axis at $(x,y)=(0,0)$.  
> The magnetostatic field in free space is
> $$\mathbf B = \hat{\boldsymbol\phi}\,\frac{\mu_0 I}{2\pi r}, \quad r>0$$
> where $r$ is the cylindrical radial coordinate.  
> Show that the circulation of $\mathbf B$ around any loop enclosing the wire is $\mu_0 I$.

**Theory**

Ampere’s law (static form):
$$
\oint_C \mathbf B\cdot d\boldsymbol\ell = \mu_0 I_{\text{encl}}
$$

By symmetry, choose a circular path of radius $r$ in a plane perpendicular to the wire, centered on the wire:

- $\mathbf B$ is tangential ($\hat{\boldsymbol\phi}$) and constant in magnitude  
- $d\boldsymbol\ell = \hat{\boldsymbol\phi}\,r\,d\phi$

**Calculation**

$$
\begin{aligned}
\oint_C \mathbf B\cdot d\boldsymbol\ell
&= \int_0^{2\pi}
\left(\frac{\mu_0 I}{2\pi r}\right)
\hat{\boldsymbol\phi}\cdot\hat{\boldsymbol\phi}\, r\,d\phi\\[4pt]
&= \frac{\mu_0 I}{2\pi}\int_0^{2\pi} d\phi\\[4pt]
&= \frac{\mu_0 I}{2\pi}\cdot 2\pi
= \mu_0 I
\end{aligned}
$$

Thus:
$$
\boxed{
\oint_C \mathbf B\cdot d\boldsymbol\ell = \mu_0 I
}
$$

This matches Ampere’s law for any closed loop enclosing the current, with the right-hand rule relating the direction of $\mathbf B$ and the current $I$.

---


