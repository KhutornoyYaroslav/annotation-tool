from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject


class FilesWidgetEvents(QObject):
    curr_file_changed = pyqtSignal(int)


class FilesWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        # Events
        self.events = FilesWidgetEvents(self)
        # Widgets
        self.top_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.list_widget = QtWidgets.QListWidget(self)
        # self.button_status = QtWidgets.QPushButton(self)

    def initGUI(self):
        self.setTitle("Files")
        self.setLayout(self.top_layout)

        # Top layout
        self.top_layout.addWidget(self.list_widget)
        self.top_layout.addLayout(self.buttons_layout)

        # List
        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

        # Buttons layout
        # self.buttons_layout.addWidget(self.button_status)

        # Buttons
        # self.button_status.setText("Mark as done")
        # self.button_status.clicked.connect(self.on_button_status_clicled)

    def set_files(self, fnames: List[str]):
        self.list_widget.clear()
        for fname in fnames:
            self.list_widget.addItem(fname)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def on_current_row_changed(self, cur: int):
        if cur != -1:
            self.events.curr_file_changed.emit(cur)
