import copy
import json
from typing import Any


class ConfigLockError(Exception):
    def __init__(self, msg: str = "Setting attribute on locked config node"):
        super(ConfigLockError, self).__init__(msg)


class ConfigTypeError(TypeError):
    def __init__(self, msg: str = "Setting wrong attribute type"):
        super(ConfigTypeError, self).__init__(msg)


class ConfigNode(dict):
    def __init__(self):
        super(ConfigNode, self).__init__()
        dict.__setattr__(self, "_locked", 0)

    def __setitem__(self, key, value):
        if self._locked:
            raise ConfigLockError

        if key in self.keys():
            if type(self[key]) != type(value):
                raise ConfigTypeError()

        return super(ConfigNode, self).__setitem__(key, copy.deepcopy(value))

    def __getitem__(self, key):
        return super(ConfigNode, self).__getitem__(key)

    def __delitem__(self, key):
        return super(ConfigNode, self).__delitem__(key)

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
            if isinstance(value, (ConfigNode, ConfigNodeList)):
                value.lock()

    def unlock(self):
        dict.__setattr__(self, "_locked", 0)
        for value in self.values():
            if isinstance(value, (ConfigNode, ConfigNodeList)):
                value.unlock()

    def islocked(self):
        return self._locked

    def merge_from_file(self, data: dict):
        for key, value in self.items():
            if key in data:
                if isinstance(value, (ConfigNode, ConfigNodeList)):
                    value.merge_from_file(data[key])
                else:
                    self.__setitem__(key, data[key])


class ConfigNodeList(list):
    def __init__(self):
        super(ConfigNodeList, self).__init__()
        list.__setattr__(self, "_locked", 0)

    def _make_node(self) -> ConfigNode:
        node = ConfigNode()
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
            super(ConfigNodeList, dcopy).append(copy.deepcopy(value))

        if self.islocked():
            dcopy.lock()

        return dcopy

    def append(self):
        if self._locked:
            raise ConfigLockError

        return super(ConfigNodeList, self).append(self._make_node())

    def extend(self, size: int):
        if self._locked:
            raise ConfigLockError

        nodes = []
        for _ in range(size):
            nodes.append(self._make_node())

        return super(ConfigNodeList, self).extend(nodes)

    def insert(self, index):
        if self._locked:
            raise ConfigLockError

        return super(ConfigNodeList, self).insert(index, self._make_node())

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

    def merge_from_file(self, data: dict):
        self.clear()
        for item in data:
            is_empty = True
            item_ = self._make_node()
            for key, value in item_.items():
                if key in item:
                    is_empty = False
                    if isinstance(value, (ConfigNode, ConfigNodeList)):
                        value.merge_from_file(item[key])
                    else:
                        item_.__setitem__(key, item[key])

            if is_empty:
                raise ConfigTypeError

            super(ConfigNodeList, self).append(item_)



# -------------

# TODO: make_config_examples(path):
# append if ConfigNodeList empty

# https://github.com/kdart/pycopia/blob/master/core/pycopia/basicconfig.py


cfg = ConfigNode()
cfg.version = 0

color_node = ConfigNode()
color_node.r = 255
color_node.g = 255
color_node.b = 255

cfg.classes = ConfigNodeList()
cfg.classes.title = ""
cfg.classes.color = color_node
cfg.classes.shapes = ConfigNodeList()
cfg.classes.shapes.type = "type"
cfg.classes.shapes.tags = ['tag_a', 'tag_b']
# cfg.classes.shapes.append()
# cfg.classes.append()

cfg.ui = ConfigNode()
cfg.ui.resolution = [800, 600]
cfg.ui.fullscreen = False

with open('config_dump.json', 'w') as f:
    json.dump(cfg, f, indent=4)

with open('config.json', 'r') as f:
    data = json.load(f)
    cfg.merge_from_file(data)


# Show config
print(cfg)


# # print(cfg.ui.fullscreen)
# for c in cfg.classes:
#     # print(c.shapes)
#     print(c.title)
#     print(c.color.r)
