# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

from ..styles.styles_container import STYLE_DICT

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'style_options_widget.ui'))


class StyleOpstionsWidget(QWidget, FORM_CLASS):

    def __init__(self, parent, parents=None):
        super(StyleOpstionsWidget, self).__init__(parents)
        self.setupUi(self)
    
        self.cbStyles.addItems(list(STYLE_DICT.keys()))

        self.parent = parent
        self.styleSettings = self.parent.styleSettings
        self.connectSignals()

    def connectSignals(self):
        self.tbNext.clicked.connect(self.nextWidget)

    def nextWidget(self):
        style = self.cbStyles.currentText()
        if not style:
            self.parent.setMessage('Style argument missing')
            return
        self.styleSettings.mapstyle = self.cbStyles.currentText()
        self.parent.on_next_tab.emit(self)
