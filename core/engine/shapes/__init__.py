
from enum import Enum
from .shapeinterface import ShapeInterface
from .boundingrect import BoundingRect
from .keypoints import Keypoints


class ShapeType(Enum):
    boundingrect = 1
    keypoints = 2

    @staticmethod
    def from_str(name: str, default = None):
        name_ = name.lower()
        if name_ in [v.name for v in ShapeType]:
            return ShapeType[name_]

        return default


def create_shape(type: ShapeType) -> ShapeInterface:
    if type == ShapeType.boundingrect:
        return BoundingRect()

    if type == ShapeType.keypoints:
        return Keypoints() # TODO: configurate

    return None


__all__ = [
    'ShapeType',
    'ShapeInterface',
    'BoundingRect',
    'Keypoints',
    'create_shape'
]
