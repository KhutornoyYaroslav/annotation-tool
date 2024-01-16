import numpy as np
import cv2 as cv
from torch import rad2deg

from core.calib.geometry import get_eulers_from_matrix
# from core.calib.camera import Camera
# import object as obj

def init_cam_matrix(points2d:list, points3d:list, img_size:tuple):
    objpoints = []
    imgpoints = []

    points3d = np.array(points3d, dtype=np.float32)
    points3d = np.expand_dims(points3d, 0)

    points2d = np.array(points2d, dtype=np.float32)
    points2d = np.expand_dims(points2d, 0)

    objpoints.append(points3d)
    imgpoints.append(points2d)

    k = cv.initCameraMatrix2D(objpoints, imgpoints, img_size, aspectRatio=1.0)
    print(k)

    # test = cv.calibrateCamera(objpoints, imgpoints, img_size, k, None)
    # print(test)

    return k


def calibrate(points2d:list, points3d:list, img_size:tuple, focal):
    assert len(points2d) == len(points3d)

    # Formate intrinsics
    # img_center = (img_size[0] - 1) / 2, (img_size[1] - 1) / 2
    # k = [[focal, 0, img_center[0]], [0, focal, img_center[1]], [0, 0, 1]]

    k = init_cam_matrix(points2d, points3d, img_size)
    k = np.array(k, dtype=np.float32)

        # aov_h_radians = np.radians(self.aov_h)
        # (self.resolution[0] / focal) / 2 = np.tan(aov_h_radians / 2)



    aov_h_radians = 2 * np.arctan((img_size[0] / k[0][0]) / 2)
    print('AoV: {0}'.format(np.degrees(aov_h_radians)))



    # Solve PnP
    status, rvec, tvec = cv.solvePnP(np.array(points3d, dtype=np.float32), np.array(points2d, dtype=np.float32), k, np.zeros((4,1)))

    # Compose direct [R t]
    R, _ = cv.Rodrigues(rvec)
    extr = np.zeros((4, 4))
    extr[:3, :3] = R
    extr[:3, 3] = np.squeeze(tvec)
    extr[3, 3] = 1.0

    # Compute inverse
    _, extr_inv = cv.invert(extr)
    Rinv = extr_inv[:3, :3]

    Tinv = extr_inv[:3, 3]
    eulers = get_eulers_from_matrix(Rinv)
    print('[{0}] R: {1}. T: {2}'.format(status, eulers, Tinv))


# def calibrate(camera:Camera, objects3d:list):

#     noise = 0.0

#     # Referense 3D points in vehicle coordinate system
#     vehicle = obj.Object3d()
#     vehicle.fromJson("./objects/VWPolo2018.json")

#     for object3d in objects3d:
#         # Project to camera plane
#         points3d = [point3d + np.random.normal(0.0, noise, 3) for point3d in object3d.points]
#         points2d = [camera.project_point(point3d) for point3d in points3d]

#         # Solve PnP
#         status, rvec, tvec = cv.solvePnP(np.array(vehicle.points), np.array(points2d), camera.get_intrinsic_matrix(), np.zeros((4,1)))

#         # Compose direct [R t]
#         R, _ = cv.Rodrigues(rvec)
#         extr = np.zeros((4, 4))
#         extr[:3, :3] = R
#         extr[:3, 3] = np.squeeze(tvec)
#         extr[3, 3] = 1.0

#         # Compute inverse
#         _, extr_inv = cv.invert(extr)
#         Rinv = extr_inv[:3, :3]

#         Tinv = extr_inv[:3, 3]
#         eulers = get_eulers_from_matrix(Rinv)
#         print('[{0}] R: {1}. T: {2}'.format(status, eulers, Tinv))