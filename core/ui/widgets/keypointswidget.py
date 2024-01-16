from typing import List
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject


class KeypointsWidgetEvents(QObject):
    curr_keypoint_changed = pyqtSignal(int)
    keypoint_disabled = pyqtSignal()


class KeypointsWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        # Events
        self.events = KeypointsWidgetEvents(self)
        # Widgets
        self.top_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.list_widget = QtWidgets.QListWidget(self)
        # self.button_disable = QtWidgets.QPushButton(self)
        self.shortcut_delete = QtWidgets.QShortcut(QtGui.QKeySequence.Delete, self)

    def initGUI(self):
        self.setTitle("Keypoints")
        self.setLayout(self.top_layout)

        # Top layout
        self.top_layout.addWidget(self.list_widget)
        self.top_layout.addLayout(self.buttons_layout)

        # List
        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

        # Buttons layout
        # self.buttons_layout.addWidget(self.button_disable)

        # Buttons
        # self.button_disable.setText("Disable") # TODO: сделать невозможным нажимать кнопку, если точка и так disable
        # self.button_disable.clicked.connect(self.events.keypoint_disabled.emit)

        # Shortcuts
        self.shortcut_delete.activated.connect(self.events.keypoint_disabled.emit)

    def set_keypoints(self, keypoints: List[str]): # TODO: provide current row
        self.list_widget.clear()
        for kpt in keypoints:
            self.list_widget.addItem(kpt)
        # if self.list_widget.count() > 0:
            # self.list_widget.setCurrentRow(0)
            # self.set_current_row(0)

    def set_current_row(self, cur: int):
        self.list_widget.currentRowChanged.disconnect(self.on_current_row_changed)
        self.list_widget.setCurrentRow(cur)
        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

    def on_current_row_changed(self, cur: int):
        if cur != -1:
            print('ON CUR ROW CHANGED: ', cur)
            self.events.curr_keypoint_changed.emit(cur)
