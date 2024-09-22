from app.dto.game import Game as GameDto


class GamePlayer:
    def play(self, game: GameDto):
        print(f'Play {game['meta']['name']}')
        pass