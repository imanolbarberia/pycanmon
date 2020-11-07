from PyQt5 import QtCore
from FrameSources import FrameSource
import time


class Model(QtCore.QAbstractTableModel):
    """
    Model class
    """

    frame_source_changed = QtCore.pyqtSignal()
    frame_received = QtCore.pyqtSignal(dict)

    header_lables = ["Timestamp", "CAN ID", "DLC", "D0 | D1 | D2 | D3 | D4 | D5 | D6 | D7"]

    def __init__(self):
        """
        Class initialization
        """
        super().__init__()
        self.listening = False
        self.frames_list = []
        self.thpool = QtCore.QThreadPool()
        self.frame_source = None

    def add_frame(self, frm: dict):
        """
        Add a frame to the data set
        :param frm: Frame to be added. Dictionary type with this format:
                {'id': id, 'data': [data], 'flags': [flags], 'tstamp': tstamp}
        :return: True if the frame was correct and was added, False otherwise
        """

        if type(frm) != dict:
            ret = False
        else:
            id_list = [el["id"] for el in self.frames_list]

            if frm["id"] in id_list:
                """
                If element exists already, just update it
                """
                pos = id_list.index(frm["id"])
                self.frames_list[pos] = frm

            else:
                """
                If element does not exist, add it
                """
                self.frames_list += [frm]

            ret = True
            """ Emit the signal noting that the layout has changed """
            self.layoutChanged.emit()
            self.frame_received.emit(frm)

        return ret

    def del_frame(self, frm_id: int):
        """
        Remove frame from the frames list. If
        :param frm_id:
        :return:
        """
        id_list = [el["id"] for el in self.frames_list]

        if frm_id in id_list:
            """
            frame ID is in the list
            """
            pos = id_list.index(frm_id)
            self.frames_list.pop(pos)
            ret = True

            """ Emit the signal noting that the layout has changed """
            self.layoutChanged.emit()

        else:
            """
            frame ID is not on the list, nothing to remove
            """
            ret = False

        return ret

    def get_frame(self, frm_id: int):
        """
        Return the frame specified by ID
        :param frm_id: ID of the frame to return
        :return: Required frame, or None if ID is not valid
        """
        id_list = [el["id"] for el in self.frames_list]

        if frm_id in id_list:
            """
            frame ID is in the list
            """
            pos = id_list.index(frm_id)
            ret = self.frames_list[pos]

        else:
            """
            frame ID is not on the list, nothing to remove
            """
            ret = None

        return ret

    def get_frames(self):
        """
        Return list of current frames
        :return: List of frames
        """
        return self.frames_list

    def set_frame_src(self, src: FrameSource):
        """
        Set frame source, where the frames will be coming from
        :param src: FrameSource type object (or inherited)
        """
        self.frame_source = src
        self.frame_source_changed.emit()

    def get_frame_src(self):
        """
        Returns the currently selected frame source
        :return: FrameSource type object
        """
        return self.frame_source

    @QtCore.pyqtSlot()
    def frame_source_started(self):
        self.listening = True

    @QtCore.pyqtSlot()
    def frame_source_stopped(self):
        self.listening = False

    def start_listening(self):
        """
        Starts to run the frame source as a separate thread and connects signals

        :return: True if the thread started correctly, False otherwise
        """
        if self.frame_source is None:
            """ 
            No frame source defined
            """
            ret = False

        elif self.frame_source.is_running():
            """
            If the frame source is already running, just don't start again
            """
            ret = False

        else:
            """
            Frame source selected
            """

            """ Connect signals and start running """
            self.frame_source.signals.work_started.connect(self.frame_source_started)
            self.frame_source.signals.work_stopped.connect(self.frame_source_stopped)
            self.frame_source.signals.frame_ready.connect(self.add_frame)
            self.thpool.start(self.frame_source)

            ret = True

        return ret

    def stop_listening(self):
        """
        Stops listening to frames

        :return: True if the thread was running, False otherwise
        """

        if self.frame_source is None:
            """
            If no frame source defined, none to stop
            """
            ret = False

        elif not self.listening:
            """
            If the current source is not emitting frames, just don't stop anything...
            """
            ret = False

        else:
            """
            Otherwise
            """

            """ Disconnect signals """
            self.frame_source.signals.work_started.disconnect(self.frame_source_started)
            self.frame_source.signals.work_stopped.disconnect(self.frame_source_stopped)
            self.frame_source.signals.frame_ready.disconnect(self.add_frame)
            self.frame_source.stop()

            """ Just wait until it safely stops """
            while self.frame_source.is_running() or self.listening is True:
                pass

    def is_listening(self):
        """
        Return if the current source is listening
        :return: True if it is listening, False otherwise
        """
        return self.listening

    def data(self, index, role=None):
        """
        Inherited from QAbstractTableModel, used to display data in a proper view
        :param index:
        :param role:
        :return:
        """
        col = index.column()
        row = index.row()
        if role == QtCore.Qt.TextAlignmentRole and col != 3:
            """
            Handle text alignment
            """
            ret = QtCore.Qt.AlignCenter

        elif role == QtCore.Qt.DisplayRole:
            """
            Handle data display
            """
            frm = self.frames_list[row]

            if col == 0:
                # Timestamp column
                tstamp = frm["tstamp"]
                msec = repr(tstamp).split(".")[1][:3]
                ret = time.strftime("%H:%M:%S.{}".format(msec), time.localtime(tstamp))

            elif col == 1:
                # ID columns
                ret = "{:02X}".format(frm["id"])

            elif col == 2:
                # DLC column
                ret = len(frm["data"])

            elif col == 3:
                # Data column
                ret = " | ".join("{:02X}".format(b) for b in frm["data"])

            else:
                # Unexpected column
                ret = None

        else:
            """
            Handle other data roles
            """
            ret = None

        return ret

    def rowCount(self, parent=None, *args, **kwargs):
        """
        Inherited from QAbstractModel. Used for counting rows to display.
        :param parent:
        :param args:
        :param kwargs:
        :return:
        """
        return len(self.frames_list)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        Inherited from QAbstractModel. Used for counting columns to display.
        :param parent:
        :param args:
        :param kwargs:
        :return:
        """
        if len(self.frames) > 0:
            ret = len(self.frames_list[0])
        else:
            ret = 0

        return ret

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """
        Inherited from QAbstractModel. Used for counting columns to display.
        :param section:
        :param orientation:
        :param role:
        :return:
        """
        if role == QtCore.Qt.DisplayRole:
            ret = self.header_lables[section]

        else:
            ret = QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

        return ret
