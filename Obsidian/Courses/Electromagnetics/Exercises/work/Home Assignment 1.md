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

> [!code]- MATLAB Solution
> ```matlab
> % Q1: Plane-wave check via orthogonality and |E|/|H| = eta
> E = [2, 0, 0];                    % V/m
> H_mA = [0, -5.309, 0];            % mA/m
> H = 1e-3 * H_mA;                  % A/m
> gamma = 1j*[0, 0, 3];             % j3 in z-hat
> 
> dot_EH  = dot(E, H);
> dot_Eg  = dot(E, gamma);
> dot_Hg  = dot(H, gamma);
> eta_ratio = norm(E)/norm(H);
> 
> fprintf('E·H=%.3g, E·γ=%.3g, H·γ=%.3g\n',dot_EH,dot_Eg,dot_Hg);
> fprintf('|E|/|H| = %.1f Ω (≈377 Ω ⇒ plane wave)\n',eta_ratio);
> ```

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

> [!code]- MATLAB Solution
> ```matlab
> E = [0, 1j*2, 5];
> H = [0, -0.0375, 1j*0.015];
> gamma = 1j*[10, 0, 0];
> eta = norm(E)/norm(H);
> fprintf('|E|=%.3f V/m, |H|=%.4f A/m, η=%.1f Ω\n',norm(E),norm(H),eta);
> ```

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

> [!code]- MATLAB Solution
> ```matlab
> c=3e8; f=2e9; mu_r=2; eps_r=4;
> k0=2*pi*f/c;
> beta=k0*sqrt(mu_r*eps_r);
> fprintf('β = %.1f rad/m\n',beta);
> ```

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

> [!code]- MATLAB Solution
> ```matlab
> syms omega t beta_x beta_y beta_z x y z real
> Ez = -2*sin(omega*t - (beta_x*x + beta_y*y + beta_z*z));
> pretty(Ez)
> ```

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

> [!code]- MATLAB Solution
> ```matlab
> eta=377*sqrt(2/4);
> E0=[0,0,1j*2];
> beta_hat=[cosd(30),sind(30),0];
> H0=cross(beta_hat,E0)/eta;
> disp(1e3*H0) % mA/m
> ```

---

> [!summary] **Question 6 — Medium classification**
> **Concept:** Use the loss tangent $\tan\delta$ to characterize the dielectric’s losses and classify the medium.
>
> **Given:**  
> The medium has a complex relative permittivity  
> $\varepsilon_{r,c} = 10(1 - j0.2)$  
> which means  
> $\varepsilon_r' = 10$ and $\varepsilon_r'' = 2$.
>
> **Definition:**  
> For any lossy dielectric,  
> $$
> \varepsilon_c = \varepsilon' - j\varepsilon'' = \varepsilon'(1 - j\tan\delta)
> $$
> so
> $$
> \tan\delta = \frac{\varepsilon''}{\varepsilon'}.
> $$
>
> **Derivation:**  
> Substituting from the given expression:
> $$
> \tan\delta = \frac{2}{10} = 0.2
> $$
> The loss tangent quantifies how much energy is dissipated versus stored.  
> Since $\tan\delta = 0.2 \ll 1$, the medium behaves as a **low-loss dielectric**.
>
> **Classification Table**
>
> | Medium type | Condition on $\tan\delta$ | Description |
> |--------------|---------------------------|--------------|
> | Perfect dielectric | $\tan\delta = 0$ | No losses |
> | **Low-loss dielectric** | **$\tan\delta \ll 1$** | Small dielectric loss (energy stored ≫ dissipated) |
> | Quasi-good insulator | $\tan\delta \approx 1$ | Moderate losses |
> | Good conductor | $\tan\delta \gg 1$ | Loss-dominated conduction |
>
> ✅ **Answer:** $\boxed{\text{Low-loss dielectric (}\tan\delta = 0.2 \ll 1\text{)}}$

> [!tip] **Note:**  
> No further calculation is needed because $\tan\delta$ is already contained in the complex permittivity expression.  
> You would only compute it from $\sigma$, $\omega$, and $\varepsilon'$ if the medium were defined by separate conduction and permittivity parameters.

> [!code]- MATLAB Solution
> ```matlab
> % Q6: Medium classification using loss tangent
> % Given: eps_r,c = 10*(1 - j*0.2)
> eps_r_real = 10;
> eps_r_imag = 10*0.2;
> tan_delta = eps_r_imag / eps_r_real;
> 
> if tan_delta == 0
>     cls = 'Perfect dielectric';
> elseif tan_delta < 0.1
>     cls = 'Very low-loss dielectric';
> elseif tan_delta < 0.5
>     cls = 'Low-loss dielectric';
> elseif tan_delta < 2
>     cls = 'Quasi-good insulator';
> else
>     cls = 'Good conductor';
> end
> 
> fprintf('tanδ = %.2f → %s\n', tan_delta, cls);
> ```

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

> [!code]- MATLAB Solution
> ```matlab
> c=3e8; f=20e6; eps_r=10; tan_delta=0.2;
> k0=2*pi*f/c;
> alpha=(k0*sqrt(eps_r)*tan_delta)/2;
> fprintf('α = %.3f Np/m\n',alpha);
> ```

---

> [!summary] **Question 8 — Field decrease over 7 m**
> **Formula:** $\text{Loss}_{dB}=8.686\,\alpha d$
>
> $$
> 8.686(0.132)(7)=8.0\ \text{dB}
> $$
>
> ✅ **Answer:** $\boxed{8\ \text{dB}}$

> [!code]- MATLAB Solution
> ```matlab
> alpha=0.132; d=7;
> L=8.686*alpha*d;
> fprintf('Loss = %.2f dB\n',L);
> ```

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

> [!code]- MATLAB Solution
> ```matlab
> opts={[0,1+1j,0];[0,1,-1j];[0,0,-2];[0,-1j,1j*2];[-1,0,2];[1,0,0]};
> for k=1:numel(opts)
>   E=opts{k};
>   Ex=E(1);Ey=E(2);Ez=E(3);
>   if abs(Ex)>1e-9,lin=false;
>   elseif abs(Ey)<1e-9||abs(Ez)<1e-9,lin=true;
>   else,lin=abs(imag(Ey/Ez))<1e-9;end
>   fprintf('Option %d → %s\n',k,string(lin));
> end
> ```

---

> [!summary] **Question 10 — Intrinsic polarization**
> Equal orthogonal components → circular; $(\mathbf u\times\mathbf v)\!\cdot\!\hat\beta<0$ → right-hand.
>
> ✅ **Answer:** Right-hand circular polarization (RHCP).

> [!code]- MATLAB Solution
> ```matlab
> u=[1,0,0]; v=[0,1,0]; beta_hat=[0,0,1];
> triple=dot(cross(u,v),beta_hat);
> if triple<0,hand="Right-hand";else,hand="Left-hand";end
> disp(hand)
> ```

---

> [!summary] **Question 11 — Axial ratio**
> Circular polarization has $a=b$ → $R=a/b=1$ (0 dB).
>
> ✅ **Answer:** $R=1$ (0 dB).

> [!code]- MATLAB Solution
> ```matlab
> a=1; b=1;
> R=a/b; R_dB=20*log10(R);
> fprintf('R=%.2f (%.1f dB)\n',R,R_dB);
> ```

---

> [!summary] **Question 12 — Average power density**
> **Given:** $H_0=0.01$ A/m. Use $\langle S\rangle=\tfrac12\eta_0H_0^2$.
>
> $$
> \langle S\rangle=\tfrac12(377)(0.01)^2=1.885\times10^{-2}\ \text{W/m}^2=18.9\ \text{mW/m}^2
> $$
>
> ✅ **Answer:** $\boxed{18.9\ \text{mW/m}^2}$

> [!code]- MATLAB Solution
> ```matlab
> eta0=377; H0=0.01;
> S=0.5*eta0*H0^2;
> fprintf('<S>=%.2e W/m^2 = %.2f mW/m^2\n',S,1e3*S);
> ```

---

> [!summary] **Question 13 — Skin depth at 10 MHz**
> $\delta=\sqrt{\tfrac{2}{\omega\mu\sigma}}$
>
> $$
> \delta=\sqrt{\frac{2}{(2\pi10^7)(4\pi10^{-7})(2\cdot10^4)}}=1.13\ \text{mm}
> $$
>
> ✅ **Answer:** $\boxed{1.1\ \text{mm}}$

> [!code]- MATLAB Solution
> ```matlab
> mu0=4*pi*1e-7; sigma=2e4; f=10e6;
> delta=sqrt(2/(2*pi*f*mu0*sigma));
> fprintf('δ = %.3f mm\n',1e3*delta);
> ```

---

> [!summary] **Question 14 — Minimum frequency for 4 mm shield**
> $\delta=t\Rightarrow f=\tfrac{1}{\pi\mu\sigma t^2}$
>
> $$
> f=\frac{1}{\pi(4\pi10^{-7})(2\cdot10^4)(0.004)^2}=0.79\ \text{MHz}
> $$
>
> ✅ **Answer:** $\boxed{0.79\ \text{MHz}}$

> [!code]- MATLAB Solution
> ```matlab
> mu0=4*pi*1e-7; sigma=2e4; t=4e-3;
> f=1/(pi*mu0*sigma*t^2);
> fprintf('f = %.2f MHz\n',f/1e6);
> ```

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

> [!code]- MATLAB Solution
> ```matlab
> eta0=377; E0=1; theta=deg2rad(20);
> S=(E0^2/(2*eta0))*cos(theta);
> fprintf('<S_perp>=%.3e W/m^2 = %.2f µW/m^2\n',S,1e6*S);
> ```

---

**See also:** [[MOC – Electromagnetics]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]

Recent in same folder

```dataview
LIST
FROM "Courses/Electromagnetics"
WHERE file.folder = this.file.folder AND file.path != this.file.path
SORT file.mtime desc
LIMIT 5
```



