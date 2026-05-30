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


def solve_closed_loop_2nd_order(closed_loop_str: str, given_kind: str, given_value: float) -> dict:
    """Given a parametric closed-loop TF and one known 2nd-order metric, return the full table.

    Combines the symbolic K-extraction from solve_K_for_spec with the metric
    derivation from solve_2nd_order. Use when the exam gives you a closed-loop
    expression in (s, K) plus one spec value (Mp, zeta, omega_n, omega_d, t_p, t_s_2pct, or K).

    closed_loop_str: e.g. "K / (s**2 + 2*s + K)" — may use literal numbers in place of K
                     if K is already known (then use given_kind="K", given_value=K_known).
    given_kind: one of {"Mp", "zeta", "omega_n", "omega_d", "t_p", "t_s_2pct", "K"}
    given_value: the known numeric value of that metric.

    Returns a dict with K, zeta, Mp, Mp_pct, omega_n, omega_d, t_p, t_s_2pct, t_s_5pct,
    t_r, omega_BW (+ omega_r, M_r if underdamped enough).
    """
    s, K = sympy.symbols("s K", positive=True, real=True)
    Gcl = sympy.sympify(closed_loop_str, locals={"s": s, "K": K})
    _num, den = sympy.fraction(sympy.cancel(sympy.together(Gcl)))
    coeffs = sympy.Poly(den, s).all_coeffs()
    if len(coeffs) != 3:
        raise NotImplementedError(
            "solve_closed_loop_2nd_order requires a 2nd-order denominator. "
            f"Got order {len(coeffs)-1} from {closed_loop_str!r}."
        )
    a2, a1, a0 = coeffs
    # wn^2 = a0/a2, 2*zeta*wn = a1/a2  → both possibly depend on K
    wn_sq_expr = sympy.simplify(a0 / a2)
    wn_expr = sympy.sqrt(wn_sq_expr)
    zeta_expr = sympy.simplify((a1 / a2) / (2 * wn_expr))

    # Solve for K from the given metric. omega_d = wn * sqrt(1 - zeta^2).
    if given_kind == "K":
        K_val = float(given_value)
    else:
        if given_kind == "Mp":
            target_zeta = _zeta_from_Mp(float(given_value))
            eq = sympy.Eq(zeta_expr, target_zeta)
        elif given_kind == "zeta":
            eq = sympy.Eq(zeta_expr, float(given_value))
        elif given_kind == "omega_n":
            eq = sympy.Eq(wn_expr, float(given_value))
        elif given_kind == "omega_d":
            omega_d_expr = wn_expr * sympy.sqrt(1 - zeta_expr ** 2)
            eq = sympy.Eq(omega_d_expr, float(given_value))
        elif given_kind == "t_p":
            omega_d_expr = wn_expr * sympy.sqrt(1 - zeta_expr ** 2)
            eq = sympy.Eq(sympy.pi / omega_d_expr, float(given_value))
        elif given_kind == "t_s_2pct":
            sigma_expr = wn_expr * zeta_expr
            eq = sympy.Eq(4 / sigma_expr, float(given_value))
        else:
            raise ValueError(
                f"given_kind must be one of {{Mp, zeta, omega_n, omega_d, t_p, t_s_2pct, K}}, "
                f"got {given_kind!r}"
            )
        sols = [s_ for s_ in sympy.solve(eq, K, positive=True) if s_.is_real]
        if not sols:
            raise ValueError(
                f"No positive real K satisfies {given_kind}={given_value} for {closed_loop_str!r}"
            )
        # Prefer the smallest positive real K that produces a physical (underdamped) closed loop
        K_val = float(min(sols, key=lambda x: float(x)))

    wn_val = float(wn_expr.subs(K, K_val))
    zeta_val = float(zeta_expr.subs(K, K_val))

    out = solve_2nd_order(zeta=zeta_val, omega_n=wn_val)
    out["K"] = K_val
    return out
