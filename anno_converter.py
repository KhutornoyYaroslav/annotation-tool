import os
import json
import ntpath
from glob import glob
from typing import Union
from uuid import uuid4
from tqdm import tqdm


def read_json(path: str) -> Union[dict, None]:
    with open(path, 'r') as f:
        return json.load(f)

    return None


def write_json(path: str, data) -> bool:
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
        return True

    return False


def convert(src_root: str, dst_root: str) -> None:
    # Create destination dir
    os.makedirs(dst_root, exist_ok=True)

    # Process files
    srcs = sorted(glob(os.path.join(src_root, "*.json")))
    for src in tqdm(srcs):
        result = {}
        # Read source
        data = read_json(src)
        if data is None:
            print('Failed to read: ', src)
            continue
        # Parse source
        result['fname'] = ntpath.basename(data['path'])
        result['objects'] = []

        for src_obj in data['objects']:
            # Create class, uuid
            res_obj = {}
            res_obj['class'] = 'car'
            res_obj['uuid'] = str(uuid4())
            res_obj['shapes'] = []

            # Create Boundinrect shape
            br_shape = {
                'type': "BoundingRect",
                'points': {
                    'top-left': None,
                    "bottom-right": None
                }
            }

            # Create Keypoints shape
            kp_shape = {
                'type': "Keypoints",
                'points': {}
            }

            for key, val in src_obj['keypoints'].items():
                kp_shape['points'][key] = None if val is None else {'x': val[0], 'y': val[1]}

            # Append to objects
            res_obj['shapes'].append(br_shape)
            res_obj['shapes'].append(kp_shape)
            result['objects'].append(res_obj)

        # Write result file
        result_path = os.path.join(dst_root, ntpath.basename(src))
        if not write_json(result_path, result):
            print('Failed to write results to: ', result_path)



if __name__ == '__main__':
    # convert(src_root="C:/Users/khutornoy/Documents/datasets/General dataset 987 pics", dst_root="")
    # convert(src_root="/media/yaroslav/SSD/khutornoy/data/CAR_KEYPOINTS/GeneralDataset987pics",
    #         dst_root="/media/yaroslav/SSD/khutornoy/data/CAR_KEYPOINTS/GeneralDataset987pics_converted/")
    