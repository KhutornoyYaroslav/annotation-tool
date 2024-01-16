from typing import List, Tuple
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from core.ui.graphics.drawable import Drawable
from core.ui.widgets import (
    MenuBar,
    StatusBar,
    FilesWidget,
    CanvasWidget,
    ObjectsWidget,
    KeypointsWidget
)


class ViewEvents(QObject):
    app_exit = pyqtSignal()
    files_open = pyqtSignal(list)
    files_close_all = pyqtSignal()
    files_current_changed = pyqtSignal(int)
    edit_undo = pyqtSignal()
    edit_redo = pyqtSignal()
    object_created = pyqtSignal()
    object_removed = pyqtSignal(int)
    object_current_changed = pyqtSignal(int)
    keypoint_current_changed = pyqtSignal(int)
    keypoint_disabled = pyqtSignal()
    canvas_mouse_left_clicked = pyqtSignal(tuple)
    canvas_mouse_right_clicked = pyqtSignal(tuple)


class View(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # Events
        self.events = ViewEvents()
        # Widgets
        self.menubar_widget = MenuBar(self)
        self.statusbar_widget = StatusBar(self)
        self.top_widget = QtWidgets.QWidget(self)
        self.top_layout = QtWidgets.QHBoxLayout(self.top_widget)
        self.canvas_widget = CanvasWidget(self.top_widget)
        self.tools_widget = QtWidgets.QWidget(self.top_widget)
        self.tools_layout = QtWidgets.QVBoxLayout(self.tools_widget)
        self.files_widget = FilesWidget(self.tools_widget)
        self.objects_widget = ObjectsWidget(self.tools_widget)
        self.keypoints_widget = KeypointsWidget(self.tools_widget)
        # Connect to widgets events
        self.menubar_widget.events.files_open.connect(self.on_menubar_files_changed)
        self.menubar_widget.events.files_close_all.connect(self.events.files_close_all.emit)
        self.menubar_widget.events.app_exit.connect(self.events.app_exit.emit)
        self.menubar_widget.events.undo.connect(self.events.edit_undo.emit)
        self.menubar_widget.events.redo.connect(self.events.edit_redo.emit)
        self.files_widget.events.curr_file_changed.connect(self.events.files_current_changed.emit)
        self.objects_widget.events.object_created.connect(self.events.object_created.emit)
        self.objects_widget.events.object_removed.connect(self.events.object_removed.emit)
        self.objects_widget.events.curr_object_changed.connect(self.events.object_current_changed.emit)
        self.keypoints_widget.events.curr_keypoint_changed.connect(self.events.keypoint_current_changed.emit)
        self.keypoints_widget.events.keypoint_disabled.connect(self.events.keypoint_disabled.emit)
        self.canvas_widget.events.mouse_left_clicked.connect(self.events.canvas_mouse_left_clicked.emit)
        self.canvas_widget.events.mouse_right_clicked.connect(self.events.canvas_mouse_right_clicked.emit)

    def initGUI(self):
        self.setWindowTitle('Annotation tool')
        # Menu bar widget
        self.setMenuBar(self.menubar_widget)
        self.menubar_widget.initGUI()
        # Create status bar
        self.setStatusBar(self.statusbar_widget)
        self.statusbar_widget.initGUI()
        # Canvas widget
        self.setCentralWidget(self.top_widget)
        self.top_widget.setLayout(self.top_layout)
        self.top_layout.addWidget(self.canvas_widget)
        self.canvas_widget.setMinimumSize(512, 512)
        # Tools area widgets
        self.top_layout.addWidget(self.tools_widget)
        self.tools_widget.setLayout(self.tools_layout)
        self.tools_widget.setMaximumWidth(256)
        self.tools_layout.addWidget(self.files_widget)
        self.files_widget.initGUI()
        self.tools_layout.addWidget(self.objects_widget)
        self.objects_widget.initGUI()
        self.tools_layout.addWidget(self.keypoints_widget)
        self.keypoints_widget.initGUI()

    def on_menubar_files_changed(self, files: List[str]):
        self.events.files_open.emit(files)

    def set_files_list(self, fnames: List[str]):
        self.files_widget.set_files(fnames)

    def set_objects_list(self, objects: List[str]):
        self.objects_widget.set_objects(objects)

    def set_keypoints_list(self, keypoints: List[str]):
        self.keypoints_widget.set_keypoints(keypoints)

    def set_curent_keypoint(self, idx: int):
        self.keypoints_widget.set_current_row(idx)

    def set_background_image(self, fname: str): # TODO: rename to 'set_canvas_image' ?
        self.canvas_widget.set_background_image(fname)

    def clear_background(self): # TODO: rename 'canvas'
        self.canvas_widget.clear()

    def repaint_background(self): # TODO: rename 'canvas'
        self.canvas_widget.repaint()

    def set_drawables(self, items: List[Drawable]):
        self.canvas_widget.set_drawables(items)
