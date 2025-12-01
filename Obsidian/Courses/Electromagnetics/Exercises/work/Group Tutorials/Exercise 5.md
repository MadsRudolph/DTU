> Quick refs: [[Courses/Electromagnetics/Formulas/Transmission Lines]], [[Courses/Electromagnetics/Formulas/Reflection & Matching]], [[Courses/Electromagnetics/Formulas/Plane Waves & Power — Quick Formula Sheet]]  
Source PDF: Exercises 5 (Transmission Line Circuits) :contentReference[oaicite:0]{index=0}  

# 30035 — **Exercise Set 5**  
## Transmission Line Circuits

---

# **Exercise 5.1 — Short-Circuited Line as a Reactive Load**  
### *Designing a reactance using a shorted TL at 300 MHz*

> **Problem**  
> At operating frequency $f = 300\ \text{MHz}$, we want to realize a **pure reactance**  
> $$
> X = +40\ \Omega
> $$
> using a section of a **lossless, 50 Ω TL** terminated in a **short circuit**:
>
> - Line: $Z_0 = 50\ \Omega$, lossless  
> - Termination: short circuit at the far end ($Z_L = 0$)  
> - Phase velocity: $u_p = 0.75c_0$  
>
> **Find:** The **shortest possible line length** $l$ that yields an input reactance $X = +40\ \Omega$ at $f = 300\ \text{MHz}$.

---

## Theory Recap  

For a **lossless** line of characteristic impedance $Z_0$ and length $l$:

- Propagation constant:  
  $$
  \gamma = j\beta,\qquad \beta = \frac{\omega}{u_p} = \frac{2\pi f}{u_p}.
  $$

- Input impedance of a **short-circuited** TL:  
  $$
  Z_\text{in}^{(\text{sc})}
  = jZ_0\tan(\beta l).
  $$

This is purely **imaginary**, so it mimics an ideal inductor or capacitor depending on the sign.

If we want a **specified reactance** $X$:
$$
X = Z_0\tan(\beta l)
\quad\Rightarrow\quad
\beta l = \arctan\left(\frac{X}{Z_0}\right) + n\pi,\quad n\in\mathbb{Z}.
$$

The **shortest non-zero** physical length corresponds to the **principal value** with $n=0$:
$$
l_\text{min} = \frac{1}{\beta}\arctan\left(\frac{X}{Z_0}\right).
$$

---

## Geometry / Setup  

- TEM propagation, single uniform section of line, shorted at far end.  
- At the input, we see a reactive impedance “generated” by the quarter-wave transformer-like behaviour.  
- We tune $l$ such that $Z_\text{in}$ matches the desired $jX$ at the given frequency.

---

## Derivation  

Given:
- $Z_0 = 50\ \Omega$  
- Desired $X = 40\ \Omega$  
- $f = 300\ \text{MHz}$  
- $u_p = 0.75c_0$  

1. **Phase constant**:
   $$
   \beta = \frac{\omega}{u_p}
         = \frac{2\pi f}{u_p}.
   $$

2. **Reactance condition**:
   $$
   X = Z_0\tan(\beta l)
   \Rightarrow
   \beta l = \arctan\left(\frac{X}{Z_0}\right)
           = \arctan\left(\frac{40}{50}\right).
   $$
   Numerically:
   $$
   \beta l \approx \arctan(0.8) \approx 0.67474\ \text{rad}.
   $$

3. **Shortest length**:
   $$
   l_\text{min} = \frac{1}{\beta}\arctan\left(\frac{40}{50}\right)
                = \frac{u_p}{\omega}\arctan\left(\frac{40}{50}\right)
                = \frac{0.75c_0}{2\pi f}\arctan\left(\frac{40}{50}\right).
   $$

Insert numbers (as in the official solution):  
Result:
$$
l_\text{min} \approx 8.05\ \text{cm}.
$$

Matches official solution. :contentReference[oaicite:1]{index=1}  

---

## Final Boxed Result  

$$
\boxed{
Z_\text{in}^{(\text{sc})} = jZ_0\tan(\beta l),\quad
\beta l = \arctan\left(\frac{X}{Z_0}\right),\quad
l_\text{min} \approx 8.05\ \text{cm}
}
$$

---

## Notes  

- This is a classic **stub matching** idea: a shorted stub used as a tunable inductive reactance.  
- For purely capacitive reactance ($X<0$), the same formula applies but yields a negative tangent → capacitive behaviour.  
- Very exam-typical: they love “design a stub length that gives this reactance at frequency $f$”.

---

## MATLAB — Exercise 5.1 (verification)

> [!code]- MATLAB — Exercise 5.1  
c0   = 3e8;
f    = 300e6;
Z0   = 50;
Xdes = 40;
up   = 0.75*c0;

w  = 2*pi*f;
beta = w/up;

beta_l = atan(Xdes/Z0);
l_min  = beta_l/beta;

fprintf('beta*l = %.5f rad\n', beta_l);
fprintf('l_min  = %.5f m (%.2f cm)\n', l_min, l_min*100);

% Check that Zin has desired reactance
Zin = 1j*Z0 * tan(beta*l_min);
fprintf('Zin ≈ j%.2f Ohm\n', imag(Zin));

---

# **Exercise 5.2 — Determining TL Parameters from Short/Open Measurements**  
### *Extracting $Z_0$, phase velocity, and $\varepsilon_r$ from impedance data*

> **Problem**  
> A **lossless TEM TL** of length $\ell = 36\ \text{cm}$ has **unknown characteristic impedance** $Z_0$ and is filled with a **non-magnetic dielectric** (i.e., $\mu_r = 1$).
>
> At frequency $f = 1\ \text{MHz}$, the **input impedance** was measured for two terminations:
>
> 1. **Short circuit at the load** → input impedance equivalent to an inductor:
>    $$
>    Z_\text{in}^{(\text{sc})} = j\omega L_\text{eq}, \quad L_\text{eq} = 0.064\ \mu\text{H}.
>    $$
> 2. **Open circuit at the load** → input impedance equivalent to a capacitor:
>    $$
>    Z_\text{in}^{(\text{oc})} = \frac{1}{j\omega C_\text{eq}}, \quad C_\text{eq} = 40\ \text{pF}.
>    $$
>
> **Find:**
> - (a) The characteristic impedance $Z_0$  
> - (b) The phase velocity $u_p$  
> - (c) The relative permittivity $\varepsilon_r$ of the insulating material.

---

## Theory Recap  

For a **lossless TEM line** (Ulaby):

- Short-circuited input impedance:
  $$
  Z_\text{in}^{(\text{sc})} = jZ_0\tan(\beta\ell).
  $$
- Open-circuited input impedance:
  $$
  Z_\text{in}^{(\text{oc})} = \frac{Z_0}{j\tan(\beta\ell)}.
  $$

- Their **product**:
  $$
  Z_\text{in}^{(\text{sc})}Z_\text{in}^{(\text{oc})} = Z_0^2.
  $$

- If the same line behaves like an inductor and capacitor, we can write:
  $$
  Z_\text{in}^{(\text{sc})} = j\omega L_\text{eq},\quad
  Z_\text{in}^{(\text{oc})} = \frac{1}{j\omega C_\text{eq}}.
  $$

So:
$$
Z_0 = \sqrt{Z_\text{in}^{(\text{sc})}Z_\text{in}^{(\text{oc})}}
    = \sqrt{\frac{L_\text{eq}}{C_\text{eq}}}.
$$

For a TEM line:
$$
u_p = \frac{\omega}{\beta},
\qquad \beta\ell = \arctan(\omega\sqrt{L_\text{eq}C_\text{eq}})
\quad (\text{see derivation below}),
$$
and the velocity is related to the medium:
$$
u_p = \frac{c_0}{\sqrt{\varepsilon_r\mu_r}}.
$$

---

## Geometry / Setup  

- Single uniform TL of length $\ell$ with same parameters in both measurements.  
- **Same frequency**, different load conditions (short / open) → enables elimination of $\beta\ell$ in one step and its recovery from a ratio in another step.  
- Because the line is TEM, $u_p$ relates directly to $\varepsilon_r$.

---

## Derivation  

### (a) Characteristic impedance $Z_0$

Start from:
$$
Z_\text{in}^{(\text{sc})} = j\omega L_\text{eq},
\qquad
Z_\text{in}^{(\text{oc})} = \frac{1}{j\omega C_\text{eq}}.
$$

Product:
$$
Z_\text{in}^{(\text{sc})}Z_\text{in}^{(\text{oc})}
= j\omega L_\text{eq}\cdot \frac{1}{j\omega C_\text{eq}}
= \frac{L_\text{eq}}{C_\text{eq}}.
$$

From TL theory:
$$
Z_0^2 = Z_\text{in}^{(\text{sc})}Z_\text{in}^{(\text{oc})}
\Rightarrow
Z_0 = \sqrt{\frac{L_\text{eq}}{C_\text{eq}}}.
$$

Insert numeric values:
- $L_\text{eq} = 0.064\ \mu\text{H} = 0.064\times 10^{-6}\ \text{H}$  
- $C_\text{eq} = 40\ \text{pF} = 40\times 10^{-12}\ \text{F}$  

Ratio:
$$
\frac{L_\text{eq}}{C_\text{eq}}
= \frac{0.064\times 10^{-6}}{40\times 10^{-12}}
= 1.6\times 10^3.
$$

Therefore:
$$
Z_0 = \sqrt{1.6\times 10^3} \approx 40\ \Omega.
$$

Matches the official solution. :contentReference[oaicite:2]{index=2}  

---

### (b) Phase velocity $u_p$

We first extract $\beta\ell$ from the **ratio** of input impedances.

From TL formulas:
$$
Z_\text{in}^{(\text{sc})}
= jZ_0\tan(\beta\ell),
\qquad
Z_\text{in}^{(\text{oc})}
= \frac{Z_0}{j\tan(\beta\ell)}.
$$

Take the ratio:
$$
\frac{Z_\text{in}^{(\text{sc})}}{Z_\text{in}^{(\text{oc})}}
= -\tan^2(\beta\ell).
$$

From equivalent inductor/capacitor models:
$$
\frac{Z_\text{in}^{(\text{sc})}}{Z_\text{in}^{(\text{oc})}}
= \frac{j\omega L_\text{eq}}{(1/(j\omega C_\text{eq}))}
= -\omega^2 L_\text{eq}C_\text{eq}.
$$

Equate:
$$
-\tan^2(\beta\ell) = -\omega^2 L_\text{eq}C_\text{eq}
\Rightarrow
\tan(\beta\ell) = \omega\sqrt{L_\text{eq}C_\text{eq}}.
$$

Therefore:
$$
\beta\ell = \arctan\left(\omega\sqrt{L_\text{eq}C_\text{eq}}\right).
$$

Then:
$$
\beta = \frac{1}{\ell}\arctan\left(\omega\sqrt{L_\text{eq}C_\text{eq}}\right),
\qquad
u_p = \frac{\omega}{\beta} 
= \frac{\omega\ell}{\arctan\left(\omega\sqrt{L_\text{eq}C_\text{eq}}\right)}.
$$

Given:
- $\ell = 36\ \text{cm} = 0.36\ \text{m}$  
- $f = 1\ \text{MHz}$ → $\omega = 2\pi f = 2\pi\times 10^6\ \text{rad/s}$  

Compute numerically (as in the official solution):
$$
u_p \approx 2.25\times 10^8\ \text{m/s}.
$$

---

### (c) Relative permittivity $\varepsilon_r$

Since the line is **TEM** and the dielectric is **non-magnetic** ($\mu_r = 1$):
$$
u_p = \frac{c_0}{\sqrt{\varepsilon_r\mu_r}}
= \frac{c_0}{\sqrt{\varepsilon_r}}.
$$

Solve for $\varepsilon_r$:
$$
\varepsilon_r = \left(\frac{c_0}{u_p}\right)^2.
$$

With $u_p \approx 2.25\times 10^8\ \text{m/s}$:
$$
\varepsilon_r = \left(\frac{3.0\times 10^8}{2.25\times 10^8}\right)^2
\approx (1.333\ldots)^2
\approx 1.78.
$$

Matches official solution. :contentReference[oaicite:3]{index=3}  

---

## Final Boxed Results  

(a) Characteristic impedance:
$$
\boxed{Z_0 = \sqrt{\frac{L_\text{eq}}{C_\text{eq}}} = 40\ \Omega}
$$

(b) Phase velocity:
$$
\boxed{
u_p = \frac{\omega\ell}{\arctan\left(\omega\sqrt{L_\text{eq}C_\text{eq}}\right)}
\approx 2.25\times 10^8\ \text{m/s}
}
$$

(c) Relative permittivity:
$$
\boxed{
\varepsilon_r = \left(\frac{c_0}{u_p}\right)^2 \approx 1.78
}
$$

---

## Notes  

- Very exam-relevant pattern: **use short/open measurements to back out $Z_0$, $u_p$, and material constants**.  
- The trick is:
  - Product of impedances → $Z_0^2$  
  - Ratio of impedances → $\tan^2(\beta\ell)$ → $\beta$ → $u_p$  
- Once $u_p$ is known for a TEM line, **$\varepsilon_r$ falls out immediately**.

---

## MATLAB — Exercise 5.2 (verification)

> [!code]- MATLAB — Exercise 5.2  
c0   = 3e8;
f    = 1e6;
w    = 2*pi*f;
L_eq = 0.064e-6;   % H
C_eq = 40e-12;     % F
ell  = 0.36;       % m

% (a) Z0
Z0 = sqrt(L_eq/C_eq);

% (b) phase velocity
beta_l = atan(w*sqrt(L_eq*C_eq));
up     = w*ell/beta_l;

% (c) epsilon_r
eps_r = (c0/up)^2;

fprintf('Z0     = %.2f Ohm\n', Z0);
fprintf('u_p    = %.3e m/s\n', up);
fprintf('eps_r  = %.3f\n', eps_r);

