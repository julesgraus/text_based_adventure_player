import unittest
from os import rmdir
from os.path import exists
from shutil import rmtree
from tempfile import gettempdir

from app.game_creator import GameCreator
from app.game_loader import GameLoader
from jfw.Config import Config
from tests.helpers.GameTestHelper import GameTestHelper


class GameLoaderTestCase(unittest.TestCase):
    def test_it_creates_the_base_game_path_on_init(self) -> None:
        tempdir = f'{gettempdir()}/test'

        if exists(tempdir):
            rmtree(tempdir)

        self.assertFalse(exists(tempdir))

        config = Config('')
        config.set('base_game_path', tempdir)

        GameLoader(config)

        self.assertTrue(exists(tempdir))
        rmdir(tempdir)
        self.assertFalse(exists(tempdir))

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
        self.assertEqual(2, len(available_games))
        self.assertEqual('first game', available_games[0].name())
        self.assertEqual('second game', available_games[1].name())


if __name__ == '__main__':
    unittest.main()
