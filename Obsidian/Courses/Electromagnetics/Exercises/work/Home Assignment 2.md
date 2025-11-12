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
> - A **PEC** enforces $E_t = 0$ at the surface → total reflection with $\Gamma = -1$.  
> - The total fields in medium 1 are the **sum** of the incident and reflected waves.  
> - Since $|\Gamma| = 1$, the two waves carry **equal and opposite power**, so the net energy transport must be zero.  
> - The **time-average Poynting vector** quantifies real power flow:
>   $$
>   \langle \mathbf{S} \rangle = \tfrac{1}{2}\text{Re}(\mathbf{E}_\text{tot} \times \mathbf{H}_\text{tot}^*)
>   $$
>
> 🧮 **Derivation**
> For a normally incident plane wave on a PEC:
> $$
> \Gamma = -1 \quad\Rightarrow\quad
> E_\text{ref} = -E_\text{inc},\qquad
> H_\text{ref} = +H_\text{inc}.
> $$
>
> Total electric field:
> $$
> E_\text{tot}(y)
> = E_0(e^{-j\beta y} - e^{+j\beta y})
> = -\,2jE_0\sin(\beta y)
> $$
>
> Total magnetic field:
> $$
> H_\text{tot}(y)
> = \frac{E_0}{\eta}(e^{-j\beta y} + e^{+j\beta y})
> = \frac{2E_0}{\eta}\cos(\beta y)
> $$
>
> Time-average power flow:
> $$
> \langle S \rangle
> = \tfrac{1}{2}\text{Re}(E_\text{tot}H_\text{tot}^*)
> = \tfrac{1}{2}\text{Re}\!\Big[-2jE_0\sin(\beta y)\cdot\tfrac{2E_0}{\eta}\cos(\beta y)\Big]
> = 0
> $$
>
> Because the product is purely imaginary, no **real** power is transmitted.  
> The forward and backward powers exactly cancel, leaving a **standing wave**.
>
> ✅ **Answer:** $\boxed{\langle\mathbf{S}_\text{tot}\rangle = 0}$
>
> 🧩 **Interpretation:**  
> At a PEC boundary, the incident energy cannot enter the conductor, so it’s fully reflected.  
> The resulting standing wave alternates between stored **electric** and **magnetic** energy,  
> but the **net time-averaged Poynting vector** is zero — there’s no continuous energy flow toward the boundary.

> [!code]- MATLAB — Standing-Wave Poynting Vector (PEC Boundary)
> ```matlab
> %% Q3 — Standing-Wave Power Flow Check (PEC Boundary)
> % For a PEC at y=0, Γ=-1 creates a standing wave with <S>=0
> 
> y = linspace(0, 2*pi, 500);  % spatial points [m or λ units]
> E0 = 1;                       % amplitude [V/m]
> beta = 1;                     % wave number [rad/m]
> eta = 377;                    % intrinsic impedance [Ω]
> 
> % Total fields in medium 1 (incident + reflected with Γ=-1)
> Ei = E0 * exp(-1j*beta*y);             % incident E
> Er = -E0 * exp(1j*beta*y);             % reflected E (Γ=-1)
> Etot = Ei + Er;                        % = -2j*E0*sin(β*y)
> 
> Hi = (E0/eta) * exp(-1j*beta*y);       % incident H
> Hr = (E0/eta) * exp(1j*beta*y);        % reflected H (same direction as inc)
> Htot = Hi + Hr;                        % = (2*E0/η)*cos(β*y)
> 
> % Time-average Poynting vector: <S> = (1/2)*Re(E * conj(H))
> S_avg = 0.5 * real(Etot .* conj(Htot));
> 
> % Verify it's zero everywhere (numerically ~1e-16)
> fprintf('Max |<S>| = %.4e W/m² (should be ~0)\n', max(abs(S_avg)));
> fprintf('Mean <S> = %.4e W/m²\n', mean(S_avg));
> 
> % Visualization
> figure;
> subplot(3,1,1);
> plot(y, abs(Etot), 'b', 'LineWidth', 1.5);
> title('Standing Wave: |E_{tot}| at PEC boundary');
> xlabel('Position y [rad or m]'); ylabel('|E| [V/m]');
> grid on;
> 
> subplot(3,1,2);
> plot(y, abs(Htot), 'r', 'LineWidth', 1.5);
> title('Standing Wave: |H_{tot}|');
> xlabel('Position y'); ylabel('|H| [A/m]');
> grid on;
> 
> subplot(3,1,3);
> plot(y, S_avg, 'k', 'LineWidth', 1.5);
> title('Time-Average Poynting Vector <S>');
> xlabel('Position y'); ylabel('<S> [W/m²]');
> ylim([-1e-15, 1e-15]);  % zoom to show it's numerically zero
> grid on;
> ```

> [!warning] ⚠️ **Gotchas**
> - Don’t confuse **instantaneous** $\mathbf S(t)$ with **time-averaged** $\langle \mathbf S \rangle$.  
> - For a PEC, $\Gamma = -1$ → total reflection; for a real metal, $|\Gamma|\lesssim1$ → small absorption.  
> - $E$ and $H$ are $90^\circ$ out of phase in space: $\sin(\beta y)$ vs. $\cos(\beta y)$.  
> - Nodes of $E$ coincide with antinodes of $H$ → alternating electric and magnetic energy storage.  
> - The standing-wave pattern proves total reflection and zero net energy transport.

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
> Compute the **transmitted power coefficient** $T_{\text{TE}}$ for the given parameters (use 4 decimal places in printed results).
>
> 💡 **Concept (TE Fresnel)**  
> For **oblique TE** incidence between lossless media:
> $$
> t_{\text{TE}}=\frac{2\,\eta_2\cos\theta_i}{\eta_2\cos\theta_i+\eta_1\cos\theta_t},\qquad
> T_{\text{TE}}=\frac{\eta_1}{\eta_2}\frac{\cos\theta_t}{\cos\theta_i}\,\bigl|t_{\text{TE}}\bigr|^2,
> $$
> where $\eta=\eta_0\sqrt{\mu_r/\varepsilon_r}$ with $\eta_0=377~\Omega$.
>
> 🧮 **Derivation (exact inputs, 4-dp outputs)**  
> Given media: $(\varepsilon_{r1},\mu_{r1})=(2,2)$ and $(\varepsilon_{r2},\mu_{r2})=(20,1)$  
> → $\eta_1=\eta_0\sqrt{2/2}= \mathbf{377.0000}~\Omega$,  
> $\eta_2=\eta_0\sqrt{1/20}= \mathbf{84.2998}~\Omega$.
>
> From Q8 we had
> $$
> \theta_i=\mathbf{34.6952}^\circ,\qquad \theta_t=\mathbf{14.7474}^\circ,
> $$
> so
> $$
> \cos\theta_i=\mathbf{0.8222},\qquad \cos\theta_t=\mathbf{0.9679}.
> $$
> Field transmission (TE):
> $$
> t_{\text{TE}}
> =\frac{2(84.2998)(0.8222)}{84.2998(0.8222)+377.0000(0.9679)}
> =\mathbf{0.3195}.
> $$
> Power transmission (TE):
> $$
> T_{\text{TE}}
> =\frac{377.0000}{84.2998}\frac{0.9679}{0.8222}\,(0.3195)^2
> =\mathbf{0.5369}\ \Rightarrow\ \mathbf{53.6898}\%.
> $$
>
> ✅ **Answer:** $\boxed{T_{\text{TE}}=53.6898\%}$
>
> 🧩 **Interpretation:**  
> Because $\eta_2\ll\eta_1$ (high-$\varepsilon$ second medium), TE suffers **stronger reflection** than TM; still, more than half the **power** transmits at this moderate incidence. Always remember: TE/TM use **different Fresnel forms**, and power coefficients include the **impedance and cosine** weighting, not just $|t|^2$.  

> [!code]- MATLAB — Live Script–Ready (prints 4 dp, recomputes from vectors)
> ```matlab
> %% Q9 — TE Power Transmission at Oblique Incidence (4 dp)
> % Geometry (from the problem)
> beta_hat = [0.6; -0.8; 0];
> n_hat    = [3/sqrt(10); -1/sqrt(10); 0];
> 
> % Media (lossless)
> eps_r1 = 2;  mu_r1 = 2;
> eps_r2 = 20; mu_r2 = 1;
> eta0 = 377;                    % [ohm]
> eta1 = eta0 * sqrt(mu_r1/eps_r1);
> eta2 = eta0 * sqrt(mu_r2/eps_r2);
> 
> % Angles
> beta_hat = beta_hat / norm(beta_hat);
> n_hat    = n_hat    / norm(n_hat);
> cos_th_i = dot(beta_hat, n_hat);
> th_i = acos(cos_th_i);
> 
> n1 = sqrt(eps_r1*mu_r1);
> n2 = sqrt(eps_r2*mu_r2);
> th_t = asin((n1/n2) * sin(th_i));
> 
> % Fresnel TE
> tTE = (2*eta2*cos(th_i)) / (eta2*cos(th_i) + eta1*cos(th_t));
> TTE = (eta1/eta2) * (cos(th_t)/cos(th_i)) * abs(tTE)^2;
> 
> % Print 4 dp
> fprintf('eta1 = %.4f ohm, eta2 = %.4f ohm\n', eta1, eta2);
> fprintf('cos(theta_i) = %.4f, cos(theta_t) = %.4f\n', cos(th_i), cos(th_t));
> fprintf('t_TE = %.4f\n', tTE);
> fprintf('T_TE = %.4f (%.4f %%)\n', TTE, 100*TTE);
> 
> % Energy sanity (optional, compute R_TE too)
> rTE = (eta2*cos(th_i) - eta1*cos(th_t)) / (eta2*cos(th_i) + eta1*cos(th_t));
> RTE = abs(rTE)^2;
> fprintf('Energy check: R_TE + T_TE = %.4f\n', RTE + TTE);
> ```

> [!warning] **Gotchas**
> - TE vs TM: **don’t mix** the Fresnel forms; the cosines/impedances sit in **different places**.  
> - Round only at the **end**. Keep full precision for intermediate cosines and impedances, then print with `%.4f`.  
> - In lossless cases, always check **$R+T\simeq1$** as a quick validator.


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
> For $\mu_1=\mu_2$, the **TM** (p-polarized) reflection goes to zero at
> $$
> \tan\theta_B=\sqrt{\frac{\varepsilon_{r2}}{\varepsilon_{r1}}},\qquad
> \theta_B=\arctan\!\Big(\sqrt{\tfrac{\varepsilon_{r2}}{\varepsilon_{r1}}}\Big).
> $$
>
> 🧮 **Derivation (exact, 4-dp output)**  
> Here $\varepsilon_{r1}=1$ (air), $\varepsilon_{r2}=10$:
> $$
> \tan\theta_B=\sqrt{\frac{10}{1}}=\sqrt{10}=3.162277660\ldots
> $$
> $$
> \theta_B=\arctan(\sqrt{10})=\boxed{72.4516^\circ}.
> $$
>
> ✅ **Answer:** $\boxed{72.4516^\circ}$
>
> 🧩 **Interpretation:**  
> Bigger $\varepsilon_{r2}$ drags the Brewster angle way up,— at ~$72.45^\circ$ the **TM** reflection cancels. In real life, tiny loss/roughness means it won’t be *exactly* zero, but it’s still the sweet spot for minimizing the ground-bounce in TM. ✨

> [!code]- MATLAB — Reusable Brewster (TM, non-magnetic, prints 4 dp)
> ```matlab
> %% Q11 — TM Brewster angle (μ1 = μ2), 4-decimal print
> eps1 = 1;    % air
> eps2 = 10;   % ground-like
> thetaB = atan( sqrt(eps2/eps1) );     % radians
> thetaB_deg = thetaB * 180/pi;         % degrees
> fprintf("TM Brewster angle = %.4f°\n", thetaB_deg);  % -> 72.4516°
> ```

> [!warning] ⚠️ **Gotchas**
> - This closed form is for **TM** with **μ1=μ2**. If μ differs, solve $\Gamma_{\text{TM}}(\theta)=0$ from Fresnel directly.  
> - Brewster is the **incident** angle in medium 1.  
> - TE has **no** Brewster zero when μ matches.


---

> [!info] **Section 5 — Electrostatics: Three Collinear Charges (Q12–Q13)**  
> Geometry: three point charges on the $x$-axis, spacing $d=10~\text{nm}=1\times10^{-8}\,\text{m}$; force on $Q_2$ toward $+x$ taken as positive.

> [!summary] **Question 12 — $Q_1=Q_3=-5~\text{aC},\; Q_2=-10~\text{aC}$**
>
> **Question:**  
> Find the **$x$-component of the force** on $Q_2$ (in nN) for three point charges aligned along the $x$-axis, equally spaced by $d=10~\text{nm}$.
>
> 💡 **Concept**  
> Coulomb’s law gives the electric force between any two point charges as
> $$
> \mathbf{F}_{ij}=k\frac{Q_iQ_j}{r_{ij}^2}\hat{r}_{ij}, \qquad
> k=8.988\times10^9~\text{N·m}^2/\text{C}^2.
> $$
> Since all charges here are **negative**, each pair repels. Symmetry tells us that forces from the left and right neighbors may cancel.
>
> 🧮 **Derivation (exact 4-dp values)**  
> Distance between charges:  
> $$
> d = 10~\text{nm} = 1.0000\times10^{-8}~\text{m}.
> $$
> Magnitudes of charges:  
> $$
> |Q_1| = |Q_3| = 5.0000\times10^{-18}~\text{C},\qquad
> |Q_2| = 1.0000\times10^{-17}~\text{C}.
> $$
> Force magnitude from **one neighbor** on $Q_2$:
> $$
> F_\text{one} = k\frac{|Q_1 Q_2|}{d^2}
> = 8.988\times10^9 \cdot \frac{(5\times10^{-18})(10\times10^{-18})}{(10^{-8})^2}
> = \boxed{4.4940~\text{nN}}.
> $$
> Directions:  
> - $Q_1$ (left) repels $Q_2$ → **rightward**, $+4.4940$ nN.  
> - $Q_3$ (right) repels $Q_2$ → **leftward**, $-4.4940$ nN.  
>
> Net:
> $$
> F_x = +4.4940 - 4.4940 = \boxed{0.0000~\text{nN}}.
> $$
>
> ✅ **Answer:** $\boxed{F_x = 0.0000~\text{nN}}$
>
> 🧩 **Interpretation:**  
> The setup is perfectly symmetric about the center charge $Q_2$, so the equal and opposite repulsive forces cancel exactly. Although each neighbor applies a $4.494~\text{nN}$ push, $Q_2$ experiences **no net force** — equilibrium due to symmetry.

> [!code]- MATLAB — Reusable Three-Charge Line (Signed 1D Force, 4-dp output)
> ```matlab
> %% Q12 — 1D Coulomb force on center charge (4-decimal precision)
> % Positions: Q1 at -d, Q2 at 0, Q3 at +d
> k  = 8.988e9;          % [N·m^2/C^2]
> d  = 1e-8;             % [m]
> Q1 = -5e-18;           % [C]
> Q2 = -10e-18;          % [C]
> Q3 = -5e-18;           % [C]
> 
> xi = [-d, +d];         % positions of Q1 and Q3
> Qi = [Q1, Q3];         % their charges
> Fx = 0;                % net force on Q2 (x-component)
> 
> for i = 1:2
>     r = 0 - xi(i);                     % vector from Qi to Q2 (signed)
>     Fx = Fx + k * Q2 * Qi(i) * (r) / abs(r)^3;  % Coulomb 1D form
> end
> 
> fprintf("Fx on Q2 = %.4f nN\n", 1e9*Fx);   % Expected → 0.0000 nN
> ```

> [!warning] ⚠️ **Gotchas**
> - Use the **signed 1D vector form** $F_x=kQ_2Q_i(x_2-x_i)/|x_2-x_i|^3$ to avoid direction mistakes.  
> - Always convert: $1~\text{aC}=10^{-18}~\text{C}$, $1~\text{nm}=10^{-9}~\text{m}$.  
> - Check symmetry: if $Q_1=Q_3$, the net force on the center is **zero** regardless of magnitudes.


---

> [!summary] **Question 13 — $Q_1=-3~\text{aC},\; Q_3=+3~\text{aC},\; Q_2=-10~\text{aC}$**
>
> **Question:**  
> Find the **$x$-component of the force** on $Q_2$ (in nN) for three equally spaced point charges ($d=10~\text{nm}$) along the $x$-axis.
>
> 💡 **Concept**  
> Coulomb’s law in 1D:
> $$
> F_x = k\,Q_2Q_i\frac{(x_2-x_i)}{|x_2-x_i|^3},\qquad
> k = 8.988\times10^9~\text{N·m}^2/\text{C}^2.
> $$
> With $Q_2<0$:
> - $Q_1=-3~\text{aC}$ → **repulsion** → $+x$ direction.  
> - $Q_3=+3~\text{aC}$ → **attraction** → also $+x$.  
> Both contributions reinforce each other.
>
> 🧮 **Derivation (exact 4-dp values)**  
> Spacing:
> $$
> d = 10~\text{nm} = 1.0000\times10^{-8}~\text{m}.
> $$
> Magnitudes:
> $$
> |Q_1| = |Q_3| = 3.0000\times10^{-18}~\text{C},\qquad
> |Q_2| = 1.0000\times10^{-17}~\text{C}.
> $$
> Single-side magnitude:
> $$
> F_\text{one} = k\frac{|Q_1Q_2|}{d^2}
> = 8.988\times10^9\frac{(3\times10^{-18})(10\times10^{-18})}{(10^{-8})^2}
> = \boxed{2.6964~\text{nN}}.
> $$
> Both sides act toward $+x$, so:
> $$
> F_x = 2F_\text{one} = \boxed{5.3928~\text{nN}}.
> $$
>
> ✅ **Answer:** $\boxed{F_x = +5.3928~\text{nN}}$
>
> 🧩 **Interpretation:**  
> The left-side **repulsion** and right-side **attraction** push in the same direction, yielding a net force of about **5.39 nN** toward $+x$.  
> Unlike the symmetric case (Q12), this configuration breaks balance, giving a definite net motion direction.

> [!code]- MATLAB — 1D Coulomb Force (Live Script–Ready, 4-dp precision)
> ```matlab
> %% Q13 — Net Coulomb Force on Middle Charge (4-decimal print)
> % Positions: Q1 at -d, Q2 at 0, Q3 at +d
> k  = 8.988e9;      % [N·m^2/C^2]
> d  = 1e-8;         % [m]
> Q1 = -3e-18;       % [C]
> Q2 = -10e-18;      % [C]
> Q3 = +3e-18;       % [C]
> 
> xi = [-d, +d];
> Qi = [Q1, Q3];
> Fx = 0;
> for i = 1:2
>     r = 0 - xi(i);                         % vector from Qi to Q2
>     Fx = Fx + k * Q2 * Qi(i) * (r) / abs(r)^3;
> end
> 
> fprintf('Fx on Q2 = %.4f nN\n', 1e9*Fx);  % → +5.3928 nN
> ```

> [!warning] ⚠️ **Gotchas**
> - Use the **signed** 1D vector form to get correct directions.  
> - Always convert properly: $1~\text{aC}=10^{-18}~\text{C}$, $1~\text{nm}=10^{-9}~\text{m}$.  
> - Both sides must point the same way here—repulsion + attraction reinforce → positive net force.

---
Recent in same folder

```dataview
LIST
FROM "Courses/Electromagnetics"
WHERE file.folder = this.file.folder AND file.path != this.file.path
SORT file.mtime desc
LIMIT 5
```
