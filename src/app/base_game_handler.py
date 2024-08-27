from json import loads, dumps
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

    def is_valid_game(self, game_file_name: str):
        if self._is_archived_game(game_file_name):
            return True

        return False

    def resolve_game_path(self, name: str):
        if exists(self._archived_game_path(name)):
            return self._archived_game_path(name)

        raise ValueError('The game does not exist')

    def _is_archived_game(self, game_file_name: str):
        if is_zipfile(self._archived_game_path(game_file_name)) is False:
            return False

        return self._contains_valid_meta(game_file_name)

    def _contains_valid_meta(self, game_file_name: str):
        meta_json = self._get_meta(game_file_name)
        if meta_json is False:
            return False
        if Validator(meta_json, {
            'name': [StrRule(), MinRule(1), MaxRule(255)],
            'description': [StrRule(), MinRule(1), MaxRule(255)]
        }).is_valid():
            return True

        return False

    def _get_meta(self, game_file_name: str) -> bool | dict:
        with ZipFile(self._archived_game_path(game_file_name), 'r') as archived_game:
            meta_file_path = zipFilePath(archived_game, 'meta.json')
            if meta_file_path.exists() is False:
                return False

            with meta_file_path.open('r') as meta_file:
                return loads(meta_file.read())

    def _write_meta_file(self, description: str, name: str, zip_file: ZipFile) -> None:
        zip_file.writestr('meta.json', dumps({
            "name": name,
            "description": description
        }))

    def _archived_game_path(self, game_file_name: str):
        return f'{self.base_game_path}/{game_file_name}.tba'
