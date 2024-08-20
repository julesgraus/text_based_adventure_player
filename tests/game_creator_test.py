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

        game = GameLoader(config).load('test game')

        self.assertEqual('test game', game.name())
        self.assertEqual('a game made for testing purposes', game.description())
