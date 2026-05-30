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
