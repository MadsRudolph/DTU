// 34840 Exam App — Solver Metadata, Form Definitions, Decision Flags & Presets (T01..T15)

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.SOLVERS_META = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  return [
    {
      id: 'T01_plane_wave_reflection',
      code: 'T01',
      title: 'Plane Wave Reflection & Media Transmission',
      shortTitle: 'Plane Wave Reflection',
      lecture: 'L1–L2, L4',
      matches: '2024 P1.1 (0.89 / 0.86 Pa), Week 4 P3 (air↔water 29.5 dB), 2022 MC1 (bubbles), 2024 MC3 (Venus)',
      keywords: 'plane wave reflection absorber wall impedance alpha reflection coefficient R standing wave air water transmission loss bubbles venus normal incidence pressure distance d front',
      description: 'Plane wave at normal incidence hitting a surface with known absorption α, reflection coefficient R, or impedance Z. Computes total pressure |p|, velocity |u|, active intensity I at distance d in front of the surface, SWR, and transmission into a second medium.',
      decisions: [
        { tag: 'Peak vs RMS', text: 'Exam gives peak pressure amplitudes ("amplitude 0.9 Pa") → keep "Input is Peak" and divide |p| by √2 before SPL.' },
        { tag: 'Sign of R', text: 'α only fixes |R| = √(1-α). Hard wall / water from air / "positive R": R > 0 (pressure max at x=0). Soft / bubbles in water / open end: R < 0 (pressure min at x=0).' },
        { tag: 'Velocity Sign', text: 'Reflected wave travels in +x, so u(x) = (p_i e^{-jkx} - R p_i e^{+jkx}) / (ρc) has a MINUS sign!' }
      ],
      presets: [
        { name: '2024 P1.1 — Absorber at 400 & 630 Hz (Default)', values: { mode: 'alpha', f: '400, 630', p_i: '0.9, 0.4+0.4j', alpha: '0.9999, 0.19', R_sign: 1, d: 0.6, z1: 411.6, z2: 1480000 } },
        { name: 'Week 4 P3 — Air ↔ Water Transmission', values: { mode: 'alpha', f: '1000', p_i: '1.0', alpha: '0', R_sign: 1, d: 0, z1: 411.6, z2: 1480000 } },
        { name: '2024 MC3 — Ideal Absorber on Venus', values: { mode: 'Z', f: '500', p_i: '1.0', Z: '50000', d: 0.5, rho_planet: 100, c_planet: 500 } },
        { name: 'Slide 36 — Surface Impedance Z = 500 + 1000j', values: { mode: 'Z', f: '500', p_i: '1.0', Z: '500+1000j', d: 0.5 } }
      ],
      fields: [
        { id: 'mode', label: 'Surface specified by', type: 'select', options: [{ value: 'alpha', label: 'Absorption α & sign of R' }, { value: 'Z', label: 'Surface impedance Z [Pa·s/m]' }, { value: 'R', label: 'Reflection coeff R directly' }], default: 'alpha' },
        { id: 'f', label: 'Frequencies f (comma-sep)', unit: 'Hz', type: 'text', default: '400, 630' },
        { id: 'p_i', label: 'Incident complex pressure p_i', unit: 'Pa (peak)', type: 'text', default: '0.9, 0.4+0.4j', help: 'Supports real or complex (e.g. 0.4+0.4j)' },
        { id: 'alpha', label: 'Absorption coeff α (if mode=α)', unit: '0..1', type: 'text', default: '0.9999, 0.19' },
        { id: 'R_sign', label: 'Sign of R (if mode=α)', unit: '+1 or -1', type: 'select', options: [{ value: 1, label: '+1 (Hard / positive R)' }, { value: -1, label: '-1 (Soft / bubbles / open)' }], default: 1 },
        { id: 'Z', label: 'Surface impedance Z (if mode=Z)', unit: 'Pa·s/m', type: 'text', default: '500+1000j' },
        { id: 'R_direct', label: 'Reflection R (if mode=R)', unit: 'complex', type: 'text', default: '0.01, 0.9' },
        { id: 'd', label: 'Distance d in front of surface', unit: 'm', type: 'number', step: '0.05', default: 0.6 },
        { id: 'z1', label: 'Medium 1 impedance z₁', unit: 'Pa·s/m', type: 'number', default: 411.6 },
        { id: 'z2', label: 'Medium 2 impedance z₂ (water=1.48e6)', unit: 'Pa·s/m', type: 'number', default: 1480000 }
      ]
    },
    {
      id: 'T02_tube_driven_end',
      code: 'T02',
      title: 'Tube / Tunnel Driven by Vibrating End Wall',
      shortTitle: 'Driven Tube / Tunnel',
      lecture: 'L2, L4',
      matches: '2023 P1.1 & P1.2 (tunnel with absorber 83.3 dB vs water 109.9 dB), Week 2 P1–P2 (resonances, ear canal)',
      keywords: 'tube tunnel vibrating wall piston velocity U0 termination absorber water soaked standing wave resonances open closed ear canal nodes',
      description: 'Uniform tube or tunnel of length L driven at x = -L by a vibrating wall with velocity amplitude U₀, terminated at x = 0 by an absorber (R=0) or reflective surface/water (R≈1). Also gives open/closed tube resonances and node positions.',
      decisions: [
        { tag: 'Absorber (R=0)', text: 'Pure progressive plane wave: |p| = ρc·U₀ is identical at every distance x along the tunnel.' },
        { tag: 'Water/Rigid (R≈1)', text: 'Standing wave: p(x) = 2A cos(kx), A = ρcU₀ / (2j sin kL). Pressure maximum at water (x=0), nodes every λ/2.' },
        { tag: 'Resonance Alert', text: 'When sin(kL) ≈ 0 (e.g. L=20 m, f=240 Hz, c=343 m/s → sin(kL)=0.037), the tube sits near a resonance and SPL is huge (~110 dB).' }
      ],
      presets: [
        { name: '2023 P1.1 & P1.2 — 20 m Tunnel at 240 Hz (Default)', values: { f: 240, U0: 0.001, L: 20, x_from_wall: 8, Z_end: 1480000, L_tube: 0.025 } },
        { name: '2023 P1 with c = 344 m/s (Off-resonance comparison)', values: { f: 240, U0: 0.001, L: 20, x_from_wall: 8, Z_end: 1480000, c: 344 } },
        { name: 'Ear Canal 25 mm (Closed–Open λ/4 Resonance)', values: { f: 3430, U0: 0.001, L: 0.025, x_from_wall: 0.025, Z_end: 1480000, L_tube: 0.025 } }
      ],
      fields: [
        { id: 'f', label: 'Driving frequency f', unit: 'Hz', type: 'number', default: 240 },
        { id: 'U0', label: 'Wall velocity amplitude U₀ (peak)', unit: 'm/s', type: 'number', step: '0.0001', default: 0.001 },
        { id: 'L', label: 'Tube / tunnel length L', unit: 'm', type: 'number', step: '0.5', default: 20 },
        { id: 'x_from_wall', label: 'Distance from vibrating wall', unit: 'm', type: 'number', step: '0.5', default: 8 },
        { id: 'Z_end', label: 'Termination impedance Z_end', unit: 'Pa·s/m', type: 'number', default: 1480000, help: 'Water = 1.48e6 Pa·s/m' },
        { id: 'L_tube', label: 'Passive tube length (for f_n table)', unit: 'm', type: 'number', step: '0.005', default: 0.025 },
        { id: 'f_node', label: 'Frequency for node distances', unit: 'Hz', type: 'number', default: 1000 }
      ]
    },
    {
      id: 'T03_levels_adding_Leq',
      code: 'T03',
      title: 'Levels, Adding Sources, Background & L_eq',
      shortTitle: 'Levels, Adding & L_eq',
      lecture: 'L3',
      matches: '2022 MC2 (0.161 Pa), 2022 MC3 (66.2 dB), 2023 MC1 (13 dB), 2024 MC2 (62 dB), Week 3 P1/P2/P5',
      keywords: 'decibels SPL rms peak amplitude adding sources coherent incoherent phase tuning forks beat background noise correction Leq equivalent level duty cycle SEL LAE',
      description: 'All fundamental level calculations: peak amplitude ↔ RMS ↔ SPL, two tones at different frequencies (or beat average), coherent phase addition, uncorrelated source sum, background noise subtraction, and equivalent continuous level L_eq,T.',
      decisions: [
        { tag: 'Coherent vs Incoherent', text: 'Same frequency + fixed phase → add complex amplitudes (0° gives +6 dB, 120° gives 0 dB, 180° gives -∞). Different frequencies or independent noise → add p²_rms (equal levels give +3 dB).' },
        { tag: 'Beating Tones', text: 'Two close tones (e.g. 440.00 & 440.10 Hz) averaged over ≥ 1 beat period 1/Δf (10 s) behave as incoherent: p_rms = √(p̂₁²/2 + p̂₂²/2).' },
        { tag: 'On/Off L_eq', text: 'Running for fraction d = t_on/T reduces L_eq by +10 log₁₀(d): d=1/4 → -6.0 dB; d=4/24=1/6 → -7.78 dB.' }
      ],
      presets: [
        { name: 'All Pre-filled Checks (2022 MC2/MC3, 2023 MC1, 2024 MC2, Wk 3)', values: { p_hat: 0.02, p1_hat: 0.18, p2_hat: 0.14, L_one: 90, phi: 120, L_list: '10, 10', L_tot: 80, L_bg: 75, p_on: 0.1, t_on: 4, T: 24, p_on2: 0.05, duty: 0.25 } }
      ],
      fields: [
        { id: 'p_hat', label: 'A: Peak pressure amplitude p̂', unit: 'Pa', type: 'number', step: '0.01', default: 0.02 },
        { id: 'p1_hat', label: 'B: Tone 1 peak amplitude p̂₁', unit: 'Pa', type: 'number', step: '0.01', default: 0.18 },
        { id: 'p2_hat', label: 'B: Tone 2 peak amplitude p̂₂', unit: 'Pa', type: 'number', step: '0.01', default: 0.14 },
        { id: 'L_one', label: 'C: Coherent tone level (each)', unit: 'dB', type: 'number', default: 90 },
        { id: 'phi', label: 'C: Phase difference φ', unit: 'deg', type: 'number', default: 120 },
        { id: 'L_list', label: 'D: Uncorrelated levels to add', unit: 'dB list', type: 'text', default: '10, 10' },
        { id: 'L_tot', label: 'E: Total level (source + bg)', unit: 'dB', type: 'number', default: 80 },
        { id: 'L_bg', label: 'E: Background level alone', unit: 'dB', type: 'number', default: 75 },
        { id: 'p_on', label: 'F1: Active RMS pressure p_on', unit: 'Pa (rms)', type: 'number', step: '0.01', default: 0.1 },
        { id: 't_on', label: 'F1: Active duration t_on', unit: 'h (or min)', type: 'number', default: 4 },
        { id: 'T', label: 'F1: Total period T', unit: 'h (or min)', type: 'number', default: 24 },
        { id: 'p_on2', label: 'F2: Active RMS pressure (duty)', unit: 'Pa (rms)', type: 'number', step: '0.01', default: 0.05 },
        { id: 'duty', label: 'F2: Duty fraction t_on/T (15/60=0.25)', unit: '0..1', type: 'number', step: '0.05', default: 0.25 },
        { id: 'L_i', label: 'G: Interval levels L_i', unit: 'dB list', type: 'text', default: '84, 95, 71' },
        { id: 't_i', label: 'G: Interval durations t_i', unit: 'time list', type: 'text', default: '15, 5, 20' }
      ]
    },
    {
      id: 'T04_octave_bands_A_weighting',
      code: 'T04',
      title: 'Octave / Third-Octave Bands & A-Weighting',
      shortTitle: 'Octave Bands & dB(A)',
      lecture: 'L3',
      matches: '2023 P2 (cello strings: -∞ / 70.9 / 77.0 / 70.1 / 57.0 dB; detuned 67.1 dB), 2022 P2 (-∞ / 71.9 / 62.73 / 46.53 dB), 2024 P1.2 (89.7 dB(A))',
      keywords: 'octave bands third-octave bands spectral components harmonics cello strings detuned out of tune A-weighting dB(A) band edges filter',
      description: 'Takes a list of tones with complex amplitudes (e.g. harmonics from multiple sources), merges identical frequencies coherently, sorts into exact octave or third-octave bands (f_c · 2^{±1/2n}), and computes band SPLs, detuned band SPLs, and A-weighted levels.',
      decisions: [
        { tag: 'Step 1: Same f', text: 'Tones at the EXACT same frequency (e.g. 1002 Hz in 2023 P2, 1200 Hz in 2022 P2) MUST be summed as complex amplitudes P₁ + P₂ first!' },
        { tag: 'Detuned String', text: 'If one source drops 1% in frequency (2023 P2.2), the shared harmonics are now at different frequencies and add as mean squares (|P₁|²/2 + |P₂|²/2).' },
        { tag: 'A-Weight First', text: 'When A-weighting tones inside a band (2024 P1.2), apply K_A(f) to EACH tone at its own frequency before summing mean squares.' }
      ],
      presets: [
        { name: '2023 P2 — Two Cello Strings (334 & 501 Hz + harmonics, Default)', values: { f: '334, 668, 1002, 501, 1002, 1503', P: '0.1, 0.001j, 0.04, 0.2, 0.05, 0.02j', fc: '125, 250, 500, 1000, 2000', n_oct: 1, detuneCount: 3, detuneFactor: 0.99, f_B: '400, 630', p_B: '0.89, 0.86' } },
        { name: '2022 P2 — Two Sources in 250–2000 Hz Octave Bands', values: { f: '400, 800, 1200, 600, 900, 1200, 1500', P: '0.1, 0.02, 0.01, 0.05j, 0.03j, 0.01j, 0.006j', fc: '250, 500, 1000, 2000', n_oct: 1, detuneCount: 3, detuneFactor: 0.99 } },
        { name: '2024 P1.2 — Two Tones (400 & 630 Hz) A-Weighted in 500 Hz Band', values: { f: '400, 630', P: '0.89, 0.86', fc: '250, 500, 1000', n_oct: 1, f_B: '400, 630', p_B: '0.89, 0.86' } }
      ],
      fields: [
        { id: 'f', label: 'A: Component frequencies f', unit: 'Hz list', type: 'text', default: '334, 668, 1002, 501, 1002, 1503' },
        { id: 'P', label: 'A: Complex peak amplitudes P', unit: 'Pa list', type: 'text', default: '0.1, 0.001j, 0.04, 0.2, 0.05, 0.02j', help: 'Complex peak amplitudes in same order as f' },
        { id: 'fc', label: 'A: Band centre frequencies f_c', unit: 'Hz list', type: 'text', default: '125, 250, 500, 1000, 2000' },
        { id: 'n_oct', label: 'A: Bandwidth type', unit: '1 or 3', type: 'select', options: [{ value: 1, label: '1/1 Octave bands (f_c / √2 .. f_c √2)' }, { value: 3, label: '1/3 Octave bands (f_c · 2^{±1/6})' }], default: 1 },
        { id: 'detuneCount', label: 'A: # of Source 1 components to detune', unit: 'count', type: 'number', default: 3 },
        { id: 'detuneFactor', label: 'A: Detune multiplier (e.g. 0.99 = -1%)', unit: 'ratio', type: 'number', step: '0.01', default: 0.99 },
        { id: 'f_B', label: 'B: Tones for A-weighting (2024 P1.2)', unit: 'Hz list', type: 'text', default: '400, 630' },
        { id: 'p_B', label: 'B: Tone peak amplitudes |p|', unit: 'Pa list', type: 'text', default: '0.89, 0.86' },
        { id: 'fc_C', label: 'C: Band centres for L_Z / L_A', unit: 'Hz list', type: 'text', default: '125, 250, 500, 1000' },
        { id: 'L_C', label: 'C: Unweighted band levels L_i', unit: 'dB list', type: 'text', default: '70, 75, 80, 42' }
      ]
    },
    {
      id: 'T05_intensity_power_SWR',
      code: 'T05',
      title: 'Intensity, Sound Power & Standing-Wave Ratio (SWR)',
      shortTitle: 'Intensity, Power & SWR',
      lecture: 'L4',
      matches: '2024 P2.2 (459.3 nW/m²), Week 4 P2 (1.54 mW), Week 4 P4 (α = 0.69, W_abs = 0.87 µW, L_W = 59.4 dB)',
      keywords: 'intensity complex pressure velocity phase sound power standing wave ratio SWR impedance tube Lmax Lmin absorbed power',
      description: 'Computes active intensity I = ½ Re{P U*} from any complex P and U, plane-wave intensity and power from SPL and area S, and absorption α and absorbed power W_abs from standing-wave tube measurements (L_max, L_min or SWR s).',
      decisions: [
        { tag: 'Peak vs RMS in I', text: 'With peak complex phasors P and U: I = ½ Re{P U*}. With RMS values: I = p_rms u_rms cos φ (no ½).' },
        { tag: 'SWR in Tube', text: 'From dB levels: s = 10^{(L_max - L_min)/20}. From pressure ratio: use s directly. Then |R| = (s-1)/(s+1) and α = 1 - |R|² = 4s/(s+1)².' }
      ],
      presets: [
        { name: 'Default Checks (2024 P2.2, Week 4 P2 & P4)', values: { P_A: '0.02+0.0275j', U_A: '107.4e-6-44.6e-6j', Lp_B: 82, S_B: 10, Lmax: 85, Lmin: 74, S_tube: 0.01, s_direct: '' } },
        { name: 'Lecture 7 Slide 38 — SWR s = 3 → α = 0.75', values: { P_A: '0.02+0.0275j', U_A: '107.4e-6-44.6e-6j', Lp_B: 82, S_B: 10, Lmax: 85, Lmin: 74, S_tube: 0.01, s_direct: 3 } }
      ],
      fields: [
        { id: 'P_A', label: 'A: Complex pressure amplitude P (peak)', unit: 'Pa', type: 'text', default: '0.02+0.0275j' },
        { id: 'U_A', label: 'A: Complex velocity amplitude U (peak)', unit: 'm/s', type: 'text', default: '107.4e-6-44.6e-6j' },
        { id: 'Lp_B', label: 'B: Plane-wave SPL L_p', unit: 'dB', type: 'number', default: 82 },
        { id: 'S_B', label: 'B: Area S perpendicular to wave', unit: 'm²', type: 'number', default: 10 },
        { id: 'Lmax', label: 'C/D: Tube standing-wave L_max', unit: 'dB', type: 'number', default: 85 },
        { id: 'Lmin', label: 'C/D: Tube standing-wave L_min', unit: 'dB', type: 'number', default: 74 },
        { id: 's_direct', label: 'C: Or direct SWR ratio s (optional)', unit: 'ratio', type: 'text', default: '', help: 'Leave blank to compute s from Lmax and Lmin' },
        { id: 'S_tube', label: 'D: Standing-wave tube cross-section S', unit: 'm²', type: 'number', step: '0.001', default: 0.01 }
      ]
    },
    {
      id: 'T06_monopole_nearfield_power',
      code: 'T06',
      title: 'Monopole: Near Field, Velocity, Phase & Sound Power',
      shortTitle: 'Monopole & Near Field',
      lecture: 'L2, L5',
      matches: '2024 P2.1 (|p| = 30/15/10 mPa, |u| = 108/41.5/25.9 µm/s), 2024 MC1 (30° phase), 2023 MC2, Week 8 P1',
      keywords: 'monopole point source volume velocity Q near field particle velocity phase difference kr radiated power free field baffle 2pi 4pi',
      description: 'Single monopole source of volume velocity amplitude Q in free space (4π) or on a rigid plane/baffle (2π). Computes |p|, near-field |u| with the (1 + 1/jkr) factor, p–u phase angle arctan(1/kr), active intensity I, and sound power W.',
      decisions: [
        { tag: '4π vs 2π', text: 'Free space = 4πr (W = ρck²|Q|² / 8π). Rigid plane / infinite baffle = 2πr (W = ρck²|Q|² / 4π, +6 dB pressure, +3 dB power for same Q).' },
        { tag: 'Near Field (kr < 1)', text: '|p| always decays as 1/r, but |u| carries √(1 + 1/(kr)²) and decays FASTER (1/r²) close to the source! p leads u by φ = arctan(1/kr).' },
        { tag: 'Active Intensity', text: 'The 1/(jkr) near-field velocity term is 90° out of phase with p (reactive), so active intensity is I = |P|²/(2ρc) = p²_rms/(ρc) at ANY radius r.' }
      ],
      presets: [
        { name: '2024 P2.1 & 2024 MC1 — Q = 10⁻⁵ m³/s at 500 Hz (Default)', values: { Q: 1e-5, f: 500, r: '0.1, 0.2, 0.3', Omega: 12.566370614359172, f_MC: 189, r_MC: 0.5 } },
        { name: 'Week 8 P1 — 0.1 Pa Amplitude at 1 m → 0.75 m', values: { Q: 1e-5, f: 500, r: '0.75, 1.0', Omega: 12.566370614359172, p1_hat_E: 0.1, r1_E: 1.0, r2_E: 0.75 } }
      ],
      fields: [
        { id: 'Q', label: 'Volume velocity amplitude |Q| (peak)', unit: 'm³/s', type: 'number', step: '1e-6', default: 1e-5 },
        { id: 'f', label: 'Frequency f', unit: 'Hz', type: 'number', default: 500 },
        { id: 'r', label: 'Field radii r (comma-sep)', unit: 'm list', type: 'text', default: '0.1, 0.2, 0.3' },
        { id: 'Omega', label: 'Solid angle Ω', unit: 'sr', type: 'select', options: [{ value: 12.566370614359172, label: '4π (Free field)' }, { value: 6.283185307179586, label: '2π (Rigid plane / infinite baffle)' }], default: 12.566370614359172 },
        { id: 'f_MC', label: 'Phase check frequency (2024 MC1)', unit: 'Hz', type: 'number', default: 189 },
        { id: 'r_MC', label: 'Phase check distance r (2024 MC1)', unit: 'm', type: 'number', step: '0.1', default: 0.5 },
        { id: 'p1_hat_E', label: 'Block E: Known |p| at r₁ (Week 8 P1)', unit: 'Pa (peak)', type: 'number', step: '0.01', default: 0.1 },
        { id: 'r1_E', label: 'Block E: Reference distance r₁', unit: 'm', type: 'number', default: 1.0 },
        { id: 'r2_E', label: 'Block E: Target distance r₂', unit: 'm', type: 'number', default: 0.75 }
      ]
    },
    {
      id: 'T07_two_sources_wall_dipole',
      code: 'T07',
      title: 'Two Monopoles, Line Interference, Rigid Wall & Dipole',
      shortTitle: 'Two Sources, Wall & Dipole',
      lecture: 'L5',
      matches: '2024 P2.2 (antiphase line p, u, I), 2023 P3 (monopole 2 m from rigid wall), 2022 P3 (cancellation x_c=2.172 m, Q₁/Q₂=1.188, I=8.33 µW/m²)',
      keywords: 'two monopoles interference line between sources antiphase dipole rigid wall image source power cancellation frequency midpoint intensity',
      description: 'Solves all two-source Part 1 problems: (A) two sources on a line with arbitrary Q₁, Q₂ (in-phase or antiphase), (B) monopole at distance h from a rigid wall (image source power and line intensity), (C) cancellation positions/frequencies between two sources, and (D) dipole radiation.',
      decisions: [
        { tag: 'Velocity on Line', text: 'Between source 1 (at x=0) and source 2 (at x=D), source 1 pushes in +x and source 2 pushes in -x: u_x = u₁ - u₂. For antiphase sources (Q₂ = -Q₁), the two minus signs cancel so u_x ≠ 0 at the midpoint where p = 0!' },
        { tag: 'Rigid Wall at h', text: 'Image source at distance 2h IN PHASE: W_wall = W_free (1 + sin(2kh)/(2kh)). At low f (kh ≪ 1), power doubles (+3 dB). At high f (kh ≫ 1), W_wall ≈ W_free.' },
        { tag: 'Opposite Waves I', text: 'Two waves meeting head-on: official shortcut is I ≈ (|p₁|² - |p₂|²)/(2ρc) (or (p²_1,rms - p²_2,rms)/ρc). State in Part 1 that this neglects near-field cross terms.' }
      ],
      presets: [
        { name: 'All 3 Part-1 Exams Pre-filled (2024 P2.2, 2023 P3, 2022 P3)', values: { f_A: 500, D: 0.4, Q1: '1e-5', Q2: '-1e-5', x: '0.1, 0.2, 0.3', h: 2, f_B: '20, 200, 2000', Q_B: '3e-3, 4e-4, 5e-5', f_B2: 200, Q_B2: 4e-4, d_from_wall: '0, 0.5, 1', D_C: 4, f0_C: 500, Lp_mid: 80 } }
      ],
      fields: [
        { id: 'f_A', label: 'A (2024 P2.2): Frequency f_A', unit: 'Hz', type: 'number', default: 500 },
        { id: 'D', label: 'A: Source separation D', unit: 'm', type: 'number', step: '0.1', default: 0.4 },
        { id: 'Q1', label: 'A: Source 1 complex Q₁ (at x=0)', unit: 'm³/s', type: 'text', default: '1e-5' },
        { id: 'Q2', label: 'A: Source 2 complex Q₂ (at x=D)', unit: 'm³/s', type: 'text', default: '-1e-5', help: 'Negative = antiphase (180°)' },
        { id: 'x', label: 'A: Field points x on line', unit: 'm list', type: 'text', default: '0.1, 0.2, 0.3' },
        { id: 'h', label: 'B (2023 P3): Distance h from rigid wall', unit: 'm', type: 'number', step: '0.5', default: 2 },
        { id: 'f_B', label: 'B: Frequencies for wall power', unit: 'Hz list', type: 'text', default: '20, 200, 2000' },
        { id: 'Q_B', label: 'B: Source |Q| at each frequency', unit: 'm³/s list', type: 'text', default: '3e-3, 4e-4, 5e-5' },
        { id: 'f_B2', label: 'B2: Frequency for line intensity', unit: 'Hz', type: 'number', default: 200 },
        { id: 'Q_B2', label: 'B2: Source |Q| for line intensity', unit: 'm³/s', type: 'number', step: '1e-4', default: 4e-4 },
        { id: 'd_from_wall', label: 'B2: Distances from wall towards source', unit: 'm list', type: 'text', default: '0, 0.5, 1' },
        { id: 'D_C', label: 'C (2022 P3): Source spacing D', unit: 'm', type: 'number', default: 4 },
        { id: 'f0_C', label: 'C: Lowest cancellation frequency f₀', unit: 'Hz', type: 'number', default: 500 },
        { id: 'Lp_mid', label: 'C: SPL at midpoint (in phase)', unit: 'dB', type: 'number', default: 80 }
      ]
    },
    {
      id: 'T08_loudspeaker',
      code: 'T08',
      title: 'Loudspeaker Driver, Closed Box & Headphone Cavity',
      shortTitle: 'Loudspeaker & Cavity',
      lecture: 'L8',
      matches: '2022 P1 (|Q| = 0.0022 m³/s, |p(5m)| = 0.106 Pa, W = 2.1 mW), Week 8 P3 (81.65 / 67.49 / 80.96 dB), Week 8 P4 (headphone 8.55 dB)',
      keywords: 'loudspeaker moving coil driver Re Bl M K Rt cone radius baffle volume velocity Q mechanical impedance excursion closed box headphone ear cavity',
      description: 'Moving-coil loudspeaker driven by voltage e_rms in an infinite baffle (2π) or free space (4π). Calculates mechanical impedance Z_M, resonance f_s, volume velocity |Q|, pressure |p(r)|, radiated power W, cone excursion, piston directivity, closed-box f_c, and headphone cavity pressure.',
      decisions: [
        { tag: 'Voltage is RMS', text: 'Exam gives RMS voltage ("4 V rms") → multiply by √2 to get peak voltage ê = √2·e_rms before computing peak |Q| and peak |p|.' },
        { tag: 'Baffle vs Box', text: 'Infinite baffle = 2πr and W = 2πr²I. Standalone closed box in free space = 4πr and W = 4πr²I.' },
        { tag: 'Below vs Above f_s', text: 'Below f_s: stiffness controlled (-12 dB/oct). Above f_s: mass controlled (SPL is flat/frequency-independent because |Q| ∝ 1/ω cancels ω in p ∝ ω|Q|).' }
      ],
      presets: [
        { name: '2022 P1 — Baffled Loudspeaker at 200 Hz, 5 m (Default)', values: { Re: 5, Bl: 2, M: 0.010, K: 1500, Rt: 2.5, a: 0.06, e_rms: 4, f: 200, r: 5, Omega: 6.283185307179586 } },
        { name: 'Week 8 P3 — Driver at 300 Hz (Bl=8, M=20g, K=2000, Rt=18, 2.8V, 2m)', values: { Re: 5, Bl: 8, M: 0.020, K: 2000, Rt: 18, a: 0.06, e_rms: 2.8, f: 300, r: 2, Omega: 6.283185307179586 } },
        { name: 'Week 8 P3 — Driver at 30 Hz (Stiffness-controlled region)', values: { Re: 5, Bl: 8, M: 0.020, K: 2000, Rt: 18, a: 0.06, e_rms: 2.8, f: 30, r: 2, Omega: 6.283185307179586 } }
      ],
      fields: [
        { id: 'Re', label: 'DC voice-coil resistance R_e', unit: 'Ω', type: 'number', step: '0.5', default: 5 },
        { id: 'Bl', label: 'Force factor B·l', unit: 'T·m (N/A)', type: 'number', step: '0.5', default: 2 },
        { id: 'M', label: 'Moving mass M (10 g = 0.010)', unit: 'kg', type: 'number', step: '0.001', default: 0.010 },
        { id: 'K', label: 'Suspension stiffness K', unit: 'N/m', type: 'number', step: '100', default: 1500 },
        { id: 'Rt', label: 'Total mechanical damping R_t', unit: 'N·s/m', type: 'number', step: '0.5', default: 2.5 },
        { id: 'a', label: 'Piston / cone radius a (6 cm = 0.06)', unit: 'm', type: 'number', step: '0.01', default: 0.06 },
        { id: 'e_rms', label: 'Drive voltage e_rms (RMS)', unit: 'V (rms)', type: 'number', step: '0.5', default: 4 },
        { id: 'f', label: 'Frequency f', unit: 'Hz', type: 'number', default: 200 },
        { id: 'r', label: 'Observation distance r', unit: 'm', type: 'number', step: '0.5', default: 5 },
        { id: 'Omega', label: 'Mounting solid angle Ω', unit: 'sr', type: 'select', options: [{ value: 6.283185307179586, label: '2π (Infinite baffle)' }, { value: 12.566370614359172, label: '4π (Free space box)' }], default: 6.283185307179586 },
        { id: 'V_cav', label: 'G: Headphone ear cavity volume V', unit: 'm³', type: 'number', step: '1e-5', default: 50e-6 },
        { id: 'L_cav', label: 'G: SPL inside sealed ear cavity', unit: 'dB', type: 'number', default: 100 },
        { id: 'f_G', label: 'G: Headphone test frequency', unit: 'Hz', type: 'number', default: 100 },
        { id: 'r_G', label: 'G: Free-field distance off ear', unit: 'm', type: 'number', step: '0.1', default: 0.5 }
      ]
    },
    {
      id: 'T09_room_modes',
      code: 'T09',
      title: 'Room Modes of a Rectangular Room',
      shortTitle: 'Room Modes',
      lecture: 'L6',
      matches: 'Week 6 P1 (5×4×3 m: 8 modes < 80 Hz, f₁₀₀=34.3 Hz), 2022 MC4 (height l_z ≈ 4 m), 2023 MC3 ((2,0,0) in 50 Hz band), 2024 MC5 ((2,0,0) at 57 Hz)',
      keywords: 'room modes natural frequencies eigenfrequencies axial tangential oblique rectangular room corner centre node Schroeder frequency dimension',
      description: 'Lists all axial, tangential, and oblique room modes below f_max, identifies which modes fall in a target octave or 1/3-octave band, checks which modes are audible at the room centre, and solves for an unknown room dimension from two given mode frequencies.',
      decisions: [
        { tag: 'Centre vs Corner', text: 'Odd index n → cos(nπ/2) = 0 → node at the room centre. Only modes with ALL EVEN indices (e.g. (2,0,0)) are heard at the centre. ALL modes have a pressure maximum in the corners.' },
        { tag: 'Index Order', text: 'Pay close attention to which dimension is x, y, z! E.g. 2024 MC5: l_x = 6 m → f_{2,0,0} = (343/2)·(2/6) = 57.2 Hz.' }
      ],
      presets: [
        { name: 'Week 6 P1 — 5 × 4 × 3 m Room below 80 Hz (Default)', values: { lx: 5, ly: 4, lz: 3, f_max: 80, fc_band: 50, n_oct_band: 3, f_mode1: 10, f_mode2: 45, ny2_C: 2, nz2_C: 1 } },
        { name: '2023 MC3 — 7.2 × 5.4 × 3.0 m Room (50 Hz 1/3-Octave Band)', values: { lx: 7.2, ly: 5.4, lz: 3.0, f_max: 70, fc_band: 50, n_oct_band: 3 } },
        { name: '2024 MC5 — 6 × 9 × 3 m Office (Mode at 57 Hz)', values: { lx: 6, ly: 9, lz: 3, f_max: 70, fc_band: 57, n_oct_band: 3 } }
      ],
      fields: [
        { id: 'lx', label: 'Room length l_x', unit: 'm', type: 'number', step: '0.2', default: 5 },
        { id: 'ly', label: 'Room width l_y', unit: 'm', type: 'number', step: '0.2', default: 4 },
        { id: 'lz', label: 'Room height l_z', unit: 'm', type: 'number', step: '0.2', default: 3 },
        { id: 'f_max', label: 'List all modes below f_max', unit: 'Hz', type: 'number', default: 80 },
        { id: 'fc_band', label: 'Band centre frequency f_c to filter', unit: 'Hz', type: 'number', default: 50 },
        { id: 'n_oct_band', label: 'Band type', unit: '1 or 3', type: 'select', options: [{ value: 3, label: '1/3 Octave band (f_c · 2^{±1/6})' }, { value: 1, label: '1/1 Octave band (f_c / √2 .. f_c √2)' }], default: 3 },
        { id: 'T_room', label: 'Reverberation time T (for Schroeder f_S)', unit: 's', type: 'number', step: '0.1', default: 0.5 },
        { id: 'f_mode1', label: 'C (2022 MC4): Known axial f(0,1,0)', unit: 'Hz', type: 'number', default: 10 },
        { id: 'f_mode2', label: 'C: Known tangential f(0, n_y, n_z)', unit: 'Hz', type: 'number', default: 45 },
        { id: 'ny2_C', label: 'C: Index n_y of second mode', unit: 'int', type: 'number', default: 2 },
        { id: 'nz2_C', label: 'C: Index n_z of second mode', unit: 'int', type: 'number', default: 1 }
      ]
    },
    {
      id: 'T10_reverberation_diffuse_field',
      code: 'T10',
      title: 'Reverberation Time (Sabine/Eyring), Diffuse Field & ISO 354',
      shortTitle: 'Reverberation & Diffuse Field',
      lecture: 'L6–L7',
      matches: '2022 MC5 (1.6 s), 2022 MC7 (ISO 354 α=0.8), 2023 MC5 (α=0.1), 2023 MC7 (66 dB), 2024 MC4 (α=0.4), Week 6 P3, Week 7 P1',
      keywords: 'reverberation time Sabine Eyring absorption area diffuse field sound power level Lp LW reverberation distance critical radius ISO 354 chamber',
      description: 'Computes Sabine and Eyring reverberation times, required absorption coefficient α of untreated surfaces to reach a target T, steady-state SPL from L_W (direct + reverberant field), reverberation radius r_rev, and ISO 354 specimen absorption.',
      decisions: [
        { tag: 'Sabine vs Eyring', text: 'Sabine T = 0.16V/A for ᾱ < 0.3 (standard exam formula). Eyring T = 0.16V/(-S ln(1-ᾱ)) for high absorption ᾱ > 0.3.' },
        { tag: 'Remaining Area Trap', text: 'When one surface (ceiling or floor) has a known α₁ and you solve for α₂ of the other surfaces: subtract S₁α₁ from A, then divide by S_rest = S_total - S₁ (NOT S_total!).' },
        { tag: 'Direct + Reverberant', text: 'L_p = L_W + 10 log₁₀(Q/(4πr²) + 4/A). Far from the source (r ≫ r_rev ≈ 0.14√(QA)), the 4/A reverberant term dominates (don’t forget the factor 4!).' }
      ],
      presets: [
        { name: 'All Pre-filled Exam Checks (2022 MC5/7, 2023 MC5/7, 2024 MC4)', values: { lx: 10, ly: 13, lz: 8, alpha_ceiling: 0.8, alpha_rest: 0, lx_B: 6, ly_B: 7, lz_B: 3, alpha_known_B: 0.8, T_meas_B: 0.44, LW_C: 75, V_C: 200, T_C: 1, Qdir: 1, src: '1, 1, 1.7', rec: '3, 8, 1.2', V_E: 150, S_E: 9, T1: 5, T2: 2 } },
        { name: '2024 MC4 — 5 × 8 × 3 m Studio (Floor α=0.1, Target T=0.4 s)', values: { lx_B: 5, ly_B: 8, lz_B: 3, alpha_known_B: 0.1, T_meas_B: 0.4 } }
      ],
      fields: [
        { id: 'lx', label: 'A (2022 MC5): Room length l_x', unit: 'm', type: 'number', default: 10 },
        { id: 'ly', label: 'A: Room width l_y', unit: 'm', type: 'number', default: 13 },
        { id: 'lz', label: 'A: Room height l_z', unit: 'm', type: 'number', default: 8 },
        { id: 'alpha_ceiling', label: 'A: Ceiling absorption α_ceil', unit: '0..1', type: 'number', step: '0.05', default: 0.8 },
        { id: 'alpha_rest', label: 'A: Other surfaces α_rest', unit: '0..1', type: 'number', step: '0.05', default: 0 },
        { id: 'lx_B', label: 'B (2023 MC5 / 2024 MC4): Room l_x', unit: 'm', type: 'number', default: 6 },
        { id: 'ly_B', label: 'B: Room l_y', unit: 'm', type: 'number', default: 7 },
        { id: 'lz_B', label: 'B: Room l_z', unit: 'm', type: 'number', default: 3 },
        { id: 'alpha_known_B', label: 'B: Known surface α (ceiling or floor)', unit: '0..1', type: 'number', step: '0.05', default: 0.8 },
        { id: 'T_meas_B', label: 'B: Target / measured T', unit: 's', type: 'number', step: '0.05', default: 0.44 },
        { id: 'LW_C', label: 'C (2023 MC7): Source power level L_W', unit: 'dB', type: 'number', default: 75 },
        { id: 'V_C', label: 'C: Room volume V', unit: 'm³', type: 'number', default: 200 },
        { id: 'T_C', label: 'C: Reverberation time T', unit: 's', type: 'number', step: '0.1', default: 1 },
        { id: 'Qdir', label: 'C: Directivity factor Q', unit: '1, 2, 4..', type: 'number', default: 1 },
        { id: 'src', label: 'C: Source (x, y, z)', unit: 'm list', type: 'text', default: '1, 1, 1.7' },
        { id: 'rec', label: 'C: Receiver (x, y, z)', unit: 'm list', type: 'text', default: '3, 8, 1.2' },
        { id: 'V_E', label: 'E (2022 MC7 ISO 354): Chamber V', unit: 'm³', type: 'number', default: 150 },
        { id: 'S_E', label: 'E: Specimen area S', unit: 'm²', type: 'number', default: 9 },
        { id: 'T1', label: 'E: Empty chamber T₁', unit: 's', type: 'number', default: 5 },
        { id: 'T2', label: 'E: Chamber with specimen T₂', unit: 's', type: 'number', default: 2 }
      ]
    },
    {
      id: 'T11_absorbers',
      code: 'T11',
      title: 'Absorbers: Membrane, Helmholtz, Perforated, Porous & Z → α',
      shortTitle: 'Sound Absorbers',
      lecture: 'L4, L7',
      matches: '2023 MC6 (membrane 130 Hz), 2024 MC7 (membrane depth 15 cm), 2024 MC6 (Helmholtz V=0.015 m³), 2022 MC6 (Z=1), Week 7 P2, Slide 36 (Paris α_r=0.53)',
      keywords: 'absorber membrane panel Helmholtz resonator perforated panel porous quarter wavelength surface impedance normal random incidence Paris formula',
      description: 'Calculates resonance frequencies (and inverse design parameters: cavity depth L or volume V) for membrane absorbers, Helmholtz resonators, perforated panels, and porous λ/4 layers, plus normal/oblique/random-incidence (Paris) absorption α from complex impedance Z.',
      decisions: [
        { tag: 'Membrane Mass m', text: 'm is SURFACE MASS DENSITY in kg/m² (= bulk density ρ_panel × thickness h). Formula: f_r = (1/2π)√(ρc²/(m·L)) ≈ 60/√(m·L).' },
        { tag: 'Helmholtz Neck', text: 'Neck area is s = πd²/4 = πr². Watch out if the question gives diameter d (5 cm → r = 2.5 cm)! Add end correction δ ≈ 0.8d only if not told to neglect it.' },
        { tag: 'Paris Formula', text: 'Always normalise Z by ρc FIRST: ζ = Z/(ρc) = r + jx. Both very small Z (Z ≪ ρc) and very large Z (Z ≫ ρc) reflect almost everything!' }
      ],
      presets: [
        { name: 'All Pre-filled Exam & Sheet Checks (Default)', values: { m_panel: 12, L_cav: 0.05, m_A2: 2.1, L_A2: 0.1, f_A3: 350, m_A3: 0.2, V_B: 0.0004, d_B: 0.02, l_eff_B: 0.021, f_B2: 140, d_B2: 0.05, l_B2: 0.02, d_C: 0.01, a_C: 0.03, l_C: 0.02, L_C: 0.05, d_D: 0.07, Z: '500+1000j', z0: 414 } }
      ],
      fields: [
        { id: 'm_panel', label: 'A1 (Wk 7): Membrane mass m', unit: 'kg/m²', type: 'number', step: '0.5', default: 12 },
        { id: 'L_cav', label: 'A1: Membrane cavity depth L', unit: 'm', type: 'number', step: '0.01', default: 0.05 },
        { id: 'm_A2', label: 'A2 (2023 MC6): Membrane mass m', unit: 'kg/m²', type: 'number', step: '0.1', default: 2.1 },
        { id: 'L_A2', label: 'A2: Membrane cavity depth L', unit: 'm', type: 'number', step: '0.01', default: 0.1 },
        { id: 'f_A3', label: 'A3 (2024 MC7): Target f_r (solve for L)', unit: 'Hz', type: 'number', default: 350 },
        { id: 'm_A3', label: 'A3: Membrane mass m', unit: 'kg/m²', type: 'number', step: '0.05', default: 0.2 },
        { id: 'V_B', label: 'B1 (Wk 4): Helmholtz volume V', unit: 'm³', type: 'number', step: '0.0001', default: 0.0004 },
        { id: 'd_B', label: 'B1: Neck diameter d', unit: 'm', type: 'number', step: '0.005', default: 0.02 },
        { id: 'l_eff_B', label: 'B1: Effective neck length l_eff', unit: 'm', type: 'number', step: '0.001', default: 0.021 },
        { id: 'f_B2', label: 'B2 (2024 MC6): Target f₀ (solve for V)', unit: 'Hz', type: 'number', default: 140 },
        { id: 'd_B2', label: 'B2: Neck diameter d (5 cm = 0.05)', unit: 'm', type: 'number', step: '0.01', default: 0.05 },
        { id: 'l_B2', label: 'B2: Neck length l (2 cm = 0.02)', unit: 'm', type: 'number', step: '0.005', default: 0.02 },
        { id: 'd_C', label: 'C (Perforated): Hole diameter d', unit: 'm', type: 'number', step: '0.001', default: 0.01 },
        { id: 'a_C', label: 'C: Hole grid spacing a', unit: 'm', type: 'number', step: '0.005', default: 0.03 },
        { id: 'l_C', label: 'C: Panel thickness l', unit: 'm', type: 'number', step: '0.005', default: 0.02 },
        { id: 'L_C', label: 'C: Cavity depth L', unit: 'm', type: 'number', step: '0.01', default: 0.05 },
        { id: 'Z', label: 'E: Complex surface impedance Z', unit: 'Pa·s/m', type: 'text', default: '500+1000j' },
        { id: 'z0', label: 'E: Reference ρc for Z normalisation', unit: 'Pa·s/m', type: 'number', default: 414 }
      ]
    },
    {
      id: 'T12_hearing_ERB_masking',
      code: 'T12',
      title: 'Hearing: ERB, Power-Spectrum Masking & Combination Tones',
      shortTitle: 'Hearing: ERB & Masking',
      lecture: 'L9',
      matches: 'Week 9 P1 & P3 (ERB 35.5 / 132.6 / 1104.1 Hz, masked thresholds, combination tones), 2022 MC14 (850/900 Hz), 2023 MC14 (400/600 Hz)',
      keywords: 'hearing psychoacoustics ERB equivalent rectangular bandwidth critical band Bark masking power spectrum model noise density combination tones cubic difference tone 2f1-f2 beating sone phon loudness',
      description: 'Computes ERB (and Bark critical bandwidth / third-octave width), masked tone threshold L_s in broadband or narrowband noise, combination-tone frequencies f₁ - n(f₂ - f₁) and masking noise density N₀, two-tone filter resolution (beating vs separate tones), and sone/phon loudness.',
      decisions: [
        { tag: 'F in kHz!', text: 'In ERB = 24.7(4.37·F + 1), F MUST be in kHz (e.g. 100 Hz → F = 0.1; 1000 Hz → F = 1.0).' },
        { tag: '1 vs 2 Filters', text: 'If |f₂ - f₁| < ERB(f_mid), the two tones fall in ONE auditory filter and beat at |f₂ - f₁| Hz (2022 MC14: 850 & 900 Hz). If |f₂ - f₁| > ERB, they are heard as TWO separate tones (2023 MC14: 400 & 600 Hz).' },
        { tag: 'Combination Tone', text: 'For primaries f₁ < f₂, the cubic difference tone is 2f₁ - f₂, which is always BELOW f₁ (never above f₂!).' }
      ],
      presets: [
        { name: 'Week 9 Exercise & 2022 MC14 (Default)', values: { F: '0.1, 1, 10', N0_dB: 40, k: 0.3, df_noise: 'Inf', f1: 1.0, f2: 1.1, L1: 50, fa: 850, fb: 900 } },
        { name: '2023 MC14 — 400 Hz and 600 Hz Tones', values: { F: '0.4, 0.5, 0.6', N0_dB: 40, k: 0.3, df_noise: 'Inf', f1: 0.4, f2: 0.6, L1: 50, fa: 400, fb: 600 } }
      ],
      fields: [
        { id: 'F', label: 'A: Centre frequencies F (in kHz!)', unit: 'kHz list', type: 'text', default: '0.1, 1, 10' },
        { id: 'N0_dB', label: 'B: Noise spectrum density N₀', unit: 'dB/Hz', type: 'number', default: 40 },
        { id: 'k', label: 'B: Detector efficiency ratio k', unit: 'linear', type: 'number', step: '0.05', default: 0.3 },
        { id: 'df_noise', label: 'B: Noise bandwidth Δf (Inf = broadband)', unit: 'Hz', type: 'text', default: 'Inf' },
        { id: 'f1', label: 'C: Primary tone f₁ (lower, in kHz)', unit: 'kHz', type: 'number', step: '0.1', default: 1.0 },
        { id: 'f2', label: 'C: Primary tone f₂ (higher, in kHz)', unit: 'kHz', type: 'number', step: '0.1', default: 1.1 },
        { id: 'L1', label: 'C: Primary tone level L₁', unit: 'dB SPL', type: 'number', default: 50 },
        { id: 'fa', label: 'E: Two-tone test f_a (in Hz)', unit: 'Hz', type: 'number', default: 850 },
        { id: 'fb', label: 'E: Two-tone test f_b (in Hz)', unit: 'Hz', type: 'number', default: 900 },
        { id: 'L_phon', label: 'F: Loudness levels in phon', unit: 'phon list', type: 'text', default: '40, 50, 60' }
      ]
    },
    {
      id: 'T13_physiology_greenwood_ABR',
      code: 'T13',
      title: 'Physiology: Greenwood Map, OAE Latency & ABR Averaging',
      shortTitle: 'Physiology: Greenwood & ABR',
      lecture: 'L10',
      matches: 'Week 10 P1 (base 20541 Hz, apex 23.7 Hz), P2 (ABR 1000 sweeps / 50 s, artifact rejection 545 s vs 55.6 s), P3 (OAE 12/7/5 ms → 1458/4505/6977 Hz)',
      keywords: 'physiology cochlea basilar membrane Greenwood map base apex OAE otoacoustic emission roundtrip latency ABR averaging SNR sweeps artifact rejection middle ear',
      description: 'Solves the Greenwood cochlear frequency–place map (forward and inverse), OAE roundtrip travel time to place and characteristic frequency, and ABR signal averaging (sweeps needed, recording duration, and artifact rejection vs no rejection).',
      decisions: [
        { tag: 'x from Base in m', text: 'Greenwood: F_c(x) = A·10^{-Gx} - B uses x in METRES measured from the BASE (x=0 is high frequency ~20.5 kHz; x=0.034 m is apex ~23.7 Hz).' },
        { tag: 'OAE Roundtrip / 2', text: 'An OAE travels in to the characteristic place x and back out, so x = c_BM · t_rt / 2 (halve the roundtrip time!).' },
        { tag: 'ABR Averaging', text: 'SNR improves by +10 log₁₀(n) (+3.01 dB per doubling of sweeps). Mixed noise averages by POWER: N_eff = √((1-p)N₁² + p·N_bad²).' }
      ],
      presets: [
        { name: 'Week 10 Exercise — Greenwood, OAE & ABR (Default)', values: { A: 20682, G: 61.765, B: 140.6, L_cochlea: 0.034, f_query: 1000, x_query_mm: 20.4, c_BM: 3, t_rt_ms: '12, 7, 5', EP: 0.3e-6, N1: 3e-6, rate: 20, SNR_target_dB: 10, frac_bad: 0.1, N_bad: 30e-6 } }
      ],
      fields: [
        { id: 'f_query', label: 'A: Query frequency F_c (→ place x)', unit: 'Hz', type: 'number', default: 1000 },
        { id: 'x_query_mm', label: 'A: Query place x from base (→ F_c)', unit: 'mm', type: 'number', step: '0.5', default: 20.4 },
        { id: 'L_cochlea', label: 'A: Cochlea length L', unit: 'm', type: 'number', step: '0.001', default: 0.034 },
        { id: 'c_BM', label: 'B: Basilar membrane wave speed c_BM', unit: 'm/s', type: 'number', step: '0.5', default: 3 },
        { id: 't_rt_ms', label: 'B: OAE roundtrip latencies t_rt', unit: 'ms list', type: 'text', default: '12, 7, 5' },
        { id: 'EP', label: 'C: ABR evoked potential amplitude EP', unit: 'V', type: 'number', step: '1e-7', default: 0.3e-6 },
        { id: 'N1', label: 'C: Clean single-sweep noise RMS N₁', unit: 'V', type: 'number', step: '1e-6', default: 3e-6 },
        { id: 'rate', label: 'C: Stimulus presentation rate', unit: 'sweeps/s', type: 'number', default: 20 },
        { id: 'SNR_target_dB', label: 'C: Target SNR after averaging', unit: 'dB', type: 'number', default: 10 },
        { id: 'frac_bad', label: 'C: Fraction of artifact sweeps (10%=0.1)', unit: '0..1', type: 'number', step: '0.05', default: 0.1 },
        { id: 'N_bad', label: 'C: Artifact sweep noise RMS N_bad', unit: 'V', type: 'number', step: '1e-6', default: 30e-6 }
      ]
    },
    {
      id: 'T14_vibration_isolation',
      code: 'T14',
      title: 'Vibration Isolation: Static Deflection, Transmissibility & Mobility',
      shortTitle: 'Vibration Isolation',
      lecture: 'L11',
      matches: '2022 MC11 (T at 7 Hz ≈ 0 dB), 2023 MC9 (1.5 cm → 4.1 Hz), 2023 MC11 (F = j3.14 N), 2024 MC10 (isolation > 7.04 Hz), Week 11 P3–P4',
      keywords: 'vibration isolation springs mass static deflection resonance f0 sqrt2 transmissibility damping mobility blocked force rigid floor accelerometer',
      description: 'Computes natural frequency f₀ and isolation onset √2·f₀ from static deflection ξ₀ (or stiffness s and mass m), transmissibility T and isolation in dB, forced mass–spring displacement/velocity/floor-force, base-excitation stiffness design, and blocked force from mobility.',
      decisions: [
        { tag: 'Isolation > √2·f₀', text: 'Isolation ONLY starts at f = √2·f₀ (where T = 1 = 0 dB for any damping). Below √2·f₀, the mount AMPLIFIES vibration (T > 1)!' },
        { tag: 'Mass Distractor', text: 'When static deflection ξ₀ is given, f₀ = (1/2π)√(g/ξ₀) ≈ 0.5/√ξ₀ depends ONLY on ξ₀ (in metres!). The machine mass is a distractor.' },
        { tag: 'Damping Effect', text: 'Adding damping reduces the peak at resonance (f ≈ f₀) but makes isolation WORSE in the isolation region (f > √2·f₀).' }
      ],
      presets: [
        { name: 'All Pre-filled Exam & Sheet Checks (2022–2024 MCs, Week 11 P3–P4)', values: { m: 100, xi0: 0.01, f: 7, zeta: 0, xi0_B: 0.015, s_C: 23800, m_C: 1.5, F_C: 5, w_C: '37.8, 378', f_D: 25, m_D: 1.5, ratio_D: -0.1, v_free: 0.01, m_src: 0.1, f_E: 500 } }
      ],
      fields: [
        { id: 'm', label: 'A (2022 MC11 / 2024 MC10): Total mass m', unit: 'kg', type: 'number', default: 100 },
        { id: 'xi0', label: 'A: Static deflection ξ₀ (1 cm = 0.01 m)', unit: 'm', type: 'number', step: '0.001', default: 0.01 },
        { id: 'f', label: 'A: Excitation frequency f', unit: 'Hz', type: 'number', step: '0.5', default: 7 },
        { id: 'zeta', label: 'A: Damping ratio ζ (0 = undamped)', unit: 'ratio', type: 'number', step: '0.05', default: 0 },
        { id: 'xi0_B', label: 'B (2023 MC9): Static deflection ξ₀ (1.5cm=0.015)', unit: 'm', type: 'number', step: '0.001', default: 0.015 },
        { id: 's_C', label: 'C (Wk 11 P3): Total spring stiffness s', unit: 'N/m', type: 'number', default: 23800 },
        { id: 'm_C', label: 'C: Mass m', unit: 'kg', type: 'number', step: '0.1', default: 1.5 },
        { id: 'F_C', label: 'C: Driving force amplitude F', unit: 'N', type: 'number', default: 5 },
        { id: 'w_C', label: 'C: Angular frequencies ω (rad/s)', unit: 'rad/s list', type: 'text', default: '37.8, 378' },
        { id: 'f_D', label: 'D (Wk 11 P4): Base excitation freq f', unit: 'Hz', type: 'number', default: 25 },
        { id: 'm_D', label: 'D: Mass m', unit: 'kg', type: 'number', step: '0.1', default: 1.5 },
        { id: 'ratio_D', label: 'D: Target motion ratio u/u_f (negative!)', unit: 'ratio', type: 'number', step: '0.05', default: -0.1 },
        { id: 'v_free', label: 'E (2023 MC11): Source free velocity v_free', unit: 'm/s', type: 'number', step: '0.005', default: 0.01 },
        { id: 'm_src', label: 'E: Source mass m_src', unit: 'kg', type: 'number', step: '0.05', default: 0.1 },
        { id: 'f_E', label: 'E: Frequency f', unit: 'Hz', type: 'number', default: 500 }
      ]
    },
    {
      id: 'T15_sound_insulation',
      code: 'T15',
      title: 'Sound Insulation: Mass Law, Two Rooms, Composite, f_c & Double Wall',
      shortTitle: 'Sound Insulation',
      lecture: 'L12',
      matches: '2023 MC8 (L₂ = 37.9 dB), 2022 MC8 (window ≥ 40.5 dB), 2022 MC9 (stacked f_c = 3000 Hz), 2024 MC8 (Δf_c = -63 Hz), 2024 MC11 (double wall +32.1 dB), Sheet P3 (28.5 dB)',
      keywords: 'sound insulation transmission loss R mass law field incidence two rooms receiver room composite wall door window crack critical frequency coincidence double wall flanking impact sound',
      description: 'Solves mass law (normal/field/random incidence), receiver-room level L₂ between two rooms, composite wall transmission loss (wall + door/window/crack, forward and inverse for required window R), critical frequency f_c vs thickness/stacking, and double-wall gain.',
      decisions: [
        { tag: 'Combine via τ', text: 'NEVER average R in dB! Always weight transmission coefficients by area: τ_res = (Σ S_i 10^{-R_i/10}) / S_tot. When cutting a window of area S_win into a wall of total area S_tot, the remaining wall area is S_tot - S_win!' },
        { tag: 'Thickness vs Stacking', text: 'Bending stiffness B ∝ h³ while mass m ∝ h, so f_c ∝ √(m/B) ∝ 1/h (thicker wall → LOWER f_c!). But stacking two loose/unbonded plates multiplies both B and m by 2, leaving f_c UNCHANGED (2022 MC9).' },
        { tag: 'Double Wall (f > f_d)', text: 'Above f_d = c/(2πd), R_double = R₁ + R₂ + 6 dB (using field mass law R₀ - 5 dB for each board as instructed in 2024 MC11).' }
      ],
      presets: [
        { name: 'All Pre-filled Exam & Sheet Checks (2022–2024 MCs, Sheet P3)', values: { m_A: 230, f_A: 500, L1_B: 80, R_B: 40, S_B: 12, V2: 60, T2: 0.5, S_i: '18, 2', R_i: '44, 26', S_tot: 20, R_res_C2: 40, S_win: 1, R_wall: 45, S_tot_D: 25, R_target: 50, R_wall_D: 55, S_win_D: 2, E: 2.6e10, rho_M: 2300, nu: 0.2, h: '0.10, 0.15', m1: 15.6, m2: 15.6, d: 0.10, f_F: 600 } }
      ],
      fields: [
        { id: 'm_A', label: 'A (Mass Law): Surface mass m (ρ_M·h)', unit: 'kg/m²', type: 'number', default: 230 },
        { id: 'f_A', label: 'A: Frequency f', unit: 'Hz', type: 'number', default: 500 },
        { id: 'L1_B', label: 'B (2023 MC8 Two Rooms): Source room L₁', unit: 'dB', type: 'number', default: 80 },
        { id: 'R_B', label: 'B: Partition wall R', unit: 'dB', type: 'number', default: 40 },
        { id: 'S_B', label: 'B: Partition wall area S (4×3=12)', unit: 'm²', type: 'number', default: 12 },
        { id: 'V2', label: 'B: Receiver room volume V₂', unit: 'm³', type: 'number', default: 60 },
        { id: 'T2', label: 'B: Receiver room reverb time T₂', unit: 's', type: 'number', step: '0.1', default: 0.5 },
        { id: 'S_i', label: 'C (Composite): Element areas S_i', unit: 'm² list', type: 'text', default: '18, 2' },
        { id: 'R_i', label: 'C: Element transmission losses R_i', unit: 'dB list', type: 'text', default: '44, 26' },
        { id: 'S_tot_D', label: 'D (2022 MC8 Window): Total wall area S_tot', unit: 'm²', type: 'number', default: 25 },
        { id: 'R_target', label: 'D: Target total R_res', unit: 'dB', type: 'number', default: 50 },
        { id: 'R_wall_D', label: 'D: Wall construction R_wall alone', unit: 'dB', type: 'number', default: 55 },
        { id: 'S_win_D', label: 'D: Window area S_win', unit: 'm²', type: 'number', default: 2 },
        { id: 'E', label: 'E (2024 MC8 f_c): Young’s modulus E', unit: 'Pa', type: 'number', default: 2.6e10 },
        { id: 'rho_M', label: 'E: Material density ρ_M', unit: 'kg/m³', type: 'number', default: 2300 },
        { id: 'nu', label: 'E: Poisson’s ratio ν', unit: 'ratio', type: 'number', step: '0.05', default: 0.2 },
        { id: 'h', label: 'E: Wall thicknesses h (before, after)', unit: 'm list', type: 'text', default: '0.10, 0.15' },
        { id: 'm1', label: 'F (2024 MC11 Double Wall): Leaf 1 mass m₁', unit: 'kg/m²', type: 'number', step: '0.1', default: 15.6 },
        { id: 'm2', label: 'F: Leaf 2 mass m₂ (1200×0.013=15.6)', unit: 'kg/m²', type: 'number', step: '0.1', default: 15.6 },
        { id: 'd', label: 'F: Air gap distance d (10 cm = 0.10)', unit: 'm', type: 'number', step: '0.01', default: 0.10 },
        { id: 'f_F', label: 'F: Frequency f', unit: 'Hz', type: 'number', default: 600 }
      ]
    }
  ];
});
