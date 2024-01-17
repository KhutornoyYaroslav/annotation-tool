from PyQt5.QtCore import QPoint


class Interactable():
    def on_left_mouse_clicked(self, pos: QPoint):
        raise NotImplementedError

    def on_right_mouse_clicked(self, pos: QPoint):
        raise NotImplementedError

    def on_left_mouse_doubleclicked(self, pos: QPoint):
        raise NotImplemented
