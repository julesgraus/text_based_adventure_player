from typing import TypedDict, Tuple

from app.dto.Character import Character


class Game(TypedDict):
    name: str
    description: str
    file_name: str
    file_path: str
    # characters: Tuple[Character]
