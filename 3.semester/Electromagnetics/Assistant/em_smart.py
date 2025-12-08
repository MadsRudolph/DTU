#!/usr/bin/env python3
"""
EM Smart Solver - Iterative Physics Variable Solver
====================================================

Feed it a "soup" of known variables, and it will solve for everything possible.

Usage:
    from em_smart import SmartSolver
    
    solver = SmartSolver()
    results = solver.solve("f=2G, Z0=50, C_eq=2p, up_factor=0.73, stub_type=open")
    print(results)

Handles SI prefixes: p, n, u, m, k, M, G
Handles constants: c, c0, eps0, mu0, eta0, pi
"""

import numpy as np
import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Callable, Optional, Any

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================
CONSTANTS = {
    'c': 2.99792458e8,
    'c0': 2.99792458e8,
    'eps0': 8.854187817e-12,
    'mu0': 4 * np.pi * 1e-7,
    'eta0': 376.730313668,
    'pi': np.pi,
}

# =============================================================================
# FEATURE 1: ALIASES (Polyglot Input)
# =============================================================================
ALIASES = {
    # Frequency aliases
    'frequency': 'f',
    'freq': 'f',
    'w': 'omega',
    'angular_freq': 'omega',
    'angular': 'omega',
    
    # Impedance aliases
    'impedance': 'Z0',
    'char_impedance': 'Z0',
    'imp': 'Z0',
    'z_0': 'Z0',
    'load': 'ZL',
    'load_impedance': 'ZL',
    'z_l': 'ZL',
    'z_load': 'ZL',
    'gen_impedance': 'Zg',
    'generator': 'Zg',
    'z_g': 'Zg',
    'z_gen': 'Zg',
    
    # Voltage aliases
    'voltage': 'Vg',
    'v_g': 'Vg',
    'v_gen': 'Vg',
    'v_in': 'V_in',
    'v_load': 'V_L',
    'v_l': 'V_L',
    
    # Length aliases
    'len': 'l',
    'length': 'l',
    'phys_length': 'l',
    'physical_length': 'l',
    'elec_length': 'len_lambda',
    'electrical_length': 'len_lambda',
    'ell': 'l',
    
    # Wavelength/propagation aliases
    'wavelength': 'lambda_',
    'lam': 'lambda_',
    'λ': 'lambda_',
    'velocity': 'up',
    'phase_velocity': 'up',
    'v_p': 'up',
    'vp': 'up',
    'velocity_factor': 'up_factor',
    'vf': 'up_factor',
    
    # Component aliases
    'cap': 'C_eq',
    'capacitance': 'C_eq',
    'capacitor': 'C_eq',
    'ind': 'L_eq',
    'inductance': 'L_eq',
    'inductor': 'L_eq',
    
    # Material aliases
    'permittivity': 'eps_r',
    'epsilon': 'eps_r',
    'eps': 'eps_r',
    'er': 'eps_r',
    'e_r': 'eps_r',
    'permeability': 'mu_r',
    'mu': 'mu_r',
    'ur': 'mu_r',
    'u_r': 'mu_r',
    'conductivity': 'sigma',
    'cond': 'sigma',
    'sig': 'sigma',
    'loss_tangent': 'tan_delta',
    'tan_d': 'tan_delta',
    'tand': 'tan_delta',
    
    # Reflection aliases
    'gamma': 'Gamma_L',
    'reflection': 'Gamma_L',
    'refl': 'Gamma_L',
    'vswr': 'VSWR',
    'swr': 'VSWR',
    
    # RLGC aliases
    'r_prime': 'R_prime',
    'l_prime': 'L_prime',
    'g_prime': 'G_prime',
    'c_prime': 'C_prime',
    'rprime': 'R_prime',
    'lprime': 'L_prime',
    'gprime': 'G_prime',
    'cprime': 'C_prime',
    
    # Geometry aliases
    'turns': 'N',
    'num_turns': 'N',
    'area': 'A',
    'radius': 'a',
    'inner_radius': 'a',
    'outer_radius': 'b',
    'separation': 'd',
    'distance': 'd',
    
    # Angle aliases
    'theta_i': 'theta_i',
    'incidence': 'theta_i',
    'incident_angle': 'theta_i',
    'theta_t': 'theta_t',
    'transmission_angle': 'theta_t',
}

# =============================================================================
# FEATURE 2: MATERIALS DATABASE (Material Scientist)
# =============================================================================
MATERIALS = {
    # Dielectrics
    'air': {'eps_r': 1.0, 'mu_r': 1.0, 'description': 'Air/Free space'},
    'vacuum': {'eps_r': 1.0, 'mu_r': 1.0, 'description': 'Vacuum'},
    'teflon': {'eps_r': 2.1, 'tan_delta': 0.0002, 'description': 'PTFE/Teflon'},
    'ptfe': {'eps_r': 2.1, 'tan_delta': 0.0002, 'description': 'PTFE/Teflon'},
    'polyethylene': {'eps_r': 2.25, 'tan_delta': 0.0002, 'description': 'Polyethylene'},
    'pe': {'eps_r': 2.25, 'tan_delta': 0.0002, 'description': 'Polyethylene'},
    'polystyrene': {'eps_r': 2.56, 'tan_delta': 0.0001, 'description': 'Polystyrene'},
    'fr4': {'eps_r': 4.4, 'tan_delta': 0.02, 'description': 'FR-4 PCB'},
    'pcb': {'eps_r': 4.4, 'tan_delta': 0.02, 'description': 'FR-4 PCB'},
    'glass': {'eps_r': 5.5, 'tan_delta': 0.002, 'description': 'Glass'},
    'silicon': {'eps_r': 11.7, 'description': 'Silicon'},
    'si': {'eps_r': 11.7, 'description': 'Silicon'},
    'gaas': {'eps_r': 12.9, 'description': 'Gallium Arsenide'},
    'alumina': {'eps_r': 9.8, 'tan_delta': 0.0001, 'description': 'Alumina (Al₂O₃)'},
    'water': {'eps_r': 80.0, 'tan_delta': 0.05, 'description': 'Water (at 20°C)'},
    'rt_duroid': {'eps_r': 2.2, 'tan_delta': 0.0009, 'description': 'Rogers RT/duroid'},
    'duroid': {'eps_r': 2.2, 'tan_delta': 0.0009, 'description': 'Rogers RT/duroid'},
    
    # Conductors
    'copper': {'sigma': 5.8e7, 'description': 'Copper (Cu)'},
    'cu': {'sigma': 5.8e7, 'description': 'Copper (Cu)'},
    'gold': {'sigma': 4.1e7, 'description': 'Gold (Au)'},
    'au': {'sigma': 4.1e7, 'description': 'Gold (Au)'},
    'silver': {'sigma': 6.17e7, 'description': 'Silver (Ag)'},
    'ag': {'sigma': 6.17e7, 'description': 'Silver (Ag)'},
    'aluminum': {'sigma': 3.5e7, 'description': 'Aluminum (Al)'},
    'al': {'sigma': 3.5e7, 'description': 'Aluminum (Al)'},
    'iron': {'sigma': 1.0e7, 'mu_r': 200, 'description': 'Iron (Fe)'},
    'fe': {'sigma': 1.0e7, 'mu_r': 200, 'description': 'Iron (Fe)'},
    'steel': {'sigma': 1.0e7, 'mu_r': 100, 'description': 'Steel'},
    'brass': {'sigma': 1.5e7, 'description': 'Brass'},
    'seawater': {'sigma': 4.0, 'eps_r': 80, 'description': 'Seawater'},
    'pec': {'sigma': 1e30, 'description': 'Perfect Electric Conductor'},
    
    # Common coax dielectrics with velocity factors
    'rg58': {'eps_r': 2.3, 'up_factor': 0.66, 'description': 'RG-58 coax'},
    'rg59': {'eps_r': 2.3, 'up_factor': 0.66, 'description': 'RG-59 coax'},
    'rg6': {'eps_r': 2.3, 'up_factor': 0.66, 'description': 'RG-6 coax'},
    'rg174': {'eps_r': 2.3, 'up_factor': 0.66, 'description': 'RG-174 coax'},
    'lmr400': {'eps_r': 2.3, 'up_factor': 0.85, 'description': 'LMR-400 coax'},
}

# SI Prefix multipliers
SI_PREFIXES = {
    'p': 1e-12,  # pico
    'n': 1e-9,   # nano
    'u': 1e-6,   # micro
    'μ': 1e-6,   # micro (unicode)
    'm': 1e-3,   # milli
    'k': 1e3,    # kilo
    'M': 1e6,    # mega
    'G': 1e9,    # giga
    'T': 1e12,   # tera
}


# =============================================================================
# VALUE PARSER
# =============================================================================
def parse_value(value_str: str) -> complex:
    """
    Parse a value string with SI prefixes and constants.
    
    Examples:
        "2G" -> 2e9
        "50" -> 50
        "2p" -> 2e-12
        "0.73c0" -> 0.73 * c0
        "337.3n" -> 337.3e-9
        "1+2j" -> (1+2j)
        "-j50" -> -50j
    """
    value_str = value_str.strip()
    
    # Handle complex numbers
    if 'j' in value_str.lower():
        # Replace 'j' patterns
        s = value_str.replace('J', 'j')
        # Handle cases like "-j50" -> "-50j"
        s = re.sub(r'([+-]?)j(\d+\.?\d*)', r'\g<1>\g<2>j', s)
        # Handle cases like "j50" -> "50j"
        s = re.sub(r'^j(\d+\.?\d*)', r'\g<1>j', s)
        try:
            return complex(s)
        except:
            pass
    
    # Check for constant multipliers (e.g., "0.73c0", "0.5*c")
    for const_name, const_val in CONSTANTS.items():
        patterns = [
            rf'([\d.]+)\s*\*?\s*{const_name}$',  # "0.73c0" or "0.73*c0"
            rf'^{const_name}$',  # just "c0"
        ]
        for pattern in patterns:
            match = re.match(pattern, value_str, re.IGNORECASE)
            if match:
                if match.groups():
                    return float(match.group(1)) * const_val
                else:
                    return const_val
    
    # Check for SI prefix at end
    if value_str and value_str[-1] in SI_PREFIXES:
        prefix = value_str[-1]
        number = value_str[:-1]
        try:
            return float(number) * SI_PREFIXES[prefix]
        except ValueError:
            pass
    
    # Try direct conversion
    try:
        return float(value_str)
    except ValueError:
        pass
    
    # Try complex
    try:
        return complex(value_str)
    except ValueError:
        pass
    
    raise ValueError(f"Cannot parse value: {value_str}")


def parse_input(input_str: str) -> Dict[str, Any]:
    """
    Parse input string like "f=2G, Z0=50, C_eq=2p" into a dictionary.
    
    Features:
        - SI prefixes (p, n, u, m, k, M, G)
        - Aliases (freq -> f, imp -> Z0, etc.)
        - Materials (mat=teflon, cond=copper)
    """
    result = {}
    warnings = []
    
    # Split by comma or semicolon
    parts = re.split(r'[,;]', input_str)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Handle key=value
        if '=' in part:
            key, value = part.split('=', 1)
            key_lower = key.strip().lower()  # Lowercase for matching
            key_original = key.strip()  # Keep original for non-matched keys
            value = value.strip()
            
            # ─────────────────────────────────────────────────────────────
            # FEATURE 2: Check for material/conductor references FIRST
            # (before aliases, since 'cond' is also an alias for sigma)
            # ─────────────────────────────────────────────────────────────
            if key_lower in ['mat', 'material', 'dielectric', 'medium']:
                mat_name = value.lower()
                if mat_name in MATERIALS:
                    mat_props = MATERIALS[mat_name]
                    for prop_key, prop_val in mat_props.items():
                        if prop_key != 'description':
                            result[prop_key] = prop_val
                    warnings.append(f"📚 Material '{mat_name}': {mat_props.get('description', '')}")
                else:
                    warnings.append(f"⚠ Unknown material: {mat_name}")
                continue
            
            if key_lower in ['cond', 'conductor', 'metal']:
                cond_name = value.lower()
                if cond_name in MATERIALS:
                    cond_props = MATERIALS[cond_name]
                    for prop_key, prop_val in cond_props.items():
                        if prop_key != 'description':
                            result[prop_key] = prop_val
                    warnings.append(f"📚 Conductor '{cond_name}': {cond_props.get('description', '')}")
                else:
                    warnings.append(f"⚠ Unknown conductor: {cond_name}")
                continue
            
            # ─────────────────────────────────────────────────────────────
            # FEATURE 1: Check for aliases
            # ─────────────────────────────────────────────────────────────
            if key_lower in ALIASES:
                key = ALIASES[key_lower]
            else:
                key = key_original  # Use original case if no alias
            
            # ─────────────────────────────────────────────────────────────
            # Parse the value
            # ─────────────────────────────────────────────────────────────
            # Check for string values (like stub_type=open)
            if value.lower() in ['open', 'short', 'true', 'false', 'te', 'tm']:
                result[key] = value.lower()
            else:
                try:
                    result[key] = parse_value(value)
                except ValueError:
                    result[key] = value  # Keep as string
    
    # Store warnings for later display
    if warnings:
        result['_warnings'] = warnings
    
    return result


# =============================================================================
# FORMULA REGISTRY
# =============================================================================
@dataclass
class Formula:
    """Represents a physics formula that can be solved."""
    name: str
    outputs: List[str]  # Variables this formula can solve for
    inputs: List[str]   # Variables needed (when solving for first output)
    func: Callable      # Function that computes output from inputs
    description: str = ""
    
    def can_solve(self, known: Dict[str, Any], target: str) -> bool:
        """Check if we can solve for target given known variables."""
        if target not in self.outputs:
            return False
        
        # Get required inputs for this target
        required = [v for v in self.inputs if v != target]
        
        # Check if all required inputs are known
        return all(v in known for v in required)
    
    def solve(self, known: Dict[str, Any], target: str) -> Any:
        """Solve for target variable."""
        # Build kwargs from known values
        kwargs = {v: known[v] for v in self.inputs if v in known}
        return self.func(target=target, **kwargs)


def build_formula_registry() -> List[Formula]:
    """Build the complete formula registry."""
    formulas = []
    
    # =========================================================================
    # BASIC FREQUENCY/WAVELENGTH RELATIONS
    # =========================================================================
    
    # omega = 2*pi*f
    def omega_f(target, **kw):
        if target == 'omega':
            return 2 * np.pi * kw['f']
        elif target == 'f':
            return kw['omega'] / (2 * np.pi)
    formulas.append(Formula(
        'omega_from_f', ['omega', 'f'], ['f', 'omega'], omega_f,
        'ω = 2πf'
    ))
    
    # lambda = up / f  (wavelength)
    def lambda_up_f(target, **kw):
        if target == 'lambda_':
            return kw['up'] / kw['f']
        elif target == 'up':
            return kw['lambda_'] * kw['f']
        elif target == 'f':
            return kw['up'] / kw['lambda_']
    formulas.append(Formula(
        'wavelength', ['lambda_', 'up', 'f'], ['up', 'f', 'lambda_'], lambda_up_f,
        'λ = u_p / f'
    ))
    
    # up = up_factor * c0  (phase velocity from factor)
    def up_from_factor(target, **kw):
        c0 = CONSTANTS['c0']
        if target == 'up':
            return kw['up_factor'] * c0
        elif target == 'up_factor':
            return kw['up'] / c0
    formulas.append(Formula(
        'up_from_factor', ['up', 'up_factor'], ['up_factor', 'up'], up_from_factor,
        'u_p = factor × c₀'
    ))
    
    # beta = omega / up  (phase constant)
    def beta_omega_up(target, **kw):
        if target == 'beta':
            return kw['omega'] / kw['up']
        elif target == 'omega':
            return kw['beta'] * kw['up']
        elif target == 'up':
            return kw['omega'] / kw['beta']
    formulas.append(Formula(
        'beta_from_omega_up', ['beta', 'omega', 'up'], ['omega', 'up', 'beta'], beta_omega_up,
        'β = ω / u_p'
    ))
    
    # beta = 2*pi / lambda
    def beta_lambda(target, **kw):
        if target == 'beta':
            return 2 * np.pi / kw['lambda_']
        elif target == 'lambda_':
            return 2 * np.pi / kw['beta']
    formulas.append(Formula(
        'beta_from_lambda', ['beta', 'lambda_'], ['lambda_', 'beta'], beta_lambda,
        'β = 2π / λ'
    ))
    
    # =========================================================================
    # TEST 5: ELECTRICAL LENGTH
    # =========================================================================
    
    # len_lambda = l / lambda  (electrical length)
    def len_lambda_calc(target, **kw):
        if target == 'len_lambda':
            return kw['l'] / kw['lambda_']
        elif target == 'l':
            return kw['len_lambda'] * kw['lambda_']
        elif target == 'lambda_':
            return kw['l'] / kw['len_lambda']
    formulas.append(Formula(
        'electrical_length', ['len_lambda', 'l', 'lambda_'], ['l', 'lambda_', 'len_lambda'], len_lambda_calc,
        'ℓ/λ = l / λ'
    ))
    
    # =========================================================================
    # TRANSMISSION LINE BASICS
    # =========================================================================
    
    # Y0 = 1/Z0
    def Y0_Z0(target, **kw):
        if target == 'Y0':
            return 1 / kw['Z0']
        elif target == 'Z0':
            return 1 / kw['Y0']
    formulas.append(Formula(
        'admittance', ['Y0', 'Z0'], ['Z0', 'Y0'], Y0_Z0,
        'Y₀ = 1/Z₀'
    ))
    
    # Gamma_L = (ZL - Z0) / (ZL + Z0)
    def gamma_from_Z(target, **kw):
        if target == 'Gamma_L':
            return (kw['ZL'] - kw['Z0']) / (kw['ZL'] + kw['Z0'])
        elif target == 'ZL':
            G = kw['Gamma_L']
            return kw['Z0'] * (1 + G) / (1 - G)
    formulas.append(Formula(
        'reflection_coeff', ['Gamma_L', 'ZL'], ['ZL', 'Z0', 'Gamma_L'], gamma_from_Z,
        'Γ_L = (Z_L - Z₀) / (Z_L + Z₀)'
    ))
    
    # VSWR = (1 + |Gamma|) / (1 - |Gamma|)
    def vswr_gamma(target, **kw):
        if target == 'VSWR':
            return (1 + abs(kw['Gamma_L'])) / (1 - abs(kw['Gamma_L']))
        elif target == 'Gamma_mag':
            return (kw['VSWR'] - 1) / (kw['VSWR'] + 1)
    formulas.append(Formula(
        'vswr', ['VSWR', 'Gamma_mag'], ['Gamma_L', 'VSWR'], vswr_gamma,
        'VSWR = (1 + |Γ|) / (1 - |Γ|)'
    ))
    
    # =========================================================================
    # TEST 2: RLGC LINE - Z0 = sqrt((R' + jωL') / (G' + jωC'))
    # =========================================================================
    
    def Z0_RLGC(target, **kw):
        if target == 'Z0':
            omega = kw['omega']
            R_prime = kw['R_prime']
            L_prime = kw['L_prime']
            G_prime = kw['G_prime']
            C_prime = kw['C_prime']
            Z0 = np.sqrt((R_prime + 1j * omega * L_prime) / (G_prime + 1j * omega * C_prime))
            return Z0
    formulas.append(Formula(
        'Z0_RLGC', ['Z0'], ['omega', 'R_prime', 'L_prime', 'G_prime', 'C_prime'], Z0_RLGC,
        'Z₀ = √[(R\' + jωL\') / (G\' + jωC\')]'
    ))
    
    # gamma_line = sqrt((R' + jωL')(G' + jωC'))
    def gamma_RLGC(target, **kw):
        if target == 'gamma_line':
            omega = kw['omega']
            R_prime = kw['R_prime']
            L_prime = kw['L_prime']
            G_prime = kw['G_prime']
            C_prime = kw['C_prime']
            return np.sqrt((R_prime + 1j * omega * L_prime) * (G_prime + 1j * omega * C_prime))
    formulas.append(Formula(
        'gamma_RLGC', ['gamma_line'], ['omega', 'R_prime', 'L_prime', 'G_prime', 'C_prime'], gamma_RLGC,
        'γ = √[(R\' + jωL\')(G\' + jωC\')]'
    ))
    
    # =========================================================================
    # TEST 1: INVERSE STUB - Open stub to realize capacitor
    # =========================================================================
    
    # Y_target = j*omega*C_eq (capacitor admittance)
    def Y_capacitor(target, **kw):
        if target == 'Y_target':
            return 1j * kw['omega'] * kw['C_eq']
        elif target == 'C_eq':
            return kw['Y_target'] / (1j * kw['omega'])
    formulas.append(Formula(
        'Y_capacitor', ['Y_target', 'C_eq'], ['omega', 'C_eq', 'Y_target'], Y_capacitor,
        'Y_target = jωC'
    ))
    
    # Z_target = 1/(j*omega*C_eq) (capacitor impedance)
    def Z_capacitor(target, **kw):
        if target == 'Z_target':
            return 1 / (1j * kw['omega'] * kw['C_eq'])
    formulas.append(Formula(
        'Z_capacitor', ['Z_target'], ['omega', 'C_eq'], Z_capacitor,
        'Z_target = 1/(jωC)'
    ))
    
    # Z_target = j*omega*L_eq (inductor impedance)
    def Z_inductor(target, **kw):
        if target == 'Z_target':
            return 1j * kw['omega'] * kw['L_eq']
        elif target == 'L_eq':
            return kw['Z_target'] / (1j * kw['omega'])
    formulas.append(Formula(
        'Z_inductor', ['Z_target', 'L_eq'], ['omega', 'L_eq', 'Z_target'], Z_inductor,
        'Z_target = jωL'
    ))
    
    # Open stub length: Y_open = j*Y0*tan(beta*l_stub) = Y_target
    # l_stub = arctan(Y_target / (j*Y0)) / beta = arctan(-j*Y_target/Y0) / beta
    def l_stub_open(target, **kw):
        if target == 'l_stub':
            Y_target = kw['Y_target']
            Y0 = kw['Y0']
            beta = kw['beta']
            # Y_open = j*Y0*tan(beta*l) = Y_target
            # tan(beta*l) = Y_target / (j*Y0) = -j*Y_target/Y0
            tan_bl = Y_target / (1j * Y0)
            bl = np.arctan(tan_bl)
            l = bl / beta
            # Ensure positive length
            if np.real(l) < 0:
                l = l + np.pi / beta
            return np.real(l)
    formulas.append(Formula(
        'l_stub_open', ['l_stub'], ['Y_target', 'Y0', 'beta'], l_stub_open,
        'Open stub: l = arctan(Y_target/(jY₀)) / β'
    ))
    
    # Short stub length: Y_short = -j*Y0*cot(beta*l_stub) = Y_target
    # cot(beta*l) = -Y_target / (j*Y0) = j*Y_target/Y0
    # tan(beta*l) = -j*Y0/Y_target
    def l_stub_short(target, **kw):
        if target == 'l_stub':
            Y_target = kw['Y_target']
            Y0 = kw['Y0']
            beta = kw['beta']
            # Y_short = -j*Y0/tan(beta*l) = Y_target
            # tan(beta*l) = -j*Y0/Y_target
            tan_bl = -1j * Y0 / Y_target
            bl = np.arctan(tan_bl)
            l = bl / beta
            if np.real(l) < 0:
                l = l + np.pi / beta
            return np.real(l)
    formulas.append(Formula(
        'l_stub_short', ['l_stub'], ['Y_target', 'Y0', 'beta'], l_stub_short,
        'Short stub: l = arctan(-jY₀/Y_target) / β'
    ))
    
    # =========================================================================
    # TEST 3: LOSSY WAVE ATTENUATION
    # =========================================================================
    
    # eps_c = eps_r * (1 - j*tan_delta) * eps0
    def eps_complex(target, **kw):
        if target == 'eps_c':
            eps0 = CONSTANTS['eps0']
            return kw['eps_r'] * (1 - 1j * kw['tan_delta']) * eps0
    formulas.append(Formula(
        'eps_complex', ['eps_c'], ['eps_r', 'tan_delta'], eps_complex,
        'ε_c = ε_r(1 - j·tan δ)ε₀'
    ))
    
    # gamma_wave = j*omega*sqrt(mu*eps_c) for wave in lossy medium
    def gamma_lossy(target, **kw):
        if target == 'gamma_wave':
            mu0 = CONSTANTS['mu0']
            mu_r = kw.get('mu_r', 1)
            mu = mu0 * mu_r
            omega = kw['omega']
            eps_c = kw['eps_c']
            return 1j * omega * np.sqrt(mu * eps_c)
    formulas.append(Formula(
        'gamma_lossy', ['gamma_wave'], ['omega', 'eps_c'], gamma_lossy,
        'γ = jω√(με_c)'
    ))
    
    # Alternative: gamma from eps_r and tan_delta directly
    def gamma_from_tan_delta(target, **kw):
        if target == 'gamma_wave':
            mu0 = CONSTANTS['mu0']
            eps0 = CONSTANTS['eps0']
            mu_r = kw.get('mu_r', 1)
            eps_r = kw['eps_r']
            tan_delta = kw['tan_delta']
            omega = kw['omega']
            mu = mu0 * mu_r
            eps_c = eps_r * (1 - 1j * tan_delta) * eps0
            return 1j * omega * np.sqrt(mu * eps_c)
    formulas.append(Formula(
        'gamma_from_tan_delta', ['gamma_wave'], ['omega', 'eps_r', 'tan_delta'], gamma_from_tan_delta,
        'γ = jω√(μ·ε_r(1-j·tanδ)ε₀)'
    ))
    
    # alpha = Re(gamma_wave), beta_wave = Im(gamma_wave)
    def alpha_beta_from_gamma(target, **kw):
        gamma = kw['gamma_wave']
        if target == 'alpha':
            return np.real(gamma)
        elif target == 'beta_wave':
            return np.imag(gamma)
    formulas.append(Formula(
        'alpha_from_gamma', ['alpha', 'beta_wave'], ['gamma_wave'], alpha_beta_from_gamma,
        'α = Re(γ), β = Im(γ)'
    ))
    
    # alpha_dB = 8.686 * alpha (Np/m to dB/m)
    def alpha_dB_calc(target, **kw):
        if target == 'alpha_dB':
            return 8.686 * kw['alpha']
        elif target == 'alpha':
            return kw['alpha_dB'] / 8.686
    formulas.append(Formula(
        'alpha_dB', ['alpha_dB', 'alpha'], ['alpha', 'alpha_dB'], alpha_dB_calc,
        'α_dB = 8.686 × α_Np'
    ))
    
    # =========================================================================
    # TEST 4: TRANSMISSION LINE VOLTAGES
    # =========================================================================
    
    # Z_in for general TL: Z_in = Z0 * (ZL + j*Z0*tan(beta*l)) / (Z0 + j*ZL*tan(beta*l))
    def Z_in_general(target, **kw):
        if target == 'Z_in':
            Z0 = kw['Z0']
            ZL = kw['ZL']
            beta = kw['beta']
            l = kw.get('l', None)
            len_lambda = kw.get('len_lambda', None)
            
            if l is not None:
                bl = beta * l
            elif len_lambda is not None:
                bl = 2 * np.pi * len_lambda
            else:
                return None
            
            tan_bl = np.tan(bl)
            Z_in = Z0 * (ZL + 1j * Z0 * tan_bl) / (Z0 + 1j * ZL * tan_bl)
            return Z_in
    formulas.append(Formula(
        'Z_in_general', ['Z_in'], ['Z0', 'ZL', 'beta', 'l'], Z_in_general,
        'Z_in = Z₀(Z_L + jZ₀tanβl)/(Z₀ + jZ_Ltanβl)'
    ))
    
    # Z_in from len_lambda directly (no beta needed)
    def Z_in_from_len_lambda(target, **kw):
        if target == 'Z_in':
            Z0 = kw['Z0']
            ZL = kw['ZL']
            len_lambda = kw['len_lambda']
            bl = 2 * np.pi * len_lambda
            tan_bl = np.tan(bl)
            # Handle special cases
            if abs(tan_bl) > 1e10:  # Near λ/4
                return Z0**2 / ZL
            Z_in = Z0 * (ZL + 1j * Z0 * tan_bl) / (Z0 + 1j * ZL * tan_bl)
            return Z_in
    formulas.append(Formula(
        'Z_in_len_lambda', ['Z_in'], ['Z0', 'ZL', 'len_lambda'], Z_in_from_len_lambda,
        'Z_in from electrical length'
    ))
    
    # V_in = Vg * Z_in / (Z_in + Zg) (voltage divider at input)
    def V_in_divider(target, **kw):
        if target == 'V_in':
            Vg = kw['Vg']
            Z_in = kw['Z_in']
            Zg = kw['Zg']
            return Vg * Z_in / (Z_in + Zg)
    formulas.append(Formula(
        'V_in_divider', ['V_in'], ['Vg', 'Z_in', 'Zg'], V_in_divider,
        'V_in = V_g × Z_in / (Z_in + Z_g)'
    ))
    
    # V_L from wave theory: V_in = V+(1 + Gamma_in*e^{-j2βl}), at load V_L = V+(1 + Gamma_L)e^{-jβl}
    # Simplified: V_L = V_in * (1 + Gamma_L) / (1 + Gamma_in)  for lossless line (|Γ| same)
    def V_L_from_V_in(target, **kw):
        if target == 'V_L':
            V_in = kw['V_in']
            Z0 = kw['Z0']
            ZL = kw['ZL']
            len_lambda = kw.get('len_lambda', 0.25)
            
            # Calculate reflection coefficients
            Gamma_L = (ZL - Z0) / (ZL + Z0)
            bl = 2 * np.pi * len_lambda
            Gamma_in = Gamma_L * np.exp(-2j * bl)
            
            # V+ from V_in
            V_plus = V_in / (1 + Gamma_in)
            
            # V_L at load (wave travels distance l)
            V_L = V_plus * np.exp(-1j * bl) * (1 + Gamma_L)
            return V_L
    formulas.append(Formula(
        'V_L_from_V_in', ['V_L'], ['V_in', 'Z0', 'ZL', 'len_lambda'], V_L_from_V_in,
        'V_L from wave propagation'
    ))
    
    # Alternative: Direct V_L calculation from Vg
    def V_L_direct(target, **kw):
        if target == 'V_L':
            Vg = kw['Vg']
            Zg = kw['Zg']
            Z0 = kw['Z0']
            ZL = kw['ZL']
            len_lambda = kw.get('len_lambda', 0.25)
            
            # Calculate Z_in
            bl = 2 * np.pi * len_lambda
            tan_bl = np.tan(bl)
            if abs(tan_bl) > 1e10:
                Z_in = Z0**2 / ZL
            else:
                Z_in = Z0 * (ZL + 1j * Z0 * tan_bl) / (Z0 + 1j * ZL * tan_bl)
            
            # V_in from voltage divider
            V_in = Vg * Z_in / (Z_in + Zg)
            
            # Gamma calculations
            Gamma_L = (ZL - Z0) / (ZL + Z0)
            Gamma_in = Gamma_L * np.exp(-2j * bl)
            
            # Wave calculation
            V_plus = V_in / (1 + Gamma_in)
            V_L = V_plus * np.exp(-1j * bl) * (1 + Gamma_L)
            return V_L
    formulas.append(Formula(
        'V_L_direct', ['V_L'], ['Vg', 'Zg', 'Z0', 'ZL', 'len_lambda'], V_L_direct,
        'V_L directly from V_g'
    ))
    
    # =========================================================================
    # MEDIUM PROPERTIES
    # =========================================================================
    
    # n = sqrt(eps_r * mu_r)
    def refractive_index(target, **kw):
        if target == 'n':
            mu_r = kw.get('mu_r', 1)
            return np.sqrt(kw['eps_r'] * mu_r)
    formulas.append(Formula(
        'refractive_index', ['n'], ['eps_r'], refractive_index,
        'n = √(ε_r μ_r)'
    ))
    
    # eta = eta0 / sqrt(eps_r) for lossless
    def eta_lossless(target, **kw):
        if target == 'eta':
            eta0 = CONSTANTS['eta0']
            mu_r = kw.get('mu_r', 1)
            return eta0 * np.sqrt(mu_r / kw['eps_r'])
    formulas.append(Formula(
        'eta_lossless', ['eta'], ['eps_r'], eta_lossless,
        'η = η₀√(μ_r/ε_r)'
    ))
    
    # eta from complex eps
    def eta_complex(target, **kw):
        if target == 'eta':
            eta0 = CONSTANTS['eta0']
            mu_r = kw.get('mu_r', 1)
            return eta0 * np.sqrt(mu_r) / np.sqrt(kw['eps_c'] / CONSTANTS['eps0'])
    formulas.append(Formula(
        'eta_complex', ['eta'], ['eps_c'], eta_complex,
        'η = η₀/√(ε_c/ε₀)'
    ))
    
    # up in medium: up = c0 / n
    def up_from_n(target, **kw):
        c0 = CONSTANTS['c0']
        if target == 'up':
            return c0 / kw['n']
        elif target == 'n':
            return c0 / kw['up']
    formulas.append(Formula(
        'up_from_n', ['up', 'n'], ['n', 'up'], up_from_n,
        'u_p = c₀/n'
    ))
    
    # Skin depth: delta_s = sqrt(2 / (omega * mu * sigma))
    def skin_depth(target, **kw):
        if target == 'delta_s':
            mu0 = CONSTANTS['mu0']
            mu_r = kw.get('mu_r', 1)
            mu = mu0 * mu_r
            return np.sqrt(2 / (kw['omega'] * mu * kw['sigma']))
    formulas.append(Formula(
        'skin_depth', ['delta_s'], ['omega', 'sigma'], skin_depth,
        'δ = √(2/(ωμσ))'
    ))
    
    # tan_delta = sigma / (omega * eps)
    def tan_delta_calc(target, **kw):
        eps0 = CONSTANTS['eps0']
        if target == 'tan_delta':
            eps = kw['eps_r'] * eps0
            return kw['sigma'] / (kw['omega'] * eps)
        elif target == 'sigma':
            eps = kw['eps_r'] * eps0
            return kw['tan_delta'] * kw['omega'] * eps
    formulas.append(Formula(
        'tan_delta_calc', ['tan_delta', 'sigma'], ['sigma', 'omega', 'eps_r', 'tan_delta'], tan_delta_calc,
        'tan δ = σ/(ωε)'
    ))
    
    # =========================================================================
    # FRESNEL / INTERFACES
    # =========================================================================
    
    # Normal incidence: Gamma = (n1 - n2) / (n1 + n2)
    def Gamma_normal(target, **kw):
        if target == 'Gamma':
            n1 = np.sqrt(kw.get('eps_r1', 1))
            n2 = np.sqrt(kw['eps_r2'])
            return (n1 - n2) / (n1 + n2)
    formulas.append(Formula(
        'Gamma_normal', ['Gamma'], ['eps_r2'], Gamma_normal,
        'Γ = (n₁-n₂)/(n₁+n₂)'
    ))
    
    # Snell's law: sin(theta_t) = n1/n2 * sin(theta_i)
    def snell_law(target, **kw):
        if target == 'theta_t':
            n1 = np.sqrt(kw.get('eps_r1', 1))
            n2 = np.sqrt(kw['eps_r2'])
            theta_i = kw['theta_i']  # in degrees
            sin_t = n1 / n2 * np.sin(np.radians(theta_i))
            if abs(sin_t) <= 1:
                return np.degrees(np.arcsin(sin_t))
            else:
                return None  # TIR
    formulas.append(Formula(
        'snell_law', ['theta_t'], ['eps_r2', 'theta_i'], snell_law,
        'Snell: sinθ_t = (n₁/n₂)sinθ_i'
    ))
    
    # Brewster angle: tan(theta_B) = n2/n1
    def brewster_angle(target, **kw):
        if target == 'theta_B':
            n1 = np.sqrt(kw.get('eps_r1', 1))
            n2 = np.sqrt(kw['eps_r2'])
            return np.degrees(np.arctan(n2 / n1))
    formulas.append(Formula(
        'brewster', ['theta_B'], ['eps_r2'], brewster_angle,
        'tanθ_B = n₂/n₁'
    ))
    
    # Critical angle: sin(theta_c) = n2/n1
    def critical_angle(target, **kw):
        if target == 'theta_c':
            n1 = np.sqrt(kw.get('eps_r1', 1))
            n2 = np.sqrt(kw['eps_r2'])
            if n1 > n2:
                return np.degrees(np.arcsin(n2 / n1))
            else:
                return None  # No TIR possible
    formulas.append(Formula(
        'critical', ['theta_c'], ['eps_r2'], critical_angle,
        'sinθ_c = n₂/n₁'
    ))
    
    # =========================================================================
    # STATICS
    # =========================================================================
    
    # Parallel plate capacitance: C = eps * A / d
    def C_parallel_plate(target, **kw):
        eps0 = CONSTANTS['eps0']
        eps_r = kw.get('eps_r', 1)
        if target == 'C':
            return eps0 * eps_r * kw['A'] / kw['d']
    formulas.append(Formula(
        'C_parallel_plate', ['C'], ['A', 'd'], C_parallel_plate,
        'C = ε₀ε_r A/d'
    ))
    
    # Coaxial capacitance: C = 2*pi*eps*L / ln(b/a)
    def C_coax(target, **kw):
        eps0 = CONSTANTS['eps0']
        eps_r = kw.get('eps_r', 1)
        if target == 'C':
            return 2 * np.pi * eps0 * eps_r * kw['L'] / np.log(kw['b'] / kw['a'])
    formulas.append(Formula(
        'C_coax', ['C'], ['L', 'a', 'b'], C_coax,
        'C = 2πεL/ln(b/a)'
    ))
    
    # Solenoid inductance: L_ind = mu * N^2 * A / l
    def L_solenoid(target, **kw):
        mu0 = CONSTANTS['mu0']
        mu_r = kw.get('mu_r', 1)
        if target == 'L_ind':
            return mu0 * mu_r * kw['N']**2 * kw['A_sol'] / kw['l_sol']
    formulas.append(Formula(
        'L_solenoid', ['L_ind'], ['N', 'A_sol', 'l_sol'], L_solenoid,
        'L = μN²A/ℓ'
    ))
    
    return formulas


# =============================================================================
# SMART SOLVER CLASS
# =============================================================================
class SmartSolver:
    """
    Iterative physics variable solver.
    
    Feed it known variables, and it solves for everything possible.
    """
    
    def __init__(self):
        self.formulas = build_formula_registry()
        self.known: Dict[str, Any] = {}
        self.solve_log: List[str] = []
        
    def reset(self):
        """Reset solver state."""
        self.known = {}
        self.solve_log = []
    
    def solve(self, input_str: str = None, **kwargs) -> Dict[str, Any]:
        """
        Solve for all possible variables.
        
        Args:
            input_str: String like "f=2G, Z0=50, C_eq=2p"
            **kwargs: Additional variables as keyword arguments
        
        Returns:
            Dictionary of all solved variables
        """
        self.reset()
        
        # Parse input string
        if input_str:
            parsed = parse_input(input_str)
            
            # Handle warnings from material/alias parsing
            if '_warnings' in parsed:
                for warning in parsed['_warnings']:
                    self.solve_log.append(warning)
                del parsed['_warnings']
            
            self.known.update(parsed)
        
        # Add kwargs
        self.known.update(kwargs)
        
        # Add constants to known
        self.known.update(CONSTANTS)
        
        # =====================================================================
        # FEATURE 3: THE DETECTIVE - Heuristic Inference Pre-Processing
        # =====================================================================
        self._run_heuristics()
        
        # Check for stub_type and select appropriate formula
        stub_type = self.known.get('stub_type', None)
        
        # Iterative solving
        max_iterations = 50
        for iteration in range(max_iterations):
            found_new = False
            
            for formula in self.formulas:
                # Skip wrong stub formula
                if stub_type == 'open' and formula.name == 'l_stub_short':
                    continue
                if stub_type == 'short' and formula.name == 'l_stub_open':
                    continue
                
                for output in formula.outputs:
                    # Skip if already known
                    if output in self.known:
                        continue
                    
                    # Check if we can solve
                    if formula.can_solve(self.known, output):
                        try:
                            value = formula.solve(self.known, output)
                            if value is not None:
                                self.known[output] = value
                                self.solve_log.append(f"[{formula.name}] {output} = {self._format_value(value)}")
                                found_new = True
                        except Exception as e:
                            pass  # Skip formulas that error
            
            if not found_new:
                break
        
        # Remove constants from output
        result = {k: v for k, v in self.known.items() if k not in CONSTANTS}
        return result
    
    def _run_heuristics(self):
        """
        FEATURE 3: The Detective - Run heuristic inference rules.
        
        Auto-calculates related variables and makes smart assumptions.
        """
        # ─────────────────────────────────────────────────────────────────────
        # Rule 1: f ↔ omega conversion
        # ─────────────────────────────────────────────────────────────────────
        if 'f' in self.known and 'omega' not in self.known:
            self.known['omega'] = 2 * np.pi * self.known['f']
            self.solve_log.append(f"🔍 [Detective] omega = 2πf = {self.known['omega']:.4g}")
        
        if 'omega' in self.known and 'f' not in self.known:
            self.known['f'] = self.known['omega'] / (2 * np.pi)
            self.solve_log.append(f"🔍 [Detective] f = ω/(2π) = {self.known['f']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 2: lambda + up → f
        # ─────────────────────────────────────────────────────────────────────
        if 'lambda_' in self.known and 'up' in self.known and 'f' not in self.known:
            self.known['f'] = self.known['up'] / self.known['lambda_']
            self.solve_log.append(f"🔍 [Detective] f = u_p/λ = {self.known['f']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 3: up_factor → up
        # ─────────────────────────────────────────────────────────────────────
        if 'up_factor' in self.known and 'up' not in self.known:
            self.known['up'] = self.known['up_factor'] * CONSTANTS['c0']
            self.solve_log.append(f"🔍 [Detective] u_p = {self.known['up_factor']}×c₀ = {self.known['up']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 4: eps_r → up (assuming mu_r = 1)
        # ─────────────────────────────────────────────────────────────────────
        if 'eps_r' in self.known and 'up' not in self.known and 'up_factor' not in self.known:
            mu_r = self.known.get('mu_r', 1)
            n = np.sqrt(self.known['eps_r'] * mu_r)
            self.known['up'] = CONSTANTS['c0'] / n
            self.known['n'] = n
            self.solve_log.append(f"🔍 [Detective] n = √(ε_r) = {n:.4g}, u_p = c₀/n = {self.known['up']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 5: Lossless TL assumption - Z0 and C_prime → L_prime
        # ─────────────────────────────────────────────────────────────────────
        if 'Z0' in self.known and 'C_prime' in self.known and 'L_prime' not in self.known:
            if 'R_prime' not in self.known and 'G_prime' not in self.known:
                # Assume lossless: Z0 = sqrt(L'/C') → L' = Z0² × C'
                self.known['L_prime'] = self.known['Z0']**2 * self.known['C_prime']
                self.solve_log.append(f"⚠️ [Detective] Assuming LOSSLESS line: L' = Z₀²C' = {self.known['L_prime']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 6: Lossless TL assumption - Z0 and L_prime → C_prime
        # ─────────────────────────────────────────────────────────────────────
        if 'Z0' in self.known and 'L_prime' in self.known and 'C_prime' not in self.known:
            if 'R_prime' not in self.known and 'G_prime' not in self.known:
                # Assume lossless: Z0 = sqrt(L'/C') → C' = L'/Z0²
                self.known['C_prime'] = self.known['L_prime'] / self.known['Z0']**2
                self.solve_log.append(f"⚠️ [Detective] Assuming LOSSLESS line: C' = L'/Z₀² = {self.known['C_prime']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 7: Default mu_r = 1 if not specified
        # ─────────────────────────────────────────────────────────────────────
        if 'mu_r' not in self.known:
            self.known['mu_r'] = 1.0
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 8: beta from omega and up
        # ─────────────────────────────────────────────────────────────────────
        if 'omega' in self.known and 'up' in self.known and 'beta' not in self.known:
            self.known['beta'] = self.known['omega'] / self.known['up']
            self.solve_log.append(f"🔍 [Detective] β = ω/u_p = {self.known['beta']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 9: lambda from up and f
        # ─────────────────────────────────────────────────────────────────────
        if 'up' in self.known and 'f' in self.known and 'lambda_' not in self.known:
            self.known['lambda_'] = self.known['up'] / self.known['f']
            self.solve_log.append(f"🔍 [Detective] λ = u_p/f = {self.known['lambda_']:.4g}")
        
        # ─────────────────────────────────────────────────────────────────────
        # Rule 10: Y0 from Z0
        # ─────────────────────────────────────────────────────────────────────
        if 'Z0' in self.known and 'Y0' not in self.known:
            self.known['Y0'] = 1 / self.known['Z0']
            self.solve_log.append(f"🔍 [Detective] Y₀ = 1/Z₀ = {self.known['Y0']:.4g}")
    
    def _format_value(self, value: Any) -> str:
        """Format a value for display."""
        if isinstance(value, complex):
            if value.imag == 0:
                return f"{value.real:.6g}"
            elif value.real == 0:
                return f"{value.imag:.6g}j"
            else:
                return f"{value.real:.6g}{value.imag:+.6g}j"
        elif isinstance(value, float):
            return f"{value:.6g}"
        else:
            return str(value)
    
    def print_results(self, result: Dict[str, Any] = None):
        """Pretty print the results."""
        if result is None:
            result = self.known
        
        print("\n" + "=" * 60)
        print("  SMART SOLVER RESULTS")
        print("=" * 60)
        
        # Group by category
        categories = {
            'Frequency/Wave': ['f', 'omega', 'lambda_', 'beta', 'beta_wave', 'up', 'up_factor', 'n', 'len_lambda'],
            'Transmission Line': ['Z0', 'Y0', 'ZL', 'Zg', 'Z_in', 'Gamma_L', 'Gamma_in', 'VSWR', 'l', 'l_stub'],
            'Voltage/Current': ['Vg', 'V_in', 'V_L', 'I_in', 'I_L'],
            'Medium': ['eps_r', 'eps_c', 'mu_r', 'sigma', 'tan_delta', 'eta', 'delta_s'],
            'Attenuation': ['gamma_wave', 'gamma_line', 'alpha', 'alpha_dB'],
            'RLGC': ['R_prime', 'L_prime', 'G_prime', 'C_prime'],
            'Component': ['C_eq', 'L_eq', 'Y_target', 'Z_target'],
            'Interface': ['Gamma', 'theta_i', 'theta_t', 'theta_B', 'theta_c'],
            'Other': []
        }
        
        printed = set()
        for cat_name, cat_vars in categories.items():
            cat_results = [(k, result[k]) for k in cat_vars if k in result and k not in CONSTANTS]
            if cat_results:
                print(f"\n  {cat_name}:")
                for k, v in cat_results:
                    print(f"    {k:15} = {self._format_value(v)}{self._get_unit(k)}")
                    printed.add(k)
        
        # Print any remaining
        remaining = [(k, v) for k, v in result.items() 
                     if k not in printed and k not in CONSTANTS and not k.startswith('stub_')]
        if remaining:
            print("\n  Other:")
            for k, v in remaining:
                if not isinstance(v, str):  # Skip string params
                    print(f"    {k:15} = {self._format_value(v)}")
        
        print("\n" + "=" * 60)
        
        # Print solve log
        if self.solve_log:
            print("\n  Solve Steps:")
            for step in self.solve_log:
                print(f"    {step}")
            print()
    
    def _get_unit(self, var: str) -> str:
        """Get unit string for a variable."""
        units = {
            'f': ' Hz',
            'omega': ' rad/s',
            'lambda_': ' m',
            'beta': ' rad/m',
            'beta_wave': ' rad/m',
            'up': ' m/s',
            'Z0': ' Ω',
            'Y0': ' S',
            'ZL': ' Ω',
            'Zg': ' Ω',
            'Z_in': ' Ω',
            'Z_target': ' Ω',
            'V_in': ' V',
            'V_L': ' V',
            'Vg': ' V',
            'l': ' m',
            'l_stub': ' m',
            'len_lambda': ' λ',
            'eta': ' Ω',
            'delta_s': ' m',
            'alpha': ' Np/m',
            'alpha_dB': ' dB/m',
            'C_eq': ' F',
            'L_eq': ' H',
            'Y_target': ' S',
            'theta_t': '°',
            'theta_B': '°',
            'theta_c': '°',
        }
        return units.get(var, '')
    
    # =========================================================================
    # FEATURE 4: GOAL SEEKER
    # =========================================================================
    def goal_seek(self, target_var: str, condition_var: str, condition_value: float,
                  search_range: Tuple[float, float] = (0.001, 0.5),
                  base_vars: Dict[str, Any] = None,
                  tolerance: float = 1e-6) -> Dict[str, Any]:
        """
        FEATURE 4: The Goal Seeker - Find value that satisfies a condition.
        
        Example: Find length l that makes Z_in purely real (imag=0)
        
        Args:
            target_var: Variable to vary (e.g., 'len_lambda', 'l')
            condition_var: Variable to check (e.g., 'Z_in')
            condition_value: Target value for condition (e.g., 0 for Z_in.imag)
            search_range: (min, max) range for target_var
            base_vars: Dictionary of other known variables
            tolerance: Acceptable error
        
        Returns:
            Dictionary with solution and all computed variables
        """
        if base_vars is None:
            base_vars = {}
        
        # Parse condition - check for .real or .imag suffix
        condition_part = 'real'  # Default to real part
        if '.' in condition_var:
            condition_var, condition_part = condition_var.rsplit('.', 1)
        
        def objective(x):
            """Objective function to minimize."""
            test_vars = base_vars.copy()
            test_vars[target_var] = x
            
            result = self.solve(**test_vars)
            
            if condition_var not in result:
                return float('inf')
            
            val = result[condition_var]
            
            if condition_part == 'imag':
                actual = np.imag(val)
            elif condition_part == 'real':
                actual = np.real(val)
            elif condition_part == 'abs' or condition_part == 'mag':
                actual = np.abs(val)
            elif condition_part == 'angle' or condition_part == 'phase':
                actual = np.angle(val, deg=True)
            else:
                actual = np.real(val)
            
            return (actual - condition_value) ** 2
        
        # Try to use scipy for optimization
        try:
            from scipy.optimize import minimize_scalar
            
            result = minimize_scalar(objective, bounds=search_range, method='bounded',
                                     options={'xatol': tolerance})
            best_x = result.x
            
        except ImportError:
            # Fallback: Simple grid search
            print("  ⚠ scipy not available, using grid search...")
            
            n_points = 1000
            x_values = np.linspace(search_range[0], search_range[1], n_points)
            best_x = search_range[0]
            best_error = float('inf')
            
            for x in x_values:
                error = objective(x)
                if error < best_error:
                    best_error = error
                    best_x = x
            
            # Refine around best point
            if best_error < float('inf'):
                delta = (search_range[1] - search_range[0]) / n_points
                fine_range = np.linspace(best_x - delta, best_x + delta, 100)
                for x in fine_range:
                    if search_range[0] <= x <= search_range[1]:
                        error = objective(x)
                        if error < best_error:
                            best_error = error
                            best_x = x
        
        # Final solve with best value
        final_vars = base_vars.copy()
        final_vars[target_var] = best_x
        final_result = self.solve(**final_vars)
        
        # Add goal seek info to log
        self.solve_log.insert(0, f"🎯 [Goal Seeker] Found {target_var} = {best_x:.6g}")
        self.solve_log.insert(1, f"🎯 [Goal Seeker] Condition: {condition_var}.{condition_part} ≈ {condition_value}")
        
        return final_result


def parse_solve_command(command: str) -> Tuple[str, str, str, float]:
    """
    Parse a SOLVE command string.
    
    Syntax examples:
        "SOLVE len_lambda FOR Z_in.imag = 0"
        "SOLVE l FOR Z_in.real = 50"
        "SOLVE len_lambda FOR VSWR = 1"
    
    Returns:
        (target_var, condition_var, condition_part, condition_value)
    """
    # Pattern: SOLVE <var> FOR <condition_var>[.part] = <value>
    pattern = r'SOLVE\s+(\w+)\s+FOR\s+([\w_]+)(?:\.(real|imag|abs|mag|angle|phase))?\s*=\s*([-\d.eE+]+)'
    
    match = re.match(pattern, command, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid SOLVE syntax: {command}\n"
                         "Expected: SOLVE <var> FOR <result>[.imag/.real] = <value>")
    
    target_var = match.group(1)
    condition_var = match.group(2)
    condition_part = match.group(3) or 'real'
    condition_value = float(match.group(4))
    
    return target_var, condition_var, condition_part, condition_value


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def list_materials():
    """Print all available materials."""
    print("\n  ═══════════════════════════════════════════════════════════")
    print("       📚 MATERIALS DATABASE")
    print("  ═══════════════════════════════════════════════════════════")
    
    print("\n  DIELECTRICS:")
    for name, props in MATERIALS.items():
        if 'eps_r' in props and 'sigma' not in props:
            desc = props.get('description', '')
            eps_r = props.get('eps_r', '-')
            tan_d = props.get('tan_delta', '-')
            print(f"    {name:12} : ε_r={eps_r}, tan(δ)={tan_d}  [{desc}]")
    
    print("\n  CONDUCTORS:")
    for name, props in MATERIALS.items():
        if 'sigma' in props:
            desc = props.get('description', '')
            sigma = props.get('sigma', '-')
            print(f"    {name:12} : σ={sigma:.2e} S/m  [{desc}]")
    
    print()


def list_aliases():
    """Print all available aliases."""
    print("\n  ═══════════════════════════════════════════════════════════")
    print("       🔤 VARIABLE ALIASES")
    print("  ═══════════════════════════════════════════════════════════")
    
    # Group aliases by canonical name
    canonical_to_aliases = {}
    for alias, canonical in ALIASES.items():
        if canonical not in canonical_to_aliases:
            canonical_to_aliases[canonical] = []
        canonical_to_aliases[canonical].append(alias)
    
    for canonical, aliases in sorted(canonical_to_aliases.items()):
        print(f"    {canonical:12} ← {', '.join(aliases)}")
    
    print()


# =============================================================================
# UNIT TESTS
# =============================================================================
def run_tests():
    """Run the 5 exam unit tests."""
    solver = SmartSolver()
    
    print("\n" + "=" * 70)
    print("  SMART SOLVER - EXAM UNIT TESTS")
    print("=" * 70)
    
    # =========================================================================
    # TEST 1: Inverse Stub (Open stub to realize capacitor)
    # =========================================================================
    print("\n" + "-" * 70)
    print("  TEST 1: Inverse Stub (Open stub for capacitor)")
    print("-" * 70)
    
    result = solver.solve("f=2G, Z0=50, up_factor=0.73, C_eq=2p, stub_type=open")
    
    l_stub = result.get('l_stub', 0)
    l_stub_mm = l_stub * 1000
    print(f"\n  Input:  f=2GHz, Z0=50Ω, up=0.73c₀, C_eq=2pF, open stub")
    print(f"  Result: l_stub = {l_stub_mm:.2f} mm")
    print(f"  Expected: ~5.4 mm (verify)")
    solver.print_results(result)
    
    # =========================================================================
    # TEST 2: RLGC Line
    # =========================================================================
    print("\n" + "-" * 70)
    print("  TEST 2: RLGC Transmission Line")
    print("-" * 70)
    
    result = solver.solve("R_prime=3.112, G_prime=38.9m, L_prime=337.3n, C_prime=61.9p, f=10G")
    
    Z0 = result.get('Z0', 0)
    print(f"\n  Input:  R'=3.112, G'=38.9mS/m, L'=337.3nH/m, C'=61.9pF/m, f=10GHz")
    print(f"  Result: Z0 = {solver._format_value(Z0)} Ω")
    print(f"  Expected: ~73.8 + j0.4 Ω (typical)")
    solver.print_results(result)
    
    # =========================================================================
    # TEST 3: Lossy Wave Attenuation
    # =========================================================================
    print("\n" + "-" * 70)
    print("  TEST 3: Lossy Wave Attenuation")
    print("-" * 70)
    
    result = solver.solve("f=300M, eps_r=4.5, tan_delta=0.02")
    
    alpha_dB = result.get('alpha_dB', 0)
    print(f"\n  Input:  f=300MHz, εr=4.5, tanδ=0.02")
    print(f"  Result: α = {alpha_dB:.4f} dB/m")
    print(f"  Expected: ~0.27 dB/m")
    solver.print_results(result)
    
    # =========================================================================
    # TEST 4: TL Voltages
    # =========================================================================
    print("\n" + "-" * 70)
    print("  TEST 4: Transmission Line Voltages")
    print("-" * 70)
    
    result = solver.solve("Vg=5, Zg=50, Z0=50, ZL=100, len_lambda=0.25")
    
    V_in = result.get('V_in', 0)
    V_L = result.get('V_L', 0)
    print(f"\n  Input:  Vg=5V, Zg=50Ω, Z0=50Ω, ZL=100Ω, ℓ=λ/4")
    print(f"  Result: V_in = {solver._format_value(V_in)} V")
    print(f"          V_L  = {solver._format_value(V_L)} V")
    print(f"  Note: For λ/4, Z_in = Z0²/ZL = 25Ω")
    solver.print_results(result)
    
    # =========================================================================
    # TEST 5: Electrical Length
    # =========================================================================
    print("\n" + "-" * 70)
    print("  TEST 5: Electrical Length")
    print("-" * 70)
    
    result = solver.solve("l=1.2, up_factor=0.73, f=200M")
    
    len_lambda = result.get('len_lambda', 0)
    print(f"\n  Input:  l=1.2m, up=0.73c₀, f=200MHz")
    print(f"  Result: ℓ/λ = {len_lambda:.4f} λ")
    print(f"  Expected: ~1.096 λ")
    solver.print_results(result)
    
    print("\n" + "=" * 70)
    print("  ALL TESTS COMPLETE")
    print("=" * 70 + "\n")


# =============================================================================
# INTERACTIVE MODE
# =============================================================================
def interactive_mode():
    """Run interactive solver session."""
    solver = SmartSolver()
    
    print("\n" + "=" * 65)
    print("  🧠 EM SMART SOLVER - Interactive Mode (v2.0)")
    print("=" * 65)
    print("\n  Enter known variables (e.g., 'f=2G, Z0=50, mat=teflon')")
    print()
    print("  Commands:")
    print("    test      - Run unit tests")
    print("    help      - Show examples")
    print("    materials - List available materials")
    print("    aliases   - List variable aliases")
    print("    SOLVE ... - Goal seek (e.g., 'SOLVE len_lambda FOR Z_in.imag=0')")
    print("    quit      - Exit")
    print()
    
    # Store base variables for SOLVE command
    base_vars = {}
    
    while True:
        try:
            user_input = input("  > ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_input.lower() == 'test':
                run_tests()
                continue
            
            if user_input.lower() in ['materials', 'mat', 'mats']:
                list_materials()
                continue
            
            if user_input.lower() in ['aliases', 'alias', 'vars']:
                list_aliases()
                continue
            
            if user_input.lower() == 'help':
                print("""
  ═══════════════════════════════════════════════════════════════
       📖 SMART SOLVER HELP
  ═══════════════════════════════════════════════════════════════
  
  BASIC EXAMPLES:
  ───────────────
  Stub length:      f=2G, Z0=50, up_factor=0.73, C_eq=2p, stub_type=open
  RLGC line:        R_prime=3.112, G_prime=38.9m, L_prime=337.3n, C_prime=61.9p, f=10G
  Attenuation:      f=300M, eps_r=4.5, tan_delta=0.02
  TL voltages:      Vg=5, Zg=50, Z0=50, ZL=100, len_lambda=0.25
  Electrical len:   l=1.2, up_factor=0.73, f=200M
  
  USING MATERIALS (Feature 2):
  ────────────────────────────
  mat=teflon, f=2G           → Automatically sets eps_r=2.1, tan_delta=0.0002
  cond=copper, f=10G         → Automatically sets sigma=5.8e7
  mat=fr4, f=1G              → Sets PCB properties (eps_r=4.4)
  
  USING ALIASES (Feature 1):
  ──────────────────────────
  freq=2G                    → Same as f=2G
  imp=50                     → Same as Z0=50
  load=100+j50               → Same as ZL=100+j50
  cap=2p                     → Same as C_eq=2p
  
  GOAL SEEKER (Feature 4):
  ────────────────────────
  First, set base variables, then use SOLVE:
  
  > Z0=50, ZL=100+j50, f=1G
    [results shown]
  > SOLVE len_lambda FOR Z_in.imag = 0
    [finds length that makes Z_in purely real]
  
  Syntax: SOLVE <vary_var> FOR <check_var>.<part> = <value>
    Parts: .real, .imag, .abs, .angle
  
  SI PREFIXES:
  ────────────
  p=pico (10⁻¹²), n=nano (10⁻⁹), u=micro (10⁻⁶), m=milli (10⁻³)
  k=kilo (10³), M=mega (10⁶), G=giga (10⁹)
  
  CONSTANTS:
  ──────────
  c, c0 = speed of light     eps0 = vacuum permittivity
  mu0 = vacuum permeability  eta0 = free space impedance (~377 Ω)
  pi = 3.14159...
                """)
                continue
            
            # ─────────────────────────────────────────────────────────────
            # FEATURE 4: Check for SOLVE command
            # ─────────────────────────────────────────────────────────────
            if user_input.upper().startswith('SOLVE'):
                try:
                    target_var, cond_var, cond_part, cond_value = parse_solve_command(user_input)
                    
                    print(f"\n  🎯 Goal Seek: Vary '{target_var}' to make {cond_var}.{cond_part} = {cond_value}")
                    print(f"  Using base variables: {base_vars}")
                    
                    # Determine search range based on variable type
                    if 'lambda' in target_var.lower() or 'len_lambda' in target_var:
                        search_range = (0.001, 0.5)  # 0 to 0.5 wavelengths
                    elif target_var == 'l':
                        search_range = (0.001, 1.0)  # 0 to 1 meter
                    else:
                        search_range = (0.001, 1.0)  # Default
                    
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
            
            # ─────────────────────────────────────────────────────────────
            # Normal solve - also store base variables for future SOLVE
            # ─────────────────────────────────────────────────────────────
            result = solver.solve(user_input)
            
            # Update base_vars with numeric values (for SOLVE command)
            for k, v in result.items():
                if isinstance(v, (int, float, complex)) and k not in CONSTANTS:
                    base_vars[k] = v
            
            solver.print_results(result)
            
        except KeyboardInterrupt:
            print("\n")
            break
        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()


# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            run_tests()
        elif sys.argv[1] == 'materials':
            list_materials()
        elif sys.argv[1] == 'aliases':
            list_aliases()
        else:
            # Solve from command line
            solver = SmartSolver()
            result = solver.solve(' '.join(sys.argv[1:]))
            solver.print_results(result)
    else:
        interactive_mode()
