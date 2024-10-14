from json import loads
from os.path import isfile

from app.base_game_handler import BaseGameHandler
from jfw.validation.rules.ends_with_rule import EndsWithRule
from jfw.validation.rules.max_rule import MaxRule
from jfw.validation.rules.min_rule import MinRule
from jfw.validation.rules.required_rule import RequiredRule
from jfw.validation.rules.str_rule import StrRule
from jfw.validation.validator import Validator


class DialogValidator(BaseGameHandler):
    def validate(self, name: str, dialog_name: str) -> Validator | bool:
        txt_path_exists = isfile(self._dialog_txt_file_path(name, dialog_name))

        dialog_file_path = self._dialog_file_path(name, dialog_name)
        dialog_path_exists = isfile(dialog_file_path)

        if txt_path_exists is False or dialog_path_exists is False:
            return False

        with (open(file=dialog_file_path, mode='r')) as dialog_file:
            contents = loads(dialog_file.read())

            validator = Validator(contents, {
                'text': [RequiredRule(), StrRule(), MinRule(1), MaxRule(255), EndsWithRule('.txt')],
            })

            return validator

    def _dialog_txt_file_path(self, name: str, dialog_name: str) -> str:
        return f'{self.game_path_or_error(name=name)}/dialogs/{dialog_name}.txt'

    def _dialog_file_path(self, name: str, dialog_name: str) -> str:
        return f'{self.game_path_or_error(name=name)}/dialogs/{dialog_name}.json'
