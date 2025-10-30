---
title: 🧭 Electromagnetics – Plane Waves & Power (Step-by-Step, Collapsible)
type: assignment
tags:
  - Electromagnetics - assignment - General
aliases: []
links:
  formulas: []
  related: []
updated: 2025-10-28
---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]
> **Quick refs:** [[Formulas/Plane Waves & Power — Quick Formula Sheet]] · [[MOC – Plane Waves]] · [[MOC – EM Loss & Skin Depth]]

# 🧭 Electromagnetics – Plane Waves & Power (Step-by-Step, Collapsible)

> 📘 **Reference:** [[Plane Waves & Power — Quick Formula Sheet]]

---

# Plane Wave Verification — Examples & MATLAB Template

> [!info] **Concept**
> A uniform plane wave in a lossless medium must:
>
> - Be **transverse** → $\mathbf E\perp\mathbf H\perp\hat\beta$  
> - Satisfy the **intrinsic impedance relation**  
>   $$
>   \frac{|\mathbf E|}{|\mathbf H|}=\eta=\sqrt{\frac{\mu}{\varepsilon}}
>   $$
> - (In vacuum) $\eta_0=377~\Omega$

---

> [!summary] **Question 1 — Is it a plane wave?**
>
> **Given**  
> $\tilde{\mathbf E}_0=(2,0,0)$ V/m,  
> $\tilde{\mathbf H}_0=(0,-5.309,0)$ mA/m,  
> $\vec\gamma=(0,0,j3)$ m⁻¹  
>
> **Derivation**
>
> 1️⃣ Compute orthogonality  
> $\tilde{\mathbf E}_0\!\cdot\!\tilde{\mathbf H}_0=0$,  
> $\tilde{\mathbf E}_0\!\cdot\!\vec\gamma=0$,  
> $\tilde{\mathbf H}_0\!\cdot\!\vec\gamma=0$ → all zero ✔  
>
> 2️⃣ Compute impedance ratio  
> $|\tilde{\mathbf H}_0|=0.005309$ A/m  
> $\dfrac{2}{0.005309}=376.7~\Omega\approx\eta_0$
>
> ✅ **Conclusion:** It *is* a plane wave in **vacuum**.

> [!code]- MATLAB Check
> ```matlab
> % --- Question 1 ---
> E = [2, 0, 0];                    % V/m
> H_mA = [0, -5.309, 0];            % mA/m
> H = 1e-3 * H_mA;                  % Convert to A/m
> gamma = 1j * [0, 0, 3];           % j3 ẑ
> 
> % Orthogonality
> dotEH = dot(E,H);
> dotEg = dot(E,gamma);
> dotHg = dot(H,gamma);
> 
> % Intrinsic impedance ratio
> eta_ratio = norm(E)/norm(H);
> 
> fprintf('E·H=%.3g, E·γ=%.3g, H·γ=%.3g\n',dotEH,dotEg,dotHg);
> fprintf('|E|/|H| = %.1f Ω (≈377 Ω ⇒ plane wave)\n',eta_ratio);
> ```

---

> [!summary] **Question 2 — Is it a plane wave?**
>
> **Given**  
> $\tilde{\mathbf E}_0=(0,j2,5)$ V/m,  
> $\tilde{\mathbf H}_0=(0,-0.0375,j0.015)$ A/m,  
> $\vec\gamma=(j10,0,0)$ m⁻¹  
>
> **Derivation**
>
> 1️⃣ $\mathbf E\perp\mathbf H\perp\hat\beta$ → satisfied ✔  
>
> 2️⃣ Magnitude ratio  
> $|\tilde{\mathbf E}_0|=\sqrt{2^2+5^2}=5.385$  
> $|\tilde{\mathbf H}_0|=\sqrt{0.0375^2+0.015^2}=0.0404$  
> $\dfrac{5.385}{0.0404}=133~\Omega$
>
> ✅ **Conclusion:** Plane wave in a medium with $\eta\approx133~\Omega$.

> [!code]- MATLAB Check
> ```matlab
> % --- Question 2 ---
> E = [0, 1j*2, 5];                 % V/m
> H = [0, -0.0375, 1j*0.015];       % A/m
> gamma = 1j * [10, 0, 0];          % j10 x-hat
> 
> eta = norm(E)/norm(H);
> fprintf('|E|=%.3f V/m, |H|=%.4f A/m, η=%.1f Ω\n',norm(E),norm(H),eta);
> ```

---

## 🔁 Reusable MATLAB Template — Plane-Wave Validator

> [!code]- General Function
> ```matlab
> % ================== Plane Wave Validator ==================
> % Checks orthogonality and impedance condition for E, H, γ
> % Assumes time-harmonic fields exp(-jβ·r)
> clear; clc
> 
> % --- USER INPUT ---
> E = [0, 1j*2, 5];           % Electric field phasor [V/m]
> H = [0, -0.0375, 1j*0.015]; % Magnetic field phasor [A/m]
> gamma = 1j*[10, 0, 0];      % Propagation vector [1/m]
> eta_expected = 377;          % Vacuum impedance [Ω]
> 
> % --- CALCULATIONS ---
> dotEH = dot(E,H);
> dotEg = dot(E,gamma);
> dotHg = dot(H,gamma);
> eta = norm(E)/norm(H);
> 
> fprintf('E·H = %.3g,  E·γ = %.3g,  H·γ = %.3g\n',dotEH,dotEg,dotHg);
> fprintf('|E|=%.4g, |H|=%.4g  => |E|/|H|=%.1f Ω\n',norm(E),norm(H),eta);
> 
> if abs(dotEH)<1e-9 && abs(dotEg)<1e-9 && abs(dotHg)<1e-9
>     if abs(eta - eta_expected)/eta_expected < 0.05
>         disp("✅ Plane wave in vacuum");
>     else
>         fprintf("✅ Plane wave in medium (η≈%.1f Ω)\n",eta);
>     end
> else
>     disp("❌ Not a transverse plane wave");
> end
> % ==========================================================
> ```

---

**References**

- DTU *Electromagnetics — Summary II* slide (Plane wave conditions)  
- *Sadiku, Elements of Electromagnetics (8th Ed.),* §7-2 – §7-3  
- Vacuum impedance: $\eta_0=\sqrt{\mu_0/\varepsilon_0}=377 \Omega$

---

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
> [!summary] **Question 6 — Medium classification (corrected)**
> **Concept:** Use the **loss tangent** to classify media. From the slides:
>
> $$\tan(\delta) = \frac{\sigma}{\omega \varepsilon_0 \varepsilon_r} \quad \text{and} \quad \tan(\delta) = \frac{\varepsilon''}{\varepsilon'}$$
>
> **Given:** Complex relative permittivity $\varepsilon_{r,c}=10(1 - j0.2)$.
>
> **Derivation (from $\varepsilon_{r,c}$):**  
> $\varepsilon_r' = 10$, $\varepsilon_r'' = 10 \times 0.2 = 2$  
> therefore  
> $$\tan(\delta) = \frac{\varepsilon''}{\varepsilon'} = \frac{2}{10} = 0.2$$
>
> **Interpretation:**  
> The loss tangent quantifies how much energy is dissipated vs stored.  
> Since $10^{-2} \le 0.2 \le 10^{2}$, the medium is a **quasi-good insulator**.
>
> **Classification (per DTU slide “Rule of thumb”)**
>
> | Type | Range of $\tan(\delta)$ | Remarks |
> |------|--------------------------|----------|
> | Perfect dielectric insulator | $\sigma = 0 \Leftrightarrow \tan(\delta) = 0$ | No loss |
> | Low-loss medium (dielectric) / good insulator | $\tan(\delta) \le 10^{-2}$ | |
> | **Quasi-good conductor / quasi-good insulator / semiconductor** | $10^{-2} \le \tan(\delta) \le 10^{2}$ | Typical range for many real dielectrics |
> | Good conductor | $\tan(\delta) \ge 10^{2}$ | Loss-dominated |
> | Perfect electric conductor (PEC) | $\rho = 0 \Leftrightarrow \sigma = \infty \Leftrightarrow \tan(\delta) = \infty$ | |
>
> ✅ **Answer:** $\boxed{\text{Quasi-good insulator}}$ since $\tan(\delta) = 0.2$.

> [!tip] **Equivalence note:**  
> If the problem gives $\sigma$ instead of $\varepsilon_{r,c}$, use  
> $\tan(\delta) = \dfrac{\sigma}{\omega \varepsilon_0 \varepsilon_r}$.  
> Both formulas are equivalent because $\varepsilon'' = \sigma / \omega$.

> [!code]- MATLAB Solution
> ```matlab
> % Q6 (corrected): classify using loss tangent from given eps_r,c
> eps_r_real = 10;
> eps_r_imag = 10 * 0.2;                % from 10*(1 - j*0.2)
> tan_delta = eps_r_imag / eps_r_real;  % -> 0.2
> 
> % Slide-based classification
> if tan_delta == 0
>     cls = "perfect dielectric insulator";
> elseif tan_delta <= 1e-2
>     cls = "low-loss medium (dielectric) / good insulator";
> elseif tan_delta <= 1e2
>     cls = "quasi-good conductor / quasi-good insulator / semiconductor";
> else
>     cls = "good conductor";
> end
> fprintf('tanδ = %.3g  =>  %s\n', tan_delta, cls);
> 
> % Alternative path if sigma is given:
> % sigma = ...; f = ...; omega = 2*pi*f; eps0 = 8.854187817e-12;
> % eps_r = 10; tan_delta_sigma = sigma / (omega * eps0 * eps_r);
> ```
> 

---
> [!summary] **Question 7 — Attenuation constant $\alpha$ (in Np/m)**
> **Concept:**  
> For a lossy dielectric, the complex propagation constant is  
>
> $$
> \gamma = \alpha + j\beta = j\omega\sqrt{\mu\varepsilon_c}, \quad
> \varepsilon_c = \varepsilon'(1 - j\tan\delta)
> $$
>
> The **general** (no low-loss assumption) formulas are  
>
> $$
> \alpha = k_0\sqrt{\frac{\mu_r\varepsilon_r}{2}}
> \sqrt{\sqrt{1+\tan^2\delta}-1}
> $$
>
> $$
> \beta = k_0\sqrt{\frac{\mu_r\varepsilon_r}{2}}
> \sqrt{\sqrt{1+\tan^2\delta}+1}
> $$
>
> where $k_0 = \dfrac{2\pi f}{c}$.
>
> **Given:**  
> $f = 20\,\text{MHz},\ \varepsilon_r = 10,\ \mu_r = 1,\ \tan\delta = 0.2$
>
> **Calculation:**
>
> $$
> \begin{aligned}
> k_0 &= \frac{2\pi(20\times10^6)}{3\times10^8} = 0.4189~\text{rad/m} \\
> \sqrt{1+\tan^2\delta} &= \sqrt{1+0.04} = 1.0199 \\
> \alpha &= 0.4189\sqrt{\tfrac{10}{2}} \sqrt{1.0199 - 1} = 0.132~\text{Np/m}
> \end{aligned}
> $$
>
> ✅ **Answer:** $\boxed{\alpha = 0.132~\text{Np/m}}$  
> *(consistent with the low-loss approximation)*

> [!code]- MATLAB Solution
> ```matlab
> % Q7: Attenuation constant in Np/m (general formula)
> c = 3e8; f = 20e6;
> mu_r = 1; eps_r = 10; tand = 0.2;
> k0 = 2*pi*f/c;
> factor = k0*sqrt(mu_r*eps_r/2);
> alpha = factor*sqrt(sqrt(1+tand^2)-1);
> beta  = factor*sqrt(sqrt(1+tand^2)+1);
> fprintf('alpha = %.3f Np/m\n', alpha);
> ```

---

> [!summary] **Question 8 — Field decrease over 7 m (in dB)**
> **Concept:**  
> The field magnitude decays as $E(d) = E_0 e^{-\alpha d}$.  
> Converting to decibels:
>
> $$
> L_{\text{dB}} = 20\log_{10}\!\big(e^{\alpha d}\big) = 8.686\,\alpha d
> $$
>
> **Given:** $\alpha = 0.132~\text{Np/m},\ d = 7~\text{m}$
>
> **Calculation:**
>
> $$
> L_{\text{dB}} = 8.686 \times 0.132 \times 7 = \boxed{8.0~\text{dB}}
> $$
>
> ✅ **Answer:** $\boxed{8.0~\text{dB}}$ attenuation after 7 m.

> [!code]- MATLAB Solution
> ```matlab
> % Q8: Field attenuation over distance
> alpha = 0.132;    % Np/m (from Q7)
> d = 7;            % meters
> loss_dB = 8.686 * alpha * d;
> fprintf('Loss over %.1f m = %.2f dB\n', d, loss_dB);
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
> [!summary] **Question 10 — Intrinsic polarization (full derivation)**
> A plane wave in air (assume vacuum) has magnetic field
>
> $$
> \vec H(\vec r,t)=H_0\Big[\underbrace{\vec u}_{\text{cos coeff.}}\cos(\omega t-\vec\beta\!\cdot\!\vec r)
> +\underbrace{\vec v}_{\text{sin coeff.}}\sin(\omega t-\vec\beta\!\cdot\!\vec r)\Big],
> $$
>
> with
>
> $$
> \vec u=\begin{bmatrix}0.5345\\0.2673\\-0.8018\end{bmatrix},\qquad
> \vec v=\begin{bmatrix}0.6172\\-0.7715\\0.1543\end{bmatrix},\qquad
> H_0=0.01~\text{A/m},\qquad
> \vec\beta=\begin{bmatrix}10\\10\\10\end{bmatrix}\ \text{m}^{-1}.
> $$
>
> **Polarization test (time trace at a fixed point):**
>
> 1) *Orthogonality* — circular/elliptical needs orthogonal basis:
>
> $$
> \vec u\cdot\vec v\approx 0\ \ (\text{numerically }-4.63\times10^{-5}\approx 0).
> $$
>
> 2) *Equal magnitudes* — circular if $|\vec u|=|\vec v|$:
>
> $$
> |\vec u|\approx1.00001,\quad |\vec v|\approx0.99998\ \Rightarrow\ |\vec u|\simeq|\vec v|.
> $$
>
> 3) *Quadrature* — cosine/sine are $90^\circ$ apart → conditions 1–3 give **circular polarization**.
>
> 4) *Handedness* — the sign of the triple product decides RH/LH:
>
> $$
> \hat\beta=\frac{\vec\beta}{|\vec\beta|},\qquad
> T=(\vec u\times \vec v)\cdot\hat\beta\approx-0.99999<0
> \ \Rightarrow\ \textbf{Right-hand circular polarization (RHCP)}.
> $$
>
> ✅ **Answer:** **Right-hand circular polarization (RHCP)**.

> [!code]- MATLAB Solution (Reusable template)
> ```matlab
> % ====================== POLARIZATION TEMPLATE ==========================
> % Analyze intrinsic polarization (linear/elliptical/circular) and handedness
> % for fields of the form:  F(t) = u*cos(ψ) + v*sin(ψ), ψ=ωt-β·r
> %
> % --- PARAMS (edit for future problems) ---
> u    = [0.5345; 0.2673; -0.8018];   % cosine coefficient vector
> v    = [0.6172; -0.7715; 0.1543];   % sine coefficient vector
> beta = [10; 10; 10];                % phase vector (1/m)
> tol_orth = 1e-3;                    % orthogonality tolerance
> tol_mag  = 1e-3;                    % equal-magnitude tolerance
> % ----------------------------------------------------------------------
> 
> % --- Compute diagnostics ---
> nu = norm(u); nv = norm(v);
> ortho = dot(u,v);
> bhat = beta / norm(beta);
> triple = dot(cross(u,v), bhat);
> 
> % --- Decide polarization type ---
> if abs(ortho) < tol_orth
>     if abs(nu - nv) < tol_mag
>         pol = "circular";
>     else
>         pol = "elliptical";
>     end
> else
>     % If u and v not orthogonal, still elliptical in general
>     pol = "elliptical";
> end
> 
> % --- Handedness (only meaningful for elliptical/circular) ---
> handed = "N/A";
> if triple < 0, handed = "right-hand";
> elseif triple > 0, handed = "left-hand";
> end
> 
> % --- Axial ratio (major/minor), valid if nearly orthogonal ---
> AR = max(nu,nv)/min(nu,nv);
> AR_dB = 20*log10(AR);
> 
> % --- Print summary ---
> fprintf('u·v = %+ .3e (≈0 => orthogonal)\n', ortho);
> fprintf('|u| = %.6f, |v| = %.6f  -> AR = %.6f (%.4f dB)\n', nu, nv, AR, AR_dB);
> fprintf('Polarization = %s, Handedness = %s (triple = %.5f)\n', pol, handed, triple);
> 
> % --- Return results as a struct (handy in Live Scripts) ---
> results = struct('u',u,'v',v,'beta',beta,'ortho',ortho,'nu',nu,'nv',nv, ...
>                  'AR',AR,'AR_dB',AR_dB,'polarization',pol,'handedness',handed, ...
>                  'triple',triple);
> % ======================================================================
> ```

---
> [!summary] **Question 11 — Axial ratio (full derivation)**
> The axial ratio $R$ is the ratio of the major to minor axes of the polarization ellipse.  
> For a field
>
> $$
> \vec H(t)=H_0\,[\vec u\cos\psi+\vec v\sin\psi],\quad \psi=\omega t-\vec\beta\!\cdot\!\vec r,
> $$
>
> with $\vec u\perp\vec v$, the ellipse axes are proportional to $|\vec u|$ and $|\vec v|$.
> Hence
>
> $$
> R=\frac{\max(|\vec u|,|\vec v|)}{\min(|\vec u|,|\vec v|)}.
> $$
>
> Using the values above:
>
> $$
> |\vec u|\approx1.00001,\quad |\vec v|\approx0.99998
> \ \Rightarrow\ R\approx \frac{1.00001}{0.99998}\approx 1.00003 \simeq 1
> $$
>
> and in dB:
>
> $$
> R_{\text{dB}}=20\log_{10}R \approx 0\ \text{dB}.
> $$
>
> ✅ **Answer:** $\boxed{R=1\ \text{(0 dB)}}$ — **ideal circular polarization**.

> [!code]- MATLAB Solution (uses the same template results)
> ```matlab
> % Using the same params as above; AR and AR_dB already computed.
> fprintf('Axial Ratio = %.6f (%.4f dB)\n', AR, AR_dB);
> % For a standalone run, re-run the PARAMS section from the template block.
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



