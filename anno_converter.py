import os
import json
import ntpath
from glob import glob
from typing import Union


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
    srcs = sorted(glob(os.path.join(src_root, "*.json")))
    for src in srcs:
        result = {}
        # Read source
        data = read_json(src)
        if data is None:
            print('Failed to read: ', src)
            continue
        # Parse source
        result['fname'] = ntpath.basename(data['path'])

        for sobj in data['objects']:
            print(sobj)
            return

        print(result)
        return


if __name__ == '__main__':
    convert(src_root="C:/Users/khutornoy/Documents/datasets/General dataset 987 pics", dst_root="")