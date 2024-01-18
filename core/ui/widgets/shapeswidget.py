from typing import List, Dict, Tuple
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt


class ShapesWidgetEvents(QObject):
    current_point_changed = pyqtSignal(int)
    # keypoint_disabled = pyqtSignal()


class ShapesWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        # Events
        self.events = ShapesWidgetEvents(self)
        # Widgets
        self.top_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.tree_widget = QtWidgets.QTreeWidget(self)
        # self.button_disable = QtWidgets.QPushButton(self)
        self.shortcut_delete = QtWidgets.QShortcut(QtGui.QKeySequence.Delete, self)

    def initGUI(self):
        self.setTitle("Object data")
        self.setLayout(self.top_layout)

        # Top layout
        self.top_layout.addWidget(self.tree_widget)
        self.top_layout.addLayout(self.buttons_layout)

        # Tree
        self.tree_widget.setColumnCount(3)
        self.tree_widget.setHeaderLabels(['Shape', 'Point', 'Value'])
        self.tree_widget.currentItemChanged.connect(self.on_current_item_changed)

        # Buttons layout
        # self.buttons_layout.addWidget(self.button_disable)

        # Buttons
        # self.button_disable.setText("Disable") # TODO: сделать невозможным нажимать кнопку, если точка и так disable
        # self.button_disable.clicked.connect(self.events.keypoint_disabled.emit)

        # Shortcuts
        # self.shortcut_delete.activated.connect(self.events.keypoint_disabled.emit)

    def on_current_item_changed(self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
        if current is not None: # TODO: ?
            print('cur item changed: ',previous, current)

    def set_shapes(self, shapes: List[Tuple[str, List[Tuple[str, str]]]]):
        self.tree_widget.clear()

        first_selected = False
        for shape in shapes:
            shape_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
            shape_item.setText(0, shape[0])
            shape_item.setDisabled(True)

            for label, value in shape[1]:
                data_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
                data_item.setText(1, label)
                data_item.setText(2, value)

                if not first_selected:
                    self.tree_widget.setCurrentItem(data_item)
                    first_selected = True
                
                shape_item.addChild(data_item)

    # def set_current_row(self, cur: int):
    #     self.list_widget.currentRowChanged.disconnect(self.on_current_row_changed)
    #     self.list_widget.setCurrentRow(cur)
    #     self.list_widget.currentRowChanged.connect(self.on_current_row_changed)

    # def on_current_row_changed(self, cur: int):
    #     if cur != -1:
    #         print('ON CUR ROW CHANGED: ', cur)
    #         self.events.curr_keypoint_changed.emit(cur)
