import sys
from PyQt5 import QtWidgets
from core.ui.view import View
from core.engine.model import Model
from core.controller.controller import Controller


def main() -> int:
    app = QtWidgets.QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(app, view, model)
    view.initGUI()
    view.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
