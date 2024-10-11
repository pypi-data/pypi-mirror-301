# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime
from typing import List

from PySide2.QtCore import Signal
from PySide2.QtGui import QIcon, QPixmap, Qt, QCursor
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QTableWidget, QTreeWidgetItem, \
    QTableWidgetItem, QMenu

from m_pyside.modules.dataclass import FileType
from m_pyside.util import get_resource_path


class FileListWidget(QWidget):
    SelectedItem = Signal()

    def __init__(self, title: str, paths: List[str], show_check_box: bool = False, parent=None):
        """
            需要显示目录路径

        :param paths: 路径
        :param parent:
        :raises FileNotFoundError: 目录不存在时候提示报错
        """
        super(FileListWidget, self).__init__(parent)

        self.show_type = None
        self._check_path_exists(paths)
        self.title = title
        self.paths = paths
        self.show_check_box = show_check_box
        self.icon_size = 30
        self.check_box_show_type = []
        if self.show_check_box:
            self.table_head = (" ", "ico", "Version", "Name", "Date", "Path", "Type")
        else:
            self.table_head = ("ico", "Version", "Name", "Date", "Path", "Type")
        self.setup_ui()

    def setup_ui(self):
        vbox_main = QVBoxLayout(self)
        # top
        hbox_top = QHBoxLayout()
        self.label_title = QLabel(self.title)
        hbox_top.addWidget(self.label_title)
        hbox_top.addStretch(1)

        vbox_main.addLayout(hbox_top)
        # file list
        self.table_widget_file = QTableWidget(self)
        self.table_widget_file.setColumnCount(len(self.table_head))
        self.table_widget_file.setHorizontalHeaderLabels(self.table_head)
        self.table_widget_file.setSortingEnabled(True)
        self.table_widget_file.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_widget_file.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget_file.customContextMenuRequested.connect(self.setup_table_menu)
        self.insert_table()
        vbox_main.addWidget(self.table_widget_file, 1)
        # filter
        if not self.show_type:
            return
        hbox_show_type = QHBoxLayout()
        hbox_show_type.setSpacing(15)
        hbox_show_type.setAlignment(Qt.AlignRight)
        label_show_type = QLabel("ShowType:")
        hbox_show_type.addWidget(label_show_type)
        for show in self.show_type:
            check_box = QCheckBox(show.upper())
            check_box.setChecked(True)
            hbox_show_type.addWidget(check_box)
            check_box.toggled.connect(self.show_hide_table)
            self.check_box_show_type.append(check_box)
        vbox_main.addLayout(hbox_show_type)

    def insert_table(self):
        resource_path = get_resource_path()
        count = 0
        row = 0
        self.show_type = []
        for p in self.paths:
            if not os.listdir(p):
                continue
            for file in os.listdir(p):
                count += 1

        self.table_widget_file.setRowCount(count)
        for p in self.paths:
            dir_path = p.replace('\\', '/')
            if not os.listdir(dir_path):
                continue
            for file in os.listdir(dir_path):
                full_path = os.path.join(dir_path, file).replace('\\', '/')
                if self.show_check_box:
                    check_box = QCheckBox()
                    self.table_widget_file.setCellWidget(row, 0, check_box)
                if os.path.isfile(full_path):
                    file_type = full_path.split(".")[-1]
                    # set icon
                    self.insert_ico(file_type, resource_path, row)
                    # set version
                    self.insert_version(file, row)
                    # set file name
                    self.insert_name(file, row)
                    # insert date
                    self.insert_date(full_path, row)
                    # set path
                    self.insert_path(dir_path, row)
                    self.insert_show_type(full_path, row)
                else:
                    self.insert_ico("dir", resource_path, row)
                    # set version
                    self.insert_version(file, row)
                    # set file name
                    self.insert_name(file, row)
                    # insert date
                    self.insert_date(full_path, row)
                    # set path
                    self.insert_path(dir_path, row)
                    self.insert_show_type(full_path, row)

                row += 1
        self.table_widget_file.resizeColumnsToContents()

    def show_hide_table(self):
        show_type = [i.text().upper() for i in list(filter(lambda x: x.isChecked() == True, self.check_box_show_type))]
        for row in range(self.table_widget_file.rowCount()):
            type = self.table_widget_file.item(row, 6 if self.show_check_box else 5).text()
            if type in show_type:
                self.table_widget_file.showRow(row)
            else:
                self.table_widget_file.hideRow(row)

    def setup_table_menu(self):
        menu = QMenu()
        open_folder = menu.addAction("Open folder")
        exec_ = menu.exec_(QCursor.pos())
        if exec_:
            self.open_folder()

    def open_folder(self):
        selected_row = self._get_selected_row()
        for row in selected_row:
            folder_path = self.table_widget_file.item(row, 4 if not self.show_check_box else 5).text()
            if not os.path.exists(folder_path):
                raise FileNotFoundError(folder_path)
            os.startfile(folder_path)

    def get_all_path(self):
        selected_row = self._get_selected_row()
        p = []
        for row in selected_row:
            full_path = os.path.join(self.table_widget_file.item(row, 4 if not self.show_check_box else 5).text(),
                                     self.table_widget_file.item(row,
                                                                 2 if not self.show_check_box else 4).text()).replace(
                '\\', '/')
            p.append(full_path)
        return p

    def _get_selected_row(self) -> List[int]:
        if not self.table_widget_file.selectedItems():
            return
        selected_row = list(set([i.row() for i in self.table_widget_file.selectedItems()]))
        return selected_row

    def insert_ico(self, file_type: str, resource_path: str, row: int):
        path_icon = None
        if file_type == FileType.abc.value:
            path_icon = QPixmap(
                os.path.join(resource_path, "abc_logo.png").replace('\\', '/')).scaledToWidth(
                self.icon_size)
            self.show_type.append(FileType.abc.value) if FileType.abc.value not in self.show_type else None
        elif file_type == FileType.ass.value:
            path_icon = QPixmap(
                os.path.join(resource_path, "ass_logo.png").replace('\\', '/')).scaledToWidth(
                self.icon_size)
            self.show_type.append(FileType.ass.value) if FileType.ass.value not in self.show_type else None
        elif file_type == FileType.fbx.value:
            path_icon = QPixmap(
                os.path.join(resource_path, "fbx_logo.png").replace('\\', '/')).scaledToWidth(
                self.icon_size)
            self.show_type.append(FileType.fbx.value) if FileType.fbx.value not in self.show_type else None
        elif file_type == FileType.ma.value or file_type == FileType.mb.value:
            path_icon = QPixmap(
                os.path.join(resource_path, "maya.jpg").replace('\\', '/')).scaledToWidth(
                self.icon_size)
            self.show_type.append(FileType.ma.value) if FileType.ma.value not in self.show_type else None
        elif file_type == FileType.sp.value:
            path_icon = QPixmap(
                os.path.join(resource_path, "sp.png").replace('\\', '/')).scaledToWidth(
                self.icon_size)
            self.show_type.append(FileType.sp.value) if FileType.sp.value not in self.show_type else None
        elif file_type == FileType.dir.value:
            path_icon = QPixmap(
                os.path.join(resource_path, "dir.png").replace('\\', '/')).scaledToWidth(
                self.icon_size)
            self.show_type.append(FileType.dir.value) if FileType.dir.value not in self.show_type else None
        label_icon = QLabel()
        label_icon.setAlignment(Qt.AlignCenter)
        label_icon.setPixmap(path_icon)
        self.table_widget_file.setCellWidget(row, 1 if self.show_check_box else 0, label_icon)

    def insert_version(self, file_name: str, row: int):
        if not re.search(r"v\d+", file_name):
            return
        version = re.search(r"(v\d+)", file_name).group(1)
        item_version = QTableWidgetItem(version)
        self.table_widget_file.setItem(row, 2 if self.show_check_box else 1, item_version)

    def insert_name(self, file_name: str, row: int):
        item = QTableWidgetItem(file_name)
        self.table_widget_file.setItem(row, 3 if self.show_check_box else 2, item)

    def insert_date(self, path: str, row: int):
        modify_date = os.path.getmtime(path)
        formatted_date = datetime.fromtimestamp(modify_date).strftime('%Y-%m-%d %H:%M:%S')
        item = QTableWidgetItem(formatted_date)
        self.table_widget_file.setItem(row, 4 if self.show_check_box else 3, item)

    def insert_path(self, path: str, row: int):
        item = QTableWidgetItem(path)
        self.table_widget_file.setItem(row, 5 if self.show_check_box else 4, item)

    def insert_show_type(self, path: str, row: int):
        dir_type = None
        if os.path.isdir(path):
            dir_type = FileType.dir.value
        else:
            dir_type = os.path.splitext(path)[1].removeprefix(".").upper()

        item = QTableWidgetItem(dir_type.upper())
        self.table_widget_file.setItem(row, 6 if self.show_check_box else 5, item)

    @staticmethod
    def _check_path_exists(paths: List[str]):
        for path in paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f'File {path} does not exist')
