> Quick refs: [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]]

---

## Exercise 19.1  
### Coulomb’s Law: Force Between Two Point Charges

> **Given**  
> Two point charges in free space:  
> - $Q_1$ at $P_1(2,\ -4,\ 1)$ nm  
> - $Q_2$ at $P_2(1,\ 1,\ -5)$ nm  
>  
> Calculate the electrostatic force they exert on each other and determine if it is **repulsive** or **attractive** for:  
> - (a) $Q_1 = 2Q_2 = 2~\text{fC}$  
> - (b) $Q_1 = -2Q_2 = 2~\text{fC}$  

---

### Theory recap  

In electrostatics, charges are at rest (no currents). The interaction between two point charges is given by **Coulomb’s law**:

$$
\mathbf{F}_{12}
= Q_1 \mathbf{E}_2(\mathbf{R} = \mathbf{R}_1)
= \frac{Q_1 Q_2}{4\pi\varepsilon_0}
\frac{\mathbf{R}_1 - \mathbf{R}_2}{\lvert \mathbf{R}_1 - \mathbf{R}_2 \rvert^3}
= -\mathbf{F}_{21},
$$

where  
- $\mathbf{F}_{12}$ = force on $Q_1$ due to $Q_2$  
- $\mathbf{F}_{21}$ = force on $Q_2$ due to $Q_1$  
- $\mathbf{R}_1 = \begin{pmatrix}2\\-4\\1\end{pmatrix}\text{ nm}$,  
  $\mathbf{R}_2 = \begin{pmatrix}1\\1\\-5\end{pmatrix}\text{ nm}$  

Key points:
- Newton’s 3rd law: $\mathbf{F}_{12} = -\mathbf{F}_{21}$  
- Same-sign charges → repulsive  
- Opposite-sign charges → attractive  
- To test repulsive vs. attractive, compare direction of $\mathbf{F}_{12}$ with the vector $\mathbf{R}_1 - \mathbf{R}_2$ (or equivalently $\mathbf{F}_{21}$ with $\mathbf{R}_2 - \mathbf{R}_1$):
  - Same direction → repulsive  
  - Opposite direction → attractive  

---

### Calculations  

#### 1. Separation vector and distance

We use the vector in the force formula:

$$
\mathbf{R}_1 - \mathbf{R}_2 =
\begin{pmatrix}
2\\-4\\1
\end{pmatrix}
-
\begin{pmatrix}
1\\1\\-5
\end{pmatrix}
=
\begin{pmatrix}
1\\-5\\6
\end{pmatrix}\ \text{nm}
$$

Magnitude:

$$
\lvert \mathbf{R}_1 - \mathbf{R}_2 \rvert
= \sqrt{1^2 + (-5)^2 + 6^2}~\text{nm}
= \sqrt{62}~\text{nm}
\approx 7.874~\text{nm}.
$$

In SI units:

- $1~\text{nm} = 10^{-9}~\text{m}$  
- $Q_1, Q_2$ in fC: $1~\text{fC} = 10^{-15}~\text{C}$  
- Coulomb constant:  
  $$
  \frac{1}{4\pi\varepsilon_0} \approx 8.99\times 10^9~\text{N·m}^2/\text{C}^2
  $$

---

#### (a) $Q_1 = 2Q_2 = 2~\text{fC}$ (both positive)

From $Q_1 = 2Q_2 = 2~\text{fC}$ we get:

- $Q_1 = 2\times 10^{-15}~\text{C}$  
- $Q_2 = 1\times 10^{-15}~\text{C}$  

Force on $Q_1$ due to $Q_2$:

$$
\mathbf{F}_{12}
= \frac{Q_1 Q_2}{4\pi\varepsilon_0}
\frac{\mathbf{R}_1 - \mathbf{R}_2}{\lvert \mathbf{R}_1 - \mathbf{R}_2 \rvert^3}
\approx
\begin{pmatrix}
36.82\\-184.1\\220.9
\end{pmatrix}
\ \mu\text{N}
$$

Using $\mathbf{F}_{21} = -\mathbf{F}_{12}$:

$$
\mathbf{F}_{21}
\approx
\begin{pmatrix}
-36.82\\184.1\\-220.9
\end{pmatrix}
\ \mu\text{N}
$$

Magnitude:

$$
\lvert \mathbf{F}_{12} \rvert
= \lvert \mathbf{F}_{21} \rvert
\approx 290~\mu\text{N}.
$$

To check repulsive vs. attractive, compare direction:

- $\mathbf{F}_{12}$ is along $\mathbf{R}_1 - \mathbf{R}_2$ (same direction).  
- Since $Q_1$ and $Q_2$ are both positive, this is a repulsive force.

Result (a):  
- $\mathbf{F}_{12} \approx (36.82,\ -184.1,\ 220.9)~\mu\text{N}$  
- $\mathbf{F}_{21} \approx (-36.82,\ 184.1,\ -220.9)~\mu\text{N}$  
- Nature: repulsive  

---

#### (b) $Q_1 = -2Q_2 = 2~\text{fC}$ (opposite signs)

Now $Q_1 = 2\times 10^{-15}~\text{C}$ and  

$$
Q_1 = -2Q_2 \Rightarrow Q_2 = -1\times 10^{-15}~\text{C}.
$$

The geometry is unchanged, only the product $Q_1Q_2$ changes sign, so the forces flip direction:

$$
\mathbf{F}_{12}
\approx
\begin{pmatrix}
-36.82\\184.1\\-220.9
\end{pmatrix}
\ \mu\text{N}
,\qquad
\mathbf{F}_{21}
\approx
\begin{pmatrix}
36.82\\-184.1\\220.9
\end{pmatrix}
\ \mu\text{N}.
$$

Magnitude is the same as before ($\approx 290~\mu\text{N}$), but:

- $\mathbf{F}_{12}$ now points opposite to $(\mathbf{R}_1 - \mathbf{R}_2)$ → attractive.  

Result (b):  
- $\mathbf{F}_{12} \approx (-36.82,\ 184.1,\ -220.9)~\mu\text{N}$  
- $\mathbf{F}_{21} \approx (36.82,\ -184.1,\ 220.9)~\mu\text{N}$  
- Nature: attractive  

---

### MATLAB verification
> [!code]- matlab
> ```matlab
> %% 19.1 — Coulomb Force (verification)
> ke = 8.99e9;                     % Coulomb constant [N m^2 / C^2]
>
> % Positions (nm -> m)
> R1 = 1e-9 * [2; -4;  1];
> R2 = 1e-9 * [1;  1; -5];
>
> dR12 = R1 - R2;                  % vector in F12 formula
> r    = norm(dR12);               % distance [m]
> u12  = dR12 / r;                 % unit vector
>
> computeForce = @(Q1,Q2) ke*Q1*Q2/r^2 * u12;
>
> %% Case (a): Q1 = 2 fC, Q2 = 1 fC
> Q1a =  2e-15;
> Q2a =  1e-15;
> F12a = computeForce(Q1a,Q2a);
> F21a = -F12a;
>
> %% Case (b): Q1 = 2 fC, Q2 = -1 fC
> Q1b =  2e-15;
> Q2b = -1e-15;
> F12b = computeForce(Q1b,Q2b);
> F21b = -F12b;
>
> fprintf("Case (a): repulsive\n");
> fprintf("F12 = [%.2f, %.2f, %.2f] µN\n", F12a*1e6);
> fprintf("F21 = [%.2f, %.2f, %.2f] µN\n\n", F21a*1e6);
>
> fprintf("Case (b): attractive\n");
> fprintf("F12 = [%.2f, %.2f, %.2f] µN\n", F12b*1e6);
> fprintf("F21 = [%.2f, %.2f, %.2f] µN\n", F21b*1e6);
> ```

---

## Exercise 19.2  
### Three Point Charges in Triangular Configuration

> **Given**  
> Three equally spaced point charges in free space:  
> - $Q_1 = Q_2$  
> - $Q_3$ (possibly different from $Q_1$)  
>  
> The charges form an equilateral triangle in the $xy$-plane.  
> The coordinate system is centered at the triangle center, and  
> $Q_3$ lies on the $x$-axis at $x = R_q$.  
>
> Tasks:  
> - (a) Sketch the configuration.  
> - (b) Find $\mathbf{E}_\text{tot}$ at the origin for three cases: $Q_3 = Q_1$, $Q_3 = -Q_1$, $Q_3 = 2Q_1$.  
> - (c) Describe the total outward flux and find $Q_3$ so the flux is zero.  
> - (d) Find the electrostatic energy for the three cases and when it becomes zero.  
> - (e) Add a fourth charge $Q_4$ at the center and find the force on it.  

---

### (a) Geometry – equilateral triangle in the $xy$-plane

All three charges lie on a circle of radius $R_q$ centered at the origin:

- $Q_3$ on the $+x$-axis:
  $$
  \mathbf{r}_3 = (R_q,\,0,\,0)
  $$
- $Q_1$ and $Q_2$ rotated by $\pm 120^\circ$:
  $$
  \begin{aligned}
  \mathbf{r}_1 &= R_q(\cos 120^\circ,\ \sin 120^\circ,\ 0)
              = \Big(-\tfrac{R_q}{2},\ \tfrac{\sqrt{3}}{2}R_q,\ 0\Big) \\
  \mathbf{r}_2 &= R_q(\cos(-120^\circ),\ \sin(-120^\circ),\ 0)
              = \Big(-\tfrac{R_q}{2},\ -\tfrac{\sqrt{3}}{2}R_q,\ 0\Big)
  \end{aligned}
  $$

The triangle is equilateral with side length:

$$
R_{12} = R_{23} = R_{13} = \sqrt{3}R_q.
$$

---

### (b) Total electric field at the center

Field from a point charge $Q_k$ at position $\mathbf{r}_k$ evaluated at the origin:

$$
\mathbf{E}_k(\mathbf{0})
= \frac{1}{4\pi\varepsilon_0}
\frac{-\mathbf{r}_k}{\lvert \mathbf{r}_k \rvert^3}
Q_k
= \frac{1}{4\pi\varepsilon_0 R_q^3}Q_k(-\mathbf{r}_k),
$$

since $\lvert \mathbf{r}_k \rvert = R_q$.

Total field:

$$
\mathbf{E}_\text{tot}(\mathbf{0})
= \sum_{k=1}^3 \mathbf{E}_k
= \frac{1}{4\pi\varepsilon_0 R_q^3}\Big[Q_1(-\mathbf{r}_1) + Q_1(-\mathbf{r}_2) + Q_3(-\mathbf{r}_3)\Big].
$$

Using the geometry:

$$
-\mathbf{r}_1 - \mathbf{r}_2 = (R_q, 0, 0) = R_q\hat{\mathbf{x}}, \qquad
-\mathbf{r}_3 = (-R_q, 0, 0) = -R_q\hat{\mathbf{x}},
$$

we get

$$
\mathbf{E}_\text{tot}(\mathbf{0})
= \frac{1}{4\pi\varepsilon_0 R_q^2}(Q_1 - Q_3)\hat{\mathbf{x}}.
$$

Now evaluate the three cases:

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

---

### (c) Total outward flux through a closed surface

Surround all three charges by an arbitrary closed surface $S$.

By Gauss’s law:

$$
\oint_S \mathbf{E}\cdot d\mathbf{S} = \frac{Q_\text{enc}}{\varepsilon_0},
\qquad
Q_\text{enc} = Q_1 + Q_2 + Q_3 = 2Q_1 + Q_3.
$$

Hence

$$
\boxed{
\displaystyle
\oint_S \mathbf{E}\cdot d\mathbf{S}
= \frac{2Q_1 + Q_3}{\varepsilon_0}
}
$$

For the three cases:

$$
\begin{array}{c|c|c}
\text{Case} & Q_3 & \displaystyle \oint_S \mathbf{E}\cdot d\mathbf{S} \\
\hline
(1) & Q_3 = Q_1      & \dfrac{3Q_1}{\varepsilon_0} \\
(2) & Q_3 = -Q_1     & \dfrac{Q_1}{\varepsilon_0} \\
(3) & Q_3 = 2Q_1     & \dfrac{4Q_1}{\varepsilon_0}
\end{array}
$$

To make the outward flux zero, we must have

$$
Q_\text{enc} = 0 \Rightarrow 2Q_1 + Q_3 = 0
\Rightarrow
\boxed{Q_3 = -2Q_1}.
$$

---

### (d) Electrostatic energy of the configuration

Electrostatic energy of three point charges:

$$
W_e = \sum_{i<j} \frac{1}{4\pi\varepsilon_0}\frac{Q_iQ_j}{R_{ij}},
\quad
R_{ij} = \sqrt{3}R_q.
$$

Thus

$$
W_e = \frac{1}{4\pi\varepsilon_0\sqrt{3}R_q}\Big(Q_1Q_2 + Q_1Q_3 + Q_2Q_3\Big).
$$

With $Q_1 = Q_2$:

$$
W_e = \frac{1}{4\pi\varepsilon_0\sqrt{3}R_q}\Big(Q_1^2 + 2Q_1Q_3\Big).
$$

Special cases:

- $Q_3 = Q_1$:
  $$
  W_e = \frac{3Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q}
      = \frac{\sqrt{3}Q_1^2}{4\pi\varepsilon_0 R_q}
  $$
- $Q_3 = -Q_1$:
  $$
  W_e = -\frac{Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q}
  $$
- $Q_3 = 2Q_1$:
  $$
  W_e = \frac{5Q_1^2}{4\pi\varepsilon_0\sqrt{3}R_q}
  $$

We can also see when the energy is zero:

$$
Q_1^2 + 2Q_1Q_3 = 0
\Rightarrow
Q_3 = -\frac{Q_1}{2}.
$$

---

### (e) Force on a fourth charge at the center

Place a fourth charge $Q_4$ at the origin. The total field from the first three charges at the center is

$$
\mathbf{E}_\text{tot}(\mathbf{0})
= \frac{Q_1 - Q_3}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}.
$$

Hence the force on $Q_4$:

$$
\boxed{
\mathbf{F}_4 = Q_4 \mathbf{E}_\text{tot}(\mathbf{0})
= Q_4\frac{Q_1 - Q_3}{4\pi\varepsilon_0 R_q^2}\hat{\mathbf{x}}
}
$$

Special cases:

$$
\begin{array}{c|c}
\text{Case} & \mathbf{F}_4 \\
\hline
Q_3 = Q_1   & 0 \\
Q_3 = -Q_1  & \hat{\mathbf{x}}\dfrac{Q_1Q_4}{2\pi\varepsilon_0R_q^2} \\
Q_3 = 2Q_1  & -\hat{\mathbf{x}}\dfrac{Q_1Q_4}{4\pi\varepsilon_0R_q^2}
\end{array}
$$

---

## Exercise 19.3  
### Total Charge on a Disc with Non-Uniform Surface Charge Density  

> **Given**  
> Surface charge density:
> $$
> \rho_s(r) = \rho_0\, r^2
> $$
> on a circular disc of radius $a$.  
> Find the total charge $Q_\text{tot}$.

---

### Theory – Surface charge integration

Total charge:

$$
Q_\text{tot} = \iint_S \rho_s(r)\,dS.
$$

Use polar coordinates (disc in the $xy$-plane):

- $0 \le r \le a$  
- $0 \le \phi \le 2\pi$  

Area element:

$$
dS = r\,dr\,d\phi.
$$

Substitute $\rho_s(r) = \rho_0 r^2$:

$$
Q_\text{tot}
= \int_0^{2\pi}\int_0^a \rho_0 r^2 (r\,dr\,d\phi)
= \int_0^{2\pi} d\phi \int_0^a \rho_0 r^3\,dr.
$$

---

### Calculation

1. Integrate over $r$:

   $$
   \int_0^a r^3\,dr = \frac{a^4}{4}.
   $$

2. Integrate over $\phi$:

   $$
   \int_0^{2\pi} d\phi = 2\pi.
   $$

3. Combine:

   $$ 
   Q_\text{tot}
   = \rho_0 \cdot \frac{a^4}{4} \cdot 2\pi
   = \frac{\pi}{2}\rho_0 a^4.
   $$

Final result:
$$
\boxed{
Q_\text{tot} = \dfrac{\pi}{2}\,\rho_0\,a^4
}
$$

---

### MATLAB verification
> [!code]- matlab
> ```matlab
> syms r phi rho0 a
>
> rho_s = rho0 * r^2;   % surface charge density
> dS    = r;            % polar area element factor
>
> Qtot = int(int(rho_s * dS, r, 0, a), phi, 0, 2*pi);
> simplify(Qtot)        % -> (pi/2)*rho0*a^4
> ```

---

## Exercise 19.4  
### Potential and Field on the Axis of a Charged Ring  

> **Given**  
> A ring of radius $a$ in the $xy$-plane ($z=0$) with constant line charge density $\rho_L = \rho_0$.  
> The center of the ring is at the origin.  
>  
> Find for points on the $z$-axis $(0,0,z)$:  
> (a) the potential $V(z)$  
> (b) the electric field $\mathbf{E}(z)$  

---

### (a) Potential $V(z)$

General expression for potential from a line charge:

$$
V(\mathbf{r}_0) = \frac{1}{4\pi\varepsilon}\int_L \frac{\rho_L(\mathbf{r})}{\lvert \mathbf{r}_0 - \mathbf{r} \rvert} dl,
\quad \varepsilon = \varepsilon_0\varepsilon_r.
$$

Parameterization of the ring:

- Charge position:
  $$
  \mathbf{r}(\phi) =
  \begin{pmatrix}
  a\cos\phi\\
  a\sin\phi\\
  0
  \end{pmatrix},
  \quad 0 \le \phi \le 2\pi
  $$
- Observation point on axis:
  $$
  \mathbf{r}_0 =
  \begin{pmatrix}
  0\\0\\z
  \end{pmatrix}
  $$
- Line element: $dl = a\,d\phi$  
- Distance:
  $$
  \lvert \mathbf{r}_0 - \mathbf{r} \rvert = \sqrt{a^2 + z^2}
  $$  
  (independent of $\phi$).

Then

$$
V(z)
= \frac{\rho_0}{4\pi\varepsilon}\int_0^{2\pi}
\frac{a\,d\phi}{\sqrt{a^2 + z^2}}
= \frac{\rho_0 a}{4\pi\varepsilon\sqrt{a^2 + z^2}}
\int_0^{2\pi} d\phi
= \frac{\rho_0 a}{2\varepsilon\sqrt{a^2 + z^2}}.
$$

Result:
$$
\boxed{
V(z) = \frac{\rho_0 a}{2\varepsilon\sqrt{a^2 + z^2}}
}
$$

---

### (b) Electric field $\mathbf{E}(z)$

General expression for field from a line charge:

$$
\mathbf{E}(\mathbf{r}_0)
= \frac{1}{4\pi\varepsilon}\int_L
\rho_L(\mathbf{r})
\frac{\mathbf{r}_0 - \mathbf{r}}{\lvert \mathbf{r}_0 - \mathbf{r} \rvert^3} dl.
$$

Using the same parameterization:

- $\mathbf{r}_0 - \mathbf{r} = \begin{pmatrix} -a\cos\phi\\-a\sin\phi\\z \end{pmatrix}$  
- $\lvert \mathbf{r}_0 - \mathbf{r} \rvert = \sqrt{a^2+z^2}$  
- $dl=a\,d\phi$  

So

$$
\mathbf{E}(z)
= \frac{\rho_0}{4\pi\varepsilon}
\int_0^{2\pi}
\frac{(-a\cos\phi,\,-a\sin\phi,\,z)\,a\,d\phi}{(a^2+z^2)^{3/2}}.
$$

The $x$ and $y$ components vanish by symmetry (integrals of $\cos\phi$ and $\sin\phi$ over $0\to 2\pi$ are zero). Remaining $z$-component:

$$
E_z(z)
= \frac{\rho_0 a z}{4\pi\varepsilon(a^2+z^2)^{3/2}}
\int_0^{2\pi} d\phi
= \frac{\rho_0 a z}{2\varepsilon(a^2+z^2)^{3/2}}.
$$

So

$$
\boxed{
\mathbf{E}(z) = \frac{\rho_0 a z}{2\varepsilon(a^2+z^2)^{3/2}}\,\hat{\mathbf{z}}
}
$$

---

## Exercise 19.5  
### Capacitance and Maximum Voltage for Two Configurations  

> **Given**  
> (a) Parallel-plate capacitor:  
> - Dielectric: $\varepsilon_r = 4$, dielectric strength $E_\text{max} = 80~\text{kV/mm}$  
> - Thickness: $d = 0.1~\text{mm}$  
> - Plate sides: $1~\text{mm}$ and $3~\text{mm}$  
>
> (b) Spherical capacitor (concentric spheres):  
> - Dielectric: $\varepsilon_r = 4$, dielectric strength $E_\text{max} = 80~\text{kV/mm}$  
> - Inner/outer diameters: $1~\text{mm}$ and $3~\text{mm}$  

---

### (a) Parallel-plate capacitor

Area:

$$
A = (1~\text{mm})(3~\text{mm})
  = 3\times 10^{-6}~\text{m}^2
$$

Thickness:

$$
d = 0.1~\text{mm} = 1\times 10^{-4}~\text{m}
$$

Capacitance:

$$
C = \varepsilon_0\varepsilon_r \frac{A}{d}
  = \varepsilon_0\cdot 4 \cdot \frac{3\times 10^{-6}}{10^{-4}}
  \approx 1.063~\text{pF}.
$$

Maximum voltage (assuming uniform field and using dielectric strength):

- $E_\text{max} = 80~\text{kV/mm} = 8\times 10^7~\text{V/m}$  
- $V_\text{max} = E_\text{max} d = (8\times 10^7)(10^{-4}) = 8\times 10^3~\text{V} = 8~\text{kV}$  

Results (a):
- $C \approx 1.063~\text{pF}$  
- $V_\text{max} \approx 8~\text{kV}$  

---

### (b) Spherical capacitor

Inner radius: $a = 0.5~\text{mm} = 0.5\times 10^{-3}~\text{m}$  
Outer radius: $b = 1.5~\text{mm} = 1.5\times 10^{-3}~\text{m}$  

Capacitance of two concentric spheres:

$$
C = \frac{4\pi\varepsilon_0\varepsilon_r}{a^{-1} - b^{-1}}
\approx 0.3338~\text{pF}.
$$

Electric field between the spheres (assuming inner conductor carries charge $Q$):

$$
E_R(R) = \frac{Q}{4\pi\varepsilon_0\varepsilon_r R^2},
$$

which is maximum at $R = a$:

$$
E_\text{max} = \frac{Q}{4\pi\varepsilon_0\varepsilon_r a^2}
\Rightarrow
Q = 4\pi\varepsilon_0\varepsilon_r a^2 E_\text{max}.
$$

The capacitor voltage is $V = Q/C$. Combining with $C$ and $Q$ above (or using the derived formula from the solution):

$$
V_\text{max} = E_\text{max} a\left(1 - \frac{a}{b}\right)
\approx 26.67~\text{kV}.
$$

Results (b):
- $C \approx 0.3338~\text{pF}$  
- $V_\text{max} \approx 26.7~\text{kV}$  

---

## Exercise 19.6  
### Charged Cylindrical Conductor with Dielectric and Outer Conductor  

> **Given**  
> - Long cylindrical conductor of radius $a = 1.5~\text{mm}$ in free space  
> - Line charge density: $Q' = 5~\text{pC/m}$  
> - Cylindrical coordinates $(r,\varphi,z)$, $z$-axis along the cylinder  
> - Assume length $L = 1~\text{m}$ for numerical values  
>
> Tasks:  
> (a) $|\mathbf{E}|$ on the surface of the conductor  
> (b) Same, but with a dielectric ring of $\varepsilon_r = 2.5$ around the conductor  
> (c) Add a neutral conducting ring around the dielectric with inner/outer radii $b=5~\text{mm}$, $c=6~\text{mm}$; find surface charge densities and field intensities at $r=b$ and $r=c$ and comment  
> (d) Total charge of the configuration and how to make the field zero outside  

---

### (a) Electric field on the surface (free space)

Use Gauss’s law in terms of $\mathbf{D}$:

$$
\oint_S \mathbf{D}\cdot d\mathbf{S} = Q' L.
$$

Choose a cylindrical Gaussian surface of radius $r$ and length $L$:

- $\mathbf{D} = D_r(r)\,\hat{\mathbf{r}}$  
- Surface area: $S = 2\pi r L$  

So

$$
D_r(r)\cdot 2\pi r L = Q'L
\Rightarrow
D_r(r) = \frac{Q'}{2\pi r}.
$$

At the conductor surface $r=a$:

$$
D_r(a) = \frac{Q'}{2\pi a}.
$$

In free space, $\mathbf{E} = \mathbf{D}/\varepsilon_0$:

$$
E_r(a) = \frac{Q'}{2\pi a\varepsilon_0}.
$$

Numerically this gives:

$$
|\mathbf{E}(r=a)| \approx 59.92~\text{V/m}.
$$

---

### (b) With dielectric of $\varepsilon_r = 2.5$

Same $\mathbf{D}$ (since it is set by free charge $Q'$), but now

$$
\varepsilon = \varepsilon_0\varepsilon_r = 2.5\varepsilon_0.
$$

Thus

$$
E_r(a) = \frac{D_r(a)}{\varepsilon}
= \frac{Q'}{2\pi a \varepsilon_0\varepsilon_r}
= \frac{1}{\varepsilon_r}\cdot \frac{Q'}{2\pi a\varepsilon_0}
\approx 23.97~\text{V/m}.
$$

The dielectric reduces the field by a factor $\varepsilon_r$.

---

### (c) Conducting ring around the dielectric

We now place a neutral conducting ring with:

- Inner radius: $b = 5~\text{mm}$  
- Outer radius: $c = 6~\text{mm}$  

Inside the metal, $\mathbf{E} = 0$. To enforce this, charges are induced on the inner and outer surfaces of the conductor.

From boundary conditions between dielectric and conductor:

- At $r=b$:
  $$
  D_r(b) = \frac{Q'}{2\pi b}
  \Rightarrow
  \rho_s(r=b) = D_r(b) \approx 159.2~\text{pC/m}^2
  $$
  and
  $$
  |\mathbf{E}(r=b)| \approx 7.190~\text{V/m}.
  $$

- At $r=c$:
  $$
  D_r(c) = \frac{Q'}{2\pi c}
  \Rightarrow
  \rho_s(r=c) = D_r(c) \approx 132.6~\text{pC/m}^2
  $$
  and
  $$
  |\mathbf{E}(r=c)| \approx 14.98~\text{V/m}.
  $$

Interpretation:

- The total charges on the inner and outer surfaces are equal in magnitude and opposite in sign (the ring is overall neutral).  
- The inner surface area is smaller, so to carry the same magnitude of charge, the surface charge density is larger at $r=b$.  
- The dielectric reduces the field in the inner region, so $|\mathbf{E}(r=b)| < |\mathbf{E}(r=c)|$ even though $\rho_s(b) > \rho_s(c)$.

---

### (d) Total charge and making the field zero outside

- The dielectric and conducting ring are overall neutral (they only have induced charges).  
- The only net free charge in the configuration is that of the original cylindrical conductor:

  $$
  Q'_\text{tot} = 5~\text{pC/m}.
  $$

To make the field zero outside (in free space beyond the outer conductor), the total enclosed charge must be zero for a cylindrical Gaussian surface at $r > c$:

- Either discharge the inner conductor (make $Q' = 0$), or  
- Give the outer conducting ring a net line charge of $-Q'$ so that the total enclosed charge is zero.

---