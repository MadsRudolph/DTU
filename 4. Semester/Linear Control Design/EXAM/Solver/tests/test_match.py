import pytest
import sympy

from lcd_solver.match import match
from lcd_solver.types import Result, ResultKind


def test_number_match_picks_closest():
    result = Result(value=2.0, kind=ResultKind.NUMBER)
    options = match(result, "5\n2.0\n0.4\n0.555")
    flags = [o.flag for o in options]
    assert flags == ["no_match", "match", "no_match", "no_match"]


def test_number_match_accepts_db_suffix():
    # -7.9588 dB → linear 0.4
    result = Result(value=0.4, kind=ResultKind.NUMBER)
    options = match(result, "-7.9588 dB\n0.5\n2.0")
    assert options[0].flag == "match"
    assert options[0].parsed == pytest.approx(0.4, rel=1e-3)


def test_number_match_flags_also_plausible_within_1pct():
    result = Result(value=1.57, kind=ResultKind.NUMBER)
    options = match(result, "1.55\n1.57\n1.60\n2.0")
    flags = [o.flag for o in options]
    assert flags[1] == "match"
    assert flags[0] == "no_match"


def test_tf_match_recognises_canonical_equivalents():
    A, B = sympy.symbols("A B")
    result = Result(value=A * B / (1 + A * B), kind=ResultKind.TF)
    options = match(result, "A*B/(A*B+1)\nA*B\n1/(1+A*B)")
    assert options[0].flag == "match"
    assert options[1].flag == "no_match"


def test_dict_match_uses_selected_key():
    result = Result(value={"K_P": 2.0, "omega_c": 25.0}, kind=ResultKind.DICT)
    options = match(result, "1.0\n2.0\n3.0", match_key="K_P")
    assert options[1].flag == "match"


def test_unparseable_option_is_flagged():
    result = Result(value=2.0, kind=ResultKind.NUMBER)
    options = match(result, "2.0\ngibberish")
    assert options[0].flag == "match"
    assert options[1].flag == "unparseable"
