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

    def recolorPolygon(self, vectorLayer, minRed, maxRed, minGreen, maxGreen, minBlue, maxBlue, outlineWidth):
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