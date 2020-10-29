from PyQt5 import QtCore


class ModelSignals(QtCore.QObject):
    data_updated = QtCore.pyqtSignal()


class Model:
    """
    Model class for representing a set of CAN frames
    """
    def __init__(self):
        """
        Class initialization
        """
        self.signals = ModelSignals()
        self.frames = {}

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

        self.signals.data_updated.emit()
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

        self.signals.data_updated.emit()
        return ret

    def get_data(self):
        """
        Return the whole frame data set
        :return: Dictionary of frames, keys being frame IDs
        """
        return self.frames
