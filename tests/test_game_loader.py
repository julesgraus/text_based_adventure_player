import unittest
from os import rmdir
from os.path import exists
from shutil import rmtree
from tempfile import gettempdir

from app.game_creator import GameCreator
from app.game_loader import GameLoader
from jfw.config import Config
from tests.helpers.GameTestHelper import GameTestHelper


class TestGameLoader(unittest.TestCase):
    def test_it_can_determine_that_a_game_does_not_exist_because_it_is_invalid(self) -> None:
        config = Config('')

        GameTestHelper(config).setup_empty_temp_base_game_path()

        game_loader = GameLoader(config)
        self.assertFalse(game_loader.is_valid_game('test game'))

    def test_it_can_determine_that_a_game_does_exist_and_is_valid(self) -> None:
        config = Config('')

        GameTestHelper(config).setup_empty_temp_base_game_path()

        game_creator = GameCreator(config)
        game_creator.create(
            name='test game',
            description='test description'
        )

        game_loader = GameLoader(config)

        self.assertTrue(game_loader.is_valid_game('test game'))

    def test_it_finds_the_games_in_the_base_game_path(self) -> None:
        config = Config('')

        game_loader_test_helper = GameTestHelper(config)
        game_loader_test_helper.setup_empty_temp_base_game_path()

        game_creator = GameCreator(config)
        game_creator.create('first game', 'first description')
        game_creator.create('second game', 'second description')

        game_loader = GameLoader(config)

        available_games = game_loader.available_games()
        state = available_games[0]['state']

        self.assertEqual(2, len(available_games))
        self.assertEqual('first game', available_games[1]['meta']['name'])
        self.assertEqual('second game', available_games[0]['meta']['name'])
        self.assertIn('game_data_checksum', state)
        self.assertIn('system_data_checksum', state)
        self.assertIn('game_data', state)
        self.assertIn('system_data', state)
        self.assertIn('state_variable', state['game_data'])
        self.assertIn('current_dialog', state['system_data'])
        self.assertEqual(1, state['game_data']['state_variable'])


if __name__ == '__main__':
    unittest.main()
