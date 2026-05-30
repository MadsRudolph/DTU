"""P7 — Theory exercises that survive as solvers: structural feedforward
picker (Q8) and nested-loop ess (Q6, Q9)."""
from __future__ import annotations
import math


def pick_feedforward_form(n_lags: int, D_order: int = 2) -> dict:
    """Per Theory Q8: for n first-order lags G_1 = prod 1/(tau_k s + 1) with disturbance
    dynamics D(s) of order D_order, the realisable feedforward is

        F_d(s) = D(s) * prod(tau_k s + 1) / (tau_f s + 1)^(n - D_order),
        tau_f <= min(tau_k) / 5

    This corresponds to option (d) in the canonical multiple-choice phrasing.
    """
    filter_order = max(0, n_lags - D_order)
    formula_latex = (
        r"F_d(s) = \frac{D(s) \prod_{k=1}^n (\tau_k s + 1)}"
        rf"{{(\tau_f s + 1)^{{{filter_order}}}}}"
    )
    return {
        "option_label": "d",
        "filter_order": filter_order,
        "formula_latex": formula_latex,
        "tau_f_bound": r"tau_f <= min(tau_k)/5",
        "explanation": (
            "Improper by (n - D_order); appended low-pass filter makes the "
            "controller realisable. Filter tau_f must be fast (<= min(tau_k)/5) "
            "so it does not attenuate genuine plant dynamics."
        ),
    }
