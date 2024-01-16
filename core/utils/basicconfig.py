import copy
import json
from typing import Any


class ConfigLockError(Exception):
    def __init__(self, msg: str = "Setting attribute on locked config node"):
        super(ConfigLockError, self).__init__(msg)


class ConfigTypeError(TypeError):
    def __init__(self, msg: str = "Setting wrong attribute type"):
        super(ConfigTypeError, self).__init__(msg)


class DictNode(dict):
    def __init__(self):
        super(DictNode, self).__init__()
        dict.__setattr__(self, "_locked", 0)

    def __setitem__(self, key, value):
        if self._locked:
            raise ConfigLockError

        if key in self.keys():
            if type(self[key]) != type(value):
                raise ConfigTypeError()

        return super(DictNode, self).__setitem__(key, copy.deepcopy(value))

    def __getitem__(self, key):
        return super(DictNode, self).__getitem__(key)

    def __delitem__(self, key):
        return super(DictNode, self).__delitem__(key)

    __setattr__ = __setitem__

    def __getattr__(self, name, default = None):
        return self.__getitem__(name) if name in self else default

    def __deepcopy__(self, memo):
        dcopy = type(self)()
        memo[id(self)] = dcopy

        for k, v in self.items():
            setattr(dcopy, k, copy.deepcopy(v, memo))

        if self.islocked():
            dcopy.lock()

        return dcopy

    def lock(self):
        dict.__setattr__(self, "_locked", 1)
        for value in self.values():
            if isinstance(value, (DictNode, ListNode)):
                value.lock()

    def unlock(self):
        dict.__setattr__(self, "_locked", 0)
        for value in self.values():
            if isinstance(value, (DictNode, ListNode)):
                value.unlock()

    def islocked(self):
        return self._locked

    def merge_from_dict(self, data: dict):
        for key, value in self.items():
            if key in data:
                if isinstance(value, (DictNode, ListNode)):
                    value.merge_from_dict(data[key])
                else:
                    self.__setitem__(key, data[key])

    def to_dict(self) -> dict:
        result = {}
        for key, value in self.items():
            if isinstance(value, (DictNode, ListNode)):
                result[key] = value.to_dict()
            else:
                result[key] = value

        return result


class ListNode(list):
    def __init__(self):
        super(ListNode, self).__init__()
        list.__setattr__(self, "_locked", 0)

    def _make_node(self) -> DictNode:
        node = DictNode()
        for attr in self.__dict__:
            if attr != "_locked":
                node.__setattr__(attr, getattr(self, attr))

        if self.islocked():
            node.lock()

        return node

    def __setattr__(self, __name: str, __value: Any) -> None:
        if hasattr(self, __name):
            if type(getattr(self, __name)) != type(__value):
                raise ConfigTypeError()

        return super().__setattr__(__name, __value)

    def __deepcopy__(self, memo):
        dcopy = type(self)()
        memo[id(self)] = dcopy

        for attr in self.__dict__:
            if attr != "_locked":
                dcopy.__setattr__(attr, getattr(self, attr))

        for value in self:
            super(ListNode, dcopy).append(copy.deepcopy(value))

        if self.islocked():
            dcopy.lock()

        return dcopy

    def append(self):
        if self._locked:
            raise ConfigLockError

        return super(ListNode, self).append(self._make_node())

    def extend(self, size: int):
        if self._locked:
            raise ConfigLockError

        nodes = []
        for _ in range(size):
            nodes.append(self._make_node())

        return super(ListNode, self).extend(nodes)

    def insert(self, index):
        if self._locked:
            raise ConfigLockError

        return super(ListNode, self).insert(index, self._make_node())

    def lock(self):
        list.__setattr__(self, "_locked", 1)
        for value in self:
            value.lock()

    def unlock(self):
        list.__setattr__(self, "_locked", 0)
        for value in self:
            value.unlock()

    def islocked(self):
        return self._locked

    def merge_from_dict(self, data: dict):
        self.clear()
        for item in data:
            is_empty = True
            item_ = self._make_node()
            for key, value in item_.items():
                if key in item:
                    is_empty = False
                    if isinstance(value, (DictNode, ListNode)):
                        value.merge_from_dict(item[key])
                    else:
                        item_.__setitem__(key, item[key])

            if is_empty:
                raise ConfigTypeError

            super(ListNode, self).append(item_)

    def to_dict(self) -> list:
        result = []
        for item in self:
            result.append(item.to_dict())

        return result


class Config(DictNode):
    def __init__(self):
        super(Config, self).__init__()

    def save(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    def load(self, path: str):
        with open(path, 'r') as f:
            data = json.load(f)
            self.merge_from_dict(data)
