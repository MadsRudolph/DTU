import pytest
import numpy as np
import control

from lcd_solver.solvers.p1_models import solve_ode_to_tf
from tests.oracle_data import F22_Q8, S21_Q8, THEORY_Q4


def _sorted_poles(G):
    return sorted(control.poles(G), key=lambda p: (round(p.real, 6), round(p.imag, 6)))


def _close(actual, expected, atol=1e-3):
    actual = _sorted_poles(actual)
    expected = sorted(expected, key=lambda p: (round(p.real, 6), round(p.imag, 6)))
    assert len(actual) == len(expected)
    for a, e in zip(actual, expected):
        assert abs(a - e) < atol, f"pole {a} ≠ {e}"


def test_F22_Q8_ode_to_poles():
    G = solve_ode_to_tf(F22_Q8["y_coeffs"], F22_Q8["u_coeffs"])
    _close(G, F22_Q8["facit_poles"])


def test_S21_Q8_ode_to_poles():
    G = solve_ode_to_tf(S21_Q8["y_coeffs"], S21_Q8["u_coeffs"])
    _close(G, S21_Q8["facit_poles"])


def test_Theory_Q4_ode_to_poles():
    G = solve_ode_to_tf(THEORY_Q4["y_coeffs"], THEORY_Q4["u_coeffs"])
    _close(G, THEORY_Q4["facit_poles"])


from lcd_solver.solvers.p1_models import solve_state_space_to_tf
from tests.oracle_data import REEXAM_F21_Q6


def test_REExam_F21_Q6_ss_to_tf():
    o = REEXAM_F21_Q6
    G = solve_state_space_to_tf(o["A"], o["B"], o["C"], o["D"])
    assert float(control.dcgain(G).real) == pytest.approx(o["facit_dc_gain"], rel=1e-6)
    poles = sorted(control.poles(G), key=lambda p: (p.real, p.imag))
    assert all(abs(p - (-1.0)) < 1e-9 for p in poles)


import sympy

from lcd_solver.solvers.p1_block_reduce import reduce_block_diagram, DSL_PRIMITIVES
from tests.oracle_data import S20_Q3, S21_Q1


def _eq(a_str: str, b_str: str) -> bool:
    a = sympy.sympify(a_str)
    b = sympy.sympify(b_str)
    return sympy.simplify(a - b) == 0


def test_S20_Q3_parallel_with_feedback():
    got = reduce_block_diagram(S20_Q3["dsl"])
    assert _eq(str(got), S20_Q3["facit_str"]), f"got {got}"


def test_S21_Q1_two_forward_shared_feedback():
    got = reduce_block_diagram(S21_Q1["dsl"])
    assert _eq(str(got), S21_Q1["facit_str"]), f"got {got}"


def test_dsl_primitives_exist():
    # Each primitive callable should be available for the parser
    assert set(DSL_PRIMITIVES) >= {"series", "parallel", "feedback"}


def test_basic_series_parallel_feedback():
    A, B, C, D = sympy.symbols("A B C D")
    got = reduce_block_diagram("feedback(series(A, B, C), D)")
    expected = A * B * C / (1 + A * B * C * D)
    assert sympy.simplify(got - expected) == 0


def test_positive_feedback_sign():
    A, B = sympy.symbols("A B")
    got = reduce_block_diagram("feedback(A, B, sign=1)")
    expected = A / (1 - A * B)
    assert sympy.simplify(got - expected) == 0
