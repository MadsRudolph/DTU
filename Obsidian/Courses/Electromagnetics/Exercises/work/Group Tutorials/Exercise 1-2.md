# Exercises 1–2 — Engineering Electromagnetics (Solutions)

---

# Exercise 1.1 — Simplifying Complex Numbers

> **Question (from PDF)**  
> Simplify the following expressions and write them in the form $z = a + jb$:  
> a) $z = \dfrac{4}{j}$  
> b) $z = \dfrac{1-j}{1+j}$  
> c) $z = \dfrac{4+5j}{6-5j}$  

---

• **Theory recap**  
- Complex numbers: $z = a + jb$, where $a,b \in \mathbb{R}$ and $j^2 = -1$.  
- Basic identities:  
  - $\dfrac{1}{j} = -j$  
  - To simplify a complex fraction, multiply numerator and denominator by the **complex conjugate** of the denominator:
    $$
    \frac{a+jb}{c+jd} = \frac{(a+jb)(c-jd)}{(c+jd)(c-jd)} = \frac{(a+jb)(c-jd)}{c^2 + d^2}.
    $$

---

• **Given**  
- (a) $z = \dfrac{4}{j}$  
- (b) $z = \dfrac{1-j}{1+j}$  
- (c) $z = \dfrac{4+5j}{6-5j}$  

---

• **Geometry / setup**  
- Pure algebra; no geometric position is needed.  
- You can interpret each $z$ as a vector in the complex plane $(\Re\{z\}, \Im\{z\})$ after simplification.

---

• **Derivation**

**(a) $z = \dfrac{4}{j}$**

Use $1/j = -j$:
$$
z = \frac{4}{j} = 4\cdot\frac{1}{j} = 4(-j) = -4j.
$$
So $a=0$, $b=-4$.

---

**(b) $z = \dfrac{1-j}{1+j}$**

Multiply numerator and denominator by the conjugate $(1-j)$:
$$
z = \frac{1-j}{1+j} \cdot \frac{1-j}{1-j}
  = \frac{(1-j)^2}{(1+j)(1-j)}.
$$

Compute:
$$
(1-j)^2 = 1 - 2j + j^2 = 1 - 2j -1 = -2j,
$$
$$
(1+j)(1-j) = 1 - j^2 = 1 - (-1) = 2.
$$

So
$$
z = \frac{-2j}{2} = -j.
$$
Hence $a=0$, $b=-1$.

---

**(c) $z = \dfrac{4+5j}{6-5j}$**

Multiply numerator and denominator by the conjugate $(6+5j)$:
$$
z = \frac{4+5j}{6-5j}\cdot\frac{6+5j}{6+5j}
  = \frac{(4+5j)(6+5j)}{(6-5j)(6+5j)}.
$$

Numerator:
$$
(4+5j)(6+5j) = 4\cdot 6 + 4\cdot 5j + 5j\cdot 6 + 5j\cdot 5j
= 24 + 20j + 30j + 25j^2
= 24 + 50j - 25
= -1 + 50j.
$$

Denominator:
$$
(6-5j)(6+5j) = 6^2 + 5^2 = 36 + 25 = 61.
$$

So
$$
z = \frac{-1+50j}{61} = -\frac{1}{61} + j\frac{50}{61}.
$$

---

• **Final boxed results**

$$
\boxed{\text{(a)}\ z = -4j}
$$

$$
\boxed{\text{(b)}\ z = -j}
$$

$$
\boxed{\text{(c)}\ z = -\dfrac{1}{61} + j\dfrac{50}{61}}
$$

---

• **Notes**  
- These manipulations appear repeatedly in electromagnetics when dealing with impedances and propagation constants.  
- Being fast and accurate with complex arithmetic is essential for transmission line and plane wave problems.

---

• **MATLAB / Maple verification (optional)**

    zA = 4/1j;
    zB = (1-1j)/(1+1j);
    zC = (4+5j)/(6-5j);
    vpa([zA, zB, zC], 6)

---

## Formula Sheet — Exam Extraction (1.1)

- Complex number: $z = a+jb$, $j^2 = -1$.  
- Inversion of $j$: $\dfrac{1}{j} = -j$.  
- Rationalization:
  $$
  \frac{a+jb}{c+jd}
  = \frac{(a+jb)(c-jd)}{c^2 + d^2}.
  $$
- Standard pattern: if $z = \dfrac{\alpha}{j}$ then $z = -j\,\alpha$.

**Exam variants:**  
- Simplifying sums/products of complex numbers.  
- Rationalizing denominators in impedances $1/(R + jX)$.

---

### Exam Relevance (1.1)

- **Level:** 🟥 essential  
- **What is being tested:**  
  - Confident manipulation of complex numbers in algebraic form.  
- **Common traps:**  
  - Forgetting $j^2=-1$.  
  - Sign errors when multiplying by conjugates.  
- **What to memorize:**  
  - $\dfrac{1}{j} = -j$.  
  - Mechanic of “multiply by the conjugate” for denominators.

---

# Exercise 1.2 — Complex Numbers in the Cartesian Plane

> **Question (from PDF)**  
> Represent the complex numbers in a Cartesian coordinate system:  
> a) (i) $z_1 = 5 + 2j$, (ii) $z_2 = 1 + 3j$, (iii) $z_3 = 2 - 3j$, (iv) $z_4 = -4 - 7j$  
> b) (i) $z_1 + z_2$, (ii) $z_1 - z_2$ → interpret these operations geometrically/graphically.

---

• **Theory recap**  
- Each complex number $z = a + jb$ is a point/vector $(a,b)$ in the complex plane.  
- Addition/subtraction of complex numbers corresponds to vector addition/subtraction in $\mathbb{R}^2$.  
- Geometric meaning:  
  - $z_1 + z_2$ is the diagonally opposite corner of the parallelogram formed by vectors $z_1$ and $z_2$.  
  - $z_1 - z_2$ is the vector pointing from tip of $z_2$ to tip of $z_1$.

---

• **Given**  
- $z_1 = 5 + 2j$  
- $z_2 = 1 + 3j$  
- $z_3 = 2 - 3j$  
- $z_4 = -4 - 7j$

---

• **Geometry / setup**  
- Plot them in the $(\Re\{z\}, \Im\{z\})$ plane:  
  - $z_1 = (5,2)$  
  - $z_2 = (1,3)$  
  - $z_3 = (2,-3)$  
  - $z_4 = (-4,-7)$  
- A typical figure shows these as arrows from origin to each point, plus vectors for $z_1+z_2$ and $z_1-z_2$.

---

• **Derivation**

Compute the requested combinations:

1. Sum:
   $$
   z_1 + z_2 = (5+2j) + (1+3j)
   = (5+1) + (2+3)j
   = 6 + 5j.
   $$

2. Difference:
   $$
   z_1 - z_2 = (5+2j) - (1+3j)
   = (5-1) + (2-3)j
   = 4 - j.
   $$

Geometric interpretation:

- $z_1+z_2$ is the vector obtained by placing $z_2$’s tail at $z_1$’s head (triangle rule).  
- $z_1-z_2$ is the vector from the tip of $z_2$ to the tip of $z_1$.

---

• **Final boxed results**

$$
\boxed{z_1 + z_2 = 6 + 5j}
$$

$$
\boxed{z_1 - z_2 = 4 - j}
$$

---

• **Notes**  
- This vector view is exactly how phasor diagrams work in AC circuit analysis and EM phasor fields.  
- Being able to interpret sums/differences visually will help with interference and superposition problems.

---

• **MATLAB / Maple verification (optional)**

    z1 = 5 + 2j;
    z2 = 1 + 3j;
    z1_plus_z2  = z1 + z2;
    z1_minus_z2 = z1 - z2;

---

## Formula Sheet — Exam Extraction (1.2)

- Complex point:
  $$
  z = a + jb \leftrightarrow (a,b) \in \mathbb{R}^2.
  $$
- Operations:
  $$
  z_1 + z_2 \leftrightarrow (a_1+a_2,\, b_1+b_2),
  $$
  $$
  z_1 - z_2 \leftrightarrow (a_1-a_2,\, b_1-b_2).
  $$

**Geometry template:**  
- Draw axes: $\Re$ horizontal, $\Im$ vertical, then place arrows from origin to each $(a,b)$.

**Exam variants:**  
- Graphical representation of phasor sums.  
- Distance between points: $|z_1 - z_2|$.

---

### Exam Relevance (1.2)

- **Level:** 🟧 important  
- **What is being tested:**  
  - Understanding complex numbers as vectors in 2D.  
  - Geometric meaning of addition and subtraction.  
- **Common traps:**  
  - Mixing up signs when subtracting.  
  - Forgetting that $z_1 - z_2$ is “from $z_2$ to $z_1$”.  
- **What to memorize:**  
  - Only the interpretation: $z_1+z_2$ → parallelogram diagonal.

---

# Exercise 1.3 — Cartesian and Polar Representation

> **Question (from PDF)**  
> **a)** Express the complex numbers in polar coordinates $r e^{j\varphi}$ and represent them graphically:  
> (i) $z = 7 + j2$  
> (ii) $z = 3 - j$  
> (iii) $z = \dfrac{1}{7 + j2}$  
>
> **b)** Convert the complex numbers into Cartesian format $z = a + jb$:  
> (i) $z = 3\angle 45^\circ$  
> (ii) $z = 5\angle 180^\circ$  
> (iii) $z = 6 e^{j4.2}$  

---

• **Theory recap**  
- Cartesian form: $z = a + jb$.  
- Polar/exponential form:
  $$
  z = r e^{j\varphi} = r(\cos\varphi + j\sin\varphi),
  $$
  where
  $$
  r = |z| = \sqrt{a^2 + b^2},\quad \varphi = \arg(z).
  $$
- Conversion back:
  $$
  a = r\cos\varphi,\quad b = r\sin\varphi.
  $$

---

• **Given**  
- (a)(i) $z = 7 + 2j$  
- (a)(ii) $z = 3 - j$  
- (a)(iii) $z = \dfrac{1}{7 + 2j}$  
- (b)(i) $z = 3\angle 45^\circ$  
- (b)(ii) $z = 5\angle 180^\circ$  
- (b)(iii) $z = 6 e^{j4.2}$  

---

• **Geometry / setup**  
- All points lie in the complex plane at $(a,b)$ and can be represented as vectors with angle $\varphi$ measured from the positive real axis.  
- Quadrants:  
  - $7+2j$: first quadrant.  
  - $3-j$: fourth quadrant.  

---

• **Derivation**

### Part (a): Cartesian → polar

**(i) $z = 7 + 2j$**

Magnitude:
$$
r = \sqrt{7^2 + 2^2} = \sqrt{49 + 4} = \sqrt{53}.
$$

Angle:
$$
\varphi = \arctan\left(\frac{2}{7}\right) \approx 15.95^\circ.
$$

So
$$
\boxed{z = \sqrt{53}\,e^{j\arctan(2/7)} = \sqrt{53}\angle 15.95^\circ}.
$$

---

**(ii) $z = 3 - j$**

Magnitude:
$$
r = \sqrt{3^2 + (-1)^2} = \sqrt{9+1} = \sqrt{10}.
$$

Angle: fourth quadrant (negative imaginary part):
$$
\varphi = \arctan\left(\frac{-1}{3}\right) \approx -18.43^\circ.
$$

So
$$
\boxed{z = \sqrt{10}\,e^{-j\arctan(1/3)} = \sqrt{10}\angle -18.43^\circ}.
$$

---

**(iii) $z = \dfrac{1}{7+2j}$**

First write $7+2j$ in polar:
$$
7+2j = \sqrt{53}\,e^{j\varphi},\quad \varphi = \arctan(2/7).
$$

The reciprocal:
$$
z = \frac{1}{\sqrt{53}e^{j\varphi}} = \frac{1}{\sqrt{53}}e^{-j\varphi}.
$$

Thus
$$
\boxed{
z = \sqrt{\frac{1}{53}}\,e^{-j\arctan(2/7)} = \sqrt{\frac{1}{53}}\angle -15.95^\circ.
}
$$

---

### Part (b): Polar → Cartesian

**(i) $z = 3\angle 45^\circ$**

Using Euler:
$$
z = 3e^{j\pi/4} = 3(\cos\frac{\pi}{4} + j\sin\frac{\pi}{4})
= 3\frac{\sqrt{2}}{2} + j3\frac{\sqrt{2}}{2}.
$$

So
$$
\boxed{z = \frac{3\sqrt{2}}{2} + j\frac{3\sqrt{2}}{2}}.
$$

---

**(ii) $z = 5\angle 180^\circ$**

$$
z = 5e^{j\pi} = 5(\cos\pi + j\sin\pi) = 5(-1 + 0j) = -5.
$$

So
$$
\boxed{z = -5}.
$$

---

**(iii) $z = 6e^{j4.2}$**

Use $z = r(\cos\varphi + j\sin\varphi)$:
$$
z = 6(\cos 4.2 + j\sin 4.2).
$$

Numerically:
$$
\cos 4.2 \approx -0.49,\quad \sin 4.2 \approx -0.872,
$$
$$
z \approx -2.94 - j5.23.
$$

So
$$
\boxed{z \approx -2.94 - j5.23}.
$$

---

• **Final boxed results**

Cartesian → polar:
$$
\boxed{7+2j = \sqrt{53}\angle 15.95^\circ}
$$

$$
\boxed{3-j = \sqrt{10}\angle -18.43^\circ}
$$

$$
\boxed{\dfrac{1}{7+2j} = \sqrt{\dfrac{1}{53}}\angle -15.95^\circ}
$$

Polar → Cartesian:
$$
\boxed{3\angle 45^\circ = \dfrac{3\sqrt{2}}{2} + j\dfrac{3\sqrt{2}}{2}}
$$

$$
\boxed{5\angle 180^\circ = -5}
$$

$$
\boxed{6e^{j4.2} \approx -2.94 - j5.23}
$$

---

• **Notes**  
- Inverting in polar simply inverts the magnitude and negates the angle: $1/(re^{j\varphi}) = (1/r)e^{-j\varphi}$.  
- This is extremely useful for converting $Z$, $\gamma$ etc. between magnitude/phase and rectangular forms.

---

• **MATLAB / Maple verification (optional)**

    z1 = 7 + 2j;
    r1 = abs(z1); phi1 = angle(z1); % radians

    z2 = 3 - 1j;
    r2 = abs(z2); phi2 = angle(z2);

    z3 = 1/(7 + 2j);
    r3 = abs(z3); phi3 = angle(z3);

    z4 = 3*exp(1j*pi/4);
    z5 = 5*exp(1j*pi);
    z6 = 6*exp(1j*4.2);

---

## Formula Sheet — Exam Extraction (1.3)

- Conversion formulas:
  $$
  r = |z| = \sqrt{a^2 + b^2},\quad \varphi = \arg(z) = \operatorname{atan2}(b,a).
  $$
  $$
  a = r\cos\varphi,\quad b = r\sin\varphi.
  $$
- Reciprocal:
  $$
  \frac{1}{re^{j\varphi}} = \frac{1}{r}e^{-j\varphi}.
  $$

**Geometry template:**  
- Draw $z$ as a vector of length $r$ at angle $\varphi$ from the real axis.

**Exam variants:**  
- Convert impedances, reflection coefficients, phasors between forms.  
- Problems where you must compare angles, e.g. phase shifts.

---

### Exam Relevance (1.3)

- **Level:** 🟥 essential  
- **What is being tested:**  
  - Fluent conversion between Cartesian and polar complex forms.  
- **Common traps:**  
  - Wrong quadrant for $\varphi$.  
  - Forgetting sign change of $\varphi$ when inverting.  
- **What to memorize:**  
  - The formulas above; plus the geometric meaning of $r$ and $\varphi$.

---

# Exercise 1.4 — Input Impedance of Simple AC Circuits

> **Question (from PDF)**  
> Calculate the input impedance $Z_\text{in}$ of the following circuits:  
>
> a) Series $R$–$L$  
> b) Parallel $R$–$C$  
> c) Series $R$–$C$  
> d) Parallel $L$–$C$  
> e) Series $R$–$L$–$C$  

(Diagrams: simple combinations of $R$, $L$, $C$ as described.)

---

• **Theory recap**  
- Impedances:
  $$
  Z_R = R,\quad Z_L = j\omega L,\quad Z_C = \frac{1}{j\omega C}.
  $$
- Series combination:
  $$
  Z_\text{series} = \sum Z_i.
  $$
- Parallel combination:
  $$
  Y = \frac{1}{Z} = \sum_i \frac{1}{Z_i}.
  $$
- Often define a characteristic frequency $\omega_0$ to get dimensionless ratios $\omega/\omega_0$.

---

• **Given**  
- Generic $R$, $L$, $C$.  
- Angular frequency $\omega$.  
- Circuits (a)–(e) combining these in simple series/parallel forms.

---

• **Geometry / setup**  
- 1D series/parallel networks with a single input port.  
- No spatial coordinates; the “geometry” is purely circuit topology.

---

• **Derivation**

### (a) Series $R$–$L$

Circuit:
- Resistor $R$ in series with inductor $L$.

Impedance:
$$
Z_\text{in} = R + j\omega L.
$$

Factor $R$ and define $\omega_0 = R/L$:
$$
Z_\text{in} = R\left(1 + j\frac{\omega L}{R}\right)
            = R\left(1 + j\frac{\omega}{\omega_0}\right),
\quad \omega_0 := \frac{R}{L}.
$$

---

### (b) Parallel $R$–$C$

Circuit:
- Resistor $R$ in parallel with capacitor $C$.

Admittance:
$$
Y = \frac{1}{R} + j\omega C = \frac{1 + j\omega RC}{R}.
$$

Thus:
$$
Z_\text{in} = \frac{1}{Y} = \frac{R}{1 + j\omega RC}.
$$

Define $\omega_0 = 1/(RC)$:
$$
Z_\text{in} = \frac{R}{1 + j\frac{\omega}{\omega_0}}.
$$

---

### (c) Series $R$–$C$

Circuit:
- Resistor $R$ in series with capacitor $C$.

Impedance:
$$
Z_\text{in} = R + \frac{1}{j\omega C}.
$$

Write:
$$
\frac{1}{j\omega C} = \frac{1}{j}\cdot\frac{1}{\omega C} = -\frac{j}{\omega C}.
$$

Then:
$$
Z_\text{in} = R - \frac{j}{\omega C}.
$$

Follow the algebra:
$$
Z_\text{in} = \frac{1 + j\omega RC}{j\omega C}
           = R\frac{1 + j\omega RC}{j\omega RC}.
$$

Define $x = \omega/\omega_0$ with $\omega_0 = 1/(RC)$:
$$
Z_\text{in} = R\frac{1 + jx}{jx}.
$$

---

### (d) Parallel $L$–$C$

Circuit:
- Inductor $L$ in parallel with capacitor $C$.

Admittance:
$$
Y = j\omega C + \frac{1}{j\omega L}
  = j\omega C - \frac{j}{\omega L}
  = j\left(\omega C - \frac{1}{\omega L}\right).
$$

Combine terms:
$$
\omega C - \frac{1}{\omega L}
= \frac{\omega^2 LC - 1}{\omega L}.
$$

So
$$
Y = j\frac{\omega^2 LC - 1}{\omega L}.
$$

Define $\omega_0^2 = 1/(LC)$, so $\omega^2LC - 1 = \omega^2/\omega_0^2 - 1$.

Then:
$$
Z_\text{in} = \frac{1}{Y}
= \frac{1}{j}\frac{\omega L}{\omega^2LC - 1}
= j\frac{\omega L}{1 - \omega^2LC}
= j\frac{\omega L}{1 - (\omega/\omega_0)^2}.
$$

Define $x = \omega/\omega_0$:
$$
Z_\text{in} = j\sqrt{\frac{L}{C}}\frac{x}{1 - x^2}.
$$

---

### (e) Series $R$–$L$–$C$

Circuit:
- Resistor $R$, inductor $L$, capacitor $C$ all in series.

Impedance:
$$
Z_\text{in} = R + j\omega L + \frac{1}{j\omega C}
            = R + j\left(\omega L - \frac{1}{\omega C}\right).
$$

Define $\omega_0^2 = 1/(LC)$ and $x = \omega/\omega_0$:
$$
\omega L - \frac{1}{\omega C}
= \sqrt{\frac{L}{C}}\left(x - \frac{1}{x}\right).
$$

Thus:
$$
Z_\text{in} = R + j\sqrt{\frac{L}{C}}\left(x - \frac{1}{x}\right).
$$

---

• **Final boxed results**

(a)
$$
\boxed{
Z_\text{in} = R\left(1 + j\frac{\omega}{\omega_0}\right),\quad \omega_0 = \frac{R}{L}
}
$$

(b)
$$
\boxed{
Z_\text{in} = \frac{R}{1 + j\frac{\omega}{\omega_0}},\quad \omega_0 = \frac{1}{RC}
}
$$

(c)
$$
\boxed{
Z_\text{in} = R\frac{1 + j\frac{\omega}{\omega_0}}{j\frac{\omega}{\omega_0}},\quad \omega_0 = \frac{1}{RC}
}
$$

(d)
$$
\boxed{
Z_\text{in} = j\sqrt{\frac{L}{C}}\frac{x}{1 - x^2},\quad x = \frac{\omega}{\omega_0},\ \omega_0^2 = \frac{1}{LC}
}
$$

(e)
$$
\boxed{
Z_\text{in} = R + j\sqrt{\frac{L}{C}}\left(x - \frac{1}{x}\right),\quad x = \frac{\omega}{\omega_0},\ \omega_0^2 = \frac{1}{LC}
}
$$

---

• **Notes**  
- (d) and (e) are resonant structures (parallel and series resonance respectively).  
- At resonance ($\omega = \omega_0$):  
  - Series $R$–$L$–$C$ has purely real impedance ($Z = R$).  
  - Parallel $L$–$C$ can exhibit very large impedance.

---

• **MATLAB / Maple verification (optional)**

    syms R L C w real
    Z_R = R;
    Z_L = 1j*w*L;
    Z_C = 1/(1j*w*C);

    Z_series_RL  = Z_R + Z_L;
    Z_par_RC     = 1 / (1/Z_R + 1/Z_C);
    Z_series_RC  = Z_R + Z_C;
    Z_par_LC     = 1 / (1/Z_L + 1/Z_C);
    Z_series_RLC = Z_R + Z_L + Z_C;

    simplify(Z_series_RL)
    simplify(Z_par_RC)
    simplify(Z_series_RC)
    simplify(Z_par_LC)
    simplify(Z_series_RLC)

---

## Formula Sheet — Exam Extraction (1.4)

- Impedances:
  $$
  Z_R = R,\quad Z_L = j\omega L,\quad Z_C = \frac{1}{j\omega C}.
  $$
- Series combination: $Z_\text{series} = \sum Z_i$.  
- Parallel combination: $Y = 1/Z = \sum_i 1/Z_i$.

**Resonant frequencies:**
- LC resonance: $\omega_0 = 1/\sqrt{LC}$.  
- RL and RC corner frequencies:
  - $\omega_0 = R/L$ for series $R$–$L$.  
  - $\omega_0 = 1/(RC)$ for $R$–$C$ configs.

**Exam variants:**
- Find $Z_\text{in}(\omega)$ and sketch Bode plots.  
- Determine resonance, bandwidth, or quality factor from these forms.

---

### Exam Relevance (1.4)

- **Level:** 🟥 essential  
- **What is being tested:**  
  - Impedance calculus with complex numbers.  
  - Recognizing resonant and low-/high-pass behavior from circuit structures.  
- **Common traps:**  
  - Wrong sign for $j$ in $Z_C$.  
  - Messing up parallel combination algebra.  
  - Forgetting to define $\omega_0$ consistently.  
- **What to memorize:**  
  - $Z_R, Z_L, Z_C$.  
  - Corner/resonant frequency relations: $R/L$, $1/(RC)$, and $1/\sqrt{LC}$.

---

# Exercise 2.1 — Travelling Wave in a Lossless Medium

> **Question (from PDF)**  
> The general form of a wave travelling along the $z$-direction in a lossless medium is  
> $$
> w(z,t) = A\cos(2\pi f t + \beta z),
> $$
> where $A$ is the amplitude, $f$ the frequency, and $\beta$ the wavenumber ($f>0$).  
>
> (a) Investigate if the wave travels in space. Assuming $\beta>0$, does it travel towards $+z$ or $-z$?  
> (b) What must be changed so that the wave travels in the opposite direction?  
> (c) Investigate how the frequency affects the wave shape (e.g., $A=1$, $z=0$, compare $f=1, 2, 0.5$ Hz). Determine periods $T$.  
> (d) Investigate how the wavenumber affects the wave shape (e.g., $t=0$, compare $\beta=\pi, 0.5\pi, 2\pi$ 1/m). Determine wavelengths $\lambda$.  
> (e–i) Interpret the given plots and determine the phase velocity $u_p$ and how $f$ and $\beta$ affect it.

---

• **Theory recap**  
- General travelling wave:
  $$
  w(z,t) = A\cos(\omega t + \beta z + \phi_0),
  $$
  where $\omega = 2\pi f$.  
- Constant-phase condition (phase point):
  $$
  \omega t + \beta z = \Phi_0 = \text{const}.
  $$
- Solving for $z(t)$:
  $$
  z(t) = \frac{\Phi_0 - \omega t}{\beta}.
  $$
  Its slope tells you the **direction** and **speed** of propagation.  
- Wavelength:
  $$
  \lambda = \frac{2\pi}{|\beta|}.
  $$
- Period:
  $$
  T = \frac{1}{f}.
  $$
- Phase velocity:
  $$
  u_p = \frac{\lambda}{T} = \frac{\omega}{\beta} = \frac{2\pi f}{\beta}.
  $$

---

• **Given**  
- Wave: $w(z,t) = A\cos(2\pi f t + \beta z)$, lossless, $\beta > 0$ unless stated otherwise.

---

• **Geometry / setup**  
- 1D propagation along $z$-axis.  
- Time snapshots: $w(z,t_i)$ vs. $z$.  
- Spatial snapshots: $w(z_0,t)$ vs. $t$.

---

• **Derivation**

### (a) Direction of propagation for $\beta>0$

Set constant phase:
$$
\Phi_0 = 2\pi f t + \beta z.
$$

Solve for $z(t)$:
$$
z(t) = \frac{\Phi_0}{\beta} - \frac{2\pi f}{\beta}t.
$$

Since $\beta>0$ and $f>0$:  
- $\dfrac{dz}{dt} = -\dfrac{2\pi f}{\beta} < 0$.  
- So, as $t$ increases, $z$ **decreases**: the wave travels towards **negative $z$**.

---

### (b) Making it travel in the opposite direction

To reverse direction, flip the sign associated with $z$ in the phase:

- Use $w(z,t) = A\cos(2\pi f t - \beta z)$ with $\beta>0$, or  
- Equivalently keep the same form but take $\beta<0$.

Either way, the wave then travels towards **positive $z$**.

---

### (c) Influence of $f$ on time-domain wave shape

Take $A=1$, $z=0$:
$$
w(0,t) = \cos(2\pi f t).
$$

Compare $f=1$ Hz, $2$ Hz, $0.5$ Hz over $0 \le t \le 4$ s.

Periods:
$$
T = \frac{1}{f}:
\quad T_{1\text{Hz}} = 1\text{ s},\quad T_{2\text{Hz}} = 0.5\text{ s},\quad T_{0.5\text{Hz}} = 2\text{ s}.
$$

Higher $f$ → shorter period → more oscillations per second.

---

### (d) Influence of $\beta$ on spatial wave shape

Set $t=0$:
$$
w(z,0) = A\cos(\beta z).
$$

Compare $\beta = \pi, 0.5\pi, 2\pi$ 1/m for $0\le z\le 4$ m.

Wavelengths:
$$
\lambda = \frac{2\pi}{\beta}:
\quad \beta=\pi \Rightarrow \lambda = 2\text{ m},
\quad \beta=0.5\pi \Rightarrow \lambda = 4\text{ m},
\quad \beta=2\pi \Rightarrow \lambda = 1\text{ m}.
$$

Smaller $\beta$ → longer wavelength (fewer spatial oscillations).

---

### (e–h) Phase velocity comparisons

General relation:
$$
u_p = \frac{\omega}{\beta} = \frac{2\pi f}{\beta}.
$$

Examples:

- Case 1: $(f_1=1\ \text{Hz},\ \beta_1=2\pi\ \text{1/m})$  
  $$
  u_{p1} = \frac{2\pi\cdot 1}{2\pi} = 1\ \text{m/s}.
  $$

- Case 2: $(f_2=2\ \text{Hz},\ \beta_2=4\pi\ \text{1/m})$  
  $$
  u_{p2} = \frac{2\pi\cdot 2}{4\pi} = 1\ \text{m/s}.
  $$

So both waves move at the **same phase velocity**.

Changing only $\beta$ with fixed $f$:

- $(f=1\ \text{Hz},\ \beta_1=2\pi,\ \beta_2=4\pi)$:
  $$
  u_{p1} = 1\ \text{m/s},\quad u_{p2} = \frac{2\pi}{4\pi} = 0.5\ \text{m/s}.
  $$

So bigger $\beta$ (same $f$) means **slower** phase velocity.

Changing only $f$ with fixed $\beta$:

- $(f_1=1\ \text{Hz},\ f_2=2\ \text{Hz},\ \beta = 2\pi)$:
  $$
  u_{p1} = 1\ \text{m/s},\quad u_{p2} = 2\ \text{m/s}.
  $$

Higher $f$ (same $\beta$) means **faster** phase velocity.

---

• **Final boxed results**

Direction:
$$
\boxed{\beta>0\ \Rightarrow\ \text{wave with }w(z,t)=A\cos(2\pi f t + \beta z)\text{ travels towards } -z.}
$$

Period and wavelength:
$$
\boxed{T = \frac{1}{f}},\quad
\boxed{\lambda = \frac{2\pi}{|\beta|}}.
$$

Phase velocity:
$$
\boxed{u_p = \frac{2\pi f}{\beta} = \frac{\lambda}{T}}
$$
(sign determined by propagation direction).

---

• **Notes**  
- The sign convention in the phase argument decides propagation direction.  
- The same phase velocity can arise from different $(f,\beta)$ pairs if $2\pi f/\beta$ is constant.

---

• **MATLAB / Maple verification (optional)**

    A  = 1;
    f1 = 1;  f2 = 2;
    b1 = 2*pi; b2 = 4*pi;

    up1 = 2*pi*f1/b1;
    up2 = 2*pi*f2/b2;   % both = 1 m/s

    % Example mesh for plotting (optional)
    t  = 0:0.01:1;
    z  = linspace(0,2,500);
    [Z,T] = meshgrid(z,t);
    w1 = A*cos(2*pi*f1*T + b1*Z);
    w2 = A*cos(2*pi*f2*T + b2*Z);

---

## Formula Sheet — Exam Extraction (2.1)

- Wave in 1D:
  $$
  w(z,t) = A\cos(\omega t \pm \beta z + \phi_0),
  $$
  where $\omega = 2\pi f$.  
- Constant phase:
  $$
  \omega t \pm \beta z = \Phi_0 \Rightarrow z(t) = \text{linear in } t.
  $$
- Wavelength and period:
  $$
  \lambda = \frac{2\pi}{|\beta|},\quad T = \frac{1}{f}.
  $$
- Phase velocity:
  $$
  u_p = \frac{\omega}{\beta} = \frac{2\pi f}{\beta} = \frac{\lambda}{T}.
  $$

**Exam variants:**  
- Identify $u_p$ from the wave equation.  
- Decide direction of propagation from sign pattern.  
- Sketch snapshots at several times or positions.

---

### Exam Relevance (2.1)

- **Level:** 🟥 essential  
- **What is being tested:**  
  - Understanding travelling waves, phase, direction, and velocity.  
- **Common traps:**  
  - Confusing sign conventions: $+\beta z$ vs $-\beta z$.  
  - Mixing $f$ vs $\omega$.  
- **What to memorize:**  
  - $u_p = \omega/\beta$, $\lambda=2\pi/\beta$, $T=1/f$.

---

# Exercise 2.2 — Attenuated Travelling Wave

> **Question (from PDF)**  
> The general form of a wave travelling along the $z$-direction in a lossy medium is  
> $$
> w(z,t) = Ae^{-\alpha z}\cos(2\pi f t - \beta z),
> $$
> where $Ae^{-\alpha z}$ is the amplitude function and $\alpha$ is the attenuation constant.  
> Assuming $A=5$, $\alpha = 0.2\ \text{m}^{-1}$, $f = 0.5\ \text{kHz}$, and phase velocity $u_p = 2\ \text{km/s}$, determine  
> (a) the angular frequency $\omega$  
> (b) the phase constant $\beta$  
> (c) the wavelength $\lambda$  
> (d) sketch the wave for $t = 0,\ 0.25,\ 0.5,\ 0.75\ \text{ms}$.

---

• **Theory recap**  
- Lossy travelling wave:
  $$
  w(z,t) = A_0 e^{-\alpha z}\cos(\omega t - \beta z)
  $$
- $\alpha$ [Np/m] is attenuation constant.  
- Phase velocity:
  $$
  u_p = \frac{\omega}{\beta} = \frac{2\pi f}{\beta}.
  $$

---

• **Given**  
- $A = 5$  
- $\alpha = 0.2\ \text{m}^{-1}$  
- $f = 0.5\ \text{kHz} = 500\ \text{Hz}$  
- $u_p = 2\ \text{km/s} = 2000\ \text{m/s}$  

---

• **Geometry / setup**  
- 1D wave along $z$ with exponentially decaying amplitude as $z$ increases.  
- The sketch shows $w(z,t)$ vs. $z$ for several time instants, with decreasing envelope.

---

• **Derivation**

**(a) Angular frequency $\omega$**

$$
\omega = 2\pi f = 2\pi \cdot 500 = 1000\pi\ \text{rad/s}.
$$

---

**(b) Phase constant $\beta$**

Use $u_p = \omega/\beta$:
$$
\beta = \frac{\omega}{u_p} = \frac{2\pi f}{u_p}
= \frac{2\pi \cdot 500}{2000}
= \frac{\pi}{2}\ \text{rad/m}.
$$

---

**(c) Wavelength $\lambda$**

$$
\lambda = \frac{2\pi}{\beta} = \frac{2\pi}{\pi/2} = 4\ \text{m}.
$$

---

**(d) Sketch**

- At each fixed time $t_i$, the wave vs. $z$ is a cosine with spatial frequency $\beta$ and amplitude envelope $5e^{-\alpha z}$.  
- Across $z$, crests and troughs have spacing $\lambda = 4$ m.  
- As $t$ increases, the pattern shifts along $z$ (direction determined by sign in $\omega t - \beta z$) while the envelope $e^{-\alpha z}$ remains the same.

---

• **Final boxed results**

$$
\boxed{\omega = 1000\pi\ \text{rad/s}}
$$

$$
\boxed{\beta = \dfrac{\pi}{2}\ \text{rad/m}}
$$

$$
\boxed{\lambda = 4\ \text{m}}
$$

Amplitude envelope: $5e^{-0.2z}$.

---

• **Notes**  
- $\alpha$ controls exponential decay; larger $\alpha$ → faster amplitude drop.  
- $u_p$ still relates $f$ and $\beta$ as in the lossless case.

---

• **MATLAB / Maple verification (optional)**

    A     = 5;
    alpha = 0.2;
    f     = 0.5e3;
    up    = 2e3;

    w  = 2*pi*f;
    beta = w/up;
    lambda = 2*pi/beta;

---

## Formula Sheet — Exam Extraction (2.2)

- Lossy wave:
  $$
  w(z,t) = A_0 e^{-\alpha z}\cos(\omega t - \beta z).
  $$
- Attenuation constant:
  $$
  A(z) = A_0 e^{-\alpha z}.
  $$
- Phase velocity:
  $$
  u_p = \frac{\omega}{\beta}.
  $$
- Wavelength:
  $$
  \lambda = \frac{2\pi}{\beta}.
  $$

**Exam variants:**  
- Given $A(z_1)$ and $A(z_2)$, find $\alpha$.  
- Find $\lambda$, $\beta$, $\omega$, $u_p$ when some are given.

---

### Exam Relevance (2.2)

- **Level:** 🟥 essential  
- **What is being tested:**  
  - Connection between $f,\ \omega,\ \beta,\ \lambda,\ u_p$ in lossy medium.  
  - Understanding of exponential attenuation.  
- **Common traps:**  
  - Confusing units (Hz vs rad/s, m vs km).  
  - Forgetting that $u_p = \omega/\beta$ still holds even with losses.  
- **What to memorize:**  
  - $\omega=2\pi f$, $\lambda=2\pi/\beta$, $u_p=\omega/\beta$.

---

# Exercise 2.3 — Determining Attenuation Constant from Measurements

> **Question (from PDF)**  
> An electromagnetic wave travelling in seawater has amplitude $A(z_1) = 98.02\ \text{V/m}$ at depth $z_1 = 10\ \text{m}$, and amplitude $A(z_2) = 81.87\ \text{V/m}$ at depth $z_2 = 100\ \text{m}$.  
> Assuming the amplitude function $A(z) = A_0 e^{-\alpha z}$, determine the attenuation constant $\alpha$ of seawater.

---

• **Theory recap**  
- Amplitude in a lossy medium:
  $$
  A(z) = A_0 e^{-\alpha z}.
  $$
- Taking ratios at two positions eliminates $A_0$:
  $$
  \frac{A(z_1)}{A(z_2)} = \frac{A_0 e^{-\alpha z_1}}{A_0 e^{-\alpha z_2}} = e^{\alpha(z_2 - z_1)}.
  $$

---

• **Given**  
- $A(z_1) = 98.02\ \text{V/m}$ at $z_1 = 10\ \text{m}$  
- $A(z_2) = 81.87\ \text{V/m}$ at $z_2 = 100\ \text{m}$  

---

• **Geometry / setup**  
- 1D propagation along depth $z$ (increasing depth).  
- Amplitude decreases with depth due to attenuation.

---

• **Derivation**

From the ratio:
$$
\frac{A(z_1)}{A(z_2)} = e^{\alpha(z_2 - z_1)}.
$$

Take natural log:
$$
\alpha(z_2 - z_1) = \ln\left(\frac{A(z_1)}{A(z_2)}\right),
$$
$$
\alpha = \frac{\ln\left(\dfrac{A(z_1)}{A(z_2)}\right)}{z_2 - z_1}.
$$

Plug in numbers:
$$
\alpha = \frac{\ln(98.02/81.87)}{100 - 10}
      = \frac{\ln(1.1975\ldots)}{90}.
$$

Numerically:
- $\alpha \approx 2\ \text{Np/km}$  
- In dB/km: $\alpha \approx 17.4\ \text{dB/km}$ (using $8.686\ \text{dB/Np}$).

---

• **Final boxed results**

In Np/m:
$$
\boxed{\alpha \approx 2\ \frac{1}{\text{km}} = 2\times 10^{-3}\ \text{m}^{-1}}
$$

In dB/km:
$$
\boxed{\alpha \approx 17.4\ \text{dB/km}}
$$

---

• **Notes**  
- Using ratios cancels the unknown initial amplitude $A_0$.  
- Converting Np to dB: $1\ \text{Np} \approx 8.686\ \text{dB}$.

---

• **MATLAB / Maple verification (optional)**

    A1 = 98.02;
    A2 = 81.87;
    z1 = 10;
    z2 = 100;

    alpha_Np_per_m  = log(A1/A2)/(z2 - z1);
    alpha_Np_per_km = alpha_Np_per_m * 1e3;
    alpha_dB_per_km = alpha_Np_per_km * 8.686;

---

## Formula Sheet — Exam Extraction (2.3)

- Amplitude ratio:
  $$
  \frac{A(z_1)}{A(z_2)} = e^{\alpha(z_2 - z_1)}.
  $$
- Attenuation constant:
  $$
  \alpha = \frac{\ln\left(A(z_1)/A(z_2)\right)}{z_2 - z_1}.
  $$
- Conversion:
  $$
  \alpha_{\text{dB}} = 8.686\,\alpha_{\text{Np}}.
  $$

**Exam variants:**  
- Given two amplitudes at different positions, solve for $\alpha$.  
- Given $\alpha$, compute amplitude at some depth.

---

### Exam Relevance (2.3)

- **Level:** 🟥 essential  
- **What is being tested:**  
  - Application of exponential decay and logarithms to physical attenuation.  
- **Common traps:**  
  - Switching $z_1$ and $z_2$ (sign error in exponent).  
  - Mixing Np and dB without conversion.  
- **What to memorize:**  
  - Ratio-based formula and $\alpha_{\text{dB}} \approx 8.686\alpha_{\text{Np}}$.

---

# Exercise 2.4 — Phase Delay and Phase Velocity from TL Measurements

> **Question (from PDF)**  
> A wave with frequency $f = 50\ \text{MHz}$ is propagating down a transmission line of length $\ell = 1\ \text{m}$. A phase delay of $\varphi_d = \pi/2$ is measured between input and output of the TL. Determine:  
> (a) the time delay $t_d$ (hint: relate phase delay to time delay and frequency)  
> (b) the phase velocity $u_p$.

---

• **Theory recap**  
- Phase delay $\varphi_d$ at given frequency $f$ corresponds to time delay $t_d$ via:
  $$
  \varphi_d = 2\pi f t_d.
  $$
- Phase velocity:
  $$
  u_p = \frac{\ell}{t_d}.
  $$

---

• **Given**  
- $f = 50\ \text{MHz} = 50 \times 10^6\ \text{Hz}$  
- $\ell = 1\ \text{m}$  
- Measured phase delay: $\varphi_d = \pi/2$  

---

• **Geometry / setup**  
- 1D propagation along TL of length $\ell$.  
- Output field is a phase-shifted version of input: same magnitude, delayed in time.

---

• **Derivation**

**(a) Time delay $t_d$**

Use:
$$
\varphi_d = 2\pi f t_d \Rightarrow t_d = \frac{\varphi_d}{2\pi f}.
$$

Insert numbers:
$$
t_d = \frac{\pi/2}{2\pi\cdot 50\cdot 10^6}
    = \frac{1}{4\cdot 50\cdot 10^6}
    = \frac{1}{200\cdot 10^6}
    = 5 \times 10^{-9}\ \text{s}
    = 5\ \text{ns}.
$$

---

**(b) Phase velocity $u_p$**

$$
u_p = \frac{\ell}{t_d}
    = \frac{1\ \text{m}}{5\times 10^{-9}\ \text{s}}
    = 2\times 10^{8}\ \text{m/s}.
$$

Compare with speed of light $c_0 \approx 3\times 10^{8}\ \text{m/s}$:
$$
u_p \approx \frac{2}{3}c_0.
$$

---

• **Final boxed results**

$$
\boxed{t_d = 5\ \text{ns}}
$$

$$
\boxed{u_p = 2\times 10^{8}\ \text{m/s} \approx \dfrac{2}{3}c_0}
$$

---

• **Notes**  
- This is a standard way to extract effective phase velocity (and thus effective dielectric constant) of a transmission line.  
- If $u_p < c_0$, the line is filled with a medium of $\varepsilon_r > 1$.

---

• **MATLAB / Maple verification (optional)**

    f  = 50e6;
    phi_d = pi/2;
    L  = 1;

    td = phi_d / (2*pi*f);
    up = L / td;

---

## Formula Sheet — Exam Extraction (2.4)

- Phase delay vs time delay:
  $$
  \varphi_d = 2\pi f t_d\quad \Rightarrow\quad t_d = \frac{\varphi_d}{2\pi f}.
  $$
- Phase velocity:
  $$
  u_p = \frac{\ell}{t_d}.
  $$
- Relation to effective permittivity:
  $$
  u_p = \frac{c_0}{\sqrt{\varepsilon_\text{eff}}}
  \quad\Rightarrow\quad
  \varepsilon_\text{eff} = \left(\frac{c_0}{u_p}\right)^2.
  $$

**Exam variants:**  
- Measure $\varphi_d$ and infer $u_p$ and $\varepsilon_\text{eff}$.  
- Change line length and compare $t_d$.

---

### Exam Relevance (2.4)

- **Level:** 🟥 essential  
- **What is being tested:**  
  - Translating measured phase into physical speed on a transmission line.  
- **Common traps:**  
  - Using $f$ instead of $\omega$ incorrectly (here we stay in $2\pi f$ explicitly).  
  - Mixing up radians and degrees (here $\varphi_d$ is in radians).  
- **What to memorize:**  
  - $\varphi_d = 2\pi f t_d$ and $u_p = \ell / t_d$.

---
