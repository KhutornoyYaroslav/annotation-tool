from uuid import UUID, uuid4
from PyQt5.QtCore import QRect
from typing import List, Dict, Tuple, Optional, Union
from core.utils.serializable import Serializable
from core.engine.shapes import ShapeInterface, ShapeType, create_shape


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
