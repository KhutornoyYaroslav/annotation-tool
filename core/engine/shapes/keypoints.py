from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from typing import List, Tuple, Union, Optional, Callable
from core.engine.shapes.shapeinterface import ShapeInterface


class Keypoints(ShapeInterface):
    def __init__(self, nodes: List[str], edges: List[Tuple[int, int]]):
        assert len(nodes) != 0
        self._keypoints = dict.fromkeys(nodes, None)
        self._cur_idx = 0
        self._edges = edges

    def is_empty(self) -> bool:
        for pt in self._keypoints:
            if pt is not None:
                return False

        return True

    def get_points_list(self) -> List[str]:
        return list(self._keypoints.keys())

    def get_current_keypoint(self) -> Union[QPoint, None]:
        if not self.keypoints:
            return None

        return list(self._keypoints.values())[self._cur_idx]

    def set_current_keypoint(self, pt: QPoint) -> bool:
        key = list(self._keypoints.keys())[self._cur_idx]
        self._keypoints[key] = pt

        return True

    def disable_current_keypoint(self):
        key = list(self._keypoints.keys())[self._cur_idx]
        self._keypoints[key] = None

    def set_current_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self._keypoints):
            self._cur_idx = idx
            return True

        return False

    def set_current_idx_by_position(self, pos: QPoint, max_radius: int = 8) -> bool:
        idx_best = None
        dist_best = max_radius

        for idx, pt in enumerate(self._keypoints.values()):
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
        self.set_current_keypoint(pos)

    def on_right_mouse_clicked(self, pos: QPoint):
        self.set_current_idx_by_position(pos)

    def draw(self, painter: QPainter, img2viewport: Optional[Callable[[QPoint], QPoint]] = None):
        # Edges
        painter.setPen(QPen(QColor(0, 255, 0), 1.0, Qt.DotLine))

        pts = list(self._keypoints.values())
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
        painter.setPen(QPen(QColor(0, 255, 0, 100), 1.0))
        painter.setFont(QFont('Times', 2 * radius, QFont.Normal))
        painter.setBrush(QColor(255, 0, 0))

        for label, pt in self._keypoints.items():
            if pt is None:
                continue
            pt_vport = img2viewport(QPoint(pt.x(), pt.y()))
            if pt_vport is not None:
                painter.drawEllipse(pt_vport, radius, radius)
                if label is not None:
                    painter.drawText(QPoint(pt_vport.x() + 2 * radius, pt_vport.y() - 2 * radius), str(label))

        cur_pt = self.get_current_keypoint()
        if cur_pt is not None:
            pt_vport = img2viewport(QPoint(cur_pt.x(), cur_pt.y()))
            if pt_vport is not None:
                painter.setBrush(QColor(0, 0, 255))
                painter.drawEllipse(pt_vport, radius, radius)
