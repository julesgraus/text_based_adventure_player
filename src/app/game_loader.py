from glob import glob
from os.path import isfile, basename
from pathlib import Path

from app.base_game_handler import BaseGameHandler
from app.dto.Game import Game as GameDto
from app.Game import Game


class GameLoader(BaseGameHandler):
    def available_games(self):
        games = []

        for game_path in glob(f'{self.base_game_path}/*.tba'):
            if not isfile(game_path):
                continue

            game_file_path = Path(game_path).stem
            if not self.is_valid_game(game_file_path):
                continue

            games.append(self._load(game_file_path))

        games.reverse()
        return games

    def _load(self, file_name) -> Game:
        if self.is_valid_game(file_name) is False:
            raise ValueError('Game does not exist')

        meta = self._get_meta(file_name)

        return Game(GameDto(
            file_name=file_name,
            file_path=self.resolve_game_path(file_name),
            name=meta['name'],
            description=meta['description']
        ))
