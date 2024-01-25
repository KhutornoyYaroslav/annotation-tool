from typing import List, Tuple
from PyQt5.QtCore import QPoint
from core.ui.view import View
from core.engine.model import Model


class Controller():
    def __init__(self, view: View, model: Model):
        self._draw_all_objects = False
        self._autofocus_on_current_object = False
        # Model, view instances
        self._view = view
        self._model = model
        # Connect to view events
        self._view.events.app_exit.connect(self.on_view_app_exit)
        self._view.events.edit_undo.connect(self.on_view_undo)
        self._view.events.edit_redo.connect(self.on_view_redo)
        self._view.events.files_open.connect(self.on_view_files_open)
        self._view.events.files_close_all.connect(self.on_view_files_close_all)
        self._view.events.files_current_changed.connect(self.on_view_files_current_changed)
        self._view.events.object_created.connect(self.on_view_object_created)
        self._view.events.object_removed.connect(self.on_view_object_removed)
        self._view.events.object_current_changed.connect(self.on_view_obejct_current_changed)
        self._view.events.object_draw_all_changed.connect(self.on_view_object_draw_all_changed)
        self._view.events.object_autofocus_changed.connect(self.on_view_object_autofocus_changed)
        self._view.events.shapes_current_item_changed.connect(self.on_shapes_current_item_changed)
        self._view.events.shapes_current_item_disabled.connect(self.on_shapes_current_item_disabled)
        self._view.events.shapes_next_item_requested.connect(self.on_shapes_next_item_requested)
        self._view.events.shapes_autoannotate_requested.connect(self.on_shapes_autoannotate_requested)
        self._view.events.canvas_mouse_left_clicked.connect(self.on_view_canvas_mouse_left_clicked)
        self._view.events.canvas_mouse_right_clicked.connect(self.on_view_canvas_mouse_right_clicked)
        self._initialize()

    def _initialize(self):
        classes = self._model.get_object_classes_list(full_info=True)
        self._view.set_object_classes(classes)

    def _update_view_objects(self): # TODO: decompose on independant methods (objects / shapes / drawing)
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            # List of objects
            objs = cur_ctx.get().get_objects_list()
            cur_obj_idx = cur_ctx.get().get_current_object_idx()
            self._view.set_objects_list(objs, cur_obj_idx)
            # Current object shapes
            cur_obj = cur_ctx.get().get_current_object()
            if cur_obj is not None:
                self._view.set_object_shapes(cur_obj.get_shapes_info(), cur_obj.get_current_shape_idx(), cur_obj.get_current_shape().get_current_point_idx())
            else:
                self._view.set_object_shapes({}, 0, 0)
            # Drawing
            shapes_to_draw = []
            if self._draw_all_objects:
                for obj in cur_ctx.get().get_objects():
                    shapes_to_draw.extend(obj.get_shapes())
            else:
                if cur_obj is not None:
                    # shapes_to_draw.append(cur_obj.get_current_shape())
                    shapes_to_draw.extend(cur_obj.get_shapes())
            self._view.set_drawables(shapes_to_draw)
            # Autofocusing on object
            if self._autofocus_on_current_object:
                if cur_obj is not None:
                    brect = cur_obj.get_shapes_bounding_rect()
                    if brect is not None:
                        self._view.set_canvas_focus(brect)

            self._view.repaint_canvas()
        else:
            self._view.set_objects_list([], 0)
            self._view.set_object_shapes({}, 0, 0)
            self._view.set_drawables([])
            self._view.clear_canvas()
            self._view.repaint_canvas()

    def on_view_files_open(self, files: List[str]):
        self._model.set_files(files)
        # Files
        actual_files = self._model.get_files()
        self._view.set_files_list(actual_files)
        # Canvas
        self._view.clear_canvas()
        self._view.repaint_canvas()
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            img = cur_ctx.get().get_image()
            if img is not None:
                self._view.set_canvas_image(img)
                # self._view.repaint_canvas()
                # # Objects
                # objs = cur_ctx.get().get_objects_list()
                # self._view.set_objects_list(objs, cur_ctx.get().get_current_object_idx())
                # # Shapes
                # shapes = {}
                # cur_obj = cur_ctx.get().get_current_object()
                # if cur_obj is not None:
                #     shapes = cur_obj.get_shapes_info()
                # self._view.set_object_shapes(shapes)
                self._update_view_objects()

    def on_view_files_close_all(self):
        self._model.close()
        # Files
        actual_files = self._model.get_files()
        self._view.set_files_list(actual_files)
        # Canvas
        # self._view.set_drawables([])
        # self._view.clear_canvas()
        # self._view.repaint_canvas()
        # # Objects
        # self._view.set_objects_list([])
        # # Shapes
        # self._view.set_object_shapes({})
        self._update_view_objects()

    def on_view_files_current_changed(self, cur_idx: int):
        if cur_idx != self._model.get_current_file_idx():
            if self._model.set_current_file_idx(cur_idx):
                cur_ctx = self._model.get_current_context()
                if cur_ctx is not None:
                    # Canvas
                    img = cur_ctx.get().get_image()
                    if img is not None:
                        self._view.set_canvas_image(img)
                    # # Objects
                    # objs = cur_ctx.get().get_objects_list()
                    # self._view.set_objects_list(objs, cur_ctx.get().get_current_object_idx())
                    # # Shapes
                    # shapes = {}
                    # cur_obj = cur_ctx.get().get_current_object()
                    # if cur_obj is not None:
                    #     shapes = cur_obj.get_shapes_info()
                    #     if self._draw_all_objects:
                    #         self._view.set_drawables(cur_obj.get_shapes()) # TODO: надо отрисовывать не только все шэйпы текущего объекта, но и и всех объектов
                    #     else:
                    #         self._view.set_drawables([cur_obj.get_current_shape()])
                    # else:
                    #     self._view.set_drawables([])
                    # self._view.set_object_shapes(shapes)
                    # self._view.repaint_canvas()
                    self._update_view_objects()

    def on_view_object_created(self, class_idx: int):
        if self._model.create_object(class_idx):
            # cur_ctx = self._model.get_current_context()
            # if cur_ctx is not None:
            #     # Objects
            #     objs = cur_ctx.get().get_objects_list()
            #     self._view.set_objects_list(objs, cur_ctx.get().get_current_object_idx())
            #     # Shapes
            #     shapes = {}
            #     cur_obj = cur_ctx.get().get_current_object()
            #     if cur_obj is not None:
            #         shapes = cur_obj.get_shapes_info()
            #         if self._draw_all_objects:
            #             self._view.set_drawables(cur_obj.get_shapes())
            #         else:
            #             self._view.set_drawables([cur_obj.get_current_shape()])
            #         self._view.repaint_canvas()
            #     self._view.set_object_shapes(shapes)
            self._update_view_objects()

    def on_view_object_removed(self, idx: int):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            if cur_ctx.get().remove_object(idx):
                # # Objects
                # objs = cur_ctx.get().get_objects_list()
                # self._view.set_objects_list(objs, cur_ctx.get().get_current_object_idx())
                # # Shapes
                # shapes = {}
                # cur_obj = cur_ctx.get().get_current_object()
                # if cur_obj is not None:
                #     shapes = cur_obj.get_shapes_info()
                #     if self._draw_all_objects:
                #         self._view.set_drawables(cur_obj.get_shapes())
                #     else:
                #         self._view.set_drawables([cur_obj.get_current_shape()])
                # else:
                #     self._view.set_drawables([])
                # self._view.repaint_canvas()
                # self._view.set_object_shapes(shapes)
                self._update_view_objects()
                cur_ctx.get().save()

    def on_view_obejct_current_changed(self, cur_idx: int):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            if cur_ctx.get().set_curr_object_idx(cur_idx):
                # # Shapes
                # cur_obj = cur_ctx.get().get_current_object()
                # if cur_obj is not None:
                #     shapes = cur_obj.get_shapes_info()
                #     shape = cur_obj.get_current_shape()
                #     self._view.set_object_shapes(shapes, cur_obj.get_current_shape_idx(), shape.get_current_point_idx())
                #     if self._draw_all_objects:
                #         self._view.set_drawables(cur_obj.get_shapes())
                #     else:
                #         self._view.set_drawables([cur_obj.get_current_shape()])
                # else:
                #     self._view.set_object_shapes([])
                # self._view.repaint_canvas()
                self._update_view_objects()

    def on_view_object_draw_all_changed(self, state: bool):
        self._draw_all_objects = state
        # cur_ctx = self._model.get_current_context()
        # if cur_ctx is not None:
        #     if state:
        #         shapes = []
        #         for obj in cur_ctx.get().get_objects():
        #             shapes.extend(obj.get_shapes())
        #         self._view.set_drawables(shapes)
        #     else:
        #         cur_obj = cur_ctx.get().get_current_object()
        #         if cur_obj is not None:
        #             self._view.set_drawables([cur_obj.get_current_shape()])
        #     self._view.repaint_canvas()
        self._update_view_objects()

    def on_view_object_autofocus_changed(self, state: bool):
        self._autofocus_on_current_object = state
        self._update_view_objects()

    def on_shapes_current_item_changed(self, shape_idx: int, point_idx: int):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            cur_obj = cur_ctx.get().get_current_object()
            if cur_obj is not None:
                if cur_obj.set_current_shape_idx(shape_idx):
                    shape = cur_obj.get_current_shape()
                    if shape.set_current_point_idx(point_idx):
                        # if self._draw_all_objects:
                        #     self._view.set_drawables(cur_obj.get_shapes())
                        # else:
                        #     self._view.set_drawables([cur_obj.get_current_shape()])
                        # self._view.repaint_canvas()
                        self._update_view_objects() # TODO: избыточно точно ?

    def on_shapes_current_item_disabled(self):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            cur_obj = cur_ctx.get().get_current_object()
            if cur_obj is not None:
                shape = cur_obj.get_current_shape()
                shape.disable_current_point()
                shapes = cur_obj.get_shapes_info()
                self._view.set_object_shapes(shapes, cur_obj.get_current_shape_idx(), shape.get_current_point_idx())
                self._view.repaint_canvas()
                # self._update_view_objects()
                cur_ctx.get().save()

    def on_shapes_next_item_requested(self):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            cur_obj = cur_ctx.get().get_current_object()
            if cur_obj is not None:
                shape = cur_obj.get_current_shape()
                shape.to_next_point()
                shapes = cur_obj.get_shapes_info()
                self._view.set_object_shapes(shapes, cur_obj.get_current_shape_idx(), shape.get_current_point_idx())
                self._view.repaint_canvas()
                # self._update_view_objects()

    def on_shapes_autoannotate_requested(self):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            cur_obj = cur_ctx.get().get_current_object()
            if cur_obj is not None:
                if cur_obj.annotate_brect(cur_ctx.get().get_image()):
                    self._update_view_objects()
                    cur_ctx.get().save()

    def on_view_canvas_mouse_left_clicked(self, pos: Tuple[int, int]):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            cur_obj = cur_ctx.get().get_current_object()
            if cur_obj is not None:
                shape = cur_obj.get_current_shape()
                shape.on_left_mouse_clicked(QPoint(*pos))
                shapes = cur_obj.get_shapes_info()
                self._view.set_object_shapes(shapes, cur_obj.get_current_shape_idx(), shape.get_current_point_idx())
                self._view.repaint_canvas()
                # self._update_view_objects()
                cur_ctx.get().save()

    def on_view_canvas_mouse_right_clicked(self, pos: Tuple[int, int]):
        cur_ctx = self._model.get_current_context()
        if cur_ctx is not None:
            cur_obj = cur_ctx.get().get_current_object()
            if cur_obj is not None:
                shape = cur_obj.get_current_shape()
                shape.on_right_mouse_clicked(QPoint(*pos))
                self._view.repaint_canvas()
                self._view.set_shapes_curent_item(cur_obj.get_current_shape_idx(), shape.get_current_point_idx())
                # self._update_view_objects()

    def on_view_app_exit(self):
        self._model.close()
        self._view.close()

    def on_view_undo(self):
        pass

    def on_view_redo(self):
        pass
