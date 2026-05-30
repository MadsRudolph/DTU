"""PyQt6 main window. Sidebar shows P1..P7 tree; content area swaps form widgets."""
from __future__ import annotations
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QLabel, QWidget,
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("LCD1 Solver — 34722")
        self.resize(1100, 700)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.sidebar = QTreeWidget()
        self.sidebar.setHeaderLabels(["Pattern / variant"])
        self.sidebar.setMinimumWidth(260)

        self.content = QStackedWidget()
        placeholder = QLabel("Select a pattern from the sidebar.")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content.addWidget(placeholder)

        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.content)
        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)
        self._populate_sidebar()
        self.sidebar.itemClicked.connect(self._on_item_clicked)

    def _populate_sidebar(self) -> None:
        # Populated by Task 21 as forms are added. Skeleton just shows the patterns.
        for label in ["P1 — Models", "P2 — Bode", "P3 — Stability",
                      "P4 — 2nd-order", "P5 — ess", "P6 — Controllers", "P7 — Theory"]:
            QTreeWidgetItem(self.sidebar, [label])
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
