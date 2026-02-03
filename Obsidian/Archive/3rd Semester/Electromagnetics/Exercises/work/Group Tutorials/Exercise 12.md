> Quick refs: [[Courses/Electromagnetics/Formulas/Plane Waves & Polarization]], [[Courses/Electromagnetics/Formulas/Vector Calculus & Coordinates]]  
> Source: Official solution sheet — Exercise 12 (polarization) 

---

# Exercise 12 — Plane Wave: Wave Polarization

---

## Exercise 12.1 — Identify Polarization Type (L / C / E)

> **Problem**  
> For each of the following EM plane waves, determine whether the polarization is:
> - **Linear**
> - **Circular**
> - **Elliptical**
>
> For phasor-domain fields we write:
> $$
 \tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0 e^{-j\boldsymbol{\beta}\cdot\mathbf{r}}
 $$
> and we decompose
> $$
 \tilde{\mathbf{E}}_0 = \tilde{\mathbf{E}}_{0r} + j\tilde{\mathbf{E}}_{0i},
 $$
> where $\tilde{\mathbf{E}}_{0r}, \tilde{\mathbf{E}}_{0i} \in \mathbb{R}^3$.
>
> (a)  
> $$
 \tilde{\mathbf{E}} =
 (\hat{\mathbf{x}}+\hat{\mathbf{y}}+\hat{\mathbf{z}})
 e^{j(x-y)/\text{m}} \ \text{V/m}
 $$
>
> (b)  
> $$
 \tilde{\mathbf{E}} =
 \begin{pmatrix}
 1 - j\\
 1 + j\\
 0
 \end{pmatrix}
 e^{-j3z/\text{m}}\ \text{V/m}
 $$
>
> (c)  
> $$
 \mathbf{E}(\mathbf{r},t) =
 \begin{pmatrix}
 1\\[2pt]
 1\\[2pt]
 \sqrt{2}
 \end{pmatrix}
 \cos\!\left(\omega t - \frac{x+y-\sqrt{2}z}{\text{m}}\right)
 -
 \begin{pmatrix}
 \sqrt{2}\\[2pt]
 \sqrt{2}\\[2pt]
 2
 \end{pmatrix}
 \sin\!\left(\omega t - \frac{x+y-\sqrt{2}z}{\text{m}}\right)\ \text{V/m}
 $$
>
> (d)  
> $$
 \mathbf{E}(\mathbf{r},t) =
 \begin{pmatrix}
 1\\[2pt]
 1\\[2pt]
 \sqrt{2}
 \end{pmatrix}
 \cos\!\left(\omega t - \frac{x+y-\sqrt{2}z}{\text{m}}\right)
 +
 \frac{1}{\sqrt{3}}
 \begin{pmatrix}
 3\\[2pt]
 -1\\[2pt]
 \sqrt{2}
 \end{pmatrix}
 \sin\!\left(\omega t - \frac{x+y-\sqrt{2}z}{\text{m}}\right)\ \text{V/m}
 $$
>
> (e)  
> $$
 \tilde{\mathbf{E}} =
 \begin{pmatrix}
 \sqrt{2} - j\\[2pt]
 1 + j3\\[2pt]
 \sqrt{2}(1+j)
 \end{pmatrix}
 e^{-j(x+y-\sqrt{2}z)/\text{m}}\ \text{V/m}
 $$

---

### Theory recap — Polarization via phasor parts

Using Ulaby & Ravaioli’s time-harmonic convention:
$$
\mathbf{E}(\mathbf{r},t) = \Re\{\tilde{\mathbf{E}}_0 e^{j(\omega t - \boldsymbol{\beta}\cdot\mathbf{r})}\}
= \tilde{\mathbf{E}}_{0r}\cos(\omega t - \boldsymbol{\beta}\cdot\mathbf{r})
- \tilde{\mathbf{E}}_{0i}\sin(\omega t - \boldsymbol{\beta}\cdot\mathbf{r}),
$$
where
$$
\tilde{\mathbf{E}}_0 = \tilde{\mathbf{E}}_{0r} + j\tilde{\mathbf{E}}_{0i}.
$$

Polarization type:

- **Linear** if  
  $$
  \tilde{\mathbf{E}}_{0r} \times \tilde{\mathbf{E}}_{0i} = \mathbf{0}.
  $$
- **Circular** if  
  $$
  \tilde{\mathbf{E}}_{0r}\times\tilde{\mathbf{E}}_{0i} \neq 0,\quad
  \lVert\tilde{\mathbf{E}}_{0r}\rVert = \lVert\tilde{\mathbf{E}}_{0i}\rVert,\quad
  \tilde{\mathbf{E}}_{0r}\cdot\tilde{\mathbf{E}}_{0i} = 0.
  $$
- **Elliptical** otherwise.

These tests only use the **constant phasor amplitude** $\tilde{\mathbf{E}}_0$, not the spatial exponential.

---

### (a) $\tilde{\mathbf{E}} = (\hat{\mathbf{x}}+\hat{\mathbf{y}}+\hat{\mathbf{z}})e^{j(x-y)/\text{m}}$

Phasor amplitude:
$$
\tilde{\mathbf{E}}_0 = (1,1,1)^T.
$$

Real and imaginary parts:
$$
\tilde{\mathbf{E}}_{0r} = (1,1,1)^T,
\qquad
\tilde{\mathbf{E}}_{0i} = (0,0,0)^T.
$$

Then
$$
\tilde{\mathbf{E}}_{0r}\times\tilde{\mathbf{E}}_{0i} = \mathbf{0}.
$$

So the polarization is **linear**.

$$
\boxed{\text{(a) linearly polarized}}
$$

---

### (b) $\tilde{\mathbf{E}} = (1-j,\ 1+j,\ 0)^T e^{-j3z/\text{m}}$

Phasor amplitude:
$$
\tilde{\mathbf{E}}_0 = (1-j,\ 1+j,\ 0)^T.
$$

Real/imaginary parts:
$$
\tilde{\mathbf{E}}_{0r} =
\begin{pmatrix}1\\1\\0\end{pmatrix},
\qquad
\tilde{\mathbf{E}}_{0i} =
\begin{pmatrix}-1\\1\\0\end{pmatrix}.
$$

1. Linear test:
$$
\tilde{\mathbf{E}}_{0r}\times\tilde{\mathbf{E}}_{0i}
=
\begin{pmatrix}0\\0\\2\end{pmatrix}
\neq \mathbf{0}
\quad\Rightarrow\quad
\text{not linear}.
$$

2. Circular tests:
   - Magnitudes:
     $$
     \lVert\tilde{\mathbf{E}}_{0r}\rVert^2 = 1^2+1^2 = 2,
     \quad
     \lVert\tilde{\mathbf{E}}_{0i}\rVert^2 = (-1)^2+1^2 = 2.
     $$
     So $\lVert\tilde{\mathbf{E}}_{0r}\rVert = \lVert\tilde{\mathbf{E}}_{0i}\rVert$.
   - Orthogonality:
     $$
     \tilde{\mathbf{E}}_{0r}\cdot\tilde{\mathbf{E}}_{0i}
     = 1(-1) + 1(1) + 0\cdot 0 = -1+1=0.
     $$

All circular conditions are satisfied.

$$
\boxed{\text{(b) circularly polarized}}
$$

---

### (c) Given directly in time domain

We rewrite in the standard form
$$
\mathbf{E}(\mathbf{r},t) = \tilde{\mathbf{E}}_{0r}\cos\Psi - \tilde{\mathbf{E}}_{0i}\sin\Psi,
\quad
\Psi = \omega t - \frac{x+y-\sqrt{2}z}{\text{m}}.
$$

Given:
$$
\tilde{\mathbf{E}}_{0r} =
\begin{pmatrix}
1\\1\\\sqrt{2}
\end{pmatrix},
\qquad
\tilde{\mathbf{E}}_{0i} =
\begin{pmatrix}
\sqrt{2}\\\sqrt{2}\\2
\end{pmatrix}.
$$

Check linearity:

1. Cross product:
   $$
   \tilde{\mathbf{E}}_{0r}\times\tilde{\mathbf{E}}_{0i} = \mathbf{0}.
   $$
   (You can verify by writing $\tilde{\mathbf{E}}_{0i} = \sqrt{2}\,\tilde{\mathbf{E}}_{0r}$.)
2. So the imaginary part is just a **real scalar multiple** of the real part.

Therefore the tip of $\mathbf{E}(\mathbf{r},t)$ moves along a single line.

$$
\boxed{\text{(c) linearly polarized}}
$$

---

### (d) Time-domain with non-collinear real/imag parts

Again
$$
\mathbf{E}(\mathbf{r},t)
= \tilde{\mathbf{E}}_{0r}\cos\Psi - \tilde{\mathbf{E}}_{0i}\sin\Psi,\quad
\Psi = \omega t - \frac{x+y-\sqrt{2}z}{\text{m}}.
$$

From the expression:
$$
\tilde{\mathbf{E}}_{0r} =
\begin{pmatrix}
1\\1\\\sqrt{2}
\end{pmatrix},
\qquad
\tilde{\mathbf{E}}_{0i} =
-\frac{1}{\sqrt{3}}
\begin{pmatrix}
3\\-1\\\sqrt{2}
\end{pmatrix}.
$$

1. Linear test:
   $$
   \tilde{\mathbf{E}}_{0r}\times\tilde{\mathbf{E}}_{0i}
   = -\frac{1}{\sqrt{3}}
   \begin{pmatrix}
   2\sqrt{2}\\[2pt]
   2\sqrt{2}\\[2pt]
   -4
   \end{pmatrix}
   \neq \mathbf{0}.
   $$
   So not linear.

2. Circular tests:
   - Magnitudes:
     $$
     \lVert\tilde{\mathbf{E}}_{0r}\rVert^2 = 1+1+2 = 4 \Rightarrow \lVert\tilde{\mathbf{E}}_{0r}\rVert = 2
     $$
     For $\tilde{\mathbf{E}}_{0i}$:
     $$
     \left\lVert\tilde{\mathbf{E}}_{0i}\right\rVert^2
     = \frac{1}{3}(3^2 + (-1)^2 + (\sqrt{2})^2)
     = \frac{1}{3}(9+1+2) = \frac{12}{3} = 4.
     $$
     So $\lVert\tilde{\mathbf{E}}_{0i}\rVert = 2$ as well.
   - Dot product:
     $$
     \tilde{\mathbf{E}}_{0r}\cdot\tilde{\mathbf{E}}_{0i}
     = -\frac{1}{\sqrt{3}}(3 -1 +2) = -\frac{4}{\sqrt{3}} \neq 0.
     $$

So it is not linear and not circular.

$$
\boxed{\text{(d) elliptically polarized}}
$$

---

### (e) Complex phasor amplitude

Phasor amplitude:
$$
\tilde{\mathbf{E}}_0 =
\begin{pmatrix}
\sqrt{2} - j\\
1 + j3\\
\sqrt{2}(1 + j)
\end{pmatrix}.
$$

Real/imaginary parts:
$$
\tilde{\mathbf{E}}_{0r} =
\begin{pmatrix}
\sqrt{2}\\[2pt]
1\\[2pt]
\sqrt{2}
\end{pmatrix},
\qquad
\tilde{\mathbf{E}}_{0i} =
\begin{pmatrix}
-1\\[2pt]
3\\[2pt]
\sqrt{2}
\end{pmatrix}.
$$

1. Linear test:
   - Clearly $\tilde{\mathbf{E}}_{0i}$ is not a scalar multiple of $\tilde{\mathbf{E}}_{0r}$; cross product is non-zero:
     $$
     \tilde{\mathbf{E}}_{0r}\times\tilde{\mathbf{E}}_{0i} \neq \mathbf{0}.
     $$

2. Circular tests:
   - Magnitudes:
     $$
     \lVert\tilde{\mathbf{E}}_{0r}\rVert^2 = 2 + 1 + 2 = 5,
     \qquad
     \lVert\tilde{\mathbf{E}}_{0i}\rVert^2 = 1 + 9 + 2 = 12,
     $$
     so $\lVert\tilde{\mathbf{E}}_{0r}\rVert \neq \lVert\tilde{\mathbf{E}}_{0i}\rVert$.
   - Dot product:
     $$
     \tilde{\mathbf{E}}_{0r}\cdot\tilde{\mathbf{E}}_{0i}
     = \sqrt{2}(-1) + 1\cdot3 + \sqrt{2}\cdot\sqrt{2}
     = -\sqrt{2} + 3 + 2 = 5 - \sqrt{2}\neq 0.
     $$

Thus not circular.

$$
\boxed{\text{(e) elliptically polarized}}
$$

---

### Notes (Exercise 12.1)

- This exercise is a **template**: every plane-wave polarization problem with known $\tilde{\mathbf{E}}_0$ can be classified with exactly these three checks.
- For linear waves, the tip of $\mathbf{E}$ moves on a **line**; for circular, on a **circle**; otherwise an **ellipse**.
- The official solution follows these same tests; our results:
  - (a) linear,
  - (b) circular,
  - (c) linear,
  - (d) elliptical,
  - (e) elliptical — all **match** the sheet.

---

### MATLAB — Exercise 12.1 (polarization classifier)

> [!code]- MATLAB — Exercise 12.1  
> ```matlab
% Polarization classification for generic phasor amplitudes
% Uses:
%   - linear:   cross(E0r, E0i) == 0
%   - circular: |E0r| = |E0i| and E0r·E0i = 0
%   - else:     elliptical
>
clear; clc;
>
% Helper: classify polarization
classifyPol = @(E0) struct( ...
  >  'E0r', real(E0), ...
  >  'E0i', imag(E0), ...
  >  'cross', cross(real(E0), imag(E0)), ...
 >   'dot',   dot(real(E0), imag(E0)), ...
>    'norm_r', norm(real(E0)), ...
 >   'norm_i', norm(imag(E0)));
>
>%% (a)
>E0_a = [1; 1; 1];
>res_a = classifyPol(E0_a)
>
>%% (b)
>E0_b = [1-1j; 1+1j; 0];
>res_b = classifyPol(E0_b)
>
>%% (c)
>E0r_c = [1; 1; sqrt(2)];
>E0i_c = [sqrt(2); sqrt(2); 2];
>E0_c  = E0r_c + 1j*E0i_c;
>res_c = classifyPol(E0_c)
>
>%% (d)
>E0r_d = [1; 1; sqrt(2)];
>E0i_d = -(1/sqrt(3))*[3; -1; sqrt(2)];
>E0_d  = E0r_d + 1j*E0i_d;
>res_d = classifyPol(E0_d)
>
%% (e)
E0_e = [sqrt(2)-1j; 1+1j*3; sqrt(2)*(1+1j)];
res_e = classifyPol(E0_e)
>
% Inspect fields:
%   res_*.cross   -> zero or not
%   res_*.norm_r, res_*.norm_i, res_*.dot
% Then apply the three polarization rules.
>```
---

## Exercise 12.2 — From Linear to Circular Polarization

> **Given**  
> A plane EM wave in a homogeneous medium with
> $$
 \varepsilon_r = 4,\quad \mu_r = 1.
 $$
> The electric field (time domain) is:
> $$
 \mathbf{E}(\mathbf{r},t) =
 \begin{pmatrix}
 1\\[2pt]
 1\\[2pt]
 2
 \end{pmatrix}
 \cos\bigl(\omega t + (x + y - z)/\text{m}\bigr)\ \text{V/m}.> $$
>
> (a) Find the **direction of propagation**.  
> (b) Find the **frequency** $f$ of the wave.  
> (c) Find a **second electric field** such that the superposition yields a **circularly polarized** wave.  
> (d) For the field in (c), determine whether the resulting circular wave is **left-** or **right-handed**.  
> (e) Give the **polarization ellipse** of the magnetic field.

---

### Theory recap

- Time-domain plane wave:
  $$
  \mathbf{E}(\mathbf{r},t) =
  \tilde{\mathbf{E}}_{0r}\cos(\omega t - \boldsymbol{\beta}\cdot\mathbf{r})
  - \tilde{\mathbf{E}}_{0i}\sin(\omega t - \boldsymbol{\beta}\cdot\mathbf{r}).
  $$
- We must match the term inside the cosine to the canonical form $\omega t - \beta\cdot r$:
  $$
  \cos(\omega t - \beta\cdot r) \quad\leftrightarrow\quad \cos(\omega t + (x+y-z)/\text{m}).
  $$
- In a homogeneous medium:
  $$
  \beta = \lVert\boldsymbol{\beta}\rVert = \frac{\omega}{c}
  = \frac{\omega}{c_0}\sqrt{\varepsilon_r\mu_r},
  $$
  where $c_0$ is the speed of light in vacuum.
- Intrinsic impedance:
  $$
  \eta = \sqrt{\frac{\mu}{\varepsilon}}
  = \eta_0\sqrt{\frac{\mu_r}{\varepsilon_r}}
  = \frac{\eta_0}{\sqrt{\varepsilon_r}}
  \quad\Rightarrow\quad
  \eta = \frac{120\pi}{2} = 60\pi~\Omega.
  $$
- For a plane wave:
  $$
  \tilde{\mathbf{H}} = \frac{1}{\eta}\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}.
  $$

---

### (a) Direction of propagation

We rewrite the cosine argument:
$$
\cos(\omega t + (x+y-z)/\text{m}) = \cos\bigl(\omega t - \beta\cdot r\bigr).
$$

Comparing:
$$
-\boldsymbol{\beta}\cdot\mathbf{r} = x + y - z,
\quad
-\beta_x x - \beta_y y - \beta_z z = x + y - z.
$$

Matching coefficients:
$$
\beta_x = -1,\quad
\beta_y = -1,\quad
\beta_z = 1\quad\Rightarrow\quad
\boldsymbol{\beta} =
\begin{pmatrix}
-1\\[2pt]
-1\\[2pt]
1
\end{pmatrix}\ \text{m}^{-1}.
$$

Unit vector:
$$
\hat{\boldsymbol{\beta}} = \frac{1}{\sqrt{3}}(-1,-1,1)^T.
$$

So the wave propagates along $(-1,-1,1)$ (i.e. diagonally “down” $x$ and $y$, “up” $z$).

$$
\boxed{
\boldsymbol{\beta} = (-1,-1,1)^T/\text{m},\quad
\hat{\boldsymbol{\beta}} = \frac{1}{\sqrt{3}}(-1,-1,1)^T
}
$$

---

### (b) Frequency of the wave

Magnitude:
$$
\lVert\boldsymbol{\beta}\rVert
= \sqrt{(-1)^2+(-1)^2+1^2}
= \sqrt{3}\ \text{m}^{-1}.
$$

Using
$$
\beta = \frac{\omega}{c_0}\sqrt{\varepsilon_r\mu_r}
= \frac{\omega}{c_0}\sqrt{4\cdot 1} = \frac{2\omega}{c_0},
$$
so
$$
\omega = \frac{\beta c_0}{2}.
$$

Frequency:
$$
f = \frac{\omega}{2\pi} = \frac{\beta c_0}{4\pi}
= \frac{c_0}{4\pi}\sqrt{3}.
$$

With $c_0 \approx 3\cdot10^8\ \text{m/s}$:
$$
f \approx \frac{3\cdot10^8\cdot\sqrt{3}}{4\pi}
\approx 41.3\cdot10^6\ \text{Hz}
= 41.3\ \text{MHz}.
$$

$$
\boxed{f \approx 41.3\ \text{MHz}}
$$

---

### (c) Add a second field to get circular polarization

We want a **circularly polarized** total field. Let the total phasor amplitude be
$$
\tilde{\mathbf{E}}_0 = \tilde{\mathbf{E}}_{0r} + j\tilde{\mathbf{E}}_{0i}
$$
with:
- $\tilde{\mathbf{E}}_{0r}$ given by the existing field,
- $\tilde{\mathbf{E}}_{0i}$ to be found.

From the given field:
$$
\mathbf{E}(\mathbf{r},t)
= \tilde{\mathbf{E}}_{0r}\cos(\omega t - \boldsymbol{\beta}\cdot\mathbf{r}),
\quad
\tilde{\mathbf{E}}_{0r} =
\begin{pmatrix}
1\\[2pt]
1\\[2pt]
2
\end{pmatrix}.
$$

For a circularly polarized wave, we require:
- $\tilde{\mathbf{E}}_{0r}\perp \tilde{\mathbf{E}}_{0i}$,
- $\tilde{\mathbf{E}}_{0i}\perp\boldsymbol{\beta}$,
- $\lVert\tilde{\mathbf{E}}_{0r}\rVert = \lVert\tilde{\mathbf{E}}_{0i}\rVert$.

A convenient construction:
$$
\tilde{\mathbf{E}}_{0i} = \hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_{0r}.
$$

Compute:
$$
\hat{\boldsymbol{\beta}} = \frac{1}{\sqrt{3}}(-1,-1,1)^T,
\quad
\tilde{\mathbf{E}}_{0r} = (1,1,2)^T.
$$

Cross product:
$$
\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_{0r}
=
\frac{1}{\sqrt{3}}
\begin{pmatrix}
-1\\-1\\1
\end{pmatrix}
\times
\begin{pmatrix}
1\\1\\2
\end{pmatrix}
=
\frac{1}{\sqrt{3}}
\begin{pmatrix}
-2\\[2pt]
2\\[2pt]
0
\end{pmatrix}
=
\begin{pmatrix}
-\sqrt{3}\\[2pt]
\sqrt{3}\\[2pt]
0
\end{pmatrix}.
$$

So choose
$$
\tilde{\mathbf{E}}_{0i} =
\begin{pmatrix}
-\sqrt{3}\\[2pt]
\sqrt{3}\\[2pt]
0
\end{pmatrix}.
$$

Check magnitudes:
$$
\lVert\tilde{\mathbf{E}}_{0r}\rVert^2 = 1+1+4 = 6,\quad
\lVert\tilde{\mathbf{E}}_{0i}\rVert^2 = 3+3+0 = 6.
$$

So the total **phasor** of the circularly polarized wave is:
$$
\tilde{\mathbf{E}}_0 =
\begin{pmatrix}
1\\1\\2
\end{pmatrix}
+ j
\begin{pmatrix}
-\sqrt{3}\\[2pt]
\sqrt{3}\\[2pt]
0
\end{pmatrix}.
$$

The **second field** we must add is the purely imaginary part:
- Vector-phasor of the added field:
  $$
  \tilde{\mathbf{E}}' = j\tilde{\mathbf{E}}_{0i}\,e^{j(x+y-z)/\text{m}}\ \text{V/m}.
  $$
- Time-domain form (from $\tilde{\mathbf{E}}' = j\tilde{\mathbf{E}}_{0i}$):
  $$
  \mathbf{E}'(\mathbf{r},t)
  = -\tilde{\mathbf{E}}_{0i}\sin\bigl(\omega t + (x+y-z)/\text{m}\bigr).
  $$

So explicitly:
$$
\boxed{
\mathbf{E}'(\mathbf{r},t)
=
-
\begin{pmatrix}
-\sqrt{3}\\[2pt]
\sqrt{3}\\[2pt]
0
\end{pmatrix}
\sin\bigl(\omega t + (x+y-z)/\text{m}\bigr)\ \text{V/m}
=
\begin{pmatrix}
\sqrt{3}\\[2pt]
-\sqrt{3}\\[2pt]
0
\end{pmatrix}
\sin(\cdots)\ \text{V/m}
}
$$

The **total circular field**:
$$
\mathbf{E}_{\text{tot}}(\mathbf{r},t)
=
\begin{pmatrix}
1\\1\\2
\end{pmatrix}
\cos(\omega t + (x+y-z)/\text{m})
-
\begin{pmatrix}
-\sqrt{3}\\[2pt]
\sqrt{3}\\[2pt]
0
\end{pmatrix}
\sin(\omega t + (x+y-z)/\text{m}).
$$

Matches the official solution.

---

### (d) Left- or right-handed?

For a given direction $\hat{\boldsymbol{\beta}}$, the handedness is defined by how $\mathbf{E}(t)$ rotates **as time increases**, viewed in the direction of propagation.

- At $t=0$ and $(x,y,z)$ s.t. phase $=0$, the field starts at $\tilde{\mathbf{E}}_{0r}$.
- As $t$ increases a small amount, $\sin(\omega t) > 0$ and
  $$
  \mathbf{E} \approx \tilde{\mathbf{E}}_{0r} - \tilde{\mathbf{E}}_{0i}\,\omega t,
  $$
  so the tip of $\mathbf{E}$ moves from $\tilde{\mathbf{E}}_{0r}$ towards $-\tilde{\mathbf{E}}_{0i}$.

With
$$
\boldsymbol{\beta} = (-1,-1,1)^T,
\quad
\tilde{\mathbf{E}}_{0r} = (1,1,2)^T,
\quad
\tilde{\mathbf{E}}_{0i} = (-\sqrt{3},\sqrt{3},0)^T,
$$
this rotation is, by the standard convention (as in the solution sheet), **left-handed**.

(If we had chosen $-\tilde{\mathbf{E}}_{0i}$ instead, the rotation sense would flip → right-handed.)

$$
\boxed{\text{(d) resulting circular wave is **left-handed**}}
$$

---

### (e) Polarization ellipse of the magnetic field

For a plane wave:
$$
\mathbf{H}(\mathbf{r},t) = \frac{1}{\eta}\hat{\boldsymbol{\beta}}\times\mathbf{E}(\mathbf{r},t)
= \frac{\sqrt{\varepsilon_r}}{\eta_0}\hat{\boldsymbol{\beta}}\times\mathbf{E}(\mathbf{r},t),
$$
since $\eta = \eta_0/\sqrt{\varepsilon_r}$.

Here $\varepsilon_r=4\Rightarrow\sqrt{\varepsilon_r}=2$, so
$$
\frac{\sqrt{\varepsilon_r}}{\eta_0} = \frac{2}{120\pi} = \frac{1}{60\pi}.
$$

Thus
$$
\mathbf{H}(\mathbf{r},t)
=
\frac{1}{60\pi}
\hat{\boldsymbol{\beta}}\times
\left[
\tilde{\mathbf{E}}_{0r}\cos(\Phi) - \tilde{\mathbf{E}}_{0i}\sin(\Phi)
\right],
\quad
\Phi = \omega t + (x+y-z)/\text{m}.
$$

Using
$$
\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_{0r} = \tilde{\mathbf{E}}_{0i},
\quad
\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{E}}_{0i} = -\tilde{\mathbf{E}}_{0r},
$$
we get
$$
\mathbf{H}(\mathbf{r},t)
= \frac{1}{60\pi}
\left[
\tilde{\mathbf{E}}_{0i}\cos\Phi + \tilde{\mathbf{E}}_{0r}\sin\Phi
\right].
$$

So explicitly:
$$
\boxed{
\mathbf{H}(\mathbf{r},t)
=
\frac{1}{60\pi}
\left[
\begin{pmatrix}
-\sqrt{3}\\[2pt]
\sqrt{3}\\[2pt]
0
\end{pmatrix}
\cos(\omega t + (x+y-z)/\text{m})
+
\begin{pmatrix}
1\\[2pt]
1\\[2pt]
2
\end{pmatrix}
\sin(\omega t + (x+y-z)/\text{m})
\right]\ \text{A/m}
}
$$

The magnetic field has the **same polarization ellipse** as $\mathbf{E}$ (just rotated and scaled by $1/(60\pi)$), still circular in this constructed case.

---

### MATLAB — Exercise 12.2

> [!code]- MATLAB — Exercise 12.2  
> ```matlab
% Exercise 12.2 — From linear to circular polarization
clear; clc;
c0   = 3e8;          % [m/s]
er   = 4;
mur  = 1;
eta0 = 120*pi;
eta  = eta0*sqrt(mur/er);
>
% Given real part of E0
E0r = [1; 1; 2];
>
% Propagation vector from cos(omega t + (x+y-z)):
beta = [-1; -1; 1];             % [1/m]
beta_hat = beta / norm(beta);
>
% (b) frequency
beta_mag = norm(beta);
omega = beta_mag * c0 / sqrt(er*mur);
f     = omega/(2*pi);
>
fprintf('beta      = [%g %g %g]^T 1/m\n', beta);
fprintf('|beta|    = %.4f 1/m\n', beta_mag);
fprintf('f         = %.3e Hz\n', f);
>
% (c) construct imaginary part via beta_hat x E0r
E0i = cross(beta_hat, E0r);
>
fprintf('E0r       = [%g %g %g]^T\n', E0r);
fprintf('E0i       = [%g %g %g]^T\n', E0i);
fprintf('|E0r|     = %.4f\n', norm(E0r));
fprintf('|E0i|     = %.4f\n', norm(E0i));
fprintf('E0r·E0i   = %.4f\n', dot(E0r,E0i));
>
% (e) Magnetic field ellipse: H(r,t) = (1/eta) beta_hat x E(r,t)
syms t x y z real
Phi = omega*t + (x + y - z);
>
Er_t = E0r*cos(Phi) - E0i*sin(Phi);      % E(t) at a given (x,y,z)
Hr_t = (1/eta)*cross(beta_hat, Er_t);   % H(t) via plane-wave relation
>
Hr_t_simpl = simplify(Hr_t)             % should match analytical expression
>```
---

## Exercise 12.3 — Polarization from Given Time-Domain Components

> **Given**  
> The electric field of a time-harmonic plane wave:
> $$
 \mathbf{E}(\mathbf{r},t) = -10\hat{\mathbf{x}}\sin(\omega t - kz - \pi/3)
 -10\hat{\mathbf{y}}\sin(\omega t - kz).
 $$
> Assume $k>0$.
>
> (a) Determine the **direction of propagation**.  
> (b) Determine the **type of polarization** (L / C / E).  
> (c) Is the wave **left- or right-handed**?  
> (d) Determine the **major and minor semi-axes** of the polarization ellipse (vectors and magnitudes).  
> (e) Determine the **axial ratio** $AR$.  
> (f) Find the **tilt angle** $\tau$ (relative to the $x$-axis) of the ellipse.

---

### (a) Direction of propagation

The phase argument is:
$$
\omega t - kz \equiv \omega t - \beta\cdot r.
$$

Thus
$$
-\beta\cdot r = -kz \quad\Rightarrow\quad \beta = k\hat{\mathbf{z}},\quad \hat{\boldsymbol{\beta}} = \hat{\mathbf{z}}.
$$

So the wave propagates in the **$+z$ direction**.

$$
\boxed{\boldsymbol{\beta} = k\hat{\mathbf{z}},\ \hat{\boldsymbol{\beta}}=\hat{\mathbf{z}}}
$$

---

### (b) Polarization type

We must extract a single common phase argument. Let
$$
\Psi = \omega t - kz.
$$

Rewrite the $x$-component:
$$
\sin(\Psi - \pi/3) = \sin\Psi\cos\frac{\pi}{3} - \cos\Psi\sin\frac{\pi}{3}.
$$

Then
$$
\begin{aligned}
E_x(\mathbf{r},t)
&= -10\sin(\Psi - \pi/3) \\
&= -10\left[\sin\Psi\cos\frac{\pi}{3} - \cos\Psi\sin\frac{\pi}{3}\right] \\
&= -10\cos\frac{\pi}{3}\sin\Psi + 10\sin\frac{\pi}{3}\cos\Psi.
\end{aligned}
$$

$E_y$ is:
$$
E_y(\mathbf{r},t) = -10\sin\Psi.
$$

So in vector notation:
$$
\mathbf{E}(\mathbf{r},t)
=
10
\begin{pmatrix}
\sin\frac{\pi}{3}\\[2pt]
0\\[2pt]
0
\end{pmatrix}
\cos\Psi
-10
\begin{pmatrix}
\cos\frac{\pi}{3}\\[2pt]
1\\[2pt]
0
\end{pmatrix}
\sin\Psi.
$$

Therefore:
$$
\tilde{\mathbf{E}}_{0r} = 10
\begin{pmatrix}
\sin\frac{\pi}{3}\\[2pt]
0\\[2pt]
0
\end{pmatrix},
\qquad
\tilde{\mathbf{E}}_{0i} = 10
\begin{pmatrix}
\cos\frac{\pi}{3}\\[2pt]
1\\[2pt]
0
\end{pmatrix}.
$$

Compute magnitudes:
$$
\lVert\tilde{\mathbf{E}}_{0r}\rVert = 10\left|\sin\frac{\pi}{3}\right| = 10\cdot\frac{\sqrt{3}}{2} = 5\sqrt{3},
$$
$$
\lVert\tilde{\mathbf{E}}_{0i}\rVert = 10\sqrt{\cos^2\frac{\pi}{3} + 1^2}
= 10\sqrt{\left(\frac{1}{2}\right)^2 + 1}
= 10\sqrt{\frac{1}{4} + 1}
= 10\sqrt{\frac{5}{4}} = 5\sqrt{5}.
$$

Clearly $\lVert\tilde{\mathbf{E}}_{0r}\rVert \neq \lVert\tilde{\mathbf{E}}_{0i}\rVert$.

Cross product:
$$
\tilde{\mathbf{E}}_{0r}\times\tilde{\mathbf{E}}_{0i}
= 10^2\sin\frac{\pi}{3}\, \hat{\mathbf{x}}\times
\begin{pmatrix}
\cos\frac{\pi}{3}\\[2pt]
1\\[2pt]
0
\end{pmatrix}
= 100\sin\frac{\pi}{3}\left(0\hat{\mathbf{x}} + 0\hat{\mathbf{y}} + 1\hat{\mathbf{z}}\right)
\neq 0.
$$

Thus:
- Not linear (cross product $\neq 0$),
- Not circular ($|E_{0r}|\neq |E_{0i}|$),

So polarization is **elliptical**.

$$
\boxed{\text{(b) elliptically polarized}}
$$

---

### (c) Left- or right-handed?

The plane wave propagates along $+\hat{\mathbf{z}}$. The polarization sense is determined by how $\mathbf{E}$ rotates in the transverse $(x,y)$ plane as $t$ increases at fixed $(x,y,z)$.

From the decomposition:
$$
\mathbf{E}(\mathbf{r},t)
= \tilde{\mathbf{E}}_{0r}\cos\Psi - \tilde{\mathbf{E}}_{0i}\sin\Psi,
$$
$\mathbf{E}$ moves from $\tilde{\mathbf{E}}_{0r}$ towards $-\tilde{\mathbf{E}}_{0i}$ as $t$ increases slightly.

Plotting or sketching $\tilde{\mathbf{E}}_{0r}$ and $-\tilde{\mathbf{E}}_{0i}$ in the $xy$-plane and using the propagation direction $\hat{\mathbf{z}}$, one finds that the tip of $\mathbf{E}$ rotates **clockwise** when viewed in the direction of propagation ($+z$). By the usual convention, this corresponds to a **left-handed** elliptically polarized wave (matching the official sheet).

$$
\boxed{\text{(c) left-handed elliptically polarized}}
$$

---

### (d) Major and minor semi-axes of the polarization ellipse

Let
$$
\mathbf{E}(\Psi) =
\tilde{\mathbf{E}}_{0r}\cos\Psi - \tilde{\mathbf{E}}_{0i}\sin\Psi.
$$

In the polarization theory (see slides/Ulaby), the major/minor axes can be written as
$$
\mathbf{E}_1 = \tilde{\mathbf{E}}_{0r}\cos\phi_1 - \tilde{\mathbf{E}}_{0i}\sin\phi_1,
$$
$$
\mathbf{E}_2 = \tilde{\mathbf{E}}_{0r}\cos\phi_2 - \tilde{\mathbf{E}}_{0i}\sin\phi_2,
$$
with
$$
\phi_1 = \frac{1}{2}\arctan\left(\frac{2\tilde{\mathbf{E}}_{0r}\cdot\tilde{\mathbf{E}}_{0i}}
{\lVert\tilde{\mathbf{E}}_{0i}\rVert^2 - \lVert\tilde{\mathbf{E}}_{0r}\rVert^2}\right),
\qquad
\phi_2 = \phi_1 + \frac{\pi}{2}.
$$

Using the results from the solution sheet (and one can verify numerically):

- One finds
  $$
  \phi_1 = \frac{\pi}{6}=30^\circ,\quad \phi_2 = \frac{2\pi}{3}=120^\circ.
  $$

Then the **axis vectors** are:
$$
\mathbf{E}_1 = 5
\begin{pmatrix}
1\\[2pt]
-1\\[2pt]
0
\end{pmatrix},
\qquad
\mathbf{E}_2 = -5\sqrt{3}
\begin{pmatrix}
1\\[2pt]
1\\[2pt]
0
\end{pmatrix}.
$$

Lengths:
$$
|\mathbf{E}_1| = 5\sqrt{2},
\qquad
|\mathbf{E}_2| = 5\sqrt{6}.
$$

So:
- **Minor** semi-axis: $\boldsymbol{\zeta} = \mathbf{E}_1$, $a_\zeta = 5\sqrt{2}$.
- **Major** semi-axis: $\boldsymbol{\xi} = \mathbf{E}_2$, $a_\xi = 5\sqrt{6}$.

$$
\boxed{
\begin{aligned}
\text{major semi-axis:}\quad &\boldsymbol{\xi} = \mathbf{E}_2,\quad a_\xi = 5\sqrt{6},\\
\text{minor semi-axis:}\quad &\boldsymbol{\zeta} = \mathbf{E}_1,\quad a_\zeta = 5\sqrt{2}.
\end{aligned}
}
$$

---

### (e) Axial ratio

Axial ratio:
$$
AR = -\frac{a_\xi}{a_\zeta}
= -\frac{5\sqrt{6}}{5\sqrt{2}}
= -\sqrt{3}.
$$

The **negative sign** indicates left-handed polarization (consistent with part (c)).

$$
\boxed{AR = -\sqrt{3}}
$$

---

### (f) Tilt angle $\tau$ of the ellipse

The tilt angle $\tau$ is the angle of the **major axis** with respect to the $x$-axis.

We use $\mathbf{E}_2$:
$$
\mathbf{E}_2 = -5\sqrt{3}(1,1,0)^T.
$$

The direction of $\mathbf{E}_2$ is proportional to $(1,1,0)$, so:
$$
\tan\tau = \frac{E_{2y}}{E_{2x}} = 1 \Rightarrow \tau = 45^\circ = \frac{\pi}{4}.
$$

$$
\boxed{\tau = 45^\circ}
$$

---

### MATLAB — Exercise 12.3 (ellipse parameters)

> [!code]- MATLAB — Exercise 12.3 
> ```matlab 
% Exercise 12.3 — polarization ellipse from time-domain E
clear; clc;
syms t z k omega real
Psi = omega*t - k*z;
>
% Original field:
Ex = -10*sin(Psi - pi/3);
Ey = -10*sin(Psi);
Ez = 0;
>
% Rewrite as E0r*cos(Psi) - E0i*sin(Psi)
% Using identities, we already know:
E0r = 10*[sin(pi/3); 0; 0];
E0i = 10*[cos(pi/3); 1; 0];
>
norm_r = norm(E0r);
norm_i = norm(E0i);
cross_ri = cross(E0r, E0i);
>
fprintf('|E0r|   = %.4f\n', norm_r);
fprintf('|E0i|   = %.4f\n', norm_i);
fprintf('E0r×E0i = [%g %g %g]^T\n', cross_ri);
>
% Compute phi1, phi2 from formula
phi1 = 0.5*atan( 2*dot(E0r,E0i) / (norm(E0i)^2 - norm(E0r)^2) );
phi2 = phi1 + pi/2;
>
phi1_val = double(phi1)
phi2_val = double(phi2)
>
% Major/minor axis vectors:
E1 = E0r*cos(phi1) - E0i*sin(phi1);
E2 = E0r*cos(phi2) - E0i*sin(phi2);
>
E1_simpl = simplify(E1);
E2_simpl = simplify(E2);
>
E1_len = simplify(norm(E1));
E2_len = simplify(norm(E2));
>
fprintf('E1      = [%s %s %s]^T\n', char(E1_simpl(1)), char(E1_simpl(2)), char(E1_simpl(3)));
fprintf('E2      = [%s %s %s]^T\n', char(E2_simpl(1)), char(E2_simpl(2)), char(E2_simpl(3)));
fprintf('|E1|    = %s\n', char(E1_len));
fprintf('|E2|    = %s\n', char(E2_len));
>
% Axial ratio
AR = -E2_len / E1_len;
AR_simpl = simplify(AR)
>
% Tilt angle relative to x-axis from E2 direction
tau = atan(E2_simpl(2)/E2_simpl(1));
tau_val = double(tau)
>```
