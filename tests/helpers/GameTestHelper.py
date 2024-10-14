from json import dumps
from os.path import isdir
from tempfile import gettempdir
from os import mkdir
from shutil import rmtree
from typing import AnyStr

from jfw.config import Config


class GameTestHelper:
    def __init__(self, config: Config):
        self.tempdir = f'{gettempdir()}/test'
        self.dialogDir = f'{gettempdir()}/test/dialogs'
        self.config = config

    def setup_empty_temp_base_game_path(self):
        if isdir(self.tempdir):
            rmtree(self.tempdir)

        mkdir(self.tempdir)

        self.config.set('base_game_path', self.tempdir)

        return self

    def create_dialog(self, game_name: str, dialog_name: str, dialog_file_contents: dict, txt_file_contents: AnyStr):
        if isdir(f'{self.tempdir}/') is False:
            raise RuntimeError(f'Game "{game_name}" does not exist')

        with (
            open(f'{self.tempdir}/{game_name}/dialogs/{dialog_name}.json', 'w+') as dialogFile,
            open(f'{self.tempdir}/{game_name}/dialogs/{dialog_name}.txt', 'w+') as txtFile
        ):
            dialogFile.write(dumps(dialog_file_contents))
            txtFile.write(dumps(txt_file_contents))
