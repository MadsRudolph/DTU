"""Historical exam examples library for the LCD solver forms.

Provides pre-canned inputs and multiple-choice options for past papers
(F22, S21, S20, ReExam F21, and Theory).
"""
from __future__ import annotations
from typing import Any


# Maps solver_function name -> list of example dicts
EXAMPLES_REGISTRY: dict[str, list[dict[str, Any]]] = {
    "solve_ode_to_tf": [
        {
            "name": "F22 Q8 (highest-deg first)",
            "inputs": {
                "y_coeffs": "5, 1, 0.5",
                "u_coeffs": "3"
            },
            "options": "0.87\n1.0\n1.73\n2.0"
        },
        {
            "name": "S21 Q8 (highest-deg first)",
            "inputs": {
                "y_coeffs": "1, 2, 1",
                "u_coeffs": "1"
            },
            "options": "-1.0\n1.0\n2.0\n-2.0"
        }
    ],
    "solve_state_space_to_tf": [
        {
            "name": "ReExam F21 Q6",
            "inputs": {
                "A": "[[-1.0, 0.0], [0.0, -1.0]]",
                "B": "[[1.0], [9.0]]",
                "C": "[[1.0, 1.0]]",
                "D": "[[0.0]]"
            },
            "options": "1.0\n9.0\n10.0\n-1.0"
        }
    ],
    "reduce_block_diagram": [
        {
            "name": "S20 Q3",
            "inputs": {
                "dsl_expr": "parallel(A, 1 / (1 + B/s))"
            },
            "options": "((1+A)*s + A*B) / (s + B)\n(A*s + B) / (s + B)\n1 / (s + B)"
        },
        {
            "name": "S21 Q1 (Nested series/parallel)",
            "inputs": {
                "dsl_expr": "(series(A, B, C, D) + series(E, C, D)) / (1 + B*C*F)"
            },
            "options": "(A*B*C*D + E*C*D) / (1 + B*C*F)\n(A*B*C*D + E) / (1 + B*C*F)"
        }
    ],
    "compose_tf_from_bode": [
        {
            "name": "F22 Q5",
            "inputs": {
                "dc_gain_dB": "6.0206",
                "corners": "[(1,-20),(1,-20),(2,20)]",
                "phase_events": "[(1,-90),(1,-90),(2,-90)]"
            },
            "options": "1.73\n2.0\n-1.0\n(s-2)/(s+1)**2"
        },
        {
            "name": "ReExam F21 Q5",
            "inputs": {
                "dc_gain_dB": "60.0",
                "corners": "[(1,-20),(10,20)]",
                "phase_events": "[(1,90),(10,90)]"
            },
            "options": "100*(s+10)/(s-1)\n100*(s-10)/(s+1)"
        }
    ],
    "solve_stable_K_range": [
        {
            "name": "S21 Q4 (Third-order)",
            "inputs": {
                "G": "1 / (s+1)**3"
            },
            "options": "0 < K < 8\nK > 8\nK < 0"
        },
        {
            "name": "ReExam F21 Q14",
            "inputs": {
                "G": "25 / (s**3 + s**2 + 10*s)"
            },
            "options": "0 < K < 0.398\n0.398\nK > 0.398"
        }
    ],
    "solve_margins": [
        {
            "name": "ReExam F21 Q14 Margins",
            "inputs": {
                "G": "25 / (s**3 + s**2 + 10*s)"
            },
            "options": "0.398\n7.96 dB\n2.51 rad/s\n0.0 dB"
        }
    ],
    "solve_2nd_order": [
        {
            "name": "ReExam F21 Q10",
            "inputs": {
                "zeta": "0.7071"
            },
            "options": "4.32%\n16.3%\n20.0%\n5.0%"
        },
        {
            "name": "F22 Q10",
            "inputs": {
                "zeta": "0.7071"
            },
            "options": "4.32%\n16.3%\n20.0%\n5.0%"
        },
        {
            "name": "S20 Q5",
            "inputs": {
                "zeta": "0.2"
            },
            "options": "0.2\n0.5\n0.7\n0.9"
        }
    ],
    "solve_closed_loop_2nd_order": [
        {
            "name": "ReExam F22 Q2 (Canonical Overshoot)",
            "inputs": {
                "closed_loop_str": "K / (s**2 + 2*s + K)",
                "given_kind": "Mp",
                "given_value": "0.17"
            },
            "options": "0.87\n1.0\n1.73\n2.0"
        }
    ],
    "solve_K_for_spec": [
        {
            "name": "S21 Q9",
            "inputs": {
                "G_str": "K / (s*(s+5))",
                "spec": "Mp <= 0.12"
            },
            "options": "19.97\n5.0\n12.0\n20.0"
        }
    ],
    "solve_KP_from_ess": [
        {
            "name": "F22 Q16",
            "inputs": {
                "G0": "-7.9588",
                "G0_unit": "dB",
                "ess_target": "0.5555"
            },
            "options": "1.0\n2.0\n3.0\n4.0"
        }
    ],
    "solve_ess_table": [
        {
            "name": "ReExam F21 Q4 (Type-2 Plant)",
            "inputs": {
                "G": "5*(s+4) / (s**2 * (s+1) * (s+20))"
            },
            "options": "type=2\ness_parabola=1.0\ness_ramp=0.0\ness_step=0.0"
        }
    ],
    "solve_pi_lead": [
        {
            "name": "F22 Q17 (alpha mode)",
            "inputs": {
                "unknown": "alpha",
                "omega_c": "6.4",
                "gamma_M_deg": "75",
                "phi_G_deg": "-112.77",
                "N_i": "5"
            },
            "options": "0.5\n0.25\n0.1\n0.05"
        },
        {
            "name": "ReExam F21 Q15 (alpha mode)",
            "inputs": {
                "unknown": "alpha",
                "omega_c": "15.0",
                "gamma_M_deg": "50",
                "phi_G_deg": "-167.842",
                "N_i": "3"
            },
            "options": "0.0918\n0.5\n0.25\n0.1"
        },
        {
            "name": "ReExam F21 Q17 (Ni mode)",
            "inputs": {
                "unknown": "Ni",
                "omega_c": "25.04",
                "gamma_M_deg": "75",
                "phi_G_deg": "-151.064",
                "alpha": "0.01"
            },
            "options": "1.57\n2.0\n3.5\n5.0"
        },
        {
            "name": "F22 Q19 (KP mode)",
            "inputs": {
                "unknown": "KP",
                "gamma_M_deg": "75",
                "alpha": "0.01",
                "N_i": "3",
                "G": "900 / ((0.25*s+1)*(s**2+50*s+3000))"
            },
            "options": "3.415\n1.0\n5.0\n10.0"
        }
    ],
    "solve_P_for_PM": [
        {
            "name": "S21 Q6 (Proportional design)",
            "inputs": {
                "G": "1 / (s*(s+2.1))",
                "target_PM_deg": "40"
            },
            "options": "8.4\n8.18\n5.0\n2.1"
        },
        {
            "name": "S20 Q9",
            "inputs": {
                "G": "20833 / (s*(s+43.3))",
                "target_PM_deg": "60"
            },
            "options": "0.06\n0.1\n1.5\n2.0"
        }
    ],
    "pick_feedforward_form": [
        {
            "name": "Theory Q8",
            "inputs": {
                "n_lags": "3",
                "D_order": "2"
            },
            "options": "a\nb\nc\nd"
        }
    ],
    "solve_nested_ess": [
        {
            "name": "Theory Q9 (two KP same)",
            "inputs": {
                "architecture": "two_KP_same",
                "G0": "0.75",
                "ess_target": "0.25"
            },
            "options": "4.0\n1.0\n2.0\n8.0"
        },
        {
            "name": "Theory Q6 (nested K1 K2)",
            "inputs": {
                "architecture": "nested_K1_K2",
                "eps1": "0.4",
                "eps2": "0.05",
                "G2_0": "0.4"
            },
            "options": "79.17\n40.0\n20.0\n0.4"
        }
    ]
}


def get_examples_for_function(solver_function: str) -> list[dict[str, Any]]:
    return EXAMPLES_REGISTRY.get(solver_function, [])
