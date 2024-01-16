import os
import glob
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject


class MenuBarEvents(QObject):
    app_exit = pyqtSignal()
    files_open = pyqtSignal(list)
    files_close_all = pyqtSignal()
    undo = pyqtSignal()
    redo = pyqtSignal()


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent):
        QtWidgets.QMenuBar.__init__(self, parent)
        # Events
        self.events = MenuBarEvents()
        # File
        self.menu_file = QtWidgets.QMenu(self)
        self.file_dialog = QtWidgets.QFileDialog(self)
        self.action_file_open_file = QtWidgets.QAction(self)
        self.action_file_open_folder = QtWidgets.QAction(self)
        self.action_file_exit = QtWidgets.QAction(self)
        self.action_file_close_all = QtWidgets.QAction(self)
        # Edit
        self.menu_edit = QtWidgets.QMenu(self)
        self.action_edit_undo = QtWidgets.QAction(self)
        self.action_edit_redo = QtWidgets.QAction(self)

    def initGUI(self):
        self.setObjectName("menuBar")
        self.setGeometry(QtCore.QRect(0, 0, self.parentWidget().size().width(), 32))
        self.addAction(self.menu_file.menuAction())
        self.addAction(self.menu_edit.menuAction())

        # File
        self.menu_file.setObjectName("menuFile")
        self.menu_file.setTitle("File")
        self.menu_file.addAction(self.action_file_open_file)
        self.menu_file.addAction(self.action_file_open_folder)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_file_close_all)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_file_exit)

        # File -> Open file...
        self.action_file_open_file.setText("Open file...")
        self.action_file_open_file.triggered.connect(self.on_open_file)

        # File -> Open folder...
        self.action_file_open_folder.setText("Open folder...")
        self.action_file_open_folder.triggered.connect(self.on_open_folder)

        # File -> Close all
        self.action_file_close_all.setText("Close all")
        self.action_file_close_all.triggered.connect(self.events.files_close_all.emit)

        # File -> Exit
        self.action_file_exit.setText("Exit")
        self.action_file_exit.setShortcut("Ctrl+Q")
        self.action_file_exit.triggered.connect(self.events.app_exit.emit)

        # Edit
        self.menu_edit.setTitle("Edit")
        self.menu_edit.addAction(self.action_edit_undo)
        self.menu_edit.addAction(self.action_edit_redo)

        # Edit -> Undo
        self.action_edit_undo.setText("Undo")
        self.action_edit_undo.setShortcut("Ctrl+Z")
        self.action_edit_undo.triggered.connect(self.events.undo.emit)

        # Edit -> Redo
        self.action_edit_redo.setText("Redo")
        self.action_edit_redo.setShortcut("Ctrl+Y")
        self.action_edit_redo.triggered.connect(self.events.redo.emit)

    def on_open_folder(self):
        files = []
        root_dir = self.file_dialog.getExistingDirectory(self)
        if root_dir:
            files = glob.glob(os.path.join(root_dir, '*'), recursive=True)
            files = sorted(files)
        if files:
            self.events.files_open.emit(files)

    def on_open_file(self):
        files = []
        file, _ = self.file_dialog.getOpenFileName(self)
        if file:
            files.append(file)
        if files:
            self.events.files_open.emit(files)
