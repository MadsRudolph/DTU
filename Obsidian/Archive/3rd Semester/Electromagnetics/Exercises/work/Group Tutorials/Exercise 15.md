> Quick refs: [[Courses/Electromagnetics/Formulas/Current in Conductors & Skin Effect]], [[Courses/Electromagnetics/Formulas/Plane Waves in Lossy Media]]

---

# 15 — Current Flow in Conductors

---

## Exercise 15.1  
### Skin Effect: AC vs DC Resistance of a Thick Copper Block

> **Given**  
> A rectangular **copper** block is excited by a plane wave, inducing a current through its thickness.  
>
> - Thickness (in direction of current flow):  
>   - $t = 60~\text{cm} = 0.60~\text{m}$  
> - Material: copper (Cu)  
>   - $\mu_r = 1$  
>   - $\varepsilon_r = 1$  
>   - $\sigma = 5.8\times 10^7~\text{S/m}$  
> - Frequencies:  
>   - $f_1 = 1~\text{kHz}$  
>   - $f_2 = 10~\text{MHz}$  
>
> **Find**  
> The ratio of **AC resistance** to **DC resistance** of the block at each frequency:
> $$
> \frac{R_\text{ac}}{R_\text{dc}} \quad\text{at } f_1, f_2.
> $$

---

### Theory recap  

For a uniform conductor (length $l$, cross-section dimensions $w\times t$):

- **DC resistance** (current fills full cross-section):
  $$
  R_\text{dc} = \frac{l}{\sigma\,t\,w}.
  $$
- **AC resistance** under skin effect (current confined to a “skin” of thickness $\delta_s$ near the surface).  
  For a **flat conductor** carrying current uniformly across its width $w$, the effective cross-section is $w\delta_s$, so:
  $$
  R_\text{ac} = \frac{l}{\sigma\,\delta_s\,w}.
  $$
- **Ratio**:
  $$
  \frac{R_\text{ac}}{R_\text{dc}}
  = \frac{l/(\sigma\delta_s w)}{l/(\sigma t w)}
  = \frac{t}{\delta_s}.
  $$
- Skin depth in a good conductor (Ulaby, plane waves in conductors):
  - Propagation constant in a good conductor:
    $$
    \alpha \approx \beta \approx \sqrt{\pi f \mu \sigma},
    $$
  - Skin depth:
    $$
    \delta_s = \frac{1}{\alpha}
    \approx \sqrt{\frac{1}{\pi f \mu \sigma}}
    = \sqrt{\frac{2}{\omega\mu\sigma}},
    \quad \omega = 2\pi f.
    $$
- Therefore:
  $$
  \frac{R_\text{ac}}{R_\text{dc}} = \alpha t.
  $$:contentReference[oaicite:0]{index=0}  

Copper with $\sigma\approx 5.8\times 10^7~\text{S/m}$ and $\mu_r\approx 1$ is an **excellent conductor**, so the good-conductor approximations are valid at both 1 kHz and 10 MHz.

---

### Geometry / setup  

- Current direction: along some length $l$ of the block (not specified, but cancels in the ratio).
- Cross section in the plane $\perp$ to current:
  - Width: $w$ (arbitrary; cancels).
  - Thickness (in direction of propagation/current penetration): $t = 0.60~\text{m}$.

Because the ratio $R_\text{ac}/R_\text{dc}$ depends only on $t$ and $\delta_s$, the exact width $w$ and length $l$ are irrelevant.

---

### Derivation  

We proceed frequency by frequency.

Constants:
$$
\mu_0 = 4\pi\times10^{-7}~\text{H/m},\quad
\mu = \mu_0\mu_r = \mu_0,\quad
\sigma = 5.8\times 10^7~\text{S/m}.
$$

#### 1) Skin depth and ratio at $f_1 = 1~\text{kHz}$

Angular frequency:
$$
\omega_1 = 2\pi f_1 = 2\pi\cdot 10^3~\text{rad/s}.
$$

Good-conductor approximation:
$$
\delta_{s1} \approx \sqrt{\frac{2}{\omega_1\mu\sigma}},
\qquad
\alpha_1 = \frac{1}{\delta_{s1}}.
$$

Using the material constants above, one obtains:  
- $\delta_{s1} \approx 2.09\times 10^{-3}~\text{m} = 2.09~\text{mm}$  
  (this matches the full lossy-medium expression used in the official solution) :contentReference[oaicite:1]{index=1}  
- Hence:
  $$
  \frac{R_\text{ac}}{R_\text{dc}}(1~\text{kHz})
  = \frac{t}{\delta_{s1}}
  \approx \frac{0.60}{2.09\times 10^{-3}}
  \approx 2.87\times 10^2
  \approx 287.
  $$:contentReference[oaicite:2]{index=2}  

#### 2) Skin depth and ratio at $f_2 = 10~\text{MHz}$

Angular frequency:
$$
\omega_2 = 2\pi f_2 = 2\pi\cdot 10^7~\text{rad/s}.
$$

Again:
$$
\delta_{s2} \approx \sqrt{\frac{2}{\omega_2\mu\sigma}},
\qquad
\alpha_2 = \frac{1}{\delta_{s2}}.
$$

Numerically:
- $\delta_{s2} \approx 2.09\times 10^{-5}~\text{m} = 20.9~\mu\text{m}$ :contentReference[oaicite:3]{index=3}  
- Then:
  $$
  \frac{R_\text{ac}}{R_\text{dc}}(10~\text{MHz})
  = \frac{t}{\delta_{s2}}
  \approx \frac{0.60}{2.09\times 10^{-5}}
  \approx 2.87\times 10^4
  \approx 2.87\times 10^4.
  $$

The official solution states:
$$
\frac{R_\text{ac}}{R_\text{dc}} = 287\ \text{(1 kHz)},\quad
\frac{R_\text{ac}}{R_\text{dc}} = 28710\ \text{(10 MHz)},
$$
which matches our results up to rounding. :contentReference[oaicite:4]{index=4}  

---

### Final boxed results  

$$
\boxed{
\frac{R_\text{ac}}{R_\text{dc}}(1~\text{kHz}) \approx 2.9\times 10^2 \;\;(\approx 287)
}
$$

$$
\boxed{
\frac{R_\text{ac}}{R_\text{dc}}(10~\text{MHz}) \approx 2.9\times 10^4 \;\;(\approx 2.87\times 10^4)
}
$$

---

### Notes  

- **Key pattern**: For a flat conductor, skin effect effectively reduces the thickness from $t$ to $\delta_s$, so the resistance increases by $t/\delta_s$.
- At high frequency, **AC resistance can be orders of magnitude larger** than DC resistance. That is exactly what you see: from $287$ up to $\sim 2.9\times10^4$.
- The parameter combination $(\mu,\sigma,f)$ controls $\delta_s$; for copper, skin depth is tiny at MHz frequencies.
- **Matches official solution**: same ratios $287$ and $28710$ (up to rounding; note that $28710 \approx 2.87\times10^4$). :contentReference[oaicite:5]{index=5}  

---

### MATLAB — Exercise 15.1 (verification)

> [!code]- MATLAB — Exercise 15.1 (verification)  
> % Exercise 15.1 — AC vs DC resistance of a thick copper block
> clear; clc;
> 
> % Material parameters (copper)
> mu0  = 4*pi*1e-7;       % H/m
> eps0 = 8.854e-12;       % F/m  (not needed here)
> mu_r = 1;
> eps_r = 1;
> sigma = 5.8e7;          % S/m
> 
> mu = mu0*mu_r;
> 
> % Block thickness
> t = 0.60;               % m
> 
> % Frequencies
> f = [1e3, 10e6];        % Hz
> 
> % Good-conductor skin depth and ratio
> for k = 1:numel(f)
>     fk     = f(k);
>     omega  = 2*pi*fk;
>     delta  = sqrt(2./(omega*mu*sigma));   % [m]
>     alpha  = 1./delta;                    % [1/m]
>     RacRdc = alpha * t;                   % ratio = t/delta
> 
>     fprintf('f = %.3e Hz:\n', fk);
>     fprintf('  delta_s = %.3e m\n', delta);
>     fprintf('  R_ac/R_dc = %.3e\n\n', RacRdc);
> end

---

## Exercise 15.2  
### Skin Effect and AC Resistance of a Coaxial Cable

> **Given**  
> A coaxial cable with **copper** conductors:
>
> - Inner conductor radius:  
>   - $a = 0.5~\text{cm} = 5.0\times 10^{-3}~\text{m}$  
> - Outer conductor inner radius:  
>   - $b = 1.0~\text{cm} = 1.0\times 10^{-2}~\text{m}$  
> - Outer conductor thickness:  
>   - $t_\text{outer} = 0.5~\text{mm} = 5.0\times 10^{-4}~\text{m}$  
> - Material (both conductors): copper  
>   - $\sigma = 58~\text{MS/m} = 5.8\times 10^7~\text{S/m}$  
>   - $\mu_r = 1$  
>   - $\varepsilon_r = 1$  
> - Frequency:  
>   - $f = 10~\text{MHz}$ (parts a–c)  
>   - $f = 1~\text{GHz}$ (part d)  
>
> **Tasks**
> - (a) At $10~\text{MHz}$: Are the inner and outer conductors **thick enough** to be treated as *infinitely thick* regarding current flow (skin effect)?  
> - (b) Compute the **surface resistance** $R_s$ at $10~\text{MHz}$.  
> - (c) Compute the **AC resistance per unit length** $R'_\text{ac}$ at $10~\text{MHz}$.  
> - (d) Repeat (b)–(c) for $f = 1~\text{GHz}$.

---

### Theory recap  

1. **Skin depth** in a good conductor:
   $$
   \delta_s = \frac{1}{\alpha}
   \approx \sqrt{\frac{1}{\pi f\mu\sigma}}
   = \sqrt{\frac{2}{\omega\mu\sigma}}.
   $$
2. **Rule-of-thumb** for “infinitely thick” conductors:  
   If the **thickness** of the conductor (in the direction of field penetration) is at least **5–10 times $\delta_s$**, then the field decays strongly before reaching the other side, and we can treat it as “infinitely thick” for AC current distribution.   
3. **Surface resistance** (good conductor, sinusoidal steady-state):
   $$
   R_s = \frac{1}{\sigma\,\delta_s}
   = \sqrt{\frac{\pi f\mu}{\sigma}}.
   $$:contentReference[oaicite:7]{index=7}  
4. **AC resistance per unit length** of a coaxial line (inner radius $a$, outer radius $b$, thick enough conductors):
   - Current flows in a cylindrical shell of thickness $\delta_s$:
     - Inner: effective cross-sectional area $A_i \approx 2\pi a\delta_s$  
     - Outer: $A_o \approx 2\pi b\delta_s$
   - AC resistance per unit length:
     $$
     R'_i = \frac{1}{\sigma A_i} = \frac{R_s}{2\pi a},
     \qquad
     R'_o = \frac{1}{\sigma A_o} = \frac{R_s}{2\pi b},
     $$
     $$
     R'_\text{ac} = R'_i + R'_o
     = \frac{R_s}{2\pi}\left(\frac{1}{a} + \frac{1}{b}\right).
     $$:contentReference[oaicite:8]{index=8}  

These expressions agree with the structure used in the official solution sheet.   

---

### Geometry / setup  

- Coaxial geometry:
  - Inner conductor: solid cylinder of radius $a$.
  - Outer conductor: cylindrical shell with inner radius $b$ and thickness $t_\text{outer}$.
- AC current flows **near the surfaces** (skin effect), so for:
  - inner conductor: region near $r=a$,
  - outer conductor: region near inner surface at $r=b$ (assuming thickness $\gg\delta_s$).

We compare:

- Inner “radial depth” available: $a = 5.0\times 10^{-3}~\text{m}$.
- Outer conductor thickness: $t_\text{outer} = 5.0\times 10^{-4}~\text{m}$.

---

### Derivation  

#### (a) Thickness vs skin depth at $10~\text{MHz}$

Compute skin depth $\delta_s$ in copper at $10~\text{MHz}$.

Using the same material parameters as in 15.1 and the general expression, the official solution gives:
$$
\delta_s(10~\text{MHz}) \approx 20.9~\mu\text{m} = 2.09\times 10^{-5}~\text{m}.
$$:contentReference[oaicite:10]{index=10}  

Now compare:

- Inner conductor “thickness” (radius):  
  $$
  \frac{a}{\delta_s} = \frac{5.0\times 10^{-3}}{2.09\times 10^{-5}} \approx 239.
  $$
- Outer conductor thickness:
  $$
  \frac{t_\text{outer}}{\delta_s} = \frac{5.0\times 10^{-4}}{2.09\times 10^{-5}} \approx 23.9.
  $$:contentReference[oaicite:11]{index=11}  

Both ratios are **$\gg 5$**, so both conductors can safely be considered “infinitely thick” for current distribution.

> Conclusion (a): **Yes**, both inner and outer conductors are sufficiently thick to be treated as infinitely thick at $10~\text{MHz}$.

---

#### (b) Surface resistance $R_s$ at $10~\text{MHz}$

From:
$$
R_s = \frac{1}{\sigma\delta_s}
\quad\text{(good conductor)}.
$$

With $\sigma = 5.8\times 10^7~\text{S/m}$ and $\delta_s(10~\text{MHz}) \approx 2.09\times 10^{-5}~\text{m}$:
$$
R_s(10~\text{MHz})
\approx \frac{1}{(5.8\times 10^7)\,(2.09\times 10^{-5})}
\approx 8.25\times 10^{-4}~\Omega.
$$:contentReference[oaicite:12]{index=12}  

This matches the official solution.

---

#### (c) AC resistance per unit length at $10~\text{MHz}$

Use:
$$
R'_\text{ac}
= \frac{R_s}{2\pi}\left(\frac{1}{a} + \frac{1}{b}\right).
$$

Plug:
- $a = 5.0\times 10^{-3}~\text{m}$,
- $b = 1.0\times 10^{-2}~\text{m}$,
- $R_s = 8.25\times 10^{-4}~\Omega$.

Compute inner and outer contributions:

- Inner conductor:
  $$
  R'_i = \frac{R_s}{2\pi a}
  \approx \frac{8.25\times 10^{-4}}{2\pi\cdot 5.0\times 10^{-3}}
  \approx 2.63\times 10^{-2}~\Omega/\text{m}
  = 26.3~\text{m}\Omega/\text{m}.
  $$
- Outer conductor:
  $$
  R'_o = \frac{R_s}{2\pi b}
  \approx \frac{8.25\times 10^{-4}}{2\pi\cdot 1.0\times 10^{-2}}
  \approx 1.31\times 10^{-2}~\Omega/\text{m}
  = 13.1~\text{m}\Omega/\text{m}.
  $$:contentReference[oaicite:13]{index=13}  

Total:
$$
R'_\text{ac}(10~\text{MHz})
= R'_i + R'_o
\approx (26.3 + 13.1)\,\text{m}\Omega/\text{m}
\approx 39.4~\text{m}\Omega/\text{m}.
$$:contentReference[oaicite:14]{index=14}  

---

#### (d) Repeat for $f = 1~\text{GHz}$

At $f = 1~\text{GHz}$, the same formulas apply.

The official solution (using the general lossy-medium formula) gives: :contentReference[oaicite:15]{index=15}  

- Skin depth:
  $$
  \delta_s(1~\text{GHz}) \approx 2.09~\mu\text{m} = 2.09\times 10^{-6}~\text{m}.
  $$
- Surface resistance:
  $$
  R_s(1~\text{GHz})
  = \frac{1}{\sigma\delta_s}
  \approx 8.25\times 10^{-3}~\Omega
  = 8.25~\text{m}\Omega.
  $$
- AC resistance per unit length:
  $$
  R'_\text{ac}(1~\text{GHz})
  = \frac{R_s}{2\pi}\left(\frac{1}{a} + \frac{1}{b}\right)
  \approx 0.394~\Omega/\text{m}.
  $$

These are exactly the values given in the official sheet. :contentReference[oaicite:16]{index=16}  

---

### Final boxed results  

(a) **Thickness check at $10~\text{MHz}$**:
$$
\boxed{
\frac{a}{\delta_s} \approx 239,\quad
\frac{t_\text{outer}}{\delta_s} \approx 23.9
\;\Rightarrow\;
\text{both conductors can be treated as infinitely thick.}
}
$$

(b) **Surface resistance at $10~\text{MHz}$**:
$$
\boxed{
R_s(10~\text{MHz}) \approx 8.25\times 10^{-4}~\Omega
}
$$

(c) **AC resistance per unit length at $10~\text{MHz}$**:
$$
\boxed{
R'_\text{ac}(10~\text{MHz}) \approx 39.4~\text{m}\Omega/\text{m}
}
$$

(d) **At $1~\text{GHz}$**:
$$
\boxed{
\delta_s(1~\text{GHz}) \approx 2.09~\mu\text{m},\quad
R_s(1~\text{GHz}) \approx 8.25~\text{m}\Omega,\quad
R'_\text{ac}(1~\text{GHz}) \approx 0.394~\Omega/\text{m}
}
$$

---

### Notes  

- The **inner conductor** contributes more to the AC resistance than the outer conductor since it has smaller radius $a$ (higher $1/a$ term).
- As frequency increases:
  - Skin depth shrinks, $\delta_s \propto 1/\sqrt{f}$.
  - Surface resistance grows, $R_s \propto \sqrt{f}$.
  - AC resistance per unit length also grows roughly as $\sqrt{f}$ (for a given geometry).
- The “**infinitely thick**” assumption is really a **geometry vs skin depth** comparison — crucial exam idea.
- **Matches official solution**:
  - Same $\delta_s$, $R_s$ and $R'_\text{ac}$ values at both 10 MHz and 1 GHz. :contentReference[oaicite:17]{index=17}  

---

### MATLAB — Exercise 15.2 (verification)

> [!code]- MATLAB — Exercise 15.2 (verification)  
> % Exercise 15.2 — Skin effect and AC resistance of a coaxial cable
> clear; clc;
> 
> % Material parameters (copper)
> mu0  = 4*pi*1e-7;    % H/m
> eps0 = 8.854e-12;    % F/m (not used directly)
> mu_r = 1;
> eps_r = 1;
> sigma = 5.8e7;       % S/m
> 
> mu = mu0*mu_r;
> 
> % Geometry
> a = 0.005;           % inner conductor radius [m]
> b = 0.010;           % inner radius of outer conductor [m]
> t_outer = 0.0005;    % thickness of outer conductor [m]
> 
> % Frequencies of interest
> f = [10e6, 1e9];     % [Hz]
> 
> for k = 1:numel(f)
>     fk    = f(k);
>     omega = 2*pi*fk;
> 
>     % Good-conductor skin depth
>     delta = sqrt(2./(omega*mu*sigma));   % [m]
> 
>     % Surface resistance
>     Rs = 1./(sigma*delta);               % [ohm]
> 
>     % AC resistance per unit length, assuming "infinite" thickness
>     Ri_prime = Rs./(2*pi*a);             % inner conductor [ohm/m]
>     Ro_prime = Rs./(2*pi*b);             % outer conductor [ohm/m]
>     Rac_prime = Ri_prime + Ro_prime;     % total [ohm/m]
> 
>     fprintf('f = %.3e Hz\n', fk);
>     fprintf('  delta_s   = %.3e m\n', delta);
>     fprintf('  a/delta   = %.3f\n', a./delta);
>     fprintf('  t_outer/d = %.3f\n', t_outer./delta);
>     fprintf('  Rs        = %.3e ohm\n', Rs);
>     fprintf('  R''_ac     = %.3e ohm/m\n\n', Rac_prime);
> end
