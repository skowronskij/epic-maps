#encoding: utf-8

from qgis.PyQt.Qt import QItemDelegate, QModelIndex, QAbstractTableModel, Qt
from qgis.PyQt.QtWidgets import QComboBox
from qgis.core import QgsWkbTypes

class LayerTypeModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        # to co bedziemy potrzebować do zwrócenia albo przetrzymywania informacji
        self.layers = []
        self.layer_style_map = {}

    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):
        return len(self.layers)

    def insertRows(self, position, rows, parent=QModelIndex()):
        layers = []
        for key, item in rows.items():
            layers.extend(list(item.keys()))
        self.beginInsertRows(parent, position, position + len(layers) - 1)
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
        elif role == Qt.UserRole:
            if index.column() == 1:
                return layer

    def setData(self, index, value, role):
        layer = self.layers[index.row()]
        if role == Qt.EditRole:
            self.layer_style_map[layer] = value
            return True

    def flags(self, model):
        if not model.isValid():
            return
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

class LayerTypeDelegate(QItemDelegate):
    def __init__(self, style_types, model, parent=None):
        QItemDelegate.__init__(self, parent)
        self.style_types = style_types
        self.model = model
        #{"points":["Battles","Towns","Other"],
        # "lines":["Rivers","Routes","Other"],
        # "polygons":["Lands","Waters","Forests","Mountains","Other"]}
    
    def createEditor(self, parent, option, index):
        if index.column() == 1:
            layer = index.data(Qt.UserRole)
            layer_type = self.getLayerType(layer)
            if not layer_type:
                return
            editor = QComboBox(parent)
            editor.addItems(self.style_types[layer_type])
            editor.currentIndexChanged.connect(self.valueChanged)
            return editor

    def getLayerType(self, layer):
        if layer.geometryType() == QgsWkbTypes.PointGeometry:
            return 'points'
        if layer.geometryType() == QgsWkbTypes.LineGeometry:
            return 'lines'
        if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
            return 'polygons'
        # jeśli typ gemoetrii inny niż przewidywany zwracamy none
        return None

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        if isinstance(editor, QComboBox):
            editor.setCurrentIndex(0)
            self.setModelData(editor, self.model, index)
        editor.blockSignals(False)
    
    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)

    def valueChanged(self):
        self.commitData.emit(self.sender())
