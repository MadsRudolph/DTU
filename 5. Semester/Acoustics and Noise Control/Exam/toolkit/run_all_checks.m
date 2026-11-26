function run_all_checks
%RUN_ALL_CHECKS  Run every T*.m template and compare its pre-filled answers
% with the official ones. Run this the evening before the exam (and once
% offline on the exam laptop) to prove MATLAB and every template work.
%
%   cd toolkit;  run_all_checks
%
% Each row: script, variable, element, official answer, tolerance, label.
% A template that crashes is reported as FAIL with its error message.

checks = {
 'T01_plane_wave_reflection',     'p_amp',            1, 0.89,      0.005,   '2024 P1.1 |p| 400 Hz [Pa]'
 'T01_plane_wave_reflection',     'p_amp',            2, 0.86,      0.005,   '2024 P1.1 |p| 630 Hz [Pa]'
 'T01_plane_wave_reflection',     'atten_dB',         1, 29.5,      0.1,     'Week 4 P3 air-water loss [dB]'
 'T02_tube_driven_end',           'Lp_A',             1, 83.1,      0.25,    '2023 P1.1 absorber SPL [dB] (exact 83.3)'
 'T02_tube_driven_end',           'Lp_R1',            1, 109.9,     0.15,    '2023 P1.2 water end SPL [dB]'
 'T03_levels_adding_Leq',         'Lp_A',             1, 57.0,      0.05,    'Week 3 P1.1 SPL [dB]'
 'T03_levels_adding_Leq',         'p_rms_B',          1, 0.161,     0.001,   '2022 MC2 tuning forks [Pa]'
 'T03_levels_adding_Leq',         'L_C',              1, 90,        0.01,    'Week 3 P2.2 120 deg [dB]'
 'T03_levels_adding_Leq',         'L_D',              1, 13.0,      0.02,    '2023 MC1 two 10 dB sources [dB]'
 'T03_levels_adding_Leq',         'L_E',              1, 78.3,      0.05,    'Week 3 P5 background [dB]'
 'T03_levels_adding_Leq',         'Leq_F',            1, 66.2,      0.05,    '2022 MC3 Leq 24 h [dB]'
 'T03_levels_adding_Leq',         'Leq_F2',           1, 62.0,      0.1,     '2024 MC2 Leq 8 h [dB] (option 62)'
 'T03_levels_adding_Leq',         'Leq_G',            1, 87.0,      0.05,    'Text ex 1.3.11 Leq [dB]'
 'T04_octave_bands_A_weighting',  'Lp_band',          2, 70.9,      0.1,     '2023 P2.1 250 Hz band [dB] (exact 71.0)'
 'T04_octave_bands_A_weighting',  'Lp_band',          3, 77.0,      0.06,    '2023 P2.1 500 Hz band [dB]'
 'T04_octave_bands_A_weighting',  'Lp_band',          4, 70.1,      0.06,    '2023 P2.1 1000 Hz band [dB]'
 'T04_octave_bands_A_weighting',  'Lp_band',          5, 57.0,      0.06,    '2023 P2.1 2000 Hz band [dB]'
 'T04_octave_bands_A_weighting',  'Lp_band_detuned',  4, 67.1,      0.06,    '2023 P2.2 detuned 1 kHz band [dB]'
 'T04_octave_bands_A_weighting',  'LA_B',             1, 89.7,      0.05,    '2024 P1.2 A-weighted [dB(A)]'
 'T04_octave_bands_A_weighting',  'LZ_C',             1, 81.5,      0.05,    'Slide 34 total [dB]'
 'T04_octave_bands_A_weighting',  'LA_C',             1, 77.2,      0.05,    'Slide 35 A-weighted [dB(A)]'
 'T05_intensity_power_SWR',       'W_B',              1, 1.54e-3,   0.01e-3, 'Week 4 P2 power [W]'
 'T05_intensity_power_SWR',       'alpha',            1, 0.69,      0.005,   'Week 4 P4.1 alpha'
 'T05_intensity_power_SWR',       'W_abs',            1, 0.87e-6,   0.01e-6, 'Week 4 P4.2 absorbed [W]'
 'T05_intensity_power_SWR',       'LW_abs',           1, 59.4,      0.05,    'Week 4 P4.2 L_W absorbed [dB]'
 'T05_intensity_power_SWR',       'I_A',              1, 459.3e-9,  2e-9,    '2024 P2.2 I at 0.1 m [W/m^2]'
 'T06_monopole_nearfield_power',  'p_amp',            1, 0.030,     0.0005,  '2024 P2.1 |p| 0.1 m [Pa]'
 'T06_monopole_nearfield_power',  'p_amp',            3, 0.010,     0.0005,  '2024 P2.1 |p| 0.3 m [Pa]'
 'T06_monopole_nearfield_power',  'u_amp',            1, 108e-6,    0.5e-6,  '2024 P2.1 |u| 0.1 m [m/s]'
 'T06_monopole_nearfield_power',  'u_amp',            2, 41.5e-6,   0.3e-6,  '2024 P2.1 |u| 0.2 m [m/s]'
 'T06_monopole_nearfield_power',  'u_amp',            3, 25.9e-6,   0.3e-6,  '2024 P2.1 |u| 0.3 m [m/s]'
 'T06_monopole_nearfield_power',  'phase_MC',         1, 30,        0.5,     '2024 MC1 p-u phase [deg]'
 'T06_monopole_nearfield_power',  'Lp_075',           1, 73.46,     0.02,    'Week 8 P1 Lp 0.75 m [dB]'
 'T06_monopole_nearfield_power',  'LW_E',             1, 81.83,     0.02,    'Week 8 P1 L_W [dB]'
 'T07_two_sources_wall_dipole',   'p_rms_A',          1, 0.024,     0.0005,  '2024 P2.2 p_rms 0.1 m [Pa]'
 'T07_two_sources_wall_dipole',   'p_rms_A',          2, 0,         1e-9,    '2024 P2.2 p_rms 0.2 m [Pa]'
 'T07_two_sources_wall_dipole',   'u_rms_A',          1, 82.2e-6,   0.2e-6,  '2024 P2.2 u_rms 0.1 m [m/s]'
 'T07_two_sources_wall_dipole',   'u_rms_A',          2, 58.7e-6,   0.2e-6,  '2024 P2.2 u_rms 0.2 m [m/s]'
 'T07_two_sources_wall_dipole',   'I_A',              1, 459.3e-9,  2e-9,    '2024 P2.2 I 0.1 m [W/m^2]'
 'T07_two_sources_wall_dipole',   'W_wall',           1, 32.7e-6,   0.03*32.7e-6, '2023 P3.1 wall power 20 Hz [W] (3 %)'
 'T07_two_sources_wall_dipole',   'W_wall',           2, 36.6e-6,   0.03*36.6e-6, '2023 P3.1 wall power 200 Hz [W] (3 %)'
 'T07_two_sources_wall_dipole',   'W_wall',           3, 54.4e-6,   0.03*54.4e-6, '2023 P3.1 wall power 2 kHz [W] (3 %)'
 'T07_two_sources_wall_dipole',   'I_B_simple',       2, 0.78e-6,   0.03e-6, '2023 P3.2 I 0.5 m from wall [W/m^2]'
 'T07_two_sources_wall_dipole',   'I_B_simple',       3, 2.45e-6,   0.07e-6, '2023 P3.2 I 1 m from wall [W/m^2]'
 'T07_two_sources_wall_dipole',   'f_cancel',         2, 1500,      1e-9,    '2022 P3.2 next cancellation [Hz]'
 'T07_two_sources_wall_dipole',   'x_c',              1, 2.172,     0.001,   '2022 P3.3 x_c [m]'
 'T07_two_sources_wall_dipole',   'Q1_over_Q2',       1, 1.188,     0.001,   '2022 P3.3 |Q1|/|Q2|'
 'T07_two_sources_wall_dipole',   'I_C',              1, 8.333e-6,  0.05e-6, '2022 P3.4 I midpoint [W/m^2]'
 'T08_loudspeaker',               'Q_amp',            1, 0.0022,    0.00005, '2022 P1.1 |Q| [m^3/s]'
 'T08_loudspeaker',               'p_amp',            1, 0.106,     0.001,   '2022 P1.1 |p| 5 m [Pa]'
 'T08_loudspeaker',               'W',                1, 2.1e-3,    0.05e-3, '2022 P1.1 power [W]'
 'T08_loudspeaker',               'Lp300_massctrl',   1, 81.65,     0.01,    'Week 8 P3.1 [dB]'
 'T08_loudspeaker',               'Lp30_full',        1, 67.49,     0.01,    'Week 8 P3.2 30 Hz [dB]'
 'T08_loudspeaker',               'Lp300_full',       1, 80.96,     0.01,    'Week 8 P3.2 300 Hz [dB]'
 'T08_loudspeaker',               'Lp_free',          1, 8.55,      0.03,    'Week 8 P4 headphone off [dB]'
 'T09_room_modes',                'f_100',            1, 34.3,      0.05,    'Week 6 P1 (1,0,0) [Hz]'
 'T09_room_modes',                'n_modes_below',    1, 8,         0,       'Week 6 P1 modes below 80 Hz'
 'T09_room_modes',                'lz_C',             1, 4,         0.3,     '2022 MC4 height [m] (option B)'
 'T09_room_modes',                'modes_2023',       1, 2,         0,       '2023 MC3 50 Hz band: nx of (2,0,0)'
 'T10_reverberation_diffuse_field','T_sabine',        1, 1.6,       0.02,    '2022 MC5 T [s]'
 'T10_reverberation_diffuse_field','alpha_walls_B',   1, 0.1,       0.01,    '2023 MC5 walls alpha'
 'T10_reverberation_diffuse_field','alpha_needed_B2', 1, 0.4,       0.035,   '2024 MC4 alpha (option 0.4)'
 'T10_reverberation_diffuse_field','Lp_C',            1, 66,        0.5,     '2023 MC7 SPL [dB]'
 'T10_reverberation_diffuse_field','p_on',            1, 1.23,      0.005,   'Week 6 P3.1 p [Pa]'
 'T10_reverberation_diffuse_field','Leq_D',           1, 91,        0.1,     'Week 6 P3.1 Leq [dB]'
 'T10_reverberation_diffuse_field','Leq_total_D',     1, 93,        0.1,     'Week 6 P3.2 Leq [dB]'
 'T10_reverberation_diffuse_field','alpha_E',         1, 0.8,       0.001,   '2022 MC7 ISO 354 alpha'
 'T10_reverberation_diffuse_field','S_needed',        1, 62,        1,       'Week 7 P1.2 area [m^2]'
 'T10_reverberation_diffuse_field','T_s30_sabine',    1, 0.77,      0.01,    'Slide 30 Sabine [s]'
 'T10_reverberation_diffuse_field','T_s30_eyring',    1, 0.65,      0.01,    'Slide 30 Eyring [s]'
 'T11_absorbers',                 'f_membrane',       1, 77,        0.5,     'Week 7 P2.1 membrane [Hz]'
 'T11_absorbers',                 'f_A2',             1, 130,       1,       '2023 MC6 membrane [Hz]'
 'T11_absorbers',                 'L_A3',             1, 0.15,      0.005,   '2024 MC7 cavity depth [m]'
 'T11_absorbers',                 'V_B2',             1, 0.015,     0.0003,  '2024 MC6 Helmholtz volume [m^3]'
 'T11_absorbers',                 'f_helmholtz',      1, 334,       1,       'Week 4 P1 bottle [Hz]'
 'T11_absorbers',                 'f_perf',           1, 432,       1.5,     'Week 7 P2.2 perforated [Hz] (c 343 vs 344)'
 'T11_absorbers',                 'alpha_n',          1, 0.451,     0.001,   'Slide 36 alpha normal'
 'T11_absorbers',                 'alpha_r',          1, 0.53,      0.002,   'Slide 36 alpha random'
 'T11_absorbers',                 'alpha_F',          1, 0.0097,    0.0002,  '2022 MC6 alpha for Z = 1'
 'T12_hearing_ERB_masking',       'ERB',              2, 132.6,     0.1,     'Week 9 P1.1 ERB 1 kHz [Hz]'
 'T12_hearing_ERB_masking',       'ERB',              3, 1104.1,    0.1,     'Week 9 P1.1 ERB 10 kHz [Hz]'
 'T12_hearing_ERB_masking',       'Ls',               1, 50.3,      0.05,    'Week 9 P1.2 threshold 0.1 kHz [dB]'
 'T12_hearing_ERB_masking',       'Ls',               3, 65.2,      0.05,    'Week 9 P1.2 threshold 10 kHz [dB]'
 'T12_hearing_ERB_masking',       'Ls_20Hz',          2, 47.8,      0.05,    'Week 9 P1.3 20 Hz noise [dB]'
 'T12_hearing_ERB_masking',       'L_CT',             2, 25.0,      0.01,    'Week 9 P3.2 CT level 800 Hz [dB]'
 'T12_hearing_ERB_masking',       'N0_req_dB',        1, 21.9,      0.05,    'Week 9 P3.3 N0 [dB/Hz]'
 'T12_hearing_ERB_masking',       'Ls_at_CT',         3, 36.7,      0.05,    'Week 9 P3.3 threshold 700 Hz [dB]'
 'T12_hearing_ERB_masking',       'same_filter',      1, 1,         0,       '2022 MC14 850/900 Hz one filter'
 'T12_hearing_ERB_masking',       'same_filter_2023', 1, 0,         0,       '2023 MC14 400/600 Hz separate'
 'T13_physiology_greenwood_ABR',  'F_base',           1, 20541,     1,       'Week 10 P1 base [Hz]'
 'T13_physiology_greenwood_ABR',  'F_apex',           1, 23.7,      0.1,     'Week 10 P1 apex [Hz]'
 'T13_physiology_greenwood_ABR',  'n_needed',         1, 1000,      0.5,     'Week 10 P2b sweeps'
 'T13_physiology_greenwood_ABR',  'N_eff',            1, 9.905e-6,  0.005e-6,'Week 10 P2c N_eff [V]'
 'T13_physiology_greenwood_ABR',  't_noRej',          1, 545,       1,       'Week 10 P2c no rejection [s]'
 'T13_physiology_greenwood_ABR',  't_rej',            1, 55.6,      0.1,     'Week 10 P2c rejection [s]'
 'T13_physiology_greenwood_ABR',  'F_oae',            1, 1458.3,    0.2,     'Week 10 P3 12 ms [Hz]'
 'T13_physiology_greenwood_ABR',  'F_oae',            3, 6977.4,    0.2,     'Week 10 P3 5 ms [Hz]'
 'T14_vibration_isolation',       'T_dB',             1, 0,         0.4,     '2022 MC11 T at 7 Hz ~ 0 dB (official 0.35)'
 'T14_vibration_isolation',       'f_isolation_starts',1, 7.04,     0.01,    '2024 MC isolation from [Hz]'
 'T14_vibration_isolation',       'f0_B',             1, 4.1,       0.05,    '2023 MC f0 [Hz]'
 'T14_vibration_isolation',       'f0_C',             1, 20.05,     0.01,    'Week 11 P3 f0 [Hz] (official 20.1)'
 'T14_vibration_isolation',       'xi_C',             1, 0.231e-3,  0.001e-3,'Week 11 P3b xi [m]'
 'T14_vibration_isolation',       'Ff_C',             2, 0.625,     0.005,   'Week 11 P3d F floor [N]'
 'T14_vibration_isolation',       's_D',              1, 3365,      5,       'Week 11 P4 stiffness [N/m]'
 'T14_vibration_isolation',       'f0_D',             1, 7.54,      0.01,    'Week 11 P4 f0 [Hz]'
 'T14_vibration_isolation',       'F_E',              1, 3.1416j,   0.01,    '2023 MC force (i 3.14 N)'
 'T15_sound_insulation',          'L2_B',             1, 37.9,      0.05,    '2023 MC8 L2 [dB]'
 'T15_sound_insulation',          'R_res',            1, 35.4,      0.05,    'Slide 18 wall + door [dB]'
 'T15_sound_insulation',          'R_crack',          1, 39.6,      0.05,    'Slide 19 crack [dB]'
 'T15_sound_insulation',          'R_win_C2',         1, 28.5,      0.05,    'Sheet P3 window [dB]'
 'T15_sound_insulation',          'R_win_D',          1, 40.5,      0.05,    '2022 MC8 window [dB]'
 'T15_sound_insulation',          'dfc',              1, -63,       0.5,     '2024 MC8 change of f_c [Hz]'
 'T15_sound_insulation',          'fc_stacked',       1, 3000,      0,       '2022 MC9 stacked f_c [Hz]'
 'T15_sound_insulation',          'fd_dw',            1, 546,       1,       '2024 MC11 f_d [Hz]'
 'T15_sound_insulation',          'R1',               1, 32.08,     0.01,    '2024 MC11 R one board [dB]'
 'T15_sound_insulation',          'gain_double',      1, 32.1,      0.05,    '2024 MC11 gain [dB]'
};

scripts = unique(checks(:,1), 'stable');
ws = struct();
errs = struct();
for i = 1:numel(scripts)
    [ws.(scripts{i}), errs.(scripts{i})] = run_one(scripts{i});
end

fprintf('\n%-5s %-4s %-44s %14s %14s\n', 'RES', 'T', 'check', 'got', 'official');
n_pass = 0;
for i = 1:size(checks, 1)
    [scr, var, idx, expected, tol, label] = checks{i, :};
    tag = scr(1:3);
    if ~isempty(errs.(scr))
        fprintf('FAIL  %-4s %-44s  script error: %s\n', tag, label, errs.(scr));
        continue
    end
    if ~isfield(ws.(scr), var)
        fprintf('FAIL  %-4s %-44s  variable %s missing\n', tag, label, var);
        continue
    end
    v = ws.(scr).(var);
    got = v(idx);
    ok = abs(double(got) - expected) <= tol;
    if ok
        res = 'PASS';
        n_pass = n_pass + 1;
    else
        res = 'FAIL';
    end
    fprintf('%-5s %-4s %-44s %14s %14s\n', res, tag, label, num2str(got, 5), num2str(expected, 5));
end
fprintf('\n%d of %d checks passed, %d templates run.\n', n_pass, size(checks, 1), numel(scripts));
if n_pass < size(checks, 1)
    error('run_all_checks:failed', '%d check(s) failed.', size(checks, 1) - n_pass);
end
end

function [vars__, err__] = run_one(script__)
% Run one template in this function's own workspace, silently, and return
% every variable it created.
err__ = '';
vars__ = struct();
try
    evalc(script__);
catch ME__
    err__ = ME__.message;
    return
end
names__ = who;
for n__ = 1:numel(names__)
    if ~endsWith(names__{n__}, '__')
        vars__.(names__{n__}) = eval(names__{n__});
    end
end
end
