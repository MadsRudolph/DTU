"""
EM Tools - Electromagnetic Calculation Library
==============================================

Python equivalent of the MATLAB EM Toolbox.
All functions work with NumPy arrays and complex numbers.

Usage:
    from em_calc import *
    
    result = Medium(4, 10e9)
    result = Polarization([1, -1j, 0])
    result = Fresnel(1, 4, 45)
    result = TLine(50, 100, 0.3)
    
    # NEW: Inverse TLine - find Z_L from VSWR + position
    result = TLine_inverse(Z0=75, VSWR=3.0, z_min=0.1)
    
    # NEW: Geometry library
    L = solenoid_inductance(N=100, A=1e-4, length=0.1)
    C = coax_capacitance(a=1e-3, b=3e-3, length=1.0)
    C = parallel_wire_capacitance(d=0.01, R=1e-3, length=1.0)
    
    # NEW: Wave uniformity check
    result = wave_uniformity(alpha=[0,0,1], beta=[0,0,5])
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
    lambda_: float = 0.0
    up: float = 0.0
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
        Medium('conductor', sigma, freq)       - Good conductor
        Medium('skin', sigma, freq)            - Skin depth only
        Medium('free', freq)                   - Free space
        Medium('tand', eps_r, tan_delta, freq) - From loss tangent
    """
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
        if arg3 is None:
            return _medium_lossless(arg1, arg2)
        else:
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
    
    return MediumResult(
        eps_r=eps_r, mu_r=mu_r, sigma=0, freq=freq, omega=omega,
        tan_delta=0, classification='Lossless',
        gamma=1j * beta, alpha=0, beta=beta,
        lambda_=lambda_, up=up, eta=eta, n=n, skin_depth=float('inf')
    )


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
    AR: float = 1.0
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
        Ex, Ey, phi_x, phi_y = arg2, arg3, arg4, arg5
        Fx = Ex * cmath.exp(1j * np.radians(phi_x))
        Fy = Ey * cmath.exp(1j * np.radians(phi_y))
        F = np.array([Fx, Fy, 0], dtype=complex)
        k_hat = np.array([0, 0, 1.0])
    elif arg2 is not None and arg3 is not None and np.isrealobj(arg1) and np.isrealobj(arg2):
        u = np.array(arg1, dtype=float).flatten()
        v = np.array(arg2, dtype=float).flatten()
        beta = np.array(arg3, dtype=float).flatten()
        if len(u) == 2: u = np.append(u, 0)
        if len(v) == 2: v = np.append(v, 0)
        F = u - 1j * v
        k_hat = beta / np.linalg.norm(beta)
    else:
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
    
    tol = 1e-3
    scale = max(np.linalg.norm(Fr), np.linalg.norm(Fi))
    if scale == 0:
        scale = 1
    
    cross_ri = np.cross(Fr, Fi)
    is_linear = np.linalg.norm(cross_ri) < tol * scale**2
    
    dot_ri = np.dot(Fr, Fi)
    amp_equal = abs(np.linalg.norm(Fr) - np.linalg.norm(Fi)) < tol * scale
    is_circular = (not is_linear) and (abs(dot_ri) < tol * scale**2) and amp_equal
    
    if is_linear:
        handedness = "N/A"
    else:
        hand = np.dot(k_hat, np.cross(Fr, -Fi))
        handedness = "RHCP" if hand > 0 else "LHCP"
    
    if is_linear:
        pol_type = "Linear"
    elif is_circular:
        pol_type = "Circular"
    else:
        pol_type = "Elliptical"
    
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
        Fresnel('snell', n1, n2, theta_i)       - Snell's law
        Fresnel('brewster', eps_r1, eps_r2)     - Brewster angle
        Fresnel('critical', eps_r1, eps_r2)     - Critical angle
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
            return _fresnel_normal(arg1, arg2)
        else:
            pol = arg4 if arg4 is not None else 'both'
            return _fresnel_oblique(arg1, arg2, arg3, pol)


def _fresnel_normal(eps_r1: float, eps_r2: float) -> FresnelResult:
    eta1 = ETA0 / np.sqrt(eps_r1)
    eta2 = ETA0 / np.sqrt(eps_r2)
    n1 = np.sqrt(eps_r1)
    n2 = np.sqrt(eps_r2)
    
    Gamma = (eta2 - eta1) / (eta2 + eta1)
    tau = 2 * eta2 / (eta2 + eta1)
    R = abs(Gamma) ** 2
    T = 1 - R
    
    return FresnelResult(
        eps_r1=eps_r1, eps_r2=eps_r2,
        eta1=eta1, eta2=eta2, n1=n1, n2=n2,
        theta_i=0, theta_t=0,
        Gamma=Gamma, Gamma_TE=Gamma, Gamma_TM=Gamma,
        tau=tau, tau_TE=tau, tau_TM=tau,
        R=R, R_TE=R, R_TM=R, T=T, T_TE=T, T_TM=T
    )


def _fresnel_oblique(eps_r1: float, eps_r2: float, theta_i_deg: float, pol: str = 'both') -> FresnelResult:
    eta1 = ETA0 / np.sqrt(eps_r1)
    eta2 = ETA0 / np.sqrt(eps_r2)
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
    
    Gamma_TE = (eta2 * np.cos(theta_i) - eta1 * np.cos(theta_t)) / \
               (eta2 * np.cos(theta_i) + eta1 * np.cos(theta_t))
    tau_TE = 2 * eta2 * np.cos(theta_i) / (eta2 * np.cos(theta_i) + eta1 * np.cos(theta_t))
    
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
        result.TIR = True
    else:
        result.theta_critical = float('nan')
        result.TIR = False
    
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
        else:
            raise ValueError(f"Unknown mode: {mode}")
    else:
        return _tline_basic(arg1, arg2, arg3)


def _tline_basic(Z0: float, ZL: complex, len_lambda: float) -> TLineResult:
    beta_l = 2 * np.pi * len_lambda
    
    Gamma_L = (ZL - Z0) / (ZL + Z0)
    Gamma_in = Gamma_L * cmath.exp(-1j * 2 * beta_l)
    
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


def _tline_quarter_wave(Z_source: float, Z_load: float) -> TLineResult:
    Z_qw = np.sqrt(Z_source * Z_load)
    return TLineResult(Z0=Z_qw, ZL=Z_load, len_lambda=0.25)


def _tline_stub(Z_target: complex, Z0: float, stub_type: str = 'both') -> TLineResult:
    X = Z_target.imag
    result = TLineResult(Z0=Z0, ZL=Z_target)
    
    if stub_type.lower() in ['short', 'both']:
        if X >= 0:
            result.short_len = np.arctan(X / Z0) / (2 * np.pi)
        else:
            result.short_len = (np.pi + np.arctan(X / Z0)) / (2 * np.pi)
    
    if stub_type.lower() in ['open', 'both']:
        if X <= 0:
            result.open_len = -np.arctan(Z0 / X) / (2 * np.pi) if X != 0 else 0.25
        else:
            result.open_len = (np.pi - np.arctan(Z0 / X)) / (2 * np.pi)
    
    return result


# =============================================================================
# NEW FEATURE 1: INVERSE TLINE SOLVER
# =============================================================================
@dataclass
class TLineInverseResult:
    """Results from inverse TLine calculation (find Z_L from VSWR + position)"""
    Z0: float = 50.0
    ZL: complex = 50.0
    VSWR: float = 1.0
    Gamma_mag: float = 0.0
    Gamma_angle_deg: float = 0.0
    Gamma_L: complex = 0j
    z_vmin: float = 0.0
    z_vmax: float = 0.0
    input_type: str = ""
    position_type: str = ""


def TLine_inverse(Z0: float, 
                  VSWR: float = None, 
                  Gamma_mag: float = None,
                  Gamma_dB: float = None,
                  z_min: float = None, 
                  z_max: float = None) -> TLineInverseResult:
    """
    Inverse TLine solver: Find Z_L from VSWR (or |Γ|) and voltage min/max position.
    
    This solves the common exam problem type where you're given:
      - VSWR (or |Γ| or Γ in dB)
      - Position of voltage minimum or maximum (in wavelengths)
      - Z0 of the line
    And you need to find Z_L.
    
    Parameters:
        Z0: Characteristic impedance [Ω]
        VSWR: Voltage standing wave ratio (provide ONE of VSWR, Gamma_mag, Gamma_dB)
        Gamma_mag: |Γ| magnitude directly
        Gamma_dB: Γ in dB (20*log10|Γ|)
        z_min: Position of voltage MINIMUM from load [wavelengths]
        z_max: Position of voltage MAXIMUM from load [wavelengths]
    
    Returns:
        TLineInverseResult with ZL, Gamma_L, etc.
    
    Theory:
        From VSWR: |Γ| = (VSWR - 1) / (VSWR + 1)
        From Γ_dB: |Γ| = 10^(Γ_dB/20)
        
        At voltage MINIMUM: ∠Γ_L = π + 4π·z_min
        At voltage MAXIMUM: ∠Γ_L = 4π·z_max
        
        Then: Z_L = Z0 · (1 + Γ_L) / (1 - Γ_L)
    
    Examples:
        # Given VSWR=3 and first voltage minimum at z=0.1λ from load
        result = TLine_inverse(Z0=75, VSWR=3.0, z_min=0.1)
        
        # Given |Γ|=0.5 and first voltage maximum at z=0.2λ
        result = TLine_inverse(Z0=50, Gamma_mag=0.5, z_max=0.2)
        
        # Given Γ=-6dB and z_min=0.15λ
        result = TLine_inverse(Z0=75, Gamma_dB=-6, z_min=0.15)
    """
    result = TLineInverseResult(Z0=Z0)
    
    # Step 1: Determine |Γ| from input
    input_count = sum(x is not None for x in [VSWR, Gamma_mag, Gamma_dB])
    if input_count != 1:
        raise ValueError("Provide exactly ONE of: VSWR, Gamma_mag, or Gamma_dB")
    
    if VSWR is not None:
        if VSWR < 1:
            raise ValueError("VSWR must be >= 1")
        mag_Gamma = (VSWR - 1) / (VSWR + 1)
        result.VSWR = VSWR
        result.input_type = "VSWR"
    elif Gamma_mag is not None:
        if Gamma_mag < 0 or Gamma_mag > 1:
            raise ValueError("|Γ| must be between 0 and 1")
        mag_Gamma = Gamma_mag
        result.VSWR = (1 + mag_Gamma) / (1 - mag_Gamma) if mag_Gamma < 1 else float('inf')
        result.input_type = "Gamma_mag"
    else:
        mag_Gamma = 10 ** (Gamma_dB / 20)
        if mag_Gamma > 1:
            raise ValueError("Γ_dB would give |Γ| > 1, check sign")
        result.VSWR = (1 + mag_Gamma) / (1 - mag_Gamma) if mag_Gamma < 1 else float('inf')
        result.input_type = "Gamma_dB"
    
    result.Gamma_mag = mag_Gamma
    
    # Step 2: Determine ∠Γ from position
    position_count = sum(x is not None for x in [z_min, z_max])
    if position_count != 1:
        raise ValueError("Provide exactly ONE of: z_min or z_max")
    
    if z_min is not None:
        angle_Gamma = np.pi + 4 * np.pi * z_min
        result.z_vmin = z_min
        result.z_vmax = (z_min + 0.25) % 0.5
        result.position_type = "v_min"
    else:
        angle_Gamma = 4 * np.pi * z_max
        result.z_vmax = z_max
        result.z_vmin = (z_max + 0.25) % 0.5
        result.position_type = "v_max"
    
    angle_Gamma = np.arctan2(np.sin(angle_Gamma), np.cos(angle_Gamma))
    result.Gamma_angle_deg = np.degrees(angle_Gamma)
    
    # Step 3: Form Γ_L and calculate Z_L
    Gamma_L = mag_Gamma * cmath.exp(1j * angle_Gamma)
    result.Gamma_L = Gamma_L
    
    ZL = Z0 * (1 + Gamma_L) / (1 - Gamma_L)
    result.ZL = ZL
    
    return result


# =============================================================================
# NEW FEATURE 2: GEOMETRY & COMPONENT LIBRARY
# =============================================================================
@dataclass
class InductanceResult:
    """Results from inductance calculation"""
    L: float = 0.0
    L_uH: float = 0.0
    L_nH: float = 0.0
    geometry: str = ""
    N: int = 0
    A: float = 0.0
    length: float = 0.0
    mu_r: float = 1.0


def solenoid_inductance(N: int, A: float = None, length: float = None,
                        radius: float = None, mu_r: float = 1.0) -> InductanceResult:
    """
    Calculate self-inductance of a solenoid.
    
    Formula: L = μ₀·μᵣ·N²·A/ℓ
    
    Parameters:
        N: Number of turns
        A: Cross-sectional area [m²] (or provide radius)
        length: Length of solenoid [m]
        radius: Radius of solenoid [m] (alternative to A)
        mu_r: Relative permeability of core (default 1 for air)
    
    Examples:
        L = solenoid_inductance(N=100, A=1e-4, length=0.1)
        L = solenoid_inductance(N=100, A=1e-4, length=0.1, mu_r=1000)
        L = solenoid_inductance(N=50, radius=0.01, length=0.05)
    """
    if A is None and radius is None:
        raise ValueError("Provide either A (area) or radius")
    if A is None:
        A = np.pi * radius**2
    if length is None or length <= 0:
        raise ValueError("Length must be positive")
    if N <= 0:
        raise ValueError("Number of turns must be positive")
    
    mu = MU0 * mu_r
    L = mu * N**2 * A / length
    
    return InductanceResult(
        L=L, L_uH=L * 1e6, L_nH=L * 1e9,
        geometry="solenoid", N=N, A=A, length=length, mu_r=mu_r
    )


@dataclass 
class CapacitanceResult:
    """Results from capacitance calculation"""
    C: float = 0.0
    C_pF: float = 0.0
    C_nF: float = 0.0
    geometry: str = ""
    length: float = 0.0
    eps_r: float = 1.0
    inner_radius: float = 0.0
    outer_radius: float = 0.0
    wire_separation: float = 0.0
    wire_radius: float = 0.0


def coax_capacitance(a: float, b: float, length: float, eps_r: float = 1.0) -> CapacitanceResult:
    """
    Calculate capacitance of coaxial cable.
    
    Formula: C = 2π·ε₀·εᵣ·ℓ / ln(b/a)
    
    Parameters:
        a: Inner conductor radius [m]
        b: Outer conductor radius [m]
        length: Length of cable [m]
        eps_r: Relative permittivity (default 1)
    
    Example:
        C = coax_capacitance(a=1e-3, b=3e-3, length=1.0, eps_r=2.1)
    """
    if a <= 0 or b <= 0:
        raise ValueError("Radii must be positive")
    if a >= b:
        raise ValueError("Inner radius a must be less than outer radius b")
    if length <= 0:
        raise ValueError("Length must be positive")
    
    eps = EPS0 * eps_r
    C = 2 * np.pi * eps * length / np.log(b / a)
    
    return CapacitanceResult(
        C=C, C_pF=C * 1e12, C_nF=C * 1e9,
        geometry="coaxial", length=length, eps_r=eps_r,
        inner_radius=a, outer_radius=b
    )


def parallel_wire_capacitance(d: float, R: float, length: float, eps_r: float = 1.0) -> CapacitanceResult:
    """
    Calculate capacitance between two parallel wires.
    
    Formula: C = π·ε₀·εᵣ·ℓ / arccosh(d/(2R))
    
    Parameters:
        d: Center-to-center separation [m]
        R: Radius of each wire [m]
        length: Length [m]
        eps_r: Relative permittivity (default 1)
    
    Example:
        C = parallel_wire_capacitance(d=0.01, R=1e-3, length=1.0)
    """
    if d <= 0 or R <= 0:
        raise ValueError("Dimensions must be positive")
    if d <= 2*R:
        raise ValueError("Separation d must be greater than 2R")
    if length <= 0:
        raise ValueError("Length must be positive")
    
    eps = EPS0 * eps_r
    x = d / (2 * R)
    arccosh_x = np.log(x + np.sqrt(x**2 - 1))
    
    C = np.pi * eps * length / arccosh_x
    
    return CapacitanceResult(
        C=C, C_pF=C * 1e12, C_nF=C * 1e9,
        geometry="parallel_wire", length=length, eps_r=eps_r,
        wire_separation=d, wire_radius=R
    )


def parallel_plate_capacitance(A: float, d: float, eps_r: float = 1.0) -> CapacitanceResult:
    """
    Calculate capacitance of parallel plate capacitor.
    
    Formula: C = ε₀·εᵣ·A/d
    
    Parameters:
        A: Plate area [m²]
        d: Plate separation [m]
        eps_r: Relative permittivity (default 1)
    """
    if A <= 0 or d <= 0:
        raise ValueError("Area and separation must be positive")
    
    eps = EPS0 * eps_r
    C = eps * A / d
    
    return CapacitanceResult(
        C=C, C_pF=C * 1e12, C_nF=C * 1e9,
        geometry="parallel_plate", eps_r=eps_r
    )


# =============================================================================
# NEW FEATURE 3: WAVE UNIFORMITY ANALYZER
# =============================================================================
@dataclass
class WaveUniformityResult:
    """Results from wave uniformity analysis"""
    is_uniform: bool = False
    classification: str = ""
    alpha: np.ndarray = field(default_factory=lambda: np.zeros(3))
    beta: np.ndarray = field(default_factory=lambda: np.zeros(3))
    alpha_mag: float = 0.0
    beta_mag: float = 0.0
    cross_product: np.ndarray = field(default_factory=lambda: np.zeros(3))
    cross_magnitude: float = 0.0
    angle_between_deg: float = 0.0
    gamma: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=complex))
    info: str = ""


def wave_uniformity(alpha=None, beta=None, gamma=None, tol: float = 1e-6) -> WaveUniformityResult:
    """
    Analyze wave uniformity by checking if α ∥ β.
    
    A plane wave has propagation factor exp(-γ·r) where γ = α + jβ.
    
    Classifications:
        - UNIFORM wave: α ∥ β (parallel) or α = 0 (lossless)
        - NON-UNIFORM wave: α not parallel to β
    
    Parameters:
        alpha: Attenuation vector [αx, αy, αz] Np/m
        beta: Phase vector [βx, βy, βz] rad/m
        gamma: Complex propagation vector (alternative to alpha+beta)
        tol: Tolerance for parallelism check
    
    Examples:
        # Uniform wave (α parallel to β)
        result = wave_uniformity(alpha=[0, 0, 1], beta=[0, 0, 5])
        
        # Non-uniform wave (α perpendicular to β)
        result = wave_uniformity(alpha=[1, 0, 0], beta=[0, 0, 5])
        
        # From complex gamma
        result = wave_uniformity(gamma=[0, 0, 1+5j])
    """
    result = WaveUniformityResult()
    
    if gamma is not None:
        gamma = np.array(gamma, dtype=complex)
        alpha = np.real(gamma)
        beta = np.imag(gamma)
    elif alpha is not None and beta is not None:
        alpha = np.array(alpha, dtype=float)
        beta = np.array(beta, dtype=float)
        gamma = alpha + 1j * beta
    else:
        raise ValueError("Provide either (alpha, beta) OR gamma")
    
    if len(alpha) == 2:
        alpha = np.append(alpha, 0)
        beta = np.append(beta, 0)
        gamma = np.append(gamma, 0)
    
    result.alpha = alpha
    result.beta = beta
    result.gamma = gamma
    result.alpha_mag = np.linalg.norm(alpha)
    result.beta_mag = np.linalg.norm(beta)
    
    cross = np.cross(alpha, beta)
    result.cross_product = cross
    result.cross_magnitude = np.linalg.norm(cross)
    
    if result.alpha_mag > tol and result.beta_mag > tol:
        cos_angle = np.dot(alpha, beta) / (result.alpha_mag * result.beta_mag)
        cos_angle = np.clip(cos_angle, -1, 1)
        result.angle_between_deg = np.degrees(np.arccos(abs(cos_angle)))
    else:
        result.angle_between_deg = 0.0
    
    if result.alpha_mag < tol:
        result.is_uniform = True
        result.classification = "Lossless (Uniform)"
        result.info = "No attenuation (α ≈ 0), wave is inherently uniform."
    elif result.beta_mag < tol:
        result.is_uniform = True
        result.classification = "Evanescent (Uniform)"
        result.info = "No propagation (β ≈ 0), pure exponential decay."
    else:
        scale = result.alpha_mag * result.beta_mag
        normalized_cross = result.cross_magnitude / scale if scale > 0 else 0
        
        if normalized_cross < tol:
            result.is_uniform = True
            result.classification = "Uniform"
            result.info = "α ∥ β: Wave decays and propagates in same direction."
        else:
            result.is_uniform = False
            result.classification = "Non-uniform"
            result.info = f"α not ∥ β (angle ≈ {result.angle_between_deg:.1f}°)"
    
    return result


# =============================================================================
# STUBMATCH - Stub matching calculator
# =============================================================================
@dataclass
class StubMatchResult:
    """Results from StubMatch calculation"""
    ZL: complex = 0j
    Z0: float = 50.0
    stub_type: str = 'short'
    d: float = 0.0
    l: float = 0.0
    d_alt: float = float('nan')
    l_alt: float = float('nan')
    lambda_: Optional[float] = None
    d_mm: Optional[float] = None
    l_mm: Optional[float] = None


def StubMatch(ZL: complex, Z0: float, stub_type: str = 'short', 
              lambda_: float = None) -> StubMatchResult:
    """
    Single-stub matching calculator using analytical solution.
    
    Solves for d where Re(Y_in) = Y0, then calculates stub length
    to cancel the susceptance.
    """
    zL = ZL / Z0
    yL = 1 / zL
    gL = yL.real
    bL = yL.imag
    
    beta = 2 * np.pi
    d_solutions = []
    l_solutions = []
    
    # Analytical solution for d where Re(y_in) = 1
    # y_in = (yL + jt) / (1 + j*yL*t) where t = tan(βd)
    # Setting Re(y_in) = 1 gives quadratic in t:
    # (|yL|² - gL)*t² - 2*bL*t + (1 - gL) = 0
    
    yL_mag_sq = gL**2 + bL**2
    
    A = yL_mag_sq - gL
    B = -2 * bL
    C = 1 - gL
    
    # Handle special case: gL = 1 (already matched conductance)
    if abs(A) < 1e-10:
        if abs(B) > 1e-10:
            t_values = [-C / B]
        else:
            t_values = []
    else:
        discriminant = B**2 - 4*A*C
        if discriminant >= 0:
            sqrt_disc = np.sqrt(discriminant)
            t1 = (-B + sqrt_disc) / (2*A)
            t2 = (-B - sqrt_disc) / (2*A)
            t_values = [t1, t2]
        else:
            t_values = []
    
    # Convert t = tan(βd) to d
    for t in t_values:
        d = np.arctan(t) / beta
        # Ensure d is in [0, 0.5)
        d = d % 0.5
        if d < 0:
            d += 0.5
        
        d_solutions.append(d)
        
        # Calculate y_in at this d
        y_in = (yL + 1j * t) / (1 + 1j * yL * t)
        b_in = y_in.imag  # Susceptance to cancel
        
        # Stub susceptance needed: b_stub = -b_in
        b_stub = -b_in
        
        # Calculate stub length
        if stub_type.lower() == 'short':
            # Short stub: Y_stub = -j*cot(βℓ)/Z0 → b_stub = -cot(βℓ)
            # So cot(βℓ) = -b_stub → tan(βℓ) = -1/b_stub
            if abs(b_stub) < 1e-10:
                l = 0.25  # 90 degrees for zero susceptance
            else:
                l = np.arctan(-1 / b_stub) / beta
        else:
            # Open stub: Y_stub = j*tan(βℓ)/Z0 → b_stub = tan(βℓ)
            l = np.arctan(b_stub) / beta
        
        # Ensure l is in (0, 0.5]
        l = l % 0.5
        if l < 0.001:
            l += 0.5
        
        l_solutions.append(l)
    
    # Sort solutions by d (closest to load first)
    if len(d_solutions) >= 2:
        pairs = sorted(zip(d_solutions, l_solutions), key=lambda x: x[0])
        d_solutions = [p[0] for p in pairs]
        l_solutions = [p[1] for p in pairs]
    
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
            if lambda_ is not None:
                result.d_alt_mm = result.d_alt * lambda_ * 1000
                result.l_alt_mm = result.l_alt * lambda_ * 1000
    
    return result


# =============================================================================
# POYNTING_PW - Poynting vector and H-field
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
    """
    if isinstance(arg1, str) and arg1.lower() == 'time':
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
        E_phasor = np.array(arg1, dtype=complex).flatten()
        if len(E_phasor) == 2:
            E_phasor = np.append(E_phasor, 0)
        
        beta_or_k = np.array(arg2, dtype=float).flatten() if arg2 is not None else np.array([0, 0, 1])
        eta = arg3 if arg3 is not None else 377
        
        if abs(np.linalg.norm(beta_or_k) - 1) < 0.01:
            k_hat = beta_or_k
        else:
            k_hat = beta_or_k / np.linalg.norm(beta_or_k)
    
    H_phasor = (1 / eta) * np.cross(k_hat, E_phasor)
    S_avg = 0.5 * np.real(np.cross(E_phasor, np.conj(H_phasor)))
    S_mag = np.linalg.norm(S_avg)
    
    return PoyntingResult(
        E_phasor=E_phasor, H_phasor=H_phasor,
        k_hat=k_hat, eta=eta, S_avg=S_avg, S_mag=S_mag
    )


# =============================================================================
# PLANEWAVECHECK
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
    """Verify if E and H fields form a valid plane wave."""
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
    tol = 1e-6
    
    E_dot_k = abs(np.dot(E, k_hat))
    H_dot_k = abs(np.dot(H, k_hat))
    scale_E = np.linalg.norm(E)
    scale_H = np.linalg.norm(H)
    
    result.transverse_E = E_dot_k < tol * scale_E if scale_E > 0 else True
    result.transverse_H = H_dot_k < tol * scale_H if scale_H > 0 else True
    
    E_dot_H = abs(np.dot(E, np.conj(H)))
    result.orthogonal_EH = E_dot_H < tol * scale_E * scale_H if scale_E * scale_H > 0 else True
    
    result.is_plane_wave = result.transverse_E and result.transverse_H and result.orthogonal_EH
    return result


def _pwc_full(E, H, k, eta, result):
    result = _pwc_basic(E, H, k, result)
    k_hat = k / np.linalg.norm(k)
    
    H_expected = np.cross(k_hat, E) / eta
    H_error = np.linalg.norm(H - H_expected) / np.linalg.norm(H) if np.linalg.norm(H) > 0 else 0
    
    result.maxwell_valid = H_error < 0.01
    result.eta_expected = eta
    
    E_mag = np.linalg.norm(E)
    H_mag = np.linalg.norm(H)
    if H_mag > 0:
        result.eta_ratio = E_mag / H_mag
    
    result.is_plane_wave = result.is_plane_wave and result.maxwell_valid
    return result


def _pwc_maxwell(E0, H0, gamma, result):
    alpha = np.real(gamma)
    beta = np.imag(gamma)
    
    result.is_uniform = np.linalg.norm(alpha) < 1e-10 * np.linalg.norm(beta) if np.linalg.norm(beta) > 0 else True
    
    gamma_hat = gamma / np.linalg.norm(gamma)
    k_hat = np.imag(gamma_hat) / np.linalg.norm(np.imag(gamma_hat)) if np.linalg.norm(np.imag(gamma_hat)) > 0 else gamma_hat
    
    result = _pwc_basic(E0, H0, np.real(k_hat) + np.imag(k_hat), result)
    
    gamma_cross_E = np.cross(gamma, E0)
    
    if np.linalg.norm(H0) > 0 and np.linalg.norm(gamma_cross_E) > 0:
        ratio = gamma_cross_E / H0
        nonzero = np.abs(H0) > 1e-10 * np.max(np.abs(H0))
        if np.any(nonzero):
            ratios = ratio[nonzero]
            spread = np.std(ratios) / np.abs(np.mean(ratios)) if np.abs(np.mean(ratios)) > 0 else 0
            result.maxwell_valid = spread < 0.01
    
    result.is_plane_wave = result.transverse_E and result.transverse_H and result.orthogonal_EH
    return result


# =============================================================================
# Convenience function
# =============================================================================
def rect2pol(z: complex) -> Tuple[float, float]:
    """Convert complex number to (magnitude, angle_degrees)"""
    return abs(z), np.degrees(cmath.phase(z))
