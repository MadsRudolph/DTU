> Quick refs: [[Lecture 11 Plane Waves Lossles]], 

---

# Exercise 10 — Plane Wave: Vector-Phasor

---

## Exercise 10.1  
### Time-Domain Fields from Given Vector-Phasors

> **Problem**  
> Find the **time-domain vector fields** from the given **vector-phasors** (phasor-domain fields).  
>  
> (All fields are time-harmonic with angular frequency $\omega$.)  
> (a)  
> $$
 \tilde{\mathbf{E}}(\mathbf{r}) =
 \begin{pmatrix}
 2\\[2pt]
 0\\[2pt]
 -1
 \end{pmatrix}
 e^{-j(x + y + z)/\text{m}}
 \ \ \text{V/m}
 $$
>
> (b)  
> $$
 \tilde{\mathbf{E}}(\mathbf{r})
 = \big[(5-j)\hat{\mathbf{x}} - (3+2j)\hat{\mathbf{y}} + (j+2)\hat{\mathbf{z}}\big]
 e^{\,j\big(\frac{2x-3y}{\text{m}} + 0.1\big)}\ \ \text{V/m}
 $$
>
> (c)  
> $$
 \tilde{\mathbf{H}}(\mathbf{r}) =
 \begin{pmatrix}
 0\\[2pt]
 j\\[2pt]
 -j
 \end{pmatrix}
 e^{\frac{-x + 3z - j 5y}{\text{m}}}
 \ \ \text{A/m}
 $$

---

### Theory recap

- Time-harmonic fields in Ulaby & Ravaioli are written as
  $$
  \mathbf{E}(\mathbf{r},t) = \Re\{\tilde{\mathbf{E}}(\mathbf{r})e^{j\omega t}\},\quad
  \mathbf{H}(\mathbf{r},t) = \Re\{\tilde{\mathbf{H}}(\mathbf{r})e^{j\omega t}\}.
  $$
- If
  $$
  \tilde{E} = A e^{j\phi},
  $$
  then
  $$
  \Re\{\tilde{E} e^{j\omega t}\}
  = \Re\{A e^{j(\omega t + \phi)}\}
  = A\cos(\omega t + \phi).
  $$
- If the phasor has factors like $e^{-j k\cdot r}$ or $e^{\alpha(\mathbf{r})}$, those stay as **spatial dependence** in the time-domain field.

Key pattern:
- Constant complex vector amplitude $\tilde{\mathbf{E}}_0$ and spatial phase $\Phi(\mathbf{r})$:
  $$
  \tilde{\mathbf{E}}(\mathbf{r}) = \tilde{\mathbf{E}}_0 e^{j\Phi(\mathbf{r})}
  \quad\Rightarrow\quad
  \mathbf{E}(\mathbf{r},t) = \Re\{\tilde{\mathbf{E}}_0 e^{j(\omega t + \Phi(\mathbf{r}))}\}.
  $$

---

### Geometry / setup

- Coordinate system: standard **Cartesian** $(x,y,z)$.
- No specific propagation medium is needed for this exercise; we only convert between phasor and time domain.
- Spatial phase terms:
  - (a) $\Phi(\mathbf{r}) = -\dfrac{x+y+z}{\text{m}}$  
  - (b) $\Phi(\mathbf{r}) = \dfrac{2x-3y}{\text{m}} + 0.1$  
  - (c) $\Phi(\mathbf{r}) = -\dfrac{5y}{\text{m}}$ plus a **real amplitude factor** $e^{(-x+3z)/\text{m}}$.

---

### Derivation

We always use
$$
\mathbf{F}(\mathbf{r},t) = \Re\{\tilde{\mathbf{F}}(\mathbf{r}) e^{j\omega t}\}
$$
component-wise.

---

#### (a) From simple constant vector phasor

Given:
$$
\tilde{\mathbf{E}}(\mathbf{r}) =
\begin{pmatrix}
2\\[2pt]
0\\[2pt]
-1
\end{pmatrix}
e^{-j(x + y + z)/\text{m}}.
$$

Time-domain field:
$$
\mathbf{E}(\mathbf{r},t)
= \Re\left\{
\begin{pmatrix}
2\\[2pt]
0\\[2pt]
-1
\end{pmatrix}
e^{j\omega t} e^{-j(x+y+z)/\text{m}}
\right\}.
$$

The spatial factor is **purely real phase** in the exponential, so
$$
\mathbf{E}(\mathbf{r},t)
=
\begin{pmatrix}
2\\[2pt]
0\\[2pt]
-1
\end{pmatrix}
\cos\!\left(\omega t - \frac{x+y+z}{\text{m}}\right)
\ \ \text{V/m}.
$$

So
$$
\boxed{
\mathbf{E}(\mathbf{r},t)
=
\begin{pmatrix}
2\\[2pt]
0\\[2pt]
-1
\end{pmatrix}
\cos\!\left(\omega t - \frac{x+y+z}{\text{m}}\right)\ \text{V/m}
}
$$

Matches the official solution (identical expression).

---

#### (b) From general complex vector amplitude

Given:
$$
\tilde{\mathbf{E}}(\mathbf{r})
= \big[(5-j)\hat{\mathbf{x}} - (3+2j)\hat{\mathbf{y}} + (j+2)\hat{\mathbf{z}}\big]
e^{\,j\left(\frac{2x-3y}{\text{m}}+0.1\right)}.
$$

Write
$$
\tilde{\mathbf{E}}(\mathbf{r})
= \tilde{\mathbf{E}}_0\, e^{j\Phi(\mathbf{r})},
\quad
\tilde{\mathbf{E}}_0 =
\begin{pmatrix}
5-j\\[2pt]
-(3+2j)\\[2pt]
j+2
\end{pmatrix},
\quad
\Phi(\mathbf{r}) = \frac{2x - 3y}{\text{m}} + 0.1.
$$

Time-domain field:
$$
\mathbf{E}(\mathbf{r},t) = \Re\{\tilde{\mathbf{E}}_0 e^{j(\omega t + \Phi(\mathbf{r}))}\}.
$$

We treat each component separately.

Let $\Psi(\mathbf{r},t) = \omega t + \Phi(\mathbf{r})$.

- $x$-component:
  $$
  (5-j)e^{j\Psi}
  = (5-j)(\cos\Psi + j\sin\Psi)
  = (5\cos\Psi + \sin\Psi) + j(5\sin\Psi - \cos\Psi).
  $$
  Real part:
  $$
  E_x(\mathbf{r},t) = 5\cos\Psi + \sin\Psi.
  $$

- $y$-component:
  $$
  -(3+2j)e^{j\Psi}
  = -(3+2j)(\cos\Psi + j\sin\Psi)
  = (-3\cos\Psi + 2\sin\Psi) + j(-3\sin\Psi - 2\cos\Psi).
  $$
  Real part:
  $$
  E_y(\mathbf{r},t) = -3\cos\Psi + 2\sin\Psi.
  $$

- $z$-component:
  $$
  (j+2)e^{j\Psi}
  = (2+j)(\cos\Psi + j\sin\Psi)
  = (2\cos\Psi - \sin\Psi) + j(2\sin\Psi + \cos\Psi).
  $$
  Real part:
  $$
  E_z(\mathbf{r},t) = 2\cos\Psi - \sin\Psi.
  $$

Thus
$$
\boxed{
\mathbf{E}(\mathbf{r},t)
=
\begin{pmatrix}
5\cos\Psi + \sin\Psi\\[2pt]
-3\cos\Psi + 2\sin\Psi\\[2pt]
2\cos\Psi - \sin\Psi
\end{pmatrix}\ \text{V/m},
\quad \Psi = \omega t + \frac{2x-3y}{\text{m}} + 0.1
}
$$

Matches the official solution (same structure and coefficients).

---

#### (c) Phasor with exponential amplitude and spatial attenuation

Given:
$$
\tilde{\mathbf{H}}(\mathbf{r}) =
\begin{pmatrix}
0\\[2pt]
j\\[2pt]
-j
\end{pmatrix}
e^{\frac{-x+3z - j 5y}{\text{m}}}.
$$

Factor real and imaginary parts in the exponent:
$$
e^{\frac{-x+3z - j 5y}{\text{m}}}
= e^{\frac{-x+3z}{\text{m}}} e^{-j 5y/\text{m}}.
$$

So
$$
\tilde{\mathbf{H}}(\mathbf{r})
=
e^{\frac{-x+3z}{\text{m}}}
\begin{pmatrix}
0\\[2pt]
j e^{-j 5y/\text{m}}\\[2pt]
- j e^{-j 5y/\text{m}}
\end{pmatrix}.
$$

Time-domain field:
$$
\mathbf{H}(\mathbf{r},t)
= \Re\{\tilde{\mathbf{H}}(\mathbf{r}) e^{j\omega t}\}
= e^{\frac{-x+3z}{\text{m}}} \Re\left\{
\begin{pmatrix}
0\\[2pt]
j e^{-j 5y/\text{m}}\\[2pt]
- j e^{-j 5y/\text{m}}
\end{pmatrix} e^{j\omega t}
\right\}.
$$

Define $\Theta(\mathbf{r},t) = \omega t - 5y/\text{m}$.

- $x$-component:
  $$
  H_x = 0.
  $$

- $y$-component:
  $$
  j e^{-j 5y/\text{m}} e^{j\omega t}
  = j e^{j(\omega t - 5y/\text{m})}
  = j(\cos\Theta + j\sin\Theta)
  = j\cos\Theta - \sin\Theta.
  $$
  Real part:
  $$
  H_y(\mathbf{r},t) = -\sin\Theta.
  $$

- $z$-component:
  $$
  -j e^{-j 5y/\text{m}} e^{j\omega t}
  = -j e^{j\Theta}
  = -j(\cos\Theta + j\sin\Theta)
  = -j\cos\Theta + \sin\Theta.
  $$
  Real part:
  $$
  H_z(\mathbf{r},t) = \sin\Theta.
  $$

Thus
$$
\boxed{
\mathbf{H}(\mathbf{r},t)
=
e^{\frac{-x+3z}{\text{m}}}
\begin{pmatrix}
0\\[2pt]
-\sin\!\left(\omega t - \frac{5y}{\text{m}}\right)\\[2pt]
\sin\!\left(\omega t - \frac{5y}{\text{m}}\right)
\end{pmatrix}\ \text{A/m}
}
$$

Matches the official solution (same amplitude factor and sin structure).

---

### Notes (Exercise 10.1)

- Main pattern: **phasor $\leftrightarrow$ time domain** using
  $$
  \mathbf{F}(\mathbf{r},t) = \Re\{\tilde{\mathbf{F}}(\mathbf{r})e^{j\omega t}\}.
  $$
- Complex coefficients in front of $e^{j\Phi}$ directly translate into combinations of **$\cos$ and $\sin$** with same spatial phase.
- The real exponential factor $e^{(-x+3z)/\text{m}}$ in (c) is a **spatial attenuation/amplification** and remains as multiplicative factor in the time-domain field.
- Common pitfalls:
  - Forgetting to take the **real part** at the end.
  - Losing minus signs in the phase: $\omega t - kx$ vs. $\omega t + kx$.
  - Mixing up $e^{j\theta}$ with $\cos\theta + j\sin\theta$ (Euler).
- Status: **Matches official solution** (same functional forms and coefficients).

---

### MATLAB — Exercise 10.1 (verification)

> [!code]- MATLAB — Exercise 10.1 (verification)  
> ```matlab
> % 10.1 — Time-domain fields from vector phasors
> % Convention: F(r,t) = real( F_tilde(r) * exp(1j*omega*t) )
> 
> %% Parameters and symbols
> syms x y z t omega real
> 
> % Helper anonymous for "real part of phasor * exp(j*omega*t)"
> timeField = @(Ftilde) real( Ftilde .* exp(1j*omega*t) );
> 
> %% (a) E~ = [2;0;-1] * exp(-j(x+y+z))
> phase_a = -(x + y + z);          % [1/m], unit-less inside exp
> Etilde_a = [2; 0; -1] .* exp(1j*phase_a);
> Ea_t = timeField(Etilde_a);      % symbolic time-domain vector
> 
> % Expected analytic expression:
> Psi_a = omega*t + phase_a;
> Ea_expected = [2; 0; -1] .* cos(Psi_a);
> 
> % Check equality (component-wise):
> simplify(Ea_t - Ea_expected)
> 
> %% (b) General complex amplitude
> phase_b = (2*x - 3*y) + 0.1;     % [1/m], assume "per meter" factor outside
> E0_b = [5 - 1j; -(3 + 2j); (1j + 2)];
> Etilde_b = E0_b .* exp(1j*phase_b);
> Eb_t = timeField(Etilde_b);
> 
> Psi_b = omega*t + phase_b;
> Eb_expected = [ ...
>     5*cos(Psi_b) + sin(Psi_b); ...
>    -3*cos(Psi_b) + 2*sin(Psi_b); ...
>     2*cos(Psi_b) - sin(Psi_b)];
> 
> simplify(Eb_t - Eb_expected)
> 
> %% (c) H~ with spatial attenuation exp((-x+3z)) and phase -5y
> amp_c   = exp(-x + 3*z);         % dimensionless spatial factor
> phase_c = -5*y;                  % [1/m]
> H0_c    = [0; 1j; -1j];
> Htilde_c = amp_c .* H0_c .* exp(1j*phase_c);
> Hc_t     = timeField(Htilde_c);
> 
> Theta_c = omega*t + phase_c;
> Hc_expected = amp_c .* [ ...
>     0; ...
>    -sin(Theta_c); ...
>     sin(Theta_c)];
> 
> simplify(Hc_t - Hc_expected)
> ```

---

## Exercise 10.2  
### Vector-Phasors from Time-Domain Fields

> **Problem**  
> Find the **vector-phasors** $\tilde{\mathbf{E}}(\mathbf{r})$ or $\tilde{\mathbf{H}}(\mathbf{r})$ corresponding to the given **time-domain vector fields**.  
> Use the convention:
> $$
 \mathbf{F}(\mathbf{r},t) = \Re\{\tilde{\mathbf{F}}(\mathbf{r})e^{j\omega t}\}.
 $$
>
> (a)  
> $$
 \mathbf{E}(\mathbf{r},t)
 = E_0 \hat{\mathbf{x}} \cos\!\left(\omega t - \frac{3x + 2y - z}{\text{m}}\right)\ \text{V/m}
 $$
>
> (b)  
> $$
 \mathbf{H}(\mathbf{r},t)
 =
 \begin{pmatrix}
 3\cos\!\left(\omega t + \frac{x+y}{\text{m}}\right) + 5\sin\!\left(\omega t + \frac{x+y}{\text{m}}\right)\\[4pt]
 \cos\!\left(\omega t + \frac{x+y}{\text{m}}\right) - 2\sin\!\left(\omega t + \frac{x+y}{\text{m}}\right)\\[4pt]
 -4\cos\!\left(\omega t + \frac{x+y}{\text{m}}\right) + \sin\!\left(\omega t + \frac{x+y}{\text{m}}\right)
 \end{pmatrix}
 \ \text{A/m}
 $$
>
> (c)  
> $$
 \mathbf{E}(\mathbf{r},t) =
 -6\hat{\mathbf{x}}\cos\!\left(\omega t + \frac{-x + 2y + 5z}{\text{m}} - \frac{\pi}{3}\right)
 + 2\hat{\mathbf{y}}\sin\!\left(\omega t + \frac{-x+2y+5z}{\text{m}} + 0.2 \right)
 $$
> $$
 \qquad\qquad
 + \hat{\mathbf{z}}\Big[
 3\cos\!\left(\omega t + \frac{-x+2y+5z}{\text{m}} - 0.35\right)
 - 2\sin\!\left(\omega t + \frac{-x+2y+5z}{\text{m}} - 0.35\right)
 \Big]\ \text{V/m}
 $$

---

### Theory recap

We need the inverse relation:

- Starting point:
  $$
  \mathbf{F}(\mathbf{r},t) = \Re\{\tilde{\mathbf{F}}(\mathbf{r}) e^{j\omega t}\}.
  $$
- For **single cosine term**:
  $$
  F(\mathbf{r},t) = A\cos(\omega t + \phi(\mathbf{r}))
  \quad\Rightarrow\quad
  \tilde{F}(\mathbf{r}) = A e^{j\phi(\mathbf{r})}.
  $$
- For linear combinations like
  $$
  a\cos\Phi + b\sin\Phi,
  $$
  we can use
  $$
  \Re\{(a - jb)e^{j\Phi}\} = a\cos\Phi + b\sin\Phi.
  $$

So in general:

- If
  $$
  F(\mathbf{r},t) = a\cos\Phi(\mathbf{r},t) + b\sin\Phi(\mathbf{r},t),
  $$
  with $\Phi(\mathbf{r},t) = \omega t + \phi(\mathbf{r})$, then
  $$
  \tilde{F}(\mathbf{r}) = (a - jb)e^{j\phi(\mathbf{r})}.
  $$

---

### Geometry / setup

- Cartesian coordinates $(x,y,z)$, same as Exercise 10.1.
- The spatial phase functions are:
  - (a) $\phi_a(\mathbf{r}) = -\dfrac{3x+2y-z}{\text{m}}$  
  - (b) $\phi_b(\mathbf{r}) = \dfrac{x+y}{\text{m}}$  
  - (c) $\phi_c(\mathbf{r}) = \dfrac{-x+2y+5z}{\text{m}}$.
- The medium is not explicitly used (we are not enforcing any plane-wave relations here yet), only signal representation.

---

### Derivation

#### (a) Single cosine term → simple phasor

We have
$$
\mathbf{E}(\mathbf{r},t)
= E_0 \hat{\mathbf{x}} \cos\!\left(\omega t - \frac{3x+2y-z}{\text{m}}\right).
$$

Compare with
$$
E_x(\mathbf{r},t) = A\cos(\omega t + \phi(\mathbf{r})).
$$

Here:
- $A = E_0$,
- $\phi(\mathbf{r}) = -\dfrac{3x+2y-z}{\text{m}}$.

So the $x$-component phasor is
$$
\tilde{E}_x(\mathbf{r}) = E_0 e^{j\phi(\mathbf{r})}
= E_0 e^{-j(3x+2y-z)/\text{m}}.
$$

No $y$ or $z$ components.

Thus
$$
\boxed{
\tilde{\mathbf{E}}(\mathbf{r})
= E_0 e^{-j(3x+2y-z)/\text{m}}\hat{\mathbf{x}}\ \text{V/m}
}
$$

Matches the official solution exactly.

---

#### (b) Combination of cosine and sine in all components

Given
$$
\mathbf{H}(\mathbf{r},t) =
\begin{pmatrix}
3\cos\Phi + 5\sin\Phi\\[2pt]
\cos\Phi - 2\sin\Phi\\[2pt]
-4\cos\Phi + \sin\Phi
\end{pmatrix}
\ \text{A/m},
\quad
\Phi = \omega t + \frac{x+y}{\text{m}}.
$$

We use
$$
a\cos\Phi + b\sin\Phi = \Re\{(a - jb)e^{j\Phi}\}.
$$

So:

- $x$-component:
  $$
  H_x = 3\cos\Phi + 5\sin\Phi
  = \Re\{(3 - j5)e^{j\Phi}\}
  \Rightarrow \tilde{H}_x(\mathbf{r}) = (3 - j5)e^{j(x+y)/\text{m}}.
  $$

- $y$-component:
  $$
  H_y = \cos\Phi - 2\sin\Phi
  = \Re\{(1 + j2)e^{j\Phi}\}
  \Rightarrow \tilde{H}_y(\mathbf{r}) = (1 + j2)e^{j(x+y)/\text{m}}.
  $$

- $z$-component:
  $$
  H_z = -4\cos\Phi + \sin\Phi
  = \Re\{(-4 - j)e^{j\Phi}\}
  \Rightarrow \tilde{H}_z(\mathbf{r}) = (-4 - j)e^{j(x+y)/\text{m}}.
  $$

Collecting:
$$
\boxed{
\tilde{\mathbf{H}}(\mathbf{r})
=
\begin{pmatrix}
3 - j5\\[2pt]
1 + j2\\[2pt]
-4 - j
\end{pmatrix}
e^{j(x+y)/\text{m}}\ \text{A/m}
}
$$

Matches the official solution (same coefficients and phase).

---

#### (c) Three mixed components with phase offsets

Write
$$
\Phi_c(\mathbf{r},t) = \omega t + \frac{-x+2y+5z}{\text{m}}.
$$

Then the three components are:

- $x$-component:
  $$
  E_x(\mathbf{r},t)
  = -6\cos\left(\Phi_c - \frac{\pi}{3}\right).
  $$
  Compare with $A\cos(\omega t + \phi)$; here $A=-6$ and total phase is $\Phi_c - \dfrac{\pi}{3}$, so
  $$
  \phi_x(\mathbf{r}) = \frac{-x+2y+5z}{\text{m}} - \frac{\pi}{3}.
  $$
  Thus
  $$
  \tilde{E}_x(\mathbf{r})
  = -6 e^{j\phi_x(\mathbf{r})}
  = -6 e^{j\left(\frac{-x+2y+5z}{\text{m}} - \frac{\pi}{3}\right)}.
  $$

- $y$-component:
  $$
  E_y(\mathbf{r},t)
  = 2\sin\left(\Phi_c + 0.2\right).
  $$
  Use $\sin\Phi = \Re\{-j e^{j\Phi}\}$, so
  $$
  2\sin(\Phi_c + 0.2)
  = \Re\{-j 2 e^{j(\Phi_c + 0.2)}\},
  $$
  hence
  $$
  \tilde{E}_y(\mathbf{r})
  = -j 2 e^{j\left(\frac{-x+2y+5z}{\text{m}} + 0.2\right)}.
  $$

- $z$-component:
  $$
  E_z(\mathbf{r},t)
  = 3\cos\left(\Phi_c - 0.35\right)
    - 2\sin\left(\Phi_c - 0.35\right).
  $$
  Rewrite the second term:
  $$
  -2\sin(\Phi_c - 0.35)
  = \Re\{-2\sin(\Phi_c - 0.35)\}
  = \Re\{-2(-j)e^{j(\Phi_c - 0.35)}\}
  = \Re\{(2j)e^{j(\Phi_c - 0.35)}\}.
  $$
  So
  $$
  E_z(\mathbf{r},t)
  = \Re\{3 e^{j(\Phi_c - 0.35)}\}
    + \Re\{2j e^{j(\Phi_c - 0.35)}\}
  = \Re\{(3 + j2)e^{j(\Phi_c - 0.35)}\}.
  $$
  Therefore
  $$
  \tilde{E}_z(\mathbf{r})
  = (3 + j2) e^{j\left(\frac{-x+2y+5z}{\text{m}} - 0.35\right)}.
  $$

Collect in vector form:
$$
\boxed{
\tilde{\mathbf{E}}(\mathbf{r})
=
\begin{pmatrix}
-6 e^{j\left(\frac{-x+2y+5z}{\text{m}} - \frac{\pi}{3}\right)}\\[4pt]
- j 2 e^{j\left(\frac{-x+2y+5z}{\text{m}} + 0.2\right)}\\[4pt]
(3 + j2) e^{j\left(\frac{-x+2y+5z}{\text{m}} - 0.35\right)}
\end{pmatrix}
\ \text{V/m}
}
$$

The official solution further factors out a common $e^{-j(x-2y-5z)/\text{m}}$; this is **algebraically equivalent** (just grouping exponents). So:

- Our expression is fully consistent with the official one.
- Differences are only in how spatial phase constants are grouped.

---

### Notes (Exercise 10.2)

- Main idea: **identify $\cos$ / $\sin$ combinations** and match to the form
  $$
  a\cos\Phi + b\sin\Phi = \Re\{(a - jb)e^{j\Phi}\}.
  $$
- For pure cosine: $\tilde{F} = A e^{j\phi(\mathbf{r})}$.
- For pure sine: $\tilde{F} = -j A e^{j\phi(\mathbf{r})}$.
- Phase shifts inside the arguments (like $\Phi \pm 0.35$) become **constant phase factors** in the phasor exponent.
- Common pitfalls:
  - Forgetting that $\sin$ uses a $-j$ factor.
  - Trying to pull $\omega t$ into the phasor: $\omega t$ always stays in $e^{j\omega t}$, not inside $\tilde{\mathbf{F}}(\mathbf{r})$.
- Status:
  - (a) and (b): **exact match** with the official solution.
  - (c): **equivalent** to the official solution after algebraic rearrangement (same amplitudes, phases, and structure).

---

### MATLAB — Exercise 10.2 (verification)

> [!code]- MATLAB — Exercise 10.2 (verification)
> ```matlab  
> % 10.2 — Vector phasors from time-domain fields
> % Verify that F(r,t) = real(F_tilde(r) * exp(1j*omega*t))
> 
> syms x y z t omega real
> 
> %% Helper: recover time-domain field from a candidate phasor
> timeField = @(Ftilde) real( Ftilde .* exp(1j*omega*t) );
> 
> %% (a) E(r,t) = E0 xhat * cos(omega*t - (3x+2y-z))
> E0 = sym('E0','real');
> phase_a = -(3*x + 2*y - z);      % [1/m], "per meter" implicit
> 
> % Candidate phasor:
> Etilde_a = [E0*exp(1j*phase_a); 0; 0];
> 
> % Reconstructed time-domain field:
> Ea_t_rec = timeField(Etilde_a);
> 
> % Original definition:
> Phi_a = omega*t + phase_a;
> Ea_t_orig = [E0*cos(Phi_a); 0; 0];
> 
> simplify(Ea_t_rec - Ea_t_orig)
> 
> %% (b) H(r,t) = [3 cos + 5 sin; cos - 2 sin; -4 cos + sin]
> phase_b = x + y;                  % [1/m]
> Phi_b   = omega*t + phase_b;
> 
> Hb_t_orig = [ ...
>     3*cos(Phi_b) + 5*sin(Phi_b); ...
>     cos(Phi_b)   - 2*sin(Phi_b); ...
>    -4*cos(Phi_b) +   sin(Phi_b)];
> 
> % Candidate phasor using (a - j b) rule:
> H0_b = [3 - 1j*5; 1 + 1j*2; -4 - 1j];
> Htilde_b = H0_b .* exp(1j*phase_b);
> 
> Hb_t_rec = timeField(Htilde_b);
> 
> simplify(Hb_t_rec - Hb_t_orig)
> 
> %% (c) E(r,t) with mixed cos/sin and phase shifts
> phase_c = -x + 2*y + 5*z;        % [1/m]
> Phi_c   = omega*t + phase_c;
> 
> Ex_t_orig = -6*cos(Phi_c - pi/3);
> Ey_t_orig =  2*sin(Phi_c + 0.2);
> Ez_t_orig =  3*cos(Phi_c - 0.35) - 2*sin(Phi_c - 0.35);
> 
> % Our candidate phasor components:
> Ex_tilde = -6 * exp(1j*(phase_c - pi/3));
> Ey_tilde = -1j*2 * exp(1j*(phase_c + 0.2));
> Ez_tilde = (3 + 1j*2) * exp(1j*(phase_c - 0.35));
> 
> Etilde_c = [Ex_tilde; Ey_tilde; Ez_tilde];
> 
> Ec_t_rec = timeField(Etilde_c);
> Ec_t_orig = [Ex_t_orig; Ey_t_orig; Ez_t_orig];
> 
> simplify(Ec_t_rec - Ec_t_orig)
> ```

---
