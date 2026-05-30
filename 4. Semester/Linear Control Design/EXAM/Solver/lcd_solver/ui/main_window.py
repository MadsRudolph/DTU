"""PyQt6 main window. Sidebar shows P1..P7 tree; content area swaps form widgets."""
from __future__ import annotations
import sys
import json
import os
from collections import defaultdict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem,
    QStackedWidget, QLabel, QWidget, QVBoxLayout, QLineEdit,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut

from lcd_solver.ui.form_builder import build_form
from lcd_solver.ui.forms import ALL_FORMS


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("LCD1 Solver — 34722")
        self.resize(1200, 800)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left sidebar panel with Search Box + Tree View
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search solvers, fields, or specs... (Ctrl+F)")
        self.search_box.setClearButtonEnabled(True)
        self.search_box.textChanged.connect(self._on_search_changed)
        self.search_box.setStyleSheet("padding: 5px; font-size: 10pt; border-radius: 4px;")
        left_layout.addWidget(self.search_box)
        
        self.sidebar = QTreeWidget()
        self.sidebar.setHeaderLabels(["Pattern / variant"])
        self.sidebar.setMinimumWidth(280)
        left_layout.addWidget(self.sidebar)
        
        self.content = QStackedWidget()
        placeholder = QLabel("Select a variant from the sidebar or search above.")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("font-size: 12pt; color: gray;")
        self.content.addWidget(placeholder)
        
        splitter.addWidget(left_panel)
        splitter.addWidget(self.content)
        splitter.setStretchFactor(1, 1)
        self.setCentralWidget(splitter)
        
        self._populate_sidebar()
        self.sidebar.itemClicked.connect(self._on_item_clicked)

        # Ctrl+F to focus search box
        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(self.search_box.setFocus)
        
        # Load state
        self._load_state()

    def _populate_sidebar(self) -> None:
        # Add special Smart Paste item at the top
        smart_item = QTreeWidgetItem(self.sidebar, ["★ Smart Paste"])
        smart_item.setStyleSheet(0, "font-weight: bold; color: #007acc;")
        from lcd_solver.ui.smart_paste import SmartPasteWidget
        smart_widget = SmartPasteWidget(self)
        self.content.addWidget(smart_widget)
        smart_item.setData(0, Qt.ItemDataRole.UserRole, smart_widget)

        by_pattern: dict[str, list] = defaultdict(list)
        for spec in ALL_FORMS:
            by_pattern[spec.pattern].append(spec)
        for pattern in sorted(by_pattern):
            top = QTreeWidgetItem(self.sidebar, [pattern])
            top.setStyleSheet(0, "font-weight: bold;")
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

    def _on_search_changed(self, text: str) -> None:
        query = text.strip().lower()
        
        for i in range(self.sidebar.topLevelItemCount()):
            parent = self.sidebar.topLevelItem(i)
            if parent.childCount() == 0:
                # Top level leaf item like Smart Paste
                match_found = (not query or query in parent.text(0).lower() or "paste" in query or "smart" in query)
                parent.setHidden(not match_found)
                continue
                
            parent_visible = False
            
            for j in range(parent.childCount()):
                child = parent.child(j)
                child_text = child.text(0).lower()
                widget = child.data(0, Qt.ItemDataRole.UserRole)
                match_found = False
                
                if query in child_text or query in parent.text(0).lower():
                    match_found = True
                elif widget and hasattr(widget, "spec"):
                    spec = widget.spec
                    if (query in spec.title.lower() or 
                        query in (spec.explanation or "").lower() or
                        any(query in f.name.lower() or query in f.label.lower() for f in spec.fields)):
                        match_found = True
                
                child.setHidden(not match_found)
                if match_found:
                    parent_visible = True
            
            parent.setHidden(not parent_visible)
            
        if query:
            self.sidebar.expandAll()

    def _get_state_path(self) -> str:
        folder = os.path.expanduser("~/.lcd_solver")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, "state.json")

    def _load_state(self) -> None:
        path = self._get_state_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                state = json.load(f)
            
            if "width" in state and "height" in state:
                self.resize(state["width"], state["height"])
            if "x" in state and "y" in state:
                self.move(state["x"], state["y"])
                
            last_pattern = state.get("last_selected_pattern")
            last_variant = state.get("last_selected_variant")
            if last_pattern and last_variant:
                for i in range(self.sidebar.topLevelItemCount()):
                    parent = self.sidebar.topLevelItem(i)
                    if parent.text(0) == last_pattern:
                        for j in range(parent.childCount()):
                            child = parent.child(j)
                            if child.text(0) == last_variant:
                                self.sidebar.setCurrentItem(child)
                                self._on_item_clicked(child, 0)
                                break
        except Exception:
            pass

    def _save_state(self) -> None:
        state = {
            "width": self.width(),
            "height": self.height(),
            "x": self.x(),
            "y": self.y(),
        }
        item = self.sidebar.currentItem()
        if item and item.parent():
            state["last_selected_pattern"] = item.parent().text(0)
            state["last_selected_variant"] = item.text(0)
            
        try:
            with open(self._get_state_path(), "w", encoding="utf-8") as f:
                json.dump(state, f, indent=4)
        except Exception:
            pass

    def closeEvent(self, event) -> None:
        self._save_state()
        super().closeEvent(event)


def launch(argv: list[str]) -> int:
    app = QApplication(argv)
    win = MainWindow()
    win.show()
    return app.exec()
