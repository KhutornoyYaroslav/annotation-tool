from PyQt5.QtCore import QPoint
from typing import List, Tuple, Union, Any, TypeVar, Generic
from core.utils.drawable import QtDrawable
from core.utils.serializable import Serializable
from core.utils.interactable import Interactable


T = TypeVar('T')

# TODO:
class ShapeItemInterface(Generic[T]):
    def set_value(self, val: T):
        raise NotImplementedError

    def get_value(self) -> T:
        raise NotImplementedError

    def set_label(self, label: str):
        raise NotImplementedError

    def get_label(self) -> str:
        raise NotImplementedError

# TODO:
class ShapeInterface(Serializable, Interactable, QtDrawable):
    def is_empty(self) -> bool:
        raise NotImplementedError

    def get_items_labels(self) -> List[str]:
        raise NotImplementedError

    def get_items_repr(self) -> List[Tuple[str, str]]:
        raise NotImplementedError

    def set_item(self, idx: int, val: Union[Any, None]) -> bool:
        raise NotImplementedError

    def get_item(self, idx: int) -> Union[Any, None]:
        raise NotImplementedError

    def get_items_idxs_by_area(self, x1: int, y1: int, x2: int, y2: int) -> List[int]:
        raise NotImplementedError






# class ShapeInterface(Serializable, Interactable, QtDrawable):
#     def is_empty(self) -> bool:
#         raise NotImplementedError

#     def get_points_list(self) -> List[str]:
#         raise NotImplementedError

#     def get_points_info(self) -> List[Tuple[str, str]]:
#         raise NotImplementedError

#     def set_current_point_idx(self, idx: int) -> bool:
#         raise NotImplementedError

#     def get_current_point_idx(self) -> int:
#         raise NotImplementedError

#     def to_next_point(self):
#         raise NotImplementedError

#     def get_current_point(self) -> Union[QPoint, None]:
#         raise NotImplementedError

#     def disable_current_point(self):
#         raise NotImplementedError

#     def set_active(self, active: bool):
#         raise NotImplementedError

#     # def set_current_point(self, pt: QPoint) -> bool:
#     #     raise NotImplementedError

#     # def set_current_point_idx_by_position(self, pos: QPoint, max_radius: int = 8) -> bool:
#     #     raise NotImplementedError
