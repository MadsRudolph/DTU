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
> syms er1 er2 positive
> eta = @(er) 377./sqrt(er);
> t = 2*eta(er2)/(eta(er1)+eta(er2));
> simplify(t)
> % er1>er2 -> eta1<eta2 -> 1<t<2
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
> A plane wave in a dielectric ($\varepsilon_r=12,\ \mu_r=1$) hits vacuum at normal incidence.  
> Find the **reflected power percentage**.
>
> 💡 **Concept**  
> For normal incidence between lossless dielectrics:
> $$
> \Gamma=\frac{\eta_2-\eta_1}{\eta_2+\eta_1},\qquad
> R=|\Gamma|^2.
> $$
> with $\eta=\dfrac{\eta_0}{\sqrt{\varepsilon_r}}$.
>
> 🧮 **Derivation**
> $$
> \eta_1=\frac{377}{\sqrt{12}}=108.83~\Omega,\quad
> \eta_2=377~\Omega
> $$
> $$
> \Gamma=\frac{377-108.83}{377+108.83}=0.5520
> \Rightarrow
> R=\Gamma^2=0.3047
> $$
>
> ✅ **Answer:** $\boxed{R=30.5\%}$
>
> 🧩 **Interpretation:**  
> About 30 % of the incident power reflects because of a **large impedance mismatch** between the dielectric (108.8 Ω) and vacuum (377 Ω). The remainder transmits into free space.

> [!code]- MATLAB — Reusable Normal-Incidence Power Coefficients
> ```matlab
> eps_r1 = 12; eps_r2 = 1;
> eta1 = 377/sqrt(eps_r1);
> eta2 = 377/sqrt(eps_r2);
> Gamma = (eta2 - eta1)/(eta2 + eta1);
> R = abs(Gamma)^2; T = 1 - R;
> fprintf("R = %.2f%%, T = %.2f%%\n", 100*R, 100*T);
> ```

> [!warning] ⚠️ **Gotchas**
> - Use **$\eta$**, not $n$, for impedance ratio in $R$/$T$.  
> - Ensure units: field reflection $\Gamma$ is dimensionless; power reflection $R=|\Gamma|^2$.  
> - Sign of $\Gamma$ is important for **phase**, but not for **power**.

---

> [!summary] **Question 6 — Transmitted Power (Percent)**
>
> **Question:**  
> Continue from Q5 — find the **transmitted power percentage**.
>
> 💡 **Concept**  
> For normal incidence:
> $$
> T=\frac{4\eta_1\eta_2}{(\eta_1+\eta_2)^2}=1-R.
> $$
>
> 🧮 **Derivation**
> $$
> T=\frac{4(108.83)(377)}{(108.83+377)^2}=0.6953
> \Rightarrow T=69.5\%.
> $$
>
> ✅ **Answer:** $\boxed{T=69.5\%}$
>
> 🧩 **Interpretation:**  
> Although the **field coefficient** $t$ from Q1 was > 1, power transmission remains < 100 %.  
> The impedance weighting ensures total energy conservation: $R+T=1$ for lossless interfaces.

> [!code]- MATLAB — Quick Verification
> ```matlab
> eta1 = 108.83; eta2 = 377;
> T = (4*eta1*eta2)/(eta1 + eta2)^2;
> fprintf("T = %.2f%%\n", 100*T);
> ```

> [!warning] ⚠️ **Gotchas**
> - Don’t plug field $t$ directly into power calculations → square and scale with impedance.  
> - Remember $R+T=1$ only for **lossless** boundaries.  
> - In real materials ($\sigma>0$), a small fraction is **absorbed**: $R+T<1$.
---



---
> [!info] **Section 3 — Oblique Incidence (TE Case) (Q7–Q9)**  
> Medium 1: $\varepsilon_{r1}=2,\ \mu_{r1}=2$; Medium 2: $\varepsilon_{r2}=20,\ \mu_{r2}=1$  
> $\hat\beta=(0.6,-0.8,0)$, $\hat n=(3/\sqrt{10},-1/\sqrt{10},0)$.

> [!summary] **Question 7 — Incidence Type and Polarization (TE/TM)**
>
> **Question:**  
> Determine the **type of incidence** (normal/oblique) and the **polarization** (TE or TM) for the given fields.
>
> 💡 **Concept**  
> - The *plane of incidence* is defined by $\hat\beta$ and $\hat n$.  
> - If $\hat\beta\nparallel\hat n$ → **oblique incidence**.  
> - For plane waves: $\tilde{\mathbf E}=-\eta(\hat\beta\times\tilde{\mathbf H})$.
>
> 🧮 **Derivation**  
> Cross product direction:
> $$
> \hat\beta\times\tilde{\mathbf H}
> =\begin{vmatrix}
> \hat x & \hat y & \hat z\\
> 0.6 & -0.8 & 0\\
> H_x & H_y & 0
> \end{vmatrix}
> =(0,0,\,0.6H_y+0.8H_x)\propto \hat z
> $$
> Hence $\tilde{\mathbf E}\parallel\hat z$, perpendicular to the plane of incidence ($xy$-plane).  
> $\Rightarrow$ **TE (transverse electric) polarization**.
>
> ✅ **Answer:** $\boxed{\text{Oblique incidence with TE polarization}}$
>
> 🧩 **Interpretation:**  
> TE means the **electric field lies perpendicular** to the plane of incidence.  
> This directly affects which Fresnel equations apply (TE set in Q9).

> [!code]- MATLAB — Verify E Orientation
> ```matlab
> Hb = [4-1j*8; 3-1j*6; 0];       % H phasor (mA/m)
> beta_hat = [0.6; -0.8; 0];
> E_dir = cross(beta_hat, Hb);    % direction ∝ E-field
> disp(E_dir)  % should point mainly along z-axis
> ```

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
> n_i=\sqrt{\varepsilon_{ri}\mu_{ri}}
> $$
>
> 🧮 **Derivation**  
> From geometry:
> $$
> \cos\theta_i=\hat\beta\cdot\hat n
> =0.6\cdot\frac{3}{\sqrt{10}}+(-0.8)\cdot\frac{-1}{\sqrt{10}}=0.82219
> $$
> $$
> \theta_i=\arccos(0.82219)=34.70^\circ
> $$
> Refractive indices:
> $$
> n_1=\sqrt{2\cdot2}=2,\quad n_2=\sqrt{20\cdot1}=4.4721
> $$
> Apply Snell’s law:
> $$
> \sin\theta_t=\frac{n_1}{n_2}\sin\theta_i
> =\frac{2}{4.4721}\sin(34.70^\circ)=0.2546
> \Rightarrow \theta_t=14.75^\circ
> $$
>
> ✅ **Answer:** $\boxed{\theta_t=14.7^\circ}$
>
> 🧩 **Interpretation:**  
> Entering a medium with higher $\varepsilon_r$ (and $n$) bends the ray **toward the normal**, consistent with Snell’s law predictions.

> [!code]- MATLAB — Reusable Snell’s Law Check
> ```matlab
> n1 = sqrt(2*2); n2 = sqrt(20*1);
> th_i = acos(0.82219);
> th_t = asin((n1/n2)*sin(th_i));
> fprintf("θ_t = %.2f°\n", th_t*180/pi);
> ```

> [!warning] ⚠️ **Gotchas**
> - Always use **refractive index** $n=\sqrt{\varepsilon_r\mu_r}$, not $\eta$.  
> - Use radians in MATLAB trig functions.  
> - If $\sin\theta_t>1$, total internal reflection occurs (not here).

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
> ✅ **Answer:** $\boxed{T_{\text{TE}}=53.7\%}$
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
> fprintf("TE Transmission = %.2f%%\n", 100*TTE);
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
> ✅ **Answer:** $\boxed{72.65^\circ}$
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
