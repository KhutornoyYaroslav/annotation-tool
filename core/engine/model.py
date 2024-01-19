from typing import List
from core.utils.basicconfig import Config
from core.engine.context import Context
from core.engine.shapes import ShapeType
from core.engine.object import ObjectFactory
from core.engine.undoredo import UndoRedoContainer


class Model():
    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._cur_file_idx = 0
        self._file_contexts: List[UndoRedoContainer[Context]] = []
        self._object_factory = ObjectFactory()
        self._initialize()

    def _initialize(self):
        for obj_class in self._cfg.annotation.classes:
            shape_types = []
            for sname in obj_class.shapes:
                stype = ShapeType.from_str(sname)
                if stype != None:
                    shape_types.append(stype)
            if len(shape_types):
                self._object_factory.register_class(obj_class.name, shape_types)

    def get_object_classes_list(self, full_info: bool = False) -> List[str]:
        return self._object_factory.get_registered_classes(full_info)

    def create_object(self, class_idx: int) -> bool:
        cur_ctx = self.get_current_context()
        if cur_ctx is not None:
            class_name = self._object_factory.get_registered_classes()[class_idx]
            obj = self._object_factory.create_object(class_name)
            if obj is not None:
                cur_ctx.get().append_object(obj)
                return True

        return False

    def save_all(self):
        for ctx in self._file_contexts:
            if not ctx.get().is_empty():
                ctx.get().save()

    def close(self):
        # self.save_all() # TODO: uncomment later
        self._file_contexts.clear()
        self._cur_file_idx = 0

    def set_files(self, files: List[str], ignore_empty: bool = True):
        if ignore_empty and not files:
            return

        files_filtered = []
        for file in files:
            if file.endswith(tuple(self._cfg.files.valid_extensions)):
                files_filtered.append(file)

        # self.save_all() # TODO: uncomment later
        self._file_contexts.clear()
        for file in files_filtered:
            context = UndoRedoContainer()
            context.add_action(Context(file))
            self._file_contexts.append(context)
        self._cur_file_idx = 0

    def get_files(self) -> List[str]:
        files = []
        for ctx in self._file_contexts:
            files.append(ctx.get().get_fname())

        return files

    def get_current_context(self):
        if not self._file_contexts:
            return None

        return self._file_contexts[self._cur_file_idx]

    def set_current_file_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self._file_contexts):
            self._cur_file_idx = idx
            return True

        return False

    def get_current_file_idx(self) -> int:
        return self._cur_file_idx
