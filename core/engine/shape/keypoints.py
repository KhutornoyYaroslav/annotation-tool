import numpy as np
from typing import Dict, List, Tuple, Optional
# from core.engine.shapes.point import Point2d
from core.engine.shape.shape import ShapeInterface

from core.engine.geometry.point import VisiblePoint

from core.utils.serializable import Serializable


# class Keypoint(Point2d):
#     def __init__(self, label: str, x: Optional[int] = None, y: Optional[int] = None, visible: bool = True):
#         super().__init__(x, y, visible)
#         self._label = label

#     def get_label(self) -> str:
#         return self._label

#     def serialize(self) -> Dict:
#         data = {}
#         data['x'] = self._x
#         data['y'] = self._y
#         data['visible'] = self._visible
#         data['label'] = self._label

#         return data

#     def deserialize(self, data: Dict):
#         self._x = data['x']
#         self._y = data['y']
#         self._visible = data['visible']
#         self._label = data['label']

# class Keypoint()


class Keypoints(ShapeInterface):
    def __init__(self, nodes: List[str], edges: List[Tuple[int, int]]):
        self._keypoints = dict.fromkeys(nodes, None)
        self._edges = edges

    def is_empty(self) -> bool:
        for pt in self._keypoints:
            if pt is None:
                return False

        return True

    def serialize(self) -> Dict:
        data = {}

        data['keypoints'] = {}
        for label, point in self.keypoints.items():
            data['keypoints'][label] = {'x': point.x(), 'y': point.y()}

        return data

    def deserialize(self, data: Dict):
        # self.name = data['name']

        for k in self.keypoints.keys():
            self.keypoints[k] = data['keypoints'][k]

    # def get_current_keypoint(self):
    #     if not self.keypoints:
    #         return None

    #     key = list(self.keypoints.keys())[self.curr_keypoint_idx] # TODO: list(.values())[idx]

    #     return self.keypoints[key] # TODO: as (key. value) pair ?

    # def set_curr_keypoint(self, pos: Tuple[int, int]):
    #     key = list(self.keypoints.keys())[self.curr_keypoint_idx]
    #     self.keypoints[key] = Point2d(*pos)

    # def disable_cur_keypoint(self):
    #     key = list(self.keypoints.keys())[self.curr_keypoint_idx]
    #     self.keypoints[key] = Point2d()

    # def set_curr_keypoint_idx(self, idx: int) -> bool:
    #     if 0 <= idx < len(self.keypoints):
    #         self.curr_keypoint_idx = idx
    #         return True

    #     return False

    # def set_curr_keypoint_idx_by_coords(self, x: int, y: int, max_radius: int = 8) -> bool:
    #     idx_best = None
    #     dist_best = max_radius
    #     for idx, pt in enumerate(self.keypoints.values()):
    #         if not pt.is_empty():
    #             dist = np.linalg.norm([pt.x - x, pt.y - y])
    #             if dist <= dist_best:
    #                 dist_best = dist
    #                 idx_best = idx

    #     if idx_best is not None:
    #         self.curr_keypoint_idx = idx_best
    #         return True

    #     return False






# class Keypoints(BaseShape):
#     def __init__(self, nodes: List[str], edges: List[Tuple[int, int]], name: str):
#         self.keypoints = dict.fromkeys(nodes, None)
#         for key in self.keypoints.keys():
#             self.keypoints[key] = Point2d()
#         self.edges = edges
#         self.name = name
#         self.curr_keypoint_idx = 0

#     def __str__(self):
#         return self.name

#     def is_empty(self) -> bool:
#         for v in self.keypoints.values():
#             if not v.is_empty():
#                 return False

#         return True

#     def serialize(self) -> Dict:
#         data = {}
#         data['name'] = self.name

#         data['keypoints'] = {}
#         for k, v in self.keypoints.items():
#             data['keypoints'][k] = v.serialize()

#         return data

#     def deserialize(self, data: Dict):
#         self.name = data['name']

#         for k in self.keypoints.keys():
#             self.keypoints[k] = data['keypoints'][k]

#     def get_current_keypoint(self):
#         if not self.keypoints:
#             return None

#         key = list(self.keypoints.keys())[self.curr_keypoint_idx] # TODO: list(.values())[idx]

#         return self.keypoints[key] # TODO: as (key. value) pair ?

#     def set_curr_keypoint(self, pos: Tuple[int, int]):
#         key = list(self.keypoints.keys())[self.curr_keypoint_idx]
#         self.keypoints[key] = Point2d(*pos)

#     def disable_cur_keypoint(self):
#         key = list(self.keypoints.keys())[self.curr_keypoint_idx]
#         self.keypoints[key] = Point2d()

#     def set_curr_keypoint_idx(self, idx: int) -> bool:
#         if 0 <= idx < len(self.keypoints):
#             self.curr_keypoint_idx = idx
#             return True

#         return False

#     def set_curr_keypoint_idx_by_coords(self, x: int, y: int, max_radius: int = 8) -> bool:
#         idx_best = None
#         dist_best = max_radius
#         for idx, pt in enumerate(self.keypoints.values()):
#             if not pt.is_empty():
#                 dist = np.linalg.norm([pt.x - x, pt.y - y])
#                 if dist <= dist_best:
#                     dist_best = dist
#                     idx_best = idx

#         if idx_best is not None:
#             self.curr_keypoint_idx = idx_best
#             return True

#         return False
