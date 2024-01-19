from uuid import UUID, uuid4
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

    def serialize(self) -> Dict:
        return super().serialize()

    def deserialize(self, data: Dict):
        return super().deserialize(data)


class ObjectFactory():
    def __init__(self):
        self._classes = {}

    def register_class(self, name: str, shapes: List[ShapeType]) -> bool:
        if name not in self._classes and len(shapes):
            self._classes[name] = shapes
            return True

        return False

    def get_registered_classes(self, full_info: bool = False) -> List[str]:
        result = []
        for name, shapes in self._classes.items():
            info = name
            if full_info:
                info += f" [" + ", ".join([s.name for s in shapes]) + "]"
            result.append(info)

        return result

    def unregister_class(self, name: str):
        self._classes.pop(name, None)

    def unregister_all_classes(self):
        self._classes.clear()

    def create_object(self, class_name: str) -> Object:
        shape_types = self._classes.get(class_name, None)
        if shape_types is not None:
            shapes = []
            for stype in shape_types:
                shape = create_shape(stype)
                shapes.append(shape)

            return Object(shapes, class_name)

        return None
