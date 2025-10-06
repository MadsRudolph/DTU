  
### + Ulaby Ch. 7-2 (p. 320 – 323)

---

## 1️⃣ Wave Foundations

### Maxwell’s Equations (phasor form)
$$
\nabla\times\mathbf{E}=-j\omega\mathbf{B},\qquad 
\nabla\times\mathbf{H}=\mathbf{J}+j\omega\mathbf{D}
$$
$$
\nabla\cdot\mathbf{D}=\rho_v,\qquad 
\nabla\cdot\mathbf{B}=0
$$

Constitutive relations:
$$
\mathbf{J}_c=\sigma\mathbf{E},\quad
\mathbf{D}=\varepsilon\mathbf{E},\quad
\mathbf{B}=\mu\mathbf{H}
$$

---

## 2️⃣ Complex Permittivity
For lossy media (Ulaby Eq. 7.4):
$$
\varepsilon_c=\varepsilon-j\frac{\sigma}{\omega}=
\varepsilon' - j\varepsilon'' 
$$
with  
$\varepsilon'=\varepsilon$ and $\varepsilon''=\sigma/\omega$.

- **Lossless medium:**  $\sigma=0\implies\varepsilon_c=\varepsilon$
- **Good conductor:**  $\sigma\gg\omega\varepsilon$

---

## 3️⃣ Wave Equations (Ulaby 7.15–7.16)
Derived from Maxwell’s equations:
$$
\nabla^2\mathbf{E}-\gamma^2\mathbf{E}=0,\qquad
\nabla^2\mathbf{H}-\gamma^2\mathbf{H}=0
$$

Propagation constant:
$$
\boxed{\gamma^2=-\omega^2\mu\varepsilon_c}
\quad\Rightarrow\quad 
\gamma=\alpha+j\beta
$$

- $\alpha$ = attenuation constant [1/m]  
- $\beta$ = phase constant [rad/m]

---

## 4️⃣ Plane-Wave Solutions

### 1-D Form (z-direction)
$$
\mathbf{E}(z)=\mathbf{E}_0 e^{-\gamma z},\qquad
\mathbf{H}(z)=\mathbf{H}_0 e^{-\gamma z}
$$

### 3-D Form (general propagation)
$$
\boxed{
\mathbf{E}(\mathbf{r})=\mathbf{E}_0 e^{-\boldsymbol{\gamma}\cdot\mathbf{r}},\quad
\mathbf{H}(\mathbf{r})=\mathbf{H}_0 e^{-\boldsymbol{\gamma}\cdot\mathbf{r}}
}
$$
with  
$\boldsymbol{\gamma}=\boldsymbol{\alpha}+j\boldsymbol{\beta}$,  
$\mathbf{r}=x\hat{\mathbf{x}}+y\hat{\mathbf{y}}+z\hat{\mathbf{z}}$

**Dispersion relation:**  
$$
\boldsymbol{\gamma}\cdot\boldsymbol{\gamma}
=\gamma_x^2+\gamma_y^2+\gamma_z^2=-\omega^2\mu\varepsilon_c
$$

---

## 5️⃣ Phase Constant, Wavelength & Velocity
From $\beta=|\boldsymbol{\beta}|$:
$$
\lambda=\frac{2\pi}{\beta}
$$
$$
u_p=\frac{\omega}{\beta}=\lambda f
$$
$\hat{\beta}=\boldsymbol{\beta}/|\boldsymbol{\beta}|$ gives the direction of propagation.

---

## 6️⃣ Intrinsic Impedance
Analogous to characteristic impedance of a transmission line:
$$
\boxed{
\eta=\frac{\mathbf{E}}{\mathbf{H}}=
\sqrt{\frac{\mu}{\varepsilon_c}}=
\sqrt{\frac{\mu_0\mu_r}{\varepsilon_0\varepsilon_r+j\frac{\sigma}{\omega}}}
}
$$

- **Free space:** $\varepsilon_r=\mu_r=1$
  $$
  \eta_0=\sqrt{\frac{\mu_0}{\varepsilon_0}}=120\pi\,\Omega\approx377\,\Omega
  $$

---

## 7️⃣ Relationship Between E and H (Plane-Wave Conditions)

From Maxwell’s equations (phasor form):
$$
\boldsymbol{\gamma}\times\mathbf{E}=+j\omega\mu\mathbf{H},\qquad
\boldsymbol{\gamma}\times\mathbf{H}=-j\omega\varepsilon_c\mathbf{E}
$$
and
$$
\boldsymbol{\gamma}\cdot\mathbf{E}=0,\qquad 
\boldsymbol{\gamma}\cdot\mathbf{H}=0
$$

Hence, **E and H are perpendicular to each other and to $\boldsymbol{\gamma}$** → Transverse Electromagnetic (TEM) wave.

---

## 8️⃣ Time Domain ↔ Phasor
$$
\mathbf{E}(\mathbf{r},t)=\Re\{\mathbf{E}_0 e^{-\boldsymbol{\gamma}\cdot\mathbf{r}}e^{j\omega t}\}
=\mathbf{E}_{0r}\cos(\omega t-\boldsymbol{\beta}\cdot\mathbf{r})
-\mathbf{E}_{0i}\sin(\omega t-\boldsymbol{\beta}\cdot\mathbf{r})\,e^{-\boldsymbol{\alpha}\cdot\mathbf{r}}
$$
Same form for $\mathbf{H}(\mathbf{r},t)$.

---

## 9️⃣ Power Flow (Ulaby 7-2.1)

For lossless media ($\sigma=0$):
$$
\boxed{
S=\mathbf{E}\times\mathbf{H}=\frac{|\mathbf{E}_0|^2}{2\eta}\,\hat{\beta}
}
$$
Poynting vector $\mathbf{S}$ represents instantaneous power density (W/m²).  
Average power density:
$$
\langle S\rangle=\frac{1}{2}\Re\{\mathbf{E}\times\mathbf{H}^*\}
$$

---

## 🔟 Example (Ulaby Example 7-1)

For a 1 MHz plane wave in air:
$$
\lambda=\frac{c}{f}=300\,\text{m},\qquad 
k=\frac{2\pi}{\lambda}=\frac{2\pi}{300}
$$
$$
\mathbf{E}(z,t)=\hat{x}\,1.2\pi\cos(2\pi\cdot10^6 t-\tfrac{2\pi z}{300}+\tfrac{\pi}{3})\;\text{mV/m}
$$
$$
\mathbf{H}(z,t)=\hat{y}\frac{\mathbf{E}(z,t)}{\eta_0}
$$
→ $|\eta_0|≈120\pi Ω$

---

## 🔸 Summary Table

| Quantity             | Symbol          | Expression                                                                | Units | Notes                               |
| -------------------- | --------------- | ------------------------------------------------------------------------- | ----- | ----------------------------------- |
| Complex permittivity | $\varepsilon_c$ | $\varepsilon-j\sigma/\omega$                                              | F/m   | Loss effects                        |
| Propagation constant | $\gamma$        | $\alpha+j\beta$                                                           | 1/m   | Attenuation + phase                 |
| Wavelength           | $\lambda$       | $2\pi/\beta$                                                              | m     | Depends on medium                   |
| Phase velocity       | $u_p$           | $\omega/\beta$                                                            | m/s   | $= \lambda f$                       |
| Intrinsic impedance  | $\eta$          | $\sqrt{\mu/\varepsilon_c}$                                                | Ω     | $= 377 Ω$ in vacuum                 |
| E–H relationship     | –               | $\gamma\times H=-j\omega\varepsilon_cE$ and $\gamma\times E=j\omega\mu H$ | –     | Fields ⊥ each other and propagation |

---

## 🧭 Conceptual Takeaways
- Plane waves are the **far-field approximation** of spherical waves.  
- Both **E** and **H** satisfy the same homogeneous wave equation.  
- In a **lossless medium**, waves propagate without attenuation.  
- **Direction:** given by $\boldsymbol{\beta}$; **magnitude:** $\beta=\omega/u_p$.  
- **Power flow:** $\mathbf{S}=\mathbf{E}\times\mathbf{H}$ points along $\hat{\beta}$.  
- **Transmission line analogy:**  
  - $\mu$ ↔ inductance per unit length $L'$  
  - $\varepsilon$ ↔ capacitance per unit length $C'$  
  - $\sigma$ ↔ conductance per unit length $G'$  

---

🔗 **Cross-References**
