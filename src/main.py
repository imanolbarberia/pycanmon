#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from FrameSources import FrameSource, DummyFrameSource
from PyQt5 import QtCore
from Model import Model
import sys


def print_frm(frm):
    print("Frame: {}".format(frm))


def main():
    app = QApplication(sys.argv)

    a = Model()
    a.set_frame_src(DummyFrameSource())
    a.frame_received.connect(print_frm)
    a.start_listening()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
