import unittest
from unittest.mock import patch, Mock

from app.dto.game import Game as GameDto
from app.dto.meta import Meta as MetaDto
from app.dto.init import Init as InitDto
from jfw.config import Config
from menu.main import Main


class MainTestCaseTestCase(unittest.TestCase):
    def test_it_shows_the_main_menu_intro(self):
        with patch("builtins.print", Mock()) as mock_print:
            (Main(Config(''))).show_intro()

            output = str(mock_print.call_args.args[0])
            self.assertIn('--=[ Welcome to the adventure player ]=--', output)
            self.assertIn('Let the adventure begin!', output)

    def test_it_shows_the_main_menu(self):
        with patch("builtins.input", return_value="") as mock_input:
            config = Config('')
            (Main(config)).show()

            output = str(mock_input.call_args.args[0])
            self.assertIn('What is it that you', output)
            self.assertIn('want to', output)
            self.assertIn('do', output)
            self.assertIn('Load a game', output)
            self.assertIn('Exit', output)
            self.assertNotIn('Create or edit a game', output)

    def test_it_shows_the_main_menu_with_creator_mode_option(self):
        with patch("builtins.input", return_value="") as mock_input:
            config = Config('')
            config.set('creator_mode', 1)

            (Main(config)).show()

            output = str(mock_input.call_args.args[0])
            self.assertIn('Create or edit a game', output)

    def test_it_handles_load_game_menu_option(self):
        game_loader = Mock()
        game_loader.return_value = game_loader

        game = GameDto(
            meta=MetaDto(
                name="test game",
                description="test description",
                file_name="test game.tba",
                file_path="some file path"
            ),
            state={},
            init=InitDto(
                state={},
                dialog='main'
            )
        )

        game_loader.available_games = Mock(return_value=[game])

        with (
            patch("builtins.print", Mock()) as mock_print,
            patch("builtins.input", return_value="1") as mock_input,
            patch("menu.main.GameLoader", game_loader),
        ):
            (Main(Config(''))).show()

            input_string = str(mock_input.call_args.args[0])
            output_string = str(mock_print.call_args.args[0])
            self.assertIn('Choose a game', input_string)
            self.assertIn('test game', input_string)
            self.assertIn(' - ', input_string)
            self.assertIn('test description', input_string)

            self.assertIn('Play test game', output_string)

    def test_it_handles_create_game_menu_option(self):
        with (
            patch("builtins.print", Mock()),
            patch("builtins.input", side_effect=['3', '']),
            patch("menu.main.CreateEditGame") as create_edit_game_mock,
        ):
            config = Config('')
            config.set('creator_mode', 1)

            (Main(config)).show()
            create_edit_game_mock.assert_called_once()
