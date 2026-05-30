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


def solve_nested_ess(*, architecture: str, **kwargs) -> float:
    """Two architectures:

    'two_KP_same' (Theory Q9):  e(0) = (1 + K_P G0) / (1 + K_P G0 + K_P^2 G0)
                                Solve for K_P given (G0, ess_target). Positive real root.

    'nested_K1_K2' (Theory Q6):  K_2 = (1 - eps2) / (eps2 · G2_0 · (1 - eps1))
    """
    if architecture == "two_KP_same":
        G0 = kwargs["G0"]
        ess = kwargs["ess_target"]
        # (1 + K_P G0) = ess (1 + K_P G0 + K_P^2 G0)
        # ess G0 K^2 + G0 (ess - 1) K + (ess - 1) = 0
        a = ess * G0
        b = G0 * (ess - 1)
        c = ess - 1
        disc = b * b - 4 * a * c
        if disc < 0:
            raise ValueError("No real K_P satisfies this nested-loop ess spec")
        roots = [(-b + math.sqrt(disc)) / (2 * a), (-b - math.sqrt(disc)) / (2 * a)]
        positives = [r for r in roots if r > 0]
        if not positives:
            raise ValueError("No positive K_P root")
        return float(max(positives))

    if architecture == "nested_K1_K2":
        eps1 = kwargs["eps1"]; eps2 = kwargs["eps2"]; G2_0 = kwargs["G2_0"]
        return float((1 - eps2) / (eps2 * G2_0 * (1 - eps1)))

    raise ValueError(f"unknown architecture {architecture!r}")
