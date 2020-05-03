# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget
from qgis.core import QgsPageSizeRegistry

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'layers_page_options_widget.ui'))


class LayersPageOptionsWidget(QWidget, FORM_CLASS):
    def __init__(self, parent, parents=None):
        super(LayersPageOptionsWidget, self).__init__(parents)
        self.setupUi(self)

        self.cbOrientation.addItems(['landscape', 'portrait'])
        self.cbSize.addItems([i.name for i in QgsPageSizeRegistry().entries()])

        self.parent = parent
        self.styleSettings = self.parent.styleSettings
        self.connectSignals()

    def connectSignals(self):
        self.tbNext.clicked.connect(self.nextWidget)
        self.tbPrevious.clicked.connect(self.prevWidget)

    def nextWidget(self):
        succes, error = self.setSettings()
        if not succes:
            self.parent.setMessage(error)
            return
        self.parent.on_next_tab.emit(self)

    def prevWidget(self):
        self.parent.on_previous_tab.emit()

    def setSettings(self):
        # TODO Layers table model with checkboxes
        self.styleSettings.layers = ['asd']
        size = self.cbSize.currentText()
        orientation = self.cbOrientation.currentText()
        if not size:
            return False, 'Size argument missing'
        if not orientation:
            return False, 'Orientation argument missing'
        self.styleSettings.size = size
        self.styleSettings.orientation= orientation
        return True, None