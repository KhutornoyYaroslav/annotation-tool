from typing import List
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from core.ui.dialogs.newobject import NewObjectDialog


class ObjectsWidgetEvents(QObject):
    object_created = pyqtSignal(int)
    object_removed = pyqtSignal(int)
    current_object_changed = pyqtSignal(int)
    draw_all_changed = pyqtSignal(bool)
    autofocus_changed = pyqtSignal(bool)


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
        self.checkbox_draw_all = QtWidgets.QCheckBox(self)
        self.checkbox_autofocus = QtWidgets.QCheckBox(self)

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
        self.buttons_layout.addWidget(self.checkbox_draw_all)
        self.buttons_layout.addWidget(self.checkbox_autofocus)

        # Buttons
        self.button_create.setText("New...")
        self.button_create.clicked.connect(self.on_object_new)

        self.button_remove.setText("Remove")
        self.button_remove.clicked.connect(self.on_object_removed)

        self.checkbox_draw_all.setText("Draw all")
        self.checkbox_draw_all.stateChanged.connect(self.on_checkbox_state_changed)

        self.checkbox_autofocus.setText("Focus on")
        self.checkbox_autofocus.stateChanged.connect(self.on_autofocus_state_changed)

    def set_objects(self, objects: List[str], current_object: int):
        self.list_widget.clear()
        for obj in objects:
            self.list_widget.addItem(obj)
        if self.list_widget.count() > 0:
            self.list_widget.currentRowChanged.disconnect(self.on_current_row_changed)
            self.list_widget.setCurrentRow(current_object)
            self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

    def set_object_classes(self, classes: List[str]):
        self._obj_classes = classes

    def on_object_removed(self):
        curr_idx = self.list_widget.currentRow()
        if curr_idx >= 0:
            self.events.object_removed.emit(curr_idx)

    def on_current_row_changed(self, cur: int):
        if cur != -1:
            self.events.current_object_changed.emit(cur)

    def on_object_new(self):
        dialog = NewObjectDialog(self)
        dialog.initGUI()
        dialog.set_object_classes(self._obj_classes)

        if dialog.exec():
            class_idx = dialog.get_current_row()
            if class_idx != -1:
                self.events.object_created.emit(class_idx)

    def on_checkbox_state_changed(self, state: int):
        self.events.draw_all_changed.emit(state == Qt.CheckState.Checked)

    def on_autofocus_state_changed(self, state: int):
        self.events.autofocus_changed.emit(state == Qt.CheckState.Checked)