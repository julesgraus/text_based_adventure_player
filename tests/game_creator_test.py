from unittest import TestCase

from app.game_creator import GameCreator
from app.game_loader import GameLoader
from jfw.Config import Config
from tests.helpers.GameTestHelper import GameTestHelper


class GameCreatorTestCase(TestCase):
    def test_it_creates_games(self):
        config = Config('')

        (GameTestHelper(config)
         .setup_empty_temp_base_game_path())

        GameCreator(config).create(
            name='test game',
            description='a game made for testing purposes'
        )

        games = GameLoader(config).available_games()
        self.assertEqual(1, len(games))
        self.assertEqual('test game', games[0].name())
        self.assertEqual('a game made for testing purposes', games[0].description())
