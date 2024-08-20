from os.path import isdir
from tempfile import gettempdir
from os import mkdir
from shutil import rmtree

from jfw.Config import Config


class GameTestHelper:
    def __init__(self, config: Config):
        self.tempdir = f'{gettempdir()}/test'
        self.config = config

    def setup_empty_temp_base_game_path(self):

        if isdir(self.tempdir):
            rmtree(self.tempdir)

        mkdir(self.tempdir)
        self.config.set('base_game_path', self.tempdir)

        return self
