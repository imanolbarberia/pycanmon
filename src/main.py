#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from View import View
from Model import Model
import sys


def main():
    app = QApplication(sys.argv)

    model = Model()
    view = View(model)
    view.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
