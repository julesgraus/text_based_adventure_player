from os import mkdir
from os.path import dirname, isdir
from pathlib import Path

from app.base_game_handler import BaseGameHandler
from app.dto.meta import Meta as MetaDto
from jfw.config import Config
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
            'description': description,
        }, {
            'name': [MinRule(1), MaxRule(255)],
            'description': [MinRule(1), MaxRule(1024)],
        })

        if not validator.is_valid():
            return validator.get_errors()

        return self._create_game(name, description)

    def _create_game(self, name: str, description: str) -> bool:
        dir = self._game_path(name)

        if isdir(dir):
            raise RuntimeError(f'Game "{name}" already exists')
        else:
            mkdir(dir)

        self._write_meta_file(meta=MetaDto(
            description=description,
            name=name,
            game_directory=dir
        ), name=name)

        self._write_state_file(state={}, name=name)
        self._write_new_init_file(name=name)
        self._make_dialog(dialog_name="main", name=name)

        return True

    def _write_new_init_file(self, name: str) -> None:
        with open(Path(f'{dirname(__file__)}/../stubs/init.stub.json').resolve(), 'r') as init_file:
            init_file_data = self._replace_stub_variables(
                stub_content=init_file.read(),
                replacements={"dialog_file_name": 'main'}
            )

            with open(f'{self.game_path_or_error(name)}/init.json', 'w+') as file:
                file.write(init_file_data)

    def _make_dialog(self, dialog_name: str, name: str) -> None:
        with (
            open(Path(f'{dirname(__file__)}/../stubs/dialog.stub.json').resolve(), 'r') as dialog_file,
            open(Path(f'{dirname(__file__)}/../stubs/dialog.stub.txt').resolve(), 'r') as txt_file
        ):
            txt_file_stub_data = self._replace_stub_variables(
                stub_content=txt_file.read(),
                replacements={"dialog_file_name": dialog_name, "init_file_name": "init"}
            )

            dialog_file_stub_data = self._replace_stub_variables(
                stub_content=dialog_file.read(),
                replacements={"dialog_file_name": dialog_name}
            )

            dialogs_path = f'{self.game_path_or_error(name=name)}/dialogs'
            if isdir(dialogs_path) is False:
                mkdir(dialogs_path)

            with (
                open(f'{self.game_path_or_error(name=name)}/dialogs/{dialog_name}.json', 'w+') as dialogFile,
                open(f'{self.game_path_or_error(name=name)}/dialogs/{dialog_name}.txt', 'w+') as txtFile
            ):
                dialogFile.write(dialog_file_stub_data)
                txtFile.write(txt_file_stub_data)

    def _replace_stub_variables(self, stub_content: str, replacements: dict) -> str:
        for search in replacements:
            stub_content = stub_content.replace(f'<{search}>', replacements[search])

        return stub_content
