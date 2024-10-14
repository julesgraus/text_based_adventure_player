import unittest
from unittest.mock import patch

from app.dialog_validator import DialogValidator
from app.game_creator import GameCreator
from app.game_loader import GameLoader
from app.game_player import GamePlayer
from jfw.config import Config
from jfw.container import Container
from tests.helpers.GameTestHelper import GameTestHelper


class GamePlayerTestCase(unittest.TestCase):
    def test_it_prints_that_it_cannot_resolve_a_dialog(self) -> None:
        config = Config('')

        game_loader_test_helper = GameTestHelper(config)
        game_loader_test_helper.setup_empty_temp_base_game_path()

        game_creator = GameCreator(config)
        game_creator.create('a game', 'a description')

        game_loader = GameLoader(config)

        game = game_loader.available_games()[0]
        game['state']['system_data']['current_dialog'] = 'doesnotexist'

        game_player = GamePlayer(config=config, dialog_validator=DialogValidator(config=config))

        with patch("builtins.print", return_value="") as mock_input:
            game_player.play(game)

            output = str(mock_input.call_args.args[0])

            self.assertIn('Could not resolve dialog', output)

    def test_it_prints_validation_errors(self) -> None:
        container = Container()

        config = Config('')
        container.bind('config', config)

        game_test_helper = GameTestHelper(config)
        game_test_helper.setup_empty_temp_base_game_path()

        dialog_validator = DialogValidator(config=config)

        container.bind('dialog_validator', dialog_validator)

        with (
            patch("builtins.print", return_value="") as mock_output,
        ):
            game_creator = GameCreator(config=config)
            game_creator.create('test_game', 'test_description')

            game_test_helper.create_dialog(
                game_name="test_game",
                dialog_name='test_dialog',
                dialog_file_contents={},
                txt_file_contents=""
            )

            game_loader = GameLoader(config=config)

            game = game_loader.available_games()[0]
            game['state']['system_data']['current_dialog'] = 'test_dialog'

            game_player = GamePlayer(config=config, dialog_validator=DialogValidator(config=config))

            game_player.play(game)

            # the mock output are Text class instances which can be converted to strings.
            output_string = "".join(map(lambda x: str(x), mock_output.call_args[0]))
            self.assertIn('"test_dialog" is invalid', output_string)
            self.assertIn('text is required', output_string)


if __name__ == '__main__':
    unittest.main()
