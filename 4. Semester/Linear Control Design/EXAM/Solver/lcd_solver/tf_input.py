"""Parse user-typed transfer function expressions into control.TransferFunction.

Single entry: `parse_tf(expr)`. The widget uses `describe_tf(G)` to echo back
a sanity-check summary below the input field.
"""
from __future__ import annotations
import math
from typing import Any

import control
import numpy as np
import sympy

_S = sympy.Symbol("s")


def parse_tf(expr: str) -> control.TransferFunction:
    """Parse a string like `12/((s+2)*(s+3))` into a control.TransferFunction.

    Accepts sympy syntax (`*`, `**`). Raises ValueError on unparseable input
    or non-rational-in-s expressions.
    """
    try:
        sym_expr = sympy.parse_expr(expr, local_dict={"s": _S})
    except (SyntaxError, sympy.SympifyError, TypeError, ValueError) as e:
        raise ValueError(f"Could not parse {expr!r}: {e}") from e

    # Reject expressions that introduce symbols other than `s` (e.g. "not a transfer function"
    # parses as the boolean `Not(...)` over free symbols).
    free = sym_expr.free_symbols - {_S}
    if free:
        raise ValueError(
            f"{expr!r} contains unknown symbols {sorted(str(x) for x in free)}; "
            f"only `s` is allowed."
        )

    rational = sympy.cancel(sympy.together(sym_expr))
    num_expr, den_expr = sympy.fraction(rational)

    try:
        num_coeffs = [float(c) for c in sympy.Poly(num_expr, _S).all_coeffs()]
        den_coeffs = [float(c) for c in sympy.Poly(den_expr, _S).all_coeffs()]
    except (sympy.PolynomialError, TypeError) as e:
        raise ValueError(f"{expr!r} is not a rational function in s: {e}") from e

    return control.tf(num_coeffs, den_coeffs)


def describe_tf(G: control.TransferFunction) -> dict[str, Any]:
    """Sanity-check summary for the widget.

    Returns dict with: poles, zeros, dc_gain_linear, dc_gain_dB, has_rhp_pole.
    DC gain is set to math.nan if the system has a pole at the origin (integrator).
    """
    poles = list(control.poles(G))
    zeros = list(control.zeros(G))
    has_rhp_pole = any(p.real > 1e-9 for p in poles)

    if any(abs(p) < 1e-9 for p in poles):
        dc_linear = math.nan
        dc_dB = math.nan
    else:
        dc_linear = float(np.real(control.dcgain(G)))
        dc_dB = 20 * math.log10(abs(dc_linear)) if abs(dc_linear) > 0 else float("-inf")

    return {
        "poles": poles,
        "zeros": zeros,
        "dc_gain_linear": dc_linear,
        "dc_gain_dB": dc_dB,
        "has_rhp_pole": has_rhp_pole,
    }
