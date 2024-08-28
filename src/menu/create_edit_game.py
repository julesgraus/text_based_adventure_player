import textwrap
from zipfile import ZipFile

from app.game import Game
from app.base_game_handler import BaseGameHandler
from app.game_creator import GameCreator
from app.game_loader import GameLoader
from jfw.config import Config
from terminal_utils.texts import Texts
from terminal_utils.foreground_color import ForegroundColor as Fg
from terminal_utils.utils import clear
from textwrap import shorten


class CreateEditGame(BaseGameHandler):
    def __init__(self, config: Config):
        super().__init__(config)
        self._config = config

    def show(self) -> None:
        prompt = Texts()
        game_loader = GameLoader(config=self._config)

        available_games = game_loader.available_games()
        available_game_count = len(available_games)
        create_game_option = available_game_count + 1
        back_to_main_menu_option = available_game_count + 2

        if available_game_count > 0:
            (prompt.add('Choose a game to edit or choose option ')
             .add(str(create_game_option), Fg.Yellow)
             .add(' to create a new game\n\n'))
        else:
            self._show_create_game()
            return

        game_counter = 1
        for game in available_games:
            (prompt.add(str(game_counter), Fg.Yellow).add(f') {game.name()}')
             .add(' - ')
             .add(f'{shorten(game.description(), 120)}\n', Fg.Blue))

            game_counter = game_counter + 1

        (prompt.add(str(create_game_option), Fg.Yellow).add(f') Create a new game\n')
         .add(str(back_to_main_menu_option), Fg.Yellow).add(f') Back to main menu\n')
         .add('\n'))

        answer = input(prompt)

        clear()
        if answer.isdigit():
            if int(answer) is create_game_option:
                self._show_create_game()
                print(Texts().add('\nGame created successfully. ', Fg.Bright_Green))
                clear()
                self.show()
            elif int(answer) is back_to_main_menu_option:
                return None
            else:
                clear()
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

    def _show_edit_game(self, game: Game) -> None:
        prompt = (Texts()
                  .add('You did choose ').add(game.name(), Fg.Yellow).add('. What do you want to edit?\n\n')
                  .add('1', Fg.Yellow).add(') Game name\n')
                  .add('2', Fg.Yellow).add(') Description\n')
                  .add('3', Fg.Yellow).add(') Back to main menu\n')
                  )

        answer = input(prompt)

        match answer:
            case "1":
                clear()
                self._show_and_handle_edit_name(game)
                self.show()
            case "2":
                clear()
                self._show_and_handle_edit_description(game)
                self.show()

        return None

    def _show_and_handle_edit_name(self, game: Game):
        new_name = input(Texts()
                         .add('Type the new ')
                         .add('name', Fg.Yellow)
                         .add(' or press enter to keep ')
                         .add(game.name(), Fg.Green)
                         .add('\n'))

        if new_name == game.name():
            return

        meta = self._get_meta(game.file_name())

        with ZipFile(self._archived_game_path(game.file_name()), 'w') as zip_file:
            self._write_meta_file(
                description=meta['description'],
                name=new_name,
                zip_file=zip_file
            )

        clear()
        print(Texts().add('The name is updated successfully', Fg.Green))

    def _show_and_handle_edit_description(self, game: Game):
        new_description = input(Texts()
                                .add('Type the new ')
                                .add('description', Fg.Yellow)
                                .add(' or press enter to keep the description: ')
                                .add(game.description(), Fg.Green)
                                .add('\n'))

        if new_description == game.description():
            return

        meta = self._get_meta(game.file_name())

        with ZipFile(self._archived_game_path(game.file_name()), 'w') as zip_file:
            self._write_meta_file(
                description=new_description,
                name=meta['name'],
                zip_file=zip_file
            )

        clear()
        print(Texts().add('The description is updated successfully', Fg.Green))
