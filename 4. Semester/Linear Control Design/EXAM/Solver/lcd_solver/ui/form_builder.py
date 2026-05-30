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
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QPlainTextEdit, QLabel,
)

from lcd_solver.match import match
from lcd_solver.types import Result, ResultKind
from lcd_solver.ui.widgets import TFInputWidget, ResultPanel
from lcd_solver.ui.examples import get_examples_for_function


FieldKind = Literal["float", "int", "str", "tf", "dropdown"]


@dataclass
class FieldSpec:
    name: str
    label: str
    kind: FieldKind
    default: Any = None
    options: list[str] | None = None
    placeholder: str = ""
    tooltip: str = ""


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
    explanation: str = ""


class SolverFormWidget(QWidget):
    def __init__(self, spec: FormSpec) -> None:
        super().__init__()
        self.spec = spec
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<h2>{spec.pattern} — {spec.variant}</h2>"))

        # Explanation Banner
        if spec.explanation:
            explanation_label = QLabel(spec.explanation)
            explanation_label.setWordWrap(True)
            explanation_label.setStyleSheet(
                "background-color: #f7f9fa; border-left: 4px solid #007acc; "
                "padding: 10px; color: #4b5563; font-size: 10pt; border-radius: 4px;"
            )
            layout.addWidget(explanation_label)

        # Examples Loader
        examples = get_examples_for_function(spec.solver_function)
        if examples:
            example_layout = QHBoxLayout()
            example_layout.addWidget(QLabel("<b>Load Past Exam Example:</b>"))
            self.example_combo = QComboBox()
            self.example_combo.addItem("-- select an example to populate fields --")
            for ex in examples:
                self.example_combo.addItem(ex["name"])
            self.example_combo.currentIndexChanged.connect(self._on_example_changed)
            example_layout.addWidget(self.example_combo)
            layout.addLayout(example_layout)
        else:
            self.example_combo = None

        form = QFormLayout()
        self._field_widgets: dict[str, QWidget] = {}
        self._field_rows: dict[str, tuple[QLabel, QWidget]] = {}

        for f in spec.fields:
            lbl = QLabel(f.label)
            if f.tooltip:
                lbl.setToolTip(f.tooltip)

            if f.kind == "tf":
                w = TFInputWidget(label="")
                if f.placeholder:
                    w.edit.setPlaceholderText(f.placeholder)
                if f.tooltip:
                    w.edit.setToolTip(f.tooltip)
            elif f.kind == "dropdown":
                w = QComboBox()
                w.addItems(f.options or [])
                if f.default is not None:
                    w.setCurrentText(str(f.default))
                if f.tooltip:
                    w.setToolTip(f.tooltip)
                w.currentTextChanged.connect(lambda _: self._update_field_visibility())
            else:
                w = QLineEdit()
                if f.default is not None:
                    w.setText(str(f.default))
                if f.placeholder:
                    w.setPlaceholderText(f.placeholder)
                if f.tooltip:
                    w.setToolTip(f.tooltip)

            form.addRow(lbl, w)
            self._field_widgets[f.name] = w
            self._field_rows[f.name] = (lbl, w)

        layout.addLayout(form)

        if spec.dict_match_keys:
            self.match_key_combo = QComboBox()
            self.match_key_combo.addItems(["auto"] + spec.dict_match_keys)
            row = QFormLayout()
            row.addRow("Match against key:", self.match_key_combo)
            layout.addLayout(row)
        else:
            self.match_key_combo = None

        layout.addWidget(QLabel("Options (one per line):"))
        self.options_box = QPlainTextEdit()
        self.options_box.setFixedHeight(120)
        self.options_box.setPlaceholderText("Paste option values from exam here, e.g.\n1.73\n2.0\n0.87")
        layout.addWidget(self.options_box)

        # Buttons layout
        btn_layout = QHBoxLayout()
        solve_btn = QPushButton("Solve")
        solve_btn.setStyleSheet("font-weight: bold; background-color: #007acc; color: white; padding: 6px;")
        solve_btn.clicked.connect(self._on_solve)
        btn_layout.addWidget(solve_btn)

        reset_btn = QPushButton("Reset / Clear All")
        reset_btn.setStyleSheet("padding: 6px;")
        reset_btn.clicked.connect(self._on_reset)
        btn_layout.addWidget(reset_btn)

        layout.addLayout(btn_layout)

        self.result_panel = ResultPanel(on_key_selected_callback=self._on_interactive_key_select)
        layout.addWidget(self.result_panel)

        # Run initial field visibility update
        self._update_field_visibility()

    def _on_interactive_key_select(self, key_name: str) -> None:
        if self.match_key_combo:
            index = self.match_key_combo.findText(key_name)
            if index >= 0:
                self.match_key_combo.setCurrentIndex(index)
                self._on_solve()

    def _update_field_visibility(self) -> None:
        if self.spec.solver_function == "solve_pi_lead":
            unknown = self._field_widgets["unknown"].currentText()
            for name, (lbl, w) in self._field_rows.items():
                if name == "unknown":
                    continue
                if unknown == "alpha":
                    visible = (name in ["omega_c", "gamma_M_deg", "phi_G_deg", "N_i"])
                elif unknown == "Ni":
                    visible = (name in ["omega_c", "gamma_M_deg", "phi_G_deg", "alpha"])
                elif unknown == "KP":
                    visible = (name in ["G", "gamma_M_deg", "alpha", "N_i"])
                else:
                    visible = True
                lbl.setVisible(visible)
                w.setVisible(visible)

        elif self.spec.solver_function == "solve_nested_ess":
            arch = self._field_widgets["architecture"].currentText()
            for name, (lbl, w) in self._field_rows.items():
                if name == "architecture":
                    continue
                if arch == "two_KP_same":
                    visible = (name in ["G0", "ess_target"])
                elif arch == "nested_K1_K2":
                    visible = (name in ["eps1", "eps2", "G2_0"])
                else:
                    visible = True
                lbl.setVisible(visible)
                w.setVisible(visible)

    def _on_example_changed(self, index: int) -> None:
        if index <= 0 or not self.example_combo:
            return
        examples = get_examples_for_function(self.spec.solver_function)
        ex = examples[index - 1]

        # Populate fields
        for name, value in ex["inputs"].items():
            if name in self._field_widgets:
                w = self._field_widgets[name]
                fspec = next((f for f in self.spec.fields if f.name == name), None)
                if fspec and fspec.kind == "tf":
                    w.edit.setText(str(value))
                elif isinstance(w, QComboBox):
                    w.setCurrentText(str(value))
                else:
                    w.setText(str(value))

        # Populate options
        if "options" in ex:
            self.options_box.setPlainText(ex["options"])

        # Update visibility
        self._update_field_visibility()

        # Clear result panel
        self.result_panel.display("—", [], [], raw_value=None, match_key=None)

    def _on_reset(self) -> None:
        if hasattr(self, "example_combo") and self.example_combo:
            self.example_combo.blockSignals(True)
            self.example_combo.setCurrentIndex(0)
            self.example_combo.blockSignals(False)

        for f in self.spec.fields:
            w = self._field_widgets[f.name]
            if f.kind == "tf":
                w.edit.clear()
            elif f.kind == "dropdown":
                if f.default is not None:
                    w.setCurrentText(str(f.default))
                else:
                    w.setCurrentIndex(0)
            else:
                if f.default is not None:
                    w.setText(str(f.default))
                else:
                    w.clear()

        if self.match_key_combo:
            self.match_key_combo.setCurrentIndex(0)

        self.options_box.clear()
        self.result_panel.display("—", [], [], raw_value=None, match_key=None)
        self._update_field_visibility()

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

        # Build the value-text first so it's visible even if matching fails
        if self.spec.result_kind == ResultKind.NUMBER:
            value_text = f"{float(raw):.6g}"
            if self.spec.solver_function == "solve_pi_lead":
                import math
                unknown = self._field_widgets["unknown"].currentText()
                if unknown == "alpha":
                    alpha_val = float(raw)
                    if alpha_val > 0:
                        md_val = 1.0 / math.sqrt(alpha_val)
                        md_db = 20.0 * math.log10(md_val)
                        value_text += f"  (Implied MD = {md_val:.3g} = {md_db:.2f} dB)"
        elif self.spec.result_kind == ResultKind.DICT:
            value_text = ", ".join(f"{k} = {v:.6g}" for k, v in raw.items())
        elif self.spec.result_kind == ResultKind.PICK:
            if isinstance(raw, tuple):
                value_text = f"({', '.join(f'{x:.6g}' if isinstance(x, float) else str(x) for x in raw)})"
            elif isinstance(raw, dict):
                value_text = raw.get("formula_latex") or str(raw)
            else:
                value_text = str(raw)
        else:  # TF
            value_text = str(raw)

        result = Result(value=raw, kind=self.spec.result_kind, plot_data=plot_fig)
        match_key = self.match_key_combo.currentText() if self.match_key_combo else None
        try:
            options = match(result, self.options_box.toPlainText(), match_key=match_key)
        except KeyError as e:
            available = list(raw.keys()) if isinstance(raw, dict) else "<not a dict>"
            self.result_panel.display(
                f"{value_text}   —   match-key {e} not in result; available: {available}",
                [], [],
            )
            return
        except Exception as e:
            self.result_panel.display(f"{value_text}   —   match error: {e}", [], [])
            return

        self.result_panel.display(value_text, options, [], raw_value=raw, match_key=match_key)


def build_form(spec: FormSpec) -> SolverFormWidget:
    return SolverFormWidget(spec)
