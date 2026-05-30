"""P4 — 2nd-order specs: bidirectional Mp <-> zeta and the time/freq spec set."""
from __future__ import annotations
import math


def _Mp_from_zeta(zeta: float) -> float:
    if zeta <= 0 or zeta >= 1:
        return 0.0
    return math.exp(-math.pi * zeta / math.sqrt(1 - zeta ** 2))


def _zeta_from_Mp(Mp: float) -> float:
    if Mp <= 0:
        return 1.0
    L = math.log(1 / Mp)
    return L / math.sqrt(math.pi ** 2 + L ** 2)


def solve_2nd_order(*, Mp=None, zeta=None, omega_n=None, t_p=None, t_s_2pct=None) -> dict:
    """Fill in whichever 2nd-order quantities are derivable.

    Accept any subset of {Mp, zeta} and any subset of {omega_n, t_p, t_s_2pct}.
    Inconsistent inputs raise ValueError.
    """
    # ---- damping ----
    if Mp is not None and zeta is not None:
        if abs(_zeta_from_Mp(Mp) - zeta) > 1e-2:
            raise ValueError(f"Mp={Mp} and zeta={zeta} are inconsistent")
    if zeta is None and Mp is not None:
        zeta = _zeta_from_Mp(Mp)
    elif zeta is not None and Mp is None:
        Mp = _Mp_from_zeta(zeta)
    elif zeta is None and Mp is None:
        raise ValueError("Provide at least one of {Mp, zeta}")

    # ---- omega_n ----
    if omega_n is None:
        if t_p is not None and zeta < 1:
            omega_n = math.pi / (t_p * math.sqrt(1 - zeta ** 2))
        elif t_s_2pct is not None:
            omega_n = 4.0 / (zeta * t_s_2pct)

    out = {"zeta": zeta, "Mp": Mp, "Mp_pct": 100 * Mp}
    if omega_n is None:
        return out

    out["omega_n"] = omega_n
    out["omega_d"] = omega_n * math.sqrt(max(0.0, 1 - zeta ** 2))
    out["t_p"] = math.pi / out["omega_d"] if out["omega_d"] > 0 else math.inf
    out["t_s_2pct"] = 4.0 / (zeta * omega_n) if zeta > 0 else math.inf
    out["t_s_5pct"] = 3.0 / (zeta * omega_n) if zeta > 0 else math.inf
    out["t_r"] = 1.8 / omega_n
    out["omega_BW"] = omega_n * math.sqrt(
        (1 - 2 * zeta ** 2) + math.sqrt(4 * zeta ** 4 - 4 * zeta ** 2 + 2)
    )
    if zeta < math.sqrt(2) / 2:
        out["omega_r"] = omega_n * math.sqrt(1 - 2 * zeta ** 2)
        out["M_r"] = 1 / (2 * zeta * math.sqrt(1 - zeta ** 2))
    return out


import re
import sympy


def solve_K_for_spec(G_str: str, spec: str) -> float:
    """Closed-loop K/(s(s+a))-style plants only (v1 limitation).

    spec ∈ {"Mp <= X", "zeta >= X"}.
    Returns the K boundary (upper bound for Mp<=, upper bound for zeta>=).
    """
    s, K = sympy.symbols("s K", positive=True)
    G = sympy.sympify(G_str, locals={"s": s, "K": K})
    Gcl = sympy.cancel(G / (1 + G))
    # Express as wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
    num, den = sympy.fraction(Gcl)
    den_poly = sympy.Poly(den, s)
    coeffs = den_poly.all_coeffs()
    if len(coeffs) != 3:
        raise NotImplementedError(
            "solve_K_for_spec v1 only handles 2nd-order-reducible closed loops"
        )
    a2, a1, a0 = coeffs
    # Normalise so leading coeff is 1
    a1_n = a1 / a2
    a0_n = a0 / a2
    # omega_n^2 = a0_n, 2*zeta*omega_n = a1_n
    wn = sympy.sqrt(a0_n)
    zeta_expr = a1_n / (2 * wn)

    m = re.match(r"\s*(Mp|zeta)\s*(<=|>=)\s*([\d.eE+-]+)\s*$", spec)
    if not m:
        raise ValueError(f"Unrecognised spec: {spec!r}")
    var, op, val = m.group(1), m.group(2), float(m.group(3))

    if var == "Mp":
        zeta_req = _zeta_from_Mp(val)  # ζ ≥ zeta_req
    else:
        zeta_req = val

    # Solve zeta_expr == zeta_req for K → that's the boundary
    eq = sympy.Eq(zeta_expr, zeta_req)
    sols = [sol for sol in sympy.solve(eq, K, positive=True) if sol.is_real]
    if not sols:
        raise ValueError(f"No positive real K satisfies the spec boundary {spec!r}")
    return float(max(sols))
