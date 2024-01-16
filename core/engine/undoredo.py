import copy
from typing import List, TypeVar, Generic


T = TypeVar('T')


class UndoRedoContainer(Generic[T]):
    def __init__(self, max_len: int = 128):
        self.stack = []
        self.curr_idx = None
        self.max_len = max(1, max_len)

    def add_action(self, action: T):
        # Remove elemets after current index
        if self.curr_idx != None:
            end_idx = len(self.stack) - 1
            steps_to_end = end_idx - self.curr_idx
            if steps_to_end > 0:
                remove_from_idx = self.curr_idx + 1
                del self.stack[remove_from_idx : remove_from_idx + steps_to_end]
        
        # Check size and remove oldest element
        if len(self.stack) >= self.max_len:
            del self.stack[0]

        # Add new action
        self.stack.append(copy.deepcopy(action))
        self.curr_idx = len(self.stack) - 1

    def get(self) -> T:
        if self.curr_idx != None and len(self.stack):
            return self.stack[self.curr_idx]
        else:
            return None

    def undo(self):
        if self.curr_idx != None and self.curr_idx > 0:
            self.curr_idx -= 1

    def redo(self):
        if self.curr_idx != None and self.curr_idx < len(self.stack) - 1:
            self.curr_idx += 1

    def clear(self):
        self.stack.clear()
        self.curr_idx = None
