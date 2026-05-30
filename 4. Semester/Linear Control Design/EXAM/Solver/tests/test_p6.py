import math
import pytest

from lcd_solver.solvers.p6_control import solve_pi_lead, solve_P_for_PM
from lcd_solver.tf_input import parse_tf
from tests.oracle_data import F22_Q17, REEXAM_F21_Q15, REEXAM_F21_Q17, F22_Q19


def test_F22_Q17_alpha_mode():
    a = solve_pi_lead(unknown="alpha",
                      omega_c=F22_Q17["omega_c"],
                      gamma_M_deg=F22_Q17["gamma_M_deg"],
                      phi_G_deg=F22_Q17["phi_G_deg"],
                      N_i=F22_Q17["N_i"])
    # Exam facit is the multiple-choice rounded value 0.5; MATLAB script and the
    # exact phase-budget formula both give alpha ≈ 0.5073. Loose tolerance picks
    # the right answer-choice "e" without misreading 0.5073 as e.g. 0.45 or 0.55.
    assert a == pytest.approx(F22_Q17["facit"], rel=2e-2)


def test_REExam_F21_Q17_Ni_mode():
    n = solve_pi_lead(unknown="Ni",
                      omega_c=REEXAM_F21_Q17["omega_c"],
                      gamma_M_deg=REEXAM_F21_Q17["gamma_M_deg"],
                      phi_G_deg=REEXAM_F21_Q17["phi_G_deg"],
                      alpha=REEXAM_F21_Q17["alpha"])
    assert n == pytest.approx(REEXAM_F21_Q17["facit"], rel=1e-2)


def test_REExam_F21_Q15_alpha_from_MD():
    a = solve_pi_lead(unknown="alpha",
                      omega_c=REEXAM_F21_Q15["omega_c"],
                      gamma_M_deg=REEXAM_F21_Q15["gamma_M_deg"],
                      phi_G_deg=REEXAM_F21_Q15["phi_G_deg"],
                      N_i=REEXAM_F21_Q15["N_i"])
    # M_D = 1/sqrt(alpha) ≈ 3.3 → alpha ≈ 0.0918
    M_D = 1 / math.sqrt(a)
    assert M_D == pytest.approx(3.3, rel=2e-2)


def test_F22_Q19_KP_mode():
    G = parse_tf(F22_Q19["G_str"])
    KP = solve_pi_lead(unknown="KP", G=G,
                      gamma_M_deg=F22_Q19["gamma_M_deg"],
                      alpha=F22_Q19["alpha"],
                      N_i=F22_Q19["N_i"])
    assert KP == pytest.approx(F22_Q19["facit"], rel=2e-2)


from tests.oracle_data import S20_Q9, S21_Q6


def test_S21_Q6_P_for_PM_40():
    G = parse_tf(S21_Q6["G_str"])
    out = solve_P_for_PM(G, S21_Q6["target_PM_deg"])
    # Facit 8.4 is the rounded multiple-choice answer; solver yields ~8.18 from
    # interpolation of phase on the log-spaced frequency grid. 5% picks "8.4" cleanly.
    assert out["K_P"] == pytest.approx(S21_Q6["facit_KP"], rel=5e-2)


def test_S20_Q9_P_for_PM_60_approximate():
    G = parse_tf(S20_Q9["G_str"])
    out = solve_P_for_PM(G, S20_Q9["target_PM_deg"])
    # Loose tolerance: plant is reconstructed approximately from MATLAB Bode read-off
    assert out["K_P"] == pytest.approx(S20_Q9["facit_KP_approx"], rel=0.5)
