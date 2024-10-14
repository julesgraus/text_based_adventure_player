from glob import glob
from os.path import isfile
from pathlib import Path

from app.base_game_handler import BaseGameHandler
from app.dto.game import Game as GameDto
from terminal_utils.texts import Texts
from terminal_utils.foreground_color import ForegroundColor as Fg
from terminal_utils.background_color import BackgroundColor as Bg


class GameLoader(BaseGameHandler):
    def available_games(self):
        games = []

        for game_path in glob(f'{self._base_game_path}/*'):
            if isfile(game_path):
                continue

            game_file_path = Path(game_path).stem
            if not self.is_valid_game(game_file_path):
                continue

            games.append(self._load(game_file_path))

        games.reverse()
        return games

    def _load(self, name: str) -> GameDto:
        if self.is_valid_game(name=name) is False:
            raise ValueError('Game does not exist')

        meta = self._get_meta(name=name)
        state = self._get_state(name=name)
        init = self._get_init(name=name)

        if meta is False or state is False or init is False:
            print(Texts().add('meta, state, or init file(s) did not exist. Exiting', Fg.Bright_Red, Bg.Red))
            exit(1)

        if len(state['game_data']) == 0:
            state['game_data'] = init['state']
            self._write_state_file(state=state['game_data'], system_state=state['system_data'], name=name)

        return GameDto(
            meta=meta,
            state=state,
            init=init,
        )

    def reset_and_load(self, name: str) -> GameDto:
        if self.is_valid_game(name=name) is False:
            raise ValueError('Game does not exist')

        state = self._get_state(name=name)
        init = self._get_init(name=name)

        if init is False or state is False:
            print(Texts().add('init or state file(s) did not exist. Exiting', Fg.Bright_Red, Bg.Red))
            exit(1)

        state['data'] = init['state']
        self._write_state_file(state=state['game_data'], system_state=state['system_data'], name=name)

        return self._load(name)
