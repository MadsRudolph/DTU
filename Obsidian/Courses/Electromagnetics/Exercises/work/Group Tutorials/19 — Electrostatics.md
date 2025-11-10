> Quick refs: [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]]
---

# 19 — Electrostatics I
## ⚡ Exercise 19.1  
### Coulomb’s Law: Force Between Two Point Charges
> **Given**  
> Two point charges in free space:  
> - $Q_1$ at $P_1(2,\ -4,\ 1)$ nm  
> - $Q_2$ at $P_2(1,\ 1,\ -5)$ nm  
>  
> Calculate the electrostatic force they exert on each other and determine if it is **repulsive** or **attractive** for:  
> - (a) $Q_1 = 2Q_2 = 2$ fC  
> - (b) $Q_1 = -2Q_2 = 2$ fC  

---
### 🧠 Theory recap  
> (L19 slides 12–15, Ulaby Ch.4.2, Solution PDF ver. 2025.11.10)  

In electrostatics, we consider charges at rest. There are no currents, since they describe a flow of moving charges.  

**Coulomb’s law** for two point charges:  
$$
\mathbf{F}_{12}=Q_1\mathbf{E}_2(\mathbf{R}=\mathbf{R}_1)=
\frac{Q_1Q_2}{4\pi\varepsilon_0}
\frac{\mathbf{R}_1-\mathbf{R}_2}{|\mathbf{R}_1-\mathbf{R}_2|^3}
=-\mathbf{F}_{21}
$$
where $\mathbf{E}_2(\mathbf{R}=\mathbf{R}_1)$ is the electrostatic field from $Q_2$ evaluated at the position of $Q_1$,  
$\mathbf{R}=\mathbf{R}_1=\begin{pmatrix}2\\-4\\1\end{pmatrix}^\text{T}$ nm.  
The position of $Q_2$ is at $\mathbf{R}=\mathbf{R}_2=\begin{pmatrix}1\\1\\-5\end{pmatrix}^\text{T}$ nm.  

- The force on $Q_1$ ($Q_2$) due to $Q_2$ ($Q_1$) is denoted $\mathbf{F}_{12}$ ($\mathbf{F}_{21}$).  
- Newton’s third law: $\mathbf{F}_{12}=-\mathbf{F}_{21}$.  
- **Repulsive** when charges have the same sign, **attractive** when opposite.  
- To find out if the force is attractive or repulsive, we just have to check if the force points in the same direction as the vector $\mathbf{R}_1\to\mathbf{R}_2$ for $\mathbf{F}_{12}$ (or $\mathbf{R}_2\to\mathbf{R}_1$ for $\mathbf{F}_{21}$). One can take the dot product of the vectors and check the sign (positive = repulsive, negative = attractive). As expected, the force is attractive when the charges are not the same type (positive-negative) and repulsive when they are the same (positive-positive or negative-negative).

---
### ⚙️ Calculations  
#### 1️⃣ Separation vectors (nm):  
$$
\mathbf{R}_1\to\mathbf{R}_2=(\mathbf{R}_2-\mathbf{R}_1)=
\begin{pmatrix}-1\\5\\-6\end{pmatrix},\qquad
\mathbf{R}_2\to\mathbf{R}_1=
\begin{pmatrix}1\\-5\\6\end{pmatrix}
$$
with $|\mathbf{R}_1\to\mathbf{R}_2|=\sqrt{62}\approx7.874$ nm.  

#### 2️⃣ Common prefactor:  
$$
\frac{1}{4\pi\varepsilon_0|\mathbf{R}_1\to\mathbf{R}_2|^3}
\approx1.841\times10^{11}~\text{N/C}^2
$$

#### (a) $Q_1 = 2$ fC, $Q_2 = 1$ fC (both positive)  
$$
\mathbf{F}_{12}=(2\times10^{-15})(1\times10^{-15})\cdot1.841\times10^{11}
\begin{pmatrix}-1\\5\\-6\end{pmatrix}
\approx
\begin{pmatrix}-36.82\\184.1\\-220.9\end{pmatrix}~\mu\text{N}
$$
$$
\mathbf{F}_{21}=-\mathbf{F}_{12}
\approx
\begin{pmatrix}36.82\\-184.1\\220.9\end{pmatrix}~\mu\text{N}
$$
Strength: $|\mathbf{F}_{12}|=|\mathbf{F}_{21}|\approx290~\mu\text{N}$.  
Dot product $\mathbf{F}_{12}\cdot(\mathbf{R}_1\to\mathbf{R}_2)>0$ → **repulsive**.  
In this case, the force is repulsive.

#### (b) $Q_1 = -2$ fC, $Q_2 = 1$ fC (opposite signs)  
We reuse the expression for the force, but with the charges specified above:  
$$
\mathbf{F}_{12}
\approx
\begin{pmatrix}36.82\\-184.1\\220.9\end{pmatrix}~\mu\text{N},\qquad
\mathbf{F}_{21}
\approx
\begin{pmatrix}-36.82\\184.1\\-220.9\end{pmatrix}~\mu\text{N}
$$
Same magnitude, opposite direction. The result is an **attractive** force.

$$
\boxed{
\begin{array}{c|c|c}
\text{case} & \mathbf{F}_{12}~(\mu\text{N}) & \text{nature} \\
\hline
\text{(a)} & (-36.82,\ 184.1,\ -220.9) & \text{repulsive} \\
\text{(b)} & (36.82,\ -184.1,\ 220.9) & \text{attractive}
\end{array}
}
$$

---
### ✅ Verification (MATLAB)
>[!code]- matlab
>```matlab
>% 19.1 — Coulomb force (exact match with solution)
>ke = 8.99e9; R = sqrt(62)*1e-9;
>dR12 = [-1; 5; -6]*1e-9;  % R1→R2
>
>% (a)
>F12a = ke*(2e-15)*(1e-15)/R^2 * (dR12/R) *1e6
>F21a = -F12a
>
>% (b)
>F12b = ke*(-2e-15)*(1e-15)/R^2 * (dR12/R) *1e6
>```

---

## ⚡ Exercise 19.2  
### Three Point Charges in Triangular Configuration
> **Given**  
> Three equally distanced point charges in free space, $Q_1=Q_2=Q$ and $Q_3$, forming a triangular configuration.  
> The Cartesian (xyz) and spherical (Rθφ) coordinate systems are introduced with the **origin located at the center** of the configuration.  
> The charges are located in the xy-plane with $Q_3$ being on the x-axis at $x=R_q$.  

#### (a) Sketch the configuration.
---
### 🧠 Theory recap  
> (L19 slides 25–27, Ulaby Ch.4.3, Solution PDF)  

- Superposition principle applies.  
- Equilateral triangle → 120° rotational symmetry.  
- Distance between any two charges: $R_q\sqrt{3}$.  
- Origin at centroid → simplifies force calculations (net force on $Q_3$ along x-axis).

### Sketch (recreated from Solution PDF)
```
          Q1
           o
          / \
   120° /     \ 120°
       /       \
      o---------o
     Q2    R_q   Q3  → +x
          ^
        origin (center)
```

Positions (nm):  
- $Q_3$: $(R_q,\ 0,\ 0)$  
- $Q_1$: $(-0.5R_q,\ \sqrt{3}/2\,R_q,\ 0)$  
- $Q_2$: $(-0.5R_q,\ -\sqrt{3}/2\,R_q,\ 0)$  

$$
\boxed{\text{Equilateral triangle in xy-plane, origin at centroid, } Q_3 \text{ at } (R_q,0,0)}
$$

---

### Summary Table
| Exercise | Key Concept | Main Result |
|----------|-------------|-------------|
| 19.1 (a) | Coulomb’s law, same sign | Repulsive, 290 μN |
| 19.1 (b) | Opposite signs | Attractive, same magnitude |
| 19.2 (a) | Symmetry, centroid origin | Sketch with $Q_3$ on +x-axis |
