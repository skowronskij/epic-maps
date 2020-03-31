# -*- coding: utf-8 -*-
"""
/***************************************************************************
 EpicMapsDialog
                                 A QGIS plugin
 Making stylish maps was never so easy!
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-02-23
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Mateusz Ośko, Piotr Koller, Jakub Skowroński
        email                : sekcja.geoinformacji.skng@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.core import QgsLayoutItemPage, QgsProject, QgsPageSizeRegistry
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets, QtGui

from .epic_maps_widget1 import EpicMapsWidget1
from .epic_maps_widget2 import EpicMapsWidget2
from .epic_maps_widget3 import EpicMapsWidget3
from ..styles.styles_container import StylesContainer
from ..styles.style_settings import StyleSettings

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'epic_maps_dialog.ui'))


class EpicMapsDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(EpicMapsDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        
        self.widget1 = EpicMapsWidget1(parent=self)
        self.widget2 = EpicMapsWidget2(parent=self)
        self.widget3 = EpicMapsWidget3(parent=self)
        self.hideallwidgets()

        self.setupUi(self)
        self.widget1.show()

        self.widget1.Next1.clicked.connect(self.changewidgetto2)
        self.widget2.Next2.clicked.connect(self.changewidgetto3)
        self.widget2.Previous2.clicked.connect(self.changewidgetto1)
        self.widget3.Previous3.clicked.connect(self.changewidgetto2)
        self.widget3.OK.clicked.connect(self.run)

        self.select_styles()
        self.pageOrientation()
        self.addItems()
        self.pageSizes()
        
    def changewidgetto1(self):
        self.hideallwidgets()
        self.widget1.show()
    
    def changewidgetto2(self):
        self.hideallwidgets()
        self.widget2.show()
        
    def changewidgetto3(self):
        self.hideallwidgets()
        self.widget3.show()

    def hideallwidgets(self):
        self.widget1.hide()
        self.widget2.hide()
        self.widget3.hide()

    def select_styles(self):
        self.styles_container = StylesContainer
        self.widget1.comboBox.addItems(list(self.styles_container.STYLE_DICT.keys()))
        self.selectedFileIndex = self.widget1.comboBox.currentIndex()
        self.selected_class = list(self.styles_container.STYLE_DICT.values())[self.selectedFileIndex]
        self.widget1.comboBox.currentIndexChanged.connect(self.styles_index)

    def styles_index(self):
        self.selectedFileIndex = self.widget1.comboBox.currentIndex()
        self.selected_class = list(self.styles_container.STYLE_DICT.values())[self.selectedFileIndex]

    def pageOrientation(self):
        self.SIZE_DICT = {"landscape": QgsLayoutItemPage.Orientation.Landscape, "portrait": QgsLayoutItemPage.Orientation.Portrait}
        self.widget2.comboBox_2.addItems(list(self.SIZE_DICT.keys()))
        self.selectedOrientationIndex = self.widget2.comboBox_2.currentIndex()
        self.selected_orientation = list(self.SIZE_DICT.values())[self.selectedOrientationIndex]
        self.widget2.comboBox_2.currentIndexChanged.connect(self.orientation_index)

    def orientation_index(self):
        self.selectedOrientationIndex = self.widget2.comboBox_2.currentIndex()
        self.selected_orientation = list(self.SIZE_DICT.values())[self.selectedOrientationIndex]

    def pageSizes(self):
        self.pages_list = [i.name for i in QgsPageSizeRegistry().entries()]
        self.widget2.comboBox.addItems(self.pages_list)
        self.selectedSizeIndex = self.widget2.comboBox.currentIndex()
        self.selectedSize = self.pages_list[self.selectedSizeIndex]
        self.widget2.comboBox.currentIndexChanged.connect(self.size_index)

    def size_index(self):
        self.selectedSizeIndex = self.widget2.comboBox.currentIndex()
        self.selectedSize = self.pages_list[self.selectedSizeIndex]

    def addItems(self):
        names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]

        self.listView = self.widget2.listView
        model = QtGui.QStandardItemModel()

        self.listView.setModel(model)

        for i in names:
            model.appendRow(QtGui.QStandardItem(i))

    def settings(self):
        self.style_settings = StyleSettings
        self.style_settings.title = self.widget3.line_edit.text()
        self.style_settings.author = self.widget3.line_edit_2.text()

    def run(self):
        self.hide()


        
        

