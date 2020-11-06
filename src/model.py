from PyQt5 import QtCore
import time


class Model(QtCore.QAbstractTableModel):
    """
    Model class for representing a set of CAN frames
    """

    header_lables = ["Timestamp", "CAN ID", "DLC", "D0 | D1 | D2 | D3 | D4 | D5 | D6 | D7"]

    def __init__(self):
        """
        Class initialization
        """
        super().__init__()
        self.frames = {}

    @QtCore.pyqtSlot()
    def data(self, index, role):
        """
        Inherited from QAbstractTableModel, used to display data in a proper view
        :param index:
        :param role:
        :return:
        """
        col = index.column()
        row = index.row()
        if role == QtCore.Qt.TextAlignmentRole and col != 3:
            """ Handle text alignment """
            ret = QtCore.Qt.AlignCenter

        elif role == QtCore.Qt.DisplayRole:
            """ Handle data display """
            fr_id = list(self.frames.keys())[row]
            items = self.frames[fr_id]

            if col == 0:
                # Timestamp column
                msec = repr(items[2]).split(".")[1][:3]
                ret = time.strftime("%H:%M:%S.{}".format(msec), time.localtime(items[2]))
            elif col == 1:
                # ID columns
                ret = "{:02X}".format(fr_id)
            elif col == 2:
                # DLC column
                ret = items[0]
            elif col == 3:
                # Data column
                ret = " | ".join("{:02X}".format(b) for b in items[1])
            else:
                # Just in case, but should not arrive here
                ret = repr(items[col-2])
        else:
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
        return len(self.frames)

    def columnCount(self, parent=None, *args, **kwargs):
        """
        Inherited from QAbstractModel. Used for counting columns to display.
        :param parent:
        :param args:
        :param kwargs:
        :return:
        """
        if len(self.frames) > 0:
            fr_id = list(self.frames.keys())[0]
            ret = len(self.frames[fr_id]) + 1
        else:
            ret = 0

        return ret

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            ret = self.header_lables[section]

        else:
            ret = QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

        return ret

    def add_frame(self, fr):
        """
        Add a frame to the data set
        :param fr: Frame to be added. List type with the following elements:
        [Frame_ID, DLC, Data list, timestamp]
        :return: True if the frame was successfully added, False otherwise
        """
        if type(fr) == list and len(fr) == 4:
            self.frames[fr[0]] = [fr[1], fr[2], fr[3]]
            ret = True
        else:
            ret = False

        self.layoutChanged.emit()
        return ret

    def del_frame(self, fr_id):
        """
        Remove a frame from the dataset, specified by its ID
        :param fr_id: ID of the frame to remove from the set
        :return: True if the frame was succesfully removed, False otherwise
        """
        if fr_id in self.frames:
            self.frames.pop(fr_id)
            ret = True
        else:
            ret = False

        self.layoutChanged.emit()
        return ret

    def get_data(self):
        """
        Return the whole frame data set
        :return: Dictionary of frames, keys being frame IDs
        """
        return self.frames
