# -*- coding: utf-8 -*-
import os
from typing import Optional

from PySide2 import QtWidgets
from PySide2.QtCore import Signal
from PySide2.QtGui import QPixmap, Qt, QFont
from PySide2.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QFrame, QHBoxLayout
from enum import Enum


class SetType(Enum):
    key = 0
    value = 1
    both = 2


class PhotoCard(QtWidgets.QWidget):
    Clicked = Signal()

    def __init__(self, data_info: dict, show_key: bool = False, picture: Optional[QPixmap] = None, parent=None):
        super(PhotoCard, self).__init__(parent)

        self.data_info = data_info
        self.picture = picture
        self._show_key = show_key
        self._label_keys = []
        self._label_values = []
        self.setup_ui()
        self.load_stylesheet()

    def setup_ui(self):
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        frame_widget = QFrame(self)
        frame_widget.setObjectName("photo_card")
        v.addWidget(frame_widget)
        v.addStretch(1)
        vbox_main = QVBoxLayout(frame_widget)
        # picture
        if self.picture:
            self.label_picture = QLabel(self)
            self.label_picture.setPixmap(self.picture)
            vbox_main.addWidget(self.label_picture, 0, Qt.AlignCenter)
        farm_info = QFrame(self)
        vbox_info = QVBoxLayout(farm_info)
        for k, v in self.data_info.items():
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignCenter)
            label_key = QLabel(f'{k}: ')
            label_value = QLabel(f'{v}')
            hbox.addWidget(label_key, 0, Qt.AlignLeft) if self._show_key else None
            hbox.addWidget(label_value, 0, Qt.AlignLeft)
            vbox_info.addLayout(hbox)
            self._label_keys.append(label_key)
            self._label_values.append(label_value)
        vbox_main.addWidget(farm_info, 0, Qt.AlignCenter)
        vbox_main.addStretch(1)

    def load_stylesheet(self):
        with open(os.path.join(os.path.dirname(__file__), "../qss/photo_card.css"), "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def set_font(self, font: QFont, set_type: SetType = SetType.both) -> None:
        """
            修改文字

        :param font: 文字样式
        :param set_type: 修改类型
        :return:
        """
        if set_type == SetType.both:
            for i in self._label_keys:
                i.setFont(font)
            for i in self._label_values:
                i.setFont(font)
        elif set_type == SetType.key:
            for i in self._label_keys:
                i.setFont(font)
        elif set_type == SetType.value:
            for i in self._label_values:
                i.setFont(font)
        else:
            raise ValueError

    def change_picture_size(self, w: int) -> None:
        """
            修改图片大小
        :param w: 宽度
        :return:
        """
        new_pic = self.picture.scaledToWidth(w)
        self.picture = new_pic
        self.label_picture.setPixmap(new_pic)

    def mousePressEvent(self, arg__1):
        super().mousePressEvent(arg__1)
        if arg__1.button() == Qt.LeftButton:
            self.Clicked.emit()
