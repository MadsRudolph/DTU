"""Smart Paste tab: offline question parser and router.

Detects transfer functions, spec constraints, and options from pasted text
using deterministic regex and keyword matching. Automatically populates the
target form and navigates to it.
"""
from __future__ import annotations
import re
from typing import Any

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit,
    QMessageBox, QGroupBox,
)
from PyQt6.QtCore import Qt


class SmartPasteWidget(QWidget):
    def __init__(self, main_window: Any) -> None:
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>★ Smart Paste (Offline Exam Question Parser)</h2>"))

        explanation = QLabel(
            "Paste a full exam question including the prompt and multiple-choice options below. "
            "The tool will use deterministic parsing to identify the correct solver form, pre-fill all "
            "detected parameters and options, and jump directly to that form for you."
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet(
            "background-color: #eef2f7; border-left: 4px solid #007acc; "
            "padding: 10px; color: #334155; font-size: 10pt; border-radius: 4px;"
        )
        layout.addWidget(explanation)

        layout.addWidget(QLabel("<b>Paste Exam Question text here:</b>"))
        self.input_area = QPlainTextEdit()
        self.input_area.setPlaceholderText(
            "Example:\n"
            "Closed-loop TF is K / (s**2 + 2*s + K). Step response shows 17% overshoot. Find omega_d.\n"
            "Options:\n"
            "0.87\n"
            "1.0\n"
            "1.73\n"
            "2.0 rad/s"
        )
        layout.addWidget(self.input_area)

        # Buttons
        btn_layout = QHBoxLayout()
        parse_btn = QPushButton("Parse Question & Jump to Form")
        parse_btn.setStyleSheet("font-weight: bold; background-color: #007acc; color: white; padding: 8px;")
        parse_btn.clicked.connect(self._on_parse)
        btn_layout.addWidget(parse_btn)

        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("padding: 8px;")
        clear_btn.clicked.connect(self.input_area.clear)
        btn_layout.addWidget(clear_btn)

        layout.addLayout(btn_layout)

    def _on_parse(self) -> None:
        text = self.input_area.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty input", "Please paste some question text first.")
            return

        routing = self.parse_question(text)
        if not routing or not routing.get("solver_function"):
            QMessageBox.information(
                self, "Parsing Unsuccessful",
                "Could not automatically match this question to a specific pattern.\n"
                "Please select the correct solver manually from the sidebar."
            )
            return

        func_name = routing["solver_function"]
        inputs = routing["inputs"]
        options = routing["options"]

        # Find and navigate to the target form in the main window
        found = False
        for i in range(self.main_window.sidebar.topLevelItemCount()):
            parent = self.main_window.sidebar.topLevelItem(i)
            for j in range(parent.childCount()):
                child = parent.child(j)
                widget = child.data(0, Qt.ItemDataRole.UserRole)
                if widget and hasattr(widget, "spec") and widget.spec.solver_function == func_name:
                    # Clear the form first
                    widget._on_reset()

                    # Pre-fill inputs
                    for k, v in inputs.items():
                        if k in widget._field_widgets:
                            w = widget._field_widgets[k]
                            # Check field spec
                            fspec = next((f for f in widget.spec.fields if f.name == k), None)
                            if fspec and fspec.kind == "tf":
                                w.edit.setText(str(v))
                            elif hasattr(w, "setCurrentText"):
                                w.setCurrentText(str(v))
                            else:
                                w.setText(str(v))

                    # Pre-fill options
                    if options:
                        widget.options_box.setPlainText(options)

                    # Update visibility
                    widget._update_field_visibility()

                    # Switch current tree item and widget view
                    self.main_window.sidebar.setCurrentItem(child)
                    self.main_window.content.setCurrentWidget(widget)
                    found = True
                    break
            if found:
                break

        if found:
            QMessageBox.information(
                self, "Parse & Route Successful",
                f"Automatically matched to form: '{parent.text(0)} — {child.text(0)}'!\n"
                f"Populated {len(inputs)} fields and {len(options.splitlines())} options. Ready to solve!"
            )
        else:
            QMessageBox.warning(
                self, "Form Not Found",
                f"Matched to solver '{func_name}', but could not locate that form in the UI."
            )

    def parse_question(self, text: str) -> dict[str, Any] | None:
        """Deterministic parser that extracts TF, specifications, and options."""
        lower_text = text.lower()

        # Extract Options (usually isolated numbers or text lines near the end)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        options_list = []

        # Try to find labeled options anywhere in the text (even split on a single line)
        # e.g. "a) MD = 5.5 dB b) MD = 3.55 dB" or "A. 1.73 B. 2.0"
        opt_matches = re.findall(
            r"\b([a-eA-E])[\s\)\.\:]{1,3}(?:[A-Z_a-z0-9\(\)]+\s*=\s*)?\s*(-?\d+(?:\.\d+)?(?:\s*dB|\s*rad/s|°|%)?)\b",
            text
        )
        if len(opt_matches) >= 3:
            options_list = [m[1] for m in opt_matches]
        else:
            # Fall back to line-by-line parsing for isolated options
            for ln in lines:
                cleaned = ln.strip()
                if "options" in cleaned.lower() or "facit" in cleaned.lower():
                    continue
                # Match a line that looks like an option (optionally labeled and with variable assignment)
                # e.g. "a) 1.73" or "1.73" or "MD = 11 dB"
                m = re.match(r"^(?:[a-eA-E][\)\.\:\s]+)?(?:[A-Z_a-z0-9\(\)]+\s*=\s*)?\s*(-?\d+(?:\.\d+)?(?:\s*dB|\s*rad/s|°|%)?)$", cleaned, re.I)
                if m:
                    sub_m = re.search(r"(-?\d+(?:\.\d+)?(?:\s*dB|\s*rad/s|°|%)?)", cleaned, re.I)
                    if sub_m:
                        options_list.append(sub_m.group(1))
                elif re.match(r"^\s*(-?\d+(?:\.\d+)?(?:\s*dB|\s*rad/s|°|%)?)\s*$", cleaned, re.I):
                    options_list.append(cleaned)

        options = "\n".join(options_list)

        # 1. ODE -> TF (P1)
        if re.search(r"\bodes?\b", lower_text) or "differential equation" in lower_text:
            y_coeffs = ""
            u_coeffs = ""
            # Look for coeffs pattern, e.g. "y'' + 2y' + y = u"
            # Simple fallback: let student type them, but route to form
            return {
                "solver_function": "solve_ode_to_tf",
                "inputs": {},
                "options": options
            }

        # 2. State-space -> TF (P1)
        if "state matrix" in lower_text or "state-space" in lower_text or re.search(r"\bA\s*=\s*", text):
            return {
                "solver_function": "solve_state_space_to_tf",
                "inputs": {},
                "options": options
            }

        # 3. Block reduction (P1)
        if "block diagram" in lower_text or "dsl" in lower_text or "feedback(" in lower_text:
            return {
                "solver_function": "reduce_block_diagram",
                "inputs": {},
                "options": options
            }

        # 4. Bode composition (P2)
        if "bode" in lower_text and ("slope" in lower_text or "corners" in lower_text):
            return {
                "solver_function": "compose_tf_from_bode",
                "inputs": {},
                "options": options
            }

        # 5. Margins (P3)
        if "margin" in lower_text and ("gain crossover" in lower_text or "phase crossover" in lower_text or re.search(r"\b(?:gm|pm)\b", lower_text)):
            # Extract plant if present
            plant = self._extract_tf(text)
            return {
                "solver_function": "solve_margins",
                "inputs": {"G": plant} if plant else {},
                "options": options
            }

        # 6. Proportional PM (P6)
        if ("proportional controller" in lower_text or "k_p for" in lower_text or "pm of" in lower_text) and "target pm" in lower_text:
            plant = self._extract_tf(text)
            pm_val = self._extract_number(text, r"\b(?:pm|phase margin)\b\s*(?:of|is|=)?\s*(\d+(?:\.\d+)?)(?:°|deg)?")
            inputs = {}
            if plant:
                inputs["G"] = plant
            if pm_val:
                inputs["target_PM_deg"] = pm_val
            return {
                "solver_function": "solve_P_for_PM",
                "inputs": inputs,
                "options": options
            }

        # 7. PI-Lead design (P6)
        if "pi-lead" in lower_text or "phase budget" in lower_text or "crossover frequency" in lower_text:
            # Extract wc, PM, plant phase
            wc = self._extract_number(text, r"\b(?:omega_c|ω_c|w_c)\b\s*=\s*(\d+(?:\.\d+)?)")
            if not wc:
                wc = self._extract_number(text, r"\|G(?:ol)?\(\s*(?:j\s*\*?\s*)?(\d+(?:\.\d+)?)(?:\s*\*?\s*j)?\s*\)\|\s*=\s*1")
            pm = self._extract_number(text, r"\b(?:gamma_m|γ_m|pm)\b\s*=\s*(\d+(?:\.\d+)?)")
            phi_g = self._extract_number(text, r"\b(?:phi_g|φ_g|phase)\b\s*=\s*([-\d\.]+)")
            inputs = {}
            if wc:
                inputs["omega_c"] = str(wc)
            if pm:
                inputs["gamma_M_deg"] = pm
            if phi_g:
                inputs["phi_G_deg"] = str(phi_g)
            return {
                "solver_function": "solve_pi_lead",
                "inputs": inputs,
                "options": options
            }

        # 8. Nested steady state (P7)
        if "nested" in lower_text or "inner loop" in lower_text or "two_kp_same" in lower_text:
            return {
                "solver_function": "solve_nested_ess",
                "inputs": {},
                "options": options
            }

        # 9. Feedforward formula (P7)
        if "feedforward" in lower_text or "proper-fast" in lower_text:
            n_lags = self._extract_number(text, r"\b(\d+)\s+(?:first-order lags|lags)")
            inputs = {}
            if n_lags:
                inputs["n_lags"] = int(n_lags)
            return {
                "solver_function": "pick_feedforward_form",
                "inputs": inputs,
                "options": options
            }

        # 10. Steady-state error table (P5)
        if "steady-state error" in lower_text or "system type" in lower_text or re.search(r"\bess\b", lower_text):
            plant = self._extract_tf(text)
            if plant:
                return {
                    "solver_function": "solve_ess_table",
                    "inputs": {"G": plant},
                    "options": options
                }
            return {
                "solver_function": "solve_KP_from_ess",
                "inputs": {},
                "options": options
            }

        # 11. Closed-loop 2nd order (P4)
        if "closed-loop" in lower_text or "overshoot" in lower_text or "damping ratio" in lower_text or "omega_d" in lower_text or "omega_n" in lower_text:
            # Check for closed loop TF
            cl_tf = self._extract_tf(text)
            if not cl_tf:
                # Fallback to general G(s)
                cl_tf = "K / (s**2 + 2*s + K)"
            
            # Find overshoot
            overshoot = self._extract_number(text, r"(\d+(?:\.\d+)?)\%\s*overshoot")
            if not overshoot:
                overshoot = self._extract_number(text, r"\b(?:m_p|mp)\b\s*=\s*(\d+(?:\.\d+)?)")
            
            given_value = None
            given_kind = "Mp"
            if overshoot:
                # Convert e.g. 17% -> 0.17
                given_value = float(overshoot) / 100.0 if float(overshoot) > 1.0 else float(overshoot)
                given_kind = "Mp"
            else:
                # Try zeta
                zeta = self._extract_number(text, r"\b(?:zeta|ζ)\b\s*=\s*(\d+(?:\.\d+)?)")
                if zeta:
                    given_value = float(zeta)
                    given_kind = "zeta"

            inputs = {
                "closed_loop_str": cl_tf
            }
            if given_value is not None:
                inputs["given_kind"] = given_kind
                inputs["given_value"] = given_value

            return {
                "solver_function": "solve_closed_loop_2nd_order",
                "inputs": inputs,
                "options": options
            }

        # 12. Stable-K range default (P3)
        if "stable for" in lower_text or "range of k" in lower_text or "stability" in lower_text:
            plant = self._extract_tf(text)
            if plant:
                return {
                    "solver_function": "solve_stable_K_range",
                    "inputs": {"G": plant},
                    "options": options
                }

        # Fallback to Margins if TF is present
        plant = self._extract_tf(text)
        if plant:
            return {
                "solver_function": "solve_margins",
                "inputs": {"G": plant},
                "options": options
            }

        return None

    def _extract_tf(self, text: str) -> str | None:
        """Find transfer function-like strings."""
        # Look for G(s) = ... or G = ...
        m = re.search(r"\b(?:g\(s\)|g|t\(s\))\s*=\s*([a-z0-9\/\*\+\-\s\(\)\*\*]+)", text, re.I)
        if m:
            candidate = m.group(1).split("\n")[0].strip()
            # Remove ending punctuation/options
            candidate = re.sub(r"[\.,;].*$", "", candidate)
            return candidate
        # Look for K / (s... or any fraction like string
        m = re.search(r"([a-z0-9_]+\s*\/\s*\([a-z0-9_\s\*\+\-\(\)]+\))", text, re.I)
        if m:
            return m.group(1).strip()
        return None

    def _extract_number(self, text: str, pattern: str) -> float | None:
        m = re.search(pattern, text, re.I)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
        return None
