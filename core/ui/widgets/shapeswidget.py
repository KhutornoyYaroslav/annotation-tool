from typing import List, Tuple, Optional
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QKeyEvent, QMouseEvent


class TreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super(TreeWidget, self).__init__(parent)

    def mousePressEvent(self, event: Optional[QMouseEvent]) -> None:
        if self.indexAt(event.pos()).flags() & Qt.ItemFlag.ItemIsSelectable:
            return super().mousePressEvent(event)

        return None

    def mouseDoubleClickEvent(self, event: Optional[QMouseEvent]) -> None:
        if self.indexAt(event.pos()).flags() & Qt.ItemFlag.ItemIsSelectable:
            return super().mouseDoubleClickEvent(event)

        return None

    def keyPressEvent(self, event: Optional[QKeyEvent]) -> None:
        current = self.currentItem()
        if current is None:
            return super().keyPressEvent(event)

        toplevel = current.parent()
        if toplevel is None:
            return None

        if event.key() == Qt.Key.Key_Down:
            if toplevel.indexOfChild(current) + 1 < toplevel.childCount():
                return super().keyPressEvent(event)

        if event.key() == Qt.Key.Key_Up:
            if toplevel.indexOfChild(current) > 0:
                return super().keyPressEvent(event)

        return None


class ShapesWidgetEvents(QObject):
    current_item_changed = pyqtSignal(int, int) # Shape idx, point idx
    current_item_disabled = pyqtSignal()
    next_item_requested = pyqtSignal()


class ShapesWidget(QtWidgets.QGroupBox):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        # Events
        self.events = ShapesWidgetEvents(self)
        # Widgets
        self.top_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.tree_widget = TreeWidget(self)
        self.shortcut_delete = QtWidgets.QShortcut(QtGui.QKeySequence.Delete, self)
        self.shortcut_space = QtWidgets.QShortcut(Qt.Key_Space, self)

    def initGUI(self):
        self.setTitle("Object data")
        self.setLayout(self.top_layout)

        # Top layout
        self.top_layout.addWidget(self.tree_widget)
        self.top_layout.addLayout(self.buttons_layout)

        # Tree
        self.tree_widget.setColumnCount(3)
        self.tree_widget.setHeaderLabels(['Shape', 'Point', 'Value'])
        self.tree_widget.setItemsExpandable(False)
        self.tree_widget.setRootIsDecorated(False)
        self.tree_widget.currentItemChanged.connect(self.on_current_item_changed)

        # Shortcuts
        self.shortcut_space.activated.connect(self.events.next_item_requested)
        self.shortcut_delete.activated.connect(self.events.current_item_disabled)

    def on_current_item_changed(self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
        if current is not None:
            toplevel = current.parent()
            if toplevel is not None:
                shape_idx = self.tree_widget.indexOfTopLevelItem(toplevel)
                point_idx = toplevel.indexOfChild(current)
                self.events.current_item_changed.emit(shape_idx, point_idx)

    def set_shapes(self, shapes: List[Tuple[str, List[Tuple[str, str]]]], current_shape: int = 0, current_point: int = 0):
        self.tree_widget.clear()

        for shape_idx, shape in enumerate(shapes):
            shape_item = QtWidgets.QTreeWidgetItem(self.tree_widget)
            shape_item.setText(0, shape[0])
            shape_item.setFlags(shape_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            shape_item.setExpanded(True)

            for point_idx, (label, value) in enumerate(shape[1]):
                data_item = QtWidgets.QTreeWidgetItem(shape_item)
                data_item.setText(1, label)
                data_item.setText(2, value)
                shape_item.addChild(data_item)

                if shape_idx == current_shape and point_idx == current_point:
                    self.tree_widget.setCurrentItem(data_item)

    def set_current_item(self, shape_idx: int, point_idx: int):
        shape_item = self.tree_widget.topLevelItem(shape_idx)
        if shape_item is not None:
            item = shape_item.child(point_idx)
            if item is not None:
                self.tree_widget.currentItemChanged.disconnect(self.on_current_item_changed)
                self.tree_widget.setCurrentItem(item)
                self.tree_widget.currentItemChanged.connect(self.on_current_item_changed)
