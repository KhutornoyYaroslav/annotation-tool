from typing import List, Tuple
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from core.utils.drawable import QtDrawable
from core.utils.basicconfig import Config
from core.ui.widgets import (
    MenuBar,
    StatusBar,
    FilesWidget,
    CanvasWidget,
    ObjectsWidget,
    ShapesWidget
)


class ViewEvents(QObject):
    app_exit = pyqtSignal()
    files_open = pyqtSignal(list)
    files_close_all = pyqtSignal()
    files_current_changed = pyqtSignal(int)
    edit_undo = pyqtSignal()
    edit_redo = pyqtSignal()
    object_created = pyqtSignal(int)
    object_removed = pyqtSignal(int)
    object_current_changed = pyqtSignal(int)
    shapes_current_item_changed = pyqtSignal(int, int)
    # keypoint_disabled = pyqtSignal()
    canvas_mouse_left_clicked = pyqtSignal(tuple)
    canvas_mouse_right_clicked = pyqtSignal(tuple)


class View(QtWidgets.QMainWindow):
    def __init__(self, cfg: Config):
        QtWidgets.QMainWindow.__init__(self)
        self._cfg = cfg
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
        self.shapes_widget = ShapesWidget(self.tools_widget)
        # Connect to widgets events
        self.menubar_widget.events.files_open.connect(self.events.files_open.emit)
        self.menubar_widget.events.files_close_all.connect(self.events.files_close_all.emit)
        self.menubar_widget.events.app_exit.connect(self.events.app_exit.emit)
        self.menubar_widget.events.undo.connect(self.events.edit_undo.emit)
        self.menubar_widget.events.redo.connect(self.events.edit_redo.emit)
        self.files_widget.events.curr_file_changed.connect(self.events.files_current_changed.emit)
        self.objects_widget.events.object_created.connect(self.events.object_created.emit)
        self.objects_widget.events.object_removed.connect(self.events.object_removed.emit)
        self.objects_widget.events.current_object_changed.connect(self.events.object_current_changed.emit)
        # self.keypoints_widget.events.keypoint_disabled.connect(self.events.keypoint_disabled.emit)
        self.shapes_widget.events.current_item_changed.connect(self.events.shapes_current_item_changed.emit)
        self.canvas_widget.events.mouse_left_clicked.connect(self.events.canvas_mouse_left_clicked.emit)
        self.canvas_widget.events.mouse_right_clicked.connect(self.events.canvas_mouse_right_clicked.emit)

        self._initialize()

    def _initialize(self):
        self.canvas_widget.set_zoom_factor(self._cfg.control.zoom_factor)

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
        # self.canvas_widget.setMinimumSize(512, 512)
        # Tools area widgets
        self.top_layout.addWidget(self.tools_widget)
        self.tools_widget.setLayout(self.tools_layout)
        self.tools_widget.setMaximumWidth(360)
        self.tools_layout.addWidget(self.files_widget)
        self.files_widget.initGUI()
        self.tools_layout.addWidget(self.objects_widget)
        self.objects_widget.initGUI()
        self.tools_layout.addWidget(self.shapes_widget)
        self.shapes_widget.initGUI()
        # Set app window size
        self.resize(self._cfg.view.appearance.wndsize[0], self._cfg.view.appearance.wndsize[1])
        if self._cfg.view.appearance.maximized:
            self.showMaximized()
        if self._cfg.view.appearance.fullscreen:
            self.showFullScreen()

    def set_files_list(self, fnames: List[str]):
        self.files_widget.set_files(fnames)

    def set_objects_list(self, objects: List[str], current_object: int = 0):
        self.objects_widget.set_objects(objects, current_object)

    def set_object_classes(self, classes: List[str]):
        self.objects_widget.set_object_classes(classes)

    def set_object_shapes(self, data: List[Tuple[str, List[Tuple[str, str]]]], current_shape: int = 0, current_point: int = 0):
        self.shapes_widget.set_shapes(data, current_shape, current_point)

    def set_shapes_curent_item(self, shape_idx: int, point_idx: int):
        self.shapes_widget.set_current_item(shape_idx, point_idx)

    def set_canvas_image(self, fname: str) -> bool:
        return self.canvas_widget.set_canvas_image(fname)

    def clear_canvas(self):
        self.canvas_widget.clear()

    def repaint_canvas(self):
        self.canvas_widget.repaint()

    def set_drawables(self, items: List[QtDrawable]):
        self.canvas_widget.set_drawables(items)
