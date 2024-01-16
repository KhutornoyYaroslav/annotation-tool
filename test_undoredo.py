from core.engine.undoredo import UndoRedoContainer


def main():

    items = UndoRedoContainer(10)
    print(items.get(), items.curr_idx)
    items.add_action(0)
    print(items.get(), items.curr_idx)
    items.add_action(1)
    print(items.get(), items.curr_idx)
    items.add_action(2)
    print(items.get(), items.curr_idx)
    items.undo()
    print(items.get(), items.curr_idx)
    items.undo()
    print(items.get(), items.curr_idx)
    items.add_action(3)
    print(items.get(), items.curr_idx)
    items.redo()
    print(items.get(), items.curr_idx)
    items.undo()
    print(items.get(), items.curr_idx)

if __name__ == '__main__':
    main()