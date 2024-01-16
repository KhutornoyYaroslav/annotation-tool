from PyQt5 import QtWidgets


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent):
        QtWidgets.QStatusBar.__init__(self, parent)

    def initGUI(self):
        self.showMessage('')
