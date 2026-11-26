// 34840 Exam App — All 45 Part-2 Multiple-Choice Questions (2022, 2023, 2024)
// Exact questions, options A-D, official answers, one-line reasons, traps, and solver links.

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.MC_DATA = factory();
  }
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  return [
    // ==================== 2022 (15 questions) ====================
    {
      id: '2022-Q1', year: 2022, qNum: 1, topic: 'Waves & Sources', solver: 'T01',
      question: 'Underwater construction work for offshore wind turbines generates noise. Consider a plane wave travelling in water towards an area where a large number of air bubbles are constantly being emitted from the bottom of the sea. What is the effect of the air bubbles on the plane wave?',
      options: {
        A: 'The plane wave is amplified',
        B: 'The air bubbles create a reflection in phase (R > 0)',
        C: 'The air bubbles create a reflection in antiphase (R < 0)',
        D: 'The air bubbles have no observable effect on the plane wave'
      },
      answer: 'C',
      reason: 'Air bubbles lower the characteristic impedance Z₂ far below water’s Z₁ (a soft / pressure-release boundary), so R = (Z₂ - Z₁)/(Z₂ + Z₁) < 0 (reflection in antiphase).',
      trap: 'Option B: thinking any impedance change reflects in phase.'
    },
    {
      id: '2022-Q2', year: 2022, qNum: 2, topic: 'Levels & Bands', solver: 'T03',
      question: 'Two tuning pitch forks from different manufacturers are tested. When played separately and measured over a 10 s period they each generate a stable pressure amplitude of 0.18 and 0.14 Pa respectively. However, they produce slightly different frequencies of 440.00 Hz and 440.10 Hz respectively. Find the rms pressure over a 10 s measurement period when played simultaneously.',
      options: {
        A: '0.141 Pa',
        B: '0.161 Pa',
        C: '0.181 Pa',
        D: '0.228 Pa'
      },
      answer: 'B',
      reason: 'Different frequencies (Δf = 0.10 Hz), and 10 s covers one full beat period 1/Δf = 10 s, so the cross term averages to zero: p_rms = √((0.18² + 0.14²)/2) = 0.1612 Pa.',
      trap: 'Option D (0.228 Pa) is √(0.18² + 0.14²) without dividing the peak amplitudes by √2!'
    },
    {
      id: '2022-Q3', year: 2022, qNum: 3, topic: 'Levels & Bands', solver: 'T03',
      question: 'A machine in a factory generates an rms pressure of 0.1 Pa when active. During a normal working day of 8 hours the machine is operated for 50% of the time, and is not used in the remaining 16 hours of the day. What is the equivalent sound pressure level over a 24 hour period?',
      options: {
        A: '58.4 dB re 20 µPa',
        B: '66.2 dB re 20 µPa',
        C: '71.0 dB re 20 µPa',
        D: '74.0 dB re 20 µPa'
      },
      answer: 'B',
      reason: '0.1 Pa rms = 74.0 dB while running. Active for 4 h out of 24 h: L_eq,24h = 74.0 + 10 log₁₀(4/24) = 74.0 - 7.78 = 66.2 dB.',
      trap: 'Option D (74.0 dB) is the running level; Option C (71.0 dB) takes 50% of 8 h (-3 dB) but forgets the remaining 16 h of the 24 h day.'
    },
    {
      id: '2022-Q4', year: 2022, qNum: 4, topic: 'Rooms & Modes', solver: 'T09',
      question: 'What is the height (z-dimension) of a rectangular room having natural frequencies of f(0,1,0) = 10 Hz and f(0,2,1) = 45 Hz? The index order is (nx, ny, nz).',
      options: {
        A: '3 m',
        B: '4 m',
        C: '5 m',
        D: '6 m'
      },
      answer: 'B',
      reason: 'f(0,1,0) = 10 Hz → l_y = c/(2·10) = 17.15 m. Then 45 = (c/2)√((2/l_y)² + (1/l_z)²) → l_z = 4.25 m → nearest option is 4 m.',
      trap: 'Official solution has a typo 2/l_y² instead of (2/l_y)² and gets 4.01 m; either way Option B (4 m) is correct.'
    },
    {
      id: '2022-Q5', year: 2022, qNum: 5, topic: 'Rooms & Modes', solver: 'T10',
      question: 'When all the sound absorbers are treated on the ceiling of a room with dimensions lx = 10 m, ly = 13 m, lz = 8 m, what is the reverberation time? Assume α = 0.8 for the ceiling and 0.0 for all other surfaces.',
      options: {
        A: '0.5 s',
        B: '1.0 s',
        C: '1.6 s',
        D: '2.2 s'
      },
      answer: 'C',
      reason: 'V = 1040 m³, A = S_ceiling · 0.8 = 130 · 0.8 = 104 m² (or T = 0.16·l_z/α). Sabine: T = 55.3·1040/(343·104) = 1.61 s (Eyring gives 1.47 s, still nearest 1.6 s).',
      trap: 'Including floor or walls in the absorbing area when α = 0 for all other surfaces.'
    },
    {
      id: '2022-Q6', year: 2022, qNum: 6, topic: 'Absorbers', solver: 'T11',
      question: 'Which surface impedance makes the absorption coefficient smallest assuming that the sound is incident from the normal direction to the surface of interest?',
      options: {
        A: 'Z = 1 N·s·m⁻³',
        B: 'Z = 100 N·s·m⁻³',
        C: 'Z = 1000 N·s·m⁻³',
        D: 'Z = 10000 N·s·m⁻³'
      },
      answer: 'A',
      reason: 'α = 1 - |(Z - ρc)/(Z + ρc)|² with ρc = 411.6: gives α = 0.0097, 0.63, 0.83, 0.15 for Z = 1, 100, 1000, 10000. Z = 1 is a factor 412 away from ρc (vs factor 24 for Z = 10000), so it reflects most.',
      trap: 'Thinking "small Z = soft = absorbing". Both Z ≪ ρc and Z ≫ ρc reflect; only Z ≈ ρc absorbs!'
    },
    {
      id: '2022-Q7', year: 2022, qNum: 7, topic: 'Rooms & Modes', solver: 'T10',
      question: 'In a reverberation chamber with volume 150 m³, the sound absorption coefficient is measured according to ISO 354. T₂₀ for the empty chamber is 5 s, while T₂₀ with a 9 m² specimen is 2 s. The thickness of the absorber is 1 cm. What is the absorption coefficient of the specimen?',
      options: {
        A: '0.5',
        B: '0.6',
        C: '0.7',
        D: '0.8'
      },
      answer: 'D',
      reason: 'ISO 354: α = (0.16·V/S)·(1/T₂ - 1/T₁) = (0.16·150/9)·(1/2 - 1/5) = (24/9)·0.3 = 0.80.',
      trap: 'The 1 cm absorber thickness is a pure distractor.'
    },
    {
      id: '2022-Q8', year: 2022, qNum: 8, topic: 'Sound Insulation', solver: 'T15',
      question: 'A wall of 25 m² (total area) should have a total sound transmission loss of R = 50 dB in one 1/3-octave band. The wall construction by itself has R = 55 dB. There should also be a window of 2 m² in the wall. What is the minimum sound transmission loss needed for the window?',
      options: {
        A: '30.5 dB',
        B: '50.0 dB',
        C: '45.5 dB',
        D: '40.5 dB'
      },
      answer: 'D',
      reason: 'Remaining wall area is 25 - 2 = 23 m². Solve S_tot·10^{-50/10} = 23·10^{-55/10} + 2·10^{-R_win/10} → R_win = -10 log₁₀((25·10⁻⁵ - 23·10⁻⁵·⁵)/2) = 40.52 dB.',
      trap: 'Option B (50 dB): forgetting that the window is only 8% of the area, or forgetting to subtract 2 m² from 25 m² for the wall part.'
    },
    {
      id: '2022-Q9', year: 2022, qNum: 9, topic: 'Sound Insulation', solver: 'T15',
      question: 'A thin plate has a critical frequency of f_c = 3000 Hz. Adding two such plates together by stacking them on top of each other, the new critical frequency of the combined plate will be:',
      options: {
        A: '2200 Hz',
        B: '1500 Hz',
        C: '3000 Hz',
        D: '800 Hz'
      },
      answer: 'C',
      reason: 'Two loose stacked plates bend independently: bending stiffness doubles (B → 2B) and surface mass doubles (m → 2m), so f_c = (c²/2π)√(2m/2B) = 3000 Hz is unchanged.',
      trap: 'Option B (1500 Hz) is for one bonded/glued plate of double thickness (where B → 8B and m → 2m, halving f_c).'
    },
    {
      id: '2022-Q10', year: 2022, qNum: 10, topic: 'Vibration', solver: 'T14',
      question: 'Consider a simple mechanical oscillator. For frequencies below the resonance frequency, such a system is said to be:',
      options: {
        A: 'Mass controlled',
        B: 'Stiffness controlled',
        C: 'Damping controlled',
        D: 'Vibration controlled'
      },
      answer: 'B',
      reason: 'In x = F/(s - ω²m + jωr), below resonance (ω ≪ ω₀) the spring stiffness term s dominates (x ≈ F/s). Above ω₀ it is mass controlled; at ω₀ it is damping controlled.',
      trap: 'Option A swaps stiffness-controlled (below f₀) and mass-controlled (above f₀).'
    },
    {
      id: '2022-Q11', year: 2022, qNum: 11, topic: 'Vibration', solver: 'T14',
      question: 'A machine (50 kg) is placed on a concrete slab (50 kg) on four springs; a static deflection of 1 cm is observed. Assume undamped conditions. What is the vibration isolation in dB (20 log T = -10 log E_iso) at 7 Hz?',
      options: {
        A: '0 dB',
        B: '10 dB',
        C: '6 dB',
        D: '3 dB'
      },
      answer: 'A',
      reason: 'From ξ₀ = 0.01 m, f₀ = (1/2π)√(g/0.01) = 4.985 Hz ≈ 5 Hz. At f = 7 Hz ≈ √2·f₀ = 7.05 Hz, transmissibility is T = 1/|1 - (7/5)²| ≈ 1 → 20 log₁₀(T) ≈ 0 dB (isolation only begins at √2·f₀).',
      trap: 'Thinking any frequency above f₀ = 5 Hz gives isolation. The 50 kg + 50 kg masses are distractors once ξ₀ = 1 cm is known.'
    },
    {
      id: '2022-Q12', year: 2022, qNum: 12, topic: 'Hearing', solver: 'T13',
      question: 'How are acoustic signals mapped in the cochlea?',
      options: {
        A: 'The high frequencies are mapped to locations at the base of the cochlea.',
        B: 'The low frequencies are mapped to locations at the base of the cochlea.',
        C: 'The envelope of an acoustic signal is mapped by the broad auditory filters towards the base of the cochlea.',
        D: 'The fine structure of an acoustic signal is detected by the narrow auditory filters towards the base of the cochlea.'
      },
      answer: 'A',
      reason: 'The basilar membrane is narrow and stiff at the base (resonating to high frequencies ~20 kHz) and wide and flexible at the apex (low frequencies ~20 Hz).',
      trap: 'Option B reverses base and apex.'
    },
    {
      id: '2022-Q13', year: 2022, qNum: 13, topic: 'Hearing', solver: 'T12',
      question: 'What mechanism in the auditory system causes the broadening of frequency selectivity for people with a sensorineural hearing loss?',
      options: {
        A: 'The auditory filters towards the base are damaged, causing reliance on broader apex filters.',
        B: 'The passive stiffness gradient of the basilar membrane is lacking across the entire membrane.',
        C: 'Sensorineural hearing loss is characterized by damage to the outer hair cells which provide frequency-specific amplification and compression.',
        D: 'Auditory nerve fibers are damaged, causing reliance on nerve fibers across a larger area.'
      },
      answer: 'C',
      reason: 'Outer hair cells (OHCs) act as the active, frequency-selective cochlear amplifier; when damaged in SNHL, sharp active tuning is lost and only broad passive basilar-membrane tuning remains.',
      trap: 'Option B: the passive stiffness gradient is structural and unchanged.'
    },
    {
      id: '2022-Q14', year: 2022, qNum: 14, topic: 'Hearing', solver: 'T12',
      question: 'Two pure tones with frequencies 900 Hz and 850 Hz each at 50 dB SPL are presented simultaneously to a normal-hearing listener. Which statement is true (assuming rectangular auditory filters)?',
      options: {
        A: 'The two tones fall within a single auditory filter and are perceived as a single tone that fluctuates at a rate of 50 Hz.',
        B: 'The two tones fall within separate auditory filters and are perceived as two separate tones.',
        C: 'The non-linearities of the middle ear produce non-linear distortions.',
        D: 'A combination tone of 950 Hz is produced with an approximate level of 25 dB.'
      },
      answer: 'A',
      reason: 'At f_mid = 875 Hz, ERB = 24.7(4.37·0.875 + 1) = 119 Hz > Δf = 50 Hz, so both tones fall in the same auditory filter and beat at f₂ - f₁ = 50 Hz.',
      trap: 'Option D: the cubic difference tone is at 2f₁ - f₂ = 2(850) - 900 = 800 Hz (below f₁), NOT 950 Hz!'
    },
    {
      id: '2022-Q15', year: 2022, qNum: 15, topic: 'Hearing', solver: 'T12',
      question: 'To characterize the shape of the auditory filters, spectral masking experiments are used. Which of the following statements regarding such considerations is true?',
      options: {
        A: 'When using lowpass-noise as a masker, the measured shape of the auditory filter does not depend on the level of the masker.',
        B: 'The estimated bandwidth of the auditory filter does not depend on the target tone’s frequency.',
        C: 'The masking curves obtained from the experiment directly give the shape of the auditory filter, and no further transformation is required.',
        D: 'Notched-noise is often preferred as a masker to avoid the detection of the target tone being made through a neighboring auditory filter, where the SNR is higher.'
      },
      answer: 'D',
      reason: 'Notched noise places a symmetric spectral notch around the signal frequency so neighbouring filters do not get a better SNR, preventing "off-frequency listening".',
      trap: 'A, B, C are all false (filter shape broadens with level; ERB grows with frequency; masking data requires derivative/fitting).'
    },

    // ==================== 2023 (15 questions) ====================
    {
      id: '2023-Q1', year: 2023, qNum: 1, topic: 'Levels & Bands', solver: 'T03',
      question: 'Two uncorrelated noise sources each produce 10 dB SPL when driven separately. Which sentence describes what happens when the two sources are active at the same time?',
      options: {
        A: 'The squared rms pressures are added, total SPL is 13 dB',
        B: 'As the sources are uncorrelated, the sound pressure stays the same, total SPL is 10 dB',
        C: 'The rms pressures are added, total SPL is 16 dB',
        D: 'For uncorrelated sources the SPL values are added, total SPL is 20 dB'
      },
      answer: 'A',
      reason: 'Uncorrelated sources add by energy (squared rms pressures p²_rms), doubling energy → 10 + 10 log₁₀(2) = 13.0 dB.',
      trap: 'Option C (+6 dB = 16 dB) is for coherent in-phase tones of the same frequency.'
    },
    {
      id: '2023-Q2', year: 2023, qNum: 2, topic: 'Waves & Sources', solver: 'T06',
      question: 'What is the correct description of the sound field very close to a monopole?',
      options: {
        A: 'The sound field is similar to a plane wave',
        B: 'The sound pressure is attenuated with distance as 1/r, but the particle velocity decays slower',
        C: 'The pressure and particle velocity are in anti-phase (180 degrees)',
        D: 'The sound pressure is attenuated with distance as 1/r, but the particle velocity decays faster'
      },
      answer: 'D',
      reason: 'For a monopole, P ∝ 1/r everywhere, while U_r = (P/ρc)(1 + 1/(jkr)) has an extra 1/r² near-field term (kr ≪ 1), so |u| decays faster than 1/r as you move away from the source.',
      trap: 'Option A is the far field (kr ≫ 1); Option C says 180° (in the near field p leads u by 90°, not 180°).'
    },
    {
      id: '2023-Q3', year: 2023, qNum: 3, topic: 'Rooms & Modes', solver: 'T09',
      question: 'Consider a room with dimensions 7.2 m (x) × 5.4 m (y) × 3.0 m (z). When placing the source in one corner and microphone in the opposite corner, the SPL in the 1/3-octave band centered at 50 Hz is 5 dB higher than neighboring bands. Which room mode (nx, ny, nz) is responsible?',
      options: {
        A: '(1,0,0)',
        B: '(0,1,0)',
        C: '(1,1,0)',
        D: '(2,0,0)'
      },
      answer: 'D',
      reason: 'The 50 Hz 1/3-octave band spans 44.5–56.1 Hz. Mode frequencies: f(1,0,0) = 23.8 Hz, f(0,1,0) = 31.8 Hz, f(1,1,0) = 39.7 Hz, f(2,0,0) = 47.6 Hz. Only (2,0,0) lies inside the 50 Hz band.',
      trap: 'Picking (1,0,0) without calculating the actual frequency.'
    },
    {
      id: '2023-Q4', year: 2023, qNum: 4, topic: 'Waves & Sources', solver: 'T07',
      question: 'What characterizes a dipole?',
      options: {
        A: 'The dipole is a very effective source as it has two internal sources that increase radiation efficiency.',
        B: 'A dipole is a mathematical model for directive sources, but has limited use in practice.',
        C: 'A dipole is a very inefficient source as it has two internal sources that cancel out especially at the higher frequencies.',
        D: 'A dipole is a very inefficient source as it has two internal sources that cancel out especially at the lower frequencies.'
      },
      answer: 'D',
      reason: 'A dipole consists of two antiphase monopoles separated by 2h. At low frequencies (2kh ≪ 1), the two halves cancel almost completely and radiated power scales as W ∝ k⁴ ∝ f⁴.',
      trap: 'Option C says higher frequencies instead of lower frequencies.'
    },
    {
      id: '2023-Q5', year: 2023, qNum: 5, topic: 'Rooms & Modes', solver: 'T10',
      question: 'Assume a rectangular room of [6 × 7 × 3] m. The absorption coefficient of the ceiling is 0.8 at 4 kHz. The walls and floor have the same material with unknown α, and T = 0.44 s at 4 kHz. What is the absorption coefficient of the floor and walls?',
      options: {
        A: '0.1',
        B: '0.3',
        C: '0.5',
        D: '0.7'
      },
      answer: 'A',
      reason: 'V = 126 m³, A = 0.16·126/0.44 = 45.8 m². Ceiling area = 42 m² → A_ceil = 42·0.8 = 33.6 m². Remaining A_rest = 12.2 m² over S_floor+walls = 42 + 2(6+7)·3 = 120 m² → α = 12.2/120 = 0.10.',
      trap: 'Dividing by total surface area 162 m² instead of 120 m², or forgetting to subtract the ceiling.'
    },
    {
      id: '2023-Q6', year: 2023, qNum: 6, topic: 'Absorbers', solver: 'T11',
      question: 'Assume a membrane absorber with a membrane having a mass per unit area of 2.1 kg/m² and cavity depth 0.1 m. At which frequency does this membrane absorber resonate?',
      options: {
        A: '100 Hz',
        B: '110 Hz',
        C: '120 Hz',
        D: '130 Hz'
      },
      answer: 'D',
      reason: 'f_r = (1/2π)√(ρc²/(m·L)) = (1/2π)√(1.412×10⁵/(2.1·0.1)) = 130.5 Hz ≈ 130 Hz (or 60/√(2.1·0.1) = 131 Hz).',
      trap: 'Forgetting the square root or using ρc instead of ρc².'
    },
    {
      id: '2023-Q7', year: 2023, qNum: 7, topic: 'Rooms & Modes', solver: 'T10',
      question: 'In a room with volume 200 m³, a sound source is at (1, 1, 1.7) m with L_W = 75 dB. The receiver is at (3, 8, 1.2) m where T = 1 s. What is the SPL at the receiver assuming directivity factor Q = 1?',
      options: {
        A: '56 dB SPL',
        B: '66 dB SPL',
        C: '76 dB SPL',
        D: '86 dB SPL'
      },
      answer: 'B',
      reason: 'A = 0.16·200/1 = 32 m², r = √(2² + 7² + (-0.5)²) = 7.30 m. L_p = 75 + 10 log₁₀(1/(4π·7.3²) + 4/32) = 75 - 9.0 = 66.0 dB.',
      trap: 'Option A (56 dB) comes from forgetting the factor 4 in 4/A (or 10 log(1/A) = -15 dB).'
    },
    {
      id: '2023-Q8', year: 2023, qNum: 8, topic: 'Sound Insulation', solver: 'T15',
      question: 'A noise source in a room produces L₁ = 80 dB in the 1 kHz 1/3-octave band. A wall of size 4 m × 3 m with R = 40 dB connects to a receiver room with T = 0.5 s and V = 60 m³. What is the SPL in the receiver room?',
      options: {
        A: '20.4 dB SPL',
        B: '32.7 dB SPL',
        C: '45.8 dB SPL',
        D: '37.9 dB SPL'
      },
      answer: 'D',
      reason: 'S = 12 m², A₂ = 55.3·60/(343·0.5) = 19.35 m². L₂ = L₁ - R + 10 log₁₀(S/A₂) = 80 - 40 + 10 log₁₀(12/19.35) = 40 - 2.07 = 37.9 dB.',
      trap: 'Flipping S/A₂ to A₂/S (+2.07 → 42.1 dB) or using V₂ instead of A₂.'
    },
    {
      id: '2023-Q9', year: 2023, qNum: 9, topic: 'Vibration', solver: 'T14',
      question: 'A machine is to be vibration isolated using four simple springs. Total mass is 80 kg. When mounted on the springs, there is a static deflection of 1.5 cm. What is the resonance frequency?',
      options: {
        A: '4.1 Hz',
        B: '5.7 Hz',
        C: '2.3 Hz',
        D: '10.2 Hz'
      },
      answer: 'A',
      reason: 'f₀ = (1/2π)√(g/ξ₀) = (1/2π)√(9.81/0.015) = 4.07 Hz ≈ 4.1 Hz (or 0.5/√0.015 = 4.08 Hz). The 80 kg mass and number of springs (4) are distractors!',
      trap: 'Dividing or multiplying by 4 springs when total static deflection ξ₀ = 1.5 cm is already given.'
    },
    {
      id: '2023-Q10', year: 2023, qNum: 10, topic: 'Sound Insulation', solver: 'T15',
      question: 'Which statement for sound transmission loss of a finite-sized wall is correct? In a diffuse sound field the sound transmission loss is approximately:',
      options: {
        A: 'equal to that of normal incidence',
        B: '5 dB higher than that of normal incidence',
        C: '5 dB lower than that of normal incidence',
        D: '15 dB lower than that of normal incidence'
      },
      answer: 'C',
      reason: 'Field-incidence mass law for real walls (limiting angle ~78°): R_field ≈ R₀ - 5 dB (course text eq. 5.2.18).',
      trap: 'Option B (+5 dB is the wrong direction) or Option D (15 dB is too large).'
    },
    {
      id: '2023-Q11', year: 2023, qNum: 11, topic: 'Vibration', solver: 'T14',
      question: 'A vibration source has a free velocity of 0.01 m/s (amplitude) and weighs 0.1 kg. Assuming its source mobility is that of its mass, what is the complex-valued force at 500 Hz if connected to a rigid surface?',
      options: {
        A: 'F = -i N',
        B: 'F = i 3.14 N',
        C: 'F = i 6.28 N',
        D: 'F = 4.34 N'
      },
      answer: 'B',
      reason: 'Rigid receiver Y_R = 0, mass mobility Y_S = 1/(jωm) → F = v_free / Y_S = jωm·v_free = j·(2π·500)·0.1·0.01 = j·π = i 3.14 N.',
      trap: 'Option C is 2π (off by factor 2); Option D drops the imaginary unit i.'
    },
    {
      id: '2023-Q12', year: 2023, qNum: 12, topic: 'Hearing', solver: 'T13',
      question: 'How can the basilar membrane be characterized?',
      options: {
        A: 'Its role is to segregate frequencies and can be conceptualized as a Fourier transformation.',
        B: 'It can be modelled as a series of cascading lowpass filters, with the lowest cutoff frequency at the apex and the highest cutoff frequency at the base.',
        C: 'Its motion pattern can be described using the wave equation with a constant impedance along the membrane.',
        D: 'It is a level-dependent system where soft sounds resonate near the apex and loud sounds by the base.'
      },
      answer: 'B',
      reason: 'A travelling wave enters at the base (high cutoff) and propagates towards the apex (low cutoff), peaking at its characteristic place and dying out beyond it—acting like a cascade of lowpass filters.',
      trap: 'Option A: the cochlea is non-linear and time-domain, not a linear Fourier transform.'
    },
    {
      id: '2023-Q13', year: 2023, qNum: 13, topic: 'Hearing', solver: 'T12',
      question: 'Which of the following statements about a sensorineural hearing impairment is correct?',
      options: {
        A: 'It is caused by a blockage of the ear canal and leads to an overall sensitivity reduction of all sounds.',
        B: 'It selectively decreases the sensitivity to high-frequency sounds.',
        C: 'It leads to a decrease in sensitivity and reduces the amount of amplitude compression in the cochlea.',
        D: 'It leads to sharper frequency sensitivity.'
      },
      answer: 'C',
      reason: 'OHC damage removes active gain for soft sounds (raising threshold / decreasing sensitivity) and linearises the response (reducing cochlear compression, causing loudness recruitment).',
      trap: 'Option A describes conductive hearing loss; Option D is the opposite of broader filters.'
    },
    {
      id: '2023-Q14', year: 2023, qNum: 14, topic: 'Hearing', solver: 'T12',
      question: 'Two pure tones with frequencies of 400 Hz and 600 Hz, both at 50 dB SPL, are simultaneously presented to a normal-hearing listener. Which statement is correct (assuming rectangular filters)?',
      options: {
        A: 'The two tones fall within a single auditory filter and are perceived as a single tone that fluctuates at 200 Hz.',
        B: 'The two tones fall within separate auditory filters and are perceived as two separate tones.',
        C: 'A combination tone of 800 Hz is produced with an approximate SPL of 25 dB.',
        D: 'The upward spread of masking caused by the 400 Hz tone makes the 600 Hz tone almost inaudible.'
      },
      answer: 'B',
      reason: 'At f_mid = 500 Hz, ERB = 24.7(4.37·0.5 + 1) = 78.7 Hz ≪ Δf = 200 Hz, so the two tones resolve into separate auditory filters and are heard as two distinct tones.',
      trap: 'Option C: the cubic difference tone is 2f₁ - f₂ = 2(400) - 600 = 200 Hz, NOT 800 Hz!'
    },
    {
      id: '2023-Q15', year: 2023, qNum: 15, topic: 'Hearing', solver: 'T12',
      question: 'Which statement regarding the hair cells in the cochlea is correct?',
      options: {
        A: 'The outer hair cells provide level-dependent amplification and are more sensitive to soft sound levels relative to loud sound levels.',
        B: 'The outer hair cells provide frequency-dependent amplification and are more sensitive to low frequencies relative to high frequencies.',
        C: 'The outer hair cells are positioned outside of the cochlea and provide compression to attenuate loud sounds before they reach the inner ear.',
        D: 'The density of the outer hair cells varies across the basilar membrane, causing auditory filters to be sharper for lower frequencies.'
      },
      answer: 'A',
      reason: 'Outer hair cells (OHCs) are the active cochlear amplifier: they provide high gain at low sound levels and little/no gain at high levels (compressive non-linearity).',
      trap: 'Option C: OHCs are inside the organ of Corti in the cochlea (not outside, and that describes the stapedius reflex).'
    },

    // ==================== 2024 (15 questions) ====================
    {
      id: '2024-Q1', year: 2024, qNum: 1, topic: 'Waves & Sources', solver: 'T06',
      question: 'A monopole is driven at f = 189 Hz. What is the absolute value of the phase difference between pressure and particle velocity at a distance of 50 cm?',
      options: {
        A: '0 degrees',
        B: '30 degrees',
        C: '60 degrees',
        D: '90 degrees'
      },
      answer: 'B',
      reason: 'kr = (2π·189/343)·0.5 = 1.731 ≈ √3. Since U_r = (P/ρc)(1 + 1/(jkr)), p leads u by φ = arctan(1/kr) = arctan(1/√3) = 30°.',
      trap: 'Option C (60°) is arctan(kr) instead of arctan(1/kr)!'
    },
    {
      id: '2024-Q2', year: 2024, qNum: 2, topic: 'Levels & Bands', solver: 'T03',
      question: 'A noisy machine is operated for 15 minutes every hour during the working day. During operation it generates an rms pressure of 0.05 Pa. What is the equivalent SPL, L_eq, over an 8 hour work period?',
      options: {
        A: '56 dB re 20 µPa',
        B: '62 dB re 20 µPa',
        C: '65 dB re 20 µPa',
        D: '68 dB re 20 µPa'
      },
      answer: 'B',
      reason: 'While running, 0.05 Pa rms = 20 log₁₀(0.05/20×10⁻⁶) = 68.0 dB. Duty cycle is 15/60 = 1/4 (-6.02 dB), so L_eq = 68.0 - 6.0 = 62.0 dB.',
      trap: 'Option D (68 dB) is the level while running; Option C (65 dB) is -3 dB.'
    },
    {
      id: '2024-Q3', year: 2024, qNum: 3, topic: 'Waves & Sources', solver: 'T01',
      question: 'On Venus: Static pressure = 9,000,000 Pa, Temperature = 700 K, Density = 0.1 g/cm³, Speed of sound = 500 m/s. To design an ideal absorber on Venus (normal incidence), what should the specific impedance of the material be?',
      options: {
        A: '70 kg/(s·m²)',
        B: '35000 kg/(s·m²)',
        C: '50000 kg/(s·m²)',
        D: '9000000 kg/(s·m²)'
      },
      answer: 'C',
      reason: 'Ideal normal-incidence absorber matches the characteristic impedance Z = ρc. Convert density: 0.1 g/cm³ = 100 kg/m³. Then Z = 100 · 500 = 50,000 kg/(s·m²).',
      trap: 'Forgetting to convert 0.1 g/cm³ → 100 kg/m³, or using the distractor static pressure / temperature.'
    },
    {
      id: '2024-Q4', year: 2024, qNum: 4, topic: 'Rooms & Modes', solver: 'T10',
      question: 'A recording studio has dimensions 5 m × 8 m × 3 m (height 3 m). The walls and ceiling are treated with absorptive materials, while the floor is untreated (α = 0.1). Desired reverberation time at 500 Hz is 0.4 s. What absorption coefficient is required for the wall and ceiling materials?',
      options: {
        A: '0.2',
        B: '0.4',
        C: '0.6',
        D: '0.8'
      },
      answer: 'B',
      reason: 'V = 120 m³, required A = 0.16·120/0.4 = 48 m². Floor area = 40 m² (A_floor = 40·0.1 = 4 m²). Walls + ceiling area = 40 + 2(5+8)·3 = 118 m². Required α = (48 - 4)/118 = 0.373 → 0.4.',
      trap: 'Dividing by total room surface area 158 m² instead of 118 m².'
    },
    {
      id: '2024-Q5', year: 2024, qNum: 5, topic: 'Rooms & Modes', solver: 'T09',
      question: 'An office with dimensions 6 m (x) × 9 m (y) × 3 m (z) has a strong room mode at 57 Hz. Which room mode (nx, ny, nz) is most likely responsible? (c = 343 m/s)',
      options: {
        A: '(1,0,0)',
        B: '(0,1,0)',
        C: '(1,1,0)',
        D: '(2,0,0)'
      },
      answer: 'D',
      reason: 'f(2,0,0) = (343/2)·(2/6) = 57.2 Hz. The other options give f(1,0,0) = 28.6 Hz, f(0,1,0) = 19.1 Hz, f(1,1,0) = 34.4 Hz.',
      trap: 'Mixing up which dimension is x, y, z.'
    },
    {
      id: '2024-Q6', year: 2024, qNum: 6, topic: 'Absorbers', solver: 'T11',
      question: 'A Helmholtz resonator is designed to absorb sound at 140 Hz. The neck has a diameter of 5 cm and a length of 2 cm. Calculate the required cavity volume (in m³), neglecting end correction.',
      options: {
        A: '0.001 m³',
        B: '0.005 m³',
        C: '0.01 m³',
        D: '0.015 m³'
      },
      answer: 'D',
      reason: 's = π(0.05)²/4 = 1.963×10⁻³ m². From f₀ = (c/2π)√(s/(V·l)), V = (s/l)·(c/(2πf₀))² = (1.963×10⁻³/0.02)·(343/(2π·140))² = 0.0149 m³ ≈ 0.015 m³.',
      trap: 'Using diameter d = 0.05 m as radius in πr² (which makes V four times too large).'
    },
    {
      id: '2024-Q7', year: 2024, qNum: 7, topic: 'Absorbers', solver: 'T11',
      question: 'A membrane absorber is designed to have a resonance frequency of 350 Hz. The membrane has a surface mass density of 0.2 kg/m². What is the required depth of the air cavity behind the membrane?',
      options: {
        A: '2.5 cm',
        B: '5 cm',
        C: '10 cm',
        D: '15 cm'
      },
      answer: 'D',
      reason: 'From f_r = (1/2π)√(ρc²/(m·L)), L = ρc²/(m·(2πf_r)²) = 1.412×10⁵ / (0.2 · (2π·350)²) = 0.146 m ≈ 15 cm.',
      trap: 'Unit error or forgetting the 2π factor.'
    },
    {
      id: '2024-Q8', year: 2024, qNum: 8, topic: 'Sound Insulation', solver: 'T15',
      question: 'The thickness of a concrete wall is changed from 10 cm to 15 cm. How much is the critical frequency changed? (Concrete: E = 2.6×10¹⁰ N/m², ρ_M = 2.3×10³ kg/m³, ν = 0.2, η = 0.02)',
      options: {
        A: '0 Hz',
        B: '+51 Hz',
        C: '-63 Hz',
        D: '-25 Hz'
      },
      answer: 'C',
      reason: 'B = Eh³/(12(1-ν²)), m = ρ_M h, f_c = (c²/2π)√(m/B) ∝ 1/h. At h = 0.10 m, f_c = 189.0 Hz; at h = 0.15 m, f_c = 126.0 Hz → Δf_c = 126.0 - 189.0 = -63.0 Hz.',
      trap: 'Thinking thicker walls have a higher critical frequency (+51 Hz). Thicker = stiffer in bending → lower f_c.'
    },
    {
      id: '2024-Q9', year: 2024, qNum: 9, topic: 'Vibration', solver: 'T14',
      question: 'Fill in the blank: A piezo-electric accelerometer gives a … signal proportional to the vibration acceleration.',
      options: {
        A: 'voltage',
        B: 'charge',
        C: 'impedance',
        D: 'current'
      },
      answer: 'B',
      reason: 'The piezoelectric crystal generates an electric charge q proportional to the inertial force F = ma on the seismic mass; a charge amplifier then converts that charge to a voltage.',
      trap: 'Option A (voltage is the output of the conditioning charge amplifier, not the piezo element itself).'
    },
    {
      id: '2024-Q10', year: 2024, qNum: 10, topic: 'Vibration', solver: 'T14',
      question: 'A machine (total mass 100 kg) is mounted on vibration isolation springs that deflect 1 cm when statically loaded. What is the lowest frequency from which we have vibration isolation?',
      options: {
        A: '10.1 Hz',
        B: '4.2 Hz',
        C: '7.0 Hz',
        D: '15.4 Hz'
      },
      answer: 'C',
      reason: 'f₀ = (1/2π)√(g/ξ₀) = (1/2π)√(9.81/0.01) = 4.985 Hz. Vibration isolation (T < 1) starts at f = √2·f₀ = 1.414 · 4.985 = 7.05 Hz ≈ 7.0 Hz.',
      trap: 'Option B (4.2 Hz) is close to f₀ itself, where the mount amplifies rather than isolates.'
    },
    {
      id: '2024-Q11', year: 2024, qNum: 11, topic: 'Sound Insulation', solver: 'T15',
      question: 'We have two gypsum boards (13 mm thick, density 1.2×10³ kg/m³). Assume the field mass law applies for each board, and we are above f_d = c/(2πd) when separating them by d = 10 cm. At 600 Hz, how much better in dB is the sound insulation when separated by 10 cm compared to mounted close together?',
      options: {
        A: '5 dB',
        B: '21.1 dB',
        C: '32.1 dB',
        D: '38.1 dB'
      },
      answer: 'C',
      reason: 'm₁ = 1200·0.013 = 15.6 kg/m². At 600 Hz (> f_d = 546 Hz), R₁ = 20 log₁₀(ωm₁/(2ρc)) - 5 = 32.08 dB. Separated: R_double = 2R₁ + 6 = 70.16 dB. Together (one leaf of 31.2 kg/m²): R_together = 32.08 + 6.02 = 38.10 dB. Improvement = 70.16 - 38.10 = 32.1 dB.',
      trap: 'Option D (38.1 dB) is R_together itself!'
    },
    {
      id: '2024-Q12', year: 2024, qNum: 12, topic: 'Hearing', solver: 'T12',
      question: 'Which one of the following statements is true regarding the masking effects of a pure tone?',
      options: {
        A: 'The tone will mask higher frequencies more than lower frequencies',
        B: 'The tone will mask lower frequencies more than higher frequencies',
        C: 'The tone will mask lower and higher frequencies equally',
        D: 'The masking of higher frequencies provided by the tone is independent of the tone’s level'
      },
      answer: 'A',
      reason: 'Upward spread of masking: the basilar membrane excitation pattern has a shallow tail towards the base (higher frequencies), and auditory filters broaden on their low-frequency side at high levels.',
      trap: 'Option B reverses the upward spread of masking.'
    },
    {
      id: '2024-Q13', year: 2024, qNum: 13, topic: 'Hearing', solver: 'T12',
      question: 'Sensorineural hearing impairment results in a condition called loudness recruitment. Which statement is true?',
      options: {
        A: 'Loudness recruitment refers to a rate of growth of loudness (as a function of level) that is smaller than normal',
        B: 'Loudness recruitment refers to a rate of growth of loudness (as a function of level) that is greater than normal',
        C: 'Loudness recruitment is primarily caused by a loss of inner hair cells',
        D: 'Loudness recruitment can only be seen at high stimulus levels'
      },
      answer: 'B',
      reason: 'Loss of OHC amplification elevates the threshold for soft sounds while loud sounds (passive regime) stay near normal loudness, so loudness grows faster than normal with increasing level.',
      trap: 'Option A says smaller than normal; Option C attributes it to IHCs instead of OHCs.'
    },
    {
      id: '2024-Q14', year: 2024, qNum: 14, topic: 'Hearing', solver: 'T12',
      question: 'Which of the following statements about the change in frequency selectivity with increasing sound level is correct?',
      options: {
        A: 'Frequency selectivity improves, meaning auditory filters become more sharply tuned at higher SPLs',
        B: 'A change in sound level does not affect frequency selectivity as tuning is a fixed property',
        C: 'Frequency selectivity decreases, meaning the basilar membrane’s tuning becomes broader at higher sound pressure levels',
        D: 'Frequency selectivity improves at higher frequencies but remains constant towards lower frequencies'
      },
      answer: 'C',
      reason: 'Active OHC amplification sharpens tuning only at low-to-moderate levels; at high SPLs the passive, broadly tuned basilar membrane response dominates.',
      trap: 'Option A reverses the level dependence.'
    },
    {
      id: '2024-Q15', year: 2024, qNum: 15, topic: 'Hearing', solver: 'T12',
      question: 'In the cochlea, inner hair cells (IHCs) and outer hair cells (OHCs) play distinct roles in hearing. Which statement best describes their primary function?',
      options: {
        A: 'IHCs amplify vibrations of the basilar membrane, while OHCs convert vibrations to electrical signals sent to the auditory nerve.',
        B: 'IHCs and OHCs both transmit signals to the auditory nerve; IHCs are sensitive to low frequencies and OHCs to high frequencies.',
        C: 'IHCs primarily transmit sound to the auditory nerve, while OHCs are responsible for the tuning of the basilar membrane and providing level-dependent amplification.',
        D: 'IHCs primarily amplify low-intensity sounds, while OHCs provide basilar membrane tuning.'
      },
      answer: 'C',
      reason: 'IHCs are the sensory transducers (~95% of afferent auditory nerve fibers connect to IHCs); OHCs are the electromotile mechanical amplifiers providing sharp tuning and compression.',
      trap: 'Option A swaps the roles of IHCs and OHCs.'
    }
  ];
});
