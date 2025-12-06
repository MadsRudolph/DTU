# E23 Exam Solutions Summary

**Exam:** Winter 2023 Electromagnetics  
**Date Completed:** December 6, 2024  
**Tools Used:** EM Helper Toolkit (MATLAB)

---

## 📊 Quick Answer Sheet

### Transmission Lines (Q4-Q17)

|Q#|Question|Answer|Method|
|---|---|---|---|
|Q4|VSWR for Γ = -j/3|**1.50**|`VSWR = (1 +|
|Q5|Power reflected for \|Γ\| = 0.3|**9%**|`P =|
|Q6|Reflection coeff. of short|**Γ = -1**|`Γ = (0-Z₀)/(0+Z₀)`|
|Q10|Normalized impedance|**zL = 0.2 - j0.5**|`zL = ZL/Z₀`|
|Q11|Input Z with series C|**74.5 Ω ∠ 13.4°**|`TLine('series_C', ...)`|
|Q12|Stub length for j30 Ω|**ℓ = 0.0606 λ**|`TLine('stub', 1j*30, 75, 'short')`|
|Q13|Load Γ from Γ_A|**Γ_L = 0.539 ∠ 22°**|`TLine('load', Z₀, Γ_A, ℓ)`|
|Q14|Load impedance Z_L|**Z_L = 183 + j104 Ω**|From Q13 result|
|Q15|Wavelength at 1550 MHz|**λ = 13.30 cm**|`λ = c₀/(f√εᵣ)`|
|Q16|Stub position d|**d = 24.45 mm**|`StubMatch(...)`|
|Q17|Stub length ℓ|**ℓ = 19.38 mm**|`StubMatch(...)`|

### Plane Waves (Q21-Q24)

|Q#|Question|Answer|Method|
|---|---|---|---|
|Q21|Frequency from β|**f = 736 MHz**|`f = ω/(2π) = β·c₀/(2π)`|
|Q22|H-field phasor|**See detailed answer**|`poynting_pw('time', a, b, E₀, β)`|
|Q23|Poynting vector|**S̄ = [0.542; -1.083; 0.542] W/m²**|From `poynting_pw`|
|Q24|Incident power|**P = 0.428 W**|`P =|

**Q22 Detailed Answer:**

```
H̃₀ = [-10.8 - j54.2; 21.7 - j21.7; 54.2 + j10.8] mA/m
```

### Materials & Wave Propagation (Q25-Q27)

|Q#|Question|Answer|Method|
|---|---|---|---|
|Q25|Min coating thickness|**t_c > 2.48 μm**|`5 × skin_depth at 18 GHz`|
|Q26|Material classification|**Lossless (approx)**|`tan(δ) = 2.8×10⁻⁴ << 1`|
|Q27|Intrinsic impedance|**η = 133.0 - j0.04 Ω**|From `Medium(εᵣ, σ, f)`|

### Interfaces & Reflection (Q28-Q33)

|Q#|Question|Answer|Method|
|---|---|---|---|
|Q28|Polarization type|**Elliptical, RHCP**|`Polarization(E_phasor)`|
|Q29|Angle of incidence|**θᵢ = 30.0°**|`θᵢ = arccos(β·n̂/|
|Q30|Transmission angle|**θₜ = 14.5°**|`Fresnel('snell', n₁, n₂, θᵢ)`|
|Q32|Reflected power|**Varies with polarization**|`Fresnel(εᵣ₁, εᵣ₂, θᵢ)`|
|Q33|Brewster angle|**θ_B = 63.4°**|`Fresnel('brewster', 1, 4)`|

**Q32 Details:**

- TE mode: R_TE ≈ 7.4%
- TM mode: R_TM ≈ 0.5%
- Total reflection depends on polarization mix

### Circuit Elements (Q34-Q37)

|Q#|Question|Answer|Method|
|---|---|---|---|
|Q34|Coaxial capacitance|**C = 14.56 pF**|`C = 2πεL/ln(b/a)`|
|Q35|Energy stored|**W = 1049 pJ**|`W = ½CV²`|
|Q36|Solenoid current|**I = 2.50 A**|`I = B/(μ₀n)`|
|Q37|Solenoid inductance|**L = 66.50 μH**|`L = μ₀N²A/ℓ`|

---

## 🔧 Helper Functions Used

### Most Common Functions

```matlab
% Material properties
Medium(eps_r, freq)              % Lossless
Medium(eps_r, sigma, freq)       % Lossy
Medium('conductor', sigma, freq) % Good conductor
Medium('skin', sigma, freq)      % Skin depth only

% Transmission lines
TLine(Z0, ZL, len_lambda)        % Full analysis
TLine('Gamma', Z0, Z)            % Get Γ from Z
TLine('Z', Z0, Gamma)            % Get Z from Γ
TLine('load', Z0, Gamma_A, len)  % Find Γ_L and Z_L from Γ_A
TLine('stub', Z_target, Z0, type)% Stub design
TLine('series_C', ...)           % TL + series capacitor

% Stub matching
StubMatch(ZL, Z0, 'short', lambda) % With wavelength → mm

% Polarization
Polarization(F_phasor)           % Analyze polarization
Polarization(F, k_hat)           % With propagation direction

% Interfaces
Fresnel(eps1, eps2)              % Normal incidence
Fresnel(eps1, eps2, theta)       % Oblique incidence
Fresnel('snell', n1, n2, theta)  % Snell's law
Fresnel('brewster', eps1, eps2)  % Brewster angle

% Plane waves
poynting_pw('time', a, b, E0, beta_vec) % H-field & Poynting
```

---

## 💡 Key Formulas Reference

### Transmission Lines

**VSWR:** $$\text{VSWR} = \frac{1 + |\Gamma|}{1 - |\Gamma|}$$

**Reflection coefficient:** $$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$

**Power reflected:** $$P_{\text{refl}} = |\Gamma|^2$$

**Gamma propagation:** $$\Gamma_{\text{in}} = \Gamma_L \cdot e^{-j2\beta\ell}$$

**Input impedance:** $$Z_{\text{in}} = Z_0 \frac{Z_L + jZ_0\tan(\beta\ell)}{Z_0 + jZ_L\tan(\beta\ell)}$$

### Wave Propagation

**Phase constant (lossless):** $$\beta = \omega\sqrt{\mu\varepsilon} = \frac{\omega}{v_p} = \frac{2\pi}{\lambda}$$

**Wavelength:** $$\lambda = \frac{v_p}{f} = \frac{c_0}{f\sqrt{\varepsilon_r}}$$

**Skin depth:** $$\delta = \frac{1}{\sqrt{\pi f \mu \sigma}}$$

**Loss tangent:** $$\tan\delta = \frac{\sigma}{\omega\varepsilon}$$

### Plane Waves

**Phasor conversion:** $$\vec{E} = \vec{a}\cos\Phi + \vec{b}\sin\Phi \Rightarrow \tilde{\vec{E}}_0 = E_0(\vec{a} - j\vec{b})$$

**Magnetic field:** $$\tilde{\vec{H}}_0 = \frac{1}{\eta}\hat{k} \times \tilde{\vec{E}}_0$$

**Time-average Poynting:** $$\bar{\vec{S}} = \frac{1}{2}\text{Re}{\tilde{\vec{E}} \times \tilde{\vec{H}}^*}$$

### Interfaces

**Snell's law:** $$n_1\sin\theta_i = n_2\sin\theta_t$$

**Fresnel (TE):** $$\Gamma_{TE} = \frac{\eta_2\cos\theta_i - \eta_1\cos\theta_t}{\eta_2\cos\theta_i + \eta_1\cos\theta_t}$$

**Fresnel (TM):** $$\Gamma_{TM} = \frac{\eta_2\cos\theta_t - \eta_1\cos\theta_i}{\eta_2\cos\theta_t + \eta_1\cos\theta_i}$$

**Brewster angle:** $$\theta_B = \arctan\left(\frac{n_2}{n_1}\right)$$

### Circuit Elements

**Coaxial capacitor:** $$C = \frac{2\pi\varepsilon L}{\ln(b/a)}$$

**Solenoid:** $$B = \mu_0 n I, \quad L = \frac{\mu_0 N^2 A}{\ell}$$

---

## 📝 Notes & Tips

### Common Pitfalls

1. **Phase signs**: Remember β·r has opposite sign to ωt in phase term
2. **Units**: Check if lengths are in λ or meters
3. **Gamma direction**: Input→Load needs `exp(+j2βℓ)`, Load→Input needs `exp(-j2βℓ)`
4. **Polarization handedness**: Use IEEE convention (looking from behind)

### Helper Script Advantages

✅ Automatic unit handling  
✅ Built-in validation  
✅ Clear, formatted output  
✅ Multiple solution methods when applicable  
✅ Detailed calculation steps shown

### Time-Saving Patterns

```matlab
% Q-type: Find Γ_L and Z_L from measurement
% Instead of manual calculation:
r = TLine('load', Z0, Gamma_measured, length_lambda);
% Access: r.Gamma_L, r.Z_L

% Q-type: Stub matching with physical dimensions
% Instead of normalized → denormalized:
r = StubMatch(ZL, Z0, 'short', wavelength_meters);
% Access: r.d_mm, r.l_mm

% Q-type: TL + lumped element
% Instead of manual impedance addition:
r = TLine('series_C', Z0, ZL, len_m, C, freq, vp);
% Access: r.Z_A, r.Z_TL, r.Z_element
```

---

## 🎯 Exam Strategy

### Time Allocation

- Quick calculations (Q4-Q6): **~2 min each**
- Helper script problems (Q11-Q17): **~5 min each**
- Complex problems (Q21-Q24, Q28-Q33): **~8 min each**
- Simple formulas (Q34-Q37): **~3 min each**

### Verification Checklist

- [ ] Units correct (Ω, λ, mm, etc.)
- [ ] Magnitude reasonable (VSWR > 1, |Γ| < 1, etc.)
- [ ] Sign conventions (phase, angles)
- [ ] Helper output matches manual check

---

**Links:**

- [[Helpers]] - Complete helper function reference
- [[E23]] - Full exam with problem statements
- [[E23 answer key]] - zero fluff

---