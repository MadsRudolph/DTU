> Quick refs: [[Lecture 10 – Transmission Lines Power, Matching & Smith Chart]]

---

## Exercise 7.1  
### Smith Chart basics: $|\Gamma|$, matched load, and one full rotation

> **Given**  
> Smith Chart conceptual questions:
> - (a) What value of $|\Gamma|$ represents the **outer perimeter** of the Smith Chart?  
> - (b) Which point on the Smith Chart represents a **matched load**?  
> - (c) What **line length** corresponds to one complete rotation around the Smith Chart, and why?  
>
> Medium: lossless transmission line, Smith Chart in the **reflection coefficient plane**.

---

### Theory recap  

Core relationships for a lossless line (Ulaby & Ravaioli, Sec. 2–10):

- Reflection coefficient at the load:
  $$
  \Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}
  $$
- Magnitude and phase:
  $$
  \Gamma_L = |\Gamma_L| e^{j\theta_r}
  $$
- Reflection coefficient at a distance $l$ from the load (towards the generator):
  $$
  \Gamma_\text{in}(l) = \Gamma_L e^{-j2\beta l}, \qquad \beta = \frac{2\pi}{\lambda}
  $$
- Smith Chart is the **$\Gamma$-plane**: each point corresponds to a particular $\Gamma$ and hence to a normalized impedance $z = Z/Z_0$.

Key ideas:

- **Outer circle** of the Smith Chart corresponds to $|\Gamma| = 1$ (total reflection).  
- **Center point** corresponds to $\Gamma = 0$ (perfect match $Z_L = Z_0$).  
- Moving along a lossless line corresponds to **rotation** on a circle of constant $|\Gamma|$ in the $\Gamma$-plane. One full rotation (change of phase $2\pi$) corresponds to a line length of $\lambda/2$.

---

### Geometry / setup  

- Work in the **reflection coefficient plane** ($\Gamma$-plane).  
- The Smith Chart is a **unit circle** in this plane:
  - Radius: $|\Gamma| \le 1$.
  - Outer perimeter: $|\Gamma| = 1$.
  - Center: $\Gamma = 0$.

- The transmission line is assumed **lossless**, so $|\Gamma|$ is constant along the line and only the phase of $\Gamma$ changes with $l$.

---

### Derivation  

#### (a) Outer perimeter $|\Gamma|$

For a purely reactive load $Z_L = jX$ on a lossless line, we have:
$$
\Gamma_L = \frac{jX - Z_0}{jX + Z_0}
$$

Because $Z_0$ is real and $Z_L$ is purely imaginary:

- The magnitudes of numerator and denominator are equal:
  $$
  |jX - Z_0| = |jX + Z_0|
  $$
- Hence:
  $$
  |\Gamma_L| = 1
  $$

Therefore, the **outer perimeter** of the Smith Chart corresponds to $|\Gamma| = 1$, i.e. all **lossless, purely reactive** loads.

---

#### (b) Matched load point  

A matched load satisfies:
$$
Z_L = Z_0 \quad \Rightarrow \quad \Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0} = 0
$$

So:

- The matched load corresponds to $\Gamma = 0$.  
- On the Smith Chart, this is the **center point**.

---

#### (c) Line length for one full rotation  

For a lossless line:
$$
\Gamma_\text{in}(l) = \Gamma_L e^{-j2\beta l} = |\Gamma_L| e^{j(\theta_r - 2\beta l)}
$$

A **full rotation** in the $\Gamma$-plane corresponds to a phase change of $2\pi$:
$$
2\beta l = 2\pi
$$

Using $\beta = 2\pi/\lambda$:
$$
2 \cdot \frac{2\pi}{\lambda} \cdot l = 2\pi
\quad\Rightarrow\quad
\frac{4\pi}{\lambda} l = 2\pi
\quad\Rightarrow\quad
l = \frac{\lambda}{2}
$$

Thus, moving **$\lambda/2$ along a lossless line** (towards the generator or toward the load) corresponds to one complete rotation around the Smith Chart.

---

### Final boxed results  

- (a)  
  $$
  \boxed{ \text{Outer perimeter: }|\Gamma| = 1 }
  $$

- (b)  
  $$
  \boxed{ \text{Matched load: center of the Smith Chart, where }\Gamma = 0 }
  $$

- (c)  
  $$
  \boxed{ \text{One full rotation in the Smith Chart corresponds to }l = \frac{\lambda}{2} \text{ on a lossless line} }
  $$

---

### Notes  

- This exercise is directly aligned with Ulaby Concept Questions 2-19 and 2-21 (8th Ed.).  
- Very typical exam question: checking if you understand the **geometry of the Smith Chart** and the **relationship between $l$ and the phase of $\Gamma$**.  
- Official solution comparison:
  - Our answers for (a), (b), and (c) **match the official solution** (same statements and reasoning).

---

### MATLAB — Exercise 7.1 (verification)  

> [!code]- MATLAB — Exercise 7.1 (verification) 
> ```matlab 
>% Smith Chart rotation vs. line length: verify lambda/2 periodicity
>clear; clc;
>
>% Parameters
>lambda = 1;              % wavelength [normalized units]
>Z0     = 50;             % reference impedance [Ohm]
>ZL     = 100 + 1j*50;    % arbitrary complex load [Ohm]
>
>% Reflection coefficient at the load
>GammaL = (ZL - Z0) / (ZL + Z0);
>
>% Sweep line length l from 0 to lambda
>l_vec  = linspace(0, lambda, 501);
>beta   = 2*pi/lambda;
>
>Gamma_in = GammaL .* exp(-1j*2*beta.*l_vec);
>
>% Check periodicity: compare Gamma_in at l and l + lambda/2 (wrapped)
>idx_half   = round(numel(l_vec)/2);
>Gamma_half = Gamma_in(idx_half+1:end);
>Gamma_ref  = Gamma_in(1:end-idx_half);
>
>err = max(abs(Gamma_half - Gamma_ref));
>
>fprintf('Max |Gamma(l+lambda/2) - Gamma(l)| = %.3e\n', err);
>
>% This script numerically confirms that a shift by lambda/2 in l
>% corresponds to one full rotation (periodicity) in Gamma_in.
>```
---

## Exercise 7.2  
### From reflection coefficient $\Gamma$ to normalized load impedance $z_L$

> **Given**  
> Use the Smith Chart to find the **normalized load impedance** $z_L = Z_L/Z_0$ corresponding to the following reflection coefficients:
> - (a) $\Gamma = 0.5$  
> - (b) $\Gamma = 0.5\angle 60^\circ$  
> - (c) $\Gamma = -1$  
> - (d) $\Gamma = 0.3\angle -30^\circ$  
> - (e) $\Gamma = 0$  
> - (f) $\Gamma = -j$  
>
> Medium: lossless transmission line, characteristic impedance $Z_0$ (value not needed because everything is normalized).

---

### Theory recap  

For a load impedance $Z_L$ on a line with characteristic impedance $Z_0$:

- Reflection coefficient at the load:
  $$
  \Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}
  $$
- Define normalized impedance:
  $$
  z_L = \frac{Z_L}{Z_0}
  $$

Rewriting the relation between $z_L$ and $\Gamma_L$ (Ulaby, Sec. 2–10):

- From $\Gamma_L$ to $z_L$:
  $$
  z_L = \frac{1 + \Gamma_L}{1 - \Gamma_L}
  $$
- From $z_L$ to $\Gamma_L$ (inverse relation, used in Exercise 7.3):
  $$
  \Gamma_L = \frac{z_L - 1}{z_L + 1}
  $$

On the Smith Chart:

- Each point corresponds to a **unique pair** $(z_L,\Gamma_L)$ connected by these formulas.
- This exercise is the Smith Chart version of Ulaby Problem 2.47.

---

### Geometry / setup  

- Work in the $\Gamma$-plane with a **unit circle** (Smith Chart).  
- For each $\Gamma$ given in **polar form**, convert to Cartesian form:
  $$
  \Gamma = |\Gamma|(\cos\theta + j\sin\theta)
  $$
- Then compute:
  $$
  z_L = \frac{1 + \Gamma}{1 - \Gamma} = r + jx
  $$
  where $r$ is the normalized resistance and $x$ the normalized reactance.

---

### Derivation  

We use the algebraic relation $z_L = (1+\Gamma)/(1-\Gamma)$ (which is exactly what you’d get if you used a Smith Chart carefully).

#### (a) $\Gamma = 0.5$  

Real and positive:

$$
z_L = \frac{1 + 0.5}{1 - 0.5} = \frac{1.5}{0.5} = 3 + j0
$$

---

#### (b) $\Gamma = 0.5\angle 60^\circ$  

Write $\Gamma$ in rectangular form:
$$
\Gamma = 0.5(\cos 60^\circ + j\sin 60^\circ)
      = 0.5\left(\frac{1}{2} + j\frac{\sqrt{3}}{2}\right)
      = 0.25 + j\cdot 0.433
$$

Then:
$$
z_L = \frac{1 + \Gamma}{1 - \Gamma}
     = \frac{(1 + 0.25) + j0.433}{(1 - 0.25) - j0.433}
     = \frac{1.25 + j0.433}{0.75 - j0.433}
$$

Multiply numerator and denominator by the complex conjugate of the denominator:
$$
z_L = \frac{(1.25 + j0.433)(0.75 + j0.433)}{0.75^2 + 0.433^2}
$$

Carrying out the multiplication and simplification (or using MATLAB / calculator):

- Real part $\approx 1$  
- Imaginary part $\approx 1.15$

So:
$$
z_L \approx 1 + j1.15
$$

---

#### (c) $\Gamma = -1$  

$$
z_L = \frac{1 + (-1)}{1 - (-1)} = \frac{0}{2} = 0 + j0
$$

This corresponds to a **short circuit** ($z_L = 0$).

---

#### (d) $\Gamma = 0.3\angle -30^\circ$  

Rectangular form:
$$
\Gamma = 0.3(\cos(-30^\circ) + j\sin(-30^\circ))
       = 0.3\left(\frac{\sqrt{3}}{2} - j\frac{1}{2}\right)
       \approx 0.26 - j0.15
$$

Then:
$$
z_L = \frac{1 + \Gamma}{1 - \Gamma}
     = \frac{(1 + 0.26) - j0.15}{(1 - 0.26) + j0.15}
     = \frac{1.26 - j0.15}{0.74 + j0.15}
$$

After multiplying by the complex conjugate of the denominator:

- Real part $\approx 1.6$  
- Imaginary part $\approx -0.5$

Thus:
$$
z_L \approx 1.6 - j0.5
$$

---

#### (e) $\Gamma = 0$  

$$
z_L = \frac{1 + 0}{1 - 0} = 1
$$

This is the **matched** normalized impedance: $z_L = 1$.

---

#### (f) $\Gamma = -j$  

Rectangular form: $\Gamma = 0 - j1$.

Then:
$$
z_L = \frac{1 - j}{1 + j}
$$

Multiply numerator and denominator by $(1 - j)$:

$$
z_L = \frac{(1 - j)^2}{1^2 + 1^2}
    = \frac{1 - 2j + j^2}{2}
    = \frac{1 - 2j - 1}{2}
    = \frac{-2j}{2} = -j
$$

So:
$$
z_L = 0 - j1 = -j
$$

---

### Final boxed results  

$$
\boxed{
\begin{aligned}
\text{(a)}\quad & \Gamma = 0.5             &&\Rightarrow\quad z_L = 3 + j0 \\
\text{(b)}\quad & \Gamma = 0.5\angle 60^\circ &&\Rightarrow\quad z_L \approx 1 + j1.15 \\
\text{(c)}\quad & \Gamma = -1              &&\Rightarrow\quad z_L = 0 + j0 \\
\text{(d)}\quad & \Gamma = 0.3\angle -30^\circ &&\Rightarrow\quad z_L \approx 1.6 - j0.5 \\
\text{(e)}\quad & \Gamma = 0               &&\Rightarrow\quad z_L = 1 \\
\text{(f)}\quad & \Gamma = -j              &&\Rightarrow\quad z_L = -j
\end{aligned}
}
$$

(All $z_L$ are **normalized** to $Z_0$.)

---

### Notes  

- This is essentially Ulaby Problem 2.47 (8th Ed.) phrased with “use the Smith Chart.”  
- In an exam, it is common that:
  - You read $\Gamma$ from measurements or a VNA Smith Chart,
  - Then either use the Smith Chart **or** the formula $z_L = (1+\Gamma)/(1-\Gamma)$ to obtain $z_L$.
- Common pitfalls:
  - Forgetting to use **normalized** quantities,
  - Sign errors when converting between rectangular and polar forms,
  - Not recognizing that $\Gamma = 0$ implies $z_L = 1$ (matched).
- Official solution comparison:
  - (a)–(f) **match the official solution** numerically:  
    $z_L = 3 + j0$, $1 + j1.15$, $0 + j0$, $1.6 - j0.5$, $1$, and $-j$.

---

### MATLAB — Exercise 7.2 (verification)  

> [!code]- MATLAB — Exercise 7.2 (verification)
> ```matlab  
>% From Gamma to normalized impedance zL
>clear; clc;
>
>% Define Gamma values (magnitude/angle in degrees)
>Gamma_mag = [0.5, 0.5, 1, 0.3, 0, 1];
>Gamma_ang_deg = [0, 60, 180, -30, 0, -90];  % angles for a)–f)
>Gamma = Gamma_mag .* exp(1j*deg2rad(Gamma_ang_deg));
>
>% Compute normalized impedances zL = (1+Gamma)/(1-Gamma)
>zL = (1 + Gamma) ./ (1 - Gamma);
>
>% Display results
>labels = {'a','b','c','d','e','f'};
>for k = 1:numel(Gamma)
 >   fprintf('(%s) Gamma = %.3f ∠ %.1f° -> zL = %.3f %+.3fj\n', ...
 >       labels{k}, Gamma_mag(k), Gamma_ang_deg(k), real(zL(k)), imag(zL(k)));
>end
>
>% This script confirms the numeric values used in the analytical solution.
>% You can change Gamma_mag and Gamma_ang_deg for other similar exercises.
>```
---

## Exercise 7.3  
### From normalized impedance $z_L$ to reflection coefficient $\Gamma_L$

> **Given**  
> Use the Smith Chart to find the **reflection coefficient** $\Gamma_L$ corresponding to the normalized load impedance
> $z_L = Z_L/Z_0$ for:
> - (a) $z_L = 3$  
> - (b) $z_L = 2 - j2$  
> - (c) $z_L = -j2$  
> - (d) $z_L = 0$  
> - (e) $z_L = +\infty$  
>
> Medium: lossless transmission line, characteristic impedance $Z_0$ (again only normalization matters).

---

### Theory recap  

Reusing the same relations as before, but now in the **inverse direction**:

- Normalized impedance:
  $$
  z_L = \frac{Z_L}{Z_0}
  $$
- Reflection coefficient in terms of $z_L$ (Ulaby, Sec. 2–10, underlying Problem 2.48):
  $$
  \Gamma_L = \frac{z_L - 1}{z_L + 1}
  $$

Special cases:

- $z_L = 1$ (matched): $\Gamma_L = 0$.  
- $z_L = 0$ (short): $\Gamma_L = -1$.  
- $z_L \to \infty$ (open): $\Gamma_L \to +1$.  

These special cases sit at very specific locations on the Smith Chart: center, leftmost, and rightmost points.

---

### Geometry / setup  

- On the Smith Chart, each normalized impedance $z_L$ corresponds to a unique point and thus a unique reflection coefficient $\Gamma_L$.
- The algebraic relation:
  $$
  \Gamma_L = \frac{z_L - 1}{z_L + 1}
  $$
  is the analytic equivalent of “using the Smith Chart” to map $z_L$ to $\Gamma_L$.

We will compute $\Gamma_L$ in **complex form** and, when meaningful, also express it in **polar form** $|\Gamma_L|\angle\theta$.

---

### Derivation  

#### (a) $z_L = 3$  

Real and positive impedance:

$$
\Gamma_L = \frac{3 - 1}{3 + 1} = \frac{2}{4} = 0.5
$$

So:
$$
\Gamma_L = 0.5\angle 0^\circ
$$

---

#### (b) $z_L = 2 - j2$  

Compute:
$$
\Gamma_L = \frac{(2 - j2) - 1}{(2 - j2) + 1} = \frac{1 - j2}{3 - j2}
$$

Multiply numerator and denominator by $(3 + j2)$:
$$
\Gamma_L = \frac{(1 - j2)(3 + j2)}{3^2 + 2^2}
$$

Expand numerator:
$$
(1 - j2)(3 + j2)
= 1\cdot 3 + 1\cdot j2 - j2\cdot 3 - j2\cdot j2
= 3 + j2 - j6 + 2
= (3 + 2) + j(2 - 6)
= 5 - j4
$$

Denominator:
$$
3^2 + 2^2 = 9 + 4 = 13
$$

Thus:
$$
\Gamma_L = \frac{5 - j4}{13} \approx 0.385 - j0.308
$$

Magnitude and phase:
- $|\Gamma_L| \approx \sqrt{0.385^2 + 0.308^2} \approx 0.49$  
- $\angle\Gamma_L \approx \tan^{-1}(-0.308/0.385) \approx -38^\circ$  

(Exact numeric angle not critical; the key is the complex value.)

---

#### (c) $z_L = -j2$  

Compute:
$$
\Gamma_L = \frac{-j2 - 1}{-j2 + 1} = \frac{-1 - j2}{1 - j2}
$$

Multiply numerator and denominator by $(1 + j2)$:
$$
\Gamma_L = \frac{(-1 - j2)(1 + j2)}{1^2 + 2^2}
$$

Expand numerator:
$$
\begin{aligned}
(-1 - j2)(1 + j2) 
&= -1\cdot 1 + (-1)\cdot j2 - j2\cdot 1 - j2\cdot j2 \\
&= -1 - j2 - j2 + 2 \\
&= 1 - j4
\end{aligned}
$$

Denominator:
$$
1^2 + 2^2 = 5
$$

Thus:
$$
\Gamma_L = \frac{1 - j4}{5} = 0.2 - j0.8
$$

Magnitude and phase:
- $|\Gamma_L| = \sqrt{0.2^2 + 0.8^2} = \sqrt{0.04 + 0.64} = \sqrt{0.68} \approx 0.825$  
- $\angle\Gamma_L \approx \tan^{-1}(-0.8/0.2) \approx -76^\circ$

---

#### (d) $z_L = 0$ (short circuit)  

Direct substitution:
$$
\Gamma_L = \frac{0 - 1}{0 + 1} = -1
$$

So:
$$
\Gamma_L = 1\angle 180^\circ
$$

This is the **leftmost point** on the Smith Chart.

---

#### (e) $z_L = +\infty$ (open circuit)  

Take the limit as $z_L \to \infty$:
$$
\Gamma_L = \lim_{z_L \to \infty} \frac{z_L - 1}{z_L + 1}
= \lim_{z_L \to \infty} \frac{1 - 1/z_L}{1 + 1/z_L} = \frac{1 - 0}{1 + 0} = 1
$$

So:
$$
\Gamma_L = 1\angle 0^\circ
$$

This is the **rightmost point** on the Smith Chart.

---

### Final boxed results  

$$
\boxed{
\begin{aligned}
\text{(a)}\quad & z_L = 3            &&\Rightarrow\quad \Gamma_L = 0.5 + j0 = 0.5\angle 0^\circ \\
\text{(b)}\quad & z_L = 2 - j2       &&\Rightarrow\quad \Gamma_L \approx 0.385 - j0.308 \\
\text{(c)}\quad & z_L = -j2          &&\Rightarrow\quad \Gamma_L = 0.2 - j0.8 \\
\text{(d)}\quad & z_L = 0            &&\Rightarrow\quad \Gamma_L = -1 = 1\angle 180^\circ \\
\text{(e)}\quad & z_L = +\infty      &&\Rightarrow\quad \Gamma_L = 1 = 1\angle 0^\circ
\end{aligned}
}
$$

(All $\Gamma_L$ are dimensionless reflection coefficients.)

---

### Notes  

- This is the exact inverse of Exercise 7.2 and corresponds to Ulaby Problem 2.48.  
- Smith Chart view:
  - (a) A point on the real axis to the **right** of the center.  
  - (b) A point in the **lower-right quadrant**.  
  - (c) A point in the **lower-right quadrant** closer to the outer circle.  
  - (d) **Short-circuit** at the far left of the real axis.  
  - (e) **Open-circuit** at the far right of the real axis.
- Exam pattern: very standard for checking that you:
  - Know the relation $\Gamma_L = (z_L - 1)/(z_L + 1)$,
  - Can handle complex algebra for typical TL terminations,
  - Recognize the special cases: short and open.
- Official solution comparison:
  - The given exercise references using the Smith Chart directly; our analytic results are **consistent** with what you would read off the Chart and with the Ulaby reference problems.
  - Any small differences would be due to **rounding** in reading off the Chart.

---

### MATLAB — Exercise 7.3 (verification)  

> [!code]- MATLAB — Exercise 7.3 (verification)
> ```matlab  
>% From normalized impedance zL to reflection coefficient GammaL
>clear; clc;
>
>% Normalized impedances for parts (a)–(e)
>zL = [3 + 0j, 2 - 2j, 0 - 2j, 0 + 0j, inf];
>
>% Compute Gamma using Gamma = (zL - 1)./(zL + 1)
>Gamma = zeros(size(zL));
>
>for k = 1:numel(zL)
 >   if isinf(zL(k))
 >       Gamma(k) = 1; % limit z -> inf
 >   else
 >       Gamma(k) = (zL(k) - 1) / (zL(k) + 1);
 >   end
>end
>
>labels = {'a','b','c','d','e'};
>
>for k = 1:numel(zL)
 >   mag = abs(Gamma(k));
 >   ang = rad2deg(angle(Gamma(k)));
 >   fprintf('(%s) zL = %s -> Gamma = %.3f %+.3fj (|Gamma| = %.3f, angle = %.1f°)\n', ...
 >       labels{k}, num2str(zL(k)), real(Gamma(k)), imag(Gamma(k)), mag, ang);
>end
>
>% This script verifies the reflection coefficients derived analytically.
>% You can reuse it for other normalized impedances by editing zL.
>```