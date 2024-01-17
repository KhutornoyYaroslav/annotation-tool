from typing import List, Tuple
from PyQt5 import QtWidgets
from core.ui.view import View
from core.engine.model import Model
from core.engine.shapes import ShapeType
# from core.config import car_nodes, car_edges
# from core.controller.drawables import DrawKeypoints


class Controller():
    def __init__(self, app: QtWidgets.QApplication, view: View, model: Model):
        self._app = app
        self._view = view
        self._model = model
        # Connect to view events
        self._view.events.app_exit.connect(self.on_view_app_exit)
        self._view.events.edit_undo.connect(self.on_view_undo)
        self._view.events.edit_redo.connect(self.on_view_redo)
        self._view.events.files_open.connect(self.on_view_files_open)
        # self.view.events.files_close_all.connect(self.on_view_files_close_all)
        # self.view.events.files_current_changed.connect(self.on_view_files_curr_changed)
        self._view.events.object_created.connect(self.on_view_object_created)
        self._view.events.object_removed.connect(self.on_view_object_removed)
        # self.view.events.object_current_changed.connect(self.on_view_obejct_curr_changed)
        # self.view.events.keypoint_current_changed.connect(self.on_view_keypoint_cur_changed)
        # self.view.events.keypoint_disabled.connect(self.on_view_keypoint_disabled)
        # self.view.events.canvas_mouse_left_clicked.connect(self.on_view_canvas_mouse_left_clicked)
        # self.view.events.canvas_mouse_right_clicked.connect(self.on_view_canvas_mouse_right_clicked)
        self._initialize()

    def _initialize(self):
        classes = self._model.get_object_classes_list(full_info=True)
        self._view.set_object_classes(classes)

    def on_view_files_open(self, files: List[str]):
        self._model.set_files(files)
        actual_files = self._model.get_files()
        self._view.set_files_list(actual_files)

        self._view.clear_canvas()
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            if self._view.set_canvas_image(cur_ctx.get().get_fname()):
                self._view.repaint_canvas()
                objs = cur_ctx.get().get_objects_list()
                self._view.set_objects_list(objs)
                # TODO:
                # cur_obj = cur_ctx.get().get_current_object()
                # if cur_obj is not None:
                #     keypoints = list(cur_obj.shape.keypoints.keys())
                #     self.view.set_keypoints_list(keypoints)
                # else:
                #     self.view.set_keypoints_list([])

    # def on_view_files_close_all(self):
    #     self.model.set_files([], ignore_empty=False)
    #     actual_files = self.model.get_files()
    #     self.view.set_files_list(actual_files)
    #     self.view.clear_background()
    #     self.view.repaint_background()
    #     self.view.set_objects_list([])
    #     self.view.set_keypoints_list([])

    # def on_view_files_curr_changed(self, curr_idx: int):
    #     if curr_idx != self.model.get_curr_file_idx():
    #         if self.model.set_curr_file_idx(curr_idx):
    #             pass
    #     # TODO: избыточная перерисовка?
    #     curr_ctx = self.model.get_current_file_context()
    #     if curr_ctx is not None:
    #         self.view.set_background_image(curr_ctx.get().fname)
    #         self.view.repaint_background()
    #         objects = [str(obj) for obj in curr_ctx.get().objects]
    #         self.view.set_objects_list(objects)
    #         cur_obj = curr_ctx.get().get_current_object()
    #         if cur_obj is not None:
    #             keypoints = list(cur_obj.shape.keypoints.keys())
    #             self.view.set_keypoints_list(keypoints)
    #         else:
    #             self.view.set_keypoints_list([])

    def on_view_object_created(self, class_idx: int):
        if self._model.create_object(class_idx):
            cur_ctx = self._model.get_current_context()
            if cur_ctx is not None:
                objs = cur_ctx.get().get_objects_list()
                self._view.set_objects_list(objs)
                # TODO:
                # cur_obj = cur_ctx.get().get_current_object()
                # if cur_obj is not None:
                #     keypoints = list(cur_obj.shape.keypoints.keys())
                #     self.view.set_keypoints_list(keypoints)
                # else:
                #     self.view.set_keypoints_list([])

    def on_view_object_removed(self, idx: int):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            if cur_ctx.get().remove_object(idx):
                objs = cur_ctx.get().get_objects_list()
                self._view.set_objects_list(objs)
                # TODO:
                # cur_obj = curr_ctx.get().get_current_object()
                # if cur_obj is not None:
                #     keypoints = list(cur_obj.shape.keypoints.keys())
                #     self.view.set_keypoints_list(keypoints)
                # else:
                #     self.view.set_keypoints_list([])

    # def on_view_obejct_curr_changed(self, curr_idx: int):
    #     curr_ctx = self.model.get_current_file_context()
    #     if curr_ctx is not None:
    #         if curr_ctx.get().set_curr_object_idx(curr_idx):
    #             cur_obj = curr_ctx.get().get_current_object()
    #             if cur_obj is not None:
    #                 keypoints = list(cur_obj.shape.keypoints.keys())
    #                 self.view.set_keypoints_list(keypoints)
    #             else:
    #                 self.view.set_keypoints_list([])

    # def on_view_keypoint_cur_changed(self, cur: int):
    #     cur_ctx = self.model.get_current_file_context()
    #     if cur_ctx is not None:
    #         cur_obj = cur_ctx.get().get_current_object()
    #         if cur_obj is not None:
    #             if cur_obj.shape.set_curr_keypoint_idx(cur):
    #                 pass
    #                 # TODO: draw on canvas current keypoint...
    #                 # TODO: get_curr_keypoint()
    #                 self.view.repaint_background() # TODO: or repaint only GL painter layer ?

    #             pt = cur_obj.shape.get_current_keypoint()
    #             if pt is not None:
    #                 print(f"CUR KEYPOINT: {cur}, POS: {pt.x}, {pt.y}")

    # def on_view_keypoint_disabled(self):
    #     cur_ctx = self.model.get_current_file_context()
    #     if cur_ctx is not None:
    #         cur_obj = cur_ctx.get().get_current_object()
    #         if cur_obj is not None:
    #             cur_obj.shape.disable_cur_keypoint()
    #             self.view.repaint_background()

    # def on_view_canvas_mouse_left_clicked(self, pos: Tuple[int, int]):
    #     print("LEFT CLICKED: ", pos)
    #     cur_ctx = self.model.get_current_file_context()
    #     if cur_ctx is not None:
    #         cur_obj = cur_ctx.get().get_current_object()
    #         if cur_obj is not None:
    #             cur_obj.shape.set_curr_keypoint(pos)
    #             self.view.set_drawables([DrawKeypoints(cur_obj.shape)])
    #             self.view.repaint_background() # TODO: or repaint only GL painter layer ?

    # def on_view_canvas_mouse_right_clicked(self, pos: Tuple[int, int]):
    #     print("RIGHT CLICKED: ", pos)
    #     cur_ctx = self.model.get_current_file_context()
    #     if cur_ctx is not None:
    #         cur_obj = cur_ctx.get().get_current_object()
    #         if cur_obj is not None:
    #             cur_obj.shape.set_curr_keypoint_idx_by_coords(pos[0], pos[1])
    #             # self.view.set_drawables([DrawKeypoints(cur_obj.shape)])
    #             self.view.set_curent_keypoint(cur_obj.shape.curr_keypoint_idx)
    #             self.view.repaint_background() # TODO: or repaint only GL painter layer ?

    def on_view_app_exit(self):
        self._model.close()
        self._app.closeAllWindows()
        self._app.quit()

    def on_view_undo(self):
        pass

    def on_view_redo(self):
        pass
