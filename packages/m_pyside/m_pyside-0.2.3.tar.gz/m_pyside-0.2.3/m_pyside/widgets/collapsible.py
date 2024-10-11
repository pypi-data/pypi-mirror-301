# -*- coding: utf-8 -*-
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget, QVBoxLayout, QToolButton, QScrollArea, QFrame, QApplication, QSizePolicy


class Collapsible(QWidget):
    toggled = Signal()

    def __init__(self, name: str, expend: bool = False, parent=None):
        super().__init__(parent)
        self.name = name
        self._is_expended = expend
        self.setupUI()

    def setupUI(self):
        vbox_main = QVBoxLayout(self)
        # toggled widget
        self._tool_button = QToolButton(self)
        self._tool_button.setText(self.name)
        self._tool_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self._tool_button.setArrowType(Qt.DownArrow if self._is_expended else Qt.RightArrow)
        self._tool_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self._tool_button.setArrowType(Qt.LeftArrow)
        # scroll widget
        self.scroll_widget = QScrollArea(self)
        self.scroll_widget.setWidgetResizable(True)
        self.frame_widget = QFrame(self)
        self.vbox_frame_main = QVBoxLayout(self.frame_widget)
        self.scroll_widget.hide() if not self._is_expended else None

        vbox_main.addWidget(self._tool_button, 0, Qt.AlignTop)
        vbox_main.addWidget(self.scroll_widget, 1, Qt.AlignTop)
        # slot
        self._tool_button.clicked.connect(self.expand)

    def expand(self):
        if self._is_expended:
            self._tool_button.setArrowType(Qt.RightArrow)
            self._is_expended = False
            self.scroll_widget.hide()
        else:
            self._tool_button.setArrowType(Qt.DownArrow)
            self._is_expended = True
            self.scroll_widget.show()
        self.toggled.emit()

    def add_widget(self, widget: QWidget):
        self.vbox_frame_main.addWidget(widget, 1, Qt.AlignTop)
        self.vbox_frame_main.update()
        self.frame_widget.adjustSize()
        self.scroll_widget.setWidget(self.frame_widget)

