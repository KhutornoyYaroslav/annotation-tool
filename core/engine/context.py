import os
import json
import ntpath
import cv2 as cv
import numpy as np
from enum import Enum
from typing import Dict, List, Union
from core.engine.objects import Object, ObjectFactory
from core.utils.serializable import Serializable


class AnnotationState(Enum):
    EMPTY = 1
    PARTITIALY = 2
    FULL = 3


class Context(Serializable):
    def __init__(self, fname: str, objects: List[Object] = [], object_factory: ObjectFactory = None):
        self._fname = fname
        self._objects = objects
        self._cur_object_idx = 0
        self._object_factory = object_factory

    def serialize(self) -> Dict:
        data = {
            'fname': ntpath.basename(self._fname),
            # 'objects': [obj.serialize() for obj in self._objects if not obj.is_empty()]
            'objects': [obj.serialize() for obj in self._objects]
        }

        return data

    def get_image(self) -> Union[np.ndarray, None]:
        img = cv.imread(self._fname, cv.IMREAD_COLOR)
        if img is not None and img.size > 0:
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            return img

        return None

    def deserialize(self, data: Dict):
        for obj_data in data['objects']:
            obj = self._object_factory.create_object(obj_data['class'])
            assert obj is not None
            self._objects.append(obj.deserialize(obj_data))

        return self

    def load(self) -> bool:
        if not os.path.exists(self._fname + ".json"):
            return False

        with open(self._fname + ".json", 'r') as f:
            self.deserialize(json.load(f))

        return True

    def save(self) -> bool:
        if not os.path.exists(self._fname):
            return False

        with open(self._fname + ".json", 'w') as f:
            json.dump(self.serialize(), f, indent=4)

        return True

    def is_empty(self):
        return not self._objects or all(obj.is_empty() for obj in self._objects)

    def append_object(self, obj: Object):
        self._objects.append(obj)
        self._cur_object_idx = len(self._objects) - 1

    def remove_object(self, idx: int) -> bool:
        if 0 <= idx < len(self._objects):
            self._objects.pop(idx)
            self._cur_object_idx = max(idx - 1, 0)
            return True

        return False

    def get_objects_list(self) -> List[str]:
        return [o.get_info() for o in self._objects]

    def get_fname(self) -> str:
        return self._fname

    def get_current_object(self):
        if not self._objects:
            return None

        return self._objects[self._cur_object_idx]

    def set_curr_object_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self._objects):
            self._cur_object_idx = idx
            return True

        return False

    def get_current_object_idx(self) -> int:
        return self._cur_object_idx

    def get_objects(self) -> List[Object]:
        return self._objects

    def get_annotation_state(self) -> AnnotationState:
        obj_anno_full_cnt = 0
        for obj in self._objects:
            obj_anno_full = 1
            for shape in obj.get_shapes():
                if shape.is_empty():
                    obj_anno_full = 0
                    break
            obj_anno_full_cnt += obj_anno_full

        if not len(self._objects):
            return AnnotationState.EMPTY
        if obj_anno_full_cnt == len(self._objects):
            return AnnotationState.FULL

        return AnnotationState.PARTITIALY
