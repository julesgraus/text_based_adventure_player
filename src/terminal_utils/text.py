from typing import LiteralString

from terminal_utils.foreground_color import ForegroundColor

from terminal_utils.background_color import BackgroundColor
from terminal_utils.style import Style


class Text:
    def __init__(self, text: LiteralString | str):
        self._text = text
        self._style = Style.Default
        self._fg = None
        self._bg = None

    def fg(self, color: ForegroundColor):
        self._fg = color
        return self

    def bg(self, color: BackgroundColor):
        self._bg = color
        return self

    def style(self, style: Style):
        self._style = style
        return self

    def __str__(self):
        # Ansi escape sequence
        to_return = '\033['

        # Set style
        to_return += str(self._style.value) + ';'

        # Set foreground color when applicable
        if self._fg:
            to_return += str(self._fg.value)

        # Set background color when applicable
        if self._bg:
            if self._fg:
                to_return += ';'
            to_return += str(self._bg.value)

        # Close the escape sequence
        to_return += 'm'

        # Append the text
        to_return += self._text

        # Reset the color
        to_return += '\033[0m'

        return to_return
