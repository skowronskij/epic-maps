import random
from qgis.core import *
from qgis.gui import *
from qgis import processing

class BaseStyle:
    def __init__(self, stylesettings):
        self.stylesettings = stylesettings
    
    def _create_landscape_layout(self):
        self.landscape_path = ":/templates/landscape.qpt"
        self.portrait_path = ":/templates/portrait.qpt"

        with open(path) as f:
                content = f.read()

        substitution_map = {
            'Tytuł': self.stylesettings.title.strip(),
            'Autor': self.stylesettings.author.strip()
        }
        for before, after in substitution_map.items():
            content = content.replace(before, after)

        layoutManager = QgsProject().instance().layoutManager()
        document = QDomDocument()
        document.setContent(content)
        layout = QgsPrintLayout(QgsProject.instance())
        layout.loadFromTemplate(document, QgsReadWriteContext())
        layoutName = self.stylesettings.title.split('\n')[0]

    def generate_layout(self):
        pass

    def generateColors(self, minRed, maxRed, minGreen, maxGreen, minBlue, maxBlue):
        red = random.randrange(minRed, maxRed)
        green = random.randrange(minGreen, maxGreen)
        blue = random.randrange(minBlue, maxBlue)
        colors = str(red) + "," + str(green) + "," + str(blue)
        return colors

    def restylePolygon(self, vectorLayer, colors, outlineWidth, make_boundary_waves=False):
        colors_split = colors.split(',')
        red = int(colors_split[0])
        green = int(colors_split[1])
        blue = int(colors_split[2])
        border_colors = str(red-20) + "," + str(green-20) + "," + str(blue-20)
        symbol = QgsFillSymbol.createSimple({'color': colors, \
            'outline_color': border_colors, \
            'outline_width': str(outlineWidth), \
            'joinstyle':'round'})

        vectorLayer.renderer().setSymbol(symbol)
        vectorLayer.triggerRepaint()
        
        if make_boundary_waves:
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
                    'outline_width':'1', 'joinstyle':'round', \
                    'use_custom_dash': '1.8', 'customdash': dash})
                lines.renderer().setSymbol(lines_symbol)
                registry.addMapLayer(lines)

    def polygon2markers(self, vectorLayer, epsg, type, marker_filename):
        provider = "memory"
        layerSource = 'Point?crs=' + epsg
        pLayer = QgsVectorLayer(layerSource, "markers", provider)

        features = vectorLayer.getFeatures()

        for feature in features:
            polygon = feature.geometry()
            extend = polygon.boundingBox()

            if type == "forest":
                number_of_points = round(polygon.area()*100)
            elif type == "mountain":
                number_of_points = round(polygon.area()*10)

            while True:
                x = random.uniform(extend.xMinimum(), extend.xMaximum())
                y = random.uniform(extend.yMinimum(), extend.yMaximum())
                point = QgsPointXY(x,y)
                geopoint = QgsGeometry.fromPointXY(point)
                if geopoint.within(polygon):
                    feature = QgsFeature()
                    feature.setGeometry(geopoint)
                    pLayer.dataProvider().addFeature(feature)
                    number_of_points -= 1
                if number_of_points <= 0:
                    break
        pLayer.updateExtents()
        QgsProject().instance().addMapLayer(pLayer)

        symbol = QgsSvgMarkerSymbolLayer(random.choice(marker_filename))
        if type == "forest":
            symbol.setSize(4)
        elif type == "mountain":
            symbol.setSize(12)
        pLayer.renderer().symbol().changeSymbolLayer(0, symbol )


    def restyleLine(self, vectorLayer, colors, width, style='solid'):
        lines_symbol = QgsLineSymbol.createSimple({'line_color': colors, \
            'outline_width':width, 'joinstyle':'round', 'line_style': style})
        vectorLayer.renderer().setSymbol(lines_symbol)
