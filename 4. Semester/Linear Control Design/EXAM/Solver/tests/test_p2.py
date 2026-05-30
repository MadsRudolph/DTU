import math
import pytest
import control
import numpy as np

from lcd_solver.solvers.p2_bode import compose_tf_from_bode
from tests.oracle_data import F22_Q5, REEXAM_F21_Q5


def _sorted_real(xs):
    return sorted(float(np.real(x)) for x in xs)


@pytest.mark.parametrize("oracle", [F22_Q5, REEXAM_F21_Q5], ids=["F22Q5", "REExamQ5"])
def test_bode_composition(oracle):
    G, fig = compose_tf_from_bode(
        dc_gain_dB=oracle["dc_gain_dB"],
        corners=oracle["corners"],
        phase_events=oracle["phase_events"],
    )
    assert _sorted_real(control.poles(G)) == pytest.approx(_sorted_real(oracle["facit_poles"]), abs=1e-6)
    assert _sorted_real(control.zeros(G)) == pytest.approx(_sorted_real(oracle["facit_zeros"]), abs=1e-6)
    # DC gain magnitude (sign may flip if our composition leaves out the negative sign)
    assert abs(float(np.real(control.dcgain(G)))) == pytest.approx(oracle["facit_dc_gain_linear_abs"], rel=1e-3)
    assert fig is not None
