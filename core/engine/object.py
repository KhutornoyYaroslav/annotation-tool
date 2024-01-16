from uuid import UUID, uuid4
from typing import Dict, Optional, Union
# from core.engine.shapes.baseshape import BaseShape
from core.utils.serializable import Serializable

from core.engine.shape import ShapeInterface, ShapeType


class Object(Serializable):
    def __init__(self, shape: ShapeInterface, class_: str, uuid: Optional[UUID] = None):
        self._shape = shape # TODO: object can have multiple shapes (video annotation, for example)
        self._class = class_
        self._uuid = uuid4() if uuid is None else uuid

    def serialize(self) -> Dict:
        data = {
            'uuid': str(self._uuid),
            'class': self._class,
            'shape': self._shape.serialize()
        }

        return data

    def deserialize(self, data: Dict):
        self._uuid = UUID(data['uuid'])
        self._class = data['class']
        self._shape.deserialize(data['shape'])


class ObjectFactory():
    def __init__(self):
        self._object_classes = dict()


    # def register_class(self, class_: str, shape_type: ShapeType):
    #     self._object_classes[class_] = shape_type

    # def unregister_class(self, class_: str):
    #     self._object_classes.pop(class_, None)

    # def create(self, class_: str) -> Union[Object, None]:
    #     shape_type = self._object_classes.get(class_, None)
    #     if shape_type is not None:
    #         # return Object(shape, class_)
    #         # TODO: create Object
    #         return None

    #     return None










# # TODO: может быть этот класс лишний? Странная обертка вокруг shape-ов.
# class AnnotationObject(Serializable):
#     def __init__(self, shape: BaseShape, tags: List[str] = [], uuid: Optional[UUID] = None):
#         self.tags = tags
#         self.shape = shape
#         self.uuid = uuid4() if uuid is None else uuid

#     def __str__(self):
#         return f"{str(self.shape)} [{str(self.uuid)}]"

#     def is_empty(self) -> bool:
#         return self.shape.is_empty()

#     def serialize(self) -> Dict:
#         data = {}
#         data['uuid'] = str(self.uuid)
#         data['shape'] = self.shape.serialize()
#         data['tags'] = self.tags

#         return data

#     def deserialize(self, data: Dict):
#         self.uuid = UUID(data['uuid'])
#         self.shape.deserialize(data['shape'])
#         self.tags = data['tags']
