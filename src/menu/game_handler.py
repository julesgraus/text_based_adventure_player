from app.base_game_handler import BaseGameHandler
from app.game_loader import GameLoader
from jfw.Config import Config
from terminal_utils.texts import Texts
from terminal_utils.foreground_color import ForegroundColor as Fg
from terminal_utils.utils import clear
from textwrap import shorten


class GameHandler(BaseGameHandler):
    def __init__(self, config: Config):
        super().__init__(config)
        self._config = config

    def show(self) -> None:
        prompt = Texts()
        game_loader = GameLoader(config=self._config)

        available_games = game_loader.available_games()
        available_game_count = len(available_games)
        back_to_main_menu_option = available_game_count + 1

        if available_game_count is 0:
            print(prompt.add('There are no games to load.'))
            return None

        game_counter = 1
        for game in game_loader.available_games():
            (prompt.add(str(game_counter), Fg.Yellow).add(f') {game.name()}')
             .add(' - ')
             .add(f'{shorten(game.description(), 120)}\n', Fg.Blue))

            game_counter = game_counter + 1

        (prompt.add(str(back_to_main_menu_option), Fg.Yellow).add(f') Back to main menu\n')
         .add('\n'))

        answer = input(prompt)

        clear()
        if answer.isdigit():
            if int(answer) == back_to_main_menu_option:
                return None

            return self._load(available_games[int(answer) - 1])

        return None
