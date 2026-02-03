# 🎯 EM Exam Navigation

> **Quick Start:** Find your problem type → Go to section → Get formula/method

---

## 🔍 Problem Finder

### What does the problem ask for?

| Looking for... | Jump to |
|----------------|---------|
| **Γ, VSWR, reflected power** | [[#Reflection Coefficient]] |
| **Z_in** (input impedance) | [[#Input Impedance]] |
| **Z_L from Γ at input** | [[#Find Load from Input]] |
| **Z_L from VSWR + position** | [[#VSWR Measurement]] |
| **Stub matching (d, ℓ)** | [[#Stub Matching]] |
| **λ/4 transformer** | [[#Quarter-Wave Transformer]] |
| **Smith chart** | [[#Smith Chart]] |
| **λ in medium** | [[#Wavelength]] |
| **Skin depth δ** | [[#Skin Depth]] |
| **Loss tangent, α, β, η** | [[#Lossy Medium]] |
| **H from E** | [[#H-field from E-field]] |
| **Poynting vector, power** | [[#Poynting Vector]] |
| **Polarization (RHCP/LHCP)** | [[#Polarization]] |
| **Fresnel Γ, τ** | [[#Fresnel Coefficients]] |
| **Brewster/Critical angle** | [[#Special Angles]] |
| **Snell's law θ_t** | [[#Snell's Law]] |
| **Capacitance** | [[#Capacitance]] |
| **Inductance** | [[#Inductance]] |
| **Coulomb force** | [[#Coulomb Force]] |
| **B-field from wire** | [[#Magnetic Field]] |

---

## ⚡ Transmission Lines

### Reflection Coefficient
$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

| Quantity          | Formula |        |          |        |     |
| ----------------- | ------- | ------ | -------- | ------ | --- |
| VSWR              | $(1 +   | \Gamma | ) / (1 - | \Gamma | )$  |
| Power reflected   | $       | \Gamma | ^2$      |        |     |
| Power transmitted | $1 -    | \Gamma | ^2$      |        |     |

**Special cases:**
- Short circuit: $Z_L = 0 \Rightarrow \Gamma = -1$
- Open circuit: $Z_L = \infty \Rightarrow \Gamma = +1$
- Matched: $Z_L = Z_0 \Rightarrow \Gamma = 0$

**MATLAB:** `TLine('Gamma', Z0, ZL)`

---

### Input Impedance
$$Z_{in} = Z_0 \frac{Z_L + jZ_0\tan(\beta\ell)}{Z_0 + jZ_L\tan(\beta\ell)}$$

**Special lengths:**
| Length | Result |
|--------|--------|
| $\ell = \lambda/4$ | $Z_{in} = Z_0^2/Z_L$ |
| $\ell = \lambda/2$ | $Z_{in} = Z_L$ |
| $\ell = \lambda$ | $Z_{in} = Z_L$ |

**MATLAB:** `r = TLine(Z0, ZL, ell_lambda)`

---

### Find Load from Input
**Given:** $\Gamma_{in}$ at input, line length $\ell$
**Find:** $\Gamma_L$ and $Z_L$

$$\Gamma_L = \Gamma_{in} \cdot e^{+j2\beta\ell}$$

Phase shift moving **toward load**: $+2\beta\ell = +4\pi(\ell/\lambda)$

**MATLAB:** `r = TLine('load', Z0, Gamma_in, ell_lambda)`

---

### VSWR Measurement
**Given:** VSWR (or |Γ|), position of V_min or V_max
**Find:** Z_L

**Step 1:** Get |Γ|
$$|\Gamma| = \frac{VSWR - 1}{VSWR + 1}$$

**Step 2:** Get phase from position
- At **V_min**: $\angle\Gamma_L = \pi + 4\pi z_{min}/\lambda$
- At **V_max**: $\angle\Gamma_L = 4\pi z_{max}/\lambda$

**Step 3:** Form $\Gamma_L$ and find $Z_L$
$$Z_L = Z_0 \frac{1 + \Gamma_L}{1 - \Gamma_L}$$

**Python:** `TLine_inverse(Z0, VSWR=..., z_min=...)`

---

### Stub Matching
**Goal:** Match $Z_L$ to $Z_0$ using stub at distance $d$

**MATLAB:** `r = StubMatch(ZL, Z0, 'short', lambda)`

**Output:** 
- $d$ = distance from load to stub [λ]
- $\ell$ = stub length [λ]

> ⚠️ Always two solutions - pick the one **closest to load**

---

### Quarter-Wave Transformer
**Match $Z_L$ to $Z_{in}$ using λ/4 section:**

$$Z_0 = \sqrt{Z_{in} \cdot Z_L}$$

> ⚠️ Only works for **real** load impedances!

---

### Smith Chart

**Normalize:** $z_L = Z_L / Z_0$

**Key points:**
| Point | Location |
|-------|----------|
| Short ($z=0$) | Left edge |
| Open ($z=\infty$) | Right edge |
| Match ($z=1$) | Center |

**Movement:**
- Toward generator → clockwise
- Toward load → counter-clockwise
- Full rotation = λ/2

**Admittance:** Rotate 180° from impedance point

---

## 🌊 Wave Propagation

### Wavelength
$$\lambda = \frac{\lambda_0}{n} = \frac{c_0}{f \cdot \sqrt{\varepsilon_r \mu_r}}$$

**Phase velocity:**
$$u_p = \frac{c_0}{n} = \frac{c_0}{\sqrt{\varepsilon_r \mu_r}}$$

**MATLAB:** `r = Medium(eps_r, f)` → `r.lambda`

---

### Skin Depth
$$\delta = \sqrt{\frac{2}{\omega \mu \sigma}} = \frac{1}{\sqrt{\pi f \mu \sigma}}$$

**Shielding rule:** thickness $> 5\delta$

**MATLAB:** `r = Medium('skin', sigma, f, mu_r)`

---

### Lossy Medium

**Loss tangent:**
$$\tan\delta = \frac{\sigma}{\omega\varepsilon}$$

| tan δ  | Classification  |
| ------ | --------------- |
| < 0.01 | Good dielectric |
| > 100  | Good conductor  |
| else   | Quasi-conductor |

**Complex permittivity:** $\varepsilon_{r,c} = \varepsilon_r' - j\varepsilon_r''$

**Intrinsic impedance:**
$$\eta = \frac{\eta_0}{\sqrt{\varepsilon_{r,c}}} = \frac{377}{\sqrt{\varepsilon_r' - j\varepsilon_r''}}$$

**MATLAB:** `r = Medium(eps_r, sigma, f)`

---

## 📡 Plane Waves

### H-field from E-field
$$\tilde{H} = \frac{1}{\eta}(\hat{k} \times \tilde{E})$$

**MATLAB:** `r = poynting_pw(E_phasor, k_hat, eta)`

---

### Poynting Vector
$$\vec{S}_{avg} = \frac{1}{2}\text{Re}\{\tilde{E} \times \tilde{H}^*\} = \frac{|E|^2}{2\eta}\hat{k}$$

**For lossy medium:** Use $\text{Re}\{\eta\}$
$$S_{avg} = \frac{|E|^2}{2 \cdot \text{Re}\{\eta\}}$$

---

### Power on Surface
$$P = S_{avg} \cdot A \cdot |\cos\theta|$$

where $\cos\theta = \hat{k} \cdot \hat{n}$

**With attenuation:**
$$|E(z)| = |E_0| \cdot e^{-\alpha z}$$

**Python Menu 7 → Option 3** handles this completely!

---

### Frequency from Phase Term

From $e^{-j(\beta_x x + \beta_y y + \beta_z z)}$:

$$|\beta| = \sqrt{\beta_x^2 + \beta_y^2 + \beta_z^2}$$
$$\omega = |\beta| \cdot c_0$$
$$f = \frac{\omega}{2\pi}$$

**Propagation direction:**
$$\hat{k} = \frac{\vec{\beta}}{|\beta|}$$

---

## 🔄 Polarization

### Quick Classification

| Condition      | Type           |     |     |                      |              |
| -------------- | -------------- | --- | --- | -------------------- | ------------ |
| $E_y/E_x$ real | **Linear**     |     |     |                      |              |
| $              | E_x            | =   | E_y | $, phase diff = ±90° | **Circular** |
| Otherwise      | **Elliptical** |     |     |                      |              |
|                |                |     |     |                      |              |

### Handedness (for +z propagation)

| Phase of $E_y$ relative to $E_x$   | Handedness |
| ---------------------------------- | ---------- |
| $E_y$ lags by 90° ($E_y = -jE_x$)  | **RHCP**   |
| $E_y$ leads by 90° ($E_y = +jE_x$) | **LHCP**   |

**MATLAB:** `r = Polarization(E_phasor, k_hat)`

---

## 🪞 Interfaces & Fresnel

### Fresnel Coefficients

**Normal incidence:**
$$\Gamma = \frac{\eta_2 - \eta_1}{\eta_2 + \eta_1} = \frac{n_1 - n_2}{n_1 + n_2}$$
$$\tau = \frac{2\eta_2}{\eta_2 + \eta_1} = \frac{2n_1}{n_1 + n_2}$$

**Power coefficients:**
- $R = |\Gamma|^2$
- $T = 1 - R$

**MATLAB:** `r = Fresnel(eps_r1, eps_r2)`

---

### Special Angles

**Brewster (TM only, zero reflection):**
$$\tan\theta_B = \frac{n_2}{n_1} = \sqrt{\frac{\varepsilon_{r2}}{\varepsilon_{r1}}}$$

**Critical (TIR, requires $n_1 > n_2$):**
$$\sin\theta_c = \frac{n_2}{n_1}$$

**MATLAB:** 
- `Fresnel('brewster', eps_r1, eps_r2)`
- `Fresnel('critical', eps_r1, eps_r2)`

---

### Snell's Law
$$n_1 \sin\theta_i = n_2 \sin\theta_t$$

$$\theta_t = \arcsin\left(\frac{n_1}{n_2}\sin\theta_i\right)$$

**MATLAB:** `r = Fresnel('snell', eps_r1, eps_r2, theta_i)`

---

## ⚡ Electrostatics & Magnetostatics

### Capacitance

| Geometry | Formula |
|----------|---------|
| **Parallel plate** | $C = \varepsilon_0 \varepsilon_r \frac{A}{d}$ |
| **Coaxial** | $C = \frac{2\pi\varepsilon_0\varepsilon_r L}{\ln(b/a)}$ |
| **Parallel wire** | $C = \frac{\pi\varepsilon_0\varepsilon_r L}{\text{acosh}(d/2R)}$ |

**Energy:** $W = \frac{1}{2}CV^2$

---

### Inductance

**Solenoid:**
$$L = \mu_0 \mu_r \frac{N^2 A}{\ell}$$

**From B measurement:**
$$B = \mu_0 \mu_r \frac{N}{\ell} I = \mu_0 \mu_r n I$$

---

### Coulomb Force
$$\vec{F} = \frac{1}{4\pi\varepsilon_0} \frac{q_1 q_2}{r^2} \hat{r}$$

- Same sign → repulsion
- Opposite sign → attraction

**MATLAB:** `[F, F_mag] = coulomb_pair(q1, q2, r1, r2)`

---

### Magnetic Field

**Infinite wire:**
$$B = \frac{\mu_0 \mu_r I}{2\pi r}$$

**Inside conductor:** $B = 0$ at center

**Infinite current sheet:**
$$\vec{H} = \pm\frac{J_s}{2}\hat{n} \times \hat{J}_s$$

---

## 🧮 Constants

| Constant | Value |
|----------|-------|
| $c_0$ | $2.998 \times 10^8$ m/s |
| $\varepsilon_0$ | $8.854 \times 10^{-12}$ F/m |
| $\mu_0$ | $4\pi \times 10^{-7}$ H/m |
| $\eta_0$ | $377$ Ω |

---

## 🛠️ Tool Quick Reference

### MATLAB Helpers
```matlab
TLine(Z0, ZL, ell_lambda)           % Basic TL
TLine('load', Z0, Gamma_in, ell)    % Find ZL from Gamma_in
TLine('Gamma', Z0, ZL)              % Just get Gamma
StubMatch(ZL, Z0, 'short', lambda)  % Stub design
Medium(eps_r, f)                    % Lossless
Medium(eps_r, sigma, f)             % Lossy
Medium('skin', sigma, f)            % Skin depth
Polarization(E_phasor, k_hat)       % Polarization
Fresnel(eps_r1, eps_r2)             % Normal incidence
Fresnel(eps_r1, eps_r2, theta_i)    % Oblique
poynting_pw(E, k_hat, eta)          % Poynting
```

### Python Assistant Menus
| Menu | Topic |
|------|-------|
| 1 | Plane Wave Check |
| 2 | Polarization |
| 3 | Fresnel |
| 4 | Medium Properties |
| 5 | Transmission Lines |
| 6 | Stub Matching |
| **7→3** | **Poynting (scalar mode)** |
| 10 | Inverse TLine (VSWR→ZL) |
| 11 | Geometry (L, C) |

---

## ✅ Exam Checklist

- [ ] MATLAB path set up
- [ ] Python assistant working
- [ ] Constants loaded
- [ ] Test one calculation

**Good luck!** 🍀
