> Quick refs: [[Courses/Electromagnetics/Formulas/Transmission Lines]], [[Courses/Electromagnetics/Formulas/Plane Waves & Power — Quick Formula Sheet]]  
Source PDF: Exercises 6 — Transmission Lines: Power Flow :contentReference[oaicite:0]{index=0}  

# 30035 — **Exercise Set 6**  
## Transmission Lines: Power Flow

---

# Exercise 6.1 — Power Delivered to a Matched Load  

### Problem  

> A lossless transmission line is terminated in a **matched load**:  
> $$
> Z_L = Z_0 \quad\Rightarrow\quad \Gamma_L = 0.
> $$
>  
> **Question:**  
> What fraction of the **incident power** is delivered to the load?  
>  
> Use Ulaby eq. (2.104) and (2.106) as reference.

---

### Theory recap  

For a lossless TL, time-average power delivered to the load is (Ulaby, power relations):
- Incident power: $P_\text{inc}$  
- Reflected power: $P_\text{ref} = |\Gamma_L|^2 P_\text{inc}$  
- Delivered power:
  $$
  P_L = P_\text{inc} - P_\text{ref}
      = \left(1 - |\Gamma_L|^2\right) P_\text{inc}.
  $$

For a matched load:
$$
Z_L = Z_0 \quad\Rightarrow\quad \Gamma_L = 0.
$$  

---

### Derivation  

For $Z_L = Z_0$:
$$
\Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0} = 0.
$$  

Therefore:
$$
P_\text{ref} = |\Gamma_L|^2 P_\text{inc} = 0,
$$
and
$$
P_L = (1 - |\Gamma_L|^2) P_\text{inc} = (1 - 0)P_\text{inc} = P_\text{inc}.
$$

So **all** incident power is delivered to the load.

---

### Final boxed result  

$$
\boxed{\text{Fraction of incident power delivered for a matched load: } \frac{P_L}{P_\text{inc}} = 1 \quad (100\%).}
$$

---

### Notes  

- A matched load has no reflections ($\Gamma = 0$), so the line “looks infinite” to the source.  
- Very common exam statement: **“Matched load ⇒ all power delivered, no standing waves (SWR = 1)”**.  
- Matches the official solution statement: *“For a matched load, $|\Gamma|=0$ … 100% of the incident power is delivered to the load.”* :contentReference[oaicite:1]{index=1}  

---

### MATLAB — Exercise 6.1 (verification)  

> [!code]- MATLAB — Exercise 6.1  
Pin  = 1;         % 1 W incident, arbitrary scale
Gamma = 0;        % matched load
Pref = abs(Gamma)^2 * Pin;
Pdel = (1 - abs(Gamma)^2) * Pin;

fprintf('P_ref / P_inc = %.2f\n', Pref/Pin);
fprintf('P_del / P_inc = %.2f\n', Pdel/Pin);

---

# Exercise 6.2 — Average Power Delivered to a Reactive Load  

### Problem  

> A **lossless transmission line** is terminated in a **purely reactive load** (i.e. $Z_L = jX$, no real part).  
>  
> **Question:**  
> What is the **time-average power** delivered by the TL to this reactive load?  
>  
> Use Ulaby eq. (2.100) as reference.

---

### Theory recap  

For a purely reactive load:
- Load impedance: $Z_L = jX$ (with $X \in \mathbb{R}$)  
- No real part → no dissipation → the load **stores and returns** energy each cycle.

Reflection coefficient magnitude:
$$
|\Gamma_L| = 1
$$
for any purely reactive load on a **lossless** line.

From power relations:
$$
P_L = (1 - |\Gamma_L|^2) P_\text{inc}.
$$  

---

### Derivation  

For $Z_L = jX$ on a lossless TL:

1. Show that $|\Gamma_L| = 1$  
   $$
   \Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}
   = \frac{jX - Z_0}{jX + Z_0}.
   $$
   Numerator and denominator are complex conjugates up to a sign in the real part, leading to  
   $|\Gamma_L| = 1$ (as given in the official solution). :contentReference[oaicite:2]{index=2}  

2. Average power:
   $$
   P_L = (1 - |\Gamma_L|^2) P_\text{inc}
       = (1 - 1)P_\text{inc}
       = 0.
   $$  

So no **net** power is delivered; energy just sloshes back and forth between line and load.

---

### Final boxed result  

$$
\boxed{\text{For a purely reactive load on a lossless TL: } P_L = 0.}
$$

---

### Notes  

- Instantaneous power is **non-zero** and oscillatory, but its **average over one period** is zero.  
- This is conceptually the same as an ideal capacitor or inductor in AC: they store and release energy but do not dissipate it.  
- Matches the official solution: *“A reactive load has $|\Gamma|=1$… no average power is delivered to it.”* :contentReference[oaicite:3]{index=3}  

---

### MATLAB — Exercise 6.2 (verification)  

> [!code]- MATLAB — Exercise 6.2  
Pin   = 1;      % incident power (arbitrary)
Gamma = 1;      % pure reactive load

Pdel = (1 - abs(Gamma)^2) * Pin;

fprintf('Average delivered power P_L = %.2f (should be 0)\n', Pdel);

---

# Exercise 6.3 — Power Flow on a Mismatched, Lossless TL  

### Problem  

> A generator with **open-circuit phasor voltage**  
> $$
> \tilde U_g = 300\ \text{V}
> $$
> and internal impedance  
> $$
> Z_g = 50\ \Omega
> $$
> is connected to a load  
> $$
> Z_L = 75\ \Omega
> $$
> through a **lossless** transmission line of  
> $$
> Z_0 = 50\ \Omega,\qquad \ell = 0.15\lambda.
> $$
>
> (a) Draw the equivalent TL circuit.  
> (b) Compute the **time-average available power** of the generator.  
> (c) Compute the **time-average power reflected** at the load and determine how much of the available power is actually **delivered** to the load.  

The official solution gives (with one small typo we will correct):
- $P_g = 225\ \text{W}$ (available power to a matched load, not 478 W)  
- Reflection coefficient $|\Gamma_L| = 0.2$  
- Delivered power: $P_L = 0.96P_g = 216\ \text{W}$. :contentReference[oaicite:4]{index=4}  

---

## Theory recap  

Key relations:

1. **Available power from a Thevenin source**  
   With open-circuit phasor voltage $\tilde U_g$ and internal resistance $R_g$:
   - Maximum average power when the load is matched ($Z_L = R_g$ real):
     $$
     P_{g,\text{avail}} = \frac{|\tilde U_g|^2}{8R_g}.
     $$
   - This is the power delivered to the matched load (and into a matched line).

2. **Reflection at the load**  
   For mismatch between $Z_L$ and $Z_0$:
   $$
   \Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}.
   $$

3. **Power reflection and delivery** (lossless line $\alpha = 0$)
   - Reflected power:
     $$
     P_\text{ref} = |\Gamma_L|^2 P_\text{inc}.
     $$
   - Delivered power:
     $$
     P_L = (1 - |\Gamma_L|^2) P_\text{inc}.
     $$
   If the generator is matched to the line, its available power $P_g$ is fully launched into the line, i.e. $P_\text{inc} = P_g$.

4. **Length of a lossless TL**  
   For power balance on a lossless line, the length $\ell$ does **not** alter total delivered power (only phases), so the factor $e^{-2\alpha \ell} = 1$.

---

## Geometry / setup  

- Generator: Thevenin source $\tilde U_g$, series $Z_g=50\ \Omega$.  
- Transmission line: $Z_0 = 50\ \Omega$, lossless, $\ell = 0.15\lambda$.  
- Load: $Z_L = 75\ \Omega$.  
- Because $Z_g = Z_0$ (both 50 Ω), the generator is **matched to the line**. So all available power $P_g$ is launched into the line (no reflection at the source). The only reflection occurs at the **load** due to mismatch $Z_L \neq Z_0$.

---

## Derivation  

### (a) Circuit  

You can represent the system as:

- Thevenin generator: $\tilde U_g = 300\ \text{V}$, $Z_g = 50\ \Omega$  
- Connected to a lossless TL: $Z_0 = 50\ \Omega$, length $0.15\lambda$  
- Terminated in $Z_L = 75\ \Omega$.  

This is exactly the diagram drawn in the solution sheet (with nodes A, B along the line). :contentReference[oaicite:5]{index=5}  

---

### (b) Time-average available power of the generator  

Available power is the power delivered when the generator sees a **matched load** equal to its internal resistance ($R_g = 50\ \Omega$).

For a Thevenin source with open-circuit phasor voltage $\tilde U_g$:

$$
P_g = \frac{|\tilde U_g|^2}{8R_g}.
$$

Given $\tilde U_g = 300\ \text{V}$ and $R_g = 50\ \Omega$:

$$
P_g = \frac{300^2}{8\cdot 50}
    = \frac{90\,000}{400}
    = 225\ \text{W}.
$$

This is the **available power**. The official PDF writes $478\ \text{W}$ in one line, but then uses $P_L = 0.96P_g = 216\ \text{W}$, which is **consistent with $P_g = 225\ \text{W}$** and not 478 W. So 478 W is clearly a typo. :contentReference[oaicite:6]{index=6}  

Since $Z_g=Z_0=50\ \Omega$, the generator is matched to the line, so:
$$
P_\text{inc} = P_g = 225\ \text{W}.
$$

---

### (c) Reflected and delivered power at the load  

1. **Reflection coefficient at the load**:

   $$
   \Gamma_L = \frac{Z_L - Z_0}{Z_L + Z_0}
            = \frac{75 - 50}{75 + 50}
            = \frac{25}{125}
            = 0.2.
   $$

   So:
   $$
   |\Gamma_L| = 0.2,\quad |\Gamma_L|^2 = 0.04.
   $$

2. **Reflected power** at the load:
   $$
   P_\text{ref} = |\Gamma_L|^2 P_\text{inc}
                = 0.04\cdot 225
                = 9\ \text{W}.
   $$

3. **Delivered power** to the load:

   For a **lossless** TL ($\alpha = 0$):

   $$
   P_L = (1 - |\Gamma_L|^2) e^{-2\alpha\ell} P_\text{inc}
       = (1 - 0.04)\cdot 1\cdot 225
       = 0.96\cdot 225
       = 216\ \text{W}.
   $$

These match the intended numbers in the official solution (216 W delivered, 4% reflected). :contentReference[oaicite:7]{index=7}  

---

## Final boxed results  

Available generator power:
$$
\boxed{P_g = 225\ \text{W} \quad \text{(available power, all incident on line since }Z_g = Z_0).}
$$

Reflected power:
$$
\boxed{P_\text{ref} = |\Gamma_L|^2 P_g = 0.04\cdot 225 = 9\ \text{W}.}
$$

Delivered power:
$$
\boxed{P_L = (1 - |\Gamma_L|^2)P_g = 0.96\cdot 225 = 216\ \text{W}.}
$$

Reflection coefficient:
$$
\boxed{\Gamma_L = 0.2.}
$$

---

## Notes  

- **Generator–line matching** ($Z_g = Z_0$) means all available power from the source is launched into the line.  
- **Load mismatch** ($Z_L \neq Z_0$) causes power reflection at the load only.  
- The official sheet’s intermediate $P_g = 478\ \text{W}$ is inconsistent with its later use of $P_L = 0.96P_g = 216\ \text{W}$. The latter is correct for $P_g = 225\ \text{W}$, so we treat 478 W as a typo and use the physically consistent 225 W.  
- This exercise illustrates a standard **power-budget** pattern:
  $$
  P_g \xrightarrow[\text{lossless line}]{} P_\text{inc}
  \xrightarrow[\Gamma_L]{} 
  \begin{cases}
  P_\text{ref} = |\Gamma_L|^2 P_\text{inc}\\[4pt]
  P_L   = (1-|\Gamma_L|^2)P_\text{inc}
  \end{cases}
  $$

---

## MATLAB — Exercise 6.3 (verification)  

> [!code]- MATLAB — Exercise 6.3  
Ug = 300;          % Thevenin open-circuit voltage (phasor magnitude)
Rg = 50;          % internal resistance
Z0 = 50;          % line impedance
ZL = 75;          % load

% (b) Available power from source
Pg = Ug^2 / (8*Rg);    % W

% Because Rg = Z0, all available power enters the line:
Pinc = Pg;

% (c) Reflection at the load
GammaL = (ZL - Z0)/(ZL + Z0);
Pref = abs(GammaL)^2 * Pinc;
PL   = (1 - abs(GammaL)^2) * Pinc;

fprintf('Pg   = %.2f W\n', Pg);
fprintf('Gamma_L = %.3f\n', GammaL);
fprintf('Pref = %.2f W\n', Pref);
fprintf('PL   = %.2f W\n', PL);

