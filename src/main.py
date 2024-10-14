import argparse
from os.path import expanduser, dirname

from app.dialog_validator import DialogValidator
from app.game_creator import GameCreator
from app.game_loader import GameLoader
from app.game_player import GamePlayer
from jfw.config import Config
from jfw.exception_handler import ExceptionHandler
from jfw.kernel import Kernel
from jfw.logger import Logger
from menu.create_edit_game import CreateEditGame
from menu.main import Main as MainMenu

parser = argparse.ArgumentParser(description='A text based adventure player')
parser.add_argument('--creator',
                    default=False,
                    action='store_true',
                    help='Enable options to allow for game creation and editing'
                    )
args = parser.parse_args()

config = Config(dirname(__file__))
config.set('creator_mode', args.creator)

config.set('base_game_path', expanduser('~/Documents/AdventurePlayer'))

logger = Logger(config=config, log_name="app")
exception_handler = ExceptionHandler(logger=logger)
kernel = Kernel(exception_handler=exception_handler)
dialog_validator = DialogValidator(config=config)
game_loader = GameLoader(config=config)
game_creator = GameCreator(config=config)
create_edit_game = CreateEditGame(config=config, game_loader=game_loader, game_creator=game_creator)
game_player = GamePlayer(config=config, dialog_validator=dialog_validator)

mainMenu = MainMenu(
    config=config,
    create_edit_game=create_edit_game,
    game_loader=game_loader,
    game_player=game_player
)


def init():
    mainMenu.show_intro()
    mainMenu.show()


if __name__ == "__main__":
    kernel.handle(init)
