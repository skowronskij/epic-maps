import random, os
from qgis.core import *
from qgis.gui import *
from qgis import processing
from qgis.PyQt.QtGui import QFont
from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface

class BaseStyle:
    def __init__(self, stylesettings):
        self.stylesettings = stylesettings
    
    def _create_landscape_layout(self):

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources'))
        template_path = os.path.join(path, '%s.qpt' % self.stylesettings.orientation)

        with open(template_path) as f:
            content = f.read()

        substitution_map = {
            'Tytul': self.stylesettings.title,
            'Autorr': self.stylesettings.author,
        }
        if self.stylesettings.author == "":
            substitution_map['Map drawn by'] = ""
        for before, after in substitution_map.items():
            content = content.replace(before, after)

        #Wczytanie szablonu wydruku
        layoutManager = QgsProject().instance().layoutManager()
        document = QDomDocument()
        document.setContent(content)
        layout = QgsPrintLayout(QgsProject.instance())
        layout.loadFromTemplate(document, QgsReadWriteContext())
        layoutName = self.stylesettings.title.split('\n')[0]
        
        #Unikanie takich samych nazw layoutów
        i=0
        while layoutManager.layoutByName(layoutName):
            # Dodawanie _numer do konca nazwy, jesli layout o danej nazwie istnieje
            layoutName = self.stylesettings.title + '_' + str(i)
            i += 1
        layout.setName(layoutName)
        
        #Zmiana rozmiwaru strony oraz zapisanie współczinnika służącego do skalowania obiektów na stronie
        page = layout.pageCollection().page(0)
        defaultPageSizeX = page.sizeWithUnits().width()
        defaultPageSizeY = page.sizeWithUnits().height()
        pageOrientation = {'portrait':0, 'landscape':1}
        page.setPageSize(self.stylesettings.size, pageOrientation.get(self.stylesettings.orientation))
        newPageSizeX = page.sizeWithUnits().width()
        newPageSizeY = page.sizeWithUnits().height()
        xRatio = newPageSizeX/defaultPageSizeX
        yRatio = newPageSizeY/defaultPageSizeY
        
        #Odnajdywanie obiektów i nadawanie im odpowiednich dla wielkości strony rozmiarów oraz miejsca
        itemIds = ['title', 'map', 'scale', 'legend', 'author', 'logo', 'logo2'] #TODO prefixy zamiast dokładnych nazw
        for itemId in itemIds:
            item = layout.itemById(itemId)
            if item != None:
                #Pozycja obiektu
                px, py = item.pagePos().x(), item.pagePos().y()
                item.attemptMove(QgsLayoutPoint(px*xRatio, py*yRatio))
                #Rozmiar obiektu
                sx, sy = item.sizeWithUnits().width(), item.sizeWithUnits().height()
                item.attemptResize(QgsLayoutSize(sx*xRatio, sy*yRatio))
                if itemId == 'map':
                    map_ = item
                    item.setLayers(self._get_layers())
                    item.zoomToExtent(iface.mapCanvas().extent())
                elif itemId == 'title' or itemId == 'subtitle' or itemId == 'author':
                    fontSize = item.font().pointSize()
                    font = QFont('Pristina', fontSize*yRatio) #TODO nazwa czcionki kopiowana automatycznie!
                    item.setFont(font)
                elif itemId == 'legend':
                    item.setLinkedMap(map_)
                    item.setLegendFilterByMapEnabled(True)
                elif itemId == 'logo':
                    item.setPicturePath(os.path.join(path, "old-paper.jpg"))
                elif itemId == "scale":
                    item.setMinimumBarWidth(item.minimumBarWidth() * xRatio)
                    item.setMaximumBarWidth(item.maximumBarWidth() * xRatio)
                    fontSize = item.font().pointSize()
                    font = QFont('Pristina', fontSize*yRatio)
                    item.setFont(font)
                item.refresh()
        
        layout.refresh()
        layoutManager.addLayout(layout)
        iface.openLayoutDesigner(layout)

    def _get_layers(self):
        layers = []
        for layers_meta in self.stylesettings.layers.values():
            layers.extend(list(layers_meta.keys()))
        return layers

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
                    'outline_width': str(5/bb.area()), 'joinstyle':'round', \
                    'use_custom_dash': str(5.8/bb.area()), 'customdash': dash})
                lines.renderer().setSymbol(lines_symbol)
                registry.addMapLayer(lines)

    def polygon2markers(self, vectorLayer, epsg, type, marker_filename):
        provider = "memory"
        layerSource = 'Point?crs=' + epsg

        pLayer = QgsVectorLayer(layerSource, "markers", provider)
        pLayer2 = QgsVectorLayer(layerSource, "markers2", provider)
        if type == "mountain":
            pLayer3 = QgsVectorLayer(layerSource, "markers3", provider)

        features = vectorLayer.getFeatures()

        for feature in features:
            polygon = feature.geometry()
            extend = polygon.boundingBox()

            def layer_create(layer):
                if type == "forest":
                    number_of_points = random.randint(int(round(polygon.area()*100)*0.85),int(round(polygon.area()*100)*1.15))
                elif type == "mountain":
                    number_of_points = random.randint(int(round(polygon.area()*10)*0.85),int(round(polygon.area()*10)*1.15))
                while True:
                    x = random.uniform(extend.xMinimum(), extend.xMaximum())
                    y = random.uniform(extend.yMinimum(), extend.yMaximum())
                    point = QgsPointXY(x,y)
                    geopoint = QgsGeometry.fromPointXY(point)
                    if geopoint.within(polygon):
                        feature = QgsFeature()
                        feature.setGeometry(geopoint)
                        layer.dataProvider().addFeature(feature)
                        number_of_points -= 1
                    if number_of_points <= 0:
                        break

            layer_create(pLayer)
            layer_create(pLayer2)
            if type == "mountain":
                layer_create(pLayer3)

        pLayer.updateExtents()
        pLayer2.updateExtents()
        QgsProject().instance().addMapLayer(pLayer)
        QgsProject().instance().addMapLayer(pLayer2)
        if type == "mountain":
            QgsProject().instance().addMapLayer(pLayer3)

        random_icons = random.sample(marker_filename,len(marker_filename))
        symbol = QgsSvgMarkerSymbolLayer(random_icons[0])
        symbol2 = QgsSvgMarkerSymbolLayer(random_icons[1])
        if type == "forest":
            symbol.setSize(4)
            symbol2.setSize(4)
        elif type == "mountain":
            symbol.setSize(12)
            symbol2.setSize(12)
            symbol3 = QgsSvgMarkerSymbolLayer(random_icons[2])
            symbol3.setSize(12)
        pLayer.renderer().symbol().changeSymbolLayer(0, symbol )
        pLayer2.renderer().symbol().changeSymbolLayer(0, symbol2 )
        if type == "mountain":
            pLayer3.renderer().symbol().changeSymbolLayer(0, symbol3 )


    def restyleLine(self, vectorLayer, colors, width, style='solid'):
        lines_symbol = QgsLineSymbol.createSimple({'line_color': colors, \
            'outline_width':width, 'joinstyle':'round', 'line_style': style})
        vectorLayer.renderer().setSymbol(lines_symbol)
