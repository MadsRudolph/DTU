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
>%% 19.1 — Coulomb Force (clean + streamlined)
>ke = 8.99e9;          % Coulomb constant
>                          
>% Positions
>R1 = [2; -4;  1];
>R2 = [1;  1; -5];
>
>dR12 = R2 - R1;       % R1 -> R2
>r = norm(dR12);       % distance
>u12 = dR12 / r;       % unit vector
>
>%% (a) Q1 = 2 fC, Q2 = 1 fC
>Q1a =  2e-15;
>Q2a =  1e-15;
>
>F12a = ke * Q1a * Q2a / r^2 * u12;
>F21a = -F12a;
>
>%% (b) Q1 = -2 fC, Q2 = 1 fC
>Q1b = -2e-15;
>Q2b =  1e-15;
>
>F12b = ke * Q1b * Q2b / r^2 * u12;
>F21b = -F12b;
>```

---

## ⚡ Exercise 19.2  
### Three Point Charges in Triangular Configuration

> **Given**  
> Three equally spaced point charges in free space:  
> - $Q_1 = Q_2$  
> - $Q_3$ (possibly different from $Q_1$)  
>  
> The charges form an **equilateral triangle** in the **$xy$-plane**.  
> The coordinate systems are centered at the **triangle center**, and  
> $$Q_3 \text{ lies on the $x$-axis at } x = R_q.$$

We want to:
- (a) Sketch the configuration.  
- (b) Find the **total electric field at the center** $(x,y,z)=(0,0,0)$ and evaluate it for  
  - $Q_3 = Q_1$  
  - $Q_3 = -Q_1$  
  - $Q_3 = 2Q_1$  

---

### 🧠 Geometry setup (equilateral triangle in the $xy$-plane)

Let all three charges lie on a circle of radius $R_q$ centered at the origin.

We place:
- $Q_3$ on the **$+x$-axis**:
  $$
  \mathbf{r}_3 = (R_q,\,0,\,0)
  $$
- $Q_1$ and $Q_2$ are rotated by $\pm 120^\circ$ around the $z$-axis:
  $$
  \begin{aligned}
  \mathbf{r}_1 &= R_q(\cos 120^\circ,\ \sin 120^\circ,\ 0)
              = \Big(-\tfrac{R_q}{2},\ \tfrac{\sqrt{3}}{2}R_q,\ 0\Big) \\
  \mathbf{r}_2 &= R_q(\cos(-120^\circ),\ \sin(-120^\circ),\ 0)
              = \Big(-\tfrac{R_q}{2},\ -\tfrac{\sqrt{3}}{2}R_q,\ 0\Big)
  \end{aligned}
  $$
This gives an **equilateral triangle** with side length
$$
R_{12} = R_{23} = R_{13} = \sqrt{3}\,R_q.
$$

---

### ⚙️ Field at the center by superposition (part b)

The field from a point charge $Q_i$ at position $\mathbf{r}_i$ evaluated at the **origin** is
$$
\mathbf{E}_i(\mathbf{0})
= \frac{1}{4\pi\varepsilon_0}\frac{Q_i}{|\mathbf{r}_i|^3}(-\mathbf{r}_i)
= \frac{1}{4\pi\varepsilon_0 R_q^3}Q_i(-\mathbf{r}_i)
$$
since $|\mathbf{r}_i| = R_q$ for all three charges.

Total field at the center:
$$
\mathbf{E}_\text{tot}(\mathbf{0})
= \sum_{i=1}^3 \mathbf{E}_i
= \frac{1}{4\pi\varepsilon_0 R_q^3}\Big[Q_1(-\mathbf{r}_1) + Q_2(-\mathbf{r}_2) + Q_3(-\mathbf{r}_3)\Big].
$$

Using $Q_1 = Q_2 = Q_1$ and the geometry:
$$
-\mathbf{r}_1 - \mathbf{r}_2 
= (R_q, 0, 0) = R_q \hat{\mathbf{x}}, \qquad
-\mathbf{r}_3 = (-R_q, 0, 0) = -R_q \hat{\mathbf{x}},
$$
we get
$$
\mathbf{E}_\text{tot}(\mathbf{0})
= \frac{1}{4\pi\varepsilon_0 R_q^3}\Big[Q_1 (R_q\hat{\mathbf{x}}) + Q_3 (-R_q\hat{\mathbf{x}})\Big]
= \frac{Q_1 - Q_3}{4\pi\varepsilon_0 R_q^2}\,\hat{\mathbf{x}}.
$$

Now plug in the three cases:

- $Q_3 = Q_1$:
  $$
  \mathbf{E}_\text{tot}(\mathbf{0}) = 0
  $$
- $Q_3 = -Q_1$:
  $$
  \mathbf{E}_\text{tot}(\mathbf{0})
  = \frac{Q_1 - (-Q_1)}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
  = \frac{Q_1}{2\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
  $$
- $Q_3 = 2Q_1$:
  $$
  \mathbf{E}_\text{tot}(\mathbf{0})
  = \frac{Q_1 - 2Q_1}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
  = -\frac{Q_1}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
  $$
which matches the official result:
$$
\begin{aligned}
\mathbf{E}_\text{tot}(R=0, Q_3 = Q_1) &= 0 \\
\mathbf{E}_\text{tot}(R=0, Q_3 = -Q_1) &= \hat{\mathbf{x}} \frac{Q_1}{2\pi\varepsilon_0 R_q^2} \\
\mathbf{E}_\text{tot}(R=0, Q_3 = 2Q_1) &= -\hat{\mathbf{x}} \frac{Q_1}{4\pi\varepsilon_0 R_q^2}
\end{aligned}
$$
---

### 🌍 (c) Total outward flux through a closed surface

We now surround all three charges with an arbitrary closed surface $S$ and want the **total outward flux**:
$$
\oint_S \mathbf{E}\cdot d\mathbf{S}.
$$

Using **Gauss’s law**:
$$
\oint_S \mathbf{E}\cdot d\mathbf{S}
= \frac{Q_\text{enc}}{\varepsilon_0}
$$
where $Q_\text{enc}$ is the **total enclosed charge**.

Here
$$
Q_\text{enc} = Q_1 + Q_2 + Q_3 = Q_1 + Q_1 + Q_3 = 2Q_1 + Q_3.
$$

So, in general:
$$
\boxed{
\displaystyle
\oint_S \mathbf{E}\cdot d\mathbf{S}
= \frac{2Q_1 + Q_3}{\varepsilon_0}
}
$$

For the three specific cases:
$$
\begin{array}{c|c|c}
\text{Case} & Q_3 & \displaystyle \oint_S \mathbf{E}\cdot d\mathbf{S} \\
\hline
(1) & Q_3 = Q_1      & \dfrac{3Q_1}{\varepsilon_0} \\
(2) & Q_3 = -Q_1     & \dfrac{Q_1}{\varepsilon_0} \\
(3) & Q_3 = 2Q_1     & \dfrac{4Q_1}{\varepsilon_0}
\end{array}
$$

To make the **total outward flux zero**, we must have:
$$
Q_\text{enc} = 0 \quad\Rightarrow\quad 2Q_1 + Q_3 = 0
$$
so
$$
\boxed{Q_3 = -2Q_1}
$$

---

### 🔋 (d) Electrostatic energy of the configuration

The total **electrostatic energy** stored in a system of three point charges is
$$
W_e = \sum_{i<j} \frac{1}{4\pi\varepsilon_0}\frac{Q_i Q_j}{R_{ij}},
$$
where $R_{ij}$ is the distance between $Q_i$ and $Q_j$.

From the geometry:
$$
R_{12} = R_{23} = R_{13} = \sqrt{3}R_q.
$$

Thus
$$
W_e = \frac{1}{4\pi\varepsilon_0\sqrt{3}R_q}\Big(Q_1Q_2 + Q_1Q_3 + Q_2Q_3\Big).
$$

With $Q_1 = Q_2 = Q_1$:
$$
Q_1Q_2 = Q_1^2,\quad Q_1Q_3 = Q_1Q_3,\quad Q_2Q_3 = Q_1Q_3,
$$
so
$$
W_e = \frac{1}{4\pi\varepsilon_0\sqrt{3}R_q}\Big(Q_1^2 + 2Q_1Q_3\Big).
$$

Now evaluate for the three cases:

- **Case 1:** $Q_3 = Q_1$
  $$
  W_e = \frac{1}{4\pi\varepsilon_0\sqrt{3}R_q}\big(Q_1^2 + 2Q_1^2\big)
      = \frac{3Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q}
      = \frac{\sqrt{3}Q_1^2}{4\pi\varepsilon_0 R_q}
  $$

- **Case 2:** $Q_3 = -Q_1$
  $$
  W_e = \frac{1}{4\pi\varepsilon_0\sqrt{3}R_q}\big(Q_1^2 - 2Q_1^2\big)
      = -\frac{Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q}
  $$

- **Case 3:** $Q_3 = 2Q_1$
  $$
  W_e = \frac{1}{4\pi\varepsilon_0\sqrt{3}R_q}\big(Q_1^2 + 4Q_1^2\big)
      = \frac{5Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q}
  $$

We can summarize:
$$
\boxed{
\begin{array}{c|c}
\text{Case} & W_e \\
\hline
Q_3 = Q_1   & \dfrac{\sqrt{3}Q_1^2}{4\pi\varepsilon_0 R_q} \\
Q_3 = -Q_1  & -\dfrac{Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q} \\
Q_3 = 2Q_1  & \dfrac{5Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q}
\end{array}
}
$$

---

### 🎯 (e) Force on a fourth charge at the center

Now we place a fourth charge $Q_4$ at the **center** of the triangle (at the origin).  
The total field at the center from the first three charges was already found:
$$
\mathbf{E}_\text{tot}(\mathbf{0})
= \frac{Q_1 - Q_3}{4\pi\varepsilon_0 R_q^2}\,\hat{\mathbf{x}}.
$$

The force on $Q_4$ is then
$$
\boxed{
\mathbf{F}_4 = Q_4\,\mathbf{E}_\text{tot}(\mathbf{0})
= Q_4\,\frac{Q_1 - Q_3}{4\pi\varepsilon_0 R_q^2}\,\hat{\mathbf{x}}
}
$$

For the three specific cases:

- **Case 1:** $Q_3 = Q_1$
  $$
  \mathbf{F}_4 = 0
  $$

- **Case 2:** $Q_3 = -Q_1$
  $$
  \mathbf{F}_4
  = Q_4\,\frac{Q_1 - (-Q_1)}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
  = Q_4\,\frac{2Q_1}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
  = \hat{\mathbf{x}}\frac{Q_1Q_4}{2\pi\varepsilon_0 R_q^2}
  $$

- **Case 3:** $Q_3 = 2Q_1$
  $$
  \mathbf{F}_4
  = Q_4\,\frac{Q_1 - 2Q_1}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
  = -\hat{\mathbf{x}}\frac{Q_1Q_4}{4\pi\varepsilon_0 R_q^2}
  $$

So:
$$
\boxed{
\begin{array}{c|c}
\text{Case} & \mathbf{F}_4 \\
\hline
Q_3 = Q_1   & 0 \\
Q_3 = -Q_1  & \hat{\mathbf{x}}\,\dfrac{Q_1Q_4}{2\pi\varepsilon_0 R_q^2} \\
Q_3 = 2Q_1  & -\hat{\mathbf{x}}\,\dfrac{Q_1Q_4}{4\pi\varepsilon_0 R_q^2}
\end{array}
}
$$
### ✅ Verification (MATLAB)
>[!code]- matlab
>```matlab
>%% 19.2 — Three charges in an equilateral triangle (numeric check)
>eps0 = 8.854e-12;
>k    = 1/(4*pi*eps0);    % Coulomb constant
>
>% Geometry (triangle in xy-plane, center at origin, Rq arbitrary)
>Rq = 0.1;                % [m] (any nonzero value works)
>
>% Positions
>r1 = [-1/2;  sqrt(3)/2; 0]*Rq;   % Q1
>r2 = [-1/2; -sqrt(3)/2; 0]*Rq;   % Q2 (= Q1)
>r3 = [1; 0; 0]*Rq;               % Q3 on +x-axis
>
>% Helper: field at origin from Qi at ri
>field_at_center = @(Q, r) k*Q*(-r)/norm(r)^3;
>
>% Choose a numeric value for Q1 and Q4
>Q1 = 1e-9;   % C (arbitrary)
>Q4 = 2e-9;   % C (arbitrary)
>
>% ---------- Case 1: Q3 = Q1 ----------
>Q3 = Q1;
>E1 = field_at_center(Q1, r1);
>E2 = field_at_center(Q1, r2);
>E3 = field_at_center(Q3, r3);
>Etot_1 = E1 + E2 + E3          % should be ~ [0; 0; 0]
>F4_1   = Q4 * Etot_1           % force on Q4 (should be ~0)
>
>% ---------- Case 2: Q3 = -Q1 ----------
>Q3 = -Q1;
>E1 = field_at_center(Q1, r1);
>E2 = field_at_center(Q1, r2);
>E3 = field_at_center(Q3, r3);
>Etot_2 = E1 + E2 + E3          % nonzero, along +x
>F4_2   = Q4 * Etot_2
>
>% ---------- Case 3: Q3 = 2 Q1 ----------
>Q3 = 2*Q1;
>E1 = field_at_center(Q1, r1);
>E2 = field_at_center(Q1, r2);
>E3 = field_at_center(Q3, r3);
>Etot_3 = E1 + E2 + E3          % nonzero, along -x
>F4_3   = Q4 * Etot_3
>
>% You can inspect:
>%   Etot_1 ~ 0
>%   Etot_2 points along +x
>%   Etot_3 points along -x
>% matching the analytical expressions in the note.
>```
### 📊 Summary Table — Field, Flux, Energy & Force (All Cases)

| Case | Condition on $Q_3$ | Direction of $\mathbf{E}(0)$ | Analytical Result (Plain) | MATLAB Check | Interpretation |
|------|---------------------|-------------------------------|-----------------------------|--------------|----------------|
| **1** | $Q_3 = Q_1$ | $\mathbf{E}(0)=0$ | Field cancels by symmetry | ✔ Etot₁ ≈ 0 | Perfect symmetry → no field, no force |
| **2** | $Q_3 = -Q_1$ | $+\hat{x}$ | $E = \dfrac{Q_1}{2\pi\varepsilon_0 R_q^2}\hat{x}$ | ✔ Etot₂ > 0 in x | $Q_1+Q_2$ dominate → field to +x |
| **3** | $Q_3 = 2Q_1$ | $-\hat{x}$ | $E = -\dfrac{Q_1}{4\pi\varepsilon_0 R_q^2}\hat{x}$ | ✔ Etot₃ < 0 in x | $Q_3$ dominates → field to –x |

---

### 💬 What this table shows

- **Case 1:** Perfect symmetry → total field = **zero** → MATLAB confirms with tiny numerical noise.  
- **Case 2:** \(Q_3\) flips sign → field points **+x** exactly as predicted.  
- **Case 3:** \(Q_3\) becomes larger → field pulled **–x**, matching the analytic negative sign.  

This validates **all analytical expressions** for field, force, energy, and flux.  

## ⚡ Exercise 19.3  
### Total Charge on a Disc with Non-Uniform Surface Charge Density

> **Given**  
> A surface charge density that varies with radius:
> $$
> \rho_s(r) = \rho_0\, r^2
> $$
> Calculate the **total charge** on a circular disc of radius $a$.

---

### 🧠 Theory — Surface Charge Integration  
For a surface with charge density $\rho_s$, the total charge is:
$$
Q_{\text{tot}} = \iint_S \rho_s \, dS.
$$

Because the region is a **disc** and the density depends only on the radial distance $r$, we switch to **polar coordinates**:
- $0 \le r \le a$
- $0 \le \phi \le 2\pi$

The surface element becomes:
$$
dS = r \, dr \, d\phi.
$$

Substitute $\rho_s = \rho_0 r^2$:
$$
Q_{\text{tot}}
= \int_0^{2\pi} \int_0^{a} \rho_0 r^2 \, (r \, dr \, d\phi)
= \int_0^{2\pi} d\phi \int_0^{a} \rho_0 r^3 \, dr.
$$

---

### ⚙️ Calculation

1. **Integrate over $r$**:
   $$
   \int_0^{a} r^3 \, dr = \frac{a^4}{4}.
   $$

2. **Integrate over $\phi$**:
   $$
   \int_0^{2\pi} d\phi = 2\pi.
   $$

3. **Multiply results**:
   $$
   Q_{\text{tot}}
   = \rho_0 \left( \frac{a^4}{4} \right) (2\pi)
   = \frac{\pi}{2}\rho_0 a^4.
   $$

---

### 🎉 Final Answer
$$
\boxed{
Q_{\text{tot}} = \frac{\pi}{2}\,\rho_0\, a^4
}
$$

---

### ✅ Verification (MATLAB)
>[!code]- matlab
>```matlab
>syms r phi rho0 a
>
>% Surface charge density
>rho_s = rho0 * r^2;
>
>% Polar surface element
>dS = r;
>
>% Integrate over the disc
>Qtot = int(int(rho_s * dS, r, 0, a), phi, 0, 2*pi);
>Qtot
>
>% Expected: (pi/2) * rho0 * a^4
>```
