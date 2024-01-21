car_nodes = [
    "fl wheel", # 0
    "bl wheel", # 1
    "br wheel", # 2
    "fr wheel", # 3
    "windshield tr", # 4
    "windshield tl", # 5
    "windshield bl", # 6
    "windshield br", # 7
    "rear window tl", # 8
    "rear window tr", # 9
    "rear window br", # 10
    "rear window bl", # 11
    "rearview mirror l", # 12
    "rearview mirror r", # 13
    "bottom of license fr", # 14
    "bottom of license fl", # 15
    "bottom of license bl", # 16
    "bottom of license br", # 17
    "headlight fr inner bottom", # 18
    "headlight fr outer top", # 19
    "headlight fl inner bottom", # 20
    "headlight fl outer top", # 21
    "headlight bl inner bottom", # 22
    "headlight bl outer top", # 23
    "headlight br inner bottom", # 24
    "headlight br outer top", # 25
    "bottom bumper fl", # 26
    "bottom bumper bl", # 27 # TODO: change order
    "bottom bumper br", # 28 # TODO: change order
    "bottom bumper fr", # 29 # TODO: change order
    "side window back l", # 30
    "side window back r" # 31
]

car_edges = [
    [14, 15], [29, 14], [26, 15], [29, 26],
    [29, 18], [18,19], [18, 20], [19, 21],
    [18, 14], [20, 15], [26, 20], [21, 20],
    [29, 19], [26, 21], [19, 7], [21, 6],
    [7, 6], [7, 4], [6, 5], [4, 5],
    [29, 3], [3, 2], [26, 0], [0, 1],
    [4, 9], [5, 8], [9, 8], [3, 7],
    [0, 6], [7, 13], [6, 12], [13, 4],
    [12, 5], [3, 13], [0, 12], [3, 19],
    [0, 21], [2, 13], [1, 12], [2, 31],
    [1, 30], [31, 10], [30, 11], [10, 9],
    [11, 8], [2, 28], [1, 27], [28, 25],
    [27, 23], [25, 31], [23, 30], [25, 10],
    [23, 11], [28, 27], [25, 23], [28, 17],
    [27, 16], [28, 24], [27, 22], [24, 25],
    [22, 23], [24, 22], [17, 16], [17, 24],
    [16, 22], [10, 11]
]
