from curses.ascii import isdigit

from jfw.Config import Config
from menu.CreateEditGame import CreateEditGame
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
              .add('The text based adventure player\n\n', Fg.Green))

    def show(self) -> None:
        clear()
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
                self._load_game()
            case 2:
                self._exit()
            case 3:
                if self._config.get('creator_mode'):
                    CreateEditGame(self._config).show()
                    self.show_intro()
                    self.show()
            case _:
                clear()
                print(Texts()
                      .add('\nInvalid choice. Try again\n', Fg.Bright_Red, Bg.Red))
                self.show()

    def _load_game(self) -> None:
        clear()
        print(Texts().add('Implement load game', Fg.Blue))

    def _exit(self) -> None:
        clear()
        print(Texts().add('See you next time!', Fg.Blue))
        exit(0)
