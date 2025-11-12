# 🧭 Electromagnetics – Home Assignment 2  

> 🔗 [[MOC – Electromagnetics]]   
> **Context:** Reflection and transmission at a dielectric boundary (normal incidence, non-magnetic).

> [!info] 🧩 Quick Formula Recap — HA2 (use with $e^{j\omega t}$ convention)
>
> **Intrinsic impedance & refractive index**
> - $\displaystyle \eta=\sqrt{\mu/\varepsilon}=\frac{\eta_0}{\sqrt{\varepsilon_r}}\sqrt{\frac{\mu_r}{1}}$, with $\eta_0\approx377~\Omega$  
> - $\displaystyle n=\sqrt{\varepsilon_r\mu_r}$
>
> **Normal incidence (lossless) — fields at a single interface**
> $$
> \Gamma=\frac{\eta_2-\eta_1}{\eta_2+\eta_1},\qquad
> t=\frac{2\eta_2}{\eta_1+\eta_2}
> $$
> Power coefficients (time-average):
> $$
> R=|\Gamma|^2,\qquad 
> T=\frac{\eta_1}{\eta_2}\,|t|^2=\frac{4\eta_1\eta_2}{(\eta_1+\eta_2)^2},\qquad
> R+T=1
> $$
>
> **Oblique incidence (plane of incidence defined by $\hat\beta$ and $\hat n$)**
> - **Snell:** $\displaystyle n_1\sin\theta_i=n_2\sin\theta_t$
> - **TE (s-pol):**
> $$
> r_{\text{TE}}=\frac{\eta_2\cos\theta_i-\eta_1\cos\theta_t}{\eta_2\cos\theta_i+\eta_1\cos\theta_t},\quad
> t_{\text{TE}}=\frac{2\eta_2\cos\theta_i}{\eta_2\cos\theta_i+\eta_1\cos\theta_t}
> $$
> $$
> R_{\text{TE}}=|r_{\text{TE}}|^2,\qquad
> T_{\text{TE}}=\frac{\eta_1}{\eta_2}\frac{\cos\theta_t}{\cos\theta_i}\,|t_{\text{TE}}|^2
> $$
> - **TM (p-pol):**
> $$
> r_{\text{TM}}=\frac{\eta_1\cos\theta_i-\eta_2\cos\theta_t}{\eta_1\cos\theta_i+\eta_2\cos\theta_t},\quad
> t_{\text{TM}}=\frac{2\eta_2\cos\theta_i}{\eta_1\cos\theta_i+\eta_2\cos\theta_t}
> $$
> $$
> R_{\text{TM}}=|r_{\text{TM}}|^2,\qquad
> T_{\text{TM}}=\frac{\eta_1}{\eta_2}\frac{\cos\theta_t}{\cos\theta_i}\,|t_{\text{TM}}|^2
> $$
>
> **Brewster angle (reflection zero)**
> - For **TM** with $\mu_1=\mu_2$: $\displaystyle \tan\theta_B=\sqrt{\varepsilon_{r2}/\varepsilon_{r1}}$
> - No Brewster zero for **TE** when $\mu_1=\mu_2$.
>
> **Poynting & PEC tip**
> - Time-average power density (lossless): $\displaystyle \langle S\rangle=\frac{|E_0|^2}{2\eta}=\frac{\eta\,|H_0|^2}{2}$ (peak); or $\langle S\rangle=\dfrac{E_{\rm rms}^2}{\eta}=\eta H_{\rm rms}^2$ (RMS).  
> - PEC at normal incidence: $\Gamma=-1$ → **standing wave** in medium 1 → $\langle \mathbf S_\text{tot}\rangle=0$.
>
> **Electrostatics mini**
> - Coulomb: $\displaystyle \mathbf F_{12}=k\,\frac{q_1q_2}{r^3}\,\mathbf r,\quad k=8.988\times10^9~\text{N·m}^2/\text{C}^2$  
> - Collinear 1D force (on $q$ at $x$ from $Q$ at $x_i$): $\displaystyle F_x=k\,qQ\,\frac{x-x_i}{|x-x_i|^3}$  
> - Superposition: $F_{\text{net}}=\sum_i F_i$  
> - Units: $1~\text{aC}=10^{-18}$ C, $1~\text{nm}=10^{-9}$ m
>
> **Orientation reminders**
> - TE: $\mathbf E\perp$ plane of incidence; TM: $\mathbf H\perp$ plane.  
> - Wave triad (lossless plane wave): $\hat\beta,\ \mathbf E,\ \mathbf H$ are mutually orthogonal; $\mathbf E=-\eta(\hat\beta\times\mathbf H)$.
>
> **Quick sanity checks 🧪**
> - Lossless interface: $R+T=1$ (use power forms).  
> - Entering higher $n$ → ray bends **toward** the normal ($\theta_t<\theta_i$).  
> - Symmetry often ⇒ zero net force (but verify magnitudes).

---
> [!info] **Section 1 — Normal Incidence Concepts (Q1–Q3)**

> [!summary] **Question 1 — Range of $t$ when $\varepsilon_{r1}>\varepsilon_{r2}$**
>
> **Question:**  
> For normal incidence between two non-magnetic dielectrics, if $\varepsilon_{r1}>\varepsilon_{r2}$, what range does the **field transmission coefficient** $t$ fall into?
>
> 💡 **Concept**  
> - Intrinsic impedance: $\displaystyle \eta=\frac{\eta_0}{\sqrt{\varepsilon_r}}$  
> - Larger $\varepsilon_r$ → smaller $\eta$  
> - Transmission coefficient (field):  
>   $$
>   t=\frac{2\eta_2}{\eta_1+\eta_2}
>   $$
>
> 🧮 **Derivation**  
> Since $\varepsilon_{r1}>\varepsilon_{r2}$ ⇒ $\eta_1<\eta_2$, the denominator is smaller than $2\eta_2$ but larger than $\eta_2$:  
> $$
> 1<t=\frac{2\eta_2}{\eta_1+\eta_2}<2
> $$
>
> ✅ **Answer:** $\boxed{1<t<2}$
>
> 🧩 **Interpretation:**  
> When the wave exits a “tighter” (high-$\varepsilon_r$) medium into a “looser” one, the **electric field amplitude** slightly increases at the boundary ($t>1$), but the **power transmission** still stays below 100 % due to the impedance ratio.

> [!code]- MATLAB — Reusable Template (Transmission Coefficient Range)
> ```matlab
> 
> eta = @(er) 377./sqrt(er);
> t = @(er1,er2) 2*eta(er2)./(eta(er1)+eta(er2));
> t(9,1) % -> 1.5 (1 < t < 2 ✅)
> t(1,9) % -> 0.666... (0 < t < 1 ✅)
> ```

> [!warning] ⚠️ **Gotchas**
> - Don’t confuse **field coefficient $t$** with **power coefficient $T$**.  
> - $t>1$ doesn’t mean more than 100 % power passes.  
> - This only holds for **lossless**, **non-magnetic** media.

---

> [!summary] **Question 2 — Range of $t$ when $\varepsilon_{r1}<\varepsilon_{r2}$**
>
> **Question:**  
> For normal incidence between two dielectrics, if $\varepsilon_{r1}<\varepsilon_{r2}$, what range does $t$ fall into?
>
> 💡 **Concept**  
> - Smaller $\varepsilon_r$ → larger $\eta$.  
> - $\eta_1>\eta_2$ for this case.
>
> 🧮 **Derivation**
> $$
> t=\frac{2\eta_2}{\eta_1+\eta_2},\quad \eta_1>\eta_2>0
> \Rightarrow 0<t<1
> $$
>
> ✅ **Answer:** $\boxed{0<t<1}$
>
> 🧩 **Interpretation:**  
> Entering a “tighter” medium ($\eta_2<\eta_1$) reduces the field amplitude at the interface ($t<1$), even though a finite fraction of **power** still transmits.

> [!warning] ⚠️ **Gotchas**
> - Again, $t$ is a **field ratio**, not a power ratio.  
> - For lossy media or magnetic contrasts, this simple bound no longer holds.

---

> [!summary] **Question 3 — PEC Boundary (Standing-Wave Power Flow)**
>
> **Question:**  
> If medium 2 is a perfect electric conductor (PEC), what is the **time-average Poynting vector** in medium 1?
>
> 💡 **Concept**  
> - Boundary condition: $E_t=0$ at PEC → $\Gamma=-1$.  
> - Total field in medium 1 = incident + reflected.
>
> 🧮 **Derivation**
> $$
> E_\text{tot}(y)=E_0(e^{-j\beta y}-e^{+j\beta y})=-2jE_0\sin(\beta y)
> $$
> The instantaneous fields form a **standing wave**.  
> Time-averaged real power flow $\langle \mathbf S_\text{tot}\rangle$ is zero, since equal forward and backward power components cancel.
>
> ✅ **Answer:** $\boxed{\langle\mathbf S_\text{tot}\rangle=0}$
>
> 🧩 **Interpretation:**  
> The fields store energy alternately in electric and magnetic form, but no **net energy transport** occurs toward the PEC — all incident power is reflected.

> [!code]- MATLAB — Reusable Standing-Wave Check
> ```matlab
> y = linspace(0,pi,500);
> E0 = 1; beta = 1;
> Etot = E0*(exp(-1j*beta*y) - exp(1j*beta*y));
> S_avg = mean(real(Etot.*conj(Etot)));  % ≈0 for standing wave
> plot(y,real(Etot)), title('Standing-wave pattern, PEC boundary')
> ```

> [!warning] ⚠️ **Gotchas**
> - Don’t confuse **instantaneous** $\mathbf S$ with its **time average**.  
> - For a finite-conductivity metal, $\Gamma\approx-1$ but $\langle\mathbf S\rangle\neq0$ → tiny absorption.  
> - The $\sin(\beta y)$ form indicates **voltage nodes** at the conductor surface.

---
> [!info] **Section 2 — Normal Incidence (Numeric) (Q4–Q6)**

> [!summary] **Question 4 — Type of Incidence**
>
> **Question:**  
> Determine the **incidence type** of the given plane wave:
> $$
> \tilde{\mathbf E}=
> \begin{bmatrix}4\\0\\j4\end{bmatrix}
> e^{-j(2~\text{m}^{-1})y}\ \text{V/m}
> $$
> propagating toward a boundary at $y=0$.
>
> 💡 **Concept**  
> If the exponential phase factor depends only on the coordinate **normal to the boundary**, the propagation is **normal incidence**.
>
> 🧮 **Derivation**  
> Here the phase term $e^{-j(2y)}$ varies only with $y$, which is perpendicular to the interface at $y=0$.  
> There is **no tangential component** of $\vec\beta$ → no refraction.
>
> ✅ **Answer:** $\boxed{\text{Normal incidence}}$
>
> 🧩 **Interpretation:**  
> This wave strikes the boundary head-on. The direction of $\vec\beta$ (phase propagation) is exactly perpendicular to the interface, so Snell’s law is trivial ($\theta_i=\theta_t=0$).

> [!warning] ⚠️ **Gotchas**
> - Don’t assume all $e^{-j\beta y}$ forms are normal → check the boundary’s orientation.  
> - The sign in $e^{\pm j\beta y}$ only indicates direction (toward ± $y$).

---
> [!summary] **Question 5 — Reflected Power (Percent)**
>
> **Question:**  
> A plane wave in a dielectric ($\varepsilon_r = 12,\ \mu_r = 1$) hits vacuum at normal incidence.  
> Find the **reflected power percentage**.
>
> 💡 **Concept**  
> For **normal incidence** between lossless, non-magnetic dielectrics:
> $$
> \Gamma = \frac{\eta_2 - \eta_1}{\eta_2 + \eta_1},\qquad
> R = |\Gamma|^2,
> $$
> with $\eta = \dfrac{\eta_0}{\sqrt{\varepsilon_r}}$ and $\eta_0 = 377~\Omega$.
>
> 🧮 **Derivation**
>
> 1️⃣ Intrinsic impedances  
> $$
> \eta_1 = \frac{377}{\sqrt{12}} = 108.83~\Omega,\qquad
> \eta_2 = 377~\Omega
> $$
>
> 2️⃣ Field reflection coefficient  
> $$
> \Gamma = \frac{377 - 108.83}{377 + 108.83} = 0.5520
> $$
>
> 3️⃣ Power reflection coefficient  
> $$
> R = \Gamma^2 = (0.5520)^2 = 0.3047 \Rightarrow 30.47\%.
> $$
>
> ✅ **Answer:** $\boxed{R = 30.5\%}$
>
> 🧩 **Interpretation:**  
> The high-$\varepsilon_r$ medium has a low impedance ($108.8~\Omega$) versus free space ($377~\Omega$).  
> That **impedance mismatch** causes about **30 %** of the incident power to bounce back, leaving  
> roughly **70 %** transmitted.  
> Remember: even if the **field** transmission $t>1$, **power** stays ≤ 100 % because power scales with both field amplitude and impedance.

> [!code]- MATLAB — Minimal (reusable)
> ```matlab
> eps_r1 = 12;  eps_r2 = 1;          % relative permittivities
> eta0   = 377;                      % [Ω] free-space impedance
> eta1   = eta0/sqrt(eps_r1);
> eta2   = eta0/sqrt(eps_r2);
> Gamma  = (eta2 - eta1)/(eta2 + eta1);   % field reflection
> R      = abs(Gamma)^2;                  % power reflection
> T      = 1 - R;                         % power transmission (lossless)
> fprintf('η1=%.2f Ω, η2=%.2f Ω\n', eta1, eta2);
> fprintf('Γ=%.4f  |  R=%.4f (%.2f%%)  T=%.4f (%.2f%%)  R+T=%.4f\n', ...
>         Gamma, R, 100*R, T, 100*T, R+T);
> ```

> 🧪 **Sanity checks**
> - If $\varepsilon_{r1} = \varepsilon_{r2} = 1$ → $\eta_1 = \eta_2$ → $\Gamma = 0$ → $R = 0$.  
> - If $\varepsilon_{r1} \to \infty$ → $\eta_1 \to 0$ → $\Gamma \to 1$ → $R \to 1$.  
> - Equivalent form using refractive index $n = \sqrt{\varepsilon_r\mu_r}$:
>   $$
>   \Gamma = \frac{n_1 - n_2}{n_1 + n_2}, \quad
>   R = \left(\frac{n_1 - n_2}{n_1 + n_2}\right)^2
>   $$

> [!warning] ⚠️ **Gotchas**
> - Use **$\eta$**, not $n$, in the impedance-based formula for $R$ and $T$.  
> - $\Gamma$ is a **field ratio**, dimensionless.  
> - Its **sign** matters for phase (interference), but not for power $R = |\Gamma|^2$.

> [!summary] **Question 6 — Transmitted Power (Percent)**
>
> **Question:**  
> Continue from Q5 — find the **transmitted power percentage** for a wave going from $\varepsilon_{r1}=12$ into vacuum at **normal incidence**.
>
> 💡 **Concept**  
> For **lossless**, **non-magnetic** media at normal incidence:
> $$
> T=\frac{4\eta_1\eta_2}{(\eta_1+\eta_2)^2}=1-R,\qquad
> \eta=\frac{\eta_0}{\sqrt{\varepsilon_r}},\ \eta_0=377~\Omega.
> $$
>
> 🧮 **Derivation**
> $$
> \eta_1=\frac{377}{\sqrt{12}}=108.83~\Omega,\quad
> \eta_2=377~\Omega
> $$
> $$
> T=\frac{4(108.83)(377)}{(108.83+377)^2}=0.6953
> \Rightarrow T=69.5\%.
> $$
>
> ✅ **Answer:** $\boxed{T=69.5\%}$
>
> 🧩 **Interpretation:**  
> Field transmission can exceed $1$ when going to a **higher impedance** medium, but **power** transmission can’t — it’s weighted by impedance. For lossless interfaces $R+T=1$, so your reflected and transmitted powers always balance.  

> [!code]- MATLAB — Live Script–Ready (with optional batch “toggle”)
> ```matlab
> %% === Q6 — Transmitted Power (Normal Incidence, Lossless, μr=1) ===
> % Runs cleanly in a Live Script cell. Edit eps_r1/eps_r2 and re-run.
> % Includes an optional batch section you can toggle with RUN_BATCH.
> 
> % ---------- USER INPUT ----------
> eps_r1   = 12;     % medium 1 relative permittivity
> eps_r2   = 1;      % medium 2 relative permittivity (vacuum)
> eta0     = 377;    % [Ω] free-space impedance
> RUN_PLOT = true;   % quick plot of R/T vs eps_r2
> RUN_BATCH = true;  % toggle: run a batch of common material pairs
> 
> % ---------- CORE CALC ----------
> eta1 = eta0 / sqrt(eps_r1);
> eta2 = eta0 / sqrt(eps_r2);
> 
> Gamma = (eta2 - eta1) / (eta2 + eta1);     % field reflection
> R = abs(Gamma)^2;                           % power reflection
> T = (4*eta1*eta2) / (eta1 + eta2)^2;       % power transmission
> 
> fprintf('\n=== Normal-Incidence Power Coefficients ===\n');
> fprintf('eps_r1 = %.4g,  eps_r2 = %.4g\n', eps_r1, eps_r2);
> fprintf('η1 = %.2f Ω,  η2 = %.2f Ω\n', eta1, eta2);
> fprintf('Γ  = %.4f  (field reflection)\n', Gamma);
> fprintf('R  = %.4f  (%.2f%%)\n', R, 100*R);
> fprintf('T  = %.4f  (%.2f%%)\n', T, 100*T);
> fprintf('R + T = %.4f  (energy check)\n\n', R+T);
> 
> % ---------- OPTIONAL PLOT: R & T vs eps_r2 ----------
> if RUN_PLOT
>     eps_r2_vec = linspace(1, 20, 200);
>     eta2_vec   = eta0 ./ sqrt(eps_r2_vec);
>     T_vec = (4*eta1.*eta2_vec) ./ (eta1 + eta2_vec).^2;
>     R_vec = 1 - T_vec;
> 
>     figure; hold on; grid on; box on;
>     plot(eps_r2_vec, 100*T_vec, 'LineWidth', 1.6);
>     plot(eps_r2_vec, 100*R_vec, '--', 'LineWidth', 1.4);
>     xlabel('\epsilon_{r2}');
>     ylabel('Power Coefficient [%]');
>     title(sprintf('Normal-Incidence Power vs. \\epsilon_{r2} (\\epsilon_{r1}=%.3g)', eps_r1));
>     legend('T (%)','R (%)','Location','best');
> end
> 
> % ---------- OPTIONAL BATCH: Common pairs (toggle with RUN_BATCH) ----------
> if RUN_BATCH
>     % Define some typical pairs (μr=1 for all)
>     pairs = [ ...
>         1,   1;    % air -> air (sanity: R=0, T=1)
>         12,  1;    % high-er -> vacuum (your Q5/Q6 case)
>         2.25,1;    % glass-ish -> vacuum
>         1,   4;    % air -> εr=4 (PTFE/PTFE-like)
>         4,   1;    % εr=4 -> vacuum
>         9,   1;    % εr=9 -> vacuum
>         1,  12;    % air -> εr=12
>     ];
>     labels = { ...
>         'air→air', 'εr=12→vac', 'εr≈2.25→vac', ...
>         'air→εr=4', 'εr=4→vac', 'εr=9→vac', 'air→εr=12' };
> 
>     fprintf('=== Batch Results (μr=1, normal incidence) ===\n');
>     fprintf('%-12s  %8s  %8s  %10s  %10s\n', 'Pair', 'R(%)', 'T(%)', 'eta1(Ω)', 'eta2(Ω)');
>     for k = 1:size(pairs,1)
>         er1k = pairs(k,1); er2k = pairs(k,2);
>         e1 = eta0/sqrt(er1k); e2 = eta0/sqrt(er2k);
>         Gk = (e2 - e1) / (e2 + e1);
>         Rk = abs(Gk)^2;
>         Tk = (4*e1*e2) / (e1 + e2)^2;
>         fprintf('%-12s  %8.2f  %8.2f  %10.2f  %10.2f\n', labels{k}, 100*Rk, 100*Tk, e1, e2);
>     end
>     fprintf('\n');
> end
> ```

> [!warning] ⚠️ **Gotchas**
> - Always use **power** formulas when reporting $R$ and $T$.  
> - $t$ (field) and $T$ (power) differ by impedance ratios.  
> - $R + T = 1$ only holds for **lossless** boundaries; if $\sigma > 0$, part of the energy is absorbed.


---
> [!info] **Section 3 — Oblique Incidence (TE Case) (Q7–Q9)**  
> Medium 1: $\varepsilon_{r1}=2,\ \mu_{r1}=2$; Medium 2: $\varepsilon_{r2}=20,\ \mu_{r2}=1$  
> $\hat\beta=(0.6,-0.8,0)$, $\hat n=(3/\sqrt{10},-1/\sqrt{10},0)$.

> [!summary] **Question 7 — Incidence Type and Polarization (TE/TM)**
>
> **Question:**  
> Determine the **type of incidence** (normal/oblique) and the **polarization** (TE or TM) for the given fields, with
> $\hat\beta=(0.6,-0.8,0)$ and interface normal $\hat n=\bigl(\tfrac{3}{\sqrt{10}},-\tfrac{1}{\sqrt{10}},0\bigr)$.
>
> 💡 **Concept**  
> - The **plane of incidence** is the plane spanned by $\hat\beta$ and $\hat n$.  
> - If $\hat\beta \nparallel \hat n$ → **oblique** incidence (otherwise normal).  
> - For a plane wave: $\tilde{\mathbf E} = -\,\eta\,(\hat\beta \times \tilde{\mathbf H})$.  
>   The **TE** case has $\tilde{\mathbf E}$ **perpendicular** to the plane of incidence;  
>   the **TM** case has $\tilde{\mathbf H}$ **perpendicular** to that plane.
>
> 🧮 **Derivation**  
> 1) Incidence type:  
>    $$
>    \hat\beta\cdot\hat n = 0.6\cdot\frac{3}{\sqrt{10}} + (-0.8)\cdot\frac{-1}{\sqrt{10}}
>    = \frac{1.8+0.8}{\sqrt{10}} = \frac{2.6}{\sqrt{10}} \neq \pm 1
>    $$
>    Since $\hat\beta$ is **not** parallel to $\hat n$, the incidence is **oblique**.  
>
> 2) Polarization via $\hat\beta\times\tilde{\mathbf H}$:  
>    With $\tilde{\mathbf H}=(H_x,H_y,0)$ (as given on the slide),  
>    $$
>    \hat\beta\times\tilde{\mathbf H}
>    =\begin{vmatrix}
>    \hat x & \hat y & \hat z\\
>    0.6 & -0.8 & 0\\
>    H_x & H_y & 0
>    \end{vmatrix}
>    =(0,\,0,\,0.6H_y+0.8H_x)\ \parallel\ \hat z.
>    $$
>    Hence $\tilde{\mathbf E}\parallel \hat z$.  
>    The plane of incidence is the $xy$-plane (it contains both $\hat\beta$ and $\hat n$, which are $z$-free), so $\tilde{\mathbf E}\perp$ plane of incidence ⇒ **TE**.
>
> ✅ **Answer:** $\boxed{\text{Oblique incidence with TE polarization}}$
>
> 🧩 **Interpretation:**  
> Because both $\hat\beta$ and $\hat n$ live in the $xy$-plane, the incidence plane is $xy$.  
> The computed $\tilde{\mathbf E}$ points along $z$, i.e., **perpendicular** to that plane → **TE**.  
> This choice determines you must use the **TE Fresnel** formulas downstream (e.g., in Q9).

> [!code]- MATLAB — Live Script–Ready TE/TM Classifier (reusable)
> ```matlab
> %% Q7 — Incidence Type & Polarization (TE/TM) — Live Script Cell
> % Inputs (edit these as needed)
> beta_hat = [0.6; -0.8; 0];                % propagation unit vector
> n_hat    = [3/sqrt(10); -1/sqrt(10); 0];  % interface unit normal
> Hb       = [4-1j*8; 3-1j*6; 0];           % example H phasor (units arbitrary)
> 
> % Normalize to be safe (in case inputs drift)
> beta_hat = beta_hat / norm(beta_hat);
> n_hat    = n_hat   / norm(n_hat);
> 
> % 1) Incidence type
> cos_inc = dot(beta_hat, n_hat);
> is_normal  = abs(abs(cos_inc) - 1) < 1e-12;
> incidence  = "oblique";
> if is_normal, incidence = "normal"; end
> 
> % 2) Build an orthonormal basis for the plane of incidence
> %    plane is spanned by n_hat and the tangential component of beta_hat
> beta_tan = beta_hat - dot(beta_hat, n_hat)*n_hat;
> if norm(beta_tan) < 1e-12
>     % normal incidence: plane of incidence is undefined; any transverse dir works
>     % we'll pick an arbitrary transverse unit vector orthogonal to n_hat
>     tmp = [1;0;0]; if abs(dot(tmp,n_hat))>0.9, tmp=[0;1;0]; end
>     t1 = tmp - dot(tmp,n_hat)*n_hat;  t1 = t1/norm(t1);
>     t2 = cross(n_hat, t1);            t2 = t2/norm(t2);
> else
>     t1 = beta_tan / norm(beta_tan);   % in-plane, along β's tangential part
>     t2 = cross(n_hat, t1);            % completes the in-plane basis
> end
> 
> % 3) E direction from β × H (phasor relation)
> E_dir = cross(beta_hat, Hb);           % ∝ E (up to impedance & scaling)
> 
> % 4) Classify TE/TM by testing E_dir against the plane of incidence
> %    - If E_dir ⟂ plane (i.e., parallel to n_hat × t1 == t2_out_of_plane) → TE
> %    - If H is ⟂ plane (≈ dot(Hb, t2_out_of_plane) ≠ 0 & E in-plane) → TM
> plane_normal = cross(beta_hat, n_hat);    % normal to the incidence plane
> if norm(plane_normal) < 1e-12
>     % Degenerate: normal incidence → TE/TM labels become conventional (choose any)
>     pol = "undefined at strictly normal incidence (choose TE/TM by field orientation)";
> else
>     plane_normal = plane_normal / norm(plane_normal);
>     % Component of E_dir along plane normal (perpendicular to the plane)
>     E_perp = abs(dot(E_dir, plane_normal));
>     % Component of H along plane normal (use Hb directly)
>     H_perp = abs(dot(Hb, plane_normal));
>     if E_perp > 1e-9 && H_perp < 1e-9
>         pol = "TE";
>     elseif H_perp > 1e-9 && E_perp < 1e-9
>         pol = "TM";
>     else
>         pol = "mixed / numerical (check inputs)";
>     end
> end
> 
> % 5) Report
> fprintf('Incidence: %s (cosθ_i = %.4f)\n', incidence, cos_inc);
> fprintf('Classification: %s\n', pol);
> fprintf('E direction (β×H): [% .3f%+.3fj  % .3f%+.3fj  % .3f%+.3fj]\n', ...
>     real(E_dir(1)), imag(E_dir(1)), real(E_dir(2)), imag(E_dir(2)), real(E_dir(3)), imag(E_dir(3)));
> 
> % Quick sanity display: E should be ~⊥ plane for TE
> % Project E_dir onto plane normal and plane itself:
> E_perp_vec  = dot(E_dir, plane_normal)*plane_normal;
> E_inplane   = E_dir - E_perp_vec;
> fprintf('||E_perp|| = %.3e,  ||E_inplane|| = %.3e\n', norm(E_perp_vec), norm(E_inplane));
> ```
>

> [!warning] ⚠️ **Gotchas**
> - TE = **E ⟂ incidence plane**, TM = **H ⟂ incidence plane**.  
> - Always define the plane of incidence first (from $\hat\beta$ and $\hat n$).  
> - The cross product order matters: $\mathbf E\propto\hat\beta\times\mathbf H$ (not the reverse).

---
> [!summary] **Question 8 — Transmission Angle $\theta_t$**
>
> **Question:**  
> Calculate the **refraction angle** $\theta_t$ for the transmitted wave.
>
> 💡 **Concept**  
> Apply **Snell’s law**:
> $$
> n_1\sin\theta_i=n_2\sin\theta_t,\qquad
> n_i=\sqrt{\varepsilon_{ri}\mu_{ri}}.
> $$
>
> 🧮 **Derivation (exact, with 4-dp outputs)**  
> Incident angle from geometry:
> $$
> \cos\theta_i=\hat\beta\cdot\hat n
> =0.6\cdot\frac{3}{\sqrt{10}}+(-0.8)\cdot\frac{-1}{\sqrt{10}}
> =\frac{2.6}{\sqrt{10}}=0.82219219\ldots
> $$
> $$
> \theta_i=\arccos\!\left(\tfrac{2.6}{\sqrt{10}}\right)=\boxed{34.6952^\circ}.
> $$
> Refractive indices:
> $$
> n_1=\sqrt{2\cdot2}=2.0000,\qquad n_2=\sqrt{20\cdot1}=4.4721.
> $$
> Snell’s law:
> $$
> \sin\theta_t=\frac{n_1}{n_2}\sin\theta_i
> =\frac{2}{\sqrt{20}}\sin(34.6952^\circ)=0.25455844\ldots
> $$
> $$
> \theta_t=\arcsin(0.25455844\ldots)=\boxed{14.7474^\circ}.
> $$
>
> ✅ **Answer:** $\boxed{\theta_t=14.7474^\circ}$
>
> 🧩 **Interpretation:**  
> Since $n_2>n_1$ (higher permittivity on transmission), the ray **bends toward the normal** ($\theta_t<\theta_i$), exactly as Snell says. Clean, consistent, no TIR risk because $\sin\theta_t<1$. ✨

> [!code]- MATLAB — Reusable Snell’s Law Check (prints 4 dp)
> ```matlab
> %% Q8 — Transmission angle (θ_t) with 4-decimal outputs
> beta_hat = [0.6; -0.8; 0];
> n_hat    = [3/sqrt(10); -1/sqrt(10); 0];
> 
> % Refractive indices (εr1=2, μr1=2) → n1=2; (εr2=20, μr2=1) → n2=sqrt(20)
> n1 = sqrt(2*2);
> n2 = sqrt(20*1);
> 
> % Exact cosθ_i from vectors (avoid rounding intermediates)
> cos_th_i = dot(beta_hat/norm(beta_hat), n_hat/norm(n_hat));
> th_i = acos(cos_th_i);                 % radians
> th_t = asin((n1/n2)*sin(th_i));        % radians
> 
> fprintf('cos(theta_i) = %.8f\n', cos_th_i);
> fprintf('theta_i      = %.4f deg\n', th_i*180/pi);
> fprintf('n1 = %.4f, n2 = %.4f\n', n1, n2);
> fprintf('theta_t      = %.4f deg\n', th_t*180/pi);
> ```

> [!warning] ⚠️ **Gotchas**
> - Use **$n=\sqrt{\varepsilon_r\mu_r}$**, not impedance, for Snell’s law.  
> - Keep everything in **radians** inside MATLAB trig; format with `%.4f` only at print time to lock 4-dp answers.  
> - If `n_1>n_2` and $\theta_i$ is large, check for **TIR** via $\sin\theta_t>1$.

---

> [!summary] **Question 9 — Transmitted Power (TE, Percent)**
>
> **Question:**  
> Compute the **transmitted power coefficient** $T_{\text{TE}}$ for the given parameters.
>
> 💡 **Concept (TE Fresnel):**  
> For oblique TE incidence:
> $$
> t_{\text{TE}}=\frac{2\eta_2\cos\theta_i}{\eta_2\cos\theta_i+\eta_1\cos\theta_t},\qquad
> T_{\text{TE}}=\frac{\eta_1}{\eta_2}\frac{\cos\theta_t}{\cos\theta_i}|t_{\text{TE}}|^2
> $$
>
> 🧮 **Derivation**  
> Using: $\eta_1=377~\Omega$, $\eta_2=84.30~\Omega$,  
> $\cos\theta_i=0.82219$, $\cos\theta_t=0.96798$
> $$
> t_\text{TE}=\frac{2(84.30)(0.8222)}{84.30(0.8222)+377(0.9680)}=0.3195
> $$
> $$
> T_\text{TE}=\frac{377}{84.30}\frac{0.9680}{0.8222}(0.3195)^2=0.537
> $$
>
> ✅ **Answer:** $\boxed{T_{\text{TE}}=53.6882\%}$
>
> 🧩 **Interpretation:**  
> Just over half the incident power transmits into the second medium.  
> TE polarization generally reflects **more** than TM for high-$\varepsilon$ contrasts because $E_\parallel$ must stay continuous, reducing transmitted field strength.

> [!code]- MATLAB — Reusable Fresnel TE Power
> ```matlab
> eta1 = 377; eta2 = 84.3;
> th_i = deg2rad(34.70); th_t = deg2rad(14.75);
> tTE = (2*eta2*cos(th_i))/(eta2*cos(th_i)+eta1*cos(th_t));
> TTE = (eta1/eta2)*(cos(th_t)/cos(th_i))*abs(tTE)^2;
> fprintf("TE Transmission = %.4f%%\n", 100*TTE);
> ```

> [!warning] ⚠️ **Gotchas**
> - **TE** and **TM** formulas are different; mixing them is a classic exam trap.  
> - Check which cosine ($\theta_i$ or $\theta_t$) belongs where in $t_{\text{TE}}$.  
> - Always ensure $R+T\approx1$ for lossless interfaces — a good sanity check.
---


---
> [!info] **Section 4 — Brewster (Ground Reflection Cancellation) (Q10–Q11)**  
> Medium 1 (air): $\varepsilon_{r1}=1,\ \mu_{r1}=1$ · Medium 2 (ground): $\varepsilon_{r2}=10,\ \mu_{r2}=1$


> [!summary] **Question 10 — Which polarization cancels the reflection?**
>
> **Question:**  
> For a transmitter–ground–receiver geometry in which the ground-reflected ray should **vanish**, which incidence **polarization** and **type** must be used at the air–ground interface?
>
> 💡 **Concept**  
> - **Brewster angle** exists (for non-magnetic media, $\mu_1=\mu_2$) **only for TM** (p-polarization).  
> - At the Brewster angle $\theta_B$, the TM reflection coefficient is zero: $\Gamma_{\text{TM}}(\theta_B)=0$.
>
> 🧮 **Derivation (qualitative)**  
> For TM, the boundary conditions on $E_\parallel$ and $H_\parallel$ allow the reflected and transmitted field orientations to become **orthogonal** at a specific $\theta_B$, forcing the reflected TM component to zero. TE does not permit this zero for equal permeabilities.
>
> ✅ **Answer:** $\boxed{\text{Oblique incidence with TM (p-) polarization}}$
>
> 🧩 **Interpretation:**  
> Aligning the link so that the **ray hits the ground at TM Brewster** removes the reflected ray in the receiver path — a classic technique to mitigate multipath fading over dielectric ground.

> [!warning] ⚠️ **Gotchas**
> - TE (s-pol) does **not** have a Brewster zero when $\mu_1=\mu_2$.  
> - Don’t mix “Brewster” with “critical angle”: **Brewster** is for zero **reflection** (TM); **critical** angle is for onset of **TIR** (from high index to low).  
> - Brewster requires **oblique** incidence; there’s no Brewster at normal incidence.

---

> [!summary] **Question 11 — Required incidence angle (degrees)**
>
> **Question:**  
> Compute the **Brewster angle** $\theta_B$ (in degrees) for the air–ground interface with $\varepsilon_{r2}=10$ and $\mu_{r1}=\mu_{r2}=1$.
>
> 💡 **Concept (TM Brewster, non-magnetic)**  
> For $\mu_1=\mu_2$:
> $$
> \tan\theta_B=\sqrt{\frac{\varepsilon_{r2}}{\varepsilon_{r1}}}
> $$
>
> 🧮 **Derivation**
> $$
> \tan\theta_B=\sqrt{\frac{10}{1}}=\sqrt{10}
> \quad\Rightarrow\quad
> \theta_B=\arctan(\sqrt{10})=72.65^\circ
> $$
>
> ✅ **Answer:** $\boxed{72.4516^\circ}$
>
> 🧩 **Interpretation:**  
> A **large permittivity contrast** ($\varepsilon_{r2}=10$) pushes the Brewster angle high. In practice, small losses or surface roughness will yield a **small but nonzero** reflected TM component — still near-minimal around $\theta_B$.

> [!code]- MATLAB — Reusable Brewster (TM, non-magnetic)
> ```matlab
> eps1 = 1;    % air
> eps2 = 10;   % ground
> thetaB_deg = atan(sqrt(eps2/eps1))*180/pi;
> fprintf("TM Brewster angle = %.2f°\n", thetaB_deg);
> ```

> [!warning] ⚠️ **Gotchas**
> - This closed-form only holds when $\mu_1=\mu_2$. If $\mu$ differs, use full Fresnel expressions and solve $\Gamma_{\text{TM}}(\theta)=0$ numerically.  
> - Brewster is defined for the **incident** angle in the **first medium** (air).  
> - At $\theta_B$, **TM** reflection is zero, but **TE** reflection is not.

---

> [!info] **Section 5 — Electrostatics: Three Collinear Charges (Q12–Q13)**  
> Geometry: three point charges on the $x$-axis, spacing $d=10~\text{nm}=1\times10^{-8}\,\text{m}$; force on $Q_2$ toward $+x$ taken as positive.


> [!summary] **Question 12 — $Q_1=Q_3=-5~\text{aC},\; Q_2=-10~\text{aC}$**
>
> **Question:**  
> Find the **$x$-component of the force** on $Q_2$ (in nN).
>
> 💡 **Concept**  
> Coulomb’s law magnitude between neighbors: $F=\dfrac{k\,|Q_iQ_j|}{r^2}$.  
> All three charges are **negative**, so each neighbor **repels** $Q_2$; geometry sets directions.
>
> 🧮 **Derivation**  
> One neighbor’s magnitude:
> $$
> F_\text{one}
> =k\frac{(5\times10^{-18})(10\times10^{-18})}{(10^{-8})^2}
> =4.49~\text{nN}.
> $$
> Directions:  
> • $Q_1$ (left) repels $Q_2$ to the **right** → $+4.49$ nN.  
> • $Q_3$ (right) repels $Q_2$ to the **left** → $-4.49$ nN.  
> Net:
> $$
> F_x=+4.49-4.49=0.
> $$
>
> ✅ **Answer:** $\boxed{0~\text{nN}}$
>
> 🧩 **Interpretation:**  
> Perfect symmetry (equal charges placed symmetrically) gives **zero net force** on the middle charge, even though each pairwise interaction is nonzero.

> [!code]- MATLAB — Reusable Three-Charge Line (Signed 1D Force)
> ```matlab
> % Positions: Q1 at x=-d, Q2 at x=0, Q3 at x=+d
> k  = 8.988e9;       % N·m^2/C^2
> d  = 1e-8;          % m
> Q1 = -5e-18; Q2 = -10e-18; Q3 = -5e-18;   % C
> xi = [-d, +d]; Qi = [Q1, Q3];
> Fx = 0;
> for i = 1:2
>     r = 0 - xi(i);                      % vector from Qi to Q2 (signed)
>     Fx = Fx + k*Q2*Qi(i) * (r) / abs(r)^3;  % 1D form of k Q2 Qi (r)/|r|^3
> end
> fprintf("Fx on Q2 = %.2f nN\n", 1e9*Fx);    % → 0.00 nN
> ```

> [!warning] ⚠️ **Gotchas**
> - Keep **direction** straight: use the vector form $kQ_2Q_i\,(x_2-x_i)/|x_2-x_i|^3$ in 1D to avoid sign slips.  
> - Symmetry can shortcut the algebra — but always verify magnitudes match.  
> - Watch units: aC → C, nm → m.

---

> [!summary] **Question 13 — $Q_1=-3~\text{aC},\; Q_3=+3~\text{aC},\; Q_2=-10~\text{aC}$**
>
> **Question:**  
> Find the **$x$-component of the force** on $Q_2$ (in nN).
>
> 💡 **Concept**  
> Like charges **repel**, unlike **attract**. With $Q_2<0$:  
> • $Q_1=-3$ aC (like) → **repulsion** → force on $Q_2$ toward **$+x$**.  
> • $Q_3=+3$ aC (unlike) → **attraction** → force on $Q_2$ toward **$+x$**.  
> Both contributions point right.
>
> 🧮 **Derivation**  
> One-side magnitude:
> $$
> F_\text{one}
> =k\frac{(3\times10^{-18})(10\times10^{-18})}{(10^{-8})^2}
> =2.70~\text{nN}.
> $$
> Both sides add:
> $$
> F_x=2F_\text{one}=5.40~\text{nN}.
> $$
>
> ✅ **Answer:** $\boxed{+5.4~\text{nN}}$
>
> 🧩 **Interpretation:**  
> Repulsion from the left and attraction from the right **both push right**, so the forces add, doubling the single-side magnitude.

> [!code]- MATLAB — Same Helper (New Charges)
> ```matlab
> k  = 8.988e9; d = 1e-8;
> Q1 = -3e-18; Q2 = -10e-18; Q3 = +3e-18;
> xi = [-d, +d]; Qi = [Q1, Q3];
> Fx = 0;
> for i = 1:2
>     r = 0 - xi(i);                          % r = x2 - xi
>     Fx = Fx + k*Q2*Qi(i) * (r) / abs(r)^3;  % signed 1D Coulomb force
> end
> fprintf("Fx on Q2 = %.2f nN\n", 1e9*Fx);    % → +5.40 nN
> ```

> [!warning] ⚠️ **Gotchas**
> - Don’t “hand-assign” directions; let the vector form set signs automatically.  
> - Confirm that the two contributions point the **same way** before summing.  
> - The $r^2$ (or $|r|^3$ in vector form) is the most common place for arithmetic slips.

---
Recent in same folder

```dataview
LIST
FROM "Courses/Electromagnetics"
WHERE file.folder = this.file.folder AND file.path != this.file.path
SORT file.mtime desc
LIMIT 5
```
