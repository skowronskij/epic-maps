from .fantasy.fantasy_style import FantasyStyle

STYLE_DICT = {"Fantasy": FantasyStyle}

class StylesContainer:

    def __init__(self, style_settings):
        self.style_settings = style_settings

    @property
    def get_style(self):
        style_class = STYLE_DICT.get(self.style_settings.mapstyle)
        return style_class(self.style_settings)
