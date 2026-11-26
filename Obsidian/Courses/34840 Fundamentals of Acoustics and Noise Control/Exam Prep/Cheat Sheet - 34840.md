---
course: "34840"
course-name: "Fundamentals of Acoustics and Noise Control"
type: exam-prep
date: 2026-11-26
tags: [Acoustics, exam-prep, cheat-sheet, formulas]
---
# Cheat Sheet — 34840 Fundamentals of Acoustics and Noise Control

> [!info] The exam
> **Fri 11 Dec 2026, written, 4 h, individual. All aids, no internet.** Part 1 = problems like the hand-in (answer as a PDF, 40 %). Part 2 = multiple choice (≈15 questions, 60 %; the last 3–4 are hearing).
> Printable version: [[Cheat Sheet - 34840.pdf]] (source `5. Semester/Acoustics and Noise Control/Exam/cheatsheet_34840.tex`).
> MATLAB templates: `5. Semester/Acoustics and Noise Control/Exam/toolkit/` (T01–T15, `run_all_checks` = 116/116 pass). Exam-day plan: [[Exam Day Checklist - 34840]]. Old exams worked: [[Old Exams 2022-2024 - Worked]].

## 0. Constants and conventions

| Quantity | Value | Note |
|---|---|---|
| ρ (air) | **1.2 kg/m³** | every exam 2022–2024 states 1.2 and 343 |
| c (air) | **343 m/s** (20 °C) | Weeks 5 and 7 used 344: that shifts answers in the 3rd digit only |
| ρc | **411.6 Pa·s/m** | sheets also use 413 / 414 |
| ρc² | 1.41 × 10⁵ Pa | air spring, membrane absorber |
| Water | ρ = 1000, c = 1480 → ρc = 1.48 × 10⁶ | hand-in values |
| p_ref | 20 µPa (air), 1 µPa (water) | 94 dB = 1 Pa, 0 dB = 20 µPa |
| I_ref, W_ref | 10⁻¹² W/m², 10⁻¹² W | L_I = L_p − 0.14 dB in a plane wave |
| u_ref | 1 nm/s | |
| g | 9.81 m/s² | static deflection |
| c(T) | 20.05 √(T in K) | f ∝ c for fixed geometry |
| γ, R_s | 1.4, 287 J/(kg K) | c = √(γ R_s T) |

**Phasor convention:** p(t) = Re{P e^{jωt}}, **capital letters are peak amplitudes**. p_rms = |P|/√2. Intensity and power with peak values carry ½. Room acoustics (L6, L12) uses **rms** throughout (no ½). ∂/∂t → jω, ∫dt → 1/(jω).

## 0.5 Decision points (read the question for these first)

| Question | Choose |
|---|---|
| Same frequency **and** fixed phase? | **Coherent:** add complex amplitudes, then \|·\|. Equal levels: −∞ … +6 dB |
| Different frequencies / independent sources? | **Incoherent:** add p²_rms (10 log Σ 10^{L/10}). Equal levels: +3 dB |
| Two tones close in frequency, averaged over ≥ one beat period 1/Δf | incoherent (2022 MC2) |
| Amplitude or rms? | "amplitude" = peak → divide by √2 before L_p. Voltages on sheets are rms unless "amplitude" |
| 20 log or 10 log? | p, u, v, F, Q → 20 log. I, W, p², τ, E → 10 log |
| Free field or baffle/wall? | free (small box in air): **4πr**, power over 4πr². Infinite baffle / on a rigid plane: **2πr**, 2πr² |
| Wall at distance h | kh ≪ 1: pressure ×2 (+6 dB), power ×2 (+3 dB). kh > π/2: wall hardly matters |
| Near field? | kr < 1: u has extra 1/(jkr) term, p leads u by atan(1/kr). Intensity still p²_rms/ρc for one monopole |
| Sabine or Eyring? | ᾱ < 0.3 Sabine; ᾱ > 0.3 or "high absorption" Eyring. Eyring always shorter |
| Below / above f_s (loudspeaker) | below: stiffness controlled, −12 dB/oct. above: mass controlled, flat |
| Below / above √2 f₀ (isolation) | T > 1 below √2 f₀ (amplifies!), isolation only above |
| Below / above f_c (wall) | below: mass law (−5 field). above: resonant, + 10 log(2ηf/πf_c), 9 dB/oct |
| Normal vs field vs random incidence (wall) | R_field = R₀ − 5 dB (exam standard). R_random = R₀ − 10 log(0.23 R₀) |
| Normal vs random incidence (absorber) | tube = α₀ (normal). Reverb room/Paris = α_r. They differ |
| Double wall | f < f₀: one wall of m₁+m₂. f₀ < f < f_d: R₁+R₂+20 log(2kd), 18 dB/oct. f > f_d: R₁+R₂+6 |
| ERB vs critical band vs third octave | the question says ERB → **24.7(4.37F+1), F in kHz** |
| Absorber type | porous: mid–high f (λ/4). membrane: low f (<500 Hz). resonator: narrow band |
| Thicker wall | f_c ∝ 1/h goes **down**. Stacked loose layers: f_c unchanged |

---

## 1. Plane waves, reflection, tubes (L1–L2) → `T01`, `T02`

[[Lecture 1 - Introduction and Plane Waves]] · [[Lecture 2 - Plane Waves Reflection and Spherical Waves]] · [[Week 1 - Fundamental Concepts and Plane Waves]] · [[Week 2 - Reflection and Spherical Waves]]

- λ = c/f, k = ω/c = 2π/λ, ω = 2πf.
- Wave equation ∂²p/∂x² = (1/c²) ∂²p/∂t²; Helmholtz ∇²P + k²P = 0. Euler: jωρU = −dP/dx.
- Forward plane wave: P = A e^{−jkx}, **U = P/ρc** (in phase). Backward wave: U = −P/ρc.
- Displacement Ξ = U/(jω), |Ξ| = |P|/(ωρc). Adiabatic cavity: p = −γ p₀ ΔV/V.
- Two waves: P = P_i e^{−jkx} + P_r e^{+jkx}, **U = (P_i e^{−jkx} − P_r e^{+jkx})/ρc** (minus!).
- R = P_r/P_i = (Z − ρc)/(Z + ρc). α = 1 − |R|². Rigid R = +1 (p max at wall, u = 0), soft R = −1.
- |p|_max = |P_i|(1+|R|), |p|_min = |P_i|(1−|R|), s = (1+|R|)/(1−|R|), |R| = (s−1)/(s+1).
- Rigid end: P = 2P_i cos kx, pressure nodes at d = (2n+1)λ/4 from the wall, spaced λ/2.
- Net intensity I = |P_i|²(1−|R|²)/(2ρc), the same at every x.
- **Two media (normal):** R₁₂ = (Z₂−Z₁)/(Z₂+Z₁), T_p = 2Z₂/(Z₁+Z₂), τ = 4Z₁Z₂/(Z₁+Z₂)² = 1 − R². Air↔water: τ ≈ 1.1 × 10⁻³ (−29.5 dB) both ways, but T_p ≈ 2 into water. Bubbles in water = soft → R < 0 (2022 MC1).
- **Tubes:** open–open and closed–closed f_n = nc/2L; closed–open f_n = (2n−1)c/4L (odd harmonics). Ear canal 25 mm → 3.4 kHz.
- **Driven end (2023 P1):** termination at x = 0, piston at x = −L with velocity U₀: A = ρcU₀ / (e^{jkL} − R e^{−jkL}), p = A(e^{−jkx} + R e^{jkx}). Absorber (R = 0): |p| = ρcU₀ everywhere. Rigid/water (R ≈ 1): p = 2A cos kx, blows up where sin kL = 0.

## 2. Levels, adding, L_eq, bands, A-weighting (L3) → `T03`, `T04`

[[Lecture 3 - Decibels Frequency Analysis and Measurements]] · [[Week 3 - Decibels Frequency Analysis and Measurements]]

- L_p = 20 log(p_rms/p_ref), p_rms = |P|/√2. Crest factor of a tone √2 (3 dB).
- Different frequencies: p²_rms = Σ|A_i|²/2. Same frequency: p_rms = |A₁ + A₂|/√2. Equal tones with phase φ: ΔL = 10 log(2 + 2cos φ): 0° +6, 90° +3, 120° 0, 180° −∞.
- Uncorrelated sum L = 10 log Σ10^{L_i/10}. N equal: +10 log N. 6 dB apart: +1; 10 dB apart: +0.4.
- Background: L_src = 10 log(10^{L_tot/10} − 10^{L_bg/10}); ΔL 3 → −3.0, 6 → −1.3, 10 → −0.5 dB.
- **L_eq,T = 10 log Σ (t_i/T) 10^{L_i/10}**. On a fraction d of the time: L + 10 log d (¼ → −6.0, ⅓ → −4.8, ⅙ → −7.8).
- L_AE (one event, t₀ = 1 s): L_eq,T = L_AE + 10 log n − 10 log(T/1 s). Time constants F 125 ms, S 1 s (decay 34.7 / 4.3 dB/s).
- **Bands:** f_c = f₀ 2^{i/n}, f_l = f_c 2^{−1/(2n)}, f_u = f_c 2^{1/(2n)}. Octave: f_c/√2 … f_c√2 (Δf = 0.707 f_c). Third octave: f_c/2^{1/6} … f_c 2^{1/6} (Δf = 0.232 f_c, 1000 → 891–1122).
- Octave edges: 125: 88–177 · 250: 177–354 · 500: 354–707 · 1k: 707–1414 · 2k: 1414–2828 · 4k: 2828–5657.
- **Recipe for a tone list:** (1) merge equal frequencies as complex numbers, (2) put each frequency in its band, (3) add |P|²/2 per band, (4) 10 log. An empty band is −∞ dB, not 0 dB.
- White noise: +3 dB/octave in octave bands (+1 dB per third octave). Pink: flat in bands.
- PSD: p² = ∫S(f)df. A third-octaves into octave: 10 log of the sum of three.

**Nominal centres** (octaves bold): 20 25 31.5 40 50 **63** 80 100 **125** 160 200 **250** 315 400 **500** 630 800 **1000** 1250 1600 **2000** 2500 3150 **4000** 5000 6300 **8000** 10k 12.5k **16k** 20k Hz.

**A- and C-weighting** (dB, course text Table 1.3.2):

| f (Hz) | 31.5 | 63 | 125 | 250 | 500 | 1k | 2k | 4k | 8k | 16k |
|---|---|---|---|---|---|---|---|---|---|---|
| **A** | −39.4 | −26.2 | −16.1 | −8.6 | −3.2 | 0 | +1.2 | +1.0 | −1.1 | −6.6 |
| **C** | −3.0 | −0.8 | −0.2 | 0 | 0 | 0 | −0.2 | −0.8 | −3.0 | −8.5 |

A at third octaves: 20 −50.5 · 25 −44.7 · 40 −34.6 · 50 −30.2 · 80 −22.5 · 100 −19.1 · 160 −13.4 · 200 −10.9 · 315 −6.6 · **400 −4.8** · **630 −1.9** · 800 −0.8 · 1250 +0.6 · 1600 +1.0 · 2500 +1.3 · 3150 +1.2 · 5000 +0.5 · 6300 −0.1 · 10k −2.5 · 12.5k −4.3 · 20k −9.3.
**Weight each tone (or band) first, then add mean squares:** p_A = p_rms 10^{K/20} (2024 P1.2).

## 3. Impedance, intensity, sound power (L4) → `T05`

[[Lecture 4 - Impedance Intensity and Sound Power]] · [[Week 4 - Impedance Intensity and Sound Power]]

- z = P/U (Pa s/m), Z_m = F/v (N s/m), Z_a = P/Q (Pa s/m³). Q = SU, F = PS, **Z_a = z/S = Z_m/S²**.
- Mass jωM, spring K/(jω), Z_m = R + j(ωM − K/ω), ω₀ = √(K/M).
- Closed tube: Z_in = −j(ρc/S) cot kl. Small cavity: **C_a = V/(ρc²)**, Z = 1/(jωC_a).
- Helmholtz: M_a = ρl_eff/S, **f₀ = (c/2π)√(S/(V l_eff))**.
- **I = ½ Re{P U\*} = p_rms u_rms cos φ.** Plane wave I = p²_rms/ρc. Spherical (any r) I = |P|²/(2ρc).
- W = ∫I·n dS: plane W = IS; sphere 4πr²I; hemisphere 2πr²I. Port: W = ½|Q|² Re{Z_a}.
- Energy density w̄_p = |P|²/(4ρc²), w̄_k = ρ|U|²/4.
- **Standing-wave tube:** s = 10^{(L_max−L_min)/20}, α = 1 − ((s−1)/(s+1))² = 4s/(s+1)². W_abs = S p_max,rms p_min,rms/ρc. p_i = (p_max+p_min)/2, p_r = (p_max−p_min)/2. (s = 3 → 0.75; s = 2 → 0.89.)

## 4. Radiation: monopole, wall, dipole, piston (L5) → `T06`, `T07`

[[Lecture 5 - Radiation Monopoles Dipoles and Pistons]] · [[Week 5 - Radiation Monopoles Dipoles and Pistons]]

- **Monopole:** P = jωρQ e^{−jkr}/(4πr), **U_r = (P/ρc)(1 + 1/(jkr))**, Z_s = ρc/(1 + 1/(jkr)), p leads u by atan(1/kr) (kr = 1 → 45°, kr = 1.73 → 30°).
- p ∝ 1/r, u decays **faster** near the source. I = |P|²/(2ρc) at any r.
- **W = ρck²|Q|²/(8π)** (peak Q). Baffle / rigid plane: ρck²|Q|²/(4π). General W = ρck²|Q|²/(2Ω), Ω = 4π or 2π.
- Pulsating sphere: Q = 4πa²U, Z_a,r = (ρc/4πa²)·jka/(1+jka). Small ka: R ∝ f², mass ρ/(4πa).
- **Two sources (any):** sum complex P_i. On the line between them u_x = u₁ − u₂ (directions!). Cancellation needs equal |p| and 180°: path difference (2n+1)λ/2, so f_n = (2n+1)f₀. Equal |p| at x_c: Q₁/Q₂ = x_c/(D − x_c).
- **Rigid wall at h (image in phase):** W = (ρck²|Q|²/8π)(1 + sin 2kh/2kh). On the line source→wall: I ≈ (|p₁|² − |p₂|²)/(2ρc), zero at the wall.
- **Dipole (2h apart, antiphase):** W = (ρck²|Q|²/4π)(1 − sin 2kh/2kh) ≈ ρc h²k⁴|Q|²/(6π); far field ∝ cos θ, power ∝ f⁴, poor at low f.
- **Baffled piston:** P = (jωρQ/2πr)·2J₁(ka sinθ)/(ka sinθ). −3 dB at ka sinθ = 1.62, −6 dB at 2.22, null at 3.83. Directivity factor → 2 at low f. Radiation mass 8ρa³/3 per side. Low-ka resistance ρck²/(2π).
- Two in-phase sources close together: p ×2, W ×4 (+6 dB). Rigid wall: p ×2, W ×2 (+3 dB). Corner (3 walls): W ×8.

## 5. Room modes and the diffuse field (L6) → `T09`, `T10`

[[Lecture 6 - Room Modes and the Diffuse Sound Field]] · [[Week 6 - Room Modes and the Diffuse Sound Field]]

- **f = (c/2)√((n_x/l_x)² + (n_y/l_y)² + (n_z/l_z)²).** Axial (1 index), tangential (2), oblique (3).
- Odd index → node in the centre (only all-even modes heard there). All modes max in corners. (2,0,0): nodes at l_x/4, 3l_x/4. Cube: permutations degenerate.
- N(f) ≈ (4πV/3)(f/c)³ + (πS/4)(f/c)² + (L/8)(f/c); dN/df ≈ 4πVf²/c³. Schroeder f_S ≈ 2000√(T/V).
- Diffuse field: incident intensity on a wall **I = p²/(4ρc)** (rms). Energy density w = p²/(ρc²).
- **A = Σ S_i α_i + Σ A_obj + 4mV**, ᾱ = A/S. Person ≈ 0.4–0.6 m² (0.42 seated student).
- **Sabine T = 55.3V/(cA) ≈ 0.16V/A.** **Eyring T = 0.16V/(−S ln(1−ᾱ))**. Air: + 4mV. Mean free path l_m = 4V/S. Decay 60/T dB/s.
- Steady state **p² = 4Wρc/A** → L_p ≈ L_W + 10 log(4/A).
- **L_p = L_W + 10 log(Q/(4πr²) + 4/R)**, R = A/(1−ᾱ) ≈ A. r_rev = √(QA/(16π)) ≈ 0.14√(QA).
- **L_W from a reverberation room:** L_W = L̄_p + 10 log V − 10 log T − 14 dB.
- **ISO 354:** α = (0.16V/S)(1/T₂ − 1/T₁) (+α_floor). Can exceed 1 (edge diffraction).
- All absorption in the ceiling: T = 0.16h/α (non-diffuse → real T longer).
- T20 = 3(t₋₂₅ − t₋₅), T30 = 2(t₋₃₅ − t₋₅), EDT = 6(t₋₁₀ − t₀). Echo: > 50 ms (17 m extra path).
- Targets: lecture 0.8–1.2 s, classroom 0.6–0.9 s, symphony 1.5–2.2 s.

## 6. Absorbers (L7) → `T11`

[[Lecture 7 - Sound Absorption and Room Acoustic Design]] · [[Week 7 - Sound Absorbers]]

- Porous: works above **f ≈ c/(4d)** (d from the **wall**), dip at d = λ/2, peak again 3λ/4. Air gap = cheap low-f absorption. Diffuse: good above λ/8.
- **Membrane: f_r = (1/2π)√(ρc²/(mL)) ≈ 60/√(mL)**, m = kg/m² (density × thickness), L = cavity depth. Reverse: L = ρc²/(m ω²).
- **Helmholtz: f₀ = (c/2π)√(s/(V(l+δ)))**, s = πd²/4, δ ≈ 0.8d (diameter). Reverse: V = (s/l_eff)(c/(2πf))².
- **Perforated panel: f₀ = (c/2π)√(P/(L(l+δ)))**, P = πd²/(4a²) (fraction). L = cavity depth, l = panel thickness.
- **α from Z:** R = (Z − ρc)/(Z + ρc), α_n = 1 − |R|² = 4r/((r+1)² + x²) with ζ = Z/ρc = r + jx. Oblique: Z cosθ instead of Z. Random (Paris): α_r = ∫₀^{π/2} α(θ) sin 2θ dθ (closed form in `T11`). **Normalise by ρc first.** Max α_r ≈ 0.95.
- Reflected level: L_refl = L_inc + 10 log(1 − α). (α 0.5 → −3, 0.9 → −10, 0.99 → −20 dB.)
- Scattering: (1−α)δ scattered, (1−α)(1−δ) specular.

## 7. Loudspeakers (L8) → `T08`

[[Lecture 8 - Loudspeakers]] · [[Week 8 - Loudspeakers]]

- F = Bl·e/R_e, **Z_M = R_t + j(ωM − K/ω)**, U = F/Z_M, **Q = SU = S Bl e/(R_e Z_M)**, S = πa². Use peak e = √2 e_rms.
- R_t already contains (Bl)²/R_e. f_s = (1/2π)√(K/M), Q_t = √(KM)/R_t.
- **p = ρω|Q|/(Ωr)** (Ω = 2π baffle, 4π box in free space). W = Ωr²|p|²/(2ρc).
- Mass-controlled (f ≫ f_s): **p = ρ S Bl e/(Ω r R_e M)**, frequency independent. Below f_s: −12 dB/oct. Vented box: −24 dB/oct below f_B.
- Excursion x = U/(jω) ∝ 1/f² above f_s.
- Z_e = R_e + jωL_e + (Bl)²/Z_M; peak R_e + (Bl)²/R_m at f_s.
- Closed box K_box = ρc²S²/V; f_c = (1/2π)√((K+K_box)/M). Internal pressure p = ρc²Sx/V.
- **Headphone/cavity:** C_A = V/(ρc²), p = Q/(jωC_A) (follows displacement, flat below resonance). Off the head: p = ρωQ/(4πr).

## 8. Hearing: selectivity and masking (L9) → `T12`

[[Lecture 9 - Hearing - Frequency Selectivity and Masking]] · [[Week 9 - Psychological Acoustics]]

- **ERB = 24.7(4.37F + 1) Hz, F in kHz** (100 Hz 35.5 · 500 78.7 · 1k 132.6 · 2k 240.6 · 4k 456.5 · 10k 1104). Bark CB = 25 + 75(1+1.4F²)^{0.69}. Third octave 0.232f. ERB < third octave above ≈ 200 Hz.
- **Power-spectrum model:** P_s = k∫W(f)N(f)df. Rectangular filter: **L_s = N₀,dB + 10 log k + 10 log min(Δf_noise, ERB)**.
- Combination tones (f₁ < f₂): f₁ − n(f₂ − f₁), strongest 2f₁ − f₂ (below f₁, moves opposite to f₂). DPOAE at 2f₁ − f₂.
- Two tones in one ERB → one tone beating at |Δf|; in separate filters → two tones.
- Loudness N = 2^{(L−40)/10} sone (+10 phon = ×2). Wider than ERB at same power → louder (summation).
- roex W(g) = (1+pg)e^{−pg}, g = |f−f_c|/f_c, ERB = 4f_c/p. Notched noise avoids off-frequency listening.
- **MC facts:** base = high f (stiff, narrow), apex = low f. OHC = amplifier (level-dependent gain, compression 0.18 dB/dB ≈ 5.6:1, only near CF), IHC = sensor. Filters broaden with level on the **low** side → masking spreads **upward**. Sensorineural (OHC) loss: higher threshold, broader filters, less compression, **loudness recruitment** (faster growth), weaker combination tones. Forward masking ≈ 200 ms, backward ≈ 20 ms.

## 9. Physiological acoustics (L10) → `T13`

[[Lecture 10 - Physiological Acoustics]] · [[Week 10 - Physiological Acoustics]]

- **Greenwood:** F = A·10^{−Gx} − B, A = 20682, G = 61.765 m⁻¹, B = 140.6, **x from the base in metres**. Inverse x = −(1/G) log₁₀((F+B)/A). Base 20.5 kHz, apex (34 mm) 24 Hz, 1 kHz at 20.4 mm, ≈ 4.9 mm/octave.
- OAE: x = c_BM t_rt/2 (halve the roundtrip), then Greenwood.
- **ABR averaging:** SNR₁ = 20 log(EP/N), SNR_n = SNR₁ + **10 log n** (+3 dB per doubling). Mixed noise: N_eff² = Σw_i N_i². Rejected sweeps still cost time: n_presented = n_clean/(1 − fraction bad).
- Middle ear: area 14 × lever 1.3 ≈ 18 → **≈ 25 dB**; bare air→fluid ≈ −29.5 dB. Stapedius reflex > 70 dB, too slow for impulses. Ear canal λ/4 ≈ 3.4 kHz.
- OAE tests OHCs (cochlea), ABR tests the neural path. Wave V: latency up, amplitude down at lower level. DPOAE = distortion source (flat phase); SFOAE/CEOAE = reflection source (rotating phase).

## 10. Vibration isolation (L11) → `T14`

[[Lecture 11 - Structure-borne Sound and Vibration Isolation]] · [[Week 11 - Structure-borne Sound and Vibration Isolation]]

- m ẍ + r ẋ + s x = F. ω₀ = √(s/m), ζ = r/(2√(ms)), η = 2ζ.
- **Static deflection: s = mg/ξ₀, f₀ = (1/2π)√(g/ξ₀) ≈ 0.5/√ξ₀** (ξ₀ in m: 1 cm → 5.0 Hz, 1.5 cm → 4.1 Hz).
- x = F/(s − ω²m + jωr). Below f₀ stiffness controlled (F/s), at f₀ damping controlled, above mass controlled (F/ω²m).
- **T = √((1 + (2ζΩ)²)/((1 − Ω²)² + (2ζΩ)²)), Ω = f/f₀.** T = 1 at Ω = √2 for any ζ. Undamped T = 1/|1−Ω²|: Ω = 3 → −18 dB, 10 → −40 dB. Damping worsens isolation above √2 f₀.
- Isolation [dB] = −20 log T = 10 log E_iso. Base excitation u/u_f = same T (negative ratio above resonance).
- Springs: parallel add s; series add 1/s. Mobilities: mass 1/(jωm), spring jω/s, damper 1/r.
- Source on receiver: **F = v_free/(Y_S + Y_R)** (rigid floor Y_R = 0). With isolator: E_iso = |1 + (jω/s)/(Y_S + Y_R)|². Infinite plate Y = 1/(8√(B'm'')).
- Accelerometer output = **charge** ∝ acceleration. Rubber dynamic stiffness > static.

## 11. Sound insulation (L12) → `T15`

[[Lecture 12 - Sound Insulation]] · [[Week 12 - Sound Insulation]]

- τ = W_t/W_i, **R = −10 log τ**. Combine elements through τ, never by averaging dB.
- **Mass law: R₀ = 20 log(ωm/(2ρc)) ≈ 20 log(fm) − 42.4** (m = kg/m²). +6 dB per doubling of m or f. **Field: R₀ − 5.**
- **Two rooms: R = L₁ − L₂ + 10 log(S/A₂)**, S = partition area, A₂ = 0.16V₂/T₂ (receiving room).
- **Composite: R_res = −10 log(Σ S_i 10^{−R_i/10}/S).** Crack τ = 1 caps R at −10 log(S_ap/S). Solve for one element: R_x = −10 log((S 10^{−R_res/10} − S_rest 10^{−R_rest/10})/S_x).
- **f_c = (c²/2π)√(m/B), B = Eh³/(12(1−ν²)), m = ρ_M h → f_c ∝ 1/h.** ≈ c²/(1.8 c_L h). Stacked loose layers: f_c unchanged. Coincidence at angle θ: f_c/sin²θ.
- Above f_c: R ≈ R₀ + 10 log(2ηf/(πf_c)) (9 dB/oct; −19 dB at f_c for η = 0.02). Thick-wall limit 20 log(ρ_M c_L/(2ρc)).
- **Double wall: f₀ = (c/2π)√((ρ/d)(1/m₁ + 1/m₂)), f_d = c/(2πd).** Ranges: R₁₊₂ (6 dB/oct) → R₁ + R₂ + 20 log(2kd) (18) → R₁ + R₂ + 6 (12). Fill the cavity, avoid ties, different leaves.
- Flanking R' = −10 log(10^{−R/10} + Σ10^{−R_F,i/10}). Impact L_n = L₂ + 10 log(A₂/10) (lower = better). R_w: shift ISO 717 curve, unfavourable sum ≤ 32 dB, read at 500 Hz.
- Enclosure: ΔL = R + 10 log α_inside. Factory → outside half space: L₂ = L₁ − R − 10 log(8πr²/S).

---

## 12. Traps (one list)

- Peak vs rms: forgetting √2 = 3 dB. SPL needs rms. Room acoustics = rms.
- Never add dB directly. Same frequency + phase = complex sum (can cancel). Different frequencies = mean squares.
- 4π vs 2π: "infinite baffle", "on the ground", "rigid plane" = 2π.
- Q is volume velocity, not quality factor or directivity factor.
- Velocity of a reflected/opposite wave has a minus sign; on the line between two sources u_x = u₁ − u₂.
- Empty band = −∞ dB. A-weight per component, then add.
- Use the exact band edges (f_c/√2, f_c√2; 2^{±1/6}), not ±10 %.
- 0.16 = 55.3/c needs V in m³, A in m². Don't mix c = 343 and 344 in one problem.
- Normalise Z by ρc before the random-incidence formula (0.53 vs 0.0032).
- Membrane: m in kg/m², not density. Perforated: P as a fraction; L cavity, l panel.
- Isolation starts at √2 f₀, not f₀. More damping is worse above √2 f₀. ξ₀ in metres.
- Greenwood x in metres from the base; OAE roundtrip /2.
- ERB formula takes kHz. dB/Hz is a density: add 10 log(bandwidth).
- Averaging gains 10 log n (not 20 log n). Average noise **powers**, not amplitudes.
- S in 10 log(S/A₂) is the wall area. Field incidence −5 dB.
- f_c goes down with thickness. Stacked plates keep f_c (the trap option is f_c/2).
- Below f₀ a double wall is worse than one leaf of the same total mass.
- Mass-controlled loudspeaker: p ∝ ωQ, so a third of the Q at 3× f gives the same p.

## 13. Where the old exams asked what

| Topic | Part 1 (problems) | Part 2 (MC) |
|---|---|---|
| Plane waves / reflection | 2023 P1 (tunnel), 2024 P1 (absorber + A-weighting) | 2022 Q1 bubbles, 2024 Venus ρc |
| Levels, L_eq, bands | 2022 P2, 2023 P2 (octave bands of tones) | 2022 Q2–3, 2023 Q1, 2024 Q2 |
| Monopole / two sources / wall | 2022 P3, 2023 P3, 2024 P2 | 2023 Q2 near field, Q4 dipole, 2024 Q1 phase |
| Loudspeaker | 2022 P1 | — |
| Room modes | — | 2022 Q4, 2023 Q3, 2024 Q5 |
| Reverberation, L_p from L_W | — | 2022 Q5, Q7, 2023 Q5, Q7, 2024 Q4 |
| Absorbers | — | 2022 Q6, 2023 Q6, 2024 Q6–7 |
| Insulation | — | 2022 Q8–9, 2023 Q8, Q10, 2024 Q8, Q11 |
| Vibration | — | 2022 Q10–11, 2023 Q9, Q11, 2024 Q9–10 |
| Hearing | — | last 3–4 questions every year |

Part 1 has so far always been L1–L5 + L8 (waves, levels, radiation, loudspeaker). Part 2 covers everything.
