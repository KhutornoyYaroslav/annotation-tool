from .object import Object
from .objectfactory import ObjectFactory
from core.config.default import Config
from core.engine.shapes import ShapeType


def build_object_factory(cfg: Config) -> ObjectFactory:
    factory = ObjectFactory()
    for obj_class in cfg.annotation.classes:
        shape_types = []
        for sname in obj_class.shapes:
            stype = ShapeType.from_str(sname)
            if stype != None:
                shape_types.append(stype)
        if len(shape_types):
            factory.register_class(obj_class.name, shape_types)
    return factory


__all__ = [
    'Object',
    'ObjectFactory',
    'build_object_factory'
]
