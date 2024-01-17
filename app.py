import sys
import argparse
from PyQt5 import QtWidgets
from core.config import cfg
from core.ui.view import View
from core.engine.model import Model
from core.controller.controller import Controller


def main() -> int:
    # Parse arguments
    parser = argparse.ArgumentParser(description='Annotation tools application')
    parser.add_argument("--config-file", dest="config_file", required=False, type=str, default="config.json",
                        help="Path to config file")
    args = parser.parse_args()

    # Read config
    cfg.save('config_defaults.json')
    cfg.load(args.config_file)
    cfg.lock()

    # Run app
    app = QtWidgets.QApplication(sys.argv)
    model = Model(cfg)
    view = View(cfg)
    controller = Controller(app, view, model)
    view.initGUI()
    view.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
