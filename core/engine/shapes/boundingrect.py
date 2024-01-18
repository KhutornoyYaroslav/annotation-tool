from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from typing import List, Tuple, Union, Optional, Callable
from core.engine.shapes.shapeinterface import ShapeInterface


class BoundingRect(ShapeInterface):
    def __init__(self):
        self._points = dict.fromkeys({"top-left", "bottom-right"}, None)
        self._cur_idx = 0

    def is_empty(self) -> bool:
        for pt in self._points:
            if pt is None:
                return True

        return False

    def get_points_list(self) -> List[str]:
        return list(self._points.keys())
    
    def get_points_info(self) -> List[Tuple[str, str]]:
        result = []
        for key, val in self._points.items():
            val_str = "none" if val is None else ", ".join([val.x(), val.y()])
            result.append((key, val_str))

        return result

    def get_current_point(self) -> Union[QPoint, None]:
        if not self._points:
            return None

        return list(self._points.values())[self._cur_idx]

    def set_current_point(self, pt: QPoint) -> bool:
        key = list(self._points.keys())[self._cur_idx]
        second_pt = list(self._points.values())[1 - self._cur_idx]

        if second_pt is None:
            self._points[key] = pt
            return True
        else:
            if key == "top-left":
                if pt.x() < second_pt.x() and pt.y() < second_pt.y():
                    self._points[key] = pt
                    return True
            else:
                if pt.x() > second_pt.x() and pt.y() > second_pt.y():
                    self._points[key] = pt
                    return True

        return False

    def set_current_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self._points):
            self._cur_idx = idx
            return True

        return False

    def set_current_idx_by_position(self, pos: QPoint, max_radius: int = 8) -> bool:
        idx_best = None
        dist_best = max_radius

        for idx, pt in enumerate(self._points.values()):
            if pt is not None:
                dist = QPoint.dotProduct(pt, pos) ** (1/2)
                if dist <= dist_best:
                    dist_best = dist
                    idx_best = idx

        if idx_best is not None:
            self._cur_idx = idx_best
            return True

        return False

    # TODO: implement
    # def serialize(self) -> Dict:
    #     return super().serialize()

    # TODO: implement
    # def deserialize(self, data: Dict):
    #     return super().deserialize(data)

    def on_left_mouse_clicked(self, pos: QPoint):
        self.set_current_point(pos)

    def on_right_mouse_clicked(self, pos: QPoint):
        self.set_current_idx_by_position(pos)

    def draw(self, painter: QPainter, img2viewport: Optional[Callable[[QPoint], QPoint]] = None):
        # Edges
        painter.setPen(QPen(QColor(0, 255, 0), 1.0, Qt.DotLine))

        if not None in self._points.values():
            tl = self._points["top-left"]
            br = self._points["bottom-right"]

            tl_vp = img2viewport(tl)
            br_vp = img2viewport(br)
            if tl_vp is not None and br_vp is not None:
                painter.drawRect(tl_vp.x(), tl_vp.y(), br_vp.x() - tl_vp.x(), br_vp.y() - tl_vp.y())

        # Points
        radius = 5.0 # radius = 0.0025 * np.linalg.norm(np.array(self.background.getViewport()[2:3]))
        painter.setPen(QPen(QColor(0, 255, 0, 100), 1.0))
        painter.setFont(QFont('Times', 2 * radius, QFont.Normal))
        painter.setBrush(QColor(255, 0, 0))

        for label, pt in self._points.items():
            if pt is None:
                continue
            pt_vport = img2viewport(pt)
            if pt_vport is not None:
                painter.drawEllipse(pt_vport, radius, radius)
                if label is not None:
                    painter.drawText(QPoint(pt_vport.x() + 2 * radius, pt_vport.y() - 2 * radius), str(label))

        cur_pt = self.get_current_point()
        if cur_pt is not None:
            pt_vport = img2viewport(cur_pt)
            if pt_vport is not None:
                painter.setBrush(QColor(0, 0, 255))
                painter.drawEllipse(pt_vport, radius, radius)
