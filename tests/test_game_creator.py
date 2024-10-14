from unittest import TestCase

from app.game_creator import GameCreator
from app.game_loader import GameLoader
from jfw.config import Config
from tests.helpers.GameTestHelper import GameTestHelper


class TestGameCreator(TestCase):
    def test_it_creates_games(self):
        config = Config('')

        game_test_helper = (GameTestHelper(config)
                            .setup_empty_temp_base_game_path())

        GameCreator(config).create(
            name='test game',
            description='a game made for testing purposes'
        )

        game_loader = GameLoader(config)
        games = game_loader.available_games()
        self.assertEqual(1, len(games))

        # Assert meta
        self.assertEqual('test game', games[0]['meta']['name'])
        self.assertEqual('a game made for testing purposes', games[0]['meta']['description'])
        self.assertIn(f'{game_test_helper.tempdir}/test game', games[0]['meta']['game_directory'])

        # State
        self.assertEqual({'state_variable': 1}, games[0]['state']['game_data'])
        self.assertEqual({'current_dialog': None}, games[0]['state']['system_data'])
        self.assertEqual(game_loader._dict_hash({}), games[0]['state']['game_data_checksum'])
        self.assertEqual(game_loader._dict_hash({'current_dialog': None}), games[0]['state']['system_data_checksum'])

        # Init
        self.assertEqual(1, games[0]['init']['state']['state_variable'])
        self.assertEqual('main', games[0]['init']['dialog'])
