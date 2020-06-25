#encoding: utf-8

from qgis.PyQt.Qt import QItemDelegate, QModelIndex, QAbstractTableModel, Qt
from qgis.PyQt.QtWidgets import QCheckBox

class LayerTypeModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        # to co bedziemy potrzebować do zwrócenia albo przetrzymywania informacji
        self.data = [1,2,3]

    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def headerData(self, section, QtOrientation, role):
        if QtOrientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Warstwa'
            elif section == 1:
                return 'Typ'

    def data(self, index, role):
        if not index.isValid():
            return
        layer = self.data[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return layer
