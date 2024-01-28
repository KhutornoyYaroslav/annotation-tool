from typing import List
from core.utils.basicconfig import Config
from core.engine.context import Context
from core.engine.undoredo import UndoRedoContainer
from core.engine.objects import build_object_factory


class Model():
    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._cur_file_idx = 0
        self._file_contexts: List[UndoRedoContainer[Context]] = []
        self._object_factory = build_object_factory(cfg)

    def get_object_classes_list(self, full_info: bool = False) -> List[str]:
        return self._object_factory.get_registered_classes_info(full_info)

    def create_object(self, class_idx: int) -> bool:
        cur_ctx = self.get_current_context()
        if cur_ctx is not None:
            class_name = self._object_factory.get_registered_classes_info()[class_idx]
            obj = self._object_factory.create_object(class_name)
            if obj is not None:
                cur_ctx.get().append_object(obj)
                return True

        return False

    def save_all(self):
        for ctx in self._file_contexts:
            # if not ctx.get().is_empty():
            ctx.get().save()

    def load_all(self):
        for ctx in self._file_contexts:
            ctx.get().load()

    def close(self):
        self.save_all()
        self._file_contexts.clear()
        self._cur_file_idx = 0

    def set_files(self, files: List[str], ignore_empty: bool = True):
        if ignore_empty and not files:
            return

        files_filtered = []
        for file in files:
            if file.endswith(tuple(self._cfg.files.valid_extensions)):
                files_filtered.append(file)

        self.save_all()
        self._file_contexts.clear()
        for file in files_filtered:
            context = UndoRedoContainer()
            context.add_action(Context(file, object_factory=self._object_factory))
            self._file_contexts.append(context)
        self._cur_file_idx = 0
        self.load_all()

    def get_files(self) -> List[str]:
        files = []
        for ctx in self._file_contexts:
            files.append(ctx.get().get_fname())

        return files

    def get_contexts(self) -> List[UndoRedoContainer[Context]]:
        return self._file_contexts

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
