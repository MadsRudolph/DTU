"""
DSP Tools - Digital Signal Processing Calculation Library
==========================================================

Python equivalent of the MATLAB DSP Toolbox for DTU 62743.
All functions work with NumPy arrays and complex numbers.

Usage:
    from dsp_calc import *
    
    # LTI System Analysis
    result = StepToImpulse([2, 3, -3, -2])
    result = SystemFunction([2, 1, -6, 1, 2])
    result = PoleZeroAnalysis(B, A)
    result = InverseSystem(B, A)
    
    # Frequency Response
    result = FrequencyResponse(B, A, N=512)
    result = LinearPhaseCheck(h)
    
    # Filter Design - IIR
    result = Prewarp(Fp, Fs)
    result = ButterworthOrder(Ap, As, Omega_p, Omega_s, filter_type='highpass')
    result = BilinearTransform(B_analog, A_analog, Fs)
    
    # Filter Design - FIR
    result = IdealImpulseResponse(omega_c, N, filter_type='lowpass')
    result = WindowedFIR(h_ideal, window='hamming')
    
    # Sampling & Aliasing
    result = SamplingAnalysis(frequencies, Fs)
    result = NyquistCheck(f_max, Fs)
    
    # Min-Phase / All-Pass
    result = MinPhaseDecomposition(B, A)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
import cmath

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================
PI = np.pi


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def to_dB(x):
    """Convert magnitude to dB"""
    return 20 * np.log10(np.abs(x) + 1e-12)


def from_dB(x_dB):
    """Convert dB to magnitude"""
    return 10 ** (x_dB / 20)


def normalize_angle(angle):
    """Normalize angle to [-π, π]"""
    return np.angle(np.exp(1j * angle))


# =============================================================================
# STEP TO IMPULSE - The "First Difference" Method
# =============================================================================
@dataclass
class StepToImpulseResult:
    """Results from Step to Impulse conversion"""
    y_step: np.ndarray = field(default_factory=lambda: np.array([]))
    h: np.ndarray = field(default_factory=lambda: np.array([]))
    n: np.ndarray = field(default_factory=lambda: np.array([]))
    method: str = "h[n] = y_step[n] - y_step[n-1]"


def StepToImpulse(y_step: Union[List, np.ndarray]) -> StepToImpulseResult:
    """
    Convert step response to impulse response using the first difference method.
    
    The fundamental LTI relationship:
        δ[n] = u[n] - u[n-1]
        Therefore: h[n] = y_step[n] - y_step[n-1]
    
    Parameters:
        y_step: Step response values starting from n=0
        
    Returns:
        StepToImpulseResult with h[n], n indices, and method description
        
    Reference: [E23 Q1, F24 Q1]
    """
    y_step = np.array(y_step, dtype=float)
    n = np.arange(len(y_step))
    
    # Compute first difference: h[n] = y_step[n] - y_step[n-1]
    y_step_shifted = np.concatenate([[0], y_step[:-1]])
    h = y_step - y_step_shifted
    
    return StepToImpulseResult(
        y_step=y_step,
        h=h,
        n=n,
        method="h[n] = y_step[n] - y_step[n-1]"
    )


# =============================================================================
# SYSTEM FUNCTION - FIR coefficients to H(z)
# =============================================================================
@dataclass
class SystemFunctionResult:
    """Results from System Function analysis"""
    B: np.ndarray = field(default_factory=lambda: np.array([]))
    A: np.ndarray = field(default_factory=lambda: np.array([1]))
    is_FIR: bool = True
    order: int = 0
    zeros: np.ndarray = field(default_factory=lambda: np.array([]))
    poles: np.ndarray = field(default_factory=lambda: np.array([]))
    H_str: str = ""


def SystemFunction(h_or_B: Union[List, np.ndarray], 
                   A: Union[List, np.ndarray] = None) -> SystemFunctionResult:
    """
    Create system function H(z) from coefficients.
    
    For FIR: H(z) = B[0] + B[1]z^{-1} + B[2]z^{-2} + ...
    For IIR: H(z) = (B[0] + B[1]z^{-1} + ...) / (A[0] + A[1]z^{-1} + ...)
    
    Parameters:
        h_or_B: Numerator coefficients (or impulse response for FIR)
        A: Denominator coefficients (default [1] for FIR)
        
    Returns:
        SystemFunctionResult with zeros, poles, and string representation
    """
    B = np.array(h_or_B, dtype=complex)
    
    if A is None:
        A = np.array([1.0])
    else:
        A = np.array(A, dtype=complex)
    
    is_FIR = len(A) == 1 and A[0] == 1
    
    # Find zeros and poles
    zeros = np.roots(B) if len(B) > 1 else np.array([])
    poles = np.roots(A) if len(A) > 1 else np.array([])
    
    order = max(len(B), len(A)) - 1
    
    # Build string representation
    terms = []
    for i, b in enumerate(B):
        if abs(b) > 1e-10:
            if i == 0:
                terms.append(f"{b:.4g}")
            else:
                sign = "+" if b.real >= 0 else ""
                terms.append(f"{sign}{b:.4g}z^{{-{i}}}")
    H_str = " ".join(terms) if terms else "0"
    
    if not is_FIR:
        denom_terms = []
        for i, a in enumerate(A):
            if abs(a) > 1e-10:
                if i == 0:
                    denom_terms.append(f"{a:.4g}")
                else:
                    sign = "+" if a.real >= 0 else ""
                    denom_terms.append(f"{sign}{a:.4g}z^{{-{i}}}")
        H_str = f"({H_str}) / ({' '.join(denom_terms)})"
    
    return SystemFunctionResult(
        B=B, A=A, is_FIR=is_FIR, order=order,
        zeros=zeros, poles=poles, H_str=H_str
    )


# =============================================================================
# POLE-ZERO ANALYSIS
# =============================================================================
@dataclass
class PoleZeroResult:
    """Results from Pole-Zero analysis"""
    zeros: np.ndarray = field(default_factory=lambda: np.array([]))
    poles: np.ndarray = field(default_factory=lambda: np.array([]))
    zeros_mag: np.ndarray = field(default_factory=lambda: np.array([]))
    poles_mag: np.ndarray = field(default_factory=lambda: np.array([]))
    is_stable: bool = False
    is_causal: bool = True
    is_minimum_phase: bool = False
    stability_reason: str = ""
    zeros_inside_UC: int = 0
    zeros_outside_UC: int = 0
    poles_inside_UC: int = 0
    poles_outside_UC: int = 0


def PoleZeroAnalysis(B: Union[List, np.ndarray], 
                     A: Union[List, np.ndarray] = None) -> PoleZeroResult:
    """
    Analyze poles and zeros for stability, causality, and minimum-phase.
    
    Stability: All poles inside unit circle (|p| < 1)
    Causality: ROC is exterior of a circle (assumed for right-sided signals)
    Minimum-phase: All zeros inside unit circle (|z| < 1)
    
    Parameters:
        B: Numerator coefficients
        A: Denominator coefficients (default [1] for FIR)
        
    Returns:
        PoleZeroResult with stability analysis
        
    Reference: [F21 Q1, E24 Q1]
    """
    B = np.array(B, dtype=complex)
    A = np.array(A, dtype=complex) if A is not None else np.array([1.0])
    
    zeros = np.roots(B) if len(B) > 1 else np.array([])
    poles = np.roots(A) if len(A) > 1 else np.array([])
    
    zeros_mag = np.abs(zeros) if len(zeros) > 0 else np.array([])
    poles_mag = np.abs(poles) if len(poles) > 0 else np.array([])
    
    # Count inside/outside unit circle
    zeros_inside = np.sum(zeros_mag < 1 - 1e-10) if len(zeros_mag) > 0 else 0
    zeros_outside = np.sum(zeros_mag > 1 + 1e-10) if len(zeros_mag) > 0 else 0
    zeros_on = len(zeros_mag) - zeros_inside - zeros_outside
    
    poles_inside = np.sum(poles_mag < 1 - 1e-10) if len(poles_mag) > 0 else 0
    poles_outside = np.sum(poles_mag > 1 + 1e-10) if len(poles_mag) > 0 else 0
    poles_on = len(poles_mag) - poles_inside - poles_outside
    
    # Stability check
    if len(poles) == 0:
        is_stable = True
        stability_reason = "FIR filter (no poles) → Always stable"
    elif poles_outside > 0:
        is_stable = False
        stability_reason = f"{poles_outside} pole(s) outside UC → Unstable"
    elif poles_on > 0:
        is_stable = False
        stability_reason = f"{poles_on} pole(s) ON UC → Marginally unstable"
    else:
        is_stable = True
        stability_reason = "All poles inside UC → Stable"
    
    # Minimum-phase check
    is_minimum_phase = (zeros_outside == 0 and zeros_on == 0)
    
    return PoleZeroResult(
        zeros=zeros, poles=poles,
        zeros_mag=zeros_mag, poles_mag=poles_mag,
        is_stable=is_stable, is_causal=True,
        is_minimum_phase=is_minimum_phase,
        stability_reason=stability_reason,
        zeros_inside_UC=int(zeros_inside),
        zeros_outside_UC=int(zeros_outside),
        poles_inside_UC=int(poles_inside),
        poles_outside_UC=int(poles_outside)
    )


# =============================================================================
# INVERSE SYSTEM ANALYSIS
# =============================================================================
@dataclass
class InverseSystemResult:
    """Results from Inverse System analysis"""
    B_inv: np.ndarray = field(default_factory=lambda: np.array([]))
    A_inv: np.ndarray = field(default_factory=lambda: np.array([]))
    can_be_stable: bool = False
    can_be_causal: bool = False
    can_be_both: bool = False
    reason: str = ""
    original_zeros: np.ndarray = field(default_factory=lambda: np.array([]))
    zeros_outside_UC: int = 0


def InverseSystem(B: Union[List, np.ndarray], 
                  A: Union[List, np.ndarray] = None) -> InverseSystemResult:
    """
    Analyze the inverse system H_inv(z) = 1/H(z) = A(z)/B(z).
    
    For the inverse system:
        - Poles of H_inv = Zeros of H
        - Zeros of H_inv = Poles of H
    
    The inverse can be stable AND causal only if ALL zeros of H(z)
    are inside the unit circle.
    
    Parameters:
        B: Numerator of original system
        A: Denominator of original system
        
    Returns:
        InverseSystemResult with stability analysis
        
    Reference: [F21 Q1, E20 Q3]
    """
    B = np.array(B, dtype=complex)
    A = np.array(A, dtype=complex) if A is not None else np.array([1.0])
    
    # Inverse: swap B and A
    B_inv = A.copy()
    A_inv = B.copy()
    
    # Zeros of original become poles of inverse
    original_zeros = np.roots(B) if len(B) > 1 else np.array([])
    zeros_mag = np.abs(original_zeros) if len(original_zeros) > 0 else np.array([])
    
    zeros_outside = np.sum(zeros_mag > 1 + 1e-10) if len(zeros_mag) > 0 else 0
    zeros_on = np.sum(np.abs(zeros_mag - 1) < 1e-10) if len(zeros_mag) > 0 else 0
    
    if zeros_outside > 0:
        can_be_stable = True  # With non-causal ROC
        can_be_causal = True  # With unstable ROC
        can_be_both = False
        reason = f"{zeros_outside} zero(s) outside UC → H_inv CANNOT be both causal AND stable"
    elif zeros_on > 0:
        can_be_stable = False
        can_be_causal = True
        can_be_both = False
        reason = f"{zeros_on} zero(s) ON UC → H_inv has poles on UC (marginally unstable)"
    else:
        can_be_stable = True
        can_be_causal = True
        can_be_both = True
        reason = "All zeros inside UC → H_inv CAN be both causal AND stable"
    
    return InverseSystemResult(
        B_inv=B_inv, A_inv=A_inv,
        can_be_stable=can_be_stable,
        can_be_causal=can_be_causal,
        can_be_both=can_be_both,
        reason=reason,
        original_zeros=original_zeros,
        zeros_outside_UC=int(zeros_outside)
    )


# =============================================================================
# CASCADE DECOMPOSITION
# =============================================================================
@dataclass
class CascadeResult:
    """Results from Cascade decomposition"""
    H_total: np.ndarray = field(default_factory=lambda: np.array([]))
    H1: np.ndarray = field(default_factory=lambda: np.array([]))
    H2: np.ndarray = field(default_factory=lambda: np.array([]))
    remainder: np.ndarray = field(default_factory=lambda: np.array([]))
    is_exact: bool = False


def CascadeDecomposition(H_total: Union[List, np.ndarray],
                          H1: Union[List, np.ndarray]) -> CascadeResult:
    """
    Find H2(z) given H(z) = H1(z) · H2(z).
    
    Uses polynomial division (deconvolution):
        H2(z) = H(z) / H1(z)
    
    Parameters:
        H_total: Total system coefficients
        H1: Known subsystem coefficients
        
    Returns:
        CascadeResult with H2 coefficients
        
    Reference: [E23 Q1]
    """
    H_total = np.array(H_total, dtype=complex)
    H1 = np.array(H1, dtype=complex)
    
    # Polynomial division
    H2, remainder = np.polydiv(H_total, H1)
    
    # Clean up small numerical errors
    H2 = np.real_if_close(H2)
    remainder = np.real_if_close(remainder)
    
    is_exact = np.allclose(remainder, 0, atol=1e-10)
    
    return CascadeResult(
        H_total=H_total,
        H1=H1,
        H2=H2,
        remainder=remainder,
        is_exact=is_exact
    )


# =============================================================================
# LINEAR PHASE CHECK (Symmetry Analysis)
# =============================================================================
@dataclass
class LinearPhaseResult:
    """Results from Linear Phase analysis"""
    h: np.ndarray = field(default_factory=lambda: np.array([]))
    is_symmetric: bool = False
    is_antisymmetric: bool = False
    filter_type: int = 0  # 1, 2, 3, or 4
    filter_type_name: str = ""
    center_K: float = 0.0
    A_omega_formula: str = ""
    phase_formula: str = ""
    A_at_0: float = 0.0
    A_at_pi_2: float = 0.0
    A_at_pi: float = 0.0
    A_min: float = 0.0
    is_positive: bool = False
    positivity_warning: str = ""


def LinearPhaseCheck(h: Union[List, np.ndarray]) -> LinearPhaseResult:
    """
    Check if FIR filter has linear phase using the symmetry trick.
    
    For symmetric h[n] = h[N-1-n]:
        H(ω) = e^{-jωK} · A(ω)
        where A(ω) is real-valued
    
    CRITICAL: Must verify A(ω) ≥ 0 for all ω before claiming
    pure linear phase ∠H(ω) = -Kω. If A(ω) < 0, there are π-jumps!
    
    Parameters:
        h: Impulse response coefficients
        
    Returns:
        LinearPhaseResult with symmetry analysis and positivity check
        
    Reference: [E23 Q1-3]
    """
    h = np.array(h, dtype=float)
    N = len(h)
    K = (N - 1) / 2
    
    # Check symmetry
    h_flipped = h[::-1]
    is_symmetric = np.allclose(h, h_flipped, atol=1e-10)
    is_antisymmetric = np.allclose(h, -h_flipped, atol=1e-10)
    
    # Determine filter type
    if N % 2 == 1:  # Odd length
        if is_symmetric:
            filter_type = 1
            filter_type_name = "Type I (Odd length, Symmetric)"
        elif is_antisymmetric:
            filter_type = 3
            filter_type_name = "Type III (Odd length, Antisymmetric)"
        else:
            filter_type = 0
            filter_type_name = "Not linear phase"
    else:  # Even length
        if is_symmetric:
            filter_type = 2
            filter_type_name = "Type II (Even length, Symmetric)"
        elif is_antisymmetric:
            filter_type = 4
            filter_type_name = "Type IV (Even length, Antisymmetric)"
        else:
            filter_type = 0
            filter_type_name = "Not linear phase"
    
    # Build A(ω) formula for Type I (most common)
    A_omega_formula = ""
    phase_formula = ""
    A_at_0 = 0.0
    A_at_pi_2 = 0.0
    A_at_pi = 0.0
    A_min = 0.0
    is_positive = False
    positivity_warning = ""
    
    if filter_type == 1:
        # Type I: A(ω) = h[K] + 2·Σ h[K-m]·cos(mω) for m=1 to K
        K_int = int(K)
        terms = [f"h[{K_int}]"]
        for m in range(1, K_int + 1):
            terms.append(f"2·h[{K_int - m}]·cos({m}ω)")
        A_omega_formula = " + ".join(terms)
        phase_formula = f"-{K}ω"
        
        # Calculate A(ω) at key points
        omega_test = np.linspace(-np.pi, np.pi, 4001)
        A_values = np.zeros_like(omega_test)
        A_values += h[K_int]
        for m in range(1, K_int + 1):
            A_values += 2 * h[K_int - m] * np.cos(m * omega_test)
        
        A_at_0 = h[K_int] + 2 * sum(h[K_int - m] for m in range(1, K_int + 1))
        A_at_pi_2 = h[K_int] + 2 * sum(h[K_int - m] * np.cos(m * np.pi/2) for m in range(1, K_int + 1))
        A_at_pi = h[K_int] + 2 * sum(h[K_int - m] * np.cos(m * np.pi) for m in range(1, K_int + 1))
        A_min = np.min(A_values)
        
        is_positive = A_min >= -1e-10
        
        if not is_positive:
            positivity_warning = f"⚠️ A(ω) goes NEGATIVE (min = {A_min:.4f})!\n" \
                                f"   Phase is NOT purely linear.\n" \
                                f"   |H(ω)| = |A(ω)|, phase has π-jumps at zero-crossings."
    
    return LinearPhaseResult(
        h=h,
        is_symmetric=is_symmetric,
        is_antisymmetric=is_antisymmetric,
        filter_type=filter_type,
        filter_type_name=filter_type_name,
        center_K=K,
        A_omega_formula=A_omega_formula,
        phase_formula=phase_formula,
        A_at_0=A_at_0,
        A_at_pi_2=A_at_pi_2,
        A_at_pi=A_at_pi,
        A_min=A_min,
        is_positive=is_positive,
        positivity_warning=positivity_warning
    )


# =============================================================================
# FREQUENCY RESPONSE
# =============================================================================
@dataclass
class FrequencyResponseResult:
    """Results from Frequency Response calculation"""
    omega: np.ndarray = field(default_factory=lambda: np.array([]))
    H: np.ndarray = field(default_factory=lambda: np.array([]))
    magnitude: np.ndarray = field(default_factory=lambda: np.array([]))
    magnitude_dB: np.ndarray = field(default_factory=lambda: np.array([]))
    phase: np.ndarray = field(default_factory=lambda: np.array([]))
    phase_unwrapped: np.ndarray = field(default_factory=lambda: np.array([]))
    group_delay: np.ndarray = field(default_factory=lambda: np.array([]))


def FrequencyResponse(B: Union[List, np.ndarray],
                      A: Union[List, np.ndarray] = None,
                      N: int = 512) -> FrequencyResponseResult:
    """
    Calculate frequency response H(e^{jω}).
    
    Parameters:
        B: Numerator coefficients
        A: Denominator coefficients (default [1])
        N: Number of frequency points
        
    Returns:
        FrequencyResponseResult with magnitude, phase, group delay
    """
    B = np.array(B, dtype=complex)
    A = np.array(A, dtype=complex) if A is not None else np.array([1.0])
    
    omega = np.linspace(-np.pi, np.pi, N)
    
    # Calculate H(e^{jω})
    H = np.zeros(N, dtype=complex)
    for i, w in enumerate(omega):
        z = np.exp(1j * w)
        num = sum(B[k] * z**(-k) for k in range(len(B)))
        den = sum(A[k] * z**(-k) for k in range(len(A)))
        H[i] = num / den if abs(den) > 1e-12 else np.inf
    
    magnitude = np.abs(H)
    magnitude_dB = 20 * np.log10(magnitude + 1e-12)
    phase = np.angle(H)
    phase_unwrapped = np.unwrap(phase)
    
    # Group delay = -d(phase)/dω
    group_delay = -np.gradient(phase_unwrapped, omega)
    
    return FrequencyResponseResult(
        omega=omega, H=H,
        magnitude=magnitude, magnitude_dB=magnitude_dB,
        phase=phase, phase_unwrapped=phase_unwrapped,
        group_delay=group_delay
    )


# =============================================================================
# PRE-WARPING (BLT)
# =============================================================================
@dataclass
class PrewarpResult:
    """Results from frequency pre-warping"""
    F: float = 0.0           # Original frequency [Hz]
    Fs: float = 0.0          # Sampling frequency [Hz]
    omega: float = 0.0       # Digital frequency [rad/sample]
    Omega: float = 0.0       # Pre-warped analog frequency [rad/s]
    formula: str = "Ω = 2·Fs·tan(π·F/Fs)"


def Prewarp(F: float, Fs: float) -> PrewarpResult:
    """
    Pre-warp a frequency for Bilinear Transform.
    
    The BLT causes frequency warping. To compensate:
        Ω = (2/T)·tan(ω/2) = 2·Fs·tan(π·F/Fs)
    
    NEVER use Hz frequencies directly in analog prototype formulas!
    
    Parameters:
        F: Digital frequency [Hz]
        Fs: Sampling frequency [Hz]
        
    Returns:
        PrewarpResult with pre-warped analog frequency
        
    Reference: [E23 Q2, F21 Q2]
    """
    omega = 2 * np.pi * F / Fs  # Digital frequency
    Omega = 2 * Fs * np.tan(np.pi * F / Fs)  # Pre-warped analog
    
    return PrewarpResult(
        F=F, Fs=Fs, omega=omega, Omega=Omega,
        formula="Ω = 2·Fs·tan(π·F/Fs)"
    )


# =============================================================================
# BUTTERWORTH ORDER CALCULATION
# =============================================================================
@dataclass
class ButterworthOrderResult:
    """Results from Butterworth order calculation"""
    Omega_p: float = 0.0
    Omega_s: float = 0.0
    Ap_dB: float = 0.0
    As_dB: float = 0.0
    filter_type: str = ""
    N_exact: float = 0.0
    N: int = 0
    formula_used: str = ""


def ButterworthOrder(Ap_dB: float, As_dB: float,
                     Omega_p: float, Omega_s: float,
                     filter_type: str = 'lowpass') -> ButterworthOrderResult:
    """
    Calculate minimum Butterworth filter order.
    
    Formula:
        N ≥ log10[(10^(As/10)-1)/(10^(Ap/10)-1)] / [2·log10(Ωs/Ωp)]
    
    For HIGHPASS: Use Ωp/Ωs instead (because Ωp > Ωs)
    
    Parameters:
        Ap_dB: Passband ripple [dB]
        As_dB: Stopband attenuation [dB]
        Omega_p: Passband edge [rad/s]
        Omega_s: Stopband edge [rad/s]
        filter_type: 'lowpass' or 'highpass'
        
    Returns:
        ButterworthOrderResult with order calculation
        
    Reference: [E23 Q2, F21 Q2]
    """
    numerator = np.log10((10**(As_dB/10) - 1) / (10**(Ap_dB/10) - 1))
    
    if filter_type.lower() == 'highpass':
        # For HP: Ωp > Ωs, so use Ωp/Ωs
        denominator = 2 * np.log10(Omega_p / Omega_s)
        formula = "N ≥ log₁₀[(10^(As/10)-1)/(10^(Ap/10)-1)] / [2·log₁₀(Ωp/Ωs)]"
    else:
        # For LP: Ωs > Ωp, so use Ωs/Ωp
        denominator = 2 * np.log10(Omega_s / Omega_p)
        formula = "N ≥ log₁₀[(10^(As/10)-1)/(10^(Ap/10)-1)] / [2·log₁₀(Ωs/Ωp)]"
    
    N_exact = numerator / denominator
    N = int(np.ceil(N_exact))
    
    return ButterworthOrderResult(
        Omega_p=Omega_p, Omega_s=Omega_s,
        Ap_dB=Ap_dB, As_dB=As_dB,
        filter_type=filter_type,
        N_exact=N_exact, N=N,
        formula_used=formula
    )


# =============================================================================
# BILINEAR TRANSFORM
# =============================================================================
@dataclass
class BilinearResult:
    """Results from Bilinear Transform"""
    B_analog: np.ndarray = field(default_factory=lambda: np.array([]))
    A_analog: np.ndarray = field(default_factory=lambda: np.array([]))
    B_digital: np.ndarray = field(default_factory=lambda: np.array([]))
    A_digital: np.ndarray = field(default_factory=lambda: np.array([]))
    Fs: float = 0.0
    formula: str = "s = (2/T)·(z-1)/(z+1)"


def BilinearTransform(B_analog: Union[List, np.ndarray],
                      A_analog: Union[List, np.ndarray],
                      Fs: float) -> BilinearResult:
    """
    Apply Bilinear Transform to convert analog filter to digital.
    
    Substitution: s = (2/T)·(z-1)/(z+1) where T = 1/Fs
    
    Parameters:
        B_analog: Analog numerator coefficients (highest power first)
        A_analog: Analog denominator coefficients (highest power first)
        Fs: Sampling frequency [Hz]
        
    Returns:
        BilinearResult with digital filter coefficients
        
    Note: For full implementation, use scipy.signal.bilinear
    """
    # This is a simplified version - for exam use scipy.signal.bilinear
    try:
        from scipy.signal import bilinear
        B_digital, A_digital = bilinear(B_analog, A_analog, Fs)
    except ImportError:
        # Fallback: just return the analog coefficients with a warning
        B_digital = np.array(B_analog)
        A_digital = np.array(A_analog)
        print("Warning: scipy not available, returning analog coefficients")
    
    return BilinearResult(
        B_analog=np.array(B_analog),
        A_analog=np.array(A_analog),
        B_digital=B_digital,
        A_digital=A_digital,
        Fs=Fs,
        formula="s = (2/T)·(z-1)/(z+1)"
    )


# =============================================================================
# IDEAL IMPULSE RESPONSE (FIR Design)
# =============================================================================
@dataclass
class IdealImpulseResult:
    """Results from ideal impulse response calculation"""
    h_ideal: np.ndarray = field(default_factory=lambda: np.array([]))
    n: np.ndarray = field(default_factory=lambda: np.array([]))
    omega_c1: float = 0.0
    omega_c2: float = 0.0
    filter_type: str = ""
    formula: str = ""
    K: float = 0.0
    N: int = 0


def IdealImpulseResponse(omega_c: Union[float, Tuple[float, float]],
                         N: int,
                         filter_type: str = 'lowpass') -> IdealImpulseResult:
    """
    Calculate ideal (infinite-length) impulse response for FIR design.
    
    Types:
        lowpass:  h[n] = sin(ωc·n)/(π·n), h[0] = ωc/π
        highpass: h[n] = δ[n] - h_LP[n]
        bandpass: h[n] = (sin(ωc2·n) - sin(ωc1·n))/(π·n)
        bandstop: h[n] = δ[n] - h_BP[n]
    
    Parameters:
        omega_c: Cutoff frequency(ies) [rad/sample]
                 Single value for LP/HP, tuple (ωc1, ωc2) for BP/BS
        N: Filter length (should be odd for Type I)
        filter_type: 'lowpass', 'highpass', 'bandpass', 'bandstop'
        
    Returns:
        IdealImpulseResult with ideal coefficients
        
    Reference: [E23 Q4, E24 Q4]
    """
    K = (N - 1) / 2
    n = np.arange(N) - K  # Centered indices: -K to +K
    
    h_ideal = np.zeros(N)
    formula = ""
    omega_c1 = 0.0
    omega_c2 = 0.0
    
    if filter_type.lower() == 'lowpass':
        omega_c1 = omega_c if isinstance(omega_c, (int, float)) else omega_c[0]
        formula = "h[n] = sin(ωc·n)/(π·n), h[0] = ωc/π"
        
        for i, n_val in enumerate(n):
            if n_val == 0:
                h_ideal[i] = omega_c1 / np.pi
            else:
                h_ideal[i] = np.sin(omega_c1 * n_val) / (np.pi * n_val)
                
    elif filter_type.lower() == 'highpass':
        omega_c1 = omega_c if isinstance(omega_c, (int, float)) else omega_c[0]
        formula = "h_HP[n] = δ[n] - h_LP[n]"
        
        h_lp = np.zeros(N)
        for i, n_val in enumerate(n):
            if n_val == 0:
                h_lp[i] = omega_c1 / np.pi
            else:
                h_lp[i] = np.sin(omega_c1 * n_val) / (np.pi * n_val)
        
        # HP = delta - LP
        delta = np.zeros(N)
        delta[int(K)] = 1.0
        h_ideal = delta - h_lp
        
    elif filter_type.lower() == 'bandpass':
        omega_c1, omega_c2 = omega_c
        formula = "h_BP[n] = (sin(ωc2·n) - sin(ωc1·n))/(π·n)"
        
        for i, n_val in enumerate(n):
            if n_val == 0:
                h_ideal[i] = (omega_c2 - omega_c1) / np.pi
            else:
                h_ideal[i] = (np.sin(omega_c2 * n_val) - np.sin(omega_c1 * n_val)) / (np.pi * n_val)
                
    elif filter_type.lower() == 'bandstop':
        omega_c1, omega_c2 = omega_c
        formula = "h_BS[n] = δ[n] - h_BP[n]"
        
        h_bp = np.zeros(N)
        for i, n_val in enumerate(n):
            if n_val == 0:
                h_bp[i] = (omega_c2 - omega_c1) / np.pi
            else:
                h_bp[i] = (np.sin(omega_c2 * n_val) - np.sin(omega_c1 * n_val)) / (np.pi * n_val)
        
        # BS = delta - BP
        delta = np.zeros(N)
        delta[int(K)] = 1.0
        h_ideal = delta - h_bp
    
    return IdealImpulseResult(
        h_ideal=h_ideal,
        n=n,
        omega_c1=omega_c1,
        omega_c2=omega_c2,
        filter_type=filter_type,
        formula=formula,
        K=K,
        N=N
    )


# =============================================================================
# WINDOW FUNCTIONS
# =============================================================================
@dataclass
class WindowResult:
    """Results from windowing operation"""
    h_ideal: np.ndarray = field(default_factory=lambda: np.array([]))
    window: np.ndarray = field(default_factory=lambda: np.array([]))
    h_windowed: np.ndarray = field(default_factory=lambda: np.array([]))
    window_type: str = ""
    window_formula: str = ""
    approx_stopband_dB: float = 0.0


def WindowedFIR(h_ideal: Union[List, np.ndarray],
                window_type: str = 'hamming') -> WindowResult:
    """
    Apply window to ideal impulse response.
    
    Common windows:
        rectangular: w[n] = 1                    (~21 dB stopband)
        hamming:     w[n] = 0.54 - 0.46·cos(2πn/(N-1))  (~53 dB)
        hanning:     w[n] = 0.5 - 0.5·cos(2πn/(N-1))    (~44 dB)
        blackman:    w[n] = 0.42 - 0.5·cos(...) + 0.08·cos(...)  (~74 dB)
    
    Parameters:
        h_ideal: Ideal impulse response
        window_type: 'rectangular', 'hamming', 'hanning', 'blackman'
        
    Returns:
        WindowResult with windowed coefficients
        
    Reference: [E23 Q4, E24 Q4]
    """
    h_ideal = np.array(h_ideal)
    N = len(h_ideal)
    n = np.arange(N)
    
    window_type = window_type.lower()
    
    if window_type == 'rectangular':
        window = np.ones(N)
        formula = "w[n] = 1"
        stopband = 21
    elif window_type == 'hamming':
        window = 0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1))
        formula = "w[n] = 0.54 - 0.46·cos(2πn/(N-1))"
        stopband = 53
    elif window_type in ['hanning', 'hann']:
        window = 0.5 - 0.5 * np.cos(2 * np.pi * n / (N - 1))
        formula = "w[n] = 0.5 - 0.5·cos(2πn/(N-1))"
        stopband = 44
    elif window_type == 'blackman':
        window = (0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) 
                  + 0.08 * np.cos(4 * np.pi * n / (N - 1)))
        formula = "w[n] = 0.42 - 0.5·cos(2πn/(N-1)) + 0.08·cos(4πn/(N-1))"
        stopband = 74
    else:
        raise ValueError(f"Unknown window type: {window_type}")
    
    h_windowed = h_ideal * window
    
    return WindowResult(
        h_ideal=h_ideal,
        window=window,
        h_windowed=h_windowed,
        window_type=window_type,
        window_formula=formula,
        approx_stopband_dB=stopband
    )


# =============================================================================
# SAMPLING ANALYSIS
# =============================================================================
@dataclass
class SamplingResult:
    """Results from sampling analysis"""
    frequencies: np.ndarray = field(default_factory=lambda: np.array([]))
    Fs: float = 0.0
    F_nyquist: float = 0.0
    F_max_signal: float = 0.0
    aliased: np.ndarray = field(default_factory=lambda: np.array([]))
    apparent_frequencies: np.ndarray = field(default_factory=lambda: np.array([]))
    omega_digital: np.ndarray = field(default_factory=lambda: np.array([]))
    has_aliasing: bool = False
    analysis: List[str] = field(default_factory=list)


def SamplingAnalysis(frequencies: Union[List, np.ndarray],
                     Fs: float) -> SamplingResult:
    """
    Analyze sampling of signal components for aliasing.
    
    Nyquist criterion: Fs > 2·F_max
    
    If F > Fs/2, aliasing occurs:
        F_apparent = |F - k·Fs| where k brings result into [0, Fs/2]
    
    Parameters:
        frequencies: Signal frequency components [Hz]
        Fs: Sampling frequency [Hz]
        
    Returns:
        SamplingResult with aliasing analysis
        
    Reference: [E24 Q3, F23 Q3, E23 Q3]
    """
    frequencies = np.array(frequencies)
    F_nyquist = Fs / 2
    F_max_signal = np.max(frequencies)
    
    aliased = np.zeros(len(frequencies), dtype=bool)
    apparent_frequencies = np.zeros(len(frequencies))
    omega_digital = np.zeros(len(frequencies))
    analysis = []
    
    for i, F in enumerate(frequencies):
        if F <= F_nyquist:
            aliased[i] = False
            apparent_frequencies[i] = F
            analysis.append(f"{F:.0f} Hz: {F:.0f} ≤ {F_nyquist:.0f} → NO aliasing → Appears at {F:.0f} Hz")
        else:
            aliased[i] = True
            # Fold back: F_apparent = |Fs - F| initially
            F_app = abs(Fs - F)
            # Keep folding if still outside [0, Fs/2]
            while F_app > F_nyquist:
                F_app = abs(Fs - F_app)
            apparent_frequencies[i] = F_app
            analysis.append(f"{F:.0f} Hz: {F:.0f} > {F_nyquist:.0f} → ALIASING → Appears at {F_app:.0f} Hz")
        
        omega_digital[i] = 2 * np.pi * apparent_frequencies[i] / Fs
    
    has_aliasing = np.any(aliased)
    
    return SamplingResult(
        frequencies=frequencies,
        Fs=Fs,
        F_nyquist=F_nyquist,
        F_max_signal=F_max_signal,
        aliased=aliased,
        apparent_frequencies=apparent_frequencies,
        omega_digital=omega_digital,
        has_aliasing=has_aliasing,
        analysis=analysis
    )


def NyquistCheck(f_max: float, Fs: float) -> Tuple[bool, float, str]:
    """
    Quick Nyquist criterion check.
    
    Returns:
        (satisfies_nyquist, F_nyquist_required, explanation)
    """
    F_required = 2 * f_max
    satisfies = Fs > F_required
    
    if satisfies:
        explanation = f"✓ Fs = {Fs:.0f} Hz > 2·F_max = {F_required:.0f} Hz → No aliasing"
    else:
        explanation = f"✗ Fs = {Fs:.0f} Hz ≤ 2·F_max = {F_required:.0f} Hz → Aliasing occurs!"
    
    return satisfies, F_required, explanation


# =============================================================================
# MIN-PHASE / ALL-PASS DECOMPOSITION
# =============================================================================
@dataclass
class MinPhaseDecompResult:
    """Results from Min-Phase / All-Pass decomposition"""
    B_original: np.ndarray = field(default_factory=lambda: np.array([]))
    A_original: np.ndarray = field(default_factory=lambda: np.array([]))
    zeros_original: np.ndarray = field(default_factory=lambda: np.array([]))
    zeros_outside_UC: np.ndarray = field(default_factory=lambda: np.array([]))
    zeros_reflected: np.ndarray = field(default_factory=lambda: np.array([]))
    B_min: np.ndarray = field(default_factory=lambda: np.array([]))
    A_min: np.ndarray = field(default_factory=lambda: np.array([]))
    B_ap: np.ndarray = field(default_factory=lambda: np.array([]))
    A_ap: np.ndarray = field(default_factory=lambda: np.array([]))
    H_min_str: str = ""
    H_ap_str: str = ""
    decomposition_steps: List[str] = field(default_factory=list)


def MinPhaseDecomposition(B: Union[List, np.ndarray],
                          A: Union[List, np.ndarray] = None) -> MinPhaseDecompResult:
    """
    Decompose H(z) into minimum-phase × all-pass: H(z) = H_min(z) · H_ap(z)
    
    Method:
        1. Find zeros outside unit circle
        2. For each z0 outside UC, reflect to 1/z0* inside UC
        3. H_min gets all zeros inside UC
        4. H_ap compensates: H_ap = (z - z0) / (z - 1/z0*)
    
    Parameters:
        B: Numerator coefficients
        A: Denominator coefficients
        
    Returns:
        MinPhaseDecompResult with decomposition
        
    Reference: [F24 Q3, E24 Q3]
    """
    B = np.array(B, dtype=complex)
    A = np.array(A, dtype=complex) if A is not None else np.array([1.0])
    
    # Find zeros
    zeros = np.roots(B) if len(B) > 1 else np.array([])
    
    zeros_outside = []
    zeros_reflected = []
    zeros_min = []
    steps = []
    
    steps.append(f"Original zeros: {zeros}")
    
    for z0 in zeros:
        if np.abs(z0) > 1 + 1e-10:
            # Outside UC - need to reflect
            z_reflected = 1 / np.conj(z0)
            zeros_outside.append(z0)
            zeros_reflected.append(z_reflected)
            zeros_min.append(z_reflected)
            steps.append(f"  z = {z0:.4f}: |z| = {np.abs(z0):.4f} > 1 → Reflect to 1/z* = {z_reflected:.4f}")
        else:
            # Inside or on UC - keep as is
            zeros_min.append(z0)
            steps.append(f"  z = {z0:.4f}: |z| = {np.abs(z0):.4f} ≤ 1 → Keep")
    
    # Build H_min numerator from minimum-phase zeros
    if len(zeros_min) > 0:
        B_min = np.poly(zeros_min)
        # Scale to match original DC gain approximately
        scale = B[0] / B_min[0] if abs(B_min[0]) > 1e-10 else 1.0
        B_min = B_min * scale
    else:
        B_min = np.array([1.0])
    
    A_min = A.copy()
    
    # Build all-pass from outside zeros
    B_ap = np.array([1.0])
    A_ap = np.array([1.0])
    
    for i, z0 in enumerate(zeros_outside):
        z_r = zeros_reflected[i]
        # All-pass factor: (z - z0) / (z - z_r) normalized
        # In coefficient form for z^{-1}: (1 - z0·z^{-1}) / (1 - z_r·z^{-1})
        B_ap_factor = np.array([1, -z0])
        A_ap_factor = np.array([1, -z_r])
        B_ap = np.convolve(B_ap, B_ap_factor)
        A_ap = np.convolve(A_ap, A_ap_factor)
    
    # Clean up
    B_min = np.real_if_close(B_min)
    B_ap = np.real_if_close(B_ap)
    A_ap = np.real_if_close(A_ap)
    
    # String representations
    H_min_str = f"H_min has zeros at: {zeros_min}"
    H_ap_str = f"H_ap = product of (z - z0)/(z - 1/z0*) factors"
    
    return MinPhaseDecompResult(
        B_original=B,
        A_original=A,
        zeros_original=zeros,
        zeros_outside_UC=np.array(zeros_outside),
        zeros_reflected=np.array(zeros_reflected),
        B_min=B_min,
        A_min=A_min,
        B_ap=B_ap,
        A_ap=A_ap,
        H_min_str=H_min_str,
        H_ap_str=H_ap_str,
        decomposition_steps=steps
    )


# =============================================================================
# CONVENIENCE: DIGITAL FREQUENCY CONVERSION
# =============================================================================
def hz_to_omega(F: float, Fs: float) -> float:
    """Convert Hz to digital angular frequency [rad/sample]"""
    return 2 * np.pi * F / Fs


def omega_to_hz(omega: float, Fs: float) -> float:
    """Convert digital angular frequency to Hz"""
    return omega * Fs / (2 * np.pi)


# =============================================================================
# QUICK VERIFICATION FUNCTIONS
# =============================================================================
def verify_filter_specs(B, A, Fs, specs):
    """
    Verify filter meets specifications.
    
    specs = {
        'passband': [(F1, min_dB), (F2, min_dB), ...],
        'stopband': [(F1, max_dB), (F2, max_dB), ...]
    }
    """
    results = {'passband': [], 'stopband': []}
    
    for F, spec_dB in specs.get('passband', []):
        omega = 2 * np.pi * F / Fs
        z = np.exp(1j * omega)
        H = sum(B[k] * z**(-k) for k in range(len(B))) / sum(A[k] * z**(-k) for k in range(len(A)))
        H_dB = 20 * np.log10(abs(H) + 1e-12)
        passed = H_dB >= spec_dB
        results['passband'].append({
            'F': F, 'H_dB': H_dB, 'spec': f'≥ {spec_dB} dB', 'passed': passed
        })
    
    for F, spec_dB in specs.get('stopband', []):
        omega = 2 * np.pi * F / Fs
        z = np.exp(1j * omega)
        H = sum(B[k] * z**(-k) for k in range(len(B))) / sum(A[k] * z**(-k) for k in range(len(A)))
        H_dB = 20 * np.log10(abs(H) + 1e-12)
        passed = H_dB <= spec_dB
        results['stopband'].append({
            'F': F, 'H_dB': H_dB, 'spec': f'≤ {spec_dB} dB', 'passed': passed
        })
    
    return results
