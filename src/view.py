from PyQt5.QtWidgets import QMainWindow, QHeaderView
from PyQt5 import uic, QtCore
from model import Model
from eventmsgs import EventMsgs


class View(QMainWindow):
    eventMsg = QtCore.pyqtSignal(int, list)

    def __init__(self, mdl: Model):
        """
        Constructor for the class
        """
        super(View, self).__init__()

        # Set model
        self.model = mdl

        # ** Load UI from Qt 5 Designer file **
        self.ui = uic.loadUi("ui/wndmain.ui", self)

        self.ui.tblFrames.setModel(self.model)
        self.ui.tblFrames.verticalHeader().hide()
        self.ui.tblFrames.setShowGrid(False)
        self.model.layoutChanged.connect(self.ui.tblFrames.resizeColumnsToContents)

        self.ui.btnTest.clicked.connect(lambda: self.eventMsg.emit(EventMsgs.MSG_BTN_CLICKED, []))

    def closeEvent(self, event):
        """
        Event for when closing the window, either by menu or by close button
        :return:
        """

        self.eventMsg.emit(EventMsgs.MSG_APP_CLOSE, [])

        event.accept()
