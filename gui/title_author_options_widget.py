# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'title_author_options_widget.ui'))


class TitleAuthorOptionsWidget(QWidget, FORM_CLASS):
    def __init__(self, parent, parents=None):
        super(TitleAuthorOptionsWidget, self).__init__(parents)
        self.setupUi(self)

        self.parent = parent
        self.styleSettings = self.parent.styleSettings
        self.connectSignals()

    def connectSignals(self):
        self.tbPrevious.clicked.connect(self.prevWidget)
        self.tbGenerate.clicked.connect(self.settingsCompleted)

    def prevWidget(self):
        self.parent.on_previous_tab.emit()

    def settingsCompleted(self):
        self.setSettings()
        print('aaa')
        self.parent.on_generate.emit()

    def setSettings(self):
        self.styleSettings.title = self.leTitle.text()
        self.styleSettings.author = self.leAuthor.text()
        
