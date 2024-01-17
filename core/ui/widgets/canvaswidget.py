import numpy as np
import OpenGL.GL as gl
from OpenGL import GLU
from typing import Tuple, List
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, QPoint
from core.ui.graphics.panandzoom import PanAndZoom
# from core.ui.graphics.drawable import Drawable


class CanvasWidgetEvents(QObject):
    mouse_left_clicked = pyqtSignal(tuple)
    mouse_right_clicked = pyqtSignal(tuple)


class CanvasWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent):
        QtWidgets.QOpenGLWidget.__init__(self, parent)
        self.events = CanvasWidgetEvents(self)
        self.gl_buffer_id = None
        self.gl_buffer_reload_flag = False
        self.canvas = PanAndZoom()
        self.mouse_press_event_pos = QPoint(0, 0)
        self.mouse_prev_press_event_pos = QPoint(0, 0)
        self.mouse_prev_press_event_button = QPoint(0, 0)
        self.drawables = []
        self._zoom_factor = 1.25

    def clear(self):
        self.canvas.clear()
        self.gl_buffer_reload_flag = False

    def set_canvas_image(self, path: str) -> bool:
        if self.canvas.load_image(path):
            self.gl_buffer_reload_flag = True
            return True

        return False

    def set_zoom_factor(self, factor: float):
        self._zoom_factor = factor

    # TODO: fix
    def set_drawables(self, items): # : List[Drawable]):
        self.drawables = items

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.mouse_press_event_pos = a0.pos()
        self.mouse_prev_press_event_pos = a0.pos()
        self.mouse_prev_press_event_button = a0.button()

        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.mouse_prev_press_event_button == QtCore.Qt.LeftButton:
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

    #     # Keypoints
    #     # Set position of keypoint

    #     if a0.button() == QtCore.Qt.LeftButton:
    #         kpts_combobox = self.parent().comboBox_keypoints
    #         objects_combobox = self.parent().comboBox_context_objects
    #         masks_combobox = self.parent().comboBox_context_masks
    #         # Forgot to press new_car button
    #         # Adds new obj
    #         if self.current_mode == "kpts":
    #             if objects_combobox.currentIndex() == -1:
    #                 self.parent().new_object_button_clicked()
    #         elif self.current_mode == "zones":
    #             if masks_combobox.currentIndex() == -1:
    #                 self.parent().new_mask_button_clicked()
    #         # Undo \ Redo
    #         ctx = self.parent().context_history.get_current().context
    #         if ctx is not None:
    #             if self.background.contains(pos_img):
    #                 self.parent().context_history.add_action(
    #                     UndoRedoItem(copy.deepcopy(ctx), self.parent().comboBox_context_objects.currentIndex(),
    #                                  self.parent().comboBox_context_masks.currentIndex()))
    #                 if self.current_mode == "kpts":
    #                     self.parent().get_curr_object_pts()[kpts_combobox.currentText()] = pos_img
    #                     self.parent().comboBox_keypoints.setItemData(kpts_combobox.currentIndex(),
    #                                                                  QtGui.QColor(120, 250, 92),
    #                                                                  QtCore.Qt.BackgroundRole)
    #                 elif self.current_mode == "zones":
    #                     points_list = self.parent().get_curr_mask_pts()
    #                     points_list.append(pos_img)
    #                 self.parent().context_history.get_current().context.save()
    #                 self.repaint()

    #     # Choose keypoint on screen
    #     if a0.button() == QtCore.Qt.RightButton:
    #         # Find nearest keypoint to mouse position
    #         dist_min = 1e6
    #         dist_thresh = 32
    #         point_key_chosen = None
    #         object_idx_chosen = None
    #         mask_idx_chosen = None

    #         # if self.current_mode == "zones":
    #         #     if masks_combobox.currentIndex() == -1:
    #         #         self.parent().new_zone_button_clicked()

    #         ctx = self.parent().context_history.get_current().context
    #         if ctx is not None:
    #             if self.current_mode == "kpts":
    #                 curr_object_idx = self.parent().comboBox_context_objects.currentIndex()
    #                 if curr_object_idx == -1:  # iterate over all cars
    #                     r = range(len(self.parent().comboBox_context_objects))
    #                 else:  # only one car
    #                     r = range(curr_object_idx, curr_object_idx + 1)
    #                 for curr_object_idx in r:
    #                     for pt_key, point in ctx.objects[curr_object_idx].keypoints.items():
    #                         if point is not None:
    #                             dist = np.linalg.norm([point.x() - pos_img.x(), point.y() - pos_img.y()])
    #                             if (dist <= dist_thresh) and (dist <= dist_min):
    #                                 dist_min = dist
    #                                 point_key_chosen = pt_key
    #                                 object_idx_chosen = curr_object_idx
    #             elif self.current_mode == "zones":
    #                 curr_mask_idx = self.parent().comboBox_context_masks.currentIndex()
    #                 if curr_mask_idx == -1:  # iterate over all masks
    #                     r = range(len(self.parent().comboBox_context_masks))
    #                 else:  # only one car
    #                     r = range(curr_mask_idx, curr_mask_idx + 1)
    #                 for curr_mask_idx in r:
    #                     for idx, point in enumerate(ctx.masks[curr_mask_idx].mask):
    #                         dist = np.linalg.norm([point.x() - pos_img.x(), point.y() - pos_img.y()])
    #                         if (dist <= dist_thresh) and (dist <= dist_min):
    #                             dist_min = dist
    #                             self.current_mask_point = idx
    #                             mask_idx_chosen = curr_mask_idx
    #         # Set found keypoint as active
    #         if point_key_chosen is not None:
    #             if self.current_mode == "kpts":
    #                 self.parent().comboBox_context_objects.setCurrentIndex(object_idx_chosen)
    #                 self.parent().context_history.get_current().comboBox_context_objects_idx = object_idx_chosen
    #                 comboBox_keypoints_id = self.parent().comboBox_keypoints.findText(str(point_key_chosen))
    #                 if comboBox_keypoints_id != -1:
    #                     self.parent().comboBox_keypoints.setCurrentIndex(comboBox_keypoints_id)
    #                 else:
    #                     raise IndexError("Could not find key '" + point_key_chosen + "' in combobox")
    #                 self.parent().update_keypoint_combobox()

    #         elif self.current_mode == "zones":
    #             print("test")
    #             print(mask_idx_chosen)
    #             if mask_idx_chosen is not None:
    #                 self.parent().comboBox_context_masks.setCurrentIndex(mask_idx_chosen)
    #                 self.parent().context_history.get_current().comboBox_context_masks_idx = mask_idx_chosen
    #             self.parent().update_context_masks_combobox()

    #         # Repaint widgets
    #         self.parent().repaint()
    # #         self.parent().glWidget_preview.repaint()
    #         return super().mouseReleaseEvent(a0)

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

    # def contains(self, pt:QPoint):
    #     return (self.src_size.width() > pt.x() >= 0) and (self.src_size.height() > pt.y() >= 0)

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
        if not self.canvas.is_empty():
            painter = QtGui.QPainter(self)
            for d in self.drawables:
                d.draw(painter, self.img2viewport)
