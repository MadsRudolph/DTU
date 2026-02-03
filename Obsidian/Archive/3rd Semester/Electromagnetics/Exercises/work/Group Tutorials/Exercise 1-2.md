> Quick refs: [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]], [[Courses/Electromagnetics/Formulas/Plane Waves & Power — Quick Formula Sheet]] 

---

# Exercise 1.1  
### Complex-number simplification

> **Given**  
> Simplify the following complex numbers and express them in Cartesian form $z = a + jb$:  
> - (a) $z = \dfrac{4}{j}$  
> - (b) $z = \dfrac{1-j}{1+j}$  
> - (c) $z = \dfrac{4+5j}{6-5j}$  

---

### Theory recap  

- Any complex number can be written in Cartesian (rectangular) form  
  $$
  z = a + jb, \quad a = \Re\{z\},\ b = \Im\{z\}.
  $$
- Division of complex numbers is usually handled by multiplying numerator and denominator with the **complex conjugate** of the denominator:
  $$
  \frac{z_1}{z_2} = \frac{z_1 z_2^*}{|z_2|^2}.
  $$

---

### Derivation  

#### (a) $z = \dfrac{4}{j}$  

Recall $j^2 = -1$ and $\frac{1}{j} = -j$:
$$
z = \frac{4}{j} = 4\cdot\frac{1}{j} = 4(-j) = -4j.
$$
So
$$
a = 0,\quad b = -4.
$$

---

#### (b) $z = \dfrac{1-j}{1+j}$  

Multiply by the complex conjugate of the denominator, $(1-j)$:
$$
z = \frac{1-j}{1+j}\cdot\frac{1-j}{1-j}
    = \frac{(1-j)^2}{1^2 - j^2}
    = \frac{1 - 2j + j^2}{1-(-1)}
    = \frac{1 - 2j -1}{2}
    = \frac{-2j}{2} = -j.
$$
Thus
$$
a = 0,\quad b = -1.
$$

---

#### (c) $z = \dfrac{4+5j}{6-5j}$  

Multiply numerator and denominator by the conjugate $(6+5j)$:
$$
z = \frac{4+5j}{6-5j}\cdot\frac{6+5j}{6+5j}
  = \frac{(4+5j)(6+5j)}{6^2 + 5^2}.
$$

Compute numerator:
$$
(4+5j)(6+5j) = 4\cdot 6 + 4\cdot 5j + 5j \cdot 6 + 5j\cdot 5j
= 24 + 20j + 30j + 25j^2
= 24 + 50j - 25
= -1 + 50j.
$$

Denominator:
$$
6^2 + 5^2 = 36 + 25 = 61.
$$

So:
$$
z = \frac{-1 + 50j}{61} = -\frac{1}{61} + j\frac{50}{61}.
$$
Hence
$$
a = -\frac{1}{61},\quad b = \frac{50}{61}.
$$

---

### Final boxed results  

$$
\boxed{z_{\text{(a)}} = -4j}
$$

$$
\boxed{z_{\text{(b)}} = -j}
$$

$$
\boxed{z_{\text{(c)}} = -\dfrac{1}{61} + j\,\dfrac{50}{61}}
$$

---

### Notes  

- This exercise is purely algebraic but foundational for later EM where phasors are used extensively.  
- Common pitfall: forgetting to multiply by the **conjugate** in (b) and (c), or mishandling $j^2 = -1$.  
- Matches official solution (same Cartesian forms).

---

### MATLAB — Exercise 1.1 (verification)  

> [!code]- MATLAB — Exercise 1.1 (verification)
> ```matlab  
>% Define the three complex expressions and verify their simplified forms
>j = 1i;  % MATLAB uses 1i or 1j for sqrt(-1)
>
>z_a = 4/j;
>z_b = (1-j)/(1+j);
>z_c = (4+5*j)/(6-5*j);
>
>% Display numeric values
>disp('Exercise 1.1:');
>fprintf('a) z = 4/j = %g + j%g\n', real(z_a), imag(z_a));
>fprintf('b) z = (1-j)/(1+j) = %g + j%g\n', real(z_b), imag(z_b));
>fprintf('c) z = (4+5j)/(6-5j) = %g + j%g\n', real(z_c), imag(z_c));
>
>% Check against derived exact results
>z_a_expected = -4*j;
>z_b_expected = -j;
>z_c_expected = -1/61 + 1i*50/61;
>
>fprintf('\nCheck differences: a) %g, b) %g, c) %g\n', ...
  >  abs(z_a - z_a_expected), ...
>    abs(z_b - z_b_expected), ...
 >   abs(z_c - z_c_expected));
>```

---

# Exercise 1.2  
### Complex numbers in the Cartesian (Argand) plane

> **Given**  
> Represent the complex numbers  
> - $z_1 = 5 + 2j$  
> - $z_2 = 1 + 3j$  
> - $z_3 = 2 - 3j$  
> - $z_4 = -4 - 7j$  
> in the complex plane.  
> Then compute:  
> - (i) $z_1 + z_2$  
> - (ii) $z_1 - z_2$  
> and interpret these operations geometrically.

---

### Theory recap  

- A complex number $z = a + jb$ can be represented as a point $(a,b)$ in the complex plane:
  - $x$-axis: $\Re\{z\}$ (real part)  
  - $y$-axis: $\Im\{z\}$ (imaginary part)  
- Addition corresponds to **vector addition** (parallelogram rule) in this plane:
  $$
  z_1 + z_2 = (a_1 + a_2) + j(b_1 + b_2).
  $$
- Subtraction corresponds to the difference of vectors, i.e. translation in the plane.

---

### Geometry / setup  

- Place the following points in the $(\Re\{z\}, \Im\{z\})$ plane:
  - $z_1 = (5, 2)$  
  - $z_2 = (1, 3)$  
  - $z_3 = (2, -3)$  
  - $z_4 = (-4, -7)$  

Each complex number is a vector from the origin to the corresponding point.

---

### Derivation  

Compute sums and differences:

1. $z_1 + z_2$:
   $$
   z_1 + z_2 = (5+2j) + (1+3j) = (5+1) + j(2+3) = 6 + 5j.
   $$

2. $z_1 - z_2$:
   $$
   z_1 - z_2 = (5+2j) - (1+3j) = (5-1) + j(2-3) = 4 - j.
   $$

---

### Final boxed results  

$$
\boxed{z_1 + z_2 = 6 + 5j}
$$

$$
\boxed{z_1 - z_2 = 4 - j}
$$

---

### Notes  

- Geometrically, $z_1 + z_2$ is obtained by placing the tail of the vector for $z_2$ at the head of $z_1$; the sum is the diagonal of the parallelogram.  
- $z_1 - z_2$ corresponds to the vector from $z_2$ to $z_1$.  
- Matches official solution (same diagrammatic interpretation and numeric values).

---

### MATLAB — Exercise 1.2 (verification)  

> [!code]- MATLAB — Exercise 1.2 (verification) 
>```matlab 
>% Complex numbers
>j  = 1i;
>z1 = 5 + 2*j;
>z2 = 1 + 3*j;
>z3 = 2 - 3*j;
>z4 = -4 - 7*j;
>
>% Operations
>z1_plus_z2  = z1 + z2;
>z1_minus_z2 = z1 - z2;
>
>fprintf('z1 + z2 = %g + j%g\n', real(z1_plus_z2), imag(z1_plus_z2));
>fprintf('z1 - z2 = %g + j%g\n', real(z1_minus_z2), imag(z1_minus_z2));
>
>% Optional plotting (for geometry intuition)
>figure; hold on; grid on; axis equal;
>plot(real(z1), imag(z1), 'o', 'DisplayName','z1');
>plot(real(z2), imag(z2), 'o', 'DisplayName','z2');
>plot(real(z3), imag(z3), 'o', 'DisplayName','z3');
>plot(real(z4), imag(z4), 'o', 'DisplayName','z4');
>plot(real(z1_plus_z2),  imag(z1_plus_z2),  'x', 'DisplayName','z1+z2');
>plot(real(z1_minus_z2), imag(z1_minus_z2), 'x', 'DisplayName','z1-z2');
>xlabel('Re\{z\}'); ylabel('Im\{z\}');
>legend show;
>title('Complex numbers in the Argand plane');
>```

---

# Exercise 1.3  
### Cartesian and polar representations

> **Given**  
> (a) Convert the following complex numbers from Cartesian to polar form $z = r e^{j\phi} = r\angle\phi$:  
>  (i) $z = 7 + 2j$  
>  (ii) $z = 3 - j$  
>  (iii) $z = \dfrac{1}{7+2j}$  
>
> (b) Convert the following from polar to Cartesian form $z = a + jb$:  
>  (i) $z = 3\angle 45^\circ$  
>  (ii) $z = 5\angle 180^\circ$  
>  (iii) $z = 6 e^{j4.2}$  

---

### Theory recap  

- For $z = a + jb$, the polar form is
  $$
  r = |z| = \sqrt{a^2 + b^2},\quad
  \phi = \arg(z) = \tan^{-1}\left(\frac{b}{a}\right)\quad(\text{with correct quadrant}).
  $$
- The relation between forms:
  $$
  z = r e^{j\phi} = r(\cos\phi + j\sin\phi).
  $$
- For the reciprocal:
  $$
  \frac{1}{z} = \frac{1}{r} e^{-j\phi}.
  $$

---

### Derivation  

#### (a) Cartesian → polar  

(i) $z = 7 + 2j$  
$$
r = \sqrt{7^2 + 2^2} = \sqrt{49 + 4} = \sqrt{53}.
$$
Angle:
$$
\phi = \tan^{-1}\left(\frac{2}{7}\right) \approx 15.95^\circ,
$$
in the first quadrant.

So:
$$
z = \sqrt{53}\, e^{j\phi} = \sqrt{53}\angle 15.95^\circ.
$$

---

(ii) $z = 3 - j$  
$$
r = \sqrt{3^2 + (-1)^2} = \sqrt{9+1} = \sqrt{10}.
$$
Angle:
$$
\phi = \tan^{-1}\left(\frac{-1}{3}\right) \approx -18.43^\circ,
$$
which lies in the fourth quadrant, consistent with $(3,-1)$.

Hence:
$$
z = \sqrt{10}\angle(-18.43^\circ).
$$

---

(iii) $z = \dfrac{1}{7+2j}$  

First write $7+2j$ in polar form from (i):  
$7+2j = \sqrt{53}\angle 15.95^\circ$.

Thus:
$$
z = \frac{1}{7+2j}
  = \frac{1}{\sqrt{53}} \angle (-15.95^\circ)
  = \sqrt{\frac{1}{53}}\angle(-15.95^\circ).
$$

---

#### (b) Polar → Cartesian  

(i) $z = 3\angle 45^\circ$  

Convert to radians: $\phi = \pi/4$. Using Euler’s formula:
$$
z = 3(\cos \tfrac{\pi}{4} + j\sin \tfrac{\pi}{4})
  = 3\left(\frac{\sqrt{2}}{2} + j\frac{\sqrt{2}}{2}\right)
  = \frac{3\sqrt{2}}{2} + j\frac{3\sqrt{2}}{2}.
$$

---

(ii) $z = 5\angle 180^\circ$  

$\phi = \pi$:
$$
z = 5(\cos\pi + j\sin\pi) = 5(-1 + j\cdot 0) = -5.
$$

---

(iii) $z = 6e^{j4.2}$  

Use $\cos, \sin$ directly:
$$
z = 6(\cos 4.2 + j\sin 4.2).
$$
Numerically (as in the official solution),
$$
\cos 4.2 \approx -0.489,\quad \sin 4.2 \approx -0.872,
$$
hence:
$$
z \approx 6(-0.489) + j\,6(-0.872) \approx -2.94 - j5.23.
$$

---

### Final boxed results  

Cartesian → polar:

$$
\boxed{7 + 2j = \sqrt{53}\angle 15.95^\circ}
$$

$$
\boxed{3 - j = \sqrt{10}\angle (-18.43^\circ)}
$$

$$
\boxed{\dfrac{1}{7+2j} = \sqrt{\dfrac{1}{53}}\angle (-15.95^\circ)}
$$

Polar → Cartesian:

$$
\boxed{3\angle 45^\circ = \dfrac{3\sqrt{2}}{2} + j\,\dfrac{3\sqrt{2}}{2}}
$$

$$
\boxed{5\angle 180^\circ = -5}
$$

$$
\boxed{6e^{j4.2} \approx -2.94 - j5.23}
$$

---

### Notes  

- Key exam pattern: converting between forms, especially when dealing with impedances and phasors.  
- Common pitfalls:
  - Using $\tan^{-1}(b/a)$ without fixing the quadrant.  
  - Forgetting to **negate the angle** when taking the reciprocal.  
- Matches official solution (same magnitudes and angles; same approximate Cartesian values).

---

### MATLAB — Exercise 1.3 (verification)  

> [!code]- MATLAB — Exercise 1.3 (verification)
>```matlab  
>j = 1i;
>
>% Part (a)
>z_a1 = 7 + 2*j;
>z_a2 = 3 - 1*j;
>z_a3 = 1/(7 + 2*j);
>
>mag_a1 = abs(z_a1); ang_a1 = angle(z_a1);  % radians
>mag_a2 = abs(z_a2); ang_a2 = angle(z_a2);
>mag_a3 = abs(z_a3); ang_a3 = angle(z_a3);
>
>fprintf('Part (a):\n');
>fprintf('7+2j => r=%g, phi=%g deg\n', mag_a1, ang_a1*180/pi);
>fprintf('3-j  => r=%g, phi=%g deg\n', mag_a2, ang_a2*180/pi);
>fprintf('1/(7+2j) => r=%g, phi=%g deg\n', mag_a3, ang_a3*180/pi);
>
>% Part (b)
>z_b1 = 3*exp(1j*pi/4);
>z_b2 = 5*exp(1j*pi);
>z_b3 = 6*exp(1j*4.2);
>
>fprintf('\nPart (b):\n');
>fprintf('3∠45° => %g + j%g\n', real(z_b1), imag(z_b1));
>fprintf('5∠180° => %g + j%g\n', real(z_b2), imag(z_b2));
>fprintf('6e^{j4.2} => %g + j%g\n', real(z_b3), imag(z_b3));
>```

---

# Exercise 1.4  
### Input impedance of simple RLC networks

> **Given**  
> Determine the input impedance $Z_{\text{in}}$ for each of the five circuits composed of $R$, $L$, and $C$ elements (series/parallel combinations). Express $Z_{\text{in}}$ in a useful normalized form and, where relevant, determine magnitude $|Z_{\text{in}}|$ and phase $\arg(Z_{\text{in}})$.  

(We follow the same circuit labeling (a)–(e) as in the exercise sheet.)

---

### Theory recap  

- For phasor-domain circuit analysis (Ulaby & Ravaioli, complex frequency methods):
  - Inductor: $Z_L = j\omega L$  
  - Capacitor: $Z_C = \dfrac{1}{j\omega C}$  
- Series combination:  
  $$
  Z_{\text{series}} = \sum Z_k.
  $$
- Parallel combination:  
  $$
  Y = \sum Y_k, \quad Z_{\text{parallel}} = \frac{1}{Y}.
  $$
- Often we define a characteristic angular frequency such as $\omega_0 = \dfrac{R}{L}$ or $\omega_0 = \dfrac{1}{RC}$ or $\omega_0 = \dfrac{1}{\sqrt{LC}}$ to normalize expressions.

---

### Derivation  

#### (a) Series $R$ and $L$  

Input impedance:
$$
Z_{\text{in}} = R + j\omega L = R\left(1 + j\frac{\omega L}{R}\right).
$$
Define
$$
\omega_0 = \frac{R}{L} \quad\Rightarrow\quad \frac{\omega L}{R} = \frac{\omega}{\omega_0},
$$
so
$$
Z_{\text{in}} = R\left(1 + j\frac{\omega}{\omega_0}\right).
$$
Magnitude and phase:
$$
|Z_{\text{in}}| = R\sqrt{1 + \left(\frac{\omega}{\omega_0}\right)^2},
\quad
\arg(Z_{\text{in}}) = \tan^{-1}\left(\frac{\omega}{\omega_0}\right).
$$

---

#### (b) Parallel $R$ and $C$  

Admittance:
$$
Y = \frac{1}{Z_{\text{in}}}
  = \frac{1}{R} + j\omega C
  = \frac{1 + j\omega RC}{R}.
$$
Hence
$$
Z_{\text{in}} = \frac{R}{1 + j\omega RC}.
$$
Define $\omega_0 = \dfrac{1}{RC}$:
$$
Z_{\text{in}} = \frac{R}{1 + j\frac{\omega}{\omega_0}}.
$$
Then
$$
|Z_{\text{in}}| = \frac{R}{\sqrt{1 + \left(\frac{\omega}{\omega_0}\right)^2}},
\quad
\arg(Z_{\text{in}}) = -\tan^{-1}\left(\frac{\omega}{\omega_0}\right).
$$

---

#### (c) Series $R$ and $C$  

Impedance:
$$
Z_{\text{in}} = R + \frac{1}{j\omega C}
              = R - j\frac{1}{\omega C}.
$$
Factor $R$:
$$
Z_{\text{in}} = R\left(1 - j\frac{1}{\omega RC}\right).
$$
Let $\omega_0 = \dfrac{1}{RC}$ and define $x = \dfrac{\omega}{\omega_0} = \omega RC$:
$$
Z_{\text{in}} = R\left(1 - j\frac{1}{x}\right).
$$
Magnitude:
$$
|Z_{\text{in}}| = R\sqrt{1 + \left(\frac{1}{x}\right)^2}
                = R\frac{\sqrt{1 + x^2}}{x}.
$$
Phase:
$$
\arg(Z_{\text{in}}) = \tan^{-1}\left(-\frac{1}{x}\right) = -\tan^{-1}\left(\frac{1}{x}\right)
= \tan^{-1}(x) - \frac{\pi}{2},
$$
consistent with expression in the official solution.

---

#### (d) Parallel $L$ and $C$  

Admittance:
$$
Y = j\omega C + \frac{1}{j\omega L}.
$$
Rewrite the second term:
$$
\frac{1}{j\omega L} = -\frac{j}{\omega L}.
$$
Then:
$$
Y = j\omega C - \frac{j}{\omega L}
  = j\left(\omega C - \frac{1}{\omega L}\right)
  = j\left(\frac{\omega^2 LC - 1}{\omega L}\right).
$$
Define $\omega_0^2 = \dfrac{1}{LC}$, so:
$$
\omega^2 LC - 1 = \frac{\omega^2}{\omega_0^2} - 1.
$$
Thus:
$$
Y = \frac{j}{\omega L}\left(\frac{\omega^2}{\omega_0^2} - 1\right)
  = \frac{j}{\omega L}\left(\frac{\omega^2 - \omega_0^2}{\omega_0^2}\right).
$$
Hence:
$$
Z_{\text{in}} = \frac{1}{Y}
= \frac{\omega L}{j}\frac{\omega_0^2}{\omega^2 - \omega_0^2}
= j\frac{\omega L}{\omega_0^2}\frac{1}{1 - \left(\frac{\omega}{\omega_0}\right)^2}.
$$
Using $\omega_0^2 = 1/(LC)$, we get
$$
\frac{\omega L}{\omega_0^2} = \omega L \cdot LC = \omega C^{-1}\cdot LC = \sqrt{\frac{L}{C}},
$$
so finally:
$$
Z_{\text{in}} = j\sqrt{\frac{L}{C}}\;\frac{\dfrac{\omega}{\omega_0}}{1 - \left(\dfrac{\omega}{\omega_0}\right)^2}.
$$
Defining $x = \dfrac{\omega}{\omega_0}$:
$$
Z_{\text{in}} = j\sqrt{\frac{L}{C}}\;\frac{x}{1-x^2}.
$$
Magnitude and phase:
$$
|Z_{\text{in}}| = \sqrt{\frac{L}{C}}\left|\frac{x}{1-x^2}\right|
$$
and $\arg(Z_{\text{in}})$ is $\pm \pi/2$ depending on the sign of $x/(1-x^2)$, exactly as tabulated in the official solution.

---

#### (e) Series $R$, $L$, and $C$  

Impedance:
$$
Z_{\text{in}} = R + j\omega L + \frac{1}{j\omega C}
              = R + j\left(\omega L - \frac{1}{\omega C}\right).
$$
Define $\omega_0 = \dfrac{1}{\sqrt{LC}}$ and $x = \dfrac{\omega}{\omega_0}$. Then
$$
\omega L - \frac{1}{\omega C}
= \sqrt{\frac{L}{C}}\left(x - \frac{1}{x}\right),
$$
so:
$$
Z_{\text{in}} = R + j\sqrt{\frac{L}{C}}\left(x - \frac{1}{x}\right).
$$
Magnitude:
$$
|Z_{\text{in}}| = \sqrt{R^2 + \frac{L}{C}\left(x - \frac{1}{x}\right)^2},
$$
Phase:
$$
\arg(Z_{\text{in}}) = \tan^{-1}\left(
\frac{\sqrt{\dfrac{L}{C}}\left(x - \frac{1}{x}\right)}{R}
\right).
$$

---

### Final boxed results  

(a) Series $RL$:
$$
\boxed{Z_{\text{in}} = R\left(1 + j\frac{\omega}{\omega_0}\right),\quad
\omega_0 = \frac{R}{L}}
$$

(b) Parallel $RC$:
$$
\boxed{Z_{\text{in}} = \frac{R}{1 + j\frac{\omega}{\omega_0}},\quad
\omega_0 = \frac{1}{RC}}
$$

(c) Series $RC$:
$$
\boxed{Z_{\text{in}} = R\left(1 - j\frac{1}{\omega RC}\right)}
$$

(d) Parallel $LC$:
$$
\boxed{Z_{\text{in}} = j\sqrt{\frac{L}{C}}\;\frac{\dfrac{\omega}{\omega_0}}{1 - \left(\dfrac{\omega}{\omega_0}\right)^2},\quad
\omega_0 = \frac{1}{\sqrt{LC}}}
$$

(e) Series $RLC$:
$$
\boxed{Z_{\text{in}} = R + j\sqrt{\frac{L}{C}}\left(x - \frac{1}{x}\right),\quad
x = \frac{\omega}{\omega_0},\ \omega_0 = \frac{1}{\sqrt{LC}}}
$$

---

### Notes  

- Very typical exam-style problem: **normalize** impedances with a characteristic frequency and interpret resonance behavior.  
- In (d), near resonance ($\omega \approx \omega_0$) the denominator $1-x^2$ becomes small, leading to large impedance magnitude.  
- Common pitfalls:
  - Sign mistakes with $1/(j\omega L)$ and $1/(j\omega C)$.  
  - Forgetting that parallel elements require adding **admittances**, not impedances.  
- Matches official solution (same expressions, including normalized forms and phase behavior).

---

### MATLAB — Exercise 1.4 (verification)  

> [!code]- MATLAB — Exercise 1.4 (verification)
>```matlab  
>syms R L C w real;
>
>% (a) Series RL
>Z_RL = R + 1i*w*L;
>
>% (b) Parallel RC
>Y_RC = 1/R + 1i*w*C;
>Z_RC_parallel = 1/Y_RC;
>
>% (c) Series RC
>Z_RC_series = R + 1/(1i*w*C);
>
>% (d) Parallel LC
>Y_LC = 1/(1i*w*L) + 1i*w*C;
>Z_LC_parallel = 1/Y_LC;
>
>% (e) Series RLC
>Z_RLC_series = R + 1i*w*L + 1/(1i*w*C);
>
>disp('Z_RL = ');           disp(simplify(Z_RL));
>disp('Z_RC_parallel = '); disp(simplify(Z_RC_parallel));
>disp('Z_RC_series = ');   disp(simplify(Z_RC_series));
>disp('Z_LC_parallel = '); disp(simplify(Z_LC_parallel));
>disp('Z_RLC_series = ');  disp(simplify(Z_RLC_series));
>```

---

# Exercise 2.1  
### Basic properties of a lossless traveling wave

> **Given**  
> A wave traveling along the $z$-direction in a lossless medium:
> $$
> w(z,t) = A\cos(2\pi f t + \beta z),
> $$
> where $A$ is amplitude, $f>0$ is frequency, and $\beta$ is the (real) phase constant (wavenumber).  
>
> Tasks:  
> (a) Determine whether the wave travels in space. For $\beta>0$, does it travel towards $+z$ or $-z$?  
> (b) Modify the expression so that the wave travels in the opposite direction.  
> (c) Investigate (by plots or reasoning) how $f$ affects wave shape vs time at fixed $z$.  
> (d) Investigate how $\beta$ affects wave shape vs $z$ at fixed $t$.  
> (e) For $A=1$, $f=1\text{ Hz}$, $\beta=2\pi\ \text{m}^{-1}$, find the phase velocity $u_p$.  
> (f)–(h) Compare phase velocities of pairs of waves with different $(f,\beta)$ combinations.

---

### Theory recap  

From Ulaby & Ravaioli, general harmonic traveling wave (along $+z$) is typically written as:
$$
w(z,t) = A\cos(\omega t - \beta z + \phi_0),
$$
where:
- $\omega = 2\pi f$ (rad/s)  
- $\beta$ = phase constant (rad/m)  
- $u_p = \dfrac{\omega}{\beta} = f\lambda$ = phase velocity  
- $\lambda = \dfrac{2\pi}{\beta}$ = wavelength  

A constant-phase point satisfies:
$$
\omega t \pm \beta z = \text{const} \quad\Rightarrow\quad
z(t) = \mp\frac{\omega}{\beta}t + \text{const}.
$$
The sign determines direction of propagation.

---

### Geometry / setup  

We track a point of fixed phase:
$$
\Phi(z,t) = 2\pi f t + \beta z = \Phi_0.
$$
Solving this relation for $z$ as a function of $t$ gives the trajectory of a "wave point" in the $z$–$t$ plane and hence the direction and speed of propagation.

---

### Derivation  

#### (a) Direction of propagation for $w(z,t) = A\cos(2\pi f t + \beta z)$  

Set $\Phi = 2\pi f t + \beta z = \Phi_0$:
$$
\beta z = \Phi_0 - 2\pi f t
\quad\Rightarrow\quad
z(t) = \frac{\Phi_0}{\beta} - \frac{2\pi f}{\beta}t.
$$
For $\beta>0$, the slope $\dfrac{dz}{dt} = -\dfrac{2\pi f}{\beta}<0$, meaning $z$ decreases as $t$ increases: the wave travels towards **negative** $z$ (i.e., along $-z$).

---

#### (b) Opposite direction  

To reverse direction, change the sign of $\beta$ (or equivalently change the sign in front of $\beta z$ inside the cosine). For example:
$$
w(z,t) = A\cos(2\pi f t - \beta z),\quad \beta>0,
$$
will now travel in the **positive** $z$-direction.

---

#### (c) Effect of frequency $f$ on time variation at fixed position  

Fix $z=0$:
$$
w(0,t) = A\cos(2\pi f t).
$$
- Higher $f$ → shorter period $T = 1/f$ → more oscillations per unit time.  
- The waveform’s spatial shape is unchanged; only the temporal oscillation rate changes.

For example, for $f = 0.5, 1, 2\ \text{Hz}$:
$$
T = 2,\ 1,\ 0.5\ \text{s}, \quad \text{respectively}.
$$

---

#### (d) Effect of $\beta$ on spatial variation at fixed time  

Fix $t=0$:
$$
w(z,0) = A\cos(\beta z).
$$
- Larger $\beta$ → shorter wavelength $\lambda = \dfrac{2\pi}{\beta}$.  
- Hence more oscillations per meter.  
- For $\beta = 0.5\pi, \pi, 2\pi\ \text{rad/m}$ the corresponding wavelengths are
  $$
  \lambda = 4,\ 2,\ 1\ \text{m}.
  $$

---

#### (e) Phase velocity for given $f$ and $\beta$  

Given $f=1\ \text{Hz}$, $\beta = 2\pi\ \text{rad/m}$:
$$
\lambda = \frac{2\pi}{\beta} = \frac{2\pi}{2\pi} = 1\ \text{m},
$$
so
$$
u_p = f\lambda = 1\cdot 1 = 1\ \frac{\text{m}}{\text{s}}
= \frac{2\pi f}{\beta}.
$$
The official solution also interprets this graphically by tracking the blue marker.

---

#### (f), (g), (h) Comparing phase velocities  

Phase velocity formula:
$$
u_p = \frac{2\pi f}{\beta}.
$$

- (f) $(f_1,\beta_1) = (1\text{ Hz}, 2\pi\ \text{m}^{-1})$ and $(f_2,\beta_2) = (2\text{ Hz}, 4\pi\ \text{m}^{-1})$:
  $$
  u_{p1} = \frac{2\pi\cdot 1}{2\pi} = 1\ \text{m/s},\quad
  u_{p2} = \frac{2\pi\cdot 2}{4\pi} = 1\ \text{m/s}.
  $$
  Both waves advance with the **same** phase velocity.

- (g) $(f_1,\beta_1) = (1\text{ Hz}, 2\pi),\ (f_2,\beta_2) = (1\text{ Hz}, 4\pi)$:
  $$
  u_{p1} = 1\ \text{m/s},\quad
  u_{p2} = \frac{2\pi\cdot 1}{4\pi} = 0.5\ \text{m/s}.
  $$
  First wave is faster.

- (h) $(f_1,\beta_1) = (2\text{ Hz}, 2\pi),\ (f_2,\beta_2) = (1\text{ Hz}, 2\pi)$:
  $$
  u_{p1} = \frac{2\pi\cdot 2}{2\pi} = 2\ \text{m/s},\quad
  u_{p2} = \frac{2\pi\cdot 1}{2\pi} = 1\ \text{m/s}.
  $$
  First wave is faster.

---

### Final boxed results  

Direction:

$$
\boxed{\text{For } w(z,t)=A\cos(2\pi f t + \beta z),\ \beta>0\Rightarrow \text{wave travels towards } -z.}
$$

$$
\boxed{\text{To reverse direction: } w(z,t)=A\cos(2\pi f t - \beta z).}
$$

Frequency & wavenumber:

$$
\boxed{T = \frac{1}{f},\quad \lambda = \frac{2\pi}{\beta},\quad u_p = \frac{\omega}{\beta} = \frac{2\pi f}{\beta} = f\lambda.}
$$

For the specific case $f=1\ \text{Hz}, \beta=2\pi\ \text{m}^{-1}$:
$$
\boxed{u_p = 1\ \text{m/s}.}
$$

---

### Notes  

- Key pattern: direction of propagation is tied to the **sign** in front of $\beta z$.  
- Typical exam move: track constant phase to identify direction and speed.  
- Matches official solution (same direction arguments, same phase velocities).

---

### MATLAB — Exercise 2.1 (verification)  

> [!code]- MATLAB — Exercise 2.1 (verification)  
>```matlab
>% Parameters for a generic wave
>A = 1;
>f = 1;            % Hz
>beta = 2*pi;      % rad/m
>w = 2*pi*f;       % rad/s
>
>% Phase velocity
>u_p = w/beta;
>
>fprintf('Phase velocity u_p = %g m/s\n', u_p);
>
>% Track a constant phase point phi0 over time
>phi0 = 1;                % arbitrary phase
>t    = linspace(0, 1, 5);
>z    = (phi0 - 2*pi*f.*t)/beta;
>
>disp('z(t) for constant phase:');
>disp(z);
>
>% Optional: plot w(z,t) at different times
>z_grid = linspace(0, 2, 500);
>figure; hold on; grid on;
>for k = 1:numel(t)
>  wzt = A*cos(2*pi*f*t(k) + beta*z_grid);
 >   plot(z_grid, wzt, 'DisplayName', sprintf('t = %.2f s', t(k)));
>end
>xlabel('z [m]'); ylabel('w(z,t)');
>legend show;
>title('Wave profiles at different times (Exercise 2.1)');
>```

---

# Exercise 2.2  
### Traveling wave in a lossy medium

> **Given**  
> A wave traveling along the $z$-direction in a **lossy** medium:
> $$
 w(z,t) = A e^{-\alpha z}\cos(2\pi f t - \beta z),
 $$
> where  
> - $A=5$ (initial amplitude),  
> - $\alpha = 0.2\ \text{m}^{-1}$ (attenuation constant),  
> - $f = 0.5\ \text{kHz}$,  
> - phase velocity $u_p = 2\ \text{km/s}$.  
>
> Determine:  
> (a) Angular frequency $\omega$  
> (b) Phase constant $\beta$  
> (c) Wavelength $\lambda$  
> (d) Sketch qualitatively the wave at several instants in time.

---

### Theory recap  

Standard relationships (Ulaby, plane waves in general media):

- Angular frequency:
  $$
  \omega = 2\pi f.
  $$
- Phase constant:
  $$
  \beta = \frac{\omega}{u_p} = \frac{2\pi f}{u_p}.
  $$
- Wavelength:
  $$
  \lambda = \frac{2\pi}{\beta} = \frac{u_p}{f}.
  $$
- Attenuation:
  $$
  \text{Amplitude}(z) = A e^{-\alpha z},
  $$
  decreasing exponentially with $z$.

---

### Derivation  

Given $f = 0.5\ \text{kHz} = 500\ \text{Hz}$, $u_p = 2\ \text{km/s} = 2000\ \text{m/s}$, $\alpha = 0.2\ \text{m}^{-1}$.

#### (a) Angular frequency  

$$
\omega = 2\pi f = 2\pi\cdot 500 = 1000\pi\ \text{rad/s}.
$$

---

#### (b) Phase constant  

$$
\beta = \frac{\omega}{u_p} = \frac{1000\pi}{2000} = \frac{\pi}{2}\ \text{rad/m}.
$$

---

#### (c) Wavelength  

$$
\lambda = \frac{2\pi}{\beta} = \frac{2\pi}{\pi/2} = 4\ \text{m}.
$$

---

#### (d) Qualitative sketch  

At fixed times $t = 0, 0.25, 0.5, 0.75\ \text{ms}$, the spatial profile $w(z,t)$ is a cosine with:

- Spatial period $\lambda = 4\ \text{m}$  
- Envelope decaying as $e^{-0.2z}$  
- Wavefronts moving at $u_p = 2\ \text{km/s}$ in the $+z$ direction (due to $-\beta z$ inside the cosine).

---

### Final boxed results  

$$
\boxed{\omega = 1000\pi\ \text{rad/s}}
$$

$$
\boxed{\beta = \dfrac{\pi}{2}\ \text{rad/m}}
$$

$$
\boxed{\lambda = 4\ \text{m}}
$$

Wave expression explicitly:
$$
\boxed{
w(z,t) = 5 e^{-0.2 z}\cos\left(1000\pi t - \frac{\pi}{2} z\right)
}
$$

---

### Notes  

- Very typical exam move: compute $(\omega,\beta,\lambda)$ from $(f,u_p)$ and vice versa.  
- Common unit pitfall: forgetting to convert kHz → Hz or km/s → m/s.  
- Matches official solution (same numerical values).

---

### MATLAB — Exercise 2.2 (verification)  

> [!code]- MATLAB — Exercise 2.2 (verification)  
>```matlab
>A     = 5;
>alpha = 0.2;        % 1/m
>f     = 0.5e3;      % Hz
>up    = 2e3;        % m/s
>
>w  = 2*pi*f;
>beta = w/up;
>lambda = 2*pi/beta;
>
>fprintf('omega = %g rad/s\n', w);
>fprintf('beta  = %g rad/m\n', beta);
>fprintf('lambda= %g m\n', lambda);
>
>% Plot wave at several times
>z = linspace(0,10,500);
>t_vals = [0 0.25e-3 0.5e-3 0.75e-3];
>
>figure; hold on; grid on;
>for k = 1:numel(t_vals)
 >   t = t_vals(k);
>    wz = A*exp(-alpha*z).*cos(w*t - beta*z);
>    plot(z, wz, 'DisplayName', sprintf('t = %.2f ms', t*1e3));
>end
>xlabel('z [m]'); ylabel('w(z,t)');
>legend show;
>title('Exercise 2.2: Lossy traveling wave');
>```


---

# Exercise 2.3  
### Determining attenuation constant from amplitude measurements

> **Given**  
> An EM wave traveling in **seawater** has amplitude  
> - $A(z_1) = 98.02\ \text{V/m}$ at depth $z_1 = 10\ \text{m}$,  
> - $A(z_2) = 81.87\ \text{V/m}$ at depth $z_2 = 100\ \text{m}$.  
>
> The amplitude function (as from Exercise 2.2) is:
> $$
 A(z) = A_0 e^{-\alpha z}
 $$
>
> Find the attenuation constant $\alpha$:
> - in $\text{Np/m}$ or $\text{Np/km}$,  
> - optionally converted to $\text{dB/km}$.

---

### Theory recap  

For a wave with amplitude $A(z) = A_0 e^{-\alpha z}$:

- At two depths $z_1,z_2$:
  $$
  \frac{A(z_1)}{A(z_2)} = \frac{A_0 e^{-\alpha z_1}}{A_0 e^{-\alpha z_2}}
  = e^{\alpha (z_2 - z_1)}
  $$
- Hence:
  $$
  \alpha = \frac{1}{z_2 - z_1}\ln\left(\frac{A(z_1)}{A(z_2)}\right)
  $$
- Conversion Np ↔ dB:
  $$
  1\ \text{Np} = 8.686\ \text{dB}
  $$

---

### Derivation  

Given:
$$
A(z_1) = 98.02,\quad A(z_2) = 81.87,\quad z_1 = 10\ \text{m},\ z_2 = 100\ \text{m}.
$$
Compute ratio:
$$
\frac{A(z_1)}{A(z_2)} = \frac{98.02}{81.87}.
$$
Then
$$
\alpha = \frac{1}{z_2 - z_1}\ln\left(\frac{A(z_1)}{A(z_2)}\right)
       = \frac{1}{90}\ln\left(\frac{98.02}{81.87}\right)\ \text{m}^{-1}.
$$
Numerically (as in official solution):
$$
\alpha = 2\ \text{km}^{-1} = 2\ \text{Np/km}.
$$

Convert to dB/km:
$$
\alpha_{\text{dB/km}} = 2 \times 8.686 \approx 17.4\ \text{dB/km}.
$$

---

### Final boxed results  

$$
\boxed{\alpha = 2\ \text{Np/km} = 2\times 10^{-3}\ \text{Np/m}}
$$

$$
\boxed{\alpha \approx 17.4\ \text{dB/km}}
$$

---

### Notes  

- Standard technique: take **log of amplitude ratio** to extract $\alpha$.  
- Common pitfall: mixing up $z_1,z_2$ sign; always use $z_2>z_1$ to keep $\alpha>0$ when amplitude decreases.  
- Matches official solution (same $\alpha$ in Np/km and dB/km).

---

### MATLAB — Exercise 2.3 (verification)  

> [!code]- MATLAB — Exercise 2.3 (verification)
>```matlab
>A1 = 98.02;   % V/m at z1
>A2 = 81.87;   % V/m at z2
>z1 = 10;      % m
>z2 = 100;     % m
>alpha_m = (1/(z2 - z1))*log(A1/A2);  % Np/m
>alpha_km = alpha_m*1e3;              % Np/km
>alpha_dB_km = alpha_km*8.686;        % dB/km
>fprintf('alpha = %g Np/m = %g Np/km = %g dB/km\n',alpha_m, alpha_km, alpha_dB_km);
>```

---

# Exercise 2.4  
### Determining phase velocity from phase delay

> **Given**  
> A sinusoidal wave with frequency $f = 50\ \text{MHz}$ propagates along a **transmission line** of length $\ell = 1\ \text{m}$.  
> A phase delay of $\varphi_d = \pi/2$ (radians) is measured between input and output.  
>
> Determine:  
> (a) Time delay $t_d$ between input and output.  
> (b) Phase velocity $u_p$ along the line.

---

### Theory recap  

For a sinusoid at angular frequency $\omega = 2\pi f$:

- Phase delay, time delay, and spatial phase constant are related by
  $$
  \varphi_d = \omega t_d = \beta \ell.
  $$
- From this, the **time delay** is
  $$
  t_d = \frac{\varphi_d}{\omega} = \frac{\varphi_d}{2\pi f}.
  $$
- The **phase velocity** can be written in two equivalent ways:
  $$
  u_p = \frac{\omega}{\beta}
      = \frac{\ell}{t_d}
      = \frac{2\pi f\,\ell}{\varphi_d}.
  $$

This explicitly uses both the **temporal** (via $\omega t_d$) and **spatial** (via $\beta\ell$) interpretations of phase delay.

---

### Derivation  

Given $f = 50\ \text{MHz} = 50\times 10^6\ \text{Hz}$, $\varphi_d = \pi/2$, $\ell = 1\ \text{m}$.

#### (a) Time delay  

Compute angular frequency:
$$
\omega = 2\pi f = 2\pi\cdot 50\times 10^6 = 100\pi\times 10^6\ \text{rad/s}.
$$

Using $\varphi_d = \omega t_d$:
$$
t_d = \frac{\varphi_d}{\omega}
    = \frac{\pi/2}{2\pi\cdot 50\times 10^6}
    = \frac{1}{4\cdot 50\times 10^6}
    = \frac{1}{200\times 10^6}
    = 5\times 10^{-9}\ \text{s}
    = 5\ \text{ns}.
$$

This is the time it takes for a **given phase point** of the wave to travel from input to output.

---

#### (b) Phase velocity  

We can now use
$$
u_p = \frac{\ell}{t_d},
$$
so
$$
u_p = \frac{1\ \text{m}}{5\times 10^{-9}\ \text{s}}
    = 2\times 10^8\ \text{m/s}.
$$

Alternatively, using the combined expression:
$$
u_p = \frac{2\pi f\,\ell}{\varphi_d}
    = \frac{2\pi\cdot 50\times 10^6\cdot 1}{\pi/2}
    = 2\times 10^8\ \text{m/s},
$$
which is the same result.

Compared to the speed of light $c_0 \approx 3\times 10^8\ \text{m/s}$:
$$
u_p \approx \frac{2}{3}c_0.
$$

---

### Final boxed results  

$$
\boxed{t_d = 5\ \text{ns}}
$$

$$
\boxed{u_p = 2\times 10^8\ \text{m/s} \approx \dfrac{2}{3}c_0}
$$

---

### Notes  

- This exercise ties together:
  - **Temporal** phase delay: $\varphi_d = \omega t_d$  
  - **Spatial** phase delay along the line: $\varphi_d = \beta \ell$  
  - **Phase velocity**: $u_p = \dfrac{\omega}{\beta} = \dfrac{\ell}{t_d}$.  
- Typical TL-exam pattern: from a measured phase shift over a known length at a known frequency, recover $t_d$ and $u_p$.  
- Common pitfalls:
  - Forgetting to convert MHz → Hz.  
  - Incorrectly treating $\varphi_d$ in degrees instead of radians.  
- Result matches the official solution numerically and conceptually.

---

### MATLAB — Exercise 2.4 (verification)  

> [!code]- MATLAB — Exercise 2.4 (verification)  
> ```matlab
>f     = 50e6;       % Hz
>phi_d = pi/2;       % rad
>l     = 1;          % m
>
>omega = 2*pi*f;
>
>% Time delay from phase delay
>t_d = phi_d/omega;
>
>% Phase velocity from time delay
>u_p_time = l/t_d;
>
>% Phase velocity directly from formula u_p = 2*pi*f*l / phi_d
>u_p_direct = 2*pi*f*l / phi_d;
>
>fprintf('Time delay t_d = %g s (%g ns)\n', t_d, t_d*1e9);
>fprintf('Phase velocity (from t_d)   u_p = %g m/s\n', u_p_time);
>fprintf('Phase velocity (direct)     u_p = %g m/s\n', u_p_direct);
>```
