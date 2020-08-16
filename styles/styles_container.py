from .fantasy.fantasy_style import FantasyStyle
from .topography.topography_style import TopographyStyle

STYLE_DICT = {"Fantasy": FantasyStyle, "Topography": TopographyStyle}
#STYLE_DICT = {"Topography": TopographyStyle}

class StylesContainer:

    def __init__(self, style_settings):
        self.style_settings = style_settings

    @property
    def get_style(self):
        style_class = STYLE_DICT.get(self.style_settings.mapstyle)
        return style_class(self.style_settings)
