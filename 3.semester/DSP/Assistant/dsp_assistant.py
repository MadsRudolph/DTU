#!/usr/bin/env python3
"""
DSP Assistant - Interactive Digital Signal Processing Problem Solver
=====================================================================

Version 3.1 - DUAL OUTPUT: Python + MATLAB Code Generation (FIXED)

Enhanced with:
- Python calculations & visualization (dsp_calc + dsp_viz)
- MATLAB code snippets for exam Live Scripts
- Explanation templates for each problem type

Run from terminal:
    python dsp_assistant.py

Topics covered:
  1. Step → Impulse Conversion
  2. System Function H(z)
  3. Pole-Zero Analysis
  4. Inverse System
  5. Cascade Decomposition
  6. Linear Phase Check (Symmetry Trick)
  7. Frequency Response
  8. Pre-warping (BLT)
  9. Butterworth Order
  10. FIR Ideal Impulse Response
  11. Windowing
  12. Sampling & Aliasing
  13. Min-Phase / All-Pass Decomposition
  
  === VISUALIZATION ===
  14. Plot Spectrum
  15. Plot Pole-Zero Diagram
  16. Plot Frequency Response
  17. Plot Linear Phase Analysis
  18. Plot Z-Surface (3D)
  19. Aliasing Visualization
"""

import sys
import os
import numpy as np

# Import DSP tools
try:
    from dsp_calc import *
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from dsp_calc import *

# Import visualization tools
VIZ_AVAILABLE = False
try:
    from dsp_viz import *
    VIZ_AVAILABLE = True
except ImportError:
    print("  Note: dsp_viz.py not found. Visualization disabled.")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_welcome():
    """Print welcome banner"""
    print()
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║                                                          ║")
    print("  ║         📡 DSP TOOLBOX ASSISTANT 📡                      ║")
    print("  ║                                                          ║")
    print("  ║     DTU 62743 Digital Signal Processing                  ║")
    print("  ║        Python Edition v3.1 (MATLAB Gen)                  ║")
    if VIZ_AVAILABLE:
        print("  ║          ✓ Visualization Enabled                         ║")
    print("  ║          ✓ MATLAB Code Generation                        ║")
    print("  ║                                                          ║")
    print("  ╚══════════════════════════════════════════════════════════╝")
    print()


def print_menu():
    """Print main menu"""
    print()
    print("  ┌────────────────────────────────────────────┐")
    print("  │         WHAT DO YOU NEED HELP WITH?        │")
    print("  ├────────────────────────────────────────────┤")
    print("  │  ─── LTI SYSTEM ANALYSIS ───               │")
    print("  │  1. Step → Impulse Conversion              │")
    print("  │  2. System Function H(z)                   │")
    print("  │  3. Pole-Zero Analysis (Stability)         │")
    print("  │  4. Inverse System                         │")
    print("  │  5. Cascade Decomposition                  │")
    print("  │                                            │")
    print("  │  ─── FREQUENCY RESPONSE ───                │")
    print("  │  6. Linear Phase Check (Symmetry)          │")
    print("  │  7. Frequency Response H(e^jω)             │")
    print("  │                                            │")
    print("  │  ─── IIR FILTER DESIGN ───                 │")
    print("  │  8. Pre-warping (BLT)                      │")
    print("  │  9. Butterworth Order Calculation          │")
    print("  │                                            │")
    print("  │  ─── FIR FILTER DESIGN ───                 │")
    print("  │  10. Ideal Impulse Response                │")
    print("  │  11. Windowing (Hamming, etc.)             │")
    print("  │                                            │")
    print("  │  ─── SAMPLING ───                          │")
    print("  │  12. Sampling & Aliasing Analysis          │")
    print("  │                                            │")
    print("  │  ─── ADVANCED ───                          │")
    print("  │  13. Min-Phase / All-Pass Decomposition    │")
    if VIZ_AVAILABLE:
        print("  │                                            │")
        print("  │  ─── VISUALIZATION 📊 ───                  │")
        print("  │  14. Plot Spectrum                         │")
        print("  │  15. Plot Pole-Zero Diagram                │")
        print("  │  16. Plot Frequency Response               │")
        print("  │  17. Plot Linear Phase Analysis            │")
        print("  │  18. Plot Z-Surface (3D)                   │")
        print("  │  19. Aliasing Visualization                │")
    print("  │                                            │")
    print("  │  0. Exit                                   │")
    print("  └────────────────────────────────────────────┘")
    print()


def get_number(prompt, allow_complex=False):
    """Get a number from user input"""
    while True:
        try:
            raw = input(prompt).strip()
            if not raw:
                return 0
            if allow_complex and 'j' in raw:
                return complex(raw.replace('i', 'j'))
            return float(raw)
        except ValueError:
            print("  Invalid input. Please enter a number.")


def get_array(prompt):
    """Get an array of numbers from user input"""
    print(f"{prompt}")
    print("  (Enter space-separated values, e.g., '1 2 3 4')")
    raw = input("  > ").strip()
    if not raw:
        return np.array([])
    try:
        values = [float(x) for x in raw.split()]
        return np.array(values)
    except ValueError:
        print("  Invalid input.")
        return np.array([])


def get_yes_no(prompt):
    """Get yes/no response"""
    response = input(prompt).strip().lower()
    return response in ['y', 'yes', '1', 'true']


def format_complex(z):
    """Format complex number for display"""
    if np.abs(np.imag(z)) < 1e-10:
        return f"{np.real(z):.4g}"
    elif np.abs(np.real(z)) < 1e-10:
        return f"{np.imag(z):.4g}j"
    else:
        sign = '+' if np.imag(z) >= 0 else ''
        return f"{np.real(z):.4g}{sign}{np.imag(z):.4g}j"


def to_matlab_array(arr):
    """Convert Python array to MATLAB array string"""
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    if isinstance(arr, list):
        # Format each element
        formatted = []
        for x in arr:
            if isinstance(x, complex):
                if np.imag(x) >= 0:
                    formatted.append(f"{np.real(x):.6g}+{np.imag(x):.6g}j")
                else:
                    formatted.append(f"{np.real(x):.6g}{np.imag(x):.6g}j")
            else:
                formatted.append(f"{x:.6g}")
        return "[" + " ".join(formatted) + "]"
    return str(arr)


def to_matlab_int_array(arr):
    """Convert Python array to MATLAB integer array string"""
    if isinstance(arr, np.ndarray):
        arr = arr.tolist()
    return "[" + " ".join(str(int(x)) if float(x).is_integer() else f"{x:.4g}" for x in arr) + "]"


# =============================================================================
# MATLAB CODE GENERATION HELPER
# =============================================================================

def print_exam_block(matlab_code, explanation):
    """Print formatted MATLAB code block and explanation for exam"""
    print("\n" + "═"*65)
    print(" 📋 MATLAB SNIPPET (Copy to Live Script)")
    print("═"*65)
    print(matlab_code.strip())
    print("═"*65)
    print(" 📝 EXPLANATION TEMPLATE")
    print("═"*65)
    print(explanation.strip())
    print("═"*65 + "\n")


# =============================================================================
# HANDLER FUNCTIONS WITH MATLAB CODE GENERATION
# =============================================================================

def handle_step_to_impulse():
    """Handle Step to Impulse conversion"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       STEP → IMPULSE CONVERSION")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Method: h[n] = y_step[n] - y_step[n-1]")
    print("  Reference: [E23 Q1]")
    print()
    
    y_step = get_array("  Enter step response values y_step[n]:")
    
    if len(y_step) == 0:
        print("  No input provided.")
        return
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = StepToImpulse(y_step)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Step-by-step calculation:")
    for n in range(len(result.h)):
        y_prev = 0 if n == 0 else result.y_step[n-1]
        print(f"    h[{n}] = y_step[{n}] - y_step[{n-1}] = {result.y_step[n]:.4g} - {y_prev:.4g} = {result.h[n]:.4g}")
    print()
    print(f"  h[n] = {[round(x, 4) for x in result.h]}")
    
    # Visualization
    if VIZ_AVAILABLE:
        print()
        if get_yes_no("  Plot impulse response? (y/n): "):
            plot_impulse_response(result.h, title='Impulse Response h[n]')
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    y_step_matlab = to_matlab_int_array(y_step)
    h_matlab = to_matlab_int_array(result.h)
    
    matlab_code = f"""
%% Step to Impulse Response Conversion
% Method: h[n] = y_step[n] - y_step[n-1]

y_step = {y_step_matlab};
n = 0:length(y_step)-1;

% Compute impulse response using first difference
h = [y_step(1), diff(y_step)];

% Display result
disp('Impulse response h[n]:');
disp(h);

% Plot
figure;
stem(n, h, 'filled', 'LineWidth', 1.5);
xlabel('n'); ylabel('h[n]');
title('Impulse Response h[n]');
grid on;

% Verify: h = {h_matlab}
"""
    
    explanation = f"""
The impulse response is found using the first-difference method:
    h[n] = y_step[n] - y_step[n-1]

This works because δ[n] = u[n] - u[n-1], so by LTI properties:
    h[n] * δ[n] = h[n] * (u[n] - u[n-1])
    h[n] = y_step[n] - y_step[n-1]

Given y_step = {y_step_matlab}
Result: h[n] = {h_matlab}

The filter has {len(result.h)} taps (order M = {len(result.h)-1}).
"""
    
    print_exam_block(matlab_code, explanation)


def handle_system_function():
    """Handle System Function H(z)"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       SYSTEM FUNCTION H(z)")
    print("  ═══════════════════════════════════════════")
    print()
    print("  For FIR: H(z) = B[0] + B[1]z^{-1} + B[2]z^{-2} + ...")
    print("  For IIR: H(z) = B(z) / A(z)")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    print()
    if get_yes_no("  Is this an IIR filter (has denominator)? (y/n): "):
        A = get_array("  Enter denominator coefficients A:")
    else:
        A = None
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = SystemFunction(B, A)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print(f"  Type: {'FIR' if result.is_FIR else 'IIR'}")
    print(f"  Order: {result.order}")
    print()
    print(f"  H(z) = {result.H_str}")
    print()
    print(f"  Zeros: {[format_complex(z) for z in result.zeros]}")
    print(f"  Poles: {[format_complex(p) for p in result.poles]}")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    B_matlab = to_matlab_array(B)
    A_matlab = to_matlab_array(A) if A is not None else "[1]"
    
    matlab_code = f"""
%% System Function H(z)
B = {B_matlab};  % Numerator coefficients
A = {A_matlab};  % Denominator coefficients

% Find zeros and poles
z = roots(B);
p = roots(A);

disp('Zeros:'); disp(z);
disp('Poles:'); disp(p);

% Pole-Zero Plot
figure;
zplane(B, A);
title('Pole-Zero Plot');

% Frequency Response
figure;
freqz(B, A, 1024);
title('Frequency Response');

% Optional: Interactive zpgui
% zpgui(p, z);  % Uncomment if zpgui is available
"""
    
    filter_type = 'FIR' if result.is_FIR else 'IIR'
    zeros_str = ", ".join([format_complex(z) for z in result.zeros])
    poles_str = ", ".join([format_complex(p) for p in result.poles]) if len(result.poles) > 0 else "None (at origin)"
    
    explanation = f"""
System Function Analysis:
    H(z) = B(z) / A(z)
    
Filter Type: {filter_type}
Order: {result.order}

Zeros (roots of B(z)): {zeros_str}
Poles (roots of A(z)): {poles_str}

For FIR filters: All poles are at z=0 (trivial)
For IIR filters: Stability requires all |poles| < 1
"""
    
    print_exam_block(matlab_code, explanation)


def handle_pole_zero():
    """Handle Pole-Zero Analysis"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       POLE-ZERO ANALYSIS")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Stability: All poles must be inside unit circle")
    print("  Minimum-phase: All zeros must be inside unit circle")
    print("  Reference: [F21 Q1, E24 Q1]")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    print()
    if get_yes_no("  Has denominator (IIR)? (y/n): "):
        A = get_array("  Enter denominator coefficients A:")
    else:
        A = None
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = PoleZeroAnalysis(B, A)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print("  ZEROS:")
    for i, z in enumerate(result.zeros):
        loc = "INSIDE" if abs(z) < 0.999 else "ON" if abs(abs(z)-1) < 0.01 else "OUTSIDE"
        print(f"    z_{i+1} = {format_complex(z)}, |z| = {abs(z):.4f} → {loc} UC")
    print(f"    Inside UC: {result.zeros_inside_UC}, Outside UC: {result.zeros_outside_UC}")
    print()
    print("  POLES:")
    for i, p in enumerate(result.poles):
        loc = "INSIDE" if abs(p) < 0.999 else "ON" if abs(abs(p)-1) < 0.01 else "OUTSIDE"
        print(f"    p_{i+1} = {format_complex(p)}, |p| = {abs(p):.4f} → {loc} UC")
    print(f"    Inside UC: {result.poles_inside_UC}, Outside UC: {result.poles_outside_UC}")
    print()
    print(f"  STABLE: {'✓ YES' if result.is_stable else '✗ NO'}")
    print(f"  Reason: {result.stability_reason}")
    print()
    print(f"  MINIMUM-PHASE: {'✓ YES' if result.is_minimum_phase else '✗ NO'}")
    
    # Visualization
    if VIZ_AVAILABLE:
        print()
        if get_yes_no("  Plot pole-zero diagram? (y/n): "):
            plot_pz(B=B, A=A if A is not None else [1], title='Pole-Zero Analysis')
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    B_matlab = to_matlab_array(B)
    A_matlab = to_matlab_array(A) if A is not None else "[1]"
    
    matlab_code = f"""
%% Pole-Zero Analysis
B = {B_matlab};  % Numerator
A = {A_matlab};  % Denominator

% Find zeros and poles
z = roots(B);
p = roots(A);

% Display with magnitudes
disp('=== ZEROS ===');
for k = 1:length(z)
    fprintf('z_%d = %.4f + %.4fj, |z| = %.4f\\n', k, real(z(k)), imag(z(k)), abs(z(k)));
end

disp('=== POLES ===');
for k = 1:length(p)
    fprintf('p_%d = %.4f + %.4fj, |p| = %.4f\\n', k, real(p(k)), imag(p(k)), abs(p(k)));
end

% Check stability
if all(abs(p) < 1)
    disp('STABLE: All poles inside unit circle');
else
    disp('UNSTABLE: Pole(s) outside unit circle!');
end

% Check minimum-phase
if all(abs(z) < 1)
    disp('MINIMUM-PHASE: All zeros inside unit circle');
else
    disp('NOT MINIMUM-PHASE: Zero(s) outside unit circle');
end

% Pole-Zero Plot
figure;
zplane(B, A);
title('Pole-Zero Plot');
% zpgui(p, z);  % Uncomment for interactive GUI
"""
    
    stable_str = "STABLE" if result.is_stable else "UNSTABLE"
    minphase_str = "MINIMUM-PHASE" if result.is_minimum_phase else "NOT MINIMUM-PHASE"
    
    explanation = f"""
Pole-Zero Analysis Results:

ZEROS: {result.zeros_inside_UC} inside UC, {result.zeros_outside_UC} outside UC
POLES: {result.poles_inside_UC} inside UC, {result.poles_outside_UC} outside UC

Stability: {stable_str}
    → {result.stability_reason}
    
Minimum-Phase: {minphase_str}
    → A system is minimum-phase iff ALL zeros are inside UC

Key Rules:
• BIBO Stability: All poles must satisfy |p| < 1
• Minimum-phase: All zeros must satisfy |z| < 1
• FIR filters are always stable (no feedback)
"""
    
    print_exam_block(matlab_code, explanation)


def handle_inverse_system():
    """Handle Inverse System analysis"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       INVERSE SYSTEM H_inv(z) = 1/H(z)")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Key insight:")
    print("    Poles of H_inv = Zeros of H")
    print("    Zeros of H_inv = Poles of H")
    print()
    print("  Reference: [F21 Q1, E20 Q3]")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    print()
    if get_yes_no("  Has denominator (IIR)? (y/n): "):
        A = get_array("  Enter denominator coefficients A:")
    else:
        A = None
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = InverseSystem(B, A)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Original zeros (become poles of H_inv):")
    for i, z in enumerate(result.original_zeros):
        loc = "INSIDE" if abs(z) < 0.999 else "ON" if abs(abs(z)-1) < 0.01 else "OUTSIDE"
        print(f"    z_{i+1} = {format_complex(z)}, |z| = {abs(z):.4f} → {loc} UC")
    print()
    print(f"  Zeros outside UC: {result.zeros_outside_UC}")
    print()
    print("  ─────────────────────────────────────────")
    print(f"  Can H_inv be STABLE?      {'✓ YES' if result.can_be_stable else '✗ NO'}")
    print(f"  Can H_inv be CAUSAL?      {'✓ YES' if result.can_be_causal else '✗ NO'}")
    print(f"  Can H_inv be BOTH?        {'✓ YES' if result.can_be_both else '✗ NO'}")
    print("  ─────────────────────────────────────────")
    print()
    print(f"  Explanation: {result.reason}")  # FIXED: was .explanation
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    B_matlab = to_matlab_array(B)
    A_matlab = to_matlab_array(A) if A is not None else "[1]"
    
    matlab_code = f"""
%% Inverse System Analysis: H_inv(z) = 1/H(z)
B = {B_matlab};  % Original numerator → becomes denominator of H_inv
A = {A_matlab};  % Original denominator → becomes numerator of H_inv

% Original zeros become poles of inverse
original_zeros = roots(B);
disp('Original zeros (become poles of H_inv):');
for k = 1:length(original_zeros)
    z = original_zeros(k);
    fprintf('z_%d = %.4f + %.4fj, |z| = %.4f\\n', k, real(z), imag(z), abs(z));
end

% Check if inverse can be stable AND causal
zeros_outside = sum(abs(original_zeros) > 1);
zeros_on_UC = sum(abs(abs(original_zeros) - 1) < 0.01);

if zeros_outside > 0 || zeros_on_UC > 0
    disp('H_inv CANNOT be both stable AND causal!');
    disp('Reason: Zero(s) on or outside UC become unstable poles.');
else
    disp('H_inv CAN be stable and causal.');
end

% The inverse system
B_inv = A;  % Swap numerator and denominator
A_inv = B;
disp('H_inv: B_inv = A, A_inv = B');
"""
    
    can_both = "YES" if result.can_be_both else "NO"
    
    explanation = f"""
Inverse System Analysis:
    H_inv(z) = 1/H(z) = A(z)/B(z)
    
Key Principle:
    • Zeros of H(z) become POLES of H_inv(z)
    • Poles of H(z) become ZEROS of H_inv(z)

Original zeros: {[format_complex(z) for z in result.original_zeros]}
Zeros outside UC: {result.zeros_outside_UC}

Can H_inv be stable + causal? {can_both}

Rule: If ANY zero of H(z) is outside or ON the unit circle,
      then H_inv(z) CANNOT be both stable AND causal.
      
      • Stable requires poles inside UC
      • Causal requires ROC to extend to infinity
      • These conflict when zeros are outside UC
"""
    
    print_exam_block(matlab_code, explanation)


def handle_cascade():
    """Handle Cascade Decomposition"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       CASCADE DECOMPOSITION")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Given H(z) = H1(z) · H2(z), find H2(z)")
    print("  Method: H2 = deconv(H, H1)")
    print("  Reference: [E23 Q1]")
    print()
    
    H_total = get_array("  Enter H_total coefficients:")
    
    if len(H_total) == 0:
        print("  No input provided.")
        return
    
    H1 = get_array("  Enter H1 coefficients:")
    
    if len(H1) == 0:
        print("  No input provided.")
        return
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = CascadeDecomposition(H_total, H1)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    if result.is_exact:  # FIXED: was .valid
        print(f"  H2 coefficients: {[round(x, 6) for x in result.H2]}")
        print()
        # Calculate verification
        verification = np.convolve(result.H1, result.H2)
        print("  Verification: H1 * H2 =", [round(x, 6) for x in verification])
        print(f"  Match: {'✓ YES' if result.is_exact else '✗ NO'}")
    else:
        print("  ✗ Decomposition failed!")
        print(f"  Remainder: {[round(x, 6) for x in result.remainder]}")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    H_total_matlab = to_matlab_array(H_total)
    H1_matlab = to_matlab_array(H1)
    H2_matlab = to_matlab_array(result.H2) if result.is_exact else "[]"
    
    matlab_code = f"""
%% Cascade Decomposition: H(z) = H1(z) · H2(z)
% Find H2 given H_total and H1

H_total = {H_total_matlab};
H1 = {H1_matlab};

% Deconvolution to find H2
[H2, remainder] = deconv(H_total, H1);

disp('H2 coefficients:');
disp(H2);

% Verify: H1 * H2 should equal H_total
verification = conv(H1, H2);
disp('Verification (H1 * H2):');
disp(verification);

% Check if decomposition is exact
if max(abs(remainder)) < 1e-10
    disp('✓ Exact decomposition');
else
    disp('✗ Non-exact decomposition (has remainder)');
    disp('Remainder:'); disp(remainder);
end

% Result: H2 = {H2_matlab}
"""
    
    explanation = f"""
Cascade Decomposition:
    H_total(z) = H1(z) · H2(z)
    
To find H2(z):
    H2(z) = H_total(z) / H1(z)
    
In MATLAB: [H2, r] = deconv(H_total, H1)

Given:
    H_total = {H_total_matlab}
    H1 = {H1_matlab}

Result:
    H2 = {H2_matlab}
    
Verification: conv(H1, H2) should equal H_total
"""
    
    print_exam_block(matlab_code, explanation)


def handle_linear_phase():
    """Handle Linear Phase Check"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       LINEAR PHASE CHECK (SYMMETRY TRICK)")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Method: Factor out e^{-jωK}, use Euler's identity")
    print("  ⚠️ TRAP: A(ω) can go NEGATIVE!")
    print("  Reference: [E23 Q1-3]")
    print()
    
    h = get_array("  Enter impulse response h[n]:")
    
    if len(h) == 0:
        print("  No input provided.")
        return
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = LinearPhaseCheck(h)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print(f"  Symmetric: {'✓ YES' if result.is_symmetric else '✗ NO'}")
    print(f"  Filter Type: {result.filter_type}")
    print(f"  Center K = {result.center_K}")  # FIXED: was .K
    print()
    print(f"  A(ω) formula: {result.A_omega_formula}")  # FIXED: was .A_omega_str
    print()
    print("  Key values:")
    print(f"    A(0) = {result.A_at_0:.4g}")
    print(f"    A(π/2) = {result.A_at_pi_2:.4g}")  # FIXED: was .A_at_pi2
    print(f"    A(π) = {result.A_at_pi:.4g}")
    print()
    
    if result.is_positive:
        print("  ✓ A(ω) ≥ 0 for all ω")
        print(f"  Phase: ∠H(ω) = -{result.center_K}ω")  # FIXED: was .K
    else:
        print("  ⚠️ WARNING: A(ω) goes NEGATIVE!")
        print(f"  {result.positivity_warning}")
        print("  Phase has π-jumps where A(ω) crosses zero!")
    
    # Visualization
    if VIZ_AVAILABLE:
        print()
        if get_yes_no("  Plot linear phase analysis? (y/n): "):
            plot_linear_phase_analysis(h)
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    h_matlab = to_matlab_array(h)
    N = len(h)
    K = result.center_K  # FIXED: was (N - 1) / 2
    
    matlab_code = f"""
%% Linear Phase Analysis (Symmetry Trick)
h = {h_matlab};
N = length(h);
K = (N-1)/2;  % Group delay

% Check symmetry: h[n] = h[N-1-n]?
h_flipped = fliplr(h);
is_symmetric = all(abs(h - h_flipped) < 1e-10);

if is_symmetric
    disp('✓ Symmetric (Type I or II linear phase)');
else
    disp('✗ Not symmetric');
end

% Calculate A(ω) for Type I (odd N, symmetric)
omega = linspace(-pi, pi, 1000);
A_omega = zeros(size(omega));

if mod(N, 2) == 1 && is_symmetric
    % Type I: A(ω) = h(K+1) + 2*sum(h(K+1-m)*cos(m*ω))
    K_idx = (N+1)/2;  % MATLAB 1-indexed center
    A_omega = h(K_idx) * ones(size(omega));
    for m = 1:K
        A_omega = A_omega + 2*h(K_idx-m)*cos(m*omega);
    end
end

% Check if A(ω) goes negative!
A_min = min(A_omega);
fprintf('A(ω) minimum: %.4f\\n', A_min);

if A_min < 0
    disp('⚠️ WARNING: A(ω) < 0 at some frequencies!');
    disp('   Phase has π-jumps. Cannot write ∠H = -Kω directly.');
else
    disp('✓ A(ω) ≥ 0 everywhere');
    fprintf('   Phase: ∠H(ω) = -%.1f·ω\\n', K);
end

% Plot A(ω)
figure;
subplot(2,1,1);
stem(0:N-1, h, 'filled'); xlabel('n'); ylabel('h[n]');
title('Impulse Response');

subplot(2,1,2);
plot(omega/pi, A_omega, 'b', 'LineWidth', 1.5);
hold on;
plot(omega/pi, zeros(size(omega)), 'r--');
xlabel('ω/π'); ylabel('A(ω)');
title('Amplitude Function A(ω) - Check for Negativity!');
grid on;
"""
    
    sym_status = "SYMMETRIC" if result.is_symmetric else "NOT SYMMETRIC"
    pos_status = "A(ω) ≥ 0 everywhere" if result.is_positive else "⚠️ A(ω) < 0 at some ω!"
    
    explanation = f"""
Linear Phase FIR Analysis:

Impulse Response: h[n] = {[round(x,4) for x in h]}
Length N = {N}, Center K = {K}

Symmetry Check: {sym_status}
    h[n] = h[N-1-n] for all n?

For Type I (odd N, symmetric):
    H(e^jω) = e^(-jKω) · A(ω)
    where A(ω) = h[K] + 2·Σ h[K-m]·cos(mω)

A(ω) Positivity: {pos_status}

Key Values:
    A(0) = {result.A_at_0:.4g} (sum of all h[n])
    A(π/2) = {result.A_at_pi_2:.4g}
    A(π) = {result.A_at_pi:.4g} (alternating sum)

⚠️ EXAM TRAP: If A(ω) < 0, you CANNOT write:
    |H(ω)| = A(ω) and ∠H(ω) = -Kω
    
Instead: |H(ω)| = |A(ω)| and phase has π-jumps!
"""
    
    print_exam_block(matlab_code, explanation)


def handle_frequency_response():
    """Handle Frequency Response calculation"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       FREQUENCY RESPONSE H(e^jω)")
    print("  ═══════════════════════════════════════════")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    print()
    if get_yes_no("  Has denominator (IIR)? (y/n): "):
        A = get_array("  Enter denominator coefficients A:")
    else:
        A = None
    
    omega_eval = get_number("  Evaluate at ω (in radians, e.g., 0, 1.57, 3.14): ")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation - Calculate H at single omega
    # ═══════════════════════════════════════════════════════════════
    B_arr = np.array(B, dtype=complex)
    A_arr = np.array(A, dtype=complex) if A is not None else np.array([1.0])
    
    # Calculate H(e^jω) at a single point
    z = np.exp(1j * omega_eval)
    num = sum(B_arr[k] * z**(-k) for k in range(len(B_arr)))
    den = sum(A_arr[k] * z**(-k) for k in range(len(A_arr)))
    H_val = num / den if abs(den) > 1e-12 else np.inf
    
    magnitude = np.abs(H_val)
    magnitude_dB = 20 * np.log10(magnitude + 1e-12)
    phase = np.angle(H_val)
    phase_deg = np.degrees(phase)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print(f"  At ω = {omega_eval:.4g} rad:")
    print(f"    H(e^jω) = {format_complex(H_val)}")
    print(f"    |H(e^jω)| = {magnitude:.4g}")
    print(f"    |H(e^jω)| in dB = {magnitude_dB:.2f} dB")
    print(f"    ∠H(e^jω) = {phase:.4g} rad = {phase_deg:.2f}°")
    
    # Visualization
    if VIZ_AVAILABLE:
        print()
        if get_yes_no("  Plot full frequency response? (y/n): "):
            plot_frequency_response(B, A if A is not None else [1])
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    B_matlab = to_matlab_array(B)
    A_matlab = to_matlab_array(A) if A is not None else "[1]"
    
    matlab_code = f"""
%% Frequency Response H(e^jω)
B = {B_matlab};
A = {A_matlab};

% Evaluate at specific ω
omega_eval = {omega_eval:.6g};  % rad

% Manual calculation using z^-n form
H_val = sum(B .* exp(-1j*omega_eval*(0:length(B)-1))) / ...
        sum(A .* exp(-1j*omega_eval*(0:length(A)-1)));

fprintf('At ω = %.4f rad:\\n', omega_eval);
fprintf('  H(e^jω) = %.4f + %.4fj\\n', real(H_val), imag(H_val));
fprintf('  |H| = %.4f\\n', abs(H_val));
fprintf('  |H| in dB = %.2f dB\\n', 20*log10(abs(H_val)));
fprintf('  ∠H = %.4f rad = %.2f°\\n', angle(H_val), angle(H_val)*180/pi);

% Full frequency response plot
figure;
freqz(B, A, 1024);
sgtitle('Frequency Response');

% Alternative: Custom plot
figure;
[H, w] = freqz(B, A, 1024);
subplot(2,1,1);
plot(w/pi, 20*log10(abs(H)), 'b', 'LineWidth', 1.5);
xlabel('ω/π'); ylabel('|H| (dB)'); grid on;
title('Magnitude Response');

subplot(2,1,2);
plot(w/pi, unwrap(angle(H))*180/pi, 'r', 'LineWidth', 1.5);
xlabel('ω/π'); ylabel('∠H (degrees)'); grid on;
title('Phase Response');
"""
    
    explanation = f"""
Frequency Response at ω = {omega_eval:.4g} rad:

H(e^jω) = Σ b[k]·e^(-jωk) / Σ a[k]·e^(-jωk)

Results:
    H(e^jω) = {format_complex(H_val)}
    Magnitude: |H| = {magnitude:.4g}
    Magnitude (dB): {magnitude_dB:.2f} dB
    Phase: ∠H = {phase:.4g} rad = {phase_deg:.2f}°

Useful ω values:
    ω = 0: DC response
    ω = π/2: Quarter Nyquist
    ω = π: Nyquist (highest frequency)
"""
    
    print_exam_block(matlab_code, explanation)


def handle_prewarp():
    """Handle Pre-warping calculation"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       PRE-WARPING (BILINEAR TRANSFORM)")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Formula: Ω = (2/T) · tan(ω/2) = 2·Fs · tan(π·F/Fs)")
    print("  Reference: [E23 Q2, F21 Q2]")
    print()
    
    F = get_number("  Enter frequency F (Hz): ")
    Fs = get_number("  Enter sampling frequency Fs (Hz): ")
    
    if Fs <= 0:
        print("  Invalid sampling frequency.")
        return
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = Prewarp(F, Fs)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print(f"  Digital frequency:")
    print(f"    ω = 2π·F/Fs = 2π·{F}/{Fs} = {result.omega:.6f} rad/sample")
    print()
    print(f"  Pre-warped analog frequency:")
    print(f"    Ω = 2·Fs·tan(ω/2) = 2·{Fs}·tan({result.omega/2:.6f})")
    print(f"    Ω = {result.Omega:.4f} rad/s")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    matlab_code = f"""
%% Pre-warping for Bilinear Transform
F = {F};      % Digital frequency (Hz)
Fs = {Fs};    % Sampling frequency (Hz)
T = 1/Fs;     % Sampling period

% Digital angular frequency
omega = 2*pi*F/Fs;
fprintf('Digital: ω = %.6f rad/sample\\n', omega);

% Pre-warped analog frequency
Omega = 2*Fs*tan(omega/2);
% Alternative: Omega = (2/T)*tan(omega/2);
fprintf('Pre-warped: Ω = %.4f rad/s\\n', Omega);

% For filter design, use this Omega in analog prototype
% Then apply bilinear transform: s = (2/T)*(z-1)/(z+1)
"""
    
    explanation = f"""
Pre-warping for Bilinear Transform:

The bilinear transform causes frequency warping:
    ω = 2·arctan(Ω·T/2)
    
To compensate, we pre-warp the analog frequency:
    Ω = (2/T)·tan(ω/2) = 2·Fs·tan(π·F/Fs)

Given:
    F = {F} Hz (desired digital frequency)
    Fs = {Fs} Hz (sampling frequency)
    T = 1/Fs = {1/Fs:.6g} s

Results:
    ω = 2π·F/Fs = {result.omega:.6f} rad/sample
    Ω = {result.Omega:.4f} rad/s (use this for analog prototype)

This ensures the digital filter has the correct cutoff
at exactly F = {F} Hz after bilinear transformation.
"""
    
    print_exam_block(matlab_code, explanation)


def handle_butterworth_order():
    """Handle Butterworth Order calculation"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       BUTTERWORTH ORDER CALCULATION")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Reference: [E23 Q2, F21 Q2]")
    print()
    
    print("  Filter type:")
    print("    1. Lowpass")
    print("    2. Highpass")
    filter_type = int(get_number("  Select (1/2): "))
    
    if filter_type not in [1, 2]:
        print("  Invalid selection.")
        return
    
    is_highpass = (filter_type == 2)
    filter_type_str = 'highpass' if is_highpass else 'lowpass'
    
    print()
    Ap = get_number("  Passband ripple Ap (dB): ")
    As = get_number("  Stopband attenuation As (dB): ")
    Omega_p = get_number("  Pre-warped passband Ωp (rad/s): ")
    Omega_s = get_number("  Pre-warped stopband Ωs (rad/s): ")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = ButterworthOrder(Ap, As, Omega_p, Omega_s, filter_type_str)
    
    # Calculate ratio and Omega_c locally since result doesn't have them
    if is_highpass:
        ratio = Omega_s / Omega_p
    else:
        ratio = Omega_p / Omega_s
    
    # Calculate cutoff frequency
    epsilon = np.sqrt(10**(Ap/10) - 1)
    Omega_c = Omega_p / (epsilon ** (1/result.N))
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print(f"  Filter Type: {'Highpass' if is_highpass else 'Lowpass'}")
    print()
    print(f"  Selectivity ratio: {ratio:.4f}")
    print(f"  N (exact) = {result.N_exact:.4f}")
    print(f"  N (rounded up) = {result.N}")
    print()
    print(f"  Cutoff frequency Ωc = {Omega_c:.4f} rad/s")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    if is_highpass:
        ratio_formula = "Omega_s / Omega_p"
        ratio_comment = "% HP: ratio = Ωs/Ωp (inverted!)"
        hp_conversion = "% Convert to highpass\n[B_a, A_a] = lp2hp(B_a, A_a, Omega_c);"
    else:
        ratio_formula = "Omega_p / Omega_s"
        ratio_comment = "% LP: ratio = Ωp/Ωs"
        hp_conversion = ""
    
    matlab_code = f"""
%% Butterworth Filter Order Calculation
% Filter type: {'HIGHPASS' if is_highpass else 'LOWPASS'}

Ap = {Ap};           % Passband ripple (dB)
As = {As};           % Stopband attenuation (dB)
Omega_p = {Omega_p}; % Pre-warped passband (rad/s)
Omega_s = {Omega_s}; % Pre-warped stopband (rad/s)

% Convert to linear scale
epsilon = sqrt(10^(Ap/10) - 1);
A = 10^(As/20);

% Selectivity ratio
{ratio_comment}
ratio = {ratio_formula};

% Calculate order
N_exact = log10((A^2 - 1) / epsilon^2) / (2 * log10(1/ratio));
N = ceil(N_exact);
fprintf('Order: N = %.4f → round up to N = %d\\n', N_exact, N);

% Cutoff frequency (from passband spec)
Omega_c = Omega_p / (epsilon^(1/N));
fprintf('Cutoff frequency: Ωc = %.4f rad/s\\n', Omega_c);

% Alternative: Use MATLAB's buttord (requires normalized frequencies)
% [N, Wn] = buttord(Wp, Ws, Ap, As, 's');  % 's' for analog

% Design analog prototype
[z_a, p_a, k_a] = buttap(N);
[B_a, A_a] = zp2tf(z_a, p_a, k_a);

% Scale to cutoff frequency
[B_a, A_a] = lp2lp(B_a, A_a, Omega_c);
{hp_conversion}

disp('Analog prototype coefficients:');
disp('B_a:'); disp(B_a);
disp('A_a:'); disp(A_a);
"""
    
    explanation = f"""
Butterworth Order Calculation:

Filter Type: {'HIGHPASS' if is_highpass else 'LOWPASS'}
Specifications:
    Passband ripple: Ap = {Ap} dB
    Stopband attenuation: As = {As} dB
    Passband edge: Ωp = {Omega_p} rad/s
    Stopband edge: Ωs = {Omega_s} rad/s

{'⚠️ HIGHPASS: Use ratio = Ωs/Ωp (not Ωp/Ωs!)' if is_highpass else 'LOWPASS: Use ratio = Ωp/Ωs'}

Formula:
    N = log₁₀((A² - 1) / ε²) / (2·log₁₀(1/ratio))
    
where:
    ε = √(10^(Ap/10) - 1)
    A = 10^(As/20)

Results:
    Selectivity ratio = {ratio:.4f}
    N (exact) = {result.N_exact:.4f}
    N (rounded up) = {result.N}
    Cutoff Ωc = {Omega_c:.4f} rad/s
"""
    
    print_exam_block(matlab_code, explanation)


def handle_ideal_impulse():
    """Handle Ideal Impulse Response calculation"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       IDEAL FIR IMPULSE RESPONSE")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Reference: [E23 Q3, F24 Q3]")
    print()
    
    print("  Filter type:")
    print("    1. Lowpass")
    print("    2. Highpass")
    print("    3. Bandpass")
    print("    4. Bandstop")
    filter_type_num = int(get_number("  Select (1-4): "))
    
    filter_types = {1: 'lowpass', 2: 'highpass', 3: 'bandpass', 4: 'bandstop'}
    if filter_type_num not in filter_types:
        print("  Invalid selection.")
        return
    
    filter_type = filter_types[filter_type_num]
    
    print()
    N = int(get_number("  Filter length N: "))
    
    if filter_type in ['lowpass', 'highpass']:
        omega_c = get_number("  Cutoff frequency ωc (rad): ")
        omega_c2 = None
    else:
        omega_c = get_number("  Lower cutoff ωc1 (rad): ")
        omega_c2 = get_number("  Upper cutoff ωc2 (rad): ")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    if filter_type in ['bandpass', 'bandstop']:
        result = IdealImpulseResponse((omega_c, omega_c2), N, filter_type)
    else:
        result = IdealImpulseResponse(omega_c, N, filter_type)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print(f"  Filter Type: {filter_type.upper()}")
    print(f"  Length N = {N}")
    print(f"  Center K = {result.K}")
    print()
    print("  Ideal impulse response h_ideal[n]:")
    for i, val in enumerate(result.h_ideal):
        print(f"    h[{i}] = {val:.6f}")
    
    # Visualization
    if VIZ_AVAILABLE:
        print()
        if get_yes_no("  Plot impulse response? (y/n): "):
            plot_impulse_response(result.h_ideal, title=f'Ideal {filter_type.upper()} h[n]')
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    if filter_type == 'lowpass':
        formula_str = "h_ideal(n) = ωc/π · sinc(ωc(n-K)/π)"
        matlab_formula = """
% Lowpass: h[n] = (ωc/π) · sinc(ωc(n-K)/π)
for n = 0:N-1
    if n == K
        h_ideal(n+1) = omega_c / pi;
    else
        h_ideal(n+1) = sin(omega_c*(n-K)) / (pi*(n-K));
    end
end"""
    elif filter_type == 'highpass':
        formula_str = "h_ideal(n) = δ[n-K] - h_LP[n]"
        matlab_formula = """
% Highpass: h[n] = δ[n-K] - h_LP[n]
for n = 0:N-1
    if n == K
        h_ideal(n+1) = 1 - omega_c / pi;
    else
        h_ideal(n+1) = -sin(omega_c*(n-K)) / (pi*(n-K));
    end
end"""
    elif filter_type == 'bandpass':
        formula_str = "h_ideal(n) = h_LP2[n] - h_LP1[n]"
        matlab_formula = f"""
% Bandpass: h[n] = h_LP(ωc2)[n] - h_LP(ωc1)[n]
omega_c1 = {omega_c};
omega_c2 = {omega_c2};
for n = 0:N-1
    if n == K
        h_ideal(n+1) = (omega_c2 - omega_c1) / pi;
    else
        h_ideal(n+1) = (sin(omega_c2*(n-K)) - sin(omega_c1*(n-K))) / (pi*(n-K));
    end
end"""
    else:  # bandstop
        formula_str = "h_ideal(n) = δ[n-K] - h_BP[n]"
        matlab_formula = f"""
% Bandstop: h[n] = δ[n-K] - h_BP[n]
omega_c1 = {omega_c};
omega_c2 = {omega_c2};
for n = 0:N-1
    if n == K
        h_ideal(n+1) = 1 - (omega_c2 - omega_c1) / pi;
    else
        h_ideal(n+1) = (sin(omega_c1*(n-K)) - sin(omega_c2*(n-K))) / (pi*(n-K));
    end
end"""
    
    h_matlab = to_matlab_array(result.h_ideal)
    
    matlab_code = f"""
%% Ideal FIR Impulse Response - {filter_type.upper()}
N = {N};           % Filter length
K = (N-1)/2;       % Center index (group delay)
omega_c = {omega_c};  % Cutoff frequency (rad)

h_ideal = zeros(1, N);
{matlab_formula}

% Display
disp('Ideal impulse response:');
disp(h_ideal);

% Plot
figure;
stem(0:N-1, h_ideal, 'filled', 'LineWidth', 1.5);
xlabel('n'); ylabel('h_{{ideal}}[n]');
title('{filter_type.upper()} Ideal Impulse Response');
grid on;

% Verify with fir1 (if applicable)
% h_fir1 = fir1(N-1, omega_c/pi, '{filter_type}', rectwin(N), 'noscale');

% Result: h_ideal = {h_matlab}
"""
    
    explanation = f"""
Ideal {filter_type.upper()} FIR Impulse Response:

Length: N = {N}
Center: K = {result.K}
Cutoff: ωc = {omega_c} rad{f', ωc2 = {omega_c2} rad' if omega_c2 else ''}

Formula: {formula_str}

The ideal impulse response is based on the inverse DTFT
of the ideal frequency response (rectangular window in frequency).

For n = K (center):
    h_ideal[K] = ωc/π (for LP)
    
For n ≠ K:
    h_ideal[n] = sin(ωc(n-K)) / (π(n-K))

Note: This ideal response has infinite extent.
We truncate to N samples, which causes Gibbs phenomenon.
Apply a window (Hamming, etc.) to reduce ripple.
"""
    
    print_exam_block(matlab_code, explanation)


def handle_windowing():
    """Handle Windowing"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       WINDOWING")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Reference: [E23 Q3, F24 Q3]")
    print()
    
    h = get_array("  Enter ideal impulse response h_ideal[n]:")
    
    if len(h) == 0:
        print("  No input provided.")
        return
    
    print()
    print("  Window type:")
    print("    1. Hamming")
    print("    2. Hanning")
    print("    3. Blackman")
    print("    4. Rectangular")
    window_num = int(get_number("  Select (1-4): "))
    
    window_types = {1: 'hamming', 2: 'hanning', 3: 'blackman', 4: 'rectangular'}
    if window_num not in window_types:
        print("  Invalid selection.")
        return
    
    window_type = window_types[window_num]
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = WindowedFIR(h, window_type)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print(f"  Window: {window_type.upper()}")
    print()
    print("  Window coefficients:")
    for i, w in enumerate(result.window):
        print(f"    w[{i}] = {w:.6f}")
    print()
    print("  Windowed impulse response:")
    for i, val in enumerate(result.h_windowed):
        print(f"    h_w[{i}] = {val:.6f}")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    h_matlab = to_matlab_array(h)
    w_matlab = to_matlab_array(result.window)
    hw_matlab = to_matlab_array(result.h_windowed)
    N = len(h)
    
    window_func = {
        'hamming': 'hamming',
        'hanning': 'hann',
        'blackman': 'blackman',
        'rectangular': 'rectwin'
    }[window_type]
    
    matlab_code = f"""
%% Windowing for FIR Filter Design
h_ideal = {h_matlab};
N = length(h_ideal);

% Generate window
w = {window_func}(N)';  % Transpose to row vector

% Apply window
h_windowed = h_ideal .* w;

disp('Window coefficients:');
disp(w);
disp('Windowed impulse response:');
disp(h_windowed);

% Plot comparison
figure;
subplot(3,1,1);
stem(0:N-1, h_ideal, 'filled'); ylabel('h_{{ideal}}');
title('Ideal Impulse Response');

subplot(3,1,2);
stem(0:N-1, w, 'filled'); ylabel('w[n]');
title('{window_type.upper()} Window');

subplot(3,1,3);
stem(0:N-1, h_windowed, 'filled'); ylabel('h_w[n]');
title('Windowed Impulse Response');
xlabel('n');

% Frequency response comparison
figure;
[H_ideal, omega] = freqz(h_ideal, 1, 1024);
[H_windowed, ~] = freqz(h_windowed, 1, 1024);

plot(omega/pi, 20*log10(abs(H_ideal)), 'b--', 'LineWidth', 1);
hold on;
plot(omega/pi, 20*log10(abs(H_windowed)), 'r', 'LineWidth', 1.5);
xlabel('ω/π'); ylabel('|H| (dB)');
legend('Ideal (rectangular)', '{window_type.upper()}');
title('Effect of Windowing on Frequency Response');
grid on;

% Result: h_windowed = {hw_matlab}
"""
    
    explanation = f"""
Windowing for FIR Filter Design:

Window Type: {window_type.upper()}
Filter Length: N = {N}

Windowed response: h_w[n] = h_ideal[n] · w[n]

Window Comparison:
    Rectangular: Narrowest main lobe, highest sidelobes (-13 dB)
    Hamming: Good compromise, -43 dB sidelobes
    Hanning: Similar to Hamming, -32 dB sidelobes
    Blackman: Widest main lobe, lowest sidelobes (-58 dB)

{window_type.upper()} Window Formula:
"""
    
    if window_type == 'hamming':
        explanation += "    w[n] = 0.54 - 0.46·cos(2πn/(N-1))"
    elif window_type == 'hanning':
        explanation += "    w[n] = 0.5 - 0.5·cos(2πn/(N-1))"
    elif window_type == 'blackman':
        explanation += "    w[n] = 0.42 - 0.5·cos(2πn/(N-1)) + 0.08·cos(4πn/(N-1))"
    else:
        explanation += "    w[n] = 1 for all n"
    
    print_exam_block(matlab_code, explanation)


def handle_sampling():
    """Handle Sampling & Aliasing Analysis"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       SAMPLING & ALIASING ANALYSIS")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Nyquist: Fs > 2·F_max")
    print("  Reference: [E24 Q3, F23 Q3]")
    print()
    
    frequencies = get_array("  Enter signal frequencies (Hz):")
    
    if len(frequencies) == 0:
        print("  No input provided.")
        return
    
    Fs = get_number("  Sampling frequency Fs (Hz): ")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = SamplingAnalysis(list(frequencies), Fs)
    
    # Calculate values locally since result doesn't have them
    num_aliased = int(np.sum(result.aliased))  # FIXED
    F_nyquist_required = 2 * result.F_max_signal  # FIXED
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print(f"  Sampling frequency Fs = {Fs} Hz")
    print(f"  Nyquist frequency = {result.F_nyquist} Hz")
    print(f"  Required Fs (Nyquist) = {F_nyquist_required} Hz")
    print()
    print("  Component analysis:")
    for i, (f, aliased, f_app) in enumerate(zip(result.frequencies, result.aliased, result.apparent_frequencies)):
        status = "⚠️ ALIASED" if aliased else "✓ OK"
        if aliased:
            print(f"    {f} Hz → {f_app} Hz {status}")
        else:
            print(f"    {f} Hz {status}")
    print()
    print(f"  Total aliased components: {num_aliased} / {len(frequencies)}")
    
    # Visualization
    if VIZ_AVAILABLE:
        print()
        if get_yes_no("  Plot aliasing visualization? (y/n): "):
            spectrum_sampled(list(frequencies), Fs)
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    freqs_matlab = to_matlab_array(frequencies)
    apparent_matlab = to_matlab_array(result.apparent_frequencies)
    
    matlab_code = f"""
%% Sampling & Aliasing Analysis
freqs = {freqs_matlab};  % Signal frequencies (Hz)
Fs = {Fs};               % Sampling frequency (Hz)
F_nyquist = Fs / 2;      % Nyquist frequency

fprintf('Sampling frequency: Fs = %.0f Hz\\n', Fs);
fprintf('Nyquist frequency: Fs/2 = %.0f Hz\\n', F_nyquist);
fprintf('Required Fs (Nyquist): > %.0f Hz\\n', 2*max(freqs));
fprintf('\\n');

% Check each component
disp('Component Analysis:');
for k = 1:length(freqs)
    f = freqs(k);
    if f <= F_nyquist
        fprintf('  %.0f Hz → OK\\n', f);
    else
        % Aliasing: apparent frequency
        f_apparent = abs(Fs - f);
        if f_apparent > F_nyquist
            f_apparent = Fs - f_apparent;
        end
        fprintf('  %.0f Hz → %.0f Hz (ALIASED!)\\n', f, f_apparent);
    end
end

% Spectrum visualization (using custom plot_spectrum if available)
figure;
freqs_pos = freqs(freqs <= F_nyquist);
freqs_aliased = freqs(freqs > F_nyquist);
amps_pos = ones(size(freqs_pos));
amps_aliased = ones(size(freqs_aliased));

% Plot original
stem([freqs_pos, -freqs_pos], [amps_pos, amps_pos], 'b', 'filled');
hold on;
% Plot aliased (in red at apparent frequencies)
if ~isempty(freqs_aliased)
    f_app = abs(Fs - freqs_aliased);
    stem([f_app, -f_app], [amps_aliased, amps_aliased], 'r', 'filled');
end
xline(F_nyquist, 'r--', 'Nyquist');
xline(-F_nyquist, 'r--');
xlabel('Frequency (Hz)');
ylabel('Amplitude');
title('Sampled Signal Spectrum (Red = Aliased)');
grid on;

% Alternatively, use custom function:
% plot_spectrum([freqs, -freqs], ones(1,2*length(freqs)), 'XRange', [-Fs/2, Fs/2]);
"""
    
    aliased_list = [f"{f}→{fa}" for f, fa, a in 
                    zip(result.frequencies, result.apparent_frequencies, result.aliased) if a]
    
    explanation = f"""
Sampling & Aliasing Analysis:

Sampling Parameters:
    Fs = {Fs} Hz
    Nyquist = Fs/2 = {result.F_nyquist} Hz
    
Signal Components: {list(frequencies)} Hz

Aliasing Rule:
    If F > Fs/2, the signal aliases to F_apparent = |Fs - F|
    (Reflects around Nyquist frequency)

Results:
    Components > Nyquist: {num_aliased}
    Aliased frequencies: {aliased_list if aliased_list else 'None'}

Nyquist Theorem:
    To avoid aliasing: Fs > 2·F_max
    Required Fs > {F_nyquist_required} Hz
"""
    
    print_exam_block(matlab_code, explanation)


def handle_minphase():
    """Handle Min-Phase / All-Pass Decomposition"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       MIN-PHASE / ALL-PASS DECOMPOSITION")
    print("  ═══════════════════════════════════════════")
    print()
    print("  H(z) = H_min(z) · H_ap(z)")
    print("  Zeros outside UC → reflect to 1/z*")
    print("  Reference: [F24 Q3, E21 Q3]")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 1: Python Calculation
    # ═══════════════════════════════════════════════════════════════
    result = MinPhaseDecomposition(B)
    
    print()
    print("  ═══════════════════════════════════════════")
    print("       PYTHON RESULT")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Original zeros:")
    for i, z in enumerate(result.zeros_original):  # FIXED: was .zeros
        loc = "INSIDE" if abs(z) < 0.999 else "OUTSIDE"
        print(f"    z_{i+1} = {format_complex(z)}, |z| = {abs(z):.4f} → {loc} UC")
    print()
    
    # Get min-phase zeros from B_min
    zeros_min = np.roots(result.B_min) if len(result.B_min) > 1 else []
    
    print("  Decomposition:")
    print(f"    H_min zeros: {[format_complex(z) for z in zeros_min]}")
    print(f"    H_ap: {result.H_ap_str}")
    print()
    if len(result.zeros_outside_UC) > 0:  # This is now an array
        print("  Zeros reflected:")
        for z_out, z_in in zip(result.zeros_outside_UC, result.zeros_reflected):
            print(f"    {format_complex(z_out)} → {format_complex(z_in)}")
    
    # ═══════════════════════════════════════════════════════════════
    # PHASE 2: MATLAB Code Generation
    # ═══════════════════════════════════════════════════════════════
    B_matlab = to_matlab_array(B)
    
    matlab_code = f"""
%% Min-Phase / All-Pass Decomposition
% H(z) = H_min(z) · H_ap(z)

B = {B_matlab};
zeros_orig = roots(B);

disp('Original zeros:');
for k = 1:length(zeros_orig)
    z = zeros_orig(k);
    fprintf('z_%d = %.4f + %.4fj, |z| = %.4f\\n', k, real(z), imag(z), abs(z));
end

% Identify zeros outside UC
outside_UC = abs(zeros_orig) > 1;
zeros_outside = zeros_orig(outside_UC);
zeros_inside = zeros_orig(~outside_UC);

% Reflect zeros outside UC
zeros_reflected = 1 ./ conj(zeros_outside);

% Minimum-phase zeros = inside + reflected
zeros_min = [zeros_inside; zeros_reflected];

disp('');
disp('Min-phase zeros:');
disp(zeros_min);

% Build H_min(z) from zeros
B_min = poly(zeros_min);
B_min = B_min * (B(1) / B_min(1));  % Match gain

% Build H_ap(z) for each reflected zero
disp('');
disp('All-pass factors:');
for k = 1:length(zeros_outside)
    z0 = zeros_outside(k);
    fprintf('H_ap_%d(z) = (z^-1 - %.4f) / (1 - %.4f·z^-1)\\n', ...
            k, conj(z0), conj(z0));
end

% Verify: H = H_min * H_ap
% conv(B_min, B_ap) should give original B (up to scaling)
"""
    
    zeros_str = [format_complex(z) for z in result.zeros_original]
    zeros_min_str = [format_complex(z) for z in zeros_min]
    
    explanation = f"""
Min-Phase / All-Pass Decomposition:

Any rational system can be written as:
    H(z) = H_min(z) · H_ap(z)

where:
    H_min(z) = minimum-phase (all zeros inside UC)
    H_ap(z) = all-pass (|H_ap(e^jω)| = 1)

Original zeros: {zeros_str}
Zeros outside UC: {len(result.zeros_outside_UC)}

Reflection Rule:
    Zero at z₀ (|z₀| > 1) → reflect to 1/z₀*
    
Min-phase zeros: {zeros_min_str}

All-pass factor for each reflected zero:
    H_ap(z) = (z⁻¹ - z₀*) / (1 - z₀*·z⁻¹)

This preserves magnitude: |H(e^jω)| = |H_min(e^jω)|
"""
    
    print_exam_block(matlab_code, explanation)


# =============================================================================
# VISUALIZATION HANDLERS (Keep existing, add MATLAB suggestions)
# =============================================================================

def handle_viz_spectrum():
    """Handle Spectrum Plotting"""
    if not VIZ_AVAILABLE:
        print("  Visualization not available. Install matplotlib.")
        return
    
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       PLOT SPECTRUM")
    print("  ═══════════════════════════════════════════")
    print()
    
    frequencies = get_array("  Enter frequencies:")
    amplitudes = get_array("  Enter amplitudes:")
    
    if len(frequencies) == 0 or len(amplitudes) == 0:
        print("  No input provided.")
        return
    
    title = input("  Title (press Enter for default): ").strip()
    if not title:
        title = "Frequency Spectrum"
    
    plot_spectrum(list(frequencies), list(amplitudes), title=title)
    
    # MATLAB equivalent
    freqs_matlab = to_matlab_array(frequencies)
    amps_matlab = to_matlab_array(amplitudes)
    
    matlab_code = f"""
%% Spectrum Plot
freqs = {freqs_matlab};
amps = {amps_matlab};

% Using custom plot_spectrum (if available)
% plot_spectrum(freqs, amps, 'Title', '{title}');

% Standard MATLAB alternative
figure;
stem(freqs, amps, 'filled', 'LineWidth', 2);
xlabel('Frequency (Hz)');
ylabel('Amplitude');
title('{title}');
grid on;
"""
    
    print_exam_block(matlab_code, "Use plot_spectrum() for exam-style arrow plots.")


def handle_viz_pz():
    """Handle Pole-Zero Plotting"""
    if not VIZ_AVAILABLE:
        print("  Visualization not available. Install matplotlib.")
        return
    
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       PLOT POLE-ZERO DIAGRAM")
    print("  ═══════════════════════════════════════════")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    print()
    if get_yes_no("  Has denominator (IIR)? (y/n): "):
        A = get_array("  Enter denominator coefficients A:")
    else:
        A = [1]
    
    plot_pz(B=B, A=A, title='Pole-Zero Diagram')
    
    # MATLAB equivalent
    B_matlab = to_matlab_array(B)
    A_matlab = to_matlab_array(A)
    
    matlab_code = f"""
%% Pole-Zero Plot
B = {B_matlab};
A = {A_matlab};

figure;
zplane(B, A);
title('Pole-Zero Diagram');

% Interactive version (if zpgui available)
% zpgui(roots(A), roots(B));
"""
    
    print_exam_block(matlab_code, "Use zplane(B,A) or zpgui(poles, zeros) in MATLAB.")


def handle_viz_freqresp():
    """Handle Frequency Response Plotting"""
    if not VIZ_AVAILABLE:
        print("  Visualization not available. Install matplotlib.")
        return
    
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       PLOT FREQUENCY RESPONSE")
    print("  ═══════════════════════════════════════════")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    print()
    if get_yes_no("  Has denominator (IIR)? (y/n): "):
        A = get_array("  Enter denominator coefficients A:")
    else:
        A = [1]
    
    Fs = get_number("  Sampling frequency Fs (Hz, 0 for normalized): ")
    
    plot_frequency_response(B, A, Fs=Fs if Fs > 0 else None)
    
    # MATLAB equivalent
    B_matlab = to_matlab_array(B)
    A_matlab = to_matlab_array(A)
    
    matlab_code = f"""
%% Frequency Response
B = {B_matlab};
A = {A_matlab};

figure;
freqz(B, A, 1024);
sgtitle('Frequency Response');
"""
    
    print_exam_block(matlab_code, "Use freqz(B, A) in MATLAB for frequency response.")


def handle_viz_linear_phase():
    """Handle Linear Phase Analysis Plotting"""
    if not VIZ_AVAILABLE:
        print("  Visualization not available. Install matplotlib.")
        return
    
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       PLOT LINEAR PHASE ANALYSIS")
    print("  ═══════════════════════════════════════════")
    print()
    print("  ⚠️ This detects the A(ω) < 0 trap!")
    print()
    
    h = get_array("  Enter impulse response h[n]:")
    
    if len(h) == 0:
        print("  No input provided.")
        return
    
    plot_linear_phase_analysis(h)
    
    # MATLAB equivalent
    h_matlab = to_matlab_array(h)
    
    matlab_code = f"""
%% Linear Phase Analysis (A(ω) Check)
h = {h_matlab};
N = length(h);
K = (N-1)/2;

% Check symmetry
is_sym = all(abs(h - fliplr(h)) < 1e-10);

% Calculate A(ω) for Type I
omega = linspace(-pi, pi, 1000);
A = h((N+1)/2) * ones(size(omega));
for m = 1:K
    A = A + 2*h((N+1)/2-m)*cos(m*omega);
end

% Check negativity
A_min = min(A);
fprintf('A(ω) min = %.4f\\n', A_min);
if A_min < 0
    disp('⚠️ A(ω) goes negative!');
end

% Plot
figure;
subplot(2,1,1); stem(0:N-1, h, 'filled'); title('h[n]');
subplot(2,1,2); plot(omega/pi, A); hold on;
plot(omega/pi, zeros(size(omega)), 'r--');
title('A(\\omega) - Check for Negativity!');
xlabel('\\omega/\\pi');
"""
    
    print_exam_block(matlab_code, "Critical: Check if A(ω) goes negative!")


def handle_viz_zsurface():
    """Handle Z-Surface 3D Plotting"""
    if not VIZ_AVAILABLE:
        print("  Visualization not available. Install matplotlib.")
        return
    
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       PLOT Z-SURFACE (3D)")
    print("  ═══════════════════════════════════════════")
    print()
    
    B = get_array("  Enter numerator coefficients B:")
    
    if len(B) == 0:
        print("  No input provided.")
        return
    
    print()
    if get_yes_no("  Has denominator (IIR)? (y/n): "):
        A = get_array("  Enter denominator coefficients A:")
    else:
        A = [1]
    
    plot_z_surface(B, A)
    
    # MATLAB equivalent
    B_matlab = to_matlab_array(B)
    A_matlab = to_matlab_array(A)
    
    matlab_code = f"""
%% Z-Surface (3D |H(z)|)
B = {B_matlab};
A = {A_matlab};

% Using custom plot_z_surface (if available)
% plot_z_surface(gca, roots(A), roots(B));

% Or use zpgui for interactive exploration
% zpgui(roots(A), roots(B));
"""
    
    print_exam_block(matlab_code, "Use plot_z_surface() or zpgui() in MATLAB.")


def handle_viz_aliasing():
    """Handle Aliasing Visualization"""
    if not VIZ_AVAILABLE:
        print("  Visualization not available. Install matplotlib.")
        return
    
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       ALIASING VISUALIZATION")
    print("  ═══════════════════════════════════════════")
    print()
    
    frequencies = get_array("  Enter signal frequencies (Hz):")
    
    if len(frequencies) == 0:
        print("  No input provided.")
        return
    
    Fs = get_number("  Sampling frequency Fs (Hz): ")
    
    spectrum_sampled(list(frequencies), Fs)
    
    # MATLAB equivalent
    freqs_matlab = to_matlab_array(frequencies)
    
    matlab_code = f"""
%% Aliasing Visualization
freqs = {freqs_matlab};
Fs = {Fs};
F_nyq = Fs/2;

% Calculate apparent frequencies
f_apparent = freqs;
for k = 1:length(freqs)
    if freqs(k) > F_nyq
        f_apparent(k) = abs(Fs - freqs(k));
    end
end

% Plot with custom plot_spectrum (if available)
% spectrum_templates('aliased', freqs(1), Fs);

% Standard plot
figure;
stem(freqs, ones(size(freqs)), 'b', 'filled');
hold on;
aliased_idx = freqs > F_nyq;
if any(aliased_idx)
    stem(f_apparent(aliased_idx), ones(sum(aliased_idx),1), 'r', 'filled');
end
xline(F_nyq, 'r--', 'Nyquist');
xlabel('Frequency (Hz)');
legend('Original', 'Aliased');
title(sprintf('Aliasing (Fs = %.0f Hz)', Fs));
"""
    
    print_exam_block(matlab_code, "Shows original frequencies and where they alias to.")


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    """Main program loop"""
    clear_screen()
    print_welcome()
    
    while True:
        print_menu()
        
        try:
            max_choice = 19 if VIZ_AVAILABLE else 13
            choice = int(get_number(f"  Enter choice (0-{max_choice}): ", False))
        except:
            continue
        
        if choice == 0:
            print("\n  Good luck on your DSP exam! 📡🎓\n")
            break
        
        handlers = {
            1: handle_step_to_impulse,
            2: handle_system_function,
            3: handle_pole_zero,
            4: handle_inverse_system,
            5: handle_cascade,
            6: handle_linear_phase,
            7: handle_frequency_response,
            8: handle_prewarp,
            9: handle_butterworth_order,
            10: handle_ideal_impulse,
            11: handle_windowing,
            12: handle_sampling,
            13: handle_minphase,
        }
        
        if VIZ_AVAILABLE:
            handlers.update({
                14: handle_viz_spectrum,
                15: handle_viz_pz,
                16: handle_viz_freqresp,
                17: handle_viz_linear_phase,
                18: handle_viz_zsurface,
                19: handle_viz_aliasing,
            })
        
        if choice in handlers:
            try:
                handlers[choice]()
            except Exception as e:
                print(f"\n  ⚠ Error: {e}")
                import traceback
                traceback.print_exc()
        
        input("\n  Press Enter to continue...")
        clear_screen()
        print_welcome()


if __name__ == "__main__":
    main()
