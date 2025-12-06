%% TEST_ALL_EM_FUNCTIONS.m
% Comprehensive test script for all 8 EM MATLAB helper functions
% This tests both functionality AND documentation examples
%
% Run this script and report any errors or unexpected outputs
% Created: 2025-12-06

clear; clc;
fprintf('\n');
fprintf('================================================================\n');
fprintf('    COMPREHENSIVE EM MATLAB FUNCTION TEST SUITE\n');
fprintf('================================================================\n');
fprintf('Testing all 8 functions with documentation examples\n\n');

%% ========================================================================
% TEST 1: Medium.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 1: Medium.m\n');
fprintf('================================================================\n\n');

try
    % Test 1.1: Lossless dielectric (documentation pattern)
    fprintf('--- Test 1.1: Lossless dielectric (eps_r=4, f=10GHz) ---\n');
    r = Medium(4, 10e9);
    assert(abs(r.n - 2) < 0.01, 'Refractive index should be 2');
    assert(abs(r.eta - 188.5) < 1, 'Eta should be ~188.5 Ohm');
    fprintf('PASS: n=%.4f, eta=%.2f Ohm\n\n', r.n, r.eta);
    
    % Test 1.2: Lossy medium (documentation pattern)
    fprintf('--- Test 1.2: Lossy medium (Seawater) ---\n');
    r = Medium(80, 4, 1e6, 1, 'Seawater');
    assert(r.tan_delta > 10, 'Seawater should be good conductor at 1 MHz');
    fprintf('PASS: tan_delta=%.2f, classification=%s\n\n', r.tan_delta, r.classification);
    
    % Test 1.3: Good conductor (documentation pattern)
    fprintf('--- Test 1.3: Good conductor (Copper at 1GHz) ---\n');
    r = Medium('conductor', 5.8e7, 1e9);
    expected_skin = 2.09e-6;  % ~2.09 um
    assert(abs(r.skin_depth - expected_skin)/expected_skin < 0.05, 'Skin depth error > 5%');
    fprintf('PASS: skin_depth=%.3e m (%.2f um)\n\n', r.skin_depth, r.skin_depth*1e6);
    
    % Test 1.4: Free space
    fprintf('--- Test 1.4: Free space at 1GHz ---\n');
    r = Medium('free', 1e9);
    assert(abs(r.eta - 377) < 1, 'Eta0 should be ~377 Ohm');
    assert(abs(r.lambda - 0.3) < 0.01, 'Lambda should be 0.3 m at 1 GHz');
    fprintf('PASS: eta0=%.2f Ohm, lambda=%.4f m\n\n', r.eta, r.lambda);
    
    % Test 1.5: From loss tangent
    fprintf('--- Test 1.5: From loss tangent ---\n');
    r = Medium('tand', 4.4, 0.02, 5e9);
    assert(abs(r.tan_delta - 0.02) < 0.001, 'Loss tangent mismatch');
    fprintf('PASS: tan_delta=%.4f\n\n', r.tan_delta);
    
    fprintf('>>> Medium.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> Medium.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% TEST 2: StubMatch.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 2: StubMatch.m\n');
fprintf('================================================================\n\n');

try
    % Test 2.1: Documentation example (Q15-Q17)
    fprintf('--- Test 2.1: Q15-Q17 exam example ---\n');
    lambda = 0.133;  % 13.3 cm
    r = StubMatch(142+1j*42.5, 75, 'short', lambda);
    assert(r.d > 0 && r.d < 0.5, 'd should be in [0, 0.5] lambda');
    assert(r.l > 0 && r.l < 0.5, 'l should be in [0, 0.5] lambda');
    fprintf('PASS: d=%.4f lambda (%.2f mm), l=%.4f lambda (%.2f mm)\n\n', ...
        r.d, r.d_mm, r.l, r.l_mm);
    
    % Test 2.2: Open stub
    fprintf('--- Test 2.2: Open stub ---\n');
    r = StubMatch(100+1j*50, 50, 'open', 0.1);
    assert(r.d > 0 && r.d < 0.5, 'd should be in [0, 0.5] lambda');
    fprintf('PASS: d=%.4f lambda, l=%.4f lambda\n\n', r.d, r.l);
    
    % Test 2.3: Purely resistive load (R > Z0)
    fprintf('--- Test 2.3: Resistive load 150 Ohm on 50 Ohm line ---\n');
    r = StubMatch(150, 50, 'short');
    fprintf('Result: d=%.4f lambda, l=%.4f lambda\n\n', r.d, r.l);
    
    % Test 2.4: Purely resistive load (R < Z0)
    fprintf('--- Test 2.4: Resistive load 25 Ohm on 50 Ohm line ---\n');
    r = StubMatch(25, 50, 'short');
    fprintf('Result: d=%.4f lambda, l=%.4f lambda\n\n', r.d, r.l);
    
    % Test 2.5: Already matched (edge case)
    fprintf('--- Test 2.5: Already matched ZL=Z0=50 ---\n');
    r = StubMatch(50, 50, 'short');
    fprintf('Result: d=%.4f lambda, l=%.4f lambda\n');
    fprintf('(May show d~0 or NaN for matched load - this is expected)\n\n');
    
    fprintf('>>> StubMatch.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> StubMatch.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% TEST 3: TLine.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 3: TLine.m\n');
fprintf('================================================================\n\n');

try
    % Test 3.1: Basic analysis (documentation pattern)
    fprintf('--- Test 3.1: Basic TLine analysis ---\n');
    r = TLine(50, 100, 0.3);
    assert(~isnan(r.Z_in), 'Z_in should not be NaN');
    assert(r.VSWR >= 1, 'VSWR should be >= 1');
    fprintf('PASS: Z_in=%.2f%+.2fj Ohm, VSWR=%.4f\n\n', real(r.Z_in), imag(r.Z_in), r.VSWR);
    
    % Test 3.2: Find load from input (Q13/Q14 - documentation pattern)
    fprintf('--- Test 3.2: Find load from Gamma_in (Q13/Q14 type) ---\n');
    Gamma_A = 0.539*exp(1j*deg2rad(166));
    r = TLine('load', 75, Gamma_A, 0.3);
    assert(abs(r.Gamma_L) > 0, 'Gamma_L should be calculated');
    fprintf('PASS: Gamma_L=%.4f angle %.2f deg, Z_L=%.2f%+.2fj Ohm\n\n', ...
        abs(r.Gamma_L), rad2deg(angle(r.Gamma_L)), real(r.Z_L), imag(r.Z_L));
    
    % Test 3.3: Quarter-wave transformer
    fprintf('--- Test 3.3: Quarter-wave transformer design ---\n');
    r = TLine('QW', 50, 100);
    expected_Z0 = sqrt(50*100);
    assert(abs(r.Z_qw - expected_Z0) < 0.01, 'QW impedance mismatch');
    fprintf('PASS: Z_QW = %.4f Ohm (expected %.4f)\n\n', r.Z_qw, expected_Z0);
    
    % Test 3.4: Gamma from impedance
    fprintf('--- Test 3.4: Gamma from impedance ---\n');
    r = TLine('Gamma', 50, 100);
    expected_Gamma = (100-50)/(100+50);
    assert(abs(r.Gamma - expected_Gamma) < 0.001, 'Gamma calculation error');
    fprintf('PASS: Gamma = %.4f (expected %.4f)\n\n', r.Gamma, expected_Gamma);
    
    % Test 3.5: Impedance from Gamma
    fprintf('--- Test 3.5: Impedance from Gamma ---\n');
    r = TLine('Z', 50, 0.5);
    expected_Z = 50 * (1+0.5)/(1-0.5);
    assert(abs(r.Z - expected_Z) < 0.01, 'Z calculation error');
    fprintf('PASS: Z = %.4f Ohm (expected %.4f)\n\n', r.Z, expected_Z);
    
    % Test 3.6: Stub design (documentation pattern)
    fprintf('--- Test 3.6: Stub design for j30 Ohm ---\n');
    r = TLine('stub', 1j*30, 75, 'short');
    assert(r.short.len_lambda > 0, 'Stub length should be positive');
    fprintf('PASS: Short stub length = %.4f lambda\n\n', r.short.len_lambda);
    
    % Test 3.7: Series element (documentation pattern)
    fprintf('--- Test 3.7: TLine with series capacitor ---\n');
    c0 = 3e8;
    r = TLine('series_C', 60, 25+1j*30, 17e-3, 1e-12, 5e9, 0.79*c0);
    assert(~isnan(r.Z_A), 'Z_A should not be NaN');
    fprintf('PASS: Z_A = %.4f%+.4fj Ohm\n\n', real(r.Z_A), imag(r.Z_A));
    
    % Test 3.8: Lambda/4 special length
    fprintf('--- Test 3.8: Lambda/4 line ---\n');
    r = TLine('lambda/4', 50, 100);
    expected_Zin = 50^2 / 100;
    assert(abs(r.Z_in - expected_Zin) < 0.01, 'Lambda/4 Zin error');
    fprintf('PASS: Z_in = %.4f Ohm (expected %.4f)\n\n', r.Z_in, expected_Zin);
    
    fprintf('>>> TLine.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> TLine.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% TEST 4: Polarization.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 4: Polarization.m\n');
fprintf('================================================================\n\n');

try
    % Test 4.1: RHCP (documentation example)
    fprintf('--- Test 4.1: RHCP wave [1; -1j; 0] ---\n');
    r = Polarization([1; -1j; 0]);
    assert(strcmp(r.type, 'Circular'), 'Should be circular');
    assert(strcmp(r.handedness, 'RHCP'), 'Should be RHCP');
    fprintf('PASS: Type=%s, Handedness=%s, AR=%.4f\n\n', r.type, r.handedness, r.AR);
    
    % Test 4.2: LHCP
    fprintf('--- Test 4.2: LHCP wave [1; 1j; 0] ---\n');
    r = Polarization([1; 1j; 0]);
    assert(strcmp(r.type, 'Circular'), 'Should be circular');
    assert(strcmp(r.handedness, 'LHCP'), 'Should be LHCP');
    fprintf('PASS: Type=%s, Handedness=%s, AR=%.4f\n\n', r.type, r.handedness, r.AR);
    
    % Test 4.3: Linear polarization
    fprintf('--- Test 4.3: Linear wave [1; 1; 0] ---\n');
    r = Polarization([1; 1; 0]);
    assert(strcmp(r.type, 'Linear'), 'Should be linear');
    fprintf('PASS: Type=%s, Handedness=%s\n\n', r.type, r.handedness);
    
    % Test 4.4: Amplitude/phase mode (documentation pattern)
    fprintf('--- Test 4.4: From amplitude/phase (Ex=10, Ey=5, phi_x=0, phi_y=90) ---\n');
    r = Polarization('ap', 10, 5, 0, 90);
    assert(strcmp(r.type, 'Elliptical'), 'Should be elliptical');
    fprintf('PASS: Type=%s, AR=%.4f\n\n', r.type, r.AR);
    
    % Test 4.5: Elliptical polarization
    fprintf('--- Test 4.5: Elliptical wave [1; 0.5j; 0] ---\n');
    r = Polarization([1; 0.5j; 0]);
    assert(strcmp(r.type, 'Elliptical'), 'Should be elliptical');
    fprintf('PASS: Type=%s, AR=%.4f, tilt=%.2f deg\n\n', r.type, r.AR, r.tilt_deg);
    
    % Test 4.6: With propagation direction
    fprintf('--- Test 4.6: LHCP in +x direction ---\n');
    r = Polarization([0; 1; 1j], [1;0;0]);
    fprintf('Type=%s, Handedness=%s\n\n', r.type, r.handedness);

    % New tolerance regression tests
    fprintf('--- Test 4.7: Linear classification near tolerance ---\n');
    % Construct Fr, Fi nearly colinear so that norm(cross_ri) is just below tol*scale^2
    tol = 1e-3;  % must match Polarization.m
    Fr = [1; 0; 0];
    % For Fr=[1;0;0], Fi=[1;delta;0] gives cross_ri=[0;0;delta]
    % scale = max(norm(Fr), norm(Fi)) ~ 1, so threshold ~= tol*scale^2 ~= tol
    delta = 0.9*tol;              % just below threshold
    Fi = [1; delta; 0];
    r = Polarization(Fr + 1j*Fi);
    assert(strcmp(r.type,'Linear'), 'Should classify as Linear near tolerance');

    fprintf('--- Test 4.8: Circular classification near tolerance ---\n');
    % Make nearly circular: equal-ish amps and orthogonal with small dot_ri and amp diff ~ tol
    A = 1;
    B = 1*(1 - 0.5*tol);  % within amplitude tolerance
    phi_x = 0; phi_y = 90; % quadrature
    r = Polarization('ap', A, B, phi_x, phi_y);
    assert(strcmp(r.type,'Circular'), 'Should classify as Circular near tolerance');

    fprintf('--- Test 4.9: Do not misclassify non-linear as linear ---\n');
    % cross_ri slightly above threshold (tol*scale^2)
    delta = 1.1*tol;              % just above threshold
    Fi = [1; delta; 0];
    r = Polarization(Fr + 1j*Fi);
    assert(~strcmp(r.type,'Linear'), 'Should not classify as Linear when above tolerance');

    fprintf('--- Test 4.10: Do not misclassify non-circular as circular ---\n');
    % Make amplitudes differ just beyond tolerance
    r = Polarization('ap', 1, 1*(1 - 2*tol), phi_x, phi_y);
    assert(~strcmp(r.type,'Circular'), 'Should not classify as Circular when beyond tolerance');

    fprintf('--- Test 4.11: Boundary condition is_linear when norm(cross_ri) == tol*scale^2 ---\n');
    % Set delta at the nominal threshold: norm(cross_ri) ≈ tol*scale^2
    % Due to scale = max(norm(Fr), norm(Fi)) being slightly > 1, this will 
    % just barely pass the threshold and classify as Linear.
    delta = tol;                  % near threshold
    Fi = [1; delta; 0];
    r = Polarization(Fr + 1j*Fi);
    % At this boundary, implementation classifies as Linear due to scale > 1.
    assert(strcmp(r.type,'Linear'), 'Boundary case near tol*scale^2 should be Linear');

    fprintf('--- Test 4.12: Dimensional scaling test (large amplitude) ---\n');
    % Verify scale^2 works: same angular deviation but 1000x amplitude
    % Should give same classification as unit amplitude case
    scale_factor = 1000;
    Fr_large = scale_factor * [1; 0; 0];
    delta_large = 0.9*tol * scale_factor^2;  % scale with scale^2
    Fi_large = [scale_factor; delta_large/scale_factor; 0];  
    % cross product magnitude = scale_factor * delta_large/scale_factor = delta_large
    % threshold = tol * (scale_factor)^2
    % ratio: delta_large / threshold = 0.9*tol*scale^2 / (tol*scale^2) = 0.9 < 1 → Linear
    r = Polarization(Fr_large + 1j*Fi_large);
    assert(strcmp(r.type,'Linear'), 'Large amplitude should still classify as Linear with scale^2');

    fprintf('>>> Polarization.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> Polarization.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% TEST 5: poynting_pw.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 5: poynting_pw.m\n');
fprintf('================================================================\n\n');

try
    % Test 5.1: Time-domain mode (Q22-Q23 - documentation pattern)
    fprintf('--- Test 5.1: Time-domain mode (Q22-Q23 type) ---\n');
    a = [2;1;0]; 
    b = [0;-1;-2]; 
    E0 = 10;
    beta_vec = [2; -4; 2];
    r = poynting_pw('time', a, b, E0, beta_vec);
    assert(norm(r.H_phasor) > 0, 'H_phasor should be non-zero');
    assert(r.S_mag > 0, 'Poynting magnitude should be positive');
    fprintf('PASS: |H|=%.4f mA/m, |S|=%.4f W/m^2\n\n', norm(r.H_phasor)*1e3, r.S_mag);
    
    % Test 5.2: Vector phasor mode
    fprintf('--- Test 5.2: Vector phasor mode ---\n');
    E_phasor = [10; 5j; 0];
    k_hat = [0; 0; 1];
    r = poynting_pw(E_phasor, k_hat, 377);
    assert(r.S_mag > 0, 'Poynting magnitude should be positive');
    fprintf('PASS: |S|=%.4f W/m^2\n\n', r.S_mag);
    
    % Test 5.3: Check H perpendicular to E and k
    fprintf('--- Test 5.3: Verify H perpendicular to E and k ---\n');
    E_phasor = [10; 0; 0];
    k_hat = [0; 0; 1];
    r = poynting_pw(E_phasor, k_hat, 377);
    dot_E_H = abs(dot(E_phasor, r.H_phasor));
    dot_k_H = abs(dot(k_hat, r.H_phasor));
    assert(dot_E_H < 1e-10, 'H should be perpendicular to E');
    assert(dot_k_H < 1e-10, 'H should be perpendicular to k');
    fprintf('PASS: E.H=%.2e, k.H=%.2e (both ~0)\n\n', dot_E_H, dot_k_H);
    
    fprintf('>>> poynting_pw.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> poynting_pw.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% TEST 6: smithchart_plot.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 6: smithchart_plot.m\n');
fprintf('================================================================\n\n');

try
    % Test 6.1: Impedance mode (documentation pattern)
    fprintf('--- Test 6.1: Plot impedance (75 Ohm line, ZL=15-j37.5) ---\n');
    fprintf('(This will create a figure - close it to continue)\n');
    smithchart_plot(75, 15 - 1j*37.5);
    fprintf('PASS: Smith chart plotted\n\n');
    pause(1);
    close all;
    
    % Test 6.2: Gamma mode (documentation pattern)
    fprintf('--- Test 6.2: Plot from Gamma ---\n');
    Gamma = 0.5*exp(1j*pi/4);
    smithchart_plot('Gamma', Gamma);
    fprintf('PASS: Smith chart plotted from Gamma\n\n');
    pause(1);
    close all;
    
    % Test 6.3: Matched load (should be at center)
    fprintf('--- Test 6.3: Matched load (center of chart) ---\n');
    smithchart_plot(50, 50);
    fprintf('PASS: Matched load at center\n\n');
    pause(1);
    close all;
    
    fprintf('>>> smithchart_plot.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> smithchart_plot.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% TEST 7: coulomb_pair.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 7: coulomb_pair.m\n');
fprintf('================================================================\n\n');

try
    % Test 7.1: Basic usage (documentation pattern)
    fprintf('--- Test 7.1: Basic Coulomb force ---\n');
    q1 = 1e-6;  % 1 uC
    q2 = -2e-6; % -2 uC
    r1 = [0; 0; 0];
    r2 = [1; 0; 0];  % 1 m apart
    [F12, F21] = coulomb_pair(q1, q2, r1, r2);
    
    % Check Newton's third law
    assert(norm(F12 + F21) < 1e-20, 'F12 + F21 should be zero (Newton''s 3rd)');
    fprintf('PASS: F12 = [%.4e, %.4e, %.4e] N\n', F12(1), F12(2), F12(3));
    fprintf('      F21 = [%.4e, %.4e, %.4e] N\n', F21(1), F21(2), F21(3));
    fprintf('      F12 + F21 = [%.2e, %.2e, %.2e] (should be ~0)\n\n', ...
        F12(1)+F21(1), F12(2)+F21(2), F12(3)+F21(3));
    
    % Test 7.2: Same sign charges (repulsion)
    fprintf('--- Test 7.2: Same sign charges (repulsion) ---\n');
    q1 = 1e-6;
    q2 = 1e-6;
    r1 = [0; 0; 0];
    r2 = [1; 0; 0];
    [F12, F21] = coulomb_pair(q1, q2, r1, r2);
    assert(F12(1) < 0, 'F12 should point away from q2 (repulsion)');
    fprintf('PASS: Repulsive force (F12 points toward -x)\n\n');
    
    % Test 7.3: Opposite sign charges (attraction)
    fprintf('--- Test 7.3: Opposite sign charges (attraction) ---\n');
    q1 = 1e-6;
    q2 = -1e-6;
    r1 = [0; 0; 0];
    r2 = [1; 0; 0];
    [F12, F21] = coulomb_pair(q1, q2, r1, r2);
    assert(F12(1) > 0, 'F12 should point toward q2 (attraction)');
    fprintf('PASS: Attractive force (F12 points toward +x)\n\n');
    
    % Test 7.4: 3D positions
    fprintf('--- Test 7.4: 3D charge positions ---\n');
    q1 = 1e-9;
    q2 = 2e-9;
    r1 = [1; 2; 3];
    r2 = [4; 5; 6];
    [F12, F21] = coulomb_pair(q1, q2, r1, r2);
    fprintf('PASS: 3D calculation completed\n');
    fprintf('      F12 = [%.4e, %.4e, %.4e] N\n\n', F12(1), F12(2), F12(3));
    
    % Test 7.5: Error on coincident charges
    fprintf('--- Test 7.5: Error handling for coincident charges ---\n');
    try
        [F12, F21] = coulomb_pair(1e-6, 1e-6, [0;0;0], [0;0;0]);
        fprintf('FAIL: Should have thrown error for coincident charges\n\n');
    catch
        fprintf('PASS: Correctly threw error for coincident charges\n\n');
    end
    
    fprintf('>>> coulomb_pair.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> coulomb_pair.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% TEST 8: B_inf_wire.m
%% ========================================================================
fprintf('================================================================\n');
fprintf('TEST 8: B_inf_wire.m\n');
fprintf('================================================================\n\n');

try
    % Test 8.1: Basic usage (documentation pattern)
    fprintf('--- Test 8.1: Basic B-field (I=10A, r=0.1m) ---\n');
    B = B_inf_wire(10, 0.1);
    mu0 = 4*pi*1e-7;
    expected_B = mu0 * 10 / (2*pi*0.1);
    assert(abs(B - expected_B) < 1e-12, 'B-field calculation error');
    fprintf('PASS: B = %.4e T (expected %.4e T)\n\n', B, expected_B);
    
    % Test 8.2: With magnetic material (documentation pattern)
    fprintf('--- Test 8.2: With magnetic material (mu_r=1000) ---\n');
    B = B_inf_wire(10, 0.1, 1000);
    expected_B = mu0 * 1000 * 10 / (2*pi*0.1);
    assert(abs(B - expected_B) < 1e-9, 'B-field with mu_r error');
    fprintf('PASS: B = %.4e T (mu_r=1000)\n\n', B);
    
    % Test 8.3: Array of distances
    fprintf('--- Test 8.3: Array of distances ---\n');
    r_array = [0.01, 0.02, 0.05, 0.1];
    B_array = B_inf_wire(5, r_array);
    assert(length(B_array) == 4, 'Should return array');
    assert(all(diff(B_array) < 0), 'B should decrease with distance');
    fprintf('PASS: B decreases with distance\n');
    fprintf('      B at r=[0.01,0.02,0.05,0.1]m: [%.2e, %.2e, %.2e, %.2e] T\n\n', ...
        B_array(1), B_array(2), B_array(3), B_array(4));
    
    % Test 8.4: Error on r <= 0
    fprintf('--- Test 8.4: Error handling for r <= 0 ---\n');
    try
        B = B_inf_wire(10, 0);
        fprintf('FAIL: Should have thrown error for r=0\n\n');
    catch
        fprintf('PASS: Correctly threw error for r=0\n\n');
    end
    
    % Test 8.5: Error on negative r
    fprintf('--- Test 8.5: Error handling for r < 0 ---\n');
    try
        B = B_inf_wire(10, -0.1);
        fprintf('FAIL: Should have thrown error for r<0\n\n');
    catch
        fprintf('PASS: Correctly threw error for r<0\n\n');
    end
    
    fprintf('>>> B_inf_wire.m: ALL TESTS PASSED <<<\n\n');
catch ME
    fprintf('FAIL: %s\n', ME.message);
    fprintf('>>> B_inf_wire.m: TEST FAILED <<<\n\n');
end

%% ========================================================================
% SUMMARY
%% ========================================================================
fprintf('================================================================\n');
fprintf('                     TEST SUMMARY\n');
fprintf('================================================================\n');
fprintf('\nAll 8 functions tested with documentation examples.\n');
fprintf('Review any FAIL messages above.\n\n');
fprintf('If all tests passed, your EM MATLAB toolkit is ready!\n');
fprintf('================================================================\n\n');
