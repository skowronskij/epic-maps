from ..base_style import BaseStyle

import processing

class FantasyStyle(BaseStyle):
    def __init__(self, stylesettings):
        super().__init__(stylesettings)

    def generate_layout(self):
        super().generate_layout(self)
        #tutaj jakaś logika która wywołuje odpowiednie funkcje dla odpowiednich warstw


    #Style - do przetestowania!
    def stylePolygonLands(self, vectorLayer):        
        self.restylePolygon(vectorLayer, 250, 255, 230, 250, 160, 200, 0.2, True)
    
    def stylePolygonWater(self, vectorLayer):
        self.restylePolygon(vectorLayer, 100, 180, 200, 230, 245, 250, 0.15)

    def stylePolygonOther(self, vectorLayer):
        self.restylePolygon(vectorLayer, 240, 255, 190, 220, 100, 140, 0.15)

    def stylePolygonForest(self, vectorLayer):
        epsg = vectorLayer.crs().authid()
        self.polygon2markers(vectorLayer, epsg, ":/fantasy/resources/tree.svg")

    def stylePolygonMountains(self, vectorLayer):
        epsg = vectorLayer.crs().authid()
        self.polygon2markers(vectorLayer, epsg, ":/fantasy/resources/mountain.svg")


    def stylePointTowns(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(":/fantasy/resources/medieval.svg")
        self.symbol.setSize(6)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )

    def stylePointBattles(self,vectorLayer):
        self.symbol = QgsSvgMarkerSymbolLayer(":/fantasy/resources/monuments.svg")
        self.symbol.setSize(6)
        vectorLayer.renderer().symbol().changeSymbolLayer(0, self.symbol )

    def stylePointOther(self,vectorLayer):
        self.symbol = vectorLayer.renderer().symbol()
        self.symbol.setColor(QColor.fromRgb(153, 0, 0))
        vectorLayer.triggerRepaint()


    def styleLineRivers(self, vectorLayer):
        self.restyleLine(vectorLayer, 100, 180, 200, 230, 245, 250)