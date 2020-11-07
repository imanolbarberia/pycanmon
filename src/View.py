from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic, QtCore
from Model import Model
from FrameSources import DummyFrameSource


class View(QMainWindow):
    eventMsg = QtCore.pyqtSignal(int, list)

    def __init__(self, mdl: Model):
        """
        Constructor for the class
        """
        super(View, self).__init__()

        # Set model
        self.model = mdl
        self.model.frame_source_changed.connect(self.update_view)

        # ** Load UI from Qt 5 Designer file **
        self.ui = uic.loadUi("ui/wndmain.ui", self)

        # TableView
        self.ui.tblFrames.setModel(self.model)
        self.ui.tblFrames.verticalHeader().hide()
        self.ui.tblFrames.setShowGrid(False)
        self.model.layoutChanged.connect(self.ui.tblFrames.resizeColumnsToContents)

        # Combo Box
        self.ui.cmbFrmSrc.activated.connect(self.on_combo_item_selected)

        # Connect button
        self.ui.btnConnect.clicked.connect(self.on_btnconnect_clicked)

        self.update_view()

    def closeEvent(self, event):
        """
        Event for when closing the window, either by menu or by close button
        :return:
        """
        if self.model.get_frame_src() is not None:
            """
            We have a frame source selected
            """
            if self.model.is_listening():
                """
                Frame listening ongoing, so stop it
                """
                self.model.stop_listening()

                """ Wait until it is finished"""
                while self.model.is_listening():
                    QApplication.processEvents()

            else:
                """
                No frame listening ongoing, we can leave safely
                """
                pass

        else:
            """
            No frame source selected, no problem
            """
            pass

        event.accept()

    def on_combo_item_selected(self, i):
        if i == 0:
            pass
        elif i == 1:
            if type(self.model.get_frame_src()) == DummyFrameSource:
                pass
            else:
                self.model.set_frame_src(DummyFrameSource())

        self.update_view()

    def on_btnconnect_clicked(self):
        if self.model.is_listening():
            self.model.stop_listening()
        else:
            self.model.start_listening()

        self.update_view()

    def update_view(self):
        sources_list = ["<None>", "Dummy"]

        self.ui.cmbFrmSrc.clear()
        self.ui.cmbFrmSrc.addItems(sources_list)

        frmsrc = self.model.get_frame_src()

        if frmsrc is None:
            self.ui.cmbFrmSrc.setCurrentIndex(sources_list.index("<None>"))
        elif type(frmsrc) == DummyFrameSource:
            self.ui.cmbFrmSrc.setCurrentIndex(sources_list.index("Dummy"))
        else:
            pass

        if frmsrc is None:
            self.ui.btnConnect.setEnabled(False)
            self.ui.btnConnect.setText("&Connect")
        else:
            self.ui.btnConnect.setEnabled(True)
            if self.model.is_listening():
                self.ui.btnConnect.setText("&Stop")
                self.ui.tblFrames.setEnabled(True)
            else:
                self.ui.btnConnect.setText("&Connect")
                self.ui.tblFrames.setEnabled(False)
