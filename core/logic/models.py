import os
import glob
import json
import numpy as np
# from core.config import keypoint_labels


def load_model(path:str):
    data = {}
    with open(path) as json_file:
        data = json.load(json_file)

    vertices = np.array(data['vertices']) if 'vertices' in data else None
    triangles = np.array(data['faces']) - 1 if 'faces' in data else None
    keypoints = data['pts'] if 'pts' in data else None
    type = data['car_type'] if 'car_type' in data else None
    name = data['name']

    return vertices, triangles, keypoints, type, name


def unique_model_types(filelist:list) -> list:
    types = []
    for file in filelist:
        type = load_model(file)[3]
        if not type in types:
            types.append(type)
    return types


def is_model_valid(path:str) -> bool:
    vertices, triangles, keypoints, type, name = load_model(path)
    if [x for x in (vertices, triangles, keypoints, type) if x is None]:
        return False

    for t in triangles:
        for v in t:
            if v < 0 or v >= len(vertices):
                return False

    for key, val in keypoints.items():
        if not key in keypoint_labels: return False
        if (val is not None) and (val < 0 or val >= len(vertices)):
            return False

    return True


def scan_models(root_path:str, check:bool = True) -> list:
    filelist = glob.glob(os.path.join(root_path, '*.json'), recursive=True)
    if check:
        filelist = [file for file in filelist if is_model_valid(file)]
    return filelist