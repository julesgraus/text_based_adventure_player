from app.dto.Game import Game as GameDto


class Game:
    def __init__(self, game_dto: GameDto):
        self._game_dto = game_dto

    def name(self) -> str:
        return self._game_dto.get('name')

    def description(self) -> str:
        return self._game_dto.get('description')
