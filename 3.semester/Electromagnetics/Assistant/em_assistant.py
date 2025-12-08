#!/usr/bin/env python3
"""
EM Assistant - Interactive Electromagnetic Problem Solver
=========================================================

Run from terminal:
    python em_assistant.py

This guides you through solving EM problems using the em_tools library.

NEW FEATURES:
  - 10. Inverse TLine (find Z_L from VSWR + position)
  - 11. Geometry Library (L, C calculations)
  - 12. Wave Uniformity Analyzer
"""

import sys
import os
import cmath
import numpy as np

# Import the EM tools
try:
    from em_calc import *
except ImportError:
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
    print("  ║              Python Edition v2.0                         ║")
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
    print("  │  ─── NEW FEATURES ───                  │")
    print("  │  10. Inverse TLine (VSWR→Z_L)          │")
    print("  │  11. Geometry Library (L, C)           │")
    print("  │  12. Wave Uniformity Analyzer          │")
    print("  │  13. 🧠 Smart Solver                   │")
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
            
            raw = raw.replace('i', 'j').replace('J', 'j')
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
    print("    2. γ = [γx; γy; γz] given separately")
    print()
    
    fmt = int(get_number("  Enter format (1 or 2): ", 1, 2))
    
    if fmt == 1:
        print("\n  --- Enter E-field phasor components ---")
        Ex = get_complex("  Ex: ")
        Ey = get_complex("  Ey: ")
        Ez = get_complex("  Ez: ")
        E = [Ex, Ey, Ez]
        
        print("\n  --- Enter H-field phasor components ---")
        Hx = get_complex("  Hx: ")
        Hy = get_complex("  Hy: ")
        Hz = get_complex("  Hz: ")
        H = [Hx, Hy, Hz]
        
        print("\n  --- Enter k from phase term ---")
        kx = get_number("  kx: ")
        ky = get_number("  ky: ")
        kz = get_number("  kz: ")
        k = [kx, ky, kz]
        
        print("\n  Use custom η? (default 377 Ω)")
        if get_yes_no("  Custom η? (y/n): "):
            eta = get_number("  Enter η [Ω]: ", 0)
        else:
            eta = 377
        
        result = PlaneWaveCheck('full', E, H, k, eta)
    else:
        print("\n  --- Enter E₀ phasor components ---")
        Ex = get_complex("  E0x: ")
        Ey = get_complex("  E0y: ")
        Ez = get_complex("  E0z: ")
        E0 = [Ex, Ey, Ez]
        
        print("\n  --- Enter H₀ phasor components ---")
        Hx = get_complex("  H0x: ")
        Hy = get_complex("  H0y: ")
        Hz = get_complex("  H0z: ")
        H0 = [Hx, Hy, Hz]
        
        print("\n  --- Enter γ (complex propagation vector) ---")
        gx = get_complex("  γx: ")
        gy = get_complex("  γy: ")
        gz = get_complex("  γz: ")
        gamma = [gx, gy, gz]
        
        result = PlaneWaveCheck('maxwell', E0, H0, gamma)
    
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
        Ex = get_complex("  Ex: ")
        Ey = get_complex("  Ey: ")
        Ez = get_complex("  Ez: ")
        E = [Ex, Ey, Ez]
        
        print("\n  --- Propagation direction k̂ ---")
        if get_yes_no("  Use default +z? (y/n): "):
            k_hat = [0, 0, 1]
        else:
            kx = get_number("  k̂x: ")
            ky = get_number("  k̂y: ")
            kz = get_number("  k̂z: ")
            k_hat = [kx, ky, kz]
        
        result = Polarization(E, k_hat)
        
    elif fmt == 2:
        print("\n  --- Enter amplitudes and phases ---")
        Ex = get_number("  |Ex| [V/m]: ", 0)
        Ey = get_number("  |Ey| [V/m]: ", 0)
        phi_x = get_number("  φx [degrees]: ")
        phi_y = get_number("  φy [degrees]: ")
        
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
        
        result = Polarization(u, v, beta)
    
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
        eps1 = get_number("  εr1 (incident): ", 0.1)
        eps2 = get_number("  εr2 (second): ", 0.1)
        
        result = Fresnel(eps1, eps2)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - NORMAL INCIDENCE")
        print("  ════════════════════════════════════════")
        print(f"  η₁ = {result.eta1:.2f} Ω, η₂ = {result.eta2:.2f} Ω")
        print(f"  Γ = {format_complex(result.Gamma)}")
        print(f"  |Γ| = {abs(result.Gamma):.4f}")
        print(f"  τ = {result.tau:.4f}")
        print(f"  R = {result.R*100:.2f}%, T = {result.T*100:.2f}%")
        print("  ════════════════════════════════════════")
        
    elif mode == 2:
        print("\n  --- Enter material properties ---")
        eps1 = get_number("  εr1: ", 0.1)
        eps2 = get_number("  εr2: ", 0.1)
        theta = get_number("  θi [degrees]: ", 0, 90)
        
        result = Fresnel(eps1, eps2, theta)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - OBLIQUE INCIDENCE")
        print("  ════════════════════════════════════════")
        print(f"  θᵢ = {result.theta_i:.2f}°")
        if result.TIR:
            print("  ⚠ TOTAL INTERNAL REFLECTION")
        else:
            print(f"  θₜ = {result.theta_t:.2f}°")
        print("  TE:", f"Γ={format_complex(result.Gamma_TE)}, R={result.R_TE:.4f}")
        print("  TM:", f"Γ={format_complex(result.Gamma_TM)}, R={result.R_TM:.4f}")
        print("  ════════════════════════════════════════")
        
    elif mode == 3:
        print("\n  --- Enter refractive indices ---")
        n1 = get_number("  n1: ", 0.1)
        n2 = get_number("  n2: ", 0.1)
        theta = get_number("  θi [degrees]: ", 0, 90)
        
        result = Fresnel('snell', n1, n2, theta)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - SNELL'S LAW")
        print("  ════════════════════════════════════════")
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
        
        result = Fresnel('brewster', eps1, eps2)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - BREWSTER ANGLE")
        print("  ════════════════════════════════════════")
        print(f"  θ_Brewster = {result.theta_Brewster:.4f}°")
        print("  ════════════════════════════════════════")
        
    else:
        print("\n  --- Enter material properties ---")
        eps1 = get_number("  εr1 (denser): ", 0.1)
        eps2 = get_number("  εr2 (less dense): ", 0.1)
        
        result = Fresnel('critical', eps1, eps2)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - CRITICAL ANGLE")
        print("  ════════════════════════════════════════")
        if result.n1 > result.n2:
            print(f"  θ_critical = {result.theta_critical:.4f}°")
        else:
            print("  n₁ < n₂: No critical angle exists")
        print("  ════════════════════════════════════════")


def handle_medium():
    """Handle medium properties calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       MEDIUM PROPERTIES")
    print("  ═══════════════════════════════════════════")
    print()
    print("    1. Lossless dielectric")
    print("    2. Lossy medium (σ)")
    print("    3. From loss tangent")
    print("    4. Good conductor")
    print("    5. Skin depth only")
    print("    6. Free space")
    print()
    
    mode = int(get_number("  Enter choice (1-6): ", 1, 6))
    
    if mode == 1:
        eps_r = get_number("  εr: ", 0.1)
        freq = get_number("  Frequency [Hz]: ", 1)
        result = Medium(eps_r, freq)
    elif mode == 2:
        eps_r = get_number("  εr: ", 0.1)
        sigma = get_number("  σ [S/m]: ", 0)
        freq = get_number("  Frequency [Hz]: ", 1)
        result = Medium(eps_r, sigma, freq)
    elif mode == 3:
        eps_r = get_number("  εr: ", 0.1)
        tan_d = get_number("  tan(δ): ", 0)
        freq = get_number("  Frequency [Hz]: ", 1)
        result = Medium('tand', eps_r, tan_d, freq)
    elif mode == 4:
        sigma = get_number("  σ [S/m]: ", 0)
        freq = get_number("  Frequency [Hz]: ", 1)
        result = Medium('conductor', sigma, freq)
    elif mode == 5:
        sigma = get_number("  σ [S/m]: ", 0)
        freq = get_number("  Frequency [Hz]: ", 1)
        result = Medium('skin', sigma, freq)
    else:
        freq = get_number("  Frequency [Hz]: ", 1)
        result = Medium('free', freq)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT")
    print("  ════════════════════════════════════════")
    print(f"  Classification: {result.classification}")
    print(f"  α = {result.alpha:.4e} Np/m")
    print(f"  β = {result.beta:.4e} rad/m")
    print(f"  λ = {result.lambda_:.4e} m")
    print(f"  uₚ = {result.up:.4e} m/s")
    print(f"  η = {format_complex(result.eta)} Ω")
    if result.skin_depth < float('inf'):
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
    print("    1. Basic TL analysis (Zin, Γ, VSWR)")
    print("    2. Find input impedance")
    print("    3. Find load impedance")
    print("    4. Reflection coefficient from Z")
    print("    5. Impedance from Γ")
    print("    6. Find load from Γ at input")
    print("    7. Quarter-wave transformer")
    print("    8. Stub design")
    print()
    
    mode = int(get_number("  Enter choice (1-8): ", 1, 8))
    
    if mode in [1, 2]:
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        ZL_r = get_number("  ZL real [Ω]: ")
        ZL_i = get_number("  ZL imag [Ω]: ")
        ZL = complex(ZL_r, ZL_i)
        length = get_number("  Length [λ]: ", 0)
        
        result = TLine(Z0, ZL, length)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT")
        print("  ════════════════════════════════════════")
        print(f"  Z_in = {format_complex(result.Z_in)} Ω")
        print(f"  Γ_L = {format_complex(result.Gamma_L)}")
        mag, ang = to_polar(result.Gamma_L)
        print(f"  |Γ| = {mag:.4f}, ∠Γ = {ang:.2f}°")
        print(f"  VSWR = {result.VSWR:.4f}")
        print("  ════════════════════════════════════════")
        
    elif mode == 3:
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        Zin_r = get_number("  Zin real [Ω]: ")
        Zin_i = get_number("  Zin imag [Ω]: ")
        Zin = complex(Zin_r, Zin_i)
        length = get_number("  Length [λ]: ", 0)
        
        result = TLine('ZL', Z0, Zin, length)
        
        print()
        print("  ════════════════════════════════════════")
        print(f"  Z_L = {format_complex(result.ZL)} Ω")
        print("  ════════════════════════════════════════")
        
    elif mode == 4:
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        Z_r = get_number("  Z real [Ω]: ")
        Z_i = get_number("  Z imag [Ω]: ")
        Z = complex(Z_r, Z_i)
        
        result = TLine('Gamma', Z0, Z)
        
        print()
        print("  ════════════════════════════════════════")
        print(f"  Γ = {format_complex(result.Gamma_L)}")
        mag, ang = to_polar(result.Gamma_L)
        print(f"  |Γ| = {mag:.4f}, ∠Γ = {ang:.2f}°")
        print(f"  VSWR = {result.VSWR:.4f}")
        print("  ════════════════════════════════════════")
        
    elif mode == 5:
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        Gamma_mag = get_number("  |Γ|: ", 0, 1)
        Gamma_ang = get_number("  ∠Γ [deg]: ")
        Gamma = from_polar(Gamma_mag, Gamma_ang)
        
        result = TLine('Z', Z0, Gamma)
        
        print()
        print("  ════════════════════════════════════════")
        print(f"  Z = {format_complex(result.ZL)} Ω")
        print("  ════════════════════════════════════════")
        
    elif mode == 6:
        Z0 = get_number("  Z0 [Ω]: ", 0.1)
        Gamma_mag = get_number("  |Γ_in|: ", 0, 1)
        Gamma_ang = get_number("  ∠Γ_in [deg]: ")
        Gamma_in = from_polar(Gamma_mag, Gamma_ang)
        length = get_number("  Length [λ]: ", 0)
        
        result = TLine('load', Z0, Gamma_in, length)
        
        print()
        print("  ════════════════════════════════════════")
        print(f"  Γ_L = {format_complex(result.Gamma_L)}")
        mag, ang = to_polar(result.Gamma_L)
        print(f"  |Γ_L| = {mag:.4f}, ∠Γ_L = {ang:.2f}°")
        print(f"  Z_L = {format_complex(result.ZL)} Ω")
        print("  ════════════════════════════════════════")
        
    elif mode == 7:
        Z_source = get_number("  Z_source [Ω]: ", 0.1)
        Z_load = get_number("  Z_load [Ω]: ", 0.1)
        
        result = TLine('QW', Z_source, Z_load)
        
        print()
        print("  ════════════════════════════════════════")
        print(f"  Z₀ = {result.Z0:.4f} Ω")
        print("  Length = λ/4")
        print("  ════════════════════════════════════════")
        
    else:
        X_target = get_number("  Target reactance X [Ω]: ")
        Z0_stub = get_number("  Stub Z0 [Ω]: ", 0.1)
        
        result = TLine('stub', complex(0, X_target), Z0_stub)
        
        print()
        print("  ════════════════════════════════════════")
        print(f"  SHORT stub: ℓ = {result.short_len:.4f} λ")
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
    
    ZL_r = get_number("  ZL real [Ω]: ")
    ZL_i = get_number("  ZL imag [Ω]: ")
    ZL = complex(ZL_r, ZL_i)
    Z0 = get_number("  Z0 [Ω]: ", 0.1)
    
    print("\n  Stub type: 1=Short, 2=Open")
    stub_choice = int(get_number("  Choice: ", 1, 2))
    stub_type = 'short' if stub_choice == 1 else 'open'
    
    print("\n  Know the wavelength λ?")
    if get_yes_no("  (y/n): "):
        lambda_ = get_number("  λ [m]: ", 0)
    else:
        lambda_ = None
    
    result = StubMatch(ZL, Z0, stub_type, lambda_)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT")
    print("  ════════════════════════════════════════")
    print(f"  d = {result.d:.4f} λ", end="")
    if lambda_:
        print(f" = {result.d_mm:.2f} mm")
    else:
        print()
    print(f"  ℓ = {result.l:.4f} λ", end="")
    if lambda_:
        print(f" = {result.l_mm:.2f} mm")
    else:
        print()
    if not np.isnan(result.d_alt):
        print(f"  Alt: d={result.d_alt:.4f}λ, ℓ={result.l_alt:.4f}λ")
    print("  ════════════════════════════════════════")


def handle_poynting():
    """Handle Poynting vector calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       POYNTING VECTOR & H-FIELD")
    print("  ═══════════════════════════════════════════")
    print()
    print("    1. Time-domain: E = E0*(a·cos + b·sin)")
    print("    2. Complex phasor E directly")
    print("    3. Scalar: |E| and η → S_avg (simple)")
    print()
    
    fmt = int(get_number("  Enter format (1-3): ", 1, 3))
    
    if fmt == 3:
        # Simple scalar mode
        print()
        print("  --- Electric field magnitude ---")
        print("    1. Enter |E| directly")
        print("    2. Calculate |E| at position (with attenuation)")
        E_mode = int(get_number("  Choice: ", 1, 2))
        
        k_hat = np.array([0, 0, 1])  # Default: +z propagation
        
        if E_mode == 1:
            E_mag = get_number("  |E| [V/m]: ", 0)
        else:
            print("\n  --- E-field at origin ---")
            print("  Enter E₀ as magnitude, or complex components")
            print("    1. |E₀| magnitude directly")
            print("    2. Complex E₀ (e.g., j20 or 20∠90°)")
            E0_mode = int(get_number("  Choice: ", 1, 2))
            
            if E0_mode == 1:
                E0_mag = get_number("  |E₀| [V/m]: ", 0)
            else:
                E0_complex = get_complex("  E₀ [V/m]: ")
                E0_mag = abs(E0_complex)
                print(f"  |E₀| = {E0_mag:.4f} V/m")
            
            print("\n  --- Propagation direction ---")
            print("    1. +z only (common case)")
            print("    2. General direction (kx, ky, kz)")
            dir_mode = int(get_number("  Choice: ", 1, 2))
            
            if dir_mode == 1:
                k_hat = np.array([0, 0, 1])
                print("  Propagation: +ẑ")
            else:
                kx = get_number("  kx: ")
                ky = get_number("  ky: ")
                kz = get_number("  kz: ")
                k_vec = np.array([kx, ky, kz])
                k_hat = k_vec / np.linalg.norm(k_vec)
                print(f"  k̂ = [{k_hat[0]:.4f}, {k_hat[1]:.4f}, {k_hat[2]:.4f}]")
            
            print("\n  --- Propagation constant γ ---")
            print("    1. Enter α (attenuation) directly")
            print("    2. Enter γ = α + jβ")
            gamma_mode = int(get_number("  Choice: ", 1, 2))
            
            if gamma_mode == 1:
                alpha = get_number("  α [Np/m]: ", 0)
            else:
                alpha = get_number("  α (real part of γ): ")
                beta = get_number("  β (imag part of γ): ")
                print(f"  γ = {alpha} + j{beta}")
            
            print("\n  --- Surface/observation position ---")
            print("    1. Enter z only (x=0, y=0)")
            print("    2. Enter full (x, y, z)")
            pos_mode = int(get_number("  Choice: ", 1, 2))
            
            if pos_mode == 1:
                z = get_number("  z [m]: ")
                pos = np.array([0, 0, z])
            else:
                x = get_number("  x [m]: ")
                y = get_number("  y [m]: ")
                z = get_number("  z [m]: ")
                pos = np.array([x, y, z])
                print(f"  Position: ({x}, {y}, {z}) m")
            
            # Calculate distance along propagation direction
            distance = np.dot(k_hat, pos)
            
            # Calculate |E| at position
            attenuation = np.exp(-alpha * distance)
            E_mag = E0_mag * attenuation
            
            print()
            print(f"  ────────────────────────────────")
            print(f"  Distance along k̂: {distance:.4f} m")
            print(f"  |E(r)| = |E₀| × e^(-α × distance)")
            print(f"        = {E0_mag:.4f} × e^(-{alpha} × {distance:.4f})")
            print(f"        = {E0_mag:.4f} × {attenuation:.4f}")
            print(f"        = {E_mag:.4f} V/m")
            print(f"  ────────────────────────────────")
        
        print("\n  --- Intrinsic impedance η ---")
        print("    1. Free space (η = 377 Ω)")
        print("    2. Lossless medium (enter εr)")
        print("    3. Lossy medium (enter complex εr)")
        print("    4. Enter η directly")
        eta_mode = int(get_number("  Choice: ", 1, 4))
        
        if eta_mode == 1:
            eta = 377.0
            eta_real = 377.0
        elif eta_mode == 2:
            eps_r = get_number("  εr: ", 0.1)
            eta = 377 / np.sqrt(eps_r)
            eta_real = eta
        elif eta_mode == 3:
            eps_r_real = get_number("  εr (real part): ")
            eps_r_imag = get_number("  εr (imag part, negative for loss): ")
            eps_r_c = eps_r_real + 1j * eps_r_imag
            eta = 377 / np.sqrt(eps_r_c)
            eta_real = eta.real
            print(f"\n  η = {eta:.2f} Ω")
        else:
            eta_real = get_number("  Re{η} [Ω]: ", 0.1)
            eta = eta_real
        
        # S_avg = |E|² / (2 * Re{η})
        S_avg_mag = E_mag**2 / (2 * eta_real)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT")
        print("  ════════════════════════════════════════")
        print(f"  |E| = {E_mag:.4f} V/m")
        print(f"  Re{{η}} = {eta_real:.2f} Ω")
        print(f"  S_avg = |E|² / (2·Re{{η}})")
        print(f"  S_avg = {E_mag:.4f}² / (2 × {eta_real:.2f})")
        print(f"  S_avg = {S_avg_mag:.6f} W/m²")
        print(f"       = {S_avg_mag*1000:.4f} mW/m²")
        
        # Ask about power calculation
        if get_yes_no("\n  Calculate power on surface? (y/n): "):
            A = get_number("  Surface area [m²]: ", 0)
            
            print("\n  --- Surface normal vector ---")
            print("    1. Normal to propagation (|cos θ| = 1)")
            print("    2. Enter surface normal (nx, ny, nz)")
            normal_mode = int(get_number("  Choice: ", 1, 2))
            
            if normal_mode == 1:
                cos_theta = 1.0
                print("  Surface perpendicular to wave → full power")
            else:
                nx = get_number("  nx: ")
                ny = get_number("  ny: ")
                nz = get_number("  nz: ")
                n_hat = np.array([nx, ny, nz])
                n_hat = n_hat / np.linalg.norm(n_hat)  # Normalize
                
                # S points in k_hat direction
                # Power into surface = |S · n̂|
                dot_product = np.dot(k_hat, n_hat)
                cos_theta = abs(dot_product)
                
                print(f"  n̂ = [{n_hat[0]:.3f}, {n_hat[1]:.3f}, {n_hat[2]:.3f}]")
                print(f"  k̂ · n̂ = {dot_product:.4f}")
                
                if dot_product < 0:
                    print("  Wave incident on surface (into surface)")
                elif dot_product > 0:
                    print("  Wave exiting surface (out of surface)")
                else:
                    print("  Wave parallel to surface (grazing)")
                
                print(f"  |cos θ| = {cos_theta:.4f}")
            
            P = S_avg_mag * A * cos_theta
            print(f"\n  P = S_avg × A × |cos θ|")
            print(f"    = {S_avg_mag:.6f} × {A} × {cos_theta:.4f}")
            print(f"  P = {P:.6f} W = {P*1000:.2f} mW")
        
        print("  ════════════════════════════════════════")
        return
    
    if fmt == 1:
        print("\n  --- a vector (cos coeff) ---")
        ax = get_number("  ax: ")
        ay = get_number("  ay: ")
        az = get_number("  az: ")
        a = [ax, ay, az]
        
        print("\n  --- b vector (sin coeff) ---")
        bx = get_number("  bx: ")
        by = get_number("  by: ")
        bz = get_number("  bz: ")
        b = [bx, by, bz]
        
        E0 = get_number("  E0 [V/m]: ", 0)
        
        print("\n  --- β vector ---")
        beta_x = get_number("  βx: ")
        beta_y = get_number("  βy: ")
        beta_z = get_number("  βz: ")
        beta_vec = [beta_x, beta_y, beta_z]
        
        # Ask for custom η
        if get_yes_no("\n  Custom η (not free space)? (y/n): "):
            eta = get_number("  η [Ω]: ", 0.1)
        else:
            eta = 377
        
        a = np.array(a)
        b = np.array(b)
        beta_vec = np.array(beta_vec)
        E_phasor = E0 * (a - 1j * b)
        k_hat = beta_vec / np.linalg.norm(beta_vec)
        H_phasor = (1/eta) * np.cross(k_hat, E_phasor)
        S_avg = 0.5 * np.real(np.cross(E_phasor, np.conj(H_phasor)))
        
        result = PoyntingResult(
            E_phasor=E_phasor, H_phasor=H_phasor,
            k_hat=k_hat, eta=eta, S_avg=S_avg, S_mag=np.linalg.norm(S_avg)
        )
    else:
        print("\n  --- E phasor components ---")
        Ex = get_complex("  Ex: ")
        Ey = get_complex("  Ey: ")
        Ez = get_complex("  Ez: ")
        E = [Ex, Ey, Ez]
        
        print("\n  --- k or β vector ---")
        kx = get_number("  kx: ")
        ky = get_number("  ky: ")
        kz = get_number("  kz: ")
        k = [kx, ky, kz]
        
        # Ask for custom η
        if get_yes_no("\n  Custom η (not free space)? (y/n): "):
            eta = get_number("  η [Ω]: ", 0.1)
        else:
            eta = 377
        
        result = poynting_pw(E, k, eta)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT")
    print("  ════════════════════════════════════════")
    H_mA = result.H_phasor * 1e3
    print(f"  H̃₀ = {format_vector(H_mA, 2)} mA/m")
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
    
    I = get_number("  Current I [A]: ")
    r = get_number("  Distance r [m]: ", 1e-10)
    
    if get_yes_no("  Magnetic material (μr ≠ 1)? (y/n): "):
        mu_r = get_number("  μr: ", 0.1)
    else:
        mu_r = 1.0
    
    B = B_inf_wire(I, r, mu_r)
    
    print()
    print("  ════════════════════════════════════════")
    print(f"  B = {B:.6e} T")
    print(f"  B = {B*1e6:.6f} μT")
    print("  ════════════════════════════════════════")


def handle_coulomb():
    """Handle Coulomb force calculation"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       COULOMB FORCE")
    print("  ═══════════════════════════════════════════")
    print()
    
    print("  --- Charge 1 ---")
    q1 = get_number("  q1 [C]: ")
    r1x = get_number("  x [m]: ")
    r1y = get_number("  y [m]: ")
    r1z = get_number("  z [m]: ")
    r1 = [r1x, r1y, r1z]
    
    print("\n  --- Charge 2 ---")
    q2 = get_number("  q2 [C]: ")
    r2x = get_number("  x [m]: ")
    r2y = get_number("  y [m]: ")
    r2z = get_number("  z [m]: ")
    r2 = [r2x, r2y, r2z]
    
    F12, F21 = coulomb_pair(q1, q2, r1, r2)
    
    print()
    print("  ════════════════════════════════════════")
    print(f"  F12 = [{F12[0]:.6e}; {F12[1]:.6e}; {F12[2]:.6e}] N")
    print(f"  |F12| = {np.linalg.norm(F12):.6e} N")
    print("  ════════════════════════════════════════")


# =============================================================================
# NEW FEATURE HANDLERS
# =============================================================================

def handle_inverse_tline():
    """Handle inverse TLine solver - find Z_L from VSWR + position"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       INVERSE TLINE SOLVER")
    print("       Find Z_L from VSWR + Vmin/Vmax position")
    print("  ═══════════════════════════════════════════")
    print()
    print("  This solves exam problems like:")
    print("  'Given VSWR=3 and first Vmin at z=0.1λ, find Z_L'")
    print()
    
    Z0 = get_number("  Z0 [Ω]: ", 0.1)
    
    print("\n  How is the reflection given?")
    print("    1. VSWR")
    print("    2. |Γ| (magnitude)")
    print("    3. Γ [dB] (e.g., -6 dB)")
    
    input_mode = int(get_number("  Choice (1-3): ", 1, 3))
    
    VSWR = Gamma_mag = Gamma_dB = None
    
    if input_mode == 1:
        VSWR = get_number("  VSWR: ", 1)
    elif input_mode == 2:
        Gamma_mag = get_number("  |Γ|: ", 0, 1)
    else:
        Gamma_dB = get_number("  Γ [dB]: ")
    
    print("\n  What position is given?")
    print("    1. Voltage MINIMUM position (z_min)")
    print("    2. Voltage MAXIMUM position (z_max)")
    
    pos_mode = int(get_number("  Choice (1-2): ", 1, 2))
    
    z_min = z_max = None
    
    if pos_mode == 1:
        z_min = get_number("  z_min [wavelengths]: ", 0)
    else:
        z_max = get_number("  z_max [wavelengths]: ", 0)
    
    result = TLine_inverse(Z0=Z0, VSWR=VSWR, Gamma_mag=Gamma_mag, 
                           Gamma_dB=Gamma_dB, z_min=z_min, z_max=z_max)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT - INVERSE TLINE")
    print("  ════════════════════════════════════════")
    print(f"  Input: {result.input_type} → |Γ| = {result.Gamma_mag:.4f}")
    print(f"  Position: {result.position_type}")
    print("  ────────────────────────────────────────")
    print(f"  |Γ| = {result.Gamma_mag:.4f}")
    print(f"  ∠Γ = {result.Gamma_angle_deg:.2f}°")
    print(f"  Γ_L = {format_complex(result.Gamma_L)}")
    print("  ────────────────────────────────────────")
    print(f"  ★ Z_L = {format_complex(result.ZL)} Ω")
    print(f"  |Z_L| = {abs(result.ZL):.4f} Ω")
    print(f"  ∠Z_L = {np.degrees(cmath.phase(result.ZL)):.2f}°")
    print("  ────────────────────────────────────────")
    print(f"  VSWR = {result.VSWR:.4f}")
    print(f"  z_vmin = {result.z_vmin:.4f}λ")
    print(f"  z_vmax = {result.z_vmax:.4f}λ")
    print("  ════════════════════════════════════════")


def handle_geometry_library():
    """Handle geometry/component library calculations"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       GEOMETRY & COMPONENT LIBRARY")
    print("  ═══════════════════════════════════════════")
    print()
    print("    1. Solenoid inductance: L = μN²A/ℓ")
    print("    2. Coaxial capacitance: C = 2πεℓ/ln(b/a)")
    print("    3. Parallel wire capacitance")
    print("    4. Parallel plate capacitance: C = εA/d")
    print()
    
    mode = int(get_number("  Enter choice (1-4): ", 1, 4))
    
    if mode == 1:
        print("\n  ═══ SOLENOID INDUCTANCE ═══")
        print("  L = μ₀·μᵣ·N²·A/ℓ")
        print()
        
        N = int(get_number("  Number of turns N: ", 1))
        
        print("\n  Enter area: 1=directly, 2=from radius")
        area_mode = int(get_number("  Choice: ", 1, 2))
        
        if area_mode == 1:
            A = get_number("  Area A [m²]: ", 0)
            radius = None
        else:
            radius = get_number("  Radius [m]: ", 0)
            A = None
        
        length = get_number("  Length ℓ [m]: ", 0)
        
        if get_yes_no("  Magnetic core (μr ≠ 1)? (y/n): "):
            mu_r = get_number("  μr: ", 0.1)
        else:
            mu_r = 1.0
        
        result = solenoid_inductance(N=N, A=A, length=length, radius=radius, mu_r=mu_r)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - SOLENOID INDUCTANCE")
        print("  ════════════════════════════════════════")
        print(f"  N = {result.N} turns")
        print(f"  A = {result.A:.6e} m²")
        print(f"  ℓ = {result.length:.6e} m")
        print(f"  μr = {result.mu_r}")
        print("  ────────────────────────────────────────")
        print(f"  ★ L = {result.L:.6e} H")
        print(f"    L = {result.L_uH:.4f} μH")
        print(f"    L = {result.L_nH:.4f} nH")
        print("  ════════════════════════════════════════")
        
    elif mode == 2:
        print("\n  ═══ COAXIAL CAPACITANCE ═══")
        print("  C = 2π·ε₀·εᵣ·ℓ / ln(b/a)")
        print()
        
        a = get_number("  Inner radius a [m]: ", 0)
        b = get_number("  Outer radius b [m]: ", 0)
        length = get_number("  Length ℓ [m]: ", 0)
        
        if get_yes_no("  Dielectric (εr ≠ 1)? (y/n): "):
            eps_r = get_number("  εr: ", 0.1)
        else:
            eps_r = 1.0
        
        result = coax_capacitance(a=a, b=b, length=length, eps_r=eps_r)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - COAXIAL CAPACITANCE")
        print("  ════════════════════════════════════════")
        print(f"  a = {result.inner_radius:.6e} m")
        print(f"  b = {result.outer_radius:.6e} m")
        print(f"  ℓ = {result.length:.6e} m")
        print(f"  εr = {result.eps_r}")
        print("  ────────────────────────────────────────")
        print(f"  ★ C = {result.C:.6e} F")
        print(f"    C = {result.C_pF:.4f} pF")
        print(f"    C = {result.C_nF:.6f} nF")
        print("  ════════════════════════════════════════")
        
    elif mode == 3:
        print("\n  ═══ PARALLEL WIRE CAPACITANCE ═══")
        print("  C = π·ε₀·εᵣ·ℓ / arccosh(d/2R)")
        print()
        
        d = get_number("  Wire separation d [m]: ", 0)
        R = get_number("  Wire radius R [m]: ", 0)
        length = get_number("  Length ℓ [m]: ", 0)
        
        if get_yes_no("  Dielectric (εr ≠ 1)? (y/n): "):
            eps_r = get_number("  εr: ", 0.1)
        else:
            eps_r = 1.0
        
        result = parallel_wire_capacitance(d=d, R=R, length=length, eps_r=eps_r)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - PARALLEL WIRE CAPACITANCE")
        print("  ════════════════════════════════════════")
        print(f"  d = {result.wire_separation:.6e} m")
        print(f"  R = {result.wire_radius:.6e} m")
        print(f"  ℓ = {result.length:.6e} m")
        print(f"  εr = {result.eps_r}")
        print("  ────────────────────────────────────────")
        print(f"  ★ C = {result.C:.6e} F")
        print(f"    C = {result.C_pF:.4f} pF")
        print("  ════════════════════════════════════════")
        
    else:
        print("\n  ═══ PARALLEL PLATE CAPACITANCE ═══")
        print("  C = ε₀·εᵣ·A/d")
        print()
        
        A = get_number("  Plate area A [m²]: ", 0)
        d = get_number("  Separation d [m]: ", 0)
        
        if get_yes_no("  Dielectric (εr ≠ 1)? (y/n): "):
            eps_r = get_number("  εr: ", 0.1)
        else:
            eps_r = 1.0
        
        result = parallel_plate_capacitance(A=A, d=d, eps_r=eps_r)
        
        print()
        print("  ════════════════════════════════════════")
        print("       RESULT - PARALLEL PLATE CAPACITANCE")
        print("  ════════════════════════════════════════")
        print(f"  A = {A:.6e} m²")
        print(f"  d = {d:.6e} m")
        print(f"  εr = {result.eps_r}")
        print("  ────────────────────────────────────────")
        print(f"  ★ C = {result.C:.6e} F")
        print(f"    C = {result.C_pF:.4f} pF")
        print("  ════════════════════════════════════════")


def handle_wave_uniformity():
    """Handle wave uniformity analysis"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════")
    print("       WAVE UNIFORMITY ANALYZER")
    print("  ═══════════════════════════════════════════")
    print()
    print("  Checks if α ∥ β for wave propagation")
    print("  γ = α + jβ (complex propagation constant)")
    print()
    print("  UNIFORM:     α ∥ β (same direction)")
    print("  NON-UNIFORM: α not ∥ β (different directions)")
    print()
    
    print("  Input format:")
    print("    1. Separate α and β vectors")
    print("    2. Complex γ vector")
    
    fmt = int(get_number("  Choice (1-2): ", 1, 2))
    
    if fmt == 1:
        print("\n  --- Attenuation vector α [Np/m] ---")
        ax = get_number("  αx: ")
        ay = get_number("  αy: ")
        az = get_number("  αz: ")
        alpha = [ax, ay, az]
        
        print("\n  --- Phase vector β [rad/m] ---")
        bx = get_number("  βx: ")
        by = get_number("  βy: ")
        bz = get_number("  βz: ")
        beta = [bx, by, bz]
        
        result = wave_uniformity(alpha=alpha, beta=beta)
    else:
        print("\n  --- Complex γ vector ---")
        print("  Enter each component as α + jβ")
        gx = get_complex("  γx: ")
        gy = get_complex("  γy: ")
        gz = get_complex("  γz: ")
        gamma = [gx, gy, gz]
        
        result = wave_uniformity(gamma=gamma)
    
    print()
    print("  ════════════════════════════════════════")
    print("       RESULT - WAVE UNIFORMITY")
    print("  ════════════════════════════════════════")
    
    status = "✓ UNIFORM" if result.is_uniform else "✗ NON-UNIFORM"
    print(f"  ★ Classification: {status}")
    print(f"    Type: {result.classification}")
    print("  ────────────────────────────────────────")
    print(f"  α = [{result.alpha[0]:.4f}; {result.alpha[1]:.4f}; {result.alpha[2]:.4f}]")
    print(f"  |α| = {result.alpha_mag:.4e} Np/m")
    print(f"  β = [{result.beta[0]:.4f}; {result.beta[1]:.4f}; {result.beta[2]:.4f}]")
    print(f"  |β| = {result.beta_mag:.4e} rad/m")
    print("  ────────────────────────────────────────")
    print(f"  α × β = [{result.cross_product[0]:.4e}; {result.cross_product[1]:.4e}; {result.cross_product[2]:.4e}]")
    print(f"  |α × β| = {result.cross_magnitude:.4e}")
    if result.alpha_mag > 1e-10 and result.beta_mag > 1e-10:
        print(f"  Angle between α and β: {result.angle_between_deg:.2f}°")
    print("  ────────────────────────────────────────")
    print(f"  {result.info}")
    print("  ════════════════════════════════════════")


# =============================================================================
# MAIN
# =============================================================================

def handle_smart_solver():
    """Handle Smart Solver with guided interview mode"""
    clear_screen()
    
    # Import SmartSolver
    try:
        from em_smart import SmartSolver, parse_value
    except ImportError:
        print("  ⚠ Error: em_smart.py not found!")
        print("  Make sure em_smart.py is in the same folder.")
        return
    
    # =========================================================================
    # VARIABLE DEFINITIONS FOR EACH TOPIC
    # =========================================================================
    TOPICS = {
        1: {
            'name': 'Transmission Line',
            'icon': '📡',
            'vars': [
                ('f', 'Frequency', 'Hz', '2G for 2 GHz'),
                ('Z0', 'Characteristic Impedance Z₀', 'Ω', '50'),
                ('ZL', 'Load Impedance Z_L', 'Ω', '100+j50'),
                ('Zg', 'Generator Impedance Z_g', 'Ω', '50'),
                ('Vg', 'Generator Voltage V_g', 'V', '5'),
                ('len_lambda', 'Electrical Length', 'λ', '0.25 for λ/4'),
                ('l', 'Physical Length', 'm', '0.15'),
                ('up_factor', 'Velocity Factor', '×c₀', '0.66'),
                ('VSWR', 'VSWR', '', '2.5'),
            ]
        },
        2: {
            'name': 'Plane Wave / Material',
            'icon': '🌊',
            'vars': [
                ('f', 'Frequency', 'Hz', '300M for 300 MHz'),
                ('eps_r', 'Relative Permittivity ε_r', '', '4.5'),
                ('mu_r', 'Relative Permeability μ_r', '', '1'),
                ('tan_delta', 'Loss Tangent tan(δ)', '', '0.02'),
                ('sigma', 'Conductivity σ', 'S/m', '58M for copper'),
                ('n', 'Refractive Index n', '', '1.5'),
            ]
        },
        3: {
            'name': 'Stub Matching',
            'icon': '🔧',
            'vars': [
                ('f', 'Frequency', 'Hz', '2G'),
                ('Z0', 'Line Impedance Z₀', 'Ω', '50'),
                ('ZL', 'Load Impedance Z_L', 'Ω', '100+j50'),
                ('up_factor', 'Velocity Factor', '×c₀', '0.66'),
                ('stub_type', 'Stub Type', '', 'open or short'),
                ('C_eq', 'Equiv. Capacitance (inverse stub)', 'F', '2p for 2 pF'),
                ('L_eq', 'Equiv. Inductance (inverse stub)', 'H', '20n for 20 nH'),
            ]
        },
        4: {
            'name': 'RLGC Line',
            'icon': '⚡',
            'vars': [
                ('f', 'Frequency', 'Hz', '10G'),
                ('R_prime', "Resistance R'", 'Ω/m', '3.112'),
                ('L_prime', "Inductance L'", 'H/m', '337.3n'),
                ('G_prime', "Conductance G'", 'S/m', '38.9m'),
                ('C_prime', "Capacitance C'", 'F/m', '61.9p'),
            ]
        },
        5: {
            'name': 'Geometry (L, C)',
            'icon': '📐',
            'vars': [
                ('N', 'Number of Turns', '', '200'),
                ('l_sol', 'Solenoid Length', 'm', '0.1'),
                ('A_sol', 'Solenoid Cross-Section Area', 'm²', '1.33e-4'),
                ('a', 'Inner Radius (coax)', 'm', '0.5e-2'),
                ('b', 'Outer Radius (coax)', 'm', '2.5e-2'),
                ('L', 'Length', 'm', '0.1'),
                ('d', 'Separation/Distance', 'm', '1e-3'),
                ('A', 'Plate Area', 'm²', '0.01'),
                ('eps_r', 'Relative Permittivity ε_r', '', '4'),
            ]
        },
        6: {
            'name': 'Interface / Fresnel',
            'icon': '🪞',
            'vars': [
                ('eps_r1', 'ε_r of Medium 1', '', '1'),
                ('eps_r2', 'ε_r of Medium 2', '', '4'),
                ('theta_i', 'Incidence Angle θ_i', '°', '45'),
                ('mu_r1', 'μ_r of Medium 1', '', '1'),
                ('mu_r2', 'μ_r of Medium 2', '', '1'),
            ]
        },
    }
    
    # =========================================================================
    # DISPLAY HEADER
    # =========================================================================
    print()
    print("  ═══════════════════════════════════════════════════════════")
    print("       🧠 SMART SOLVER - Interview Mode")
    print("  ═══════════════════════════════════════════════════════════")
    print()
    print("  I'll guide you through the variables step by step.")
    print("  Press Enter to skip any variable you don't know.")
    print()
    print("  ─── MODE SELECTION ───")
    print("  [G] Guided Interview (recommended)")
    print("  [R] Raw Input Mode (var=val, var=val, ...)")
    print("  [T] Run Unit Tests")
    print()
    
    mode = input("  Select mode [G/R/T]: ").strip().lower()
    
    if mode == 't':
        from em_smart import run_tests
        run_tests()
        return
    
    if mode == 'r':
        # RAW MODE - original behavior
        _handle_raw_mode(SmartSolver())
        return
    
    # =========================================================================
    # GUIDED INTERVIEW MODE
    # =========================================================================
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════════════════════")
    print("       🧠 SMART SOLVER - Guided Interview")
    print("  ═══════════════════════════════════════════════════════════")
    print()
    print("  ─── WHAT TYPE OF PROBLEM? ───")
    print()
    
    for num, topic in TOPICS.items():
        print(f"    {num}. {topic['icon']} {topic['name']}")
    print()
    print("    0. ↩ Back to Menu")
    print()
    
    try:
        choice = input("  Select topic (0-6): ").strip()
        if not choice or choice == '0':
            return
        topic_num = int(choice)
        if topic_num not in TOPICS:
            print("  Invalid choice.")
            return
    except ValueError:
        print("  Invalid input.")
        return
    
    topic = TOPICS[topic_num]
    
    # =========================================================================
    # COLLECT VARIABLES
    # =========================================================================
    clear_screen()
    print()
    print(f"  ═══════════════════════════════════════════════════════════")
    print(f"       {topic['icon']} {topic['name']} - Enter Known Values")
    print(f"  ═══════════════════════════════════════════════════════════")
    print()
    print("  📝 Enter values with SI prefixes: p n u m k M G")
    print("     Examples: 2G = 2×10⁹, 50n = 50×10⁻⁹, 38.9m = 0.0389")
    print("     Press Enter to skip unknown variables")
    print()
    print("  ─────────────────────────────────────────────────────────────")
    
    collected = {}
    
    for var_name, var_desc, var_unit, var_example in topic['vars']:
        unit_str = f" [{var_unit}]" if var_unit else ""
        prompt = f"  {var_desc}{unit_str}"
        hint = f"(e.g., {var_example})"
        
        # Format nicely
        full_prompt = f"{prompt}\n    {hint}: "
        
        user_val = input(full_prompt).strip()
        
        if user_val:
            # Handle special string values
            if var_name == 'stub_type':
                if user_val.lower() in ['open', 'short', 'o', 's']:
                    collected[var_name] = 'open' if user_val.lower() in ['open', 'o'] else 'short'
            else:
                try:
                    # Try to parse the value
                    parsed = parse_value(user_val)
                    collected[var_name] = parsed
                    print(f"    ✓ {var_name} = {parsed}")
                except Exception as e:
                    print(f"    ⚠ Couldn't parse '{user_val}', skipping...")
        print()
    
    # =========================================================================
    # ASK FOR ADDITIONAL VARIABLES
    # =========================================================================
    print("  ─────────────────────────────────────────────────────────────")
    print("  📎 Any other variables I missed?")
    print("     Format: var=value (or press Enter when done)")
    print()
    
    while True:
        extra = input("  Additional var=value: ").strip()
        if not extra:
            break
        
        if '=' in extra:
            try:
                key, val = extra.split('=', 1)
                key = key.strip()
                val = val.strip()
                
                if val.lower() in ['open', 'short']:
                    collected[key] = val.lower()
                else:
                    parsed = parse_value(val)
                    collected[key] = parsed
                print(f"    ✓ {key} = {collected[key]}")
            except Exception as e:
                print(f"    ⚠ Couldn't parse: {e}")
        else:
            print("    ⚠ Use format: variable=value")
    
    # =========================================================================
    # SOLVE AND DISPLAY RESULTS
    # =========================================================================
    if not collected:
        print("\n  ⚠ No variables entered. Nothing to solve.")
        return
    
    print()
    print("  ═══════════════════════════════════════════════════════════")
    print("       📊 SOLVING...")
    print("  ═══════════════════════════════════════════════════════════")
    
    # Show what was collected
    print()
    print("  Known variables:")
    for k, v in collected.items():
        print(f"    {k} = {v}")
    
    # Run solver
    solver = SmartSolver()
    
    # Build input string for solver
    input_parts = []
    for k, v in collected.items():
        if isinstance(v, str):
            input_parts.append(f"{k}={v}")
        elif isinstance(v, complex):
            if v.imag == 0:
                input_parts.append(f"{k}={v.real}")
            else:
                input_parts.append(f"{k}={v}")
        else:
            input_parts.append(f"{k}={v}")
    
    # Solve using kwargs directly for better precision
    try:
        result = solver.solve(**collected)
        solver.print_results(result)
        
        # Offer to continue
        print()
        print("  ─────────────────────────────────────────────────────────────")
        print("  Would you like to add more variables and re-solve?")
        again = input("  [Y/N]: ").strip().lower()
        
        if again == 'y':
            print()
            print("  Enter additional variables (format: var=value)")
            print("  Press Enter when done.")
            
            while True:
                extra = input("  > ").strip()
                if not extra:
                    break
                
                if '=' in extra:
                    try:
                        key, val = extra.split('=', 1)
                        key = key.strip()
                        val = val.strip()
                        
                        if val.lower() in ['open', 'short']:
                            collected[key] = val.lower()
                        else:
                            parsed = parse_value(val)
                            collected[key] = parsed
                        print(f"    ✓ {key} = {collected[key]}")
                    except Exception as e:
                        print(f"    ⚠ Couldn't parse: {e}")
            
            # Re-solve
            if collected:
                result = solver.solve(**collected)
                solver.print_results(result)
                
    except Exception as e:
        print(f"\n  ⚠ Error: {e}")
        import traceback
        traceback.print_exc()


def _handle_raw_mode(solver):
    """Handle raw input mode for Smart Solver (with all features)"""
    clear_screen()
    print()
    print("  ═══════════════════════════════════════════════════════════")
    print("       🧠 SMART SOLVER - Raw Input Mode (v2.0)")
    print("  ═══════════════════════════════════════════════════════════")
    print()
    print("  Enter known variables in format:")
    print("    variable=value, variable=value, ...")
    print()
    print("  ─── NEW FEATURES ───")
    print("  • Aliases: freq=2G, imp=50, load=100 (same as f, Z0, ZL)")
    print("  • Materials: mat=teflon, cond=copper (auto-sets properties)")
    print("  • SOLVE: 'SOLVE len_lambda FOR Z_in.imag=0' (goal seek)")
    print()
    print("  ─── COMMANDS ───")
    print("  help      - Variable reference    materials - List materials")
    print("  aliases   - List aliases          test      - Run tests")
    print("  quit      - Exit to menu")
    print()
    
    # Store base variables for SOLVE command
    base_vars = {}
    
    while True:
        print("  ─────────────────────────────────────────")
        user_input = input("  > ").strip()
        
        if not user_input:
            break
        
        if user_input.lower() in ['q', 'quit', 'exit', 'back']:
            break
        
        if user_input.lower() in ['materials', 'mat', 'mats']:
            from em_smart import list_materials
            list_materials()
            continue
        
        if user_input.lower() in ['aliases', 'alias', 'vars']:
            from em_smart import list_aliases
            list_aliases()
            continue
        
        if user_input.lower() == 'help':
            print("""
  ═══════════════════════════════════════════════════════════════
       📖 SMART SOLVER - VARIABLE REFERENCE
  ═══════════════════════════════════════════════════════════════
  
  FREQUENCY/WAVE:
    f (freq)     = frequency [Hz]          omega (w)  = angular freq [rad/s]
    lambda_      = wavelength [m]          beta       = phase constant [rad/m]
    up (vp)      = phase velocity [m/s]    up_factor  = velocity factor (×c0)
    
  TRANSMISSION LINE:
    Z0 (imp)     = char. impedance [Ω]     ZL (load)  = load impedance [Ω]
    Zg           = generator impedance [Ω] Vg         = generator voltage [V]
    len_lambda   = length [wavelengths]    l (length) = physical length [m]
    VSWR         = voltage standing wave ratio
    
  MATERIAL:
    eps_r (er)   = relative permittivity   mu_r       = relative permeability
    tan_delta    = loss tangent            sigma      = conductivity [S/m]
    
  STUB:
    C_eq (cap)   = equivalent capacitance [F]
    L_eq (ind)   = equivalent inductance [H]
    stub_type    = 'open' or 'short'
    
  RLGC:
    R_prime, L_prime, G_prime, C_prime = RLGC parameters [per meter]
    
  MATERIALS (use mat=X or cond=X):
    Dielectrics: air, vacuum, teflon, polyethylene, fr4, glass, silicon
    Conductors:  copper, gold, silver, aluminum, brass, pec
    Coax cables: rg58, rg59, rg6, lmr400
    
  GOAL SEEKER:
    SOLVE <vary> FOR <check>.<part> = <value>
    Example: SOLVE len_lambda FOR Z_in.imag = 0
    Parts: .real, .imag, .abs, .angle
            """)
            continue
        
        if user_input.lower() == 'test':
            from em_smart import run_tests
            run_tests()
            continue
        
        # Check for SOLVE command
        if user_input.upper().startswith('SOLVE'):
            try:
                from em_smart import parse_solve_command
                target_var, cond_var, cond_part, cond_value = parse_solve_command(user_input)
                
                print(f"\n  🎯 Goal Seek: Vary '{target_var}' to make {cond_var}.{cond_part} = {cond_value}")
                print(f"  Using base variables: {base_vars}")
                
                # Determine search range
                if 'lambda' in target_var.lower() or 'len_lambda' in target_var:
                    search_range = (0.001, 0.5)
                elif target_var == 'l':
                    search_range = (0.001, 1.0)
                else:
                    search_range = (0.001, 1.0)
                
                result = solver.goal_seek(
                    target_var=target_var,
                    condition_var=f"{cond_var}.{cond_part}",
                    condition_value=cond_value,
                    search_range=search_range,
                    base_vars=base_vars
                )
                
                solver.print_results(result)
                
            except ValueError as e:
                print(f"  ⚠ {e}")
            continue
        
        try:
            result = solver.solve(user_input)
            
            # Store base variables for future SOLVE commands
            from em_smart import CONSTANTS
            for k, v in result.items():
                if isinstance(v, (int, float, complex)) and k not in CONSTANTS:
                    base_vars[k] = v
            
            solver.print_results(result)
        except Exception as e:
            print(f"  ⚠ Error: {e}")
        
        print()
        print("  Enter more variables (or press Enter to return to menu)")


def main():
    """Main program loop"""
    clear_screen()
    print_welcome()
    
    while True:
        print_menu()
        
        try:
            choice = int(get_number("  Enter choice (0-13): ", 0, 13))
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
            10: handle_inverse_tline,
            11: handle_geometry_library,
            12: handle_wave_uniformity,
            13: handle_smart_solver,
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
