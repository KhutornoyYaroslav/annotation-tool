from typing import List
from PyQt5 import QtWidgets


class NewObjectDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(NewObjectDialog, self).__init__(parent)
        # Widgets
        self.top_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.list_widget = QtWidgets.QListWidget(self)
        self.button_ok = QtWidgets.QPushButton(self)
        self.button_cancel = QtWidgets.QPushButton(self)

    def initGUI(self):
        self.setWindowTitle("Choose object class")
        self.setLayout(self.top_layout)

        # Top layout
        self.top_layout.addWidget(self.list_widget)
        self.top_layout.addLayout(self.buttons_layout)

        # Buttons layout
        self.buttons_layout.addWidget(self.button_ok)
        self.buttons_layout.addWidget(self.button_cancel)

        # Buttons
        self.button_ok.setText("Ok")
        self.button_ok.clicked.connect(self.accept)

        self.button_cancel.setText("Cancel")
        self.button_cancel.clicked.connect(self.reject)

    def set_object_classes(self, classes: List[str]):
        self.list_widget.clear()
        for c in classes:
            self.list_widget.addItem(c)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def get_current_row(self) -> int:
        return self.list_widget.currentRow()
