from typing import TypedDict, Tuple

from app.dto.Character import Character


class Game(TypedDict):
    name: str
    description: str
    # characters: Tuple[Character]
