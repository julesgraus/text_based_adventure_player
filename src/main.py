import argparse
from os.path import expanduser, dirname

from jfw.Config import Config
from jfw.ExceptionHandler import ExceptionHandler
from jfw.Kernel import Kernel
from jfw.Container import Container
from jfw.Logger import Logger
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

container = Container()
container.bind('config', config)
container.bind('logger', Logger(container.resolve('config'), 'app'))
container.bind('exception_handler', ExceptionHandler(container.resolve('logger')))

kernel = Kernel(container.resolve('exception_handler'))

mainMenu = MainMenu(config)


def init():
    mainMenu.show_intro()
    mainMenu.show()


if __name__ == "__main__":
    kernel.handle(init)
