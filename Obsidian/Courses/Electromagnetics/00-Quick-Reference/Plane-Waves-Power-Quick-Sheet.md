---
title: "Plane Waves Power Quick Sheet"
type: formula
tags: [electromagnetics, quick-ref]
aliases: []
links: {"formulas": [], "related": []}
updated: "2025-11-05"

---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]
> **Quick refs:** [[MOC – Electromagnetics]] · [[MOC – Plane-Waves]] · [[MOC – Transmission-Lines]] · [[MOC – EM Loss & Skin Depth]]

> For **Electromagnetics (Applied)** — condensed reference of key relationships used in the assignment.  
> Constants: $c=3\times10^8\ \text{m/s}$, $\eta_0=377\ \Omega$, $\mu_0=4\pi\times10^{-7}$, $\epsilon_0=1/(\mu_0 c^2)$.

---

## 🌊 Plane Wave Basics
- Phase constant:  
  $\displaystyle \beta = \omega\sqrt{\mu\epsilon} = k_0\sqrt{\mu_r\epsilon_r}$

- Free-space wavenumber:  
  $\displaystyle k_0 = \frac{2\pi f}{c1}$

- Intrinsic impedance:  
  $\displaystyle \eta = \sqrt{\frac{\mu}{\epsilon}} = \eta_0\sqrt{\frac{\mu_r}{\epsilon_r}}$
- In Vacuum
   $\displaystyle \eta = \sqrt{\frac{\mu}{\epsilon}} =120\ \pi = 377\ \Omega$

- Wave velocity:  
  $\displaystyle v_p = \frac{\omega}{\beta} = \frac{c}{\sqrt{\mu_r\epsilon_r}}$

- Relationship between $\mathbf E$ and $\mathbf H$:  
  $\displaystyle \mathbf H_0 = \frac{1}{\eta}(\hat\beta\times\mathbf E_0)$

- Transverse condition (plane wave):  
  $\mathbf E\perp\mathbf H\perp\hat\beta$

---

## 🔄 Time-Domain Conversion
- From phasor:  
  $\displaystyle \mathbf E(\mathbf r,t) = \Re\{\mathbf E_0 e^{j(\omega t-\vec\beta\cdot\mathbf r)}\}$  
  $\displaystyle \mathbf H(\mathbf r,t) = \Re\{\mathbf H_0 e^{j(\omega t-\vec\beta\cdot\mathbf r)}\}$

- Phase relations:  
  $j$ corresponds to $+90^\circ$ phase shift $\Rightarrow$ cosine → negative sine.

---

## ⚙️ Lossy Media
- Complex permittivity:  
  $\displaystyle \epsilon_c = \epsilon' - j\epsilon'' = \epsilon'(1-j\tan\delta)$

- Loss tangent:  
  $\displaystyle \tan\delta = \frac{\epsilon''}{\epsilon'}$
> [!summary]
> | Type | Range of $\tan(\delta)$ | Remarks |
> |------|--------------------------|----------|
> | Perfect dielectric insulator | $\sigma = 0 \Leftrightarrow \tan(\delta) = 0$ | No loss |
> | Low-loss medium (dielectric) / good insulator | $\tan(\delta) \le 10^{-2}$ | |
> | Quasi-good conductor / quasi-good insulator / semiconductor | $10^{-2} \le \tan(\delta) \le 10^{2}$ | Typical range for many real dielectrics |
> | Good conductor | $\tan(\delta) \ge 10^{2}$ | Loss-dominated |
> | Perfect electric conductor (PEC) | $\rho = 0 \Leftrightarrow \sigma = \infty \Leftrightarrow \tan(\delta) = \infty$ | |
- Attenuation constant (low-loss):  
  $\displaystyle \alpha \approx \frac{k_0\sqrt{\epsilon_r}\tan\delta}{2}$

- Phase constant (approx):  
  $\displaystyle \beta \approx k_0\sqrt{\epsilon_r}$

- Power loss over distance:  
  $\displaystyle \text{Loss}_{dB} = 8.686\,\alpha\,d$

---

## 🧲 Skin Depth & Conductors
- Skin depth:  
  $\displaystyle \delta = \sqrt{\frac{2}{\omega\mu\sigma}}$

- Frequency for given thickness ($\delta=t$):  
  $\displaystyle f = \frac{1}{\pi\mu\sigma t^2}$

---

## ⚡ Polarization
- **Linear:** field oscillates in one fixed direction → $E_y/E_z$ real.  
- **Circular:** two orthogonal equal components in quadrature ($90^\circ$ phase).  
- Handedness: $(\mathbf u\times\mathbf v)\cdot\hat\beta < 0$ → right-hand.  
- Axial ratio:  
  $\displaystyle R = \frac{a}{b}$ (for circular $R=1$, 0 dB)

---

## 💡 Power Flow
- Instantaneous Poynting vector:  
  $\displaystyle \mathbf S = \mathbf E \times \mathbf H$

- Time-average power density:  
  $\displaystyle \langle S \rangle = \frac{1}{2}\Re\{\mathbf E \times \mathbf H^*\}$

- In a uniform plane wave (free space):  
  $\displaystyle \langle S \rangle = \frac{E_0^2}{2\eta_0} = \frac{1}{2}\eta_0 H_0^2$

- Projected power on surface (angle $\theta$):  
  $\displaystyle \langle S_\perp \rangle = \langle S \rangle \cos\theta$

- Incident Power:  
---

## 🧮 Quick Reference Values

| Symbol | Meaning | Typical Expression |
|:--:|:--|:--|
| $k_0$ | Free-space wavenumber | $2\pi/\lambda_0$ |
| $\lambda_0$ | Wavelength | $c/f$ |
| $\eta_0$ | Free-space impedance | $377\ \Omega$ |
| $\alpha$ | Attenuation constant | $[\mathrm{Np/m}]$ |
| $\beta$ | Phase constant | $[\mathrm{rad/m}]$ |
| $\delta$ | Skin depth | $[\mathrm{m}]$ |
| $\tan\delta$ | Loss tangent | $\epsilon''/\epsilon'$ |
| $\langle S\rangle$ | Average Poynting | $E_0^2/(2\eta_0)$ |

---

> 🧠 **Tip for revision:**  
> - To check if something is a plane wave → confirm orthogonality and impedance.  
> - To classify a medium → compare $\tan\delta$.  
> - To evaluate power → use $\langle S \rangle = E_0^2/(2\eta_0)$ and apply $\cos\theta$ for angle projection.  
> - For conductors → skin depth tells how far fields penetrate; attenuation doubles for 2δ thickness.

---

**Linked detailed derivations:**  
See → [[Assignment-01]]
---

**See also:** [[MOC – Electromagnetics]]

Recent in same folder

```dataview
LIST FROM "Courses/Electromagnetics"
WHERE file.folder = this.file.folder AND file.name != this.file.name
SORT file.mtime desc
LIMIT 5
```


Outgoing links

```dataview
LIST FROM outgoing([[]])
WHERE contains(file.path,"Courses/Electromagnetics")
```
