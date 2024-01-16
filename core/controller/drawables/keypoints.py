from typing import Optional, Callable
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from core.ui.graphics.drawable import Drawable
from core.engine.shape.keypoints import Keypoints


class DrawKeypoints(Drawable):
    def __init__(self, shape: Keypoints):
        self.shape = shape

    def draw(self, painter: QPainter, img2viewport: Optional[Callable[[QPoint], QPoint]] = None):
        # Draw edges
        painter.setPen(QPen(QColor(0, 255, 0), 1.0, Qt.DotLine))

        pts = list(self.shape.keypoints.values())
        for edge in self.shape.edges:
            pt1, pt2 = pts[edge[0]], pts[edge[1]]
            if pt1.is_empty() or pt2.is_empty():
                continue

            beg = img2viewport(QPoint(pt1.x, pt1.y))
            end = img2viewport(QPoint(pt2.x, pt2.y))

            if beg is not None and end is not None:
                painter.drawLine(beg, end)

        # Draw nodes
        radius = 3.0 # radius = 0.0025 * np.linalg.norm(np.array(self.background.getViewport()[2:3]))
        painter.setPen(QPen(QColor(0, 255, 0, 100), 1.0))
        painter.setFont(QFont('Times', 2 * radius, QFont.Normal))
        painter.setBrush(QColor(255, 0, 0))

        for label, pt in self.shape.keypoints.items():
            if pt.is_empty():
                continue
            pt_vport = img2viewport(QPoint(pt.x, pt.y))
            if pt_vport is not None:
                painter.drawEllipse(pt_vport, radius, radius)
                if label is not None:
                    painter.drawText(QPoint(pt_vport.x() + 2 * radius, pt_vport.y() - 2 * radius), str(label))

        cur_pt = self.shape.get_current_keypoint()
        if not cur_pt.is_empty():
            pt_vport = img2viewport(QPoint(cur_pt.x, cur_pt.y))
            if pt_vport is not None:
                painter.setBrush(QColor(0, 0, 255))
                painter.drawEllipse(pt_vport, radius, radius)
