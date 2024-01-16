from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from typing import Optional, Callable


class Drawable():
    def draw(self, painter: QPainter, img2viewport: Optional[Callable[[QPoint], QPoint]] = None):
        raise NotImplementedError
