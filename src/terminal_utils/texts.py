from functools import reduce
from typing import LiteralString

from terminal_utils.background_color import BackgroundColor
from terminal_utils.foreground_color import ForegroundColor
from terminal_utils.style import Style
from terminal_utils.text import Text


class Texts:
    def __init__(self):
        self.texts = []

    def add(self,
            text: LiteralString | str,
            foreground_color: ForegroundColor | None = None,
            background_color: BackgroundColor | None = None,
            style: Style | None = None
            ):

        instance = Text(text)

        if foreground_color:
            instance.fg(foreground_color)

        if background_color:
            instance.bg(background_color)

        if style:
            instance.style(style)

        self.texts.append(instance)

        return self

    def __str__(self):
        return reduce(lambda carry, current: carry + str(current), self.texts, '')
