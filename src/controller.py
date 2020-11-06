from model import Model
from view import View
from PyQt5.QtCore import QThreadPool
from FrameReader import DummyFrameReader
from eventmsgs import EventMsgs


class Controller:
    def __init__(self, mdl: Model, vw: View):
        super(Controller, self).__init__()
        self.model = mdl
        self.view = vw

        self.fr_reader = None
        self.thpool = QThreadPool()

        # Connect button activation to function
        self.view.eventMsg.connect(self.process_event_msg)

    def run(self):
        self.view.show()

    def process_event_msg(self, msg, largs):
        if msg == EventMsgs.MSG_APP_CLOSE:
            pass
        elif msg == EventMsgs.MSG_BTN_CLICKED:
            self.activate()
        else:
            pass

    def activate(self):
        if self.fr_reader is None:
            self.fr_reader = DummyFrameReader()

            self.fr_reader.setAutoDelete(True)

            self.fr_reader.signals.workStarted.connect(self.on_reader_start)
            self.fr_reader.signals.workStopped.connect(self.on_reader_stop)
            self.fr_reader.signals.frameReceived.connect(self.on_frame_ready)
            self.thpool.start(self.fr_reader)
        else:
            self.fr_reader.stop()
            self.fr_reader = None

    @staticmethod
    def on_reader_start():
        print("[CTRL]: Reader started!")

    @staticmethod
    def on_reader_stop():
        print("[CTRL]: Reader stopped!")

    def on_frame_ready(self, frm):
        self.model.add_frame(frm)
