from textwrap import shorten

from app.game_loader import GameLoader
from app.game_player import GamePlayer
from jfw.config import Config
from menu.create_edit_game import CreateEditGame
from terminal_utils.texts import Texts
from terminal_utils.utils import clear
from terminal_utils.foreground_color import ForegroundColor as Fg
from terminal_utils.background_color import BackgroundColor as Bg
from terminal_utils.style import Style as Style
from sys import exit


class Main:
    def __init__(self, config: Config, create_edit_game: CreateEditGame, game_loader: GameLoader, game_player: GamePlayer):
        self._config = config
        self._create_edit_game = create_edit_game
        self._game_loader = game_loader
        self._game_player = game_player

    def show_intro(self):
        print(Texts()
              .add('--=[ Welcome to the adventure player ]=--', Fg.Bright_Green, style=Style.Bold)
              .add('\n')
              .add('Let the adventure begin!\n\n', Fg.Green))

    def show(self) -> None:
        options = (Texts()
                   .add('What is it that you ').add('want to', Fg.Yellow).add(' do?\n\n')
                   .add('1', Fg.Yellow).add(') Load a game\n')
                   .add('2', Fg.Yellow).add(') Reset a game\n')
                   .add('3', Fg.Yellow).add(') Exit\n'))

        if self._config.get('creator_mode') == 1:
            options.add('4', Fg.Yellow).add(') Create or edit a game\n')

        answer = input(options)
        if answer.isdigit():
            return self._handle(int(answer))

    def _handle(self, answer: int) -> None:
        match answer:
            case 1:
                clear()
                self._load_game()
            case 2:
                self._reset_and_load_game()
            case 3:
                self._exit()
            case 4:
                if self._config.get('creator_mode'):
                    clear()
                    self._create_edit_game.show()
                    self.show_intro()
                    self.show()
            case _:
                clear()
                print(Texts()
                      .add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
                self.show()

    def _load_game(self) -> None:
        available_games = self._game_loader.available_games()

        answer, back_to_main_menu_option = self._prompt_for_game(available_games)

        clear()
        if answer.isdigit():
            answer = int(answer)
            if answer == back_to_main_menu_option:
                self.show()
            elif 0 < answer <= len(available_games):
                game = available_games[answer - 1]
                self._game_player.play(game)
            else:
                print(Texts().add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
                self._load_game()
        else:
            print(Texts().add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
            self._load_game()

    def _reset_and_load_game(self) -> None:
        clear()
        available_games = self._game_loader.available_games()
        answer, back_to_main_menu_option = self._prompt_for_game(available_games)

        clear()
        if answer.isdigit():
            answer = int(answer)
            if 0 < answer <= len(available_games):
                game = available_games[answer - 1]
                self._game_loader.reset_and_load(name=game['meta']['name'])
                print(Texts().add('\nGame reset.\n', Fg.Bright_Green))
                self.show()
            else:
                print(Texts().add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
                self._reset_and_load_game()
        else:
            print(Texts().add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
            self._reset_and_load_game()

    def _prompt_for_game(self, available_games):
        prompt = Texts().add('Choose a game\n\n')
        back_to_main_menu_option = len(available_games) + 1
        for key, game in enumerate(available_games):
            (prompt.add(str(key + 1), Fg.Yellow).add(f') {game['meta']['name']}')
             .add(' - ')
             .add(f'{shorten(game['meta']['description'], 120)}\n', Fg.Blue))
        prompt.add(str(back_to_main_menu_option), Fg.Yellow).add(') Back to main menu\n')
        answer = input(prompt)
        return answer, back_to_main_menu_option

    def _exit(self) -> None:
        clear()
        print(Texts().add('See you next time!', Fg.Blue))
        exit(0)
