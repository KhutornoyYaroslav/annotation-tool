import numpy as np
from typing import List
from ultralytics import YOLO


def detect_cars(img: np.ndarray, min_conf: float = 0.5, model: str = 'yolov8m.pt', device: str = 'cuda') -> List[List[int]]:
    results = []

    if img is None or not img.size:
        return results
    
    detector = YOLO(model)
    predicts = detector.predict(img, conf=min_conf, imgsz=416, classes=[2], device=device)

    for pred in predicts:
        confs = pred.boxes.conf.cpu().numpy()
        boxes = pred.boxes.xyxy.cpu().numpy().astype(int)

        for c, b in zip(confs, boxes):
            results.append(b.tolist())

    return results
