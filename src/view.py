from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import uic
from model import Model


class View(QMainWindow):
    onTestBtnClicked = pyqtSignal()

    def __init__(self, mdl: Model):
        """
        Constructor for the class
        """
        super(View, self).__init__()

        # Set model
        self.model = mdl

        # ** Load UI from Qt 5 Designer file **
        self.ui = uic.loadUi("ui/wndmain.ui", self)
        self.model.signals.data_updated.connect(self.display_values)
        self.ui.btnTest.clicked.connect(self.onTestBtnClicked.emit)

    def closeEvent(self, event):
        """
        Event for when closing the window, either by menu or by close button
        :return:
        """
        # Write current configuration before closing
        event.accept()

    def display_values(self):
        print("[VIEW]: {}".format(self.model.get_values()))
