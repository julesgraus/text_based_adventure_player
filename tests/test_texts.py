import unittest

from terminal_utils.background_color import BackgroundColor
from terminal_utils.foreground_color import ForegroundColor
from terminal_utils.style import Style
from terminal_utils.text import Text


class TestTexts(unittest.TestCase):
    def test_construction(self):
        text = (Text('Example text')
                .style(Style.Default)
                .fg(ForegroundColor.White)
                .bg(BackgroundColor.Bright_GRAY)
                )

        self.assertEqual(f'['
                         f'{Style.Default.value};'
                         f'{ForegroundColor.White.value};'
                         f'{BackgroundColor.Bright_GRAY.value}'
                         f'mExample text'
                         f'[0m', str(text)
                         )
