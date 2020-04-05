from ..base_style import BaseStyle

import processing

class FantasyStyle(BaseStyle):
    def __init__(self, stylesettings):
        super().__init__(stylesettings)

    def generate_layout(self):
        super().generate_layout(self)
        #tutaj jakaś logika która wywołuje odpowiednie funkcje dla odpowiednich warstw

    def stylePolygonLands(self, vectorLayer):
        registry = QgsProject.instance()
        
        red = random.randrange(250,255)
        green = random.randrange(230,250)
        blue = random.randrange(160,200)
        colors = str(red) + "," + str(green) + "," + str(blue)
        border_colors = str(red-20) + "," + str(green-20) + "," + str(blue-20)

        symbol = QgsFillSymbol.createSimple({'color': colors, \
            'outline_color': border_colors, \
            'outline_width':'0.2', \
            'joinstyle':'round'})

        vectorLayer.renderer().setSymbol(symbol)
        vectorLayer.triggerRepaint()

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
            