import json
import os

for file in os.listdir('models'):
    full_filename = "%s/%s" % ('models', file)
    with open(full_filename, "r") as f:
        data = json.load(f)
        if data["car_type"] == "2x":
            data["car_type"] = "Hatchback"
            with open(full_filename, "w") as fw:
                json.dump(data, fw)
        elif data["car_type"] == "3x":
            data["car_type"] = "Sedan"
            with open(full_filename, "w") as fw:
                json.dump(data, fw)

