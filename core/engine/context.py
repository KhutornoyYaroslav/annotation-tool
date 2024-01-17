import os
import json
from typing import Dict, List
from core.engine.object import Object
from core.utils.serializable import Serializable


class Context(Serializable):
    def __init__(self, fname: str, objects: List[Object] = []):
        self._fname = fname
        self._objects = objects
        self._cur_object_idx = 0

    def serialize(self) -> Dict:
        data = {
            'fname': self._fname,
            'objects': [obj.serialize() for obj in self._objects if not obj.is_empty()]
        }

        return data

    def deserialize(self, data: Dict):
        self._objects = [Object().deserialize(obj) for obj in data['objects']]

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
