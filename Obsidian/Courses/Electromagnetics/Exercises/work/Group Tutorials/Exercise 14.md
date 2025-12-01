> Quick refs: [[Courses/Electromagnetics/Formulas/Plane Waves & Power — Quick Formula Sheet]]

---

# 14 — Plane Waves: Electromagnetic Power Density

---

## Exercise 14.1  
### Time-Average Power Density from $H$ in Air

> **Problem (rephrased)**  
> The magnetic field of a uniform plane wave travelling in air is  
> $$
> \mathbf{H}(y,t)
> = 50~\frac{\text{mA}}{\text{m}}
> \,\sin\!\big(2\pi\cdot 10~\text{MHz}\, t - k y\big)\,\hat{\mathbf{x}}.
> $$
> Assume $k>0$ and propagation in a homogeneous, lossless medium (air).  
>  
> **Find** the **time-average power density** carried by the wave (magnitude and direction).

---

### Theory recap  

- Time-harmonic plane wave fields (phasor form):
  $$
  \mathbf{E}(\mathbf{r},t) = \Re\{\tilde{\mathbf{E}}(\mathbf{r}) e^{j\omega t}\},\quad
  \mathbf{H}(\mathbf{r},t) = \Re\{\tilde{\mathbf{H}}(\mathbf{r}) e^{j\omega t}\}.
  $$
- Time-average Poynting vector (power density) for a time-harmonic field:
  $$
  \mathbf{S}_{\text{av}} 
  = \frac{1}{2}\Re\{\tilde{\mathbf{E}}\times\tilde{\mathbf{H}}^{\!*}\}
  \quad [\text{W/m}^2].
  $$
- For a uniform plane wave in a simple medium, the intrinsic impedance is
  $$
  \eta = \sqrt{\frac{\mu}{\varepsilon}},
  $$
  and the fields satisfy
  $$
  \tilde{\mathbf{E}} = -\,\eta\,\hat{\boldsymbol{\beta}}\times\tilde{\mathbf{H}},
  $$
  where $\hat{\boldsymbol{\beta}}$ is the propagation direction (unit vector).  
- In terms of $\tilde{\mathbf{H}}$ only:
  $$
  \mathbf{S}_{\text{av}} 
  = \frac{1}{2}|\tilde{\mathbf{H}}|^2\,\Re\{\eta\}\,\hat{\boldsymbol{\beta}}
  \quad\text{(lossless medium, $\eta$ real).}
  $$:contentReference[oaicite:0]{index=0}  

For air (approximated as free space):
$$
\eta_{\text{air}} \approx \eta_0 = 120\pi~\Omega \approx 377~\Omega.
$$

---

### Geometry / setup  

- The argument of the sine is $2\pi f t - k y$, i.e. $\omega t - \beta y$.
  - This corresponds to a wave propagating in the **$+y$-direction**.
  - Hence $\hat{\boldsymbol{\beta}} = \hat{\mathbf{y}}$.
- Magnetic field is polarized along $\hat{\mathbf{x}}$:
  $$
  H_0 = 50~\frac{\text{mA}}{\text{m}} = 0.05~\frac{\text{A}}{\text{m}},
  \quad
  \mathbf{H} = H_0 \sin(\omega t - \beta y)\,\hat{\mathbf{x}}.
  $$

Phasor representation (note: $\sin$ corresponds to a $\pm j$ factor vs. cosine convention):
$$
\tilde{\mathbf{H}}(y)
= -j H_0 e^{-j\beta y}\,\hat{\mathbf{x}}.
$$:contentReference[oaicite:1]{index=1}  

Magnitude:
$$
|\tilde{\mathbf{H}}| = H_0 = 0.05~\frac{\text{A}}{\text{m}}.
$$

---

### Derivation  

Use
$$
\mathbf{S}_{\text{av}} 
= \frac{1}{2}|\tilde{\mathbf{H}}|^2\,\eta_{\text{air}}\;\hat{\boldsymbol{\beta}}
\quad(\text{lossless, real } \eta).
$$

1. Magnitude of $\tilde{\mathbf{H}}$:
   $$
   |\tilde{\mathbf{H}}|^2 = H_0^2
   = (0.05)^2 = 2.5\times 10^{-3}~\frac{\text{A}^2}{\text{m}^2}.
   $$
2. Use $\eta_{\text{air}} \approx 377~\Omega$:
   $$
   |\mathbf{S}_{\text{av}}|
   = \frac{1}{2} H_0^2 \eta_{\text{air}}
   = \frac{1}{2}\,(2.5\times 10^{-3})\cdot 377
   \approx 0.471~\frac{\text{W}}{\text{m}^2}.
   $$
3. Direction is $\hat{\boldsymbol{\beta}} = \hat{\mathbf{y}}$.

Thus:
$$
\mathbf{S}_{\text{av}}
\approx 0.471~\frac{\text{W}}{\text{m}^2}\,\hat{\mathbf{y}}.
$$:contentReference[oaicite:2]{index=2}  

---

### Final boxed result  

$$
\boxed{
\mathbf{S}_{\text{av}}
\approx 0.471~\frac{\text{W}}{\text{m}^2}\,\hat{\mathbf{y}}
}
$$

---

### Notes  

- Classic pattern: given $H$-field of a plane wave in a **simple medium**, compute time-average power via $|\tilde{\mathbf{H}}|^2$ and $\eta$.  
- Very typical exam step:  
  - Identify propagation direction from $\omega t - \beta y$ or $\omega t - \boldsymbol{\beta}\cdot\mathbf{r}$.  
  - Use $\mathbf{S}_{\text{av}} = \tfrac{1}{2}|\tilde{\mathbf{H}}|^2\eta\,\hat{\boldsymbol{\beta}}$.  
- **Match check:** numerical result and direction agree with the official solution (same $0.471~\text{W/m}^2$ along $+\hat{\mathbf{y}}$).:contentReference[oaicite:3]{index=3}  

---

### MATLAB — Exercise 14.1 (verification)

> [!code]- MATLAB — Exercise 14.1 (verification)  
> % Plane wave power density from H-field in air
> 
> % PARAMETERS (make these editable for reuse)
> H0_mA_per_m = 50;          % magnetic field amplitude [mA/m]
> eta_air      = 120*pi;     % intrinsic impedance of air ~ 377 ohm
> 
> % CONVERSIONS
> H0 = H0_mA_per_m*1e-3;     % [A/m]
> 
> % TIME-AVERAGE POWER DENSITY
> S_av_mag = 0.5 * H0.^2 * eta_air;   % [W/m^2]
> S_av_vec = [0; S_av_mag; 0];        % along +y (propagation direction)
> 
> fprintf('Exercise 14.1: S_av = %.3f W/m^2 in +y-direction\n', S_av_mag);

---

## Exercise 14.2  
### Phase Velocity from $E$ and Average Power Density

> **Problem (rephrased)**  
> A uniform plane wave propagates in a **lossless, non-magnetic** medium ($\mu_r=1$).  
> - Electric field amplitude: $|E| = 24.56~\text{V/m}$  
> - Average power density magnitude: $|\mathbf{S}_{\text{av}}| = 2.4~\text{W/m}^2$  
>
> **Find** the **phase velocity** $u_p$ of the wave in this medium.

---

### Theory recap  

- For a uniform plane wave in a general (possibly lossy) medium, average power density in terms of $\tilde{\mathbf{E}}$ is
  $$
  \mathbf{S}_{\text{av}} 
  = \frac{1}{2}|\tilde{\mathbf{E}}|^2\Re\left\{\frac{1}{\eta^\ast}\right\}\hat{\boldsymbol{\beta}}.
  $$  
- In a **lossless** medium, $\eta$ is real, so $\eta^\ast=\eta$ and
  $$
  |\mathbf{S}_{\text{av}}|
  = \frac{1}{2}\frac{|\tilde{\mathbf{E}}|^2}{\eta}.
  $$
- Intrinsic impedance in a simple, lossless medium:
  $$
  \eta = \sqrt{\frac{\mu_0\mu_r}{\varepsilon_0\varepsilon_r}}.
  $$
- Phase velocity:
  $$
  u_p = \frac{1}{\sqrt{\mu_0\mu_r\varepsilon_0\varepsilon_r}}
  = \frac{\eta}{\mu_0\mu_r}.
  $$:contentReference[oaicite:5]{index=5}  

Since $\mu_r=1$, this simplifies to $u_p = \eta/\mu_0$.

---

### Geometry / setup  

- Medium is non-magnetic: $\mu_r=1$.
- Lossless: $\eta$ is real.
- Only magnitudes of $E$ and $\mathbf{S}_{\text{av}}$ are needed; propagation direction does not affect $u_p$.

Given:
$$
|\tilde{\mathbf{E}}| = E_0 = 24.56~\text{V/m},\quad
|\mathbf{S}_{\text{av}}| = S_0 = 2.4~\text{W/m}^2.
$$

---

### Derivation  

1. From the power density relation in a lossless medium:
   $$
   S_0 = \frac{1}{2}\frac{E_0^2}{\eta}
   \quad\Rightarrow\quad
   \eta = \frac{E_0^2}{2 S_0}.
   $$
2. Once $\eta$ is known, use
   $$
   u_p = \frac{\eta}{\mu_0}.
   $$
   (Here $\mu_r=1$.)

Numerically:

- Compute $\eta$:
  $$
  \eta = \frac{(24.56)^2}{2\cdot 2.4}~\Omega
  \approx \frac{603}{4.8}~\Omega
  \approx 126~\Omega.
  $$
  (Exact arithmetic + rounding in the official solution yields a consistent value.):contentReference[oaicite:6]{index=6}  
- Then
  $$
  u_p = \frac{\eta}{\mu_0}
  \approx \frac{126}{4\pi\times 10^{-7}}~\text{m/s}
  \approx 1.0\times 10^8~\text{m/s},
  $$
  taking into account rounding consistent with the given data and official solution.:contentReference[oaicite:7]{index=7}  

---

### Final boxed result  

$$
\boxed{
u_p \approx 1.0\times 10^8~\text{m/s}
}
$$

---

### Notes  

- Key pattern:  
  - From $E_0$ and $|\mathbf{S}_{\text{av}}|$ you back out $\eta$ in a lossless medium.  
  - Then convert $\eta \rightarrow \varepsilon_r$ or directly to phase velocity using $u_p = \eta/\mu_0$ (for $\mu_r=1$).  
- Very exam-typical chain:
  $$
  |\mathbf{S}_{\text{av}}|
  \Rightarrow \eta \Rightarrow \varepsilon_r \Rightarrow u_p.
  $$
- **Match check:** The official solution also arrives at $u_p = 1\cdot 10^8~\text{m/s}$ using the same relations.  

---

### MATLAB — Exercise 14.2 (verification)

> [!code]- MATLAB — Exercise 14.2 (verification)  
> % Phase velocity from E amplitude and average power density
> 
> % PARAMETERS (editable)
> E0   = 24.56;          % electric field amplitude [V/m]
> S_av = 2.4;            % average power density [W/m^2]
> mu0  = 4*pi*1e-7;      % [H/m]
> 
> % INTRINSIC IMPEDANCE (lossless medium)
> eta = E0.^2 ./ (2*S_av);   % [ohm]
> 
> % PHASE VELOCITY
> u_p = eta ./ mu0;          % [m/s]
> 
> fprintf('Exercise 14.2:\n');
> fprintf('  eta  = %.3f ohm\n', eta);
> fprintf('  u_p  = %.3e m/s\n', u_p);

---

## Exercise 14.3  
### Power Flow through an Aperture for an Elliptically Polarized Wave

> **Problem (rephrased)**  
> The magnetic field phasor amplitude of an elliptically polarized plane wave in a **lossless, non-magnetic** medium with $\varepsilon_r = 4$ is
> $$
> \tilde{\mathbf{H}}_0
> = 10^{-3}
> \begin{bmatrix}
> 0 \\ 3 \\ j4
> \end{bmatrix}
> ~\frac{\text{A}}{\text{m}}.
> $$
> The wave propagates along the **$+x$-axis**.
>
> (a) Determine the **time-average power** flowing through a flat aperture located in the $yz$-plane with area $A = 20~\text{m}^2$.  
> (b) If the same aperture is oriented such that its normal points in the direction of the vector
> $$
> \begin{bmatrix} 3 \\ 4 \\ 0 \end{bmatrix},
> $$
> how much time-average power flows through it?

---

### Theory recap  

- For a plane wave:
  $$
  \mathbf{S}_{\text{av}}
  = \frac{1}{2}\Re\{\tilde{\mathbf{E}}\times\tilde{\mathbf{H}}^{\!*}\}
  = \frac{1}{2}|\tilde{\mathbf{H}}|^2\Re\{\eta\}\,\hat{\boldsymbol{\beta}}
  \quad(\text{lossless medium}).
  $$  
- Intrinsic impedance in the medium:
  $$
  \eta = \sqrt{\frac{\mu}{\varepsilon}}
  = \sqrt{\frac{\mu_0\mu_r}{\varepsilon_0\varepsilon_r}}.
  $$
- Magnitude of $\tilde{\mathbf{H}}_0$:
  $$
  |\tilde{\mathbf{H}}_0|^2 = |10^{-3}|^2\left(0^2 + 3^2 + 4^2\right)
  = 10^{-6}\cdot 25
  = 2.5\times 10^{-5}~\frac{\text{A}^2}{\text{m}^2}.
  $$:contentReference[oaicite:10]{index=10}  
- Power through an aperture of vector area $\mathbf{A} = A\,\hat{\mathbf{n}}$:
  $$
  P_{\text{av}} = \mathbf{S}_{\text{av}}\cdot\mathbf{A}
  = |\mathbf{S}_{\text{av}}|\,A\,\cos\theta
  $$
  where $\theta$ is the angle between propagation direction $\hat{\boldsymbol{\beta}}$ and the aperture normal $\hat{\mathbf{n}}$.

---

### Geometry / setup  

- Medium: lossless, non-magnetic:
  $$
  \mu_r = 1,\quad \varepsilon_r = 4.
  $$
- Propagation direction: along $+x$, so
  $$
  \hat{\boldsymbol{\beta}} = \hat{\mathbf{x}}.
  $$
- Intrinsic impedance:
  $$
  \eta = \sqrt{\frac{\mu_0}{\varepsilon_0\varepsilon_r}}
  = \frac{120\pi}{\sqrt{\varepsilon_r}}
  = \frac{120\pi}{2}
  \approx 188~\Omega.
  $$  

Apertures:

- (a) Aperture in the **$yz$-plane**:
  - Normal $\hat{\mathbf{n}} = \hat{\mathbf{x}}$.
  - Area vector: $\mathbf{A} = 20~\text{m}^2\,\hat{\mathbf{x}}$.
- (b) Aperture oriented along direction $\mathbf{v} = [3,4,0]^T$:
  - Unit normal:
    $$
    \hat{\mathbf{n}} = \frac{1}{|\mathbf{v}|}\mathbf{v}
    = \frac{1}{5}\begin{bmatrix}3\\4\\0\end{bmatrix}.
    $$  

---

### Derivation  

#### 1) Average power density vector

Magnitude of $\tilde{\mathbf{H}}_0$:
$$
|\tilde{\mathbf{H}}_0|^2
= 2.5\times 10^{-5}~\frac{\text{A}^2}{\text{m}^2}.
$$

Average power density:
$$
|\mathbf{S}_{\text{av}}|
= \frac{1}{2}|\tilde{\mathbf{H}}_0|^2\,\eta
= \frac{1}{2}(2.5\times 10^{-5})\cdot 188
\approx 2.35\times 10^{-3}~\frac{\text{W}}{\text{m}^2}.
$$

Direction is $\hat{\boldsymbol{\beta}} = \hat{\mathbf{x}}$, so
$$
\mathbf{S}_{\text{av}} \approx 2.35\times 10^{-3}~\frac{\text{W}}{\text{m}^2}\,\hat{\mathbf{x}}.
$$  

---

#### (a) Aperture in the $yz$-plane  

Here the aperture normal is $\hat{\mathbf{n}} = \hat{\mathbf{x}}$, so $\theta = 0$ and $\cos\theta = 1$.

Vector area:
$$
\mathbf{A} = 20~\text{m}^2\,\hat{\mathbf{x}}.
$$

Average power:
$$
P_{\text{av},a}
= \mathbf{S}_{\text{av}}\cdot\mathbf{A}
= (2.35\times 10^{-3})\times 20
\approx 4.71\times 10^{-2}~\text{W}
= 47.1~\text{mW}.
$$:contentReference[oaicite:14]{index=14}  

---

#### (b) Aperture normal along $[3,4,0]^T$  

Normal vector:
$$
\hat{\mathbf{n}}
= \frac{1}{5}\begin{bmatrix}3\\4\\0\end{bmatrix}.
$$

Angle with propagation direction:
$$
\cos\theta 
= \hat{\mathbf{x}}\cdot\hat{\mathbf{n}}
= \frac{3}{5}.
$$

Hence
$$
P_{\text{av},b}
= |\mathbf{S}_{\text{av}}|\,(A\,\cos\theta)
= (2.35\times 10^{-3})\cdot 20\cdot\frac{3}{5}
= 47.1\times 10^{-3}\cdot\frac{3}{5}~\text{W}
\approx 2.83\times 10^{-2}~\text{W}
= 28.3~\text{mW}.
$$:contentReference[oaicite:15]{index=15}  

---

### Final boxed results  

(a)  
$$
\boxed{
P_{\text{av},a} \approx 47.1~\text{mW}
}
$$

(b)  
$$
\boxed{
P_{\text{av},b} \approx 28.3~\text{mW}
}
$$

---

### Notes  

- The **polarization** (elliptical) only enters through the magnitude $|\tilde{\mathbf{H}}_0|$; for power calculations in a lossless medium we just need $|\tilde{\mathbf{H}}_0|^2$ and $\eta$.  
- Geometry is key:
  - (a) Normal aligned with propagation direction $\Rightarrow$ full power passes.  
  - (b) Normal tilted: only the component along propagation contributes (cosine factor).  
- Very exam-typical pattern:  
  1. Compute $\eta$ from $(\varepsilon_r,\mu_r)$.  
  2. Compute $|\mathbf{S}_{\text{av}}|$ from $|\tilde{\mathbf{H}}|^2$.  
  3. Project onto an aperture with some orientation using dot products / $\cos\theta$.  
- **Match check:** Both numerical powers (47.1 mW and 28.3 mW) match the official solution exactly.:contentReference[oaicite:16]{index=16}  

---

### MATLAB — Exercise 14.3 (verification)

> [!code]- MATLAB — Exercise 14.3 (verification)  
> % Power through an aperture for an elliptically polarized plane wave
> 
> mu0 = 4*pi*1e-7;   % [H/m]
> eps0 = 8.854e-12;  % [F/m]
> 
> % Medium parameters
> eps_r = 4;         % given
> mu_r  = 1;         % non-magnetic
> 
> % Wave impedance
> eta = sqrt(mu0*mu_r/(eps0*eps_r));   % [ohm]
> 
> % H-field phasor amplitude components (A/m)
> H0_vec = 1e-3 * [0; 3; 1j*4];
> 
> % Magnitude squared of H
> H0_mag2 = real(H0_vec'*conj(H0_vec));  % |H0|^2 [A^2/m^2]
> 
> % Average power density magnitude
> S_av_mag = 0.5 * H0_mag2 * real(eta);  % [W/m^2]
> S_av_vec = [S_av_mag; 0; 0];           % along +x
> 
> % (a) Aperture in yz-plane
> A   = 20;                              % [m^2]
> n_a = [1; 0; 0];                       % normal in +x
> A_a = A * n_a;
> P_a = dot(S_av_vec, A_a);              % [W]
> 
> % (b) Aperture normal along [3;4;0]
> n_b = [3; 4; 0];
> n_b = n_b / norm(n_b);                 % unit normal
> A_b = A * n_b;
> P_b = dot(S_av_vec, A_b);              % [W]
> 
> fprintf('Exercise 14.3:\n');
> fprintf('  |S_av| = %.3e W/m^2\n', S_av_mag);
> fprintf('  P_a    = %.3e W\n', P_a);
> fprintf('  P_b    = %.3e W\n', P_b);
