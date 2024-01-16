from typing import Dict
from core.utils.serializable import Serializable


class ShapeInterface(Serializable):
    def is_empty(self) -> bool:
        raise NotImplementedError
