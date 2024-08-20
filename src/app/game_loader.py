import os.path
from glob import glob
from os.path import isfile, basename
from pathlib import Path

from app.base_game_handler import BaseGameHandler
from app.dto.Game import Game as GameDto
from app.Game import Game


class GameLoader(BaseGameHandler):

    def load(self, name) -> Game:
        if self.is_valid_game(name) is False:
            raise ValueError('Game does not exist')

        meta = self._get_meta(name)

        return Game(GameDto(
            name=meta['name'],
            description=meta['description']
        ))

    def available_games(self):
        names = []

        for game_path in glob(f'{self.base_game_path}/*.tba'):
            if not isfile(game_path):
                continue

            game_name = Path(game_path).stem
            if not self.is_valid_game(game_name):
                continue

            names.append(game_name)

        names.reverse()
        return names
