#!/usr/bin/env python3
"""
EM Calc Test Suite
==================
Run this script to verify all em_calc functions work correctly.

Usage:
    python test_em_calc.py
"""

import numpy as np
from em_calc import *

def print_header(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)

def test_stubmatch():
    """Test StubMatch with various load impedances"""
    print_header("TEST: StubMatch")
    
    def verify(ZL, Z0, stub_type='short', name=''):
        result = StubMatch(ZL, Z0, stub_type)
        
        # Verify solution: Y_total should equal 1 + j0
        zL = ZL / Z0
        yL = 1 / zL
        beta = 2 * np.pi
        t = np.tan(beta * result.d)
        y_at_d = (yL + 1j * t) / (1 + 1j * yL * t)
        
        if stub_type == 'short':
            b_stub = -1 / np.tan(beta * result.l)
        else:
            b_stub = np.tan(beta * result.l)
        
        y_total = y_at_d + 1j * b_stub
        error = abs(y_total - 1)
        passed = error < 0.001
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: d={result.d:.4f}λ, ℓ={result.l:.4f}λ  {status}")
        return passed
    
    tests = [
        (142 + 42.5j, 75, 'short', 'Q16 exam (142+j42.5, Z0=75)'),
        (100 + 50j, 50, 'short', 'Inductive load, short stub'),
        (100 + 50j, 50, 'open', 'Inductive load, open stub'),
        (25 - 25j, 50, 'short', 'Capacitive load, short stub'),
        (25 - 25j, 50, 'open', 'Capacitive load, open stub'),
        (150, 50, 'short', 'Pure resistive R > Z0'),
        (25, 75, 'short', 'Pure resistive R < Z0'),
        (50 + 100j, 50, 'short', 'Highly reactive load'),
        (30 - 40j, 50, 'open', 'Complex load, open stub'),
        (200 + 150j, 75, 'short', 'Large impedance'),
    ]
    
    passed = sum(verify(ZL, Z0, st, name) for ZL, Z0, st, name in tests)
    return passed, len(tests)


def test_tline():
    """Test basic TLine calculations"""
    print_header("TEST: TLine")
    
    tests_passed = 0
    total = 0
    
    # Quarter-wave transformer
    total += 1
    t = TLine(50, 100, 0.25)
    if abs(t.Z_in - 25) < 0.01:
        print(f"  Quarter-wave (Z0=50, ZL=100): Z_in={t.Z_in:.2f}Ω (expect 25) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Quarter-wave: Z_in={t.Z_in:.2f}Ω (expect 25) ✗ FAIL")
    
    # Half-wave line
    total += 1
    t = TLine(50, 75+25j, 0.5)
    if abs(t.Z_in - (75+25j)) < 0.01:
        print(f"  Half-wave (ZL=75+j25): Z_in={t.Z_in:.2f}Ω ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Half-wave: Z_in={t.Z_in:.2f}Ω ✗ FAIL")
    
    # VSWR calculation
    total += 1
    t = TLine(50, 100, 0)
    expected_vswr = (100/50 + 50/100) / 2 * 2  # Should be 2
    if abs(t.VSWR - 2) < 0.01:
        print(f"  VSWR (ZL=100, Z0=50): VSWR={t.VSWR:.2f} (expect 2) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  VSWR: {t.VSWR:.2f} (expect 2) ✗ FAIL")
    
    return tests_passed, total


def test_tline_inverse():
    """Test inverse TLine solver"""
    print_header("TEST: TLine Inverse")
    
    tests_passed = 0
    total = 0
    
    # Test: VSWR=3, z_min=0.1λ
    total += 1
    r = TLine_inverse(Z0=75, VSWR=3.0, z_min=0.1)
    fwd = TLine(75, r.ZL, 0)
    if abs(fwd.VSWR - 3.0) < 0.01:
        print(f"  VSWR=3, z_min=0.1λ: Z_L={r.ZL:.2f}Ω, verify VSWR={fwd.VSWR:.2f} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  VSWR mode ✗ FAIL")
    
    # Test: |Γ|=0.5, z_max=0.2λ
    total += 1
    r = TLine_inverse(Z0=50, Gamma_mag=0.5, z_max=0.2)
    fwd = TLine(50, r.ZL, 0)
    if abs(abs(fwd.Gamma_L) - 0.5) < 0.01:
        print(f"  |Γ|=0.5, z_max=0.2λ: |Γ_L|={abs(fwd.Gamma_L):.3f} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Gamma_mag mode ✗ FAIL")
    
    # Test: Γ_dB=-6, z_min=0.15λ
    total += 1
    r = TLine_inverse(Z0=75, Gamma_dB=-6, z_min=0.15)
    expected_mag = 10**(-6/20)  # ~0.501
    if abs(r.Gamma_mag - expected_mag) < 0.01:
        print(f"  Γ=-6dB: |Γ|={r.Gamma_mag:.3f} (expect {expected_mag:.3f}) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Gamma_dB mode ✗ FAIL")
    
    return tests_passed, total


def test_medium():
    """Test Medium properties calculator"""
    print_header("TEST: Medium")
    
    tests_passed = 0
    total = 0
    
    # Lossless dielectric
    total += 1
    m = Medium(4, 10e9)
    if abs(m.n - 2) < 0.01:
        print(f"  Lossless (εr=4): n={m.n:.2f} (expect 2) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Lossless dielectric ✗ FAIL")
    
    # Free space wavelength
    total += 1
    m = Medium(1, 3e8)  # 300 MHz in free space
    if abs(m.lambda_ - 1.0) < 0.01:
        print(f"  Free space (f=300MHz): λ={m.lambda_:.2f}m (expect 1) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Free space wavelength ✗ FAIL")
    
    return tests_passed, total


def test_polarization():
    """Test Polarization analyzer"""
    print_header("TEST: Polarization")
    
    tests_passed = 0
    total = 0
    
    # RHCP
    total += 1
    p = Polarization([1, -1j, 0])
    if p.type == 'Circular' and p.handedness == 'RHCP':
        print(f"  [1, -j, 0]: {p.type}, {p.handedness} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  RHCP test ✗ FAIL")
    
    # LHCP
    total += 1
    p = Polarization([1, 1j, 0])
    if p.type == 'Circular' and p.handedness == 'LHCP':
        print(f"  [1, +j, 0]: {p.type}, {p.handedness} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  LHCP test ✗ FAIL")
    
    # Linear
    total += 1
    p = Polarization([1, 1, 0])
    if p.type == 'Linear':
        print(f"  [1, 1, 0]: {p.type}, tilt={p.tilt_deg:.1f}° ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Linear test ✗ FAIL")
    
    return tests_passed, total


def test_fresnel():
    """Test Fresnel coefficients"""
    print_header("TEST: Fresnel")
    
    tests_passed = 0
    total = 0
    
    # Normal incidence n1=1, n2=2
    total += 1
    f = Fresnel(1, 4)  # n2 = sqrt(4) = 2
    expected_gamma = (1-2)/(1+2)  # -1/3
    if abs(f.Gamma - expected_gamma) < 0.01:
        print(f"  Normal (n1=1, n2=2): Γ={f.Gamma:.4f} (expect -0.333) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Normal incidence ✗ FAIL")
    
    # Transmission coefficient
    total += 1
    expected_tau = 2*1/(1+2)  # 2/3
    if abs(f.tau - expected_tau) < 0.01:
        print(f"  Transmission: τ={f.tau:.4f} (expect 0.667) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Transmission ✗ FAIL")
    
    return tests_passed, total


def test_geometry():
    """Test geometry library functions"""
    print_header("TEST: Geometry Library")
    
    tests_passed = 0
    total = 0
    
    # Solenoid
    total += 1
    L = solenoid_inductance(N=100, A=1e-4, length=0.1)
    expected = 4*np.pi*1e-7 * 100**2 * 1e-4 / 0.1
    if abs(L.L - expected) < 1e-12:
        print(f"  Solenoid (N=100): L={L.L_uH:.2f}μH ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Solenoid ✗ FAIL")
    
    # Parallel plate capacitor
    total += 1
    C = parallel_plate_capacitance(A=0.01, d=1e-3, eps_r=4)
    expected = 8.854187817e-12 * 4 * 0.01 / 1e-3
    if abs(C.C - expected)/expected < 0.001:
        print(f"  Parallel plate: C={C.C_pF:.2f}pF ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Parallel plate ✗ FAIL")
    
    # Coax capacitance
    total += 1
    C = coax_capacitance(a=1e-3, b=3e-3, length=1.0, eps_r=2.1)
    if C.C > 0:
        print(f"  Coax: C={C.C_pF:.2f}pF ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Coax ✗ FAIL")
    
    return tests_passed, total


def test_wave_uniformity():
    """Test wave uniformity analyzer"""
    print_header("TEST: Wave Uniformity")
    
    tests_passed = 0
    total = 0
    
    # Uniform (parallel)
    total += 1
    r = wave_uniformity(alpha=[0, 0, 1], beta=[0, 0, 5])
    if r.is_uniform:
        print(f"  α∥β: {r.classification} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Parallel vectors ✗ FAIL")
    
    # Non-uniform (perpendicular)
    total += 1
    r = wave_uniformity(alpha=[1, 0, 0], beta=[0, 0, 5])
    if not r.is_uniform:
        print(f"  α⊥β: {r.classification}, angle={r.angle_between_deg:.0f}° ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Perpendicular vectors ✗ FAIL")
    
    # Lossless
    total += 1
    r = wave_uniformity(alpha=[0, 0, 0], beta=[0, 0, 5])
    if r.is_uniform and 'Lossless' in r.classification:
        print(f"  Lossless: {r.classification} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Lossless ✗ FAIL")
    
    return tests_passed, total


def main():
    print("\n" + "=" * 60)
    print("       EM CALC TEST SUITE")
    print("=" * 60)
    
    total_passed = 0
    total_tests = 0
    
    # Run all tests
    for test_func in [
        test_stubmatch,
        test_tline,
        test_tline_inverse,
        test_medium,
        test_polarization,
        test_fresnel,
        test_geometry,
        test_wave_uniformity,
    ]:
        passed, total = test_func()
        total_passed += passed
        total_tests += total
    
    # Summary
    print_header("SUMMARY")
    print(f"  Total: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n  ✓ ALL TESTS PASSED! ✓")
    else:
        print(f"\n  ✗ {total_tests - total_passed} test(s) failed")
    
    print("=" * 60 + "\n")
    
    return total_passed == total_tests


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
