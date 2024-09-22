from json import loads, dumps
from os import makedirs
from os.path import isdir
from typing import Dict, Any
import hashlib
from app.dto.init import Init as InitDto
from app.dto.meta import Meta as MetaDto
from app.dto.state import State as StateDto

from jfw.config import Config
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
        if isdir(self._game_path(name=name)) is False:
            return False

        if self._contains_valid_meta(name):
            return True

        return False

    def game_path_or_error(self, name: str) -> str | bool:
        if isdir(self._game_path(name)):
            return self._game_path(name)

        raise ValueError(f'The game ({self._game_path(name)}) does not exist')

    def _contains_valid_meta(self, game_file_name: str):
        meta_json = self._get_meta(game_file_name)

        return meta_json is not False and Validator(meta_json, {
            'name': [StrRule(), MinRule(1), MaxRule(255)],
            'description': [StrRule(), MinRule(1), MaxRule(255)]
        }).is_valid()

    def _get_meta(self, name: str) -> bool | MetaDto:
        with (open(file=f'{self.game_path_or_error(name=name)}/meta.json', mode='r')) as meta_file:
            contents = loads(meta_file.read())

        return MetaDto(**contents)

    def _get_init(self, name: str) -> bool | InitDto:
        with (open(file=f'{self.game_path_or_error(name=name)}/init.json', mode='r')) as init_file:
            contents = loads(init_file.read())

        return InitDto(**contents)

    def _get_state(self, name: str) -> bool | StateDto:
        with (open(file=f'{self.game_path_or_error(name=name)}/state.json', mode='r')) as state_file:
            contents = loads(state_file.read())

        if contents['checksum'] != self._dict_hash(contents['data']):
            raise RuntimeError('invalid state')

        return StateDto(**contents)

    def _get_dialog(self, name: str, game_name: str) -> bool | dict:
        with (open(file=f'{self._game_path(name=game_name)}/dialogs{name}.json', mode='r')) as dialog_file:
            contents = loads(dialog_file.read())

        return contents

    def _write_meta_file(self, meta: MetaDto, name: str) -> None:
        with (open(file=f'{self._game_path(name=name)}/meta.json', mode='w')) as dialog_file:
            dialog_file.write(dumps(meta))

    def _write_state_file(self, state: dict[str, any], name: str) -> None:
        with open(f'{self._game_path(name=name)}/state.json', "w") as file:
            file.write(dumps(StateDto(
                checksum=self._dict_hash(state),
                data=state
            )))

    def _game_path(self, name: str) -> str:
        return f'{self.base_game_path}/{name}'

    def _dict_hash(self, dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.sha256()
        # We need to sort arguments so {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()
