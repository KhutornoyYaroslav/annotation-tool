from typing import List
from core.engine.objects.object import Object
from core.engine.shapes import ShapeType, create_shape


class ObjectFactory():
    def __init__(self):
        self._classes = {}

    def register_class(self, name: str, shapes: List[ShapeType]) -> bool:
        if name not in self._classes and len(shapes):
            self._classes[name] = shapes
            return True

        return False

    def get_registered_classes_info(self, full_info: bool = False) -> List[str]:
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
