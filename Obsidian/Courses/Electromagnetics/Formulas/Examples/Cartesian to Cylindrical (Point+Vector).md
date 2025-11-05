---
title: Cartesian to Cylindrical (Point+Vector)
type: formula
tags: [electromagnetics, formula, examples, coordinate-systems]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05
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
