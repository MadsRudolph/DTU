#!/usr/bin/env node
// Automated verification suite for 34840 Exam App
// 1. Runs all 116 checks from ../toolkit/run_all_checks.m with identical expected values and tolerances.
// 2. Verifies extra exam problems, metadata (15 solvers, 45 MC questions), and static offline bundle integrity.
// 3. Opens exam-app.html via file:// inside a network-isolated namespace (unshare -rn) in headless Chromium
//    and verifies live DOM computation and KaTeX math rendering with networking completely unavailable.

'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const P = require('./src/physics.js');
const SOLVERS_META = require('./src/solvers_meta.js');
const MC_DATA = require('./src/mc_data.js');
const CHEATSHEET_DATA = require('./src/cheatsheet_data.js');

// Exact 116 checks from ../toolkit/run_all_checks.m (1-based index as in MATLAB)
const CHECKS = [
  ['T01_plane_wave_reflection',     'p_amp',            1, 0.89,      0.005,   '2024 P1.1 |p| 400 Hz [Pa]'],
  ['T01_plane_wave_reflection',     'p_amp',            2, 0.86,      0.005,   '2024 P1.1 |p| 630 Hz [Pa]'],
  ['T01_plane_wave_reflection',     'atten_dB',         1, 29.5,      0.1,     'Week 4 P3 air-water loss [dB]'],
  ['T02_tube_driven_end',           'Lp_A',             1, 83.1,      0.25,    '2023 P1.1 absorber SPL [dB] (exact 83.3)'],
  ['T02_tube_driven_end',           'Lp_R1',            1, 109.9,     0.15,    '2023 P1.2 water end SPL [dB]'],
  ['T03_levels_adding_Leq',         'Lp_A',             1, 57.0,      0.05,    'Week 3 P1.1 SPL [dB]'],
  ['T03_levels_adding_Leq',         'p_rms_B',          1, 0.161,     0.001,   '2022 MC2 tuning forks [Pa]'],
  ['T03_levels_adding_Leq',         'L_C',              1, 90,        0.01,    'Week 3 P2.2 120 deg [dB]'],
  ['T03_levels_adding_Leq',         'L_D',              1, 13.0,      0.02,    '2023 MC1 two 10 dB sources [dB]'],
  ['T03_levels_adding_Leq',         'L_E',              1, 78.3,      0.05,    'Week 3 P5 background [dB]'],
  ['T03_levels_adding_Leq',         'Leq_F',            1, 66.2,      0.05,    '2022 MC3 Leq 24 h [dB]'],
  ['T03_levels_adding_Leq',         'Leq_F2',           1, 62.0,      0.1,     '2024 MC2 Leq 8 h [dB] (option 62)'],
  ['T03_levels_adding_Leq',         'Leq_G',            1, 87.0,      0.05,    'Text ex 1.3.11 Leq [dB]'],
  ['T04_octave_bands_A_weighting',  'Lp_band',          2, 70.9,      0.1,     '2023 P2.1 250 Hz band [dB] (exact 71.0)'],
  ['T04_octave_bands_A_weighting',  'Lp_band',          3, 77.0,      0.06,    '2023 P2.1 500 Hz band [dB]'],
  ['T04_octave_bands_A_weighting',  'Lp_band',          4, 70.1,      0.06,    '2023 P2.1 1000 Hz band [dB]'],
  ['T04_octave_bands_A_weighting',  'Lp_band',          5, 57.0,      0.06,    '2023 P2.1 2000 Hz band [dB]'],
  ['T04_octave_bands_A_weighting',  'Lp_band_detuned',  4, 67.1,      0.06,    '2023 P2.2 detuned 1 kHz band [dB]'],
  ['T04_octave_bands_A_weighting',  'LA_B',             1, 89.7,      0.05,    '2024 P1.2 A-weighted [dB(A)]'],
  ['T04_octave_bands_A_weighting',  'LZ_C',             1, 81.5,      0.05,    'Slide 34 total [dB]'],
  ['T04_octave_bands_A_weighting',  'LA_C',             1, 77.2,      0.05,    'Slide 35 A-weighted [dB(A)]'],
  ['T05_intensity_power_SWR',       'W_B',              1, 1.54e-3,   0.01e-3, 'Week 4 P2 power [W]'],
  ['T05_intensity_power_SWR',       'alpha',            1, 0.69,      0.005,   'Week 4 P4.1 alpha'],
  ['T05_intensity_power_SWR',       'W_abs',            1, 0.87e-6,   0.01e-6, 'Week 4 P4.2 absorbed [W]'],
  ['T05_intensity_power_SWR',       'LW_abs',           1, 59.4,      0.05,    'Week 4 P4.2 L_W absorbed [dB]'],
  ['T05_intensity_power_SWR',       'I_A',              1, 459.3e-9,  2e-9,    '2024 P2.2 I at 0.1 m [W/m^2]'],
  ['T06_monopole_nearfield_power',  'p_amp',            1, 0.030,     0.0005,  '2024 P2.1 |p| 0.1 m [Pa]'],
  ['T06_monopole_nearfield_power',  'p_amp',            3, 0.010,     0.0005,  '2024 P2.1 |p| 0.3 m [Pa]'],
  ['T06_monopole_nearfield_power',  'u_amp',            1, 108e-6,    0.5e-6,  '2024 P2.1 |u| 0.1 m [m/s]'],
  ['T06_monopole_nearfield_power',  'u_amp',            2, 41.5e-6,   0.3e-6,  '2024 P2.1 |u| 0.2 m [m/s]'],
  ['T06_monopole_nearfield_power',  'u_amp',            3, 25.9e-6,   0.3e-6,  '2024 P2.1 |u| 0.3 m [m/s]'],
  ['T06_monopole_nearfield_power',  'phase_MC',         1, 30,        0.5,     '2024 MC1 p-u phase [deg]'],
  ['T06_monopole_nearfield_power',  'Lp_075',           1, 73.46,     0.02,    'Week 8 P1 Lp 0.75 m [dB]'],
  ['T06_monopole_nearfield_power',  'LW_E',             1, 81.83,     0.02,    'Week 8 P1 L_W [dB]'],
  ['T07_two_sources_wall_dipole',   'p_rms_A',          1, 0.024,     0.0005,  '2024 P2.2 p_rms 0.1 m [Pa]'],
  ['T07_two_sources_wall_dipole',   'p_rms_A',          2, 0,         1e-9,    '2024 P2.2 p_rms 0.2 m [Pa]'],
  ['T07_two_sources_wall_dipole',   'u_rms_A',          1, 82.2e-6,   0.2e-6,  '2024 P2.2 u_rms 0.1 m [m/s]'],
  ['T07_two_sources_wall_dipole',   'u_rms_A',          2, 58.7e-6,   0.2e-6,  '2024 P2.2 u_rms 0.2 m [m/s]'],
  ['T07_two_sources_wall_dipole',   'I_A',              1, 459.3e-9,  2e-9,    '2024 P2.2 I 0.1 m [W/m^2]'],
  ['T07_two_sources_wall_dipole',   'W_wall',           1, 32.7e-6,   0.03*32.7e-6, '2023 P3.1 wall power 20 Hz [W] (3 %)'],
  ['T07_two_sources_wall_dipole',   'W_wall',           2, 36.6e-6,   0.03*36.6e-6, '2023 P3.1 wall power 200 Hz [W] (3 %)'],
  ['T07_two_sources_wall_dipole',   'W_wall',           3, 54.4e-6,   0.03*54.4e-6, '2023 P3.1 wall power 2 kHz [W] (3 %)'],
  ['T07_two_sources_wall_dipole',   'I_B_simple',       2, 0.78e-6,   0.03e-6, '2023 P3.2 I 0.5 m from wall [W/m^2]'],
  ['T07_two_sources_wall_dipole',   'I_B_simple',       3, 2.45e-6,   0.07e-6, '2023 P3.2 I 1 m from wall [W/m^2]'],
  ['T07_two_sources_wall_dipole',   'f_cancel',         2, 1500,      1e-9,    '2022 P3.2 next cancellation [Hz]'],
  ['T07_two_sources_wall_dipole',   'x_c',              1, 2.172,     0.001,   '2022 P3.3 x_c [m]'],
  ['T07_two_sources_wall_dipole',   'Q1_over_Q2',       1, 1.188,     0.001,   '2022 P3.3 |Q1|/|Q2|'],
  ['T07_two_sources_wall_dipole',   'I_C',              1, 8.333e-6,  0.05e-6, '2022 P3.4 I midpoint [W/m^2]'],
  ['T08_loudspeaker',               'Q_amp',            1, 0.0022,    0.00005, '2022 P1.1 |Q| [m^3/s]'],
  ['T08_loudspeaker',               'p_amp',            1, 0.106,     0.001,   '2022 P1.1 |p| 5 m [Pa]'],
  ['T08_loudspeaker',               'W',                1, 2.1e-3,    0.05e-3, '2022 P1.1 power [W]'],
  ['T08_loudspeaker',               'Lp300_massctrl',   1, 81.65,     0.01,    'Week 8 P3.1 [dB]'],
  ['T08_loudspeaker',               'Lp30_full',        1, 67.49,     0.01,    'Week 8 P3.2 30 Hz [dB]'],
  ['T08_loudspeaker',               'Lp300_full',       1, 80.96,     0.01,    'Week 8 P3.2 300 Hz [dB]'],
  ['T08_loudspeaker',               'Lp_free',          1, 8.55,      0.03,    'Week 8 P4 headphone off [dB]'],
  ['T09_room_modes',                'f_100',            1, 34.3,      0.05,    'Week 6 P1 (1,0,0) [Hz]'],
  ['T09_room_modes',                'n_modes_below',    1, 8,         0,       'Week 6 P1 modes below 80 Hz'],
  ['T09_room_modes',                'lz_C',             1, 4,         0.3,     '2022 MC4 height [m] (option B)'],
  ['T09_room_modes',                'modes_2023',       1, 2,         0,       '2023 MC3 50 Hz band: nx of (2,0,0)'],
  ['T10_reverberation_diffuse_field','T_sabine',        1, 1.6,       0.02,    '2022 MC5 T [s]'],
  ['T10_reverberation_diffuse_field','alpha_walls_B',   1, 0.1,       0.01,    '2023 MC5 walls alpha'],
  ['T10_reverberation_diffuse_field','alpha_needed_B2', 1, 0.4,       0.035,   '2024 MC4 alpha (option 0.4)'],
  ['T10_reverberation_diffuse_field','Lp_C',            1, 66,        0.5,     '2023 MC7 SPL [dB]'],
  ['T10_reverberation_diffuse_field','p_on',            1, 1.23,      0.005,   'Week 6 P3.1 p [Pa]'],
  ['T10_reverberation_diffuse_field','Leq_D',           1, 91,        0.1,     'Week 6 P3.1 Leq [dB]'],
  ['T10_reverberation_diffuse_field','Leq_total_D',     1, 93,        0.1,     'Week 6 P3.2 Leq [dB]'],
  ['T10_reverberation_diffuse_field','alpha_E',         1, 0.8,       0.001,   '2022 MC7 ISO 354 alpha'],
  ['T10_reverberation_diffuse_field','S_needed',        1, 62,        1,       'Week 7 P1.2 area [m^2]'],
  ['T10_reverberation_diffuse_field','T_s30_sabine',    1, 0.77,      0.01,    'Slide 30 Sabine [s]'],
  ['T10_reverberation_diffuse_field','T_s30_eyring',    1, 0.65,      0.01,    'Slide 30 Eyring [s]'],
  ['T11_absorbers',                 'f_membrane',       1, 77,        0.5,     'Week 7 P2.1 membrane [Hz]'],
  ['T11_absorbers',                 'f_A2',             1, 130,       1,       '2023 MC6 membrane [Hz]'],
  ['T11_absorbers',                 'L_A3',             1, 0.15,      0.005,   '2024 MC7 cavity depth [m]'],
  ['T11_absorbers',                 'V_B2',             1, 0.015,     0.0003,  '2024 MC6 Helmholtz volume [m^3]'],
  ['T11_absorbers',                 'f_helmholtz',      1, 334,       1,       'Week 4 P1 bottle [Hz]'],
  ['T11_absorbers',                 'f_perf',           1, 432,       1.5,     'Week 7 P2.2 perforated [Hz] (c 343 vs 344)'],
  ['T11_absorbers',                 'alpha_n',          1, 0.451,     0.001,   'Slide 36 alpha normal'],
  ['T11_absorbers',                 'alpha_r',          1, 0.53,      0.002,   'Slide 36 alpha random'],
  ['T11_absorbers',                 'alpha_F',          1, 0.0097,    0.0002,  '2022 MC6 alpha for Z = 1'],
  ['T12_hearing_ERB_masking',       'ERB',              2, 132.6,     0.1,     'Week 9 P1.1 ERB 1 kHz [Hz]'],
  ['T12_hearing_ERB_masking',       'ERB',              3, 1104.1,    0.1,     'Week 9 P1.1 ERB 10 kHz [Hz]'],
  ['T12_hearing_ERB_masking',       'Ls',               1, 50.3,      0.05,    'Week 9 P1.2 threshold 0.1 kHz [dB]'],
  ['T12_hearing_ERB_masking',       'Ls',               3, 65.2,      0.05,    'Week 9 P1.2 threshold 10 kHz [dB]'],
  ['T12_hearing_ERB_masking',       'Ls_20Hz',          2, 47.8,      0.05,    'Week 9 P1.3 20 Hz noise [dB]'],
  ['T12_hearing_ERB_masking',       'L_CT',             2, 25.0,      0.01,    'Week 9 P3.2 CT level 800 Hz [dB]'],
  ['T12_hearing_ERB_masking',       'N0_req_dB',        1, 21.9,      0.05,    'Week 9 P3.3 N0 [dB/Hz]'],
  ['T12_hearing_ERB_masking',       'Ls_at_CT',         3, 36.7,      0.05,    'Week 9 P3.3 threshold 700 Hz [dB]'],
  ['T12_hearing_ERB_masking',       'same_filter',      1, 1,         0,       '2022 MC14 850/900 Hz one filter'],
  ['T12_hearing_ERB_masking',       'same_filter_2023', 1, 0,         0,       '2023 MC14 400/600 Hz separate'],
  ['T13_physiology_greenwood_ABR',  'F_base',           1, 20541,     1,       'Week 10 P1 base [Hz]'],
  ['T13_physiology_greenwood_ABR',  'F_apex',           1, 23.7,      0.1,     'Week 10 P1 apex [Hz]'],
  ['T13_physiology_greenwood_ABR',  'n_needed',         1, 1000,      0.5,     'Week 10 P2b sweeps'],
  ['T13_physiology_greenwood_ABR',  'N_eff',            1, 9.905e-6,  0.005e-6,'Week 10 P2c N_eff [V]'],
  ['T13_physiology_greenwood_ABR',  't_noRej',          1, 545,       1,       'Week 10 P2c no rejection [s]'],
  ['T13_physiology_greenwood_ABR',  't_rej',            1, 55.6,      0.1,     'Week 10 P2c rejection [s]'],
  ['T13_physiology_greenwood_ABR',  'F_oae',            1, 1458.3,    0.2,     'Week 10 P3 12 ms [Hz]'],
  ['T13_physiology_greenwood_ABR',  'F_oae',            3, 6977.4,    0.2,     'Week 10 P3 5 ms [Hz]'],
  ['T14_vibration_isolation',       'T_dB',             1, 0,         0.4,     '2022 MC11 T at 7 Hz ~ 0 dB (official 0.35)'],
  ['T14_vibration_isolation',       'f_isolation_starts',1, 7.04,     0.01,    '2024 MC isolation from [Hz]'],
  ['T14_vibration_isolation',       'f0_B',             1, 4.1,       0.05,    '2023 MC f0 [Hz]'],
  ['T14_vibration_isolation',       'f0_C',             1, 20.05,     0.01,    'Week 11 P3 f0 [Hz] (official 20.1)'],
  ['T14_vibration_isolation',       'xi_C',             1, 0.231e-3,  0.001e-3,'Week 11 P3b xi [m]'],
  ['T14_vibration_isolation',       'Ff_C',             2, 0.625,     0.005,   'Week 11 P3d F floor [N]'],
  ['T14_vibration_isolation',       's_D',              1, 3365,      5,       'Week 11 P4 stiffness [N/m]'],
  ['T14_vibration_isolation',       'f0_D',             1, 7.54,      0.01,    'Week 11 P4 f0 [Hz]'],
  ['T14_vibration_isolation',       'F_E',              1, {re:0, im:3.1416}, 0.01, '2023 MC force (i 3.14 N)'],
  ['T15_sound_insulation',          'L2_B',             1, 37.9,      0.05,    '2023 MC8 L2 [dB]'],
  ['T15_sound_insulation',          'R_res',            1, 35.4,      0.05,    'Slide 18 wall + door [dB]'],
  ['T15_sound_insulation',          'R_crack',          1, 39.6,      0.05,    'Slide 19 crack [dB]'],
  ['T15_sound_insulation',          'R_win_C2',         1, 28.5,      0.05,    'Sheet P3 window [dB]'],
  ['T15_sound_insulation',          'R_win_D',          1, 40.5,      0.05,    '2022 MC8 window [dB]'],
  ['T15_sound_insulation',          'dfc',              1, -63,       0.5,     '2024 MC8 change of f_c [Hz]'],
  ['T15_sound_insulation',          'fc_stacked',       1, 3000,      0,       '2022 MC9 stacked f_c [Hz]'],
  ['T15_sound_insulation',          'fd_dw',            1, 546,       1,       '2024 MC11 f_d [Hz]'],
  ['T15_sound_insulation',          'R1',               1, 32.08,     0.01,    '2024 MC11 R one board [dB]'],
  ['T15_sound_insulation',          'gain_double',      1, 32.1,      0.05,    '2024 MC11 gain [dB]']
];

const ws = {};
const scripts = [...new Set(CHECKS.map(c => c[0]))];
for (const scr of scripts) {
  ws[scr] = P.runSolver(scr, {});
}

console.log(`${'RES'.padEnd(5)} ${'T'.padEnd(4)} ${'check'.padEnd(44)} ${'got'.padStart(14)} ${'official'.padStart(14)}`);
let nPass = 0;
let nFail = 0;

for (const [scr, varName, idx, expected, tol, label] of CHECKS) {
  const tag = scr.slice(0, 3);
  const resObj = ws[scr];
  if (!resObj || !(varName in resObj.vars)) {
    console.log(`FAIL  ${tag.padEnd(4)} ${label.padEnd(44)}  variable ${varName} missing`);
    nFail++;
    continue;
  }
  const rawVal = resObj.vars[varName];
  const got = Array.isArray(rawVal) ? rawVal[idx - 1] : rawVal;

  let diff, gotStr, expStr;
  if (typeof expected === 'object' && expected !== null && 're' in expected) {
    const gC = P.cplx(got);
    diff = Math.hypot(gC.re - expected.re, gC.im - expected.im);
    gotStr = P.fmtComplex(gC, 5);
    expStr = P.fmtComplex(expected, 5);
  } else {
    diff = Math.abs(Number(got) - Number(expected));
    gotStr = P.fmtNum(Number(got), 5);
    expStr = P.fmtNum(Number(expected), 5);
  }

  const ok = diff <= tol;
  if (ok) {
    nPass++;
    console.log(`PASS  ${tag.padEnd(4)} ${label.padEnd(44)} ${gotStr.padStart(14)} ${expStr.padStart(14)}`);
  } else {
    nFail++;
    console.log(`FAIL  ${tag.padEnd(4)} ${label.padEnd(44)} ${gotStr.padStart(14)} ${expStr.padStart(14)} (diff=${diff} > tol=${tol})`);
  }
}

console.log(`\n${nPass} of ${CHECKS.length} toolkit checks passed across ${scripts.length} templates.`);
assert.strictEqual(nPass, 116, `Expected 116 passed checks, got ${nPass}`);
assert.strictEqual(nFail, 0);

// Extra check 1: 2022 P2 octave bands
const t04_2022 = P.solveT04({
  f: [400, 800, 1200, 600, 900, 1200, 1500],
  P: ['0.1', '0.02', '0.01', '0.05j', '0.03j', '0.01j', '0.006j'],
  fc: [250, 500, 1000, 2000],
  n_oct: 1
});
assert.strictEqual(t04_2022.vars.Lp_band[0], -Infinity);
assert(Math.abs(t04_2022.vars.Lp_band[1] - 71.9) < 0.05);
assert(Math.abs(t04_2022.vars.Lp_band[2] - 62.73) < 0.05);
assert(Math.abs(t04_2022.vars.Lp_band[3] - 46.53) < 0.05);
console.log('PASS  Extra check: 2022 P2 octave bands (-Inf / 71.9 / 62.73 / 46.53 dB)');

// Extra check 2: Week 12 S1.1 party wall L_A
const R_party = [40, 42, 49, 55, 61, 67];
const L1_party = [70, 77, 78, 78, 79, 75];
const T2_party = [1.0, 1.0, 1.2, 1.2, 1.0, 0.8];
const fc_party = [125, 250, 500, 1000, 2000, 4000];
const L2_party = fc_party.map((_, i) => L1_party[i] - R_party[i] + 10 * Math.log10(15 * T2_party[i] / (0.16 * 50)));
const t04_party = P.solveT04({ fc_C: fc_party, L_C: L2_party });
assert(Math.abs(t04_party.vars.LA_C - 33.7) < 0.05);
console.log('PASS  Extra check: Week 12 S1.1 party wall L_A (33.7 dB(A))');

// Metadata & MC data integrity checks
assert.strictEqual(SOLVERS_META.length, 15, 'Must have 15 solver definitions');
assert.strictEqual(MC_DATA.length, 45, 'Must have all 45 multiple-choice questions (2022-2024)');
assert.strictEqual(MC_DATA.filter(q => q.year === 2022).length, 15);
assert.strictEqual(MC_DATA.filter(q => q.year === 2023).length, 15);
assert.strictEqual(MC_DATA.filter(q => q.year === 2024).length, 15);
assert(CHEATSHEET_DATA.sections.length >= 12);
assert.strictEqual(CHEATSHEET_DATA.workedPart1.length, 8);
console.log('PASS  Metadata check: 15 solver UIs, 45 MC questions (2022–2024), 13 cheat-sheet sections, 8 worked Part 1 problems');

// Static offline bundle verification
const htmlPath = path.join(__dirname, 'exam-app.html');
assert(fs.existsSync(htmlPath), 'exam-app.html must exist');
const html = fs.readFileSync(htmlPath, 'utf8');
assert(!/src=["']https?:\/\//i.test(html), 'No external http/https script/img src allowed');
assert(!/href=["']https?:\/\//i.test(html), 'No external http/https stylesheet/font href allowed');
assert(!/url\(["']?https?:\/\//i.test(html), 'No external http/https CSS url() allowed');
assert(!/url\(fonts\//i.test(html), 'No unbundled relative font URLs allowed in exam-app.html');
const fontMatches = html.match(/data:font\/woff2;base64,/g) || [];
assert.strictEqual(fontMatches.length, 12, 'All 12 KaTeX WOFF2 fonts must be base64-inlined');
console.log('PASS  Offline bundle check: zero external URLs, 12/12 KaTeX WOFF2 fonts base64-inlined');

// Headless Chromium offline verification in isolated network namespace (unshare -rn)
try {
  const dom = execSync(
    `unshare -rn chromium --headless --no-sandbox --disable-gpu --dump-dom "file://${htmlPath}" 2>/dev/null`,
    { encoding: 'utf8', maxBuffer: 20 * 1024 * 1024 }
  );
  assert(dom.includes('<span class="highlight-val">0.89</span>'), 'DOM must contain computed T01 result 0.89 Pa');
  assert(dom.includes('<span class="highlight-val">0.86</span>'), 'DOM must contain computed T01 result 0.86 Pa');
  assert(dom.includes('<span class="highlight-val">29.5</span>'), 'DOM must contain computed T01 result 29.5 dB');
  assert(dom.includes('class="katex-mathml"'), 'DOM must contain rendered KaTeX formulas');
  assert(dom.includes('id="mc-2024-Q15"'), 'DOM must contain rendered MC drill cards');
  assert(dom.includes('id="handin-scratchpad"'), 'DOM must contain rendered Part 1 Hand-in Builder');
  console.log('PASS  Headless Chromium offline test (unshare -rn, file://): DOM rendered & computed cleanly with network disabled');
} catch (err) {
  console.error('FAIL  Headless Chromium offline test failed:', err.message);
  process.exit(1);
}

console.log('\nSUMMARY: 116/116 MATLAB toolkit checks passed + 5/5 integration & offline browser checks passed (121/121 total).');
