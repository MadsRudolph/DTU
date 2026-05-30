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
