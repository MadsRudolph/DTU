"""P1 — Block diagram reduction via a tiny symbolic DSL.

Three primitives:
  series(*blocks)              -> product of blocks
  parallel(*blocks)            -> sum of blocks
  feedback(forward, fb_path, sign=-1)
      -> forward / (1 - sign * forward * fb_path)
        (sign=-1 -> negative feedback -> forward / (1 + forward * fb_path))
        (sign=+1 -> positive feedback -> forward / (1 - forward * fb_path))

Block names appearing in the DSL string become sympy.Symbol's automatically.
"""
from __future__ import annotations
from functools import reduce
from operator import mul, add

import sympy


def _series(*blocks):
    return reduce(mul, blocks, sympy.Integer(1))


def _parallel(*blocks):
    return reduce(add, blocks, sympy.Integer(0))


def _feedback(forward, fb_path, sign=-1):
    return forward / (1 - sign * forward * fb_path)


DSL_PRIMITIVES = {
    "series": _series,
    "parallel": _parallel,
    "feedback": _feedback,
}


def reduce_block_diagram(dsl_expr: str) -> sympy.Expr:
    """Evaluate a DSL expression and return the canonical simplified TF.

    Undeclared identifiers (A, B, C, ...) become fresh sympy.Symbol's via
    parse_expr's auto-symbolisation.
    """
    s = sympy.Symbol("s")
    parsed = sympy.parse_expr(
        dsl_expr,
        local_dict={**DSL_PRIMITIVES, "s": s},
    )
    return sympy.cancel(sympy.together(parsed))
