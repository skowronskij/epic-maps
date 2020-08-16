from ..base_style import BaseStyle
from qgis.core import *
from qgis.gui import *
from PyQt5.QtGui import QColor

import processing
import os

class TopographyStyle(BaseStyle):
    def __init__(self, stylesettings):
        super().__init__(stylesettings)
        self.stylesettings.types = {"points":["Churches","Hotels","Museums","Airports","Hospitals"],"lines":["Rivers","Rails","Roads"],"polygons":["Lakes", "Forests", "Buildings"]}

    def generate_layout(self):
        super().generate_layout(self)

    def stylePolygonLakes(self, vectorLayer):
        symbol = QgsFillSymbol.createSimple({'color': "#0099ff", 
            'outline_color': "#0099ff", 
            'outline_width': str(1),})
        vectorLayer.renderer().setSymbol(symbol)
        vectorLayer.triggerRepaint()

    def stylePolygonForests(self, vectorLayer):
        symbol = QgsFillSymbol.createSimple({'color': "#01a257", 
            'outline_color': "#01a257", 
            'outline_width': str(1),})
        vectorLayer.renderer().setSymbol(symbol)
        vectorLayer.triggerRepaint()

    def stylePolygonBuildings(self, vectorLayer):
        symbol = QgsFillSymbol.createSimple({'color': "#ff9900", 
            'outline_color': "#ff9900", 
            'outline_width': str(1),})
        vectorLayer.renderer().setSymbol(symbol)
        vectorLayer.triggerRepaint()

    def stylePointChurches(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","place_of_worship_christian3.svg"))
        self.symbol.setSize(5)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )
        vectorLayer.triggerRepaint()

    def stylePointHotels(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","accommodation_hotel2.svg"))
        self.symbol.setSize(5)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )
        vectorLayer.triggerRepaint()

    def stylePointMuseums(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","tourist_museum.svg"))
        self.symbol.setSize(5)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )
        vectorLayer.triggerRepaint()

    def stylePointAirports(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","transport_aerodrome2.svg"))
        self.symbol.setSize(5)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )
        vectorLayer.triggerRepaint()

    def stylePointHospitals(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","amenity=hospital.svg"))
        self.symbol.setSize(5)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )
        vectorLayer.triggerRepaint()

    def styleLineRivers(self, vectorLayer):
        self.symbol = QgsLineSymbol.createSimple({'line_color': "#0099ff",
            'outline_width':str(0.5), 'joinstyle':'round'})
        vectorLayer.renderer().setSymbol(self.symbol)
        vectorLayer.triggerRepaint()

    def styleLineRails(self, vectorLayer):
        vectorLayer.loadNamedStyle(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","rail.qml"))
        vectorLayer.triggerRepaint()

    def styleLineRoads(self, vectorLayer):
        self.symbol = QgsLineSymbol.createSimple({'line_color': "#990000",'outline_color': "#000000",
            'outline_width':str(0.8), 'joinstyle':'round'})
        vectorLayer.renderer().setSymbol(self.symbol)
        vectorLayer.triggerRepaint()

    def testing(self, layer_style_map):
        root = QgsProject.instance().layerTreeRoot()
        group = root.findGroup(f'Epic Maps {self.stylesettings.mapstyle} - {self.stylesettings.title}')
        for layer, style in layer_style_map.items():
            copy = layer.clone()
            copy.updateExtents(True)
            layer_type = self.getLayerType(copy)
            method_name = f'style{layer_type}{style}'
            method = getattr(self, method_name)
            method(copy)
            QgsProject.instance().addMapLayer(copy, False)
            group.addLayer(copy)
            copy.triggerRepaint()
        self._create_landscape_layout()
        # return copies

    def getLayerType(self, layer):
        if layer.geometryType() == QgsWkbTypes.PointGeometry:
            return 'Point'
        if layer.geometryType() == QgsWkbTypes.LineGeometry:
            return 'Line'
        if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
            return 'Polygon'
        # jeśli typ gemoetrii inny niż przewidywany zwracamy none
        return None
