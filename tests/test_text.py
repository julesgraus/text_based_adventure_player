import unittest
from unittest.mock import patch, Mock

from terminal_utils.background_color import BackgroundColor
from terminal_utils.foreground_color import ForegroundColor
from terminal_utils.style import Style
from terminal_utils.text import Text
from terminal_utils.texts import Texts

class TestText(unittest.TestCase):
    def test_adding_text(self):

        with patch('terminal_utils.texts.Text', Mock(spec_set=Text)) as text_mock:
            fg_color = ForegroundColor.Black
            bg_color = BackgroundColor.White
            style = Style.Bold

            str(Texts().add(
                text="Example text",
                foreground_color=fg_color,
                background_color=bg_color,
                style=style
            ))

            text_mock.assert_called_once_with('Example text')
            text_mock.return_value.fg.assert_called_once_with(fg_color)
            text_mock.return_value.bg.assert_called_once_with(bg_color)
            text_mock.return_value.style.assert_called_once_with(style)
    def test_converting_to_string(self):
        self.assertEqual(f'[{Style.Blink.value};'
                         f'{ForegroundColor.Black.value};{BackgroundColor.White.value}m'
                         f'Example text[0m',
                         str(Texts().add(
                text="Example text",
                foreground_color=ForegroundColor.Black,
                background_color=BackgroundColor.White,
                style=Style.Blink
            )))


