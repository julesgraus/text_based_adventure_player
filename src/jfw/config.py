from pathlib import Path


class Config:
    def __init__(self, base_path: str):
        self.root_path = Path(base_path).resolve()
        self.dict = {}

    def base_path(self):
        return self.root_path

    def app_path(self):
        return self.root_path.joinpath('app')

    def log_path(self):
        return self.root_path.joinpath('logs')

    def set(self, key: str, value):
        self.dict[key] = value
        return self

    def get(self, key: str, default=None):
        if key not in self.dict:
            return default

        return self.dict[key]
