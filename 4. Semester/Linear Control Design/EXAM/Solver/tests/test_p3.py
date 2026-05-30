import math
import pytest

from lcd_solver.tf_input import parse_tf
from lcd_solver.solvers.p3_stability import solve_stable_K_range
from tests.oracle_data import S21_Q4, REEXAM_F21_Q14


def test_S21_Q4_stable_plant():
    G = parse_tf(S21_Q4["G"])
    low, high = solve_stable_K_range(G)
    assert low == pytest.approx(S21_Q4["facit_low"], abs=1e-9)
    assert high == pytest.approx(S21_Q4["facit_high"], rel=1e-3)


def test_REExam_Q14_stable_plant_low_GM():
    G = parse_tf(REEXAM_F21_Q14["G"])
    low, high = solve_stable_K_range(G)
    assert low == 0.0
    assert high == pytest.approx(REEXAM_F21_Q14["facit_high"], rel=1e-2)


def test_unstable_plant_inverts_range():
    # Plant: (s+10)/((s-1)(s+5)) — RHP pole at +1, LHP zero at -10.
    # DC = -10/-5 = -2 → K_min = 1/|G(0)| = 0.5. Verified via Routh: stable for K > 0.5.
    G = parse_tf("(s+10) / ((s-1)*(s+5))")
    low, high = solve_stable_K_range(G)
    assert math.isinf(high), "unstable plant must yield K_high = inf"
    assert low > 0, f"K_min must be positive, got {low}"
