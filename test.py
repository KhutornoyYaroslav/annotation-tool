from core.engine.object import Object, ObjectFactory
from core.engine.shape.shape import ShapeInterface


class BoundingRect(ShapeInterface):
    def __init__(self):
        pass

class Polygon(ShapeInterface):
    def __init__(self):
        pass


factory = ObjectFactory()
factory.register_class('person', BoundingRect)
factory.register_class('car', BoundingRect)

obj1 = factory.create('person')
obj2 = factory.create('person')

print(obj1._class, obj1._uuid, obj1._shape)
print(obj2._class, obj2._uuid, obj2._shape)