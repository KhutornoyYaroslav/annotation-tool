import numpy as np

def get_rotation_matrix(eulers, order='YXZ'):
    eulers_rads = np.radians(eulers)
    st = np.sin(eulers_rads)
    ct = np.cos(eulers_rads)

    rx = np.array([[1, 0, 0], [0, ct[0], -st[0]], [0, st[0], ct[0]]])
    ry = np.array([[ct[1], 0, st[1]], [0, 1, 0], [-st[1], 0, ct[1]]])
    rz = np.array([[ct[2], -st[2], 0], [st[2], ct[2], 0], [0, 0, 1]])

    if order == 'XYZ':
        r = np.matmul(rx, np.matmul(ry, rz))
    elif order == 'XZY':
        r = np.matmul(rx, np.matmul(rz, ry))
    elif order == 'YXZ':
        r = np.matmul(ry, np.matmul(rx, rz))
    elif order == 'YZX':
        r = np.matmul(ry, np.matmul(rz, rx))
    elif order == 'ZXY':
        r = np.matmul(rz, np.matmul(rx, ry))
    else:
        r = np.matmul(rz, np.matmul(ry, rx))
    return r

def get_eulers_from_matrix(rot, order='YXZ'):

    tmp = rot[1,1] / rot[1,0] # cos/sin (rotation around Z axis)
    roll = np.arctan(tmp)

    tmp = rot[2,2] / rot[0,2] # cos/sin (rotation around Y axis)
    yaw = np.arctan(tmp)

    pitch = np.arcsin(-rot[1][2]) # -sin (rotation around X axis)

    return np.degrees([pitch, yaw, roll])