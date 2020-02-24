from .fantasy.fantasy_style import FantasyStyle

class StylesContainer:
    STYLE_DICT = {"fantasy": FantasyStyle}

    def __init__(self, style_settings):
        self.style_settings = style_settings

    @property
    def style_class(self):
        style_class = self.STYLE_DICT.get(self.style_settings.mapstyle)
        return style_class(self.style_settings)