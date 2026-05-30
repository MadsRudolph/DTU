"""Type-aware option matching.

Each solver returns a Result(value, kind, ...). The match() function parses
the user's pasted options text per Result.kind and ranks each option."""
from __future__ import annotations
import math
import re
from dataclasses import dataclass
from typing import Any

import sympy

from lcd_solver.types import Result, ResultKind


_DB_SUFFIX = re.compile(r"^\s*(.+?)\s*dB\s*$", re.IGNORECASE)


@dataclass
class Option:
    raw_text: str
    parsed: Any
    distance: float | None
    flag: str  # "match" | "also_plausible" | "no_match" | "unparseable"
    note: str = ""  # e.g. matched-against-key when auto-matching a DICT result


def _parse_number(raw: str) -> float:
    """Accept '5', '-7.9588 dB', '1/2', 'pi/4', etc."""
    m = _DB_SUFFIX.match(raw)
    if m:
        inner = float(sympy.sympify(m.group(1)))
        return 10 ** (inner / 20)
    return float(sympy.sympify(raw))


def _parse_sym(raw: str) -> sympy.Expr:
    return sympy.cancel(sympy.together(sympy.sympify(raw)))


def match(result: Result, options_text: str, match_key: str | None = None) -> list[Option]:
    """Parse the user's options block and rank against result.value."""
    lines = [ln.strip() for ln in options_text.splitlines() if ln.strip()]

    if result.kind == ResultKind.NUMBER:
        return _match_number(float(result.value), lines)
    if result.kind == ResultKind.TF:
        return _match_tf(result.value, lines)
    if result.kind == ResultKind.DICT:
        if match_key in (None, "", "auto"):
            return _match_dict_auto(result.value, lines)
        return _match_number(float(result.value[match_key]), lines)
    if result.kind == ResultKind.PICK:
        # PICK: solver returns canonical text; no symbolic option comparison
        return [Option(raw_text=ln, parsed=None, distance=None, flag="no_match") for ln in lines]
    raise ValueError(f"unknown kind {result.kind}")


def _match_number(target: float, lines: list[str]) -> list[Option]:
    options: list[Option] = []
    for ln in lines:
        try:
            val = _parse_number(ln)
        except (ValueError, TypeError, sympy.SympifyError):
            options.append(Option(raw_text=ln, parsed=None, distance=None, flag="unparseable"))
            continue
        # Avoid division by zero for target ~ 0
        denom = abs(target) if abs(target) > 1e-12 else 1.0
        dist = abs(val - target) / denom
        options.append(Option(raw_text=ln, parsed=val, distance=dist, flag="no_match"))

    # Rank parseable by distance
    parseable = [o for o in options if o.distance is not None]
    if parseable:
        winner = min(parseable, key=lambda o: o.distance)
        winner.flag = "match"
        for o in parseable:
            if o is not winner and o.distance < 0.01:
                o.flag = "also_plausible"
    return options


def _match_dict_auto(result_dict: dict, lines: list[str]) -> list[Option]:
    """Auto-mode for DICT results.

    For each option, find every dict key it's near (within 5%). Annotate the note
    with all near matches and their distances. Crown a single 'match' only when
    one option is tightly (<1%) and uniquely matched — otherwise surface all
    plausible options and let the user pick the metric explicitly. This is
    deliberately conservative because exam distractors are designed to look
    like other metrics in the same problem (e.g. t_r ≈ ω_d for some ζ).
    """
    TIGHT = 0.01   # 1% — single-winner threshold
    SOFT = 0.05    # 5% — surface as also_plausible

    numeric_items = [(k, float(v)) for k, v in result_dict.items()
                     if isinstance(v, (int, float)) and not isinstance(v, bool)
                     and math.isfinite(float(v))]
    if not numeric_items:
        return [Option(raw_text=ln, parsed=None, distance=None, flag="no_match") for ln in lines]

    options: list[Option] = []
    for ln in lines:
        try:
            val = _parse_number(ln)
        except (ValueError, TypeError, sympy.SympifyError):
            options.append(Option(raw_text=ln, parsed=None, distance=None, flag="unparseable"))
            continue
        # Score against every key
        scored = []
        for k, target in numeric_items:
            denom = abs(target) if abs(target) > 1e-12 else 1.0
            d = abs(val - target) / denom
            scored.append((k, d))
        scored.sort(key=lambda x: x[1])
        best_key, best_dist = scored[0]
        # Build a note that mentions all keys within SOFT — that's the "feels like AI" hint
        near = [(k, d) for k, d in scored if d < SOFT]
        if near:
            note = "near: " + ", ".join(f"{k} (Δ={d:.1%})" for k, d in near)
        else:
            note = f"closest: {best_key} (Δ={best_dist:.1%})"
        options.append(Option(
            raw_text=ln, parsed=val, distance=best_dist, flag="no_match", note=note,
        ))

    parseable = [o for o in options if o.distance is not None]
    if not parseable:
        return options

    # Tight matches: option within 1% of its best key
    tight = [o for o in parseable if o.distance < TIGHT]
    if len(tight) == 1:
        # Single unambiguous winner
        tight[0].flag = "match"
        tight[0].note = "match — " + tight[0].note
    elif len(tight) > 1:
        # Multiple tight matches → ambiguous: surface all
        for o in tight:
            o.flag = "also_plausible"
            o.note = "ambiguous — " + o.note
    # Otherwise: no winner crowned. Mark soft matches as also_plausible.
    for o in parseable:
        if o.flag == "no_match" and o.distance < SOFT:
            o.flag = "also_plausible"
    return options


def _match_tf(target: Any, lines: list[str]) -> list[Option]:
    """Symbolic equality. Accepts sympy.Expr or control.TransferFunction."""
    # Coerce control.TF -> sympy expression if needed
    target_sym = target if isinstance(target, sympy.Expr) else _control_tf_to_sympy(target)
    options: list[Option] = []
    for ln in lines:
        try:
            opt = _parse_sym(ln)
        except (ValueError, TypeError, sympy.SympifyError):
            options.append(Option(raw_text=ln, parsed=None, distance=None, flag="unparseable"))
            continue
        try:
            eq = sympy.simplify(opt - target_sym) == 0
        except Exception:
            eq = False
        flag = "match" if eq else "no_match"
        options.append(Option(raw_text=ln, parsed=opt, distance=None, flag=flag))
    return options


def _control_tf_to_sympy(G) -> sympy.Expr:
    import control
    s = sympy.Symbol("s")
    num = sum(c * s ** i for i, c in enumerate(reversed(list(G.num[0][0]))))
    den = sum(c * s ** i for i, c in enumerate(reversed(list(G.den[0][0]))))
    return sympy.cancel(num / den)
