#encoding: utf-8

from qgis.PyQt.Qt import QItemDelegate, QModelIndex, QAbstractTableModel, Qt
from qgis.PyQt.QtWidgets import QCheckBox

class LayerTypeModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        # to co bedziemy potrzebować do zwrócenia albo przetrzymywania informacji
        self.layers = []

    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):
        return len(self.layers)

    def insertRows(self, position, rows, parent=QModelIndex()):
        layers = []
        for key, item in rows.items():
            layers.extend(list(item.keys()))
        self.beginInsertRows(parent, position, position + len(rows) - 1)
        for i, layer in enumerate(layers):
            self.layers.insert(position+i, layer)
        self.endInsertRows()
        return True

    def removeRows(self, row=None, count=None, parent=QModelIndex()):
        if count==None:
            count = len(self.layers)
        if row==None:
            row = 0
        self.beginRemoveRows(parent, row, row+count)
        self.layers = []
        self.endRemoveRows()

    def headerData(self, section, QtOrientation, role):
        if QtOrientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Warstwa'
            elif section == 1:
                return 'Typ'

    def data(self, index, role):
        if not index.isValid():
            return
        layer = self.layers[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return layer.name()

    def flags(self, model):
        if not model.isValid():
            return
        return Qt.ItemIsEnabled | Qt.ItemIsEditable
