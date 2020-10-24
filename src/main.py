#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QApplication
from view import View


def main():
    app = QApplication(sys.argv)
    view = View()

    view.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
