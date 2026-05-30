import pytest

from lcd_solver.solvers.p5_ess import solve_KP_from_ess
from tests.oracle_data import F22_Q16


def test_F22_Q16_KP_from_ess():
    KP = solve_KP_from_ess(F22_Q16["G0"], F22_Q16["G0_unit"], F22_Q16["ess_target"])
    assert KP == pytest.approx(F22_Q16["facit_KP"], rel=1e-3)


def test_linear_input_passes_through():
    # ess = 1/(1+K_P*G0) = 1/(1+2*0.4) = 5/9; check the formula inverts cleanly.
    KP = solve_KP_from_ess(0.4, "linear", 5.0 / 9.0)
    assert KP == pytest.approx(2.0, rel=1e-3)


def test_invalid_unit_raises():
    with pytest.raises(ValueError):
        solve_KP_from_ess(0.4, "bogus", 0.5)


from lcd_solver.tf_input import parse_tf
from lcd_solver.solvers.p5_ess import solve_ess_table
from tests.oracle_data import REEXAM_F21_Q4


def test_REExam_F21_Q4_type2_ess_table():
    G = parse_tf(REEXAM_F21_Q4["G_str"])
    t = solve_ess_table(G)
    assert t["type"] == REEXAM_F21_Q4["facit_type"]
    assert t["ess_step"] == pytest.approx(REEXAM_F21_Q4["facit_ess_step"], abs=1e-9)
    assert t["ess_ramp"] == pytest.approx(REEXAM_F21_Q4["facit_ess_ramp"], abs=1e-9)
    assert t["ess_parabola"] == pytest.approx(REEXAM_F21_Q4["facit_ess_parabola"], rel=1e-3)
