import pytest

from lcd_solver.solvers.p7_theory import pick_feedforward_form
from tests.oracle_data import THEORY_Q8


def test_Theory_Q8_picks_option_d():
    out = pick_feedforward_form(n_lags=THEORY_Q8["n_lags"], D_order=THEORY_Q8["D_order"])
    assert out["option_label"] == THEORY_Q8["facit_option"]
    assert "min" in out["tau_f_bound"]
    assert "tau_f" in out["tau_f_bound"]
    assert out["filter_order"] == THEORY_Q8["n_lags"] - THEORY_Q8["D_order"]
