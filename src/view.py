from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic


class View(QMainWindow):
    def __init__(self):
        """
        Constructor for the class
        """
        super(View, self).__init__()

        # ** Load UI from Qt 5 Designer file **
        self.ui = uic.loadUi("ui/wndmain.ui", self)

    def closeEvent(self, event):
        """
        Event for when closing the window, either by menu or by close button
        :return:
        """
        # Write current configuration before closing
        event.accept()
