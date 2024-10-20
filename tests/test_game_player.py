import unittest
from unittest.mock import patch, Mock

from app.dialog_validator import DialogValidator
from app.dto.meta import Meta as MetaDto
from app.dto.game import Game as GameDto
from app.dto.init import Init as InitDto
from app.dto.system_data import SystemData
from app.game_creator import GameCreator
from app.game_loader import GameLoader
from app.game_player import GamePlayer
from jfw.config import Config
from jfw.container import Container
from tests.helpers.GameTestHelper import GameTestHelper


class TestGamePlayer(unittest.TestCase):
    def test_it_prints_that_it_cannot_resolve_a_dialog(self) -> None:
        config = Mock()
        dialog_validator = Mock()
        dialog_validator.validate = Mock(side_effect=[False])

        game_player = GamePlayer(
            config=config,
            dialog_validator=dialog_validator
        )

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
                "system_data": SystemData(
                    current_dialog="main"
                )
            },
            init=InitDto(
                state={},
                dialog='main'
            )
        )

        with patch("builtins.print", Mock()) as mock_print:
            game_player.play(game)
            output = str(mock_print.call_args.args[0])
            self.assertIn('Could not resolve dialog', output)

    def test_it_prints_validation_errors(self) -> None:
        config = Mock()
        dialog_validator = Mock()
        dialog_validator.is_valid = Mock(side_effect=[False])
        dialog_validator.validate = Mock(side_effect=[dialog_validator])
        dialog_validator.get_errors = Mock(side_effect=[['test validation error']])

        game_player = GamePlayer(
            config=config,
            dialog_validator=dialog_validator
        )

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
                "system_data": SystemData(
                    current_dialog="test dialog"
                )
            },
            init=InitDto(
                state={},
                dialog='main'
            )
        )

        with patch("builtins.print", Mock()) as mock_print:
            game_player.play(game)
            output = str(mock_print.call_args.args[0])
            self.assertIn('"test dialog" is invalid:', output)
            self.assertIn('test validation error', output)


if __name__ == '__main__':
    unittest.main()
