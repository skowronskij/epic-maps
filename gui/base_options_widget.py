
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget


class BaseOptionsWidget(QWidget):

    def __init__(self, parent, parents=None):
        super(BaseOptionsWidget, self).__init__(parents)
        self.setupUi(self)

        self.parent = parent
        if self.parent:
            self.styleSettings = self.parent.styleSettings
            self.connectSignals()

    def connectSignals(self):
        print('asd')
        self.tbNext.clicked.connect(self.nextWidget)

    def nextWidget(self):
        # self.setSettings()
        print('asd')
        self.parent.on_next_tab.emit(self)