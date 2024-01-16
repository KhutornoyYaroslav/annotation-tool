import numpy as np
import OpenGL.GL as gl
from OpenGL import GLU
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from core.ui.utils.object3d import Object3D


class GLWidgetModel(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        self.object3d = None
        self.prev_mouse_pos = None

    def setObject3d(self, object: Object3D):
        self.object3d = object
        self.repaint()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if (self.object3d is not None) and (self.prev_mouse_pos is not None):
            delta_pos = a0.pos() - self.prev_mouse_pos
            self.object3d.rotation[0] = (self.object3d.rotation[0] + np.clip(delta_pos.y(), -6, 6)) % 360
            self.object3d.rotation[1] = (self.object3d.rotation[1] + np.clip(delta_pos.x(), -6, 6)) % 360
        self.prev_mouse_pos = a0.pos()

        self.repaint()
        return super().mouseMoveEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.prev_mouse_pos = a0.pos()
        return super().mousePressEvent(a0)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        zoom_step = 0.5
        zoom = a0.angleDelta().y()
        if self.object3d is not None:
            if zoom > 0:
                self.object3d.position[2] += zoom_step
            elif zoom < 0:
                self.object3d.position[2] -= zoom_step

        self.repaint()
        return super().wheelEvent(a0)

    def initializeGL(self):
        gl.glClearColor(0.3, 0.3, 0.3, 1.0)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        GLU.gluPerspective(45.0, width / height, 0.1, 1000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        keys = [key for key, pt in self.parent().get_curr_object_pts().items() if pt is not None]

        cbox_keypoints_idx = self.parent().cbox_keypoints.currentIndex()
        cbox_context_objects_idx = self.parent().cbox_context_objects.currentIndex()

        current_key = None
        if cbox_context_objects_idx != -1:
            if cbox_keypoints_idx != -1:
                current_key = self.parent().comboBox_keypoints.currentText()
            else:
                raise IndexError("Could not find key id'" + cbox_keypoints_idx + "' in combobox")

        if self.object3d is not None:
            self.object3d.draw(color=(0.45, 0.75, 0.95))

            if len(keys):
                if current_key in keys : keys.remove(current_key)
                self.object3d.draw_keypoints(keys, (1., 0., 0.))

            if current_key is not None:
                self.object3d.draw_keypoints([current_key], (0., 0., 1.))