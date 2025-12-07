"""
EM Tools - Electromagnetic Calculation Library
==============================================

Python equivalent of the MATLAB EM Toolbox.
All functions work with NumPy arrays and complex numbers.

Usage:
    from em_tools import *
    
    result = Medium(4, 10e9)
    result = Polarization([1, -1j, 0])
    result = Fresnel(1, 4, 45)
    result = TLine(50, 100, 0.3)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Union
import cmath

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================
EPS0 = 8.854187817e-12  # F/m
MU0 = 4 * np.pi * 1e-7  # H/m
C0 = 1 / np.sqrt(EPS0 * MU0)  # m/s
ETA0 = np.sqrt(MU0 / EPS0)  # ~377 Ohm


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def to_polar(z):
    """Convert complex number to (magnitude, angle_degrees)"""
    return abs(z), np.degrees(cmath.phase(z))


def from_polar(mag, ang_deg):
    """Convert polar (magnitude, angle_degrees) to complex"""
    return mag * cmath.exp(1j * np.radians(ang_deg))


# =============================================================================
# B_INF_WIRE - Magnetic field from infinite wire
# =============================================================================
def B_inf_wire(I: float, r: float, mu_r: float = 1.0) -> float:
    """
    B-field magnitude around an infinitely long wire.
    
    Parameters:
        I: Current [A]
        r: Radial distance from wire [m]
        mu_r: Relative permeability (default 1)
    
    Returns:
        B: Magnetic field magnitude [T]
    """
    if r <= 0:
        raise ValueError("Distance r must be positive.")
    
    mu = MU0 * mu_r
    B = mu * I / (2 * np.pi * r)
    return B


# =============================================================================
# COULOMB_PAIR - Coulomb force between charges
# =============================================================================
def coulomb_pair(q1: float, q2: float, r1: np.ndarray, r2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Coulomb force between two point charges (vector form).
    
    Parameters:
        q1, q2: Charges [C]
        r1, r2: Position vectors [x, y, z] in meters
    
    Returns:
        F12: Force on q1 due to q2 [N]
        F21: Force on q2 due to q1 [N]
    """
    r1 = np.array(r1, dtype=float)
    r2 = np.array(r2, dtype=float)
    
    k_e = 1 / (4 * np.pi * EPS0)
    
    R12 = r1 - r2
    d12 = np.linalg.norm(R12)
    
    if d12 == 0:
        raise ValueError("Charges must not coincide.")
    
    u12 = R12 / d12
    Fmag = k_e * q1 * q2 / (d12 ** 2)
    
    F12 = Fmag * u12
    F21 = -F12
    
    return F12, F21


# =============================================================================
# MEDIUM - Wave parameters in materials
# =============================================================================
@dataclass
class MediumResult:
    """Results from Medium calculation"""
    eps_r: float = 1.0
    mu_r: float = 1.0
    sigma: float = 0.0
    freq: float = 0.0
    omega: float = 0.0
    tan_delta: float = 0.0
    classification: str = ""
    gamma: complex = 0j
    alpha: float = 0.0
    beta: float = 0.0
    lambda_: float = 0.0  # wavelength (lambda is reserved)
    up: float = 0.0  # phase velocity
    eta: complex = 0j
    n: float = 1.0
    skin_depth: float = float('inf')
    name: str = ""


def Medium(arg1, arg2=None, arg3=None, arg4=None, arg5=None) -> MediumResult:
    """
    Electromagnetic wave parameters in materials.
    
    Modes:
        Medium(eps_r, freq)                    - Lossless dielectric
        Medium(eps_r, sigma, freq)             - Lossy medium
        Medium(eps_r, sigma, freq, mu_r)       - Magnetic material
        Medium(eps_r, sigma, freq, mu_r, name) - With label
        Medium('conductor', sigma, freq)       - Good conductor
        Medium('skin', sigma, freq)            - Skin depth only
        Medium('free', freq)                   - Free space
        Medium('tand', eps_r, tan_delta, freq) - From loss tangent
    """
    # Detect mode
    if isinstance(arg1, str):
        mode = arg1.lower()
        if mode == 'free':
            return _medium_free_space(arg2)
        elif mode == 'conductor':
            mu_r = arg4 if arg4 is not None else 1.0
            return _medium_conductor(arg2, arg3, mu_r)
        elif mode == 'skin':
            mu_r = arg4 if arg4 is not None else 1.0
            return _medium_skin_depth(arg2, arg3, mu_r)
        elif mode == 'tand':
            mu_r = arg5 if arg5 is not None else 1.0
            return _medium_from_tand(arg2, arg3, arg4, mu_r)
        else:
            raise ValueError(f"Unknown mode: {mode}")
    else:
        # Numeric input
        if arg3 is None:
            # Lossless: Medium(eps_r, freq)
            return _medium_lossless(arg1, arg2)
        else:
            # Lossy: Medium(eps_r, sigma, freq, [mu_r], [name])
            mu_r = arg4 if arg4 is not None else 1.0
            name = arg5 if arg5 is not None else "Lossy Medium"
            return _medium_lossy(arg1, arg2, arg3, mu_r, name)


def _medium_lossless(eps_r: float, freq: float, mu_r: float = 1.0) -> MediumResult:
    omega = 2 * np.pi * freq
    eps = EPS0 * eps_r
    mu = MU0 * mu_r
    
    beta = omega * np.sqrt(mu * eps)
    lambda_ = 2 * np.pi / beta
    up = omega / beta
    eta = np.sqrt(mu / eps)
    n = C0 / up
    
    result = MediumResult(
        eps_r=eps_r, mu_r=mu_r, sigma=0, freq=freq, omega=omega,
        tan_delta=0, classification='Lossless',
        gamma=1j * beta, alpha=0, beta=beta,
        lambda_=lambda_, up=up, eta=eta, n=n, skin_depth=float('inf')
    )
    return result


def _medium_lossy(eps_r: float, sigma: float, freq: float, mu_r: float = 1.0, name: str = "Lossy Medium") -> MediumResult:
    omega = 2 * np.pi * freq
    eps = EPS0 * eps_r
    mu = MU0 * mu_r
    
    tan_delta = sigma / (omega * eps)
    
    if tan_delta < 0.01:
        classification = 'Lossless (approx)'
    elif tan_delta < 0.1:
        classification = 'Low-Loss Dielectric'
    elif tan_delta < 10:
        classification = 'Quasi-Conductor'
    else:
        classification = 'Good Conductor'
    
    gamma = cmath.sqrt(1j * omega * mu * (sigma + 1j * omega * eps))
    alpha = gamma.real
    beta = gamma.imag
    
    lambda_ = 2 * np.pi / beta if beta > 0 else float('inf')
    up = omega / beta if beta > 0 else float('inf')
    
    eta = cmath.sqrt(1j * omega * mu / (sigma + 1j * omega * eps))
    n = C0 / up if up < float('inf') else 1.0
    skin_depth = 1 / alpha if alpha > 0 else float('inf')
    
    return MediumResult(
        eps_r=eps_r, mu_r=mu_r, sigma=sigma, freq=freq, omega=omega,
        tan_delta=tan_delta, classification=classification,
        gamma=gamma, alpha=alpha, beta=beta,
        lambda_=lambda_, up=up, eta=eta, n=n, skin_depth=skin_depth, name=name
    )


def _medium_conductor(sigma: float, freq: float, mu_r: float = 1.0) -> MediumResult:
    mu = MU0 * mu_r
    omega = 2 * np.pi * freq
    
    alpha = np.sqrt(np.pi * freq * mu * sigma)
    beta = alpha
    
    skin_depth = 1 / alpha
    lambda_ = 2 * np.pi / beta
    up = omega / beta
    
    eta = (1 + 1j) * np.sqrt(omega * mu / (2 * sigma))
    
    return MediumResult(
        eps_r=1, mu_r=mu_r, sigma=sigma, freq=freq, omega=omega,
        tan_delta=float('inf'), classification='Good Conductor',
        gamma=alpha + 1j * beta, alpha=alpha, beta=beta,
        lambda_=lambda_, up=up, eta=eta, n=C0/up, skin_depth=skin_depth
    )


def _medium_skin_depth(sigma: float, freq: float, mu_r: float = 1.0) -> MediumResult:
    mu = MU0 * mu_r
    delta = 1 / np.sqrt(np.pi * freq * mu * sigma)
    
    return MediumResult(sigma=sigma, mu_r=mu_r, freq=freq, skin_depth=delta)


def _medium_free_space(freq: float) -> MediumResult:
    omega = 2 * np.pi * freq
    k0 = omega / C0
    lambda0 = C0 / freq
    
    return MediumResult(
        eps_r=1, mu_r=1, sigma=0, freq=freq, omega=omega,
        classification='Free Space',
        gamma=1j * k0, alpha=0, beta=k0,
        lambda_=lambda0, up=C0, eta=ETA0, n=1
    )


def _medium_from_tand(eps_r: float, tan_delta: float, freq: float, mu_r: float = 1.0) -> MediumResult:
    omega = 2 * np.pi * freq
    eps = EPS0 * eps_r
    sigma = tan_delta * omega * eps
    return _medium_lossy(eps_r, sigma, freq, mu_r, 'From Loss Tangent')


# =============================================================================
# POLARIZATION - Wave polarization analysis
# =============================================================================
@dataclass
class PolarizationResult:
    """Results from Polarization analysis"""
    type: str = ""
    handedness: str = "N/A"
    AR: float = 1.0  # Axial ratio
    AR_dB: float = 0.0
    major: float = 0.0
    minor: float = 0.0
    tilt_deg: float = 0.0
    F: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=complex))
    k_hat: np.ndarray = field(default_factory=lambda: np.array([0, 0, 1.0]))


def Polarization(arg1, arg2=None, arg3=None, arg4=None, arg5=None) -> PolarizationResult:
    """
    Complete polarization analysis of an EM wave.
    
    Modes:
        Polarization(F)                              - Complex phasor, +z propagation
        Polarization(F, k_hat)                       - Specify propagation direction
        Polarization('ap', Ex, Ey, phi_x, phi_y)     - Amplitude/phase
        Polarization(u, v, beta)                     - Time-domain coefficients
    """
    if isinstance(arg1, str) and arg1.lower() == 'ap':
        # Amplitude/Phase mode
        Ex, Ey, phi_x, phi_y = arg2, arg3, arg4, arg5
        Fx = Ex * cmath.exp(1j * np.radians(phi_x))
        Fy = Ey * cmath.exp(1j * np.radians(phi_y))
        F = np.array([Fx, Fy, 0], dtype=complex)
        k_hat = np.array([0, 0, 1.0])
    elif arg2 is not None and arg3 is not None and np.isrealobj(arg1) and np.isrealobj(arg2):
        # Time-domain mode: u, v, beta
        u = np.array(arg1, dtype=float).flatten()
        v = np.array(arg2, dtype=float).flatten()
        beta = np.array(arg3, dtype=float).flatten()
        if len(u) == 2: u = np.append(u, 0)
        if len(v) == 2: v = np.append(v, 0)
        F = u - 1j * v
        k_hat = beta / np.linalg.norm(beta)
    else:
        # Complex phasor mode
        F = np.array(arg1, dtype=complex).flatten()
        if len(F) == 2:
            F = np.append(F, 0)
        if arg2 is not None:
            k_hat = np.array(arg2, dtype=float).flatten()
            k_hat = k_hat / np.linalg.norm(k_hat)
        else:
            k_hat = np.array([0, 0, 1.0])
    
    Fr = np.real(F)
    Fi = np.imag(F)
    
    # Classification tolerance
    tol = 1e-3
    scale = max(np.linalg.norm(Fr), np.linalg.norm(Fi))
    if scale == 0:
        scale = 1
    
    cross_ri = np.cross(Fr, Fi)
    is_linear = np.linalg.norm(cross_ri) < tol * scale**2
    
    dot_ri = np.dot(Fr, Fi)
    amp_equal = abs(np.linalg.norm(Fr) - np.linalg.norm(Fi)) < tol * scale
    is_circular = (not is_linear) and (abs(dot_ri) < tol * scale**2) and amp_equal
    
    # Handedness
    if is_linear:
        handedness = "N/A"
    else:
        # E(t) = Fr*cos - Fi*sin = u*cos + v*sin where u=Fr, v=-Fi
        hand = np.dot(k_hat, np.cross(Fr, -Fi))
        handedness = "RHCP" if hand > 0 else "LHCP"
    
    # Type
    if is_linear:
        pol_type = "Linear"
    elif is_circular:
        pol_type = "Circular"
    else:
        pol_type = "Elliptical"
    
    # Axial ratio calculation
    idx = np.argsort(np.abs(Fr) + np.abs(Fi))[::-1][:2]
    Fr2 = Fr[idx]
    Fi2 = Fi[idx]
    
    num = 2 * np.dot(Fr2, Fi2)
    den = np.linalg.norm(Fi2)**2 - np.linalg.norm(Fr2)**2
    phi1 = 0.5 * np.arctan2(num, den)
    phi2 = phi1 + np.pi/2
    
    E1 = np.linalg.norm(Fr2 * np.cos(phi1) - Fi2 * np.sin(phi1))
    E2 = np.linalg.norm(Fr2 * np.cos(phi2) - Fi2 * np.sin(phi2))
    
    if E1 >= E2:
        major, minor, tilt = E1, E2, phi1
    else:
        major, minor, tilt = E2, E1, phi2
    
    if minor < 1e-12 * major:
        AR = float('inf')
        AR_dB = float('inf')
    else:
        AR = major / minor
        AR_dB = 20 * np.log10(AR)
    
    return PolarizationResult(
        type=pol_type, handedness=handedness,
        AR=AR, AR_dB=AR_dB,
        major=major, minor=minor, tilt_deg=np.degrees(tilt),
        F=F, k_hat=k_hat
    )


# =============================================================================
# FRESNEL - Reflection/Transmission at interfaces
# =============================================================================
@dataclass
class FresnelResult:
    """Results from Fresnel calculation"""
    eps_r1: float = 1.0
    eps_r2: float = 1.0
    mu_r1: float = 1.0
    mu_r2: float = 1.0
    eta1: float = ETA0
    eta2: float = ETA0
    n1: float = 1.0
    n2: float = 1.0
    theta_i: float = 0.0
    theta_t: float = 0.0
    Gamma: complex = 0j
    Gamma_TE: complex = 0j
    Gamma_TM: complex = 0j
    tau: complex = 1.0
    tau_TE: complex = 1.0
    tau_TM: complex = 1.0
    R: float = 0.0
    R_TE: float = 0.0
    R_TM: float = 0.0
    T: float = 1.0
    T_TE: float = 1.0
    T_TM: float = 1.0
    TIR: bool = False
    theta_Brewster: float = 0.0
    theta_critical: float = 0.0


def Fresnel(arg1, arg2=None, arg3=None, arg4=None) -> FresnelResult:
    """
    Fresnel reflection/transmission calculator.
    
    Modes:
        Fresnel(eps_r1, eps_r2)                 - Normal incidence
        Fresnel(eps_r1, eps_r2, theta_i)        - Oblique incidence
        Fresnel(eps_r1, eps_r2, theta_i, 'TE')  - TE only
        Fresnel(eps_r1, eps_r2, theta_i, 'TM')  - TM only
        Fresnel('snell', n1, n2, theta_i)       - Snell's law
        Fresnel('brewster', eps_r1, eps_r2)    - Brewster angle
        Fresnel('critical', eps_r1, eps_r2)    - Critical angle
    """
    if isinstance(arg1, str):
        mode = arg1.lower()
        if mode == 'snell':
            return _fresnel_snell(arg2, arg3, arg4)
        elif mode == 'brewster':
            return _fresnel_brewster(arg2, arg3)
        elif mode == 'critical':
            return _fresnel_critical(arg2, arg3)
        else:
            raise ValueError(f"Unknown mode: {mode}")
    else:
        if arg3 is None:
            # Normal incidence
            return _fresnel_normal(arg1, arg2)
        else:
            # Oblique incidence
            pol = arg4 if arg4 is not None else 'both'
            return _fresnel_oblique(arg1, arg2, arg3, pol)


def _fresnel_normal(eps_r1: float, eps_r2: float, mu_r1: float = 1.0, mu_r2: float = 1.0) -> FresnelResult:
    eta1 = ETA0 * np.sqrt(mu_r1 / eps_r1)
    eta2 = ETA0 * np.sqrt(mu_r2 / eps_r2)
    n1 = np.sqrt(eps_r1 * mu_r1)
    n2 = np.sqrt(eps_r2 * mu_r2)
    
    Gamma = (eta2 - eta1) / (eta2 + eta1)
    tau = 2 * eta2 / (eta2 + eta1)
    R = abs(Gamma) ** 2
    T = 1 - R
    
    return FresnelResult(
        eps_r1=eps_r1, eps_r2=eps_r2, mu_r1=mu_r1, mu_r2=mu_r2,
        eta1=eta1, eta2=eta2, n1=n1, n2=n2,
        theta_i=0, theta_t=0,
        Gamma=Gamma, Gamma_TE=Gamma, Gamma_TM=Gamma,
        tau=tau, tau_TE=tau, tau_TM=tau,
        R=R, R_TE=R, R_TM=R, T=T, T_TE=T, T_TM=T
    )


def _fresnel_oblique(eps_r1: float, eps_r2: float, theta_i_deg: float, pol: str = 'both') -> FresnelResult:
    eta1 = ETA0 * np.sqrt(1.0 / eps_r1)
    eta2 = ETA0 * np.sqrt(1.0 / eps_r2)
    n1 = np.sqrt(eps_r1)
    n2 = np.sqrt(eps_r2)
    
    theta_i = np.radians(theta_i_deg)
    sin_theta_t = (n1 / n2) * np.sin(theta_i)
    
    result = FresnelResult(
        eps_r1=eps_r1, eps_r2=eps_r2,
        eta1=eta1, eta2=eta2, n1=n1, n2=n2,
        theta_i=theta_i_deg
    )
    
    if abs(sin_theta_t) > 1:
        # Total internal reflection
        result.TIR = True
        result.theta_t = float('nan')
        result.Gamma_TE = cmath.exp(1j * 2 * _tir_phase(n1, n2, theta_i, 'TE'))
        result.Gamma_TM = cmath.exp(1j * 2 * _tir_phase(n1, n2, theta_i, 'TM'))
        result.R_TE = 1.0
        result.R_TM = 1.0
        result.T_TE = 0.0
        result.T_TM = 0.0
        return result
    
    theta_t = np.arcsin(sin_theta_t)
    result.theta_t = np.degrees(theta_t)
    
    # TE (s-polarized)
    Gamma_TE = (eta2 * np.cos(theta_i) - eta1 * np.cos(theta_t)) / \
               (eta2 * np.cos(theta_i) + eta1 * np.cos(theta_t))
    tau_TE = 2 * eta2 * np.cos(theta_i) / (eta2 * np.cos(theta_i) + eta1 * np.cos(theta_t))
    
    # TM (p-polarized)
    Gamma_TM = (eta2 * np.cos(theta_t) - eta1 * np.cos(theta_i)) / \
               (eta2 * np.cos(theta_t) + eta1 * np.cos(theta_i))
    tau_TM = 2 * eta2 * np.cos(theta_i) / (eta2 * np.cos(theta_t) + eta1 * np.cos(theta_i))
    
    result.Gamma_TE = Gamma_TE
    result.Gamma_TM = Gamma_TM
    result.tau_TE = tau_TE
    result.tau_TM = tau_TM
    result.R_TE = abs(Gamma_TE) ** 2
    result.R_TM = abs(Gamma_TM) ** 2
    result.T_TE = 1 - result.R_TE
    result.T_TM = 1 - result.R_TM
    result.theta_Brewster = np.degrees(np.arctan(n2 / n1))
    
    return result


def _tir_phase(n1, n2, theta_i, pol):
    cos_i = np.cos(theta_i)
    sin_i = np.sin(theta_i)
    x = np.sqrt((n1 * sin_i / n2) ** 2 - 1)
    if pol.upper() == 'TE':
        return np.arctan2(x, cos_i)
    else:
        return np.arctan2((n1 / n2) ** 2 * x, cos_i)


def _fresnel_snell(n1: float, n2: float, theta_i_deg: float) -> FresnelResult:
    theta_i = np.radians(theta_i_deg)
    sin_theta_t = (n1 / n2) * np.sin(theta_i)
    
    result = FresnelResult(n1=n1, n2=n2, theta_i=theta_i_deg)
    
    if abs(sin_theta_t) > 1:
        result.TIR = True
        result.theta_t = float('nan')
        result.theta_critical = np.degrees(np.arcsin(n2 / n1))
    else:
        result.theta_t = np.degrees(np.arcsin(sin_theta_t))
        result.TIR = False
    
    return result


def _fresnel_brewster(eps_r1: float, eps_r2: float) -> FresnelResult:
    n1 = np.sqrt(eps_r1)
    n2 = np.sqrt(eps_r2)
    theta_B = np.degrees(np.arctan(n2 / n1))
    
    return FresnelResult(
        eps_r1=eps_r1, eps_r2=eps_r2, n1=n1, n2=n2,
        theta_Brewster=theta_B
    )


def _fresnel_critical(eps_r1: float, eps_r2: float) -> FresnelResult:
    n1 = np.sqrt(eps_r1)
    n2 = np.sqrt(eps_r2)
    
    result = FresnelResult(eps_r1=eps_r1, eps_r2=eps_r2, n1=n1, n2=n2)
    
    if n1 > n2:
        result.theta_critical = np.degrees(np.arcsin(n2 / n1))
        result.TIR = True  # TIR is possible
    else:
        result.theta_critical = float('nan')
        result.TIR = False  # TIR not possible
    
    return result


# =============================================================================
# TLINE - Transmission Line Calculator
# =============================================================================
@dataclass
class TLineResult:
    """Results from TLine calculation"""
    Z0: float = 50.0
    ZL: complex = 50.0
    Z_in: complex = 50.0
    len_lambda: float = 0.0
    Gamma_L: complex = 0j
    Gamma_in: complex = 0j
    VSWR: float = 1.0
    z_vmax: float = 0.0
    z_vmin: float = 0.0
    P_reflected: float = 0.0
    P_delivered: float = 1.0
    RL_dB: float = float('inf')
    # For stub design
    short_len: float = 0.0
    open_len: float = 0.0


def TLine(arg1, arg2=None, arg3=None, arg4=None, arg5=None) -> TLineResult:
    """
    Transmission Line Calculator.
    
    Modes:
        TLine(Z0, ZL, len_lambda)              - Basic analysis
        TLine('Zin', Z0, ZL, len_lambda)       - Find input impedance
        TLine('ZL', Z0, Zin, len_lambda)       - Find load impedance
        TLine('Gamma', Z0, Z)                  - Gamma from impedance
        TLine('Z', Z0, Gamma)                  - Impedance from Gamma
        TLine('load', Z0, Gamma_in, len)       - Find load from Gamma at input
        TLine('QW', Z_source, Z_load)          - Quarter-wave transformer
        TLine('stub', Z_target, Z0)            - Stub design
        TLine('stub', Z_target, Z0, 'short')   - Short stub only
    """
    if isinstance(arg1, str):
        mode = arg1.lower()
        if mode == 'zin':
            return _tline_zin(arg2, arg3, arg4)
        elif mode == 'zl':
            return _tline_zl(arg2, arg3, arg4)
        elif mode == 'gamma':
            return _tline_gamma_from_z(arg2, arg3)
        elif mode == 'z':
            return _tline_z_from_gamma(arg2, arg3)
        elif mode == 'load':
            return _tline_find_load(arg2, arg3, arg4)
        elif mode == 'qw':
            return _tline_quarter_wave(arg2, arg3)
        elif mode == 'stub':
            stub_type = arg4 if arg4 is not None else 'both'
            return _tline_stub(arg2, arg3, stub_type)
        elif mode == 'gamma_in':
            return _tline_gamma_propagate(arg2, arg3)
        elif mode == 'gamma_l':
            return _tline_gamma_to_load(arg2, arg3)
        else:
            raise ValueError(f"Unknown mode: {mode}")
    else:
        # Basic analysis: TLine(Z0, ZL, len_lambda)
        return _tline_basic(arg1, arg2, arg3)


def _tline_basic(Z0: float, ZL: complex, len_lambda: float) -> TLineResult:
    beta_l = 2 * np.pi * len_lambda
    
    Gamma_L = (ZL - Z0) / (ZL + Z0)
    Gamma_in = Gamma_L * cmath.exp(-1j * 2 * beta_l)
    
    # Input impedance
    if abs(len_lambda % 0.5 - 0.25) < 1e-9:
        Z_in = Z0 ** 2 / ZL
    elif abs(len_lambda % 0.5) < 1e-9:
        Z_in = ZL
    else:
        Z_in = Z0 * (1 + Gamma_in) / (1 - Gamma_in)
    
    mag_Gamma = abs(Gamma_L)
    VSWR = (1 + mag_Gamma) / (1 - mag_Gamma) if mag_Gamma < 1 else float('inf')
    
    P_reflected = mag_Gamma ** 2
    P_delivered = 1 - P_reflected
    RL_dB = -20 * np.log10(mag_Gamma) if mag_Gamma > 0 else float('inf')
    
    # Vmax/Vmin positions
    if mag_Gamma > 1e-10:
        phi_L = cmath.phase(Gamma_L)
        z_vmax = (-phi_L / (4 * np.pi)) % 0.5
        z_vmin = ((np.pi - phi_L) / (4 * np.pi)) % 0.5
    else:
        z_vmax = z_vmin = float('nan')
    
    return TLineResult(
        Z0=Z0, ZL=ZL, Z_in=Z_in, len_lambda=len_lambda,
        Gamma_L=Gamma_L, Gamma_in=Gamma_in, VSWR=VSWR,
        z_vmax=z_vmax, z_vmin=z_vmin,
        P_reflected=P_reflected, P_delivered=P_delivered, RL_dB=RL_dB
    )


def _tline_zin(Z0: float, ZL: complex, len_lambda: float) -> TLineResult:
    return _tline_basic(Z0, ZL, len_lambda)


def _tline_zl(Z0: float, Z_in: complex, len_lambda: float) -> TLineResult:
    beta_l = 2 * np.pi * len_lambda
    
    if abs(len_lambda % 0.5 - 0.25) < 1e-9:
        ZL = Z0 ** 2 / Z_in
    elif abs(len_lambda % 0.5) < 1e-9:
        ZL = Z_in
    else:
        ZL = Z0 * (Z_in - 1j * Z0 * np.tan(beta_l)) / (Z0 - 1j * Z_in * np.tan(beta_l))
    
    result = _tline_basic(Z0, ZL, len_lambda)
    result.Z_in = Z_in
    return result


def _tline_gamma_from_z(Z0: float, Z: complex) -> TLineResult:
    Gamma = (Z - Z0) / (Z + Z0)
    mag = abs(Gamma)
    VSWR = (1 + mag) / (1 - mag) if mag < 1 else float('inf')
    
    return TLineResult(Z0=Z0, ZL=Z, Gamma_L=Gamma, VSWR=VSWR)


def _tline_z_from_gamma(Z0: float, Gamma: complex) -> TLineResult:
    Z = Z0 * (1 + Gamma) / (1 - Gamma)
    return TLineResult(Z0=Z0, ZL=Z, Gamma_L=Gamma)


def _tline_find_load(Z0: float, Gamma_in: complex, len_lambda: float) -> TLineResult:
    beta_l = 2 * np.pi * len_lambda
    Gamma_L = Gamma_in * cmath.exp(1j * 2 * beta_l)
    Z_L = Z0 * (1 + Gamma_L) / (1 - Gamma_L)
    
    mag = abs(Gamma_L)
    VSWR = (1 + mag) / (1 - mag) if mag < 1 else float('inf')
    
    return TLineResult(
        Z0=Z0, ZL=Z_L, len_lambda=len_lambda,
        Gamma_L=Gamma_L, Gamma_in=Gamma_in, VSWR=VSWR
    )


def _tline_gamma_propagate(Gamma_L: complex, len_lambda: float) -> TLineResult:
    beta_l = 2 * np.pi * len_lambda
    Gamma_in = Gamma_L * cmath.exp(-1j * 2 * beta_l)
    return TLineResult(Gamma_L=Gamma_L, Gamma_in=Gamma_in, len_lambda=len_lambda)


def _tline_gamma_to_load(Gamma_in: complex, len_lambda: float) -> TLineResult:
    beta_l = 2 * np.pi * len_lambda
    Gamma_L = Gamma_in * cmath.exp(1j * 2 * beta_l)
    return TLineResult(Gamma_L=Gamma_L, Gamma_in=Gamma_in, len_lambda=len_lambda)


def _tline_quarter_wave(Z_source: float, Z_load: float) -> TLineResult:
    Z_qw = np.sqrt(Z_source * Z_load)
    return TLineResult(Z0=Z_qw, ZL=Z_load, len_lambda=0.25)


def _tline_stub(Z_target: complex, Z0: float, stub_type: str = 'both') -> TLineResult:
    X = Z_target.imag if isinstance(Z_target, complex) else Z_target
    
    result = TLineResult(Z0=Z0)
    
    # Short stub: Z_in = j*Z0*tan(β*ℓ) = jX → tan(βℓ) = X/Z0
    tan_bl = X / Z0
    beta_l = np.arctan(tan_bl)
    if beta_l < 0:
        beta_l += np.pi
    result.short_len = beta_l / (2 * np.pi)
    
    # Open stub: Z_in = -j*Z0*cot(β*ℓ) = jX → cot(βℓ) = -X/Z0
    if abs(X) > 1e-10:
        tan_bl_open = -Z0 / X
        beta_l_open = np.arctan(tan_bl_open)
        if beta_l_open < 0:
            beta_l_open += np.pi
        result.open_len = beta_l_open / (2 * np.pi)
    else:
        result.open_len = float('nan')
    
    return result


# =============================================================================
# STUBMATCH - Single-stub matching
# =============================================================================
@dataclass
class StubMatchResult:
    """Results from StubMatch calculation"""
    ZL: complex = 0j
    Z0: float = 50.0
    stub_type: str = "short"
    lambda_: float = float('nan')
    d: float = 0.0  # Distance to stub (wavelengths)
    l: float = 0.0  # Stub length (wavelengths)
    d_alt: float = float('nan')
    l_alt: float = float('nan')
    d_mm: float = 0.0
    l_mm: float = 0.0


def StubMatch(ZL: complex, Z0: float, stub_type: str = 'short', lambda_: float = None) -> StubMatchResult:
    """
    Single-stub matching calculator.
    
    Parameters:
        ZL: Load impedance [Ω]
        Z0: Characteristic impedance [Ω]
        stub_type: 'short' or 'open'
        lambda_: Wavelength [m] (optional, for physical lengths)
    """
    zL = ZL / Z0
    yL = 1 / zL
    beta = 2 * np.pi
    
    d_solutions = []
    l_solutions = []
    
    # Search for solutions
    for d in np.linspace(0.001, 0.499, 1000):
        y_in = (yL + 1j * np.tan(beta * d)) / (1 + 1j * yL * np.tan(beta * d))
        
        if abs(y_in.real - 1) < 0.01:
            # Refine
            d_fine = np.linspace(max(0.001, d - 0.01), min(0.499, d + 0.01), 100)
            errors = [abs((yL + 1j * np.tan(beta * df)) / (1 + 1j * yL * np.tan(beta * df)).real - 1) 
                      for df in d_fine]
            d_refined = d_fine[np.argmin(errors)]
            
            if not d_solutions or all(abs(ds - d_refined) > 0.02 for ds in d_solutions):
                d_solutions.append(d_refined)
                
                y_in = (yL + 1j * np.tan(beta * d_refined)) / (1 + 1j * yL * np.tan(beta * d_refined))
                b_in = y_in.imag
                b_stub = -b_in
                
                if stub_type.lower() == 'short':
                    if abs(b_stub) < 1e-10:
                        l = 0.25
                    else:
                        l = np.arctan(-1 / b_stub) / beta
                else:
                    l = np.arctan(b_stub) / beta
                
                l = l % 0.5
                if l < 0.001:
                    l += 0.5
                l_solutions.append(l)
    
    result = StubMatchResult(ZL=ZL, Z0=Z0, stub_type=stub_type)
    
    if lambda_ is not None:
        result.lambda_ = lambda_
    
    if d_solutions:
        result.d = d_solutions[0]
        result.l = l_solutions[0]
        
        if lambda_ is not None:
            result.d_mm = result.d * lambda_ * 1000
            result.l_mm = result.l * lambda_ * 1000
        
        if len(d_solutions) >= 2:
            result.d_alt = d_solutions[1]
            result.l_alt = l_solutions[1]
    
    return result


# =============================================================================
# POYNTING_PW - Poynting vector and H-field for plane waves
# =============================================================================
@dataclass
class PoyntingResult:
    """Results from poynting_pw calculation"""
    E_phasor: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=complex))
    H_phasor: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=complex))
    k_hat: np.ndarray = field(default_factory=lambda: np.array([0, 0, 1.0]))
    eta: float = ETA0
    S_avg: np.ndarray = field(default_factory=lambda: np.zeros(3))
    S_mag: float = 0.0


def poynting_pw(arg1, arg2=None, arg3=None, arg4=None, arg5=None) -> PoyntingResult:
    """
    Plane wave Poynting vector and H-field calculator.
    
    Modes:
        poynting_pw(E_phasor, k_hat, [eta])           - Vector phasor
        poynting_pw('time', a, b, E0, beta_vec, [eta]) - Time-domain
    """
    if isinstance(arg1, str) and arg1.lower() == 'time':
        # Time-domain mode
        a = np.array(arg2, dtype=float).flatten()
        b = np.array(arg3, dtype=float).flatten()
        E0 = arg4
        beta_vec = np.array(arg5, dtype=float).flatten() if arg5 is not None else np.array([0, 0, 1])
        eta = 377
        
        if len(a) == 2: a = np.append(a, 0)
        if len(b) == 2: b = np.append(b, 0)
        
        E_phasor = E0 * (a - 1j * b)
        k_hat = beta_vec / np.linalg.norm(beta_vec)
    else:
        # Vector phasor mode
        E_phasor = np.array(arg1, dtype=complex).flatten()
        if len(E_phasor) == 2:
            E_phasor = np.append(E_phasor, 0)
        
        beta_or_k = np.array(arg2, dtype=float).flatten() if arg2 is not None else np.array([0, 0, 1])
        eta = arg3 if arg3 is not None else 377
        
        if abs(np.linalg.norm(beta_or_k) - 1) < 0.01:
            k_hat = beta_or_k
        else:
            k_hat = beta_or_k / np.linalg.norm(beta_or_k)
    
    # H-field phasor
    H_phasor = (1 / eta) * np.cross(k_hat, E_phasor)
    
    # Time-average Poynting vector
    S_avg = 0.5 * np.real(np.cross(E_phasor, np.conj(H_phasor)))
    S_mag = np.linalg.norm(S_avg)
    
    return PoyntingResult(
        E_phasor=E_phasor, H_phasor=H_phasor,
        k_hat=k_hat, eta=eta,
        S_avg=S_avg, S_mag=S_mag
    )


# =============================================================================
# PLANEWAVECHECK - Verify plane wave conditions
# =============================================================================
@dataclass
class PlaneWaveResult:
    """Results from PlaneWaveCheck"""
    is_plane_wave: bool = False
    is_uniform: bool = False
    transverse_E: bool = False
    transverse_H: bool = False
    orthogonal_EH: bool = False
    maxwell_valid: bool = False
    eta_ratio: complex = 0j
    eta_expected: complex = ETA0
    errors: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)


def PlaneWaveCheck(mode: str, E, H, k_or_gamma, eta: float = None) -> PlaneWaveResult:
    """
    Verify if E and H fields form a valid plane wave.
    
    Modes:
        PlaneWaveCheck('full', E, H, k, [eta])      - Full check with k from exp term
        PlaneWaveCheck('maxwell', E0, H0, gamma)    - Maxwell's equations check
        PlaneWaveCheck('basic', E, H, k)            - Basic orthogonality only
    """
    E = np.array(E, dtype=complex).flatten()
    H = np.array(H, dtype=complex).flatten()
    k_or_gamma = np.array(k_or_gamma, dtype=complex).flatten()
    
    if len(E) == 2: E = np.append(E, 0)
    if len(H) == 2: H = np.append(H, 0)
    if len(k_or_gamma) == 2: k_or_gamma = np.append(k_or_gamma, 0)
    
    result = PlaneWaveResult()
    
    mode = mode.lower()
    
    if mode == 'basic':
        return _pwc_basic(E, H, k_or_gamma, result)
    elif mode == 'full':
        eta_val = eta if eta is not None else ETA0
        return _pwc_full(E, H, k_or_gamma, eta_val, result)
    elif mode == 'maxwell':
        return _pwc_maxwell(E, H, k_or_gamma, result)
    else:
        raise ValueError(f"Unknown mode: {mode}")


def _pwc_basic(E, H, k, result):
    k_hat = k / np.linalg.norm(k)
    
    # Check transversality
    E_dot_k = abs(np.dot(E, k_hat))
    H_dot_k = abs(np.dot(H, k_hat))
    scale_E = np.linalg.norm(E)
    scale_H = np.linalg.norm(H)
    
    tol = 1e-6
    result.transverse_E = E_dot_k < tol * scale_E if scale_E > 0 else True
    result.transverse_H = H_dot_k < tol * scale_H if scale_H > 0 else True
    
    # Check E ⊥ H
    E_dot_H = abs(np.dot(E, np.conj(H)))
    result.orthogonal_EH = E_dot_H < tol * scale_E * scale_H if scale_E * scale_H > 0 else True
    
    result.is_plane_wave = result.transverse_E and result.transverse_H and result.orthogonal_EH
    
    return result


def _pwc_full(E, H, k, eta, result):
    result = _pwc_basic(E, H, k, result)
    
    k_hat = k / np.linalg.norm(k)
    
    # Check H = (1/η) * k̂ × E
    H_expected = np.cross(k_hat, E) / eta
    H_error = np.linalg.norm(H - H_expected) / np.linalg.norm(H) if np.linalg.norm(H) > 0 else 0
    
    result.maxwell_valid = H_error < 0.01
    result.eta_expected = eta
    
    # Calculate actual η ratio
    E_mag = np.linalg.norm(E)
    H_mag = np.linalg.norm(H)
    if H_mag > 0:
        result.eta_ratio = E_mag / H_mag
    
    result.is_plane_wave = result.is_plane_wave and result.maxwell_valid
    
    return result


def _pwc_maxwell(E0, H0, gamma, result):
    # Check if gamma is purely imaginary (lossless)
    alpha = np.real(gamma)
    beta = np.imag(gamma)
    
    result.is_uniform = np.linalg.norm(alpha) < 1e-10 * np.linalg.norm(beta) if np.linalg.norm(beta) > 0 else True
    
    gamma_hat = gamma / np.linalg.norm(gamma)
    k_hat = np.imag(gamma_hat) / np.linalg.norm(np.imag(gamma_hat)) if np.linalg.norm(np.imag(gamma_hat)) > 0 else gamma_hat
    
    result = _pwc_basic(E0, H0, np.real(k_hat) + np.imag(k_hat), result)
    
    # Check Maxwell: -γ × E0 = -jωμH0 → γ × E0 ∝ H0
    gamma_cross_E = np.cross(gamma, E0)
    
    # Should be proportional to H0
    if np.linalg.norm(H0) > 0 and np.linalg.norm(gamma_cross_E) > 0:
        ratio = gamma_cross_E / H0
        # All components should have same ratio
        nonzero = np.abs(H0) > 1e-10 * np.max(np.abs(H0))
        if np.any(nonzero):
            ratios = ratio[nonzero]
            spread = np.std(ratios) / np.abs(np.mean(ratios)) if np.abs(np.mean(ratios)) > 0 else 0
            result.maxwell_valid = spread < 0.01
    
    result.is_plane_wave = result.transverse_E and result.transverse_H and result.orthogonal_EH
    
    return result


# =============================================================================
# Convenience function for rect2pol
# =============================================================================
def rect2pol(z: complex) -> Tuple[float, float]:
    """Convert complex number to (magnitude, angle_degrees)"""
    return abs(z), np.degrees(cmath.phase(z))
