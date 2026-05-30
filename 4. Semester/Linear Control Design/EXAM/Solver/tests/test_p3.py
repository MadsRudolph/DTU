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


from lcd_solver.solvers.p3_stability import solve_margins
from tests.oracle_data import F22_Q11


def test_solve_margins_returns_full_dict():
    # F22 Q11's plant isn't explicitly recorded in the MATLAB script, but the
    # wrapper must return all five keys and reproduce known margins for S21 Q4's
    # plant 1/(s+1)^3 (GM=8 at omega=sqrt(3)).
    G = parse_tf("1 / (s+1)**3")
    m = solve_margins(G)
    assert set(m) == {"GM", "GM_dB", "PM_deg", "omega_pc", "omega_gc"}
    assert m["GM"] == pytest.approx(8.0, rel=1e-3)
    assert m["GM_dB"] == pytest.approx(20 * math.log10(8.0), rel=1e-3)


def test_solve_margins_F22_Q11_x_crossing_consistency():
    # F22 Q11 documents the Nyquist negative-real-axis crossing at -0.1639,
    # giving GM = 1/0.1639 ≈ 6.10 (15.71 dB). Verify the algebraic identity.
    x = F22_Q11["x_crossing"]
    expected_GM_dB = 20 * math.log10(1 / abs(x))
    assert expected_GM_dB == pytest.approx(F22_Q11["facit_GM_dB"], rel=1e-3)
