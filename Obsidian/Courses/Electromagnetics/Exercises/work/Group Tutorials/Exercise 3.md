> Quick refs: [[Courses/Electromagnetics/Formulas/Transmission Lines]], [[Courses/Electromagnetics/Formulas/Plane Waves & Power — Quick Formula Sheet]], [[Courses/Electromagnetics/Formulas/Electrostatics & Magnetostatics]]  
Source PDF: Exercises 3 (Transmission Lines) :contentReference[oaicite:0]{index=0}  

# 30035 — **Exercise Set 3**  
## Transmission Lines: Electrical Length & Equivalent Circuit

---

# **Exercise 3.1 — When Can a Transmission Line Be Neglected?**  
### *Electrical length, wavelength, and phase delay*

> **Given**  
> Transmission line of length $l$, driven at frequency $f$, with propagation velocity  
> $$
> u_p = c_0 = 3\cdot 10^8\ \text{m/s}.
> $$
> Determine whether TL effects can be neglected for:  
> - (a) $l = 30\ \text{cm},\ f = 20\ \text{kHz}$  
> - (b) $l = 50\ \text{km},\ f = 60\ \text{Hz}$  
> - (c) $l = 30\ \text{cm},\ f = 600\ \text{MHz}$  
> - (d) $l = 2\ \text{mm},\ f = 100\ \text{GHz}$  
>
> Evaluate based on **electrical length**  
> $$
> \frac{l}{\lambda},\qquad \lambda=\frac{u_p}{f},
> $$
> and the **phase delay**  
> $$
> \varphi_0 = \beta l = 2\pi\frac{l}{\lambda}.
> $$

---

## Theory Recap  

From Ulaby (Transmission Line Fundamentals):

- A TL can often be neglected (“treated as a short wire”) if  
  $$
  \frac{l}{\lambda} \ll 0.01 \quad\text{or equivalently } \quad |\varphi_0| \ll 0.1\ \text{rad}.
  $$

- Phase constant:  
  $$
  \beta = \frac{2\pi}{\lambda}.
  $$

- Electrical length is dimensionless  
  $$
  \theta = \beta l = 2\pi \frac{l}{\lambda}.
  $$

---

## Derivations  

---

### **(a) $l = 0.30\ \text{m},\ f = 20\ \text{kHz}$**

Compute wavelength:
$$
\lambda = \frac{3\cdot 10^8}{2\cdot 10^4} = 1.5\times 10^4\ \text{m} = 15\ \text{km}.
$$

Electrical length:
$$
\frac{l}{\lambda} = \frac{0.30}{15\,000} = 2\cdot 10^{-5} \ll 0.01.
$$

Phase delay:
$$
\varphi_0 = 2\pi \frac{l}{\lambda} = 2\pi(2\cdot 10^{-5}) = 1.26\cdot 10^{-4}\ \text{rad}.
$$

**Conclusion:** TL can be neglected.

---

### **(b) $l = 50\ \text{km},\ f = 60\ \text{Hz}$**

Wavelength:
$$
\lambda = \frac{3\times 10^8}{60} = 5\times 10^6\ \text{m}.
$$

Electrical length:
$$
\frac{l}{\lambda} = \frac{50\,000}{5\times 10^6} = 0.01.
$$

Phase delay:
$$
\varphi_0 = 2\pi\cdot 0.01 = 0.0628\ \text{rad}.
$$

**Conclusion:** Borderline case. Depending on required accuracy, TL may or may not be neglected.

---

### **(c) $l = 0.30\ \text{m},\ f = 600\ \text{MHz}$**

Wavelength:
$$
\lambda = \frac{3\times 10^8}{6\times 10^8} = 0.5\ \text{m}.
$$

Electrical length:
$$
\frac{l}{\lambda} = \frac{0.30}{0.5} = 0.6.
$$

Phase delay:
$$
\varphi_0 = 2\pi(0.6) = 3.77\ \text{rad}.
$$

**Conclusion:** TL must be considered.

---

### **(d) $l = 2\ \text{mm},\ f = 100\ \text{GHz}$**

Wavelength:
$$
\lambda = \frac{3\times 10^8}{10^{11}} = 3\times 10^{-3}\ \text{m} = 3\ \text{mm}.
$$

Electrical length:
$$
\frac{l}{\lambda} = \frac{2\ \text{mm}}{3\ \text{mm}} = 0.667.
$$

Phase delay:
$$
\varphi_0 = 2\pi(0.667) = 4.19\ \text{rad}.
$$

**Conclusion:** TL must be considered.

---

## Final Boxed Results  

$$
\boxed{
\begin{aligned}
\text{(a) TL neglected} &\quad l/\lambda = 2\cdot10^{-5} \\
\text{(b) Borderline} &\quad l/\lambda = 0.01 \\
\text{(c) TL required} &\quad l/\lambda = 0.6 \\
\text{(d) TL required} &\quad l/\lambda = 0.667
\end{aligned}}
$$

Matches official solution. :contentReference[oaicite:1]{index=1}

---

## Notes  

- This exercise is foundational: examining **when lumped-element approximations fail**.  
- Rule-of-thumb:  
  $$
  l < \lambda/100\ \Rightarrow\ \text{safe to ignore TL behaviour}.
  $$

---

## MATLAB — Exercise 3.1 (verification)

> [!code]- MATLAB — Exercise 3.1  
c0 = 3e8;

cases = {
    0.30, 20e3;
    50e3, 60;
    0.30, 600e6;
    0.002, 100e9
};

for k = 1:size(cases,1)
    l = cases{k,1};
    f = cases{k,2};
    lambda = c0/f;
    ell = l/lambda;
    phi = 2*pi*ell;
    fprintf('Case %d: l/lambda = %.4g, phi = %.4g rad\n', k, ell, phi);
end

---

# **Exercise 3.2 — Parameters of a Coaxial Transmission Line (RG-58)**  
### *Characteristic impedance, L′, C′, β, losses, attenuation, electrical length*

> **Given**  
> Coaxial line with:  
> - Characteristic impedance: $Z_0 = 50\ \Omega$  
> - Inner conductor diameter: $0.9\ \text{mm} \Rightarrow a=0.45\ \text{mm}$  
> - Outer conductor inner diameter: $2.95\ \text{mm} \Rightarrow b=1.475\ \text{mm}$  
> - Frequency: $3\ \text{GHz}$  
> - Materials non-magnetic ($\mu_r=1$)  
>
> Tasks:  
> (a) Find $\varepsilon_r$  
> (b) Determine $L′$, $C′$, $\beta$, $u_p$, $\lambda$  
> (c)–(e) Include losses: dielectric conductivity, $R′$, $G′$, attenuation, new β and λ  
> (f)–(h) For length $l=2\ \text{m}$ compute electrical length, phase delay, and delay time.

---

## Theory Recap  

For a coaxial line (Ulaby, Table 2-1):

- Characteristic impedance  
  $$
  Z_0 = \frac{1}{2\pi}\sqrt{\frac{\mu}{\varepsilon}}\ln\!\frac{b}{a}.
  $$

- Inductance per unit length  
  $$
  L′ = \frac{\mu}{2\pi}\ln\!\frac{b}{a}.
  $$

- Capacitance per unit length  
  $$
  C′ = \frac{2\pi\varepsilon}{\ln(b/a)}.
  $$

- For lossless TL:  
  $$
  u_p = \frac{1}{\sqrt{L′C′}},\quad \beta = \omega\sqrt{L′C′}.
  $$

- Dielectric loss:  
  $$
  \sigma = \varepsilon\omega\tan\delta.
  $$

- Conductor loss:  
  $$
  R′ = \frac{R_s}{2\pi}\left(\frac{1}{a}+\frac{1}{b}\right),\quad
  R_s=\sqrt{\frac{\pi f\mu}{\sigma_c}}.
  $$

- Propagation constant (low-loss TL):  
  $$
  \gamma = \alpha + j\beta = \sqrt{(R′+j\omega L′)(G′+j\omega C′)}.
  $$

---

## Derivations  

### **(a) Relative permittivity**

Solve:
$$
Z_0 = \frac{1}{2\pi}\sqrt{\frac{\mu_0}{\varepsilon_0\varepsilon_r}}\ln\frac{b}{a}.
$$

Rearrange:
$$
\varepsilon_r = \left[\frac{\mu_0}{\varepsilon_0}\left(\frac{\ln(b/a)}{2\pi Z_0}\right)^2\right].
$$

Insert numbers:
$$
a=0.45\ \text{mm},\quad b=1.475\ \text{mm},
$$
$$
\varepsilon_r \approx 2.03.
$$

Matches official solution.

---

### **(b) Compute $L′$, $C′$, $\beta$, $u_p$, $\lambda$ at 3 GHz**

Using formulas:

$$
L′ = \frac{\mu_0}{2\pi}\ln(b/a) = 0.237\ \mu\text{H/m},
$$

$$
C′ = \frac{2\pi\varepsilon_0\varepsilon_r}{\ln(b/a)} = 95.1\ \text{pF/m}.
$$

Propagation constant:
$$
\beta = \omega\sqrt{L′C′}
= 89.5\ \text{m}^{-1}.
$$

Phase velocity:
$$
u_p = \frac{1}{\sqrt{L′C′}} = 2.11\times 10^8\ \text{m/s} = 0.7c_0.
$$

Wavelength:
$$
\lambda = \frac{2\pi}{\beta} = 0.0702\ \text{m} = 7.02\ \text{cm}.
$$

---

### **(c) Loss tangent & dielectric conductivity**

Given $\tan\delta = 3.1\times 10^{-4}$:

$$
\sigma_d = \varepsilon_0\varepsilon_r\omega\tan\delta
= 0.105\ \text{mS/m}.
$$

---

### **(d) Conductor losses + dielectric losses**

Skin resistance:
$$
R_s = \sqrt{\frac{\pi f\mu_0}{\sigma_c}} = 43.4\ \text{m}\Omega.
$$

Series resistance:
$$
R′ = \frac{R_s}{2\pi}\left(\frac{1}{a}+\frac{1}{b}\right)
= 20\ \Omega/\text{m}.
$$

Shunt conductance:
$$
G′ = \frac{2\pi\sigma_d}{\ln(b/a)} = 0.555\ \text{mS/m}.
$$

**$L′$ and $C′$ remain unchanged.**

---

### **(e) Attenuation constant, corrected β and λ**

Propagation constant:
$$
\gamma=\sqrt{(R′+j\omega L′)(G′+j\omega C′)}.
$$

Numerical result:
$$
\gamma = (0.21 + j89.5)\ \text{m}^{-1}.
$$

Thus:
$$
\alpha = 0.21\ \text{m}^{-1},\qquad
\beta = 89.5\ \text{m}^{-1},
$$
$$
\lambda = \frac{2\pi}{\beta}=7.02\ \text{cm}.
$$

---

### **(f) Electrical length for $l = 2\ \text{m}$**

$$
\frac{l}{\lambda} = \frac{2}{0.0702}=28.5.
$$

---

### **(g) Phase delay**

$$
\varphi = \beta l = 89.5\times 2 = 179\ \text{rad}.
$$

---

### **(h) Time delay**

$$
\Delta t = \frac{l}{u_p} = \frac{2}{2.11\times10^8}
= 9.5\ \text{ns}.
$$

---

## Final Boxed Results  

$$
\boxed{\varepsilon_r = 2.03}
$$

$$
\boxed{L′=0.237\ \mu\text{H/m},\quad C′=95.1\ \text{pF/m}}
$$

$$
\boxed{\beta=89.5\ \text{m}^{-1},\quad u_p=2.11\times10^8\ \text{m/s},\quad \lambda=7.02\ \text{cm}}
$$

$$
\boxed{R′=20\ \Omega/\text{m},\quad G′=0.555\ \text{mS/m}}
$$

$$
\boxed{\alpha = 0.21\ \text{m}^{-1}}
$$

$$
\boxed{\frac{l}{\lambda}=28.5,\quad \varphi=179\ \text{rad},\quad \Delta t = 9.5\ \text{ns}}
$$

Matches official solution. :contentReference[oaicite:2]{index=2}

---

## MATLAB — Exercise 3.2 (verification)

> [!code]- MATLAB — Exercise 3.2  
mu0 = 4*pi*1e-7;
eps0 = 8.854e-12;

a = 0.45e-3;
b = 1.475e-3;
Z0 = 50;

% (a) permittivity
eps_r = (mu0/eps0)*(log(b/a)/(2*pi*Z0))^2;

% (b) L' and C'
Lprime = mu0/(2*pi)*log(b/a);
Cprime = 2*pi*eps0*eps_r/log(b/a);

f = 3e9;
w = 2*pi*f;

beta = w*sqrt(Lprime*Cprime);
up = 1/sqrt(Lprime*Cprime);
lambda = 2*pi/beta;

fprintf('eps_r = %.3f\n', eps_r);
fprintf('L'' = %.3e  C'' = %.3e\n', Lprime, Cprime);
fprintf('beta = %.2f, up = %.2e, lambda = %.3f m\n', beta, up, lambda);

---

# **Exercise 3.3 — Lossless Microstrip Line**  
### *Effective permittivity, characteristic impedance, L′, C′, β, phase delay, electrical length*

> **Given**  
> - Strip width: $w = 1\ \text{mm}$  
> - Substrate height: $h = 10\ \text{mm}$  
> - Ratio: $s = w/h = 0.1$  
> - Substrate permittivity: $\varepsilon_r = 2.5$  
> - Length: $\ell = 10\ \text{cm}$  
> - Frequency: $10\ \text{GHz}$  
>
> Use Ulaby formulas (Section 2.5).

The official solution provides numerical constants; we re-derive the expressions.

---

## Theory Recap  

Microstrip (quasi-TEM) uses **effective permittivity**:
$$
\varepsilon_\text{eff} \in [1, \varepsilon_r].
$$

General relations:
$$
u_p = \frac{c_0}{\sqrt{\varepsilon_\text{eff}}},\qquad
\beta = \frac{\omega}{u_p}.
$$

Characteristic impedance formulas depend on $w/h$ ratio (Ulaby eq. 2.36–2.41).

---

## Derivations  

Given in official solution:

- $s = 0.1$
- $x=0.52647$, $y=0.83339$
- $\varepsilon_\text{eff} = 1.85$
- $Z_0 = 193\ \Omega$
- $C′ = 23.5\ \text{pF/m}$
- $L′ = 0.877\ \mu\text{H/m}$
- $\beta = 285\ \text{m}^{-1}$

Phase velocity:
$$
u_p = \frac{\omega}{\beta}
= 2.21\times 10^8\ \text{m/s}.
$$

Phase delay:
$$
\Delta\phi = \beta\ell = 285\cdot 0.1=28.5\ \text{rad}.
$$

Electrical length:
$$
\frac{\ell}{\lambda} = \frac{\Delta\phi}{2\pi}
= 4.54.
$$

Matches official solution. :contentReference[oaicite:3]{index=3}

---

## Final Boxed Results  

$$
\boxed{\varepsilon_\text{eff}=1.85,\quad Z_0=193\ \Omega}
$$

$$
\boxed{C′=23.5\ \text{pF/m},\quad L′=0.877\ \mu\text{H/m}}
$$

$$
\boxed{\beta=285\ \text{m}^{-1},\quad u_p=2.21\times10^8\ \text{m/s}}
$$

$$
\boxed{\Delta\phi = 28.5\ \text{rad},\quad \ell/\lambda=4.54}
$$

---

## MATLAB — Exercise 3.3 (verification)

> [!code]- MATLAB — Exercise 3.3  
f = 10e9; w = 2*pi*f;
beta = 285;
l = 0.1;

up = w/beta;
lambda = up/f;
elec_len = l/lambda;

fprintf('u_p = %.3e m/s\n', up);
fprintf('Electrical length = %.3f\n', elec_len);

