from PyQt5.QtCore import QPoint
from typing import List, Tuple, Union
from core.utils.drawable import QtDrawable
from core.utils.serializable import Serializable
from core.utils.interactable import Interactable


class ShapeInterface(Serializable, Interactable, QtDrawable):
    def is_empty(self) -> bool:
        raise NotImplementedError

    def get_points_list(self) -> List[str]:
        raise NotImplementedError

    def get_points_info(self) -> List[Tuple[str, str]]:
        raise NotImplementedError

    def set_current_point_idx(self, idx: int) -> bool:
        raise NotImplementedError

    def get_current_point_idx(self) -> int:
        raise NotImplementedError

    def to_next_point(self):
        raise NotImplementedError

    def get_current_point(self) -> Union[QPoint, None]:
        raise NotImplementedError

    def disable_current_point(self):
        raise NotImplementedError

    # def set_current_point(self, pt: QPoint) -> bool:
    #     raise NotImplementedError

    # def set_current_point_idx_by_position(self, pos: QPoint, max_radius: int = 8) -> bool:
    #     raise NotImplementedError
