#!/usr/bin/env python3
"""
EM Assistant - Interactive Electromagnetic Problem Solver
=========================================================

Run from terminal:
    python em_assistant.py

This guides you through solving EM problems using the em_tools library.
"""

import sys
import os
import cmath
import numpy as np

# Import the EM tools
try:
    from em_calc import *
except ImportError:
    # If em_calc.py is in the same directory
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from em_calc import *


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_welcome():
    """Print welcome banner"""
    print()
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║                                                          ║")
    print("  ║            ⚡ EM TOOLBOX ASSISTANT ⚡                    ║")
    print("  ║                                                          ║")
    print("  ║     Interactive Electromagnetic Problem Solver           ║")
    print("  ║              Python Edition                              ║")
    print("  ║                                                          ║")
    print("  ╚══════════════════════════════════════════════════════════╝")
    print()


def print_menu():
    """Print main menu"""
    print()
    print("  ┌────────────────────────────────────────┐")
    print("  │         WHAT DO YOU NEED HELP WITH?    │")
    print("  ├────────────────────────────────────────┤")
    print("  │  1. Plane Wave Verification            │")
    print("  │  2. Polarization Analysis              │")
    print("  │  3. Fresnel (Reflection/Transmission)  │")
    print("  │  4. Medium Properties (η, β, λ, etc.)  │")
    print("  │  5. Transmission Lines                 │")
    print("  │  6. Stub Matching                      │")
    print("  │  7. Poynting Vector / H-field          │")
    print("  │  8. Magnetic Field (Infinite Wire)     │")
    print("  │  9. Coulomb Force                      │")
    print("  │                                        │")
    print("  │  0. Exit                               │")
    print("  └────────────────────────────────────────┘")
    print()


def get_number(prompt, min_val=None, max_val=None, allow_complex=False):
    """Get a number from user input"""
    while True:
        try:
            raw = input(prompt).strip()
            if not raw:
                return 0
            
            # Handle complex numbers
            raw = raw.replace('i', 'j').replace('J', 'j')
            # Handle cases like "5j" or "-3j"
            if raw.endswith('j') and not any(c in raw[:-1] for c in ['+', '-', '*']):
                if raw == 'j':
                    raw = '1j'
                elif raw == '-j':
                    raw = '-1j'
            
            val = complex(eval(raw.replace('^', '**')))
            
            if not allow_complex and val.imag != 0:
                print("    ⚠ Please enter a real number.")
                continue
            
            if not allow_complex:
                val = val.real
            
            if min_val is not None and val.real < min_val:
                print(f"    ⚠ Value must be >= {min_val}")
                continue
            if max_val is not None and val.real > max_val:
                print(f"    ⚠ Value must be <= {max_val}")
                continue
            
            return val
        except Exception as e:
            print(f"    ⚠ Invalid input. Try: 5, -3, 1+2j, 5j, 1e-9")


def get_complex(prompt):
    """Get a complex number from user input"""
    return get_number(prompt, allow_complex=True)


def get_yes_no(prompt):
    """Get yes/no response"""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no', '']:
            return False
        print("    ⚠ Please enter y or n")


def format_complex(z, precision=4):
    """Format complex number for display"""
    if abs(z.imag) < 1e-10:
        return f"{z.real:.{precision}f}"
    elif abs(z.real) < 1e-10:
        if z.imag >= 0:
            return f"j{z.imag:.{precision}f}"
        else:
            return f"-j{abs(z.imag):.{precision}f}"
    else:
        if z.imag >= 0:
            return f"{z.real:.{precision}f} + j{z.imag:.{precision}f}"
        else:
            return f"{z.real:.{precision}f} - j{abs(z.imag):.{precision}f}"


def format_vector(v, precision=4):
    """Format a vector for display"""
    parts = []
    for x in v:
        if isinstance(x, complex) or (hasattr(x, 'imag') and x.imag != 0):
            parts.append(format_complex(complex(x), precision))
        else:
            parts.append(f"{float(x.real if hasattr(x, 'real') else x):.{precision}f}")
    return f"[{'; '.join(parts)}]"


# =============================================================================
# TOPIC HANDLERS
# =============================================================================

def handle_plane_wave():
    """Handle plane wave verification"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       PLANE WAVE VERIFICATION")
    print("  ═══════════════════════════════════════════")
    print()
    print("  What format is your problem?")
    print()
    print("    1. exp(-j(ax + by + cz)) in field expression")
    print("       (Extract k from phase term)")
    print()
    print("    2. γ = [γx; γy; γz] given separately")
    print("       (Complex propagation vector)")
    print()
    
    fmt = int(get_number("  Enter format (1 or 2): ", 1, 2))
    
    if fmt == 1:
        # Full mode
        print("\n  --- Enter E-field phasor components ---")
        Ex = get_complex("  Ex (e.g., 0 or 5 or 1j*2): ")
        Ey = get_complex("  Ey: ")
        Ez = get_complex("  Ez: ")
        E = [Ex, Ey, Ez]
        
        print("\n  --- Enter H-field phasor components ---")
        Hx = get_complex("  Hx: ")
        Hy = get_complex("  Hy: ")
        Hz = get_complex("  Hz: ")
        H = [Hx, Hy, Hz]
        
        print("\n  --- Enter k from phase term exp(-j(kx·x + ky·y + kz·z)) ---")
        kx = get_number("  kx: ")
        ky = get_number("  ky: ")
        kz = get_number("  kz: ")
        k = [kx, ky, kz]
        
        print("\n  Use custom η? (default is 377 Ω for free space)")
        if get_yes_no("  Custom η? (y/n): "):
            eta = get_number("  Enter η [Ω]: ", 0)
        else:
            eta = 377
        
        print(f"\n  Calling: PlaneWaveCheck('full', E, H, k, {eta})")
        result = PlaneWaveCheck('full', E, H, k, eta)
        
    else:
        # Maxwell mode
        print("\n  --- Enter E₀ phasor components ---")
        Ex = get_complex("  E0x (e.g., 2 or 1j*5): ")
        Ey = get_complex("  E0y: ")
        Ez = get_complex("  E0z: ")
        E0 = [Ex, Ey, Ez]
        
        print("\n  --- Enter H₀ phasor components ---")
        print("  (Remember to convert mA/m to A/m if needed)")
        Hx = get_complex("  H0x: ")
        Hy = get_complex("  H0y: ")
        Hz = get_complex("  H0z: ")
        H0 = [Hx, Hy, Hz]
        
        print("\n  --- Enter γ (complex propagation vector) ---")
        print("  Example: γ = j3 in z → γz = 1j*3")
        gx = get_complex("  γx: ")
        gy = get_complex("  γy: ")
        gz = get_complex("  γz: ")
        gamma = [gx, gy, gz]
        
        print("\n  Calling: PlaneWaveCheck('maxwell', E0, H0, gamma)")
        result = PlaneWaveCheck('maxwell', E0, H0, gamma)
    
    # Display results
    print()
    print("  ═══════════════════════════════════════════")
    print("       RESULT")
    print("  ═══════════════════════════════════════════")
    print(f"  Is Plane Wave: {'✓ YES' if result.is_plane_wave else '✗ NO'}")
    print(f"  E ⊥ k: {'✓' if result.transverse_E else '✗'}")
    print(f"  H ⊥ k: {'✓' if result.transverse_H else '✗'}")
    print(f"  E ⊥ H: {'✓' if result.orthogonal_EH else '✗'}")
    if hasattr(result, 'maxwell_valid'):
        print(f"  Maxwell Valid: {'✓' if result.maxwell_valid else '✗'}")
    if result.eta_ratio != 0:
        print(f"  η ratio |E|/|H|: {abs(result.eta_ratio):.2f} Ω")
    print("  ═══════════════════════════════════════════")


def handle_polarization():
    """Handle polarization analysis"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       POLARIZATION ANALYSIS")
    print("  ═══════════════════════════════════════════")
    print()
    print("  What format is your E-field?")
    print()
    print("    1. Complex phasor: E = [Ex; Ey; Ez]")
    print("    2. Amplitude/Phase: Ex∠φx, Ey∠φy")
    print("    3. Time-domain: u·cos + v·sin")
    print()
    
    fmt = int(get_number("  Enter format (1-3): ", 1, 3))
    
    if fmt == 1:
        print("\n  --- Enter E-field phasor components ---")
        print("  Examples: 1, -1j, 1+1j, 1j*2")
        Ex = get_complex("  Ex: ")
        Ey = get_complex("  Ey: ")
        Ez = get_complex("  Ez: ")
        E = [Ex, Ey, Ez]
        
        print("\n  --- Enter propagation direction k̂ ---")
        print("  Default is +z: [0; 0; 1]")
        if get_yes_no("  Use default +z? (y/n): "):
            k_hat = [0, 0, 1]
        else:
            kx = get_number("  k̂x: ")
            ky = get_number("  k̂y: ")
            kz = get_number("  k̂z: ")
            k_hat = [kx, ky, kz]
        
        print(f"\n  Calling: Polarization({format_vector(E)}, {k_hat})")
        result = Polarization(E, k_hat)
        
    elif fmt == 2:
        print("\n  --- Enter amplitudes and phases ---")
        Ex = get_number("  |Ex| [V/m]: ", 0)
        Ey = get_number("  |Ey| [V/m]: ", 0)
        phi_x = get_number("  φx [degrees]: ")
        phi_y = get_number("  φy [degrees]: ")
        
        print(f"\n  Calling: Polarization('ap', {Ex}, {Ey}, {phi_x}, {phi_y})")
        result = Polarization('ap', Ex, Ey, phi_x, phi_y)
        
    else:
        print("\n  --- Enter u vector (cos coefficient) ---")
        ux = get_number("  ux: ")
        uy = get_number("  uy: ")
        uz = get_number("  uz: ")
        u = [ux, uy, uz]
        
        print("\n  --- Enter v vector (sin coefficient) ---")
        vx = get_number("  vx: ")
        vy = get_number("  vy: ")
        vz = get_number("  vz: ")
        v = [vx, vy, vz]
        
        print("\n  --- Enter β vector ---")
        bx = get_number("  βx: ")
        by = get_number("  βy: ")
        bz = get_number("  βz: ")
        beta = [bx, by, bz]
        
        print(f"\n  Calling: Polarization({u}, {v}, {beta})")
        result = Polarization(u, v, beta)
    
    # Display results
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT")
    print("  ════════════════════════════════════════")
    print(f"  Type:        {result.type}")
    print(f"  Handedness:  {result.handedness}")
    print("  ────────────────────────────────────────")
    if result.AR == float('inf'):
        print("  Axial Ratio: ∞ (Linear)")
    elif result.AR < 1.001:
        print("  Axial Ratio: 1.000 (0.00 dB) - Circular")
    else:
        print(f"  Axial Ratio: {result.AR:.4f} ({result.AR_dB:.2f} dB)")
    print(f"  Major axis:  {result.major:.4f}")
    print(f"  Minor axis:  {result.minor:.4f}")
    print(f"  Tilt angle:  {result.tilt_deg:.2f}°")
    print("  ════════════════════════════════════════")


def handle_fresnel():
    """Handle Fresnel calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       FRESNEL - REFLECTION/TRANSMISSION")
    print("  ═══════════════════════════════════════════")
    print()
    print("  What do you need?")
    print()
    print("    1. Normal incidence (θ = 0°)")
    print("    2. Oblique incidence (θ ≠ 0°)")
    print("    3. Transmitted angle (Snell's law)")
    print("    4. Brewster angle")
    print("    5. Critical angle (TIR)")
    print()
    
    mode = int(get_number("  Enter choice (1-5): ", 1, 5))
    
    if mode == 1:
        print("\n  --- Enter material properties ---")
        eps1 = get_number("  εr1 (incident medium): ", 0.1)
        eps2 = get_number("  εr2 (second medium): ", 0.1)
        
        print(f"\n  Calling: Fresnel({eps1}, {eps2})")
        result = Fresnel(eps1, eps2)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - NORMAL INCIDENCE")
        print("  ════════════════════════════════════════")
        print(f"  η₁ = {result.eta1:.2f} Ω")
        print(f"  η₂ = {result.eta2:.2f} Ω")
        print(f"  n₁ = {result.n1:.4f}, n₂ = {result.n2:.4f}")
        print("  ────────────────────────────────────────")
        print(f"  Γ = {format_complex(result.Gamma)}")
        print(f"  |Γ| = {abs(result.Gamma):.4f}")
        print(f"  τ = {result.tau:.4f}")
        print("  ────────────────────────────────────────")
        print(f"  R (reflected power) = {result.R:.4f} ({result.R*100:.2f}%)")
        print(f"  T (transmitted power) = {result.T:.4f} ({result.T*100:.2f}%)")
        print("  ════════════════════════════════════════")
        
    elif mode == 2:
        print("\n  --- Enter material properties ---")
        eps1 = get_number("  εr1 (incident medium): ", 0.1)
        eps2 = get_number("  εr2 (second medium): ", 0.1)
        theta = get_number("  θi [degrees]: ", 0, 90)
        
        print(f"\n  Calling: Fresnel({eps1}, {eps2}, {theta})")
        result = Fresnel(eps1, eps2, theta)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - OBLIQUE INCIDENCE")
        print("  ════════════════════════════════════════")
        print(f"  θᵢ = {result.theta_i:.2f}°")
        if result.TIR:
            print("  ⚠ TOTAL INTERNAL REFLECTION")
            print("  θₜ = N/A (evanescent wave)")
        else:
            print(f"  θₜ = {result.theta_t:.2f}°")
        print("  ────────────────────────────────────────")
        print("  TE (s-polarized):")
        print(f"    Γ_TE = {format_complex(result.Gamma_TE)}")
        print(f"    |Γ_TE| = {abs(result.Gamma_TE):.4f}")
        print(f"    R_TE = {result.R_TE:.4f}, T_TE = {result.T_TE:.4f}")
        print("  TM (p-polarized):")
        print(f"    Γ_TM = {format_complex(result.Gamma_TM)}")
        print(f"    |Γ_TM| = {abs(result.Gamma_TM):.4f}")
        print(f"    R_TM = {result.R_TM:.4f}, T_TM = {result.T_TM:.4f}")
        if not result.TIR:
            print("  ────────────────────────────────────────")
            print(f"  θ_Brewster = {result.theta_Brewster:.2f}°")
        print("  ════════════════════════════════════════")
        
    elif mode == 3:
        print("\n  --- Enter refractive indices ---")
        n1 = get_number("  n1: ", 0.1)
        n2 = get_number("  n2: ", 0.1)
        theta = get_number("  θi [degrees]: ", 0, 90)
        
        print(f"\n  Calling: Fresnel('snell', {n1}, {n2}, {theta})")
        result = Fresnel('snell', n1, n2, theta)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - SNELL'S LAW")
        print("  ════════════════════════════════════════")
        print(f"  n₁ = {result.n1:.4f}, n₂ = {result.n2:.4f}")
        print(f"  θᵢ = {result.theta_i:.2f}°")
        if result.TIR:
            print("  ⚠ TOTAL INTERNAL REFLECTION")
            print(f"  θ_critical = {result.theta_critical:.2f}°")
        else:
            print(f"  θₜ = {result.theta_t:.2f}°")
        print("  ════════════════════════════════════════")
        
    elif mode == 4:
        print("\n  --- Enter material properties ---")
        eps1 = get_number("  εr1: ", 0.1)
        eps2 = get_number("  εr2: ", 0.1)
        
        print(f"\n  Calling: Fresnel('brewster', {eps1}, {eps2})")
        result = Fresnel('brewster', eps1, eps2)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - BREWSTER ANGLE")
        print("  ════════════════════════════════════════")
        print(f"  n₁ = {result.n1:.4f}, n₂ = {result.n2:.4f}")
        print(f"  θ_Brewster = {result.theta_Brewster:.4f}°")
        print("  At this angle: Γ_TM = 0 (no TM reflection)")
        print("  ════════════════════════════════════════")
        
    else:
        print("\n  --- Enter material properties ---")
        print("  (Note: n1 must be > n2 for TIR to exist)")
        eps1 = get_number("  εr1 (denser medium): ", 0.1)
        eps2 = get_number("  εr2 (less dense): ", 0.1)
        
        print(f"\n  Calling: Fresnel('critical', {eps1}, {eps2})")
        result = Fresnel('critical', eps1, eps2)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - CRITICAL ANGLE")
        print("  ════════════════════════════════════════")
        print(f"  n₁ = {result.n1:.4f}, n₂ = {result.n2:.4f}")
        if result.n1 > result.n2:
            print(f"  θ_critical = {result.theta_critical:.4f}°")
            print("  For θᵢ > θ_c: Total Internal Reflection")
        else:
            print("  n₁ < n₂: No critical angle exists")
            print("  TIR not possible in this direction")
        print("  ════════════════════════════════════════")


def handle_medium():
    """Handle medium properties calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       MEDIUM PROPERTIES")
    print("  ═══════════════════════════════════════════")
    print()
    print("  What type of medium?")
    print()
    print("    1. Lossless dielectric")
    print("    2. Lossy medium (with conductivity σ)")
    print("    3. From loss tangent tan(δ)")
    print("    4. Good conductor")
    print("    5. Skin depth only")
    print("    6. Free space")
    print()
    
    mode = int(get_number("  Enter choice (1-6): ", 1, 6))
    
    if mode == 1:
        print("\n  --- Enter parameters ---")
        eps_r = get_number("  εr: ", 0.1)
        freq = get_number("  Frequency [Hz]: ", 1)
        
        result = Medium(eps_r, freq)
        
    elif mode == 2:
        print("\n  --- Enter parameters ---")
        eps_r = get_number("  εr: ", 0.1)
        sigma = get_number("  σ [S/m]: ", 0)
        freq = get_number("  Frequency [Hz]: ", 1)
        
        result = Medium(eps_r, sigma, freq)
        
    elif mode == 3:
        print("\n  --- Enter parameters ---")
        eps_r = get_number("  εr: ", 0.1)
        tan_d = get_number("  tan(δ): ", 0)
        freq = get_number("  Frequency [Hz]: ", 1)
        
        result = Medium('tand', eps_r, tan_d, freq)
        
    elif mode == 4:
        print("\n  --- Enter parameters ---")
        sigma = get_number("  σ [S/m]: ", 1)
        freq = get_number("  Frequency [Hz]: ", 1)
        
        result = Medium('conductor', sigma, freq)
        
    elif mode == 5:
        print("\n  --- Enter parameters ---")
        sigma = get_number("  σ [S/m]: ", 1)
        freq = get_number("  Frequency [Hz]: ", 1)
        
        result = Medium('skin', sigma, freq)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - SKIN DEPTH")
        print("  ════════════════════════════════════════")
        print(f"  σ = {sigma:.3e} S/m")
        print(f"  freq = {freq:.3e} Hz")
        print("  ────────────────────────────────────────")
        print(f"  δ = {result.skin_depth:.4e} m")
        print(f"  δ = {result.skin_depth*1e6:.4f} μm")
        print(f"  δ = {result.skin_depth*1e3:.4f} mm")
        print("  ════════════════════════════════════════")
        return
        
    else:
        print("\n  --- Enter frequency ---")
        freq = get_number("  Frequency [Hz]: ", 1)
        
        result = Medium('free', freq)
    
    # Display results for modes 1-4, 6
    print()
    print("  ════════════════════════════════════════")
    print(f"       {result.classification.upper()} @ {result.freq:.2e} Hz")
    print("  ════════════════════════════════════════")
    print(f"  εr = {result.eps_r:.4f}")
    print(f"  μr = {result.mu_r:.4f}")
    if result.sigma > 0:
        print(f"  σ = {result.sigma:.3e} S/m")
        print(f"  tan(δ) = {result.tan_delta:.3e}")
    print("  ────────────────────────────────────────")
    print(f"  α = {result.alpha:.4e} Np/m")
    print(f"  β = {result.beta:.4e} rad/m")
    print(f"  λ = {result.lambda_:.4e} m")
    print(f"  uₚ = {result.up:.4e} m/s")
    print(f"  n = {result.n:.4f}")
    print("  ────────────────────────────────────────")
    print(f"  η = {format_complex(result.eta)} Ω")
    print(f"  |η| = {abs(result.eta):.4f} Ω")
    if result.alpha > 0:
        print("  ────────────────────────────────────────")
        print(f"  Skin depth = {result.skin_depth:.4e} m")
    print("  ════════════════════════════════════════")


def handle_tline():
    """Handle transmission line calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       TRANSMISSION LINES")
    print("  ═══════════════════════════════════════════")
    print()
    print("  What do you need?")
    print()
    print("    1. Basic TL analysis (Zin, Γ, VSWR)")
    print("    2. Find input impedance")
    print("    3. Find load impedance")
    print("    4. Reflection coefficient from Z")
    print("    5. Impedance from Γ")
    print("    6. Find load from Γ at input (Q13/Q14 type)")
    print("    7. Quarter-wave transformer design")
    print("    8. Stub design (realize impedance)")
    print()
    
    mode = int(get_number("  Enter choice (1-8): ", 1, 8))
    
    if mode in [1, 2]:
        print("\n  --- Enter TL parameters ---")
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        ZL_r = get_number("  ZL real part [Ω]: ")
        ZL_i = get_number("  ZL imag part [Ω]: ")
        ZL = complex(ZL_r, ZL_i)
        length = get_number("  Length [wavelengths]: ", 0)
        
        result = TLine(Z0, ZL, length)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - TL ANALYSIS")
        print("  ════════════════════════════════════════")
        print(f"  Z₀ = {Z0:.2f} Ω")
        print(f"  Z_L = {format_complex(ZL)} Ω")
        print(f"  Length = {length:.4f} λ")
        print("  ────────────────────────────────────────")
        print(f"  Z_in = {format_complex(result.Z_in)} Ω")
        print(f"  |Z_in| = {abs(result.Z_in):.4f} Ω")
        print("  ────────────────────────────────────────")
        print(f"  Γ_L = {format_complex(result.Gamma_L)}")
        mag, ang = to_polar(result.Gamma_L)
        print(f"  |Γ_L| = {mag:.4f}, ∠Γ_L = {ang:.2f}°")
        print(f"  Γ_in = {format_complex(result.Gamma_in)}")
        print("  ────────────────────────────────────────")
        print(f"  VSWR = {result.VSWR:.4f}")
        print(f"  Return Loss = {result.RL_dB:.2f} dB")
        print(f"  Power delivered = {result.P_delivered*100:.2f}%")
        print("  ════════════════════════════════════════")
        
    elif mode == 3:
        print("\n  --- Enter TL parameters ---")
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        Zin_r = get_number("  Zin real part [Ω]: ")
        Zin_i = get_number("  Zin imag part [Ω]: ")
        Zin = complex(Zin_r, Zin_i)
        length = get_number("  Length [wavelengths]: ", 0)
        
        result = TLine('ZL', Z0, Zin, length)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - FIND LOAD")
        print("  ════════════════════════════════════════")
        print(f"  Z_L = {format_complex(result.ZL)} Ω")
        print("  ════════════════════════════════════════")
        
    elif mode == 4:
        print("\n  --- Enter parameters ---")
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        Z_r = get_number("  Z real part [Ω]: ")
        Z_i = get_number("  Z imag part [Ω]: ")
        Z = complex(Z_r, Z_i)
        
        result = TLine('Gamma', Z0, Z)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - Γ FROM Z")
        print("  ════════════════════════════════════════")
        print(f"  Γ = {format_complex(result.Gamma_L)}")
        mag, ang = to_polar(result.Gamma_L)
        print(f"  |Γ| = {mag:.4f}")
        print(f"  ∠Γ = {ang:.2f}°")
        print(f"  VSWR = {result.VSWR:.4f}")
        print("  ════════════════════════════════════════")
        
    elif mode == 5:
        print("\n  --- Enter parameters ---")
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        print("\n  Enter Γ in polar form:")
        Gamma_mag = get_number("  |Γ|: ", 0)
        Gamma_ang = get_number("  ∠Γ [degrees]: ")
        Gamma = from_polar(Gamma_mag, Gamma_ang)
        
        result = TLine('Z', Z0, Gamma)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - Z FROM Γ")
        print("  ════════════════════════════════════════")
        print(f"  Z = {format_complex(result.ZL)} Ω")
        print(f"  |Z| = {abs(result.ZL):.4f} Ω")
        print("  ════════════════════════════════════════")
        
    elif mode == 6:
        print("\n  --- Q13/Q14 Type Problem ---")
        print("  Given Γ at input, find Γ_L and Z_L")
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        print("\n  Enter Γ_in in polar form:")
        Gamma_mag = get_number("  |Γ_in|: ", 0)
        Gamma_ang = get_number("  ∠Γ_in [degrees]: ")
        Gamma_in = from_polar(Gamma_mag, Gamma_ang)
        length = get_number("  Length [wavelengths]: ", 0)
        
        result = TLine('load', Z0, Gamma_in, length)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - FIND LOAD")
        print("  ════════════════════════════════════════")
        print(f"  Phase shift: +2βℓ = +{2*360*length:.2f}°")
        print("  ────────────────────────────────────────")
        print(f"  Γ_L = {format_complex(result.Gamma_L)}")
        mag, ang = to_polar(result.Gamma_L)
        print(f"  |Γ_L| = {mag:.4f}, ∠Γ_L = {ang:.2f}°")
        print("  ────────────────────────────────────────")
        print(f"  Z_L = {format_complex(result.ZL)} Ω")
        print(f"  |Z_L| = {abs(result.ZL):.2f} Ω")
        print("  ────────────────────────────────────────")
        print(f"  VSWR = {result.VSWR:.4f}")
        print("  ════════════════════════════════════════")
        
    elif mode == 7:
        print("\n  --- Quarter-Wave Transformer Design ---")
        Z_source = get_number("  Z_source [Ω]: ", 0.1)
        Z_load = get_number("  Z_load [Ω]: ", 0.1)
        
        result = TLine('QW', Z_source, Z_load)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - QW TRANSFORMER")
        print("  ════════════════════════════════════════")
        print(f"  Required Z₀ = √({Z_source} × {Z_load})")
        print(f"  Z₀ = {result.Z0:.4f} Ω")
        print("  Length = λ/4")
        print("  ════════════════════════════════════════")
        
    else:
        print("\n  --- Stub Design ---")
        print("  Realize target impedance with stub")
        X_target = get_number("  Target reactance X [Ω] (jX): ")
        Z0_stub = get_number("  Stub Z0 [Ω]: ", 0.1)
        
        result = TLine('stub', complex(0, X_target), Z0_stub)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - STUB DESIGN")
        print("  ════════════════════════════════════════")
        print(f"  Target Z = j{X_target} Ω")
        print(f"  Stub Z₀ = {Z0_stub} Ω")
        print("  ────────────────────────────────────────")
        print(f"  SHORT stub: ℓ = {result.short_len:.4f} λ")
        if not np.isnan(result.open_len):
            print(f"  OPEN stub:  ℓ = {result.open_len:.4f} λ")
        print("  ════════════════════════════════════════")


def handle_stub_match():
    """Handle stub matching calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       SINGLE-STUB MATCHING")
    print("  ═══════════════════════════════════════════")
    print()
    
    print("  --- Enter parameters ---")
    ZL_r = get_number("  ZL real part [Ω]: ")
    ZL_i = get_number("  ZL imag part [Ω]: ")
    ZL = complex(ZL_r, ZL_i)
    Z0 = get_number("  Z0 [Ω]: ", 0.1)
    
    print("\n  Stub type:")
    print("    1. Short-circuited")
    print("    2. Open-circuited")
    stub_choice = int(get_number("  Choice: ", 1, 2))
    stub_type = 'short' if stub_choice == 1 else 'open'
    
    print("\n  Do you know the wavelength λ?")
    if get_yes_no("  (y/n): "):
        lambda_ = get_number("  λ [m]: ", 0)
    else:
        lambda_ = None
    
    result = StubMatch(ZL, Z0, stub_type, lambda_)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT - STUB MATCHING")
    print("  ════════════════════════════════════════")
    print(f"  Load: Z_L = {format_complex(ZL)} Ω")
    print(f"  Line: Z₀ = {Z0} Ω ({stub_type.upper()} stub)")
    if lambda_:
        print(f"  λ = {lambda_*100:.2f} cm")
    print("  ────────────────────────────────────────")
    print("  SOLUTION 1:")
    print(f"    d = {result.d:.4f} λ", end="")
    if lambda_:
        print(f" = {result.d_mm:.2f} mm")
    else:
        print()
    print(f"    ℓ = {result.l:.4f} λ", end="")
    if lambda_:
        print(f" = {result.l_mm:.2f} mm")
    else:
        print()
    if not np.isnan(result.d_alt):
        print("  SOLUTION 2:")
        print(f"    d = {result.d_alt:.4f} λ")
        print(f"    ℓ = {result.l_alt:.4f} λ")
    print("  ════════════════════════════════════════")


def handle_poynting():
    """Handle Poynting vector calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       POYNTING VECTOR & H-FIELD")
    print("  ═══════════════════════════════════════════")
    print()
    print("  What format is your E-field?")
    print()
    print("    1. Time-domain: E = E0*(a·cos + b·sin)")
    print("    2. Complex phasor E directly")
    print()
    
    fmt = int(get_number("  Enter format (1-2): ", 1, 2))
    
    if fmt == 1:
        print("\n  --- Enter a vector (cos coefficient) ---")
        ax = get_number("  ax: ")
        ay = get_number("  ay: ")
        az = get_number("  az: ")
        a = [ax, ay, az]
        
        print("\n  --- Enter b vector (sin coefficient) ---")
        bx = get_number("  bx: ")
        by = get_number("  by: ")
        bz = get_number("  bz: ")
        b = [bx, by, bz]
        
        E0 = get_number("  E0 amplitude [V/m]: ", 0)
        
        print("\n  --- Enter β vector ---")
        beta_x = get_number("  βx: ")
        beta_y = get_number("  βy: ")
        beta_z = get_number("  βz: ")
        beta_vec = [beta_x, beta_y, beta_z]
        
        print("\n  Use custom η? (default is 377 Ω)")
        if get_yes_no("  Custom η? (y/n): "):
            eta = get_number("  Enter η [Ω]: ", 0)
            result = poynting_pw('time', a, b, E0, beta_vec, eta)
        else:
            # For time mode we need to handle differently
            a = np.array(a)
            b = np.array(b)
            beta_vec = np.array(beta_vec)
            eta = 377
            E_phasor = E0 * (a - 1j * b)
            k_hat = beta_vec / np.linalg.norm(beta_vec)
            H_phasor = (1/eta) * np.cross(k_hat, E_phasor)
            S_avg = 0.5 * np.real(np.cross(E_phasor, np.conj(H_phasor)))
            
            result = PoyntingResult(
                E_phasor=E_phasor, H_phasor=H_phasor,
                k_hat=k_hat, eta=eta, S_avg=S_avg, S_mag=np.linalg.norm(S_avg)
            )
    else:
        print("\n  --- Enter E phasor components ---")
        Ex = get_complex("  Ex: ")
        Ey = get_complex("  Ey: ")
        Ez = get_complex("  Ez: ")
        E = [Ex, Ey, Ez]
        
        print("\n  --- Enter k or β vector ---")
        kx = get_number("  kx: ")
        ky = get_number("  ky: ")
        kz = get_number("  kz: ")
        k = [kx, ky, kz]
        
        print("\n  Use custom η? (default is 377 Ω)")
        if get_yes_no("  Custom η? (y/n): "):
            eta = get_number("  Enter η [Ω]: ", 0)
        else:
            eta = 377
        
        result = poynting_pw(E, k, eta)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT - H-FIELD & POYNTING")
    print("  ════════════════════════════════════════")
    print(f"  Ẽ₀ = {format_vector(result.E_phasor)} V/m")
    print(f"  k̂ = [{result.k_hat[0]:.4f}, {result.k_hat[1]:.4f}, {result.k_hat[2]:.4f}]")
    print(f"  η = {result.eta:.0f} Ω")
    print("  ────────────────────────────────────────")
    print("  H̃₀ = (1/η)·k̂ × Ẽ₀")
    H_mA = result.H_phasor * 1e3
    print(f"  H̃₀ = {format_vector(H_mA, 2)} mA/m")
    print("  ────────────────────────────────────────")
    print("  S̄ = ½·Re{Ẽ × H̃*}")
    print(f"  S̄ = [{result.S_avg[0]:.3f}; {result.S_avg[1]:.3f}; {result.S_avg[2]:.3f}] W/m²")
    print(f"  |S̄| = {result.S_mag:.3f} W/m²")
    print("  ════════════════════════════════════════")


def handle_bfield_wire():
    """Handle B-field from infinite wire"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       B-FIELD FROM INFINITE WIRE")
    print("  ═══════════════════════════════════════════")
    print()
    
    print("  --- Enter parameters ---")
    I = get_number("  Current I [A]: ")
    r = get_number("  Distance r [m]: ", 1e-10)
    
    print("\n  Is the material magnetic (μr ≠ 1)?")
    if get_yes_no("  (y/n): "):
        mu_r = get_number("  μr: ", 0.1)
    else:
        mu_r = 1.0
    
    B = B_inf_wire(I, r, mu_r)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT")
    print("  ════════════════════════════════════════")
    print(f"  B = {B:.6e} T")
    print(f"  B = {B*1e6:.6f} μT")
    print(f"  B = {B*1e3:.6f} mT")
    print("  ════════════════════════════════════════")


def handle_coulomb():
    """Handle Coulomb force calculation"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       COULOMB FORCE BETWEEN CHARGES")
    print("  ═══════════════════════════════════════════")
    print()
    
    print("  --- Enter charge 1 ---")
    q1 = get_number("  q1 [C]: ")
    print("  Position r1:")
    r1x = get_number("    x [m]: ")
    r1y = get_number("    y [m]: ")
    r1z = get_number("    z [m]: ")
    r1 = [r1x, r1y, r1z]
    
    print("\n  --- Enter charge 2 ---")
    q2 = get_number("  q2 [C]: ")
    print("  Position r2:")
    r2x = get_number("    x [m]: ")
    r2y = get_number("    y [m]: ")
    r2z = get_number("    z [m]: ")
    r2 = [r2x, r2y, r2z]
    
    F12, F21 = coulomb_pair(q1, q2, r1, r2)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT")
    print("  ════════════════════════════════════════")
    print("  F12 (force on q1 due to q2):")
    print(f"    = [{F12[0]:.6e}; {F12[1]:.6e}; {F12[2]:.6e}] N")
    print(f"    |F12| = {np.linalg.norm(F12):.6e} N")
    print()
    print("  F21 (force on q2 due to q1):")
    print(f"    = [{F21[0]:.6e}; {F21[1]:.6e}; {F21[2]:.6e}] N")
    print(f"    |F21| = {np.linalg.norm(F21):.6e} N")
    print("  ════════════════════════════════════════")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main program loop"""
    clear_screen()
    print_welcome()
    
    while True:
        print_menu()
        
        try:
            choice = int(get_number("  Enter choice (0-9): ", 0, 9))
        except:
            continue
        
        if choice == 0:
            print("\n  Goodbye and good luck on your exam! 🎓\n")
            break
        
        handlers = {
            1: handle_plane_wave,
            2: handle_polarization,
            3: handle_fresnel,
            4: handle_medium,
            5: handle_tline,
            6: handle_stub_match,
            7: handle_poynting,
            8: handle_bfield_wire,
            9: handle_coulomb,
        }
        
        if choice in handlers:
            try:
                handlers[choice]()
            except Exception as e:
                print(f"\n  ⚠ Error: {e}")
        
        input("\n  Press Enter to continue...")
        clear_screen()
        print_welcome()


if __name__ == "__main__":
    main()
