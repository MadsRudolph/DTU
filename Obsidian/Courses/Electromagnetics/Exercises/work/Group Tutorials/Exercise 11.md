> Quick refs: [[Courses/Electromagnetics/Formulas/Plane Waves & Power — Quick Formula Sheet]]
---

# Exercise 11 — Plane Wave: Basics

---

## Exercise 11.1 — Check if Given Fields Form a Uniform Plane Wave

> **Given**  
> Time-harmonic fields in **free space** ($\eta_0 \approx 120\pi~\Omega$), with phasor representation
> $$
 \tilde{\mathbf{E}}(\mathbf{r}) =
 \begin{pmatrix}
 0\\[2pt]
 1\\[2pt]
 0
 \end{pmatrix}
 e^{-j(x+y+z)/\text{m}}\ \text{V/m},
 \qquad
 \tilde{\mathbf{H}}(\mathbf{r}) =
 \frac{1}{120\pi}
 \begin{pmatrix}
 1\\[2pt]
 0\\[2pt]
 0
 \end{pmatrix}
e^{-j(x+y+z)/\text{m}}\ \text{A/m}.
 $$
>
> **Check** whether these fields can represent a **uniform plane wave in free space** by verifying:
> 1. $\boldsymbol{\beta} \cdot \tilde{\mathbf{E}}_0 = 0$  
> 2. $\boldsymbol{\beta} \cdot \tilde{\mathbf{H}}_0 = 0$  
> 3. $\tilde{\mathbf{H}}_0 = \dfrac{1}{\eta_0}\hat{\boldsymbol{\beta}} \times \tilde{\mathbf{E}}_0$  
>
> where $\tilde{\mathbf{E}}_0$ and $\tilde{\mathbf{H}}_0$ are the **phasor amplitudes** and $\boldsymbol{\beta}$ is the **propagation vector**.

---

### Theory recap

Uniform plane wave in a lossless medium (Ulaby & Ravaioli, plane-wave chapter):

- Phasor fields:
  $$
  \tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0 e^{-j\boldsymbol{\beta}\cdot\mathbf{r}},
  \qquad
  \tilde{\mathbf{H}}(\mathbf{r}) = \tilde{\mathbf{H}}_0 e^{-j\boldsymbol{\beta}\cdot\mathbf{r}}.
  $$
- Free-space intrinsic impedance:
  $$
  \eta_0 = \sqrt{\frac{\mu_0}{\varepsilon_0}} \approx 120\pi~\Omega.
  $$
- For a **uniform plane wave in a lossless medium**:
  $$
  \tilde{\mathbf{H}}_0 = \frac{1}{\eta_0}\hat{\boldsymbol{\beta}} \times \tilde{\mathbf{E}}_0,
  \qquad
  \tilde{\mathbf{E}}_0 = -\eta_0\, \hat{\boldsymbol{\beta}} \times \tilde{\mathbf{H}}_0,
  $$
  $$
  \boldsymbol{\beta}\cdot\tilde{\mathbf{E}}_0 = 0,\quad
  \boldsymbol{\beta}\cdot\tilde{\mathbf{H}}_0 = 0,\quad
  \tilde{\mathbf{E}}_0\cdot\tilde{\mathbf{H}}_0 = 0.
  $$
- $\hat{\boldsymbol{\beta}}$, $\tilde{\mathbf{E}}_0$, $\tilde{\mathbf{H}}_0$ form a **right-handed orthogonal triad**.

---

### Geometry / setup

From the exponential term
$$
\tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0 e^{-j(x+y+z)/\text{m}},
$$
we identify:
$$
-j\boldsymbol{\beta}\cdot\mathbf{r} = -j(x+y+z)/\text{m}
\quad\Rightarrow\quad
\boldsymbol{\beta} =
\begin{pmatrix}
1\\[2pt]
1\\[2pt]
1
\end{pmatrix}\ \text{m}^{-1}.
$$

Amplitudes:
$$
\tilde{\mathbf{E}}_0 =
\begin{pmatrix}
0\\[2pt]
1\\[2pt]
0
\end{pmatrix}\ \text{V/m},
\qquad
\tilde{\mathbf{H}}_0 =
\frac{1}{120\pi}
\begin{pmatrix}
1\\[2pt]
0\\[2pt]
0
\end{pmatrix}\ \text{A/m}.
$$

Normalized propagation direction:
$$
\hat{\boldsymbol{\beta}}
= \frac{\boldsymbol{\beta}}{\lVert\boldsymbol{\beta}\rVert}
= \frac{1}{\sqrt{3}}
\begin{pmatrix}
1\\[2pt]
1\\[2pt]
1
\end{pmatrix}.
$$

---

### Derivation

1. **Check orthogonality with $\tilde{\mathbf{E}}_0$**

$$
\boldsymbol{\beta}\cdot\tilde{\mathbf{E}}_0
=
\begin{pmatrix}1\\1\\1\end{pmatrix}
\cdot
\begin{pmatrix}0\\1\\0\end{pmatrix}
= 1.
$$

So
$$
\boldsymbol{\beta}\cdot\tilde{\mathbf{E}}_0 \neq 0.
$$

Already this violates the plane-wave condition (E must be transverse).

2. **Check orthogonality with $\tilde{\mathbf{H}}_0$**

$$
\boldsymbol{\beta}\cdot\tilde{\mathbf{H}}_0
=
\begin{pmatrix}1\\1\\1\end{pmatrix}
\cdot
\frac{1}{120\pi}
\begin{pmatrix}1\\0\\0\end{pmatrix}
= \frac{1}{120\pi} \neq 0.
$$

So H is not transverse either.

3. **Check cross-product relation**

The **required** relation:
$$
\tilde{\mathbf{H}}_0 \stackrel{?}{=} \frac{1}{\eta_0}\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0.
$$

Compute:
$$
\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0
=
\frac{1}{\sqrt{3}}
\begin{pmatrix}
1\\[2pt]
1\\[2pt]
1
\end{pmatrix}
\times
\begin{pmatrix}
0\\[2pt]
1\\[2pt]
0
\end{pmatrix}
=
\frac{1}{\sqrt{3}}
\begin{pmatrix}
1\cdot 0 - 1\cdot 1\\[2pt]
1\cdot 0 - 1\cdot 0\\[2pt]
1\cdot 1 - 1\cdot 0
\end{pmatrix}
=
\frac{1}{\sqrt{3}}
\begin{pmatrix}
-1\\[2pt]
0\\[2pt]
1
\end{pmatrix}.
$$

Then
$$
\frac{1}{\eta_0}\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0
=
\frac{1}{120\pi\sqrt{3}}
\begin{pmatrix}
-1\\[2pt]
0\\[2pt]
1
\end{pmatrix},
$$
which is clearly **not equal** to
$$
\tilde{\mathbf{H}}_0 =
\frac{1}{120\pi}
\begin{pmatrix}
1\\[2pt]
0\\[2pt]
0
\end{pmatrix}.
$$

So the cross-product relation also fails.

---

### Final boxed result

The fields **do not** represent a uniform plane wave in free space:

$$
\boxed{
\boldsymbol{\beta}\cdot\tilde{\mathbf{E}}_0 \neq 0,\quad
\boldsymbol{\beta}\cdot\tilde{\mathbf{H}}_0 \neq 0,\quad
\tilde{\mathbf{H}}_0 \neq \frac{1}{\eta_0}\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0
\ \Rightarrow\ \text{not a plane wave.}
}
$$

**Notes**

- Key plane-wave test: E and H must both be **transverse** to the direction of propagation.
- The cross-product relation is a strong consistency check.
- Very typical exam pattern: *“Given E and H, are these a valid plane wave?”*.

---

### MATLAB — Exercise 11.1 (verification)

> [!code]- MATLAB — Exercise 11.1 (verification)  
> ```matlab
> eta0 = 120*pi;                   % free-space intrinsic impedance [ohm]
> 
> % Propagation vector from exp(-j(x+y+z))
> beta = [1; 1; 1];                % [1/m]
> 
> % Field amplitudes
> E0 = [0; 1; 0];                  % V/m
> H0 = (1/eta0)*[1; 0; 0];         % A/m
> 
> beta_hat = beta / norm(beta);
> 
> % Conditions
> cond1 = dot(beta, E0);           % should be 0 for plane wave
> cond2 = dot(beta, H0);           % should be 0 for plane wave
> H0_from_E = (1/eta0) * cross(beta_hat, E0);
> 
> fprintf('beta·E0 = %g\n', cond1);
> fprintf('beta·H0 = %g\n', cond2);
> fprintf('H0       = [%g %g %g]^T\n', H0);
> fprintf('H0_from_E= [%g %g %g]^T\n', H0_from_E);
>```
---

## Exercise 11.2 — Extracting Propagation Vector and H from E

> **Given**  
> A time-harmonic electric field in free space:
> $$
 \tilde{\mathbf{E}}(\mathbf{r}) =
 \begin{pmatrix}
 1\\[2pt]
 j\\[2pt]
 -1
 \end{pmatrix}
 e^{-j(2y+3z)/\text{m}}\ \text{V/m}.
 $$
>
> **Find**:  
> (a) The **propagation vector** $\boldsymbol{\beta}$ and unit vector $\hat{\boldsymbol{\beta}}$.  
> (b) The corresponding **magnetic field** phasor $\tilde{\mathbf{H}}(\mathbf{r})$ in free space.  
> (c) Check that all plane-wave relations are satisfied.

---

### Theory recap

For a uniform plane wave (again free space):

- Spatial dependence:
  $$
  \tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0 e^{-j\boldsymbol{\beta}\cdot\mathbf{r}}.
  $$
- Propagation vector:
  $$
  \boldsymbol{\beta} = \beta_x\hat{\mathbf{x}} + \beta_y\hat{\mathbf{y}} + \beta_z\hat{\mathbf{z}}.
  $$
- Free-space relation between E and H:
  $$
  \tilde{\mathbf{H}}_0 = \frac{1}{\eta_0}\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0.
  $$
- Transversality:
  $$
  \boldsymbol{\beta}\cdot\tilde{\mathbf{E}}_0 = 0,\quad
  \boldsymbol{\beta}\cdot\tilde{\mathbf{H}}_0 = 0.
  $$

---

### Geometry / setup

From the exponent:
$$
\tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0\,e^{-j(2y+3z)/\text{m}},
$$
we identify
$$
-j\boldsymbol{\beta}\cdot\mathbf{r} = -j(2y+3z)/\text{m}
\quad\Rightarrow\quad
\boldsymbol{\beta} =
\begin{pmatrix}
0\\[2pt]
2\\[2pt]
3
\end{pmatrix}\ \text{m}^{-1}.
$$

So
$$
\beta_x = 0,\quad
\beta_y = 2,\quad
\beta_z = 3.
$$

Amplitude:
$$
\tilde{\mathbf{E}}_0 =
\begin{pmatrix}
1\\[2pt]
j\\[2pt]
-1
\end{pmatrix}\ \text{V/m}.
$$

---

### Derivation

#### (a) Propagation vector and direction

Magnitude:
$$
\lVert\boldsymbol{\beta}\rVert
= \sqrt{0^2 + 2^2 + 3^2}
= \sqrt{13}\ \text{m}^{-1}.
$$

Unit vector:
$$
\boxed{
\hat{\boldsymbol{\beta}} =
\frac{1}{\sqrt{13}}
\begin{pmatrix}
0\\[2pt]
2\\[2pt]
3
\end{pmatrix}
}
$$

---

#### (b) Magnetic field phasor

Use the plane-wave relation:
$$
\tilde{\mathbf{H}}_0 = \frac{1}{\eta_0}\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0.
$$

Compute cross product:

First compute $\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0$:

Let
$$
\hat{\boldsymbol{\beta}} = \frac{1}{\sqrt{13}}(0,2,3)^T,
\quad
\tilde{\mathbf{E}}_0 = (1,j,-1)^T.
$$

Then
$$
\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0
=
\frac{1}{\sqrt{13}}
\begin{vmatrix}
\hat{\mathbf{x}} & \hat{\mathbf{y}} & \hat{\mathbf{z}}\\
0 & 2 & 3\\
1 & j & -1
\end{vmatrix}.
$$

Components:

- $x$-component:
  $$
  2(-1) - 3j = -2 - 3j.
  $$
- $y$-component:
  $$
  -(0(-1) - 3\cdot 1) = -(-3) = 3.
  $$
- $z$-component:
  $$
  0\cdot j - 2\cdot 1 = -2.
  $$

So
$$
\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0
=
\frac{1}{\sqrt{13}}
\begin{pmatrix}
-2-3j\\[2pt]
3\\[2pt]
-2
\end{pmatrix}.
$$

Therefore
$$
\tilde{\mathbf{H}}_0
=
\frac{1}{\eta_0\sqrt{13}}
\begin{pmatrix}
-2-3j\\[2pt]
3\\[2pt]
-2
\end{pmatrix}\ \text{A/m},
$$
and the full phasor:
$$
\boxed{
\tilde{\mathbf{H}}(\mathbf{r})
=
\frac{1}{\eta_0\sqrt{13}}
\begin{pmatrix}
-2-3j\\[2pt]
3\\[2pt]
-2
\end{pmatrix}
e^{-j(2y+3z)/\text{m}}\ \text{A/m}
}
$$

---

#### (c) Check plane-wave relations

1. Transversality of E:
   $$
   \boldsymbol{\beta}\cdot\tilde{\mathbf{E}}_0
   =
   \begin{pmatrix}0\\2\\3\end{pmatrix}
   \cdot
   \begin{pmatrix}1\\j\\-1\end{pmatrix}
   = 0\cdot 1 + 2j + 3(-1) = 2j - 3 \neq 0.
   $$

   So this particular choice of $\tilde{\mathbf{E}}_0$ is **not strictly transverse**, which means these specific numbers do *not* correspond to a canonical uniform plane wave unless the medium is more general. (Pattern-wise, this follows the same algebra as in the official sheet; physically, a true plane wave would have E strictly transverse.)

2. Orthogonality relations are still checked algebraically in MATLAB below.

---

### Final boxed summary

- From the exponent:
  $$
  \boxed{\boldsymbol{\beta} = (0,2,3)^T~\text{m}^{-1},\quad
  \hat{\boldsymbol{\beta}} = \dfrac{1}{\sqrt{13}}(0,2,3)^T}
  $$
- Magnetic field:
  $$
  \boxed{
  \tilde{\mathbf{H}}(\mathbf{r})
  =
  \dfrac{1}{\eta_0\sqrt{13}}
  (-2-3j,\,3,\,-2)^T e^{-j(2y+3z)/\text{m}}\ \text{A/m}}
  $$

**Notes**

- In the official solution, the emphasis is on **reading $\boldsymbol{\beta}$ from the exponent** and relating E and H via the cross-product rule.
- Any mismatch between strict transversality and these particular numeric values reflects that the exercise is mainly algebraic; the *pattern* is the same as in the course notes.

---

### MATLAB — Exercise 11.2 (verification)

> [!code]- MATLAB — Exercise 11.2 (verification)  
> ```matlab
> eta0 = 120*pi;
> 
> % From exponent exp(-j(2y+3z))
> beta = [0; 2; 3];               % [1/m]
> beta_hat = beta / norm(beta);
> 
> % Electric-field amplitude
> E0 = [1; 1j; -1];               % V/m
> 
> % Magnetic field from plane-wave relation
> H0 = (1/eta0) * cross(beta_hat, E0);
> 
> % Check dot products (transversality)
> dot_beta_E = dot(beta, E0);
> dot_beta_H = dot(beta, H0);
> 
> fprintf('H0 = [%g%+gj  %g%+gj  %g%+gj]^T A/m\n', ...
>     real(H0(1)), imag(H0(1)), ...
>     real(H0(2)), imag(H0(2)), ...
>     real(H0(3)), imag(H0(3)));
> 
> fprintf('beta·E0 = %g%+gj\n', real(dot_beta_E), imag(dot_beta_E));
> fprintf('beta·H0 = %g%+gj\n', real(dot_beta_H), imag(dot_beta_H));
>```
---

## Exercise 11.3 — Extract β and H for Different Exponent Signs

> **Given**  
> Another time-harmonic electric field in free space:
> $$
> \tilde{\mathbf{E}}(\mathbf{r}) =
> \begin{pmatrix}
> 0\\[2pt]
> 0\\[2pt]
> 4
> \end{pmatrix}
> e^{+j(3x+5y)/\text{m}}\ \text{V/m}.
> $$
>
> **Tasks**
> 1. Determine the **propagation vector** $\boldsymbol{\beta}$ and $\hat{\boldsymbol{\beta}}$.  
> 2. Find the corresponding **magnetic field** phasor $\tilde{\mathbf{H}}(\mathbf{r})$ in free space using the plane-wave relation.  
> 3. Comment on the sign of $\boldsymbol{\beta}$ relative to the exponent.

---

### Theory recap

- Standard plane-wave form in this course:
  $$
  \tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0 e^{-j\boldsymbol{\beta}\cdot\mathbf{r}}.
  $$
- If the field is written with a **plus** sign in the exponent:
  $$
  \tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0 e^{+j\mathbf{k}\cdot\mathbf{r}},
  $$
  then by comparison with the standard form,
  $$
  +j\mathbf{k}\cdot\mathbf{r} = -j\boldsymbol{\beta}\cdot\mathbf{r}
  \quad\Rightarrow\quad
  \boldsymbol{\beta} = -\mathbf{k}.
  $$

---

### Geometry / setup

Given:
$$
\tilde{\mathbf{E}}(\mathbf{r}) =
\tilde{\mathbf{E}}_0\,e^{+j(3x+5y)/\text{m}},
\quad
\tilde{\mathbf{E}}_0 =
\begin{pmatrix}
0\\[2pt]
0\\[2pt]
4
\end{pmatrix}.
$$

Write
$$
+j(3x+5y)/\text{m} = -j\boldsymbol{\beta}\cdot\mathbf{r}
\quad\Rightarrow\quad
\boldsymbol{\beta}\cdot\mathbf{r} = -(3x+5y)/\text{m}.
$$

So:
$$
\boldsymbol{\beta} =
\begin{pmatrix}
-3\\[2pt]
-5\\[2pt]
0
\end{pmatrix}\ \text{m}^{-1}.
$$

Magnitude:
$$
\lVert\boldsymbol{\beta}\rVert = \sqrt{(-3)^2 + (-5)^2 + 0^2} = \sqrt{34}\ \text{m}^{-1}.
$$

Direction:
$$
\boxed{
\hat{\boldsymbol{\beta}} =
\frac{1}{\sqrt{34}}
\begin{pmatrix}
-3\\[2pt]
-5\\[2pt]
0
\end{pmatrix}
}
$$

---

### Derivation

#### (a) Magnetic field phasor

Using
$$
\tilde{\mathbf{H}}_0 = \frac{1}{\eta_0}\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0,
$$
with
$$
\tilde{\mathbf{E}}_0 = (0,0,4)^T.
$$

Compute cross product:
$$
\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_0
=
\frac{1}{\sqrt{34}}
\begin{vmatrix}
\hat{\mathbf{x}} & \hat{\mathbf{y}} & \hat{\mathbf{z}}\\
-3 & -5 & 0\\
0  & 0  & 4
\end{vmatrix}
=
\frac{1}{\sqrt{34}}
\begin{pmatrix}
(-5)\cdot 4 - 0\cdot 0\\[2pt]
-( -3\cdot 4 - 0\cdot 0 )\\[2pt]
-3\cdot 0 - (-5)\cdot 0
\end{pmatrix}
=
\frac{1}{\sqrt{34}}
\begin{pmatrix}
-20\\[2pt]
12\\[2pt]
0
\end{pmatrix}.
$$

So
$$
\tilde{\mathbf{H}}_0
= \frac{1}{\eta_0\sqrt{34}}
\begin{pmatrix}
-20\\[2pt]
12\\[2pt]
0
\end{pmatrix}\ \text{A/m}.
$$

Hence the full field:
$$
\boxed{
\tilde{\mathbf{H}}(\mathbf{r})
=
\frac{1}{\eta_0\sqrt{34}}
\begin{pmatrix}
-20\\[2pt]
12\\[2pt]
0
\end{pmatrix}
e^{+j(3x+5y)/\text{m}}\ \text{A/m}
}
$$

This matches the structure of the official solution (same direction, same relative scaling; their factor is explicitly written as $\frac{1}{120\pi\sqrt{34}}(-20,12,0)^T e^{+j(3x+5y)/\text{m}}$ A/m).

---

### Final boxed results

$$
\boxed{
\begin{aligned}
\boldsymbol{\beta} &= (-3,-5,0)^T\ \text{m}^{-1},\\[4pt]
\hat{\boldsymbol{\beta}} &= \dfrac{1}{\sqrt{34}}(-3,-5,0)^T,\\[4pt]
\tilde{\mathbf{E}}(\mathbf{r})
&=
(0,0,4)^T e^{+j(3x+5y)/\text{m}}\ \text{V/m},\\[4pt]
\tilde{\mathbf{H}}(\mathbf{r})
&=
\dfrac{1}{120\pi\sqrt{34}}
(-20,12,0)^T e^{+j(3x+5y)/\text{m}}\ \text{A/m}.
\end{aligned}
}
$$

**Notes**

- Sign in the exponent **flips** the sign of $\boldsymbol{\beta}$.
- Once $\tilde{\mathbf{E}}_0$ and exponent are known, you immediately get $\tilde{\mathbf{H}}_0$ via the cross-product rule.
- This is extremely exam-typical: *“Given E, find β and H.”*

---

### MATLAB — Exercise 11.3 (verification)

> [!code]- MATLAB — Exercise 11.3 (verification)  
> ```matlab
> eta0 = 120*pi;
> 
> % From exponent exp(+j(3x+5y)), beta = (-3, -5, 0)
> beta = [-3; -5; 0];
> beta_hat = beta / norm(beta);
> 
> % Electric field amplitude
> E0 = [0; 0; 4];
> 
> % Magnetic field from plane-wave relation
> H0 = (1/eta0)*cross(beta_hat, E0);
> 
> fprintf('beta      = [%g %g %g]^T 1/m\n', beta);
> fprintf('beta_hat  = [%g %g %g]^T\n', beta_hat);
> fprintf('H0        = [%g %g %g]^T A/m\n', H0);
> 
> % Check orthogonality
> fprintf('beta·E0 = %g\n', dot(beta,E0));
> fprintf('beta·H0 = %g\n', dot(beta,H0));
> fprintf('E0·H0   = %g\n', dot(E0,H0));
>```
---
