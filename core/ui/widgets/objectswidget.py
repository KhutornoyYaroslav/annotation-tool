from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from core.ui.dialogs.newobject import NewObjectDialog


class ObjectsWidgetEvents(QObject):
    object_created = pyqtSignal(int)
    object_removed = pyqtSignal(int)
    curr_object_changed = pyqtSignal(int)


class ObjectsWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self._obj_classes = []
        # Events
        self.events = ObjectsWidgetEvents(self)
        # Widgets
        self.top_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.list_widget = QtWidgets.QListWidget(self)
        self.button_create = QtWidgets.QPushButton(self)
        self.button_remove = QtWidgets.QPushButton(self)

    def initGUI(self):
        self.setTitle("Objects")
        self.setLayout(self.top_layout)

        # Top layout
        self.top_layout.addWidget(self.list_widget)
        self.top_layout.addLayout(self.buttons_layout)

        # List
        self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

        # Buttons layout
        self.buttons_layout.addWidget(self.button_create)
        self.buttons_layout.addWidget(self.button_remove)

        # Buttons
        self.button_create.setText("New...")
        self.button_create.clicked.connect(self.on_object_new)

        self.button_remove.setText("Remove")
        self.button_remove.clicked.connect(self.on_object_removed)

    def set_objects(self, objects: List[str]):
        self.list_widget.clear()
        for obj in objects:
            self.list_widget.addItem(obj)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def set_object_classes(self, classes: List[str]):
        self._obj_classes = classes

    def on_object_removed(self):
        curr_idx = self.list_widget.currentRow()
        if curr_idx >= 0:
            self.events.object_removed.emit(curr_idx)

    def on_current_row_changed(self, cur: int):
        if cur != -1:
            self.events.curr_object_changed.emit(cur)

    def on_object_new(self):
        dialog = NewObjectDialog(self)
        dialog.initGUI()
        dialog.set_object_classes(self._obj_classes)

        if dialog.exec():
            class_idx = dialog.get_current_row()
            if class_idx != -1:
                self.events.object_created.emit(class_idx)
