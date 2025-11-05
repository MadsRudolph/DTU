---

title: Coordinate Systems
type: formula
tags: [electromagnetics, formula, coordinate-systems]
aliases: []
links: {"formulas":[], "related":[]}
updated: 2025-11-05
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
> Use for problems with **point or spherical symmetry** - e.g., electric field of a point charge, or inside/outside a sphere.

---

> [!details]- 🔗 Related examples
> - [[Examples/Cartesian to Cylindrical (Point+Vector)]]
