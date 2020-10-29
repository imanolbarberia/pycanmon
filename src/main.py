#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication
from controller import Controller
from view import View
from model import Model


def main():
    app = QApplication(sys.argv)
    model = Model()
    view = View(model)
    ctrl = Controller(model, view)

    ctrl.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
