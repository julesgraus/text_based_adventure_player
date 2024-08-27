from json import dumps
from typing import List
from zipfile import ZipFile

from app.base_game_handler import BaseGameHandler
from jfw.Config import Config
from jfw.validation.rules.max_rule import MaxRule
from jfw.validation.rules.min_rule import MinRule
from jfw.validation.validator import Validator


class GameCreator(BaseGameHandler):
    def __init__(self, config: Config):
        super().__init__(config=config)

    def create(self, name: str, description: str) -> list[str] | bool:
        if self.is_valid_game(name):
            return ['The game already exists']

        validator = Validator({
            'name': name,
            'description': description
        }, {
            'name': [MinRule(1), MaxRule(255)],
            'description': [MinRule(1), MaxRule(1024)]
        })

        if not validator.is_valid():
            return validator.get_errors()

        return self._create_game(name, description)

    def _create_game(self, name, description) -> bool:
        with ZipFile(self._archived_game_path(name), 'w') as zip_file:
            self._write_meta_file(description, name, zip_file)

        return True
