from typing import LiteralString
from time import localtime, strftime
from jfw.config import Config


class Logger:
    def __init__(self, config: Config, log_name: LiteralString) -> None:
        self.__config = config
        self.__log_name = log_name
        self.__setup_logs_directory()

    def log(self, message: str | LiteralString) -> None:
        with open(self.__log_path(), 'at+', encoding="utf-8") as f:
            f.write(self.__decorate_with_timestamp(message))
            f.close()

    def __decorate_with_timestamp(self, message: str | LiteralString):
        return f'[{strftime('%Y-%m-%d %H:%M:%S', localtime())}] {message}\n'

    def __log_path(self) -> str:
        return f'{self.__config.log_path()}/{self.__log_name}.log'

    def __setup_logs_directory(self) -> None:
        try:
            self.__config.log_path().mkdir(exist_ok=True)
            if not self.__config.log_path().exists():
                print(f'Tried, but failed creating the logs dir at {self.__config.log_path()}.')
        except FileExistsError:
            print('Could not create logs directory')
