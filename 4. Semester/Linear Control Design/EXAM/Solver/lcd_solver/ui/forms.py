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
            FieldSpec("y_coeffs", "y coeffs (highest-deg first, comma-sep)", "str"),
            FieldSpec("u_coeffs", "u coeffs (highest-deg first, comma-sep)", "str"),
        ],
        solver_module="lcd_solver.solvers.p1_models",
        solver_function="solve_ode_to_tf",
        result_kind=ResultKind.TF,
    ),
    FormSpec(
        title="P1 — State-space → TF",
        pattern="P1", variant="State-space → TF",
        fields=[
            FieldSpec("A", "A (Python literal, e.g. [[-1,0],[0,-1]])", "str"),
            FieldSpec("B", "B", "str"),
            FieldSpec("C", "C", "str"),
            FieldSpec("D", "D", "str"),
        ],
        solver_module="lcd_solver.solvers.p1_models",
        solver_function="solve_state_space_to_tf",
        result_kind=ResultKind.TF,
    ),
    FormSpec(
        title="P1 — Block reduction",
        pattern="P1", variant="Block reduction (DSL)",
        fields=[
            FieldSpec("dsl_expr", "DSL: series / parallel / feedback over named blocks", "str",
                      default="feedback(series(A, B), C)"),
        ],
        solver_module="lcd_solver.solvers.p1_block_reduce",
        solver_function="reduce_block_diagram",
        result_kind=ResultKind.TF,
    ),
    # P2
    FormSpec(
        title="P2 — Bode read-off",
        pattern="P2", variant="Compose G(s) from read-off",
        fields=[
            FieldSpec("dc_gain_dB", "DC gain (dB)", "float", default=0.0),
            FieldSpec("corners", "Corners: list of (ω, Δslope dB/dec)", "str",
                      default="[(1,-20),(10,+20)]"),
            FieldSpec("phase_events", "Phase events: list of (ω, Δφ°)", "str",
                      default="[(1,-90),(10,+90)]"),
        ],
        solver_module="lcd_solver.solvers.p2_bode",
        solver_function="compose_tf_from_bode",
        result_kind=ResultKind.TF,
        show_plot=True,
    ),
    # P3
    FormSpec(
        title="P3 — Stable-K range",
        pattern="P3", variant="Stable-K range (handles RHP)",
        fields=[FieldSpec("G", "G(s)", "tf")],
        solver_module="lcd_solver.solvers.p3_stability",
        solver_function="solve_stable_K_range",
        result_kind=ResultKind.PICK,   # tuple — display canonical, user eyeball-matches
    ),
    FormSpec(
        title="P3 — Margins",
        pattern="P3", variant="GM / PM / ω_pc / ω_gc",
        fields=[FieldSpec("G", "G(s)", "tf")],
        solver_module="lcd_solver.solvers.p3_stability",
        solver_function="solve_margins",
        result_kind=ResultKind.DICT,
        dict_match_keys=["GM", "GM_dB", "PM_deg", "omega_pc", "omega_gc"],
    ),
    # P4
    FormSpec(
        title="P4 — 2nd-order specs",
        pattern="P4", variant="Mp ↔ ζ (bidirectional)",
        fields=[
            FieldSpec("Mp", "Mp (fraction, blank for unknown)", "str"),
            FieldSpec("zeta", "ζ (blank for unknown)", "str"),
            FieldSpec("omega_n", "ω_n (rad/s, blank for unknown)", "str"),
            FieldSpec("t_p", "t_p (s, blank for unknown)", "str"),
            FieldSpec("t_s_2pct", "t_s 2% (s, blank for unknown)", "str"),
        ],
        solver_module="lcd_solver.solvers.p4_secondorder",
        solver_function="solve_2nd_order",
        result_kind=ResultKind.DICT,
        dict_match_keys=["zeta", "Mp", "Mp_pct", "omega_n", "omega_d",
                         "t_p", "t_s_2pct", "t_s_5pct", "t_r", "omega_BW"],
    ),
    FormSpec(
        title="P4 — Closed-loop + 1 spec → full table",
        pattern="P4", variant="Closed-loop TF + 1 known metric",
        fields=[
            FieldSpec("closed_loop_str", "Closed-loop TF in s, K", "str",
                      default="K / (s**2 + 2*s + K)"),
            FieldSpec("given_kind", "Known metric", "dropdown", default="Mp",
                      options=["Mp", "zeta", "omega_n", "omega_d", "t_p", "t_s_2pct", "K"]),
            FieldSpec("given_value", "Value of that metric", "float", default=0.17),
        ],
        solver_module="lcd_solver.solvers.p4_secondorder",
        solver_function="solve_closed_loop_2nd_order",
        result_kind=ResultKind.DICT,
        dict_match_keys=["K", "zeta", "Mp", "Mp_pct", "omega_n", "omega_d",
                         "t_p", "t_s_2pct", "t_s_5pct", "t_r", "omega_BW"],
    ),
    FormSpec(
        title="P4 — K for transient spec",
        pattern="P4", variant="K range for Mp / ζ spec",
        fields=[
            FieldSpec("G_str", "G(s, K)", "str", default="K/(s*(s+5))"),
            FieldSpec("spec", "Spec (e.g. 'Mp <= 0.12')", "str", default="Mp <= 0.12"),
        ],
        solver_module="lcd_solver.solvers.p4_secondorder",
        solver_function="solve_K_for_spec",
        result_kind=ResultKind.NUMBER,
    ),
    # P5
    FormSpec(
        title="P5 — K_P from ess",
        pattern="P5", variant="K_P from step ess on type-0",
        fields=[
            FieldSpec("G0", "G(0)", "float"),
            FieldSpec("G0_unit", "unit", "dropdown", default="dB", options=["dB", "linear"]),
            FieldSpec("ess_target", "target ess", "float"),
        ],
        solver_module="lcd_solver.solvers.p5_ess",
        solver_function="solve_KP_from_ess",
        result_kind=ResultKind.NUMBER,
    ),
    FormSpec(
        title="P5 — ess table",
        pattern="P5", variant="System type + Kp/Kv/Ka + ess",
        fields=[FieldSpec("G", "G(s)", "tf")],
        solver_module="lcd_solver.solvers.p5_ess",
        solver_function="solve_ess_table",
        result_kind=ResultKind.DICT,
        dict_match_keys=["type", "K_p", "K_v", "K_a",
                         "ess_step", "ess_ramp", "ess_parabola"],
    ),
    # P6
    FormSpec(
        title="P6 — PI-Lead (3-way)",
        pattern="P6", variant="PI-Lead phase budget",
        fields=[
            FieldSpec("unknown", "unknown", "dropdown", default="alpha",
                      options=["alpha", "Ni", "KP"]),
            FieldSpec("omega_c", "ω_c (rad/s, blank if KP-mode)", "str"),
            FieldSpec("gamma_M_deg", "γ_M (°)", "float", default=75),
            FieldSpec("phi_G_deg", "φ_G (°, blank if KP-mode)", "str"),
            FieldSpec("N_i", "N_i", "float", default=5),
            FieldSpec("alpha", "α (blank if alpha-mode)", "str"),
            FieldSpec("G", "G(s) — only used in KP-mode", "tf"),
        ],
        solver_module="lcd_solver.solvers.p6_control",
        solver_function="solve_pi_lead",
        result_kind=ResultKind.NUMBER,
    ),
    FormSpec(
        title="P6 — P-for-PM",
        pattern="P6", variant="K_P for target PM",
        fields=[
            FieldSpec("G", "G(s)", "tf"),
            FieldSpec("target_PM_deg", "target PM (°)", "float", default=45),
        ],
        solver_module="lcd_solver.solvers.p6_control",
        solver_function="solve_P_for_PM",
        result_kind=ResultKind.DICT,
        dict_match_keys=["K_P", "omega_c"],
    ),
    # P7
    FormSpec(
        title="P7 — Feedforward formula",
        pattern="P7", variant="Pick proper-fast F_d",
        fields=[
            FieldSpec("n_lags", "n (number of first-order lags)", "int", default=3),
            FieldSpec("D_order", "Disturbance dynamics order", "int", default=2),
        ],
        solver_module="lcd_solver.solvers.p7_theory",
        solver_function="pick_feedforward_form",
        result_kind=ResultKind.PICK,
    ),
    FormSpec(
        title="P7 — Nested ess",
        pattern="P7", variant="K from nested-loop ess",
        fields=[
            FieldSpec("architecture", "architecture", "dropdown", default="two_KP_same",
                      options=["two_KP_same", "nested_K1_K2"]),
            FieldSpec("G0", "G(0) (two_KP_same only)", "str"),
            FieldSpec("ess_target", "ess target (two_KP_same only)", "str"),
            FieldSpec("eps1", "eps1 (nested_K1_K2 only)", "str"),
            FieldSpec("eps2", "eps2 (nested_K1_K2 only)", "str"),
            FieldSpec("G2_0", "G2(0) (nested_K1_K2 only)", "str"),
        ],
        solver_module="lcd_solver.solvers.p7_theory",
        solver_function="solve_nested_ess",
        result_kind=ResultKind.NUMBER,
    ),
]
