"""PyQt6 main window. Sidebar shows P1..P7 tree; content area swaps form widgets."""
from __future__ import annotations
import sys
from collections import defaultdict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QLabel, QWidget,
)
from PyQt6.QtCore import Qt

from lcd_solver.ui.form_builder import build_form
from lcd_solver.ui.forms import ALL_FORMS


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("LCD1 Solver — 34722")
        self.resize(1200, 800)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.sidebar = QTreeWidget()
        self.sidebar.setHeaderLabels(["Pattern / variant"])
        self.sidebar.setMinimumWidth(280)
        self.content = QStackedWidget()
        placeholder = QLabel("Select a variant from the sidebar.")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content.addWidget(placeholder)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.content)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)
        self._populate_sidebar()
        self.sidebar.itemClicked.connect(self._on_item_clicked)

    def _populate_sidebar(self) -> None:
        by_pattern: dict[str, list] = defaultdict(list)
        for spec in ALL_FORMS:
            by_pattern[spec.pattern].append(spec)
        for pattern in sorted(by_pattern):
            top = QTreeWidgetItem(self.sidebar, [pattern])
            for spec in by_pattern[pattern]:
                child = QTreeWidgetItem(top, [spec.variant])
                widget = build_form(spec)
                self.content.addWidget(widget)
                child.setData(0, Qt.ItemDataRole.UserRole, widget)
        self.sidebar.expandAll()

    def _on_item_clicked(self, item: QTreeWidgetItem, _col: int) -> None:
        widget = item.data(0, Qt.ItemDataRole.UserRole)
        if isinstance(widget, QWidget):
            self.content.setCurrentWidget(widget)


def launch(argv: list[str]) -> int:
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    return app.exec()
