from jfw.ExceptionHandler import ExceptionHandler
from terminal_utils.utils import clear


class Kernel:
    exceptionHandler: ExceptionHandler

    def __init__(self, exception_handler: ExceptionHandler):
        self.exceptionHandler = exception_handler

    def handle(self, callback: callable) -> None:
        try:
            clear()
            callback()
        except (KeyboardInterrupt, SystemExit):
            pass
        except BaseException as e:
            self.exceptionHandler.handle(e)
