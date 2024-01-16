from typing import Dict


class Serializable():
    def serialize(self) -> Dict:
        raise NotImplementedError
    
    def deserialize(self, data: Dict):
        raise NotImplementedError
