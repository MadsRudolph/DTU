"""FormSpec → QWidget builder.

Each solver gets a FormSpec declaring its inputs. build_form() turns that into
a QWidget with the input fields, an options textarea, a Solve button, and a
ResultPanel wired to the solver function.
"""
from __future__ import annotations
import importlib
from dataclasses import dataclass, field
from typing import Any, Callable, Literal

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QPlainTextEdit, QLabel,
)

from lcd_solver.match import match
from lcd_solver.types import Result, ResultKind
from lcd_solver.ui.widgets import TFInputWidget, ResultPanel


FieldKind = Literal["float", "int", "str", "tf", "dropdown"]


@dataclass
class FieldSpec:
    name: str
    label: str
    kind: FieldKind
    default: Any = None
    options: list[str] | None = None


@dataclass
class FormSpec:
    title: str
    pattern: str
    variant: str
    fields: list[FieldSpec]
    solver_module: str         # e.g. "lcd_solver.solvers.p6_control"
    solver_function: str       # e.g. "solve_pi_lead"
    result_kind: ResultKind = ResultKind.NUMBER
    dict_match_keys: list[str] = field(default_factory=list)
    show_plot: bool = False


class SolverFormWidget(QWidget):
    def __init__(self, spec: FormSpec) -> None:
        super().__init__()
        self.spec = spec
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<h3>{spec.pattern} — {spec.variant}</h3>"))

        form = QFormLayout()
        self._field_widgets: dict[str, QWidget] = {}
        for f in spec.fields:
            if f.kind == "tf":
                w = TFInputWidget(label="")
                form.addRow(f.label, w)
            elif f.kind == "dropdown":
                w = QComboBox()
                w.addItems(f.options or [])
                if f.default is not None:
                    w.setCurrentText(str(f.default))
                form.addRow(f.label, w)
            else:
                w = QLineEdit()
                if f.default is not None:
                    w.setText(str(f.default))
                form.addRow(f.label, w)
            self._field_widgets[f.name] = w
        layout.addLayout(form)

        if spec.dict_match_keys:
            self.match_key_combo = QComboBox()
            self.match_key_combo.addItems(spec.dict_match_keys)
            row = QFormLayout()
            row.addRow("Match against key:", self.match_key_combo)
            layout.addLayout(row)
        else:
            self.match_key_combo = None

        layout.addWidget(QLabel("Options (one per line):"))
        self.options_box = QPlainTextEdit()
        self.options_box.setFixedHeight(120)
        layout.addWidget(self.options_box)

        solve_btn = QPushButton("Solve")
        solve_btn.clicked.connect(self._on_solve)
        layout.addWidget(solve_btn)

        self.result_panel = ResultPanel()
        layout.addWidget(self.result_panel)

    def _gather_inputs(self) -> dict[str, Any]:
        import ast
        kwargs: dict[str, Any] = {}
        for f in self.spec.fields:
            w = self._field_widgets[f.name]
            if f.kind == "tf":
                txt = w.edit.text().strip() if hasattr(w, "edit") else w.text().strip()
                kwargs[f.name] = None if not txt else w.get_tf()
            elif f.kind == "dropdown":
                kwargs[f.name] = w.currentText()
            elif f.kind == "int":
                txt = w.text().strip()
                kwargs[f.name] = None if not txt else int(txt)
            elif f.kind == "float":
                txt = w.text().strip()
                kwargs[f.name] = None if not txt else float(txt)
            else:  # str — try Python-literal first for lists/tuples/etc.
                txt = w.text().strip() if hasattr(w, "text") else ""
                if not txt:
                    kwargs[f.name] = None
                else:
                    try:
                        kwargs[f.name] = ast.literal_eval(txt)
                    except (ValueError, SyntaxError):
                        kwargs[f.name] = txt
        # Strip None entries: solver kwargs use missing-means-default
        return {k: v for k, v in kwargs.items() if v is not None}

    def _call_solver(self, kwargs: dict[str, Any]):
        mod = importlib.import_module(self.spec.solver_module)
        fn: Callable = getattr(mod, self.spec.solver_function)
        return fn(**kwargs)

    def _on_solve(self) -> None:
        try:
            kwargs = self._gather_inputs()
            raw = self._call_solver(kwargs)
        except Exception as e:
            self.result_panel.display(f"Error: {e}", [], [])
            return

        # Solvers that show a plot return (value, matplotlib_figure)
        plot_fig = None
        if self.spec.show_plot and isinstance(raw, tuple) and len(raw) == 2:
            raw, plot_fig = raw

        result = Result(value=raw, kind=self.spec.result_kind, plot_data=plot_fig)
        match_key = self.match_key_combo.currentText() if self.match_key_combo else None
        options = match(result, self.options_box.toPlainText(), match_key=match_key)

        if self.spec.result_kind == ResultKind.NUMBER:
            value_text = f"{float(raw):.6g}"
        elif self.spec.result_kind == ResultKind.DICT:
            value_text = ", ".join(f"{k} = {v:.6g}" for k, v in raw.items())
        elif self.spec.result_kind == ResultKind.PICK:
            # PICK can be tuple (stable-K range) or dict (feedforward) — render generically
            if isinstance(raw, tuple):
                value_text = f"({', '.join(f'{x:.6g}' if isinstance(x, float) else str(x) for x in raw)})"
            elif isinstance(raw, dict):
                value_text = raw.get("formula_latex") or str(raw)
            else:
                value_text = str(raw)
        else:  # TF
            value_text = str(raw)
        self.result_panel.display(value_text, options, [])


def build_form(spec: FormSpec) -> SolverFormWidget:
    return SolverFormWidget(spec)
