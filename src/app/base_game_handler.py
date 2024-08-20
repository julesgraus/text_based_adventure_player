from json import loads
from os import makedirs
from os.path import exists
from zipfile import is_zipfile, ZipFile, Path as zipFilePath

from jfw.Config import Config
from jfw.validation.rules.max_rule import MaxRule
from jfw.validation.rules.min_rule import MinRule
from jfw.validation.rules.str_rule import StrRule
from jfw.validation.validator import Validator


class BaseGameHandler:
    def __init__(self, config: Config):
        self.base_game_path = config.get('base_game_path')

        if self.base_game_path is None:
            raise RuntimeError('base_game_path config setting not set')

        makedirs(self.base_game_path, exist_ok=True)

    def is_valid_game(self, name: str):
        if self._is_archived_game(name):
            return True

        return False

    def resolve_game_path(self, name: str):
        if exists(self._archived_game_path(name)):
            return self._archived_game_path(name)

        raise ValueError('The game does not exist')

    def _is_archived_game(self, name):
        if is_zipfile(self._archived_game_path(name)) is False:
            return False

        return self._contains_valid_meta(name)

    def _contains_valid_meta(self, name):
        meta_json = self._get_meta(name)
        if meta_json is False:
            return False
        if Validator(meta_json, {
            'name': [StrRule(), MinRule(1), MaxRule(255)],
            'description': [StrRule(), MinRule(1), MaxRule(255)]
        }).is_valid():
            return True

        return False

    def _get_meta(self, name) -> bool | dict:
        with ZipFile(self._archived_game_path(name), 'r') as archived_game:
            meta_file_path = zipFilePath(archived_game, 'meta.json')
            if meta_file_path.exists() is False:
                return False

            with meta_file_path.open('r') as meta_file:
                return loads(meta_file.read())

    def _archived_game_path(self, name: str):
        return f'{self.base_game_path}/{name}.tba'
