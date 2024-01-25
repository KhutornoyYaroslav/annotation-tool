import cv2 as cv
import numpy as np
from typing import Tuple


class PanAndZoom:
    def __init__(self):
        self.img = None
        self.roi = (0, 0, 0, 0)

    def clear(self):
        self.img = None
        self.roi = (0, 0, 0, 0)

    def is_empty(self):
        return self.img is None or self.img.size == 0

    def load_image(self, path: str) -> bool:
        img_ = cv.imread(path, cv.IMREAD_COLOR)
        if img_ is not None and img_.size > 0:
            self.img = cv.cvtColor(img_, cv.COLOR_BGR2RGB)
            h, w = self.img.shape[0:2]
            self.roi = (0, 0, w, h)
            return True

        return False

    def get_zoom_image(self, resize_to_orig_size: bool = True) -> np.ndarray:
        h, w = self.img.shape[0:2]
        rx, ry, rw, rh = self.roi
        img_roi = self.img[ry:ry + rh, rx:rx + rw]

        if resize_to_orig_size:
            img_roi = cv.resize(img_roi, dsize=(w, h), interpolation=cv.INTER_AREA)

        return img_roi

    def get_image_size(self) -> Tuple[int, int]:
        h, w = self.img.shape[0:2]
        return w, h

    def get_image_aspect(self) -> float:
        h, w = self.img.shape[0:2]
        return w / h

    def get_zoom_factor(self) -> float:
        return self.img.shape[1] / self.roi[2]

    def get_roi(self) -> Tuple[int, int, int, int]:
        return self.roi

    def clear_zoom(self):
        self.roi = (0, 0, self.img.shape[1], self.img.shape[0])

    def translate(self, dx, dy):
        h, w = self.img.shape[0:2]
        rx, ry, rw, rh = self.roi
        dx = int(np.clip(dx, -rx, w - (rx + rw)))
        dy = int(np.clip(dy, -ry, h - (ry + rh)))
        self.roi = (rx + dx, ry + dy, rw, rh)

    def zoom(self, factor: float, min_width: int = 16):
        h, w = self.img.shape[0:2]
        rx, ry, rw, rh = self.roi

        w_new = int(np.clip(rw / factor, min_width, w))
        h_new = int(np.clip(np.round(h * w_new / w), 1, h))
        x_new = (2 * rx + rw) // 2 - w_new // 2
        y_new = (2 * ry + rh) // 2 - h_new // 2
        x_new = int(np.clip(x_new, 0, w - w_new))
        y_new = int(np.clip(y_new, 0, h - h_new))

        self.roi = (x_new, y_new, w_new, h_new)

    def set_roi(self,
                rect: Tuple[int, int, int, int],
                keep_original_aspect: bool = True) -> bool:
        h, w = self.img.shape[0:2]

        rect_ = list(rect)
        if keep_original_aspect:
            new_h = int(rect_[2] * (h / w))
            dy = int((rect_[3] - new_h) / 2)
            rect_[3] = new_h
            rect_[1] += dy

        if rect_[2] == 0 or rect_[2] > w or rect_[3] == 0 or rect_[3] > h:
            return False

        rect_[0] = np.clip(rect_[0], 0, w - rect_[2])
        rect_[1] = np.clip(rect_[1], 0, h - rect_[3])
        self.roi = tuple(rect_)
        
        return True
