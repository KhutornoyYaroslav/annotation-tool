from typing import List
from core.engine.context import FileContext
from core.engine.undoredo import UndoRedoContainer
from core.config import image_extensions


class Model():
    def __init__(self):
        self.curr_file_idx = 0
        self.file_contexts: List[UndoRedoContainer[FileContext]] = []

    def save_all(self):
        for ctx in self.file_contexts:
            if not ctx.get().is_empty():
                ctx.get().save()

    def close(self):
        self.save_all()
        self.file_contexts.clear()
        self.curr_file_idx = 0

    def set_files(self, files: List[str], ignore_empty: bool = True):
        if ignore_empty and not files:
            return

        files_filtered = []
        for file in files:
            if file.endswith(image_extensions):
                files_filtered.append(file)

        self.save_all()
        self.file_contexts.clear()
        for file in files_filtered:
            context = UndoRedoContainer()
            context.add_action(FileContext(file, try_load=True))
            self.file_contexts.append(context)
        self.curr_file_idx = 0

    def get_files(self) -> List[str]:
        files = []
        for ctx in self.file_contexts:
            files.append(ctx.get().fname)

        return files

    def get_current_file_context(self):
        if not self.file_contexts:
            return None

        return self.file_contexts[self.curr_file_idx]

    def set_curr_file_idx(self, idx: int) -> bool:
        if 0 <= idx < len(self.file_contexts):
            self.curr_file_idx = idx
            return True

        return False

    def get_curr_file_idx(self) -> int:
        return self.curr_file_idx
