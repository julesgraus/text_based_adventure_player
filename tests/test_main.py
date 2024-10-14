import unittest
from unittest.mock import patch, Mock

from app.dialog_validator import DialogValidator
from app.dto.game import Game as GameDto
from app.dto.meta import Meta as MetaDto
from app.dto.init import Init as InitDto
from app.game_creator import GameCreator
from app.game_loader import GameLoader
from app.game_player import GamePlayer
from helpers.GameTestHelper import GameTestHelper
from jfw.config import Config
from menu.create_edit_game import CreateEditGame
from menu.main import Main


class MainTestCaseTestCase(unittest.TestCase):
    def test_it_shows_the_main_menu_intro(self):
        with patch("builtins.print", Mock()) as mock_print:
            (Main(
                config=Mock(),
                create_edit_game=Mock(),
                game_loader=Mock(),
                game_player=Mock()
            )).show_intro()

            output = str(mock_print.call_args.args[0])
            self.assertIn('--=[ Welcome to the adventure player ]=--', output)
            self.assertIn('Let the adventure begin!', output)

    def test_it_shows_the_main_menu(self):
        with patch("builtins.input", return_value="") as mock_input:
            (Main(
                config=Mock(),
                create_edit_game=Mock(),
                game_loader=Mock(),
                game_player=Mock()
            )).show()

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

            (Main(
                config=config,
                create_edit_game=Mock(),
                game_loader=Mock(),
                game_player=Mock()
            )).show()

            output = str(mock_input.call_args.args[0])
            self.assertIn('Create or edit a game', output)

    def test_it_handles_load_game_menu_option(self):
        game_loader_mock = Mock()
        game_loader_mock.return_value = game_loader_mock

        game_player = Mock()
        game_player.return_value = game_player
        game_player.play = Mock()

        game = GameDto(
            meta=MetaDto(
                name="test game",
                description="test description",
                game_directory="test",
            ),
            state={
                "game_data_checksum": "",
                "system_data_checksum": "",
                "game_data": {},
                "system_data": {
                    "current_dialog": "main"
                }
            },
            init=InitDto(
                state={},
                dialog='main'
            )
        )

        game_loader_mock.available_games = Mock(return_value=[game])

        with (
            patch("builtins.print", Mock()),
            # First 1 = "Load game", Second 1 = "Test Game"
            patch("builtins.input", side_effect=["1", "1"]) as mock_input,
        ):
            config = Config('')
            game_test_helper = GameTestHelper(config=config)
            game_test_helper.setup_empty_temp_base_game_path()

            (Main(
                config=config,
                create_edit_game=Mock(),
                game_loader=game_loader_mock,
                game_player=game_player
            )).show()

            output_string = str(mock_input.call_args.args[0])
            self.assertIn('Choose a game', output_string)
            self.assertIn('test game', output_string)
            self.assertIn(' - ', output_string)
            self.assertIn('test description', output_string)

            game_player.play.assert_called_with(game)

    def test_it_handles_create_game_menu_option(self):
        create_edit_game_mock = Mock()
        create_edit_game_mock.show = create_edit_game_mock

        with (
            patch("builtins.print", Mock()),
            patch("builtins.input", side_effect=['4', '']),
        ):
            config = Config('')
            config.set('creator_mode', 1)

            game_test_helper = GameTestHelper(config=config)
            game_test_helper.setup_empty_temp_base_game_path()

            game_loader = GameLoader(config=config)

            (Main(
                config=config,
                create_edit_game=create_edit_game_mock,
                game_loader=game_loader,
                game_player=GamePlayer(
                    config=config,
                    dialog_validator=DialogValidator(
                        config=config
                    )
                )
            )).show()

            create_edit_game_mock.assert_called_once()
