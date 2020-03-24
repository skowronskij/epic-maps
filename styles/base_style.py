class BaseStyle:
    def __init__(self, stylesettings):
        self.__stylesettings = stylesettings
    
    def _create_landscape_layout(self, stylesettings):
        self.landscape_path = ":/templates/landscape.qpt"
        self.portrait_path = ":/templates/portrait.qpt"

        with open(path) as f:
                content = f.read()

        substitution_map = {
            'Tytuł': stylesettings.title.text().strip(),
            'Autor': stylesettings.author.text().strip()
        }
        for before, after in substitution_map.items():
            content = content.replace(before, after)

        layoutManager = QgsProject().instance().layoutManager()
        document = QDomDocument()
        document.setContent(content)
        layout = QgsPrintLayout(QgsProject.instance())
        layout.loadFromTemplate(document, QgsReadWriteContext())
        layoutName = stylesettings.title.text().split('\n')[0]

    def generate_layout(self):
        pass

