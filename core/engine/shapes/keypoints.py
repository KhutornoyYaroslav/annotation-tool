from PyQt5.QtCore import QPoint, Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from typing import List, Dict, Tuple, Union, Optional, Callable
from core.engine.shapes.shapeinterface import ShapeInterface


class Keypoints(ShapeInterface):
    def __init__(self, nodes: List[str], edges: List[Tuple[int, int]]):
        assert len(nodes) != 0
        self._points = dict.fromkeys(nodes, None)
        self._cur_idx = 0
        self._edges = edges
        self.active = True

    def is_empty(self) -> bool:
        for pt in self._points:
            if pt is not None:
                return False

        return True

    def set_active(self, active: bool):
        self.active = active

    def get_points_list(self) -> List[str]:
        return list(self._points.keys())

    def get_points_info(self) -> List[Tuple[str, str]]:
        result = []
        for key, val in self._points.items():
            val_str = "none" if val is None else ", ".join([str(val.x()), str(val.y())])
            result.append((key, val_str))

        return result

    def get_current_point(self) -> Union[QPoint, None]:
        return list(self._points.values())[self._cur_idx]

    def set_current_point(self, pt: QPoint) -> bool:
        key = list(self._points.keys())[self._cur_idx]
        self._points[key] = pt

        return True

    def disable_current_point(self):
        key = list(self._points.keys())[self._cur_idx]
        self._points[key] = None

    def to_next_point(self):
        next_idx = self._cur_idx + 1
        if next_idx >= len(self._points):
            next_idx = 0
        self._cur_idx = next_idx

    def set_current_point_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self._points):
            self._cur_idx = idx
            return True

        return False

    def get_current_point_idx(self) -> int:
        return self._cur_idx

    def set_current_point_idx_by_position(self, pos: QPoint, max_radius: int = 8) -> bool:
        idx_best = None
        dist_best = max_radius

        for idx, pt in enumerate(self._points.values()):
            if pt is not None:
                delta = pt - pos
                dist = (delta.x() ** 2 + delta.y() ** 2) ** (1/2)
                if dist <= dist_best:
                    dist_best = dist
                    idx_best = idx

        if idx_best is not None:
            self._cur_idx = idx_best
            return True

        return False

    def get_bounding_rect(self) -> Union[QRect, None]:
        xs, ys = [], []
        for point in self._points.values():
            if point is not None:
                xs.append(point.x())
                ys.append(point.y())

        if not len(xs) or not len(ys):
            return None

        top_left = QPoint(min(xs), min(ys))
        bottom_right = QPoint(max(xs), max(ys))

        if bottom_right == top_left:
            bottom_right.setX(bottom_right.x() + 1)
            bottom_right.setY(bottom_right.y() + 1)

        return QRect(top_left, bottom_right)

    def serialize(self) -> Dict:
        points = {}
        for key, val in self._points.items():
            val_ = None if val is None else {'x': val.x(), 'y': val.y()}
            points[key] = val_

        data = {
            'type': self.__class__.__name__,
            'points': points
        }

        return data

    def deserialize(self, data: Dict):
        for key, val in data['points'].items():
            self._points[key] = None if val is None else QPoint(val['x'], val['y'])

        return self

    def on_left_mouse_clicked(self, pos: QPoint):
        self.set_current_point(pos)

    def on_right_mouse_clicked(self, pos: QPoint):
        self.set_current_point_idx_by_position(pos)

    def draw(self, painter: QPainter, img2viewport: Optional[Callable[[QPoint], QPoint]] = None):
        # Edges
        painter.setPen(QPen(QColor(0, 255, 0, 150), 1.0, Qt.DotLine))
        painter.setBrush(QColor(0, 0, 0, 0))

        pts = list(self._points.values())
        for edge in self._edges:
            pt1, pt2 = pts[edge[0]], pts[edge[1]]
            if pt1 is None or pt2 is None:
                continue

            beg = img2viewport(QPoint(pt1.x(), pt1.y()))
            end = img2viewport(QPoint(pt2.x(), pt2.y()))

            if beg is not None and end is not None:
                painter.drawLine(beg, end)

        # Nodes
        radius = 3.0 # radius = 0.0025 * np.linalg.norm(np.array(self.background.getViewport()[2:3]))
        painter.setPen(QPen(QColor(0, 255, 0, 150), 1.0))
        painter.setFont(QFont('Times', 2 * radius, QFont.Normal))
        painter.setBrush(QColor(0, 255, 0))

        for label, pt in self._points.items():
            if pt is None:
                continue
            pt_vport = img2viewport(QPoint(pt.x(), pt.y()))
            if pt_vport is not None:
                painter.drawEllipse(pt_vport, radius, radius)
                if label is not None:
                    painter.drawText(QPoint(pt_vport.x() + 2 * radius, pt_vport.y() - 2 * radius), str(label))

        if self.active:
            cur_pt = self.get_current_point()
            if cur_pt is not None:
                pt_vport = img2viewport(QPoint(cur_pt.x(), cur_pt.y()))
                if pt_vport is not None:
                    radius = 5
                    painter.setPen(QPen(QColor(255, 0, 0, 200), 2.0))
                    painter.drawArc(pt_vport.x() - radius, pt_vport.y() - radius, 2*radius, 2*radius, 0, 16 * 360)
