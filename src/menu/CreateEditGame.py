from curses.ascii import isdigit

from app.game_creator import GameCreator
from app.game_loader import GameLoader
from jfw.Config import Config
from terminal_utils.texts import Texts
from terminal_utils.foreground_color import ForegroundColor as Fg
from terminal_utils.utils import clear


class CreateEditGame:
    def __init__(self, config: Config):
        self._config = config

    def show(self) -> None:
        clear()
        prompt = Texts()
        game_loader = GameLoader(config=self._config)

        available_games = game_loader.available_games()
        available_game_count = len(available_games)
        create_game_option = available_game_count + 1

        if available_game_count > 0:
            (prompt.add('Choose a game to edit or choose option ')
             .add(str(create_game_option), Fg.Yellow)
             .add(' to create a new game\n\n'))
        else:
            self._show_create_game()
            return

        game_counter = 1
        for game_name in game_loader.available_games():
            prompt.add(str(game_counter), Fg.Yellow).add(f') {game_name}\n')
            game_counter = game_counter + 1

        prompt.add(str(create_game_option), Fg.Yellow).add(f') Create a new game\n')
        prompt.add('\n')

        answer = input(prompt)


        clear()
        if answer.isdigit():
            if int(answer) is create_game_option:
                self._show_create_game()
                print(Texts().add('\nGame created successfully. ', Fg.Bright_Green))
                self.show()
            else:
                self._show_edit_game(available_games[int(answer) - 1])

        return None

    def _show_create_game(self):
        name = input(Texts()
                     .add('What is the ')
                     .add('name', Fg.Yellow)
                     .add(' of your new game?\n')
                     )

        description = input(Texts()
                            .add('What is the ')
                            .add('description', Fg.Yellow)
                            .add(' of your new game?\n')
                            )

        game_creator = GameCreator(config=self._config)
        result = game_creator.create(name, description)

        if result is True:
            return True
        elif result is False:
            print(Texts().add('The game could not be created\n', Fg.Bright_Red))
        elif type(result) is list:
            clear()

            validation_message = (Texts()
                                  .add('There were some errors when filling out the questions. Please try again: \n'))
            for message in result:
                validation_message.add(f'  - {message}\n', Fg.Bright_Red)
            validation_message.add('\n')

            print(validation_message)
            self._show_create_game()
        pass

    def _show_edit_game(self, game_name: str) -> None:
        clear()

        prompt = (Texts()
         .add('You did choose ').add(game_name, Fg.Yellow).add('. What do you want to edit?\n\n')
         .add('1', Fg.Yellow).add(') Game name\n')
         .add('2', Fg.Yellow).add(') Description\n')
         )

        answer = input(prompt)

        match answer:
            case "1":
                print('Todo implement edit game name')
                exit()
            case "2":
                print('Todo implement edit game description')
                exit()

        return None
