import core.engine.geometry as geom
from typing import Dict, Union, Optional
from .shape import ShapeInterface


class BoundingRect(ShapeInterface):
    def __init__(self, tl: Optional[geom.Point] = None, br: Optional[geom.Point] = None):
        super().__init__(self)
        self._tl = tl
        self._br = br

    def is_empty(self) -> bool:
        return self._tl is None or self._br is None

    def get_tl(self) -> Union[geom.Point, None]:
        return self._tl

    def set_tl(self, pt: Union[geom.Point, None]):
        self._tl = pt

    def get_br(self) -> Union[geom.Point, None]:
        return self._br

    def set_br(self, pt: Union[geom.Point, None]):
        self._br = pt

    # def serialize(self) -> Dict:
    #     # TODO: implement
    #     return super().serialize()

    # def deserialize(self, data: Dict):
    #     # TODO: implement
    #     return super().deserialize(data)