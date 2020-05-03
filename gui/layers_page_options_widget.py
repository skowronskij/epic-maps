# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import QgsPageSizeRegistry, QgsProject, QgsMapLayerType

from ..models.layerListModel import LayersListModel, LayerDelegate

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'layers_page_options_widget.ui'))


class LayersPageOptionsWidget(QWidget, FORM_CLASS):
    def __init__(self, parent, parents=None):
        super(LayersPageOptionsWidget, self).__init__(parents)
        self.setupUi(self)

        self.parent = parent
        self.styleSettings = self.parent.styleSettings
        self.setGui()
        self.connectSignals()

    def setGui(self):
        self.cbOrientation.addItems(['landscape', 'portrait'])
        self.cbSize.addItems([i.name for i in QgsPageSizeRegistry().entries()])
        self.lvLayers.setModel(LayersListModel())
        self.lvLayers.setItemDelegate(LayerDelegate(self))

    def connectSignals(self):
        self.tbNext.clicked.connect(self.nextWidget)
        self.tbPrevious.clicked.connect(self.prevWidget)

    def nextWidget(self):
        succes, error = self.setSettings()
        if not succes:
            self.parent.setMessage(error)
            return
        self.parent.on_next_tab.emit(self)

    def show(self):
        self.setLayerList()
        super(LayersPageOptionsWidget, self).show()

    def prevWidget(self):
        self.parent.on_previous_tab.emit()

    def setSettings(self):
        layers = self.lvLayers.model().selected_layers
        if not layers:
            return False, 'No layers selected'
        size = self.cbSize.currentText()
        if not size:
            return False, 'Size argument missing'
        orientation = self.cbOrientation.currentText()
        if not orientation:
            return False, 'Orientation argument missing'
        self.styleSettings.size = size
        self.styleSettings.orientation= orientation
        return True, None

    def setLayerList(self):
        self.lvLayers.model().removeRows()
        model = self.lvLayers.model()
        layers = [
            layer for layer in QgsProject.instance().mapLayers().values() 
            if layer.type() == QgsMapLayerType.VectorLayer
            ]
        model.insertRows(0, layers)
        for row in range(0, model.rowCount()):
            self.lvLayers.openPersistentEditor(model.index(row))