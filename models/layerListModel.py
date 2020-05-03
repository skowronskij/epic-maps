#encoding: utf-8

from qgis.PyQt.Qt import QItemDelegate, QModelIndex, QAbstractListModel, Qt
from qgis.PyQt.QtWidgets import QCheckBox

class LayersListModel(QAbstractListModel):    
    def __init__(self, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.layers = []
        self.selected_layers = []
    
    def rowCount(self, parent=QModelIndex()):
        return len(self.layers)
    
    def data(self, index, role):
        if not index.isValid():
            return
        layer = self.layers[index.row()]
        if role == Qt.UserRole:
            return layer

    def setData(self, index, value, role):
        layer = self.layers[index.row()]
        if role == Qt.EditRole:
            if value == True:
                if layer not in self.selected_layers:
                    self.selected_layers.append(layer)
            else:
                if layer in self.selected_layers:
                    self.selected_layers.remove(layer)
            return True

    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + len(rows) - 1)
        for i, layer in enumerate(rows):
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
        self.selected_layers = []
        self.endRemoveRows()

    def flags(self, model):
        if not model.isValid():
            return
        return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable

class LayerDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)
    
    def createEditor(self, parent, option, index):
        layer_name = index.data(Qt.UserRole).name()
        editor = QCheckBox(layer_name, parent)
        editor.clicked.connect(self.valueChanged)
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setChecked(False)
        editor.blockSignals(False)
    
    def setModelData(self, editor, model, index):
        model.setData(index, editor.isChecked(), Qt.EditRole)

    def valueChanged(self):
        self.commitData.emit(self.sender())