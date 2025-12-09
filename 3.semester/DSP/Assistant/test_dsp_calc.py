#!/usr/bin/env python3
"""
DSP Calc Test Suite
===================
Run this script to verify all dsp_calc functions work correctly.

Usage:
    python test_dsp_calc.py
"""

import numpy as np
from dsp_calc import *

def print_header(title):
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def test_step_to_impulse():
    """Test Step→Impulse conversion"""
    print_header("TEST: StepToImpulse")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Basic step response from mock exam
    total += 1
    y_step = [2, 3, -3, -2, 0, 0]
    result = StepToImpulse(y_step)
    expected_h = [2, 1, -6, 1, 2, 0]
    
    if np.allclose(result.h[:6], expected_h):
        print(f"  Basic case: y_step={y_step[:4]}... → h={list(result.h[:5])} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Basic case: h={list(result.h[:5])} (expected {expected_h[:5]}) ✗ FAIL")
    
    # Test 2: Simple step response
    total += 1
    y_step = [1, 1, 1, 1]
    result = StepToImpulse(y_step)
    expected_h = [1, 0, 0, 0]
    
    if np.allclose(result.h, expected_h):
        print(f"  Constant step: y_step=[1,1,1,1] → h={list(result.h)} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Constant step: h={list(result.h)} (expected {expected_h}) ✗ FAIL")
    
    return tests_passed, total


def test_system_function():
    """Test SystemFunction"""
    print_header("TEST: SystemFunction")
    
    tests_passed = 0
    total = 0
    
    # Test 1: FIR
    total += 1
    B = [1, 2, 1]
    result = SystemFunction(B)
    
    if result.is_FIR and result.order == 2:
        print(f"  FIR [1,2,1]: order={result.order}, FIR={result.is_FIR} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  FIR test ✗ FAIL")
    
    # Test 2: IIR
    total += 1
    B = [1, 0]
    A = [1, -0.5]
    result = SystemFunction(B, A)
    
    if not result.is_FIR and len(result.poles) == 1:
        print(f"  IIR 1/(1-0.5z^-1): poles={result.poles} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  IIR test ✗ FAIL")
    
    return tests_passed, total


def test_pole_zero_analysis():
    """Test PoleZeroAnalysis"""
    print_header("TEST: PoleZeroAnalysis")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Stable IIR
    total += 1
    B = [1]
    A = [1, -0.5]  # Pole at z=0.5
    result = PoleZeroAnalysis(B, A)
    
    if result.is_stable and result.poles_inside_UC == 1:
        print(f"  Stable IIR (pole at 0.5): stable={result.is_stable} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Stable IIR test ✗ FAIL")
    
    # Test 2: Unstable IIR
    total += 1
    B = [1]
    A = [1, -2]  # Pole at z=2
    result = PoleZeroAnalysis(B, A)
    
    if not result.is_stable and result.poles_outside_UC == 1:
        print(f"  Unstable IIR (pole at 2): stable={result.is_stable} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Unstable IIR test ✗ FAIL")
    
    # Test 3: FIR always stable
    total += 1
    B = [1, 2, 3, 2, 1]
    result = PoleZeroAnalysis(B)
    
    if result.is_stable:
        print(f"  FIR always stable: {result.stability_reason} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  FIR stability test ✗ FAIL")
    
    return tests_passed, total


def test_inverse_system():
    """Test InverseSystem"""
    print_header("TEST: InverseSystem")
    
    tests_passed = 0
    total = 0
    
    # Test 1: FIR with zeros inside UC
    total += 1
    B = [1, -0.5]  # Zero at z=0.5 (inside)
    result = InverseSystem(B)
    
    if result.can_be_both:
        print(f"  Zero inside UC: can_be_both={result.can_be_both} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Zero inside UC test ✗ FAIL")
    
    # Test 2: FIR with zero outside UC
    total += 1
    B = [1, -2]  # Zero at z=2 (outside)
    result = InverseSystem(B)
    
    if not result.can_be_both and result.zeros_outside_UC == 1:
        print(f"  Zero outside UC: can_be_both={result.can_be_both} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Zero outside UC test ✗ FAIL")
    
    return tests_passed, total


def test_cascade():
    """Test CascadeDecomposition"""
    print_header("TEST: CascadeDecomposition")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Simple cascade
    total += 1
    H1 = [1, 1]
    H2 = [2, -1, -5, 6]  # Expected result
    H_total = np.convolve(H1, H2)
    
    result = CascadeDecomposition(H_total, H1)
    
    if result.is_exact and np.allclose(result.H2, H2):
        print(f"  Cascade: H_total/H1 = H2 ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Cascade test ✗ FAIL")
    
    return tests_passed, total


def test_linear_phase():
    """Test LinearPhaseCheck"""
    print_header("TEST: LinearPhaseCheck")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Symmetric Type I
    total += 1
    h = [1, 2, 3, 2, 1]
    result = LinearPhaseCheck(h)
    
    if result.is_symmetric and result.filter_type == 1:
        print(f"  Type I symmetric: filter_type={result.filter_type} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Type I test ✗ FAIL")
    
    # Test 2: Positive A(ω)
    total += 1
    h = [1, 2, 3, 2, 1]  # Should have A(ω) ≥ 0
    result = LinearPhaseCheck(h)
    
    if result.is_positive:
        print(f"  Positive A(ω): min={result.A_min:.4f} ≥ 0 ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Positive A(ω) test ✗ FAIL")
    
    # Test 3: Negative A(ω) - the trap!
    total += 1
    h = [2, 1, -6, 1, 2]  # This has A(ω) < 0!
    result = LinearPhaseCheck(h)
    
    if not result.is_positive:
        print(f"  Negative A(ω) trap: min={result.A_min:.4f} < 0 ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Negative A(ω) trap test ✗ FAIL")
    
    return tests_passed, total


def test_prewarp():
    """Test Prewarp"""
    print_header("TEST: Prewarp")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Basic prewarping
    total += 1
    F = 2000
    Fs = 8000
    result = Prewarp(F, Fs)
    
    # Manual calculation
    expected_Omega = 2 * Fs * np.tan(np.pi * F / Fs)
    
    if abs(result.Omega - expected_Omega) < 0.01:
        print(f"  Prewarp (F=2kHz, Fs=8kHz): Ω={result.Omega:.2f} rad/s ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Prewarp test ✗ FAIL")
    
    return tests_passed, total


def test_butterworth_order():
    """Test ButterworthOrder"""
    print_header("TEST: ButterworthOrder")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Lowpass order
    total += 1
    result = ButterworthOrder(
        Ap_dB=1, As_dB=20,
        Omega_p=1000, Omega_s=2000,
        filter_type='lowpass'
    )
    
    # Order should be around 3-4 for these specs
    if 2 <= result.N <= 5:
        print(f"  LP order: N={result.N} (expect 3-4) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  LP order: N={result.N} ✗ FAIL")
    
    # Test 2: Highpass - ratio should be inverted
    total += 1
    result_lp = ButterworthOrder(1, 20, 1000, 2000, 'lowpass')
    result_hp = ButterworthOrder(1, 20, 2000, 1000, 'highpass')
    
    # Both should give same order
    if result_lp.N == result_hp.N:
        print(f"  HP order matches LP: N={result_hp.N} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  HP order test ✗ FAIL")
    
    return tests_passed, total


def test_ideal_impulse():
    """Test IdealImpulseResponse"""
    print_header("TEST: IdealImpulseResponse")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Lowpass center value
    total += 1
    omega_c = np.pi / 2
    N = 11
    result = IdealImpulseResponse(omega_c, N, 'lowpass')
    
    expected_center = omega_c / np.pi
    actual_center = result.h_ideal[5]  # Center index
    
    if abs(actual_center - expected_center) < 0.01:
        print(f"  LP h[0]: {actual_center:.4f} (expect {expected_center:.4f}) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  LP h[0] test ✗ FAIL")
    
    # Test 2: Highpass is delta minus lowpass
    total += 1
    result_hp = IdealImpulseResponse(omega_c, N, 'highpass')
    result_lp = IdealImpulseResponse(omega_c, N, 'lowpass')
    
    delta = np.zeros(N)
    delta[5] = 1
    expected_hp = delta - result_lp.h_ideal
    
    if np.allclose(result_hp.h_ideal, expected_hp):
        print(f"  HP = δ - LP: verified ✓ PASS")
        tests_passed += 1
    else:
        print(f"  HP formula test ✗ FAIL")
    
    return tests_passed, total


def test_windowing():
    """Test WindowedFIR"""
    print_header("TEST: WindowedFIR")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Hamming window center value
    total += 1
    h_ideal = np.ones(21)
    result = WindowedFIR(h_ideal, 'hamming')
    
    # Center of Hamming should be 1.0
    center_val = result.window[10]
    if abs(center_val - 1.0) < 0.01:
        print(f"  Hamming center: {center_val:.4f} (expect 1.0) ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Hamming center test ✗ FAIL")
    
    # Test 2: Rectangular window is all ones
    total += 1
    result = WindowedFIR(h_ideal, 'rectangular')
    
    if np.allclose(result.window, np.ones(21)):
        print(f"  Rectangular window: all ones ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Rectangular test ✗ FAIL")
    
    return tests_passed, total


def test_sampling():
    """Test SamplingAnalysis"""
    print_header("TEST: SamplingAnalysis")
    
    tests_passed = 0
    total = 0
    
    # Test 1: No aliasing
    total += 1
    frequencies = [500, 1000, 1200]
    Fs = 3000
    result = SamplingAnalysis(frequencies, Fs)
    
    if not result.has_aliasing and np.allclose(result.apparent_frequencies, frequencies):
        print(f"  No aliasing (Fs=3kHz): correct ✓ PASS")
        tests_passed += 1
    else:
        print(f"  No aliasing test ✗ FAIL")
    
    # Test 2: Aliasing occurs
    total += 1
    frequencies = [500, 1200, 1800]
    Fs = 3000  # Nyquist = 1500 Hz
    result = SamplingAnalysis(frequencies, Fs)
    
    # 1800 Hz should alias to 3000-1800 = 1200 Hz
    if result.has_aliasing and result.aliased[2]:
        expected_alias = 1200
        if abs(result.apparent_frequencies[2] - expected_alias) < 1:
            print(f"  Aliasing: 1800 Hz → {result.apparent_frequencies[2]:.0f} Hz ✓ PASS")
            tests_passed += 1
        else:
            print(f"  Aliasing value test ✗ FAIL")
    else:
        print(f"  Aliasing detection test ✗ FAIL")
    
    return tests_passed, total


def test_minphase():
    """Test MinPhaseDecomposition"""
    print_header("TEST: MinPhaseDecomposition")
    
    tests_passed = 0
    total = 0
    
    # Test 1: Zero outside UC gets reflected
    total += 1
    B = np.poly([2, 0.5])  # Zeros at 2 (outside) and 0.5 (inside)
    result = MinPhaseDecomposition(B)
    
    if len(result.zeros_outside_UC) == 1 and abs(result.zeros_outside_UC[0] - 2) < 0.01:
        print(f"  Zero at 2 detected outside UC ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Zero detection test ✗ FAIL")
    
    # Test 2: Reflection is correct
    total += 1
    expected_reflection = 0.5  # 1/2 = 0.5
    if len(result.zeros_reflected) == 1 and abs(result.zeros_reflected[0] - expected_reflection) < 0.01:
        print(f"  Reflection: 2 → {result.zeros_reflected[0]:.2f} ✓ PASS")
        tests_passed += 1
    else:
        print(f"  Reflection test ✗ FAIL")
    
    return tests_passed, total


def main():
    print("\n" + "=" * 60)
    print("       DSP CALC TEST SUITE")
    print("       DTU 62743 - Digital Signal Processing")
    print("=" * 60)
    
    total_passed = 0
    total_tests = 0
    
    # Run all tests
    for test_func in [
        test_step_to_impulse,
        test_system_function,
        test_pole_zero_analysis,
        test_inverse_system,
        test_cascade,
        test_linear_phase,
        test_prewarp,
        test_butterworth_order,
        test_ideal_impulse,
        test_windowing,
        test_sampling,
        test_minphase,
    ]:
        passed, total = test_func()
        total_passed += passed
        total_tests += total
    
    # Summary
    print_header("SUMMARY")
    print(f"  Total: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n  ✓ ALL TESTS PASSED! ✓")
        print("\n  Your DSP Toolbox is ready for the exam! 📡")
    else:
        print(f"\n  ✗ {total_tests - total_passed} test(s) failed")
    
    print("=" * 60 + "\n")
    
    return total_passed == total_tests


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
