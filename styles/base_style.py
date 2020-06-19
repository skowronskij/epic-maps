class BaseStyle:
    def __init__(self, stylesettings):
        self.__stylesettings = stylesettings
    
    def _create_landscape_layout(self):
        self.landscape_path = ":/templates/landscape.qpt"
        self.portrait_path = ":/templates/portrait.qpt"

        with open(path) as f:
                content = f.read()

        substitution_map = {
            'Tytuł': self.__stylesettings.title.strip(),
            'Autor': self.__stylesettings.author.strip()
        }
        for before, after in substitution_map.items():
            content = content.replace(before, after)

        layoutManager = QgsProject().instance().layoutManager()
        document = QDomDocument()
        document.setContent(content)
        layout = QgsPrintLayout(QgsProject.instance())
        layout.loadFromTemplate(document, QgsReadWriteContext())
        layoutName = self.__stylesettings.title.split('\n')[0]

    def generate_layout(self):
        pass

    def restylePolygon(self, vectorLayer, minRed, maxRed, minGreen, maxGreen, minBlue, maxBlue, outlineWidth, make_boundary_waves=False):
        red = random.randrange(minRed, maxRed)
        green = random.randrange(minGreen, maxGreen)
        blue = random.randrange(minBlue, maxBlue)
        colors = str(red) + "," + str(green) + "," + str(blue)
        border_colors = str(red-20) + "," + str(green-20) + "," + str(blue-20)

        symbol = QgsFillSymbol.createSimple({'color': colors, \
            'outline_color': border_colors, \
            'outline_width': outlineWidth, \
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
                    'outline_width':'0.2', 'joinstyle':'round', \
                    'use_custom_dash': '1', 'customdash': dash})
                lines.renderer().setSymbol(lines_symbol)
                registry.addMapLayer(lines)

    def polygon2markers(self, vectorLayer, epsg, marker_filename):
        provider = "memory"
        layerSource = 'Point?crs=' + epsg
        pLayer = QgsVectorLayer(layerSource, "markers", provider)

        features = vectorLayer.getFeatures()
        for feature in features:
            polygon = feature.geometry()
            extend = polygon.boundingBox()

            number_of_points = 50 #póki co przypadkowa wartość, trzeba to jeszcze przemyśleć

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
        registry.addMapLayer(pLayer)

        symbol = QgsSvgMarkerSymbolLayer(marker_filename)
        symbol.setSize(4) #póki co przypadkowa wartość, trzeba to jeszcze przemyśleć
        pLayer.renderer().symbol().changeSymbolLayer(0, symbol )


    def restyleLine(self, vectorLayer, minRed, maxRed, minGreen, maxGreen, minBlue, maxBlue):
        red = random.randrange(minRed, maxRed)
        green = random.randrange(minGreen, maxGreen)
        blue = random.randrange(minBlue, maxBlue)
        colors = str(red) + "," + str(green) + "," + str(blue)
        lines_symbol = QgsLineSymbol.createSimple({'outline_color': colors, \
            'outline_width':'0.2', 'joinstyle':'round'})
        vectorLayer.renderer().setSymbol(lines_symbol)