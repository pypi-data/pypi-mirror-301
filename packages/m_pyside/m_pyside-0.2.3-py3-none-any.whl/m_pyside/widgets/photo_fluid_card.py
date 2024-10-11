# -*- coding: utf-8 -*-
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QGridLayout, QScrollArea, QFrame, QVBoxLayout, QLineEdit, \
    QGraphicsDropShadowEffect, QSlider, QHBoxLayout


class PhotoFluidCard(QScrollArea):
    def __init__(self, card_width: int, show_search: bool = False, show_slider: bool = False, parent=None):
        super(PhotoFluidCard, self).__init__(parent)

        self._card_list = []
        self.card_width = card_width
        self.show_search = show_search
        self.show_slider = show_slider

        self.width, self.height = self.rect().size().toTuple()
        self.setWidgetResizable(True)
        self.frame_main = QFrame(self)
        self.frame_main.setContentsMargins(0, 0, 0, 0)
        self.vbox_main = QVBoxLayout(self.frame_main)
        self.vbox_main.setContentsMargins(10, 10, 10, 10)
        if self.show_search:
            self.lineEdit_search = QLineEdit(self.frame_main)
            self.vbox_main.addWidget(self.lineEdit_search)
        if self.show_slider:
            hbox_slider = QHBoxLayout()
            self.slider = QSlider(Qt.Horizontal)
            self.slider.setMaximum(self.card_width * 10)
            self.slider.setTickPosition(QSlider.TicksBelow)
            self.slider.setValue(self.card_width)
            hbox_slider.addWidget(self.slider, 1)
            self.lineEdit_slider = QLineEdit(self.frame_main)
            self.lineEdit_slider.setMaximumWidth(80)
            self.lineEdit_slider.setText(str(self.slider.value()))
            hbox_slider.addWidget(self.lineEdit_slider, 0, Qt.AlignRight)
            self.vbox_main.addLayout(hbox_slider)
        self.grid_main = QGridLayout()
        self.grid_main.setAlignment(Qt.AlignTop)
        self.vbox_main.addLayout(self.grid_main)

        # slot
        self.slider.valueChanged.connect(self._change_size)

    def show_widgets(self):
        """
            显示PhotoFluidCard

        :raises ValueError: 如果没有设置card触发诧异
        :return:
        """
        if self._card_list is None:
            raise ValueError("Card list is empty")
        max_width_count = self.width // (self.card_width + self.grid_main.spacing() * 2)
        row = 0
        column = 0
        for card in self._card_list:  # type: QWidget
            card.setMinimumWidth(self.card_width)
            card.setMinimumHeight(self.card_width)
            self._add_shadow(card)
            if column >= max_width_count:
                row += 1
                column = 0
                self.grid_main.addWidget(card, row, column)
                column += 1
            else:
                self.grid_main.addWidget(card, row, column)
                column += 1
        self.frame_main.adjustSize()
        self.setWidget(self.frame_main)

    def _add_shadow(self, widget: QWidget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(3, 3)
        shadow.setBlurRadius(10)
        shadow.setColor(Qt.gray)
        widget.setGraphicsEffect(shadow)

    def add_card(self):
        pass

    def add_widget(self, widget: QWidget) -> None:
        """
            添加一个自定义widget

        :param widget: widget
        :return:
        """
        self._card_list.append(widget)

    def add_widgets(self, widgets: List[QWidget]) -> None:
        """
            添加自定义widget列表

        :param widgets:
        :return:
        """
        self._card_list.extend(widgets)

    def remove_widget(self, widget: QWidget) -> None:
        """
            移除一个自定义widget

        :param widget: widget
        :return:
        """
        self._card_list.remove(widget)

    def remove_widgets(self, widgets: List[QWidget]) -> None:
        """
            移除widgets列表

        :param widgets:
        :return:
        """
        self._card_list.remove(widgets)

    def _change_size(self, value: int):
        """
            slider 触发函数

        :param value:
        :return:
        """
        self.card_width = value
        self.lineEdit_slider.setText(str(value))
        self.show_widgets()

    def resizeEvent(self, event):
        super(PhotoFluidCard, self).resizeEvent(event)
        self.width, self.height = self.frameSize().toTuple()
        self.show_widgets()

    @property
    def card_count(self) -> int:
        return len(self._card_list)

    @property
    def cards(self) -> list:
        return self._card_list
