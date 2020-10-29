from PyQt5.QtCore import QObject, pyqtSignal


class ModelSignals(QObject):
    data_updated = pyqtSignal()


class Model:
    def __init__(self):
        self.signals = ModelSignals()
        self.mat = []

    def add_frame(self, fr):
        self.mat += fr
        self.signals.data_updated.emit()

    def get_values(self):
        return self.mat
