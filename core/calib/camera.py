import numpy as np
from core.calib.geometry import get_rotation_matrix

class Camera:
    def __init__(self, name=""):
        self.aov_h = 30.0
        self.resolution = [640., 480.]
        self.position = [0., 0., 0.]
        self.eulers = [0., 0., 0.]
        self.name = name
        self.fps = 25

    def get_image_center(self):
        return [(self.resolution[0] - 1) / 2, (self.resolution[1] - 1) / 2]

    def set_euler_rot(self, eulers):
        self.eulers = eulers
        self.eulers[0] += 180.0

    def get_euler_rot(self):
        eulers = self.eulers
        eulers[0] -= 180.0
        return eulers

    def get_focal(self):
        aov_h_radians = np.radians(self.aov_h)
        focal = self.resolution[0] / (2 * np.tan(aov_h_radians / 2))
        return focal

    def get_intrinsic_matrix(self):
        f = self.get_focal()
        k = [[f, 0, self.get_image_center()[0]], [0, f, self.get_image_center()[1]], [0, 0, 1]]
        return np.array(k)

    def get_extrinsic_matrix(self):
        r = get_rotation_matrix(self.eulers)
        rt = np.transpose(r)
        t = np.array(self.position)
        tmp = np.matmul(-rt, t)
        res = np.empty((3, 4))
        res[:3, :3] = rt
        res[:3, 3] = tmp
        return res

    def get_proj_matrix(self):
        return np.matmul(self.get_intrinsic_matrix(), self.get_extrinsic_matrix())

    def project_point(self, point3d):
        proj = self.get_proj_matrix()
        point2d = np.matmul(proj, np.append(point3d, 1.0))
        res = [point2d[0] / point2d[2], point2d[1] / point2d[2]]
        return res

    def project_points(self, points3d, drop_out=True):
        proj = self.get_proj_matrix()
        res = []
        for point3d in points3d:
            point2d_homo = np.matmul(proj, np.append(point3d, 1.0))
            point2d = [point2d_homo[0] / point2d_homo[2], point2d_homo[1] / point2d_homo[2]]

            if drop_out:
                if point2d[0] < 0 or point2d[0] >= self.resolution[0]:
                    continue
                if point2d[1] < 0 or point2d[1] >= self.resolution[1]:
                    continue

            res.append(point2d)
        return res