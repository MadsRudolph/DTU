**Quick reference for checking your work**

---

## Transmission Lines

|Q|Answer|
|:-:|---|
|4|VSWR = **1.50**|
|5|P_reflected = **9%**|
|6|Γ = **-1**|
|10|zL = **0.2 - j0.5**|
|11|Z_A = **74.5 Ω ∠ 13.4°**|
|12|ℓ = **0.0606 λ**|
|13|Γ_L = **0.539 ∠ 22°**|
|14|Z_L = **(183 + j104) Ω**|
|15|λ = **13.30 cm**|
|16|d = **24.45 mm**|
|17|ℓ = **19.38 mm**|

---

## Plane Waves

|Q|Answer|
|:-:|---|
|21|f = **736 MHz**|
|22|H̃₀ = **[-10.8-j54.2; 21.7-j21.7; 54.2+j10.8] mA/m**|
|23|S̄ = **[0.542; -1.083; 0.542] W/m²**|
|24|P = **0.428 W**|

---

## Materials & Propagation

|Q|Answer|
|:-:|---|
|25|t_c > **2.48 μm**|
|26|**Lossless (approx)**|
|27|η = **(133.0 - j0.04) Ω**|

---

## Interfaces & Reflection

|Q|Answer|
|:-:|---|
|28|**Elliptical, RHCP**|
|29|θᵢ = **30.0°**|
|30|θₜ = **14.5°**|
|32|**Varies** (R_TE ≈ 7.4%, R_TM ≈ 0.5%)|
|33|θ_B = **63.4°** (TM only)|

---

## Circuit Elements

|Q|Answer|
|:-:|---|
|34|C = **14.56 pF**|
|35|W = **1049 pJ**|
|36|I = **2.50 A**|
|37|L = **66.50 μH**|

---

## Key Constants Used

```matlab
c₀  = 2.998 × 10⁸ m/s
ε₀  = 8.854 × 10⁻¹² F/m
μ₀  = 4π × 10⁻⁷ H/m
η₀  = 377 Ω
```

---

## Most Used Helper Commands

```matlab
% Q4: VSWR = (1 + abs(Gamma)) / (1 - abs(Gamma))

% Q11: TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0)

% Q12: TLine('stub', 1j*30, 75, 'short')

% Q13-14: TLine('load', 75, 0.539*exp(1j*deg2rad(166)), 0.3)

% Q15-17: StubMatch(142+1j*42.5, 75, 'short', 0.133)

% Q22-23: poynting_pw('time', [2;1;0], [0;-1;-2], 10, [2;-4;2])

% Q28: Polarization(5*[1; sqrt(3); 2j], [1;0;0])

% Q29-30: Fresnel('snell', 1, 2, 30)

% Q26-27: Medium(8, 0.01, 5e9)
```

---

## Verification Tips

✓ **VSWR always ≥ 1**  
✓ **|Γ| ≤ 1** for passive loads  
✓ **Wavelength** decreases with frequency and √εᵣ  
✓ **Skin depth** decreases with frequency and σ  
✓ **Transmission angle** < incidence angle when n₂ > n₁  
✓ **Brewster angle** only exists for TM mode  
✓ **Power conservation**: R + T = 1

---

_E23 Winter 2023 - Generated 2024-12-06_