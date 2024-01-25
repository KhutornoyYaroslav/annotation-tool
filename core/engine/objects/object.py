import cv2 as cv
import numpy as np
from uuid import UUID, uuid4
from PyQt5.QtCore import QRect, QPoint
from typing import List, Dict, Tuple, Optional, Union
from core.utils.serializable import Serializable
from core.engine.shapes import ShapeInterface, ShapeType, create_shape, Keypoints, BoundingRect
from core.utils.yolo_predict import detect_cars


class Object(Serializable):
    def __init__(self, shapes: List[ShapeInterface], class_name: str, uuid: Optional[UUID] = None):
        assert len(shapes) != 0
        self._shapes = shapes
        self._cur_shape_idx = 0
        self._class_name = class_name
        self._uuid = uuid4() if uuid is None else uuid

    def is_empty(self):
        for shape in self._shapes:
            if shape.is_empty():
                return True

        return False

    def get_current_shape(self) -> ShapeInterface:
        return self._shapes[self._cur_shape_idx]

    def set_current_shape_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self._shapes):
            self._cur_shape_idx = idx
            return True

        return False

    def get_current_shape_idx(self) -> int:
        return self._cur_shape_idx

    def get_shapes(self) -> List[ShapeInterface]:
        return self._shapes

    def get_info(self) -> str:
        return self._class_name + " [" + str(self._uuid) + "]"

    def get_shapes_info(self) -> List[Tuple[str, List[Tuple[str, str]]]]:
        result = []
        for shape in self._shapes:
            result.append((shape.__class__.__name__, shape.get_points_info()))

        return result
    
    def get_shapes_bounding_rect(self) -> Union[QRect, None]:
        res = None
        for shape in self._shapes:
            br = shape.get_bounding_rect()
            if br is not None:
                if res is None:
                    res = br
                else:
                    if br.width() * br.height() > res.width() * res.height():
                        res = br

        return res

    def annotate_brect(self, img: np.ndarray) -> bool:
        if img is None or not img.size:
            return False

        h, w = img.shape[0:2]

        kp_brect = None
        for shape in self._shapes:
            if isinstance(shape, Keypoints):
                kp_brect = shape.get_bounding_rect()
                break
        
        if kp_brect is None:
            return False

        # Expand Keypoints brect
        k = 2.0
        roi_w = int(k * kp_brect.width())
        roi_h = int(k * kp_brect.height())
        roi_x = int(kp_brect.x() + (kp_brect.width() - roi_w) / 2)
        roi_y = int(kp_brect.y() + (kp_brect.height() - roi_h) / 2)

        # Clip ROI
        roi_x = np.clip(roi_x, 0, w)
        roi_y = np.clip(roi_y, 0, h)
        roi_w = np.clip(roi_w, 0, w - roi_x)
        roi_h = np.clip(roi_h, 0, h - roi_y)

        if roi_w == 0 or roi_h == 0:
            return False
    
        img_roi = img[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

        # Detect by YOLO
        rects = detect_cars(img_roi, device='cpu')
        for r in rects:
            r[0::2] += roi_x
            r[1::2] += roi_y
            # cv.rectangle(img_roi, r[0:2], r[2:4], (0, 255, 0), 1)
        
        best_r = None
        max_area = None
        for r in rects:
            det_brect = QRect(QPoint(*r[0:2]), QPoint(*r[2:4]))
            inter_brect = kp_brect.intersected(det_brect)
            inter_area = inter_brect.width() * inter_brect.height()
            if best_r is None:
                best_r = det_brect
                max_area = inter_area
            else:
                if inter_area > max_area:
                    best_r = det_brect
                    max_area = inter_area

        if best_r is not None:
            # Add padding
            padding = 1
            best_r = best_r.united(kp_brect)
            best_r.setLeft(np.clip(0, best_r.left() - padding, w))
            # best_r.setTop(np.clip(0, best_r.top() - padding, h))
            best_r.setRight(np.clip(0, best_r.right() + padding, w))
            # best_r.setBottom(np.clip(0, best_r.bottom() + padding, h))

            # Set result brect
            for shape in self._shapes:
                if isinstance(shape, BoundingRect):
                    shape._points["top-left"] = best_r.topLeft()
                    shape._points["bottom-right"] = best_r.bottomRight()
                    return True

        return False

    def serialize(self) -> Dict:
        data = {
            'class': self._class_name,
            'uuid': str(self._uuid),
            'shapes': [s.serialize() for s in self._shapes]
        }

        return data

    def deserialize(self, data: Dict):
        self._uuid = UUID(data['uuid'])

        self._shapes.clear() # TODO: check it
        for shape_data in data['shapes']:
            shape = create_shape(ShapeType.from_str(shape_data['type']))
            assert shape is not None
            self._shapes.append(shape.deserialize(shape_data))

        return self
