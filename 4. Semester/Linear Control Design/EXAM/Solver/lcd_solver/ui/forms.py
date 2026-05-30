"""Declarative FormSpec registry — every solver's UI lives here."""
from __future__ import annotations
from lcd_solver.ui.form_builder import FieldSpec, FormSpec
from lcd_solver.types import ResultKind


ALL_FORMS: list[FormSpec] = [
    # P1
    FormSpec(
        title="P1 — ODE → TF",
        pattern="P1", variant="ODE → TF",
        fields=[
            FieldSpec(
                "y_coeffs", "y coeffs (highest-deg first, comma-sep)", "str",
                placeholder="e.g. 5, 1, 0.5",
                tooltip="Coefficients of y and its derivatives. E.g. '5, 1, 0.5' for 5y'' + y' + 0.5y."
            ),
            FieldSpec(
                "u_coeffs", "u coeffs (highest-deg first, comma-sep)", "str",
                placeholder="e.g. 3",
                tooltip="Coefficients of u and its derivatives. E.g. '3' for 3u."
            ),
        ],
        solver_module="lcd_solver.solvers.p1_models",
        solver_function="solve_ode_to_tf",
        result_kind=ResultKind.TF,
        explanation=(
            "Converts an ordinary differential equation (ODE) to a Transfer Function G(s) = U(s)/Y(s).\n"
            "Provide coefficients starting from the highest derivative first."
        ),
    ),
    FormSpec(
        title="P1 — State-space → TF",
        pattern="P1", variant="State-space → TF",
        fields=[
            FieldSpec(
                "A", "A (Python literal, e.g. [[-1,0],[0,-1]])", "str",
                placeholder="e.g. [[-1, 0], [0, -1]]",
                tooltip="State matrix A as a Python list of lists."
            ),
            FieldSpec(
                "B", "B", "str",
                placeholder="e.g. [[1], [9]]",
                tooltip="Input matrix B as a column vector list."
            ),
            FieldSpec(
                "C", "C", "str",
                placeholder="e.g. [[1, 1]]",
                tooltip="Output matrix C as a row vector list."
            ),
            FieldSpec(
                "D", "D", "str",
                placeholder="e.g. [[0]]",
                tooltip="Direct transmission matrix D as a list."
            ),
        ],
        solver_module="lcd_solver.solvers.p1_models",
        solver_function="solve_state_space_to_tf",
        result_kind=ResultKind.TF,
        explanation=(
            "Computes the Transfer Function G(s) = C(sI-A)^-1 B + D from state-space matrices.\n"
            "Input matrices using standard Python nested list syntax."
        ),
    ),
    FormSpec(
        title="P1 — Block reduction",
        pattern="P1", variant="Block reduction (DSL)",
        fields=[
            FieldSpec(
                "dsl_expr", "DSL: series / parallel / feedback over named blocks", "str",
                default="feedback(series(A, B), C)",
                placeholder="e.g. feedback(series(A, B), C)",
                tooltip="Reduce blocks symbolically. Operators: series(X, Y), parallel(X, Y), feedback(X, Y)."
            ),
        ],
        solver_module="lcd_solver.solvers.p1_block_reduce",
        solver_function="reduce_block_diagram",
        result_kind=ResultKind.TF,
        explanation=(
            "Reduces symbolic block diagrams into a single canonical Transfer Function.\n"
            "Use nested combinations of series(X, Y), parallel(X, Y), and feedback(plant, feedback_path)."
        ),
    ),
    # P2
    FormSpec(
        title="P2 — Bode read-off",
        pattern="P2", variant="Compose G(s) from read-off",
        fields=[
            FieldSpec(
                "dc_gain_dB", "DC gain (dB)", "float", default=0.0,
                placeholder="e.g. 6.02",
                tooltip="DC gain in decibels. Default is 0.0 dB."
            ),
            FieldSpec(
                "corners", "Corners: list of (ω, Δslope dB/dec)", "str",
                default="[(1,-20),(10,+20)]",
                placeholder="e.g. [(1,-20),(10,+20)]",
                tooltip="Poles and zeros frequencies. Negative slope for poles (-20), positive slope for zeros (+20)."
            ),
            FieldSpec(
                "phase_events", "Phase events: list of (ω, Δφ°)", "str",
                default="[(1,-90),(10,+90)]",
                placeholder="e.g. [(1,-90),(10,+90)]",
                tooltip="Phase events to identify LHP vs RHP poles/zeros. E.g. RHP zero causes phase to DROP (-90)."
            ),
        ],
        solver_module="lcd_solver.solvers.p2_bode",
        solver_function="compose_tf_from_bode",
        result_kind=ResultKind.TF,
        show_plot=True,
        explanation=(
            "Reconstructs the transfer function G(s) from Bode magnitude and phase read-offs.\n"
            "Format corners as [(omega, delta_slope)] and phase events as [(omega, delta_phase)]."
        ),
    ),
    # P3
    FormSpec(
        title="P3 — Stable-K range",
        pattern="P3", variant="Stable-K range (handles RHP)",
        fields=[
            FieldSpec(
                "G", "G(s)", "tf",
                placeholder="e.g. 1 / (s+1)**3",
                tooltip="Open-loop plant transfer function G(s)."
            )
        ],
        solver_module="lcd_solver.solvers.p3_stability",
        solver_function="solve_stable_K_range",
        result_kind=ResultKind.PICK,
        explanation=(
            "Calculates the range of proportional gain K for closed-loop stability.\n"
            "Supports plant G(s) with open-loop RHP (unstable) poles automatically using Routh-Hurwitz."
        ),
    ),
    FormSpec(
        title="P3 — Margins",
        pattern="P3", variant="GM / PM / ω_pc / ω_gc",
        fields=[
            FieldSpec(
                "G", "G(s)", "tf",
                placeholder="e.g. 25 / (s**3 + s**2 + 10*s)",
                tooltip="Open-loop loop transfer function G(s)."
            )
        ],
        solver_module="lcd_solver.solvers.p3_stability",
        solver_function="solve_margins",
        result_kind=ResultKind.DICT,
        dict_match_keys=["GM", "GM_dB", "PM_deg", "omega_pc", "omega_gc"],
        explanation=(
            "Computes standard loop margins: Gain Margin (linear & dB), Phase Margin (degrees),\n"
            "and their crossover frequencies (omega_pc = phase crossover, omega_gc = gain crossover)."
        ),
    ),
    # P4
    FormSpec(
        title="P4 — 2nd-order specs",
        pattern="P4", variant="Mp ↔ ζ (bidirectional)",
        fields=[
            FieldSpec(
                "Mp", "Mp (fraction, blank for unknown)", "str",
                placeholder="e.g. 0.17",
                tooltip="Maximum overshoot Mp as a fraction between 0 and 1. (0.17 represents 17%)."
            ),
            FieldSpec(
                "zeta", "ζ (blank for unknown)", "str",
                placeholder="e.g. 0.5",
                tooltip="Damping ratio zeta."
            ),
            FieldSpec(
                "omega_n", "ω_n (rad/s, blank for unknown)", "str",
                placeholder="e.g. 2.0",
                tooltip="Natural frequency omega_n in rad/s."
            ),
            FieldSpec(
                "t_p", "t_p (s, blank for unknown)", "str",
                placeholder="e.g. 1.77",
                tooltip="Peak time t_p in seconds."
            ),
            FieldSpec(
                "t_s_2pct", "t_s 2% (s, blank for unknown)", "str",
                placeholder="e.g. 4.0",
                tooltip="2% Settling time t_s in seconds."
            ),
        ],
        solver_module="lcd_solver.solvers.p4_secondorder",
        solver_function="solve_2nd_order",
        result_kind=ResultKind.DICT,
        dict_match_keys=["zeta", "Mp", "Mp_pct", "omega_n", "omega_d",
                         "t_p", "t_s_2pct", "t_s_5pct", "t_r", "omega_BW"],
        explanation=(
            "Solves second-order system metrics. Fill any subset of parameters (typically ζ or Mp\n"
            "along with one frequency/time metric) and leave the rest blank to compute all remaining specs."
        ),
    ),
    FormSpec(
        title="P4 — Closed-loop + 1 spec → full table",
        pattern="P4", variant="Closed-loop TF + 1 known metric",
        fields=[
            FieldSpec(
                "closed_loop_str", "Closed-loop TF in s, K", "str",
                default="K / (s**2 + 2*s + K)",
                placeholder="e.g. K / (s**2 + 2*s + K)",
                tooltip="Closed-loop transfer function containing symbolic gain 'K' and Laplace variable 's'."
            ),
            FieldSpec(
                "given_kind", "Known metric", "dropdown", default="Mp",
                options=["Mp", "zeta", "omega_n", "omega_d", "t_p", "t_s_2pct", "K"],
                tooltip="Select which metric has a known numerical constraint."
            ),
            FieldSpec(
                "given_value", "Value of that metric", "float", default=0.17,
                placeholder="e.g. 0.17",
                tooltip="Enter the numerical value for the selected known metric."
            ),
        ],
        solver_module="lcd_solver.solvers.p4_secondorder",
        solver_function="solve_closed_loop_2nd_order",
        result_kind=ResultKind.DICT,
        dict_match_keys=["K", "zeta", "Mp", "Mp_pct", "omega_n", "omega_d",
                         "t_p", "t_s_2pct", "t_s_5pct", "t_r", "omega_BW"],
        explanation=(
            "Given a parametric closed-loop TF containing variable 'K', solves for the required K value\n"
            "and computes the complete second-order metrics table from exactly one known specification."
        ),
    ),
    FormSpec(
        title="P4 — K for transient spec",
        pattern="P4", variant="K range for Mp / ζ spec",
        fields=[
            FieldSpec(
                "G_str", "G(s, K)", "str", default="K/(s*(s+5))",
                placeholder="e.g. K/(s*(s+5))",
                tooltip="Parametric loop gain transfer function containing symbol K."
            ),
            FieldSpec(
                "spec", "Spec (e.g. 'Mp <= 0.12')", "str", default="Mp <= 0.12",
                placeholder="e.g. Mp <= 0.12 or zeta >= 0.5",
                tooltip="Spec expression using inequality, e.g. Mp <= 0.12 or zeta >= 0.5."
            ),
        ],
        solver_module="lcd_solver.solvers.p4_secondorder",
        solver_function="solve_K_for_spec",
        result_kind=ResultKind.NUMBER,
        explanation=(
            "Finds the range or boundary value of gain K that satisfies a transient specification.\n"
            "Supported specs: Mp (fraction, e.g. Mp <= 0.12) or zeta (e.g. zeta >= 0.5)."
        ),
    ),
    # P5
    FormSpec(
        title="P5 — K_P from ess",
        pattern="P5", variant="K_P from step ess on type-0",
        fields=[
            FieldSpec(
                "G0", "G(0)", "float",
                placeholder="e.g. 0.4",
                tooltip="DC gain value G(0) of the plant."
            ),
            FieldSpec(
                "G0_unit", "unit", "dropdown", default="dB", options=["dB", "linear"],
                tooltip="Decide if the G(0) value is provided in decibels or linear scale."
            ),
            FieldSpec(
                "ess_target", "target ess", "float",
                placeholder="e.g. 0.555",
                tooltip="Target steady-state error under unit-step input."
            ),
        ],
        solver_module="lcd_solver.solvers.p5_ess",
        solver_function="solve_KP_from_ess",
        result_kind=ResultKind.NUMBER,
        explanation=(
            "Solves for proportional controller gain K_P to satisfy a target steady-state error (ess)\n"
            "for a Type-0 plant under step input. DC gain G(0) can be entered in dB or linear scale."
        ),
    ),
    FormSpec(
        title="P5 — ess table",
        pattern="P5", variant="System type + Kp/Kv/Ka + ess",
        fields=[
            FieldSpec(
                "G", "G(s)", "tf",
                placeholder="e.g. 5*(s+4) / (s**2 * (s+1) * (s+20))",
                tooltip="Open-loop transfer function G(s)."
            )
        ],
        solver_module="lcd_solver.solvers.p5_ess",
        solver_function="solve_ess_table",
        result_kind=ResultKind.DICT,
        dict_match_keys=["type", "K_p", "K_v", "K_a",
                         "ess_step", "ess_ramp", "ess_parabola"],
        explanation=(
            "Computes system type, error coefficients (Kp = position, Kv = velocity, Ka = acceleration),\n"
            "and steady-state errors under unit step, ramp, and parabolic inputs for plant G(s)."
        ),
    ),
    # P6
    FormSpec(
        title="P6 — PI-Lead (3-way)",
        pattern="P6", variant="PI-Lead phase budget",
        fields=[
            FieldSpec(
                "unknown", "unknown", "dropdown", default="alpha",
                options=["alpha", "Ni", "KP"],
                tooltip="Choose which parameter is the unknown to solve for."
            ),
            FieldSpec(
                "omega_c", "ω_c (rad/s, blank if KP-mode)", "str",
                placeholder="e.g. 6.4",
                tooltip="Design crossover frequency omega_c in rad/s."
            ),
            FieldSpec(
                "tau_d", "τ_d (s, Lead time constant, optional)", "str",
                placeholder="e.g. 0.355",
                tooltip="Lead compensator time constant, e.g. 0.355 from (0.355s + 1)."
            ),
            FieldSpec(
                "gamma_M_deg", "γ_M (°)", "float", default=75,
                placeholder="e.g. 75",
                tooltip="Target Phase Margin in degrees."
            ),
            FieldSpec(
                "phi_G_deg", "φ_G (°, blank if KP-mode)", "str",
                placeholder="e.g. -112.77",
                tooltip="Plant phase angle at crossover frequency in degrees."
            ),
            FieldSpec(
                "N_i", "N_i", "float", default=5,
                placeholder="e.g. 5",
                tooltip="PI frequency ratio N_i. Default is 5."
            ),
            FieldSpec(
                "alpha", "α (blank if alpha-mode)", "str",
                placeholder="e.g. 0.0918",
                tooltip="Lead controller attenuation factor alpha."
            ),
            FieldSpec(
                "G", "G(s) — only used in KP-mode", "tf",
                placeholder="e.g. 900 / ((0.25*s+1)*(s**2+50*s+3000))",
                tooltip="Plant transfer function G(s) required only when solving for KP."
            ),
        ],
        solver_module="lcd_solver.solvers.p6_control",
        solver_function="solve_pi_lead",
        result_kind=ResultKind.DICT,
        dict_match_keys=["alpha", "M_D", "M_D_dB", "N_i", "K_P"],
        explanation=(
            "Solves the Phase-Budget design equation: -180 + gamma_M = phi_G + phi_Lead + phi_PI.\n"
            "Hides irrelevant inputs dynamically based on which parameter is the unknown."
        ),
    ),
    FormSpec(
        title="P6 — P-for-PM",
        pattern="P6", variant="K_P for target PM",
        fields=[
            FieldSpec(
                "G", "G(s)", "tf",
                placeholder="e.g. 1 / (s*(s+2.1))",
                tooltip="Open-loop plant transfer function G(s)."
            ),
            FieldSpec(
                "target_PM_deg", "target PM (°)", "float", default=45,
                placeholder="e.g. 45",
                tooltip="Target Phase Margin in degrees."
            ),
        ],
        solver_module="lcd_solver.solvers.p6_control",
        solver_function="solve_P_for_PM",
        result_kind=ResultKind.DICT,
        dict_match_keys=["K_P", "omega_c"],
        explanation=(
            "Designs a proportional controller (finds K_P) to achieve a target Phase Margin (PM).\n"
            "Also reports the resulting gain crossover frequency omega_c."
        ),
    ),
    # P7
    FormSpec(
        title="P7 — Feedforward formula",
        pattern="P7", variant="Pick proper-fast F_d",
        fields=[
            FieldSpec(
                "n_lags", "n (number of first-order lags)", "int", default=3,
                placeholder="e.g. 3",
                tooltip="Number of plant lags."
            ),
            FieldSpec(
                "D_order", "Disturbance dynamics order", "int", default=2,
                placeholder="e.g. 2",
                tooltip="Order of the disturbance transfer function numerator."
            ),
        ],
        solver_module="lcd_solver.solvers.p7_theory",
        solver_function="pick_feedforward_form",
        result_kind=ResultKind.PICK,
        explanation=(
            "Determines the structure of a realizable feedforward controller F_d(s) for a system\n"
            "with n first-order lags and disturbance of order D_order. Appends low-pass filter to make it proper."
        ),
    ),
    FormSpec(
        title="P7 — Nested ess",
        pattern="P7", variant="K from nested-loop ess",
        fields=[
            FieldSpec(
                "architecture", "architecture", "dropdown", default="two_KP_same",
                options=["two_KP_same", "nested_K1_K2"],
                tooltip="Select nested-loop architecture."
            ),
            FieldSpec(
                "G0", "G(0) (two_KP_same only)", "str",
                placeholder="e.g. 0.75",
                tooltip="Inner plant DC gain G(0)."
            ),
            FieldSpec(
                "ess_target", "ess target (two_KP_same only)", "str",
                placeholder="e.g. 0.25",
                tooltip="Target steady-state error."
            ),
            FieldSpec(
                "eps1", "eps1 (nested_K1_K2 only)", "str",
                placeholder="e.g. 0.4",
                tooltip="Inner-loop error coefficient eps1."
            ),
            FieldSpec(
                "eps2", "eps2 (nested_K1_K2 only)", "str",
                placeholder="e.g. 0.05",
                tooltip="Outer-loop error coefficient eps2."
            ),
            FieldSpec(
                "G2_0", "G2(0) (nested_K1_K2 only)", "str",
                placeholder="e.g. 0.4",
                tooltip="DC gain G2(0) of inner plant."
            ),
        ],
        solver_module="lcd_solver.solvers.p7_theory",
        solver_function="solve_nested_ess",
        result_kind=ResultKind.NUMBER,
        explanation=(
            "Calculates gains for nested control loops to satisfy steady-state error (ess) targets.\n"
            "Hides irrelevant inputs dynamically based on the loop architecture."
        ),
    ),
]
