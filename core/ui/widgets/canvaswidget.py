import numpy as np
import OpenGL.GL as gl
from OpenGL import GLU
from typing import Tuple, List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QLineF, Qt, QRect
from core.ui.graphics.panandzoom import PanAndZoom
from core.utils.drawable import QtDrawable
from core.utils.basicconfig import Config


class CanvasWidgetEvents(QObject):
    mouse_left_clicked = pyqtSignal(tuple)
    mouse_right_clicked = pyqtSignal(tuple)


class CanvasWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent, cfg: Config):
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        self._cfg = cfg
        self.events = CanvasWidgetEvents(self)
        self.gl_buffer_id = None
        self.gl_buffer_reload_flag = False
        self.canvas = PanAndZoom()
        self.mouse_press_event_pos = QPoint(0, 0)
        self.mouse_prev_press_event_pos = QPoint(0, 0)
        self.mouse_current_pos = QPoint(0, 0)
        self.drawables = []
        self._zoom_factor = 1.25
        self.initialize()

    def initialize(self):
        self.setMouseTracking(True)

    def clear(self):
        self.canvas.clear()
        self.gl_buffer_reload_flag = False

    def set_canvas_image(self, img: np.ndarray):
        self.canvas.set_image(img)
        self.gl_buffer_reload_flag = True

    def set_zoom_factor(self, factor: float):
        self._zoom_factor = factor

    def set_drawables(self, items: List[QtDrawable]):
        self.drawables = items

    def set_focus(self, img_roi: QRect) -> bool:
        if not img_roi.isEmpty() and not self.canvas.is_empty():
            pad_factor = self._cfg.control.auto_focus.pad_factor
            min_width = self._cfg.control.auto_focus.roi_min_width

            aspect = img_roi.width() / img_roi.height()
            new_w = int(max(pad_factor * img_roi.width(), min_width))
            new_h = int(new_w * aspect)
            new_x = int(img_roi.x() + img_roi.width() / 2 - new_w / 2)
            new_y = int(img_roi.y() + img_roi.height() / 2 - new_h / 2)
            new_roi = QRect(new_x, new_y, new_w, new_h)

            if self.canvas.set_roi((new_roi.x(), new_roi.y(), new_roi.width(), new_roi.height()), True):           
                self.gl_buffer_reload_flag = True
                self.repaint()
                return True

        return False

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_press_event_pos = a0.pos()
        self.mouse_prev_press_event_pos = a0.pos()

        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_current_pos = a0.pos()
        self.repaint()

        if a0.buttons() == QtCore.Qt.LeftButton:
            if not self.canvas.is_empty():
                pos_img = self.viewport2img(a0.pos())
                prev_pos_img = self.viewport2img(self.mouse_prev_press_event_pos)

                if pos_img is not None and prev_pos_img is not None:
                    delta = pos_img - prev_pos_img

                    self.canvas.translate(-delta.x(), -delta.y())
                    self.gl_buffer_reload_flag = True

                    self.mouse_prev_press_event_pos = a0.pos()
                    self.repaint()

        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        if not self.canvas.is_empty():
            if a0.button() == QtCore.Qt.LeftButton:
                if self.mouse_press_event_pos == a0.pos(): # TODO: compare in img coordiantes ?
                    pos_img = self.viewport2img(a0.pos())
                    if pos_img is not None:
                        self.events.mouse_left_clicked.emit((pos_img.x(), pos_img.y()))
            if a0.button() == QtCore.Qt.RightButton:
                pos_img = self.viewport2img(self.mouse_press_event_pos)
                if pos_img is not None:
                    self.events.mouse_right_clicked.emit((pos_img.x(), pos_img.y()))

        return super().mouseReleaseEvent(a0)

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if not self.canvas.is_empty():
            scale = self._zoom_factor
            if a0.angleDelta().y() <= 0:
                scale = 1 / scale
            self.canvas.zoom(scale)

            self.gl_buffer_reload_flag = True
            self.repaint()

        return super().wheelEvent(a0)

    def calc_viewport_scale_offset(self) -> Tuple[float, Tuple[int, int]]:
        wnd_size = self.width(), self.height()

        if not self.canvas.is_empty():
            img_size = self.canvas.get_image_size()
        else:
            img_size = wnd_size

        img_aspect = img_size[0] / img_size[1]
        wnd_aspect = wnd_size[0] / wnd_size[1]

        if wnd_aspect > img_aspect:
            scale = wnd_size[1] / img_size[1]
            offset = (int((wnd_size[0] - scale * img_size[0]) / 2), 0)
        else:
            scale = wnd_size[0] / img_size[0]
            offset = (0, int((wnd_size[1] - scale * img_size[1]) / 2))

        return scale, offset

    def calc_viewport(self) -> Tuple[int, int, int, int]:
        x, y, w, h = 0, 0, self.width(), self.height()

        if not self.canvas.is_empty():
            img_size = self.canvas.get_image_size()
            s, (x, y) = self.calc_viewport_scale_offset()
            w, h = int(s * img_size[0]), int(s * img_size[1])

        return x, y, w, h

    def viewport2img(self, point: QPoint) -> QPoint:
        roi = self.canvas.get_roi()
        w, h = self.canvas.get_image_size()

        scale, offset = self.calc_viewport_scale_offset()
        x = roi[0] + roi[2] * (point.x() - offset[0]) / (w * scale)
        y = roi[1] + roi[3] * (point.y() - offset[1]) / (h * scale)

        if (roi[0] <= x < roi[0] + roi[2]) and (roi[1] <= y < roi[1] + roi[3]):
            return QPoint(x, y)

        return None

    def img2viewport(self, point: QPoint) -> QPoint:
        roi = self.canvas.get_roi()
        normed_x = (point.x() - roi[0] + 0.5) / roi[2]
        normed_y = (point.y() - roi[1] + 0.5) / roi[3]

        if normed_x < 0.0 or normed_x >= 1.0 or normed_y < 0.0 or normed_y >= 1.0:
            return None

        w, h = self.canvas.get_image_size()
        s, offset = self.calc_viewport_scale_offset()

        x = int(np.round(s * (normed_x * w) + offset[0]))
        y = int(np.round(s * (normed_y * h) + offset[1]))

        return QPoint(x, y)

    def initializeGL(self):
        gl.glClearColor(0.3, 0.3, 0.3, 1.0)
        gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        self.gl_buffer_id = gl.glGenBuffers(1)

    def resizeGL(self, width, height):
        # Update perspective projection
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        if not self.canvas.is_empty():
            GLU.gluPerspective(45.0, self.canvas.get_image_aspect(), 0.1, 1000.0)
        else:
            GLU.gluPerspective(45.0, width / height, 0.1, 1000.0)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # Update viewport
        gl.glViewport(*self.calc_viewport())

        # Draw background
        if not self.canvas.is_empty():
            if self.gl_buffer_reload_flag:
                img = self.canvas.get_zoom_image()
                data = np.flipud(img).flatten()
                gl.glBindBuffer(gl.GL_PIXEL_UNPACK_BUFFER, self.gl_buffer_id)
                gl.glBufferData(gl.GL_PIXEL_UNPACK_BUFFER, len(data), data, gl.GL_STREAM_DRAW)
                gl.glBindBuffer(gl.GL_PIXEL_UNPACK_BUFFER, 0)
                self.resizeGL(self.width(), self.height())
                self.gl_buffer_reload_flag = False

            vp_scale, vp_offset = self.calc_viewport_scale_offset()
            gl.glBindBuffer(gl.GL_PIXEL_UNPACK_BUFFER, self.gl_buffer_id)
            gl.glPixelZoom(vp_scale, vp_scale)
            gl.glWindowPos2i(*vp_offset)
            gl.glDrawPixels(*self.canvas.get_image_size(), gl.GL_RGB, gl.GL_UNSIGNED_BYTE, None)
            gl.glBindBuffer(gl.GL_PIXEL_UNPACK_BUFFER, 0)

        # Draw objects
        painter = QtGui.QPainter(self)
        if not self.canvas.is_empty():
            for d in self.drawables:
                d.draw(painter, self.img2viewport)

        # Draw cursor
        if not self.canvas.is_empty():
            painter.setPen(QPen(QColor(0, 255, 0), 1.0, Qt.DashLine))
            mx, my = self.mouse_current_pos.x(), self.mouse_current_pos.y()
            hline = QLineF(0, my, self.width(), my)
            vline = QLineF(mx, 0, mx, self.height())
            painter.drawLines([hline, vline])
