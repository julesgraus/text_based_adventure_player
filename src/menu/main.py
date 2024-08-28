from textwrap import shorten

from app.game_loader import GameLoader
from jfw.config import Config
from menu.create_edit_game import CreateEditGame
from terminal_utils.texts import Texts
from terminal_utils.utils import clear
from terminal_utils.foreground_color import ForegroundColor as Fg
from terminal_utils.background_color import BackgroundColor as Bg
from terminal_utils.style import Style as Style


class Main:
    def __init__(self, config: Config):
        self._config = config

    def show_intro(self):
        clear()
        print(Texts()
              .add('--=[ Welcome to the adventure player ]=--', Fg.Bright_Green, style=Style.Bold)
              .add('\n')
              .add('Let the adventure begin!\n\n', Fg.Green))

    def show(self) -> None:
        options = (Texts()
                   .add('What is it that you ').add('want to', Fg.Yellow).add(' do?\n\n')
                   .add('1', Fg.Yellow).add(') Load a game\n')
                   .add('2', Fg.Yellow).add(') Exit\n'))

        if self._config.get('creator_mode'):
            options.add('3', Fg.Yellow).add(') Create or edit a game\n')

        answer = input(options)
        if answer.isdigit():
            return self._handle(int(answer))

    def _handle(self, answer: int) -> None:
        match answer:
            case 1:
                clear()
                self._load_game()
            case 2:
                self._exit()
            case 3:
                if self._config.get('creator_mode'):
                    clear()
                    CreateEditGame(self._config).show()
                    self.show_intro()
                    self.show()
            case _:
                clear()
                print(Texts()
                      .add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
                self.show()

    def _load_game(self) -> None:
        game_loader = GameLoader(config=self._config)
        available_games = game_loader.available_games()

        prompt = Texts().add('Choose a game\n\n')

        back_to_main_menu_option = len(available_games) + 1

        for key, game in enumerate(available_games):
            (prompt.add(str(key + 1), Fg.Yellow).add(f') {game.name()}')
             .add(' - ')
             .add(f'{shorten(game.description(), 120)}\n', Fg.Blue))

        prompt.add(str(back_to_main_menu_option), Fg.Yellow).add(') Back to main menu\n')

        answer = input(prompt)

        clear()
        if answer.isdigit():
            answer = int(answer)
            if answer == back_to_main_menu_option:
                self.show()
            elif 0 < answer <= len(available_games):
                game = available_games[answer - 1]
                print(f'Loaded {game.name()}')
            else:
                print(Texts().add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
                self._load_game()
        else:
            print(Texts().add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
            self._load_game()

    def _exit(self) -> None:
        clear()
        print(Texts().add('See you next time!', Fg.Blue))
        exit(0)
