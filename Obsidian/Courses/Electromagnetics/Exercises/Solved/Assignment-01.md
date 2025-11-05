---
title: "Assignment 01"
type: assignment
tags: [electromagnetics, plane-waves, exercise]
aliases: []
links: {"formulas": [], "related": []}
updated: 2025-10-28

---
> 🔗 [[MOC – Electromagnetics]] · [[MOC – Lectures]] · [[MOC – Exercises]] · [[Formulas/Plane Waves & Power — Quick Formula Sheet]]
> **Quick refs:** [[Formulas/Plane Waves & Power — Quick Formula Sheet]] · [[MOC – Plane-Waves]] · [[MOC – EM Loss & Skin Depth]]

# 🧭 Electromagnetics – Plane Waves & Power (Step-by-Step, Collapsible)

> 📘 **Reference:** [[Plane-Waves-Power-Quick-Sheet]]

---

## 🌊 Plane-Wave Verification — Cross-Product Method (Corrected)

> [!info] **Uniform Plane Wave Conditions (phasor amplitudes)**
>
> For a **uniform plane wave** in a lossless medium:
>
> $$\begin{aligned}
> \vec{\gamma}\times\tilde{\mathbf H}_0 &= -j\omega\varepsilon\,\tilde{\mathbf E}_0,\\
> \vec{\gamma}\times\tilde{\mathbf E}_0 &= +j\omega\mu\,\tilde{\mathbf H}_0,\\[3pt]
> \vec{\gamma}\!\cdot\!\tilde{\mathbf E}_0 &= 0,\qquad 
> \vec{\gamma}\!\cdot\!\tilde{\mathbf H}_0 = 0.
> \end{aligned}
> $$
> These ensure  
> • **Transverse** → $\mathbf E\perp\mathbf H\perp\hat\beta$  
> • **Mutually consistent** cross-products (no sign conflict)

---

> [!summary] **Question 1 — Not a plane wave**
>
> **Given**
> $$
> \tilde{\mathbf E}_0=\begin{bmatrix}2\\0\\0\end{bmatrix}\text{ V/m},\quad
> \tilde{\mathbf H}_0=\begin{bmatrix}0\\-5.309\\0\end{bmatrix}\text{ mA/m},\quad
> \vec{\gamma}=\begin{bmatrix}0\\0\\j3\end{bmatrix}\text{ m}^{-1}.
> $$
>
> Although $\vec{\gamma}\times\tilde{\mathbf H}_0\parallel\tilde{\mathbf E}_0$  the two slide equations cannot be satisfied simultaneously with **positive** $\omega\varepsilon$ and $\omega\mu$. Hence **not** a plane wave.

> [!code]- MATLAB Verification
> ```matlab
> % === Question 1 ===
> E0 = [2; 0; 0];               % V/m
> H0 = [0; -5.309e-3; 0];       % A/m  (mA/m → A/m)
> g  = [0; 0; 1j*3];            % x̂ * j10
> 
> tol = 1e-10;
> 
> % --- Transverse checks ---
> dotEg = dot(E0,g);
> dotHg = dot(H0,g);
> 
> % --- Cross products ---
> gXH = cross(g,H0);
> gXE = cross(g,E0);
> 
> % --- Parallelism residuals (0 if perfectly parallel) ---
> par1 = norm(cross(gXH, E0));   % γ×H0 ∥ E0
> par2 = norm(cross(gXE, H0));   % γ×E0 ∥ H0
> 
> % --- Recover ωε and ωμ component-wise using the slide relations ---
> % γ×H0 = -j*ωε*E0   ⇒  ωε = -(γ×H0)./(j*E0)
> % γ×E0 = +j*ωμ*H0   ⇒  ωμ =  (γ×E0)./(j*H0)
> omega_eps = []; omega_mu = [];
> 
> for k = 1:3
>     if abs(E0(k)) > 0
>         omega_eps(end+1) = (-gXH(k)) / (1j*E0(k));
>     end
>     if abs(H0(k)) > 0
>         omega_mu(end+1)  = ( gXE(k)) / (1j*H0(k));
>     end
> end
> 
> % --- Check conditions ---
> eps_real_ok = all(abs(imag(omega_eps)) < tol);
> mu_real_ok  = all(abs(imag(omega_mu))  < tol);
> eps_pos_ok  = all(real(omega_eps) > 0);
> mu_pos_ok   = all(real(omega_mu)  > 0);
> eps_consist = max(real(omega_eps)) - min(real(omega_eps)) < 1e-9;
> mu_consist  = max(real(omega_mu))  - min(real(omega_mu))  < 1e-9;
> trans_ok    = abs(dotEg) < tol && abs(dotHg) < tol;
> parallel_ok = par1 < tol && par2 < tol;
> 
> % --- Display results ---
> fprintf('E·γ=%.3e, H·γ=%.3e\n', dotEg, dotHg);
> fprintf('||cross(γ×H0,E0)||=%.3e, ||cross(γ×E0,H0)||=%.3e\n', par1, par2);
> fprintf('omega*eps components: %s\n', mat2str(omega_eps,6));
> fprintf('omega*mu  components: %s\n', mat2str(omega_mu ,6));
> 
> if trans_ok && parallel_ok && eps_real_ok && mu_real_ok && eps_pos_ok && mu_pos_ok ...
>         && eps_consist && mu_consist
>     disp("✅ Plane wave (relations hold with positive, consistent ωε and ωμ).");
> else
>     disp("❌ Not a plane wave (one or more checks failed).");
> end
> ```

---

> [!summary] **Question 2 — Plane wave (corrected MATLAB verification)**
>
> **Given**
>
> $$
> \tilde{\mathbf E}_0=\begin{bmatrix}0\\ j2\\ 5\end{bmatrix}\ \text{V/m},\quad
> \tilde{\mathbf H}_0=\begin{bmatrix}0\\ -37.5\\ j15\end{bmatrix}\ \text{mA/m},\quad
> \vec{\gamma}=\begin{bmatrix}j10\\0\\0\end{bmatrix}\ \text{m}^{-1}.
> $$
>
> Both cross-product relations are satisfied with **positive** $\omega\varepsilon$ and $\omega\mu$,  
> all components are consistent and transverse conditions hold → **Plane wave** ✅

> [!code]- MATLAB Verification
> ```matlab
> % === Question 2 ===
> E0 = [0; 1j*2; 5];               % V/m
> H0 = [0; -37.5e-3; 1j*15e-3];    % A/m  (mA/m → A/m)
> g  = [1j*10; 0; 0];              % x̂ * j10
> 
> tol = 1e-10;
> 
> % --- Transverse checks ---
> dotEg = dot(E0,g);
> dotHg = dot(H0,g);
> 
> % --- Cross products ---
> gXH = cross(g,H0);
> gXE = cross(g,E0);
> 
> % --- Parallelism residuals (0 if perfectly parallel) ---
> par1 = norm(cross(gXH, E0));   % γ×H0 ∥ E0
> par2 = norm(cross(gXE, H0));   % γ×E0 ∥ H0
> 
> % --- Recover ωε and ωμ component-wise using the slide relations ---
> % γ×H0 = -j*ωε*E0   ⇒  ωε = -(γ×H0)./(j*E0)
> % γ×E0 = +j*ωμ*H0   ⇒  ωμ =  (γ×E0)./(j*H0)
> omega_eps = []; omega_mu = [];
> 
> for k = 1:3
>     if abs(E0(k)) > 0
>         omega_eps(end+1) = (-gXH(k)) / (1j*E0(k));
>     end
>     if abs(H0(k)) > 0
>         omega_mu(end+1)  = ( gXE(k)) / (1j*H0(k));
>     end
> end
> 
> % --- Check conditions ---
> eps_real_ok = all(abs(imag(omega_eps)) < tol);
> mu_real_ok  = all(abs(imag(omega_mu))  < tol);
> eps_pos_ok  = all(real(omega_eps) > 0);
> mu_pos_ok   = all(real(omega_mu)  > 0);
> eps_consist = max(real(omega_eps)) - min(real(omega_eps)) < 1e-9;
> mu_consist  = max(real(omega_mu))  - min(real(omega_mu))  < 1e-9;
> trans_ok    = abs(dotEg) < tol && abs(dotHg) < tol;
> parallel_ok = par1 < tol && par2 < tol;
> 
> % --- Display results ---
> fprintf('E·γ=%.3e, H·γ=%.3e\n', dotEg, dotHg);
> fprintf('||cross(γ×H0,E0)||=%.3e, ||cross(γ×E0,H0)||=%.3e\n', par1, par2);
> fprintf('omega*eps components: %s\n', mat2str(omega_eps,6));
> fprintf('omega*mu  components: %s\n', mat2str(omega_mu ,6));
> 
> if trans_ok && parallel_ok && eps_real_ok && mu_real_ok && eps_pos_ok && mu_pos_ok ...
>         && eps_consist && mu_consist
>     disp("✅ Plane wave (relations hold with positive, consistent ωε and ωμ).");
> else
>     disp("❌ Not a plane wave (one or more checks failed).");
> end
> ```

---
> [!code]- MATLAB Plane-Wave Verification (Final Reusable Template)
> ```matlab
> % ==================== Plane-Wave Verification ====================
> % Verifies whether given E0, H0, and γ satisfy the uniform plane-wave
> % conditions from the EM theory slides:
> %   γ × H0 = -j ωε E0
> %   γ × E0 = +j ωμ H0
> %   γ·E0 = 0,  γ·H0 = 0
> %
> % ✅ Works for all Q1/Q2-type problems (just change inputs below)
> % ==================================================================
> 
> clear; clc
> % --- USER INPUTS (example: Question 2) ---
> E0 = [0; 1j*2; 5];               % Electric field phasor [V/m]
> H0 = [0; -37.5e-3; 1j*15e-3];    % Magnetic field phasor [A/m]
> g  = [1j*10; 0; 0];              % Propagation vector [1/m]
> 
> % --- SETTINGS ---
> tol         = 1e-10;   % general tolerance for floating-point checks
> tol_consist = 1e-9;    % tolerance for ωε/ωμ consistency
> 
> % --- Step 1: Transverse checks (E ⟂ γ, H ⟂ γ) ---
> dotEg = dot(E0, g);
> dotHg = dot(H0, g);
> trans_ok = abs(dotEg) < tol && abs(dotHg) < tol;
> 
> % --- Step 2: Cross products (from slide relations) ---
> % γ×H0 = -j ωε E0
> % γ×E0 = +j ωμ H0
> gXH = cross(g, H0);
> gXE = cross(g, E0);
> 
> % Scale-invariant parallelism residuals (should be ~0 for parallel)
> par1 = norm(cross(gXH, E0)) / max(norm(gXH)*norm(E0), eps);
> par2 = norm(cross(gXE, H0)) / max(norm(gXE)*norm(H0), eps);
> parallel_ok = par1 < 1e-10 && par2 < 1e-10;
> 
> % --- Step 3: Recover ωε and ωμ from available components ---
> omega_eps = [];
> omega_mu  = [];
> for k = 1:3
>     if abs(E0(k)) > 0
>         omega_eps(end+1) = (-gXH(k)) / (1j*E0(k));  % expect real, >0
>     end
>     if abs(H0(k)) > 0
>         omega_mu(end+1)  = ( gXE(k)) / (1j*H0(k));  % expect real, >0
>     end
> end
> 
> % --- Step 4: Physical sanity checks ---
> eps_real_ok = all(abs(imag(omega_eps)) < tol);
> mu_real_ok  = all(abs(imag(omega_mu))  < tol);
> eps_pos_ok  = all(real(omega_eps) > 0);
> mu_pos_ok   = all(real(omega_mu)  > 0);
> 
> eps_vals = real(omega_eps);
> mu_vals  = real(omega_mu);
> eps_consist = isempty(eps_vals) || (max(eps_vals)-min(eps_vals) < tol_consist);
> mu_consist  = isempty(mu_vals)  || (max(mu_vals)-min(mu_vals)  < tol_consist);
> 
> % --- Step 5: Print diagnostic summary ---
> fprintf('\n=== Plane-Wave Verification ===\n');
> fprintf('E·γ=%.3e,  H·γ=%.3e\n', dotEg, dotHg);
> fprintf('Parallel residuals: r1=%.3e, r2=%.3e\n', par1, par2);
> fprintf('ωε components: %s\n', mat2str(omega_eps,6));
> fprintf('ωμ components: %s\n', mat2str(omega_mu ,6));
> 
> % --- Step 6: Combined decision ---
> is_plane_wave = trans_ok && parallel_ok && ...
>                 eps_real_ok && eps_pos_ok && eps_consist && ...
>                 mu_real_ok  && mu_pos_ok  && mu_consist;
> 
> if is_plane_wave
>     disp("✅ Plane wave (relations hold with positive, consistent ωε and ωμ).");
> else
>     disp("❌ Not a plane wave (one or more checks failed).");
> end
> % ==================================================================
> ```
---

---
> [!summary] **Question 3 — Phase constant β**  
> **Problem:**  
> An electromagnetic wave is propagating in a **lossless medium** with relative permittivity  
> $\varepsilon_r = 4$ and relative permeability $\mu_r = 2$.  
> The frequency is $f = 2~\text{GHz}$.  
> The wave propagates in the **$xy$-plane**, making a **30° angle** from the positive $x$-axis.  
> Determine the **phase constant** β.
>
> **Concept:**  
> For a lossless medium, the phase constant is  
> $$
> \beta = k_0\sqrt{\mu_r\varepsilon_r}, \qquad
> k_0 = \frac{2\pi f}{c}.
> $$
>
> **Given:**  
> $f = 2~\text{GHz}$, $\varepsilon_r = 4$, $\mu_r = 2$, $c = 3\times10^8~\text{m/s}$  
> Propagation direction:  
> $$
> \hat{\beta} = (\cos30^\circ)\hat{x} + (\sin30^\circ)\hat{y}.
> $$
>
> **Calculation:**  
> $$
> k_0 = \frac{2\pi (2\times10^9)}{3\times10^8} = 41.89~\text{rad/m}
> $$
> $$
> \beta = 41.89\sqrt{\mu_r\varepsilon_r}
>        = 41.89\sqrt{2\times4}
>        = 41.89\sqrt{8}
>        = 118.6~\text{rad/m}
> $$
>
> ✅ **Answer:** $\boxed{\beta = 118.6~\text{rad/m}}$
>
> Propagation direction (unit vector):  
> $\hat{\beta} = (0.866\hat{x} + 0.5\hat{y})$

> [!code]- MATLAB Solution
> ```matlab
> % Question 3 – Phase constant β
> c = 3e8;
> f = 2e9;
> mu_r = 2;
> eps_r = 4;
> 
> k0 = 2*pi*f/c;
> beta = k0*sqrt(mu_r*eps_r);
> 
> % Unit propagation vector (30° in xy-plane)
> beta_hat = [cosd(30), sind(30), 0];
> 
> fprintf('β = %.1f rad/m\n', beta);
> fprintf('β̂ = [%.3f, %.3f, 0]\n', beta_hat);
> ```

---
> [!summary] **Question 4 — Electric Field in Time Domain**
>
> With angular frequency $\omega$, phase vector $\vec{\beta}$, and position vector $\vec{r}$, determine the **time-domain expression** for the electric field when  
> 
> $$
> \tilde{\mathbf E}_0 =
> \begin{bmatrix}
> 0 \\[2pt]
> 0 \\[2pt]
> j2
> \end{bmatrix}
> \text{ V/m},
> \quad
> \psi = \omega t - \vec{\beta}\!\cdot\!\vec r.
> $$
>
> The wave propagates in the $xy$-plane at an angle of 30°, in a **lossless medium** with $\varepsilon_r=4$ and $\mu_r=2$ (from Q3).

---

> [!info] **Concept — Phasor → Time-Domain Conversion**
>
> For the $e^{j\omega t}$ phasor convention, a component $\tilde E=Ae^{j\phi}$ corresponds to  
> $$
> E(t)=A\cos(\omega t+\phi-\vec{\beta}\!\cdot\!\vec r)
> $$
> so:
>
> | Phasor component | Time-domain equivalent |
> |:-----------------|:-----------------------|
> | $\tilde E=+A$ (real) | $+A\cos\psi$ |
> | $\tilde E=-A$ (real) | $-A\cos\psi$ |
> | $\tilde E=+jA$ | $-A\sin\psi$ |
> | $\tilde E=-jA$ | $+A\sin\psi$ |
>
> where $\psi=\omega t-\vec{\beta}\!\cdot\!\vec r$.  
> These rules come directly from $\Re\{Ae^{j\psi}\}$ and $\Re\{jAe^{j\psi}\}$.

---

### 🧮 Derivation

Given $\tilde{\mathbf E}_0=(0,0,j2)$:

$$
E_z = \Re\{j2\,e^{j\psi}\}
     = 2\cos(\psi+\tfrac{\pi}{2})
     = -2\sin(\psi).
$$

$$
\Rightarrow\quad
\boxed{\mathbf E(\mathbf r,t)
=(0,0,-2)\sin(\omega t-\vec{\beta}\!\cdot\!\vec r)}.
$$

✅ **Answer:** $\mathbf E(\mathbf r,t)=(0,0,-2)\sin(\omega t-\vec{\beta}\!\cdot\!\vec r)$

---

> [!code]- **MATLAB Tool — Phasor → Time-Domain (MCQ Helper)**
> ```matlab
> % ==========================================================
> %  Phasor → Time-domain (MCQ-friendly)
> %  e^{jωt} convention: F(t) = Re{ F~ e^{jψ} }
> % ==========================================================
> clear; clc
> 
> % --- USER INPUT (edit for new problems) ---
> Ftilde = [0; 0; 1j*2];   % complex phasor [V/m] or [A/m]
> syms psi real             % keep ψ symbolic: ψ = ωt - β·r
> 
> % --- Magnitude & phase of each component ---
> A   = abs(Ftilde);
> phi = angle(Ftilde);
> tol = 1e-8;
> 
> fprintf('Components (ψ = ωt - β·r):\n');
> for k = 1:3
>     disp(canonicalString(A(k),phi(k),tol))
> end
> 
> % ---------- Helper function ----------
> function s = canonicalString(A,phi,tol)
>     if A < tol, s = '0'; return; end
>     m = round(phi/(pi/2)); phi_snap = (pi/2)*m;
>     if abs(phi - phi_snap) < tol
>         k = mod(m,4); % 0:cos, 1:-sin, 2:-cos, 3:sin
>         switch k
>             case 0, s = sprintf('%.3g*cos(ψ)',A);
>             case 1, s = sprintf('%.3g*(-sin(ψ))',A);
>             case 2, s = sprintf('%.3g*(-cos(ψ))',A);
>             case 3, s = sprintf('%.3g*sin(ψ)',A);
>         end
>     else
>         s = sprintf('%.3g*cos(ψ %+6.1f°)',A,rad2deg(phi));
>     end
> end
> ```

---

### 🧭 How to Use the Code

1. **Set your phasor**  
   Replace `Ftilde` with your complex phasor components (e.g., `[0; 0; 1j*2]`).

2. **Run the script**  
   It prints each component as a clean sinusoid, e.g.
```
Components (ψ = ωt - β·r):  
0  
0  
2*(-sin(ψ))
```
3. **Interpret**  
The output directly matches the MCQ options:
- `2*(-sin(ψ))` → amplitude 2, negative sign → $-2\sin(ψ)$  
⇒ choose $\mathbf E=(0,0,-2)\sin(\omega t-\vec{\beta}\!\cdot\!\vec r)$.

4. **Reuse**  
For any new field (E or H), just replace the vector in `Ftilde`.  
The helper automatically converts any $\tilde F_k$ with phase 0°, ±90°, 180° into the proper $\sin$ / $\cos$ form.

---

> [!tip]
> If your course uses the $e^{-j\omega t}$ convention, swap the sign for the $\pm jA$ terms (i.e., $+jA ↦ + A\sin\psi$ instead of $-A\sin\psi$).  
> Stick to one convention consistently throughout your notes.

---
> [!summary] **Question 5 — Magnetic Field Phasor $\tilde{\mathbf H}_0$**
>
> **Problem (from quiz)**  
> A uniform plane wave propagates in a lossless medium with $\varepsilon_r=4$ and $\mu_r=2$.  
> The electric-field phasor is  
> $$
> \tilde{\mathbf E}_0=
> \begin{bmatrix}0\\0\\j2\end{bmatrix}\ \text{V/m},
> $$
> and the propagation direction is  
> $\hat{\beta}=(\cos30^\circ,\ \sin30^\circ,\ 0)$.  
> Find the **magnetic-field phasor amplitude** $\tilde{\mathbf H}_0$ in mA/m.
>
> **Given:**  
> $\varepsilon_r=4,\quad \mu_r=2,\quad \hat{\beta}=(\cos30^\circ,\sin30^\circ,0),\quad \tilde{\mathbf E}_0=(0,0,j2)$.
>
> ---
>
> **Concept — Field Relationship in a Plane Wave**
>
> For a wave obeying the $e^{j\omega t}$ convention:
> $$
> \boxed{\tilde{\mathbf H}_0=\frac{1}{\eta}(\hat{\beta}\times\tilde{\mathbf E}_0)},\qquad
> \eta=\eta_0\sqrt{\frac{\mu_r}{\varepsilon_r}},\quad \eta_0=377~\Omega
> $$
>
> The vectors $\mathbf E$, $\mathbf H$, and $\hat\beta$ form a right-handed orthogonal triad.

---

### 🧮 Derivation

Compute:
$$
\eta=377\sqrt{\tfrac{2}{4}}=266.7~\Omega
$$
$$
\hat{\beta}\times\tilde{\mathbf E}_0
=(\cos30,\sin30,0)\times(0,0,j2)
=(j1,\,-j1.732,\,0)
$$
$$
\tilde{\mathbf H}_0
=\frac{1}{266.7}(j1,\,-j1.732,\,0)
=(j3.754,\,-j6.502,\,0)\ \text{mA/m}
$$

✅ **Answer:**  
$\boxed{\tilde{\mathbf H}_0=(j3.754,\,-j6.502,\,0)\ \text{mA/m}}$

---

> [!code]- **MATLAB Tool — Determine $\tilde{\mathbf H}_0$ and Compare with MCQ**
> ```matlab
> % ==============================================================
> %   Magnetic Field Phasor Finder (e^{jωt} convention)
> %   Computes H0 = (1/eta) * (β̂ × E0)
> %   Also prints amplitude + phase for MCQ comparison
> % ==============================================================
> clear; clc
> 
> % --- USER INPUT (edit for new problems) ---
> E0 = [0, 0, 1j*2];                  % Electric-field phasor [V/m]
> beta_hat = [cosd(30), sind(30), 0]; % Propagation direction
> eps_r = 4; mu_r = 2;
> 
> % --- Computation ---
> eta0 = 377;                    % Free-space impedance [Ω]
> eta  = eta0 * sqrt(mu_r/eps_r);
> bhat = beta_hat / norm(beta_hat);
> H0   = cross(bhat, E0) / eta;  % A/m
> 
> % --- Display results ---
> fprintf('H0 (A/m)  = [%+.6g, %+.6g, %+.6g]\n', H0);
> fprintf('H0 (mA/m) = [%+.3f, %+.3f, %+.3f]\n', 1e3*H0);
> 
> % Amplitude and phase (useful for MCQ reasoning)
> mag = abs(1e3*H0);
> ang = angle(H0)*180/pi;
> fprintf('\nComponent magnitudes (mA/m): [%.3f, %.3f, %.3f]\n', mag);
> fprintf('Component phases (deg): [%.1f°, %.1f°, %.1f°]\n', ang);
> 
> % --- Optional consistency check ---
> ratio = norm(E0)/norm(H0);
> fprintf('\n|E|/|H| = %.2f Ω  (η expected = %.2f Ω)\n', ratio, eta);
> ```
>
> **How to use:**
> 1. Replace `E0`, `beta_hat`, `eps_r`, `mu_r` with your problem values.  
> 2. Run the script.  
> 3. The line  
>    ```
>    H0 (mA/m) = [ +j3.754  -j6.502  0.000 ]
>    ```
>    tells you directly which MCQ option matches.  
> 4. Use the phase output (`±90° → j or −j`) to identify sign errors in alternatives.  
> 5. Check `|E|/|H|≈η` to verify correctness.

---

### 🧭 Key Takeaways
- $\tilde{\mathbf H}_0$ is **orthogonal** to both $\tilde{\mathbf E}_0$ and $\hat{\beta}$, following the right-hand rule.  
- The $j$ factor indicates the **90° phase shift** between $\mathbf E$ and $\mathbf H$.  
- The magnitude ratio $\dfrac{|\mathbf E|}{|\mathbf H|}=\eta$ always holds in a lossless medium.  
- Reversing $\hat{\beta}$ would flip the sign of $\mathbf H_0$.  

---
> [!summary] **Question 6 — Medium classification**
>
> **Problem:**  
> A uniform electromagnetic plane wave with a frequency of 20 MHz propagates in a non-magnetic medium with the **complex relative permittivity**
> $$
> \varepsilon_{r,c} = 10(1 - j0.2)
> $$
> Classify the medium using the loss-tangent method.
>
> 
>
> **Concept:**  
> The loss tangent quantifies how much electric energy is dissipated compared to stored energy:
> $$
> \tan(\delta) = \frac{\varepsilon''}{\varepsilon'} = \frac{\sigma}{\omega\varepsilon_0\varepsilon_r}.
> $$
>
> 
>
> **Derivation:**  
> From $\varepsilon_{r,c}=10(1-j0.2)$  
> → $\varepsilon'_r=10$,  $\varepsilon''_r=2$  
> → $\tan(\delta)=\dfrac{\varepsilon''}{\varepsilon'}=\dfrac{2}{10}=0.2$  
>
> 
>
> **Classification (rule of thumb):**
>
> | Type | Range of $\tan(\delta)$ | Description |
> |------|---------------------------|--------------|
> | Perfect dielectric | 0 | No loss |
> | Low-loss dielectric | ≤ 10⁻² | Good insulator |
> | **Quasi-good insulator / conductor** | 10⁻² ≤ tan δ ≤ 10² | Moderate loss |
> | Good conductor | ≥ 10² | Loss-dominated |
>
> ✅ **Answer:** $\boxed{\text{Quasi-good insulator}}$ since $\tan\delta=0.2$.
---

> [!code]- **MATLAB Template**
> ```matlab
> % Q6 – Medium classification from complex permittivity
> eps_r_complex = 10*(1 - 1j*0.2);
> eps_r_real = real(eps_r_complex);
> eps_r_imag = -imag(eps_r_complex);
> tan_delta = eps_r_imag / eps_r_real;
> 
> if tan_delta == 0
>     cls = "Perfect dielectric";
> elseif tan_delta <= 1e-2
>     cls = "Low-loss dielectric";
> elseif tan_delta <= 1e2
>     cls = "Quasi-good insulator / conductor";
> else
>     cls = "Good conductor";
> end
> 
> fprintf("tanδ = %.3f  →  %s\n", tan_delta, cls);
> ```
>
> ---
>
> **Alternative:**  
> If $\sigma$ is given instead, use $\tan\delta = \dfrac{\sigma}{\omega\varepsilon_0\varepsilon_r}$.

---
> [!summary] **Question 7 — Attenuation constant $\alpha$ (Np/m)**
>
> **Problem:**  
> A 20 MHz plane wave propagates in a non-magnetic medium ($\mu_r=1$) with $\varepsilon_r=10$ and $\tan\delta=0.2$.  
> Determine the **attenuation constant** $\alpha$ in Np/m.
>
> 
>
> **Concept:**  
> For a lossy dielectric:
> $$
> \gamma = \alpha + j\beta = j\omega\sqrt{\mu\varepsilon_c},\quad
> \varepsilon_c = \varepsilon'(1 - j\tan\delta)
> $$
>
> General formulas (no low-loss approximation):
> $$
> \alpha = k_0\sqrt{\frac{\mu_r\varepsilon_r}{2}}
> \sqrt{\sqrt{1+\tan^2\delta}-1},\quad
> \beta  = k_0\sqrt{\frac{\mu_r\varepsilon_r}{2}}
> \sqrt{\sqrt{1+\tan^2\delta}+1}
> $$
> with $k_0=\dfrac{2\pi f}{c}$.
>
> 
>
> **Calculation:**
> $$
> \begin{aligned}
> f &= 20~\text{MHz},\quad \tan\delta=0.2,\\
> k_0 &= \tfrac{2\pi(20\times10^6)}{3\times10^8}=0.41888~\text{rad/m},\\
> \sqrt{1+\tan^2\delta}&=\sqrt{1.04}=1.01990,\\
> \alpha &= 0.41888\sqrt{\tfrac{10}{2}}\sqrt{1.01990-1}
> = \boxed{0.1319~\text{Np/m}}.
> \end{aligned}
> $$
>
> ✅ **Answer:** $\boxed{\alpha=0.1319~\text{Np/m}}$.
---

> [!code]- **MATLAB Template**
> ```matlab
> % Q7 – Attenuation constant (precise)
> c = 3e8;  f = 20e6;
> mu_r = 1; eps_r = 10; tand = 0.2;
> 
> k0 = 2*pi*f/c;
> factor = k0*sqrt(mu_r*eps_r/2);
> alpha = factor*sqrt(sqrt(1+tand^2)-1);
> beta  = factor*sqrt(sqrt(1+tand^2)+1);
> 
> fprintf("α = %.4f Np/m\n", alpha);
> fprintf("β = %.4f rad/m\n", beta);
> ```
>
> ---
>
> **Note:** Using `%.4f` ensures you get the exact `0.1319 Np/m` result.

---
> [!summary] **Question 8 — Field decrease over 7 m (in dB)**
>
> **Problem:**  
> After the wave from Question 7 propagates 7 m, by how many decibels (dB) has its **field amplitude** decreased?  
> (Use $\alpha=0.1319$ Np/m.)
>
> 
>
> **Concept:**  
> The field magnitude decays as $E(d)=E_0e^{-\alpha d}$.  
> Converting to decibels:
> $$
> L_\text{dB} = 20\log_{10}(e^{\alpha d}) = 8.686\,\alpha d
> $$
>
> 
>
> **Calculation:**
> $$
> L_\text{dB}=8.686(0.1319)(7)=\boxed{8.00~\text{dB}}
> $$
>
> ✅ **Answer:** $\boxed{8.0~\text{dB}}$ attenuation after 7 m.
 
> [!code]- **MATLAB Template**
> ```matlab
> % Q8 – Field attenuation over distance
> alpha = 0.1319;   % Np/m (from Q7)
> d = 7;            % m
> loss_dB = 8.686 * alpha * d;
> fprintf("Field attenuation = %.2f dB\n", loss_dB);
> ```
>
>
> **Tip:** This formula works for any distance `d` and attenuation constant `α` — just edit the two numbers.

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
> [!summary] **Question 10 — Intrinsic Polarization (Full Derivation, Corrected)**
>
> A plane wave in air (assume vacuum) has the magnetic field
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
> ---
>
> **Step 1 — Orthogonality and Magnitudes**
>
> - $\vec u\cdot\vec v = -4.63\times10^{-5}\approx0$ → **orthogonal**  
> - $|\vec u|=1.000011,\ |\vec v|=0.999978$ → **equal magnitude**  
> - $\text{Axial Ratio: }AR = 1.000033\ (0.0003~\text{dB})$  
>
> ⮕ These confirm **circular polarization**.
>
> ---
>
> **Step 2 — Handedness**
>
> For a field written as $F(t)=\vec u\cos\psi+\vec v\sin\psi$  
> with $\psi=\omega t-\vec\beta\!\cdot\!\vec r$, the handedness is found from
>
> $$
> s=\hat\beta\cdot(\vec u\times\vec v)
> $$
>
> - If $s>0$ → Right-hand circular (RHCP)  
> - If $s<0$ → Left-hand circular (LHCP)
>
> Calculation gives $s=-0.99999<0$ → **Left-hand circular polarization (LHCP)**.
>
> ✅ **Answer:** $\boxed{\text{Left-hand circular polarization (LHCP)}}$

---

> [!code]- MATLAB Solution (Reusable & Corrected)
> ```matlab
> % ====================== POLARIZATION TEMPLATE (corrected) =====================
> % Field form: F(t) = u*cos(psi) + v*sin(psi), psi = omega*t - beta·r
> % Handedness rule for this form:
> %   s = bhat · (u × v)
> %   s > 0  -> right-hand,  s < 0 -> left-hand
> %
> % --- PARAMETERS (edit for new problems) ---
> u    = [0.5345;  0.2673; -0.8018];   % cosine coefficient vector
> v    = [0.6172; -0.7715;  0.1543];   % sine coefficient vector
> beta = [10; 10; 10];                 % phase vector (1/m)
> tol_orth = 1e-3;                     % orthogonality tolerance
> tol_mag  = 1e-3;                     % equal-magnitude tolerance
> % -----------------------------------------------------------------------------
>
> % Diagnostics
> nu = norm(u); nv = norm(v);
> ortho  = dot(u,v);
> bhat   = beta / norm(beta);
> s      = dot(cross(u,v), bhat);      % <-- corrected sign & rule
>
> % Type
> if abs(ortho) < tol_orth && abs(nu - nv) < tol_mag
>     pol = "circular";
> else
>     pol = "elliptical";
> end
>
> % Handedness
> handed = "N/A";
> if s > 0, handed = "right-hand";
> elseif s < 0, handed = "left-hand";
> end
>
> % Axial ratio (quick estimate from |u|,|v|)
> AR    = max(nu,nv)/min(nu,nv);
> AR_dB = 20*log10(AR);
>
> % Report
> fprintf('u·v = %+ .3e (≈0 => orthogonal)\n', ortho);
> fprintf('|u| = %.6f, |v| = %.6f  -> AR ≈ %.6f (%.4f dB)\n', nu, nv, AR, AR_dB);
> fprintf('Polarization = %s, Handedness = %s (s = %.5f)\n', pol, handed, s);
> % =============================================================================
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
> [!summary] **Question 12 — Time-Average Power Density (Lossless Plane Wave)**
>
> **Question:**  
> What is the magnitude of the **time-average power flow density** at  
> $x = y = z = 100~\text{m}$?  
> Express the value in $\mu\text{W}/\text{m}^2$.
>
> ---
>
> **Concept:**  
> For a **lossless plane wave**, the time-average Poynting vector magnitude is given by:
>
> - Using **peak (phasor)** fields:  
>   $$
>   \langle S \rangle = \frac{|E_0|^2}{2\eta_0} = \frac{\eta_0 |H_0|^2}{2}
>   $$
>
> - Using **RMS** fields:  
>   $$
>   \langle S \rangle = \frac{E_{\text{rms}}^2}{\eta_0} = \eta_0 H_{\text{rms}}^2
>   $$
>
> Since the given magnetic field amplitude $H_0 = 0.01~\text{A/m}$ is an **RMS value**,  
> we use the **RMS form** of the expression.
>
> ---
>
> **Given:**
> - $H_0 = 0.01~\text{A/m}$
> - $\eta_0 = 377~\Omega$
>
> ---
>
> **Calculation:**
>
> $$
> \begin{aligned}
> \langle S \rangle &= \eta_0 H_0^2 \\
> &= 377 \times (0.01)^2 \\
> &= 3.77\times10^{-2}~\text{W/m}^2 \\
> &= 37.7~\text{mW/m}^2
> \end{aligned}
> $$
>
> ✅ **Answer:** $\boxed{37.7~\text{mW/m}^2}$
>
> ---
>
> **Interpretation:**  
> This is the **time-average power density** (magnitude of the Poynting vector)  
> of a uniform plane wave propagating in a **lossless medium** (vacuum).
>
> ---

> [!code]- MATLAB Solution
> ```matlab
> % Q12 — Time-average power density (lossless plane wave)
> eta0 = 377;          % [ohm] intrinsic impedance of free space
> H0   = 0.01;         % [A/m] magnetic field amplitude (RMS)
> 
> % If given as RMS: use S = eta0 * H0^2
> % If given as peak: use S = 0.5 * eta0 * H0^2
> 
> S = eta0 * H0^2;      % [W/m^2]
> fprintf("<S> = %.4f W/m^2 = %.2f mW/m^2 = %.2f µW/m^2\n", S, 1e3*S, 1e6*S);
> ```


---
> [!summary] **Question 13 — Skin Depth at 10 MHz**
>
> **Question:**  
> “At a frequency of 10 MHz, what is the skin depth of the conductor given in mm?  
> The conductor is non-magnetic and has conductivity $\sigma = 2\cdot10^4~\text{S/m}$.”
>
> ---
>
> **Concept:**  
> The **skin depth** $\delta$ is the distance below the surface of a conductor where  
> the electromagnetic field amplitude falls to $1/e$ (≈ 37%) of its value at the surface.  
> It is given by:
>
> $$
> \delta = \sqrt{\frac{2}{\omega \mu \sigma}}, \qquad \omega = 2\pi f
> $$
>
> ---
>
> **Given:**  
> - $f = 10~\text{MHz}$  
> - $\sigma = 2\times10^4~\text{S/m}$  
> - $\mu = \mu_0 = 4\pi\times10^{-7}~\text{H/m}$  
>
> **Calculation:**
>
> $$
> \begin{aligned}
> \delta &= \sqrt{\frac{2}{(2\pi\times10^7)(4\pi\times10^{-7})(2\times10^4)}} \\
> &= 1.125\times10^{-3}~\text{m} = 1.125~\text{mm}
> \end{aligned}
> $$
>
> ✅ **Answer:** $\boxed{\delta = 1.125~\text{mm}}$
>
> ---
>
> **Interpretation:**  
> Inside a conductor, the electric field decays exponentially as  
> $E(z)=E_0e^{-z/\delta}$.  
> After one skin depth, the field has dropped to 37% of the surface value.  
> For this conductor, only the outermost 1 mm carries most of the current.
>
> ---

> [!code]- MATLAB Solution
> ```matlab
> % Q13 – Skin depth at 10 MHz
> mu0   = 4*pi*1e-7;      % [H/m]
> sigma = 2e4;            % [S/m]
> f     = 10e6;           % [Hz]
> delta = sqrt(2/(2*pi*f*mu0*sigma));
> fprintf('δ = %.4f mm\n', 1e3*delta);
> ```
---

> [!summary] **Question 14 — Minimum Frequency for a 4 mm EM Shield**
>
> **Question:**  
> “For a thickness of 4 mm, what is the minimum frequency of the EM shield?  
> Express the frequency in MHz.”
>
> 
>
> **Concept:**  
> The **skin depth relation** is
>
> $$
> \delta = \sqrt{\frac{2}{\omega\mu\sigma}}, \qquad \omega = 2\pi f
> $$
>
> Solving for $f$:
>
> $$
> f = \frac{1}{\pi\mu\sigma\delta^2}
> $$
>
> For shielding, two regimes are compared:
>
> 1. **Transition region:** $\delta = t$  
> 2. **Effective shielding (rule of thumb):** $t \ge 5\delta$ → field almost zero inside.
>
> 
>
> **Given:**  
> - $t = 4~\text{mm} = 0.004~\text{m}$  
> - $\sigma = 2\times10^4~\text{S/m}$  
> - $\mu = \mu_0 = 4\pi\times10^{-7}~\text{H/m}$  
> ---

> [!info] Case 1 — When $\delta = t$
>
> $$
> f = \frac{1}{\pi(4\pi\times10^{-7})(2\times10^{4})(0.004)^2}
> = 0.79~\text{MHz}
> $$
>
> ✅ **Interpretation:**  
> This frequency marks the point where the field begins to be significantly attenuated,  
> since the skin depth equals the material thickness.
>
> 

> [!info] Case 2 — Rule of Thumb ($t ≥ 5\delta$)
>
> Effective shielding is achieved when $t = 5\delta$, i.e. $\delta = t/5$.  
> Substituting gives:
>
> $$
> f = \frac{1}{\pi\mu\sigma(t/5)^2}
> = \frac{25}{\pi\mu\sigma t^2}
> = 25\times0.79~\text{MHz}
> \approx 19.8~\text{MHz}
> $$
>
> ✅ **Interpretation:**  
> At approximately 20 MHz, the conductor thickness is five times the skin depth,  
> so the field is attenuated by $e^{-5} ≈ 0.7\%$ — essentially complete shielding.
 
> [!summary] **Final Answers**
>
> - $\boxed{f_{\delta=t}=0.79~\text{MHz}}$  
> - $\boxed{f_{t\ge5\delta}=19.8~\text{MHz}}$ (**effective shielding**)
 ---

> [!code]- MATLAB Solution
> ```matlab
> % Q14 – Minimum frequency for EM shield
> mu0   = 4*pi*1e-7;  % [H/m]
> sigma = 2e4;        % [S/m]
> t     = 4e-3;       % [m]
> 
> % Case 1: δ = t
> f_eq   = 1/(pi*mu0*sigma*t^2);
> 
> % Case 2: t = 5δ (rule of thumb)
> f_rule = 25*f_eq;
> 
> fprintf("Case 1 (δ=t): %.3f MHz\n", f_eq/1e6);
> fprintf("Case 2 (t≥5δ): %.3f MHz\n", f_rule/1e6);
> ```
---

**Note:**  
When $t ≥ 5\delta$, the wave inside the material is attenuated by a factor $e^{-5}$,  
leaving < 1 % of the original field — practically a **Faraday-cage-level shield**.

---
> [!summary] **Question 15 — Total Time-Average Power Incident on a Surface**
>
> **Question:**  
> “A radio wave propagating in vacuum is incident on a surface of size  
> $A = 0.05~\text{m}^2$.  
> The incidence angle (between the wave vector $\vec\beta$ and the surface normal) is  
> $\varphi = 20^\circ$.  
> The electric-field magnitude is $E_0 = 1~\text{V/m}$.  
> What is the **total time-average power** incident on the surface?  
> Express your result in **µW** (not µW/m²).”
>
> ---
>
> **Concept:**  
> The time-average **Poynting vector magnitude** in a plane wave is  
>
> $$
> S_0 = \frac{E_0^2}{2\eta_0}
> $$
>
> where $\eta_0 = 377~\Omega$ is the intrinsic impedance of free space.  
> Only the component **normal** to the surface contributes to the incident power:
>
> $$
> P_i = S_0 A \cos\varphi
> $$
>
> ---
>
> **Given:**
> - $E_0 = 1~\text{V/m}$  
> - $\eta_0 = 377~\Omega$  
> - $A = 0.05~\text{m}^2$  
> - $\varphi = 20^\circ$
>
> ---
>
> **Step-by-Step Calculation:**
>
> 1. Compute the time-average power density:
>    $$
>    S_0 = \frac{E_0^2}{2\eta_0}
>        = \frac{1^2}{2\times377}
>        = 1.326\times10^{-3}\ \text{W/m}^2
>    $$
>
> 2. Find the perpendicular component:
>    $$
>    S_\perp = S_0\cos20^\circ
>             = 1.25\times10^{-3}\ \text{W/m}^2
>    $$
>
> 3. Multiply by area:
>    $$
>    P_i = S_\perp A
>        = (1.25\times10^{-3})(0.05)
>        = 6.25\times10^{-5}\ \text{W}
>    $$
>
> 4. Convert to micro-watts:
>    $$
>    6.25\times10^{-5}\ \text{W} = 62.5~\mu\text{W}
>    $$
>
> ✅ **Answer:** $\boxed{P_i = 62.5~\mu\text{W}}$
>
> ---
>
> **Interpretation:**  
> The incident wave delivers **62.5 µW** of average power to the surface at  
> 20° incidence.  
> The cosine factor accounts for the reduced effective area seen by the wavefront.
>


> [!code]- MATLAB Solution
> ```matlab
> % Q15 – Total time-average power incident on a surface
> E0   = 1;          % [V/m]
> eta0 = 377;        % [ohm]
> A    = 0.05;       % [m^2]
> phi  = deg2rad(20);% [radians]
> 
> % Compute average power
> S0     = E0^2/(2*eta0);   % Average power density [W/m^2]
> S_perp = S0*cos(phi);     % Perpendicular component
> P      = S_perp*A;        % Total incident power [W]
> 
> fprintf("Total Power = %.2f µW\n", P*1e6);
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



