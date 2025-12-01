> Quick refs: [[Courses/Electromagnetics/Formulas/Transmission Lines]], [[Courses/Electromagnetics/Formulas/Reflection & Matching]], [[Courses/Electromagnetics/Formulas/Plane Waves & Power — Quick Formula Sheet]]  
Source PDF: Exercises 4 (Single-Termination TLs) :contentReference[oaicite:0]{index=0}  

# 30035 — **Exercise Set 4**  
## Transmission Lines: Single-Termination

---

# **Exercise 4.1 — Reflection Coefficient & Standing Wave Locations**  
### *300 Ω air line, series RL load at 5 MHz*

> **Given**  
> - TL: $Z_0 = 300\ \Omega$ (lossless, air → $u_p = c_0$)  
> - Load: resistor + inductor in series  
>   $$
>   Z_L = 600\ \Omega + j\omega L,\qquad L=0.02\ \text{mH}
>   $$
> - Operating frequency: $f = 5\ \text{MHz}$  
> - Compute:  
>   (a) Reflection coefficient $\Gamma_L$ at the load  
>   (b) Distance to nearest **voltage maximum** from the load  
>   (c) Distance to nearest **current maximum** from the load  

---

## Theory Recap  

### Reflection coefficient at load
For a load $Z_L$ on a TL with characteristic impedance $Z_0$:
$$
\Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}.
$$

### Standing-wave pattern on a lossless TL
- Voltage maxima occur where $\Gamma_\text{in}$ is **real and positive**.  
- Current maxima occur where $\Gamma_\text{in}$ is **real and negative**.  
- Moving a distance $d$ away from the load corresponds to a rotation of  
  $$
  \Gamma_\text{in}(d)=\Gamma_L e^{-j2\beta d}.
  $$
- Wavelength in air:  
  $$
  \lambda = \frac{u_p}{f} = \frac{c_0}{f}.
  $$

- Distance to first voltage maximum:  
  $$
  d_\text{Vmax} = \frac{\theta_r \lambda}{4\pi},\qquad \theta_r=\arg(\Gamma_L).
  $$

- Current maxima are shifted by $\lambda/4$.

---

## Geometry / Setup  

We calculate:

1. Load impedance  
2. Reflection coefficient magnitude and phase  
3. Wavelength at 5 MHz  
4. Use TL rotation relation to find Vmax and Imax nodes.

---

## Derivations  

### **(a) Reflection coefficient at the load**

Angular frequency:
$$
\omega = 2\pi f = 31.4\ \text{Mrad/s}.
$$

Reactive load component:
$$
X_L = \omega L = 31.4\times 10^6 \cdot 0.02\times 10^{-3}
= 628.32\ \Omega.
$$
Thus
$$
Z_L = 600 + j628.32\ \Omega.
$$

Compute reflection coefficient:
$$
\Gamma_L 
= \frac{(600 + j628.32)-300}{(600 + j628.32)+300}
= \frac{300 + j628.32}{900 + j628.32}.
$$

Official result (verified):
$$
\Gamma_L = 0.552 + j0.313 = 0.6346\angle 29.55^\circ.
$$

---

### **(b) Location of nearest voltage maximum**

Wavelength:
$$
\lambda = \frac{c_0}{f} 
= \frac{3\times 10^8}{5\times 10^6}
= 60\ \text{m}.
$$

Phase angle of $\Gamma_L$:
$$
\theta_r = 29.55^\circ = 0.5159\ \text{rad}.
$$

Voltage maximum at distance:
$$
d_\text{Vmax}
= \frac{\theta_r\lambda}{4\pi}
= \frac{0.5159 \cdot 60}{4\pi}
= 2.46\ \text{m}.
$$

---

### **(c) Location of nearest current maximum**

Current maxima occur at:
$$
d_\text{Imax} = d_\text{Vmax} + \frac{\lambda}{4}.
$$

Compute shift:
$$
\frac{\lambda}{4} = 15\ \text{m}.
$$

Thus:
$$
d_\text{Imax} = 2.46 + 15 = 17.5\ \text{m}.
$$

---

## Final Boxed Results  

$$
\boxed{\Gamma_L = 0.552 + j0.313 = 0.6346\angle 29.55^\circ}
$$

$$
\boxed{d_\text{Vmax} = 2.46\ \text{m}}
$$

$$
\boxed{d_\text{Imax} = 17.5\ \text{m}}
$$

Matches official solution. :contentReference[oaicite:1]{index=1}

---

## Notes  

- Key exam pattern: interpret standing waves directly from $\Gamma_L$ instead of full field expressions.  
- Moving along TL = **rotation in the Γ-plane**.  
- Useful shortcut:  
  - Vmax → positive real Γ  
  - Imax → negative real Γ  

---

## MATLAB — Exercise 4.1 (verification)

> [!code]- MATLAB — Exercise 4.1  
Z0 = 300;
L  = 0.02e-3;
f  = 5e6;  w = 2*pi*f;
ZL = 600 + 1j*w*L;

GammaL = (ZL - Z0)./(ZL + Z0);

lambda = 3e8/f;
theta_r = angle(GammaL);

dV = theta_r*lambda/(4*pi);
dI = dV + lambda/4;

fprintf('Gamma_L = %.4f + j%.4f\n', real(GammaL), imag(GammaL));
fprintf('Vmax distance = %.3f m\n', dV);
fprintf('Imax distance = %.3f m\n', dI);

---

# **Exercise 4.2 — Determine Load from Reflection Coefficient**  

> **Given**  
> - TL characteristic impedance: $Z_0 = 75\ \Omega$  
> - Reflection coefficient at load:  
>   $$
>   \Gamma_L = j0.75.
>   $$  
> - Find the load impedance $Z_L$.

---

## Theory Recap  

Inversion formula:
$$
Z_L = Z_0\frac{1+\Gamma_L}{1-\Gamma_L}.
$$

---

## Derivation  

Compute:
$$
Z_L = 75 \frac{1 + j0.75}{1 - j0.75}.
$$

Multiply numerator & denominator by conjugate:
$$
Z_L = 75 \frac{(1+j0.75)(1+j0.75)}{1+(0.75)^2}
= 75\frac{1 + 1.5j - 0.5625}{1.5625}.
$$

Simplify:
$$
Z_L = 75\left(\frac{0.4375}{1.5625} + j\frac{1.5}{1.5625}\right)
= 75(0.28 + j0.96)
= 21 + j72\ \Omega.
$$

Matches official result. :contentReference[oaicite:2]{index=2}

---

## Final Boxed Result  

$$
\boxed{Z_L = 21 + j72\ \Omega}
$$

---

## MATLAB — Exercise 4.2

> [!code]- MATLAB — Exercise 4.2  
Z0 = 75;
Gamma = 1j*0.75;

ZL = Z0*(1+Gamma)/(1-Gamma);
disp(ZL);

---

# **Exercise 4.3 — Input Reflection Coefficient & Input Impedance**  
### *100 Ω lossless line, length 0.35λ, load 60 + j30 Ω*

> **Given**  
> - TL: $Z_0 = 100\ \Omega$  
> - Length: $l = 0.35\lambda$  
> - Load: $Z_L = 60 + j30\ \Omega$  
> - Compute:  
>   (a) Draw circuit  
>   (b) $\Gamma_L$  
>   (c) $\Gamma_\text{in}$  
>   (d) $Z_\text{in}$  

---

## Theory Recap  

Reflection coefficient at load:
$$
\Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}.
$$

Propagation on a lossless TL:
$$
\Gamma_\text{in} = \Gamma_L e^{-j2\beta l}
= \Gamma_L e^{-j4\pi l/\lambda}.
$$

Input impedance:
$$
Z_\text{in} = Z_0\frac{1+\Gamma_\text{in}}{1-\Gamma_\text{in}}.
$$

---

## Derivations  

### **(b) Reflection coefficient at the load**

$$
Z_L = 60 + j30.
$$

Compute:
$$
\Gamma_L = \frac{(60+j30)-100}{(60+j30)+100}
= \frac{-40 + j30}{160 + j30}.
$$

Given result:
$$
\Gamma_L = -0.21 + j0.23.
$$

Matches official. :contentReference[oaicite:3]{index=3}  

---

### **(c) Reflection coefficient at the input**

Given $l = 0.35\lambda$,
$$
\Gamma_\text{in}
= \Gamma_L e^{-j2\beta l}
= \Gamma_L e^{-j2(2\pi/\lambda)(0.35\lambda)}
= \Gamma_L e^{-j1.4\pi}.
$$

Numeric result (official):
$$
\Gamma_\text{in} = -0.151 - j0.267.
$$

---

### **(d) Input impedance**

Compute:
$$
Z_\text{in}
= 100\frac{1+\Gamma_\text{in}}{1-\Gamma_\text{in}}
= 64.8 - j38.3\ \Omega.
$$

Matches official. :contentReference[oaicite:4]{index=4}

---

## Final Boxed Results  

$$
\boxed{\Gamma_L = -0.21 + j0.23}
$$

$$
\boxed{\Gamma_\text{in} = -0.151 - j0.267}
$$

$$
\boxed{Z_\text{in} = 64.8 - j38.3\ \Omega}
$$

---

## MATLAB — Exercise 4.3

> [!code]- MATLAB — Exercise 4.3  
Z0 = 100;
ZL = 60 + 1j*30;
l = 0.35;

GammaL = (ZL - Z0)/(ZL + Z0);
Gamma_in = GammaL * exp(-1j*2*2*pi*l);
Zin = Z0*(1+Gamma_in)/(1-Gamma_in);

disp(GammaL);
disp(Gamma_in);
disp(Zin);

---

# **Exercise 4.4 — Load from Zero Input Reflection**  

> **Given**  
> - TL characteristic impedance: $Z_0 = 30\ \Omega$  
> - Input reflection coefficient: $\Gamma_\text{in}=0$  
> - Find load impedance $Z_L$.

---

## Theory  

For a **lossless** TL:
$$
\Gamma_\text{in}=0 \quad\Longleftrightarrow\quad Z_\text{in}=Z_0.
$$
Only possible if:
$$
Z_L = Z_0.
$$

---

## Final Boxed Result  

$$
\boxed{Z_L = 30\ \Omega}
$$

Matches official. :contentReference[oaicite:5]{index=5}

---

# **Exercise 4.5 — Transmission Lines in Series**  
### *Cascade of two different TLs terminated in complex load*

> **Given**  
> - Right TL:  
>   - $Z_0 = 50\ \Omega$, $l = 0.7\lambda$  
>   - Load: $Z_L = 60 - j30\ \Omega$  
> - Left TL:  
>   - $Z_0 = 75\ \Omega$, $l = 0.2\lambda$  
>   - Terminated by input of right TL  
>
> Compute the **overall input impedance**.

---

## Theory Recap  

Input impedance formula for arbitrary TL terminated in $Z_L$:
$$
Z_\text{in}
= Z_0\frac{Z_L + jZ_0\tan(\beta l)}{Z_0 + jZ_L\tan(\beta l)}.
$$

---

## Derivations  

### Step 1 — Right TL input impedance

Given result:
$$
Z_\text{in}^{(1)} = 28.8979 + j6.0275\ \Omega.
$$

---

### Step 2 — Left TL input impedance

Use previous result as its load:

Given:
$$
Z_\text{in} = 153 + j73\ \Omega.
$$

Matches official. :contentReference[oaicite:6]{index=6}

---

## Final Boxed Result  

$$
\boxed{Z_\text{in} = 153 + j73\ \Omega}
$$

---

## MATLAB — Exercise 4.5

> [!code]- MATLAB — Exercise 4.5  
ZL = 60 - 1j*30;

Z0r = 50; lr = 0.7*pi;   % Using beta*l = 2π*l/λ → absorbed into tan()
Z0l = 75; ll = 0.2*pi;

Zin1 = Z0r*(ZL + 1j*Z0r*tan(2*pi*0.7))/(Z0r + 1j*ZL*tan(2*pi*0.7));
Zin  = Z0l*(Zin1 + 1j*Z0l*tan(2*pi*0.2))/(Z0l + 1j*Zin1*tan(2*pi*0.2));

disp(Zin1);
disp(Zin);

---

# **Exercise 4.6 — Transmission Lines in Parallel**  

> **Given**  
> Two branches:  
> - Upper TL: $(75\ \Omega,\ l=0.2\lambda)$ terminated in $(60 - j30)\ \Omega$  
> - Lower TL: $(50\ \Omega,\ l=0.7\lambda)$ terminated in $(40 + j20)\ \Omega$  
>
> Determine the **overall input impedance**:
> $$
> Z_\text{in} = \left( \frac{1}{Z_\text{in}^{(1)}} + \frac{1}{Z_\text{in}^{(2)}} \right)^{-1}.
> $$

---

## Derivations  

Upper TL:
$$
Z_\text{in}^{(1)} = 56.915 + j27.204\ \Omega.
$$

Lower TL:
$$
Z_\text{in}^{(2)} = 68.495 - j22.674\ \Omega.
$$

Parallel combination:
$$
Z_\text{in} = 36.1 + j3.26\ \Omega.
$$

Matches official. :contentReference[oaicite:7]{index=7}

---

## Final Boxed Result  

$$
\boxed{Z_\text{in} = 36.1 + j3.26\ \Omega}
$$

---

## MATLAB — Exercise 4.6

> [!code]- MATLAB — Exercise 4.6  
Z1 = 56.915 + 1j*27.204;
Z2 = 68.495 - 1j*22.674;

Zin = (Z1*Z2)/(Z1 + Z2);
disp(Zin);

