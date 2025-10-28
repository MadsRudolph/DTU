---
title: "🧭 Electromagnetics – Plane Waves & Power (Step-by-Step, Collapsible)"
type: "assignment"
tags:
- Electromagnetics
  - assignment
  - General
aliases: []
links:
  formulas: []
  related: []
updated: "2025-10-28"
---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]
> **Quick refs:** [[Formulas/Plane Waves & Power — Quick Formula Sheet]] · [[MOC – Plane Waves]] · [[MOC – EM Loss & Skin Depth]]

# 🧭 Electromagnetics – Plane Waves & Power (Step-by-Step, Collapsible)

> 📘 **Reference:** [[Plane Waves & Power — Quick Formula Sheet]]


---

> [!summary] **Question 1 — Is it a plane wave?**
> **Concept:** A uniform plane wave must be transverse ($\mathbf E\perp\mathbf H\perp\hat\beta$) and satisfy $|\mathbf E|/|\mathbf H|=\eta$.
>
> **Given**  
> $\tilde{\mathbf E}_0=(2,0,0)$ V/m,  $\tilde{\mathbf H}_0=(0,-5.309,0)$ mA/m,  $\vec\gamma=(0,0,j3)$ m⁻¹  
>
> **Formulas**  
> – Transverse checks: $\tilde{\mathbf E}_0\!\cdot\!\tilde{\mathbf H}_0=0$, $\tilde{\mathbf E}_0\!\cdot\!\vec\gamma=0$, $\tilde{\mathbf H}_0\!\cdot\!\vec\gamma=0$  
> – Impedance: $|\mathbf E|/|\mathbf H|=\eta$
>
> **Derivation**  
> 1️⃣ Check orthogonality → all dot-products 0 ✔  
> 2️⃣ Compute ratio: $|\tilde{\mathbf H}_0|=0.005309$ A/m, $\frac{2}{0.005309}=376.7 \Omega\approx\eta_0$
>
> ✅ **Answer:** It *is* a plane wave.

---

> [!summary] **Question 2 — Is it a plane wave?**
> **Concept:** Same method as Q1.
>
> **Given**  
> $\tilde{\mathbf E}_0=(0,j2,5)$, $\tilde{\mathbf H}_0=(0,-0.0375,j0.015)$ A/m, $\vec\gamma=(j10,0,0)$ m⁻¹
>
> **Derivation**  
> Orthogonal? Yes.  
> Magnitude ratio $|\tilde{\mathbf E}|=5.385$, $|\tilde{\mathbf H}|=0.0404$, $\dfrac{5.385}{0.0404}=133 \Omega$ (valid medium).
>
> ✅ **Answer:** Plane wave in medium ($\eta≈133 \Omega$).

---

> [!summary] **Question 3 — Phase constant β**
> **Concept:** Phase constant $\beta=k_0\sqrt{\mu_r\epsilon_r}$ in lossless media.
>
> **Given:** $f=2$ GHz, $\epsilon_r=4$, $\mu_r=2$
>
> $$
> k_0=\frac{2\pi f}{c}=41.89,\qquad
> \beta=41.89\sqrt8=118.6\ \text{rad/m}
> $$
>
> ✅ **Answer:** $\boxed{\beta=118.6\ \text{rad/m}}$

---

> [!summary] **Question 4 — Electric field in time domain**
> **Concept:** Convert phasor → real-time sinusoid.
>
> **Given:** $\tilde{\mathbf E}_0=(0,0,j2)$  
>
> $$
> E_z=\Re\{j2e^{j\Phi}\}=2\cos(\Phi+\tfrac{\pi}{2})=-2\sin\Phi
> $$
>
> ✅ **Answer:** $\boxed{\mathbf E(\mathbf r,t)=(0,0,-2)\sin(\omega t-\vec\beta\!\cdot\!\mathbf r)}$

---

> [!summary] **Question 5 — Magnetic field phasor $\tilde{\mathbf H}_0$**
> **Concept:** $\tilde{\mathbf H}_0=\dfrac{1}{\eta}(\hat\beta\times\tilde{\mathbf E}_0)$
>
> **Given** $\tilde{\mathbf E}_0=(0,0,j2)$, $\hat\beta=(\cos30°,\,\sin30°,\,0)$, $\epsilon_r=4$, $\mu_r=2$
>
> $$
> \eta=377\sqrt{\tfrac{2}{4}}=266.7,\quad
> \hat\beta\times\tilde{\mathbf E}_0=(j1,-j1.732,0)
> $$
>
> $$
> \tilde{\mathbf H}_0=\tfrac{1}{266.7}(j1,-j1.732,0)=(j3.754,-j6.502,0)\,\text{mA/m}
> $$
>
> ✅ **Answer:** $(j3.754,\,-j6.502,\,0)$ mA/m.

---

> [!summary] **Question 6 — Medium classification**
> **Concept:** Use loss tangent $\tan\delta$ to identify material type.
>
> **Given:** $\tan\delta=0.2$
>
> | Medium type | Condition |
> |---|---|
> | Perfect dielectric | $\tan\delta=0$ |
> | **Low-loss dielectric** | **$\tan\delta\ll1$** |
> | Quasi-good insulator | $\tan\delta\approx1$ |
> | Good conductor | $\tan\delta\gg1$ |
>
> ✅ **Answer:** Low-loss dielectric ($0.2\ll1$).

---

> [!summary] **Question 7 — Attenuation constant α**
> **Concept:** Low-loss approximation $\alpha≈\tfrac{k_0\sqrt{\epsilon_r}\tan\delta}{2}$
>
> **Given:** $\epsilon_r=10$, $\tan\delta=0.2$, $f=20$ MHz  
>
> $$
> \lambda_0=\tfrac{3\cdot10^8}{20\cdot10^6}=15,\quad
> k_0=0.419,\quad
> \alpha=\tfrac{0.419\cdot3.162\cdot0.2}{2}=0.132\ \text{Np/m}
> $$
>
> ✅ **Answer:** $\boxed{0.13\ \text{Np/m}}$

---

> [!summary] **Question 8 — Field decrease over 7 m**
> **Formula:** $\text{Loss}_{dB}=8.686\,\alpha d$
>
> $$
> 8.686(0.132)(7)=8.0\ \text{dB}
> $$
>
> ✅ **Answer:** $\boxed{8\ \text{dB}}$

---

> [!summary] **Question 9 — Linear polarization (+x propagation)**
> **Concept:** $E_x=0$ (transverse) and $E_y/E_z$ real (same phase → linear)
>
> | Option | $\mathbf E_0$ | $E_x=0$? | Linear? | Conclusion |
> |:--:|:--|:--:|:--:|:--|
> | 1 | $(0,1+j,0)$ | Yes | Single component | ✅ Valid |
> | 2 | $(0,1,-j)$ | Yes | Phase shift → elliptical | ❌ |
> | 3 | $(0,0,-2)$ | Yes | Single component | ✅ Valid |
> | 4 | $(0,-j,j2)$ | Yes | Ratio $(-j)/(j2)=-½$ real | ✅ Valid |
> | 5 | $(-1,0,2)$ | No | — | ❌ |
> | 6 | $(1,0,0)$ | No (parallel) | — | ❌ |
>
> ✅ **Answer:** Valid $\mathbf E_0$ vectors: $(0,1+j,0)$, $(0,0,-2)$, $(0,-j,j2)$.

---

> [!summary] **Question 10 — Intrinsic polarization**
> Equal orthogonal components → circular; $(\mathbf u\times\mathbf v)\!\cdot\!\hat\beta<0$ → right-hand.
>
> ✅ **Answer:** Right-hand circular polarization (RHCP).

---

> [!summary] **Question 11 — Axial ratio**
> Circular polarization has $a=b$ → $R=a/b=1$ (0 dB).
>
> ✅ **Answer:** $R=1$ (0 dB).

---

> [!summary] **Question 12 — Average power density**
> **Given:** $H_0=0.01$ A/m. Use $\langle S\rangle=\tfrac12\eta_0H_0^2$.
>
> $$
> \langle S\rangle=\tfrac12(377)(0.01)^2=1.885\times10^{-2}\ \text{W/m}^2=18.9\ \text{mW/m}^2
> $$
>
> ✅ **Answer:** $\boxed{18.9\ \text{mW/m}^2}$

---

> [!summary] **Question 13 — Skin depth at 10 MHz**
> $\delta=\sqrt{\tfrac{2}{\omega\mu\sigma}}$
>
> $$
> \delta=\sqrt{\frac{2}{(2\pi10^7)(4\pi10^{-7})(2\cdot10^4)}}=1.13\ \text{mm}
> $$
>
> ✅ **Answer:** $\boxed{1.1\ \text{mm}}$

---

> [!summary] **Question 14 — Minimum frequency for 4 mm shield**
> $\delta=t\Rightarrow f=\tfrac{1}{\pi\mu\sigma t^2}$
>
> $$
> f=\frac{1}{\pi(4\pi10^{-7})(2\cdot10^4)(0.004)^2}=0.79\ \text{MHz}
> $$
>
> ✅ **Answer:** $\boxed{0.79\ \text{MHz}}$

---

> [!summary] **Question 15 — Incident power on a surface**
> $\langle S\rangle_\perp=\dfrac{E_0^2}{2\eta_0}\cos\theta$
>
> $$
> \langle S\rangle_\perp=\frac{1}{2\cdot377}\cos20^\circ
> =1.25\times10^{-3}\ \text{W/m}^2
> =1.25\times10^3\ \mu\text{W/m}^2
> $$
>
> ✅ **Answer:** $\boxed{1.25\times10^3\ \mu\text{W/m}^2}$
---

**See also:** [[MOC – Electromagnetics]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]

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