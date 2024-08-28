from app.dto.game import Game as GameDto


class Game:
    def __init__(self, game_dto: GameDto):
        self._game_dto = game_dto

    def name(self) -> str:
        return self._game_dto.get('name')

    def description(self) -> str:
        return self._game_dto.get('description')

    def file_name(self) -> str:
        return self._game_dto.get('file_name')

    def file_path(self) -> str:
        return self._game_dto.get('file_path')
