from PySide2 import QtGui, QtWidgets, QtCore


class AssetInfo(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super(QtWidgets.QGroupBox, self).__init__(parent)
        self.main_layout = QtWidgets.QVBoxLayout()
