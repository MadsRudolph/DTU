"""Reusable PyQt6 widgets for the LCD solver UI."""
from __future__ import annotations
import math
from typing import Callable

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPlainTextEdit, QGroupBox, QPushButton, QTableWidget, QTableWidgetItem,
    QSplitter, QStackedWidget, QHeaderView,
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

from lcd_solver.tf_input import parse_tf, describe_tf


def get_unit(key: str) -> str:
    if key.startswith("omega_") or key == "omega":
        return "rad/s"
    if key.startswith("t_") and not key.startswith("type"):
        return "s"
    if key == "Mp":
        return "fraction"
    if key == "Mp_pct":
        return "%"
    if key == "GM_dB" or key.endswith("_dB"):
        return "dB"
    if key == "PM_deg" or key.endswith("_deg"):
        return "°"
    if key in ("zeta", "K", "N_i", "alpha", "K_p", "K_v", "K_a"):
        return "dimensionless"
    return "dimensionless"


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
    """Computed value (left), ranked options table (right), traps footnote (bottom)."""

    def __init__(self, on_key_selected_callback: Callable[[str], None] | None = None) -> None:
        super().__init__("Result & Options Matching")
        self.on_key_selected_callback = on_key_selected_callback

        main_layout = QVBoxLayout(self)

        # Splitter to allow resizing of results table vs options table
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)

        # Left Panel (Simple Value label or Key-Value dictionary table)
        self.left_stacked = QStackedWidget()
        self.splitter.addWidget(self.left_stacked)

        # Stack 0: Simple value label
        self.value_label = QLabel("—")
        self.value_label.setStyleSheet("font-size: 14pt; font-weight: bold; padding: 10px;")
        self.value_label.setWordWrap(True)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.left_stacked.addWidget(self.value_label)

        # Stack 1: Detailed Dictionary Table
        self.dict_table = QTableWidget(0, 3)
        self.dict_table.setHorizontalHeaderLabels(["Metric (Key)", "Computed Value", "Unit"])
        self.dict_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.dict_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.dict_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.dict_table.setAlternatingRowColors(True)
        self.dict_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.dict_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.dict_table.cellClicked.connect(self._on_dict_row_clicked)
        self.left_stacked.addWidget(self.dict_table)

        # Right Panel: Options & Traps
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.addWidget(QLabel("<b>Pasted Options Matcher:</b>"))

        self.options_table = QTableWidget(0, 3)
        self.options_table.setHorizontalHeaderLabels(["Option", "Flag", "Note / Distractor Trap Check"])
        self.options_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.options_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.options_table.horizontalHeader().setStretchLastSection(True)
        self.options_table.setAlternatingRowColors(True)
        self.options_table.cellClicked.connect(self._on_options_row_clicked)
        right_layout.addWidget(self.options_table)

        self.traps_label = QLabel("")
        self.traps_label.setStyleSheet("color: #b58900; font-style: italic;")
        self.traps_label.setWordWrap(True)
        right_layout.addWidget(self.traps_label)

        self.splitter.addWidget(right_container)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)

        self._current_dict: dict[str, Any] = {}
        self._current_match_key: str | None = None

    def _on_dict_row_clicked(self, row: int, _col: int) -> None:
        item = self.dict_table.item(row, 0)
        if item and self.on_key_selected_callback:
            key_name = item.text()
            self.on_key_selected_callback(key_name)

    def _on_options_row_clicked(self, row: int, _col: int) -> None:
        note_item = self.options_table.item(row, 2)
        if not note_item or not self.on_key_selected_callback:
            return
        text = note_item.text()
        mentioned_keys = []
        for key in self._current_dict.keys():
            if f" {key} " in f" {text} " or f"near: {key}" in text or f"closest: {key}" in text:
                mentioned_keys.append(key)
        if mentioned_keys:
            self.on_key_selected_callback(mentioned_keys[0])

    def display(self, value_text: str, options, traps: list[str] = None, raw_value: Any = None, match_key: str | None = None) -> None:
        if traps is None:
            traps = []
        self._current_dict = {}
        self._current_match_key = match_key

        if isinstance(raw_value, dict):
            self._current_dict = raw_value
            self.left_stacked.setCurrentWidget(self.dict_table)
            self.dict_table.setRowCount(len(raw_value))
            for i, (k, v) in enumerate(raw_value.items()):
                key_item = QTableWidgetItem(k)
                key_item.setFlags(key_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                if isinstance(v, (int, float)):
                    val_str = f"{float(v):.6g}"
                else:
                    val_str = str(v)
                val_item = QTableWidgetItem(val_str)
                val_item.setFlags(val_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                unit_item = QTableWidgetItem(get_unit(k))
                unit_item.setFlags(unit_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                if match_key == k:
                    bg_color = QColor(190, 220, 255)
                    key_item.setBackground(bg_color)
                    val_item.setBackground(bg_color)
                    unit_item.setBackground(bg_color)
                    font = key_item.font()
                    font.setBold(True)
                    key_item.setFont(font)
                    val_item.setFont(font)
                    unit_item.setFont(font)

                self.dict_table.setItem(i, 0, key_item)
                self.dict_table.setItem(i, 1, val_item)
                self.dict_table.setItem(i, 2, unit_item)
        else:
            self.left_stacked.setCurrentWidget(self.value_label)
            self.value_label.setText(value_text)

        self.options_table.setRowCount(len(options))
        for i, opt in enumerate(options):
            opt_item = QTableWidgetItem(opt.raw_text)
            opt_item.setFlags(opt_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.options_table.setItem(i, 0, opt_item)

            cell = QTableWidgetItem(opt.flag)
            cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if opt.flag == "match":
                cell.setBackground(QColor(180, 240, 180))
                cell.setForeground(QColor(0, 80, 0))
            elif opt.flag == "also_plausible":
                cell.setBackground(QColor(255, 240, 160))
                cell.setForeground(QColor(100, 70, 0))
            elif opt.flag == "unparseable":
                cell.setBackground(QColor(255, 180, 180))
                cell.setForeground(QColor(120, 0, 0))
            self.options_table.setItem(i, 1, cell)

            note = getattr(opt, "note", "") or ""
            note_item = QTableWidgetItem(note)
            note_item.setFlags(note_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            if "near:" in note or "closest:" in note:
                note_item.setForeground(QColor(0, 100, 200))
                note_item.setToolTip("Click this note to automatically match against this key!")
            self.options_table.setItem(i, 2, note_item)

        self.traps_label.setText(" • ".join(traps) if traps else "")
