"""
FrameSources.py

Frame source classes are defined here. Frame sources are objects that somehow "produce" CAN frames (either by reading
CAN bus directly, or from a file, or...) and notify that frame via a PyQt5 signal.
"""
from PyQt5 import QtCore
import time


class FrameSourceSignals(QtCore.QObject):
    """
    Signals for the FrameSource class
    """
    frame_ready = QtCore.pyqtSignal(dict)
    work_started = QtCore.pyqtSignal()
    work_stopped = QtCore.pyqtSignal()


class FrameSource(QtCore.QRunnable):
    """
    Base FrameSource class, that is a runnable that emits frame signals
    """

    signals = FrameSourceSignals()

    def __init__(self):
        """
        Class constructor, call first QObject constructor and then QRunnable constructor
        """
        super().__init__()

        self.running = False

    def run(self):
        """
        Inherited method from QRunnable. This method is called from a Threadpool to be run in background
        :return: Nothing
        """
        self.running = True

        """ Emit the 'work_started' signal """
        self.signals.work_started.emit()

        while self.running:
            pass

        """ Emit the 'work_stopped signal' """
        self.signals.work_stopped.emit()

    def stop(self):
        """
        Mark the object as not running
        :return:
        """
        self.running = False

    def is_running(self):
        """
        Return if the runnable is currently running or not
        :return:
        """
        return self.running


class DummyFrameSource(FrameSource):
    """
    Dummy Frame source that produces always the same hardcoded frames, just made for testing
    """

    def __init__(self):
        """
        Class constructor
        """
        super().__init__()

    def run(self):
        self.running = True
        self.signals.work_started.emit()

        counter = 0

        while self.running:
            self.signals.frame_ready.emit(
                {"id": 0x350,
                 "data": [1, 2, 3],
                 "flags": [],
                 "tstamp": time.time()}
            )

            if counter % 2 == 1:
                self.signals.frame_ready.emit(
                    {"id": 0x535,
                     "data": [],
                     "flags": [],
                     "tstamp": time.time()}
                )

            if counter % 5 == 0:
                self.signals.frame_ready.emit(
                    {"id": 0x788,
                     "data": [0x12, 0x23, 0x34, 0x45, 0x56, 0x67, 0x78, 0x89, 0x9a],
                     "flags": [],
                     "tstamp": time.time()}
                )

            time.sleep(0.1)
            counter += 1

        self.signals.work_stopped.emit()
