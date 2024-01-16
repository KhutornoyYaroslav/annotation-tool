import os
import json
from typing import Dict, List
from core.engine.object import AnnotationObject
from core.engine.shape import ShapeType, create_shape
from core.utils.serializable import Serializable


class FileContext(Serializable): # Rename to 'Context' ??
    def __init__(self, fname: str, objects: List[AnnotationObject] = [], try_load: bool = True):
        self.fname = fname
        self.objects = objects
        self.curr_object_idx = 0
        self.annotation_done = False
        # TODO: uncomment later
        # if try_load:
            # self.load()

    def serialize(self) -> Dict:
        data = {
            'fname': self.fname,
            'annotation_done': self.annotation_done,
            'objects': [obj.serialize() for obj in self.objects if not obj.is_empty()]
        }

        return data

    def deserialize(self, data: Dict):
        self.objects = [AnnotationObject().deserialize(obj) for obj in data['objects']]
        self.annotation_done = data['annotation_done']

    def load(self) -> bool:
        if not os.path.exists(self.fname + ".json"):
            return False

        with open(self.fname + ".json", 'r') as f:
            self.deserialize(json.load(f))

        return True

    def save(self) -> bool:
        if not os.path.exists(self.fname):
            return False

        with open(self.fname + ".json", 'w') as f:
            json.dump(self.serialize(), f, indent=4)

        return True

    def is_empty(self):
        return not self.objects or all(obj.is_empty() for obj in self.objects)

    def mark_as_done(self):
        self.annotation_done = True

    def mark_as_in_process(self):
        self.annotation_done = False

    def is_annotation_done(self) -> bool:
        return self.annotation_done

    def create_object(self, shape_type: ShapeType, **kwargs):
        shape = create_shape(shape_type, **kwargs)
        obj = AnnotationObject(shape)
        self.objects.append(obj)
        self.curr_object_idx = len(self.objects) - 1

    def remove_object(self, idx: int) -> bool:
        if 0 <= idx < len(self.objects):
            del self.objects[idx]
            self.curr_object_idx = 0
            return True

        return False

    def get_current_object(self):
        if not self.objects:
            return None

        return self.objects[self.curr_object_idx]

    def set_curr_object_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self.objects):
            self.curr_object_idx = idx
            return True

        return False
