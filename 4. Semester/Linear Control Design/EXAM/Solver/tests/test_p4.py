import math
import pytest

from lcd_solver.solvers.p4_secondorder import solve_2nd_order
from tests.oracle_data import REEXAM_F21_Q10, F22_Q10, S20_Q5


def test_zeta_to_Mp_REExam_Q10():
    out = solve_2nd_order(zeta=REEXAM_F21_Q10["zeta"])
    assert out["Mp_pct"] == pytest.approx(REEXAM_F21_Q10["facit_Mp_pct"], rel=1e-2)


def test_Mp_to_zeta_S20_Q5():
    Mp = (S20_Q5["y_peak"] - S20_Q5["y_ss"]) / S20_Q5["y_ss"]
    out = solve_2nd_order(Mp=Mp)
    assert out["zeta"] == pytest.approx(S20_Q5["facit_zeta_approx"], abs=0.05)


def test_t_p_with_omega_n():
    out = solve_2nd_order(zeta=0.5, omega_n=10.0)
    assert out["t_p"] == pytest.approx(math.pi / (10.0 * math.sqrt(1 - 0.25)), rel=1e-6)
    assert out["t_s_2pct"] == pytest.approx(4.0 / (0.5 * 10.0), rel=1e-6)


def test_inconsistent_inputs_raise():
    with pytest.raises(ValueError):
        solve_2nd_order(Mp=0.5, zeta=0.7)  # Mp=0.5 implies zeta ≈ 0.215, not 0.7
