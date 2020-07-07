from ..base_style import BaseStyle
from qgis.core import *
from qgis.gui import *

import processing
import os

class FantasyStyle(BaseStyle):
    def __init__(self, stylesettings):
        super().__init__(stylesettings)
        self.water_colors = self.generateColors(100, 180, 200, 230, 245, 250)
        self.land_colors = self.generateColors(250, 255, 230, 250, 160, 200)
        self.routes_colors = self.generateColors(102, 114, 50, 60, 30, 40)
        self.stylesettings.types = {"points":["Battles","Towns","Other"],"lines":["Rivers","Routes","Other"],"polygons":["Lands","Waters","Forests","Mountains","Other"]}

    def generate_layout(self):
        super().generate_layout(self)
        #tutaj jakaś logika która wywołuje odpowiednie funkcje dla odpowiednich warstw

    #Style - do przetestowania!
    def stylePolygonLands(self, vectorLayer):   
        self.restylePolygon(vectorLayer, self.land_colors, 0.2, True)
    
    def stylePolygonWaters(self, vectorLayer):
        self.restylePolygon(vectorLayer, self.water_colors,  0.15)

    def stylePolygonOther(self, vectorLayer):
        colors = self.generateColors(240, 255, 190, 220, 100, 140)
        self.restylePolygon(vectorLayer, colors, 0.15)

    def stylePolygonForests(self, vectorLayer):
        epsg = vectorLayer.crs().authid()
        self.polygon2markers(vectorLayer, epsg, "forest", [os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","tree.svg"),os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","tree2.svg")])

    def stylePolygonMountains(self, vectorLayer):
        epsg = vectorLayer.crs().authid()
        self.polygon2markers(vectorLayer, epsg, "mountain", [os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","mountain1.svg"),os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","mountain2.svg"),os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","mountain3.svg")])

    def stylePointTowns(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","monuments.svg"))
        self.symbol.setSize(6)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )
        vectorLayer.triggerRepaint()

    def stylePointBattles(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(os.path.join(os.path.dirname(os.path.abspath(__file__)),"resources","medieval.svg"))
        self.symbol.setSize(6)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )
        vectorLayer.triggerRepaint()

    def stylePointOther(self,vectorLayer):
        self.symbol = vectorLayer.renderer().symbol()
        colors = self.generateColors(140, 150, 0, 30, 0, 30)
        self.symbol.setColor(QColor.fromRgb(153, 0, 0))
        vectorLayer.triggerRepaint()

    def styleLineRivers(self, vectorLayer):
        self.restyleLine(vectorLayer, self.water_colors, '0.5')
        vectorLayer.triggerRepaint()

    def styleLineRoutes(self, vectorLayer):
        self.restyleLine(vectorLayer, self.routes_colors, '0.5', 'dot')
        vectorLayer.triggerRepaint()

    def styleLineOther(self, vectorLayer):
        colors = self.generateColors(140, 160, 140, 180, 130, 160)
        self.restyleLine(vectorLayer, colors, '0.5')
        vectorLayer.triggerRepaint()

    def testing(self, layer_style_map):
        for layer, style in layer_style_map.items():
            layer_type = self.getLayerType(layer)
            method_name = f'style{layer_type}{style}'
            method = getattr(self, method_name)
            method(layer)
        self._create_landscape_layout()

    def getLayerType(self, layer):
        if layer.geometryType() == QgsWkbTypes.PointGeometry:
            return 'Point'
        if layer.geometryType() == QgsWkbTypes.LineGeometry:
            return 'Line'
        if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
            return 'Polygon'
        # jeśli typ gemoetrii inny niż przewidywany zwracamy none
        return None
