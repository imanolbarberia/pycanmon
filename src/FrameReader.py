from PyQt5 import QtCore
import time


class FrameReaderSignals(QtCore.QObject):
    frameReceived = QtCore.pyqtSignal(list)
    workStarted = QtCore.pyqtSignal()
    workStopped = QtCore.pyqtSignal()


class FrameReader(QtCore.QRunnable):
    signals = FrameReaderSignals()

    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        pass


class DummyFrameReader(FrameReader):
    def __init__(self):
        super().__init__()
        self.running = False

    @QtCore.pyqtSlot()
    def run(self):
        self.running = True
        self.signals.workStarted.emit()

        counter = 0

        while self.running:
            self.signals.frameReceived.emit(
                [0x350, 3, [1, 2, 3], time.time()]
            )

            if counter % 2 == 1:
                self.signals.frameReceived.emit(
                    [0x535, 0, [], time.time()]
                )

            if counter % 5 == 0:
                self.signals.frameReceived.emit(
                    [0x788, 8, [0x12, 0x23, 0x34, 0x45, 0x56, 0x67, 0x78, 0x89, 0x9a], time.time()]
                )

            time.sleep(0.1)
            counter += 1

        self.signals.workStopped.emit()

    def stop(self):
        self.running = False


class FileFrameReader(FrameReader):
    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        pass


class CANFrameReader(FrameReader):
    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        pass

