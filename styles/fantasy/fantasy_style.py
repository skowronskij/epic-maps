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
        self.recolorPolygon(vectorLayer, 250, 255, 230, 250, 160, 200, 0.2)

        registry = QgsProject.instance()

        vectorLayer.selectAll()
        bb = vectorLayer.boundingBoxOfSelected()
        vectorLayer.removeSelection()
        mean = (bb.height() + bb.width()) / 2
        bufDist = int(mean / 100)
        bufDist2 = bufDist * 2

        buffs = []
        buffs.append(processing.run("qgis:buffer", {'INPUT':vectorLayer, 'DISTANCE': bufDist, 'DISSOLVE': True, 'SEGMENTS': 100, 'OUTPUT':'memory:'})['OUTPUT'])
        buffs.append(processing.run("qgis:buffer", {'INPUT':vectorLayer, 'DISTANCE': bufDist2, 'DISSOLVE': True, 'SEGMENTS': 100, 'OUTPUT':'memory:'})['OUTPUT'])
        
        dashes = ['5;2', '3;1']
        for buff, dash in zip(buffs, dashes):
            lines = processing.run("qgis:polygonstolines", {'INPUT':buff, 'OUTPUT':'memory:'})['OUTPUT']
            
            lines_symbol = QgsLineSymbol.createSimple({'outline_color': border_colors, \
                'outline_width':'0.2', 'joinstyle':'round', \
                'use_custom_dash': '1', 'customdash': dash})
            lines.renderer().setSymbol(lines_symbol)
            registry.addMapLayer(lines)
    
    def stylePolygonWater(self, vectorLayer):
        self.recolorPolygon(vectorLayer, 100, 180, 200, 230, 245, 250, 0.15)

    def stylePolygonOther(self, vectorLayer):
        self.recolorPolygon(vectorLayer, 240, 255, 190, 220, 100, 140, 0.15)
