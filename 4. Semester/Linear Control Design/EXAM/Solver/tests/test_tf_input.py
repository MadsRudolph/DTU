import math
import pytest
import control
import sympy

from lcd_solver.tf_input import parse_tf, describe_tf


def test_parse_factored_form():
    G = parse_tf("12 / ((s+2)*(s+3))")
    assert float(control.dcgain(G)) == pytest.approx(2.0, rel=1e-6)
    assert sorted([float(p.real) for p in control.poles(G)]) == pytest.approx([-3.0, -2.0])


def test_parse_polynomial_form():
    G = parse_tf("25 / (s**3 + s**2 + 10*s)")
    poles = sorted(control.poles(G), key=lambda p: (p.real, p.imag))
    assert any(abs(p) < 1e-9 for p in poles), "missing integrator at origin"


def test_parse_rhp_pole_is_flagged():
    G = parse_tf("100*(s+10) / (s-1)")
    desc = describe_tf(G)
    assert desc["has_rhp_pole"] is True
    assert any(p.real > 0 for p in desc["poles"])


def test_parse_dc_gain_dB_matches_linear():
    G = parse_tf("12 / ((s+2)*(s+3))")
    desc = describe_tf(G)
    assert desc["dc_gain_linear"] == pytest.approx(2.0, rel=1e-6)
    assert desc["dc_gain_dB"] == pytest.approx(20 * math.log10(2.0), rel=1e-4)


def test_parse_rejects_garbage():
    with pytest.raises(ValueError):
        parse_tf("not a transfer function")
