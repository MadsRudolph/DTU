# 34840 exam toolkit (MATLAB)

Fill-in templates for every problem type in the 34840 written exam
(Fri 11 Dec 2026, all aids, no internet). Each template is a plain script:

1. Open it, read the header (what it solves, which old exam / sheet problems it matches).
2. Edit the `GIVEN - edit these` block (or the GIVEN lines inside a lettered block).
3. Run it (F5 or `run T07_two_sources_wall_dipole`). Every line without a semicolon prints its result.
4. Copy the numbers you need. The comments next to each line say what the pre-filled answer should be.

Every template is pre-filled with a real exam or sheet problem, so running it
unchanged reproduces a known official answer. That is your test that nothing is broken.

`run_all_checks` runs all 15 templates and compares 116 pre-filled results with the
official answers. Run it once on the exam laptop **with Wi-Fi off** the day before.
Last run (26-Nov-2026, R2026a): **116 of 116 checks passed**.

```
cd "5. Semester/Acoustics and Noise Control/Exam/toolkit"
matlab -batch run_all_checks        # or just type run_all_checks in MATLAB
```

## Which template for which question

| Question looks like … | Template | Pre-filled with |
|---|---|---|
| Plane wave on an absorber/wall, given α or R or Z; pressure at distance d; air↔water | `T01_plane_wave_reflection` | 2024 P1.1 (0.89 / 0.86 Pa), Week 4 P3 |
| Vibrating end wall drives a tube/tunnel; termination absorber/water/open; tube resonances, nodes | `T02_tube_driven_end` | 2023 P1.1–1.2 (83.1 / 109.9 dB) |
| SPL from amplitude, adding dB, coherent vs incoherent, background noise, L_eq of on/off source, L_AE | `T03_levels_adding_Leq` | 2022 MC2–3, 2024 MC2, 2023 MC1, Week 3 |
| List of tones (harmonics, two sources) → octave / third-octave band SPL; A-weighting | `T04_octave_bands_A_weighting` | 2023 P2 (70.9/77.0/70.1/57.0, detuned 67.1), 2024 P1.2 (89.7 dB(A)), 2022 P2 as alternative |
| Intensity from p and u, power from SPL, standing-wave ratio → α, absorbed power | `T05_intensity_power_SWR` | Week 4 P2, P4 |
| One monopole: p, u, near-field phase, intensity, power, L_p ↔ L_W | `T06_monopole_nearfield_power` | 2024 P2.1, 2024 MC1 (30°), Week 8 P1 |
| Two monopoles on a line (in phase / antiphase), cancellation, monopole near a rigid wall, dipole, sources at 2-D positions | `T07_two_sources_wall_dipole` | 2024 P2.2, 2023 P3, 2022 P3 |
| Loudspeaker (Re, Bl, M, K, Rt, a): Q, SPL, power, excursion, Z_e, directivity, closed box, headphone cavity | `T08_loudspeaker` | 2022 P1, Week 8 P3–P4 |
| Room modes, mode in a band, centre/corner, dimension from a mode, mode count | `T09_room_modes` | Week 6 P1, 2022 MC4, 2023 MC3, 2024 MC5 |
| Sabine/Eyring, α needed for target T, L_p from L_W (direct + reverberant), r_rev, ISO 354, L_W in reverb room | `T10_reverberation_diffuse_field` | 2022 MC5/MC7, 2023 MC5/MC7, 2024 MC4, Week 6 P3, Week 7 P1 |
| Membrane, Helmholtz, perforated panel, porous λ/4, α from Z (normal/oblique/random) | `T11_absorbers` | Week 7 P2, 2023 MC6, 2024 MC6–7, slide 36, 2022 MC6 |
| ERB, masked threshold (power spectrum model), combination tones, same filter?, sone/phon | `T12_hearing_ERB_masking` | Week 9 exercise, 2022/2023 MC14 |
| Greenwood map, OAE latency → frequency, ABR averaging, ear canal, middle ear | `T13_physiology_greenwood_ABR` | Week 10 exercise |
| Mass on springs: f0, static deflection, transmissibility, forced response, base excitation, mobility force | `T14_vibration_isolation` | 2022 MC11, 2023 MC (4.1 Hz, j3.14 N), 2024 MC (7.04 Hz), Week 11 P3–P4 |
| Mass law, two rooms (L2), door/window/crack, f_c, stacking, double wall, flanking, L_n | `T15_sound_insulation` | 2022 MC8–9, 2023 MC8, 2024 MC8/MC11, sheet P3 |

## Known differences from the official solutions (all inside the checks' tolerance)

- **2023 P1.1**: exact 83.3 dB; the official 83.1 dB writes 0.413/√2 as 0.286 Pa.
- **2023 P2.1 250 Hz band**: exact 71.0 dB; the official 70.9 rounds p_rms to 0.07 Pa.
- **2023 P3**: the official powers (32.7/36.6/54.4 µW) and pressures are about 2 % below ours with ρ = 1.2. They look like ρ ≈ 1.18 was used. Our 33.2/37.3/55.3 µW is what the stated constants give.
- **2022 MC4**: the official MATLAB line has `2/ly^2` instead of `(2/ly)^2` and gets exactly 4 m. Correct physics gives 4.25 m; the answer is still option B.
- **2022 MC11**: 0.25 dB with the exact f0 = 4.985 Hz, 0.35 dB with f0 rounded to 5 Hz. Either way "≈ 0 dB", answer A.
- **Week 7 P2.2**: 431 Hz with c = 343, 432 Hz with c = 344.

## Style

Equation first as a comment (`% $$ … $$`), then one plain MATLAB line, result printed.
No helper functions, no loops, no printf in the templates (only `run_all_checks` uses them).
Constants are ρ = 1.2 kg/m³, c = 343 m/s, as every exam since 2022 prescribes.
