from json import loads

from app.base_game_handler import BaseGameHandler
from app.dialog_validator import DialogValidator
from app.dto.game import Game as GameDto
from jfw.config import Config
from jfw.validation.validator import Validator
from terminal_utils.texts import Texts
from terminal_utils.foreground_color import ForegroundColor as Fg
from terminal_utils.background_color import BackgroundColor as Bg


class GamePlayer(BaseGameHandler):
    def __init__(self, config: Config, dialog_validator: DialogValidator):
        super().__init__(config)
        self._dialog_validator = dialog_validator

    def play(self, game: GameDto) -> None:
        if self._validate_current_dialog(game) is False:
            return

    def _validate_current_dialog(self, game: GameDto) -> bool:
        current_dialog_name = self._determine_current_dialog(game)

        validator_or_false = self._dialog_validator.validate(name=game["meta"]["name"], dialog_name=current_dialog_name)

        if validator_or_false is False:
            print((Texts().add(f'Could not resolve dialog', Fg.Bright_Red, Bg.Red)))
            return False

        if self._print_dialog_validation_errors_if_invalid(
                dialog_name=current_dialog_name,
                validator=validator_or_false
        ) is False:
            return False

        return True

    def _determine_current_dialog(self, game: GameDto):
        system_data = game['state']['system_data']
        current_dialog = system_data['current_dialog']

        if current_dialog is None:
            system_data['current_dialog'] = game['init']['dialog']
            self._write_state_file(state=game['state']['game_data'], system_state=system_data,
                                   name=game['meta']['name'])

        return system_data['current_dialog']

    def _get_dialog_text(self, name: str) -> str:
        with (open(file=f'{self.game_path_or_error(name=name)}/dialogs/{name}.txt', mode='r')) as dialog_txt_file:
            return loads(dialog_txt_file.read())

    def _print_dialog_validation_errors_if_invalid(self, dialog_name: str, validator: Validator) -> bool:
        if validator.is_valid():
            return False

        validation_message = (Texts()
                              .add(f'Dialog "{dialog_name}" is invalid: \n'))

        for message in validator.get_errors():
            validation_message.add(f'  - {message}\n', Fg.Bright_Red)
        validation_message.add('\n')

        print(validation_message, Fg.Bright_Red, Bg.Red)

        return True
