"""Solver result envelope and result-kind enum."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ResultKind(str, Enum):
    NUMBER = "number"   # solver returns a single float
    TF     = "tf"       # solver returns a sympy.Expr (block reduction) or control.TF (Bode compose)
    DICT   = "dict"     # solver returns dict[str, float]
    PICK   = "pick"     # solver returns a structural choice (formula text + condition)


@dataclass
class Result:
    """What every solver returns. Carries the answer + metadata for matching/UI."""
    value: Any
    kind: ResultKind
    traps_hit: list[str] = field(default_factory=list)
    plot_data: Any = None  # matplotlib Figure or None; UI inspects only for is-None
