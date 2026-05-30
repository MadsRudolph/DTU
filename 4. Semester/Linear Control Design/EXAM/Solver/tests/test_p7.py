import pytest

from lcd_solver.solvers.p7_theory import pick_feedforward_form
from tests.oracle_data import THEORY_Q8


def test_Theory_Q8_picks_option_d():
    out = pick_feedforward_form(n_lags=THEORY_Q8["n_lags"], D_order=THEORY_Q8["D_order"])
    assert out["option_label"] == THEORY_Q8["facit_option"]
    assert "min" in out["tau_f_bound"]
    assert "tau_f" in out["tau_f_bound"]
    assert out["filter_order"] == THEORY_Q8["n_lags"] - THEORY_Q8["D_order"]


from lcd_solver.solvers.p7_theory import solve_nested_ess
from tests.oracle_data import THEORY_Q9, THEORY_Q6


def test_Theory_Q9_nested_two_KP():
    KP = solve_nested_ess(
        architecture=THEORY_Q9["architecture"],
        G0=THEORY_Q9["G0"],
        ess_target=THEORY_Q9["ess_target"],
    )
    assert KP == pytest.approx(THEORY_Q9["facit_KP"], rel=1e-3)


def test_Theory_Q6_nested_K1_K2():
    K2 = solve_nested_ess(
        architecture=THEORY_Q6["architecture"],
        eps1=THEORY_Q6["eps1"],
        eps2=THEORY_Q6["eps2"],
        G2_0=THEORY_Q6["G2_0"],
    )
    assert K2 == pytest.approx(THEORY_Q6["facit_K2"], rel=1e-3)
