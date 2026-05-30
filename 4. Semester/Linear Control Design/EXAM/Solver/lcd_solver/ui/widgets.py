"""Reusable PyQt6 widgets for the LCD solver UI."""
from __future__ import annotations
import math
from typing import Callable

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPlainTextEdit, QGroupBox, QPushButton, QTableWidget, QTableWidgetItem,
)
from PyQt6.QtGui import QColor

from lcd_solver.tf_input import parse_tf, describe_tf


class TFInputWidget(QWidget):
    """Single-line text input for a transfer function, echoes describe_tf below."""

    def __init__(self, label: str = "G(s)") -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("e.g. 12/((s+2)*(s+3))")
        row.addWidget(self.edit)
        layout.addLayout(row)
        self.echo = QLabel("")
        self.echo.setWordWrap(True)
        layout.addWidget(self.echo)
        self.edit.textChanged.connect(self._refresh_echo)

    def _refresh_echo(self) -> None:
        text = self.edit.text().strip()
        if not text:
            self.echo.setText("")
            return
        try:
            G = parse_tf(text)
            d = describe_tf(G)
            warn = ""
            if d["has_rhp_pole"]:
                warn = "<br><b><span style='color:red'>⚠ RHP pole present — unstable plant</span></b>"
            poles = ", ".join(f"{p.real:.3g}{'+' if p.imag>=0 else '-'}{abs(p.imag):.3g}j" for p in d["poles"])
            zeros = ", ".join(f"{z.real:.3g}{'+' if z.imag>=0 else '-'}{abs(z.imag):.3g}j" for z in d["zeros"]) or "—"
            dc_line = ""
            if not math.isnan(d["dc_gain_linear"]):
                dc_line = f"<br>DC gain: {d['dc_gain_linear']:.4g} ({d['dc_gain_dB']:.2f} dB)"
            self.echo.setText(f"poles: {poles}<br>zeros: {zeros}{dc_line}{warn}")
        except Exception as e:
            self.echo.setText(f"<span style='color:red'>parse error: {e}</span>")

    def get_tf(self):
        return parse_tf(self.edit.text().strip())


class ResultPanel(QGroupBox):
    """Computed value (top), ranked options table (middle), traps footnote (bottom)."""

    def __init__(self) -> None:
        super().__init__("Result")
        layout = QVBoxLayout(self)
        self.value_label = QLabel("—")
        self.value_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(self.value_label)
        self.options_table = QTableWidget(0, 2)
        self.options_table.setHorizontalHeaderLabels(["Option", "Flag"])
        layout.addWidget(self.options_table)
        self.traps_label = QLabel("")
        self.traps_label.setStyleSheet("color: #b58900;")
        self.traps_label.setWordWrap(True)
        layout.addWidget(self.traps_label)

    def display(self, value_text: str, options, traps: list[str]) -> None:
        self.value_label.setText(value_text)
        self.options_table.setRowCount(len(options))
        for i, opt in enumerate(options):
            self.options_table.setItem(i, 0, QTableWidgetItem(opt.raw_text))
            cell = QTableWidgetItem(opt.flag)
            if opt.flag == "match":
                cell.setBackground(QColor(180, 230, 180))
            elif opt.flag == "also_plausible":
                cell.setBackground(QColor(230, 230, 180))
            elif opt.flag == "unparseable":
                cell.setBackground(QColor(230, 180, 180))
            self.options_table.setItem(i, 1, cell)
        self.traps_label.setText(" • ".join(traps) if traps else "")
