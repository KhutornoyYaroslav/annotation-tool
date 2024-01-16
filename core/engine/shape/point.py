import core.engine.geometry as geom
from .shape import ShapeInterface
from typing import Dict, Optional, Union


class Point(ShapeInterface):
    def __init__(self, pos: Optional[geom.Point] = None):
        self._pos = pos

    def is_empty(self) -> bool:
        return self._pos is None

    def get_pos(self) -> Union[geom.Point, None]:
        return self._pos

    def set_pos(self, pos: Union[geom.Point, None]):
        self._pos = pos

    # def serialize(self) -> Dict:
    #     data = {
    #         'x': self._pos.x(),
    #         'y': self._pos.y()
    #     }

    #     return data

    # def deserialize(self, data: Dict):
    #     return super().deserialize(data)