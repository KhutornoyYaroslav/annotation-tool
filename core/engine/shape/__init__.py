from enum import Enum
from .shape import ShapeInterface
from .boundingrect import BoundingRect
# from .keypoints import Keypoints


# class ShapeType(Enum):
#     BOUNDINGRECT = 1
#     KEYPOINTS = 2


__all__ = [
    # 'ShapeType',
    'ShapeInterface',
    'BoundingRect'
]


# def create_shape(shape_type: ShapeType, **kwargs) -> ShapeInterface:
#     if shape_type == ShapeType.KEYPOINTS:
#         return Keypoints(kwargs['nodes'], kwargs['edges'], kwargs['name'])

#     raise NotImplementedError
