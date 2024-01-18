from typing import List, Tuple
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
